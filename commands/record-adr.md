---
name: record-adr
description: Create an Architecture Decision Record using Michael Nygard format
---

# Record ADR Command

Create Architecture Decision Record for significant architectural choices.

## Usage

```
/record-adr [title]
```

## Process

1. **Prompt for Information** (if not provided):
   - Title
   - Status (Proposed/Accepted/Deprecated)
   - Context
   - Decision
   - Positive consequences
   - Negative consequences

2. **Generate ADR Number**
   Find highest existing ADR in `docs/adr/`, increment

3. **Create File**
   `docs/adr/NNNN-title.md`:
   ```markdown
   # ADR-NNNN: {Title}

   ## Status
   {Status}

   ## Context
   {Context - what issue are we facing?}

   ## Decision
   {What change are we making?}

   ## Consequences

   ### Positive
   - {Benefit 1}
   - {Benefit 2}

   ### Negative
   - {Drawback 1}
   - {Drawback 2}
   ```

4. **Update Index**
   Append to `docs/adr/README.md`:
   ```markdown
   - [ADR-NNNN: {Title}](NNNN-title.md) - {Status} - {Date}
   ```

5. **Link to Feature**
   If active feature, add to `.claude/context/active/{feature}.md`:
   ```markdown
   ## Recent Decisions
   - {Decision summary} (ADR-NNNN)
   ```

## Example

```
/record-adr "Use SwiftData over CoreData"

Prompts:
Status? Accepted
Context? We need local persistence. CoreData is legacy, SwiftData is modern.
Decision? Use SwiftData for all persistence in this iOS 18+ app.
Positive consequences? Simpler API, better concurrency, automatic CloudKit sync
Negative consequences? Requires iOS 17+, fewer resources, less mature tooling
```

Creates: `docs/adr/0001-use-swiftdata-over-coredata.md`

## Related Commands

- `/record-lesson` - Document lessons learned
- `/workflow-status` - Link ADR to active feature
