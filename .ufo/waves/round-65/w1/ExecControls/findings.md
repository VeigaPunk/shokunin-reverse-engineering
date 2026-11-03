# ExecControls — R65-C1 control arms, round 65 w1

Tool: `tools/round-65/jsc-closure-matrix.py` (frozen, sha256 79a4dca40d2b37dc8d88711e9a95ec25e7d2e099bfd3ed52bb38bab77ff922c6).
Scratch: `/fast/scratch/hyaku/kaidoku-r65/ExecControls` (deleted after the pass). Receipts in this directory.
No full matrix run was made (executor's move).

## A — selftest
```
TMPDIR=$S python3 -I -B tools/round-65/jsc-closure-matrix.py --selftest > selftest.txt 2>&1
```
- exit=0; `SELFTEST CLEAN cases=34 failures=0`; 34 `PASS` lines, 0 `FAIL` lines (grep counts).
- Verdict: PASS — classifier/verdict/census/closure unit expectations all hold.

## B — do-nothing control
```
python3 -I -B tools/round-65/jsc-closure-matrix.py --skip-run --out donothing.json > /dev/null 2>&1
cmp donothing.json .ufo/waves/round-65/l1/c1-before-donothing.json
```
- exit=1; receipt: `runs_matching: 0`, `skip_run: true`, `exit: 1`.
- cmp exit=0: byte-identical to the L1 `c1-before-donothing.json`.
- Verdict: PASS — deterministic not-run emission matches the frozen baseline exactly.

## C — pin mutation (mutated scratch copy only; matrix never run on it)
```
cp -a --reflink=auto ~/.local/share/kaidoku-jsc $S/tc        # cp_exit=0
printf '\x00' | dd of=$S/tc/d8-14.8.178.1/snapshot_blob.bin bs=1 seek=100 conv=notrunc
python3 -I -B tools/round-65/jsc-closure-matrix.py --manifest --toolchain-root $S/tc \
  --probe .ufo/waves/round-64/inputs/probe-electron.jsc \
  --node ~/.local/share/fnm/node-versions/v24.21.0/installation/bin/node \
  --python ~/.local/share/kaidoku-jsc/venv/bin/python > pin-mutation.json 2>&1
```
- Pre-flip sha256 `601efdc639d9f439cca3d1274e0917ab28ee09d6870787d6052d8949fa73e24d` (= the pin); byte at offset 100 was `0x80`, so the `\x00` write is a genuine flip; post-flip sha256 `98c3f89bde717ce08d74c7dfe22de217d14ca9a478843c246fdd6df93e6a664b`.
- exit=2; `pin_mismatch: ["d8-14.8.178.1/snapshot_blob.bin"]` — names exactly the mutated file, nothing else.
- Verdict: PASS — the closure pin detects a single-byte mutation and names only it.

## D — cache control
```
cp -a --reflink=auto ~/.local/share/kaidoku-jsc $S/tc2        # cp_exit=0; pycache absent pre-copy
mkdir -p $S/tc2/jsc2js-src/View8/__pycache__; : > $S/tc2/jsc2js-src/View8/__pycache__/x.pyc
python3 -I -B tools/round-65/jsc-closure-matrix.py --manifest --toolchain-root $S/tc2 ... > cache-present.json 2>&1
rm -rf $S/tc2/jsc2js-src/View8/__pycache__
python3 -I -B tools/round-65/jsc-closure-matrix.py --manifest --toolchain-root $S/tc2 ... > cache-clean.json 2>&1
```
- Dirty run: exit=2; `cache_present: ["jsc2js-src/View8/__pycache__", "jsc2js-src/View8/__pycache__/x.pyc"]`; finding text `cache present 2: ...`.
- Clean re-run: exit=0; `"ok": true`, entries=30, no findings.
- Verdict: PASS — bytecode-cache presence blocks closure (exit 2) and removal restores it (exit 0).

## E — census arms
```
$S/tc3 = {a.bin "alpha", sub/b.bin "beta"}
python3 -I -B tools/round-65/jsc-closure-matrix.py --census census-a.json --toolchain-root $S/tc3   # exit=0, entries=2
python3 -I -B tools/round-65/jsc-closure-matrix.py --census census-b.json --toolchain-root $S/tc3   # exit=0, entries=2
python3 -I -B tools/round-65/jsc-closure-matrix.py --compare census-a.json census-b.json            # exit=0 (equal)
printf gamma > $S/tc3/c.bin
python3 -I -B tools/round-65/jsc-closure-matrix.py --census census-c.json --toolchain-root $S/tc3   # exit=0, entries=3
python3 -I -B tools/round-65/jsc-closure-matrix.py --compare census-a.json census-c.json            # exit=1
```
- a-vs-b compare exit=0 (identical trees → equal). a-vs-c compare exit=1 with `"added": ["c.bin"]`, changed/removed empty (census-ac-compare.txt).
- Verdict: PASS — the census is stable across repeated runs on an unchanged tree and names exactly the added path when the tree grows.

## Summary
All five control arms behave as the R65-C1 predicate requires: selftest clean (34/34), do-nothing not-run emission exit 1 and byte-identical to the L1 baseline, single-byte pin mutation named precisely with exit 2, bytecode-cache presence refuses with exit 2 and clears on removal, census equal-when-unchanged and names the added file when changed. No defect found in the frozen instrument; nothing to report against it.
