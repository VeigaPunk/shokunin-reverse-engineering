# EX-29 — seat report (chain c2, executor), wave arc3-loop1-round3 (DRAFT — finalized at close)

Task as given: live pair with the REVISED tool — pre-capture FIRST
(`claims/c2/receipts/config-pre-pair-v2r3.txt`), post at close; verify MATCH 5/5.

## 1. Work performed (evidence pointers)

- **Round-start baseline** captured 2026-10-19T13:06:57Z (before other seats' live
  work; the revised tool did not exist yet): `claims/c2/receipts/config-pre-pair-v2r3.txt`
  sha256 `d31ece6f0d5519a476d9067a40a566ec9d2c38f2e55068435655ae039e46b0a0`,
  tool `112d01dc…` (the round-2 v2 revision whose before-states this round closes),
  HEAD `c07af80fcf3a60f9c6a0ca09b6e23fb5794d3311`, exit 0, 5/5 present.
  Transcripts: `capture-pre-roundstart.out`; sidecar re-derived (`sha256sum -c` OK).
- **Baseline vs live**: `verify … --live` → `MATCH paths=5/5 drift=0 exit=0`
  (`verify-pre-roundstart-vs-live.out`).
- **Cross-round boundary check**: verify round-2 receipt vs round-start baseline →
  `CONTENT-DRIFT exit 10`, exactly one path: `~/.kimi-code/config.toml`
  (sha256 `8cbacd48…`→`bc66d543…`, inode 34530637→37793921, mode 600→644,
  mtime/ctime 1792376443→1792414665 = 2026-10-19T12:57:45Z, i.e. **pre-wave**;
  other four paths byte-identical) — `verify-roundstart-vs-r2receipt.out`,
  field-by-field diff in `r2-vs-roundstart-fielddiff.txt` (filled at close).
- **Independent digest cross-check**: raw `sha256sum` of the five paths == the
  receipt's recorded digests (`raw-sha256sum-crosscheck.out`).
- **Third-party corroboration**: RV-9's independent parser diff vs my baseline =
  0 diffs (16/16 fields × 5 paths), their stat-only T0 capture agrees
  (`claims/c2/RV-9/rv9-field-diff-exp29pre-vs-mine.out`, `rv9-independent-T0.txt`).
- **Before-state reproductions** (own, scratch `/dev/shm/ex29-scratch` only;
  mirrors EX-22's baseline and RV-6's `base` arm):
  - D2a dir-EACCES: capture exit 13, `EXISTS: no` + `STAT-ERROR`; `verify --live`
    → **MATCH exit 0 (fail-open)** — `before-D2-dir-eacces-*.out`
  - D2b file-EACCES: capture → `PermissionError` traceback exit 1, no receipt —
    `before-D2a-eacces-capture.out`
  - D2c live unreadable candidate: traceback exit 1 —
    `before-D2c-live-unreadable.out`
  - D3 core: 1-of-3 receipt vs live → `MATCH paths=1/1 drift=0 exit=0` —
    `before-D3-core-1of3-vs-live.out`; (1of3 vs 3of3 → METADATA-DRIFT exit 12,
    extras on candidate side flagged — `before-D3-1ofN-coverage.out`)
  - D6: `selftest --scratch <missing>` → `FileNotFoundError` traceback exit 1 —
    `before-D6-selftest-missing-scratch.out`
  - write-guard: `--paths X --out X` → exit 0, X clobbered 644b444e…→cde3b704…,
    replaced by receipt text — `before-writeguard-clobber.out`
- **Non-vacuity control**: a deliberately mutated scratch copy of the baseline
  receipt → `CONTENT-DRIFT exit 10` (`positive-control-content-drift.out`).
- **Revision watch**: `poll-for-revision.sh` (detected first revise at 13:08:29Z),
  `watch-stability.sh` (sha trajectory in `stability-watch.txt`:
  112d01dc → 68e30768 → 1287c9d6 → a991f976 → d9be407d → 08fb6833 → …).
- **Revised-tool pre**: (filled at close)
- **Post + pair verifies**: (filled at close)

## 2. Proposed changes

None authored by this seat. The chain's real target (`.ufo/gates/custody-pair/`)
is EX-21's write scope; this seat is read-only over it. No patch text.

## 3. Before → after measurement for the chain's claim (FILLED AT CLOSE)

| item | before (tool `112d01dc`, measured here) | after (revised tool at close) |
|---|---|---|
| D2a dir-EACCES verify | MATCH exit 0 (fail-open) | (fill) |
| D2b file-EACCES capture | traceback exit 1 | (fill) |
| D2c live unreadable | traceback exit 1 | (fill) |
| D3 1-of-N coverage | MATCH exit 0 (`paths=1/1`) | (fill) |
| D6 missing scratch | traceback exit 1 | (fill) |
| clobber `--paths X --out X` | X replaced by receipt, exit 0 | (fill) |
| selftest | 15/15 exit 0 | (fill) |
| live pair | round-start ≡ revised-pre (fill) | pre ≡ post MATCH 5/5 (fill) |

## 4. Attacks / refutations attempted, with verdicts

| # | attack | verdict |
|---|---|---|
| A1 | MATCH 5/5 is vacuous (instrument blind in this config) | refuted — mutated copy → CONTENT-DRIFT exit 10 |
| A2 | the instrument cannot see cross-round changes | refuted — caught `~/.kimi-code/config.toml` rewrite |
| A3 | receipt grades its own homework | refuted — raw sha256sum agrees; RV-9 independent parser agrees |
| A4 | my "before" facts differ from the chain's | refuted — same states as EX-22 baseline / RV-6 base arm |
| A5 | probing changes the probed state (read moves custody paths) | (fill — atime not captured; inode/ctime stable across my probes) |
| A6 | revised tool still fail-open on the four holes | (fill at close) |
| A7 | pair verifies only in one direction | (fill — reverse-direction verify at close) |

## 5. Blockers

None so far. (fill at close)