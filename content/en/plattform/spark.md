---
title: "Spark"
description: "Zenoh Tunnel — network bridge between edge and cloud"
weight: 5
---

## The Spark

A spark leaps across — from the forge to the outside. **Spark** is the Zenoh
tunnel of the ForgeIEC platform: a network bridge that connects PLC
installations across site boundaries. Edge-to-cloud, machine-to-machine,
workshop-to-control-room.

---

## Zenoh Protocol

Spark is based on the Zenoh protocol — a modern pub/sub protocol for
distributed systems with minimal latency and automatic network discovery:

- **Zero-config discovery** — participants find each other automatically
  on the network
- **Adaptive transmission** — from local shared memory to WAN tunnel,
  transparently
- **Efficient** — minimal overhead, suitable for embedded systems and
  cloud infrastructure alike

---

## Use Cases

### Live Monitoring

Monitor process values from remote PLC installations in real time —
without VPN configuration, without port forwarding. Spark provides
the data tunnel.

### Variable Forcing

Force variables on remote controllers as if sitting right at the device.
For commissioning, remote maintenance, and diagnostics.

### Multi-Site Networking

Connect multiple ForgeIEC installations into a logical network. Each site
publishes and subscribes to variables — Spark forwards the data
transparently.

### Edge-to-Cloud

Stream PLC data to cloud platforms for long-term analysis, machine
learning, or central dashboards. Spark is the bridge between shopfloor
and IT.

---

## Platform Integration

Spark runs as an independent process alongside `anvild` and uses
Anvil Technology (Zero-Copy Shared Memory) for local data exchange.
Over the network, Spark communicates via Zenoh.

```
Site A                              Site B
+---------+    Zenoh Tunnel     +---------+
|  anvild |<--- Spark ----- Spark --->|  anvild |
+---------+    (Internet)       +---------+
```

---

## Technical Specifications

| Property | Value |
|----------|-------|
| **Protocol** | Zenoh |
| **Transport** | TCP, UDP, TLS, QUIC |
| **Discovery** | Multicast + Scouting |
| **Local IPC** | Anvil Technology (Shared Memory) |
| **Platforms** | x86_64, ARM64, ARMv7 (Linux) |

---

<div style="text-align:center; padding: 2rem;">

**Spark — The spark that connects sites.**

blacksmith@forgeiec.io

</div>
