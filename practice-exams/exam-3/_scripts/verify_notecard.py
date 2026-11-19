"""Prove the 3x5 notecard solves every practice-exam question.

Each function below is the notecard entry exactly as printed (same symbols, same order of
operations, card constants). For every question in build_practice_exam_3_*.py it computes the
answer from the card formula and checks it against the generator's keyed answer.

Run: PYTHONIOENCODING=utf-8 python practice-exams/exam-3/_scripts/verify_notecard.py
"""
import math
import re
import sys
from math import atan, degrees, pi, radians, sin, sqrt, tan
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import examlib3  # noqa: E402

# Card constants (back side, top line)
g, G, ME, RE = 9.8, 6.67e-11, 5.98e24, 6.37e6
GM = G * ME
MSUN, AU, C = 2e30, 1.5e11, 3e8


# ---------------- card entries (front: Ch 12) ----------------
def card_sofa(L, M, loads, xB, ask):
    FB = g * (M * L / 2 + sum(m * x for m, x, _ in loads)) / xB
    return FB if ask == "right" else (M + sum(m for m, _, _ in loads)) * g - FB


def card_diving(L, M, a, ask):
    B = (L / 2) / a * M * g
    return B if ask == "B" else B - M * g


def card_seesaw(L, mk, MT):
    return L * mk / (2 * MT)


def card_wallbeam(L, M, m, theta, T):
    return L / (m * g) * (T * sin(radians(theta)) - M * g / 2)


def card_ladder_empty(mu):
    return degrees(atan(1 / (2 * mu)))


def card_ladder_climb(L, theta, mu, M, m):
    return L / M * (mu * (M + m) * tan(radians(theta)) - m / 2)


def card_ladder_top(mu, M, m):
    return degrees(atan((M + m / 2) / ((M + m) * mu)))


def card_light(m, theta):
    return m * g / sin(radians(theta))


def card_wire(m, l, d, Y):
    return m * g * l / (pi * (d / 2) ** 2 * Y)


def card_block(m, w, l, h, Y):
    return m * g * h / (w * l * Y)


# ---------------- card entries (back: Ch 13) ----------------
def card_g(h):
    return GM / (RE + h) ** 2


def card_period(h):
    return 2 * pi * sqrt((RE + h) ** 3 / GM)


def card_alt_from_T(T_s):
    return (T_s ** 2 * GM / (4 * pi ** 2)) ** (1 / 3) - RE


def card_binary(M, r):
    return 4 * pi * sqrt(r ** 3 / (G * M))


def card_launch_speed(h):
    return sqrt(2 * GM * (1 / RE - 1 / (RE + h)))


def card_height_from_v(v):
    return 2 * GM * RE / (2 * GM - v ** 2 * RE) - RE


def card_escape(M, R):
    return sqrt(2 * G * M / R)


def card_horizon(M):
    return 2 * G * M / C ** 2


def card_planet(a_au):
    return sqrt(G * MSUN / (a_au * AU))


def card_equal_pull(Mb):
    k = sqrt(ME / Mb)
    return k / (1 + k)


UNIT = {"min": 60, "hr": 3600, "day": 86400, "s": 1, "yr": 86400 * 365}


def card_answer(name, kw):
    """Card formula -> number in the same display units the exam uses."""
    if name == "beam_carry":
        return card_sofa(kw["L"], kw["M"], kw["loads"], kw.get("right_x") or kw["L"], kw.get("ask", "right"))
    if name == "diving_board":
        return card_diving(kw["L"], kw["M"], kw["a"], kw.get("ask", "B"))
    if name == "seesaw":
        return card_seesaw(kw["L"], kw["mk"], kw["MT"])
    if name == "boom":
        return card_wallbeam(kw["L"], kw["M"], kw["m"], kw["theta"], kw["Tmax"])
    if name == "ladder_min":
        return card_ladder_empty(kw["mu"])
    if name == "ladder_climb":
        return card_ladder_climb(kw["L"], kw["theta"], kw["mu"], kw["M"], kw["m"])
    if name == "ladder_top_angle":
        return card_ladder_top(kw["mu"], kw["M"], kw["m"])
    if name == "lamp":
        return card_light(kw["m"], kw["theta"])
    if name == "wire":
        v = card_wire(kw["m"], kw["L0"], kw["d"], kw["Y"])
        return v * 1e3 if v < 0.02 else v      # exam shows mm when tiny
    if name == "block_compress":
        return card_block(kw["m"], kw["w"], kw["l"], kw["h"], kw["Y"]) * 1e3   # mm
    if name == "g_altitude":
        return card_g(kw["h"])
    if name == "sat_period":
        return card_period(kw["h"]) / UNIT[kw.get("unit", "min")]
    if name == "orbit_from_period":
        return card_alt_from_T(kw["T_hr"] * 3600) / 1e3                       # km
    if name == "binary":
        return card_binary(kw["M"], kw["d"] / 2) / UNIT[kw.get("unit", "day")]
    if name == "rocket_speed":
        return card_launch_speed(kw["h"]) / 1e3                                # km/s
    if name == "rocket_height":
        return card_height_from_v(kw["v"]) / 1e3                               # km
    if name == "escape":
        return card_escape(kw["M"], kw["R"]) / 1e3                             # km/s
    if name == "event_horizon":
        return card_horizon(kw["M"])
    if name == "planet_speed":
        return card_planet(kw["a_au"]) / 1e3                                   # km/s
    if name == "equal_pull":
        return 100 * card_equal_pull(kw["Mb"])                                 # %
    raise KeyError(name)


def specs_of(build_file):
    """Run a build script with assemble() replaced so it returns the raw (generator, kwargs) specs."""
    src = build_file.read_text(encoding="utf-8")
    src = src.replace('if __name__ == "__main__":', "if False:")
    ns = {"__name__": "specs", "__file__": str(build_file)}
    real = examlib3.assemble
    examlib3.assemble = lambda specs, seed, **k: specs
    try:
        exec(compile(src, str(build_file), "exec"), ns)
    finally:
        examlib3.assemble = real
    return ns["Q"], real(ns["Q"], seed=int(re.search(r"seed=(\d+)", src).group(1)))


bad = 0
for bf in sorted(HERE.glob("build_practice_exam_3_*.py")):
    specs, recs = specs_of(bf)
    print(f"== {bf.name}")
    for i, ((f, kw), rec) in enumerate(zip(specs, recs), 1):
        mode, keyed_value, nums = rec["check"]
        card = card_answer(f.__name__, kw)
        key_idx = examlib3.LETTERS.index(rec["key"])
        if mode == "near":
            dist = [abs(math.log(c / card)) for c in nums]
            pick = dist.index(min(dist))
        elif mode == "max":
            pick = max((c, j) for j, c in enumerate(nums) if c <= card)[1]
        else:
            pick = min((c, j) for j, c in enumerate(nums) if c >= card)[1]
        same = abs(card - keyed_value) <= 1e-6 * abs(keyed_value)
        ok = same and pick == key_idx
        bad += not ok
        print(f"{'OK ' if ok else 'BAD'} Q{i:>2} {f.__name__:<18} card={card:.6g} key={keyed_value:.6g} -> card picks {examlib3.LETTERS[pick]}, key {rec['key']}")
print("ALL CARD FORMULAS MATCH" if not bad else f"{bad} MISMATCHES")
sys.exit(1 if bad else 0)
