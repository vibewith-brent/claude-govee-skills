# Claude Govee Skills

Agent Skills for controlling Govee smart lights via LAN API. Provides modular capabilities for device discovery, control, pre-built patterns, and custom pattern generation using advanced mathematics.

## Skills Overview

This repository contains four specialized skills:

### 1. **govee-discovery**
Find Govee devices on your local network via multicast or network scanning.

```bash
uv run govee-discovery/scripts/discover.py
uv run govee-discovery/scripts/find_ip.py [subnet]
```

### 2. **govee-control**
Direct LAN control of Govee lights - power, brightness, color, temperature.

```bash
uv run govee-control/scripts/govee_lan.py <command> <device_ip> [args]
```

### 3. **govee-patterns**
Pre-built animated patterns: rainbow, fire, ocean, disco, strobe, pulse.

```bash
uv run govee-patterns/scripts/pattern_demo.py <device_ip> <pattern> [duration]
```

### 4. **govee-pattern-creator**
Generate custom patterns using advanced mathematics: Fourier series, Perlin noise, Lissajous curves, fractals, plasma effects.

```bash
uv run govee-pattern-creator/scripts/generate_pattern.py <device_ip> <pattern_type> [duration] [params]
```

## Quick Start

### Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) package manager
- Govee device with LAN Control enabled (Govee Home App → Settings)
- Device on same network

### Installation

```bash
# Clone repository
git clone https://github.com/vibewith-brent/claude-govee-skills.git
cd claude-govee-skills

# Initialize uv project
uv sync
```

### Basic Usage

```bash
# 1. Find your device
uv run govee-discovery/scripts/discover.py

# 2. Control the lights
uv run govee-control/scripts/govee_lan.py on 192.168.1.58
uv run govee-control/scripts/govee_lan.py color 192.168.1.58 255 0 128

# 3. Run a pattern
uv run govee-patterns/scripts/pattern_demo.py 192.168.1.58 rainbow 60

# 4. Create custom pattern
uv run govee-pattern-creator/scripts/generate_pattern.py 192.168.1.58 fourier 120 8
```

## Using as Claude Agent Skills

### In Claude Code

Install skills by symlinking or copying to your skills directory:

```bash
# Link all skills
ln -s "$(pwd)/govee-discovery" ~/.claude/skills/
ln -s "$(pwd)/govee-control" ~/.claude/skills/
ln -s "$(pwd)/govee-patterns" ~/.claude/skills/
ln -s "$(pwd)/govee-pattern-creator" ~/.claude/skills/

# Or copy them
cp -r govee-* ~/.claude/skills/
```

Then ask Claude:
- "Find my Govee devices"
- "Turn on the lights and set them to purple"
- "Run the rainbow pattern for 2 minutes"
- "Create a Fourier pattern with 8 harmonics"

### In Claude API

Upload skills via the Skills API:

```python
import anthropic

client = anthropic.Anthropic()

# Upload skill (example for govee-discovery)
with open("govee-discovery/SKILL.md", "rb") as f:
    skill = client.skills.create(
        file=f,
        name="govee-discovery"
    )
```

See [Claude API Skills documentation](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills) for details.

### In Claude.ai

Zip each skill directory and upload via Settings → Features → Skills.

```bash
zip -r govee-discovery.zip govee-discovery/
zip -r govee-control.zip govee-control/
zip -r govee-patterns.zip govee-patterns/
zip -r govee-pattern-creator.zip govee-pattern-creator/
```

## Skill Documentation

Each skill contains detailed documentation:

- **SKILL.md**: Main skill instructions and usage
- **Additional guides**: Pattern catalogs, mathematical references, troubleshooting

### Skill-Specific Docs

- `govee-patterns/PATTERNS.md`: Technical details on pre-built patterns
- `govee-pattern-creator/MATH_PATTERNS.md`: Mathematical theory and custom pattern API

## Architecture

```
claude-govee-skills/
├── govee-discovery/
│   ├── SKILL.md                    # Discovery skill instructions
│   └── scripts/
│       ├── discover.py             # Multicast discovery
│       └── find_ip.py              # Network scanner
├── govee-control/
│   ├── SKILL.md                    # Control skill instructions
│   └── scripts/
│       └── govee_lan.py            # LAN API client
├── govee-patterns/
│   ├── SKILL.md                    # Patterns skill instructions
│   ├── PATTERNS.md                 # Pattern catalog
│   └── scripts/
│       └── pattern_demo.py         # Pre-built patterns
└── govee-pattern-creator/
    ├── SKILL.md                    # Pattern creator instructions
    ├── MATH_PATTERNS.md            # Mathematical reference
    └── scripts/
        ├── pattern_engine.py       # Pattern generation engine
        └── generate_pattern.py     # Pattern runner
```

## Advanced Pattern Creation

The pattern creator supports:

- **Fourier Series**: Harmonic wave superposition
- **Perlin Noise**: Smooth natural transitions
- **Lissajous Curves**: Parametric geometric patterns
- **Wave Interference**: Multi-wave beating patterns
- **Mandelbrot Fractals**: Fractal zoom animations
- **Plasma Effects**: Classic demoscene gradients

See `govee-pattern-creator/MATH_PATTERNS.md` for mathematical details and custom pattern API.

## LAN API Protocol

The Govee LAN API uses UDP:
- **Port 4001**: Multicast discovery
- **Port 4002**: Response listening
- **Port 4003**: Control commands

Commands are JSON over UDP with typical 10-50ms latency. No API key required.

## Supported Devices

Works with Govee devices supporting LAN Control:
- H606A (Glide Wall Panels)
- H6066 (Hexagon Light Panels)
- LED strip lights with WiFi
- Smart bulbs with WiFi

Enable LAN Control in Govee Home App device settings.

## Limitations

- **No scenes**: Use Cloud API for preset scenes
- **No segments**: Multi-segment control not supported
- **Local only**: Requires same network as device
- **UDP**: Fire-and-forget commands (no confirmation except status query)

## Contributing

Contributions welcome! Ideas:
- Additional pattern algorithms
- Cloud API integration
- Multi-device coordination
- Music synchronization
- New mathematical effect

## License

MIT License - see [LICENSE](LICENSE)

## References

- [Govee LAN API Documentation](https://app-h5.govee.com/user-manual/wlan-guide)
- [Govee Developer Platform](https://developer.govee.com/)
- [Claude Agent Skills Guide](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills)
- [Mathematical Pattern Theory](govee-pattern-creator/MATH_PATTERNS.md)

## Related Projects

- `govee.py`: Cloud API client (included for future use)
- Other Govee control libraries: [awesome-govee](https://github.com/topics/govee)
