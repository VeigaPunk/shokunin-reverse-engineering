# R50-C2 atom critic (seat C2AtomCritic, round 50 wave 1, pre-freeze)

Base `7c678ae6d97aedb969fd253b52b3d2882ef1e186` (lane `kaidoku-shokunin`). Attacked: the B1–B11 draft atom list in `.ufo/waves/round-50/draft/plans/round-50-claims.md` (R50-C2 section). Lane tree read-only (`git show` / `ls-tree` / `cat-file` only). Nothing committed, staged or stashed in the lane. Scratch `/fast/scratch/hyaku/kaidoku-r50/C2AtomCritic` (removed after receipts were copied). No tool installed or upgraded, no pacman, no data run.

## Verdict

**Not freezable as drafted.** Of the eleven atoms: **B11 is green at base and is not an atom**; **B10 cannot be red at FREEZE** if its file is committed in the frozen `tools/round-50/` tree; **B8 cannot be bound** from committed bytes; **B9 names a heading that holds zero of the rows it needs**; **B3 omits a seat** the closure names; **B4 cites the wrong section** of the closure; **B2 is already green at base under the plan's wording**. Under plan wording (a token or phrase present in raw text), **22 of 22** single-edit forgeries of a correct landing pass, including comment, fence, duplicate, indentation and polarity forgeries. A draft tightened predicate set rejects all 22 and accepts the correct landing (a construction that shows the B-set is satisfiable, not a proof of completeness; see Limits). Round-49's frozen counter also goes green on the A9 comment and fence forgeries. The L1 should rewrite B1–B11 with the sentences in §4 before the freeze.

## 1. Per-atom state at base and under plan wording

Columns: **base** = result on the unmodified base (D0 overlay), *naive* = plan wording taken literally, *tight* = draft predicate (`tools/round-50/c2-probe.py`). `G` = green, `r` = red, `n/a` = not implemented.

| atom | base naive/tight | plan-wording forgeries accepted (naive G) | defect found | disposition for L1 |
|---|---|---|---|---|
| B1 coverage fraction | r/r | F1a, F1b, F1c (3 of 3) | "fraction" is undefined: the coverage row lists several `N/N knowledge files` fractions; the row's leading fraction is dated "at the round-47 landing". The plan text "`138/138` at the base vs 139" is wrong for the base: `git ls-tree -r --name-only 7c678ae6 corpus/knowledge \| grep -c '\.md$'` is **139** at base, so the stale value is 138 against 139. A commit cannot name its own hash, so "at REV" needs the *measured* revision named | rewrite (§4 B1) |
| B2 calibration cites verdict and measure | **G/r** | F2a (inside HTML comment), F2b (8-hex digest) (2 of 2) | **green at base under plan wording**: `rejected-harmed` appears in the round-49 A9 line of `SCORECARD.md`, `c2-final` in the round-49 section. The atom must bind to the calibration row, not the file | rewrite (§4 B2) |
| B3 round-48 seat settlement | r/r | F3a (plan wording), F3b (drops C1Battery), F3c (in comment), F3d (duplicate line) (4 of 4) | the plan's example line names C1Meaning and ScribeReportNumbers and 72, **omitting C1Battery**. The closure's routed defect 7 (`corpus/lessons/round-48-verifier-spotcheck.md`) names all three seats with no report: C1Battery, C1Meaning, ScribeReportNumbers. Round-49 A4 derives the same three from `.ufo/waves/round-48/r48-w1-results.json` at base (seat statuses sit inside escaped `output` strings, not a `status` field) | rewrite (§4 B3) |
| B4 closure per-axis correction | r/r | F4a (fenced), F4b (wrong source row) (2 of 2) | "per-axis table" is wrong: that table (closure lines 103–107) has coverage, depth, calibration only. The quality and discernment verdicts are in the trend list at closure **lines 125–126** (`quality — harmed`, `discernment — improved (decision-level only)`) | rewrite (§4 B4) |
| B5 receipts named | r/r | F5a (sha dropped), F5b (prose outside section) (2 of 2) | "named" is a token test. The receipts exist at base: `.ufo/waves/round-48/l1/scores/c1-final-33f65a91.json` raw sha256 `6320c5d2…d86e`, `c2-final-33f65a91.json` raw `d1bb87d8…3914` (the round-49 A5 line states both) | rewrite (§4 B5) |
| B6 S149 correction row | r/r | F6a (duplicate), F6b (in comment), F6c (4-space indent), F6d (anchor names DESCRIPTION) (4 of 4) | (i) census `supersedes` mask: any row whose teaches contains `supersedes` suppresses the E04 duplicate-URL check, target unchecked (`w2/W2C2Registry.md` F3, reproduced by that seat on `S999`, `S146`, `S147`); (ii) the FreeBSD snapshot marks sections with `<a id="ERRORS">`, not `<h2>`/`<h3>`, so the round-49 `html_norm`/`section_of` returns no heading for the quote (`corpus/evidence/round-49/c2/freebsd-sysexits.html`, `id="ERRORS"` at line 1080). A locator for this snapshot must be marker-aware (the probe's extension, §3) | rewrite (§4 B6) |
| B7 S147 tier-B row | r/r | F7a (tier cell A, teaches says tier B), F7b (in comment) (2 of 2) | "tier B per CORPUS tier text": the tier definitions live in the **fleet** file `/home/vgpnk/Projects/shokunin/CORPUS.md:93-97` ("B: strong secondary (expert write-up…, survey, textbook)"), outside the lane. A counter reading it binds a moving fleet file and must pin its sha or the tier sentence. The B direction itself is supported by that text | rewrite; pin CORPUS sha (§4 B7) |
| B8 S138 grounding row | r/**n/a** | not run | **cannot be bound from committed bytes**: no committed 22-member listing exists (`git grep` for the member name finds only round-44 counters); `tools/round-49/carriers.json` holds **9** `sha256` entries, not 22. The S138 anchor (`22 members / 152 B / 7 distinct sha256`) reports fetched contents-API data. "a located quote that *grounds* the census" is judgment: the round-49 closure (`corpus/lessons/round-49-verifier-spotcheck.md:71`) says the located quote grounds one directory name, not the census | **drop "grounds the census"**, or commit the 10 listings in the freeze and re-derive; otherwise the atom is not evaluable (exit 2) |
| B9 registry census (`tools/round-49/**`) | r/r | F9a (fenced rows), F9b (`0=not met; 1=violation; 2=usage`), F9c (new heading) (3 of 3) | **the named heading holds zero rows**: `## Local round-evidence gate registry` (SKILL.md:772) contains the interactive-r1 rows only (`git show 7c678ae6:SKILL.md \| awk` → 0 `tools/` rows). The round-44..48 instrument rows sit under `### Round-44/45`, `### Round-46` subsections of `## SquashFS recursion through sasquatch — round 36` (SKILL.md:1557, rows 1693–1761). Six paths to register at base: `tools/round-49/{c1-controls,c1-counter,c1-oracle,c1-run}.py`, `c1-run.sh`, `c2-mismatch.py`. Polarity: the round-48 `C1Gold` critic showed `0=not met; 1=violation; 2=usage` passes a regex meaning check | rewrite; pin the heading (§4 B9) |
| B10 selftest `tools/round-50/selftest-r49-c2.py` | r/**n/a** | not run | **structural**: the plan freezes all of `tools/round-50/` at FREEZE. If the selftest is committed before FREEZE, it is green at FREEZE whenever its expected values match its output, so the do-nothing overlay cannot turn it red. Expected values authored in the same file are self-consistent by construction. Also the closure asked for a `--selftest` on `c2-mismatch.py`, which is frozen and cannot be edited | move the selftest out of the frozen tree or make it REV-only; pin expected values by sha in the counter (§4 B10) |
| B11 round-49 freeze agreement | **G/G** | n/a (green at base) | **green at base, so not an atom.** All four declarations read `decc5697bfd4ec1e9de4a762ad199d9bd9c4230d`: `corpus/lessons/round-49.md` line 4, `SCORECARD.md:3754`, `LOG.md:3453`, `.ufo/waves/round-49/l1/FREEZE`. A do-nothing overlay leaves it green, so the battery fails. The header gap (W2 F9, M02) is real: the round-49 frozen counter exits 0 with the lesson header changed to `b6f7ca2a…` (receipt below). Keep as a non-battery guard, or restate as a round-50 atom (round-50 lesson header, round-50 SCORECARD section, round-50 LOG entry and `.ufo/waves/round-50/l1/FREEZE` agree; each absent at FREEZE, so red) | drop from atoms or restate (§4 B11) |

## 2. Structural findings (not per-atom)

- **S1 Battery coupling.** B1 and B2 read the same `## Owned axes` table; B3, B4 and B5 read one heading; B6–B8 read `corpus/SOURCES.md`; B9 reads SKILL.md. A single-mutation overlay that changes a shared heading flips several atoms, which breaks "each mutation turns exactly its own atom red". Key each atom on its own line or cell and name the heading once.
- **S2 Stripping is absent in the reused machinery.** The round-49 counter has no comment or fence stripping; forgeries in `<!-- -->` or fences go green (below). Its helpers also match only rows with a 0–3-space indent (`registry_rows`, `ROW_RE`) and mark only `<h2>`/`<h3>` (`html_norm`). Any reuse must add stripping and a marker-aware locator, and say so.
- **S3 FREEZE count.** With B10 out of the FREEZE state and B11 green, the expected FREEZE count is **9** (B1–B9 red). The plan says only "N>0"; state 9 and the do-nothing set.
- **S4 Re-derivation revisions.** Inputs the repair does not touch read at base (B2 `c2-final.json`, B3 results, B4 closure, B5 receipts): correct. Registry rows read at REV (B6–B7, B9): correct. B1 must name the measured revision, not REV (see table).
- **S5 Census masks.** Because `supersedes` suppresses E04, the census cannot catch a duplicate correction row; the atom must check the target id exactly.

## 3. Commands, exit codes, sha256 (receipts under `w1/C2AtomCritic/receipts/`)

Draft probe (seat instrument, `w1/C2AtomCritic/tools/round-50/`):

| step | command | exit | result | sha256 (stdout) |
|---|---|---|---|---|
| probe matrix | `SCR=<scratch> python3 -I -B .ufo/waves/round-50/w1/C2AtomCritic/tools/round-50/c2-probe-run.py > <scratch>/probe-stdout.jsonl` | 0 | 25 cases (`G`, `D0`, `D11`, 22 forgeries), 11 atoms each; matrix `receipts/matrix.md` | `c3ed983bc58e03759f18b3498409da7c6688f097500a2177542690632bfcebd0` (`receipts/probe-stdout.jsonl`) |
| probe source | `sha256sum c2-probe.py c2-probe-run.py` | 0 | — | `c2-probe.py` `cb68f7b8aef6c4b1ca31f1c6b89aed758c99eb8cd84e34896fdd4694fe343cab`; `c2-probe-run.py` `eadada50d5a64027ff6a0740649a488fe3f1dd0398ffaf5a553309f71442ae54` (`tools/round-50/SHA256SUMS.txt`) |

Round-49 frozen counter run on real fixture commits (`tools/round-49/c2-mismatch.py` as frozen at FREEZE `decc5697…`, `GIT_NO_REPLACE_OBJECTS=1 python3 -I -B`), scratch clone `git clone --shared` detached at base, toplevel asserted, identity set in the clone only:

| fixture | commit | exit | mismatches | red | stdout sha256 |
|---|---|---|---|---|---|
| base (control) | `7c678ae6` | 0 | 0 | none | `488524a4f02852a0721a7eb421157348b0c281c2fff1edad181ad095f6127b5c` |
| A9 line wrapped in `<!-- -->` | `559ab8a623f992976a1203964491fd8001630e49` | **0** | 0 | none | `8756fe1af8795f1e0a6cb77ec313b93d5fde78470e0650196883c7ee66335cfb` |
| A9 line inside a code fence | `5d6361341ea164b0dd51471583016f0c447d718d` | **0** | 0 | none | `c639a2507638d3f5839fcc1d2825994c88132b3db362ead2978c48bcf45fda47` |
| A9 line deleted (control) | `d0bf91ce5df4a0b5a8a1d8029aca4683d775ef80` | 1 | 1 | A9 | `a4ffdfcd05c48ffa51824a0b72f95ad74de225aa92378ca0a4d1ca15ccfb5a18` |
| round-49 lesson header → `b6f7ca2a…` (B11 gap) | `ac5b1b345fe27ce9af4601ae4b4ecc32bb28738b` | **0** | 0 | none | `66aef59eb4a6ce2a2810ea66c52a0c2db2484d4b757b4bac249b6596e66d01b5` |

Each fixture is one commit on the base in the scratch clone (`git -C $C add <file> && git -C $C commit`); the commit hashes above are not reproducible after scratch removal, but the edits are: the A9 wrap and fence replace the single line `- A9 verdict=rejected-harmed source=corpus/lessons/round-48-verifier-spotcheck.md calibration=harmed` in `SCORECARD.md`; the header change replaces `Declared freeze \`decc5697…\`` in `corpus/lessons/round-49.md`.

Base-state checks (read-only): `git show 7c678ae6:.ufo/waves/round-49/l1/FREEZE` = `decc5697…`; `git ls-tree -r --name-only 7c678ae6 corpus/knowledge \| grep -c '\.md$'` = 139; `git show 7c678ae6:.ufo/waves/round-48/l1/scores/c2-final-33f65a91.json \| sha256sum` = `d1bb87d8…3914`; `…c1-final-33f65a91.json` = `6320c5d2…d86e`; `…round-49/l1/scores/c2-final.json` = `544167f2a6a715954152459659faa67d031ecf9f0231f185930f02ef5de61565`.

Not run: the frozen round-49 `--battery` on these fixtures (the plain exit is the finding); the B8 listing search beyond `git grep` for the member name; a B10 selftest (not implementable before FREEZE).

## 4. Proposed predicate sentences (for the L1 to freeze)

- **B1** The first `N/N knowledge files mapped at <40-hex>` in the visible (comment- and fence-free) `| coverage |` row of `## Owned axes` has N equal to the count of `corpus/knowledge/*.md` at that hash, and the hash is a commit. The hash is the measured revision the L1 records (not REV). Red if the row has no such match.
- **B2** The visible `| calibration |` row of `## Owned axes` contains `rejected-harmed` and the full 64-hex sha256 of `.ufo/waves/round-49/l1/scores/c2-final.json` at base.
- **B3** Exactly one visible line starting `- B3 ` in `## Record corrections — round 50`, equal to `- B3 seats=75 reports=72 missing=C1Battery,C1Meaning,ScribeReportNumbers`, where the three values are re-derived from `.ufo/waves/round-48/r48-w1-results.json` (parsed `output` strings) and the base tree (same rule as round-49 A4).
- **B4** Exactly one visible line `- B4 quality=harmed discernment=improved-decision-level-only source=corpus/lessons/round-48-verifier-spotcheck.md`; the closure at base contains `quality — harmed` and `discernment — improved (decision-level only)` at its trend list (lines 125–126).
- **B5** Exactly one visible line `- B5 tip=<40-hex, a commit> receipts=<c1 path>,<c2 path> sha256=<raw sha256 of each>`, with the two receipts at base.
- **B6** Exactly one visible registry row (0–3-space indent, outside fences and comments) whose teaches cell opens `supersedes S149 —`, with tier cell `C`, status `rejected`, a new id, the S149 row byte-identical to base, the anchor carrying the 64-hex sha256 of `corpus/evidence/round-49/c2/freebsd-sysexits.html` and a quote located under a heading the anchor names, using a marker-aware locator (`<a id>` and `<h2>`/`<h3>`).
- **B7** As B6 for `supersedes S147 —`, tier cell `B`, status `mined`, anchor pinning `corpus/evidence/round-49/c2/popper.html`, and tier `B` checked against `CORPUS.md` at a pinned sha256 (fleet file, outside the lane).
- **B8** Drop "grounds the census". Keep: the quote is located in a committed snapshot whose sha is pinned in the row. A census claim needs committed listing bytes or it is not evaluable.
- **B9** Each of the six `tools/round-49/*.py|*.sh` paths is cell 0 of exactly one visible row inside the section the L1 names (pin it: a new section, or the existing round-44–48 subsections under SKILL.md:1557); verdict map `0=<met-class>; 1=<not-met-class>; 2=<could-not-evaluate-class>` with polarity checked (`0=not met` is red).
- **B10** Remove from the atom set, or place after FREEZE; any expected values are pinned by the counter's own sha, not written by the selftest.
- **B11** Drop from the battery (guard only), or restate as a round-50 REV-only agreement (lesson-50, SCORECARD round-50, LOG-50, `.ufo/waves/round-50/l1/FREEZE`).

Plan text to correct as well: B3 names three seats; B4 source is the trend list; B9 heading; B10 location; B11 green at base; B1 base count (139, not 138-vs-139 at REV); B8 wording.

## 5. Probe results (what the matrix shows)

- Genuine landing `G` (the B-corrections written as §4 sentences, plus S150/S151 and six SKILL rows): **green on all tight predicates** (B1–B7, B9, B11); B8 and B10 not implemented. So the set is satisfiable without tripping any tightened predicate.
- Base `D0`: naive B2 green (plan wording passes at base); tight red everywhere except B11 (green, expected).
- Forgeries (22, each a single targeted edit of `G`, `receipts/matrix.md`): naive green **22/22**; tight red **22/22**.
- Two probe bugs found and fixed during the run, reported for transparency: (a) the first tight B6 had no marker-aware locator, so the genuine landing failed; (b) the first tight B6 checked the snapshot heading but not the heading the anchor names, so `F6d` passed. Both fixed; the final matrix is `receipts/matrix.md`.

## 6. Limits of this seat

- The probe is a draft, in memory, and not the frozen counter. The 22 forgeries are chosen by this seat to test its own tight predicates; a 22/22 kill is not evidence of completeness, and round 49 found further misses after its own battery passed (W2C2Forge, W2C2Mutate: 13 of 30 green).
- Not implemented: B8, B10. The `G` landing is a construction from the plan's words, not an L1 draft.
- Round-48 `results.json` is parsed as the seats' `output` strings, so the B3 derivation is only as good as that parse.
- The CORPUS tier text (B7) is read from the fleet file, not from the lane.

## Tools and channels

None installed, upgraded or removed. No pacman transaction. Scratch `/fast/scratch/hyaku/kaidoku-r50/C2AtomCritic` removed after receipts copied.
