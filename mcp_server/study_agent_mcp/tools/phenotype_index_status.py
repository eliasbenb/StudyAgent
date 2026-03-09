from __future__ import annotations

import os
from typing import Any, Dict

from study_agent_mcp.retrieval import index_status

from ._common import with_meta


def register(mcp: object) -> None:
    @mcp.tool(name="phenotype_index_status")
    def phenotype_index_status_tool() -> Dict[str, Any]:
        status = index_status()
        status["embed_url"] = os.getenv("EMBED_URL", "http://localhost:3000/ollama/api/embed")
        status["embed_model"] = os.getenv("EMBED_MODEL", "qwen3-embedding:4b")
        status["embed_api_key_set"] = os.getenv("EMBED_API_KEY") is not None
        return with_meta(status, "phenotype_index_status")

    return None
