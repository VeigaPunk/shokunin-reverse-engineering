# ScribeLesson — round 99 wave 1 (L1 KaidokuR99, attempt 1)

Seat: scribe. Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Scratch: `/fast/scratch/hyaku/kaidoku-r99/ScribeLesson` (trap-deleted on exit).
Draft deliverable (never `corpus/`): `.ufo/waves/round-99/w1/ScribeLesson/lesson-draft-material.md`.
Receipts copied into `.ufo/waves/round-99/w1/ScribeLesson/`.

## Behaviour

Drafted the three requested items for `corpus/lessons/round-99.md` (Mistakes candidates with the
fix's ability-to-fail named; Named limits for both claims; the 14 new `SKILL.md` registry rows
checked against their tools' own source). Every claim in the draft was executed by this seat;
no number is quoted without a run behind it.

## Reproductions (clone at the named rev, `git rev-parse --show-toplevel` asserted)

| check | command | observed |
|---|---|---|
| C1 base control | `python3 -I -B tools/round-99/self-assessment-audit.py --root $S/base --rev de098f51cd73d3b9b4a895840da8f2bb0a386db8 --json-out $W/c1-base-repro.json` | `mismatches 17; head-score mismatch; head-fraction mismatch; map-rows 176 of 182; registry 0 of 9`, exit 1 — label and both missing-sets identical to the committed `pre/c1-do-nothing-at-base.json` |
| C1 forgery control, rebuilt | `git apply .ufo/waves/round-99/pre/c1-forgery-control.diff` at base + commit, then the same command | `mismatches 15; head-score ok; head-fraction ok; map-rows 176 of 182; registry 0 of 9`, exit 1 — identical sets to the committed `pre/c1-forgery-control.json` |
| C1 at Bk | same command, `--rev c19d57cd2e65a036478b9e78f6c5397dedfb2bcb` | `mismatches 0; head-score ok; head-fraction ok; map-rows 183 of 183; registry 14 of 14`, exit 0 — matches committed `c1-at-c19d57cd….json` |
| C2 at Bk | `python3 -I -B tools/round-99/pe-upx-trunc-battery.py --root $S/clone --repair tools/round-99/upx-pe-repair.py --rev c19d57cd2… --work $W/work --json-out $W/rec.json` | `recovered 30 of 30; decoy 9 of 9; intact 10 of 10; overlay 20 of 20; truncated 40 of 40; refused 2 of 2; cli 3 of 3; static 1 of 1; effective 79 of 79`, exit 0 |
| C2 with the round-98 repair | same, `--repair tools/round-98/upx-pe-repair.py` | `truncated 0 of 40; cli 0 of 3` (otherwise full), exit 1 — matches the committed freeze control |
| forgeries regenerate | `python3 -I -B tools/round-99/gen-forgeries.py --base tools/round-99/upx-pe-repair.py --out-dir $W/forge` | all seven g2…g8 byte-identical to `tools/round-99/forgeries/` |

## Gates (the two frozen predicates, reproduced)

- R99-C1: `mismatches 0` and exit 0 at `c19d57cd2` — met. Base control `mismatches 17`, exit 1;
  forgery control `mismatches 15`, exit 1 (both re-derived from the committed bytes, not quoted).
- R99-C2: the full label and exit 0 at `01c4b79cc` and at `c19d57cd2` — met. All nine controls at
  the freeze (`pre/c2-*.json`) exit 1.
- Byte identity checked: counter `e732465b…` and battery `d4ed4430…` are the same at the freeze
  `8fb5ac4f` and at `Bk`; all 14 registry-row sha256 pins equal the tool bytes at `Bk`.

## Touched surfaces

Only `.ufo/waves/round-99/w1/ScribeLesson.md` (this file) and `.ufo/waves/round-99/w1/ScribeLesson/`
(the draft + six copied receipts). `corpus/` untouched; no git mutation in the lane or fleet repo;
no commit, no push.

## Findings (6)

1. **M99-f — the C1 counter's head atoms are not revision-bound.** `self-assessment-audit.py:54-59`
   imports `tools/round-66/coverage-selfcheck.py` from the **working tree**; the receipt pins 14
   tools, not that one. Mutating the working-tree recipe flipped the label at an unchanged `--rev`
   `c19d57cd2` from `mismatches 0` to `mismatches 2; head-score mismatch; head-fraction mismatch`
   (exit 1), and back on restore. The `SKILL.md:2074` write-scope cell "read-only over `git show
   <rev>`" is therefore contradicted by the tool's own source.
2. **M99-g — both round-99 counters write their receipt through a predictable name.**
   `self-assessment-audit.py:226` and `pe-upx-trunc-battery.py:361` open `<out>.partial` with a
   plain `open()`. A symlink planted there is followed: the victim file was overwritten with the
   receipt and `<out>` became a symlink to it (measured for both counters). v7/v8 use
   `tempfile.mkstemp` + dir fsync (`stop-boundary-repair-battery-v7.py:95`); the r99 counters
   regress from QUALITY Rows 189/192.
3. **M99-h — the C1 selftest banner is a hardcoded literal.** `self-assessment-audit.py:198` prints
   `"SELFTEST cases=9"`; deleting the `F8-unregistered-tool` case still printed `cases=9 failures=0`
   (exit 0). The committed `pre/c1-selftest.txt` cannot distinguish 9 cases from 8.
4. **M99-i — three registry rows are contradicted by their tool's own source** (A4 checks form, not
   truth): `SKILL.md:2065` claims 14 selftest cases where the tool builds 11 and prints
   `cases=11`; `SKILL.md:2067` says the generator writes "the fixture directory it is given" while
   the tool takes no directory argument and wrote 13 files into the clone's own
   `.ufo/waves/round-97/forgery/`; `SKILL.md:2074` (finding 1). Two further rows are incomplete:
   `SKILL.md:2076` omits the `not-mz` and `not-pe` refusals, and `SKILL.md:2073` documents an
   exit 1 that the r98 tool's own docstring denies (measured: three rc-1 traceback paths on a real
   pack — missing `--in` file, missing `--out` dir, `--out` is a dir).
5. **M99-j — the C1 forgery control's revision is unreachable from the lane.**
   `git cat-file -t e2502c3dd1b850e24df103f4be83178615f73724` → `fatal: git cat-file: could not get
   object info`; only `pre/c1-forgery-control.diff` is committed. Applying that diff to a fresh
   base clone reproduces the control exactly, so the evidence is sound but the revision is not.
6. **M99-k — the round-98 closure's D2 is only half-closed.** v7/v8 raw selftest outputs are now
   committed (23 / 24 cases, `failures=0`), but the round-99 counter's own raw output is the
   two-line hardcoded banner of finding 3 — the shape D2 named, one level down.

## Named limits drafted

- **C2** (12 items): truncation only; one packer version, `--best` only, PE only; decoy arm covers
  9 of 10 carriers (the 517-offset DLL's window lies in the section table); the static leg is a
  text screen; the pre-freeze dry run is disclosed; `--rev worktree` copies the candidate from the
  tree; exit 2 covers usage/preflight, so "refused" and "not evaluated" share a code; the
  arithmetic uses the last section header in table order; `filealign-zero` is refused; the
  forbidden-token list is a literal tuple; carriers are absolute host paths outside the lane;
  the overlay arm's bytes are runtime-random, only its counts reproduce.
- **C1** (6 items): A3 is a ≥ 20-character length floor, not a content check (a stem-only row with
  20 filler characters passes; with 5 it fails); A4 checks row form, not row truth, and its
  `TOOL_DIRS` exclude `tools/round-9[0-6]/` — seven such tools still have no registry row; the A1/A2
  recipe is not revision-bound; the selftest count is not measured; recipe A remains unreconciled
  (142 of 183 mapped, `coverage_score 7.76`, 41 hidden) while the head is reconciled against the
  stem recipe only; the counter's receipt write is redirectable.

## Out of scope (not attempted, stated so the record is complete)

- The C1 forgery-control diff's fixture content was not re-derived from the *unreachable* revision
  (impossible); it was re-derived from the committed diff, which is the reproducible artefact.
- `corpus/lessons/round-99.md` already exists in the lane working tree as an **untracked** file
  (mtime 19:00, written by another seat) — read for context only, not edited. This seat's draft is
  a separate file, so the two do not collide.
- The four C2 carriers whose host paths are outside the lane (`/opt/ghidra/…`,
  `/home/vgpnk/.local/share/…`, `/usr/lib/python3.14/…`) were not relocated or pinned by this seat;
  the battery's own sha256 pin check covers them.
- No claim was re-frozen, re-pinned or re-scored; every control was reproduced from committed bytes.

## Artifacts

- Report: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-99/w1/ScribeLesson.md`
- Draft: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-99/w1/ScribeLesson/lesson-draft-material.md`
- Receipts: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-99/w1/ScribeLesson/{c1-at-c19d57cd…,c2-at-c19d57cd…,c1-do-nothing-at-base,c1-forgery-control,c2-r98-upx-pe-repair-at-freeze}.json`, `c2-controls-at-freeze.txt`
- Tooling: none installed or upgraded this seat (no pacman, no `uv tool`, no network fetch).
