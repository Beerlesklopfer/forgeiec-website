---
title: "FAQ"
summary: "Wachsende Sammlung häufiger Fragen + Lösungen aus der Praxis"
---

## Häufig gestellte Fragen

Hier sammeln wir Symptome + Lösungen, die in Devloop oder Inbetrieb-
nahme regelmäßig vorkommen. Jeder Eintrag ist nach **Symptom** sortiert
und nennt sowohl die schnelle Abhilfe als auch den eigentlichen Grund —
damit Sie nicht nur das aktuelle Problem lösen, sondern auch verstehen
warum es auftrat.

Die FAQ wächst mit dem Projekt — wenn Sie einen Fall haben der hier
fehlt, schreiben Sie an blacksmith@forgeiec.io oder öffnen Sie ein
Issue.

---

## Themen

### [Variablen bleiben "hängen" trotz frischem Deploy](/help/faq/stuck-variables-shm/)

Eine BOOL- oder INT-Variable behält einen Wert (TRUE/FALSE oder einen
Zahlenwert) der nicht zur Programm-Logik passt. `monitor.snapshot`
meldet `forced=false`, der ST-Code schreibt offensichtlich einen anderen
Wert — und trotzdem bleibt der Wert "kleben". Ursache: stale Anvil-
Shared-Memory.

---

<div style="text-align:center; padding: 2rem;">

**Fragen wachsen mit dem Projekt — und die Antworten wachsen mit.**

blacksmith@forgeiec.io

</div>
