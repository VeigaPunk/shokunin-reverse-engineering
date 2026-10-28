# R46W1ScribeLesson — round 46 wave 1 seat report

Role: lesson scribe (leaf, no subagent dispatch). Lane tree was read-only for this seat; the
only lane writes are under `.ufo/waves/round-46/w1/R46W1ScribeLesson/`. Scratch root
`/fast/scratch/hyaku/kaidoku-r46/R46W1ScribeLesson` (`TMPDIR` and `HYAKU_SCRATCH` both set to
it) was removed after the receipts were copied here. Nothing installed (no `uv`/`npx`/binary
needed; `python3` 3.14.8 and `git` 2.56.0 were present). No commit, stage, stash or any
mutating git/jj command was run; no fixture repo was created outside `$S`, and every fixture
was `git -C <d> init` in `$S` with `git -C <d> rev-parse --show-toplevel == <d>` asserted.

## What was produced

1. `lesson.md` in this directory — the `## Mistakes` rows (M46-1, M46-2, M46-3) and the
   `## Gate` draft (S142 source row, admit, `Assimilation: none` with reason, census
   before → after), plus a reconciliation section against the already-landed
   `corpus/lessons/round-46.md`.
2. Sixteen computed receipts (`R1`–`R14` JSON, `P1`/`P2` JSON) plus `receipts.tsv`
   (command / exit / stdout sha256 / UTC per run), `probe.out`, `census.out`,
   `census-validate.out`, `F5-outpath-refusal.out`, and the two drivers (`driver.sh`,
   `probe.py`).

## Behaviour measured (all with exact command, exit, stdout sha256, UTC in `receipts.tsv`)

| # | measurement | exit | stdout sha256 | UTC | value |
|---|---|---|---|---|---|
| R1 | `attest.py --freeze 3182047 --rev 781e19ae` (the **dispatch-named** freeze) | 2 | `7ecb8b15…` | 17:00:54Z | `frozen_path_changed ["tools/round-46/", "tools/round-46/attest.py", "…/gate.py", "…/registry.py"]`; `blob_changed ["tools/round-46/"]`; `restored` = the three touched **files** |
| R2 | `attest.py --freeze 65678df0 --rev 7bf33e31` (frozen bytes, full battery) | 0 | `4bc8f97a…` | 17:00:54Z | `met_target true`; battery `forgeries_total 9, v1_green 9, v2_green 0, genuine_green 1, v2_crash 0` |
| R3 | `attest.py --profile v1 --freeze 65678df0 --rev 65678df0` (the control the plan names "at the freeze") | 1 | `1e9726ac…` | 17:00:54Z | `failing ["battery genuine_green 0 != 1"]`; `forgeries_total 9`, `v1_green 9` → **the numbers exist, the exit 0 does not** |
| R4 | `attest.py --profile v1 --freeze 65678df0 --rev 7bf33e31 --no-battery` | 0 | `d2c23005…` | 17:00:54Z | the v1 clause set is green on the landed genuine artefact post-landing |
| R5 | `registry.py` (worktree bytes, post-F4) `--freeze 65678df0 --rev 781e19ae` | 0 | `116cebac…` | 17:00:54Z | `met_target true`; battery `7/7/0/1`; `unregistered []`, `thin []`, `absent_at_rev []`, `scope_size 38` |
| R6/R7 | `registry.py --profile v1` / default `--freeze 65678df0 --rev 65678df0` | 1 / 1 | `03160306…` / `e00d2cf1…` | 17:00:54Z | at the freeze: markers 0, `header != house schema`, `unregistered 38 of 38` |
| R8 | `registry.py --profile v1 --freeze 65678df0 --rev 781e19ae --no-battery` | 0 | `1dcfeda1…` | 17:00:54Z | v1 structural green on the landed section |
| R9 | `attest.py --freeze 65678df0 --rev 65678df0` | 1 | `54d004b4…` | 17:00:54Z | at the measured freeze block 23 is present (`rows 13`) and red only on `interpreter sha256 pin does not match the bytes at rev` |
| R10/R11 | `registry.py --root <abs>` (lane cwd) and `--root .` (lane cwd) | 0 / 0 | `116cebac…` both | 17:02:59Z / 17:03:00Z | invocation form (cwd, relative root) does not change the verdict: stdout byte-identical to R5 |
| R12 | **frozen** `registry.py` (`db5adc02…`, copied from `git show 65678df0:`) `--freeze 65678df0 --rev 781e19ae` | 1 | `ba30eeef…` | 17:03:42Z | `failing ["battery v1_green 0 != 7"]`; all seven fixtures `v1_exit 1` |
| R13 | frozen `attest.py --profile v1 --freeze 3182047 --rev 3182047` | 1 | `ca2aad31…` | 17:05:08Z | `block_present 0`, `marker_occurrences 0`, `rule_blocks 22 < 23`, battery `skipped` |
| R14 | frozen `attest.py --freeze 65678df0 --rev 0425224` (F4) | 2 | `1f75bcb0…` | 17:05:08Z | `frozen_path_changed ["tools/round-46/", "tools/round-46/registry.py"]`; `restored ["tools/round-46/registry.py"]` although it is modified |
| P1 | frozen `attest.py` (with battery) on a fixture whose block 23 gains one row: `| scratch note, no routed id | nothing routed | pin | 0 |` | 0 | `probe.out` sha `e52a4d11…` | 17:04:48Z | `met_target true`, `rows 14`, battery `9/9/0/1/0` |
| P2 | frozen `attest.py --no-battery` on a fixture whose Refs paragraph is one citation repeated six times | 0 | `probe.out` sha `e52a4d11…` | 17:04:48Z | `met_target true`, `refs 7` from **one** distinct citation |
| census | `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` | 0 | `065a45eb…` | 17:06:18Z | `kaidoku ok`; **15** `W04`; one of them is `S142 duplicate url git-scm.com/docs/git-log across scopes` |
| R-F5 | frozen `attest.py … --json-out <scratch>/refused.json` | 2 | `1e273744…` | 17:07:46Z | `{"reason": "--json-out outside the lane root: …"}` — receipts are scoped to the measured root |
| fetch | `curl https://git-scm.com/docs/git-log` | 200 | `0a73e33b…` (375,834 bytes) | 17:05:32Z | byte-identical to the digest recorded in the S142 row; quote "Show full diff with respect to first parent. This is the same format as --patch produces for non-merge commits." present (19 words) |

## Findings

**F1 (HIGH; M46-2 class) — the frozen C2 instrument contradicts the plan's own clause 6.**
R46-C2 clause 6 requires `battery.v1_green == 7`; the frozen `tools/round-46/registry.py`
(`db5adc02…` at the measured freeze) computes **0** — R12, exit 1, `failing ["battery v1_green
0 != 7"]`, every one of the seven fixtures `v1_exit 1`. Cause, by code read: at `db5adc02` the
v1 branch switches only the marker/fence parse; `strict_cell`, `strict_exit` and `presence`
are gated on the *spec*, not the profile, so the ported v1 clause set still applies the v2
checks. This is the L1's own `l1/scores/c2-at-781e19ae.json` (mtime 16:59:26Z) reproduced, so
the verdict is the instrument's, not a seat's. Consequence: the claim was unsatisfiable at the
frozen bytes, and the only way to reach it was to edit the frozen path (F4 `0425224`), which
under the plan's own freeze rule makes every later score exit 2 — R14. F4's bytes do make the
numbers (R5/R10/R11, `v1_green 7`, exit 0), so the fix works and is shown able to fail against
the bytes it replaced (R12). Not fixed by this seat; reported with the differing values.

**F2 (MEDIUM; M46-3 class) — three frozen sentences are not computed by their clause set.**
(a) "every row's trigger names a routed `R45-CL<n>` id" is not enforced: P1 appends a row with
no routed id and the frozen counter still returns `met_target true` with the full 9-forgery
battery green (exit 0). The code checks only the union of cell 0 over all rows
(`{m.group(0) for r in rows …}`), never per row. (b) "at least six citations" is counted per
occurrence: P2 makes one citation six times and `refs 7` satisfies clause 5. (c) The
Freeze-integrity rule's "`restored` names a path the history arm saw and the blob arm finds
clean" is false for file-level names: the blob arm reports the frozen *directory*
(`blob_changed ["tools/round-46/"]`) while the history arm reports files, so every touched
file is listed as `restored` although modified (R1: three files; R14: `registry.py`). (d) LOW:
R46-C2 clause 4 says the cell "enumerates `0=`, `1=`, `2=`" while `EXITMAP` also accepts `0:`
(code read, no receipt).

**F3 (MEDIUM; M46-1 class) — the plan names four control receipts, two of which cannot or do
not exist.** At the declared freeze the C1 v1-profile subject does not exist (R13:
`block_present 0`, battery `skipped`); at the measured freeze the battery runs but the receipt
is red because the battery's genuine arm is always scored with `--profile v2` (R3:
`genuine_green 0 != 1`). The files: `.ufo/waves/round-46/controls/` holds
`ctl-c1-0-do-nothing.json`, `ctl-c1-fidelity.json`, `ctl-c2-0-do-nothing.json`,
`ctl-c2-1-v1-scope.json`, `ctl-c2-fidelity.json`. `ctl-c1-1-v1-profile.json` is absent;
`ctl-c2-1-v1-profile.json` is absent while `ctl-c2-1-v1-scope.json` is `counter:
round-45-c2`, `scope_size 6` (the round-45 counter, not a v1-profile run of the seven C2
forgery classes); `ctl-c2-2-ghost-tool.json` is absent. The satisfiability preflight checked
computability, never the revision at which a value exists, and never that the named files be
produced.

**F4 (MEDIUM; record) — the freeze identity is three-valued and the re-derivation rule gives
the wrong one.** `git log --format=%H -1 -- plans/round-46-claims.md` → `3182047` (the claims
file never changed); `git log --format=%H -1 -- tools/round-46/` → `0425224` (F4); the
controls were taken at `50862e4a`, the scores at `65678df0` (then `0425224`). Scoring at the
dispatch's freeze is exit 2 (R1) and scoring F4 under the previous freeze is exit 2 (R14), so
each score exists only at the freeze that post-dates the last fix — which is why the round
needed four freeze commits. The plan's own sentence ("the commit that first contains this file
and `tools/round-46/`") is true of `3182047` and of no score.

**F5 (LOW; tool/contract friction) — `--json-out` is scoped to `--root`, not to the caller's
scratch.** `gate.out_path` refuses any path outside `os.path.realpath(root)`. The seat contract
says write only in the seat directory plus scratch, and the plan's counting command runs with
`--root <lane>`, so receipts must land in the lane (this seat used its own directory). Pointed
at a fixture (the battery's and this seat's probe's mode), the receipt must land *inside the
fixture*: probe run P1/P2 had to write into the fixture and be copied out, and R-F5 records the
refusal verbatim — `attest.py … --json-out <scratch>/refused.json` at 17:07:46Z, exit 2,
stdout sha256 `1e273744…`, `{"reason": "--json-out outside the lane root: …"}`. Not a claim
violation; a documentation gap worth one line in round 47.

**F6 (LOW; Gate) — S142 adds a duplicate-URL warning.** `corpus/SOURCES.md` 141 → 142 rows
(`227d6982^` vs now), and `W04` 14 (round-45 close) → 15 measured now, the new line being
`S142 duplicate url git-scm.com/docs/git-log across scopes` against this lane's own `S074`
(1 occurrence before `227d6982`, 2 after). The Gate draft states the delta instead of repeating
round 45's "adds no new W04".

## Gates

| gate | result |
|---|---|
| read-only on lane tree | held: every lane write is under `.ufo/waves/round-46/w1/R46W1ScribeLesson/`; `git status --porcelain -- tools/round-46/ plans/ corpus/ SKILL.md LOG.md SCORECARD.md` at 17:07:46Z printed 0 lines (empty stdout, sha256 `e3b0c442…`) |
| frozen bytes never mutated | held: frozen counters were read with `git show 65678df0:…` into a scratch copy (`sha256 db5adc02…` registry, `e6c44d2d…` attest, `847aa33b…` gate) and run from there |
| fixture repo identity | held: each probe fixture `git -C <d> init` in `$S`, `rev-parse --show-toplevel == <d>` asserted before the first commit |
| scratch hygiene | held: receipts copied here first, then `$S` removed; nothing under `/tmp` |
| exit-code semantics | held in reading: 2 is reported as could-not-evaluate, never counted toward a target (R1, R14) |
| `Report:` trailer | `lesson.md` + this report at the paths the prompt names, relative to the lane root |

## Touched surfaces

- Created: `.ufo/waves/round-46/w1/R46W1ScribeLesson/` (dir) — `lesson.md`, `R1`–`R14` JSON,
  `P1`/`P2` JSON, `receipts.tsv`, `probe.out`, `census.out`, `census-validate.out`,
  `driver.sh`, `probe.py`.
- Created: `.ufo/waves/round-46/w1/R46W1ScribeLesson.md` (this report).
- Not touched: `SKILL.md`, `plans/`, `tools/`, `corpus/`, `LOG.md`, `SCORECARD.md`,
  `PROVINCE.md`, `SHONEN.md`, `.ufo/state/`, `.ufo/watchdog.log`, `.scratch/`, any sibling
  seat, the fleet repo.

## Out of scope / not run

- The 38 registry rows (registry-row seats), block 23 edits, `SKILL.md` rule text: not mine.
- Command A (the depth proxy, `citation_resolved_rules 23/23`, `depth_score`) — **not run** by
  this seat; the landed M46-4 row is neither confirmed nor refuted here.
- `attest.py --selftest` / `registry.py --selftest` re-runs, the C1 nine-forgery battery at
  revisions other than R2's, and any mutation of the frozen selftests: **not run**.
- The two absent control receipts (`ctl-c1-1-v1-profile.json`, `ctl-c2-2-ghost-tool.json`)
  were not manufactured: F3 records why the first cannot exist as described at the freeze.
- No verdict on the canonical judge, no commit, no push, no report rewrite.

## Artifact paths

- `.ufo/waves/round-46/w1/R46W1ScribeLesson/lesson.md` — the draft to land.
- `.ufo/waves/round-46/w1/R46W1ScribeLesson/receipts.tsv` — command / exit / stdout sha256 / UTC
  for R1–R14.
- `.ufo/waves/round-46/w1/R46W1ScribeLesson/{R1..R14,P1,P2}.json` — the receipts themselves.
- `.ufo/waves/round-46/w1/R46W1ScribeLesson/{probe.out,census.out,census-validate.out,
  F5-outpath-refusal.out}` — small-text outputs (`probe.out` sha256 `e52a4d11…`, `census.out`
  `065a45eb…`, `F5-outpath-refusal.out` `1e273744…`).
- `.ufo/waves/round-46/w1/R46W1ScribeLesson/{driver.sh,probe.py}` — the exact drivers.
- Scratch `/fast/scratch/hyaku/kaidoku-r46/R46W1ScribeLesson` removed after the copy.
