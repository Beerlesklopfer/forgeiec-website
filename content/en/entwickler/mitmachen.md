---
title: "Contribute"
linkTitle: "Contribute"
url: /en/developer/contribute/
description: "ForgeIEC has become too big to carry alone. Where help is wanted — bus bridges, graphical editors, documentation, test hardware, packaging — and how to start."
lead: "ForgeIEC has become too big to carry alone. This page says where help is wanted, how to start and what a contribution requires."
eyebrow: "For developers and companies"
full: true
---

<section class="band band--tight">
<div class="container">
<div class="split">
<div class="prose-band">
<span class="eyebrow">What it is about</span>

## ForgeIEC in three sentences

ForgeIEC is IEC 61131-3 control software: a Studio for programming, a runtime on industrial Linux and bus bridges (“Tongs”) to the field devices. The Structured Text editor is in use at the pilot customer, the SoLaWi Ackervielfalt; much else is in progress. So far the project has been developed by one person — Jörg Bernau.

</div>
<div class="card">
<p class="card-kicker">In short</p>
<ul>
<li>source code under AGPL-3.0-or-later, access on request</li>
<li>Rust for the runtime and the bridges, C++ with Qt 6 for the Studio</li>
<li>every change passes the same quality gates</li>
<li>third-party contributions only once the CLA is in force</li>
</ul>
</div>
</div>
</div>
</section>

<section class="band band--soft">
<div class="container">
<div class="section-head">
<span class="eyebrow">Where help is wanted</span>

## Open areas

<p>Derived from the open issues of the repositories anvil, forgeiec-studio, hearth-studio and tongs-core and the work plan in tongs-core issue #18 (as of 2026-10-22).</p>
</div>
<div class="grid grid-3">
<div class="card">
<p class="card-kicker">Bus bridges</p>
<h3>One Tongs per protocol</h3>
<p>For EtherCAT, PROFIBUS and EtherNet/IP the skeleton is in place; the protocol-specific part is missing. LoRaWAN is the focus for the SoLaWis. PROFINET is planned as a Tongs in C++ against a Siemens stack.</p>
<div class="chip-row">{{< status "wip" >}} {{< status "plan" "PROFINET: planned" >}}</div>
</div>
<div class="card">
<p class="card-kicker">Studio</p>
<h3>Views per Tongs in QML</h3>
<p>The Studio shows the parameters, diagnosis and bus traffic of every Tongs on a common QML base. The per-protocol files only set titles and labels so far — they deserve groups and views of their own.</p>
<div class="chip-row">{{< status "wip" >}}</div>
</div>
<div class="card">
<p class="card-kicker">Languages</p>
<h3>Graphical editors that compile</h3>
<p>LD, FBD and SFC have editors but are not compiled yet – they are planned for versions 0.3, 0.4 and 0.5 (<a href="/en/roadmap/">roadmap</a>); IL is deprecated. What is needed is the path from the graphical body to code — and clean serialisation to PLCopen XML.</p>
<div class="chip-row">{{< status "wip" >}}</div>
</div>
<div class="card">
<p class="card-kicker">Knowledge</p>
<h3>Documentation and translations</h3>
<p>Help pages, wiki pages and translations of the user interfaces. The website is maintained in German and English; more languages need someone to keep them current.</p>
</div>
<div class="card">
<p class="card-kicker">Hardware</p>
<h3>Test hardware and field tests</h3>
<p>The bus test over real shared memory has so far only run on the development machine, never on a target device (armhf/aarch64). Devices, couplers and people who test in the field are wanted.</p>
</div>
<div class="card">
<p class="card-kicker">Delivery</p>
<h3>Packaging</h3>
<p>The Windows installer, Debian and RPM packages for more distributions and architectures, dependencies and package relations that do not break on upgrade.</p>
</div>
</div>
</div>
</section>

<section class="band">
<div class="container">
<div class="section-head">
<span class="eyebrow">How to start</span>

## From the first contact to the first commit

</div>
<ol class="steps steps--5">
<li><h3>Get in touch</h3><p>A mail to blacksmith@forgeiec.io: who you are, what you can do and which area attracts you.</p></li>
<li><h3>Get access</h3><p>The source code is under AGPL-3.0-or-later; the repositories are not public, access is given on request.</p></li>
<li><h3>Read the wiki</h3><p>The entry point is the page “Architecture”: processes, repositories, the class and dependency tree and “Where do I change what?”.</p></li>
<li><h3>Start from the template</h3><p>The example Tongs <code>tongs-example</code> and the wiki page “Creating a Tongs” show everything a new bridge needs.</p></li>
<li><h3>Pass the gates</h3><p>Every change passes the quality gates; code, commits, issues and the wiki are in English.</p></li>
</ol>
<p class="note-small mt-2">What the quality gates check is described on the page <a href="../engineering/">Engineering practice</a>.</p>
</div>
</section>

<section class="band band--soft">
<div class="container">
<div class="prose-band">
<span class="eyebrow">What a contribution requires</span>

## The Contributor License Agreement

ForgeIEC is offered under AGPL-3.0-or-later and, in addition, under a commercial licence. That is only possible while the author holds all rights in the code. Contributions therefore need a Contributor License Agreement (CLA): you sign once, stay the author of your contribution and grant a non-exclusive right of use. The text: {{< page-link path="/cla" text="Contributor License Agreement" >}}.

<!-- ENTWURF: the CLA is not yet reviewed by a lawyer and not in force; the link above appears only once the CLA page is published (draft removed). -->

{{< callout type="warning" title="Not yet in force" >}}
The CLA is a draft. **Until it is in force, no third-party contributions are accepted.** Bug reports, hints and talks about working together are welcome already.
{{< /callout >}}

</div>
</div>
</section>

<section class="band">
<div class="container">
<div class="section-head">
<span class="eyebrow">Thank you</span>

## Contributors

<p>ForgeIEC stands on the work of others. Listed are the people and projects named in the files AUTHORS, NOTICE, LEGAL/THIRD_PARTY_NOTICES.md and LEGAL/PROVENANCE.md of the Studio repository — with respect and thanks.</p>
</div>
<!-- ENTWURF: list taken from AUTHORS, NOTICE, LEGAL/THIRD_PARTY_NOTICES.md and LEGAL/PROVENANCE.md of the branch licence-cleanup (2026-10-22); update when those files change. -->
<div class="grid grid-2">
<ul class="ack-list">
<li><strong>Jörg Bernau (alias “Blacksmith”)</strong><span>originator, architect and principal author of ForgeIEC</span></li>
<li><strong>OpenPLC v3 — Thiago Alves and contributors</strong><span>origin: ForgeIEC started as a fork of OpenPLC (GPL-3.0); its history is kept in the repository</span></li>
<li><strong>matiec — Edouard Tisserant, Mario de Sousa, Laurent Bessard</strong><span>the original IEC compiler, since replaced by an own core (LGPL)</span></li>
<li><strong>Qt 6 — The Qt Company and contributors</strong><span>the Studio's user interface (LGPL-3.0; Qt Charts GPL-3.0)</span></li>
<li><strong>iceoryx2 — Contributors to the Eclipse Foundation</strong><span>inter-process communication over shared memory (Apache-2.0 or MIT)</span></li>
<li><strong>gRPC — The gRPC Authors; Protocol Buffers — Google LLC</strong><span>connection Studio ⇄ runtime (Apache-2.0; BSD-3-Clause)</span></li>
</ul>
<ul class="ack-list">
<li><strong>tree-sitter — Max Brunsfeld and contributors</strong><span>with the grammars tree-sitter-st (Tyler Matijevich), tree-sitter-md (Matthias Deiml) and tree-sitter-xml (ObserverOfTime), all MIT</span></li>
<li><strong>toml++ — Mark Gillard</strong><span>TOML parser (MIT)</span></li>
<li><strong>libxml2 — Daniel Veillard and contributors; OpenSSL — The OpenSSL Project Authors</strong><span>XSD validation and TLS (MIT; Apache-2.0)</span></li>
<li><strong>marked — Christopher Jeffrey; Mermaid — Knut Sveidqvist and contributors</strong><span>Markdown and diagrams (MIT)</span></li>
<li><strong>async-opcua — Adam Lock and contributors</strong><span>OPC UA stack in the bellows gateway (MPL-2.0)</span></li>
<li><strong>PLCopen</strong><span>the TC6 XML v2.01 schema for validating PLCopen XML files</span></li>
</ul>
</div>
<p class="note-small mt-2">Plus the Rust crates in <code>Cargo.lock</code> under free licences (MIT, Apache-2.0, BSD-3-Clause and others), SQLite and Argon2.</p>
</div>
</section>

<section class="band band--tight">
<div class="container">
<div class="cta-band">
<div>
<h2>What can you contribute?</h2>
<p>Write what you offer: code, hardware, tests, documentation or experience with a bus.</p>
</div>
<div class="btn-row">
<a class="btn btn-primary" href="mailto:blacksmith@forgeiec.io?subject=Contributing%20to%20ForgeIEC">Write a mail</a>
</div>
</div>
</div>
</section>
