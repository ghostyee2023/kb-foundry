# New User Onboarding Guide

Use this guide when a user is trying the skill for the first time or gives a vague request without customer context.

## When to Trigger

Trigger onboarding when any of these are true:

- The user says "新手", "第一次", "怎么用", "引导", "help", "onboarding", "不会用", or "从哪开始".
- The user invokes the skill but gives no customer context.
- The user asks what the skill can do, with no specific customer in mind.

Do not trigger onboarding when the user already provides a customer name, business type, or clear delivery request. Go straight to the workflow in SKILL.md.

## Core Principles

- Ask one question at a time. Never present a long form.
- Acknowledge each answer briefly before asking the next.
- Skip questions the user already answered in their first message.
- If the user only wants to explore, give a lightweight tour and stop. Do not force them into a full diagnosis.
- If the user gets impatient, offer to skip ahead to a first-version output based on what you have.

## Onboarding Flow

### Step 1 — Intent

Ask:

> 你是先想了解这个 skill 能做什么，还是已经有一个客户或项目想用它搭知识库？

- Explore → Step 2a
- Have a customer or project → Step 2b

### Step 2a — Lightweight Tour

Give a 3-sentence summary: this skill turns a customer's real business into a running knowledge-base operating system — diagnosing the business, designing workflows, configuring AI capabilities, and producing a deliverable directory with execution rules.

Ask:

> 你想看一个已经搭好的例子吗？

If yes, describe the lawyer-firm example in 5-6 lines: a law firm knowledge base with a case delivery workflow, intake forms, conflict checks, document drafts, and AI execution rules that mark sensitive actions for lawyer confirmation.

Ask:

> 有没有什么具体场景你想了解的？

Answer briefly, then suggest:

> 如果你有客户场景了，随时告诉我，我可以帮你从诊断开始跑一遍。

End onboarding.

### Step 2b — Customer Info Gathering

Ask these one at a time. Skip any that the user already answered.

1. 这个客户是做什么的？（行业、主要业务）
2. 客户靠什么赚钱？卖的是产品、服务、课程还是内容？
3. 你想帮客户解决的核心问题是什么？（整理资料 / 搭业务流程 / 引入 AI 协作 / 交付方案）
4. 客户大概是什么规模？（个人 / 小团队 / 公司）

After the last answer, summarize what you heard in 2-3 lines, then go to Step 3.

Also capture the primary workspace/runtime, who owns the system, and the highest-risk information when these are not already known.

### Step 3 — Recommend Scale

Based on the answers, recommend a delivery scale:

- Lite: personal, small team, unclear needs, or pilot.
- Standard: stable business, wants AI collaboration, needs workflow and capability switches.
- Full delivery: consulting delivery, AI transformation, organizational knowledge base, long-term maintenance.

Explain the recommendation in one sentence.

Ask:

> 这个规模你觉得合适吗？还是想先从轻量版开始看看效果？

- User agrees → Step 4
- User wants to adjust → adjust and continue

### Step 4 — Quick Diagnosis

Run the minimal five-dimensional diagnosis using `references/five-dimensional-diagnosis.md`. Use only what the user has told you. Do not invent details.

Output:

```text
客户：
业务类型：
收入模式：
核心业务流（初步判断）：
主要输入：
主要输出：
可复用资产：
高风险信息：
缺失信息：
推荐第一版范围：
```

Then show a first-version directory proposal based on `assets/customer-kb-directory-template.md`, renamed for the customer's business language.

Keep the output at stage `designed`. A proposal is not yet scaffolded or ready for customer acceptance.

### Step 5 — Next Action

Tell the user what they can do next, picking the most relevant:

- If information is sufficient: 我可以先生成变更预览和交付清单；你确认后再创建目录、业务流包和能力开关。
- If key information is missing: 还缺几个关键信息：（list them）。回答后我继续。
- If the user wants to see a sample: 我可以展示一个类似行业的已搭好案例。
- If the user wants files: 告诉我明确的客户根目录；我先检查冲突、输出 create/merge/keep/blocked 预览，再按你确认的方案生成。

End with one clear recommended next step.
