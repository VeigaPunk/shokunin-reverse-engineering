# ExecRepro report: independent reproduction of R95-C1 at 4bda1d1dd3788973f10e61212b70df18b3b14ea0

Verdict: R95-C1 reproduces from a fresh clone. Every claimed exit code, label, count, reason, revision and verdict matches the L1's committed receipts. The only mismatches are per-run fields the v5 writer generates from a random nonce.

Full evidence, exact command lines and per-field tables: `.ufo/waves/round-95/w1/ExecRepro/repro.md`.

## Results

| leg | command (short) | rc | outcome vs committed |
|---|---|---|---|
| a | v5 honest run, `--rev 4bda1d1d` | 0 | label, met True, selfverify ok=True reasons=0, counts and stdout byte-equal to `l1/scores/honest-pos.*`. Only `fresh_provenance` (nonce, fresh pack sha) and the two repaired-cell output shas differ, as expected from `secrets.token_hex(8)`. |
| b | forgery battery, `--honest-dir` = seat | 0 | full JSON and stdout equal to `l1/scores/c1-forgery-at-4bda…json` and `c1-forgery-stdout.txt`. Before admits (4 of 4); pos, F1, F2, F3 refused with reasons `label-not-frozen`, `label-not-recomputed`, `revision-not-bound`, `pins-not-bound`, exit 1 each. 12 of 12 fixture sha pins match. |
| c | symlink probe on v5 | 0 | full JSON equal to `l1/scores/c1-symlink-v5-at-4bda…json`. verdict hardened, victim_intact true, receipt_valid true. |
| d1 | round-94 counter over committed forged fixtures, run at base | 0 | full JSON equal to `pre/c1-old-counter-admits-at-base.json`: met true, 4 of 4 agree/predicted/valid. The old instrument admits all four forgeries. |
| d2 | probe on round-94 v4 writer at base b5331db1 | 1 | full JSON equal to `pre/c1-symlink-v4-at-base.json`: victim_intact false, verdict followed-symlink. Do-nothing control confirmed. |
| selftest v5 | `--selftest --work` (and rerun on same work dir) | 0, 0 | `SELFTEST cases=6 failures=0`, matches `l1/scores/m95b…` GREEN lines. |
| selftest agreement-v2 | `--selftest` | 0 | `SELFTEST cases=5 failures=0`. No committed counterpart in the lane. |
| selftest forgery | `--selftest` | 0 | `SELFTEST cases=3 failures=0`, matches `l1/scores/m95a…` GREEN block. |

Pins: `sha256sum -c .ufo/waves/round-95/pins.sha256` in the 4bda clone gives 26 of 26 OK (rc 0). Instrument hashes match the claim pins: v5 6fc81208…, agreement-v2 ca7d213a…, forgery 8e43d7cf…, probe e07ff669…, v4 c41d54d7… at base and at 4bda, round-94 counter dc384a44….

## Observations

1. v5 honest JSON is not byte-reproducible across runs (nonce-driven fresh pack). Compare by fields, not bytes.
2. The v5 probe leaves the planted `<json-out>.tmp` symlink in place. The victim is intact and the writer does not follow it. This is harmless for C1.
3. The forgery fixtures are not present at base (`.ufo/waves/round-95/forgery/` absent there). d1 read them from the 4bda clone; their bytes match the pins in the receipt.

## Drafts and attacks

No C1 attack was attempted; the item was reproduction only. No R95-C2 draft was produced in this seat (not assigned to ExecRepro).

## Tooling

No tools installed or updated. No pacman transactions. No host state changed.

## Files written

In `.ufo/waves/round-95/w1/ExecRepro/`:
- `repro.md` (command lines, exit codes, per-field match tables)
- `honest-pos.json`, `honest-pos.stdout`, `honest-pos.stderr`, `honest-pos.rc`
- `forgery.json`, `forgery.stdout`, `forgery.stderr`, `forgery.rc`
- `probe-v5.json`, `probe-v5.stdout`, `probe-v5.stderr`, `probe-v5.rc`
- `probe-v4-at-base.json`, `probe-v4-at-base.stdout`, `probe-v4-at-base.stderr`, `probe-v4-at-base.rc`
- `d1-old-counter.json`, `d1-old-counter.stderr`, `d1-old-counter.rc`
- `selftest-v5.{stdout,stderr,rc}`, `selftest-v5-rerun.{stdout,stderr,rc}`, `selftest-agreement-v2.{stdout,stderr,rc}`, `selftest-forgery.{stdout,stderr,rc}`
- `sha256-instruments-at-4bda.txt`, `pins-check.txt`, `compare.txt`, `compare.py`

This report: `.ufo/waves/round-95/w1/ExecRepro.md`.

Scratch under `/fast/scratch/hyaku/kaidoku-r95/ExecRepro` (clones, work dirs) removed before yield.
