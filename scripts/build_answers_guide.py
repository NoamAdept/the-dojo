#!/usr/bin/env python3
"""The Dojo answers guide: one short answer for every challenge.

    python3 scripts/build_answers_guide.py --md      # rewrite docs/answers/<id>.md
    python3 scripts/build_answers_guide.py --check   # fail if docs/answers is out of date
    python3 scripts/build_answers_guide.py --pdf     # dist/the-dojo-answers.pdf

Each answer is the goal (the **Goal:** line of docs/answers/<id>.md), then the files, commands
or task lines from the challenge's solution/ folder, without comments. To say on page 1 that
every answer passed its check, first run scripts/verify_answers.py --json dist/verify.json and
add --report dist/verify.json. The PDF needs node with the playwright package.
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
from academy.ui_flavor import display_title  # noqa: E402

E = html.escape


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


def goal_of(cid: str) -> str:
    path = ANSWERS / f"{cid}.md"
    md = path.read_text() if path.exists() else ""
    m = re.search(r"\*\*Goal[.:]\*\*\s*(.*?)\n\n", md, re.S)
    return " ".join(m.group(1).split()) if m else ""


# ------------------------------------------------------------------ answers


def tidy(lines: list[str]) -> str:
    """No blank lines at the ends, and never two in a row."""
    out: list[str] = []
    for ln in lines:
        ln = ln.rstrip()
        if ln or (out and out[-1]):
            out.append(ln)
    while out and not out[-1]:
        out.pop()
    return "\n".join(out)


def drop_shebang(text: str) -> list[str]:
    """Only the first line's: a #! inside a heredoc is part of the answer."""
    lines = text.splitlines()
    return lines[1:] if lines and lines[0].startswith("#!") else lines


SOLVE_NOISE = ("# Answer used by", "# Prints the flag", "set -euo pipefail", "# data/settings.txt and config.txt are typed")


def clean_code(name: str, text: str) -> str:
    """Drop whole-line comments; keep everything that runs."""
    ext = Path(name).suffix
    hash_comments = ext in (".py", ".sh", ".cmake") or name.endswith("CMakeLists.txt")
    keep = []
    for i, ln in enumerate(text.splitlines()):
        s = ln.strip()
        if hash_comments and s.startswith("#") and not (i == 0 and s.startswith("#!") and ext == ".sh"):
            continue
        if ext in (".cpp", ".h", ".hpp", ".c") and s.startswith("//"):
            continue
        keep.append(ln)
    return tidy(keep)


def answer(ch: dict) -> dict:
    """What a learner types or writes, read from the challenge's verified solution/ folder."""
    sol = ch["_dir"] / "solution"
    files = sorted(p for p in sol.rglob("*") if p.is_file() and "__pycache__" not in p.parts)
    commands, tasks, code = "", [], []
    for p in files:
        rel = p.relative_to(sol).as_posix()
        text = p.read_text()
        if rel == "solve.sh":
            commands = tidy([ln for ln in drop_shebang(text) if not ln.strip().startswith(SOLVE_NOISE)])
        elif re.fullmatch(r"answers/task\d+\.sh", rel):
            tasks.append((int(re.search(r"\d+", p.name).group()), tidy(drop_shebang(text))))
        elif "Instructor stand-in" in text:  # a compiled program: show how to build it instead
            m = re.search(r"themselves with:\s*\n#\s*(.+)", text)
            if m:
                commands = "\n".join(filter(None, [commands, m.group(1).strip(), f"./{rel}"]))
        else:
            code.append((rel, clean_code(rel, text)))
    return {"flag": not (ch["_dir"] / "files" / "check").exists(), "commands": commands,
            "tasks": sorted(tasks), "code": code}


LANG = {".py": "python", ".cpp": "cpp", ".h": "cpp", ".hpp": "cpp", ".sh": "bash", ".cmake": "cmake",
        ".json": "json", ".txt": "text"}


def fence(lang: str, text: str) -> str:
    ticks = "```" if "```" not in text else "````"
    return f"{ticks}{lang}\n{text}\n{ticks}"


def answer_md(ch: dict, belt_label: str) -> str:
    a = answer(ch)
    out = [f"# {display_title(ch['id'], ch['title'])}", "", f"`{ch['id']}` · {belt_label}", "",
           f"**Goal:** {goal_of(ch['id'])}", ""]
    for rel, text in a["code"]:
        lang = "cmake" if rel.endswith("CMakeLists.txt") else LANG.get(Path(rel).suffix, "text")
        out += [f"**File `{rel}`**", "", fence(lang, text), ""]
    if a["commands"]:
        label = ("Type in the challenge folder. The last line shows the flag:" if a["flag"]
                 else "Then type:" if a["code"] else "Type in the challenge folder:")
        out += [label, "", fence("bash", a["commands"]), ""]
    if a["tasks"]:
        out += ["Put each answer in `answers/taskN.sh`, in place of the `TODO` line.", ""]
        for k, text in a["tasks"]:
            out += [f"**Task {k}**", "", fence("bash", text), ""]
    out.append("Paste the flag in the flag box and press **Submit**." if a["flag"]
               else "Run `./check`. It must print `CHECK_OK`. Then press **Mark as done**.")
    return "\n".join(out) + "\n"


def all_md() -> dict[Path, str]:
    return {ANSWERS / f"{ch['id']}.md": answer_md(ch, b["belt_label"])
            for b in belts() for m in b["mods"] for ch in m["challenges"]}


# ------------------------------------------------------------------ PDF

CSS = """
@font-face{font-family:Geist;font-weight:400;src:url(data:font/woff2;base64,{G400})}
@font-face{font-family:Geist;font-weight:600;src:url(data:font/woff2;base64,{G600})}
@font-face{font-family:Geist;font-weight:700;src:url(data:font/woff2;base64,{G700})}
@font-face{font-family:"Geist Mono";font-weight:400;src:url(data:font/woff2;base64,{M400})}
:root{--fg:#14161a;--muted:#5b616b;--line:#dfe2e7;--sunken:#f3f4f6;--accent:#c2410c;--accent-soft:#fff1e8}
*{box-sizing:border-box}
html,body{margin:0;background:#fff;color:var(--fg)}
body{font:400 10pt/1.45 Geist,system-ui,sans-serif;-webkit-print-color-adjust:exact;print-color-adjust:exact}
code,pre{font-family:"Geist Mono",ui-monospace,monospace}
code{font-size:.88em;background:var(--sunken);border-radius:3px;padding:.05em .3em}
b{font-weight:600}
p{margin:0 0 2mm}
.top{border-bottom:2.5px solid var(--fg);padding-bottom:3mm;margin-bottom:4mm;display:flex;justify-content:space-between;align-items:flex-end}
.top h1{margin:0;font-size:25pt;font-weight:700;letter-spacing:-.02em;line-height:1.05}
.top h1 span{color:var(--accent)}
.top p{margin:1.5mm 0 0;font-size:11pt;color:var(--muted)}
.secret{border:1.5px solid var(--accent);background:var(--accent-soft);border-radius:6px;padding:2.6mm 3.6mm;margin:0 0 3mm;font-size:10.5pt}
.box{border:1px solid var(--line);border-radius:6px;padding:2.8mm 3.6mm;margin:0 0 3mm}
.box h3{margin:0 0 1.5mm;font-size:10.5pt}
.legend{display:grid;grid-template-columns:auto 1fr;gap:1.4mm 3.5mm;align-items:baseline}
.legend .k{font-weight:600;white-space:nowrap}
.note{color:var(--muted);font-size:9pt}
h2{font-size:12.5pt;margin:4mm 0 1.5mm}
.tcols{column-count:3;column-gap:5mm;font-size:8.2pt}
.tbelt{font-weight:700;font-size:9.6pt;margin:2.2mm 0 1mm;break-after:avoid}
.tbelt:first-child{margin-top:0}
.tbelt span{font-weight:400;color:var(--muted)}
ol.tlist{list-style:none;padding:0;margin:0 0 2mm}
ol.tlist li{display:flex;gap:1.5mm;padding:.2mm 0;border-bottom:1px dotted var(--line);break-inside:avoid}
ol.tlist .tn{width:5.5mm;text-align:right;color:var(--muted);flex:none}
ol.tlist .tt{flex:1}
ol.tlist .tp{width:5.5mm;text-align:right;flex:none}
.belt{break-before:page}
h2.beltname{font-size:17pt;margin:0 0 1mm;display:flex;align-items:center;gap:3mm;border-bottom:2.5px solid var(--fg);padding-bottom:1.8mm}
h2.beltname small{font-size:10pt;font-weight:400;color:var(--muted);margin-left:auto}
.dot{width:5mm;height:5mm;border-radius:50%;border:1px solid #0003;flex:none}
.cols{column-count:2;column-gap:6mm;column-fill:auto}
.module{color:var(--accent);font-weight:600;letter-spacing:.06em;text-transform:uppercase;font-size:8.4pt;margin:4mm 0 0;break-after:avoid}
.cols .module:first-child{margin-top:2mm}
.ch{padding:2.4mm 0 1.6mm;border-top:1px solid var(--line)}
.module+.ch{border-top:0;padding-top:1mm}
.ch.small{break-inside:avoid}
.ch h3{margin:0 0 .8mm;font-size:10.2pt;font-weight:700;display:grid;grid-template-columns:7mm 1fr auto;column-gap:1.5mm;align-items:baseline;break-after:avoid}
.ch h3 .n{color:var(--accent)}
.ch h3 .cid{font:400 7pt "Geist Mono",monospace;color:var(--muted);white-space:nowrap}
.ch h3 .flag{font-size:7.4pt;font-weight:600;color:#fff;background:var(--accent);border-radius:8px;padding:.2mm 1.8mm;margin-left:1.5mm;text-transform:uppercase}
.ch .goal{margin:0 0 1.4mm;font-size:8.9pt;line-height:1.4}
.ch .lbl{font-size:7.8pt;font-weight:600;color:var(--muted);margin:1.2mm 0 .6mm;break-after:avoid}
.ch .lbl code{font-size:1em;color:var(--fg)}
.ch pre{margin:0 0 1mm;padding:1.4mm 2.2mm;background:var(--sunken);border-radius:4px;font:400 7.3pt/1.36 "Geist Mono",monospace;white-space:pre-wrap;word-break:break-word}
.ch pre .l{display:block;padding-left:calc(var(--i)*1ch);text-indent:calc(var(--i)*-1ch);min-height:1.36em}
table.tasks{width:100%;border-collapse:collapse;margin:0 0 1mm}
table.tasks td{padding:0 0 .8mm;vertical-align:top}
table.tasks td.tn{width:6mm;font:600 7.3pt/1.36 "Geist Mono",monospace;color:var(--accent);padding-top:1.4mm}
table.tasks pre{margin:0}
table.tasks tr{break-inside:avoid}
.howto{break-before:page}
.howto+.belt{break-before:auto;margin-top:4mm}
"""

BELT_COLOR = {"white": "#f7f7f0", "yellow": "#f5c400", "orange": "#f07f13", "blue": "#1f6fd1"}

HOWTO = """<div class="box"><h3>How to read the answers</h3><div class="legend">
<span class="k">File <code>x.py</code></span><span>The finished file. Open it with vim and make it the same. Comments are removed.</span>
<span class="k">Commands</span><span>Type them in the challenge folder (<code>~/dojo/NAME</code>), in this order.</span>
<span class="k">Task 1, 2, 3 …</span><span>Put this in <code>answers/task1.sh</code>, <code>answers/task2.sh</code> … in place of the <code>TODO</code> line.</span>
<span class="k">Then</span><span>Run <code>./check</code>. It must print <code>CHECK_OK</code>. Press <b>Mark as done</b>.</span>
<span class="k" style="color:var(--accent)">FLAG</span><span>The flag is different for each learner, so it is not here.
Run the commands. The last line shows the flag. Paste it in the flag box and press <b>Submit</b>.</span>
</div></div>"""


def inline_md(text: str) -> str:
    out = []
    for p in re.split(r"(`[^`]+`)", text):
        if len(p) > 1 and p.startswith("`") and p.endswith("`"):
            out.append(f"<code>{E(p[1:-1])}</code>")
        else:
            out.append(re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", E(p)))
    return "".join(out)


def code_html(text: str) -> str:
    """One block per line with a hanging indent, so a wrapped line stays under its own code."""
    out = []
    for ln in text.expandtabs(4).splitlines() or [""]:
        n = len(ln) - len(ln.lstrip(" ")) + 2
        out.append(f'<span class="l" style="--i:{n}">{E(ln) or " "}</span>')
    return "".join(out)


def challenge_html(n: int, ch: dict) -> str:
    a = answer(ch)
    body = [f'<p class="goal">{inline_md(goal_of(ch["id"]))}</p>']
    for rel, text in a["code"]:
        body.append(f'<div class="lbl">File <code>{E(rel)}</code></div><pre>{code_html(text)}</pre>')
    if a["commands"]:
        label = ("Commands. The last line shows the flag." if a["flag"] else "Then these commands" if a["code"] else "Commands")
        body.append(f'<div class="lbl">{label}</div><pre>{code_html(a["commands"])}</pre>')
    if a["tasks"]:
        rows = "".join(f'<tr><td class="tn">{k}</td><td><pre>{code_html(t)}</pre></td></tr>' for k, t in a["tasks"])
        body.append(f'<div class="lbl">Put each answer in <code>answers/taskN.sh</code></div><table class="tasks">{rows}</table>')
    lines = sum(t.count("\n") + 1 for t in [a["commands"], *(t for _, t in a["tasks"]), *(t for _, t in a["code"])] if t)
    flag = '<span class="flag">Flag</span>' if a["flag"] else ""
    return (f'<section class="ch{" small" if lines <= 40 else ""}"><h3><span class="n">{n}</span>'
            f'<span>{E(display_title(ch["id"], ch["title"]))}{flag}</span><span class="cid">{E(ch["id"])}</span></h3>'
            f'{"".join(body)}</section>')


def render(pages: dict[str, int] | None, proof: str) -> str:
    """pages: challenge id -> page; {} leaves room for the numbers (first pass), None leaves them out."""
    font = {k: base64.b64encode((FONTS / f).read_bytes()).decode() for k, f in
            {"G400": "Geist-400.woff2", "G600": "Geist-600.woff2", "G700": "Geist-700.woff2", "M400": "GeistMono-400.woff2"}.items()}
    css = CSS
    for k, v in font.items():
        css = css.replace("{" + k + "}", v)
    toc, out, n = [], [], 0
    for b in belts():
        count = sum(len(m["challenges"]) for m in b["mods"])
        toc.append(f'<div class="tbelt">{E(b["belt_label"])} <span>{E(b["title"])}</span></div><ol class="tlist">')
        out.append(f'<section class="belt"><h2 class="beltname"><span class="dot" style="background:{BELT_COLOR.get(b["belt"], "#ccc")}"></span>'
                   f'{E(b["belt_label"])}<small>{E(b["title"])} · {count} challenges</small></h2><div class="cols">')
        for m in b["mods"]:
            out.append(f'<div class="module">{E(m["title"])}</div>')
            for ch in m["challenges"]:
                n += 1
                page = f'<span class="tp">{pages.get(ch["id"], "")}</span>' if pages is not None else ""
                toc.append(f'<li><span class="tn">{n}</span><span class="tt">{E(display_title(ch["id"], ch["title"]))}</span>{page}</li>')
                out.append(challenge_html(n, ch))
        toc.append("</ol>")
        out.append("</div></section>")
    return (f"<!doctype html><html lang='en'><head><meta charset='utf-8'><title>The Dojo answers</title>"
            f"<style>{css}</style></head><body>"
            f'<header class="top"><div><h1>The <span>Dojo</span> · Answers</h1><p>All {n} challenges, in the same order as the page.</p></div></header>'
            f'<div class="secret"><b>This guide has all the answers.</b> Do not give it to learners.</div>{proof}'
            f'<h2>Find a challenge</h2><p class="note">The names are the same as on The Dojo page.'
            f'{" The number on the right is the page." if pages else ""}</p>'
            f'<div class="tcols">{"".join(toc)}</div><div class="howto">{HOWTO}</div>{"".join(out)}</body></html>')


PDF_JS = r"""
const { chromium } = require('playwright');
(async () => {
  const [src, out] = process.argv.slice(2);
  const opts = process.env.CHROMIUM_PATH ? { executablePath: process.env.CHROMIUM_PATH } : {};
  const b = await chromium.launch(opts);
  const p = await b.newPage();
  await p.goto('file://' + src, { waitUntil: 'load' });
  await p.evaluate(() => document.fonts.ready);
  await p.pdf({ path: out, format: 'A4', printBackground: true, outline: true, tagged: true,
    displayHeaderFooter: true, headerTemplate: '<span></span>',
    footerTemplate: '<div style="font-size:7.5pt;color:#6b727d;width:100%;padding:0 13mm;display:flex;justify-content:space-between;font-family:sans-serif">' +
      '<span>The Dojo · Answers · do not give to learners</span><span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>',
    margin: { top: '11mm', bottom: '13mm', left: '13mm', right: '13mm' } });
  await b.close();
})().catch(e => { console.error(e); process.exit(1); });
"""


def to_pdf(html_path: Path, pdf_path: Path) -> None:
    if not shutil.which("node"):
        raise SystemExit("--pdf needs node with the playwright package")
    with tempfile.TemporaryDirectory() as tmp:
        js = Path(tmp) / "pdf.js"
        js.write_text(PDF_JS)
        env = os.environ.copy()
        root = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
        if root:  # let require('playwright') find a global install
            env["NODE_PATH"] = os.pathsep.join(filter(None, [root, env.get("NODE_PATH")]))
        subprocess.run(["node", str(js), str(html_path.resolve()), str(pdf_path.resolve())], check=True, env=env)


def find_pages(pdf: Path) -> dict[str, int]:
    """Page of each challenge: the first page that shows its id (only challenge headings show ids).

    Uses pdftotext (poppler-utils) or PyMuPDF; with neither, returns {} and the list has no page numbers.
    """
    ids = [c["id"] for b in belts() for m in b["mods"] for c in m["challenges"]]
    if shutil.which("pdftotext"):
        texts = subprocess.run(["pdftotext", str(pdf), "-"], capture_output=True, text=True).stdout.split("\f")
    else:
        try:
            import pymupdf
        except ImportError:
            return {}
        texts = [pg.get_text() for pg in pymupdf.open(pdf)]
    found = {}
    for cid in ids:
        pat = re.compile(rf"(?<![\w-]){re.escape(cid)}(?![\w-])")
        page = next((i + 1 for i, t in enumerate(texts) if pat.search(t)), None)
        if page:
            found[cid] = page
    return found if len(found) == len(ids) else {}


# -------------------------------------------------------------------- main


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--md", action="store_true", help="rewrite docs/answers/<id>.md")
    ap.add_argument("--check", action="store_true", help="fail if docs/answers is out of date")
    ap.add_argument("--pdf", action="store_true", help="write dist/the-dojo-answers.pdf")
    ap.add_argument("--report", type=Path, help="JSON from scripts/verify_answers.py --json")
    ap.add_argument("--out", type=Path, default=ROOT / "dist" / "the-dojo-answers.html")
    args = ap.parse_args()

    if args.md or args.check:
        want = all_md()
        stale = sorted(p.name for p, text in want.items() if not p.exists() or p.read_text() != text)
        extra = sorted(p.name for p in ANSWERS.glob("*.md") if p not in want)
        if args.check:
            for name in stale + extra:
                print(f"out of date: docs/answers/{name}")
            if stale or extra:
                print("run: python3 scripts/build_answers_guide.py --md")
                return 1
            print(f"docs/answers: all {len(want)} up to date")
        else:
            for p, text in want.items():
                p.write_text(text)
            for name in extra:
                (ANSWERS / name).unlink()
            print(f"wrote {len(stale)} of {len(want)} answers in docs/answers" + (f", removed {len(extra)}" if extra else ""))
        if not args.pdf:
            return 0

    proof = ""
    if args.report:
        res = json.loads(args.report.read_text())["results"]
        ok = sum(r["status"] == "PASS" for r in res)
        commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
        proof = (f'<p class="note"><b>{ok} of {len(res)} answers pass their own <code>./check</code></b> '
                 f'(scripts/verify_answers.py, {dt.date.today().isoformat()}, commit <code>{commit or "?"}</code>).</p>')
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(render(None, proof))
    if args.pdf:
        pdf = args.out.with_suffix(".pdf")
        args.out.write_text(render({}, proof))
        to_pdf(args.out, pdf)
        pages = find_pages(pdf)  # second pass: fill in the page numbers, or leave them out
        args.out.write_text(render(pages or None, proof))
        to_pdf(args.out, pdf)
        if pages and find_pages(pdf) != pages:
            print("warning: page numbers moved between passes", file=sys.stderr)
        print(f"wrote {pdf}")
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
