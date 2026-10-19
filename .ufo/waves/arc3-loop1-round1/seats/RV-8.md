# RV-8 seat report — arc3-loop1-round1, chain c2, role reviewer

Seat: RV-8 | chain c2 | role reviewer
Task: consumer sweep — grep the repo for every invocation of the citation-drift
probe (SKILL.md recipes, gates docs, scripts); confirm flag compatibility and
that no consumer parses output in a way the guard breaks.

Status: **EX-16 landed mid-window** (worktree files written 2026-10-19
07:15:47–07:15:55 -03); the post-state is **measured on the final instrument**
(probe sha256 `e2665074a685ca65966f291f98b5e264b15c67827982811a24dc73b16497a36a`,
expected `ff47bfd6…`, table `738b3a56…`, HEAD `e845c2b5…`), not just on the
prototype proxy. One transient intermediate landing state was caught and is
flagged in §5.11.

## 1. Work performed (evidence pointers)

- Read the frozen claims and seat rules: `claims-frozen.md:40-54` (C2 claim),
  `:73-88` (seat discipline, patch-text rule).
- **Tracked-file census** for `citation-drift` (`git ls-files | xargs grep -l`):
  matches only `LOG.md` (1), `SCORECARD.md` (1), `SKILL.md` (1), `.ufo/` (220 —
  wave records). No other surface.
- **Scripts / hooks / CI:** none invoke the probe. Only tracked `*.sh` is
  `.ufo/waves/luna-round-5/receipts/census-pre.sh` (probe-free); `.git/hooks`
  has no non-samples; no Makefile / `.github` / CI config.
- **Gates docs / sibling instrument:** `.ufo/gates/` contains only
  `c1-census-v10.py` + `citation-drift/`; `grep -c citation-drift` in the census
  → 0 (no coupling).
- **Other prose surfaces probe-free:** `corpus/`, `PROVINCE.md`, `README.md`,
  `MINT.md`, `SHONEN.md`, `AGENTS.md`, `.ufo/continuation`, `.ufo/rounds`,
  `.ufo/interactive-sessions` → 0 matches.
- **Live consumer:** `SKILL.md:371` — the `citation-drift` registry row (recipe
  flags, `--selftest`, `--strict` semantics, pinned-values column).
- **Records (non-runnable):** `SCORECARD.md:815,853,873-874,907,918-919,925-926`
  (the frozen-run debt), `:990,:1054,:1267,:1297-1303`; `LOG.md:1079,1134-1135`.
- **Historical consumer shapes enumerated (r5–r10):** default recipe;
  custom `--table` + committed `--expected` (`E16.md:117-119` r10,
  `CR2.md:91` r10, `C4.md:153-159` r10, `E22.md:144-150` r10); frozen-rev runs
  (`P3.md:51-54`, `V1.md:194-196`, `C2.md:139-149` r10); parse patterns
  `tail -1` (`S1.md:61`, `CR2.md:44` r10, RV-6 harness), `grep -c "^CITATION_DRIFT:"`
  (RV-6 harness), verbatim verdict-line compare (`E58.md:329,:591` r6 — historical
  scratch harness).
- **Flag surface read:** original `:443-453`, landed instrument — same 7 flags
  (`--root --rev --table --expected --snapshot-dir --selftest --strict`); every
  consumer invocation uses only these.
- **Output surface read:** header/finding/verdict lines with the verdict LAST,
  selftest summary line, exit map 0/1/2 — unchanged by the landing (P1–P11).
- **Baseline consumer-shape runs** on copies (repo read-only): T1–T11, see
  `claims/c2/RV-8/baseline-transcripts.txt`. First T3/T5 attempts hit the `/tmp`
  user quota (Errno 122; RV-6/PL-2 recorded the same wall) and were redone
  cleanly under `/var/tmp/rv8`; the 0-byte partial table was discarded.
- **Post-landing runs on the final instrument**: P1–P12, transcripts in
  `claims/c2/RV-8/post-landed-transcripts.txt`; harness
  `claims/c2/RV-8/post-harness.sh`. Cross-checked against EX-16's own receipts
  (`claims/c2/EX-16/after-sha256.txt`, `after-selftest-13.txt`,
  `after-injections.txt`) — all match.
- **Cross-reads (chain convergence):** RV-6 `harness-pre.out` + `RV-6.md`
  (independent silent-rc-0 matrix; attack 6 argues digest enforcement on
  whatever table is loaded), RV-7 `verify-pre.log` (selftest case-table
  sensitivity), SC-4 `verify-changeset.sh` (§§4/5/9 tamper-via-`--table` attack
  probes), EX-25 `replay-driver.sh` (before/after replay incl. tampered-table
  injection), EX-20 `registry-row.patch.md` (the consumer-facing row text),
  EX-21 `logs/proto-probe.diff` (prototype guard, `table_sha256` top-level key,
  skip-on-unpinned), EX-24 `pin-mutability.md` (pin-mutability attacks; R2
  fail-closed recommendation; measured that fail-closed costs one condition and
  that deleting the pin key disables a skip-on-unpinned guard; T5: the pin is
  read from the effective `--expected`), PL-2 `frozen-run-guard.patch.md` (the
  chain plan EX-16 applied).
- **Supplementary proxy runs (EX-21 prototype — superseded by the landing):**
  X1–X12, transcripts in `claims/c2/RV-8/proxy-transcripts.txt`.
- Hygiene: my import-based diagnostic created
  `.ufo/gates/citation-drift/__pycache__/citation-drift-probe.cpython-314.pyc`
  (mtime 07:16) — removed at 07:18; the gate dir is back to the three tracked
  files. (`.ufo/gates/__pycache__/` — a census-module pyc from another seat —
  remains untracked; `.gitignore` does not cover it.)
- Artifacts: `claims/c2/RV-8/consumer-inventory.md`,
  `baseline-transcripts.txt`, `guard-compat-matrix.md`, `proxy-transcripts.txt`,
  `post-landed-transcripts.txt`, `post-harness.sh`.

## 2. Proposed changes

None by this seat (reviewer; no write scope beyond this report and its
artifacts). Consumer-facing notes for the parent, for integration:

1. **Registry-row patch reconciliation (EX-20's `registry-row.patch.md`).** The
   landed finding ids are `pointer_table_tampered` (digest mismatch),
   `pointer_table_unreadable` (absent table / absent expected), and
   `pointer_table_unpinned` (baseline without a pin). The patch text currently
   writes `table_tampered` and does not name the unpinned id — substitute the
   landed ids before applying. The case count (13) and the fail-closed unpinned
   clause match the landing.
2. **Intermediate-state hazard (§5.11).** The integration commit must capture
   the final worktree state (`e2665074…`), not the 07:15:47–55 intermediate
   (`53a94df2…`, red selftest).
3. **Pycache hygiene.** Keep untracked `__pycache__` dirs out of the
   integration commit (two have appeared under `.ufo/gates/` this wave; one is
   mine and was removed, one is a census-module pyc from another seat).

## 3. Before→after measurement relevant to the C2 claim

Before (HEAD `e845c2b`, gate sha256 probe `3067621a…`, table `738b3a56…`,
expected `4e28ba90…`), commands and outputs verbatim in
`claims/c2/RV-8/baseline-transcripts.txt`:

- T1 default recipe → `reported findings=0 exit=0` rc=0; T2 `--strict` → `clean
  findings=0 exit=0` rc=0.
- T3 selftest (TMPDIR redirected) → `CLEAN cases=11 passed=11 failed=0 exit=0` rc=0.
- T4 `tail -1` → the verdict line is the last stdout line (parse contract holds).
- T5/T5b valid-JSON emptied table + committed expected → `reported findings=0
  exit=0` / `--strict` `clean findings=0 exit=0` — **silent-green class**
  (independently reproduced by RV-6 cases B/C/F/G).
- T6 absent table → `could-not-evaluate … exit=2` (already the declared class).
- T9 frozen rev `679af5d…` → `reported findings=16 exit=0`, verdict line last.
- T10 byte-identical table copy + committed expected → rc=0.
- T11 foreign-CWD default-path invocation → rc=0.

**After (LANDED, final instrument — P1–P12 in
`claims/c2/RV-8/post-landed-transcripts.txt`):**

- P1 default recipe → `reported findings=0 exit=0`; P2 `--strict` → `clean
  findings=0 exit=0`.
- P3 `--selftest` → `CLEAN cases=13 passed=13 failed=0 exit=0`
  (`table_tampered` → `pointer_table_tampered`; `table_absent` →
  `pointer_table_unreadable`). Matches EX-16's `after-selftest-13.txt`.
- P4 byte-identical table copy + committed expected → rc=0.
- P5 modified (emptied) table + committed expected → `pointer_table_tampered …
  could-not-evaluate findings=1 exit=2` — the silent-green class closes in both
  modes.
- P6 absent table → `pointer_table_unreadable … exit=2`.
- P7 foreign-CWD default-path → rc=0; P8 flag surface unchanged (same 7 flags).
- P9 frozen rev `679af5d…` → `reported findings=16 exit=0`, verdict line last
  (drift reporting preserved; probe semantics 0/1/2 map intact).
- P10 isolated tree, tampered table at the default path → exit 2 (the claim's
  injection-fixture shape works).
- P11 unpinned expected (pin key deleted) + real table → `pointer_table_unpinned
  … could-not-evaluate findings=1 exit=2` — **fail-closed** (PL-2 shape).
- P12 custom expected pinning a custom table's digest → rc=0 — the re-pin
  escape hatch works; the pin is read from the effective `--expected`, not
  hardcoded.

Supplementary proxy (EX-21 prototype, superseded): X1–X12 in
`claims/c2/RV-8/proxy-transcripts.txt`; its one consumer-visible divergence from
the landed shape (X11: skip-on-unpinned, silent) is resolved — the landed
instrument is fail-closed (P11).

## 4. Consumer inventory summary (full detail in the artifact)

- Live consumers: `SKILL.md:371` only. No scripts, hooks, CI, Makefile, or
  sibling gate invoke the probe; `corpus/` and the prose surfaces are clean.
- Records reference it (`SCORECARD.md`, `LOG.md`) but contain no runnable
  commands and no parsers.
- Established consumer shapes from wave history: default recipe (+`--strict`,
  `--selftest`), custom `--table` + committed `--expected`, frozen-rev reruns,
  and the parse patterns `tail -1` / `grep -c "^CITATION_DRIFT:"` (plus one
  historical verbatim verdict-line compare in a scratch harness).

## 5. Attacks / refutations attempted, with verdicts

1. **"Some consumer passes a flag the guard could break"** — REFUTED. Every
   invocation site in the repo (registry row + 220 wave-record invocations) uses
   only the 7 argparse flags; no consumer passes `--snapshot-dir` (committed
   table has no `@` targets: `grep '"@' pointer-table.json` → 0). The landed
   guard adds no flag (P8) — flag-compatible by construction and by measurement.
2. **"Some consumer parses output in a way the guard breaks"** — REFUTED at
   format level. The load-bearing parse patterns are `tail -1` (verdict last)
   and `grep -c "^CITATION_DRIFT:"`; the landed guard adds at most one finding
   line and keeps the verdict line last with the unchanged
   `CITATION_DRIFT_VERDICT: <label> findings=N exit=M` format and the existing
   labels (P1/P2/P5/P6/P9/P10 measured). The behavior changes are intentional:
   tampered/unpinned table runs flip from silent rc0 to exit 2.
3. **"Path-scoped guard (check only the default table path) preserves the r10
   experiment shape"** — TRUE but REFUTED as the chain's design by consensus
   (RV-6 attack 6, SC-4 §§4/5/9, EX-25's injection, EX-20's row text, PL-2's
   plan). Accepted consequence, now landed: custom modified `--table` +
   committed `--expected` (the r10 landing/experiment recipes and this wave's
   attack harnesses) exits 2 by design (P5). **The escape hatch is verified on
   the landed instrument** (P12): a custom `expected.json` pinning the custom
   table's digest runs; the pin is not hardcoded (also EX-24 T5).
4. **"Byte-identical copies of the committed table keep working"** — CONFIRMED
   (T10 pre, P4 landed, rc=0 both). Archived-tree consumers (r5
   `E12.md:30-31`) rely on this.
5. **"The selftest survives the guard"** — CONFIRMED on the landed instrument
   (P3: 13/13 CLEAN; EX-16's receipt matches). The failure mode was real in the
   intermediate state: the 07:15:51 intermediate probe's selftest was
   `FAILED cases=13 passed=1 failed=12 exit=1` (fixture expecteds built without
   the pin → every case `pointer_table_unpinned`), exactly the harness-pin
   requirement EX-24 measured and EX-20 anticipated; the final state pins the
   fixture table per case (diff in `post-landed-transcripts.txt`).
6. **"Unpinned expected + real table"** — landed behavior: **fail-closed**
   (P11: `pointer_table_unpinned`, exit 2), matching PL-2's plan and EX-20's
   row text. EX-21's prototype instead skipped (X11: rc=0, silent — EX-24's T3
   attack); that shape was not landed. No live consumer passes a custom
   expected without a pin (RV-7's harness copies all three gate files).
7. **"Whitespace-only reformat of the committed table"** — under byte-digest
   pinning this is a mismatch until the pin is updated in the same commit
   (RV-6's after-harness probe). Documented consequence, not a defect.
8. **"The registry row cannot be edited safely"** — REFUTED. The table's
   `skill-registry-row` entry (`pointer-table.json:107-112`) is an unpinned
   anchor on the *sibling* row (`interactive-r1-recovery \| gate / kaidoku`),
   not on the citation-drift row text; the row edit (EX-20's patch) cannot break
   the table pin.
9. **`/tmp` quota wall** — CONFIRMED hazard this wave (Errno 122; my first T3
   selftest died at `git init`, rc 128; RV-6/PL-2 recorded the same). Consumers
   that run `--selftest` must redirect `TMPDIR` (r9/r10 precedent; RV-6/RV-7/
   SC-4/EX-25/EX-16 all did). Not a guard defect; wave-wide note.
10. **"EX-21's prototype is the design EX-16 will land"** — PARTIALLY: the
    landed probe (`e2665074…`) is PL-2's prototype (fail-closed, nested
    `pointer_table.sha256`), not EX-21's (`776cef6a…`, skip-on-unpinned,
    top-level `table_sha256`). The X-series proxy bound the landed behavior but
    the landed instrument was verified directly (P1–P12).
11. **Transient intermediate landing state (incident, resolved)** — my harness
    copied the gate dir at 07:15:51 and caught probe `53a94df2…` whose selftest
    was RED (1/13); the real probe was rewritten at 07:15:55 to the final
    `e2665074…` (selftest green). Evidence: sha256s, mtimes, and the
    intermediate-vs-final diff (missing fixture-pin lines) in
    `post-landed-transcripts.txt`. Consequence: the integration commit must take
    the final worktree state; a commit from the 07:15:47–55 window would ship a
    red selftest. Not a defect of the final instrument.
12. **Pycache hygiene** — my diagnostic import created
    `.ufo/gates/citation-drift/__pycache__/` (untracked, not gitignored);
    removed. A census-module pyc under `.ufo/gates/__pycache__/` (another seat)
    remains; flagged for the integrator.

## 6. Blockers / gaps

- EX-16's seat report had not appeared in `seats/` at write time (its
  after-receipts under `claims/c2/EX-16/` are present and match my readings).
  Its own claim statement is the parent's to reconcile; nothing in my consumer
  sweep depends on it.
- The registry-row patch (EX-20) is not applied and needs the token
  substitutions in §2.1 — the only consumer-facing text still out of step with
  the landed code.
- `/tmp` user quota (first T3/T5 attempts contaminated; redone under
  `/var/tmp/rv8`; partial files removed; `/var/tmp/rv8` scratch cleaned after
  this report, with the harness preserved at
  `claims/c2/RV-8/post-harness.sh`).

## Verdict (RV-8)

**Flag compatibility: compatible** — the landed guard keeps all 7 flags, adds
none, and requires none; every consumer invocation shape in the repo runs
unchanged (P1/P2/P7/P8).

**Output-parse compatibility: compatible** — verdict line stays last, format
and labels unchanged for existing cases; `tail -1` and
`grep "^CITATION_DRIFT:"` consumers unaffected (P1/P2/P9, and the guard runs in
P5/P6/P10/P11). The guard's classes surface as exit 2 with a verdict line
(declared could-not-evaluate), never as `reported findings=0 exit=0`.

**Consumer-behavior changes: three, all intended, declared, and verified on the
landed instrument:** (a) modified table (any path) vs the pinned digest → exit 2
(P5/P10); (b) absent table → exit 2 (P6, pre-existing); (c) unpinned expected →
exit 2 (P11). Byte-identical copies and custom-pinned expecteds still run
(P4/P12). No consumer in the repo parses the probe in a way the guard breaks,
and no invocation site uses a flag the guard touches. The single remaining
consumer-facing action is the EX-20 row-patch token reconciliation (§2.1).
