---
name: workflow-orchestration
description: This skill should be used when starting any development task, managing workflow stages, or sequencing development activities. Triggers include "start feature", "begin development", "workflow status", "what stage am I in", "next step", and managing transitions between Planning, TDD Red, TDD Green, Refactor, Visual Verify, Review, and Complete stages. Provides the core workflow state machine and orchestration patterns for mobile/macOS development.
---

# Workflow Orchestration for Development

Orchestrate development workflows through an explicit state machine that prevents getting lost in long conversations and ensures quality at every stage.

## Core Philosophy

Development workflows must be **explicit, trackable, and recoverable**. The workflow-orchestration system provides:

1. **Explicit stages** - Clear progression from Planning through Completion
2. **Hub and Spoke model** - Return to Dashboard between features
3. **State persistence** - Resume work across sessions
4. **Gentle guidance** - Suggest next steps without forcing

## Workflow State Machine

The core workflow follows this progression:

```
Dashboard (Hub)
    ↓ /start-feature
Planning
    ↓ plan approved
TDD Red (write failing test)
    ↓ test fails
TDD Green (implement to pass)
    ↓ test passes
Refactor
    ↓ code cleaned, tests green
Visual Verify
    ↓ screenshots approved
Code Review
    ↓ review passed
Complete
    ↓ return to Dashboard
```

### Dashboard (Hub State)

The Dashboard is the **central hub** where all workflow begins and ends.

**Purpose:**
- View all active features
- Resume suspended work
- Start new features
- Check for stale work

**Display format:**
```
Active Features:
1. Login Screen [Visual Verify] 🟡
   Branch: feat/login-screen
   Gates: ✅ TDD ✅ Build ⏳ Visual ⏳ Review

2. Dashboard Refactor [TDD Green] 🟢
   Branch: feat/dashboard
   Gates: ✅ TDD ⏳ Build ⏳ Visual ⏳ Review

Stale Work:
3. Settings Screen [Suspended: 12 days] ⚠️
   Suggest: Archive or resume?

Actions:
- /start-feature (new)
- Type number to resume
- /prepare-release
```

**Entry conditions:**
- Session start
- Feature completion
- Manual return via `/dashboard`

**Exit conditions:**
- User selects feature to resume
- User invokes `/start-feature`

### Planning Stage

Break down features and make architectural decisions.

**Purpose:**
- Define feature scope
- Create task breakdown
- Identify architectural decisions
- Plan test strategy

**Activities:**
- Analyze requirements
- Create ADR if architectural choice needed
- Define acceptance criteria
- Plan implementation approach
- Coordinate with implementation plugin (swiftui-dev) for design/plan

**Entry conditions:**
- `/start-feature` invoked
- Feature selected from Dashboard

**Exit conditions:**
- Plan approved and documented
- Tasks defined

**Transitions:**
- → TDD Red: Plan complete
- → Dashboard: Cancelled

### TDD Red Stage

Write a failing test before implementation.

**Purpose:**
- Define expected behavior through test
- Ensure test can fail (validate test quality)
- Set up test-first discipline

**Activities:**
- Write test case
- Run test to verify it FAILS
- Document failure output

**Entry conditions:**
- Planning complete
- Need more test coverage (from TDD Green)
- Bug found during Visual Verify

**Exit conditions:**
- Test written and verified failing

**Transitions:**
- → TDD Green: Test fails as expected

**Enforcement:**
- PreToolUse hook blocks implementation code if no failing test

### TDD Green Stage

Write minimal implementation to make test pass.

**Purpose:**
- Implement just enough to pass test
- Verify test now passes
- Avoid over-engineering

**Activities:**
- Write minimal code
- Run tests
- Verify all tests pass
- Coordinate with implementation plugin for code generation

**Entry conditions:**
- Failing test exists (from TDD Red)

**Exit conditions:**
- Test(s) passing

**Transitions:**
- → Refactor: Tests passing, ready to clean up
- → TDD Red: Need more test coverage

### Refactor Stage

Clean up code while maintaining green tests.

**Purpose:**
- Improve code quality
- Extract abstractions
- Maintain test coverage

**Activities:**
- Refactor implementation
- Run tests frequently
- Ensure tests stay green
- Delegate to swiftui-dev architect-review if structural changes

**Entry conditions:**
- Tests passing (from TDD Green)
- Review feedback requiring refactor (from Code Review)

**Exit conditions:**
- Code cleaned
- Tests still passing
- Ready for visual validation

**Transitions:**
- → Visual Verify: Refactor complete
- → TDD Green: Verify tests still pass

### Visual Verify Stage

Prove UI works correctly with screenshot evidence.

**Purpose:**
- Run actual app
- Capture screenshots
- Validate visual correctness
- Test on multiple device sizes

**Activities:**
- Build and run app
- Navigate to feature
- Capture screenshots (all device sizes)
- Visual inspection (layout, behavior, completeness)
- Save screenshots to `visual-proofs/feature-name/device/timestamp.png`

**Entry conditions:**
- Implementation and refactor complete

**Exit conditions:**
- Screenshots captured for all required devices
- Visual inspection passed
- No UI bugs found

**Transitions:**
- → Code Review: Visual verification passed
- → TDD Red: Visual bugs discovered

**Critical importance:**
This is the MOST IMPORTANT gate. A dashboard with content running off-screen is a HARD FAIL even if tests pass.

### Code Review Stage

Final quality checks before completion.

**Purpose:**
- Review against coding standards
- Check for dead code or TODOs
- Verify all gates passed
- Ensure documentation complete

**Activities:**
- Run gate-enforcer agent
- Check for TODO/FIXME comments
- Verify no unused code
- Delegate to swiftui-dev /audit if needed
- Review accessibility IDs
- Confirm modern patterns only

**Entry conditions:**
- Visual verification passed

**Exit conditions:**
- All quality checks passed
- No issues found

**Transitions:**
- → Complete: Review passed
- → Refactor: Issues found requiring changes

### Complete Stage

Feature done, return to Dashboard.

**Purpose:**
- Mark feature complete
- Archive feature context
- Update project state
- Record final status

**Activities:**
- Mark all gates as passed in audit log
- Archive feature context
- Update branch status
- Prompt for lessons learned
- Return to Dashboard

**Entry conditions:**
- All gates passed
- Code review complete

**Exit conditions:**
- Feature marked complete

**Transitions:**
- → Dashboard: Always

## Orchestrating with Implementation Plugins

The workflow orchestrator delegates platform-specific work to implementation plugins like swiftui-dev.

### Delegation Pattern

**Command invocation:**
```
Planning stage → /swiftui:design (UI/UX design)
Planning stage → /swiftui:plan (implementation breakdown)
TDD Green → mobile-code-implementer agent
Visual Verify → /swiftui:screenshot (capture)
Code Review → /swiftui:audit (quality check)
```

**Agent deployment:**
```
Deploy swiftui-ux-designer for design work
Deploy mobile-code-implementer for code generation
Deploy architect-review for structural validation
```

**Handoff process:**
1. Identify task requiring implementation
2. Delegate to appropriate swiftui-dev command/agent
3. Wait for completion
4. Validate output against gates
5. Continue workflow

### Integration Example

```
User: "Add login screen"

Orchestrator:
1. Detect feature request
2. Suggest /start-feature
3. Guide through Planning:
   - Delegate to /swiftui:design
   - Delegate to /swiftui:plan
4. Transition to TDD Red
5. Enforce failing test first
6. Transition to TDD Green:
   - Delegate to mobile-code-implementer
7. Transition to Visual Verify:
   - Use /swiftui:screenshot
   - Add validation layer
8. Transition to Code Review:
   - Run gate-enforcer
   - Use /swiftui:audit if needed
9. Complete and return to Dashboard
```

## State Management

### Feature State Tracking

Each active feature maintains state in `.claude/context/active/feature-name.md`:

```markdown
# Feature: Login Screen

**Branch**: feat/login-screen
**Started**: 2026-01-19 09:00
**Current Stage**: Visual Verify

## Workflow Progress
- ✅ Planning
- ✅ TDD Red
- ✅ TDD Green
- ✅ Refactor
- 🔄 Visual Verify (current)
- ⏳ Code Review

## Quality Gates
- ✅ TDD Gate
- ✅ Accessibility Gate
- ✅ Build Gate
- ⏳ Visual Verification Gate
- ⏳ Code Review Gate

## Recent Decisions
- Use @Observable for AuthService (ADR-007)

## Next Steps
1. Run app in simulator
2. Capture screenshots
3. Verify layout on all devices
```

### Session State Persistence

Workflow state persists in `.session/state.json`:

```json
{
  "activeFeature": "login-screen",
  "currentStage": "Visual Verify",
  "branch": "feat/login-screen",
  "gateStatus": {
    "tdd": "passed",
    "accessibility": "passed",
    "build": "passed",
    "visualVerification": "pending",
    "codeReview": "pending"
  },
  "lastAction": "Updated AuthService to use async/await",
  "timestamp": "2026-01-19T10:30:00Z"
}
```

## Workflow Guidance Patterns

### Gentle Redirection

Suggest next steps without forcing:

**Example 1 - TDD enforcement:**
```
User starts writing implementation code without test.

Orchestrator: "It looks like you're writing implementation code, but we
haven't seen a failing test yet. Shall we create the test first to follow
TDD discipline?"
```

**Example 2 - Stage transition:**
```
Tests pass after implementation.

Orchestrator: "Great! All tests are passing. Ready to refactor and clean
up the code, or shall we add more test coverage first?"
```

**Example 3 - Visual verification reminder:**
```
Refactoring complete, tests green.

Orchestrator: "Code is clean and tests are passing. Time for the most
important gate: let's run the app and verify the UI works correctly.
Ready for /verify-visual?"
```

### Proactive Suggestions

Recommend next actions based on workflow stage:

**After Planning:**
- "Plan approved. Let's transition to TDD Red - what test should we write first?"

**After TDD Red:**
- "Test is failing as expected. Ready to write minimal implementation to make it pass?"

**After TDD Green:**
- "Tests are passing! Ready to refactor or need more test coverage?"

**After Visual Verify:**
- "Screenshots look good. Shall we run the code review checklist?"

## Context Switching

Handle interruptions gracefully with stash/resume.

### Automatic Stashing

When starting new feature while one is active:

```
User: "/start-feature"

Orchestrator detects active feature: Login Screen

Orchestrator: "You currently have an active feature: Login Screen
(stage: Visual Verify). Would you like to:
1. Stash it and start new feature
2. Continue with current feature
3. Return to Dashboard"

User: "1"

Orchestrator:
1. Saves state to .session/suspended-login-screen.json
2. Clears active context
3. Proceeds with new feature
```

### Manual Stashing

```
User: "/stash Need to fix urgent bug"

Orchestrator:
1. Saves current state with reason
2. Returns to Dashboard
3. Shows stashed work in Dashboard
```

### Resuming

```
User: "/resume login-screen"

OR

User selects "1" from Dashboard

Orchestrator:
1. Loads .session/suspended-login-screen.json
2. Restores feature context
3. Displays current stage and gates
4. Suggests next action
```

## Stale Work Detection

Check for abandoned work on session start.

**Detection criteria:**
- Branch last commit >7 days ago (configurable)
- No workflow activity in >7 days

**Action:**
```
⚠️  Stale Work Detected

Branch: feat/settings-screen
Last commit: 9 days ago
Last workflow activity: 12 days ago
Current stage: TDD Red (incomplete)

Options:
1. Resume work
2. Archive (create archive branch)
3. Delete (abandon)
```

## Best Practices

### DO:
- ✅ Always start from Dashboard
- ✅ Complete one stage before moving to next
- ✅ Follow TDD Red → Green → Refactor cycle
- ✅ Run visual verification before code review
- ✅ Return to Dashboard after completion
- ✅ Stash work if context switching
- ✅ Use gentle guidance, not hard blocks

### DON'T:
- ❌ Skip workflow stages
- ❌ Write implementation before test
- ❌ Mark complete without visual verification
- ❌ Force workflow progression
- ❌ Abandon features without archiving

## References

For detailed information, see:

- `references/state-machine.md` - Complete state machine specification
- `references/integration-patterns.md` - swiftui-dev integration examples
- `references/stash-resume.md` - Context switching patterns

## Related Skills

- `quality-gates` - Gate definitions and enforcement
- `visual-verification` - Screenshot capture and validation
- `session-continuity` - State persistence across sessions
- `context-management` - ADR and lesson tracking
