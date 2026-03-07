---
title: "Plataforma"
description: "La plataforma ForgeIEC -- todos los componentes para la automatizacion industrial"
weight: 10
---

## La plataforma ForgeIEC

ForgeIEC es una plataforma de automatizacion industrial completa -- desde el
entorno de desarrollo hasta el sistema de supervision. Cada componente lleva
el nombre de una herramienta de forja, porque ForgeIEC esta forjado para
la industria.

---

### Forge Studio

**Entorno de desarrollo IEC 61131-3**

El IDE profesional para la programacion de PLCs. Los cinco lenguajes IEC,
edicion grafica y textual, compilacion local, despliegue remoto. Construido
con C++17 y Qt6.

[Mas informacion](forge-studio/)

---

### Anvil

**Runtime PLC en tiempo real**

El daemon de runtime que ejecuta los programas IEC en el sistema objetivo.
Comunicacion Zero-Copy entre el runtime y los bridges de protocolo mediante
la tecnologia Anvil de memoria compartida.

[Mas informacion](anvil/)

---

### Bellows

**Pasarela OPC UA** -- En desarrollo

Comunicacion maquina-a-maquina conforme al estandar OPC UA. Integracion
transparente de los sistemas de automatizacion en la infraestructura IT
existente.

[Mas informacion](bellows/)

---

### Hearth

**SCADA/HMI** -- En desarrollo

Visualizacion de procesos e interfaz hombre-maquina para la supervision
industrial. Paneles en tiempo real, historico de datos, gestion de alarmas.

[Mas informacion](hearth/)

---

### Spark

**Tunel Zenoh**

Puente de red Edge-to-Cloud basado en el protocolo Zenoh. Conexion segura
entre los PLCs en planta y los servicios en la nube, sin VPN, sin
configuracion compleja.

[Mas informacion](spark/)

---

### Tongs

**Bridges Fieldbus**

Los puentes de protocolo para Modbus TCP/RTU, EtherCAT y Profibus DP. Cada
bridge funciona como un proceso independiente, supervisado y reiniciado
automaticamente por el runtime.

[Mas informacion](tongs/)

---

### Ledger

**Gestion de ordenes de fabricacion** -- En desarrollo

Integracion MES para la gestion de ordenes de fabricacion, seguimiento de
produccion y trazabilidad. Puente entre la automatizacion y la planificacion
de la produccion.

[Mas informacion](ledger/)

---

<div style="text-align:center; padding: 2rem;">

**Basado en OpenPLC** — ForgeIEC esta basado en el proyecto
[OpenPLC](https://autonomylogic.com/) y es totalmente compatible con su
arquitectura de archivos. Los proyectos OpenPLC existentes se pueden abrir
y desarrollar directamente.

**Todos los componentes son Open Source. Sin costes de licencia. Sin dependencia de proveedor.**

blacksmith@forgeiec.io

</div>
