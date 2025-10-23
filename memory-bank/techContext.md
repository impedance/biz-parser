# Tech Context — BizDocument Parser

## Primary Stack
- **Language:** TypeScript (strict mode), targeting Node.js 18+.  
- **Tooling:** ESLint, Prettier, Jest/Vitest for testing, TypeDoc (optional) for API documentation.  
- **Build:** `tsc` emitting ESM/CJS as needed, artefacts placed in `dist/`.

## Project Structure (planned)
- `src/` — domain models, parser modules, error utilities.
- `tests/` — unit tests and integration suites using fixtures from the spec.
- `tests/fixtures/` — manually transcribed input/output pairs from `requirements.pdf`.
- `docs/spec-examples.md` — quick reference to canonical samples.
- `scripts/` — helper utilities (`validate-aicode.sh`, snapshot runners).

## Operational Practices
- Use `rg` for repository searches, avoiding `grep` unless unavailable.
- Respect sandbox/approval settings when running commands.
- Maintain AICODE comments per `agent-rules.md`; run `scripts/validate-aicode.sh` after modifying tagged comments.
- Keep Memory Bank updated at session start/end, especially `activeContext.md` and `progress.md`.
