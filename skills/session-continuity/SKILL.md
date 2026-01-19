---
name: session-continuity
description: This skill should be used when resuming work across Claude Code sessions, managing workflow state persistence, stashing and resuming features, or handling session start/end activities. Triggers include "resume work", "restore session", "what was I working on", "stash feature", session start activities, and maintaining development context across interruptions.
---

# Session Continuity for Development

Preserve and restore workflow state across Claude Code sessions.

## Core Capabilities

1. **Session Start** - Load context, restore workflow state, display dashboard
2. **Session End** - Save state, prompt for lessons
3. **Stash/Resume** - Handle context switching
4. **Stale Detection** - Warn about abandoned work

## Session Start Workflow

**Trigger**: Claude Code session begins (SessionStart hook)

**Actions**:
1. Load `.claude/context/active/*.md` files
2. Load `.session/state.json`
3. Check for stale work (>7 days by default)
4. Display Dashboard or restore active feature
5. Show gate status summary

**Output**:
```
╔════════════════════════════════════════════════════════════╗
║            Welcome Back - Session Restored                 ║
╠════════════════════════════════════════════════════════════╣
║                                                            ║
║  Last Active: Login Screen feature                         ║
║  Current Stage: Visual Verify                              ║
║  Branch: feat/login-screen                                 ║
║                                                            ║
║  Workflow Progress:                                        ║
║    ✅ Planning → ✅ TDD Red → ✅ TDD Green → ✅ Refactor    ║
║    🔄 Visual Verify (current)                              ║
║                                                            ║
║  Last Action: Updated AuthService to use async/await       ║
║                                                            ║
║  Pending Gates:                                            ║
║    ✅ TDD - Tests passing                                  ║
║    ✅ Accessibility - All IDs present                      ║
║    ✅ Build - No warnings                                  ║
║    ⏳ Visual Verification - Not started                    ║
║    ⏳ Code Review - Not started                            ║
║                                                            ║
║  Ready to continue with visual verification?               ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
```

## Session State Format

**File**: `.session/state.json`

```json
{
  "activeFeature": "login-screen",
  "currentStage": "Visual Verify",
  "branch": "feat/login-screen",
  "gateStatus": {
    "tdd": "passed",
    "testPass": "passed",
    "accessibility": "passed",
    "build": "passed",
    "visualVerification": "pending",
    "codeReview": "pending"
  },
  "recentDecisions": [
    "Use @Observable for AuthService",
    "Store token in Keychain (ADR-007)"
  ],
  "lastAction": "Updated AuthService to use async/await",
  "timestamp": "2026-01-19T10:30:00Z",
  "sessionCount": 3
}
```

## Stash and Resume

### Automatic Stashing

When starting new feature while one is active:

```
User: "/start-feature"

Detect: Active feature exists (Login Screen)

Prompt:
"Active feature detected: Login Screen (stage: Visual Verify)
1. Stash and start new
2. Continue current
3. View Dashboard

Choice?"

If stash:
1. Save to .session/suspended-login-screen.json
2. Clear active context
3. Proceed with new feature
```

### Manual Stashing

```bash
/stash "Need to fix urgent bug"
```

**Creates**: `.session/suspended-feature-name.json` with reason

### Resuming

```bash
/resume login-screen
```

**Or select from Dashboard**:
```
1. Login Screen [Suspended: 2 hours ago] 🔄
```

**Loads**:
1. Suspended state JSON
2. Feature context from `.claude/context/active/`
3. Restores workflow stage
4. Shows gate status
5. Suggests next action

## Stale Work Detection

**Criteria**:
- Branch last commit >7 days (configurable in `.claude/dev-workflow.local.md`)
- No workflow activity >7 days

**Detection**: On session start

**Prompt**:
```
⚠️  Stale Work Detected

Branch: feat/settings-screen
Last commit: 9 days ago
Last workflow activity: 12 days ago
Current stage: TDD Red (incomplete)

Options:
1. Resume work
2. Archive (create archive/settings-screen branch)
3. Delete (abandon, close context)
```

## Session End Workflow

**Trigger**: Claude Code session ends (Stop hook)

**Actions**:
1. Save current state to `.session/state.json`
2. Update feature context in `.claude/context/active/`
3. Increment session count
4. Prompt for lessons learned (if applicable)

**Lessons prompt**:
```
Session ending. Record any lessons learned?

Categories:
- Process: Workflow insights
- Tech: Framework/language gotchas
- Tooling: IDE, build, dependency issues

/record-lesson [title]  or  Skip
```

## Configuration

**In `.claude/dev-workflow.local.md`**:

```markdown
## Workflow Preferences

auto_summarize_on_session_start: true
check_stale_work_days: 7
hub_dashboard_on_start: true
prompt_for_lessons_on_stop: true
```

## State Persistence Files

```
.session/
├── state.json                      # Current active state
├── suspended-feature-1.json        # Stashed features
├── suspended-feature-2.json
└── history/
    └── 2026-01-19-session.json    # Session history
```

## Best Practices

**DO**:
- ✅ Load context on every session start
- ✅ Save state on session end
- ✅ Check for stale work regularly
- ✅ Prompt for lessons after problem-solving
- ✅ Archive completed features

**DON'T**:
- ❌ Skip state persistence
- ❌ Ignore stale work warnings
- ❌ Abandon features without archiving

## Related Skills

- `workflow-orchestration` - Workflow stages persisted
- `context-management` - What context is saved
- `quality-gates` - Gate status persistence
