---
title: "Ledger"
description: "Order Management — production planning, recipe management, and MES integration"
weight: 7
---

## The Ledger — *In Development*

Every forge keeps an order book — which order, which material, which quantity.
**Ledger** is the order management module of the ForgeIEC platform: the bridge
between manufacturing control and business operations.

> Ledger is in active development. The features described here
> represent the planned scope.

---

## Planned Features

### Production Planning

- Order entry and prioritization
- Capacity planning and machine scheduling
- Real-time order status tracking
- Feedback from the PLC — automatic progress reporting

### Recipe Management

- Management of production recipes and parameter sets
- Versioning and release workflow
- Automatic parameter transfer to the PLC on order change
- Traceability: which recipe was loaded when

### Batch Tracking

- Batch logging with timestamps
- Assignment of production data to orders
- Material tracking from receiving to finished product
- Export function for quality documentation

### MES Integration

- Interfaces to supervisory MES systems
- ISA-95-compatible data models
- REST/OPC-UA-based data exchange
- Bidirectional: receive orders, send feedback

---

## Platform Integration

Ledger connects the production level (Anvil, Tongs) with the planning
level (MES, ERP). The PLC reports piece counts and states, Ledger
manages the orders and controls the material flow.

```
ERP / MES
    |
  Ledger (Order Management)
    |
  anvild (PLC Core)
    |
  Tongs (Fieldbus Bridges) --> Machines
```

---

<div style="text-align:center; padding: 2rem;">

**Ledger — From order to finished product.**

blacksmith@forgeiec.io

</div>
