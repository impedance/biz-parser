# System Patterns — BizDocument Parser

## Architectural Overview
- **Layered parsing pipeline**  
  1. Normalise input (UTF-8, `\n` line endings).  
  2. Tokenise lines with tag recognition and line-number tracking.  
  3. Recursive-descent parser builds a tree of discriminated union types (`Block`, `Dictionary`, `ListBlock`, raw text).
- **Data model**  
  - `Block` root with optional `head`, `number`, `body` array preserving order.  
  - `Dictionary` stores explicit `separator` and ordered `{ key, value }` entries.  
  - `ListBlock` tracks `kind`/marker metadata and contains block items.  
  - Content union permits nested structures alongside plain text.

## Key Rules from Spec
- Empty documents map to `{ kind: "block" }`.  
- `<head>` applies to the current block only.  
- `<block>` sections can nest arbitrarily; unmatched tags are errors.  
- Dictionaries split on the first occurrence of the declared separator; empty values allowed.  
- Lists may be ordered (`.`) or unordered (`*`, `o`), support nesting, and treat non-marker lines inside a list as part of the current item’s body.

## Extension Strategy
- Encapsulate tag handlers (`parseDictionary`, `parseList`, etc.) so new constructs can be added without rewriting the parser core.  
- Keep discriminated unions and utility builders together to maintain type safety.  
- Maintain fixtures and snapshot tests for each spec scenario to guard against regressions.
