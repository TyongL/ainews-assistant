# Quickstart For OpenClaw

## Goal

Continue implementation of this project without redesigning it from scratch.

## Read First

1. `OpenClaw学习指令_AI资讯助手.md`
2. `OpenClaw接手执行任务书.md`
3. `ai-news-assistant/README.md`
4. `ai-news-assistant/SKILL.md`

## Core Working Directory

- `ai-news-assistant/`

## Current State

Already done:

- product design
- workflow definition
- installable repo scaffold
- prompts, templates, examples
- minimal Feishu integration structure
- basic tests for Feishu config and request building

Not done yet:

- real Feishu authentication flow execution
- real Bitable writes
- real Feishu Doc creation
- end-to-end routing from ingest to note to script

## Your Immediate Task

Work on the existing scaffold and complete:

1. real Feishu API integration
2. Bitable write flow
3. Feishu Docs creation flow
4. wiring ingest, note, and script flows to Feishu

## Important Constraints

- do not redesign the architecture
- do not change the single-news-item workflow unit
- do not replace Feishu as the main content destination
- do not discard the existing prompts, templates, and repo structure
