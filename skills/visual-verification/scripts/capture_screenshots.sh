#!/bin/bash
# Batch screenshot capture for all configured devices
# Usage: capture_screenshots.sh <feature-name>

set -e

FEATURE_NAME="${1:-current-feature}"
SCREENSHOT_DIR="visual-proofs/$FEATURE_NAME"
TIMESTAMP=$(date +%Y-%m-%d-%H%M%S)

# Default devices (override in .claude/dev-workflow.local.md)
DEVICES=(
    "iPhone SE (3rd generation)"
    "iPhone 15 Pro"
    "iPad Pro (12.9-inch) (6th generation)"
)

echo "Capturing screenshots for feature: $FEATURE_NAME"
echo "Devices: ${DEVICES[@]}"

for DEVICE in "${DEVICES[@]}"; do
    DEVICE_SLUG=$(echo "$DEVICE" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | sed 's/[()]//g')
    DEVICE_DIR="$SCREENSHOT_DIR/$DEVICE_SLUG"

    mkdir -p "$DEVICE_DIR"

    echo "Capturing on: $DEVICE"

    # Use swiftui-dev screenshot command
    /swiftui:screenshot "$FEATURE_NAME" --device "$DEVICE" --output "$DEVICE_DIR/$TIMESTAMP.png"

    echo "  Saved to: $DEVICE_DIR/$TIMESTAMP.png"
done

echo "Screenshot capture complete!"
echo "Review screenshots in: $SCREENSHOT_DIR"
