---
title: "Architektur"
eyebrow: "Für technische Leitung"
lead: "Wie ForgeIEC aufgebaut ist: welche Prozesse auf der Steuerung laufen, wie sie Daten austauschen, wie Fehler gemeldet werden — und warum es so gebaut ist."
description: "Architektur von ForgeIEC: Studio, Anvil-Server (anvild), SPS-Zyklus forgeiec_plc, Anvil-Bus auf iceoryx2, Tongs-Bridges je Bussegment, Tongs-Bus als Steuerebene, Fehler- und Parametermodell, Entscheidungen mit Gründen."
full: true
---

<!-- Quellen: tongs-core-Wiki (Zweig main: Architecture, Platform, Tongs-Bus, Runtime, Parameters, Diagnostics),
     Gutachten widersprueche/03-architektur.md (A-03, A-04, A-15), 01-webseite.md (W-15),
     forgeiec-rivet README (Zweig development), Cargo-Beschreibungen in anvil-server/crate-contract und shared. Stand 22.10.2026. -->

<section class="band band--tight">
<div class="container arch">

ForgeIEC trennt drei Aufgaben sauber voneinander: **Programmieren** am Arbeitsplatz, **Ausführen** auf der Steuerung und **Anbinden** der Feldgeräte. Jede Aufgabe läuft in eigenen Prozessen, die über einen gemeinsamen Speicherbus Daten tauschen. Fällt eine Busanbindung aus, läuft der Rest weiter.

<ul class="toc-inline" aria-label="Inhalt dieser Seite">
<li><a href="#ueberblick">Überblick</a></li>
<li><a href="#bausteine">Bausteine und Repositories</a></li>
<li><a href="#crates">Crate-Baum</a></li>
<li><a href="#ebenen">Datenebenen</a></li>
<li><a href="#fehlermodell">Fehlermodell</a></li>
<li><a href="#parameter">Parametermodell</a></li>
<li><a href="#entscheidungen">Entscheidungen</a></li>
<li><a href="#stand">Stand</a></li>
</ul>

</div>
</section>

<section class="band band--soft" id="ueberblick">
<div class="container arch">

<span class="eyebrow">Überblick</span>

## Das System auf einen Blick

Das Studio auf dem Arbeitsplatz spricht über **gRPC** mit dem **Anvil-Server (anvild)** auf der Steuerung. Dort laufen das SPS-Programm, die Busanbindungen und die Bedienoberfläche als getrennte Prozesse; sie tauschen ihre Daten über den **Anvil-Bus**, einen Publish/Subscribe-Bus auf gemeinsamem Speicher (iceoryx2).

{{< figure-svg name="system-overview" caption="Prozesse und Verbindungen. Durchgezogene Pfeile: Daten; farbig: die Steuerebene (Tongs-Bus), auf der nur anvild in eine Tongs schreibt." >}}
Oben links das ForgeIEC Studio auf dem Arbeitsplatz. Es ist über gRPC mit dem Anvil-Server (anvild) auf der Steuerung verbunden. anvild startet den SPS-Zyklus forgeiec_plc als eigenen Prozess. Beide hängen am Anvil-Bus (iceoryx2, gemeinsamer Speicher), auf dem Prozessdaten, Status und Diagnose laufen. Auf demselben Bus liegt der Tongs-Bus als Steuerebene, deren einziger Master anvild ist. Darunter je Bussegment ein Tongs-Prozess (Modbus TCP/RTU, LoRaWAN in Arbeit, weitere) sowie Hearth, die Bedienoberfläche als Vorschau. Die Tongs sprechen mit den Feldgeräten, Hearth liefert Bildschirme an Browser auf Panel oder Tablet. Rechts der Fernzugriff Rivet (in Entwicklung): Ein Gateway im LAN der Steuerung baut nur ausgehende Verbindungen zu einem zentralen Server auf, über den ein Handy mit WireGuard-App die freigegebene Steuerung erreicht.
{{< /figure-svg >}}

- **ForgeIEC Studio** übersetzt das IEC-Programm (Strukturierter Text) in C++-Quelltext und überträgt ihn an die Steuerung.
- **anvild** baut daraus mit `make` und `g++` das Programm **`forgeiec_plc`** und startet es als eigenen Prozess. Er startet und überwacht auch je Bussegment eine **Tongs** (deutsch: *Zange*), eine Brücke zwischen SPS und Feldgeräten.
- **Der Anvil-Bus** verbindet alle Prozesse der Steuerung, ohne die Daten zu kopieren.
- **Der Tongs-Bus** ist die Rückwand von anvild: Adressen, Herzschlag, Parameter und Befehle für die Tongs. Hearth (und das ruhende Gateway bellowsd) lesen dort mit und beauftragen anvild, wenn sie etwas ändern wollen.
- **Hearth** liest die Prozessdaten direkt vom Anvil-Bus; die HMI-Gruppen gibt anvild aus dem Monitorstrom des SPS-Programms heraus. Hearth erzeugt keine Werte, es zeigt sie.
- **Rivet** bringt den Bildschirm der Steuerung sicher aufs Handy, ohne Portfreigabe — mehr auf der [Rivet-Seite](/de/rivet/).

</div>
</section>

<section class="band" id="bausteine">
<div class="container arch">

<span class="eyebrow">Schichten</span>

## Bausteine und Repositories

Jede Schicht hat ihr eigenes Repository. Die Tongs und tongs-core sind Untermodule des Repositorys `anvil` und bauen nur in diesem Baum; alle Teilnehmer am Bus bauen gegen dieselbe iceoryx2-Version wie anvild.

<div class="grid grid-3">
<div class="card">
<p class="card-kicker">Arbeitsplatz</p>
<h3>Studio</h3>
<p>Das Engineering-Werkzeug (C++, Qt 6): ST-Editor, eigener Compilerkern, Buskonfiguration, Diagnose. Spricht nur über gRPC mit der Steuerung.</p>
</div>
<div class="card">
<p class="card-kicker">Steuerung</p>
<h3>anvil</h3>
<p>Der Anvil-Server <code>anvild</code>, der Transport <code>shared/anvil</code> (iceoryx2 mit stabiler C-Schnittstelle für die SPS-Laufzeit) und die Vertrags-Crates. Hält alle Tongs als Untermodule.</p>
</div>
<div class="card">
<p class="card-kicker">Gemeinsame Basis</p>
<h3>tongs-core</h3>
<p>Was alle Tongs teilen: Fehlermodell, Statusformat, Laufzeitrahmen, Tongs-Bus-Protokoll, Parameter- und Diagnosemodell. Eine neue Tongs enthält nur noch ihr Protokoll.</p>
</div>
<div class="card">
<p class="card-kicker">Busanbindung</p>
<h3>Die Tongs</h3>
<p>Je Protokoll ein Repository: <code>tongs-modbustcp</code>, <code>tongs-modbusrtu</code>, <code>tongs-ethercat</code>, <code>tongs-ethernetip</code>, <code>tongs-profibus</code>, dazu <code>tongs-lorawan</code> in Arbeit.</p>
</div>
<div class="card">
<p class="card-kicker">Verträge</p>
<h3>crate-contract und shared</h3>
<p>Eine Quelle der Wahrheit für das, was mehrere Prozesse sprechen: der Codec für IEC-Typen auf dem Draht, der Leser der Variablenbeschreibung, der Befehls-Handshake. <code>shared</code> ist der Anvil-Transport selbst.</p>
</div>
<div class="card">
<p class="card-kicker">Bedienung</p>
<h3>hearth</h3>
<p>Hearth Server (Rust) zeigt Bildschirme im Browser und liest dafür die Anvil-Topics; Hearth Studio ist der Editor dazu. Läuft heute als Vorschau.</p>
</div>
</div>

</div>
</section>

<section class="band band--soft" id="crates">
<div class="container arch">

<span class="eyebrow">Für Entwickler</span>

## Der Crate-Baum von tongs-core

Drei der fünf Crates haben **keinen Zugriff auf Prozesse, Speicher oder Netz**. Sie laufen in Unit-Tests ohne gemeinsamen Speicher — so bleibt das Herz jeder Busanbindung schnell und vollständig testbar.

{{< figure-svg name="crate-tree" caption="Pfeile zeigen von einem Crate zu dem, was es benutzt. Eine Tongs hängt nur an tongs-core und tongs-runtime; tongs-core reicht die Typen der Modell-Crates weiter." >}}
Oben stehen die Tongs-Programme (eigene Repositories) und anvild. Eine Tongs benutzt tongs-runtime und tongs-core. tongs-runtime benutzt tongs-core und anvil, den Transport mit C-Schnittstelle, der wiederum iceoryx2 in Version 0.9.2 benutzt. tongs-core benutzt das Diagnosemodell forge-device-diag und das Parametermodell forge-tongs-params; forge-device-diag benutzt ebenfalls forge-tongs-params. Nur mit dem Cargo-Feature „bus“ benutzt tongs-core zusätzlich das Busprotokoll forgeiec-tongs-bus und anvil. anvild benutzt forgeiec-tongs-bus, anvil und tongs-core. Ohne Ein- und Ausgabe sind forge-device-diag, forge-tongs-params und forgeiec-tongs-bus.
{{< /figure-svg >}}

- **tongs-core**: Zustandsmaschine des Fehlermodells, Statusformat, Wartezeiten, Uhren; mit Feature `bus` die Tongs als Teilnehmer am Tongs-Bus.
- **tongs-runtime**: Kommandozeile, Signale, Konfiguration, Anvil-Anbindung, Statusveröffentlichung, Supervisor. Eine Tongs implementiert genau ein Trait, `Protocol`.
- **forgeiec-tongs-bus**: das Protokoll des Tongs-Bus, *sans-IO*.
- **forge-tongs-params** und **forge-device-diag**: Parameter- und Diagnosemodell; aus dem Diagnosemodell wird der C-Header für das Studio erzeugt, ein Test hält beide gleich.

</div>
</section>

<section class="band" id="ebenen">
<div class="container arch">

<span class="eyebrow">Daten</span>

## Vier Datenebenen auf einem Bus

Prozesswerte, Zustand, Diagnose und Steuerbefehle laufen auf getrennten Topics. **Der Tongs-Bus trägt Adressen, Herzschlag, Parameter und Befehle, nie Prozesswerte** — so stört Verwaltung nie den Zyklus.

{{< figure-svg name="data-planes" caption="Die Topics auf dem Anvil-Bus und ihre Richtung. Der Status kommt auch dann mindestens einmal pro Sekunde, wenn ein Segment keine Geräte hat." >}}
Links das SPS-Programm forgeiec_plc, die Leser (anvild, Hearth, Studio) und anvild als Master; rechts die Tongs, ein Prozess je Segment. Erstens schickt das SPS-Programm seine Ausgänge zyklisch auf Anvil/GROUP an die Tongs. Zweitens kommen die Eingänge von der Tongs auf Anvil/GROUP/bridge zurück. Drittens veröffentlicht die Tongs den Zustand jedes Geräts auf Anvil/status/segment, mindestens einmal pro Sekunde. Viertens veröffentlicht sie die Diagnosewerte aus der Gerätebeschreibung auf Anvil/diag/segment. Fünftens, in beide Richtungen zwischen anvild und den Tongs: der Tongs-Bus auf Anvil/tongsbus für Adressen, Herzschlag, Parameter und Befehle, nie für Prozesswerte.
{{< /figure-svg >}}

Der Statusdatensatz ist binär und hat feste Größe (5152 Byte für bis zu 64 Geräte je Segment). Ein Leser beurteilt die Frische an seiner eigenen Uhr: Ein Datensatz, der älter als drei Sekunden ist, gilt als tote Tongs, ihre Geräte als offline.

</div>
</section>

<section class="band band--soft" id="fehlermodell">
<div class="container arch">

<span class="eyebrow">Zuverlässigkeit</span>

## Das Fehlermodell

**Jede Busanbindung meldet Störungen mit denselben zehn Zuständen** — egal ob Modbus, LoRaWAN oder EtherCAT. Ein SPS-Programm sieht deshalb eine einzige Diagnoseschnittstelle für jedes Protokoll: `xOnline`, `xFault` und `xWarning` je Gerät, dazu Fehlercode und Zähler. Nur in den Zuständen *Online* und *Degraded* sind Werte vertrauenswürdig; *Degraded* heißt online, aber mit einer fehlschlagenden Variable. Dieselbe Klassifikation nutzen der erzeugte SPS-Code, die Anzeige im Studio, Hearth und anvild.

Jedes Gerät hat seinen eigenen Verbindungszustand, seinen eigenen Status und seine eigene Wartezeit; ein nicht erreichbares Gerät hält kein anderes auf, und Gerätetasks teilen sich keine blockierende Sperre. Zustandswechsel gehen nur über eine Funktion, die Übergänge ablehnt, die das Modell nicht kennt. Nach einem Fehler wartet die Tongs exponentiell (1, 2, 4, 8, 16, dann 30 s). Stürzt eine Tongs ab, startet anvild sie mit Wartezeit neu (höchstens 30 s); der Zustand in anvild bleibt davon unberührt.

{{< figure-svg name="fault-model" caption="Die erlaubten Übergänge (tongs_core::can_transition). Ein Gerät, das nie geantwortet hat, ist Unreachable, nicht Timeout." >}}
Start ist Unknown. Von Unknown geht es nach Connecting oder Disabled; von Disabled nach Connecting, sobald das Gerät eingeschaltet wird. Connecting führt nach Online, Unreachable oder ConfigError; ConfigError führt erst nach einem Neuladen der Konfiguration zurück nach Connecting. Online und Degraded wechseln untereinander und führen beide nach Timeout oder Unreachable. Timeout und Unreachable führen nach Backoff, Backoff nach einer Wartezeit von 1, 2, 4, 8, 16, dann 30 Sekunden wieder nach Connecting. Jeder Zustand außer Shutdown führt nach Shutdown, dem Ende.
{{< /figure-svg >}}

</div>
</section>

<section class="band" id="parameter">
<div class="container arch">

<span class="eyebrow">Einstellungen</span>

## Das Parametermodell

**Eine Einstellung wird erst geprüft, dann wirksam, dann gespeichert — und jede Seite prüft mit demselben Code.** Parameter gibt es auf zwei Ebenen: Geräteparameter stammen aus der Gerätebeschreibung (FDD) des Herstellers, eine Tongs erfindet keine eigenen. Segmentparameter sind das, was keine FDD wissen kann — etwa wo ein Funkdienst lauscht oder eine Zykluszeit; die Tongs beschreibt sie selbst und gibt die Beschreibung auch ohne laufenden Prozess aus (`--describe`). Das Studio stellt beides ohne Protokollwissen dar.

Werte sind binär, nach IEC-Typen kodiert und über Nummern adressiert. Ein Schreibzugriff landet zuerst in einem Entwurf; `APPLY` macht ihn wirksam oder lehnt ihn mit Begründung ab, `SAVE` speichert ihn atomar, `DISCARD` verwirft ihn. anvild prüft jeden Wert vor dem Bus genauso, wie die Tongs ihn prüfen wird, und nennt jeden abgelehnten. Geheime Werte werden nie zurückgelesen, nur ob sie gesetzt sind und ein Fingerabdruck; über den Bus schreibt anvild sie heute nicht, weil dessen Verschlüsselung noch nicht gebaut ist — sie kommen aus dem Projekt.

</div>
</section>

<section class="band band--soft" id="entscheidungen">
<div class="container arch">

<span class="eyebrow">Warum so</span>

## Entscheidungen und ihre Gründe

<div class="grid grid-2">
<div class="card decision">
<p class="card-kicker">Prozess je Bussegment</p>
<h3>Eine Tongs pro Segment statt eines großen Daemons</h3>
<p class="why">Ein hängendes oder abstürzendes Protokoll reißt weder die SPS noch andere Busse mit. anvild startet die Tongs neu; jede kann einzeln neu laden (SIGHUP) und endet geordnet (SIGTERM, binnen fünf Sekunden).</p>
</div>
<div class="card decision">
<p class="card-kicker">Steuerebene</p>
<h3>Typisierte Binärdatensätze statt JSON</h3>
<p class="why">Jedes Register hat ein festes Layout aus IEC-Typen; kein JSON, kein XML. Der Master braucht keinen Parser, Telegramme passen in Rahmen von 512 Byte, und ein fehlerhafter Schreibzugriff wird sofort abgelehnt. Über die gRPC-Schnittstelle zum Studio laufen ebenfalls typisierte Nachrichten.</p>
</div>
<div class="card decision">
<p class="card-kicker">Testbarkeit</p>
<h3>Protokollkern ohne Ein- und Ausgabe</h3>
<p class="why">Das Busprotokoll ist <em>sans-IO</em>: Rahmen und Zeit gehen hinein, Rahmen und Ereignisse kommen heraus. Damit läuft es in Tests auf einer simulierten, auch verlustbehafteten Leitung — ohne gemeinsamen Speicher, ohne Netz.</p>
</div>
<div class="card decision">
<p class="card-kicker">Eindeutige Zuständigkeit</p>
<h3>Ein Master pro Maschine</h3>
<p class="why">Nur anvild schreibt in eine Tongs; jeder andere Schreibversuch wird abgewiesen. Eine Tongs braucht deshalb keine Rechteliste. Hört ein Master beim Start einen zweiten, verlässt er den Bus und anvild beendet sich.</p>
</div>
<div class="card decision">
<p class="card-kicker">Lebenszeit</p>
<h3>Die Bridges enden mit dem Master</h3>
<p class="why">SPS-Programm und Tongs enden mit anvild; ohne Herzschlag (Vorgabe 3 s) muss eine Tongs sich beenden. Die Feldgeräte gehen über ihre eigene Überwachung in den sicheren Zustand. Die Regel gilt für Tongs am Tongs-Bus; die vorhandenen Protokoll-Tongs nutzen ihn noch nicht (Stand 22.10.2026).</p>
</div>
<div class="card decision">
<p class="card-kicker">Abtastung</p>
<h3>Höchstens halb so lang wie der Systemzyklus</h3>
<p class="why">Damit ein Signal ohne Aliasing erfasst wird, darf die Abfrageperiode höchstens 0,5 × Systemzyklus betragen. Die erreichte Periode wird gemessen, nicht angenommen: anvild berechnet je Gerät Mittelwert, Schwankung und Überläufe und meldet Verstöße.</p>
</div>
</div>

Zur Sicherheit auf der Maschine: Der Anvil-Transport lässt nur Prozesse der Benutzergruppe von anvild zu. Das ist der äußere Zaun, keine Berechtigung; die Authentifizierung privilegierter Schreibzugriffe auf dem Tongs-Bus ist spezifiziert, aber noch nicht gebaut. ForgeIEC ersetzt keine Sicherheitssteuerung (kein SIL/PL).

</div>
</section>

<section class="band" id="stand">
<div class="container arch">

<span class="eyebrow">Ehrlicher Stand</span>

## Was heute läuft

<div class="table-wrap">
<table class="status-table">
<thead><tr><th>Baustein</th><th>Stand im Detail</th><th>Status</th></tr></thead>
<tbody>
<tr><td>ST-Editor, Compilerkern, anvild, forgeiec_plc</td><td class="detail">Vorabversion 0.2, im Pilotbetrieb bei der SoLaWi Ackervielfalt</td><td>{{< status "use" >}}</td></tr>
<tr><td>Modbus TCP / RTU</td><td class="detail">Bridges für beide Varianten</td><td>{{< status "use" "verfügbar" >}}</td></tr>
<tr><td>LoRaWAN</td><td class="detail">Schwerpunkt für die SoLaWis</td><td>{{< status "wip" >}}</td></tr>
<tr><td>EtherCAT, PROFIBUS, EtherNet/IP</td><td class="detail">Gerüst mit Fehlermodell und Anbindung, Protokollteil folgt</td><td>{{< status "wip" >}}</td></tr>
<tr><td>Hearth (Bedienung)</td><td class="detail">über den Anvil-Bus, als Vorschau</td><td>{{< status "wip" "Vorschau" >}}</td></tr>
<tr><td>Rivet (Fernzugriff)</td><td class="detail">in Entwicklung, Pilot mit SoLaWis</td><td>{{< status "wip" >}}</td></tr>
<tr><td>bellowsd (HMI/OPC-UA-Gateway)</td><td class="detail">derzeit nicht in Entwicklung</td><td>{{< status "rest" >}}</td></tr>
</tbody>
</table>
</div>

Quellcode unter AGPL-3.0-or-later; Einblick auf Anfrage. Die Entwickler-Dokumentation (Wiki von tongs-core mit Architektur, Abhängigkeitsbaum und „Wo ändere ich was“) ist noch nicht öffentlich — Zugang ebenfalls auf Anfrage an [blacksmith@forgeiec.io](mailto:blacksmith@forgeiec.io).

</div>
</section>
