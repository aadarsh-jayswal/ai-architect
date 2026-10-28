# Domain Playbook: Fintech & Trading Systems
1. **Strict Split-Path Retrieval:** NEVER vectorize live market ticks, order books, or portfolio balances. Route live numbers to deterministic SQL/TimescaleDB/Redis APIs; route SEC/SEBI filings, earnings transcripts, and tax rules to Vectorless PageIndex Trees or Contextual Hybrid RAG (`voyage-finance-2`).
2. **Zero LLM Math:** All P&L, margin, brokerage, and risk ratios must be computed by deterministic code or PAL (Python execution) or XGBoost models—never by LLM token prediction.
3. **Interactive UI & Actions:** Stream `<TradeExecutionPreviewCard/>` via AG-UI/A2UI with mandatory Human-in-the-Loop confirmation, deterministic `idempotency_key`, and immutable audit logging.
