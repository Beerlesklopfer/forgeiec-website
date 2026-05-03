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

Los temas principales estan en la [vision general de ayuda](/help/).

## En el editor

- **F1** en un elemento enfocado → pagina de ayuda contextual
- **Ayuda → Ayuda en linea** en el menu principal → punto de entrada (esta pagina)
- **Ayuda → Acerca de ForgeIEC** → informacion de version + licencia
