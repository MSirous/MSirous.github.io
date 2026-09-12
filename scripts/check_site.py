"""Fail the build when a rendered page references a missing local asset or page."""

from __future__ import annotations

import argparse
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse


class ReferenceParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.references: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        if tag in {"a", "link"} and attributes.get("href"):
            self.references.append(attributes["href"] or "")
        if tag in {"img", "script", "source"} and attributes.get("src"):
            self.references.append(attributes["src"] or "")


def local_target(page: Path, site: Path, reference: str) -> Path | None:
    parsed = urlparse(reference)
    if parsed.scheme or parsed.netloc or reference.startswith(("#", "mailto:", "tel:")):
        return None
    path = unquote(parsed.path)
    if not path:
        return None
    target = site / path.lstrip("/") if path.startswith("/") else page.parent / path
    if target.is_dir():
        target /= "index.html"
    return target.resolve()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("site", type=Path)
    args = parser.parse_args()
    site = args.site.resolve()
    missing: list[tuple[Path, str]] = []

    for page in site.rglob("*.html"):
        document = ReferenceParser()
        document.feed(page.read_text(encoding="utf-8"))
        for reference in document.references:
            target = local_target(page, site, reference)
            if target is not None and not target.exists():
                missing.append((page.relative_to(site), reference))

    if missing:
        for page, reference in missing:
            print(f"{page}: missing {reference}")
        return 1

    print(f"Checked {sum(1 for _ in site.rglob('*.html'))} HTML pages: local links OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
