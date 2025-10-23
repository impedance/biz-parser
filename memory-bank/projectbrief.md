# Project Brief — BizDocument Parser

## Mission
Deliver a maintainable TypeScript parser that converts BizDocumentAI-formatted text into deterministic JSON structures suitable for downstream AI workflows.

## Key Outcomes
- Accurate coverage of all constructs defined in `requirements.pdf` (blocks, heads, dictionaries, ordered/unordered lists, mixed content).
- Developer-facing package exposing `parseDocument(text: string): Block` plus supporting utilities.
- Automated tests and fixtures mirroring every example in the canonical spec.
- Documentation sufficient for hand-off to platform and support teams.

## Constraints & Considerations
- `requirements.pdf` is the sole authoritative specification. Text extraction omits code blocks, so samples must be transcribed manually when needed.
- Repository must follow AICODE protocols and maintain Memory Bank files per `mb-rules.md`.
- Target runtime: Node.js ≥ 18; TypeScript `strict` mode enforced.
