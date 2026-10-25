"""Draw the problem diagrams for practice-exam-2-3.

Run:  python practice-exams/exam-2/_scripts/make_figures_2_2.py
Writes PNGs to practice-exams/exam-2/figures/2-3/.
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyArrowPatch, Polygon, Rectangle, Ellipse

OUT = Path(__file__).resolve().parent.parent / "figures" / "2-3"
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




# 1. Banked curve, v_max: friction points DOWN the bank
fig, ax = canvas(4.2, 2.6)
up, top = incline(ax, 20, 4, origin=(4, 0))
c, n = block_on_slope(ax, np.array([4, 0]) + up * 2.0, up, size=0.6)
arrow(ax, c, c + n * 1.1)
ax.text(*(c + n * 1.25), r"$N$")
arrow(ax, c, c + np.array([0, -1.0]))
ax.text(c[0] + 0.1, c[1] - 1.0, r"$mg$")
arrow(ax, c, c - up * 0.9)
ax.text(*(c - up * 1.1 + np.array([0, -0.3])), r"$f_s$")
ax.text(3.0, 0.08, r"$\theta$")
ax.text(3.4, 1.7, r"center of curve $\rightarrow$", fontsize=10)
ax.set_xlim(-0.2, 6.6)
ax.set_ylim(-0.3, 2.4)
save(fig, "q01-banked-max")

# 3. Sled pulled by a rope at an angle
fig, ax = canvas(4.0, 1.8)
ax.plot([0, 4.2], [0, 0], "k", lw=1.5)
ax.add_patch(Rectangle((0.6, 0.05), 1.0, 0.4, fill=False, lw=1.5))
t = np.radians(30)
arrow(ax, (1.6, 0.25), (1.6 + 1.6 * np.cos(t), 0.25 + 1.6 * np.sin(t)))
ax.plot([1.6, 2.6], [0.25, 0.25], "k:", lw=1)
ax.text(2.15, 0.33, r"$\phi$", fontsize=11)
ax.text(3.1, 1.15, r"$F=50$ N", fontsize=10)
arrow(ax, (0.6, -0.35), (3.6, -0.35), lw=1)
ax.text(2.1, -0.65, r"$d = 12$ m", ha="center", fontsize=10)
ax.set_xlim(0, 4.3)
ax.set_ylim(-0.9, 1.4)
save(fig, "q03-sled")

# 4. Coyote falls off a cliff
fig, ax = canvas(2.6, 2.8)
ax.plot([-1.2, 0, 0, 1.6], [2.4, 2.4, 0, 0], "k", lw=1.5)
ax.add_patch(Circle((0.35, 2.55), 0.15, fill=True, color="k"))
ax.text(0.6, 2.6, r"$v_i=0$", fontsize=10)
arrow(ax, (0.35, 2.2), (0.35, 0.5), ls="--", lw=1)
ax.text(0.55, 0.3, r"$v=?$", fontsize=10)
dim(ax, (-0.4, 0), (-0.4, 2.4), r"$45$ m", offset=(-0.45, 0), fontsize=10)
ax.set_xlim(-1.3, 1.7)
ax.set_ylim(-0.2, 2.9)
save(fig, "q04-coyote")

# 5. Halfpipe with a rough patch, several passes
fig, ax = canvas(4.6, 2.8)
x = np.linspace(-1, 1, 400)
y = np.where(np.abs(x) > 0.55, ((np.abs(x) - 0.55) / 0.45) ** 2 * 2.2, 0)
ax.plot(x * 3, y, "k", lw=1.5)
ax.plot([-0.9, 0.9], [0, 0], color="0.4", lw=5, solid_capstyle="butt")
ax.text(0, -0.5, r"$L=4.0$ m,  $\mu=0.10$", ha="center")
arrow(ax, (-3.25, 0), (-3.25, 1.75))
ax.text(-3.4, 0.9, r"$h_i$", ha="right")
ax.text(-2.1, 1.2, r"$\mu=0$")
ax.text(1.35, 1.2, r"$\mu=0$")
ax.set_xlim(-3.8, 3.8)
ax.set_ylim(-0.8, 2.4)
save(fig, "q05-halfpipe")

# 6. Sliding up a rough incline until it stops
fig, ax = canvas(4.4, 2.6)
up, top = incline(ax, 30, 5.5, origin=(5.5, 0))
c, n = block_on_slope(ax, np.array([5.5, 0]) + up * 0.8, up)
arrow(ax, c + up * 0.4, c + up * 1.4)
ax.text(*(c + up * 0.5 + n * 0.6), r"$v_i=8.0$ m/s", fontsize=10)
ax.text(4.35, 0.15, r"$\theta$")
ax.text(1.2, 0.4, r"$\mu_k=0.20$", fontsize=10)
ax.text(*(c + up * 2.6 + n * 0.9), r"$\Delta x=?$", fontsize=11)
ax.set_xlim(0, 5.8)
ax.set_ylim(-0.2, 3.1)
save(fig, "q06-incline-up-stop")

# 7. Horizontal spring launcher
fig, ax = canvas(4.0, 1.4)
ax.plot([0, 0], [0, 0.7], "k", lw=2)
ax.plot([0, 4.0], [0, 0], "k", lw=1.5)
xs = np.linspace(0, 1.0, 200)
ax.plot(xs, 0.25 + 0.12 * np.sin(xs * 2 * np.pi * 7), "k", lw=1.2)
ax.add_patch(Rectangle((1.0, 0.02), 0.45, 0.45, fill=False, lw=1.5))
ax.text(1.22, 0.25, r"$m$", ha="center", va="center", fontsize=10)
arrow(ax, (1.7, 0.25), (2.6, 0.25))
ax.text(2.75, 0.2, r"$v=?$", fontsize=11)
ax.text(0.2, 0.75, r"$k$, compressed $x$", fontsize=9)
ax.text(3.2, -0.3, r"$\mu=0$", fontsize=10)
ax.set_xlim(-0.2, 4.1)
ax.set_ylim(-0.5, 1.0)
save(fig, "q07-spring-horizontal")

# 8. Loop: launched from h, normal force at top
fig, ax = canvas(4.0, 2.8)
x = np.linspace(0, 2.2, 100)
ax.plot(x - 2.2, 3.0 * (1 - x / 2.2) ** 2, "k", lw=1.5)
ax.plot([0, 2.6], [0, 0], "k", lw=1.5)
ax.add_patch(Circle((1.3, 1.0), 1.0, fill=False, lw=1.5))
ax.add_patch(Rectangle((-2.2, 2.95), 0.3, 0.22, fill=False, lw=1.5))
dim(ax, (-2.5, 0), (-2.5, 3.0), r"$h$", offset=(-0.25, 0))
ax.plot([1.3, 1.3 + 0.7], [1.0, 1.7], "k", lw=1)
ax.text(1.75, 1.2, r"$R$")
ax.text(0.9, 2.25, r"$N=?$", fontsize=11)
ax.set_xlim(-2.9, 2.7)
ax.set_ylim(-0.2, 3.4)
save(fig, "q08-loop-top")

# 9. Cue ball and 8-ball
fig, ax = canvas(3.6, 1.2)
ax.add_patch(Circle((0, 0), 0.3, fill=False, lw=1.5))
ax.add_patch(Circle((2.6, 0), 0.3, fill=False, lw=1.5))
ax.text(2.6, 0, "8", ha="center", va="center", fontsize=12)
arrow(ax, (0.4, 0), (1.4, 0))
ax.text(0.9, 0.25, r"$3.0$ m/s", ha="center", fontsize=10)
ax.text(2.6, -0.65, "at rest", ha="center", fontsize=10)
ax.text(0, -0.65, "cue", ha="center", fontsize=10)
ax.set_xlim(-0.5, 3.1)
ax.set_ylim(-0.9, 0.5)
save(fig, "q09-cue-ball")

# 10. Elastic collision, both moving right
fig, ax = canvas(4.2, 1.6)
ax.add_patch(Circle((0, 0), 0.3, fill=False, lw=1.5))
ax.add_patch(Circle((3, 0), 0.45, fill=False, lw=1.5))
arrow(ax, (0.4, 0), (1.3, 0))
arrow(ax, (3.5, 0), (4.0, 0))
ax.text(0, -0.8, r"$2$ kg,  $+6$ m/s", ha="center")
ax.text(3, -0.8, r"$4$ kg,  $+1$ m/s", ha="center")
ax.set_xlim(-0.6, 4.3)
ax.set_ylim(-1.1, 0.6)
save(fig, "q10-elastic")

# 11. Ballistic pendulum: find h
fig, ax = canvas(4.0, 2.8)
ax.plot([1.2, 3.2], [3, 3], "k", lw=2)
ax.plot([1.8, 1.8], [3, 1.4], "k", lw=1)
ax.plot([2.6, 2.6], [3, 1.4], "k", lw=1)
ax.add_patch(Rectangle((1.5, 0.4), 1.4, 1.0, fill=False, lw=1.5))
ax.text(2.2, 0.9, r"$M$", ha="center", va="center")
ax.add_patch(Rectangle((1.5 + 1.1, 0.4 + 0.45), 1.4, 1.0, fill=False, lw=1, ls="--"))
ax.plot([3.1, 4.4], [0.4, 0.4], "k:", lw=1)
ax.plot([3.1, 4.4], [0.85, 0.85], "k:", lw=1)
dim(ax, (4.25, 0.4), (4.25, 0.85), r"$h=?$", offset=(0.45, 0))
ax.add_patch(Ellipse((0.2, 0.9), 0.35, 0.14, fill=True, color="k"))
arrow(ax, (0.45, 0.9), (1.2, 0.9))
ax.text(0.0, 1.15, r"$400$ m/s", fontsize=10)
ax.set_xlim(-0.1, 5.0)
ax.set_ylim(0.2, 3.2)
save(fig, "q11-ballistic-h")

# 12. Hanging mass on a ring pulley: tension
fig, ax = canvas(2.8, 3.0)
ax.add_patch(Circle((0, 2), 0.8, fill=False, lw=3))
ax.plot([0], [2], "k.")
ax.plot([-0.8, -0.8], [2, 0.7], "k", lw=1)
ax.add_patch(Rectangle((-1.05, 0.3), 0.5, 0.4, fill=False, lw=1.5))
ax.text(-1.25, 0.5, r"$m$", ha="right", va="center")
ax.text(-0.7, 1.3, r"$T=?$", fontsize=10)
ax.text(0.85, 2.7, r"ring $M,\ R$", fontsize=10)
ax.text(0.5, 1.0, r"$I=MR^2$")
ax.set_xlim(-1.6, 2.2)
ax.set_ylim(0.1, 2.9)
save(fig, "q12-ring-pulley")

# 13. Hoop rolling down an incline
fig, ax = canvas(4.2, 2.4)
up, top = incline(ax, 18, 6, origin=(6, 0))
n = np.array([up[1], -up[0]])
if n[1] < 0:
    n = -n
c0 = top - up * 0.6 + n * 0.35
ax.add_patch(Circle(c0, 0.35, fill=False, lw=2.5))
ax.add_patch(Circle(c0, 0.28, fill=False, lw=0.8))
ax.text(c0[0] + 0.45, c0[1] + 0.35, r"$v_i=0$")
c1 = np.array([6, 0]) + up * 1.2 + n * 0.35
ax.add_patch(Circle(c1, 0.35, fill=False, lw=1.5, ls="--"))
ax.text(c1[0] - 0.3, c1[1] + 0.55, r"$v=?$")
dim(ax, (top[0] - 0.3, 0), (top[0] - 0.3, top[1]), r"$h$", offset=(-0.3, 0))
ax.set_xlim(-0.8, 6.3)
ax.set_ylim(-0.2, 2.6)
save(fig, "q13-hoop")

# 14. Non-spinning disk dropped onto a spinning disk
fig, ax = canvas(3.6, 2.8)
ax.plot([0, 0], [-0.3, 2.6], "k", lw=1)
ax.add_patch(Ellipse((0, 0.4), 3.2, 0.7, fill=False, lw=1.5))
ax.add_patch(Ellipse((0, 1.9), 2.0, 0.45, fill=False, lw=1.5))
arrow(ax, (0.9, 0.0), (1.4, 0.15), connectionstyle="arc3,rad=0.2")
ax.text(1.75, 0.35, r"$\omega_i$")
ax.text(1.15, 1.95, r"$\omega=0$", fontsize=10)
arrow(ax, (0.6, 1.5), (0.6, 0.9), lw=1)
ax.set_xlim(-2, 2.6)
ax.set_ylim(-0.4, 2.6)
save(fig, "q14-disk-on-disk")

# 15. Child runs against the rotation, jumps on at the rim (top view)
fig, ax = canvas(3.6, 3.0)
ax.add_patch(Circle((0, 0), 1.2, fill=False, lw=1.5))
ax.plot([0], [0], "k.")
ax.plot([0, 0], [0, -1.2], "k", lw=1)
ax.text(0.08, -0.6, r"$R$")
arrow(ax, (-2.4, -1.2), (-0.15, -1.2))
ax.add_patch(Circle((-2.6, -1.2), 0.12, fill=True, color="k"))
ax.text(-2.5, -0.9, r"$v=4.0$ m/s", fontsize=10)
arrow(ax, (0.2, 1.2), (0.9, 0.85), connectionstyle="arc3,rad=-0.25")
ax.text(0.95, 1.0, r"$\omega_i$")
ax.set_xlim(-2.9, 1.5)
ax.set_ylim(-1.5, 1.5)
save(fig, "q15-child-against")

print(f"Wrote figures to {OUT}")
