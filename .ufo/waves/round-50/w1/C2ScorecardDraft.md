# C2ScorecardDraft — round 50 wave 1 (pre-freeze): SCORECARD repairs for R50-C2

Base `7c678ae6d97aedb969fd253b52b3d2882ef1e186` (lane HEAD unchanged; `git status` outside `round-50/` clean). Read-only on the lane tree; no install; no git mutation in the lane. Fixtures in a `git clone --shared` scratch clone (toplevel asserted before each commit; identity set in the clone only); scratch removed after copying receipts. Receipts: `.ufo/waves/round-50/w1/C2ScorecardDraft/receipts/` (`receipts.sha256`). Checks run 2026-10-28; final lane-HEAD check 23:40:39Z.

## Verdict

**Draft complete, but the brief's correction grammar is partly inert and the section placement must change before the freeze.** Three things the L1 must fold in:

1. **`corrects verdict …` and `corrects receipts …` are not parsed by any round-47/48/49 counter.** The round-48 `CORR` regex accepts only `seats|window|path|rev|axes|quote`; round-47 only `seats|window|path|rev`; round-49 parses no `corrects` line (exact A9 match). Such a line is silently dropped, so an atom behind it would read green by absence. The draft uses the round-49 `- B4 verdict=…` machine form for verdicts and `corrects path …` for the two receipts.
2. **The round-50 correction section must sit before `## Record corrections — round 49`, not after it.** The frozen round-49 A9 battery appends its mutation at end of file. After the round-49 section, that mutation lands in the round-50 section, A9 stays green, and the round-49 battery goes red (`A9 contradictory second line appended -> red [] noop []`, exit 1). Before it, the battery is exit 0.
3. **B8 as worded is unsatisfiable, and B3 needs its own atom.** No quote can ground a 22-member count, and the round-48 `seats` clause re-derives only the dispatch total (75), not "settled". The settlement facts (72 of 75 with artifacts; `C1Meaning` blocked; `ScribeReportNumbers` aborted) need a parser of the results `output` field.

Landing text is in `.ufo/waves/round-50/w1/C2ScorecardDraft/landing-blocks.md` (Block 1 coverage leading clause; Block 2 calibration row append; Block 3 `## Record corrections — round 50`) and source-row drafts in `sources-drafts.md` (S150, S151, S152). The draft grammar harness `tools/round-50/c2-grammar-check.py` exits 0 at base (every parsed correction re-derives; the A-form and path lines resolve).

## Findings

| # | Sev | Target | Finding | Command (base or fixture) | Exit | Receipt / sha256 |
|---|---|---|---|---|---|---|
| F1 | **high** | grammar, brief §3(3) | `corrects verdict` and `corrects receipts` match no counter regex. Parsed classes: round-47 `seats\|window\|path\|rev`; round-48 `seats\|window\|path\|rev\|axes\|quote`. Verdict has no class; receipts maps to `path`. | `python3 -I -B` regex test (inline, output in `receipts/grammar-inert-test.txt`) | 0 | `501c1514…` (`grammar-inert-test.txt`); `SCORECARD.md` at base contains 0 `corrects verdict`/`corrects receipts` lines |
| F2 | **high** | placement, round-49 A9 battery | Round-49 battery mutation `A9 contradictory second line appended` = `sc.rstrip('\n') + '\n- A9 …'` (`tools/round-49/c2-mismatch.py` `mutations()`), so it writes at EOF. Fixture A (round-50 section after round-49 corrections): battery fails, A9 is a no-op. Fixture B (before the round-49 heading): green. | `git -C <clone> commit` of each placement, then `GIT_NO_REPLACE_OBJECTS=1 python3 -I -B tools/round-49/c2-mismatch.py --root <clone> --rev <rev> --freeze decc5697bfd4ec1e9de4a762ad199d9bd9c4230d --battery --json-out …` | A: 1 · B: 0 | A (`84eebc28…`, EOF): `c2-fixture-r50section.json` `700f2429…`, failing `["A9 contradictory second line appended -> red [] noop []"]`; B (`6630ad34…`): `c2-fixture2.json` `82229fe3…`, `mismatches 0`, `battery.failing []`, do-nothing red ×9. Diffs: `receipts/fixture-placement-{A-EOF,B-before-r49}.diff` |
| F3 | **high** (B3) | round-48 settlement | 75 results. Report artifact (`w1/<seat>.md` or `w1/<seat>/`) for 72; missing: `C1Meaning` (`"status": "blocked"`, `frozen_worktree_dirty`, `files_changed []`), `C1Battery` (no `w1/C1Battery.md`; receipt directory `w1/C1Battery-2/`), `ScribeReportNumbers` (`"aborted": true`). Results schema is `{agent,name,note,output}`; `status` is inside `output` text, not a top-level key. `seats` class proves only dispatch total: `w1-dispatch.json` `counts.spawn 75`, claimed `1 wave, 75 seats total` = derived `[1,75]`. | `jq '.results\|length' .ufo/waves/round-48/r48-w1-results.json`; `jq -r '.results[]\|select(.output\|test("\"status\": \"blocked\"\|\"aborted\": true"))\|.name'` → `C1Meaning`, `ScribeReportNumbers`; artifact loop over 75 names | 0 | results `8eec161e…`; harness `grammar.out.json` `db5a0623…` (`lines[0] claimed [1,75] derived [1,75]`) |
| F4 | high (verified) | round-49 counter at base | Counter at base is green; the battery is clean. | `GIT_NO_REPLACE_OBJECTS=1 python3 -I -B tools/round-49/c2-mismatch.py --root . --rev 7c678ae6… --freeze decc5697… --battery --json-out …` | 0 | `atoms_total 9`, `mismatches 0`, `battery.failing []`; stdout `44338e71…` |
| F5 | info (verified) | round-49 counter at freeze | Reproduces the W2 receipt byte-for-byte. | `… --rev decc5697… --freeze decc5697… --json-out …` | 1 | `mismatches 9`, all A1–A9 fail; `7aa900e1…` equals `W2C2Scorecard` F4 receipt |
| F6 | **medium** (B1) | coverage row `SCORECARD.md:23` | Base knowledge count is 139, not 138. All 139 stems are named in `corpus/README.md` (0 unnamed). The row's leading fraction 138/138 is the round-47 landing value. | `git ls-tree -r --name-only 7c678ae6… corpus/knowledge \| grep -c '\.md$'`; stem-in-README check (python, read-only) | 0 | 139; 0 unnamed; `2026-10-28-r49-squashfs-v1v2-core` named in README (true) |
| F7 | **medium** (B2) | calibration row `SCORECARD.md:25` | Row carries no `rejected-harmed` text and no round-49 measure. The numeric `0 → 10` is unchanged. Last-change cell reads `operator-steered r1 + luna-round-2`, which is stale. | `git show 7c678ae6…:SCORECARD.md \| sed -n 25p \| grep -c 'rejected-harmed'` | 1 (grep: no match; count 0) | Block 2 adds verdict + round-49 + round-50 measures |
| F8 | **medium** (B6) | S149 row (`corpus/SOURCES.md:155`) | Locator `DESCRIPTION` is wrong. In the committed snapshot the quote (offset 11050) follows the `ERRORS` heading (10784) and precedes the second `ERRORS` (13621); `DESCRIPTION` (10564) ends before it. The "second mirror" reason inverts provenance (FreeBSD is origin; man7 S148 is the Linux rendering). | python plain-text offsets over `git show 7c678ae6…:corpus/evidence/round-49/c2/freebsd-sysexits.html` | 0 | snapshot `1fc793a2…5dbf` = S149 pinned sha ✓ |
| F9 | **medium** (B7) | S147 row (`corpus/SOURCES.md:153`) | Tier A is wrong for an expert survey. `CORPUS.md:93–96`: A = primary/authoritative; B = "strong secondary (expert write-up with reproducible detail, survey, textbook)". Locator `2. Backdrop to Popper’s Thought` and both quotes verified in the snapshot (21-word quote at 12284, between §2 heading at 8872 and §3 at 12986; 9-word at 12719). | python offset checks over `popper.html` | 0 | snapshot `2c2d48c6…ec207` = S147 pinned sha ✓ |
| F10 | **high** (B8) | S138 grounding | B8 asks for "a located quote that grounds the 22-member census". The census is a count over LFS-pinned member bytes. `w1/C1S138Reopen.md` (round 49) records that the tree page has no sentence grounding `teaches`; its draft manifest sha `4bc53dbb…` is not the file (`06a72dd5…`). Draft S152 narrows `teaches` and grounds the census in receipts. | read: `git show 7c678ae6…:.ufo/waves/round-49/w1/C1S138Reopen.md` | — | not re-fetched (no network); pins are the round-49 receipts |
| F11 | low (B11) | freeze consistency | Already satisfied at base: lesson header `decc5697…`; `SCORECARD.md` round-49 `Declared freeze decc5697…`; `.ufo/waves/round-49/l1/FREEZE` = `decc5697…`; `LOG.md:3453` `decc5697…`. No block. | `git show <base>:…` | 0 | — |
| F12 | low | round-48 prose (not an atom) | `planned (round 49): … pin the gate.py helper …` never marked not-executed (W2 F12). Optional line in Block 3 notes. | prose | — | — |
| F13 | low | Last-change cells | Coverage and calibration last-change cells predate rounds 41, 47–49. Optional cell edits in Block 1/2 notes. | prose | — | — |
| F14 | info | `depth` | Closure's depth verdict is `improved`; SCORECARD round-48 `depth 10 → 10` is a score, not a verdict. Not a contradiction, not corrected. | prose | — | — |

## Atom map (B-atoms named in the plan)

| atom | satisfied by (landing-blocks.md) | status at draft |
|---|---|---|
| B1 coverage fraction | Block 1 (replaces leading clause of `SCORECARD.md:23`) | drafted; `<N>` filled at landing (139 at base; `<N>` = 140 if the C1 entry is admitted) |
| B2 calibration row cites `rejected-harmed` + round-49 measure | Block 2 (appends to `SCORECARD.md:25`) | drafted; round-50 measure `<N>` at landing |
| B3 round-48 seat settlement | Block 3 line 1 (`corrects seats round-48: 1 wave, 75 seats total — …`) | total re-derives (`[1,75]`); settlement text is **not** counted by the existing grammar — needs a round-50 atom parsing results `output` (F3) |
| B4 round-48 per-axis verdict | Block 3 line 2 (`- B4 verdict=rejected-harmed … quality=harmed discernment=improved-at-decision-level-only …`) | drafted in the A9 machine form; **no existing counter parses it** — needs a round-50 atom (F1) |
| B5 round-48 final receipts `33f65a91`/`8847042a` | Block 3 lines 3–4 (`corrects path …c1-final-33f65a91.json`, `…c2-final-33f65a91.json`) | both paths exist at base (harness `exists_at_rev true` ×2); sha256s in the lines |
| B6 S149 correction | `sources-drafts.md` S150 (`supersedes S149`) | drafted; quote and locator verified against the snapshot |
| B7 S147 tier | `sources-drafts.md` S151 (`supersedes S147`, tier B) | drafted; CORPUS tier text verified |
| B8 S138 grounding | `sources-drafts.md` S152 (`supersedes S138`, `teaches` narrowed) | drafted as a narrowing; the plan's wording (quote grounds census) is infeasible (F10) |
| B9 registry census (tools/round-49/**) | not this seat (SKILL.md registry). Census input: `tools/round-49/` holds six instruments (`c1-controls.py`, `c1-counter.py`, `c1-oracle.py`, `c1-run.py`, `c1-run.sh`, `c2-mismatch.py`) | not drafted here |
| B10 `tools/round-50/selftest-r49-c2.py` | not this seat | not drafted here |
| B11 freeze agreement | no block needed | satisfied at base (F11) |

## Grammar and placement rules the freeze should pin (for the L1)

- Correction lines: `- corrects <seats|path|rev|window|axes|quote> <key>: <statement>` for the parsed classes. Seats statement must contain `<n> waves, <m> seats total`. Path lines name a file that exists at REV.
- Verdicts: the A9 machine form, one line per verdict, in the round-50 section. If the round-50 counter should read a `corrects verdict` form, add the `verdict` class to its `CORR` regex before the freeze (otherwise the line is inert).
- Placement: round-50 section immediately before `## Record corrections — round 49` (line-anchored match, because the round-48 "Owned scores" prose quotes that heading).
- Block 1 `<N>/<N>`: record2's `FRAC` (`\d+/\d+`) does not match `<N>/<N>`, so the coverage row yields no fraction until the landing fills it. Fill before the freeze-measured landing run.

## Not run / limits

- The round-50 counter (`c2-record.py`) does not exist; the grammar harness is a draft check, not the counter. Its exit 0 means "every parsed line re-derives", not "B1–B11 met".
- `tools/round-48/record2.py` was not run (its `gate.py` import is worktree-sourced; not needed for these lines).
- No network fetch: S138 page, S147/S149 re-opening not repeated; quotes were checked against committed snapshots only.
- No data run, no freeze, no `--data-run`.
- Fixture commit hashes (`84eebc28…`, `6630ad34…`) exist only in scratch (removed); the diffs are kept under `receipts/`.

## Tools and installs

None installed or upgraded. Used: `git` (read-only on lane; mutations only in the scratch clone), `python3 -I -B`, `jq`, `sha256sum`. `pacman` not used.

## Artifacts

- `.ufo/waves/round-50/w1/C2ScorecardDraft/landing-blocks.md` — Blocks 1–3 and landing notes.
- `.ufo/waves/round-50/w1/C2ScorecardDraft/sources-drafts.md` — S150–S152 drafts with verification table.
- `.ufo/waves/round-50/w1/C2ScorecardDraft/tools/round-50/c2-grammar-check.py` — draft harness (exit 0 at base).
- `.ufo/waves/round-50/w1/C2ScorecardDraft/receipts/` — `receipts.sha256` covers: `grammar.out.json` (`db5a0623…`), `grammar-inert-test.txt` (`501c1514…`), `c2-at-base-battery.json` / `c2-at-base.stdout` (`44338e71…`), `c2-at-freeze.json` (`7aa900e1…`), `c2-fixture-r50section.json` (`700f2429…`), `c2-fixture2.json` (`82229fe3…`), `fixture-revs.txt` (`2e215d50…`), `fixture-placement-*.diff`, `r48-w1-results.json` (`8eec161e…`), round-48/49 receipt copies (`c1-final-33f65a91.json` `6320c5d2…`, `c2-final-33f65a91.json` `d1bb87d8…`, `c1-at-2e785632.json` `a6e9f605…`, `c2-at-2e785632.json` `8dcd1891…`, `c2-final.json` `544167f2…`, `c2-at-landing.json` `0cad6d5c…`).
