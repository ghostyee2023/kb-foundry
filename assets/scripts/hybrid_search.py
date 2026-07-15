#!/usr/bin/env python3
"""Zero-dependency local search for a customer knowledge-base vault."""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


EXCLUDED_DIRS = {".git", ".obsidian", ".tmp", "node_modules", "__pycache__"}
DEFAULT_TOP_K = 10
MAX_FILE_BYTES = 2_000_000


@dataclass
class Document:
    path: Path
    title: str
    text: str
    tokens: list[str]


def cjk_ngrams(text: str, n_min: int = 2, n_max: int = 4) -> list[str]:
    grams: list[str] = []
    for run in re.findall(r"[\u4e00-\u9fff]+", text):
        if len(run) < n_min:
            grams.append(run)
            continue
        for size in range(n_min, min(n_max, len(run)) + 1):
            grams.extend(run[index : index + size] for index in range(len(run) - size + 1))
    return grams


def tokenize(text: str) -> list[str]:
    lowered = text.lower()
    latin = re.findall(r"[a-z0-9][a-z0-9_\-]*", lowered)
    return latin + cjk_ngrams(lowered)


def is_excluded(root: Path, path: Path) -> bool:
    parts = path.relative_to(root).parts
    return any(part in EXCLUDED_DIRS or part.startswith(".") for part in parts)


def iter_markdown_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*.md"):
        if is_excluded(root, path):
            continue
        try:
            if path.stat().st_size > MAX_FILE_BYTES:
                continue
        except OSError:
            continue
        yield path


def read_document(root: Path, path: Path) -> Document:
    text = path.read_text(encoding="utf-8-sig", errors="replace")
    title_match = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else path.stem
    relative = path.relative_to(root).as_posix()
    combined = f"{title}\n{relative}\n{text}"
    return Document(path=path, title=title, text=text, tokens=tokenize(combined))


def build_corpus(root: Path) -> list[Document]:
    return [read_document(root, path) for path in iter_markdown_files(root)]


def make_snippet(text: str, query_tokens: list[str], width: int = 160) -> str:
    compact = re.sub(r"\s+", " ", text).strip()
    lowered = compact.lower()
    hits = [lowered.find(token) for token in query_tokens if lowered.find(token) >= 0]
    first_hit = min(hits, default=0)
    start = max(0, first_hit - width // 3)
    return compact[start : start + width]


def score_documents(root: Path, docs: list[Document], query: str) -> list[dict[str, object]]:
    query_tokens = list(dict.fromkeys(tokenize(query)))
    if not query_tokens:
        return []

    doc_frequency: dict[str, int] = {}
    for document in docs:
        unique_tokens = set(document.tokens)
        for token in query_tokens:
            if token in unique_tokens:
                doc_frequency[token] = doc_frequency.get(token, 0) + 1

    average_length = sum(len(document.tokens) for document in docs) / max(len(docs), 1)
    results: list[dict[str, object]] = []

    for document in docs:
        token_counts: dict[str, int] = {}
        for token in document.tokens:
            token_counts[token] = token_counts.get(token, 0) + 1

        bm25 = 0.0
        for token in query_tokens:
            frequency = token_counts.get(token, 0)
            if frequency == 0:
                continue
            document_frequency = doc_frequency.get(token, 0)
            inverse_frequency = math.log(
                1 + (len(docs) - document_frequency + 0.5) / (document_frequency + 0.5)
            )
            k1 = 1.5
            b = 0.75
            denominator = frequency + k1 * (
                1 - b + b * len(document.tokens) / max(average_length, 1)
            )
            bm25 += inverse_frequency * (frequency * (k1 + 1)) / denominator

        relative_path = document.path.relative_to(root).as_posix()
        title_tokens = set(tokenize(document.title))
        path_tokens = set(tokenize(relative_path))
        title_boost = sum(1.5 for token in query_tokens if token in title_tokens)
        path_boost = sum(0.8 for token in query_tokens if token in path_tokens)
        score = bm25 + title_boost + path_boost
        if score <= 0:
            continue

        results.append(
            {
                "path": relative_path,
                "title": document.title,
                "score": round(score, 4),
                "snippet": make_snippet(document.text, query_tokens),
            }
        )

    results.sort(key=lambda item: (-float(item["score"]), str(item["path"])))
    return results


def run_self_test() -> int:
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        (root / "案件流程.md").write_text(
            "# 案件流程\n客户咨询进入冲突检查，然后生成代理方案。\n",
            encoding="utf-8",
        )
        (root / "培训交付.md").write_text(
            "# 培训交付\n课程需求进入方案设计和学员反馈。\n",
            encoding="utf-8",
        )
        hidden = root / ".private"
        hidden.mkdir()
        (hidden / "案件秘密.md").write_text("# 案件秘密\n不应被检索。\n", encoding="utf-8")

        documents = build_corpus(root)
        errors: list[str] = []
        if len(documents) != 2:
            errors.append(f"expected 2 visible documents, got {len(documents)}")
        results = score_documents(root, documents, "案件 冲突")
        if not results or results[0]["path"] != "案件流程.md":
            errors.append("Chinese query did not rank 案件流程.md first")
        if any(str(result["path"]).startswith(".private") for result in results):
            errors.append("hidden directory leaked into results")

        if errors:
            for error in errors:
                print(f"SELF-TEST FAIL: {error}")
            return 1
        print("SELF-TEST PASS: Chinese retrieval, ranking, and exclusions")
        return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Search customer Markdown files locally.")
    parser.add_argument("query", nargs="?", default="", help="Search query")
    parser.add_argument("--root", default=".", help="Customer vault root")
    parser.add_argument("--top-k", type=int, default=DEFAULT_TOP_K, help="Number of results")
    parser.add_argument("--self-test", action="store_true", help="Run built-in regression")
    args = parser.parse_args()

    sys.stdout.reconfigure(encoding="utf-8")
    if args.self_test:
        return run_self_test()
    if not args.query.strip():
        parser.error("provide a query or use --self-test")
    if args.top_k < 1:
        parser.error("--top-k must be at least 1")

    root = Path(args.root).resolve()
    if not root.is_dir():
        print(f"Root is not a directory: {root}", file=sys.stderr)
        return 2
    documents = build_corpus(root)
    results = score_documents(root, documents, args.query)[: args.top_k]
    payload = {
        "query": args.query,
        "root": str(root),
        "documents": len(documents),
        "count": len(results),
        "results": results,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
