# Matter｜Context Projection

`unit_id: unit.matter.projection`

**Scope：** Minimal sufficient recovery/context projection.

## Trigger
- Resume/cross-session/multi-skill subtask needs prior matter context.

## Negative Trigger
- No prior matter context needed.

## Essential Procedure
1. Select only current subtask-relevant source/fact/evidence/research/results/decisions/deliverables/open issues.
2. Do not replay all history.
3. Preserve `matter_id` and native status boundaries.

## Deepening Conditions
- Cross-skill or long matter.

## Exit Sufficiency
- Projection is sufficient for current work with no unrelated matter leakage.

## Professional Results
- minimal context projection

# Resume Capsule

Required minimum: `matter_id`, `matter_label`, `current_goal`, `last_material_directive`, `current_stage`, `current_result_refs`, `stale_result_refs`, `open_issue_refs`, `decision_refs`, `recent_source_changes`, `recommended_next_units`, `generated_at`.

When materially relevant and available, projection may add only the needed subset of: `party_role_refs`, `verified_fact_refs`, `disputed_fact_refs`, `evidence_issue_refs`, `research_result_refs`, `deliverable_state_refs` and affected `dependency_edges`.

Forbidden: `full conversation history`, `all source contents`, `all result bodies`, `unrelated user profile/personality`, `authorization tokens/consent inferred from prior session`.

- Recover the minimum context sufficient to continue the legal task.
- If Host has no persistence, produce/export the capsule honestly; do not claim persistent memory.
- A capsule may restore state references, never prior action authorization.
- Cross-session fallback must preserve matter_id and source/result state boundaries.
- A resumed task must not silently promote STALE, disputed or unverified objects to CURRENT/VERIFIED.

## Projection Boundary

Matter projection selects only professional state needed to resume the current subtask. If the projection crosses a skill/tool boundary, load `unit.interop.disclosure`; Least Necessary Disclosure authority remains there.
