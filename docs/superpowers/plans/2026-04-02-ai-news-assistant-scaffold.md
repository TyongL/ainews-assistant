# AI News Assistant Scaffold Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create an OpenClaw-installable `ai-news-assistant` repository scaffold that packages the approved AI资讯助手 workflow as a reusable project.

**Architecture:** Build a documentation-first skill repository with a clear `SKILL.md`, install/readme guidance, prompt/config/template assets, and minimal script entrypoints. Keep runtime code intentionally thin in v0 so OpenClaw can learn the workflow and future implementation can fill in Feishu integrations without restructuring the repo.

**Tech Stack:** Markdown, JSON, Python 3, npm package metadata

---

## Chunk 1: Planning And Repository Layout

### Task 1: Define the repository structure

**Files:**
- Create: `D:\工作\AIProject\项目\2026-04-02_AI资讯助手\ai-news-assistant\README.md`
- Create: `D:\工作\AIProject\项目\2026-04-02_AI资讯助手\ai-news-assistant\SKILL.md`
- Create: `D:\工作\AIProject\项目\2026-04-02_AI资讯助手\ai-news-assistant\package.json`
- Create: `D:\工作\AIProject\项目\2026-04-02_AI资讯助手\ai-news-assistant\.gitignore`

- [ ] Step 1: Create the root repository files with installation, role, and package metadata
- [ ] Step 2: Verify the repository root reflects an OpenClaw-installable layout

### Task 2: Add configuration and prompt assets

**Files:**
- Create: `D:\工作\AIProject\项目\2026-04-02_AI资讯助手\ai-news-assistant\config\default-config.json`
- Create: `D:\工作\AIProject\项目\2026-04-02_AI资讯助手\ai-news-assistant\config\feishu-schema.md`
- Create: `D:\工作\AIProject\项目\2026-04-02_AI资讯助手\ai-news-assistant\prompts\ingest.md`
- Create: `D:\工作\AIProject\项目\2026-04-02_AI资讯助手\ai-news-assistant\prompts\companion.md`
- Create: `D:\工作\AIProject\项目\2026-04-02_AI资讯助手\ai-news-assistant\prompts\archive.md`
- Create: `D:\工作\AIProject\项目\2026-04-02_AI资讯助手\ai-news-assistant\prompts\script.md`

- [ ] Step 1: Write default configuration for workflow state, statuses, and Feishu-facing structure
- [ ] Step 2: Write prompt assets for ingest, reading, archive, and script generation stages
- [ ] Step 3: Verify naming and scope align with the approved product design

## Chunk 2: Templates, Examples, And Script Entrypoints

### Task 3: Add document templates and examples

**Files:**
- Create: `D:\工作\AIProject\项目\2026-04-02_AI资讯助手\ai-news-assistant\templates\daily_report.md`
- Create: `D:\工作\AIProject\项目\2026-04-02_AI资讯助手\ai-news-assistant\templates\deep_note.md`
- Create: `D:\工作\AIProject\项目\2026-04-02_AI资讯助手\ai-news-assistant\templates\script.md`
- Create: `D:\工作\AIProject\项目\2026-04-02_AI资讯助手\ai-news-assistant\examples\sample_input.md`
- Create: `D:\工作\AIProject\项目\2026-04-02_AI资讯助手\ai-news-assistant\examples\sample_note.md`
- Create: `D:\工作\AIProject\项目\2026-04-02_AI资讯助手\ai-news-assistant\examples\sample_script.md`

- [ ] Step 1: Create reusable markdown templates for the main Feishu document types
- [ ] Step 2: Add example artifacts that show the intended output quality and flow
- [ ] Step 3: Verify examples match the templates and product workflow

### Task 4: Add minimal script entrypoints

**Files:**
- Create: `D:\工作\AIProject\项目\2026-04-02_AI资讯助手\ai-news-assistant\scripts\ingest_news.py`
- Create: `D:\工作\AIProject\项目\2026-04-02_AI资讯助手\ai-news-assistant\scripts\feishu_sync.py`
- Create: `D:\工作\AIProject\项目\2026-04-02_AI资讯助手\ai-news-assistant\scripts\generate_note.py`
- Create: `D:\工作\AIProject\项目\2026-04-02_AI资讯助手\ai-news-assistant\scripts\generate_script.py`

- [ ] Step 1: Create minimal Python CLI scripts with clear TODO boundaries and argument parsing
- [ ] Step 2: Ensure each script can run with `--help` and communicate intended responsibilities
- [ ] Step 3: Keep implementation thin; no fake Feishu integration logic beyond placeholders

## Chunk 3: Verification

### Task 5: Verify scaffold completeness

**Files:**
- Verify: `D:\工作\AIProject\项目\2026-04-02_AI资讯助手\ai-news-assistant\`

- [ ] Step 1: List created files to confirm expected structure exists
- [ ] Step 2: Run `python scripts\ingest_news.py --help`
- [ ] Step 3: Run `python scripts\generate_note.py --help`
- [ ] Step 4: Run `python scripts\generate_script.py --help`
- [ ] Step 5: Summarize install and next-step guidance for OpenClaw

Plan complete and saved to `docs/superpowers/plans/2026-04-02-ai-news-assistant-scaffold.md`. Ready to execute.
