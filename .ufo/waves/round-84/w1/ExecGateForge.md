# R84-W1 / ExecGateForge — gate forgery attack on R84-C1's counter

Seat: executor (gate forgery attack). Counter under attack:
`tools/round-84/freeze-precheck.py` (frozen, read-only; executed from the lane with
`python3 -I -B`, never edited). Method: private scratch git repo
`/fast/scratch/hyaku/kaidoku-r84/ExecGateForge/repo` with its own `git -C "$D"` fixture —
the lane repo was never touched. Each forged container was committed as
`.ufo/waves/round-84/<case>.json` and scored at its rev, mirroring the C1 counting-command
shape (`--root <repo> --rev <sha> --container <path>`).

## Fixture repo

- rev1 (all forged containers + counter blobs): `555589a6bb9ccc71c1a173a0d55fb75bcbc76350`
- rev2 (adds `tools/round-85/late-tool.py`, exists only in a later revision): `21876cc40b08ec610c05f4b70657db1cbbda3cdd`
- rev3 (adds the honest control container): used only for the combined exit-0 check below.
- Counter blobs: copies of lane `tools/round-84/freeze-precheck.py` and
  `tools/round-84/nested-sqfs.py` (sha256 pinned in fixture containers).
- `git rev-parse --show-toplevel` asserted equal to the fixture dir before any commit.
- Scratch dir removed before this yield; all receipts copied to
  `.ufo/waves/round-84/w1/ExecGateForge/receipts/` (25 files).

## Per-forgery results (11/11 executed; verdict, findings, exit code)

Each case ran twice: `-bare` (no `--expect`) and `-exp` (`--expect <container>=FLAGGED`).
Verdict/findings identical in both; receipts hold the full gate JSON.

| # | Forgery | Verdict | Findings | exit bare | exit exp |
|---|---------|---------|----------|-----------|----------|
| 1 | claim names unpinned counter path (f01) | FLAGGED | `COUNTER_PATH_NOT_PINNED:tools/round-84/freeze-precheck.py` | 1 | 1 |
| 2 | pin names a different path than the claim (f02: pin holds `nested-sqfs.py`) | FLAGGED | `COUNTER_PATH_NOT_PINNED:tools/round-84/freeze-precheck.py` | 1 | 1 |
| 3 | pin digest is a valid digest of another blob (f03: `nested-sqfs.py`'s digest on `freeze-precheck.py`) | FLAGGED | `COUNTER_PIN_MISMATCH:tools/round-84/freeze-precheck.py` | 1 | 1 |
| 4 | two claims: one names+pins a counter, one names none (f04) | FLAGGED | `CLAIM_NO_COUNTER_PATH:R84-C2` (only the defective claim) | 1 | 1 |
| 5 | path present only in `instruments`/`fixtures`, no claim string names it (f05) | FLAGGED | `CLAIM_NO_COUNTER_PATH:R84-C1` | 1 | 1 |
| 6 | claim names bare filename `attribution-audit.py` (f06) | FLAGGED | `CLAIM_NO_COUNTER_PATH:R84-C1` | 1 | 1 |
| 7 | claim names directory prefix `tools/round-84/` (f07) | FLAGGED | `CLAIM_NO_COUNTER_PATH:R84-C1` | 1 | 1 |
| 8 | claim names `tools/round-84/./nested-sqfs.py` (f08) | FLAGGED | `COUNTER_BLOB_ABSENT:tools/round-84/./nested-sqfs.py` | 1 | 1 |
| 9 | claim names a path existing only in a later revision (f09: `tools/round-85/late-tool.py` at rev1) | FLAGGED | `COUNTER_BLOB_ABSENT:tools/round-85/late-tool.py` | 1 | 1 |
| 10 | `claims` is a dict, not a list (f10) | FLAGGED | `CONTAINER_NO_CLAIMS` (claims counted 0) | 1 | 1 |
| 11 | two claims naming the same unpinned path (f11) | FLAGGED | `COUNTER_PATH_NOT_PINNED:tools/round-84/freeze-precheck.py` **×2** — once per claim | 1 | 1 |

**Accepted forgeries: none.** No crash, no timeout, no non-JSON output, no empty stderr
anomalies (all runs stderr-empty). Case 10 would have been the crash candidate (`claims` as
dict) — the gate coerces to `[]` and reports `CONTAINER_NO_CLAIMS` instead.

## Exit-code semantics (measured, relevant to the C1 counting command)

- Bare single-container runs: exit 1 for every FLAGGED verdict (FLAGGED without expectation
  is a mismatch by the gate's own rule).
- `-exp` solo runs: `mismatches []`, `refused_expected 1`, but exit **1** — `met` requires
  `accepted_expected >= 1`, which a lone forged container cannot satisfy
  (receipt `f05-path-only-in-pins-exp.json`: `mismatches [] refused 1 accepted 0 met false`).
- Combined FLAGGED-expected + CLEAN-expected containers in one invocation: exit **0**,
  `mismatches []`, `refused 1`, `accepted 1`, `met true` (receipt `combined.json`). This is
  exactly the C1 counting-command shape (round-83 FLAGGED + round-84 CLEAN), so the claim's
  declared invocation returns 0 when both halves hold.

## Findings and observations for the L1

1. **No calibration hole found.** All eleven forgeries are refused with exactly one finding
   each (f11: two), and every finding is the semantically correct one. The gate's ordering —
   blob-existence check before pin check, pin lookup by exact string, per-claim path
   extraction with `(?<![\w./-])` boundary — leaves no bypass among the tested classes.
2. **f08 normalization:** `git show <rev>:tools/round-84/./nested-sqfs.py` fails (`git` does
   not normalize `./` in tree paths; probe returncode != 0), so the dotted spelling lands in
   `COUNTER_BLOB_ABSENT` and cannot be laundered even when the container also pins the dotted
   key at the correct digest (the pin is inert). Refusal, not acceptance — safe direction.
3. **f11 answers the posed question:** the same unpinned path is reported **twice** (once per
   claim); deduplication (`sorted(set(...))`) exists only within a single claim's string set.
   A consumer keying findings by path must dedupe itself.
4. **f02 nuance:** a pin of a *different* path is not itself flagged; the finding names the
   claim's path as unpinned. A container could pin unrelated paths without any finding beyond
   the per-claim one — acceptable, but reviewers should not expect a "stale pin" finding.
5. **Control confirmed insufficient-by-design:** with `--control instruments-only`, f05 (path
   only in pins, claim names nothing) is `control.accepted true` while the real gate refuses
   it — the cheap rule accepts this forgery, which is the claimed property of the control.
6. **Cosmetic only (no action needed for C1):** `COUNTER_BLOB_ABSENT` short-circuits pin
   validation (f08, f09), so a misspelled-but-pinned path never reports the pin as mismatched;
   and solo `--expect FLAGGED` runs exit 1 despite `mismatches []` (see exit-code semantics).

## Scope note

All eleven assigned cases were executable; none was skipped. No production file, sibling-lane
file, frozen byte, or fleet-root tracked file was written; the only writes are this report,
the receipts under `.ufo/waves/round-84/w1/ExecGateForge/receipts/`, and the since-removed
scratch tree.

## Tooling record (operator 2026-10-19 authorization)

No tool installed or upgraded. Used preexisting host `python3` and `git` only
(`pacman` paused host-wide; no install was needed).

## Files changed / retained evidence

- `.ufo/waves/round-84/w1/ExecGateForge.md` (this report)
- `.ufo/waves/round-84/w1/ExecGateForge/receipts/` — 25 gate receipts:
  `f01…f11` × `-bare`/`-exp` (22), `f05-path-only-in-pins-ctl.json`, `combined.json`,
  `selftest.json` (gate `--selftest` run against the lane copy: `cases 10, failures [],
  exit 0`, confirming every finding class reachable on fixtures).

## Risks / blockers

None. The scratch fixture repo was deleted after receipt copy; its rev shas are recorded
above for reproduction (rebuild recipe: two counter blobs + 12 container files, commits as
described — all container bytes are reproducible from the receipt files).
