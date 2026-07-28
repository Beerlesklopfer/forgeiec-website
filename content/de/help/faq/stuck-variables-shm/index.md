---
title: "Variable bleibt 'haengen' trotz frischem Deploy"
summary: "BOOL/INT-Wert haftet entgegen der Programm-Logik — Ursache ist meist stale Anvil-Shared-Memory"
---

{{< callout type="symptom" title="Symptom" >}}
Eine BOOL- oder INT-Pool-Variable behaelt einen Wert (TRUE/FALSE oder
Zahlenwert) der nicht zur Programm-Logik passt. `monitor.snapshot`
meldet `forced=false`, der ST-Code schreibt offensichtlich einen
anderen Wert — und trotzdem bleibt der Wert "kleben". **Ursache:
stale Anvil-Shared-Memory.**
{{< /callout >}}

Klassisches Bild:

- Im Variables-Tab steht `TRUE` als Wert
- Die F-Checkbox ist **nicht** gesetzt (`forced = false`)
- Der ST-Code schreibt offensichtlich einen anderen Wert
  (z.B. `Bellows.LED_14 := (Position = 14);` und Position ist nirgends 14)
- Neue Compile + Deploy zeigen "Compilation finished successfully" —
  aendert aber nichts am Verhalten

Sie restarten ForgeIEC Studio, anvild, bellowsd — der Wert bleibt.

---

## Ursache

ForgeIEC nutzt die **Anvil**-Zero-Copy-Shared-Memory-Schicht fuer
die Datenuebertragung zwischen PLC-Runtime, Editor und HMI-Bruecken.
Die Shared-Memory-Segmente und die gemeinsame Service-Registry
liegen als Dateien unter `/dev/shm/` bzw. unterhalb von `/tmp/`.

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

{{< callout type="solution" title="Loesung — PLC-Runtime neu starten" >}}
Anvil raeumt die Segmente **abgestuerzter Peers** selbst auf: bei
jeder Neuerzeugung eines Anvil-Node werden die Ressourcen toter
Nodes zurueckgeholt — ohne lebende Peers anzutasten. Ein Neustart
der PLC-Runtime genuegt deshalb:

In ForgeIEC Studio ueber das Runtime-Menue `Stop` + `Start`, oder
direkt `Build → Compile and Upload`. Die SHM-Topics werden dabei
frisch angelegt, ohne stale Payload.
{{< /callout >}}

Nach dem naechsten Scan-Zyklus zeigt der Live-Monitor den korrekten,
von Ihrer Programm-Logik berechneten Wert.

{{< callout type="warning" title="SHM-Dateien nicht von Hand loeschen" >}}
Aeltere Anleitungen empfahlen ein `rm -rf` auf die SHM-Dateien als
Notloesung. **Tun Sie das nicht im laufenden Betrieb.** Segmente und
Service-Registry sind die **gemeinsame Ablage aller Anvil-Peers** —
anvild, bellowsd, hearth und die tongs-Bridges haengen daran. Ein
pauschaler Wipe reisst den lebenden Peers ihre Segmente weg; der
Anvil-Bus bricht danach **still** auseinander, ohne Retry und ohne
Selbstheilung.

Aus genau diesem Grund raeumt anvild inzwischen weder beim Start
noch beim PLC-Stop pauschal auf — das Aufraeumen macht die
Anvil-Schicht gezielt pro totem Node.

Bleibt im Restfall doch etwas haengen: alle Anvil-Peers gemeinsam
stoppen (`bellowsd`, `hearth`, `tongs-*`, `anvild`) und danach wieder
starten. Ohne lebende Nodes werden die Segmente toter Nodes sauber
zurueckgeholt.
{{< /callout >}}

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
Runtime-Neustart die einfachste Loesung. Bei wiederholtem Auftreten
ohne AI-Aktivitaet bitte das Vorkommen melden (mit
`journalctl -u anvild` und `journalctl -u bellowsd` der letzten
Stunde) an blacksmith@forgeiec.io — gezieltes, selektives Aufraeumen
toter Nodes aus dem Studio heraus ist ein laufender Backlog-Punkt.

---

## Verwandt

- [Online-Hilfe](/help/online/) — kontext-sensitive Editor-Hilfe
- [Tests](/help/tests/) — automatisierte Testabdeckung
