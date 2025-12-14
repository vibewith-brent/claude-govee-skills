# Mathematical Pattern Reference

Advanced mathematics behind custom pattern generation.

## Pattern Engine API

All patterns are functions with this signature:

```python
def pattern_function(t: float, params: dict) -> PatternFrame:
    """
    Args:
        t: Current time in seconds (monotonically increasing)
        params: Dictionary of pattern parameters

    Returns:
        PatternFrame with r, g, b (0-255), brightness (1-100)
    """
    pass
```

## Mathematical Techniques

### 1. Fourier Series

**Theory**: Any periodic function can be represented as a sum of sine/cosine waves.

```python
def fourier_pattern(t: float, params: dict) -> PatternFrame:
    harmonics = params.get('harmonics', 5)

    # Sum multiple sine waves
    value = 0
    for n in range(1, harmonics + 1):
        amplitude = 1.0 / n  # Decreasing amplitude
        frequency = n  # Harmonic frequencies
        value += amplitude * math.sin(2 * math.pi * frequency * t / 10)

    # Normalize to 0-1
    value = (value + harmonics) / (2 * harmonics)

    # Map to hue
    hue = value * 360
    return PatternFrame.from_hsv(hue, 1.0, 1.0, 100)
```

**Key Concept**: More harmonics = more complex patterns. Amplitude decay prevents high frequencies from dominating.

### 2. Perlin Noise

**Theory**: Gradient noise function producing smooth, natural-looking randomness.

```python
def perlin_pattern(t: float, params: dict) -> PatternFrame:
    scale = params.get('scale', 0.05)

    # 1D Perlin noise (simplified)
    x = t * scale
    x_floor = math.floor(x)
    x_frac = x - x_floor

    # Gradient interpolation
    g0 = gradient(x_floor)
    g1 = gradient(x_floor + 1)

    # Smooth interpolation (fade function)
    fade = x_frac * x_frac * (3 - 2 * x_frac)

    noise = g0 + fade * (g1 - g0)

    # Map to color
    hue = (noise * 180 + 180) % 360
    return PatternFrame.from_hsv(hue, 0.8, 1.0, 100)
```

**Key Concept**: Perlin noise has controlled smoothness. Scale controls frequency of variation.

### 3. Lissajous Curves

**Theory**: Parametric curves defined by perpendicular harmonic oscillations.

```python
def lissajous_pattern(t: float, params: dict) -> PatternFrame:
    freq_x = params.get('freq_x', 3)
    freq_y = params.get('freq_y', 2)

    # Parametric equations
    x = math.sin(freq_x * t)
    y = math.sin(freq_y * t)

    # Map position to color
    # x, y are in [-1, 1]
    hue = ((math.atan2(y, x) + math.pi) / (2 * math.pi)) * 360
    saturation = min(1.0, math.sqrt(x*x + y*y))

    return PatternFrame.from_hsv(hue, saturation, 1.0, 100)
```

**Key Concept**: Frequency ratio determines pattern shape. Irrational ratios never repeat.

### 4. Wave Interference

**Theory**: Superposition principle - waves add linearly.

```python
def interference_pattern(t: float, params: dict) -> PatternFrame:
    num_waves = params.get('waves', 3)

    # Multiple waves with different frequencies and phases
    total = 0
    for i in range(num_waves):
        frequency = 0.5 + i * 0.3
        phase = i * math.pi / num_waves
        amplitude = 1.0 / num_waves

        total += amplitude * math.sin(2 * math.pi * frequency * t + phase)

    # Normalize
    total = (total + 1) / 2  # Map [-1,1] to [0,1]

    # Map to color with interference peaks = bright, nodes = dim
    brightness = int(50 + 50 * total)
    hue = (t * 30) % 360

    return PatternFrame.from_hsv(hue, 1.0, 1.0, brightness)
```

**Key Concept**: Constructive and destructive interference creates beating patterns.

### 5. Mandelbrot Set

**Theory**: Fractal defined by iteration z → z² + c

```python
def mandelbrot_pattern(t: float, params: dict) -> PatternFrame:
    zoom = math.exp(-t * params.get('zoom_speed', 0.02))

    # Point in complex plane
    c = complex(-0.7, 0.0)  # Interesting region
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
        return PatternFrame(0, 0, 0, 100)  # In set = black

    hue = (iterations * 20) % 360
    saturation = 1.0
    value = min(1.0, iterations / max_iter)

    return PatternFrame.from_hsv(hue, saturation, value, 100)
```

**Key Concept**: Iteration count at different points creates fractal boundaries.

### 6. Plasma Effect

**Theory**: Sum of multiple 2D sine waves projected to 1D time.

```python
def plasma_pattern(t: float, params: dict) -> PatternFrame:
    # Treat time as both x and y for 2D effect
    x = t * 0.5
    y = t * 0.3

    # Multiple sine waves at different scales
    plasma = (
        math.sin(x * 0.5) +
        math.sin(y * 0.7) +
        math.sin((x + y) * 0.3) +
        math.sin(math.sqrt(x*x + y*y) * 0.4)
    )

    # Normalize to [0, 1]
    plasma = (plasma + 4) / 8

    # Rainbow mapping
    hue = (plasma * 360 + t * 20) % 360

    return PatternFrame.from_hsv(hue, 1.0, 1.0, 100)
```

**Key Concept**: Multiple overlapping waves create organic-looking gradients.

## Color Space Conversions

### HSV to RGB

Used extensively for hue-based patterns:

```python
def hsv_to_rgb(h: float, s: float, v: float) -> tuple[int, int, int]:
    """
    h: 0-360 (hue)
    s: 0-1 (saturation)
    v: 0-1 (value)
    returns: (r, g, b) in 0-255
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
```

### Why HSV?

- **Hue** can be smoothly varied for rainbow effects
- **Saturation** controls color intensity vs whiteness
- **Value** controls brightness independently of color

RGB is harder to create smooth color transitions with.

## Easing Functions

Make patterns feel more natural with non-linear interpolation.

### Smooth Start/Stop (Sigmoid)

```python
def sigmoid(x: float) -> float:
    """Maps [0,1] to [0,1] with slow start and end"""
    return 1 / (1 + math.exp(-10 * (x - 0.5)))
```

### Ease In/Out (Cubic)

```python
def ease_in_out(x: float) -> float:
    """Cubic easing"""
    if x < 0.5:
        return 4 * x * x * x
    else:
        return 1 - pow(-2 * x + 2, 3) / 2
```

### Bounce

```python
def bounce(x: float) -> float:
    """Bouncing effect"""
    if x < 4/11:
        return (121 * x * x) / 16
    elif x < 8/11:
        return (363/40 * x * x) - (99/10 * x) + 17/5
    elif x < 9/10:
        return (4356/361 * x * x) - (35442/1805 * x) + 16061/1805
    else:
        return (54/5 * x * x) - (513/25 * x) + 268/25
```

## Combining Patterns

### Additive Blending

```python
def blend_add(p1: PatternFrame, p2: PatternFrame, ratio: float = 0.5):
    """Add two patterns"""
    return PatternFrame(
        min(255, int(p1.r * ratio + p2.r * ratio)),
        min(255, int(p1.g * ratio + p2.g * ratio)),
        min(255, int(p1.b * ratio + p2.b * ratio)),
        min(100, int((p1.brightness + p2.brightness) / 2))
    )
```

### Multiplicative Blending

```python
def blend_multiply(p1: PatternFrame, p2: PatternFrame):
    """Multiply two patterns (darkening)"""
    return PatternFrame(
        int((p1.r / 255) * (p2.r / 255) * 255),
        int((p1.g / 255) * (p2.g / 255) * 255),
        int((p1.b / 255) * (p2.b / 255) * 255),
        min(100, int((p1.brightness + p2.brightness) / 2))
    )
```

## Performance Optimization

### Pre-computation

For expensive functions, compute lookup tables:

```python
# Pre-compute sine table
SINE_TABLE = [math.sin(i * math.pi / 180) for i in range(360)]

def fast_sin(degrees: float) -> float:
    return SINE_TABLE[int(degrees) % 360]
```

### Reduce Precision

Not all bits matter:

```python
# Round to reduce floating point operations
t_rounded = round(t, 2)
```

### Avoid Re-computation

Cache repeated calculations:

```python
# Bad
for i in range(10):
    x = expensive_function(t) * i

# Good
base = expensive_function(t)
for i in range(10):
    x = base * i
```

## Pattern Design Tips

1. **Start simple**: Test with basic sine waves before adding complexity
2. **Use parameters**: Make patterns configurable for experimentation
3. **Normalize carefully**: Ensure RGB values stay in 0-255 range
4. **Test edge cases**: What happens at t=0? At very large t?
5. **Consider brightness**: Some colors appear darker than others
6. **Phase relationships**: Small phase differences create interesting beats
7. **Non-repeating**: Irrational frequency ratios create endless variation

## Further Reading

- **Fourier Analysis**: Any signal processing textbook
- **Perlin Noise**: Ken Perlin's original paper (1985)
- **Fractals**: "The Fractal Geometry of Nature" by Mandelbrot
- **Color Theory**: "Color Science" by Wyszecki and Stiles
- **Demoscene**: iq/rgba's shader tutorials at https://iquilezles.org/
