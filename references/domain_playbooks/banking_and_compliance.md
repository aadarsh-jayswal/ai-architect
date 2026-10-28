# Domain Playbook: Banking, KYC & Regulatory Compliance
1. **Temporal Policy Versioning:** Tag every circular/policy chunk with `effective_from`, `effective_to`, `circular_id`, and `is_latest_version = true` to prevent mixing 2022 and 2026 rules.
2. **Layout-Aware Fee & Rate Tables:** Parse PDFs with Docling/LlamaParse preserving full Markdown/HTML tables intact inside Parent chunks.
3. **Compliance & Data Residency:** Enforce RBI data localization, India DPDP Act 2023 consent/redaction, and strict Row-Level Security (RLS) so retail users and branch officers only retrieve authorized tiers.
