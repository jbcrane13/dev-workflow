---
name: lesson
description: Record lessons learned from mistakes or discoveries
arguments:
  - name: title
    description: Title for the lesson (omit to list existing lessons)
    required: false
---

# /lesson Command

Capture mistakes, gotchas, and hard-won knowledge to prevent repetition.

## Usage

```
/lesson                              # List all lessons
/lesson "Actor isolation gotcha"     # Create new lesson
/lesson 5                            # View lesson #5
```

## Workflow

### Creating a New Lesson

1. **Determine next number**: Check `docs/lessons/README.md` for highest number
2. **Create file**: `docs/lessons/NNNN-kebab-title.md`
3. **Use template**: Load from `project-notes` skill templates
4. **Update index**: Add entry to `docs/lessons/README.md`

### Lesson Template (Concise - ~120 tokens)

```markdown
# L-NNNN: Title

**Date:** YYYY-MM-DD
**Project:** ProjectName

## Problem
[1-2 sentences: What went wrong or was confusing?]

## Root Cause
[1-2 sentences: Why did this happen?]

## Solution
[1-2 sentences: How was it fixed?]

## Prevention
[1 sentence: How to avoid this in the future]
```

### Listing Lessons

Read and display `docs/lessons/README.md`:

```markdown
# Lessons Learned

| # | Title | Project | Date |
|---|-------|---------|------|
| 1 | Actor isolation breaks with Task.detached | NetMonitor | 2026-01-15 |
| 2 | Visual verification catches layout bugs | NetMonitor | 2026-01-18 |
```

## Directory Structure

```
docs/
└── lessons/
    ├── README.md                    # Index of all lessons
    ├── 0001-actor-task-detached.md
    ├── 0002-visual-verification.md
    └── 0003-swiftdata-migration.md
```

## Lesson Categories

Common patterns to capture:

- **Concurrency gotchas** - Actor isolation, Sendable, Task behavior
- **API surprises** - Unexpected framework behavior
- **Build issues** - Xcode, signing, dependencies
- **Testing gaps** - What tests missed that manual verification caught
- **Performance traps** - What caused slowdowns
- **Integration issues** - Framework/library conflicts

## When to Create a Lesson

- Spent significant time debugging something
- Found a non-obvious solution
- Hit a framework edge case
- Discovered a pattern that prevents issues
- Made a mistake that could be repeated

## Integration

- Permanent records in version control
- Index loaded at session start
- Cross-referenced with ADRs when applicable
- Searchable via claude-mem
