---
title: "Architecture + Security Engineering (for experts)"
summary: "Technical depth — why ForgeIEC's AI layer is industrially viable, not a toy"
---

## Target audience

This page is for **security officers, IT architects, CISOs,
compliance officers + technical leads** evaluating whether
ForgeIEC's AI layer is qualified for industrial use. If you are
looking for pure user manuals, [start here](/help/ai/).

We show concrete architecture decisions, the rationale behind them,
the normative specifications we implement, and honestly also what
is **not yet** implemented.

---

## Formal specification as single source of truth

The AI layer is not emergent code behaviour — it follows an
**explicitly written architecture specification**:

- Document: `documentation/architecture/mcp-platform-v1.md` (in
  the source tree, approx. 2300 LOC)
- Normative level: **RFC-2119** — `MUST` / `SHOULD` / `MAY`
- Reviewable: every change to the spec goes through code review
  like any other change
- Version-tagged: `v1` is the current major version; all completed
  sprints (MCP-1 to MCP-9, MCP-4a, MCP-4b) reference their spec
  sections

This means: the implementation is not "the code is the spec",
but rather "the spec is the requirement, the code is measured
against it".

---

## Protocol conformance: MCP 2025-03-26

ForgeIEC implements the **Model Context Protocol** (Anthropic-
published open protocol for LLM tool integration) in version
`2025-03-26`:

- Transport: **HTTP + SSE** (Server-Sent Events) — no custom
  protocol, no WebSocket sprawl
- Wire format: **JSON-RPC 2.0** — strictly per spec, `id` +
  `method` + `params`/`result`/`error`
- `initialize` → `tools/list` → `tools/call` lifecycle: spec-
  conformant, testable with the official MCP inspector
- `capabilities.tools.listChanged: true` — we signal to the client
  that the tool list can change (editor restart, project switch)
- `notifications/tools/list_changed` is **not yet** emitted
  (backlog) — currently the client must re-list on reconnect

This allows **third-party clients** to connect (e.g. Claude Code,
OpenAI ChatGPT with MCP connector, mcp-inspector) without
ForgeIEC-specific code.

---

## Transport security: TLS + optional mTLS

### TLS 1.3 (always active for remote bind)

- Implementation: **Qt6 QSslSocket** with system OpenSSL (TLS
  1.3 + 1.2 supported)
- Server certificate: RSA-4096, SAN-bound, 10-year validity,
  auto-regenerated on bind address change (RFC 6125 SAN
  validation compatible)
- Cipher suites: system defaults (Debian OpenSSL hardening
  follows distribution policy)
- No self-implemented crypto — everything goes through OpenSSL
  CLI shell-out or the Qt6 SSL stack

### mTLS (mutual TLS, optional for federation)

- Activated as soon as `~/.config/ForgeIEC/mcp/trust/*.pem`
  contains one or more CA certs
- `peerVerifyMode = QueryPeer` — client cert is **requested** but
  not strictly required (falls back to bearer auth), allowing
  gradual roll-out
- Chain validation against the trust store happens in the Qt SSL
  stack
- Self-implemented check of certificate subjects against the
  `peers.toml` list — see next section

---

## Federation roster with replay protection

Where other LLM tool platforms practise "first-connection-trust"
(every cert is accepted on first sight), ForgeIEC enforces
**signed rosters**:

```toml
# peers.toml — signed by the Team-CA
[meta]
sequence_number = 17
signed_ts = "2026-05-12T18:00:00Z"
signed_by = "ForgeIEC-Team-CA"
ca_fingerprint_sha256 = "ba:fc:ef:..."
signature_b64 = "..."

[[peer]]
name = "alice@team"
fingerprint_sha256 = "ab:cd:..."
role = "author"
endpoint = "https://alice-ws.factory:7531"
```

**Properties:**

- **Signature:** Ed25519 (preferred, small + fast) or RSA-PSS-
  SHA256 (interop with hardware tokens). Shelled out via openssl
  CLI, not self-implemented.
- **Replay protection:** monotonic `sequence_number` per file.
  Stored via QSettings, every reload with `seq <= last_seen`
  is **refused**.
- **Canonical payload:** the signature covers the TOML file
  without the `signature_b64` line — line-oriented, reproducible
  with `grep -v '^signature_b64'`.
- **Distribution:** arbitrary — Git, S3, HTTP, USB. The container
  is irrelevant; mathematical verification happens at reception.

**Implemented** in `FMcpPeerRoster::verifySignature` with openssl
shell-out for Ed25519+RSA-PSS verification. Reload via
QFileSystemWatcher with 200 ms debounce. The stale-roster reload
loop bug is fixed — see the FAQ entry on stale SHM, same kind of
defensive mechanism.

---

## Confirmation State Machine — no silent automation

Every writing MCP operation goes through a **Confirmation State
Machine** (Spec §9.5):

1. Tool call arrives
2. Handler decides: is operator approval needed (state-changing,
   destructive, side-effect-bearing)?
3. If yes: tool returns `FORGE_ERR_CONFIRMATION_REQUIRED` with
   pending ID + question + options + context
4. LLM client replies via `editor.confirm(id, choice)`
5. State machine resumes the original tool call with the operator's
   choice

Implementation: `FConfirmationStateMachine` (UUIDv4-keyed, default
5-minute timeout, append-only audit trail).

**Guarantees:**

- **No state-changing tool can run without confirm** — the call
  path goes through the state machine; bypass is only via the
  explicit `force=true` parameter that ONLY the state machine
  itself sets on resume
- **Operator visibility:** every pending confirmation is shown
  in the chat as a visual element, and is queryable via the
  `editor.pending_confirmations` MCP tool
- **Timeout behaviour:** expired confirmations set `choice =
  "timeout"`; the tool resume callback decides what that means
  (typically FORGE_ERR_USER_CANCELED)
- **Audit log:** all confirmations + choices are recorded in
  `~/.config/ForgeIEC/mcp_audit.log` (JSONL), append-only

---

## Three-layer defence against unintended effects

### Layer 1 — Build-time gate

```cmake
option(MCP_OVERRIDE_SECURITIES "Unlock MCP write tools" OFF)
```

Default OFF. Write tools (`project.write.*`, `codegen.deploy`,
`runtime.stop`, `editor.quit`, `oscilloscope_set_channels`) return
`FORGE_ERR_PERMISSION_DENIED` when not set.

**Important:** this is **not a runtime flag**. The check is
preprocessor-conditional — the disabled code path is **not even
present in the binary** at default build. An operator cannot turn
it on via a config file.

### Layer 2 — Runtime State Machine

As above — every write action requires operator approval.

### Layer 3 — Operator visibility

- Chat log shows every tool call as a visible element
- Audit log (JSONL) records everything with timestamp
- Build with MCP_OVERRIDE_SECURITIES shows a **security override
  banner** in the initialize output:

  ```
  !!! SECURITY OVERRIDE ACTIVE !!!
  This build MUST NOT run on a productive PLC.
  ```

  The banner also appears in every `warnings[]` list in write
  responses — tooling can act on it.

---

## Force path: explicitly out of MCP

Variable forcing — manually setting a value independent of the
program logic — is the **most side-effect-laden** operation in
the PLC editor. It can move real hardware (start a motor, open a
valve).

**Decision:** force is explicitly **not** accessible via MCP.
There is **no** `force.set` tool, neither in the default build
nor in the override build.

**Rationale:** an AI agent cannot be held accountable for hardware
side effects of a force setting. That responsibility remains
**explicitly with the operator** who manually sets the GUI force
checkbox. The AI layer can read whether a value is forced
(`monitor.snapshot` returns `forced=true`), but cannot force on
its own.

Defence in depth:

- **Layer 1 (codegen TOML):** force bridge is compiled in only
  when `-DFORCING_ENABLED` is set (development builds)
- **Layer 2 (anvild RPC):** ForceVariable gRPC endpoint checks the
  build mode of the PLC binary
- **Layer 3 (Editor UI):** force checkbox is greyed out when the
  PLC build does not support forcing
- **Layer 4 (MCP):** no tool for force; Phase-3 perhaps a
  `force.*` family behind a double state-machine gate

---

## Human identification — Memorable ID + Randomart

Instead of comparing 64-char hex fingerprints (not practical),
ForgeIEC provides **two deterministically derivable
visualisations** of the same fingerprint:

### Memorable ID (BIP-39 wordlist)

- 44 bits from the SHA-256 fingerprint
- 4 indices of 11 bits each
- Wordlist: canonical **BIP-39 English** (2048 words, deduplicated
  by first 4 letters, pronounceable)
- Format: `word-word-word-word`
- On a bit flip in the first 44 bits: **all 4 words change**
- Verbally verifiable ("Read me your Memorable ID over the phone")

### Randomart (OpenSSH drunken bishop)

- Algorithm: identical to `ssh-keygen -lv -E sha256`
- 17×9 grid, bishop walk by 2-bit move per fingerprint byte
- Augmentation string `" .o+=*BOX@%&#/^SE"` maps counter to
  characters
- Start and end markers (S/E) at the bishop path endpoints
- Visually distinctive: a different cert **looks different**;
  human pattern recognition picks up "their" peer

Both implemented in `FMcpFingerprintArt` (two static methods,
pure, deterministic, thread-safe, no heap allocation for the
wordlist).

Surfaced in:

- `server_info.trust_store_cas[]` — per trust-store CA cert
- `team.list_peers` — per peer
- `team.request_cert` — for the freshly issued cert
- Peer-confirm dialog (UI implementation comes with MCP-5)

---

## Caretaker model — cert lifecycle

Spec §7.4 defines:

- **Caretaker role:** one workstation in the team holds the Team-
  CA private key and issues member certs
- Activated via QSettings `mcp/caretaker_enabled` PLUS a
  confirmation modal containing the literal phrase **"I accept
  Team-CA responsibility"** PLUS `MCP_OVERRIDE_SECURITIES=ON`
- Data: `~/.config/ForgeIEC/mcp/ca-team/{ca.key, ca.crt}` (RSA-
  4096, 10 years, CA:TRUE basicConstraint, keyCertSign+cRLSign+
  digitalSignature keyUsage)
- Operations: `team.request_cert` (sign CSR), `team.revoke_peer`
  (revoke + re-sign roster), `team.export_setup` (onboarding
  bundle)
- **Every** operation goes through the State Machine — no
  automatic renewal, no silent issuance
- Multi-Caretaker setup possible (HA) — conflict resolution via
  monotonic sequence_number in the roster

Implementation status 2026-05:

- `FMcpCaretaker` class + `team.request_cert` tool: **done**
- `team.list_peers`: **done**
- `team.revoke_peer`: **stub** (revoked.toml mutation +
  re-signing in backlog)
- `team.rotate_cert`, `team.export_setup`: **backlog**
- Caretaker toggle UI in Preferences: **backlog**

---

## Implementation language + memory safety

ForgeIEC editor is **C++17 + Qt6**. The AI layer (`FMcpServer`,
`FMcpCaretaker`, `FMcpTrustStore`, `FMcpPeerRoster`,
`FMcpFingerprintArt`) uses throughout:

- **RAII** for lifetime management (QObject parent chain)
- **PIMPL** where opaque types are more practical
- **No raw pointers** across class boundaries — `QPointer`,
  `unique_ptr`, `shared_ptr` depending on ownership semantics
- **Implicit-shared QObjects** (`QSslCertificate`, `QString`,
  `QByteArray`) — safe for cross-thread snapshots
- **No global mutable state** — every module is object-owned

The runtime server (`anvild`) is **Rust + Tokio + tonic**.
Memory-safe by borrow checker, async runtime for concurrency. The
gRPC layer between editor and anvild is proto-specified.

iceoryx2 (shared-memory IPC) is **Rust + C-FFI**. We use it
behind our own ABI probe (`anvil-shared@50cb29f`) that detects
type-hash drift before connect — three defence layers against
mismatched versions in production.

---

## Test coverage + reproducibility

- **117+ automated tests** cover the IEC 61131-3 language, all
  132 standard library blocks, the multi-task threading system,
  the persistence path, the force path
- **Test data committed** in the repo (`tests/data/`),
  reproducible
- **Jitter tests** with physical measurement against baseline
- **Codegen** is deterministic — the same `.forge` project
  produces byte-identical `POUS.c` outputs (matiec)
- **Audit log** for LLM activity is append-only JSONL — no entry
  is ever removed, every entry has a timestamp + tool name +
  args + confirm choice

---

## What is honestly not yet there

We are transparent about what is missing:

- **`team.revoke_peer`** is a stub (revoked.toml mutation +
  re-signing follows)
- **`team.rotate_cert` + `team.export_setup`**: backlog
- **OCSP / CRL handling:** not yet implemented (revocation
  currently via signed roster, not via standard PKI path)
- **Memorable-ID typing confirmation** (Spec §7.4.2 specifies
  "operator MUST type peer's Memorable ID to confirm"): today
  still yes/cancel
- **`notifications/tools/list_changed`** SSE: not yet emitted
- **Hardware token (PKCS#11 / FIDO2)** for the Team-CA key:
  roadmap, today a file on disk with 600 permissions
- **Force tools family** (`force.*`): Phase-3 backlog
- **Bulk mode + extended permissions** for >10 tool-turn
  operations (Spec MCP-10): backlog

These items are listed in the internal sprint board
(`project_open_backlog.md`) with priorities.

---

## Standards + cross-references

What we implement and what we lean on:

| Standard | Use |
|---|---|
| IEC 61131-3 (ST/IL/FBD/LD/SFC) | Programming language + compile path via matiec |
| PLCopen XML | Project file format |
| RFC 6125 (SAN validation) | TLS server cert |
| Ed25519 (RFC 8032) | Roster signature (preferred) |
| RSA-PSS (RFC 8017) | Roster signature (HW token interop) |
| BIP-39 (Bitcoin) | Wordlist for Memorable ID |
| SSH ssh-keygen | Randomart algorithm |
| MCP 2025-03-26 (Anthropic) | Protocol lifecycle |
| JSON-RPC 2.0 | Wire format |
| RFC 2119 | Spec normative language |
| TOML 1.0 | Configuration files |

---

## License

ForgeIEC + all subprojects (anvild, bellowsd, tongs-modbustcp, …):
**AGPL-3.0-or-later**. Source repository inspectable; build
reproducibility via Debian CPack + signed APT repository.

---

## Contact for security review

For questions, audit requests, or vulnerability reports:
blacksmith@forgeiec.io

We prefer responsible disclosure — please give us a reasonable
window to fix issues before publishing.

---

## Next

- [Security model (user view)](/help/ai/security/)
- [Team mode + trust](/help/ai/team/)
- [Back to the AI overview](/help/ai/)
