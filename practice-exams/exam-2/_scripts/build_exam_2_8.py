"""Practice Exam 2-8: the professor's lecture-note examples, one per question,
with new numbers.

Run:  PYTHONIOENCODING=utf-8 python practice-exams/exam-2/_scripts/build_exam_2_8.py
"""
from math import cos, radians, sin, sqrt

import figs
from examlib import build

g = 9.8
Q = []

# 1 -- notes p.4-5/18 halfpipe with a rough strip ("it rains in the night")
h1 = 2.5 - 0.02 * 8.0
Q.append(dict(
    stem=r"A skater starts from rest at a height of 2.5 m on one side of a halfpipe. Overnight a puddle dried and left a rough strip 8.0 m long on the flat bottom with $\mu_k = 0.02$; the rest of the halfpipe is frictionless. How high up the far side does the skater rise?",
    choices=["2.34 m", "2.26 m", "2.18 m", "2.10 m", "2.02 m"], key="a",
    check=("near", h1, [2.34, 2.26, 2.18, 2.10, 2.02], 0.02),
    value="2.34 m", topic="Halfpipe with a rough strip", source="Ch 7/8 notes p. 4/18–5/18", card="Halfpipe",
    solution=r"""
Notecard, from rest, one crossing:

$$h_f = h_i - \mu L$$

**Plug in:**

$$h_f = 2.5 - (0.02)(8.0) = 2.5 - 0.16 = 2.34\ \text{m}$$
""",
    distract=["b)–e) subtract the friction loss 1.5, 2, 2.5 and 3 times. Crossing the strip once loses $\\mu L$ once."],
    fig=figs.halfpipe(r"$h_i = 2.5$ m", r"$L = 8.0$ m, $\mu_k = 0.02$", r"$h_f = ?$"), figsize=(4.2, 2.0)))

# 2 -- notes p.3/18 roller coaster
v2 = sqrt(2 * g * (75 - 30))
Q.append(dict(
    stem=r"A roller coaster car starts from rest at the top of a 75 m hill and rolls down a frictionless track. How fast is it moving at a point on the track 30 m above the ground?",
    choices=["21.0 m/s", "29.7 m/s", "38.3 m/s", "42.0 m/s", "882 m/s"], key="b",
    check=("near", v2, [21.0, 29.7, 38.3, 42.0, 882], 0.05),
    value="29.7 m/s", topic="Roller coaster", source="Ch 7/8 notes p. 3/18", card="Fall / coaster",
    solution=r"""
Notecard (no friction, from rest):

$$v_f = \sqrt{v_i^2 + 2g(h_i - h_f)} = \sqrt{2g(h_i - h_f)}$$

**Plug in:**

$$v_f = \sqrt{2(9.8)(75 - 30)} = \sqrt{882} = 29.7\ \text{m/s}$$
""",
    distract=["a) 21.0 forgets the 2.", "c) 38.3 uses the full 75 m drop.", "d) 42.0 doubles the drop.", "e) 882 forgets the square root."],
    fig=figs.coaster(r"$75$ m", r"$30$ m"), figsize=(3.8, 1.7)))

# 3 -- notes p.6/18 sliding up a frictionless incline
s12 = sin(radians(12))
v3 = sqrt(5.0 ** 2 - 2 * g * 4.0 * s12)
Q.append(dict(
    stem=r"A block slides up a frictionless incline ($\theta = 12^\circ$) with an initial speed of 5.0 m/s. How fast is it moving after it has slid 4.0 m along the incline?",
    choices=["2.95 m/s", "4.10 m/s", "6.43 m/s", "8.70 m/s", "it stops before it slides the whole 4.0 m"], key="a",
    check=("near", v3, [2.95, 4.10, 6.43, 8.70, None], 0.005),
    value="2.95 m/s", topic="Sliding up a frictionless incline", source="Ch 7/8 notes p. 6/18", card="One block on incline (Up, $\\mu = 0$)",
    solution=r"""
Notecard, sliding up, with $\mu = 0$:

$$v_f = \sqrt{v_i^2 - 2g\,\Delta x\sin\theta}$$

**Plug in** ($\sin 12^\circ = 0.2079$):

$$v_f = \sqrt{5.0^2 - 2(9.8)(4.0)(0.2079)} = \sqrt{25 - 16.30} = \sqrt{8.70} = 2.95\ \text{m/s}$$
""",
    distract=["b) 4.10 forgets the 2.", "c) 6.43 adds instead of subtracts.", "d) 8.70 forgets the square root.", "e) comes from using $\\cos\\theta$."],
    fig=figs.slope_block(12, "up", r"$v_i = 5.0$ m/s", r"$\mu = 0$"), figsize=(3.8, 1.3)))

# 4 -- notes p.9/18 rough incline, stops early -> how far
s15, c15 = sin(radians(15)), cos(radians(15))
vf2_4 = 4.0 ** 2 - 2 * g * 3.0 * (s15 + 0.30 * c15)
dx4 = 4.0 ** 2 / (2 * g * (s15 + 0.30 * c15))
assert vf2_4 < 0
Q.append(dict(
    stem=r"A block is given a speed of 4.0 m/s up a $15^\circ$ incline with $\mu_k = 0.30$. How far up the incline does it slide before it comes to rest?",
    choices=["0.74 m", "1.49 m", "2.98 m", "3.15 m", "6.30 m"], key="b",
    check=("near", dx4, [0.74, 1.49, 2.98, 3.15, 6.30], 0.005),
    value="1.49 m", topic="Rough incline, sliding up: stopping distance", source="Ch 7/8 notes p. 9/18", card="One block on incline (Stop up)",
    solution=r"""
Notecard, stop up:

$$\Delta x = \frac{v_i^2}{2g(\sin\theta + \mu\cos\theta)}$$

**Plug in** ($\sin 15^\circ = 0.2588$, $\cos 15^\circ = 0.9659$):

$$\Delta x = \frac{4.0^2}{2(9.8)(0.2588 + 0.30 \times 0.9659)} = \frac{16}{19.6(0.5486)} = 1.49\ \text{m}$$
""",
    distract=["a) 0.74 has an extra factor of 2.", "c) 2.98 forgets the 2.", "d) 3.15 ignores friction.", "e) 6.30 ignores friction and the 2."],
    fig=figs.slope_block(15, "up", r"$v_i = 4.0$ m/s", r"$\mu_k = 0.30$", extra=r"$\Delta x = ?$"), figsize=(3.8, 1.5)))

# 5 -- notes p.10/18 sliding down a rough incline, stopping distance
s8, c8 = sin(radians(8)), cos(radians(8))
dx5 = 2.5 ** 2 / (2 * g * (0.25 * c8 - s8))
Q.append(dict(
    stem=r"A block is sliding **down** an $8^\circ$ incline ($\mu_k = 0.25$) at 2.5 m/s. How far does it slide before it comes to rest?",
    choices=["0.82 m", "1.29 m", "2.94 m", "5.88 m", "it never stops; it speeds up"], key="c",
    check=("near", dx5, [0.82, 1.29, 2.94, 5.88, None], 0.01),
    value="2.94 m", topic="Rough incline, sliding down: stopping distance", source="Ch 7/8 notes p. 10/18", card="One block on incline (Stop down)",
    solution=r"""
It stops, because $\mu\cos\theta = 0.248$ is bigger than $\sin\theta = 0.139$. Notecard, stop down:

$$\Delta x = \frac{v_i^2}{2g(\mu\cos\theta - \sin\theta)}$$

**Plug in** ($\sin 8^\circ = 0.1392$, $\cos 8^\circ = 0.9903$):

$$\Delta x = \frac{2.5^2}{2(9.8)(0.25 \times 0.9903 - 0.1392)} = \frac{6.25}{19.6(0.1084)} = 2.94\ \text{m}$$

The bracket is small (0.108), so keep 4 digits in the trig values.
""",
    distract=["a) 0.82 uses the sliding-**up** bracket.", "b) 1.29 leaves out $\\sin\\theta$.", "d) 5.88 forgets the 2.", "e) It does stop, since $\\mu\\cos\\theta > \\sin\\theta$."],
    fig=figs.slope_block(8, "down", r"$2.5$ m/s", r"$\mu_k = 0.25$", extra=r"$\Delta x = ?$"), figsize=(3.8, 1.2)))

# 6 -- notes p.11/18 mass slides down a ramp into a spring
x6 = sqrt(2 * 2.0 * g * 1.5 / 1500)
Q.append(dict(
    stem=r"A 2.0 kg mass starts from rest at the top of a frictionless ramp 1.5 m high. It slides down and across a frictionless floor into a spring with $k = 1500$ N/m. How far is the spring compressed when the mass comes to rest?",
    choices=["0.020 m", "0.039 m", "0.099 m", "0.14 m", "0.20 m"], key="e",
    check=("near", x6, [0.020, 0.039, 0.099, 0.14, 0.20], 0.005),
    value="0.20 m", topic="Mass slides into a spring", source="Ch 7/8 notes p. 11/18", card="Spring (stop a mass)",
    solution=r"""
Notecard, stop a mass, starting from rest ($v_i = 0$):

$$x = \sqrt{\frac{2mgh + mv_i^2}{k}} = \sqrt{\frac{2mgh}{k}}$$

**Plug in:**

$$x = \sqrt{\frac{2(2.0)(9.8)(1.5)}{1500}} = \sqrt{0.0392} = 0.20\ \text{m}$$
""",
    distract=["a) 0.020 is $mgh/k$ (no 2, no root).", "b) 0.039 forgets the square root.",
              "c) 0.099 has the 2 upside down.", "d) 0.14 forgets the 2."],
    fig=figs.ramp_spring(r"$1.5$ m", r"$k$"), figsize=(3.8, 1.6)))

# 7 -- notes p.14/18 power climbing stairs
P7 = 80 * g * 18 / 15
Q.append(dict(
    stem=r"An 80 kg man climbs 18 m of stairs in 15 s. What is his average power output?",
    choices=["96 W", "941 W", "1880 W", "14,100 W", "254,000 W"], key="b",
    check=("near", P7, [96, 941, 1880, 14100, 254000], 2),
    value="941 W", topic="Power climbing stairs", source="Ch 7/8 notes p. 14/18", card="Power",
    solution=r"""
Notecard:

$$P = \frac{mgh}{t}$$

**Plug in:**

$$P = \frac{(80)(9.8)(18)}{15} = \frac{14{,}112}{15} = 941\ \text{W}$$
""",
    distract=["a) 96 forgets $g$.", "c) 1880 doubles it.", "d) 14,100 is the work $mgh$ in joules, not power.", "e) 254,000 multiplies by $t$."],
    fig=figs.stairs(r"$18$ m", r"$t = 15$ s"), figsize=(3.0, 2.0)))

# 8 -- notes p.15-16/18 block up an incline, hanging mass, stops early
s25, c25 = sin(radians(25)), cos(radians(25))
B8 = 3.0 - 15 * s25 - 0.30 * 15 * c25
vf2_8 = 2.5 ** 2 + 2 * g * 1.0 * B8 / 18
dx8 = (15 + 3.0) * 2.5 ** 2 / (-2 * g * B8)
Q.append(dict(
    stem=r"A 15 kg block on a $25^\circ$ incline ($\mu_k = 0.30$) is tied by a light string over a massless pulley to a 3.0 kg hanging mass. The block is moving **up** the incline at 2.5 m/s (the hanging mass is moving down). How fast is the block moving after it has slid 1.0 m up the incline?",
    choices=["1.49 m/s", "1.62 m/s", "2.33 m/s", "3.79 m/s", "it stops before it slides the whole 1.0 m"], key="e",
    check=("stops", vf2_8),
    value="stops (at 0.77 m)", topic="Incline + hanging mass, stops early", source="Ch 7/8 notes p. 15/18–16/18", card="Incline + hanging mass + pulley",
    solution=rf"""
Notecard, $m_2$ falls ($m_1$ slides **up**), massless pulley:

$$v_f = \sqrt{{v_i^2 + \frac{{2g\,\Delta x\,B}}{{m_1 + m_2}}}}$$

$$B = m_2 - m_1\sin\theta - \mu m_1\cos\theta$$

**Net pull:**

$$B = 3.0 - 15(0.4226) - 0.30(15)(0.9063) = 3.0 - 6.339 - 4.078 = -7.42\ \text{{kg}}$$

**Plug in:**

$$v_f = \sqrt{{2.5^2 + \frac{{2(9.8)(1.0)(-7.42)}}{{18}}}} = \sqrt{{6.25 - 8.08}} = \sqrt{{-1.83}}$$

Negative under the root: it "doesn't go 1.0 m." **Where it stops** (notecard):

$$\Delta x = \frac{{-(m_1 + m_2)v_i^2}}{{2gB}} = \frac{{-(18)(6.25)}}{{2(9.8)(-7.42)}} = {dx8:.2f}\ \text{{m}}$$
""",
    distract=["a) 1.49 forgets the 2 in $2g$.", "b) 1.62 ignores friction.", "c) 2.33 uses the $m_1$-slides-down $B$.", "d) 3.79 adds the bracket instead of subtracting it."],
    fig=figs.incline_hanging(r"$25^\circ$", r"$\mu_k = 0.30$", r"$2.5$ m/s", m1_dir="up"), figsize=(4.0, 2.1)))

# 9 -- notes p.12-13/18 loop, minimum launch height (min trap)
h9 = 2.5 * 9.0
Q.append(dict(
    stem=r"A roller coaster car is launched from rest at height $h$ on a frictionless track that leads into a vertical circular loop of radius $R = 9.0$ m. How high must the launch height be for the car to stay on the track (barely) at the top of the loop?",
    choices=["18 m", "20 m", "22 m", "24 m", "27 m"], key="d",
    check=("min", h9, [18, 20, 22, 24, 27]),
    value="22.5 m → 24", topic="Loop-the-loop, minimum launch height", source="Ch 7/8 notes p. 12/18–13/18", card="Loop",
    solution=r"""
Notecard: launch $h = \tfrac52 R$ (from $v_t = \sqrt{gR}$ at the top plus energy).

**Plug in:**

$$h = \tfrac52(9.0) = 22.5\ \text{m}$$

**Answer-choice trap.** 22.5 m is a **minimum**. From 22 m the car falls off at the top, even though 22 is the closest number. The smallest choice that works is **d) 24 m**.
""",
    distract=["a) 18 m is $2R$: it reaches the top with zero speed.", "c) 22 m is the nearest number, but it's below the minimum.", "e) 27 m is $3R$ (works, but isn't the minimum choice)."],
    fig=figs.loop(left_label=r"$h = ?$", ramp=True), figsize=(3.6, 2.3)))

# 10 -- notes p.3/5 elastic collision, both moving right
v10_1 = (4 * 4.0 + 2 * 2 * 1.0) / 8
v10_2 = 4.0 + v10_1 - 1.0
Q.append(dict(
    stem=r"A 6.0 kg ball moving right at 4.0 m/s catches up to and collides **elastically** with a 2.0 kg ball moving right at 1.0 m/s. What is the velocity of the 2.0 kg ball after the collision?",
    choices=["+1.0 m/s", "+2.5 m/s", "+3.25 m/s", "+4.0 m/s", "+5.5 m/s"], key="e",
    check=("near", v10_2, [1.0, 2.5, 3.25, 4.0, 5.5], 0.05),
    value="+5.5 m/s", topic="1-D elastic collision", source="Ch 9 notes p. 3/5", card="Elastic",
    solution=r"""
Notecard formulas, right $= +$: $m_1 = 6.0$, $v_{1i} = +4.0$; $m_2 = 2.0$, $v_{2i} = +1.0$.

$$v_{1f} = \frac{(m_1 - m_2)v_{1i} + 2m_2v_{2i}}{m_1 + m_2} = \frac{(4.0)(4.0) + 2(2.0)(1.0)}{8.0} = \frac{20}{8} = +2.5\ \text{m/s}$$

$$v_{2f} = v_{1i} + v_{1f} - v_{2i} = 4.0 + 2.5 - 1.0 = +5.5\ \text{m/s}$$
""",
    distract=["a) +1.0 is no change.", "b) +2.5 is the 6.0 kg ball's velocity.", "c) +3.25 is the stick-together answer.", "d) +4.0 assumes the balls swap velocities."],
    fig=figs.two_balls(r"$6.0$ kg, $+4.0$ m/s", r"$2.0$ kg, $+1.0$ m/s", right_v="right", r1=0.45, r2=0.28), figsize=(3.6, 1.1)))

# 11 -- Ch 11 notes p.5/8 rod dropped from center to edge
I11 = 0.5 * 300 * 2.5 ** 2
w11 = I11 * 1.6 / (I11 + 50 * 2.5 ** 2 / 3)
Q.append(dict(
    stem=r"A merry-go-round (a disk, $I = \tfrac12 MR^2$, $M = 300$ kg, $R = 2.5$ m) rotates at 1.6 rad/s. A 50 kg rod, 2.5 m long, is dropped onto it so that it lies from the center to the edge. What is the new angular velocity?",
    choices=["1.20 rad/s", "1.37 rad/s", "1.44 rad/s", "1.56 rad/s", "1.60 rad/s"], key="c",
    check=("near", w11, [1.20, 1.37, 1.44, 1.56, 1.60], 0.005),
    value="1.44 rad/s", topic="Rod dropped from the center to the edge", source="Ch 11 notes p. 5/8", card="Angular momentum ($I_{add}$: rod)",
    solution=r"""
Notecard with $I_{add}$ = rod center$\to$edge $= \tfrac13 m\ell^2$:

$$\omega_f = \frac{I_1\omega_1}{I_1 + \tfrac13 m\ell^2}$$

**Moments of inertia:** $I_1 = \tfrac12(300)(2.5)^2 = 937.5$; $\tfrac13(50)(2.5)^2 = 104.2$ (kg·m²).

**Plug in:**

$$\omega_f = \frac{(937.5)(1.6)}{937.5 + 104.2} = \frac{1500}{1041.7} = 1.44\ \text{rad/s}$$
""",
    distract=["a) 1.20 treats the rod as a point mass at the rim ($m\\ell^2$).", "b) 1.37 uses $\\tfrac12 m\\ell^2$.",
              "d) 1.56 uses the rod-about-its-middle formula, $\\tfrac1{12}m\\ell^2$.", "e) 1.60 ignores the rod."],
    fig=figs.mgr_rod(), figsize=(2.8, 2.6)))

# 12 -- Ch 9 notes p.5/5 ballistic pendulum, bullet speed
V12 = sqrt(2 * g * 0.080)
v12 = (2.0 + 0.006) / 0.006 * V12
Q.append(dict(
    stem=r"A 0.006 kg bullet is fired into a 2.0 kg block hanging from light strings. The bullet lodges in the block, and the block swings up 0.080 m. What was the bullet's speed?",
    choices=["1.25 m/s", "22.9 m/s", "334 m/s", "419 m/s", "837 m/s"], key="d",
    check=("near", v12, [1.25, 22.9, 334, 419, 837], 0.6),
    value="419 m/s", topic="Ballistic pendulum, bullet speed", source="Ch 9 notes p. 5/5", card="Ballistic",
    solution=r"""
Notecard:

$$v = \frac{M + m}{m}\sqrt{2gh}$$

**Plug in:**

$$v = \frac{2.006}{0.006}\sqrt{2(9.8)(0.080)} = 334.3 \times 1.252 = 419\ \text{m/s}$$
""",
    distract=["a) 1.25 is $V = \\sqrt{2gh}$, the block's speed after the hit.", "b) 22.9 uses energy conservation through the collision.",
              "c) 334 is just the mass ratio.", "e) 837 doubles it."],
    fig=figs.ballistic(), figsize=(3.4, 2.1)))

# 13 -- Ch 10 notes p.4-6/8 hanging mass on a disk pulley, moving down at v_i
v13 = sqrt(1.0 ** 2 + 2 * 2.0 * g * 1.5 / (2.0 + 3.0))
Q.append(dict(
    stem=r"A 2.0 kg mass hangs from a light string wrapped around a pulley that is a uniform disk ($I = \tfrac12 MR^2$, $M = 6.0$ kg, $R = 0.40$ m). The mass is moving **down** at 1.0 m/s. How fast is it moving after it has dropped another 1.5 m?",
    choices=["2.62 m/s", "2.89 m/s", "3.43 m/s", "3.57 m/s", "5.51 m/s"], key="d",
    check=("near", v13, [2.62, 2.89, 3.43, 3.57, 5.51], 0.005),
    value="3.57 m/s", topic="Hanging mass on a disk pulley", source="Ch 10 notes p. 4/8–6/8", card="Atwood / mass on pulley (one mass)",
    solution=r"""
Notecard, one mass: $v_f^2 = v_i^2 + \dfrac{2mgh}{m + I/R^2}$. A disk has $I/R^2 = \tfrac12 M = 3.0$ kg.

$$v_f = \sqrt{v_i^2 + \frac{2mgh}{m + \tfrac12 M}}$$

**Plug in:**

$$v_f = \sqrt{1.0^2 + \frac{2(2.0)(9.8)(1.5)}{2.0 + 3.0}} = \sqrt{1.0 + 11.76} = \sqrt{12.76} = 3.57\ \text{m/s}$$
""",
    distract=["a) 2.62 forgets the 2.", "b) 2.89 treats the pulley as a ring ($I/R^2 = M$).", "c) 3.43 forgets $v_i^2$.", "e) 5.51 ignores the pulley (free fall)."],
    fig=figs.pulley_one(r"disk, $M = 6.0$ kg", r"$v_i = 1.0$ m/s"), figsize=(2.6, 2.2)))

# 14 -- Ch 10 notes p.7/8 disk rolls down from height h
v14 = sqrt(4 / 3 * g * 1.8)
Q.append(dict(
    stem=r"A solid disk ($I = \tfrac12 MR^2$) starts from rest and rolls without slipping down an incline from a height of 1.8 m. How fast is its center moving at the bottom?",
    choices=["3.43 m/s", "4.20 m/s", "4.85 m/s", "5.02 m/s", "5.94 m/s"], key="c",
    check=("near", v14, [3.43, 4.20, 4.85, 5.02, 5.94], 0.005),
    value="4.85 m/s", topic="Disk rolling down an incline", source="Ch 10 notes p. 7/8–8/8", card="Rolling (disk row)",
    solution=r"""
Notecard, disk row: $v = \sqrt{\tfrac43 gh}$.

**Plug in:**

$$v = \sqrt{\tfrac43(9.8)(1.8)} = \sqrt{23.52} = 4.85\ \text{m/s}$$
""",
    distract=["a) 3.43 uses $\\tfrac23$ instead of $\\tfrac43$.", "b) 4.20 is a ring, $\\sqrt{gh}$.", "d) 5.02 is a sphere, $\\sqrt{\\tfrac{10}{7}gh}$.", "e) 5.94 is sliding, $\\sqrt{2gh}$."],
    fig=figs.rolling(r"", r"$v = ?$", r"$1.8$ m"), figsize=(3.6, 1.6)))

# 15 -- Ch 11 notes p.1/8 disk dropped on a spinning disk
I15a, I15b = 0.5 * 400 * 2.0 ** 2, 0.5 * 150 * 1.2 ** 2
w15 = I15a * 2.5 / (I15a + I15b)
Q.append(dict(
    stem=r"A disk ($I_1 = \tfrac12 MR^2$, $M = 400$ kg, $R = 2.0$ m) rotates at 2.5 rad/s. A second disk ($I_2 = \tfrac12 mr^2$, $m = 150$ kg, $r = 1.2$ m) that is **not** rotating drops onto it; it bounces, chatters, and the two stick. What is their final angular velocity?",
    choices=["2.20 rad/s", "2.50 rad/s", "2.84 rad/s", "4.40 rad/s", "5.00 rad/s"], key="a",
    check=("near", w15, [2.20, 2.50, 2.84, 4.40, 5.00], 0.005),
    value="2.20 rad/s", topic="Disk dropped on a spinning disk", source="Ch 11 notes p. 1/8", card="Angular momentum",
    solution=r"""
Notecard with $\omega_2 = 0$:

$$\omega_f = \frac{I_1\omega_1}{I_1 + I_2}$$

**Moments of inertia:** $I_1 = \tfrac12(400)(2.0)^2 = 800$; $I_2 = \tfrac12(150)(1.2)^2 = 108$ (kg·m²).

**Plug in:**

$$\omega_f = \frac{(800)(2.5)}{800 + 108} = \frac{2000}{908} = 2.20\ \text{rad/s}$$
""",
    distract=["b) 2.50 is no change.", "c) 2.84 flips the ratio.", "d) 4.40 doubles it.", "e) 5.00 doubles the starting speed."],
    fig=figs.stacked_disks(r"$2.5$ rad/s", r"$\omega = 0$", top_sign=None), figsize=(3.4, 1.9)))

INTRO = r"""
Practice Exam 2-8 is built from the professor's **lecture-note examples**, one per question, with new numbers. It keeps his setups and his unknowns: the halfpipe after the rain, the roller coaster, the four incline cases, the spring at the bottom of a ramp, the man on the stairs, the block that "doesn't go" up the incline, loop launch height, the 3×5-notecard elastic collision, the rod on the merry-go-round, the ballistic pendulum, the pulley "Atwood's machine w/ torque," the rolling disk, and the disk dropped on a disk. Question 9 is a **minimum** trap: round up. The last column says which 3×5 notecard entry solves each question.
"""

if __name__ == "__main__":
    build(8, "Chapters 6, 7/8, 9, 10, 11", Q, INTRO)
