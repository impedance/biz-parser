# AGENT OPERATIONS OVERVIEW

Use this document at the start of every session. It distills the mandatory rules from `agent-rules.md` and `mb-rules.md` so you can execute the protocol without missing critical steps.

## Required Reference Documents

- `agent-rules.md` — Canonical guide for AICODE comment tags (WHY / TRAP / LINK / TODO / ASK), their formats, and the session workflow for using them.
- `mb-rules.md` — Source of truth for Memory Bank usage. Defines the required files inside `memory-bank/`, update triggers, and how to maintain `activeContext.md` and `progress.md`.

Always load both documents (and every file inside `memory-bank/` when present) before planning or writing code.

## Quickstart Checklist (Run Every Session)

1. **Load Context**
   - Read this file, then open `agent-rules.md` and `mb-rules.md` end to end.
   - Enumerate all files under `memory-bank/` (create the folder if it is missing) and read each Markdown file: `projectbrief.md`, `productContext.md`, `systemPatterns.md`, `techContext.md`, `activeContext.md`, `progress.md`, plus any additional context docs.
2. **Scan AICODE Knowledge**
   - Use the recommended searches from `agent-rules.md` to list existing AICODE comments, focusing on `AICODE-WHY`, `AICODE-TRAP`, high-priority `AICODE-TODO`, and unanswered `AICODE-ASK`.
3. **Establish Plan**
   - Confirm current objectives from `activeContext.md` / `progress.md`.
   - Capture your intended steps in the planning tool before making edits (unless the task is trivial per policy).

## AICODE Comment Protocol (See `agent-rules.md` for examples)

- **Tag Types:** WHY (business rationale), TRAP (risks/gotchas), LINK (paired context), TODO (AI work queue with priority), ASK (questions for humans).
- **Format:** Single-line comments only, timestamped where required, and always prefixed with `AICODE-`.
- **Comment Style:** Match the file’s native syntax (`//`, `#`, `<!-- -->`, `/* */`, etc.). No multi-line blocks.
- **Validation:** `scripts/validate-aicode.sh` enforces formatting, single-line usage, and checks for secrets—run it when you add or modify AICODE comments.

## Session Workflow (from `agent-rules.md`)

- **Start (≈5 min):** Load AICODE tags, review high-priority TODOs, inspect outstanding ASK items, and note TRAP warnings relevant to the task.
- **During Development:** Document decisions with WHY, log hazards with TRAP, connect dependencies via LINK, queue follow-up work with TODO (prioritized), and record open questions with ASK.
- **End (≈5 min):** Clear completed TODOs, update remaining TODO priorities, convert resolved ASK items into WHY notes, and summarize AICODE-related changes in commit messages.

## Memory Bank Responsibilities (from `mb-rules.md`)

- Treat `memory-bank/` as the persistent knowledge base—agent memory resets every session.
- Maintain the core files listed earlier; additional sub-docs are welcome for complex domains.
- Update the Memory Bank whenever you uncover new patterns, finish significant work, clarify context, or respond to an explicit “update memory bank” request (which requires reviewing every file).
- Keep `activeContext.md` and `progress.md` synchronized with current focus, blocking issues, and next steps.

## Operational Notes

- Never skip reading existing Memory Bank entries; all context flows from them.
- Prefer `rg` for repository searches; honor sandbox, approval, and tooling constraints described in the CLI harness documentation.
- If `memory-bank/` is missing, create it immediately before proceeding so the persistent context can be captured.

By following this checklist and the detailed rules in the linked documents, each session starts with complete context, preserves institutional knowledge through AICODE comments, and keeps the Memory Bank authoritative.
