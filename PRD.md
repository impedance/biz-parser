# BizDocument Parser PRD

## 1. Overview
- **Product name:** BizDocument Parser (working title)
- **Purpose:** Provide a deterministic parser that converts documents written in the BizDocumentAI format into structured JSON. The parser underpins downstream AI workflows by supplying clean, typed data extracted from semi-structured business texts (contracts, procedures, policies).
- **Primary artifacts:** TypeScript library exposing `parseDocument(text: string): Block`, associated domain types, validation helpers, documentation, and automated tests.

## 2. Background & Inputs
- **Specification:** `requirements.pdf` (BizDocumentAI Spec, published 2025-04-06) defines tags, nesting rules, and expected JSON outputs. Examples cover empty documents, plain text, heads, nested blocks, dictionaries with custom separators, ordered and unordered lists (including nested and mixed kinds), and lists that interleave extra block content.
- **Implementation blueprint:** `plan.md` captures a proposed multi-phase delivery plan (analysis, data modelling, parser construction, testing, packaging, etc.) targeting a robust TypeScript solution.
- **Current repo:** Contains planning/protocol docs only; parser codebase yet to be implemented. No Memory Bank files exist—must be created as the project evolves per `mb-rules.md`.

## 3. Goals & Non-Goals
### 3.1 Goals
- Parse any document conforming to the BizDocumentAI spec into a well-typed tree of blocks, lists, and dictionaries.
- Preserve business semantics: block heads, numbering, nested structure, list metadata, and dictionary key/value pairs.
- Provide an API to integrate parsing into other services or CLIs.
- Deliver developer-friendly documentation, tests, and validation scripts to ensure longevity.

### 3.2 Non-Goals
- No requirement to build authoring or editing tools for the format.
- No mandate to support binary inputs or streaming I/O (v1 reads whole text).
- Full-blown visualisation of the parsed structure is out of scope.

## 4. Success Metrics
- 100% of sample inputs in `requirements.pdf` parse into JSON structurally identical to the provided expectations.
- >90% code coverage on core parsing modules; zero lint/type errors.
- Parser handles real-world documents up to 10k lines within 2 seconds on reference hardware.
- Comprehensive README and API docs considered “ready for hand-off” by adjacent teams.

## 5. Stakeholders & Personas
- **AI Platform Engineers:** Integrate parser into enterprise RAG ingestion pipeline; expect stable API and predictable errors.
- **Business Analysts / Content Ops:** Supply domain documents; rely on parser to surface structured data without manual tagging.
- **QA & Support:** Need clear error messages and diagnostics for malformed inputs.

## 6. User Stories (Representative)
1. As an AI engineer, I can call `parseDocument(text)` and receive a JSON-ready structure to feed into downstream indexing pipelines.
2. As a support engineer, I can view descriptive parse errors pinpointing the offending line when documents violate the spec.
3. As a product engineer, I can extend the parser with new tag handlers (e.g., `<table>`) without rewriting the entire stack.

## 7. Functional Requirements
### 7.1 Document Ingestion
- Parser accepts UTF-8 text; normalises line endings to `\n`.
- Trims leading/trailing whitespace globally; ignores consecutive blank lines unless otherwise specified.

### 7.2 Core Data Structure
- Root of every document is a `Block { kind: "block" }`.
- Block fields:
  - `number?: string` — optional identifier (present when taken from lists).
  - `head?: string` — optional heading, supplied via `<head>` tag or list item text.
  - `body?: ContentNode[]` — optional, contains text fragments (`string`) and structured children (`Block`, `ListBlock`, `Dictionary`), preserving order.

### 7.3 Head & Text Handling
- `<head>` tags set `block.head`. Tag contents stripped of surrounding whitespace.
- Plain paragraphs become `string` entries in `body`, with consecutive blank lines collapsed.
- Inline text outside structured tags remains as-is (no markup parsing beyond spec tags).

### 7.4 Nested Blocks
- `<block> ... </block>` wraps a new `Block` object in the parent’s `body`.
- Support arbitrary nesting depth; parser must detect unmatched tags and raise descriptive errors.
- Empty `<block>` results in `{ kind: "block" }`.

### 7.5 Dictionaries
- `<dict sep=":">` (default `:`) defines a dictionary whose body contains key/value pairs per line.
- Each entry splits on the first occurrence of the separator; trailing spaces trimmed.
- Empty values allowed; missing separator results in parse error.
- Output shape: `{ kind: "dict", separator: string, items: Array<{ key: string; value: string }> }`.

### 7.6 Lists
- `<list kind=".">` (ordered) and `<list kind="*">` (unordered) wrap list content.
- Each non-empty line matching the list marker forms a `Block` item:
  - Ordered: prefix `^[0-9]+\.`; `number` stores the numeric part, `head` stores remainder.
  - Unordered: prefix `*` or alternate marker `o` for nested variants as per spec.
- Mixed lists require separate `<list>` sections per marker type.
- Nested lists: indentation or marker stacking indicates hierarchy; parent item body receives nested `ListBlock`.
- Additional lines inside `<list>` that do not match the list marker are appended to the current item’s `body` as text or nested blocks.
- Output shape: `{ kind: "list", listType: "." | "*" | "o" | string, items: Block[] }`.

### 7.7 Mixed Content & Ordering
- Blocks may interleave text, dictionaries, lists, and nested blocks. Parser must preserve authoring order.
- Root block’s `body` may be absent when document empty.

### 7.8 Serialization
- Primary format is plain JavaScript objects; JSON output via `JSON.stringify`.
- Optional fields omitted when undefined.

## 8. Non-Functional Requirements
- Implemented in TypeScript targeting Node 18+ runtimes.
- 100% strict type checking (`strict` in `tsconfig.json`).
- Developer tooling: ESLint, Prettier, Jest (or Vitest), Husky hooks (optional), `scripts/validate-aicode.sh` compatibility.
- Repo must conform to AICODE tagging protocol and Memory Bank workflow as the project matures.

## 9. API Surface
| Function | Description |
|----------|-------------|
| `parseDocument(text: string): Block` | Parses entire document returning root block or throws `ParseError`. |
| `parseFromFile(path: string): Promise<Block>` | Convenience helper that reads UTF-8 file and delegates to `parseDocument`. |
| `toJSON(block: Block): string` *(optional)* | Serializes block tree to JSON string with stable formatting. |

## 10. Parsing Architecture
- **Lexer layer:** Convert raw text into tokens (tags, text lines) while tracking line numbers.
- **Parser layer:** Recursive descent functions per construct (`parseBlock`, `parseDict`, `parseList`).
- **Builder utilities:** Helpers to attach child nodes, collapse whitespace, and validate invariants.
- **Error handling:** Custom `ParseError` with `message`, `line`, `column`, `context`.

## 11. Testing Strategy
- Unit tests for tokeniser, dictionary parsing, list detection, nested structures, whitespace handling.
- Golden-file / snapshot tests covering each example from `requirements.pdf`.
- Property-based tests for randomised list numbering (stretch goal).
- Negative tests: unmatched tags, malformed dictionary entries, inconsistent nesting.

## 12. Documentation & DX
- README describing format, usage examples, error glossary.
- API reference generated via TypeDoc or hand-written Markdown.
- Contribution guidelines: coding standards, testing instructions, Memory Bank maintenance reminders.

## 13. Risks & Mitigations
- **Incomplete sample extraction:** PDF text omits code blocks in plain-text export. Action: capture examples manually (screenshot/manual transcription) before implementation.
- **Ambiguity in nested list markers (`o` usage):** Clarify via exploratory tests; document assumptions.
- **Time overrun due to complex grammar:** Prioritise incremental delivery (start with blocks + heads, then dictionaries, lists).

## 14. Open Questions
1. Do we allow inline formatting aside from specified tags (e.g., `<em>`, `<strong>`)? Currently assumed *no*.
2. How should parser behave on unknown tags? Current stance: raise `ParseError`, but configurable tolerance may be needed.
3. Should dictionary `separator` be exposed in output even when default `:`? Proposed: yes for clarity.
4. Is there a canonical way to signal list nesting (indentation vs repeated tags)? Need confirmation from spec maintainer.

## 15. Timeline (Indicative)
| Week | Milestones |
|------|------------|
| 1 | Confirm requirements, establish repo scaffolding, implement core types & tokeniser. |
| 2 | Implement block & dictionary parsing; add unit tests. |
| 3 | Implement list parsing (ordered, unordered, nested, mixed). |
| 4 | Finalise error handling, documentation, CI, and publish initial release. |

## 16. Acceptance Criteria
- PRD signed off by engineering lead and AI platform PM.
- Prototype parser passes all sample cases and core unit tests.
- Documentation reviewed and merged alongside initial code baseline.

---
Prepared by: Codex Agent  
Date: 2025-10-23
