# Evidence and Upgrade

Use runtime evidence to promote stages, enable capabilities, and decide upgrades.

## Validation Record

Record each first run, capability test, failure, rollback, and customer acceptance with:

```yaml
record_id:
date:
project_id:
workflow_id:
stage_before:
stage_after:
fixture_or_real_input:
expected_output:
actual_output:
capabilities_used:
human_confirmations:
result: pass | fail | blocked
blockers:
evidence_paths:
rollback_used:
owner:
next_action:
```

## Evidence Strength

- `simulated`: generated example or dry run; proves only structural readiness.
- `representative`: approved fixture close to real work; supports walkthrough readiness.
- `real_run`: real customer workflow with governed data; supports pilot evidence.
- `accepted`: customer or named owner confirms agreed acceptance criteria.
- `repeated`: multiple successful runs show the workflow is operational.

Do not use simulated or representative evidence to claim customer adoption.

## Capability Promotion

- Start new optional capabilities as `manual` or `experimental`.
- Promote to `on` only after a recorded pass inside the served workflow node.
- Mark `blocked` when runtime, permission, data, or dependency is missing.
- A blocked capability must have a human fallback.
- Retire only with recorded close impact and asset-preservation action.

## Workflow Promotion

- `experimental` -> `on`: at least one complete real run, explicit owner, no blocked required capability, and a review record.
- `on` -> `paused`: record why, preserve assets, and define the reactivation condition.
- Any status -> `retired`: preserve reusable assets, remove active triggers, and record the replacement or reason.

## Upgrade Trigger

Upgrade only when evidence shows one of:

- the same blocker recurs
- a manual node repeats enough to standardize
- a new user role requires a governed view
- current search, template, or capability fails acceptance
- scale/profile requirements genuinely increase

Do not add directories, skills, or automations merely because they are available.
