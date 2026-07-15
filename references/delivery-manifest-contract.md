# Customer KB Delivery Manifest Contract

Use `customer-kb-delivery/v1` as the machine-readable contract for every saved customer root. The manifest records what was designed, what exists, what may run, and what evidence supports the current stage.

## Top-Level Shape

```json
{
  "schema_version": "customer-kb-delivery/v1",
  "project_id": "client-project-id",
  "customer_label": "Customer-facing label",
  "business_type": "consulting | content | training | internal_team | ai_transformation | other",
  "delivery_scale": "lite",
  "stage": "walkthrough_ready",
  "root_path": ".",
  "business_goal": "One concrete operating outcome",
  "success_criteria": ["Observable delivery criterion"],
  "platform": {
    "primary_workspace": "Obsidian/local files/Feishu/other",
    "ai_runtimes": ["Codex"],
    "python_available": true,
    "external_integrations": []
  },
  "artifacts": {
    "root_readme": "README.md",
    "agent_rules": ["AGENTS.md", "CLAUDE.md"],
    "workbench": "00_Workbench/Today.md",
    "path_register": "00_Workbench/Path_Register.md",
    "workflow_switchboard": "10_Governance/Workflow_Switchboard.md",
    "capability_switchboard": "11_Capabilities/Capability_Switchboard.md",
    "validation_records_dir": "11_Capabilities/Validation_Records"
  },
  "directories": ["00_Workbench", "10_Governance", "11_Capabilities"],
  "risk_boundaries": [
    {
      "risk": "Sensitive customer material",
      "protected_scope": "Private customer files",
      "human_gate": "Named owner confirms external use",
      "fallback": "Keep local and produce a redacted draft"
    }
  ],
  "workflows": [],
  "capabilities": [],
  "first_run": {},
  "validation_evidence": [],
  "rollback": {},
  "ownership": {}
}
```

## Workflow Record

```json
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
    "output": "Proposal",
    "review": "Owner approval",
    "sedimentation": "Reusable solution module",
    "feedback": "Win/loss and delivery feedback"
  },
  "main_directory": "06_Delivery",
  "read_scope": ["02_Inbox"],
  "write_scope": ["06_Delivery"],
  "required_capabilities": ["proposal_draft"],
  "human_confirmation_points": ["Qualification", "Price", "External send"],
  "promotion_gate": "One complete real run with a review record",
  "acceptance_criteria": ["One real request reaches an approved proposal"]
}
```

## Capability Record

```json
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
  "fallback": "Use the approved proposal template manually",
  "human_confirmation": "Owner approves price and external send",
  "acceptance_criteria": ["Draft stays within approved scope"],
  "validation_evidence": []
}
```

## First-Run Record

```json
{
  "workflow_id": "lead_to_proposal_flow",
  "fixture_path": "02_Inbox/example-request.md",
  "expected_output_path": "06_Delivery/proposal-template.md",
  "record_path": "11_Capabilities/Validation_Records/first-run.md",
  "status": "ready",
  "human_confirmation_points": ["Qualification", "Price", "External send"],
  "acceptance_criteria": ["User can explain the complete flow"]
}
```

## Rollback and Ownership

```json
{
  "rollback": {
    "snapshot_required": true,
    "snapshot_location": ".kb-foundry-backups/before-v1",
    "change_log": "10_Governance/Change_Log",
    "restore_steps": ["Disable new workflows", "Restore reviewed files from snapshot"]
  },
  "ownership": {
    "business_owner": "Named role",
    "system_maintainer": "Named role",
    "rule_approver": "Named role",
    "review_cadence": "Monthly"
  }
}
```

## Invariants

- Use relative paths only; reject absolute paths and `..` traversal.
- Apply the required artifact keys from `scale-and-stage-gates.md`.
- Keep at least one `experimental` or `on` workflow.
- Require all seven lifecycle nodes for every workflow.
- Require workflow owner, human confirmation points, and promotion gate.
- Map every capability to an existing workflow and lifecycle node.
- Do not let an active workflow require a `blocked` or `retired` capability.
- Require every `on` capability to reference existing passing validation evidence.
- Keep all read/write scopes inside the customer root.
- Require AGENTS/CLAUDE equality when both are delivered.
- Require a first-run record for `walkthrough_ready` and later stages.
- Require passing first-run and accepted-strength validation evidence for `accepted`; require repeated evidence for `operational`.
- Keep rollback steps and named ownership for Standard and Full delivery.
- Run clean-surface lint before customer handoff.

## Validation

```bash
python scripts/validate_customer_kb.py --root <customer-root> --manifest <customer-root>/delivery-manifest.json
```

The validator is read-only. It does not create, overwrite, move, or delete customer files.
