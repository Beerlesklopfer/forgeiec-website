---
title: "Roadmap"
linkTitle: "Roadmap"
url: /en/roadmap/
description: "ForgeIEC release plan: one IEC 61131-3 language per version – 0.2 ST, 0.3 LD, 0.4 FBD, 0.5 SFC. Plus connectivity, Rivet, Hearth and migration."
eyebrow: "Release plan"
lead: "One IEC 61131-3 language per version, in a fixed order and without date promises. What runs today is at the top."
full: true
---

<section class="band band--tight">
<div class="container">
<div class="section-head">
<span class="eyebrow">Languages</span>
<h2>One language per version</h2>
<p>The platform – Studio, Anvil server and Tongs – numbers its versions as <code>0.(2+n).0</code>: every new minor version brings one more IEC language. New buses and fixes come as patch versions <code>0.x.y</code>.</p>
</div>
<ol class="timeline">
<li class="tl-item tl-item--now">
<span class="tl-dot" aria-hidden="true"></span>
<span class="tl-when">Now</span>
<div class="tl-card">
<h3><span class="tl-version">0.2</span> Structured Text (ST)</h3>
<p>Editor, own compiler core and transfer to the controller. With patch 0.2.2 the ST editor is in productive use at the pilot customer SoLaWi Ackervielfalt.</p>
{{< status "use" >}}
</div>
</li>
<li class="tl-item tl-item--next">
<span class="tl-dot" aria-hidden="true"></span>
<span class="tl-when">Next</span>
<div class="tl-card">
<h3><span class="tl-version">0.3</span> Ladder Diagram (LD)</h3>
<p>The graphical language of electrical engineering. Not compiled yet.</p>
{{< status "plan" >}}
</div>
</li>
<li class="tl-item">
<span class="tl-dot" aria-hidden="true"></span>
<span class="tl-when">After that</span>
<div class="tl-card">
<h3><span class="tl-version">0.4</span> Function Block Diagram (FBD)</h3>
<p>Wiring blocks graphically. Not compiled yet.</p>
{{< status "plan" >}}
</div>
</li>
<li class="tl-item">
<span class="tl-dot" aria-hidden="true"></span>
<span class="tl-when">After that</span>
<div class="tl-card">
<h3><span class="tl-version">0.5</span> SFC (sequential function chart)</h3>
<p>Sequences of steps and transitions – in the standard a set of structuring elements. Not compiled yet.</p>
{{< status "plan" >}}
</div>
</li>
<li class="tl-item tl-item--dropped">
<span class="tl-dot" aria-hidden="true"></span>
<span class="tl-when">No version</span>
<div class="tl-card">
<h3>Instruction List (IL)</h3>
<p>No longer part of the current standard – not coming. The reason is below.</p>
{{< status "rest" "deprecated" >}}
</div>
</li>
</ol>
</div>
</section>

<section class="band band--soft">
<div class="container">
<div class="section-head">
<span class="eyebrow">Beyond the languages</span>
<h2>Connectivity, remote access, operation, migration</h2>
<p>These areas move independently of the language versions.</p>
</div>
<!-- ENTWURF: owner to confirm the sentence on Rivet's and Hearth's own version numbers. -->
<table class="status-table">
<thead><tr><th scope="col">Area</th><th scope="col">What is planned</th><th scope="col">Status</th></tr></thead>
<tbody>
<tr><td>Connectivity</td><td class="detail">Modbus TCP and RTU available. LoRaWAN is our focus. EtherCAT, PROFIBUS and EtherNet/IP are in progress; new buses come as patch versions.</td><td>{{< status "use" "Modbus available" >}}</td></tr>
<tr><td>PROFINET</td><td class="detail">In C++ against the Siemens stack.</td><td>{{< status "plan" >}}</td></tr>
<tr><td>Rivet – remote access</td><td class="detail">Own version number (currently 0.1.0). Pilot with solidarity farms.</td><td>{{< status "wip" "in development" >}}</td></tr>
<tr><td>Hearth – operator interface</td><td class="detail">Own version number (Hearth Studio currently 0.2.0). Runs over the internal Anvil bus.</td><td>{{< status "wip" "preview" >}}</td></tr>
<tr><td>Migration / import</td><td class="detail">Native import of CODESYS projects (3 and 4). <!-- ENTWURF: owner to clarify exact CODESYS versions and file formats --></td><td>{{< status "plan" "planned, release open" >}}</td></tr>
<tr><td>Migration today</td><td class="detail">Import and export of PLCopen XML in the Studio (menu and AI tools).</td><td>{{< status "use" "available" >}}</td></tr>
</tbody>
</table>
</div>
</section>

<section class="band">
<div class="container split">
<div>
<span class="eyebrow">Background</span>
<h2>Why IL is not coming</h2>
</div>
<div class="prose-band">

IL (instruction list) was deprecated in IEC 61131-3 edition 3 (2013) and is no longer part of the current edition, IEC 61131-3:2025 (published May 2025). ForgeIEC does not develop it; it would also need its own translation path to assembler. <!-- ENTWURF: Annex B der Norm einsehen, bevor es als Normaussage zitiert wird --> Its uses are covered by Structured Text (textual) and by Ladder Diagram and Function Block Diagram (graphical), with Sequential Function Chart as structuring elements.

Sources: [IEC 61131-3:2025 abstract at AFNOR](https://www.boutique.afnor.org/en-gb/standard/iec-6113132025/programmable-controllers-part-3-programming-languages/xs304903/444755) · [Stefan Henneken: comparison of edition 3 and edition 4](https://stefanhenneken.net/2025/06/11/iec-61131-3-comparison-of-edition-3-and-edition-4/) · [Wikipedia: IEC 61131-3](https://en.wikipedia.org/wiki/IEC_61131-3)

Questions about the order, or about a bus you need? Write to [blacksmith@forgeiec.io](mailto:blacksmith@forgeiec.io).

</div>
</div>
</section>
