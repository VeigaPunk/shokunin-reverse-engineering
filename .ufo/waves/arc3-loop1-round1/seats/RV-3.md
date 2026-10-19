# Seat report — RV-3 | chain c1 | role reviewer

Wave: arc3-loop1-round1 (kaidoku-shokunin) | Date: 2026-10-19 | Status: COMPLETE.
Seat task (frozen): grade `knowledge-entry.patch.md` against `corpus/QUALITY.md` criteria
and the r3-07 entry's structure; list required fixes (or accept). Verdict + grade in
`claims/c1/RV-3/quality-grade.md`.

**Verdict: ACCEPT-WITH-FIXES** on the pinned revision (patch artifact sha256
`d662c195d75cdbdb07e3534170ce9cb2ac3f830b93d5380e7b8310bca7d8ba59`, 18,701 B, mtime
07:14:01 -03). No hard gate fails. Two one-line fixes: (1) the entry's `recheck:` line
needs a TMPDIR redirect to reproduce on this host; (2) an accuracy line about the `ev_` id
domain (EX-09 measured what the entry says was not measured). Full criterion table in the
grade file.

## 1. Work performed (each bullet carries an evidence pointer)

- Read the frozen rules (`claims-frozen.md:1-104`), the quality bar
  (`corpus/QUALITY.md`, 15 admission rows + 6 signals), the r3-07 structural precedent
  (`corpus/knowledge/2026-10-13-r3-evm-interface.md`, incl. errata `:149-155`), and the
  wave's authoring contract (`claims/c1/PL-1/plan.md:269-280`).
- Built grading infrastructure outside the repo (scratch `/home/vgpnk/.cache/rv3-arc3/`;
  deviation from the `/tmp` rule — `/tmp` is usrquota-exhausted fleet-wide, `EDQUOT`
  reproduced by `printf` and by `patch` itself): an extracted HEAD tree
  (`git archive HEAD corpus/knowledge corpus/README.md SKILL.md`, 1.4 MB), a
  working-tree variant of SCORECARD recipe A (`cmdA-worktree.py`), a patch applier, a
  per-file diff tool, and a criterion checker (`check-entry.py`). Harness self-tested
  against three states (token+file = 82/82; token-only = dangling; file-only = missing).
- Independently verified the evidence base before grading (pre-registered in
  `claims/c1/RV-3/independent-verification.txt`): keccak recompute of the Smoke K=5;
  recomputed all five KdxToken artifact hashes; byte checks at all 11 reported offsets
  (`5b` each); selector occurrence counts (`grep -o … | wc -l`); KdxToken CBOR trailer
  (`000825` + `1220`); `soljson.js` sha256 `221d7a66…` vs EX-02's receipt.
- Polled for the artifact (background loop, 60 s cadence; found at check 8 ≈ 07:15) and
  graded two revisions: the 07:11 revision (16,454 B) and the current 07:14 revision.
- Graded the current revision end-to-end: applied to a pristine HEAD copy
  (`/home/vgpnk/.cache/rv3-arc3/patched2`), recipe A, per-file sha256 diff, criterion
  checks, citation sweep, and a verbatim run of the entry's own `recheck:` command.
- Preserved the recheck evidence in-lane: `claims/c1/RV-3/evidence/recheck-verbatim.out`
  (failure, 678 B), `recheck-fixed.out` (success, 9,399 B).

## 2. Proposed changes

- Patch-text artifacts proposed by this seat: **none** (reviewer; the two fixes below are
  instructions to EX-12/parent, each a one-line edit).
- Required fix 1 — entry `recheck:` line (applied-file line 7): add a writable TMPDIR
  (e.g. `cd <writable-dir> && TMPDIR=<writable-dir> npx -y rea-agents@6.4.0
  inspect-evm-interface <abs path> hex --format json`). Evidence: verbatim run exits 1
  `execution_failure` (worker EDQUOT); with `TMPDIR=/var/tmp/rv3-tmp` it exits 0 and
  reproduces `ev_45849c8b…`, 5/5 `dispatch:"abi"`, decoded `c1081a56…`, offsets
  89/137/167/215/263.
- Required fix 2 — id-domain sentence (applied-file lines 21/28): "was not measured" is
  stale; cite `claims/c1/EX-09/rerun-compare.md` §5 (bit-exact re-derivation of
  `ev_4dd5ea20…`; display fields excluded; path-keyed) or scope the sentence.
- Recorded, no action: the 07:11 revision's §4 carried a stale entry identity
  (claimed 8,316 B / `f95c5a05…`; actual apply 8,598 B / `d8d85949…`); the 07:14
  revision matches its §4 exactly (9,513 B / 32 lines / `a5119120…`).

## 3. Before → after measurement (chain C1 claim: knowledge 81 → 82)

- Before (HEAD `e845c2b`, recipe A verbatim from `SCORECARD.md:88-124`):
  `{"knowledge_files": 81, "mapped": 81, "missing": [], "dangling": [],
  "citation_resolved_rules": 13, "rule_blocks": 13, "coverage_score": 10.0,
  "depth_score": 10.0}` — matches EX-11's `command-A-before.txt`.
- After (current patch applied to a pristine tree, same recipe semantics):
  `{"knowledge_files": 82, "mapped": 82, "missing": [], "dangling": [],
  "citation_resolved_rules": 13, "rule_blocks": 13, "coverage_score": 10.0,
  "depth_score": 10.0}`.
- Prior-81 byte-identical: per-file sha256 over `corpus/knowledge/` — all 81 unchanged;
  tree diff shows only the one added file + `corpus/README.md`.
- Map edit line-neutral: README 190 → 190 lines; `corpus/README.md:38` gains
  `` `2026-10-19-arc3-r1-evm-real-solc` `` (byte-identical to RV-4's frozen token patch).
- Entry self-identity: applied file 9,513 B / 32 lines /
  `a5119120ee6a6142b8be6e297e39c85e0464fb27761c6ee0e7cc7cf8a1d5e56b` — matches the
  artifact's §4 claim.

## 4. Attacks / refutations attempted, with verdicts

| attack | result |
|---|---|
| apply patch to pristine HEAD, re-measure | PASS — clean apply; 82/82; prior-81 intact |
| token/file stem mismatch (three candidate names in the wave) | PASS on the frozen stem; RV-4's frozen patch + records drafts + this entry agree |
| fabricated citations (9 `ev_` ids, 18 hex tokens, 34 paths) | PASS — all resolve; §10's self-attack claim reproduced (33/34 with the 34th a name-only reference) |
| entry self-identity sha | PASS on current revision; FAIL caught on 07:11 revision (recorded) |
| recheck reproducibility | FAIL as written (EDQUOT `execution_failure`); PASS with TMPDIR — Fix 1 |
| id-domain statement vs EX-09 | CONTRADICTED — Fix 2 |
| ABI↔probe consistency (args/mutability) | PASS — Rv2Token probe payload equals the compiled ABI for all 5 |
| zero-false-positive claims | PASS — Rv2Many 11/11 no extras; Rv2Token's sole non-dispatch PUSH4 `16ee4b79@1900` unreported (EX-07 m1) |
| "re-run dressed as a move" (CR-c) | PASS — delta bullet cites r3-07:59-70 and matches the stub's `pure`/empty output |
| pre-probe K timing | PASS — expected-selectors.txt 41.6 s before the first envelope ("42 s") |
| structure vs r3-07 | modern template (l7-01/arc2-r7 precedent) with r3-07's load-bearing elements present; r3-07 section names not required — no fix |

## 5. Blockers

- `/tmp` usrquota exhaustion (fleet-wide, reproduces by `printf` and breaks `patch`
  mid-write): scratch moved to `/home/vgpnk/.cache/rv3-arc3/` (outside the repo) and
  `/var/tmp/rv3-tmp`; the deviation is recorded here. Scratch is cleaned after close.
- None blocking: the graded revision's content verifies end-to-end; the two fixes are
  one-line edits that do not affect the measured before→after numbers (the map token and
  file stem are untouched by both fixes).
