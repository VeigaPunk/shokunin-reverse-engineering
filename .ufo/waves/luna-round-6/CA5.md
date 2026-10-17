## CLAIM
This round must leave PROVINCE Core rows, corpus map rows/tokens, and held-surface status unchanged. The 10-leg battery measures; no successful output alone promotes a surface or changes client pins.

## METHOD
Read `PROVINCE.md:8-32,38-70`, `corpus/README.md:11-61`, `SCORECARD.md:88-124`, and round-5 guard `.ufo/waves/luna-round-5/X1.md:42-47`. At HEAD `f0e8cde`, `git status --short --branch` showed no tracked changes (only untracked `.ufo/interactive-sessions/` and `.ufo/waves/`); `git diff --exit-code -- PROVINCE.md corpus/README.md SCORECARD.md LOG.md` emitted no diff. A read-only `git show HEAD:corpus/README.md` token count returned `72`. No probes, command A, or config checks were run.

## FINDINGS
- `PROVINCE.md:28-32` explicitly distinguishes catalog availability from held capability: Core movement needs an end-to-end probe plus a `LOG.md` entry citing `evidence_id` and subject SHA-256. Therefore do not add or rewrite Core rows, statuses, evidence claims, or held surfaces from this measurement battery (`PROVINCE.md:38-62`).
- Do not revise per-client registrations based on a 6.5.0 test: `PROVINCE.md:8-24` records Devin/OMP at 6.5.0 and Kimi at 6.4.0.
- Preserve the coverage map in `corpus/README.md:11-61`. Prior guard `X1.md:42-47` requires byte-identical map rows, unchanged 72-token set, and unchanged command A; the recorded control is 72/72 mapped, 9/9 citation-resolved rules, 10.0/10.0. `SCORECARD.md:88-124` defines command A as source-derived, not a probe.

## THREATS
This is a snapshot scope audit, not proof of end-of-round immutability. I did not run command A or inspect before/after operator-config hashes; those outcomes remain unverified here.

## VERDICT
CLEAN