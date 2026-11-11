"""Question generators for PHYS1408 Exam 3 (Ch 12 Statics, Ch 13 Gravity).

Every generator is one problem type taken from the professor's lecture notes
(Professors-Notes/Chapter 12 Statics-2.pdf, Chapter 13 Gravity-2.pdf) or the
2015 Exam 3 (Professors-Notes/exam 3-4.pdf). Each takes the target answer letter
and the numbers, computes the answer, builds distractors from specific mistakes,
and writes the worked solution.

Templates use <<name>> placeholders (filled by T()) to keep LaTeX braces readable.
"""
import math
from math import atan, cos, degrees, pi, radians, sin, sqrt, tan

import figs3
from examlib3 import G, LETTERS, ME, RE, U, g, grid, numeric, place_text, plain, sig, tex

C_LIGHT = 3e8
M_SUN = 2e30
AU = 1.5e11


def T(_tpl, **kw):
    s = _tpl
    for k, v in kw.items():
        s = s.replace(f"<<{k}>>", str(v))
    assert "<<" not in s, s[s.index("<<"):s.index("<<") + 30]
    return s


def N(v, n=None):
    """Given values: compact, the way the professor writes them (4 m, 0.25, 6.37e6). Computed values: n sig figs."""
    if n is not None:
        return tex(v, n)
    for k in range(1, 5):
        if abs(sig(v, k) - v) <= 1e-9 * max(1, abs(v)):
            break
    t = tex(v, k)
    return t


class NotOnExam(Exception):
    """PHYS1408 rule: only procedures worked in the lecture notes or on the 2015 Exam 3 may be tested."""


def banned(why):
    raise NotOnExam(why)


def rec(**kw):
    kw.setdefault("prev", None)
    kw.setdefault("fig", None)
    return kw


# =====================================================================
# Chapter 12 — Statics
# =====================================================================

def beam_carry(target, L, M, loads, right_x=None, ask="right", names=("James", "Sarah"), obj="sofa"):
    """Two people hold a uniform beam (left one at x = 0). Point loads [(mass, x, what)].
    Notes Ch 12 p. 4/10 (two men carry a sofa), p. 5/10 (kid sits on the sofa); 2015 Exam 3 #1."""
    right_x = L if right_x is None else right_x
    A, B = names
    W = M * g
    torque_loads = sum(m * g * x for m, x, _ in loads)
    total = W + sum(m * g for m, _, _ in loads)
    R = (W * L / 2 + torque_loads) / right_x
    Lf = total - R
    val = R if ask == "right" else Lf
    other = Lf if ask == "right" else R
    who, pivot = (B, A) if ask == "right" else (A, B)

    mistakes = [
        (other, f"is the force on {pivot}, the other person."),
        (total / 2, "splits the total weight evenly; that is only true with nothing extra and both at the ends."),
    ]
    if right_x != L:
        R_L = (W * L / 2 + torque_loads) / L
        mistakes.append((R_L if ask == "right" else total - R_L,
                         f"uses {N(L)} m (the full length) as {B}'s lever arm instead of {N(right_x)} m."))
    R_noW = torque_loads / right_x
    mistakes.append((R_noW if ask == "right" else total - W - R_noW, f"leaves out the {obj}'s own weight."))
    R_noload = (W * L / 2) / right_x
    mistakes.append((R_noload if ask == "right" else W - R_noload, "leaves out the added load."))
    mistakes.append((total, "is the total weight of everything; the two people share it."))
    mistakes.append((W / 2 + sum(m * g for m, _, _ in loads), f"gives {who} half the {obj} plus the whole load; the load's share depends on where it sits."))
    mistakes.append((val / g, "forgets $g$ (answers in kg, not N)."))
    choices, nums, distract = numeric(val, mistakes, target, "N")

    load_txt = "; ".join(f"{N(m)} kg {what} at {N(x)} m" for m, x, what in loads)
    if right_x == L:
        hold = f"{A} and {B} each hold one end of a uniform {N(L)} m, {N(M)} kg {obj}."
    else:
        hold = (f"A {N(M)} kg {obj} {N(L)} m long is carried by {A} and {B}. {A} has one end; "
                f"{B} holds the {obj} {N(L - right_x)} m from the other end.")
    if len(loads) == 1 and loads[0][1] == L:
        place = f"A helper sets a {N(loads[0][0])} kg {loads[0][2]} on the very end of the {obj} that {B} is holding."
    else:
        place = " ".join(f"A {N(m)} kg {what} is placed on the {obj} {N(x)} m from {A}." for m, x, what in loads)
    stem = f"{hold} {place} How much force must {who} exert now?"

    terms_sym = [r"\tfrac{L}{2}\,Mg"] + [rf"x_{{{i + 1}}}\,m_{{{i + 1}}}g" for i in range(len(loads))]
    terms_num = [U(rf"{N(L / 2)}\ \text{{m}}", f"{obj} center") + r"\," + U(rf"({N(M)})(9.8)", f"{obj} weight")]
    for m, x, what in loads:
        terms_num.append(U(rf"{N(x)}\ \text{{m}}", f"{what} position") + r"\," + U(rf"({N(m)})(9.8)", f"{what} weight"))
    sol = T(r"""
**Step 1: pick the pivot at <<pivot>>'s hands.** A force applied at the pivot has $r = 0$, so its torque is zero and it drops out of the equation. The notes do this on p. 3/10 ("A is eliminated").

**Step 2: torque balance about <<pivot>>.** Every force here is vertical and the <<obj>> is horizontal, so each torque is $\tau = rF$, with $r$ measured from <<pivot>>. The <<obj>>'s weight acts at its center, $L/2$. <<B>>'s upward push is counterclockwise; the weights are clockwise.

$$
\sum\tau_{<<pivot>>} = 0:\quad x_{<<B>>}\,F_{<<B>>} = <<terms_sym>>
$$

**Step 3: plug in** ($x_{<<B>>} = <<xr>>$ m):

$$
<<xr>>\ \text{m}\times F_{<<B>>} = <<terms_num>>
$$

$$
F_{<<B>>} = \frac{<<num>>\ \text{N m}}{<<xr>>\ \text{m}} = <<R>>\ \text{N}
$$
""", pivot=pivot if ask == "right" else A, obj=obj, B=B, xr=N(right_x),
          terms_sym=" + ".join(terms_sym), terms_num=" + ".join(terms_num),
          num=N(W * L / 2 + torque_loads, 4), R=N(R, 4))
    if ask == "left":
        sol += T(r"""
**Step 4: forces up = forces down** ($\sum F_y = 0$) gives <<A>>'s share:

$$
F_{<<A>>} = \underbrace{<<tot>>\ \text{N}}_{\text{total weight}} - \underbrace{<<R>>\ \text{N}}_{F_{<<B>>}} = <<Lf>>\ \text{N}
$$

(You can also take torques about <<B>> directly, as the notes do on p. 5/10 for Jim.)
""", A=A, B=B, tot=N(total, 4), R=N(R, 4), Lf=N(Lf, 4))
    ticks = sorted(set([0, L, right_x] + [x for _, x, _ in loads]))
    fig = figs3.beam(L, [(0, A, "up"), (right_x, B, "up")],
                     [(L / 2, f"{N(M)} kg")] + [(x, f"{N(m)} kg") for m, x, _ in loads], ticks=ticks)
    prev = "2015 Exam 3 #1 (sofa + box of books on Sarah's end), new numbers" if right_x != L else None
    return rec(stem=stem, choices=choices, key=target, check=("near", val, nums),
               topic=f"Two people carry a {obj}", source_short="Ch 12 p. 4–5" + ("; 2015 #1" if prev else ""),
               source="Ch 12 notes p. 4/10 (two men carry a sofa: $\\sum\\tau_{Jim}$, $\\sum\\tau_{Sam}$) and p. 5/10 (20 kg kid set on the sofa 1 m from Jim).",
               prev=prev, card="Sofa / beam", tests="torque balance about one carrier to find the other carrier's force.",
               solution=sol, distract=distract, fig=fig, figsize=(4.4, 1.6), figwidth="3.2in", layout=52)


def diving_board(target, L, M, a, ask="B"):
    """Notes Ch 12 p. 3/10: board on support A (end, x=0) and B (x=a); A pulls DOWN."""
    W = M * g
    B = (L / 2) / a * W
    A = B - W
    val = B if ask == "B" else A
    if ask == "B":
        mistakes = [(A, "is the force from support A, not B."), (W, "is just the board's weight $Mg$."),
                    ((L / a) * W, "puts the board's weight at the far end ($L$) instead of its center ($L/2$)."),
                    (B + W, "adds $Mg$ instead of subtracting it.")]
    else:
        mistakes = [(B, "is the force from support B, not A."), (W, "is just the board's weight $Mg$."),
                    (B + W, "gets the direction of A wrong: with A pushing up, $\\sum F_y$ gives a nonsense $B + Mg$."),
                    ((L / a - 1) * W, "puts the board's weight at the far end ($L$) instead of its center.")]
    choices, nums, distract = numeric(val, mistakes, target, "N")
    stem = (f"A uniform diving board is {N(L)} m long and has a mass of {N(M)} kg. It rests on two supports: "
            f"support A at the back end (x = 0) and support B {N(a)} m from that end. Nothing is standing on the board. "
            f"What is the magnitude of the force from support {ask}?")
    sol = T(r"""
**Step 1: draw the forces** (notes p. 3/10). The board's weight $Mg$ acts at its center, $L/2 = <<h>>$ m. B pushes **up**. A must pull **down**, or the board would tip off B.

**Step 2: torque about A** removes A ($r = 0$):

$$
\sum\tau_A = 0:\quad a\,B - \tfrac{L}{2}\,Mg = 0
$$

$$
B = \frac{L/2}{a}\,Mg = \frac{\overbrace{<<h>>\ \text{m}}^{L/2}}{\underbrace{<<a>>\ \text{m}}_{\text{A to B}}}\,\underbrace{(<<M>>)(9.8)}_{Mg = <<W>>\ \text{N}} = <<B>>\ \text{N}
$$

**Step 3: $\sum F_y = 0$** with B up and A, $Mg$ down:

$$
B - A - Mg = 0 \;\Rightarrow\; A = B - Mg = <<B>> - <<W>> = <<A>>\ \text{N}
$$

In the notes ($L = 10$ m, $a = 1$ m) this gives $B = 5Mg$ and $A = 4Mg$.
""", h=N(L / 2), a=N(a), M=N(M), W=N(W, 4), B=N(B, 4), A=N(A, 4))
    fig = figs3.beam(L, [(0, "A", "down"), (a, "B", "up")], [(L / 2, r"$Mg$")], ticks=[0, a, L / 2, L])
    return rec(stem=stem, choices=choices, key=target, check=("near", val, nums),
               topic=f"Diving board, support {ask}", source_short="Ch 12 p. 3",
               source="Ch 12 notes p. 3/10 (diving board, $L = 10$ m, $M = 1000$ kg: $B = 5Mg$, $A = 4Mg$).",
               card="Diving board", tests="choosing the pivot to eliminate one support, then $\\sum F_y = 0$ (A pulls down).",
               solution=sol, distract=distract, fig=fig, figsize=(4.4, 1.6), figwidth="3.2in", layout=52)


def seesaw(target, L, mk, MT, ask="x", Ms=None):
    """Notes Ch 12 p. 4/10: kid m_k at the end, M_T at x from the center; x = L m_k / (2 M_T)."""
    if ask != "x":
        banned("seesaw solved for the mass: the notes only solve for x")
    x = L * mk / (2 * MT)
    assert x < L / 2
    extra = f" The seesaw itself has a mass of {N(Ms)} kg." if Ms else ""
    if ask == "x":
        val = x
        mistakes = [(L * mk / MT, "forgets that the kid's lever arm is $L/2$, not $L$."),
                    (L / 2 - x, "measures from the end of the seesaw instead of from the center."),
                    (L / 2 + x if L / 2 + x < L else None, "adds the half-length."),
                    (L * mk / (2 * (MT + Ms)) if Ms else None, "adds the seesaw's mass to the adult's; its weight acts at the pivot and has no torque.")]
        choices, nums, distract = numeric(val, mistakes, target, "m")
        stem = (f"A seesaw {N(L)} m long pivots at its center. A {N(mk)} kg kid sits at one end. How far from the "
                f"center must a {N(MT)} kg adult sit on the other side so that the seesaw balances?{extra}")
    else:
        val = MT
        mistakes = [(L * mk / x, "uses $L$ instead of $L/2$ for the kid's lever arm."),
                    (mk * 2 * x / L, "inverts the lever-arm ratio."),
                    (mk, "assumes equal masses balance at any position."),
                    (MT + Ms if Ms else None, "adds the seesaw's mass.")]
        choices, nums, distract = numeric(val, mistakes, target, "kg")
        stem = (f"A seesaw {N(L)} m long pivots at its center. A {N(mk)} kg kid sits at one end. The seesaw balances when "
                f"the kid's parent sits {N(x, 3)} m from the center on the other side. What is the parent's mass?{extra}")
    sol = T(r"""
**Step 1: torque about the center (pivot).** The seesaw's own weight acts at the center, so its lever arm is zero. That's why the notes say its mass "don't care!" The kid is $L/2$ from the pivot; the adult is $x$ from it.

$$
\sum\tau_{center} = 0:\quad \tfrac{L}{2}\,m_k g - x\,M_T g = 0 \;\Rightarrow\; x = \frac{L\,m_k}{2M_T}
$$

$g$ cancels.

**Step 2: plug in:**

$$
<<line>>
$$
""", line=(rf"x = \frac{{{U(N(L) + r'\ \text{m}', 'length')}\,{U(N(mk) + r'\ \text{kg}', 'kid')}}}{{2\,{U(N(MT) + r'\ \text{kg}', 'adult')}}} = {N(x, 3)}\ \text{{m}}"
           if ask == "x" else
           rf"M_T = \frac{{L\,m_k}}{{2x}} = \frac{{{U(N(L) + r'\ \text{m}', 'length')}\,{U(N(mk) + r'\ \text{kg}', 'kid')}}}{{2\,{U(N(x, 3) + r'\ \text{m}', 'parent to center')}}} = {N(MT, 3)}\ \text{{kg}}"))
    sol += "\nIn the notes, $m_k = 20$ kg and $M_T = 100$ kg give $x = L/10$.\n"
    return rec(stem=stem, choices=choices, key=target, check=("near", val, nums),
               topic="Seesaw balance" + (" (find the mass)" if ask != "x" else ""), source_short="Ch 12 p. 4",
               source="Ch 12 notes p. 4/10 (seesaw, $m_k = 20$ kg, $M = 100$ kg, $x = L/10$).",
               card="Seesaw", tests="torque balance about the pivot; the seesaw's own mass drops out.",
               solution=sol, distract=distract, fig=figs3.seesaw(), figsize=(3.6, 1.3), figwidth="2.6in")


def boom(target, L, M, m, theta, Tmax=None, x=None, ask="x"):
    """Notes Ch 12 p. 6/10: beam hinged at a wall, cable from the far end at theta; mass m hangs at x."""
    if ask != "x":
        banned("wall beam solved for T: the notes only solve for x_max")
    s = sin(radians(theta))
    if ask == "x":
        val = (L / (m * g)) * (Tmax * s - M * g / 2)
        assert 0 < val < L, val
        mistakes = [((L / (m * g)) * (Tmax * cos(radians(theta)) - M * g / 2), "uses $\\cos\\theta$ instead of $\\sin\\theta$ for the cable's perpendicular part."),
                    (L * Tmax * s / (m * g), "leaves out the beam's own weight."),
                    ((L / (m * g)) * (Tmax * s - M * g), "puts the beam's weight at the far end ($L$) instead of $L/2$."),
                    ((L / (m * g)) * (Tmax * s - M * g / 2) / 2, "divides by 2 one time too many.")]
        mistakes = [(v if 0 < v < 0.95 * L else None, w) for v, w in mistakes]
        choices, nums, distract = numeric(val, mistakes, target, "m", cap=0.97 * L)
        assert max(nums) < L, "x choices must fit on the beam"
        stem = (f"A uniform {N(L)} m, {N(M)} kg beam sticks straight out from a wall on a hinge. A cable runs from the far end of the beam "
                f"back to the wall above the hinge, making a {N(theta)}° angle with the beam. The cable can hold at most "
                f"$T_{{max}} = {N(Tmax)}$ N. A {N(m)} kg mass hangs from the beam a distance $x$ from the wall. What is the largest $x$ "
                f"the cable can support?")
        sol = T(r"""
**Step 1: torque about the hinge** (left end). The notes say "Do torque at left to remove reaction forces": the hinge forces $R_x$, $R_y$ act at $r = 0$.

Only the **perpendicular** part of the tension, $T\sin\theta$, makes torque at the far end ($\tau = rF_\perp$, notes p. 1/10). The beam's weight acts at $L/2$; the mass's weight acts at $x$.

$$
\sum\tau_{left} = 0:\quad -x\,mg - \tfrac{L}{2}\,Mg + L\,T\sin\theta = 0
$$

**Step 2: solve for $x$:**

$$
x = \frac{L}{mg}\left(T\sin\theta - \frac{Mg}{2}\right)
$$

**Step 3: plug in $T = T_{max}$:**

$$
x_{max} = \frac{<<L>>\ \text{m}}{\underbrace{(<<m>>)(9.8)}_{mg}}\left(\underbrace{(<<T>>)(\sin <<th>>^\circ)}_{T\sin\theta = <<Ts>>\ \text{N}} - \underbrace{\frac{(<<M>>)(9.8)}{2}}_{Mg/2 = <<half>>\ \text{N}}\right) = <<x>>\ \text{m}
$$
""", L=N(L), m=N(m), T=N(Tmax), th=N(theta), Ts=N(Tmax * s, 4), M=N(M), half=N(M * g / 2, 4), x=N(val, 3))
    else:
        val = (x * m * g + (L / 2) * M * g) / (L * s)
        mistakes = [((x * m * g + (L / 2) * M * g) / (L * cos(radians(theta))), "uses $\\cos\\theta$ instead of $\\sin\\theta$."),
                    (x * m * g / (L * s), "leaves out the beam's own weight."),
                    ((x * m * g + L * M * g) / (L * s), "puts the beam's weight at $L$ instead of $L/2$."),
                    ((x * m * g + (L / 2) * M * g) / L, "forgets the angle (uses all of $T$ as perpendicular).")]
        choices, nums, distract = numeric(val, mistakes, target, "N")
        stem = (f"A uniform {N(L)} m, {N(M)} kg beam sticks straight out from a wall on a hinge. A cable runs from the far end of the beam "
                f"back to the wall above the hinge, making a {N(theta)}° angle with the beam. A {N(m)} kg mass hangs from the beam "
                f"{N(x)} m from the wall. What is the tension in the cable?")
        sol = T(r"""
**Step 1: torque about the hinge** (left end) removes the hinge forces (notes p. 6/10: "Do torque at left to remove reaction forces"). Only $T\sin\theta$ makes torque ($\tau = rF_\perp$, p. 1/10).

$$
\sum\tau_{left} = 0:\quad -x\,mg - \tfrac{L}{2}\,Mg + L\,T\sin\theta = 0 \;\Rightarrow\; T = \frac{x\,mg + \tfrac{L}{2}Mg}{L\sin\theta}
$$

**Step 2: plug in:**

$$
T = \frac{\underbrace{(<<x>>)(<<m>>)(9.8)}_{\text{mass: } <<t1>>\ \text{N m}} + \underbrace{(<<h>>)(<<M>>)(9.8)}_{\text{beam: } <<t2>>\ \text{N m}}}{\underbrace{(<<L>>)(\sin <<th>>^\circ)}_{L\sin\theta}} = <<T>>\ \text{N}
$$
""", x=N(x), m=N(m), t1=N(x * m * g, 4), h=N(L / 2), M=N(M), t2=N(L / 2 * M * g, 4), L=N(L), th=N(theta), T=N(val, 4))
    sol += "\nNotes numbers: $L = 5$ m, $T_{max} = 10^4$ N, $M = 1000$ kg, $m = 100$ kg, $\\theta = 30^\\circ$ give $x_{max} = 0.510$ m.\n"
    fig = figs3.boom(theta, {"T": r"$T$" if ask == "x" else r"$T=?$", "x": r"$x$" if ask == "x" else f"{N(x)} m",
                             "m": f"{N(m)} kg", "M": f"{N(M)} kg", "L": f"{N(L)} m"})
    return rec(stem=stem, choices=choices, key=target, check=("near", val, nums),
               topic="Beam on a wall hinge with a cable" + (" ($x_{max}$)" if ask == "x" else " (tension)"),
               source_short="Ch 12 p. 6", source="Ch 12 notes p. 6/10 (beam hinged at the wall, cable at $\\theta = 30^\\circ$, find $x_{max}$); $\\tau = rF_\\perp$ from p. 1/10.",
               card="Wall beam + cable", tests="torque about the hinge with the perpendicular part of the tension.",
               solution=sol, distract=distract, fig=fig, figsize=(3.4, 2.4), figwidth="2.4in")


def ladder_min(target, mu):
    """Notes Ch 12 p. 7/10: theta_min = atan(1/(2 mu_s)), frictionless wall."""
    val = degrees(atan(1 / (2 * mu)))
    mistakes = [(degrees(atan(2 * mu)), "is $\\tan^{-1}(2\\mu_s)$, the complement of the right angle (measured from the wall)."),
                (degrees(atan(1 / mu)), "drops the $\\tfrac12$ (puts the ladder's weight at the top instead of the middle)."),
                (degrees(atan(mu)), "is $\\tan^{-1}\\mu_s$, the angle of a block sliding on a slope, not the ladder."),
                (degrees(atan(1 / (4 * mu))), "has an extra factor of 2.")]
    choices, nums, distract = numeric(val, mistakes, target, "°", n=3, cap=90)
    stem = (f"A uniform ladder leans against a frictionless wall. The coefficient of static friction between the ladder and the floor is "
            f"$\\mu_s = {N(mu)}$. What is the minimum angle $\\theta$ between the ladder and the floor at which the ladder will not slide?")
    sol = T(r"""
**Step 1: forces** (notes p. 7/10). Floor: $N = mg$ up and friction $F_f$ toward the wall. Wall (frictionless): $N_w$ only, horizontal. At $\theta_{min}$ friction is at its maximum, $F_f = \mu_s N$, so $N_w = F_f = \mu_s mg$.

**Step 2: torque about the base.** Weight $mg$ acts at $L/2$ with lever arm $\tfrac{L}{2}\cos\theta$; $N_w$ acts at the top with lever arm $L\sin\theta$:

$$
\tfrac{L}{2}\cos\theta\,mg - L\sin\theta\,\mu_s mg = 0 \;\Rightarrow\; \tan\theta = \frac{1}{2\mu_s}
$$

**Step 3: plug in:**

$$
\theta_{min} = \tan^{-1}\frac{1}{2\,\underbrace{(<<mu>>)}_{\mu_s}} = \tan^{-1}(<<r>>) = <<th>>^\circ
$$

$L$ and $m$ both cancel: only $\mu_s$ matters.
""", mu=N(mu), r=N(1 / (2 * mu), 4), th=N(val, 3))
    return rec(stem=stem, choices=choices, key=target, check=("near", val, nums),
               topic="Ladder, minimum angle", source_short="Ch 12 p. 7",
               source="Ch 12 notes p. 7/10 (\"ladder leans at $\\theta$, what is minimum $\\theta$ for it not to slide?\" $\\theta_{min} = \\tan^{-1}\\tfrac{1}{2\\mu_s}$).",
               card="Ladder", tests="ladder torque balance about the base; $\\theta_{min} = \\tan^{-1}(1/2\\mu_s)$.",
               solution=sol, distract=distract, fig=figs3.ladder(55, man=False), figsize=(2.2, 2.2), figwidth="1.5in")


def ladder_climb(target, L, theta, mu, M, m, step=0.5):
    """Notes Ch 12 p. 8/10 and 2015 Exam 3 #2: x = (L/M)(mu (M+m) tan(theta) - m/2). Maximum question."""
    x = (L / M) * (mu * (M + m) * tan(radians(theta)) - m / 2)
    assert 0 < x < L, x
    choices, nums, distract = grid(x, target, step, "m", "max", fmt=lambda v: f"{v:.1f}")
    stem = (f"A {N(M)} kg man (with the load he carries) climbs a uniform {N(L)} m, {N(m)} kg ladder that leans against a frictionless wall "
            f"at {N(theta)}° to the floor. The coefficient of static friction between the ladder and the floor is {N(mu)}. "
            f"How far up the ladder can he safely climb?")
    sol = T(r"""
**Step 1: forces** (notes p. 8/10). $\sum F_y$: $N = (M + m)g$. $\sum F_x$: $N_w = F_f$, and at the limit $F_f = \mu_s N = \mu_s(M+m)g$.

**Step 2: torque about the base.** Ladder weight at $L/2$ (arm $\tfrac{L}{2}\cos\theta$), man at $x$ (arm $x\cos\theta$), wall force at the top (arm $L\sin\theta$):

$$
\tfrac{L}{2}\cos\theta\,mg + x\cos\theta\,Mg - L\sin\theta\,\mu_s(M+m)g = 0
$$

Cancel $g$, divide by $\cos\theta$:

$$
x = \frac{L}{M}\Big(\mu_s(M+m)\tan\theta - \frac{m}{2}\Big)
$$

**Step 3: plug in** ($\tan <<th>>^\circ = <<tan>>$):

$$
x = \frac{\overbrace{<<L>>}^{L}}{\underbrace{<<M>>}_{M}}\Big(\underbrace{(<<mu>>)}_{\mu_s}\underbrace{(<<Mm>>)}_{M+m}(<<tan>>) - \underbrace{\tfrac{<<m>>}{2}}_{m/2}\Big) = <<x>>\ \text{m}
$$

**Step 4: it's a maximum.** He can go up to <<x>> m; any farther and the ladder slips. The largest choice that still works is **<<ans>>**. (On the 2015 exam, $x = 3.78$ m and the answer was b) 3.5 m.)
""", th=N(theta), tan=N(tan(radians(theta)), 4), L=N(L), M=N(M), mu=N(mu), Mm=N(M + m), m=N(m), x=N(x, 3),
          ans=choices[LETTERS.index(target)])
    return rec(stem=stem, choices=choices, key=target, check=("max", x, nums),
               topic="Man climbing a ladder, $x_{max}$", source_short="Ch 12 p. 8; 2015 #2",
               source="Ch 12 notes p. 8/10 (leaning ladder with a man climbing it, $x = \\tfrac{L}{M}(\\mu_s(M+m)\\tan\\theta - \\tfrac{m}{2})$ = 8.8 m).",
               prev="2015 Exam 3 #2 (150 kg man, 20 kg ladder, 71°, $\\mu = 0.25$, 5 m), new numbers",
               card="Ladder", tests="ladder torque balance with a climber, then the maximum-answer rule.",
               solution=sol, distract=distract, fig=figs3.ladder(theta), figsize=(2.2, 2.4), figwidth="1.5in")


def ladder_top_angle(target, mu, M, m, L=10):
    """Notes Ch 12 p. 9/10: angle so he can climb to x = L: tan(theta) = (M + m/2)/((M+m) mu)."""
    val = degrees(atan((M + m / 2) / ((M + m) * mu)))
    mistakes = [(degrees(atan(1 / (2 * mu))), "is $\\theta_{min}$ for the empty ladder (p. 7/10); it ignores the man."),
                (degrees(atan(M / ((M + m) * mu))), "drops the ladder's own $m/2$ term."),
                (degrees(atan(1 / mu)), "is $\\tan^{-1}(1/\\mu_s)$, which treats all the weight as being at the top."),
                (90 - val, "is the angle from the wall, not from the floor.")]
    choices, nums, distract = numeric(val, mistakes, target, "°", cap=90)
    stem = (f"A {N(M)} kg man (plus load) wants to climb all the way to the top of a uniform {N(L)} m, {N(m)} kg ladder leaning against a "
            f"frictionless wall. The coefficient of static friction with the floor is {N(mu)}. What is the minimum angle between "
            f"the ladder and the floor that lets him reach the top without the ladder slipping?")
    sol = T(r"""
**Step 1: start from the climbing result** (notes p. 8/10), $xM = \mu_s L(M+m)\tan\theta - \tfrac{mL}{2}$, and set $x = L$ (notes p. 9/10, "He can climb to $x = L$, what $\theta$ is minimum?"):

$$
LM + L\frac{m}{2} = \mu_s L(M+m)\tan\theta \;\Rightarrow\; \tan\theta = \frac{M + m/2}{(M+m)\mu_s}
$$

$L$ cancels, so the ladder's length doesn't matter.

**Step 2: plug in:**

$$
\theta_{min} = \tan^{-1}\frac{\overbrace{<<M>> + <<mh>>}^{M + m/2}}{\underbrace{(<<Mm>>)}_{M+m}\underbrace{(<<mu>>)}_{\mu_s}} = \tan^{-1}(<<r>>) = <<th>>^\circ
$$

Notes numbers ($M = 150$, $m = 10$, $\mu_s = 0.4$): $\tan^{-1}(155/64) = 67.6^\circ$.
""", M=N(M), mh=N(m / 2), Mm=N(M + m), mu=N(mu), r=N((M + m / 2) / ((M + m) * mu), 4), th=N(val, 3))
    return rec(stem=stem, choices=choices, key=target, check=("near", val, nums),
               topic="Ladder angle to reach the top", source_short="Ch 12 p. 9",
               source="Ch 12 notes p. 9/10 (\"He can climb to $x = L$, what $\\theta$ is minimum?\" $\\theta_{min} = \\tan^{-1}\\tfrac{M + m/2}{(M+m)\\mu_s} = 67.6^\\circ$).",
               card="Ladder", tests="the notes p. 9 procedure: solve for $\\theta$ with $x = L$.",
               solution=sol, distract=distract)


def lamp(target, m, theta, ask="ceiling"):
    """2015 Exam 3 #3: light hung by a cord at theta with the ceiling plus a horizontal cord."""
    if ask != "ceiling":
        banned("horizontal-cord tension: 2015 #3 asks only for the ceiling cord")
    W = m * g
    Tc = W / sin(radians(theta))
    Th = W / tan(radians(theta))
    val = Tc if ask == "ceiling" else Th
    if ask == "ceiling":
        mistakes = [(W / cos(radians(theta)), "uses $\\cos\\theta$: that would be the angle from the vertical."),
                    (W, "is just the light's weight."), (Th, "is the tension in the horizontal cord."),
                    (W * sin(radians(theta)), "multiplies by $\\sin\\theta$ instead of dividing.")]
    else:
        mistakes = [(Tc, "is the tension in the ceiling cord."), (W * tan(radians(theta)), "uses $\\tan\\theta$ upside down."),
                    (W, "is just the light's weight."), (Tc * sin(radians(theta)) * 0 + W * cos(radians(theta)), "is $mg\\cos\\theta$.")]
    choices, nums, distract = numeric(val, mistakes, target, "N")
    which = "the cord connected to the ceiling" if ask == "ceiling" else "the horizontal cord"
    stem = (f"A {N(m)} kg light hangs from a knot. One cord runs from the knot to the ceiling, making a {N(theta)}° angle with the ceiling. "
            f"A second cord is exactly horizontal and is anchored in the wall. What is the tension in {which}?")
    sol = T(r"""
**Step 1: forces on the knot** (static, so $\sum F_x = \sum F_y = 0$, notes p. 1/10). Ceiling cord $T$ at $\theta$ above the horizontal; horizontal cord $T_h$; the light's weight $mg$ hangs straight down.

**Step 2: $\sum F_y = 0$.** Only the ceiling cord has a vertical part, $T\sin\theta$:

$$
T\sin\theta = mg \;\Rightarrow\; T = \frac{mg}{\sin\theta} = \frac{\underbrace{(<<m>>)(9.8)}_{mg = <<W>>\ \text{N}}}{\sin <<th>>^\circ} = <<Tc>>\ \text{N}
$$
""", m=N(m), W=N(W, 4), th=N(theta), Tc=N(Tc, 4))
    if ask != "ceiling":
        sol += T(r"""
**Step 3: $\sum F_x = 0$.** The horizontal cord balances the ceiling cord's horizontal part:

$$
T_h = T\cos\theta = \frac{mg}{\tan\theta} = \frac{<<W>>\ \text{N}}{\tan <<th>>^\circ} = <<Th>>\ \text{N}
$$
""", W=N(W, 4), th=N(theta), Th=N(Th, 4))
    return rec(stem=stem, choices=choices, key=target, check=("near", val, nums),
               topic="Light hung by two cords" + (" (horizontal cord)" if ask != "ceiling" else ""),
               source_short="2015 #3; Ch 12 p. 1",
               source="2015 Exam 3 #3, solved with $\\sum F_x = \\sum F_y = 0$ from Ch 12 notes p. 1/10 (\"Static means not moving\").",
               prev="2015 Exam 3 #3 (20 kg light, 40° with the ceiling: 305 N $\\rightarrow$ b) 300 N), new numbers",
               card="Two cords", tests="$\\sum F_y = 0$ on the knot: $T\\sin\\theta = mg$.",
               solution=sol, distract=distract, fig=figs3.lamp(theta, r"$T=?$" if ask == "ceiling" else r"$T$"),
               figsize=(3.2, 1.9), figwidth="2.3in")


def wire(target, m, L0, d, Y, ask="dl"):
    """2015 Exam 3 #5 and Ch 12 notes p. 10/10: Y = (F/A)/(dl/l)."""
    if ask != "dl":
        banned("wire solved for Y: 2015 #5 only solves for the stretch")
    F = m * g
    A = pi * (d / 2) ** 2
    dl = F * L0 / (A * Y)
    mm = dl < 0.02
    if ask == "dl":
        val = dl
        mistakes = [(dl / 4, "uses the diameter as the radius in $A = \\pi r^2$."),
                    (dl / g, "forgets $g$ (uses the mass instead of the weight)."),
                    (dl * pi / 4, "uses $A = d^2$ (no $\\pi$, no half)."),
                    (dl * 4, "uses $r = d/4$ (halves the radius twice)."),
                    (dl / L0, "finds the strain $\\Delta\\ell/\\ell$ and stops.")]
        unit, scale = ("mm", 1e3) if mm else ("m", 1)
        choices, nums, distract = numeric(val, mistakes, target, unit, scale=scale)
        stem = (f"A {N(m)} kg load hangs from a circular wire {N(L0)} m long with a diameter of {N(d)} m and a Young's modulus of "
                f"${N(Y)}$ N/m². By how much does the wire stretch?")
        nums_chk = nums
        val_chk = val * scale
    else:
        val = Y
        mistakes = [(Y * 4 if False else Y / 4, "uses the diameter as the radius."), (Y / g, "forgets $g$."),
                    (Y * pi / 4, "uses $A = d^2$."), (Y * 4, "uses $r = d/4$.")]
        choices, nums, distract = numeric(val, mistakes, target, "N/m²")
        stem = (f"A {N(m)} kg load hangs from a circular wire {N(L0)} m long with a diameter of {N(d)} m. The wire stretches "
                f"{plain(dl * 1e3)} mm. What is the Young's modulus of the wire?")
        nums_chk, val_chk = nums, val
    sol = T(r"""
**Step 1: the formula** (Ch 12 notes p. 10/10):

$$
Y = \frac{\text{tensile stress}}{\text{tensile strain}} = \frac{F/A}{\Delta\ell/\ell}
$$

**Step 2: the pieces.** The force is the load's weight, and the area is the wire's circular cross-section (radius = half the diameter):

$$
F = mg = (<<m>>)(9.8) = <<F>>\ \text{N}
$$

$$
A = \pi r^2 = \pi\Big(\underbrace{\tfrac{<<d>>}{2}}_{r}\Big)^2 = <<A>>\ \text{m}^2
$$
""", m=N(m), F=N(F, 4), d=N(d), A=N(A, 4))
    if ask == "dl":
        sol += T(r"""
**Step 3: solve for the stretch:**

$$
\Delta\ell = \frac{F\,\ell}{A\,Y} = \frac{\underbrace{(<<F>>)}_{F}\underbrace{(<<L>>)}_{\ell}}{\underbrace{(<<A>>)}_{A}\underbrace{(<<Y>>)}_{Y}} = <<dl>>\ \text{m}
$$
""", F=N(F, 4), L=N(L0), A=N(A, 4), Y=N(Y), dl=N(dl, 3))
    else:
        sol += T(r"""
**Step 3: solve for $Y$** ($\Delta\ell = <<dl>>$ m):

$$
Y = \frac{F\,\ell}{A\,\Delta\ell} = \frac{(<<F>>)(<<L>>)}{(<<A>>)(<<dl>>)} = <<Y>>\ \text{N/m}^2
$$
""", F=N(F, 4), L=N(L0), A=N(A, 4), dl=N(dl, 3), Y=N(Y, 3))
    return rec(stem=stem, choices=choices, key=target, check=("near", val_chk, nums_chk),
               topic="Young's modulus, wire" + (" stretch" if ask == "dl" else " (find Y)"),
               source_short="Ch 12 p. 10; 2015 #5",
               source="Ch 12 notes p. 10/10 (Young's modulus $Y = \\frac{F/A}{\\Delta\\ell/\\ell}$).",
               prev="2015 Exam 3 #5 (500 kg, 4.00 m, 0.001 m diameter, $8\\times10^{10}$: 0.312 m $\\rightarrow$ e) 0.3 m), new numbers",
               card="Moduli", tests="tensile stress/strain with a circular cross-section ($r = d/2$).",
               solution=sol, distract=distract)


def block_compress(target, m, w, l, h, Y, what="jello"):
    """2015 Exam 3 #4: block w x l x h compressed by mass m on top."""
    F = m * g
    A = w * l
    dh = F * h / (A * Y)
    mistakes = [(dh / g, "forgets $g$."), (F * h / (w * h * Y), "uses a side face ($w \\times h$) as the area."),
                (dh / h, "finds the strain and stops (forgets to multiply by the height)."),
                (F * h / (l * h * Y), "uses the other side face ($l \\times h$).")]
    choices, nums, distract = numeric(dh, mistakes, target, "mm", scale=1e3)
    stem = (f"A block of {what} with $Y = {N(Y)}$ N/m² is {N(w)} m wide, {N(l)} m long and {N(h)} m high. "
            f"A {N(m)} kg mass resting on top compresses it. By how much does the height shrink?")
    sol = T(r"""
**Step 1: the formula** (Ch 12 notes p. 10/10), with compression instead of stretch:

$$
Y = \frac{F/A}{\Delta h/h} \;\Rightarrow\; \Delta h = \frac{F\,h}{A\,Y}
$$

**Step 2: the pieces.** The mass pushes down on the **top** face, so $A$ = width × length. $h$ is the original height.

$$
F = (<<m>>)(9.8) = <<F>>\ \text{N}
$$

$$
A = (<<w>>)(<<l>>) = <<A>>\ \text{m}^2
$$

**Step 3: plug in:**

$$
\Delta h = \frac{\underbrace{(<<F>>)}_{F}\underbrace{(<<h>>)}_{h}}{\underbrace{(<<A>>)}_{\text{top area}}\underbrace{(<<Y>>)}_{Y}} = <<dh>>\ \text{m} = <<dhmm>>\ \text{mm}
$$
""", m=N(m), F=N(F, 4), w=N(w), l=N(l), A=N(A, 4), h=N(h), Y=N(Y), dh=N(dh, 3), dhmm=N(dh * 1e3, 3))
    return rec(stem=stem, choices=choices, key=target, check=("near", dh * 1e3, nums),
               topic=f"Young's modulus, compressed block", source_short="2015 #4; Ch 12 p. 10",
               source="2015 Exam 3 #4, solved with Young's modulus from Ch 12 notes p. 10/10.",
               prev="2015 Exam 3 #4 (jello 3 m × 4 m × 0.1 m, 500 kg: 1.36 mm $\\rightarrow$ e) 1.3 mm), new numbers",
               card="Moduli", tests="compressive stress on the top face, strain = $\\Delta h/h$.",
               solution=sol, distract=distract)


def shear(target, F, side, S, Y, metal="tungsten"):
    """Ch 12 notes p. 10/10: S = (F/A)/(dx/h). Cube of side `side`; force on the top face."""
    banned("shear modulus: formula only on Ch 12 p. 10, no worked problem in the notes or 2015 exam")
    A = side ** 2
    h = side
    dx = F * h / (A * S)
    mistakes = [(F * h / (A * Y), "uses Young's modulus $Y$ instead of the shear modulus $S$."),
                (F / (A * S), "finds the strain $\\Delta x/h$ and stops."),
                (F * h / (A * S) * 4, "uses half the side for the area."),
                (F * h / (A * S) / 4, "uses twice the side for the area.")]
    choices, nums, distract = numeric(dx, mistakes, target, "m")
    stem = (f"A {metal} cube {N(side)} m on a side is glued to the floor. A force of ${N(F)}$ N pushes sideways on its top face "
            f"(parallel to the face). For {metal}, $Y = {N(Y)}$ N/m² and $S = {N(S)}$ N/m². How far does the top face move sideways?")
    sol = T(r"""
**Step 1: which modulus?** A force **parallel** to a face is a shear (notes p. 10/10, the sketch with $F$ along the top and $\Delta x$). Use the shear modulus $S$, not $Y$:

$$
S = \frac{\text{shear stress}}{\text{shear strain}} = \frac{F/A}{\Delta x/h} \;\Rightarrow\; \Delta x = \frac{F\,h}{A\,S}
$$

**Step 2: plug in** (top face area $A = <<s>>^2 = <<A>>$ m², height $h = <<s>>$ m):

$$
\Delta x = \frac{\underbrace{(<<F>>)}_{F}\underbrace{(<<s>>)}_{h}}{\underbrace{(<<A>>)}_{A}\underbrace{(<<S>>)}_{S}} = <<dx>>\ \text{m}
$$
""", s=N(side), A=N(A, 4), F=N(F), S=N(S), dx=N(dx, 3))
    return rec(stem=stem, choices=choices, key=target, check=("near", dx, nums),
               topic="Shear modulus", source_short="Ch 12 p. 10",
               source="Ch 12 notes p. 10/10 (shear $S = \\frac{F/A}{\\Delta x/h}$; tungsten $Y = 35\\times10^{10}$, $S = 14\\times10^{10}$).",
               card="Moduli", tests="picking the shear modulus for a sideways force, $\\Delta x = Fh/(AS)$.",
               solution=sol, distract=distract)


def bulk(target, P, V0, B, Y, metal="tungsten"):
    """Ch 12 notes p. 10/10: B = -P/(dV/V0)."""
    banned("bulk modulus: formula only on Ch 12 p. 10, no worked problem")
    dV = P * V0 / B
    mistakes = [(P * V0 / Y, "uses Young's modulus instead of the bulk modulus."),
                (P / B, "finds the volume strain $\\Delta V/V_0$ and stops."),
                (P * V0 / B * 10, "slips a power of ten."), (P * V0 / B / 10, "slips a power of ten.")]
    choices, nums, distract = numeric(dV, mistakes, target, "m³")
    stem = (f"A {N(V0)} m³ block of {metal} ($Y = {N(Y)}$ N/m², $B = {N(B)}$ N/m²) is put under an extra pressure of "
            f"${N(P)}$ N/m² on all sides. By how much does its volume shrink?")
    sol = T(r"""
**Step 1: which modulus?** Pressure squeezing from all sides changes the volume: the bulk modulus (notes p. 10/10):

$$
B = \frac{\text{volume stress}}{\text{volume strain}} = \frac{-P}{\Delta V/V_0} \;\Rightarrow\; |\Delta V| = \frac{P\,V_0}{B}
$$

**Step 2: plug in:**

$$
|\Delta V| = \frac{\underbrace{(<<P>>)}_{P}\underbrace{(<<V>>)}_{V_0}}{\underbrace{(<<B>>)}_{B}} = <<dV>>\ \text{m}^3
$$

The minus sign in the formula just says the volume goes down when pressure goes up.
""", P=N(P), V=N(V0), B=N(B), dV=N(dV, 3))
    return rec(stem=stem, choices=choices, key=target, check=("near", dV, nums),
               topic="Bulk modulus", source_short="Ch 12 p. 10",
               source="Ch 12 notes p. 10/10 (bulk $B = \\frac{-\\Delta F/A}{\\Delta V/V_0} = \\frac{-P}{\\Delta V/V_0}$; tungsten $B = 20\\times10^{10}$).",
               card="Moduli", tests="picking the bulk modulus for pressure on all sides.",
               solution=sol, distract=distract)


# =====================================================================
# Chapter 13 — Gravity
# =====================================================================

def g_altitude(target, h, mass=None, ask="g", gt=None):
    """Notes Ch 13 p. 1/10 (g = GM/R^2) with r = R + h; 2015 Exam 3 #12."""
    if ask != "g":
        banned("height for a given g: 2015 #12 only asks for g")
    GM = G * ME
    if ask == "g":
        r = RE + h
        val = GM / r ** 2
        mistakes = [(GM / RE ** 2, "uses $R_{earth}$ (surface $g$), ignoring the height."),
                    (GM / h ** 2 if GM / h ** 2 < 2000 else None, "uses $h$ instead of $R + h$ (the 2015 exam's e) 700 m/s² is this mistake)."),
                    (GM / (RE ** 2 + h ** 2), "adds the squares, $R^2 + h^2$, instead of squaring $R + h$."),
                    (g * RE / r, "scales by $R/(R+h)$ without squaring.")]
        choices, nums, distract = numeric(val, mistakes, target, "m/s²")
        who = f" on a {N(mass)} kg astronaut" if mass else ""
        stem = f"What is the acceleration due to gravity{who} at a height of {N(h / 1e3)} km above the Earth's surface?"
        sol = T(r"""
**Step 1: the formula** (notes p. 1/10): $mg = \dfrac{GMm}{R^2}$, so $g = \dfrac{GM}{R^2}$ at the surface. Above the surface the distance is measured from Earth's **center**: $r = R + h$ (notes p. 2/10).

$$
g = \frac{GM_{earth}}{(R + h)^2}
$$

**Step 2: distance from the center:**

$$
r = \underbrace{6.37\times10^{6}}_{R_{earth}} + \underbrace{<<h>>}_{h\ \text{in m}} = <<r>>\ \text{m}
$$

**Step 3: plug in:**

$$
g = \frac{\underbrace{(6.67\times10^{-11})}_{G}\underbrace{(5.98\times10^{24})}_{M_{earth}}}{(<<r>>)^2} = <<g>>\ \text{m/s}^2
$$
""", h=N(h), r=N(r, 4), g=N(val, 3))
        if mass:
            sol += "\nThe person's mass cancels ($mg = GMm/r^2$); it's extra information.\n"
        topic = "$g$ at an altitude"
    else:
        val = sqrt(GM / gt) - RE
        mistakes = [(sqrt(GM / gt), "gives $r$, the distance from Earth's center; forgets to subtract $R$."),
                    (RE * (g / gt - 1), "uses $g \\propto 1/r$ instead of $1/r^2$."),
                    (RE * (sqrt(g / gt)), "gives $r$ found from the ratio $\\sqrt{g/g'}$ without subtracting $R$.")]
        choices, nums, distract = numeric(val, mistakes, target, "km", scale=1e-3)
        stem = f"At what height above the Earth's surface is the acceleration due to gravity {N(gt)} m/s²?"
        sol = T(r"""
**Step 1: the formula** (notes p. 1/10), with $r = R + h$ measured from Earth's center (p. 2/10):

$$
g' = \frac{GM}{r^2} \;\Rightarrow\; r = \sqrt{\frac{GM}{g'}}
$$

**Step 2: plug in:**

$$
r = \sqrt{\frac{\underbrace{(6.67\times10^{-11})(5.98\times10^{24})}_{GM_{earth}}}{\underbrace{<<gt>>}_{g'}}} = <<r>>\ \text{m}
$$

**Step 3: subtract Earth's radius** to get the height above the surface:

$$
h = r - R = <<r>> - 6.37\times10^{6} = <<h>>\ \text{m} = <<hk>>\ \text{km}
$$
""", gt=N(gt), r=N(sqrt(GM / gt), 4), h=N(val, 3), hk=N(val / 1e3, 3))
        topic = "Height where $g$ has a given value"
    return rec(stem=stem, choices=choices, key=target, check=("near", val if ask == "g" else val / 1e3, nums),
               topic=topic, source_short="Ch 13 p. 1–2; 2015 #12",
               source="Ch 13 notes p. 1/10 ($g = GM_E/R_E^2 = 9.81$ m/s²) and p. 2/10 ($r = R + h$).",
               prev="2015 Exam 3 #12 (750 km: 7.87 m/s² $\\rightarrow$ b) 8 m/s²), new numbers",
               card="Gravity", tests="$g = GM/r^2$ with $r$ measured from Earth's center.",
               solution=sol, distract=distract)


def newton_force(target, m1, m2, r, desc, names=("", "")):
    """Notes Ch 13 p. 1/10: F = G M1 M2 / r^2 (with M_moon = M_earth/80, d_EM = 4e8 m, M_sun = 2e30, d_ES = 1.5e11)."""
    banned("F = GMm/r^2 force between two bodies: never worked as a problem in the notes or 2015 exam")
    F = G * m1 * m2 / r ** 2
    mistakes = [(G * m1 * m2 / r, "doesn't square $r$."), (G * m1 * m2 / (r / 1e3) ** 2, "leaves $r$ in km."),
                (G * m1 * m2 / (2 * r) ** 2, "uses $2r$."), (G * m1 * m2 / (r / 2) ** 2, "uses $r/2$.")]
    choices, nums, distract = numeric(F, mistakes, target, "N")
    stem = desc
    sol = T(r"""
**Newton's law of gravitation** (notes p. 1/10):

$$
F = \frac{G M_1 M_2}{r^2}
$$

with $r$ the center-to-center distance.

$$
F = \frac{\underbrace{(6.67\times10^{-11})}_{G}\underbrace{(<<m1>>)}_{M_1}\underbrace{(<<m2>>)}_{M_2}}{\underbrace{(<<r>>)^2}_{r^2}} = <<F>>\ \text{N}
$$
""", m1=N(m1), m2=N(m2), r=N(r), F=N(F, 3))
    return rec(stem=stem, choices=choices, key=target, check=("near", F, nums),
               topic="Newton's law of gravity", source_short="Ch 13 p. 1",
               source="Ch 13 notes p. 1/10 ($F = GM_1M_2/r^2$; $M_{moon} = M_{earth}/80$, $d_{EM} = 4\\times10^8$ m, $M_{sun} = 2\\times10^{30}$ kg, $d_{ES} = 1.5\\times10^{11}$ m).",
               card="Gravity", tests="$F = GMm/r^2$ with $r$ in meters, squared.",
               solution=sol, distract=distract)


def sat_period(target, h, unit="min", mass=None):
    """Notes Ch 13 p. 2/10: T^2 = 4 pi^2 r^3 / GM, r = R + h; 2015 Exam 3 #10."""
    GM = G * ME
    sc = {"min": 1 / 60, "hr": 1 / 3600, "day": 1 / 86400}[unit]
    uname = {"min": "min", "hr": "hours", "day": "days"}[unit]
    r = RE + h
    Tp = 2 * pi * sqrt(r ** 3 / GM)
    mistakes = [(2 * pi * sqrt(h ** 3 / GM), "uses $h$ instead of $r = R + h$."),
                (sqrt(r ** 3 / GM), "drops the $4\\pi^2$ (forgets the $2\\pi$ in $v = 2\\pi r/T$)."),
                (2 * pi * sqrt(RE ** 3 / GM), "uses $R_{earth}$ (an orbit skimming the surface)."),
                (4 * pi ** 2 * r ** 3 / GM / 3600 if False else pi * sqrt(r ** 3 / GM), "uses $\\pi$ instead of $2\\pi$.")]
    choices, nums, distract = numeric(Tp, mistakes, target, uname, scale=sc)
    who = f" (mass {N(mass)} kg)" if mass else ""
    stem = f"What is the period of a satellite{who} in a circular orbit around the Earth at an altitude of {plain(h / 1e3)} km above the Earth's surface?"
    sol = T(r"""
**Step 1: gravity supplies the centripetal force** (notes p. 2/10):

$$
\frac{GMm}{r^2} = \frac{mv^2}{r},\qquad v = \frac{2\pi r}{T}\;\Rightarrow\; T^2 = \frac{4\pi^2 r^3}{GM}
$$

The satellite's mass $m$ cancels.

**Step 2: orbit radius from Earth's center:**

$$
r = \underbrace{6.37\times10^{6}}_{R} + \underbrace{<<h>>}_{h} = <<r>>\ \text{m}
$$

**Step 3: plug in:**

$$
T = \sqrt{\frac{4\pi^2(<<r>>)^3}{\underbrace{(6.67\times10^{-11})(5.98\times10^{24})}_{GM_{earth}}}} = <<Ts>>\ \text{s}
$$

**Step 4: convert:** $<<Ts>>\ \text{s} = <<Tu>>$ <<uname>>.
""", h=N(h), r=N(r, 4), Ts=N(Tp, 4), Tu=N(Tp * sc, 3), uname=uname)
    sol += "\nNotes example: $h = 400$ km gives $T = 5546$ s = 92.4 min (low Earth orbit).\n"
    return rec(stem=stem, choices=choices, key=target, check=("near", Tp * sc, nums),
               topic="Satellite period", source_short="Ch 13 p. 2; 2015 #10",
               source="Ch 13 notes p. 2/10 (satellite orbiting a planet, $T^2 = 4\\pi^2r^3/GM$, $r = R + h$; $h = 400$ km $\\rightarrow$ 92.4 min).",
               prev="2015 Exam 3 #10 (altitude $10^8$ m: 3.99 days $\\rightarrow$ d) 4 days), new numbers",
               card="Orbit", tests="$T^2 = 4\\pi^2r^3/GM$ with $r = R + h$.",
               solution=sol, distract=distract, fig=figs3.orbit(), figsize=(2.4, 2.0), figwidth="1.5in")


def orbit_speed(target, h):
    """Notes Ch 13 p. 2/10 (GM/r = v^2) and p. 10/10 (v = sqrt(GM/r)) for an Earth satellite."""
    banned("satellite orbital speed: never worked as a problem (p. 10 does planets around the Sun)")
    GM = G * ME
    r = RE + h
    v = sqrt(GM / r)
    mistakes = [(sqrt(2 * GM / r), "is $\\sqrt{2GM/r}$, the escape-speed formula."),
                (sqrt(GM / RE), "uses $R$ instead of $R + h$."),
                (sqrt(GM / h) if h > 1e6 else None, "uses $h$ instead of $R + h$."),
                (GM / r / 1e3, "forgets the square root.")]
    choices, nums, distract = numeric(v, mistakes, target, "km/s", scale=1e-3)
    stem = f"How fast does a satellite move in a circular orbit {plain(h / 1e3)} km above the Earth's surface?"
    sol = T(r"""
**Step 1:** gravity is the centripetal force (notes p. 2/10 and p. 10/10):

$$
\frac{GMm}{r^2} = \frac{mv^2}{r} \;\Rightarrow\; v = \sqrt{\frac{GM}{r}}
$$

**Step 2:** $r = R + h = 6.37\times10^{6} + <<h>> = <<r>>$ m.

**Step 3: plug in:**

$$
v = \sqrt{\frac{\underbrace{(6.67\times10^{-11})(5.98\times10^{24})}_{GM_{earth}}}{\underbrace{<<r>>}_{r}}} = <<v>>\ \text{m/s} = <<vk>>\ \text{km/s}
$$
""", h=N(h), r=N(r, 4), v=N(v, 4), vk=N(v / 1e3, 3))
    return rec(stem=stem, choices=choices, key=target, check=("near", v / 1e3, nums),
               topic="Orbital speed of a satellite", source_short="Ch 13 p. 2, 10",
               source="Ch 13 notes p. 2/10 ($GM/r = v^2$) and p. 10/10 (orbital speed $v = \\sqrt{GM/r}$).",
               card="Orbit", tests="$v = \\sqrt{GM/r}$ with $r = R + h$.", solution=sol, distract=distract)


def orbit_from_period(target, T_hr):
    """Notes Ch 13 p. 3/10 (geosynchronous): r = (T^2 GM / 4 pi^2)^(1/3), h = r - R."""
    GM = G * ME
    Ts = T_hr * 3600
    r = (Ts ** 2 * GM / (4 * pi ** 2)) ** (1 / 3)
    h = r - RE
    mistakes = [(r, "gives $r$ (from Earth's center); forgets to subtract $R$."),
                ((Ts ** 2 * GM) ** (1 / 3) - RE, "drops the $4\\pi^2$."),
                ((Ts ** 2 * GM / (2 * pi ** 2)) ** (1 / 3) - RE if False else ((Ts ** 2 * GM / (4 * pi ** 2)) ** 0.5 / 1e3 if (Ts ** 2 * GM / (4 * pi ** 2)) ** 0.5 / 1e3 > h * 1.3 else None), "takes a square root instead of a cube root."),
                (((Ts / 2) ** 2 * GM / (4 * pi ** 2)) ** (1 / 3) - RE, "uses half the period.")]
    choices, nums, distract = numeric(h, mistakes, target, "km", scale=1e-3)
    stem = (f"A satellite is to circle the Earth once every {N(T_hr)} hours. At what altitude above the Earth's surface must it orbit?")
    sol = T(r"""
**Step 1: solve the period formula for $r$** (notes p. 3/10, geosynchronous orbit):

$$
T^2 = \frac{4\pi^2r^3}{GM} \;\Rightarrow\; r = \left(\frac{T^2GM}{4\pi^2}\right)^{1/3}
$$

**Step 2: period in seconds:** $T = <<Th>>\ \text{h} \times 3600\ \text{s/h} = <<Ts>>$ s.

**Step 3: plug in:**

$$
r = \left(\frac{\underbrace{(<<Ts>>)^2}_{T^2}\underbrace{(6.67\times10^{-11})(5.98\times10^{24})}_{GM_{earth}}}{4\pi^2}\right)^{1/3} = <<r>>\ \text{m}
$$

**Step 4: altitude above the surface:**

$$
h = r - R = <<r>> - 6.37\times10^{6} = <<h>>\ \text{m} = <<hk>>\ \text{km}
$$

Notes example: $T = 24$ h gives $r = 4.22\times10^{7}$ m and $h = 35{,}900$ km.
""", Th=N(T_hr), Ts=N(Ts, 4), r=N(r, 4), h=N(h, 3), hk=N(h / 1e3, 3))
    return rec(stem=stem, choices=choices, key=target, check=("near", h / 1e3, nums),
               topic="Orbit altitude from the period", source_short="Ch 13 p. 3",
               source="Ch 13 notes p. 3/10 (geosynchronous orbit: $T = 24$ h $\\rightarrow$ $r = 4.22\\times10^7$ m, $h = 35{,}900$ km).",
               card="Orbit", tests="the geosynchronous-orbit procedure (notes p. 3): $r = (T^2GM/4\\pi^2)^{1/3}$, then $h = r - R$.",
               solution=sol, distract=distract)


def binary(target, M, d, unit="day", give="d"):
    """Notes Ch 13 p. 4/10: T^2 = 16 pi^2 r^3 / GM with r = d/2; 2015 Exam 3 #11."""
    sc = {"s": 1, "min": 1 / 60, "hr": 1 / 3600, "day": 1 / 86400, "yr": 1 / (86400 * 365)}[unit]
    uname = {"s": "s", "min": "min", "hr": "hours", "day": "days", "yr": "years"}[unit]
    r = d / 2
    Tp = sqrt(16 * pi ** 2 * r ** 3 / (G * M))
    mistakes = [(sqrt(16 * pi ** 2 * d ** 3 / (G * M)), "uses the separation $d$ as the orbit radius (the notes warn: separation is $2r$, not $r$)."),
                (sqrt(4 * pi ** 2 * r ** 3 / (G * M)), "uses the single-planet $4\\pi^2$ formula (forgets that the separation is $2r$ in the force)."),
                (sqrt(4 * pi ** 2 * d ** 3 / (G * M)), "uses the single-planet formula with $r = d$."),
                (sqrt(16 * pi ** 2 * r ** 3 / (G * 2 * M)), "uses $2M$ for the mass.")]
    choices, nums, distract = numeric(Tp, mistakes, target, uname, scale=sc)
    if give == "d":
        stem = (f"Two equal-mass stars (${N(M)}$ kg each) orbit their common center of mass, halfway between them. "
                f"Their separation is $d = {N(d)}$ m. What is the period of their orbit?")
    else:
        stem = (f"Two stars, each with the mass of the Sun (${N(M)}$ kg), circle their common center of mass. Each star moves on a "
                f"circle of radius ${N(r)}$ m. What is the period?")
    sol = T(r"""
**Step 1: the force uses the separation, the circle uses $r$** (notes p. 4/10). Each star moves on a circle of radius $r$ about the center; the distance between the stars is $2r$:

$$
\frac{GM^2}{(2r)^2} = \frac{Mv^2}{r},\qquad v = \frac{2\pi r}{T}\;\Rightarrow\; T^2 = \frac{16\pi^2 r^3}{GM}
$$

**Step 2: the orbit radius:** $r = <<rtxt>>$.

**Step 3: plug in:**

$$
T = \sqrt{\frac{16\pi^2(<<r>>)^3}{\underbrace{(6.67\times10^{-11})}_{G}\underbrace{(<<M>>)}_{M}}} = <<Ts>>\ \text{s} = <<Tu>>\ \text{<<uname>>}
$$

Notes example: $M = 2\times10^{30}$ kg, $r = 6\times10^{10}$ m gives 185 days.
""", rtxt=(rf"d/2 = {N(r)}\ \text{{m}}" if give == "d" else rf"{N(r)}\ \text{{m}}\ (\text{{given}})"),
          r=N(r), M=N(M), Ts=N(Tp, 4), Tu=N(Tp * sc, 3), uname=uname)
    return rec(stem=stem, choices=choices, key=target, check=("near", Tp * sc, nums),
               topic="Binary stars, period", source_short="Ch 13 p. 4" + ("; 2015 #11" if give == "d" else ""),
               source="Ch 13 notes p. 4/10 (two equal-mass stars, $T^2 = 16\\pi^2r^3/GM$; \"separation btwn the masses is $2r$ (not $r$)\").",
               prev="2015 Exam 3 #11 ($10^{31}$ kg each, $d = 10^8$ m: 2.9 min $\\rightarrow$ a) 3 minutes), new numbers" if give == "d" else None,
               card="Binary stars", tests="$T^2 = 16\\pi^2r^3/GM$ with $r$ = half the separation.",
               solution=sol, distract=distract, fig=figs3.binary(r"$d$" if give == "d" else r"$2r$"), figsize=(2.4, 2.0), figwidth="1.5in")


def rocket_speed(target, h):
    """Notes Ch 13 p. 8/10: v = sqrt(2GM(1/R - 1/r)); 2015 Exam 3 #9."""
    GM = G * ME
    r = RE + h
    v = sqrt(2 * GM * (1 / RE - 1 / r))
    mistakes = [(sqrt(2 * g * h), "uses $mgh$ (constant $g$), which is wrong this far up."),
                (sqrt(GM * (1 / RE - 1 / r)), "forgets the 2 from $\\tfrac12mv^2$."),
                (sqrt(GM / r), "is the orbital speed at that height, not the launch speed."),
                (sqrt(2 * GM / RE), "is the escape speed.")]
    choices, nums, distract = numeric(v, mistakes, target, "km/s", scale=1e-3)
    stem = f"A rocket fired straight up from the Earth's surface rises to a maximum height of {plain(h / 1e3)} km. At what speed was it launched? (Ignore air resistance.)"
    sol = T(r"""
**Step 1: conservation of energy** (notes p. 7–8/10). At launch $r = R$, speed $v$; at the top $r = R + h$, speed 0. Gravitational PE is $U = -GMm/r$:

$$
-\frac{GMm}{R} + \frac12mv^2 = -\frac{GMm}{r} \;\Rightarrow\; v = \sqrt{2GM\Big(\frac1R - \frac1r\Big)}
$$

**Step 2: top of the flight:** $r = R + h = 6.37\times10^{6} + <<h>> = <<r>>$ m.

**Step 3: plug in:**

$$
v = \sqrt{2\,\underbrace{(6.67\times10^{-11})(5.98\times10^{24})}_{GM_{earth}}\Big(\underbrace{\frac{1}{6.37\times10^{6}}}_{1/R} - \underbrace{\frac{1}{<<r>>}}_{1/r}\Big)} = <<v>>\ \text{m/s} = <<vk>>\ \text{km/s}
$$

Notes example: $h = 1000$ km needs $v = 4119$ m/s.
""", h=N(h), r=N(r, 4), v=N(v, 4), vk=N(v / 1e3, 3))
    return rec(stem=stem, choices=choices, key=target, check=("near", v / 1e3, nums),
               topic="Launch speed to reach a height", source_short="Ch 13 p. 7–8; 2015 #9",
               source="Ch 13 notes p. 7/10 ($U = -GMm/r$, energy conservation) and p. 8/10 (\"given a target altitude $h = 1000$ km, what $v$ to launch?\" 4119 m/s).",
               prev="2015 Exam 3 #9 (1000 km), new numbers",
               card="Rocket", tests="energy conservation with $U = -GMm/r$, solved for $v$.",
               solution=sol, distract=distract)


def rocket_height(target, v):
    """Notes Ch 13 p. 7-8/10: h = 2GMR/(2GM - v^2 R) - R."""
    GM = G * ME
    r = 2 * GM * RE / (2 * GM - v ** 2 * RE)
    h = r - RE
    mistakes = [(v ** 2 / (2 * g), "uses $mgh$ with constant $g$."), (r, "gives $r$, the distance from Earth's center; forgets to subtract $R$."),
                (GM * RE / (GM - v ** 2 * RE) - RE if GM - v ** 2 * RE > 0 else None, "forgets the $\\tfrac12$ in $\\tfrac12mv^2$."),
                (v ** 2 / g, "uses $v^2/g$.")]
    choices, nums, distract = numeric(h, mistakes, target, "km", scale=1e-3)
    stem = f"A rocket is launched straight up from the Earth's surface at {plain(v)} m/s. How high above the surface does it rise? (Ignore air resistance.)"
    sol = T(r"""
**Step 1: conservation of energy** (notes p. 7/10), launch at $r = R$ with speed $v_i$, top at $r$ with speed 0:

$$
-\frac{GMm}{R} + \frac12mv_i^2 = -\frac{GMm}{r} \;\Rightarrow\; r = \frac{1}{\frac1R - \frac{v_i^2}{2GM}} = \frac{2GMR}{2GM - v_i^2R}
$$

**Step 2: plug in** ($2GM = 2(6.67\times10^{-11})(5.98\times10^{24}) = <<2GM>>$):

$$
r = \frac{\underbrace{(<<2GM>>)}_{2GM}\underbrace{(6.37\times10^{6})}_{R}}{<<2GM>> - \underbrace{(<<v>>)^2}_{v_i^2}(6.37\times10^{6})} = <<r>>\ \text{m}
$$

**Step 3: height above the surface:**

$$
h = r - R = <<r>> - 6.37\times10^{6} = <<h>>\ \text{m} = <<hk>>\ \text{km}
$$

Keep at least 4 significant figures until the subtraction: $r$ and $R$ are close, so early rounding changes the answer. The notes' $v_i = 1000$ m/s example shows $h = 50.73$ km; carried through without rounding, it is 51.4 km.
""", **{"2GM": N(2 * GM, 4)}, v=N(v), r=N(r, 5), h=N(h, 3), hk=N(h / 1e3, 3))
    return rec(stem=stem, choices=choices, key=target, check=("near", h / 1e3, nums),
               topic="Height reached from the launch speed", source_short="Ch 13 p. 7–8",
               source="Ch 13 notes p. 7/10 and p. 8/10 (rocket launch $v_i = 1000$ m/s, $h = \\tfrac{2GMR}{2GM - v_i^2R} - R$).",
               card="Rocket", tests="energy conservation with $U = -GMm/r$, solved for $h$.",
               solution=sol, distract=distract)


def escape(target, M, R, body):
    """Notes Ch 13 p. 9/10: v_esc = sqrt(2GM/R)."""
    v = sqrt(2 * G * M / R)
    mistakes = [(sqrt(G * M / R), "forgets the 2 (that is the orbital speed at the surface)."),
                (sqrt(2 * G * M / (2 * R)), "uses the diameter."), (2 * G * M / R / 1e3 if 2 * G * M / R / 1e3 < 1e3 else None, "forgets the square root."),
                (sqrt(2 * G * M / R) * 2, "doubles the answer.")]
    choices, nums, distract = numeric(v, mistakes, target, "km/s", scale=1e-3)
    stem = f"What is the escape speed from the surface of {body} (mass ${N(M)}$ kg, radius ${N(R)}$ m)?"
    sol = T(r"""
**Step 1: energy conservation** (notes p. 9/10). To escape, the object just reaches $r = \infty$ with $v = 0$, where $U = 0$ and $K = 0$:

$$
-\frac{GMm}{R} + \frac{mv^2}{2} = 0 + 0 \;\Rightarrow\; v_{esc} = \sqrt{\frac{2GM}{R}}
$$

**Step 2: plug in:**

$$
v_{esc} = \sqrt{\frac{2\,\underbrace{(6.67\times10^{-11})}_{G}\underbrace{(<<M>>)}_{M}}{\underbrace{<<R>>}_{R}}} = <<v>>\ \text{m/s} = <<vk>>\ \text{km/s}
$$

For Earth the notes get 11,181 m/s, about 11.2 km/s.
""", M=N(M), R=N(R), v=N(v, 4), vk=N(v / 1e3, 3))
    return rec(stem=stem, choices=choices, key=target, check=("near", v / 1e3, nums),
               topic="Escape speed", source_short="Ch 13 p. 9",
               source="Ch 13 notes p. 9/10 ($v_{escape} = \\sqrt{2GM/R}$ = 11.2 km/s for Earth).",
               card="Escape", tests="$v_{esc} = \\sqrt{2GM/R}$.", solution=sol, distract=distract)


def event_horizon(target, M, desc):
    """Notes Ch 13 p. 9/10: r = 2GM/c^2."""
    r = 2 * G * M / C_LIGHT ** 2
    mistakes = [(G * M / C_LIGHT ** 2, "forgets the 2."), (2 * G * M / C_LIGHT, "doesn't square $c$."),
                (sqrt(2 * G * M) / C_LIGHT, "takes a square root."), (4 * G * M / C_LIGHT ** 2, "uses $4GM$.")]
    choices, nums, distract = numeric(r, [(v, w) for v, w in mistakes if v / r < 1e3], target, "m")
    stem = f"{desc} If its escape speed equals the speed of light ($c = 3\\times10^{{8}}$ m/s), what is the radius of its event horizon?"
    sol = T(r"""
**Set $v_{escape} = c$** (notes p. 9/10). Then $r$ is the radius of the event horizon:

$$
c^2 = \frac{2GM}{r} \;\Rightarrow\; r = \frac{2GM}{c^2}
$$

$$
r = \frac{2\,\underbrace{(6.67\times10^{-11})}_{G}\underbrace{(<<M>>)}_{M}}{\underbrace{(3\times10^{8})^2}_{c^2}} = <<r>>\ \text{m}
$$

Notes example: $M = 10^{37}$ kg gives $r = 1.48\times10^{10}$ m, about $\tfrac{1}{10}$ the radius of Earth's orbit.
""", M=N(M), r=N(r, 3))
    return rec(stem=stem, choices=choices, key=target, check=("near", r, nums),
               topic="Event horizon radius", source_short="Ch 13 p. 9",
               source="Ch 13 notes p. 9/10 (\"if $v_{escape} = c$ … $r$ is the radius of the event horizon\", $r = 2GM/c^2$).",
               card="Escape", tests="setting $v_{esc} = c$: $r = 2GM/c^2$.", solution=sol, distract=distract)


def planet_speed(target, a_au, name):
    """Notes Ch 13 p. 10/10: v = sqrt(GM_sun/r), 1 AU = 1.5e11 m, M_sun = 2e30 kg."""
    r = a_au * AU
    v = sqrt(G * M_SUN / r)
    mistakes = [(sqrt(2 * G * M_SUN / r), "uses $\\sqrt{2GM/r}$ (escape speed)."), (sqrt(G * M_SUN / AU), "uses 1 AU (Earth's distance)."),
                (sqrt(G * M_SUN / r) * sqrt(a_au) if a_au > 1.5 or a_au < 0.67 else None, "multiplies by $\\sqrt{r}$ instead of dividing (uses Earth's speed times $\\sqrt{a}$)."),
                (G * M_SUN / r / 1e9 if False else None, "")]
    choices, nums, distract = numeric(v, mistakes, target, "km/s", scale=1e-3)
    stem = (f"{name} orbits the Sun at {N(a_au)} AU (1 AU $= 1.5\\times10^{{11}}$ m, $M_{{sun}} = 2\\times10^{{30}}$ kg). "
            f"Treating the orbit as a circle, what is its orbital speed?")
    sol = T(r"""
**Gravity is the centripetal force** (notes p. 10/10):

$$
\frac{GMm}{r^2} = \frac{mv^2}{r} \;\Rightarrow\; v = \sqrt{\frac{GM_{sun}}{r}}
$$

**Distance in meters:** $r = <<a>>\ \text{AU} \times 1.5\times10^{11}\ \text{m/AU} = <<r>>$ m.

$$
v = \sqrt{\frac{\underbrace{(6.67\times10^{-11})(2\times10^{30})}_{GM_{sun} = 1.33\times10^{20}}}{<<r>>}} = <<v>>\ \text{m/s} = <<vk>>\ \text{km/s}
$$

The notes' table on p. 10/10 gives Earth 29.8 km/s and Jupiter 13.1 km/s: "only a factor of 10" across the planets.
""", a=N(a_au), r=N(r, 4), v=N(v, 4), vk=N(v / 1e3, 3))
    return rec(stem=stem, choices=choices, key=target, check=("near", v / 1e3, nums),
               topic="Orbital speed of a planet", source_short="Ch 13 p. 10",
               source="Ch 13 notes p. 10/10 (orbital speed of planets, $v = \\sqrt{GM/r}$ with $GM_{sun} = 1.33\\times10^{20}$).",
               card="Planet speed", tests="$v = \\sqrt{GM/r}$ with $r$ converted from AU.", solution=sol, distract=distract)


def equal_pull(target, Mb, d, body="moon"):
    """2015 Exam 3 #13: point between Earth and a body where the pulls are equal."""
    k = sqrt(ME / Mb)
    f = k / (1 + k)
    mistakes = [(ME / (ME + Mb), "uses the mass ratio without the square root."),
                (0.5, "assumes the halfway point."), (1 / (1 + k), "gives the distance from the " + body + "'s center."),
                ((ME / Mb) ** (1 / 3) / (1 + (ME / Mb) ** (1 / 3)), "uses a cube root.")]
    choices, nums, distract = numeric(f, mistakes, target, "%", scale=100, gap=0.015, cap=100)
    choices = [c.replace(" %", "%") for c in choices]
    stem = (f"The Earth and the {body} (mass ${N(Mb)}$ kg) are {d / 1e3:,.0f} km apart, center to center. How far from the center of the Earth "
            f"toward the {body}, as a percentage of the Earth–{body} distance, is the point where the gravitational pull toward the Earth equals "
            f"the pull toward the {body}?")
    sol = T(r"""
**Step 1: set the two pulls equal** with Newton's law (Ch 13 notes p. 1/10). Let $x$ be the distance from Earth's center, so the distance to the <<b>> is $d - x$. The test mass $m$ cancels:

$$
\frac{GM_Em}{x^2} = \frac{GM_bm}{(d - x)^2} \;\Rightarrow\; \frac{x}{d - x} = \sqrt{\frac{M_E}{M_b}}
$$

**Step 2: the square root:**

$$
k = \sqrt{\frac{\overbrace{5.98\times10^{24}}^{M_E}}{\underbrace{<<Mb>>}_{M_b}}} = <<k>>
$$

**Step 3: solve for the fraction:** $x = k(d - x)$, so

$$
\frac{x}{d} = \frac{k}{1 + k} = \frac{<<k>>}{<<k1>>} = <<f>> = <<pct>>\%
$$

The distance doesn't matter for the percentage; only the mass ratio does.
""", b=body, Mb=N(Mb), k=N(k, 4), k1=N(1 + k, 4), f=N(f, 4), pct=N(100 * f, 3))
    return rec(stem=stem, choices=choices, key=target, check=("near", 100 * f, nums),
               topic="Equal-pull point", source_short="2015 #13; Ch 13 p. 1",
               source="2015 Exam 3 #13, solved with $F = GMm/r^2$ from Ch 13 notes p. 1/10.",
               prev="2015 Exam 3 #13 (moon $7\\times10^{22}$ kg, 400,000 km: 90.2% $\\rightarrow$ b) 90%), new numbers",
               card="Equal pull", tests="setting two inverse-square pulls equal: $x/d = k/(1+k)$, $k = \\sqrt{M_E/M_b}$.",
               solution=sol, distract=distract)


# =====================================================================
# Concept questions (each answer is stated or shown in the notes)
# =====================================================================

def c_diving_direction(target):
    banned("concept question: the live exam asks only the computational problems from the notes / 2015 exam")
    wrong = [("Up, with a force equal to the board's weight $Mg$", "$\\sum F_y$ then can't balance: B already pushes up with more than $Mg$."),
             ("Up, with a force larger than support B's", "The notes find $A = 4Mg$ pointing down and $B = 5Mg$ up."),
             ("Zero: support A carries no force", "Without A, the torque of $Mg$ about B would tip the board off B."),
             ("Up, with a force equal to support B's", "$\\sum\\tau_B = 0$ needs A to pull the back end down.")]
    choices, distract = place_text("Down, with magnitude $B - Mg$", wrong, target)
    sol = r"""
In the notes' FBD (p. 3/10) **A points down and B up**: $\sum F_y$: $B - A - Mg = 0$. The board's weight acts at its center, 5 m out, far past support B. Torque about B shows the back end would lift, so A must hold it **down**: $\sum\tau_B$: $1A - 4Mg = 0$, so $A = 4Mg$. With $B = 5Mg$, $A = B - Mg$.
"""
    return rec(stem="A uniform diving board rests on two supports near its back end: support A at the very back and support B a short distance in front of A. The rest of the board sticks out past B. In which direction does support A push on the board, and how big is that force?",
               choices=choices, key=target, check=("concept",), topic="Diving board, direction of A", source_short="Ch 12 p. 3",
               source="Ch 12 notes p. 3/10 (diving board FBD: A down, B up; $A = 4Mg$, $B = 5Mg$).",
               card="Diving board", tests="reading the diving-board FBD: the back support pulls down.", solution=sol, distract=distract)


def c_ladder_roof(target):
    banned("concept question: the live exam asks only the computational problems from the notes / 2015 exam")
    wrong = [("Make the ladder less steep (smaller $\\theta$)", "Smaller $\\theta$ means smaller $\\tan\\theta$, so $x$ goes down."),
             ("Use a floor with a smaller $\\mu_s$", "Smaller $\\mu_s$ means less friction, so $x$ goes down."),
             ("Move the ladder's base farther from the wall", "That makes $\\theta$ smaller, so $x$ goes down."),
             ("Nothing: $x$ depends only on the man's mass", "$x = \\tfrac{L}{M}(\\mu_s(M+m)\\tan\\theta - \\tfrac m2)$ depends on $\\mu_s$ and $\\theta$.")]
    choices, distract = place_text("Make the ladder steeper (larger $\\theta$)", wrong, target)
    sol = r"""
Notes p. 9/10, "What would get him to roof? increase $\mu_s$ or $\theta$." With $x = \frac{L}{M}\big(\mu_s(M+m)\tan\theta - \frac m2\big)$ from p. 8/10, raising $\theta$ from 65° to 70° moves him from 8.8 m to 11.4 m, and raising $\mu_s$ from 0.4 to 0.6 gets him to 13.4 m. Of the choices, only a steeper ladder helps.
"""
    return rec(stem="A man climbing a ladder that leans against a frictionless wall finds he can't reach the roof before the ladder would slip. Which change lets him climb higher?",
               choices=choices, key=target, check=("concept",), topic="What lets him climb higher?", source_short="Ch 12 p. 8–9",
               source="Ch 12 notes p. 9/10 (\"What would get him to roof? increase $\\mu_s$ or $\\theta$\").",
               card="Ladder", tests="how $x_{max}$ depends on $\\theta$ and $\\mu_s$.", solution=sol, distract=distract)


def c_kepler(target, factor=4):
    banned("concept question: the live exam asks only the computational problems from the notes / 2015 exam")
    t = factor ** 1.5
    nums = sorted(set([factor ** 0.5, factor, t, factor ** 2, factor ** 3]))
    assert len(nums) == 5
    k = LETTERS.index(target)
    # rotate so that t lands on target: use the 5 candidates in sorted order, drop/insert as needed
    cands = [factor ** 0.5, factor, factor ** 2, factor ** 3, factor ** 2.5, factor ** (2 / 3), factor ** 4, factor ** (1 / 3)]
    below = sorted([c for c in cands if c < t], reverse=True)[:k]
    above = sorted([c for c in cands if c > t])[:4 - k]
    assert len(below) == k and len(above) == 4 - k, (k, below, above)
    vals = sorted(below + [t] + above)
    choices = [f"{v:.3g} times" for v in vals]
    expl = {factor ** 0.5: "uses $T \\propto r^{1/2}$.", float(factor): "assumes $T \\propto r$.",
            float(factor ** 2): "uses $T \\propto r^2$.", float(factor ** 3): "forgets to take the square root ($T^2 \\propto r^3$ gives $T^2$, not $T$).",
            factor ** 2.5: "uses $T \\propto r^{5/2}$.", factor ** (1 / 3): "uses a cube root ($T \\propto r^{1/3}$).",
            factor ** (2 / 3): "flips the exponent ($T \\propto r^{2/3}$ instead of $r^{3/2}$).",
            float(factor ** 4): "uses $T \\propto r^4$."}
    distract = {}
    for i, v in enumerate(vals):
        if v != t:
            e = min(expl, key=lambda e: abs(e - v))
            assert abs(e - v) < 1e-9, (v, e)
            distract[LETTERS[i]] = expl[e]
    sol = rf"""
Notes p. 2/10: $T^2 = \dfrac{{4\pi^2r^3}}{{GM}}$, so $T^2 \propto r^3$. That's the straight line on Kepler's plot of $T^2$ vs $a^3$ (p. 5/10).

$$
\frac{{T_B}}{{T_A}} = \left(\frac{{r_B}}{{r_A}}\right)^{{3/2}} = {factor}^{{3/2}} = {plain(t, 3)}
$$
"""
    return rec(stem=f"Planet B orbits the same star as planet A, with an orbit radius {factor} times larger. How many times longer is planet B's period than planet A's?",
               choices=choices, key=target, check=("concept",), topic="Kepler: $T^2 \\propto a^3$", source_short="Ch 13 p. 2, 5",
               source="Ch 13 notes p. 5/10 (Kepler's $T^2$ vs $a^3$ plot is a straight line) and p. 2/10 ($T^2 = 4\\pi^2r^3/GM$).",
               card="Orbit", tests="scaling with $T^2 \\propto r^3$.", solution=sol, distract=distract)


def c_static(target):
    banned("concept question: the live exam asks only the computational problems from the notes / 2015 exam")
    wrong = [("$\\sum F = 0$ only", "Forces can balance while the object still spins (a twist)."),
             ("$\\sum\\tau = 0$ only", "Torques can balance while the object still slides."),
             ("$\\sum F = ma$ with $a = g$", "That's free fall, not \"not moving\"."),
             ("Every force on it is zero", "Forces act (weights, supports); they just add to zero.")]
    choices, distract = place_text("$\\sum F_x = \\sum F_y = \\sum F_z = 0$ and $\\sum\\tau_x = \\sum\\tau_y = \\sum\\tau_z = 0$", wrong, target)
    sol = r"""
Notes p. 1/10: "Static means not moving: $\sum F_x = \sum F_y = \sum F_z = 0$, $\sum\tau_x = \sum\tau_y = \sum\tau_z = 0$." Both conditions are needed.
"""
    return rec(stem="According to the notes, what conditions must hold for an object to be in static equilibrium?",
               choices=choices, key=target, check=("concept",), topic="Static equilibrium conditions", source_short="Ch 12 p. 1",
               source="Ch 12 notes p. 1/10 (\"Static means not moving\").", card="Statics",
               tests="the two conditions for statics.", solution=sol, distract=distract)


def c_torque(target):
    banned("concept question: the live exam asks only the computational problems from the notes / 2015 exam")
    wrong = [("$\\tau = rF$ always, whatever the direction of $F$", "Only the perpendicular part of $F$ twists: $\\tau = rF_\\perp$."),
             ("$\\tau = r_\\perp F_\\perp$", "That counts the angle twice."),
             ("$\\tau = F/r$", "A longer wrench gives more torque, not less."),
             ("$\\tau = r\\,F_\\parallel$, the part of $F$ along the wrench", "A push along the wrench doesn't twist it.")]
    choices, distract = place_text("$\\tau = r_\\perp F = rF_\\perp$", wrong, target)
    sol = r"""
Notes p. 1/10: "Torque is a twist." When $F$ is perpendicular to $r$, $\tau = rF$. Otherwise use either the perpendicular lever arm $r_\perp$ or the perpendicular part of the force $F_\perp$: $\tau = r_\perp F = rF_\perp$. (This is why the wall-beam problem on p. 6/10 uses $LT\sin\theta$.)
"""
    return rec(stem="A force $F$ is applied at the end of a wrench of length $r$, at an angle to the wrench. Which expression gives the torque?",
               choices=choices, key=target, check=("concept",), topic="Torque definition", source_short="Ch 12 p. 1",
               source="Ch 12 notes p. 1/10 ($\\tau = rF$; $\\tau = r_\\perp F = rF_\\perp$).", card="Statics",
               tests="only the perpendicular part of the force (or arm) counts.", solution=sol, distract=distract)


def c_geosync(target):
    banned("concept question: the live exam asks only the computational problems from the notes / 2015 exam")
    wrong = [("12 hours, so it passes over twice a day", "The notes use $T = 24$ h."),
             ("92 minutes, a low Earth orbit", "That's the 400 km LEO example on p. 2/10, not geosynchronous."),
             ("24 hours, at any altitude you like", "$T$ fixes $r$: $r = (T^2GM/4\\pi^2)^{1/3} = 4.22\\times10^7$ m."),
             ("27 days, like the Moon", "Not from the notes; geosynchronous means $T = 24$ h.")]
    choices, distract = place_text("24 hours, which keeps an equatorial satellite over the same point on the equator", wrong, target)
    sol = r"""
Notes p. 3/10: "Geosynchronous orbit (Earth with time): 24 hr orbit places equatorial satellite over same point on the equator." $T = 8.64\times10^4$ s gives $r = 4.22\times10^7$ m, $h = 35{,}900$ km.
"""
    return rec(stem="What is the period of a geosynchronous orbit, and why is that orbit useful?",
               choices=choices, key=target, check=("concept",), topic="Geosynchronous orbit", source_short="Ch 13 p. 3",
               source="Ch 13 notes p. 3/10 (geosynchronous orbit).", card="Orbit",
               tests="what geosynchronous means.", solution=sol, distract=distract)


def c_kepler_ellipse(target):
    banned("concept question: the live exam asks only the computational problems from the notes / 2015 exam")
    wrong = [("A circle centered on the Earth", "That's the geocentric picture the notes say came before Copernicus."),
             ("A circle centered on the Sun, at constant speed", "The notes: both earlier models used \"constant velocity circular paths\"; Kepler found otherwise."),
             ("A straight line", "Planets orbit."),
             ("A spiral toward the Sun", "Not in the notes.")]
    choices, distract = place_text("An ellipse", wrong, target)
    sol = r"""
Notes p. 5/10: "Kepler studied orbit of Mars 20 yrs … Both [geocentric and heliocentric models used] constant velocity circular paths. Kepler found Mars follows elliptical orbit."
"""
    return rec(stem="After studying the orbit of Mars for 20 years, what shape did Kepler find the orbit to be?",
               choices=choices, key=target, check=("concept",), topic="Kepler: Mars's orbit", source_short="Ch 13 p. 5",
               source="Ch 13 notes p. 5/10.", card="Orbit (Kepler)", tests="Kepler's finding about Mars.", solution=sol, distract=distract)


def c_seesaw_mass(target):
    banned("concept question: the live exam asks only the computational problems from the notes / 2015 exam")
    wrong = [("It's too small to matter", "The notes' seesaw mass could be anything; it never enters."),
             ("It cancels because both sides of the seesaw weigh the same", "Close, but the torque method says why: its weight acts at the pivot."),
             ("It's included in the adult's mass", "It isn't; $x = Lm_k/2M_T$ has no seesaw mass."),
             ("Gravity doesn't act on the seesaw", "It does; its weight just has zero lever arm.")]
    choices, distract = place_text("Its weight acts at the pivot, so its lever arm and torque about the pivot are zero", wrong, target)
    sol = r"""
Notes p. 4/10: "seesaw length $L$, mass $M$ (don't care!)". Torques are taken about the center, $\sum\tau_{center}$: $\frac L2 m_kg - xM_Tg = 0$. The seesaw's weight acts at the center, where $r = 0$, so $\tau = rF = 0$ (the same reason "A is eliminated" on p. 3/10).
"""
    return rec(stem="In the balanced-seesaw problem, the seesaw is uniform and pivots at its center. Why doesn't the seesaw's own mass affect where the adult must sit?",
               choices=choices, key=target, check=("concept",), topic="Why the seesaw's mass drops out", source_short="Ch 12 p. 3–4",
               source="Ch 12 notes p. 4/10 (\"mass M (don't care!)\") and p. 3/10 ($\\tau = rF$, $r = 0$).", card="Seesaw",
               tests="a force through the pivot has no torque.", solution=sol, distract=distract)
