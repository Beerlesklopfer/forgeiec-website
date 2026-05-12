---
title: "FAQ"
summary: "Wachsende Sammlung haeufiger Fragen + Loesungen aus der Praxis"
---

## Haeufig gestellte Fragen

Hier sammeln wir Symptome + Loesungen, die in Devloop oder Inbetrieb-
nahme regelmaessig vorkommen. Jeder Eintrag ist nach **Symptom** sortiert
und nennt sowohl die schnelle Abhilfe als auch den eigentlichen Grund —
damit Sie nicht nur das aktuelle Problem loesen, sondern auch verstehen
warum es auftrat.

Die FAQ waechst mit dem Projekt — wenn Sie einen Fall haben der hier
fehlt, schreiben Sie an blacksmith@forgeiec.io oder oeffnen Sie ein
Issue.

---

## Themen

### [Variablen bleiben "haengen" trotz frischem Deploy](/help/faq/stuck-variables-shm/)

Eine BOOL- oder INT-Variable behaelt einen Wert (TRUE/FALSE oder einen
Zahlenwert) der nicht zur Programm-Logik passt. `monitor.snapshot`
meldet `forced=false`, der ST-Code schreibt offensichtlich einen anderen
Wert — und trotzdem bleibt der Wert "kleben". Ursache: stale iceoryx2
Shared-Memory.

---

<div style="text-align:center; padding: 2rem;">

**Fragen wachsen mit dem Projekt — und die Antworten wachsen mit.**

blacksmith@forgeiec.io

</div>
