# Round 27 — non-author verifier spot-check

author: hyaku closure (non-author integrator, @m_opus)

Fresh closure subagent dispatched by the hyaku orchestrator, not by the lane, and not the round's
author. Runtime model as exposed to this session: `anthropic/claude-opus-5-5` (the `task` route,
no model parameter passed). It judged committed bytes only: base
`cd32264f7ee356a9c0f48bd8e3fcdac222db22a0`, head `29a76a637ad445f836b9b30382c0a6ee92a069a8`.
Two read-only reviewer seats that this closure dispatched (`R27CloseHygiene`, `R27CloseSweep`)
re-checked the hygiene bullets and the corrections sweep. Every other row below was re-run by
the closure itself. No lane gate or selftest was executed. Installs: none.

## Decision

- Status `ok`: a real report, landed by the lane identity, citing commits that exist.
- **Not admitted: `rejected-honest-stop`.** R27-C1 (depth) missed its frozen target at 15 of 16
  rows (exit 1), and the closure re-derived the same miss. The miss is not narrowed, swapped
  or gamed. R27-C2 (operability, capability acquisition) is met, and the closure re-ran the tool
  itself to confirm. No axis is harmed. A round is admitted only if every claim verifies, so this
  round is not admitted.

## Driver digest (copied from `.ufo/watchdog.log`)

```
2026-10-22T11:41:36-03:00 launch kaidoku round=27 pgid=1190817 driver=hyaku-inline attempt=1
2026-10-22T12:56:42-03:00 complete kaidoku round=27; hyaku-inline attempt=1
```

## Step-1 conformance

| check | command | observed |
|---|---|---|
| report landed by lane | `git -C /home/vgpnk/Projects/shokunin log --format='%an %H %cI' -- .ufo/reports/round-27/kaidoku.md` | `kaidoku-shokunin 57a140edf49dae6c62ba58b7c7910c453f57b847 2026-10-22T12:56:19-03:00`, after the tip commit 29a76a63 (12:54:46-03:00) |
| prompt committed | same, `-- .ufo/prompts/kaidoku-round-27.md` | `d77574cb…` by kaidoku-shokunin at 11:41:34-03:00. 350 lines, with the MISSION/AXES binding, `SHONEN`, the report path, write scope, L0, push, Frontier step and Claim sizing present |
| SHONEN heading | report lines 64-69 | `## SHONEN`, four lines, all `[~]` (asserted by the author) |
| cited commits exist and are ancestors of `main` | `git merge-base --is-ancestor <h> main` for a4f674b3, 9dca26df, c6d619a3, 97358f75, 4084d897, c4ec7a2e, 29a76a63 and the base cd32264f | all 8 `anc-ok` |
| pushed, no leftovers | `scripts/hyaku/jj-lane.sh state <lane>`; `git -C <lane> status --porcelain \| wc -l` | `local=remote=29a76a63… ahead=0 behind=0 tracked=0 untracked=0`; `0` |
| report sections | report | it has Work performed, Landed changes (each commit tied to a LOG line), Sources & frontier, Trend verdicts and SHONEN. LOG.md:2972 holds the round-27 entry |

Conformance defects (status-neutral):
- No gate-registry rows. `git grep -n -E 'c1-rename-identity|c2-xpin-check|xpin-attribute' 29a76a63 -- SKILL.md` prints nothing. The round-27 counters and the tool have no row at the lane's registry home. Rounds 22-24 kept one (SKILL.md:679, :731, :770).
- The C2 selftest is red at the tip. The report and SCORECARD say `c2-xpin-check.py --selftest` exits 1 from `97358f75` on, because case `correct-stub` was anchored to the pre-row state (`w2/RecountC2.md`). Under §Gate standard a red selftest is a conformance defect, so it is routed below. This closure did not run it.

## Freeze ledger entry (`corpus/claim-freezes.tsv`, row `round-27`, FLAGGED)

`round-27 FLAGGED INSTRUMENT_ABSENT,INSTRUMENT_REVISED,INSTRUMENT_UNPINNED`. The closure checked it:
- `claims.json` was touched only by the freeze commit: `git log cd32264f..29a76a63 -- .ufo/waves/round-27/claims.json` gives `a4f674b3` alone. Targets were not edited after the data, so they were not narrowed.
- Both counters are byte-identical at the freeze and the tip. sha256 `e0a079955c16…` (C1) and `d8de667ff82a…` (C2) at `a4f674b3` and at `29a76a63` equal `claims.json` `instruments`. Neither counter changed after the freeze: `git log cd32264f..29a76a63 -- tools/round-27/c1-rename-identity.py tools/round-27/c2-xpin-check.py` gives `a4f674b3` only.
- `INSTRUMENT_ABSENT` is correct and expected. `tools/round-27/xpin-attribute.mjs` is the R27-C2 product, absent at the freeze by design, and first appears at `97358f75`.
- `INSTRUMENT_UNPINNED` is correct. `tools/round-26/recompute-ids.py` is loaded by the C1 counter without a pin. Its receipt `after/recompute-pin.txt` says it is unchanged since the base (sha256 `89afa375…208b`), and the round range touches no `tools/round-26` path.
- The row's word "sha256-pinned" overreaches: only the two counters are pinned, and the lesson's wave-2 correction already says so.
- Data came after the freeze. All 48 `runs.tsv` rows have `utc_start` in 14:54:51Z–14:56:43Z, after the freeze commit at 14:51:23Z. Table and runs were first committed at `9dca26df` and never changed afterwards.

## Claims — re-derived by the closure

### R27-C1 depth: 16-row renamed-copy identity table plus entry. Target 16/16, `entry_ok` 1, exit 0. **Missed: 15/16.**

These are plain measurements over committed bytes at `29a76a63`: `git show`, Python `hashlib`/`json`, and the closure's own comparisons. The lane counter was not run.

| measurement | observed |
|---|---|
| `runs.tsv` data rows; per (carrier, verb) | 48; 3 each for all 16 pairs |
| exit codes; `pkg_version`/`pkg_json_sha256` | 48 × `0`; 48 × `6.5.0`/`a5003023…` |
| distinct `envelope_sha256` in `runs.tsv` | **47 of 48**; the one shared value is `f601872bf55d…` = RunTxD tinyxxd `inspect-binary-layout` base (14:55:49Z) and repeat (14:55:50Z) |
| those two envelope files | byte-identical (`tinyxxd-inspect-binary-layout-base.json` == `-repeat.json`, 51287 bytes), `meta.duration` `132ms` in both, `meta.command` `inspect-binary-layout` |
| every `runs.tsv` sha256 matches a committed envelope file | 48/48 (47 distinct files) |
| own path present, other path absent, `meta.command` = verb (all 48) | 0 failures |
| table verdicts re-derived from `runs.tsv` ids (`unstable` if base≠repeat, `content-keyed` if renamed=base, else `rename-sensitive`) | 16/16 match `table.tsv`; 10 content-keyed, 6 rename-sensitive, 0 unstable |
| the unused extra run (envelope `81a069ab…`, 15:09:45Z) | it appears only in seat reports `w1/RunTxD.md` and `w2/CriticC1HonestStop.md` (`git grep -l 81a069abb9c7 29a76a63`), not in `runs.tsv`, `table.tsv` or `envelopes/` |
| entry | `corpus/knowledge/2026-10-22-r27-renamed-copy-evidence-id-identity.md` exists. Its first lines are `source:`/`verified-at:`/`recheck:`, it cites S082 and S083 (both new rows), and it states the 15/16 miss (seat `R27CloseSweep`) |
| committed receipts | `before/c1-at-cd32264f.txt` `rows_complete=0/16 entry_ok=0` exit 1. `after/c1-at-97358f75.txt` reports 15 rows COMPLETE and `INCOMPLETE tinyxxd inspect-binary-layout: base: envelope_sha256 shared with another run; repeat: …`, `rows_complete=15/16 entry_ok=1` exit 1. Selftest receipt `before/c1-selftest.txt` has 22 cases and 0 failures |

Ruling. The plain measurements reproduce the committed after-state exactly. Every verdict
re-derives, and exactly one pair breaks the frozen distinct-envelope rule. That rule is frozen in
the counter, which is pinned and unchanged, so 15/16 is the honest result and the target is
missed. The L1 kept the original repeat envelope. Replacing it with the later extra run would
have passed the counter, but it would also have changed the measured data after the counter had
ruled. Keeping the original is correct. The cause, two genuine runs tying on `meta.duration`, is
plausible from the bytes: the only volatile field is equal. It is mined as M27-2 and QUALITY row
40. The target was not narrowed (`claims.json` was committed once) and not gamed (no substitution,
no counter edit). Verdict: **claim not verified (honest stop)**. The depth axis is `unchanged`
(10 → 10 on the card), not harmed. The knowledge the table carries is real, but the claim as
frozen is not met, and this closure does not count it.

### R27-C2 operability, capability acquisition: `xpin-attribute.mjs`. Target 24/24, 3/3, capability row 1, source row 1, exit 0. **Met.**

The closure re-ran the tool itself. The tool is the product, not a gate, and it is read-only over
saved envelopes. It ran from a `git archive` of `29a76a63` under
`/fast/scratch/hyaku/close-kaidoku-r27/tree`, with node v24.21.0, `--pkg65
/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents` (`package.json` 6.5.0, sha256
`a5003023…50a6c`) and `--pkg67 /home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents`
(6.7.0, sha256 `3f6c47fb…b570`).

| measurement | observed |
|---|---|
| tool on the 24 round-26 envelopes listed in `corpus/evidence/round-27/c2/r26-attribution.tsv` | exit 0. Output **byte-identical** to the committed receipt (`diff` empty). 21 `6.5.0`, 3 `both`. Stored id = 6.5.0-rule id on 24/24. On all 3 `both` rows the 6.5.0 and 6.7.0 ids are equal |
| tool on the 48 round-27 C1 envelopes (`r27-c1-attribution.tsv`) | output byte-identical to the receipt; 42 `6.5.0`, 6 `both` |
| the closure's own red envelopes, built from round-26 `analyze-base.json` | `.data.evidence_id` set to the 6.7.0-rule id gives `6.7.0`. An all-zero id gives `none`. Tampering `.data.confidence` gives `none`, and both recomputed ids change. Every result is correct |
| capability row | `SCORECARD.md` `## Capabilities` row "cross-pin evidence-ID attribution for saved REA envelopes" (first-working round 27), added by `97358f75` |
| source row | S081 is new since the base: opened 2026-10-22, status `mined`, and it names root `a1722018f28f9df2`. It is listed in round-27 `## Gate` |
| committed receipts | `before/c2-at-cd32264f.txt` exit 1, all counts 0. `after/c2-at-97358f75.txt` `r26_rows_ok=24/24 red_ok=3/3 capability_row=1 source_row=1 (S081)` exit 0 |

Ruling: **verified (met)**. The capability was observed running by a non-author. Operability:
`improved`. Width, already disclosed by the lane: a record whose `relationship_coverage` key is
set or absent always prints `both`, and no committed receipt holds a real `6.7.0` label.

### Other axes and harm

- `git diff cd32264f 29a76a63 -- SCORECARD.md` gives `44 0` (numstat). It is append-only: the hunks are the capability row and the appended round-27 sections. Owned axes rows (coverage, depth, calibration) are unchanged.
- SKILL.md, PROVINCE.md, corpus/README.md, QUALITY.md and corpus/knowledge only gained lines. The one in-place change in SOURCES.md is the S079 `used-by` cell, which is permitted and logged in the lesson (seat `R27CloseSweep`).
- Hygiene: there are 11 appended correction bullets, plus the wave-2 corrections at SCORECARD.md:3125 and :3130. Seat `R27CloseHygiene` re-checked every cited line at `a4f674b3`. Bullets 4, 5 and 6 hold as written. Bullets 1, 2, 3, 7, 8, 9, 10 and 11 were wrong as first written, and each is covered by an appended correction. **Wrong and uncorrected: 0.** Minor defects in the corrections themselves: :3130 calls lines 16-17 "AXES rule lines", but they are SCORECARD's own baseline-citation rule. :3125 says "the current planned field is the round-27 one", which is ambiguous until :3128/:3130 resolve it.
- Knowledge sweep, a routed defect and not a harm. The round-26 entry `corpus/knowledge/2026-10-22-r26-native-reader-evidence-id-identity.md` (table rows :32-33, `## Use`) and QUALITY row 37 still say `analyze`/`inspect` are "content-keyed" with no round-27 pointer. Both stay true within their stated scope: the r26 Limits say "directory-insensitivity at an identical file name", and round 27 found that a name-only or directory-only copy keeps the id. They are therefore not false. They are incomplete beside round 27's extension finding. SKILL.md (:946) and the r17 entry (:212-215) did get pointers.

| axis | verdict | basis |
|---|---|---|
| depth | unchanged | R27-C1 missed 15/16 (re-derived). Score 10 → 10. No harm |
| operability | improved | R27-C2 met. Tool re-run by the closure reproduces both receipts byte for byte |
| coverage | unchanged | not claimed. Recipe-A count 110/110 is reported; the row keeps its round-26 measurement |
| calibration | unchanged | not claimed. 11 hygiene bullets plus corrections are append-only, with 0 left wrong |
| freshness | unchanged | not claimed. Two round-26 ids re-run equal (below) |
| adjacency | unchanged | sibling tameshi source read in `w1/SiblingOverlap.md`, not absorbed and not opened as a row |

## Discernment spot-check

Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku`
exits 0 with `kaidoku ok` and six W04 warnings (S033, S047, S054, S062, S069, S083). S083 shares
the 6.5.0 tarball URL with S079. Rows 80 → 83 (`grep -cE '^\| S[0-9]{3,} \|'` at base and head).

| item | gate decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S081 (new row; 6.7.0 projection code) | admit | `/home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents/dist/domain/evidence.js` sha256 `a3fb9f028e04e3a1…` (= Gate), `:178` `relationship_coverage: evidence.relationship_coverage,` and `:183` `const computeEvidenceId = (evidence) => \`ev_${digestCanonicalValue(semanticProjection(evidence), "Evidence")}\`;`; `canonicalDigest.js` `f46d6bd4…` `:8` `export const digestCanonicalValue = (value, context = "Comparison") => {`; `package.json:4` `"version": "6.7.0",` (`3f6c47fb…`) | agree | Every quote and hash reproduces byte for byte. It is primary installed code, tier A for the scope it names. It is the round-26 spot-check's routed defect 1, now learned |
| S083 (new row after wave 2; 6.5.0 snapshot naming) | admit | `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/cli-runtime/binary-BVOr2mgE.js` sha256 `64c07dae6fe8b79a…` (= Gate), `:5318` `return /^\.[A-Za-z0-9]{1,12}$/u.test(extension) ? extension : ".bin";` (≤25 words, contiguous), `:293` `targetPath = await realpath(input.targetPath);`; `bridge/ghidra/ReaGhidraBridge.java` `db16aed4…` `:1975` `result.add(currentProgram.getName());`; `GhidraTargetSnapshot.js` `a27e4107…` `:14`, `:78` | agree | All quotes reproduce at their stated lines. A new row is the right route: S079's source and anchor cells cannot change in place |
| S082 (new row; tinyxxd package record) | admit | `/var/lib/pacman/local/tinyxxd-1.3.17-1/desc` sha256 `a2d70e537e159315…` (= Gate): `%PACKAGER%` `Alexander F. Rødseth <xyproto@archlinux.org>`, `%BUILDDATE%` `1790704346`, `%URL%` `https://github.com/xyproto/tinyxxd`. The mtree entry for `./usr/bin/tinyxxd` gives `size=38928 sha256digest=7b1e5d0c…3ae65`, which equals `sha256sum /usr/bin/tinyxxd` | agree | The local records reproduce and tie the carrier bytes to the package. The lane already corrected the Arch HTML page quotes, which are rendered composites, and the CSP-nonce page hash. The row does not depend on them |
| npm version document `https://registry.npmjs.org/rea-agents/6.7.0` | reject (excluded: S037's family) | fetched 2026-10-22: `version` 6.7.0, `dist.shasum` `11f23ba377303a5c28b3162180cf2bf3f3643708` (= the S081 Gate tarball sha1), `dist.attestations.url` present, 0 `relationship*` paths (`jq`) | agree | It is the exact source URL of S037, whose scope is publish identity, not runtime behaviour. It holds no projection code, so a second row would duplicate S037 |

## Trend verdicts

- **expansion: improved.** Knowledge files went from 109 to 110 (`git ls-tree --name-only <rev> corpus/knowledge/ | grep -c '\.md$'`). The new entry is on ground the map did not hold: extension-dependent `analyze`/`inspect` ids, a second carrier, and the S083 mechanism. It has coverage-map rows at `corpus/README.md:76` and `:168`, and its `source:` cites the mined rows S082 and S083. All 16 of its table verdicts re-derive from committed envelopes. Only the duplicate-bytes gate fails. One capability row was admitted and observed running by this closure.
- **quality: improved.** The round-26 seven-verb rule is narrowed by a code mechanism (S083) and by live separation of name and extension (`w2/FalsifyExtensionOnly.md`, `FalsifySuffixMapping.md`), with pointers in SKILL.md:946 and the r17 entry. Two round-26 ids re-verify: the two `ev_` ids in `w1/FreshnessR26.md` are both in `corpus/evidence/round-26/c1/table.tsv` (`comm -12` gives 2 of 2). Of the 11 hygiene corrections, 0 are left wrong. No entry was found false and left unmarked. The r26 entry and QUALITY row 37 still need pointers, routed as defect 1.
- **discernment: improved.** This closure differs from the lane's self-assessment (`unchanged`), and the outside check rules. The spot-check agrees with the gate on 3 admits (S081, S082, S083) and 1 reject (the 6.7.0 version document). The round-26 spot-check disagreement (S037 family) became a new code row, S081. The lane also mined M27-1 and M27-2 with failures on real bytes, and QUALITY row 40 cites M27-2. Offsets on record: the S082 HTML quotes and 8 of 11 hygiene bullets needed corrections, but the lane's own wave 2 caught all of them before filing. QUALITY rows 38 and 39 cite round-26 lessons and spot-check lines rather than M27-1. They have lessons behind them, so they are not criteria without a lesson.

## SHONEN

All four boxes are `[~]`, asserted by the author. Boxes 1 (SKILL.md tables, patterns and checklists with cited sources) and 2 (an end-to-end task logged in LOG.md, here 48 REA calls in `runs.tsv` plus LOG.md:2972) look checkable by a non-author from committed bytes. This is a note for the operator, who owns promotion. Nothing here writes `[x]`.

## Dead seats

Wave 2 had 6 of 34 seats dead at spawn (17.6%). They were `MutQualityRow38`, `MutQualityRow39`, `MutQualityRow40`, `MutXpinTool`, `MutLessonM27` and `MutC1DupGate`, each with "Error: No model selected. Use /login, set an API key environment variable, or create /home/vgpnk/.omp/agent/agent.db". The lane did not replace or reroute them. The route is operator-owned. As a result, QUALITY rows 38-40, the M27 fixes and the C2 tool had no mutation test this round. This is below the session's 20% trip, so it is recorded and not tripped.

## Routed defects (the lane owns these; fix next round)

1. **Corrections sweep.** Append a round-27 pointer to `corpus/knowledge/2026-10-22-r26-native-reader-evidence-id-identity.md` (table rows `analyze`/`inspect`, `## Use`). Add a QUALITY row superseding row 37. Both should say that the `analyze`/`inspect` id holds only when both paths map to the same snapshot suffix (S083, round-27 entry).
2. **Red C2 selftest.** `tools/round-27/c2-xpin-check.py --selftest` exits 1 from `97358f75` on (`correct-stub`). Re-anchor the fixture in a new commit and commit the green receipt. Do not count it as a claim.
3. **Registry.** Add SKILL.md registry rows for `tools/round-27/c1-rename-identity.py` and `c2-xpin-check.py` (gate or probe, verdict map, selftest spelling, pinned values), following the round-22 to round-24 registry sections.
4. **Pinning.** The next freeze pins every file a counter loads, which `recompute-ids.py` was not (`INSTRUMENT_UNPINNED`). Freeze-row wording names exactly what was pinned.
5. **Duplicate-bytes gate (M27-2, QUALITY row 40).** A repaired gate is a new claim with its own freeze and a green case for a genuine byte tie. Round 27's C1 stays a miss and is never re-scored.
6. **Gate quotes from rendered HTML.** Quote contiguous served bytes, or label the quote a composite at write time (the S082 lesson).
7. **SCORECARD :3130/:3125.** Append a clarification: lines 16-17 are SCORECARD's own rule, and the current planned field is the one at :3128.
8. **Mutation tests.** When a mutation-tester route is available, give QUALITY rows 38-40 and `xpin-attribute.mjs` the mutation tests the dead seats did not run.

## Commands re-run by this closure (summary)

`git log/show/diff/merge-base/ls-tree/grep` over the lane at the cited revisions; Python
`hashlib`/`json` over `git show` bytes for C1; `node tools/round-27/xpin-attribute.mjs` from a
`git archive` of the tip for C2; `sha256sum`/`sed -n` on the installed rea-agents 6.5.0/6.7.0
files and the tinyxxd pacman records; `curl https://registry.npmjs.org/rea-agents/6.7.0`;
`scripts/sources-census.sh validate`; `scripts/hyaku/jj-lane.sh state`. Scratch:
`/fast/scratch/hyaku/close-kaidoku-r27/`.
