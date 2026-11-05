# ExecRepro: independent non-author reproduction of R95-C1 at 4bda1d1dd3788973f10e61212b70df18b3b14ea0

Seat: ExecRepro (executor). Base: b5331db1fb0ce0bf93695ce1730cf831effef6a9. Instrument revision: 4bda1d1dd3788973f10e61212b70df18b3b14ea0.
Clone: a fresh `git clone --shared` of the lane, checked out at 4bda1d1d (for legs a-c and the selftests) and at b5331db1 (for leg d2 and the base-side pins). The lane itself was not written.

Shell variables used for every command below (exact values):

```
S=/fast/scratch/hyaku/kaidoku-r95/ExecRepro
CLONE=$S/clone
BASE=$S/base
SEAT=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-95/w1/ExecRepro
LABEL='repaired 12 of 12; wrong 0; unsafe 0; intact 6 of 6; far-refused 12 of 12; fresh-roundtrip 2 of 2'
```

## Commands and exit codes

Exit codes are read from `$SEAT/<name>.rc`, which each command writes with `echo $?`.

### (a) honest v5 public run: rc 0

```
cd "$CLONE" && TMPDIR="$S/tmp" python3 -I -B tools/round-95/stop-boundary-repair-battery-v5.py --root "$CLONE" --repair-cmd tools/round-92/upx-stop-boundary-search-repair.py --work "$S/work" --rev 4bda1d1dd3788973f10e61212b70df18b3b14ea0 --expect "$LABEL" --json-out "$SEAT/honest-pos.json" > "$SEAT/honest-pos.stdout" 2> "$SEAT/honest-pos.stderr"; echo $? > "$SEAT/honest-pos.rc"
```

Captured stdout (`honest-pos.stdout`): `selfverify ok=True reasons=0` then `repaired 12 of 12; wrong 0; unsafe 0; intact 6 of 6; far-refused 12 of 12; fresh-roundtrip 2 of 2 met True exit 0`. Stderr is empty.

### (b) forgery battery: rc 0

```
cd "$CLONE" && TMPDIR="$S/tmp" python3 -I -B tools/round-95/c1-forgery-refusal.py --root "$CLONE" --fixtures "$CLONE/.ufo/waves/round-95/forgery" --old-prefix forge --old-counter tools/round-94/c1-receipt-agreement.py --honest-dir "$SEAT" --honest-prefix honest --world-rev b5331db1fb0ce0bf93695ce1730cf831effef6a9 --instrument-rev 4bda1d1dd3788973f10e61212b70df18b3b14ea0 --expect "$LABEL" --json-out "$SEAT/forgery.json" > "$SEAT/forgery.stdout" 2> "$SEAT/forgery.stderr"; echo $? > "$SEAT/forgery.rc"
```

Captured stdout ends with `forgeries refused 4 of 4; before admits True; honest accepted True`. Stderr is empty.

### (c) symlink probe on v5: rc 0

```
cd "$CLONE" && TMPDIR="$S/tmp" python3 -I -B tools/round-95/symlink-probe.py --root "$CLONE" --writer tools/round-95/stop-boundary-repair-battery-v5.py --repair-cmd .ufo/waves/round-93/controls/identity_noop.py --work "$S/work-probe" --rev 4bda1d1dd3788973f10e61212b70df18b3b14ea0 --expect "$LABEL" --json-out "$SEAT/probe-v5.json" > "$SEAT/probe-v5.stdout" 2> "$SEAT/probe-v5.stderr"; echo $? > "$SEAT/probe-v5.rc"
```

(The shell variable is `$S/work-probe`, not `$S/work`, so the probe does not share the honest run's work directory.)

### (d1) round-94 agreement counter over the committed forged fixtures, run from the base clone: rc 0

```
cd "$BASE" && python3 -I -B "$CLONE/tools/round-94/c1-receipt-agreement.py" --dir "$CLONE/.ufo/waves/round-95/forgery" --prefix forge > "$SEAT/d1-old-counter.json" 2> "$SEAT/d1-old-counter.stderr"; echo $? > "$SEAT/d1-old-counter.rc"
```

The counter file is byte-identical to the base one (sha256 dc384a44… both in base and clone; see `sha256-instruments-at-4bda.txt`). The fixtures are read from the 4bda clone because `.ufo/waves/round-95/forgery/` does not exist at base (checked: `No such file or directory`); the fixture bytes match the pins in the receipt (see the fixture rows below).

### (d2) symlink probe on the round-94 v4 writer at base: rc 1 (expected: the probe exits 0 only for a hardened writer)

```
cd "$BASE" && TMPDIR="$S/tmp" python3 -I -B "$CLONE/tools/round-95/symlink-probe.py" --root "$BASE" --writer tools/round-94/stop-boundary-repair-battery-v4.py --repair-cmd .ufo/waves/round-93/controls/identity_noop.py --work "$S/work-d2" --rev b5331db1fb0ce0bf93695ce1730cf831effef6a9 --expect "repaired 12 of 12; wrong 0; unsafe 0; intact 6 of 6; far-refused 12 of 12; fresh-roundtrip 2 of 2" --json-out "$SEAT/probe-v4-at-base.json" > "$SEAT/probe-v4-at-base.stdout" 2> "$SEAT/probe-v4-at-base.stderr"; echo $? > "$SEAT/probe-v4-at-base.rc"
```

The probe script itself was taken from the 4bda clone, which is the same file (sha e07ff669…, pinned). The base clone supplies the v4 writer and the identity-no-op repair command.

### Selftests

```
cd "$CLONE" && TMPDIR="$S/tmp" python3 -I -B tools/round-95/stop-boundary-repair-battery-v5.py --selftest --work "$S/work-S5" > "$SEAT/selftest-v5.stdout" 2> "$SEAT/selftest-v5.stderr"; echo $? > "$SEAT/selftest-v5.rc"          # rc 0
cd "$CLONE" && TMPDIR="$S/tmp" python3 -I -B tools/round-95/c1-agreement-v2.py --selftest "$S/work-S2" > "$SEAT/selftest-agreement-v2.stdout" 2> "$SEAT/selftest-agreement-v2.stderr"; echo $? > "$SEAT/selftest-agreement-v2.rc"   # rc 0
cd "$CLONE" && TMPDIR="$S/tmp" python3 -I -B tools/round-95/c1-forgery-refusal.py --selftest "$S/work-SF" > "$SEAT/selftest-forgery.stdout" 2> "$SEAT/selftest-forgery.stderr"; echo $? > "$SEAT/selftest-forgery.rc"           # rc 0
cd "$CLONE" && TMPDIR="$S/tmp" python3 -I -B tools/round-95/stop-boundary-repair-battery-v5.py --selftest --work "$S/work-S5" > "$SEAT/selftest-v5-rerun.stdout" 2> "$SEAT/selftest-v5-rerun.stderr"; echo $? > "$SEAT/selftest-v5-rerun.rc"   # rc 0, same work dir (idempotence rerun)
```

Selftest results: v5 `SELFTEST cases=6 failures=0` (rc 0; rerun on the same work dir also rc 0 and `cases=6 failures=0`); agreement-v2 `SELFTEST cases=5 failures=0` (rc 0); forgery `SELFTEST cases=3 failures=0` (rc 0).

## Match or mismatch per field

Legend: "committed" is the lane file named in the row. "mine" is the file in this seat. "n/a" means the committed file has no such field, so there is nothing to compare.

### (a) honest v5 run vs `.ufo/waves/round-95/l1/scores/honest-pos.{json,stdout,stderr,rc}`

| field | mine | committed | match |
|---|---|---|---|
| rc | 0 | 0 | match |
| stdout (byte-equal) | `selfverify ok=True reasons=0` + label line | same | match |
| stderr (byte-equal, empty) | empty | empty | match |
| label (`expect`) | `repaired 12 of 12; wrong 0; unsafe 0; intact 6 of 6; far-refused 12 of 12; fresh-roundtrip 2 of 2` | same | match |
| met | True | True (label line) | match |
| exit | 0 | 0 | match |
| class | T7-chain-stop-boundary | same | match |
| counter_sha256 | 6fc81208… | 6fc81208… (= claim pin) | match |
| counts (14 keys) | identical dict | identical dict | match |
| fresh_cells[0..3]: all non-`output` fields | identical | identical | match |
| fresh_cells[0,1].output.sha256 | df742dfd… | c3faecaa… | MISMATCH (expected, see below) |
| fresh_provenance.nonce | 8996258291ee0a2a | 3b1961c96a2fe80d | MISMATCH (expected, see below) |
| fresh_provenance.fresh_packed_sha256 | df742dfd… | c3faecaa… | MISMATCH (expected, see below) |
| fresh_provenance other keys (blocks, deterministic, marker_offset 97640, source, source_sha256 a9ba02dc…, collides_public_packed false) | identical | identical | match |
| verdict | n/a | n/a | n/a |
| revision | n/a (the v5 receipt has no revision field) | n/a | n/a |

Expected mismatch: `fresh_provenance` says `"nonce"` comes from `secrets.token_hex(8)` at `tools/round-93/stop-boundary-repair-battery-v3.py:196`, which v5 imports. Every run gets a new nonce and a new marker, so the packed fresh source and its sha change between runs. The fresh cells' verdict fields (class, delta sign, roundtrip, value, stored) are unchanged. The JSON is therefore not byte-equal to the committed one: the full file differs only in `fresh_provenance` and `fresh_cells[0,1].output`.

### (b) forgery battery vs `.ufo/waves/round-95/l1/scores/c1-forgery-at-4bda1d1dd3788973f10e61212b70df18b3b14ea0.json` and `c1-forgery-stdout.txt`

| field | mine | committed | match |
|---|---|---|---|
| rc | 0 | (no committed rc; the target says exit 0) | match |
| full JSON | byte-equal parsed dict | same | match |
| stdout (byte-equal) | same | `c1-forgery-stdout.txt` | match |
| met | True | True | match |
| expect (label) | frozen label | frozen label | match |
| instrument_revision | 4bda1d1d… | 4bda1d1d… | match |
| world_revision | b5331db1… | b5331db1… | match |
| counter_sha256 (forgery counter) | 8e43d7cf… | 8e43d7cf… (= pin) | match |
| before.admits / counts / exit / met | True / {agree 4, predicted 4, valid 4} / 0 / True | same | match |
| honest rows | `pos`: agree, predicted, valid True, reasons [] | same | match |
| pos | exit 1, reasons `label-not-frozen`, refused True | same | match |
| F1 | exit 1, reasons `label-not-recomputed`, refused True | same | match |
| F2 | exit 1, reasons `revision-not-bound`, refused True | same | match |
| F3 | exit 1, reasons `pins-not-bound`, refused True | same | match |
| forgeries refused | 4 of 4 | 4 of 4 | match |

### (b-fixtures) forgery fixture bytes vs pins in `fixture_sha256`

| file | sha256 (computed) | pinned in receipt | match |
|---|---|---|---|
| forge-pos.json | 9d9f8111… | 9d9f8111… | match |
| forge-pos.stdout | e8db076c… | e8db076c… | match |
| forge-pos.rc | 9a271f2a… | 9a271f2a… | match |
| forge-F1.json | 98e42df1… | 98e42df1… | match |
| forge-F1.stdout | 1bdc856b… | 1bdc856b… | match |
| forge-F1.rc | 4355a46b… | 4355a46b… | match |
| forge-F2.json | 8025ec57… | 8025ec57… | match |
| forge-F2.stdout | 2f6b97d8… | 2f6b97d8… | match |
| forge-F2.rc | 4355a46b… | 4355a46b… | match |
| forge-F3.json | 63f1aeda… | 63f1aeda… | match |
| forge-F3.stdout | ebd07632… | ebd07632… | match |
| forge-F3.rc | 4355a46b… | 4355a46b… | match |

Fixture rc values read from disk: pos 0, F1 1, F2 1, F3 1.

### (c) probe on v5 vs `.ufo/waves/round-95/l1/scores/c1-symlink-v5-at-4bda1d1dd3788973f10e61212b70df18b3b14ea0.json`

| field | mine | committed | match |
|---|---|---|---|
| rc | 0 | (no committed rc) | match |
| full JSON | byte-equal parsed dict | same | match |
| met | True | True | match |
| receipt_met | False | False | match |
| receipt_valid | True | True | match |
| receipt_label | `repaired 0 of 12; wrong 0; unsafe 0; intact 6 of 6; far-refused 0 of 12; fresh-roundtrip 0 of 2` | same | match |
| revision | 4bda1d1d… | 4bda1d1d… | match |
| verdict | hardened | hardened | match |
| victim_intact | True | True | match |
| tmp_is_symlink / tmp_left | True / True | True / True | match |
| writer_rc | 1 | 1 | match |
| writer_sha256 | 6fc81208… | 6fc81208… (= pin) | match |

### (d1) round-94 counter over forged fixtures vs `.ufo/waves/round-95/pre/c1-old-counter-admits-at-base.json`

| field | mine | committed | match |
|---|---|---|---|
| rc | 0 | (exit 0 implied by met True) | match |
| full JSON | byte-equal parsed dict | same | match |
| met | True | True | match |
| counts_of_4 | agree 4, predicted 4, valid 4 | same | match |
| rows: all four `stdout` lines | identical | identical | match |

### (d2) v4 probe at base vs `.ufo/waves/round-95/pre/c1-symlink-v4-at-base.json`

| field | mine | committed | match |
|---|---|---|---|
| rc | 1 | (no committed rc) | match (the expected value for a non-hardened writer) |
| full JSON | byte-equal parsed dict | same | match |
| victim_intact | False | False | match (the expected value) |
| verdict | followed-symlink | followed-symlink | match |
| tmp_is_symlink / tmp_left | False / False | False / False | match |
| writer | tools/round-94/stop-boundary-repair-battery-v4.py | same | match |
| writer_sha256 | c41d54d7… | c41d54d7… (= pin) | match |
| revision | b5331db1… | b5331db1… | match |
| met | False | False | match |

### Selftests (no committed selftest receipt exists for two of the three; the reds and greens in the lane are text notes)

| selftest | rc mine | output mine | committed counterpart | match |
|---|---|---|---|---|
| v5 `--selftest --work` | 0 | `SELFTEST cases=6 failures=0` | `l1/scores/m95b-selftest-idempotence-red-green.txt`: GREEN run 1 and run 2 both `SELFTEST cases=6 failures=0, exit 0` | match (label, met, exit, failures) |
| v5 rerun on same work dir | 0 | `SELFTEST cases=6 failures=0` | m95b GREEN run 2 (rerun) | match |
| agreement-v2 `--selftest` | 0 | `SELFTEST cases=5 failures=0`; cases honest-accepted, rewrite-refused, not-recomputed-refused, short-revision-refused, fabricated-pins-refused, all ok | none in the lane | n/a (no committed counterpart) |
| forgery `--selftest` | 0 | `mini-before-admits: ok`, `mini-forgeries-refused: ok`, `mini-honest-accepted: ok`, `SELFTEST cases=3 failures=0` | `l1/scores/m95a-intact-denominator-red-green.txt` GREEN block, same three lines, `SELFTEST cases=3 failures=0`, GREEN exit 0 | match |

The selftest outputs have no label, met, reasons, revision, verdict, victim_intact or receipt_valid fields, so those columns do not apply to them.

## Base-side pins (kill rule: any pinned sha256 differing)

- `sha256sum -c .ufo/waves/round-95/pins.sha256` in the 4bda clone: 26 of 26 `OK`, rc 0 (`pins-check.txt`).
- Instrument hashes at 4bda, see `sha256-instruments-at-4bda.txt`: v5 6fc81208…, agreement-v2 ca7d213a…, forgery 8e43d7cf…, probe e07ff669…, v3 verdict 60026511…, v4 c41d54d7…, round-94 counter dc384a44…, upx repair ce1b1769…; `identity_noop.py` 518422b5… (path `.ufo/waves/round-93/controls/identity_noop.py`; the earlier `tools/round-93/controls/...` path in my command was my own typo and does not exist, the probe got the correct path). All match the claim pins.
- Base (b5331db1) v4 and round-94 counter hashes: c41d54d7… and dc384a44…, identical to the claim `old_instruments` pins.

## Observations (not claim-breaking)

1. The honest v5 JSON is not byte-reproducible because of the per-run nonce (above). Its verdict fields are reproducible. Anyone who compares by bytes instead of by fields will see a false mismatch.
2. The v5 probe run leaves the planted `<json-out>.tmp` symlink in place (`tmp_is_symlink true`, `tmp_left true`). The writer does not follow it and the victim is intact; the writer just does not remove an entry it never created. Harmless for C1; noting it.
3. The `--honest-dir` argument of the forgery battery accepts the seat directory, so the honest triple used in (b) is the one this seat produced in (a), not the L1's copy. Results agree with the L1's committed run.

## Files written in this seat

Receipts and captured streams (all in `$SEAT`): `honest-pos.{json,stdout,stderr,rc}`, `forgery.{json,stdout,stderr,rc}`, `probe-v5.{json,stdout,stderr,rc}`, `probe-v4-at-base.{json,stdout,stderr,rc}`, `d1-old-counter.{json,stderr,rc}`, `selftest-v5.{stdout,stderr,rc}`, `selftest-v5-rerun.{stdout,stderr,rc}`, `selftest-agreement-v2.{stdout,stderr,rc}`, `selftest-forgery.{stdout,stderr,rc}`.

Analysis files: `sha256-instruments-at-4bda.txt`, `pins-check.txt`, `compare.txt` (full field comparison output), `compare.py` (the comparison script, read-only over lane files and seat receipts), and this `repro.md`.

Scratch `$S` (clone, base clone, work dirs) is removed after this file was written.
