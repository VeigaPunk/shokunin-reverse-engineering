# Draft material for `corpus/lessons/round-99.md` (ScribeLesson, round 99 wave 1)

Draft only — not a corpus edit. Every claim below was executed by this seat; the command
lines and receipts are in `.ufo/waves/round-99/w1/ScribeLesson.md`.

## 1. `## Mistakes` — candidates, with the fix's ability to fail named

Shape follows `corpus/lessons/round-98.md` §Mistakes: class · evidence pointer · captured-by · fix.

- **M99-f · a counter whose verdict depends on a byte the receipt does not pin (own, this
  round).** `tools/round-99/self-assessment-audit.py` computes the head atoms (A1/A2) by
  importing `tools/round-66/coverage-selfcheck.py` **from the working tree**
  (`self-assessment-audit.py:54-59`, `load_cs()` reads `HERE/../round-66/coverage-selfcheck.py`;
  `HERE` is the tool's own directory, not `--rev`). The receipt's `tools` map pins 14 tools
  and does **not** include the round-66 recipe. Evidence: with the working tree at `Bk` clean,
  mutating the working-tree `tools/round-66/coverage-selfcheck.py` (`"mapped": len(mapped)` →
  `len(mapped) - 1`) and re-running the frozen command at the **same** `--rev` flipped the
  label from `mismatches 0` to `mismatches 2; head-score mismatch; head-fraction mismatch`
  (exit 1), and back to `mismatches 0` after `git checkout --`. A dirty tree under a clean
  revision name therefore changes the verdict. Captured-by: none of the committed round-99
  receipts — `c1-at-c19d57cd…json` records `counter_sha256` for the audit only.
  Fix: none landed; the recipe must be read through `git show <rev>:tools/round-66/…` and its
  sha256 pinned in the receipt (the QUALITY Row 195/196 byte-binding shape). Shown able to
  fail: the mutation above, not a committed receipt.

- **M99-g · a receipt written through a predictable name (own, this round).**
  `tools/round-99/self-assessment-audit.py:226` and `tools/round-99/pe-upx-trunc-battery.py:361`
  both write `<out>.partial` with a plain `open(tmp, "w")` and then `os.replace(tmp, out)`.
  A symlink planted at `<out>.partial` is followed: the run overwrote the victim file with the
  receipt bytes and left `<out>` as a symlink to the victim. Evidence: with
  `receipt.json.partial → victim.txt` planted, `self-assessment-audit.py --json-out
  receipt.json` rewrote `victim.txt` (2 130 B of receipt JSON) and `receipt.json` became a
  symlink to it; the same held for `pe-upx-trunc-battery.py --json-out rec.json`. The
  round-97/98 counters `v7`/`v8` do not have this defect: `write_receipt` uses
  `tempfile.mkstemp` in the target directory (`stop-boundary-repair-battery-v7.py:95`) and
  fsyncs the directory after the replace. Captured-by: no round-99 criterion — the frozen
  predicate is the label, and the label is unaffected by where the bytes land.
  Fix: the r99 counters should adopt v7's `write_receipt` (unique temporary name, dir fsync);
  the QUALITY Row 189/192 shape already states the rule. Shown able to fail: the planted-symlink
  probe above, not a committed receipt.

- **M99-h · a hardcoded selftest banner (own, this round).**
  `tools/round-99/self-assessment-audit.py:198` prints
  `print("SELFTEST cases=9 failures=%d" % len(fails))` — the case count is a literal, not
  `len(cases)`. Removing the `F8-unregistered-tool` case from the selftest body still printed
  `SELFTEST cases=9 failures=0` (exit 0), so the committed raw output
  `.ufo/waves/round-99/pre/c1-selftest.txt` ("SELFTEST cases=9 failures=0 / rc=0") cannot
  distinguish nine cases from eight. `v7` and `v8` print `len(results)`
  (`stop-boundary-repair-battery-v7.py:465`, `…v8.py:485`). Captured-by: none; the C1
  predicate reads `mismatches`, not the banner. Fix: print `len(cases)`, as v7/v8 do.
  Shown able to fail: the F8-deletion probe, not a committed receipt.

- **M99-i · a registry row whose tool's own source contradicts it (own, this round; the
  round-98 closure's D1 shape recurs one level down).** The 14 new `SKILL.md` registry rows
  added at landing A (`64cc3e10`, `SKILL.md:2065-2078`) are checked by the C1 counter's atom
  A4 only for *form* (kind word, exit map with `0=`/`1=`/`2=`, a cell carrying the file's
  full sha256, ≥ 5 cells). A4 never reads the tool's source, so a row that states a wrong
  fact about its own tool passes. Three rows are contradicted by their tool's source:
  1. `SKILL.md:2065` (`craft-citation-v2.py`) — the row and the tool's own docstring
     (`craft-citation-v2.py:22`, `_selftest` docstring `:223`) both say "14 fixture cases";
     the source builds **11** (`cases = [...]` at `:277` plus ten `cases.append` at
     `:296,302,320,323,328,331,333,335,338,339`) and the run prints `SELFTEST cases=11
     failures=0`. The row's "14" is the tool's stale prose, not its behaviour.
  2. `SKILL.md:2067` (`gen-forgery-fixtures.py`) — the row's write-scope cell says "writes
     only the fixture directory **it is given**"; the tool takes **no** directory argument
     (`main()` at `:40` has no `argv`; `OUTDIR` is a hardcoded constant
     `ROOT/.ufo/waves/round-97/forgery` at `:27`), so running it wrote 13 files into the
     clone's own `.ufo/waves/round-97/forgery/` with no argument at all.
  3. `SKILL.md:2074` (`self-assessment-audit.py`) — the row's write-scope cell says
     "read-only over `git show <rev>`"; the tool imports the round-66 recipe from the working
     tree (M99-f above), so the A1/A2 inputs are not `git show <rev>` reads.
  Captured-by: none of the round-99 criteria (A4 checks form, not truth). Fix: not landed;
  A4 would need to compare a row's stated selftest count / write scope against the tool's
  source, or the rows should be re-derived from the tools they describe. Shown able to fail:
  the three probes above, not a committed receipt.

- **M99-j · a fix that is committed but not reproducible from the lane (own, this round).**
  The C1 forgery control's receipt names `rev e2502c3dd1b850e24df103f4be83178615f73724`,
  which does **not** exist in the lane: `git cat-file -t e2502c3d…` → `fatal: git cat-file:
  could not get object info`. Only the diff
  `.ufo/waves/round-99/pre/c1-forgery-control.diff` is committed. Applying that diff to a
  fresh clone at base `de098f51` and committing reproduces the control exactly
  (`mismatches 15; head-score ok; head-fraction ok; map-rows 176 of 182; registry 0 of 9`,
  exit 1, and the same `map_rows_missing` and `registry_missing` sets as the committed
  receipt). Captured-by: none — the diff and the receipt agree; only the revision is
  unreachable. Fix: commit the fixture revision, or record in the receipt that the fixture
  lives in a scratch clone and name the diff as the reproducible artefact. Shown able to
  fail: the apply-and-rescore above.

- **M99-k · the round-98 closure's D2, partially closed (own, this round).** The round-98
  verifier routed defect D2 ("the v8 selftest tally is seat prose, not a committed raw
  output"). Round 99 committed `.ufo/waves/round-99/l1/selftest-v7.txt` and
  `selftest-v8.txt` (both `cases=23` / `cases=24`, `failures=0`), so v7/v8 are closed — but
  the round-99 counter's own raw output
  `.ufo/waves/round-99/pre/c1-selftest.txt` is two lines with a hardcoded count (M99-h), so
  the new counter repeats the shape D2 named. Captured-by: none. Fix: banner measures
  `len(cases)`; the raw output then names each case as v7/v8's do.

## 2. `## Named limits` — both claims

### R99-C2 (coverage: truncated UPX-packed PE, refusal)

From the entry's `## Limits` (`corpus/knowledge/2026-11-05-r99-pe-upx-truncation-refusal.md`):
1. Only truncation is decided. A pack whose bytes are corrupted but whose length is intact is
   not detected — the round-98 co-tamper of `dd[1].RVA` still passes both the repair and
   `upx -t` (SentinelInputs, round 98).
2. One packer version (5.2.0), `--best` only; PE only (Mach-O stays Frontier).
3. The decoy arm covers 9 of 10 carriers: on `lib7-Zip-JBinding.dll` the window start lies
   inside the section table, where writing a look-alike would corrupt the header.
4. The static leg is a text screen for spawning and dynamic import, not a sandbox.
5. The candidate was drafted and dry-run once before the freeze commit (disclosed in
   `plans/round-99-claims.md`); the landed score reads the committed bytes through `git show`.

From the counter's docstring (`tools/round-99/pe-upx-trunc-battery.py:1-56`) and the tool's
(`tools/round-99/upx-pe-repair.py:1-52`):
6. `--rev worktree` is accepted and copies the candidate from the working tree
   (`pe-upx-trunc-battery.py:195-196`); only a commit rev binds the candidate bytes.
7. Exit 2 is usage/preflight (pin mismatch, wrong upx, pack failure, unreadable rev) — a
   preflight failure is not a label, and the battery's own label vocabulary cannot distinguish
   "refused" from "not evaluated".
8. The refusal arithmetic uses the **last section header in table order**
   (`upx-pe-repair.py`, `end = ALIGN_UP(last.rawdataptr + last.SizeOfRawData, FileAlignment)`);
   the packer's own `isection[iobjs - 1]` is the same index, but a PE whose section table is
   reordered is out of scope.
9. `FileAlignment == 0` is refused as `filealign-zero` — the packer's own refusal, but the
   tool refuses a file the packer might still read on some path.
10. The static leg's forbidden-token list is a literal tuple
    (`pe-upx-trunc-battery.py:94-96`); a candidate that spawns the packer through a route
    the list does not name passes the leg. It is a text screen, as the entry says.
11. Carriers are absolute host paths outside the lane (`DL = /home/vgpnk/.local/share/…`,
    `OGL = /usr/lib/python3.14/…`, `/opt/ghidra/…`), sha256-pinned. On a host without them
    the battery exits 2 at preflight, so the claim is host-bound.
12. The overlay arm appends a runtime-random overlay (`os.urandom`, length 1–4096), so its
    cells are not byte-reproducible between runs; only the counts are.

### R99-C1 (calibration: self-assessment mismatches 17 → 0)

From the counter's docstring (`tools/round-99/self-assessment-audit.py:1-35`) and the probes:
13. A3 counts a stem as mapped when **any** table row carries it with ≥ 20 characters of other
    text. Measured: a stem-only row with 20 filler characters passes (mismatches 0), with 5
    characters it fails (mismatches 1). The rule is a length floor, not a content check —
    the round-98 forgery's "stem-only rows" fail only because their filler is short.
14. A4 checks the registry row's **form**, not its truth: kind word, exit map with `0=` and
    `1=`/`2=`, ≥ 5 cells, cell 4 ≥ 10 characters, and a cell carrying the file's full sha256
    at the revision. The seven `tools/round-9[0-6]/*.py` that still have no registry row
    (`tools/round-93/craft-citation-semantic.py`, `tools/round-93/stop-boundary-repair-battery-v3.py`,
    `tools/round-94/c1-landing-extra-checks.py`, `tools/round-94/c1-receipt-agreement.py`,
    `tools/round-94/stop-boundary-repair-battery-v4.py`, `tools/round-96/fresh-source2-check.py`,
    `tools/round-96/gen-forgery-fixtures.py`) are outside A4's `TOOL_DIRS`
    (`"tools/round-97", "tools/round-98", "tools/round-99"`), so "registry 14 of 14" does not
    mean the registry is complete.
15. The recipe that produces A1/A2 is not revision-bound (M99-f). A1/A2 therefore compare the
    head against whatever `tools/round-66/coverage-selfcheck.py` the running tree holds.
16. The `--selftest` count is not measured (M99-h).
17. The recipe-A fraction is a different population: at `Bk` the round-66 counter's own
    `recipe_a` still reads `mapped 142` of 183 files with 41 hidden entries and
    `coverage_score 7.76`, while the stem recipe reads 183/183 at 10.0
    (`.ufo/waves/round-99/l1/scores/coverage-selfcheck-at-c19d57cd….json`). The head is
    reconciled against the stem recipe only; recipe A remains unreconciled and is disclosed
    in the SCORECARD row.
18. The counter's own write scope is the lane's `.ufo/` tree (M99-g): a planted symlink at the
    receipt path redirects the write.

## 3. Registry-row check — statements the tool's own source contradicts

The 14 rows added at landing A are `SKILL.md:2065-2078` at `Bk`. Each row's sha256 matches the
tool's bytes at `Bk` (all 14 verified by `sha256sum`), so the pin column is sound; the
contradictions are in the descriptive columns.

| SKILL.md line | tool | row says | tool's own source says | verdict |
|---|---|---|---|---|
| 2065 | `tools/round-97/craft-citation-v2.py` | "`--selftest` (14 fixture cases, expected exit per case)" | the source builds 11 cases (`craft-citation-v2.py:277` + ten `cases.append` at `:296,302,320,323,328,331,333,335,338,339`) and prints `SELFTEST cases=11 failures=0` | **contradicted** (the row repeats the tool's own stale docstring at `:22`/`:223`) |
| 2066 | `tools/round-97/depth-blocks-v4.py` | "`--selftest` (padded-decoy and own-table fixtures)" | source has `--decoy-proof` as a **separate** mode with its own exit map (`:260`, `:272-278`), and the selftest prints `SELFTEST cases=8 failures=0` | consistent as written; the row omits that `--decoy-proof` returns 0/1 on a different predicate |
| 2067 | `tools/round-97/gen-forgery-fixtures.py` | "writes only the fixture directory **it is given**" | the tool takes no directory argument; `OUTDIR` is hardcoded (`gen-forgery-fixtures.py:27`), `main()` at `:40` has no `argv`; a run with no arguments wrote 13 files into the clone's `.ufo/waves/round-97/forgery/` | **contradicted** |
| 2068 | `tools/round-97/kill-rule-v3.py` | "`--selftest`; K-ownrun recursion unbounded and K-cwd cannot fail (M97-r, M97-s, open)" | consistent with the tool's docstring (`:37-41`); the tool has `--selftest` (`:618`) | consistent |
| 2069 | `tools/round-97/stop-boundary-repair-battery-v7.py` | "`--selftest` (23 cases, 0 failures at round 98, ExecReproC2)" | source prints `len(results)` (`:465`); the committed raw output `.ufo/waves/round-99/l1/selftest-v7.txt` reads `cases=23 failures=0` | consistent; the row still cites seat prose where a committed raw file now exists |
| 2070 | `tools/round-98/allowlist-check.py` | "no `--selftest`; the v7 control (`legs passed 1 of 4`) is its red case" | no `--selftest` flag in the source; `--json-out` required (`:55`); exit 2 on usage (`:65`), 0/1 otherwise (`:101`) | consistent |
| 2071 | `tools/round-98/pe-upx-tamper-battery.py` | "reads `--repair-cmd` from the working tree" | true: `--rev` defaults to `worktree` (`:122`) and the repair is read from the tree; exit 2 on pin/upx/pack preflight (`:137,144,148`) | consistent |
| 2072 | `tools/round-98/stop-boundary-repair-battery-v8.py` | "`--selftest` (24 cases, 0 failures; raw output `.ufo/waves/round-99/l1/selftest-v8.txt`)" | source prints `len(results)` (`:485`); the committed raw file reads `cases=24 failures=0` | consistent |
| 2073 | `tools/round-98/upx-pe-repair.py` | "0=repaired or intact; 2=typed refusal; **1=uncaught CLI error** (three crash paths, SentinelInputs r98)" | the row is right and the tool's own docstring is wrong: `main()` returns only 0 or 2 (`:137`,`:152`), but the docstring (`:34-36`) declares no exit 1. Measured on a real UPX-packed PE: missing `--in` **file** → rc 1 `FileNotFoundError`; missing `--out` directory → rc 1 `FileNotFoundError`; `--out` is a directory → rc 1 `IsADirectoryError`; a stale `<out>.tmp-<pid>` is ignored (rc 0). A missing `--in` **argument** is argparse → rc 2 | **the tool's source contradicts the row's exit 1** — the docstring declares two statuses and the code has three; the row is the accurate side. Route the docstring, not the row |
| 2074 | `tools/round-99/self-assessment-audit.py` | "read-only over `git show <rev>`" | `load_cs()` reads `HERE/../round-66/coverage-selfcheck.py` from the **working tree** (`:54-59`); mutating it flips the verdict at an unchanged `--rev` | **contradicted** (M99-f) |
| 2075 | `tools/round-99/pe-upx-trunc-battery.py` | "candidate read through `git show <rev>:<path>`" | true for a commit rev (`:198`), but `--rev worktree` is accepted and copies from the tree (`:195-196`); exit 2 on pin/upx/pack/unreadable-rev (`:228,234,262,269,273`) | consistent for the committed rev; the `worktree` mode is a named limit |
| 2076 | `tools/round-99/upx-pe-repair.py` | "0=repaired or intact; 2=typed refusal (truncated, filealign-zero, sections, PackHeader candidates, input-unreadable, output-is-directory, output-dir-missing, output-write-failed)" | the source also refuses `not-mz` and `not-pe` (`:73`,`:76`) — two refusal reasons the row omits; and argparse's own usage error (a missing `--out` argument) exits 2 with a usage message and no `refused:` line, so exit 2 does not uniquely mean "typed refusal" | **incomplete** — two typed refusals (`not-mz`, `not-pe`) are missing from the row's list, and the exit-2 namespace is shared with argparse |
| 2077 | `tools/round-99/gen-forgeries.py` | "0=fixtures written; 1=SystemExit naming a missing transform anchor" | source raises `SystemExit("anchor missing for %s: …")` from `must_replace` (`:30-33`), and `main()` returns 0 (`:102`) | consistent |
| 2078 | `tools/round-99/build-size-cache.py` | "0=cache written; 1=pack failure (CalledProcessError)" | source uses `subprocess.run(..., check=True)` (`:31`) — a `CalledProcessError` escapes as an uncaught traceback, so the exit is 1 with a traceback, not a typed refusal | consistent on the exit code; the failure is untyped (no `Refuse`-style message), unlike the r99 repair's envelope |

## 4. Reproductions this seat ran (all exit codes observed)

- C1 base control at `de098f51` in a fresh clone: `mismatches 17; head-score mismatch;
  head-fraction mismatch; map-rows 176 of 182; registry 0 of 9`, exit 1 — identical label and
  identical `map_rows_missing` / `registry_missing` sets to the committed
  `.ufo/waves/round-99/pre/c1-do-nothing-at-base.json`.
- C1 forgery control, rebuilt by applying the committed diff to base and committing: `mismatches
  15; head-score ok; head-fraction ok; map-rows 176 of 182; registry 0 of 9`, exit 1 — identical
  sets to the committed `.ufo/waves/round-99/pre/c1-forgery-control.json`.
- C1 at `Bk` in a fresh clone: `mismatches 0; head-score ok; head-fraction ok; map-rows 183 of
  183; registry 14 of 14`, exit 0 — matching the committed `c1-at-c19d57cd….json`.
- C2 at `Bk` in a fresh clone: `recovered 30 of 30; decoy 9 of 9; intact 10 of 10; overlay 20 of
  20; truncated 40 of 40; refused 2 of 2; cli 3 of 3; static 1 of 1; effective 79 of 79`, exit 0.
- C2 with the round-98 repair as the candidate at `Bk`: `truncated 0 of 40; cli 0 of 3`
  (otherwise full), exit 1 — matching the committed freeze control.
- `gen-forgeries.py --base tools/round-99/upx-pe-repair.py` regenerates the seven committed
  fixtures **byte-identically** (g2…g8 all `IDENTICAL`).
- `tools/round-99/upx-pe-repair.py` typed CLI envelope, measured: missing input file → rc 2
  `refused: input-unreadable: …`; missing output directory → rc 2 `refused: output-dir-missing`;
  output is a directory → rc 2 `refused: output-is-directory`; no traceback, nothing created.
- Both round-99 repair tools leave a planted symlink at their temporary path untouched
  (`VICTIM` still `ORIGINAL` after a successful repair), so the tool-side write is safe; the
  **counter-side** receipt write is not (M99-g).
