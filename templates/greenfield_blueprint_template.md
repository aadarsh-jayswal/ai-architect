# Production AI Architecture Blueprint: [Project Name]

## 1. Requirement Lock & Constraints Summary
- **Domain & Company Stage:** [Stage 1 Trial / Stage 2 Growth / Stage 3 Enterprise (1L+ Users)]
- **Latency & FinOps SLA:** [P95 Target ms | Max Cost per Trace]
- **Compliance & Security Boundary:** [DPDP Act 2023 / RBI / SOC2 / HIPAA / RBAC Rules]

## 2. Multi-Paradigm Decision & Anti-Bloat Justification
- **Why Lower Tiers Were Accepted/Rejected:** [Code vs. Jev vs. XGBoost/TabPFN vs. LLM]
- **Selected Agentic Design Patterns (from the 21-Pattern Catalog):** [...]

## 3. Data Ingestion, RAG & Storage Topology
- **Document Parsing & Chunking Strategy:** [Docling/LlamaParse / Parent-Child / Contextual Headers / Vectorless Tree]
- **Search & Reranking Pipeline:** [In-DB BM25 + Vector RRF (k=60) / Alpha Setting / Cross-Encoder Cutoff]
- **Memory & Storage Map:** [RAM / sessionStorage / IndexedDB / Redis Semantic Cache / Postgres+pgvector]
- **Out-of-Band "Dreaming" Batch Loop:** [Nightly Transcript & Curriculum Gap Audit]

## 4. In-App Action Execution & Interactive UI Streaming
- **Generative UI Tier:** [Pre-built JSON Props (<800ms) / AG-UI + A2UI Declarative / MCP-Apps]
- **Action Mutation Schema (Zod / Pydantic) & Client Cache Invalidation:** [OBO JWT + Idempotency + Undo Card]

## 5. 5-Layer Security, Cycle Guards & 3-Layer Eval Harness
- **Guardrails & Loop Caps:** [PII Middleware / Max Iterations / Per-Trace Budget Breaker]
- **Golden Set & CI/CD Gates:** [Retrieval Recall@5 | RAG Triad Faithfulness | Schema Validity]
