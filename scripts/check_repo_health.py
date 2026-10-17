#!/usr/bin/env python3
"""Audit GitHub repositories listed in README.md for archive status or inactivity."""

from __future__ import annotations

import concurrent.futures
import datetime
import json
import os
import pathlib
import re
import sys
import urllib.error
import urllib.request

ROOT_DIR = pathlib.Path(__file__).resolve().parent.parent
README_PATH = ROOT_DIR / "README.md"
GITHUB_REPO_REGEX = re.compile(r"https://github\.com/([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+?)(?:\)|/|\s|$)")
STALE_DAYS_THRESHOLD = 540


def check_repo(slug: str, token: str | None) -> str | None:
    """Return an issue description if the repository is archived or stale, else None."""
    api_url = f"https://api.github.com/repos/{slug}"
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "awesome-compliance-as-code-health-monitor/1.0",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    req = urllib.request.Request(api_url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return f"- [NOT FOUND / 404] `{slug}`"
        return None
    except Exception:  # noqa: BLE001
        return None

    if data.get("archived"):
        return f"- [ARCHIVED] `{slug}`"

    pushed_at = data.get("pushed_at")
    if pushed_at:
        last_push = datetime.datetime.fromisoformat(pushed_at.replace("Z", "+00:00"))
        cutoff = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=STALE_DAYS_THRESHOLD)
        if last_push < cutoff:
            return f"- [INACTIVE > {STALE_DAYS_THRESHOLD}d] `{slug}` (last push: {last_push.date()})"
    return None


def main() -> int:
    content = README_PATH.read_text(encoding="utf-8")
    raw_slugs = set(GITHUB_REPO_REGEX.findall(content))
    slugs = sorted(
        s.removesuffix(".git")
        for s in raw_slugs
        if not s.startswith("fabriziosalmi/awesome-compliance-as-code")
        and not s.startswith("sindresorhus/")
    )
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")

    print(f"Auditing {len(slugs)} GitHub repositories for archive status and freshness...")
    findings: list[str] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:
        results = pool.map(lambda s: check_repo(s, token), slugs)
        for finding in results:
            if finding:
                findings.append(finding)
                print(f"  WARN {finding}", file=sys.stderr)

    if findings:
        print(f"Found {len(findings)} archived or stale repository entry/entries:", file=sys.stderr)
        for item in findings:
            print(f"  {item}", file=sys.stderr)
        return 1

    print(f"OK: all {len(slugs)} GitHub repositories are active and unarchived.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
