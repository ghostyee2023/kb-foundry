# Safe Scaffolding

Use this workflow whenever the user asks to create, scaffold, land, migrate, or update a customer knowledge-base root.

## Phases

1. **Plan**
   - Resolve the exact customer root.
   - Confirm it is not the delivery system's own root.
   - Inventory only the target root; do not scan unrelated locations.
   - Produce the scale, artifact list, directories, and planned changes.

2. **Preview**
   - Mark every path as `create`, `merge`, `keep`, `conflict`, or `blocked`.
   - Show existing root rules, customer files, and high-risk conflicts.
   - Stop when the target, customer, or overwrite choice is ambiguous.

3. **Snapshot**
   - Before modifying an existing root, create or point to a customer-approved backup/snapshot.
   - Record snapshot location and restore steps in the delivery manifest.
   - A new empty root may record `snapshot_required: false` with a reason.

4. **Apply**
   - Write one coherent artifact group at a time.
   - Never recursively overwrite an existing customer root.
   - Never replace `AGENTS.md`, `CLAUDE.md`, customer context, or governance rules without explicit approval.
   - Preserve customer language and existing assets; merge only with a reviewed plan.

5. **Validate**
   - Run `scripts/validate_customer_kb.py` against the root and manifest.
   - Run the shipped search tool when included.
   - Record failures as blockers; do not relabel them as accepted.

6. **Walk through and hand off**
   - Use one real or approved representative input.
   - Record the first-run result and human confirmation points.
   - Deliver known blockers, rollback steps, ownership, and next upgrade conditions.

## Path Rules

- Keep manifest paths relative to the customer root.
- Reject absolute paths and `..` traversal in customer-facing configuration.
- Keep every write inside the resolved customer root or the explicitly named delivery output directory.
- Do not write customer material into this skill repository, OPC internals, public examples, or shared method assets.

## No-Silent-Overwrite Rule

For every existing file, choose exactly one:

- `keep`: no change
- `merge`: reviewed field-level merge
- `replace`: explicit customer approval plus snapshot
- `rename`: preserve old file and add a new customer-facing path
- `blocked`: unresolved conflict; do not write

Do not infer replacement permission from "build a knowledge base" or "generate files".

## External Actions

Scaffolding authority does not authorize skill installation, external sync, API setup, publishing, messaging, or customer delivery. Treat each as a separate capability and permission boundary.
