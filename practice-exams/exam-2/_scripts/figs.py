"""Reusable, parameterized diagrams for the professor-style practice exams (2-7 on).

Each function returns a drawing function f(ax) for examlib's question dicts.
Labels are passed in, so the same template serves different numbers.
"""
import numpy as np
from matplotlib.patches import Circle, Ellipse, Polygon, Rectangle

from examlib import arrow, block_on, dim, disk_top_view, hanging_pulley, incline


def halfpipe(left, patch, right):
    def f(ax):
        x = np.linspace(-1, 1, 400)
        y = np.where(np.abs(x) > 0.55, ((np.abs(x) - 0.55) / 0.45) ** 2 * 2.2, 0)
        ax.plot(x * 3, y, "k", lw=1.5)
        ax.plot([-0.9, 0.9], [0, 0], color="0.4", lw=5, solid_capstyle="butt")
        ax.text(0, -0.5, patch, ha="center", fontsize=10)
        ax.text(-3.4, 1.6, left, ha="right", fontsize=10)
        ax.text(3.2, 1.2, right, fontsize=10)
        ax.text(-2.1, 1.2, r"$\mu=0$", fontsize=9); ax.text(1.35, 1.2, r"$\mu=0$", fontsize=9)
        ax.set_xlim(-5.0, 4.9); ax.set_ylim(-0.8, 2.4)
    return f


def ledge_projectile(h, v0, ang):
    def f(ax):
        ax.plot([-0.8, 0, 0, 7], [2, 2, 0, 0], "k", lw=1.5)
        t = np.linspace(0, 2.4, 100)
        ax.plot(t * 2.4, 2 + t * 2.4 * 0.6 - 0.5 * (t * 2.4) ** 2 * 0.17, "k--", lw=1)
        arrow(ax, (0, 2), (1.1, 2.75)); ax.text(0.9, 3.0, v0, fontsize=10); ax.text(0.8, 2.12, ang, fontsize=10)
        dim(ax, (-0.4, 0), (-0.4, 2), h, offset=(-0.5, 0), fontsize=10)
        ax.plot([4.1, 4.1], [0, 3.05], "k", lw=1); ax.text(4.25, 1.5, r"$H=?$")
        ax.set_xlim(-1.5, 7); ax.set_ylim(-0.2, 3.5)
    return f


def loop(left_label=None, ramp=False, mark=r"$v_{\min}=?$", top_mark=None, bottom_mark=None):
    def f(ax):
        ax.add_patch(Circle((1.3, 1.0), 1.0, fill=False, lw=1.5))
        ax.plot([1.3, 2.0], [1.0, 1.7], "k", lw=1); ax.text(1.7, 1.15, r"$R$")
        if ramp:
            x = np.linspace(0, 2.2, 100); ax.plot(x - 2.2, 3.0 * (1 - x / 2.2) ** 2, "k", lw=1.5)
            ax.plot([0, 2.6], [0, 0], "k", lw=1.5)
            ax.add_patch(Rectangle((-2.2, 2.95), 0.3, 0.22, fill=False, lw=1.5))
            dim(ax, (-2.5, 0), (-2.5, 3.0), left_label or r"$h$", offset=(-0.45, 0), fontsize=10)
            xmin = -3.3
        else:
            ax.plot([-1.6, 2.6], [0, 0], "k", lw=1.5)
            ax.add_patch(Rectangle((0.0, 0), 0.25, 0.2, fill=False, lw=1.5))
            arrow(ax, (-1.2, 0.35), (-0.1, 0.35)); ax.text(-1.5, 0.55, mark, fontsize=10)
            xmin = -1.8
        if top_mark:
            ax.text(1.0, 2.15, top_mark, fontsize=10)
        if bottom_mark:
            arrow(ax, (1.3, 0.05), (1.3, 0.7)); ax.text(0.35, 0.3, bottom_mark, fontsize=10)
        ax.set_xlim(xmin, 2.8); ax.set_ylim(-0.2, 3.4 if ramp else 2.4)
    return f


def slope_block(theta_deg, direction, speed, mu, extra=None):
    """direction: 'up' or 'down' (motion along the slope)."""
    def f(ax):
        up, top, n = incline(ax, theta_deg, 5.5, origin=(5.5, 0))
        pos = 0.9 if direction == "up" else 4.2
        c = block_on(ax, np.array([5.5, 0]) + up * pos, up, n, size=0.5)
        sgn = 1 if direction == "up" else -1
        arrow(ax, c + sgn * up * 0.4 + n * 0.45, c + sgn * up * 1.4 + n * 0.45)
        ax.text(*(c + sgn * up * 0.3 + n * 1.0), speed, fontsize=10)
        ax.text(4.3, 0.12, rf"${theta_deg}^\circ$", fontsize=10)
        ax.text(1.6, 0.3, mu, fontsize=10)
        if extra:
            ax.text(*(c + sgn * up * 2.4 + n * 1.0), extra, fontsize=10)
        hmax = 5.5 * np.sin(np.radians(theta_deg))
        ax.set_xlim(0, 5.8); ax.set_ylim(-0.2, hmax + 0.6)
    return f


def ramp_spring(h_label, k_label):
    def f(ax):
        x = np.linspace(0, 1.6, 100); ax.plot(x, 1.6 * (1 - x / 1.6) ** 2, "k", lw=1.5)
        ax.plot([1.6, 4.4], [0, 0], "k", lw=1.5); ax.plot([4.4, 4.4], [0, 0.6], "k", lw=2)
        xs = np.linspace(3.4, 4.4, 200); ax.plot(xs, 0.2 + 0.1 * np.sin((xs - 3.4) * 2 * np.pi * 7), "k", lw=1.2)
        ax.add_patch(Rectangle((0.05, 1.5), 0.3, 0.25, fill=False, lw=1.5)); ax.text(0.5, 1.75, r"$v_i=0$", fontsize=10)
        dim(ax, (-0.3, 0), (-0.3, 1.5), h_label, offset=(-0.4, 0), fontsize=10)
        ax.text(3.5, 0.5, k_label, fontsize=10); ax.text(2.0, 0.6, r"$\mu=0$", fontsize=10)
        ax.text(3.3, -0.4, r"$x=?$", fontsize=10)
        ax.set_xlim(-1.0, 4.6); ax.set_ylim(-0.6, 2.0)
    return f


def vertical_spring(h_label, note):
    def f(ax):
        ys = np.linspace(0, 0.9, 200); ax.plot(0.25 * np.sin(ys * 2 * np.pi * 9), ys, "k", lw=1.2)
        ax.plot([-0.8, 0.8], [0, 0], "k", lw=2); ax.add_patch(Circle((0, 1.05), 0.15, fill=False, lw=1.5))
        ax.plot([0.5, 1.1], [1.05, 1.05], "k:", lw=1); ax.plot([0.5, 1.1], [2.3, 2.3], "k:", lw=1)
        dim(ax, (0.95, 1.05), (0.95, 2.3), h_label, offset=(0.5, 0), fontsize=10)
        ax.text(-1.35, 0.45, note, fontsize=8, rotation=90, va="center")
        ax.set_xlim(-1.6, 1.9); ax.set_ylim(-0.1, 2.5)
    return f


def two_balls(left, right, left_v="right", right_v=None, r1=0.35, r2=0.35):
    def f(ax):
        ax.add_patch(Circle((0, 0), r1, fill=False, lw=1.5)); ax.add_patch(Circle((3, 0), r2, fill=False, lw=1.5))
        arrow(ax, (r1 + 0.1, 0), (r1 + 1.0, 0))
        if right_v == "left":
            arrow(ax, (3 - r2 - 0.1, 0), (3 - r2 - 0.9, 0))
        elif right_v == "right":
            arrow(ax, (3 + r2 + 0.05, 0), (3 + r2 + 0.6, 0))
        ax.text(0, -0.8, left, ha="center"); ax.text(3, -0.8, right, ha="center")
        ax.set_xlim(-0.9, 4.1); ax.set_ylim(-1.1, 0.6)
    return f


def carts(left, right, lv, rv, rv_dir=None):
    def f(ax):
        ax.plot([-0.3, 6], [0, 0], "k", lw=1.5)
        for x0, w, lab in [(0, 1.2, left), (3.4, 1.8, right)]:
            ax.add_patch(Rectangle((x0, 0.15), w, 0.6, fill=False, lw=1.5)); ax.text(x0 + w / 2, 0.45, lab, ha="center", va="center", fontsize=9)
        arrow(ax, (1.3, 0.45), (2.2, 0.45)); ax.text(1.4, 0.95, lv, fontsize=10)
        if rv_dir == "left":
            arrow(ax, (3.3, 0.45), (2.6, 0.45)); ax.text(2.6, 0.95, rv, fontsize=10)
        elif rv_dir == "right":
            arrow(ax, (5.3, 0.45), (6.0, 0.45)); ax.text(5.0, 0.95, rv, fontsize=10)
        else:
            ax.text(3.9, 0.95, rv, fontsize=10)
        ax.set_xlim(-0.4, 6.3); ax.set_ylim(-0.1, 1.2)
    return f


def ballistic(label=r"$m,\ v=?$", h=r"$h$"):
    def f(ax):
        ax.plot([1.2, 3.2], [3, 3], "k", lw=2); ax.plot([1.8, 1.8], [3, 1.4], "k", lw=1); ax.plot([2.6, 2.6], [3, 1.4], "k", lw=1)
        ax.add_patch(Rectangle((1.5, 0.4), 1.4, 1.0, fill=False, lw=1.5)); ax.text(2.2, 0.9, r"$M$", ha="center", va="center")
        ax.add_patch(Rectangle((2.6, 0.85), 1.4, 1.0, fill=False, lw=1, ls="--"))
        ax.plot([3.1, 4.4], [0.4, 0.4], "k:", lw=1); ax.plot([3.1, 4.4], [0.85, 0.85], "k:", lw=1)
        dim(ax, (4.25, 0.4), (4.25, 0.85), h, offset=(0.4, 0))
        ax.add_patch(Ellipse((0.2, 0.9), 0.35, 0.14, fill=True, color="k")); arrow(ax, (0.45, 0.9), (1.2, 0.9)); ax.text(0.0, 1.15, label, fontsize=10)
        ax.set_xlim(-0.2, 4.9); ax.set_ylim(0.2, 3.2)
    return f


def pulley_one(label, v_label=r"$v_i=0$", thick=False):
    def f(ax):
        hanging_pulley(ax, center=(0, 2), r=0.7, mass_label=r"$m$", thick=thick)
        ax.text(0.8, 2.7, label, fontsize=10)
        arrow(ax, (-0.25, 0.6), (-0.25, 0.0)); ax.text(-0.15, 0.2, v_label, fontsize=9)
        ax.set_xlim(-1.4, 2.8); ax.set_ylim(-0.1, 2.9)
    return f


def atwood(m1, m2, extra=None):
    def f(ax):
        ax.plot([-1.3, 1.3], [3.2, 3.2], "k", lw=2); ax.plot([0, 0], [3.2, 2.55], "k", lw=1)
        hanging_pulley(ax, center=(0, 2.0), r=0.55, mass_label=m1, other=m2)
        if extra:
            ax.text(0.7, 2.5, extra, fontsize=9)
        ax.set_xlim(-1.5, 1.6); ax.set_ylim(0.0, 3.3)
    return f


def rolling(theta_label, what=r"$v,\ \omega=?$", h_label=r"$h$"):
    def f(ax):
        up, top, n = incline(ax, 20, 6, origin=(6, 0))
        c0 = top - up * 0.6 + n * 0.35; ax.add_patch(Circle(c0, 0.35, fill=False, lw=1.5)); ax.text(c0[0] + 0.45, c0[1] + 0.35, r"$v_i=0$")
        c1 = np.array([6, 0]) + up * 1.2 + n * 0.35; ax.add_patch(Circle(c1, 0.35, fill=False, lw=1.5, ls="--")); ax.text(c1[0] - 0.4, c1[1] + 0.55, what)
        dim(ax, (top[0] - 0.3, 0), (top[0] - 0.3, top[1]), h_label, offset=(-0.5, 0), fontsize=10)
        ax.text(4.9, 0.12, theta_label, fontsize=10)
        ax.set_xlim(-1.3, 6.3); ax.set_ylim(-0.2, 2.6)
    return f


def rolling_accel(theta_label):
    def f(ax):
        up, top, n = incline(ax, 25, 5, origin=(5, 0))
        c1 = np.array([5, 0]) + up * 2.6 + n * 0.4
        ax.add_patch(Circle(c1, 0.4, fill=False, lw=1.5)); ax.plot(*c1, "k.")
        arrow(ax, c1 - up * 0.5 + n * 0.6, c1 - up * 1.5 + n * 0.6); ax.text(*(c1 - up * 1.7 + n * 0.9), r"$a=?$")
        ax.text(3.9, 0.12, theta_label, fontsize=10)
        ax.set_xlim(0.4, 5.3); ax.set_ylim(-0.2, 2.7)
    return f


def incline_disk_pulley(theta_label, mu_label, v_label):
    def f(ax):
        t = np.radians(25)
        ax.add_patch(Polygon([(0, 2.6), (5.6, 0), (0, 0)], closed=True, fill=False, lw=1.5))
        down = np.array([np.cos(t), -np.sin(t)]); n = np.array([np.sin(t), np.cos(t)])
        pc = np.array([0.0, 2.6]) + n * 0.45; ax.add_patch(Circle(pc, 0.35, fill=False, lw=1.5)); ax.plot(*pc, "k.")
        b0 = np.array([0, 2.6]) + down * 2.2; c = block_on(ax, b0, down, n, size=0.6)
        ax.plot([pc[0] + n[0] * 0.35, b0[0] + n[0] * 0.3], [pc[1] + n[1] * 0.35, b0[1] + n[1] * 0.3], "k", lw=1)
        arrow(ax, c + down * 0.5, c + down * 1.4); ax.text(*(c + down * 1.0 + n * 0.5), v_label, fontsize=10)
        ax.text(4.4, 0.1, theta_label, fontsize=10); ax.text(1.9, 0.6, mu_label, fontsize=10); ax.text(pc[0] - 0.7, pc[1] + 0.4, "disk", fontsize=9)
        ax.set_xlim(-0.9, 5.8); ax.set_ylim(-0.2, 3.6)
    return f


def incline_hanging(theta_label, mu_label, v_label, m1_dir="up"):
    def f(ax):
        t = np.radians(28)
        ax.add_patch(Polygon([(0, 0), (4.4, 4.4 * np.tan(t)), (4.4, 0)], closed=True, fill=False, lw=1.5))
        upv = np.array([np.cos(t), np.sin(t)]); nv = np.array([-np.sin(t), np.cos(t)])
        pc = np.array([4.4, 4.4 * np.tan(t)]) + np.array([0.25, 0.25]); ax.add_patch(Circle(pc, 0.25, fill=False, lw=1.5))
        b0 = upv * 1.4; c = block_on(ax, b0, upv, nv, size=0.6, label=r"$m_1$")
        ax.plot([b0[0] + upv[0] * 0.6 + nv[0] * 0.3, pc[0] - 0.05], [b0[1] + upv[1] * 0.6 + nv[1] * 0.3, pc[1] + 0.24], "k", lw=1)
        ax.plot([pc[0] + 0.25] * 2, [pc[1], 0.9], "k", lw=1)
        ax.add_patch(Rectangle((pc[0] + 0.02, 0.45), 0.46, 0.45, fill=False, lw=1.5)); ax.text(pc[0] + 0.25, 0.67, r"$m_2$", ha="center", va="center", fontsize=9)
        s = 1 if m1_dir == "up" else -1
        arrow(ax, c + s * upv * 0.2 + nv * 0.55, c + s * upv * 1.0 + nv * 0.55); ax.text(*(c + nv * 1.1 - upv * 0.6), v_label, fontsize=10)
        ax.text(0.9, 0.08, theta_label, fontsize=10); ax.text(2.4, 0.3, mu_label, fontsize=10)
        ax.set_xlim(-0.2, 5.3); ax.set_ylim(-0.2, 3.0)
    return f


def stacked_disks(bottom, top, top_sign="-"):
    def f(ax):
        ax.plot([0, 0], [-0.3, 2.6], "k", lw=1)
        ax.add_patch(Ellipse((0, 0.4), 3.2, 0.7, fill=False, lw=1.5)); ax.add_patch(Ellipse((0, 1.9), 2.4, 0.5, fill=False, lw=1.5))
        arrow(ax, (0.9, 0.0), (1.4, 0.15), connectionstyle="arc3,rad=0.2"); ax.text(1.6, 0.35, bottom, fontsize=10)
        if top_sign == "-":
            arrow(ax, (-0.8, 1.65), (-1.3, 1.78), connectionstyle="arc3,rad=-0.2")
        ax.text(1.3, 2.0, top, fontsize=10)
        arrow(ax, (0.5, 1.5), (0.5, 0.9), lw=1)
        ax.set_xlim(-2.2, 2.9); ax.set_ylim(-0.4, 2.6)
    return f


def mgr_runner(v_label, at_rim=True):
    def f(ax):
        disk_top_view(ax, (0, 0), 1.2)
        ax.plot([0, 0], [0, -1.2], "k", lw=1); ax.text(0.08, -0.6, r"$R$")
        arrow(ax, (-2.4, -1.2), (-0.15, -1.2)); ax.add_patch(Circle((-2.6, -1.2), 0.12, fill=True, color="k"))
        ax.text(-2.5, -0.9, v_label, fontsize=10)
        arrow(ax, (0.9, 0.85), (0.2, 1.2), connectionstyle="arc3,rad=0.25"); ax.text(0.95, 1.0, r"$\omega_i$")
        ax.set_xlim(-2.9, 1.5); ax.set_ylim(-1.5, 1.5)
    return f


def mgr_walk_in():
    def f(ax):
        for cx, (px, py), lab in [(0, (0, -0.85), r"$\omega_i$"), (2.6, (2.6, 0), r"$\omega_f=?$")]:
            disk_top_view(ax, (cx, 0), 0.9); ax.add_patch(Circle((px, py), 0.09, fill=True, color="k")); ax.text(cx + 0.65, 0.85, lab)
        arrow(ax, (1.0, 0), (1.6, 0))
        ax.set_xlim(-1.1, 3.9); ax.set_ylim(-1.1, 1.2)
    return f


def mgr_rod():
    def f(ax):
        disk_top_view(ax, (0, 0), 1.25)
        ax.add_patch(Rectangle((-0.06, 0), 0.12, 1.25, fill=True, color="0.5")); ax.text(0.15, 0.6, "rod", fontsize=10)
        arrow(ax, (1.0, -0.9), (1.35, 0.1), connectionstyle="arc3,rad=0.25"); ax.text(1.25, -0.75, r"$\omega_i$")
        ax.set_xlim(-1.4, 1.7); ax.set_ylim(-1.4, 1.4)
    return f


def wheel(note):
    def f(ax):
        ax.add_patch(Circle((0, 0), 1.0, fill=False, lw=1.5))
        for a in np.radians([0, 60, 120, 180, 240, 300]):
            ax.plot([0, np.cos(a)], [0, np.sin(a)], "k", lw=0.8)
        arrow(ax, (1.25, -0.3), (0.5, 1.2), connectionstyle="arc3,rad=0.45"); ax.text(1.2, 0.9, r"$\omega$")
        ax.text(-1.3, -1.4, note, fontsize=9)
        ax.set_xlim(-1.4, 1.7); ax.set_ylim(-1.6, 1.3)
    return f


def wall_bounce(v_in, v_out):
    def f(ax):
        ax.plot([3.0, 3.0], [-0.8, 0.8], "k", lw=2)
        for k in range(8):
            ax.plot([3.0, 3.2], [-0.8 + k * 0.2, -0.6 + k * 0.2], "k", lw=0.8)
        ax.add_patch(Circle((2.7, 0), 0.25, fill=False, lw=1.5))
        arrow(ax, (0.6, 0.3), (2.2, 0.3)); arrow(ax, (2.2, -0.3), (0.6, -0.3))
        ax.text(1.4, 0.55, v_in, ha="center", fontsize=10); ax.text(1.4, -0.7, v_out, ha="center", fontsize=10)
        ax.set_xlim(0.3, 3.4); ax.set_ylim(-1.0, 0.9)
    return f


def stairs(h_label, t_label):
    def f(ax):
        xs, ys = [0], [0]
        for i in range(6):
            xs += [i * 0.5, (i + 1) * 0.5]; ys += [(i + 1) * 0.4, (i + 1) * 0.4]
        ax.plot(xs, ys, "k", lw=1.5); ax.plot([0, 3.0], [0, 0], "k", lw=1.5)
        ax.add_patch(Circle((0.25, 0.75), 0.12, fill=True, color="k")); ax.plot([0.25, 0.25], [0.63, 0.4], "k", lw=2)
        dim(ax, (3.2, 0), (3.2, 2.4), h_label, offset=(0.45, 0), fontsize=10)
        ax.text(0.2, 2.2, t_label, fontsize=10)
        ax.set_xlim(-0.2, 4.0); ax.set_ylim(-0.1, 2.6)
    return f


def coaster(h1, h2):
    def f(ax):
        x = np.linspace(0, 8, 300)
        y = 3.0 * np.exp(-(x / 2.6) ** 2) + 1.0 * (1 - np.exp(-(x / 2.6) ** 2))
        ax.plot(x, y, "k", lw=1.5); ax.plot([0, 8], [0, 0], "k:", lw=1)
        ax.add_patch(Circle((0.2, 3.2), 0.18, fill=True, color="k")); ax.text(0.5, 3.3, r"$v=0$", fontsize=10)
        dim(ax, (-0.4, 0), (-0.4, 3.0), h1, offset=(-0.5, 0), fontsize=10)
        dim(ax, (7.7, 0), (7.7, 1.0), h2, offset=(0.55, 0), fontsize=10); ax.text(6.0, 1.4, r"$v=?$")
        ax.set_xlim(-1.5, 8.9); ax.set_ylim(-0.3, 3.7)
    return f


def flat_curve(mu_label, r_label):
    def f(ax):
        a = np.linspace(np.radians(200), np.radians(340), 100)
        for rr in (1.6, 2.1):
            ax.plot(rr * np.cos(a), rr * np.sin(a) + 2.2, "k", lw=1.5)
        ax.plot([0], [2.2], "k."); ax.plot([0, 1.85 * np.cos(np.radians(250))], [2.2, 2.2 + 1.85 * np.sin(np.radians(250))], "k--", lw=1)
        ax.text(-0.85, 1.3, r_label, fontsize=10)
        ax.add_patch(Rectangle((-0.15, 0.25), 0.3, 0.2, fill=False, lw=1.5)); arrow(ax, (0.2, 0.35), (0.9, 0.42))
        ax.text(0.6, -0.05, r"$v_{\max}=?$"); ax.text(-1.95, 0.1, mu_label, fontsize=10)
        ax.set_xlim(-2.3, 2.3); ax.set_ylim(-0.2, 2.4)
    return f
