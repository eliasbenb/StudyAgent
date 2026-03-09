from __future__ import annotations

import argparse
import json
import sys
import time

from study_agent_mcp.retrieval import get_default_index, index_status


def main() -> int:
    parser = argparse.ArgumentParser(description="Probe MCP phenotype index + search path.")
    parser.add_argument("--query", default="acute GI bleed in hospitalized patients")
    parser.add_argument("--top-k", type=int, default=5)
    args = parser.parse_args()

    status = index_status()
    print("INDEX STATUS:")
    print(json.dumps(status, indent=2))

    if not status.get("exists"):
        print("ERROR: index directory missing.", file=sys.stderr)
        return 1

    try:
        t0 = time.time()
        index = get_default_index()
        print(f"INDEX LOAD OK: {len(index.catalog)} docs in {time.time() - t0:.2f}s")
    except Exception as exc:
        print(f"ERROR: index load failed: {exc}", file=sys.stderr)
        return 2

    try:
        t1 = time.time()
        results = index.search(args.query, top_k=args.top_k)
        print(f"SEARCH OK: {len(results)} results in {time.time() - t1:.2f}s")
        print(json.dumps(results[: args.top_k], indent=2))
    except Exception as exc:
        print(f"ERROR: search failed: {exc}", file=sys.stderr)
        return 3

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
