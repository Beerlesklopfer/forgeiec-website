# XML-Schemas für ForgeIEC

Dieses Verzeichnis bündelt die XSD-Schemas, gegen die ForgeIEC seine
PLCopen-XML-Dateien validiert. Zwei Schemas, gemeinsam genutzt:

| Datei                | Owner    | Lizenz             | Zweck                                                    |
|----------------------|----------|--------------------|----------------------------------------------------------|
| `tc6_0201.xsd`       | PLCopen e.V. | (siehe XML-Header) | Offizielles PLCopen-XML-Standard-Schema (TC6 v2.01).      |
| `forgeiec-v2.xsd`    | ForgeIEC | AGPL-3.0-or-later  | Schema unserer `<addData name="forgeiec.io/v2/*">`-Erweiterungen. |

## Validierungs-Pipeline

Für eine `.forge`-Datei läuft die Validierung in zwei Pässen:

```
Pass 1 (Whole-doc):
    tc6_0201.xsd  validate  <project>-Root → strukturelle PLCopen-Korrektheit

Pass 2 (Extension):
    forgeiec-v2.xsd  validate  each <addData name="https://forgeiec.io/v2/..."/*
                              → ForgeIEC-spezifische Attribute korrekt typisiert
```

Implementiert in `editor/src/runtime/FXsdValidator.cpp` (libxml2-FFI),
siehe `documentation/sprints/plcopen-import-export.md §4.6b`.

## Bekannte Non-Konformanz von `.forge`-Files

`.forge`-Files sind **HEUTE NICHT** strikt tc6_0201-konform, weil
ForgeIEC die folgenden Extensions direkt im PLCopen-Namespace
unterbringt statt in `<addData>`:

| Verletzung                                          | Datei-Stelle                              | Plan                                |
|-----------------------------------------------------|-------------------------------------------|-------------------------------------|
| `<pou pouType="anvilVarList">`                      | POUs                                      | Phase D Vanilla-Export: repack auf `globalVarList` + addData |
| `<variable busDirection="…" deviceId="…">`          | Per-Variable                              | Phase D: Attribute in addData          |
| `<returnType>` als Sibling von `<interface>`        | Function-POUs                             | Phase D: schon im PLCopen, falsche Position fixen |
| Fehlende `<coordinateInfo>` in `<contentHeader>`    | Header                                    | Phase D: leeres `<coordinateInfo>` immer schreiben |

Phase D des PLCOPEN-IE-1-Sprints adressiert das systematisch:
Vanilla-Export erzeugt sauber konformes PLCopen, ForgeIEC-Export
behält die nicht-konformen Effizienz-Codierungen.

## Hosting

Beide Schemas sind ausserdem auf `https://forgeiec.io/schemas/`
verfügbar (Quelle: `documentation/website/`-Submodule). Importer
können wahlweise lokal (Repo-Pfad) oder online (URL) validieren.

## Hinzufügen einer neuen ForgeIEC-Extension

1. Neuen Eintrag in `forgeiec-v2.xsd` ergänzen (mit
   `targetNamespace="https://forgeiec.io/v2/<NAME>"`).
2. Element-Wrapper schreibt `xmlns="https://forgeiec.io/v2/<NAME>"`
   (User-Vorgabe §4.6a, commit 10aef31).
3. ForgeIEC-Loader (`FPlcopenXml.cpp`) liest + schreibt das neue Element.
4. Test in `tests/import/FPlcopenForeignImportTest.cpp` oder
   eigene Test-Suite ergänzen.

## Lizenzen lesen

Bevor Du die `tc6_0201.xsd` extern verteilst (z.B. eigene Webseite,
Buch, kommerzielles Tool), prüfe die PLCopen-Terms unter
<https://plcopen.org/legal/>. Wir hosten die Datei in diesem Repo +
unserer Webseite unter dem Assumption "Free download for non-
commercial and commercial use with attribution" — wenn PLCopen das
anders sieht, Kontakt: `blacksmith@forgeiec.io`.
