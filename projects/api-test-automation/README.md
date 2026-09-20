# API Test Automation Framework

A production-grade API test automation framework I design and build: typed
service clients, CI, live reporting, contract validation and production
synthetic monitoring.

> Generalized write-up of my approach and skills. No employer-specific
> architecture, business logic, internal tooling details, credentials or
> metrics are included.

## Stack

`Python` · `pytest` · `httpx` · `pydantic` · `allure-pytest` ·
`GitHub Actions` · `Allure Report` · `Allure TestOps` · `jsonschema`

## What I build

- **Functional + negative API coverage** for REST services behind a
  token-based auth gateway — happy paths and error paths alike.
- Assertions target a **stable machine-readable error contract**
  (`errorCode`), not brittle message text, so tests survive copy changes.
- **Typed client layer** (`src/` layout, a client per service over a thin
  `httpx` wrapper): auth headers, request/response logging into the report.
  Tests take ready sessions from fixtures instead of assembling tokens by hand.

## Highlights

- **Production synthetic monitoring** — a separate, zero-mutation smoke suite
  safe to run against production (availability + auth-gateway checks + latency
  thresholds), plus an optional authenticated tier on a dedicated test account
  that is strictly read-only / self-cleaning.
- **Live email-flow automation** — end-to-end password recovery driven by
  reading a one-time code from a test inbox over IMAP.
- **OpenAPI contract-drift detection** — responses validated against service
  OpenAPI specs (`jsonschema`); a spec violation fails the test as a
  contract drift, so doc/reality mismatches surface automatically.
- **Live reporting** — Allure HTML published to GitHub Pages with trend
  history (separate reports per environment), and results streamed into a test
  management system (Allure TestOps).
- **Feedback automation** — CI turns red runs and contract drift into tracked
  items and posts run summaries to a team chat.

## Engineering practices

- Every external integration is **gated behind secrets and degrades softly** —
  a missing secret skips that step instead of breaking CI.
- Production checks are **non-destructive by design**; anything that could
  create data is isolated and opt-in.

## My role

Designed and built the framework end to end: architecture, test suites, CI/CD,
reporting, production monitoring and the reporting/notification automations.
