# QA Automation MCP Server (Python)

A **Model Context Protocol (MCP) server** in Python that connects an LLM
(Claude) with QA tooling — a **test management system (Allure TestOps)** and
**GitHub** — so test artifacts can be created and maintained from the assistant.

## What it does

Exposes MCP tools that let the assistant:

- **create and update test cases**;
- **build and edit checklists**;
- **create test plans**;
- link these to GitHub.

It turns natural-language requests into real test-management changes without
manual click-work.

## Stack

`Python` · `MCP (Model Context Protocol)` · test management system API ·
GitHub API

<!-- TODO: add what you want public — MCP SDK/version, transport
     (stdio / HTTP), and a repo link if it lives separately. -->

## Why it matters

- Removes repetitive manual work in the test-management UI.
- Keeps test cases / plans consistent and close to code and CI.
- Shows building on the MCP standard to integrate an LLM with real engineering
  systems (auth, API clients, tool schemas).

## My role

Designed and implemented the server end to end: the tool surface (test cases,
checklists, test plans) and the integrations with the test-management system,
GitHub and the assistant.
