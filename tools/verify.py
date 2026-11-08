#!/usr/bin/env python3
"""Verification for the ADHD Task Paralysis Handbook.

Dependency-free checks:
  1. Every relative Markdown link resolves to an existing file.
  2. site/index.html parses as valid, well-formed-ish HTML and every
     href/src reference points at a real local file (no network deps).
  3. The printable ladder card exists with all 10 rungs.
  4. LICENSE carries the exact required copyright line.
  5. No secrets-looking strings in tracked text files.
"""

import html.parser
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FAILS = []
CHECKS = []


def check(name, ok, detail=""):
    CHECKS.append((name, ok, detail))
    if not ok:
        FAILS.append(f"{name}: {detail}")


def md_links(md_path):
    text = md_path.read_text(encoding="utf-8")
    for match in re.finditer(r"\[([^\]]*)\]\(([^)]+)\)", text):
        url = match.group(2).strip()
        if url.startswith(("http://", "https://", "mailto:", "#")):
            continue
        yield url


def verify_markdown_links():
    md_files = list(ROOT.glob("docs/*.md")) + [ROOT / "README.md"]
    check("markdown files present", len(md_files) >= 9, f"found {len(md_files)}")
    broken = []
    for md in filter(Path.is_file, md_files):
        for url in md_links(md):
            target = (md.parent / url.split("#")[0]).resolve()
            if not target.is_file():
                broken.append(f"{md.name} -> {url}")
    check("all markdown links resolve", not broken, "; ".join(broken) or "ok")


class RefCollector(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.refs = []
        self.scripts = []
        self.stack = []
        self.errors = []

    VOID = {
        "area", "base", "br", "col", "embed", "hr", "img", "input",
        "link", "meta", "source", "track", "wbr",
    }

    def handle_starttag(self, tag, attrs):
        if tag in self.VOID:
            return
        self.stack.append(tag)
        for attr, value in attrs:
            if attr in ("href", "src") and value:
                self.refs.append(value)
        if tag == "script":
            # inline scripts: baseline is empty (print button uses onclick)
            self.scripts.append("")

    def handle_endtag(self, tag):
        if tag in self.VOID:
            return
        if not self.stack or self.stack[-1] != tag:
            self.errors.append(f"mismatched </{tag}> (open: {self.stack[-3:]})")
        else:
            self.stack.pop()


def verify_site():
    html_path = ROOT / "site" / "index.html"
    css_path = ROOT / "site" / "style.css"
    check("site/index.html exists", html_path.is_file())
    check("site/style.css exists", css_path.is_file())
    if not (html_path.is_file() and css_path.is_file()):
        return

    raw = html_path.read_text(encoding="utf-8")

    parser = RefCollector()
    try:
        parser.feed(raw)
        parser.close()
        well_formed = not parser.errors and not parser.stack
    except Exception as exc:  # pragma: no cover
        well_formed = False
        parser.errors.append(str(exc))
    check(
        "site/index.html is well-formed HTML",
        well_formed,
        "; ".join(parser.errors) or ("unclosed: %s" % parser.stack if parser.stack else "ok"),
    )

    missing = []
    external = []
    for ref in parser.refs:
        if ref.startswith(("http://", "https://", "//")):
            external.append(ref)
        elif not ref.startswith("#") and not (ROOT / "site" / ref).is_file():
            missing.append(ref)
    check("site references only existing local files", not missing, "; ".join(missing) or "ok")
    check("site loads nothing from the network", not external, "; ".join(external) or "ok")

    check(
        "no <script> includes in site (print button is attribute-only)",
        "<script" not in raw.lower(),
    )

    # CSS sanity + print rules present
    css = css_path.read_text(encoding="utf-8")
    check("style.css is non-trivial", len(css) > 2000, f"{len(css)} bytes")
    check("print stylesheet exists (@media print)", "@media print" in css)
    check("print styles hide chapter cards", ".cards" in css and "display: none" in css)

    # the ladder card on the site has all ten rungs
    rungs = re.findall(r"Rung (\d+)", raw)
    check("ladder card has rungs 1-10", sorted(map(int, rungs)) == list(range(1, 11)),
          f"found rungs {sorted(set(map(int, rungs)))}")

    # relative doc links from the site resolve
    doc_missing = [r for r in parser.refs if r.startswith("../docs/")
                   and not (ROOT / "site" / r).resolve().is_file()]
    check("site chapter links resolve to docs/", not doc_missing, "; ".join(doc_missing) or "ok")


def verify_license():
    lic = ROOT / "LICENSE"
    check("LICENSE exists", lic.is_file())
    if lic.is_file():
        text = lic.read_text(encoding="utf-8")
        check("LICENSE copyright line is exact",
              "Copyright (c) 2026 Asdale Dynamics, LLC" in text)
        check("LICENSE is MIT", "MIT License" in text)


def verify_readme():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    check("README credits Asdale Dynamics, LLC", "Asdale Dynamics, LLC" in readme)
    check("README explains how to run the site", "http.server" in readme)


def verify_no_secrets():
    pattern = re.compile(
        r"(sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|"
        r"-----BEGIN [A-Z ]*PRIVATE KEY-----|xox[bap]-[A-Za-z0-9-]{10,})",
    )
    hits = []
    for path in list(ROOT.glob("docs/*")) + list(ROOT.glob("site/*")) + \
            [ROOT / "README.md", ROOT / "LICENSE", Path(__file__)]:
        if not path.is_file():
            continue
        if pattern.search(path.read_text(encoding="utf-8", errors="ignore")):
            hits.append(path.name)
    check("no secret-shaped strings in repo", not hits, "; ".join(hits) or "ok")


def main():
    verify_markdown_links()
    verify_site()
    verify_license()
    verify_readme()
    verify_no_secrets()

    passed = sum(1 for _, ok, _ in CHECKS if ok)
    print(f"Verification: {passed}/{len(CHECKS)} checks passed\n")
    for name, ok, _ in CHECKS:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    if FAILS:
        print("\nFailures:")
        for f in FAILS:
            print(f"  - {f}")
        return 1
    print("\nAll good. (JUnit-free, dependency-free, coffee-free.)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
