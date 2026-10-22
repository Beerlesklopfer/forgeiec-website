---
title: "Engineering practice"
linkTitle: "Engineering practice"
url: /en/developer/engineering/
description: "How ForgeIEC is built: 13 quality gates, a system test against the installed package, specifications with evidence, signed packages from CI. Every number with its measurement date and source."
lead: "How ForgeIEC is built — with gates every change has to pass and tests that check the shipped package. Every number on this page states when it was measured and where it comes from."
eyebrow: "For CTOs, tech leads and recruiters"
full: true
---

<section class="band band--tight">
<div class="container">
<ul class="stats">
  <li class="stat"><span class="stat-value">13</span><span class="stat-label">quality gates per change</span><span class="stat-source">tongs-core, <code>tools/qm.sh</code>, counted 2026-10-22</span></li>
  <li class="stat"><span class="stat-value">≈&nbsp;96&nbsp;%</span><span class="stat-label">line coverage, gate at 90&nbsp;%</span><span class="stat-source">tongs-core, <code>cargo llvm-cov</code>, measured 2026-10-22</span></li>
  <li class="stat"><span class="stat-value">5</span><span class="stat-label">dependent repositories built on every push</span><span class="stat-source">backward check, <code>.forgejo/workflows/qm.yml</code>, 2026-10-22</span></li>
  <li class="stat"><span class="stat-value">18 + 10</span><span class="stat-label">package slots in the Linux CI (runtime + Studio)</span><span class="stat-source"><code>linux.yml</code> of anvil and the Studio, counted 2026-10-22</span></li>
</ul>
</div>
</section>

<section class="band band--soft">
<div class="container">
<div class="section-head">
<span class="eyebrow">Quality gates</span>

## Thirteen gates, the same locally and in CI

<p>The script <code>tools/qm.sh</code> in the core repository <code>tongs-core</code> runs every gate — on the developer's machine exactly as in CI on every push and pull request. All gates run; a red one does not hide the others. Whoever changes a gate changes it in the script, not in the workflow.</p>
</div>

<div class="table-wrap">
<table class="table gate-table">
<thead><tr><th>Gate</th><th>What it checks</th></tr></thead>
<tbody>
<tr><td>format</td><td>uniform formatting (<code>cargo fmt --all --check</code>)</td></tr>
<tr><td>clippy</td><td>static analysis, every warning is an error (<code>-D warnings</code>)</td></tr>
<tr><td>tests</td><td>all tests of the workspace with all features</td></tr>
<tr><td>docs</td><td>the API documentation builds, warnings are errors</td></tr>
<tr><td>deploy</td><td><code>deploy.sh</code> and <code>deploy.fish</code> equal their templates</td></tr>
<tr><td>machete</td><td>no unused dependency</td></tr>
<tr><td>unsafe</td><td>every crate forbids <code>unsafe</code>; only the Anvil module of <code>tongs-runtime</code> may use it; plus a <code>cargo geiger</code> report</td></tr>
<tr><td>lock</td><td>all <code>iceoryx2</code> packages in <code>Cargo.lock</code> have one version</td></tr>
<tr><td>audit</td><td>known vulnerabilities (RustSec); vulnerabilities fail</td></tr>
<tr><td>deny</td><td>licences, duplicate versions and sources of the dependencies (<code>deny.toml</code>)</td></tr>
<tr><td>msrv</td><td>the code builds with the promised minimum Rust version (1.88)</td></tr>
<tr><td>abdeckung</td><td>line coverage at least 90&nbsp;% (<code>cargo llvm-cov</code>)</td></tr>
<tr><td>rueckwaerts</td><td>every Tongs (bus bridge) still builds against the new state of the core</td></tr>
</tbody>
</table>
</div>
<p class="note-small">Source: <code>tongs-core/tools/qm.sh</code> and <code>README.md</code>, as of 2026-10-22. The two German gate names (coverage, backward) are the names in the script. The tools have pinned versions and come pre-installed in a container image in CI.</p>
</div>
</section>

<section class="band">
<div class="container">
<div class="grid grid-2">
<div class="prose-band">
<span class="eyebrow">Backward check</span>

### A change to the core breaks nothing silently

Five bus bridges build on `tongs-core`: Modbus TCP, Modbus RTU, EtherCAT, EtherNet/IP and PROFIBUS — each in its own repository. The core's CI fetches all five and builds them against the state of the run (`cargo check --locked`). A broken API shows up in the core's pull request, not days later in the next run of a bridge.

</div>
<div class="prose-band">
<span class="eyebrow">Mutation tests</span>

### Checking that the tests check something

Coverage only says which lines a test touches. Mutation tests (`cargo mutants`) change the code on purpose and see whether a test notices. They are too slow for every push — about 1,400 mutants in the workspace — so they run weekly in the night to Sunday and by hand, as a report, not a gate.

<p class="note-small">Source: <code>tongs-core/.forgejo/workflows/qm-nightly.yml</code>, as of 2026-10-22.</p>
</div>
</div>
</div>
</section>

<section class="band band--soft">
<div class="container">
<div class="split">
<div class="prose-band">
<span class="eyebrow">System test</span>

## What is tested is what is shipped

Unit tests check the code in the tree. The system test `tools/system-test.sh` checks the **installed package**: it starts the Anvil server (anvild) from the latest package of the apt repository with an example Tongs — isolated, with its own registry, storage and port, without touching a running service of the machine.

It checks that the master assigns an address, the Tongs comes online, a protocol without a binary is reported, status and process data follow the simulation — and that the Tongs ends by itself when the Anvil server is killed.

</div>
<div class="card example-card">
<p class="card-kicker">Example · tongs-core issue #26</p>
<h3>A Tongs lived on after anvild was killed</h3>
<dl>
<dt>Found</dt><dd>by the system test: after <code>kill -KILL</code> of the Anvil server the Tongs process ran on for 15 seconds and more — without a bus.</dd>
<dt>Cause</dt><dd>The log went through a pipe to the Anvil server. With the server gone the pipe was broken; the log line before terminating failed, and the task that should have ended the process died with it.</dd>
<dt>Fix</dt><dd>Act first, then log; a broken pipe is ignored.</dd>
<dt>Since then</dt><dd>the system test is its regression test. Issue closed.</dd>
</dl>
</div>
</div>
</div>
</section>

<section class="band">
<div class="container">
<div class="section-head">
<span class="eyebrow">Way of working</span>

## Rules that carry the project

<p>A project of this size stays manageable only if every decision can be found — also by someone who joins later.</p>
</div>
<div class="grid grid-3">
<div class="card">
<h3>Specifications with evidence</h3>
<p>Protocols and models live in versioned papers (e.g. <code>tongs-bus-v1</code>, <code>tongs-parameter-v1</code>, <code>diag-model-v1</code>). Where the code differs, the measured state decides; the paper gets a corrections banner at the top and a correction note in place.</p>
</div>
<div class="card">
<h3>Audits with a finding format</h3>
<p>Reviews of papers, contracts and architecture decisions follow a fixed format: <strong>fact</strong> (measured, with the command), <strong>assumption</strong>, <strong>impact</strong> and <strong>what is not the cause</strong>. A review on paper alone is not enough.</p>
</div>
<div class="card">
<h3>The wiki is the entry point</h3>
<p>New developers start with the page “Architecture” of the core wiki: processes, repositories, the crate dependency tree, types and “Where do I change what?”. The wiki describes the current state only, without history.</p>
</div>
<div class="card">
<h3>English in code and process</h3>
<p>Comments, commit messages, issues and wiki pages are in English, so that every developer can follow. The website is available in German and English.</p>
</div>
<div class="card">
<h3>One rule, one place</h3>
<p>Every rule is written down exactly once: a quality gate is changed in <code>qm.sh</code>, not in the CI workflow; the licence boundary lives in <code>LICENSING.md</code>; tool versions in a single file.</p>
</div>
<div class="card">
<h3>Commits with reasons, bugs as issues</h3>
<p>One commit per change, with the why in the message. Every bug found on the way becomes an issue at once — even if it is not fixed right away. Open on 2026-10-22: 65 issues in the Studio, 21 in anvil, 40 in hearth-studio, 3 in tongs-core.</p>
</div>
</div>
</div>
</section>

<section class="band band--soft">
<div class="container">
<div class="grid grid-2">
<div class="prose-band">
<span class="eyebrow">CI and packages</span>

### Signed packages from an automated CI

The runtime (anvil) is built in **18 slots**: Debian 12 and 13, Ubuntu 22.04 and 24.04, each for amd64, aarch64 and armhf, plus AlmaLinux, Rocky Linux and RHEL 8 and 9 for amd64. The Studio in **10 slots**: Debian 12 and 13, Ubuntu 24.04, AlmaLinux 9 and Fedora 44, each for amd64 and aarch64. Packaged as `.deb` and `.rpm`.

The packages are signed and published to `apt.forgeiec.io` and `rpm.forgeiec.io` — see [Download](/en/download/) for installation. The Studio also has a Windows CI with its own Windows runner and an Inno Setup installer.

<p class="note-small">Source: <code>.forgejo/workflows/linux.yml</code> and <code>windows.yml</code> of anvil and the Studio, counted 2026-10-22.</p>
</div>
<div class="prose-band">
<span class="eyebrow">Security and licences</span>

### Documented, not just claimed

For the EU Cyber Resilience Act (CRA) there is a public [security page](/security/cra/) with a `security.txt` per RFC 9116 and a coordinated vulnerability disclosure policy.

The licence situation is measured: a provenance audit of 2026-10-22 checked 2,618 files line by line with `git blame` and records where the code comes from. On the Rust side the `deny` gate checks the licence of every dependency on every push.

</div>
</div>
</div>
</section>

<section class="band">
<div class="container">
<!-- ENTWURF: paragraph "Working with AI tools" — wording to be reviewed by the owner. -->
<div class="prose-band">
<span class="eyebrow">Working with AI tools</span>

## Developed with AI assistance — and checked by measurement

ForgeIEC is developed with AI tools, and the history says so openly: most commits carry a `Co-Authored-By` line. In the Studio repository that is 91&nbsp;% of the author's own commits (1,821 of 1,999 commits by the author on the branch `development` since 2026-02-28, merges included; measured on 2026-10-22).

The author sets the direction, decides, and checks by measurement: quality gates, audits, system tests and reports with sources. What an AI tool contributes is treated like any other contribution — it has to pass the same gates.

</div>
</div>
</section>

<section class="band band--tight">
<div class="container">
<div class="cta-band">
<div>
<h2>More about the developer</h2>
<p>Who is behind ForgeIEC and what kind of role he is looking for.</p>
</div>
<div class="btn-row">
<a class="btn btn-primary" href="../">To the developer profile</a>
<a class="btn btn-secondary" href="mailto:blacksmith@forgeiec.io">blacksmith@forgeiec.io</a>
</div>
</div>
</div>
</section>
