---
title: "Cobertura de pruebas"
summary: "Aseguramiento automatizado de la calidad: 117 pruebas verifican el vocabulario completo de IEC 61131-3, todos los bloques estandar y el sistema multi-tarea"
---

ForgeIEC esta protegido por un conjunto completo de pruebas automatizadas.
Cada commit se verifica antes del merge con **117 pruebas unitarias** que
cubren el vocabulario completo de IEC 61131-3 Structured Text, todos los
bloques funcionales estandar y el sistema de multi-tarea.

## Resumen de las suites de pruebas

| Suite | Pruebas | Verifica |
|-------|--------:|----------|
| **FStCompilerTest** | 101 | Vocabulario ST completo |
| **FStLibraryTest** | 8 | Los 132 bloques estandar (FBs + FCs) |
| **FCodeGeneratorThreadingTest** | 8 | Planificacion multi-tarea + sincronizacion lock-free |
| **Total** | **117** | **0 errores** |

---

## 1. Vocabulario ST (FStCompilerTest)

101 pruebas verifican cada construccion del lenguaje IEC 61131-3 Structured Text
soportada. Cada prueba compila un fragmento ST mediante el
FStCompiler y verifica el codigo C++ generado.

### 1.1 Asignaciones

| Prueba | Codigo ST | Verifica |
|--------|-----------|----------|
| `assignSimple` | `a := 42;` | Asignacion simple |
| `assignExpression` | `a := b + 1;` | Asignacion con expresion |
| `assignExternal` | `ExtVar := 10;` | Acceso VAR_EXTERNAL |
| `assignGvlQualified` | `GVL.ExtVar := 5;` | Ruta GVL cualificada |

### 1.2 Operadores aritmeticos

| Prueba | Codigo ST | Operador C |
|--------|-----------|------------|
| `arithmeticAdd` | `a := b + 1;` | `+` |
| `arithmeticSub` | `a := b - 1;` | `-` |
| `arithmeticMul` | `a := b * 2;` | `*` |
| `arithmeticDiv` | `a := b / 2;` | `/` |
| `arithmeticMod` | `a := b MOD 3;` | `%` |
| `arithmeticPower` | `c := x ** 2.0;` | `EXPT()` |
| `arithmeticNegate` | `a := -b;` | `-(...)` |
| `arithmeticParentheses` | `a := (b + 1) * 2;` | Parentesis |

### 1.3 Operadores de comparacion

| Prueba | Codigo ST | Operador C |
|--------|-----------|------------|
| `compareEqual` | `flag := a = b;` | `==` |
| `compareNotEqual` | `flag := a <> b;` | `!=` |
| `compareLess` | `flag := a < b;` | `<` |
| `compareGreater` | `flag := a > b;` | `>` |
| `compareLessEqual` | `flag := a <= b;` | `<=` |
| `compareGreaterEqual` | `flag := a >= b;` | `>=` |

### 1.4 Operadores booleanos

| Prueba | Codigo ST | Operador C |
|--------|-----------|------------|
| `boolAnd` | `flag := flag AND flag;` | `&&` |
| `boolOr` | `flag := flag OR flag;` | `\|\|` |
| `boolXor` | `flag := flag XOR flag;` | `^` |
| `boolNot` | `flag := NOT flag;` | `!` |

### 1.5 Literales

| Prueba | Codigo ST | Verifica |
|--------|-----------|----------|
| `literalInteger` | `a := 12345;` | Entero |
| `literalReal` | `c := 3.14;` | Punto flotante |
| `literalBoolTrue` | `flag := TRUE;` | Valor booleano |
| `literalBoolFalse` | `flag := FALSE;` | Valor booleano |
| `literalString` | `text := 'hello';` | Cadena de caracteres |
| `literalTime` | `counter := T#500ms;` | Constante de tiempo |

### 1.6 Estructuras de control

**IF / ELSIF / ELSE / END_IF**

| Prueba | Verifica |
|--------|----------|
| `ifSimple` | Condicion simple |
| `ifElse` | Bifurcacion If-Else |
| `ifElsif` | Bifurcacion multiple con ELSIF |
| `ifNested` | Bloques IF anidados |

**FOR / WHILE / REPEAT**

| Prueba | Verifica |
|--------|----------|
| `forSimple` | FOR idx := 0 TO 10 DO |
| `forWithBy` | FOR con paso BY |
| `whileLoop` | Bucle WHILE |
| `repeatUntil` | Bucle REPEAT/UNTIL |

**CASE**

| Prueba | Verifica |
|--------|----------|
| `caseStatement` | CASE/OF con multiples labels + switch/case/break |

**RETURN / EXIT**

| Prueba | Verifica |
|--------|----------|
| `returnStatement` | RETURN → goto __end |
| `exitStatement` | EXIT dentro de FOR → break |

### 1.7 Bloques funcionales (llamadas FB)

| Prueba | Verifica |
|--------|----------|
| `fbCallWithInputs` | `MyTon(IN := flag, PT := T#500ms);` |
| `fbCallWithOutputAssign` | `MyTimer(IN := flag, Q => flag);` — asignacion OUT => |

### 1.8 Acceso a arrays

| Prueba | Verifica |
|--------|----------|
| `arrayReadSubscript` | `a := arr[3];` |
| `arrayWriteSubscript` | `arr[5] := 42;` |
| `arrayComputedIndex` | `a := arr[idx + 1];` |
| `arrayInForLoop` | Acceso a array en bucle FOR |

### 1.9 Conversiones de tipo

El compilador reconoce el patron `XXX_TO_YYY` y genera
casts de estilo C (`(TYPE)value`), conforme a la norma IEC.

| Prueba | Codigo ST | Genera |
|--------|-----------|--------|
| `typeConvIntToReal` | `INT_TO_REAL(a)` | `(REAL)a` |
| `convRealToInt` | `REAL_TO_INT(c)` | `(INT)c` |
| `convBoolToInt` | `BOOL_TO_INT(flag)` | `(INT)flag` |
| `convIntToBool` | `INT_TO_BOOL(a)` | `(BOOL)a` |
| `convDintToReal` | `DINT_TO_REAL(counter)` | `(REAL)counter` |
| `convIntToDint` | `INT_TO_DINT(a)` | `(DINT)a` |

### 1.10 Acceso a miembros de estructura

| Prueba | Verifica |
|--------|----------|
| `structMemberAccess` | `pos.x := 42;` → `data__->pos.value.x` |

### 1.11 Variables inter-tareas (multi-tarea)

| Prueba | Verifica |
|--------|----------|
| `crossPrimitiveGet` | `__GET_EXTERNAL_ATOMIC` para lectura lock-free |
| `crossPrimitiveSet` | `__SET_EXTERNAL_ATOMIC` para escritura lock-free |
| `crossStructuredGet` | `__snap_` acceso snapshot thread-local |
| `crossStructuredMemberAccess` | `__snap_Struct.field` acceso |

### 1.12 Bloques funcionales estandar

Cada FB estandar IEC se instancia y se invoca:

| Prueba | Tipo FB | Verifica |
|--------|---------|----------|
| `fbTon` | TON | Retardo al conectar |
| `fbTof` | TOF | Retardo al desconectar |
| `fbTp` | TP | Timer de impulso |
| `fbCtu` | CTU | Contador ascendente |
| `fbCtd` | CTD | Contador descendente |
| `fbRtrig` | R_TRIG | Flanco ascendente |
| `fbFtrig` | F_TRIG | Flanco descendente |
| `fbRs` | RS | Reset-dominante |
| `fbSr` | SR | Set-dominante |

### 1.13 Funciones estandar

| Categoria | Pruebas | Funciones |
|-----------|--------:|-----------|
| Matematicas | 12 | ABS, SQRT, SIN, COS, TAN, ASIN, ACOS, ATAN, EXP, LN, LOG, TRUNC |
| Seleccion | 4 | SEL, LIMIT, MIN, MAX |
| Cadenas | 6 | LEN, LEFT, RIGHT, MID, CONCAT, FIND |
| Desplazamiento de bits | 4 | SHL, SHR, ROL, ROR |
| Conversion de tipo | 6 | INT_TO_REAL, REAL_TO_INT, BOOL_TO_INT, ... |

### 1.14 Casos limite

| Prueba | Verifica |
|--------|----------|
| `complexNestedExpression` | Expresiones anidadas |
| `multipleStatementsOnSeparateLines` | Programas multilinea |
| `emptyBody` | Cuerpo POU vacio |
| `commentOnlyBody` | Solo comentarios |
| `caseInsensitiveKeywords` | IF/if/If |
| `caseInsensitiveVariables` | Mayusculas/minusculas |

---

## 2. Biblioteca estandar (FStLibraryTest)

8 pruebas basadas en datos verifican **los 132 bloques** de la
biblioteca estandar (`standard_library.sql`) automaticamente.

### 2.1 Bloques funcionales (13 FBs)

| Prueba | Verifica |
|--------|----------|
| `fbSingleInstance` | Cada FB instanciable e invocable individualmente |
| `fbDoubleInstance` | Dos instancias del mismo tipo FB simultaneamente |
| `fbOutputRead` | Todas las salidas legibles tras la invocacion |

**FBs cubiertos:** SR, RS, R_TRIG, F_TRIG, CTU, CTD, CTUD, TON, TOF, TP,
RTC, SEMA, RampGen

### 2.2 Funciones (119 FCs)

| Prueba | Verifica |
|--------|----------|
| `fcCall` | Cada FC invocable con los parametros correctos (104 probadas) |
| `fcInExpression` | Valor de retorno FC utilizable en expresiones |

**Categorias cubiertas:**

- **Aritmetica:** ADD, SUB, MUL, DIV, MOD, EXPT, ABS
- **Comparacion:** EQ, NE, LT, GT, LE, GE
- **Trigonometria:** SIN, COS, TAN, ASIN, ACOS, ATAN, ATAN2
- **Logaritmo:** EXP, LN, LOG, SQRT
- **Seleccion:** SEL, MUX, LIMIT, MIN, MAX, MOVE, CLAMP
- **Cadenas:** LEN, LEFT, RIGHT, MID, CONCAT, INSERT, DELETE, REPLACE, FIND
- **Desplazamiento de bits:** SHL, SHR, ROL, ROR
- **Conversion de tipo:** 60+ funciones de conversion (BOOL_TO_INT, INT_TO_REAL, ...)
- **Extensiones ForgeIEC:** LERP, MAP_RANGE, HYPOT, DEG, RAD, IK_2Link,
  CABS, CADD, CMUL, CSUB, CARG, CCONJ, CPOLAR, CRECT

---

## 3. Multi-tarea (FCodeGeneratorThreadingTest)

8 pruebas verifican el sistema completo de planificacion multi-tarea segun
la especificacion de diseno (MT-spec, docs/design/multi-task-scheduler.md).

| Prueba | Verifica |
|--------|----------|
| `singleProgramDefaultTask` | Un PROGRAM sin tarea explicita → sintesis DefaultTask, sin threading |
| `twoProgramsTwoTasks` | Dos tareas → RESOURCE0_start__, Legacy-Shim config_run__, ambos hilos de tarea |
| `crossPrimitiveAtomicEmission` | Variable INT compartida → almacenamiento Location `std::atomic<>`, `__GET_EXTERNAL_ATOMIC` en el cuerpo |
| `crossStructuredDoubleBuffer` | STRUCT compartido → `__DBUF_[2]` + `thread_local __snap_` + copia Double-Buffer entrada/salida |
| `localVarNoSync` | Variable solo en una tarea → `__SET_EXTERNAL` normal, sin Atomic |
| `conflictTwoWriters` | Dos tareas escriben la misma variable → advertencia de compilacion |
| `singleProgramDefaultTask` | Retrocompatibilidad: los proyectos existentes funcionan sin cambios |

### Arquitectura multi-tarea

```
Primary Task (Task 0)          Secondary Tasks (1..N)
    |                               |
    | config_run__()                | RESOURCE0_task_thread__()
    |   ├─ sync_in                  |   ├─ dbuf_rd (copy-in)
    |   ├─ TASK0_body__()           |   ├─ TASKn_body__()
    |   └─ sync_out                 |   └─ dbuf_wr (copy-out)
    |                               |
    | [bajo bufferLock]             | [lock-free]
```

**Mecanismos de sincronizacion:**
- **CrossPrimitive** (BOOL, INT, REAL, ...): `std::atomic<T>` en la variable Location, `__GET_EXTERNAL_ATOMIC` / `__SET_EXTERNAL_ATOMIC` en el codigo del cuerpo
- **CrossStructured** (STRUCT, ARRAY, STRING): Double-Buffer `__DBUF_[2]` con indice de escritura atomico, snapshots `thread_local` `__snap_` para consistencia del Set

---

## Aseguramiento de la calidad

### Verificacion automatizada

Las pruebas se ejecutan en cada build con `-DBUILD_TESTS=ON`.
La integracion en el pipeline CI (Forgejo Actions) esta preparada.

### Pruebas basadas en datos

Las pruebas de biblioteca (`FStLibraryTest`) leen las definiciones de bloques
directamente desde `standard_library.sql`. Cuando se agregan nuevos bloques,
se prueban automaticamente — no es necesario crear casos de prueba manualmente.

### Completitud

La suite de pruebas cubre el vocabulario completo de IEC 61131-3 Structured Text
tal como lo soporta ForgeIEC:

- Todos los operadores (aritmeticos, comparacion, booleanos, desplazamiento de bits)
- Todas las estructuras de control (IF, FOR, WHILE, REPEAT, CASE)
- Todos los tipos de literales (Integer, Real, Bool, String, Time)
- Todos los FBs y FCs estandar (132 bloques)
- Acceso a arrays y estructuras
- Variables cualificadas GVL
- Sincronizacion inter-tareas (Atomics + Double-Buffer)
- Conversiones de tipo (generacion de casts C)
