# R41W2C2Rescore — artifacts index

Seat: R41W2C2Rescore (round 41, wave 2, falsify the landing). Lane root:
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. No lane file was written except this
directory and `../R41W2C2Rescore.md`. No VCS mutation in the lane; the only commit made
anywhere was inside a throwaway clone under scratch (artifact 11, fixture identity
`-c user.name=fx`).

## Commands (all from scratch dir; `S` = scratch, removed at exit)

1. Re-score, frozen counter, measured revision:
   ```
   python3 -I -B <LANE>/tools/round-41/c2-counter.py --root <LANE> \
     --rev e9a24d07256d1606f01aa4d2d65f74e649c5f3d4 \
     --freeze d764389e9cbe61b9d1b07538ff3bff02d50bb34f --json-out "$S/c2.json"
   ```
   exit 1. → `01-c2-rerun-at-e9a24d07.json`; comparison with the L1 receipt →
   `02-rerun-vs-frozen.txt` (only `argv` differs).
2. Independent observed-tuple recomputation (own reader, frozen feature definitions):
   `python3 -I -B indep-tuple-check.py <LANE>` → `04-indep-summary.json`,
   `05-per-carrier-tuples.json`; source `03-indep-tuple-check.py`.
3. One-hunk diagnostic patch of a **scratch copy** of the counter (lane untouched) →
   `06-patched-counter.diff`; run against the same root/rev/freeze →
   `07-c2-patched-receipt.json` (exit 0, `met_target` true).
4. Frozen counter selftest → `08-selftest.txt` (70/70 pass).
5. Cross-engine check: my observed tuple vs the counter's own `observed_features`
   on all 52 envelopes → `09-xengine-compare.py`, `09-xengine-output.json` (0 diffs).
6. Recorded REA parameters per carrier from `run.json` → `10-depth-check.py`,
   `10-depth-check-output.json` (52/52 exit 0; 15 at depth 1, 35 at depth 3, 2
   out-of-domain with no depth; recorded depth vs `--max-depth` argv: 0 disagreements).
7. Data-side repair attempt inside a `--shared` clone, then the frozen counter at the
   new commit → `11-datafix-sandbox-receipt.json` (exit 2 `frozen_path_changed` on
   `corpus/evidence/round-41/c2/heldout`).
8. Freeze-time interface citations (`git show` at `d764389`) → `12-read-chain-citation.txt`.

## sha256

```
38d9585f0ffe80068334ef56521e41c7206cebd35f147d4ddf3d89281140cba0  01-c2-rerun-at-e9a24d07.json
9ad1a0e94505c6767402bbd03724cc6aab6ae3252f9ee4a9e29c80bc79e5a6c3  02-rerun-vs-frozen.txt
c679e6136ef0ce36511a9323ee18ee20448e279862b71089a57df5cc94229f12  03-indep-tuple-check.py
6242874327196536df83554efe8b1b8d82207be839d0574184715542d79da97b  04-indep-summary.json
5a431fddc7194283160ab877034989dde9106b7e1c6ffb17e357a181c4fadbdb  05-per-carrier-tuples.json
12733efc333acacd3ac99ef9cf62021e87c69f6edae8840643e2751aeecb80e5  06-patched-counter.diff
a9d747e44fc61fc0307f181ef03dd610726332d823cbc8c858e3d975c16b17f1  07-c2-patched-receipt.json
f3db407a7763381d5a7b16c7c2ef5361b90a036f94c5855cc9cb301e00bb29a6  08-selftest.txt
644abeead3a994a1d7dbb976cf22e84491760c577ec73038b1c591496d8dbf88  09-xengine-compare.py
4e0295247db4da77915199929e91755e7cbbdd837a143cf3c4203076b854d0b7  09-xengine-output.json
5326f79e23ba69c8ed0a0ea02fde836b41792e9b08c92f2aeef88d93723645df  10-depth-check-output.json
0c418c342ef6a6e08b9d5dfdd4b6b75fb28df2119bdc6a9093d8256ee1f3252a  10-depth-check.py
44e6888accbfd9ef01f956db20db415a30fa530e5a7e2b9db4f6c01399dc6e05  11-datafix-sandbox-receipt.json
8c1ea86220dd1a7affb9dc4e6bed76fb176d8bf63f85a8576179b9eedf5fa2ea  12-read-chain-citation.txt
```

Inputs read (read-only, unchanged): `corpus/evidence/round-41/c2/heldout/manifest.json`
sha256 `7717df938128bab093b6e6817c032d18e9f351934f441639317702cf2114d91d`, 52 carriers,
52 envelope dirs, 21 classes.

No vendor firmware bytes are included anywhere here (C2 uses lane-built carriers only).
No tool installs were performed.
