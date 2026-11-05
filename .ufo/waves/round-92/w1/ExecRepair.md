# ExecRepair — R92-C1 candidate (window repair by packer verdict)

Seat: ExecRepair (executor), lane kaidoku, round 92 wave 1. Clone of the lane at the frozen
declaration commit `11f8606178dfd9e72001b31daf412c5463106a63`, candidate built only inside the
scratch clone; the lane was never written except this seat directory (receipts below).

## Result

Frozen counter `tools/round-92/stop-boundary-repair-battery.py`, unmodified, run exactly per the
frozen command:

```
cd "$S/clone" && TMPDIR="$S/tmp" python3 -I -B tools/round-92/stop-boundary-repair-battery.py \
  --root "$S/clone" --repair-cmd tools/round-92/upx-stop-boundary-search-repair.py \
  --work "$S/work" --rev "$(git rev-parse HEAD)" \
  --expect "repaired 10 of 10; wrong 0; unsafe 0; intact 5 of 5; far-refused 10 of 10" \
  --json-out .ufo/waves/round-92/w1/ExecRepair/c1-candidate.json
→ "repaired 10 of 10; wrong 0; unsafe 0; intact 5 of 5; far-refused 10 of 10 met True exit 0", rc=0
```

- Label: `repaired 10 of 10; wrong 0; unsafe 0; intact 5 of 5; far-refused 10 of 10`, `met_target
  true`, exit 0 — the frozen R92-C1 label, met on the first counter run after the probe-driven
  geometry fix (below). The counter was not tuned; its sha256 matches the claims.json pin
  (`63e9df431f5d7aeeca2bd5384efff36b4f2ebedfdc3ee71aaa250287fc9388bc`), and the imported v2
  instrument matches `f6ddb48b4d9cbd460002db68d834f909955e2c7d4e60d7ad85325ef4e66f1874`.
- Measured revision: `11f8606178dfd9e72001b31daf412c5463106a63` (declaration commit; the candidate
  is an untracked file in the clone, no tracked file modified — `git status --porcelain` showed
  only `?? tools/round-92/upx-stop-boundary-search-repair.py`).
- Receipt: `.ufo/waves/round-92/w1/ExecRepair/c1-candidate.json` (counts: scored 10, repaired 10,
  wrong 0, unsafe 0, refused 0, silent 0, intact 5, far 10, far_refused 10).
- Candidate sha256: `ce1b1769d56c1d90fcf2ee0800ca508476b45eddc2e8a6d7e2f01aa8d12a70c1`
  (byte-exact copy delivered as `.ufo/waves/round-92/w1/ExecRepair/upx-stop-boundary-search-repair.py`).

## Design, as implemented

`tools/round-92/upx-stop-boundary-search-repair.py` (Python 3, stdlib only, executable):

1. Loads `tools/round-91/upx-stop-boundary-repair.py` from ROOT (ROOT = three dirnames up from the
   candidate's own path) via importlib and reuses its `read_input`, `checked_target`,
   `write_atomic`, `Refused`; loads r87/r88/r90 from the same ROOT for the walk.
2. Runs the round-91 path unchanged (`rep91().repair(d)`): intact identity, block-0 law, break
   law. Any non-`stop-boundary` upstream refusal is re-raised → typed refusal, rc 2, no output.
3. On the round-91 `stop-boundary` refusal (input already red by `upx -t` inside that path):
   - locate last-block spots on the tampered bytes: always `blocks[-1]` of the
     `r90.longest_prefix` walk (for these carriers identical to the battery's `v2.layout` last
     block, e.g. xxd off 15455), plus a second reading — an unappended plausible header at the
     walk stop whose declared span overshoots the PackHeader — which never fires on the five
     counter carriers (retained for carriers without chain-end slack);
   - for each spot, try every `v` in `[stored-16, stored+16]` clamped to `0 < v <= sz_unc`,
     skipping `v == stored` (the input itself is already red), written as 4-byte LE `sz_cpr` at
     `block+4`; green = `/usr/bin/upx -t -q` rc 0 on a private copy under TMPDIR;
   - output only if EXACTLY ONE green `(offset, v)` exists across ALL probes, the output differs
     from the input only inside `[block+4, block+8)`, length unchanged, and a final `upx -t` on
     the output is green → atomic write, rc 0, one JSON stdout line
     (`{"block", "blocks", "class": "repaired", "delta", "derived_sz_cpr", "stored_sz_cpr"}`);
   - zero greens → typed refusal `stop-boundary: no green value …`; two-plus greens → typed
     refusal `stop-boundary: N green values …`; both rc 2, last stdout line
     `{"tool", "class": "T7-chain-stop-boundary", "refused"}`, no output file;
   - internal exception → `{"tool", "class", "error"}` rc 1, no output; both `--out` and `--info`
     targets are validated before the first write; no `/tmp` writes (tempfiles under TMPDIR).
4. Intact input → rc 0, output byte-identical (round-91 path).

## Measured geometry finding (drove one design fix)

First draft assumed the pristine b_info chain ends at the PackHeader and gated the last-block
spot on a `< 12`-byte residual. The probe disproved this on all five carriers — the chain ends
thousands of bytes before the PackHeader (jq 10097 < 14000, xxd 15630 < 19524, libz 60127 <
65544, docker-init 352674 < 357748, xz 42590 < 46532), so the walk's PackHeader bound absorbs
small `+delta` lies and the walk steps THROUGH the tampered block: `blocks[-1]` IS the tamper
site in both ±7 directions. First draft refused all 20 cells (receipt
`probe1-firstdraft-failure.json`); after the fix, the probe shows per cell: ±7 → exactly one
green == the pristine value → repaired to pristine; ±40 → zero greens in ±16 → typed refusal
(receipt `probe2-green-census.json`).

## Attack findings (own failure modes)

- **Multi-green windows**: not observed — each ±7 cell has exactly one green (the pristine
  value) and each ±40 cell zero greens across all five carriers. A ±64 sweep around pristine on
  xxd (129 probes) found NO second green anywhere: no two-green configuration was constructible,
  so the "two-green forged fixture" selftest case is skipped with a loud note (`two-green fixture
  NOT constructible in the swept window (0 greens …)`) instead of a fake pass.
- **Outside-window writes**: structurally excluded — only `spot+4..spot+7` is ever written, and
  the pre-write gate re-diffs output vs input (diff ⊆ `[p+4, p+8)`, length equal); counter
  `unsafe 0` and `wrong 0` confirm.
- **Output-length change**: excluded by the same gate; no cell produced a length change.
- **Far-window refusal**: all 10 ±40 cells refused typed (rc 2, `refused` JSON, no output) —
  the ±16 window never reaches a green value there.
- **Cost**: ≤ 33 probes per spot (one spot in practice on these carriers); full battery wall
  time 3.43 s; per-cell repair 0.1 s (jq/xxd/libz/xz), 0.2 s (docker-init); pack ~0.1–1.9 s per
  carrier. Intact arms cost one round-91 path pass each.

## Selftest

`--selftest` (fixtures under TMPDIR work dir): intact identity, last-block −7 and +7 repaired to
the pristine bytes, −40 and +40 typed refusals, not-an-ELF refusal, two-green forge attempt:

```
python3 -I -B tools/round-92/upx-stop-boundary-search-repair.py --selftest   → rc=0
SELFTEST cases=6 failures=0  | walk=v2.layout blocks=5 last=(off=15455, cpr=163, unc=784);
two-green sweep +-64 around pristine: greens=[]; two-green fixture NOT constructible …
```

Receipt: `selftest.log`. CLI contract was additionally checked end-to-end (repaired cell rc 0 +
`out==pristine` + info file; intact rc 0 identity; far rc 2, refused JSON as last stdout line,
no output file).

## Deviations / limits

- The two-green forged fixture could not be constructed (see above) — skipped honestly, as the
  item allows ("if you can construct one").
- The declared `±16` window is the tool's own bound: deltas in `(16, 40]` behave like far cells
  (typed refusal) whenever no green exists in-window; only `±7` (near) and `±40` (far) are
  battery classes, per the frozen claim.
- C2 (counterfeit arms, positive control) is another seat's item; not touched.
- No tools were installed or upgraded (host python 3.14.8 and pinned `/usr/bin/upx` 5.2.0 sha256
  `cf2f6e7c…` were already present); no pacman, no host-state change.

## Files written

- `.ufo/waves/round-92/w1/ExecRepair/upx-stop-boundary-search-repair.py` (candidate, byte-exact)
- `.ufo/waves/round-92/w1/ExecRepair/selftest.log`
- `.ufo/waves/round-92/w1/ExecRepair/c1-candidate.json` (frozen-counter receipt)
- `.ufo/waves/round-92/w1/ExecRepair/probe1-firstdraft-failure.json`, `probe2-green-census.json`
  (attack/geometry receipts)
- `.ufo/waves/round-92/w1/ExecRepair.md` (this report) and the same content at
  `.ufo/waves/round-92/w1/ExecRepair/ExecRepair.md`
- Nothing else in the lane; scratch `/fast/scratch/hyaku/kaidoku-r92/ExecRepair` deleted before
  yield.
