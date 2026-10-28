# Module 02: Advanced RAG Taxonomy, Vectorless Tree Index & Migration Runbooks

## 1. Retrieval Architecture Decision Matrix
- **Small Structured Corpus (<500 Markdown/SOP files):** Indexed Markdown file tree + `grep` / BM25 progressive disclosure. Zero vector DB overhead.
- **Vectorless RAG (PageIndex JSON Tree):** For tens to thousands of long, structured documents (SEC filings, RBI circulars, textbooks, contracts) requiring cross-section reasoning and explainable navigation paths.
  - *Indexing:* Detect TOC or infer section hierarchy -> split by logical sections (never arbitrary token counts) -> summarize each node (`node_id`, `title`, `page_range`, `summary`) into an in-context JSON tree.
  - *Retrieval:* LLM reads root tree -> reasons & selects child `node_id`s -> follows cross-references ("see Appendix G") -> extracts full raw section text.
- **Contextual Hybrid Vector RAG:** For high-scale (100k–10M+) low-latency factoid & keyword retrieval.
  - *Stage 1 (Offline Ingestion):* Layout-aware parsing (Docling / LlamaParse — never split tables mid-row) + Parent-Child chunking + **Anthropic Contextual Retrieval** (prepend `[Doc Title | Section | Effective Date]` before embedding).
  - *Stage 2 (In-DB Hybrid Search):* Hard Metadata Pre-filter (`tenant_id`, `is_active = true`) + Parallel Dense Vector + Sparse BM25/BM25F fused inside DB via **Reciprocal Rank Fusion (RRF, k=60)**. Tune `alpha` (`0.0` = pure BM25, `0.5` = balanced, `0.75` = semantic + exact code boost).
  - *Stage 3 (Reranking & Abstention Gate):* Cross-Encoder Reranker (Cohere Rerank v4 / BGE-v2) narrows Top-40 to Top-5. If top score < confidence cutoff (e.g., `0.45`), deterministically abstain ("Not in verified data").
- **Enterprise Hybrid (Vectors + Trees):** Use vector search to narrow 1M docs to top 5 candidate documents, then use PageIndex JSON Trees inside those 5 documents for lossless section reasoning.
- **GraphRAG:** Use when queries require traversing multi-hop entity relationships across fragmented documents.

## 2. Domain-Specific Embedding Selection
- General / Multilingual: `text-embedding-3-large` or `voyage-4-large`
- Financial & Trading: `voyage-finance-2`
- Legal & Compliance: `voyage-law-2`
- Source Code: `voyage-code-4`
- Multimodal / Visual PDFs: `Cohere embed-v4.0` or `ColPali`

## 3. Lost-in-the-Middle Context Ordering
Always assemble the prompt in this exact order:
1. System Instructions & Abstention Rules
2. Best Retrieved Chunk (#1 Rank)
3. Supporting Chunks (#3, #4, #5)
4. Second-Best Retrieved Chunk (#2 Rank — placed at the end for recency attention)
5. User Query + Citation Format Contract

## 4. 11-Step Zero-Downtime Embedding Migration Runbook (Brownfield)
1. Freeze & record live Index A version.
2. Create shadow Index B with the new embedding model/schema.
3. Re-embed all historical documents into Index B in background batches.
4. Enable **Dual-Write** on ingestion pipeline (write new/updated docs + SHA-256 tombstones to both Index A and B).
5. Run Golden Set retrieval & RBAC permission tests against both indexes.
6. Compare Recall@5, MRR, P95 latency, and cost.
7. Canary route 5% of live traffic to Index B.
8. Atomically flip the read alias from Index A to Index B.
9. Monitor faithfulness, latency, and error rates.
10. Keep Index A warm for instant alias rollback if regressions appear.
11. Retire Index A after the safety window closes.
