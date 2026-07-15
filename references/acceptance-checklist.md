# Acceptance Checklist

Use this checklist before considering a customer knowledge-base root deliverable complete.

## Required Root Files

- `delivery-manifest.json` exists and uses `customer-kb-delivery/v1`.
- `README.md` explains the customer knowledge base in customer-facing language.
- `AGENTS.md` exists when Codex-style agents will work in the root.
- `CLAUDE.md` exists when Claude-style agents will work in the root.
- `AGENTS.md` and `CLAUDE.md` are identical when both exist.

## Required Operating Mechanisms

- Workflow switchboard exists and names active, paused, and future workflows.
- Capability switchboard exists and maps capabilities to workflow nodes.
- System-level skill candidate list exists when installable reusable skills are needed.
- Project-level skill registry exists when customer-specific skills are needed.
- Skill installation and enablement list exists when any skill needs installation, validation, or activation.
- AI boundary or execution rules exist for sensitive domains.
- Validation records directory exists for first-run evidence.
- Delivery scale and runtime stage match the evidence in the manifest.
- Rollback strategy and named ownership exist at the level required by the selected scale.

## Clean Customer Surface

The customer root must not expose internal OPC mechanisms.

Reject the deliverable if the customer root contains:

- OPC internal paths.
- OPC sync mechanism documents.
- `from_opc`.
- `source_catalog`.
- Internal redaction notes.
- Private customer names from other projects.
- Ghost/G鬼总 personal context.

Customer-facing project skill types should be:

- `delivered`
- `custom`
- `training`

## Skill Layer Checks

System-level skills:

- Are reusable tool capabilities.
- Are listed only if relevant to the customer.
- Have a status such as `candidate`, `manual`, `on`, or `blocked`.
- Do not expose the full delivery-machine skill catalog.

Project-level skills:

- Serve a specific workflow node.
- Have read scope, write scope, and fallback.
- Use business-action names.
- Do not bypass workflow or capability switches.

## Workflow Checks

Every active workflow must include:

```text
input
-> judgment
-> processing
-> output
-> review
-> sedimentation
-> feedback
```

If a workflow does not form a loop, keep it as a task, template, or capability instead.

## Directory Checks

- Top-level directories are ordered by operating sequence.
- Names use the customer's business language.
- The directory does not copy OPC names blindly.
- Main knowledge assets do not exceed four levels unless an `assets/` exception is explicit.
- Sensitive materials have a private or governed location.

## Handoff Checks

Before handoff, produce or verify:

- First workflow walkthrough.
- First three templates or forms needed for actual use.
- Skill install/enablement notes.
- Human confirmation points.
- Known blockers and next upgrade list.
- Delivery manifest, validator result, rollback instructions, and current runtime stage.

## Machine Validation

Before handoff, run:

```bash
python scripts/validate_customer_kb.py --root <customer-root> --manifest <customer-root>/delivery-manifest.json
```

Do not report `accepted` or `operational` when validation fails. `accepted` and `operational` also require a passing first-run record and validation evidence.

## Final Acceptance Output

When reporting completion, include:

```text
Status:
Root path:
Active workflow:
Enabled mechanisms:
Pending decisions:
Validation performed:
Delivery scale:
Runtime stage:
Manifest:
Rollback:
```
