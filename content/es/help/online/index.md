---
title: "Ayuda en linea"
summary: "Punto de entrada para la ayuda contextual desde el editor ForgeIEC"
---

## Ayuda en linea — ¿Que es?

La ayuda en linea es la capa de ayuda contextual del editor ForgeIEC.
Al pulsar **F1** en el editor, su navegador se abre directamente en la
pagina de ayuda del elemento actualmente enfocado (dialogo, panel,
tabla de variables, accion de generacion de codigo, ...).

## Esquema de URL

Todas las paginas de ayuda viven bajo un esquema uniforme:

```
https://forgeiec.io/<idioma>/help/<tema>/
```

- `<idioma>` sigue la locale del editor (de, en, fr, es, ja, tr, zh, ar);
  por defecto `de` si no existe una pagina localizada
- `<tema>` es un slug identico en todos los idiomas, no traducido

Asi puede abrir una pagina de ayuda directamente en el navegador sin
iniciar el editor.

## Temas disponibles

### Editor & lenguajes

- [Structured Text (ST)](/es/help/st/) — Editor ST + fundamentos del lenguaje
- [Instruction List (IL)](/es/help/il/) — lenguaje IEC basado en acumulador
- [Function Block Diagram (FBD)](/es/help/fbd/) — cableado grafico de funciones y bloques funcionales
- [Ladder Diagram (LD)](/es/help/ld/) — metafora del esquema electrico: contactos, bobinas
- [Sequential Function Chart (SFC)](/es/help/sfc/) — modelo paso-transicion para secuenciadores

### Modelo & variables

- [Gestion de variables](/es/help/variables/) — panel Variables como vista central del FAddressPool
- [Biblioteca](/es/help/library/) — biblioteca estandar IEC + extensiones ForgeIEC + bloques definidos por usuario
- [Panel de propiedades](/es/help/properties-panel/) — editor inline para el elemento de bus seleccionado
- [Preferencias](/es/help/preferences/) — dialogo central de configuracion: editor, runtime, PLC, asistente IA

### Bus & hardware

- [Configuracion de bus](/es/help/bus-config/) — esquema XML PLCopen para configuracion de buses de campo industriales

### General

- [Cobertura de pruebas](/es/help/tests/) — 117 pruebas automatizadas para el conjunto de caracteristicas IEC, bloques estandar y multi-tasking
- [Filosofia de Codigo Abierto](/es/help/open-source/) — contexto

## En el editor

- **F1** en un elemento enfocado → pagina de ayuda contextual
- **Ayuda → Ayuda en linea** en el menu principal → punto de entrada (esta pagina)
- **Ayuda → Acerca de ForgeIEC** → informacion de version + licencia
