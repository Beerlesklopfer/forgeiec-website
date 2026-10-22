---
title: "Engineering-Praxis"
linkTitle: "Engineering-Praxis"
description: "Wie ForgeIEC gebaut wird: 13 Qualitätstore, Systemtest gegen das installierte Paket, Spezifikationen mit Belegen, signierte Pakete aus der CI. Jede Zahl mit Messdatum und Quelle."
lead: "Wie ForgeIEC gebaut wird — mit Toren, die jede Änderung bestehen muss, und Tests, die das ausgelieferte Paket prüfen. Jede Zahl auf dieser Seite nennt ihr Messdatum und ihre Quelle."
eyebrow: "Für CTOs, Tech-Leads und Recruiter"
full: true
---

<section class="band band--tight">
<div class="container">
<ul class="stats">
  <li class="stat"><span class="stat-value">13</span><span class="stat-label">Qualitätstore je Änderung</span><span class="stat-source">tongs-core, <code>tools/qm.sh</code>, gezählt am 22.10.2026</span></li>
  <li class="stat"><span class="stat-value">≈&nbsp;96&nbsp;%</span><span class="stat-label">Zeilenabdeckung, Tor ab 90&nbsp;%</span><span class="stat-source">tongs-core, <code>cargo llvm-cov</code>, gemessen 22.10.2026</span></li>
  <li class="stat"><span class="stat-value">5</span><span class="stat-label">abhängige Repositories bei jedem Push mitgebaut</span><span class="stat-source">Rückwärtsprüfung, <code>.forgejo/workflows/qm.yml</code>, 22.10.2026</span></li>
  <li class="stat"><span class="stat-value">18 + 10</span><span class="stat-label">Paket-Slots in der Linux-CI (Runtime + Studio)</span><span class="stat-source"><code>linux.yml</code> von anvil und Studio, gezählt 22.10.2026</span></li>
</ul>
</div>
</section>

<section class="band band--soft">
<div class="container">
<div class="section-head">
<span class="eyebrow">Qualitätstore</span>

## Dreizehn Tore, lokal und in der CI dieselben

<p>Das Skript <code>tools/qm.sh</code> im Kern-Repository <code>tongs-core</code> führt alle Tore aus — auf dem Entwicklerrechner genauso wie in der CI bei jedem Push und jedem Pull-Request. Alle Tore laufen durch; ein rotes verdeckt die anderen nicht. Wer ein Tor ändert, ändert es im Skript, nicht im Workflow.</p>
</div>

<div class="table-wrap">
<table class="table gate-table">
<thead><tr><th>Tor</th><th>Was es prüft</th></tr></thead>
<tbody>
<tr><td>format</td><td>einheitliche Formatierung (<code>cargo fmt --all --check</code>)</td></tr>
<tr><td>clippy</td><td>statische Analyse, jede Warnung ist ein Fehler (<code>-D warnings</code>)</td></tr>
<tr><td>tests</td><td>alle Tests des Arbeitsbereichs mit allen Features</td></tr>
<tr><td>docs</td><td>API-Dokumentation baut, Warnungen sind Fehler</td></tr>
<tr><td>deploy</td><td><code>deploy.sh</code> und <code>deploy.fish</code> gleichen den Vorlagen</td></tr>
<tr><td>machete</td><td>keine ungenutzte Abhängigkeit</td></tr>
<tr><td>unsafe</td><td>jede Crate verbietet <code>unsafe</code>; nur das Anvil-Modul von <code>tongs-runtime</code> darf es; dazu ein <code>cargo geiger</code>-Bericht</td></tr>
<tr><td>lock</td><td>alle <code>iceoryx2</code>-Pakete in <code>Cargo.lock</code> tragen dieselbe Version</td></tr>
<tr><td>audit</td><td>bekannte Sicherheitslücken (RustSec); Lücken sind Fehler</td></tr>
<tr><td>deny</td><td>Lizenzen, doppelte Versionen und Quellen der Abhängigkeiten (<code>deny.toml</code>)</td></tr>
<tr><td>msrv</td><td>der Code baut mit der zugesagten Mindestversion von Rust (1.88)</td></tr>
<tr><td>abdeckung</td><td>Zeilenabdeckung mindestens 90&nbsp;% (<code>cargo llvm-cov</code>)</td></tr>
<tr><td>rueckwaerts</td><td>jede Zange (Bus-Brücke) baut noch gegen den neuen Stand des Kerns</td></tr>
</tbody>
</table>
</div>
<p class="note-small">Quelle: <code>tongs-core/tools/qm.sh</code> und <code>README.md</code>, Stand 22.10.2026. Die Werkzeuge haben feste Versionen und liegen in der CI in einem vorgebauten Container-Image.</p>
</div>
</section>

<section class="band">
<div class="container">
<div class="grid grid-2">
<div class="prose-band">
<span class="eyebrow">Rückwärtsprüfung</span>

### Eine Änderung am Kern bricht nichts still

Auf `tongs-core` bauen fünf Bus-Brücken auf: Modbus TCP, Modbus RTU, EtherCAT, EtherNet/IP und PROFIBUS — jede in einem eigenen Repository. Die CI des Kerns holt alle fünf und baut sie gegen den Stand des Laufs (`cargo check --locked`). Ein API-Bruch zeigt sich im Pull-Request des Kerns, nicht Tage später im nächsten Lauf einer Brücke.

</div>
<div class="prose-band">
<span class="eyebrow">Mutationstests</span>

### Prüfen, ob die Tests etwas prüfen

Abdeckung sagt nur, welche Zeilen ein Test berührt. Mutationstests (`cargo mutants`) verändern den Code gezielt und schauen, ob ein Test das bemerkt. Für jeden Push sind sie zu langsam — rund 1 400 Mutanten im Arbeitsbereich —, deshalb laufen sie wöchentlich in der Nacht auf Sonntag und von Hand, als Bericht, nicht als Tor.

<p class="note-small">Quelle: <code>tongs-core/.forgejo/workflows/qm-nightly.yml</code>, Stand 22.10.2026.</p>
</div>
</div>
</div>
</section>

<section class="band band--soft">
<div class="container">
<div class="split">
<div class="prose-band">
<span class="eyebrow">Systemtest</span>

## Getestet wird das, was ausgeliefert wird

Unit-Tests prüfen den Code im Baum. Der Systemtest `tools/system-test.sh` prüft das **installierte Paket**: Er startet den Anvil-Server (anvild) aus dem neuesten Paket des apt-Repositorys mit einer Beispiel-Zange — isoliert, mit eigener Registry, eigenem Speicher und eigenem Port, ohne einen laufenden Dienst der Maschine zu berühren.

Geprüft wird: Der Master vergibt eine Adresse, die Zange meldet sich online, ein Protokoll ohne Programm wird gemeldet, Status und Prozessdaten folgen der Simulation — und die Zange beendet sich selbst, wenn der Anvil-Server getötet wird.

</div>
<div class="card example-card">
<p class="card-kicker">Beispiel · tongs-core Issue #26</p>
<h3>Eine Zange lebte weiter, nachdem anvild getötet war</h3>
<dl>
<dt>Gefunden</dt><dd>vom Systemtest: Nach <code>kill -KILL</code> des Anvil-Servers lief der Prozess der Zange 15 Sekunden und länger weiter — ohne Bus.</dd>
<dt>Ursache</dt><dd>Das Log lief über eine Pipe zum Anvil-Server. Mit ihm war die Pipe tot; die Log-Zeile vor dem Beenden schlug fehl, und die Aufgabe, die das Beenden auslösen sollte, starb mit.</dd>
<dt>Behebung</dt><dd>Erst handeln, dann loggen; eine gebrochene Pipe wird ignoriert.</dd>
<dt>Seitdem</dt><dd>ist der Systemtest der Regressionstest dafür. Issue geschlossen.</dd>
</dl>
</div>
</div>
</div>
</section>

<section class="band">
<div class="container">
<div class="section-head">
<span class="eyebrow">Arbeitsweise</span>

## Regeln, die das Projekt tragen

<p>Ein Projekt dieser Größe bleibt nur beherrschbar, wenn jede Entscheidung auffindbar ist — auch für jemanden, der neu dazukommt.</p>
</div>
<div class="grid grid-3">
<div class="card">
<h3>Spezifikationen mit Belegen</h3>
<p>Protokolle und Modelle stehen in versionierten Papieren (z.&nbsp;B. <code>tongs-bus-v1</code>, <code>tongs-parameter-v1</code>, <code>diag-model-v1</code>). Weicht der Code ab, entscheidet der gemessene Stand; das Papier bekommt einen Korrektur-Kasten oben und eine Korrekturnotiz an der Stelle.</p>
</div>
<div class="card">
<h3>Gutachten mit Befundformat</h3>
<p>Prüfungen von Papieren, Verträgen und Architekturentscheidungen folgen einem festen Format: <strong>Fakt</strong> (gemessen, mit Befehl), <strong>Annahme</strong>, <strong>Auswirkung</strong> und <strong>was nicht die Ursache ist</strong>. Eine reine Papierprüfung genügt nicht.</p>
</div>
<div class="card">
<h3>Das Wiki ist der Einstieg</h3>
<p>Neue Entwickler beginnen mit der Seite „Architecture“ des Kern-Wikis: Prozesse, Repositories, Abhängigkeitsbaum der Crates, Typen und „Where do I change what?“. Das Wiki beschreibt nur den aktuellen Stand, ohne Historie.</p>
</div>
<div class="card">
<h3>Englisch in Code und Prozess</h3>
<p>Kommentare, Commit-Nachrichten, Issues und Wiki-Seiten sind englisch — damit jede Entwicklerin und jeder Entwickler mitlesen kann. Die Webseite gibt es auf Deutsch und Englisch.</p>
</div>
<div class="card">
<h3>Eine Regel, ein Ort</h3>
<p>Jede Regel steht genau einmal: Ein Qualitätstor wird in <code>qm.sh</code> geändert, nicht im CI-Workflow; die Lizenzgrenze steht in <code>LICENSING.md</code>; Werkzeugversionen in einer einzigen Datei.</p>
</div>
<div class="card">
<h3>Commits mit Begründung, Fehler als Issue</h3>
<p>Ein Commit je Änderung, mit dem Warum im Text. Jeder unterwegs gefundene Fehler wird sofort ein Issue — auch wenn er nicht gleich behoben wird. Offen am 22.10.2026: 65 Issues im Studio, 21 in anvil, 40 in hearth-studio, 3 in tongs-core.</p>
</div>
</div>
</div>
</section>

<section class="band band--soft">
<div class="container">
<div class="grid grid-2">
<div class="prose-band">
<span class="eyebrow">CI und Pakete</span>

### Signierte Pakete aus einer automatisierten CI

Die Runtime (anvil) wird in **18 Slots** gebaut: Debian 12 und 13, Ubuntu 22.04 und 24.04 je für amd64, aarch64 und armhf, dazu AlmaLinux, Rocky Linux und RHEL 8 und 9 für amd64. Das Studio in **10 Slots**: Debian 12 und 13, Ubuntu 24.04, AlmaLinux 9 und Fedora 44 je für amd64 und aarch64. Gepackt wird als `.deb` und `.rpm`.

Die Pakete kommen signiert in die Repositories `apt.forgeiec.io` und `rpm.forgeiec.io` — Installation siehe [Download](/de/download/). Für das Studio gibt es zusätzlich eine Windows-CI mit eigenem Windows-Runner und Inno-Setup-Installer.

<p class="note-small">Quelle: <code>.forgejo/workflows/linux.yml</code> und <code>windows.yml</code> von anvil und Studio, gezählt am 22.10.2026.</p>
</div>
<div class="prose-band">
<span class="eyebrow">Sicherheit und Lizenzen</span>

### Dokumentiert, nicht nur behauptet

Für die EU-Cyberresilienzverordnung (CRA) gibt es eine öffentliche [Sicherheitsseite](/security/cra/) mit `security.txt` nach RFC 9116 und einer Richtlinie zur koordinierten Offenlegung von Schwachstellen.

Die Lizenzlage wird gemessen: Ein Provenienz-Audit vom 22.10.2026 hat 2 618 Dateien zeilenweise per `git blame` geprüft und hält fest, woher der Code stammt. In der Rust-Welt prüft das Tor `deny` die Lizenzen jeder Abhängigkeit bei jedem Push.

</div>
</div>
</div>
</section>

<section class="band">
<div class="container">
<!-- ENTWURF: Absatz „Arbeit mit KI-Werkzeugen“ — Wortlaut vom Eigentümer prüfen lassen. -->
<div class="prose-band">
<span class="eyebrow">Arbeit mit KI-Werkzeugen</span>

## KI-gestützt entwickelt — und gemessen geprüft

ForgeIEC wird mit KI-Werkzeugen entwickelt, und das steht offen in der Historie: Die meisten Commits tragen eine `Co-Authored-By`-Zeile. Im Studio-Repository sind es 91&nbsp;% der eigenen Commits (1 821 von 1 999 Commits des Autors auf dem Zweig `development` seit dem 28.02.2026, Merges eingeschlossen; gemessen am 22.10.2026).

Der Autor gibt die Richtung vor, entscheidet und prüft durch Messung: Qualitätstore, Gutachten, Systemtests und Berichte mit Quellenangaben. Was ein KI-Werkzeug beiträgt, wird behandelt wie jeder andere Beitrag — es muss dieselben Tore bestehen.

</div>
</div>
</section>

<section class="band band--tight">
<div class="container">
<div class="cta-band">
<div>
<h2>Mehr über den Entwickler</h2>
<p>Wer hinter ForgeIEC steht und welche Aufgabe er sucht.</p>
</div>
<div class="btn-row">
<a class="btn btn-primary" href="../">Zum Entwickler-Profil</a>
<a class="btn btn-secondary" href="mailto:blacksmith@forgeiec.io">blacksmith@forgeiec.io</a>
</div>
</div>
</div>
</section>
