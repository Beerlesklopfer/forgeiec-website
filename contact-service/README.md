# forgeiec-contact — contact form backend

A single Python file (`contact_service.py`, Python 3.11+, standard library
only) that receives the contact form of forgeiec.io and sends each valid
submission as one plain-text e-mail to `blacksmith@forgeiec.io`.

```
browser ──HTTPS──▶ nginx ──/api/contact/──▶ 127.0.0.1:8724 (this service) ──SMTP──▶ localhost:25 (local MTA)
```

- `GET /api/contact/token` returns a signed timestamp (HMAC-SHA256). Nothing
  is stored. A submission is accepted only 3 s to 2 h after the token was
  issued (bots that post at once fail, stale pages fail).
- `POST /api/contact/` accepts `application/json` or
  `application/x-www-form-urlencoded` with `name`, `email`, `subject-type`
  (`pilot`, `licence`, `partnership`, `job`, `other`), `message`, `consent`,
  `website` (honeypot, must be empty), `token` and optional `lang` (`de`/`en`).
- `GET /api/contact/health` returns `{"ok": true}`.

No cookies, no CORS headers (same origin), `Cache-Control: no-store` on every
answer. The log contains only outcome codes, counters and exception class
names — never a name, address, message or client IP.

## Files

| File | Purpose |
|---|---|
| `contact_service.py` | the service |
| `test_contact.py` | unit and end-to-end tests (`python3 -m unittest -v`) |
| `forgeiec-contact.service` | systemd unit (hardened, DynamicUser) |
| `nginx-contact.conf` | nginx rate-limit zone and `location /api/contact/` |
| `env.example` | template for `/etc/forgeiec-contact/env` |
| `DATENSCHUTZ-ABSCHNITT.md` | draft paragraph for the privacy policy (German) |

## Configuration: `/etc/forgeiec-contact/env`

| Variable | Default | Meaning |
|---|---|---|
| `CONTACT_SECRET` | — (required) | HMAC key for the token, ≥ 32 characters |
| `CONTACT_MAIL_FROM` | — (required) | `From:` of the notification mail, e.g. `kontakt@forgeiec.io` |
| `CONTACT_MAIL_TO` | `blacksmith@forgeiec.io` | recipient |
| `CONTACT_LISTEN_HOST` | `127.0.0.1` | listen address (keep loopback) |
| `CONTACT_PORT` | `8724` | listen port; must match `proxy_pass` in nginx |
| `CONTACT_TRUSTED_PROXIES` | `127.0.0.1,::1` | peers whose `X-Forwarded-For` is trusted for the rate limit; empty = never trust |
| `CONTACT_SMTP_HOST` | `localhost` | SMTP server |
| `CONTACT_SMTP_PORT` | `25` (`465` with `tls`) | SMTP port |
| `CONTACT_SMTP_SECURITY` | `none` | `none`, `starttls` or `tls` (implicit TLS) |
| `CONTACT_SMTP_USER` | empty | SMTP login; requires `starttls` or `tls` |
| `CONTACT_SMTP_PASSWORD` | empty | SMTP password |
| `CONTACT_SMTP_PASSWORD_FILE` | empty | read the password from this file instead |
| `CONTACT_SMTP_TIMEOUT` | `15` | SMTP timeout in seconds |
| `CONTACT_RATE_PER_IP` | `5` | accepted submissions per client IP per window |
| `CONTACT_RATE_WINDOW` | `3600` | sliding window in seconds |
| `CONTACT_GLOBAL_PER_HOUR` | `30` | accepted submissions per hour for everybody together |
| `CONTACT_TOKEN_MIN_AGE` | `3` | minimum token age in seconds |
| `CONTACT_TOKEN_MAX_AGE` | `7200` | maximum token age in seconds |

**Default: the local MTA on the web server** — `localhost:25`, no STARTTLS,
no login. With the local MTA only `CONTACT_SECRET` and `CONTACT_MAIL_FROM`
need to be set. The login/STARTTLS variables exist for other setups (an
external relay); with them, add the relay's address to `IPAddressAllow=` in
the unit.

Rate limits are counted in memory only for submissions that passed
validation; a restart resets them. nginx additionally limits all requests to
`/api/contact/` (10/min per address, burst 5).

## Install (once, as root on the web server)

```sh
# 1. code
install -d -m 0755 /opt/forgeiec-contact
install -m 0644 contact_service.py README.md /opt/forgeiec-contact/

# 2. configuration and secret
install -d -m 0700 /etc/forgeiec-contact
install -m 0600 env.example /etc/forgeiec-contact/env
python3 -c "import secrets; print(secrets.token_urlsafe(48))"   # paste as CONTACT_SECRET
$EDITOR /etc/forgeiec-contact/env

# 3. systemd
install -m 0644 forgeiec-contact.service /etc/systemd/system/
systemd-analyze verify /etc/systemd/system/forgeiec-contact.service
systemctl daemon-reload
systemctl enable --now forgeiec-contact
systemctl status forgeiec-contact
journalctl -u forgeiec-contact -n 20

# 4. nginx (see comments in nginx-contact.conf)
#    zone line   -> /etc/nginx/conf.d/forgeiec-contact-zone.conf
#    location    -> into the HTTPS server {} block of forgeiec.io
nginx -t && systemctl reload nginx
```

Changing the secret invalidates tokens already handed out (visitors with the
page open must reload). Changing any variable needs
`systemctl restart forgeiec-contact`.

## Local MTA check list

- [ ] The MTA listens on `localhost:25` and accepts mail from `127.0.0.1`
      without authentication (Postfix: `mynetworks` contains `127.0.0.0/8`,
      `[::1]/128`).
- [ ] It accepts the envelope sender `CONTACT_MAIL_FROM` (no
      `smtpd_sender_login_maps`-style restriction for local submissions) and
      delivers to `blacksmith@forgeiec.io` (locally or relayed).
- [ ] The `From` domain `forgeiec.io` matches the server: the SPF record of
      forgeiec.io allows this server's outgoing IP, and the MTA signs with
      the forgeiec.io DKIM key (otherwise DMARC lets the receiver reject).
- [ ] Delivery test on the server (one of):

```sh
swaks --server localhost:25 --from kontakt@forgeiec.io --to blacksmith@forgeiec.io \
      --header "Subject: forgeiec-contact MTA test" --body "test"

printf 'From: kontakt@forgeiec.io\r\nTo: blacksmith@forgeiec.io\r\nSubject: forgeiec-contact MTA test\r\n\r\ntest\r\n' \
  | curl -sS smtp://localhost:25 --mail-from kontakt@forgeiec.io --mail-rcpt blacksmith@forgeiec.io -T -
```

## Test with curl

```sh
# on the server, directly against the service
curl -s http://127.0.0.1:8724/api/contact/health
curl -s http://127.0.0.1:8724/api/contact/token

# end to end through nginx (sends one real mail!)
TOKEN=$(curl -s https://forgeiec.io/api/contact/token | python3 -c 'import json,sys; print(json.load(sys.stdin)["token"])')
sleep 4
curl -s https://forgeiec.io/api/contact/ -H 'Content-Type: application/json' \
  -d "{\"name\":\"Test\",\"email\":\"test@example.com\",\"subject-type\":\"other\",
       \"message\":\"Test from curl, please ignore.\",\"consent\":true,\"website\":\"\",
       \"lang\":\"de\",\"token\":\"$TOKEN\"}"
# -> {"ok": true}

# validation errors (no mail)
curl -s https://forgeiec.io/api/contact/ -H 'Content-Type: application/json' -d '{"email":"x"}'
# -> {"ok": false, "error": "invalid_token"}
```

Response codes: `200 {"ok": true}`; `422 invalid_fields` (with
`"fields": {"name": "required" | "too_long" | "control_chars" | "invalid", …}`);
`400 invalid_token | token_too_fresh | token_expired | bad_request`;
`411 length_required`; `413 payload_too_large` (> 16 KiB);
`415 unsupported_media_type`; `429 rate_limited` (with `Retry-After`);
`503 service_busy` (global ceiling) or `mail_failed` (SMTP error);
`404`, `405`, `500 internal`. A filled honeypot gets a quiet `200 {"ok": true}`
and no mail.

## Tests

```sh
cd contact-service && python3 -m unittest -v
```

The end-to-end tests start the service and a fake SMTP server on ephemeral
loopback ports; no real mail is sent.

## Roll back

```sh
systemctl disable --now forgeiec-contact
rm /etc/systemd/system/forgeiec-contact.service && systemctl daemon-reload
# remove the location block and the zone file from nginx, then
nginx -t && systemctl reload nginx
rm -r /opt/forgeiec-contact /etc/forgeiec-contact
```

The form then shows its error message with the `mailto:` fallback; for a
clean removal also take the `contact-form` shortcode out of
`content/de/kontakt.md` and `content/en/contact.md`.
