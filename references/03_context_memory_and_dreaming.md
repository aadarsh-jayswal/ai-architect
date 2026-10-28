# Module 03: Context Engineering, Production Memory & Out-of-Band "Dreaming"

## 1. The 4 Context Engineering Actions
1. **Write:** Persist plans, scratchpads, and intermediate artifacts outside the active prompt window.
2. **Select:** Retrieve only the schema, memories, and chunks strictly required for the current step.
3. **Compress:** Summarize long tool-call trails (`"Checked A & B; A failed due to X; B returned Y"`) to prevent Context Rot.
4. **Isolate:** Partition sub-agent contexts so verbose intermediate exploration never pollutes the coordinator's window.

## 2. The 3 Memory Stores (Never Mix in One Unfiltered Table)
- **Short-Term (Thread-Scoped Checkpointer):** Active conversation messages, current tool results, and resumable graph state (LangGraph PostgresCheckpointer / Redis).
- **Episodic Memory:** Timestamped records of past sessions, ticket resolutions, and few-shot behavioral traces.
- **Semantic Memory:** Structured user facts, preferences, and entity relationships (updated dynamically when facts change, e.g., `"User's manager is Priya"`).
- **Procedural Memory:** System skills, tool formatting rules, and SOP instructions.

## 3. In-Band Production Memory Guardrails (Anthropic Architecture)
- **Lineage-Aware Versioning:** Every memory write logs `version_id`, `source_session_id`, `author_agent_id`, and `timestamp` for 1-click rollback.
- **Optimistic Concurrency via Pre/Post Hashing:**
  1. Compute `hash_pre = SHA256(current_memory_state)`.
  2. Draft memory update.
  3. Compute `hash_post = SHA256(live_memory_state)` immediately before commit.
  4. If `hash_pre != hash_post`, abort commit, re-fetch latest state, and re-merge.
- **3-Tier Blast-Radius Permissioning:**
  - *Tier 1 (Org-Wide Global Knowledge):* Strictly **Read-Only** for runtime agents.
  - *Tier 2 (Team / Tenant Context):* Scoped by RBAC / `tenant_id`.
  - *Tier 3 (Individual Agent Scratchpad):* Full Read/Write for the agent's local task loop.

## 4. Out-of-Band "Dreaming" Batch Architecture
Never burn live user latency trying to curate global knowledge in-band. Run an asynchronous nightly/batch **Dreaming Orchestrator**:
1. **Permission-Scoped Transcript Partitioning:** Group session transcripts and tool-call logs strictly by `tenant_id` / ACL boundary so secrets never leak across tenants.
2. **Sub-Agent Fleet Review:** Analyze thumbs-down traces, low-confidence reranker scores, and repeated MCP tool parameter retries.
3. **Three Automated Outputs (with Human-in-the-Loop Diff Approval):**
   - *RAG Curriculum Gap Report:* Identifies missing document topics or broken table chunks causing abstentions/hallucinations.
   - *Self-Healing Tool Instructions:* Patches MCP tool descriptions when agents repeatedly fail parameter formatting (e.g., date/currency formats).
   - *Memory Compaction & Pruning:* Removes stale/contradictory facts and proposes clean diffs with prevalence stats (`"Failed in 14% of sessions"`).
