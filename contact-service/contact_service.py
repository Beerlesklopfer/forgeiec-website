#!/usr/bin/env python3
"""ForgeIEC website contact form backend.

A small, dependency-free HTTP service (Python 3.11+, standard library only)
that sits behind nginx at /api/contact/ and turns validated form submissions
into one plain-text e-mail each.

Endpoints (paths as nginx forwards them, i.e. with the /api/contact prefix):

    GET  /api/contact/token    -> {"ok": true, "token": "..."}
    POST /api/contact/         -> {"ok": true} or {"ok": false, "error": ...}
    GET  /api/contact/health   -> {"ok": true}

Design rules:
  * no state on disk, no cookies, no CORS headers, Cache-Control: no-store;
  * the anti-bot token is a signed timestamp (HMAC-SHA256), nothing is stored;
  * rate limits live in memory only and are lost on restart;
  * the log never contains a name, address, message or client IP: only
    outcome codes, counters and exception class names.

Configuration comes from environment variables (see README.md); in
production systemd reads them from /etc/forgeiec-contact/env.
"""

from __future__ import annotations

import base64
import collections
import hashlib
import hmac
import ipaddress
import json
import logging
import os
import re
import secrets
import signal
import smtplib
import ssl
import sys
import threading
import time
import unicodedata
import urllib.parse
from dataclasses import dataclass, field
from datetime import datetime, timezone
from email.headerregistry import Address
from email.message import EmailMessage
from email.utils import formatdate, make_msgid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

LOG = logging.getLogger("forgeiec-contact")

PATH_PREFIX = "/api/contact"
MAX_BODY = 16 * 1024
MAX_NAME = 100
MAX_EMAIL = 254
MAX_LOCAL_PART = 64
MIN_MESSAGE = 10
MAX_MESSAGE = 5000
TOKEN_VERSION = "v1"

# Subject types offered by the form: key -> label used in the mail subject.
SUBJECT_TYPES = {
    "pilot": "Pilot request",
    "licence": "Licence",
    "partnership": "Partnership/contributing",
    "job": "Job/collaboration",
    "other": "Other",
}
LANGUAGES = ("de", "en")

_ATEXT = r"[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]"
_LOCAL_RE = re.compile(rf"{_ATEXT}+(?:\.{_ATEXT}+)*")
_LABEL_RE = re.compile(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?")
_TLD_RE = re.compile(r"(?:[A-Za-z]{2,63}|xn--[A-Za-z0-9-]{1,59})")


# --------------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------------

class ConfigError(Exception):
    """Raised when the environment does not describe a usable service."""


def _env_int(env, name, default, minimum=0):
    raw = env.get(name, "").strip()
    if not raw:
        return default
    try:
        value = int(raw)
    except ValueError:
        raise ConfigError(f"{name} must be an integer") from None
    if value < minimum:
        raise ConfigError(f"{name} must be >= {minimum}")
    return value


@dataclass
class Config:
    secret: bytes
    mail_from: str
    mail_to: str = "blacksmith@forgeiec.io"
    host: str = "127.0.0.1"
    port: int = 8724
    trusted_proxies: frozenset = frozenset({"127.0.0.1", "::1"})
    smtp_host: str = "localhost"
    smtp_port: int = 25
    smtp_security: str = "none"      # none | starttls | tls
    smtp_user: str = ""
    smtp_password: str = ""
    smtp_timeout: int = 15
    rate_per_ip: int = 5
    rate_window: int = 3600
    global_per_hour: int = 30
    token_min_age: int = 3
    token_max_age: int = 7200

    @classmethod
    def from_env(cls, env=None) -> "Config":
        env = os.environ if env is None else env
        secret = env.get("CONTACT_SECRET", "")
        if len(secret) < 32:
            raise ConfigError("CONTACT_SECRET must be set (at least 32 characters)")
        mail_from = env.get("CONTACT_MAIL_FROM", "").strip()
        mail_to = env.get("CONTACT_MAIL_TO", "blacksmith@forgeiec.io").strip()
        for name, value in (("CONTACT_MAIL_FROM", mail_from), ("CONTACT_MAIL_TO", mail_to)):
            if not is_valid_email(value):
                raise ConfigError(f"{name} must be a plain e-mail address")
        security = env.get("CONTACT_SMTP_SECURITY", "none").strip().lower() or "none"
        if security not in ("none", "starttls", "tls"):
            raise ConfigError("CONTACT_SMTP_SECURITY must be none, starttls or tls")
        password = env.get("CONTACT_SMTP_PASSWORD", "")
        password_file = env.get("CONTACT_SMTP_PASSWORD_FILE", "").strip()
        if password_file:
            try:
                with open(password_file, encoding="utf-8") as fh:
                    password = fh.read().strip()
            except OSError:
                raise ConfigError("CONTACT_SMTP_PASSWORD_FILE is not readable") from None
        proxies = set()
        for item in env.get("CONTACT_TRUSTED_PROXIES", "127.0.0.1,::1").split(","):
            item = item.strip()
            if not item:
                continue
            try:
                proxies.add(str(ipaddress.ip_address(item)))
            except ValueError:
                raise ConfigError("CONTACT_TRUSTED_PROXIES must list IP addresses") from None
        cfg = cls(
            secret=secret.encode("utf-8"),
            mail_from=mail_from,
            mail_to=mail_to,
            host=env.get("CONTACT_LISTEN_HOST", "127.0.0.1").strip() or "127.0.0.1",
            port=_env_int(env, "CONTACT_PORT", 8724),
            trusted_proxies=frozenset(proxies),
            smtp_host=env.get("CONTACT_SMTP_HOST", "localhost").strip() or "localhost",
            smtp_port=_env_int(env, "CONTACT_SMTP_PORT", 465 if security == "tls" else 25, 1),
            smtp_security=security,
            smtp_user=env.get("CONTACT_SMTP_USER", "").strip(),
            smtp_password=password,
            smtp_timeout=_env_int(env, "CONTACT_SMTP_TIMEOUT", 15, 1),
            rate_per_ip=_env_int(env, "CONTACT_RATE_PER_IP", 5, 1),
            rate_window=_env_int(env, "CONTACT_RATE_WINDOW", 3600, 1),
            global_per_hour=_env_int(env, "CONTACT_GLOBAL_PER_HOUR", 30, 1),
            token_min_age=_env_int(env, "CONTACT_TOKEN_MIN_AGE", 3),
            token_max_age=_env_int(env, "CONTACT_TOKEN_MAX_AGE", 7200, 1),
        )
        if cfg.smtp_user and not cfg.smtp_password:
            raise ConfigError("CONTACT_SMTP_USER is set but no password is configured")
        if cfg.smtp_user and cfg.smtp_security == "none":
            raise ConfigError("SMTP login requires CONTACT_SMTP_SECURITY=starttls or tls")
        if cfg.token_min_age >= cfg.token_max_age:
            raise ConfigError("CONTACT_TOKEN_MIN_AGE must be below CONTACT_TOKEN_MAX_AGE")
        return cfg


# --------------------------------------------------------------------------
# Token: signed timestamp, stateless
# --------------------------------------------------------------------------

def _b64(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def make_token(secret: bytes, now: float | None = None) -> str:
    """Return 'v1.<unix-ts>.<nonce>.<mac>'; the nonce only makes tokens unique."""
    ts = int(time.time() if now is None else now)
    nonce = _b64(secrets.token_bytes(9))
    payload = f"{TOKEN_VERSION}.{ts}.{nonce}"
    mac = _b64(hmac.new(secret, payload.encode("ascii"), hashlib.sha256).digest())
    return f"{payload}.{mac}"


def check_token(token, secret: bytes, min_age: int, max_age: int,
                now: float | None = None) -> str | None:
    """Return None when the token is acceptable, else an error code."""
    if not isinstance(token, str) or len(token) > 200 or not token.isascii():
        return "invalid_token"
    parts = token.split(".")
    if len(parts) != 4 or parts[0] != TOKEN_VERSION or not parts[1].isdigit():
        return "invalid_token"
    payload = ".".join(parts[:3])
    expected = _b64(hmac.new(secret, payload.encode("ascii"), hashlib.sha256).digest())
    if not hmac.compare_digest(expected, parts[3]):
        return "invalid_token"
    age = (time.time() if now is None else now) - int(parts[1])
    if age < min_age:
        return "token_too_fresh"
    if age > max_age:
        return "token_expired"
    return None


# --------------------------------------------------------------------------
# Validation
# --------------------------------------------------------------------------

def is_valid_email(value) -> bool:
    """Strict syntax check: ASCII dot-atom local part, DNS host name with TLD.

    Quoted local parts, IP literals, comments and non-ASCII addresses are
    rejected on purpose; they are legal but almost never used in practice
    and only widen the attack surface of the Reply-To header.
    """
    if not isinstance(value, str) or not value or len(value) > MAX_EMAIL:
        return False
    if not value.isascii() or value.count("@") != 1:
        return False
    local, domain = value.split("@")
    if not local or len(local) > MAX_LOCAL_PART or not _LOCAL_RE.fullmatch(local):
        return False
    if len(domain) > 253:
        return False
    labels = domain.split(".")
    if len(labels) < 2:
        return False
    if not all(_LABEL_RE.fullmatch(label) for label in labels):
        return False
    return bool(_TLD_RE.fullmatch(labels[-1]))


def has_line_breaking_or_control(value: str, allow_newlines: bool = False) -> bool:
    """True if value holds control characters (Cc) or Unicode line separators.

    Single-line fields go into mail headers, so any CR, LF or other control
    character is refused outright (header injection). Multi-line fields may
    contain LF, CR and TAB only.
    """
    allowed = {"\n", "\r", "\t"} if allow_newlines else set()
    for ch in value:
        if ch in allowed:
            continue
        cat = unicodedata.category(ch)
        if cat in ("Cc", "Zl", "Zp", "Cs"):
            return True
    return False


def _as_bool(value) -> bool:
    if value is True:
        return True
    if isinstance(value, str):
        return value.strip().lower() in ("1", "true", "on", "yes")
    return False


@dataclass
class Submission:
    name: str
    email: str
    subject_type: str
    message: str
    lang: str


@dataclass
class ValidationResult:
    submission: Submission | None = None
    fields: dict = field(default_factory=dict)   # field -> error code
    error: str | None = None                     # request-level error code


def validate(data: dict, cfg: Config, now: float | None = None) -> ValidationResult:
    """Validate a decoded submission. Field errors are collected together."""
    res = ValidationResult()

    def text(key):
        value = data.get(key, "")
        if value is None:
            return ""
        if not isinstance(value, str):
            res.fields[key] = "invalid"
            return ""
        return value

    name = text("name").strip()
    email = text("email").strip()
    subject_type = text("subject-type").strip()
    message = text("message").replace("\r\n", "\n").replace("\r", "\n").strip()
    lang = text("lang").strip().lower()
    website = data.get("website", "")

    if "name" not in res.fields:
        if not name:
            res.fields["name"] = "required"
        elif has_line_breaking_or_control(name):
            res.fields["name"] = "control_chars"
        elif len(name) > MAX_NAME:
            res.fields["name"] = "too_long"

    if "email" not in res.fields:
        if not email:
            res.fields["email"] = "required"
        elif has_line_breaking_or_control(email):
            res.fields["email"] = "control_chars"
        elif len(email) > MAX_EMAIL:
            res.fields["email"] = "too_long"
        elif not is_valid_email(email):
            res.fields["email"] = "invalid"

    if "subject-type" not in res.fields:
        if not subject_type:
            res.fields["subject-type"] = "required"
        elif subject_type not in SUBJECT_TYPES:
            res.fields["subject-type"] = "invalid"

    if "message" not in res.fields:
        if not message:
            res.fields["message"] = "required"
        elif has_line_breaking_or_control(message, allow_newlines=True):
            res.fields["message"] = "control_chars"
        elif len(message) < MIN_MESSAGE:
            res.fields["message"] = "too_short"
        elif len(message) > MAX_MESSAGE:
            res.fields["message"] = "too_long"

    if not _as_bool(data.get("consent")):
        res.fields["consent"] = "required"

    if lang not in LANGUAGES:
        lang = "de"

    # Honeypot: a filled 'website' field marks a bot. Reported separately so
    # the handler can answer with a quiet success and send nothing.
    if website not in ("", None):
        res.error = "honeypot"
        return res

    token_error = check_token(data.get("token"), cfg.secret,
                              cfg.token_min_age, cfg.token_max_age, now)
    if token_error:
        res.error = token_error
        return res

    if res.fields:
        res.error = "invalid_fields"
        return res

    res.submission = Submission(name, email, subject_type, message, lang)
    return res


# --------------------------------------------------------------------------
# Rate limiting (sliding window, memory only)
# --------------------------------------------------------------------------

class RateLimiter:
    """Sliding-window counter per key plus one global window."""

    MAX_KEYS = 10000

    def __init__(self, per_key: int, window: int, global_limit: int,
                 global_window: int = 3600, clock=time.monotonic):
        self.per_key = per_key
        self.window = window
        self.global_limit = global_limit
        self.global_window = global_window
        self.clock = clock
        self._keys: dict[str, collections.deque] = {}
        self._global: collections.deque = collections.deque()
        self._lock = threading.Lock()

    @staticmethod
    def _prune(dq, horizon):
        while dq and dq[0] <= horizon:
            dq.popleft()

    def acquire(self, key: str) -> tuple[str | None, int]:
        """Record one event for key. Return (error code or None, retry-after s)."""
        with self._lock:
            now = self.clock()
            self._prune(self._global, now - self.global_window)
            dq = self._keys.get(key)
            if dq is not None:
                self._prune(dq, now - self.window)
                if len(dq) >= self.per_key:
                    return "rate_limited", max(1, int(dq[0] + self.window - now) + 1)
            if len(self._global) >= self.global_limit:
                return "service_busy", max(1, int(self._global[0] + self.global_window - now) + 1)
            if dq is None:
                if len(self._keys) >= self.MAX_KEYS:
                    self._sweep(now)
                dq = self._keys.setdefault(key, collections.deque())
            dq.append(now)
            self._global.append(now)
            return None, 0

    def _sweep(self, now):
        for k in list(self._keys):
            self._prune(self._keys[k], now - self.window)
            if not self._keys[k]:
                del self._keys[k]
        if len(self._keys) >= self.MAX_KEYS:   # still full: drop the oldest half
            for k in sorted(self._keys, key=lambda k: self._keys[k][-1])[: self.MAX_KEYS // 2]:
                del self._keys[k]


# --------------------------------------------------------------------------
# Mail
# --------------------------------------------------------------------------

def build_message(sub: Submission, cfg: Config, now: datetime | None = None) -> EmailMessage:
    now = now or datetime.now(timezone.utc)
    label = SUBJECT_TYPES[sub.subject_type]
    local, domain = sub.email.split("@")
    msg = EmailMessage()
    msg["From"] = cfg.mail_from
    msg["To"] = cfg.mail_to
    msg["Reply-To"] = Address(display_name=sub.name, username=local, domain=domain)
    msg["Subject"] = f"[forgeiec.io] {label}: {sub.name}"
    msg["Date"] = formatdate(now.timestamp(), usegmt=True)
    msg["Message-ID"] = make_msgid(domain=cfg.mail_from.split("@")[1])
    body = (
        "Contact form submission from forgeiec.io\n"
        "\n"
        f"Type:    {label}\n"
        f"Name:    {sub.name}\n"
        f"E-mail:  {sub.email}\n"
        "Consent: given (privacy notice accepted)\n"
        "\n"
        "Message:\n"
        f"{sub.message}\n"
        "\n"
        "-- \n"
        f"Language: {sub.lang} | Received: {now.strftime('%Y-%m-%d %H:%M:%S UTC')}\n"
    )
    msg.set_content(body, charset="utf-8", cte="quoted-printable")
    return msg


def send_mail(msg: EmailMessage, cfg: Config) -> None:
    context = ssl.create_default_context()
    if cfg.smtp_security == "tls":
        smtp = smtplib.SMTP_SSL(cfg.smtp_host, cfg.smtp_port,
                                timeout=cfg.smtp_timeout, context=context)
    else:
        smtp = smtplib.SMTP(cfg.smtp_host, cfg.smtp_port, timeout=cfg.smtp_timeout)
    with smtp:
        smtp.ehlo()
        if cfg.smtp_security == "starttls":
            smtp.starttls(context=context)
            smtp.ehlo()
        if cfg.smtp_user:
            smtp.login(cfg.smtp_user, cfg.smtp_password)
        smtp.send_message(msg, from_addr=cfg.mail_from, to_addrs=[cfg.mail_to])


# --------------------------------------------------------------------------
# Statistics (counters only, never personal data)
# --------------------------------------------------------------------------

class Counters:
    def __init__(self):
        self._c = collections.Counter()
        self._lock = threading.Lock()

    def inc(self, outcome: str) -> int:
        with self._lock:
            self._c[outcome] += 1
            return self._c[outcome]

    def snapshot(self) -> dict:
        with self._lock:
            return dict(self._c)


# --------------------------------------------------------------------------
# HTTP
# --------------------------------------------------------------------------

STATUS = {
    "invalid_fields": 422,
    "invalid_token": 400,
    "token_too_fresh": 400,
    "token_expired": 400,
    "bad_request": 400,
    "length_required": 411,
    "payload_too_large": 413,
    "unsupported_media_type": 415,
    "rate_limited": 429,
    "service_busy": 503,
    "mail_failed": 503,
    "not_found": 404,
    "method_not_allowed": 405,
    "internal": 500,
}


class ContactHandler(BaseHTTPRequestHandler):
    server_version = "forgeiec-contact"
    sys_version = ""
    protocol_version = "HTTP/1.1"
    timeout = 15  # socket timeout per request (slow clients)

    # The default access log would record client IP and path: suppress it.
    def log_message(self, format, *args):  # noqa: A002 (stdlib signature)
        return

    def log_request(self, code="-", size="-"):
        return

    # --- helpers -----------------------------------------------------------

    @property
    def app(self) -> "ContactServer":
        return self.server  # type: ignore[return-value]

    def _send_json(self, status: int, payload: dict, extra: dict | None = None):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        if self.close_connection:
            self.send_header("Connection", "close")
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def _error(self, code: str, extra: dict | None = None, **payload):
        self.app.counters.inc(code)
        LOG.info("outcome=%s", code)
        self._send_json(STATUS.get(code, 400), {"ok": False, "error": code, **payload}, extra)

    def _route(self) -> str | None:
        path = urllib.parse.urlsplit(self.path).path
        if path == PATH_PREFIX or path == PATH_PREFIX + "/":
            return "submit"
        if path == PATH_PREFIX + "/token":
            return "token"
        if path == PATH_PREFIX + "/health":
            return "health"
        return None

    def client_ip(self) -> str:
        peer = self.client_address[0]
        try:
            peer = str(ipaddress.ip_address(peer))
        except ValueError:
            return peer
        if peer in self.app.cfg.trusted_proxies:
            xff = self.headers.get("X-Forwarded-For", "")
            candidate = xff.split(",")[-1].strip() if xff else ""
            try:
                return str(ipaddress.ip_address(candidate))
            except ValueError:
                pass
        return peer

    def _guarded(self, fn):
        try:
            fn()
        except Exception as exc:  # never leak internals to the client or log
            LOG.error("outcome=internal error_class=%s", type(exc).__name__)
            self.close_connection = True
            try:
                self._error("internal")
            except Exception:
                pass

    # --- methods -----------------------------------------------------------

    def do_GET(self):
        self._guarded(self._get)

    def do_POST(self):
        self._guarded(self._post)

    def _not_allowed(self, allow):
        self.close_connection = True
        self._error("method_not_allowed", {"Allow": allow})

    do_PUT = do_DELETE = do_PATCH = do_OPTIONS = do_HEAD = \
        lambda self: self._guarded(lambda: self._other())

    def _other(self):
        route = self._route()
        if route is None:
            self.close_connection = True
            return self._error("not_found")
        self._not_allowed("POST" if route == "submit" else "GET")

    def _get(self):
        route = self._route()
        if route == "token":
            self.app.counters.inc("token")
            return self._send_json(200, {"ok": True, "token": make_token(self.app.cfg.secret)})
        if route == "health":
            return self._send_json(200, {"ok": True})
        if route == "submit":
            return self._not_allowed("POST")
        return self._error("not_found")

    def _read_body(self) -> bytes | None:
        if self.headers.get("Transfer-Encoding"):
            self.close_connection = True
            self._error("length_required")
            return None
        raw_len = self.headers.get("Content-Length")
        if raw_len is None or not raw_len.strip().isdigit():
            self.close_connection = True
            self._error("length_required")
            return None
        length = int(raw_len)
        if length > MAX_BODY:
            self.close_connection = True   # do not read the oversized body
            self._error("payload_too_large")
            return None
        return self.rfile.read(length)

    @staticmethod
    def _decode(ctype: str, raw: bytes) -> dict | None:
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            return None
        if ctype == "application/json":
            try:
                data = json.loads(text)
            except ValueError:
                return None
            return data if isinstance(data, dict) else None
        try:
            pairs = urllib.parse.parse_qsl(text, keep_blank_values=True,
                                           strict_parsing=bool(text), max_num_fields=20)
        except ValueError:
            return None
        data = {}
        for key, value in pairs:
            if key in data:        # duplicate keys are ambiguous: refuse
                return None
            data[key] = value
        return data

    def _post(self):
        route = self._route()
        if route != "submit":
            self.close_connection = True
            if route is None:
                return self._error("not_found")
            return self._not_allowed("GET")
        ctype = self.headers.get("Content-Type", "").split(";")[0].strip().lower()
        if ctype not in ("application/json", "application/x-www-form-urlencoded"):
            self.close_connection = True
            return self._error("unsupported_media_type")
        raw = self._read_body()
        if raw is None:
            return
        data = self._decode(ctype, raw)
        if data is None:
            return self._error("bad_request")

        res = validate(data, self.app.cfg)
        if res.error == "honeypot":
            # Quiet success: a bot should not learn that it was recognised.
            self.app.counters.inc("honeypot")
            LOG.info("outcome=honeypot")
            return self._send_json(200, {"ok": True})
        if res.error == "invalid_fields":
            return self._error("invalid_fields", fields=res.fields)
        if res.error:
            return self._error(res.error)

        limited, retry = self.app.limiter.acquire(self.client_ip())
        if limited:
            return self._error(limited, {"Retry-After": str(retry)})

        try:
            send_mail(build_message(res.submission, self.app.cfg), self.app.cfg)
        except (OSError, smtplib.SMTPException) as exc:
            LOG.warning("outcome=mail_failed error_class=%s", type(exc).__name__)
            self.app.counters.inc("mail_failed")
            return self._send_json(503, {"ok": False, "error": "mail_failed"})
        n = self.app.counters.inc("sent")
        LOG.info("outcome=sent sent_total=%d", n)
        self._send_json(200, {"ok": True})


class ContactServer(ThreadingHTTPServer):
    daemon_threads = False        # let running requests finish on shutdown
    block_on_close = True
    allow_reuse_address = True
    request_queue_size = 32

    def __init__(self, cfg: Config, address=None):
        self.cfg = cfg
        self.limiter = RateLimiter(cfg.rate_per_ip, cfg.rate_window, cfg.global_per_hour)
        self.counters = Counters()
        host = (address or (cfg.host, cfg.port))[0]
        if ":" in host:
            import socket
            self.address_family = socket.AF_INET6
        super().__init__(address or (cfg.host, cfg.port), ContactHandler)


def main(argv=None) -> int:
    logging.basicConfig(stream=sys.stderr, level=logging.INFO,
                        format="%(levelname)s %(message)s")
    try:
        cfg = Config.from_env()
    except ConfigError as exc:
        LOG.error("configuration error: %s", exc)
        return 2
    server = ContactServer(cfg)
    LOG.info("listening on %s:%d", *server.server_address[:2])

    def stop(signum, _frame):
        LOG.info("signal %d received, shutting down", signum)
        # shutdown() blocks until serve_forever returns, so call it elsewhere.
        threading.Thread(target=server.shutdown, daemon=True).start()

    signal.signal(signal.SIGTERM, stop)
    signal.signal(signal.SIGINT, stop)
    try:
        server.serve_forever(poll_interval=0.5)
    finally:
        server.server_close()
        LOG.info("stopped; counters %s", json.dumps(server.counters.snapshot(), sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
