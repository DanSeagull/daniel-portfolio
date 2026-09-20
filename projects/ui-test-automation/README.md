# UI Test Automation

Automated UI tests — smoke and critical end-to-end user paths — run in CI with
Allure reporting.

> Generalized write-up. No employer-specific screens, flows or data.

<!-- TODO: confirm the specifics (framework / platform) so the page is accurate. -->

## Stack

`<!-- TODO: framework, e.g. XCUITest / Appium / Playwright -->` ·
`Allure Report` · `GitHub Actions`

## Approach

- **Smoke suite** — app launches and core screens load.
- **Critical happy paths** — the key user journeys end to end.
- Page-object style structure for readable, low-maintenance tests; stable
  selectors and explicit waits.
- Screenshots/attachments captured into the Allure report on failure for fast
  triage.
- UI kept as a thin critical-path layer on top of broader API coverage — most
  behavior is verified faster and more reliably at the API level, with UI
  focused on what only the client can prove.

## My role

Set up the UI automation project, the smoke/e2e cases, and their CI + reporting
integration.
