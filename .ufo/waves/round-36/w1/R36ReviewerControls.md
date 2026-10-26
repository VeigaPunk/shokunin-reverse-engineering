# R36ReviewerControls — control-receipt re-derivation (round 36, wave 1)

Seat: R36ReviewerControls (leaf; no subagents). Date: 2026-10-26.
Scope: re-derive every frozen control receipt under `.ufo/waves/round-36/controls/` (c1-0..2, c2-0..3);
rebuild CTL-C1-1 and CTL-C2-2 in fixture repos and re-score. Frozen inputs consumed read-only:
base `cab59f221fe19726b5692bfa4d9a9679e96b8a73`, freeze `790561d4e3aca732a434081aa9573ec2fa5fd7d0`,
counters `tools/round-36/c1-counter.py` / `c2-counter.py`, carriers+before receipts+oracle at
`corpus/evidence/round-36/c1/`, control-receipts commit `6a870b9290e9566468d7d9e6d1b8308daf025b12`.

**Verdict: 7/7 controls reproduce. Every control exits 1 and fails on exactly its intended guard —
no control trips the kill rule, and none fails on an incidental check. No defect found.**

## 1. Agreement summary

| Control | Stored rev | Re-derivation method | Exit (stored / mine) | Receipt agreement |
|---|---|---|---|---|
| ctl-c1-0-do-nothing | `cab59f22` (lane base) | counter re-run at lane, read-only | 1 / 1 | IDENTICAL incl. revision (argv-normalized) |
| ctl-c1-1-no-sasquatch-pipeline | `104dd4a2` (scratch-only) | fixture rebuild | 1 / 1 | AGREE on every field; only `revision` differs (mine `a95bc1c61332`) |
| ctl-c1-2-forged-oracle-copy | `6a16267c` (scratch-only) | fixture rebuild | 1 / 1 | AGREE on every field; only `revision` differs (mine `7fb45516370d`) |
| ctl-c2-0-do-nothing | `cab59f22` (lane base) | counter re-run at lane, read-only | 1 / 1 | IDENTICAL incl. revision (argv-normalized) |
| ctl-c2-1-junk-count | `f5679b9c` (scratch-only) | fixture rebuild | 1 / 1 | AGREE on every field; only `revision` differs (mine `ba961abd6594`) |
| ctl-c2-2-delete-bad-pointers | `a7a9fdb2` (scratch-only) | fixture rebuild (required) | 1 / 1 | AGREE on every field; only `revision` differs (mine `3e9927dd58e2`) |
| ctl-c2-3-substitute-other-document | `94cd0035` (scratch-only) | fixture rebuild | 1 / 1 | AGREE on every field; only `revision` differs (mine `c7ec2a47ef89`) |

"AGREE" = full deep JSON comparison (dict/list/leaf walk) of stored vs rebuilt receipt after
removing `argv` (scratch paths) and `revision` (my fixture commits cannot hash to L1's scratch
commits). Zero field differences beyond those two keys. The five fixture revs are absent from the
lane repo (`git cat-file -t` → MISSING for all five; the four lane commits exist), confirming the
controls were scored in throwaway fixture repos, as the freeze protocol prescribes.

## 2. Intended-guard confirmation, control by control

All seven stored `.out` files record `exit=1`; my seven independent runs reproduced exit 1 and
byte-identical stdout summary lines.

- **ctl-c1-0 (do-nothing at base)** — intended guard: a do-nothing state must not meet the target.
  Fails globally and per carrier: `carriers_unchanged=false` (no carriers.json at base),
  `oracle_frozen=false` for all four K (oracle.tsv only at freeze — note `oracle_files` 3/4/2130/2130
  still come from the freeze copy), `before_present=false`/`after_present=false` for all four, all
  seven bindings false. Nothing incidental: it is absent-everything, not a scorer artifact.
- **ctl-c1-1 (no-sasquatch pipeline, all bindings present)** — intended guard: a pipeline that never
  ran sasquatch must not count as an after. All bindings true (`S107` sourced, entry/PROVINCE row/
  coverage map row present), `carriers_unchanged=true`, `oracle_frozen=true` ×4, and every carrier's
  `before_*` checks true (genuine no-sasquatch receipts: gap=true, hits=0). Per carrier the ONLY
  failing checks are `after_sasquatch_gap=true` and `after_oracle_hits=0/<oracle_files>`; notably
  `after_evidence_id_ok=true` — so the refusal is on content (still reports the sasquatch gap,
  publishes zero oracle files), not on envelope validity. Rebuild confirmed this exactly:
  failing=[after_gap,after_hits] for K1..K4.
- **ctl-c1-2 (forged oracle-copy envelope)** — intended guard: a forged envelope must fail the
  rea-agents-6.5.0 evidence-id recomputation. All four carriers: `after_present/subject/operation ok`,
  `after_sasquatch_gap=false`, `after_oracle_hits == oracle_files` (3/4/2130/2130 — the forgery even
  matches the oracle), and the SINGLE failing check is `after_evidence_id_ok=false` on all four.
  This is precisely the claimed failure mode; nothing else fails.
- **ctl-c2-0 (do-nothing at base)** — intended guard: the base's known drift must be visible.
  `mismatches=3` = 2 unresolved pointers (`receipts-B/`, `ScoutSkillPlacement.md`) + O1 (stated
  116/116 vs observed 122/122); `guards_ok=false` via `unrepaired` = both base-unresolved pointers.
- **ctl-c2-1 (junk counts)** — intended guard: wrong stated counts must fail even with pointers kept.
  Only O1 among the 7 assertions fails (stated 999/999 vs observed 122/122); unresolved stays 2 →
  `mismatches=3`; `guards_ok=false`. O2/O3/O4/R1/R2/R3 still matching also confirms the observed
  values are stable across the C2 fixtures.
- **ctl-c2-2 (delete the bad pointers)** — intended guard: the deletion shortcut must be caught by
  the pointer-count floor, and by nothing else. `mismatches=0`, `unresolved=[]`,
  `assertion_mismatches=[]`, `pointers=32 < base_pointers=34` → `pointers_not_fewer=false` →
  `guards_ok=false` → `met_target=false`. The guard is the sole reason it exits 1 — exactly the
  subtle case the kill rule needs to reject "fix by removal".
- **ctl-c2-3 (substitute other documents)** — intended guard: substitution with resolving pointers
  to *different* documents must be caught by the same-document repair rule. `mismatches=0`,
  `unresolved=[]`, `pointers=34` (`pointers_not_fewer=true`), but `unrepaired` = both
  base-unresolved pointers → `guards_ok=false`. Sole failing mechanism is `unrepaired`.

## 3. How the rebuilds were done (exact commands and fixtures)

Scratch: `S=/fast/scratch/hyaku/kaidoku-r36/R36ReviewerControls` (removed after evidence capture;
`TMPDIR`/`HYAKU_SCRATCH` pointed into it). Counters invoked with `python3 -I -B`; xpin evidence-id
recomputation used the frozen `tools/round-27/xpin-attribute.mjs` from the freeze commit via node
v24.21.0 against `--pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`.

At-lane re-derivations (read-only; json-out to scratch):

```
python3 -I -B $L/tools/round-36/c1-counter.py --root $L --rev cab59f22… --freeze 790561d4… \
  --pkg65 …/rea-agents --json-out $S/rebuilt-ctl-c1-0.json        # exit=1
python3 -I -B $L/tools/round-36/c2-counter.py --root $L --rev cab59f22… --base cab59f22… \
  --json-out $S/rebuilt-ctl-c2-0.json                             # exit=1
```

Fixture repo A (C1): `mktemp -d fx.XXXX` under S, `git init -q`,
`git rev-parse --show-toplevel` verified equal to the fixture dir before the first commit,
`git fetch --no-tags $L main` (brings base/freeze/control commits; lane untouched),
`git checkout -B c1-1 790561d4…`. Binding docs reconstructed to the counter's frozen shapes:
PROVINCE.md `## Round-36 additions to Core` row (first cell contains `sasquatch`, row cites the
entry path); entry `corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md` with
`source: S107 …`; corpus/SOURCES.md S107 row (11 cells, opened `2026-10-26`, used-by = entry path);
corpus/README.md coverage-map row containing the entry stem. carriers.json/oracle.tsv/before.json
used verbatim from the freeze tree, so `carriers_unchanged`, `oracle_frozen` and
`before_evidence_id_ok` rest on the committed bytes.

- CTL-C1-1 branch: `after.json := before.json` (verbatim) for K1..K4 — commit `a95bc1c61332c03c5462607d758be8590a80f4ad`.
- CTL-C1-2 branch: `after.json :=` before-envelope with `normalized_result.files` replaced by the
  oracle rows (`firmware.bin_extract/<rel>` prefix, oracle sha256s) and `extraction_gaps=[]` — the
  same "forged oracle-copy" construction as the counter's own frozen selftest case; the stored
  `evidence_id` is left untouched so the recomputation must mismatch — commit
  `7fb45516370dfe3c4fab22cebfe115ba70754fd5`.

```
python3 -I -B $L/tools/round-36/c1-counter.py --root <fxA> --rev a95bc1c6… --freeze 790561d4… \
  --pkg65 …/rea-agents --json-out $S/rebuilt-ctl-c1-1.json        # exit=1
python3 -I -B $L/tools/round-36/c1-counter.py --root <fxA> --rev 7fb45516… --freeze 790561d4… \
  --pkg65 …/rea-agents --json-out $S/rebuilt-ctl-c1-2.json        # exit=1
```

Rebuilt decisive fields (identical to stored receipts in every field):
- c1-1 rebuild: carriers_matched=0, unchanged=true, bindings all true (entry_source_ids ["S107"],
  opened_source_rows ["S107"]); K1..K4 each: oracle_frozen=true, all before_* ok, after evidence/
  subject/operation ok, failing only `after_gap=true` and `after_hits=0/N` (N=3/4/2130/2130).
- c1-2 rebuild: carriers_matched=0, unchanged=true; K1..K4 each failing only `after_evidence_id_ok`,
  with `after_hits=N/N` and `after_gap=false` — i.e. the forgery fools every content check except
  the evidence-id recomputation.

Fixture repo B (C2): same init/toplevel-verify/fetch, branches at base `cab59f22…` (base tree
contains all 122 knowledge files, SKILL/PROVINCE/README/result.json — observed values therefore
match the stored controls' observed blocks exactly, as they do across ctl-c2-0..3):

- CTL-C2-1: Owned-axes coverage row `116/116 knowledge files mapped` → `999/999` (first occurrence
  only; nothing else edited) — commit `ba961abd6594c2d3ed9f1a93b4de9a72f05ecd86`.
- CTL-C2-2 (required rebuild): same row → `122/122` (restated to the observed count, which is what
  isolates the guard), cap row "pre-registered two-lane live battery on REA 6.5.0": remove
  " + `receipts-B/`"; SHONEN box 4: "(w1 `ScoutSkillPlacement.md`)" → "(w1)" — commit
  `3e9927dd58e2930f354e8b47ff614a7cecd06281`.
- CTL-C2-3: row → `122/122`; `receipts-B/` → `` `corpus/README.md` ``; `ScoutSkillPlacement.md` →
  `` `README.md` `` (both resolve at base; neither equals or suffix-matches the bad pointer) —
  commit `c7ec2a47ef89677ada08ca6f8e2c64c8a78b6043`.

```
python3 -I -B $L/tools/round-36/c2-counter.py --root <fxB> --rev <branch sha> --base cab59f22… \
  --json-out $S/rebuilt-ctl-c2-{1,2,3}.json                       # all exit=1
```

Rebuilt decisive fields (identical to stored in every field): c2-1 mismatches=3, pointers=34,
unrepaired both, O1 999/999 vs 122/122; c2-2 mismatches=0, pointers=32, `pointers_not_fewer=false`,
unrepaired both, no assertion/unresolved findings; c2-3 mismatches=0, pointers=34,
`pointers_not_fewer=true`, unrepaired both (substitutes point at other documents).

Supporting tree check: `git diff --stat cab59f22 6a870b92` = 50 files, 8933 insertions, 0
deletions — the control-receipts commit only ADDS round-36 tooling/evidence/plans, so every
self-assessment surface at control time is byte-identical to base (consistent with the identical
`observed` blocks across ctl-c2-0..3).

## 4. Tooling record

No tools installed or upgraded (operator authorization noted, unused): node v24.21.0, git 2.56.0
and system python3 were preexisting; pacman untouched; sasquatch/unblob not needed (controls
consume committed envelopes; no REA CLI run was required).

## 5. Bounds compliance

Lane mutations: none — only this report file written. Git in the lane: read-only only (log, ls-tree,
cat-file, merge-base, diff, show). Fixture repos: `init/fetch/checkout -B/add/commit/rev-parse`
exclusively, `rev-parse --show-toplevel` verified equal to the fixture dir before each first commit,
every later git call naming `-C <fixture>`. No frozen predicate, counter, carrier, oracle, envelope
or receipt modified. No subagents, no background jobs, no `agent://all`. Scratch removed at end;
all cited evidence is inlined above.

## 6. Residual risk and verification gaps

- The five stored fixture revisions exist nowhere anymore; agreement is proven at receipt level
  (every counter-produced field), which is what the kill rule consumes, but the exact byte content
  of L1's scratch fixture trees is unrecoverable. [INFERENCE] L1's fixtures were equivalent states;
  receipt-level identity across 7/7 is the strongest available evidence.
- ctl-c1-1's stored receipt shows `after_evidence_id_ok=true`, i.e. L1 put genuine REA no-sasquatch
  envelopes into the after slot; my verbatim `after := before` copy reproduces that signature
  field-for-field, which corroborates but does not prove L1 used the same construction.
- The xpin evidence-id rule and the counters were consumed as frozen; auditing xpin itself was out
  of scope for this seat.
- Not re-run here: REA extract-firmware before/after carrier runs and the K3/K4 AppImage digests
  (covered by the C1 evidence seats / harness receipts, not by the controls).

## 7. Conclusion

All seven frozen controls are honest and reproducible: each exits 1 for exactly its intended reason,
none meets its target, so the R36-C1 and R36-C2 kill rules were correctly NOT tripped and the
round's claimed data was scored against validated counters. No actionable defect found in scope.
