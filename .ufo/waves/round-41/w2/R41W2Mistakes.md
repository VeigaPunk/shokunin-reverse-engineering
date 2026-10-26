# R41W2Mistakes — round-41 landing mistakes mine

**Verdict: DEFECTS FOUND.** Attacked the four round-41 landing mistakes — (a) V4 `after.json`
silently missing from the data commit (1 MiB snapshot skip), (b) C2 declared-tuple key mismatch
uncaught pre-freeze, (c) `c1-run.sh` argv-size failure on the V4 receipt, (d) seat R41C1Counter
rewriting artifacts after the freeze. All four confirmed from primary evidence; each ships a
red/green check script in `w2/artifacts/R41W2Mistakes/`. The C1 claim verdict (MET at
`e9a24d07`) and the C2 stop (NOT MET, honest stop) are consistent with the retained score
receipts; they are not re-scored here.

All commands ran with cwd = the lane root
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin` unless stated. No tools were installed or
updated; no vendor bytes were fetched or touched; nothing outside the seat's report/artifacts
paths was written.

---

## (a) M41-3 — V4 `after.json` (2.8 MB) skipped by the directory commit's 1 MiB rule

- **Class:** evidence silently left out of a commit — a commit helper's size-based skip, not a
  failure of the counter or the run.
- **Mechanism (verified):** `jj-lane.sh` commits a named directory (snapshot) like `git add`;
  this host sets `snapshot.max-new-file-size = 1MiB` (measured: `jj --ignore-working-copy
  get snapshot.max-new-file-size` → `1MiB`). New files over 1 MiB are not snapshotted. V4's
  `after.json` is 2,852,279 bytes (≈2.72 MiB) — over the cap — so the data commit `5ca6941b`
  landed V3/L3/L4 `after.json`/`run.json` but no V4 `after.json`.
- **Evidence pointers:**
  - `git ls-tree -r --name-only 5ca6941b -- corpus/evidence/round-41/c1/` → V4 dir holds only
    `nonregular.tsv`, `oracle-run.json`, `oracle.tsv`, `run-harness-failure.log` (no
    `after.json`); V3/L3/L4 hold `after.json` + `run.json`.
  - `git diff --name-status 5ca6941b e9a24d07 -- corpus/evidence/round-41/c1/` →
    `A corpus/evidence/round-41/c1/V4/after.json` (only change).
  - First score at `042b8769` read V4 `receipt_present` false → 3/4 (kept, not hidden; see
    lesson). The score at `e9a24d07` → 4/4.
  - Commit messages: `5ca6941b` "…V4 run.json not written: c1-run.sh jq ARG_MAX…";
    `e9a24d07` "R41-C1 V4 receipt after.json (2.8 MB; skipped by the directory commit's 1 MiB
    rule at 5ca6941b, named as a file here)".
- **Captured-by:** none (the helper's warning was not read by the L1). The fix became QUALITY
  84 (M41-3; `evidence-tracked.py` red/green receipts in `l1/mistakes/`).
- **Check script:** `artifacts/R41W2Mistakes/check-m41-3-evidence-tracked.py` (git-tree only).
  - RED on mistaken state: `python3 -I -B …/check-m41-3-evidence-tracked.py $PWD 5ca6941b061591748c6755c1dcfc188941fcbd35`
    → `{'rev': '5ca6941b…', 'missing': ['corpus/evidence/round-41/c1/V4/after.json']}`, **exit 1**.
  - GREEN on repaired fixture: same script at `e9a24d07256d1606f01aa4d2d65f74e649c5f3d4`
    → `'missing': []`, **exit 0**.

---

## (b) M41-1 — C2 declared-tuple key mismatch uncaught because the L1 dry-ran its own control scorer

- **Class:** a two-seat interface frozen without an end-to-end dry run of the frozen counter —
  generator writes the combo declared tuple under one key, counter reads three other keys; the
  mismatch is invisible to any tool that does not run the frozen counter on the dev/held-out set.
- **Mechanism (verified):**
  - `tools/round-41/heldout-gen-v3.py` (same at freeze `d764389e`) writes each combo carrier's
    declared tuple under `'declared': declared` with `'class_expected': None` (lines 1464,
    1469); named classes carry `class_expected.features`.
  - `tools/round-41/c2-counter.py` (same at freeze) reads the declared tuple only from
    `class_expected.features`, else `features`, else `declared_features` (lines 1497–1503).
    Combo entries satisfy none → `declared-tuple-incomplete` → `observed_features_match_declared`
    false.
  - Score receipt `l1/scores/c2-at-e9a24d07.json`: `matched 52`/`n 52`,
    `exit_code 1`, `declared_features.missing = [C01..C12]`, `by_class.combo =
    declared-tuple-incomplete`.
  - The L1's pre-freeze C2 "dry run" was the control scorer `tools/round-41/c2-controls.py`
    (docstring: runs the *interpreter* vs the *evaluator* on dev envelopes), which never invokes
    `c2-counter.py` and has no declared-feature binding; `controls/c2/dev-scores-prefreeze.json`
    records scores only (no counter argv, no `observed_features_match_declared`). No C2 dry run
    of the frozen counter exists anywhere in `l1/` or `w1/` (search for dryrun traces finds only
    C1: `l1/dryrun-c1.json`, `l1/dryrun-c1-counter.json`). The claims file documents the
    pre-freeze dry run for C1 only.
- **Captured-by:** QUALITY 83 (pre-freeze dry run of every claim counter on a sandbox clone
  with development inputs of the frozen shape) — applied to C1, not to C2. Extended by QUALITY
  84 (M41-1; `l1/mistakes/declared-keys.py` red/green).
- **Check script:** `artifacts/R41W2Mistakes/check-m41-1-declared-keys.py` (mirrors the frozen
  counter's three-key reader).
  - RED on mistaken state: `python3 -I -B …/check-m41-1-declared-keys.py corpus/evidence/round-41/c2/heldout/manifest.json`
    → `unreadable_by_counter: [C01..C12]` (12 of 52), **exit 1**.
  - GREEN on repaired fixture: `manifest-repaired-green.json` (committed manifest with each
    combo tuple also copied under `features`) → `unreadable_by_counter: []`, **exit 0**.

---

## (c) M41-5 — `c1-run.sh` argv-size failure on the V4 receipt (run.json never written)

- **Class:** tool robustness on a large carrier — the harness passes the envelope-data summary to
  jq as one argv string (`--argjson summary "$summary"`); Linux caps a single argument string at
  `MAX_ARG_STRLEN = 32 × PAGE_SIZE = 131072` bytes and fails execve with E2BIG independent of
  total ARG_MAX (2,097,152 here).
- **Mechanism (verified, reproduced):**
  - The failure log retained: `corpus/evidence/round-41/c1/V4/run-harness-failure.log` and
    `l1/c1-run-V4.log` both contain exactly
    `tools/round-41/c1-run.sh: line 547: /home/vgpnk/.local/bin/jq: Argument list too long`.
    Line 547 is the receipt jq (`--argjson summary "$summary"`), which runs after `after.json`
    was already moved into the outdir — hence V4 has `after.json` but no `run.json`.
  - The summary the harness computes from V4's committed `after.json` is **146,561 bytes**
    (verified by running the exact summary jq from `c1-run.sh` lines 517–536 on
    `corpus/evidence/round-41/c1/V4/after.json`). That single string exceeds the 131,072-byte
    per-argument cap.
  - Threshold measured on this host: 131,071 bytes succeeds, 131,072 fails with rc=126
    "Argument list too long" (per-argument cap = 32 × 4096). The L1's label "ARG_MAX" points at
    the same `E2BIG` but the binding limit is the per-argument length cap, not the 2 MiB total.
- **Evidence pointers:** the two logs above; commit `5ca6941b` tree (V4 has no `run.json`);
  `c1-run.sh` lines 543–547 and 556–600 (the two `--argjson` sites); the R41-CL2 fix routing.
- **Captured-by:** none. Fix routed R41-CL2 (`--slurpfile`), measured by `w2/R41W2C1Run.md`.
- **Check script:** `artifacts/R41W2Mistakes/check-m41-5-argmax.sh` (uses the real V4 summary
  `v4-summary.json`, 146,561 bytes, derived from the committed receipt).
  - RED on mistaken state: the exact harness receipt-jq pattern with `--argjson summary` →
    **rc=126**, stderr "Argument list too long".
  - GREEN on the repair: same data via `--slurpfile summary` → **rc=0**.

---

## (d) M41-4 — seat R41C1Counter rewrote its artifacts after the freeze

- **Class:** a seat kept editing its artifacts after the L1 copied them into the freeze — a
  freeze-integrity/process violation, caught by diligence, not by an instrument.
- **Mechanism (verified):**
  - The L1's record `w1/artifacts/R41C1Counter-postfreeze/README.txt` states the seat rewrote
    files in its artifacts dir after the freeze (mtimes 18:12 −03; freeze commit committer time
    `d764389e` = 18:08:13 −03), that the freeze-committed bytes were restored in place, and that
    the post-freeze copies were kept aside. It records three distinct byte sets: frozen
    instrument `tools/round-41/c1-counter.py` (sha256 `bbabbfec…`), freeze-committed artifact
    (`9a3dcf4b…`), post-freeze artifact (`06cd72c4…`).
  - Git blobs confirm: `R41C1Counter/c1-counter.py` is the same blob (`00def310…`) at every
    commit from `d764389e` through `7a24ff74`, so the rewrite never entered any tree; at
    `7a24ff74` the restored dir is byte-identical to the freeze while the kept-aside dir differs
    (content sha256s: freeze `9a3dcf4b…`, post-freeze `06cd72c4…`, tool `bbabbfec…`).
- **Captured-by:** none (the wave-context rule "never touch them afterwards" is not an
  enumerated QUALITY criterion). Restore landed at `7a24ff74`.
- **Check script:** `artifacts/R41W2Mistakes/check-m41-4-postfreeze-restore.py`.
  - GREEN on repaired state: lane at tip → 26 artifact files all freeze==tip, three distinct
    byte sets, **exit 0**.
  - RED on mistaken state: `--mistaken-fixture` = freeze tree overlaid with the post-freeze
    bytes (the seat's rewrite state) → 15 failures (e.g. `c1-counter.py: freeze 9a3dcf4b1303
    != committed 06cd72c45cc6`), **exit 1**.

---

## Cross-cutting observations

- QUALITY 84 was added this round precisely from M41-1 and M41-3; this seat's checks (b) and
  (a) operationalize the same two criteria from the frozen instruments' own byte behavior, with
  green fixtures that are either the repaired real commit or a minimal manifest repair.
- The four mistakes are separable: (a)+(c) both hit the V4 data commit but have different
  mechanisms (snapshot-size skip vs single-argument exec cap) and different fixes ((a) name the
  file / check `ls-tree` vs disk; (c) `--slurpfile`); (b) is an interface-contract miss visible
  only to the frozen counter; (d) is a process/immutability miss with no tree impact.
- No claim verdict is affected by this seat's findings beyond what the L1 already recorded:
  C1 met at `e9a24d07` (4/4, exit 0, incl. `c1-extra.py`), C2 stopped honestly (52/52 pairs,
  exit 1 on `observed_features_match_declared`).
