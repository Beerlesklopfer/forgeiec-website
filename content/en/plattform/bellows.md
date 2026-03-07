---
title: "Bellows"
description: "OPC UA Gateway — standardized machine communication for industry"
weight: 3
---

## The Bellows — *In Development*

The bellows keep the fire alive and direct air where it is needed.
**Bellows** is the OPC UA gateway of the ForgeIEC platform — the
standardized interface between workshop and control room, between
machine and supervisory system.

> Bellows is in active development. The features described here
> represent the planned scope.

---

## OPC UA — The Industry Standard

OPC Unified Architecture is the vendor-independent standard for
machine-to-machine communication in industrial automation. Bellows
implements this standard as an integral part of the ForgeIEC platform.

---

## Planned Features

### OPC UA Server

- Expose all PLC variables as OPC UA nodes
- Automatic mapping of IEC data types to the OPC UA information model
- Browse, Read, Write, and Subscribe services
- Security through certificate authentication

### OPC UA Client

- Access external OPC UA servers from the PLC program
- Read and write remote variables
- Event subscriptions for state-based control

### Information Model Mapping

- Automatic generation of the address space from the project configuration
- Support for user-defined information models
- Companion specification compatibility (PackML, Euromap, etc.)

---

## Platform Integration

Bellows will run as an independent bridge process — monitored and managed
by `anvild`. Communication with the PLC core uses Anvil Technology
(Zero-Copy Shared Memory), just like the fieldbus bridges.

```
Forge Studio  --->  anvild  --->  Bellows (OPC UA)  --->  SCADA/MES/Cloud
                      |
                    Anvil SHM
```

---

<div style="text-align:center; padding: 2rem;">

**Bellows — Standardized communication for connected manufacturing.**

blacksmith@forgeiec.io

</div>
