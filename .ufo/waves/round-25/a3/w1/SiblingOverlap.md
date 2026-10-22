# Round 25 attempt 3, wave 1: sibling-lane overlap for R25-C1 and R25-C2

Seat: KaidokuR25a3.SiblingOverlap (connector, leaf). Lane tip read: 08c7a7299ed61c3fdc30ddb0adfe4e812d5eac76.
Revenger tip read: 876630dbb4d630e016d7d8c32a19ea04c646cbae. All sibling access was read-only (rg, sed, git ls-files/log/rev-parse).
Axes used: adjacency (correct cite, defer or ignore), quality (scope honesty of C2), coverage (C2 counter result unchanged).

## Attack and verdict

The attack: a sibling lane already holds EVM selector-name resolution (4byte, openchain, signature DB) or C1's
self-assessment ground, so kaidoku's C2 would re-claim sibling work, or must cite it.
**Verdict: holds (no sibling holds selector-name resolution or C1 ground).** One sibling seat queried 4byte.directory
once, but only as a falsifier, not as held knowledge. Revenger's EVM work sits on the extraction layer below C2.

## Method (observations)

1. `ls -d /home/vgpnk/Projects/shokunin/*-shokunin` at 2026-10-22T10:42:28Z, exit 0: 21 lanes, so 20 siblings.
2. Per-lane counts with `rg -i -c -g '!.git' -g '!node_modules'` (default; skips hidden dirs) at 10:42:40Z, exit 0.
   Excerpt: `revenger-shokunin \bEVM\b=202 ... 4byte=0 openchain=0 signature (database|db)=0`.
   4byte or openchain appeared in no other lane either; game-dev-2d's two `4byte` hits are unrelated test strings
   (`atk-a2-4byte-magic`, `all4byte-identical`).
3. Default rg skips `.ufo/`, so I reran with `--hidden -g '!.git' -g '!.jj' -g '!node_modules'`, using
   `\bEVM\b|4byte|openchain|signature (database|db)|sig\.eth|inspect.evm`, at 10:45:58Z, exit 0.
   Totals: revenger 1162, kagi 744, souji 16, tsukuroi 11, kotoba 6, game-dev-2d 2, kasegi 2, game-dev-3d 1, others 0.
4. `timeout 90 rg -uu ... -e '4byte|openchain|signature (database|db)|sig\.eth|selector name' revenger-shokunin kasegi-shokunin`
   at 10:45:46Z, exit 0: only `revenger-shokunin/.ufo/waves/round-61/build/ScribeEntryEvm.md:1` and
   `.ufo/waves/round-61/falsify-w3/W3EvmSelectorConstants.md:1`. Both are git-tracked (`git ls-files --error-unmatch`, rc=0;
   last commit 7a66d22, 2026-10-21).
   Kotoba's 6 hits are 5 case-insensitive byte runs in `.ufo/round-44/evidence/omp-live-18.12.2-strings.txt`
   (`"Evm]`, `=evM`, …) plus `.ufo/waves/round-49/build/CensusRevenger.md:42`, a census description of revenger; none is EVM work.
   The completed hidden sweep (10:46:48Z) again lists only `W3EvmSelectorConstants.md` as revenger's 4byte/openchain/sigdb file.
5. Kagi's 744 hits are nested sandbox copies of one line, `.ufo/waves/round-25/build/ConnSiblings4.md:26`:
   "`corpus/verify_*.py` are 11 fixture verifiers (EVM, PE resources, icons, JS graphs)" (a note about revenger's verifiers).
6. Unknown: the first all-lane `-uu` sweep (all ignored files, including sandboxes) did not finish inside its 60 s window
   and was moved to the background by the harness. No result from it is used. The hidden-inclusive per-lane sweep in item 3 did complete.

## Overlap table

| lane | file pointer | overlap kind | kaidoku should |
|---|---|---|---|
| revenger | `corpus/knowledge/round-62-evm-dispatch-byte-evidence.md` (admitted r62, `corpus/lessons/round-62.md:238` "admit, authored-byte/saved-field correspondence only") | same REA verb `inspect_evm_interface` (evmole@0.9.3) on 7 authored fixtures; dispatch offset, not names | **ignore for C2 support; cite only if C2 states extraction recall** (see the proposed move) |
| revenger | `corpus/knowledge/evm-saved-interface-candidates.md` (header: "rejected — round-61 fresh falsify wave"); `corpus/lessons/round-61.md:79` rejects "REA reports every statically valid PUSH4→JUMPDEST pattern" (falsified by saved r26) | provider misses a valid selector pattern behind an entry STOP | **defer**: rejected entry, so never support; the r26 negative is the reason C2 must not generalize recall |
| revenger | `.ufo/waves/round-61/falsify-w3/W3EvmSelectorConstants.md:10` | the same database as C2: "the public 4-byte registry maps `0xdeadbeef`→`CodeIsLawZ95677371()`" (accessed 2026-10-21) | **defer**: a seat report, not admitted knowledge; it independently agrees with C2's `[inference]` about junk submissions, but kaidoku's own saved pages already carry that evidence |
| revenger | `corpus/SOURCES.md:32` S018 (Solidity v0.8.37 ABI, §Function Selector) | the same primary source as kaidoku S021 | **ignore**: kaidoku opened its own row |
| revenger / ADJ-06 | `PROVINCE.md:3` "Owns: reverse engineering of shipped artifacts"; `corpus/lessons/round-62.md:29` "ADJ-06 … Operator-owned and unresolved" | domain-level contest of shipped-artifact RE, named by the round-24 spot-check | **defer to the operator**; C2 must declare no ownership; fleet `.ufo/l0-questions.md:42` still carries the question |
| tsukuroi | `PROVINCE.md:51,79,128-129`; `.ufo/waves/round-19/l1-capture/siblings/kaidoku/d1d981d2cc04/PROVINCE.md:93` | registers ADJ-06 and pins a kaidoku PROVINCE snapshot holding the old "selectors stay bare hashes" text | **ignore**: pinned by commit and sha256; C2 changed line 93 in place (see second-order effects) |
| kotoba | `PROVINCE.md:41,51`; `corpus/knowledge/sibling-overlap-census-round49.md:119-121` | census reports the kaidoku/revenger contest at kaidoku tip 08c7a72 | **ignore**: report only, no ruling |
| tabi | `corpus/adjacency.tsv:3-5` | refuses RE ("→ revenger/kaidoku"); CDP runtime contest with revenger | **ignore** for C1 and C2 (CDP is not in either claim) |
| kasegi | `SKILL.md:110`, `corpus/knowledge/operator-queue.md:58` | deployed bytecode ↔ repo-commit identity (claimability) | **ignore**: C2 claims no deployed contracts (entry Limits) |
| game-dev-3d | `corpus/knowledge/rea.md:24` | refuses "claiming revenger's routes (PE/EVM/ZIP/ELF/JS-graph)" | **ignore**: a third-party attribution, not a ruling |
| kagi, souji | kagi sandbox copies of `ConnSiblings4.md:26`; souji `tests/vault/*/Verdict-Log.md` roster lines | lexical mentions only | **ignore** |
| all 20 | no hits for 4byte, openchain or signature DB outside revenger's round-61 seat reports | none for C2 naming; none for C1 | **ignore** |

C1 (observation): items I1-I5 in `tools/round-25/a2/c1-calibration.py:63-91` read only kaidoku SCORECARD, LOG, SHONEN,
`corpus/QUALITY.md` and PROVINCE. No sibling file is an input, and no sibling holds kaidoku self-assessment ground.

## Second-order effects

- Observation: `git diff -U0 18e7eb6d…ad473 08c7a729…ec76 -- PROVINCE.md` (10:48:09Z, exit 0) shows a single line,
  93, replaced in place (`1 insertion(+), 1 deletion(-)`). Tsukuroi's OUT-008 pointer (`PROVINCE.md:3-6,88-100`) is pinned at
  `d1d981d2cc04` with a blob sha256. Inference: the anchor is not broken, though a live re-read of 88-100 now shows the new
  C2 wording rather than the snapshot text.
- Observation: C2's entry has no cross-lane block (`rg -i 'revenger|kasegi|sibling|cross-lane|Q10'` on the entry gave no hits). Revenger's
  candidates entry cites kaidoku's `2026-10-13-r3-evm-interface.md:151-153` as prior art, so the citation runs one way only.

## Proposed move (one, bounded)

Add one recall sentence and one cross-lane line to the C2 entry's Limits (edit by L1 only), and add nothing to SOURCES:
"REA returned exactly the ABI's selectors on all six carriers (69 of 69, 0 extra). Revenger's saved r26 record
(`revenger-shokunin/corpus/lessons/round-61.md:79`) shows the same provider version missing a valid pattern, so recall is not
assumed elsewhere. ADJ-06 ownership is not decided here."
Evidence for 69 of 69: `python3 -I -B recall.py /home/vgpnk/Projects/shokunin/kaidoku-shokunin` (10:45:32Z, exit 0), which imports
the lane resolver's `abi_signatures` and `envelope_functions` read-only. Excerpt: `TOTAL abi=69 rea=69 missed=0 extra=0`. Per carrier:
rv2token 5/5, kdxtoken 6/6, vaultb-opt200 13/13, carrierb 8/8, stewardtoken 22/22, carrierv 15/15.

- Axes improved: quality (C2's "no name" counts now have an explicit, measured denominator) and adjacency (gives the overlap the
  round-24 spot-check named a concrete, non-ownership pointer).
- Axes not harmed (inference): the coverage counter checks the Markdown count and S075-S077 cite, mined and used-by state.
  Editing the body adds no file and no SOURCES row, so 108 and 1 should hold. Rerun `c2-coverage.py` after any edit to confirm.
- Risks: citing a sibling lesson could read as importing a ruling; the wording above avoids that. The recall figure covers
  six lane-compiled carriers only. The entry's `verified-at` line would need the new evidence path.
- Verification for L1: rerun `recall.py` (sha256 below); rerun `c2-coverage.py --rev <new>` (expect 108 and 1) and
  `c1-calibration.py --rev <new>` (expect 0).

## Artifacts (under /fast/scratch/hyaku/kaidoku-r25-a3/seats/SiblingOverlap/)

- `recall.py` sha256 2582863639afdeae95009f924c35635c829a886a901fdce82432a76724671ebe
- `recall.out` sha256 b0b2e9be24a1cd9cd0b9f816b2940115e7c7ff2d793d01002a71b161d07d56e1

Tooling: none installed or upgraded. No web page opened, no REA call, no signature-database request (0 of 120).
