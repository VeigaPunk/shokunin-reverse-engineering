# ReviewerScope — frozen-bytes audit (round 97, wave 1)

Lane: /home/vgpnk/Projects/shokunin/kaidoku-shokunin. F = e859a88d78567c44bc1ecfd211afe123755ae1c7, L = 867ed98d85f45a18265441c1760386ef353b3d43, base = 2a54af0.
Scratch: /fast/scratch/hyaku/kaidoku-r97/ReviewerScope (clone detached at L, rev-parse verified = 867ed98d85f45a18265441c1760386ef353b3d43).

## Item 1 — diff F..L over frozen paths
Command: `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff --name-status e859a88d78567c44bc1ecfd211afe123755ae1c7 867ed98d85f45a18265441c1760386ef353b3d43 -- tools/round-97 .ufo/waves/round-97 plans/round-97-claims.md` → rc 0, exactly one line:
`A  .ufo/waves/round-97/pre/s323-rename2-fetch.html` (509 insertions; --stat agrees).
Every pre-existing C1/C2 file is byte-identical across F..L; no tools/round-97/*.py touched; plans/round-97-claims.md untouched.
**Verdict: PASS** — the landing added exactly one file (`pre/s323-rename2-fetch.html`) and modified nothing frozen.

## Item 2 — pins.sha256 at L
Command: `cd /fast/scratch/hyaku/kaidoku-r97/ReviewerScope/clone && sha256sum -c .ufo/waves/round-97/pins.sha256` → rc 0.
59/59 lines `OK` (4 tools/round-97 scripts, battery v7, mutants*.json 3x, c2 fixtures + manifests 6x, 13 forgery fixtures, pre receipts, 13 legacy tools/round-9x pins, controls). No non-OK line.
**Verdict: PASS.**

## Item 3 — frozen predicate string agreement
- plans/round-97-claims.md:40-42 — label “mutants killed 21 of 21; forgeries refused **17** of 17; negctl refused 3 of 3; probe consistent 1 of 1; honest accepted 1 of 1; wlink 2 of 2; durability 2 of 2; bytes 5 of 5; dirtyrefuse 1 of 1; ownrec 1 of 1”.
- tools/round-97/kill-rule-v3.py:733-736 label format builds the identical ordering/wording from `TOTAL_MUTANTS = 21` (L82) and `TOTAL_FORGERIES = 17` (L83); L739 `met` gate enforces the same 21/17/3/1/1/2/2/5/1/1 targets.
- `--expect` default = `FROZEN_LABEL` = the claims string verbatim.
**Verdict: PASS** — executable format and claims predicate agree.
**Finding (low):** kill-rule-v3.py:48 module docstring still reads “forgeries refused 13 of 13”While the executed label says 17 of 17 (item 3 documents this). It is a stale docstring inside the frozen instrument — byte-audit passes (present at F too), but it's misleading if cited as the predicate. Runtime `TOTAL_FORGERIES = 17` is correct (13 round-97 fixtures + 4 round-95 = 17, confirmed by mutants.json `forgery_reasons` keys and .ufo/waves/round-97/forgery 13 files plus .ufo/waves/round-95/forgery). **Action: none within freeze; flag as docstring drift for a future freeze-compatible sed.**

## Item 4 — mutant table shape
Command: python3 inspection of .ufo/waves/round-97/mutants.json → (`mutants` list length 22, names: M0, M1..M10, M-d1, M-w1, M-f1..f5, M-c1, M-p1, M-r1, M-r2 = 21 real + M0).
`kill_class` present on every entry; all 21 real are in {crash, semantic}; M0 carries `semantic`. Supplementary shape probe (all good): every `find` string is present exactly once in its target .py, both `mutants-before.json` and `mutants-before-noc1.json` are clean diffs of the canonical 22-entry table (paths/sizes recorded from the working tree, 5208 vs 5208 bytes), every forged fixture entry referenced by the frozen rule `kill-rule-v3.py` at the freeze rev F exists on disk AND has an intended refusus reason in the baked-in forge table, and `--decl` pins match the frozen rev F.
**Verdict: PASS.**

## Summary
- Item 1 diff: exactly one added file, nothing frozen modified → PASS
- Item 2 pins 59/59 OK → PASS
- Item 3 predicate executable/claims agree at 17 → PASS (docstring drift noted)
- Item 4 mutants table 22 entries, kill_class on all, 21 real + M0 → PASS

Findings: 1 (docstring “13 of 13” at tools/round-97/kill-rule-v3.py:48 — low severity, no effect on byte-freedom of instruments or on the C1 predicate itself).
