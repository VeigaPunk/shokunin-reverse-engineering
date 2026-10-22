# R25-C1 mutation probe — `tools/round-25/a2/c1-calibration.py`

Seat `C1Mutation`, round 25 attempt 3, wave 1. Lane read-only; all mutation in a disposable
clone. UTC window 2026-10-22T10:45Z–10:50Z. Everything below is an observation of the runs
recorded under the seat dir; only the one marked `[inference]` is a reading, not a fact.

## Method

* Clone `/fast/scratch/hyaku/kaidoku-r25-a3/seats/C1Mutation/clone` of the lane, base
  `08c7a7299ed61c3fdc30ddb0adfe4e812d5eac76` (`git clone -q` + detached checkout).
* Instrument under test `instrument-pristine.py`, sha256
  `4378af84fa8e036f62e85e81a07d21d0ed899a34b56f790a4682f0c965356eee`, byte-identical to the
  lane's `tools/round-25/a2/c1-calibration.py` at the base commit.
* Detector, one run per mutant: `python3 -I -B <seat>/instrument-pristine.py --root
  <seat>/clone --rev <mutant-rev>` → JSON on stdout; exit 0 no mismatch / 1 mismatch / 2 cannot
  evaluate.
* Baseline at `08c7a729`: `{"mismatches": 0, "items": 5}`, exit 0. Each mutant = one minimal
  edit committed in the clone, then the clone is reset to base. Harnesses: `harness.py`
  (M1–M17), `probe_missing_blob.py` (M18), `verify.py` (per-mutant content proof). Every run's
  stdout, exit code and UTC stamp is retained in `results/*.json`.

## Mutant table — can each of I1–I5 fail? Yes (observation)

Each of I1, I2, I3, I4, I5 flips to false with exit 1 under one mutant (M1–M5, one per item)
and stays true under a mutant where the underlying statement is false (M6–M11): no item is
frozen true, none is self-verifying.

| # | mutant commit | edit | expected | observed (exit / mism / item) | verdict |
|---|---|---|---|---|---|
| M1 | `3c2190365c0b` | SCORECARD: drop spot-check path from round-24 verdict line | I1 false | 1 / 1 / I1=false | detected (also false reject) |
| M2 | `dcb8ffe0e804` | LOG: drop spot-check path from round-24 verdict line | I2 false | 1 / 1 / I2=false | detected (also false reject) |
| M3 | `25da4a81bcf5` | QUALITY: delete admission row 34 | I3 false | 1 / 1 / I3=false | detected |
| M4 | `3d0a968d7f12` | SCORECARD coverage row `108/108`→`107/108` | I4 false | 1 / 1 / I4=false (stated [107,108] vs observed 108) | detected |
| M5 | `a18cf85ed367` | SHONEN pointer `PROVINCE.md:95-116`→`88-116` | I5 false | 1 / 1 / I5=false (stated [88,116]; Adjacent = 95–266) | detected |
| M6 | `d02e94ff6f7d` | SCORECARD verdict line → "**not yet recorded in this card** …" line still holding path + token | I1 must fail | 0 / 0 / I1=true | **false accept** |
| M7 | `dbf64bef38a7` | LOG verdict line → "**not yet recorded in this log** …" line | I2 must fail | 0 / 0 / I2=true | **false accept** |
| M8 | `9c314666274a` | QUALITY row 34 citation → `round-24.md`; a weak-signal row 7 cites the spot-check | I3 must fail | 0 / 0 / I3=true | **false accept** |
| M9 | `c56145e6370c` | decoy `\| coverage \|` row `108/108` before the live row; live row → `90/90` | I4 must fail | 0 / 0 / I4=true (read the decoy) | **false accept** |
| M10 | `0c11e2aa0ed9` | README coverage map: EVM-selector row dropped (107/108 mapped); card unchanged | I4 must fail | 0 / 0 / I4=true (stated [108,108], observed 108) | **false accept** |
| M11 | `b89688f9bb51` | SHONEN: earlier `PROVINCE.md:95-116` pointer added; live assertion → `88-116` | I5 must fail | 0 / 0 / I5=true (first match) | **false accept** |
| M12 | `541bf5ca0d67` | stale `\| coverage \|` row `107/107` before the live `108/108` row | I4 must fail | 1 / 1 / I4=false | **false reject** |
| M13 | `70cca3a9efa2` | SHONEN pointer rewritten `PROVINCE.md lines 95-116` (same range) | I5 must fail | 1 / 1 / I5=false (stated null) | **false reject** |
| M14 | `1187dc9ec063` | coverage row `108/108` → `108 of 108` knowledge files mapped | I4 must fail | 1 / 1 / I4=false (stated null) | **false reject** |
| M15 | `fc32d45b2570` | QUALITY row 34 citation loses the `.md` suffix | I3 must fail | 1 / 1 / I3=false | **false reject** |
| M16 | `7633a4f384a1` | SCORECARD: verdict text and spot-check path split over two lines | I1 must fail | 1 / 1 / I1=false | **false reject** |
| M17 | `210397c6a7ac` | LOG: same two-line split | I2 must fail | 1 / 1 / I2=false | **false reject** |
| M18 | `5e22f037ba3c` | delete `corpus/lessons/round-24-verifier-spotcheck.md` | cannot evaluate | exit 2 `{"error": "missing_blob", "path": "corpus/lessons/round-24-verifier-spotcheck.md", …}` | cannot-evaluate OK |
| C1 | control | `--rev deadbeef` | cannot evaluate | exit 2 `{"error": "bad_rev", "rev": "deadbeef"}` | control OK |

## False accepts (6) — instrument exits 0 while the statement is false

1. **M6 (I1)** SCORECARD.md:3048 = "Round-24 outside decision: **not yet recorded in this
   card** — the round-24 verifier spot-check (`corpus/lessons/round-24-verifier-spotcheck.md`,
   verdict rejected-honest-stop) is pending…". The card no longer records the decision, yet the
   one-line substring test fires → I1 true, exit 0.
2. **M7 (I2)** LOG.md:2954 = same construction, "**not yet recorded in this log**" → I2 true,
   exit 0. (LOG.md:2811 cites the spot-check but without the token.)
3. **M8 (I3)** QUALITY row 34 now cites `corpus/lessons/round-24.md`; the only line in the
   whole file naming `round-24-verifier-spotcheck` is the new weak-signal row 7 (line 56).
   I3's `^\| \d+ \|` filter cannot tell admission criteria from "Signals of weak material".
4. **M9 (I4)** SCORECARD.md:23 is a decoy `| coverage |` row stating `108/108 knowledge files
   mapped`; the live row (line 24) states `90/90` — false with 108 knowledge files present.
   First-match wins → I4 true, exit 0.
5. **M10 (I4)** dropping the EVM-selector row from the `corpus/README.md` coverage map leaves
   107 of 108 mapped, so the card's "108/108 knowledge files mapped" is false; the lane's own
   recipe A at that commit prints (exit 0) `{"dangling": [], "knowledge_files": 108, "mapped":
   107, "missing": ["2026-10-22-r25-evm-selector-name-resolution"]}`. The instrument never
   opens the coverage map → I4 true, exit 0.
6. **M11 (I5)** SHONEN.md:4 = "Boundary reference: `PROVINCE.md:95-116` (the `## Adjacent`
   refusal list)." while the live assertion (line 13) is `PROVINCE.md:88-116`, which starts
   inside `## Frontier`. First regex match wins → I5 true, exit 0.

## False rejects (8) — instrument exits 1 while the statement is true

* **M1/M2** dropping only the path leaves the verdict recorded ("Round-24 outside decision:
  the round-24 verifier spot-check records round 24 as **not admitted, rejected-honest-stop**
  … This card accepts that verdict"); I1/I2 fail on the citation form, not the claim
  `[inference: the instrument tests the citation, not the decision]`.
* **M16/M17** verdict text and path on two consecutive lines: decision and citation both
  present, one-line test fails.
* **M12** a stale `| coverage |` row ahead of the live one flips I4 false although the live
  row states 108/108 and the observed count is 108.
* **M13/M14/M15** `PROVINCE.md lines 95-116` (same range, prose form) → stated null → I5
  false; `108 of 108 knowledge files mapped` (true) → stated null → I4 false;
  `corpus/lessons/round-24-verifier-spotcheck` without `.md` → I3 false.

## Coverage notes for the L1 (observation)

* I4 never reads `corpus/README.md`: it compares the card's own N/N with the number of
  `corpus/knowledge/*.md` files; the row's "missing [], dangling []" claim is outside it (M10).
* I4 and I5 are first-match-wins over the whole file (M9, M11, M12); I3 cannot distinguish an
  admission criterion from a weak signal (M8); I1/I2 are one-line substring tests defeated by a
  negation or a line wrap (M6, M7, M16, M17). Every item is a text-shape check.

## Restoration evidence

* Clone reset to base `08c7a7299ed61c3fdc30ddb0adfe4e812d5eac76`, work tree clean,
  `git status --porcelain` empty (`results/restored-hashes.json`). Base sha256: SCORECARD.md
  `6de61b5bbd58…`, LOG.md `37be1e33e26e…`, corpus/QUALITY.md `e200c853a31c…`, SHONEN.md
  `120cd2b3bb5f…`, corpus/README.md `8369cb9c2061…`, PROVINCE.md `73df22ffba77…`, instrument
  `4378af84fa8e…`; M18 spot-check blob before `653517f846b7…` = after restore `653517f846b7…`.
* Lane HEAD still `08c7a7299ed61…`; only lane write by this seat is this report file. The lane
  work tree shows pre-existing modifications (`SCORECARD.md`, `corpus/SOURCES.md`,
  `corpus/knowledge/2026-10-22-r25-evm-selector-name-resolution.md`,
  `corpus/lessons/round-25.md`, untracked `.ufo/waves/round-25/a3/`,
  `corpus/evidence/round-25/a3/`) that are **not** from this seat — every measurement reads
  Git blobs at commits, never the lane work tree.

## Artifacts (seat dir, sha256)

`harness.py` `928eca4b42b17c62e9376996cf78dc58d8b27b982fe83113507e8c33438309ae` ·
`verify.py` `7a5add66397f5f0afbc07941078511f53e2a7f972d672172f2a1cea9102d1e0e` ·
`probe_missing_blob.py` `bfc061c6720574c0395a444a1d9d0abd8b8f5ff7aeecbbfff64a6af21d12c9c2` ·
`instrument-pristine.py` `4378af84fa8e036f62e85e81a07d21d0ed899a34b56f790a4682f0c965356eee` ·
`verification.txt` `0c2f25253b48c9cac49b271e40ce1576319123482f8b3f936b16382782202567` ·
`results/verification.json` `33ee69f7a303931c5b1cf153285667f085b5fbde1e4c4ad6c465ac9ec9044311` ·
`results/restored-hashes.json` `1036ed9725ad74399a3d961f91dfa0ee48378ee43f7e49201d136d8daa2448a1` ·
`results/M1…M18` (18 per-mutant JSONs: rev, exit, UTC, before/after sha256, raw stdout).
Tooling: no installs needed (`git`, `python3` stdlib, `grep`); no REA call, no web, no `jj`.
