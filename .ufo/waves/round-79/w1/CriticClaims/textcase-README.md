# C1 counterexample — reproduce

Evidence copies, NOT production files. `textcase-target.py` is the declaration's
`tools/round-78/attack-gate.py` (pristine sha256 `4e4baf00…`) with **only** the three round-79
selftest case bodies replaced by source-text assertions (sha256
`d9145e9f60fbe2cebdf754b85465447b005b2ea5dde699a77f1b026893c5d57a`). `textcase-instrument.py` is the
frozen `tools/round-79/gate-mutation.py` with `TARGET_SHA256` patched to that digest.

Reproduce:

```bash
D=$(mktemp -d)                     # under your scratch root, not the lane
mkdir -p "$D/tools/round-78"
cp textcase-target.py "$D/tools/round-78/attack-gate.py"
git -C "$D" init -q
git -C "$D" add -A
git -C "$D" -c user.email=x@y.invalid -c user.name=x commit -qm fixture
python3 -I -B textcase-instrument.py --root "$D" --rev "$(git -C "$D" rev-parse HEAD)" \
        --work "$D/work" --battery --json-out "$D/c1-textcase.json"
python3 -I -B textcase-instrument.py --validate "$D/c1-textcase.json"
```

Observed (and recorded in `c1-textcase.json`): `mutants_total 8`, `killed 8`, `survivors 0`,
`declared_case_hits 8`, `pristine {cases 29, failures 0}`, `target_pin.matched true`, `ok true`,
exit 0; `--validate` `defects []`. `m03`, `m05`, `m08` are each `sole_detector true`. The three
cases call no gate function — they assert that an anchor literal is present in the file.
