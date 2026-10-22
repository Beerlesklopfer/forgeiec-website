---
title: "Mitmachen"
linkTitle: "Mitmachen"
description: "ForgeIEC ist zu groß geworden, um es allein zu tragen. Wo Hilfe gebraucht wird — Bus-Brücken, grafische Editoren, Dokumentation, Testhardware, Paketbau — und wie man anfängt."
lead: "ForgeIEC ist zu groß geworden, um es allein zu tragen. Hier steht, wo Hilfe gebraucht wird, wie man anfängt und was ein Beitrag voraussetzt."
eyebrow: "Für Entwicklerinnen, Entwickler und Firmen"
full: true
---

<section class="band band--tight">
<div class="container">
<div class="split">
<div class="prose-band">
<span class="eyebrow">Worum es geht</span>

## ForgeIEC in drei Sätzen

ForgeIEC ist Steuerungssoftware nach IEC 61131-3: ein Studio zum Programmieren, eine Runtime auf Industrie-Linux und Bus-Brücken („Zangen“, englisch *Tongs*) zu den Feldgeräten. Der Strukturierte-Text-Editor ist beim Pilotkunden, der SoLaWi Ackervielfalt, im Einsatz; vieles andere ist in Arbeit. Entwickelt wird das Projekt bisher von einer Person — Jörg Bernau.

</div>
<div class="card">
<p class="card-kicker">Kurz gesagt</p>
<ul>
<li>Quellcode unter AGPL-3.0-or-later, Zugang auf Anfrage</li>
<li>Rust für Runtime und Brücken, C++ mit Qt 6 für das Studio</li>
<li>jede Änderung besteht dieselben Qualitätstore</li>
<li>Beiträge Dritter erst, wenn die CLA in Kraft ist</li>
</ul>
</div>
</div>
</div>
</section>

<section class="band band--soft">
<div class="container">
<div class="section-head">
<span class="eyebrow">Wo Hilfe gebraucht wird</span>

## Offene Bereiche

<p>Abgeleitet aus den offenen Issues der Repositories anvil, forgeiec-studio, hearth-studio und tongs-core und dem Arbeitsplan in tongs-core Issue #18 (Stand 22.10.2026).</p>
</div>
<div class="grid grid-3">
<div class="card">
<p class="card-kicker">Bus-Brücken</p>
<h3>Eine Zange je Protokoll</h3>
<p>Für EtherCAT, PROFIBUS und EtherNet/IP steht das Gerüst; der protokollspezifische Teil fehlt. LoRaWAN ist der Schwerpunkt für die SoLaWis. PROFINET ist als Zange in C++ gegen einen Siemens-Stack geplant.</p>
<div class="chip-row">{{< status "wip" >}} {{< status "plan" "PROFINET: geplant" >}}</div>
</div>
<div class="card">
<p class="card-kicker">Studio</p>
<h3>Ansichten je Zange in QML</h3>
<p>Das Studio zeigt Parameter, Diagnose und Busverkehr jeder Zange auf einer gemeinsamen QML-Basis. Die Dateien je Protokoll setzen bisher nur Titel und Beschriftungen — sie verdienen eigene Gruppen und Ansichten.</p>
<div class="chip-row">{{< status "wip" >}}</div>
</div>
<div class="card">
<p class="card-kicker">Sprachen</p>
<h3>Grafische Editoren, die übersetzen</h3>
<p>FBD, LD, SFC und IL haben Editoren, werden aber noch nicht übersetzt. Gebraucht wird der Weg vom grafischen Rumpf zum Code — und saubere Serialisierung nach PLCopen XML.</p>
<div class="chip-row">{{< status "wip" >}}</div>
</div>
<div class="card">
<p class="card-kicker">Wissen</p>
<h3>Dokumentation und Übersetzungen</h3>
<p>Hilfeseiten, Wiki-Seiten und Übersetzungen der Oberflächen. Die Webseite wird auf Deutsch und Englisch gepflegt; weitere Sprachen brauchen jemanden, der sie aktuell hält.</p>
</div>
<div class="card">
<p class="card-kicker">Hardware</p>
<h3>Testhardware und Feldtests</h3>
<p>Der Bustest über echten Shared Memory lief bisher nur auf dem Entwicklungsrechner, nie auf einem Zielgerät (armhf/aarch64). Gebraucht werden Geräte, Koppler und Menschen, die im Feld testen.</p>
</div>
<div class="card">
<p class="card-kicker">Auslieferung</p>
<h3>Paketbau</h3>
<p>Windows-Installer, Debian- und RPM-Pakete für weitere Distributionen und Architekturen, Abhängigkeiten und Paketbeziehungen, die beim Aktualisieren nicht brechen.</p>
</div>
</div>
</div>
</section>

<section class="band">
<div class="container">
<div class="section-head">
<span class="eyebrow">Wie man anfängt</span>

## Vom ersten Kontakt zum ersten Commit

</div>
<ol class="steps steps--5">
<li><h3>Melden</h3><p>Eine Mail an blacksmith@forgeiec.io: wer Sie sind, was Sie können und welcher Bereich Sie reizt.</p></li>
<li><h3>Zugang erhalten</h3><p>Der Quellcode steht unter AGPL-3.0-or-later; die Repositories sind nicht öffentlich, Zugang gibt es auf Anfrage.</p></li>
<li><h3>Das Wiki lesen</h3><p>Einstieg ist die Seite „Architecture“: Prozesse, Repositories, Klassen- und Abhängigkeitsbaum und „Where do I change what?“.</p></li>
<li><h3>Mit der Vorlage beginnen</h3><p>Die Beispiel-Zange <code>tongs-example</code> und die Wiki-Seite „Creating a Tongs“ zeigen alles, was eine neue Brücke braucht.</p></li>
<li><h3>Die Tore bestehen</h3><p>Jede Änderung besteht die Qualitätstore; Code, Commits, Issues und Wiki sind englisch.</p></li>
</ol>
<p class="note-small mt-2">Was die Qualitätstore prüfen, steht auf der Seite <a href="../engineering-praxis/">Engineering-Praxis</a>.</p>
</div>
</section>

<section class="band band--soft">
<div class="container">
<div class="prose-band">
<span class="eyebrow">Was ein Beitrag voraussetzt</span>

## Die Contributor License Agreement

ForgeIEC wird unter AGPL-3.0-or-later und zusätzlich unter einer kommerziellen Lizenz angeboten. Das geht nur, solange alle Rechte am Code beim Autor liegen. Beiträge brauchen deshalb eine Contributor License Agreement (CLA): Sie unterschreiben einmal, bleiben Urheber Ihres Beitrags und räumen ein einfaches Nutzungsrecht ein. Den Text finden Sie unter {{< page-link path="/cla" text="Contributor License Agreement" >}}.

<!-- ENTWURF: Die CLA ist noch nicht anwaltlich geprüft und nicht in Kraft; der Link oben erscheint erst, wenn die CLA-Seite veröffentlicht ist (draft entfernt). -->

{{< callout type="warning" title="Noch nicht in Kraft" >}}
Die CLA ist ein Entwurf. **Solange sie nicht in Kraft ist, werden keine Beiträge Dritter angenommen.** Fehlerberichte, Hinweise und Gespräche über eine Zusammenarbeit sind schon jetzt willkommen.
{{< /callout >}}

</div>
</div>
</section>

<section class="band">
<div class="container">
<div class="section-head">
<span class="eyebrow">Danke</span>

## Wer bisher beigetragen hat

<p>ForgeIEC steht auf der Arbeit anderer. Genannt sind die Personen und Projekte aus den Dateien AUTHORS, NOTICE, LEGAL/THIRD_PARTY_NOTICES.md und LEGAL/PROVENANCE.md des Studio-Repositorys — mit Respekt und Dank.</p>
</div>
<!-- ENTWURF: Liste aus AUTHORS, NOTICE, LEGAL/THIRD_PARTY_NOTICES.md und LEGAL/PROVENANCE.md des Zweigs licence-cleanup (22.10.2026); bei Änderungen dieser Dateien nachziehen. -->
<div class="grid grid-2">
<ul class="ack-list">
<li><strong>Jörg Bernau (alias „Blacksmith“)</strong><span>Urheber, Architekt und Hauptautor von ForgeIEC</span></li>
<li><strong>OpenPLC v3 — Thiago Alves und Mitwirkende</strong><span>Ursprung: ForgeIEC begann als Fork von OpenPLC (GPL-3.0); die Historie ist im Repository erhalten</span></li>
<li><strong>matiec — Edouard Tisserant, Mario de Sousa, Laurent Bessard</strong><span>der ursprüngliche IEC-Compiler, inzwischen durch einen eigenen Kern ersetzt (LGPL)</span></li>
<li><strong>Qt 6 — The Qt Company und Mitwirkende</strong><span>Oberfläche des Studios (LGPL-3.0; Qt Charts GPL-3.0)</span></li>
<li><strong>iceoryx2 — Contributors to the Eclipse Foundation</strong><span>Interprozesskommunikation über Shared Memory (Apache-2.0 oder MIT)</span></li>
<li><strong>gRPC — The gRPC Authors; Protocol Buffers — Google LLC</strong><span>Verbindung Studio ⇄ Runtime (Apache-2.0; BSD-3-Clause)</span></li>
</ul>
<ul class="ack-list">
<li><strong>tree-sitter — Max Brunsfeld und Mitwirkende</strong><span>mit den Grammatiken tree-sitter-st (Tyler Matijevich), tree-sitter-md (Matthias Deiml) und tree-sitter-xml (ObserverOfTime), alle MIT</span></li>
<li><strong>toml++ — Mark Gillard</strong><span>TOML-Parser (MIT)</span></li>
<li><strong>libxml2 — Daniel Veillard und Mitwirkende; OpenSSL — The OpenSSL Project Authors</strong><span>XSD-Prüfung und TLS (MIT; Apache-2.0)</span></li>
<li><strong>marked — Christopher Jeffrey; Mermaid — Knut Sveidqvist und Mitwirkende</strong><span>Markdown und Diagramme (MIT)</span></li>
<li><strong>async-opcua — Adam Lock und Mitwirkende</strong><span>OPC-UA-Stack im Gateway bellows (MPL-2.0)</span></li>
<li><strong>PLCopen</strong><span>das Schema TC6 XML v2.01 zur Prüfung von PLCopen-XML-Dateien</span></li>
</ul>
</div>
<p class="note-small mt-2">Dazu kommen die Rust-Crates aus <code>Cargo.lock</code> unter freien Lizenzen (MIT, Apache-2.0, BSD-3-Clause u.&nbsp;a.) sowie SQLite und Argon2.</p>
</div>
</section>

<section class="band band--tight">
<div class="container">
<div class="cta-band">
<div>
<h2>Was können Sie beitragen?</h2>
<p>Schreiben Sie, was Sie anbieten: Code, Hardware, Tests, Dokumentation oder Erfahrung mit einem Bus.</p>
</div>
<div class="btn-row">
<a class="btn btn-primary" href="mailto:blacksmith@forgeiec.io?subject=Mitmachen%20bei%20ForgeIEC">Mail schreiben</a>
</div>
</div>
</div>
</section>
