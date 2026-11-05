# ConnectorOverlap — read-only overlap scan and synthesis (round 97, wave 1)

Seat: ConnectorOverlap (connector). Lane: /home/vgpnk/Projects/shokunin/kaidoku-shokunin.
Declared axes: calibration, depth. Freeze: e859a88d78567c44bc1ecfd211afe123755ae1c7. Landing: 867ed98d85f45a18265441c1760386ef353b3d43.
Base revision: 2a54af0785f75d50912e1136443c8e78e62adf27.

## 1. Sibling receipt-writer defect (kake-shokunin)

- `git -C /home/vgpnk/Projects/shokunin/kake-shokunin cat-file -p bde9869144f69c5a459c0d2c93f5135922fe3a8d`:
  EXISTS (object type: commit, author: protocol-shokunin 1793899548 -0300; subject: "round-95 verifier spot-check (integrator, hyaku): non-author admit/reject"; commit diff adds `corpus/lessons/round-95-verifier-spotcheck.md`).
- `git -C /home/vgpnk/Projects/shokunin/kake-shokunin grep -n 'tmp' -- scripts/instrument_receipts.py`:
  - Line 47: `comparison, so ``c69_tmp_honour.py`` — which only passes ``--selftest`` to`
  - Line 107: `".ufo/waves/round-69/c69_tmp_honour.py",`
  - Line 108: `".ufo/waves/round-72/c72_tmp_v2.py",`
  - Line 109: `".ufo/waves/round-73/c73_tmp_v3.py",`
  - Line 643: `temporary = destination + ".tmp"`
- Verification: in kake-shokunin's current HEAD, `write_receipt` (lines 643–646) still opens predictable `<destination>.tmp` for writing:
  ```python
  643:    temporary = destination + ".tmp"
  644:    with open(temporary, "w", encoding="ascii", newline="\n") as handle:
  645:        handle.write(text)
  646:    os.replace(temporary, destination)
  ```
  It lacks `tempfile.mkstemp` (predictable name collision and symlink hijacking risk), file-level `os.fsync(handle.fileno())` before replace, and directory-level `os.fsync(dir_fd)` after replace (S322 / Row 192 defect).

## 2. Other lanes: round-97 scope and path overlap

- `grep -l 'round-97' /home/vgpnk/Projects/shokunin/*-shokunin/.ufo 2>/dev/null`: 0 matches (wildcard targets directories).
  Recursive scan across all sibling `.ufo` trees:
  - `revenger-shokunin`: active `.ufo/waves/round-97/` (C1 coverage via v6 admission counter, C2 calibration via forge reach).
  - `lore-shokunin`: historical round-97 records (currently round 102).
  - `souji-shokunin`: `sibling-overlap-table.tsv:436` records `kaidoku-shokunin/tools/round-97/stop-boundary-repair-battery-v7.py:6` as independent scope.
  - Others: historical mention / scout notes in kake, kengaku, kotoba, mado, mori, tabi, tameshi.
- Fleet prompt files: only two exist under `/home/vgpnk/Projects/shokunin/.ufo/prompts/`:
  - `/home/vgpnk/Projects/shokunin/.ufo/prompts/kaidoku-round-97.md`
  - `/home/vgpnk/Projects/shokunin/.ufo/prompts/revenger-round-97.md`
- Path overlap audit:
  - Revenger round-97 counters: `reports/round-97/c1_k_admit_counter6.py`, `reports/round-97/forge_reach6.py`.
  - Revenger round-97 fixtures: `reports/round-97/controls/`, `reports/round-97/forgeries/` (19 deltas).
  - Kaidoku round-97 instruments: `tools/round-97/stop-boundary-repair-battery-v7.py`, `tools/round-97/kill-rule-v3.py`, `tools/round-97/craft-citation-v2.py`, `tools/round-97/depth-blocks-v4.py`.
  - Kaidoku QUALITY rows 195–196: Row 195 (line 335), Row 196 (line 337); lines 195–196 (Row 122).
  - Result: 0 overlapping paths. Complete independence between kaidoku and revenger claims.

## 3. Sibling QUALITY check for blob-bound receipt pins

- Command: `git -C <lane> grep -n 'cat-file blob' -- corpus/QUALITY.md`
  - `souji-shokunin`: 0 hits (exit 1). (Uses `cat-file -e <landed>:<path>`, Q29/Q101).
  - `tsukuroi-shokunin`: 0 hits (exit 1). (Uses `cat-file -e <rev>:<path>`, rule 104; `cat-file -t <oid>`, rule 107).
  - `chousa-shokunin`: 0 hits (exit 1). (Uses `--rev <40-hex>`, rules 153/155).
  - `kengaku-shokunin`: 0 hits (exit 1). (Uses `git cat-file -e <rev>^{commit}` + `git show <rev>:<path>`, Q62).
  - `kumitate-shokunin`: 0 hits (exit 1). (Uses `cat-file -e <rev>^{commit}` / `<tip>:<receipt>`, Q51/Q52).
- Total sibling hits: 0 across all 5 lanes. Kaidoku's Row 195 is the sole fleet criterion enforcing `git cat-file blob <revision>:<path>` to defeat dirty working-tree counter substitutions.

## 4. Synthesis and proposed move

- Evidence:
  1. C1 hardened `stop-boundary-repair-battery-v7.py:90-114` and `kill-rule-v3.py:97-120` with atomic durability (`tempfile.mkstemp` + `os.fsync(fh.fileno())` + `os.replace` + `os.fsync(dfd)` per S322/S323) and blob binding (`git cat-file blob` per Row 195).
  2. In contrast, C2 instruments `tools/round-97/craft-citation-v2.py:382-384` and `tools/round-97/depth-blocks-v4.py:297-299` still write `--json-out` via bare, non-atomic, non-durable `with open(args.json_out, "w", ...) as fh: json.dump(...)`.
  3. CriticC2 discovered that `craft-citation-v2.py` tests keyword restatement across `"|".join(row)` (row-wide) rather than the criterion cell specifically (`row[-1]`), and both depth/craft parsers process raw `|` tables inside code fences.
  4. Sibling lanes (`kake-shokunin` scripts/instrument_receipts.py:643-646) retain the un-fsynced predictable `<dest>.tmp` defect, while 5 sibling QUALITY tables lack `cat-file blob` pin binding entirely.
- Affected axes:
  - `calibration` (improved): eliminating C2's non-atomic `--json-out` write brings depth receipts to the same crash-durability and symlink-immunity standard established in C1 (Row 189, Row 192, S322, S323).
  - `depth` (improved): scoping craft keyword restatement to `row[-1]` and excluding code fences prevents false-green craft/depth verdicts without affecting valid tables.
  - No axis harmed: coverage, freshness, and operability remain intact.
- Proposed move:
  In Round 98, port C1's durable `write_receipt` implementation into `craft-citation-v3.py` and `depth-blocks-v5.py`, restrict criterion restatement to `row[-1]`, and publish a cross-lane recommendation for `kake-shokunin` (adopt mkstemp+fsync) and `souji/tsukuroi/chousa/kengaku/kumitate` (adopt Row 195 `git cat-file blob` binding).
- Risks:
  Opening directory file descriptors for `os.fsync(dfd)` requires read access on directory path; C1 v7 proved this pattern portable on POSIX/Linux.
- Verification:
  Selftest in `depth-blocks-v5.py` and `craft-citation-v3.py` validating that symlinked `--json-out` paths are refused and receipts remain complete JSON or absent across mock exceptions.
