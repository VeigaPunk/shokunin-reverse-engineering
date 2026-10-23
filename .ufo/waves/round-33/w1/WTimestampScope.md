# WTimestampScope — round-33 timestamp-repair allowance audit (5 pinned rows, base receipts, scope)

Reviewer seat, round 33 w1. Read-only audit of the five allowance entries of the L1-directed
hash-bound timestamp repair (`prep/R33TimestampRepair.md`), every token on their pinned lines at
base `428315a8f5674b952def862910af6e07a6c2224b`, and the base-red/repaired receipts. No gate was
run; all verification was performed by reading the lane's Git objects at the pinned revision
(`git show`, `git blame --porcelain`), independent sha256 recomputation, and reading retained
scratch artifact digests. No lane file written other than this report.

## 1. The five allowance rows and their pinned lines (verified at base `428315a8`)

Blob line bytes extracted from base Git objects; computed line sha256, all ISO-8601 tokens on the
line (regex `\d{4}-…T…(Z|±hh:mm)`), and blame commit/committer time:

| row | `FILE:LINE` | spec pin `line_sha256` | computed line sha256 | tokens on line (all) | blame commit / committer time |
|---|---|---|---|---|---|
| 1 | `a2audit-gate.json:14` | `8c727cad3617fa4ab79a61febdbf6b0ddd8b15880bb54e0889c8585ae3d9ec4b` | identical | `2026-10-23T07:35:00Z` (1) | `33393e594f…` / 06:56:11Z |
| 2 | `a2audit-settle.json:3` | `8c727cad3617fa4ab79a61febdbf6b0ddd8b15880bb54e0889c8585ae3d9ec4b` | identical | `2026-10-23T07:35:00Z` (1) | `bbdd793d558…` / 07:14:24Z |
| 3 | `a2residual-dispatch.json:17` | `1213815d435402b8ddde10e67f0faca71a9e798b5607caa5cb1b31944c47729b` | identical | `2026-10-23T07:55:00Z` (1) | `bbdd793d558…` / 07:14:24Z |
| 4 | `a2residual-settle.json:3` | `3d42105e95a6420edce5857477487c29f4883ad2e29269cde31ddfd3f986cd77` | identical | `2026-10-23T07:55:00Z` (1) | `9ef97f08b65…` / 07:30:33Z |
| 5 | `a2after/timestamps-strict-at-9ef97f08.txt:3` | `3bcd5127ee49014d02a9c248c614e725fbc117b67e65f49f6cbcf399b462de03` | identical | **8 tokens** (see §2) | `547d6f2c9f…` / 07:41:55Z |

Rows 1 and 2 pin byte-identical lines (same sha256, same deadline value) at different paths; the
wrapper's key is `(file, line)` + hash, so both are independently binding. Epoch conversions
checked: 1792738571=06:56:11Z, 1792739664=07:14:24Z, 1792740633=07:30:33Z, 1792741315=07:41:55Z.

## 2. Each allowance is an old planned deadline, not an observed future run

- Row 1 `settle_deadline=07:35:00Z`: introduced 06:56:11Z — planned deadline written 38m49s
  before the cutoff it schedules. Deadline field, not a run instant.
- Row 2 `settle_deadline=07:35:00Z`: introduced 07:14:24Z; file `observed_cutoff_utc` is
  `07:12:53+00:00` and the latest `transcript_last_assistant_at` on the file is `07:07:22.859Z`
  (line 164) — both ≤ the allowed value, so it is the planned cutoff bounding the settle window.
- Row 3 `deadline=07:55:00Z` (line 17 of `a2residual-dispatch.json`): introduced 07:14:24Z —
  dispatch spec written 40m36s before the deadline it schedules. Verified in context (line 14-17):
  it is the authorization-window deadline of the residual dispatch, with `operator_ruling "Main
  07:10Z…"` and `gate_second_grant` on adjacent lines; not a run instant.
- Row 4 `deadline=07:55:00Z`: introduced 07:30:33Z; file `observed_cutoff_utc` is
  `07:28:02+00:00` and the latest `transcript_last_assistant_at` is `07:26:35.868Z` (line 76) —
  both ≤ 07:55:00Z, so it is the planned cutoff bounding the residual window.
- Row 5 echo line 3: the line's 8 timestamp tokens are `06:56:11Z, 07:35:00Z, 07:14:24Z,
  07:35:00Z, 07:14:24Z, 07:55:00Z, 07:30:33Z, 07:55:00Z` — the four `committer_time` values and
  the four `timestamp` values of the prior strict run's findings, all of which are planned-deadline
  fields (two 07:35:00Z, two 07:55:00Z) or their introducing committer instants. No `utc_start`/
  `utc_end` execution field is on line 3 (those live on lines 1 and 5 of the same receipt file).
  Only the two `07:55:00Z` tokens are strictly later than the line's committer time (07:41:55Z),
  exactly the two findings the tool flags at base. They are copies of the two residual planned
  deadlines, not observed run instants.

## 3. Hash binding prevents an inserted event from inheriting an allowance

Wrapper `run-gate-hashed.py` (scratch sha256 `e011ed69e72bed408de30211712b2e65d69fd01b9c002a45eb7ce5acf6055bb0`; identical installed copy) verified in source: for every spec row it reads `<rev>:<scope>/<file>` as a Git blob, splits on LF, hashes the exact line bytes, and compares to the spec pin; **only if all rows match** does it forward the `--allow` arguments to the unchanged tool (which then runs normally). Any mismatch, missing path, or missing line exits 1 with `{"error":{"code":"allowance_line_changed",…}}`, `tool_run:false`, and forwards no allowance.

- Selftest receipts (origin-isolated, wrapper, and installed-copy runs all byte-identical):
  `green` clone `13493f8c…` exit 0, 6 findings / 0 unexempted / 5-of-5 applied; `sameline` clone
  `3adfeda7…` (2001-02-03T04:05:06Z inserted into the allowed echo line) exit 1,
  `code=allowance_line_changed`, `tool_run=False`; `unlisted` clone `45d2b034…` exit 1, 7 findings /
  1 unexempted at `a2extra/unlisted.json:1`, 5-of-5 applied.
- Counterfactual `hashed-selftest-runs/sameline-raw-five-allows.json` (digest verified
  `7344533abd051405d0c37c65365ad3586893c7a71e05df2a8343b5cbccdb595f`): invoking the unchanged tool
  directly on the same-line clone with the same five raw `--allow` args exits 0 and exempts the
  inserted `2001-02-03T04:05:06Z` instant (13 findings, all exempted — including the injected
  instant and the 2000-commit 2026 echoes). The wrapper instead refuses the whole spec, leaving the
  inserted instant unexempted. This is exactly the laundering vector the pin closes.

## 4. Base-red and repaired receipts (lane copies vs scratch digest-identical)

- Base-red `receipts-hashed-base-red/`: `utc_start=08:19:08Z`, `exit=1`, `utc_end=08:19:09Z`;
  `allowances-empty.json` spec (lane sha256 `48d5f3c4bfd519db18acfb5f0b532dca153f5e69e255b5cdfbba08495627f7b2` = scratch) with `allow:[]`; `verified_lines=[]`, `allow_forwarded=[]`; stdout
  (sha256 `de2e83f02f83da1150f23b114ab3a030c82a93a1cf5e7808b56aedee25999fff`) = the raw 08:09:39Z
  baseline: `files_scanned=179`, 6 findings, 6 unexempted. The original red is reproduced as the
  control.
- Repaired `receipts-hashed-repaired/`: `utc_start=08:19:09Z`, `exit=0`, `utc_end=08:19:10Z`;
  spec `allowances-hashed.json` (sha256 `0ba984d64e98c8784974d852a89919ec54685188e68428c95c4953427d500332`); argv forwards exactly the five `--allow` rows in spec order; `verified_lines` reports all
  five line hashes (matching my independent computation for every row, including row 5's two echoed
  tokens); `allow_forwarded` lists all five; stdout (sha256 `afef2d70317e65a2f914896d29264fd9922efc3b2600db3648919386b40bd070`) = `files_scanned=179`, 6 findings, 6 exempted, 0 unexempted, all
  five allowances `applied:true`. `resolved_rev=428315a8f5674b952def862910af6e07a6c2224b` in both
  receipts. Lane copies of both stdout files are sha256-identical to the scratch receipts.
- Historical bare four-line runs also present: `9ef97f08` green (168 files, 4 findings, 0
  unexempted, 4/4 applied; stdout sha256 `c5888db554e93639abe30a692cd781e02a9a95d4aa5535258623200e88bf9375`) and base `428315a8` red with 2 unexempted receipt-copy findings (stdout sha256
  `9c17514b3d9bfa1a06e9aae198cc733fe4b5af2be7058fc6cdb6a21e494404ac`) — the exact comparison pair the
  repair replaces.

## 5. Scope limits

- Specs and stdout consistently report `scope: ".ufo/waves/round-32"`; the scan is revision-scoped
  (reads via `git ls-tree`/`cat-file`/`blame`), `files_skipped=0`, no binary blobs. No claim,
  score, build, formatter, or REA runs; no carrier execution; no pacman transaction.
- Fixture/control claims verified retained: `fixture/repo` 29,055 bytes, `hashed-fixture` 438,704
  bytes (< 1 MiB), both with `GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE` unset in receipts;
  `fixture-runs/` holds all seven cases with exits and stdout matching the report's table exactly
  (mixed-no-allow 1/2/2, mixed-allow-deadline 1/2/1, mixed-allow-actual 1/2/1, planned-no-allow
  1/1/1, planned-allow-deadline 0/1/0, planned-wrong-line 1/1/1 with `applied:false`, echo-allow-deadline 1/2/1). The `--allow` semantics claim (`applied:true` only when a future finding
  matched the exact key) is confirmed by these controls.
- Tool integrity: `evidence-timestamps.py` sha256 `489ef6ca668ec5c8b3d7faed0e24e6bd3cbf616951f4d49dfbec438e392acc00` at base blob and in the worktree (git status clean for the path); `--selftest`
  receipt `SELFTEST: CLEAN cases=5` (digest `d6c7c21a8ed600b5c0d98894eeae555c2dfcf4a30be8c925567931332632753d`). Each selftest case is capped (`timeout 120` inside
  `run-hashed-selftest.sh:22`, runner under `timeout 600`); no `selftest-*` tempdirs remain.
- Safety: this repair item is unrelated to the held R33FixtureBuilder item (no fixture-builder
  artifact read; only the metadata files were read), and no quarantine files were opened.

## 6. Findings by severity

- **Critical/major:** none. All five allowance rows are genuine old planned deadlines, their pins
  bind exactly the base line bytes, hash binding demonstrably prevents same-line insertion from
  inheriting an allowance, and the base-red/repaired receipts reproduce the claimed 6/6 vs 6/0
  outcome with matching digests.
- **Minor (documentation precision):**
  1. Row 5's spec `tokens` array (`["2026-10-23T07:55:00Z","2026-10-23T07:55:00Z"]`) is the
     future-dated subset, not an inventory of all timestamp tokens on the line, which carries 8
     (four committer instants + four deadline echoes). The `token_rule` text describes the subset
     correctly ("the only tokens later than the line's committer time are…"), so this is not
     functionally wrong — but a reader treating `tokens` as the full line inventory would
     undercount. Rec: rename to `future_tokens` or document "sub-in of tokens later than the line's
     committer time" in the spec/order. No effect on hash binding.
  2. Report §7 "largest payload 2,178 bytes" is accurate for tool stdout (the repaired stdout is
     2,178 bytes) but not for all retained scratch files: `hashed-selftest-runs/sameline-raw-five-allows.json` is 3,765 bytes (still < 1 MiB). Cosmetic understatement; no bound violated.

## 7. Residual risk and verification gaps

- Verification is evidence-based, not a re-run: selftest and gate behavior were confirmed from the
  retained receipts' digests and the wrapper source, not by executing them in this seat (no gate
  runs were permitted). The wrapper source itself was read in full and its hash check, fail-fast
  exit-1 path, and `--allow` forwarding are consistent with every retained receipt.
- The pin covers line bytes only; any legitimate reflow invalidates all allowances until re-pinned
  and re-selftested (intended default-deny, documented). Verification of "re-pin cycle" behavior
  (a changed spec plus re-pinned hashes) is not in the retained evidence — the three selftest
  cases cover changed-line refusal and unlisted-file refusal, not a legitimate re-pin.
- `a2audit-settle.json`/`a2residual-settle.json` planned-deadline classification rests on the
  reported `observed_cutoff_utc` and `transcript_last_assistant_at` maxima (verified present and
  within bounds above), not on an independent census of every seat transcript.

## 8. Tooling

No installs or updates performed; only `git`, `sha256sum`, `python3`, `/usr/bin/find`,
`/usr/bin/du`, `date` used (all pre-existing). No pacman transactions. No gate runs, no parser
runs, no fixture writes, no lane mutations other than this report.

Trailer: `.ufo/waves/round-33/w1/WTimestampScope.md`
