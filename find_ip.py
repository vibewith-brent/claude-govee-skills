# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Scan local network to find Govee device IP."""

import socket
import sys
from govee_lan import GoveeLAN


def scan_network(subnet: str = "192.168.1") -> list[str]:
    """Scan network for Govee devices by testing status query."""
    print(f"Scanning {subnet}.0/24 for Govee devices...")
    found = []

    for i in range(1, 255):
        ip = f"{subnet}.{i}"
        try:
            client = GoveeLAN(device_ip=ip)
            # Quick status check with short timeout
            result = client.get_status()
            if result and "msg" in result:
                print(f"✓ Found Govee device at {ip}")
                found.append(ip)
        except (socket.timeout, OSError, ConnectionRefusedError):
            pass
        except Exception as e:
            pass

        if i % 10 == 0:
            print(f"  Scanned {i}/254...", end="\r")

    return found


def main() -> None:
    if len(sys.argv) > 1:
        subnet = sys.argv[1]
    else:
        subnet = "192.168.1"
        print("Using default subnet 192.168.1.x")
        print("Specify different subnet: uv run find_ip.py 192.168.0\n")

    devices = scan_network(subnet)

    if devices:
        print(f"\nFound {len(devices)} device(s):")
        for ip in devices:
            print(f"  - {ip}")
        print(f"\nTest with: uv run pattern_demo.py {devices[0]} rainbow")
    else:
        print("\nNo devices found. Make sure:")
        print("  1. LAN Control is enabled in Govee app")
        print("  2. Device is on same network")
        print("  3. Correct subnet specified")


if __name__ == "__main__":
    main()
