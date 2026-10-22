---
title: "Architecture"
url: /en/architecture/
eyebrow: "For technical leaders"
lead: "How ForgeIEC is built: which processes run on the controller, how they exchange data, how faults are reported — and why it is built this way."
description: "ForgeIEC architecture: Studio, Anvil server (anvild), PLC cycle process forgeiec_plc, Anvil bus on iceoryx2, one Tongs bridge per bus segment, the Tongs-Bus as control plane, fault and parameter model, decisions with their reasons."
full: true
---

<!-- Sources: tongs-core wiki (branch main: Architecture, Platform, Tongs-Bus, Runtime, Parameters, Diagnostics),
     audit widersprueche/03-architektur.md (A-03, A-04, A-15), 01-webseite.md (W-15),
     forgeiec-rivet README (branch development), Cargo descriptions in anvil-server/crate-contract and shared. As of 22.10.2026. -->

<section class="band band--tight">
<div class="container arch">

ForgeIEC keeps three jobs apart: **programming** at the workstation, **running** on the controller and **connecting** the field devices. Each job runs in its own processes, which exchange data over a shared-memory bus. If one bus connection fails, the rest keeps running.

<ul class="toc-inline" aria-label="On this page">
<li><a href="#overview">Overview</a></li>
<li><a href="#building-blocks">Building blocks and repositories</a></li>
<li><a href="#crates">Crate tree</a></li>
<li><a href="#planes">Data planes</a></li>
<li><a href="#fault-model">Fault model</a></li>
<li><a href="#parameters">Parameter model</a></li>
<li><a href="#decisions">Decisions</a></li>
<li><a href="#status">Status</a></li>
</ul>

</div>
</section>

<section class="band band--soft" id="overview">
<div class="container arch">

<span class="eyebrow">Overview</span>

## The system at a glance

The Studio on the workstation talks **gRPC** to the **Anvil server (anvild)** on the controller. There, the PLC program, the bus connections and the operator interface run as separate processes; they exchange data over the **Anvil bus**, a publish/subscribe bus on shared memory (iceoryx2).

{{< figure-svg name="system-overview" caption="Processes and connections. Solid arrows: data; coloured: the control plane (Tongs-Bus), on which only anvild writes into a Tongs." >}}
Top left, ForgeIEC Studio on the workstation. It is connected over gRPC to the Anvil server (anvild) on the controller. anvild starts the PLC cycle forgeiec_plc as a process of its own. Both are attached to the Anvil bus (iceoryx2, shared memory), which carries process data, status and diagnosis. On the same bus runs the Tongs-Bus, the control plane whose only master is anvild. Below, one Tongs process per bus segment (Modbus TCP/RTU, LoRaWAN in progress, others) and Hearth, the operator interface, as a preview. The Tongs talk to the field devices; Hearth delivers screens to a browser on a panel or tablet. On the right, the remote access Rivet (in development): a gateway in the controller's LAN builds only outgoing connections to a central server, through which a phone with the WireGuard app reaches the released controller.
{{< /figure-svg >}}

- **ForgeIEC Studio** translates the IEC program (Structured Text) into C++ source and transfers it to the controller.
- **anvild** builds the program **`forgeiec_plc`** from it with `make` and `g++` and starts it as a process of its own. It also starts and supervises one **Tongs** per bus segment (German *Zange*, tongs): a bridge between the PLC and the field devices.
- **The Anvil bus** connects all processes on the controller without copying the data.
- **The Tongs-Bus** is the backplane of anvild: addresses, heartbeat, parameters and commands for the Tongs. Hearth (and the resting gateway bellowsd) read along and instruct anvild when they want something changed.
- **Hearth** reads the process data directly from the Anvil bus; anvild publishes the HMI groups from the PLC program's monitor stream. Hearth produces no values, it shows them.
- **Rivet** brings the controller's screen safely to a phone, without port forwarding — more on the [Rivet page](/en/rivet/).

</div>
</section>

<section class="band" id="building-blocks">
<div class="container arch">

<span class="eyebrow">Layers</span>

## Building blocks and repositories

Every layer has its own repository. The Tongs and tongs-core are submodules of the `anvil` repository and build only inside that tree; every participant on the bus builds against the same iceoryx2 version as anvild.

<div class="grid grid-3">
<div class="card">
<p class="card-kicker">Workstation</p>
<h3>Studio</h3>
<p>The engineering tool (C++, Qt 6): ST editor, own compiler core, bus configuration, diagnosis. Talks to the controller over gRPC only.</p>
</div>
<div class="card">
<p class="card-kicker">Controller</p>
<h3>anvil</h3>
<p>The Anvil server <code>anvild</code>, the transport <code>shared/anvil</code> (iceoryx2 with a stable C interface for the PLC runtime) and the contract crates. Holds all Tongs as submodules.</p>
</div>
<div class="card">
<p class="card-kicker">Common base</p>
<h3>tongs-core</h3>
<p>What all Tongs share: fault model, status format, runtime frame, Tongs-Bus protocol, parameter and diagnosis model. A new Tongs contains only its protocol.</p>
</div>
<div class="card">
<p class="card-kicker">Bus connection</p>
<h3>The Tongs</h3>
<p>One repository per protocol: <code>tongs-modbustcp</code>, <code>tongs-modbusrtu</code>, <code>tongs-ethercat</code>, <code>tongs-ethernetip</code>, <code>tongs-profibus</code>, plus <code>tongs-lorawan</code> in progress.</p>
</div>
<div class="card">
<p class="card-kicker">Contracts</p>
<h3>crate-contract and shared</h3>
<p>One source of truth for what several processes speak: the codec for IEC types on the wire, the reader of the variable description, the command handshake. <code>shared</code> is the Anvil transport itself.</p>
</div>
<div class="card">
<p class="card-kicker">Operation</p>
<h3>hearth</h3>
<p>Hearth Server (Rust) shows screens in the browser and reads the Anvil topics for them; Hearth Studio is its editor. Runs as a preview today.</p>
</div>
</div>

</div>
</section>

<section class="band band--soft" id="crates">
<div class="container arch">

<span class="eyebrow">For developers</span>

## The crate tree of tongs-core

Three of the five crates have **no access to processes, memory or network**. They run in unit tests without shared memory — which keeps the heart of every bus connection fast and fully testable.

{{< figure-svg name="crate-tree" caption="Arrows point from a crate to what it uses. A Tongs depends only on tongs-core and tongs-runtime; tongs-core re-exports the types of the model crates." >}}
At the top, the Tongs programs (own repositories) and anvild. A Tongs uses tongs-runtime and tongs-core. tongs-runtime uses tongs-core and anvil, the transport with a C interface, which in turn uses iceoryx2 version 0.9.2. tongs-core uses the diagnosis model forge-device-diag and the parameter model forge-tongs-params; forge-device-diag also uses forge-tongs-params. Only with the Cargo feature "bus" does tongs-core also use the bus protocol forgeiec-tongs-bus and anvil. anvild uses forgeiec-tongs-bus, anvil and tongs-core. forge-device-diag, forge-tongs-params and forgeiec-tongs-bus do no input or output.
{{< /figure-svg >}}

- **tongs-core**: the fault state machine, status format, backoff, clocks; with feature `bus` the Tongs as a participant on the Tongs-Bus.
- **tongs-runtime**: command line, signals, configuration, Anvil binding, status publisher, supervisor. A Tongs implements exactly one trait, `Protocol`.
- **forgeiec-tongs-bus**: the Tongs-Bus protocol, *sans-IO*.
- **forge-tongs-params** and **forge-device-diag**: parameter and diagnosis model; the C header for the Studio is generated from the diagnosis model, and a test keeps both equal.

</div>
</section>

<section class="band" id="planes">
<div class="container arch">

<span class="eyebrow">Data</span>

## Four data planes on one bus

Process values, state, diagnosis and control commands travel on separate topics. **The Tongs-Bus carries addresses, heartbeat, parameters and commands, never process values** — so administration never disturbs the cycle.

{{< figure-svg name="data-planes" caption="The topics on the Anvil bus and their direction. The status arrives at least once a second even when a segment has no devices." >}}
On the left the PLC program forgeiec_plc, the readers (anvild, Hearth, Studio) and anvild as the master; on the right the Tongs, one process per segment. First, the PLC program sends its outputs cyclically on Anvil/GROUP to the Tongs. Second, the inputs come back from the Tongs on Anvil/GROUP/bridge. Third, the Tongs publishes the state of every device on Anvil/status/segment, at least once a second. Fourth, it publishes the diagnostic values from the device description on Anvil/diag/segment. Fifth, in both directions between anvild and the Tongs: the Tongs-Bus on Anvil/tongsbus for addresses, heartbeat, parameters and commands, never for process values.
{{< /figure-svg >}}

The status record is binary and of fixed size (5152 bytes for up to 64 devices per segment). A reader judges freshness by its own clock: a record older than three seconds means a dead Tongs, and its devices count as offline.

</div>
</section>

<section class="band band--soft" id="fault-model">
<div class="container arch">

<span class="eyebrow">Reliability</span>

## The fault model

**Every bus connection reports faults with the same ten states** — whether Modbus, LoRaWAN or EtherCAT. A PLC program therefore sees one diagnosis interface for every protocol: `xOnline`, `xFault` and `xWarning` per device, plus error code and counters. Only in the states *Online* and *Degraded* can values be trusted; *Degraded* means online, but with a failing variable. The generated PLC code, the Studio display, Hearth and anvild all use the same classification.

Every device has its own connection state, its own status and its own backoff; an unreachable device does not delay another, and device tasks share no blocking lock. State changes go through a single function that refuses transitions the model does not have. After a failure, the Tongs waits exponentially (1, 2, 4, 8, 16, then 30 s). If a Tongs crashes, anvild restarts it with a backoff (at most 30 s); the state held by anvild stays untouched.

{{< figure-svg name="fault-model" caption="The allowed transitions (tongs_core::can_transition). A device that never answered is Unreachable, not Timeout." >}}
The start is Unknown. From Unknown to Connecting or Disabled; from Disabled to Connecting once the device is enabled. Connecting leads to Online, Unreachable or ConfigError; ConfigError leads back to Connecting only after the configuration is reloaded. Online and Degraded change into each other and both lead to Timeout or Unreachable. Timeout and Unreachable lead to Backoff, and Backoff after a wait of 1, 2, 4, 8, 16, then 30 seconds back to Connecting. Every state except Shutdown leads to Shutdown, the end.
{{< /figure-svg >}}

</div>
</section>

<section class="band" id="parameters">
<div class="container arch">

<span class="eyebrow">Settings</span>

## The parameter model

**A setting is checked first, then made effective, then saved — and every side checks it with the same code.** Parameters exist on two levels: device parameters come from the manufacturer's device description (FDD); a Tongs does not invent any. Segment parameters are what no FDD can know — where a radio service listens, say, or a cycle time; the Tongs describes them itself and prints the description even without a running process (`--describe`). The Studio renders both without knowing the protocol.

Values are binary, encoded as IEC types and addressed by number. A write lands in a draft first; `APPLY` makes it effective or refuses it with reasons, `SAVE` stores it atomically, `DISCARD` drops it. anvild checks every value before the bus exactly as the Tongs will and names every refused one. Secret values are never read back, only whether they are set and a fingerprint; anvild does not write them over the bus today because its encryption is not built yet — they come from the project.

</div>
</section>

<section class="band band--soft" id="decisions">
<div class="container arch">

<span class="eyebrow">Why this way</span>

## Decisions and their reasons

<div class="grid grid-2">
<div class="card decision">
<p class="card-kicker">Process per bus segment</p>
<h3>One Tongs per segment instead of one big daemon</h3>
<p class="why">A hanging or crashing protocol takes down neither the PLC nor other buses. anvild restarts the Tongs; each one reloads on its own (SIGHUP) and ends in order (SIGTERM, within five seconds).</p>
</div>
<div class="card decision">
<p class="card-kicker">Control plane</p>
<h3>Typed binary records instead of JSON</h3>
<p class="why">Every register has a fixed layout of IEC types; no JSON, no XML. The master needs no parser, telegrams fit into 512-byte frames, and a malformed write is refused at once. The gRPC interface to the Studio carries typed messages as well.</p>
</div>
<div class="card decision">
<p class="card-kicker">Testability</p>
<h3>A protocol core without input and output</h3>
<p class="why">The bus protocol is <em>sans-IO</em>: frames and time go in, frames and events come out. So it runs in tests on a simulated line, a lossy one included — without shared memory, without a network.</p>
</div>
<div class="card decision">
<p class="card-kicker">Clear authority</p>
<h3>One master per machine</h3>
<p class="why">Only anvild writes into a Tongs; any other write is refused. A Tongs therefore needs no rights list. If a master hears a second one at start-up, it leaves the bus and anvild ends.</p>
</div>
<div class="card decision">
<p class="card-kicker">Lifetime</p>
<h3>The bridges end with the master</h3>
<p class="why">PLC program and Tongs end with anvild; without a heartbeat (default 3 s) a Tongs must end. The field devices go to their safe state through their own supervision. The rule applies to Tongs on the Tongs-Bus; the existing protocol Tongs do not use it yet (as of 22.10.2026).</p>
</div>
<div class="card decision">
<p class="card-kicker">Sampling</p>
<h3>At most half the system cycle</h3>
<p class="why">To sample a signal without aliasing, the poll period may be at most 0.5 × the system cycle. The achieved period is measured, not assumed: anvild computes mean, jitter and overruns per device and reports violations.</p>
</div>
</div>

On security on the machine: the Anvil transport admits only processes of anvild's user group. That is the outer fence, not an authorisation; authentication of privileged writes on the Tongs-Bus is specified but not built yet. ForgeIEC does not replace a safety PLC (no SIL/PL).

</div>
</section>

<section class="band" id="status">
<div class="container arch">

<span class="eyebrow">Honest status</span>

## What runs today

<div class="table-wrap">
<table class="status-table">
<thead><tr><th>Building block</th><th>Details</th><th>Status</th></tr></thead>
<tbody>
<tr><td>ST editor, compiler core, anvild, forgeiec_plc</td><td class="detail">Preview version 0.2, in pilot use at the SoLaWi Ackervielfalt</td><td>{{< status "use" >}}</td></tr>
<tr><td>Modbus TCP / RTU</td><td class="detail">bridges for both variants</td><td>{{< status "use" "available" >}}</td></tr>
<tr><td>LoRaWAN</td><td class="detail">the focus for the SoLaWis</td><td>{{< status "wip" >}}</td></tr>
<tr><td>EtherCAT, PROFIBUS, EtherNet/IP</td><td class="detail">skeleton with fault model and binding, protocol part to follow</td><td>{{< status "wip" >}}</td></tr>
<tr><td>Hearth (operation)</td><td class="detail">over the Anvil bus, as a preview</td><td>{{< status "wip" "preview" >}}</td></tr>
<tr><td>Rivet (remote access)</td><td class="detail">in development, pilot with SoLaWis</td><td>{{< status "wip" >}}</td></tr>
<tr><td>bellowsd (HMI/OPC UA gateway)</td><td class="detail">not in development at present</td><td>{{< status "rest" >}}</td></tr>
</tbody>
</table>
</div>

Source code under AGPL-3.0-or-later; access on request. The developer documentation (the tongs-core wiki with architecture, dependency tree and "where do I change what") is not public yet — access on request as well, at [blacksmith@forgeiec.io](mailto:blacksmith@forgeiec.io).

</div>
</section>
