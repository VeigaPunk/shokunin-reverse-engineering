# MutationC1 — fresh-mutant battery N1–N10 (round 96, wave w1)

Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` at HEAD `3baac2ef4b9b2830d299125b8184ca06d9e6584d`
(disclosed supersession of declaration `e4d1f7de9deae83e6d5f78d2d7f0157196002af0`).
Method: per mutant, a fresh `git clone --shared` of the lane under scratch
(`/fast/scratch/hyaku/kaidoku-r96/MutationC1/clone`), exactly one find/replace applied
(find asserted to occur exactly once, mirroring `build_copy` discipline), detector runs,
clone discarded. The lane tree was never mutated; every detector wrote only under scratch.

## Detector baseline (pristine bytes, required green)

```
python3 -I -B tools/round-96/kill-rule-v2.py --root . --work <scratch>/w-base \
  --mutants .ufo/waves/round-96/mutants.json --fixtures .ufo/waves/round-96/forgery \
  --prefix forge --expect 'repaired 12 of 12; wrong 0; unsafe 0; intact 6 of 6; far-refused 12 of 12; fresh-roundtrip 2 of 2' \
  --json-out <scratch>/receipts/base-killrule.json
```

- exit **0**, label `mutants killed 10 of 10; forgeries refused 10 of 10; negctl refused 3 of 3; probe consistent 1 of 1; honest accepted 1 of 1`, met True, `identity_not_killed true`, no red honest legs. Receipt: `receipts/base-killrule.json`.
- First baseline attempt used the C1 **score** label as `--expect` and was red — pilot error,
  superseded by the run above; the correct `--expect` is the battery FROZEN_LABEL (confirmed
  against committed `l1/scores/c1-at-decl-worktree.json` and the fixture-baked labels).
- Clean-mutant method note: for counter/probe/rule mutants the harness run uses the pristine
  lane as `--root` with the mutated module passed via `--counter`/`--probe` (absolute path) or
  run as the rule binary itself — the same semantics as the rule's own `build_copy` (mutant
  copy, pristine pins). Mutating the tree in place additionally trips K-forgeries via
  counter-pin mismatch against the fixture-baked pins (observed on N1's first run and noted
  per-row below); it is a legitimate tree-tamper kill but not the mutant's behavioral signal.

## Verdict table

| mutant | file (all `tools/round-96/`) | detector run | exit | verdict |
|---|---|---|---|---|
| N1 resolve_rev reverts to hex-only input | `stop-boundary-repair-battery-v6.py` | v6 `--selftest`; kill rule (clean: `--counter` → mutant) | selftest 0; kill rule **1** | **KILLED** — kill rule honest arm red, K-dmain `pos` exit 1 (receipt `head=None` → fail-closed `head-not-bound`); all other legs green. Selftest green 13/13 (blind: no symbolic-rev case). Tree-level run also red (K-dmain + K-forgeries pin artifact). Receipts: `receipts/N1-killrule-clean.json`, `receipts/N1-killrule.json` |
| N2 count_problems drops bool rejection | `stop-boundary-repair-battery-v6.py` | v6 `--selftest`; kill rule (clean); bool-count probe | selftest 0; kill rule **0** | **SURVIVED** — full frozen score green with the binding dropped; a met-False receipt carrying a bool count (`scored: True`, self-consistent label) is refused on pristine (`counts-type:scored`) but **accepted** on mutated (`ok=True reasons=[]`). No fixture or leg feeds bool counts. Coverage finding. Receipts: `receipts/N2-killrule-clean.json`, `receipts/N2-boolprobe2.out` |
| N3 verify_receipt drops met-False direction | `stop-boundary-repair-battery-v6.py` | v6 `--selftest`; kill rule (clean) | selftest **1**; kill rule **1** | **KILLED** — selftest `verify-catches-met-lying: FAIL` (1 failure); kill rule `forgeries refused 9 of 10`, `forge-met-lying` **accepted** (`reasons=[]`). Receipts: `receipts/N3-selftest.out`, `receipts/N3-killrule-clean.json` |
| N4 main drops `receipt["head"]` | `stop-boundary-repair-battery-v6.py` | v6 `--selftest`; kill rule (clean) | selftest 0; kill rule **1** | **KILLED** — K-dmain `pos` exit 1 (`head-not-bound` fail-closed); selftest green 13/13 (blind: no main-level head case). Receipt: `receipts/N4-killrule-clean.json` |
| N5 c_fsync restores os.fsync before counting | `kill-rule-v2.py` | mutated rule run on pristine world | **1** | **KILLED (meta, self-observed)** — the tampered harness's own honest arm reports `K-fsync fsync_calls=0 ok=False` → `honest accepted 0 of 1` → met False → exit 1; all other legs green (`r95-battery-regression ok`). Receipt: `receipts/N5-killrule.json` |
| N6 `identity_not_killed = True` unconditionally | `kill-rule-v2.py` | mutated rule run (declared mutants); differential with killing-identity mutants file | in-suite **0**; pristine-rule probe **1** vs mutated-rule probe **0** | **SURVIVED in-suite; observed only by crafted probe** — declared-M0 run stays green (rc 0). With a mutants file whose M0 actually kills (forced selftest failure): pristine rule → M0 `killed=True`, `identity_not_killed=False`, met False, exit 1; mutated rule → receipt honestly records M0 `killed=True` but reports `identity_not_killed=True` → met True, exit **0**. No in-suite leg feeds a killing identity. Receipts: `receipts/N6-killrule.json`, `receipts/N6-probe-pristine.json`, `receipts/N6-probe-mutated.json` |
| N7 write_receipt uses `open(w)` again | `symlink-probe-v2.py` | kill rule (`--probe` → mutant); planted-link differential on the probe's own receipt | in-suite **0**; demo differential | **SURVIVED in-suite** — full frozen score green with the r95 writer restored; nobody in the suite plants a link at the probe's own `--json-out` (no probe selftest exists). Differential: with a symlink planted at the probe's own receipt path, pristine probe leaves the external victim intact (`sha256 297d0db4…`, `out.json` becomes a regular file via `os.replace`); mutated probe **clobbers the victim** (victim now contains the receipt JSON, `sha256 f5830127…`, `out.json` stays a symlink). First attempt was an invalid mutant (orphaned `except` → SyntaxError, crashed at import, victim untouched); discarded and redone with a compiling full-body replacement. Receipts: `receipts/N7-killrule.json`, `receipts/N7-planted-link-demo.txt` |
| N8 c_probe consistency `and` → `or` | `kill-rule-v2.py` | mutated rule run (declared mutants); stub-probe unit differential with a lying receipt | in-suite **0**; differential | **SURVIVED in-suite; observed only by unit probe** — honest probe is fully consistent under both predicates (rc 0). Stub probe writing `{verdict:"followed-symlink", met:true, victim_intact:true, receipt_valid:true}`: pristine `c_probe` ok=**False** (lie caught), mutated `c_probe` ok=**True** (half-lying receipt accepted). Receipts: `receipts/N8-killrule.json`, `receipts/N8-stubprobe-differential.txt` |
| N9 schema check skipped when counts is a dict | `stop-boundary-repair-battery-v6.py` | v6 `--selftest`; kill rule (clean) | selftest **1** (crash); kill rule **1** (crash, no receipt) | **KILLED** — `verify-catches-unlabelled-counts` crashes with `KeyError: 'fresh_scored'` (the exact crash the typed schema exists to prevent); kill rule crashes the same way on `forge-unlabelled` in K-forgeries, stderr recorded. Receipts: `receipts/N9-selftest.out`, `receipts/N9-killrule-clean.stderr` |
| N10 legacy rule counts M10 as killed | `legacy-kill-rule.py` | mutated legacy rule full run vs committed before-side receipt | **1** (1 is the by-design before-side exit) | **OBSERVED only by receipt-diff** — mutated rule reports `r95-rule mutants killed 6 of 10` with M10 `killed=True` while `checks_all_ok=True` (forced); committed `pre/c1-legacy-rule-at-base.json` (rule sha `2192da45…` matches HEAD bytes) records **5 of 10**, survivors M10/M2/M3/M4/M6. Exit code unchanged (1 either way); no r96 instrument runs the legacy rule, so nothing automated observes the tamper. Receipt: `receipts/N10-legacy.json` |

## Byte hashes (sha256)

Pristine (HEAD): v6 `7d7d559ac144eda6d163dd1d9ab26ed95ac089e18ccbb029bd91ae4277e46c06`;
kill-rule-v2 `3b8c7583c9c9d6aa9e42a6a8e718d16bac4371a4fbdf7fd345f0190b1dc9bb5f`;
symlink-probe-v2 `67b74a4b9f884464efc8021f584d6eeb4447b13e65f3882a41025ff58dfa11ec`;
legacy-kill-rule `2192da45bdf581cf1272c9a8c58e0a0059b26b591c9d1a7bf1395c3838d23939`.

Mutated: N1 `29b58bf3c068b9f9f3aee25bb50aaec77d2081fa8976f1fceda68511bac09601`;
N2 `aab3ee1e99bdbc7aace96ac3045e8fb806d90d3aa0afc66a4f06a99a5c274a4f`;
N3 `1cbd1f85f3aab6bc0ac30394a9bb0fc9c8ee59b3e6a4ba44eb36b8609ae57631`;
N4 `297d8de87daf631cf83e97c2cb6d4c6d6142536e985328666e31ed75248e272f`;
N5 `0a0c5bf3da4b8f6f6bd9b27f6bf01d4777b1d5bad794cefe13eec49215160693`;
N6 `5b82d29cfe9997af946b1d62767581d6abf9938e642a841cce38107d9038ec49`;
N7 (valid) `b3735088a2b5e0814dd88f2f71285f0f77bda92869923050ea2126fe27db79d1`;
N8 `3353293fa4641b3b15b003ffe5a28faec3ef251e5cc4f513bdeaeb62f243bebf`;
N9 `7154db11874ecdf97711de026203997ccd1ba87494f9e1cef913e3956666bfe6`;
N10 `019bd3245f80e758acf73408b2d682a3a95f8abeb1aca8587471ed6d5054ae8d`.

Diffs: `diffs/N1-v6-resolve-rev-hex-only.diff` … `diffs/N10-legacy-m10-forced-killed.diff`
(N7 diff is the valid v2 mutant).

## Incidental findings (fresh, out-of-band)

1. **cwd-dependent honest leg in kill-rule-v2.** The rule invokes the r95 regression battery
   with a relative `--honest-dir .ufo/waves/round-95/l1/scores`. The identical command from a
   cwd other than the tree root turns that leg spuriously red (`honest accepted 0 of 1`,
   exit 1) — deliberately reproduced with the pristine rule and pristine world from
   `/home/vgpnk` (`receipts/cwd-artifact-demo.json`: only `r95-battery-regression` red), while
   the same command from the tree root is green (`receipts/base-killrule.json`). The frozen
   counting command is safe only where the operator's cwd equals the tree root.
2. **Tree-level counter mutation trips K-forgeries via pins.** With the mutant bytes in place
   at `--root`, `counter_pins` hashes the mutated counter while the forged fixtures bake the
   pristine sha → every round-96 forgery gains `counter-pin-not-bound` and exact-refusal
   fails. Legitimate extra kill signal for tree tamper (the pins gate), but it masks the
   mutant's behavioral signal; per-mutant scoring should keep the harness's own
   copy-mutant/pins-from-root split.
3. **Selftest blind spots (recorded, not defects alone):** v6 `--selftest` has no symbolic-rev
   (HEAD) case (N1) and no main-level head-binding case (N4) — both kill only at kill-rule
   level via K-dmain.

## Score against ticket expectation

Expected killed: N1–N4, N7–N9. Actual: N1, N3, N4, N9 killed as expected; **N2, N7 survived**
(both are unobserved bindings — bool-count schema and the probe's own-receipt writer);
N5 self-observed as predicted (meta); N6, N10 survived in-suite and are observable only by
the crafted probes recorded above. Net: 4/8 expected kills confirmed cleanly; 2 coverage
findings (N2, N7); 3 meta-mutants characterized (N5 self-detected, N6/N10 probe/diff-only).
