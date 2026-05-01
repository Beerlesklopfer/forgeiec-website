---
title: "Project file format (.forge)"
summary: "Anatomy of a ForgeIEC project file: PLCopen XML with ForgeIEC extensions"
---

## Overview

A ForgeIEC project file uses the **`.forge`** extension (the legacy
`.forgeiec` extension is still accepted on load) and is a regular
**PLCopen TC6 XML document** with a few ForgeIEC-specific extensions
attached through the standard `<addData>` mechanism. The file is UTF-8,
human-readable, diff-able in any XML editor, and Git-friendly.

```
.forge file
  +-- <project>            ← PLCopen root element
        +-- <fileHeader>   tool meta (name, date)
        +-- <contentHeader> author, project name
        +-- <types>        data types + POUs (PROGRAM/FB/FUNCTION + GVLs)
        +-- <instances>    resource / task configuration
        +-- <addData>      ForgeIEC extensions (bus, pool, ...)
```

## Root element

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://www.plcopen.org/xml/tc6_0201">
  <fileHeader companyName="ForgeIEC"
              creationDateTime="2026-04-30T12:00:00"
              productName="ForgeIEC"
              productVersion="0.1.0"/>
  <contentHeader author="Joerg Bernau" name="Ackersteuerung"/>
  ...
</project>
```

| Attribute | Meaning |
|---|---|
| `xmlns` | PLCopen TC6 namespace (fixed) |
| `companyName` | producer tool — always `"ForgeIEC"` for ForgeIEC |
| `creationDateTime` | ISO-8601 timestamp of first creation |
| `productVersion` | editor version that wrote the file |
| `author` | free-form author label |
| `name` | project name (UI label, not a filename) |

## `<types>` — library + POUs

Three sections:

### `<dataTypes>`

User-defined data types (STRUCT, enumerations, aliases).

```xml
<dataTypes>
  <dataType name="ST_KcCurve">
    <baseType>
      <struct>
        <variable name="days_initial"><type><INT/></type></variable>
        <variable name="days_growing"><type><INT/></type></variable>
      </struct>
    </baseType>
  </dataType>
</dataTypes>
```

### `<pous>`

All program organization units:

| pouType | Meaning |
|---|---|
| `program`        | PROGRAM (top-level code) |
| `functionBlock`  | FUNCTION_BLOCK (instantiable, stateful) |
| `function`       | FUNCTION (stateless, has `returnType`) |

Every POU has an `<interface>` (variable declarations grouped into
`<inputVars>`, `<outputVars>`, `<inOutVars>`, `<localVars>`,
`<externalVars>`, `<tempVars>`) and a `<body>` carrying ST source code
in an `<ST>` element.

```xml
<pou name="PLC_PRG" pouType="program">
  <interface>
    <localVars>
      <variable name="counter"><type><INT/></type></variable>
    </localVars>
  </interface>
  <body>
    <ST>
      <xhtml xmlns="http://www.w3.org/1999/xhtml">counter := counter + 1;</xhtml>
    </ST>
  </body>
</pou>
```

### Special POU types (ForgeIEC extension)

ForgeIEC introduces five list-shaped POUs stored with their own `pouType`:

| pouType            | Purpose |
|---|---|
| `globalVarList`    | GVL — programmer-visible variable pool |
| `tempVarList`      | TVL — VAR_TEMP list |
| `persistVarList`   | PVL — VAR_PERSIST list (RETAIN) |
| `anvilVarList`     | AnvilVarList — auto-generated PUBLISH/SUBSCRIBE |
| `hmiVarList`       | HmiVarList — Bellows HMI export |

## `<instances>` — resource / task

```xml
<instances>
  <configurations>
    <configuration name="config0">
      <resource name="resource0">
        <task name="task0" interval="T#20ms" priority="0"/>
        <pouInstance name="instance0" taskName="task0" typeName="PLC_PRG"/>
      </resource>
    </configuration>
  </configurations>
</instances>
```

`interval` sets the cycle time. Multiple tasks are supported; each task
runs one or more program instances.

## `<addData>` — ForgeIEC extensions

PLCopen TC6 allows vendor-specific data under `<addData>`. ForgeIEC
uses several namespaces:

| Namespace | Content |
|---|---|
| `https://forgeiec.io/v2/bus-config`  | bus segments + devices ([detail](/en/help/bus-config/)) |
| `https://forgeiec.io/v2/address-pool`| address pool: located variables, bus bindings, tags |
| `https://forgeiec.io/v2/monitoring`  | UI state: which variables are live-monitored |

Typical layout:

```xml
<addData>
  <data name="https://forgeiec.io/v2/bus-config" handleUnknown="discard">
    <fi:busConfig xmlns:fi="https://forgeiec.io/v2">
      <fi:segment ...>
        <fi:device ...>
          <fi:module .../>
        </fi:device>
      </fi:segment>
    </fi:busConfig>
  </data>
</addData>
```

`handleUnknown="discard"` is the PLCopen directive: a tool that does
not understand this block may discard it — the file is still valid
PLCopen XML.

### Address pool

The address pool is **the single source of truth** for the variables of
a plant. Each entry has the **IEC address as primary key** (`%IX0.0`,
`%QW3`, …) — names, tags and bus bindings are descriptors that may
change without breaking identity.

```xml
<addData>
  <data name="https://forgeiec.io/v2/address-pool" handleUnknown="discard">
    <fi:pool xmlns:fi="https://forgeiec.io/v2">
      <fi:variable address="%IX0.0"
                   name="T_1"
                   anvilGroup="Pfirsich"
                   busDirection="in"
                   deviceId="0e5d5537-e328-44e6-8214-78d529b18ebd"
                   modbusAddress="0"
                   moduleSlot="0"/>
    </fi:pool>
  </data>
</addData>
```

| Attribute | Required | Meaning |
|---|---|---|
| `address`        | yes  | IEC address — primary key in the pool |
| `name`           | no   | programmer-visible name (`T_1`, `Motor_Run`) |
| `anvilGroup`     | no   | Anvil IPC group (hardware channel) |
| `gvlNamespace`   | no   | GVL grouping (editor side) |
| `hmiGroup`       | no   | Bellows HMI group (HMI channel) |
| `busDirection`   | no   | `in` / `out` — polling direction |
| `deviceId`       | no   | UUID of the bus device this variable is bound to |
| `modbusAddress`  | no   | Modbus register offset relative to the slave |
| `moduleSlot`     | no   | slot inside the device |

A variable can carry **several tags simultaneously** (e.g. both
`anvilGroup="Pfirsich"` and `hmiGroup="Pfirsich"`). For the ST compiler
to accept the Bellows form `Bellows.Pfirsich.T_1`, the **HMI export for
that group must additionally be enabled** — otherwise the `hmiGroup`
tag stays a pure descriptor without effect on code generation.

<!--
TODO (backlog):
  1. Dedicated doc page covering the Bellows export switch (exact
     condition: per-variable flag vs. HmiVarList activation).
  2. ST compiler: add the validation pass that rejects references to
     an inactive Bellows tag with a clear compile error.
-->


## ST language additions (body content)

The `<ST>` body carries IEC 61131-3 Structured Text wrapped in xhtml.
ForgeIEC adds two convenience features on top:

### Bit access on ANY_BIT types

`var.<bit>` extracts/sets a single bit, directly on `BYTE`/`WORD`/
`DWORD`/`LWORD` variables:

```iec
bButtons.0 := IN_Buttons.0 OR Bellows.Pfirsich.T_1;
OUT_Valves.3 := jk[3].Q;
```

The compiler lowers it to clean bit masking.

### 3-level qualified variables

`<Category>.<Group>.<Variable>` reaches pool entries without declaring
GVLs explicitly:

| Category prefix  | Source |
|---|---|
| `Anvil.X.Y`      | pool variable with `anvilGroup="X"` |
| `Bellows.X.Y`    | pool variable with `hmiGroup="X"` |
| `GVL.X.Y`        | pool variable with `gvlNamespace="X"` |
| `HMI.X.Y`        | synonym for `Bellows.X.Y` |
| `POOL.X.Y`       | any tag |

`Anvil.X.Y` and `Bellows.X.Y` may resolve to **two distinct pool
entries** — the compiler emits separate C symbols whenever the entries
have different IEC addresses.

## Migration / compatibility

* File extension: `.forge` is canonical. `.forgeiec` (legacy) is still
  accepted on load; on save the editor writes `.forge`.
* The XML format is backward compatible: older ForgeIEC versions ignore
  unknown `<addData>` blocks (`handleUnknown="discard"`) and open the
  file anyway.
* Standard PLCopen tools open the standard part (`<types>`, `<instances>`)
  correctly; ForgeIEC extensions are missing there but survive a save
  cycle as long as the foreign tool round-trips `<addData>` blocks
  unchanged.

## Related topics

* [Bus configuration](/en/help/bus-config/) — detailed schema for
  `fi:busConfig`, devices and modules.
* [Test coverage](/en/help/tests/) — automated tests that keep the
  format round-trip stable.
