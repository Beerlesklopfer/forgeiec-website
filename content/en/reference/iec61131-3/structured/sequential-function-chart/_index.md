---
title: "Sequential Function Chart (SFC)"
summary: "Step-and-transition state-machine notation; hosts ST/IL/LD/FBD inside its action bodies."
weight: 10
---

## Sequential Function Chart

SFC is the IEC-blessed way to express **sequential machine
logic** without inventing a step counter by hand. The program
is drawn as a graph of:

- **Steps** — numbered states the program can be in. Each step
  has zero or more **actions** attached, each action written in
  one of the four "real" languages (ST, IL, LD, FBD) and run
  while the step is active.
- **Transitions** — boolean conditions between steps. When the
  condition fires, the source step deactivates and the target
  step activates.
- **Branches** — divergence (one step → many possible next
  steps) and convergence (many possible previous steps → one
  next step), both in alternative ("OR") and parallel ("AND")
  flavour.

SFC is sometimes called the "fifth language" but it is not on
the same level as the other four. ST/IL/LD/FBD are general-
purpose programming languages; SFC is a **structuring layer**
that uses one of those four to describe what each step does.

### Sub-pages

- [Elements](elements/) — steps, transitions, action
  qualifiers, divergence / convergence patterns.
