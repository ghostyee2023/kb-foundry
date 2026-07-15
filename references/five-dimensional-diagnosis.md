# Five-Dimensional Diagnosis

Translate the customer's business into five dimensions before naming directories or choosing tools.

## 1. Context

- What does the customer sell, to whom, and for what promised result?
- Who uses, owns, maintains, and approves the system?
- What is the first operating outcome and how will it be observed?
- What is explicitly outside the first version?

## 2. Assets

- What source materials, records, templates, cases, data, and systems already exist?
- Which assets are temporary, reusable, customer-facing, confidential, or regulated?
- Where are they now, who owns them, and which may the AI read or write?
- Which formats, volumes, duplication, and quality problems affect migration?

## 3. Capabilities

- Which business actions must be performed at each workflow node?
- Which actions are manual, templated, AI-assisted, automated, blocked, or unnecessary?
- What runtime, permissions, dependencies, fallback, and human confirmation does each capability need?
- What evidence would justify promoting a capability from manual/experimental to on?

## 4. Workflows

- Which real trigger starts the work?
- How does input move through judgment, processing, output, review, sedimentation, and feedback?
- Which role owns each decision and handoff?
- Can the workflow close independently, and what real first-run fixture will prove it?

## 5. Governance

- What must never be automated, exposed, overwritten, or sent externally?
- How are workflow/capability states, run evidence, blockers, changes, and rollback recorded?
- Who approves rules, high-risk actions, and stage promotion?
- What review cadence and retirement conditions keep the system maintainable?

## Scale Recommendation

After diagnosis, choose Lite, Standard, or Full using `scale-and-stage-gates.md`. Recommend the smallest profile that can run one real workflow. Do not equate customer size with complexity; use workflow count, risk, roles, and governance needs.

## Minimal Diagnosis Output

```yaml
customer_label:
business_type:
business_goal:
success_criteria:
users_and_owners:
current_assets:
high_risk_assets:
core_workflow:
required_capabilities:
human_confirmation_points:
platform_and_runtime:
missing_inputs:
recommended_scale: lite | standard | full
recommended_stage: designed
first_run_fixture:
explicit_non_goals:
```

Every diagnosis must show which statements came from the customer and which remain assumptions.
