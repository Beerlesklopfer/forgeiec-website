---
title: "Editor de Structured Text"
summary: "Editor ST + fundamentos del lenguaje: instrucciones IEC 61131-3, acceso a bits, referencias cualificadas al pool"
---

## Visión general

**Structured Text (ST)** es el lenguaje de alto nivel similar a Pascal
de IEC 61131-3 y el editor predeterminado para POUs PROGRAM,
FUNCTION_BLOCK y FUNCTION en ForgeIEC. El editor es una composición
basada en `QWidget` formada por una tabla de variables y un área de
código, acopladas mediante un splitter vertical.

```
+----------------------------------------+
| Variable table                         |  <- FVariablesPanel
| (VAR/VAR_INPUT/VAR_OUTPUT/VAR_INST)    |
+========================================+  <- QSplitter (vertical)
| Code area                              |  <- FStCodeEdit
| (Tree-sitter highlighting + folding +  |
|  Ctrl-Space completion)                |
+----------------------------------------+
```

## Disposición del editor

| Área | Contenido |
|---|---|
| **Tabla de variables** (arriba) | Declaraciones con columnas Nombre, Tipo, Valor inicial, Dirección, Comentario. Las ediciones se sincronizan en vivo en el bloque `VAR ... END_VAR` del código. |
| **Área de código** (abajo) | Fuente ST entre las secciones de variables. Plegado de líneas controlado por el AST de tree-sitter, números de línea, resaltado de la línea del cursor. |
| **Barra de búsqueda** (Ctrl-F / Ctrl-H) | Mostrada sobre el área de código, con modo de reemplazo para buscar y reemplazar. |

El splitter recuerda su posición por POU en el estado de la
disposición.

## Resaltado de sintaxis con Tree-sitter

En lugar de un `QSyntaxHighlighter` basado en regex, ForgeIEC analiza
la fuente ST con **Tree-sitter** en un AST y colorea mediante consultas
de captura:

  - **Palabras clave** (`IF`, `THEN`, `FOR`, `FUNCTION_BLOCK`, ...): magenta
  - **Tipos de datos** (`BOOL`, `INT`, `REAL`, `TIME`, ...): cian
  - **Cadenas + literales de tiempo** (`'abc'`, `T#20ms`): verde
  - **Comentarios** (`(* ... *)`, `// ...`): gris, cursiva
  - **PUBLISH / SUBSCRIBE**: palabras clave de la extensión Anvil, estilo dedicado

Beneficio: el resaltado se mantiene correcto en construcciones complejas
(comentarios anidados, literales de tiempo, referencias cualificadas), y
el mismo AST gobierna los rangos plegables para el plegado de código.

## Autocompletado de código (Ctrl-Espacio)

Pulsar **Ctrl-Espacio** o teclear dos caracteres coincidentes abre el
popup de autocompletado. El completador conoce:

  - **Palabras clave IEC** (`IF`, `CASE`, `FOR`, `WHILE`, `RETURN`, ...)
  - **Tipos de datos** (`BOOL`, `INT`, `DINT`, `REAL`, `STRING`, `TIME`, ...)
  - **Variables locales** de la POU actual
  - **Nombres de POU** del proyecto (PROGRAM, FUNCTION_BLOCK, FUNCTION)
  - **Bloques de biblioteca** (`TON`, `R_TRIG`, `JK_FF`, `DEBOUNCE`, ...)
  - **Funciones estándar** (`ABS`, `SQRT`, `LIMIT`, `LEN`, ...)

Los cambios en el pool de variables (señal `poolChanged`) se propagan
al modelo de autocompletado con un debounce de 100 ms — las nuevas
entradas del pool quedan disponibles casi al instante, sin que cada
pulsación de tecla desencadene un reescaneo completo.

## Fundamentos del lenguaje (IEC 61131-3)

### Instrucciones

| Instrucción | Forma |
|---|---|
| **Asignación** | `var := expression;` |
| **IF / ELSIF / ELSE** | `IF cond THEN ... ELSIF cond THEN ... ELSE ... END_IF;` |
| **CASE** | `CASE x OF 1: ... ; 2,3: ... ; ELSE ... END_CASE;` |
| **FOR** | `FOR i := 1 TO 10 BY 1 DO ... END_FOR;` |
| **WHILE** | `WHILE cond DO ... END_WHILE;` |
| **REPEAT** | `REPEAT ... UNTIL cond END_REPEAT;` |
| **EXIT / RETURN** | Salir del bucle / salir de la POU |

### Expresiones

Operadores estándar con precedencia IEC: `**`, unarios `+/-/NOT`,
`* / MOD`, `+ -`, comparaciones, `AND / &`, `XOR`, `OR`. Paréntesis
como en Pascal. No se permiten conversiones numéricas implícitas —
`INT_TO_DINT`, `REAL_TO_INT`, etc., deben invocarse explícitamente.

### Acceso a bits sobre tipos ANY_BIT

`var.<bit>` extrae o establece un único bit, directamente en variables
`BYTE`/`WORD`/`DWORD`/`LWORD`:

```text
status.0 := TRUE;             (* set bit 0 *)
alarm := flags.7 OR flags.3;  (* read bits *)
```

El compilador traduce esto en máscaras de bits limpias con
`AND`/`OR`/desplazamiento, sin variables auxiliares.

### Referencias cualificadas de 3 niveles

`<Categoría>.<Grupo>.<Variable>` accede directamente a entradas del
pool, sin necesidad de declarar GVLs explícitamente:

| Prefijo | Origen |
|---|---|
| `Anvil.X.Y`   | Entrada de pool con `anvilGroup="X"` |
| `Bellows.X.Y` | Entrada de pool con `hmiGroup="X"` |
| `GVL.X.Y`     | Entrada de pool con `gvlNamespace="X"` |
| `HMI.X.Y`     | Sinónimo de `Bellows.X.Y` |

`Anvil.X.Y` y `Bellows.X.Y` pueden apuntar independientemente a
diferentes entradas del pool — el compilador emite símbolos C separados
en cuanto las direcciones IEC difieran.

### Variables localizadas (`AT %...`)

Las variables localizadas vinculan una declaración a una dirección IEC:

```text
button_raw    AT %IX0.0  : BOOL;
motor_speed   AT %QW1    : INT;
flag_persist  AT %MX10.3 : BOOL;
```

La dirección es la clave primaria en el pool — véase
[Formato de archivo de proyecto](../file-format/).

## Ejemplos de código

### Ejemplo 1 — llamada a TON con bloque de biblioteca

```text
PROGRAM PLC_PRG
VAR
    start_button   AT %IX0.0  : BOOL;
    motor_run      AT %QX0.0  : BOOL;
    fbDelay        : TON;
END_VAR

fbDelay(IN := start_button, PT := T#3s);
motor_run := fbDelay.Q;
END_PROGRAM
```

`fbDelay` es una instancia del FB de biblioteca `TON`. Tras 3 segundos
de `start_button` mantenido, `motor_run` cambia a TRUE.

### Ejemplo 2 — lectura de Bellows pilotando una salida

```text
PROGRAM Lampen
VAR
    relay_lamp  AT %QX0.1 : BOOL;
END_VAR

(* HMI panel can write Bellows.Pfirsich.T_1 *)
relay_lamp := Bellows.Pfirsich.T_1 OR Anvil.Sensors.contact_door;
END_PROGRAM
```

`Bellows.Pfirsich.T_1` y `Anvil.Sensors.contact_door` son referencias
de 3 niveles que el compilador resuelve sin una declaración de GVL —
siempre que ambas etiquetas se mantengan en el pool de direcciones y la
exportación HMI para el grupo `Pfirsich` esté activa.

## Temas relacionados

- [Biblioteca](../library/) — bloques de función + funciones disponibles
- [Instruction List](../il/) — editor de texto alternativo (basado en acumulador)
- [Formato de archivo de proyecto](../file-format/) — cómo se almacena el código ST en `.forge`
