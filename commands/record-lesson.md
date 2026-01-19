---
name: record-lesson
description: Document lessons learned categorized by Process, Tech, or Tooling
---

# Record Lesson Command

Capture lessons learned to avoid repeating mistakes.

## Usage

```
/record-lesson [title]
```

## Process

1. **Prompt for Information**:
   - Title
   - Category (Process/Tech/Tooling)
   - Impact (Low/Medium/High)
   - Problem description
   - Solution
   - Prevention strategies
   - Related links (ADRs, docs)

2. **Create File**
   `.claude/context/lessons/YYYY-MM-DD-title.md`:
   ```markdown
   ## YYYY-MM-DD: {Title}

   **Category**: {Process|Tech|Tooling}
   **Impact**: {Low|Medium|High}
   **Tags**: {comma, separated}

   ### Problem
   {What went wrong or was discovered}

   ### Solution
   {What fixed it}

   ### Prevention
   - {How to avoid}
   - {Warning signs}

   ### Related
   - {Links to ADRs, docs}
   ```

3. **Update Index**
   Append to `.claude/context/lessons/README.md` grouped by category

## Example

```
/record-lesson "SwiftUI Preview Memory Leak"

Category? Tooling
Impact? High
Problem? Xcode SwiftUI previews consuming 12GB RAM after 2 hours
Solution? Restart Xcode hourly during heavy preview work
Prevention? Monitor Activity Monitor, use simulator for complex UI
Related? ADR-003 (why we use simulators over previews)
```

## Categories

- **Process**: Workflow, planning, communication
- **Tech**: Framework limitations, language gotchas
- **Tooling**: IDE, build, dependency issues

## Related Commands

- `/record-adr` - Architectural decisions
- `/workflow-status` - Current work context
