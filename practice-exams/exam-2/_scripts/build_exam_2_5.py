"""Practice Exam 2-5: questions, verified answers, figures, exam and key.

Run:  python practice-exams/exam-2/_scripts/build_exam_2_5.py
"""
from math import cos, radians, sin, sqrt, tan

import numpy as np
from matplotlib.patches import Polygon
from examlib import (Circle, Ellipse, Rectangle, arrow, block_on, build, dim, disk_top_view,
                     hanging_pulley, incline)

g = 9.8
Q = []

# 1 ------------------------------------------------------------ banked v_min (min trap)
t25 = tan(radians(25))
v1 = sqrt(g * 103 * (t25 - 0.12) / (1 + 0.12 * t25))


def f1(ax):
    up, top, n = incline(ax, 25, 4, origin=(4, 0))
    c = block_on(ax, np.array([4, 0]) + up * 2.0, up, n, size=0.55)
    arrow(ax, c, c + n * 1.0); ax.text(*(c + n * 1.15), r"$N$")
    arrow(ax, c, c + np.array([0, -0.9])); ax.text(c[0] + 0.1, c[1] - 0.95, r"$mg$")
    arrow(ax, c, c + up * 0.9); ax.text(*(c + up * 1.15 + np.array([0, 0.1])), r"$f_s$")
    ax.text(3.0, 0.08, r"$\theta$"); ax.text(3.0, 1.9, r"center of curve $\rightarrow$", fontsize=10)
    ax.set_xlim(-0.2, 6.3); ax.set_ylim(-0.3, 2.4)


Q.append(dict(
    stem=r"A highway curve of radius 103 m is banked at $\theta = 25^\circ$. The coefficient of static friction between the tires and the road is $\mu_s = 0.12$. What is the minimum speed at which a car can take the curve without sliding down the bank?",
    choices=["11 m/s", "18 m/s", "19 m/s", "22 m/s", "25 m/s"], key="c",
    check=("min", v1, [11, 18, 19, 22, 25]),
    value="18.2 m/s → 19", topic="Banked curve, minimum speed", source="Ch 6 notes p. 7/7; handout p. 2/3", card="Curve",
    solution=r"""
At $v_{min}$ the car tends to slide **down** the bank, so friction points **up** the bank. The notecard formula with the $-$ signs:

$$v_{min} = \sqrt{gr\,\frac{\tan\theta - \mu_s}{1 + \mu_s\tan\theta}}$$

**Plug in** ($\tan 25^\circ = 0.4663$):

$$
\begin{aligned}
v_{min} &= \sqrt{(9.8)(103)\,\frac{0.4663 - 0.12}{1 + (0.12)(0.4663)}} \\[8pt]
&= \sqrt{1009.4 \times \frac{0.3463}{1.0560}} = \sqrt{331.0} = 18.2\ \text{m/s}
\end{aligned}
$$

**Answer-choice trap.** 18.2 m/s is a **minimum**. At 18 m/s the car slides down the bank, even though 18 is the closest number. The smallest choice that works is **c) 19 m/s**.
""",
    distract=["a) 11 is the flat-curve formula, $\\sqrt{\\mu_s gr}$.", "b) 18 is the nearest number, but it's below the minimum.",
              "d) 22 is the frictionless bank, $\\sqrt{gr\\tan\\theta}$.", "e) 25 is $v_{max}$."],
    fig=f1, figsize=(4.0, 2.0)))

# 2 ------------------------------------------------------------ Atwood with disk pulley
v2 = sqrt(2 * g * 2.0 * (5 - 3) / (5 + 3 + 1))


def f2(ax):
    ax.plot([-1.3, 1.3], [3.2, 3.2], "k", lw=2); ax.plot([0, 0], [3.2, 2.55], "k", lw=1)
    hanging_pulley(ax, center=(0, 2.0), r=0.55, mass_label=r"$m_1$", other=r"$m_2$")
    ax.text(0.7, 2.5, "disk", fontsize=9)
    ax.set_xlim(-1.5, 1.6); ax.set_ylim(0.0, 3.3)


Q.append(dict(
    stem=r"Masses $m_1 = 5.0$ kg and $m_2 = 3.0$ kg hang from opposite ends of a light string over a pulley that is a uniform disk ($I = \tfrac12 MR^2$, $M = 2.0$ kg). They are released from rest. How fast is $m_1$ moving after it has fallen 2.0 m?",
    choices=["2.80 m/s", "2.95 m/s", "3.13 m/s", "3.61 m/s", "6.26 m/s"], key="b",
    check=("near", v2, [2.80, 2.95, 3.13, 3.61, 6.26], 0.005),
    value="2.95 m/s", topic="Atwood's machine, disk pulley", source="Ch 7/8 notes p. 2/18 + Ch 10 notes p. 4/8", card="Atwood / mass on pulley",
    solution=r"""
Notecard (two masses):

$$v_f = \sqrt{v_i^2 + \frac{2gh(m_1 - m_2)}{m_1 + m_2 + I/R^2}}$$

A disk has $I/R^2 = \tfrac12 M = 1.0$ kg ($R$ cancels).

**Plug in** ($v_i = 0$, $h = 2.0$ m):

$$
\begin{aligned}
v_f &= \sqrt{\frac{2(9.8)(2.0)(5.0 - 3.0)}{5.0 + 3.0 + 1.0}} \\[8pt]
&= \sqrt{\frac{78.4}{9.0}} = \sqrt{8.71} = 2.95\ \text{m/s}
\end{aligned}
$$
""",
    distract=["a) 2.80 treats the pulley as a ring ($I/R^2 = M$).", "c) 3.13 ignores the pulley's mass.",
              "d) 3.61 leaves $m_2$ out of the denominator.", "e) 6.26 is free fall, $\\sqrt{2gh}$."],
    fig=f2, figsize=(2.4, 2.5)))

# 3 ------------------------------------------------------------ roller coaster with initial speed
v3 = sqrt(8.0 ** 2 + 2 * g * (30 - 12))


def f3(ax):
    x = np.linspace(0, 8, 300)
    y = 3.0 - 1.8 * (1 - np.exp(-((x - 0.3) / 2.0) ** 2)) + 0.0 * x
    y = 3.0 * np.exp(-(x / 3.2) ** 2) + 1.2 * (1 - np.exp(-(x / 3.2) ** 2))
    ax.plot(x, y, "k", lw=1.5); ax.plot([0, 8], [0, 0], "k:", lw=1)
    ax.add_patch(Circle((0.2, 3.2), 0.18, fill=True, color="k")); arrow(ax, (0.5, 3.35), (1.3, 3.2)); ax.text(0.6, 3.6, r"$8.0$ m/s", fontsize=10)
    dim(ax, (-0.4, 0), (-0.4, 3.0), r"$30$ m", offset=(-0.5, 0), fontsize=10)
    dim(ax, (7.7, 0), (7.7, 1.2), r"$12$ m", offset=(0.55, 0), fontsize=10); ax.text(6.0, 1.6, r"$v = ?$")
    ax.set_xlim(-1.4, 8.8); ax.set_ylim(-0.3, 4.0)


Q.append(dict(
    stem=r"A roller coaster car passes over the top of a 30 m hill at 8.0 m/s. The track is frictionless. How fast is it moving when it reaches a section of track 12 m above the ground?",
    choices=["15.5 m/s", "18.8 m/s", "20.4 m/s", "25.5 m/s", "26.8 m/s"], key="c",
    check=("near", v3, [15.5, 18.8, 20.4, 25.5, 26.8], 0.05),
    value="20.4 m/s", topic="Roller coaster with a starting speed", source="Ch 7/8 notes p. 3/18", card="Fall / coaster",
    solution=r"""
Notecard (no friction):

$$v_f = \sqrt{v_i^2 + 2g(h_i - h_f)}$$

**Plug in:**

$$v_f = \sqrt{8.0^2 + 2(9.8)(30 - 12)} = \sqrt{64 + 352.8} = \sqrt{416.8} = 20.4\ \text{m/s}$$

Add the KE you start with **inside** the root, not to the final speed.
""",
    distract=["a) 15.5 forgets the 2 in $2g$.", "b) 18.8 ignores the starting speed.",
              "d) 25.5 uses the full 30 m drop.", "e) 26.8 adds 8.0 m/s to the speed from rest ($18.8 + 8.0$)."],
    fig=f3, figsize=(3.8, 1.8)))

# 4 ------------------------------------------------------------ sliding up rough incline, speed after distance
s20, c20 = sin(radians(20)), cos(radians(20))
vf2_4 = 36 - 2 * g * 2.0 * (s20 + 0.15 * c20)
v4 = sqrt(vf2_4)


def f4(ax):
    up, top, n = incline(ax, 20, 5.5, origin=(5.5, 0))
    c = block_on(ax, np.array([5.5, 0]) + up * 0.8, up, n, size=0.5)
    arrow(ax, c + up * 0.4 + n * 0.45, c + up * 1.4 + n * 0.45); ax.text(*(c + up * 0.3 + n * 0.95), r"$v_i = 6.0$ m/s", fontsize=10)
    ax.text(4.4, 0.12, r"$20^\circ$", fontsize=10); ax.text(1.3, 0.35, r"$\mu_k = 0.15$", fontsize=10)
    ax.set_xlim(0, 5.8); ax.set_ylim(-0.2, 2.3)


Q.append(dict(
    stem=r"A block slides **up** a $20^\circ$ incline ($\mu_k = 0.15$) with an initial speed of 6.0 m/s. How fast is it moving after it has slid 2.0 m along the incline?",
    choices=["4.13 m/s", "4.75 m/s", "5.15 m/s", "7.41 m/s", "it stops before it slides the whole 2.0 m"], key="a",
    check=("near", v4, [4.13, 4.75, 5.15, 7.41, None], 0.005),
    value="4.13 m/s", topic="Sliding up a rough incline", source="Ch 7/8 notes p. 7/18–8/18", card="One block on incline (Up)",
    solution=r"""
Notecard, sliding **up**:

$$v_f = \sqrt{v_i^2 - 2g\,\Delta x(\sin\theta + \mu\cos\theta)}$$

**Plug in** ($\sin 20^\circ = 0.3420$, $\cos 20^\circ = 0.9397$):

$$
\begin{aligned}
v_f &= \sqrt{6.0^2 - 2(9.8)(2.0)(0.3420 + 0.15 \times 0.9397)} \\[8pt]
&= \sqrt{36 - 39.2(0.4830)} = \sqrt{36 - 18.93} = \sqrt{17.07} = 4.13\ \text{m/s}
\end{aligned}
$$

The number under the root is positive, so it does make it 2.0 m (e is wrong).
""",
    distract=["b) 4.75 ignores friction.", "c) 5.15 forgets the 2 in $2g$.",
              "d) 7.41 adds instead of subtracts (that's the sliding-down sign).", "e) It doesn't stop: $v_f^2 = 17.07 > 0$."],
    fig=f4, figsize=(3.8, 1.6)))

# 5 ------------------------------------------------------------ spring: compression needed for a launch height
x5 = sqrt(2 * 0.25 * g * 3.0 / 1200)


def f5(ax):
    ys = np.linspace(0, 0.9, 200); ax.plot(0.25 * np.sin(ys * 2 * np.pi * 9), ys, "k", lw=1.2)
    ax.plot([-0.8, 0.8], [0, 0], "k", lw=2); ax.add_patch(Circle((0, 1.05), 0.15, fill=False, lw=1.5))
    ax.plot([0.5, 1.1], [1.05, 1.05], "k:", lw=1); ax.plot([0.5, 1.1], [2.3, 2.3], "k:", lw=1)
    dim(ax, (0.95, 1.05), (0.95, 2.3), r"$3.0$ m", offset=(0.5, 0), fontsize=10)
    ax.text(-1.3, 0.45, r"$x = ?$", fontsize=10)
    ax.set_xlim(-1.6, 1.9); ax.set_ylim(-0.1, 2.5)


Q.append(dict(
    stem=r"A vertical spring ($k = 1200$ N/m) is used to launch a 0.25 kg ball straight up. How far must the spring be compressed for the ball to rise 3.0 m above the release point?",
    choices=["0.006 m", "0.012 m", "0.055 m", "0.078 m", "0.11 m"], key="e",
    check=("near", x5, [0.006, 0.012, 0.055, 0.078, 0.11], 0.003),
    value="0.11 m", topic="Vertical spring launch, find the compression", source="Ch 7/8 notes p. 12/18; 2015 Exam 2 #5", card="Spring",
    solution=r"""
Notecard launch line, $h = \dfrac{kx^2}{2mg}$. **Solve for $x$:**

$$
\begin{aligned}
kx^2 &= 2mgh \\[8pt]
x &= \sqrt{\frac{2mgh}{k}}
\end{aligned}
$$

**Plug in:**

$$x = \sqrt{\frac{2(0.25)(9.8)(3.0)}{1200}} = \sqrt{\frac{14.7}{1200}} = \sqrt{0.01225} = 0.11\ \text{m}$$
""",
    distract=["a) 0.006 is $mgh/k$ (no 2, no root).", "b) 0.012 forgets the square root.",
              "c) 0.055 is $\\sqrt{mgh/2k}$ (the 2 upside down).", "d) 0.078 drops the 2: $\\sqrt{mgh/k}$."],
    fig=f5, figsize=(2.2, 2.2)))

# 6 ------------------------------------------------------------ normal force at the bottom of a loop
N6 = 60 * g + 60 * (2 * g * 20) / 8


def f6(ax):
    x = np.linspace(0, 2.2, 100); ax.plot(x - 2.2, 3.0 * (1 - x / 2.2) ** 2, "k", lw=1.5)
    ax.plot([0, 2.6], [0, 0], "k", lw=1.5); ax.add_patch(Circle((1.3, 1.0), 1.0, fill=False, lw=1.5))
    ax.add_patch(Rectangle((-2.2, 2.95), 0.3, 0.22, fill=False, lw=1.5))
    dim(ax, (-2.5, 0), (-2.5, 3.0), r"$20$ m", offset=(-0.45, 0), fontsize=10)
    ax.plot([1.3, 2.0], [1.0, 1.7], "k", lw=1); ax.text(2.05, 1.75, r"$R = 8$ m", fontsize=9)
    arrow(ax, (1.3, 0.05), (1.3, 0.75)); ax.text(0.35, 0.3, r"$N = ?$", fontsize=10)
    ax.set_xlim(-3.2, 2.8); ax.set_ylim(-0.2, 3.4)


Q.append(dict(
    stem=r"A 60 kg rider in a roller coaster car starts from rest 20 m above the bottom of a vertical loop of radius $R = 8.0$ m. The track is frictionless. What normal force does the seat exert on the rider at the **bottom** of the loop?",
    choices=["588 N", "2350 N", "2940 N", "3530 N", "7060 N"], key="d",
    check=("near", N6, [588, 2350, 2940, 3530, 7060], 5),
    value="3530 N", topic="Loop, normal force at the bottom", source="Ch 7/8 notes p. 13/18", card="Loop",
    solution=r"""
**Speed at the bottom** (energy from the start, drop $h = 20$ m):

$$v_b^2 = 2gh = 2(9.8)(20) = 392\ \text{m}^2/\text{s}^2$$

**Forces at the bottom.** $N$ points up, toward the center, and $mg$ points down. Notecard:

$$N_{bot} = \frac{mv_b^2}{R} + mg$$

**Plug in:**

$$N_{bot} = \frac{(60)(392)}{8.0} + (60)(9.8) = 2940 + 588 = 3528 \approx 3530\ \text{N}$$

That's 6 times the rider's weight.
""",
    distract=["a) 588 N is just the weight $mg$.", "b) 2350 subtracts $mg$ (the top-of-loop sign).",
              "c) 2940 forgets to add $mg$.", "e) 7060 doubles it."],
    fig=f6, figsize=(3.6, 2.3)))

# 7 ------------------------------------------------------------ single block down incline, disk pulley (no hanging mass)
s35, c35 = sin(radians(35)), cos(radians(35))
B7 = 3 * s35 - 0.2 * 3 * c35
v7 = sqrt(2 * g * 1.5 * B7 / (3 + 1))


def f7(ax):
    t = radians(35)
    ax.add_patch(Polygon([(0, 2.8), (2.8 / np.tan(t), 0), (0, 0)], closed=True, fill=False, lw=1.5))
    down = np.array([np.cos(t), -np.sin(t)]); n = np.array([np.sin(t), np.cos(t)])
    pc = np.array([0.0, 2.8]) + n * 0.45; ax.add_patch(Circle(pc, 0.35, fill=False, lw=1.5)); ax.plot(*pc, "k.")
    b0 = np.array([0, 2.8]) + down * 1.6; c = block_on(ax, b0, down, n, size=0.55, label=r"$m$")
    ax.plot([pc[0] + n[0] * 0.35, b0[0] + n[0] * 0.28], [pc[1] + n[1] * 0.35, b0[1] + n[1] * 0.28], "k", lw=1)
    arrow(ax, c + down * 0.5, c + down * 1.3); ax.text(2.8, 0.15, r"$35^\circ$", fontsize=10)
    ax.text(1.2, 0.5, r"$\mu = 0.20$", fontsize=10); ax.text(pc[0] - 0.6, pc[1] + 0.45, "disk", fontsize=9)
    ax.set_xlim(-0.8, 4.2); ax.set_ylim(-0.2, 3.7)


Q.append(dict(
    stem=r"A 3.0 kg block starts from rest and slides **down** a $35^\circ$ incline ($\mu = 0.20$). It is tied by a light string to a pulley at the top of the incline. The pulley is a uniform disk ($I = \tfrac12 MR^2$, $M = 2.0$ kg) that unwinds as the block slides. How fast is the block moving after it has slid 1.5 m?",
    choices=["2.69 m/s", "3.01 m/s", "3.47 m/s", "3.56 m/s", "4.11 m/s"], key="b",
    check=("near", v7, [2.69, 3.01, 3.47, 3.56, 4.11], 0.005),
    value="3.01 m/s", topic="Block down an incline with a disk pulley", source="2015 Exam 2 #13", card="Incline + hanging mass + pulley ($m_2 = 0$)",
    solution=r"""
Notecard, incline + pulley, with no hanging mass ($m_2 = 0$) and the block sliding **down**:

$$v_f = \sqrt{v_i^2 + \frac{2g\,\Delta x\,B}{m + I/R^2}}, \qquad B = m\sin\theta - \mu m\cos\theta$$

**Net pull** ($\sin 35^\circ = 0.5736$, $\cos 35^\circ = 0.8192$):

$$B = 3.0(0.5736) - 0.20(3.0)(0.8192) = 1.721 - 0.492 = 1.229\ \text{kg}$$

**Pulley term:** disk, $I/R^2 = \tfrac12 M = 1.0$ kg.

**Plug in** ($v_i = 0$):

$$
\begin{aligned}
v_f &= \sqrt{\frac{2(9.8)(1.5)(1.229)}{3.0 + 1.0}} \\[8pt]
&= \sqrt{\frac{36.14}{4.0}} = \sqrt{9.04} = 3.01\ \text{m/s}
\end{aligned}
$$
""",
    distract=["a) 2.69 treats the pulley as a ring.", "c) 3.47 ignores the pulley's mass.",
              "d) 3.56 ignores friction.", "e) 4.11 ignores both friction and the pulley."],
    fig=f7, figsize=(2.8, 2.4)))

# 8 ------------------------------------------------------------ force: rebound at a different speed
F8 = 0.40 * (10 - (-15)) / 0.050


def f8(ax):
    ax.plot([3.0, 3.0], [-0.8, 0.8], "k", lw=2)
    for k in range(8):
        ax.plot([3.0, 3.2], [-0.8 + k * 0.2, -0.6 + k * 0.2], "k", lw=0.8)
    ax.add_patch(Circle((2.7, 0), 0.25, fill=False, lw=1.5))
    arrow(ax, (0.6, 0.3), (2.2, 0.3)); arrow(ax, (2.2, -0.3), (1.0, -0.3))
    ax.text(1.4, 0.55, r"$15$ m/s in", ha="center", fontsize=10); ax.text(1.6, -0.7, r"$10$ m/s out", ha="center", fontsize=10)
    ax.set_xlim(0.3, 3.4); ax.set_ylim(-1.0, 0.9)


Q.append(dict(
    stem=r"A 0.40 kg ball hits a wall head-on at 15 m/s and bounces straight back at 10 m/s. The ball is in contact with the wall for 0.050 s. What is the magnitude of the average force on the ball?",
    choices=["40 N", "80 N", "120 N", "160 N", "200 N"], key="e",
    check=("near", F8, [40, 80, 120, 160, 200], 1),
    value="200 N", topic="Force from a change in momentum", source="Ch 9 notes p. 1/5", card="Force from $\\Delta p$",
    solution=r"""
Notecard: $F = \dfrac{m(v_f - v_i)}{t}$ with **signs**. Take "away from the wall" as $+$, so $v_i = -15$ m/s and $v_f = +10$ m/s.

$$F = \frac{m(v_f - v_i)}{t}$$

**Plug in:**

$$F = \frac{0.40\,(10 - (-15))}{0.050} = \frac{0.40(25)}{0.050} = 200\ \text{N}$$
""",
    distract=["a) 40 uses $15 - 10$ (ignores the reversal).", "b) 80 uses only the rebound speed.",
              "c) 120 uses only the incoming speed (as if it stopped).", "d) 160 uses $15 + 5$."],
    fig=f8, figsize=(3.2, 1.6)))

# 9 ------------------------------------------------------------ inelastic KE fraction (equal momenta)
vf9 = (1 * 1 + 3 * (-1 / 3)) / 4


def f9(ax):
    ax.plot([-0.3, 5.2], [0, 0], "k", lw=1.5)
    for x0, w, lab in [(0, 0.9, r"$m$"), (3.2, 1.8, r"$3m$")]:
        ax.add_patch(Rectangle((x0, 0.15), w, 0.6, fill=False, lw=1.5)); ax.text(x0 + w / 2, 0.45, lab, ha="center", va="center")
    arrow(ax, (1.0, 0.45), (1.9, 0.45)); ax.text(1.2, 0.95, r"$v$", fontsize=11)
    arrow(ax, (3.1, 0.45), (2.4, 0.45)); ax.text(2.4, 0.95, r"$v/3$", fontsize=11)
    ax.set_xlim(-0.4, 5.3); ax.set_ylim(-0.1, 1.2)


Q.append(dict(
    stem=r"A cart of mass $m$ moving right at speed $v$ collides head-on with a cart of mass $3m$ moving **left** at speed $v/3$. The carts couple together. What fraction of the initial kinetic energy is retained after the collision?",
    choices=["0%", "25%", "50%", "75%", "100%"], key="a",
    check=("near", 0.0 if abs(vf9) < 1e-12 else 100 * vf9, [0, 25, 50, 75, 100], 1),
    value="0%", topic="Inelastic collision, KE fraction", source="Ch 9 notes p. 1/5; 2015 Exam 2 #7", card="Stick (inelastic)",
    solution=r"""
Symbolic masses and speeds, so **set $m = 1$ and $v = 1$**. Right is $+$: $m_1 = 1$, $v_1 = +1$; $m_2 = 3$, $v_2 = -\tfrac13$.

**Final velocity** (notecard):

$$v_f = \frac{m_1v_1 + m_2v_2}{m_1 + m_2} = \frac{(1)(1) + (3)(-\tfrac13)}{4} = \frac{1 - 1}{4} = 0$$

The momenta are equal and opposite, so the carts **stop dead**. Then

$$\frac{K_f}{K_i} = \frac{(m_1 + m_2)v_f^2}{m_1v_1^2 + m_2v_2^2} = \frac{4(0)^2}{1 + 3(\tfrac19)} = 0$$

All of the kinetic energy is lost.
""",
    distract=["b) 25% is the mass ratio $\\frac{m}{4m}$, which only applies when one cart starts at rest.",
              "c) and d) come from treating the second cart as moving the same way.", "e) 100% would need an elastic collision."],
    fig=f9, figsize=(3.6, 0.9)))

# 10 ----------------------------------------------------------- elastic head-on, both moving
v10_1 = ((2 - 3) * 5 + 2 * 3 * (-4)) / 5
v10_2 = 5 + v10_1 - (-4)


def f10(ax):
    ax.add_patch(Circle((0, 0), 0.32, fill=False, lw=1.5)); ax.add_patch(Circle((3, 0), 0.4, fill=False, lw=1.5))
    arrow(ax, (0.4, 0), (1.3, 0)); arrow(ax, (2.55, 0), (1.75, 0))
    ax.text(0, -0.8, r"$2$ kg, $+5$ m/s", ha="center"); ax.text(3, -0.8, r"$3$ kg, $-4$ m/s", ha="center")
    ax.set_xlim(-0.8, 3.9); ax.set_ylim(-1.1, 0.6)


Q.append(dict(
    stem=r"A 2.0 kg ball moving right at 5.0 m/s collides **elastically** head-on with a 3.0 kg ball moving left at 4.0 m/s. What is the velocity of the 3.0 kg ball after the collision? Positive to the right / negative to the left.",
    choices=["+5.8 m/s", "+5.0 m/s", "+4.0 m/s", "+3.2 m/s", "−0.4 m/s"], key="d",
    check=("near", v10_2, [5.8, 5.0, 4.0, 3.2, -0.4], 0.05),
    value="+3.2 m/s", topic="1-D elastic collision, head-on", source="Ch 9 notes p. 2/5–3/5; 2015 Exam 2 #6", card="Elastic",
    solution=r"""
Notecard formulas, right $= +$: $m_1 = 2.0$, $v_{1i} = +5.0$; $m_2 = 3.0$, $v_{2i} = -4.0$.

$$
\begin{aligned}
v_{1f} &= \frac{(m_1 - m_2)v_{1i} + 2m_2v_{2i}}{m_1 + m_2} = \frac{(-1.0)(5.0) + 2(3.0)(-4.0)}{5.0} = \frac{-5 - 24}{5} = -5.8\ \text{m/s} \\[8pt]
v_{2f} &= v_{1i} + v_{1f} - v_{2i} = 5.0 + (-5.8) - (-4.0) = +3.2\ \text{m/s}
\end{aligned}
$$

The 3.0 kg ball reverses and moves right at 3.2 m/s.
""",
    distract=["a) +5.8 is the size of the 2.0 kg ball's velocity, not the 3.0 kg ball's.", "b) +5.0 assumes the balls swap velocities.",
              "c) +4.0 assumes the 3.0 kg ball just reverses at the same speed.", "e) −0.4 is the stick-together answer."],
    fig=f10, figsize=(3.6, 1.1)))

# 11 ----------------------------------------------------------- ballistic KE fraction bins
frac11 = 100 * 0.020 / (3.98 + 0.020)
assert 0.1 < frac11 < 1


def f11(ax):
    ax.plot([1.2, 3.2], [3, 3], "k", lw=2); ax.plot([1.8, 1.8], [3, 1.4], "k", lw=1); ax.plot([2.6, 2.6], [3, 1.4], "k", lw=1)
    ax.add_patch(Rectangle((1.5, 0.4), 1.4, 1.0, fill=False, lw=1.5)); ax.text(2.2, 0.9, "3.98 kg", ha="center", va="center", fontsize=9)
    ax.add_patch(Ellipse((0.2, 0.9), 0.35, 0.14, fill=True, color="k")); arrow(ax, (0.45, 0.9), (1.2, 0.9)); ax.text(0.0, 1.15, "0.020 kg", fontsize=9)
    ax.set_xlim(-0.2, 3.4); ax.set_ylim(0.2, 3.2)


Q.append(dict(
    stem=r"A 0.020 kg bullet is fired into a 3.98 kg block of wood hanging at rest from light strings, and lodges in it. The block swings upward. What fraction of the bullet's initial kinetic energy remains in the motion of the block (with the bullet) just after the collision?",
    choices=["< 0.1%", "0.1–1%", "1–10%", "10–50%", "> 50%"], key="b",
    check=("concept",),
    value="0.5%", topic="Ballistic pendulum, KE kept", source="Ch 9 notes p. 5/5; 2015 Exam 2 #8", card="Ballistic",
    solution=r"""
Notecard: $\dfrac{K_f}{K_i} = \dfrac{m}{M + m}$ (no speed or height needed).

$$\frac{K_f}{K_i} = \frac{0.020}{3.98 + 0.020} = \frac{0.020}{4.00} = 0.005 = 0.5\%$$

That falls in the 0.1–1% range.
""",
    distract=["a) < 0.1% would need a much heavier block (2015 Exam #8 used $M = 10$ kg and a 5 g bullet).",
              "e) > 50% would mean the collision kept most of the KE; sticking collisions with $m \\ll M$ lose almost all of it."],
    fig=f11, figsize=(2.6, 2.1)))

# 12 ----------------------------------------------------------- parallel axis, rod
I12 = 2.0 * (1.0 ** 2 / 12 + (0.5 - 0.2) ** 2)


def f12(ax):
    ax.add_patch(Rectangle((0, -0.12), 4.0, 0.24, fill=False, lw=1.5)); ax.plot([0.8], [0], "ko"); ax.plot([2.0], [0], "k+", ms=10)
    ax.text(0.8, 0.45, "axis", ha="center", fontsize=10); ax.text(2.0, 0.45, "center", ha="center", fontsize=10)
    dim(ax, (0, -0.45), (0.8, -0.45), r"$0.20$ m", offset=(0, -0.3), fontsize=10)
    dim(ax, (0, -1.05), (4.0, -1.05), r"$\ell = 1.0$ m", offset=(0, -0.3), fontsize=10)
    ax.set_xlim(-0.2, 4.2); ax.set_ylim(-1.6, 0.7)


Q.append(dict(
    stem=r"A thin uniform rod has mass 2.0 kg and length 1.0 m ($I_{cm} = \tfrac1{12}m\ell^2$). It rotates about an axis perpendicular to the rod, located 0.20 m from one end. What is the rod's moment of inertia about this axis?",
    choices=["0.08 kg·m²", "0.17 kg·m²", "0.25 kg·m²", "0.35 kg·m²", "0.67 kg·m²"], key="d",
    check=("near", I12, [0.08, 0.17, 0.25, 0.35, 0.67], 0.005),
    value="0.35 kg·m²", topic="Parallel axis theorem, rod", source="Ch 10 notes p. 2/8", card="Parallel axis",
    solution=r"""
Notecard rod shortcut, axis $a$ from one end:

$$I = m\left[\frac{\ell^2}{12} + \left(\frac{\ell}{2} - a\right)^2\right]$$

$d = \dfrac{\ell}{2} - a = 0.50 - 0.20 = 0.30$ m from the **center**.

**Plug in:**

$$
\begin{aligned}
I &= 2.0\left[\frac{1.0^2}{12} + (0.50 - 0.20)^2\right] \\[8pt]
&= 2.0(0.0833 + 0.090) = 0.35\ \text{kg·m}^2
\end{aligned}
$$

Check: it's between $I_{cm} = 0.17$ and $I_{end} = \tfrac13 m\ell^2 = 0.67$.
""",
    distract=["a) 0.08 is $ma^2$, measured from the end.", "b) 0.17 is $I_{cm}$ alone.",
              "c) 0.25 is the #1 mistake: $I_{cm} + ma^2$, using the distance from the **end**.", "e) 0.67 is the rod about its end."],
    fig=f12, figsize=(3.6, 1.6)))

# 13 ----------------------------------------------------------- rolling sphere, omega
v13 = sqrt(10 / 7 * g * 0.80)
w13 = v13 / 0.050


def f13(ax):
    up, top, n = incline(ax, 18, 6, origin=(6, 0))
    c0 = top - up * 0.6 + n * 0.35; ax.add_patch(Circle(c0, 0.35, fill=False, lw=1.5)); ax.text(c0[0] + 0.45, c0[1] + 0.35, r"$v_i = 0$")
    c1 = np.array([6, 0]) + up * 1.2 + n * 0.35; ax.add_patch(Circle(c1, 0.35, fill=False, lw=1.5, ls="--")); ax.text(c1[0] - 0.3, c1[1] + 0.55, r"$\omega = ?$")
    dim(ax, (top[0] - 0.3, 0), (top[0] - 0.3, top[1]), r"$0.80$ m", offset=(-0.5, 0), fontsize=10)
    ax.set_xlim(-1.2, 6.3); ax.set_ylim(-0.2, 2.6)


Q.append(dict(
    stem=r"A solid sphere ($I = \tfrac25 MR^2$, $M = 1.5$ kg, $R = 0.050$ m) starts from rest and rolls without slipping down an incline from a height of 0.80 m. What is its rotational velocity $\omega$ at the bottom?",
    choices=["3.3 rad/s", "33 rad/s", "56 rad/s", "65 rad/s", "67 rad/s"], key="e",
    check=("near", w13, [3.3, 33, 56, 65, 67], 0.5),
    value="67 rad/s", topic="Rolling sphere, find $\\omega$", source="Ch 10 notes p. 6/8–8/8; 2015 Exam 2 #10", card="Rolling (sphere row)",
    solution=r"""
Notecard, sphere row: $v = \sqrt{\tfrac{10}{7}gh}$, then $\omega = \dfrac{v}{R}$.

**Speed:**

$$v = \sqrt{\tfrac{10}{7}(9.8)(0.80)} = \sqrt{11.2} = 3.35\ \text{m/s}$$

**Rotational velocity:**

$$\omega = \frac{v}{R} = \frac{3.35}{0.050} = 67\ \text{rad/s}$$
""",
    distract=["a) 3.3 is $v$ (m/s), not $\\omega$.", "b) 33 divides by the diameter (0.10 m) instead of the radius.",
              "c) 56 uses the ring formula, $\\sqrt{gh}$.", "d) 65 uses the disk formula, $\\sqrt{\\tfrac43 gh}$."],
    fig=f13, figsize=(3.6, 1.6)))

# 14 ----------------------------------------------------------- jump on at r < R
I14 = 0.5 * 200 * 2.5 ** 2
w14 = (I14 * 0.80 + 30 * 4.0 * 1.5) / (I14 + 30 * 1.5 ** 2)


def f14(ax):
    disk_top_view(ax, (0, 0), 1.25)
    ax.plot([0, 0], [0, -0.75], "k", lw=1); ax.text(0.08, -0.4, r"$1.5$ m", fontsize=9)
    arrow(ax, (-2.4, -0.75), (-0.1, -0.75)); ax.add_patch(Circle((-2.6, -0.75), 0.12, fill=True, color="k"))
    ax.text(-2.5, -0.45, r"$4.0$ m/s", fontsize=10)
    arrow(ax, (0.95, 0.95), (0.2, 1.3), connectionstyle="arc3,rad=0.25"); ax.text(1.0, 1.05, r"$\omega_i$")
    ax.set_xlim(-2.9, 1.6); ax.set_ylim(-1.4, 1.5)


Q.append(dict(
    stem=r"A merry-go-round (a disk, $I = \tfrac12 MR^2$, $M = 200$ kg, $R = 2.5$ m) rotates at 0.80 rad/s. A 30 kg child runs at 4.0 m/s in the direction of rotation, along a line that passes 1.5 m from the center, and jumps on at that point (1.5 m from the center, not at the rim). What is the new angular velocity?",
    choices=["0.72 rad/s", "0.80 rad/s", "0.98 rad/s", "1.09 rad/s", "1.16 rad/s"], key="c",
    check=("near", w14, [0.72, 0.80, 0.98, 1.09, 1.16], 0.005),
    value="0.98 rad/s", topic="Person runs and jumps on inside the rim", source="Ch 11 notes p. 4/8; 2015 Exam 2 #12", card="Angular momentum",
    solution=r"""
Notecard with $+mvr$ (running with the rotation) and $I_{add} = mr^2$, where $r = 1.5$ m is where the child lands:

$$\omega_f = \frac{I_1\omega_1 + mvr}{I_1 + mr^2}$$

**Platform:** $I_1 = \tfrac12(200)(2.5)^2 = 625$ kg·m².

**Plug in:**

$$
\begin{aligned}
\omega_f &= \frac{(625)(0.80) + (30)(4.0)(1.5)}{625 + (30)(1.5)^2} \\[8pt]
&= \frac{500 + 180}{625 + 67.5} = \frac{680}{692.5} = 0.98\ \text{rad/s}
\end{aligned}
$$

Use $r = 1.5$ m in **both** places (the child's $L = mvr$ and their $I = mr^2$), not the rim radius.
""",
    distract=["a) 0.72 ignores the child's running momentum.", "b) 0.80 is no change.",
              "d) 1.09 forgets to add the child's $mr^2$.", "e) 1.16 uses the rim radius 2.5 m in $mvr$."],
    fig=f14, figsize=(3.2, 2.0)))

# 15 ----------------------------------------------------------- rotational kinematics, time from angle
t15 = sqrt(2 * 50 / 4.0)


def f15(ax):
    ax.add_patch(Circle((0, 0), 1.0, fill=False, lw=1.5))
    for a in np.radians([0, 60, 120, 180, 240, 300]):
        ax.plot([0, np.cos(a)], [0, np.sin(a)], "k", lw=0.8)
    arrow(ax, (1.25, -0.3), (0.5, 1.2), connectionstyle="arc3,rad=0.45"); ax.text(1.2, 0.9, r"$\alpha$")
    ax.text(-1.2, -1.4, r"from rest, $\Delta\theta = 50$ rad", fontsize=9)
    ax.set_xlim(-1.3, 1.6); ax.set_ylim(-1.5, 1.3)


Q.append(dict(
    stem=r"A wheel starts from rest and speeds up with a constant angular acceleration of 4.0 rad/s². How long does it take to turn through 50 rad?",
    choices=["5.0 s", "6.25 s", "12.5 s", "25 s", "50 s"], key="a",
    check=("near", t15, [5.0, 6.25, 12.5, 25, 50], 0.05),
    value="5.0 s", topic="Rotational kinematics, time from an angle", source="Ch 10 notes p. 1/8", card="Rot. kinematics",
    solution=r"""
$\omega_f$ isn't given or asked for, so use the equation without it:

$$\Delta\theta = \omega_i t + \tfrac12\alpha t^2$$

**Solve for $t$** (starting from rest, $\omega_i = 0$):

$$
\begin{aligned}
\Delta\theta &= \tfrac12\alpha t^2 \\[8pt]
t &= \sqrt{\frac{2\,\Delta\theta}{\alpha}}
\end{aligned}
$$

**Plug in:**

$$t = \sqrt{\frac{2(50)}{4.0}} = \sqrt{25} = 5.0\ \text{s}$$
""",
    distract=["b) 6.25 is $\\Delta\\theta/2\\alpha$ with no root.", "c) 12.5 is $\\Delta\\theta/\\alpha$.",
              "d) 25 is $2\\Delta\\theta/\\alpha$ (forgot the square root).", "e) 50 is just $\\Delta\\theta$."],
    fig=f15, figsize=(2.6, 2.4)))

INTRO = r"""
Practice Exam 2-5 reuses the exam's problem types with new twists: a coaster with a starting speed, the compression **needed** for a launch, $N$ at the **bottom** of a loop, a rebound at a different speed, a collision where the carts stop dead, a child landing **inside** the rim. Question 1 is a **minimum** trap: round up to the choice that works. The last column says which 3×5 notecard entry solves each question.
"""

if __name__ == "__main__":
    build(5, "Chapters 6, 7/8, 9, 10, 11", Q, INTRO)
