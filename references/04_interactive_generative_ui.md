# Module 04: In-App Action Execution, Generative UI Streaming & Storage Topology

## 1. In-App Action Execution ("Text-to-Action" Copilot Pattern)
When users instruct the chat to perform actions inside the host application (e.g., *"Create a high-priority query for Acme billing due Friday"*):

### A. Slot-Filling & Schema Validation (Node.js/Zod & Python/Pydantic)
Never guess missing required fields. Validate tool parameters against strict schemas before execution:

**TypeScript (Zod) Action Contract:**
```typescript
import { z } from "zod";

export const CreateQueryActionSchema = z.object({
  idempotencyKey: z.string().uuid(),
  title: z.string().min(5).max(120),
  category: z.enum(["BILLING", "TECHNICAL", "COMPLIANCE", "GENERAL"]),
  priority: z.enum(["LOW", "MEDIUM", "HIGH", "CRITICAL"]),
  dueDateIso: z.string().datetime(),
  assigneeId: z.string().optional(),
});
```

**Python (Pydantic v2) Action Contract:**
```python
from pydantic import BaseModel, Field
from typing import Literal, Optional
from uuid import UUID
from datetime import datetime

class CreateQueryAction(BaseModel):
    idempotency_key: UUID
    title: str = Field(min_length=5, max_length=120)
    category: Literal["BILLING", "TECHNICAL", "COMPLIANCE", "GENERAL"]
    priority: Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    due_date_iso: datetime
    assignee_id: Optional[str] = None
```

### B. Blast-Radius Execution Routing
- **Low Blast Radius (Drafts, creating standard tasks, applying UI filters):**
  1. Execute mutation using **User-Scoped OBO JWT** + deterministic `idempotency_key`.
  2. Emit an SSE **Client Side-Effect Event**: `{ "type": "CLIENT_EFFECT", "action": "INVALIDATE_QUERY", "queryKeys": ["queries", "tasks"] }` so React / TanStack Query / Zustand updates the main app screen immediately without page reload.
  3. Render a compact `<ActionCompletedCard/>` in chat featuring a deterministic **`[Undo]` button** (`DELETE /api/queries/:id`).
- **High Blast Radius (Deleting records, financial transfers, bulk updates):**
  1. Halt execution before DB write.
  2. Stream an interactive `<ActionPreviewCard/>` with pre-filled fields and `[Confirm]` / `[Edit]` buttons.

## 2. The 3-Tier Generative UI Streaming Architecture
Decouple **UI Component Code** from **Retrieved/Generated Data**:
1. **Tier 1 — Pre-Built Typed Component Props (<800ms Time-to-Interactive):** Host frontend holds pre-built React components (`<QuizCard/>`, `<TradeConfirmation/>`, `<LoanTable/>`). LLM streams only a 100-token JSON prop payload. Use for 90% of production features.
2. **Tier 2 — Declarative UI Specs (AG-UI Transport + A2UI Wire Format, 1.5–2.5s):** LLM streams a flat JSON adjacency list of approved design-system primitives (`Card`, `Row`, `Form`, `BarChart`) with JSON Pointer (`/data/...`) state bindings. Zero CSS hallucinations, zero iframe overhead.
3. **Tier 3 — Sandboxed Canvas / MCP-Apps (`ui://` URIs, 8–20s):** Isolated `iframe` for ad-hoc custom simulations or third-party host clients (Claude Desktop / VS Code).

## 3. Progressive 1st-Item Streaming & Speculative Pre-Fetching
Never make a user wait 12 seconds for a 10-item quiz or multi-step checklist:
- Retrieve & generate **Item #1 only** and render it on screen in **<800ms**.
- While the user interacts with Item #1, an async background worker generates Items #2–#10 and caches them in `sessionStorage` / Redis.

## 4. Client & Server Storage Topology
- **React State / RAM:** Active streaming tokens and ephemeral UI toggles.
- **`sessionStorage`:** Pre-fetched quiz/wizard queue and current tab workflow state.
- **`localStorage`:** Theme toggles, non-sensitive UI preferences.
- **`IndexedDB`:** Offline industrial manuals, large client-side history caches, non-repeating `seen_question_ids`.
- **`HttpOnly` Secure Cookies:** Scoped session/OBO auth tokens (never accessible to LLM prompts).
- **Redis / RedisVL:** Exact response cache (<5ms), Semantic Cache (>0.96 cosine similarity + tenant filter), and BullMQ/Celery job queues.
- **PostgreSQL (`pgvector` + `pg_search`) / Qdrant:** Durable relational records, ACID transactions, and hybrid vector+BM25 indexes.
