# R39MutR38Counter — mutation probe of `tools/round-38/c1-counter.py`

**Verdict: DEFECTS FOUND — the counter's runtime logic is sound on real data, but 17 of 18 single-logic mutants survive its `--selftest`; the selftest's receipt-level red cases (wrong handler, extraction gap) are held up entirely by the evidence-id recompute side channel, so the handler, gap, oracle-match, binding and S-id clauses have zero isolated selftest coverage. Enumerated below as the tests the round-39 C1 counter selftest must add.**

Scope: learn which clauses of the round-38 C1 counter actually discriminate, before the round-39 C1 counter freezes. Lane untouched (read-only git only); all mutants lived in scratch copies; scratch removed at end. Leaf seat — no subagents, no background jobs.

## Baseline (detector sanity — runs first, mandatory)

- Pristine `--selftest --pkg65 ~/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents` → rc=0, `{"cases": 15, "green_ok": 1, "red_ok": 14, "failures": []}`.
- Pristine scoring: `python3 c1-counter.py --root <lane> --rev 7e97951460647e4fc39542b7a4f0255b5bf1af17 --freeze e059ca9391642d5b71b6662cabcbdce0d9308719 --pkg65 <pkg65> --json-out pristine-rev.json` → rc=1, `met_target=false`, `carriers_matched=3/4`.
- This red is the **true state, not a detector failure**: at 7e979514 K2 carries one real `extraction_gaps` entry `{"kind": "unpublished-entry", "relative_path": "firmware.bin_extract/var/lib/run-link", ...}` (the R38-C1 honest stop), and PROVINCE.md at that rev has no `## Round-38 additions to Core` section (BE SquashFS stayed Frontier). All mutant REV verdicts below are deltas against this pristine state; every mutant also returns rc=1, so "verdict at REV" = which real-repo flags move.

## Key mechanism discovered (changes how the selftest must be read)

xpin-attribute.mjs prints `path \t stored \t id65 \t id67 \t attribution`; the counter keeps `(f[1], f[2])`, so `ev[key][0] == ev[key][1]` is **"stored `evidence_id` == id recomputed under the frozen 6.5.0 pin"** (receipt honesty), not a pkg65/pkg67 equality. The 6.5.0 `semanticProjection` projects `normalized_result` wholesale (`dist/domain/evidence.js`), so **any** tamper of `chunks[].handler` or `extraction_gaps` breaks the stored-id match. Therefore the selftest's 'wrong chunk handler (LE)' and 'extraction gap present' red cases are red through *two* channels, and mutants weakening the target clause alone survive.

Proof (instrumented run, `artifacts/DBG07-le-case-K3.json`): under M07, K3 in the LE case has `after_handler_ok=true` yet `matched=false` with `after_evidence_id_ok=false`. Composites (two-logic probes, labeled as such):

- C1 = gap-allow-one + evidence-id-weakened → selftest failure `extraction gap present: want 1 got 0` (artifacts/C1-selftest.json).
- C2 = handler-any + evidence-id-weakened → selftest failure `wrong chunk handler (LE): want 1 got 0` (artifacts/C2-selftest.json).

## Sweep — mutant | selftest kills? | verdict at 7e979514 | reading

Patches: `artifacts/mutants.patch`; raw per-mutant rc/JSON in scratch was ephemeral, summarized in `artifacts/results.json`.

| # | Mutant (clause) | Change | Selftest kills? | REV 7e979514 vs pristine | Reading |
|---|---|---|---|---|---|
| M01 | gap | `gaps(env)==[]` → `len(gaps(env))<2` | **NO** (1 green/14 red, 0 failures) | `carriers_matched 3→4` (K2 matched) | Gap clause has no isolated kill; on real data this mutant declares K2's honest-stop receipt covered. Only the missing Core-promotion bindings keep `met_target=false`. |
| M02 | gap | drop `and d.get('after_gaps_empty')` from ok | **NO** | `carriers_matched 3→4` | Same. |
| M03 | oracle-match | drop `sha == fs` (path-only) | **NO** | NO DELTA | Nothing publishes right-path/wrong-sha. sha half of `matched()` untested. |
| M04 | oracle-match | drop `endswith('/'+rel)` | YES — killed by **green** case (`green: want 0 got 1`) | hits 0 across K1–K4 → `carriers_matched 3→0` | Prefix tolerance is load-bearing on real REA layouts (published paths are nested). Best-covered clause: killed left and right. |
| M05 | oracle-match | `hits==oracle_files` → `(hits or 0)>0` | **NO** | NO DELTA | "all files" vs "any file" undiscriminated. |
| M06 | handler | accept any handler containing `'squashfs'` | **NO** | NO DELTA | LE red case survives via evidence-id side channel only (see DBG07). Handler clause: zero isolated coverage. |
| M07 | handler | `len(chunk_handlers)>0` | **NO** | NO DELTA | Same; C2 composite flips the LE case green. |
| M08 | evid-id | drop stored==recomputed | **NO** | NO DELTA | The receipt-honesty check — the one doing the masking — has no negative test. Highest-priority gap. |
| M09 | evid-id | drop `startswith('ev_')` | **NO** | NO DELTA | Equivalent-in-practice: with the frozen xpin pin, recomputed ids are always `ev_*`, so stored==recomputed implies the prefix. Unkillable without mocking xpin. |
| M10 | evid-id | `==` → `(== or startswith)` | **NO** | NO DELTA | Killed by a tampered-stored-id case, which doesn't exist yet. |
| M11 | bindings | frontier note: `'superseded' in l` only | **NO** | NO DELTA | No near-miss note fixture (superseded-without-big-endian). |
| M12 | bindings | SOURCES: pad short rows instead of skip | **NO** | NO DELTA | **Equivalent mutant**: padded rows get `c[8]=''/c[10]=''` and can never satisfy opened+used-by; behavior identical on all inputs. Not a test gap. |
| M13 | bindings | drop `entry_present` from bind_ok | **NO** | NO DELTA | Redundant with `sourced` today; one fixture makes it independent (below). |
| M14 | bindings | province_core_row: drop `and ENTRY in r` | **NO** | NO DELTA | No fixture pairs handler-in-cell0 with a wrong entry path. |
| M15 | S-id | `S\d{3,}` → `S\d+` | **NO** | NO DELTA | No short-id fixture. |
| M16 | S-id | drop trailing `(?![0-9A-Za-z])` | **NO** | NO DELTA | `S\d{3,}` is greedy: `S1120` matches either way; needs glued-token fixture (`S1123a`). |
| M17 | S-id | drop leading `(?<![0-9A-Za-z])` | **NO** | NO DELTA | Needs leading-junk fixture (`XS112`). |
| M18 | S-id | `S\d{3,}` → `S\d{3}` | **NO** | NO DELTA | Existing 'S-id substring S1120' case is red under both (registry has S112, not S1120) — it tests *registry-entry mismatch*, not the quantifier. |

Score: 1/18 killed by selftest; 1 load-bearing kill at REV (M04) plus the gap clause bound by real data (M01/M02 flip K2); M09/M12 equivalent-in-practice; **14 genuine survivors = tests round-39 must add**.

## Tests the round-39 C1 counter selftest must add

Red cases unless marked green; receipt-tampering cases must **re-mint** `evidence_id` (run xpin after the tamper, as `mint()` already does) so only the target clause can fire:

1. Wrong-handler receipt, re-minted → isolates the handler clause (kills M06/M07).
2. One-gap receipt, re-minted → isolates the gap clause (kills M01/M02).
3. Tampered stored `evidence_id` (any `ev_…` value ≠ recomputed) → kills M08/M10.
4. Published file with right path, wrong sha256, re-minted → kills M03.
5. Carrier with only 1 of N oracle files published, re-minted → kills M05 (and strengthens 4).
6. Delete ENTRY while the SOURCES row still lists it under used-by → kills M13.
7. Province Core row: handler in cell0, entry cell ≠ ENTRY → kills M14.
8. Frontier note line containing 'superseded' but not 'big-endian' → kills M11.
9. S-id boundary fixtures: entry `source: S7` + registry row S7 (kills M15); `source: XS112` (kills M17); `source: S1123a` with registry S1123 (kills M16); **green** variant citing `S1120` with a matching opened/used registry row (kills M18).
10. M12: equivalent mutant — no test can kill it; if the 11-column shape is meant to be load-bearing, that is a contract decision for the round-39 author, not a selftest case.

For the C1 side of round 39 (six BE carriers): note that K2-style honest stops are exactly what the gap clause exists to catch, and a gap-blind counter passes 4/4 carriers at 7e979514 — the round-39 selftest should carry items 1–3 before the carrier count grows.

## Method, commands, bounds

- Scratch `S=/fast/scratch/hyaku/kaidoku-r39/R39MutR38Counter` (removed at end); `HYAKU_SCRATCH=$S TMPDIR=$S` on every counter run so the tool's own tempdirs stayed inside seat scratch; `cd "$S"` before runs.
- Workspace: `mut/c1-counter.py` (pristine, sha256 `a7a62b09…16db8`) + `mut/selftest/` fixtures + `round-27/xpin-attribute.mjs` copied from the lane working tree (selftest resolves them relative to the script).
- 18 mutants generated by unique-string replacement (assert count==1, AST-parsed); 2 labeled composites for the masking proof. Every run: `--selftest --pkg65 …` then `--root <lane> --rev 7e979514… --freeze e059ca93… --pkg65 …`.
- Debug instrumentation (DBG07/07b) was scratch-only, never in the lane.
- Restoration evidence: lane `tools/round-38/c1-counter.py` sha256 before and after = `a7a62b098709035607375078a12d2668bb6d36bbabfc5a7459f04d00a9516db8` (unchanged); `git status --porcelain tools/round-38` → clean; no VCS-mutating git/jj commands used anywhere.
- Tooling: **no installs** — used existing node v24.21.0, python3 3.14.8, system git; pacman untouched; sasquatch/unblob never invoked (not needed for this probe).
- [INFERENCE] tag: nothing in this report is inferred; all rows are measured runs. The one judgment call — M09 "equivalent-in-practice" — is derived from reading the frozen xpin pin (ids always `ev_*`), stated above.

Artifacts: `artifacts/mutants.patch` (18+2 unified diffs), `artifacts/results.json` (machine-readable sweep), `artifacts/pristine-rev.json`, `artifacts/C1-selftest.json`, `artifacts/C2-selftest.json`, `artifacts/DBG07-le-case-K3.json`.
