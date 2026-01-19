---
name: adr
description: Create or list Architecture Decision Records
arguments:
  - name: title
    description: Title for the new ADR (omit to list existing ADRs)
    required: false
---

# /adr Command

Record architecture decisions with context and consequences.

## Usage

```
/adr                           # List all ADRs
/adr "Use SwiftData"           # Create new ADR
/adr 3                         # View ADR #3
/adr 3 --status superseded     # Update status
```

## Workflow

### Creating a New ADR

1. **Determine next number**: Check `docs/adr/README.md` for highest number
2. **Create file**: `docs/adr/NNNN-kebab-title.md`
3. **Use template**: Load from `project-notes` skill templates
4. **Update index**: Add entry to `docs/adr/README.md`

### ADR Template (Concise - ~150 tokens)

```markdown
# ADR-NNNN: Title

**Status:** Proposed | Accepted | Deprecated | Superseded
**Date:** YYYY-MM-DD

## Context
[2-3 sentences: What problem needed solving? What constraints existed?]

## Decision
[1-2 sentences: What did we decide?]

## Consequences
- (+) [Positive outcome]
- (+) [Another benefit]
- (-) [Trade-off accepted]
- (-) [Limitation]
```

### Listing ADRs

Read and display `docs/adr/README.md`:

```markdown
# Architecture Decisions

| # | Title | Status | Date |
|---|-------|--------|------|
| 1 | Use SwiftData over CoreData | Accepted | 2026-01-15 |
| 2 | Actor-based services | Accepted | 2026-01-16 |
```

## Directory Structure

```
docs/
└── adr/
    ├── README.md           # Index of all ADRs
    ├── 0001-use-swiftdata.md
    ├── 0002-actor-services.md
    └── 0003-navigation-stack.md
```

## Status Transitions

- **Proposed** → **Accepted** (after validation)
- **Accepted** → **Deprecated** (no longer applies)
- **Accepted** → **Superseded by ADR-NNNN** (replaced)

## Integration

- Creates permanent records in version control
- Index loaded at session start via hooks
- Searchable via claude-mem observations
- Referenced in lessons learned when relevant
