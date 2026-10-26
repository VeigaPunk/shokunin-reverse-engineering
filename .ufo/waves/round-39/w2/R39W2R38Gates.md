# R39W2R38Gates — r38 gate selftests: parity + mutation

**VERDICT: CONFIRMED** — all 12 recorded round-38 runs reproduce byte/field-exactly under the patched tools (`52b0eb29` == working tree for `tools/round-38/`); all three `--selftest`s are green at baseline and 8/9 core-check mutants go red. 1 survivor = coverage finding (F1); 1 doc-level inconsistency in the landed file itself (F2). No behavioral falsification.

Axes (godspeed): **coverage** (do the selftests detect core-check breakage?) and **depth** (does the patched run mode still reproduce every recorded verdict byte-for-byte?). No tool installs/updates were needed or made; no pacman transactions.

## Environment
- Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` HEAD `e40a25df`; `git diff 52b0eb29 HEAD --stat -- tools/round-38/` empty and `git status --porcelain -- tools/round-38/` clean → working-tree tools are byte-identical to the `52b0eb29` landing. Pristine copies in scratch hashed equal to lane files.
- git 2.56.0, Python 3.14.8, bash 5.3.20, GNU Awk 5.4.1. Scratch `S=/fast/scratch/hyaku/kaidoku-r39/R39W2R38Gates` (TMPDIR pointed there; removed at end).

## Part 1 — Parity: recorded round-38 argv rerun on patched tools

Tool copies run from scratch (`python3 -I -B` / `bash`), `--root` = lane, read-only git only. Recorded argv reconstructed from each record's own fields (freeze/rev/paths; intended-doc opts).

| Arm | Recorded source | Recorded argv (essentials) | Recorded verdict | Rerun verdict | rc | JSON/STDOUT vs record |
|---|---|---|---|---|---|---|
| FD1 | `l1/freeze-drift-077e212b.json` | freeze `e059ca93` rev `077e212b` + 5 default-set paths | drift | drift | 1 | FULL MATCH (every recorded field) |
| FD2 | `l1/freeze-drift-0fc61133.json` | rev `0fc61133` | drift, net_changed=[claims,c1-counter], ships_freeze_bytes=false | identical | 1 | FULL MATCH (true full equality incl. `net_changed`, `ships_freeze_bytes`) |
| FD3 | `l1/freeze-drift-cb4326b2.json` | rev `cb4326b2` | clean | clean | 0 | FULL MATCH |
| FD4 | `l1/freeze-drift-final.json` | rev `7a1ac7fe` | drift, net_changed=[], ships_freeze_bytes=true | identical | 1 | FULL MATCH (full equality) |
| FD5 | `l1/freeze-drift-gen-controls.json` | rev `077e212b`, paths=[`tools/round-38/gen-controls.py`] | drift | drift | 1 | FULL MATCH |
| ID1 | `l1/intended-doc/base.json` | rev=base=`77091b49`, PROVINCE.md, 'REA MCP server', `.ufo/waves/round-19/evidence/doctor/` | not-bound ("intended path not named in the unit row") | identical | 1 | FULL MATCH |
| ID2 | `l1/intended-doc/final.json` | rev `7a1ac7fe` | bound | bound | 0 | FULL MATCH |
| ID3 | `l1/intended-doc/landed-0fc61133.json` | rev `0fc61133` | bound | bound | 0 | FULL MATCH |
| ID4 | `l1/intended-doc/shortcut-s2.json` | rev `HEAD` (literal) | not-bound | **bound** | 0 | DIFF: `verdict`, `reasons` only — see below |
| RI1 | `l1/registry-immutable/base-vs-base.txt` | base=rev=`e059ca93` | (empty) + "exit 0" | (empty) | 0 | match |
| RI2 | `l1/registry-immutable/at-0fc61133.txt` | `e059ca93` → `0fc61133` | "S110 changed columns: 6" + "exit 1" | identical | 1 | match (record appends the rc line; stdout + actual rc identical) |
| RI3 | `l1/registry-immutable/at-final.txt` | `e059ca93` → `7a1ac7fe` | (empty) + "exit 0" | (empty) | 0 | match |

- **ID4 divergence resolved — moving ref, not a tool change.** The record landed in `7a1ac7fe` itself, i.e. `HEAD` at record time was a pre-repair commit. Pin-scan (same argv, pinned revs): not-bound with the identical single reason at `77091b49`, `cb4326b2`, `79f69347`, `f1010f67`, `077e212b`; bound at `0fc61133` and `7a1ac7fe`. `object_at_rev`/`object_at_base` = `27dc0c58…` in both record and rerun (intended doc unchanged). Every plausible then-HEAD reproduces the recorded verdict; today's `HEAD` (`e40a25df`) sits past the pointer repair, hence bound.
- **Default-set ambiguity closed.** Records don't show whether the 5 paths were passed or defaulted; I passed them explicitly and ran FD4b with no path args: `fd4.json == fd4b.json` → `True` (explicit == default-set).
- Deviations (declared): `--json-out` redirected into scratch (original out path unrecorded; the selftest's `json-out-parity` case covers stdout==file); RI recorded `.txt`s embed the recorder's `exit N` echo, so comparison is stdout-text + actual rc.

## Part 2 — Mutation testing of each selftest

Baselines (TMPDIR=$S, fixtures built under $S): `freeze-drift --selftest` → `SELFTEST cases=8 pass=8 fail=0`, rc 0; `intended-doc --selftest` → `cases=9 pass=9 fail=0`, rc 0; `registry-immutable.sh --selftest` → `cases=5 pass=5 fail=0`, rc 0. All in scratch copies; lane untouched.

Pristine sha256: fd `65e5d437…d0fd098` · id `f1653554…409f5e` · ri `b3ea8fc7…17b669` (full hashes re-listed under Restoration).

| Mutant | Tool | Core-check mutation (scratch copy only) | Expected detector | Actual | Verdict | After sha256 |
|---|---|---|---|---|---|---|
| fd-m1 | freeze-drift | drop `-- *[:glob]paths` pathspec from the drift `git log` | clean-history, counter-edited… red | rc 1, `cases=8 pass=6 fail=2` — `clean-history` exit 1≠0; `counter-edited-after-freeze` drift commits ≠ [c2] | **KILLED** | `6118b7a6450d…bc76ab4a` |
| fd-m2 | freeze-drift | ancestor gate `returncode:` → `returncode == 42` (never fires) | non-ancestor-range red | rc 1, `fail=1` — `non-ancestor-range` exit 0≠2 | **KILLED** | `ef5099452b1e…272c8460` |
| fd-m3 | freeze-drift | unknown-rev `cat-file -e` check `and False` | unknown-revision red | rc 1, `fail=1` — `unknown-revision` "reason does not name the unknown revision" | **KILLED** | `f64f9586c3e1…0809f733` |
| id-m1 | intended-doc | `if False and a.intended not in toks:` (pointer check off) | pointer-names-another-path red | rc 1, `fail=1` — expected reason missing | **KILLED** | `5c774c2455bc…6ced9b58b` |
| id-m2 | intended-doc | `elif at_rev != at_base:` → `elif False:` (doc-change check off) | intended-doc-edited-after-base red | rc 1, `fail=1` — exit 0≠1 | **KILLED** | `f10103e286f5…306493f06` |
| id-m3 | intended-doc | unit-row matcher first-cell equality → substring `a.unit in l` | duplicate/absent-row cases red | rc 0, `cases=9 pass=9 fail=0` | **SURVIVED** (F1) | `ce5bc8a7e785…e5ff68c77` |
| ri-m1 | registry-immutable | deletion refusal `!(order[i] in seen)` → `… && 0` | row-deletion red | rc 1, `fail=1` — `row-deletion` exit 0≠1, needle `S003` missing | **KILLED** | `45ca779fb7be…7bcc9bbf48` |
| ri-m2 | registry-immutable | reorder refusal `revorder[i] != common[i]` → `… && 0` | row-reorder red | rc 1, `fail=1` — `row-reorder` exit 0≠1, needle `S001` missing | **KILLED** | `cc7e5581dbe1…c57e6b52ed` |
| ri-m3 | registry-immutable | exempt scope column: add `c!=6` to allowed set | in-place-cell red | rc 1, `fail=1` — `in-place-cell` exit 0≠1, needle `S002 changed columns: 6` missing | **KILLED** | `6b76f86f4ddf…5adbb66fe29` |

Score: **8 killed / 1 survived / 0 inconclusive** across the three selftests; both new registry refusals (deletion, reorder) are real and selftest-covered.

## Findings

- **F1 (coverage, minor) — id-m3 survives.** Loosening intended-doc's row match from *first-cell equality* to *line contains the unit name* leaves all 9 selftest cases green: the fixture never places the unit name in a non-first cell of another row, so the selftest cannot detect a matcher that over-matches (in the real PROVINCE.md the unit string can appear in other cells/rows). Coverage finding only — the shipped matcher itself is correct (ID1–ID3 reproduce exactly). A one-row fixture variant (another unit's row mentioning `REA MCP server` mid-row, expecting `unit rows found: 1`) would kill it.
- **F2 (doc, minor) — landed VARIANT NOTE is self-contradictory.** `tools/round-38/registry-immutable.sh` (as landed at `52b0eb29`) carries: "this copy adds the two append-only checks the round-38 run mode lacks … It is NOT the assigned deliverable; tools/round-38/registry-immutable.sh is unchanged by this seat." Ground truth: `git diff a2f64e1d 52b0eb29 -- tools/round-38/registry-immutable.sh` shows the run-mode awk *did* change (order tracking + deletion/reorder refusals in `END`) plus `--selftest`; the `a2f64e1d` version's `END` is just `exit hit ? 1 : 0` with no selftest. The canonical file was changed and the note says it wasn't — variant-note residue. Behavior is unaffected (RI1–RI3 reproduce; both new refusals killed by m1/m2), but the note misstates provenance and should be corrected by whoever owns that file.

## Restoration & bounds evidence
- Lane tool sha256 before == after (no lane mutation): `freeze-drift.py 65e5d4377c19131a161d6bb8e99b4dd83a860dafdec4288f7017d848fd0fd098` · `intended-doc.py f1653554362a7f73cdac3f0134676a993f09ca4e6bc82c45f89b6fa272409f5e` · `registry-immutable.sh b3ea8fc7e36fa8be0e9dfb98e540b95c3919db65c82d134dc1c7c2973817b669`. All mutations lived only in `$S/mut/` scratch copies, removed with the scratch.
- No git mutations (read-only `show/log/diff/status/rev-parse/merge-base/cat-file` only); no writes outside `.ufo/waves/round-39/w2/artifacts/R39W2R38Gates/` and this report; scratch `S` removed after artifact copy; nothing installed.

## Artifacts (all under `.ufo/waves/round-39/w2/artifacts/R39W2R38Gates/`)
- `selftests/`: `st-fd.out`, `st-id.out`, `st-ri.out` (green baselines, full case lists)
- `parity/`: `fd1..fd5.json/.out`, `fd4b.out` (default-set equivalence), `id1..id4.out`
- `mutants/`: `m-fd1..3.out`, `m-id1..3.out`, `m-ri1..3.out` (full per-case outputs)
