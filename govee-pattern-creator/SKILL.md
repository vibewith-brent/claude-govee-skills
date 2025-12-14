---
name: govee-pattern-creator
description: Generate custom animated light patterns using advanced mathematical functions including Fourier transforms, Perlin noise, parametric curves, and wave superposition. Use when the user wants to create new custom patterns, design unique lighting effects, or experiment with mathematical pattern generation.
---

# Govee Pattern Creator

Create custom animated light patterns using advanced mathematical functions and algorithms. Generate unique lighting effects beyond pre-built patterns.

## Prerequisites

- Device IP address
- LAN Control enabled
- Basic understanding of desired effect (optional)

## Quick Start

Generate a pattern using the pattern engine:

```bash
uv run govee-pattern-creator/scripts/generate_pattern.py <device_ip> <pattern_type> [duration] [params...]
```

## Available Pattern Types

### Fourier Series Patterns

Create patterns by combining multiple sine waves at different frequencies.

```bash
uv run govee-pattern-creator/scripts/generate_pattern.py <ip> fourier [duration] [harmonics]
```

Parameters:
- `harmonics`: Number of frequency components (default: 5)

**Examples:**
```bash
# Basic fourier pattern
uv run govee-pattern-creator/scripts/generate_pattern.py 192.168.1.58 fourier 60 3

# Complex harmonics
uv run govee-pattern-creator/scripts/generate_pattern.py 192.168.1.58 fourier 120 8
```

**Effect**: Creates complex periodic patterns by superimposing multiple sine waves. Higher harmonic counts produce more intricate color transitions.

### Perlin Noise Patterns

Smooth random patterns using Perlin noise for organic, natural-looking transitions.

```bash
uv run govee-pattern-creator/scripts/generate_pattern.py <ip> perlin [duration] [scale]
```

Parameters:
- `scale`: Noise scale factor (default: 0.05)

**Examples:**
```bash
# Slow organic movement
uv run govee-pattern-creator/scripts/generate_pattern.py 192.168.1.58 perlin 90 0.02

# Faster turbulence
uv run govee-pattern-creator/scripts/generate_pattern.py 192.168.1.58 perlin 60 0.1
```

**Effect**: Smooth, natural-looking color flows. Lower scale = slower, more gradual changes.

### Lissajous Curves

Parametric curves creating hypnotic geometric color patterns.

```bash
uv run govee-pattern-creator/scripts/generate_pattern.py <ip> lissajous [duration] [freq_x] [freq_y]
```

Parameters:
- `freq_x`: X-axis frequency (default: 3)
- `freq_y`: Y-axis frequency (default: 2)

**Examples:**
```bash
# Classic 3:2 ratio
uv run govee-pattern-creator/scripts/generate_pattern.py 192.168.1.58 lissajous 60 3 2

# Complex 5:4 ratio
uv run govee-pattern-creator/scripts/generate_pattern.py 192.168.1.58 lissajous 90 5 4
```

**Effect**: Creates repeating geometric patterns. Different frequency ratios produce different shapes.

### Wave Interference

Simulate wave interference patterns with multiple wave sources.

```bash
uv run govee-pattern-creator/scripts/generate_pattern.py <ip> interference [duration] [waves]
```

Parameters:
- `waves`: Number of interfering waves (default: 3)

**Examples:**
```bash
# Two-wave interference
uv run govee-pattern-creator/scripts/generate_pattern.py 192.168.1.58 interference 60 2

# Complex multi-wave
uv run govee-pattern-creator/scripts/generate_pattern.py 192.168.1.58 interference 120 5
```

**Effect**: Beating patterns from wave superposition. Creates pulsing color effects.

### Mandelbrot Zoom

Animated journey through the Mandelbrot fractal set.

```bash
uv run govee-pattern-creator/scripts/generate_pattern.py <ip> mandelbrot [duration] [zoom_speed]
```

Parameters:
- `zoom_speed`: Zoom rate (default: 0.02)

**Example:**
```bash
uv run govee-pattern-creator/scripts/generate_pattern.py 192.168.1.58 mandelbrot 120 0.01
```

**Effect**: Continuously zooming fractal colors. Mesmerizing mathematical beauty.

### Plasma Effect

Classic demoscene plasma effect using combined sine waves.

```bash
uv run govee-pattern-creator/scripts/generate_pattern.py <ip> plasma [duration]
```

**Example:**
```bash
uv run govee-pattern-creator/scripts/generate_pattern.py 192.168.1.58 plasma 90
```

**Effect**: Smooth, flowing color gradients reminiscent of 90s demos.

## Advanced Features

### Custom Pattern Scripts

Create your own pattern by defining a generator function. See [MATH_PATTERNS.md](MATH_PATTERNS.md) for the API.

```python
from pattern_engine import PatternEngine, PatternFrame

def my_pattern(t: float, params: dict) -> PatternFrame:
    """
    t: time in seconds
    params: user parameters
    returns: PatternFrame with r, g, b, brightness
    """
    hue = (t * 30) % 360  # Your math here
    return PatternFrame.from_hsv(hue, 1.0, 1.0, 100)
```

### Combining Patterns

Layer multiple mathematical functions:

```bash
# See MATH_PATTERNS.md for combination techniques
```

## Mathematical Functions Reference

For detailed mathematical explanations of each pattern type, see [MATH_PATTERNS.md](MATH_PATTERNS.md).

## Performance Notes

- Complex patterns (high harmonics, dense fractals) use more CPU
- Update rate: 10-30 FPS depending on complexity
- Network latency affects smoothness
- Lower duration values for testing new patterns

## Pattern Ideas

**Sunrise/Sunset**: Use sigmoid functions for smooth warm-to-cool transitions
**Northern Lights**: Perlin noise with green/blue/purple palette
**Heartbeat**: Non-linear pulse with exponential decay
**Breathing**: Slow sine wave with extended holds at peaks
**Rave**: High-frequency fourier with random phase shifts
**Meditation**: Very slow perlin noise with narrow color palette

## Troubleshooting

**Pattern too fast/slow**: Adjust time scale in pattern function
**Colors too intense**: Reduce saturation or add brightness limits
**Choppy animation**: Reduce computational complexity or update rate
**Device not responding**: Check LAN Control enabled and IP is correct
