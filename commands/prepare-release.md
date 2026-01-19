---
name: prepare-release
description: Run complete release checklist validating all features, gates, and readiness
---

# Prepare Release Command

Validate all work is ready for release.

## Usage

```
/prepare-release
```

## Checklist

1. **All Features Complete**
   - No active features (Dashboard clear)
   - No stashed work
   - No stale branches

2. **All Gates Passed**
   For each feature branch:
   - TDD Gate: ✅
   - Accessibility Gate: ✅
   - Build Gate: ✅
   - Visual Verification Gate: ✅
   - Code Review Gate: ✅

3. **Code Quality**
   - No TODO/FIXME comments
   - No dead code
   - Modern patterns only
   - Zero warnings

4. **Git Status**
   - All changes committed
   - No uncommitted work
   - Clean working directory

5. **Version Bump**
   - Prompt for version number
   - Update Info.plist
   - Tag release

## Process

Invoke **gate-enforcer** agent for comprehensive validation across all branches.

## Related Commands

- `/workflow-status` - Check current state
- `/gate-status` - Verify all gates
