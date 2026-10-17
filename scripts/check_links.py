#!/usr/bin/env python3
"""Verify that all HTTPS URLs referenced in README.md resolve with HTTP 2xx/3xx."""

from __future__ import annotations

import concurrent.futures
import pathlib
import re
import sys
import urllib.error
import urllib.request

ROOT_DIR = pathlib.Path(__file__).resolve().parent.parent
README_PATH = ROOT_DIR / "README.md"
URL_REGEX = re.compile(r"\]\((https?://[^)\s]+)\)")
USER_AGENT = "awesome-compliance-as-code-link-checker/1.0 (+https://github.com/fabriziosalmi/awesome-compliance-as-code)"


def check_single_url(url: str, timeout: float = 15.0) -> tuple[str, int, str]:
    """Return (url, status_code, error_message)."""
    for method in ("HEAD", "GET"):
        req = urllib.request.Request(
            url,
            method=method,
            headers={
                "User-Agent": USER_AGENT,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                status = resp.getcode() or 200
                if 200 <= status < 400:
                    return (url, status, "")
        except urllib.error.HTTPError as exc:
            if method == "HEAD" and exc.code in (403, 405, 406, 429):
                continue
            if exc.code == 429:
                return (url, 429, "")
            return (url, exc.code, f"HTTP {exc.code}")
        except Exception as exc:  # noqa: BLE001
            if method == "HEAD":
                continue
            return (url, 0, str(exc))
    return (url, 0, "unreachable")


def main() -> int:
    content = README_PATH.read_text(encoding="utf-8")
    urls = sorted(set(URL_REGEX.findall(content)))
    print(f"Checking {len(urls)} unique URLs in README.md...")

    failures: list[tuple[str, int, str]] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        for url, status, err in pool.map(check_single_url, urls):
            if err:
                failures.append((url, status, err))
                print(f"  FAIL [{status}] {url} ({err})", file=sys.stderr)

    if failures:
        print(f"Link check failed: {len(failures)}/{len(urls)} URL(s) unreachable.", file=sys.stderr)
        return 1

    print(f"OK: all {len(urls)} URL(s) responded cleanly.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
