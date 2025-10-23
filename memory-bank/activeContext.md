# Active Context — BizDocument Parser

## Current Focus
- Repository setup centered on documentation (`AGENTS.md`, `PRD.md`, `plan.md`); parser code not yet started.
- Memory Bank initialised to track persistent knowledge.
- Next immediate milestone (per plan Phase A): transcribe BizDocumentAI spec examples into fixtures and create `docs/spec-examples.md`.

## Recent Decisions
- Retain `requirements.pdf`, `PRD.md`, and `plan.md` as canonical references alongside the Memory Bank.
- Dictionaries will output ordered entry arrays and include the separator value (needs confirmation once examples are captured).

## Open Questions
- Confirm precise formatting of unordered nested list markers (`o`) from the spec examples.
- Determine whether default dictionary separator `:` should be persisted explicitly in JSON output.
