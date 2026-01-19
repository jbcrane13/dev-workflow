---
name: start-feature
description: Begin a new feature with full workflow context setup, branch creation, and Planning stage entry
---

# Start Feature Command

Initialize a new feature with complete workflow scaffolding.

## Usage

```
/start-feature [feature-name]
```

If feature name not provided, prompt interactively.

## Process

1. **Check for Active Work**
   - Load `.session/state.json`
   - If active feature exists:
     - Prompt: Stash current work or continue?
     - If stash: Save to `.session/suspended-{name}.json`

2. **Gather Feature Information**
   Prompt for (if not provided):
   - **Feature name** (kebab-case)
   - **Description** (1-2 sentences)
   - **Acceptance criteria** (optional, bulleted list)
   - **Parent feature** (if sub-task)

3. **Create Git Branch**
   ```bash
   git checkout -b feat/{feature-name}
   ```

   Unless `auto_create_branch: false` in config.

4. **Initialize Feature Context**
   Create `.claude/context/active/{feature-name}.md`:
   ```markdown
   # Feature: {Feature Name}

   **Branch**: feat/{feature-name}
   **Started**: {timestamp}
   **Current Stage**: Planning

   ## Description
   {user-provided description}

   ## Acceptance Criteria
   {criteria if provided}

   ## Workflow Progress
   - 🔄 Planning (current)
   - ⏳ TDD Red
   - ⏳ TDD Green
   - ⏳ Refactor
   - ⏳ Visual Verify
   - ⏳ Code Review

   ## Quality Gates
   - ⏳ TDD Gate
   - ⏳ Test Pass Gate
   - ⏳ Accessibility Gate
   - ⏳ Build Gate
   - ⏳ Visual Verification Gate
   - ⏳ Code Review Gate

   ## Recent Decisions
   (none yet)

   ## Next Steps
   1. Break down feature into tasks
   2. Identify architectural decisions
   3. Plan test strategy
   ```

5. **Update Session State**
   Save to `.session/state.json`:
   ```json
   {
     "activeFeature": "{feature-name}",
     "currentStage": "Planning",
     "branch": "feat/{feature-name}",
     "gateStatus": {
       "tdd": "pending",
       "testPass": "pending",
       "accessibility": "pending",
       "build": "pending",
       "visualVerification": "pending",
       "codeReview": "pending"
     },
     "timestamp": "{current-time}"
   }
   ```

6. **Enter Planning Stage**
   Activate **workflow-orchestrator** agent with Planning mode:
   - Analyze requirements
   - Break down into tasks
   - Create TodoWrite items if complex
   - Check if architectural decision needed → suggest `/record-adr`
   - Plan test strategy

   If swiftui-dev available:
   - Suggest `/swiftui:design` for UI/UX design
   - Suggest `/swiftui:plan` for implementation breakdown

7. **Display Next Steps**
   ```
   Feature "Login Screen" initialized!

   Branch: feat/login-screen
   Stage: Planning

   Next steps:
   1. Review and refine requirements
   2. Create implementation plan
   3. Identify ADR needs (architectural decisions)
   4. Transition to TDD Red when ready

   Ready to proceed with planning?
   ```

## Configuration

From `.claude/dev-workflow.local.md`:
- `auto_create_branch` - Create git branch automatically (default: true)
- `preferred_plugin` - Implementation plugin to coordinate with (default: swiftui-dev)

## Examples

**Simple feature**:
```
/start-feature logout-button
```

**Interactive**:
```
/start-feature

Prompts:
Feature name? settings-screen
Description? User settings with profile and preferences
Acceptance criteria? (optional)
- User can view profile
- User can change theme
- User can log out
```

## Integration with Workflow

This command is the entry point to the workflow state machine:

```
Dashboard
    ↓ /start-feature
Planning (activated by this command)
    ↓
TDD Red
    ↓
[workflow continues...]
```

## Related Commands

- `/workflow-status` - Check current state after starting
- `/gate-status` - View quality gates
- `/stash` - Pause current feature
