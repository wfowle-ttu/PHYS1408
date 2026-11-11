"""Practice Exam 3-1: notes and 2015 Exam 3 procedures only, new numbers.

Run:  PYTHONIOENCODING=utf-8 python practice-exams/exam-3/_scripts/build_practice_exam_3_1.py
"""
import gens as q
from examlib3 import S, assemble, build

Q = assemble([
    S(q.beam_carry, L=4.0, M=80, loads=[(40, 4.0, "box of books")], right_x=3.6, ask="right", names=("Mike", "Dana")),
    S(q.ladder_climb, L=6.0, theta=70, mu=0.30, M=120, m=25, step=0.5),
    S(q.lamp, m=15, theta=35, ask="ceiling"),
    S(q.block_compress, m=400, w=2.0, l=3.0, h=0.15, Y=2.5e4),
    S(q.wire, m=300, L0=3.0, d=0.0015, Y=2.0e11),
    S(q.diving_board, L=8.0, M=600, a=1.5, ask="B"),
    S(q.seesaw, L=5.0, mk=20, MT=80, ask="x", Ms=40),
    S(q.boom, L=4.0, M=200, m=150, theta=40, Tmax=3000, ask="x"),
    S(q.g_altitude, h=500e3, mass=90),
    S(q.sat_period, h=2.0e7, unit="hr"),
    S(q.binary, M=5e30, d=2e9, unit="hr"),
    S(q.rocket_speed, h=600e3),
    S(q.equal_pull, Mb=8.0e22, d=3.8e8),
    S(q.escape, M=7.4e22, R=1.74e6, body="the Moon"),
    S(q.orbit_from_period, T_hr=8),
], seed=31)

INTRO = """
Practice Exam 3-1 follows the 2015 Exam 3 (its Ch 12 and 13 questions, #1–5 and #9–13) with new numbers, plus lecture-note examples: the diving board, the seesaw, the wall beam with a cable, and the orbit altitude from a period. Question 2 is a **maximum**: pick the largest choice that still works. Every question is a procedure worked in the notes or on the 2015 exam.
"""

if __name__ == "__main__":
    build(1, Q, INTRO)
