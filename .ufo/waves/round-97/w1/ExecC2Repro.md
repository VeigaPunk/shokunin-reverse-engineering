# ExecC2Repro — independent reproduction of R97-C2 (round 97, attempt 1)

Seat: ExecC2Repro (executor). Lane repo: /home/vgpnk/Projects/shokunin/kaidoku-shokunin.
Landing L = 867ed98d85f45a18265441c1760386ef353b3d43. Base = 2a54af0785f75d50912e1136443c8e78e62adf27.
Clone: /fast/scratch/hyaku/kaidoku-r97/ExecC2Repro/clone (git clone --shared, checkout --detach L; toplevel verified equal to $S/clone before any run).
No REA call was made. No tooling was installed (system Python 3.14.8 used; no install/upgrade needed).

## Runs (all from clone cwd unless noted)

1. Frozen C (depth v4 @L):
   `python3 -I -B tools/round-97/depth-blocks-v4.py --root . --rev 867ed98d85f45a18265441c1760386ef353b3d43 --expect-blocks 36 --shape-from 36 --expect 'blocks 36, resolved 36, required-shaped 1/1' --json-out $S/c2c.json`
   rc=0, label `blocks 36, resolved 36, required-shaped 1/1`. Receipt byte-identical (JSON-equality) to L1 `c2-depth-v4-at-867ed98d85f45a18265441c1760386ef353b3d43.json` (mine==l1: True, field-for-field).

2. Frozen D (craft-citation-v2, after manifest @L):
   `python3 -I -B tools/round-97/craft-citation-v2.py --root . --manifest .ufo/waves/round-97/manifests/block36-after.json --block 36 --rev 867ed98d85f45a18265441c1760386ef353b3d43 --json-out $S/c2d.json`
   rc=0 (`ok`), receipt JSON-equal to L1 `c2-block36-at-867ed98d85f45a18265441c1760386ef353b3d43.json` (True).

3. Frozen E (craft-citation-v2, junk manifest @L):
   `python3 -I -B tools/round-97/craft-citation-v2.py --root . --manifest .ufo/waves/round-97/manifests/block36-junk.json --block 36 --rev 867ed98d85f45a18265441c1760386ef353b3d43 --json-out $S/c2e.json`
   rc=1 (`failing`), 4 criterion-not-restated failures; receipt JSON-equal to L1 `c2-block36-junk-at-867ed98d85f45a18265441c1760386ef353b3d43.json` (True).

4. Decoy proof: `python3 -I -B tools/round-97/depth-blocks-v4.py --decoy-proof --json-out $S/decoy.json`
   rc=0, `{"control_killed": true, "decoy": {"v3_accepts": true, "v4_accepts": false}, "real": {"v3_accepts": true, "v4_accepts": true}}`.

5. Selftests: `python3 -I -B tools/round-97/craft-citation-v2.py --selftest --work $S/cc` rc=0 (11 cases, 0 failures); `python3 -I -B tools/round-97/depth-blocks-v4.py --selftest` rc=0 (8 cases, 0 failures).

6. Base-side depth v4 (`--expect-blocks 36`, expect block 1 / 36-absent):
   First attempt at worktree checkout 2a54af0 inside the clone failed rc=2: `tools/round-97/depth-blocks-v4.py` does not exist at that rev (base has only tools/round-96; confirmed via `git ls-tree 2a54af0 tools/`).
   Corrected run (tool reads SKILL.md at `--rev`, so running the L tool against the base rev is the faithful before-side):
   `python3 -I -B tools/round-97/depth-blocks-v4.py --root . --rev 2a54af0785f75d50912e1136443c8e78e62adf27 --expect-blocks 36 --shape-from 36 --expect 'blocks 36, resolved 36, required-shaped 1/1' --json-out $S/c2c-base.json`
   rc=1, label `blocks 35, resolved 35, required-shaped 0/0`, `met_target=false`, block 36 absent (35 blocks). Matches the expected before-side.

## Verdict
All frozen commands reproduced exactly: C rc=0, D rc=0, E rc=1, decoy control_killed=true, both selftests green, base depth v4 rc=1 with 35 blocks. Own receipts are JSON-equal to the L1 landing receipts for C, D and E. No discrepancy found.

## Files
Report: .ufo/waves/round-97/w1/ExecC2Repro.md
Receipts copied to .ufo/waves/round-97/w1/ExecC2Repro/: c2c.json, c2d.json, c2e.json, decoy.json, c2c-base.json.
L1 receipts compared (not overwritten): .ufo/waves/round-97/l1/scores/c2-depth-v4-at-*.json, c2-block36-at-*.json, c2-block36-junk-at-*.json.

## Risks / blockers
None. Scratch at /fast/scratch/hyaku/kaidoku-r97/ExecC2Repro (298G free at start); clone left at L.
One methodological note: the literal "checkout base then run depth v4" cannot execute because the tool is absent at the base rev; the `--rev`-based before-side run above is the equivalent check and gave the expected rc=1.
