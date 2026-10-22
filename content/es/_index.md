---
title: "ForgeIEC"
---

<div style="text-align:center; padding: 3rem 1rem;">

# Forjado para la industria.

**Un entorno de desarrollo IEC 61131-3 con calidad industrial. Codigo abierto.**

[Contacto](mailto:blacksmith@forgeiec.io)

</div>

---

## Lo que estamos construyendo

ForgeIEC es un entorno de desarrollo IEC 61131-3 completo para
automatizacion industrial — los cinco lenguajes IEC, sistemas de bus
industriales, depuracion en tiempo real.

Desarrollado con la ambicion de competir de igual a igual con los sistemas
comerciales establecidos. Cada funcion esta respaldada por pruebas
documentadas antes de su publicacion.

---

## Por que codigo abierto

La automatizacion industrial es una tecnologia clave. Pero el acceso a
herramientas profesionales esta restringido por costes de licencia y
sistemas propietarios. ForgeIEC hace accesible el valor de la automatizacion
para todos — sin dependencia del fabricante, sin costes de licencia.

Como proyecto de codigo abierto, ForgeIEC pertenece a la comunidad.

---

## Primeros pasos

```bash
# Instalar la clave de firma (una sola vez)
sudo install -d -m 0755 /etc/apt/keyrings
curl -fsSL https://apt.forgeiec.io/forgeiec.gpg \
  | sudo tee /etc/apt/keyrings/forgeiec.gpg >/dev/null

# Añadir la fuente del repositorio
echo "deb [arch=amd64,arm64 signed-by=/etc/apt/keyrings/forgeiec.gpg] \
https://apt.forgeiec.io/trixie trixie main" \
  | sudo tee /etc/apt/sources.list.d/forgeiec.list

# Instalar editor + runtime
sudo apt update
sudo apt install forgeiec-studio forgeiec-anvil-server
```

Ejemplo para Debian 13 (trixie). Para Debian 12 (bookworm) o Ubuntu 24.04 (noble), sustituya las dos apariciones de `trixie`. Todas las distribuciones, RPM y los demás paquetes: [Descargas](/download/).

---

<div style="text-align:center; padding: 2rem;">

**Publicaremos informacion detallada cuando haya una version
de calidad industrial disponible.**

blacksmith@forgeiec.io

</div>
