"""Practice Exam 2-9: lecture-note examples and 2015 Exam 2 questions with new
numbers (no banked curves).

Run:  PYTHONIOENCODING=utf-8 python practice-exams/exam-2/_scripts/build_exam_2_9.py
"""
from math import cos, radians, sin, sqrt

import figs
from examlib import build

g = 9.8
Q = []

# 1 -- Ch 6 notes p.2/7 flat curve v_max (max trap)
v1 = sqrt(0.35 * g * 55)
Q.append(dict(
    stem=r"A car goes around a flat curve of radius 55 m. The coefficient of static friction between the tires and the road is $\mu_s = 0.35$. What is the maximum speed at which the car can take the curve?",
    choices=["4.4 m/s", "9.7 m/s", "13 m/s", "14 m/s", "23 m/s"], key="c",
    check=("max", v1, [4.4, 9.7, 13, 14, 23]),
    value="13.7 m/s → 13", topic="Flat curve, maximum speed", source="Ch 6 notes p. 2/7", card="Curve (flat)",
    solution=r"""
Notecard, flat curve:

$$v_{max} = \sqrt{\mu_s gr}$$

**Plug in:**

$$v_{max} = \sqrt{(0.35)(9.8)(55)} = \sqrt{188.7} = 13.7\ \text{m/s}$$

**Answer-choice trap.** 13.7 m/s is a **maximum**. At 14 m/s the car slides, even though 14 is the closest number. The largest choice that works is **c) 13 m/s**.
""",
    distract=["a) 4.4 forgets $g$.", "b) 9.7 has an extra $\\tfrac12$ under the root.", "d) 14 is the nearest number, but it's above the maximum.", "e) 23 drops $\\mu_s$: $\\sqrt{gr}$."],
    fig=figs.flat_curve(r"$\mu_s = 0.35$", r"$55$ m"), figsize=(3.2, 1.7)))

# 2 -- Ch 7/8 notes p.13/18 normal force at the bottom, launched from 5R/2
N2 = 6 * 70 * g
Q.append(dict(
    stem=r"A 70 kg rider starts from rest at the minimum launch height ($h = \tfrac52 R$) needed to barely make it around a frictionless vertical loop. What normal force does the seat exert on the rider at the **bottom** of the loop?",
    choices=["686 N", "1370 N", "2740 N", "3430 N", "4120 N"], key="e",
    check=("near", N2, [686, 1370, 2740, 3430, 4120], 6),
    value="4120 N", topic="Loop, normal force at the bottom", source="Ch 7/8 notes p. 13/18", card="Loop",
    solution=r"""
From the minimum launch height, $v_b^2 = 2gh = 2g\left(\tfrac52R\right) = 5gR$. Notecard, bottom:

$$N_{bot} = \frac{mv_b^2}{R} + mg = \frac{m(5gR)}{R} + mg = 6mg$$

$R$ cancels. **Plug in:**

$$N_{bot} = 6(70)(9.8) = 4116 \approx 4120\ \text{N}$$

His notes call this "$N = 6mg$, death & unconsciousness."
""",
    distract=["a) 686 N is just $mg$.", "b) 1370 is $2mg$.", "c) 2740 is $4mg$.", "d) 3430 is $5mg$ (forgot to add $mg$)."],
    fig=figs.loop(left_label=r"$\frac{5}{2}R$", ramp=True, bottom_mark=r"$N=?$"), figsize=(3.6, 2.3)))

# 3 -- Ch 7/8 notes p.7-8/18 sliding up a rough incline
s25, c25 = sin(radians(25)), cos(radians(25))
v3 = sqrt(3.5 ** 2 - 2 * g * 0.80 * (s25 + 0.15 * c25))
Q.append(dict(
    stem=r"A 4.0 kg block slides up a $25^\circ$ incline at 3.5 m/s. The coefficient of kinetic friction is 0.15. When the block has slid 0.80 m, how fast is it still moving?",
    choices=["1.87 m/s", "2.37 m/s", "2.81 m/s", "4.58 m/s", "it stops before it slides the whole 0.80 m"], key="a",
    check=("near", v3, [1.87, 2.37, 2.81, 4.58, None], 0.005),
    value="1.87 m/s", topic="Sliding up a rough incline", source="Ch 7/8 notes p. 7/18–8/18", card="One block on incline (Up)",
    solution=r"""
Notecard, sliding up:

$$v_f = \sqrt{v_i^2 - 2g\,\Delta x(\sin\theta + \mu\cos\theta)}$$

**Plug in** ($\sin 25^\circ = 0.4226$, $\cos 25^\circ = 0.9063$):

$$v_f = \sqrt{3.5^2 - 2(9.8)(0.80)(0.4226 + 0.15 \times 0.9063)} = \sqrt{12.25 - 8.76} = \sqrt{3.49} = 1.87\ \text{m/s}$$
""",
    distract=["b) 2.37 ignores friction.", "c) 2.81 forgets the 2.", "d) 4.58 adds instead of subtracts.", "e) $v_f^2 = 3.49 > 0$, so it makes it."],
    fig=figs.slope_block(25, "up", r"$v_i = 3.5$ m/s", r"$\mu_k = 0.15$"), figsize=(3.8, 1.8)))

# 4 -- Ch 7/8 notes p.10/18 sliding down a rough incline, speed
s20, c20 = sin(radians(20)), cos(radians(20))
v4 = sqrt(2.0 ** 2 + 2 * g * 2.5 * (s20 - 0.30 * c20))
Q.append(dict(
    stem=r"A block is sliding **down** a $20^\circ$ incline ($\mu_k = 0.30$) at 2.0 m/s. How fast is it moving after it has slid 2.5 m?",
    choices=["1.72 m/s", "2.00 m/s", "2.34 m/s", "2.46 m/s", "2.64 m/s"], key="e",
    check=("near", v4, [1.72, 2.00, 2.34, 2.46, 2.64], 0.005),
    value="2.64 m/s", topic="Sliding down a rough incline", source="Ch 7/8 notes p. 10/18", card="One block on incline (Down)",
    solution=r"""
Notecard, sliding down:

$$v_f = \sqrt{v_i^2 + 2g\,\Delta x(\sin\theta - \mu\cos\theta)}$$

**Plug in** ($\sin 20^\circ = 0.3420$, $\cos 20^\circ = 0.9397$):

$$v_f = \sqrt{2.0^2 + 2(9.8)(2.5)(0.3420 - 0.30 \times 0.9397)} = \sqrt{4.0 + 49(0.0601)} = \sqrt{6.94} = 2.64\ \text{m/s}$$

The bracket is positive (barely), so it speeds up a little.
""",
    distract=["a) 1.72 forgets $v_i^2$.", "b) 2.00 assumes no change.", "c) 2.34 forgets the 2.", "d) 2.46 uses friction $\\mu mg$ instead of $\\mu mg\\cos\\theta$."],
    fig=figs.slope_block(20, "down", r"$2.0$ m/s", r"$\mu_k = 0.30$"), figsize=(3.8, 1.5)))

# 5 -- Ch 7/8 notes p.17/18 block slides down, hanging mass rises
s35, c35 = sin(radians(35)), cos(radians(35))
B5 = 10 * s35 - 2.0 - 0.20 * 10 * c35
v5 = sqrt(1.5 ** 2 + 2 * g * 0.60 * B5 / 12)
Q.append(dict(
    stem=r"A 10 kg block on a $35^\circ$ incline ($\mu_k = 0.20$) is tied over a massless pulley at the top to a 2.0 kg hanging mass. The block slides **down** the incline at 1.5 m/s while the hanging mass rises. How fast is the block moving after it has slid 0.60 m?",
    choices=["1.43 m/s", "2.07 m/s", "2.17 m/s", "2.43 m/s", "it stops before it slides the whole 0.60 m"], key="b",
    check=("near", v5, [1.43, 2.07, 2.17, 2.43, None], 0.005),
    value="2.07 m/s", topic="Incline + hanging mass, block slides down", source="Ch 7/8 notes p. 17/18", card="Incline + hanging mass + pulley",
    solution=r"""
Notecard with $m_1$ sliding **down**, massless pulley:

$$v_f = \sqrt{v_i^2 + \frac{2g\,\Delta x\,B}{m_1 + m_2}}$$

$$B = m_1\sin\theta - m_2 - \mu m_1\cos\theta$$

**Net pull** ($\sin 35^\circ = 0.5736$, $\cos 35^\circ = 0.8192$):

$$B = 10(0.5736) - 2.0 - 0.20(10)(0.8192) = 5.736 - 2.0 - 1.638 = 2.098\ \text{kg}$$

**Plug in:**

$$v_f = \sqrt{1.5^2 + \frac{2(9.8)(0.60)(2.098)}{12}} = \sqrt{2.25 + 2.06} = \sqrt{4.31} = 2.07\ \text{m/s}$$

"It speeds up!"
""",
    distract=["a) 1.43 forgets $v_i^2$.", "c) 2.17 divides by $m_1$ only.", "d) 2.43 ignores friction.", "e) $B > 0$, so it speeds up."],
    fig=figs.incline_hanging(r"$35^\circ$", r"$\mu_k = 0.20$", r"$1.5$ m/s", m1_dir="down"), figsize=(4.0, 2.1)))

# 6 -- 2015 #5 vertical spring launch
h6 = 1800 * 0.025 ** 2 / (2 * 0.080 * g)
Q.append(dict(
    stem=r"A 0.080 kg mass is placed on a vertical spring of spring constant $k = 1800$ N/m. The spring is compressed 0.025 m from its equilibrium length. When the mass on the compressed spring is released, it shoots the mass straight up. How far does the mass fly above the release point?",
    choices=["0.36 m", "0.72 m", "1.43 m", "7.03 m", "28.7 m"], key="b",
    check=("near", h6, [0.36, 0.72, 1.43, 7.03, 28.7], 0.01),
    value="0.72 m", topic="Vertical spring launch", source="2015 Exam 2 #5", card="Spring (launch up)",
    solution=r"""
Notecard, launch up:

$$h = \frac{kx^2}{2mg}$$

**Plug in:**

$$h = \frac{(1800)(0.025)^2}{2(0.080)(9.8)} = \frac{1.125}{1.568} = 0.72\ \text{m}$$
""",
    distract=["a) 0.36 has an extra factor of 2.", "c) 1.43 forgets the $\\tfrac12$ on the spring PE.", "d) 7.03 forgets $g$.", "e) 28.7 forgets to square $x$."],
    fig=figs.vertical_spring(r"$h = ?$", r"$k$, compressed $x$"), figsize=(2.2, 2.2)))

# 7 -- Ch 9 notes p.1/5 ball bounces straight back
F7 = 2 * 0.060 * 40 / 0.0040
Q.append(dict(
    stem=r"A 0.060 kg tennis ball hits a wall head-on at 40 m/s and bounces straight back at 40 m/s. It is in contact with the wall for 0.0040 s. What is the magnitude of the average force on the ball?",
    choices=["0 N", "4.8 N", "600 N", "1200 N", "2400 N"], key="d",
    check=("near", F7, [0, 4.8, 600, 1200, 2400], 1),
    value="1200 N", topic="Force from a bounce", source="Ch 9 notes p. 1/5", card="Force from $\\Delta p$",
    solution=r"""
Notecard, bounce back at the same speed:

$$|F| = \frac{2mv}{t}$$

**Plug in:**

$$|F| = \frac{2(0.060)(40)}{0.0040} = \frac{4.8}{0.0040} = 1200\ \text{N}$$
""",
    distract=["a) 0 ignores the direction change.", "b) 4.8 is the change in momentum (N·s), not a force.", "c) 600 is a ball that just stops ($mv/t$).", "e) 2400 doubles it again."],
    fig=figs.wall_bounce(r"$40$ m/s in", r"$40$ m/s out"), figsize=(3.2, 1.6)))

# 8 -- Ch 9 notes p.1/5 completely inelastic, head-on
v8 = (900 * 20 + 1200 * (-10)) / 2100
Q.append(dict(
    stem=r"A 900 kg car moving east at 20 m/s collides head-on with a 1200 kg car moving west at 10 m/s. The cars stick together. What is their velocity just after the collision? (East is positive.)",
    choices=["+2.86 m/s", "+8.57 m/s", "+14.3 m/s", "+20.0 m/s", "+30.0 m/s"], key="a",
    check=("near", v8, [2.86, 8.57, 14.3, 20.0, 30.0], 0.01),
    value="+2.86 m/s", topic="Completely inelastic collision", source="Ch 9 notes p. 1/5", card="Stick (inelastic)",
    solution=r"""
Notecard, with west as **negative**:

$$v_f = \frac{m_1v_1 + m_2v_2}{m_1 + m_2}$$

**Plug in:**

$$v_f = \frac{(900)(20) + (1200)(-10)}{900 + 1200} = \frac{18{,}000 - 12{,}000}{2100} = +2.86\ \text{m/s}$$

The pair moves east, slowly.
""",
    distract=["b) 8.57 leaves out the second car's momentum.", "c) 14.3 forgets the minus sign.", "d) 20.0 is the first car's speed before.", "e) 30.0 adds the speeds."],
    fig=figs.carts(r"900 kg", r"1200 kg", r"$20$ m/s", r"$10$ m/s", rv_dir="left"), figsize=(4.0, 0.9)))

# 9 -- 2015 #6 elastic head-on
v9_1 = ((1.5 - 2.5) * 4.0 + 2 * 2.5 * (-2.0)) / 4.0
v9_2 = 4.0 + v9_1 - (-2.0)
Q.append(dict(
    stem=r"A 1.5 kg mass moving to the right at 4.0 m/s collides **elastically** in a head-on collision with a 2.5 kg mass moving at 2.0 m/s to the left. How fast and in what direction is the 2.5 kg mass moving after the collision? Positive to the right / negative to the left.",
    choices=["−3.5 m/s", "−2.0 m/s", "+0.25 m/s", "+2.0 m/s", "+2.5 m/s"], key="e",
    check=("near", v9_2, [-3.5, -2.0, 0.25, 2.0, 2.5], 0.05),
    value="+2.5 m/s", topic="1-D elastic collision", source="2015 Exam 2 #6; Ch 9 notes p. 3/5", card="Elastic",
    solution=r"""
Notecard, right $= +$: $m_1 = 1.5$, $v_{1i} = +4.0$; $m_2 = 2.5$, $v_{2i} = -2.0$.

$$v_{1f} = \frac{(m_1 - m_2)v_{1i} + 2m_2v_{2i}}{m_1 + m_2} = \frac{(-1.0)(4.0) + 2(2.5)(-2.0)}{4.0} = \frac{-4 - 10}{4} = -3.5\ \text{m/s}$$

$$v_{2f} = v_{1i} + v_{1f} - v_{2i} = 4.0 + (-3.5) - (-2.0) = +2.5\ \text{m/s}$$
""",
    distract=["a) −3.5 is the 1.5 kg mass's velocity.", "b) −2.0 is no change.", "c) +0.25 is the stick-together answer.", "d) +2.0 assumes it just reverses at the same speed."],
    fig=figs.two_balls(r"$1.5$ kg, $+4.0$ m/s", r"$2.5$ kg, $-2.0$ m/s", right_v="left", r1=0.3, r2=0.42), figsize=(3.6, 1.1)))

# 10 -- 2015 #8 ballistic KE fraction
frac10 = 100 * 0.010 / (4.99 + 0.010)
assert 0.1 < frac10 < 0.5
Q.append(dict(
    stem=r"A bullet (mass 0.010 kg) is fired into a suspended block of wood (4.99 kg). Initially the wood is not moving. The bullet lodges in the wood, and the block swings up. What fraction of the initial kinetic energy remained in the motion of the block of wood?",
    choices=["<0.1%", "0.1–0.5%", "0.5–1%", "1–10%", ">10%"], key="b",
    check=("concept",),
    value="0.2%", topic="Ballistic pendulum, KE fraction", source="2015 Exam 2 #8", card="Ballistic",
    solution=r"""
Notecard:

$$\frac{K_f}{K_i} = \frac{m}{M + m} = \frac{0.010}{5.00} = 0.002 = 0.2\%$$

That's in the **0.1–0.5%** range.
""",
    distract=["a) <0.1% would need a block heavier than 10 kg.", "e) >10% would mean the collision kept a lot of KE."],
    fig=figs.ballistic(r"$m_b$"), figsize=(3.4, 2.1)))

# 11 -- Ch 11 notes p.6/8 alpha from a time
a11 = (100 - 40) / 12
Q.append(dict(
    stem=r"A wheel speeds up uniformly from 40 rad/s to 100 rad/s in 12 s. What is its angular acceleration?",
    choices=["2.5 rad/s²", "3.33 rad/s²", "5.0 rad/s²", "8.33 rad/s²", "11.7 rad/s²"], key="c",
    check=("near", a11, [2.5, 3.33, 5.0, 8.33, 11.7], 0.01),
    value="5.0 rad/s²", topic="Rotational kinematics, $\\alpha$ from a time", source="Ch 11 notes p. 6/8", card="Rot. kinematics",
    solution=r"""
$\Delta\theta$ isn't given or asked for, so use the equation without it:

$$\omega_f = \omega_i + \alpha t$$

**Solve for $\alpha$:**

$$\alpha = \frac{\omega_f - \omega_i}{t}$$

**Plug in:**

$$\alpha = \frac{100 - 40}{12} = \frac{60}{12} = 5.0\ \text{rad/s}^2$$
""",
    distract=["a) 2.5 has an extra factor of 2.", "b) 3.33 is $\\omega_i/t$.", "d) 8.33 is $\\omega_f/t$.", "e) 11.7 adds the speeds."],
    fig=figs.wheel(r"$40 \to 100$ rad/s in $12$ s"), figsize=(2.6, 2.4)))

# 12 -- Ch 10 notes p.3/8 rolling sphere acceleration
a12 = 5 / 7 * g * sin(radians(22))
Q.append(dict(
    stem=r"A solid ball ($I = \tfrac25 mr^2$) rolls without slipping down a $22^\circ$ incline. What is the acceleration of its center?",
    choices=["1.84 m/s²", "2.45 m/s²", "2.62 m/s²", "3.67 m/s²", "6.49 m/s²"], key="c",
    check=("near", a12, [1.84, 2.45, 2.62, 3.67, 6.49], 0.005),
    value="2.62 m/s²", topic="Rolling ball acceleration", source="Ch 10 notes p. 3/8", card="Rolling (sphere row)",
    solution=r"""
Notecard, sphere row: $a = \tfrac57 g\sin\theta$, "less than sliding."

**Plug in:**

$$a = \tfrac57(9.8)\sin 22^\circ = \tfrac57(9.8)(0.3746) = 2.62\ \text{m/s}^2$$
""",
    distract=["a) 1.84 is a ring.", "b) 2.45 is a disk.", "d) 3.67 is sliding, $g\\sin\\theta$.", "e) 6.49 uses $\\cos\\theta$."],
    fig=figs.rolling_accel(r"$22^\circ$"), figsize=(3.2, 1.9)))

# 13 -- Ch 11 notes p.3/8 counter-rotating ring dropped on a disk
I13a, I13b = 0.5 * 400 * 2.0 ** 2, 150 * 1.2 ** 2
w13 = (I13a * 2.5 + I13b * (-3.0)) / (I13a + I13b)
Q.append(dict(
    stem=r"A rotating disk ($I = \tfrac12 MR^2$, $M = 400$ kg, $R = 2.0$ m, $\omega = +2.5$ rad/s) has a counter-rotating ring fall onto it ($I = mr^2$, $m = 150$ kg, $r = 1.2$ m, $\omega = -3.0$ rad/s). What is their final angular velocity?",
    choices=["+1.33 rad/s", "+1.85 rad/s", "+1.97 rad/s", "+2.50 rad/s", "+2.61 rad/s"], key="a",
    check=("near", w13, [1.33, 1.85, 1.97, 2.50, 2.61], 0.005),
    value="+1.33 rad/s", topic="Counter-rotating ring dropped on a disk", source="Ch 11 notes p. 3/8", card="Angular momentum",
    solution=r"""
Notecard, with the ring's $\omega_2$ **negative**:

$$\omega_f = \frac{I_1\omega_1 + I_2\omega_2}{I_1 + I_2}$$

**Moments of inertia:** $I_1 = \tfrac12(400)(2.0)^2 = 800$; $I_2 = (150)(1.2)^2 = 216$ (kg·m²).

**Plug in:**

$$\omega_f = \frac{(800)(2.5) + (216)(-3.0)}{800 + 216} = \frac{2000 - 648}{1016} = +1.33\ \text{rad/s}$$
""",
    distract=["b) 1.85 treats the ring as a disk ($\\tfrac12 mr^2$).", "c) 1.97 ignores the ring's spin.", "d) 2.50 is no change.", "e) 2.61 forgets the minus sign."],
    fig=figs.stacked_disks(r"$+2.5$", r"ring $-3.0$"), figsize=(3.4, 1.9)))

# 14 -- Ch 11 notes p.4/8 man runs up and jumps on the rim
I14 = 0.5 * 350 * 2.2 ** 2
w14 = (I14 * 0.40 + 90 * 3.5 * 2.2) / (I14 + 90 * 2.2 ** 2)
Q.append(dict(
    stem=r"A 90 kg man runs at 3.5 m/s up to a turning merry-go-round (a disk, $I = \tfrac12 MR^2$, $M = 350$ kg, $R = 2.2$ m, $\omega_i = 0.40$ rad/s) and jumps on at the rim, moving in the same direction as the rim. What is the new angular velocity?",
    choices=["−0.28 rad/s", "0.26 rad/s", "0.40 rad/s", "0.80 rad/s", "1.22 rad/s"], key="d",
    check=("near", w14, [-0.28, 0.26, 0.40, 0.80, 1.22], 0.01),
    value="0.80 rad/s", topic="Man runs and jumps on the rim", source="Ch 11 notes p. 4/8", card="Angular momentum",
    solution=r"""
Notecard with $+mvR$ (same direction) and $I_{add} = mR^2$:

$$\omega_f = \frac{\tfrac12 MR^2\,\omega_i + mvR}{\tfrac12 MR^2 + mR^2}$$

**Plug in** ($\tfrac12 MR^2 = \tfrac12(350)(2.2)^2 = 847$ kg·m²):

$$
\begin{aligned}
\omega_f &= \frac{(847)(0.40) + (90)(3.5)(2.2)}{847 + (90)(2.2)^2} \\[8pt]
&= \frac{338.8 + 693}{847 + 435.6} = \frac{1031.8}{1282.6} = 0.80\ \text{rad/s}
\end{aligned}
$$
""",
    distract=["a) −0.28 uses $-mvR$ (running against the rim).", "b) 0.26 ignores his running momentum.", "c) 0.40 is no change.", "e) 1.22 forgets to add his $mR^2$."],
    fig=figs.mgr_runner(r"$3.5$ m/s"), figsize=(3.2, 2.0)))

# 15 -- Ch 11 notes p.7/8 man walks from the rim to the center
w15 = (300 + 2 * 80) / 300 * 1.2
Q.append(dict(
    stem=r"An 80 kg man rides on the rim of a merry-go-round ($I = \tfrac12 MR^2$, $M = 300$ kg, $R = 2.5$ m). Initially the angular velocity is 1.2 rad/s. He walks from the rim to the center. What is the angular velocity when he reaches the center?",
    choices=["0.78 rad/s", "1.20 rad/s", "1.52 rad/s", "1.84 rad/s", "2.48 rad/s"], key="d",
    check=("near", w15, [0.78, 1.20, 1.52, 1.84, 2.48], 0.005),
    value="1.84 rad/s", topic="Man walks from the rim to the center", source="Ch 11 notes p. 7/8", card="Angular momentum (rim→center)",
    solution=r"""
Notecard, rim$\to$center:

$$\omega_f = \frac{M + 2m}{M}\,\omega_i$$

**Plug in:**

$$\omega_f = \frac{300 + 2(80)}{300}(1.2) = \frac{460}{300}(1.2) = 1.84\ \text{rad/s}$$

$R$ isn't needed. The KE goes up: "it took energy to move from rim to the center."
""",
    distract=["a) 0.78 flips the ratio (walking out).", "b) 1.20 is no change.", "c) 1.52 uses $\\frac{M + m}{M}$.", "e) 2.48 uses $\\frac{M + 4m}{M}$."],
    fig=figs.mgr_walk_in(), figsize=(3.6, 1.7)))

INTRO = r"""
Practice Exam 2-9 mixes **lecture-note examples** and **2015 Exam 2 questions** with new numbers, with no banked curves. It covers the flat curve, $N = 6mg$ at the bottom of the loop, the incline cases, the block sliding down with a hanging mass, the spring launch, the bounce, the head-on sticking cars, the elastic collision, the ballistic KE fraction, $\alpha$ from a time, the rolling ball, the counter-rotating ring, the man jumping on, and the man walking to the center. Question 1 is a **maximum** trap: round down. The last column says which 3×5 notecard entry solves each question.
"""

if __name__ == "__main__":
    build(9, "Chapters 6, 7/8, 9, 10, 11", Q, INTRO)
