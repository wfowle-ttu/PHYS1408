"""Independent numeric check of every answer in practice-exam-2-2.

Run:  python practice-exams/exam-2/_scripts/verify_2_2.py
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


def check_min(num, value, choices, key):
    """Minimum: key is the smallest choice >= value."""
    ok = [k for k, c in choices.items() if c >= value]
    best = min(ok, key=lambda k: choices[k])
    status = "OK " if best == key else "FAIL"
    print(f"{status} Q{num:>2}: computed {value:.4f} (a minimum) -> key {key}) {choices[key]}")
    assert best == key


def check_stops(num, inside, key):
    status = "OK " if inside < 0 and key == "e" else "FAIL"
    print(f"{status} Q{num:>2}: v_f^2 = {inside:.4f} < 0 -> key e) it stops")
    assert inside < 0 and key == "e"


# 1. Flat curve: v_max = sqrt(mu_s g r)
mu, r = 0.40, 35.0
check(1, sqrt(mu * g * r), {"a": 3.7, "b": 11.7, "c": 16.6, "d": 18.5, "e": 137.0}, "b", 0.05)

# 2. Banked curve v_min (minimum -> smallest choice that works)
r, mu, th = 90.0, 0.15, 30.0
t = tan(radians(th))
vmin = sqrt(g * r * (t - mu) / (1 + mu * t))
choices2 = {"a": 12.0, "b": 18.0, "c": 20.0, "d": 23.0, "e": 27.0}
check_min(2, vmin, choices2, "c")
# distractor sources
assert abs(sqrt(mu * g * r) - 11.5) < 0.1                       # flat curve
assert abs(sqrt(g * r * t) - 22.6) < 0.1                        # frictionless bank
assert abs(sqrt(g * r * (t + mu) / (1 - mu * t)) - 26.5) < 0.1  # v_max

# 3. Atwood machine, massless pulley
m1, m2, h = 8.0, 6.0, 1.5
check(3, sqrt(2 * g * h * (m1 - m2) / (m1 + m2)), {"a": 1.45, "b": 2.05, "c": 2.71, "d": 3.13, "e": 5.42}, "b", 0.005)

# 4. Roller coaster from rest at 65 m, over a 45 m hump, speed at 10 m
check(4, sqrt(2 * g * (65 - 10)), {"a": 14.0, "b": 19.8, "c": 23.2, "d": 32.8, "e": 35.7}, "d", 0.05)

# 5. Frictionless incline, sliding up
vi, th, dx = 5.0, 15.0, 2.5
check(5, sqrt(vi**2 - 2 * g * dx * sin(radians(th))), {"a": 3.5, "b": 4.3, "c": 6.1, "d": 12.3}, "a", 0.05)

# 6. Sliding DOWN a rough incline, stopping distance (professor's form)
vi, th, mu = 4.0, 12.0, 0.35
s, c = sin(radians(th)), cos(radians(th))
assert mu * c > s  # it does stop
check(6, vi**2 / (2 * g * (mu * c - s)), {"a": 1.5, "b": 2.4, "c": 6.1, "d": 12.1}, "c", 0.05)

# 7. Block up an incline pulled by a hanging mass -> stops before 1.5 m
m1, m2, th, mu, vi, dx = 15.0, 4.0, 25.0, 0.30, 3.0, 1.5
s, c = sin(radians(th)), cos(radians(th))
br = m2 - m1 * s - mu * m1 * c
check_stops(7, vi**2 + 2 * g * dx / (m1 + m2) * br, "e")
print(f"      stop distance = {(m1 + m2) * vi**2 / (-2 * g * br):.3f} m")
# distractors: no friction 2.32, sign flip 2.51, no m1 sin 2.98, adds 4.35
assert abs(sqrt(vi**2 + 2 * g * dx / (m1 + m2) * (m2 - m1 * s)) - 2.32) < 0.005
assert abs(sqrt(vi**2 + 2 * g * dx / (m1 + m2) * (m1 * s - m2 - mu * m1 * c)) - 2.51) < 0.005
assert abs(sqrt(vi**2 + 2 * g * dx / (m1 + m2) * (m2 - mu * m1 * c)) - 2.98) < 0.005
assert abs(sqrt(vi**2 - 2 * g * dx / (m1 + m2) * br) - 4.35) < 0.005

# 8. Mass slides down frictionless ramp into a spring
m, h, k = 2.5, 0.80, 1800.0
check(8, sqrt(2 * m * g * h / k), {"a": 0.011, "b": 0.022, "c": 0.10, "d": 0.15, "e": 0.21}, "d", 0.005)

# 9. Power climbing stairs
m, h, t = 70.0, 12.0, 8.0
check(9, m * g * h / t, {"a": 105, "b": 457, "c": 1030, "d": 8230, "e": 65900}, "c", 5)

# 10. Ball bounces straight back: F = 2 m v / dt
m, v, dt = 0.15, 30.0, 0.010
check(10, 2 * m * v / dt, {"a": 0.0, "b": 4.5, "c": 9.0, "d": 450, "e": 900}, "e", 0.5)

# 11. Rotational kinematics: time from w_i, w_f, dtheta
wi, wf, dth = 10.0, 50.0, 90.0
check(11, dth / ((wi + wf) / 2), {"a": 1.5, "b": 1.8, "c": 2.25, "d": 3.0, "e": 9.0}, "d", 0.005)

# 12. Parallel axis: rod, axis 0.30 m from one end
m, l, d = 3.0, 1.2, 1.2 / 2 - 0.30
check(12, m * l**2 / 12 + m * d**2, {"a": 0.09, "b": 0.27, "c": 0.36, "d": 0.50, "e": 0.63}, "e", 0.005)

# 13. Solid sphere rolling: a = 5/7 g sin(th)
th = 25.0
check(13, 5 / 7 * g * sin(radians(th)), {"a": 2.07, "b": 2.96, "c": 4.14, "d": 6.34, "e": 7.00}, "b", 0.005)

# 14. Person drops onto merry-go-round at r = 1.5 m
M, R, w0, m, r = 300.0, 2.5, 1.2, 60.0, 1.5
Id = 0.5 * M * R**2
check(14, Id * w0 / (Id + m * r**2), {"a": 1.05, "b": 1.10, "c": 1.12, "d": 1.20, "e": 1.37}, "a", 0.005)

# 15. Rod dropped from center to edge of a merry-go-round
M, R, w0, m, l = 400.0, 3.0, 1.5, 60.0, 3.0
Id = 0.5 * M * R**2
check(15, Id * w0 / (Id + m * l**2 / 3), {"a": 1.36, "b": 1.43, "c": 1.46, "d": 1.50, "e": 1.73}, "a", 0.005)

keys = "b c b d a c e d c e d e b a a".split()
print("\nKey:", " ".join(keys), "| letter counts:", {L: keys.count(L) for L in "abcde"})
print("All 15 answers verified.")
