# Scale and Stage Gates

Choose the smallest delivery that can run one real workflow. Scale controls required artifacts; stage records evidence, not optimism.

## Scale Profiles

### Lite

Use for an individual, pilot, or small team with one core workflow.

Require artifact keys:

- `root_readme`
- `agent_rules`
- `workbench`
- `path_register`
- `workflow_switchboard`
- `capability_switchboard`
- `validation_records_dir`

Require one active or experimental workflow, only the capabilities needed by that workflow, one first-run fixture, and one review/feedback destination.

### Standard

Use for a stable business that needs repeated AI collaboration and controlled capability growth.

Require every Lite artifact plus:

- `system_skill_candidates`
- `project_skill_registry`
- `skill_install_plan`
- `ai_boundary`
- `upgrade_log`

Require explicit capability dependencies, read/write scopes, human gates, fallback, and first-run record path.

### Full

Use for organizational delivery, paid transformation work, or long-term multi-workflow operation.

Require every Standard artifact plus:

- `diagnosis_report`
- `lifecycle_map`
- `workflow_packages`
- `training_plan`
- `handoff_report`
- `rollback_plan`

Require named owners, multiple workflow packages only when each can close independently, training evidence, rollback procedure, and acceptance evidence.

## Runtime Stages

Use only these stages:

| Stage | Meaning | Promotion gate |
| --- | --- | --- |
| `designed` | Diagnosis and architecture exist | Customer scope and scale are explicit |
| `scaffolded` | Required directories and initial files exist | Manifest paths resolve and clean-surface lint passes |
| `walkthrough_ready` | First workflow fixture, output target, and human gates are prepared | Validator passes and user can start the walkthrough |
| `pilot_running` | A real workflow run is in progress | A run record exists and blockers are tracked |
| `accepted` | Customer accepted the agreed delivery | First run passed and acceptance evidence is recorded |
| `operational` | Customer can run and govern the system without delivery-side intervention | Repeated run evidence, owner, upgrade, and rollback mechanisms exist |

Do not skip from `designed` to `accepted`. A directory tree is not an operational knowledge base.

## Promotion Rules

- Promote one stage at a time.
- Record evidence before changing the stage.
- A failed first run returns to `scaffolded` or `walkthrough_ready`; do not hide the failure.
- A blocked required capability prevents promotion to `pilot_running`.
- `accepted` and `operational` require `first_run.status: pass` and non-empty validation evidence.
- Scale may increase only when real workflow evidence shows the smaller profile is insufficient.
