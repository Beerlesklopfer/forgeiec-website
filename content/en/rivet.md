---
title: "Rivet"
date: 2026-10-22
draft: false
wide: true
description: "Rivet: remote access from a phone to controllers in the local network, without port forwarding and without a third-party cloud. Status: in development, pilot with solidarity farms."
---

<style>
.rv { --rv-line: var(--text, currentColor); --rv-accent: var(--brand, #F59E0B); --rv-box: rgba(148,163,184,.12); --rv-muted: rgba(148,163,184,.9); }
.rv-lead { font-size: 1.2em; line-height: 1.5; margin: 0 0 1.2em; }
.rv-cards { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 1em; margin: 1.2em 0; }
.rv-card { border: 1px solid rgba(148,163,184,.35); border-radius: .4em; padding: .9em 1em; background: var(--rv-box); }
.rv-card h3 { margin: 0 0 .4em; font-size: 1.05em; }
.rv-card p { margin: 0; }
.rv h3 { margin-top: 1.6em; }
.rv > :first-child { margin-top: 0; }
.rv-shot { max-width: 36rem; }
.rv .rv-card h3 { margin: 0 0 .4em; }
/* Tables sit inside .rv, so the redesign rule for .prose > table does not reach them. */
.rv table { display: block; overflow-x: auto; max-width: 100%; border: 1px solid var(--border); border-radius: var(--radius); margin: 1.5rem 0; }
.rv-fig { margin: 1.4em 0; }
.rv-fig svg { width: 100%; height: auto; display: block; }
.rv-fig .rv-v { display: none; max-width: 340px; margin: 0 auto; }
.rv-fig figcaption { font-size: .9em; opacity: .85; margin-top: .4em; }
.rv-two { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 1.4em; }
.prose .rv table { font-size: .92em; }
.prose .rv th { padding: .5em .7em; text-align: left; vertical-align: bottom; }
.prose .rv td { padding: .6em .7em; vertical-align: top; }
.prose .rv table td:first-child { white-space: normal; width: auto; min-width: 7em; }
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
  .prose .rv table { display: block; overflow-x: auto; max-width: 100%; }
  .prose .rv th, .prose .rv td { min-width: 10em; }
}
</style>

<div class="rv">

## Operate your plant from a phone – without opening a door into your network {#benefit}

<p class="rv-lead">Rivet connects the phone of an authorised person with a controller in the local network.
No port forwarding has to be set up on site, and no third-party cloud provider is involved.</p>

{{< callout type="warning" title="Status: in development" >}}
Rivet is not a finished product yet. The code is being written and has so far been tried on a test server.
The first intended use: solidarity farms (SoLaWis) want to operate their irrigation control from a phone
with it.
{{< /callout >}}

<div class="rv-cards">
<div class="rv-card">
<h3>The problem</h3>
<p>Irrigation, heating, pumps or PLCs often have a user interface in the local network. Whoever wants to reach
it from elsewhere usually puts it straight on the internet or ties themselves to a vendor cloud.</p>
</div>
<div class="rv-card">
<h3>The solution</h3>
<p>A small gateway on site opens the connection to our server <strong>from the inside out</strong>. Over
this path the phone reaches only the services you have released in the portal, nothing else.</p>
</div>
<div class="rv-card">
<h3>What stays under your control</h3>
<p>You decide in the portal which phones reach which plant. A blocked phone is out within seconds. A phone's
key is created on the phone and never leaves it.</p>
</div>
</div>

<figure class="rv-fig" role="img" aria-label="Phone, ForgeIEC server, gateway and controller: the gateway opens the connection to the server from inside">
<svg class="rv-h" viewBox="0 0 800 190" xmlns="http://www.w3.org/2000/svg" font-family="Inter, system-ui, sans-serif" font-size="15" fill="currentColor">
  <defs>
    <marker id="rv-ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="currentColor"/></marker>
    <marker id="rv-ah2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="var(--rv-accent, #F59E0B)"/></marker>
  </defs>
  <rect x="462" y="18" width="328" height="160" rx="10" fill="none" stroke="currentColor" stroke-dasharray="5 5" opacity=".55"/>
  <text x="621" y="40" text-anchor="middle" font-size="13" opacity=".8">Your local network (no open port)</text>
  <rect x="10" y="78" width="130" height="58" rx="8" fill="var(--rv-box, rgba(148,163,184,.12))" stroke="currentColor"/>
  <text x="75" y="112" text-anchor="middle" font-weight="600">Phone</text>
  <rect x="226" y="78" width="150" height="58" rx="8" fill="var(--rv-box, rgba(148,163,184,.12))" stroke="currentColor"/>
  <text x="301" y="104" text-anchor="middle" font-weight="600">ForgeIEC</text>
  <text x="301" y="122" text-anchor="middle" font-weight="600">server</text>
  <rect x="470" y="78" width="130" height="58" rx="8" fill="var(--rv-box, rgba(148,163,184,.12))" stroke="currentColor"/>
  <text x="535" y="112" text-anchor="middle" font-weight="600">Gateway</text>
  <rect x="650" y="78" width="126" height="58" rx="8" fill="var(--rv-box, rgba(148,163,184,.12))" stroke="currentColor"/>
  <text x="713" y="112" text-anchor="middle" font-weight="600">Controller</text>
  <line x1="142" y1="107" x2="222" y2="107" stroke="currentColor" stroke-width="2" marker-end="url(#rv-ah)" marker-start="url(#rv-ah)"/>
  <text x="182" y="96" text-anchor="middle" font-size="12">encrypted</text>
  <line x1="466" y1="107" x2="380" y2="107" stroke="var(--rv-accent, #F59E0B)" stroke-width="3" marker-end="url(#rv-ah2)"/>
  <text x="418" y="152" text-anchor="middle" font-size="12" fill="var(--rv-accent, #F59E0B)">opened from</text>
  <text x="418" y="167" text-anchor="middle" font-size="12" fill="var(--rv-accent, #F59E0B)">inside</text>
  <line x1="602" y1="107" x2="646" y2="107" stroke="currentColor" stroke-width="2" marker-end="url(#rv-ah)"/>
</svg>
<svg class="rv-v" viewBox="0 0 320 470" xmlns="http://www.w3.org/2000/svg" font-family="Inter, system-ui, sans-serif" font-size="16" fill="currentColor">
  <defs>
    <marker id="rv-av" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="currentColor"/></marker>
    <marker id="rv-av2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="var(--rv-accent, #F59E0B)"/></marker>
  </defs>
  <rect x="85" y="10" width="150" height="54" rx="8" fill="var(--rv-box, rgba(148,163,184,.12))" stroke="currentColor"/>
  <text x="160" y="43" text-anchor="middle" font-weight="600">Phone</text>
  <line x1="160" y1="68" x2="160" y2="118" stroke="currentColor" stroke-width="2" marker-end="url(#rv-av)" marker-start="url(#rv-av)"/>
  <text x="172" y="98" font-size="13">encrypted</text>
  <rect x="85" y="122" width="150" height="54" rx="8" fill="var(--rv-box, rgba(148,163,184,.12))" stroke="currentColor"/>
  <text x="160" y="155" text-anchor="middle" font-weight="600">ForgeIEC server</text>
  <line x1="160" y1="252" x2="160" y2="180" stroke="var(--rv-accent, #F59E0B)" stroke-width="3" marker-end="url(#rv-av2)"/>
  <text x="172" y="212" font-size="13" fill="var(--rv-accent, #F59E0B)">opened from inside</text>
  <rect x="20" y="240" width="280" height="220" rx="10" fill="none" stroke="currentColor" stroke-dasharray="5 5" opacity=".55"/>
  <text x="160" y="450" text-anchor="middle" font-size="13" opacity=".8">Your local network (no open port)</text>
  <rect x="85" y="256" width="150" height="54" rx="8" fill="var(--rv-box, rgba(148,163,184,.12))" stroke="currentColor"/>
  <text x="160" y="289" text-anchor="middle" font-weight="600">Gateway</text>
  <line x1="160" y1="314" x2="160" y2="358" stroke="currentColor" stroke-width="2" marker-end="url(#rv-av)"/>
  <rect x="85" y="362" width="150" height="54" rx="8" fill="var(--rv-box, rgba(148,163,184,.12))" stroke="currentColor"/>
  <text x="160" y="395" text-anchor="middle" font-weight="600">Controller</text>
</svg>
<figcaption>The gateway opens the connection from inside. That is why no door has to be opened on the internet
connection; mobile connections without their own public address work too.</figcaption>
</figure>

<div class="rv-two">
<div>

### Who it is for

For machine and plant builders who want to service their machines at the customer's site remotely, without a
cloud vendor in between. And for operators who want to operate their own plant from a phone.
<!-- ENTWURF: The target group "machine and plant builders" is the owner's brief; the repository speaks of "operators of plants" and "not bound to an industry" (README.md, CLAUDE.md 1). -->

### What you do on site

1. Plug the gateway into the local network of the controller (or install Rivet as a package on the device itself).
   <!-- ENTWURF: Which gateway hardware is supplied is open (CLAUDE.md 11, question 6: "concrete boards?"). -->
2. Open the gateway's web interface and sign in with the access key.
3. Enter the registration code from the portal. What can be reached is set in the portal.
4. Add phones in the portal: scan the QR code with the WireGuard app, switch the tunnel on.

</div>
<div>

### What Rivet is not

- **Not a cloud service of a third party.** ForgeIEC runs gateway, server and portal itself.
- **Not a replacement for safety functions.** Emergency stop, interlocks and everything that makes a plant
  safe belong in the plant, not in a remote access.
- **Not a finished product yet** (see status above).

### Next step

<p class="rv-cta">Would you like to try Rivet in a pilot? <a href="/en/contact/?type=pilot">Request a pilot</a></p>
<!-- ENTWURF: A pilot offer (scope, terms, costs) is not described in the repository. -->

</div>
</div>

<div class="rv-two">
<div>

{{< screenshot program="rivet" name="gateway-setup" alt="Setting up the Rivet gateway in the browser" caption="Setting up the gateway: enter the registration code, choose the mode." >}}

</div>
<div>

{{< screenshot program="rivet" name="portal-phone-setup" alt="Rivet portal: add a phone with a QR code for the WireGuard app" caption="Adding a phone: scan the QR code with the WireGuard app." >}}

</div>
</div>

---

## For experts: the technology in detail {#technology}

Everything below can be checked in the repository `forgeiec-rivet` (branch `development`, commit `5f01540`,
22 Oct 2026). The specification is `CLAUDE.md` in that repository. We distinguish strictly between
**implemented** (code and tests present), **specified** (described in `CLAUDE.md`, not coded) and
**planned/open** (recorded as an open question or as "later").

### Implementation status {#status}

| Area | Implemented | Specified, not coded | Planned / open |
|---|---|---|---|
| Gateway | uplink in-process (boringtun + smoltcp), TLS front end with certificate swap at runtime, setup wizard, registration, heartbeat, long poll for phones and forwards, forwards (userspace and kernel path via TUN `rivet0` + nftables), router configuration for router gateways | fetching and swapping themes on the gateway (portal side exists); renewing the API key from the web interface (`POST /api/apikey/rotate`; only the command `forgeiec-rivet reset-api-key` exists) | own Rivet app for Android/iOS (open question 14) |
| Server | portal with three levels, API v1, `routes.sqlite` + nginx module, WireGuard service `forgeiec-rivet-wg` (interfaces `uplink` and `phones`, nftables, mini DNS), DNS sync with Hetzner, wildcard certificates via certbot (DNS-01), emergency rotation, e-mails (account access, setup link), cleanup timer, packages and CI | `install.sh` (bootstrap); alert e-mails (gateway offline, certificate expiring, unusual fetches); releases with `SHA256SUMS` and signature | terminate TLS in nginx instead of wildcards on the gateways (open question 1) |
| Operations | builds for 12 slots, packages `forgeiec-rivet` and `forgeiec-rivet-server` | self-test for router gateways ("does the router let more into the LAN?"); interop test in CI against kernel WireGuard or `wireguard-go` as the gateway's peer | fallback over TCP 443 when UDP is blocked (open question 11); direct access when the server is down (open question 8); switching off the old phone path via the gateway |

### Architecture {#architecture}

| Component | Code | Technology (checked in `Cargo.toml`, `requirements.txt` or source) | Task |
|---|---|---|---|
| **Gateway** `forgeiec-rivet` | `client/` | Rust (edition 2024), tokio; `boringtun 0.7` without default features (only `noise::Tunn`); `smoltcp 0.14`; `rustls 0.23` with `ring` + `tokio-rustls`; `hyper 1`; `Rocket 0.5` (`json`, `secrets`) with `rocket_dyn_templates` (Tera); `fluent-bundle`; `ureq 2`; `rustables 0.9` and `netlink-*` for TUN/nftables; `x509-parser`, `rcgen`, `qrcode` | outbound uplink to the server, forwarding of released TCP ports into the LAN, setup web interface |
| **Portal** | `server/portal/` | Django 5.2, Django REST Framework 3.18, gunicorn (`127.0.0.1:8001`), `cryptography`, `certbot` + `certbot-dns-hetzner`, `hcloud` | levels and accounts, registration, heartbeat, certificates, phones, forwards; writes `routes.sqlite`, controls `forgeiec-rivet-wg` |
| **WireGuard service** `forgeiec-rivet-wg` (the privileged helper) | `server/wg-daemon/` | Rust, rust-netlink (`netlink-packet-wireguard`, `-route`, `-generic`), `rustables 0.9`; kernel WireGuard | holds the kernel interfaces `uplink` and `phones`, sets peers and the nftables table `ip rivet_server`, mini DNS for phones, delivers statistics |
| **nginx module** `ngx_stream_rivet_module` | `server/nginx-module/` | C, dynamic stream module, SQLite | TLS passthrough: target per SNI or UDP port from `routes.sqlite`, without reload |

**Ports on the server** (from `server/contrib/nginx/rivet-stream.conf.in`, `forgeiec-rivet-wg.service.in`, `settings.py`):

| Port | Protocol | Purpose |
|---|---|---|
| 80 | TCP | redirect to HTTPS |
| 443 | TCP | nginx `stream` with `ssl_preread`: portals → local `127.0.0.1:8443`, devices → `10.78.x.y:443` via the uplink, unknown → `127.0.0.1:8444` |
| 51900 | UDP | WireGuard `uplink` (server `10.78.0.1/16`), one peer per gateway |
| 52000 | UDP | WireGuard `phones` (server `10.79.0.1/16`), one peer per phone |
| 51000–51899, 51901–51999 | UDP | old phone path: one port per gateway, nginx passes it on to `10.78.x.y:51820` |
| 53 on `10.79.0.1` | UDP/TCP | mini DNS, only from the phone network `10.79.0.0/16` |

**Data paths**

1. **Browser → gateway web interface** `https://<device>.<customer>.<zone>.forgeiec.io`: nginx reads only the
   host name (SNI), looks the target up in `routes.sqlite` and passes the still-encrypted connection with a
   PROXY protocol header through the uplink to `10.78.x.y:443`. TLS ends only in the gateway (rustls); nginx
   decrypts nothing. This interface is for setup.
2. **Phone → service in the LAN (path via the server, CLAUDE.md 4.13):** phone WireGuard to UDP 52000 →
   server interface `phones` → filter `phone_access` (phone address, gateway address, TCP port) → SNAT to
   `10.78.0.2` → uplink → gateway. The gateway accepts from `10.78.0.2` only TCP on ports that have a forward
   and opens its own TCP connection in the LAN to the target. The phone reaches the service at
   `<uplink-address>:<port>`, e.g. `http://10.78.0.5:8000`, or by name through the mini DNS.
3. **Phone → gateway directly (old path, kept until all phones have moved):** WireGuard to the gateway's UDP
   port on the server → nginx → uplink → phone tunnel in the gateway (`10.77.0.0/24`, gateway `10.77.0.1`)
   → kernel path (TUN `rivet0`, nftables DNAT in table `ip rivet`) or, without `CAP_NET_ADMIN`, forwarding in
   userspace (smoltcp).
4. **Gateway → portal:** HTTPS directly over the internet (not through the uplink), so that registration works
   without an uplink: `register`, `heartbeat`, `cert`, `peers` (long poll), `uplink-key`.

**Uplink in the gateway** (`client/src/net/uplink.rs`): one `boringtun::noise::Tunn` with the server as the only
peer over an ordinary outbound UDP socket, behind it a smoltcp stack with the address `10.78.x.y`. Only traffic
to this address is accepted: from `10.78.0.1` (nginx) TCP 443/80, UDP 51820 and ICMP; from `10.78.0.2` TCP
only. Fragments and all other senders are dropped. Keepalive 15 s, MTU 1280. After 180 s without a handshake
the gateway opens a new UDP socket and resolves the server name again (against one-way dead NAT mappings on
mobile networks). At most 256 concurrent connections in the uplink stack.

**Operating modes** (field `uplink_mode` in the portal, `models.py`): `rivet` (the Rivet gateway holds the
tunnel itself), `router` (the router's WireGuard holds the tunnel, a Rivet gateway behind it binds with a code),
`client` (plain WireGuard client without Rivet, no heartbeat). First router target according to `CLAUDE.md`:
Teltonika RUT241, guide `docs/router-rutos.md`.

### Addressing and certificates {#addressing}

Names follow four levels (`server/portal/gateways/hosts.py`; the base domain is a setting, default
`forgeiec.io`):

| Level | Address | In the code |
|---|---|---|
| Operator (installation) | `rivet.<base>` | `RIVET_PORTAL_HOST`: operator area, gateway API, uplink endpoint |
| Organisation | `<zone>.<base>` | model `Zone` |
| Customer | `<customer>.<zone>.<base>` | model `Organisation` |
| Device | `<device>.<customer>.<zone>.<base>` | `Gateway.fqdn`; the gateway answers here, not the portal |

The README still shows the older scheme `<slug>.<zone>.forgeiec.io`; the code uses the one above.

- **One wildcard certificate per customer** `*.<customer>.<zone>.<base>`: issued by certbot with
  `certbot-dns-hetzner` (DNS-01, ECDSA) from the portal's venv; renewal by the timer `forgeiec-rivet-certs`
  (daily at 03:00 and 15:00).
- **Distribution:** the deploy hook `import_wildcard_cert` stores the private key Fernet-encrypted in the portal
  database and raises the customer's `cert_version`. The gateway sees the higher version in the heartbeat
  response and fetches `GET /api/v1/cert` (gateway bearer key, response with `Cache-Control: no-store`). Every
  fetch is logged in `CertFetchLog`. Blocked gateways get nothing (API 403).
- **Checks in the gateway** (`client/src/tls.rs`) before taking it over: PEM readable, key matches the
  certificate, name covers the gateway's own address, not expired, newer than the active one. Then written
  atomically (key 0600) and activated via `ArcSwap` without restart. Without a valid wildcard the gateway uses
  a self-signed certificate (rcgen).
- **Portals** have their own certificates; a gateway wildcard does not cover them. Emergency rotation per zone
  in the operator area and in the Django admin (`services.emergency_rotation`).
- **DNS:** the portal maintains the records at Hetzner (`gateways/dns.py`, timer `forgeiec-rivet-dns` every
  15 minutes) and touches only records carrying its own labels.

### Identity and authorisation {#identity}

| Secret | How it is created | Where it is kept | Who sees it |
|---|---|---|---|
| Gateway web interface key | `rvt_` + 32 random bytes (base64url), on first start | only SHA-256 in `config.json`; plain text once in the journal and in `initial-api-key` (0600) | whoever may read that file or the journal on the device |
| Gateway → portal key | `rgw_` + `secrets.token_urlsafe(32)` at registration | gateway: `config.json` (0600); portal: only SHA-256 | only the gateway |
| Registration code | one-time, valid 14 days by default (`RIVET_REGISTRATION_CODE_DAYS`) | portal | the person setting up the gateway |
| A phone's private key | in the WireGuard app or in the browser (WebCrypto X25519, `phone_qr.js`) | only on the phone | nobody else; only the public key goes to the portal, a field containing "private" is rejected with 400 |
| Gateway uplink key | in the gateway (mode `rivet`) | `config.json` (0600) | only the gateway |
| A router's uplink key | recommended: in the router itself; alternatively generated in the portal and shown **once**, not stored | router | – |
| Customer wildcard key | certbot on the server | portal DB (Fernet) and on **every** gateway of that customer | the server and the customer's gateways |
| Server WireGuard keys | postinst (X25519 from `cryptography`) | `/etc/forgeiec/rivet-server/{uplink,phones}.key`, 0600 root; the service gets them via `LoadCredential` | the server |

- **Sign-in at the gateway** (`client/src/auth.rs`, `web.rs`): constant-time comparison (`subtle`), encrypted
  session cookie (Rocket `secrets`) for 12 hours with a prefix of the key hash, so a new key ends all sessions.
  Failed attempts: 1 s delay, at most 5 per source IP and 30 in total within 5 minutes.
- **Registration:** `POST /api/v1/register` without authentication, limited to `10/hour` per client IP
  (`FORGEIEC_RIVET_REGISTER_RATE`). All other API calls use a bearer key that the portal stores only as a hash.
- **Phone setup:** QR code and `.conf` file are created in the browser; the private key never leaves the page.
  Alternatively a setup link by e-mail: the portal stores only the SHA-256 of the token, valid 7 days, single use.
- **Portal accounts** are bound to their level; rights per membership: manage phones, gateways, users. The
  session is valid only for the host where it was created.

### Isolation {#isolation}

- **What a phone reaches** (path via the server): only TCP to `(phone address, uplink address of a gateway,
  port)` from the access list. It contains the forwards of all active gateways of **its** customer; rules with
  access "service" only for phones with access "service". Plus the mini DNS at `10.79.0.1:53`. Everything else
  from `phones` is dropped (`fw.rs`).
- **What a compromised gateway reaches:** on the server `iifname "uplink" oifname "uplink" drop` and
  `iifname "uplink" drop` apply: no other gateways, no routing through the server. Towards phones only replies
  (`oifname "phones"` only `established,related`). It does, however, hold its customer's wildcard key and can
  impersonate any other gateway **of that customer** if it can also redirect DNS or traffic (described in
  `CLAUDE.md` section 5 as a consciously accepted risk).
- **What the server reaches:** from the uplink the gateway accepts only the connections listed above; only the
  forwards from the portal lead into the LAN. Without a forward nothing is forwarded.
- **What the server sees:** HTTPS to the gateway web interface passes through encrypted (passthrough). The inner
  traffic of phones on the path via the server, however, it does see, because it decrypts the phone tunnels
  (`CLAUDE.md` 4.13: "consciously accepted"). Whatever the application does not encrypt itself is plain text there.
- **Overlapping LAN subnets** are possible: nothing is routed into any LAN; the server only knows the
  per-gateway unique `10.78.x.y`.

### Routing module `ngx_stream_rivet_module` {#routing}

<details>
<summary>How the module works (from <code>server/nginx-module/</code>)</summary>

- Directives `sqlite_map_database`, `sqlite_map <input> $<output> { query …; default …; cache_ttl …; }`,
  `allow_backend`, `sqlite_map_check_changes`.
- Per worker, `init_process` opens the database with `SQLITE_OPEN_READONLY | SQLITE_OPEN_NOMUTEX`,
  `PRAGMA query_only = 1`, busy timeout 20 ms; statements are prepared once with `sqlite3_prepare_v3(…,
  SQLITE_PREPARE_PERSISTENT)`.
- **No reload:** a cache per worker (positive and negative, LRU) is dropped as soon as `PRAGMA data_version`
  changes or the file was replaced (new inode). New or blocked gateways take effect immediately.
- **Input checked** before it reaches SQLite (SNI lower-cased, 1–253 characters, only `[a-z0-9.-]`), then
  passed only as the bound parameter `?1`. **Output checked:** only `IPv4:port` or `[IPv6]:port` within
  `allow_backend` (default `10.78.0.0/16`), otherwise `default` (protection against forwarding to arbitrary targets).
- If the DB is missing or broken, `default` applies; nginx keeps running, and portals never depend on the DB
  (static `map`).
- Table `routes` (`fqdn`, `zone`, `tls_backend`, `udp_port`, `wg_backend`, `enabled`, `updated_at`); the only
  writer is Django (`gateways/routes.py`), `manage.py sync_routes` rebuilds it.

</details>

### Operations {#operations}

| What | Value | Source |
|---|---|---|
| Heartbeat | every 5 minutes and after start; version, uptime, uplink handshake, per phone handshake and rx/tx, certificate and theme version, applied firewall; no keys | `client/src/sync.rs`, `api.py` |
| Phone list and forwards | long poll `GET /api/v1/peers`, the server holds up to 60 s; last list kept offline in `peers.json` | `api.py`, `settings.py` |
| Heartbeat cleanup | timer `forgeiec-rivet-cleanup`, daily, retention 30 days | `server/contrib/` |
| Peer sync | timer `forgeiec-rivet-uplink-sync` every 10 minutes | `server/wg-daemon/contrib/` |
| Phones: last seen, data volume | from the server interface `phones` (status of `forgeiec-rivet-wg`), otherwise from the heartbeat | `Phone.connection` in `models.py` |
| Gateway service | account `blacksmith`, no root; `CAP_NET_BIND_SERVICE` and `CAP_NET_ADMIN`; `ProtectSystem=strict`, `NoNewPrivileges` | `client/contrib/forgeiec-rivet.service` |

<div class="rv-shot">

{{< screenshot program="rivet" name="gateway-overview" alt="Rivet gateway overview with address, certificate and connection state" caption="Gateway overview: address, certificate, tunnel to the server, portal." >}}

</div>

Note: the README still describes the gateway service without nftables and with `CAP_NET_BIND_SERVICE` only.
The current code additionally needs `CAP_NET_ADMIN` for the kernel path (TUN `rivet0`, nftables via netlink,
no external programs).

### Platforms, packages and build {#packages}

- **Built for 12 slots**, gateway and server alike: Debian 12/13 and Ubuntu 22.04/24.04, each amd64, arm64
  and armhf (`client/contrib/slot-build.sh --list`). As target hardware for the gateway `CLAUDE.md` names
  Debian 12 arm64 and Ubuntu 24.04 armhf. According to its README, the nginx module has only been built and
  tested against nginx 1.26.3 (Debian 13).
- **Packages:** `forgeiec-rivet` (cargo-deb) and `forgeiec-rivet-server` (CMake/CPack), built natively in a
  container of the target architecture (podman, qemu-user), not cross-compiled.
- **`client/deploy.sh`:** `build` (default), `rebuild`, `test`, `run` (dry run without root on 8443/8080),
  `peer`, `package`, `slot <s|all>`, `install`, `restart`, `clean`, `help`. **`server/deploy.sh`:**
  `configure`, `rebuild`, `test`, `run`, `package`, `install`, `restart`, `clean`, `slot`, `help`.
- **CI:** Forgejo workflows `client.yml` and `server.yml`, each a matrix over the 12 slots; only `main`
  publishes to `apt.forgeiec.io`.

### Quality {#quality}

| Part | Tests | Status |
|---|---|---|
| Gateway (`client/`) | `cargo test`: **94 passed, 1 ignored** (the kernel test `kernel_weg` runs only under `unshare -rn`) | run on 22 Oct 2026 (`--offline`, commit `5f01540`) |
| WireGuard service | 69 test functions; plus `tests/kernel-netns.sh` with a real WireGuard peer (39 checks according to its README) | counted, not run |
| Portal | 421 test methods, 4 of them live tests against the Hetzner API (only with a token) | counted, not run |
| nginx module | C unit tests (103 checks), 20 integration tests with a real nginx, load test | results of 27 Sep 2026 according to `server/nginx-module/README.md` |

The nginx module's load test (according to its README: 1000 connections with 20 parallel clients, Ryzen 9 9950X
in a Podman container) reached about 11,600 connections per second with and without a DB query; the measured
latency there is dominated by the Python client, not by the query. There are no other performance or
availability figures.

### Repository {#repository}

<details>
<summary>Layout of <code>forgeiec-rivet</code></summary>

```
client/          gateway (Rust): src/{main,auth,config,front,tls,web,setup,sync,portal,forwards}.rs,
                 src/net/{uplink,hub,peers,stack}.rs, src/sys/{tun,rtnl,nft}.rs, templates/, locale/
server/portal/   Django project rivet_server, app gateways (models, API, levels, tests)
server/wg-daemon/  forgeiec-rivet-wg (Rust, netlink, nftables, mini DNS)
server/nginx-module/  ngx_stream_rivet_module (C) with unit, integration and load tests
server/contrib/  systemd units and timers, debconf/postinst, nginx templates
docs/            api-v1.md, betrieb-server.md, router-rutos.md
.github/workflows/  client.yml, server.yml
```

Licence field in both `Cargo.toml` files: `LicenseRef-proprietary`.

</details>

### Threat model (as far as `CLAUDE.md` states it) {#threats}

- **Shared wildcard key per customer** (consciously accepted): whoever extracts it from a gateway can pose as any
  address under `*.<customer>.<zone>`, but not as a gateway of another customer or as a portal.
  Countermeasures in the specification: exploiting it also requires redirecting DNS or traffic; portals under
  their own certificates; session cookie only for its own host; emergency rotation; blocked gateways receive
  no new certificates; short Let's Encrypt lifetimes.
- **The server is the trust anchor**: it distributes the keys and sees the inner traffic of phones on the path
  via the server (consciously accepted).
- **Router gateways:** there, the router's firewall decides whether the server gets into the LAN, not Rivet.
- **Tampered routing database:** the nginx module accepts only targets within `allow_backend`.
- **ECH** would hide the SNI; therefore no DNS HTTPS records with ECH are published for the Rivet zones.
- **UDP blocked or throttled** on mobile networks: then the uplink does not come up (open question 11).
- **Dependence on the server:** without the server there is no remote access; the LAN itself keeps working
  (open question 8).

### Known limits {#limits}

- Forwards for TCP only; at most 20 rules per gateway; IPv4 only inside the tunnel.
- When a gateway is added to the customer, the phone needs a new configuration (`AllowedIPs`).
- No fallback when UDP is blocked; no direct access when the server is down.
- Theme takeover on the gateway, alert e-mails, `install.sh` and the self-test for router gateways are still
  missing (see [implementation status](#status)).
- Two phone paths run in parallel until the old one via the gateway is removed.

### In contrast to … {#comparison}

The table lists only properties that follow from the architecture.

| | Port forwarding on the router | Vendor cloud | Commercial VPN service | Rivet |
|---|---|---|---|---|
| Inbound port at the site | yes | no | depends on the product | no, the gateway only connects outbound |
| Controller visible on the internet | yes | no | no | no |
| Third party in the data path | no | yes (vendor) | yes (provider) | no, only the ForgeIEC server |
| Works without a public IP (CGNAT, mobile) | no | yes | yes | yes |
| Release per phone and port | no | depends on the product | depends on the product | yes, in the portal |
| Who sees decrypted traffic | nobody in between | the vendor | depends on the product | the ForgeIEC server on the phone path via the server (see [isolation](#isolation)) |

</div>
