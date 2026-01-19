---
name: gate-status
description: Show detailed quality gate validation status with pass/fail criteria and remediation guidance
---

# Gate Status Command

Display detailed quality gate status with validation details.

## Usage

```
/gate-status
```

## Output

```
╔════════════════════════════════════════╗
║       Quality Gate Status              ║
╠════════════════════════════════════════╣
║                                        ║
║  ✅ TDD Gate                           ║
║     Tests exist: LoginViewTests.swift  ║
║     Status: 5 tests passing            ║
║     Last run: 2 minutes ago            ║
║                                        ║
║  ✅ Accessibility Gate                 ║
║     Interactive elements: 8            ║
║     With IDs: 8                        ║
║     Missing IDs: 0                     ║
║                                        ║
║  ✅ Build Gate                         ║
║     Build: Success                     ║
║     Warnings: 0                        ║
║     Errors: 0                          ║
║                                        ║
║  ❌ Visual Verification Gate           ║
║     Status: BLOCKING                   ║
║     Screenshots: Not found             ║
║     Required devices:                  ║
║       - iPhone SE (3rd generation)     ║
║       - iPhone 15 Pro                  ║
║       - iPad Pro (12.9-inch)           ║
║     Action: Run /verify-visual         ║
║                                        ║
║  ⏳ Code Review Gate                   ║
║     Status: Not started                ║
║     Prerequisite: Visual Verify        ║
║                                        ║
╠════════════════════════════════════════╣
║  Overall Status: 1 gate failing        ║
║  Can proceed: NO                       ║
╚════════════════════════════════════════╝
```

## Process

1. Invoke **gate-enforcer** agent
2. Check all gates:
   - TDD: Test files and test runs
   - Accessibility: Run audit script
   - Build: Check build log
   - Visual Verification: Check screenshot paths
   - Code Review: Check for TODOs, dead code
3. Format results with remediation guidance

## Related Commands

- `/workflow-status` - Overall workflow state
- `/verify-visual` - Run visual verification
- `/override` - Emergency gate bypass
