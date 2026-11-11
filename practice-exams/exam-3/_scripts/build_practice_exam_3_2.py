"""Practice Exam 3-2: notes and 2015 Exam 3 procedures only, new numbers.

Run:  PYTHONIOENCODING=utf-8 python practice-exams/exam-3/_scripts/build_practice_exam_3_2.py
"""
import gens as q
from examlib3 import S, assemble, build

Q = assemble([
    S(q.beam_carry, L=5.0, M=60, loads=[(25, 1.5, "child")], ask="left", names=("Jim", "Sam")),
    S(q.diving_board, L=6.0, M=400, a=1.2, ask="A"),
    S(q.seesaw, L=4.0, mk=24, MT=60, ask="x", Ms=30),
    S(q.ladder_min, mu=0.35),
    S(q.boom, L=3.0, M=120, m=80, theta=35, Tmax=2000, ask="x"),
    S(q.lamp, m=12, theta=50, ask="ceiling"),
    S(q.wire, m=150, L0=2.0, d=0.001, Y=7e10),
    S(q.ladder_climb, L=9.0, theta=72, mu=0.30, M=140, m=15, step=0.5),
    S(q.g_altitude, h=1.2e6),
    S(q.orbit_from_period, T_hr=12),
    S(q.binary, M=2e30, d=6e10, unit="day", give="r"),
    S(q.rocket_height, v=2000),
    S(q.event_horizon, M=4e36, desc=r"A black hole has a mass of $4\times10^{36}$ kg."),
    S(q.planet_speed, a_au=2.8, name="An asteroid"),
    S(q.equal_pull, Mb=1.2e23, d=5.0e8),
], seed=32)

INTRO = """
Practice Exam 3-2 leans on the **lecture-note examples** with new numbers: the sofa with a child on it, the diving board's back support (which pulls **down**), the seesaw, the minimum ladder angle, the wall beam, the orbit altitude from a period, binary stars, the rocket height, the event horizon, and a planet's orbital speed. It also has the 2015 types: two cords, the wire, the climbing man (a **maximum**), $g$ at an altitude, and the equal-pull point. Every question is a procedure worked in the notes or on the 2015 exam.
"""

if __name__ == "__main__":
    build(2, Q, INTRO)
