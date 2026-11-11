# PHYS1408 — course-specific exam prep rule

This adds to `../../CLAUDE.md` (school-wide rules). Where the two conflict, this file wins for PHYS1408.

## Only procedures the professor has shown

Every live-exam question is one of the problems worked in the professor's lecture notes (`Professors-Notes/Chapter N ….pdf`) or on the previous exam for that unit (`Professors-Notes/exam N-….pdf`), or a combination of them. The live version changes only the **numbers and names**, never the procedure.

So every practice question, driller, study-guide section, and **notecard** entry must be one of those worked problems, solved by the same procedure for the same unknown. Concretely:

- **No reverse-direction variants** (solving for a different unknown than the source problem did). This overrides the school-wide "include reverse-direction problems" rule. If the notes themselves run a problem both ways (e.g. Ch 13 p. 7 height from speed, p. 8 speed from height), both directions are allowed.
- **No formula-only topics.** A formula or definition the notes state but never use in a worked problem (e.g. Ch 12 shear and bulk modulus) is not tested.
- **No concept questions.** The previous exams are all calculation.
- **No outside numbers or facts** beyond what a question states.

The exam is 50 minutes with a 3×5 notecard, so the notecard must hold the solution for every allowed problem type, and nothing else.

Exam 3 enforces this in code: `practice-exams/exam-3/_scripts/gens.py` raises `NotOnExam` for banned generators and variants.
