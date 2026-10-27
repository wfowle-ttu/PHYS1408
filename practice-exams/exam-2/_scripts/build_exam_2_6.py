"""Practice Exam 2-6: questions, verified answers, figures, exam and key.

Run:  python practice-exams/exam-2/_scripts/build_exam_2_6.py
"""
from math import cos, pi, radians, sin, sqrt

import numpy as np
from matplotlib.patches import Polygon
from examlib import (Circle, Ellipse, Rectangle, arrow, block_on, build, dim, disk_top_view,
                     hanging_pulley, incline)

g = 9.8
Q = []

# 1 ------------------------------------------------------------ flat curve v_max (max trap)
v1 = sqrt(0.55 * g * 40)


def f1(ax):
    a = np.linspace(np.radians(200), np.radians(340), 100)
    for rr in (1.6, 2.1):
        ax.plot(rr * np.cos(a), rr * np.sin(a) + 2.2, "k", lw=1.5)
    ax.plot([0], [2.2], "k.")
    ax.plot([0, 1.85 * np.cos(np.radians(250))], [2.2, 2.2 + 1.85 * np.sin(np.radians(250))], "k--", lw=1)
    ax.text(-0.75, 1.3, r"$40$ m", fontsize=10)
    ax.add_patch(Rectangle((-0.15, 0.25), 0.3, 0.2, fill=False, lw=1.5)); arrow(ax, (0.2, 0.35), (0.9, 0.42))
    ax.text(-1.9, 0.1, r"$\mu_s = 0.55$", fontsize=10)
    ax.set_xlim(-2.3, 2.3); ax.set_ylim(-0.2, 2.4)


Q.append(dict(
    stem=r"A car drives around a flat (unbanked) curve of radius 40 m. The coefficient of static friction between the tires and the road is $\mu_s = 0.55$. What is the maximum speed at which the car can take the curve without sliding?",
    choices=["4.7 m/s", "10.4 m/s", "14 m/s", "15 m/s", "19.8 m/s"], key="c",
    check=("max", v1, [4.7, 10.4, 14, 15, 19.8]),
    value="14.7 m/s → 14", topic="Flat curve, maximum speed", source="Ch 6 notes p. 2/7", card="Curve (flat)",
    solution=r"""
Notecard, flat curve ($\theta = 0$): friction alone supplies the centripetal force.

$$v_{max} = \sqrt{\mu_s gr}$$

**Plug in:**

$$v_{max} = \sqrt{(0.55)(9.8)(40)} = \sqrt{215.6} = 14.7\ \text{m/s}$$

**Answer-choice trap.** 14.7 m/s is a **maximum**. At 15 m/s the car slides, even though 15 is the closest number. The largest choice that works is **c) 14 m/s**.
""",
    distract=["a) 4.7 forgets $g$: $\\sqrt{\\mu_s r}$.", "b) 10.4 has an extra $\\tfrac12$ under the root.",
              "d) 15 is the nearest number, but it's above the maximum.", "e) 19.8 drops $\\mu_s$: $\\sqrt{gr}$."],
    fig=f1, figsize=(3.2, 1.7)))

# 2 ------------------------------------------------------------ one-mass pulley, tension
a2 = 5.0 * g / (5.0 + 0.5 * 6.0)
T2 = 5.0 * (g - a2)


def f2(ax):
    hanging_pulley(ax, center=(0, 2), r=0.7, mass_label=r"$m$")
    ax.text(0.8, 2.7, r"disk, $M = 6.0$ kg", fontsize=10); ax.text(-0.55, 1.1, r"$T = ?$", fontsize=10)
    ax.set_xlim(-1.4, 2.8); ax.set_ylim(0.0, 2.9)


Q.append(dict(
    stem=r"A 5.0 kg mass hangs from a light string wrapped around a pulley that is a uniform disk ($I = \tfrac12 MR^2$, $M = 6.0$ kg) on a frictionless axle. The mass is released. What is the tension in the string while the mass falls?",
    choices=["0 N", "18.4 N", "26.7 N", "30.6 N", "49.0 N"], key="b",
    check=("near", T2, [0, 18.4, 26.7, 30.6, 49.0], 0.05),
    value="18.4 N", topic="Hanging mass on a disk pulley, tension", source="Ch 10 notes p. 4/8; 2015 Exam 2 #9", card="Atwood / mass on pulley (one mass)",
    solution=r"""
Notecard, one mass: $a = \dfrac{mg}{m + I/R^2}$. A disk has $I/R^2 = \tfrac12 M = 3.0$ kg.

**Acceleration:**

$$a = \frac{mg}{m + \tfrac12 M} = \frac{(5.0)(9.8)}{5.0 + 3.0} = \frac{49}{8.0} = 6.125\ \text{m/s}^2$$

**Tension** (notecard, $T = m(g - a)$ for the falling mass):

$$T = m(g - a) = 5.0(9.8 - 6.125) = 5.0(3.675) = 18.4\ \text{N}$$

Check from the pulley side: $T = \dfrac{I}{R^2}a = 3.0(6.125) = 18.4$ N (checks).
""",
    distract=["a) 0 assumes a massless pulley (then nothing pulls back).", "c) 26.7 treats the pulley as a ring ($I/R^2 = M$).",
              "d) 30.6 is $ma$, not $m(g - a)$.", "e) 49.0 is $mg$, true only if the mass doesn't accelerate."],
    fig=f2, figsize=(2.6, 2.2)))

# 3 ------------------------------------------------------------ halfpipe with a push
h3 = 2.0 + 3.0 ** 2 / (2 * g) - 0.12 * 5.0


def f3(ax):
    x = np.linspace(-1, 1, 400)
    y = np.where(np.abs(x) > 0.55, ((np.abs(x) - 0.55) / 0.45) ** 2 * 2.2, 0)
    ax.plot(x * 3, y, "k", lw=1.5); ax.plot([-0.9, 0.9], [0, 0], color="0.4", lw=5, solid_capstyle="butt")
    ax.text(0, -0.5, r"$L = 5.0$ m,  $\mu = 0.12$", ha="center")
    ax.add_patch(Circle((-2.55, 1.15), 0.12, fill=True, color="k")); arrow(ax, (-2.5, 1.0), (-2.2, 0.55))
    ax.text(-4.7, 1.25, r"$2.0$ m, $3.0$ m/s", fontsize=10); ax.text(3.2, 1.0, r"$h_f = ?$")
    ax.set_xlim(-4.8, 4.0); ax.set_ylim(-0.8, 2.4)


Q.append(dict(
    stem=r"A skateboarder is 2.0 m up one wall of a halfpipe, moving **down** the wall at 3.0 m/s. The halfpipe is frictionless except for a 5.0 m long section of the flat bottom with $\mu = 0.12$. How high up the far wall does she rise?",
    choices=["0.46 m", "1.26 m", "1.40 m", "1.86 m", "2.46 m"], key="d",
    check=("near", h3, [0.46, 1.26, 1.40, 1.86, 2.46], 0.005),
    value="1.86 m", topic="Halfpipe with a starting speed", source="Ch 7/8 notes p. 4/18–5/18; 2015 Exam 2 #1", card="Halfpipe",
    solution=r"""
Notecard, one crossing ($n = 1$) with a starting speed:

$$h_f = h_i + \frac{v_i^2}{2g} - n\mu L$$

**Plug in:**

$$
\begin{aligned}
h_f &= 2.0 + \frac{3.0^2}{2(9.8)} - (1)(0.12)(5.0) \\[8pt]
&= 2.0 + 0.459 - 0.60 = 1.86\ \text{m}
\end{aligned}
$$

The starting speed is worth an extra $v_i^2/2g = 0.46$ m of height.
""",
    distract=["a) 0.46 m is only the starting KE as height, $v_i^2/2g$.", "b) 1.26 counts the friction loss twice.",
              "c) 1.40 ignores the starting speed.", "e) 2.46 ignores friction."],
    fig=f3, figsize=(4.2, 2.0)))

# 4 ------------------------------------------------------------ Atwood, acceleration, massless
a4 = (7 - 5) * g / (7 + 5)


def f4(ax):
    ax.plot([-1.3, 1.3], [3.2, 3.2], "k", lw=2); ax.plot([0, 0], [3.2, 2.55], "k", lw=1)
    hanging_pulley(ax, center=(0, 2.0), r=0.55, mass_label=r"$7$", other=r"$5$")
    ax.text(-1.45, 0.05, "kg", fontsize=9)
    ax.set_xlim(-1.5, 1.6); ax.set_ylim(0.0, 3.3)


Q.append(dict(
    stem=r"A 7.0 kg mass and a 5.0 kg mass hang from opposite ends of a light string over a massless, frictionless pulley. What is the magnitude of their acceleration?",
    choices=["1.63 m/s²", "2.80 m/s²", "3.92 m/s²", "9.80 m/s²", "19.6 m/s²"], key="a",
    check=("near", a4, [1.63, 2.80, 3.92, 9.80, 19.6], 0.005),
    value="1.63 m/s²", topic="Atwood's machine, acceleration", source="Ch 7/8 notes p. 2/18", card="Atwood / mass on pulley",
    solution=r"""
Notecard with a massless pulley ($I = 0$):

$$a = \frac{(m_1 - m_2)g}{m_1 + m_2 + I/R^2} = \frac{(m_1 - m_2)g}{m_1 + m_2}$$

**Plug in:**

$$a = \frac{(7.0 - 5.0)(9.8)}{7.0 + 5.0} = \frac{19.6}{12.0} = 1.63\ \text{m/s}^2$$
""",
    distract=["b) 2.80 divides by $m_1$ only.", "c) 3.92 divides by $m_2$ only.",
              "d) 9.80 is free fall.", "e) 19.6 forgets to divide by the masses: $(m_1 - m_2)g$."],
    fig=f4, figsize=(2.4, 2.5)))

# 5 ------------------------------------------------------------ time to stop sliding down a rough incline
s15, c15 = sin(radians(15)), cos(radians(15))
dx5 = 5.0 ** 2 / (2 * g * (0.45 * c15 - s15))
t5 = 2 * dx5 / (5.0 + 0)


def f5(ax):
    up, top, n = incline(ax, 15, 6, origin=(6, 0))
    c = block_on(ax, np.array([6, 0]) + up * 4.6, up, n, size=0.5)
    arrow(ax, c - up * 0.4 + n * 0.45, c - up * 1.4 + n * 0.45); ax.text(*(c - up * 0.6 + n * 0.95), r"$5.0$ m/s", fontsize=10)
    ax.text(4.8, 0.12, r"$15^\circ$", fontsize=10); ax.text(2.6, 0.3, r"$\mu_k = 0.45$", fontsize=10)
    ax.set_xlim(0, 6.3); ax.set_ylim(-0.2, 2.1)


Q.append(dict(
    stem=r"A block is sliding **down** a $15^\circ$ incline ($\mu_k = 0.45$) at 5.0 m/s. Friction slows it down. How long does it take to come to rest?",
    choices=["0.74 s", "1.45 s", "2.67 s", "2.90 s", "it never stops; it speeds up"], key="d",
    check=("near", t5, [0.74, 1.45, 2.67, 2.90, None], 0.005),
    value="2.90 s", topic="Time to stop sliding down a rough incline", source="Ch 7/8 notes p. 10/18; 2015 Exam 2 #4", card="One block on incline (Stop down, Time)",
    solution=r"""
It does stop, because $\mu_k\cos\theta = 0.435$ is bigger than $\sin\theta = 0.259$.

**Step 1: Stopping distance** (notecard, stop down):

$$\Delta x = \frac{v_i^2}{2g(\mu\cos\theta - \sin\theta)} = \frac{5.0^2}{2(9.8)(0.45 \times 0.9659 - 0.2588)} = \frac{25}{19.6(0.1758)} = 7.25\ \text{m}$$

**Step 2: Time** (notecard, with $v_f = 0$):

$$t = \frac{2\,\Delta x}{v_i + v_f} = \frac{2(7.25)}{5.0 + 0} = 2.90\ \text{s}$$

(Or by forces: $a = g(\mu\cos\theta - \sin\theta) = 1.72$ m/s², then $t = v_i/a = 2.90$ s.)
""",
    distract=["a) 0.74 uses the sliding-**up** bracket, $(\\sin\\theta + \\mu\\cos\\theta)$.", "b) 1.45 forgets the 2 in $2\\Delta x$.",
              "c) 2.67 uses friction $\\mu mg$ instead of $\\mu mg\\cos\\theta$.", "e) It does stop, since $\\mu\\cos\\theta > \\sin\\theta$."],
    fig=f5, figsize=(3.8, 1.5)))

# 6 ------------------------------------------------------------ spring launch, speed partway up
v6 = sqrt(2 * (0.5 * 900 * 0.08 ** 2 - 0.15 * g * 0.50) / 0.15)


def f6(ax):
    ys = np.linspace(0, 0.9, 200); ax.plot(0.25 * np.sin(ys * 2 * np.pi * 9), ys, "k", lw=1.2)
    ax.plot([-0.8, 0.8], [0, 0], "k", lw=2); ax.add_patch(Circle((0, 1.05), 0.15, fill=False, lw=1.5))
    ax.add_patch(Circle((0, 1.95), 0.15, fill=False, lw=1, ls="--")); ax.text(0.3, 2.0, r"$v = ?$", fontsize=10)
    dim(ax, (0.95, 1.05), (0.95, 1.95), r"$0.50$ m", offset=(0.55, 0), fontsize=10)
    ax.text(-1.5, 0.45, r"$k = 900$, $x = 0.08$", fontsize=8, rotation=90, va="center")
    ax.set_xlim(-1.7, 2.0); ax.set_ylim(-0.1, 2.3)


Q.append(dict(
    stem=r"A vertical spring ($k = 900$ N/m) is compressed 0.080 m with a 0.15 kg ball resting on it, then released. How fast is the ball moving when it is 0.50 m above the release point?",
    choices=["3.13 m/s", "3.78 m/s", "5.35 m/s", "6.20 m/s", "8.19 m/s"], key="c",
    check=("near", v6, [3.13, 3.78, 5.35, 6.20, 8.19], 0.005),
    value="5.35 m/s", topic="Spring launch, speed partway up", source="Ch 7/8 notes p. 12/18", card="Spring",
    solution=r"""
Notecard spring equation, with all three terms:

$$\tfrac12 kx^2 = \tfrac12 mv^2 + mgh$$

**Solve for $v$:**

$$
\begin{aligned}
\tfrac12 mv^2 &= \tfrac12 kx^2 - mgh \\[8pt]
v &= \sqrt{\frac{2\left(\tfrac12 kx^2 - mgh\right)}{m}}
\end{aligned}
$$

**Plug in:** spring PE $= \tfrac12(900)(0.080)^2 = 2.88$ J; gravity PE gained $= (0.15)(9.8)(0.50) = 0.735$ J.

$$v = \sqrt{\frac{2(2.88 - 0.735)}{0.15}} = \sqrt{\frac{4.29}{0.15}} = \sqrt{28.6} = 5.35\ \text{m/s}$$
""",
    distract=["a) 3.13 is $\\sqrt{2gh}$ (no spring at all).", "b) 3.78 drops the $\\tfrac12$ on the KE.",
              "d) 6.20 ignores the height gained (no $mgh$).", "e) 8.19 drops the $\\tfrac12$ on the spring PE."],
    fig=f6, figsize=(2.4, 2.2)))

# 7 ------------------------------------------------------------ incline + hanging, m1 slides down, massless
s40, c40 = sin(radians(40)), cos(radians(40))
B7 = 12 * s40 - 3 - 0.25 * 12 * c40
v7 = sqrt(1.0 + 2 * g * 0.80 * B7 / 15)


def f7(ax):
    t = radians(40)
    ax.add_patch(Polygon([(0, 0), (3.2, 3.2 * np.tan(t)), (3.2, 0)], closed=True, fill=False, lw=1.5))
    upv = np.array([np.cos(t), np.sin(t)]); nv = np.array([-np.sin(t), np.cos(t)])
    pc = np.array([3.2, 3.2 * np.tan(t)]) + np.array([0.25, 0.25]); ax.add_patch(Circle(pc, 0.25, fill=False, lw=1.5))
    b0 = upv * 2.0; c = block_on(ax, b0, upv, nv, size=0.6, label=r"$m_1$")
    ax.plot([b0[0] + upv[0] * 0.6 + nv[0] * 0.3, pc[0] - 0.05], [b0[1] + upv[1] * 0.6 + nv[1] * 0.3, pc[1] + 0.24], "k", lw=1)
    ax.plot([pc[0] + 0.25] * 2, [pc[1], 1.2], "k", lw=1)
    ax.add_patch(Rectangle((pc[0] + 0.02, 0.75), 0.46, 0.45, fill=False, lw=1.5)); ax.text(pc[0] + 0.25, 0.97, r"$m_2$", ha="center", va="center", fontsize=9)
    arrow(ax, c - upv * 0.3 + nv * 0.5, c - upv * 1.1 + nv * 0.5)
    ax.text(0.7, 0.08, r"$40^\circ$", fontsize=10); ax.text(1.8, 0.3, r"$\mu_k = 0.25$", fontsize=10)
    ax.set_xlim(-0.2, 4.3); ax.set_ylim(-0.2, 3.3)


Q.append(dict(
    stem=r"A 12 kg block on a $40^\circ$ incline ($\mu_k = 0.25$) is tied by a light string over a massless pulley at the top to a 3.0 kg hanging mass. The block is sliding **down** the incline at 1.0 m/s (so the hanging mass is rising). How fast is the block moving after it has slid 0.80 m down the incline?",
    choices=["1.59 m/s", "1.88 m/s", "2.04 m/s", "2.43 m/s", "it stops before it slides the whole 0.80 m"], key="b",
    check=("near", v7, [1.59, 1.88, 2.04, 2.43, None], 0.005),
    value="1.88 m/s", topic="Incline + hanging mass, block slides down", source="Ch 7/8 notes p. 17/18–18/18", card="Incline + hanging mass + pulley",
    solution=r"""
Notecard with $m_1$ sliding **down** and a massless pulley ($I = 0$):

$$v_f = \sqrt{v_i^2 + \frac{2g\,\Delta x\,B}{m_1 + m_2}}, \qquad B = m_1\sin\theta - m_2 - \mu m_1\cos\theta$$

**Net pull** ($\sin 40^\circ = 0.6428$, $\cos 40^\circ = 0.7660$):

$$B = 12(0.6428) - 3.0 - 0.25(12)(0.7660) = 7.714 - 3.0 - 2.298 = 2.416\ \text{kg}$$

**Plug in:**

$$
\begin{aligned}
v_f &= \sqrt{1.0^2 + \frac{2(9.8)(0.80)(2.416)}{12 + 3.0}} \\[8pt]
&= \sqrt{1.0 + \frac{37.88}{15}} = \sqrt{1.0 + 2.526} = \sqrt{3.526} = 1.88\ \text{m/s}
\end{aligned}
$$

$B > 0$, so the block speeds up (e is wrong).
""",
    distract=["a) 1.59 forgets $v_i^2$.", "c) 2.04 divides by $m_1$ only.", "d) 2.43 ignores friction.",
              "e) comes from using the wrong $B$ (the $m_2$-falls version, which is negative)."],
    fig=f7, figsize=(3.0, 2.2)))

# 8 ------------------------------------------------------------ projectile from a ledge
s55 = sin(radians(55))
H8 = 12 + (18 * s55) ** 2 / (2 * g)


def f8(ax):
    ax.plot([-0.8, 0, 0, 7], [2, 2, 0, 0], "k", lw=1.5)
    t = np.linspace(0, 2.6, 100); ax.plot(t * 1.8, 2 + t * 1.8 * np.tan(np.radians(55)) * 0.45 - 0.5 * (t * 1.8) ** 2 * 0.28, "k--", lw=1)
    arrow(ax, (0, 2), (0.7, 3.0)); ax.text(0.6, 3.15, r"$v_0 = 18$ m/s", fontsize=10); ax.text(0.45, 2.15, r"$55^\circ$", fontsize=10)
    dim(ax, (-0.4, 0), (-0.4, 2), r"$12$ m", offset=(-0.45, 0), fontsize=10)
    ax.set_xlim(-1.3, 6); ax.set_ylim(-0.2, 3.7)


Q.append(dict(
    stem=r"A ball is thrown from the edge of a 12 m high ledge at 18 m/s, $55^\circ$ above the horizontal. How high above the ground below is the ball at the highest point of its path?",
    choices=["5.4 m", "11.1 m", "12.0 m", "17.4 m", "23.1 m"], key="e",
    check=("near", H8, [5.4, 11.1, 12.0, 17.4, 23.1], 0.05),
    value="23.1 m", topic="Projectile from a ledge (review)", source="2015 Exam 2 #2", card="Projectile",
    solution=r"""
Notecard:

$$H = h_0 + \frac{(v_0\sin\theta)^2}{2g}$$

**Plug in** ($\sin 55^\circ = 0.8192$, so $v_0\sin\theta = 14.75$ m/s):

$$H = 12 + \frac{(14.75)^2}{2(9.8)} = 12 + \frac{217.4}{19.6} = 12 + 11.1 = 23.1\ \text{m}$$
""",
    distract=["a) 5.4 uses $\\cos\\theta$ and forgets the ledge.", "b) 11.1 forgets to add the ledge.",
              "c) 12.0 is just the ledge.", "d) 17.4 uses $\\cos\\theta$ instead of $\\sin\\theta$."],
    fig=f8, figsize=(3.6, 1.8)))

# 9 ------------------------------------------------------------ bullet into block, stick (no swing)
v9 = 0.015 * 300 / (2.0 + 0.015)


def f9(ax):
    ax.plot([-0.3, 4.5], [0, 0], "k", lw=1.5)
    ax.add_patch(Rectangle((2.2, 0), 1.2, 0.8, fill=False, lw=1.5)); ax.text(2.8, 0.4, "2.0 kg", ha="center", va="center", fontsize=9)
    ax.add_patch(Ellipse((0.2, 0.4), 0.35, 0.14, fill=True, color="k")); arrow(ax, (0.45, 0.4), (1.5, 0.4))
    ax.text(0.0, 0.7, r"$0.015$ kg, $300$ m/s", fontsize=9); ax.text(2.4, -0.35, r"$\mu = 0$", fontsize=10)
    ax.set_xlim(-0.4, 4.6); ax.set_ylim(-0.5, 1.1)


Q.append(dict(
    stem=r"A 0.015 kg bullet moving at 300 m/s embeds itself in a 2.0 kg block resting on a frictionless table. How fast does the block (with the bullet) move just after the collision?",
    choices=["2.23 m/s", "2.25 m/s", "4.5 m/s", "25.9 m/s", "300 m/s"], key="a",
    check=("near", v9, [2.23, 2.25, 4.5, 25.9, 300], 0.005),
    value="2.23 m/s", topic="Completely inelastic: bullet into a block", source="Ch 9 notes p. 1/5", card="Stick (inelastic)",
    solution=r"""
They stick, so momentum only (notecard, block at rest):

$$v_f = \frac{m_1v_1 + m_2v_2}{m_1 + m_2} = \frac{m v}{m + M}$$

**Plug in:**

$$v_f = \frac{(0.015)(300)}{0.015 + 2.0} = \frac{4.5}{2.015} = 2.23\ \text{m/s}$$
""",
    distract=["b) 2.25 leaves the bullet's mass out of the denominator (close; keep 3 digits).", "c) 4.5 is the momentum (kg·m/s), not a speed.",
              "d) 25.9 uses energy conservation through the collision (never do that).", "e) 300 is the bullet's speed before."],
    fig=f9, figsize=(3.4, 1.0)))

# 10 ----------------------------------------------------------- elastic, light ball bounces back
v10 = ((0.5 - 1.5) * 6.0) / 2.0


def f10(ax):
    ax.add_patch(Circle((0, 0), 0.28, fill=False, lw=1.5)); ax.add_patch(Circle((2.8, 0), 0.45, fill=False, lw=1.5))
    arrow(ax, (0.35, 0), (1.3, 0)); ax.text(0, -0.8, r"$0.5$ kg, $+6$ m/s", ha="center"); ax.text(2.8, -0.8, r"$1.5$ kg, at rest", ha="center")
    ax.set_xlim(-0.8, 3.8); ax.set_ylim(-1.1, 0.6)


Q.append(dict(
    stem=r"A 0.50 kg ball moving right at 6.0 m/s collides **elastically** head-on with a 1.5 kg ball at rest. What is the velocity of the 0.50 kg ball after the collision? Positive to the right / negative to the left.",
    choices=["+6.0 m/s", "+3.0 m/s", "+1.5 m/s", "0 m/s", "−3.0 m/s"], key="e",
    check=("near", v10, [6.0, 3.0, 1.5, 0, -3.0], 0.05),
    value="−3.0 m/s", topic="1-D elastic collision, light ball bounces back", source="Ch 9 notes p. 2/5–3/5", card="Elastic",
    solution=r"""
Notecard, right $= +$: $m_1 = 0.50$, $v_{1i} = +6.0$; $m_2 = 1.5$, $v_{2i} = 0$.

$$v_{1f} = \frac{(m_1 - m_2)v_{1i} + 2m_2v_{2i}}{m_1 + m_2} = \frac{(0.50 - 1.5)(6.0) + 0}{2.0} = \frac{-6.0}{2.0} = -3.0\ \text{m/s}$$

The light ball bounces back to the left. (The 1.5 kg ball leaves at $v_{2f} = 6.0 - 3.0 - 0 = +3.0$ m/s.)
""",
    distract=["a) +6.0 is no change.", "b) +3.0 is the 1.5 kg ball's velocity.", "c) +1.5 is the stick-together answer.",
              "d) 0 is the equal-mass (cue ball) result, which needs equal masses."],
    fig=f10, figsize=(3.6, 1.1)))

# 11 ----------------------------------------------------------- rotational kinematics, angle to stop
th11 = 12.0 ** 2 / (2 * 1.5)


def f11(ax):
    ax.add_patch(Circle((0, 0), 1.0, fill=False, lw=1.5))
    for a in np.radians([0, 60, 120, 180, 240, 300]):
        ax.plot([0, np.cos(a)], [0, np.sin(a)], "k", lw=0.8)
    ax.text(-1.3, -1.4, r"$12$ rad/s, slows at $1.5$ rad/s$^2$", fontsize=9)
    ax.set_xlim(-1.4, 1.6); ax.set_ylim(-1.6, 1.2)


Q.append(dict(
    stem=r"A wheel spinning at 12 rad/s slows down with a constant angular deceleration of 1.5 rad/s². Through what angle does it turn before it stops?",
    choices=["7.6 rad", "8.0 rad", "24 rad", "48 rad", "96 rad"], key="d",
    check=("near", th11, [7.6, 8.0, 24, 48, 96], 0.05),
    value="48 rad", topic="Rotational kinematics, angle to stop", source="Ch 10 notes p. 1/8", card="Rot. kinematics",
    solution=r"""
Time isn't given or asked for, so use the equation without it:

$$\omega_f^2 = \omega_i^2 + 2\alpha\,\Delta\theta$$

**Solve for $\Delta\theta$** ($\omega_f = 0$, and $\alpha = -1.5$ rad/s² because it slows):

$$
\begin{aligned}
0 &= \omega_i^2 + 2\alpha\,\Delta\theta \\[8pt]
\Delta\theta &= \frac{-\omega_i^2}{2\alpha}
\end{aligned}
$$

**Plug in:**

$$\Delta\theta = \frac{-(12)^2}{2(-1.5)} = \frac{144}{3.0} = 48\ \text{rad}$$
""",
    distract=["a) 7.6 is the answer in revolutions, $48/2\\pi$.", "b) 8.0 is the time to stop, $\\omega_i/\\alpha$, in seconds.",
              "c) 24 has an extra factor of 2 in the denominator.", "e) 96 forgets the 2: $\\omega_i^2/\\alpha$."],
    fig=f11, figsize=(2.6, 2.4)))

# 12 ----------------------------------------------------------- disk about a rim point
I12 = 1.5 * 4.0 * 0.30 ** 2


def f12(ax):
    ax.add_patch(Circle((0, 0), 1.0, fill=False, lw=1.5)); ax.plot([0], [0], "k+", ms=10); ax.plot([1.0], [0], "ko")
    ax.text(1.1, 0.15, "axis", fontsize=10); ax.text(-0.3, 0.15, "center", fontsize=9)
    dim(ax, (0, -0.25), (1.0, -0.25), r"$R$", offset=(0, -0.2))
    ax.set_xlim(-1.2, 1.8); ax.set_ylim(-1.2, 1.2)


Q.append(dict(
    stem=r"A uniform disk ($I_{cm} = \tfrac12 MR^2$, $M = 4.0$ kg, $R = 0.30$ m) rotates about an axis perpendicular to the disk through a point on its **edge**. What is its moment of inertia about this axis?",
    choices=["0.12 kg·m²", "0.18 kg·m²", "0.27 kg·m²", "0.36 kg·m²", "0.54 kg·m²"], key="e",
    check=("near", I12, [0.12, 0.18, 0.27, 0.36, 0.54], 0.005),
    value="0.54 kg·m²", topic="Parallel axis theorem, disk about its rim", source="Ch 10 notes p. 2/8", card="Parallel axis (disk about rim)",
    solution=r"""
Notecard: disk about a point on its rim, $I = \tfrac32 MR^2$. (That's $I_{cm} + md^2$ with $d = R$: $\tfrac12 MR^2 + MR^2$.)

$$I = \tfrac32 MR^2$$

**Plug in:**

$$I = \tfrac32(4.0)(0.30)^2 = 1.5(4.0)(0.090) = 0.54\ \text{kg·m}^2$$
""",
    distract=["a) 0.12 uses the rod-end fraction, $\\tfrac13 MR^2$.", "b) 0.18 is $I_{cm}$ alone.",
              "c) 0.27 uses $d = R/2$.", "d) 0.36 is $MR^2$ alone (forgot $I_{cm}$)."],
    fig=f12, figsize=(2.6, 2.0)))

# 13 ----------------------------------------------------------- rolling ring, acceleration
a13 = 0.5 * g * sin(radians(28))


def f13(ax):
    up, top, n = incline(ax, 28, 5, origin=(5, 0))
    c1 = np.array([5, 0]) + up * 2.6 + n * 0.4
    ax.add_patch(Circle(c1, 0.4, fill=False, lw=2.5)); ax.add_patch(Circle(c1, 0.32, fill=False, lw=0.8))
    arrow(ax, c1 - up * 0.5 + n * 0.6, c1 - up * 1.5 + n * 0.6); ax.text(*(c1 - up * 1.7 + n * 0.9), r"$a = ?$")
    ax.text(3.9, 0.12, r"$28^\circ$", fontsize=10)
    ax.set_xlim(0.4, 5.3); ax.set_ylim(-0.2, 2.8)


Q.append(dict(
    stem=r"A thin hoop ($I = MR^2$) rolls without slipping down a $28^\circ$ incline. What is the acceleration of its center?",
    choices=["2.30 m/s²", "3.07 m/s²", "3.29 m/s²", "4.33 m/s²", "4.60 m/s²"], key="a",
    check=("near", a13, [2.30, 3.07, 3.29, 4.33, 4.60], 0.005),
    value="2.30 m/s²", topic="Rolling acceleration, hoop", source="Ch 10 notes p. 3/8", card="Rolling (ring row)",
    solution=r"""
Notecard, ring (hoop) row: $a = \tfrac12 g\sin\theta$.

**Plug in:**

$$a = \tfrac12(9.8)\sin 28^\circ = \tfrac12(9.8)(0.4695) = 2.30\ \text{m/s}^2$$
""",
    distract=["b) 3.07 is a disk, $\\tfrac23 g\\sin\\theta$.", "c) 3.29 is a sphere, $\\tfrac57 g\\sin\\theta$.",
              "d) 4.33 uses $\\cos\\theta$.", "e) 4.60 is sliding, $g\\sin\\theta$."],
    fig=f13, figsize=(3.2, 1.9)))

# 14 ----------------------------------------------------------- counter-rotating disk on disk
I14a, I14b = 0.5 * 40 * 0.5 ** 2, 0.5 * 20 * 0.5 ** 2
w14 = (I14a * 6.0 + I14b * (-2.0)) / (I14a + I14b)


def f14(ax):
    ax.plot([0, 0], [-0.3, 2.6], "k", lw=1)
    ax.add_patch(Ellipse((0, 0.4), 3.0, 0.65, fill=False, lw=1.5)); ax.add_patch(Ellipse((0, 1.9), 3.0, 0.65, fill=False, lw=1.5))
    arrow(ax, (0.9, 0.05), (1.4, 0.2), connectionstyle="arc3,rad=0.2"); ax.text(1.6, 0.35, r"$+6.0$")
    arrow(ax, (-0.9, 1.6), (-1.4, 1.75), connectionstyle="arc3,rad=-0.2"); ax.text(-2.2, 2.0, r"$-2.0$")
    arrow(ax, (0.6, 1.5), (0.6, 0.9), lw=1); ax.text(1.6, 1.9, "20 kg", fontsize=9); ax.text(1.6, -0.15, "40 kg", fontsize=9)
    ax.set_xlim(-2.4, 2.6); ax.set_ylim(-0.4, 2.5)


Q.append(dict(
    stem=r"A disk ($I = \tfrac12 MR^2$, $M = 40$ kg, $R = 0.50$ m) spins at +6.0 rad/s. A second disk ($I = \tfrac12 MR^2$, $M = 20$ kg, $R = 0.50$ m) spinning the **opposite** way at −2.0 rad/s is dropped onto it, and the two end up turning together. What is their final angular velocity?",
    choices=["+2.00 rad/s", "+3.33 rad/s", "+4.00 rad/s", "+4.67 rad/s", "+6.00 rad/s"], key="b",
    check=("near", w14, [2.00, 3.33, 4.00, 4.67, 6.00], 0.005),
    value="+3.33 rad/s", topic="Counter-rotating disk dropped on a disk", source="Ch 11 notes p. 3/8; 2015 Exam 2 #11", card="Angular momentum",
    solution=r"""
$L_i = L_f$, with the dropped disk's $\omega_2$ **negative**:

$$\omega_f = \frac{I_1\omega_1 + I_2\omega_2}{I_1 + I_2}$$

**Moments of inertia first:**

$$I_1 = \tfrac12(40)(0.50)^2 = 5.0\ \text{kg·m}^2 \qquad\qquad I_2 = \tfrac12(20)(0.50)^2 = 2.5\ \text{kg·m}^2$$

**Plug in:**

$$\omega_f = \frac{(5.0)(6.0) + (2.5)(-2.0)}{5.0 + 2.5} = \frac{30 - 5.0}{7.5} = +3.33\ \text{rad/s}$$
""",
    distract=["a) 2.00 treats the top disk as a ring ($mr^2$).", "c) 4.00 ignores the top disk's spin.",
              "d) 4.67 forgets the minus sign.", "e) 6.00 is no change."],
    fig=f14, figsize=(3.4, 1.8)))

# 15 ----------------------------------------------------------- walk from rim to halfway in
I15 = 0.5 * 300 * 3.0 ** 2
w15 = (I15 + 75 * 3.0 ** 2) * 1.0 / (I15 + 75 * 1.5 ** 2)


def f15(ax):
    for cx, (px, py), lab in [(0, (0, -0.9), r"$\omega_i = 1.0$"), (2.7, (2.7, -0.45), r"$\omega_f = ?$")]:
        disk_top_view(ax, (cx, 0), 0.9); ax.add_patch(Circle((px, py), 0.09, fill=True, color="k")); ax.text(cx - 0.5, 1.05, lab, fontsize=10)
    arrow(ax, (1.0, 0), (1.6, 0)); ax.text(2.85, -0.35, r"$R/2$", fontsize=9)
    ax.set_xlim(-1.1, 3.8); ax.set_ylim(-1.2, 1.4)


Q.append(dict(
    stem=r"A 75 kg person stands at the rim of a merry-go-round (a disk, $I = \tfrac12 MR^2$, $M = 300$ kg, $R = 3.0$ m) that rotates at 1.0 rad/s. The person walks **halfway** in, to 1.5 m from the center. What is the new angular velocity? (Treat the person as a point mass.)",
    choices=["0.75 rad/s", "1.00 rad/s", "1.33 rad/s", "1.50 rad/s", "2.00 rad/s"], key="c",
    check=("near", w15, [0.75, 1.00, 1.33, 1.50, 2.00], 0.005),
    value="1.33 rad/s", topic="Person walks partway in", source="Ch 11 notes p. 7/8", card="Angular momentum (walk in/out)",
    solution=r"""
Notecard, walk in/out: $\omega_f = \dfrac{I_i}{I_f}\omega_i$. The person's $I = mr^2$ changes from $r = 3.0$ m to $r = 1.5$ m.

$$\omega_f = \frac{\tfrac12 MR^2 + mR^2}{\tfrac12 MR^2 + m\left(\tfrac{R}{2}\right)^2}\,\omega_i$$

**Moments of inertia:** disk $= \tfrac12(300)(3.0)^2 = 1350$; person at the rim $= 75(3.0)^2 = 675$; person halfway $= 75(1.5)^2 = 168.75$ (all kg·m²).

**Plug in:**

$$\omega_f = \frac{1350 + 675}{1350 + 168.75}(1.0) = \frac{2025}{1518.75} = 1.33\ \text{rad/s}$$

The rim$\to$center shortcut $\frac{M + 2m}{M}$ only works for walking **all the way** to the center.
""",
    distract=["a) 0.75 flips the ratio (walking out).", "b) 1.00 is no change.",
              "d) 1.50 uses the rim$\\to$center shortcut, as if they walked all the way in.", "e) 2.00 assumes halving the distance doubles $\\omega$."],
    fig=f15, figsize=(3.6, 1.7)))

INTRO = r"""
Practice Exam 2-6 rounds out the set: a flat-curve **maximum** (Question 1 is a round-**down** trap), string tension, a halfpipe with a starting speed, time to stop sliding **down**, spring speed partway up, a bullet into a block on a table (no swing), a light ball bouncing back, a disk spun about its rim, and walking **partway** in. The last column says which 3×5 notecard entry solves each question.
"""

if __name__ == "__main__":
    build(6, "Chapters 6, 7/8, 9, 10, 11", Q, INTRO)
