# R25 a3 wave 1 — C2Rerun (KaidokuR25a3.C2Rerun)

Seat: rerun of the R25-C2 counting command at three revisions, instrument sha256 pin
check, independent knowledge count, and hand check of SOURCES rows S075–S077.
All times UTC 2026-10-22. All conclusions below are `observation` unless labeled.

## 1. Instrument sha256 pin — holds

- Command: `git -C <lane> cat-file blob <REV>:tools/round-25/a2/c2-coverage.py | sha256sum`
  for the three revs, plus `sha256sum` on the working-tree file; compared against the pin
  recorded in `.ufo/waves/round-25/a2/claims.json` at 7ef837a473ae65d924b9ea34e7748f722a6cd7d5.
- Output (exit 0, ~10:43Z): all four hashes equal
  `7a7e6d6529033c5dfac6da252507ac597b30f0a3d4740522d17f87f4ee6b2c70`, byte-identical to the
  claims.json pin for `tools/round-25/a2/c2-coverage.py`.
- Verdict: holds. The script executed at every rev is the pinned instrument; no drift
  between the instrument commit 9dcd11e and lane tip 08c7a72.

## 2. Reruns of the counting command — before 107/0 and after 108/1 hold

- Command, per rev: `python3 -I -B tools/round-25/a2/c2-coverage.py --root <lane> --rev <REV>`
  (run ~10:43Z, exit codes observed).
- Rev 9dcd11ecb412fe4828f274580018039b8edbc05a (instrument/before rev): exit 1,
  `"knowledge_md": 107`, `"entry_present": false`, `"entry_sourced": 0`. Matches claims.json
  `before` {107, 0, exit 1}.
- Rev 0e333eb2fc25f538a99058761f379845f2534c42 (L1 C1 commit): exit 1,
  `"knowledge_md": 107`, `"entry_present": false`, `"entry_sourced": 0`. Still before-state;
  the C1 commit added no knowledge entry.
- Rev 08c7a7299ed61c3fdc30ddb0adfe4e812d5eac76 (L1 C2 commit, lane tip): exit 0,
  `"knowledge_md": 108`, `"entry_present": true`, `"cited_rows": ["S021","S075","S076","S077"]`,
  `"qualifying_rows": ["S075","S076","S077"]`, `"entry_sourced": 1`. Matches claims.json
  `target` {108, 1, exit 0}.
- Verdict: holds — before 107/0 at both pre-C2 revs, after 108/1 at the tip.

## 3. Independent knowledge count (git ls-tree) — agrees with the instrument

- Command: `git -C <lane> ls-tree -r --name-only <REV> corpus/knowledge/ | grep -c '\.md$'`.
- Output (exit 0, ~10:43Z): 9dcd11e → 107; 0e333eb → 107; 08c7a72 → 108.
- Verdict: holds. Independent count equals `knowledge_md` at every rev, so the
  instrument's `endswith(".md")` count over the recursive ls-tree is faithful.

## 4. Hand check of SOURCES rows S075–S077 — all three qualify at the tip

- Command: `git cat-file blob 08c7a72...:corpus/SOURCES.md` rows extracted per cell,
  and the entry blob's `source:` line (both ~10:44Z, exit 0).
- Extracted cells (awk -F'|', 13 fields per row, matching the instrument's parser):
  - S075: status `mined`, opened `2026-10-22`, used-by `corpus/knowledge/2026-10-22-r25-evm-selector-name-resolution.md, corpus/lessons/round-25.md`
  - S076: status `mined`, opened `2026-10-22`, used-by same two paths
  - S077: status `mined`, opened `2026-10-22`, used-by same two paths
- Entry `source:` line at the tip cites S075, S076, S077 and also S021 (Solidity ABI spec).
  S021 appears in `cited_rows` but not `qualifying_rows`, correctly, because S021's opened
  date is 2026-10-19, not 2026-10-22.
- Verdict: holds. Each of S075–S077 is `mined`, opened 2026-10-22, and names the entry in
  used-by, satisfying the instrument's qualifying rule; `entry_sourced=1` rests on real rows.

## 5. Order and working-tree sanity

- `git merge-base --is-ancestor` (exit 0, ~10:44Z): 9dcd11e is ancestor of 0e333eb, and
  0e333eb is ancestor of 08c7a72 — the three runs are a genuine before→C1→C2 progression.
- `git diff --quiet 08c7a72 -- corpus/SOURCES.md` clean: working-tree SOURCES.md equals the
  tip blob, so the hand-checked rows are the rows the instrument parsed.
- Instrument source review (read before running): it only reads Git objects
  (rev-parse/ls-tree/cat-file); it wrote nothing in the lane. `inference` from source, plus
  clean exit with no lane mutation observed.

## Result summary

| Rev | knowledge_md | entry_sourced | exit | claim state |
|---|---|---|---|---|
| 9dcd11e | 107 | 0 | 1 | before 107/0 — holds |
| 0e333eb | 107 | 0 | 1 | before 107/0 — holds |
| 08c7a72 | 108 | 1 | 0 | after 108/1 — holds |

Overall verdict: the R25-C2 counting claim reproduces exactly as frozen in
`.ufo/waves/round-25/a2/claims.json`; instrument pin intact; no counterexample found.

## Artifacts

- None beyond this report. Every command ran read-only in-place (`git` read-only
  subcommands and the instrument itself, which writes nothing); scratch seat
  /fast/scratch/hyaku/kaidoku-r25-a3/seats/C2Rerun/ holds only an empty tmp/ dir.
- No tools installed or upgraded (nothing needed beyond preinstalled python3/git/awk).

## Residual risk and verification gaps

- The instrument's qualifying rule is substring-based (`ENTRY in used_by`); a used-by cell
  could qualify a row for the wrong reason. Hand check shows the real cells are exact and
  sensible, so this did not fire here — but it bounds what a green run proves.
- This seat checks count and source linkage only, per the claims.json `limits` field: the
  entry's truth content is not verified here (other seats falsify content).
- S075–S077 cells were verified from the 08c7a72 blob by field extraction, not from the
  primary web pages; page-opening provenance belongs to the evidence seats.
