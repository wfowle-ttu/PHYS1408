"""Shared helpers for PHYS1408 Exam 3 practice exams (Ch 12 Statics, Ch 13 Gravity).

One list of question records -> practice-exam-3-N.qmd + practice-exam-3-N-key.qmd.
Question generators live in gens.py; each returns a record with
  stem, choices (5 display strings), key (letter), check, value, topic,
  source, prev (2015 Exam 3 match or None), card (notecard entry),
  tests (one line), solution (markdown), distract {letter: text}, fig (f(ax) or None).

check is one of
  ("near", value, [5 numbers])   the keyed choice is the nearest (log distance)
  ("max",  value, [5 numbers])   the keyed choice is the largest choice <= value
  ("min",  value, [5 numbers])   the keyed choice is the smallest choice >= value
  ("concept",)

Run build scripts with PYTHONIOENCODING=utf-8.
"""
import math
import random
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

EXAM_DIR = Path(__file__).resolve().parent.parent
LETTERS = "abcde"
plt.rcParams.update({"font.size": 12, "mathtext.fontset": "stix"})

# Constants exactly as printed on the 2015 Exam 3 header (g = 9.8 as in all his notes).
G = 6.67e-11
ME = 5.98e24
RE = 6.37e6
g = 9.8


# ------------------------------------------------------------------ number formatting
def sig(v, n=3):
    """Round v to n significant figures (as a float)."""
    if v == 0:
        return 0.0
    return round(v, -int(math.floor(math.log10(abs(v)))) + (n - 1))


def tex(v, n=3, sci_hi=1e5, sci_lo=1e-3):
    """LaTeX (no $) for a number rounded to n sig figs; scientific outside [sci_lo, sci_hi)."""
    v = sig(v, n)
    a = abs(v)
    if a != 0 and (a >= sci_hi or a < sci_lo):
        e = int(math.floor(math.log10(a)))
        m = v / 10 ** e
        ms = f"{m:.{n - 1}f}"
        if float(ms) == 10.0:
            e += 1
            ms = f"{v / 10 ** e:.{n - 1}f}"
        return rf"{ms}\times10^{{{e}}}"
    if a >= 10 ** (n - 1):
        return f"{v:,.0f}".replace(",", "{,}")
    dec = max(0, n - 1 - int(math.floor(math.log10(a)))) if a else 0
    return f"{v:.{dec}f}"


def plain(v, n=3):
    """Plain-text version of tex() for answer choices (no math needed for ordinary numbers)."""
    t = tex(v, n)
    return f"${t}$" if "times" in t else t.replace("{,}", ",")


def U(value, label):
    r"""\underbrace{value}_{\text{label}}"""
    return rf"\underbrace{{{value}}}_{{\text{{{label}}}}}"


# ------------------------------------------------------------------ choice building
def numeric(correct, mistakes, target, unit, n=3, scale=1.0, gap=0.12, fill=1.4, cap=None):
    """Build 5 sorted numeric choices with the correct value at letter `target`.

    mistakes: list of (value, explanation), in priority order. Values are in the
    same units as `correct`; `scale` converts to display units.
    Returns (choices, nums, distract) where nums are the display numbers.
    """
    k = LETTERS.index(target)
    c = sig(correct * scale, n)

    def far(v, others):
        return all(abs(math.log(v / o)) > gap for o in others)

    below, above = [], []
    for v, why in mistakes:
        if v is None or v <= 0:
            continue
        d = sig(v * scale, n)
        if not far(d, [c] + [b[0] for b in below + above]):
            continue
        if d < c and len(below) < k:
            below.append((d, why))
        elif d > c and len(above) < 4 - k:
            above.append((d, why))
    filler = "No standard mistake gives this value; it is a spacing choice."
    while len(below) < k:
        lo = min([c] + [b[0] for b in below])
        below.append((sig(lo / fill, n), filler))
    need = 4 - k - len(above)
    hi = max([c] + [b[0] for b in above])
    if cap is not None and need and hi * fill ** need >= cap:
        # spread evenly between the top choice and the cap (angles under 90°, percentages under 100%)
        taken = [c] + [b[0] for b in above]
        top = max(taken)
        step = (cap - top) / (need + 1)
        for j in range(1, need + 1):
            above.append((sig(top + j * step, n), filler))
    while len(above) < 4 - k:
        hi = max([c] + [b[0] for b in above])
        above.append((sig(hi * fill, n), filler))
    items = sorted(below + [(c, None)] + above)
    choices, nums, distract = [], [], {}
    for i, (d, why) in enumerate(items):
        choices.append(f"{plain(d, n)}{'' if unit in ('°', '%') else ' '}{unit}".strip())
        nums.append(d)
        if why:
            distract[LETTERS[i]] = why
    assert items[k][1] is None, (items, k)
    return choices, nums, distract


def grid(value, target, step, unit, mode, n=3, fmt=None):
    """Choices on an even grid (professor style) for a maximum or minimum question.

    mode "max": keyed = largest grid value <= value.  mode "min": smallest >= value.
    """
    k = LETTERS.index(target)
    if mode == "max":
        base = math.floor(value / step + 1e-9) * step
    else:
        base = math.ceil(value / step - 1e-9) * step
    frac = abs(value - base) / step
    assert 0.08 < frac < 0.92 or abs(value - base) < 1e-12, f"value {value} too close to a grid line"
    nums = [round(base + (i - k) * step, 10) for i in range(5)]
    assert nums[0] > 0, nums
    f = fmt or (lambda v: plain(v, n))
    choices = [f"{f(v)} {unit}".strip() for v in nums]
    distract = {}
    for i, v in enumerate(nums):
        if i == k:
            continue
        if mode == "max":
            distract[LETTERS[i]] = ("works, but it is not the largest choice that works." if v < value
                                    else "is more than the maximum, so it fails.")
        else:
            distract[LETTERS[i]] = ("is below the minimum, so it fails." if v < value
                                    else "works, but it is not the smallest choice that works.")
    return choices, nums, distract


def place_text(correct, wrong, target):
    """Text choices: correct goes at `target`; wrong = list of (text, why) in order."""
    k = LETTERS.index(target)
    order = list(wrong)
    choices, distract = [], {}
    for i in range(5):
        if i == k:
            choices.append(correct)
        else:
            t, why = order.pop(0)
            choices.append(t)
            distract[LETTERS[i]] = why
    return choices, distract


def S(f, **kw):
    """A question spec: generator + its numbers. The answer letter is chosen later by assemble()."""
    return (f, kw)


def assemble(specs, seed, tries=4000):
    """Pick balanced answer letters that let the distractors be real mistakes.

    For each question and each letter, count the 'spacing' filler choices that letter would force.
    Then search seeded random balanced letter assignments and keep the one with the fewest fillers.
    """
    cost = []
    for f, kw in specs:
        row = []
        for L in LETTERS:
            q = f(L, **kw)
            row.append(sum("spacing choice" in d for d in q.get("distract", {}).values()))
        cost.append(row)
    rng = random.Random(seed)
    best, best_keys = None, None
    base = list(LETTERS) * (len(specs) // 5)
    for _ in range(tries):
        rng.shuffle(base)
        c = sum(cost[i][LETTERS.index(L)] for i, L in enumerate(base))
        if best is None or c < best:
            best, best_keys = c, list(base)
    # local improvement: swap pairs while it lowers the cost
    improved = True
    while improved:
        improved = False
        for i in range(len(specs)):
            for j in range(i + 1, len(specs)):
                a, b = best_keys[i], best_keys[j]
                if a == b:
                    continue
                d = (cost[i][LETTERS.index(b)] + cost[j][LETTERS.index(a)]
                     - cost[i][LETTERS.index(a)] - cost[j][LETTERS.index(b)])
                if d < 0:
                    best_keys[i], best_keys[j] = b, a
                    best += d
                    improved = True
    print(f"filler choices in this exam: {best}")
    return [f(L, **kw) for (f, kw), L in zip(specs, best_keys)]


def letters(n_q, seed):
    """Balanced answer letters: n_q/5 of each, shuffled with a fixed seed."""
    assert n_q % 5 == 0
    keys = list(LETTERS) * (n_q // 5)
    random.Random(seed).shuffle(keys)
    return keys


# ------------------------------------------------------------------ checking
def check_question(num, q):
    kind = q["check"][0]
    key = q["key"]
    if kind == "near":
        _, value, nums = q["check"]
        dist = [abs(math.log(c / value)) for c in nums]
        best = LETTERS[dist.index(min(dist))]
        second = sorted(dist)[1]
        ok = best == key and second > 2 * min(dist) and second > 0.06
        msg = f"computed {value:.5g}, nearest {best}"
    elif kind == "max":
        _, value, nums = q["check"]
        ok_c = [(c, LETTERS[i]) for i, c in enumerate(nums) if c <= value]
        best = max(ok_c)[1] if ok_c else None
        ok = best == key
        msg = f"computed {value:.5g} (max) -> {best}"
    elif kind == "min":
        _, value, nums = q["check"]
        ok_c = [(c, LETTERS[i]) for i, c in enumerate(nums) if c >= value]
        best = min(ok_c)[1] if ok_c else None
        ok = best == key
        msg = f"computed {value:.5g} (min) -> {best}"
    elif kind == "concept":
        ok, msg = True, "concept"
    else:
        raise ValueError(kind)
    assert len(q["choices"]) == 5 and len(set(q["choices"])) == 5, q["choices"]
    print(f"{'OK ' if ok else 'FAIL'} Q{num:>2}: {key}) {q['choices'][LETTERS.index(key)]}  [{msg}]")
    return ok


# ------------------------------------------------------------------ writing
CONSTANTS = (
    r"$G = 6.67\times10^{-11}\ \tfrac{\text{N m}^2}{\text{kg}^2}$ $\qquad$ "
    r"$M_{earth} = 5.98\times10^{24}$ kg $\qquad$ $R_{earth} = 6.37\times10^{6}$ m $\qquad$ "
    r"$g = 9.8\ \text{m/s}^2$"
)


def _fig_md(n, i, q):
    w = q.get("figwidth", "2.6in")
    return f"![](figures/3-{n}/q{i:02d}.png){{width={w} fig-align=\"center\"}}"


def write_exam(n, qs, label="Practice Exam"):
    slug = label.lower().replace(" ", "-")
    out = [
        "---",
        f'title: "PHYS1408 {label} 3-{n}"',
        f'subtitle: "Chapters 12 (Statics) and 13 (Gravity) — {len(qs)} multiple-choice questions"',
        "format:",
        "  pdf:",
        "    papersize: letter",
        "    fontsize: 11pt",
        "    fig-pos: H",
        "    include-in-header:",
        "      text: |",
        "        \\usepackage{needspace}",
        "        \\usepackage{array}",
        "---",
        "",
        CONSTANTS,
        "",
        "**Instructions.** Choose the single best answer (a–e). Answers are rounded; pick the nearest choice. "
        "For a **maximum** (\"how far can he safely…\"), pick the largest choice that still works; for a "
        "**minimum**, the smallest choice that still works. A calculator and your 3×5 notecard are allowed.",
        "",
    ]
    for i, q in enumerate(qs, 1):
        need = 14 if q.get("fig") else 10
        out += ["```{=latex}", f"\\needspace{{{need}\\baselineskip}}", "```"]
        if q.get("fig"):
            w = q.get("layout", 64)
            out += [f'::: {{layout="[{w},{100 - w}]" layout-valign="top"}}', "::: {}"]
        out += [f"**{i}.** {q['stem'].strip()}", ""]
        out += ["```{=latex}", "\\begingroup\\leftskip=1.5em", "```"]
        out += [f"{L})\\ {c}\\" if j < 4 else f"{L})\\ {c}" for j, (L, c) in enumerate(zip(LETTERS, q["choices"]))]
        out += ["", "```{=latex}", "\\par\\endgroup", "```", ""]
        if q.get("fig"):
            out += [":::", "", f"![](figures/3-{n}/q{i:02d}.png)", ":::", ""]
        out += ["```{=latex}", "\\medskip", "```", ""]
    (EXAM_DIR / f"{slug}-3-{n}.qmd").write_text("\n".join(out), encoding="utf-8")


def write_key(n, qs, intro, label="Practice Exam", script=None):
    slug = label.lower().replace(" ", "-")
    out = [
        "---",
        f'title: "PHYS1408 {label} 3-{n} — Answer Key"',
        'subtitle: "Worked solutions with course-material citations"',
        "format:",
        "  pdf:",
        "    papersize: letter",
        "    fontsize: 11pt",
        "    fig-pos: H",
        "    include-in-header:",
        "      text: |",
        "        \\usepackage{longtable,array,colortbl,cancel,needspace}",
        "filters:",
        "  - _filters/tables.lua",
        "---",
        "",
        f"Every numeric answer was computed and checked in `_scripts/{script or f'build_{slug}_3_{n}.py'}`. "
        "Constants are the ones printed on the 2015 Exam 3: $G = 6.67\\times10^{-11}$, "
        "$M_{earth} = 5.98\\times10^{24}$ kg, $R_{earth} = 6.37\\times10^{6}$ m, and $g = 9.8$ m/s².",
        "",
        "**Sources.** \"Ch 12 notes p. 6/10\" means page 6 of the professor's *Chapter 12 Statics* notes "
        "(he numbers his pages \"6/10\"). \"2015 Exam 3 #2\" is question 2 of the previous exam in "
        "`Professors-Notes/exam 3-4.pdf`.",
        "",
        intro.strip(),
        "",
        "| Q | Ans | Answer | Type | Topic (source) | Notecard |",
        "|:-:|:-:|:--|:--|:--|:--|",
    ]
    for i, q in enumerate(qs, 1):
        ans = q["choices"][LETTERS.index(q["key"])]
        typ = "Concept" if q["check"][0] == "concept" else ("Max" if q["check"][0] == "max" else
                                                            "Min" if q["check"][0] == "min" else "Calc")
        out.append(f"| {i} | **{q['key']}** | {ans} | {typ} | {q['topic']} ({q['source_short']}) | {q['card']} |")
    out.append("")
    for i, q in enumerate(qs, 1):
        ans = q["choices"][LETTERS.index(q["key"])]
        out += ["```{=latex}", "\\needspace{8\\baselineskip}", "```",
                f"# {i}. {q['topic']} — **{q['key']}) {ans}**", "",
                f"**Source:** {q['source']}  ",
                f"**Previous-exam match:** {q.get('prev') or 'none (lecture-notes example)'}  ",
                f"**Notecard:** {q['card']}  ",
                f"**What it tests:** {q['tests']}", ""]
        if q.get("fig"):
            out += [_fig_md(n, i, q), ""]
        out += [q["solution"].strip(), ""]
        if q.get("distract"):
            out += ["Why the other choices are wrong:", ""]
            for L in LETTERS:
                if L in q["distract"]:
                    out.append(f"* {L}) {q['choices'][LETTERS.index(L)]}: {q['distract'][L]}")
            out.append("")
    (EXAM_DIR / f"{slug}-3-{n}-key.qmd").write_text("\n".join(out), encoding="utf-8")


def draw_figures(n, qs):
    d = EXAM_DIR / "figures" / f"3-{n}"
    d.mkdir(parents=True, exist_ok=True)
    for i, q in enumerate(qs, 1):
        if not q.get("fig"):
            continue
        fig, ax = plt.subplots(figsize=q.get("figsize", (4.0, 2.0)))
        ax.set_aspect("equal")
        ax.axis("off")
        q["fig"](ax)
        fig.savefig(d / f"q{i:02d}.png", dpi=220, bbox_inches="tight", pad_inches=0.04)
        plt.close(fig)


def build(n, qs, intro, label="Practice Exam", script=None):
    ok = all(check_question(i, q) for i, q in enumerate(qs, 1))
    keys = [q["key"] for q in qs]
    print("Key:", " ".join(keys), "| counts:", {L: keys.count(L) for L in LETTERS})
    assert ok, "a check failed"
    assert len(set(keys.count(L) for L in LETTERS)) == 1, "letters not balanced"
    draw_figures(n, qs)
    write_exam(n, qs, label)
    write_key(n, qs, intro, label, script)
    print(f"Wrote {label} 3-{n} (+ key, figures)")
