---
title: "Roadmap"
linkTitle: "Roadmap"
description: "Release-Plan von ForgeIEC: eine IEC-61131-3-Sprache pro Version – 0.2 ST, 0.3 KOP, 0.4 FUP, 0.5 AS. Dazu Anbindung, Rivet, Hearth und Migration."
eyebrow: "Release-Plan"
lead: "Eine IEC-61131-3-Sprache pro Version, in fester Reihenfolge und ohne Datumsversprechen. Was heute läuft, steht oben."
full: true
---

<section class="band band--tight">
<div class="container">
<div class="section-head">
<span class="eyebrow">Sprachen</span>
<h2>Eine Sprache pro Version</h2>
<p>Die Plattform – Studio, Anvil-Server und Tongs – zählt ihre Versionen nach dem Schema <code>0.(2+n).0</code>: Jede neue Minor-Version bringt eine weitere IEC-Sprache. Neue Busse und Fehlerbehebungen kommen als Patch-Versionen <code>0.x.y</code>.</p>
</div>
<ol class="timeline">
<li class="tl-item tl-item--now">
<span class="tl-dot" aria-hidden="true"></span>
<span class="tl-when">Jetzt</span>
<div class="tl-card">
<h3><span class="tl-version">0.2</span> Strukturierter Text (ST)</h3>
<p>Editor, eigener Compiler-Kern und Übertragung auf die Steuerung. Mit Patch 0.2.2 ist der ST-Editor beim Pilotkunden SoLaWi Ackervielfalt produktiv im Einsatz.</p>
{{< status "use" >}}
</div>
</li>
<li class="tl-item tl-item--next">
<span class="tl-dot" aria-hidden="true"></span>
<span class="tl-when">Als Nächstes</span>
<div class="tl-card">
<h3><span class="tl-version">0.3</span> Kontaktplan (KOP / LD)</h3>
<p>Die grafische Sprache der Elektrotechnik. Heute noch nicht übersetzbar.</p>
{{< status "plan" >}}
</div>
</li>
<li class="tl-item">
<span class="tl-dot" aria-hidden="true"></span>
<span class="tl-when">Danach</span>
<div class="tl-card">
<h3><span class="tl-version">0.4</span> Funktionsbausteinsprache (FUP / FBD)</h3>
<p>Bausteine grafisch verschalten. Heute noch nicht übersetzbar.</p>
{{< status "plan" >}}
</div>
</li>
<li class="tl-item">
<span class="tl-dot" aria-hidden="true"></span>
<span class="tl-when">Danach</span>
<div class="tl-card">
<h3><span class="tl-version">0.5</span> SFC (Ablaufsprache / AS)</h3>
<p>Schrittketten mit Schritten und Transitionen – in der Norm ein Satz von Strukturierungselementen. Heute noch nicht übersetzbar.</p>
{{< status "plan" >}}
</div>
</li>
<li class="tl-item tl-item--dropped">
<span class="tl-dot" aria-hidden="true"></span>
<span class="tl-when">Keine Version</span>
<div class="tl-card">
<h3>Anweisungsliste (AWL / IL)</h3>
<p>Nicht mehr Teil der aktuellen Norm – kommt nicht. Warum, steht unten.</p>
{{< status "rest" "abgekündigt" >}}
</div>
</li>
</ol>
</div>
</section>

<section class="band band--soft">
<div class="container">
<div class="section-head">
<span class="eyebrow">Neben den Sprachen</span>
<h2>Anbindung, Fernzugriff, Bedienung, Migration</h2>
<p>Diese Bereiche kommen unabhängig von den Sprach-Versionen.</p>
</div>
<!-- ENTWURF: Satz zu den eigenen Versionsnummern von Rivet und Hearth vom Eigentümer bestätigen lassen. -->
<table class="status-table">
<thead><tr><th scope="col">Bereich</th><th scope="col">Was geplant ist</th><th scope="col">Stand</th></tr></thead>
<tbody>
<tr><td>Anbindung</td><td class="detail">Modbus TCP und RTU verfügbar. LoRaWAN ist unser Schwerpunkt. EtherCAT, PROFIBUS und EtherNet/IP sind in Arbeit; neue Busse kommen als Patch-Versionen.</td><td>{{< status "use" "Modbus verfügbar" >}}</td></tr>
<tr><td>PROFINET</td><td class="detail">In C++ gegen den Siemens-Stack.</td><td>{{< status "plan" >}}</td></tr>
<tr><td>Rivet – Fernzugriff</td><td class="detail">Eigene Versionsnummer (derzeit 0.1.0). Pilot mit SoLaWis.</td><td>{{< status "wip" "in Entwicklung" >}}</td></tr>
<tr><td>Hearth – Bedienoberfläche</td><td class="detail">Eigene Versionsnummer (Hearth Studio derzeit 0.2.0). Läuft über den internen Anvil-Bus.</td><td>{{< status "wip" "Vorschau" >}}</td></tr>
<tr><td>Migration / Import</td><td class="detail">Nativer Import von CODESYS-Projekten (3 und 4). <!-- ENTWURF: genaue CODESYS-Versionen und Dateiformate vom Eigentümer klären --></td><td>{{< status "plan" "geplant, Release offen" >}}</td></tr>
<tr><td>Migration heute</td><td class="detail">Import und Export von PLCopen-XML im Studio (Menü und KI-Werkzeuge).</td><td>{{< status "use" "verfügbar" >}}</td></tr>
<tr><td>Dokumentation im Studio</td><td class="detail">Heute: Dokumentation als Markdown im Projekt, bearbeitbar an Variablen und Datentypen. Geplant: ein Bearbeitungsfeld für POU- und Projekt-Dokumentation, eine funktionierende Dokumentationsansicht mit Export, die Mermaid-Ansicht im Studio mit Daten aus dem Projekt und optional eine Prüfung der Dokumentationsabdeckung durch den KI-Assistenten. <!-- ENTWURF: offene Punkte aus widersprueche/06-doku-im-studio.md (D-1, D-4, D-5, Abdeckungsprüfung); keine Termine --></td><td>{{< status "plan" "geplant" >}}</td></tr>
</tbody>
</table>
</div>
</section>

<section class="band">
<div class="container split">
<div>
<span class="eyebrow">Hintergrund</span>
<h2>Warum AWL nicht kommt</h2>
</div>
<div class="prose-band">

AWL (Anweisungsliste) wurde mit der dritten Ausgabe der IEC 61131-3 (2013) abgekündigt und ist in der aktuellen Ausgabe, IEC 61131-3:2025 (erschienen im Mai 2025), nicht mehr enthalten. ForgeIEC entwickelt sie nicht; sie bräuchte außerdem einen eigenen Übersetzungsweg nach Assembler. <!-- ENTWURF: Annex B der Norm einsehen, bevor es als Normaussage zitiert wird --> Ihr Einsatzgebiet decken Strukturierter Text (textuell) sowie Kontaktplan und Funktionsbausteinsprache (grafisch) ab, ergänzt um die Ablaufsprache als Strukturierungsmittel.

Quellen: [IEC 61131-3:2025, Kurzbeschreibung bei AFNOR](https://www.boutique.afnor.org/en-gb/standard/iec-6113132025/programmable-controllers-part-3-programming-languages/xs304903/444755) · [Stefan Henneken: Vergleich von Edition 3 und Edition 4](https://stefanhenneken.net/2025/06/11/iec-61131-3-comparison-of-edition-3-and-edition-4/) · [Wikipedia: IEC 61131-3](https://en.wikipedia.org/wiki/IEC_61131-3)

Fragen zur Reihenfolge oder zu einem Bus, den Sie brauchen? Schreiben Sie an [blacksmith@forgeiec.io](mailto:blacksmith@forgeiec.io).

</div>
</div>
</section>
