# Active Context — BizDocument Parser

## Current Focus
- BizDocumentAI examples transcribed into fixtures under `tests/fixtures/` with a consolidated reference in `docs/spec-examples.md`.
- TypeScript domain models defined in `src/models.ts` / `src/index.ts` to mirror the fixture outputs.
- Next up: project scaffolding (tooling, tsconfig, tests) ahead of implementing the parser.

## Recent Decisions
- Fixture outputs mirror the PDF exactly: dictionary items are emitted as key/value objects without an explicit separator field, even when non-default separators are used.
- Nested unordered markers (`o`) are represented as nested lists attached to the parent bullet item.

## Open Questions
- Confirm whether additional metadata (e.g., list marker kind) should be exposed in the JSON model beyond what the spec examples show.
