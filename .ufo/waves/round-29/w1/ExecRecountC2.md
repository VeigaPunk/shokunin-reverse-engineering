# R29-C2 measured-tip recount

**Verdict: holds.** The measured-tip counter reports the requested `responses_complete=178/178 entries=252 mismatches=0 predicted_true=38 predicted_false=214 entry_ok=1`; it exited 0. The selftest reports 19 cases, 0 failures; it exited 0.

## Evidence

All times UTC on 2026-10-22. Commands ran in `/fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecRecountC2/clone`; `GIT_DIR`, `GIT_WORK_TREE`, and `GIT_INDEX_FILE` were unset for Git/Python commands.

- **[Observation] Clone:** `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q /home/vgpnk/Projects/shokunin/kaidoku-shokunin /fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecRecountC2/clone` — 2026-10-22T20:20:57Z, exit 0.
- **[Observation] Revision:** `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git rev-parse HEAD` — 2026-10-22T20:21:34Z, exit 0; exact output `18be864a528873b2b70d8c94e31f880290249e90`.
- **[Observation] Counter:** `python3 -I -B tools/round-29/c2-filtered-unseen.py --root /fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecRecountC2/clone --rev 18be864a528873b2b70d8c94e31f880290249e90` (with the three Git variables unset) — 2026-10-22T20:21:23Z, exit 0. Full stdout:

```text
responses_complete=178/178 entries=252 mismatches=0 predicted_true=38 predicted_false=214 entry_ok=1
```

  Stderr was empty.
- **[Observation] Selftest:** `python3 -I -B tools/round-29/c2-filtered-unseen.py --selftest` (with the three Git variables unset and `TMPDIR=/fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecRecountC2/tmp`) — 2026-10-22T20:21:42Z, exit 0. Full stdout:

```text
ok green-both-branches exit=0 want=0
ok red-flag-flipped-canonical-alternative exit=1 want=1
ok red-flag-flipped-canonical-name exit=1 want=1
ok red-flag-on-non-canonical exit=1 want=1
ok red-flag-not-boolean exit=1 want=1
ok red-missing-response exit=1 want=1
ok red-selector-key-absent exit=1 want=1
ok red-early-fetch exit=1 want=1
ok red-sha exit=1 want=1
ok red-url exit=1 want=1
ok red-status exit=1 want=1
ok red-no-canonical-branch exit=1 want=1
ok red-entry-wrong-count exit=1 want=1
ok red-entry-old-row exit=1 want=1
ok red-row-not-in-gate exit=1 want=1
ok red-row-status exit=1 want=1
ok red-cites-other-new-row exit=1 want=1
ok red-no-false-branch exit=1 want=1
ok red-pin-refusal exit=2 want=2
selftest cases=19 failures=0
```

  Stderr was empty.
- **[Observation] Source hash:** `sha256sum tools/round-29/c2-filtered-unseen.py` — 2026-10-22T20:21:58Z, exit 0; `00ca0a3d72515c2636c63f39785d799924dd6530f67cc8787b2a632817c5a801`.

## Retained artifacts

- `counter.stdout` — SHA-256 `d9a5502760474b98ff2e7b2663b5adc8de11b8f30285abe2ec5abef977ed174d`
- `counter.stderr` (empty) — SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `selftest.stdout` — SHA-256 `3e3d5926afec89d77fefb11add5b0f1cb2bef1eaad502e1c0dc5f140418fa06a`
- `selftest.stderr` (empty) — SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Executed source: `clone/tools/round-29/c2-filtered-unseen.py` — SHA-256 `00ca0a3d72515c2636c63f39785d799924dd6530f67cc8787b2a632817c5a801`

Artifact paths are relative to `/fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecRecountC2/`. No tools were installed or updated. No blocker observed.
