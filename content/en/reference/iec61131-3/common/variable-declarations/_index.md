---
title: "Variable declarations"
summary: "VAR, VAR_INPUT, VAR_OUTPUT, VAR_IN_OUT, VAR_GLOBAL, VAR_EXTERNAL, VAR_TEMP — the eight scope blocks of IEC 61131-3."
weight: 30
iec_chapter: "6.5"
construct_kind: "declaration"
keywords: ["VAR", "VAR_INPUT", "VAR_OUTPUT", "VAR_IN_OUT", "VAR_GLOBAL", "VAR_EXTERNAL", "VAR_TEMP", "END_VAR"]
llm_signals:
  - error_pattern: "Expected END_VAR"
    where: "FStCompiler"
    diagnosis: "VAR block not closed."
    fix_strategy: "Add END_VAR after the last declaration in the block."
    fix_example: |
      VAR
          iCount : INT;
          xReady : BOOL;
      END_VAR
  - error_pattern: "VAR block in text body"
    where: "FStCompiler"
    diagnosis: "Trying to put a `VAR ... END_VAR` block inside the executable body of a POU. ForgeIEC's MCP write-tools split declarations from body — declarations go through `project.write.add_variable`, body through `project.write.set_text_body`."
    fix_strategy: "Move the declarations out of the body. Use `project.write.add_variable scope_kind=pou scope_name=<POU>` for each variable. Then the body contains only executable statements."
    fix_example: |
      (* WRONG — VAR block inside body *)
      VAR
          iCount : INT;
      END_VAR
      iCount := iCount + 1;

      (* CORRECT — declaration via MCP, body is just statements *)
      (* MCP: project.write.add_variable scope_kind=pou
              scope_name=PLC_PRG name=iCount iecType=INT *)
      iCount := iCount + 1;
  - error_pattern: "VAR_INPUT inside FUNCTION body modified"
    where: "matiec"
    diagnosis: "Function inputs (VAR_INPUT) are read-only inside the function body. Trying to assign to one is a compile error."
    fix_strategy: "Copy the input into a local working variable first."
    fix_example: |
      FUNCTION MyFunc : INT
          VAR_INPUT
              iLimit : INT;
          END_VAR
          VAR
              iLocal : INT;
          END_VAR
          iLocal := iLimit;
          (* now mutate iLocal freely *)
          iLocal := iLocal * 2;
          MyFunc := iLocal;
      END_FUNCTION
---

## The eight scope blocks

| Block | Scope | Persistent? | Used in |
|---|---|---|---|
| `VAR` | POU-local | Across cycles (FB only); per call (FUN) | All POU types |
| `VAR_INPUT` | Read-only input parameter | n/a | All POU types |
| `VAR_OUTPUT` | Output parameter | Across cycles (FB) | FB and FUNCTION (FUN return is separate) |
| `VAR_IN_OUT` | Pass-by-reference parameter | n/a | All POU types |
| `VAR_TEMP` | Throwaway, only valid this call | No | All POU types |
| `VAR_GLOBAL` | Project-wide | Across cycles | GVL POUs (Global Variable Lists) |
| `VAR_EXTERNAL` | Reference to a `VAR_GLOBAL` | Across cycles (the source's lifetime) | All POU types |
| `VAR CONSTANT` | Compile-time constant | n/a | Modifier on any block |

In ForgeIEC, declarations are typically created via the editor's
Variables panel (or via `project.write.add_variable` over MCP),
not as raw `VAR ... END_VAR` text in the body. The XML save
format does emit them as IEC blocks for round-trip
compatibility with other tools, but the editor never asks you
to type them.

## Block syntax

```text
VAR [CONSTANT | RETAIN | NON_RETAIN] [PUBLIC | PRIVATE]
    name1 : TYPE1 [:= initial_value];
    name2, name3 : TYPE2;
END_VAR
```

Modifiers:

- `CONSTANT` — compile-time constant, can't be assigned at run-time.
- `RETAIN` — value survives a power cycle (persisted).
- `NON_RETAIN` — explicit non-persistent (default for most types).
- `PUBLIC` / `PRIVATE` — for FB members; controls whether
  external code can read/write through the FB instance.

## VAR (POU-local)

Inside a `FUNCTION_BLOCK` or `PROGRAM`, `VAR` declarations
persist across scan cycles. Inside a `FUNCTION` they're
re-initialised on every call (functions have no state).

```iec-st
PROGRAM PLC_PRG
    VAR
        iCount   : INT := 0;
        tonStep  : TON;
        sMessage : STRING(80) := 'Init';
    END_VAR
    (* body *)
END_PROGRAM
```

## VAR_INPUT, VAR_OUTPUT, VAR_IN_OUT

Function-block and function parameters:

```iec-st
FUNCTION_BLOCK FB_Counter
    VAR_INPUT
        xCU : BOOL;
        iPV : INT;
    END_VAR
    VAR_OUTPUT
        xQ : BOOL;
        iCV : INT;
    END_VAR
    VAR
        xPrevCU : BOOL;          (* internal state *)
    END_VAR
    (* body *)
END_FUNCTION_BLOCK
```

`VAR_INPUT` is read-only inside the body (you can't assign to
it). `VAR_OUTPUT` is read-write but its lifetime ties to the
FB instance.

`VAR_IN_OUT` passes by reference — the callee mutates the
caller's variable directly. Useful for modifying caller-owned
data structures without copying:

```iec-st
FUNCTION_BLOCK FB_Sort
    VAR_IN_OUT
        arr : ARRAY[1..100] OF INT;
    END_VAR
    (* sorts arr in place — caller sees the result *)
END_FUNCTION_BLOCK
```

## VAR_GLOBAL

In a `GlobalVarList` POU:

```iec-st
VAR_GLOBAL
    gxRunning   : BOOL := FALSE;
    giCounter   : DINT;
    gtonStartup : TON;
END_VAR
```

To use a `VAR_GLOBAL` from another POU, you can either:

1. Declare a `VAR_EXTERNAL` block in the consuming POU that
   names the same identifier and type — the standard's official
   way.
2. Reference it via the three-level form `GVL.<Group>.<Name>`
   directly — ForgeIEC's editor handles this automatically and
   the matiec generator emits the `VAR_EXTERNAL` for you.

The three-level form is preferred in ForgeIEC; it keeps each
POU's `VAR` blocks short and makes the dependency obvious in
the source.

## VAR_TEMP

Function-local scratchpad that's reset at the start of every
call. Useful inside FBs when you don't want a value to persist
across cycles:

```iec-st
FUNCTION_BLOCK FB_Avg
    VAR_INPUT iValues : ARRAY[1..10] OF INT; END_VAR
    VAR_OUTPUT iAvg : INT; END_VAR
    VAR_TEMP
        iSum : DINT;       (* zeroed at every call *)
        i    : INT;
    END_VAR
    iSum := 0;
    FOR i := 1 TO 10 DO
        iSum := iSum + INT_TO_DINT(iValues[i]);
    END_FOR;
    iAvg := DINT_TO_INT(iSum / 10);
END_FUNCTION_BLOCK
```

## RETAIN — power-cycle persistence

`VAR RETAIN` variables keep their value across a PLC restart
(stored in retentive memory; on real hardware this is usually
battery-backed RAM or flash).

```iec-st
VAR RETAIN
    diLifetimeCycles : DINT;
END_VAR
```

In ForgeIEC, the RETAIN modifier maps to the
`is_retain` flag on the pool variable. See Memory:
`project_persistvarlist_to_attribute` for the model rationale.

## IEC reference

IEC 61131-3 third edition (2013), clause **6.5** —
"Variables", subclauses 6.5.1 through 6.5.7 for the individual
blocks.

## matiec conformance

matiec implements all eight blocks per the standard. The
strict separation between declaration and body is the main
ForgeIEC-side wrinkle (`VAR` blocks live in the editor's
declaration panels, not in `set_text_body` payloads) — see
the second `llm_signals` entry above.
