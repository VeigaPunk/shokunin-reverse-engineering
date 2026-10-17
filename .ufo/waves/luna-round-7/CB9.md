## CLAIM

No round-7 draft sneaks a Lessons-index row in: none proposes a `## Lessons` entry or a `corpus/lessons/` artifact for the six 6.5.0 entries, and none alters the pre-existing `lessons/round-13-distillation` token (`corpus/README.md:131`); command A's 78/78 claim is unaffected by the lessons index.

## METHOD

Read-only at HEAD 411175e. Sweeps: `grep -rin 'lesson' .ufo/waves/luna-round-7/`; `grep -rn 'Lessons|round-13-distillation|corpus/lessons'`; row-shape sweep `grep -rn '^| '`; `grep -rn '2026-10-16-round'`; `grep -rnw 'gist'`. Read all in-scope drafts: E1D–E6D, G1–G6, Z1–Z6, M1/M2, K3/K4, plus L1/P0/C5. Mechanical section check via `git show HEAD:corpus/README.md` with command A's coverage-map regex `2026-10-\d{2}-[a-z0-9-]+` (`SCORECARD.md:101-102`).

## FINDINGS

- Pattern sweeps: only `F8.md:8`, `K4.md:14`, `P0.md:8`, `L1.md`, `C5.md:8` mention lessons; each preserves the index or rules additions out. No `2026-10-16-round*` token and no `gist` column proposal anywhere in the wave.
- Every proposed insertion in E1D–E6D, G1–G6, Z1–Z6, M1/M2, K3/K4 targets the coverage map (before `## Knowledge`: `M2.md:8-12`, `P0.md:8`) or the Knowledge table (after its last row: `K3.md:8-10`, `K4.md:10-12`); none targets `## Lessons` (`corpus/README.md:141-152`).
- `P0.md:8`: "No lessons digest is assigned; leave Lessons index unchanged." `C5.md:8`: preserve the legacy token "and position."
- Measured at HEAD: coverage-map tokens=72, none lessons-typed; Knowledge rows=73, exactly 1 lessons-path row (`corpus/README.md:131`); Lessons rows=7 (`:145-151`). Command A reads only the `## Coverage map` section, so the legacy Knowledge-table token cannot alter mapped/missing/dangling or coverage_score=10.0.

## THREATS

Draft-scope verification only; the landed README does not yet exist, and command A cannot detect a mis-placed row outside the coverage map (a Lessons row would be invisible to it). `K4.md:14`'s "79 rows" is a Knowledge-table count (72+6+1 legacy), not a command A field. Separately, `F8.md:8` notes M1's underscore map tokens (`M1.md:11-13`) would break mapped=78 if landed; hyphen map rows (`P0.md:8`, `E4D.md:10-12`, `E6D.md:21-23`) are required — not a lessons-index issue.

## VERDICT

CLEAN — no draft introduces Lessons rows or `corpus/lessons/` artifacts; all six entries are routed to Knowledge + coverage map, and the legacy lessons token is preserved untouched.
