"""Recompute every number used in study-guide-exam-3.qmd (notes examples + 2015 Exam 3 #1-5, #9-13).

Run: PYTHONIOENCODING=utf-8 python practice-exams/exam-3/_scripts/verify_guide.py
"""
from math import atan, degrees, pi, radians, sin, sqrt, tan

g = 9.8
G = 6.67e-11
ME_notes, ME_exam, RE = 5.97e24, 5.98e24, 6.37e6


def show(label, v, expect=None, tol=0.01):
    flag = ""
    if expect is not None:
        flag = "OK" if abs(v - expect) <= tol * abs(expect) else f"MISMATCH (notes/expected {expect})"
    print(f"{label:<48} {v:.6g}  {flag}")


print("== Ch 12 notes")
show("p3 diving board B/Mg (L=10, a=1)", (10 / 2) / 1, 5)
show("p3 diving board A/Mg", 5 - 1, 4)
show("p4 seesaw x/L (mk=20, MT=100)", 20 / (2 * 100), 0.1)
show("p4 sofa each end (M=50) N", 50 * g / 2, 245)
show("p5 Sam S (kid 20 kg at 1 m, sofa 50 kg, L=4)", (20 * g * 1 + 50 * g * 2) / 4, 294)
show("p5 Jim J", (3 * 20 * g + 2 * 50 * g) / 4, 392)
show("p6 x_max", 5 / (100 * g) * (1e4 * 0.5 - 1000 * g / 2), 0.5102)
show("p7 theta_min mu=0.4 (no number in notes)", degrees(atan(1 / 0.8)))
show("p8 x (L=10, 65°, mu .4, M 150, m 10)", 10 / 150 * (0.4 * 160 * tan(radians(65)) - 5), 8.80)
show("p8 tan 65", tan(radians(65)), 2.1445)
show("p9 x at 70°", 10 / 150 * (0.4 * 160 * tan(radians(70)) - 5), 11.4)
show("p9 tan 70", tan(radians(70)), 2.75)
show("p9 x with mu .6", 10 / 150 * (0.6 * 160 * tan(radians(65)) - 5), 13.4)
show("p9 theta_min to reach top", degrees(atan(155 / (0.4 * 160))), 67.6)

print("== 2015 Exam 3, Ch 12")
S1 = (2.5 * 100 * g + 5 * 50 * g) / 4.5
show("#1 Sarah (N)", S1, 1090, 0.002)
show("#1 torque sum (N m)", 2.5 * 100 * g + 5 * 50 * g)
show("#1 James (N)", 150 * g - S1)
x2 = 5 / 150 * (0.25 * 170 * tan(radians(71)) - 20 / 2)
show("#2 tan71", tan(radians(71)))
show("#2 x (m)", x2)
show("#3 T ceiling (N)", 20 * g / sin(radians(40)))
show("#3 sin40", sin(radians(40)))
show("#3 horizontal cord (N)", 20 * g / tan(radians(40)))
show("#4 dh (mm)", 500 * g * 0.1 / (3 * 4 * 3e4) * 1e3)
A5 = pi * 0.0005 ** 2
show("#5 area (m^2)", A5)
show("#5 dl (m)", 500 * g * 4 / (A5 * 8e10))

print("== Ch 13 notes (notes use M = 5.97e24)")
GM = G * ME_notes
show("p1 g", GM / RE ** 2, 9.81)
r = RE + 4e5
show("p2 T LEO (s)", 2 * pi * sqrt(r ** 3 / GM), 5546)
show("p2 T LEO (min)", 2 * pi * sqrt(r ** 3 / GM) / 60, 92.4)
rg = (86400 ** 2 * GM / (4 * pi ** 2)) ** (1 / 3)
show("p3 r geo", rg, 4.22e7)
show("p3 h geo (km)", (rg - RE) / 1e3, 35900)
Tb = sqrt(16 * pi ** 2 * (6e10) ** 3 / (G * 2e30))
show("p4 binary T (s)", Tb, 1.599e7)
show("p4 binary T (days)", Tb / 86400, 185)
rr = 2 * GM * RE / (2 * GM - 1000 ** 2 * RE)
show("p8 rocket r (v=1000)", rr)
show("p8 rocket h (km)", (rr - RE) / 1e3, 50.73)
show("p8 2GM", 2 * GM)
show("p8 numerator 2GMR", 2 * GM * RE, 5.07e21)
show("p8 v for 1000 km", sqrt(2 * GM * (1 / RE - 1 / (RE + 1e6))), 4119)
show("p9 v_esc", sqrt(2 * GM / RE), 11181)
show("p9 event horizon M=1e37", 2 * G * 1e37 / 9e16, 1.48e10)
show("p10 GM_sun", G * 2e30, 1.33e20)
for name, a, ex in [("Merc", 0.6e11, 47.15), ("Venus", 1.05e11, 35.59), ("Earth", 1.5e11, 29.78), ("Mars", 2.25e11, 24.31),
                    ("Jupiter", 7.8e11, 13.06), ("Saturn", 1.5e12, 9.42), ("Uranus", 3e12, 6.66), ("Neptune", 4.5e12, 5.44)]:
    show(f"p10 v {name} (km/s)", sqrt(G * 2e30 / a) / 1e3, ex)

print("== 2015 Exam 3, Ch 13 (exam constants M = 5.98e24)")
GM = G * ME_exam
show("GM (exam)", GM)
v9 = sqrt(2 * GM * (1 / RE - 1 / (RE + 1e6)))
show("#9 v (m/s)", v9)
r10 = RE + 1e8
T10 = 2 * pi * sqrt(r10 ** 3 / GM)
show("#10 r", r10)
show("#10 T (s)", T10)
show("#10 T (days)", T10 / 86400)
T11 = sqrt(16 * pi ** 2 * (5e7) ** 3 / (G * 1e31))
show("#11 T (s)", T11)
show("#11 T (min)", T11 / 60)
show("#12 r", RE + 7.5e5)
show("#12 g", GM / (RE + 7.5e5) ** 2)
show("#12 GM/h^2 (choice e trap)", GM / 7.5e5 ** 2)
k = sqrt(ME_exam / 7e22)
show("#13 mass ratio", ME_exam / 7e22)
show("#13 k", k)
show("#13 fraction", k / (1 + k))
show("#13 x (km)", k / (1 + k) * 4e5)
