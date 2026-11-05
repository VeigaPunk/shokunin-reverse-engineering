# SentinelWrite — receipt write-path security review (round 95, R95-C1)

Scope: `tools/round-95/stop-boundary-repair-battery-v5.py` (writer `write_receipt`, `verify_receipt`,
`main`) and `tools/round-95/symlink-probe.py`, at declaration commit
`4bda1d1dd3788973f10e61212b70df18b3b14ea0`, read from a clone under scratch (`git clone --shared`,
`checkout -q 4bda1d1d`). Lane not patched. Python 3.14.8. strace at `/usr/bin/strace`
(already on host; nothing installed).

Severity scale: NONE, LOW, MED, HIGH.

## Findings

| # | Item | Severity | Evidence (command, exit) |
|---|------|----------|--------------------------|
| a | Symlinked receipt parent directory | NONE (residual, out of stated scope) | `exp_symlink.py` case A: exit 0; receipt lands in the real dir the link names |
| b | Pre-created receipt path is a symlink to a victim | NONE | `exp_symlink.py` case B and B2: exit 0; victim unchanged, target a regular file, dangling target not created. Probe leg: `victim_intact true` |
| c | mkstemp name predictability and O_EXCL | NONE | `exp_symlink.py` case C-excl: exit 0, `FileExistsError`, victim intact, no receipt written. strace: `O_RDWR|O_CREAT|O_EXCL|O_NOFOLLOW`, mode 0600 |
| d | Writes outside `--work` / `--json-out` dir (v5 honest run) | NONE | `strace -f -qq -e trace=openat,rename,renameat,renameat2,unlink,unlinkat`; honest run rc 0. 859 rename/unlink and 909 write-flag opens; 0 outside `work/`, `out/`, `tmp/` (the `/dev/null` write opens excluded) |
| e | Secret-shaped strings in receipts | NONE (premise mismatch, see below) | `grep -ci` for `PATH=`, `HOME=`, token, key, secret, password, session, cookie: 0 each in the lane's `l1/scores/*.json`, my honest and probe receipts. Positive control `grep -c sha256` on the lane json: 22 |
| f | Probe writes outside its `--work` | NONE for the probe's victim and writer legs; LOW for the probe's own `--json-out` (below) | probe strace: 79 write-flag opens and 1 rename, 0 outside `probe-work/`, `probe-out/`. Separate test `exp2`: planted symlink at `--json-out` followed, victim overwritten |

### Finding detail

**(a) Symlinked parent directory — NONE within the stated scope.** `write_receipt` calls
`mkstemp(dir=dirname(abspath(path)))`. If the operator-named directory is a symlink, the temp file
and the receipt land in the link's target directory (exp case A: `landed_in_real=['receipt.json']`).
That is path resolution of the path the operator passed, not an escape from it. An attacker who can
swap a parent directory mid-run is the "parent-dir swap" the claim names out of scope. There is no
O_NOFOLLOW on directory components, and a check-then-use race exists there in principle
[INFERENCE, not exercised].

**(b) Symlink at the receipt path — NONE.** `os.replace(tmp, path)` is `rename(2)`, which replaces the
directory entry and does not write through it. Confirmed: victim bytes unchanged, target becomes a
regular file with the receipt JSON, no leftover `.tmp`. A dangling symlink to a nonexistent outside
path is replaced and the outside path is not created.

**(c) mkstemp — NONE.** Temp name is `<basename>.<8 random chars>.tmp`. The strace shows
`O_RDWR|O_CREAT|O_EXCL|O_NOFOLLOW` with mode 0600. The random suffix's RNG seeding was not read
[INFERENCE: CPython tempfile draws from a urandom-seeded PRNG]. Experiment C monkeypatched the name
to a fixed value and planted a symlink at it: `mkstemp` raised `FileExistsError`, the victim was
untouched, and no receipt was written. Fail-closed, not retried into the victim.
Observed side effect: receipts are now mode 0600 (v4 mode not measured). This is a tightening, not a
finding.

**(d) Write scope on the honest v5 run — NONE.** Run in the clone with `--work` and `--json-out`
in separate scratch dirs and `TMPDIR` under scratch, `--rev` as the frozen commit. Honest-run stdout:
`selfverify ok=True reasons=0` and `repaired 12 of 12; wrong 0; unsafe 0; intact 6 of 6; far-refused 12 of 12; fresh-roundtrip 2 of 2 met True exit 0`.
All write-capable opens and renames go to `work/`, `out/` (receipt temp then rename) or `tmp/`. The only
other write-flag open is `/dev/null`.

**(e) Secret-shaped strings — NONE, with a premise mismatch.** Counts were 0 for every pattern in every
receipt set checked. Premise mismatch: at `4bda1d1d` the only files under `.ufo/waves/round-95/l1/scores/`
are the two `s320-open2-fetch{1,2}.html` files. The `*.json` receipts the claim names
(`honest-pos.json`, `c1-*.json`) are untracked in the lane working tree and not committed. Counts above
are for the untracked files, read-only. The repair helper's `_clean_env` sets `HOME` to `tempfile.gettempdir()`;
that value reaches the child's environment only and is not written into receipts.

**(f) Probe write scope — NONE for the legs it exercises; LOW for its own receipt.** The probe's victim,
`<json-out>.tmp` symlink and writer run all stay under `--work`. Its own receipt is written by
`open(args.json_out, "w")`, which follows a symlink at that path. Experiment exp2: victim
`victim-dir/victim.txt` planted, `pr.json` symlinked to it, probe run exit 0, victim overwritten with the
probe's JSON (680 bytes). Impact: needs an attacker who can plant a link at the operator-chosen
`--json-out` path. The writer under test is hardened (case B and probe leg); the probe, which tests this
exact class, is not. Remediation: route the probe's own receipt through the same `mkstemp` + `os.replace`
writer. Not patched (lane is read-only for this seat).

## Additional observations (not in the requested list)

- `verify_receipt` re-opens the receipt path after `os.replace` rather than the fd it wrote, so
  self-verification is not a boundary against a writer with access to the output directory
  [INFERENCE from code reading; not exercised]. Severity LOW. The claim's named limits already say
  it does not authenticate provenance.
- `resolve_rev` passes `--rev` into `git rev-parse --verify`, after a `[0-9a-f]{6,64}` regex. Not a
  write surface. NONE.

## Overall

No HIGH or MED findings. The v5 writer's receipt path is sound on the tested cases: symlinks at the receipt
and `.tmp` paths are not followed, the temp is O_EXCL|O_NOFOLLOW, and writes stay in scope. The only LOW
item with a demonstrated effect is the probe's own `--json-out` write (f).

## Files written (seat directory)

- `security.md` (this file)
- `exp_symlink.py` — experiment script (a, b, c, d-fail)
- `exp-symlink-output.txt` — its output, rc 0
- `honest.stdout`, `honest.stderr`, `honest.rc` — honest v5 run (rc 0)
- `honest-receipt.json` — honest v5 receipt (mode 0600)
- `strace-honest.txt` — strace of the honest run (1.4 MB)
- `probe.stdout`, `probe.stderr` — probe run on v5 (rc 0)
- `c1-symlink-v5.json` — probe receipt (`victim_intact true`, `receipt_valid true`)
- `strace-probe.txt` — strace of the probe run (452 KB)
- `probe-jsonout-symlink-victim-after.txt` — victim after the probe `--json-out` symlink test (f)

Scratch dir `/fast/scratch/hyaku/kaidoku-r95/SentinelWrite` removed. Also written: the report
`.ufo/waves/round-95/w1/SentinelWrite.md` (lane-relative Report trailer).

## Commands and exit codes

- `command -v strace` → `/usr/bin/strace`
- `git -C <lane> cat-file -t 4bda1d1d...` → `commit`; `git clone --shared -q` + `checkout -q 4bda1d1d` → ok
- honest v5 under strace → rc 0 (`honest.rc`); stdout tail `met True exit 0`, `selfverify ok=True reasons=0`
- probe under strace → rc 0; `victim_intact true`, `receipt_valid true`, `verdict hardened`, `writer_rc 1`
  (the identity no-op repair red-verdicts, as designed)
- `python3 -I -B exp_symlink.py` → rc 0
- probe json-out symlink test (exp2) → rc 0
- trace classification: `grep -E` and `grep -cvE` counts as above
- secret counts: `grep -ci` as above; positive control `grep -c sha256` → 22
