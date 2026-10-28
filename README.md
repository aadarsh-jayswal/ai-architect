# AI Architect

**Design AI/ML systems, audit existing applications, and choose the simplest effective architecture.**

AI Architect is a reusable Codex skill for turning requirements or repository evidence into architecture blueprints and focused upgrade plans. It covers deterministic workflows, classical machine learning, LLMs, retrieval-augmented generation (RAG), and agent systems, with guidance for fintech, banking, industrial IoT, and education.

## What it helps you do

- Clarify the problem, available data, query patterns, action requirements, and deployment constraints.
- Compare approaches before introducing more complex models or agents.
- Plan ingestion, retrieval, reranking, storage, and memory.
- Design in-app actions, structured outputs, and interactive UI streaming.
- Define security controls, evaluation gates, observability, latency budgets, and operating costs.
- Audit an existing repository and prioritize targeted improvements and migration steps.

## Two workflows

| Workflow | Starting point | Process | Deliverable |
| --- | --- | --- | --- |
| **Greenfield** | A new product or AI/ML use case | Three discovery rounds covering the problem and data, queries and actions, then scale and constraints; a 10-point requirement summary for your approval | An architecture blueprint using the included template |
| **Brownfield** | An existing repository | Repository scanner and four-pass reconnaissance, followed by ranked fixes and migration planning | A surgical audit and upgrade plan using the included template |

The core selection rule is to stop at the simplest approach that reliably solves the requirement. The skill considers deterministic code, typed decision models, tabular ML, visual models, schema-validated LLM calls, grounded RAG, single agents, and finally multi-agent systems.

## Install locally in Codex

You need Codex and Git. Python 3 is needed only to run the bundled helper scripts.

Clone this repository into your personal skills directory. If an `ai-architect` folder already exists there, review or update that installation instead of cloning over it.

**Windows PowerShell**

```powershell
New-Item -ItemType Directory -Path "$HOME/.agents/skills" -Force | Out-Null
git clone https://github.com/aadarsh-jayswal/ai-architect.git "$HOME/.agents/skills/ai-architect"
```

**macOS / Linux**

```bash
mkdir -p "$HOME/.agents/skills"
git clone https://github.com/aadarsh-jayswal/ai-architect.git "$HOME/.agents/skills/ai-architect"
```

For a project-specific installation, clone into `.agents/skills/ai-architect` inside that project instead. Codex discovers local skills automatically; restart Codex if the skill does not appear. See the [official skill documentation](https://learn.chatgpt.com/docs/build-skills) for discovery locations and invocation options.

## Usage

Ask Codex to use AI Architect and describe your project. In Codex CLI or the IDE extension, you can explicitly mention `$ai-architect`.

**Design a new system**

```text
Use $ai-architect to design an internal support assistant for a fintech team.
It must answer from policy documents and perform approved account actions.
Start with requirement discovery and compare the simplest viable approaches.
```

**Audit an existing application**

```text
Use $ai-architect to audit this repository's RAG application.
Focus on retrieval quality, tenant isolation, latency, and operating cost.
Produce a ranked upgrade plan based on repository evidence.
```

**Compare architecture options**

```text
Use $ai-architect to assess whether this workflow needs deterministic code,
classical ML, a single LLM call, RAG, or an agent. Ask for missing requirements
before selecting an architecture.
```

## Bundled tools

Run these commands from the cloned skill folder.

### Repository reconnaissance

```bash
python scripts/brownfield_repo_scanner.py /path/to/project
```

Produces a JSON report with detected dependency markers, database/schema files, RAG and agent code markers, and heuristic risk flags. Findings are starting points for inspection; a missing marker does not establish that a capability is absent.

### Token and cost estimation

```bash
python scripts/token_and_latency_calculator.py --dau 100000 --queries-per-user 5 --indic-ratio 0.3
```

Estimates monthly cost and savings under configurable token, caching, and routing assumptions. Use `--help` to see available inputs. Default prices and token multipliers are modeling assumptions; the reported latency values are fixed reference estimates. Validate them against your providers and workload before using them for planning.

Both scripts use the Python standard library.

## Repository contents

```text
ai-architect/
|-- README.md
|-- SKILL.md
|-- LICENSE
|-- licence/
|   `-- LICENSE
|-- references/
|   |-- 01_agentic_patterns_and_paradigms.md
|   |-- 02_rag_taxonomy_and_vectorless.md
|   |-- 03_context_memory_and_dreaming.md
|   |-- 04_interactive_generative_ui.md
|   |-- 05_security_evals_and_finops.md
|   `-- domain_playbooks/
|       |-- banking_and_compliance.md
|       |-- edtech_and_learning.md
|       |-- fintech_and_trading.md
|       `-- industrial_and_iot.md
|-- scripts/
|   |-- brownfield_repo_scanner.py
|   `-- token_and_latency_calculator.py
`-- templates/
    |-- brownfield_surgical_audit_template.md
    `-- greenfield_blueprint_template.md
```

[SKILL.md](SKILL.md) contains the workflow instructions. Supporting references are loaded as needed, and the templates define the blueprint and audit outputs.

## Author

**Aadarsh Jayswal**

- GitHub: [aadarsh-jayswal](https://github.com/aadarsh-jayswal)
- Email: [aadarshjayswal.tech@gmail.com](mailto:aadarshjayswal.tech@gmail.com)

## License

Released under the [MIT License](LICENSE).

Copyright (c) 2026 Aadarsh Jayswal.
