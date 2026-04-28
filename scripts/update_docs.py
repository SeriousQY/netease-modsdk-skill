#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

OWNER = "EaseCation"
REPO = "netease-modsdk-wiki"
BRANCH = "main"
API_BASE = f"https://api.github.com/repos/{OWNER}/{REPO}"
RAW_BASE = f"https://raw.githubusercontent.com/{OWNER}/{REPO}/{BRANCH}"
ROOT = Path(__file__).resolve().parents[1]
REFERENCES = ROOT / "references"
WIKI = REFERENCES / "wiki"

DOWNLOAD_EXACT = {
    "api-index.json",
    "docs/mcdocs/readme.md",
    "docs/mcdocs/context7.json",
}
DOWNLOAD_PREFIXES = (
    "docs/",
)


def fetch_bytes(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "mcmodapi-skill-updater"})
    with urllib.request.urlopen(req, timeout=60) as response:
        return response.read()


def fetch_json(url: str):
    return json.loads(fetch_bytes(url).decode("utf-8", "replace"))


def repo_tree() -> list[dict]:
    url = f"{API_BASE}/git/trees/{BRANCH}?recursive=1"
    data = fetch_json(url)
    if data.get("truncated"):
        print("warning: GitHub tree response is truncated", file=sys.stderr)
    return data.get("tree", [])


def should_download(path: str) -> bool:
    if path in DOWNLOAD_EXACT:
        return True
    return path.endswith(".md") and any(path.startswith(prefix) for prefix in DOWNLOAD_PREFIXES)


def raw_url(path: str) -> str:
    return f"{RAW_BASE}/{urllib.parse.quote(path, safe='/')}"


def write_binary(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def read_json_lenient(path: Path):
    text = path.read_bytes().decode("utf-8", "replace")
    return json.loads(text)


def md_escape(value) -> str:
    if value is None:
        return ""
    text = str(value).replace("\r", " ").replace("\n", " ").strip()
    text = text.replace("|", "\\|")
    return text


def anchor(text: str) -> str:
    s = text.strip().lower()
    s = re.sub(r"[^\w涓€-榭縗- ]+", "", s)
    s = re.sub(r"\s+", "-", s)
    return s or "entry"


def local_doc_link(link: str) -> str:
    if not link:
        return ""
    clean = link.split("#", 1)[0].lstrip("/")
    if not clean:
        return ""
    target = Path("wiki") / clean
    return target.as_posix()


def summarize_params(values) -> str:
    if not values:
        return ""
    parts = []
    for item in values:
        if isinstance(item, dict):
            name = item.get("name") or item.get("param") or item.get("key") or ""
            typ = item.get("type") or item.get("valueType") or ""
            desc = item.get("description") or item.get("desc") or item.get("remark") or ""
            combined = ": ".join(x for x in [name, typ] if x)
            if desc:
                combined = f"{combined} {desc}".strip()
            if combined:
                parts.append(combined)
        elif item:
            parts.append(str(item))
    return "; ".join(parts[:6])


def row_for(item: dict) -> str:
    name = md_escape(item.get("name"))
    method = md_escape(item.get("method"))
    item_type = md_escape(item.get("type"))
    side = md_escape(item.get("side"))
    description = md_escape(item.get("description"))
    params = md_escape(summarize_params(item.get("params")))
    returns = md_escape(summarize_params(item.get("return")))
    doc = local_doc_link(item.get("link") or "")
    doc_cell = f"[{md_escape(item.get('link'))}]({doc})" if doc else md_escape(item.get("link"))
    display = method or name
    entry_anchor = anchor(display)
    return f"| <a id=\"{entry_anchor}\"></a>{item_type} | {name} | {method} | {side} | {description} | {params} | {returns} | {doc_cell} |"


def write_index(path: Path, title: str, items: list[dict], intro: str) -> None:
    lines = [
        f"# {title}",
        "",
        intro,
        "",
        f"Total entries: {len(items)}",
        "",
        "| Type | Name | Method | Side | Description | Params | Return | Source |",
        "|---|---|---|---|---|---|---|---|",
    ]
    lines.extend(row_for(item) for item in items)
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def write_search_guide() -> None:
    (REFERENCES / "search-guide.md").write_text(
        """# mcmodapi Search Guide

Search generated indexes first, then mirrored wiki markdown.

## Priority order

1. `api-index.md` - all API and event entries from upstream `api-index.json`.
2. `interfaces.md` - API/interface entries only.
3. `events.md` - event entries only.
4. `wiki/docs/**/*.md` - full mirrored upstream markdown docs.
5. For API/event details, prioritize `wiki/docs/mcdocs/1-ModAPI/**/*.md` and `wiki/docs/api-tools/*.md`.

## Recommended exact searches

- `RegisterSystem`
- `ListenForEvent`
- `CreateEngineCompFactory`
- `GetEngineCompFactory`
- `extraClientApi`
- `extraServerApi`
- event names ending in `Event`

## Context7 relationship

`wiki/docs/mcdocs/context7.json` only stores a Context7 URL and public key; it is not the full documentation body. Context7 provides semantic snippets and examples, but the local mirror contains the complete upstream markdown docs, raw `api-index.json`, and generated indexes. Prefer local indexes and markdown for exact API signatures and source links; use Context7 only as a supplementary semantic/example source.

## Fallback rule

If the local indexes and mirrored docs do not contain the target identifier, report that the local `mcmodapi` docs had no match, then use Context7, GitHub, web, or other sources.

## Encoding note

Some upstream Chinese fields are mojibake in `api-index.json`. Preserve those fields as-is and rely on English identifiers, method names, event names, and mirrored markdown files for reliable lookup.
""",
        encoding="utf-8",
    )


def main() -> int:
    REFERENCES.mkdir(parents=True, exist_ok=True)
    tree = repo_tree()
    paths = sorted(item["path"] for item in tree if item.get("type") == "blob" and should_download(item.get("path", "")))
    if not paths:
        raise RuntimeError("no matching files found in GitHub tree")

    for path in paths:
        data = fetch_bytes(raw_url(path))
        destination = WIKI / path
        write_binary(destination, data)
        if path == "api-index.json":
            write_binary(REFERENCES / "api-index.raw.json", data)

    api_data = read_json_lenient(REFERENCES / "api-index.raw.json")
    if not isinstance(api_data, list):
        raise RuntimeError("api-index.json did not contain a list")

    events = [item for item in api_data if item.get("type") == "event"]
    interfaces = [item for item in api_data if item.get("type") != "event"]

    write_index(
        REFERENCES / "api-index.md",
        "NetEase ModSDK API Index",
        api_data,
        "Generated from `api-index.json`. Source links point to mirrored local markdown under `wiki/`.",
    )
    write_index(
        REFERENCES / "events.md",
        "NetEase ModSDK Events",
        events,
        "Event-only subset generated from `api-index.json`.",
    )
    write_index(
        REFERENCES / "interfaces.md",
        "NetEase ModSDK Interfaces",
        interfaces,
        "API/interface subset generated from `api-index.json`.",
    )
    write_search_guide()

    print(f"Downloaded {len(paths)} files")
    print(f"Indexed {len(api_data)} entries: {len(interfaces)} interfaces/APIs, {len(events)} events")
    print(f"Output: {REFERENCES}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())



