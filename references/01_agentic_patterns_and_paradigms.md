# Module 01: Model Paradigms, 21 Agentic Design Patterns & Loop Engineering

## 1. Hybrid Multi-Paradigm Chaining Patterns
- **Pattern A (Jev Router -> LLM Writer):** Route 100% of incoming unstructured requests through Jev/System-1 classifier first. Auto-route if probability >= 0.90; invoke frontier LLM only for final prose synthesis or <0.90 edge cases.
- **Pattern B (SLM/Jev Feature Extractor -> XGBoost Predictor -> LLM Explainer):** Extract structured columns from messy text, run millisecond tabular prediction in XGBoost/LightGBM/TabPFN, and use LLM only to narrate SHAP values.
- **Pattern C (XGBoost as an MCP Tool):** Conversational agent translates user "what-if" parameters into JSON and calls an XGBoost microservice via MCP—never guessing math in tokens.

## 2. The 21 Agentic Design Patterns Selection Matrix
1. **Prompt Chaining:** Sequential steps with strict Zod/Pydantic handoff contracts.
2. **Routing:** Intent classification with confidence thresholds and fallback paths.
3. **Parallelization:** Sharding independent tasks with rate-limiters (`max_concurrency`) and result merging.
4. **Reflection:** Generator + Critic Agent rubric loop (cap at `max_iterations = 3`).
5. **Tool Use:** Function calling with deterministic input/output schema validation and idempotency keys.
6. **Planning:** Milestone decomposition, dependency DAGs, and checkpointed replanning.
7. **Multi-Agent Collaboration:** Choose topology explicitly: Central Orchestrator, Peer-to-Peer Mesh, or Sequential Pipeline.
8. **Memory Management:** Short-term thread buffer, Episodic event store, Long-term Semantic & Procedural namespaces with TTL.
9. **Learning & Adaptation:** Aggregate user edits/outcomes -> filter noise/adversarial inputs -> A/B test prompt/policy updates.
10. **Model Context Protocol (MCP):** Standardized tool/resource manifests with descriptor hash-locking and scoped permissions.
11. **Goal Setting & Monitoring:** SMART KPIs, real-time drift detection, and automated mitigation.
12. **Exception Handling & Recovery:** Classify errors into Transient (exponential backoff + jitter), Permanent (fallback model/cache), or Critical (checkpoint state + human escalation).
13. **Human-in-the-Loop (HITL):** Decision gates for high-blast-radius actions with SLA timers and reviewer fatigue monitoring.
14. **Knowledge Retrieval (RAG):** Grounded synthesis with verifiable citations.
15. **Inter-Agent Communication (A2A v1.0):** Agent Cards (`/.well-known/agent.json`), Correlation IDs, TTLs, and deadlock detection.
16. **Resource-Aware Optimization:** Complexity router dynamically selecting Mini ($), Base ($$), or Frontier ($$$) models.
17. **Reasoning Techniques:** CoT, Tree-of-Thoughts (ToT), Self-Consistency (SC), ReAct, PAL (Program-Aided Language Models), and Graph Prompting.
18. **Guardrails & Safety:** Input sanitization (`before_agent`), PII redaction, risk scoring, and output policy checks.
19. **Evaluation & Monitoring:** Golden test gates, RAG Triad metrics, and automated rollback triggers.
20. **Prioritization:** `Priority = (Value / Effort) * Urgency * Risk` with Task Aging (starvation prevention) and state preemption.
21. **Exploration & Discovery:** Broad scouting -> theme clustering -> novelty/impact scoring -> hypothesis testing.

## 3. Loop Engineering & The "Failure Bundle" Contract
- **Golden Rule of Loop Design:** Your loop is only as honest as the verifier allowed to tell it NO.
- **Failure Bundle Contract:** When any verification or tool step fails, never return a bare `"fail"`. Return:
  `{ "failed_step": "...", "state_snapshot": "...", "root_cause": "...", "suggested_fix": "..." }`.

## 4. Model Class Routing: Interactive Flash vs. Deep Reasoning
- **Synchronous Hot-Path (TTFT < 500ms):** Use high-speed instruction models for chat, UI actions, and slot extraction. 
- **Asynchronous Deep Reasoning (TTFT > 3s):** Run thinking/reasoning models strictly in background workers (Celery/BullMQ) for question generation, multi-hop research, and code verification.
- **Client Assumption Gate:** When a client demands a single frontier model, split traffic: 85% to lightweight models via LiteLLM, 15% to frontier models for difficult queries.
