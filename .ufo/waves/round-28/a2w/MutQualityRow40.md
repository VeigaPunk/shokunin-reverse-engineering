# MutQualityRow40 — mutation test of QUALITY row 40 in the round-28 counters

Seat `KaidokuR28a2.MutQualityRow40`. Scope: routed defect 8 of `corpus/lessons/round-27-verifier-spotcheck.md`, QUALITY row 40 only. Lane read-only; all mutation work in the sandbox clone `/fast/scratch/hyaku/kaidoku-r28/seats/a2w/MutQualityRow40/clone` (`git clone` of the lane at `9db24c9e`). Times are UTC, 2026-10-22. Installs: none.

## Verdict

- **Holds, thinly.** The C1 counter enforces row 40 with one green case, `green-identical-4byte-bodies-across-selectors` (`tools/round-28/c1-heldout-naming.py:530`). The mutant that makes the counter refuse byte-identical response bodies (M1) is killed by exactly that case, so the shipped case bites today. Observation.
- **Three of four mutants survive.** The green case bites only while the fixture keeps a byte-identical pair (M2), the C2 counter ships no look-alike case at all (M4), and the reused-run refusal has no case at all (M3). Observation.
- **Neither counter has a duplicate-envelope gate.** Row 40's own round-27 shape (two genuine runs, byte-identical envelopes) has no counterpart here: the committed data holds 61 runs with 61 distinct envelope sha256, so nothing refuses a shared envelope and nothing tests that. Observation.

## Where the rule lives

- `tools/round-28/c1-heldout-naming.py:14-17` (docstring): byte-identical response bodies for different selectors are legitimate and "are never refused: responses are keyed by their manifest entry, not by their bytes".
- The gate is `check_lookups` (`:212-256`): each response is checked against its own manifest entry (file, url, status, utc, sha256), never against another response's bytes. The reused-run refusal is `check_runs` (`:165-167`, "need exactly 1" call record per carrier).
- The green case is `:530`. The C2 counter (`tools/round-28/c2-filtered-flag.py:139-177`) has no such case: its only green case is `green-both-branches` (`:285`), about the `filtered` rule, not duplicates.
- Committed data (`python3 dup-probe.py clone`): c1 holds 375 response files, 285 distinct sha256, and **one sha256 shared by 91 files** (the empty 4byte result); c2 holds 231 response files, 231 distinct sha256; c1 envelopes 61 files, 61 distinct sha256, none shared.

## Method

Detector: `python3 tools/round-28/c1-heldout-naming.py --selftest` (21 cases) and `python3 tools/round-28/c2-filtered-flag.py --selftest` (17 cases), run in the clone with `TMPDIR=/fast/scratch/hyaku/kaidoku-r28/seats/a2w/MutQualityRow40/tmp`. Baseline on pristine bytes (18:26Z): C1 `selftest cases=21 failures=0` exit 0; C2 `selftest cases=17 failures=0` exit 0. Each mutant was applied to the clone's copy, measured, then the file restored from `pristine-c1.py` / `pristine-c2.py`.

## M1 — false refusal of byte-identical bodies (C1) — **KILLED**

Diff (`m1.diff`, in `check_lookups`): refuses a response when another selector's manifest entry carries the same sha256.

```
+        # MUTATION M1 (row 40 probe): treat byte-identical bodies as reused evidence
+        for ofile, om in sorted(manifest.items()):
+            if ofile == fname or "-" not in ofile or om.get("sha256") != m.get("sha256"):
+                continue
```

Selftest (18:28Z): `FAIL green-identical-4byte-bodies-across-selectors exit=1 want=0`; `selftest cases=21 failures=1`; exit 1. **Killing case: `green-identical-4byte-bodies-across-selectors`** (the only case that changed; the other 20 kept their expected exit). On the committed bytes (18:28Z, `m1-realdat.txt`) the mutant gives `runs_ok=60/61 rows_complete=96/187 tally_equal=1 entry_ok=1` against the pristine `runs_ok=60/61 rows_complete=186/187 tally_equal=1 entry_ok=1`: it would refuse 91 legitimate 4byte responses and destroy the measurement.

## M2 — the green case stops being a look-alike (C1) — **SURVIVED**

Diff (`m2.diff`, in the selftest fixture): the three 4byte bodies become byte-distinct, so the case named "identical bodies across selectors" no longer holds identical bodies.

```
-        state["db"]["4byte-%s-p0.json" % s] = empty4  # byte-identical bodies across selectors: legitimate
+        state["db"]["4byte-%s-p0.json" % s] = (empty4, empty4b, empty4c)[i]
```

Selftest (18:29Z): `ok green-identical-4byte-bodies-across-selectors exit=0 want=0`; `selftest cases=21 failures=0`; exit 0. **Survived.** No case verifies that the green case still contains a byte-identical pair.

## M3 — reused run no longer refused (C1) — **SURVIVED**

Diff (`m3.diff`, in `check_runs`): the "exactly one call record" refusal becomes "at least one".

```
-        if len(rs_) != 1:
-            reasons.append("%s: %d call records (need exactly 1)" % (name, len(rs_)))
+        if not rs_:
+            reasons.append("%s: %d call records (need at least 1)" % (name, len(rs_)))
```

Selftest (18:29Z): `selftest cases=21 failures=0`; exit 0. **Survived.** The behaviour is real (`python3 demo.py c1-reused-run <counter> clone`, 18:29Z, a fixture with a second call record for carrier k1, same envelope file, different `utc_start`): pristine prints `FAIL k1: 2 call records (need exactly 1)` and `runs_ok=1/2`, exit 1; the mutant prints `runs_ok=2/2 rows_complete=3/3 tally_equal=1 entry_ok=1`, exit 0. No shipped case plants a second call record.

## M4 — false refusal of byte-identical bodies (C2) — **SURVIVED**

Diff (`m4.diff`, in `count`): the same duplicate-bytes refusal as M1, keyed on the manifest sha256 (same four added lines, in `c2-filtered-flag.py`).

Selftest (18:29Z): `selftest cases=17 failures=0`; exit 0. **Survived.** The behaviour is real (`python3 demo.py c2-identical-bodies <counter> clone`, 18:29Z, a fixture where two selectors' openchain responses are byte-identical): pristine `responses_complete=3/3 entries=3 mismatches=0`, exit 0; the mutant prints `FAIL openchain-22222222.json: ... byte-identical to openchain-11111111.json (duplicate bytes refused)` and `responses_complete=1/3`, exit 1. The C2 selftest ships no look-alike case, so the false refusal is invisible to it.

## M1+M2 combined — **SURVIVED** (the row-40 hole)

M1 and M2 applied together (18:29Z): `selftest cases=21 failures=0`, exit 0, while the counter now refuses byte-identical bodies. The green case protects the behaviour only as long as the fixture keeps a byte-identical pair; nothing in the selftest holds that.

## Findings (coverage, not a change to the contract)

1. `tools/round-28/c1-heldout-naming.py:530` — the green case is not self-verifying: a fixture change that removes the byte-identical pair leaves the suite green (M2). One assertion that two fixture bodies hash equal would pin it.
2. `tools/round-28/c1-heldout-naming.py:165` — the reused-run refusal has no case; a second call record for one carrier is accepted by a mutant and refused by the pristine counter (M3).
3. `tools/round-28/c2-filtered-flag.py` — no green look-alike case at all, so a duplicate-bytes refusal there is invisible to the suite (M4).
4. Row 40's round-27 shape (two genuine runs, byte-identical envelopes, told apart by the call record) is not exercised by either round-28 counter; the committed data has no shared envelope sha256 to exercise it with. Unknown for the round-27 envelope case; not exercised here.

## Artifacts (all under `/fast/scratch/hyaku/kaidoku-r28/seats/a2w/MutQualityRow40/`, sha256)

`pristine-c1.py` 29c2b571ac97098ac90b6aefc2112306b8b816722fe25abb3d84e03f22eeb27c · `pristine-c2.py` 4fdf7db81c5e56b3dfe8232ae87b89e3094e047f979adb088550381095fd60ef
`m1-mutant.py` 55ae625cbf3e5a9bef94b68eae4c74bca2fbdbd4db109804b56764975e7a1ba5 · `m2-mutant.py` cb4d98cf36e989ca25f4371c1a9bdb13bc2e24dbda1a071c59ebef4b812932fd
`m3-mutant.py` b56bf0660ac798e270151e3e88e1a19d44e20df7b21c504015a38b3e57eb8cb7 · `m4-mutant.py` 929c7962ef25357caf1bba6c04022049466c9a3a2e7b1e00bd3390dc95103ab8
`m12-mutant.py` 5e2be9cf641cc2156435797fa8bca49a0e155cf5ccc4948fd6cc845962180adb · `demo.py` 4b1762d65c24ce82e08d29a0740b373a7011bea5b8c80030e24a72027fe1232e
`m1.diff` df0fc7694386ed85cad72e31a82b62fbd7250f450e310c3b7691b25e357ab338 · `m2.diff` 66dd290f426b501df6c5faa206a5353f3db303382ea3aaa108d953f3b4bcbd1c
`m3.diff` 155ad5571b6094ea512fef3a4c28c2e99bbbdcb354a8a2c22bc27c0a5ad8b9fc · `m4.diff` c03035459148b07ef8735a5b1a2593ca5121198903afc9d3209cd533d83d3248
`m12.diff` d35050b4fb12fe984a49751bcd556d8aa8ee312bba1e4d7dc116061828ede241 · `dup-probe.py` 8de1ca16e2c34177e95c3f58469eeb20088aaa6e5fb475aeac64223b8d77e7c4
`m1-selftest.txt` 315b1e0de6be6a465d91a725ad678b3af0e6ed0a5e706fc6a6552f1f2462e7b1 · `m2-selftest.txt` e346a027f149f94c0cc441818ee0fc8884e1f2a03a43855f1f6c98b0da6d332d
`m3-selftest.txt` e346a027f149f94c0cc441818ee0fc8884e1f2a03a43855f1f6c98b0da6d332d · `m12-selftest.txt` e346a027f149f94c0cc441818ee0fc8884e1f2a03a43855f1f6c98b0da6d332d
`m4-selftest.txt` d6dd57b1a59bf465321d19b9852a5090a774e5d0ab0c1e39cf16a3051f0f12fb · `restored-c1-selftest.txt` e346a027f149f94c0cc441818ee0fc8884e1f2a03a43855f1f6c98b0da6d332d
`restored-c2-selftest.txt` d6dd57b1a59bf465321d19b9852a5090a774e5d0ab0c1e39cf16a3051f0f12fb · `m1-realdat.txt` cd8cef5975a9eb74487ae440f01aa77aff7c4c21de233cf48c13cde4754b87fa
`pristine-realdat.txt` 598c5b0c00bb6ebb422ecce481fd2b8280e11747fb95144dcbdcd631226fb5f4

## Restoration and lane state

- Clone files restored byte-exact: after the last restore `sha256sum` gave `29c2b571…eeb27c` (C1) and `4fdf7db8…fd60ef` (C2), equal to the pristine copies and to the lane's own bytes; `diff -q` reports no difference.
- Both selftests on the restored clone: C1 `selftest cases=21 failures=0` exit 0, C2 `selftest cases=17 failures=0` exit 0.
- The lane was written only by this report. The lane's two counters still hash `29c2b571…` and `4fdf7db8…`. No git write, no jj command, no REA call, no network request was made.
- This seat changed no counter; whether the L1 turns findings 1-3 into counter cases is the L1's decision.
