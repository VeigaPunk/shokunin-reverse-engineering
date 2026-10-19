# EX-25 — probe interplay post-landing: citation-drift probe at HEAD vs the C2 census edit

Seat EX-25 · chain c2 · role executor · wave arc3-loop1-round2 · 2026-10-19.
Artifact type: probe interplay dossier (task: *"probe interplay post-landing:
citation-drift probe at HEAD → findings=0; the census edit must not stale any
pinned needle"*).

Typed claims under test:

1. **Probe-clean**: the citation-drift probe at HEAD reads `findings=0 exit=0`
   after EX-16's census edit lands (worktree state), in both modes, with the
   frozen-run guard intact.
2. **Needle-invariance**: the census edit stales no pinned needle — i.e. every
   needle in `pointer-table.json` still resolves against byte-identical bytes.

## 0. Verdict

Both claims verify, on measured evidence:

- Probe post-landing: `CITATION_DRIFT_VERDICT: reported findings=0 exit=0`
  (probe mode) and `clean findings=0 exit=0` (`--strict`); selftest 13/13.
- Needle-invariance: 35 needles → 17 distinct target files, **none** under
  `.ufo/gates/`; all 17 byte-identical between worktree and HEAD blob both
  pre- and post-landing; the census landing changes exactly one file and that
  file is not a needle target. Table digest `738b3a56…` still equals its
  `expected.json` pin; `expected.json` and the probe script are byte-unchanged.
- The census's own clean-tree reading is invariant under its edit (loci
  6/9/2, PASS 0/0/0/0 before and after), so the shared read surface the two
  instruments watch (SCORECARD.md:56-60 is census-CURRENT scope *and* carries
  needles sc59-stanza-key-anchor / sc59-receipt-stamp) is stable.
- Positive control: the probe **would** catch a census-file pin if one existed
  (synthetic needle into `c1-census-v10.py:560` → `citation_out_of_range`,
  HEAD blob 490 lines) — so `findings=0` is a live measurement, not a vacuous
  one.

## 1. Identity of the landed artifacts (read-only captures)

| Object | Pre-landing (HEAD `14b1682`) | Post-landing (settled worktree) |
|---|---|---|
| `.ufo/gates/c1-census-v10.py` | `6f1d19ff…`, 490 lines | `82fb807e79963f6dc6b9d055ab7378464b3636adfb498e5b615393f5f47c57aa`, 560 lines, 28,606 B, mtime 2026-10-19 09:06:50 -0300 (`+80/-10`, 1 file) |
| `.ufo/gates/citation-drift/pointer-table.json` | `738b3a56…` | `738b3a56…` (unchanged) |
| `.ufo/gates/citation-drift/expected.json` | `ff47bfd6…` | `ff47bfd6…` (unchanged) |
| `.ufo/gates/citation-drift/citation-drift-probe.py` | `e2665074…` | `e2665074…` (unchanged) |

Settle proof: the census hash moved twice during EX-16's write
(`6f1d19ff → 7b5a0e88 → 1431620f → 59975ae0 → 82fb807e`); two samples 50 s
apart, 12:07:28Z and 12:08:18Z, are identical at `82fb807e…`. EX-16's own
`receipts/after/after-sha256.txt` (captured 12:06:58Z) independently records
`82fb807e…` / 560 lines — the fresh-identity discipline holds (the artifact
does not inline its own stale hash; the hash lives in its receipt).

## 2. Probe runs (evidence files in this directory)

- `probe-head.out`, `probe-head-strict.out`, `probe-selftest.out` (pre-landing,
  09:05Z): `reported findings=0` / `clean findings=0` / `13/13 CLEAN`.
- `post-landing-probe.out` (12:09Z, after the hash settled): probe mode
  `reported findings=0 exit=0`; `--strict` `clean findings=0 exit=0`;
  selftest `cases=13 passed=13 failed=0 exit=0`.
- `hashes.txt`, `post-landing-hashes.txt`: instrument digests, before and after.

## 3. Needle-invariance analysis

Needle inventory (mechanical, from `pointer-table.json`): 31 `entries` + 4
`quoted` = 35 needles over **17 distinct target files**:

```
PROVINCE.md  SKILL.md  SCORECARD.md  SHONEN.md  LOG.md  corpus/README.md
corpus/QUALITY.md  corpus/knowledge/{2026-10-13-mcp-registrations,
2026-10-13-r4-12-godot-arm64-scale, 2026-10-13-r4-16-frontier-rescan,
2026-10-18-arc2-r6-pe-midrung, 2026-10-18-arc2-r7-pe-wall}.md
corpus/lessons/2026-10-15-round-1.md  evidence/round-1-2026-10-15/rea-bundle.json
.ufo/waves/arc2-loop1-round3/receipts/config-pre-pair.txt
.ufo/waves/arc2-loop1-round8/E2.md
.ufo/waves/arc2-loop1-round8/receipts/r8-ctl-envelope.json
```

Findings:

- No needle's `file` or `target` is `.ufo/gates/c1-census-v10.py`; no needle
  target is under `.ufo/gates/` at all. The census landing's blast radius
  (one file, `+80/-10`) is disjoint from the needle resolution set.
- Worktree-vs-HEAD byte identity for all 17 targets: **17/17 identical**,
  measured both before and after the landing (`worktree==HEAD for 17 of 17 …
  differing: []`; re-run post-landing identical). This includes SCORECARD.md,
  whose lines :59/:60/:68-72/:270/:622/:699 carry needles and which the census
  declares in CURRENT/DATED scope — neither instrument's shared surface moved.
- Frozen-run guard: table digest unchanged and still equal to the
  `pointer_table` pin in `expected.json` ⇒ no re-pin obligation; the edit did
  not touch the table, so the guard's "any table edit re-pins in the same
  commit" rule is not triggered.
- Positive control (`synthetic-needle-control.out`): with a synthetic table
  (re-pinned in a copied `expected.json`), a needle
  `{"id":"synthetic-census-pin","file":".ufo/gates/c1-census-v10.py","line":560}`
  reports `citation_out_of_range … beyond EOF (490 lines)` (findings=1, probe
  exit 0). Two facts follow: the probe's detection path reaches a
  census-file pin, and the probe grades **git objects at `--rev`**, so a
  worktree-only edit is invisible to it until committed. `findings=0` post-landing
  is therefore "no needle target changed", measured — not blindness.

## 4. Instrument-side corroboration on the settled census

Clean-tree invariance (the census reads the worktree; trees are scratch copies
from `git archive HEAD` under `/var/tmp/ex25/`):

- Pre-edit census on clean tree: PASS 0/0/0/0, loci 6/9/2 (`landed-census-clean.out`).
- Landed census on lane root: PASS 0/0/0/0, loci **6/9/2** (identical),
  `UNREADABLE []`, `G2 … ok (current-ok loci=5, total loci=17, floor=1)`,
  `DECLARED FAIL CLASSES: []` (`landed-census-clean.out`).

Fail-closures fire on the landed instrument (fixture confirmations; EX-16's
own before/after receipts cover the same classes in their directory):

- absent scoped file: `atk-h1` (SKILL.md absent) → `UNREADABLE
  ['SKILL.md: FileNotFoundError']`, `DECLARED ['UNREADABLE']`, **FAIL exit 1**
  — versus the pre-edit v10 run on the same tree: silent `lines=0 loci=0`
  **PASS exit 0** (`sim-matrix.txt` entry C/B).
- truncated file: SKILL.md at 19 lines (< declared max 20) → `UNREADABLE
  ['SKILL.md: 19 lines < declared max 20 (rows beyond EOF)']`, FAIL exit 1
  (`landed-census-atk-trunc.out`).
- blind instrument: needles neutered (PIN/VER/PTR → `(?!)`) → loci 0,
  `G2 … SUSPECT (… floor=1)`, `DECLARED ['BLIND-INSTRUMENT']`, **FAIL exit 1**
  (`landed-blind-atk-h3.out`) — versus the pre-edit neutered v10 run: silent
  **PASS exit 0**.

## 5. Interplay notes / residuals (named, not closed here)

- **HEAD-vs-worktree asymmetry**: the probe is blob-scoped; the census is
  worktree-scoped. Post-landing "probe findings=0" therefore constrains what
  the *commit* will do, not the uncommitted edit. After the parent's work
  commit, needles re-resolve at the new HEAD: all needle-pinned lines sit far
  from EOF (SCORECARD max pinned :699 of 1417; LOG quoted :1012) and the
  records convention appends — so `findings=0` is expected to persist, but
  that is an expectation, not a measurement, until a commit exists. Re-run
  `citation-drift-probe.py --root . --rev <work-commit>` then.
- **Census-internal line drift**: the edit moved the census's own anchors
  (pre → post): `def main()` 427 → 478; `out, counts, filelines, unreadable`
  438 → 489; truncation check new at :499; `g2_ok` 453 → 518
  (`census-line-map.txt`). No needle pins the census, but round-1 patch texts
  citing census internals (`RV-11` :382-390/:397-398) are now doubly stale —
  quotes into an instrument's own body must be revision-anchored per the
  rule-#14 discipline. Named for the chain; not a needle-staleness.
- **Per-needle partial blindness** (e.g. PIN alone neutered keeps loci > 0) is
  EX-16's declared H4 residual (their `receipts/after/h3-blind-pin.out`);
  outside this seat's interlock scope and left named.
- EX-16's seat report had not landed in `seats/` at write time (12:10Z);
  measurements above come from the artifact itself plus EX-16's receipts
  (same recorded identity). Gap named, not filled.

## 6. Scope discipline

Wrote only `seats/EX-25.md` and files in `claims/c2/EX-25/`. Scratch (trees,
neutered instruments, synthetic table) under `/var/tmp/ex25/`; no `/tmp` use.
No git mutations; the census and custody paths read-only. The synthetic table
and its expected copy exist only in scratch; their digests are recorded here:
synth table sha256 `c6d5d068…`, and the control's findings line is in
`synthetic-needle-control.out`.

## 7. Addendum — revision re-derivation (append-only), 2026-10-19 12:13Z

EX-16 revised the instrument again after §1's capture, so §1's post-landing
identity (`82fb807e…`, 560 lines) is SUPERSEDED, not wrong: it was the settled
state at 12:07–12:08Z. Observed revision chain: `6f1d19ff → 7b5a0e88 →
1431620f → 59975ae0 → 82fb807e → c95a5cf3 → df9ffdf9`.

FINAL measured revision (two 45 s-apart samples identical at 12:12:06Z and
12:12:51Z; EX-16's `receipts/after/after-sha256.txt`, re-captured 12:12:15Z,
declares it "r9 final"): `.ufo/gates/c1-census-v10.py` sha256
`df9ffdf963efa549f55c65770bca25120513015fe3b01c150a1087e0cf8e6b43`, 601 lines,
`+121/-10` vs HEAD; py_compile ok.

Battery re-run at `df9ffdf9` (receipt files in this directory now carry the
final-revision outputs):

- census on lane root: PASS 0/0/0/0; G2's floor is now per-file —
  `ok (current-ok loci per file: PROVINCE.md=17, SCORECARD.md=14, SKILL.md=3;
  total loci=17; floor=1/file)`; `UNREADABLE []`, `DECLARED FAIL CLASSES []`.
- absent-SKILL fixture: FAIL exit 1, `UNREADABLE ['SKILL.md: FileNotFoundError']`,
  `DECLARED ['UNREADABLE']`.
- truncated SKILL (19 < declared 20): FAIL exit 1, `UNREADABLE ['SKILL.md: 19
  lines < declared max 20 (rows beyond EOF)']`.
- neutered needles: FAIL exit 1, `G2 … SUSPECT (… floor=1/file)`,
  `DECLARED ['BLIND-INSTRUMENT']`.
- probe: `reported findings=0 exit=0`, `clean findings=0 exit=0`,
  selftest 13/13 (`post-landing-probe.out`).
- needle targets: worktree==HEAD **17/17**; digest trio unchanged
  (`738b3a56…` / `ff47bfd6…` / `e2665074…`).

Both typed claims hold at the final revision. Integration duty (named): re-run
`citation-drift-probe.py --root . --rev <work-commit>` once the parent commits —
the probe is blob-scoped, so only a commit is a landing it can verify.
