---
title: "Ledger"
description: "Gestion de ordenes de fabricacion e integracion MES"
weight: 7
---

## Ledger -- Gestion de ordenes de fabricacion

**En desarrollo**

Ledger es el modulo de gestion de ordenes de fabricacion de la plataforma
ForgeIEC. El libro de registro del forjador documenta cada pieza producida --
Ledger documenta cada orden de fabricacion, cada paso de produccion y cada
resultado.

---

## Integracion MES

Los sistemas MES (Manufacturing Execution Systems) son el enlace entre la
planificacion de produccion (ERP) y la ejecucion en planta (PLCs). Ledger
proporcionara esta capa de integracion para la plataforma ForgeIEC.

### Funcionalidades planificadas

- **Gestion de ordenes** -- Recepcion, lanzamiento y seguimiento de ordenes de fabricacion
- **Seguimiento de produccion** -- Conteo de piezas, tiempos de ciclo, tasa de rendimiento
- **Trazabilidad** -- Asociacion de parametros de proceso a cada lote producido
- **Informes de produccion** -- Generacion automatica de informes por turno, equipo o periodo
- **Interfaz ERP** -- Intercambio de datos con los sistemas de planificacion existentes

---

## Arquitectura prevista

Ledger funcionara como un servicio independiente, conectado al runtime
mediante Anvil (Zero-Copy IPC) para los datos de proceso en tiempo real,
y mediante una API REST para la integracion con los sistemas IT.

### Integracion en la plataforma

- **Anvil** -- Datos de proceso en tiempo real (contadores, estados de maquina)
- **Hearth** -- Visualizacion de ordenes de fabricacion en el HMI
- **Bellows** -- Intercambio de datos OPC UA con sistemas MES de terceros
- **Forge Studio** -- Configuracion de variables de produccion desde el IDE

---

## Casos de uso

### Fabricacion discreta

Seguimiento de ordenes de fabricacion pieza a pieza, con conteo automatico
y deteccion de rechazos basada en las senales del PLC.

### Industria de proceso

Seguimiento de lotes de produccion, registro de parametros de proceso
(temperatura, presion, caudal) y generacion de informes de lote.

### Mantenimiento

Contadores de horas de funcionamiento, ciclos de mantenimiento preventivo
y activacion automatica de ordenes de mantenimiento.

---

<div style="text-align:center; padding: 2rem;">

**Ledger esta en desarrollo. La informacion se actualizara a medida que
avance el proyecto.**

blacksmith@forgeiec.io

</div>
