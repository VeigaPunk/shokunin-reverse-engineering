# CriticSeparability — R31-C1 / R31-C2 separability and the lowest-axis basis

Seat: wave 1 critic (leaf). Lane `kaidoku-shokunin`; review target is the freeze commit
`35ba7c522dba55f9be27eb161d4254eacaa24330` (lane base `c369242f`); the lane HEAD moved to
`f368a101277ab9c4ddff428db739a734efb5c280` while this seat worked (L1 integration). Verified
read-only: at `f368a10` the six pinned blobs are identical to the freeze blobs
(`git rev-parse 35ba7c5:<p>` == `HEAD:<p>` for `claims.json`, both TSVs and all three counters).
All runs in `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CriticSeparability/` (artifacts §7).
Report time 2026-10-23T04:20:15Z.

## 0. Verdicts

| Attack | Verdict |
|---|---|
| **S1 Cross-dependence of the two counters' deliverables** | **holds (separable)** — neither counter reads the other claim's envelopes, entry or doc rows; each prints a target-shaped line with the other's work absent (§3) |
| **S2 The exact shared input** | `corpus/evidence/round-31/c1/carriers.tsv` (read by C2, added by the freeze commit, not a C1 result), the declared oracle, and three undeclared common-mode inputs (§4.2) |
| **S3 Frozen inputs/instruments pinned inside the counters** | **fails as a counter property** — one post-freeze commit moves both verdicts silently; repaired outside the counters by the landed `tools/round-31/freeze-integrity.py` (§4.3), which I re-ran red/green |
| **S4 C2 `committed_check` imposes an entry-id gate not in the frozen predicate** | **fails (fixable, not a tradeoff)** — exact envelope + S092 entry without the id is rejected (§4.4) |
| **S5 `lowest_axis`** | **holds** — three owned axes tied at 10.0, none retired; the cited range carries the tie but not the retirement clause (§5) |
| **S6 Freeze-second tie in both `committed_check`s** | latent, not triggered; evidence commits must land ≥1 s after `1792728307` (§4.5) |

## 1. Method

* Sandbox clones only (contract form): `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q
  <LANE> <seat>/clone && … checkout -q -B ctl 35ba7c5…`; control commits with
  `git -C <clone> -c user.name=ctl -c user.email=ctl@local commit`.
  `clone` = freeze; `clone2` = freeze + simulated C1 work (`f00dca2b`); `clone3` = freeze +
  simulated C2 work (`a171d12d`); `clone4` = freeze + rewritten `predictions.tsv` (`2dbda62f`);
  `clone5` = freeze + edited `sqlite_oracle.py` (`9b2a5110`). All five clean, HEAD recorded.
* Counters were run only in `--selftest` mode and at the freeze clone (contract allowance). The
  truncated states were probed by importing the frozen modules and calling the exact gate
  functions `measure()` calls (pins, `entry_ok`, `province_ok`, `skill_ok`, `committed_check`);
  no REA was run on `clone2..5`. Envelope bytes in `clone2/clone3` are **simulated** JSON — the
  cross-dependence question is path-level, and the trace (§2) shows neither counter opens the
  other's envelope directory.
* Full path lists were obtained by tracing the canonical freeze runs with
  `strace -f -qq -s 240 -e trace=%file` (execve argv + every file argument), not by reading code
  alone; the code was then used to attribute each path to a line.

## 2. Path lists at `--root <freeze clone> --rev HEAD`

Trace evidence: `c1b.trace` (511,924 lines), `c2b.trace` (600,740), summarised in `c1.exact.txt`
/ `c2.exact.txt`.

### 2.1 C1 (`c1-sqlite-positive.py`)

Lane paths at `--rev` (all via `git show <rev>:<path>` / `git log <rev> --diff-filter=A -- <path>`):

| Path | Read by |
|---|---|
| `corpus/evidence/round-31/c1/carriers.tsv` | `measure:146` (`show`), and the worktree copy at `:150` compared to it |
| `corpus/evidence/round-31/c1/envelopes/<id>.json` ×12 (`proj-341, proj-350, proj-361, proj-370, proj-371, chinook, chinook-autoinc, gpkg-curve, gpkg-curvepolygon, gpkg-line-zm, gpkg-multisurface, gpkg-test-gpkg-nulls`) | `committed_check:103`; `git log` on each only if the blob exists (absent at freeze) |
| `corpus/knowledge/2026-10-23-r31-sqlite-positive.md` | `measure:169` |
| `PROVINCE.md` | `measure:198` |
| `.ufo/waves/round-31/claims.json` | path only, in `git log --diff-filter=A --format=%ct` (`measure:166`); **no content read** |

Worktree (not `--rev`): `<root>/corpus/evidence/round-31/c1/carriers.tsv`; `tools/round-31/c1-sqlite-positive.py`;
`tools/round-31/sqlite_oracle.py` (`importlib` by `HERE`, `:45`), i.e. the oracle is loaded from the
executing tree, never from a revision.

Scratch: all 12 carriers
`/fast/scratch/hyaku/kaidoku-r31/carriers/{proj-341.db,proj-350.db,proj-361.db,proj-370.db,proj-371.db,
chinook.sqlite,chinook-autoinc.sqlite,gpkg-curve.gpkg,gpkg-curvepolygon.gpkg,gpkg-line-zm.gpkg,
gpkg-multisurface.gpkg,gpkg-test-gpkg-nulls.gpkg}` (pin `sha256_file`, oracle parse, REA), each
carrier's `-wal` and `-journal` (oracle `lexists(path+"-wal")` and REA snapshot `statx`), the REA pin
`~/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/package.json` and the npx cache/dist, and
`TMPDIR` (node compile cache). **No c2 path, no `SKILL.md`, no `predictions.tsv`, no mutant.**

### 2.2 C2 (`c2-sqlite-refusals.py`)

Lane paths at `--rev`:

| Path | Read by |
|---|---|
| `corpus/evidence/round-31/c2/predictions.tsv` | `measure:279` (`show`) + worktree compare `:283` |
| **`corpus/evidence/round-31/c1/carriers.tsv`** | `carrier_sha:68` — the 3 carrier pins and the base pin |
| `.ufo/waves/round-31/claims.json` | `measure:302` (**content**: `mutant_sha256`, `mutant_sibling_sha256`) and `:328` (`git log` add time) |
| `corpus/evidence/round-31/c2/envelopes/<id>.json` ×23 | `committed_check:234` |
| `corpus/knowledge/2026-10-23-r31-sqlite-refusals.md` | `:331`, `entry_ok:252` |
| `SKILL.md` | `skill_ok:262` |

Worktree: `tools/round-31/c2-sqlite-refusals.py`, `tools/round-31/sqlite_oracle.py` (`:46`),
`corpus/evidence/round-31/c2/predictions.tsv`.

Scratch: **3** carriers — `carriers/chinook.sqlite` (base pin `base_of`, `:75`, `:295`; 7 requests),
`carriers/proj-371.db` (1), `carriers/gpkg-curve.gpkg` (2) — and 13 mutants under
`/fast/scratch/hyaku/kaidoku-r31/mutants/<id>/db.sqlite` (`m-missing, m-enotdir/file, m-not-sqlite,
m-bad-pagesize, m-journal-hot, m-journal-short, m-journal-empty, m-journal-zero28, m-journal-symlink,
m-db-symlink, m-directory, m-over-256mib, m-wal-over`) plus their `-journal`/`-wal` siblings
(`statx`/`readlink`); the REA pin package.json, npx cache, `TMPDIR`.
**No `PROVINCE.md`, no c1 entry, no `c1/envelopes`.**

## 3. The two truncated states, and what each counter prints

Built in `clone2` (only C1's files) and `clone3` (only C2's files): envelopes under the claim's own
`envelopes/`, the claim's entry (S096 resp. S092), and the claim's doc surface (PROVINCE `## Core`
row resp. SKILL verb+entry+23 rows). Probe output `probe.out` (exit 0):

| Gate in the OTHER-claim-absent state | clone2 (C1 work present) → C2 | clone3 (C2 work present) → C1 |
|---|---|---|
| pins reach the per-row loop | base+3 carrier pins ok, mutant pins ok | 12/12 carriers ok, list worktree==rev |
| own entry gate | `entry_ok=0 (entry absent)` | `entry_ok=0 (entry absent)` |
| own doc gate | `skill_ok=0 (SKILL names neither the verb nor the entry)` | `province_ok=0 (no PROVINCE table row names the verb and the entry)` |
| committed envelopes | 23/23 `committed envelope absent` | 12/12 `committed envelope absent` |
| **would print** | `requests=23 matches=0 target=23 entry_ok=0 (entry absent) skill_ok=0 (SKILL names neither the verb nor the entry)`, exit 1 | `carriers=12 pass=0 target=12 entry_ok=0 (entry absent) province_ok=0 (no PROVINCE table row names the verb and the entry)`, exit 1 |
| other claim's files visible at rev | 12 c1 envelopes present, C2 never opens them | 23 c2 envelopes present, C1 never opens them |

`matches=0` / `pass=0` (not a judge failure) is the right reading: in the canonical freeze run every
row printed the **committed-gate** reason, which is only reached when `judge()` already returned
`P1-pass`/`P2-match` — so the live half passes on the identical carrier/mutant/prediction inputs and
only the absent committed envelope and doc rows hold the counter back. Both freeze runs were
byte-identical across two invocations (`diff c1.freeze.out c1b.out` empty; same for C2), so the live
half is stable for these inputs.

**S1 verdict: separable.** The only file C2 reads from C1's namespace is `carriers.tsv`, which
`git log --diff-filter=A` dates to the freeze commit itself (`1792728307`), i.e. a frozen pre-data
input, not a C1 result. C1 reads nothing from C2's namespace at all (grep and trace agree).

## 4. Findings

### 4.1 `claims.json` separability sentence — accurate where it is specific
Verified: C2's distinct carrier paths are exactly the three named
(`chinook.sqlite`, `proj-371.db`, `gpkg-curve.gpkg`; probe field `c2_pin_distinct_carrier_paths`),
and the base carrier is one of them. The sentence is silent about three further shared inputs
(§4.2). No false claim, incomplete enumeration.

### 4.2 The complete shared-input set (observation)

| Shared input | C1 | C2 |
|---|---|---|
| `corpus/evidence/round-31/c1/carriers.tsv` | 12-carrier list + worktree equality | 3 carrier sha pins + base pin |
| `tools/round-31/sqlite_oracle.py` (worktree) | `expected_report` for 12 carriers | `expected_report`/`album_rows` for 3 acceptances |
| `.ufo/waves/round-31/claims.json` | `git log` add-time only | mutant pins (content) + add-time |
| REA pin `…/rea-agents/package.json` + npx cache | version check, recorded sha | same |
| scratch carrier bytes | all 12 | 3 of the 12 (+13 mutants) |

### 4.3 Common-mode frozen inputs are unpinned inside the counters — and now gated outside them

Counterexample, constructed and measured (no REA):
`clone4` commit `2dbda62f` rewrites one `code_pointer` cell of `predictions.tsv`. C2's only guard is
`pred_text != open(root/PRED).read()` (`:283`); at `--rev HEAD` both sides are the rewritten bytes, so
the guard is silent (`rev_eq_worktree: true`), `first_added` is still the freeze second, and
`claims.frozen_inputs["…/predictions.tsv"] = acac45e3…` is read by no counter (`grep frozen_inputs
tools/round-31/*.py` → none) while the rev bytes hash to `6f38666b…`.
`clone5` commit `9b2a5110` appends one line to `sqlite_oracle.py`: the counter's `load_oracle()`
returns the edited module (marker present), `rev == worktree` again, and
`claims.instruments["tools/round-31/sqlite_oracle.py"] = aefd8639…` is unread while the rev bytes
hash to `d90c0ce7…`. One commit therefore moves **both** claims' verdicts with no `PIN` line; this is
declared shared (oracle) but breaks causal independence in the strong sense for predictions/carriers.

Repair status: the L1 landed `tools/round-31/freeze-integrity.py` after the freeze (docstring names
M31-2 and this exact control). Re-ran it read-only from the lane tree against my clones:
`--root clone` → `freeze-integrity: CLEAN pins=5 freeze=35ba7c522dba rev=HEAD`, exit 0;
`--root clone4` → `FAIL	corpus/evidence/round-31/c2/predictions.tsv	sha=6f38666b1794	commits_after_freeze=2dbda62f`,
`freeze-integrity: FAIL pins=5 changed=1`, exit 1; `--root clone5` → `FAIL	tools/round-31/sqlite_oracle.py	sha=d90c0ce76770	commits_after_freeze=9b2a5110`,
exit 1. So the defect is real, already repaired, and the repair is **outside** the frozen counters —
the round must run the gate (a counter-only reading of the kill rule would miss it).

### 4.4 C2's `committed_check` adds a gate the frozen predicate does not state

`if rid not in entry_text: return False, "entry does not name %s" % rid` (`:246-247`). The frozen
P2 predicate requires only that the committed envelope equal the live envelope but `meta`; the
`doc_gates` for C2 name `entry_ok` (cites S092) and `skill_ok` (SKILL rows), not entry→id. Probe on
`clone3`: a byte-exact committed envelope plus an entry citing S092 but not the id returns
`(False, 'entry does not name m-wal-over')`. By contrast C1's analogous clause is declared
("the round-31 entry names that evidence_id"). Smallest safe correction: the C2 entry must list all
23 request ids (the counter is frozen; do not relax it retroactively), and the predicate sentence
should record the clause if this claim family is ever re-frozen. Not a tradeoff the canonical judge
must reject — the claim can still verify — but an undeclared condition on the entry.

### 4.5 Latent freeze-second tie

Both `committed_check`s reject `added <= freeze_ct` in whole committer seconds
(`c1:107`, `c2:238`). An evidence commit whose committer second equals `1792728307` would print
"not added after the freeze". Not triggered here (state commits are `1792729008…`). Observation for
the L1: commit evidence ≥1 s after the freeze commit.

### 4.6 Incident (disclosed)

A builder script of mine omitted `-C <clone>` on one git call, so
`git -c user.name=ctl -c user.email=ctl@local commit -q …` ran with cwd `/home/vgpnk/Projects/shokunin`
(the fleet repo). It created **no commit**: output `no changes added to commit` / exit 1, fleet HEAD
before and after `f0dadee386559ce4a80b9655c9a088c375f4b510` ("hyaku phase-4: kotodama r59 closure,
parked"), reflog top unchanged (`HEAD@{0}: export from jj`). The fleet `.git/index` mtime advanced to
2026-10-23T04:16:24Z (git's stat-cache refresh; no staged entry was added — the commit reported no
changes). No lane file, ref, worktree or jj state was touched. The bug was fixed in
`build_states.py` (`-C d` plus `cwd=S`) before `clone2..5` were built.

## 5. Lowest-axis verdict — **holds**

At `c369242f` (`git show c369242f:SCORECARD.md`):

* `:21-25` is the owned-axes table: `coverage 9.72 → 10.0` (`:23`), `depth 10 → 10` (`:24`),
  `calibration 0 → 10` (`:25`). Three-way tie at the maximum, 10.0.
* The lane owns exactly those three: `:376-377` "NOT a lane-owned proxy — the owned set is
  coverage/depth/calibration"; `:629` "the three finite owned proxies (coverage/depth/calibration)".
* No retirement: `:155-156` "**retired:** none"; `:325` "Retired: none."; `:629-631` saturation line
  10.0 with no retirement row. `:31` "A perfect finite proxy retires no domain axis".
* Obligation is live: `AXES.md:33-39` "At least one claim works the lane's lowest-scoring
  non-retired axis". The capability table's last first-working round is **27** (`SCORECARD:623`
  "cross-pin evidence-ID attribution", last cell `round 27`); with window N=10 (`:632`) rounds
  28–37 are inside the window, so round 31 is inside it and the stagnation nudge (`AXES.md:66-73`)
  does **not** waive the obligation. The tie statement is therefore load-bearing. `[INFERENCE]` on
  the window arithmetic; the cells above are observations.
* Under `argmin`, all three tied axes attain the minimum, so coverage (C1) and depth (C2) each
  satisfy "a lowest-scoring non-retired axis". The lane's own record reads ties the same way:
  `:1343-1344` "coverage is the owned axis (three-way tie, most-falsifiable-next-claim tie-break
  per luna-round-2 precedent)" and `:2228` "The tied-lowest calibration obligation". The field's
  claim that "on a tie every axis is a lowest axis" is the standard argmin reading and agrees with
  the outside lesson that raised the defect (`corpus/lessons/round-30-verifier-spotcheck.md:148`:
  "The lowest-axis basis is unstated (coverage, depth and calibration are all tied at 10)").

**Defect (citation scope, fixable):** the parenthesised range `SCORECARD.md:21-25` supports the tie
but does not contain the "none retired" clause; that clause lives at `:144-156` / `:325` /
`:629-643`. The statement is true, the citation is short by one range. Smallest safe correction:
cite `:21-25` for the tie and `:155-156` (or `:144-156`) for the retirement state in the round's
report/SCORECARD section — `claims.json` is frozen and must not be edited.

## 6. Commands, exit codes, UTC times

| # | Command (cwd = seat dir unless noted) | Exit | Time (UTC) |
|---|---|---|---|
| 1 | `python3 -I -B tools/round-31/c1-sqlite-positive.py --selftest` (clone @35ba7c5) | 0 (`selftest cases=14 failures=0`) | 04:11–04:12Z |
| 2 | `python3 -I -B tools/round-31/c2-sqlite-refusals.py --selftest` | 0 (`cases=12 failures=0`) | 04:11–04:12Z |
| 3 | `TMPDIR=$S/tmp timeout 900 strace -f -qq -e trace=%file -o c1.trace python3 -I -B …/c1-sqlite-positive.py --root clone --rev HEAD` | 1 | out 04:12:47Z |
| 4 | same for `c2-sqlite-refusals.py` → `c2.trace` | 1 | out 04:13:40Z |
| 5 | repeats with `-s 240` → `c1b.trace`/`c2b.trace` (byte-identical stdout) | 1, 1 | 04:15:09Z / 04:15:42Z |
| 6 | `python3 -I -B probe_states.py` (gates in clone2/clone3, no REA) | 0 | 04:17:11Z |
| 7 | `python3 -I -B <lane>/tools/round-31/freeze-integrity.py --root clone{,4,5} --round 31 --rev HEAD` | 0 / 1 / 1 | 04:18–04:19Z |
| 8 | clone builds (`git clone` + `checkout -B ctl 35ba7c5` + control commits) | 0 | 04:16–04:18Z |

Full counter stdout at the freeze (both runs): 12 lines `<id>\tP1-fail\tcommitted envelope absent`
+ `carriers=12 pass=0 target=12 entry_ok=0 (entry absent) province_ok=0 (no PROVINCE table row names
the verb and the entry)`; 23 lines `<id>\tP2-miss\tcommitted envelope absent` +
`requests=23 matches=0 target=23 entry_ok=0 (entry absent) skill_ok=0 (SKILL names neither the verb
nor the entry)`. Exit 1 both — the target line is **not** met at the freeze, as expected.

## 7. Artifact manifest (all under `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CriticSeparability/`)

| Path | sha256 |
|---|---|
| `c1.freeze.out` | `a76e62b9e646e5455d8c0376f95342632fd47d05c6750c833f268a7a21d9507e` |
| `c1.freeze.err` (empty) | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `c2.freeze.out` | `cb6ff04bcb71f78fa354dd54fe1503491d6b7c63ed932a81bae2312df17ad6b0` |
| `c2.freeze.err` (empty) | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `c1b.out` | `a76e62b9e646e5455d8c0376f95342632fd47d05c6750c833f268a7a21d9507e` |
| `c2b.out` | `cb6ff04bcb71f78fa354dd54fe1503491d6b7c63ed932a81bae2312df17ad6b0` |
| `c1.trace` (52,149,502 B) | `2d617140684974485ae2b14382677d40912c37f73e48c5971ec33c588308b0ed` |
| `c2.trace` (81,019,439 B) | `c931350b1e3ef821c8ebcbeb74eb2e00d6d43d4fdf44ecaea6e8afaf5d1fafca` |
| `c1b.trace` (52,528,398 B) | `3048d90314092f67528343858fb7e89fb53168f0817183b637e88516043f7d04` |
| `c2b.trace` (80,431,562 B) | `c3520782c040e9344aca1bc1e68999353fda473d3cfd085c95a65cf6a5b60ac9` |
| `c1.exact.txt` (exec argv + non-temp paths) | `19bb020adb9b546dc500720b60c6e12d415150cc83230232602e1e6371ef51bd` |
| `c2.exact.txt` | `03b7f1bea86136af04249821995331c5d4bdeec8417232ba5ff3815a5563506c` |
| `c1.paths2.txt` | `1a83750103a5085a60a0588e49b179836058f10754b90c3a275b15575b66c9f9` |
| `c2.paths2.txt` | `c78bc376b8b6fd7ceae9b0f3e8c6022ee263d5779d27e774cb98635a34d04894` |
| `probe.out` | `793f035173421fbdf8fbc1e13002c77a458b334dd8aa8e0135376de7771caf61` |
| `probe_states.py` | `331f0a28c44233f0315f56c6f7ce3f188cbcf7c02577f26b7c30c0969963f5b1` |
| `build_states.py` | `5516bc0fc7d5cb6363f4f4074b1d5e1d4a225cb6cf7fee71817c2cacc949dc7b` |
| `extract_paths.py` | `98802446ad7be792013d553b7030d35d164be191c0013bd20e68341976de73b7` |
| `extract2.py` | `0c3209a29f42ed98d59937b9cd5f5545b0ee64e7266689c79c0f0edb2f39058c` |

Clones (sandbox, clean): `clone` @ `35ba7c5`, `clone2` @ `f00dca2b01cb63078d051550a54badd93b17cc2f`,
`clone3` @ `a171d12dad7b7becc288868a402b7ef6b0e766e2`,
`clone4` @ `2dbda62fb422a2b096427203a758f85e81aae934`,
`clone5` @ `9b2a5110e0baedc6e09bac2a38d17c472a532343`.
No installs or updates were made (REA 6.5.0 already cached; `package.json` version 6.5.0,
sha256 `a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c`, matching `claims.rea_pin`).
