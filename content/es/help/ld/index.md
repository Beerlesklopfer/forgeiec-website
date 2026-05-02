---
title: "Editor de Ladder Diagram (LD)"
summary: "Metáfora del esquema eléctrico: raíles de alimentación, contactos, bobinas"
---

## Visión general

Ladder Diagram (LD) es el más antiguo de los tres lenguajes gráficos
IEC 61131-3 y sigue la **metáfora del esquema eléctrico**: entre un
**raíl de alimentación** izquierdo y otro derecho, **rutas de corriente**
horizontales (escalones) llevan la señal. En cada escalón los contactos
se sitúan a la izquierda (en serie) y las bobinas a la derecha;
dependiendo del estado de la variable o bien "dejan pasar" o "bloquean"
la corriente. LD es muy adecuado para lógica de control simple —
finales de carrera, circuitos de autorretención, interbloqueos — y es
muy legible para los planificadores eléctricos.

## Disposición del editor

El editor LD tiene la misma estructura que el editor FBD (barra de
herramientas en la parte superior, QGraphicsView con rejilla + zoom +
panorámica, tabla de variables a la derecha), con dos particularidades:

* El **raíl de alimentación izquierdo** y el **raíl de alimentación
  derecho** son elementos permanentes del diagrama. No pueden moverse y
  crecen verticalmente con el número de escalones.
* La barra de herramientas añade botones para los símbolos LD
  (contactos, bobinas, disparadores de flanco) y un botón `Add Rung`
  que inserta una nueva conexión de escalón entre los raíles de
  alimentación.

## Símbolos

### Contactos (lado izquierdo del escalón)

| Símbolo | Significado |
|---|---|
| `--\| \|--` | **Contacto NA** — pasa cuando la variable es TRUE |
| `--\|/\|--` | **Contacto NC** — pasa cuando la variable es FALSE |
| `--\|P\|--` | **Contacto de flanco ascendente** — pasa durante un ciclo en flanco ascendente |
| `--\|N\|--` | **Contacto de flanco descendente** — pasa durante un ciclo en flanco descendente |

Los contactos en serie actúan como **AND** lógico, las rutas en
paralelo como **OR** lógico.

### Bobinas (lado derecho del escalón)

| Símbolo | Significado |
|---|---|
| `--( )` | **Bobina estándar** — escribe el estado de la ruta de corriente en la variable |
| `--(/)` | **Bobina negada** — escribe el estado invertido |
| `--(S)` | **Bobina Set** — pone la variable a TRUE y la enclava (incluso si la ruta se abre después) |
| `--(R)` | **Bobina Reset** — pone la variable a FALSE y la enclava |

Los pares Set/Reset implementan un circuito de autorretención sin
lógica IF-THEN explícita.

### Bloques de función en el escalón

Las funciones y los bloques de función de la biblioteca pueden
insertarse **en línea entre contactos y bobinas**. El editor LD los
dibuja como una caja horizontal con listas de pines a la derecha y a
la izquierda — semánticamente idéntico al bloque FBD. Usos típicos:
temporizadores (`TON`), contadores (`CTU`), comparadores (`GT`, `EQ`).

## Ejemplo — circuito de autorretención con prioridad de paro

Un circuito de relé clásico: un pulsador de marcha `xStart` enciende un
motor `qMotor`, un pulsador de paro `xStop` lo apaga. Mientras se haya
pulsado `xStart` al menos una vez y `xStop` no esté pulsado, el motor
permanece encendido (autorretención).

```text
        |                                              |
        |   xStart      xStop                          |
   +----| |---+--|/|---+-----------------------( )----+
        |    |         |                       qMotor  |
        |    |         |                                |
        |   qMotor     |                                |
        +----| |-------+                                |
        |                                              |
```

Léase como una frase:

  * `xStart` (NA) **o** `qMotor` (contacto de autorretención, NA) — en paralelo,
  * **y** `xStop` (NC) — en serie,
  * pilotan la bobina `qMotor`.

En tiempo de compilación, el compilador LD traduce este escalón a:

```text
qMotor := (xStart OR qMotor) AND NOT xStop;
```

Esta es la forma más simple de un enclavamiento con prioridad de paro.
Si ambos pulsadores se presionan al mismo tiempo, gana `xStop` porque
el contacto NC abre la ruta.

## Temas relacionados

* [Function Block Diagram](../fbd/) — lenguaje hermano orientado al
  flujo de datos.
* [Biblioteca](../library/) — bloques de función para uso en línea en
  el escalón (`TON`, `CTU`, `JK_FF`, `DEBOUNCE`).
* [Panel de variables](../variables/) — pool de direcciones y vinculación
  de variables.
