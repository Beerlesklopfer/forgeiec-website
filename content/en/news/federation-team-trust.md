---
title: "Federation + team trust: multiple workstations, controllable trust"
date: 2026-05-13
summary: "ForgeIEC now connects multiple workstations into a team — with verifiable identities and a clear role model"
components: [studio]
---

{{< components "studio" >}}

## Why this matters

Industrial automation rarely happens at a single workstation. Team
leads review code. Commissioning engineers diagnose remotely.
Build servers compile overnight. Until now this meant: everyone
had their own editor, manually kept in sync, no real federation.

With the now-completed **federation sprint** ForgeIEC Studio
becomes a **multi-workstation system**:

- Multiple Studios see each other — controlled via trust store
- A **Caretaker** takes central responsibility for "who belongs"
- Identities are **human-verifiable** — four words, a small
  picture, no 64-char hex comparison
- Onboarding + revocation run through a **clear protocol**, not
  through emailed files

That makes ForgeIEC **team-ready** for the first time, without
trading security for convenience.

---

## What you get

### A new colleague joins the team

Instead of distributing certificates by USB stick:

1. The new colleague generates a request in their ForgeIEC Studio.
2. The Caretaker sees the request — **with Memorable ID +
   randomart** of the not-yet-issued cert.
3. The Caretaker verifies visually / verbally ("Read me your four
   words"), confirms in the dialog.
4. Freshly issued cert goes back. The colleague is a Member.

Memorable ID example: `road-trash-smile-deny`. Four English words
from a 2048-word list, derived deterministically from the cert —
a single bit change at the beginning shifts **all four** words
completely.

Randomart example:

```
+----[SHA256]-----+
|        o. ..... |
|       o .o .   .|
|      o  ....   o|
|.    . .+.   o ..|
| + .. ..Soo.. o  |
|. +. . . +.++.   |
| oo   o .oo+..   |
|...= o +o.+      |
|E+*o. +.o=o      |
+-----------------+
```

You learn the **shape** of a colleague's picture after 2–3
connections.

### A colleague leaves / a laptop disappears

The Caretaker revokes the cert. The signed revocation list goes
to all team members. From the next roster pull (default every 5
minutes, on demand sooner) every other Studio refuses the revoked
cert.

### IT keeps the strings in hand

- **peers.toml + revoked.toml** are digitally signed. Distribution
  can use Git, shared drive, USB — bytes only need to arrive
  intact; mathematical verification happens at reception.
- **Replay protection** via monotonic `sequence_number` prevents
  an attacker from replaying an older (un-revoked) version.
- **TLS 1.3 + optional mTLS** on the wire. Cipher suites follow
  distribution hardening defaults.
- **Build-time gate** for write operations: the default APT
  distribution is read-only. Writing requires a deliberate build
  switch.

---

## Security: visible at every step

Every writing action (issue cert, update roster, revoke member)
goes through the **Confirmation State Machine**:

- Tool call returns `FORGE_ERR_CONFIRMATION_REQUIRED` with context
- Operator sees in the chat: what is about to happen, with which
  identity, with which Memorable ID / randomart
- Confirmation via `editor.confirm` — audit log with timestamp +
  choice + args

No silent background issuance. No automatic rotation without an
operator click. Lost cert → just expires, operator notices,
operator decides.

---

## Architecture depth for auditors

If you want to verify this is not just "security as a slogan",
the load-bearing details are at
[Architecture + Security](/help/ai/architecture/):

- Full formal spec with RFC 2119 normative language
- Cross-reference to every source class + file in the source tree
- Standards table: BIP-39, OpenSSH randomart, Ed25519, RSA-PSS,
  RFC 6125, MCP 2025-03-26
- Honest list of **still-open items** (no marketing varnish)

---

## Plus: stale SHM is history

The same release also includes `anvild` auto-cleanup. What used to
slow down occasional commissioning sessions as "variable sticks
despite fresh deploy" is now simply
`sudo systemctl restart anvild` — the daemon cleans up stale
shared-memory segments on startup.

Background + fix documented: [FAQ entry](/help/faq/stuck-variables-shm/).

{{< callout type="note" title="Addendum" >}}
The blanket cleanup at anvild startup has since been removed again:
it tore away the shared segments of **live** peers (bellowsd,
hearth, tongs-*). Cleanup is now done by the Anvil layer,
selectively per dead node; as a user you simply restart the PLC
runtime. Current state in the
[FAQ entry](/help/faq/stuck-variables-shm/).
{{< /callout >}}

---

## Where you use it

| Setup | What you configure |
|---|---|
| **Single workstation** | Nothing. Federation is optional. |
| **Two programmers in an office** | Caretaker on one workstation, Member on the other. Trust store on a shared drive. |
| **Team with build server** | Build server has its own cert, runs headless, calls Studio MCP tools via `curl` from CI. |
| **Multiple sites** | peers.toml distributed via Git, signed, every change pull-anchored. |

---

## Where to read more

- [User: connecting multiple workstations](/help/ai/team/)
- [Architecture + Security](/help/ai/architecture/)
- [MCP for application engineers](/help/mcp/programmers/)
- [MCP for IT + operations](/help/mcp/it/)

Source repositories:
[Forgejo](https://git.forgeiec.io/ForgeIEC/forgeiec-studio).

---

## What comes next

- Caretaker toggle UI in Preferences (instead of QSettings edit +
  modal today)
- `team.rotate_cert` + `team.revoke_peer` fully implemented
- `team.export_setup` as the onboarding bundle generator
- Memorable-ID typing as additional confirmation hardening for
  high-risk operations (Spec §7.4.2)
