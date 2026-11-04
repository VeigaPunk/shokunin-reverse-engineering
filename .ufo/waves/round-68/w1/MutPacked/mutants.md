# mutants.md — R68-C2 route, five targeted mutants

Seat: `MutPacked` (mutation-tester, round-68 / w1 / attempt 1)
Target under test (read-only, NEVER edited): `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-68/packed-elf.py`
Frozen sha256: `48ef4c688a14faf381abbd2cc2b29061035f38c97815e2365957843433e5276e` (re-verified after the probe: unchanged)
Mutations applied only to scratch copies under `/fast/scratch/hyaku/kaidoku-r68/MutPacked/mut/` (scratch removed at yield).
Base `fcbe200f6739c38939e0dabf3f251de2cc6bd727`; operative freeze `1eaf596e5f241762349fbd102c9e09ec1df18e3f`.

## Detectors used (same bounded detector on pristine, mutant and restored bytes)

| id | detector | invocation | scale |
|---|---|---|---|
| D1 | tool selftest | `python3 <copy> --selftest` → rc + `cases`/`failed` | 13 registered cases |
| D2 | no-claim short circuit | `python3 <copy> --root <fixture repo> --rev deadbeef --pkg <REA root> --skip-run --json-out …` | payload minus `instrument` |
| D3 | real route, real environment | `python3 <copy> --root <fixture repo> --rev deadbeef --pkg <REA 6.5.0 root> --work <scratch> --json-out …` (actual `/usr/bin/upx` 5.2.0, `readelf` 2.47, REA analyze/decompile on `/usr/bin/jq` + `/usr/bin/xxd`) | scoring fields of the receipt |
| D4 | fixture-root `score()` call, green configuration (`S0_green`) | `harness.py <copy> S0_green` — real `score()`, `section_count`, `counts_from`, `carrier_arms`, `fold`; modelled `upx`/`readelf`/REA over fixture carriers with real sha256 pins, all arms satisfied | `(rc, met_target, failing, control_ok)` |
| D5 | fixture-root `score()` call, single-arm break (`S1`…`S5`) | `harness.py <copy> S<n>` — same, one arm's precondition broken per scenario | `(rc, met_target, failing, control_ok)` |

Every detector was first run on the pristine copy: D1 `cases 13 failed []` rc 0; D2 rc 1, `met_target null`, `verdict_claimed false`, `closure null`; D3 rc 0 `met_target true carriers_matched 2 control_ok true before_procedures [3, 3]`; D4 rc 0 `met_target true failing []`; D5 each scenario rc 1 with exactly the broken arm named in `failing` (`S5`: arms all true, `control_ok false`, `failing []`). Baseline is green where it must be, so a mutant's silence is a survival, not an inconclusive run. D4/D5 are deterministic (pristine `S1` repeated → byte-identical result object).

## Mutants (minimal, one behaviour-bearing point each)

| # | patch site | original → mutant |
|---|---|---|
| M1 | line 257 `identity_ok = (unpack["rc"] == 0 and os.path.exists(unpacked) and sha256_file(unpacked) == c["sha256"])` | → `identity_ok = True` |
| M2 | line 261 `recovery_ok = bool(rec_counts) and rec_counts == orig_counts` | → `recovery_ok = bool(rec_counts) and rec_counts == rec_counts` |
| M3 | line 249 `detected = listing["rc"] == 0 and secs == 0` | → `detected = listing["rc"] == 0` |
| M4 | line 254 `before_ok = before_procedures is not None and before_procedures < floor` | → `before_ok = before_procedures is not None and before_procedures == before_procedures` |
| M5 | line 289 `verdict = fold(carriers, all(c["control"]["list_rc"] != 0 and c["control"]["decompress_rc"] != 0 for c in carriers), len(CARRIERS))` | → `verdict = fold(carriers, True, len(CARRIERS))` |

Mutant shas: M1 `85d34a25387a6763d2957de65a7c18f4b359a0dd76124c3eda554376fe6dfafc`, M2 `855dbb269442ab7404c03f4e7d5173a6212dc7c83176a6948451d7663aa95345`, M3 `eb7691535e622df3c8961c6edb1ff3b2a4b6d9ccd31617269c4edd6738a38465`, M4 `541311a19ba7040d5b8004a8025b6130a7bdf105fe4a6532b5f82bc712780667`, M5 `0c501fa8779360e8367f2c878a9a0564f8d502b3ea36e0068d02a4223bdea734`. Pristine scratch copy `48ef4c68…` = frozen pin.

## Result matrix

| mutant | D1 selftest | D2 `--skip-run` | D3 real green route | D4 modelled green `S0_green` | D5 binding scenario | fires? |
|---|---|---|---|---|---|---|
| M1 identity_ok≡True | 13/13 pass, rc 0 | rc 1, payload identical to pristine except `instrument.sha256` | rc 0, `met_target true`, `failing []`, all arms true — identical scoring fields | identical verdict (`rc 0, met true, failing []`) | **S1_identity_broken** | **yes, only there** |
| M2 recovery_ok self-compare | 13/13 pass, rc 0 | rc 1, identical payload | rc 0 green, identical scoring fields | identical | **S2_recovery_broken** | **yes, only there** |
| M3 detected = `upx -l` rc only | 13/13 pass, rc 0 | rc 1, identical payload | rc 0 green, identical scoring fields (`section_count` 0 on both carriers) | identical | **S3_sections_present** | **yes, only there** |
| M4 before_ok self-compare | 13/13 pass, rc 0 | rc 1, identical payload | rc 0 green, identical (`before_procedures [3, 3]`, floors 50/25) | identical | **S4_before_above_floor** | **yes, only there** |
| M5 control arm dropped from `fold` | 13/13 pass, rc 0 | rc 1, identical payload | rc 0 green, identical (`control_ok true`) | identical | **S5_control_hot** | **yes, only there** |

Each mutant differs from pristine in exactly one of the six `score()` scenarios (verified exhaustively: 5 mutants × 6 scenarios; `receipts/matrix.json`). No collateral change in any non-target scenario.

### Where each killer fires, with the case name

| mutant | killer scenario | pristine (rc, met, failing, control_ok) | mutant (rc, met, failing, control_ok) |
|---|---|---|---|
| M1 | `S1_identity_broken` (unpacked bytes ≠ pin on both carriers) | `1, false, [fa:identity_ok, fb:identity_ok], true` | `0, true, [], true` |
| M2 | `S2_recovery_broken` (unpacked inventory ≠ original inventory) | `1, false, [fa:recovery_ok, fb:recovery_ok], true` | `0, true, [], true` |
| M3 | `S3_sections_present` (`upx -l` rc 0 but 2 section headers) | `1, false, [fa:detected, fb:detected], true` | `0, true, [], true` |
| M4 | `S4_before_above_floor` (packed inventory 150 procs, floors 50/25) | `1, false, [fa:before_ok, fb:before_ok], true` | `0, true, [], true` |
| M5 | `S5_control_hot` (`upx -l` on the original returns 0) | `1, false, [], false` | `0, true, [], true` |

## Survivors (named)

**All five survive every detector the lane actually runs: D1 selftest (13/13 green), D2 `--skip-run`, D3 the real green route, D4 the modelled green route.** None survives its own single-arm-break scenario; the surviving set is exactly `{M1, M2, M3, M4, M5}` under the green configuration that R68-C2 is scored in.

### What the green run would then claim (false greens)

- **M1 survives →** `identity_ok` is decorative: `upx -d` could emit *any* bytes and the receipt would still print `identity_ok true` / `packed_sha` + unpack path recorded as restored. The claim sentence "unpack with sha identity" would be unevidenced, and `carriers_matched 2 of 2` would be satisfied on an unpack that changed the program. **Binding case:** `S1_identity_broken`.
- **M2 survives →** `recovery_ok` collapses to "REA returned three integers for the unpacked file"; "recovers the original's REA inventory" is then false-by-construction and unfalsifiable. **Binding case:** `S2_recovery_broken`.
- **M3 survives →** `detected` becomes "the packer's own list verb said so", dropping the independent structural clause (no section-header table). A file UPX merely *recognises* but did not fully pack would score `detected`. On the pinned carriers `section_count` is 0 either way, so the clause is untested by the real run. **Binding case:** `S3_sections_present`.
- **M4 survives →** `before_ok` becomes true for any packed inventory at all; the "stub, not the program" premise (`procedure_count` below the carrier floor) is never checked, so a packed image that still reported ≥ floor procedures would be scored `before_ok`. **Binding case:** `S4_before_above_floor`.
- **M5 survives →** `control_ok` is hard-wired true; the negative arm on the same bytes (original must not be reported packed, `upx -d` must refuse) disappears from the fold, so `control_ok true` in the receipt becomes vacuous and `met_target` no longer depends on it. **Binding case:** `S5_control_hot`.

### Coverage finding (report-only; contract untouched)

`selftest()` (line 305) registers 13 cases, but **no case evaluates any of the five arm expressions**: at lines 313–314 `identity-equal` / `identity-mismatch` compare the *string literals* `"ab"*32` and `"cd"*32` without calling `score()`, and `skip-run-no-claim` inspects a hand-built dict. `carrier-ok-*`, `fold-*`, `sections-*`, `counts-*` exercise pure helpers, so a defect in `score()`'s arm wiring is invisible to `--selftest` — which is why all five mutants are 13/13. The registry's "13 cases" is true and, for these five sites, non-discriminating. Observation, not a claim change: R68-C2 stays as declared; no arm in the receipt was altered.

## Restoration evidence

- Frozen file `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-68/packed-elf.py` sha256 before and after the probe: `48ef4c688a14faf381abbd2cc2b29061035f38c97815e2365957843433e5276e` — **never written**; mutations existed only as scratch copies.
- `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin status --porcelain -- tools/round-68` → no modified tracked file (only an unrelated untracked `tools/round-68/registry-conformance.receipt.json` written by another seat).
- Restored/verified bytes: pristine scratch copy equals the frozen pin (`48ef4c68…`); every D3 receipt records `instrument.sha256` equal to the copy actually executed (M1 `85d34a25…` … M5 `0c501fa8…`), so each mutant's receipt is self-identifying.
- Scratch `/fast/scratch/hyaku/kaidoku-r68/MutPacked/` removed after receipts were copied here; no tracked lane file, fleet file, jj/git index, or other lane was touched.

## Evidence files (this directory)

- `receipts/harness.py` — the fixture-root detector (D4/D5), unchanged from the scratch run.
- `receipts/mutants/` — pristine copy + the five mutant copies exactly as scored, with shas.
- `receipts/pristine-S*.json`, `receipts/M*-S*.json`, `receipts/matrix.json` — D4/D5 matrix.
- `receipts/det-pristine-S1.json` — determinism repeat.
- `receipts/real-*.json`, `receipts/real-pristine-baseline.json`, `receipts/real-env-mutant-comparison.json` — D3.
- `receipts/skip-*.json` — D2.
- `receipts/selftest-*.txt` — D1 transcripts.
- `receipts/MANIFEST.sha256` — shas of every file above.
