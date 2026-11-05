# ExecReproC1 — independent reproduction of R99-C1 (round 99, attempt 1)

Seat: ExecReproC1 (executor, lane kaidoku). Scope: reproduce and attack R99-C1
(calibration, self-assessment mismatches 17 -> 0). No re-freeze, no re-pin, no scoring.
Scratch /fast/scratch/hyaku/kaidoku-r99/ExecReproC1 used and trap-deleted on exit
(confirmed gone: `ls` -> "No such file or directory"). No tool installed (none needed);
no pacman transaction touched; no host parameter changed. All git mutations were inside
my own clones/fixtures only; the lane was touched read-only plus my wave directory.

## Setup evidence

- `git clone --shared /home/vgpnk/Projects/shokunin/kaidoku-shokunin $S/clone`; checkout
  `--detach 8fb5ac4fa8d7b0cb5123b230e5d319a765011066` (freeze F); `rev-parse HEAD` -> 8fb5ac4fa...
- `git -C $S/clone rev-parse --show-toplevel` -> exactly $S/clone (asserted before every write).
- Frozen counter bytes verified before any run:
  `sha256sum $S/clone/tools/round-99/self-assessment-audit.py` ->
  `e732465bde4d7c125b45fc60ead9343ee6d1c73378830e42e028ac2d0334eec0` = `counter_sha256`
  in all three reference receipts.
- Lane HEAD observed at c19d57cd... (Bk) with 12 dirty files; all measurement was done in
  the detached clone at pinned revs, so the dirty tree never leaked in.

## 1. Frozen C1 command at B0, A, Bk (rc from `echo $?`)

Command (per leg): `python3 -I -B tools/round-99/self-assessment-audit.py --root $S/clone --rev <rev> --json-out <receipt>`, cwd = the F clone.

| rev | receipt (wave dir) | label (verbatim) | rc |
|---|---|---|---|
| B0 de098f51... | c1-at-B0.repro.json | `mismatches 17; head-score mismatch; head-fraction mismatch; map-rows 176 of 182; registry 0 of 9` met False | 1 |
| A 64cc3e10... | c1-at-A.repro.json | `mismatches 0; head-score ok; head-fraction ok; map-rows 182 of 182; registry 14 of 14` met True | 0 |
| Bk c19d57cd... | c1-at-Bk.repro.json | `mismatches 0; head-score ok; head-fraction ok; map-rows 183 of 183; registry 14 of 14` met True | 0 |

Field-by-field comparison (`compare.py` -> compare.json) of label, mismatches, exit, met,
rev, counter_sha256 against `.ufo/waves/round-99/pre/c1-do-nothing-at-base.json` and the
two `.ufo/waves/round-99/l1/scores/c1-at-<rev>.json` receipts: **B0 AGREE, A AGREE, Bk AGREE**
(zero differing fields).

## 2. Selftest

`python3 -I -B tools/round-99/self-assessment-audit.py --selftest` (cwd = F clone), rc=0;
stdout `SELFTEST cases=9 failures=0` (c1-selftest.repro.txt). Matches the claims file
("9 cases, 0 failures").

## 3. Forgery control rebuilt from scratch

`bash forgery.sh`: second shared clone, `checkout --detach de098f51...` (B0),
`git apply --whitespace=nowarn` of the copied `.ufo/waves/round-99/pre/c1-forgery-control.diff`
(copy kept as c1-forgery-control.diff), fixture commit in-clone only with
`-c user.name=fixture -c user.email=fixture@fixture.invalid`;
toplevel assert passed; fixture commit `c60a6a7b538d71d1dfbc4b5e0a32eded33ebf438`.
Counter (F bytes) with `--root $S/clone-f --rev c60a6a7b...`:

`mismatches 15; head-score ok; head-fraction ok; map-rows 176 of 182; registry 0 of 9` met False, rc=1.

Matches the contract's forgery control exactly (mismatches 15, head atoms fooled,
map-rows and registry unchanged, exit 1). Receipt: c1-forgery.repro.json.

## 4. Independent recount (own short script recount.py — NOT the counter)

All content read via `git -C $S/clone show/ls-tree <rev>:<path>`; receipt recount.json.
Definitions: stems = `corpus/knowledge/*.md` basenames minus `.md`; table row = line
starting `|` inside `## Coverage map` of `corpus/README.md` (slice ends at the next `^## `
heading), >= 3 cells, not a separator row; registry = direct-child `*.py` of
`tools/round-97|98|99`; pinned = the blob's full sha256 present in SKILL.md at that rev
(checked both "in a registry-section row carrying the backticked path" and "anywhere in
SKILL.md"; identical results).

| rev | stems | stems backticked in a table row | counter map-rows | registry pinned (own row) | counter registry |
|---|---|---|---|---|---|
| B0 | 182 | 176 | 176 of 182 | 0 of 9 | 0 of 9 |
| A | 182 | 182 | 182 of 182 | 14 of 14 | 14 of 14 |
| Bk | 183 | 183 | 183 of 183 | 14 of 14 | 14 of 14 |

**Full agreement with the frozen counter at all three revisions.** The B0 gap is exactly
the six stems the counter lists (`2026-11-05-r93-citation-semantics`, `-r93-fresh-pack-oracle`,
`-r94-receipt-path-json`, `-r95-receipt-world-binding`, `-r96-kill-rule-coverage`,
`-r97-receipt-byte-binding`); A adds exactly those six rows, Bk adds the r99 entry + row.

Definitional footnote (not a disagreement): a naive exact-`` `stem` `` substring read of
"backticked in a table row" yields only 141/147/148 because the map also references stems
as comma-separated backtick spans and as `` `knowledge/<stem>.md` ``; after handling those
documented reference styles (split spans on commas, strip `knowledge/` prefix and `.md`
suffix) the counts match the counter's A3 exactly. I also reimplemented A3's >= 20-char
residual test independently; it changes nothing at the three measured revisions
(stem-only rows exist only in the forgery, where A3 correctly rejects them).

## Attack notes (all survived)

- Head atoms: at B0 both head atoms mismatch (17 = 2 head + 6 map + 9 registry), matching
  the frozen base control; at A/Bk they flip to ok only after the SCORECARD head fraction
  is genuinely corrected at A — the forgery variant (edit 168/168 -> 182/182 in prose)
  fools the two head atoms but still scores 15, so the head atoms are not trivially
  forgeable without also passing A3/A4.
- Registry atom demands the full blob sha256 inside a conforming row (kind word, exit map,
  >= 10-char cell 4), not just path presence: the forgery's path-only rows score 0 of 9.
- Counter reads everything through `git show <rev>:<path>`, so a dirty worktree cannot
  influence a measurement (verified: measured revs while my clone cwd sat at F).

## Verdict

R99-C1 independently reproduced end to end: 17 -> 0 at A and held at Bk, exit codes and
labels byte-identical to the pre/L1 receipts, selftest 9/0, forgery control 15/exit 1,
and an independent recount of both A3 (coverage map) and A4 (registry) agreeing at B0, A
and Bk. Zero disagreements found. No tooling installed; nothing in the lane modified
outside my wave directory.

Evidence directory (all receipts, scripts and compare output):
.ufo/waves/round-99/w1/ExecReproC1/
