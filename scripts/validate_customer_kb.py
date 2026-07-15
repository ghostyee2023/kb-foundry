#!/usr/bin/env python3
"""Read-only validator for customer-kb-delivery/v1 roots and manifests."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "customer-kb-delivery/v1"
BUSINESS_TYPES = {
    "consulting",
    "content",
    "training",
    "internal_team",
    "ai_transformation",
    "other",
}
SCALES = {"lite", "standard", "full"}
STAGES = [
    "designed",
    "scaffolded",
    "walkthrough_ready",
    "pilot_running",
    "accepted",
    "operational",
]
FLOW_STATUSES = {"experimental", "on", "paused", "blocked", "retired"}
CAPABILITY_STATUSES = {"core", "on", "manual", "experimental", "blocked", "retired"}
FIRST_RUN_STATUSES = {"ready", "running", "pass", "fail", "blocked"}
LIFECYCLE_NODES = {
    "input",
    "judgment",
    "processing",
    "output",
    "review",
    "sedimentation",
    "feedback",
}
LITE_ARTIFACTS = {
    "root_readme",
    "agent_rules",
    "workbench",
    "path_register",
    "workflow_switchboard",
    "capability_switchboard",
    "validation_records_dir",
}
STANDARD_ARTIFACTS = LITE_ARTIFACTS | {
    "system_skill_candidates",
    "project_skill_registry",
    "skill_install_plan",
    "ai_boundary",
    "upgrade_log",
}
FULL_ARTIFACTS = STANDARD_ARTIFACTS | {
    "diagnosis_report",
    "lifecycle_map",
    "workflow_packages",
    "training_plan",
    "handoff_report",
    "rollback_plan",
}
REQUIRED_ARTIFACTS = {
    "lite": LITE_ARTIFACTS,
    "standard": STANDARD_ARTIFACTS,
    "full": FULL_ARTIFACTS,
}
RISK_FIELDS = {"risk", "protected_scope", "human_gate", "fallback"}
OWNERSHIP_FIELDS = {
    "business_owner",
    "system_maintainer",
    "rule_approver",
    "review_cadence",
}
ROLLBACK_FIELDS = {"snapshot_location", "change_log"}
SCAN_SUFFIXES = {".md", ".txt", ".json", ".yaml", ".yml", ".py"}
EXCLUDED_DIRS = {".git", ".obsidian", ".tmp", "node_modules", "__pycache__"}
MAX_SCAN_BYTES = 2_000_000
BANNED_PATTERNS = {
    "d:\\work\\opc": "OPC local path",
    "d:/work/opc": "OPC local path",
    "from_opc": "internal sync marker",
    "source_catalog": "internal source marker",
    "鬼总": "private operator identity",
    "01_战略上下文/": "OPC internal directory",
    "12_客户版知识库产品/": "OPC internal directory",
}


def non_empty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def require_text(obj: dict[str, Any], fields: set[str], path: str) -> list[str]:
    return [
        f"{path}.{field} must be a non-empty string"
        for field in sorted(fields)
        if not non_empty(obj.get(field))
    ]


def validate_string_list(
    value: Any, path: str, *, allow_empty: bool = False
) -> list[str]:
    if not isinstance(value, list):
        return [f"{path} must be an array"]
    if not value and not allow_empty:
        return [f"{path} must contain at least one item"]
    errors: list[str] = []
    for index, item in enumerate(value):
        if not non_empty(item):
            errors.append(f"{path}[{index}] must be a non-empty string")
    return errors


def relative_path_error(value: Any) -> str | None:
    if not non_empty(value):
        return "must be a non-empty relative path"
    normalized = value.replace("\\", "/")
    if normalized.startswith("/") or normalized.startswith("//"):
        return "must not be absolute"
    if re.match(r"^[A-Za-z]:", normalized):
        return "must not include a drive prefix"
    parts = [part for part in normalized.split("/") if part not in {"", "."}]
    if ".." in parts:
        return "must not contain '..' traversal"
    return None


def resolve_under(root: Path, value: str) -> Path | None:
    if relative_path_error(value):
        return None
    target = (root / value.replace("/", str(Path("/")))).resolve()
    return target if target == root or root in target.parents else None


def validate_declared_path(
    root: Path, value: Any, path: str, *, must_exist: bool = True
) -> list[str]:
    error = relative_path_error(value)
    if error:
        return [f"{path} {error}"]
    target = resolve_under(root, value)
    if target is None:
        return [f"{path} resolves outside the customer root"]
    if must_exist and not target.exists():
        return [f"{path} does not exist: {value}"]
    return []


def validate_path_list(
    root: Path,
    value: Any,
    path: str,
    *,
    allow_empty: bool = False,
    must_exist: bool = True,
) -> list[str]:
    errors = validate_string_list(value, path, allow_empty=allow_empty)
    if errors:
        return errors
    for index, item in enumerate(value):
        errors.extend(
            validate_declared_path(root, item, f"{path}[{index}]", must_exist=must_exist)
        )
    return errors


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_artifacts(root: Path, manifest: dict[str, Any], scale: str) -> list[str]:
    path = "$.artifacts"
    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, dict):
        return [f"{path} must be an object"]

    errors: list[str] = []
    missing_keys = REQUIRED_ARTIFACTS.get(scale, set()) - set(artifacts)
    if missing_keys:
        errors.append(
            f"{path} missing required {scale} keys: {', '.join(sorted(missing_keys))}"
        )

    for key, value in artifacts.items():
        item_path = f"{path}.{key}"
        if isinstance(value, list):
            errors.extend(validate_path_list(root, value, item_path))
        else:
            errors.extend(validate_declared_path(root, value, item_path))

    agent_rules = artifacts.get("agent_rules")
    if isinstance(agent_rules, list) and len(agent_rules) > 1:
        resolved = [resolve_under(root, value) for value in agent_rules if non_empty(value)]
        existing = [path for path in resolved if path is not None and path.is_file()]
        if len(existing) == len(agent_rules):
            hashes = {file_hash(path) for path in existing}
            if len(hashes) != 1:
                errors.append("$.artifacts.agent_rules files must be byte-identical")
    return errors


def validate_platform(manifest: dict[str, Any]) -> list[str]:
    platform = manifest.get("platform")
    if not isinstance(platform, dict):
        return ["$.platform must be an object"]
    errors = require_text(platform, {"primary_workspace"}, "$.platform")
    errors.extend(validate_string_list(platform.get("ai_runtimes"), "$.platform.ai_runtimes"))
    if not isinstance(platform.get("python_available"), bool):
        errors.append("$.platform.python_available must be a boolean")
    errors.extend(
        validate_string_list(
            platform.get("external_integrations"),
            "$.platform.external_integrations",
            allow_empty=True,
        )
    )
    return errors


def validate_risks(manifest: dict[str, Any]) -> list[str]:
    risks = manifest.get("risk_boundaries")
    if not isinstance(risks, list) or not risks:
        return ["$.risk_boundaries must be a non-empty array"]
    errors: list[str] = []
    for index, risk in enumerate(risks):
        path = f"$.risk_boundaries[{index}]"
        if not isinstance(risk, dict):
            errors.append(f"{path} must be an object")
        else:
            errors.extend(require_text(risk, RISK_FIELDS, path))
    return errors


def validate_workflows(
    root: Path, manifest: dict[str, Any]
) -> tuple[list[str], dict[str, dict[str, Any]]]:
    workflows = manifest.get("workflows")
    if not isinstance(workflows, list) or not workflows:
        return ["$.workflows must be a non-empty array"], {}

    errors: list[str] = []
    by_id: dict[str, dict[str, Any]] = {}
    active_count = 0
    for index, workflow in enumerate(workflows):
        path = f"$.workflows[{index}]"
        if not isinstance(workflow, dict):
            errors.append(f"{path} must be an object")
            continue
        errors.extend(require_text(workflow, {"flow_id", "name", "owner", "promotion_gate"}, path))
        flow_id = workflow.get("flow_id")
        if non_empty(flow_id):
            normalized = flow_id.strip()
            if normalized in by_id:
                errors.append(f"{path}.flow_id duplicates an earlier workflow: {normalized!r}")
            else:
                by_id[normalized] = workflow

        status = workflow.get("status")
        if not isinstance(status, str) or status not in FLOW_STATUSES:
            errors.append(f"{path}.status must be one of {sorted(FLOW_STATUSES)}")
        elif status in {"experimental", "on"}:
            active_count += 1
        errors.extend(validate_string_list(workflow.get("entry_points"), f"{path}.entry_points"))

        lifecycle = workflow.get("lifecycle")
        if not isinstance(lifecycle, dict):
            errors.append(f"{path}.lifecycle must be an object")
        else:
            errors.extend(require_text(lifecycle, LIFECYCLE_NODES, f"{path}.lifecycle"))

        errors.extend(
            validate_declared_path(root, workflow.get("main_directory"), f"{path}.main_directory")
        )
        errors.extend(validate_path_list(root, workflow.get("read_scope"), f"{path}.read_scope"))
        errors.extend(validate_path_list(root, workflow.get("write_scope"), f"{path}.write_scope"))
        errors.extend(
            validate_string_list(
                workflow.get("required_capabilities"),
                f"{path}.required_capabilities",
                allow_empty=True,
            )
        )
        errors.extend(
            validate_string_list(workflow.get("acceptance_criteria"), f"{path}.acceptance_criteria")
        )
        errors.extend(
            validate_string_list(
                workflow.get("human_confirmation_points"),
                f"{path}.human_confirmation_points",
            )
        )

    if active_count == 0:
        errors.append("$.workflows must include at least one experimental or on workflow")
    return errors, by_id


def validate_capabilities(
    root: Path, manifest: dict[str, Any], workflows: dict[str, dict[str, Any]]
) -> tuple[list[str], dict[str, dict[str, Any]]]:
    capabilities = manifest.get("capabilities")
    if not isinstance(capabilities, list) or not capabilities:
        return ["$.capabilities must be a non-empty array"], {}

    errors: list[str] = []
    by_id: dict[str, dict[str, Any]] = {}
    for index, capability in enumerate(capabilities):
        path = f"$.capabilities[{index}]"
        if not isinstance(capability, dict):
            errors.append(f"{path} must be an object")
            continue
        errors.extend(
            require_text(
                capability,
                {"capability_id", "name", "owner", "fallback", "human_confirmation"},
                path,
            )
        )
        capability_id = capability.get("capability_id")
        if non_empty(capability_id):
            normalized = capability_id.strip()
            if normalized in by_id:
                errors.append(
                    f"{path}.capability_id duplicates an earlier capability: {normalized!r}"
                )
            else:
                by_id[normalized] = capability

        status = capability.get("status")
        if not isinstance(status, str) or status not in CAPABILITY_STATUSES:
            errors.append(f"{path}.status must be one of {sorted(CAPABILITY_STATUSES)}")

        served_workflows = capability.get("served_workflows")
        errors.extend(validate_string_list(served_workflows, f"{path}.served_workflows"))
        if isinstance(served_workflows, list):
            for flow_id in served_workflows:
                if non_empty(flow_id) and flow_id not in workflows:
                    errors.append(f"{path}.served_workflows references unknown flow {flow_id!r}")

        served_nodes = capability.get("served_nodes")
        errors.extend(validate_string_list(served_nodes, f"{path}.served_nodes"))
        if isinstance(served_nodes, list):
            for node in served_nodes:
                if non_empty(node) and node not in LIFECYCLE_NODES:
                    errors.append(f"{path}.served_nodes contains unknown node {node!r}")

        errors.extend(validate_path_list(root, capability.get("read_scope"), f"{path}.read_scope"))
        errors.extend(validate_path_list(root, capability.get("write_scope"), f"{path}.write_scope"))
        errors.extend(
            validate_string_list(
                capability.get("dependencies"), f"{path}.dependencies", allow_empty=True
            )
        )
        errors.extend(
            validate_string_list(
                capability.get("acceptance_criteria"), f"{path}.acceptance_criteria"
            )
        )
        errors.extend(
            validate_string_list(
                capability.get("validation_evidence"),
                f"{path}.validation_evidence",
                allow_empty=True,
            )
        )
        if status == "on" and not capability.get("validation_evidence"):
            errors.append(f"{path}.validation_evidence is required when status is on")

    for capability_id, capability in by_id.items():
        for dependency in capability.get("dependencies", []):
            if dependency not in by_id:
                errors.append(
                    f"capability {capability_id!r} depends on unknown capability {dependency!r}"
                )
    return errors, by_id


def validate_cross_references(
    workflows: dict[str, dict[str, Any]], capabilities: dict[str, dict[str, Any]]
) -> list[str]:
    errors: list[str] = []
    for flow_id, workflow in workflows.items():
        if workflow.get("status") not in {"experimental", "on"}:
            continue
        for capability_id in workflow.get("required_capabilities", []):
            capability = capabilities.get(capability_id)
            if capability is None:
                errors.append(
                    f"active workflow {flow_id!r} requires unknown capability {capability_id!r}"
                )
                continue
            if capability.get("status") in {"blocked", "retired"}:
                errors.append(
                    f"active workflow {flow_id!r} requires {capability.get('status')} capability {capability_id!r}"
                )
            if flow_id not in capability.get("served_workflows", []):
                errors.append(
                    f"required capability {capability_id!r} does not declare served workflow {flow_id!r}"
                )
    return errors


def validate_first_run(
    root: Path,
    manifest: dict[str, Any],
    workflows: dict[str, dict[str, Any]],
    stage: str,
) -> list[str]:
    first_run = manifest.get("first_run")
    stage_index = STAGES.index(stage) if stage in STAGES else 0
    if stage_index < STAGES.index("walkthrough_ready"):
        if first_run in ({}, None):
            return []
    if not isinstance(first_run, dict) or not first_run:
        return ["$.first_run must be a non-empty object at walkthrough_ready or later"]

    errors = require_text(first_run, {"workflow_id"}, "$.first_run")
    workflow_id = first_run.get("workflow_id")
    if non_empty(workflow_id):
        workflow = workflows.get(workflow_id)
        if workflow is None:
            errors.append("$.first_run.workflow_id must reference an existing workflow")
        elif workflow.get("status") not in {"experimental", "on"}:
            errors.append("$.first_run.workflow_id must reference an active workflow")

    errors.extend(
        validate_declared_path(root, first_run.get("fixture_path"), "$.first_run.fixture_path")
    )
    errors.extend(
        validate_declared_path(
            root, first_run.get("expected_output_path"), "$.first_run.expected_output_path"
        )
    )
    record_path = first_run.get("record_path")
    path_error = relative_path_error(record_path)
    if path_error:
        errors.append(f"$.first_run.record_path {path_error}")
    else:
        resolved = resolve_under(root, record_path)
        if resolved is None or not resolved.parent.is_dir():
            errors.append("$.first_run.record_path parent must exist inside the customer root")

    status = first_run.get("status")
    if not isinstance(status, str) or status not in FIRST_RUN_STATUSES:
        errors.append(f"$.first_run.status must be one of {sorted(FIRST_RUN_STATUSES)}")
    errors.extend(
        validate_string_list(
            first_run.get("human_confirmation_points"),
            "$.first_run.human_confirmation_points",
        )
    )
    errors.extend(
        validate_string_list(first_run.get("acceptance_criteria"), "$.first_run.acceptance_criteria")
    )

    record_target = resolve_under(root, record_path) if not path_error else None
    if stage in {"pilot_running", "accepted", "operational"}:
        if record_target is None or not record_target.is_file():
            errors.append(f"$.first_run.record_path must exist when stage is {stage}")
    if stage == "pilot_running" and status == "ready":
        errors.append("$.first_run.status cannot remain ready when stage is pilot_running")
    if stage in {"accepted", "operational"} and status != "pass":
        errors.append(f"$.first_run.status must be 'pass' when stage is {stage}")
    return errors


def validate_evidence(root: Path, manifest: dict[str, Any], stage: str) -> list[str]:
    evidence = manifest.get("validation_evidence")
    if not isinstance(evidence, list):
        return ["$.validation_evidence must be an array"]
    if stage in {"accepted", "operational"} and not evidence:
        return [f"$.validation_evidence must be non-empty when stage is {stage}"]

    errors: list[str] = []
    seen: set[str] = set()
    passing_strengths: set[str] = set()
    for index, item in enumerate(evidence):
        path = f"$.validation_evidence[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{path} must be an object")
            continue
        errors.extend(require_text(item, {"record_id", "path", "result", "evidence_strength"}, path))
        record_id = item.get("record_id")
        if non_empty(record_id):
            if record_id in seen:
                errors.append(f"{path}.record_id duplicates an earlier record: {record_id!r}")
            seen.add(record_id)
        errors.extend(validate_declared_path(root, item.get("path"), f"{path}.path"))
        if item.get("result") not in {"pass", "fail", "blocked"}:
            errors.append(f"{path}.result must be pass, fail, or blocked")
        if item.get("evidence_strength") not in {
            "simulated",
            "representative",
            "real_run",
            "accepted",
            "repeated",
        }:
            errors.append(f"{path}.evidence_strength is invalid")
        elif item.get("result") == "pass":
            passing_strengths.add(item["evidence_strength"])
    if stage == "accepted" and not passing_strengths.intersection({"accepted", "repeated"}):
        errors.append("$.validation_evidence needs accepted or repeated passing evidence")
    if stage == "operational" and "repeated" not in passing_strengths:
        errors.append("$.validation_evidence needs repeated passing evidence for operational")
    return errors


def validate_capability_evidence(
    manifest: dict[str, Any], capabilities: dict[str, dict[str, Any]]
) -> list[str]:
    evidence = manifest.get("validation_evidence")
    known_ids = {
        item.get("record_id")
        for item in evidence
        if isinstance(item, dict) and non_empty(item.get("record_id"))
    } if isinstance(evidence, list) else set()
    errors: list[str] = []
    for capability_id, capability in capabilities.items():
        for record_id in capability.get("validation_evidence", []):
            if record_id not in known_ids:
                errors.append(
                    f"capability {capability_id!r} references unknown validation evidence {record_id!r}"
                )
    return errors


def validate_rollback_and_ownership(
    root: Path, manifest: dict[str, Any], scale: str
) -> list[str]:
    errors: list[str] = []
    rollback = manifest.get("rollback")
    if not isinstance(rollback, dict):
        errors.append("$.rollback must be an object")
    else:
        if not isinstance(rollback.get("snapshot_required"), bool):
            errors.append("$.rollback.snapshot_required must be a boolean")
        errors.extend(require_text(rollback, ROLLBACK_FIELDS, "$.rollback"))
        snapshot = rollback.get("snapshot_location")
        if non_empty(snapshot) and snapshot != "not_applicable_new_root":
            errors.extend(
                validate_declared_path(
                    root, snapshot, "$.rollback.snapshot_location", must_exist=False
                )
            )
        errors.extend(
            validate_declared_path(
                root, rollback.get("change_log"), "$.rollback.change_log"
            )
        )
        errors.extend(
            validate_string_list(rollback.get("restore_steps"), "$.rollback.restore_steps")
        )

    ownership = manifest.get("ownership")
    if not isinstance(ownership, dict):
        errors.append("$.ownership must be an object")
    else:
        errors.extend(require_text(ownership, OWNERSHIP_FIELDS, "$.ownership"))

    if scale in {"standard", "full"} and isinstance(rollback, dict):
        if rollback.get("snapshot_required") is not True:
            errors.append(f"$.rollback.snapshot_required must be true for {scale} delivery")
    return errors


def iter_scannable_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in SCAN_SUFFIXES:
            continue
        parts = path.relative_to(root).parts
        if any(part in EXCLUDED_DIRS or part.startswith(".") for part in parts):
            continue
        try:
            if path.stat().st_size <= MAX_SCAN_BYTES:
                files.append(path)
        except OSError:
            continue
    return files


def lint_clean_surface(root: Path) -> list[str]:
    errors: list[str] = []
    for path in iter_scannable_files(root):
        text = path.read_text(encoding="utf-8-sig", errors="replace")
        lowered = text.lower()
        for pattern, label in BANNED_PATTERNS.items():
            haystack = lowered if pattern.isascii() else text
            needle = pattern.lower() if pattern.isascii() else pattern
            if needle in haystack:
                relative = path.relative_to(root).as_posix()
                errors.append(f"clean-surface lint: {relative} contains {label} marker {pattern!r}")
    return errors


def validate_manifest(root: Path, manifest: Any, *, content_lint: bool = True) -> list[str]:
    if not isinstance(manifest, dict):
        return ["$ must be a JSON object"]
    errors: list[str] = []

    if manifest.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"$.schema_version must equal {SCHEMA_VERSION!r}")
    errors.extend(
        require_text(
            manifest,
            {"project_id", "customer_label", "business_goal"},
            "$",
        )
    )
    business_type = manifest.get("business_type")
    if not isinstance(business_type, str) or business_type not in BUSINESS_TYPES:
        errors.append(f"$.business_type must be one of {sorted(BUSINESS_TYPES)}")
    scale = manifest.get("delivery_scale")
    if not isinstance(scale, str) or scale not in SCALES:
        errors.append(f"$.delivery_scale must be one of {sorted(SCALES)}")
        scale = "lite"
    stage = manifest.get("stage")
    if not isinstance(stage, str) or stage not in STAGES:
        errors.append(f"$.stage must be one of {STAGES}")
        stage = "designed"
    if manifest.get("root_path") != ".":
        errors.append("$.root_path must equal '.'")
    errors.extend(validate_string_list(manifest.get("success_criteria"), "$.success_criteria"))
    errors.extend(validate_platform(manifest))
    errors.extend(validate_artifacts(root, manifest, scale))
    errors.extend(validate_path_list(root, manifest.get("directories"), "$.directories"))
    errors.extend(validate_risks(manifest))

    workflow_errors, workflows = validate_workflows(root, manifest)
    errors.extend(workflow_errors)
    capability_errors, capabilities = validate_capabilities(root, manifest, workflows)
    errors.extend(capability_errors)
    errors.extend(validate_cross_references(workflows, capabilities))
    errors.extend(validate_first_run(root, manifest, workflows, stage))
    errors.extend(validate_evidence(root, manifest, stage))
    errors.extend(validate_capability_evidence(manifest, capabilities))
    errors.extend(validate_rollback_and_ownership(root, manifest, scale))
    if content_lint:
        errors.extend(lint_clean_surface(root))
    return list(dict.fromkeys(errors))


def write_fixture_file(root: Path, relative: str, text: str = "# Fixture\n") -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def make_fixture(root: Path) -> dict[str, Any]:
    root.mkdir(parents=True, exist_ok=True)
    rules = "# Customer AI Rules\nUse the registered workflow and human gates.\n"
    files = {
        "README.md": "# Customer Knowledge Base\n",
        "AGENTS.md": rules,
        "CLAUDE.md": rules,
        "00_Workbench/Today.md": "# Today\n",
        "00_Workbench/Path_Register.md": "# Paths\n",
        "10_Governance/Workflow_Switchboard.md": "# Workflows\n",
        "10_Governance/Change_Log/README.md": "# Changes\n",
        "11_Capabilities/Capability_Switchboard.md": "# Capabilities\n",
        "02_Inbox/example-request.md": "# Example request\n",
        "06_Delivery/proposal-template.md": "# Proposal template\n",
    }
    for relative, text in files.items():
        write_fixture_file(root, relative, text)
    (root / "11_Capabilities/Validation_Records").mkdir(parents=True, exist_ok=True)

    return {
        "schema_version": SCHEMA_VERSION,
        "project_id": "test-client-kb",
        "customer_label": "Test customer",
        "business_type": "consulting",
        "delivery_scale": "lite",
        "stage": "walkthrough_ready",
        "root_path": ".",
        "business_goal": "Turn one qualified request into an approved proposal",
        "success_criteria": ["One representative request reaches an approved draft"],
        "platform": {
            "primary_workspace": "local files",
            "ai_runtimes": ["Codex"],
            "python_available": True,
            "external_integrations": [],
        },
        "artifacts": {
            "root_readme": "README.md",
            "agent_rules": ["AGENTS.md", "CLAUDE.md"],
            "workbench": "00_Workbench/Today.md",
            "path_register": "00_Workbench/Path_Register.md",
            "workflow_switchboard": "10_Governance/Workflow_Switchboard.md",
            "capability_switchboard": "11_Capabilities/Capability_Switchboard.md",
            "validation_records_dir": "11_Capabilities/Validation_Records",
        },
        "directories": [
            "00_Workbench",
            "02_Inbox",
            "06_Delivery",
            "10_Governance",
            "11_Capabilities",
        ],
        "risk_boundaries": [
            {
                "risk": "Sensitive request data",
                "protected_scope": "Private customer files",
                "human_gate": "Owner approves external use",
                "fallback": "Use a redacted representative fixture",
            }
        ],
        "workflows": [
            {
                "flow_id": "lead_to_proposal_flow",
                "name": "Lead to proposal",
                "status": "experimental",
                "owner": "Business owner",
                "entry_points": ["New qualified inquiry"],
                "lifecycle": {
                    "input": "Capture request",
                    "judgment": "Qualify and route",
                    "processing": "Diagnose and draft",
                    "output": "Proposal draft",
                    "review": "Owner approval",
                    "sedimentation": "Reusable proposal module",
                    "feedback": "Win/loss review",
                },
                "main_directory": "06_Delivery",
                "read_scope": ["02_Inbox"],
                "write_scope": ["06_Delivery"],
                "required_capabilities": ["proposal_draft"],
                "human_confirmation_points": ["Qualification", "Price", "External send"],
                "promotion_gate": "One complete real run with a review record",
                "acceptance_criteria": ["One request reaches an approved proposal draft"],
            }
        ],
        "capabilities": [
            {
                "capability_id": "proposal_draft",
                "name": "Proposal draft assistance",
                "status": "manual",
                "owner": "Knowledge-base maintainer",
                "served_workflows": ["lead_to_proposal_flow"],
                "served_nodes": ["processing"],
                "read_scope": ["02_Inbox"],
                "write_scope": ["06_Delivery"],
                "dependencies": [],
                "fallback": "Use the approved template manually",
                "human_confirmation": "Owner approves price and external send",
                "acceptance_criteria": ["Draft stays within the approved scope"],
                "validation_evidence": [],
            }
        ],
        "first_run": {
            "workflow_id": "lead_to_proposal_flow",
            "fixture_path": "02_Inbox/example-request.md",
            "expected_output_path": "06_Delivery/proposal-template.md",
            "record_path": "11_Capabilities/Validation_Records/first-run.md",
            "status": "ready",
            "human_confirmation_points": ["Qualification", "Price", "External send"],
            "acceptance_criteria": ["User can explain the complete flow"],
        },
        "validation_evidence": [],
        "rollback": {
            "snapshot_required": False,
            "snapshot_location": "not_applicable_new_root",
            "change_log": "10_Governance/Change_Log",
            "restore_steps": ["Disable the experimental workflow"],
        },
        "ownership": {
            "business_owner": "Business owner",
            "system_maintainer": "Knowledge-base maintainer",
            "rule_approver": "Business owner",
            "review_cadence": "Monthly",
        },
    }


def run_self_test() -> int:
    cases: list[tuple[str, Any, bool]] = []
    roots: list[Path] = []
    temporary = tempfile.mkdtemp(prefix="kb-foundry-validator-")
    base = Path(temporary)
    try:
        valid_root = base / "valid"
        valid = make_fixture(valid_root)
        roots.append(valid_root)
        cases.append(("valid walkthrough-ready root", (valid_root, valid), True))

        traversal_root = base / "traversal"
        traversal = make_fixture(traversal_root)
        traversal["artifacts"]["workbench"] = "../outside.md"
        roots.append(traversal_root)
        cases.append(("path traversal", (traversal_root, traversal), False))

        missing_root = base / "missing"
        missing = make_fixture(missing_root)
        (missing_root / "00_Workbench/Today.md").unlink()
        roots.append(missing_root)
        cases.append(("missing required artifact", (missing_root, missing), False))

        mismatch_root = base / "mismatch"
        mismatch = make_fixture(mismatch_root)
        (mismatch_root / "CLAUDE.md").write_text("# Different rules\n", encoding="utf-8")
        roots.append(mismatch_root)
        cases.append(("mismatched agent rules", (mismatch_root, mismatch), False))

        blocked_root = base / "blocked"
        blocked = make_fixture(blocked_root)
        blocked["capabilities"][0]["status"] = "blocked"
        roots.append(blocked_root)
        cases.append(("blocked required capability", (blocked_root, blocked), False))

        leak_root = base / "leak"
        leak = make_fixture(leak_root)
        write_fixture_file(leak_root, "README.md", "# Customer\nInternal: D:/work/opc/private\n")
        roots.append(leak_root)
        cases.append(("internal path leak", (leak_root, leak), False))

        accepted_root = base / "accepted"
        accepted = make_fixture(accepted_root)
        accepted["stage"] = "accepted"
        accepted["first_run"]["status"] = "pass"
        write_fixture_file(
            accepted_root,
            "11_Capabilities/Validation_Records/first-run.md",
            "# First run\n",
        )
        roots.append(accepted_root)
        cases.append(("accepted without evidence", (accepted_root, accepted), False))

        weak_root = base / "weak-evidence"
        weak = make_fixture(weak_root)
        weak["stage"] = "accepted"
        weak["first_run"]["status"] = "pass"
        write_fixture_file(
            weak_root,
            "11_Capabilities/Validation_Records/first-run.md",
            "# First run\n",
        )
        weak["validation_evidence"] = [
            {
                "record_id": "first-run-simulated",
                "path": "11_Capabilities/Validation_Records/first-run.md",
                "result": "pass",
                "evidence_strength": "simulated",
            }
        ]
        roots.append(weak_root)
        cases.append(("accepted with weak evidence", (weak_root, weak), False))

        duplicate_root = base / "duplicate"
        duplicate = make_fixture(duplicate_root)
        duplicate["workflows"].append(copy.deepcopy(duplicate["workflows"][0]))
        roots.append(duplicate_root)
        cases.append(("duplicate workflow id", (duplicate_root, duplicate), False))

        failed = False
        for name, payload, should_pass in cases:
            root, manifest = payload
            errors = validate_manifest(root.resolve(), manifest)
            passed = not errors
            if passed != should_pass:
                failed = True
                print(f"SELF-TEST FAIL: {name}")
                for error in errors:
                    print(f"  - {error}")
            else:
                print(f"SELF-TEST PASS: {name}")
        return 1 if failed else 0
    finally:
        shutil.rmtree(base, ignore_errors=True)


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a customer knowledge-base root.")
    parser.add_argument("--root", type=Path, help="Customer root directory")
    parser.add_argument("--manifest", type=Path, help="customer-kb-delivery/v1 JSON")
    parser.add_argument("--no-content-lint", action="store_true", help="Skip leak scanning")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    parser.add_argument("--self-test", action="store_true", help="Run built-in regressions")
    args = parser.parse_args()

    sys.stdout.reconfigure(encoding="utf-8")
    if args.self_test:
        return run_self_test()
    if args.root is None:
        parser.error("--root is required unless --self-test is used")

    root = args.root.resolve()
    if not root.is_dir():
        print(f"FAIL: root is not a directory: {root}")
        return 2
    manifest_path = args.manifest.resolve() if args.manifest else root / "delivery-manifest.json"
    if not manifest_path.is_file():
        print(f"FAIL: manifest not found: {manifest_path}")
        return 2
    try:
        manifest = load_json(manifest_path)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"FAIL: cannot read manifest: {exc}")
        return 2

    errors = validate_manifest(root, manifest, content_lint=not args.no_content_lint)
    if args.format == "json":
        print(
            json.dumps(
                {
                    "root": str(root),
                    "manifest": str(manifest_path),
                    "valid": not errors,
                    "errors": errors,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    elif errors:
        print(f"FAIL {root}")
        for error in errors:
            print(f"  - {error}")
    else:
        print(f"PASS {root}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
