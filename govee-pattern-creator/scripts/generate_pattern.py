# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Generate and run custom mathematical patterns on Govee devices."""

import sys
import time
import os

# Add govee-control to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../govee-control/scripts'))

from govee_lan import GoveeLAN
from pattern_engine import get_pattern, PATTERNS


def run_pattern(device_ip: str, pattern_name: str, duration: float, params: dict) -> None:
    """Run a mathematical pattern on the device."""
    client = GoveeLAN(device_ip=device_ip)
    pattern_func = get_pattern(pattern_name)

    # Turn device on
    client.turn_on()
    time.sleep(0.5)

    print(f"Running {pattern_name} pattern for {duration}s with params {params}")
    print("Press Ctrl+C to stop")

    start_time = time.time()
    frame_count = 0

    try:
        while time.time() - start_time < duration:
            t = time.time() - start_time

            # Generate frame
            frame = pattern_func(t, params)

            # Send to device
            client.set_color(frame.r, frame.g, frame.b)
            client.set_brightness(frame.brightness)

            frame_count += 1
            time.sleep(0.05)  # ~20 FPS

    except KeyboardInterrupt:
        print(f"\nPattern interrupted after {time.time() - start_time:.1f}s")
    finally:
        # Reset to white
        client.set_color(255, 255, 255)
        client.set_brightness(100)
        fps = frame_count / (time.time() - start_time)
        print(f"Pattern complete! Rendered {frame_count} frames ({fps:.1f} FPS)")


def main() -> None:
    if len(sys.argv) < 3:
        print("""Usage: uv run generate_pattern.py <device_ip> <pattern> [duration] [params...]

Available patterns:
  fourier [harmonics=5]        - Fourier series with harmonic waves
  perlin [scale=0.05]          - Smooth Perlin noise
  lissajous [fx=3] [fy=2]      - Lissajous parametric curves
  interference [waves=3]        - Wave interference patterns
  mandelbrot [zoom=0.02]       - Mandelbrot fractal zoom
  plasma                       - Classic plasma effect

Examples:
  uv run generate_pattern.py 192.168.1.58 fourier 60 8
  uv run generate_pattern.py 192.168.1.58 perlin 90 0.02
  uv run generate_pattern.py 192.168.1.58 lissajous 60 5 4
  uv run generate_pattern.py 192.168.1.58 plasma 120
""")
        sys.exit(1)

    device_ip = sys.argv[1]
    pattern_name = sys.argv[2].lower()

    if pattern_name not in PATTERNS:
        print(f"Error: Unknown pattern '{pattern_name}'")
        print(f"Available: {', '.join(PATTERNS.keys())}")
        sys.exit(1)

    # Default duration
    duration = float(sys.argv[3]) if len(sys.argv) > 3 else 60.0

    # Parse pattern-specific parameters
    params = {}

    if pattern_name == 'fourier':
        params['harmonics'] = int(sys.argv[4]) if len(sys.argv) > 4 else 5
    elif pattern_name == 'perlin':
        params['scale'] = float(sys.argv[4]) if len(sys.argv) > 4 else 0.05
    elif pattern_name == 'lissajous':
        params['freq_x'] = int(sys.argv[4]) if len(sys.argv) > 4 else 3
        params['freq_y'] = int(sys.argv[5]) if len(sys.argv) > 5 else 2
    elif pattern_name == 'interference':
        params['waves'] = int(sys.argv[4]) if len(sys.argv) > 4 else 3
    elif pattern_name == 'mandelbrot':
        params['zoom_speed'] = float(sys.argv[4]) if len(sys.argv) > 4 else 0.02

    run_pattern(device_ip, pattern_name, duration, params)


if __name__ == "__main__":
    main()
