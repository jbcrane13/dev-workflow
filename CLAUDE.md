# CLAUDE.md

This file provides guidance to Claude Code when working with the dev-workflow plugin.

## Project Overview

**Claude Code Plugin** - Development workflow management with project notes, ADRs, lessons learned, and context persistence.

## Purpose

Complement episodic memory with declarative context:
- **ADRs** - Why decisions were made
- **Lessons** - Mistakes to avoid repeating
- **State** - Current project snapshot
- **Notes** - Technical details hard to rediscover

## Key Constraints

### Token Budgets

| Document Type | Target | Max |
|---------------|--------|-----|
| ADR | 150 | 250 |
| Lesson | 120 | 180 |
| Note | 150 | 250 |
| State | 300 | 450 |

### Directory Structure

```
project/
├── .claude/context/           # Ephemeral (gitignored)
│   └── project-state.md
└── docs/
    ├── adr/README.md + NNNNs
    ├── lessons/README.md + NNNNs
    └── notes/README.md + topics
```

## Plugin Components

| Type | Name | Purpose |
|------|------|---------|
| Commands | adr, lesson, state, note, context | User actions |
| Skill | project-notes | Auto-activates on docs/ |
| Agent | context-curator | Document lifecycle |
| Hooks | SessionStart, Stop, PreToolUse | Context loading |

## Development Guidelines

- Templates in `skills/project-notes/templates/`
- Commands in `commands/`
- Keep all documentation within token budgets
- Indexes must stay in sync with documents
