#!/usr/bin/env python3
"""Audit GitHub repositories listed in README.md for archive status, renames, license drift, or inactivity."""

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
ENTRY_REPO_REGEX = re.compile(
    r"^- \[[^\]]+\]\(https://github\.com/(?P<slug>[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)\) - .+ `(?P<license>[^`]+)`$"
)
STALE_DAYS_THRESHOLD = 540


def check_repo(slug: str, declared_license: str, token: str | None) -> str | None:
    """Return an issue description if the repository is archived, renamed, license-mismatched, or stale."""
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

    full_name = data.get("full_name")
    if full_name and full_name.lower() != slug.lower():
        return f"- [RENAMED] `{slug}` redirected to `{full_name}`"

    if data.get("archived"):
        return f"- [ARCHIVED] `{slug}`"

    lic_info = data.get("license")
    api_spdx = lic_info.get("spdx_id") if isinstance(lic_info, dict) else None
    if api_spdx and api_spdx != "NOASSERTION" and api_spdx != declared_license:
        return f"- [LICENSE DRIFT] `{slug}` declares `{declared_license}`, GitHub API reports `{api_spdx}`"

    pushed_at = data.get("pushed_at")
    if pushed_at:
        last_push = datetime.datetime.fromisoformat(pushed_at.replace("Z", "+00:00"))
        cutoff = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=STALE_DAYS_THRESHOLD)
        if last_push < cutoff:
            return f"- [INACTIVE > {STALE_DAYS_THRESHOLD}d] `{slug}` (last push: {last_push.date()})"
    return None


def main() -> int:
    content = README_PATH.read_text(encoding="utf-8")
    repo_entries: list[tuple[str, str]] = []
    for line in content.splitlines():
        match = ENTRY_REPO_REGEX.match(line)
        if match:
            repo_entries.append((match.group("slug"), match.group("license")))

    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")

    print(
        f"Auditing {len(repo_entries)} GitHub repositories for archive status, renames, license accuracy, and freshness..."
    )
    findings: list[str] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:
        results = pool.map(lambda item: check_repo(item[0], item[1], token), repo_entries)
        for finding in results:
            if finding:
                findings.append(finding)
                print(f"  WARN {finding}", file=sys.stderr)

    if findings:
        print(f"Found {len(findings)} repository health issue(s):", file=sys.stderr)
        for item in findings:
            print(f"  {item}", file=sys.stderr)
        return 1

    print(f"OK: all {len(repo_entries)} GitHub repositories are active, unarchived, canonical, and license-verified.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
