# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "httpx",
#     "python-dotenv",
# ]
# ///
"""Govee API client for controlling smart lights (Cloud and LAN)."""

import json
import os
import sys
import uuid
from pathlib import Path

import httpx
from dotenv import load_dotenv

from govee_lan import GoveeLAN

BASE_URL = "https://openapi.api.govee.com"
DEVICES_ENDPOINT = "/router/api/v1/user/devices"
CONTROL_ENDPOINT = "/router/api/v1/device/control"
SCENES_ENDPOINT = "/router/api/v1/device/scenes"


def get_api_key() -> str:
    """Load API key from environment or .env file."""
    load_dotenv()
    key = os.getenv("GOVEE_API_KEY")
    if not key:
        print("Error: GOVEE_API_KEY not set. Set it in environment or .env file.", file=sys.stderr)
        sys.exit(1)
    return key


def make_request(method: str, endpoint: str, data: dict | None = None) -> dict:
    """Make authenticated request to Govee API."""
    headers = {
        "Govee-API-Key": get_api_key(),
        "Content-Type": "application/json",
    }
    url = f"{BASE_URL}{endpoint}"

    with httpx.Client(timeout=60) as client:
        if method == "GET":
            response = client.get(url, headers=headers)
        else:
            response = client.post(url, headers=headers, json=data)

    if response.status_code == 401:
        print("Error: Invalid API key", file=sys.stderr)
        sys.exit(1)
    if response.status_code == 429:
        print("Error: Rate limit exceeded (10,000/day)", file=sys.stderr)
        sys.exit(1)

    return response.json()


def list_devices() -> None:
    """List all Govee devices and their capabilities."""
    result = make_request("GET", DEVICES_ENDPOINT)
    print(json.dumps(result, indent=2))


def control_device(device: str, sku: str, capability_type: str, instance: str, value: int | dict) -> None:
    """Send control command to device."""
    payload = {
        "requestId": str(uuid.uuid4()),
        "payload": {
            "sku": sku,
            "device": device,
            "capability": {
                "type": capability_type,
                "instance": instance,
                "value": value,
            },
        },
    }
    result = make_request("POST", CONTROL_ENDPOINT, payload)
    print(json.dumps(result, indent=2))


def power(device: str, sku: str, state: str) -> None:
    """Turn device on or off."""
    value = 1 if state.lower() == "on" else 0
    control_device(device, sku, "devices.capabilities.on_off", "powerSwitch", value)


def brightness(device: str, sku: str, level: int) -> None:
    """Set brightness (1-100)."""
    level = max(1, min(100, level))
    control_device(device, sku, "devices.capabilities.range", "brightness", level)


def color(device: str, sku: str, r: int, g: int, b: int) -> None:
    """Set RGB color (0-255 each)."""
    r = max(0, min(255, r))
    g = max(0, min(255, g))
    b = max(0, min(255, b))
    rgb_value = (r << 16) + (g << 8) + b
    control_device(device, sku, "devices.capabilities.color_setting", "colorRgb", rgb_value)


def temperature(device: str, sku: str, kelvin: int) -> None:
    """Set color temperature (2000-9000K)."""
    kelvin = max(2000, min(9000, kelvin))
    control_device(device, sku, "devices.capabilities.color_setting", "colorTemperatureK", kelvin)


def segment_color(device: str, sku: str, segments: list[int], r: int, g: int, b: int) -> None:
    """Set color for specific segments."""
    r = max(0, min(255, r))
    g = max(0, min(255, g))
    b = max(0, min(255, b))
    rgb_value = (r << 16) + (g << 8) + b
    value = {"segment": segments, "rgb": rgb_value}
    control_device(device, sku, "devices.capabilities.segment_color_setting", "segmentedColorRgb", value)


def gradient_pattern(device: str, sku: str) -> None:
    """Apply a rainbow gradient pattern across all segments."""
    import time
    colors = [
        (255, 0, 0),     # Red
        (255, 127, 0),   # Orange
        (255, 255, 0),   # Yellow
        (0, 255, 0),     # Green
        (0, 255, 255),   # Cyan
        (0, 0, 255),     # Blue
        (139, 0, 255),   # Purple
    ]
    # Apply different colors to different segment groups
    for i, (r, g, b) in enumerate(colors):
        segments = [i * 2, i * 2 + 1] if i * 2 + 1 <= 14 else [i * 2]
        segments = [s for s in segments if s <= 14]
        if segments:
            segment_color(device, sku, segments, r, g, b)
            time.sleep(0.3)


def list_scenes(device: str, sku: str) -> None:
    """List available dynamic scenes for a device."""
    payload = {
        "requestId": str(uuid.uuid4()),
        "payload": {
            "sku": sku,
            "device": device,
        },
    }
    result = make_request("POST", SCENES_ENDPOINT, payload)

    # Parse and display scenes in a readable format
    if result.get("code") == 200 and "payload" in result:
        capabilities = result["payload"].get("capabilities", [])
        for cap in capabilities:
            if cap.get("instance") == "lightScene":
                options = cap.get("parameters", {}).get("options", [])
                print(f"Available scenes ({len(options)}):\n")
                for opt in options:
                    name = opt.get("name", "Unknown")
                    value = opt.get("value", {})
                    param_id = value.get("paramId", "")
                    scene_id = value.get("id", "")
                    print(f"  {name}: paramId={param_id}, id={scene_id}")
                return
    # Fallback: print raw response
    print(json.dumps(result, indent=2))


def apply_scene(device: str, sku: str, param_id: int, scene_id: int) -> None:
    """Apply a dynamic scene by paramId and id."""
    value = {"paramId": param_id, "id": scene_id}
    control_device(device, sku, "devices.capabilities.dynamic_scene", "lightScene", value)


def print_usage() -> None:
    """Print usage instructions."""
    print("""Usage: uv run govee.py [--lan] <command> [args]

Options:
  --lan                                     Use LAN API instead of Cloud API

Cloud API Commands:
  list                                      List all devices
  power <device> <sku> <on|off>             Turn device on/off
  brightness <device> <sku> <1-100>         Set brightness
  color <device> <sku> <r> <g> <b>          Set RGB color (0-255 each)
  temperature <device> <sku> <K>            Set color temp (2000-9000K)
  segment <device> <sku> <seg> <r> <g> <b>  Set segment color (seg: comma-separated)
  gradient <device> <sku>                   Apply rainbow gradient pattern
  scenes <device> <sku>                     List available dynamic scenes
  scene <device> <sku> <paramId> <id>       Apply a dynamic scene

LAN API Commands:
  discover                                  Discover devices on local network
  status <ip>                               Query device status
  power <ip> <on|off>                       Turn device on/off
  brightness <ip> <1-100>                   Set brightness
  color <ip> <r> <g> <b>                    Set RGB color (0-255 each)
  temperature <ip> <K>                      Set color temp (2000-9000K)

Cloud API Examples:
  uv run govee.py list
  uv run govee.py power "1A:74:CD:C2:EB:A4:08:21" "H606A" on
  uv run govee.py brightness "1A:74:CD:C2:EB:A4:08:21" "H606A" 75
  uv run govee.py color "1A:74:CD:C2:EB:A4:08:21" "H606A" 255 0 128
  uv run govee.py scenes "1A:74:CD:C2:EB:A4:08:21" "H606A"
  uv run govee.py scene "1A:74:CD:C2:EB:A4:08:21" "H606A" 4280 3853

LAN API Examples:
  uv run govee.py --lan discover
  uv run govee.py --lan power 192.168.1.23 on
  uv run govee.py --lan brightness 192.168.1.23 75
  uv run govee.py --lan color 192.168.1.23 255 0 128
  uv run govee.py --lan status 192.168.1.23

Note: LAN API requires devices to have LAN Control enabled in Govee app
      and bypasses Cloud API rate limits (10,000/day).
""")


def main() -> None:
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)

    # Check for LAN mode flag
    use_lan = False
    args_offset = 1
    if sys.argv[1] == "--lan":
        use_lan = True
        args_offset = 2
        if len(sys.argv) < 3:
            print_usage()
            sys.exit(1)

    cmd = sys.argv[args_offset].lower()

    # Handle LAN API commands
    if use_lan:
        match cmd:
            case "discover":
                client = GoveeLAN()
                devices = client.discover_devices()
                print(f"Found {len(devices)} device(s):\n")
                for dev in devices:
                    print(json.dumps(dev, indent=2))
            case "status" if len(sys.argv) == args_offset + 2:
                ip = sys.argv[args_offset + 1]
                client = GoveeLAN(device_ip=ip)
                result = client.get_status()
                print(json.dumps(result, indent=2))
            case "power" if len(sys.argv) == args_offset + 3:
                ip = sys.argv[args_offset + 1]
                state = sys.argv[args_offset + 2]
                client = GoveeLAN(device_ip=ip)
                if state.lower() == "on":
                    client.turn_on()
                    print("Device turned on")
                else:
                    client.turn_off()
                    print("Device turned off")
            case "brightness" if len(sys.argv) == args_offset + 3:
                ip = sys.argv[args_offset + 1]
                level = int(sys.argv[args_offset + 2])
                client = GoveeLAN(device_ip=ip)
                client.set_brightness(level)
                print(f"Brightness set to {level}")
            case "color" if len(sys.argv) == args_offset + 5:
                ip = sys.argv[args_offset + 1]
                r = int(sys.argv[args_offset + 2])
                g = int(sys.argv[args_offset + 3])
                b = int(sys.argv[args_offset + 4])
                client = GoveeLAN(device_ip=ip)
                client.set_color(r, g, b)
                print(f"Color set to RGB({r}, {g}, {b})")
            case "temperature" if len(sys.argv) == args_offset + 3:
                ip = sys.argv[args_offset + 1]
                kelvin = int(sys.argv[args_offset + 2])
                client = GoveeLAN(device_ip=ip)
                client.set_temperature(kelvin)
                print(f"Temperature set to {kelvin}K")
            case "help" | "-h" | "--help":
                print_usage()
            case _:
                print(f"Unknown LAN command or wrong arguments: {cmd}", file=sys.stderr)
                print_usage()
                sys.exit(1)
        return

    # Handle Cloud API commands
    match cmd:
        case "list":
            list_devices()
        case "power" if len(sys.argv) == 5:
            power(sys.argv[2], sys.argv[3], sys.argv[4])
        case "brightness" if len(sys.argv) == 5:
            brightness(sys.argv[2], sys.argv[3], int(sys.argv[4]))
        case "color" if len(sys.argv) == 7:
            color(sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]))
        case "temperature" if len(sys.argv) == 5:
            temperature(sys.argv[2], sys.argv[3], int(sys.argv[4]))
        case "segment" if len(sys.argv) == 8:
            segments = [int(s) for s in sys.argv[4].split(",")]
            segment_color(sys.argv[2], sys.argv[3], segments, int(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7]))
        case "gradient" if len(sys.argv) == 4:
            gradient_pattern(sys.argv[2], sys.argv[3])
        case "scenes" if len(sys.argv) == 4:
            list_scenes(sys.argv[2], sys.argv[3])
        case "scene" if len(sys.argv) == 6:
            apply_scene(sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5]))
        case "help" | "-h" | "--help":
            print_usage()
        case _:
            print(f"Unknown command or wrong arguments: {cmd}", file=sys.stderr)
            print_usage()
            sys.exit(1)


if __name__ == "__main__":
    main()
