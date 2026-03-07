---
title: "Forge Studio"
description: "Entorno de desarrollo IEC 61131-3 -- IDE profesional para la programacion de PLCs"
weight: 1
---

## Forge Studio -- El IDE para la automatizacion industrial

Forge Studio es el entorno de desarrollo integrado de ForgeIEC para la
programacion de PLCs conforme a la norma IEC 61131-3. Desarrollado en C++17
con Qt6, ofrece una herramienta de calidad industrial para todas las tareas
de programacion de automatismos.

---

## Los cinco lenguajes IEC 61131-3

Un solo editor para todos los lenguajes -- conmutacion transparente, variables
compartidas, estructura de proyecto unificada.

- **Texto estructurado (ST)** -- Resaltado de sintaxis, autocompletado, buscar y reemplazar
- **Lista de instrucciones (IL)** -- Soporte completo del lenguaje con edicion inteligente
- **Diagrama de bloques funcionales (FBD)** -- Editor grafico con biblioteca de bloques
- **Diagrama de contactos (LD)** -- Representacion familiar para logica de conmutacion
- **Grafcet (SFC)** -- Diagramas de secuencia para control de procesos

---

## Compilacion y despliegue

Forge Studio compila los programas IEC localmente en la estacion de trabajo.
Los archivos C generados se transfieren al PLC objetivo mediante gRPC cifrado.
El PLC solo necesita un compilador C -- no se requiere ningun compilador IEC
en el sistema objetivo.

- Compilacion local con `iec2c` (IEC 61131-3 a C)
- Transferencia cifrada al sistema objetivo
- Generacion automatica del Makefile adaptado a la plataforma
- Soporte para arquitecturas x86_64, ARM64 y ARMv7

---

## Sistemas de bus industriales

Configuracion de buses de campo al estilo CoDeSys con jerarquia de segmentos
y deteccion automatica de dispositivos.

- **Modbus TCP** -- Comunicacion Ethernet
- **Modbus RTU** -- Conexion serie RS-485
- **EtherCAT** -- Bus de campo Ethernet en tiempo real
- **Profibus DP** -- Estandar industrial probado
- Asignacion automatica de direcciones IEC sin conflictos
- Escaner de red para descubrimiento de dispositivos

---

## Depuracion en directo

- Observacion de variables en tiempo real durante la ejecucion del PLC
- Forzado de valores sin parada de produccion
- Panel de monitorizacion con funcion de filtro

---

## Biblioteca estandar

Biblioteca estandar IEC completa: contadores, temporizadores, deteccion de
flancos, conversiones de tipo y funciones matematicas. Ampliable con bloques
definidos por el usuario. Almacenada en una base de datos SQLite para acceso
rapido y busqueda eficiente.

---

## Gestion de usuarios

- Autenticacion por contrasena con cifrado bcrypt
- Tokens JWT para sesiones
- Primer inicio de sesion al estilo CoDeSys
- Control de acceso basado en roles

---

<div style="text-align:center; padding: 2rem;">

**Forge Studio -- Programar para la industria. Open Source.**

blacksmith@forgeiec.io

</div>
