---
title: "Hearth"
description: "SCADA/HMI para la visualizacion de procesos industriales"
weight: 4
---

## Hearth -- SCADA/HMI

**En desarrollo**

Hearth es el sistema de supervision e interfaz hombre-maquina de la plataforma
ForgeIEC. El hogar es el corazon de la forja, donde arde el fuego -- Hearth es
el corazon de la supervision, donde los procesos se visualizan.

---

## Visualizacion de procesos

Los sistemas de automatizacion industrial necesitan una interfaz de supervision
para observar, controlar y diagnosticar los procesos de produccion. Hearth
proporcionara esta capa de visualizacion.

### Funcionalidades planificadas

- **Paneles en tiempo real** -- Visualizacion de variables de proceso con actualizacion en directo
- **Sinopticos** -- Representacion grafica de las instalaciones con simbolos industriales
- **Historico de datos** -- Registro y visualizacion de tendencias a largo plazo
- **Gestion de alarmas** -- Deteccion, notificacion y reconocimiento de alarmas
- **Informes** -- Generacion de informes de produccion automatizados

---

## Arquitectura prevista

Hearth funcionara como una aplicacion web, accesible desde cualquier navegador
en la red. Los datos de proceso se recibiran a traves de OPC UA (Bellows) o
directamente mediante gRPC desde el runtime.

### Componentes planificados

- Interfaz web responsive (escritorio y tablet)
- Editor de sinopticos integrado
- Motor de alarmas configurable
- Base de datos historica
- Sistema de permisos y perfiles de usuario

---

## Integracion en la plataforma

Hearth se integrara con los demas componentes de la plataforma ForgeIEC:

- **Anvil** -- Datos de proceso en tiempo real
- **Bellows** -- Comunicacion OPC UA estandar
- **Ledger** -- Datos de produccion y ordenes de fabricacion
- **Forge Studio** -- Configuracion desde el IDE

---

<div style="text-align:center; padding: 2rem;">

**Hearth esta en desarrollo. La informacion se actualizara a medida que
avance el proyecto.**

blacksmith@forgeiec.io

</div>
