# AI News Assistant

AI News Assistant is an OpenClaw-installable workflow package for a Feishu-native AI news operating system.

It turns the existing `ai-news` skill family into a single conversational product:

- ingest mixed news input from chat
- split input into individual news items
- classify and track each item as a workflow unit
- support guided reading and background research
- turn discussions into structured notes
- turn notes into scripts or distribution-ready content

## Core Model

Frontend:
- OpenClaw chat

Workflow state:
- Feishu Bitable

Content storage:
- Feishu Docs

Reusable capability layer:
- prompts, templates, scripts, and migrated logic from existing `ai-news` skills

## Install

### OpenClaw

```bash
git clone <your-repo-url> ~/skills/ai-news-assistant
cd ~/skills/ai-news-assistant
npm install
```

Then in OpenClaw:

```text
set up ai news assistant
```

or invoke:

```text
/ai-news-assistant
```

## Repository Layout

```text
ai-news-assistant/
  README.md
  SKILL.md
  package.json
  config/
  prompts/
  templates/
  scripts/
  examples/
```

## Current Scope

This scaffold is v0. It includes:

- installable repo structure
- product behavior definition in `SKILL.md`
- Feishu-oriented schemas and templates
- prompt assets for the main stages
- minimal CLI script entrypoints for later integration work

This scaffold does not yet include:

- production Feishu API integration
- persistent local database
- deployment packaging
- end-to-end automation

## Next Build Steps

1. Connect `scripts/feishu_sync.py` to Feishu APIs.
2. Wire OpenClaw actions to the CLI entrypoints.
3. Replace placeholder processing with migrated logic from the old `ai-news` skills.
4. Add integration tests around ingest, note generation, and script generation.
