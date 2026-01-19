---
name: visual-verification
description: This skill should be used when validating UI correctness through screenshots, running visual verification checks, capturing app screenshots on multiple devices, or proving that implemented features work correctly. Triggers include "verify visual", "capture screenshots", "test UI", "visual proof", "screenshot verification", and ensuring no layout issues like clipped content, off-screen elements, or broken interactions before feature completion.
---

# Visual Verification for Development

Prove UI works correctly with screenshot evidence - the most important quality gate.

## Critical Importance

Visual verification is the **MOST IMPORTANT** quality gate:

- Tests passing ≠ UI works correctly
- Code compiling ≠ Layout is correct
- **Screenshots prove the feature actually works**

**Example failures** (HARD BLOCK even if all tests pass):
- ❌ Dashboard with content running off bottom of screen
- ❌ Button partially hidden behind keyboard
- ❌ Text truncated with `...` when it should wrap
- ❌ Navigation broken (tapping button does nothing)
- ❌ Layout works on iPhone but broken on iPad

## Visual Verification Workflow

### 1. Pre-Verification Checklist

Before running `/verify-visual`:

- [ ] App builds successfully (`/swiftui:build`)
- [ ] All tests passing (`/swiftui:test`)
- [ ] Feature accessible in running app
- [ ] Required simulators available
- [ ] Know all screens/states to verify

### 2. Run Visual Verification

```bash
/verify-visual
```

**Process**:
1. **Build app** - Ensure latest code
2. **Launch simulators** - All required device sizes
3. **Install app** - On each simulator
4. **Navigate to feature** - Access implemented screens
5. **Capture screenshots** - All states, all devices
6. **Save screenshots** - Organized by device and state

### 3. Device Size Requirements

**Default devices** (configurable in `.claude/dev-workflow.local.md`):
- **Compact**: iPhone SE (3rd generation) - Smallest screen
- **Standard**: iPhone 15 Pro - Typical modern iPhone
- **Max**: iPhone 15 Pro Max - Largest iPhone
- **Tablet**: iPad Pro (12.9-inch) - iPad layout

**Why multiple sizes matter**:
- Layout that works on iPhone 15 Pro may fail on SE (smaller)
- Layout that works on iPhone may break on iPad (different size class)

### 4. Screenshot Organization

**Path structure**:
```
visual-proofs/
└── feature-name/
    ├── iphone-se/
    │   ├── 2026-01-19-103045-login-initial.png
    │   └── 2026-01-19-103046-login-filled.png
    ├── iphone-15-pro/
    │   ├── 2026-01-19-103047-login-initial.png
    │   └── 2026-01-19-103048-login-filled.png
    └── ipad-pro/
        ├── 2026-01-19-103049-login-initial.png
        └── 2026-01-19-103050-login-filled.png
```

**Filename format**: `YYYY-MM-DD-HHMMSS-screen-state.png`

### 5. What to Capture

**For each device size, capture**:
- Initial state (screen first appears)
- Filled state (with test data)
- Error states (if applicable)
- Loading states (if applicable)
- Different orientations (portrait/landscape if supported)

**User flows to test**:
- Happy path (everything works)
- Error scenarios (validation failures)
- Edge cases (very long text, empty states)

### 6. Visual Inspection Checklist

Review each screenshot for:

**Layout correctness**:
- [ ] All content visible on screen (not clipped)
- [ ] No content running off edges
- [ ] Proper spacing and alignment
- [ ] Correct font sizes and weights
- [ ] Consistent margins/padding

**Interactive elements**:
- [ ] All buttons visible and accessible
- [ ] Text fields not hidden behind keyboard
- [ ] Tap targets large enough (44×44 points minimum)
- [ ] No overlapping elements

**Device-specific**:
- [ ] Safe area insets respected
- [ ] Notch/Dynamic Island handled
- [ ] Home indicator area clear
- [ ] Different size classes handled

**Behavior** (manual testing required):
- [ ] Buttons respond to taps
- [ ] Navigation works correctly
- [ ] Text fields accept input
- [ ] Gestures work (swipe, pinch, etc.)
- [ ] Animations smooth

### 7. Gate Validation

**Hybrid approach** (AI pre-flight + human confirmation):

**AI checks** (gate-enforcer agent):
- Screenshot files exist at correct paths
- Resolution appropriate for device
- Basic layout analysis:
  - Elements on-screen (not clipped)
  - Reasonable contrast
  - No obvious overlaps
  - Text readable

**Human confirmation required**:
```
I've analyzed the screenshots. Layout appears correct on all devices:
- iPhone SE: ✅ All content visible
- iPhone 15 Pro: ✅ Layout correct
- iPad Pro: ✅ Tablet layout working

Please confirm the UI behaves as expected:
1. Navigation works correctly
2. Buttons respond to taps
3. Text input functions properly
4. No visual bugs observed

Approve visual verification? (yes/no)
```

**User must explicitly approve** - AI cannot fully validate behavior

## Integration with swiftui-dev

Visual verification uses swiftui-dev capabilities:

**Screenshot capture**:
```bash
/swiftui:screenshot feature-name --device "iPhone SE (3rd generation)"
/swiftui:screenshot feature-name --device "iPhone 15 Pro"
/swiftui:screenshot feature-name --device "iPad Pro (12.9-inch) (6th generation)"
```

**Or batch**:
```bash
/swiftui:screenshot feature-name --all-devices
```

**Uses**: `$SWIFTUI_DEV_ROOT/skills/ios-simulator/scripts/screenshot.py`

## Common Visual Issues

**Layout problems**:
- Content extends beyond screen bounds (ScrollView missing)
- Button hidden behind keyboard (keyboard avoidance needed)
- Text truncated (line limit too low, should use `.lineLimit(nil)`)
- Overlap between elements (conflicting constraints)

**Size class issues**:
- iPad shows iPhone layout (not using size classes)
- iPhone SE truncates content that fits on larger phones
- Landscape broken (only tested portrait)

**Safe area problems**:
- Content behind notch/Dynamic Island
- Content behind home indicator
- Content behind status bar

## Troubleshooting

**"App won't launch in simulator"**:
- Check build succeeded
- Verify app installed: `xcrun simctl listapps booted`
- Check simulator console for crash logs

**"Screenshots blank/black"**:
- Wait for app to fully render before capturing
- Check UI actually loaded (not error state)
- Verify screenshot script has correct bundle ID

**"Layout looks correct but behavior broken"**:
- Visual verification catches layout, not behavior
- Must manually test interactions
- Add UI tests for behavior validation

**"Gate passes but UI is actually broken"**:
- AI pre-flight has limitations
- Always require human confirmation
- Review screenshots manually, don't trust AI completely

## Configuration

**In `.claude/dev-workflow.local.md`**:

```markdown
## Screenshot Storage
screenshot_path: visual-proofs/
screenshot_device_default: iPhone 15 Pro

## Gate Configuration
gates:
  visual_verification_required: true
  visual_verification_devices:
    - iPhone SE (3rd generation)
    - iPhone 15 Pro
    - iPad Pro (12.9-inch) (6th generation)
```

## Best Practices

**DO**:
- ✅ Test on smallest device (iPhone SE) first
- ✅ Capture multiple states (empty, filled, error)
- ✅ Test keyboard handling for text fields
- ✅ Verify both portrait and landscape if supported
- ✅ Actually tap buttons to verify they work
- ✅ Save all screenshots for proof

**DON'T**:
- ❌ Test only on one device size
- ❌ Skip visual verification (most important gate!)
- ❌ Rely only on AI analysis
- ❌ Approve without actually testing interactions
- ❌ Delete screenshots after verification

## Scripts

**Available in `scripts/`**:
- `capture_screenshots.sh` - Batch capture for all devices
- `validate_screenshots.py` - Check screenshot existence and resolution

## Related Skills

- `quality-gates` - Visual verification gate definition
- `workflow-orchestration` - When visual verification occurs
- `ios-simulator` (swiftui-dev) - Simulator management and screenshot capture
