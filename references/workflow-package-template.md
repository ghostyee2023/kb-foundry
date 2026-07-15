# Workflow Package Template

Use this template when a customer workflow needs to become a removable operating unit.

## Registration Fields

```yaml
flow_id:
workflow_name:
status: draft
business_goal:
owner:
entry_points:
input_sources:
lifecycle_chain:
  - input:
  - judgment:
  - processing:
  - output:
  - review:
  - sedimentation:
  - feedback:
main_directory:
read_scope:
write_scope:
required_capabilities:
optional_capabilities:
automation_policy:
workspace_policy:
outputs:
review_method:
feedback_targets:
human_confirmation_points:
first_run_fixture:
expected_first_output:
run_evidence_path:
promotion_gate:
shutdown_actions:
retirement_actions:
rollback_actions:
acceptance_criteria:
```

## Design Rules

- A workflow package must be a complete loop, not a single task.
- A directory is not a workflow. A workflow uses directories as asset destinations.
- A capability is not a workflow. A capability serves one or more workflow nodes.
- If a workflow cannot be closed independently, merge it into a larger workflow.
- If a workflow is only a one-time setup action, record it as a delivery task, not a recurring workflow package.
- Every active workflow must have an owner, first-run fixture, evidence path, and promotion gate.
- Product output, customer acceptance, and workflow evidence are separate. Do not promote a workflow merely because its files exist.

## Common Customer Workflows

- lead_to_proposal_flow: clue collection -> qualification -> diagnosis -> proposal -> follow-up -> case reuse
- content_engine_flow: input collection -> topic decision -> drafting -> publishing -> data review -> method reuse
- training_delivery_flow: learner input -> curriculum planning -> lesson delivery -> Q&A -> review -> course asset upgrade
- project_delivery_flow: requirement intake -> plan -> execution -> acceptance -> review -> SOP upgrade
- knowledge_ingest_flow: raw material -> classification -> extraction -> carding -> index -> reuse
- governance_flow: issue signal -> rule judgment -> fix -> evidence -> rule update -> workspace feedback
