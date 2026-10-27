"""Shared helpers for building PHYS1408 Exam 2 practice exams (2-4 onward).

Each build_exam_2_N.py script lists its questions as dicts. build() then
  1. checks every answer (the keyed choice must be the only one that matches,
     or for a min/max the choice that physically works),
  2. draws the figures,
  3. writes practice-exam-2-N.qmd and practice-exam-2-N-key.qmd.

Question dict fields
  stem      markdown question text
  choices   list of 5 display strings (a-e)
  key       correct letter
  check     one of:
              ("near", value, [5 numbers], tol)   nearest choice, unique within tol
              ("min", value, [5 numbers])         smallest choice >= value
              ("max", value, [5 numbers])         largest choice <= value
              ("stops", v_f_squared)              keyed choice is "it stops" (needs v_f^2 < 0)
              ("concept",)                        no numeric check
  value     short answer string for the key table
  topic     short topic name
  source    where it comes from (notes page / exam)
  card      which 3x5 notecard entry solves it
  solution  markdown worked solution
  distract  list of "x) explanation" strings
  fig       function(ax) drawing the diagram, or None
  figsize   (w, h) inches
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Ellipse, FancyArrowPatch, Polygon, Rectangle

EXAM_DIR = Path(__file__).resolve().parent.parent
plt.rcParams.update({"font.size": 12, "mathtext.fontset": "cm"})
LETTERS = "abcde"


# ------------------------------------------------------------------ drawing
def arrow(ax, p, q, **kw):
    style = dict(arrowstyle="-|>", mutation_scale=14, lw=1.5, color="k")
    style.update(kw)
    ax.add_patch(FancyArrowPatch(p, q, **style))


def dim(ax, p, q, text, offset=(0, 0), **kw):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="<|-|>", mutation_scale=10, lw=1, color="k"))
    mid = ((p[0] + q[0]) / 2 + offset[0], (p[1] + q[1]) / 2 + offset[1])
    ax.text(*mid, text, ha="center", va="center", **kw)


def incline(ax, theta_deg, length, origin=(0, 0)):
    """Right-triangle incline rising to the LEFT of origin. Returns (up-slope unit vector, top point, outward normal)."""
    t = np.radians(theta_deg)
    x0, y0 = origin
    top = (x0 - length * np.cos(t), y0 + length * np.sin(t))
    ax.add_patch(Polygon([origin, top, (top[0], y0)], closed=True, fill=False, lw=1.5))
    up = np.array([-np.cos(t), np.sin(t)])
    n = np.array([np.sin(t), np.cos(t)])  # outward normal (points above the slope)
    return up, np.array(top), n


def incline_right(ax, theta_deg, length, origin=(0, 0)):
    """Incline rising to the RIGHT of origin. Returns (up-slope unit vector, top point, outward normal)."""
    t = np.radians(theta_deg)
    x0, y0 = origin
    top = (x0 + length * np.cos(t), y0 + length * np.sin(t))
    ax.add_patch(Polygon([origin, top, (top[0], y0)], closed=True, fill=False, lw=1.5))
    up = np.array([np.cos(t), np.sin(t)])
    n = np.array([-np.sin(t), np.cos(t)])
    return up, np.array(top), n


def block_on(ax, base, up, n, size=0.5, label=None, **kw):
    c = np.array(base, dtype=float)
    pts = [c, c + up * size, c + up * size + n * size, c + n * size]
    ax.add_patch(Polygon(pts, closed=True, fill=False, lw=1.5, **kw))
    center = c + (up + n) * size / 2
    if label:
        ax.text(*center, label, ha="center", va="center", fontsize=9)
    return center


def disk_top_view(ax, center, r, **kw):
    ax.add_patch(Circle(center, r, fill=False, lw=1.5, **kw))
    ax.plot(*center, "k.")


def spin_arrow(ax, center, r, start_deg, end_deg, label=None, **kw):
    a0, a1 = np.radians(start_deg), np.radians(end_deg)
    p = (center[0] + r * np.cos(a0), center[1] + r * np.sin(a0))
    q = (center[0] + r * np.cos(a1), center[1] + r * np.sin(a1))
    rad = 0.35 if end_deg > start_deg else -0.35
    arrow(ax, p, q, connectionstyle=f"arc3,rad={rad}", **kw)
    if label:
        ax.text(q[0] + 0.1, q[1] + 0.1, label)


def hanging_pulley(ax, center=(0, 2), r=0.6, mass_label="m", thick=False, other=None):
    ax.add_patch(Circle(center, r, fill=False, lw=3 if thick else 1.5))
    ax.plot(*center, "k.")
    ax.plot([center[0] - r] * 2, [center[1], center[1] - 1.3], "k", lw=1)
    ax.add_patch(Rectangle((center[0] - r - 0.25, center[1] - 1.75), 0.5, 0.45, fill=False, lw=1.5))
    ax.text(center[0] - r, center[1] - 1.52, mass_label, ha="center", va="center", fontsize=10)
    if other:
        ax.plot([center[0] + r] * 2, [center[1], center[1] - 0.8], "k", lw=1)
        ax.add_patch(Rectangle((center[0] + r - 0.22, center[1] - 1.2), 0.44, 0.4, fill=False, lw=1.5))
        ax.text(center[0] + r, center[1] - 1.0, other, ha="center", va="center", fontsize=10)


# ------------------------------------------------------------------ checking
def check_question(num, q):
    kind = q["check"][0]
    key = q["key"]
    if kind == "near":
        _, value, nums, tol = q["check"]
        hits = [LETTERS[i] for i, c in enumerate(nums) if c is not None and abs(c - value) <= tol]
        ok = hits == [key]
        msg = f"computed {value:.4f}, matches {hits}"
    elif kind == "min":
        _, value, nums = q["check"]
        ok_choices = [(c, LETTERS[i]) for i, c in enumerate(nums) if c is not None and c >= value]
        best = min(ok_choices)[1] if ok_choices else None
        ok = best == key
        msg = f"computed {value:.4f} (minimum) -> smallest choice that works: {best}"
    elif kind == "max":
        _, value, nums = q["check"]
        ok_choices = [(c, LETTERS[i]) for i, c in enumerate(nums) if c is not None and c <= value]
        best = max(ok_choices)[1] if ok_choices else None
        ok = best == key
        msg = f"computed {value:.4f} (maximum) -> largest choice that works: {best}"
    elif kind == "stops":
        _, vf2 = q["check"]
        ok = vf2 < 0 and "stop" in q["choices"][LETTERS.index(key)].lower()
        msg = f"v_f^2 = {vf2:.4f} -> stops"
    elif kind == "concept":
        ok, msg = True, "conceptual"
    else:
        raise ValueError(kind)
    print(f"{'OK ' if ok else 'FAIL'} Q{num:>2}: key {key}) {q['choices'][LETTERS.index(key)]}  [{msg}]")
    return ok


# ------------------------------------------------------------------ writing
def _choices_line(choices):
    parts = []
    for L, c in zip(LETTERS, choices):
        c = c.replace(" ", "\\ ") if not c.startswith("it ") and "$" not in c else c
        parts.append(f"{L})\\ {c}")
    return " $\\quad$ ".join(parts)


def write_exam(n, title_sub, qs):
    out = [
        "---",
        f'title: "PHYS1408 Practice Exam 2-{n}"',
        f'subtitle: "{title_sub}"',
        "format:",
        "  pdf:",
        "    geometry: margin=0.75in",
        "    fontsize: 11pt",
        "    fig-pos: H",
        "  html:",
        "    embed-resources: true",
        "---",
        "",
        "Use $g = 9.8\\ \\text{m/s}^2$. Choose the single best answer. Answers are rounded to the precision shown. "
        "For a minimum or maximum, choose the answer choice that actually works.",
        "",
    ]
    for i, q in enumerate(qs, 1):
        body = f"**{i}.** {q['stem'].strip()}\\\n{_choices_line(q['choices'])}"
        if q.get("fig"):
            out += ['::: {layout="[58,42]" layout-valign="top"}', "::: {}", body, ":::", "",
                    f"![](figures/2-{n}/q{i:02d}.png)", ":::", ""]
        else:
            out += [body, ""]
    (EXAM_DIR / f"practice-exam-2-{n}.qmd").write_text("\n".join(out), encoding="utf-8")


def write_key(n, qs, intro):
    out = [
        "---",
        f'title: "PHYS1408 Practice Exam 2-{n} — Answer Key"',
        'subtitle: "Worked solutions"',
        "format:",
        "  pdf:",
        "    geometry: margin=0.75in",
        "    fontsize: 11pt",
        "  html:",
        "    embed-resources: true",
        "    toc: true",
        "---",
        "",
        f"All answers were checked numerically with `_scripts/build_exam_2_{n}.py`. $g = 9.8\\ \\text{{m/s}}^2$ throughout.",
        "",
        intro.strip(),
        "",
        "| Q | Answer | Value | Topic | Notecard entry |",
        "|:-:|:-:|:-:|:--|:--|",
    ]
    for i, q in enumerate(qs, 1):
        out.append(f"| {i} | **{q['key']}** | {q['value']} | {q['topic']} | {q['card']} |")
    out.append("")
    for i, q in enumerate(qs, 1):
        ans = q["choices"][LETTERS.index(q["key"])]
        out += [f"# {i}. {q['topic']} — **{q['key']}) {ans}**", "",
                f"**Source:** {q['source']}. **Notecard:** {q['card']}.", "",
                q["solution"].strip(), ""]
        if q.get("distract"):
            out += ["Distractors:", ""] + [f"* {d}" for d in q["distract"]] + [""]
    (EXAM_DIR / f"practice-exam-2-{n}-key.qmd").write_text("\n".join(_one_equation_per_line(out)), encoding="utf-8")


def _one_equation_per_line(lines):
    """Split single-line $$ blocks that hold several equations joined by \\qquad
    into separate $$ blocks with blank lines between them."""
    import re
    text = "\n".join(lines).split("\n")
    out = []
    for ln in text:
        st = ln.strip()
        if st.startswith("$$") and st.endswith("$$") and len(st) > 4 and "\\qquad" in st:
            parts = [p.strip().rstrip(",").strip() for p in re.split(r"(?:\\qquad)+", st[2:-2].strip())]
            if len(parts) > 1 and all("=" in p for p in parts) and not parts[0].endswith(":"):
                for k, p in enumerate(parts):
                    if k:
                        out.append("")
                    out.append(f"$${p}$$")
                continue
        out.append(ln)
    return out


def draw_figures(n, qs):
    d = EXAM_DIR / "figures" / f"2-{n}"
    d.mkdir(parents=True, exist_ok=True)
    for i, q in enumerate(qs, 1):
        if not q.get("fig"):
            continue
        fig, ax = plt.subplots(figsize=q.get("figsize", (4.0, 2.6)))
        ax.set_aspect("equal")
        ax.axis("off")
        q["fig"](ax)
        fig.savefig(d / f"q{i:02d}.png", dpi=200, bbox_inches="tight", pad_inches=0.05)
        plt.close(fig)


def build(n, title_sub, qs, intro):
    assert len(qs) == 15, len(qs)
    ok = all(check_question(i, q) for i, q in enumerate(qs, 1))
    keys = [q["key"] for q in qs]
    print("Key:", " ".join(keys), "| counts:", {L: keys.count(L) for L in LETTERS})
    assert ok, "a check failed"
    draw_figures(n, qs)
    write_exam(n, title_sub, qs)
    write_key(n, qs, intro)
    print(f"Wrote practice-exam-2-{n}.qmd, practice-exam-2-{n}-key.qmd and figures/2-{n}/")
