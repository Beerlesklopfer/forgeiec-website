---
title: "I am looking for a new role"
linkTitle: "Developer"
url: /en/developer/
description: "Jörg Bernau, developer of ForgeIEC, is looking for a new role: architecture of industrial and embedded software, Rust, C++/Qt 6, IEC 61131-3, field buses, quality culture."
eyebrow: "Developer · Jörg Bernau"
lead: "ForgeIEC is my project – from the compiler architecture to the signed package. Now I am looking for a team where I can bring this experience."
full: true
---
<!-- ENTWURF: CV / career link missing — from the owner -->
<!-- ENTWURF: target role and form (permanent / freelance) missing — from the owner -->

<section class="band band--tight">
<div class="container split">
<div>
<span class="eyebrow">In short</span>
<h2>What I do</h2>
</div>
<div class="prose-band">

I build ForgeIEC as its author and architect: the development environment, the own compiler core for IEC 61131-3, the runtime, the bus bridges and the packages that bring it all to the customer. The project shows how I work – and it has grown so large that I would like to take it further in a team.

Everything on this page is backed by the project. How I go about it is described on [Engineering practice](/en/developer/engineering/); if you want to contribute, see [Contribute](/en/developer/contribute/).

</div>
</div>
</section>

<section class="band band--soft">
<div class="container">
<div class="section-head">
<span class="eyebrow">Technical focus</span>
<h2>What I have worked on</h2>
<p>All of it can be seen in the ForgeIEC repositories; access on request.</p>
</div>
<div class="grid grid-3">
<article class="card">
<p class="card-kicker">Languages</p>
<h3>Rust and C++ with Qt 6</h3>
<p>Runtime, bus bridges and remote access in Rust; the development environment as a native C++ application with Qt 6.</p>
</article>
<article class="card">
<p class="card-kicker">Control engineering</p>
<h3>IEC 61131-3 with an own compiler core</h3>
<p>An own core translates Structured Text to C++ – including the object-oriented extensions of the standard.</p>
</article>
<article class="card">
<p class="card-kicker">Field level</p>
<h3>Industrial buses</h3>
<p>Modbus, EtherCAT, PROFIBUS, EtherNet/IP and LoRaWAN – one bridge per protocol with a shared fault and parameter model.</p>
</article>
<article class="card">
<p class="card-kicker">System architecture</p>
<h3>Processes, shared memory, gRPC</h3>
<p>Inter-process communication over shared memory (iceoryx2); between tool and controller over gRPC and protobuf.</p>
</article>
<article class="card">
<p class="card-kicker">Quality</p>
<h3>CI and quality gates</h3>
<p>Every change has to pass fixed gates; system tests check the installed package; audits separate fact from assumption.</p>
</article>
<article class="card">
<p class="card-kicker">Delivery and law</p>
<h3>Packages, security, licences</h3>
<p>Debian and RPM packages from CI, signed; security documentation under the CRA; a clean boundary between AGPL and Apache-2.0.</p>
</article>
</div>
</div>
</section>

<section class="band">
<div class="container split">
<div>
<span class="eyebrow">In a team</span>
<h2>What I bring to a team</h2>
</div>
<div>
<ul class="facts">
<li>{{< icon "cpu" >}}<div><strong>Architecture of embedded and industrial software</strong><span>Cutting systems so that parts can fail, be tested and be shipped independently.</span></div></li>
<li>{{< icon "shield" >}}<div><strong>Quality culture</strong><span>Rules that are measured rather than claimed: gates, system tests, findings with sources.</span></div></li>
<li>{{< icon "package" >}}<div><strong>From code to customer</strong><span>Build, packaging, signing and documentation as part of development, not as an afterthought.</span></div></li>
</ul>
</div>
</div>
</section>

<section class="band">
<div class="container">
<div class="cta-band">
<div>
<h2>Let's talk.</h2>
<p>Looking for someone for architecture, control or systems software? I look forward to your message at blacksmith@forgeiec.io.</p>
</div>
<div class="btn-row">
<a class="btn btn-primary" href="mailto:blacksmith@forgeiec.io?subject=New%20role">Write an e-mail</a>
<a class="btn btn-secondary" href="/en/developer/engineering/">Engineering practice</a>
</div>
</div>
</div>
</section>
