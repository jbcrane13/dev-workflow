---
name: verify-visual
description: Run visual verification gate - build app, capture screenshots on multiple devices, and validate UI correctness
---

# Visual Verification Command

Capture screenshots and validate UI works correctly - the most important quality gate.

## Usage

```
/verify-visual [options]
```

**Options**:
- `--device "<name>"` - Single device (overrides default)
- `--batch` - All configured devices
- `--feature <name>` - Feature name (default: current active)

## Process

1. **Pre-flight Checks**
   - Verify app builds: `/swiftui:build`
   - Verify tests pass: `/swiftui:test`
   - Check active feature in workflow

2. **Determine Devices**
   From `.claude/dev-workflow.local.md`:
   ```markdown
   gates:
     visual_verification_devices:
       - iPhone SE (3rd generation)
       - iPhone 15 Pro
       - iPad Pro (12.9-inch) (6th generation)
   ```

3. **For Each Device**:
   a. Boot simulator (if not running)
   b. Build and install app
   c. Launch app
   d. **Interactive**: User navigates to feature
   e. Capture screenshots:
      ```bash
      /swiftui:screenshot {feature-name} --device "{device-name}"
      ```
   f. Save to: `visual-proofs/{feature-name}/{device-slug}/YYYY-MM-DD-HHMMSS-{state}.png`

4. **Visual Inspection Prompts**
   For each captured screenshot:
   ```
   Screenshot captured: {path}

   Checklist:
   - [ ] All content visible (not clipped)
   - [ ] No content running off edges
   - [ ] Proper spacing and alignment
   - [ ] Interactive elements accessible
   - [ ] Layout correct for this device size

   Screenshot OK? (y/n/skip)
   ```

5. **AI Pre-flight Analysis**
   **gate-enforcer** agent analyzes:
   - Screenshot files exist
   - Resolution appropriate
   - Basic layout (elements on-screen)
   - Contrast/readability

6. **Human Confirmation Required**
   ```
   AI Analysis Complete:
   ✅ iPhone SE: Layout appears correct
   ✅ iPhone 15 Pro: Layout appears correct
   ✅ iPad Pro: Layout appears correct

   Please confirm by testing in running app:
   1. Navigation works correctly
   2. Buttons respond to taps
   3. Text input functions properly
   4. No visual bugs observed

   Approve visual verification? (yes/no/review)
   ```

   **User must explicitly approve** - AI cannot fully validate behavior

7. **Update Gate Status**
   If approved:
   - Mark Visual Verification Gate as passed
   - Update `.session/state.json`
   - Update feature context
   - Suggest transition to Code Review

## Examples

**Default (all devices)**:
```
/verify-visual
```

**Single device**:
```
/verify-visual --device "iPad Pro (12.9-inch) (6th generation)"
```

**Batch mode**:
```
/verify-visual --batch
```

## Troubleshooting

**App won't launch**:
- Check build succeeded
- Verify correct bundle ID
- Check simulator logs

**Screenshots blank/black**:
- Wait for UI to render before capturing
- Ensure app isn't showing error state

**Gate passes but UI actually broken**:
- Always manually test interactions
- Don't rely solely on AI analysis
- Review screenshots carefully

## Critical Importance

This is the **MOST IMPORTANT gate**:
- Dashboard with content running off-screen = **HARD FAIL**
- Even if tests pass and code compiles
- Visual proof required before completion

## Related Commands

- `/gate-status` - Check if visual verification passed
- `/workflow-status` - See next step after verification
- `/swiftui:screenshot` - Lower-level screenshot capture
