---
title: "Partner"
summary: "Wer mitbaut — und in welchen Bereichen wir Unterstuetzung suchen"
---

## Wer fuer eine Partnerschaft passt

ForgeIEC waechst nicht durch Marketing-Vereinbarungen, sondern durch
Leute die **Code, Hardware oder Praxiswissen einbringen**. Wir suchen
Partner mit nachweisbarem Open-Source-Engagement und konkretem
Beitrag zu einem der Subsysteme.

| Kriterium | Was wir sehen wollen |
|---|---|
| **Nachweisbare OSS-Beitraege** | Commits / PRs / Bug-Reports in bestehenden Projekten — nicht nur Nutzung |
| **Oeffentliches Profil** | GitHub, GitLab, Codeberg, Forgejo — egal welches Hosting |
| **Domain-Expertise** | Industrielle Automatisierung, Feldbusse, IEC 61131-3, Embedded-Systeme oder verwandtes |
| **Langfristige Perspektive** | Plattform-Aufbau ist Marathon — wir suchen keine Kurz-Engagements |

Open Source als Marketing-Etikett ohne Code-Beitrag passt **nicht**
zu unserem Modell.

---

## Bereiche in denen wir konkret Unterstuetzung suchen

### 🔧 Bus-Bridges (tongs-*)

{{< components "tongs,anvild" >}}

- **tongs-ethercat** — DC-Sync, Slave-State-Machine, ENI-XML-Import
- **tongs-profibus** — DP-Master, GSD-Import-Toolchain
- **tongs-ethernetip** — CIP-Connections, EDS-Import
- **tongs-can** — CANopen + J1939

Wer einen Stack fuer eines dieser Protokolle gut kennt — ideale
Stelle. Skeleton + Fault-Model + IPC-Wire-Format stehen, der
Protokoll-spezifische Teil fehlt.

### 🛠️ Studio-Editor-Features

{{< components "studio" >}}

- **FBD/LD/SFC-Editoren** — heute liegt der Fokus auf ST. Grafische
  Sprachen brauchen eigene Tree-sitter-Grammatik + Canvas-Renderer.
- **Vendor-Catalog-Pflege** — FDDs fuer weitere Hersteller (heute:
  Weidmueller). Wer mit GSDML/EDS/ESI-Konvertern arbeiten kann ist
  hilfreich.
- **Internationalisierung** — Studio + Website werden aktuell nach
  EN/DE/FR/ES/ZH/JA/TR/AR uebersetzt; manche Sprachen sind nur
  maschinell vorbefuellt.

### 🌬️ HMI-Anbindung (bellowsd)

{{< components "bellowsd" >}}

- **OPC-UA-Companion-Specs** — bellowsd unterstuetzt heute generische
  OPC-UA-Knoten. Companion-Spec-Adapter (z.B. PackML, OPC-UA-Robotics)
  sind willkommen.
- **HMI-Frameworks** — `Hearth` ist als IIoT-Subscriber-Layer in
  Planung. Wer mit MQTT, Time-Series-DBs (InfluxDB, TimescaleDB)
  oder Grafana-Pipelines arbeitet, kann hier Architektur mitgestalten.

### 🔥 Runtime + Determinismus (anvild)

{{< components "anvild" >}}

- **Real-Time-Linux-Tuning** — PREEMPT_RT-Kernel, CPU-Pinning,
  Cache-Locality fuer Sub-Millisekunden-Cycle-Times
- **Rust+LLVM-Codegen (rusty)** — geplante Migration der Layer-1-
  Codegen weg von matiec/C-Output hin zu Rust+LLVM. Determinismus-
  Garantien + Online-Change-Vorbereitung.
- **Hardware-Targets** — Raspberry Pi, BeagleBone, industrielle x86,
  ARM-SBCs. Testing + Performance-Profiling auf echter Hardware.

### 📚 Bildung + Dokumentation

{{< components "studio" >}}

- **Tutorials** — von „erstes Knight-Rider in 5 Minuten" bis „komplette
  Maschinensteuerung mit OPC-UA + EtherCAT"
- **Beispiel-Projekte** — heute liegen nur 2 Demos im Tree. Mehr
  ist immer besser.
- **Lehr-Curriculum** — Hochschulen die ForgeIEC als Lehr-IDE
  einsetzen wollen. Wir liefern Studio kostenlos, Dozenten bringen
  IEC-Curriculum.

---

## Was Partner zurueck bekommen

| Leistung | Konkret |
|---|---|
| **Source-Zugang** | Alles ist OSS — Source liegt auf GitHub + Forgejo |
| **Frueher Zugriff** | Development-Branch ist auf Feature-Status-Niveau (siehe [News](/news/)) — Partner sehen Aenderungen am Tag des Pushes |
| **Code-Review-Zugang** | PRs werden vom Kernteam reviewt, Feedback in Stunden statt Wochen |
| **Roadmap-Mitsprache** | Sprint-Planung passiert offen ueber GitHub-Issues + Architektur-Specs |
| **Technische Beratung** | Architektur-Diskussion via Issues, Mail, oder direkter Draht |
| **Branding** | Partner werden auf dieser Seite aufgefuehrt (sobald die ersten da sind) |

Wir verkaufen **keine** Premium-Lizenzen und versprechen **keine**
Service-Vertrags-Privilegien — alle Funktionen sind Teil der
AGPL-3.0-Distribution. Partnerschaft heisst **enger Kontakt + frueher
Einblick + Mitarbeit**, nicht „bezahltes Sondermenue".

---

## Aktuell registrierte Partner

Stand 2026-05: noch keine externen Partner — die Plattform ist im
Aufbau-Sprint, Partner-Onboarding kommt sobald die ersten Subsystem-
APIs (Bridge-SDK, FDD-Format) stabilisiert sind.

Wenn Sie zu den ersten gehoeren wollen: kommen Sie auf uns zu (siehe
unten).

---

## Bewerbung

Schicken Sie uns:

1. **Wer sind Sie?** — Person / Organisation, Hintergrund
2. **Wo haben Sie schon beigetragen?** — Links zu OSS-Projekten,
   konkrete Commits / PRs / Issues
3. **Welcher Bereich?** — siehe Liste oben (Bus-Bridges /
   Editor / HMI / Runtime / Bildung) — bitte konkret
4. **Was waere Ihr erster Schritt?** — kein Plan-Dokument noetig,
   ein Absatz reicht

Antwort: blacksmith@forgeiec.io.

---

## Verwandte Themen

- [News](/news/) — was die letzten Sprints geliefert haben
- [Architektur + Sicherheit](/help/ai/architecture/) — Spec-Tiefe
  fuer Sicherheits-Reviewer
- [Download](/download/) — alle Komponenten + Source-Tree
