---
title: "Federation + Team-Trust: Mehrere Workstations, kontrollierbares Vertrauen"
date: 2026-05-13
summary: "ForgeIEC verbindet jetzt mehrere Workstations zu einem Team — mit verifizierbaren Identitäten und einem klaren Rollenmodell"
components: [studio]
---

{{< components "studio" >}}

## Warum das wichtig ist

Industrielle Automatisierung passiert selten an einer einzelnen
Workstation. Team-Leads reviewen den Code. Inbetriebnehmer
diagnostizieren remote. Build-Server kompilieren nachts. Bisher
hieß das: jeder hat seinen eigenen Editor, manuell synchronisiert,
keine echte Federation.

Mit der jetzt abgeschlossenen **Federation-Sprint-Reihe** wird
ForgeIEC Studio zu einem **Multi-Workstation-System**:

- Mehrere Studios sehen sich gegenseitig — kontrolliert per
  Trust-Store
- Ein **Caretaker** übernimmt die zentrale Verantwortung für
  „wer gehört dazu"
- Identitäten sind **menschen-verifizierbar** — vier Wörter,
  ein kleines Bild, kein 64-Zeichen-Hex-Vergleich
- Onboarding + Revocation laufen über ein **klares Protokoll**,
  nicht über Datei-Versand per Mail

Das macht ForgeIEC erstmals **team-tauglich** ohne dass die
Sicherheit unter dem Komfort leidet.

---

## Was Sie davon haben

### Ein neuer Kollege kommt ins Team

Statt Zertifikate per USB-Stick zu verteilen:

1. Neuer Kollege erzeugt in seinem ForgeIEC Studio einen Antrag.
2. Caretaker sieht den Antrag — **mit Memorable-ID + Randomart**
   des noch-nicht-ausgestellten Certs.
3. Caretaker prüft visuell / verbal („Lies mir deine 4 Wörter
   vor"), bestätigt im Confirm-Dialog.
4. Frischer Ausweis geht zurück. Kollege ist Member.

Memorable-ID-Beispiel: `road-trash-smile-deny`. Vier englische
Worte aus einer 2048-Worte-Liste, deterministisch aus dem Cert
abgeleitet — schon ein einzelnes geändertes Bit am Anfang
verschiebt **alle vier** Worte komplett.

Randomart-Beispiel:

```
+----[SHA256]-----+
|        o. ..... |
|       o .o .   .|
|      o  ....   o|
|.    . .+.   o ..|
| + .. ..Soo.. o  |
|. +. . . +.++.   |
| oo   o .oo+..   |
|...= o +o.+      |
|E+*o. +.o=o      |
+-----------------+
```

Sie lernen die **Form** eines Kollegen-Bildes nach 2–3 Verbindungen
wieder.

### Ein Kollege geht / Notebook verschwindet

Der Caretaker widerruft das Cert. Die signierte Revocations-Liste
geht an alle Team-Mitglieder. Ab dem nächsten Roster-Pull
(default alle 5 Minuten, auf Wunsch sofort) lehnt jedes andere
Studio das widerrufene Cert ab.

### IT hält die Fäden in der Hand

- **peers.toml + revoked.toml** sind digital signiert. Die
  Verteilung kann über Git, geteiltes Laufwerk, USB laufen — die
  Bytes müssen nur unverfälscht ankommen, die mathematische
  Prüfung passiert beim Empfang.
- **Replay-Schutz** per monotonem `sequence_number` verhindert dass
  ein Angreifer eine alte (un-revoked) Version zurückspielt.
- **TLS 1.3 + optional mTLS** auf dem Wire. Cipher-Suiten folgen
  den Distribution-Hardening-Defaults.
- **Build-time-Gate** für schreibende Operationen: die Default-
  Distribution aus dem APT-Repo kann nur lesen. Schreiben braucht
  bewussten Build-Switch.

---

## Sicherheit: in jedem Schritt sichtbar

Jeder schreibende Vorgang (Cert ausstellen, Roster aktualisieren,
Member widerrufen) durchläuft die **Confirmation State Machine**:

- Tool-Aufruf liefert `FORGE_ERR_CONFIRMATION_REQUIRED` mit
  Kontext zurück
- Operator sieht im Chat: was passieren soll, mit welcher Identität,
  mit welcher Memorable-ID/Randomart
- Bestätigung per `editor.confirm` — Audit-Log mit Timestamp +
  Choice + Args

Keine stille Hintergrund-Ausstellung. Keine automatische
Rotation ohne Operator-Klick. Verlorenes Cert → läuft einfach
ab, Operator bemerkt, Operator entscheidet.

---

## Architektur-Tiefe für Auditoren

Wer prüfen will dass das nicht nur „Sicherheit als Slogan" ist,
findet die belastbaren Details unter
[Architektur + Sicherheit](/help/ai/architecture/):

- Vollständige formale Spec mit RFC-2119-Verbindlichkeit
- Cross-Reference zu allen Quellklassen + Dateien im Source-Tree
- Standards-Tabelle: BIP-39, OpenSSH-randomart, Ed25519, RSA-PSS,
  RFC 6125, MCP 2025-03-26
- Ehrliche Liste der **noch offenen Punkte** (kein
  Marketing-Beschönigen)

---

## Plus: Stale-SHM ist Geschichte

Im selben Release ist auch der `anvild`-Auto-Cleanup eingeflossen.
Was bisher als „Variable klebt trotz frischem Deploy" gelegentlich
Inbetriebnahme-Sitzungen verlangsamt hat, ist mit
`sudo systemctl restart anvild` jetzt einfach erledigt — der
Daemon räumt stale Shared-Memory-Segmente beim Start selbst auf.

Hintergrund + Fix dokumentiert: [FAQ-Eintrag](/help/faq/stuck-variables-shm/).

{{< callout type="note" title="Nachtrag" >}}
Der pauschale Cleanup beim anvild-Start wurde inzwischen wieder
entfernt: er hat die gemeinsamen Segmente **lebender** Peers
(bellowsd, hearth, tongs-*) mitgerissen. Das Aufräumen macht heute
die Anvil-Schicht gezielt pro totem Node; als Anwender starten Sie
einfach die PLC-Runtime neu. Aktueller Stand im
[FAQ-Eintrag](/help/faq/stuck-variables-shm/).
{{< /callout >}}

---

## Wo Sie das nutzen

| Setup | Was Sie konfigurieren |
|---|---|
| **Einzel-Workstation** | nichts. Federation ist optional. |
| **Zwei Programmierer im Büro** | Caretaker auf einer Workstation, Member auf der anderen. Trust-Store per geteiltem Laufwerk. |
| **Team mit Build-Server** | Build-Server hat eigenes Cert, läuft headless, ruft Studio-MCP-Tools per `curl` aus CI heraus. |
| **Mehrere Standorte** | peers.toml per Git verteilt, signiert, jede Änderung pull-anchored. |

---

## Wo es konkret nachzulesen ist

- [Anwender: mehrere Workstations verbinden](/help/ai/team/)
- [Architektur + Sicherheit](/help/ai/architecture/)
- [MCP für Applikationsingenieure](/help/mcp/programmers/)
- [MCP für IT + Betrieb](/help/mcp/it/)

Source-Repository: `ForgeIEC/forgeiec-studio` im Forgejo unter
`git.forgeiec.io` — Zugriff nach Freischaltung Ihres
SSH-Public-Keys.

---

## Was als nächstes kommt

- Caretaker-Toggle-UI in den Preferences (statt heute QSettings-
  Editieren plus Modal-Confirmation)
- `team.rotate_cert` + `team.revoke_peer` voll implementiert
- `team.export_setup` als Onboarding-Bundle-Generator
- Memorable-ID-Typing als zusätzliche Confirmation-Hardening für
  high-risk Operationen (Spec §7.4.2)
