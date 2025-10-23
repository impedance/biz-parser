# Progress Log — BizDocument Parser

## Status Summary (2025-10-23)
- ✅ PRD established outlining scope, success metrics, and stakeholders.
- ✅ Execution plan (`plan.md`) rewritten for coding-agent workflow.
- ✅ Memory Bank initialised with foundational context.
- ✅ Spec fixtures transcribed; see `docs/spec-examples.md` and `tests/fixtures/`.
- ✅ TypeScript domain models captured in `src/models.ts` / `src/index.ts`, matching the canonical fixtures.
- ⏳ Parser implementation not started; project scaffolding is the next prerequisite.

## Upcoming Milestones
1. Scaffold parser infrastructure (tokeniser + recursive descent) with initial unit tests.
2. Wire up fixture-driven tests to validate early parser increments.
3. Establish tooling scripts (lint, typecheck, validate AICODE) alongside CI configuration.

## Risks & Watch Items
- Dictionary outputs omit the separator field even for custom delimiters—ensure downstream models do not assume it exists.
- List marker metadata beyond numbering (`kind`, bullet symbol) is not yet represented in fixtures; revisit if later requirements demand it.

## Тестовый план (2025-10-23)
- Сверить существующие фикстуры с разделами `requirements.pdf` и зафиксировать пробелы (nested `o`-маркер, смешанные списки, контент внутри пунктов).
- Доработать набор входов/выходов для отсутствующих позитивных кейсов и расширить `tests/fixtures` негативными примерами (незакрытые теги, мусорные строки в списках).
- Настроить e2e- и unit-тесты: snapshot по каждой паре текст/JSON, отдельные проверки токенизатора и диагностики ошибок.
- Обеспечить отчётливые сообщения об ошибках (линия, тип проблемы) и включить их в тесты на негативные сценарии.

## Следующие шаги (2025-10-23)
1. Утвердить формат диагностик и закрыть открытый вопрос по метаданным списков (`memory-bank/activeContext.md:15`).
2. Завести тестовый раннер (Vitest/Jest) и подключить имеющиеся фикстуры как snapshot-тесты.
3. Сформировать backlog edge-кейсов (например, вложенные `<dict>` внутри списков) и добавлять их в `tests/fixtures` до начала реализации парсера.
