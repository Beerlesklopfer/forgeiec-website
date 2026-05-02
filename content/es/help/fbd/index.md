---
title: "Editor de Function Block Diagram (FBD)"
summary: "Cableado gráfico de funciones, bloques de función y variables"
---

## Visión general

Function Block Diagram (FBD) es uno de los tres lenguajes gráficos
IEC 61131-3 soportados por ForgeIEC Studio. Un programa FBD consiste
en **llamadas a funciones y bloques de función** cableadas entre sí —
y a variables de entrada y salida — mediante **conexiones de hilo
explícitas**. A diferencia de Ladder Diagram, FBD **no tiene raíles
de alimentación**: cada conexión es un único hilo que lleva un pin de
salida a uno o varios pines de entrada.

## Disposición del editor

El editor FBD es un widget de tres partes:

```
+---------------------------------------------+
| Toolbar (Select | Wire | Block | Var | ...) |
+--------------------------------+------------+
|                                |            |
|       QGraphicsView            |  Variable  |
|       Grid + Zoom + Pan        |  table     |
|                                |  (right)   |
|                                |            |
+--------------------------------+------------+
```

* **Barra de herramientas en la parte superior:** Cambio de
  herramientas (Select, Wire, Place Block, Place In-/Out-Variable,
  Comment, Zoom).
* **QGraphicsView:** La superficie de dibujo con una rejilla de fondo
  (10 px menor, 50 px mayor) y desplazamiento con el botón central del
  ratón. La rueda del ratón hace zoom alrededor del cursor.
* **Tabla de variables a la derecha:** Acoplable, muestra las variables
  locales de la POU. Arrastrar y soltar desde la tabla crea un elemento
  in-/out-variable en el editor.

## Herramientas

| Herramienta | Efecto |
|---|---|
| **Select** | Seleccionar, mover, eliminar elementos. |
| **Wire** | Hacer clic en un puerto de salida, luego en un puerto de entrada — la conexión se crea. |
| **Place Block** | Soltar una función o un bloque de función desde la biblioteca. La lista de pines (entradas a la izquierda, salidas a la derecha) se toma de la definición de la biblioteca. |
| **InVar / OutVar** | Colocar un elemento de variable de entrada o salida. El nombre se introduce mediante un diálogo y puede ser una variable cualificada GVL, Anvil o Bellows. |
| **Comment** | Nota de texto libre sin efecto semántico. |

## Bloques y pines

Un **elemento de bloque** representa una llamada a una función (`ADD`,
`SEL`, ...) o a un bloque de función (`TON`, `CTU`, ...). El elemento
muestra el nombre del tipo en el encabezado, debajo el nombre de la
instancia (solo FB), y a los lados los puertos:

```
        +---- TON -----+
        | tonA         |
   IN --| IN          Q|-- timeUp
   PT --| PT         ET|-- elapsed
        +--------------+
```

Las entradas están **siempre a la izquierda**, las salidas **siempre a
la derecha**. Los pines negados se marcan con un pequeño círculo en el
puerto.

## Arrastre desde la biblioteca

Desde el panel de biblioteca, cualquier bloque estándar o de usuario
puede ser **arrastrado y soltado directamente en el editor**. Al
soltarlo, la lista de pines se toma de la definición de la biblioteca;
para los bloques de función el editor crea automáticamente una entrada
de instancia `VAR` en la sección de variables locales.

## Conversión de ida y vuelta a ST

En tiempo de compilación, el compilador de ForgeIEC traduce el cuerpo
FBD a Structured Text. Una ordenación topológica de los bloques por
flujo de datos determina el orden de ejecución. Por lo tanto: **todo
cuerpo FBD es semánticamente equivalente a un cuerpo ST**, y la
elección del lenguaje es puramente una cuestión de legibilidad.

## Ejemplo — temporizador a la conexión con `TON`

Un `TON` (temporizador a la conexión) retarda una señal de entrada en
un tiempo configurable. En FBD usted

  * cablea una **variable de entrada** `start` al pin `IN` de la instancia `TON`,
  * cablea una **variable de entrada** con valor `T#5s` al pin `PT`,
  * conecta la salida `Q` a una **variable de salida** `lampe`.

En ST eso queda como sigue:

```text
PROGRAM PLC_PRG
VAR
    start  AT %IX0.0 : BOOL;
    lampe  AT %QX0.0 : BOOL;
    tmr    : TON;
END_VAR

tmr(IN := start, PT := T#5s);
lampe := tmr.Q;
END_PROGRAM
```

Esta es exactamente la forma que el compilador genera a partir del
diagrama FBD — la instancia de variable `tmr` es la caja `Block`, y
los dos hilos son las dos asignaciones `:=`.

## Temas relacionados

* [Biblioteca](../library/) — qué bloques ofrece el selector de bloques.
* [Panel de variables](../variables/) — declaración de variables y pool de direcciones.
* [Ladder Diagram](../ld/) — lenguaje hermano orientado a la ruta de corriente.
