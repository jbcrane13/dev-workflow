---
name: note
description: Create or view technical notes on specific topics
arguments:
  - name: topic
    description: Topic name (omit to list existing notes)
    required: false
---

# /note Command

Capture implementation details and technical knowledge that's hard to rediscover.

## Usage

```
/note                           # List all notes
/note "companion-protocol"      # Create/view note on topic
/note companion-protocol        # Same (quotes optional)
```

## Workflow

### Creating a New Note

1. **Normalize topic**: Convert to kebab-case
2. **Check existence**: Look for `docs/notes/{topic}.md`
3. **Create or update**: Use template if new, edit if exists
4. **Update index**: Add/update entry in `docs/notes/README.md`

### Note Template (~150 tokens)

```markdown
# Note: Topic Title

**Updated:** YYYY-MM-DD

## Overview
[2-3 sentences: What is this and why does it matter?]

## How It Works
[Key mechanics, flow, or architecture]

## Key Files
- `path/to/file.swift` - Purpose
- `path/to/other.swift` - Purpose

## Gotchas
- [Edge case or non-obvious behavior]

## Related
- ADR-N: Related decision
- L-N: Related lesson
```

### Listing Notes

Read and display `docs/notes/README.md`:

```markdown
# Technical Notes

| Topic | Description | Updated |
|-------|-------------|---------|
| companion-protocol | iOS-macOS communication protocol | 2026-01-18 |
| network-scanning | How device discovery works | 2026-01-16 |
```

## Directory Structure

```
docs/
└── notes/
    ├── README.md                 # Index of all notes
    ├── companion-protocol.md
    ├── network-scanning.md
    └── data-migration.md
```

## What Makes a Good Note

**Include:**
- Implementation details that took time to figure out
- Protocol/API specifics that aren't obvious from code
- Integration points between components
- Non-obvious file locations for features

**Avoid:**
- Duplicating code comments
- General Swift/SwiftUI patterns (use skill references instead)
- Temporary debugging notes (use project-state for that)

## When to Create a Note

- Implemented something with non-obvious architecture
- Figured out how existing code works
- Set up an integration that needs documentation
- Created a protocol or pattern others need to understand

## Integration

- Permanent records in version control
- Index available for on-demand loading
- Cross-references ADRs and lessons
- Complements code comments with higher-level context
