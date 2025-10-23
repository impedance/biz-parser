# BizDocument Parser Execution Plan

This plan guides coding agents through building the BizDocument parser in alignment with the BizDocumentAI specification. It complements the PRD and operational rules in `AGENTS.md`.

## 0. Canonical References
- `requirements.pdf` — primary source of truth for the BizDocumentAI format (tags, nesting, and expected JSON). **Note:** PDF text extraction omits fenced code blocks; manually transcribe input/output samples before implementation.
- `PRD.md` — product requirements distilled from the spec and program goals.
- `AGENTS.md`, `agent-rules.md`, `mb-rules.md` — session protocol, AICODE tagging rules, and Memory Bank workflow.

Always defer to `requirements.pdf` when conflicts arise.

## 1. Session Ritual for Coding Agents
1. Load `AGENTS.md`, `agent-rules.md`, `mb-rules.md`, and all Memory Bank files (create the bank if missing).
2. Capture the working intent in the planning tool (unless the task is trivial per policy).
3. Run targeted `rg` searches for existing AICODE comments relevant to the parser work.
4. Update Memory Bank entries (`activeContext.md`, `progress.md`) with new insights or completed milestones.

## 2. Phase Roadmap
### Phase A — Spec Capture & Test Assets
- Extract every example input/output pair from `requirements.pdf`. If tools miss code blocks, copy them manually into `tests/fixtures/`.
- Create a consolidated reference document (`docs/spec-examples.md`) with the raw text and expected JSON for quick lookup.
- Validate assumptions about whitespace handling (“strip and skip empty lines”), list markers, dictionary separators, and nesting by cross-checking with examples.

### Phase B — Domain Model Alignment
- Define TypeScript interfaces mirroring the spec:
  - Root `Block` with optional `head`, `number`, and ordered `body`.
  - `Dictionary` preserving separator and key/value ordering (use array of entries, not plain object, to allow duplicates and maintain order—verify against spec examples).
  - `ListBlock` capturing kind/marker metadata and `Block` items.
- Document invariants (e.g., `kind` discriminators, optional fields omitted when undefined).

### Phase C — Parser Infrastructure
- Normalise input (UTF-8, `\n` line endings) and implement a lightweight lexer/tokeniser that produces line records with line numbers, tag tokens, and raw content.
- Establish a recursive-descent parser scaffold with context-aware functions:
  - `parseDocument` → root block
  - `parseBlock`
  - `parseDictionary`
  - `parseList`
- Track parsing cursor, manage stacks for nested tags, and surface structured `ParseError` messages with line/column data.

### Phase D — Feature Implementation Sequence
1. **Plain Text & Heads**
   - Support empty documents → `{ kind: "block" }`.
   - Map paragraphs to `string` entries; collapse consecutive blank lines.
   - Parse `<head>...</head>` into `block.head`.
2. **Nested Blocks**
   - Recognise `<block>` … `</block>` pairs; allow arbitrary depth and interleaving with other content types.
3. **Dictionaries**
   - Handle `<dict sep=":">` (default `:`) and overrides.
   - Split on the first separator occurrence; allow empty values.
   - Emit ordered arrays of `{ key, value }`.
4. **Lists**
   - Implement ordered (`kind="."`) and unordered (`kind="*"`/`"o"`) lists.
   - Capture item numbers/head text per spec; support nested lists either via additional `<list>` blocks or marker conventions outlined in examples.
   - Route non-marker lines inside a list to the current item’s `body`.
5. **Mixed Content & Edge Cases**
   - Ensure mixed sequences (text + dict + list within a block) preserve order.
   - Confirm lists inside blocks and dictionaries inside list items parse correctly.

For each step, add or update fixtures and automated tests before proceeding.

### Phase E — Error Handling & Validation
- Define `ParseError` with message, line, column, and optional context snippet.
- Detect unmatched or misordered tags, malformed dictionary entries, and unsupported list markers.
- Provide configurable strict vs. permissive modes if future requirements demand (log-only vs throw).

### Phase F — Tooling, CI, Packaging
- Project scaffolding: `package.json`, `tsconfig.json` with `strict: true`, ESLint + Prettier, test runner (Jest or Vitest).
- Scripts: `build`, `test`, `lint`, `typecheck`, `spec:snapshots` (fixture runner), `validate:aicode`.
- CI workflow invoking lint, type checks, tests.
- Publishable build artefacts in `dist/` with declaration files.

### Phase G — Documentation & Knowledge Continuity
- Maintain Memory Bank (`activeContext.md`, `progress.md`) with milestone summaries, pitfalls, and open questions.
- Update `README.md` with usage examples, format overview, error glossary, and contribution guide.
- Document extension patterns (e.g., adding new tags) and any deliberate deviations from the spec.

## 3. Deliverables Checklist
- [ ] Complete fixture set mirroring every example in `requirements.pdf`.
- [ ] Type definitions (`src/models.ts`) reviewed against spec JSON.
- [ ] Parser modules with unit + integration tests for blocks, heads, dictionaries, lists, and mixed documents.
- [ ] Error handling module with negative tests.
- [ ] CI pipeline green (lint, type check, tests).
- [ ] Developer documentation and Memory Bank updates merged.

## 4. Risks & Mitigations
- **Missing example data:** Manual transcription required; schedule time in Phase A.
- **Ambiguous list nesting markers:** Prototype against sample inputs; record explicit rules in docs and Memory Bank.
- **Spec evolution:** Encapsulate parsing logic to allow new tag handlers; track pending spec questions in `progress.md`.

## 5. Open Questions (Track in Memory Bank)
1. Should default dictionary separator be omitted from JSON when it is `:`? (Spec unclear without examples.)
2. How are unordered nested markers (`o`) precisely formatted in source text?
3. Are unknown tags fatal errors or ignored content?

Resolve these by revisiting the canonical PDF or consulting project stakeholders; keep answers documented for future sessions.
