---
title: "Architektur + Sicherheits-Engineering (fuer Experten)"
summary: "Technische Tiefe — warum ForgeIEC's KI-Schicht industriell tragfaehig ist und nicht ein Spielzeug"
---

## Zielpublikum

Diese Seite ist fuer **Sicherheitsbeauftragte, IT-Architekten, CISOs,
Compliance-Officer + technische Leads** die pruefen ob die KI-Schicht
in ForgeIEC fuer Industrie-Einsatz qualifiziert ist. Wenn Sie reine
Anwender-Anleitungen suchen, sind Sie [hier richtig](/help/ai/).

Wir zeigen hier konkrete Architektur-Entscheidungen, ihre Begruendungen,
die normativen Spezifikationen die wir umsetzen, und ehrlich auch was
**noch nicht** implementiert ist.

---

## Formale Spezifikation als Single-Source-of-Truth

Die KI-Schicht ist nicht emergentes Code-Verhalten — sie folgt einer
**explizit ausgeschriebenen Architektur-Spezifikation**:

- Dokument: `documentation/architecture/mcp-platform-v1.md` (im
  Source-Tree, ca. 2300 LOC)
- Verbindlichkeits-Stufe: **RFC-2119** — `MUST` / `SHOULD` / `MAY`
- Reviewable: jede Aenderung der Spec geht durch Code-Review wie
  jede andere Aenderung
- Versions-getaggt: `v1` ist die aktuelle Major-Version, alle
  bisherigen Sprints (MCP-1 bis MCP-9, MCP-4a, MCP-4b) referenzieren
  ihre Spec-Abschnitte

Das heisst: die Implementierung ist nicht „der Code ist die Spec",
sondern „die Spec ist die Vorgabe, der Code wird daran gemessen".

---

## Protokoll-Konformitaet: MCP 2025-03-26

ForgeIEC implementiert das **Model Context Protocol** (Anthropic-
publiziertes offenes Protokoll fuer LLM-Tool-Integration) in der
Version `2025-03-26`:

- Transport: **HTTP + SSE** (Server-Sent Events) — kein Custom-
  Protokoll, kein WebSocket-Wildwuchs
- Wire-Format: **JSON-RPC 2.0** — strikt nach Spec, `id` + `method`
  + `params`/`result`/`error`
- `initialize` → `tools/list` → `tools/call`-Lifecycle: standard-
  konform, prüfbar mit dem offiziellen MCP-Inspector
- `capabilities.tools.listChanged: true` — wir signalisieren dem
  Client dass die Tool-Liste sich aendern kann (Editor-Restart,
  Project-Switch)
- `notifications/tools/list_changed` wird **noch nicht** gesendet
  (Backlog) — aktuell muss der Client beim Reconnect re-listen

Damit lassen sich **Drittanbieter-Clients** anschliessen (z.B.
Claude Code, OpenAI ChatGPT mit MCP-Connector, mcp-inspector) ohne
ForgeIEC-spezifischen Code.

---

## Transport-Sicherheit: TLS + optional mTLS

### TLS 1.3 (immer aktiv bei remote-bind)

- Implementierung: **Qt6 QSslSocket** mit dem System-OpenSSL (TLS
  1.3 + 1.2 unterstuetzt)
- Server-Zertifikat: RSA-4096, SAN-bound, 10 Jahre Gueltigkeit,
  bei Bind-Adress-Aenderung automatisch regeneriert (RFC 6125 SAN-
  validation kompatibel)
- Cipher-Suites: System-Defaults (Debian-OpenSSL Hardening folgt
  Distribution-Politik)
- Keine selbst-implementierte Krypto — alles ueber OpenSSL-CLI
  geshellt oder Qt6 SSL-Stack

### mTLS (mutual TLS, optional fuer Federation)

- Aktiviert sobald `~/.config/ForgeIEC/mcp/trust/*.pem` einen oder
  mehrere CA-Certs enthaelt
- `peerVerifyMode = QueryPeer` — Client-Cert wird **angefordert**
  aber ist nicht zwingend (faellt auf Bearer-Auth zurueck), erlaubt
  graduellen Roll-out
- Chain-Validation gegen den Trust-Store erfolgt im Qt-SSL-Stack
- Selbst-implementierte Pruefung der Zertifikats-Subjects gegen die
  `peers.toml`-Liste — siehe naechster Abschnitt

---

## Federation-Roster mit Replay-Schutz

Wo andere LLM-Tool-Plattformen „first-connection-trust" praktizieren
(jeder Cert wird beim ersten Sehen akzeptiert), erzwingt ForgeIEC
**signierte Roster**:

```toml
# peers.toml — von Team-CA signiert
[meta]
sequence_number = 17
signed_ts = "2026-05-12T18:00:00Z"
signed_by = "ForgeIEC-Team-CA"
ca_fingerprint_sha256 = "ba:fc:ef:..."
signature_b64 = "..."

[[peer]]
name = "alice@team"
fingerprint_sha256 = "ab:cd:..."
role = "author"
endpoint = "https://alice-ws.factory:7531"
```

**Eigenschaften:**

- **Signatur:** Ed25519 (bevorzugt, klein + schnell) oder RSA-PSS-
  SHA256 (Interop mit Hardware-Tokens). Ueber openssl-CLI
  geshellt, nicht selbst implementiert.
- **Replay-Protection:** monotone `sequence_number` pro Datei.
  Gespeichert per QSettings, jeder Reload mit `seq <= last_seen`
  wird **abgelehnt**.
- **Canonical-Payload:** Signatur deckt die TOML-Datei ohne die
  `signature_b64`-Zeile ab — line-orientiert, reproduzierbar mit
  `grep -v '^signature_b64'`.
- **Verteilung:** beliebig — Git, S3, HTTP, USB. Der Container
  ist irrelevant; die mathematische Pruefung passiert beim Empfang.

**Implementiert** in `FMcpPeerRoster::verifySignature` mit
openssl-Shell-out fuer Ed25519+RSA-PSS-Verifikation. Reload via
QFileSystemWatcher mit 200ms-Debounce. Stale-Roster-Bug (Loop) ist
beseitigt — siehe FAQ-Eintrag zu SHM, gleicher Mechanismus
defensiv abgestuetzt.

---

## Confirmation State Machine — keine stille Automation

Jede schreibende MCP-Operation laeuft durch eine **Confirmation State
Machine** (Spec §9.5):

1. Tool-Aufruf trifft ein
2. Handler erkennt: ist ein Operator-Approval noetig (state-changing,
   destructive, side-effect-bearing)?
3. Wenn ja: Tool returnt `FORGE_ERR_CONFIRMATION_REQUIRED` mit
   Pending-ID + Frage + Options + Context
4. LLM-Client antwortet via `editor.confirm(id, choice)`
5. State-Machine resumed den ursprünglichen Tool-Aufruf mit dem
   Operator-Choice

Implementierung: `FConfirmationStateMachine` (UUIDv4-keyed,
default 5-min-Timeout, append-only Audit-Trail).

**Garantien:**

- **Kein Tool das State aendert, kann ohne Confirm laufen** — der
  Aufruf-Path geht durch State-Machine; Bypass nur via expliziten
  `force=true`-Parameter den NUR die State-Machine selbst setzt
  beim Resume
- **Operator-Sichtbarkeit:** jede Pending-Confirmation ist im Chat
  als visuelles Element sichtbar, und ueber
  `editor.pending_confirmations` MCP-Tool abfragbar
- **Timeout-Behavior:** abgelaufene Confirmations setzen `choice =
  "timeout"`; der Tool-Resume-Callback entscheidet was das heisst
  (typisch FORGE_ERR_USER_CANCELED)
- **Audit-Log:** alle Confirmations + Choices werden in
  `~/.config/ForgeIEC/mcp_audit.log` (JSONL) protokolliert,
  append-only

---

## Three-Layer Defense gegen unbeabsichtigte Wirkungen

### Layer 1 — Build-time Gate

```cmake
option(MCP_OVERRIDE_SECURITIES "Unlock MCP write tools" OFF)
```

Default OFF. Schreibende Tools (`project.write.*`, `codegen.deploy`,
`runtime.stop`, `editor.quit`, `oscilloscope_set_channels`)
returnen `FORGE_ERR_PERMISSION_DENIED` wenn nicht gesetzt.

**Wichtig:** das ist **kein Runtime-Flag**. Die Pruefung ist
preprocessor-konditional — das deaktivierte Code-Pfad ist beim
Default-Build **gar nicht ueberhaupt im Binary**. Ein Operator kann
ihn nicht via Config-Datei einschalten.

### Layer 2 — Runtime State Machine

Wie oben — jede write-Aktion erfordert Operator-Approval.

### Layer 3 — Operator-Sichtbarkeit

- Chat-Verlauf zeigt jeden Tool-Call als sichtbares Element
- Audit-Log (JSONL) protokolliert alles mit Timestamp
- Build mit MCP_OVERRIDE_SECURITIES blendet einen **Security-
  Override-Banner** im initialize-Output ein:

  ```
  !!! SECURITY OVERRIDE ACTIVE !!!
  This build MUST NOT run on a productive PLC.
  ```

  Der Banner erscheint auch in jeder `warnings[]`-Liste in
  schreibenden Responses — Tooling kann ihn auswerten.

---

## Force-Pfad: explizit out-of-MCP

Variable-Forcing — das manuelle Setzen eines Werts unabhaengig von der
Programm-Logik — ist die **stark side-effect-behaftete** Operation
im PLC-Editor. Es kann reale Hardware bewegen (Motor anwerfen,
Ventil oeffnen).

**Entscheidung:** Force ist explizit **nicht** ueber MCP zugaenglich.
Es gibt **kein** `force.set`-Tool, weder im Default-Build noch im
Override-Build.

**Begruendung:** Ein KI-Agent kann nicht haftbar gemacht werden
fuer Hardware-Side-Effects einer Force-Setzung. Diese Verantwortung
bleibt **explizit beim Operator**, der die GUI-Force-Checkbox manuell
setzt. Die KI-Schicht kann lesen ob ein Wert forciert ist
(`monitor.snapshot` returns `forced=true`), aber nicht selbst
forcieren.

Defense-in-depth:

- **Layer 1 (Codegen-TOML):** Force-Bridge wird nur kompiliert wenn
  `-DFORCING_ENABLED` gesetzt ist (Development-Builds)
- **Layer 2 (anvild RPC):** ForceVariable-gRPC-Endpoint pruft Build-
  Mode der PLC-Binary
- **Layer 3 (Editor-UI):** Force-Checkbox wird greyout wenn der
  PLC-Build kein Force unterstuetzt
- **Layer 4 (MCP):** kein Tool fuer Force; Phase-3 evtl. ein
  `force.*`-Family hinter doppeltem state-machine-Gate

---

## Human-Identification — Memorable-ID + Randomart

Statt 64-char Hex-Fingerprints vergleichen zu lassen (in Praxis
nicht zumutbar) bietet ForgeIEC **zwei deterministisch ableitbare
Visualisierungen** desselben Fingerprints:

### Memorable-ID (BIP-39 wordlist)

- 44 bit aus dem SHA-256-Fingerprint
- 4 Indizes a 11 bit
- Wordlist: kanonische **BIP-39 English** (2048 Worte, dedupliziert
  auf erste 4 Letters, pronounceable)
- Format: `word-word-word-word`
- Bei Bit-Flip in den ersten 44 Bits: **alle 4 Worte aendern sich**
- Verbal verifizierbar ("Lies mir deinen Memorable-ID am Telefon")

### Randomart (OpenSSH drunken bishop)

- Algorithmus: identisch zu `ssh-keygen -lv -E sha256`
- 17×9 Grid, bishop-walk per 2-bit-Move pro Byte des Fingerprints
- Augmentation-String `" .o+=*BOX@%&#/^SE"` mapt Counter-Wert auf
  Zeichen
- Start- und End-Marker (S/E) am Bishop-Pfad-Endpunkten
- Visuell signifikant: ein anderer Cert sieht **anders aus**, der
  menschliche Wiedererkennungs-Bias erkennt „seinen" Peer

Beides ist in `FMcpFingerprintArt` implementiert (zwei statische
Methoden, pur, deterministisch, threadsafe, ohne Heap-Allocation
fuer die Wordlist).

Surfaced in:

- `server_info.trust_store_cas[]` — pro Trust-Store-CA-Cert
- `team.list_peers` — pro Peer
- `team.request_cert` — fuer den frisch ausgestellten Cert
- Peer-Confirm-Dialog (UI-Implementierung kommt mit MCP-5)

---

## Caretaker-Modell — Cert-Lifecycle

Spec §7.4 definiert:

- **Caretaker-Rolle:** eine Workstation im Team haelt den Team-CA-
  Privatschluessel und stellt Member-Certs aus
- Aktiviert ueber QSettings `mcp/caretaker_enabled` PLUS ein
  Bestaetigungs-Modal mit Wortlaut **„I accept Team-CA
  responsibility"** PLUS `MCP_OVERRIDE_SECURITIES=ON`
- Daten: `~/.config/ForgeIEC/mcp/ca-team/{ca.key, ca.crt}` (RSA-4096,
  10 Jahre, CA:TRUE basicConstraint, keyCertSign+cRLSign+
  digitalSignature keyUsage)
- Operationen: `team.request_cert` (sign CSR), `team.revoke_peer`
  (revoke + re-sign roster), `team.export_setup` (onboarding-bundle)
- **Jede** Operation laueft durch die State Machine — keine
  automatische Erneuerung, keine stille Ausstellung
- Multi-Caretaker-Setup moeglich (HA) — Konflikt-Aufloesung per
  monotonem sequence_number im Roster

Implementations-Stand 2026-05:

- `FMcpCaretaker`-Klasse + `team.request_cert`-Tool: **done**
- `team.list_peers`: **done**
- `team.revoke_peer`: **Stub** (revoked.toml-Mutation + Re-signing
  Backlog)
- `team.rotate_cert`, `team.export_setup`: **Backlog**
- Caretaker-Toggle-UI in Preferences: **Backlog**

---

## Implementation-Sprache + Memory-Sicherheit

ForgeIEC-Editor ist **C++17 + Qt6**. Die KI-Schicht (`FMcpServer`,
`FMcpCaretaker`, `FMcpTrustStore`, `FMcpPeerRoster`,
`FMcpFingerprintArt`) nutzt durchgaengig:

- **RAII** fuer Lifetime-Management (QObject-Parent-Chain)
- **PIMPL** wo opaque-types praktischer sind
- **No raw pointers** ueber Klassen-Grenzen — `QPointer`, `unique_ptr`,
  `shared_ptr` je nach Ownership-Semantik
- **Implicit-shared QObjects** (`QSslCertificate`, `QString`,
  `QByteArray`) — sicher fuer Cross-Thread-Snapshots
- **No global mutable state** — alle Module sind objekt-besitzbar

Der Runtime-Server (`anvild`) ist **Rust + Tokio + tonic**. Memory-
sicher per Borrow-Checker, async-runtime fuer Concurrency. Die
gRPC-Schicht zwischen Editor und anvild ist proto-spezifiziert.

iceoryx2 (Shared-Memory-IPC) ist **Rust + C-FFI**. Wir nutzen es
hinter einer eigenen ABI-Probe (`anvil-shared@50cb29f`) die Type-
Hash-Drift vor Connection erkennt — wir haben drei Defense-Layer
gegen Mismatched-Versions in Production.

---

## Test-Coverage + Reproduzierbarkeit

- **117+ automatisierte Tests** decken die IEC-61131-3-Sprache,
  alle 132 Standard-Library-Bausteine, das Multi-Task-Threading-
  System, den Persistenz-Pfad, den Force-Pfad ab
- **Test-Daten committed** im Repo (`tests/data/`), reproduzierbar
- **Jitter-Tests** mit physikalischer Messung gegen Baseline
- **Codegen** ist deterministisch — gleiches `.forge`-Projekt
  produziert byte-identische `POUS.c`-Outputs (matiec)
- **Audit-Log** fuer LLM-Aktivitaet ist append-only JSONL — kein
  Eintrag wird je entfernt, alle Eintraege haben Zeitstempel +
  Tool-Name + Args + Confirm-Choice

---

## Was ehrlich noch nicht da ist

Wir sind transparent ueber das was noch fehlt:

- **`team.revoke_peer`** ist Stub (revoked.toml-Mutation +
  Re-signing folgt)
- **`team.rotate_cert` + `team.export_setup`**: Backlog
- **OCSP / CRL handling:** noch nicht implementiert (Revocation
  derzeit ueber signiertes Roster, nicht ueber Standard-PKI-Pfad)
- **Memorable-ID-Typing-Confirmation** (Spec §7.4.2 sieht „Operator
  MUST type peer's Memorable-ID to confirm" vor): heute noch
  yes/cancel
- **`notifications/tools/list_changed`** SSE: noch nicht emittiert
- **Hardware-Token (PKCS#11 / FIDO2)** fuer Team-CA-Key:
  Roadmap, heute Datei auf Disk mit 600-permissions
- **Force-Tools-Familie** (`force.*`): Phase-3 Backlog
- **Bulk-Mode + erweiterte Berechtigung** fuer >10-Tool-Turn-
  Operationen (Spec MCP-10): Backlog

Diese Items sind im internen Sprint-Board (`project_open_backlog.md`)
mit Prioritaeten gelistet.

---

## Standards + Cross-Reference

Was implementieren wir und was beziehen wir uns drauf:

| Standard | Verwendung |
|---|---|
| IEC 61131-3 (ST/IL/FBD/LD/SFC) | Programmiersprache + Compile-Path via matiec |
| PLCopen XML | Projekt-Dateiformat |
| RFC 6125 (SAN-Validation) | TLS-Server-Cert |
| Ed25519 (RFC 8032) | Roster-Signatur (bevorzugt) |
| RSA-PSS (RFC 8017) | Roster-Signatur (HW-Token-Interop) |
| BIP-39 (Bitcoin) | Wordlist fuer Memorable-ID |
| SSH ssh-keygen | Randomart-Algorithmus |
| MCP 2025-03-26 (Anthropic) | Protokoll-Lifecycle |
| JSON-RPC 2.0 | Wire-Format |
| RFC 2119 | Spec-Verbindlichkeits-Sprache |
| TOML 1.0 | Konfigurations-Dateien |

---

## Lizenz

ForgeIEC + alle Subprojekte (anvild, bellowsd, tongs-modbustcp, …):
**AGPL-3.0-or-later**. Source-Repository einsehbar; Build-
Reproduzierbarkeit ueber Debian-CPack + signed APT-Repository.

---

## Kontakt fuer Security-Review

Bei Fragen, Audit-Anfragen oder Schwachstellen-Meldungen:
blacksmith@forgeiec.io

Wir bevorzugen verantwortliche Offenlegung — geben Sie uns einen
angemessenen Zeitraum zur Behebung bevor Sie veroeffentlichen.

---

## Weiter

- [Sicherheits-Modell (Anwender-Sicht)](/help/ai/security/)
- [Team-Mode + Trust](/help/ai/team/)
- [Zurueck zur AI-Uebersicht](/help/ai/)
