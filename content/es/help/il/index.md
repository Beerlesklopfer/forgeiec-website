---
title: "Editor de Instruction List"
summary: "Editor IL: lenguaje IEC 61131-3 basado en acumulador con registro CR"
---

## Visión general

**Instruction List (IL)** es el lenguaje de texto similar a ensamblador
de IEC 61131-3 e históricamente el primero de los cinco lenguajes IEC.
Los programas son secuencias de instrucciones que manipulan un único
**registro acumulador** interno — el *Current Result* (`CR`). Cada
línea es una sentencia con la forma

```
[Label:] Operator [Modifier] [Operand] (* Comment *)
```

y o bien lee del acumulador o escribe en él, o accede a una variable
externa.

En ForgeIEC IL se edita mediante el `FIlEditor` — la disposición y el
herramental son análogos al [editor ST](../st/).

## Disposición del editor

```
+----------------------------------------+
| Variable table                         |  <- FVariablesPanel
| (VAR/VAR_INPUT/VAR_OUTPUT)             |
+========================================+  <- QSplitter (vertical)
| Code area                              |  <- FStCodeEdit
| (tree-sitter-instruction-list grammar) |
+----------------------------------------+
```

| Área | Contenido |
|---|---|
| **Tabla de variables** (arriba) | Declaraciones con Nombre, Tipo, Valor inicial, Dirección, Comentario — sincronizadas con el bloque `VAR ... END_VAR`. |
| **Área de código** (abajo) | Fuente IL con resaltado tree-sitter (gramática `tree-sitter-instruction-list`). |
| **Barra de búsqueda** (Ctrl-F / Ctrl-H) | Barra de buscar y reemplazar. |

El modo online y la superposición de valores en línea funcionan de
forma idéntica al editor ST.

## Modelo de acumulador

El acumulador (`CR`) contiene el resultado intermedio de la evaluación
en curso. Una secuencia típica:

  1. `LD x` — carga `x` en el acumulador (`CR := x`)
  2. `AND y` — combina el acumulador con `y` (`CR := CR AND y`)
  3. `ST z` — almacena el acumulador en `z` (`z := CR`)

Esto convierte a IL en una **máquina de un único registro y sin pila**
— muy próxima a las plataformas de microcontrolador que dominaban
cuando el lenguaje se estandarizó en 1993.

## Operadores clave

| Grupo | Operadores | Efecto |
|---|---|---|
| **Carga / Almacenamiento** | `LD`, `LDN`, `ST`, `STN` | Establecer acumulador / almacenar acumulador (`N` = negado) |
| **Set / Reset** | `S`, `R` | Set / reset de bit (variable BOOL, cuando `CR` = TRUE) |
| **Lógica de bits** | `AND`, `OR`, `XOR`, `NOT` | Combinar acumulador con operando |
| **Aritmética** | `ADD`, `SUB`, `MUL`, `DIV`, `MOD` | Acumulador + operando → acumulador |
| **Comparación** | `GT`, `GE`, `EQ`, `NE`, `LE`, `LT` | Resultado de comparación en `CR` |
| **Salto** | `JMP`, `JMPC`, `JMPCN` | Saltar a etiqueta (`C` = cuando `CR` = TRUE) |
| **Llamada** | `CAL`, `CALC`, `CALCN` | Llamar a instancia de bloque de función |
| **Retorno** | `RET`, `RETC`, `RETCN` | Salir de la POU |

## Modificadores

Un operador puede refinarse mediante modificadores de sufijo:

| Modificador | Significado |
|---|---|
| `N` | **Negación** del operando (`LDN x` carga `NOT x`) |
| `C` | **Condicional** — ejecutar solo cuando `CR` = TRUE (`JMPC label`) |
| `(`...`)` | **Modificador de paréntesis** — diferir la evaluación hasta que se cierre `)` |

La forma con paréntesis permite expresiones compuestas sin variables
intermedias:

```
LD   a
AND( b
OR   c
)
ST   result            (* result := a AND (b OR c) *)
```

## Cuándo usar IL en lugar de ST

Hoy, ST es la opción predeterminada. IL sigue teniendo sentido cuando:

  - **El rendimiento del microcontrolador** es decisivo — IL se
    corresponde 1:1 con las instrucciones máquina en la mayoría de los
    back-ends matiec, sin optimización intermedia.
  - **Sistemas heredados** deben mantenerse compatibles (lógica derivada
    de S5/S7 AWL, base instalada antigua de ABB / Beckhoff).
  - **Bloques de lógica muy compactos** — interbloqueos, autorretenciones,
    condiciones de flanco a menudo son dos líneas más cortos en IL que
    en ST.

Para todo lo demás, ST es más legible y más fácil de mantener.

## Ejemplo de código — contactor con autorretención y contactos NA/NC

**Autorretención de contactor** clásica en IL: pulsar `start` energiza
el contactor `K1`, el pulsador `stop` (NC, activo bajo) lo desenergiza.
Lógica:

```
K1 := (start OR K1) AND NOT stop
```

En IL:

```
PROGRAM Selbsthaltung
VAR
    start  AT %IX0.0 : BOOL;       (* NO push-button *)
    stop   AT %IX0.1 : BOOL;       (* NC push-button, low-active *)
    K1     AT %QX0.0 : BOOL;       (* contactor *)
END_VAR

    LD    start
    OR    K1                    (* CR := start OR K1 *)
    ANDN  stop                  (* CR := CR AND NOT stop *)
    ST    K1                    (* K1 := CR *)
END_PROGRAM
```

Cuatro instrucciones, un registro, sin almacenamiento temporal.
Exactamente el tipo de construcción para el que IL fue diseñado
originalmente.

## Temas relacionados

- [Structured Text](../st/) — el lenguaje hermano similar a Pascal
- [Biblioteca](../library/) — bloques de función invocables mediante `CAL`
- [Formato de archivo de proyecto](../file-format/) — cuerpo IL dentro de `<body><IL>...`
