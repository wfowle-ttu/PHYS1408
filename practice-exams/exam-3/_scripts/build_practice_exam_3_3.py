"""Practice Exam 3-3: notes and 2015 Exam 3 procedures only, new numbers.

Run:  PYTHONIOENCODING=utf-8 python practice-exams/exam-3/_scripts/build_practice_exam_3_3.py
"""
import gens as q
from examlib3 import ME, S, assemble, build

Q = assemble([
    S(q.beam_carry, L=6.0, M=90, loads=[(30, 6.0, "crate")], right_x=5.2, ask="right", names=("Luis", "Ana")),
    S(q.ladder_climb, L=8.0, theta=62, mu=0.35, M=110, m=30, step=0.5),
    S(q.ladder_top_angle, mu=0.5, M=90, m=20, L=7),
    S(q.lamp, m=25, theta=55, ask="ceiling"),
    S(q.wire, m=200, L0=2.5, d=0.002, Y=1.2e11),
    S(q.block_compress, m=150, w=0.5, l=0.5, h=0.2, Y=5e5, what="rubber"),
    S(q.diving_board, L=5.0, M=300, a=1.0, ask="B"),
    S(q.seesaw, L=3.6, mk=18, MT=72, ask="x"),
    S(q.g_altitude, h=3.0e5, mass=75),
    S(q.sat_period, h=8e5, unit="min", mass=500),
    S(q.rocket_height, v=3000),
    S(q.rocket_speed, h=2.0e6),
    S(q.escape, M=6.4e23, R=3.4e6, body="a small planet"),
    S(q.equal_pull, Mb=ME / 80, d=4e8),
    S(q.binary, M=3e30, d=1e10, unit="hr"),
], seed=33)

INTRO = """
Practice Exam 3-3 mixes the 2015 Exam 3 types (sofa with a load on the end, the climbing man, two cords, the wire, the jello block, $g$ at an altitude, satellite period, launch speed, binary stars, the equal-pull point) with notes examples: the angle needed to reach the top of the ladder, the diving board, the seesaw, the rocket height, and escape speed. Question 2 is a **maximum**: pick the largest choice that still works. Every question is a procedure worked in the notes or on the 2015 exam.
"""

if __name__ == "__main__":
    build(3, Q, INTRO)
