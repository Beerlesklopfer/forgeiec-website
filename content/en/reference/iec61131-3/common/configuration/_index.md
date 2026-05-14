---
title: "Configuration: CONFIGURATION, RESOURCE, TASK"
summary: "How PROGRAMs are bound to tasks and how tasks are scheduled. The IEC equivalent of an OS scheduler config."
weight: 50
iec_chapter: "6.8"
construct_kind: "configuration"
keywords: ["CONFIGURATION", "RESOURCE", "TASK", "PROGRAM", "INTERVAL", "PRIORITY"]
---

## The three layers

| Layer | What it represents | Plural? |
|---|---|---|
| `CONFIGURATION` | One PLC system | One per project, typically |
| `RESOURCE` | One CPU within the PLC | Many — multi-CPU PLCs |
| `TASK` | One scheduling slot on a resource | Many per resource |
| `PROGRAM` instance | An instantiated PROGRAM POU bound to a task | Many per task (rare) |

A `PROGRAM` POU type is **just a class** — it doesn't run on
its own. It runs only when a `PROGRAM <name> WITH <task>;`
statement inside a `RESOURCE` block instantiates it and binds
it to a task.

## Syntax

```iec-st
CONFIGURATION MyConfig
    RESOURCE MainCPU ON CPU01
        TASK fastTask(INTERVAL := T#10ms, PRIORITY := 1);
        TASK slowTask(INTERVAL := T#1s,  PRIORITY := 5);

        PROGRAM ioCycle WITH fastTask : PLC_PRG();
        PROGRAM stats   WITH slowTask : PRG_Stats();
    END_RESOURCE
END_CONFIGURATION
```

This says:
- One PLC, one CPU.
- Two tasks: `fastTask` runs every 10 ms, `slowTask` every
  1 second. Lower priority number = higher priority.
- Two PROGRAM instances: `ioCycle` of type `PLC_PRG` runs on
  fastTask; `stats` of type `PRG_Stats` runs on slowTask.

## TASK parameters

```iec-st
TASK <name>(INTERVAL := <time>, PRIORITY := <int>);
TASK <name>(SINGLE := <bool_var>, PRIORITY := <int>);
```

- `INTERVAL` — periodic task; runs every N time units.
  Most common.
- `SINGLE` — event-triggered task; runs once each time the
  named BOOL variable rises FALSE→TRUE. Used for
  interrupt-style work.
- `PRIORITY` — integer 0..N where 0 is highest. The runtime
  scheduler preempts a lower-priority task when a higher-
  priority task becomes ready.

## PROGRAM instances and the task scheduler

Each PROGRAM instance is a separate state-bearing
incarnation of the PROGRAM POU type. Two instances of the
same PROGRAM type bound to two different tasks have their
own VAR storage, run their own timer FB instances etc.

In ForgeIEC, the configuration block is rarely written by
hand — the editor manages it through the
"Task Configuration" dialog and emits the IEC syntax at
save-time. The MCP `tasks.list_resources` /
`tasks.write.create_task` / `tasks.write.add_program_instance`
tools cover the same ground programmatically.

## Cycle time and budgeting

A periodic task with `INTERVAL := T#20ms` is expected to
finish its work in **less than 20 ms**, every cycle, every
time. If it doesn't, the runtime flags an overrun and the
behaviour is implementation-defined (some runtimes skip the
next cycle, some signal a fault, some keep running with
ever-growing lag).

Two consequences for ST code:

- Loops in PROGRAM bodies must be bounded — see the
  [iteration scan-cycle warning](../../textual/structured-text/iteration/).
- Timer FBs (`TON`, `TOF`, `TP`) tick at task-cycle
  granularity. A `TON(PT := T#1ms)` in a 20 ms task fires
  after one full task cycle, not after the nominal 1 ms.

## VAR_GLOBAL access scope

`VAR_GLOBAL` declared inside a `RESOURCE` is scoped to that
resource. `VAR_GLOBAL` at `CONFIGURATION` level is visible to
all resources. Cross-resource sharing requires `VAR_ACCESS`
declarations — rare and seldom needed in single-CPU PLC
projects.

## IEC reference

IEC 61131-3 third edition (2013), clause **6.8** —
"Configuration and resource elements".

## matiec conformance

matiec implements the full configuration syntax and the
priority-based scheduler model. ForgeIEC's anvild runtime
honours `INTERVAL` and `PRIORITY` on POSIX targets via
`pthread_setschedparam`.

The `SINGLE` (event-triggered) task variant is supported by
matiec but uncommon in ForgeIEC projects — most production
work uses `INTERVAL` cyclic tasks.
