#!/usr/bin/env python3
"""Build the instructor answers guide (HTML, and PDF with --pdf) from docs/answers/.

Every challenge in the belts (dojos.yaml `core`) gets one walkthrough from
`docs/answers/<id>.md`, in belt and module order.

Pass the JSON report of scripts/verify_answers.py to stamp each walkthrough:

    python3 scripts/verify_answers.py --json dist/verify.json
    python3 scripts/build_answers_guide.py --report dist/verify.json --pdf
    python3 scripts/build_answers_guide.py --report dist/verify.json --pdf --per-belt dist/belts   # + one PDF per belt

The build also cross-checks each walkthrough against its challenge and prints warnings:
code lines that do not appear in the solution, and a "N/N tasks pass" claim that differs
from what ./check really printed. With --strict those warnings fail the build.

The PDF step needs pandoc, plus node with the playwright package and a Chromium.
"""

from __future__ import annotations

import argparse
import base64
import datetime as dt
import html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CURRICULUM = Path(os.environ.get("ACADEMY_CURRICULUM", ROOT / "curriculum"))
ANSWERS = ROOT / "docs" / "answers"
FONTS = ROOT / "platform" / "academy" / "static" / "fonts"
sys.path[:0] = [str(ROOT / "platform"), str(ROOT / "vendor")]  # vendored PyYAML: no pip needed

from academy.models import load_yaml  # noqa: E402


# ---------------------------------------------------------------- curriculum


def belts() -> list[dict]:
    """Belts in order, each with its modules and their challenges (challenge.yaml dicts)."""
    by_slug = {}
    for mp in (CURRICULUM / "modules").glob("*/module.yaml"):
        m = load_yaml(mp)
        m["_dir"] = mp.parent
        by_slug[m["slug"]] = m
    out = []
    for belt in load_yaml(CURRICULUM / "dojos.yaml")["core"]:
        mods = []
        for slug in belt["modules"]:
            m = by_slug[slug]
            chs = []
            for cid in m.get("challenges") or []:
                y = m["_dir"] / "challenges" / cid / "challenge.yaml"
                if y.exists():
                    c = load_yaml(y)
                    c["_dir"] = y.parent
                    chs.append(c)
            mods.append({"title": m["title"], "challenges": chs})
        out.append({**belt, "mods": mods})
    return out


_RUNTIME = re.compile(
    r"^(\./|cat |ls|cd |vim |man |python3\b|g\+\+|gdb|make|cmake|pwd|exit|academy |echo \$|printenv|ps |"
    r"\"\$|pgrep|tr |readlink|whoami|\. \./|wc |date|grep -n|tail|head|mkdir|chmod|printf|\w+$|#|//|[{}()\[\];]+$|$)"
)


def _norm(line: str) -> str:
    line = re.sub(r"\s//.*$", "", line)
    line = re.sub(r"\s#\s.*$", "", line)
    return re.sub(r"\s+", "", line)


def cross_check(ch: dict, md: str, result: dict | None) -> list[str]:
    warnings = []
    sol = ch["_dir"] / "solution"
    text = ""
    if sol.is_dir():
        for f in sorted(sol.rglob("*")):
            if f.is_file():
                try:
                    text += f.read_text() + "\n"
                except UnicodeDecodeError:
                    pass
    lines = {_norm(ln) for ln in text.splitlines()}
    blob = "".join(_norm(ln) for ln in text.splitlines())
    missing = []
    for draft, lang, block in re.findall(r"(<!-- draft[^>]*-->\s*)?```(\w*)\n(.*?)```", md, re.S):
        if draft or lang in ("", "text", "console", "output"):
            continue  # a deliberate first draft or sample output, not the answer
        for raw in block.splitlines():
            # `echo 'TEXT' > file` writes TEXT into an answer file: compare TEXT itself.
            m = re.match(r"""^\s*echo\s+(['"]?)(.*)\1\s*>{1,2}\s*\S+\s*$""", raw)
            n = _norm(m.group(2) if m else raw)
            if n and not _RUNTIME.match(raw.strip()) and n not in lines and n not in blob:
                missing.append(raw.strip())
    if missing:
        warnings.append(f"{len(missing)} code line(s) not in solution/, e.g. {missing[0][:70]!r}")
    claims = re.findall(r"(\d+)/(\d+) tasks? pass", md)
    if result and result.get("tasks") and claims and "/".join(claims[-1]) != result["tasks"]:
        warnings.append(f"says {'/'.join(claims[-1])} tasks pass, ./check printed {result['tasks']}")
    return warnings


# ------------------------------------------------------------------ render

CSS = """
@font-face{font-family:Geist;font-weight:400;src:url(data:font/woff2;base64,{G400})}
@font-face{font-family:Geist;font-weight:600;src:url(data:font/woff2;base64,{G600})}
@font-face{font-family:Geist;font-weight:700;src:url(data:font/woff2;base64,{G700})}
@font-face{font-family:"Geist Mono";font-weight:400;src:url(data:font/woff2;base64,{M400})}
:root{--fg:#14161a;--muted:#565d68;--accent:#c2410c;--accent-soft:#fdede4;--ok:#15803d;--ok-soft:#e4f3e8;
  --border:#e1e4e8;--code-bg:#f4f5f7}
@page{size:A4;margin:16mm 16mm 18mm 16mm}
html{background:#fff}
body{font-family:Geist,system-ui,sans-serif;color:var(--fg);font-size:10pt;line-height:1.5;margin:0}
code,pre{font-family:"Geist Mono",ui-monospace,monospace;font-size:8.6pt}
:not(pre)>code{background:var(--code-bg);border-radius:3px;padding:0 .25em}
pre{background:var(--code-bg);border:1px solid var(--border);border-radius:6px;padding:.6em .8em;
  white-space:pre-wrap;word-break:break-word;break-inside:avoid}
pre code{background:none;padding:0}
a{color:var(--accent)}
.cover{height:250mm;display:flex;flex-direction:column;justify-content:center;break-after:page}
.cover .kicker{color:var(--accent);font-weight:600;letter-spacing:.08em;text-transform:uppercase;font-size:9pt}
.cover h1{font-size:34pt;margin:.1em 0 .2em;line-height:1.1}
.cover .subtitle{font-size:16pt;font-weight:600;color:var(--muted);margin-top:.4em}
.cover p{font-size:11pt;color:var(--muted);max-width:140mm}
.cover .proof{margin-top:1.5em;border-left:3px solid var(--ok);background:var(--ok-soft);padding:.8em 1em;
  color:var(--fg);font-size:10pt;max-width:150mm}
.cover .warn{border-left-color:var(--accent);background:var(--accent-soft)}
.toc{break-after:page}
.toc h2{font-size:16pt}
.toc ol{padding-left:2.2em}
.toc li{margin:.15em 0}
.toc .count{color:var(--muted)}
.belt{break-before:page}
.belt>h1{font-size:22pt;margin:0;border-bottom:3px solid var(--accent);padding-bottom:.2em}
.belt>.tagline{color:var(--muted);margin:.4em 0 1em}
.module{color:var(--accent);font-weight:600;letter-spacing:.06em;text-transform:uppercase;font-size:8.5pt;
  margin:2em 0 .4em}
.challenge{break-before:auto;margin-top:1.4em;padding-top:.8em;border-top:1px solid var(--border)}
.challenge h2{font-size:14pt;margin:0 0 .1em}
.challenge h2+p em{color:var(--muted)}
.stamp{display:inline-block;font-size:8.5pt;font-weight:600;border-radius:999px;padding:.1em .7em;
  background:var(--ok-soft);color:var(--ok);margin:.2em 0 .4em}
.stamp.no{background:var(--accent-soft);color:var(--accent)}
.toc a{color:var(--fg);text-decoration:none}
.toc .module{margin-top:1em}
li>p{margin:.3em 0}
"""


def _font(name: str) -> str:
    p = FONTS / name
    return base64.b64encode(p.read_bytes()).decode() if p.exists() else ""


def md_to_html(md: str) -> str:
    p = subprocess.run(
        ["pandoc", "-f", "gfm", "-t", "html", "--no-highlight"],
        input=md, capture_output=True, text=True, check=True,
    )
    return p.stdout


def stamp(result: dict | None) -> str:
    if not result:
        return '<span class="stamp no">Not verified in this build</span>'
    if result["status"] != "PASS":
        return '<span class="stamp no">Answer did NOT pass ./check in this build</span>'
    what = {"flag": "flag accepted by the dojo", None: "CHECK_OK"}.get(result.get("tasks"))
    what = what or f"CHECK_OK, {result['tasks']} tasks"
    return f'<span class="stamp">Verified: answer run in a fresh copy, {what}</span>'


def render(belt_list, docs, results, meta, title="The Dojo<br>answers guide") -> str:
    css = (CSS.replace("{G400}", _font("Geist-400.woff2")).replace("{G600}", _font("Geist-600.woff2"))
              .replace("{G700}", _font("Geist-700.woff2")).replace("{M400}", _font("GeistMono-400.woff2")))
    ids = [c["id"] for b in belt_list for m in b["mods"] for c in m["challenges"]]
    total = len(ids)
    ok = sum(1 for cid in ids if results.get(cid, {}).get("status") == "PASS")
    if results:
        cls = "proof" if ok == total else "proof warn"
        proof = (f'<div class="{cls}"><b>{ok} of {total} answers verified.</b> Each answer in this guide was applied to a '
                 f'fresh copy of its challenge and run through that challenge\'s own <code>./check</code> '
                 f'(or flag check), on {meta["date"]} at commit <code>{meta["commit"]}</code>. '
                 f'Re-run with <code>scripts/verify_answers.py</code>.</div>')
    else:
        proof = '<div class="proof warn">Built without a verification report.</div>'
    parts = [f"<!doctype html><html><head><meta charset='utf-8'><title>The Dojo answers</title>"
             f"<style>{css}</style></head><body>",
             f'<section class="cover"><div class="kicker">Instructor copy · keep away from learners</div>'
             f"<h1>{title}</h1>"
             f"<p>Full, worked answers for all {total} challenges in "
             f"{'the ' + str(len(belt_list)) + ' belts' if len(belt_list) > 1 else 'this belt'}. Each walkthrough gives "
             f"the goal, the ideas it needs, the steps with the exact commands or code, what a passing check "
             f"looks like, and the mistakes learners usually make.</p>{proof}</section>"]
    toc = ['<section class="toc"><h2>Contents</h2><ol>']
    for b in belt_list:
        n = sum(len(m["challenges"]) for m in b["mods"])
        toc.append(f'<li><b>{html.escape(b["belt_label"])}: {html.escape(b["title"])}</b> '
                   f'<span class="count">· {n} challenges</span></li>')
    if len(belt_list) == 1:
        toc = ['<section class="toc"><h2>Contents</h2>']
        for m in belt_list[0]["mods"]:
            toc.append(f'<div class="module">{html.escape(m["title"])}</div><ol>')
            toc += [f'<li><a href="#{c["id"]}">{html.escape(c["title"])}</a></li>' for c in m["challenges"]]
            toc.append("</ol>")
    toc.append("</ol></section>" if len(belt_list) > 1 else "</section>")
    parts += toc
    for b in belt_list:
        parts.append(f'<section class="belt"><h1>{html.escape(b["belt_label"])}: {html.escape(b["title"])}</h1>'
                     f'<p class="tagline">{html.escape(b.get("tagline", ""))}</p>')
        for m in b["mods"]:
            parts.append(f'<div class="module">Module: {html.escape(m["title"])}</div>')
            for ch in m["challenges"]:
                body = md_to_html(docs[ch["id"]])
                body = re.sub(r"(</h2>\s*<p><em>.*?</em></p>)", lambda mm: mm.group(1) + stamp(results.get(ch["id"])),
                              body, count=1, flags=re.S)
                parts.append(f'<article class="challenge" id="{ch["id"]}">{body}</article>')
        parts.append("</section>")
    parts.append("</body></html>")
    return "\n".join(parts)


PDF_JS = r"""
const { chromium } = require('playwright');
(async () => {
  const [src, out] = process.argv.slice(2);
  const opts = {};
  if (process.env.CHROMIUM_PATH) opts.executablePath = process.env.CHROMIUM_PATH;
  const b = await chromium.launch(opts);
  const p = await b.newPage();
  await p.goto('file://' + src, { waitUntil: 'load' });
  const label = process.env.GUIDE_LABEL || 'The Dojo answers guide';
  await p.pdf({ path: out, format: 'A4', printBackground: true, displayHeaderFooter: true,
    headerTemplate: '<span></span>',
    footerTemplate: '<div style="font-size:7pt;color:#6b727d;width:100%;text-align:center;font-family:sans-serif">' +
      label + ' (instructor copy) · <span class="pageNumber"></span>/<span class="totalPages"></span></div>',
    margin: { top: '14mm', bottom: '16mm', left: '14mm', right: '14mm' } });
  await b.close();
})().catch(e => { console.error(e); process.exit(1); });
"""


def to_pdf(html_path: Path, pdf_path: Path, label: str = "") -> None:
    node = shutil.which("node")
    if not node:
        raise SystemExit("--pdf needs node with the playwright package")
    with tempfile.TemporaryDirectory() as tmp:
        js = Path(tmp) / "pdf.js"
        js.write_text(PDF_JS)
        env = os.environ.copy()
        if label:
            env["GUIDE_LABEL"] = label
        # Let `require('playwright')` find a globally installed copy.
        root = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
        if root:
            env["NODE_PATH"] = os.pathsep.join(filter(None, [root, env.get("NODE_PATH")]))
        subprocess.run([node, str(js), str(html_path.resolve()), str(pdf_path.resolve())], check=True, env=env)


# -------------------------------------------------------------------- main


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--report", type=Path, help="JSON from scripts/verify_answers.py --json")
    ap.add_argument("--out", type=Path, default=ROOT / "dist" / "the-dojo-answers.html")
    ap.add_argument("--pdf", action="store_true", help="also write a PDF next to the HTML")
    ap.add_argument("--per-belt", type=Path, metavar="DIR",
                    help="also write one guide per belt into DIR (HTML, and PDF with --pdf)")
    ap.add_argument("--strict", action="store_true", help="fail on cross-check warnings or missing walkthroughs")
    args = ap.parse_args()

    belt_list = belts()
    results = {}
    if args.report:
        results = {r["id"]: r for r in json.loads(args.report.read_text())["results"]}

    docs, problems = {}, []
    for b in belt_list:
        for m in b["mods"]:
            for ch in m["challenges"]:
                path = ANSWERS / f"{ch['id']}.md"
                md = path.read_text() if path.exists() else None
                if md is None:
                    problems.append(f"{ch['id']}: no docs/answers/{ch['id']}.md")
                    md = f"## {ch['title']}\n\n*{ch['id']}*\n\nNo walkthrough yet.\n"
                docs[ch["id"]] = md
                for w in cross_check(ch, md, results.get(ch["id"])):
                    problems.append(f"{ch['id']}: {w}")
                if results and results.get(ch["id"], {}).get("status") != "PASS":
                    problems.append(f"{ch['id']}: answer did not pass ./check in the report")
    known = {cid for b in belt_list for m in b["mods"] for cid in (c["id"] for c in m["challenges"])}
    for orphan in sorted(p.stem for p in ANSWERS.glob("*.md") if p.stem not in known):
        problems.append(f"docs/answers/{orphan}.md: no such challenge in the belts")

    commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    meta = {"date": dt.date.today().isoformat(), "commit": commit or "unknown"}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(render(belt_list, docs, results, meta))
    print(f"wrote {args.out} ({len(docs)} walkthroughs)")
    if args.pdf:
        pdf = args.out.with_suffix(".pdf")
        to_pdf(args.out, pdf)
        print(f"wrote {pdf}")
    if args.per_belt:
        args.per_belt.mkdir(parents=True, exist_ok=True)
        for i, b in enumerate(belt_list, 1):
            name = f"{i}-{b['belt']}-belt-answers"
            out = args.per_belt / f"{name}.html"
            title = (f"{html.escape(b['belt_label'])}<br>answers and walkthroughs"
                     f'<div class="subtitle">{html.escape(b["title"])}</div>')
            out.write_text(render([b], docs, results, meta, title=title))
            print(f"wrote {out}")
            if args.pdf:
                to_pdf(out, out.with_suffix(".pdf"), label=f"The Dojo {b['belt_label']} answers")
                print(f"wrote {out.with_suffix('.pdf')}")
    for p in problems:
        print("WARN", p)
    return 1 if (args.strict and problems) else 0


if __name__ == "__main__":
    raise SystemExit(main())
