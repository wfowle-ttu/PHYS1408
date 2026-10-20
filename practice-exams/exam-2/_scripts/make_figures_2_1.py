"""Draw the problem diagrams for practice-exam-2-1.

Run:  python practice-exams/exam-2/_scripts/make_figures_2_1.py
Writes PNGs to practice-exams/exam-2/figures/2-1/.
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyArrowPatch, Polygon, Rectangle, Ellipse

OUT = Path(__file__).resolve().parent.parent / "figures" / "2-1"
OUT.mkdir(parents=True, exist_ok=True)
plt.rcParams.update({"font.size": 12, "mathtext.fontset": "cm"})


def canvas(w=4.2, h=3.0):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def arrow(ax, p, q, **kw):
    style = dict(arrowstyle="-|>", mutation_scale=14, lw=1.5, color="k")
    style.update(kw)
    ax.add_patch(FancyArrowPatch(p, q, **style))


def dim(ax, p, q, text, offset=(0, 0), **kw):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="<|-|>", mutation_scale=10, lw=1, color="k"))
    mid = ((p[0] + q[0]) / 2 + offset[0], (p[1] + q[1]) / 2 + offset[1])
    ax.text(*mid, text, ha="center", va="center", **kw)


def save(fig, name):
    fig.savefig(OUT / f"{name}.png", dpi=200, bbox_inches="tight", pad_inches=0.05)
    plt.close(fig)


def incline(ax, theta_deg, length, origin=(0, 0)):
    """Right-triangle incline rising to the left. Returns unit vector pointing up the slope."""
    t = np.radians(theta_deg)
    x0, y0 = origin
    top = (x0 - length * np.cos(t), y0 + length * np.sin(t))
    ax.add_patch(Polygon([origin, top, (top[0], y0)], closed=True, fill=False, lw=1.5))
    return np.array([-np.cos(t), np.sin(t)]), np.array(top)


def block_on_slope(ax, pos, up, size=0.5, **kw):
    n = np.array([-up[1], up[0]])
    if n[1] < 0:
        n = -n
    c = np.array(pos)
    pts = [c, c + up * size, c + up * size + n * size, c + n * size]
    ax.add_patch(Polygon(pts, closed=True, fill=False, lw=1.5, **kw))
    return c + (up + n) * size / 2, n


# 1. Halfpipe with rough patch
fig, ax = canvas(4.6, 2.8)
x = np.linspace(-1, 1, 400)
y = np.where(np.abs(x) > 0.55, ((np.abs(x) - 0.55) / 0.45) ** 2 * 2.2, 0)
ax.plot(x * 3, y, "k", lw=1.5)
ax.plot([-0.9, 0.9], [0, 0], color="0.4", lw=5, solid_capstyle="butt")
dim(ax, (-0.9, -0.35), (0.9, -0.35), "", )
ax.text(0, -0.65, r"$L=8.0$ m,  $\mu=0.15$", ha="center")
arrow(ax, (-3.25, 0), (-3.25, 1.75))
ax.text(-3.4, 0.9, r"$h_i$", ha="right")
ax.text(-2.1, 1.2, r"$\mu=0$")
ax.text(1.35, 1.2, r"$\mu=0$")
ax.text(3.2, 1.0, r"$h_f=?$")
ax.set_xlim(-3.8, 3.8)
ax.set_ylim(-0.9, 2.4)
save(fig, "q01-halfpipe")

# 2. Projectile from a ledge
fig, ax = canvas(4.4, 2.8)
ax.plot([-0.8, 0, 0, 7], [2, 2, 0, 0], "k", lw=1.5)
t = np.linspace(0, 2.4, 100)
ax.plot(t * 2.4, 2 + t * 2.4 * np.tan(np.radians(30)) - 0.5 * (t * 2.4) ** 2 * 0.17, "k--", lw=1)
arrow(ax, (0, 2), (1.3, 2 + 1.3 * np.tan(np.radians(30))))
ax.text(1.1, 2.9, r"$v_0$")
ax.text(0.9, 2.1, r"$\theta$")
dim(ax, (-0.4, 0), (-0.4, 2), r"$h$", offset=(-0.35, 0))
xp = 2.4 * 1.7
ax.plot([xp, xp], [0, 3.15], "k", lw=1)
ax.text(xp + 0.15, 1.5, r"$H=?$")
ax.set_xlim(-1.2, 7)
ax.set_ylim(-0.2, 3.6)
save(fig, "q02-projectile")

# 3. Loop-the-loop
fig, ax = canvas(3.4, 3.0)
ax.add_patch(Circle((0, 1), 1, fill=False, lw=1.5))
ax.plot([-2.2, 1.5], [0, 0], "k", lw=1.5)
ax.add_patch(Rectangle((-0.75, 0), 0.25, 0.2, fill=False, lw=1.5))
arrow(ax, (-1.6, 0.35), (-0.85, 0.35))
ax.text(-2.1, 0.5, r"$v_{\min}=?$")
arrow(ax, (0, 1), (0.7, 1.7))
ax.text(0.2, 1.45, r"$R$")
ax.set_xlim(-2.3, 1.6)
ax.set_ylim(-0.2, 2.2)
save(fig, "q03-loop")

# 4. Block sliding up a rough ramp
fig, ax = canvas(4.4, 2.4)
up, top = incline(ax, 20, 6, origin=(6, 0))
c, n = block_on_slope(ax, np.array([6, 0]) + up * 1.2, up)
arrow(ax, c + up * 0.4, c + up * 1.4)
ax.text(*(c + up * 1.0 + n * 0.5), r"$v_i=6$ m/s,  $\Delta t=?$")
ax.text(4.7, 0.15, r"$\theta$")
ax.text(1.0, 0.35, r"$\mu_k=0.30$")
ax.set_xlim(0, 6.3)
ax.set_ylim(-0.2, 2.6)
save(fig, "q04-ramp")

# 5. Banked curve, cross-section with free-body forces
fig, ax = canvas(4.2, 2.6)
up, top = incline(ax, 15, 4, origin=(4, 0))
c, n = block_on_slope(ax, np.array([4, 0]) + up * 2.3, up, size=0.6)
arrow(ax, c, c + n * 1.2)
ax.text(*(c + n * 1.3), r"$N$")
arrow(ax, c, c + np.array([0, -1.0]))
ax.text(c[0] + 0.1, c[1] - 1.0, r"$mg$")
arrow(ax, c, c - up * 0.9)
ax.text(*(c - up * 1.1 + np.array([0, -0.25])), r"$f_s$")
ax.text(3.0, 0.08, r"$\theta$")
ax.text(3.6, 1.6, r"center of curve $\rightarrow$", fontsize=10)
ax.set_xlim(-0.2, 6.6)
ax.set_ylim(-0.3, 2.6)
save(fig, "q05-banked")

# 6. Vertical spring launcher
fig, ax = canvas(2.6, 3.2)
ys = np.linspace(0, 0.9, 200)
ax.plot(0.25 * np.sin(ys * 2 * np.pi * 9), ys, "k", lw=1.2)
ax.plot([-0.8, 0.8], [0, 0], "k", lw=2)
ax.add_patch(Circle((0, 1.05), 0.15, fill=False, lw=1.5))
ax.text(0.25, 1.05, r"$m$", va="center")
ax.plot([0.5, 1.1], [1.05, 1.05], "k:", lw=1)
ax.plot([0.5, 1.1], [2.3, 2.3], "k:", lw=1)
dim(ax, (0.95, 1.05), (0.95, 2.3), r"$h=?$", offset=(0.45, 0))
ax.text(-1.25, 0.45, r"$k$, compressed $x$", fontsize=9, rotation=90, va="center")
ax.set_xlim(-1.4, 1.8)
ax.set_ylim(-0.1, 2.5)
save(fig, "q06-spring")

# 7. Head-on elastic collision
fig, ax = canvas(4.2, 1.6)
ax.add_patch(Circle((0, 0), 0.45, fill=False, lw=1.5))
ax.add_patch(Circle((3, 0), 0.3, fill=False, lw=1.5))
arrow(ax, (0.5, 0), (1.3, 0))
arrow(ax, (2.6, 0), (1.8, 0))
ax.text(0, -0.8, r"$3$ kg,  $+4$ m/s", ha="center")
ax.text(3, -0.8, r"$1$ kg,  $-6$ m/s", ha="center")
ax.set_xlim(-0.8, 4.0)
ax.set_ylim(-1.1, 0.6)
save(fig, "q07-elastic")

# 8. Perfectly inelastic collision of two carts
fig, ax = canvas(4.2, 1.4)
for x0, w, lab in [(0, 1.0, r"$m$"), (3.0, 1.6, r"$2m$")]:
    ax.add_patch(Rectangle((x0, 0.2), w, 0.6, fill=False, lw=1.5))
    ax.add_patch(Circle((x0 + 0.2, 0.1), 0.1, fill=False, lw=1))
    ax.add_patch(Circle((x0 + w - 0.2, 0.1), 0.1, fill=False, lw=1))
    ax.text(x0 + w / 2, 0.5, lab, ha="center", va="center")
ax.plot([-0.3, 5.0], [0, 0], "k", lw=1.5)
arrow(ax, (1.1, 0.5), (2.0, 0.5))
ax.text(1.55, 0.75, r"$3v$", ha="center")
ax.text(3.8, 1.0, "at rest", ha="center")
ax.set_xlim(-0.4, 5.1)
ax.set_ylim(-0.1, 1.2)
save(fig, "q08-inelastic")

# 9. Ballistic pendulum
fig, ax = canvas(4.0, 2.8)
ax.plot([1.2, 3.2], [3, 3], "k", lw=2)
ax.plot([1.8, 1.8], [3, 1.4], "k", lw=1)
ax.plot([2.6, 2.6], [3, 1.4], "k", lw=1)
ax.add_patch(Rectangle((1.5, 0.4), 1.4, 1.0, fill=False, lw=1.5))
ax.text(2.2, 0.9, r"$M$", ha="center", va="center")
ax.add_patch(Rectangle((1.5 + 1.1, 0.4 + 0.45), 1.4, 1.0, fill=False, lw=1, ls="--"))
ax.plot([3.1, 4.4], [0.4, 0.4], "k:", lw=1)
ax.plot([3.1, 4.4], [0.85, 0.85], "k:", lw=1)
dim(ax, (4.25, 0.4), (4.25, 0.85), r"$h$", offset=(0.3, 0))
ax.add_patch(Ellipse((0.2, 0.9), 0.35, 0.14, fill=True, color="k"))
arrow(ax, (0.45, 0.9), (1.2, 0.9))
ax.text(0.2, 1.15, r"$m,\ v=?$")
ax.set_xlim(-0.1, 4.8)
ax.set_ylim(0.2, 3.2)
save(fig, "q09-ballistic")

# 10. Hanging mass on a disk pulley
fig, ax = canvas(2.8, 3.0)
ax.add_patch(Circle((0, 2), 0.8, fill=False, lw=1.5))
ax.plot([0], [2], "k.")
ax.plot([-0.8, -0.8], [2, 0.7], "k", lw=1)
ax.add_patch(Rectangle((-1.05, 0.3), 0.5, 0.4, fill=False, lw=1.5))
ax.text(-1.25, 0.5, r"$m$", ha="right", va="center")
arrow(ax, (-0.3, 0.6), (-0.3, 0.0))
ax.text(-0.2, 0.25, r"$v_i=0$", fontsize=10)
ax.text(0.95, 2.6, r"$M,\ R$")
ax.text(0.6, 1.0, r"$I=\frac{1}{2}MR^2$")
ax.set_xlim(-1.6, 2.0)
ax.set_ylim(-0.1, 2.9)
save(fig, "q10-pulley")

# 11. Solid cylinder rolling down an incline
fig, ax = canvas(4.2, 2.4)
up, top = incline(ax, 18, 6, origin=(6, 0))
n = np.array([-up[1], up[0]])
c0 = top - up * 0.6 + n * 0.35
ax.add_patch(Circle(c0, 0.35, fill=False, lw=1.5))
ax.text(c0[0] + 0.45, c0[1] + 0.35, r"$v_i=0$")
c1 = np.array([6, 0]) + up * 2.2 + n * 0.35
ax.add_patch(Circle(c1, 0.35, fill=False, lw=1.5, ls="--"))
ax.text(c1[0] + 0.2, c1[1] + 0.5, r"$\omega_f=?$")
dim(ax, (top[0] - 0.3, 0), (top[0] - 0.3, top[1]), r"$h$", offset=(-0.3, 0))
ax.set_xlim(-0.8, 6.3)
ax.set_ylim(-0.2, 2.4)
save(fig, "q11-rolling")

# 12. Ring dropped onto a spinning disk
fig, ax = canvas(3.6, 2.8)
ax.plot([0, 0], [-0.3, 2.6], "k", lw=1)
ax.add_patch(Ellipse((0, 0.4), 3.2, 0.7, fill=False, lw=1.5))
ax.add_patch(Ellipse((0, 1.9), 2.2, 0.5, fill=False, lw=1.5))
arrow(ax, (0.9, 0.0), (1.4, 0.15), connectionstyle="arc3,rad=0.2")
arrow(ax, (-0.5, 1.65), (-1.0, 1.75), connectionstyle="arc3,rad=-0.2")
ax.text(1.75, 0.35, "disk")
ax.text(1.25, 1.95, "ring")
arrow(ax, (0.6, 1.5), (0.6, 0.9), lw=1)
ax.set_xlim(-2, 2.6)
ax.set_ylim(-0.4, 2.6)
save(fig, "q12-disk-ring")

# 13. Child jumps tangentially onto merry-go-round rim (top view)
fig, ax = canvas(3.6, 3.0)
ax.add_patch(Circle((0, 0), 1.2, fill=False, lw=1.5))
ax.plot([0], [0], "k.")
ax.plot([0, 0], [0, -1.2], "k", lw=1)
ax.text(0.08, -0.6, r"$R$")
arrow(ax, (-2.4, -1.2), (-0.15, -1.2))
ax.add_patch(Circle((-2.6, -1.2), 0.12, fill=True, color="k"))
ax.text(-2.5, -0.9, r"$v=6$ m/s", fontsize=10)
arrow(ax, (0.9, 0.85), (0.2, 1.2), connectionstyle="arc3,rad=0.25")
ax.text(0.95, 1.0, r"$\omega_i$")
ax.set_xlim(-2.9, 1.5)
ax.set_ylim(-1.5, 1.5)
save(fig, "q13-child-mgr")

# 14. Person walks from rim to center (top view, before/after)
fig, ax = canvas(4.4, 2.0)
for cx, (px, py), lab in [(0, (0, -0.85), r"$\omega_i$"), (2.6, (2.6, 0), r"$\omega_f=?$")]:
    ax.add_patch(Circle((cx, 0), 0.9, fill=False, lw=1.5))
    ax.add_patch(Circle((px, py), 0.09, fill=True, color="k"))
    ax.text(cx + 0.65, 0.85, lab)
ax.plot([0], [0], "k.")
arrow(ax, (1.0, 0), (1.6, 0))
ax.set_xlim(-1.1, 3.9)
ax.set_ylim(-1.1, 1.2)
save(fig, "q14-walk-in")

# 15. Block sliding down a rough incline, tied over a disk pulley
fig, ax = canvas(4.4, 2.6)
t = np.radians(25)
ax.add_patch(Polygon([(0, 2.6), (5.6, 0), (0, 0)], closed=True, fill=False, lw=1.5))
down = np.array([np.cos(t), -np.sin(t)])
n = np.array([np.sin(t), np.cos(t)])
pc = np.array([0.0, 2.6]) + n * 0.45
ax.add_patch(Circle(pc, 0.35, fill=False, lw=1.5))
ax.plot(*pc, "k.")
b0 = np.array([0, 2.6]) + down * 2.2
c, _ = block_on_slope(ax, b0, down, size=0.6)
ax.plot([pc[0] + n[0] * 0.35, b0[0] + n[0] * 0.3], [pc[1] + n[1] * 0.35, b0[1] + n[1] * 0.3], "k", lw=1)
arrow(ax, c + down * 0.5, c + down * 1.4)
ax.text(*(c + down * 1.0 + n * 0.45), r"$v_i=0.50$ m/s", fontsize=10)
ax.text(4.5, 0.1, r"$\theta$")
ax.text(1.9, 0.7, r"$\mu=0.15$")
ax.set_xlim(-0.8, 5.8)
ax.set_ylim(-0.2, 3.6)
save(fig, "q15-incline-pulley")

print(f"Wrote figures to {OUT}")
