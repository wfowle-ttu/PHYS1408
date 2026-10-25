"""Draw the problem diagrams for practice-exam-2-2.

Run:  python practice-exams/exam-2/_scripts/make_figures_2_2.py
Writes PNGs to practice-exams/exam-2/figures/2-2/.
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyArrowPatch, Polygon, Rectangle, Ellipse

OUT = Path(__file__).resolve().parent.parent / "figures" / "2-2"
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


# 1. Flat curve (top view)
fig, ax = canvas(3.4, 2.8)
a = np.linspace(np.radians(200), np.radians(340), 100)
for rr in (1.6, 2.1):
    ax.plot(rr * np.cos(a), rr * np.sin(a) + 2.2, "k", lw=1.5)
ax.plot([0], [2.2], "k.")
ax.plot([0, 1.85 * np.cos(np.radians(250))], [2.2, 2.2 + 1.85 * np.sin(np.radians(250))], "k--", lw=1)
ax.text(-0.45, 1.3, r"$r$")
ax.add_patch(Rectangle((-0.15, 0.25), 0.3, 0.2, fill=False, lw=1.5))
arrow(ax, (0.2, 0.35), (0.9, 0.42))
ax.text(0.6, -0.05, r"$v_{\max}=?$")
ax.text(-1.9, 0.1, r"$\mu_s=0.40$", fontsize=10)
ax.set_xlim(-2.3, 2.3)
ax.set_ylim(-0.2, 2.4)
save(fig, "q01-flat-curve")

# 2. Banked curve, v_min: friction points UP the bank
fig, ax = canvas(4.2, 2.6)
up, top = incline(ax, 30, 4, origin=(4, 0))
c, n = block_on_slope(ax, np.array([4, 0]) + up * 2.0, up, size=0.6)
arrow(ax, c, c + n * 1.1)
ax.text(*(c + n * 1.25), r"$N$")
arrow(ax, c, c + np.array([0, -1.0]))
ax.text(c[0] + 0.1, c[1] - 1.0, r"$mg$")
arrow(ax, c, c + up * 0.9)
ax.text(*(c + up * 1.15 + np.array([0, 0.1])), r"$f_s$")
ax.text(2.95, 0.08, r"$\theta$")
ax.text(3.4, 1.9, r"center of curve $\rightarrow$", fontsize=10)
ax.set_xlim(-0.2, 6.6)
ax.set_ylim(-0.3, 2.6)
save(fig, "q02-banked-min")

# 3. Atwood machine
fig, ax = canvas(2.8, 3.0)
ax.plot([-1.2, 1.2], [3.0, 3.0], "k", lw=2)
ax.plot([0, 0], [3.0, 2.4], "k", lw=1)
ax.add_patch(Circle((0, 2.1), 0.3, fill=False, lw=1.5))
ax.plot([-0.3, -0.3], [2.1, 0.9], "k", lw=1)
ax.plot([0.3, 0.3], [2.1, 1.5], "k", lw=1)
ax.add_patch(Rectangle((-0.6, 0.4), 0.6, 0.5, fill=False, lw=1.5))
ax.add_patch(Rectangle((0.05, 1.1), 0.5, 0.4, fill=False, lw=1.5))
ax.text(-0.3, 0.65, r"$m_1$", ha="center", va="center")
ax.text(0.3, 1.3, r"$m_2$", ha="center", va="center")
arrow(ax, (-0.85, 0.9), (-0.85, 0.3))
arrow(ax, (0.8, 1.0), (0.8, 1.6))
ax.text(-1.5, 0.15, r"$v_i=0$", fontsize=10)
ax.set_xlim(-1.6, 1.3)
ax.set_ylim(0.0, 3.1)
save(fig, "q03-atwood")

# 4. Roller coaster
fig, ax = canvas(4.6, 2.8)
x = np.linspace(0, 10, 400)
y = 6.5 * np.exp(-(x / 1.4) ** 2) + 4.5 * np.exp(-((x - 5) / 1.0) ** 2) + 1.0 * (x > 6.5) * (1 - np.exp(-(x - 6.5) * 3))
y = np.maximum(y, 0.4)
ax.plot(x, y, "k", lw=1.5)
ax.plot([0, 10], [0, 0], "k:", lw=1)
ax.add_patch(Circle((0.25, y[10] + 0.25), 0.2, fill=True, color="k"))
ax.text(0.6, 6.4, r"$v=0$", fontsize=10)
ax.text(5.3, 4.8, r"$45$ m", fontsize=10)
ax.text(8.6, 1.6, r"$v=?$", fontsize=11)
dim(ax, (9.7, 0), (9.7, 1.0), r"$10$ m", offset=(0.0, 0.45), fontsize=9)
dim(ax, (-0.4, 0), (-0.4, 6.5), r"$65$ m", offset=(-0.5, 0), fontsize=10)
ax.set_xlim(-1.4, 10.3)
ax.set_ylim(-0.3, 7.2)
save(fig, "q04-coaster")

# 5. Frictionless incline, sliding up
fig, ax = canvas(4.4, 2.2)
up, top = incline(ax, 15, 6, origin=(6, 0))
c, n = block_on_slope(ax, np.array([6, 0]) + up * 1.0, up)
arrow(ax, c + up * 0.4, c + up * 1.4)
ax.text(*(c + up * 0.4 + n * 0.55), r"$v_i=5.0$ m/s")
dim(ax, np.array([6, 0]) + up * 1.0 - n * 0.3, np.array([6, 0]) + up * 3.5 - n * 0.3, r"$2.5$ m", offset=(0.1, -0.35), fontsize=10)
ax.text(4.8, 0.12, r"$\theta$")
ax.text(1.2, 0.3, r"$\mu=0$")
ax.set_xlim(0, 6.3)
ax.set_ylim(-0.5, 1.9)
save(fig, "q05-incline-up")

# 6. Sliding DOWN a rough incline
fig, ax = canvas(4.4, 2.2)
up, top = incline(ax, 12, 6, origin=(6, 0))
c, n = block_on_slope(ax, np.array([6, 0]) + up * 4.3, up)
arrow(ax, c - up * 0.4, c - up * 1.4)
ax.text(*(c - up * 0.6 + n * 0.5), r"$v_i=4.0$ m/s")
ax.text(4.9, 0.1, r"$\theta$")
ax.text(2.6, 0.3, r"$\mu_k=0.35$")
ax.text(4.2, 0.95, r"$\Delta x=?$", fontsize=11)
ax.set_xlim(0, 6.3)
ax.set_ylim(-0.2, 1.8)
save(fig, "q06-incline-down")

# 7. Block up an incline, pulled by a hanging mass
fig, ax = canvas(4.4, 2.6)
t = np.radians(25)
ax.add_patch(Polygon([(0, 0), (4.6, 4.6 * np.tan(t)), (4.6, 0)], closed=True, fill=False, lw=1.5))
upv = np.array([np.cos(t), np.sin(t)])
nv = np.array([-np.sin(t), np.cos(t)])
pc = np.array([4.6, 4.6 * np.tan(t)]) + np.array([0.25, 0.25])
ax.add_patch(Circle(pc, 0.25, fill=False, lw=1.5))
b0 = upv * 1.2
c, _ = block_on_slope(ax, b0, upv, size=0.6)
ax.plot([b0[0] + upv[0] * 0.6 + nv[0] * 0.3, pc[0] - 0.05], [b0[1] + upv[1] * 0.6 + nv[1] * 0.3, pc[1] + 0.24], "k", lw=1)
ax.plot([pc[0] + 0.25, pc[0] + 0.25], [pc[1], 0.9], "k", lw=1)
ax.add_patch(Rectangle((pc[0], 0.4), 0.5, 0.5, fill=False, lw=1.5))
ax.text(pc[0] + 0.25, 0.65, r"$m_2$", ha="center", va="center", fontsize=10)
ax.text(*(c - nv * 0.05), r"$m_1$", ha="center", va="center", fontsize=10)
arrow(ax, c + upv * 0.5 + nv * 0.5, c + upv * 1.4 + nv * 0.5)
ax.text(*(c + nv * 1.0 - upv * 0.4), r"$v_i=3.0$ m/s", fontsize=10)
ax.text(0.9, 0.1, r"$\theta$")
ax.text(2.6, 0.4, r"$\mu_k=0.30$", fontsize=10)
ax.set_xlim(-0.2, 5.6)
ax.set_ylim(-0.2, 3.0)
save(fig, "q07-incline-hanging")

# 8. Mass slides down a frictionless ramp into a spring
fig, ax = canvas(4.4, 2.4)
x = np.linspace(0, 1.6, 100)
ax.plot(x, 1.6 * (1 - x / 1.6) ** 2, "k", lw=1.5)
ax.plot([1.6, 4.4], [0, 0], "k", lw=1.5)
ax.plot([4.4, 4.4], [0, 0.6], "k", lw=2)
xs = np.linspace(3.4, 4.4, 200)
ax.plot(xs, 0.2 + 0.1 * np.sin((xs - 3.4) * 2 * np.pi * 7), "k", lw=1.2)
ax.add_patch(Rectangle((0.05, 1.5), 0.3, 0.25, fill=False, lw=1.5))
ax.text(0.5, 1.75, r"$m,\ v_i=0$", fontsize=10)
dim(ax, (-0.3, 0), (-0.3, 1.5), r"$h$", offset=(-0.25, 0))
ax.text(3.6, 0.5, r"$k$", fontsize=11)
ax.text(2.0, 0.6, r"$\mu=0$", fontsize=10)
ax.text(3.3, -0.4, r"compression $x=?$", fontsize=10)
ax.set_xlim(-0.8, 4.6)
ax.set_ylim(-0.6, 2.0)
save(fig, "q08-ramp-spring")

# 9. Person climbs stairs
fig, ax = canvas(3.2, 2.6)
xs, ys = [0], [0]
for i in range(6):
    xs += [i * 0.5, (i + 1) * 0.5]
    ys += [(i + 1) * 0.4, (i + 1) * 0.4]
ax.plot(xs, ys, "k", lw=1.5)
ax.plot([0, 3.0], [0, 0], "k", lw=1.5)
ax.add_patch(Circle((0.25, 0.75), 0.12, fill=True, color="k"))
ax.plot([0.25, 0.25], [0.63, 0.4], "k", lw=2)
dim(ax, (3.2, 0), (3.2, 2.4), r"$12$ m", offset=(0.45, 0), fontsize=10)
ax.text(0.2, 2.2, r"$\Delta t = 8.0$ s", fontsize=10)
ax.set_xlim(-0.2, 4.0)
ax.set_ylim(-0.1, 2.6)
save(fig, "q09-stairs")

# 10. Ball bounces straight back off a wall
fig, ax = canvas(3.6, 1.8)
ax.plot([3.0, 3.0], [-0.8, 0.8], "k", lw=2)
for k in range(8):
    ax.plot([3.0, 3.2], [-0.8 + k * 0.2, -0.6 + k * 0.2], "k", lw=0.8)
ax.add_patch(Circle((2.7, 0), 0.25, fill=False, lw=1.5))
arrow(ax, (0.6, 0.3), (2.2, 0.3))
arrow(ax, (2.2, -0.3), (0.6, -0.3))
ax.text(1.4, 0.55, r"$30$ m/s in", ha="center", fontsize=10)
ax.text(1.4, -0.7, r"$30$ m/s out", ha="center", fontsize=10)
ax.set_xlim(0.3, 3.4)
ax.set_ylim(-1.0, 0.9)
save(fig, "q10-bounce")

# 11. Spinning wheel speeding up
fig, ax = canvas(2.6, 2.6)
ax.add_patch(Circle((0, 0), 1.0, fill=False, lw=1.5))
for ang in np.radians([0, 60, 120, 180, 240, 300]):
    ax.plot([0, np.cos(ang)], [0, np.sin(ang)], "k", lw=0.8)
arrow(ax, (1.25, -0.3), (0.5, 1.2), connectionstyle="arc3,rad=0.45")
ax.text(1.2, 0.9, r"$\omega$")
ax.text(-1.2, -1.35, r"$10 \to 50$ rad/s,  $\Delta\theta = 90$ rad", fontsize=9)
ax.set_xlim(-1.3, 1.6)
ax.set_ylim(-1.5, 1.3)
save(fig, "q11-wheel")

# 12. Rod pivoting about an axis 0.30 m from one end
fig, ax = canvas(4.0, 1.6)
ax.add_patch(Rectangle((0, -0.12), 4.0, 0.24, fill=False, lw=1.5))
ax.plot([1.0], [0], "ko")
ax.plot([2.0], [0], "k+", ms=10)
ax.text(1.0, 0.45, "axis", ha="center", fontsize=10)
ax.text(2.0, 0.45, "center", ha="center", fontsize=10)
dim(ax, (0, -0.45), (1.0, -0.45), r"$0.30$ m", offset=(0, -0.3), fontsize=10)
dim(ax, (0, -1.05), (4.0, -1.05), r"$\ell = 1.2$ m", offset=(0, -0.3), fontsize=10)
ax.set_xlim(-0.2, 4.2)
ax.set_ylim(-1.6, 0.7)
save(fig, "q12-rod-axis")

# 13. Solid sphere rolling down an incline
fig, ax = canvas(4.2, 2.2)
up, top = incline(ax, 25, 5, origin=(5, 0))
n = np.array([up[1], -up[0]])  # outward normal (above the slope)
if n[1] < 0:
    n = -n
c1 = np.array([5, 0]) + up * 2.6 + n * 0.4
ax.add_patch(Circle(c1, 0.4, fill=False, lw=1.5))
arrow(ax, c1 - up * 0.5 + n * 0.55, c1 - up * 1.5 + n * 0.55)
ax.text(*(c1 - up * 1.6 + n * 0.85), r"$a=?$")
ax.text(3.9, 0.12, r"$\theta$")
ax.set_xlim(0, 5.3)
ax.set_ylim(-0.2, 2.5)
save(fig, "q13-sphere-rolling")

# 14. Person steps onto merry-go-round at r < R (top view)
fig, ax = canvas(3.0, 2.8)
ax.add_patch(Circle((0, 0), 1.25, fill=False, lw=1.5))
ax.plot([0], [0], "k.")
ax.plot([0, 0.75], [0, 0], "k", lw=1)
ax.text(0.3, 0.12, r"$r$")
ax.plot([0, -1.25 * np.cos(np.radians(40))], [0, -1.25 * np.sin(np.radians(40))], "k--", lw=1)
ax.text(-0.75, -0.45, r"$R$")
ax.add_patch(Circle((0.75, 0), 0.1, fill=True, color="k"))
arrow(ax, (0.95, 0.95), (0.2, 1.3), connectionstyle="arc3,rad=0.25")
ax.text(1.0, 1.05, r"$\omega_i$")
ax.set_xlim(-1.5, 1.6)
ax.set_ylim(-1.4, 1.5)
save(fig, "q14-person-drops")

# 15. Rod dropped from center to edge (top view)
fig, ax = canvas(3.0, 2.8)
ax.add_patch(Circle((0, 0), 1.25, fill=False, lw=1.5))
ax.add_patch(Rectangle((-0.06, 0), 0.12, 1.25, fill=True, color="0.5"))
ax.plot([0], [0], "k.")
ax.text(0.15, 0.6, "rod", fontsize=10)
arrow(ax, (1.0, -0.9), (1.35, 0.1), connectionstyle="arc3,rad=0.25")
ax.text(1.25, -0.75, r"$\omega_i$")
ax.set_xlim(-1.4, 1.7)
ax.set_ylim(-1.4, 1.4)
save(fig, "q15-rod-mgr")

print(f"Wrote figures to {OUT}")
