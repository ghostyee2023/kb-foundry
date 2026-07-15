# Customer KB Directory Template

Rename these directories for the customer's business language. Keep the operating order.

```text
AGENTS.md
CLAUDE.md
delivery-manifest.json

00_System_Entry/
  README.md
  Path_Register.md
  Directory_Map.md
  Workflow_Index.md

01_Business_Context/
  Customer_Profile/
  Products_And_Offers/
  Strategy_Notes/
  Style_And_Standards/

02_Input_Inbox/
  Local_Input/
  Cloud_Input/
  Screenshots/
  Links/
  Raw_Materials/

03_Knowledge_Assets/
  Source_Summaries/
  Concepts_And_Methods/
  Cases/
  Risks_And_Anti_Cases/
  Reusable_Units/

04_Decision_And_Planning/
  Candidate_Ideas/
  Priority_Lists/
  Plans/
  Review_Boards/

05_Production/
  Drafts/
  Templates/
  Working_Files/
  Output_Ready/

06_Delivery/
  Client_Projects/
  SOPs/
  Proposals/
  Training_Materials/
  Demo_Assets/

07_Distribution_Or_Handoff/
  Published/
  Sent_To_Client/
  Platform_Assets/
  Handoff_Records/

08_Feedback_Data/
  Metrics/
  Customer_Feedback/
  Single_Output_Reviews/
  Case_Performance/

09_Review_Journal/
  Daily_Reviews/
  Project_Reviews/
  Decision_Reviews/
  Lessons_Learned/

10_Governance/
  Rules/
  Workflow_Switchboard.md
  Change_Log/
  Pending_Changes/
  Run_Evidence/
  AI_Execution_Rules/

11_Capabilities_And_Agents/
  Capability_Switchboard.md
  System_Skill_Candidates.md
  Project_Skill_Registry.md
  Skill_Install_And_Enablement.md
  Tool_Records/
  Agent_Roles/
  Templates/
  Project_Skills/
  Skill_Packages/
  Validation_Records/
```

## Scaling Rules

- Use `references/scale-and-stage-gates.md` before choosing directories.
- For a Lite customer, keep only the business context, one inbox, one core workflow's production/delivery paths, feedback/review, governance, capability switchboard, and validation records. Do not scaffold every directory above.
- For a small customer, merge `04_Decision_And_Planning` into `01_Business_Context` and merge `07_Distribution_Or_Handoff` into `06_Delivery` when those stages are still needed.
- For a content business, keep `04`, `05`, `07`, and `08` separate.
- For a consulting business, keep `06_Delivery` and `08_Feedback_Data` separate.
- For a team knowledge base, add role-based indexes under `00_System_Entry`.
- Avoid more than four directory levels in the main knowledge assets.

## AI Execution Layer

Every customer root that expects AI assistance should include:

- `AGENTS.md`: execution rules for Codex-style agents.
- `CLAUDE.md`: execution rules for Claude-style agents.
- `Workflow_Switchboard.md`: which end-to-end workflows are active.
- `Capability_Switchboard.md`: which capabilities can be called.
- `System_Skill_Candidates.md`: installable system-level skills curated from the delivery machine.
- `Project_Skill_Registry.md`: project-level skills available in this customer workspace.
- `Skill_Install_And_Enablement.md`: installation, activation, validation, and rollback plan.
- `AI_Execution_Rules/`: internal governance notes for AI behavior.
- `Validation_Records/`: evidence from first runs and capability tests.

Root execution rules must define read scope, write scope, high-risk boundaries, human confirmation points, and failure fallback.

## Capability Layer Templates

When generating the `11_Capabilities_And_Agents/` directory for a customer, use these templates as starting content. Fill the `{{PLACEHOLDER}}` sections based on the customer's industry and enabled workflows.

- `Capability_Switchboard.md`: use `assets/Capability_Switchboard.template.md`. Fill `{{CAPABILITIES}}` with capabilities mapped to each workflow node.
- `System_Skill_Candidates.md`: use `assets/System_Skill_Candidates.template.md`. Fill `{{INDUSTRY_SKILLS}}` based on customer industry type (content IP / consulting / training / internal team).
- `Project_Skill_Registry.md`: use `assets/Project_Skill_Registry.template.md`. Fill `{{PROJECT_SKILLS}}` with planned project-level skills for each workflow node.
- `Skill_Install_And_Enablement.md`: use `assets/Skill_Install_And_Enablement.template.md`. Fill `{{AI_TOOL}}` and `{{MINIMAL_SKILLS}}` based on customer environment.

For Standard and Full delivery, these four files are required. Lite requires the capability switchboard but may defer the system-skill, project-skill, and installation files until evidence shows they are needed.

Every saved customer root also requires `delivery-manifest.json`, created from `assets/delivery-manifest.template.json`. The manifest is the machine-readable contract for paths, workflows, capabilities, first-run evidence, ownership, and rollback.

## Skill Layering

Use two skill layers:

1. System-level skills
   - Reusable across customers.
   - Installed from a curated source catalog.
   - Examples: documents, spreadsheets, PDF, browser, Feishu integration, skill creator.

2. Project-level skills
   - Specific to the customer's business workflows.
   - Delivered with the project, created later as custom skills, or taught to the customer.
   - Must name served workflow, served node, read scope, write scope, fallback, and validation evidence.
   - Keep one project skill registry and label each customer-facing delivery type as `delivered`, `custom`, or `training`.
   - Do not expose OPC-side sync mechanics in the customer root.
