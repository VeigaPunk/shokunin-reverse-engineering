# Round-30 wave-2 review — corrections (ReviewCorrections)

Attacked: the round-30 corrections — the SHONEN pointer fix, the R29-C1 "published" provenance corrections at every site, the SCORECARD:3166 correction and the l7-02 pointer. Diff `d210fb8f..main`, main = `3502b94c5b93d86c5d67866035fd150899456295`. Read-only: I ran git read commands only (diff, show, log, grep, cat-file, rev-parse). No REA runs, no counters, no carrier or mutant access, no installs. The `/skill:godspeed` file is not on this host (a filesystem search for `*godspeed*` returned nothing at 2026-10-23T03:12Z), so I worked from the assignment text alone.

## Verdict

- Deletions: **holds.** There is exactly one deleted line in the whole `d210fb8f..main` diff (all files, not only the seven named), and it is the SHONEN pointer line.
- SHONEN 97-118 and 116-118: **holds.**
- Every site the scribes named got its appended correction, and no old line was deleted: **holds.**
- SCORECARD:3166 correction: **holds.** It is byte-identical to the scribe draft.
- l7-02 pointer: **holds, with a scoping overstatement** (Low-1 below).
- Line pointers inside the new correction text: **fails once.** The README correction points to the wrong row (Medium-1).

## Findings by severity

### Medium-1 — the `corpus/README.md` correction points to the wrong row (observation)

The correction at `corpus/README.md:233` ends "(rows 79 and 175 above)". Round 30 inserted two coverage-map rows at `:81-82` in the same commit series. That pushed the R29 knowledge-index row from line 175 at the base to line 177 at main. At main, line 175 is the **round-28** held-out row.

- Command: `git show main:corpus/README.md | awk 'NR>=175 && NR<=177'` and `git show d210fb8f:corpus/README.md | awk 'NR==175'`. Exit 0, 2026-10-23T03:13:22Z.
- Main excerpt: `175|| \`2026-10-22-r28-evm-heldout-selector-naming\` | Held-out score …` and `177|| \`2026-10-22-r29-evm-fresh-selector-naming\` | … 16 fresh published-interface car…`
- Base excerpt: `175|| \`2026-10-22-r29-evm-fresh-selector-naming\` | …`
- Cause (inference): the scribe took its line numbers from the base, as `ScribeR29Provenance.md:22` shows ("`corpus/README.md:79` … Same README, `:175`"). The integrator then added rows above line 175 and copied the numbers without re-anchoring them.
- Fix: append a pointer correction that says "rows 79 and 177". Row 79 is still correct (`[same] corpus/README.md:79`).

### Low-1 — the l7-02 pointer claims more is superseded than round 30 tested (observation plus inference)

`corpus/knowledge/2026-10-16-l7-02-inspect-rust-binary.md:14` says the whole clause "Untested: non-ELF inputs, missing-metadata/rejected-input behavior" is superseded for REA 6.5.0. Rejected-input behavior was only exercised on ELF. The refusals entry says so itself: `corpus/knowledge/2026-10-23-r30-rust-auditable-refusals.md:49` reads "One container (ELF x86_64) … PE and Mach-O edits, the 256 MiB input cap and the 8 MiB report budget were not exercised." The parentheticals in the pointer do name "19 accept/refuse signatures on ELF mutants", so a careful reader can recover the scope. But the lead verb "superseded" still covers non-ELF rejected input, which remains untested.

- Command: `git show main:corpus/knowledge/2026-10-23-r30-rust-auditable-refusals.md | grep -n -i -E '…PE|Mach-O…'`. Exit 0, 2026-10-23T03:13:5xZ.
- Fix: make it "partly superseded", and say that non-ELF rejected input and the 256 MiB and 8 MiB bounds stay untested. The latter already matches SCORECARD:3240 "planned".

### Low-2 — R29 "published" statements outside the scribe's six-file search carry no correction (observation)

The scribe searched only PROVINCE, the r29 entry, SCORECARD, README, LOG and SKILL (`ScribeR29Provenance.md:11`). A lane-wide search finds more R29-C1 statements that call the 16 lists published, with no correction attached:

| site | text | in the diff? |
|---|---|---|
| `corpus/knowledge/2026-10-22-r25-evm-selector-name-resolution.md:210-211` (round-29 pointer) | "16 fresh published-interface carriers: named 122, right 122, wrong 0" | no |
| `corpus/lessons/round-29.md:9-10` | "16 fresh carriers compiled from published interface lists" | no |
| `tools/round-29/make-carriers.py:4` (frozen instrument docstring) | "holding a published interface's function list" | no |
| `.ufo/waves/round-29/claims.json:49` (frozen claim `limits`) | "compiled stubs that hold a published function list" | no |

- Command: `git grep -n -i -E 'published[- ](interface|function list|names|list)|public names' main -- . ':!.ufo/waves/round-30' ':!.ufo/waves/round-29/w1'`. Exit 0, 2026-10-23T03:13Z.
- Inference: routed defect 5 (`corpus/lessons/round-29-verifier-spotcheck.md:127`) asks only for the entry and PROVINCE ("stop calling the lists 'published' in the entry and PROVINCE"), and both are done. However, routed defect 6 (`:128`) cites the lane rule "§Evidence standard 'Corrections sweep every mention'". Under that rule, the r25 pointer and the round-29 lesson are unswept mentions. The frozen `claims.json` and the instrument docstring are frozen artifacts; listing them is enough, and they should not be edited.

### Low-3 — the SCORECARD provenance correction cites one line that does not say "published" (observation)

`SCORECARD.md:3230` cites "`SCORECARD.md:3171`, `:3177`, `:3182`". Line 3177 is the R29-C1 claim row. It says "16 fresh hex-screened carriers" and contains neither "publish" nor "public". The search `git show main:SCORECARD.md | sed -n 3177p | grep -o -i '…publish…\|…public…'` printed nothing, exit 1, 2026-10-23T03:13Z. This does no harm, but it is not a "published" site. 3171 and 3182 are correct.

## SHONEN pointer (`SHONEN.md:12`) — holds

- New text: "`PROVINCE.md:97-118` (the `## Adjacent` refusal list; safety refusal at :116-118; range refreshed round 30 from `95-116`/`:114-116`, which drifted +2 after Frontier additions in `2832c5b3` and `2f18996d` …)".
- `git show main:PROVINCE.md | grep -n '^## '` gives `73:## Frontier`, `97:## Adjacent`, `269:## Adjacent — round-23 explicit exclusion`. Line 118 at main is "licensed for reuse" `(unowned)`.", which ends the list (119 is blank). Lines 116-118 are the "Quality/safety verdicts on findings" bullet. Exit 0, 2026-10-23T03:12Z. **Observation: 97-118 and 116-118 are exact.**
- Drift attribution: I printed the line of `^## Adjacent$` at each commit that touched PROVINCE. Results: `c4ec7a2e 95`, `2832c5b3 96`, `071270b5 96`, `2f18996d 97`, `24da3459 97`. `git show --unified=0 2832c5b3 -- PROVINCE.md` gives `@@ -93,0 +94 @@` (+1 line), and the same for `2f18996d` gives `@@ -94,0 +95 @@` (+1 line). Both insertions fall inside `## Frontier`. Exit 0, 2026-10-23T03:12Z. **Observation: the +2 drift and both named commits are correct.**
- Base PROVINCE already had `## Adjacent` at 97 (base 97-118 is identical to main). The round-30 PROVINCE addition was appended at EOF (`@@ -326,3 +326,15 @@`), so it shifts nothing.
- The new line keeps the old `95-116`/`:114-116` strings and the round-25 note in its text, so the history is still readable even though the line was rewritten in place.
- The other SHONEN pointers are unchanged and still hold: `PROVINCE.md:8-14` holds the 6.7.0 and 6.5.0 pins, and `:24` contains `v42/207`.

## Per-site table — R29-C1 "published" sites (from `ScribeR29Provenance.md`)

"Old line unchanged" means the base line and main line are byte-equal at the same number, from `git show <rev>:<file> | sed -n <n>p` for both revs, 2026-10-23T03:13Z, exit 0.

| file | site (scribe's number) | old line unchanged at main | correction appended at | correction line cites | verdict |
|---|---|---|---|---|---|
| `PROVINCE.md` | `:95` | yes (same number) | `:340` (EOF, in the round-30 section) | no line number | holds |
| r29 entry | `:5`, `:10`, `:76`, `:82`, `:96-97` (`:1` scoped to n04, correctly not a site) | yes, all six | `:108` (EOF) | no line number | holds |
| `SCORECARD.md` | `:3171`, `:3182` | yes, both | `:3230` (round-30 section, defect 5 at `:3225` points to it) | `:3171`, `:3177`, `:3182` | holds; `:3177` is not a "published" site (Low-3) |
| `corpus/README.md` | `:79`, `:175` (base) | yes; `:175` moved to `:177` at main (rows inserted at `:81-82`), text unchanged | `:233` (EOF) | "rows 79 and 175" | **fails: 175 should be 177** (Medium-1) |
| `LOG.md` | `:2997`, `:3004` | yes, both | `:3020` (round-30 entry, EOF) | `LOG.md:2997`, `:3004` | holds |

Core sentence: `git grep -n -F "only carrier n04 rests on an opened source (S088); the other 15 lists … not opened published interfaces" main` finds it in exactly those 5 lane files (`LOG.md:3020`, `PROVINCE.md:340`, `SCORECARD.md:3230`, `corpus/README.md:233`, r29 entry `:108`), plus the round-30 wave records. The prefixes differ only by the added "round 30" or "round 30, routed defect 5 of …". Exit 0, 2026-10-23T03:13:22Z.

## Per-site table — the other corrections

| correction | site | check | verdict |
|---|---|---|---|
| SCORECARD:3166 (`ScribeScorecard3166.md`) | old line `SCORECARD.md:3166` | byte-equal base and main ("covers 31 of 36 keys; 5 `system:magic` keys have none") | not deleted, holds |
| SCORECARD:3166 | bullet `SCORECARD.md:3229` | `cmp` of the draft's bullet (`/fast/scratch/hyaku/kaidoku-r30/seats/w1/ScribeScorecard3166/SCORECARD-correction-draft.md`, sha256 `be95fd7b…94aef`, matching the scribe) against main line 3229 printed `BULLET_IDENTICAL`. Facts match `.ufo/waves/round-29/after/canonical-keyhash.txt:3` `keys=36 with_signature=31 magic=5 mis_keyed=6` and the r28 entry `:89-95` "(5 keep none, 6 keep another selector's)" | holds |
| SCORECARD:3166 | cited ranges | the spot-check `:127-129` routes defects 5-7. `:128` asks for "a named correction (append-only …)" at 3166, which is met | holds |
| l7-02 pointer | `corpus/knowledge/2026-10-16-l7-02-inspect-rust-binary.md:11-14` (appended section) | lines 1-10 unchanged (numstat `4 0`). Both target entries exist at main (`git cat-file -e`). The quoted clause matches `:10` verbatim | holds; scope overstated (Low-1) |
| LOG motivating quote | `LOG.md` round-30 entry | cites `l7-02…md:10` "Untested: non-ELF inputs", which is present at `:10` | holds |

## Deletions

Command: `git diff --numstat d210fb8f main | awk '$2>0'` gives `1	1	SHONEN.md` and nothing else. Also, `git diff --unified=0 … -- <7 named files> | grep '^-'` (excluding `---` headers) shows one line: the old SHONEN `PROVINCE.md:95-116` pointer. Exit 0, 2026-10-23T03:12Z.

Numstat for the 7 named files: LOG 12/0, PROVINCE 12/0, SCORECARD 37/0, SHONEN 1/1, README 8/0, l7-02 4/0, r29 entry 2/0. **Deletions found: 1, the SHONEN pointer line only. This equals the expected count.**

## Residual risk and verification gaps

- Append-only placement (inference): the PROVINCE correction sits at `:340`, 245 lines below the statement it corrects at `:95`, in a different section. The README, SCORECARD and LOG corrections are similarly far from their sites. A reader of the old line sees no forward pointer. This follows the lane's existing convention (the round-27 note at PROVINCE EOF), so it is not a defect.
- I did not open external sources or re-run the round-29 keyhash audit. The 3166 facts rest on the committed receipt and the r28 entry.
- No `lsp` server applies to these Markdown, TSV and JSON files. All "site" evidence is from literal git text tools, which is right for line-anchored prose.

## Hashes of the main blobs read (`git show main:<f> | sha256sum`)

| sha256 | file |
|---|---|
| `ba680ed3be110a6bb948cff8d099331ada3a6424cff1087863fa53394099b869` | `SHONEN.md` |
| `4b48b5bac5961c83abd5cd36c631f16fb110fa2f812fdd2bd913b7f0b809a3f6` | `PROVINCE.md` |
| `e035f6733fac469fad9b20429ca07e13c63fa56b432ee1564b8721a12ba76c52` | `SCORECARD.md` |
| `3f30403c9ae848211348fd053b5329a8d6bb7c6dab96992e3c7643e40c144a12` | `LOG.md` |
| `379281f6c827f84c58ebf3c17128a532f5fba9feaf0fda6dfb7e393f26608b35` | `corpus/README.md` |
| `f0c6831d8f39bdf0e72a068bdb2ae9b92e132fbc6d9234381d23ebf6042953b5` | `corpus/knowledge/2026-10-22-r29-evm-fresh-selector-naming.md` |
| `365ed86c9ba1097bb711d519833eb56cafa6c408a3cddd5298320566068cb9fe` | `corpus/knowledge/2026-10-16-l7-02-inspect-rust-binary.md` |
| `c1b344760c812bf9b069a9dcb5dc27556da44303280fde70b49dca943d1fbd23` | `.ufo/waves/round-30/w1/ScribeR29Provenance.md` |
| `cecd037598c94d704f43ca300802f1ecbcf747bc4418d60ea555ba8d11d5a583` | `.ufo/waves/round-30/w1/ScribeScorecard3166.md` |
| `78e4febf842cff649ba322be88b141df78e547ab0d8f87e4df3f5e3e0dac76ad` | `corpus/lessons/round-29-verifier-spotcheck.md` |

Scratch artifacts: none. Two temporary files used for the `cmp` (`/tmp/rc_draft.txt`, `/tmp/rc_main.txt`) were deleted. Installs: none. Processes: none left running.

Report: .ufo/waves/round-30/w2/ReviewCorrections.md
