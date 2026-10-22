---
title: "ForgeIEC"
description: "Steuerungssoftware nach IEC 61131-3 für Maschinen- und Anlagenbauer: ohne Lizenzgebühr pro Gerät, ohne Herstellerbindung. Vorabversion 0.2, im Pilotbetrieb."
more: "Mehr erfahren"

hero:
  eyebrow: "IEC 61131-3 · Vorabversion 0.2"
  title: "Ihre Steuerung. Ohne Gerätelizenz, ohne Herstellerbindung."
  lead: "ForgeIEC ist Steuerungssoftware für Maschinen- und Anlagenbauer: programmieren nach IEC 61131-3, auf Linux-Industrierechnern betreiben, Feldgeräte und Bedienung anbinden. Open Source – eine kommerzielle Lizenz gibt es auf Anfrage."
  secondaryLabel: "Download"
  secondaryHref: "/download/"
  meta:
    - "Im Pilotbetrieb bei einer SoLaWi"
    - "Linux, Windows-Build vorhanden"
    - "Ihr Steuerungsprogramm bleibt Ihres"

problem:
  eyebrow: "Das Problem"
  title: "Steuerungssoftware bindet – an Lizenzen, Hersteller und Dienste."
  items:
    - "Bei vielen Anbietern kostet die Laufzeitlizenz Geld – pro Steuerung, mit jeder ausgelieferten Maschine aufs Neue."
    - "Wer sich für ein System entscheidet, bindet Programme, Hardware und Wissen an die Werkzeuge eines Herstellers."
    - "Und Fernwartung führt oft über offene Ports oder über die Cloud eines Dritten."

solution:
  eyebrow: "Die Lösung"
  title: "Eine Plattform für Programmieren, Betreiben und Anbinden."
  lead: "ForgeIEC deckt den Weg vom Programm bis zum Feldgerät ab – mit offenen Lizenzen und auf Hardware, die Sie selbst wählen."
  cards:
    - icon: "code"
      kicker: "Programmieren"
      title: "Strukturierter Text nach IEC 61131-3"
      text: "Ein eigener Editor mit eigenem Compiler-Kern, der auch objektorientierte Bausteine versteht."
      points:
        - "ST heute im Einsatz; FUP, KOP, AS und AWL folgen"
        - "Gerätebeschreibungen der Hersteller direkt im Projekt"
      href: "/plattform/forge-studio/"
    - icon: "cpu"
      kicker: "Betreiben"
      title: "Laufzeit auf Industrie-Hardware"
      text: "Die Laufzeitumgebung läuft als Dienst auf Linux-Rechnern mit x86 oder ARM. Programme kommen über das Netzwerk auf die Steuerung."
      points:
        - "Variablen live beobachten und Verläufe aufzeichnen"
        - "Updates als signierte Pakete aus dem apt-Repository"
      href: "/plattform/anvil/"
    - icon: "plug"
      kicker: "Anbinden"
      title: "Feldbusse, Funk und Bedienung"
      text: "Jedes Protokoll hat eine eigene Brücke. Fällt eine aus, läuft der Rest weiter."
      points:
        - "Modbus TCP und RTU verfügbar, LoRaWAN in Arbeit"
        - "Bedienoberfläche Hearth als Vorschau"
      href: "/plattform/tongs/"

rivet:
  eyebrow: "Rivet · Fernzugriff"
  title: "Fernzugriff auf Ihre Maschinen – ohne offenen Port und ohne fremde Cloud."
  lead: "Rivet verbindet das Handy mit der Steuerung. Ein kleines Gateway neben der Steuerung baut die Verbindung selbst nach außen auf – im Netz der Anlage wird kein Port geöffnet."
  points:
    - title: "Keine Portfreigabe"
      text: "Keine öffentliche IP-Adresse, kein DynDNS. Funktioniert auch hinter CGNAT und am LTE-Anschluss."
    - title: "Kein Dritter im Datenpfad"
      text: "Gateway und Server sind eigene Infrastruktur, kein Cloud- oder VPN-Anbieter dazwischen. Der Server reicht die Verbindung nur verschlüsselt weiter und sieht keine Inhalte."
    - title: "Nur die freigegebene Steuerung ist erreichbar"
      text: "Das Handy erreicht nur die freigegebene Steuerung auf den freigegebenen Ports. Andere Geräte im Netz bleiben unerreichbar."
  linkLabel: "Rivet im Detail"
  href: "/rivet/"
  status: "in Entwicklung · Pilot mit SoLaWis"
  caption: "Das Gateway baut den Tunnel von innen auf; der Server vermittelt nur."

status:
  eyebrow: "Ehrlicher Stand"
  title: "Was heute geht – und was noch nicht."
  lead: "ForgeIEC ist eine Vorabversion (0.2). Der ST-Editor ist beim Pilotkunden produktiv im Einsatz; vieles andere ist in Arbeit."
  colArea: "Bereich"
  colDetail: "Was das heißt"
  colState: "Stand"
  legendUse: "läuft beim Pilotkunden bzw. ist verfügbar"
  legendWip: "wird entwickelt, noch nicht fertig"
  legendPlan: "vorgesehen"
  legendRest: "derzeit nicht in Entwicklung"
  rows:
    - area: "Programmieren in ST"
      detail: "Editor, eigener Compiler-Kern, Übertragung auf die Steuerung"
      state: "use"
    - area: "FUP, KOP, AS, AWL"
      detail: "Grafische und weitere Sprachen: Editoren in Arbeit, noch nicht übersetzbar"
      state: "wip"
    - area: "Laufzeit auf Linux"
      detail: "Anvil-Server (anvild) für Debian und Ubuntu, signierte Pakete"
      state: "use"
    - area: "Modbus TCP und RTU"
      detail: "Anbindung von Feldgeräten über Modbus"
      state: "use"
      label: "verfügbar"
    - area: "LoRaWAN"
      detail: "Funk-Sensorik für weitläufige Anlagen – unser Schwerpunkt für die SoLaWis"
      state: "wip"
    - area: "EtherCAT, PROFIBUS, EtherNet/IP"
      detail: "Grundgerüst steht, die Protokolle sind in Arbeit; weitere Busse folgen"
      state: "wip"
    - area: "Bedienoberfläche Hearth"
      detail: "Läuft über den internen Anvil-Bus"
      state: "wip"
      label: "Vorschau"
    - area: "Fernzugriff Rivet"
      detail: "Sicherer Zugriff vom Handy ohne Portfreigabe"
      state: "wip"
      label: "in Entwicklung · Pilot SoLaWis"
    - area: "Windows"
      detail: "Ein Windows-Build existiert, seine CI läuft; Installer auf Anfrage"
      state: "wip"
      label: "auf Anfrage"
    - area: "OPC-UA-Gateway bellowsd"
      detail: "Paket bleibt im apt-Repository, wird derzeit nicht weiterentwickelt"
      state: "rest"

trust:
  eyebrow: "Vertrauen"
  title: "Klare Regeln, bevor Sie sich entscheiden."
  facts:
    - icon: "scale"
      title: "Lizenz"
      text: "Studio, Laufzeit-Dienst und Busbrücken stehen unter AGPL-3.0-or-later. Was in Ihr Projekt eingebunden wird – generierter Code, Laufzeit-Schnittstellen, libanvil – steht unter Apache-2.0. Eine kommerzielle Lizenz ist möglich."
    - icon: "alert"
      title: "Kein Ersatz für eine Sicherheitssteuerung"
      text: "ForgeIEC ist keine Sicherheits-SPS und hat keine SIL- oder PL-Einstufung. Not-Halt und Schutzfunktionen gehören auf dafür zugelassene Sicherheitstechnik."
    - icon: "package"
      title: "Linux und Windows"
      text: "Linux-Pakete kommen signiert aus einer automatisierten CI über das apt-Repository. Ein Windows-Build existiert und seine CI läuft; den Installer gibt es auf Anfrage."
    - icon: "chat"
      title: "Support und kommerzielle Lizenz"
      text: "Auf Anfrage. Der Quellcode steht unter AGPL; Zugang zu den Repositories auf Anfrage."

faq:
  title: "Häufige Fragen zur Lizenz"
  disclaimer: "Information, keine Rechtsberatung. Maßgeblich sind die Lizenztexte."
  items:
    - q: "Muss ich mein SPS-Programm offenlegen?"
      a: "Nein. Der generierte Steuerungscode und die Laufzeit-Schnittstellen, die in Ihr Projekt eingebunden werden (Runtime-API, libanvil), stehen unter Apache-2.0. Sie dürfen darauf auch eigene, geschlossene Bibliotheken bauen. Das Studio, der Laufzeit-Dienst und die Busbrücken stehen unter AGPL-3.0-or-later. Eine kommerzielle Lizenz ist möglich."
    - q: "Was gilt, wenn ich ForgeIEC selbst verändere?"
      a: "Änderungen am Studio, am Laufzeit-Dienst oder an den Busbrücken fallen unter die AGPL: Geben Sie die veränderte Software weiter oder bieten Sie sie über ein Netzwerk an, müssen Sie den Quellcode dieser Änderungen zugänglich machen. Wer das nicht möchte, fragt nach einer kommerziellen Lizenz."
    - q: "Fallen Lizenzgebühren pro Steuerung an?"
      a: "Unter den offenen Lizenzen nicht. Support und eine kommerzielle Lizenz gibt es auf Anfrage."
    - q: "Bekomme ich den Quellcode?"
      a: "Ja. Der Quellcode steht unter AGPL; den Zugang zu den Repositories gibt es auf Anfrage an blacksmith@forgeiec.io."

proof:
  eyebrow: "Im Einsatz"
  title: "Pilotbetrieb bei der SoLaWi Ackervielfalt"
  text: "Die SoLaWi Ackervielfalt, eine solidarische Landwirtschaft, ist der Pilotkunde von ForgeIEC: Ihre Steuerungsprogramme entstehen im ST-Editor, der dort produktiv eingesetzt wird. Weitere SoLaWis folgen."

cta:
  title: "Sprechen wir über Ihre Maschine."
  text: "Sie bauen Maschinen oder Anlagen und möchten ForgeIEC in einem Pilotprojekt erproben? Schreiben Sie, was Sie steuern wollen – Jörg Bernau antwortet persönlich."
  secondaryLabel: "Zum Download"
  secondaryHref: "/download/"
---
<!-- Der Inhalt der Startseite steht vollständig im Front Matter (layouts/index.html). -->
<!-- ENTWURF: Lizenz-FAQ (faq.items) muss vor der Veröffentlichung von einem Anwalt gelesen werden; Information, keine Rechtsberatung. -->
