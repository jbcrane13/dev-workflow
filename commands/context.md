---
name: context
description: View loaded project context summary
arguments:
  - name: scope
    description: "Scope: summary (default), full, adrs, lessons, notes, state"
    required: false
---

# /context Command

View what project context is currently loaded and available.

## Usage

```
/context              # Summary of all loaded context
/context full         # Full context details
/context adrs         # List ADRs with details
/context lessons      # List lessons with details
/context notes        # List notes with details
/context state        # Show current project state
```

## Workflow

### Summary View (Default)

Display concise overview of loaded context:

```
Project Context Summary
=======================

Project State: NetMonitor iOS (Updated: 2026-01-18 9:00 PM)
  Phase: Phase 1 - Feature Complete Release
  In Progress: 2 items
  Blocked: None

Architecture Decisions: 5 ADRs
  Latest: ADR-5 Use NavigationStack (2026-01-17)

Lessons Learned: 3 lessons
  Latest: L-3 Visual verification catches layout bugs (2026-01-18)

Technical Notes: 4 notes
  Recent: companion-protocol, network-scanning

Episodic Memory: Available via claude-mem search
```

### Full View

Load and display complete content from:
- `.claude/context/project-state.md`
- `docs/adr/README.md`
- `docs/lessons/README.md`
- `docs/notes/README.md`

### Scoped Views

Load specific indexes with full entries:
- `adrs` - Full ADR index with status
- `lessons` - Full lesson index
- `notes` - Full notes index
- `state` - Complete project state

## Context Sources

| Source | Location | Loaded At |
|--------|----------|-----------|
| Project State | `.claude/context/project-state.md` | Session start |
| ADR Index | `docs/adr/README.md` | Session start |
| Lessons Index | `docs/lessons/README.md` | Session start |
| Notes Index | `docs/notes/README.md` | On demand |
| Episodic Memory | claude-mem MCP | On demand |

## Token Budget

| Component | Typical Tokens |
|-----------|----------------|
| Project State | ~300 |
| ADR Index | ~100 |
| Lessons Index | ~100 |
| Summary | ~200 |
| **Session Start Total** | **~700** |

## Integration

- Provides transparency into what Claude "knows"
- Helps user understand context availability
- Useful for debugging context-related issues
- Shows when to refresh or update context
