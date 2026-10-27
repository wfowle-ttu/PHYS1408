"""Practice Exam 2-4: questions, verified answers, figures, exam and key.

Run:  python practice-exams/exam-2/_scripts/build_exam_2_4.py
"""
from math import cos, radians, sin, sqrt, tan, pi

import numpy as np
from examlib import (Circle, Ellipse, Rectangle, arrow, block_on, build, dim, disk_top_view,
                     hanging_pulley, incline, incline_right, spin_arrow)

g = 9.8
Q = []

# 1 ------------------------------------------------------------ banked v_max
t12 = tan(radians(12))
v1 = sqrt(g * 45 * (t12 + 0.30) / (1 - 0.30 * t12))


def f1(ax):
    up, top, n = incline(ax, 12, 4, origin=(4, 0))
    c = block_on(ax, np.array([4, 0]) + up * 2.0, up, n, size=0.55)
    arrow(ax, c, c + n * 1.0); ax.text(*(c + n * 1.15), r"$N$")
    arrow(ax, c, c + np.array([0, -0.9])); ax.text(c[0] + 0.1, c[1] - 0.95, r"$mg$")
    arrow(ax, c, c - up * 0.9); ax.text(*(c - up * 1.1 + np.array([0, -0.3])), r"$f_s$")
    ax.text(3.1, 0.06, r"$\theta$"); ax.text(3.0, 1.3, r"center of curve $\rightarrow$", fontsize=10)
    ax.set_xlim(-0.2, 6.3); ax.set_ylim(-0.3, 1.9)


Q.append(dict(
    stem=r"A highway curve of radius 45 m is banked at $\theta = 12^\circ$. The coefficient of static friction between the tires and the road is $\mu_s = 0.30$. What is the maximum speed at which a car can take the curve without sliding up the bank?",
    choices=["9.7 m/s", "11.5 m/s", "15.5 m/s", "21.9 m/s", "241 m/s"], key="c",
    check=("near", v1, [9.7, 11.5, 15.5, 21.9, 241], 0.05),
    value="15.5 m/s", topic="Banked curve, maximum speed", source="Ch 6 notes p. 3/7–5/7", card="Curve",
    solution=rf"""
At $v_{{max}}$ the car tends to slide **up** the bank, so friction points **down** the bank. The notecard formula with the $+$ signs:

$$v_{{max}} = \sqrt{{gr\,\frac{{\tan\theta + \mu_s}}{{1 - \mu_s\tan\theta}}}}$$

**Plug in** ($\tan 12^\circ = 0.2126$, $g = 9.8$ m/s², $r = 45$ m):

$$
\begin{{aligned}}
v_{{max}} &= \sqrt{{(9.8)(45)\,\frac{{0.2126 + 0.30}}{{1 - (0.30)(0.2126)}}}} \\[8pt]
&= \sqrt{{441 \times \frac{{0.5126}}{{0.9362}}}} = \sqrt{{241.4}} = 15.5\ \text{{m/s}}
\end{{aligned}}
$$
""",
    distract=["a) 9.7 is the frictionless bank, $\\sqrt{gr\\tan\\theta}$.",
              "b) 11.5 is the flat-curve formula, $\\sqrt{\\mu_s gr}$.",
              "d) 21.9 multiplies by an extra $\\sqrt2$.",
              "e) 241 forgets the square root."],
    fig=f1, figsize=(4.0, 1.8)))

# 2 ------------------------------------------------------------ loop launch height (min trap)
h2 = 2.5 * 7.5


def f2(ax):
    x = np.linspace(0, 2.2, 100)
    ax.plot(x - 2.2, 3.0 * (1 - x / 2.2) ** 2, "k", lw=1.5)
    ax.plot([0, 2.6], [0, 0], "k", lw=1.5)
    ax.add_patch(Circle((1.3, 1.0), 1.0, fill=False, lw=1.5))
    ax.add_patch(Rectangle((-2.2, 2.95), 0.3, 0.22, fill=False, lw=1.5))
    dim(ax, (-2.5, 0), (-2.5, 3.0), r"$h=?$", offset=(-0.35, 0))
    ax.plot([1.3, 2.0], [1.0, 1.7], "k", lw=1); ax.text(1.75, 1.2, r"$R$")
    ax.set_xlim(-3.1, 2.7); ax.set_ylim(-0.2, 3.4)


Q.append(dict(
    stem=r"A roller coaster car starts from rest on a frictionless track and enters a vertical circular loop of radius $R = 7.5$ m. What is the minimum starting height (measured from the bottom of the loop) for the car to make it all the way around the loop?",
    choices=["11 m", "15 m", "18 m", "20 m", "38 m"], key="d",
    check=("min", h2, [11, 15, 18, 20, 38]),
    value="18.75 m → 20", topic="Loop-the-loop, minimum launch height", source="Ch 7/8 notes p. 12/18–13/18", card="Loop",
    solution=r"""
**Top of the loop:** "barely" means $N = 0$, so $mg = \dfrac{mv_t^2}{R}$ and $v_t^2 = gR$.

**Energy, start to top** ($E_i = E_f$; the top is $2R$ high):

$$E_i = mgh \qquad\qquad E_f = mg(2R) + \tfrac12 mv_t^2$$

$$
\begin{aligned}
mgh &= 2mgR + \tfrac12 m(gR) \\[8pt]
h &= \tfrac52 R
\end{aligned}
$$

**Plug in:**

$$h = \tfrac52(7.5) = 18.75\ \text{m}$$

**Answer-choice trap.** 18.75 m is a **minimum**. Starting at 18 m, the car falls off the track, even though 18 is the closest number. The smallest choice that works is **d) 20 m**.
""",
    distract=["a) 11 m is $\\tfrac32 R$.", "b) 15 m is $2R$: it reaches the top with zero speed and falls.",
              "c) 18 m is the nearest number, but it's below the minimum.", "e) 38 m is $5R$ (mixing up $v_b^2 = 5gR$ with a height)."],
    fig=f2, figsize=(3.6, 2.3)))

# 3 ------------------------------------------------------------ halfpipe, find mu
mu3 = (4.0 - 3.1) / 6.0


def f3(ax):
    x = np.linspace(-1, 1, 400)
    y = np.where(np.abs(x) > 0.55, ((np.abs(x) - 0.55) / 0.45) ** 2 * 2.2, 0)
    ax.plot(x * 3, y, "k", lw=1.5)
    ax.plot([-0.9, 0.9], [0, 0], color="0.4", lw=5, solid_capstyle="butt")
    ax.text(0, -0.5, r"$L = 6.0$ m,  $\mu = ?$", ha="center")
    ax.text(-3.4, 1.6, r"$h_i = 4.0$ m", ha="right", fontsize=10)
    ax.text(3.2, 1.2, r"$h_f = 3.1$ m", fontsize=10)
    ax.set_xlim(-4.8, 4.9); ax.set_ylim(-0.8, 2.4)


Q.append(dict(
    stem=r"A skateboarder starts from rest 4.0 m up one wall of a halfpipe. The halfpipe is frictionless except for a 6.0 m long rough section of the flat bottom. After one pass across the rough section, she rises to a height of 3.1 m on the far wall. What is the coefficient of kinetic friction of the rough section?",
    choices=["0.15", "0.52", "0.67", "0.78", "0.90"], key="a",
    check=("near", mu3, [0.15, 0.52, 0.67, 0.78, 0.90], 0.005),
    value="0.15", topic="Halfpipe, find $\\mu$", source="Ch 7/8 notes p. 4/18–5/18", card="Halfpipe",
    solution=r"""
Notecard (from rest, one crossing): $h_f = h_i - \mu L$. **Solve for $\mu$:**

$$
\begin{aligned}
\mu L &= h_i - h_f \\[8pt]
\mu &= \frac{h_i - h_f}{L}
\end{aligned}
$$

**Plug in:**

$$\mu = \frac{4.0 - 3.1}{6.0} = \frac{0.9}{6.0} = 0.15$$
""",
    distract=["b) 0.52 is $h_f/L$.", "c) 0.67 is $h_i/L$.", "d) 0.78 is $h_f/h_i$.", "e) 0.90 is the height lost, not divided by $L$."],
    fig=f3, figsize=(4.2, 2.0)))

# 4 ------------------------------------------------------------ sliding down rough incline, speed
s35, c35 = sin(radians(35)), cos(radians(35))
v4 = sqrt(4 + 2 * g * 3 * (s35 - 0.25 * c35))


def f4(ax):
    up, top, n = incline(ax, 35, 5, origin=(5, 0))
    c = block_on(ax, np.array([5, 0]) + up * 4.0, up, n, size=0.5)
    arrow(ax, c - up * 0.4 + n * 0.5, c - up * 1.4 + n * 0.5)
    ax.text(*(c - up * 0.3 + n * 1.0), r"$v_i = 2.0$ m/s", fontsize=10)
    ax.text(4.0, 0.12, r"$35^\circ$", fontsize=10); ax.text(2.2, 0.4, r"$\mu_k = 0.25$", fontsize=10)
    ax.set_xlim(0.6, 5.3); ax.set_ylim(-0.2, 3.4)


Q.append(dict(
    stem=r"A block slides **down** a $35^\circ$ incline ($\mu_k = 0.25$) with an initial speed of 2.0 m/s. How fast is it moving after it has slid 3.0 m along the incline?",
    choices=["2.0 m/s", "3.85 m/s", "4.66 m/s", "4.80 m/s", "5.07 m/s"], key="e",
    check=("near", v4, [2.0, 3.85, 4.66, 4.80, 5.07], 0.005),
    value="5.07 m/s", topic="Sliding down a rough incline", source="Ch 7/8 notes p. 10/18", card="One block on incline (Down)",
    solution=rf"""
Notecard, sliding **down**:

$$v_f = \sqrt{{v_i^2 + 2g\,\Delta x(\sin\theta - \mu\cos\theta)}}$$

**Plug in** ($\sin 35^\circ = 0.5736$, $\cos 35^\circ = 0.8192$, $\Delta x = 3.0$ m along the slope):

$$
\begin{{aligned}}
v_f &= \sqrt{{2.0^2 + 2(9.8)(3.0)\left(0.5736 - 0.25 \times 0.8192\right)}} \\[8pt]
&= \sqrt{{4.0 + 58.8(0.3688)}} = \sqrt{{4.0 + 21.68}} = \sqrt{{25.68}} = 5.07\ \text{{m/s}}
\end{{aligned}}
$$

The bracket is positive, so the block speeds up.
""",
    distract=["a) 2.0 m/s assumes the speed doesn't change.", "b) 3.85 forgets the 2 in $2g$.",
              "c) 4.66 forgets $v_i^2$.", "d) 4.80 uses friction $\\mu mg$ instead of $\\mu mg\\cos\\theta$."],
    fig=f4, figsize=(3.4, 2.4)))

# 5 ------------------------------------------------------------ spring compression from a moving block
x5 = sqrt(1.5 * 4.0 ** 2 / 600)


def f5(ax):
    ax.plot([0, 4.4], [0, 0], "k", lw=1.5); ax.plot([4.4, 4.4], [0, 0.7], "k", lw=2)
    xs = np.linspace(3.3, 4.4, 200); ax.plot(xs, 0.25 + 0.12 * np.sin((xs - 3.3) * 2 * np.pi * 7), "k", lw=1.2)
    ax.add_patch(Rectangle((0.6, 0.02), 0.5, 0.45, fill=False, lw=1.5)); ax.text(0.85, 0.25, r"$m$", ha="center", va="center")
    arrow(ax, (1.3, 0.25), (2.2, 0.25)); ax.text(1.3, 0.55, r"$4.0$ m/s", fontsize=10)
    ax.text(3.5, 0.6, r"$k$", fontsize=11); ax.text(1.8, -0.35, r"$\mu = 0$", fontsize=10)
    ax.set_xlim(0.3, 4.6); ax.set_ylim(-0.5, 0.9)


Q.append(dict(
    stem=r"A 1.5 kg block slides at 4.0 m/s along a frictionless floor into a spring with $k = 600$ N/m. How far is the spring compressed when the block comes to rest?",
    choices=["0.010 m", "0.040 m", "0.14 m", "0.20 m", "0.28 m"], key="d",
    check=("near", x5, [0.010, 0.040, 0.14, 0.20, 0.28], 0.005),
    value="0.20 m", topic="Spring stops a sliding mass", source="Ch 7/8 notes p. 11/18", card="Spring",
    solution=r"""
Level floor, so $h = 0$. The notecard's "stop a mass" line becomes

$$x = \sqrt{\frac{2mgh + mv_i^2}{k}} = \sqrt{\frac{mv_i^2}{k}}$$

(That's $\tfrac12 kx^2 = \tfrac12 mv_i^2$: all the KE becomes spring PE.)

**Plug in:**

$$x = \sqrt{\frac{(1.5)(4.0)^2}{600}} = \sqrt{\frac{24}{600}} = \sqrt{0.040} = 0.20\ \text{m}$$
""",
    distract=["a) 0.010 is $mv/k$ (momentum, not energy).", "b) 0.040 forgets the square root.",
              "c) 0.14 drops a $\\tfrac12$ on one side only.", "e) 0.28 has an extra factor of 2."],
    fig=f5, figsize=(3.8, 1.2)))

# 6 ------------------------------------------------------------ power = F v
P6 = 250 * g * 1.2


def f6(ax):
    ax.plot([-1, 1], [3, 3], "k", lw=2); ax.plot([0, 0], [3, 1.2], "k", lw=1)
    ax.add_patch(Rectangle((-0.5, 0.4), 1.0, 0.8, fill=False, lw=1.5)); ax.text(0, 0.8, "250 kg", ha="center", va="center", fontsize=9)
    arrow(ax, (0.8, 0.6), (0.8, 1.6)); ax.text(0.95, 1.0, r"$1.2$ m/s", fontsize=10)
    ax.set_xlim(-1.2, 2.0); ax.set_ylim(0.2, 3.2)


Q.append(dict(
    stem=r"A motor lifts a 250 kg crate straight up at a constant speed of 1.2 m/s. What power does the motor deliver?",
    choices=["180 W", "300 W", "2940 W", "5880 W", "29,400 W"], key="c",
    check=("near", P6, [180, 300, 2940, 5880, 29400], 5),
    value="2940 W", topic="Power, $P = Fv$", source="Ch 7/8 notes p. 14/18", card="Power",
    solution=r"""
At constant speed the motor's force equals the weight, $F = mg$. Notecard: $P = Fv$.

$$P = Fv = mgv$$

**Plug in:**

$$P = (250)(9.8)(1.2) = 2940\ \text{W}$$
""",
    distract=["a) 180 W is $\\tfrac12 mv^2$ (energy, not power).", "b) 300 is $mv$ (momentum).",
              "d) 5880 doubles it.", "e) 29,400 uses 12 m/s."],
    fig=f6, figsize=(2.4, 2.2)))

# 7 ------------------------------------------------------------ incline + hanging mass + disk pulley
s20, c20 = sin(radians(20)), cos(radians(20))
B7 = 5 - 6 * s20 - 0.20 * 6 * c20
v7 = sqrt(2 * g * 1.2 * B7 / (6 + 5 + 2))


def f7(ax):
    t = radians(20)
    ax.add_patch(__import__("matplotlib").patches.Polygon([(0, 0), (4.4, 4.4 * np.tan(t)), (4.4, 0)], closed=True, fill=False, lw=1.5))
    upv = np.array([np.cos(t), np.sin(t)]); nv = np.array([-np.sin(t), np.cos(t)])
    pc = np.array([4.4, 4.4 * np.tan(t)]) + np.array([0.3, 0.3])
    ax.add_patch(Circle(pc, 0.3, fill=False, lw=1.5)); ax.plot(*pc, "k.")
    b0 = upv * 1.4; c = block_on(ax, b0, upv, nv, size=0.6, label=r"$m_1$")
    ax.plot([b0[0] + upv[0] * 0.6 + nv[0] * 0.3, pc[0] - 0.05], [b0[1] + upv[1] * 0.6 + nv[1] * 0.3, pc[1] + 0.29], "k", lw=1)
    ax.plot([pc[0] + 0.3] * 2, [pc[1], 0.75], "k", lw=1)
    ax.add_patch(Rectangle((pc[0] + 0.05, 0.3), 0.5, 0.45, fill=False, lw=1.5)); ax.text(pc[0] + 0.3, 0.52, r"$m_2$", ha="center", va="center", fontsize=9)
    ax.text(0.8, 0.08, r"$20^\circ$", fontsize=10); ax.text(2.2, 0.25, r"$\mu_k = 0.20$", fontsize=10)
    ax.text(pc[0] + 0.4, pc[1] + 0.3, "disk", fontsize=9)
    ax.set_xlim(-0.2, 5.6); ax.set_ylim(-0.2, 2.4)


Q.append(dict(
    stem=r"A 6.0 kg block on a $20^\circ$ incline ($\mu_k = 0.20$) is tied by a light string over a pulley to a 5.0 kg hanging mass. The pulley is a uniform disk ($I = \tfrac12 MR^2$, $M = 4.0$ kg). The system is released from rest, and the hanging mass falls. How fast is it moving after it has fallen 1.2 m?",
    choices=["1.69 m/s", "1.81 m/s", "1.97 m/s", "2.31 m/s", "4.85 m/s"], key="b",
    check=("near", v7, [1.69, 1.81, 1.97, 2.31, 4.85], 0.005),
    value="1.81 m/s", topic="Incline + hanging mass + disk pulley", source="Ch 7/8 notes p. 15/18; 2015 Exam 2 #13", card="Incline + hanging mass + pulley",
    solution=rf"""
Notecard, with $m_2$ falling ($m_1$ slides **up** the slope):

$$v_f = \sqrt{{v_i^2 + \frac{{2g\,\Delta x\,B}}{{m_1 + m_2 + I/R^2}}}}, \qquad B = m_2 - m_1\sin\theta - \mu m_1\cos\theta$$

**Net pull** ($\sin 20^\circ = 0.3420$, $\cos 20^\circ = 0.9397$):

$$B = 5.0 - 6.0(0.3420) - 0.20(6.0)(0.9397) = 5.0 - 2.052 - 1.128 = 1.820\ \text{{kg}}$$

**Pulley term:** a disk has $I/R^2 = \tfrac12 M = 2.0$ kg.

**Plug in** ($v_i = 0$, $\Delta x = 1.2$ m):

$$
\begin{{aligned}}
v_f &= \sqrt{{0 + \frac{{2(9.8)(1.2)(1.820)}}{{6.0 + 5.0 + 2.0}}}} \\[8pt]
&= \sqrt{{\frac{{42.81}}{{13.0}}}} = \sqrt{{3.293}} = 1.81\ \text{{m/s}}
\end{{aligned}}
$$
""",
    distract=["a) 1.69 treats the pulley as a ring ($I/R^2 = M$).", "c) 1.97 ignores the pulley's mass.",
              "d) 2.31 ignores friction.", "e) 4.85 is free fall, $\\sqrt{2g\\Delta x}$."],
    fig=f7, figsize=(4.2, 2.0)))

# 8 ------------------------------------------------------------ inelastic, numeric
v8 = (1500 * 25 + 2500 * 15) / 4000


def f8(ax):
    ax.plot([-0.2, 6], [0, 0], "k", lw=1.5)
    for x0, w, lab in [(0, 1.2, "1500 kg"), (3.4, 2.0, "2500 kg")]:
        ax.add_patch(Rectangle((x0, 0.15), w, 0.6, fill=False, lw=1.5)); ax.text(x0 + w / 2, 0.45, lab, ha="center", va="center", fontsize=9)
    arrow(ax, (1.3, 0.45), (2.2, 0.45)); ax.text(1.4, 0.95, r"$25$ m/s", fontsize=10)
    arrow(ax, (5.5, 0.45), (6.2, 0.45)); ax.text(4.6, 0.95, r"$15$ m/s", fontsize=10)
    ax.set_xlim(-0.3, 6.4); ax.set_ylim(-0.1, 1.2)


Q.append(dict(
    stem=r"A 1500 kg car moving at 25 m/s rear-ends a 2500 kg truck moving at 15 m/s in the same direction. They lock together. What is their speed just after the collision?",
    choices=["0 m/s", "9.4 m/s", "18.8 m/s", "20.0 m/s", "40.0 m/s"], key="c",
    check=("near", v8, [0, 9.4, 18.8, 20.0, 40.0], 0.06),
    value="18.75 m/s", topic="Completely inelastic collision", source="Ch 9 notes p. 1/5", card="Stick (inelastic)",
    solution=r"""
They stick, so momentum only. Notecard:

$$v_f = \frac{m_1v_1 + m_2v_2}{m_1 + m_2}$$

**Plug in** (both moving the same way, so both velocities are $+$):

$$v_f = \frac{(1500)(25) + (2500)(15)}{1500 + 2500} = \frac{37{,}500 + 37{,}500}{4000} = 18.75\ \text{m/s}$$
""",
    distract=["a) 0 treats the truck as moving the opposite way.", "b) 9.4 leaves out the truck's momentum.",
              "d) 20.0 averages the two speeds.", "e) 40.0 adds them."],
    fig=f8, figsize=(4.0, 0.9)))

# 9 ------------------------------------------------------------ elastic, target at rest
v9_1 = (4 - 1) * 3 / 5
v9_2 = 3 + v9_1 - 0


def f9(ax):
    ax.add_patch(Circle((0, 0), 0.45, fill=False, lw=1.5)); ax.add_patch(Circle((2.8, 0), 0.28, fill=False, lw=1.5))
    arrow(ax, (0.55, 0), (1.5, 0)); ax.text(0, -0.8, r"$4$ kg, $+3$ m/s", ha="center"); ax.text(2.8, -0.8, r"$1$ kg, at rest", ha="center")
    ax.set_xlim(-0.8, 3.8); ax.set_ylim(-1.1, 0.6)


Q.append(dict(
    stem=r"A 4.0 kg ball moving to the right at 3.0 m/s collides **elastically** head-on with a 1.0 kg ball at rest. What is the velocity of the 1.0 kg ball after the collision?",
    choices=["0 m/s", "+1.8 m/s", "+2.4 m/s", "+3.0 m/s", "+4.8 m/s"], key="e",
    check=("near", v9_2, [0, 1.8, 2.4, 3.0, 4.8], 0.05),
    value="+4.8 m/s", topic="1-D elastic collision", source="Ch 9 notes p. 2/5–3/5", card="Elastic",
    solution=r"""
Notecard formulas, right $= +$: $m_1 = 4.0$, $v_{1i} = +3.0$; $m_2 = 1.0$, $v_{2i} = 0$.

$$v_{1f} = \frac{(m_1 - m_2)v_{1i} + 2m_2v_{2i}}{m_1 + m_2} = \frac{(3.0)(3.0) + 0}{5.0} = +1.8\ \text{m/s}$$

$$v_{2f} = v_{1i} + v_{1f} - v_{2i} = 3.0 + 1.8 - 0 = +4.8\ \text{m/s}$$

A heavy ball hitting a light one sends the light one off faster than the heavy one was going.
""",
    distract=["a) 0 confuses it with the stuck ball case.", "b) +1.8 is the 4.0 kg ball's velocity.",
              "c) +2.4 is the stick-together answer.", "d) +3.0 is the equal-mass (cue ball) result."],
    fig=f9, figsize=(3.6, 1.1)))

# 10 ----------------------------------------------------------- ballistic pendulum, bullet speed
V10 = sqrt(2 * g * 0.12)
v10 = (1.5 + 0.012) / 0.012 * V10


def f10(ax):
    ax.plot([1.2, 3.2], [3, 3], "k", lw=2); ax.plot([1.8, 1.8], [3, 1.4], "k", lw=1); ax.plot([2.6, 2.6], [3, 1.4], "k", lw=1)
    ax.add_patch(Rectangle((1.5, 0.4), 1.4, 1.0, fill=False, lw=1.5)); ax.text(2.2, 0.9, r"$M$", ha="center", va="center")
    ax.add_patch(Rectangle((2.6, 0.85), 1.4, 1.0, fill=False, lw=1, ls="--"))
    ax.plot([3.1, 4.4], [0.4, 0.4], "k:", lw=1); ax.plot([3.1, 4.4], [0.85, 0.85], "k:", lw=1)
    dim(ax, (4.25, 0.4), (4.25, 0.85), r"$h$", offset=(0.3, 0))
    ax.add_patch(Ellipse((0.2, 0.9), 0.35, 0.14, fill=True, color="k")); arrow(ax, (0.45, 0.9), (1.2, 0.9)); ax.text(0.1, 1.15, r"$v = ?$")
    ax.set_xlim(-0.1, 4.8); ax.set_ylim(0.2, 3.2)


Q.append(dict(
    stem=r"A 0.012 kg bullet is fired into a 1.5 kg block of wood hanging at rest from light strings. The bullet lodges in the block, which swings up to a height of 0.12 m. What was the bullet's speed?",
    choices=["1.5 m/s", "17 m/s", "126 m/s", "193 m/s", "386 m/s"], key="d",
    check=("near", v10, [1.5, 17, 126, 193, 386], 0.6),
    value="193 m/s", topic="Ballistic pendulum, bullet speed", source="Ch 9 notes p. 5/5", card="Ballistic",
    solution=r"""
Notecard: $v = \dfrac{M + m}{m}\sqrt{2gh}$ (momentum through the hit, energy for the swing).

**Plug in:**

$$
\begin{aligned}
v &= \frac{1.5 + 0.012}{0.012}\sqrt{2(9.8)(0.12)} \\[8pt]
&= 126 \times 1.534 = 193\ \text{m/s}
\end{aligned}
$$
""",
    distract=["a) 1.5 m/s is $V = \\sqrt{2gh}$, the block's speed after the hit.",
              "b) 17 m/s uses energy conservation through the collision (never do that).",
              "c) 126 is just the mass ratio $\\frac{M+m}{m}$.", "e) 386 doubles it."],
    fig=f10, figsize=(3.4, 2.1)))

# 11 ----------------------------------------------------------- rotational kinematics, angle
th11 = (30 + 0) / 2 * 6.0


def f11(ax):
    ax.add_patch(Circle((0, 0), 1.0, fill=False, lw=1.5))
    for a in np.radians([90, 210, 330]):
        ax.add_patch(Ellipse((0.5 * np.cos(a), 0.5 * np.sin(a)), 0.9, 0.3, angle=np.degrees(a), fill=False, lw=1))
    ax.plot(0, 0, "k.")
    ax.text(-1.3, -1.4, r"$30$ rad/s $\to 0$ in $6.0$ s", fontsize=10)
    ax.set_xlim(-1.4, 1.6); ax.set_ylim(-1.6, 1.2)


Q.append(dict(
    stem=r"A ceiling fan spinning at 30 rad/s is switched off and slows uniformly to a stop in 6.0 s. Through what angle does it turn while stopping?",
    choices=["5.0 rad", "14.3 rad", "15 rad", "45 rad", "90 rad"], key="e",
    check=("near", th11, [5.0, 14.3, 15, 45, 90], 0.05),
    value="90 rad", topic="Rotational kinematics", source="Ch 10 notes p. 1/8; Ch 11 notes p. 6/8", card="Rot. kinematics",
    solution=r"""
$\alpha$ isn't given or asked for, so use the equation without it:

$$\Delta\theta = \frac{\omega_i + \omega_f}{2}\,t$$

**Plug in:**

$$\Delta\theta = \frac{30 + 0}{2}(6.0) = 15 \times 6.0 = 90\ \text{rad}$$
""",
    distract=["a) 5.0 is the angular acceleration (rad/s²).", "b) 14.3 is the answer in revolutions, $90/2\\pi$.",
              "c) 15 is the average angular velocity.", "d) 45 halves it twice."],
    fig=f11, figsize=(2.6, 2.4)))

# 12 ----------------------------------------------------------- one-mass pulley, ring
a12 = 2.0 * g / (2.0 + 3.0)


def f12(ax):
    hanging_pulley(ax, center=(0, 2), r=0.7, mass_label=r"$m$", thick=True)
    ax.text(0.8, 2.7, r"ring, $M = 3.0$ kg", fontsize=10)
    ax.set_xlim(-1.4, 2.6); ax.set_ylim(0.0, 2.9)


Q.append(dict(
    stem=r"A 2.0 kg mass hangs from a light string wrapped around a pulley that is a thin ring ($I = MR^2$, $M = 3.0$ kg) on a frictionless axle. The mass is released. What is its acceleration?",
    choices=["2.45 m/s²", "3.92 m/s²", "5.60 m/s²", "6.53 m/s²", "9.80 m/s²"], key="b",
    check=("near", a12, [2.45, 3.92, 5.60, 6.53, 9.80], 0.005),
    value="3.92 m/s²", topic="Hanging mass on a ring pulley", source="Ch 10 notes p. 4/8; 2015 Exam 2 #9", card="Atwood / mass on pulley (one mass)",
    solution=r"""
Notecard, one mass: $a = \dfrac{mg}{m + I/R^2}$. A ring has $I = MR^2$, so $I/R^2 = M$ ($R$ cancels).

$$a = \frac{mg}{m + M}$$

**Plug in:**

$$a = \frac{(2.0)(9.8)}{2.0 + 3.0} = \frac{19.6}{5.0} = 3.92\ \text{m/s}^2$$
""",
    distract=["a) 2.45 uses $I/R^2 = 2M$.", "c) 5.60 treats the pulley as a disk ($\\tfrac12 M$).",
              "d) 6.53 leaves $m$ out of the denominator.", "e) 9.80 is free fall (massless pulley, nothing holding it)."],
    fig=f12, figsize=(2.6, 2.2)))

# 13 ----------------------------------------------------------- rolling acceleration, disk
a13 = 2 / 3 * g * sin(radians(30))


def f13(ax):
    up, top, n = incline(ax, 30, 5, origin=(5, 0))
    c1 = np.array([5, 0]) + up * 2.6 + n * 0.4
    ax.add_patch(Circle(c1, 0.4, fill=False, lw=1.5)); ax.plot(*c1, "k.")
    arrow(ax, c1 - up * 0.5 + n * 0.6, c1 - up * 1.5 + n * 0.6); ax.text(*(c1 - up * 1.7 + n * 0.9), r"$a = ?$")
    ax.text(3.9, 0.12, r"$30^\circ$", fontsize=10)
    ax.set_xlim(0.4, 5.3); ax.set_ylim(-0.2, 2.9)


Q.append(dict(
    stem=r"A solid cylinder ($I = \tfrac12 MR^2$) rolls without slipping down a $30^\circ$ incline. What is the acceleration of its center?",
    choices=["2.45 m/s²", "3.27 m/s²", "3.50 m/s²", "4.90 m/s²", "6.53 m/s²"], key="b",
    check=("near", a13, [2.45, 3.27, 3.50, 4.90, 6.53], 0.005),
    value="3.27 m/s²", topic="Rolling acceleration", source="Ch 10 notes p. 3/8", card="Rolling (disk row)",
    solution=r"""
Notecard, disk (solid cylinder) row: $a = \tfrac23 g\sin\theta$.

**Plug in:**

$$a = \tfrac23(9.8)\sin 30^\circ = \tfrac23(9.8)(0.5) = 3.27\ \text{m/s}^2$$
""",
    distract=["a) 2.45 is a ring, $\\tfrac12 g\\sin\\theta$.", "c) 3.50 is a sphere, $\\tfrac57 g\\sin\\theta$.",
              "d) 4.90 is sliding, $g\\sin\\theta$.", "e) 6.53 forgets $\\sin\\theta$."],
    fig=f13, figsize=(3.2, 2.0)))

# 14 ----------------------------------------------------------- counter-rotating drop
I14a, I14b = 0.5 * 150 * 2.0 ** 2, 40 * 1.5 ** 2
w14 = (I14a * 2.5 + I14b * (-3.0)) / (I14a + I14b)


def f14(ax):
    ax.plot([0, 0], [-0.3, 2.6], "k", lw=1)
    ax.add_patch(Ellipse((0, 0.4), 3.2, 0.7, fill=False, lw=1.5)); ax.add_patch(Ellipse((0, 1.9), 2.4, 0.5, fill=False, lw=2.5))
    arrow(ax, (0.9, 0.0), (1.4, 0.15), connectionstyle="arc3,rad=0.2"); ax.text(1.6, 0.35, r"$+2.5$")
    arrow(ax, (0.9, 1.65), (1.3, 1.78), connectionstyle="arc3,rad=0.2", color="0.4"); ax.text(1.3, 2.0, r"$-3.0$", fontsize=10)
    arrow(ax, (-0.5, 1.5), (-0.5, 0.9), lw=1); ax.text(-1.8, 2.0, "ring", fontsize=10); ax.text(-2.3, 0.0, "platform", fontsize=10)
    ax.set_xlim(-2.4, 2.6); ax.set_ylim(-0.4, 2.6)


Q.append(dict(
    stem=r"A platform (a disk, $I = \tfrac12 MR^2$, $M = 150$ kg, $R = 2.0$ m) rotates at +2.5 rad/s. A thin ring ($I = mr^2$, $m = 40$ kg, $r = 1.5$ m) spinning in the **opposite** direction at −3.0 rad/s is dropped centered onto it, and the two end up turning together. What is their final angular velocity?",
    choices=["+1.23 rad/s", "+1.78 rad/s", "+1.92 rad/s", "+2.50 rad/s", "+2.62 rad/s"], key="a",
    check=("near", w14, [1.23, 1.78, 1.92, 2.50, 2.62], 0.005),
    value="+1.23 rad/s", topic="Counter-rotating object dropped on a disk", source="Ch 11 notes p. 3/8; 2015 Exam 2 #11", card="Angular momentum",
    solution=r"""
$L_i = L_f$, with the ring's $\omega_2$ **negative**. Notecard:

$$\omega_f = \frac{I_1\omega_1 + I_2\omega_2}{I_1 + I_2}$$

**Moments of inertia first:**

$$I_1 = \tfrac12(150)(2.0)^2 = 300\ \text{kg·m}^2 \qquad\qquad I_2 = (40)(1.5)^2 = 90\ \text{kg·m}^2$$

**Plug in:**

$$\omega_f = \frac{(300)(2.5) + (90)(-3.0)}{300 + 90} = \frac{750 - 270}{390} = +1.23\ \text{rad/s}$$
""",
    distract=["b) +1.78 treats the ring as a disk ($\\tfrac12 mr^2$).", "c) +1.92 ignores the ring's spin.",
              "d) +2.50 is no change.", "e) +2.62 forgets the minus sign on the ring."],
    fig=f14, figsize=(3.4, 1.9)))

# 15 ----------------------------------------------------------- walk from center to rim
w15 = 250 / (250 + 2 * 60) * 1.8


def f15(ax):
    for cx, (px, py), lab in [(0, (0, 0), r"$\omega_i = 1.8$"), (2.7, (2.7, -0.9), r"$\omega_f = ?$")]:
        disk_top_view(ax, (cx, 0), 0.9); ax.add_patch(Circle((px, py), 0.09, fill=True, color="k")); ax.text(cx - 0.5, 1.05, lab, fontsize=10)
    arrow(ax, (1.0, 0), (1.6, 0))
    ax.set_xlim(-1.1, 3.8); ax.set_ylim(-1.2, 1.4)


Q.append(dict(
    stem=r"A 60 kg person stands at the **center** of a merry-go-round (a disk, $I = \tfrac12 MR^2$, $M = 250$ kg, $R = 2.0$ m) that rotates at 1.8 rad/s. The person walks out to the rim. What is the angular velocity when the person reaches the rim? (Treat the person as a point mass.)",
    choices=["1.22 rad/s", "1.45 rad/s", "1.80 rad/s", "2.23 rad/s", "2.66 rad/s"], key="a",
    check=("near", w15, [1.22, 1.45, 1.80, 2.23, 2.66], 0.005),
    value="1.22 rad/s", topic="Person walks from the center to the rim", source="Ch 11 notes p. 7/8", card="Angular momentum (walk in/out)",
    solution=r"""
Notecard, walk in/out: $\omega_f = \dfrac{I_i}{I_f}\omega_i$. At the center the person adds nothing ($m \cdot 0^2$); at the rim they add $mR^2$.

$$\omega_f = \frac{\tfrac12 MR^2}{\tfrac12 MR^2 + mR^2}\,\omega_i = \frac{M}{M + 2m}\,\omega_i$$

(That's the notecard's rim$\to$center ratio, flipped, because they're walking **out**.)

**Plug in:**

$$\omega_f = \frac{250}{250 + 2(60)}(1.8) = \frac{250}{370}(1.8) = 1.22\ \text{rad/s}$$

Walking outward adds $I$, so the merry-go-round slows down.
""",
    distract=["b) 1.45 forgets the $\\tfrac12$ on the disk.", "c) 1.80 is no change.",
              "d) 2.23 uses $\\frac{M + m}{M}$, a speed-up.", "e) 2.66 uses the rim$\\to$center formula without flipping it (walking in, not out)."],
    fig=f15, figsize=(3.6, 1.7)))

INTRO = r"""
Practice Exam 2-4 uses the same problem types as Exams 2-1 through 2-3 with new numbers and new twists (find $\mu$ instead of a height, walk **out** instead of in, power from $Fv$, a one-mass ring pulley). Question 2 is a **minimum** trap: round up to the choice that works. The last column says which 3×5 notecard entry solves each question.
"""

if __name__ == "__main__":
    build(4, "Chapters 6, 7/8, 9, 10, 11", Q, INTRO)
