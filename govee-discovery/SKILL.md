---
name: govee-discovery
description: Discover Govee smart light devices on the local network via multicast or network scanning. Use when the user needs to find Govee devices, locate device IPs, or determine which Govee lights are available on the network.
---

# Govee Device Discovery

Discover Govee smart light devices on your local network using multicast discovery or network scanning.

## Prerequisites

- Govee devices must have LAN Control enabled (Settings in Govee Home App)
- Devices must be on the same network as the control system

## Methods

### Multicast Discovery (Recommended)

Fast discovery using UDP multicast. Finds all Govee devices that respond to broadcast scan messages.

```bash
uv run govee-discovery/scripts/discover.py
```

Returns device information including:
- IP address
- Device MAC address
- Model (SKU) like "H606A"
- Firmware versions

### Network Scanning

Scans IP range to find Govee devices by attempting status queries.

```bash
# Default 192.168.1.0/24
uv run govee-discovery/scripts/find_ip.py

# Custom subnet
uv run govee-discovery/scripts/find_ip.py 192.168.0
```

Useful when multicast discovery fails or you need to scan specific network ranges.

## Workflow

1. Run discovery to find available devices
2. Note the device IP address from the results
3. Use the IP with govee-control or govee-patterns skills

## Example Output

```json
{
  "ip": "192.168.1.58",
  "device": "1A:74:CD:C2:EB:A4:08:21",
  "sku": "H606A",
  "bleVersionHard": "3.04.01",
  "bleVersionSoft": "1.00.16",
  "wifiVersionHard": "1.04.01",
  "wifiVersionSoft": "1.03.01"
}
```

## Troubleshooting

If no devices found:
1. Verify LAN Control is enabled in Govee Home App
2. Check device is on same network/subnet
3. Try network scanning with correct subnet
4. Check firewall allows UDP multicast (ports 4001-4003)
