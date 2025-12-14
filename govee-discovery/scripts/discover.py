# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Discover Govee devices via multicast."""

import json
import sys
import os

# Add parent scripts directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../govee-control/scripts'))

from govee_lan import GoveeLAN


def main() -> None:
    """Discover Govee devices on local network."""
    client = GoveeLAN()
    print("Scanning for Govee devices via multicast...")

    devices = client.discover_devices()

    if devices:
        print(f"\nFound {len(devices)} device(s):\n")
        for dev in devices:
            print(json.dumps(dev, indent=2))
    else:
        print("\nNo devices found.")
        print("\nTroubleshooting:")
        print("  1. Enable LAN Control in Govee Home App")
        print("  2. Ensure device is on same network")
        print("  3. Check firewall allows UDP ports 4001-4003")


if __name__ == "__main__":
    main()
