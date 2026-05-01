---
title: "Einstellungen (Preferences)"
summary: "Zentraler Konfigurationsdialog des Editors: Editor, Runtime, PLC, AI Assistant"
---

## Ueberblick

Der **Preferences-Dialog** ist die zentrale Anlaufstelle fuer alle
editor-globalen Einstellungen — alles, was nicht zum geoeffneten Projekt
gehoert, sondern den Editor selbst, die Verbindung zu einer Runtime und
das Verhalten beim Upload betrifft.

Geoeffnet wird der Dialog ueber **`Edit > Preferences...`** (in einigen
Themes auch unter `Tools > Preferences...`). Druecken Sie **F1** im
Dialog, um direkt diese Seite zu oeffnen.

```
Preferences
+-- Editor          (Schrift, Tab-Breite, Zeilennummern)
+-- Runtime         (anvild-Host/Port, Anvil Debug, Network Scanner)
+-- PLC             (Build-Mode, Auto-Start, Persist, Monitoring)
+-- AI Assistant    (LLM-Endpoint, Tokens, Temperature)
```

## Editor

Steuert die Darstellung im ST-Code-Editor und in allen anderen
Text-Eingabe-Feldern.

| Feld | Bedeutung |
|---|---|
| **Font**         | Schriftfamilie. Vorgefiltert auf monospace-Schriften (Empfehlung: `JetBrains Mono`, `Cascadia Code`, `Consolas`). |
| **Font size**    | Schriftgroesse in Punkt. Default `10`. |
| **Tab width**    | Anzahl Leerzeichen pro Tab-Stop. Default `4`. |
| **Show line numbers** | Zeigt links neben dem Code-Editor laufende Zeilennummern. |

## Runtime

Verbindung zu einem **anvild**-Daemon und IPC-Diagnose.

| Feld | Bedeutung |
|---|---|
| **Host**         | Hostname oder IP der PLC. Default `localhost`. |
| **Port**         | gRPC-Port von anvild. Default `50051`. |
| **User**         | Benutzername fuer die Token-Authentifizierung. |
| **Anvil Debug**  | IPC-Diagnose-Stufe (`Off`, `Errors only`, `Verbose`). Schreibt zusaetzliche Stats in den anvild-Log — nuetzlich, um Iceoryx-Topic-Drift in Production zu finden. |

Zusaetzlich: **Auto-Connect on start** verbindet sich beim Editor-Start
automatisch mit dem zuletzt erfolgreich verbundenen anvild — sinnvoll
auf einem dedizierten Engineering-Laptop.

Der **Network Scanner**-Block in derselben Lasche scannt das LAN nach
Modbus-TCP-Geraeten (Port 502) und ForgeIEC-Runtimes (Port 50051) und
fuegt Treffer in die Bus-Konfiguration ein.

## PLC

Steuert, was nach einem **Upload** auf der PLC passiert.

| Feld | Bedeutung |
|---|---|
| **Compile Mode** | `Development` (Live-Monitoring + Forcing aktiv) oder `Production` (gestripptes Binary, ohne Debug-Bridges — Sicherheits-Boundary). |
| **PLC autostart**| Startet die PLC-Runtime automatisch nach erfolgreichem Upload, ohne den Bestaetigungsdialog. |
| **Persist enabled** | Aktiviert das periodische Speichern von `VAR_PERSIST`/`RETAIN`-Variablen nach `/var/lib/anvil/persistent.dat`. Werte ueberleben einen Neustart der Runtime. |
| **Persist polling interval** | Intervall in Sekunden zwischen den automatischen Speichervorgaengen (Default `5 s`). |
| **Monitor history** | Anzahl Samples pro Variable im Oszilloskop-Recorder (Default `1000`). |
| **Monitor interval**| Abtast-Intervall in Millisekunden fuer das Live-Monitoring (Default `100 ms`). |

## Library

Sync-Verhalten fuer die Standard-Library zwischen Editor-Ressource und
PLC-seitigem Library-Pfad — siehe [Library](../library/) fuer das volle
Drift-Modell. Zwei Modi:

  - **Auto-Push aus** (Default) — der Editor zeigt nur einen Hinweis im
    Output-Panel, wenn beim Connect ein Drift erkannt wird. Push erfolgt
    manuell ueber `Tools > Sync Library`.
  - **Auto-Push an** — der Editor schickt die lokale Library-Version
    automatisch, sobald ein Drift erkannt wird. Nuetzlich in einem
    Single-Programmer-Setup.

## AI Assistant

Optionale Code-Vervollstaendigung gegen einen lokalen, OpenAI-kompatiblen
LLM-Server (LM Studio, Ollama, llama.cpp, vLLM).

| Feld | Bedeutung |
|---|---|
| **Enable AI Assistant** | Schaltet die Inline-Completion ein. |
| **API Endpoint**        | OpenAI-kompatibler Endpoint, z. B. `http://localhost:1234/v1`. |
| **Max Tokens**          | Antwort-Limit pro Anfrage. Default `2048`. |
| **Temperature**         | `Precise (0.1)`, `Balanced (0.3)`, `Creative (0.7)`, `Wild (1.0)`. |

## UX-State (automatisch persistiert)

Folgende Felder werden **ohne** Preferences-Dialog im Hintergrund
gespeichert, damit der Editor beim naechsten Start in dem Zustand
oeffnet, in dem Sie ihn verlassen haben:

  - Fenster-Geometrie + Window-State (`windowGeometry`, `windowState`)
  - Splitter- und Header-Positionen (`splitterState`, `headerState`)
  - Hoehe des Output-Panels (`outputPanelHeight`)
  - Letztes geoeffnetes Projekt (`lastProject`) und Recent-Files-Liste
  - Session-Zustand: offene POU-Tabs, aktiver Tab, Cursor- und
    Scroll-Position pro POU

## Speicherort der Settings

Die Settings liegen ueber Qts `QSettings` plattform-spezifisch:

| Plattform | Pfad |
|---|---|
| **Windows** | Registry: `HKCU\Software\ForgeIEC\ForgeIEC Studio` |
| **Linux**   | `~/.config/ForgeIEC/ForgeIEC Studio.conf` |
| **macOS**   | `~/Library/Preferences/io.forgeiec.studio.plist` |

Loeschen dieser Datei / dieses Registry-Schluessels setzt alle
Einstellungen auf Default zurueck — nuetzlich nach einem fehlgeschlagenen
Upgrade.

## Geplante Erweiterungen

Im Backlog (Cluster R Phase 3): das Output-Panel bekommt eigene
Severity-Farben (Error rot, Warning gelb, Info weiss) und eine
einstellbare Schriftgroesse. Beide Optionen werden dann hier in einer
neuen Lasche `Output` auftauchen.

## Verwandte Themen

  - [Library](../library/) — Sync-Verhalten zwischen Editor und Runtime.
  - [Bus-Konfiguration](../bus-config/) — projekt-bezogene Settings, die
    *nicht* hier sondern direkt am Bus-Segment / -Device liegen.
