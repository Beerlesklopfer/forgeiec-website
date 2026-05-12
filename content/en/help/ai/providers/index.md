---
title: "AI providers — ChatGPT, Claude, local"
summary: "Which AI services work with ForgeIEC and how to set them up"
---

## Which providers work?

The AI assistant in ForgeIEC is **not bound to a single provider**.
You can freely choose:

| Variant | Provider | What it's good for |
|---|---|---|
| **Cloud** | ChatGPT (OpenAI) | Fast, very strong models, data goes to the internet |
| **Cloud** | Claude (Anthropic) | Excellent for long tasks + code review, data goes to the internet |
| **Local** | LM Studio / llama.cpp / Ollama | Data stays in-house, free, slower than cloud |
| **Local** | Self-hosted vLLM / Together-API-compatible | If you run cloud-grade models behind your own firewall |

ForgeIEC Studio automatically detects whether an endpoint speaks
**OpenAI or Anthropic format** — you don't have to configure that.

---

## Connecting to ChatGPT (OpenAI)

**Prerequisite:** an OpenAI account with prepaid credits. The API
is separate from the ChatGPT web subscription — you pay per token
used, not a flat fee.

**Step 1 — Create an API key**

1. Sign in at `https://platform.openai.com/api-keys`.
2. Click `Create new secret key`, give it a name (e.g.
   `ForgeIEC-WS-Joe`).
3. The key starts with `sk-...` and is shown **only once** — copy
   it immediately into a secure place (password manager).

**Step 2 — Enter it in Studio**

In the AI panel, in the profile configuration:

| Field | Value |
|---|---|
| API | `https://api.openai.com/v1` |
| API Key | `sk-...` (your key) |
| Model | e.g. `gpt-4o`, `gpt-4o-mini`, `gpt-5` |

**Step 3 — Test query**

```
Say hello.
```

If everything works, the assistant replies. If you see an HTTP-401
or HTTP-429 message in the output: API key wrong or rate limit
exceeded.

**Cost:** A few cents per request. A typical programming session
costs USD 0.10 - 1.00 depending on the model.

---

## Connecting to Claude (Anthropic)

**Prerequisite:** Anthropic account with console access. As with
OpenAI, the API is separate from the claude.ai web subscription.

**Step 1 — Create an API key**

1. Sign in at `https://console.anthropic.com/settings/keys`.
2. Click `Create Key`, give it a name.
3. The key starts with `sk-ant-...` — copy it to the password
   manager.

**Step 2 — Enter it in Studio**

| Field | Value |
|---|---|
| API | `https://api.anthropic.com` |
| API Key | `sk-ant-...` |
| Model | e.g. `claude-opus-4-7`, `claude-sonnet-4-6`, `claude-haiku-4-5-20251001` |

ForgeIEC Studio automatically detects from the hostname
`api.anthropic.com` that Anthropic format applies — no extra
setting needed.

**Step 3 — Test query**

Same as above — say hello, see the reply.

**Cost:** Similar to OpenAI; Claude Opus is slightly pricier but
often finishes long tasks faster.

---

## Local AI (LM Studio, llama.cpp, Ollama)

**When does it make sense?**

- Data must not leave the network
- No per-request API costs
- You have a powerful GPU (at least 8 GB VRAM for smaller models,
  24+ GB for 30B models)
- You want to try without setting up an account

**Variant A — LM Studio** (easiest)

1. Download + install LM Studio from `https://lmstudio.ai`.
2. Pick a model in the LM Studio browser, e.g.
   `qwen3-coder-30b-a3b-instruct` for coding tasks.
3. In the `Developer` tab, start a local server — default at
   `http://localhost:1234`.
4. In the ForgeIEC editor:

   | Field | Value |
   |---|---|
   | API | `http://localhost:1234/v1` |
   | API Key | (leave empty or anything) |
   | Model | as shown in LM Studio |

**Variant B — llama.cpp server**

`llama-server -m model.gguf --port 1234` — same API URL as LM
Studio.

**Variant C — Ollama**

1. Start `ollama serve`, pull a model (`ollama pull qwen2.5-coder`).
2. Address: `http://localhost:11434/v1` (OpenAI-compatible endpoint).

**Model recommendation for PLC coding (as of 2026-05):**

- For local operation, at least a **code-specialised 30B model**
  (e.g. Qwen-3-Coder-30B-A3B, DeepSeek-Coder-V2-Lite)
- Smaller models (7B-14B) make many IEC-ST syntax errors and often
  loop

---

## Which provider for which task?

| You want … | Recommendation |
|---|---|
| Fast simple help (create one variable) | gpt-4o-mini or Claude Haiku |
| Complex programming (multiple POUs, refactor) | Claude Opus or gpt-4o |
| Code review with detailed feedback | Claude Opus |
| Data must stay in-house | LM Studio + Qwen-Coder-30B |
| Long diagnostic session with many values | Claude Sonnet (1M context) or gpt-5 |
| First steps without spending money | LM Studio with a small model |

---

## Multiple providers in parallel?

Yes. You can set a **different provider per persona**:

- Blacksmith Master → gpt-4o (fast, good coding)
- Reviewer → claude-opus-4-7 (thorough)
- Monitor → small local model (safe, free)

Switch in the AI panel between the tabs — settings are saved per
persona.

---

## Security + privacy

**Cloud providers:**
- Your requests + the ST code snippets the assistant sends pass
  through the internet to the respective provider.
- If that is not acceptable for your project → local AI.
- Never share API keys with colleagues or check them into Git.

**Local AI:**
- Data does not leave your machine.
- The API key is optional / irrelevant (no real server checks it).

**In all cases:**
- The ForgeIEC editor itself stores no requests or replies in the
  cloud.
- Chat history is saved locally under
  `~/.config/ForgeIEC/Chats/<persona>.jsonl`.
- The audit log at `~/.config/ForgeIEC/mcp_audit.log` records
  every write action with a timestamp — regardless of provider.

---

## Next

- [Personas](/help/ai/agents/) — characters
- [Daily operation](/help/ai/chat/) — input + emergency stop
- [Security model](/help/ai/security/)
- [Back to the AI overview](/help/ai/)
