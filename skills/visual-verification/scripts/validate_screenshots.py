#!/usr/bin/env python3
"""
Validate screenshot existence and basic properties for visual verification gate.
"""

import os
import sys
from pathlib import Path

def validate_screenshots(feature_name, devices):
    """Check if screenshots exist for all required devices."""

    base_dir = Path("visual-proofs") / feature_name
    missing = []
    found = []

    for device in devices:
        device_slug = device.lower().replace(" ", "-").replace("(", "").replace(")", "")
        device_dir = base_dir / device_slug

        if not device_dir.exists():
            missing.append(device)
            continue

        screenshots = list(device_dir.glob("*.png"))
        if not screenshots:
            missing.append(device)
        else:
            found.append((device, len(screenshots)))

    return found, missing

def main():
    if len(sys.argv) < 2:
        print("Usage: validate_screenshots.py <feature-name> [devices...]")
        sys.exit(1)

    feature_name = sys.argv[1]
    devices = sys.argv[2:] if len(sys.argv) > 2 else [
        "iPhone SE (3rd generation)",
        "iPhone 15 Pro",
        "iPad Pro (12.9-inch) (6th generation)"
    ]

    print(f"Validating screenshots for: {feature_name}")
    print(f"Required devices: {', '.join(devices)}")
    print()

    found, missing = validate_screenshots(feature_name, devices)

    if found:
        print("✅ Screenshots found:")
        for device, count in found:
            print(f"  - {device}: {count} screenshot(s)")

    if missing:
        print("\n❌ Missing screenshots for:")
        for device in missing:
            print(f"  - {device}")
        print(f"\nRun: /verify-visual to capture missing screenshots")
        sys.exit(1)

    print("\n✅ All required screenshots present!")
    sys.exit(0)

if __name__ == "__main__":
    main()
