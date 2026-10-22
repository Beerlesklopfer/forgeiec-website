# Screenshots of the ForgeIEC programs

The pages use the Hugo shortcode `screenshot` (logic in
`layouts/partials/screenshot.html`). As long as no file exists, the page
shows a marked placeholder ("Screenshot folgt" / "Screenshot to follow")
in the same aspect ratio. Drop a file in the right place and the page
shows it on the next build; no page has to be edited.

## File scheme

```
static/img/screenshots/<program>/<name>-<version>.png
```

- `<program>`: `studio`, `fdd-editor`, `hearth`, `hearth-server`, `rivet`
  (also `anvil`, `tongs` if ever needed)
- `<name>`: the screen's stem from the list below, e.g. `editor-st`
- `<version>`: the version of the program shown, three numbers, e.g. `0.2.0`

Example: `static/img/screenshots/studio/editor-st-0.2.0.png`.

Without `version=` in the shortcode the **highest** version wins
(compared per number: `0.10.0` > `0.9.0`), so a newer screenshot replaces
the old one without touching the pages. A `.webp` of the same stem and
version is preferred over the `.png`. Files that do not match the scheme
are ignored. The caption gets "<Program> <version>" appended
automatically.

## Where the version numbers come from

`versions.txt` (in this folder) holds the current program versions;
`make screenshots-list` flags screenshots older than that as `outdated`.

| program | source of the version | 22.10.2026 |
|---|---|---|
| studio | forgeiec-studio `CMakeLists.txt`, `project(ForgeIEC VERSION …)` | 0.2.0 |
| fdd-editor | built with the Studio, same version | 0.2.0 |
| anvil | anvil `Cargo.toml` | 0.2.2 |
| tongs | tongs-core workspace `Cargo.toml` | 0.2.2 |
| hearth | hearth-studio `CMakeLists.txt`, `project(HearthStudio VERSION …)` | 0.2.0 |
| hearth-server | hearth-studio `hearth/Cargo.toml` | 0.2.1 |
| rivet | forgeiec-rivet `client/Cargo.toml` (branch development) | 0.1.0 |

The version shown in the program's About dialog / package is the one to
use in the file name.

## Make targets

- `make screenshots-missing` — builds into a temp dir, lists every
  placeholder as `<program>/<name>`.
- `make screenshots-list` — lists existing files with version, marks
  `outdated` ones.

## How to take a clean screenshot

- **Size**: 2560 × 1600 px (16:10, sharp on 2× displays). Other ratios
  only with `ratio="…"` in the shortcode.
- **Format**: PNG (lossless; text stays crisp). Optional extra `.webp`.
- Light theme of the program, default window layout, no debug panels.
- A clean demo project (e.g. a built-in example such as `traffic_light`
  or `blinky`), not a customer project.
- **Nothing private**: no personal names, e-mail addresses, IP
  addresses, host names, serial numbers, API keys, registration codes,
  QR codes of real phones, certificates or tokens. Use the example zone
  and slug from the documentation (`kornfeld.solawis.forgeiec.io` style)
  only if it is not a live installation; otherwise blur.
- Crop to the window; no desktop, no taskbar, no mouse pointer.
- Check: `make screenshots-list`, then build and look at the page.

## The screens (scope taken from the source code, 22.10.2026)

At most one graphical editor appears, marked "in development" —
FBD/LD/SFC/IL are not compiled yet.

| # | program/name | what it shows (source) | page |
|---|---|---|---|
| 1 | studio/editor-st | Main window with the Structured Text editor (`studio/src/lang/st/FStEditor.cpp`, `FMainWindow.cpp`) | /plattform/forge-studio/, home |
| 2 | studio/variables | Variables panel with filters by text, type, range and tag (`FVariablesPanel.cpp`) | /plattform/forge-studio/ |
| 3 | studio/library | Block library with categories and documentation search (`FLibraryPanel.cpp`, `FLibraryHelpPanel.cpp`) | /plattform/forge-studio/ |
| 4 | studio/oscilloscope | Live oscilloscope: timing, analog and normalized view (`FOscilloscopeWidget.cpp`) | /plattform/forge-studio/ |
| 5 | studio/plc-stats | Live runtime statistics: state, program, run time, cycle metrics (`FPlcStatsPanel.h`) | /plattform/anvil/ |
| 6 | studio/network | Network picture: interfaces, buses on them, devices on the buses (`FNetworkPanel.h`) | /plattform/tongs/ |
| 7 | studio/device | Device panel: the device drawing from its description with live lamps, properties beside it (`FDevicePanel.h`) | /plattform/tongs/ |
| 8 | studio/ai-assistant | AI assistant dock with one tab per persona (`FAiAssistantDock.cpp`) | /help/ai/ |
| 9 | studio/tongs-panel | Tongs panel in QML: per-protocol view, diagnosis, bus traffic — branch `p3-tongs-qml`, **in development** (`studio/qml/tongs/*.qml`) | /architektur/ |
| 10 | studio/editor-sfc | SFC editor — **in development, not compiled yet** (`studio/src/lang/sfc/FSfcEditor.cpp`) | /plattform/forge-studio/ |
| 11 | fdd-editor/catalog | FDD editor: device description as a tree with tabs and an edit mask (`editor/src/ui/FFddEditorWindow.cpp`, `FFddDetailPanel.cpp`) | /plattform/forge-studio/ |
| 12 | hearth/editor | Hearth Studio: screens, symbols, wires, variables, inspector (hearth-studio `README.md`) — preview | /plattform/hearth/ |
| 13 | hearth-server/hmi | A published Hearth screen in the browser with live values (hearth-studio `README.md`, Hearth Server) — preview | /plattform/hearth/ |
| 14 | rivet/gateway-setup | Gateway web UI, setup: registration code, zone, mode (`client/templates/setup.html.tera`) | Rivet page |
| 15 | rivet/gateway-overview | Gateway web UI, overview: address, certificate, uplink and portal state (`client/templates/overview.html.tera`) | Rivet page |
| 16 | rivet/portal-phone-setup | Portal: add a phone with a QR code for the WireGuard app (`server/portal/gateways/templates/gateways/_phone_setup.html`) | Rivet page, home Rivet band |

## Shortcode lines (de / en)

```
{{< screenshot program="studio" name="editor-st" alt="ForgeIEC Studio mit einem Programm in Strukturiertem Text im Editor" caption="Der ST-Editor im Hauptfenster des Studios." >}}
{{< screenshot program="studio" name="editor-st" alt="ForgeIEC Studio with a Structured Text program in the editor" caption="The ST editor in the Studio's main window." >}}

{{< screenshot program="studio" name="variables" alt="Variablenliste des Projekts mit Filterleiste" caption="Variablen: filtern nach Text, Typ, Bereich und Markierung." >}}
{{< screenshot program="studio" name="variables" alt="Project variable list with filter bar" caption="Variables: filter by text, type, range and tag." >}}

{{< screenshot program="studio" name="library" alt="Bausteinbibliothek mit Kategorien und Dokumentation" caption="Bibliothek: Bausteine nach Kategorie, Suche auch in der Dokumentation." >}}
{{< screenshot program="studio" name="library" alt="Block library with categories and documentation" caption="Library: blocks by category, search includes the documentation." >}}

{{< screenshot program="studio" name="oscilloscope" alt="Oszilloskop mit mehreren Variablenverläufen" caption="Oszilloskop: Zeitdiagramm, analoge und normierte Ansicht." >}}
{{< screenshot program="studio" name="oscilloscope" alt="Oscilloscope showing several variable traces" caption="Oscilloscope: timing, analog and normalized view." >}}

{{< screenshot program="studio" name="plc-stats" alt="Laufzeitstatistik der Steuerung im Studio" caption="Laufzeitstatistik: Zustand, Programm, Laufzeit und Zykluswerte, live." >}}
{{< screenshot program="studio" name="plc-stats" alt="Runtime statistics of the controller in the Studio" caption="Runtime statistics: state, program, run time and cycle figures, live." >}}

{{< screenshot program="studio" name="network" alt="Netzbild mit Schnittstellen, Bussen und Geräten" caption="Das Netzbild: Schnittstellen, Busse darauf, Geräte daran." >}}
{{< screenshot program="studio" name="network" alt="Network picture with interfaces, buses and devices" caption="The network picture: interfaces, the buses on them, the devices on the buses." >}}

{{< screenshot program="studio" name="device" alt="Gerätezeichnung mit leuchtenden Statuslampen und Eigenschaften" caption="Geräteansicht: die Zeichnung aus der Gerätebeschreibung, Lampen mit Live-Werten." >}}
{{< screenshot program="studio" name="device" alt="Device drawing with lit status lamps and properties" caption="Device view: the drawing from the device description, lamps lit by live values." >}}

{{< screenshot program="studio" name="ai-assistant" alt="KI-Helfer-Leiste mit einem Reiter je Persona" caption="Der KI-Helfer: ein Reiter je Persona." >}}
{{< screenshot program="studio" name="ai-assistant" alt="AI assistant dock with one tab per persona" caption="The AI assistant: one tab per persona." >}}

{{< screenshot program="studio" name="tongs-panel" alt="Tongs-Ansicht mit Diagnose und Busverkehr" caption="Tongs-Ansicht je Protokoll mit Diagnose und Busverkehr." status="wip" >}}
{{< screenshot program="studio" name="tongs-panel" alt="Tongs view with diagnosis and bus traffic" caption="Tongs view per protocol with diagnosis and bus traffic." status="wip" >}}

{{< screenshot program="studio" name="editor-sfc" alt="Editor für Ablaufsprache (AS), geplant für Version 0.5" caption="Ablaufsprache (AS): geplant für Version 0.5, Programme werden noch nicht übersetzt." status="plan" >}}
{{< screenshot program="studio" name="editor-sfc" alt="Sequential Function Chart (SFC) editor, planned for version 0.5" caption="Sequential Function Chart (SFC): planned for version 0.5, programs are not compiled yet." status="plan" >}}

{{< screenshot program="fdd-editor" name="catalog" alt="FDD-Editor mit Gerätebeschreibung als Baum und Eingabemaske" caption="Der FDD-Editor: Gerätebeschreibungen als Baum, bearbeitet in einer Maske." >}}
{{< screenshot program="fdd-editor" name="catalog" alt="FDD editor with a device description as a tree and an edit form" caption="The FDD editor: device descriptions as a tree, edited in a form." >}}

{{< screenshot program="hearth" name="editor" alt="Hearth Studio mit einem Bildschirm aus Symbolen und Verbindungen" caption="Hearth Studio: Bildschirme aus Symbolen, Verbindungen und Variablen." status="wip" >}}
{{< screenshot program="hearth" name="editor" alt="Hearth Studio with a screen built from symbols and wires" caption="Hearth Studio: screens built from symbols, wires and variables." status="wip" >}}

{{< screenshot program="hearth-server" name="hmi" alt="Veröffentlichter Hearth-Bildschirm im Browser mit Live-Werten" caption="Ein veröffentlichter Bildschirm im Browser, mit Live-Werten." status="wip" >}}
{{< screenshot program="hearth-server" name="hmi" alt="Published Hearth screen in a browser with live values" caption="A published screen in the browser, with live values." status="wip" >}}

{{< screenshot program="rivet" name="gateway-setup" alt="Einrichtung des Rivet-Gateways im Browser" caption="Gateway einrichten: Registrierungscode eingeben, Betriebsart wählen." >}}
{{< screenshot program="rivet" name="gateway-setup" alt="Setting up the Rivet gateway in the browser" caption="Setting up the gateway: enter the registration code, choose the mode." >}}

{{< screenshot program="rivet" name="gateway-overview" alt="Übersicht des Rivet-Gateways mit Adresse, Zertifikat und Verbindungsstatus" caption="Gateway-Übersicht: Adresse, Zertifikat, Tunnel zum Server, Portal." >}}
{{< screenshot program="rivet" name="gateway-overview" alt="Rivet gateway overview with address, certificate and connection state" caption="Gateway overview: address, certificate, tunnel to the server, portal." >}}

{{< screenshot program="rivet" name="portal-phone-setup" alt="Rivet-Portal: Handy mit QR-Code für die WireGuard-App hinzufügen" caption="Handy hinzufügen: QR-Code mit der WireGuard-App scannen." >}}
{{< screenshot program="rivet" name="portal-phone-setup" alt="Rivet portal: add a phone with a QR code for the WireGuard app" caption="Adding a phone: scan the QR code with the WireGuard app." >}}
```

In templates (e.g. the home page) use the partial directly:
`{{ partial "screenshot.html" (dict "page" . "program" "studio" "name" "editor-st" "alt" "…" "caption" "…") }}`
