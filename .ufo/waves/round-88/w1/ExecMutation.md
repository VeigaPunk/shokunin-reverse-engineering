# ExecMutation — R88-C1 mutation probe (seat report)

Scope: mutation testing of `tools/round-88/upx-chain-repair.py` and
`tools/round-88/upx-chain-battery.py` with a declared-case table, 13 rows plus 3
control-green probes. No instrument was modified; both sha256 match the `claims.json`
pins (`59ee51b0…`, `a01ed622…`). No tool installed; no git/jj mutation.

## Ran

```
python3 tools/round-88/upx-chain-repair.py  --selftest     # cases=11 failures=0 rc=0
python3 tools/round-88/upx-chain-battery.py --selftest     # cases=6  failures=0 rc=0
python3 tools/round-88/upx-chain-battery.py --root <lane> \
  --repair-cmd tools/round-88/upx-chain-repair.py --upx /usr/bin/upx \
  --pkg <rea-agents> --work <scratch>/base-work \
  --json-out <scratch>/base-receipt.json --evidence-dir <scratch>/base-rea
# recovered 4 of 4, controls N1/N2/N3 all true, regression 8 of 8 met, exit 0 (182.95 s)
```

Then, per mutant: copy to a depth-preserving scratch mirror, assert the anchor occurs
exactly once, apply the single edit, `py_compile`, run `--selftest`, parse
`SELFTEST cases=… failures=…`. Each repair mutant was additionally run through the real
counter with `--no-rea` (`rea_recover` false by construction; only the four byte arms read).

## Numbers

- Table: 13 rows → **5 killed by selftest** (`R06`, `B01`, `B02`, `B03`, `B04`),
  **6 survivors** (`R01`, `R02`, `R03`, `R04`, `R05`, `R07`), **2 absent-case gaps**
  (`R08` exit-1-on-untyped-error, `B05` rc-None-not-refusal).
- Counter kills 2 of the 6 survivors (`R03`, `R04`) and R06 as well, all **on dinit only**:
  `test_ok`/`identity` false, `upx: …: Exception: compressed data violation`, derived
  `sz_cpr` 136 vs base 226, accounted 123,942,159 vs `u_len` 851,288.
- Survivors on both instruments: `R01` (`derived <= sz_unc0` bound dropped), `R02`
  (sentinel-reach test dropped), `R05` (`sz_cpr0 != 0` gate dropped), `R07` (candidate
  method gate dropped) — all produce byte-identical repaired output on all four carriers.
- Candidate census: jq/xxd/libz have **1** admissible candidate each; dinit has **3**
  (724/derived 136/does-not-fit, 814/226/fits/**selected**, 1028/440/850,696/fits). The
  selftest fixture has **1** candidate (s1 140, derived 40, accounted 200 vs `u_len` 64), so
  no selection rule is observable there.
- Control-green probes: all three (G1 identity refuses unpacked ELF; G2 N1 recorded true
  unconditionally; G3 naive-global refuses unpacked ELF) turn **all** controls green with
  `recovered 0 of 4`, exit 1, `met_target` false. None turns the claim green.

## Findings that limit the claim

1. The repair selftest cannot see the selection law: single-candidate fixture → 6/8 repair
   mutants survive; the `u_len` preference and the accounted-total tiebreak are exercised by
   exactly one of four carriers (dinit).
2. `szcpr-nonzero-not-derived` does not exercise the `sz_cpr0 != 0` gate: for `_fixture(7)`
   the upstream repair answers `intact=True`, so `geometry()` is never entered; R05 is an
   equivalent mutant here. The named limit is upheld by the upstream verdict, not this guard.
3. Three guards (`R01`, `R02`, `R07`) are killed by nothing — conservative direction, but no
   instrument distinguishes them.
4. N1 is a refusal-shape control, not a capability control: three independent mutants make it
   (and N2/N3) green with a do-nothing repair. `met_target` stays false, so no false green of
   the claim itself.
5. No selftest covers exit-code or stderr semantics (0/2/1 contract). R08 is exit-code
   equivalent to base (an uncaught exception already exits 1) and only changes the traceback
   into one line; B05 (rc None as success) has no case, and by source reading would make the
   counter die instead of recording could-not-evaluate.
6. Population fragility: without dinit, R03/R04/R06 would survive the counter too.

## Artifacts (lane-relative)

- `.ufo/waves/round-88/w1/ExecMutation/table.json`
- `.ufo/waves/round-88/w1/ExecMutation/report.md`
- `.ufo/waves/round-88/w1/ExecMutation/receipts/` (base + 7 repair-probe + 3 control-probe
  receipts, `mutants.json`, `candidate-census.json`, `geometry-probe.json`)

Scratch `/fast/scratch/hyaku/kaidoku-r88/ExecMutation/` was deleted after the receipts were
copied; mutants are reproducible from the anchor/replacement/diff/sha256 recorded in
`table.json`.
