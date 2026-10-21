# CoverageMap (w2) — README new-row review, candidate 2838351450ff1ee4baa620c962a1153450d53311

Seat: `KaidokuR23.CoverageMap-2` (leaf, source review, no dispatch).
B = `aa1450b82f9ede35aada63efe8a34e01c6e02f72` (baseline). C = `2838351450ff1ee4baa620c962a1153450d53311` (candidate). Recorded counter rev = `6615aea642aec36959180e7ea940b2794c7f1cb`.

Method: candidate bytes only, via `git show`, `git ls-tree`, `git grep`, `git diff`, `git cat-file`, plus `awk`/`comm`/`grep`/`sha256sum` over those bytes. No counter, REA, sigrok, test, build, or linter run. Labels: **Observed** = command output or bytes; **Inferred** = reasoned from observed bytes; **Unknown** = not established.

## Verdict

No blocking defect in the new README row. Both R23 entries are mapped, all 156 baseline table rows survive, and `corpus/README.md` is outside the R23-C1 counter's read set. The remaining findings are low-severity presentation or precision items, plus out-of-item registry defects routed to L1.

## Findings

### A. Assigned item: README new row

**A1 — pass (Observed). Both files exist and are mapped.**
- `corpus/knowledge/2026-10-21-r23-offline-signal-envelopes.md` @C sha256 `7598d2cb436ceee4b6dc01c10869a9db0cd0f49afaf971aa02eb9f771aee6c35`
- `corpus/knowledge/2026-10-21-r23-dart-legacy-layout-boundary.md` @C sha256 `22711853c6a9ee31ce31669db17e8c8bef95892ba9c6831321704c2bd0178351`
- Both are present at `2b40aec`, the first commit that changed README (path-filtered `git log B..C`). README blob is `b5863fc` at 2b40aec, 6615aea and C, so 2838351 did not change README bytes.
- Mapping: coverage row `corpus/README.md:72` names both entries; knowledge row `:159` names both; lessons row `:176` is `round-23`, whose file `corpus/lessons/round-23.md` exists at C (sha256 `8327a21fbae3c976af820e10063d973f1862a945a041d4b02a90906700a70723`).

**A2 — pass (Observed). Prior rows preserved.**
- `git diff --numstat B C -- corpus/README.md` → `3	3`.
- Sorted set difference of `^| ` rows: baseline rows missing at C = 0; rows added at C = 3 (`:72`, `:159`, `:176`).
- The three removed lines are blank lines directly after the headings at B `:72` `## Knowledge`, B `:159` `## Lessons`, B `:176` `## Frontier`.
- README sha256: B `33c979d3c9d0ccf886f0bac423d3e5540c27b74d59a292538a50d0a1d1a0812d`; C `795466e5be2ac7341014a30a1a793a1aea17cdbb1f0d3451abc305085a62b57c`.

**A3 — low (Observed). Unrelated whitespace restyle.** The three blank-line deletions in A2 change no row, but the contract says NEVER restyle unrelated code. At C the headings sit at `:73` `## Knowledge`, `:160` `## Lessons`, `:177` `## Frontier`, each directly followed by its table or list. Rendering impact: none expected [Inferred: GFM allows a table or list to follow an ATX heading; no renderer was run]. Fix: restore the three blank lines. No row content changes.

**A4 — low (Observed). First two-entry row in the Knowledge section.**
- B Knowledge section: 83 rows, all single-entry. C: 83 single-entry rows plus `README:159`, which has two entries.
- Two-entry rows elsewhere exist only in the Coverage-map section at B `:22`, `:35`, `:63`.
- Impact: a one-entry-per-row reader would resolve only the first name on `:159`. No such reader was found: `git grep README` over `.ufo/waves/round-23/tools`, `verify.py` and `frozen/` at C returned no matches.
- Fix option: split `:159` into two rows. This touches only the new row.

**A5 — low (Observed). "Complete" lacks its contract scope in the README.**
- `README:72`: "legacy-layout Saber libapp headers complete but string pool partial".
- Dart entry line 35: "`libapp.coverage:complete` is scoped to the reader's section/header contract"; line 48: "## What complete does not mean". Its table shows both instruction symbols with `magic_valid:false`, which is by design and not a data-header failure.
- The substance matches. The wording can be read as "all four snapshot headers validated". Fix option: add "(reader-contract scope)" to `:72`.

**A6 — low (Observed). The new coverage row names no T1 verb token.** `README:72` names no verb, while the R22 rows at `:70` and `:71` name theirs. Name-based lookup in the README therefore misses `inspect-signal-decoders`, `decode-signal-recording` and `inspect-dart-aot`. Fix option: add those tokens to `:72`.

**A7 — low (Observed). Unreconciled R22 "not counted" line.** `README:71` says "inspect-dart-aot refuses missing dynamic snapshot symbols and is not counted". That is true for the R22 carrier and must stay under the prior-rows rule. `README:72` now holds the same verb for a different carrier, and the reconciliation appears only inside the knowledge entries. Fix option: add a cross-reference clause to `:72` only.

**A8 — pass (Observed). Row descriptions match their targets.**
- "tool-subject decoder catalog with a signature-module failure": the signal entry's diagnostics paragraph reports a `signature` decoder load failure, and that module is excluded from the returned catalog.
- "selected synthetic/public UART annotations, not hardware acquisition": the signal entry says `uart-hi.bin` is inert synthetic and the official sample is third-party. `hardware_acquisition:not-performed` is a provider declaration.
- "legacy-layout Saber libapp headers complete but string pool partial, not universal Dart/source recovery": the Dart entry reports `string_pool.coverage:partial`, no source recovery and no SDK identification.
- Lessons gist "reportless-seat uncertainty; no replacement credit": supported by `corpus/lessons/round-23.md` lines 51 and 70.

### B. "map106" and held counts

**B1 — pass (Observed). 106 is a file count.** `git ls-tree -r --name-only C corpus/knowledge | grep -c '\.md$'` → `106`. At B it is `104`; the delta is the two R23 entries.

**B2 — pass (Observed). Every knowledge basename occurs in the README.** A per-basename `grep -qF` loop found 0 unmapped at C and 0 unmapped at B. This is substring presence, not proof that each file has its own row.

**B3 — pass (Observed). README is outside the counter.** `count-c1.py` reads `corpus/SOURCES.md` (lines 86–91), `corpus/knowledge/` (line 94), the round-20 catalog (line 95), and the round-22/23 evidence roots. It never reads `corpus/README.md`, so README edits cannot change k.

**B4 — pass (Observed). Held 4/6 and catalog 137/153 come from the recorded run, not from the map.** `.ufo/waves/round-23/verify/initial/after-c1.json` @C: `source_rev` 6615aea; `expected_exit` 1, `exit` 1, `passed` true. Its stdout reports `finding` `c1_incomplete`, `t1_exercised_count` 4, `t1_exercised` `[identify-flutter-build, inspect-dart-aot, inspect-signal-decoders, decode-signal-recording]`, `catalog_mentioned_count` 137, `catalog_total` 153, `catalog_zero_count` 16. Not held: `debug-with-gdb`, `debug-with-rizin`. The 137/153 figure is a verb-mention census over knowledge files and must not stand in for held 4/6. Map106 must not stand in for either.

**B5 — pass (Observed) with inference. Counter inputs are unchanged from 6615aea to C.** `git diff --name-only 6615aea C` lists 18 files: `verify/initial/*`, `verify-initial-producer.json`, `LOG.md`, `SCORECARD.md`, `corpus/lessons/round-23.md`. None is a counter input. [Inferred: the recorded 4/6 applies to C's counter inputs. This seat did not re-run it.]

**B6 — Inferred.** The W1-to-C change in catalog counts (135→137 mentioned, 18→16 zero) fits the two signal verbs gaining their first corpus mentions. Not verified by regex.

### C. Stale W1 proposal findings, re-evaluated at C

W1 report `.ufo/waves/round-23/w1/CoverageMap.md` @C: file sha256 `aa46c5f9eeb8453c674a1fa3acac9c538ce0574dfe4f56083d90e97a6ca69268`. Its body hash (`sed '$d' | sha256sum`) is `5bc074f0d5d5a6d05f8d5a9df0f898125ebcbbadd78157b8fb8f2e4d0371c628`, which equals its trailer, so the report is intact.

| # | W1 item | W1 claim | Status at C |
|---|---|---|---|
| 1 | F1 counter at a3c92eb | k=1/6; catalog 135/153, zero 18 | Superseded. At 6615aea (`after-c1.json`): k=4/6, catalog 137/153, zero 16. W1 predates the landed rows. |
| 2 | F1 `SELFTEST_MANIFEST_SHA256` read as `UNSET`, then `ad1b4462…` | concurrent-edit observation | Superseded. `count-c1.py:25` @C = `458b30d5…`. `frozen/expected-v2.json` sha256 @C = `458b30d5…` (match). Neither `UNSET` nor `ad1b4462` occurs in `count-c1.py` @C. |
| 3 | F2 Dart witnesses = `connect-dart-symbols/*.envelope.json` (`ev_dcdab9…`, `ev_04072…`) | proposed own-work family | Not landed as witnesses. The Dart entry (line 31) mentions that directory only as non-witnesses, and no R23 knowledge text cites a `.ufo/waves/round-23/evidence/c1/…json` path from it, so the counter cannot bind it. Landed S061 cites L1's `inspect-dart-legacy-saber.envelope.json`. |
| 4 | F3 no sigrok/Dart knowledge before R23 | pre-wave census | Historical. No longer true at C. |
| 5 | F4/F5 `inspect-dart-aot` mention-only; signal verbs "not yet exercised" | statuses | Superseded. S058–S061 and two knowledge entries exist; the counter records four verbs. Debugger verbs remain unheld, as W1 F5 said. |
| 6 | F6 proposed S058 = own-work signal family | row proposal | Superseded. Landed S058 = sigrok-cli 0.7.2 manual (docs); landed S060 = signal envelopes. |
| 7 | F6 proposed S059 = AppImage tool pin (`49d2f597…`) | row proposal | Not landed. Landed S059 = sigrok-dumps UART README. The AppImage digest appears only in the knowledge body (signal entry line 93); `git show C:corpus/SOURCES.md \| grep -c 49d2f597` = 0. |
| 8 | F6 proposed S060 = Dart connect family | row proposal | Superseded by landed S061 (L1 legacy-layout envelope). |
| 9 | F6 insertion at SOURCES line 64 | location | Still correct: S058–S061 occupy lines 64–67. 61 registry rows, no duplicate IDs. |
| 10 | F6 eligibility rules: `source:` first line, ID ≥58, tier A/B, status mined, date 2026-10-21, exact used-by paths without backticks | rules | Landed rows satisfy them: 13 split cells each, tier A, status mined, date 2026-10-21, exact used-by paths; both knowledge files start with `source:` and an S-ID. |
| 11 | F7 caveats (decode-invalid-decoder uncounted; carrier signature unverified; dart_version null; PYTHONHOME diagnostics) | caveats | Still valid. Landed text carries them, e.g. S061 "no archive-index/APK signature verification is asserted". |
| 12 | Open risk 8: S059 host-local AppImage path | risk | Superseded by the landed S059 choice. The host path persists only in knowledge text. |
| 13 | README:70–71 cited | anchors | Still correct at C. |
| 14 | Report integrity | body hash | Intact (see above). |

### D. Out-of-item observations (route to L1)

**D1 — Observed. Token-merge defects in committed R23 bytes.** No counter effect: `count-c1.py` reads only SOURCES cells 1, 4, 8, 9 and 11 (lines 86–91 and 107), and never the evidence cell. These are readability defects.
- `corpus/SOURCES.md:64`: `opened2026-10-21`, `sigrok-cli0.7.2`. `:65`: `opened2026-10-21`, `and625kHz`, `at9600baud`. `:66` and `:67`: `opened2026-10-21`. Earlier rows at `:55`–`:63` use `opened 2026-10-21` (six rows).
- `corpus/SOURCES.md:111` round-23 log line: `round23`, `identified5`, `screened5`, `included4`, `excluded1`.
- Signal entry: line 1 and line 107 `sigrok-cli0.7.2`; line 17 `reports110`; lines 22 and 108 `Python3.5.2`; line 41 `at960000Hz`; line 69 `,625kHz` and `at9600baud`; line 76 `retains12885`; line 88 `this6.5.0`.
- Dart entry: line 8 `Saber1360103`. The R22 entry names the carrier `saber_1360103` (`corpus/knowledge/2026-10-21-r22-flutter-positive-dart-refusal.md:3`).

**D2 — Observed. S058–S061 are structurally valid for the counter.** `awk -F'|'` gives NF=13 for all four rows. Each row has tier A, status `mined`, date `2026-10-21`, and exact used-by paths. The registry has 61 S-rows and no duplicate IDs.

**D3 — Observed. AppImage registration gap.** The digest `49d2f597ec3ed3d71bfeb0465474ec2aac084fa1f66cbb132d996f7c9f50b614` appears only in the signal entry (line 93). No registry row covers it, so the sigrok tool-identity claim rests on knowledge text and a host path. Route to L1.

## Produced files and hashes

- `.ufo/waves/round-23/w2/CoverageMap.md`: this report. Its own sha256 is given in the delivery message, since a self-hash cannot be embedded.

## Installs

None. No package, tool, config or pacman transaction.

## Open risks

1. The held count (4/6) was not re-measured at C by this seat. The designated run seat should run `count-c1.py --rev 2838351450ff1ee4baa620c962a1153450d53311` once. Tree identity makes the recorded 6615aea value applicable, but that step is inferred (B5).
2. Markdown rendering was not run. The A3 no-impact statement is inferred.
3. A4, A5, A6 and A7 are presentation or precision choices; L1 decides.
4. The source-census control was not re-run here. The only evidence is the recorded 12/12 `summary.json` at 6615aea.
5. These are author-side findings only, not outside admission.
