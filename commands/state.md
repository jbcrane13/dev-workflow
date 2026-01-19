---
name: state
description: View or update project state snapshot
arguments:
  - name: action
    description: "Action: view (default), update, or section name to update"
    required: false
---

# /state Command

Maintain a living snapshot of project status for quick context restoration.

## Usage

```
/state                    # View current state
/state update             # Full interactive update
/state phase "Phase 2"    # Update specific section
/state progress           # Update In Progress section
/state blocked            # Update Blocked section
```

## Workflow

### Viewing State

Read and display `.claude/context/project-state.md`

### Updating State

1. **Read current**: Load `.claude/context/project-state.md`
2. **Identify changes**: Compare with session work
3. **Update sections**: Modify relevant sections
4. **Write back**: Save updated file
5. **Update timestamp**: Set "Updated" to current datetime

### State Template (~300 tokens)

```markdown
# Project State: ProjectName

**Updated:** YYYY-MM-DD HH:MM

## Current Phase
[Phase name and brief description]

## What's Built
- [Completed feature 1]
- [Completed feature 2]
- [Completed feature 3]

## In Progress
- [Current work item 1]
- [Current work item 2]

## Blocked
- [Blocker 1 - reason]
- None

## Next Up
- [Upcoming task 1]
- [Upcoming task 2]

## Technical Debt
- [Known issue 1]
- [Cleanup needed]

## Key Decisions
- ADR-1: [Brief reference]
- ADR-2: [Brief reference]
```

## File Location

```
.claude/
└── context/
    └── project-state.md    # Ephemeral, not in git
```

**Note:** This file is in `.claude/` (gitignored) because it changes frequently and represents Claude's working memory, not permanent project documentation.

## When to Update

- **Completing a feature** - Move from "In Progress" to "What's Built"
- **Starting new work** - Add to "In Progress"
- **Hitting blockers** - Add to "Blocked"
- **Phase transitions** - Update "Current Phase"
- **Discovering debt** - Add to "Technical Debt"
- **Making decisions** - Reference ADR in "Key Decisions"

## Automatic Updates

The `Stop` hook can prompt for state updates when significant work was completed during a session.

## Integration

- Loaded at session start via `SessionStart` hook
- Provides immediate project context
- Complements episodic memory (what IS vs what happened)
- References ADRs for decision context
