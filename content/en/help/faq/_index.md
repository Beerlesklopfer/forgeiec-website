---
title: "FAQ"
summary: "Growing collection of common questions + practical solutions"
---

## Frequently Asked Questions

This page collects symptoms + solutions that come up repeatedly during
development or commissioning. Each entry is sorted by **symptom** and
names both the quick fix and the underlying cause — so that you not
only solve the immediate problem but also understand why it happened.

The FAQ grows with the project — if you have a case that is missing,
write to blacksmith@forgeiec.io or open an issue.

---

## Topics

### [Variables "stick" despite a fresh deploy](/help/faq/stuck-variables-shm/)

A BOOL or INT variable holds a value (TRUE/FALSE or a numeric value)
that does not match the program logic. `monitor.snapshot` reports
`forced=false`, the ST code clearly writes a different value — and
yet the value stays "glued". Cause: stale Anvil shared memory.

---

<div style="text-align:center; padding: 2rem;">

**Questions grow with the project — and the answers grow with them.**

blacksmith@forgeiec.io

</div>
