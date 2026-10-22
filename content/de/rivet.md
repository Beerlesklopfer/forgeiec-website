---
title: "Rivet"
date: 2026-10-22
draft: false
description: "Rivet: Fernzugriff vom Handy auf Steuerungen im lokalen Netz, ohne Portfreigabe und ohne fremde Cloud. Status: in Entwicklung, Pilot mit solidarischen Landwirtschaften."
---

# Rivet

<style>
.rv { --rv-line: var(--text, currentColor); --rv-accent: var(--spark, #F59E0B); --rv-box: rgba(148,163,184,.12); --rv-muted: rgba(148,163,184,.9); }
.rv-lead { font-size: 1.2em; line-height: 1.5; margin: 0 0 1.2em; }
.rv-cards { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 1em; margin: 1.2em 0; }
.rv-card { border: 1px solid rgba(148,163,184,.35); border-radius: .4em; padding: .9em 1em; background: var(--rv-box); }
.rv-card h3 { margin: 0 0 .4em; font-size: 1.05em; }
.rv-card p { margin: 0; }
.rv h3 { margin-top: 1.6em; }
.rv-fig { margin: 1.4em 0; }
.rv-fig svg { width: 100%; height: auto; display: block; }
.rv-fig .rv-v { display: none; max-width: 340px; margin: 0 auto; }
.rv-fig figcaption { font-size: .9em; opacity: .85; margin-top: .4em; }
.rv-two { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 1.4em; }
.hero-body .rv table { font-size: .92em; }
.hero-body .rv th { padding: .5em .7em; text-align: left; vertical-align: bottom; }
.hero-body .rv td { padding: .6em .7em; vertical-align: top; }
.hero-body .rv table td:first-child { white-space: normal; width: auto; min-width: 7em; }
.rv td code { overflow-wrap: normal; word-break: normal; }
.rv p code, .rv li code { overflow-wrap: anywhere; }
.rv pre { overflow-x: auto; max-width: 100%; }
.rv details { border: 1px solid rgba(148,163,184,.3); border-radius: .4em; padding: .5em .9em; margin: 1em 0; }
.rv summary { cursor: pointer; font-weight: 600; }
.rv-cta a { font-weight: 700; }
@media (max-width: 760px) {
  .rv-cards, .rv-two { grid-template-columns: 1fr; }
  .rv-fig .rv-h { display: none; }
  .rv-fig .rv-v { display: block; }
  .rv { max-width: calc(100vw - 4rem); }
  .hero-body .rv table { display: block; overflow-x: auto; max-width: 100%; }
  .hero-body .rv th, .hero-body .rv td { min-width: 10em; }
}
</style>

<div class="rv">

## Ihre Anlage vom Handy aus bedienen – ohne offene Tür ins Firmennetz {#nutzen}

<p class="rv-lead">Rivet verbindet das Handy einer berechtigten Person mit einer Steuerung im lokalen Netz.
Vor Ort muss dafür keine Portfreigabe eingerichtet werden, und es ist kein fremder Cloud-Anbieter
im Spiel.</p>

{{< callout type="warning" title="Status: in Entwicklung" >}}
Rivet ist noch kein fertiges Produkt. Der Code entsteht, erprobt wird er bisher auf einem Testserver.
Der erste vorgesehene Einsatz: Solidarische Landwirtschaften (SoLaWis) wollen damit ihre
Bewässerungssteuerung vom Handy aus bedienen.
{{< /callout >}}

<div class="rv-cards">
<div class="rv-card">
<h3>Das Problem</h3>
<p>Bewässerung, Heizung, Pumpe oder SPS haben oft eine Bedienoberfläche im lokalen Netz. Wer sie von
unterwegs erreichen will, stellt sie meist direkt ins Internet oder bindet sich an eine Hersteller-Cloud.</p>
</div>
<div class="rv-card">
<h3>Die Lösung</h3>
<p>Ein kleines Gateway vor Ort baut die Verbindung <strong>von innen nach außen</strong> zu unserem Server auf.
Das Handy erreicht über diesen Weg nur die Dienste, die Sie im Portal freigegeben haben, sonst nichts.</p>
</div>
<div class="rv-card">
<h3>Was Sie in der Hand behalten</h3>
<p>Sie legen im Portal fest, welche Handys welche Anlage erreichen. Ein gesperrtes Handy ist in Sekunden
draußen. Der Schlüssel eines Handys entsteht auf dem Handy und verlässt es nicht.</p>
</div>
</div>

<figure class="rv-fig" role="img" aria-label="Handy, ForgeIEC-Server, Gateway und Steuerung: das Gateway baut die Verbindung von innen zum Server auf">
<svg class="rv-h" viewBox="0 0 800 190" xmlns="http://www.w3.org/2000/svg" font-family="Inter, system-ui, sans-serif" font-size="15" fill="currentColor">
  <defs>
    <marker id="rv-ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="currentColor"/></marker>
    <marker id="rv-ah2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="var(--rv-accent, #F59E0B)"/></marker>
  </defs>
  <rect x="462" y="18" width="328" height="160" rx="10" fill="none" stroke="currentColor" stroke-dasharray="5 5" opacity=".55"/>
  <text x="621" y="40" text-anchor="middle" font-size="13" opacity=".8">Ihr lokales Netz (kein Port offen)</text>
  <rect x="10" y="78" width="130" height="58" rx="8" fill="var(--rv-box, rgba(148,163,184,.12))" stroke="currentColor"/>
  <text x="75" y="112" text-anchor="middle" font-weight="600">Handy</text>
  <rect x="226" y="78" width="150" height="58" rx="8" fill="var(--rv-box, rgba(148,163,184,.12))" stroke="currentColor"/>
  <text x="301" y="104" text-anchor="middle" font-weight="600">ForgeIEC-</text>
  <text x="301" y="122" text-anchor="middle" font-weight="600">Server</text>
  <rect x="470" y="78" width="130" height="58" rx="8" fill="var(--rv-box, rgba(148,163,184,.12))" stroke="currentColor"/>
  <text x="535" y="112" text-anchor="middle" font-weight="600">Gateway</text>
  <rect x="650" y="78" width="126" height="58" rx="8" fill="var(--rv-box, rgba(148,163,184,.12))" stroke="currentColor"/>
  <text x="713" y="112" text-anchor="middle" font-weight="600">Steuerung</text>
  <line x1="142" y1="107" x2="222" y2="107" stroke="currentColor" stroke-width="2" marker-end="url(#rv-ah)" marker-start="url(#rv-ah)"/>
  <text x="182" y="96" text-anchor="middle" font-size="12">verschlüsselt</text>
  <line x1="466" y1="107" x2="380" y2="107" stroke="var(--rv-accent, #F59E0B)" stroke-width="3" marker-end="url(#rv-ah2)"/>
  <text x="418" y="152" text-anchor="middle" font-size="12" fill="var(--rv-accent, #F59E0B)">von innen</text>
  <text x="418" y="167" text-anchor="middle" font-size="12" fill="var(--rv-accent, #F59E0B)">aufgebaut</text>
  <line x1="602" y1="107" x2="646" y2="107" stroke="currentColor" stroke-width="2" marker-end="url(#rv-ah)"/>
</svg>
<svg class="rv-v" viewBox="0 0 320 470" xmlns="http://www.w3.org/2000/svg" font-family="Inter, system-ui, sans-serif" font-size="16" fill="currentColor">
  <defs>
    <marker id="rv-av" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="currentColor"/></marker>
    <marker id="rv-av2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="var(--rv-accent, #F59E0B)"/></marker>
  </defs>
  <rect x="85" y="10" width="150" height="54" rx="8" fill="var(--rv-box, rgba(148,163,184,.12))" stroke="currentColor"/>
  <text x="160" y="43" text-anchor="middle" font-weight="600">Handy</text>
  <line x1="160" y1="68" x2="160" y2="118" stroke="currentColor" stroke-width="2" marker-end="url(#rv-av)" marker-start="url(#rv-av)"/>
  <text x="172" y="98" font-size="13">verschlüsselt</text>
  <rect x="85" y="122" width="150" height="54" rx="8" fill="var(--rv-box, rgba(148,163,184,.12))" stroke="currentColor"/>
  <text x="160" y="155" text-anchor="middle" font-weight="600">ForgeIEC-Server</text>
  <line x1="160" y1="252" x2="160" y2="180" stroke="var(--rv-accent, #F59E0B)" stroke-width="3" marker-end="url(#rv-av2)"/>
  <text x="172" y="212" font-size="13" fill="var(--rv-accent, #F59E0B)">von innen aufgebaut</text>
  <rect x="20" y="240" width="280" height="220" rx="10" fill="none" stroke="currentColor" stroke-dasharray="5 5" opacity=".55"/>
  <text x="160" y="450" text-anchor="middle" font-size="13" opacity=".8">Ihr lokales Netz (kein Port offen)</text>
  <rect x="85" y="256" width="150" height="54" rx="8" fill="var(--rv-box, rgba(148,163,184,.12))" stroke="currentColor"/>
  <text x="160" y="289" text-anchor="middle" font-weight="600">Gateway</text>
  <line x1="160" y1="314" x2="160" y2="358" stroke="currentColor" stroke-width="2" marker-end="url(#rv-av)"/>
  <rect x="85" y="362" width="150" height="54" rx="8" fill="var(--rv-box, rgba(148,163,184,.12))" stroke="currentColor"/>
  <text x="160" y="395" text-anchor="middle" font-weight="600">Steuerung</text>
</svg>
<figcaption>Das Gateway öffnet die Verbindung von innen. Deshalb muss am Internetanschluss keine Tür
geöffnet werden; auch Mobilfunk-Anschlüsse ohne eigene öffentliche Adresse funktionieren.</figcaption>
</figure>

<div class="rv-two">
<div>

### Für wen

Für Maschinen- und Anlagenbauer, die ihre Anlagen beim Kunden aus der Ferne betreuen wollen, ohne einen
Cloud-Anbieter dazwischen. Und für Betreiber, die ihre Anlage selbst vom Handy aus bedienen wollen.
<!-- ENTWURF: Zielgruppe „Maschinen- und Anlagenbauer“ ist eine Vorgabe des Inhabers; das Repository nennt „Betreiber:innen von Anlagen“ und „nicht an eine Branche gebunden“ (README.md, CLAUDE.md 1). -->

### Was vor Ort zu tun ist

1. Gateway ins lokale Netz der Steuerung stecken (oder Rivet als Paket auf dem Gerät selbst installieren).
   <!-- ENTWURF: Welche Gateway-Hardware geliefert wird, ist offen (CLAUDE.md 11, Frage 6: „konkrete Boards?“). -->
2. Die Oberfläche des Gateways öffnen und mit dem Zugangsschlüssel anmelden.
3. Den Registrierungscode aus dem Portal eingeben. Was erreichbar ist, legen Sie im Portal fest.
4. Handys im Portal hinzufügen: QR-Code mit der WireGuard-App scannen, Tunnel einschalten.

</div>
<div>

### Was Rivet nicht ist

- **Kein Cloud-Dienst eines Dritten.** Gateway, Server und Portal betreibt ForgeIEC selbst.
- **Kein Ersatz für Sicherheitsfunktionen.** Not-Halt, Verriegelungen und alles, was eine Anlage sicher
  macht, gehören in die Anlage, nicht in einen Fernzugriff.
- **Noch kein fertiges Produkt** (siehe Status oben).

### Nächster Schritt

<p class="rv-cta">Sie möchten Rivet in einem Pilot erproben? <a href="/de/kontakt/">Pilot anfragen</a></p>
<!-- ENTWURF: Ein Pilotangebot (Umfang, Konditionen, Kosten) ist im Repository nicht beschrieben; die Kontaktseite /de/kontakt/ existiert in diesem Branch noch nicht. -->

</div>
</div>

---

## Für Fachleute: die Technik im Detail {#technik}

Alle Angaben unten sind im Repository `forgeiec-rivet` (Branch `development`, Stand Commit `5f01540`,
22.10.2026) nachprüfbar. Die Spezifikation steht dort in `CLAUDE.md`. Wir unterscheiden streng:
**umgesetzt** (Code und Tests vorhanden), **spezifiziert** (in `CLAUDE.md` beschrieben, nicht programmiert)
und **geplant/offen** (als offene Frage oder „später“ vermerkt).

### Stand der Umsetzung {#stand}

| Bereich | Umgesetzt | Spezifiziert, nicht programmiert | Geplant / offen |
|---|---|---|---|
| Gateway | Uplink im Prozess (boringtun + smoltcp), TLS-Vorbau mit Zertifikatstausch im Betrieb, Einrichtungsassistent, Registrierung, Heartbeat, Long-Poll für Handys und Weiterleitungen, Weiterleitungen (Userspace und Kernel-Weg über TUN `rivet0` + nftables), Router-Konfiguration für Router-Gateways | Theme-Abruf und -Tausch auf dem Gateway (Portal-Seite vorhanden); API-Key erneuern über die Oberfläche (`POST /api/apikey/rotate`; vorhanden ist nur das Kommando `forgeiec-rivet reset-api-key`) | eigene Rivet-App für Android/iOS (offene Frage 14) |
| Server | Portal mit drei Ebenen, API v1, `routes.sqlite` + nginx-Modul, WireGuard-Dienst `forgeiec-rivet-wg` (Interfaces `uplink` und `phones`, nftables, Mini-DNS), DNS-Abgleich mit Hetzner, Wildcard-Zertifikate per certbot (DNS-01), Notfall-Rotation, Mails (Zugang, Einrichtungslink), Aufräum-Timer, Pakete und CI | `install.sh` (Bootstrap); Alarm-Mails (Gateway offline, Zertifikat läuft ab, ungewöhnliche Abrufe); Releases mit `SHA256SUMS` und Signatur | TLS in nginx terminieren statt Wildcard auf den Gateways (offene Frage 1) |
| Betrieb | Bau für 12 Slots, Pakete `forgeiec-rivet` und `forgeiec-rivet-server` | Selbsttest bei Router-Gateways („lässt der Router mehr ins LAN?“); Interop-Test in der CI gegen Kernel-WireGuard bzw. `wireguard-go` als Gegenstelle des Gateways | Ausweichweg über TCP 443, wenn UDP gesperrt ist (offene Frage 11); Direktzugang bei Serverausfall (offene Frage 8); alten Handy-Weg über das Gateway abschalten |

### Architektur {#architektur}

| Komponente | Code | Technik (geprüft in `Cargo.toml`, `requirements.txt` bzw. Quelltext) | Aufgabe |
|---|---|---|---|
| **Gateway** `forgeiec-rivet` | `client/` | Rust (Edition 2024), tokio; `boringtun 0.7` ohne Default-Features (nur `noise::Tunn`); `smoltcp 0.14`; `rustls 0.23` mit `ring` + `tokio-rustls`; `hyper 1`; `Rocket 0.5` (`json`, `secrets`) mit `rocket_dyn_templates` (Tera); `fluent-bundle`; `ureq 2`; `rustables 0.9` und `netlink-*` für TUN/nftables; `x509-parser`, `rcgen`, `qrcode` | ausgehender Uplink zum Server, Weiterleitung freigegebener TCP-Ports ins LAN, Einrichtungsoberfläche |
| **Portal** | `server/portal/` | Django 5.2, Django REST Framework 3.18, gunicorn (`127.0.0.1:8001`), `cryptography`, `certbot` + `certbot-dns-hetzner`, `hcloud` | Ebenen und Konten, Registrierung, Heartbeat, Zertifikate, Handys, Weiterleitungen, schreibt `routes.sqlite`, steuert `forgeiec-rivet-wg` |
| **WireGuard-Dienst** `forgeiec-rivet-wg` (der privilegierte Helfer) | `server/wg-daemon/` | Rust, rust-netlink (`netlink-packet-wireguard`, `-route`, `-generic`), `rustables 0.9`; Kernel-WireGuard | hält die Kernel-Interfaces `uplink` und `phones`, setzt Peers und die nftables-Tabelle `ip rivet_server`, Mini-DNS für Handys, liefert Statistik |
| **nginx-Modul** `ngx_stream_rivet_module` | `server/nginx-module/` | C, dynamisches stream-Modul, SQLite | TLS-Passthrough: Ziel je SNI bzw. UDP-Port aus `routes.sqlite`, ohne Reload |

**Ports auf dem Server** (aus `server/contrib/nginx/rivet-stream.conf.in`, `forgeiec-rivet-wg.service.in`, `settings.py`):

| Port | Protokoll | Wofür |
|---|---|---|
| 80 | TCP | Umleitung auf HTTPS |
| 443 | TCP | nginx `stream` mit `ssl_preread`: Portale → lokal `127.0.0.1:8443`, Geräte → `10.78.x.y:443` über den Uplink, unbekannte → `127.0.0.1:8444` |
| 51900 | UDP | WireGuard `uplink` (Server `10.78.0.1/16`), ein Peer je Gateway |
| 52000 | UDP | WireGuard `phones` (Server `10.79.0.1/16`), ein Peer je Handy |
| 51000–51899, 51901–51999 | UDP | alter Handy-Weg: je Gateway ein Port, nginx reicht ihn an `10.78.x.y:51820` weiter |
| 53 auf `10.79.0.1` | UDP/TCP | Mini-DNS, nur aus dem Handy-Netz `10.79.0.0/16` |

**Datenwege**

1. **Browser → Gateway-Oberfläche** `https://<gerät>.<kunde>.<zone>.forgeiec.io`: nginx liest nur den
   Hostnamen (SNI), schlägt das Ziel in `routes.sqlite` nach und reicht die Verbindung verschlüsselt mit
   PROXY-Protocol-Header über den Uplink an `10.78.x.y:443`. TLS endet erst im Gateway (rustls); nginx
   entschlüsselt nichts. Diese Oberfläche dient der Einrichtung.
2. **Handy → Dienst im LAN (Weg über den Server, CLAUDE.md 4.13):** Handy-WireGuard zu UDP 52000 →
   Server-Interface `phones` → Filter `phone_access` (Handy-Adresse, Gateway-Adresse, TCP-Port) → SNAT auf
   `10.78.0.2` → Uplink → Gateway. Das Gateway nimmt von `10.78.0.2` nur TCP auf Ports mit Weiterleitung an
   und öffnet dafür eine eigene TCP-Verbindung im LAN zum Ziel. Das Handy erreicht den Dienst unter
   `<uplink-adresse>:<port>`, z. B. `http://10.78.0.5:8000`, oder per Name über den Mini-DNS.
3. **Handy → Gateway direkt (alter Weg, läuft weiter, bis alle Handys umgestellt sind):** WireGuard zum
   UDP-Port des Gateways auf dem Server → nginx → Uplink → Handy-Tunnel im Gateway (`10.77.0.0/24`,
   Gateway `10.77.0.1`) → Kernel-Weg (TUN `rivet0`, nftables-DNAT in Tabelle `ip rivet`) oder, ohne
   `CAP_NET_ADMIN`, Weiterleitung im Userspace (smoltcp).
4. **Gateway → Portal:** HTTPS direkt übers Internet (nicht durch den Uplink), damit die Registrierung ohne
   Uplink funktioniert: `register`, `heartbeat`, `cert`, `peers` (Long-Poll), `uplink-key`.

**Uplink im Gateway** (`client/src/net/uplink.rs`): ein `boringtun::noise::Tunn` mit dem Server als einzigem
Peer über einen gewöhnlichen, ausgehenden UDP-Socket, dahinter ein smoltcp-Stack mit der Adresse `10.78.x.y`.
Angenommen wird nur, was an diese Adresse geht: von `10.78.0.1` (nginx) TCP 443/80, UDP 51820 und ICMP; von
`10.78.0.2` nur TCP. Fragmente und alle anderen Absender werden verworfen. Keepalive 15 s, MTU 1280. Nach
180 s ohne Handshake öffnet das Gateway einen neuen UDP-Socket und löst den Servernamen neu auf (gegen
einseitig tote NAT-Zuordnungen im Mobilfunk). Höchstens 256 gleichzeitige Verbindungen im Uplink-Stack.

**Betriebsarten** (Feld `uplink_mode` im Portal, `models.py`): `rivet` (Rivet-Gateway hält den Tunnel
selbst), `router` (der WireGuard des Routers hält den Tunnel, ein Rivet-Gateway dahinter bindet sich per Code
an), `client` (reiner WireGuard-Client ohne Rivet, kein Heartbeat). Erstes Router-Ziel laut `CLAUDE.md`:
Teltonika RUT241, Anleitung `docs/router-rutos.md`.

### Adressschema und Zertifikate {#adressen}

Die Namen ergeben sich aus vier Ebenen (`server/portal/gateways/hosts.py`; die Basisdomain ist eine
Einstellung, Vorgabe `forgeiec.io`):

| Ebene | Adresse | Im Code |
|---|---|---|
| Betreiber (Installation) | `rivet.<basis>` | `RIVET_PORTAL_HOST`: Betreiberbereich, Gateway-API, Uplink-Endpoint |
| Organisation | `<zone>.<basis>` | Modell `Zone` |
| Kunde | `<kunde>.<zone>.<basis>` | Modell `Organisation` |
| Gerät | `<gerät>.<kunde>.<zone>.<basis>` | `Gateway.fqdn`; hier antwortet das Gateway, nicht das Portal |

Die README nennt noch das ältere Schema `<slug>.<zone>.forgeiec.io`; der Code verwendet das obige.

- **Wildcard-Zertifikat je Kunde** `*.<kunde>.<zone>.<basis>`: ausgestellt von certbot mit
  `certbot-dns-hetzner` (DNS-01, ECDSA) aus dem venv des Portals; Erneuerung per Timer
  `forgeiec-rivet-certs` (täglich 03:00 und 15:00).
- **Verteilung:** Der Deploy-Hook `import_wildcard_cert` legt den privaten Schlüssel Fernet-verschlüsselt in
  der Portal-Datenbank ab und erhöht die `cert_version` des Kunden. Das Gateway sieht die höhere Version in
  der Heartbeat-Antwort und holt `GET /api/v1/cert` (Bearer-Schlüssel des Gateways, Antwort mit
  `Cache-Control: no-store`). Jeder Abruf wird in `CertFetchLog` protokolliert. Gesperrte Gateways bekommen
  nichts (API 403).
- **Prüfung im Gateway** (`client/src/tls.rs`) vor der Übernahme: PEM lesbar, Schlüssel passt zum
  Zertifikat, Name deckt die eigene Adresse ab, nicht abgelaufen, neuer als das aktive. Dann atomar
  geschrieben (Schlüssel 0600) und per `ArcSwap` ohne Neustart aktiviert. Fehlt ein gültiges Wildcard,
  nutzt das Gateway ein selbst signiertes Zertifikat (rcgen).
- **Portale** haben eigene Zertifikate; ein Gateway-Wildcard deckt sie nicht ab. Notfall-Rotation je Zone im
  Betreiberbereich und im Django-Admin (`services.emergency_rotation`).
- **DNS:** Das Portal pflegt die Einträge bei Hetzner (`gateways/dns.py`, Timer `forgeiec-rivet-dns` alle
  15 Minuten) und fasst nur Einträge mit seinen eigenen Labels an.

### Identität und Berechtigung {#identitaet}

| Geheimnis | Wie es entsteht | Wo es liegt | Wer es sieht |
|---|---|---|---|
| UI-Zugangsschlüssel des Gateways | `rvt_` + 32 Zufallsbytes (base64url), beim ersten Start | nur SHA-256 in `config.json`; Klartext einmal im Journal und in `initial-api-key` (0600) | wer am Gerät die Datei bzw. das Journal lesen darf |
| Schlüssel Gateway → Portal | `rgw_` + `secrets.token_urlsafe(32)` bei der Registrierung | Gateway: `config.json` (0600); Portal: nur SHA-256 | nur das Gateway |
| Registrierungscode | einmalig, Vorgabe 14 Tage gültig (`RIVET_REGISTRATION_CODE_DAYS`) | Portal | Person, die das Gateway einrichtet |
| Privater Schlüssel eines Handys | in der WireGuard-App oder im Browser (WebCrypto X25519, `phone_qr.js`) | nur auf dem Handy | niemand sonst; an das Portal geht nur der öffentliche Schlüssel, ein Feld mit „private“ wird mit 400 abgewiesen |
| Uplink-Schlüssel des Gateways | im Gateway (Betriebsart `rivet`) | `config.json` (0600) | nur das Gateway |
| Uplink-Schlüssel eines Routers | empfohlen im Router selbst; alternativ im Portal erzeugt und **einmal** angezeigt, nicht gespeichert | Router | – |
| Wildcard-Schlüssel des Kunden | certbot auf dem Server | Portal-DB (Fernet) und auf **jedem** Gateway dieses Kunden | Server und Gateways des Kunden |
| WireGuard-Schlüssel des Servers | postinst (X25519 aus `cryptography`) | `/etc/forgeiec/rivet-server/{uplink,phones}.key`, 0600 root; der Dienst bekommt sie per `LoadCredential` | Server |

- **Anmeldung am Gateway** (`client/src/auth.rs`, `web.rs`): Vergleich in konstanter Zeit (`subtle`),
  verschlüsseltes Sitzungs-Cookie (Rocket `secrets`) für 12 Stunden mit einem Präfix des Schlüssel-Hashes, so
  dass ein neuer Schlüssel alle Sitzungen beendet. Fehlversuche: 1 s Verzögerung, höchstens 5 je Quell-IP
  und 30 insgesamt in 5 Minuten.
- **Registrierung:** `POST /api/v1/register` ohne Anmeldung, begrenzt auf `10/hour` je Client-IP
  (`FORGEIEC_RIVET_REGISTER_RATE`). Alle anderen API-Aufrufe mit Bearer-Schlüssel, im Portal nur als Hash.
- **Handy einrichten:** QR-Code und `.conf`-Datei entstehen im Browser; der private Schlüssel verlässt die
  Seite nie. Alternativ ein Einrichtungslink per Mail: im Portal nur der SHA-256 des Tokens, 7 Tage gültig,
  einmal verwendbar.
- **Portal-Konten** sind an ihre Ebene gebunden; Rechte je Mitgliedschaft: Handys, Gateways, Benutzer
  verwalten. Die Sitzung gilt nur für den Host, an dem sie entstand.

### Isolation {#isolation}

- **Was ein Handy erreicht** (Weg über den Server): nur TCP zu `(Handy-Adresse, Uplink-Adresse eines
  Gateways, Port)` aus der Zugriffsliste. Sie enthält die Weiterleitungen aller aktiven Gateways **seines**
  Kunden; Regeln mit Zugang „Service“ nur für Handys mit Zugang „Service“. Dazu der Mini-DNS auf
  `10.79.0.1:53`. Alles andere aus `phones` wird verworfen (`fw.rs`).
- **Was ein kompromittiertes Gateway erreicht:** Auf dem Server gilt `iifname "uplink" oifname "uplink" drop`
  und `iifname "uplink" drop`: keine anderen Gateways, kein Routing über den Server. Zu den Handys nur
  Antworten (`oifname "phones"` nur `established,related`). Es besitzt aber den Wildcard-Schlüssel seines
  Kunden und kann sich damit als jedes andere Gateway **dieses Kunden** ausgeben, wenn es zusätzlich DNS oder
  Verkehr umleiten kann (in `CLAUDE.md` Abschnitt 5 als bewusst akzeptiertes Risiko beschrieben).
- **Was der Server erreicht:** Das Gateway nimmt aus dem Uplink nur die oben genannten Verbindungen an; ins
  LAN führen nur die Weiterleitungen aus dem Portal. Ohne Weiterleitung wird nichts weitergeleitet.
- **Was der Server sieht:** HTTPS zur Gateway-Oberfläche läuft verschlüsselt durch (Passthrough). Den
  inneren Verkehr der Handys auf dem Weg über den Server sieht er dagegen, weil er die Handy-Tunnel
  entschlüsselt (`CLAUDE.md` 4.13: „bewusst akzeptiert“). Was die Anwendung nicht selbst verschlüsselt, liegt
  dort im Klartext vor.
- **Überlappende LAN-Netze** sind möglich: In kein LAN wird geroutet, der Server kennt nur die je Gateway
  eindeutige `10.78.x.y`.

### Routing-Modul `ngx_stream_rivet_module` {#routing}

<details>
<summary>Wie das Modul arbeitet (aus <code>server/nginx-module/</code>)</summary>

- Direktiven `sqlite_map_database`, `sqlite_map <eingabe> $<ausgabe> { query …; default …; cache_ttl …; }`,
  `allow_backend`, `sqlite_map_check_changes`.
- Je Worker öffnet `init_process` die Datenbank mit `SQLITE_OPEN_READONLY | SQLITE_OPEN_NOMUTEX`,
  `PRAGMA query_only = 1`, Busy-Timeout 20 ms; Statements einmal mit `sqlite3_prepare_v3(…,
  SQLITE_PREPARE_PERSISTENT)`.
- **Ohne Reload:** Cache je Worker (positiv und negativ, LRU) wird verworfen, sobald sich
  `PRAGMA data_version` ändert oder die Datei ersetzt wurde (neuer Inode). Neue oder gesperrte Gateways
  wirken damit sofort.
- **Eingabe geprüft,** bevor sie an SQLite geht (SNI klein geschrieben, 1–253 Zeichen, nur `[a-z0-9.-]`),
  danach nur als gebundener Parameter `?1`. **Ausgabe geprüft:** nur `IPv4:Port` bzw. `[IPv6]:Port` innerhalb
  `allow_backend` (Standard `10.78.0.0/16`), sonst `default` (Schutz vor Weiterleitung auf beliebige Ziele).
- Fehlt die DB oder ist sie kaputt, gilt `default`; nginx läuft weiter, Portale hängen nie an der DB
  (statische `map`).
- Tabelle `routes` (`fqdn`, `zone`, `tls_backend`, `udp_port`, `wg_backend`, `enabled`, `updated_at`); einziger
  Schreiber ist Django (`gateways/routes.py`), `manage.py sync_routes` baut sie neu auf.

</details>

### Betrieb {#betrieb}

| Was | Wert | Quelle |
|---|---|---|
| Heartbeat | alle 5 Minuten und nach dem Start; Version, Uptime, Uplink-Handshake, je Handy Handshake und rx/tx, Zertifikats- und Theme-Version, angewandte Firewall; keine Schlüssel | `client/src/sync.rs`, `api.py` |
| Handy-Liste und Weiterleitungen | Long-Poll `GET /api/v1/peers`, Server hält bis 60 s; letzte Liste offline in `peers.json` | `api.py`, `settings.py` |
| Heartbeats aufräumen | Timer `forgeiec-rivet-cleanup`, täglich, Aufbewahrung 30 Tage | `server/contrib/` |
| Peers abgleichen | Timer `forgeiec-rivet-uplink-sync` alle 10 Minuten | `server/wg-daemon/contrib/` |
| Handys: zuletzt gesehen, Datenmenge | aus dem Server-Interface `phones` (Status von `forgeiec-rivet-wg`), sonst aus dem Heartbeat | `Phone.connection` in `models.py` |
| Gateway-Dienst | Konto `blacksmith`, kein root; `CAP_NET_BIND_SERVICE` und `CAP_NET_ADMIN`; `ProtectSystem=strict`, `NoNewPrivileges` | `client/contrib/forgeiec-rivet.service` |

Hinweis: Die README beschreibt den Gateway-Dienst noch ohne nftables und nur mit `CAP_NET_BIND_SERVICE`.
Der aktuelle Code braucht für den Kernel-Weg zusätzlich `CAP_NET_ADMIN` (TUN `rivet0`, nftables per Netlink,
ohne externe Programme).

### Plattformen, Pakete und Bau {#pakete}

- **Gebaut für 12 Slots**, Gateway und Server gleich: Debian 12/13 und Ubuntu 22.04/24.04, je amd64, arm64
  und armhf (`client/contrib/slot-build.sh --list`). Als Zielhardware des Gateways nennt `CLAUDE.md`
  Debian 12 arm64 und Ubuntu 24.04 armhf. Das nginx-Modul ist laut seiner README nur gegen nginx 1.26.3
  (Debian 13) gebaut und getestet.
- **Pakete:** `forgeiec-rivet` (cargo-deb) und `forgeiec-rivet-server` (CMake/CPack), gebaut nativ im
  Container der Zielarchitektur (podman, qemu-user), nicht per Cross-Compile.
- **`client/deploy.sh`:** `build` (Standard), `rebuild`, `test`, `run` (Probelauf ohne root auf 8443/8080),
  `peer`, `package`, `slot <s|all>`, `install`, `restart`, `clean`, `help`. **`server/deploy.sh`:**
  `configure`, `rebuild`, `test`, `run`, `package`, `install`, `restart`, `clean`, `slot`, `help`.
- **CI:** Forgejo-Workflows `client.yml` und `server.yml`, je eine Matrix über die 12 Slots; nach
  `apt.forgeiec.io` veröffentlicht nur `main`.

### Qualität {#qualitaet}

| Teil | Tests | Status |
|---|---|---|
| Gateway (`client/`) | `cargo test`: **94 bestanden, 1 übersprungen** (der Kernel-Test `kernel_weg` läuft nur mit `unshare -rn`) | am 22.10.2026 ausgeführt (`--offline`, Commit `5f01540`) |
| WireGuard-Dienst | 69 Testfunktionen; dazu `tests/kernel-netns.sh` mit echter WireGuard-Gegenstelle (laut README 39 Prüfungen) | gezählt, nicht ausgeführt |
| Portal | 421 Testmethoden, davon 4 Live-Tests gegen die Hetzner-API (nur mit Token) | gezählt, nicht ausgeführt |
| nginx-Modul | Unit-Tests in C (103 Prüfungen), 20 Integrationstests mit echtem nginx, Lasttest | Ergebnisse vom 27.09.2026 laut `server/nginx-module/README.md` |

Der Lasttest des nginx-Moduls (laut dessen README, 1000 Verbindungen mit 20 parallelen Clients, Ryzen 9 9950X
im Podman-Container) ergab rund 11 600 Verbindungen pro Sekunde mit und ohne DB-Abfrage; die gemessene Latenz
bestimmt dort der Python-Client, nicht die Abfrage. Weitere Leistungs- oder Verfügbarkeitszahlen gibt es nicht.

### Repository {#repository}

<details>
<summary>Aufbau von <code>forgeiec-rivet</code></summary>

```
client/          Gateway (Rust): src/{main,auth,config,front,tls,web,setup,sync,portal,forwards}.rs,
                 src/net/{uplink,hub,peers,stack}.rs, src/sys/{tun,rtnl,nft}.rs, templates/, locale/
server/portal/   Django-Projekt rivet_server, App gateways (Modelle, API, Ebenen, Tests)
server/wg-daemon/  forgeiec-rivet-wg (Rust, Netlink, nftables, Mini-DNS)
server/nginx-module/  ngx_stream_rivet_module (C) mit Unit-, Integrations- und Lasttest
server/contrib/  systemd-Units und Timer, debconf/postinst, nginx-Vorlagen
docs/            api-v1.md, betrieb-server.md, router-rutos.md
.github/workflows/  client.yml, server.yml
```

Lizenzangabe in beiden `Cargo.toml`: `LicenseRef-proprietary`.

</details>

### Bedrohungsmodell (soweit `CLAUDE.md` es nennt) {#bedrohungen}

- **Gemeinsamer Wildcard-Schlüssel je Kunde** (bewusst akzeptiert): Wer ein Gateway ausliest, kann sich als
  beliebige Adresse unter `*.<kunde>.<zone>` ausgeben, nicht aber als Gateway eines anderen Kunden oder als
  Portal. Gegenmaßnahmen laut Spezifikation: Ausnutzen braucht zusätzlich Umleitung von DNS oder Verkehr;
  Portale unter eigenen Zertifikaten; Sitzungs-Cookie nur für den eigenen Host; Notfall-Rotation; gesperrte
  Gateways bekommen keine neuen Zertifikate; kurze Laufzeiten von Let's Encrypt.
- **Der Server ist der Vertrauensanker**: Er verteilt die Schlüssel und sieht den inneren Verkehr der Handys
  auf dem Weg über den Server (bewusst akzeptiert).
- **Router-Gateways:** Ob der Server ins LAN kommt, entscheidet dort die Firewall des Routers, nicht Rivet.
- **Manipulierte Routing-Datenbank:** Das nginx-Modul nimmt nur Ziele innerhalb `allow_backend` an.
- **ECH** würde den SNI verbergen; für die Rivet-Zonen werden deshalb keine DNS-HTTPS-Records mit ECH
  veröffentlicht.
- **UDP gesperrt oder gedrosselt** im Mobilfunk: Dann steht der Uplink nicht (offene Frage 11).
- **Abhängigkeit vom Server:** Ohne Server kein Fernzugriff; das LAN selbst arbeitet weiter (offene Frage 8).

### Bekannte Grenzen {#grenzen}

- Weiterleitungen nur für TCP; höchstens 20 Regeln je Gateway; im Tunnel nur IPv4.
- Kommt ein Gateway zum Kunden hinzu, braucht das Handy eine neue Konfiguration (`AllowedIPs`).
- Kein Ausweichweg, wenn UDP gesperrt ist; kein Direktzugang bei Serverausfall.
- Theme-Übernahme auf dem Gateway, Alarm-Mails, `install.sh` und der Selbsttest für Router-Gateways fehlen
  noch (siehe [Stand der Umsetzung](#stand)).
- Zwei Handy-Wege laufen parallel, bis der alte über das Gateway entfällt.

### Im Unterschied zu … {#vergleich}

Die Tabelle nennt nur Eigenschaften, die aus dem Aufbau folgen.

| | Portfreigabe am Router | Hersteller-Cloud | kommerzieller VPN-Dienst | Rivet |
|---|---|---|---|---|
| Eingehender Port am Standort | ja | nein | je nach Produkt | nein, das Gateway baut nur ausgehend auf |
| Steuerung im Internet sichtbar | ja | nein | nein | nein |
| Dritter im Datenpfad | nein | ja (Hersteller) | ja (Anbieter) | nein, nur der ForgeIEC-Server |
| Funktioniert ohne öffentliche IP (CGNAT, Mobilfunk) | nein | ja | ja | ja |
| Freigabe je Handy und Port | nein | je nach Produkt | je nach Produkt | ja, im Portal |
| Wer sieht entschlüsselten Verkehr | niemand dazwischen | der Hersteller | je nach Produkt | der ForgeIEC-Server beim Handy-Weg über den Server (siehe [Isolation](#isolation)) |

</div>
