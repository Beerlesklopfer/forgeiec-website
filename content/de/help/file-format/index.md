---
title: "Projekt-Dateiformat (.forge)"
summary: "Aufbau der ForgeIEC-Projektdatei: PLCopen-XML mit ForgeIEC-Erweiterungen"
---

## Ueberblick

Eine ForgeIEC-Projektdatei traegt die Endung **`.forge`** (Alt-Endung
`.forgeiec` wird beim Laden weiterhin akzeptiert) und ist ein normales
**PLCopen-TC6-XML-Dokument** mit einigen ForgeIEC-spezifischen
Erweiterungen, die ueber den standardkonformen `<addData>`-Mechanismus
eingeklinkt sind. Die Datei ist UTF-8-kodiert, mensch-lesbar, in beliebigem
XML-Editor diff-bar und in Git versionierbar.

```
.forge-Datei
  +-- <project>            ← PLCopen-Wurzelelement
        +-- <fileHeader>   Meta (Werkzeugname, Datum)
        +-- <contentHeader> Autor, Projektname
        +-- <types>        Datentypen + POUs (PROGRAM/FB/FUNCTION + GVLs)
        +-- <instances>    Resource/Task-Konfiguration
        +-- <addData>      ForgeIEC-Erweiterungen (Bus, Pool, ...)
```

## Wurzelelement

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://www.plcopen.org/xml/tc6_0201">
  <fileHeader companyName="ForgeIEC"
              creationDateTime="2026-04-30T12:00:00"
              productName="ForgeIEC"
              productVersion="0.1.0"/>
  <contentHeader author="Joerg Bernau" name="Ackersteuerung"/>
  ...
</project>
```

| Attribut | Bedeutung |
|---|---|
| `xmlns` | PLCopen-TC6-Namespace (fest) |
| `companyName` | Erzeuger-Werkzeug — bei ForgeIEC immer `"ForgeIEC"` |
| `creationDateTime` | ISO-8601-Zeitstempel der ersten Erstellung |
| `productVersion` | Editor-Version, mit der das Projekt geschrieben wurde |
| `author` | Frei waehlbarer Autor-Name |
| `name` | Projektname (UI-Label, kein Dateiname) |

## `<types>` — Bibliothek + POUs

Enthaelt drei Sektionen:

### `<dataTypes>`

User-definierte Datentypen (STRUCT, Enumerationen, Aliase).

```xml
<dataTypes>
  <dataType name="ST_KcCurve">
    <baseType>
      <struct>
        <variable name="days_initial"><type><INT/></type></variable>
        <variable name="days_growing"><type><INT/></type></variable>
      </struct>
    </baseType>
  </dataType>
</dataTypes>
```

### `<pous>`

Alle Programm-Organisations-Einheiten:

| pouType | Bedeutung |
|---|---|
| `program`        | PROGRAM (top-level Code) |
| `functionBlock`  | FUNCTION_BLOCK (instanziierbar, mit Zustand) |
| `function`       | FUNCTION (zustandslos, hat `returnType`) |

Jede POU hat `<interface>` (Variablen-Deklarationen, gegliedert in
`<inputVars>`, `<outputVars>`, `<inOutVars>`, `<localVars>`,
`<externalVars>`, `<tempVars>`) und einen `<body>`, der den ST-Quellcode
in einem `<ST>`-Element traegt.

```xml
<pou name="PLC_PRG" pouType="program">
  <interface>
    <localVars>
      <variable name="counter"><type><INT/></type></variable>
    </localVars>
  </interface>
  <body>
    <ST>
      <xhtml xmlns="http://www.w3.org/1999/xhtml">counter := counter + 1;</xhtml>
    </ST>
  </body>
</pou>
```

### Spezielle POU-Typen (ForgeIEC-Erweiterung)

ForgeIEC kennt fuenf Listenformen, die als POU mit eigenem `pouType`
gespeichert werden:

| pouType            | Zweck |
|---|---|
| `globalVarList`    | GVL — programmer-visible Variablen-Pool |
| `tempVarList`      | TVL — VAR_TEMP-Liste |
| `persistVarList`   | PVL — VAR_PERSIST-Liste (RETAIN) |
| `anvilVarList`     | AnvilVarList — auto-generated PUBLISH/SUBSCRIBE |
| `hmiVarList`       | HmiVarList — Bellows-HMI-Export |

## `<instances>` — Resource / Task

```xml
<instances>
  <configurations>
    <configuration name="config0">
      <resource name="resource0">
        <task name="task0" interval="T#20ms" priority="0"/>
        <pouInstance name="instance0" taskName="task0" typeName="PLC_PRG"/>
      </resource>
    </configuration>
  </configurations>
</instances>
```

`interval` setzt die Zykluszeit. Mehrere Tasks sind moeglich; jede Task
fuehrt eine oder mehrere Programm-Instanzen aus.

## `<addData>` — ForgeIEC-Erweiterungen

PLCopen TC6 erlaubt vendor-spezifische Daten unter `<addData>`. ForgeIEC
nutzt mehrere Namespaces:

| Namespace | Inhalt |
|---|---|
| `https://forgeiec.io/v2/bus-config`  | Bus-Segmente + Devices ([Detail](/help/bus-config/)) |
| `https://forgeiec.io/v2/address-pool`| Adress-Pool: located variables, Bus-Bindings, Tags |
| `https://forgeiec.io/v2/monitoring`  | UI-Status: welche Variablen werden live ueberwacht |

Ein typischer Aufbau:

```xml
<addData>
  <data name="https://forgeiec.io/v2/bus-config" handleUnknown="discard">
    <fi:busConfig xmlns:fi="https://forgeiec.io/v2">
      <fi:segment ...>
        <fi:device ...>
          <fi:module .../>
        </fi:device>
      </fi:segment>
    </fi:busConfig>
  </data>
</addData>
```

`handleUnknown="discard"` ist die PLCopen-Direktive: ein Werkzeug, das
diesen Block nicht versteht, darf ihn ignorieren — die Datei bleibt
trotzdem ein gueltiges PLCopen-XML.

### Adress-Pool

Der Adress-Pool ist **die einzige Quelle der Wahrheit** fuer die
Variablen einer Anlage. Jeder Eintrag hat als **Primaerschluessel die
IEC-Adresse** (`%IX0.0`, `%QW3`, …) — Name, Tags und Bus-Bindings sind
Beschreiber, die sich aendern koennen, ohne die Identitaet zu brechen.

```xml
<addData>
  <data name="https://forgeiec.io/v2/address-pool" handleUnknown="discard">
    <fi:pool xmlns:fi="https://forgeiec.io/v2">
      <fi:variable address="%IX0.0"
                   name="T_1"
                   anvilGroup="Pfirsich"
                   busDirection="in"
                   deviceId="0e5d5537-e328-44e6-8214-78d529b18ebd"
                   modbusAddress="0"
                   moduleSlot="0"/>
    </fi:pool>
  </data>
</addData>
```

| Attribut | Pflicht | Bedeutung |
|---|---|---|
| `address`        | ja  | IEC-Adresse — Primaerschluessel im Pool |
| `name`           | nein | Programmer-sichtbarer Name (`T_1`, `Motor_Run`) |
| `anvilGroup`     | nein | Anvil-IPC-Gruppe (Hardware-Kanal) |
| `gvlNamespace`   | nein | GVL-Zuordnung (Editor-seitige Gruppierung) |
| `hmiGroup`       | nein | Bellows-HMI-Gruppe (HMI-Kanal) |
| `busDirection`   | nein | `in` / `out` — Polling-Richtung |
| `deviceId`       | nein | UUID des Bus-Devices, an das diese Variable gebunden ist |
| `modbusAddress`  | nein | Modbus-Register-Offset relativ zum Slave |
| `moduleSlot`     | nein | Slot innerhalb des Devices |

Eine Variable kann **mehrere Tags gleichzeitig** tragen (z. B. sowohl
`anvilGroup="Pfirsich"` als auch `hmiGroup="Pfirsich"`). Damit der
ST-Compiler die Bellows-Schreibweise `Bellows.Pfirsich.T_1` akzeptiert,
muss zusaetzlich der **HMI-Export fuer die jeweilige Gruppe aktiv
geschaltet** sein — sonst bleibt das `hmiGroup`-Tag ein reiner
Beschreiber ohne Wirkung auf die Code-Generierung.

<!--
TODO (Backlog):
  1. Eigene Doku-Seite zum Bellows-Export-Schalter (genaue Bedingung:
     per-Variable-Flag vs. HmiVarList-Aktivierung).
  2. ST-Compiler: Validierungs-Pass ergaenzen, der einen Verweis auf
     ein inaktives Bellows-Tag mit einem klaren Compile-Fehler ablehnt.
-->


## ST-Sprachvorrat (Body-Inhalt)

Der `<ST>`-Body enthaelt den IEC 61131-3 Structured-Text-Code als
xhtml-Wrapper. ForgeIEC erweitert den Sprachvorrat um zwei Komfort-Features:

### Bit-Zugriff auf ANY_BIT-Typen

`var.<bit>` extrahiert/setzt ein einzelnes Bit, auch direkt auf `BYTE`/
`WORD`/`DWORD`/`LWORD`-Variablen:

```iec
bButtons.0 := IN_Buttons.0 OR Bellows.Pfirsich.T_1;
OUT_Valves.3 := jk[3].Q;
```

Wird vom Compiler in saubere Bit-Maskierung uebersetzt.

### 3-Level qualifizierte Variablen

`<Category>.<Group>.<Variable>` greift auf Pool-Eintraege zu, ohne
GVLs explizit zu deklarieren:

| Category-Prefix  | Quelle |
|---|---|
| `Anvil.X.Y`      | Pool-Variable mit `anvilGroup="X"` |
| `Bellows.X.Y`    | Pool-Variable mit `hmiGroup="X"` |
| `GVL.X.Y`        | Pool-Variable mit `gvlNamespace="X"` |
| `HMI.X.Y`        | Synonym fuer `Bellows.X.Y` |
| `POOL.X.Y`       | beliebiger Tag |

`Anvil.X.Y` und `Bellows.X.Y` koennen unabhaengig voneinander auf zwei
verschiedene Pool-Eintraege zeigen — der Compiler emittiert getrennte
C-Symbole, sobald die Pool-Eintraege unterschiedliche IEC-Adressen
tragen.

## Migration / Kompatibilitaet

* Dateiendung: `.forge` ist die kanonische Endung. `.forgeiec` (alte
  Schreibweise) wird beim Laden weiterhin akzeptiert; beim Speichern
  schreibt der Editor `.forge`.
* Das XML-Format ist abwaerts-kompatibel: aeltere ForgeIEC-Versionen
  ignorieren neue `<addData>`-Bloecke (`handleUnknown="discard"`) und
  oeffnen die Datei trotzdem.
* Standard-PLCopen-Werkzeuge oeffnen den Standard-Teil (`<types>`,
  `<instances>`) korrekt; die ForgeIEC-Erweiterungen fehlen dort,
  bleiben beim Speichern aber erhalten, wenn das Werkzeug
  `<addData>`-Bloecke ungelesen durchschleift.

## Verwandte Themen

* [Bus-Konfiguration](/help/bus-config/) — Detailschema `fi:busConfig`,
  Geraete- und Modul-Definitionen.
* [Testabdeckung](/help/tests/) — automatisierte Tests, die das Format
  round-trip-stabil halten.
