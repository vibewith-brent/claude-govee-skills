# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Govee LAN API client for local UDP control of smart lights."""

import json
import socket
import struct
import time
from typing import Any


MULTICAST_ADDR = "239.255.255.250"
DISCOVERY_PORT = 4001
LISTEN_PORT = 4002
CONTROL_PORT = 4003
DISCOVERY_TIMEOUT = 3.0


class GoveeLAN:
    """Govee LAN API client for local control."""

    def __init__(self, device_ip: str | None = None):
        """Initialize LAN client with optional device IP."""
        self.device_ip = device_ip
        self.socket = None

    def discover_devices(self, timeout: float = DISCOVERY_TIMEOUT) -> list[dict[str, Any]]:
        """Discover Govee devices on local network via multicast.

        Returns list of devices with structure:
        {
            "ip": "192.168.1.23",
            "device": "1F:80:C5:32:32:36:72:4E",
            "sku": "H606A",
            "bleVersionHard": "3.01.01",
            "bleVersionSoft": "1.03.01",
            "wifiVersionHard": "1.00.10",
            "wifiVersionSoft": "1.02.03"
        }
        """
        # Create UDP socket for discovery
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Enable multicast
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)

        # Bind to listen port for responses
        sock.bind(("", LISTEN_PORT))
        sock.settimeout(timeout)

        # Prepare scan message
        scan_msg = {
            "msg": {
                "cmd": "scan",
                "data": {
                    "account_topic": "reserve"
                }
            }
        }
        message = json.dumps(scan_msg).encode("utf-8")

        # Send multicast discovery
        sock.sendto(message, (MULTICAST_ADDR, DISCOVERY_PORT))

        # Collect responses
        devices = []
        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                data, addr = sock.recvfrom(1024)
                response = json.loads(data.decode("utf-8"))

                if response.get("msg", {}).get("cmd") == "scan":
                    device_data = response["msg"]["data"]
                    devices.append(device_data)
            except socket.timeout:
                break
            except (json.JSONDecodeError, KeyError):
                continue

        sock.close()
        return devices

    def _send_command(self, command: dict[str, Any]) -> dict[str, Any] | None:
        """Send command to device via UDP.

        Most commands do not return responses except devStatus query.
        """
        if not self.device_ip:
            raise ValueError("Device IP not set. Use discover_devices() or set device_ip.")

        message = json.dumps(command).encode("utf-8")

        # Create UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(2.0)

        try:
            # Send command to device
            sock.sendto(message, (self.device_ip, CONTROL_PORT))

            # Only status query returns response
            if command.get("msg", {}).get("cmd") == "devStatus":
                try:
                    data, _ = sock.recvfrom(1024)
                    return json.loads(data.decode("utf-8"))
                except socket.timeout:
                    return None

            return None
        finally:
            sock.close()

    def turn_on(self) -> None:
        """Turn device on."""
        cmd = {"msg": {"cmd": "turn", "data": {"value": 1}}}
        self._send_command(cmd)

    def turn_off(self) -> None:
        """Turn device off."""
        cmd = {"msg": {"cmd": "turn", "data": {"value": 0}}}
        self._send_command(cmd)

    def set_brightness(self, level: int) -> None:
        """Set brightness (1-100)."""
        level = max(1, min(100, level))
        cmd = {"msg": {"cmd": "brightness", "data": {"value": level}}}
        self._send_command(cmd)

    def set_color(self, r: int, g: int, b: int) -> None:
        """Set RGB color (0-255 each)."""
        r = max(0, min(255, r))
        g = max(0, min(255, g))
        b = max(0, min(255, b))
        cmd = {
            "msg": {
                "cmd": "colorwc",
                "data": {
                    "color": {"r": r, "g": g, "b": b},
                    "colorTemInKelvin": 0
                }
            }
        }
        self._send_command(cmd)

    def set_temperature(self, kelvin: int) -> None:
        """Set color temperature (2000-9000K)."""
        kelvin = max(2000, min(9000, kelvin))
        cmd = {
            "msg": {
                "cmd": "colorwc",
                "data": {
                    "color": {"r": 0, "g": 0, "b": 0},
                    "colorTemInKelvin": kelvin
                }
            }
        }
        self._send_command(cmd)

    def get_status(self) -> dict[str, Any] | None:
        """Query device status.

        Returns response like:
        {
            "msg": {
                "cmd": "devStatus",
                "data": {
                    "onOff": 1,
                    "brightness": 100,
                    "color": {"r": 255, "g": 0, "b": 0},
                    "colorTemInKelvin": 7200
                }
            }
        }
        """
        cmd = {"msg": {"cmd": "devStatus", "data": {}}}
        return self._send_command(cmd)


def main() -> None:
    """CLI for LAN API testing."""
    import sys

    if len(sys.argv) < 2:
        print("""Usage: uv run govee_lan.py <command> [args]

Commands:
  discover                     Discover devices on local network
  status <ip>                  Query device status
  on <ip>                      Turn device on
  off <ip>                     Turn device off
  brightness <ip> <1-100>      Set brightness
  color <ip> <r> <g> <b>       Set RGB color (0-255 each)
  temperature <ip> <K>         Set color temp (2000-9000K)

Examples:
  uv run govee_lan.py discover
  uv run govee_lan.py on 192.168.1.23
  uv run govee_lan.py brightness 192.168.1.23 75
  uv run govee_lan.py color 192.168.1.23 255 0 128
  uv run govee_lan.py temperature 192.168.1.23 4000
""")
        sys.exit(1)

    cmd = sys.argv[1].lower()

    if cmd == "discover":
        client = GoveeLAN()
        devices = client.discover_devices()
        print(f"Found {len(devices)} device(s):\n")
        for dev in devices:
            print(json.dumps(dev, indent=2))
        sys.exit(0)

    if len(sys.argv) < 3:
        print("Error: IP address required", file=sys.stderr)
        sys.exit(1)

    ip = sys.argv[2]
    client = GoveeLAN(device_ip=ip)

    match cmd:
        case "status":
            result = client.get_status()
            print(json.dumps(result, indent=2))
        case "on":
            client.turn_on()
            print("Device turned on")
        case "off":
            client.turn_off()
            print("Device turned off")
        case "brightness" if len(sys.argv) == 4:
            client.set_brightness(int(sys.argv[3]))
            print(f"Brightness set to {sys.argv[3]}")
        case "color" if len(sys.argv) == 6:
            r, g, b = int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
            client.set_color(r, g, b)
            print(f"Color set to RGB({r}, {g}, {b})")
        case "temperature" if len(sys.argv) == 4:
            kelvin = int(sys.argv[3])
            client.set_temperature(kelvin)
            print(f"Temperature set to {kelvin}K")
        case _:
            print(f"Unknown command or wrong arguments: {cmd}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
