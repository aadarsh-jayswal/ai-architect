# Domain Playbook: Industrial, Manufacturing & IoT
1. **Heavy BM25 + Parent-Child Safety Retrieval:** Set hybrid `alpha` toward keyword precision (`0.3 - 0.5`) to match exact part SKUs (`VALVE-882-X`) and fault codes (`ERR_094`). Retrieve the entire Parent repair procedure so safety warnings are never truncated.
2. **Multimodal Diagram Indexing:** Use ColPali / VLM patch embeddings (`Cohere embed-v4.0`) for wiring schematics and engineering blueprints.
3. **Sensor Anomaly Routing:** Route high-frequency telemetry streams to XGBoost / Isolation Forests / JEPA encoders—invoke the LLM only to synthesize the maintenance checklist UI.
