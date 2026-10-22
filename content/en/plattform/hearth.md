---
title: "Hearth"
description: "SCADA/HMI — process visualization and plant operation in the browser"
weight: 4
---

## The Hearth — *Preview*

The hearth is the center of the forge — here you see the glow of the metal,
here you feel the heat. **Hearth** is the SCADA/HMI solution of the ForgeIEC
platform: process visualization and plant operation, accessible anywhere
through the browser.

{{< callout type="note" title="Preview" >}}
Hearth is available as a preview: the Hearth server (package
`forgeiec-hearth-server`) reads the process data directly from the
Anvil bus and serves the operator interface in the browser. The list
below describes the intended scope — not all of it is implemented.
{{< /callout >}}

---

## Intended Scope

### Process Visualization

- Web-based display of plant states and process values
- Responsive dashboards for desktop, tablet, and mobile devices
- Real-time updates without manual reloading
- Freely configurable process screens with symbols and animations

### Alarm Management

- Central alarm management with acknowledgment and escalation
- Alarm history with timestamps and user logs
- Prioritization and filtering by plant areas
- Push notifications for critical states

### Trend Recording

- Long-term recording of process values
- Configurable sampling rates and storage duration
- Trend charts with zoom, pan, and cursor queries
- Export to CSV and common formats

### Operator Interface

- Input forms for setpoints and recipe parameters
- User management with permission levels
- Operator log (audit trail) for regulated environments

---

## Platform Integration

Hearth reads the process data directly from the Anvil bus (iceoryx2,
without copying) — the same path the runtime uses internally.
Instructions to the plant go to the Anvil server (anvild). Access is
through the web browser — no installation required on the operator
device.

```
Browser  --->  Hearth (web server)  <---  Anvil bus (iceoryx2)  <---  forgeiec_plc (PLC cycle)
                       |
                       +--- instructions --->  Anvil server (anvild)
```

**Licence:** AGPL-3.0-or-later

---

<div style="text-align:center; padding: 2rem;">

**Hearth — The plant in view, from anywhere.**

blacksmith@forgeiec.io

</div>
