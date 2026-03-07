---
title: "Bellows"
description: "Pasarela OPC UA para comunicacion maquina-a-maquina"
weight: 3
---

## Bellows -- Pasarela OPC UA

**En desarrollo**

Bellows es la pasarela OPC UA de la plataforma ForgeIEC. El fuelle de la forja
alimenta el fuego -- Bellows alimenta la comunicacion entre los sistemas de
automatizacion y la infraestructura IT.

---

## Comunicacion maquina-a-maquina

OPC UA (Open Platform Communications Unified Architecture) es el estandar
de comunicacion para la Industria 4.0. Bellows proporcionara un servidor
OPC UA completo que expone las variables del PLC a los sistemas de nivel
superior.

### Casos de uso previstos

- **Integracion SCADA** -- Conexion de PLCs a sistemas de supervision existentes
- **Intercambio de datos M2M** -- Comunicacion directa entre PLCs y sistemas de terceros
- **Pasarela IT/OT** -- Puente entre las redes de automatizacion y la infraestructura informatica
- **Historizacion** -- Disponibilidad de datos de proceso para archivo

---

## Arquitectura prevista

Bellows funcionara como un proceso independiente, gestionado por el daemon
`anvild`. Los datos de proceso se reciben a traves de Anvil (Zero-Copy IPC)
y se exponen mediante el protocolo OPC UA.

```
PLC  --->  anvild  --->  Bellows (Servidor OPC UA)  --->  Clientes OPC UA
            Anvil IPC                                      SCADA, MES, Cloud
```

### Funcionalidades planificadas

- Servidor OPC UA conforme a la especificacion
- Exposicion automatica de variables IEC
- Modelo de informacion configurable
- Cifrado y autenticacion
- Descubrimiento automatico de servicios
- Historico de datos integrado

---

## Seguridad

- Cifrado TLS para todas las conexiones
- Autenticacion por certificado o contrasena
- Control de acceso granular por variable
- Conformidad con los perfiles de seguridad OPC UA

---

<div style="text-align:center; padding: 2rem;">

**Bellows esta en desarrollo. La informacion se actualizara a medida que
avance el proyecto.**

blacksmith@forgeiec.io

</div>
