"""Independent numeric check of every answer in practice-exam-2-1.

Run:  python practice-exams/exam-2/_scripts/verify_2_1.py
Each problem recomputes its answer from the given numbers and asserts that the
keyed choice matches it (to the precision shown on the exam) and that no other
choice also matches.
"""
from math import sqrt, sin, cos, radians

g = 9.8


def check(num, value, choices, key, tol):
    """choices: dict letter -> number shown on exam. tol: rounding tolerance."""
    hits = [k for k, c in choices.items() if abs(c - value) <= tol]
    status = "OK " if hits == [key] else "FAIL"
    print(f"{status} Q{num:>2}: computed {value:.4f} -> key {key}) {choices[key]}  (matches: {hits})")
    assert hits == [key], f"Q{num} key mismatch"


# 1. Halfpipe with rough patch: h_f = h_i - mu*L
h_i, L, mu = 6.0, 8.0, 0.15
check(1, h_i - mu * L, {"a": 4.8, "b": 5.1, "c": 5.6, "d": 6.0, "e": 6.2}, "a", 0.05)

# 2. Projectile from a ledge: H = h + (v0 sin th)^2 / 2g
h, v0, th = 5.0, 25.0, 30.0
H = h + (v0 * sin(radians(th))) ** 2 / (2 * g)
check(2, H, {"a": 5.0, "b": 8.0, "c": 13.0, "d": 21.0, "e": 36.9}, "c", 0.05)

# 3. Loop-the-loop: v_bottom,min = sqrt(5 g R)
R = 6.0
check(3, sqrt(5 * g * R), {"a": 7.7, "b": 10.8, "c": 15.3, "d": 17.1, "e": 24.2}, "d", 0.05)

# 4. Sliding up a rough ramp until it stops: a = g(sin th + mu cos th), t = v/a
v, mu, th = 6.0, 0.30, 20.0
a = g * (sin(radians(th)) + mu * cos(radians(th)))
check(4, v / a, {"a": 0.61, "b": 0.98, "c": 1.4, "d": 1.8, "e": 2.9}, "b", 0.005)

# 5. Banked curve v_max = sqrt(g r (mu + tan th)/(1 - mu tan th))
from math import tan
r, mu, th = 80.0, 0.25, 15.0
t = tan(radians(th))
vmax = sqrt(g * r * (mu + t) / (1 - mu * t))
check(5, vmax, {"a": 14.0, "b": 14.5, "c": 17.6, "d": 20.9, "e": 28.0}, "d", 0.05)

# 6. Vertical spring launch: h = k x^2 / (2 m g) above release point
m, k, x = 0.10, 1500.0, 0.04
check(6, k * x**2 / (2 * m * g), {"a": 0.12, "b": 0.49, "c": 1.2, "d": 2.4, "e": 12.0}, "c", 0.05)

# 7. 1-D elastic collision: v1f = ((m1-m2)v1 + 2 m2 v2)/(m1+m2)
m1, v1, m2, v2 = 3.0, 4.0, 1.0, -6.0
v1f = ((m1 - m2) * v1 + 2 * m2 * v2) / (m1 + m2)
v2f = v1 + v1f - v2
assert abs(0.5 * m1 * v1**2 + 0.5 * m2 * v2**2 - 0.5 * m1 * v1f**2 - 0.5 * m2 * v2f**2) < 1e-9
check(7, v1f, {"a": 9.0, "b": 2.5, "c": 1.0, "d": -1.0, "e": -2.5}, "d", 0.005)

# 8. Perfectly inelastic: mass m at 3v hits 2m at rest -> KE fraction retained
vf = (1 * 3) / (1 + 2)
frac = 0.5 * 3 * vf**2 / (0.5 * 1 * 3**2)
print(f"   Q 8: fraction retained = {frac:.4f} (range c: 30-40%)")
assert 0.30 <= frac <= 0.40

# 9. Ballistic pendulum: v = (M+m)/m sqrt(2 g h)
mb, M, h = 0.008, 2.0, 0.08
vb = (M + mb) / mb * sqrt(2 * g * h)
check(9, vb, {"a": 1.25, "b": 63.0, "c": 157.0, "d": 251.0, "e": 314.0}, "e", 0.5)

# 10. Hanging mass on disk pulley, energy: v = sqrt(2 m g h / (m + M/2))
m, M, R, h = 2.0, 6.0, 0.25, 1.5
v = sqrt(2 * m * g * h / (m + M / 2))
# cross-check with torque route: a = mg/(m + M/2), v^2 = 2 a h
assert abs(v - sqrt(2 * (m * g / (m + M / 2)) * h)) < 1e-9
check(10, v, {"a": 2.0, "b": 3.4, "c": 4.4, "d": 5.4, "e": 7.7}, "b", 0.05)

# 11. Solid cylinder rolling from height h: v = sqrt(4/3 g h), w = v/R
h, R = 2.0, 0.05
w = sqrt(4 / 3 * g * h) / R
check(11, w, {"a": 5.1, "b": 89.0, "c": 102.0, "d": 125.0, "e": 280.0}, "c", 0.5)

# 12. Ring dropped on spinning disk (counter-rotating)
I1 = 0.5 * 300 * 2.0**2
I2 = 100 * 1.5**2
wf = (I1 * 3.0 + I2 * (-4.0)) / (I1 + I2)
check(12, wf, {"a": 1.09, "b": 1.64, "c": 2.18, "d": 2.40, "e": 3.27}, "a", 0.005)

# 13. Child runs and jumps tangentially onto rim of merry-go-round
M, R, w0, mc, vc = 400.0, 2.5, 0.50, 40.0, 6.0
Id = 0.5 * M * R**2
wf = (Id * w0 + mc * vc * R) / (Id + mc * R**2)
check(13, wf, {"a": 0.42, "b": 0.82, "c": 0.98, "d": 1.30, "e": 2.4}, "b", 0.005)

# 14. Person walks from rim to center
M, R, m, w0 = 400.0, 3.0, 80.0, 1.5
wf = (0.5 * M * R**2 + m * R**2) * w0 / (0.5 * M * R**2)
check(14, wf, {"a": 1.07, "b": 1.25, "c": 1.5, "d": 1.8, "e": 2.1}, "e", 0.005)

# 15. Block down rough incline tied to a disk pulley (energy with friction)
m, th, mu, vi, Mp, d = 4.0, 25.0, 0.15, 0.50, 3.0, 1.0
s, c = sin(radians(th)), cos(radians(th))
meff = m + Mp / 2  # disk pulley adds M/2 of "effective mass"
vf2 = vi**2 + 2 * m * g * d * (s - mu * c) / meff
assert vf2 > 0
check(15, sqrt(vf2), {"a": 2.08, "b": 2.42, "c": 2.50, "d": 2.92}, "a", 0.005)

print("\nAll 15 answers verified.")
