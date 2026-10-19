# RV-8 — C3 pin-line drift characterization

**Disposition:** The live pin and its targeted `current-ok` classification are **VERIFIED / REPRODUCED**. Pin-line movement is **VERIFIED** from direct snapshot scans. The full current census is a **DISCREPANCY**: it exits FAIL for a separate undeclared SCORECARD locus, not for the Kimi pin.

## First-hand re-derivation

- `grep -n 'rea-agents@' ~/.kimi-code/config.toml` returned `/home/vgpnk/.kimi-code/config.toml:4126:args = [ "-y", "rea-agents@6.7.0", "mcp" ]`.
- A byte-level receipt measured 4,150 lines, 1 literal `rea-agents@` occurrence, and 1 matching line. The line SHA-256 is `eb23737749a7dbd615db449daee491d821580fdb86df2660a92334df733b6cb1` excluding its terminator (`eb1c7da74fc5f870d7c6537e87beeaf043491b5cdd00ee7a2f65e426d9f2b675` including LF). See `RV-8/evidence/live-pin-receipt.txt`.
- Snapshot re-grep (`RV-8/evidence/pin-snapshots.txt`) found the same pin text once in each available file, at these measured locations: `20261018-085645.bak:2915`, `20261018-114557.bak:2932`, `20261018-143236.bak:2940`, `20261018-145016.bak:3227`, `20261018-150133.bak:3298`, `20261018-161746.bak:3298`, `20261018-201656.bak:3157`, and live config `:4126`.

**Characterization:** the literal package pin remained `rea-agents@6.7.0` in the inspected snapshots, while its line position moved (including a non-monotone move). The active config has exactly one `rea-agents@` occurrence. Therefore a numeric line pointer is perishable and must be re-derived from the live file; it is not a stable identity. I did not edit the config. These available snapshots do not constitute a complete history of every edit, so I make no claim about unobserved intermediate states or the exact cause of each shift.

## Instrument result

- Gate identity re-derived with `sha256sum .ufo/gates/c1-census-v10.py`: `e4fb740cb8153f15c623f3b9f7ca781e270053b0557be5393010359b2213b7b4`.
- Running its own `live_pins()`, `ptr_check("~/.kimi-code/config.toml", 4126, live)` returned `('ok', 'pins 6.7.0')`. Its `classify()` result for `PROVINCE.md` block `15-26` contains line 18 `kind=ptr`, value `~/.kimi-code/config.toml:4126`, `disp=current-ok`, `why=pins 6.7.0`; the Kimi pin assertion at line 18 is also `current-ok`. Exact capture: `RV-8/evidence/pointer-disposition.txt`. The paragraph-level aggregate is `info` because it also contains historical assertions; this does not change the pointer assertion's disposition.
- Standard full run `python3 .ufo/gates/c1-census-v10.py --json` exited 1 / `FAIL`; full JSON is `RV-8/evidence/census-v10.json`. The reported blocking locus is `SCORECARD.md` block `1833-1839` (assertion at line 1834, `UNDECLARED`, no client token in the clause). `stale=[]`, `unresolved=[]`, `scope_errors=[]`, and `frontier_errors=[]`. Thus the targeted pin is current-ok, but the whole census is not PASS.

## Evidence boundary

All measurements above were re-derived in this seat from the live config, available config snapshots, and the current gate. No prior seat or round result is used as evidence. All files created for this task are under `.ufo/waves/arc3-loop1-round9/claims/c3/RV-8/`; no config, gate, corpus, PROVINCE, SKILL, SCORECARD, or LOG file was changed. The seat artifact is the measured note; I did not edit the corpus because the frozen write scope prohibits it.