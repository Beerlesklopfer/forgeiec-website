---
title: "Añadir una variable"
summary: "El FAddVariableDialog — todos los campos en un único modal, patrones de rango para creación masiva, envoltorio de array"
---

## Visión general

El **FAddVariableDialog** es la ventana modal usada para añadir una
nueva variable a una POU o al pool. Recoge todos los campos en un único
paso y muestra una **vista previa en vivo** de la declaración IEC ST
resultante justo debajo del formulario — lo que escriba se renderiza
inmediatamente como un fragmento `VAR ... END_VAR` terminado.

El diálogo funciona en dos modos:

  - **Modo Añadir**: campos vacíos, OK crea una nueva variable.
    Accesible mediante el icono más en el panel de variables o
    Ctrl+N en el editor de POU.
  - **Modo Editar**: doble clic en una variable existente del panel —
    el mismo diálogo, con todos los campos precompletados.

## Campos

| Campo | Obligatorio | Significado |
|---|---|---|
| **Nombre** | sí | Nombre visible para el programador. Validado contra las reglas de identificadores IEC (letra + letras/dígitos/`_`). Se usa para creación masiva con un patrón de rango (véase abajo). |
| **Tipo** | sí | Combo con tipos elementales IEC, FBs estándar, FBs del proyecto, tipos de datos del usuario. La creación de arrays se gestiona mediante la casilla del envoltorio. |
| **Dirección** | depende de la POU | Var-class — véase abajo. |
| **Inicial** | no | Valor inicial (`FALSE`, `0`, `T#100ms`, `'OFF'`). |
| **Address** | no | Solo para POU de tipo VarList. Vacío = `pool->nextFreeAddress` asigna automáticamente al crear. |
| **Retain** | no | Casilla — RETAIN, el valor sobrevive a un ciclo de alimentación. |
| **Constant** | no | Casilla — `VAR CONSTANT`, no escribible en tiempo de ejecución. |
| **Envoltorio Array** | no | Envuelve el tipo seleccionado en `ARRAY [..] OF`. |
| **Documentation** | no | Comentario de texto libre, almacenado como `<documentation>` en PLCopen XML. |

## Patrón de rango para creación masiva

En lugar de escribir `LED_0`, `LED_1`, ... `LED_7` individualmente
puede especificar un **patrón de rango** en el campo de nombre:

| Entrada | Efecto |
|---|---|
| `LED_0..7` | Crea ocho variables de `LED_0` hasta `LED_7`. |
| `LED_0-7` | Sinónimo, mismo efecto. |
| `Sensor_1..3` | Crea tres variables de `Sensor_1` hasta `Sensor_3`. |

En cada creación masiva la dirección se incrementa si está establecida:
`%QX0.0` → `%QX0.0`, `%QX0.1`, ..., `%QX0.7`.

## Casilla del envoltorio Array

Si quiere declarar **una** variable como array, marque la casilla del
array. Aparecen dos spin boxes para el rango de índice y el tipo se
envuelve en tiempo de ejecución como `ARRAY [..] OF <type>`.

| Combo Tipo | Casilla Array | Rango de índice | Declaración resultante |
|---|---|---|---|
| `INT` | desactivada | — | `: INT;` |
| `INT` | activada | `0..7` | `: ARRAY [0..7] OF INT;` |
| `BOOL` | activada | `1..16` | `: ARRAY [1..16] OF BOOL;` |
| `T_Motor` (struct de usuario) | activada | `0..3` | `: ARRAY [0..3] OF T_Motor;` |

El envoltorio reside deliberadamente en una casilla en lugar de en el
combo de tipo — eso mantiene el combo despejado y le permite construir
arrays de cualquier cosa sin buscar en el combo.

## Combo de tipo

El combo agrega cuatro fuentes en una única lista:

  1. **Tipos elementales IEC**: `BOOL`, `BYTE`, `WORD`, `DWORD`, `LWORD`,
     `INT`, `DINT`, `LINT`, `UINT`, `UDINT`, `ULINT`, `REAL`, `LREAL`,
     `TIME`, `DATE`, `TIME_OF_DAY`, `DATE_AND_TIME`, `STRING`, `WSTRING`.
  2. **FBs estándar** de la biblioteca: `TON`, `TOF`, `TP`, `R_TRIG`,
     `F_TRIG`, `CTU`, `CTD`, `CTUD`, `SR`, `RS`, ...
  3. **Bloques de función del proyecto** — todo FB declarado en el
     proyecto actual (biblioteca de usuario).
  4. **Tipos de datos de usuario** de `<dataTypes>`: STRUCTs, enums, alias.

Las plantillas ARRAY **no** aparecen en el combo — pasan por la casilla
del envoltorio.

## Dirección (var-class) por tipo de POU

Qué valores de dirección se ofrecen depende del tipo de POU:

| Tipo de POU | Dirección disponible |
|---|---|
| `PROGRAM` / `FUNCTION_BLOCK` / `FUNCTION` | `VAR` / `VAR_INPUT` / `VAR_OUTPUT` / `VAR_IN_OUT` / `VAR_TEMP` |
| `GlobalVarList` (GVL) | Fijo `VAR_GLOBAL` — combo oculto. |
| `AnvilVarList` | Fijo `VAR_GLOBAL` (autogenerado) — combo oculto. |
| Globales del pool (sin contenedor POU) | Sin dirección — la dirección `%I`/`%Q` la establece implícitamente. |

## Modo edición

Doble clic en una variable existente del panel de variables abre el
mismo diálogo. Cada campo está precompletado; en OK los cambios se
enrutan a través de `pou->renameVariable` / `pool->rebind` (de modo
que los índices `byAddress` permanezcan sincronizados). El diálogo
detecta el modo edición por `existing != nullptr`.

## Ejemplo — 8 LEDs en un solo bloque

Ocho LEDs de salida como variables del pool, en un solo paso:

  - **Nombre**: `LED_0..7`
  - **Tipo**: `BOOL`
  - **Dirección**: oculta (global del pool)
  - **Address**: `%QX0.0` (autoincremento)
  - **Inicial**: `FALSE`

OK crea ocho entradas en el pool:

```text
LED_0  AT %QX0.0 : BOOL := FALSE;
LED_1  AT %QX0.1 : BOOL := FALSE;
LED_2  AT %QX0.2 : BOOL := FALSE;
LED_3  AT %QX0.3 : BOOL := FALSE;
LED_4  AT %QX0.4 : BOOL := FALSE;
LED_5  AT %QX0.5 : BOOL := FALSE;
LED_6  AT %QX0.6 : BOOL := FALSE;
LED_7  AT %QX0.7 : BOOL := FALSE;
```

Las ocho variables pueden seleccionarse después en el panel de
variables y asignarse a un grupo HMI mediante una operación masiva —
p. ej. `Set HMI Group... -> Frontpanel`.

## Temas relacionados

  - [Gestión de variables](../) — el panel de variables con columnas,
    filtros y operaciones masivas.
  - [Formato de archivo de proyecto](../../file-format/) — cómo se
    persiste el pool como bloque `<addData>` en PLCopen XML.
