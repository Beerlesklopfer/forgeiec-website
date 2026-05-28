---
title: "Live diagnostics: monitor + oscilloscope for IEC 61131-3"
date: 2026-05-10
summary: "Live variable values, FB-member resolution, oscilloscope with trigger, CSV recording, measured jitter — commissioning tools at industry level"
components: [studio, anvild]
---

{{< components "studio,anvild" >}}

## What it's about

During commissioning you spend 90 % of the time **observing**:
which variable has which value, when does which timer switch, why
does the motor refuse to run. ForgeIEC Studio has a complete
diagnostic stack for that — live values on the Variables tab, an
oscilloscope with trigger for time series, and honest statements
about sampling limits.

---

## Live values throughout the editor

- **Variables tab** shows live values per pool variable, shared
  between UI + AI assistant (same data source).
- **POU locals** in the live snapshot — even nested FB outputs
  like `kr_main.StepTimer.Q` are resolved and visible.
- **Force status** per variable shows `forced=true/false` in the
  snapshot — also queryable via the `monitor.snapshot` MCP tool.
- **Detach on project switch**: no more "ghost watches" — the
  `FLiveValueStore` cleans up properly when you close or open a
  project.

Background: live values flow via gRPC from the anvild daemon to
Studio; during the migration away from an older Zenoh/Spark setup
the whole pipeline became more robust + faster.

---

## Oscilloscope with trigger

Classic PLC diagnostic question: "Why does `Motor_Ready` not
switch, even though all conditions should be met?"

Answer: oscilloscope capture — pre-trigger window + trigger on
edge / threshold / comparison:

```
oscilloscope.capture {
  channels: ["MX0.0 LED_00", "%MD200 Pressure_1"]
  duration_ms: 5000
  pre_trigger_ms: 1000
  trigger: { pool_address: "%MX0.0", condition: "rising", threshold: 0.5 }
}
```

Returns a time series with relative `t_us` values and statistics
per channel (mean, min, max, p95, p99). CSV export via
`oscilloscope.export_csv` — for Excel + log analysis + reports.

Plus: **streaming mode** with `oscilloscope.start_streaming` +
`stop_streaming` for long sessions that don't fit in a single
capture.

---

## Recording workflow

`monitor.start_recording` starts a background watch recording —
all watched variables are logged. `stop_recording` closes the CSV
file. Useful for "24h weekend run" or "watch a new plant for 4
hours and analyse afterwards".

---

## Cycle stats + honest measurement limits

`monitor.cycle_stats` delivers task cycle statistics — min, max,
average, jitter. Plus a **jitter baseline spec** in the repository
at `tests/data/runtime/jitter_baseline.json`, measured with a
dedicated test script (`test/qa/measure_jitter.py`).

The sampling floor is the **shortest task cycle time** — ForgeIEC
communicates that explicitly in the `monitor.read_value` response
and in the AI init string:

> "The shortest task cycle time is the sampling floor.
> Expected pulse duration = timer constant + 1 task cycle
> (switching delay via TON reset pattern)."

No "infinite resolution" marketing fog, just honest physics.

---

## FB member resolution — even nested

So far in many IDEs not a given: that a `MyTimer.Q` or
`kr_main.StepTimer.Q` is visible in the live snapshot without
manually setting up a watch per FB instance. ForgeIEC Studio:

- On the bridge side (anvild), codegen emits FB-member outputs
  automatically into the monitor stream.
- Editor-side, `monitor.snapshot` and the Variables tab show the
  full resolved path.
- Identifiers are tree-sitter-typed, so also autocompletable in
  live-monitor filters and scope channel selectors.

---

## What the commits delivered

- `b94251a`, `a41f12b` — FB-member outputs in the live snapshot
- `7fd5476` — setWatchInterval loss fix + scope gRPC migration
- `9b3db68`, `5a777e7` — jitter baseline tool + quantitative
  measurement script
- `db4d84c` — `oscilloscope.*` (5 tools)
- `b221ebf` — `monitor.start_recording` + `stop_recording`
- `193bf3d` — `FLiveValueStore` lifecycle: clearAllWatches +
  detach on pool switch
- `3c61445` — `tasks.cycle_overview` + `bellows.protocol_status`
- `f7546bc` — multi-source watches + FB outputs helper

---

## Where you use it

| Question | Tool |
|---|---|
| "Is a switch at TRUE?" | Variables tab live column |
| "Which values did LED_04 have in the last 5 s?" | `oscilloscope.capture` |
| "Exactly when does `Motor_Ready` switch?" | Scope with rising-edge trigger |
| "How long does the task take in worst case?" | `monitor.cycle_stats` |
| "What changed during the weekend run?" | `start_recording` + CSV analysis |

---

## Where to read more

- [What the AI can do](/help/ai/tools/) — live observation section
- [MCP for application engineers](/help/mcp/programmers/) — SSE
  stream docs
