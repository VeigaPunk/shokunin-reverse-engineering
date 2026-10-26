# R39W2RegistryReview — SKILL.md `### Round-35/37/38/39 instrument registry` vs the tools

**Verdict: DEFECTS FOUND** — 17 of 22 rows verify cell-by-cell against the code and live runs; 5 rows carry false cells: one material verdict-map falsehood (`registry-immutable.sh` bad-revision behaviour), one undeclared exit code (`mk-carriers.py` exit 3), one self-contradictory verdict-map cell (`round-37/c1-run.sh`), and two wrong line-number pins (`freeze-drift.py`, `round-37/c1-counter.py`). Every self-test command exists, runs as stated, and prints exactly the stated case count; every gate's entry command reproduces the recorded verdict.

Reviewed text: `SKILL.md` at `52b0eb2907c704ed5f184c47b14c723208e5cbbc`, lines 1333–1354 (full rows copied to `artifacts/R39W2RegistryReview/registry-rows-and-pins.txt`). `git diff 52b0eb29..HEAD -- tools/ SKILL.md` is empty, so the working-tree tools are the reviewed bytes. Wave-1 source-read revision for the round-35/37/38 rows is `a2f64e1da78afcf8cc39287106604dbcc270844c` (per the section preamble); between `a2f64e1d` and `52b0eb29` only `tools/round-38/{freeze-drift.py,intended-doc.py,registry-immutable.sh}` changed (diffstat: +179/+171/+102), so line pins for unchanged files were checked at both revisions and give the same answer.

Method: every self-test command executed verbatim; every gate's entry command executed at the recorded revisions; every verdict-map cell checked against the code's exit paths (`main`/`sys.exit`/`return` reads) and, where cheap, probed empirically; every write-scope cell checked against the code's write sites; every line-number pin checked at `a2f64e1d` (and at `52b0eb29` for the three changed gates). Evidence files under `artifacts/R39W2RegistryReview/` hold the exact commands and outputs.

## Findings (false cells), by severity

### F1 (medium) — `tools/round-38/registry-immutable.sh` verdict-map cell: the claimed bad-revision behaviour is false

Cell (verdict map): "…No `2`: a bad revision makes the `git show` row set fail under `set -e`, so bash exits with git's own code (**128 expected, not exercised**) and that code is undeclared → reads could-not-evaluate."

Measured (both directions, evidence `false-cells-evidence.txt`):

```
$ bash tools/round-38/registry-immutable.sh $LANE 0000000000000000000000000000000000000000 52b0eb29…
fatal: path 'corpus/SOURCES.md' exists on disk, but not in '0000…'
S001 row deleted (append-only) … S122 row deleted (append-only)   [122 lines]
EXIT=1
$ bash tools/round-38/registry-immutable.sh $LANE a2f64e1d… 0000000000000000000000000000000000000000
fatal: … ; S001…S117 row deleted (append-only)
EXIT=1
```

A bad revision exits **1** — the *declared* "rows changed" code — with an `S### row deleted (append-only)` line for every row, not git's 128. Mechanism: `rows()` is only ever invoked inside the process substitutions `<(rows "$base") <(rows "$rev")`; a failing `git show` there does not trigger `set -e`/`pipefail` in the main shell, and the empty feed defeats awk's `NR==FNR` base/rev split (with an empty first file, every rev row is misread as a base row; `seen` stays empty; the END block reports every row deleted and `exit 1`). The row's own hedge "(128 expected, not exercised)" is falsified: an unevaluable invocation reads as a **drift violation** (false positive), not could-not-evaluate. Same false-positive class for any base at which `corpus/SOURCES.md` has no `S`-rows. The gate's clean/drift cases themselves verify (selftest 5/5; live run `a2f64e1d→52b0eb29` → 0 silent), so only this cell is false.

### F2 (low) — `tools/round-39/mk-carriers.py` verdict-map cell: undeclared exit 3

Cell: "`0` written; `2` usage or a refused carrier". Code (`main`): the manifest write is wrapped in `except OSError → print 'cannot write …' → return 3`. Measured (evidence `mkcarriers-heldout-evidence.txt`): `--out` into a `chmod 500` dir → `mk-carriers: cannot write …: [Errno 13] Permission denied` → **EXIT=3**, outside the declared map. (Argparse errors do exit 2, as stated.)

### F3 (low) — `tools/round-37/c1-run.sh` verdict-map cell is self-contradictory

Cell: "`2` usage/environment (**bad mode, carrier id absent from `carriers.json**`, …)" and, later in the same cell, "Undeclared `1`: an unknown carrier id aborts under `set -e` from the python lookup (exercised → `1`)". Both clauses describe the same case, with different codes. Measured: `c1-run.sh after KZ …` → `unknown carrier KZ` → **EXIT=1**; the `2` path for a carrier is a missing carrier *file* (`[[ -f $carrier ]] || exit 2`), not an absent id. The `2`-list item "carrier id absent from `carriers.json`" is false (the truth is disclosed in the same cell's undeclared-1 note, so the cell contradicts itself rather than the reader).

### F4 (low) — `tools/round-38/freeze-drift.py` pinned-value cell: line pin off

Cell: "the default set (`:26-32`) is the round-38 kill rule…". At the stated read revision `a2f64e1d`, `DEFAULT = [` is at **:25** (list `:25-31`); at the landing commit it is `:32-38`. Content is correct (claims doc, both counters, carriers manifest, oracle glob — 5 paths); the pin is wrong at both revisions. Evidence: `registry-rows-and-pins.txt`.

### F5 (low) — `tools/round-37/c1-counter.py` pinned-value cell: line pin off

Cell: "(`git()` `:33-36` returns bytes)". `def git` spans **:29-33** (file unchanged `a2f64e1d→52b0eb29`). The substance is correct and the neighbouring pins are exact: the `TypeError: a bytes-like object is required, not 'str'` lands at `load_oracle` **:93** (reproduced, exit 1), the selftest `FileNotFoundError` at `make_fixture` **:323** (reproduced, exit 1), the spliced fixture block at **:163-186** referencing an undefined `d` (confirmed in source). Evidence: `probe-evidence2.txt`, `registry-rows-and-pins.txt`.

## Verified-true cells (per row; all commands in the cited evidence files)

Legend: map = verdict map vs code exit paths; st = self-test command + stated case count; entry = entry command runs as stated; ws = write scope; pins = pinned-value path.

| row | map | st | entry | ws | pins |
|---|---|---|---|---|---|
| `round-35/c1-coverage-counter.py` | ✓ (0 `C1_CLEAN`/1 `C1_FAIL:`/2 missing-args·claims-absent·unparseable·predicate-mismatch; no catch-all → crash reads `failed`, as the cell states) | ✓ `C1_SELFTEST: ok`, `green=0 red=1`, exit 0 | n/a (no run cited in row) | ✓ `--json-out` only; selftest `TemporaryDirectory` removed; disclosed always-all-true `checks` map confirmed at `:184` | ✓ `ENTRIES` `:16-19`, 11-col `ROW_RE` `:22`, claims path, S125/S129, selftest `:42-118` |
| `round-35/c2-calibration-counter.py` | ✓ (0/1/2; uncaught → 1) | ✓ `C2_SELFTEST: ok`, `green=0 red=1`, exit 0 | n/a | ✓ `--json-out` only; tempdir removed | ✓ `EIGHT_CELL_SECTIONS` `:21`, `SETTLE_FILES` `:26`, `LESSON_PATH` `:31`, `CENSUS_PATH` `:32`, `R34B_ENTRY` `:33`, census literals `:68` (predicate span `:7-19` vs actual `:7-18` — cosmetic, not reported as a defect) |
| `round-37/c1-counter.py` | ✓ (probe; declared 0/1/2; all three observed failure modes reproduced exactly: `--selftest` w/o args → 2, placeholder → 1 `FileNotFoundError` `:323`, scoring at base → 1 `TypeError` `:93`) | ✓ no working selftest, as stated | ✓ (the crashes are the stated behaviour) | ✓ `--json-out`; crashed selftest leaves `kaidoku-r37/selftest/` behind (re-observed) | ✓ except F5 (`:12-16`, `:93`, `:323`, `:163-186`, `sasquatch_v4be_sha256` literal `fac88740…` exact, `PINS` construction, carriers.json read at `--rev` only) |
| `round-37/c1-run.sh` | **F3** (rest ✓: 0 receipt written; 2 bad mode — measured; 3 REA child non-zero; undeclared 1 unknown-carrier — measured) | ✓ no selftest | ✓ `after K1` → 0, `<mode>.json` + `<mode>-run.json` with all stated fields | ✓ OUTDIR files + removed `kaidoku-r37/c1-run.XXXXXX` | ✓ carriers.json path; `rea-agents@6.5.0` + `timeout 900` hardcoded; 10-line stderr head |
| `round-37/gen-squashfs.py` | ✓ (0 written / 2 argparse; no `sys.exit` — grep) | ✓ no selftest | ✓ two `le/gzip` runs byte-identical (`12ab150b…` twice); magics `hsqs`/`sqsh` measured | ✓ writes the out image only; docstring `:2-4` limits | ✓ `MAGIC :7`, `COMP :8`, `MKFS_TIME :14`, `UID :15`, gzip level 9 (`zlib.compressobj(9,…)`), xz preset 6 |
| `round-38/c1-counter.py` | ✓ (0 met / 1 not met / 2 incl. carriers·xpin-absent-at-freeze; uncaught → 1, as stated) | ✓ 15 cases, `green_ok 1, red_ok 14`, exit 0 | n/a | ✓ `--json-out`; `kaidoku-r38/c1-counter.*` removed (`:198`,`:389`) | ✓ constants `:28-37` exact; selftest reads `dev-after.json`/`dev-oracle.tsv` from the working tree (`:273-274`) + `xpin-attribute.mjs` |
| `round-38/c1-run.sh` | ✓ (child status propagated; oracle sasquatch-fail → 1; bad mode → 2 measured; missing arg → 1 measured) | ✓ no selftest | n/a (usage paths measured) | ✓ OUTDIR (removed first) / OUTDIR tree + TSV on stdout; scratch `kaidoku-r38/c1-run-$$` | ✓ `rea-agents@6.5.0` argv; `REA_UNBLOB_COMMAND` required, absolute; `before` strips `$HOME/.local/bin` |
| `round-38/c2-counter.py` | ✓ (0/1/2; uncaught → 1; `except Unevaluable` `:256`) | ✓ 14 cases, `green_ok 1, red_ok 13`, exit 0 | n/a | ✓ `--json-out`; `kaidoku-r38/c2-selftest.*` removed (`:346`) | ✓ `TOKEN/PTR/LANE` `:27-29`, `BOX1/BOX4` `:30-31` exact |
| `round-38/freeze-drift.py` | ✓ (0 clean / 1 drift / 2 unknown-rev·non-ancestor·git-log-failure·argparse; selftest cases match) | ✓ 8 cases, exit 0 | ✓ live run freeze `8fcda41c` → rev `6fdaf4f1`, default paths → `clean`, drift 0, exit 0 | ✓ `--json-out` only; read-only git log/diff | **F4** (pin `:26-32` vs actual `:25-31` at base); parity claim ✓ (`R39CL2Selftests.md`: "18/18 parity runs, 0 mismatches") |
| `round-38/intended-doc.py` | ✓ (0 bound / 1 not-bound / 2 file-absent-at-rev·at-base·argparse; all 9 selftest cases match the map) | ✓ 9 cases, exit 0 | ✓ wave-1 receipts are fixture-scoped (their commits `1b93891e`/`2be55397` exist only in that seat's scratch fixture — `cat-file` fails in the lane; expected, disclosed in `R39CL2Registry.md` §2) | ✓ stdout JSON only; argparse has no `--json-out` | ✓ `--intended` + `--unit` first cell; `<rev>:<intended>` vs `<base>:<intended>` identity; no digest file |
| `round-38/registry-immutable.sh` | **F1** (rest ✓: 0 silent — measured live; 1 `<id> changed columns: n` — selftest; deletion/reorder → 1 as the landed variant adds) | ✓ 5 cases, exit 0 | ✓ `a2f64e1d→52b0eb29` → 0 silent | ✓ stdout only; read-only | ✓ allowed columns 9/11/12; BASE `S`-row field-by-field compare |
| `round-38/gen-controls.py` | ✓ (0 control-missed / 1 kill / 2 internal·missing-out·unknown-kind) | ✓ no selftest — exactly two `selftest` hits (docstring `:34`, fixture-dir `:41`) | ✓ `c1-1` → stdout `{"control":"c1-1","counter_exit":1,"kill":false}`, exit 0 | ✓ `--out` receipt; `kaidoku-r38/controls-<kind>/` scratch | ✓ `PKG65` default exact; imports the counters via importlib (`:35-37`,`:97-99`) — not-independent, as disclosed |
| `round-38/selftest/` (4 files) | ✓ data row, no verdict | ✓ not executable | n/a | ✓ read-only inputs | ✓ all four sha256 pins exact (`d9193aea…`, `69a8abd5…`, `ff1587fe…`, `acc64a3d…`); read by `c1-counter.py:273-274` + `gen-controls.py:42-43`; `dev-before.json`/`dev-le-xz.sqsh` have no consumer under `tools/` (the only `dev-before.json` reader is `tools/round-36/c1-counter.py:269`, which reads round-36's own copy) |
| `round-39/c1-counter.py` | ✓ (0 met / 1 not met / 2 incl. `frozen_path_changed`; usage → 2; `FrozenPathChanged.reason` exact) | ✓ 33 cases, `green_ok 1, red_ok 32`, exit 0 | ✓ rev `6fdaf4f1`, freeze `8fcda41c` → met, 6/6, unchanged, exit 0 (matches the recorded score `c1-at-6fdaf4f1.json`) | ✓ `--json-out` + private scratch `$HYAKU_SCRATCH/kaidoku-r39/counter` | ✓ `.ufo/waves/round-39/c1/carriers.json` |
| `round-39/c1-run.sh` | ✓ (0 ok / 2 usage-environment / 3 tool failure; after-arm no-receipt → 3, oracle sasquatch-fail → 3 in code) | ✓ none in script; wave-1 `R39C1Harness.md` states the 68-case external selftest | ✓ `after` + `oracle` on K1 → 0/0, receipts + oracle TSVs written | ✓ OUTDIR + removed scratch; foreign-scratch refusal measured → 2 | ✓ (see O3) |
| `round-39/mk-carriers.py` | **F2** (rest ✓: 0 written; 2 usage + refused carrier measured) | ✓ none | ✓ regenerates the frozen `carriers.json` **byte-identically** (`cmp` identical) from the six carriers' own paths/oracles/symlinks | ✓ `--out` (tmp+replace inside its dir) | ✓ — |
| `round-39/sqfs-list.py` | ✓ (0 ok / 2 `SqfsError`; garbage input measured → 2) | ✓ none (wave-1 `R39C1IndepReader.md` exists) | ✓ K-tree image → 0, TSVs + `--inspect` JSON | ✓ the `--files`/`--symlinks` outputs (+stdout) | ✓ — |
| `round-39/gen-squashfs.py` | ✓ (0 written / 2 argparse measured) | ✓ none | ✓ image written, exit 0 | ✓ the output image only | ✓ K5/K6 pins present in `carriers.json`; the two advertised fixes confirmed in the source delta vs round-37 (xz container id 4 + UTF-8 byte-length names) |
| `round-39/sqfs-triage.py` | ✓ (0 labelled / 2 `TableError`·`EnvelopeError`·`InvocationError`; 1 only for failed `--selftest` — adversarial envelopes (string in `files`, non-list `chunks`, top-level array) all stay 0/2) | ✓ 35 cases, exit 0 | ✓ real `SKILL.md` + K1 envelope → `escaping-symlink-removed`, exit 0 | ✓ stdout only | ✓ marker `<!-- sqfs-triage-table v1 -->` in `SKILL.md` |
| `round-39/heldout-gen.py` | ✓ guards measured: existing-out → 1, unknown class → 1, bad seed → 1 (see O2 for the undeclared `--run`-failure 1) | ✓ none (wave-1 `R39C2HeldoutGen.md` exists) | ✓ fresh `--out`, seed = freeze hash → 0, 20 carriers (10 classes × 2) | ✓ `--out` (+ removed scratch) | ✓ seed = R39-C2 freeze hash |
| `round-39/c2-counter.py` | ✓ (0 met / 1 not met / 2 incl. `frozen_path_changed` `:161` and `no_manifest_at_rev` `:165` — both reasons exact) | ✓ 27 cases, exit 0 | ✓ rev `6fdaf4f1`, freeze `8fcda41c` → met, 20/20, exit 0 (matches `c2-at-6fdaf4f1.json`) | ✓ `--json-out` + private scratch `kaidoku-r39/c2-counter.*` removed in `finally` | ✓ `corpus/evidence/round-39/c2/heldout/manifest.json` |
| `round-39/absence-sweep.py` | ✓ (0 ABSENT / 1 PRESENT / 2 usage·unreadable-root; INCOMPLETE → 2) | ✓ 18 cases, exit 0 | ✓ fleet-root arm re-run → `VERDICT ABSENT`, exit 0 (both-roots arm not re-run: bounds forbid running tools against `/home/vgpnk/Projects/shokuknow`; the recorded `l1/absence/summary.txt` stands) | ✓ stdout only (`--json` also prints to stdout) | ✓ — |

Preamble checks: the cross-reference to wave-1 `R39CL2Registry.md` is accurate (the file exists and matches what the rows say, including its "could not verify" list); the "uncaught exceptions in the round-35/37/38 Python counters exit 1" sentence is true for all five counters it names (verified in code for r35 ×2 and r38 ×2, observed for r37); the `tools/round-37/c1-counter.py` probe sentence matches the code and the reproduced crashes.

## Observations (residual risk, not false cells)

- **O1** — The round-39 counter rows omit what the round-35/37/38 rows state explicitly: `c1-counter.py`/`c2-counter.py` catch only `Unevaluable`, so an uncaught exception (e.g. malformed `carriers.json` at freeze → `JSONDecodeError`) exits 1 and reads "not met". The preamble's crash sentence covers round-35/37/38 only. Same hazard class as wave-1 F3, now undocumented for the round-39 pair.
- **O2** — `heldout-gen.py` with `--run` returns **1** when any REA run errors (`if failures: return 1`); the row's `1`-cell lists only the three guards and says "REA failures recorded per carrier" without the exit code. Argparse errors (exit 2) are also undeclared.
- **O3** — `round-39/c1-run.sh`'s pinned-value cell says "carrier pins in `carriers.json`", but the harness never reads that file; it pins whatever carrier it was handed (the pin *comparison* lives in the counter's `carrier_pin_ok`). Defensible as a system-level statement; misleading as a tool-level one.
- **O4** — `intended-doc.py`'s "Exercised 2026-10-26" receipts are fixture-scoped; the fixture commits are not lane objects. Correctly disclosed by wave-1; noted so a later reader does not try to reproduce those exact args in the lane.

## Verification gaps

- The `both-roots` arm of the absence sweep (PRESENT on `/home/vgpnk/Projects/shokuknow`) was not re-run — bounds forbid running tools against that tree; the recorded `.ufo/waves/round-39/l1/absence/summary.txt` (`rc=1` on both claims) is cited, not re-exercised.
- `gen-controls.py` kinds `c1-0`/`c2-0` remain unexercised (they replay the live counters), as wave-1 already disclosed.
- The r39 `c1-counter` selftest's "each on its clause" phrasing was verified by count (33 = 1 green + 32 red), not by auditing each case's targeted clause.
- REA-propagated exit codes through `round-38/c1-run.sh` before/after arms remain unenumerated (no REA run through that harness in this seat; wave-1 disclosed the same gap).

## Bounds, tooling, scratch

- Writes: this report + `artifacts/R39W2RegistryReview/` (10 evidence files) only. No VCS mutation (read-only git only; the self-tests built their own throwaway fixture repos in scratch). No writes outside the lane; the absence sweep and `git` reads over the fleet repo were read-only.
- No tools installed or upgraded (nothing needed); `sasquatch-v4be`, `sasquatch-v4be` pins, `unblob`, REA 6.5.0 untouched and used only via the harness/CLI as authorized.
- Scratch `S=/fast/scratch/hyaku/kaidoku-r39/R39W2RegistryReview` removed at the end. Residue outside my scratch, created by tool code that hardcodes shared scratch roots (same as wave-1 §9 disclosed): `/fast/scratch/hyaku/kaidoku-r37/selftest/green` (r37 counter's crashed selftest) and empty `kaidoku-r38/controls-*` dirs.
