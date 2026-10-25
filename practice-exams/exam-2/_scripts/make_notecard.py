"""Build notecard-exam-2.qmd from the notecards in study-guide-exam-2-worked.qmd.

Run:  python practice-exams/exam-2/_scripts/make_notecard.py
(after rendering the worked guide, so its HTML section anchors exist)

Each card comes from the worked guide's "The 3×5 notecard" summary section, so
the two documents can't drift apart. Every card links to the worked sections it
covers.
"""
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
QMD = HERE / "study-guide-exam-2-worked.qmd"
HTML = HERE / "study-guide-exam-2-worked.html"
OUT = HERE / "notecard-exam-2.qmd"
WORKED = "study-guide-exam-2-worked.html"

qmd = QMD.read_text(encoding="utf-8")
html = HTML.read_text(encoding="utf-8")

# section number (e.g. "7.12", "R.1") -> html anchor id
anchors = {}
for m in re.finditer(r'<section id="([^"]+)" class="level2"[^>]*>\s*<h2[^>]*>(.*?)</h2>', html, re.S):
    title = re.sub(r"<[^>]+>", "", m.group(2)).strip()
    num = re.match(r"((?:\d+|R)\.\d+)\s", title)
    if num:
        anchors[num.group(1)] = m.group(1)


def expand(refs):
    """'7.5–7.8, R.2' -> ['7.5', '7.6', '7.7', '7.8', 'R.2']"""
    out = []
    for part in [p.strip() for p in refs.split(",")]:
        rng = re.match(r"(\w+)\.(\d+)[–-](\w+)\.(\d+)$", part)
        if rng and rng.group(1) == rng.group(3):
            out += [f"{rng.group(1)}.{k}" for k in range(int(rng.group(2)), int(rng.group(4)) + 1)]
        else:
            out.append(part)
    return out


summary = re.search(r"^# The 3×5 notecard: every formula in one place\n(.*?)(?=^# )", qmd, re.M | re.S).group(1)
cards = re.findall(r"^## (.+?) \(([^)]*)\)\n\n::: \{\.callout-tip title=\"Notecard\"\}\n(.*?)\n:::", summary, re.M | re.S)
assert len(cards) >= 19, len(cards)

# order cards by chapter, the way the course runs
def first_key(refs):
    n = expand(refs)[0]
    ch, sec = n.split(".")
    return (100 if ch == "R" else int(ch), int(sec))

cards.sort(key=lambda c: first_key(c[1]))

lines = [
    "---",
    'title: "PHYS1408 Exam 2 Notecard"',
    'subtitle: "Every 3×5 notecard equation, one card per problem type"',
    "format:",
    "  html:",
    "    embed-resources: true",
    "    toc: true",
    "    toc-depth: 1",
    "  pdf:",
    "    geometry: margin=0.6in",
    "    fontsize: 10pt",
    "    toc: false",
    "---",
    "",
    "$g = 9.8$ m/s². Each card's links go to the fully worked problems in the "
    f"[Exam 2 Worked Problems]({WORKED}). For a minimum, round **up** to an answer choice that works; for a maximum, round **down**.",
    "",
]

missing = []
for title, refs, body in cards:
    nums = expand(refs)
    links = []
    for n in nums:
        if n in anchors:
            links.append(f"[{n}]({WORKED}#{anchors[n]})")
        else:
            missing.append(n)
            links.append(n)
    # keep the equations and symbol definitions; drop the "Covers" line
    body = re.sub(r"^\*\*Covers:\*\*.*$", "", body, flags=re.M).strip()
    lines += [f"# {title}", "", "**Worked examples:** " + " · ".join(links), "", body, ""]

OUT.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
print(f"wrote {OUT.name}: {len(cards)} cards; missing anchors: {missing}")
