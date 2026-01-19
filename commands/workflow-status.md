---
name: workflow-status
description: Display current workflow state, active feature, stage progression, and gate status
---

# Workflow Status Command

Show comprehensive workflow state including current stage, gates, and progress.

## Usage

```
/workflow-status
```

## Output

Displays formatted workflow dashboard:

```
╔════════════════════════════════════════════════════════════╗
║              Workflow Status                               ║
╠════════════════════════════════════════════════════════════╣
║                                                            ║
║  Feature: Login Screen                                     ║
║  Branch: feat/login-screen                                 ║
║  Stage: Visual Verify 🔄                                   ║
║                                                            ║
║  Progress:                                                 ║
║    ✅ Planning → ✅ TDD Red → ✅ TDD Green → ✅ Refactor    ║
║    🔄 Visual Verify (current) → ⏳ Code Review             ║
║                                                            ║
║  Quality Gates:                                            ║
║    ✅ TDD - Tests passing                                  ║
║    ✅ Accessibility - All IDs present                      ║
║    ✅ Build - Zero warnings                                ║
║    ⏳ Visual Verification - Pending                        ║
║    ⏳ Code Review - Not started                            ║
║                                                            ║
║  Recent Decisions:                                         ║
║    - Use @Observable for AuthService                       ║
║    - Store token in Keychain (ADR-007)                     ║
║                                                            ║
║  Next Action:                                              ║
║    Run /verify-visual to capture screenshots               ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
```

## Process

1. Load `.session/state.json`
2. Load `.claude/context/active/{feature-name}.md`
3. Check gate status (invoke gate-enforcer if needed)
4. Format and display

## Related Commands

- `/gate-status` - Detailed gate information
- `/start-feature` - Begin new feature
- `/verify-visual` - Next action if in Visual Verify stage
