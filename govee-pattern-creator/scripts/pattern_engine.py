# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Pattern engine for generating mathematical light patterns."""

import math
from dataclasses import dataclass
from typing import Callable


@dataclass
class PatternFrame:
    """Single frame of pattern output."""
    r: int  # 0-255
    g: int  # 0-255
    b: int  # 0-255
    brightness: int  # 1-100

    @classmethod
    def from_hsv(cls, h: float, s: float, v: float, brightness: int = 100) -> 'PatternFrame':
        """Create frame from HSV color space."""
        r, g, b = hsv_to_rgb(h, s, v)
        return cls(r, g, b, brightness)


def hsv_to_rgb(h: float, s: float, v: float) -> tuple[int, int, int]:
    """Convert HSV to RGB.

    Args:
        h: Hue (0-360)
        s: Saturation (0-1)
        v: Value (0-1)

    Returns:
        RGB tuple (0-255 each)
    """
    c = v * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = v - c

    if h < 60:
        r, g, b = c, x, 0
    elif h < 120:
        r, g, b = x, c, 0
    elif h < 180:
        r, g, b = 0, c, x
    elif h < 240:
        r, g, b = 0, x, c
    elif h < 300:
        r, g, b = x, 0, c
    else:
        r, g, b = c, 0, x

    return (
        int((r + m) * 255),
        int((g + m) * 255),
        int((b + m) * 255)
    )


# Pattern Functions

def fourier_pattern(t: float, params: dict) -> PatternFrame:
    """Fourier series pattern using harmonic frequencies."""
    harmonics = params.get('harmonics', 5)

    value = 0
    for n in range(1, harmonics + 1):
        amplitude = 1.0 / n
        frequency = n
        value += amplitude * math.sin(2 * math.pi * frequency * t / 10)

    # Normalize to 0-1
    value = (value + sum(1/n for n in range(1, harmonics + 1))) / (2 * sum(1/n for n in range(1, harmonics + 1)))

    hue = value * 360
    return PatternFrame.from_hsv(hue, 1.0, 1.0, 100)


def perlin_pattern(t: float, params: dict) -> PatternFrame:
    """Perlin noise-like smooth random pattern."""
    scale = params.get('scale', 0.05)

    # Simplified 1D Perlin noise
    x = t * scale
    x_floor = math.floor(x)
    x_frac = x - x_floor

    # Simple gradient function using sine
    def gradient(i: int) -> float:
        return math.sin(i * 12.9898 + 78.233) * 43758.5453

    g0 = gradient(x_floor)
    g1 = gradient(x_floor + 1)

    # Fade function for smooth interpolation
    fade = x_frac * x_frac * (3 - 2 * x_frac)

    noise = g0 + fade * (g1 - g0)

    # Map to color
    hue = ((noise + 1) * 180) % 360
    saturation = 0.8
    return PatternFrame.from_hsv(hue, saturation, 1.0, 100)


def lissajous_pattern(t: float, params: dict) -> PatternFrame:
    """Lissajous curve pattern."""
    freq_x = params.get('freq_x', 3)
    freq_y = params.get('freq_y', 2)

    x = math.sin(freq_x * t * 0.5)
    y = math.sin(freq_y * t * 0.5)

    # Map position to color
    hue = ((math.atan2(y, x) + math.pi) / (2 * math.pi)) * 360
    saturation = min(1.0, math.sqrt(x*x + y*y))

    return PatternFrame.from_hsv(hue, saturation, 1.0, 100)


def interference_pattern(t: float, params: dict) -> PatternFrame:
    """Wave interference pattern."""
    num_waves = params.get('waves', 3)

    total = 0
    for i in range(num_waves):
        frequency = 0.5 + i * 0.3
        phase = i * math.pi / num_waves
        amplitude = 1.0 / num_waves

        total += amplitude * math.sin(2 * math.pi * frequency * t + phase)

    # Normalize
    total = (total + 1) / 2

    brightness = int(50 + 50 * total)
    hue = (t * 30) % 360

    return PatternFrame.from_hsv(hue, 1.0, 1.0, brightness)


def mandelbrot_pattern(t: float, params: dict) -> PatternFrame:
    """Mandelbrot set zoom pattern."""
    zoom_speed = params.get('zoom_speed', 0.02)
    zoom = math.exp(-t * zoom_speed)

    # Interesting region of Mandelbrot set
    c = complex(-0.7, 0.27)
    c = c * zoom

    # Iterate
    z = 0
    iterations = 0
    max_iter = 50

    while abs(z) < 2 and iterations < max_iter:
        z = z*z + c
        iterations += 1

    # Map iterations to color
    if iterations == max_iter:
        return PatternFrame(0, 0, 50, 50)  # In set = dark blue

    hue = (iterations * 20 + t * 10) % 360
    value = min(1.0, iterations / max_iter * 1.5)

    return PatternFrame.from_hsv(hue, 1.0, value, 100)


def plasma_pattern(t: float, params: dict) -> PatternFrame:
    """Classic demoscene plasma effect."""
    x = t * 0.5
    y = t * 0.3

    plasma = (
        math.sin(x * 0.5) +
        math.sin(y * 0.7) +
        math.sin((x + y) * 0.3) +
        math.sin(math.sqrt(x*x + y*y) * 0.4)
    )

    # Normalize
    plasma = (plasma + 4) / 8

    hue = (plasma * 360 + t * 20) % 360

    return PatternFrame.from_hsv(hue, 1.0, 1.0, 100)


# Pattern registry
PATTERNS: dict[str, Callable[[float, dict], PatternFrame]] = {
    'fourier': fourier_pattern,
    'perlin': perlin_pattern,
    'lissajous': lissajous_pattern,
    'interference': interference_pattern,
    'mandelbrot': mandelbrot_pattern,
    'plasma': plasma_pattern,
}


def get_pattern(name: str) -> Callable[[float, dict], PatternFrame]:
    """Get pattern function by name."""
    if name not in PATTERNS:
        raise ValueError(f"Unknown pattern: {name}. Available: {', '.join(PATTERNS.keys())}")
    return PATTERNS[name]
