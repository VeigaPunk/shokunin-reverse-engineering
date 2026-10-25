# Round-35 freeze status — candid setup-order defect

The intended one-command `freeze-integrity.py` check was run at the freeze commit and failed:

```
python3 -I -B tools/round-34/freeze-integrity.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --round 35 --rev f1ea3a6d079362c5aa7a09851d5749c75d773441 --claims .ufo/waves/round-35/claims-frozen.json
```

Output: `freeze-integrity: FAIL pins=4 changed=2 freeze=13d7a8152f7f`; exit 1. The reason is material: the final counter bytes changed after the first frozen claims object (that object's pins are for earlier counter bytes). The counter hash at the `f1ea3a6d` revision is C1 `018e96d0…`, C2 `3a23f3eb…`, while the gate reports C1 `d49ff16a…` and C2 `c0f37d21…` from earlier history. The later canonical freeze `claims-frozen.json` does contain the final hashes, but the round-34 gate's `--claims` path is honored only for input selection after it discovers its freeze; it discovers the first-added file matching the path (`13d7a815`), which is why it still rejects.

Census-start receipt and plan pins passed (the output includes `ok` for those paths). This does not make the gate CLEAN. The freeze setup therefore has `INSTRUMENT_REVISED` debt and C1/C2 were not scored before the final freeze. This receipt is an honest failure record; it does not repair or supersede the frozen claims. Subsequent work may proceed only as a falsification of these frozen targets, never as a re-freeze. The main claims require an honest stop if their unchanged instruments cannot be used at the frozen revision.
