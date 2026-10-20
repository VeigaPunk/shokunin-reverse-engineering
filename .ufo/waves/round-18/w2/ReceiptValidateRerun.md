# HOLDS — receipt-validate re-run and mid-map tamper (R18 w2)

Seat: KaidokuR18.ReceiptValidateRerun (author-side advisory). Lane: `kaidoku-shokunin`.
Revision under test: `b2aad08ceeee8dd125ce0d316056d8bd766c7f94` (baseline `9011581`).
Read-only: no lane file was modified; all mutation happened under `/tmp`.

Verdict: **HOLDS**. `--selftest` exits 0 (18 cases); `--require-mid-maps` over the 15 r18
receipts exits 0 (15 valid, 0 findings, 5442 checks); a path-rewritten `/tmp` copy of a run
dir stays green, and flipping one hex digit in one copied mid map makes it exit 1 with
`mid_map_sha256_mismatch`. Two bounded strictness limits are recorded at the end; neither
falsifies the claim that mid maps are retained, digested and re-verified.

## Evidence identity (observation)

Tested bytes are the REV bytes, not a drifting worktree:

```
$ git show b2aad08…:.ufo/waves/round-17/tools/receipt-validate.py | sha256sum
70672eb3bd0c06e93ca439a31558f35ab7f76bd23aa74acd026290972553d145  -
$ sha256sum .ufo/waves/round-17/tools/receipt-validate.py
70672eb3bd0c06e93ca439a31558f35ab7f76bd23aa74acd026290972553d145
(pins.py REV == worktree == 9e9c72507de429c913891c65ffeafda9a686fee532d6a9dcfcd42b8092639fe0)
identical_to_REV=37 differing=0   # 15 receipt.json + 22 pins/mid-*.json
```

`producer.json` records the same validator digest (`…\.ufo/waves/round-18/runs/calib-aether/producer.json:12`),
so the tool identity the runs were produced under is the tool re-run here.

## Commands and exit codes (observation)

1. Selftest — exit 0:
```
$ python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py --selftest
SELFTEST: CLEAN cases=18
EXIT=0
```
The 18 cases include the mid-map axis specifically — `carrier_mid_map_green`,
`carrier_mid_map_tampered_red`, `carrier_mid_map_forged_red`,
`carrier_r17_shape_green_without_flag`, `carrier_flag_r17_shape_red`,
`carrier_flag_mid_map_green`, `carrier_flag_checks_absent_red`,
`carrier_entries_forged_red_{no_flag,flag}` — so the selftest is not vacuous here
(`receipt-validate.py:884-888` asserts exit 1 *and* the `mid_map_sha256_mismatch` code).

2. All 15 receipts, `--require-mid-maps` — exit 0:
```
$ /bin/bash -c 'python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py \
    --require-mid-maps .ufo/waves/round-18/runs/*/receipt.json'
EXIT=0   counts={'invalid': 0, 'receipts': 15, 'unreadable': 0, 'valid': 15} exit 0
find .ufo/waves/round-18/runs -name receipt.json -type f | sort | xargs … --require-mid-maps
EXIT=0   total checks 5442
```
Per receipt: 1-3 map-bearing `pin_checks` (22 total), every `analyze` step carries ≥1 map-bearing
check (3,2,2,1,2,1,1,1,1,1,2,1,1,2,1), 360-372 checks each. Nothing was skipped by the flag —
`receipt-validate.py:570-585` would have reported `mid_checks_absent`/`mid_map_missing` otherwise.

3. Tamper in a `/tmp` copy with rewritten paths — exit 1, required code present:
```
$ cp -a …/runs/calib-aether /tmp/rvr-calib-aether   # receipt paths rewritten src→/tmp
$ … --require-mid-maps /tmp/rvr-calib-aether/receipt.json     → EXIT=0 (control, green)
$ python3 - <<'EOF'   # flip first hex digit of one entry sha256 in pins/mid-2.json
EOF
$ … --require-mid-maps /tmp/rvr-calib-aether/receipt.json     → EXIT=1
{"code":"mid_map_sha256_mismatch","where":"$.steps.analyze.pin_checks[1]",
 "path":"/tmp/rvr-calib-aether/pins/mid-2.json",
 "recorded_sha256":"21d14b598c80652e7c4f5183b84026a0aae058756c7a740f24c9d099acde80f9",
 "actual_sha256":"0912eebf8540ad94f45512e5243fee35360ff8ff7ec012ee722b1a8f133c25ee"}
{"code":"mid_map_compare_mismatch","where":"$.steps.analyze.pin_checks[1].equal","recorded":true,"recomputed":false}
{"code":"sha256_mismatch","where":"$.steps.analyze.pin_checks[1].map", …}
```
A crude append-tamper (`printf tampered >> mid-2.json`) likewise gives exit 1 with
`mid_map_sha256_mismatch` plus `mid_map_unparseable` ("Extra data: line 767 column 1").

4. Flag discrimination on real r18 content (negative control) — the flag is load-bearing:
```
stripped map_path/map_sha256 from the s1246-swiss-methods copy
$ … /tmp/rvr-shape/receipt.json                    → EXIT=0  codes []
$ … --require-mid-maps /tmp/rvr-shape/receipt.json → EXIT=1  codes ['mid_map_missing']
```

5. Two harder forgeries, both caught (observation):
```
consistent forgery (map entry sha→0*64 AND receipt map_sha256 updated to match) → EXIT=1
  mid_map_compare_mismatch $.steps.analyze.pin_checks[1].equal   True -> False
  mid_map_compare_mismatch $.steps.analyze.pin_checks[1].changed [] -> ['…/golang/go1.16.0.json']
shrunk map (one entry dropped, digest AND entries count forged consistently 152→151) → EXIT=1
  mid_entries_mismatch  recorded 151 / pins_pre_entries 152
  mid_map_compare_mismatch .equal True->False ; .missing []->['…/golang/go1.15.0.json']
```
The shrink case is the one the comments claim is closed (`receipt-validate.py:483-488`: a
verdict-only entry "cannot shrink the pin set"), and it is: the forged `entries` is compared
against `len(pins_pre.entries)` independently of the map's own length.

6. Exit-2 branch exercised on a genuinely absent path (observation):
```
$ … --require-mid-maps .ufo/waves/round-18/runs/run-log.txt/receipt.json
EXIT=2  status unreadable  (matches receipt-validate.py:646-651)
```

## Why the tamper finding is the right code (observation → code reading)

`verify_mid_maps` (`receipt-validate.py:453-586`) recomputes the map digest before parsing
(`:512-517`), then re-derives the recorded verdict with `pins.compare(pre, mid_map)`
(`:551-569`), and `check_binding` independently rejects any step whose recorded `equal` is not
`True` (`:197-203`). So digest, content and verdict are three separate commitments; the copy
rewrite only relocates `map_path`, which is exactly why green-before/red-after isolates the
tampered byte rather than a path move.

## Bounded limits (inference, with reproducing commands)

These are strictness observations beyond the routed R17-PINMAP ask ("retain mid maps (or their
digest)", `corpus/lessons/round-17-verifier-spotcheck.md:141-147`), not falsifications.

- **Map timing is not bound to the step window.** `started_at_utc`/`ended_at_utc` are
  presence-only (`receipt-validate.py:397-405`), and `taken_at_utc` is only compared
  map-vs-receipt (`:532-537`), never against the window; `monotonic_ns` is never read
  (`grep -n monotonic` → no logic hit). Reproducer: set `mid-2.json` `taken_at_utc` to
  `2020-01-01T00:00:00+00:00`, update the receipt's sha and `taken_at_utc` to match →
  `EXIT=0`, while the step window is `16:24:08Z–16:25:18Z`. Similarly, reversing the three
  `pin_checks` order → `EXIT=0`. Content cannot be forged without detection; the *claim that a
  map was taken mid-run* is not temporally checked.
- **No receipt-level digest manifest.** `predictions/SHA256SUMS` and `carriers/SHA256SUMS` cover
  predictions and carriers, not `runs/*/receipt.json`; the receipt is itself the commitment and
  is REV-committed (37/37 blobs identical). Consistency forgery therefore costs a visible Git
  diff, which is sufficient for this lane's threat model — stated so the guarantee is not
  over-read as provenance attestation.

## Harness note (observation, not a lane defect)

Under this session's tool shell, `runs/*/receipt.json` expanded to include the non-existent
`runs/run-log.txt/receipt.json` (mid-pattern `*` matched a regular file), producing exit **2**;
clean `/bin/bash -c` (5.3.20) and POSIX mode expand only real directories → exit **0**. Any
recorded command should enumerate with `find … -name receipt.json -type f` so the reproduction
does not depend on the caller's glob implementation.

## Reproduction blocks

```
R=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
cd $R
python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py --selftest                       # 0
find .ufo/waves/round-18/runs -name receipt.json -type f | sort | \
  xargs python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps      # 0
rm -rf /tmp/rvr-calib-aether && cp -a .ufo/waves/round-18/runs/calib-aether /tmp/rvr-calib-aether
python3 -I -B -c "p='/tmp/rvr-calib-aether/receipt.json';s=open(p).read();open(p,'w').write(s.replace('$R/.ufo/waves/round-18/runs/calib-aether','/tmp/rvr-calib-aether'))"
python3 -I -B -c "import json;p='/tmp/rvr-calib-aether/pins/mid-2.json';d=json.load(open(p));k=sorted(d['entries'])[0];s=d['entries'][k]['sha256'];d['entries'][k]['sha256']=('0' if s[0]!='0' else '1')+s[1:];json.dump(d,open(p,'w'),sort_keys=True,indent=2)"
python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps /tmp/rvr-calib-aether/receipt.json  # 1 + mid_map_sha256_mismatch
```

## Handoff notes

No installs or upgrades were performed (nothing was missing; no pacman transaction was
attempted). No REA/Ghidra analysis, no carrier execution, no lane writes, no `jj`/git writes.
Main-agent gate: the two commands in `Reproduction blocks` lines 1-2 plus the tamper trio, and
`git status --porcelain .ufo/waves/round-18/runs` (expect empty).
