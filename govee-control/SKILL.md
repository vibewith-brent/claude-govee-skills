---
name: govee-control
description: Control Govee smart lights locally via LAN API - turn on/off, adjust brightness, set RGB colors, change color temperature. Use when the user wants to control Govee device settings or change light properties.
---

# Govee LAN Control

Direct local control of Govee smart lights using the LAN API. No API key required - works over local network.

## Prerequisites

- Device IP address (use govee-discovery skill to find it)
- LAN Control enabled in Govee Home App

## Available Commands

### Power Control

```bash
# Turn on
uv run govee-control/scripts/govee_lan.py on <device_ip>

# Turn off
uv run govee-control/scripts/govee_lan.py off <device_ip>
```

### Brightness

Set brightness level (1-100):

```bash
uv run govee-control/scripts/govee_lan.py brightness <device_ip> <level>
```

Example:
```bash
uv run govee-control/scripts/govee_lan.py brightness 192.168.1.58 75
```

### RGB Color

Set color using RGB values (0-255 each):

```bash
uv run govee-control/scripts/govee_lan.py color <device_ip> <r> <g> <b>
```

Examples:
```bash
# Purple
uv run govee-control/scripts/govee_lan.py color 192.168.1.58 128 0 255

# Red
uv run govee-control/scripts/govee_lan.py color 192.168.1.58 255 0 0

# Cyan
uv run govee-control/scripts/govee_lan.py color 192.168.1.58 0 255 255
```

### Color Temperature

Set white color temperature in Kelvin (2000-9000):

```bash
uv run govee-control/scripts/govee_lan.py temperature <device_ip> <kelvin>
```

Examples:
```bash
# Warm white
uv run govee-control/scripts/govee_lan.py temperature 192.168.1.58 2700

# Cool white
uv run govee-control/scripts/govee_lan.py temperature 192.168.1.58 6500
```

### Device Status

Query current device state:

```bash
uv run govee-control/scripts/govee_lan.py status <device_ip>
```

Returns:
```json
{
  "msg": {
    "cmd": "devStatus",
    "data": {
      "onOff": 1,
      "brightness": 100,
      "color": {"r": 255, "g": 0, "b": 0},
      "colorTemInKelvin": 0
    }
  }
}
```

### Discovery

Discover all devices on network:

```bash
uv run govee-control/scripts/govee_lan.py discover
```

## Protocol Details

The LAN API uses UDP on ports:
- **4001**: Discovery (multicast)
- **4002**: Listen for responses
- **4003**: Control commands

Commands are sent as JSON over UDP with no encryption. Response time is typically 10-50ms.

## Common Workflows

### Find and control a device
```bash
# 1. Discover devices
uv run govee-control/scripts/govee_lan.py discover

# 2. Turn on device at found IP
uv run govee-control/scripts/govee_lan.py on 192.168.1.58

# 3. Set color
uv run govee-control/scripts/govee_lan.py color 192.168.1.58 255 0 128
```

### Check status before changing
```bash
# Query current state
uv run govee-control/scripts/govee_lan.py status 192.168.1.58

# Make changes based on current state
uv run govee-control/scripts/govee_lan.py brightness 192.168.1.58 50
```

## Limitations

- No scene/preset control (use Cloud API for scenes)
- No segment control for multi-segment devices
- Commands do not return confirmation (except status query)
- Network latency affects response time

## Supported Devices

Works with any Govee device that supports LAN Control, including:
- H606A (Glide Wall Panels)
- H6066 (Hexagon Light Panels)
- LED strip lights with WiFi
- Smart bulbs with WiFi
