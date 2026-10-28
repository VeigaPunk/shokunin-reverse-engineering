# R44C2Counter — P44-C2 calibration counter (round 44, wave 1, pre-freeze)

Seat `R44C2Counter` (executor). Lane `kaidoku-shokunin`, base `c29360e3ba5381a5ab69e372d0d9577970f85018`.

## What I built

| item | value |
|---|---|
| artifact | `.ufo/waves/round-44/w1/artifacts/R44C2Counter/c2-counter.py` (1378 lines) |
| sha256 | `fda73a8e4092d43b0bc1d2a388c14ba314e6ed8f082adf02dfd9151410ce41c5` |
| installed path (L1) | `tools/round-44/c2-counter.py` |
| rubric it reads | `tools/round-44/c2-rubric.json` (frozen at the freeze commit) |
| dev-arm fixtures | `…/artifacts/R44C2Counter/dev-rubric.json`, `dev-rubric-landing-bound.json`, `dev-rubric-landing-unbound.json` |
| receipts | `…/artifacts/R44C2Counter/receipts/*.json` (7) + 5 score JSONs beside them |

I did **not** write anything under `tools/round-44/` (the L1 installs the counter), did not
touch a lane tracked file, and did not run `tools/round-44/c1-run.sh` (the after-side C1
data procedure). Only my seat's artifact/report paths and my scratch under
`/fast/scratch/hyaku/kaidoku-r44/probe-R44C2Counter/` were written.

```
python3 -I -B tools/round-44/c2-counter.py --root <LANE> --rev <REV> --freeze <FREEZE> \
    --work <SCRATCH> --json-out <OUT> [--rubric <FILE>] [--export auto|full|<glob,glob>] [--seat <NAME>]
python3 -I -B tools/round-44/c2-counter.py --root <LANE> --rev <BASE> --work <SCRATCH> \
    --json-out <OUT> --rubric <FILE> --pre-freeze          # base census (CTL-C2-0 gate)
python3 -I -B tools/round-44/c2-counter.py --selftest
python3 -I -B tools/round-44/c2-counter.py --schema          # the rubric contract, printed
```

## The rubric contract the counter implements

Top level (object): `predicate`, optional `freeze` (the rubric may name the commit it is
bound to; a mismatch is exit 2), `frozen_paths` (list of strings or of
`{"path": …, "expected_edit": {…}}`), `expected_edits` (map form), `frozen_dirs`
(directory pathspecs — every file under them that existed at FREEZE is frozen),
`export_paths` (globs), `entries` (list; also accepted: `checks`, `items`, `statements`).

Entry (object) — `check`, `command` and `asserted` are **required** (a missing `check` or
`command` is a malformed rubric → exit 2):

```json
{
  "id": "<stable id>",
  "check": "json | text | exit | <descriptive label>",
  "command": ["python3", "-I", "-B", "tools/round-44/c2-checks.py", "<kind>"],
  "asserted": <the expected observation>,
  "compare": "eq | set_eq | numeric_eq | subset | ge | le",
  "observed_key": "observed",
  "file": "SCORECARD.md",
  "files": ["corpus/knowledge"],
  "timeout": 600,
  "repair_command": ["python3", "-I", "-B", "…"],
  "expected_edit": {"append": ["<line>"], "append_text": "<bytes>",
                    "preserve": ["<sha256 of a cited line>"], "marker": "<text>"}
}
```

**Check-command contract.** The command runs with the exported tree of REV as its working
directory and prints the observation on stdout. `check: "json"` parses stdout as JSON and
reads `observed_key` (default `observed`, then `value`, `result`, `match`, `ok`); `check:
"text"` takes stdout verbatim; `check: "exit"` maps the exit status to a boolean; a
descriptive label behaves like `json` with a text fallback. A command that cannot start,
times out, or exits non-zero with empty stdout **cannot be evaluated** → the whole score is
exit 2, never a pass. The counter exports the tree into a scratch clone (`git clone --shared
--no-checkout` + `git archive`, read-only); the env carries `HYAKU_TREE`, `HYAKU_REPO`,
`HYAKU_ROOT`, `HYAKU_REV`, `HYAKU_FREEZE`, `HYAKU_RUBRIC`, `HYAKU_WORK`, `HYAKU_SEAT`, and
`{rev} {freeze} {root} {tree} {repo} {work} {rubric} {seat}` are substituted in argv.

## Predicate behaviour (P44-C2)

1. **Freeze integrity.** FREEZE must be an ancestor of REV. Every frozen path — the rubric
   file itself, the counter file, the rubric's `frozen_paths`, the `frozen_dirs` pathspecs,
   and `SCORECARD.md`/`SHONEN.md`/`corpus/README.md`/`SKILL.md` (the R44-C2 frozen surface
   the claim names) — is walked in `FREEZE..REV` with merge diffs
   (`--diff-merges=first-parent`), a name-only union walk as a cross-check, and per-path
   status (`M/D/R/T/U` are changes; `A` is a change whenever the path existed at FREEZE).
   A frozen path whose blob differs from FREEZE, or that was touched and restored, is
   `frozen_path_changed` → **exit 2**, never a pass. `corpus/SOURCES.md` is deliberately not
   frozen: C1 appends its S138/S139 rows there and the claim pins no SOURCES row count.
2. **Repairs.** A repair is admissible only when the rubric binds it: the blob at REV must
   be the blob at FREEZE **plus** the bound block — byte-for-byte (`append_text`), or
   line-identity over the appended lines (`append`, blank separator lines ignored), plus
   cited-line digests that must still occur (`preserve`) and/or a marker line. The freeze
   blob must be a prefix of the REV blob, so nothing may be edited in place and nothing may
   be deleted. A suffix-containment check is **not** used: an in-place fabrication inside the
   frozen file is rejected (measured, see receipts).
3. **Evaluation.** Each entry's check argv runs in the scratch export of REV; the
   observation is compared with the asserted value under the entry's `compare` mode.
4. **A note is never evidence.** When a check fails, an appended correction note does **not**
   repair the entry. The entry may declare `repair_command`: a second argv that re-derives
   the value from REV state; only when that re-derived value equals the asserted value is
   the entry repaired (`repaired_by_rederived_value`). Without it, the note leaves the entry
   a mismatch.
5. **Exit codes.** `0` iff `mismatches == 0`, no entry is unevaluable and at least one entry
   was evaluated (`entries_evaluated > 0`); `1` on a mismatch; `2` for a malformed rubric, an
   absent frozen file, a frozen path that changed, an empty rubric, a check that cannot run,
   or a freeze that is not an ancestor. **Exit 2 means could-not-evaluate, never "not a
   pass"; it never counts toward the target.** The receipt always carries `mismatches`,
   `mismatches_count`, `entries_evaluated`, `unevaluable`, `frozen_path_changed`,
   `pre_freeze`, `claim_score`, `counter_sha256` and `counter_sha256_at_freeze`.
6. **`--pre-freeze`** runs the base census (CTL-C2-0's honest-stop gate): the freeze walk
   is reported but not enforced, because at the base the freeze is not yet an ancestor of
   REV. The receipt carries `pre_freeze: true` and `claim_score: false`, so a census can
   never be mistaken for a claim score.

## Evidence (receipts: seat, command, exit code, stdout sha256, wall time)

| receipt | exit | stdout sha256 | wall s | what it shows |
|---|---|---|---|---|
| `receipts/selftest.json` | 0 | `d02c9efef6ea90fbcf56e533abde9619785456c204385dbfe1a934cf09a4d386` | 0.42 | the 16-arm self-test matrix is green |
| `receipts/dev-arm-lane.json` | 1 | `cc579adaceac4212553d69ae38b702b2e6be5a82ca5874a1b948fca3bec64a47` | 0.38 | the counter runs on the real lane at the base and reports mismatches |
| `receipts/pre-freeze-census.json` | 1 | `d48e6941d26e97dde9292670e0cbcc335dd76769edc0165a72098d44014abb8a` | 0.38 | the base census runs pre-freeze and reports `entries_evaluated` + `mismatches` |
| `receipts/no-rubric-at-base.json` | 2 | `003bd8577716559be8d91fbb097063f70fb4ba05ed7c430e58ac59ce3372c5b3` | 0.04 | no frozen rubric at FREEZE → `rubric_absent_at_freeze`, exit 2 (never a pass) |
| `receipts/landing-bound.json` | 0 | `ac643f72f913c348f0177dcbb3e3987a28640414966622b68ee3976525d9b294` | 0.33 | a bound appended repair to `SCORECARD.md` is admissible |
| `receipts/landing-unbound.json` | 2 | `3c06e33488574d8783eacec0ece89c4a9e3a626a0299547754b772996944cbf2` | 0.06 | the same append **without** a bound `expected_edit` → `frozen_path_changed` |
| `receipts/in-place-fabrication.json` | 2 | `0f9bf90382ba32d207fa03d5c401993e87cac65dfe9514e2e0185da310add19f` | 0.06 | an in-place fabrication ("R43-C2 met" rewritten into the frozen blob) is rejected |

## Self-test matrix (`--selftest`, all green)

| arm | expected | got |
|---|---|---|
| clean rubric at the base | 0 | 0 |
| seeded mismatch on the reality side | 1 | 1 |
| seeded mismatch on the claim side | 1 | 1 |
| rubric entry with no command | 2 | 2 |
| the committed rubric edited after the freeze | 2 | 2 |
| appended repair bound by `expected_edit` | 0 | 0 |
| the same append without a bound `expected_edit` | 2 | 2 |
| a note alone never repairs | 1 | 1 |
| a note plus an independent re-derivation | 0 | 0 |
| empty rubric (`entries_evaluated == 0`) | 2 | 2 |
| a file changed under a frozen directory pathspec | 2 | 2 |
| a file **added** under a frozen directory pathspec | 2 | 2 |
| a weak `expected_edit` (marker only) | 2 | 2 |
| pre-freeze census at the base | 1 (mismatch reported) | 1 |
| pre-freeze census of a rubric that declares the freeze | 1 (census runs) | 1 |

## Lane dev-arm findings (probe grade — the frozen rubric is another seat's job)

The dev rubric I used to exercise the counter on the real lane at the base
(`dev-rubric.json`, four checks over `SCORECARD.md`, `SHONEN.md`, `corpus/README.md`) is
**not** the frozen rubric and its checks are crude. It reports 2 of 4 mismatches:

* `dev-scorecard-map-count` — `SCORECARD.md`'s coverage headline claims **133** knowledge
  files mapped; `corpus/knowledge/*.md` holds **137** at the base. A real candidate for the
  frozen rubric (category b), and a candidate C2 repair.
* `dev-readme-map-coverage` — my probe's regex also matches lesson/evidence stems quoted in
  `corpus/README.md` (`2026-10-13-round-1`, …), so its "dangling" list is a **probe
  artefact**, not necessarily a lane defect. The rubric author must scope the stem pattern.
* `dev-shonen-path-line` — all 8 `path:line` assertions in `SHONEN.md` resolve at the base
  (match).
* `dev-scorecard-evidence-pointer` — all 36 `corpus/knowledge/…` pointers in `SCORECARD.md`
  resolve (match).

**The honest-stop gate is not yet run**: this is a four-check dev probe, not the enumerated
frozen rubric, so it cannot decide whether R44-C2 stops (zero mismatches at base). The
census mechanism that would decide it is in place and measured (`--pre-freeze`).

## Sentinel blockers addressed (`R44C2Sentinel`, wave-1 review, two rounds)

1. *"A note must never be evidence."* The `supersession` escape hatch is **removed** from the
   counter. A failed check is repaired only by an independent re-derivation
   (`repair_command`), never by the presence of a note. Measured: `note_alone_does_not_repair`
   → 1, `note_with_rederived_value` → 0.
2. *"`expected edit bytes` cannot exist pre-freeze; a suffix-containment check accepts an
   in-place fabrication."* The binding is containment-free: the REV blob must be the FREEZE
   blob **plus** the bound block (`append_text` byte-for-byte; `append` line identity;
   `preserve` cited-line digests), and the freeze blob must be a prefix (nothing edited in
   place, nothing deleted). Measured on the real `SCORECARD.md` blob: an in-place
   "R43-C2 met" fabrication → exit 2 `bound_edit_violation`. `tools/round-44` is also
   freezable as a directory pathspec (`frozen_dirs`), and the counter ships with
   `tools/round-44/c2-counter.py` and `tools/round-44/c2-rubric.json` in its frozen set.
3. *"The counting command has no pre-freeze mode."* `--pre-freeze` added: the base census
   runs (freeze walk reported, not enforced), and the receipt carries `pre_freeze`,
   `claim_score: false`, `entries_evaluated` and `mismatches` — so CTL-C2-0's honest-stop
   gate can actually run instead of dying on `freeze_not_ancestor`.
4. *"Exit 2 must never be reachable as 'not a pass'; an empty rubric must be exit 2."*
   `entries_evaluated == 0` → exit 2 (`no_evaluable_entries`); every other exit-2 reason is
   a genuine could-not-evaluate (malformed rubric, absent frozen file, frozen path changed,
   check that cannot run). Exit 1 is reserved for a measured mismatch.

The Sentinel's second pass found four residual holes; all are closed and covered by new
self-test arms:

5. *A file **added** under a frozen directory pathspec was only noted.* An addition under a
   frozen pathspec is now a change (`frozen_path_changed`), because the claim freezes
   `tools/round-44/*`. The same rule applies to the rubric and the counter themselves: a
   post-freeze addition of `tools/round-44/c2-rubric.json` or `tools/round-44/c2-counter.py`
   is `added_after_freeze` → exit 2. (Arms `frozen_dir_added`.)
6. *`expected_edit` with only a `marker`, or an empty `append`, admitted arbitrary appended
   content.* A binding must now carry `append_text` (byte-for-byte) or a non-empty `append`
   (line identity); `marker` and `preserve` are additional only. A rubric with a
   contentless binding is **malformed** → exit 2 at freeze time, not a silent hole. (Arm
   `weak_expected_edit`.)
7. *`--pre-freeze` refused a rubric that declares the canonical freeze.* The declared
   freeze is now **recorded** (`declared_freeze`) and not enforced in the census, so
   CTL-C2-0 can score the frozen rubric at the base. (Arm
   `pre_freeze_with_declared_freeze`.)
8. *`--rubric` still yielded `claim_score: true`.* A claim score now requires
   `rubric_source == 'freeze'`; every `--rubric` run is a census/dev arm and reports
   `claim_score: false`.

## Limits and risks (honest)

* The rubric's **enumeration** is another seat's (`R44C2Rubric`); this counter only
  re-derives what the rubric names. A check outside the frozen set is not counter ground.
* **Export coverage.** `auto` exports the rubric-named paths, the path-like literals inside
  the check commands, the rubric's `export_paths` globs and the C2 default surface
  (`SCORECARD.md`, `SHONEN.md`, `PROVINCE.md`, `SKILL.md`, `LOG.md`, `corpus/README.md`,
  `corpus/SOURCES.md`, `corpus/knowledge/*`, `corpus/lessons/*`, `corpus/evidence/*.json`).
  A check that discovers paths at runtime and reads something outside that set sees a
  missing file → the check fails → exit 2 (honest, never a false pass). `--export full`
  exports the whole tree (34 183 files, ~511 MB) when needed.
* A check that crashes is *not* a mismatch: non-zero exit with empty stdout is
  could-not-evaluate → exit 2. A crashing check must be fixed, not counted as a defect.
* `expected_edit` binds the *repair*, not the *result*: the L1 must write the rubric's
  bound append lines before the freeze, or the landing will be inadmissible (exit 2). The
  bound lines are the appended block's non-blank lines, in order.
* If the L1 installs `tools/round-44/c2-counter.py` **after** the freeze commit, the
  counter's own blob is absent at FREEZE; the receipt then shows
  `counter_sha256_at_freeze: null` and the counter is not itself frozen. Installing the
  counter (and the rubric) **in** the freeze commit is the admissible order.
* The counter reads committed bytes only: it cannot verify that a repaired *statement* is
  true, only that the check re-derives it. Every rubric check must re-derive the value
  independently (recount, re-resolve), never re-read the number it is checking.
* `python3` here is 3.14 on this host; the counter uses only the standard library and runs
  under `-I -B`.

## For the L1

> **Install the current on-disk artifact, not the wave-1 snapshot.** An earlier version of
> the counter was picked up by commit `9a8de923` ("round-44 wave-1 receipts … seat outputs
> so far"); the file changed after that (the Sentinel's eight contract fixes). The version to
> install is the working-tree one, sha256
> `fda73a8e4092d43b0bc1d2a388c14ba314e6ed8f082adf02dfd9151410ce41c5`, 1378 lines. Verify
> the digest before freezing.
>
> The counter and the rubric must land **in the freeze commit**: a post-freeze addition of
> `tools/round-44/c2-counter.py` or `tools/round-44/c2-rubric.json` is now
> `added_after_freeze` → exit 2, and `frozen_dirs: ["tools/round-44"]` makes any file added
> under that directory after the freeze a `frozen_path_changed` too.

1. Install `…/artifacts/R44C2Counter/c2-counter.py` → `tools/round-44/c2-counter.py` **in the
   freeze commit** (so the counter and the rubric are frozen).
2. Freeze the rubric at `tools/round-44/c2-rubric.json`; the rubric must declare
   `frozen_paths` (SCORECARD.md, SHONEN.md, corpus/README.md, and every file it repairs),
   `frozen_dirs: ["tools/round-44"]`, and an `expected_edit` for every file the landing
   appends to.
3. Run the base census before the freeze: `--pre-freeze --rev <BASE> --rubric <rubric>`.
   **If it reports `mismatches == 0`, R44-C2 stops (honest stop)** — report that instead of
   loosening the rubric.
4. After the freeze and the landing, the claim score is
   `--rev <REV> --freeze <FREEZE>`; exit 0 requires `mismatches == 0`,
   `entries_evaluated > 0` and `frozen_path_changed []`.
