# Pattern Technical Reference

This document explains how each pre-built pattern works.

## Rainbow Wave

**Algorithm**: HSV to RGB conversion with incrementing hue

```python
hue = (hue + 2) % 360
# Convert HSV(hue, 1.0, 1.0) to RGB
# Update every 100ms
```

**Effect**: Smooth transition through full color spectrum
**Speed**: Completes full cycle every ~18 seconds

## Ocean Wave

**Algorithm**: Dual sine waves for blue and green channels

```python
blue = 200 + 55 * sin(step)
green = 100 + 100 * sin(step * 0.7)
# Red channel fixed at 0
```

**Effect**: Oscillates between deep blue and cyan
**Frequencies**: Different sine wave speeds create complex motion

## Fire Effect

**Algorithm**: Random sampling from fire color ranges

```python
r = random(200, 255)  # High red
g = random(40, 120)   # Variable orange
b = 0                 # No blue
brightness = random(60, 100)
```

**Effect**: Chaotic flickering simulating flames
**Update**: 50-150ms random intervals

## Pulse Effect

**Algorithm**: Sine wave brightness modulation

```python
brightness = 50 + 49 * sin(step)
step += 0.1
# Color fixed at purple RGB(138, 43, 226)
```

**Effect**: Smooth breathing at ~1.6 second period
**Range**: 1-99% brightness

## Strobe Effect

**Algorithm**: Color array cycling with fixed intervals

```python
colors = [(255,0,0), (0,255,0), (0,0,255), (255,255,0), (255,0,255)]
current = colors[i % len(colors)]
# Cycle every 300ms
```

**Effect**: Sharp color transitions
**Speed**: ~3.3 colors per second

## Disco Party

**Algorithm**: Random RGB and brightness

```python
r, g, b = random(0, 255) for each channel
brightness = random(70, 100)
# Update every 150-400ms
```

**Effect**: Chaotic party lighting
**Variation**: Variable timing prevents predictable patterns

## Mathematical Functions Used

### HSV to RGB Conversion
Used for smooth color transitions where hue varies but saturation and value stay constant.

### Sine Waves
`sin(x)` produces smooth oscillations. Used for:
- Brightness pulsing
- Color channel modulation
- Wave-like transitions

### Random Sampling
Uniform random distribution for:
- Fire flicker simulation
- Disco randomness
- Variable timing

## Performance Characteristics

| Pattern | Update Rate | CPU Usage | Network Load |
|---------|-------------|-----------|--------------|
| Rainbow | 10 Hz | Low | Low |
| Ocean | 10 Hz | Low | Low |
| Fire | 6-20 Hz | Medium | Variable |
| Pulse | 20 Hz | Low | Low |
| Strobe | 3 Hz | Low | Low |
| Disco | 2.5-6 Hz | Medium | Variable |

Update rates are approximate and affected by network latency.
