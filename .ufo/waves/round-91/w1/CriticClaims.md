# Round 91 — CriticClaims seat: adversarial falsification of R91-C1 and R91-C2 as declared

Lane `kaidoku-shokunin`, declaration commit `deb2765a55fef0e4e81500a027dfe59951b69e87`, base `2135f6e1d3f69a259b32cc5167c52ccb1a261c24`.
Claims were not re-declared, renamed or re-targeted. Attacks ran in a scratch clone at the declaration commit (`git clone --shared` + `checkout`); the lane was read-only. Receipts and cheat sources are under `.ufo/waves/round-91/w1/CriticClaims/evidence/`.

## Verdict summary

| attack | subject | verdict |
|---|---|---|
| ATTACK-1 (a) | C1 is a coverage capability, or a guard restated? Is "refused" a repair? | SURVIVES as declared (a measured refusal; a guard with the packer's verdict as oracle). Not a repair. |
| ATTACK-2 (b) | Can a repair pass `refused 8 of 8; unsafe 0; intact 4 of 4` by a cheat other than the two named rules? | FALSIFIES. Two cheats pass both frozen labels: a carrier-reading repair (CHEAT-A) and a hash-table repair (CHEAT-B). "Write nothing" cannot pass (intact arm). |
| ATTACK-3 (b') | Does "refused" measure the typed rc-2 refusal the claim describes? | FALSIFIES (as worded). An rc-1 exit passes `refused`. |
| ATTACK-4 (c) | Are block 31's counts supported by the base receipt and QUALITY rows? | Counts SURVIVE. Row-3 criterion (QUALITY 169) FALSIFIES: row 169 says nothing about intact refusal. |
| ATTACK-5 (d) | Does block 31 cite only paths present at base (QUALITY 159)? | SURVIVES: all three cited paths exist at base. |
| ATTACK-6 (d') | Does the depth counter enforce the kill rule for non-knowledge paths and QUALITY rows? | FALSIFIES. Ghost QUALITY rows and ghost paths in block 31 still score `met True exit 0`. |
| ATTACK-7 (e) | Does the table clause accept a table whose rows say nothing? | FALSIFIES as evidence of routing (shape only, as the claim's own limits concede). Content-free table scores `met True exit 0`. |

## Reproduction (independent, at the declaration commit)

Instrument pins: sha256 of all instruments at `deb2765a` in my clone match `claims.json` (`upx-stop-boundary-repair.py` 473bb3a9…, `stop-boundary-battery.py` 5998b6bd…, `depth-blocks-v3.py` bcf6c4ea…, `upx-later-block-battery.py` 5462ef13…, `depth-blocks-v2.py` 359f15e1…, `upx-break-repair.py` 90dea087…). `/usr/bin/upx` passes its pin (battery accepts it). REA `package.json` sha256 `a5003023…` at `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/` matches the pin.

| check | command (abbrev.) | result | exit |
|---|---|---|---|
| C1 candidate | `python3 -I -B tools/round-91/stop-boundary-battery.py --root <clone> --repair-cmd tools/round-91/upx-stop-boundary-repair.py --work <S>/work/repro-cand --rev deb2765a… --expect 'refused 8 of 8; unsafe 0; intact 4 of 4'` | `refused 8 of 8; unsafe 0; intact 4 of 4 met True` | 0 |
| C1 base control | same, `--repair-cmd tools/round-90/upx-break-repair.py` | `refused 0 of 8; unsafe 2; intact 4 of 4 met False` (matches `pre/c1-base-round90-repair.json`) | 1 |
| C1 regression | `python3 -I -B tools/round-90/upx-later-block-battery.py --root <clone> --rev deb2765a… --repair-cmd tools/round-91/upx-stop-boundary-repair.py --pkg /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents --expect 'P1 6 of 6; P2 4 of 4; P3 4 of 4'` | `P1 6 of 6; P2 4 of 4; P3 4 of 4`; all controls true; `met_target true` | 0 |
| C2 counter | `python3 -I -B tools/round-91/depth-blocks-v3.py --root <clone> --rev deb2765a… --expect-blocks 31 --shape-from 31 --expect 'blocks 31, resolved 31, required-shaped 1/1'` | `blocks 31, resolved 31, required-shaped 1/1 … met=True` | 0 |
| candidate selftest | `python3 -I -B tools/round-91/upx-stop-boundary-repair.py --selftest` | `SELFTEST cases=4 failures=0` | 0 |

Environment note (not a claim defect): the regression counter's default `--pkg` (`~/.local/share/rea-agents/6.5.0`) does not exist on this host; it exits 2 `unevaluable: rea_pin`. I passed the pinned npx path explicitly.

## ATTACK-1 (a) — coverage capability or guard restatement; is "refused" a repair?

Evidence: the new branch in `repair()` (`tools/round-91/upx-stop-boundary-repair.py`, lines ~186–196) is `if upx_test(d): return d …; raise Refused(…)`. `upx_test` runs `/usr/bin/upx -t` on the input. The added code is therefore a guard whose decision is delegated to the packer's verdict. The counter's `refused` is "rc ≠ 0 and no output file" (`score_cell`). The claim's own Limits section says "refused, not repaired".

Reader may conclude: on the eight frozen tampered cells the repair produces no output file and exits nonzero; on the four frozen intact carriers it returns the input byte-identical; both outcomes are gated by `upx -t` on the input.

Reader may not conclude: that any broken carrier is repaired (refusal leaves the broken file broken); that refusals are correct for recoverable inputs (no arm tests that a refused input is unrecoverable); that the intact arm tests the repair's reasoning (for intact input the branch is `upx -t` green by construction, so the intact arm restates the oracle); or anything about other packers, versions, or carriers beyond the four pinned ones.

Verdict: **SURVIVES** as declared (a measured refusal). It must not be read as a repair.

## ATTACK-2 (b) — cheats the frozen label admits

Three cheat repairs were built in scratch as wrappers around the candidate (`evidence/cheats/`). Each replaces only the `upx_test` oracle:

- **CHEAT-A (carrier-read):** `upx_test(d)` = "d equals `upx --best` of one of the four carrier paths" (reads `/usr/bin/jq`, `/usr/bin/xxd`, `/usr/lib/libz.so.1.3.2`, `/usr/bin/docker-init`).
- **CHEAT-B (hash-table):** `upx_test(d)` = "sha256(d) ∈ the four pinned packed sha256 values" (`cheats/table.txt`; these equal the base receipt's `packed_sha256`). No carrier read, no packer verdict.
- **CHEAT-C (exit-1 refusal):** the candidate with its `rc 2` refusal changed to `rc 1`.

Results:

| cheat | frozen C1 counter | regression battery | receipt |
|---|---|---|---|
| CHEAT-A | `refused 8 of 8; unsafe 0; intact 4 of 4 met True`, exit 0 | `P1 6 of 6; P2 4 of 4; P3 4 of 4 met True`, exit 0 | `receipts/c1-cheat_carrier_read.json`, `receipts/reg-cheat_carrier_read.json` |
| CHEAT-B | `refused 8 of 8; unsafe 0; intact 4 of 4 met True`, exit 0 | `P1 6 of 6; P2 4 of 4; P3 4 of 4 met True`, exit 0 | `receipts/c1-cheat_hash_table.json`, `receipts/reg-cheat_hash_table.json` |
| CHEAT-C | `refused 8 of 8; unsafe 0; intact 4 of 4 met True`, exit 0 (all eight tampered cells `rc 1`) | not run (not needed to show the gap) | `receipts/c1-cheat_typed_only.json` |

A first CHEAT-B run scored `intact 0 of 4`. That was a harness error on my side (the battery runs repairs under a restricted environment, so the table path variable was dropped). I fixed it by hard-coding the table path, and the rerun is the result above.

"Write nothing on every path" cannot pass. Intact requires output-file identity. Measured: a rc-0 no-output stub scores tampered `other` and intact `identity False`; a rc-2 stub scores intact `rc 2, identity False`; a copy-through stub scores tampered `silent` (refused 0). The intact arm excludes all three.

Exposing cells. Neither is in the frozen predicate:

- **Blinded intact arm for CHEAT-A.** The four carrier paths (resolved by realpath) were bound by bwrap to a decoy binary, then each packed intact carrier was given to each repair. Results (`evidence/exposure/`):
  - Candidate: `identity` on jq, xxd, libz, docker-init (4 of 4).
  - CHEAT-A: `rc 2, no output` on all four (0 of 4).
  - Unblinded control on jq and libz: both `identity`.
  The regression `carrier_blind` arm does not expose CHEAT-A. It re-scores only P1 interior cells (`upx-later-block-battery.py`: `if not c["p1"]: continue`, `blocks[1]`), and P1 is repaired upstream of `upx_test`, so the arm passes (`reg-cheat_carrier_read.json`, `carrier_blind: true`).
- **Unpinned intact arm for CHEAT-B.** `/usr/bin/ls` packed with `upx --best` (`upx -t` rc 0, not one of the four pinned carriers): candidate `rc 0, identity`; CHEAT-B `rc 2, no output`.

Also noted: `upx-stop-boundary-repair.py` reads `/usr/bin/xxd` at line 229, inside `selftest()` (lines 215–260), not in `repair()` (lines 164–200). The claim's statement that "the repair reads no carrier path" holds for `repair()`. The file itself does read a carrier path, in its selftest, and that read is outside the scored path.

Verdict: **FALSIFIES.** The frozen label admits CHEAT-A and CHEAT-B, and each passes the regression label too. CHEAT-A is already declared as audit-level (Limits), but the audit-level claim is not measured by any arm. CHEAT-B violates the declared Limit that the intact arm "depends on upx -t as the packer's verdict", and that Limit is not measured either.

## ATTACK-3 (b') — does `refused` measure the typed rc-2 refusal?

Evidence: CHEAT-C returns `rc 1` on all eight tampered cells, with no output file, and scores `refused 8 of 8`. The counter's `refused` is `rc != 0 and out is None` (`score_cell`). The claim's Candidate section describes "a typed refusal (`stop-boundary: …`, rc 2)". `QUALITY` row 177 (base) names this exact hazard for the round-90 repair.

Verdict: **FALSIFIES** as worded. The predicate measures "nonzero, no output"; the description says "typed, rc 2". The label cannot tell a typed refusal from an uncaught exit that the candidate's own `except Exception` maps to rc 1.

## ATTACK-4 (c) — block 31's counts against the base receipt and QUALITY rows

Block 31 text is read from `SKILL.md` at `deb2765a` (block 31 of 31, `## Queue-drain craft`).

| block-31 statement | supporting evidence | verdict |
|---|---|---|
| "four pinned carriers, two directions each … returned `rc 0` on all eight cells" | `c1-base-round90-repair.json` cells: eight rows, all `rc 0` | SURVIVES |
| "two wrote bytes outside the tampered window" | `counts.unsafe 2`; `outside_window` on `jq` −7 and `libz` −7 (4-byte window) | SURVIVES |
| "six returned the broken file unchanged" / "six of eight cells" | `counts.silent 6` (jq +7, xxd ×2, libz +7, dinit ×2) | SURVIVES |
| "none was refused" | `counts.refused 0` | SURVIVES |
| "four of four intact carriers" (`intact` identity) | `intact` identity true ×4 (receipt). The receipt does not record `upx -t` on intact inputs. Independently: `upx -t -q` on the four `upx --best` packed intact carriers returned rc 0 each | SURVIVES |
| Row 1 criterion `QUALITY 176`: last-block −7 write past the window, rc 0 | QUALITY row 176 at base: "round-90 break-point repair … on a last-block `- 7` tamper (jq block offset 10,094; libz 60,124) … writes the four-byte `UPX!` sentinel … change outside the tampered window" | SURVIVES |
| Row 2 criterion `QUALITY 167`: exit code is not the verdict, rc 0 on broken file | QUALITY row 167 at base: "a repair's exit code means 'I changed the field I own', not 'the file is fixed'" | SURVIVES |
| Row 3 criterion `QUALITY 169`: "intact input refused by mistake" | QUALITY row 169 at base is "a superseding instrument inherits its predecessor's guards and refusal contract": FIFO `--in`, `/dev/zero`, uncaught `Refused`. It says nothing about refusing an intact input | FALSIFIES |

Verdict: the counts survive. The row-3 criterion is mis-cited. No base QUALITY row in the 167–177 range states "never refuse an intact input". The frozen counter cannot see this, because it does not resolve QUALITY citations (see ATTACK-6).

## ATTACK-5 (d) — paths cited by block 31 present at 2135f6e (QUALITY 159)

Block 31's cited paths, extracted from the declaration-commit block text, checked with `git cat-file -e 2135f6e1…:<path>`:

- `corpus/QUALITY.md`: rc 0
- `corpus/knowledge/2026-11-04-r90-interior-block-szcpr.md`: rc 0 (113 lines at base; the cited range 12–30 exists)
- `tools/round-90/upx-break-repair.py`: rc 0

Verdict: **SURVIVES.** Block 31 cites only paths present at the base revision.

## ATTACK-6 (d') — does the counter enforce the kill rule on the citations?

The kill rule says "block 31 citing a path absent at the base revision". The counter's `resolve()` uses `PATTERN = corpus/knowledge/([a-z0-9-]+\.md)(?::…)` and checks only those citations. Two fixtures were built from block 31 (in the scratch clone, restored clean afterwards, `dirty files after restore: 0`):

- `quality-ghost`: the three QUALITY row numbers in block 31's table replaced by `QUALITY 99999`, `88888`, `77777`. Result: `blocks 31, resolved 31, required-shaped 1/1 … met=True`, exit 0 (`receipts/c2-fx-quality-ghost.json`).
- `path-ghost`: `corpus/QUALITY.md` in the Refs line replaced by `corpus/NO-SUCH-FILE.md`, `tools/round-90/upx-break-repair.py` replaced by `tools/round-90/NO-SUCH.py`. Result: `met=True`, exit 0 (`receipts/c2-fx-path-ghost.json`).

Verdict: **FALSIFIES** the counter as an enforcement of its own kill rule for QUALITY rows and non-knowledge paths. The current block 31 is clean (ATTACK-5), but the frozen counter cannot falsify a block that is not.

## ATTACK-7 (e) — does the table clause accept a table whose rows say nothing?

Direct: `table_shape` on a header, separator and three body rows `| aa | bb | cc | dd |` (no routing content) returns `ok True`, `rows 3`, `min_cells 4`, `problems []`.

Full counter: block 31 replaced by a prose stub that clears the 25-word and two-span floors and carries that content-free table. Result: `blocks 31, resolved 31, required-shaped 1/1 … met=True`, exit 0 (`receipts/c2-fixture-meaningless-table.json`).

Verdict: **FALSIFIES** as evidence of routing. The predicate certifies table shape and citations, and nothing else. The claim's own Limits section says exactly this ("v3 measures the table's shape and its citations, not that its routing is correct"), so the claim survives on its declared terms. The reading "required-shaped 1/1 shows a decision table routing three classes to guards" does not survive.

## Cheap-rule controls and do-nothing controls

- Do-nothing (round-90 repair): `refused 0 of 8; unsafe 2; intact 4 of 4`, exit 1, reproduced exactly.
- Blanket refusal (rc 2, no output on every input): measured on jq only, the stub returns `rc 2`, no output, `identity False` on the intact packed jq, so it fails the intact arm; the other three intact carriers were not run against this stub.
- Geometry-only refusal: not separately re-run; ExecCandidate's seat owns it.

## Findings to route (no new claims proposed)

1. Frozen C1 label admits CHEAT-A (carrier read) and CHEAT-B (hash table); both pass the regression label. Exposing cells: blinded T7 intact arm (CHEAT-A: 0 of 4 vs candidate 4 of 4) and unpinned intact input (CHEAT-B refuses `ls`, candidate identity).
2. The `refused` arm does not assert the typed rc-2 refusal described in the candidate text (CHEAT-C passes).
3. The C2 block-31 `QUALITY 169` row-3 citation does not match the row's text.
4. The C2 counter does not resolve QUALITY row citations or non-knowledge paths; the kill-rule clause is unenforced for them.
5. The C2 shape predicate is satisfied by a content-free table.
6. Host reproducibility: the regression counter's default `--pkg` path is absent on this host.
7. Candidate file reads `/usr/bin/xxd` in `selftest()`; not on the scored path.

## Tools installed

None. Pacman was not used.

## Files written

- `.ufo/waves/round-91/w1/CriticClaims.md` (this report)
- `.ufo/waves/round-91/w1/CriticClaims/evidence/receipts/` (C1 candidate, base control, cheat receipts; regression receipts; C2 baseline and fixture receipts)
- `.ufo/waves/round-91/w1/CriticClaims/evidence/cheats/` (CHEAT-A/B/C sources, noop/copy stubs, `table.txt`, driver)
- `.ufo/waves/round-91/w1/CriticClaims/evidence/exposure/` (blinded and unpinned intact logs)

Scratch `/fast/scratch/hyaku/kaidoku-r91/CriticClaims` removed after copying the evidence above. No lane file was modified.
