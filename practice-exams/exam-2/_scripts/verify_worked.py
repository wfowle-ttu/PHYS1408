"""Independent numeric check of every result in study-guide-exam-2-worked.qmd.

Run:  python practice-exams/exam-2/_scripts/verify_worked.py
Each example from the professor's notes (and the 2015 Exam 2) is recomputed
here and compared with the value printed in the worked guide.
"""
from math import sqrt, sin, cos, tan, radians

g = 9.8
results = []


def check(label, value, printed, tol):
    ok = abs(value - printed) <= tol
    results.append(ok)
    print(f"{'OK ' if ok else 'FAIL'} {label:<48} computed {value:12.5f}   printed {printed}")


def banked(r, mu, th, sign):
    t = tan(radians(th))
    return sqrt(g * r * (t + sign * mu) / (1 - sign * mu * t))


# ---- Ch 6 -------------------------------------------------------------
check("6.1 flat curve vmax", sqrt(0.1 * g * 50), 7.0, 0.05)
check("6.2 banked 10deg mu.1 r50 vmax", banked(50, 0.1, 10, +1), 11.7, 0.05)
check("6.2 banked 10deg mu.2", banked(50, 0.2, 10, +1), 13.8, 0.05)
check("6.2 banked 10deg mu.3", banked(50, 0.3, 10, +1), 15.7, 0.05)
check("6.2 banked 10deg mu.4", banked(50, 0.4, 10, +1), 17.4, 0.05)
check("6.2 cloverleaf r100 20deg mu.3", banked(100, 0.3, 20, +1), 27.0, 0.5)
check("6.3 banked 70deg vmax", banked(60, 0.2, 70, +1), 62.0, 0.5)
check("6.3 banked 70deg vmin", banked(60, 0.2, 70, -1), 31.0, 0.5)
check("6.4 banked 40deg vmax", banked(70, 0.2, 40, +1), 29.3, 0.05)
check("6.4 banked 40deg vmin", banked(70, 0.2, 40, -1), 19.4, 0.05)

# ---- Ch 7/8 -----------------------------------------------------------
check("7.2 Atwood", sqrt(2 * g * 2 * (10 - 5) / 15), 3.61, 0.005)
check("7.3 coaster v2", sqrt(2 * g * 80), 39.6, 0.05)
check("7.3 coaster v3", sqrt(2 * g * 50), 31.3, 0.05)
check("7.3 coaster v4", sqrt(2 * g * 100), 44.3, 0.05)
check("7.4 halfpipe notes", 3 - 0.01 * 10, 2.9, 1e-9)
check("7.4 halfpipe exam #1", 7 - 0.1 * 5, 6.5, 1e-9)
check("7.5 frictionless incline", sqrt(16 - 2 * g * 3 * sin(radians(10))), 2.41, 0.005)
s30, c30 = sin(radians(30)), cos(radians(30))
check("7.6 rough up 0.5 m", sqrt(2.5**2 - 2 * g * 0.5 * (s30 + 0.1 * c30)), 0.708, 0.0015)
s10, c10 = sin(radians(10)), cos(radians(10))
inside = 9 - 2 * g * 2 * (0.2 * c10 + s10)
check("7.7 rough up inside root", inside, -5.53, 0.005)
check("7.7 stop distance up", 9 / (2 * g * (0.2 * c10 + s10)), 1.24, 0.005)
check("7.8 rough down v at 2 m", sqrt(9 + 2 * g * 2 * (s10 - 0.2 * c10)), 2.84, 0.005)
check("7.8 stop distance down", 9 / (2 * g * (0.2 * c10 - s10)), 19.7, 0.05)
# The professor's notes round sin10 = 0.174, cos10 = 0.985 by hand:
check("7.7 prof rounding: inside root", 9 - 2 * g * 2 * (0.2 * 0.985 + 0.174), -5.54, 0.005)
check("7.8 prof rounding: v at 2 m", sqrt(9 + 2 * g * 2 * (0.174 - 0.2 * 0.985)), 2.85, 0.005)
check("7.8 prof rounding: stop distance", 9 / (2 * g * (0.2 * 0.985 - 0.174)), 19.96, 0.005)
check("7.9 spring from ramp", sqrt(2 * 1 * g * 1 / 1000), 0.14, 0.005)
check("7.10 spring launch notes", 1000 * 0.01**2 / (2 * 0.01 * g), 0.51, 0.005)
check("7.10 spring launch exam #5", 2000 * 0.02**2 / (2 * 0.05 * g), 0.82, 0.005)
check("7.11 power", 100 * g * 25 / 20, 1225, 1e-6)
m1, m2, mu, vi, dx = 20, 2, 0.4, 2, 0.5
br = m2 - m1 * s30 - mu * m1 * c30
check("7.12 up: inside root", vi**2 + 2 * g * dx / (m1 + m2) * br, -2.64, 0.01)
check("7.12 up: stop distance", (m1 + m2) * (0 - vi**2) / (2 * g * br), 0.30, 0.005)
check("7.13 down m2=2", sqrt(vi**2 + 2 * g * dx / 22 * (m1 * s30 - 2 - mu * m1 * c30)), 2.12, 0.005)
check("7.13 down m2=10", sqrt(vi**2 + 2 * g * dx / 30 * (m1 * s30 - 10 - mu * m1 * c30)), 1.32, 0.005)
check("7.14 loop vtop R=10", sqrt(g * 10), 9.9, 0.05)
check("7.14 loop h", 2.5 * 10, 25, 1e-9)
check("7.14 loop vbottom exam #3", sqrt(5 * g * 10), 22.1, 0.05)
check("7.15 ramp time exam #4", 7 / (g * (sin(radians(5)) + 0.6 * cos(radians(5)))), 1.04, 0.005)
check("7.16 projectile exam #2", 3 + (20 * sin(radians(45)))**2 / (2 * g), 13.2, 0.05)

# ---- Ch 9 -------------------------------------------------------------
vf = (2 * 2 + 1 * 1) / 3
check("9.2 inelastic KE fraction exam #7", 0.5 * 3 * vf**2 / (0.5 * 2 * 4 + 0.5 * 1 * 1), 25 / 27, 1e-9)
v1f = ((10 - 2) * 5 + 2 * 2 * 2) / 12
check("9.3 elastic notes v1f", v1f, 4.0, 1e-9)
check("9.3 elastic notes v2f", 5 + v1f - 2, 7.0, 1e-9)
v1f = ((1 - 2) * 5 + 2 * 2 * (-2)) / 3
check("9.3 elastic exam #6 v1f", v1f, -4.33, 0.005)
check("9.3 elastic exam #6 v2f", 5 + v1f - (-2), 2.67, 0.005)
m, M, h = 0.005, 1.0, 0.05
vb = (M + m) / m * sqrt(2 * g * h)
check("9.5 ballistic notes v", vb, 199, 0.5)
check("9.5 ballistic notes eta %", 100 * (M + m) * g * h / (0.5 * m * vb**2), 0.50, 0.005)
m, M, h = 0.005, 10.0, 0.01
check("9.5 ballistic exam #8 eta %", 100 * m / (M + m), 0.050, 0.0005)
check("9.5 ballistic exam #8 v", (M + m) / m * sqrt(2 * g * h), 886, 0.5)

# ---- Ch 10 ------------------------------------------------------------
check("10.1 alpha from t", (100 - 50) / 10, 5, 1e-9)
check("10.1 alpha from dtheta", (100**2 - 50**2) / (2 * 40), 93.75, 1e-9)
a = 1 * g / (1 + 10 / 2)
check("10.4 pulley a", a, 1.63, 0.005)
check("10.4 pulley vf kinematics", sqrt(1 + 2 * a * 2), 2.74, 0.005)
check("10.4 pulley vf energy", sqrt(((0.5 + 10 / 4) * 1 + 1 * g * 2) / (0.5 + 10 / 4)), 2.74, 0.005)
check("10.4 pulley exam #9", 0.5 * g / (0.5 + 0.6 * 10), 0.75, 0.005)
check("10.5 sphere omega exam #10", sqrt(10 / 7 * g * 1) / 0.01, 374, 0.5)
mm, Mp, th, mu, vi, d = 5, 2, 30, 0.1, 0.8, 0.6
vf2 = vi**2 + 2 * mm * g * d * (sin(radians(th)) - mu * cos(radians(th))) / (mm + Mp / 2)
check("10.6 incline+pulley exam #13", sqrt(vf2), 2.17, 0.005)

# ---- Ch 11 ------------------------------------------------------------
Id = 0.5 * 500 * 2**2
check("11.1 disk on disk", Id * 2 / (Id + 0.5 * 200 * 1**2), 1.82, 0.005)
check("11.2 man drops at 1 m", Id * 1 / (Id + 100 * 1**2), 0.91, 0.005)
check("11.3 counter-rotating ring", (Id * 3 + 200 * 1.5**2 * -2) / (Id + 200 * 1.5**2), 1.45, 0.005)
I1, I2 = 0.5 * 200 * 9, 0.8 * 100 * 2.5**2
check("11.3 exam #11", (I1 * 4 + I2 * -2) / (I1 + I2), 1.86, 0.005)
check("11.4 man runs on", (Id * 0.5 + 100 * 3 * 2) / (Id + 100 * 4), 0.786, 0.0005)
check("11.4 exam #12", (0.5 * 500 * 4 * 0.7 + 50 * 10 * 2) / (0.5 * 500 * 4 + 50 * 4), 1.42, 0.005)
check("11.5 rod center to edge", Id * 2 / (Id + 100 * 4 / 3), 1.76, 0.005)
check("11.6 walk to center", (500 + 200) / 500 * 2, 2.8, 1e-9)
check("11.6 KE before", 0.5 * (Id + 100 * 4) * 2**2, 2800, 1e-9)
check("11.6 KE after", 0.5 * Id * 2.8**2, 3920, 1e-6)

print(f"\n{sum(results)}/{len(results)} checks passed")
assert all(results)
