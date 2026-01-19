---
name: context-management
description: This skill should be used when creating Architecture Decision Records (ADRs), recording lessons learned, maintaining architecture notes, or managing project context and documentation. Triggers include "record decision", "create ADR", "document lesson", "architecture note", "what did we decide", and managing persistent project knowledge across sessions using the Michael Nygard ADR format.
---

# Context Management for Development

Maintain persistent project knowledge through ADRs, lessons learned, and architecture notes.

## Storage Structure

```
docs/adr/               # Architecture Decision Records (permanent, version-controlled)
  ├── README.md         # ADR index
  └── NNNN-title.md     # Individual ADRs

.claude/context/        # Claude's working context (gitignored ephemeral state)
  ├── lessons/          # Lessons learned (categorized: Process/Tech/Tooling)
  ├── architecture/     # Architecture diagrams and notes
  └── active/           # Active feature contexts
```

## Architecture Decision Records (ADRs)

**Format**: Michael Nygard format

**Template**:
```markdown
# ADR-NNN: [Title]

## Status
[Proposed | Accepted | Deprecated | Superseded by ADR-XXX]

## Context
[What is the issue we're facing? What factors are in play?
Include technical, political, social, and project constraints.]

## Decision
[What is the change we're making? Be specific and concise.]

## Consequences

### Positive
- [Benefit 1]
- [Benefit 2]

### Negative
- [Drawback 1]
- [Drawback 2]
```

**When to create**:
- Choosing between architectural approaches
- Major technology decisions
- Pattern selections
- Integration strategies

**Storage**: `docs/adr/NNNN-title.md` (version-controlled)

**Numbering**: Sequential, zero-padded (0001, 0002, etc.)

## Lessons Learned

**Categories**:
- **Process**: Workflow, planning, communication
- **Tech**: Framework limitations, language gotchas
- **Tooling**: IDE, build, dependency issues

**Template**:
```markdown
## YYYY-MM-DD: [Title]

**Category**: [Process | Tech | Tooling]
**Impact**: [Low | Medium | High]
**Tags**: [comma, separated, tags]

### Problem
[Specific description of what went wrong or was discovered]

### Solution
[What fixed it or workaround used]

### Prevention
- [How to avoid in future]
- [Warning signs to watch for]

### Related
- [Link to ADRs, other lessons, or documentation]
```

**Storage**: `.claude/context/lessons/YYYY-MM-DD-title.md`

**Proactive prompting**:
- End of session
- After solving difficult problem
- When user mentions "learned" or "gotcha"

## Architecture Notes

**Storage**: `.claude/context/architecture/`

**Content types**:
- System architecture diagrams (Mermaid)
- Component relationships
- Data flow documentation
- Integration patterns
- Security architecture

**Update frequency**: As architecture evolves

## Feature Context

**Active features**: `.claude/context/active/feature-name.md`

```markdown
# Feature: [Name]

**Branch**: feat/[name]
**Started**: YYYY-MM-DD HH:MM
**Current Stage**: [Stage]

## Workflow Progress
- ✅ Planning
- ✅ TDD Red
- 🔄 TDD Green (current)
- ⏳ Refactor
- ⏳ Visual Verify
- ⏳ Code Review

## Quality Gates
- ✅ TDD Gate
- ⏳ Accessibility Gate
- ⏳ Build Gate
- ⏳ Visual Verification Gate
- ⏳ Code Review Gate

## Recent Decisions
- [Decision with optional ADR link]

## Next Steps
1. [Action 1]
2. [Action 2]
```

**Archiving**: Move to `.claude/context/archive/` when complete

## Context Curator Responsibilities

The context-curator agent:

1. **Proactively suggests ADRs** when detecting architectural decisions
2. **Prompts for lessons** at session end or after problem-solving
3. **Maintains context organization** (indexing, archiving)
4. **Token budget awareness** (keeps ADRs concise, archives old content)

**Trigger phrases**:
- "We decided to use X instead of Y" → Suggest ADR
- "That was a tricky bug" → Suggest lesson
- Session ending → Prompt for lessons

## Best Practices

**ADRs**:
- ✅ Document the "why", not just "what"
- ✅ Include trade-offs (positive and negative)
- ✅ Keep concise (150-250 words)
- ✅ Update status when superseded

**Lessons**:
- ✅ Be specific with context
- ✅ Include working solution
- ✅ Add prevention strategies
- ✅ Use searchable tags

**Architecture Notes**:
- ✅ Use diagrams where helpful
- ✅ Keep current (remove outdated)
- ✅ Link to related ADRs

## Templates

See `templates/` directory for:
- `adr-template.md` - Michael Nygard ADR format
- `lesson-template.md` - Lessons learned format
- `feature-context-template.md` - Active feature tracking

## Related Skills

- `workflow-orchestration` - When to create context
- `session-continuity` - How context loads on session start
