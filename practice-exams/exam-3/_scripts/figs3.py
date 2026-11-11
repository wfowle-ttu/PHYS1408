"""Parameterized sketches in the style of the professor's hand drawings (Ch 12/13 notes, 2015 Exam 3)."""
import numpy as np
from matplotlib.patches import Circle, FancyArrowPatch, Rectangle


def arrow(ax, p, q, **kw):
    style = dict(arrowstyle="-|>", mutation_scale=12, lw=1.4, color="k")
    style.update(kw)
    ax.add_patch(FancyArrowPatch(p, q, **style))


def hatch_v(ax, x, y0, y1, side=-1):
    ax.plot([x, x], [y0, y1], "k", lw=1.5)
    for y in np.linspace(y0 + 0.1, y1, 7):
        ax.plot([x, x + side * 0.18], [y, y - 0.18], "k", lw=0.8)


def hatch_h(ax, x0, x1, y):
    ax.plot([x0, x1], [y, y], "k", lw=1.5)
    for x in np.linspace(x0 + 0.1, x1, 9):
        ax.plot([x, x - 0.18], [y, y + 0.18], "k", lw=0.8)


def beam(L, supports, loads, ticks=None, width=6.0):
    """Horizontal beam 0..L.  supports: [(x, label, 'up'|'down')]; loads: [(x, label)] (down arrows).
    ticks: positions to label along the top (default 0 and L)."""
    s = width / L

    def f(ax):
        ax.add_patch(Rectangle((0, 0), L * s, 0.18, fill=False, lw=1.5))
        for t in (ticks if ticks is not None else [0, L]):
            ax.plot([t * s] * 2, [0.18, 0.32], "k", lw=1)
            ax.text(t * s, 0.42, f"{t:g}", ha="center", fontsize=10)
        for x, lab, d in supports:
            if d == "up":
                arrow(ax, (x * s, -0.95), (x * s, -0.02))
                ax.text(x * s, -1.25, lab, ha="center", fontsize=10)
            else:
                arrow(ax, (x * s, 0.0), (x * s, -0.95))
                ax.text(x * s, -1.25, lab, ha="center", fontsize=10)
        for x, lab in loads:
            arrow(ax, (x * s, 0.1), (x * s, -0.8), color="0.25")
            ax.text(x * s + 0.08, -0.7, lab, ha="left", fontsize=9)
        ax.set_xlim(-0.4, L * s + 0.6)
        ax.set_ylim(-1.45, 0.75)
    return f


def seesaw(L_label="L", left_label=r"$m_k$", right_label=r"$M$"):
    def f(ax):
        ax.plot([0, 6], [0.6, 0.6], "k", lw=2.5)
        ax.add_patch(plt_triangle((3, 0.6)))
        arrow(ax, (0, 0.6), (0, -0.4)); ax.text(0, -0.7, left_label, ha="center", fontsize=10)
        arrow(ax, (4.0, 0.6), (4.0, -0.4)); ax.text(4.0, -0.7, right_label, ha="center", fontsize=10)
        ax.annotate("", (3, 1.0), (4.0, 1.0), arrowprops=dict(arrowstyle="<->", lw=0.9))
        ax.text(3.5, 1.1, r"$x=?$", ha="center", fontsize=10)
        ax.annotate("", (0, 1.0), (3, 1.0), arrowprops=dict(arrowstyle="<->", lw=0.9))
        ax.text(1.5, 1.1, r"$L/2$", ha="center", fontsize=10)
        ax.set_xlim(-0.5, 6.5); ax.set_ylim(-0.9, 1.5)
    return f


def plt_triangle(top):
    from matplotlib.patches import Polygon
    x, y = top
    return Polygon([(x, y), (x - 0.3, y - 0.5), (x + 0.3, y - 0.5)], closed=True, fill=False, lw=1.3)


def boom(theta_deg, labels):
    """Beam hinged at a wall (left), cable from far end up to the wall at angle theta with the beam."""
    t = np.radians(theta_deg)
    Lb = 5.0

    def f(ax):
        hatch_v(ax, 0, -0.6, Lb * np.tan(t) + 0.3)
        ax.add_patch(Rectangle((0, -0.12), Lb, 0.24, fill=False, lw=1.5))
        ax.add_patch(Circle((0.18, 0), 0.1, fill=False, lw=1))
        ax.plot([Lb, 0], [0.12, Lb * np.tan(t)], "k", lw=1.2)
        ax.text(Lb / 2 + 0.2, Lb * np.tan(t) / 2 + 0.3, labels.get("T", r"$T$"), fontsize=10)
        ax.text(Lb - 1.0, 0.25, r"$\theta$", fontsize=10)
        xm = labels.get("xpos", 1.6)
        ax.plot([xm, xm], [-0.12, -0.7], "k", lw=1)
        ax.add_patch(Rectangle((xm - 0.25, -1.15), 0.5, 0.45, fill=False, lw=1.3))
        ax.text(xm, -0.92, labels.get("m", r"$m$"), ha="center", va="center", fontsize=9)
        ax.annotate("", (0, -1.45), (xm, -1.45), arrowprops=dict(arrowstyle="<->", lw=0.9))
        ax.text(xm / 2, -1.75, labels.get("x", r"$x$"), ha="center", fontsize=10)
        ax.text(Lb / 2, -0.45, labels.get("M", ""), ha="center", fontsize=9)
        ax.text(Lb + 0.1, -0.35, labels.get("L", ""), fontsize=9)
        ax.set_xlim(-0.4, Lb + 1.0); ax.set_ylim(-2.0, Lb * np.tan(t) + 0.4)
    return f


def ladder(theta_deg, label_x=r"$x=?$", man=True):
    t = np.radians(theta_deg)
    Ll = 4.0

    def f(ax):
        top = (0, Ll * np.sin(t))
        base = (Ll * np.cos(t), 0)
        hatch_v(ax, 0, -0.1, top[1] + 0.4, side=-1)
        hatch_h(ax, -0.2, base[0] + 1.0, 0)
        ax.plot([base[0], top[0]], [base[1], top[1]], "k", lw=2)
        ax.text(base[0] - 0.55, 0.12, r"$\theta$", fontsize=10)
        if man:
            p = (base[0] * 0.45, top[1] * 0.55)
            ax.plot(*p, "ko", ms=6)
            ax.text(p[0] + 0.15, p[1], label_x, fontsize=10)
        ax.set_xlim(-0.5, base[0] + 1.1); ax.set_ylim(-0.2, top[1] + 0.5)
    return f


def lamp(theta_deg, label=r"$T=?$"):
    """Light hung from a ceiling cord at theta with the ceiling, and a horizontal cord to a wall."""
    t = np.radians(theta_deg)

    def f(ax):
        knot = (3.0, 0.0)
        L = 1.6
        attach = (knot[0] + L * np.cos(t), knot[1] + L * np.sin(t))
        hatch_h(ax, attach[0] - 0.6, attach[0] + 0.8, attach[1])
        hatch_v(ax, 0, -0.6, 0.6, side=-1)
        ax.plot([0, knot[0]], [0, 0], "k", lw=1.2)
        ax.plot([knot[0], attach[0]], [knot[1], attach[1]], "k", lw=1.2)
        ax.plot([knot[0], attach[0] + 0.6], [0, 0], "k--", lw=0.7)
        ax.text(knot[0] + 0.85, 0.12, r"$\theta$", fontsize=10)
        ax.plot([knot[0], knot[0]], [0, -0.6], "k", lw=1.2)
        ax.add_patch(Rectangle((knot[0] - 0.25, -1.0), 0.5, 0.4, fill=False, lw=1.3))
        ax.text(knot[0] + 0.2, 0.75, label, fontsize=10)
        ax.set_xlim(-0.4, attach[0] + 1.0); ax.set_ylim(-1.1, attach[1] + 0.3)
    return f


def orbit(label_h=r"$h$", label_T=r"$T=?$"):
    def f(ax):
        ax.add_patch(Circle((0, 0), 1.0, fill=False, lw=1.5))
        ax.add_patch(Circle((0, 0), 1.7, fill=False, lw=1, ls="--"))
        ax.text(-0.2, -0.1, r"$R$", fontsize=10)
        ax.plot([0, 0.71], [0, 0.71], "k", lw=0.8)
        ax.plot([0.71, 1.2], [0.71, 1.2], "k", lw=0.8)
        ax.text(1.0, 0.8, label_h, fontsize=10)
        ax.plot(1.2, 1.2, "ks", ms=5)
        ax.text(1.9, 0.0, label_T, fontsize=10)
        ax.set_xlim(-1.9, 2.6); ax.set_ylim(-1.9, 1.9)
    return f


def binary(label=r"$d$"):
    def f(ax):
        ax.add_patch(Circle((0, 0), 1.3, fill=False, lw=1, ls="--"))
        ax.add_patch(Circle((-1.3, 0), 0.18, fill=False, lw=1.5))
        ax.add_patch(Circle((1.3, 0), 0.18, fill=False, lw=1.5))
        arrow(ax, (-1.3, 0.2), (-1.3, -0.8)); arrow(ax, (1.3, -0.2), (1.3, 0.8))
        ax.annotate("", (-1.3, -1.6), (1.3, -1.6), arrowprops=dict(arrowstyle="<->", lw=0.9))
        ax.text(0, -1.95, label, ha="center", fontsize=10)
        ax.set_xlim(-2.0, 2.0); ax.set_ylim(-2.2, 1.5)
    return f
