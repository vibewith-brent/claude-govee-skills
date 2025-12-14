# Claude Govee Skills

Claude Code skill for controlling Govee smart lights via Cloud API and Local LAN control.

## Setup

### Cloud API Setup

#### 1. Get Govee API Key

1. Open the Govee Home App
2. Go to Profile → About Us → Apply for API Key
3. The key will be sent to your email

#### 2. Configure API Key

```bash
cp .env.example .env
# Edit .env and add your API key
```

### LAN API Setup

LAN control doesn't require an API key but needs configuration:

1. Open Govee Home App
2. Select your device
3. Enable "LAN Control" in device settings
4. Ensure device is on same network as control system

### 3. Install the Skill in Claude Code

Copy this skill folder to your Claude Code skills directory:

```bash
cp -r . ~/.claude/skills/govee-lights
```

Or symlink it:

```bash
ln -s "$(pwd)" ~/.claude/skills/govee-lights
```

## Usage with Claude Code

Once installed, you can ask Claude to control your Govee lights:

- "List my Govee devices"
- "Turn on my Hexagon lights"
- "Set brightness to 50%"
- "Change the color to purple"
- "Set color temperature to 4000K"

## Direct CLI Usage

### Cloud API (requires API key)

```bash
# List devices
uv run govee.py list

# Power control
uv run govee.py power <device_id> <sku> on|off

# Brightness (1-100)
uv run govee.py brightness <device_id> <sku> <value>

# RGB color (0-255 each)
uv run govee.py color <device_id> <sku> <r> <g> <b>

# Color temperature (2000-9000K)
uv run govee.py temperature <device_id> <sku> <kelvin>

# List available scenes
uv run govee.py scenes <device_id> <sku>

# Apply scene
uv run govee.py scene <device_id> <sku> <paramId> <id>
```

### LAN API (local control, no API key needed)

```bash
# Discover devices on local network
uv run govee.py --lan discover

# Query device status
uv run govee.py --lan status <device_ip>

# Power control
uv run govee.py --lan power <device_ip> on|off

# Brightness (1-100)
uv run govee.py --lan brightness <device_ip> <value>

# RGB color (0-255 each)
uv run govee.py --lan color <device_ip> <r> <g> <b>

# Color temperature (2000-9000K)
uv run govee.py --lan temperature <device_ip> <kelvin>
```

### Cloud vs LAN Comparison

| Feature | Cloud API | LAN API |
|---------|-----------|---------|
| API Key Required | Yes | No |
| Rate Limit | 10,000/day | None |
| Network | Internet | Local only |
| Scene Control | Yes (query/apply) | No |
| Segment Control | Yes | No |
| Status Query | Via capabilities | Direct |
| Speed | ~200-500ms | ~10-50ms |

## Supported Devices

Works with any Govee device that supports the Govee API, including:

- Glide Hexagon Light Panels Ultra
- Glide Wall Light
- LED Strip Lights
- Smart Bulbs
- And more

## API Reference

### Cloud API

- [Govee Developer Platform](https://developer.govee.com/)
- [API Getting Started](https://developer.govee.com/docs/getting-started)
- [Device Control Reference](https://developer.govee.com/reference/control-you-devices)

### LAN API

- [Official LAN API Documentation](https://app-h5.govee.com/user-manual/wlan-guide)
- [LAN API Community Guide](https://community.govee.com/posts/mastering-the-lan-api-series-lan-api-101/136755)
