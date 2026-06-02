from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "probe_outputs"
OUT_PATH = OUT_DIR / "connector_probe_2026-05-31.json"


def fetch_json(name: str, url: str, timeout: int = 20) -> dict:
    request = Request(url, headers={"User-Agent": "oli-research-stack-v0/0.1"})
    started_at = datetime.now(timezone.utc).isoformat()
    try:
        with urlopen(request, timeout=timeout) as response:
            raw = response.read(1_000_000)
            text = raw.decode("utf-8", errors="replace")
            parsed = json.loads(text)
            return {
                "connector": name,
                "url": url,
                "ok": True,
                "started_at": started_at,
                "status": getattr(response, "status", None),
                "summary": summarize(name, parsed),
            }
    except Exception as exc:  # noqa: BLE001 - probe records failures explicitly.
        return {
            "connector": name,
            "url": url,
            "ok": False,
            "started_at": started_at,
            "error": f"{type(exc).__name__}: {exc}",
        }


def fetch_text(name: str, url: str, timeout: int = 20) -> dict:
    request = Request(url, headers={"User-Agent": "oli-research-stack-v0/0.1"})
    started_at = datetime.now(timezone.utc).isoformat()
    try:
        with urlopen(request, timeout=timeout) as response:
            raw = response.read(300_000)
            text = raw.decode("utf-8", errors="replace")
            return {
                "connector": name,
                "url": url,
                "ok": True,
                "started_at": started_at,
                "status": getattr(response, "status", None),
                "summary": {
                    "chars": len(text),
                    "first_300": text[:300],
                    "contains_expected_markers": contains_expected_markers(name, text),
                },
            }
    except Exception as exc:  # noqa: BLE001 - probe records failures explicitly.
        return {
            "connector": name,
            "url": url,
            "ok": False,
            "started_at": started_at,
            "error": f"{type(exc).__name__}: {exc}",
        }


def summarize(name: str, parsed: object) -> dict:
    if name.startswith("github_repo"):
        data = parsed if isinstance(parsed, dict) else {}
        return {
            "full_name": data.get("full_name"),
            "description": data.get("description"),
            "stars": data.get("stargazers_count"),
            "forks": data.get("forks_count"),
            "open_issues": data.get("open_issues_count"),
            "license": (data.get("license") or {}).get("spdx_id"),
            "pushed_at": data.get("pushed_at"),
        }
    if name == "huggingface_model_search":
        items = parsed if isinstance(parsed, list) else []
        return {
            "count": len(items),
            "top": [
                {
                    "id": item.get("id"),
                    "downloads": item.get("downloads"),
                    "likes": item.get("likes"),
                    "lastModified": item.get("lastModified"),
                }
                for item in items[:5]
                if isinstance(item, dict)
            ],
        }
    if name == "semantic_scholar_search":
        data = parsed if isinstance(parsed, dict) else {}
        papers = data.get("data") or []
        return {
            "total": data.get("total"),
            "top": [
                {
                    "title": paper.get("title"),
                    "year": paper.get("year"),
                    "citationCount": paper.get("citationCount"),
                    "url": paper.get("url"),
                }
                for paper in papers[:5]
                if isinstance(paper, dict)
            ],
        }
    if name == "openalex_search":
        data = parsed if isinstance(parsed, dict) else {}
        results = data.get("results") or []
        return {
            "count": len(results),
            "top": [
                {
                    "title": item.get("title"),
                    "publication_year": item.get("publication_year"),
                    "cited_by_count": item.get("cited_by_count"),
                    "doi": item.get("doi"),
                }
                for item in results[:5]
                if isinstance(item, dict)
            ],
        }
    if name == "nvd_keyword_search":
        data = parsed if isinstance(parsed, dict) else {}
        vulns = data.get("vulnerabilities") or []
        return {
            "totalResults": data.get("totalResults"),
            "sample": [
                {
                    "id": ((v.get("cve") or {}).get("id")),
                    "published": ((v.get("cve") or {}).get("published")),
                }
                for v in vulns[:5]
                if isinstance(v, dict)
            ],
        }
    return {"type": type(parsed).__name__}


def contains_expected_markers(name: str, text: str) -> dict:
    lowered = text.lower()
    if name == "openrouter_docs_index":
        return {
            "has_docs_title": "openrouter | documentation" in lowered,
            "has_apps_link": "/apps" in lowered or "app attribution" in lowered,
            "has_models": "models" in lowered,
        }
    if name == "arxiv_memory_search":
        return {
            "has_agent_memory": "agent memory" in lowered,
            "has_entry": "<entry>" in lowered,
        }
    return {}


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    probes = [
        fetch_text("openrouter_docs_index", "https://openrouter.ai/docs/llms.txt"),
        fetch_json("github_repo_hermes", "https://api.github.com/repos/NousResearch/hermes-agent"),
        fetch_json("github_repo_opencode", "https://api.github.com/repos/opencode-ai/opencode"),
        fetch_json("github_repo_kilocode", "https://api.github.com/repos/Kilo-Org/kilocode"),
        fetch_json("huggingface_model_search", "https://huggingface.co/api/models?search=Qwen3&limit=5"),
        fetch_text(
            "arxiv_memory_search",
            "https://export.arxiv.org/api/query?" + urlencode({"search_query": "all:agent memory", "start": 0, "max_results": 5}),
        ),
        fetch_json(
            "semantic_scholar_search",
            "https://api.semanticscholar.org/graph/v1/paper/search?"
            + urlencode({"query": "agent memory temporal knowledge graph", "limit": 5, "fields": "title,year,citationCount,url"}),
        ),
        fetch_json(
            "openalex_search",
            "https://api.openalex.org/works?"
            + urlencode({"search": "agent memory temporal knowledge graph", "per-page": 5}),
        ),
        fetch_json(
            "nvd_keyword_search",
            "https://services.nvd.nist.gov/rest/json/cves/2.0?"
            + urlencode({"keywordSearch": "Claude Code", "resultsPerPage": 5}),
        ),
    ]
    payload = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "probes": probes,
        "summary": {
            "ok": sum(1 for item in probes if item["ok"]),
            "failed": sum(1 for item in probes if not item["ok"]),
            "failed_connectors": [item["connector"] for item in probes if not item["ok"]],
        },
    }
    OUT_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(payload["summary"], indent=2))
    print(OUT_PATH)


if __name__ == "__main__":
    main()

