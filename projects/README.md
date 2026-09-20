# Daniel Chaykin — QA Automation Engineer

QA / SDET focused on **API test automation**, CI/CD, and integrating LLMs into
QA tooling. I build test frameworks from scratch, wire them into CI with live
reporting, and automate the boring parts of test management.

## Projects

### 🔧 [API Test Automation — Backend (6 microservices)](projects/api-test-automation)
End-to-end API automation for a mobile product backend: ~75 functional tests +
19 production smoke tests across 6 services, on `pytest` + `httpx` + `pydantic`.
Two-tier production synthetic monitoring, live IMAP password-recovery flow,
OpenAPI contract-drift detection, dual Allure reports on GitHub Pages, Allure
TestOps integration, and auto-filed issues to Confluence + Slack notifications.

### 🤖 [QA Automation MCP Server (Python)](projects/qa-automation-mcp-server)
A Model Context Protocol server that connects Claude with **GitHub** and
**Allure TestOps** — creating/updating test cases, building checklists and
assembling test plans straight from the assistant.

### 📱 [UI Test Automation](projects/ui-test-automation)
Smoke + critical-path UI automation for the client app, in CI with Allure
reporting, layered on top of the broader API coverage.

## Skills

- **Languages:** Python (primary)
- **Testing:** pytest, httpx, pydantic, API/contract testing, negative testing,
  synthetic monitoring, UI automation
- **Reporting / TMS:** Allure Report, Allure TestOps
- **CI/CD:** GitHub Actions, GitHub Pages
- **Integrations:** MCP (Model Context Protocol), Slack API, Confluence/Jira,
  IMAP, OpenAPI / JSON Schema
- **Practices:** stable error-contract assertions, secret-gated soft-degrading
  CI steps, zero-mutation production checks

## Contact

<!-- TODO: keep/adjust your preferred contacts -->
- GitHub: [@DanSeagull](https://github.com/DanSeagull)
