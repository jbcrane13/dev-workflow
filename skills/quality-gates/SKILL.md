---
name: quality-gates
description: This skill should be used when checking quality requirements, validating feature completion readiness, or enforcing development standards. Triggers include "check gates", "gate status", "can I complete this", "quality check", "what gates are pending", and validating TDD compliance, accessibility requirements, build status, visual verification, and code review standards. Defines hard blocks and override procedures for emergency situations.
---

# Quality Gates for Development

Enforce quality standards through hard gates that must pass before feature completion. Gates prevent silent failures and ensure consistent quality across all work.

## Gate Philosophy

Quality gates are **hard blocks**, not suggestions:

1. **No code without tests** - TDD is enforced
2. **No completion without visual proof** - Screenshots required
3. **No silent failures** - Gates must explicitly pass
4. **Emergency override available** - With justification logging

## Gate Definitions

### TDD Gate

**Purpose**: Ensure test-first development

**Validation**:
- Failing test must exist before implementation code
- Test file recently created/modified (`*Tests.swift`)
- Test run output shows failure

**Enforced**: PreToolUse hook (automatic)

**Pass criteria**:
- ✅ Test file exists
- ✅ Test was run and FAILED first
- ✅ Implementation written after test

**Fail criteria**:
- ❌ Implementation code without corresponding test
- ❌ Test not run to verify failure
- ❌ Test file doesn't follow naming convention

**Override**: Not available for TDD gate (fundamental requirement)

**Example validation**:
```bash
# Check for test file
find . -name "*Tests.swift" -newer implementation.swift

# Verify test was run
grep "Test Case.*failed" test-output.log
```

### Test Pass Gate

**Purpose**: Ensure all tests pass before progression

**Validation**:
- All unit tests passing
- All UI tests passing
- No test failures
- Test coverage adequate

**Enforced**: Before transitioning from TDD Green to Refactor

**Pass criteria**:
- ✅ `xcodebuild test` exits 0
- ✅ All test cases pass
- ✅ No flaky tests

**Fail criteria**:
- ❌ Any test failure
- ❌ Build fails
- ❌ Tests don't run

**Override**: Available with justification

**Validation command**:
```bash
/swiftui:test
# Must show: "Test Suite ... passed"
```

### Accessibility Gate

**Purpose**: Ensure all interactive UI has accessibility identifiers

**Validation**:
- Every Button, TextField, Toggle, Picker, Link has `.accessibilityIdentifier()`
- IDs follow naming convention: `{screen}_{element}_{descriptor}`
- List cells include unique IDs with item.id

**Enforced**: PostToolUse hook (automatic), gate-enforcer agent

**Pass criteria**:
- ✅ All interactive elements have IDs
- ✅ IDs follow naming convention
- ✅ No duplicate IDs

**Fail criteria**:
- ❌ Missing accessibility ID on interactive element
- ❌ ID doesn't follow naming convention
- ❌ Duplicate IDs exist

**Override**: Available with justification (not recommended)

**Validation**:
```python
# swiftui-dev provides accessibility_audit.py
python $SWIFTUI_DEV_ROOT/skills/modern-apple-dev/scripts/accessibility_audit.py
```

**Example requirement**:
```swift
Button("Submit") { }
    .accessibilityIdentifier("login_button_submit")

TextField("Email", text: $email)
    .accessibilityIdentifier("login_textfield_email")

ForEach(items) { item in
    ItemRow(item: item)
        .accessibilityIdentifier("home_cell_item_\(item.id)")
}
```

### Build Gate

**Purpose**: Ensure code compiles with zero warnings

**Validation**:
- Build succeeds
- Zero warnings
- Swift 6 concurrency compliance
- No deprecated API usage

**Enforced**: Before any completion stage

**Pass criteria**:
- ✅ `xcodebuild build` exits 0
- ✅ Zero warnings in build log
- ✅ No deprecation warnings

**Fail criteria**:
- ❌ Build fails
- ❌ Any warnings present
- ❌ Deprecated API usage

**Override**: Available for warnings only (not build failures)

**Validation command**:
```bash
/swiftui:build
# Must show: "BUILD SUCCEEDED" with 0 warnings
```

### Visual Verification Gate (MOST IMPORTANT)

**Purpose**: Prove UI works correctly with screenshot evidence

**Validation**:
- App runs successfully
- Screenshots captured for all device sizes
- UI renders completely on screen
- Layout matches requirements
- Behavior works as expected
- No clipping or off-screen content

**Enforced**: Before Code Review stage

**Pass criteria**:
- ✅ App launches without crash
- ✅ Feature accessible in app
- ✅ Screenshots exist for all required devices:
  - Compact (iPhone SE)
  - Standard (iPhone 15 Pro)
  - Max (iPhone 15 Pro Max)
  - Tablet (iPad Pro) if applicable
- ✅ Visual inspection passed:
  - No content running off edges
  - No clipping or overlap
  - Layout correct on all sizes
  - Buttons respond
  - Navigation works
- ✅ Screenshots saved to `visual-proofs/feature-name/device/timestamp.png`

**Fail criteria** (examples):
- ❌ Dashboard with scrollable content running off screen
- ❌ Button partially hidden behind keyboard
- ❌ Text truncated when should wrap
- ❌ Navigation broken (tapping does nothing)
- ❌ Layout broken on iPad (works on iPhone only)
- ❌ Content overlapping other elements
- ❌ Missing device sizes

**Override**: Available for emergency hotfixes only

**Validation approach**:
1. **Automated pre-flight** (gate-enforcer agent):
   - Screenshot files exist at paths
   - Resolution appropriate for device
   - Basic layout analysis (AI vision)
   - Contrast/readability check
2. **Human confirmation required**:
   - "Screenshots analyzed. Layout appears correct. Please confirm UI behaves as expected."
   - User must explicitly approve

**Critical importance**:
This is the MOST IMPORTANT gate. Tests passing and code compiling are NOT sufficient. The UI must be proven to work visually.

### Code Review Gate

**Purpose**: Final quality and standards check

**Validation**:
- No TODO or FIXME comments added during session
- No dead code (unused methods, views, models)
- Modern patterns only (no legacy Swift/SwiftUI)
- Accessibility IDs present
- Architecture follows SOLID principles

**Enforced**: Before Complete stage

**Pass criteria**:
- ✅ No new TODO/FIXME comments
- ✅ No unused code
- ✅ Modern patterns verified (@Observable, SwiftData, NavigationStack)
- ✅ All accessibility IDs present
- ✅ Architecture review passed (if structural changes)

**Fail criteria**:
- ❌ TODO/FIXME comments found
- ❌ Dead code detected
- ❌ Legacy patterns (ObservableObject, @Published, CoreData, @StateObject)
- ❌ Missing accessibility IDs
- ❌ Architectural violations

**Override**: Available with justification

**Validation**:
```bash
# Check for TODOs
grep -r "TODO\|FIXME" --include="*.swift" .

# Run swiftui-dev audit
/swiftui:audit

# Check for legacy patterns
python $SWIFTUI_DEV_ROOT/skills/modern-apple-dev/scripts/legacy_pattern_detector.py

# Run architecture review if structural changes
Deploy: architect-review
```

## Gate Status Display

Show gate status visually:

```
╔════════════════════════════════════════╗
║       Quality Gate Status              ║
╠════════════════════════════════════════╣
║                                        ║
║  ✅ TDD Gate                           ║
║     Tests exist: LoginViewTests.swift  ║
║     Status: 5 passing                  ║
║                                        ║
║  ✅ Accessibility Gate                 ║
║     All elements have IDs              ║
║     Verified: 8 interactive elements   ║
║                                        ║
║  ✅ Build Gate                         ║
║     Build: Success                     ║
║     Warnings: 0                        ║
║                                        ║
║  ❌ Visual Verification Gate           ║
║     Screenshots: Not found             ║
║     Required: SE, Pro, iPad            ║
║     BLOCKING: Run /verify-visual       ║
║                                        ║
║  ⏳ Code Review Gate                   ║
║     Status: Not started                ║
║                                        ║
╠════════════════════════════════════════╣
║  Cannot proceed to completion          ║
║  1 gate failing: Visual Verification   ║
╚════════════════════════════════════════╝
```

## Gate Enforcement Workflow

### At Each Stage Transition

```
User completes refactoring, requests transition to Visual Verify

Orchestrator:
1. Invoke gate-enforcer agent
2. Check applicable gates:
   - TDD Gate (must be passed from earlier)
   - Test Pass Gate (verify still passing)
   - Accessibility Gate (check all IDs present)
   - Build Gate (verify zero warnings)
3. If all pass:
   - Allow transition to Visual Verify
4. If any fail:
   - Block transition
   - Display gate status
   - Provide remediation guidance
```

### Before Feature Completion

```
User believes feature is complete

Orchestrator:
1. Invoke gate-enforcer agent with full validation
2. Check ALL gates:
   - TDD Gate
   - Test Pass Gate
   - Accessibility Gate
   - Build Gate
   - Visual Verification Gate
   - Code Review Gate
3. If all pass:
   - Mark feature complete
   - Archive context
   - Return to Dashboard
4. If any fail:
   - BLOCK completion
   - Show failing gates
   - Guide to resolution
```

## Break Glass Override

Emergency situations may require bypassing a gate.

### When to Override

**Acceptable**:
- P0 production crash requiring hotfix
- Security vulnerability fix
- Critical bug affecting users
- Time-sensitive demo preparation

**NOT acceptable**:
- "I don't want to write tests"
- "Visual verification takes too long"
- "It's just a small change"
- Convenience or laziness

### Override Procedure

```bash
/override gate=visual-verify reason="Hotfix for P0 production crash - UI verification deferred to post-deploy validation"
```

**Logged information**:
```json
{
  "timestamp": "2026-01-19T10:45:00Z",
  "user": "blake",
  "feature": "login-screen",
  "gate": "visual-verify",
  "reason": "Hotfix for P0 production crash - UI verification deferred to post-deploy validation",
  "branch": "feat/login-screen",
  "commit": "abc123"
}
```

**Audit log** (`.claude/context/audit-log.md`):
```markdown
## 2026-01-19 10:45 - Gate Override

**Gate**: Visual Verification
**Feature**: Login Screen
**Reason**: Hotfix for P0 production crash - UI verification deferred to post-deploy validation
**User**: blake
**Branch**: feat/login-screen
**Commit**: abc123

**Follow-up required**: Visual verification must be completed post-deploy
```

### Override Limits

**Cannot override**:
- TDD Gate (fundamental requirement)
- Build Gate when build actually fails (warnings only can be overridden)

**Can override with justification**:
- Test Pass Gate
- Accessibility Gate
- Build Gate (warnings only)
- Visual Verification Gate
- Code Review Gate

## Gate Configuration

Configure gates in `.claude/dev-workflow.local.md`:

```markdown
## Gate Configuration

gates:
  tdd_strict: true  # No override available

  test_pass_required: true
  test_pass_override_allowed: true

  accessibility_required: true
  accessibility_override_allowed: true

  build_warnings_allowed: 0  # Zero warnings required
  build_warnings_override_allowed: true  # Can override warnings

  visual_verification_required: true
  visual_verification_override_allowed: true  # Emergency only
  visual_verification_devices:
    - iPhone SE (3rd generation)
    - iPhone 15 Pro
    - iPad Pro (12.9-inch) (6th generation)

  code_review_required: true
  code_review_override_allowed: true
```

## Gate Validation Scripts

**TDD Gate**:
```bash
# Check for test file newer than implementation
test_file="${impl_file//.swift/Tests.swift}"
[[ "$test_file" -nt "$impl_file" ]]
```

**Accessibility Gate**:
```bash
# Use swiftui-dev audit
python $SWIFTUI_DEV_ROOT/skills/modern-apple-dev/scripts/accessibility_audit.py src/
```

**Build Gate**:
```bash
# Build with zero warnings
xcodebuild build -scheme MyApp 2>&1 | tee build.log
warnings=$(grep -c "warning:" build.log)
[[ $warnings -eq 0 ]]
```

**Visual Verification Gate**:
```bash
# Check screenshot existence
required_devices=("iphone-se" "iphone-15-pro" "ipad-pro")
for device in "${required_devices[@]}"; do
    [[ -d "visual-proofs/$feature_name/$device" ]] || exit 1
done
```

## Best Practices

### DO:
- ✅ Check gates at every stage transition
- ✅ Fix failing gates immediately
- ✅ Provide clear remediation guidance
- ✅ Log all gate checks to audit log
- ✅ Require justification for overrides
- ✅ Review override logs regularly

### DON'T:
- ❌ Skip gate checks
- ❌ Override without justification
- ❌ Allow gates to drift (configuration vs actual)
- ❌ Override for convenience
- ❌ Ignore gate warnings

## Troubleshooting

**"TDD Gate blocking but I have a test"**:
- Verify test file recently modified
- Ensure test was run and failed
- Check test file naming (`*Tests.swift`)

**"Visual Verification passing but UI is broken"**:
- AI pre-flight may have false positive
- Always require human confirmation
- Review screenshots manually

**"Build Gate failing on warnings"**:
- Fix warnings (don't override)
- If urgent hotfix, override with justification
- Plan to fix warnings in follow-up

## References

For detailed information, see:

- `references/gate-validation-scripts.md` - Complete validation script library
- `references/override-procedures.md` - When and how to override gates

## Related Skills

- `workflow-orchestration` - When gates are checked during workflow
- `visual-verification` - How to pass visual verification gate
- `session-continuity` - Gate status persistence
