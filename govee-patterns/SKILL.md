---
name: govee-patterns
description: Run pre-built animated light patterns on Govee devices including rainbow waves, fire effects, ocean waves, disco party, strobes, and pulse effects. Use when the user wants to run animated patterns or special lighting effects on their Govee lights.
---

# Govee Light Patterns

Pre-built animated patterns for Govee smart lights. Each pattern uses smooth transitions and mathematical functions to create dynamic lighting effects.

## Prerequisites

- Device IP address (use govee-discovery to find it)
- LAN Control enabled in Govee Home App

## Available Patterns

### Rainbow Wave
Smooth color spectrum transitions through the full rainbow.

```bash
uv run govee-patterns/scripts/pattern_demo.py <device_ip> rainbow [duration]
```

Default: 30 seconds

### Ocean Wave
Calming blue and cyan wave transitions simulating ocean movement.

```bash
uv run govee-patterns/scripts/pattern_demo.py <device_ip> ocean [duration]
```

Default: 30 seconds

### Fire Effect
Flickering orange and red flames with random intensity variations.

```bash
uv run govee-patterns/scripts/pattern_demo.py <device_ip> fire [duration]
```

Default: 25 seconds

### Pulse Effect
Smooth breathing brightness effect with purple color.

```bash
uv run govee-patterns/scripts/pattern_demo.py <device_ip> pulse [duration]
```

Default: 20 seconds

### Strobe Effect
Fast multi-color flashing between red, green, blue, yellow, and magenta.

```bash
uv run govee-patterns/scripts/pattern_demo.py <device_ip> strobe [duration]
```

Default: 15 seconds

### Disco Party
Random colors with varying brightness for party atmosphere.

```bash
uv run govee-patterns/scripts/pattern_demo.py <device_ip> disco [duration]
```

Default: 30 seconds

### All Patterns
Run all patterns sequentially for a full demo.

```bash
uv run govee-patterns/scripts/pattern_demo.py <device_ip> all
```

Runs each pattern for shorter duration in sequence.

## Pattern Details

See [PATTERNS.md](PATTERNS.md) for technical details on how each pattern works.

## Examples

```bash
# Run rainbow for 60 seconds
uv run govee-patterns/scripts/pattern_demo.py 192.168.1.58 rainbow 60

# Quick fire effect
uv run govee-patterns/scripts/pattern_demo.py 192.168.1.58 fire 10

# Demo all patterns
uv run govee-patterns/scripts/pattern_demo.py 192.168.1.58 all
```

## Interrupting Patterns

Press Ctrl+C to stop a running pattern. The lights will reset to white at 100% brightness.

## Performance Notes

- Update rate: ~10-20 FPS depending on pattern
- Network latency affects smoothness (LAN is faster than Cloud API)
- Patterns automatically turn device on if needed

## Creating Custom Patterns

For custom pattern creation, see the **govee-pattern-creator** skill which provides tools for generating new patterns with complex mathematical functions.
