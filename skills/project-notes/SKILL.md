---
name: project-notes
description: Project context management with ADRs, lessons, state, and technical notes
alwaysApply: false
globs:
  - "docs/adr/**"
  - "docs/lessons/**"
  - "docs/notes/**"
  - ".claude/context/**"
---

# Project Notes Skill

Manage project context through structured documentation: Architecture Decision Records, Lessons Learned, Project State, and Technical Notes.

## Purpose

Complement episodic memory (what happened) with declarative context (what IS):
- **ADRs** - Why decisions were made
- **Lessons** - Mistakes and solutions to avoid repeating
- **State** - Current project status snapshot
- **Notes** - Implementation details hard to rediscover

## Token Budget

Keep documents concise to minimize context consumption:

| Document Type | Target Tokens | Max Tokens |
|---------------|---------------|------------|
| ADR | 150 | 250 |
| Lesson | 120 | 180 |
| State | 300 | 450 |
| Note | 150 | 250 |
| Index | 100 | 150 |

**Session start baseline: ~700 tokens** (vs ~38k for full episodic index)

## Directory Structure

```
project-root/
├── .claude/
│   └── context/
│       └── project-state.md    # Ephemeral (gitignored)
└── docs/
    ├── adr/
    │   ├── README.md           # Index
    │   └── NNNN-title.md       # Decision records
    ├── lessons/
    │   ├── README.md           # Index
    │   └── NNNN-title.md       # Lessons learned
    └── notes/
        ├── README.md           # Index
        └── topic-name.md       # Technical notes
```

## Templates

Use templates in `templates/` directory for consistent structure.

### ADR Template

```markdown
# ADR-NNNN: Title

**Status:** Proposed | Accepted | Deprecated | Superseded
**Date:** YYYY-MM-DD

## Context
[2-3 sentences: Problem and constraints]

## Decision
[1-2 sentences: What we decided]

## Consequences
- (+) [Benefit]
- (-) [Trade-off]
```

### Lesson Template

```markdown
# L-NNNN: Title

**Date:** YYYY-MM-DD
**Project:** ProjectName

## Problem
[What went wrong?]

## Root Cause
[Why did it happen?]

## Solution
[How was it fixed?]

## Prevention
[How to avoid in future]
```

### State Template

```markdown
# Project State: ProjectName

**Updated:** YYYY-MM-DD HH:MM

## Current Phase
[Phase description]

## What's Built
- [Feature 1]
- [Feature 2]

## In Progress
- [Current work]

## Blocked
- None

## Technical Debt
- [Known issue]
```

### Note Template

```markdown
# Note: Topic

**Updated:** YYYY-MM-DD

## Overview
[What and why]

## How It Works
[Key mechanics]

## Key Files
- `path/file.swift` - Purpose

## Gotchas
- [Edge case]
```

## Index Format

Indexes enable quick scanning without loading full documents.

### ADR Index (docs/adr/README.md)

```markdown
# Architecture Decisions

| # | Title | Status | Date |
|---|-------|--------|------|
| 1 | Use SwiftData | Accepted | 2026-01-15 |
```

### Lessons Index (docs/lessons/README.md)

```markdown
# Lessons Learned

| # | Title | Project | Date |
|---|-------|---------|------|
| 1 | Actor isolation gotcha | NetMonitor | 2026-01-15 |
```

### Notes Index (docs/notes/README.md)

```markdown
# Technical Notes

| Topic | Description | Updated |
|-------|-------------|---------|
| companion-protocol | iOS-macOS communication | 2026-01-18 |
```

## Workflow Integration

### Session Start
1. Load project state from `.claude/context/project-state.md`
2. Load ADR index from `docs/adr/README.md`
3. Load lessons index from `docs/lessons/README.md`
4. Summarize in ~200 tokens

### During Session
- Create ADRs when making significant decisions
- Create lessons when solving tricky problems
- Create notes when implementing complex features
- Update state on milestones

### Session End
- Optionally update project state with progress
- Consider what should be captured as ADR/lesson/note

## Commands

| Command | Purpose |
|---------|---------|
| `/adr` | Create/list Architecture Decision Records |
| `/lesson` | Record lessons learned |
| `/state` | View/update project state |
| `/note` | Create/view technical notes |
| `/context` | View loaded context summary |

## Best Practices

### Writing ADRs
- Focus on **why**, not just what
- Include alternatives considered
- Note both positive and negative consequences
- Link to related ADRs

### Writing Lessons
- Be specific about the problem
- Include reproduction steps if applicable
- Make prevention actionable
- Cross-reference relevant code

### Maintaining State
- Update immediately on milestones
- Keep lists current (remove completed items from "In Progress")
- Be honest about blockers and debt
- Reference relevant ADRs

### Writing Notes
- Focus on knowledge hard to rediscover
- Don't duplicate code comments
- Include file locations
- Update when implementation changes
