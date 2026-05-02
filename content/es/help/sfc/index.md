---
title: "Editor de Sequential Function Chart (SFC)"
summary: "Modelo paso-transición para control secuencial y máquinas de modos"
---

## Visión general

Sequential Function Chart (SFC) es el tercer lenguaje gráfico
IEC 61131-3 y describe **secuencias orientadas a estado** mediante un
modelo de paso-transición — formalmente emparentado con las redes de
Petri. Un diagrama SFC consiste en una secuencia de **pasos**
conectados por **transiciones** con condiciones. En cualquier instante
un subconjunto de los pasos está activo; un paso se abandona cuando su
transición saliente se vuelve TRUE.

SFC es el lenguaje natural para **control secuencial, máquinas de
modos y procesos por lotes** — cualquier cosa que usted describiría
como "primero esto, luego aquello, excepto cuando ...".

## Disposición del editor

El editor SFC sigue el mismo esquema de tres partes que FBD y LD: barra
de herramientas en la parte superior, QGraphicsView con rejilla + zoom
+ panorámica, tabla de variables a la derecha. La barra de herramientas
ofrece herramientas para cada tipo de elemento SFC.

## Tipos de elemento

### Paso

Un paso es una **caja rectangular** con un nombre. Mientras está
activo, las acciones asociadas a él se ejecutan.

* **Paso inicial:** El punto de entrada de la POU. Se vuelve activo al
  arrancar el programa. Se dibuja con un **borde doble** en el editor.
* **Pasos sucesivos:** Se dibujan con un único borde. Se vuelven
  activos cuando dispara la transición precedente.

Puertos: arriba (IN, desde la transición previa), abajo (OUT, hacia la
siguiente transición), derecha (conexión a bloques de acción).

### Transición

Una transición es una **barra horizontal corta** sobre la línea de
conexión vertical entre dos pasos. A la derecha de la barra está la
**condición** — bien una expresión ST (p. ej. `tmr.Q AND xReady`) o
bien la salida de un bloque de función.

Cuando la condición se vuelve TRUE, el paso precedente se desactiva y
el siguiente paso se activa.

### Bloque de acción

Un bloque de acción describe **qué ocurre mientras un paso está
activo**. Consta de dos celdas: el **calificador** a la izquierda y el
**nombre de la acción** a la derecha (una referencia a una acción ST o
a una variable de salida).

| Calificador | Significado |
|---|---|
| `N` | No-almacenado — se ejecuta mientras el paso esté activo (predeterminado). |
| `P` | Pulso — dispara una vez durante un ciclo al activarse el paso. |
| `S` | Set — fija y permanece activo a través de las transiciones de paso. |
| `R` | Reset — borra una acción previamente fijada con `S`. |
| `L` | Limitado — se ejecuta como máximo durante el tiempo dado. |
| `D` | Retardado — se inicia solo tras el retardo dado. |

Pueden acoplarse varios bloques de acción a un mismo paso.

### Divergencia y convergencia

Una **divergencia** ramifica la secuencia en múltiples rutas, una
**convergencia** las une de nuevo. SFC tiene dos clases:

* **Selección (divergencia OR):** Se entra exactamente en **una** de
  las rutas, según qué condición de transición se vuelva TRUE primero.
  Se dibuja como una **única barra horizontal**.
* **Paralela (divergencia AND):** **Todas** las rutas se vuelven
  activas simultáneamente y se ejecutan independientemente. Solo cuando
  cada una alcanza el punto de convergencia avanza la secuencia. Se
  dibuja como una **doble barra horizontal**.

### Salto

Un elemento de salto es una **flecha hacia abajo** que lleva el nombre
del paso de destino. Transfiere el control de la ruta actual a un paso
nombrado — se usa típicamente para "volver al inicio" al final de una
secuencia, o para gestión de errores ("saltar a `Step_Error`").

## Aplicación

SFC encaja siempre que un programa tiene una **secuencia temporal**
clara:

* **Modos de máquina** — Init → Idle → Running → Cleanup → Idle.
* **Procesos por lotes** — Llenar → Calentar → Mezclar → Vaciar.
* **Secuencias de seguridad** — realizar secuencias de paro en un orden
  definido ("primero calentador apagado, luego bomba apagada, luego
  contactor principal").
* **Ingeniería de procesos** — pasos de reacción con retardos y
  condiciones.

Comparada con una implementación ST de la misma función, la versión SFC
es significativamente más legible — el orden de los pasos y las
condiciones de bifurcación son gráficamente obvios, mientras que en ST
una construcción `CASE state OF` transmite la misma información solo
indirectamente.

## Temas relacionados

* [Function Block Diagram](../fbd/) — para la lógica **dentro** de una
  acción o de una condición de transición.
* [Ladder Diagram](../ld/) — lenguaje gráfico alternativo para
  circuitos de interbloqueo más sencillos.
* [Biblioteca](../library/) — los temporizadores (`TON`, `TP`) son
  partes habituales de las condiciones de transición.
