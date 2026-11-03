# ExecControls — R65-C1 control arms (w1)

All five control arms of the frozen `tools/round-65/jsc-closure-matrix.py` (sha256 79a4dca4…) ran with the predicted outcomes; no instrument defect found. Commands, exits and one-line verdicts: `.ufo/waves/round-65/w1/ExecControls/findings.md`; raw receipts in the same directory (`selftest.txt`, `donothing.json`, `pin-mutation.json`, `cache-present.json`, `cache-clean.json`, `census-a/b/c.json`, `census-ab-compare.txt`, `census-ac-compare.txt`). Scratch `/fast/scratch/hyaku/kaidoku-r65/ExecControls` deleted. No full matrix run was made (executor's move).

- A selftest: exit 0, `SELFTEST CLEAN cases=34 failures=0`.
- B do-nothing: exit 1, `runs_matching: 0`; `cmp` with `.ufo/waves/round-65/l1/c1-before-donothing.json` exit 0 — byte-identical to the L1 baseline.
- C pin mutation: one `\x00` written at offset 100 of `d8-14.8.178.1/snapshot_blob.bin` in a scratch copy (pre `601efdc6…` → post `98c3f89b…`); `--manifest` exit 2 naming exactly `d8-14.8.178.1/snapshot_blob.bin`. Matrix not run on the mutated copy.
- D cache control: empty `__pycache__/x.pyc` in a scratch copy → `--manifest` exit 2 naming `jsc2js-src/View8/__pycache__` and `…/x.pyc`; after removal, exit 0 with `ok: true`.
- E census: repeated census on an unchanged 2-file tree equal (compare exit 0); after adding `c.bin`, compare exit 1 with `"added": ["c.bin"]`.
