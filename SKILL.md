---
name: kb-foundry
description: "Design, scaffold, validate, and hand off customer-facing knowledge-base operating systems from business diagnosis through lifecycle mapping, workflow packages, capability switches, safe directory creation, AI execution rules, first-run evidence, rollback, training, and upgrades. Use when a user asks to create, configure, productize, audit, repair, or deliver a client/customer knowledge base, workflow operating system, AI-enabled delivery root, capability layer, or governed customer knowledge-base package."
---

# KB Foundry

Version: v1.0-beta.3

## Core Rule

Build from the customer's business, not from a favorite directory tree. A folder scaffold is not an operational system, and a simulated walkthrough is not customer acceptance.

Use this order:

```text
five-dimensional diagnosis
-> scale and current stage
-> customer-kb-delivery/v1 manifest
-> lifecycle mapping
-> workflow packages
-> capability switches
-> customer-language directory placement
-> change preview and snapshot
-> safe scaffolding
-> machine validation
-> first workflow walkthrough
-> runtime evidence and stage promotion
-> handoff, training, rollback, and upgrade
```

Do not copy OPC names, private context, internal paths, sync mechanics, or another customer's materials into the customer root.

## Modes

### Explore

Use when the customer, target root, or delivery scope is unclear. Ask one question at a time using `references/onboarding-guide.md`. Produce diagnosis, recommended scale, stage `designed`, first workflow, assumptions, and a directory proposal. Do not write files.

### Design

Use when customer context is sufficient but the user has not authorized scaffolding. Produce the five dimensions, lifecycle, workflow/capability plan, `customer-kb-delivery/v1` draft, and create/merge/keep/blocked preview.

### Scaffold

Use only when the user explicitly asks to create, save, land, scaffold, or update files and names the target root. Read `references/safe-scaffolding.md`. Inspect only that root, protect existing files, require a snapshot for existing Standard/Full roots, and apply one coherent artifact group at a time.

### Audit or Repair

Use when a customer root already exists. Read the manifest, run `scripts/validate_customer_kb.py`, report evidence-backed failures, and propose a repair preview. Do not silently repair or promote stages unless the user asks.

## Workflow

1. Confirm customer and authority.
   Identify customer label, business type, target root, requested action, primary workspace/runtime, users, owners, risk boundaries, and whether writes are authorized.

2. Run the five-dimensional diagnosis.
   Read `references/five-dimensional-diagnosis.md`. Separate customer facts from assumptions. Diagnose context, assets, capabilities, workflows, and governance.

3. Choose scale and stage.
   Read `references/scale-and-stage-gates.md`. Use the smallest of Lite, Standard, or Full that can close one real workflow. Record one of: `designed`, `scaffolded`, `walkthrough_ready`, `pilot_running`, `accepted`, or `operational`.

4. Create the delivery contract.
   Read `references/delivery-manifest-contract.md` and copy `assets/delivery-manifest.template.json`. Every saved root must have `delivery-manifest.json` using `customer-kb-delivery/v1`.

5. Map the lifecycle and workflow packages.
   Use `references/workflow-package-template.md`. Every active workflow needs input, judgment, processing, output, review, sedimentation, feedback, owner, first-run fixture, evidence path, human gates, fallback, and promotion criteria.

6. Configure capability switches.
   Use `references/capability-switch-template.md` and `assets/Capability_Switchboard.template.md`. Bind every skill, agent, CLI, rule, template, automation, or external tool to a workflow node. Define runtime, read/write scopes, dependencies, owner, human confirmation, fallback, evidence, close impact, and retirement condition.

7. Translate into customer-language directories.
   Start from `assets/customer-kb-directory-template.md`, then remove, merge, rename, and reorder based on the diagnosed lifecycle. Lite must not inherit the full template by default.

8. Configure the AI execution layer.
   Add root rules only for the runtimes the customer uses. Keep `AGENTS.md` and `CLAUDE.md` byte-identical when both exist. Use the system-skill, project-skill, installation, workbench, and AI-boundary templates only when the selected scale requires them.

9. Preview and scaffold safely.
   Follow `references/safe-scaffolding.md`. Mark every planned path as create, merge, keep, replace-with-approval, rename, conflict, or blocked. Never recursively overwrite a customer root.

10. Validate the customer root.
    Run:

    ```bash
    python scripts/validate_customer_kb.py --root <customer-root> --manifest <customer-root>/delivery-manifest.json
    ```

    Fix or report missing artifacts, path traversal, broken workflow/capability references, blocked required capabilities, mismatched agent rules, missing evidence, and internal information leaks. The validator is read-only.

11. Prepare and run the first workflow.
    Use `references/first-workflow-walkthrough.md` and `references/first-day-checklist.md`. Use a real or approved representative input, record human confirmation points, expected output, actual output, blockers, and fallback.

12. Record evidence and promote honestly.
    Read `references/evidence-and-upgrade.md` and copy `assets/validation-record.template.md`. Promote one stage at a time. `accepted` and `operational` require a passing first run and recorded evidence.

13. Hand off and train.
    Use `references/acceptance-checklist.md`. Deliver current stage, scale, manifest, validator result, owners, first-run status, known blockers, rollback steps, training path, and evidence-based upgrade triggers.

## Scale Rules

- Lite: one workflow, minimal directories, capability switchboard, first-run fixture, and validation records.
- Standard: Lite plus controlled skill/capability growth, AI boundaries, install plan, ownership, upgrade log, and snapshot.
- Full: Standard plus formal diagnosis, lifecycle map, workflow packages, training, handoff, rollback, and acceptance evidence.

Do not choose Full because the customer is important. Choose it only when workflow, risk, roles, and delivery evidence require it.

## Runtime Assets

- `assets/scripts/hybrid_search.py`: zero-dependency Chinese/English local search with hidden-directory exclusions and self-test.
- `scripts/validate_customer_kb.py`: read-only delivery manifest, cross-reference, stage, path, and clean-surface validator.
- `examples/lawyer-firm/`: Standard professional-service reference at stage `walkthrough_ready`; it is not represented as real customer acceptance.

Run runtime self-tests with:

```bash
python assets/scripts/hybrid_search.py --self-test
python scripts/validate_customer_kb.py --self-test
```

## Output

For exploration, return:

- customer facts and assumptions
- five-dimensional diagnosis
- recommended scale and current stage
- first workflow and required capabilities
- customer-language directory proposal
- missing information and next decision

For a saved delivery, additionally return:

- `delivery-manifest.json`
- change preview and snapshot/rollback plan
- created/merged/kept/blocked path report
- validator result
- first-run fixture and record
- ownership, training, handoff, and upgrade conditions

## Boundaries

- Preserve customer confidentiality and data minimization.
- Do not write by default; require explicit file-generation authority and a named target root.
- Scaffolding authority does not authorize skill installation, external sync, API setup, publishing, messaging, or customer-facing delivery.
- Do not replace existing root rules, customer context, governance, or high-value assets without explicit approval and rollback.
- Do not enable automation before registering its workflow node, capability switch, scopes, human gate, fallback, and evidence plan.
- Do not expose the delivery machine's full skill catalog; curate only customer-relevant system skills.
- Do not claim `accepted` or `operational` from structure, templates, or simulated runs.
- When runtime or platform availability is uncertain, mark the capability blocked/manual and provide a human fallback.

## References

- `references/onboarding-guide.md`: read for first-time or vague requests.
- `references/five-dimensional-diagnosis.md`: read before architecture design.
- `references/scale-and-stage-gates.md`: read to choose delivery scale and runtime stage.
- `references/delivery-manifest-contract.md`: read for `customer-kb-delivery/v1`.
- `references/workflow-package-template.md`: read for formal workflow packages.
- `references/capability-switch-template.md`: read for capability registration.
- `references/safe-scaffolding.md`: read before creating or changing a customer root.
- `references/first-workflow-walkthrough.md`: read before the first workflow run.
- `references/first-day-checklist.md`: read for day-one onboarding.
- `references/evidence-and-upgrade.md`: read for validation evidence and promotion.
- `references/acceptance-checklist.md`: read before handoff or completion claims.
- `assets/delivery-manifest.template.json`: copy for every saved customer root.
- `assets/validation-record.template.md`: copy for first runs and capability tests.
- `assets/customer-kb-directory-template.md`: adapt; never copy blindly.
- `assets/workbench-template.md`: adapt for the daily entry point.
- `assets/Capability_Switchboard.template.md`: adapt for workflow-bound capabilities.
- `assets/System_Skill_Candidates.template.md`: use for Standard/Full curated system skills.
- `assets/Project_Skill_Registry.template.md`: use for customer-specific skills.
- `assets/Skill_Install_And_Enablement.template.md`: use for controlled installation and rollback.
