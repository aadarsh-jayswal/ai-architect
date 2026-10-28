# Module 05: Zero-Trust Security, 3-Layer Evals, Stage Gates & FinOps

## 1. The 5-Layer Zero-Trust Agent Security Stack
`User -> Input Guardrail (before_agent) -> Agent -> Tool Allowlist -> Least-Privilege Scoped OBO Auth -> Sandbox -> Secret Manager -> OpenTelemetry Audit Logs`
- **PII Middleware:** Enforce automatic detection (`email`, `credit_card`, `phone`, `aadhaar`, `pan`, `ip`) with `redact`, `mask`, `hash`, or `block` strategies *before* sending prompts to external LLMs and *before* writing logs.
- **MCP Descriptor Hash-Locking & `200 OK` Schema Pinning:** Hash external MCP tool manifests at deploy time to block runtime tool-poisoning. Validate every external API `200 OK` response against a strict Zod/Pydantic schema so silent API drift never causes LLM fabrication.
- **Hard Cycle Detector & Token Circuit-Breaker:** Kill any trace that calls the same tool with similar arguments `> 3 times` or exceeds the per-trace token/rupee budget cap.
- **Regulatory Compliance (India DPDP Act 2023 / RBI / GDPR / HIPAA):** Enforce verifiable consent, purpose limitation, data residency (India/VPC regions), and automated retention purging.

## 2. The 3-Layer Decoupled Evaluation Harness
- **Cold-Start Day-0 Bootstrapping:** If no test dataset exists, automatically synthesize 50 adversarial test pairs from raw docs/schemas (Exact ID lookups, multi-row table math, leading questions presupposing false premises, out-of-scope abstentions, and version conflicts).
- **Layer 1: Retrieval Evals (Pure Math, $0 LLM Cost):** `Recall@K` (target >= 85%), `MRR`, and metadata filter accuracy. If Recall@5 < 85%, freeze prompt changes and fix chunking/BM25/reranker.
- **Layer 2: Generation & Hallucination Evals (RAG Triad):**
  - *Context Faithfulness (Intrinsic Hallucination check):* Zero contradiction of retrieved numbers/facts.
  - *Extrinsic Groundedness:* Zero invention beyond retrieved context.
  - *Negative Rejection / Abstention:* Correctly abstains on missing data or sycophantic leading questions.
- **Layer 3: Deterministic UI, Action & Latency Contracts:** 100% Zod/Pydantic validity, idempotency verification, and P95 Time-to-Interactive.

## 3. Company Stage-Gate Calibration Matrix
| Stage | Scale | Mandatory Eval & Operational Gate | Upgrade / Migration Strategy |
| :--- | :--- | :--- | :--- |
| **Stage 1: PoC / Trial** | 10 – 500 users | 30–50 Golden Set cases, Recall@5 >= 80%, 100% JSON schema validity. | Direct iteration; optimize for speed of learning. |
| **Stage 2: Growth** | 1k – 50k users | Automated CI/CD Eval Gate (200+ cases), P95 UI < 1.5s, cost/task tracking, 5% sampled live trace evals. | Shadow Deployment (run new pipeline in parallel before cutover). |
| **Stage 3: Enterprise** | 1 Lakh – 10M+ users | P99 latency SLAs, LiteLLM multi-provider failover, 0.0% RBAC leakage, red-teaming, canary auto-rollback. | 11-Step Dual-Write Shadow Index + Canary Rollout (1% -> 10% -> 100%). |

## 4. FinOps & Indic Token Multipliers
- **3-Layer Caching:** (1) Exact Redis Cache -> (2) Tenant-Scoped Semantic Cache (>0.96 cosine) -> (3) Provider Prompt Caching (pin static system prompts, schemas, and trees at prefix for 50–90% discount).
- **Indic Language Token Multiplier:** English ~ 4 chars/token. Hindi, Gujarati, Marathi, Tamil, etc. consume **2.5x to 4.0x more tokens** per word. Always apply the Indic multiplier in cost and context-window budgets for Indian deployments.
