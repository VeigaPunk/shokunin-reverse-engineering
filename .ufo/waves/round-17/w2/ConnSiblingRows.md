# ConnSiblingRows — w2 falsification of the r17 sibling surface

Read-only attack of `da64646adcb19c1ede7537b799b8c7d283fe43da` (baseline
`b563c799…`, predictions frozen at `271167473d87ef710f07ecdd98caf0ce12091686`).
Axes named: **calibration** (does the produced artifact say what it can back?)
and **depth** (does the log-capture capability carry its own evidence into the
fleet?). No REA analyze/search/decompile, no Ghidra, no carrier execution; no
sibling or lane file edited; this report is the only write.

## 0. The direct question, answered first

**No sibling tool retains REA analyzer (Ghidra) logs** — w1's negative holds.
[observation]

- `find /home/vgpnk/Projects -name ghidra.log -not -path '*kaidoku*'` → no output;
  same for `script.log` (whole host, not just the 21 lanes).
- `grep -rn "ghidra\.log\|script\.log\|rea-ghidra" --include="*.md" --include="*.py"
  --include="*.sh" --include="*.json" /home/vgpnk/Projects/shokunin` outside
  kaidoku → only prose: `tameshi-shokunin/.ufo/waves/round-16/w1/Overlap2.md:179`
  (describes kaidoku's dirs), fleet-root `.ufo/reports/round-1/kaidoku.md:25,57`
  (kaidoku's own report), and `souji-shokunin/results/qrun-12.json:35`
  (`/tmp/s12-qrun-transcript.log`, unrelated).
- No sibling sets `TMPDIR` for REA (`grep -rn TMPDIR` outside kaidoku → only
  audio/fleet freeze tools), and no sibling PROVINCE claims log retention
  (`grep -rn -i "log capture\|capture the log\|run log\|session log" --include=PROVINCE.md`
  over all lanes → no output; `grep -ic "log capture" */PROVINCE.md` → every
  lane 0).
- Nearest sibling art, neither copying an analyzer log [observation]:
  `tameshi-shokunin/tools/repeat-control.py:17-40` retains N runs of an exact
  argv (`run-<k>.stdout/.stderr/.exit`, `command.txt` with tool sha256) — generic,
  not REA; `revenger-shokunin/corpus/live/runs/round-36/producer-receipt.json`
  retains REA `inspect-pe-resources` raw stdout (`raw_output_sha256`/`raw_output_bytes`),
  separated stderr (`stderr_sha256`) and `exit_code`; the `evidence_id` lives in
  the sibling `inspection.json`, not the receipt; earlier rounds (`round-35`)
  record `"stderr_separation": "not captured separately; output is combined"`.
  Revenger never invokes `rea … analyze`, so it never creates a Ghidra runtime
  root (`grep -rln " analyze " revenger-shokunin/corpus` → only round-1 prose).

So the **capability is uncontested at the fleet level**, and the r17 log binding
is genuinely new. The contested scope is method and provenance, not artifact
ownership; F1/F2 (the registry cannot show its own exercise) and F3 (an
unresolvable provenance pin) sit exactly on that seam.

## 1. Findings

### F1 — C1(b) is false at the produced rev: 11 unlabelled-variant rows, 0 labelled
*Severity: **medium** (claim-level; the round's own counting tool reports it).*

`python3 -I -B .ufo/waves/round-17/tools/invocation-audit.py --root …/kaidoku-shokunin --rev da64646…`
→
```
{'argv_records': 74, 'exercised_match': 6, 'labelled_unexercised': 0,
 'receipt_files': 20, 'receipt_glob_pathform_excluded': 71, 'rows': 17,
 'unlabelled_variant': 11, 'unreadable_receipts': 0}
```
All 11 are the new r17 rows plus `custody-pair`: `go-carrier-run`,
`go-log-extract`, `go-route-predict`, `go-route-compare`, `receipt-validate`,
`pins`, `temporal-sweep`, `invocation-audit`, `go-buildinfo-probe`,
`round17-structural-controls`, `custody-pair` — each `matched_receipt: None`.

Root cause is visible in the same output: the exercised argv that would match
them is not retained under a receipt path at this rev. The receipts under
`runs/*/receipt.json` carry only `steps = {analyze, inspect-go-binary}` (all 8,
checked), `grep -rl "log-extract" .ufo/waves/round-17/runs/` → no file, and the
row commands name entry points (`bash run-carriers.sh <LABEL>`) whose argv is
never recorded; `run-log.txt` holds start/end timestamps only.
C1(a) by contrast *is* met — `temporal-sweep.py --root … --rev da64646
--sites-rev b563c799…` → `{'corrected': 4, 'new_unqualified_at_rev': 0,
'sites': 4, 'unqualified': 0}`.

*Smallest fix:* per row, either retain the exercised argv (one `verification.json`
with an `argv` array for each step) or append the literal word `unexercised` to
the row. Acceptance is the same command returning `unlabelled_variant: 0`.

*In-flight, not counted as a finding:* `.ufo/waves/round-17/verify.py` (untracked
at read time, L1-authored; header line 10 `writes verification.json + verify/`)
records `argv` per command (`verify.py:71`) and writes `W/verification.json`
(`:173`). That is the vehicle for this fix; the finding stands for the committed
rev `da64646` and the acceptance applies to the integrated rev.

### F2 — Two rows cite a round-17 `verification.json` that does not exist
*Severity: **medium** (dangling evidence pointer in a registry row).*

`git ls-tree -r --name-only da64646 -- .ufo/waves/round-17 | grep verification.json`
→ no match (count 0). `SKILL.md:448` (citation-drift) and `:449` (custody-pair)
both name `.ufo/waves/round-17/verification.json` as the retained-argv receipt.
The audit matched citation-drift against `.ufo/waves/round-16/verification.json`
instead, and custody-pair against nothing. [observation]

*Smallest fix:* land the r17 `verification.json` (which also closes F1 for every
tool that `run-carriers.sh` invoked) or replace both pointers with the file that
actually holds the argv. The in-flight `verify.py:173` writes exactly that path,
so F2 should close with F1 if the row pointers then resolve.

### F3 — Unresolvable frozen-prediction SHA in two committed sites
*Severity: **medium** — it is the anchor C2's "prediction before observation" rests on.*

`git -C …/kaidoku-shokunin cat-file -t 2716747` → `fatal: Not a valid object name 2716747`.
Sites: `.ufo/waves/round-17/run-carriers.sh:2` ("predictions frozen at lane
commit 2716747") and `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:37`
("all eight carriers were committed at `2716747` before the first run"). The
lesson has it right: `corpus/lessons/round-17.md:26` cites the full
`271167473d87ef710f07ecdd98caf0ce12091686`. [observation]

Why this is a sibling finding, not a local typo: tameshi's r16 ruling requires
any citation of kaidoku's pattern to pin a resolvable revision —
"`b563c799…` (`claims.json:4`), never kaidoku HEAD, and never the in-flight r17
files as landed evidence" (`tameshi-shokunin/.ufo/waves/round-16/w1/Overlap2.md:146-149`).
A sibling that follows this knowledge entry's `recheck:` cannot resolve its own
provenance anchor.

*Smallest fix:* replace `2716747` with `271167473d87ef710f07ecdd98caf0ce12091686`
in both files (append-only correction line in the knowledge entry).

### F4 — `contract.md` contradicts the shipped tools it is supposed to describe
*Severity: **medium** (cross-seat hazard: wave-2/3 seats audit against this file).*

Two sections diverge from the tool at the same rev:

1. `contract.md:31-50` vs `.ufo/waves/round-17/tools/carrier-run.py:120-140,260-290,357-365`:
   contract has no `--pin`, no private `TMPDIR`, no `bound_sessions`/
   `unbound_sessions`, and says exit 2 only "if analyze exit != 0"; the tool
   redirects the session root into `/tmp/kr17-rea-*`, binds each log by
   `Using log file:` + `IMPORTING: …target-<carrier sha[:12]>.bin`, and exits 2
   unless exactly one session binds. `SKILL.md:532` already documents the
   as-built behavior, so the registry and the contract disagree.
2. `contract.md:90-97` vs `temporal-sweep.py:61-62,160-172`: contract says a site
   is corrected by a line containing `R16-PROVENANCE` **and the path**; the tool
   also requires the exact `file:line` token and the phrase
   `temporal stability not evidenced` (matched case-insensitively against
   `line.lower()`). A seat writing a correction to the contract's spec produces
   a line the tool counts as uncorrected. `SKILL.md:538` documents the tool
   correctly.

This is why w1's S3 reads as an open capability gap: the contract text still
describes the pre-fix copy-every-new-dir behavior, while the tool committed at
the same rev (`2711674`, `carrier-run.py` already contains `bound_sessions`,
`target_ok`, `kr17-rea`) had closed it. Eight receipts confirm the closure:
`bound_sessions=1`, `unbound_sessions=0` in all 8. [observation]

*Smallest fix:* one dated "as-built correction" block per divergent section in
`contract.md` pointing at the tool lines; do not rewrite history.

### F5 — "No mid-run check differed" has no retained evidence
*Severity: **low-medium** — same defect class as R16-PROVENANCE, in the round that claims to discharge it.*

`corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:26-29` says the 146
paths "were hashed before, every 30 s during, and after each session … no
mid-run check differed." The check exists
(`carrier-run.py:422-433`) but records only a mismatch:
`rec["pins_changed_during_run"]` on inequality, nothing otherwise. No receipt
carries a mid-check count or timestamp:
`python3 -c "… sorted(d['steps']) …"` over all 8 `runs/*/receipt.json` →
no `pins_mid`/`mid_pin_checks` key in any, and `grep -rl "mid_pin\|pins_changed_during_run" runs/`
→ no file. The run durations (e.g. `run-log.txt`: 10:47:42→10:49:24) imply checks
almost certainly ran, but the receipt cannot show that they did. [observation;
the inference that checks ran is marked as inference]

*Smallest fix:* `rec["mid_pin_checks"] = n` (and `last_mid_utc`) incremented in
the same branch, plus one selftest assertion; then the sentence cites a count.

### F6 — Three contract tools have no registry row at all
*Severity: **low-medium** — makes C1(b)'s `M → 0` satisfiable by omission.*

`python3 -B -` comparison of `contract.md` `## W/tools/<name>` headings against
`SKILL.md` rows whose 2nd cell matches `(probe|gate|tool) / kaidoku` →
`contract tools with NO matching registry row: ['retain.py', 'carrier-census.py', 'measure.py']`.
`retain.py` is load-bearing for `receipt-validate.py`'s `retain` shape
(`receipt-validate.py:9,14`) and `carrier-census.py` produced a retained,
argv-carrying artifact (`w1/carrier-census.json`, `inspect.argv`). Because
`invocation-audit.py` derives its universe from SKILL.md rows only
(`invocation-audit.py:8-9,275-299`), a missing row is invisible to the count.

`retain.py` is also the one tool that duplicates tameshi-owned craft
(`tools/repeat-control.py`); registering it with that pointer prevents a silent
second-lane method claim.

*Smallest fix:* add the three rows; label them `unexercised` unless a retained
argv exists (`retain.py` currently has a seat report, `w1/RetainTool.md`, but no
receipt).

### F7 — Eight private session parents left under `/tmp`, nothing removes them
*Severity: **low** (host hygiene; no lane owns `/tmp`).*

`ls -d /tmp/kr17-rea-* | wc -l` → `8`; each holds a `node-compile-cache`
directory (`ls /tmp/kr17-rea-1cqz92us` → `node-compile-cache`). Receipts record
`session_parent_leftovers: ["node-compile-cache"]` but no removal happens.
`carrier-run.py:263` creates the root with `tempfile.mkdtemp`; only REA's own
`rea-ghidra-*` child is deleted on close. souji's province excludes live lane
work (`souji-shokunin/PROVINCE.md:34-36`), so these are unreferenced residue.

*Smallest fix:* after the post-pin snapshot, `shutil.rmtree(private_root)` guarded
by an exact `kr17-rea-` prefix check, and record `session_parent_removed: true`
in the receipt.

## 2. Contested scope (reported, not resolved)

| id | parties | state at da64646 |
|---|---|---|
| S1 shipped-artifact RE | revenger `PROVINCE.md:3-7` vs kaidoku `PROVINCE.md:3-4` | unchanged; tsukuroi still refuses to arbitrate (`PROVINCE.md:51,79-81`). My re-scan found **no new Go claim** in revenger (`grep -in "go binary\|golang\|go 1\." revenger-shokunin/PROVINCE.md` → 0), so the r17 Go ground is still kaidoku-only. |
| S2 method craft | tameshi `PROVINCE.md:10-12` owns "kaidoku's audit-lane pattern"; `Overlap2.md:146-149` gates citations on a resolvable baseline, `:166` allows kaidoku r17 as a second lane **after it commits** | the commit condition is now met (tools at `2711674`, corrections at `da64646`); the baseline condition is violated by F3. No sibling currently cites the r17 rows (`grep -rn "round-17/tools\|go-carrier-run\|temporal-sweep\|invocation-audit\|go-log-extract"` outside kaidoku → 0 hits), so the contest is latent. |
| S3 log-capture capability | none vs kaidoku | uncontested. A future capability row may claim *REA Ghidra session-log capture*, not generic argv/stdout retention, which tameshi (`repeat-control.py`) and revenger (`producer-receipt.json`) already hold. |

Bounded no-findings [observation]:
- No sibling `SKILL.md` inventories the r17 rows; revenger still has no
  `SKILL.md` at all (18 of 21 lanes), matching w1's inventory.
- w1's sibling citations resolve at their stated lines: revenger `:3-7,:15`,
  tsukuroi `:26,:51,:79-81`, tameshi `:10-12,:34`, mori `:22,:54`, souji
  `:4,:34-36,:40-41`, tabi `:15`, game-dev-3d `:38-41,:78`, and kagi `:63`
  (the 1Password quote is at the end of that long line). No w1 citation drift.
- A live `npm exec rea-agents@6.5.0 mcp` (PID 3221) still exists and no
  `/tmp/rea-ghidra-*` root is present; the private-`TMPDIR` design makes it moot
  for attribution, which the 8 receipts' `unbound_sessions: []` corroborate.
- `SCORECARD.md` at this rev contains no `retained REA Ghidra-session log` text
  (`git show da64646:SCORECARD.md | grep -i "retained REA"` → 0), so
  `measure.py:46`'s `CAPABILITY_TEXT` predicate is 0/1 before integration. This
  is ConnScorecardCapability's seam; recorded here only so a sibling does not
  read an absent row as a withdrawn claim.

## 3. One bounded move (synthesis)

**Make the registry the fleet-visible index of the capability, and make the
contract describe the shipped tool** — a single dated correction pass, no
behavior change, no sibling write:

1. Append an "as-built (r17)" block to `contract.md` §carrier-run and
   §temporal-sweep naming `--pin`, the private `TMPDIR`, the log binding, the
   one-bound-session exit rule, and the exact `file:line` + phrase correction
   predicate, each pointing at the tool lines.
2. Land the three missing rows (`retain.py`, `carrier-census.py`, `measure.py`),
   labelled `unexercised` where no retained argv exists, with one pointer to
   `tameshi/tools/repeat-control.py` on the `retain` row.
3. Land `.ufo/waves/round-17/verification.json` carrying the `argv` arrays that
   `run-carriers.sh` already executed, so the ten r17 rows classify
   `exercised_match` instead of `unlabelled_variant`.
4. Correct `2716747` → `271167473d…` in the two sites (F3).

Affected axes. **Calibration** improves: the audit's own measure goes
`unlabelled_variant 11 → 0`, the contract stops generating phantom gaps, and the
frozen-prediction anchor resolves. **Depth** improves: a sibling can find and
re-run the capability from one registry row, and the retention craft is
attributed instead of re-claimed. No axis is harmed: no carrier is added or run,
no target is executed, no sibling repo is touched, and no claim is upgraded.

## 4. Risks, stated

- Labelling rows `unexercised` is honest but reads as weaker than the runs
  performed; item 3 is what restores `exercised_match`, so land 3 with 2.
- `retain.py`/`pins.py` instantiate craft tameshi owns; the row must say
  "lane-local instance" or it becomes a second-lane method claim that tameshi's
  admission rule forbids without two-lane evidence.
- The contract correction must not weaken the pins limitation ("identical bytes
  at two instants, never continuity") while adding the as-built detail.
- F5's count field must be additive: `receipt-validate.py` classifies by shape
  (`receipt-validate.py:240-253`), so a new key must not enter its required set
  before the 8 existing receipts are re-validated.

## 5. Verification of the move

- `python3 -I -B …/tools/invocation-audit.py --root …/kaidoku-shokunin --rev <integrated>` →
  `unlabelled_variant: 0`, `labelled_unexercised` or `exercised_match` covering
  all 17 rows.
- `python3 -I -B …/tools/temporal-sweep.py --root … --rev <integrated> --sites-rev b563c799…`
  → still `sites 4 / corrected 4 / unqualified 0` (no regression).
- `python3 -I -B …/tools/receipt-validate.py runs/*/receipt.json` → exit 0 on all
  eight after any additive field.
- `git cat-file -t 271167473d87ef710f07ecdd98caf0ce12091686` → `commit`, and
  `grep -c 2716747` over the two files → 0.

No sibling file was edited and no arbitration is proposed beyond reporting S1–S3
to L1 and, through L1, the integrator. Evidence above is observation from
read-only reads of lane and sibling files and of round-17 tool output on Git
objects; the "checks almost certainly ran" reading in F5 is inference.
