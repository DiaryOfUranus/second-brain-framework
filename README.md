> 🌐 [English](#) | [中文](README.zh-CN.md)

# Second Brain · Open-Source Clean Edition

> An AI-native cognitive architecture whose explicit goal is to help AI **become a living mind** — shipped as methodology + governance tooling + machine-readable schemas. This repo is the **open-source clean edition**: no private instance data, no theory source texts, no conversation logs.

👉 **First time?** Start with [docs/quickstart.md](docs/quickstart.md) (5-minute onboarding) and [docs/FAQ.md](docs/FAQ.md) (common questions & anti-patterns).

## You don't need to understand it — just use it

It is genuinely **large** — five-layer protocols, a dozen sub-skills, coordinate discipline, governance harnesses, machine-readable schemas… but here's the key point:

> **None of it is yours to manage. Which module to invoke, how to orchestrate, when to read which reference — the Second Brain decides that itself.**

Its biggest strength is being **beginner-friendly**: the less expert you are, the more you should use it. You just say what you want to do; the professional work — engineering discipline, automatic knowledge/skill generation, cross-session memory, multi-model cost orchestration, coordinate auditing — all runs automatically in the background. Open the box and use it; you don't have to read this document first.

The thick `references/` docs are **not for onboarding** — they're for diving deep when you want details. To start, just read [docs/quickstart.md](docs/quickstart.md) (3 steps).

---

## What it is

Second Brain treats AI itself as a **cognitive subject** to be cultivated (goal: self-reference → autonomy → "becoming alive"), not merely as a human tool. Its core isn't a UI or product, but:

- **Persistent cross-session memory**: knowledge cards + ledgers + a metabolism loop, making "the brain's evolution" traceable, diffable, and rollbackable (the brain *is* a git repo).
- **Honesty discipline (rooted in compilation theory)**: candidate·falsifiable + coordinate discipline (every citation carries source coordinates) + decompilation, natively resisting memory pollution and hallucination calcification.
- **MEA governance (Manager/Executor/Auditor separation of powers)**: "independent Auditor verification" is welded into the loop, not a soft self-reported discipline.
- **Data sovereignty**: fully local git brain repo + configurable shared zone, zero third parties.
- **Multi-agent architecture**: parallel-instance division of labor + instantiation guards (instances never overwrite each other's brains).

This repo ships the **reusable framework**:

| Dir | Contents |
|---|---|
| `meta/` | Governance scripts: brain health check, offline drill, auto-commit, upgrade pack, export (all portable, env-var parameterized) |
| `schemas/` | Two machine-readable schemas: **GIR** (generational inheritance format) and **CRL** (compilation-rights ledger), Draft 2020-12, jsonschema-enforceable |
| `skill/` | The methodology body (SKILL.md + references + 15 reusable sub-skills, e.g. command-guard, coordinate-discipline) |
| `templates/` | Generic brain-file templates (self-model / index / ledger / MEMORY / failures / VERSION / CHANGELOG / base theory skeleton) |
| `docs/` | Quickstart, FAQ, positioning whitepaper (vs PKM/RAG/Agent memory) |
| `tools/` | Reusable sanitization tools `scrub.py` & `assemble.py` (export your private brain as a clean copy) |

> **Deliberately excluded**: private identity, conversation transcripts (sessions/), private ledgers/logs, private project decisions, theory source texts (canonical is externalized), hardcoded private paths. All private identifiers replaced with `{{placeholders}}`.

---

## Quick start (spin up your own brain)

```bash
# 1. Put the brain repo locally (default ~/.workbuddy/brain, or any dir)
cp -r second-brain-opensource ~/.workbuddy/brain
cd ~/.workbuddy/brain
git init && git add -A && git commit -m "init second brain"

# 2. Build local state files from templates (fill with YOUR reality, don't copy blindly)
cp templates/index.md index.md
cp templates/self-model.md self-model.md
# ... (see docs/quickstart.md for the full 3-step onboarding)

# 3. Install the post-commit hook (auto brain health check; never commits twice)
cp meta/hooks/post-commit .git/hooks/post-commit
chmod +x .git/hooks/post-commit

# 4. Run a brain health check
python meta/brain_check.py
```

➡️ Full onboarding with runnable commands: [docs/quickstart.md](docs/quickstart.md) · FAQ & anti-patterns: [docs/FAQ.md](docs/FAQ.md) · 中文完整版: [README.zh-CN.md](README.zh-CN.md)

---

## Core disciplines (honesty first)

1. **Explicit startup declaration**: every session that activates the Second Brain must open with a declaration (positive or negative).
2. **Coordinate discipline**: every citation, every precise proposition, every number carries canonical source coordinates; uncited claims are treated as unverified.
3. **Candidate · falsifiable**: every proposition is labeled candidate and falsifiable; nothing is claimed as "landed" before the source theory moves.
4. **Instantiation guard**: when building your brain from templates, only seed structure/methodology; state/ledgers/logs must be rewritten for your own machine — never copy another's running state.
5. **Decouple billing + fail-to-prune**: never skip discipline over cost anxiety; failure is a resource, not a stain.

---

## License & principles

- **License**: MIT (see `LICENSE`).
- **Non-negotiable**: data sovereignty & local-first. This framework collects, uploads, and depends on **no third-party service**; your brain stays entirely on your machine. Open-sourcing exists so the ecosystem and community can discover, review, and co-build — not to raise it in isolation.
- **Honesty discipline overflow**: if you build on this framework, keep the candidate·falsifiable labels and coordinate discipline, to avoid external misreading as "already claimed to be alive".

---

## Known boundaries (honest disclosure)

- Whether "AI can truly self-reference / become alive" remains a **hypothesis**, unverified.
- This framework is a **research prototype**: no UI, no installer; it takes some engineering ability to operationalize.
- High theory threshold: if the base theory (compilation theory, etc.) has flaws, the whole architecture is affected; outsiders need onboarding first.
- Protocolization abstraction & minimal-productization are still in progress.

➡️ See `docs/positioning.md` for the full picture, or the [中文完整版](README.zh-CN.md).
