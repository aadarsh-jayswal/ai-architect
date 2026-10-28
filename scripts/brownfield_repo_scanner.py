#!/usr/bin/env python3
# Brownfield Repository Reconnaissance Scanner (4-Pass Diagnostic Tool)
# Run inside any existing project: python brownfield_repo_scanner.py /path/to/repo
import json
import re
import sys
from pathlib import Path

AI_SDK_PATTERNS = [
    "openai", "anthropic", "@google/genai", "litellm", "langchain",
    "langgraph", "llamaindex", "mastra", "ai", "chromadb", "qdrant",
    "pinecone", "pgvector", "xgboost", "lightgbm", "bullmq", "celery",
    "zod", "pydantic"
]

HOT_PATH_REGEX = re.compile(
    r"(RecursiveCharacterTextSplitter|TokenTextSplitter|embed|rerank|streamText|"
    r"createAgent|StateGraph|vector|tsvector|HNSW|IVFFlat)",
    re.IGNORECASE
)

def scan_repo(root_path: Path):
    report = {
        "repo": str(root_path.resolve()),
        "detected_dependencies": [],
        "orm_and_db_files": [],
        "rag_and_agent_hotpaths": [],
        "risk_flags": []
    }
    manifest_files = ["package.json", "requirements.txt", "pyproject.toml", "docker-compose.yml"]
    for mf in manifest_files:
        for match in root_path.rglob(mf):
            if "node_modules" in match.parts or ".venv" in match.parts:
                continue
            text = match.read_text(errors="ignore").lower()
            for pkg in AI_SDK_PATTERNS:
                if pkg in text and pkg not in report["detected_dependencies"]:
                    report["detected_dependencies"].append(pkg)

    for ext in ("*.prisma", "*.sql", "*model*.ts", "*model*.py", "*schema*.ts", "*schema*.py"):
        for f in root_path.rglob(ext):
            if any(p in f.parts for p in ("node_modules", ".venv", ".git", "dist")):
                continue
            report["orm_and_db_files"].append(str(f.relative_to(root_path)))

    for code_ext in ("*.py", "*.ts", "*.tsx", "*.js"):
        for cf in root_path.rglob(code_ext):
            if any(p in cf.parts for p in ("node_modules", ".venv", ".git", "dist", "build")):
                continue
            content = cf.read_text(errors="ignore")
            matches = set(HOT_PATH_REGEX.findall(content))
            if matches:
                report["rag_and_agent_hotpaths"].append({
                    "file": str(cf.relative_to(root_path)),
                    "markers": sorted(list(matches))
                })

    if "litellm" not in report["detected_dependencies"]:
        report["risk_flags"].append("No AI Gateway (e.g., LiteLLM) detected — single-provider outage risk.")
    if not any("rerank" in str(h["markers"]).lower() for h in report["rag_and_agent_hotpaths"]):
        report["risk_flags"].append("No Cross-Encoder Reranker marker found in hot-path files.")

    return report

if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    print(json.dumps(scan_repo(target), indent=2))
