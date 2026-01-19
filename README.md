# Dev Workflow Plugin for Claude Code

Development workflow management with project notes, ADRs, lessons learned, and context persistence across sessions.

## Overview

This plugin provides a lightweight notes system that complements episodic memory (claude-mem) with declarative project context:

| Feature | Purpose | Token Budget |
|---------|---------|--------------|
| **ADRs** | Record why decisions were made | ~150-250 each |
| **Lessons** | Capture mistakes to avoid repeating | ~120-180 each |
| **State** | Snapshot of current project status | ~300-450 total |
| **Notes** | Technical details hard to rediscover | ~150-250 each |

**Session start baseline: ~700 tokens** (vs ~38k for full episodic memory index)

## Installation

```bash
# From local directory
claude plugins:install /Users/blake/Projects/dev-workflow

# Enable the plugin
claude plugins:enable dev-workflow
```

## Commands

| Command | Description |
|---------|-------------|
| `/adr [title]` | Create or list Architecture Decision Records |
| `/lesson [title]` | Record lessons learned |
| `/state [action]` | View or update project state |
| `/note [topic]` | Create or view technical notes |
| `/context [scope]` | View loaded project context |

## Directory Structure

The plugin creates/manages these directories in your project:

```
your-project/
├── .claude/
│   └── context/
│       └── project-state.md    # Ephemeral state (gitignored)
└── docs/
    ├── adr/
    │   ├── README.md           # ADR index
    │   └── 0001-decision.md    # Decision records
    ├── lessons/
    │   ├── README.md           # Lessons index
    │   └── 0001-lesson.md      # Lessons learned
    └── notes/
        ├── README.md           # Notes index
        └── topic-name.md       # Technical notes
```

## Quick Start

### Record a Decision

```
/adr "Use SwiftData over CoreData"
```

Creates `docs/adr/0001-use-swiftdata-over-coredata.md` with template.

### Capture a Lesson

```
/lesson "Actor isolation breaks with Task.detached"
```

Creates `docs/lessons/0001-actor-isolation-task-detached.md`.

### Update Project State

```
/state update
```

Interactive update of `.claude/context/project-state.md`.

### Add Technical Note

```
/note "companion-protocol"
```

Creates or updates `docs/notes/companion-protocol.md`.

## Hooks

The plugin includes session hooks:

- **SessionStart** - Loads project context summary (~200 tokens)
- **Stop** - Suggests what might be worth capturing
- **PreToolUse** - Validates document structure when writing to docs/

## Integration with claude-mem

This plugin **complements** claude-mem, not replaces it:

| claude-mem | dev-workflow |
|------------|--------------|
| Episodic (what happened) | Declarative (what IS) |
| Auto-generated observations | Manually curated documents |
| Chronological history | Organized by topic |
| Searchable via MCP | Quick reference at session start |

**Recommended workflow:**
1. SessionStart loads notes summary (~700 tokens)
2. claude-mem available for deep history search
3. Create ADRs when making decisions
4. Create lessons when solving gotchas
5. Update state on milestones

## Token Economics

| Component | Tokens | When Loaded |
|-----------|--------|-------------|
| Project State | ~300 | Session start |
| ADR Index | ~100 | Session start |
| Lessons Index | ~100 | Session start |
| Summary | ~200 | Session start |
| **Total Baseline** | **~700** | Every session |

Individual ADRs, lessons, and notes loaded on-demand when relevant.

## Components

### Skill: project-notes

Auto-activates when working with `docs/adr/`, `docs/lessons/`, `docs/notes/`, or `.claude/context/`.

### Agent: context-curator

Specialist for creating and managing project documentation with token budget awareness.

## Templates

Templates available in `skills/project-notes/templates/`:
- `adr.md` - Architecture Decision Record
- `lesson.md` - Lesson Learned
- `state.md` - Project State
- `note.md` - Technical Note
- `adr-index.md`, `lessons-index.md`, `notes-index.md` - Index files

## Requirements

- Claude Code CLI >= 2.0.0

## License

MIT

## Author

Blake Crane (jbcrane13@github.com)
