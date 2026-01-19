# dev-workflow Configuration Template

Copy this to `.claude/dev-workflow.local.md` in your project and customize.

```markdown
# dev-workflow Configuration

## Implementation Plugin
preferred_plugin: swiftui-dev

## Screenshot Storage
screenshot_path: visual-proofs/
screenshot_device_default: iPhone 15 Pro

## Gate Configuration
gates:
  tdd_strict: true  # No override available

  test_pass_required: true
  test_pass_override_allowed: true

  accessibility_required: true
  accessibility_override_allowed: true

  build_warnings_allowed: 0  # Zero warnings required
  build_warnings_override_allowed: true

  visual_verification_required: true
  visual_verification_override_allowed: true  # Emergency only
  visual_verification_devices:
    - iPhone SE (3rd generation)
    - iPhone 15 Pro
    - iPad Pro (12.9-inch) (6th generation)

  code_review_required: true
  code_review_override_allowed: true

## Context Storage
adr_path: docs/adr/
lessons_path: .claude/context/lessons/
architecture_notes_path: .claude/context/architecture/
context_path: .claude/context/

## Workflow Preferences
auto_create_branch: true
auto_summarize_on_session_start: true
check_stale_work_days: 7
hub_dashboard_on_start: true
prompt_for_lessons_on_stop: true

## Audit
audit_log_path: .claude/context/audit-log.md
log_overrides: true

## Device Size Classes (Optional)
# Define size classes for visual verification
size_classes:
  compact:
    name: iPhone SE (3rd generation)
    description: Smallest supported screen
  standard:
    name: iPhone 15 Pro
    description: Standard modern iPhone
  max:
    name: iPhone 15 Pro Max
    description: Largest iPhone
  tablet:
    name: iPad Pro (12.9-inch) (6th generation)
    description: Tablet size
```

## Usage

1. Copy this file to your project: `.claude/dev-workflow.local.md`
2. Customize settings for your project
3. Add to `.gitignore`: `.claude/*.local.md`
4. Commit the template (this file) to version control for team reference
