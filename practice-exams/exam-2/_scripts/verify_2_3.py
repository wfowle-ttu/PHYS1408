"""Independent numeric check of every answer in practice-exam-2-3.

Run:  python practice-exams/exam-2/_scripts/verify_2_3.py
Each problem recomputes its answer from the given numbers and asserts that the
keyed choice matches it (to the precision shown on the exam) and that no other
choice also matches. Min/max questions are keyed to the choice that physically
works (round a minimum UP, a maximum DOWN), as the professor grades them.
"""
from math import sqrt, sin, cos, tan, radians

g = 9.8


def check(num, value, choices, key, tol):
    """choices: dict letter -> number shown on exam. tol: rounding tolerance."""
    hits = [k for k, c in choices.items() if abs(c - value) <= tol]
    status = "OK " if hits == [key] else "FAIL"
    print(f"{status} Q{num:>2}: computed {value:.4f} -> key {key}) {choices[key]}  (matches: {hits})")
    assert hits == [key], f"Q{num} key mismatch"


def near(x, target, tol):
    assert abs(x - target) <= tol, (x, target)


# 1. Banked curve v_max (maximum -> largest choice that still works)
r, mu, th = 78.0, 0.25, 20.0
t = tan(radians(th))
vmax = sqrt(g * r * (mu + t) / (1 - mu * t))
choices = {"a": 9, "b": 14, "c": 17, "d": 21, "e": 23}
best = max((k for k, c in choices.items() if c <= vmax), key=lambda k: choices[k])
print(f"{'OK ' if best == 'd' else 'FAIL'} Q 1: computed {vmax:.4f} (a maximum) -> key {best}) {choices[best]}")
assert best == "d"
near(sqrt(g * r * (t - mu) / (1 + mu * t)), 8.94, 0.01)  # v_min
near(sqrt(mu * g * r), 13.8, 0.05)                        # flat curve
near(sqrt(g * r * t), 16.7, 0.05)                         # frictionless

# 2. Conceptual: "Energy is the ability to do work" -> e (no computation)
print("OK  Q 2: conceptual, key e) the ability to do work")

# 3. Work by a rope at 30 degrees
F, d, phi = 50.0, 12.0, 30.0
check(3, F * d * cos(radians(phi)), {"a": 0, "b": 300, "c": 520, "d": 600, "e": 1200}, "c", 1)

# 4. Coyote falls from a 45 m cliff
h = 45.0
check(4, sqrt(2 * g * h), {"a": 29.7, "b": 42.0, "c": 59.4, "d": 441, "e": 882}, "a", 0.05)

# 5. Halfpipe: number of complete crossings of the rough patch
hi, L, mu = 1.8, 4.0, 0.10
loss = mu * L
n, hh = 0, hi
while hh - loss >= 0:
    hh -= loss
    n += 1
print(f"{'OK ' if n == 4 else 'FAIL'} Q 5: complete crossings = {n} (left with {hh:.2f} m, stops {hh / mu:.1f} m into patch)")
assert n == 4

# 6. Rough incline, sliding up: stopping distance
vi, th, mu = 8.0, 30.0, 0.20
s, c = sin(radians(th)), cos(radians(th))
check(6, vi**2 / (2 * g * (s + mu * c)), {"a": 0.61, "b": 2.42, "c": 3.27, "d": 4.66, "e": 4.85}, "e", 0.005)
near(vi**2 / (2 * g * (s + mu)), 4.66, 0.005)   # friction with mg, not mg cos
near(vi**2 / (2 * g), 3.27, 0.005)              # straight up, no slope
near(vi / (2 * g * (s + mu * c)), 0.61, 0.005)  # v not squared

# 7. Spring launches a mass horizontally
k, x, m = 800.0, 0.10, 0.20
check(7, sqrt(k * x**2 / m), {"a": 4.47, "b": 6.32, "c": 8.94, "d": 20.0, "e": 40.0}, "b", 0.005)

# 8. Normal force at the top of a loop, launched from h = 30 m, R = 10 m
m, h, R = 500.0, 30.0, 10.0
v2 = 2 * g * (h - 2 * R)
check(8, m * v2 / R - m * g, {"a": 0, "b": 4900, "c": 9800, "d": 14700, "e": 24500}, "b", 1)

# 9. Cue ball hits 8-ball (equal masses, elastic): cue ball stops
m1 = m2 = 0.17
v1, v2 = 3.0, 0.0
v1f = ((m1 - m2) * v1 + 2 * m2 * v2) / (m1 + m2)
check(9, v1f, {"a": -3.0, "b": -1.5, "c": 0.0, "d": 1.5, "e": 3.0}, "c", 1e-9)

# 10. Elastic, both moving right: velocity of the 2 kg ball afterward
m1, v1, m2, v2 = 2.0, 6.0, 4.0, 1.0
v1f = ((m1 - m2) * v1 + 2 * m2 * v2) / (m1 + m2)
check(10, v1f, {"a": 4.33, "b": 2.67, "c": 0.67, "d": 0.0, "e": -0.67}, "e", 0.005)

# 11. Ballistic pendulum: how high does the block swing?
m, M, v = 0.010, 2.0, 400.0
V = m * v / (M + m)
check(11, V**2 / (2 * g), {"a": 0.10, "b": 0.20, "c": 0.40, "d": 1.99, "e": 40.6}, "b", 0.005)
near(0.5 * m * v**2 / ((M + m) * g), 40.6, 0.05)

# 12. Tension in the string over a ring pulley (I = M R^2)
m, M = 3.0, 4.0
a = m * g / (m + M)
check(12, M * a, {"a": 0, "b": 11.8, "c": 16.8, "d": 29.4, "e": 42.0}, "c", 0.05)
near(0.5 * M * (m * g / (m + M / 2)), 11.8, 0.05)  # assumes a disk pulley

# 13. Hoop rolling from h = 1.5 m
h = 1.5
check(13, sqrt(g * h), {"a": 3.83, "b": 4.43, "c": 4.58, "d": 5.42, "e": 7.67}, "a", 0.005)

# 14. Non-spinning disk dropped onto a spinning disk
I1 = 0.5 * 200 * 1.5**2
I2 = 0.5 * 100 * 1.0**2
check(14, I1 * 4.0 / (I1 + I2), {"a": 2.00, "b": 2.67, "c": 2.77, "d": 3.27, "e": 4.00}, "d", 0.005)

# 15. Child runs AGAINST the rotation and jumps onto the rim
M, R, w0, mc, vc = 200.0, 2.0, 1.0, 30.0, 4.0
Id = 0.5 * M * R**2
wf = (Id * w0 - mc * vc * R) / (Id + mc * R**2)
check(15, wf, {"a": 0.31, "b": 0.40, "c": 0.77, "d": 1.23, "e": 1.60}, "a", 0.005)

keys = "d e c a d e b b c e b c a d a".split()
print("\nKey:", " ".join(keys), "| letter counts:", {L: keys.count(L) for L in "abcde"})
print("All 15 answers verified.")
