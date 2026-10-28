# C1CtlDoNothing — R49-C1 do-nothing controls (pre-freeze, draft tools)

**Verdict.** Controls (a) and (b) both behave as the plan says (exit 1, `carriers_matched 0`; no kill-rule fire).
**But the only clause that stops the round-44-copy shortcut is `run_provenance_ok`, and a relabel + re-mint of that same copy (b3) reaches `carriers_matched 4`** (docs bindings still false → exit 1, so the kill rule was not triggered by my fixture; it would be if the six doc bindings were true). Nothing in CTL-C1-4 as planned (straight copy) covers this variant.

Setup: `mkclone.sh /fast/scratch/hyaku/kaidoku-r49/C1CtlDoNothing/clone` → `DEV_FREEZE=01b4a58db7ce30b97df52a2026d1f7b98aed08b9` (toplevel verified; fixture commits made only in that clone, identity `r49-dev`). Counter sha256 `d6d70cb7ecc789b5ac0b0cbb7ee5b656abeea395cea9a158249d9a4723a95779`. 2026-10-28 ~21:04-21:10Z. Common args: `python3 -I -B tools/round-49/c1-counter.py --root <clone> --rev <REV> --freeze 01b4a58d… --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents --work <S>/work-X --json-out <S>/out-X.json`. Receipts (stdout, json-out, empty stderr) in `w1/C1CtlDoNothing/`.

| ctl | REV | what | exit | carriers_matched | stdout sha256 | json-out sha256 |
|---|---|---|---|---|---|---|
| a | DEV_FREEZE | no receipts | **1** | **0** | f99f6bb3…d6d | b7bdca1e…65b |
| b1 | 41e0b753 | r44 `c1/<id>/after.json` ×4 copied to `corpus/evidence/round-49/c1/<id>/after.json` (the assigned shortcut) | **1** | **0** | bd832eb0…c56 | 341be876…51f |
| b2 | 40e8103e | whole r44 `c1/<id>/` dirs copied (after.json, envelope, tree, provenance, logs) | **1** | **0** | 93d9af8e…d6c | 1897c2cd…b70 |
| b3 | fcf294fc | b2 + `parameters.output_directory` rewritten `/kaidoku-r44/`→`/kaidoku-r49/` and `evidence_id` re-minted via the counter's own `mint_many` | **1** | **4** | 7eca0fe9…f20 | 3810b237…6d |

Failing clauses:
- **a**: all 12 per-carrier receipt clauses ×4 (`receipt_present, receipt_fresh, handler_ok, chunks_ok, gaps_ok, nonregular_unpublished_ok, operation_ok, oracle_hits_ok, path_shape_ok, projection_ok, run_provenance_ok, subject_pin_ok, evidence_envelope_ok, evidence_id_ok`); `bindings_false` = `province_core_section, province_core_row, frontier_note, entry_present, sourced, coverage_map_row`; `frozen_path_changed []`.
- **b1, b2** (identical): `failing` = exactly 4 entries, `{v1le,v1be,v2le,v2be}:run_provenance_ok` (output_directory `/fast/scratch/hyaku/kaidoku-r44/probe-R44C1Run/…`); same six doc bindings false. Every other receipt clause — including `receipt_fresh`, `projection_ok` (the counter-time rerun), `evidence_id_ok`, `tree_ok` — is **true** on the round-44 bytes. b1 shows the other r44 evidence files are not needed (after.json alone suffices; tree comes from the rerun).
- **b3**: `failing` has no carrier clause; only the six doc bindings false. `evidence_id_ok` true (the id is a public deterministic mint over the envelope; no secret).

Repro for b3 (clone at b2): load `tools/round-49/c1-counter.py` with importlib, `xp=m.find_xpin(root+'/tools/round-49')`, replace the string `/kaidoku-r44/` with `/kaidoku-r49/` in each `after.json`, `m.mint_many(work, xp, PKG, envs)`, write back `evidence_id`, commit, score.

Findings
1. Kill rule not fired by (a)/(b1)/(b2): non-zero exit, `carriers_matched 0`. OK as planned.
2. **Single-clause defence.** Round-44-receipt reuse is rejected solely by `run_provenance_ok` (string prefix test on `output_directory` + the id minted over it). Evidence that `receipt_fresh` ("first added in a commit descending from the freeze") does not catch the shortcut: copying makes the blob new at REV, so it passes.
3. **b3: relabel+remint reaches 4/4.** The plan discloses "does not prove which process wrote the committed receipt", but CTL-C1-4 only plants the unaltered r44 files, so the control proves only the string check, not provenance. Suggest: add a relabeled/re-minted control as a documented counterfactual that is *expected to still be red* only if some clause binds the receipt to a committed `provenance.json` / run record written by `c1-run.sh` (the plan says the runner records `provenance.json`; b3 ran with the r44 `provenance.json`, `run.json` unmodified and the counter did not flag them — the counter appears not to cross-check them), or else state in the plan that C1 admits a relabel and that its guard is process discipline, not the counter. Not run: whether b3 + hand-written landing blocks yields exit 0 (docs bindings are text-only; I did not write them).
4. Not run: CTL-C1-1/2/3/5/POS (other seats), the counter `--selftest`.

Tools installed: none.
