"""Tests for contact_service.py (unittest only, no network beyond loopback).

Run from this directory:  python3 -m unittest -v
"""

import email
import email.policy
import http.client
import json
import socketserver
import threading
import time
import unittest
import urllib.parse

import contact_service as cs

SECRET = "s" * 48
ENV = {
    "CONTACT_SECRET": SECRET,
    "CONTACT_MAIL_FROM": "kontakt@forgeiec.io",
    "CONTACT_MAIL_TO": "blacksmith@forgeiec.io",
}


def make_cfg(**overrides):
    env = dict(ENV)
    env.update(overrides)
    return cs.Config.from_env(env)


def old_token(secret=SECRET, age=10):
    return cs.make_token(secret.encode(), time.time() - age)


def valid_data(**overrides):
    data = {
        "name": "Erika Mustermann",
        "email": "erika@example.com",
        "subject-type": "pilot",
        "message": "Wir möchten ForgeIEC in einem Pilotprojekt testen.",
        "consent": True,
        "website": "",
        "lang": "de",
        "token": old_token(),
    }
    data.update(overrides)
    return data


# --------------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------------

class ConfigTests(unittest.TestCase):
    def test_defaults_local_mta(self):
        cfg = make_cfg()
        self.assertEqual((cfg.smtp_host, cfg.smtp_port, cfg.smtp_security),
                         ("localhost", 25, "none"))
        self.assertEqual(cfg.smtp_user, "")
        self.assertEqual(cfg.host, "127.0.0.1")

    def test_missing_or_short_secret(self):
        for secret in ("", "short"):
            with self.assertRaises(cs.ConfigError):
                make_cfg(CONTACT_SECRET=secret)

    def test_bad_from_address(self):
        with self.assertRaises(cs.ConfigError):
            make_cfg(CONTACT_MAIL_FROM="Kontakt <kontakt@forgeiec.io>")

    def test_login_requires_tls(self):
        with self.assertRaises(cs.ConfigError):
            make_cfg(CONTACT_SMTP_USER="u", CONTACT_SMTP_PASSWORD="p")
        cfg = make_cfg(CONTACT_SMTP_USER="u", CONTACT_SMTP_PASSWORD="p",
                       CONTACT_SMTP_SECURITY="starttls", CONTACT_SMTP_PORT="587")
        self.assertEqual(cfg.smtp_port, 587)

    def test_bad_trusted_proxy(self):
        with self.assertRaises(cs.ConfigError):
            make_cfg(CONTACT_TRUSTED_PROXIES="localhost")


# --------------------------------------------------------------------------
# Token
# --------------------------------------------------------------------------

class TokenTests(unittest.TestCase):
    key = SECRET.encode()

    def check(self, token, now=None):
        return cs.check_token(token, self.key, 3, 7200, now)

    def test_valid(self):
        t = cs.make_token(self.key, 1000)
        self.assertIsNone(self.check(t, now=1003))
        self.assertIsNone(self.check(t, now=1000 + 7200))

    def test_too_fresh(self):
        t = cs.make_token(self.key, 1000)
        self.assertEqual(self.check(t, now=1000), "token_too_fresh")
        self.assertEqual(self.check(t, now=1002.9), "token_too_fresh")

    def test_too_old(self):
        t = cs.make_token(self.key, 1000)
        self.assertEqual(self.check(t, now=1000 + 7201), "token_expired")

    def test_tampered_timestamp(self):
        t = cs.make_token(self.key, 1000)
        parts = t.split(".")
        parts[1] = "900"
        self.assertEqual(self.check(".".join(parts), now=1010), "invalid_token")

    def test_tampered_mac(self):
        t = cs.make_token(self.key, 1000)
        flipped = t[:-1] + ("A" if t[-1] != "A" else "B")
        self.assertEqual(self.check(flipped, now=1010), "invalid_token")

    def test_wrong_secret(self):
        t = cs.make_token(b"x" * 48, 1000)
        self.assertEqual(self.check(t, now=1010), "invalid_token")

    def test_garbage(self):
        for t in (None, "", 123, "v1.abc.def.ghi", "v2.1.a.b", "a" * 500, "v1.1.ä.b"):
            self.assertEqual(self.check(t, now=1010), "invalid_token", repr(t))

    def test_tokens_unique(self):
        self.assertNotEqual(cs.make_token(self.key, 5), cs.make_token(self.key, 5))


# --------------------------------------------------------------------------
# Validation
# --------------------------------------------------------------------------

class EmailSyntaxTests(unittest.TestCase):
    def test_valid(self):
        for a in ("a@b.de", "first.last+tag@sub.example.co.uk", "x_y-z@xn--bcher-kva.example",
                  "o'brien@example.com", "a@xn--p1ai.xn--p1ai"):
            self.assertTrue(cs.is_valid_email(a), a)

    def test_invalid(self):
        for a in ("", "plain", "a@b", "a@@b.de", "a@b@c.de", ".a@b.de", "a.@b.de",
                  "a..b@c.de", "a@-b.de", "a@b-.de", "a@b..de", "a@b.d", "a@b.123",
                  '"q"@b.de', "a@[127.0.0.1]", "jörg@b.de", "a@bücher.de", "a b@c.de",
                  "a@b.de ", "<a@b.de>", "A <a@b.de>", "a@b.de,c@d.de",
                  "x" * 65 + "@b.de", "a@" + "b" * 64 + ".de",
                  "a@" + ".".join(["b" * 60] * 5) + ".de"):
            self.assertFalse(cs.is_valid_email(a), a)

    def test_max_length(self):
        local = "a" * 64
        domain = ".".join(["b" * 61] * 3) + ".de"     # 189 chars
        addr = f"{local}@{domain}"
        self.assertLessEqual(len(addr), 254)
        self.assertTrue(cs.is_valid_email(addr))
        self.assertFalse(cs.is_valid_email(addr + "x" * (255 - len(addr))))


class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.cfg = make_cfg()

    def run_v(self, **overrides):
        return cs.validate(valid_data(**overrides), self.cfg)

    def assertField(self, res, field, code):
        self.assertEqual(res.error, "invalid_fields")
        self.assertEqual(res.fields.get(field), code, res.fields)

    def test_valid(self):
        res = self.run_v()
        self.assertIsNone(res.error)
        self.assertEqual(res.submission.subject_type, "pilot")
        self.assertEqual(res.submission.lang, "de")

    def test_name_limits(self):
        self.assertIsNone(self.run_v(name="N" * 100).error)
        self.assertField(self.run_v(name="N" * 101), "name", "too_long")
        self.assertField(self.run_v(name="   "), "name", "required")
        self.assertField(self.run_v(name=""), "name", "required")

    def test_name_trimmed(self):
        self.assertEqual(self.run_v(name="  Max  ").submission.name, "Max")

    def test_email_rules(self):
        self.assertField(self.run_v(email=""), "email", "required")
        self.assertField(self.run_v(email="nope"), "email", "invalid")
        self.assertField(self.run_v(email="a@" + "b" * 250 + ".de"), "email", "too_long")

    def test_subject_type(self):
        for key in cs.SUBJECT_TYPES:
            self.assertIsNone(self.run_v(**{"subject-type": key}).error)
        self.assertField(self.run_v(**{"subject-type": "spam"}), "subject-type", "invalid")
        self.assertField(self.run_v(**{"subject-type": ""}), "subject-type", "required")

    def test_message_limits(self):
        self.assertIsNone(self.run_v(message="x" * 10).error)
        self.assertIsNone(self.run_v(message="x" * 5000).error)
        self.assertField(self.run_v(message="x" * 9), "message", "too_short")
        self.assertField(self.run_v(message="   x" * 2 + "   "), "message", "too_short")
        self.assertField(self.run_v(message="x" * 5001), "message", "too_long")
        self.assertField(self.run_v(message=""), "message", "required")

    def test_message_multiline_allowed(self):
        res = self.run_v(message="Zeile eins\r\nZeile zwei\n\tEingerückt")
        self.assertIsNone(res.error)
        self.assertEqual(res.submission.message, "Zeile eins\nZeile zwei\n\tEingerückt")

    def test_message_control_chars(self):
        self.assertField(self.run_v(message="Hallo Welt\x00!"), "message", "control_chars")
        self.assertField(self.run_v(message="Hallo Welt\x1b[31m"), "message", "control_chars")

    def test_consent(self):
        for value in (True, "on", "true", "1", "yes"):
            self.assertIsNone(self.run_v(consent=value).error, value)
        for value in (False, "", "off", "0", None, 1, [], "nein"):
            self.assertField(self.run_v(consent=value), "consent", "required")
        data = valid_data()
        del data["consent"]
        self.assertEqual(cs.validate(data, self.cfg).fields.get("consent"), "required")

    def test_non_string_fields(self):
        self.assertField(self.run_v(name=["a"]), "name", "invalid")
        self.assertField(self.run_v(message={"x": 1}), "message", "invalid")

    def test_all_field_errors_together(self):
        res = self.run_v(name="", email="x", message="kurz", consent=False)
        self.assertEqual(set(res.fields), {"name", "email", "message", "consent"})

    def test_lang_whitelist(self):
        self.assertEqual(self.run_v(lang="en").submission.lang, "en")
        self.assertEqual(self.run_v(lang="xx\r\n").submission.lang, "de")

    def test_honeypot(self):
        res = self.run_v(website="http://spam.example")
        self.assertEqual(res.error, "honeypot")
        self.assertIsNone(res.submission)
        # honeypot wins even over other errors
        self.assertEqual(self.run_v(website="x", name="").error, "honeypot")

    def test_token_errors_in_validation(self):
        self.assertEqual(self.run_v(token=cs.make_token(SECRET.encode())).error, "token_too_fresh")
        self.assertEqual(self.run_v(token=old_token(age=7300)).error, "token_expired")
        self.assertEqual(self.run_v(token=old_token("w" * 48)).error, "invalid_token")
        self.assertEqual(self.run_v(token="").error, "invalid_token")


class HeaderInjectionTests(unittest.TestCase):
    def setUp(self):
        self.cfg = make_cfg()

    attacks = [
        "Max\r\nBcc: victim@example.com",
        "Max\nBcc: victim@example.com",
        "Max\rBcc: victim@example.com",
        "Max\u2028Bcc: victim@example.com",
        "Max\u2029x",
        "Max\x85Bcc: x@example.com",
        "Max\x00",
        "Max\tTab",
        "Max\x0bVT",
    ]

    def test_name(self):
        for value in self.attacks:
            res = cs.validate(valid_data(name=value), self.cfg)
            self.assertEqual(res.fields.get("name"), "control_chars", repr(value))

    def test_email(self):
        for suffix in ("\r\nBcc: v@example.com", "\nTo: v@example.com", "\u2028"):
            res = cs.validate(valid_data(email="a@example.com" + suffix), self.cfg)
            self.assertEqual(res.fields.get("email"), "control_chars", repr(suffix))

    def test_subject_type(self):
        res = cs.validate(valid_data(**{"subject-type": "pilot\r\nBcc: v@example.com"}), self.cfg)
        self.assertEqual(res.fields.get("subject-type"), "invalid")

    def test_message_cannot_add_headers(self):
        sub = cs.validate(valid_data(message="Text\r\n\r\nBcc: v@example.com\r\n"),
                          self.cfg).submission
        msg = cs.build_message(sub, self.cfg)
        parsed = email.message_from_bytes(msg.as_bytes(policy=email.policy.SMTP),
                                          policy=email.policy.default)
        self.assertIsNone(parsed["Bcc"])

    def test_display_name_specials_are_quoted(self):
        sub = cs.validate(valid_data(name='Evil, "Bob" <x@evil.example>;'), self.cfg).submission
        msg = cs.build_message(sub, self.cfg)
        parsed = email.message_from_bytes(msg.as_bytes(policy=email.policy.SMTP),
                                          policy=email.policy.default)
        addrs = parsed["Reply-To"].addresses
        self.assertEqual(len(addrs), 1)
        self.assertEqual(addrs[0].addr_spec, "erika@example.com")


# --------------------------------------------------------------------------
# Rate limiter
# --------------------------------------------------------------------------

class FakeClock:
    def __init__(self):
        self.t = 1000.0

    def __call__(self):
        return self.t


class RateLimitTests(unittest.TestCase):
    def test_per_ip_sliding_window(self):
        clock = FakeClock()
        rl = cs.RateLimiter(5, 3600, 100, clock=clock)
        for i in range(5):
            self.assertEqual(rl.acquire("1.2.3.4"), (None, 0))
            clock.t += 60
        err, retry = rl.acquire("1.2.3.4")
        self.assertEqual(err, "rate_limited")
        self.assertGreater(retry, 0)
        self.assertEqual(rl.acquire("5.6.7.8"), (None, 0))   # other IP unaffected
        clock.t = 1000.0 + 3600 + 1                          # first event slid out
        self.assertEqual(rl.acquire("1.2.3.4"), (None, 0))
        self.assertEqual(rl.acquire("1.2.3.4")[0], "rate_limited")

    def test_global_ceiling(self):
        clock = FakeClock()
        rl = cs.RateLimiter(5, 3600, 3, clock=clock)
        for ip in ("a", "b", "c"):
            self.assertIsNone(rl.acquire(ip)[0])
        self.assertEqual(rl.acquire("d")[0], "service_busy")
        clock.t += 3601
        self.assertIsNone(rl.acquire("d")[0])

    def test_rejected_do_not_count(self):
        clock = FakeClock()
        rl = cs.RateLimiter(1, 3600, 100, clock=clock)
        rl.acquire("a")
        for _ in range(10):
            rl.acquire("a")
        self.assertEqual(len(rl._global), 1)

    def test_key_table_bounded(self):
        clock = FakeClock()
        rl = cs.RateLimiter(5, 3600, 10 ** 6, clock=clock)
        rl.MAX_KEYS = 100
        for i in range(250):
            rl.acquire(f"ip{i}")
        self.assertLessEqual(len(rl._keys), 100)


# --------------------------------------------------------------------------
# End-to-end: real HTTP server + fake SMTP server on ephemeral ports
# --------------------------------------------------------------------------

class FakeSMTPHandler(socketserver.StreamRequestHandler):
    """Just enough ESMTP for smtplib.send_message (no 8BITMIME, no SMTPUTF8)."""

    def reply(self, line):
        self.wfile.write(line.encode("ascii") + b"\r\n")

    def handle(self):
        self.reply("220 fake.test ESMTP")
        envelope = {"from": None, "to": []}
        while True:
            line = self.rfile.readline()
            if not line:
                return
            cmd = line.decode("ascii", "replace").strip()
            verb = cmd[:4].upper()
            if verb in ("EHLO", "HELO"):
                self.reply("250-fake.test")
                self.reply("250 SIZE 100000")
            elif verb == "MAIL":
                envelope["from"] = cmd
                self.reply("250 OK")
            elif verb == "RCPT":
                envelope["to"].append(cmd)
                self.reply("250 OK")
            elif verb == "DATA":
                self.reply("354 go ahead")
                chunks = []
                while True:
                    data_line = self.rfile.readline()
                    if data_line in (b".\r\n", b""):
                        break
                    if data_line.startswith(b".."):
                        data_line = data_line[1:]
                    chunks.append(data_line)
                self.server.messages.append((dict(envelope), b"".join(chunks)))
                self.reply("250 queued")
            elif verb == "RSET":
                envelope = {"from": None, "to": []}
                self.reply("250 OK")
            elif verb == "QUIT":
                self.reply("221 bye")
                return
            else:
                self.reply("502 not implemented")


class FakeSMTPServer(socketserver.ThreadingTCPServer):
    daemon_threads = True
    allow_reuse_address = True

    def __init__(self):
        super().__init__(("127.0.0.1", 0), FakeSMTPHandler)
        self.messages = []


class EndToEndTests(unittest.TestCase):
    def setUp(self):
        self.smtp = FakeSMTPServer()
        threading.Thread(target=self.smtp.serve_forever, args=(0.05,), daemon=True).start()
        self.cfg = make_cfg(CONTACT_SMTP_HOST="127.0.0.1",
                            CONTACT_SMTP_PORT=str(self.smtp.server_address[1]),
                            CONTACT_PORT="0", CONTACT_RATE_PER_IP="5",
                            CONTACT_GLOBAL_PER_HOUR="8")
        self.server = cs.ContactServer(self.cfg, ("127.0.0.1", 0))
        self.port = self.server.server_address[1]
        self.thread = threading.Thread(target=self.server.serve_forever, args=(0.05,), daemon=True)
        self.thread.start()

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.smtp.shutdown()
        self.smtp.server_close()

    def request(self, method, path, body=None, headers=None):
        conn = http.client.HTTPConnection("127.0.0.1", self.port, timeout=10)
        try:
            conn.request(method, path, body=body, headers=headers or {})
            resp = conn.getresponse()
            raw = resp.read()
            return resp, (json.loads(raw) if raw else None)
        finally:
            conn.close()

    def post_json(self, data, headers=None):
        h = {"Content-Type": "application/json"}
        h.update(headers or {})
        return self.request("POST", "/api/contact/", json.dumps(data).encode(), h)

    def test_token_endpoint(self):
        resp, body = self.request("GET", "/api/contact/token")
        self.assertEqual(resp.status, 200)
        self.assertTrue(body["ok"])
        self.assertEqual(resp.getheader("Cache-Control"), "no-store")
        self.assertIsNone(resp.getheader("Set-Cookie"))
        self.assertIsNone(resp.getheader("Access-Control-Allow-Origin"))
        self.assertEqual(cs.check_token(body["token"], SECRET.encode(), 3, 7200), "token_too_fresh")
        self.assertIsNone(cs.check_token(body["token"], SECRET.encode(), 3, 7200,
                                         now=time.time() + 5))

    def test_full_submission_json(self):
        data = valid_data(name="Jörg Bärenfänger", lang="en",
                          message="Grüße aus Köln — wir hätten gern einen Pilot.\nZweite Zeile ß.")
        resp, body = self.post_json(data)
        self.assertEqual((resp.status, body), (200, {"ok": True}))
        self.assertEqual(resp.getheader("Cache-Control"), "no-store")
        self.assertIsNone(resp.getheader("Set-Cookie"))
        self.assertIsNone(resp.getheader("Access-Control-Allow-Origin"))
        self.assertEqual(len(self.smtp.messages), 1)
        envelope, raw = self.smtp.messages[0]
        self.assertIn("<kontakt@forgeiec.io>", envelope["from"])
        self.assertEqual([r.upper() for r in envelope["to"]], ["RCPT TO:<BLACKSMITH@FORGEIEC.IO>"])
        raw.decode("ascii")   # the wire format must be pure 7-bit ASCII
        msg = email.message_from_bytes(raw, policy=email.policy.default)
        self.assertEqual(set(k.lower() for k in msg.keys()), {
            "from", "to", "reply-to", "subject", "date", "message-id",
            "content-type", "content-transfer-encoding", "mime-version"})
        self.assertEqual(msg["From"], "kontakt@forgeiec.io")
        self.assertEqual(msg["To"], "blacksmith@forgeiec.io")
        reply_to = msg["Reply-To"].addresses
        self.assertEqual(len(reply_to), 1)
        self.assertEqual(reply_to[0].display_name, "Jörg Bärenfänger")
        self.assertEqual(reply_to[0].addr_spec, "erika@example.com")
        self.assertEqual(str(msg["Subject"]), "[forgeiec.io] Pilot request: Jörg Bärenfänger")
        self.assertEqual(msg.get_content_type(), "text/plain")
        self.assertEqual(msg.get_content_charset(), "utf-8")
        text = msg.get_content().replace("\r\n", "\n")
        self.assertIn("Name:    Jörg Bärenfänger", text)
        self.assertIn("Grüße aus Köln — wir hätten gern einen Pilot.\nZweite Zeile ß.", text)
        self.assertIn("E-mail:  erika@example.com", text)
        self.assertRegex(text, r"Language: en \| Received: \d{4}-\d\d-\d\d \d\d:\d\d:\d\d UTC")

    def test_form_encoded(self):
        data = valid_data(consent="on", **{"subject-type": "licence"})
        body = urllib.parse.urlencode(data).encode()
        resp, out = self.request("POST", "/api/contact/", body,
                                 {"Content-Type": "application/x-www-form-urlencoded"})
        self.assertEqual((resp.status, out), (200, {"ok": True}))
        msg = email.message_from_bytes(self.smtp.messages[0][1], policy=email.policy.default)
        self.assertTrue(str(msg["Subject"]).startswith("[forgeiec.io] Licence: "))

    def test_form_duplicate_keys_rejected(self):
        body = urllib.parse.urlencode(valid_data()) + "&name=Second"
        resp, out = self.request("POST", "/api/contact/", body.encode(),
                                 {"Content-Type": "application/x-www-form-urlencoded"})
        self.assertEqual((resp.status, out["error"]), (400, "bad_request"))
        self.assertEqual(self.smtp.messages, [])

    def test_validation_error_response(self):
        resp, out = self.post_json(valid_data(email="bad", consent=False))
        self.assertEqual(resp.status, 422)
        self.assertEqual(out, {"ok": False, "error": "invalid_fields",
                               "fields": {"email": "invalid", "consent": "required"}})
        self.assertEqual(self.smtp.messages, [])

    def test_token_errors(self):
        cases = [(cs.make_token(SECRET.encode()), "token_too_fresh"),
                 (old_token(age=7300), "token_expired"),
                 (old_token("q" * 48), "invalid_token")]
        for token, code in cases:
            resp, out = self.post_json(valid_data(token=token))
            self.assertEqual((resp.status, out["error"]), (400, code))
        self.assertEqual(self.smtp.messages, [])

    def test_honeypot_quiet_success_without_mail(self):
        resp, out = self.post_json(valid_data(website="https://spam.example"))
        self.assertEqual((resp.status, out), (200, {"ok": True}))
        self.assertEqual(self.smtp.messages, [])

    def test_header_injection_over_http(self):
        resp, out = self.post_json(valid_data(name="X\r\nBcc: victim@example.com"))
        self.assertEqual(resp.status, 422)
        self.assertEqual(out["fields"], {"name": "control_chars"})
        self.assertEqual(self.smtp.messages, [])

    def test_body_size_limit(self):
        data = valid_data(message="x" * 4000, pad="y" * (cs.MAX_BODY))
        resp, out = self.post_json(data)
        self.assertEqual((resp.status, out["error"]), (413, "payload_too_large"))
        # exactly at the limit is accepted (as far as size is concerned)
        base = json.dumps(valid_data(pad="")).encode()
        filler = cs.MAX_BODY - len(base)
        body = json.dumps(valid_data(pad="y" * filler)).encode()
        self.assertEqual(len(body), cs.MAX_BODY)
        resp, out = self.request("POST", "/api/contact/", body,
                                 {"Content-Type": "application/json"})
        self.assertEqual(resp.status, 200)

    def test_missing_length_and_chunked(self):
        conn = http.client.HTTPConnection("127.0.0.1", self.port, timeout=10)
        conn.putrequest("POST", "/api/contact/")
        conn.putheader("Content-Type", "application/json")
        conn.putheader("Transfer-Encoding", "chunked")
        conn.endheaders()
        conn.send(b"2\r\n{}\r\n0\r\n\r\n")
        resp = conn.getresponse()
        self.assertEqual(resp.status, 411)
        conn.close()

    def test_bad_requests(self):
        resp, out = self.request("POST", "/api/contact/", b"{}", {"Content-Type": "text/plain"})
        self.assertEqual((resp.status, out["error"]), (415, "unsupported_media_type"))
        resp, out = self.request("POST", "/api/contact/", b"{nope", {"Content-Type": "application/json"})
        self.assertEqual((resp.status, out["error"]), (400, "bad_request"))
        resp, out = self.request("POST", "/api/contact/", b"[1,2]", {"Content-Type": "application/json"})
        self.assertEqual((resp.status, out["error"]), (400, "bad_request"))
        resp, out = self.request("POST", "/api/contact/", b"\xff\xfe", {"Content-Type": "application/json"})
        self.assertEqual((resp.status, out["error"]), (400, "bad_request"))
        resp, out = self.request("GET", "/api/contact/other")
        self.assertEqual((resp.status, out["error"]), (404, "not_found"))
        resp, out = self.request("GET", "/api/contact/")
        self.assertEqual((resp.status, out["error"]), (405, "method_not_allowed"))
        self.assertEqual(resp.getheader("Allow"), "POST")
        resp, out = self.request("PUT", "/api/contact/", b"", {"Content-Length": "0"})
        self.assertEqual(resp.status, 405)

    def test_rate_limit_per_forwarded_ip(self):
        hdr = {"X-Forwarded-For": "203.0.113.7"}
        for _ in range(5):
            resp, _ = self.post_json(valid_data(), hdr)
            self.assertEqual(resp.status, 200)
        resp, out = self.post_json(valid_data(), hdr)
        self.assertEqual((resp.status, out["error"]), (429, "rate_limited"))
        self.assertTrue(int(resp.getheader("Retry-After")) > 0)
        resp, _ = self.post_json(valid_data(), {"X-Forwarded-For": "198.51.100.1"})
        self.assertEqual(resp.status, 200)
        self.assertEqual(len(self.smtp.messages), 6)

    def test_global_ceiling(self):
        for i in range(8):
            resp, _ = self.post_json(valid_data(), {"X-Forwarded-For": f"203.0.113.{i}"})
            self.assertEqual(resp.status, 200)
        resp, out = self.post_json(valid_data(), {"X-Forwarded-For": "203.0.113.99"})
        self.assertEqual((resp.status, out["error"]), (503, "service_busy"))

    def test_xff_ignored_from_untrusted_peer(self):
        self.server.cfg.trusted_proxies = frozenset({"192.0.2.1"})
        for i in range(5):
            resp, _ = self.post_json(valid_data(), {"X-Forwarded-For": f"203.0.113.{i}"})
            self.assertEqual(resp.status, 200)
        resp, out = self.post_json(valid_data(), {"X-Forwarded-For": "203.0.113.50"})
        self.assertEqual(out["error"], "rate_limited")   # all counted as 127.0.0.1

    def test_mail_failure_does_not_leak(self):
        self.server.cfg.smtp_port = 1    # nothing listens there
        with self.assertLogs("forgeiec-contact", level="WARNING") as logs:
            resp, out = self.post_json(valid_data())
        self.assertEqual(logs.output,
                         ["WARNING:forgeiec-contact:outcome=mail_failed "
                          "error_class=ConnectionRefusedError"])
        self.assertEqual((resp.status, out), (503, {"ok": False, "error": "mail_failed"}))

    def test_log_has_no_personal_data(self):
        with self.assertLogs("forgeiec-contact", level="INFO") as logs:
            self.post_json(valid_data(name="Geheimname", email="geheim@example.com",
                                      message="Geheimer Nachrichtentext"),
                           {"X-Forwarded-For": "203.0.113.42"})
            self.post_json(valid_data(email="kaputt"))
        joined = "\n".join(logs.output)
        for secret in ("Geheim", "geheim@", "kaputt", "203.0.113.42", "127.0.0.1"):
            self.assertNotIn(secret, joined)
        self.assertIn("outcome=sent", joined)
        self.assertIn("outcome=invalid_fields", joined)


if __name__ == "__main__":
    unittest.main()
