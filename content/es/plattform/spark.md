---
title: "Spark"
description: "Tunel Zenoh -- puente de red Edge-to-Cloud"
weight: 5
---

## Spark -- Tunel Zenoh

Spark es el puente de red Edge-to-Cloud de la plataforma ForgeIEC. La chispa
enciende el fuego -- Spark enciende la conexion entre los PLCs en planta y
los servicios en la nube.

---

## Edge-to-Cloud sin compromisos

Las instalaciones industriales modernas necesitan una conexion fiable entre
los equipos de campo y los servicios cloud -- para el telemantenimiento,
el analisis de datos y la supervision remota. Spark proporciona esta conexion
mediante el protocolo Zenoh.

### Por que Zenoh?

Zenoh es un protocolo de comunicacion disenado para entornos restringidos
y distribuidos. A diferencia de las VPN tradicionales o las conexiones MQTT,
Zenoh ofrece:

- **Travesia NAT nativa** -- Sin configuracion compleja de cortafuegos
- **Protocolo pub/sub eficiente** -- Bajo consumo de ancho de banda
- **Enrutamiento adaptativo** -- Seleccion automatica de la mejor ruta de red
- **Latencia minima** -- Disenado para aplicaciones en tiempo real

---

## Casos de uso

### Telemantenimiento

Conexion segura a PLCs remotos para diagnostico, actualizacion de programas
y lectura de variables -- sin desplazamiento al sitio.

### Recopilacion de datos en la nube

Transmision de datos de proceso a plataformas cloud (AWS, Azure,
infraestructura privada) para analisis, machine learning y mantenimiento
predictivo.

### Supervision multi-sitio

Supervision centralizada de varias instalaciones desde un punto unico,
con datos en tiempo real y latencia minima.

---

## Arquitectura

Spark funciona como un daemon en el PLC, conectado al runtime mediante
Anvil (Zero-Copy IPC). Los datos se transmiten de forma selectiva a los
nodos Zenoh remotos.

```
Sitio A                          Cloud / Sitio central
+------------+                   +------------------+
| anvild     |                   | Zenoh Router     |
|   |        |                   |   |              |
|   +- Spark |----- Zenoh ---------|  +- Servicios  |
|   |  Anvil |   (cifrado)       |     Analitica    |
+------------+                   +------------------+
```

### Caracteristicas

- Cifrado de extremo a extremo (TLS 1.3)
- Filtrado configurable de las variables transmitidas
- Reconexion automatica en caso de corte de red
- Compresion de datos para enlaces de bajo ancho de banda
- Compatible con redes moviles (4G/5G)

---

## Detalles tecnicos

- **Protocolo**: Zenoh (zero overhead network protocol)
- **Transporte**: TCP, UDP, WebSocket
- **Cifrado**: TLS 1.3
- **Plataformas**: x86_64, ARM64, ARMv7 (Linux)
- **Integracion**: Anvil IPC hacia el runtime, Zenoh hacia la nube

---

<div style="text-align:center; padding: 2rem;">

**Spark -- La chispa que conecta la planta con la nube.**

blacksmith@forgeiec.io

</div>
