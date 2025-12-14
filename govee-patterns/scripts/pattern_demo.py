# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Cool color pattern demo for Govee H606A using LAN API."""

import sys
import time
import math
from govee_lan import GoveeLAN


def rainbow_wave(client: GoveeLAN, duration: float = 30.0, speed: float = 0.1) -> None:
    """Smooth rainbow wave animation."""
    print("Starting rainbow wave pattern...")
    start_time = time.time()
    hue = 0

    while time.time() - start_time < duration:
        # HSV to RGB conversion for smooth color transitions
        h = hue % 360
        s = 1.0
        v = 1.0

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

        r = int((r + m) * 255)
        g = int((g + m) * 255)
        b = int((b + m) * 255)

        client.set_color(r, g, b)
        hue += 2
        time.sleep(speed)

    print("Rainbow wave complete!")


def pulse_effect(client: GoveeLAN, r: int, g: int, b: int, duration: float = 20.0) -> None:
    """Pulsing brightness effect with specified color."""
    print(f"Starting pulse effect with RGB({r}, {g}, {b})...")
    client.set_color(r, g, b)
    start_time = time.time()
    step = 0

    while time.time() - start_time < duration:
        # Sine wave for smooth pulsing (1-100)
        brightness = int(50 + 49 * math.sin(step))
        client.set_brightness(brightness)
        step += 0.1
        time.sleep(0.05)

    client.set_brightness(100)
    print("Pulse effect complete!")


def strobe_effect(client: GoveeLAN, colors: list[tuple[int, int, int]], duration: float = 15.0, speed: float = 0.3) -> None:
    """Strobe between multiple colors."""
    print("Starting strobe effect...")
    start_time = time.time()
    i = 0

    while time.time() - start_time < duration:
        r, g, b = colors[i % len(colors)]
        client.set_color(r, g, b)
        i += 1
        time.sleep(speed)

    print("Strobe effect complete!")


def fire_effect(client: GoveeLAN, duration: float = 25.0) -> None:
    """Flickering fire effect."""
    print("Starting fire effect...")
    start_time = time.time()

    while time.time() - start_time < duration:
        # Random fire colors (orange to red)
        import random
        r = random.randint(200, 255)
        g = random.randint(40, 120)
        b = 0
        brightness = random.randint(60, 100)

        client.set_color(r, g, b)
        client.set_brightness(brightness)
        time.sleep(random.uniform(0.05, 0.15))

    client.set_brightness(100)
    print("Fire effect complete!")


def ocean_wave(client: GoveeLAN, duration: float = 30.0) -> None:
    """Smooth ocean wave effect (blue/cyan transitions)."""
    print("Starting ocean wave effect...")
    start_time = time.time()
    step = 0

    while time.time() - start_time < duration:
        # Oscillate between deep blue and cyan
        blue_component = int(200 + 55 * math.sin(step))
        green_component = int(100 + 100 * math.sin(step * 0.7))

        client.set_color(0, green_component, blue_component)
        step += 0.08
        time.sleep(0.1)

    print("Ocean wave complete!")


def disco_party(client: GoveeLAN, duration: float = 30.0) -> None:
    """Random color party mode."""
    print("Starting disco party mode...")
    import random
    start_time = time.time()

    while time.time() - start_time < duration:
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        brightness = random.randint(70, 100)

        client.set_color(r, g, b)
        client.set_brightness(brightness)
        time.sleep(random.uniform(0.15, 0.4))

    client.set_brightness(100)
    print("Disco party complete!")


def main() -> None:
    if len(sys.argv) < 3:
        print("""Usage: uv run pattern_demo.py <device_ip> <pattern> [duration]

Available patterns:
  rainbow     - Smooth rainbow wave (default: 30s)
  pulse       - Pulsing purple effect (default: 20s)
  strobe      - Multi-color strobe (default: 15s)
  fire        - Flickering fire effect (default: 25s)
  ocean       - Ocean wave blue/cyan (default: 30s)
  disco       - Random disco party (default: 30s)
  all         - Run all patterns sequentially

Examples:
  uv run pattern_demo.py 192.168.1.23 rainbow
  uv run pattern_demo.py 192.168.1.23 pulse 30
  uv run pattern_demo.py 192.168.1.23 all

Note: Make sure LAN Control is enabled in your Govee app!
""")
        sys.exit(1)

    device_ip = sys.argv[1]
    pattern = sys.argv[2].lower()
    duration = float(sys.argv[3]) if len(sys.argv) > 3 else None

    client = GoveeLAN(device_ip=device_ip)

    # Ensure device is on
    client.turn_on()
    time.sleep(0.5)

    try:
        match pattern:
            case "rainbow":
                rainbow_wave(client, duration or 30.0)
            case "pulse":
                pulse_effect(client, 138, 43, 226, duration or 20.0)  # Purple
            case "strobe":
                colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)]
                strobe_effect(client, colors, duration or 15.0)
            case "fire":
                fire_effect(client, duration or 25.0)
            case "ocean":
                ocean_wave(client, duration or 30.0)
            case "disco":
                disco_party(client, duration or 30.0)
            case "all":
                print("\n=== Running all patterns ===\n")
                rainbow_wave(client, 15.0)
                time.sleep(1)
                ocean_wave(client, 15.0)
                time.sleep(1)
                fire_effect(client, 15.0)
                time.sleep(1)
                pulse_effect(client, 138, 43, 226, 10.0)
                time.sleep(1)
                strobe_effect(client, [(255, 0, 0), (0, 255, 0), (0, 0, 255)], 10.0)
                time.sleep(1)
                disco_party(client, 15.0)
                print("\n=== All patterns complete! ===")
            case _:
                print(f"Unknown pattern: {pattern}", file=sys.stderr)
                sys.exit(1)

    except KeyboardInterrupt:
        print("\nPattern interrupted by user")
    finally:
        # Reset to white at 100% brightness
        client.set_color(255, 255, 255)
        client.set_brightness(100)
        print("Reset to white")


if __name__ == "__main__":
    main()
