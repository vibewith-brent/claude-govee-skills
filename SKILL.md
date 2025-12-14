---
name: govee-lights
description: Control Govee smart lights via the Govee API. Use this skill when the user wants to turn lights on/off, change brightness, set colors, adjust color temperature, or list their Govee devices.
---

# Govee Lights Control

Control Govee smart lights including Glide Hexagon Light Panels Ultra and other Govee devices.

## Prerequisites

- Govee API key (obtain from Govee Home App → Profile → About Us → Apply for API Key)
- API key stored in environment variable `GOVEE_API_KEY` or in `.env` file

## Available Operations

### List Devices
Retrieve all Govee devices and their capabilities:
```bash
uv run govee.py list
```

### Power Control
Turn device on or off:
```bash
uv run govee.py power <device_id> <sku> on
uv run govee.py power <device_id> <sku> off
```

### Brightness
Set brightness (1-100):
```bash
uv run govee.py brightness <device_id> <sku> <value>
```

### Color (RGB)
Set color using RGB values (0-255 each):
```bash
uv run govee.py color <device_id> <sku> <red> <green> <blue>
```

### Color Temperature
Set color temperature in Kelvin (2000-9000):
```bash
uv run govee.py temperature <device_id> <sku> <kelvin>
```

## Workflow

1. First, run `list` to discover devices and get their `device` ID and `sku`
2. Use the device ID and SKU for subsequent control commands
3. The script outputs JSON responses for verification

## API Details

- **Base URL:** `https://openapi.api.govee.com`
- **Rate Limit:** 10,000 requests/day per account
- **Auth Header:** `Govee-API-Key`

## Capability Reference

| Capability | Instance | Value Type |
|------------|----------|------------|
| on_off | powerSwitch | 0 (off) or 1 (on) |
| range | brightness | 1-100 |
| color_setting | colorRgb | 0-16777215 (RGB packed) |
| color_setting | colorTemperatureK | 2000-9000 |
| segment_color_setting | segmentedColorRgb | Per-segment control |
| mode | presetScene | Scene enum values |

## Error Handling

- **401:** Invalid API key
- **429:** Rate limit exceeded
- **400:** Invalid parameters or unsupported capability

## Example Session

```
# List devices to find your Hexagon Panels
uv run govee.py list

# Turn on the lights
uv run govee.py power "AA:BB:CC:DD:EE:FF" "H6066" on

# Set to 50% brightness
uv run govee.py brightness "AA:BB:CC:DD:EE:FF" "H6066" 50

# Set purple color (R=128, G=0, B=255)
uv run govee.py color "AA:BB:CC:DD:EE:FF" "H6066" 128 0 255

# Set warm white (3000K)
uv run govee.py temperature "AA:BB:CC:DD:EE:FF" "H6066" 3000
```
