---
title: "Biblioteca (Bloques de función + Funciones)"
summary: "Biblioteca estándar IEC 61131-3 + extensiones de ForgeIEC + bloques definidos por el usuario"
---

## Visión general

La biblioteca de ForgeIEC es la colección central de todos los bloques
reutilizables que un programa de aplicación puede invocar desde un
proyecto `.forge` — abarcando tanto los bloques de función y funciones
estandarizados de IEC 61131-3, como las extensiones específicas del
proyecto o de ForgeIEC.

La biblioteca se muestra en el **panel Biblioteca** (acoplamiento
predeterminado: barra lateral derecha). Pulse **F1** mientras el panel
Biblioteca tenga el foco para abrir esta página.

```
Library
+-- Standard Function Blocks    (Bistable, Edge, Counter, Timer, ...)
+-- Standard Functions          (Arithmetic, Comparison, Bitwise, ...)
+-- User Library                (project-specific blocks)
```

Actualmente la biblioteca incluye **casi 100 bloques** y **algo más de
30 funciones**. Cada entrada incluye:

  - **Nombre** (p. ej. `TON`, `JK_FF`)
  - **Lista de pines** (entradas + salidas con tipo y posición)
  - **Tipo** (`FUNCTION_BLOCK` con estado, o `FUNCTION` sin estado)
  - **Descripción** + **texto de ayuda** con notas de uso
  - **Ejemplo de código** (visible en el panel de ayuda de la biblioteca)

## Árbol de categorías

### Bloques de función estándar

| Grupo | Bloques |
|---|---|
| **Biestables** | `SR`, `RS` — set/reset con prioridad |
| **Detección de flancos** | `R_TRIG`, `F_TRIG` — flanco ascendente/descendente |
| **Contadores** | `CTU`, `CTD`, `CTUD` — contar arriba / abajo / ambos |
| **Temporizadores** | `TON`, `TOF`, `TP` — retardo a la conexión / a la desconexión / impulso |
| **Movimiento** | perfiles, rampas, trayectorias (en preparación) |
| **Generación de señales** | FBs generadores para señales de prueba y validación |
| **Manipuladores de funciones** | hold, latch, historial |
| **Control en lazo cerrado** | PID, histéresis, dos puntos |
| **Aplicación** *(ForgeIEC)* | `JK_FF`, `DEBOUNCE` — bloques cercanos a la aplicación que han demostrado ser universalmente útiles en la práctica |

### Funciones estándar

| Grupo | Contenido |
|---|---|
| **Aritmética** | `ADD`, `SUB`, `MUL`, `DIV`, `MOD` (sobre cualquier tipo ANY_NUM) |
| **Comparación** | `EQ`, `NE`, `LT`, `LE`, `GT`, `GE` |
| **Bit a bit** | `AND`, `OR`, `XOR`, `NOT` (sobre ANY_BIT — véase `help/st`) |
| **Desplazamiento de bits** | `SHL`, `SHR`, `ROL`, `ROR` |
| **Selección** | `SEL`, `MAX`, `MIN`, `LIMIT`, `MUX` |
| **Numéricas** | `ABS`, `SQRT`, `LN`, `LOG`, `EXP`, `SIN`, `COS`, `TAN`, `ASIN`, `ACOS`, `ATAN` |
| **Cadenas** | `LEN`, `LEFT`, `RIGHT`, `MID`, `CONCAT`, `INSERT`, `DELETE`, `REPLACE`, `FIND` |
| **Conversión de tipos** | `BOOL_TO_INT`, `REAL_TO_DINT`, `STRING_TO_INT`, ... |

### Biblioteca de usuario

Bloques de función y funciones definidos en el proyecto — todo lo
declarado como `FUNCTION_BLOCK` o `FUNCTION` aterriza automáticamente
en esta categoría y puede invocarse desde cualquier parte del proyecto,
igual que los bloques estándar.

## Panel Biblioteca — uso

| Acción | Efecto |
|---|---|
| **Buscar** (lupa en la parte superior) | Filtra la vista en árbol por nombre de bloque — escribir `to` encuentra `TON`. |
| **Doble clic** sobre un bloque | Abre la ayuda del bloque en un panel de detalle: descripciones de pines + ejemplo de código. |
| **Arrastrar** al editor ST | Inserta la llamada al bloque en la posición del cursor, incluida la declaración de instancia en la sección local `VAR_INST`. |
| **Clic derecho > "Insert Call..."** | Igual que arrastrar, mediante el menú contextual. |
| **F1** sobre un bloque | Abre esta página. |

## Ejemplo 1 — Antirrebote de pulsador con `DEBOUNCE`

`DEBOUNCE` filtra impulsos cortos de ruido del contacto de un pulsador
mecánico. `Q` solo cambia cuando `IN` permanece estable durante toda la
duración `T_Debounce` — tanto en flanco ascendente como descendente.

### Distribución de pines

| Pin | Dirección | Tipo | Significado |
|---|---|---|---|
| `IN`         | INPUT  | `BOOL` | Entrada cruda (típicamente `%IX`, con rebote mecánico) |
| `tDebounce`  | INPUT  | `TIME` | Tiempo mínimo estable (típicamente `T#10ms`...`T#50ms`) |
| `Q`          | OUTPUT | `BOOL` | Salida sin rebotes |

### Ejemplo de código

Cuerpo de PROGRAM que realiza el antirrebote de un pulsador en `%IX0.0`
y reenvía la señal sin rebotes como flanco único a un contactor con
autorretención:

```text
PROGRAM PLC_PRG
VAR
    button_raw      AT %IX0.0 : BOOL;       (* bouncing contact *)
    button_clean    : BOOL;                  (* after DEBOUNCE *)
    button_pressed  : BOOL;                  (* single-shot per press *)
    relay_lamp      AT %QX0.0 : BOOL;        (* lamp as self-hold *)
    fbDeb           : DEBOUNCE;              (* instance *)
    fbTrig          : R_TRIG;                (* edge detector *)
END_VAR

fbDeb(IN := button_raw, tDebounce := T#20ms);
button_clean := fbDeb.Q;

fbTrig(CLK := button_clean);
button_pressed := fbTrig.Q;

(* Self-hold: toggle on every rising edge *)
IF button_pressed THEN
    relay_lamp := NOT relay_lamp;
END_IF;
END_PROGRAM
```

`DEBOUNCE` se construye internamente con dos bloques `TON` (dirección
alta y baja) — uno lleva `Q` a TRUE solo tras `T_Debounce` con `IN`
activo, el otro lo lleva a FALSE solo tras `T_Debounce` con `IN`
inactivo. Esto hace el filtro simétrico: ni el rebote del contacto al
pulsar ni al soltar producen un fallo.

> **Uso típico:** pulsadores mecánicos, finales de carrera, sensores
> basados en contacto. Para "un solo disparo por pulsación" — como se
> muestra arriba — encadene un `R_TRIG` después de `Q`.

## Ejemplo 2 — Autorretención con anulación de modo (`JK_FF`)

`JK_FF` es un flipflop biestable con antirrebote de pulsador
incorporado. En cada flanco ascendente estable de `xButton` conmuta `Q`
entre TRUE y FALSE — de modo que un pulsador simple se convierte en un
interruptor "on/off" **sin** que el programa de aplicación tenga que
cablear a mano la lógica DEBOUNCE + R_TRIG + toggle.

### Distribución de pines

| Pin | Dirección | Tipo | Significado |
|---|---|---|---|
| `xButton`    | INPUT  | `BOOL` | Contacto crudo del pulsador (con rebote) |
| `tDebounce`  | INPUT  | `TIME` | Tiempo de antirrebote (típicamente `T#20ms`) |
| `J`          | INPUT  | `BOOL` | "Set" (fuerza `Q` a TRUE mientras esté activo) |
| `K`          | INPUT  | `BOOL` | "Reset" (fuerza `Q` a FALSE mientras esté activo) |
| `Q`          | OUTPUT | `BOOL` | Estado actual |
| `Q_N`        | OUTPUT | `BOOL` | Estado negado (`NOT Q`) |
| `xStable`    | OUTPUT | `BOOL` | TRUE mientras `xButton` haya estado estable durante `tDebounce` |

### Ejemplo de código

Un control de lámpara con tres pulsadores: `T1` conmuta la lámpara,
`T_Mains` la fuerza encendida (p. ej. "luz principal en todas partes"),
`T_Off` apaga todo:

```text
PROGRAM PLC_PRG
VAR
    bButtons     AT %IX0.0 : ARRAY [0..3] OF BOOL;
    relay_lamp   AT %QX0.0 : BOOL;
    fbToggle     : JK_FF;
END_VAR

fbToggle(
    xButton    := bButtons[0],   (* toggle button T1 *)
    tDebounce  := T#20ms,
    J          := bButtons[1],   (* main light ON while held *)
    K          := bButtons[2]    (* main light OFF while held *)
);

relay_lamp := fbToggle.Q;
END_PROGRAM
```

Tabla de verdad de las entradas `J`/`K`:

| `J` | `K` | Comportamiento |
|---|---|---|
| FALSE | FALSE | Conmuta en cada pulsación con antirrebote |
| TRUE  | FALSE | Q := TRUE (set, anula la conmutación) |
| FALSE | TRUE  | Q := FALSE (reset, anula la conmutación) |
| TRUE  | TRUE  | indefinido — evítelo |

`xStable` permite implementar la lógica de "el pulsador está pulsado
ahora" (p. ej. un LED que visualice la pulsación sin tener que esperar
al efecto de conmutación).

## Sincronización de la biblioteca entre editor y PLC

La biblioteca estándar reside en dos lugares:

  - **Lado del editor:** `editor/resources/library/standard_library.json`
    (compilado en el `.exe` mediante el sistema de recursos de Qt).
  - **Lado del PLC:** submódulo de anvild, mismo archivo JSON, incluido
    por el paso `make` sobre las fuentes C cargadas.

La **sincronización de la biblioteca** compara SHA-256 de ambas
versiones al conectarse. En caso de divergencia aparece una nota en el
panel de salida; la reacción es configurable:

  - `Preferences > Library > Auto-Push` desactivado (predeterminado):
    push manual mediante `Tools > Sync Library`. Protege un runtime de
    producción contra una sobrescritura accidental por parte de un
    editor más antiguo.
  - `Preferences > Library > Auto-Push` activado: la divergencia
    desencadena un push automático. Útil en configuraciones de
    desarrollo con un único programador.

## Extensiones de ForgeIEC

Los siguientes bloques no están estandarizados en IEC 61131-3 pero se
incluyen como parte de la biblioteca estándar porque su uso ha
demostrado ser universalmente útil en la práctica:

| Bloque | Propósito |
|---|---|
| `JK_FF` | Flipflop de conmutación con antirrebote de pulsador integrado (véase Ejemplo 2). |
| `DEBOUNCE` | Antirrebote de pulsador simétrico (véase Ejemplo 1). |

Estos bloques se ubican en *Standard Function Blocks / Application* y
están marcados como `isStandard: true` en el JSON fuente,
identificándolos como "no eliminables" (es decir, no pueden eliminarse
accidentalmente desde el panel Biblioteca).

## Añadir sus propios bloques a la biblioteca de usuario

Toda declaración `FUNCTION_BLOCK` y `FUNCTION` en el proyecto actual
aterriza automáticamente en **User Library**. Tiempos de visibilidad:

  1. **En el panel Biblioteca:** inmediatamente tras declarar y guardar la POU.
  2. **En el autocompletado de código (Ctrl-Espacio):** inmediatamente.
  3. **En el editor FBD/LD como bloque:** inmediatamente.
  4. **En el PLC** tras `Compile + Upload`.

Para reutilizar un bloque entre proyectos, exporte la POU mediante
`File > Export POU...` como archivo `.forge-pou` e impórtelo en el
proyecto de destino — una "biblioteca de espacio de trabajo"
multiproyecto está en el backlog.

## Temas relacionados

- [Sintaxis de Structured Text](../st/) — cómo se ve la llamada a un bloque en ST.
- [Editor de Function Block Diagram](../fbd/) — cómo se cablea un
  bloque gráficamente.
- [Panel de variables](../variables/) — cómo el pool de direcciones ve
  la instancia.
