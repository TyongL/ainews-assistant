# AI News Assistant

AI News Assistant is an OpenClaw-installable workflow package that migrates the real working logic of the old `ai-news` skill family into a Feishu-native product workflow.

This repository is not meant to be a generic "news summarizer". It is designed to preserve the original system's strengths:

- source-first reading instead of model freestyle guessing
- item-level deep reading and discussion
- background research only when the source is insufficient
- preservation of the user's original thought chain
- high-fidelity note archival instead of shallow summaries
- script generation with a distinct point of view and delivery style

It turns the original manual skill chain into a single conversational product:

- ingest mixed news input from chat or source links
- split input into individual news items
- classify and track each item as a workflow unit
- support guided reading and background research
- turn discussions into structured cognitive notes
- turn notes into scripts or distribution-ready content

## Core Model

Frontend:
- OpenClaw chat

Workflow state:
- Feishu Bitable

Content storage:
- Feishu Docs

Reusable capability layer:
- prompts, templates, scripts, and migrated logic from `ainews`, `ainews-companion`, `ainews-archive`, and `XHIP-agent`

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

## What Has Been Migrated

The repository now carries the productized logic of the old skill system in a mixed-migration form:

- `ainews`
  - kept: source-first ingest, source link preservation, "what should we read first" handoff
  - adapted: no longer locked to one RSS-only flow; now designed for mixed user-fed input plus source fetch
- `ainews-companion`
  - kept at high fidelity: source sovereignty, anti-hallucination rule, mandatory plain-language explanation, critical sparring, hidden note drafting
- `ainews-archive`
  - kept at high fidelity: preserve detail, preserve user original thought chain, structure notes for long-term retrieval
  - adapted: archive target is Feishu docs and workflow state instead of local PARA folders
- `XHIP-agent`
  - kept: script generation as a real content transformation task rather than summary rewriting
  - adapted: input/output should move toward Feishu note and doc flows

## Current Scope

This repository currently includes:

- installable repo structure
- workflow definition in `SKILL.md`
- migrated behavioral rules from the old `ai-news` system
- Feishu-oriented schemas and templates
- prompt assets for ingest, companion, archive, and script stages
- minimal CLI script entrypoints and a basic Feishu integration layer

This repository does not yet fully include:

- production-complete Feishu API write flows
- end-to-end automation from OpenClaw action to Feishu state update
- migrated XHIP knowledge-base retrieval implementation

## Next Build Steps

1. Complete real Feishu write flows in `scripts/feishu_sync.py`.
2. Wire OpenClaw actions to the CLI entrypoints.
3. Move more concrete legacy logic into ingest, note, and script generation code.
4. Add integration tests around ingest, note generation, and script generation.
