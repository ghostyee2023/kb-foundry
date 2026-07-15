# Capability Switch Template

Use this template when configuring the tools, skills, agents, templates, rules, or automations a customer knowledge base can call.

## Capability Fields

```yaml
capability_id:
capability_name:
category:
implementation_type:
provider_type:
provider_name:
runtime:
config_surface:
default_status:
served_workflows:
served_nodes:
triggers:
input_requirements:
output_type:
read_scope:
write_scope:
dependencies:
owner:
human_confirmation:
fallback:
acceptance_criteria:
validation_evidence:
shutdown_impact:
retirement_condition:
```

## Status Values

- core: required infrastructure
- on: enabled by default
- manual: only used when explicitly triggered
- experimental: available for trial
- blocked: known dependency or permission gap
- retired: no longer used

## Capability Categories

- foundational capability: reusable action across workflows, such as classification, extraction, writing, review, publishing, or sync
- business capability: assembled capability for a specific business outcome, such as client diagnosis or course delivery
- system capability: governance capability, such as routing, permissions, lint, logging, or automation evidence

## Design Rules

- A capability must name the workflow and node it serves.
- A capability must define read and write scope before automation is allowed.
- A blocked capability cannot be required by an active workflow.
- An automation is a capability, not a shortcut around workflow design.
- A template is also a capability when it controls repeated output.
- A capability cannot move from `manual` or `experimental` to `on` without validation evidence from its served workflow node.
- Every blocked capability needs a usable human fallback.
