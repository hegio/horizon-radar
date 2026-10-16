#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Convert a Horizon daily briefing into a click-to-expand page.

Each news item becomes a <details> block: click the title to expand the
detail (summary / background / impact / tags). Adds Jekyll front matter
(the data/summaries source has none) and cleans Horizon's markdown-escaped
HTML entities (&\\#x27; -> ').

Usage: make_collapsible.py <src.md> <dst.md>
"""
import html
import pathlib
import re
import sys


def clean(text: str) -> str:
    """Undo Horizon's double-escaped entities: &\\#x27; -> ' etc."""
    text = text.replace("\\#", "#")
    return html.unescape(text)


def front_matter_for(dst: pathlib.Path) -> str:
    m = re.search(r"(\d{4}-\d{2}-\d{2})-summary-([A-Za-z-]+)\.md$", dst.name)
    if not m:
        return ""
    date, lang = m.group(1), m.group(2)
    return (
        "---\n"
        'layout: default\n'
        f'title: "Horizon Summary: {date} ({lang.upper()})"\n'
        f"date: {date}\n"
        f"lang: {lang}\n"
        "---\n\n"
    )


def convert(text: str, dst: pathlib.Path) -> str:
    m = re.match(r"\A(---\n.*?\n---\n)(.*)\Z", text, re.S)
    front, body = (m.group(1), m.group(2)) if m else (front_matter_for(dst), text)

    hm = re.search(r"(?m)^> .*$", body)
    header_line = hm.group(0) if hm else ""

    g = re.search(r"(?m)^## .*$", body)
    if not g:
        return front + clean(body)
    rest = body[g.start():]

    item_pat = re.compile(
        r'(<a id="item-[^"]+"></a>\n###[^\n]+\n.*?)(?=\n<a id="item-|\n## |\Z)', re.S)
    group_pat = re.compile(r"(?m)^(## [^\n]+)\s*$")

    parts = re.split(group_pat, rest)
    # parts: ['', '## g1', content1, '## g2', content2, ...]
    out = [header_line, ""]
    for i in range(1, len(parts), 2):
        heading = parts[i]
        content = parts[i + 1] if i + 1 < len(parts) else ""
        out += [heading, ""]
        for block in item_pat.findall(content):
            lines = block.rstrip().split("\n")
            heading_line = lines[1] if len(lines) > 1 else ""
            body_md = clean("\n".join(lines[2:]).strip())
            m2 = re.match(r"### (.+?) (⭐️ ?[0-9.?]+/10)\s*$", heading_line)
            if m2:
                title = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", m2.group(1))
                title = html.unescape(title.replace("\\", "")).strip()
                summary = f"{title} {m2.group(2)}"
            else:
                summary = clean(heading_line[4:].strip())
            out += [
                '<details markdown="1">',
                f"<summary><strong>{summary}</strong></summary>",
                "",
                body_md,
                "",
                "</details>",
                "",
            ]
    return front + "\n".join(out).rstrip() + "\n"


def main() -> None:
    if len(sys.argv) != 3:
        print("usage: make_collapsible.py <src.md> <dst.md>")
        sys.exit(1)
    src, dst = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
    if not src.exists():
        print(f"WARN: {src} missing; nothing to convert")
        sys.exit(0)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(convert(src.read_text(encoding="utf-8"), dst), encoding="utf-8")
    print(f"collapsible page written: {dst}")


if __name__ == "__main__":
    main()
