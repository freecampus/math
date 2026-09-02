#!/usr/bin/env python3
"""Smoke-test rendered HTML, links, IDs, image text alternatives, and identity."""

from __future__ import annotations

import argparse
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
QUARTO_DUPLICATE_IDS = {
    "quarto-bootstrap",
    "quarto-search",
    "quarto-text-highlighting-styles",
}


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []
        self.ids: list[str] = []
        self.images_without_alt = 0
        self.html_language = ""
        self.main_count = 0
        self.h1_count = 0
        self.has_skip_link = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "html":
            self.html_language = str(values.get("lang", "")).strip()
        if tag == "main":
            self.main_count += 1
        if tag == "h1":
            self.h1_count += 1
        if values.get("id"):
            self.ids.append(str(values["id"]))
        if tag == "a" and values.get("href"):
            self.links.append(str(values["href"]))
            if values["href"] == "#quarto-document-content":
                self.has_skip_link = True
        if tag == "img" and "alt" not in values:
            self.images_without_alt += 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("site", type=Path, nargs="?", default=ROOT / "build")
    args = parser.parse_args()
    site = args.site.resolve()
    errors: list[str] = []
    html_files = sorted(site.rglob("*.html"))
    if not html_files:
        errors.append(f"{site}: no rendered HTML files")
    parsed: dict[Path, PageParser] = {}
    for path in html_files:
        content = path.read_text(encoding="utf-8")
        page = PageParser()
        page.feed(content)
        parsed[path] = page
        duplicates = {
            value
            for value in page.ids
            if page.ids.count(value) > 1 and value not in QUARTO_DUPLICATE_IDS
        }
        if duplicates:
            errors.append(
                f"{path.relative_to(site)}: duplicate HTML IDs {sorted(duplicates)}"
            )
        if page.images_without_alt:
            relative = path.relative_to(site)
            errors.append(
                f"{relative}: {page.images_without_alt} image(s) lack alt attributes"
            )
        relative = path.relative_to(site)
        if not page.html_language:
            errors.append(f"{relative}: HTML language is missing")
        if page.main_count != 1:
            errors.append(f"{relative}: expected one main landmark")
        if not page.h1_count:
            errors.append(f"{relative}: page has no level-one heading")
        if not page.has_skip_link:
            errors.append(f"{relative}: page has no main-content skip link")
        if re.search(r"osl-incubator|osl-edu-math|>edu-math<", content, re.IGNORECASE):
            errors.append(f"{path.relative_to(site)}: stale project identity")

    for source, page in parsed.items():
        for href in page.links:
            split = urlsplit(href)
            if (
                split.scheme
                or split.netloc
                or href.startswith(("mailto:", "javascript:"))
            ):
                continue
            path_text = unquote(split.path)
            if not path_text:
                target = source
            elif path_text.startswith("/"):
                target = site / path_text.lstrip("/")
            else:
                target = source.parent / path_text
            if target.is_dir():
                target = target / "index.html"
            if target.suffix == "":
                target = target.with_suffix(".html")
            if not target.exists():
                errors.append(f"{source.relative_to(site)}: broken link {href!r}")
                continue
            if split.fragment and target.suffix == ".html":
                target_page = parsed.get(target.resolve())
                if target_page is None:
                    target_page = PageParser()
                    target_page.feed(target.read_text(encoding="utf-8"))
                    parsed[target.resolve()] = target_page
                if split.fragment not in target_page.ids:
                    errors.append(
                        f"{source.relative_to(site)}: missing anchor {href!r}"
                    )

    scratch = list((ROOT / "docs/.quarto").glob("quarto-session-temp*"))
    if scratch:
        errors.append(
            "temporary Quarto session directories remain: "
            + ", ".join(str(path) for path in scratch)
        )
    if errors:
        print("\n".join(errors))
        return 1
    manifest = {
        "html_pages": len(html_files),
        "checked_links": sum(len(page.links) for page in parsed.values()),
    }
    print(json.dumps(manifest, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
