# A2CitedReport — cited-runs gate over the filed round-31 fleet report

Seat `KaidokuR32A2.A2CitedReport` (leaf, attempt 2). Report finalized 2026-10-23T06:58Z; run timestamps below are per-run.
Attempt 1's `ExecCitedRuns` seat produced no usable report (omp SIGSEGV 06:19:06Z); nothing from it was read or reused.

## Identity and pin

| item | value |
|---|---|
| lane | `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` |
| git HEAD at run start (06:45:30Z) | `f382e3b7978e6091a19ca93277c15a75c0016b43` |
| git HEAD observed at 06:52:09Z (peer commit) | `411f3a80a1efefabe2ba12f227147023cfbce4bd`; `git merge-base --is-ancestor f382e3b7 411f3a80` exit 0; `git diff --quiet f382e3b7 411f3a80 -- tools/round-31/cited-runs-gate.py` exit 0 |
| report under test | `/home/vgpnk/Projects/shokunin/.ufo/reports/round-31/kaidoku.md`, 11,261 bytes, sha256 `1e135cbeca5a8c0862c3496a76603f1125c5673d0d464e1d63ee1d53150bbb84`, mtime `2026-10-23 01:45:03 -0300` |
| report provenance | committed in the fleet repo at `dcd6c59` ("round-31: kaidoku report", 2026-10-23T01:45:09-03:00); `git show dcd6c59:… | sha256sum` equals the working-file hash above; `git status --porcelain -- …` empty |
| gate | `tools/round-31/cited-runs-gate.py`, 21,664 bytes, mode 0755, sha256 `f025ac052da465935a2f9cededda67e6a13c5203fdd116dc117b971db4418b83`; worktree blob `94ae4b567be5bf7ca103af5b4ff77dcd2ef5ae65` equals `f382e3b7:tools/round-31/cited-runs-gate.py` |
| ordered tools | python3 3.14.8 (`/usr/bin/python3`), git 2.56.0 |
| disk | `df -h /fast`: 804G, 560G used, 244G avail, 70% (06:45:30Z); no rebuild was needed or run |

Gate bytes were executed from a scratch copy whose sha256 equals the lane file and the pin blob; see R2.

## Usage inspected before running

`--report`, `--lane`, `--rev` are all required; `--selftest` takes none of them (`--selftest` with any of the three → usage error, exit 2). Exit codes 0 = every assertion backed, 1 = at least one finding, 2 = usage error.

The contract the run tests, quoted from `tools/round-31/cited-runs-gate.py:16-18` (sha256 `f025ac05…`):
> Every assertion line must cite at least one lane path under `.ufo/waves/` or `corpus/evidence/` that exists as a blob at --rev

The blob read is at the `--rev` pin, not at any revision named inside a citation (`:164`):
> kind = run_git(self.lane, ["cat-file", "-t", "%s:%s" % (self.rev, path)])

`--selftest` seeds its throw-away repo beside the script (`:402`): `base = os.path.dirname(SCRIPT)`. Running it in place would therefore create a directory under the lane's `tools/round-31/`; to keep the lane read-only, the byte-identical scratch copy was used instead.

## Runs

### R1 — gate over the filed report (pin f382e3b7)

Started/ended `2026-10-23T06:47:04Z` / `2026-10-23T06:47:04Z` (1 s clock resolution). Exit **0**.

Exact argv:

```text
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE /usr/bin/timeout --signal=TERM --kill-after=5s 600 /bin/bash -c 'ulimit -v 4194304; exec /usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r32/a2audit/A2CitedReport/cited-runs-gate.py --report /home/vgpnk/Projects/shokunin/.ufo/reports/round-31/kaidoku.md --lane /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev f382e3b7978e6091a19ca93277c15a75c0016b43'
```

stdout (full), saved as `fleet.out` (sha256 `d530e69a5d9a48603f1f0db036df09dee9db778ef0b6813e5c9e97396b727851`):

```text
cited-runs-gate: ok assertions=7 report=/home/vgpnk/Projects/shokunin/.ufo/reports/round-31/kaidoku.md rev=f382e3b7978e6091a19ca93277c15a75c0016b43
```

stderr empty (`fleet.err` = 0 bytes, sha256 `e3b0c442…b855`). `fleet.exit` = `0`.

### R2 — selftest (byte-identical copy, scratch)

Started/ended `2026-10-23T06:47:04Z` / `2026-10-23T06:47:04Z`. Exit **0**.

Exact argv:

```text
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE /usr/bin/timeout --signal=TERM --kill-after=5s 300 /bin/bash -c 'ulimit -v 4194304; exec /usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r32/a2audit/A2CitedReport/cited-runs-gate.py --selftest'
```

stdout (full), saved as `selftest.out` (sha256 `4963578bc5aa6634dd60200b0fb86b50248cf26933f763dcb85326adc1d5cd63`):

```text
SELFTEST case backed-pass: PASS (exit 0)
SELFTEST case uncited-pass: PASS (exit 1)
SELFTEST case path-absent-at-rev: PASS (exit 1)
SELFTEST case path-present-at-base-rev: PASS (exit 0)
SELFTEST case token-absent: PASS (exit 1)
SELFTEST case red-receipt-clean: PASS (exit 1)
SELFTEST case counter-backed: PASS (exit 0)
SELFTEST case counter-miscount: PASS (exit 1)
SELFTEST case exit0-equals-form: PASS (exit 0)
SELFTEST case exit0-red: PASS (exit 1)
SELFTEST case shorthand-relative: PASS (exit 0)
SELFTEST case outside-prefix: PASS (exit 1)
SELFTEST case mixed-lines: PASS (exit 1)
SELFTEST case no-assertion: PASS (exit 0)
SELFTEST case usage-no-args: PASS (exit 2)
SELFTEST case usage-bad-rev: PASS (exit 2)
SELFTEST case usage-missing-report: PASS (exit 2)
SELFTEST ok cases=17 passed=17
SELFTEST repo=/fast/scratch/hyaku/kaidoku-r32/a2audit/A2CitedReport/cited-runs-gate-selftest-cg2_aj4j (removed)
```

stderr empty (sha256 `e3b0c442…b855`); `selftest.exit` = `0`. The temp repo was created under `/fast/scratch/...` and removed; `ls` after the run shows no `cited-runs-gate-selftest-*` residue.

### R3 — per-line assertion map (same gate functions, read-only driver)

Started `2026-10-23T06:47:39Z`, exit 0. Driver `audit_assertions.py` (sha256 `eb9016b4802e9ffc310742eb4d70bc54a4421b7437851098f54e8568efe7853f`) imports the scratch copy and calls `asserted_tokens`, `citation_candidates`, `blob_text`, `Gate.check`; output `audit.out` (sha256 `18544e4c9b830f5a0a34f1bdbcfec35fda31f4ce54e49ccd2bddb7251bfbeddf`). It reports `round_name='round-31' lines=142`, `asserted=7 findings=0 notes=0`.

The seven classified lines, all resolved to committed blobs at `f382e3b7`:

| line | asserted tokens | citation(s) that back every token |
|---|---|---|
| 34 | `PASS` | `.ufo/waves/round-31/after/cited-runs-gate-round30-report.txt` (blob `37d8daee…`) — see F6 |
| 59 | `exit 0`, `carriers=12`, `pass=12`, `target=12` | `…/after/c1-sqlite-positive-at-0007731e.txt` (blob `859b070a…`) and `…/after/c1-sqlite-positive-at-tip-16c00c2d.txt` (same blob) |
| 64 | `exit 0`, `requests=23`, `matches=23`, `target=23` | `…/after/c2-sqlite-refusals-at-0007731e.txt` (blob `cf9b2e66…`) and `…/after/c2-sqlite-refusals-at-tip-16c00c2d.txt` (same blob) |
| 66 | `CLEAN` | `…/after/freeze-integrity-at-tip-16c00c2d.txt` (blob `60e0d5ab…`) |
| 67 | `PASS` | `…/after/settle-gate.txt` (blob `1935411e…`) |
| 82 | `exit 0` | `…/before/sources-census-start.txt` (blob `c86c90e1…`) |
| 83 | `exit 0` | `…/after/sources-census-end.txt` (blob `05cad42f…`) |

Other citations on lines 59 and 64 (`at-tip-16c00c2d`) are also present at the pin and hold the same tokens. The driver's per-candidate dump shows the gate tried only paths under `.ufo/waves/` and `corpus/evidence/`. The six `tools/round-31/…` mentions in the report are rewritten to `.ufo/waves/round-31/tools/…` and `corpus/evidence/round-31/tools/…`, which are not blobs at the pin; they back nothing.

### R4 — falsifiability controls on this exact report text

Generator `make_mutants.py` (sha256 `83c97eb764750df6694842b6541135f33ade72a3e092058d06a16b4d751ad74e`) copies the filed report to `/fast/scratch/.../ctl/.ufo/reports/round-31/` and applies one replacement each, asserting exactly one occurrence. Started/ended `2026-10-23T06:49:59Z`/`06:50:00Z`. Every run used the same lane and pin as R1.

| mutant | change | report sha256 | exit | stdout finding |
|---|---|---|---|---|
| m0-identical | none | `1e135cbe…` (equals filed report) | 0 | `cited-runs-gate: ok assertions=7 …` |
| m1-citation-absent | line 67 cites `settle-gate-missing.txt` | `1c65c4c0…` | 1 | ``UNCITED 67: - Settle ledger: `settle: PASS` (`.ufo/waves/round-31/after/settle-gate-missing.txt`).`` |
| m2-token-absent | line 66 cites `settle-gate.txt` (holds `PASS`, not `CLEAN`) | `aa1e7048…` | 1 | `UNBACKED 66: .ufo/waves/round-31/after/settle-gate.txt lacks CLEAN` |
| m3-counter-mismatch | line 64 asserts `requests=24` | `3222d65c…` | 1 | `UNBACKED 64: .ufo/waves/round-31/after/c2-sqlite-refusals-at-0007731e.txt lacks requests=24` |

Each mutant produced exactly one finding; m0's report file is byte-identical to the filed report and reproduced the green result. Stderr for m1/m2/m3 each carried the matching `note:` plus `cited-runs-gate: FAIL findings=1 assertions=7 …`; m0 stderr was empty.

### R5 — lines the gate does not classify (completeness scan)

Started `2026-10-23T06:51:37Z`, exit 0. Driver `blind_spot_scan.py` (sha256 `4a7a5223b5732768a72320d2d1e8fa3dc55508010692dc96eff4e6c4e72d4085`), output `blind2.out` (sha256 `1bb4e2b0997f9e099e9c87046f07a2185156672c680bb7aa43dabc56981409fe`). It lists result-shaped lines with no gate-recognised token: `delta=2, exit-code=5, ratio=5` — 12 distinct lines: 21, 23, 24, 58, 63, 72, 90, 91, 99, 101, 102, 106. (An earlier scan without the `delta` pattern, `blind.out` sha256 `cbeb9b80…`, is superseded.)

## Findings

**F1 — Gate is green at the pin (exercised).** Exit 0, `assertions=7`, zero findings, empty stderr, over report sha256 `1e135cbe…` at `f382e3b7`. This is the receipt the routed item lacked: the gate really was run over the filed round-31 report with the current lane. Scope: exactly seven success-token lines are certified; nothing else is.

**F2 — Selftest is green from identical bytes (exercised).** 17/17 cases, exit 0. The executed copy is sha256-identical to the lane file and to the pin blob (`94ae4b56…`). No lane write occurred; the script's in-place temp-repo behaviour (`:402`) was avoided by running the copy in scratch.

**F3 — The green result is falsifiable on this report (exercised).** Three one-point mutations of the filed text produced the expected `UNCITED`/`UNBACKED` finding and exit 1, and an unmodified copy reproduced exit 0 with the same report hash. The green run is therefore not a parse no-op.

**F4 — Citation resolution is existence-at-pin, not run-revision attribution (exercised; one inference).** The two receipts cited on lines 59 and 64 under the name `…-at-0007731e.txt` do **not** exist at `0007731e`:

| path | 0007731e | f368a101 | 16c00c2d | f2f5977b | f382e3b7 | first added |
|---|---|---|---|---|---|---|
| `after/c1-sqlite-positive-at-0007731e.txt` | absent | absent | present | present | present | `1288285e` |
| `after/c2-sqlite-refusals-at-0007731e.txt` | absent | absent | present | present | present | `1288285e` |
| `after/c1-sqlite-positive-at-tip-16c00c2d.txt` | absent | absent | absent | present | present | `f2f5977b` |
| `after/c2-sqlite-refusals-at-tip-16c00c2d.txt` | absent | absent | absent | present | present | `f2f5977b` |

`git cat-file -e <rev>:<path>` produced this matrix; `git log --diff-filter=A` gave the add commits. Neither at-`0007731e` receipt contains any `rev`/`0007731e` marker in its bytes (`grep -n -i -E 'rev|0007731e'` exit 1 on both). At the pin, each `at-0007731e` receipt is the same blob as its `at-tip` counterpart (`859b070a…` C1, `cf9b2e66…` C2), so the committed bytes are at least consistent across both claimed runs. The filename rev and the commit subject of `1288285e` — "round-31: SCORECARD round-31 section, LOG entry, round-29 docstring supersession entry, after receipts at 0007731e (C1 12/12, C2 23/23, freeze-integrity CLEAN)" — are the only committed link between those counters and rev `0007731e`. **[INFERENCE]** the counters did run at `0007731e`; the receipt bytes do not prove it, and the gate cannot check it because it resolves every citation at `--rev` (line 164). This is the one substantive gap between "green gate" and "run at the named rev proved".

**F5 — Twelve result-shaped lines are outside the gate's coverage (exercised).** R5 lists 5 exit-code lines (21, 58, 63, 90, 91), 5 ratio lines (23, 24, 101, 102, 106) and 2 delta lines (72, 99). Line 91 — "the cited-runs gate exits 1 on the round-30 report" — carries no citation at all; the same fact is cited on line 34 by `.ufo/waves/round-31/after/cited-runs-gate-round30-report.txt`, whose committed bytes end `cited-runs-gate: FAIL findings=8 assertions=9 …` and `exit=1` (observed). The gate's docstring limits assertions to success tokens (`PASS`, positive `CLEAN`, `exit 0`, `key=<int>`), so these are a documented boundary, not a violation of the gate; but the green RA receipt does not certify any of them.

**F6 — Line 34 is a syntactic false-positive assertion, harmlessly backed (exercised).** The line reads `- Defect 1, gate PASS claims without committed receipts: …`. `PASS` there is prose ("gate PASS claims"), not a gate result, yet `asserted_tokens` classifies the line and demands `PASS` in a citation. It is satisfied only because the cited receipt contains the word `PASS` inside its diagnostics and quoted excerpts (`note: line 16 asserts 'PASS'; …` and `UNBACKED 16: .ufo/waves/round-30/settle.tsv lacks PASS`). Had the receipt been worded without `PASS`, this prose line would have produced a false `UNBACKED` **[INFERENCE]** from the token matcher; no such wording was tested. No suppression or gate change was made; the observed verdict was 0, and the exit did not depend on this line being semantically correct.

**F7 — Read-only lane, concurrent peers, no interference with committed receipts (exercised).** This seat's lane commands were read-only (`rev-parse`, `cat-file`, `show`, `log`, `status`, `diff --quiet`, `hash-object`); the only file written under the lane is this report. The lane worktree was dirty and changing while I worked — `git status --porcelain` counts 14 (06:45:30Z), 15, 16, 32, 34 (06:52:33Z) — including tracked edits to `SKILL.md`, `corpus/QUALITY.md`, the claim-freezes TSVs, one knowledge file and `corpus/lessons/round-31.md`, plus untracked `a2audit/` peer reports. The gate reads only committed blobs at `--rev` (line 164) and the gate file's worktree bytes equal the pin blob, so those concurrent edits cannot alter R1's receipts. Peer commit `411f3a80` landed after R1; `f382e3b7` remains its ancestor and the gate file is unchanged between them. No process of mine survived: `pgrep -af 'A2CitedReport|cited-runs-gate'` at 06:52:09Z returned none.

## Evidence index (scratch, `/fast/scratch/hyaku/kaidoku-r32/a2audit/A2CitedReport/`)

| file | sha256 |
|---|---|
| `cited-runs-gate.py` (== lane/pin bytes) | `f025ac052da465935a2f9cededda67e6a13c5203fdd116dc117b971db4418b83` |
| `fleet.out` / `fleet.err` / `fleet.exit` | `d530e69a…` / `e3b0c442…` (empty) / `0` |
| `selftest.out` / `selftest.err` / `selftest.exit` | `4963578b…` / `e3b0c442…` (empty) / `0` |
| `audit_assertions.py` / `audit.out` / `audit.err` | `eb9016b4…` / `18544e4c…` / `e3b0c442…` (empty) |
| `make_mutants.py` | `83c97eb7…` |
| `ctl/.ufo/reports/round-31/m0-identical.md` | `1e135cbe…` (equals filed report) |
| `ctl/.ufo/reports/round-31/m1-citation-absent.md` | `1c65c4c0…` |
| `ctl/.ufo/reports/round-31/m2-token-absent.md` | `aa1e7048…` |
| `ctl/.ufo/reports/round-31/m3-counter-mismatch.md` | `3222d65c…` |
| `mut-m1-citation-absent.out` / `mut-m2-token-absent.out` / `mut-m3-counter-mismatch.out` | `1b318d67…` / `a5d203f7…` / `30d559ea…` |
| `blind_spot_scan.py` / `blind2.out` / `blind2.err` | `4a7a5223…` / `1bb4e2b0…` / `e3b0c442…` (empty) |

Timestamps are in `selftest.started/.ended`, `fleet.started/.ended`, `audit.started/.ended`, `muts.started/.ended`, `blind2.started/.ended`.

## Limits

- The gate certifies token existence in committed blobs at `--rev`; it does not certify the revision a receipt was produced at (F4), does not cover red/ratio/delta claims (F5), and classifies prose tokens literally (F6). None of these were changed or worked around.
- No tool was installed or updated; no pacman transaction was attempted.
- No counter, predicate, target or carrier was executed or edited. No lane or fleet git/jj state was written, staged, committed, or pushed.
- The fleet report under test is the committed `dcd6c59` blob (hash-equal to the working file), so R1's input is reproducible from the fleet repo.

## Closure statement

The routed item's missing receipt now exists and is green: `cited-runs-gate: ok assertions=7 … rev=f382e3b7…`, exit 0, plus `SELFTEST ok cases=17 passed=17`, exit 0, plus three failing mutants proving the verdict is falsifiable on this text. Its honest scope is F4–F6: seven success-token lines are backed at the pin; the `at-0007731e` run-revision attribution and the twelve red/ratio/delta claims are not certified by this run.
