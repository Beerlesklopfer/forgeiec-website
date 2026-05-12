---
title: "Variable bleibt 'haengen' trotz frischem Deploy"
summary: "BOOL/INT-Wert haftet entgegen der Programm-Logik — Ursache ist meist stale iceoryx2 Shared-Memory"
---

## Symptom

Eine ForgeIEC-Pool-Variable (typischerweise ein `BOOL` auf einer
HMI-/Bellows-Adresse wie `%MX1.6`) zeigt im Live-Monitor oder am
angeschlossenen Geraet einen Wert, der nicht zur Programm-Logik passt.

Klassisches Bild:

- Im Variables-Tab steht `TRUE` (Wert)
- Die F-Checkbox ist **nicht** gesetzt (`forced = false`)
- Der ST-Code schreibt offensichtlich einen anderen Wert
  (z.B. `Bellows.LED_14 := (Position = 14);` und Position ist nirgends 14)
- Neue Compile + Deploy zeigen "Compilation finished successfully" —
  aendert aber nichts am Verhalten

Sie restarten Editor, anvild, bellowsd — der Wert bleibt.

---

## Ursache

ForgeIEC nutzt **iceoryx2 Shared-Memory** (intern "Anvil" genannt) fuer
die Datenuebertragung zwischen PLC-Runtime, Editor und HMI-Bruecken.
Shared-Memory-Topics werden in `/tmp/iceoryx2/` und `/dev/shm/` als
Dateien gehalten.

Wenn ein PLC-Prozess hart beendet wird (z.B. abgestuerzter Deploy,
SIGKILL waehrend laufender Publishes, Watchdog-Reset), kann eine
**Subscriber-Queue mit stale Payload** in der Datei zurueckbleiben.

Beim naechsten Start fragt die `bellows_subscribe_all()`-Routine
genau diese Queue ab — und schreibt die alten TRUE-Werte zurueck
in den PLC-Speicher, **bevor** der POU laufen kann.

Da das vor jedem Scan-Zyklus passiert, "fixiert" sich der alte Wert,
auch wenn die POU im selben Zyklus etwas anderes berechnet — beim
naechsten Zyklus kommt die stale Payload erneut.

Symptom-typisch ist, dass nur **einzelne Bits** betroffen sind
(genau jene, deren stale Payload noch im SHM steht); andere Variablen
auf demselben Topic cyclen normal.

---

## Loesung: anvild neu starten

Seit anvild **v0.1.0+** raeumt der Daemon stale SHM-Segmente
automatisch beim Start auf. Ein einfacher Restart genuegt:

```bash
sudo systemctl restart anvild
```

Anschliessend im Editor: `Build -> Compile and Upload` (oder MCP-Tool
`codegen.deploy`) — die SHM-Topics werden frisch angelegt, ohne stale
Payload.

Nach dem naechsten Scan-Zyklus zeigt der Live-Monitor den korrekten,
von Ihrer Programm-Logik berechneten Wert.

> **Hinweis fuer aeltere anvild-Versionen** (vor Auto-Cleanup): falls
> ein Restart nicht hilft, muessen die SHM-Dateien manuell entfernt
> werden — `sudo systemctl stop bellowsd anvild && sudo rm -rf
> /tmp/iceoryx2/* /dev/shm/iox2_* && sudo systemctl start anvild
> bellowsd`.

---

## Wann tritt das auf?

Im normalen Devloop **tritt das praktisch nie auf**. Sauberer Deploy
ueber `Build -> Compile and Upload` und ordentliches Stop+Start ueber
das Runtime-Menue raeumt die SHM-Topics regulaer auf.

Beobachtbar ist der Effekt vor allem in einem Szenario:

**Sie haben den lokalen AI-Assistenten (MCP) im Projekt experimentieren
lassen.** Das LLM hat moeglicherweise:

- Wiederholt `set_text_body` + `codegen.deploy` in schneller Folge ausgefuehrt
- Force-Setzungen vorgenommen und nicht sauber zurueckgenommen
- POU-Instances umbenannt oder geloescht waehrend die PLC noch lief
- Mehrere Deploy-Iterationen ohne `runtime.stop` dazwischen versucht

Solche Sequenzen koennen einen kurzen Moment erzeugen in dem die alte
forgeiec-plc-Instanz mit `SIGTERM`/`SIGKILL` endet bevor sie ihre
Subscriber-Queues aus dem SHM zuruecknimmt — und genau diese Queue
liest die NEUE forgeiec-plc-Instanz dann zum Start wieder ein.

Weitere (seltenere) Ausloeser ohne AI-Beteiligung:

- Hartes `kill -9` auf `forgeiec-plc` durch Operator
- Crashes der HMI-Bruecke (`bellowsd`) im laufenden Betrieb
- Mischbetrieb verschiedener anvild-Versionen auf demselben Host

Wenn Sie ein einmaliges Vorkommen erleben, ist der oben genannte
SHM-Reset die einfachste Loesung. Bei wiederholtem Auftreten ohne
AI-Aktivitaet bitte das Vorkommen melden (mit `journalctl -u anvild`
und `journalctl -u bellowsd` der letzten Stunde) an
blacksmith@forgeiec.io — die Auto-Cleanup-Logik beim anvild-Start ist
ein laufender Backlog-Punkt.

---

## Verwandt

- [Online-Hilfe](/help/online/) — kontext-sensitive Editor-Hilfe
- [Tests](/help/tests/) — automatisierte Testabdeckung
