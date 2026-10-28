# C2MutAtoms — fixture-side mutation test of the nine round-49 C2 atoms (wave 1, pre-freeze)

## Verdict

**NOT READY TO FREEZE.** On the GREEN fixture (draft `c2-mismatch.py`, `mismatches 0`, in-counter battery green), **14 of 27** planned single-atom fixture mutations stay green; with the two extras, 16 of 29 are undetected. All nine atoms have at least one undetected change. The plan's own kill rule ("a mutation that leaves its atom green … stops C2 and is reported as a miss") is therefore met for every atom. The 13 remaining mutations flip exactly their own atom red, so the counter does detect the changes it was built to read.

Most important findings (fold in before the freeze):

1. **The counter does not read the sources that quote the same values.** The committed closure `corpus/lessons/round-48-verifier-spotcheck.md` quotes the dead hash `663f30ee7516942a…` (line 16), the receipt digests `c30628ae…` and `3cc2d72d…` (lines 75, 99) and the verdict `rejected-harmed` (line 7). Base `LOG.md` line 3439 names the final freeze `b6f7ca2a`. Editing the lesson alone (M04), or re-pinning SCORECARD and lesson together (M02, M15), or flipping the closure's Admission verdict (M26), all stay green. A1, A2, A5 and A9 compare the record only with itself.
2. **The battery's own A7 mutation is red for the wrong reason, and the real defect slips through.** Battery `A7 teaches states the wrong status` replaces `EX_USAGE is 64` with `EX_USAGE is 2`, leaving `EX_USAGE is 2, not 2`. That is red only because the `64` token disappears. The swap `EX_USAGE is 2, not 64` (M19) keeps `EX_USAGE` and `\b64\b`, so A7 passes while the teaches cell now contradicts the snapshot line `EX_USAGE 64`.
3. **Stated numbers and lists are checked for presence, not value or completeness.** The quote word counts `(21 words)` / `(22 words)` are never re-derived (M16, M20: truncated quotes of 7 and 12 words stay green). `identified 2` is never derived; the code checks only `identified >= screened`, although the docstring says "every number is re-derived from the registry" (M22). Dropped log pointers and dropped `unnamed` entries are invisible (M07, M08). Seat-name swaps between results entries are invisible (M12).
4. **Shadowing and first-match reads.** `section()` reads only the first matching `## …` heading (X02). `registry_rows` is last-wins for duplicate ids (X01). A9 uses `any()`, so a second contradictory correction line is accepted (M25). A substring test on the closure accepts a token that survives in a prose aside (M26).

Report: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-49/w1/C2MutAtoms.md` (receipts and per-mutation diffs under `.ufo/waves/round-49/w1/C2MutAtoms/`).

## Method

- Scratch clone built by the lane's helpers: `mkclone.sh $S/clone` → `DEV_FREEZE=7a202afa75d4a75d15892df2e5d1af7f16eddfb1`; `c2-after.py $S/clone` → `DEV_AFTER=ea7e1ccca5f5af698ab0ff15b60836d7ac9d979c` (the GREEN fixture). `S=/fast/scratch/hyaku/kaidoku-r49/C2MutAtoms`. Clone toplevel asserted equal to `$S/clone` before any git call; identity `r49-dev` set in the clone only. Lane tree not touched.
- Each mutation is a commit in the clone that descends from `DEV_AFTER`, changes only the intended paths (asserted: changed-path set equals the mutation's file set; no-op mutations refused), and is scored by the draft counter at that commit:
  `python3 -I -B $S/clone/tools/round-49/c2-mismatch.py --root $S/clone --rev <MUT> --freeze 7a202afa75d4a75d15892df2e5d1af7f16eddfb1 --json-out <OUT>` (plain run, `--battery` not run per mutant). The clone is reset to `DEV_AFTER` after each.
- Driver: `.ufo/waves/round-49/w1/C2MutAtoms/drive.py` (copied to the lane artifact directory; reruns reproduce the same diffs).
- Mutation classes used across the 9 atoms: number change, hex-digit rewrite, pointer move, id swap, value swap, truncated quote, snapshot edit with re-pin, row deletion, list omission, section/row duplication, reorder.
- Scratch mutation commit hashes are not reproducible (commit timestamps). The **diff sha256** is the stable identifier; the stdout sha256 includes the scratch commit hash and is recorded per run in `json/`.

## Baseline (the counter on the drafts)

| run | command (clone) | exit | result | stdout sha256 |
|---|---|---|---|---|
| green fixture, battery | `c2-mismatch.py --root $S/clone --rev ea7e1ccc… --freeze 7a202afa… --battery` | 0 | `mismatches 0`, `battery.failing []`, do-nothing overlay red = all nine | `7ec63e63e0ff50c83081e515f170d159f21cdaac69a454442ccc1536fe9a139e` (`green.json`) |
| freeze itself | `c2-mismatch.py --root $S/clone --rev 7a202afa… --freeze 7a202afa…` | 1 | `mismatches 9` | `8326ffaf91bfe9b10f80020424cec39901efe0d364a910cb4aedf68f7f32791c` (`freeze.out`) |
| control (final, after all mutations) | same as green fixture, plain | 0 | `mismatches 0` | `dd5dc8055d21e9753512cdee7526ab14fb14caefed2b5e1486ff94d87da2ece1` |

Counter sha256 `90fa4722c960a8c21dd3166f115f721fa097115cc576703478c7a55c7d15243f` (draft file in the lane and the clone copy are byte-identical).

## Findings: undetected mutations (14 planned + 2 extras)

Exit 0, `mismatches 0`, no atom red for each. "Diff sha256" is of `git diff DEV_AFTER <mut>`.

| id | atom | exact fixture change (committed bytes) | diff sha256 | why it stays green / fold-in |
|---|---|---|---|---|
| M02 | A1 | coordinated: `SCORECARD.md` `**Declared freeze:** b6f7ca2a…873a` → `61b87d74…edad` (the round-48 base commit) and lesson `declared=b6f7ca2a…` → `declared=61b87d74…` | `7b8adc3a6969a359b6c076021d1d3a6ca8ae2ef4b240fd4c557b7942edd29ab4` | A1 checks only SCORECARD == lesson A1 and both are commits. Base `LOG.md` line 3439 names `b6f7ca2a` as the final freeze; not read. Fold-in: cross-check A1 against LOG.md. |
| M04 | A2 | lesson `dead=663f30ee7516942a0120e7de68fe88356e680822` → `…6e680823` (one hex digit) | `dd8a5b79597698df14e08940667bee697c2dc19104c267046fe6c2adaa616639` | Dead hash is checked only for "not a commit". Closure line 16 quotes `663f30ee7516942a0120e7de68fe88356e680822` as the cited hash; not read. |
| M07 | A3 | delete ` log_33f65a91=3440,3441,3444` from the A3 line | `779a61a0a6921a610f2dc7da3bef011ec925a8dfe608e677ed1f3b16ffd3eaaf` | `keys` need only be non-empty; a dropped pointer is never counted. Fold-in: require the set of log_ keys to equal the set of hashes named in the record. |
| M08 | A3 | `unnamed=577a02a5,8847042a` → `unnamed=8847042a` | `13db85d821c97589a94fafec9346359609fb17c012ec549fa8e926e96e66758f` | Only listed unnamed hashes are checked; omission invisible. |
| M12 | A4 | committed `.ufo/waves/round-48/r48-w1-results.json`: `"name": "ScribeBlock"` ↔ `"name": "ScribeScore"` (entries 49 and 52) | `4a422223725db60b8e3f4fc5398a1a8803cafff7c7bc50cb27f29d93db8de45d` | A4 derives only the multiset of names; seat name is never tied to the entry's `output.seat`. Fold-in: compare `name` with the output `seat`. |
| M15 | A5 | coordinated: round-48 `c2-final-33f65a91.json` `"axes_atoms": 2,` → `3,`; lesson `c2_raw`, `c2_stripped`, `report_c2` re-derived | `638b02773b99e4abc063e27548b22848f772dbc29562789b286ec4ad5c0fca92` | A5 reads the receipt and the lesson, not the closure line 99 (`c30628ae…`, newline-stripped) nor the round-48 report that A5 says quoted the prefix. |
| M16 | A6 | S147 anchor quote truncated to `"falsifiability as his criterion for demarcating science"`, `(21 words)` kept (quote is 7 words) | `5d13bb2b35867c6d635bcda031f3e986e339dd3ed8f2798b99ea6dec8f2d3775` | Quote is a substring of the snapshot and the heading check still passes; stated word count never re-derived. Fold-in: count words. |
| M17 | A6 | snapshot `corpus/evidence/round-49/c2/popper.html` gets one trailing HTML comment; S147 `sha256` pin re-pinned to the new digest (`eec524db…4049b00`) | `cd5127e1cbd77a606d61241a78539ceec55a229650ce3b6ee6e53e5e49ce35fc` | Snapshot dir is not in the frozen set; the counter cannot tell a re-pin from a fetch. Base row S145 (frozen text, line 151) still pins `2c2d48c6…207` for the same page and is not read. Fold-in: cross-check S147 against S145's pin (or note this as a disclosed limit). |
| M19 | A7 | S148 teaches cell `EX_USAGE is 64, not 2` → `EX_USAGE is 2, not 64` | `0e1c245137523223964822f0a435e6194bc91136fa35bb04118999d78ee5b14f` | A7 tests only the presence of `EX_USAGE` and `\b64\b` in the cell. The swapped claim contradicts snapshot line `EX_USAGE 64`. Battery's own A7 mutation is red only because it deletes the `64` (`EX_USAGE is 2, not 2`). Fold-in: test the value bound to `EX_USAGE`, against the snapshot. |
| M20 | A7 | S148 quote truncated to `"The command was used incorrectly, e.g., with the wrong number of arguments"`, `(22 words)` kept (12 words) | `82b8a128a51d0834214e3a5155d96ab1792312af0311e67a05e86fda6d538b17` | Same as M16: stated word count not re-derived. |
| M22 | A8 | round-49 search-log entry `identified 2,` → `identified 3,` | `3670a37fb90b5e4ed9926f8e88667184db2a388930c59670025feed1fb7c44ea` | `identified` is never derived (only `identified >= screened`). Docstring "every number is re-derived" overclaims. Fold-in: fix the docstring or bound the number. |
| M24 | A8 | swap the round-48 and round-49 search-log entry lines | `9978b88a73c290183ee9611fd28a77f289d66fd7d624aa01ca7b0fc0f4359634` | Order-insensitive by construction. Low severity (journal order, no number changed). |
| M25 | A9 | append after the real A9 line `- A9 verdict=accepted source=corpus/lessons/round-48-verifier-spotcheck.md calibration=improved` | `823b14c82f6bba04b847aa9fa5c53a86b8c0cf05ea3d44985d808e35870eaee3` | A9 uses `any()`; a second, contradictory correction is silently accepted. Fold-in: require exactly one A9 line. |
| M26 | A9 | closure `Admission: **rejected-harmed**` → `**accepted**`, plus appended prose `Earlier draft verdict: rejected-harmed (superseded).` | `1aeadd45c0680df167fa2bf009a5bd5bf434adf5c2c66989e62c92a1ea6a70a4` | A9 checks the token as a substring anywhere in the file. The closure now says accepted with its calibration row still `harmed`. Fold-in: parse the verdict field. |
| X01 (extra) | A7 | duplicate `| S148 |` row with bogus teaches `EX_USAGE is 2, not 64` inserted before the real row | `67e5bc96b801be9bf81de8f5eaf4fff72912a0bd0ae4158a4e55871873f611cf` | `registry_rows` is last-wins; duplicate ids are never rejected. |
| X02 (extra) | A1 | second `## Corrections to round 48` section appended to the lesson with a false A1 line | `e16421a27d0c0b1800c4818a4fcc15749602b503c7ca6a92e0377cefe2c0309d` | `section()` returns the first matching section only. Fold-in: reject duplicate sections. |

## Detected mutations (13 planned; each flips its own atom only)

| id | atom | exact change | exit | red | diff sha256 |
|---|---|---|---|---|---|
| M01 | A1 | SCORECARD declared freeze last hex digit `a`→`b` | 1 | A1 | `14d899b5d058753d73b1928e9c720f0a8535c49d0b8fa48ac145f464ebc009e2` |
| M03 | A1 | delete the lesson A1 line | 1 | A1 | `6fa8c391f56c659ae711f6d4b7bd4829fc64d0ba20204140f3c770ac12bf6818` |
| M05 | A2 | `actual` digit rewritten (8-hex prefix kept, not a commit) | 1 | A2 | `eab9290af26787fe4d8a145fe4fc8ac8168527f50ce2edc00ee457fce13fbc1c` |
| M06 | A2 | swap dead/actual values | 1 | A2 | `094196f64757ba7699f5c509ebae60f9f7181870c6845368407400f422248351` |
| M09 | A3 | pointer `log_2e785632` line `3445`→`3446` | 1 | A3 | `28c52f365edb7a9e6e8eb66abe68d8ac94c801f9e33d069ecec62173aa6136c2` |
| M10 | A4 | `seats=75`→`76` | 1 | A4 | `905d7ace0078643dd733c9ce4265c0a11c4aa7661a0d9c65a6ae6a66137a1063` |
| M11 | A4 | delete committed `.ufo/waves/round-48/w1/CritAssim.md` | 1 | A4 | `f535a420af3f0d131488d07ea7ad02139ca522bf78bd063a804333c06346b106` |
| M13 | A5 | `c2_raw` last hex digit `4`→`5` | 1 | A5 | `16f650102d10097821fb602a3753a864ae95367f2966755ce9714145cfc23bae` |
| M14 | A5 | delete ` report_c1=3cc2d72d` | 1 | A5 | `9909647c7e28108fb63676afbbb8218f128624ad1120003dacda35f8fb026497` |
| M18 | A6 | S147 `opened` 2026-10-28 → 2026-10-27 | 1 | A6 | `9a273fd43c23f2272bff111a2673945b817f884d00f749ee47ed74e7b0e895be` |
| M21 | A7 | snapshot `EX_USAGE 64`→`65`, S148 pin re-pinned | 1 | A7 | `93ee9795e0ab3ee96c36d44a250e4bd0221dd9f00bdf5f25a00efea9ddb21e93` |
| M23 | A8 | round-48 entry `included 1, excluded 1` → `0, 2` | 1 | A8 | `e8887607e17f5c152eafc65efb93c5f56ca302768873bb2d8b6ecc42a137b5d8` |
| M27 | A9 | move the A9 line under `## Record corrections — round 48` | 1 | A9 | `8c59a48a7f8a56a48c5cea16739730848085b0b70678fe275091d5f7b5a55f89` |

Per atom (planned 3 each): A1 M01 red, M02 green, M03 red · A2 M04 green, M05 red, M06 red · A3 M07 green, M08 green, M09 red · A4 M10 red, M11 red, M12 green · A5 M13 red, M14 red, M15 green · A6 M16 green, M17 green, M18 red · A7 M19 green, M20 green, M21 red · A8 M22 green, M23 red, M24 green · A9 M25 green, M26 green, M27 red.

## Observations that are not single mutations

- **Freeze-integrity does not bind the record atoms.** The frozen set covers `tools/round-49` and the plan only. Every file the 16 green mutations touch (`corpus/lessons/round-49.md`, `corpus/SOURCES.md`, `SCORECARD.md`, `corpus/lessons/round-48-verifier-spotcheck.md`, `corpus/evidence/round-49/c2/*`, `.ufo/waves/round-48/r48-w1-results.json`, `.ufo/waves/round-48/l1/scores/*`) is outside it. A post-freeze edit of any of them is freeze-admissible, so "`mismatches 0` at REV" is only as strong as the atoms.
- **The battery is narrow.** Its eleven mutations are all red, but none of the sixteen greens above is among them, and its A7 mutation is red for the wrong reason (see finding 2).
- **Overclaim in the docstring.** "every number is re-derived from the registry" (A8) is false for `identified`; "quote <= 25 words" (A6/A7) checks the bound, not the stated word count.

## Not run / disclosures

- `--battery` was not run per mutant; the in-counter battery was run once on the green fixture only.
- The C1 counter, the controls and any data run were not touched (outside this seat).
- The first pass of the driver aborted at M17 (a regex-scoping bug in my driver: the popper digest also appears in S145, so the replacement was scoped to the S147 row). M12 was first written as a whole-file JSON reformat (a 299 KB diff), then rewritten as a two-line textual swap. The final, complete run is `run2.log`; `results.json`/`results.tsv` are from that run. Verdicts for the M01–M16 shared mutations were identical in both passes.
- Coordinated mutations (M02, M15) edit two files at once by design; they show the counter cannot distinguish a consistent forgery from a true record.

## Tooling

No tools installed or upgraded. Everything used is already on the host (`git`, `python3`, the lane helpers).

## Artifacts (`.ufo/waves/round-49/w1/C2MutAtoms/`)

- `drive.py` (the driver), `results.tsv`, `results.json` (per-mutation exit, mismatches, red set, diff sha256, stdout sha256, UTC time, counter sha256).
- `json/<commit12>.json` (counter output per mutation and for the control), `diffs/<id>.diff` (exact `git diff DEV_AFTER <mut>` for each of the 29), `green.json`, `freeze.out`, `green.out`, `hashes.txt`, `receipts.sha256`, `run2.log`.
- Times (UTC) of the final run: 2026-10-28T21:16:58Z to 21:17:09Z; the scratch clone was removed after copying these receipts.
