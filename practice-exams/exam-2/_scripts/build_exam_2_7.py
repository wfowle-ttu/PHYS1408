"""Practice Exam 2-7: the 2015 Exam 2, question by question, with new numbers,
plus two lecture-note examples (Atwood's machine, alpha from an angle).

Run:  PYTHONIOENCODING=utf-8 python practice-exams/exam-2/_scripts/build_exam_2_7.py
"""
from math import cos, radians, sin, sqrt

import figs
from examlib import build

g = 9.8
Q = []

# 1 -- 2015 #1 halfpipe with a friction patch
h1 = 5.0 - 0.15 * 4.0
Q.append(dict(
    stem=r"A skateboarder rides down the wall of a halfpipe from an initial height of 5.0 m, starting from rest. The halfpipe is frictionless except for a region 4.0 m long on the bottom with a coefficient of friction $\mu = 0.15$. How high up the far side of the halfpipe does he rise before he comes to rest?",
    choices=["4.7 m", "4.6 m", "4.5 m", "4.4 m", "4.3 m"], key="d",
    check=("near", h1, [4.7, 4.6, 4.5, 4.4, 4.3], 0.02),
    value="4.4 m", topic="Halfpipe with a friction patch", source="2015 Exam 2 #1; Ch 7/8 notes p. 4/18–5/18", card="Halfpipe",
    solution=r"""
Notecard, starting from rest with one crossing ($v_i = 0$, $n = 1$):

$$h_f = h_i - \mu L$$

**Plug in:**

$$h_f = 5.0 - (0.15)(4.0) = 5.0 - 0.60 = 4.4\ \text{m}$$
""",
    distract=[r"a)–c) and e) are 0.1 m steps around the answer, like the 2015 exam's choices. Only $h_i - \mu L$ gives 4.4."],
    fig=figs.halfpipe(r"$h_i = 5.0$ m", r"$L = 4.0$ m, $\mu = 0.15$", r"$h_f = ?$"), figsize=(4.2, 2.0)))

# 2 -- 2015 #2 projectile max height from a ledge
s40 = sin(radians(40))
H2 = 4.0 + (22 * s40) ** 2 / (2 * g)
Q.append(dict(
    stem=r"A mass is fired from a height of 4.0 m above the flat ground below at 22 m/s at an angle of $40^\circ$ above the horizontal. How high above the ground below does the mass fly at the highest point in its trajectory?",
    choices=["4.0 m", "10.2 m", "14.2 m", "18.5 m", "28.7 m"], key="c",
    check=("near", H2, [4.0, 10.2, 14.2, 18.5, 28.7], 0.05),
    value="14.2 m", topic="Projectile max height from a ledge", source="2015 Exam 2 #2", card="Projectile",
    solution=r"""
Notecard:

$$H = h_0 + \frac{(v_0\sin\theta)^2}{2g}$$

**Plug in** ($v_0\sin\theta = 22\sin 40^\circ = 14.14$ m/s):

$$H = 4.0 + \frac{(14.14)^2}{2(9.8)} = 4.0 + \frac{200}{19.6} = 4.0 + 10.2 = 14.2\ \text{m}$$
""",
    distract=["a) 4.0 is just the ledge.", "b) 10.2 forgets to add the ledge.", "d) 18.5 uses $\\cos\\theta$.", "e) 28.7 uses all of $v_0$ (as if thrown straight up)."],
    fig=figs.ledge_projectile(r"$4.0$ m", r"$22$ m/s", r"$40^\circ$"), figsize=(3.8, 1.9)))

# 3 -- 2015 #3 loop minimum speed at the bottom (min trap)
v3 = sqrt(5 * g * 12)
Q.append(dict(
    stem=r"In order to go all the way around a circular loop of radius $R = 12$ m, how fast must a mass be moving as it enters the bottom of the loop?",
    choices=["11 m/s", "19 m/s", "22 m/s", "24 m/s", "26 m/s"], key="e",
    check=("min", v3, [11, 19, 22, 24, 26]),
    value="24.2 m/s → 26", topic="Loop-the-loop, minimum speed at the bottom", source="2015 Exam 2 #3; Ch 7/8 notes p. 12/18–13/18", card="Loop",
    solution=r"""
Notecard: bottom minimum $v_b = \sqrt{5gR}$.

**Plug in:**

$$v_b = \sqrt{5(9.8)(12)} = \sqrt{588} = 24.2\ \text{m/s}$$

**Answer-choice trap.** 24.2 m/s is a **minimum**. At 24 m/s the mass falls off the loop, even though 24 is the closest number. The smallest choice that works is **e) 26 m/s**.
""",
    distract=["a) 11 is $\\sqrt{gR}$, the minimum at the **top**.", "b) 19 is $\\sqrt{3gR}$.",
              "c) 22 is $\\sqrt{4gR}$: just enough to reach the top with zero speed.", "d) 24 is the nearest number, but it's below the minimum."],
    fig=figs.loop(), figsize=(3.0, 1.9)))

# 4 -- 2015 #4 sliding up a rough ramp, time to stop
s8, c8 = sin(radians(8)), cos(radians(8))
dx4 = 6.0 ** 2 / (2 * g * (s8 + 0.50 * c8))
t4 = 2 * dx4 / 6.0
Q.append(dict(
    stem=r"A mass of 4.0 kg is sliding up a ramp ($\mu = 0.50$ and $\theta = 8^\circ$), initially sliding at 6.0 m/s. How long does it continue to slide along the ramp before it comes to rest?",
    choices=["0.97 s", "1.72 s", "1.93 s", "2.90 s", "4.40 s"], key="a",
    check=("near", t4, [0.97, 1.72, 1.93, 2.90, 4.40], 0.005),
    value="0.97 s", topic="Sliding up a rough ramp, time to stop", source="2015 Exam 2 #4", card="One block on incline (Stop up, Time)",
    solution=r"""
**Step 1: Stopping distance** (notecard, stop up):

$$\Delta x = \frac{v_i^2}{2g(\sin\theta + \mu\cos\theta)} = \frac{6.0^2}{2(9.8)(0.1392 + 0.50 \times 0.9903)} = \frac{36}{19.6(0.6343)} = 2.90\ \text{m}$$

**Step 2: Time** (notecard, $v_f = 0$):

$$t = \frac{2\,\Delta x}{v_i + v_f} = \frac{2(2.90)}{6.0 + 0} = 0.97\ \text{s}$$

The 4.0 kg mass cancels.
""",
    distract=["b) 1.72 uses the sliding-**down** bracket, $(\\mu\\cos\\theta - \\sin\\theta)$.", "c) 1.93 has an extra factor of 2.",
              "d) 2.90 is the stopping **distance** in meters, not the time.", "e) 4.40 ignores friction."],
    fig=figs.slope_block(8, "up", r"$v_i = 6.0$ m/s", r"$\mu = 0.50$"), figsize=(3.8, 1.2)))

# 5 -- 2015 #5 vertical spring launch
h5 = 1500 * 0.030 ** 2 / (2 * 0.040 * g)
Q.append(dict(
    stem=r"A 0.040 kg mass is placed on a vertical spring of spring constant $k = 1500$ N/m. The spring is compressed 0.030 m from its equilibrium length. When the mass on the compressed spring is released, it shoots the mass straight up. How far does the mass fly above the release point?",
    choices=["0.17 m", "0.86 m", "1.7 m", "3.4 m", "17 m"], key="c",
    check=("near", h5, [0.17, 0.86, 1.7, 3.4, 17], 0.03),
    value="1.7 m", topic="Vertical spring launch", source="2015 Exam 2 #5; Ch 7/8 notes p. 12/18", card="Spring (launch up)",
    solution=r"""
Notecard, launch up (measured from the release point):

$$h = \frac{kx^2}{2mg}$$

**Plug in:**

$$h = \frac{(1500)(0.030)^2}{2(0.040)(9.8)} = \frac{1.35}{0.784} = 1.7\ \text{m}$$
""",
    distract=["a) 0.17 slips a decimal.", "b) 0.86 has an extra factor of 2 in the denominator.",
              "d) 3.4 forgets the $\\tfrac12$ on the spring PE.", "e) 17 slips a decimal the other way."],
    fig=figs.vertical_spring(r"$h = ?$", r"$k$, compressed $x$"), figsize=(2.2, 2.2)))

# 6 -- 2015 #6 elastic head-on, velocity of the heavier ball
v6_1 = ((2 - 3) * 4 + 2 * 3 * (-3)) / 5
v6_2 = 4 + v6_1 - (-3)
Q.append(dict(
    stem=r"A 2.0 kg mass moving to the right at 4.0 m/s collides **elastically** in a head-on collision with a 3.0 kg mass moving at 3.0 m/s to the left. How fast and in what direction is the 3.0 kg mass moving after the collision? Positive to the right / negative to the left.",
    choices=["+4.4 m/s", "+2.6 m/s", "−0.2 m/s", "−2.6 m/s", "−4.4 m/s"], key="b",
    check=("near", v6_2, [4.4, 2.6, -0.2, -2.6, -4.4], 0.05),
    value="+2.6 m/s", topic="1-D elastic collision", source="2015 Exam 2 #6; Ch 9 notes p. 3/5", card="Elastic",
    solution=r"""
Notecard formulas, right $= +$: $m_1 = 2.0$, $v_{1i} = +4.0$; $m_2 = 3.0$, $v_{2i} = -3.0$.

$$v_{1f} = \frac{(m_1 - m_2)v_{1i} + 2m_2v_{2i}}{m_1 + m_2} = \frac{(-1.0)(4.0) + 2(3.0)(-3.0)}{5.0} = \frac{-4 - 18}{5} = -4.4\ \text{m/s}$$

$$v_{2f} = v_{1i} + v_{1f} - v_{2i} = 4.0 + (-4.4) - (-3.0) = +2.6\ \text{m/s}$$
""",
    distract=["a) +4.4 is the size of the 2.0 kg mass's velocity.", "c) −0.2 is the stick-together answer.",
              "d) −2.6 has the sign wrong.", "e) −4.4 is the 2.0 kg mass's velocity."],
    fig=figs.two_balls(r"$2.0$ kg, $+4.0$ m/s", r"$3.0$ kg, $-3.0$ m/s", right_v="left", r1=0.3, r2=0.4), figsize=(3.6, 1.1)))

# 7 -- 2015 #7 inelastic KE fraction, symbolic
vf7 = (3 * 2 + 1 * 1) / 4
frac7 = 4 * vf7 ** 2 / (3 * 2 ** 2 + 1 * 1 ** 2)
Q.append(dict(
    stem=r"A railroad car of mass $3m$ and velocity $2v$ collides completely **inelastically** with another railroad car of mass $m$ and velocity $v$ (same direction). The two cars collide and couple together. What fraction of the initial kinetic energy is still retained by the cars after the collision?",
    choices=["<1%", "2–5%", "10–20%", "30–50%", ">90%"], key="e",
    check=("concept",),
    value="94%", topic="Inelastic collision, KE fraction (symbolic)", source="2015 Exam 2 #7; Ch 9 notes p. 1/5", card="Stick (inelastic)",
    solution=r"""
Symbolic, so **set $m = 1$ and $v = 1$**: $m_1 = 3$, $v_1 = 2$; $m_2 = 1$, $v_2 = 1$.

**Shared velocity** (notecard):

$$v_f = \frac{m_1v_1 + m_2v_2}{m_1 + m_2} = \frac{3(2) + 1(1)}{4} = 1.75$$

**KE fraction** (notecard):

$$\frac{K_f}{K_i} = \frac{(m_1 + m_2)v_f^2}{m_1v_1^2 + m_2v_2^2} = \frac{4(1.75)^2}{3(2)^2 + 1(1)^2} = \frac{12.25}{13} = 0.94$$

94% is retained: **>90%**. (When both cars move the same way at similar speeds, little KE is lost.)
""",
    distract=["d) 30–50% would need a big speed difference.", "a) <1% is the ballistic-pendulum size of loss."],
    fig=figs.carts(r"$3m$", r"$m$", r"$2v$", r"$v$", rv_dir="right"), figsize=(4.0, 0.9)))
assert frac7 > 0.90

# 8 -- 2015 #8 ballistic pendulum, KE fraction
frac8 = 100 * 0.008 / (6.0 + 0.008)
assert 0.1 < frac8 < 0.5
Q.append(dict(
    stem=r"A bullet (mass 0.008 kg) is fired into a suspended block of wood (6.0 kg). Initially the wood is not moving. The bullet lodges in the wood. Recoil of the wood causes it to swing (rising 0.02 m). What fraction of the initial kinetic energy remained in the motion of the block of wood?",
    choices=["<0.1%", "0.1–0.5%", "0.5–1%", "1–10%", ">10%"], key="b",
    check=("concept",),
    value="0.13%", topic="Ballistic pendulum, KE fraction", source="2015 Exam 2 #8; Ch 9 notes p. 5/5", card="Ballistic",
    solution=r"""
Notecard: $\dfrac{K_f}{K_i} = \dfrac{m}{M + m}$. The swing height isn't needed.

$$\frac{K_f}{K_i} = \frac{0.008}{6.0 + 0.008} = 0.0013 = 0.13\%$$

That's in the **0.1–0.5%** range.
""",
    distract=["a) <0.1% would need a block heavier than 8 kg.", "e) >10% would mean the collision kept a lot of KE, which a sticking bullet never does."],
    fig=figs.ballistic(r"$m_b$", r"$h$"), figsize=(3.4, 2.1)))

# 9 -- 2015 #9 hanging mass on a pulley, I = 3/5 MR^2
a9 = 1.5 * g / (1.5 + 0.6 * 8.0)
Q.append(dict(
    stem=r"A mass of 1.5 kg hangs from a pulley ($I = \tfrac35 MR^2$, $M = 8.0$ kg, $R = 0.20$ m) as shown. What is the downward linear acceleration of the hanging mass?",
    choices=["0.83 m/s²", "1.33 m/s²", "1.83 m/s²", "2.33 m/s²", "2.83 m/s²"], key="d",
    check=("near", a9, [0.83, 1.33, 1.83, 2.33, 2.83], 0.01),
    value="2.33 m/s²", topic="Hanging mass on a pulley with $I$", source="2015 Exam 2 #9; Ch 10 notes p. 4/8", card="Atwood / mass on pulley (one mass)",
    solution=r"""
Notecard, one mass: $a = \dfrac{mg}{m + I/R^2}$. Here $I = \tfrac35 MR^2$, so $I/R^2 = \tfrac35 M = 4.8$ kg ($R$ cancels).

$$a = \frac{mg}{m + \tfrac35 M}$$

**Plug in:**

$$a = \frac{(1.5)(9.8)}{1.5 + 4.8} = \frac{14.7}{6.3} = 2.33\ \text{m/s}^2$$
""",
    distract=["The other choices are 0.5 m/s² steps around the answer, like the 2015 exam's. $R = 0.20$ m is a distractor: it cancels."],
    fig=figs.pulley_one(r"$I=\frac{3}{5}MR^2$"), figsize=(2.6, 2.2)))

# 10 -- 2015 #10 sphere rolls down, find omega
v10 = sqrt(10 / 7 * g * 1.5)
w10 = v10 / 0.020
Q.append(dict(
    stem=r"A sphere ($M = 3.0$ kg, $R = 0.020$ m, $I = \tfrac25 MR^2$) rolls down an incline from a height of 1.5 m, starting from rest. At the bottom of the incline, what is the sphere's rotational velocity $\omega$?",
    choices=["4.6 rad/s", "229 rad/s", "458 rad/s", "2290 rad/s", "52,500 rad/s"], key="b",
    check=("near", w10, [4.6, 229, 458, 2290, 52500], 1),
    value="229 rad/s", topic="Rolling sphere, find $\\omega$", source="2015 Exam 2 #10; Ch 10 notes p. 6/8–8/8", card="Rolling (sphere row)",
    solution=r"""
Notecard, sphere: $v = \sqrt{\tfrac{10}{7}gh}$, then $\omega = \dfrac{v}{R}$.

$$v = \sqrt{\tfrac{10}{7}(9.8)(1.5)} = \sqrt{21} = 4.58\ \text{m/s}$$

$$\omega = \frac{v}{R} = \frac{4.58}{0.020} = 229\ \text{rad/s}$$
""",
    distract=["a) 4.6 is $v$ (m/s), not $\\omega$.", "c) 458 divides by $R/2$.", "d) 2290 slips a decimal in $R$.", "e) 52,500 is $\\omega^2$."],
    fig=figs.rolling(r"", r"$\omega = ?$", r"$h$"), figsize=(3.6, 1.6)))

# 11 -- 2015 #11 counter-rotating wheel dropped on a disk
I11a, I11b = 0.5 * 150 * 2.0 ** 2, 0.8 * 50 * 1.5 ** 2
w11 = (I11a * 3.0 + I11b * (-2.0)) / (I11a + I11b)
Q.append(dict(
    stem=r"A disk ($I = \tfrac12 MR^2$, mass 150 kg, radius 2.0 m) rotates at 3.0 rad/s. A wheel ($I = 0.8MR^2$, mass 50 kg, radius 1.5 m, initially rotating in the opposite direction at −2.0 rad/s) is dropped onto the disk. Their collision is completely inelastic. After they stop bouncing, what is the angular velocity (rad/s) of the two-object stack?",
    choices=["−0.5 rad/s", "0 rad/s", "+1 rad/s", "+1.5 rad/s", "+2 rad/s"], key="e",
    check=("near", w11, [-0.5, 0, 1, 1.5, 2], 0.2),
    value="1.85 rad/s → +2", topic="Counter-rotating wheel dropped on a disk", source="2015 Exam 2 #11; Ch 11 notes p. 3/8", card="Angular momentum",
    solution=r"""
Notecard, with the wheel's $\omega_2$ **negative**:

$$\omega_f = \frac{I_1\omega_1 + I_2\omega_2}{I_1 + I_2}$$

**Moments of inertia first:**

$$I_1 = \tfrac12(150)(2.0)^2 = 300\ \text{kg·m}^2$$

$$I_2 = 0.8(50)(1.5)^2 = 90\ \text{kg·m}^2$$

**Plug in:**

$$\omega_f = \frac{(300)(3.0) + (90)(-2.0)}{300 + 90} = \frac{900 - 180}{390} = 1.85\ \text{rad/s}$$

The nearest choice is **e) +2 rad/s**, the same as on the 2015 exam.
""",
    distract=["d) +1.5 is the other neighbor, but 1.85 is closer to 2.", "a) and b) come from adding the wheel's $I$ without its spin, or flipping signs."],
    fig=figs.stacked_disks(r"$+3.0$", r"wheel $-2.0$"), figsize=(3.4, 1.9)))

# 12 -- 2015 #12 child jumps onto the merry-go-round rim
I12 = 0.5 * 400 * 2.5 ** 2
w12 = (I12 * 0.60 + 45 * 6.0 * 2.5) / (I12 + 45 * 2.5 ** 2)
Q.append(dict(
    stem=r"A merry-go-round (a disk $I = \tfrac12 MR^2$, $M = 400$ kg, $R = 2.5$ m) rotates at +0.60 rad/s. A child with a mass of 45 kg jumps onto the merry-go-round (going the same direction) at the rim. The child was running at 6.0 m/s as she jumps on. What is the new rotation rate for the merry-go-round WITH the child?",
    choices=["0.3 rad/s", "0.5 rad/s", "0.7 rad/s", "0.9 rad/s", "1.1 rad/s"], key="d",
    check=("near", w12, [0.3, 0.5, 0.7, 0.9, 1.1], 0.05),
    value="0.93 rad/s", topic="Child jumps onto a merry-go-round", source="2015 Exam 2 #12; Ch 11 notes p. 4/8", card="Angular momentum",
    solution=r"""
Notecard with $+mvR$ (same direction) and $I_{add} = mR^2$ (person at the rim):

$$\omega_f = \frac{\tfrac12 MR^2\,\omega_i + mvR}{\tfrac12 MR^2 + mR^2}$$

**Plug in** ($\tfrac12 MR^2 = \tfrac12(400)(2.5)^2 = 1250$ kg·m²):

$$
\begin{aligned}
\omega_f &= \frac{(1250)(0.60) + (45)(6.0)(2.5)}{1250 + (45)(2.5)^2} \\[8pt]
&= \frac{750 + 675}{1250 + 281} = \frac{1425}{1531} = 0.93\ \text{rad/s}
\end{aligned}
$$

The nearest choice is **d) 0.9 rad/s**.
""",
    distract=["b) 0.5 ignores the child's running momentum (0.49).", "e) 1.1 forgets to add the child's $mR^2$ (1.14)."],
    fig=figs.mgr_runner(r"$6.0$ m/s"), figsize=(3.2, 2.0)))

# 13 -- 2015 #13 block down an incline, disk pulley
s25, c25 = sin(radians(25)), cos(radians(25))
B13 = 6.0 * s25 - 0.12 * 6.0 * c25
v13 = sqrt(0.50 ** 2 + 2 * g * 0.80 * B13 / (6.0 + 0.5 * 3.0))
Q.append(dict(
    stem=r"A mass of 6.0 kg slides down a $25^\circ$ inclined surface (with $\mu = 0.12$) at 0.50 m/s. It is connected to a pulley (as shown). The pulley is a disk with mass 3.0 kg, radius 0.06 m, and moment of inertia $0.5MR^2$. How fast is the mass sliding when it has slid 0.80 m down along the incline?",
    choices=["2.05 m/s", "1.98 m/s", "1.88 m/s", "1.49 m/s", "it stops before it slides the whole 0.80 m"], key="a",
    check=("near", v13, [2.05, 1.98, 1.88, 1.49, None], 0.005),
    value="2.05 m/s", topic="Incline + friction + disk pulley", source="2015 Exam 2 #13", card="Incline + hanging mass + pulley ($m_2 = 0$)",
    solution=r"""
Notecard with no hanging mass ($m_2 = 0$), block sliding **down**:

$$v_f = \sqrt{v_i^2 + \frac{2g\,\Delta x\,B}{m + I/R^2}}$$

$$B = m\sin\theta - \mu m\cos\theta$$

**Net pull** ($\sin 25^\circ = 0.4226$, $\cos 25^\circ = 0.9063$):

$$B = 6.0(0.4226) - 0.12(6.0)(0.9063) = 2.536 - 0.653 = 1.883\ \text{kg}$$

**Pulley term:** $I = 0.5MR^2$, so $I/R^2 = 0.5M = 1.5$ kg.

**Plug in:**

$$
\begin{aligned}
v_f &= \sqrt{0.50^2 + \frac{2(9.8)(0.80)(1.883)}{6.0 + 1.5}} \\[8pt]
&= \sqrt{0.25 + \frac{29.53}{7.5}} = \sqrt{0.25 + 3.94} = 2.05\ \text{m/s}
\end{aligned}
$$
""",
    distract=["b) 1.98 forgets $v_i^2$.", "c) 1.88 treats the pulley as a ring ($I/R^2 = M$).",
              "d) 1.49 forgets the 2 in $2g$.", "e) $B > 0$, so it speeds up and never stops."],
    fig=figs.incline_disk_pulley(r"$25^\circ$", r"$\mu = 0.12$", r"$0.50$ m/s"), figsize=(3.6, 2.2)))

# 14 -- notes: Atwood's machine (massless pulley)
v14 = sqrt(2 * g * 1.5 * (12 - 8) / (12 + 8))
Q.append(dict(
    stem=r"In an Atwood's machine, $m_1 = 12$ kg and $m_2 = 8.0$ kg hang from a light string over a massless, frictionless pulley. They are released from rest. How fast is $m_1$ moving after it has fallen 1.5 m?",
    choices=["2.42 m/s", "3.13 m/s", "3.83 m/s", "4.85 m/s", "5.42 m/s"], key="a",
    check=("near", v14, [2.42, 3.13, 3.83, 4.85, 5.42], 0.005),
    value="2.42 m/s", topic="Atwood's machine", source="Ch 7/8 notes p. 2/18", card="Atwood / mass on pulley",
    solution=r"""
Notecard, massless pulley ($I = 0$), from rest:

$$v_f = \sqrt{\frac{2gh(m_1 - m_2)}{m_1 + m_2}}$$

**Plug in:**

$$v_f = \sqrt{\frac{2(9.8)(1.5)(12 - 8.0)}{12 + 8.0}} = \sqrt{\frac{117.6}{20}} = \sqrt{5.88} = 2.42\ \text{m/s}$$
""",
    distract=["b) 3.13 divides by $m_1$ only.", "c) 3.83 divides by $m_2$ only.", "d) 4.85 doubles the answer.", "e) 5.42 is free fall, $\\sqrt{2gh}$."],
    fig=figs.atwood(r"$m_1$", r"$m_2$"), figsize=(2.4, 2.5)))

# 15 -- notes: alpha from omega_i, omega_f and an angle
a15 = (60 ** 2 - 20 ** 2) / (2 * 100)
Q.append(dict(
    stem=r"A wheel speeds up uniformly from 20 rad/s to 60 rad/s while turning through 100 rad. What is its angular acceleration?",
    choices=["0.40 rad/s²", "8.0 rad/s²", "16 rad/s²", "32 rad/s²", "36 rad/s²"], key="c",
    check=("near", a15, [0.40, 8.0, 16, 32, 36], 0.05),
    value="16 rad/s²", topic="Rotational kinematics, $\\alpha$ from an angle", source="Ch 11 notes p. 6/8", card="Rot. kinematics",
    solution=r"""
No time is given or asked for, so use the equation without $t$:

$$\omega_f^2 = \omega_i^2 + 2\alpha\,\Delta\theta$$

**Solve for $\alpha$:**

$$\alpha = \frac{\omega_f^2 - \omega_i^2}{2\,\Delta\theta}$$

**Plug in:**

$$\alpha = \frac{60^2 - 20^2}{2(100)} = \frac{3600 - 400}{200} = 16\ \text{rad/s}^2$$
""",
    distract=["a) 0.40 is $\\Delta\\omega/\\Delta\\theta$.", "b) 8.0 squares the difference: $(\\omega_f - \\omega_i)^2/2\\Delta\\theta$.",
              "d) 32 forgets the 2.", "e) 36 drops $\\omega_i$ and the 2."],
    fig=figs.wheel(r"$20 \to 60$ rad/s over $100$ rad"), figsize=(2.6, 2.4)))

INTRO = r"""
Practice Exam 2-7 is the **2015 Exam 2, question by question, with new numbers**. It keeps the same wording, the same unknowns and the same style of answer choices, including his evenly spaced choices on #1, #9 and #12 and the percentage ranges on #7 and #8. Questions 14 and 15 are lecture-note examples (Atwood's machine; $\alpha$ from an angle). Question 3 is a **minimum** trap: round up. The last column says which 3×5 notecard entry solves each question.
"""

if __name__ == "__main__":
    build(7, "Chapters 6, 7/8, 9, 10, 11", Q, INTRO)
