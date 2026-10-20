# ConnProvenanceRoutes — R16-PROVENANCE / R16-INVOCATION vs QUALITY #18

Author-side advisory seat (`KaidokuR17.ConnProvenanceRoutes-3`), not outside review. Read-only.
Labels: **(obs.)** = read from committed bytes at baseline `b563c799d97774aae4351276fe43cb897311e349`
or from the named file; **(inf.)** = my inference. No REA command, no Ghidra, no carrier execution,
no gate run, no tool install/update. Only this report was written.

Anchors: `RD` = `corpus/lessons/round-16-verifier-spotcheck.md`; `C` = `.ufo/waves/round-17/contract.md`;
`Q` = `corpus/QUALITY.md`; `R15` = `corpus/lessons/round-15-verifier-spotcheck.md`;
`R16` = `corpus/lessons/round-16.md`.

## 1. Answer

**R16-INVOCATION (`RD:184`) is a class recurrence of r15 route 1 (`R15:185`), captured by QUALITY #18
clause 2 (`Q:28`) in prose but not in extension.** #18 says "**future** recheck guidance either matches
the exercised isolation flags and paths or explicitly names an unexercised variant" (`Q:28`). The
citation-drift row (`SKILL.md:448`) pre-dates the criterion; the r15 fix closed the two *named* instances
(`R16:54`) and QUALITY #18's why-cell cites those same four routes (`Q:28`). The r16 verifier states the
boundary itself: "This pre-existing generalization gap is **not one of the four** specific r15 routes,
which are closed" (`RD:184`) — true of the four instances, false of the class. The criterion's provenance
is the instance list, so it could not see a sibling row. Recurrence was structural, not a diligence lapse.

**R16-PROVENANCE (`RD:183`) is *not* captured by #18.** The nearest clause is "Structural/no-harm
tallies retain the producer and immutable inputs, not only unexplained booleans" (`Q:28`). The r16
receipt satisfies that letter: 22 command records with argv/cwd/exit (`verification.json:5-395`), a
single 20-entry map (`producer_and_fixture_sha256`, `verification.json:397-418`), plus the unexplained predicate
`"pins_unchanged_during_run": true` (`verification.json:419`). #18 specifies the provenance of the
*inputs*; the boolean's truth value is a *relation between two instants*, which no static input can
discharge. The gap is a type gap, not a population gap.

**Root common to both: instance-closure where the defect class is population-quantified.** The r15
routes split cleanly: routes 1 and 3 carry classes (any registry row; any structural/no-harm boolean
without its measurement), and both reappear in r16 — route 1 exactly (the surviving sibling row 448),
route 3 in shape (an unexplained boolean, though what is missing has shifted from a producing command to
a predicate measurement). Routes 2 and 4 are singletons (one registry row; one SHONEN box) and do not
recur (`RD:183-184`, `R15:186,188`). The predictor is whether the fix closed over the population or only
over the named artifact — not difficulty.

Timing (inf. from recorded timestamps): #18 landed in `27b8fc1` at 08:35:55Z (`git show` of that commit's
`corpus/QUALITY.md` has row 18; commit author time 2026-10-20T05:35:55-03:00); the receipt records
execution at 08:36:33Z (`verification.json:4`) — 38 s later. The boolean was written after the criterion
existed, so this is not a pre-criterion artifact.

## 2. Evidence — the temporal population is narrower than the claim

`C1(a)` promises "**Every** lane statement asserting that round-16 pins stayed unchanged during
execution gets a named append-only correction" (`claims.json:12`). The planned counter's site set is a
fixed five-file list plus four regex phrases (`C:91-92`). At `b563c79`:

| site | text | in the counter? |
|---|---|---|
| `corpus/lessons/round-16.md:154` | "All producer/fixture pins remained unchanged during execution." | yes — list + regex |
| `.ufo/waves/round-16/verification.json:419` | `"pins_unchanged_during_run": true,` | yes — list + regex |
| `corpus/knowledge/2026-10-20-r16-go-selection-preview.md:95-96` | "Producer and fixture pins were unchanged during the run." | **no** — regex hits, file not in `C:91` |
| `LOG.md:2012` | "Producer/fixture hashes remain unchanged across execution." | **no** — file in `C:91`, phrase not in `C:92` |
| `/home/vgpnk/Projects/shokunin/.ufo/reports/round-16/kaidoku.md:60` | "Producer/input hashes stayed unchanged during execution." | **no** — outside `--root LANE` |
| `SCORECARD.md` | no such assertion; r16 block points at the receipt (`SCORECARD.md:2299`) | n/a |

Counts (obs.): declared-population sites = **2**; actual r16 assertion sites in lane + fleet report =
**5**. The defect's own enumeration ("report, lesson, LOG and scorecard", `RD:183`) is itself recalled,
not searched: scorecard has no such sentence, and the knowledge entry — which does — is unnamed. A
search over the same bytes would have produced the true list, so the same instrument applied to the
defect text would have corrected the defect.

Two defects in the `corrected` test (`C:94-95`):

1. **Path-coarse, not site-coarse.** A site is `corrected` if *some* line contains `R16-PROVENANCE` and
   the site's repo-relative path. One omnibus line naming `LOG.md` marks every LOG site corrected; there
   is no line identity, no required replacement sentence, no adjacency. This is the r16 lesson's own
   rejected class: "vacuous / marker sufficiency … presence evidence only" (`R16:58`). If
   `unqualified: 0` is presented as route resolution, the round repeats that error at the verifier layer.
2. **Self-exempt.** `corpus/lessons/round-17.md` is a correction *source* but not a site *file*
   (`C:91` vs `C:94`). The round's own lesson — the most likely place to restate the claim — cannot be
   counted. A sentence such as "pre/post maps show pins were unchanged during execution" would pass
   unseen at the post revision.

Logical limit the correction must preserve: two endpoint snapshots prove *same bytes at two instants*,
never "unchanged throughout"; a pre/post equality can be produced by a change-then-revert. `C:20` already
requires `pins.py --help` to say this; the prose rule must carry the same limit.

The implementation confirms the design, and does not accidentally compensate for it:
`.ufo/waves/round-17/tools/temporal-sweep.py:19-21` calls itself "a wording census, not a semantic
check"; `:83-93` reduces corrections to a set of file paths; `:105,109,118,133` applies `corrected` by
path membership; and selftest Case 2 (`:225`) asserts that "a named correction for one file corrects all
of its sites". So the path-coarseness is a *chosen criterion behavior*, not an implementation slip. The
selftest has no paraphrase case ("unchanged across"), no `corpus/knowledge/**` case, and no out-of-root
case.

## 3. Evidence — the invocation population is M=2 under the implementation

Seven registry rows (`SKILL.md:447-450,487,506,507`). The contract text (`C:81-88`) states exact-token
matching with `<...>` wildcards and interpreter stripping only; the shipped `invocation-audit.py` adds two
normalizations the contract does not mention — absolute paths under `--root` are relpath-normalized
(`:179-195,280-283,302-308`) and `[...]`-bracketed tokens are optional (`:87-146`). Classifications below are
therefore *under the implementation*, with the contract-text deltas noted:

| row | class under the implementation | basis |
|---|---|---|
| 447 `interactive-r1-recovery` | `exercised_match` | exact argv in `.ufo/rounds/interactive-r1/gate-results.json` |
| 448 `citation-drift` | `unlabelled_variant` | see below |
| 449 `custody-pair` | `unlabelled_variant` | no matching array-argv receipt; the optional-bracket form is handled, so the bracket is not the blocker |
| 450 `quote-fidelity` | `exercised_match` | relative row paths normalize to the round-14 absolute argv (`invocation-audit.py:179-195`); the contract text alone would call it unlabelled |
| 487 `go-snapshot-inventory` | `exercised_match` | round-15 `verification.json`, `--select 1.24.7 1.25.7 1.26.8` |
| 506 `go-selection-preview` | `exercised_match` | round-16 `verification.json`, `--request 1.24.7 --goos linux --goarch amd64` |
| 507 `round16-structural-controls` | `exercised_match` | `<BEFORE> <AFTER>` wildcards match the two revision hashes |

Row 448 diverges on **three** axes, not the two named in `RD:184`:
- no `-I` (`SKILL.md:448` vs round-16 receipt);
- relative script/table/expected paths plus `--root .` (vs absolute);
- **no `--strict`**. Every retained citation-drift argv is `--strict`: round-14 and round-15 without
  `-I`, only round-16 with `-I` (census over all `argv`/`orig_argv` at `b563c79`; two distinct forms,
  both `--strict`, both absolute). So the row's advertised *default probe mode* — "0 reported, drift is
  reported, never failed" (`SKILL.md:448`) — has **never been exercised in any retained receipt**. The
  defect notices isolation and paths but not the mode. A repair that pastes the strict argv into the
  runnable slot while keeping the first semantic clause creates an internal command/semantics
  contradiction: `--strict` maps 0 clean / 1 failed / 2 could-not-evaluate, not "0 reported, never failed".

Row 450 shows the implementation **outrunning its contract**, not a false positive. The row is
`python3 -I .ufo/waves/round-14/tools/quote-fidelity.py --manifest .ufo/waves/round-14/fixtures/manifest-corrected.json`
(`SKILL.md:450`); round-14 `verification.json` retains the same script, same `-I`, same
`--manifest …/manifest-corrected.json` with absolute paths. `_relpath` makes the two spellings equal
(`invocation-audit.py:179-195,280-283,302-308`), so the row is `exercised_match`. The normalization assumes
the row's relative paths are read from the lane root — the lane's documented convention, but not stated in
`C:81-88`. A reader re-deriving the
count from `C:81-88` alone would get `unlabelled_variant` for it — M=3, not M=2. The counter's number is
therefore **not reproducible from its written rule**: L1 should
state the path normalization in `C:81-88`, or have the tool print the normalization it applied. This is a
calibration defect in the rule text, not in the audit.

Receipt discovery is a naming convention, not an evidence relation (`C:83`). At `b563c79`, 34
`.ufo/**/*.json` files carry `argv`/`orig_argv`, 5 match the four declared names, 29 do not (obs., Git
object census). This is **latent**, not currently biting: the included receipts cover six of the seven
rows (five via a `verification.json`, row 447 via `gate-results.json`), so no row's evidence is lost
today. But row 507's own output `controls.json` and
the r16 `documentation-red.json` are excluded by name. A row whose only receipt is named otherwise
would be classified unexercised, with only the global `receipt_glob_pathform_excluded` count
(`invocation-audit.py:255-260,343`) as a signal; the exclusion is not attributed to a row. Row 449 shows
the second half: the tool *was* run
(`.ufo/waves/arc3-loop1-round3/claims/c2/EX-25/probe-after-candidate.json`), but the argv is stored as a
**string**, against a `/var/tmp` copy, with a `--paths` flag — invisible twice over
(`iter_exercised_argvs`, `:227-242`, accepts only a list of strings, so a string argv cannot contribute),
and there is no class for "tool exercised, this argv not retained".

## 4. Fix shape that would have caught it

One move, two instantiations: **derive the population by search at the pinned revision, and classify by
evidence relation rather than by vocabulary.** A criterion can only be population-closing if its
verification enumerates the population, not the remembered instances.

1. **Population.** `temporal-sweep.py`: site set = every line at `REV` whose content matches a *family* of
   temporal patterns (`unchanged during|remain(s|ed) unchanged across|stable throughout|pins_unchanged…`),
   over lane `*.md`/`*.json` **including `corpus/knowledge/**`**, plus explicit `--external` paths for the
   fleet report. Out-of-root sites are reported as `out_of_lane_unverifiable`; they are never silently
   dropped. Lines that quote the phrase in order to route it (`RD:183`) are excluded by digest-keyed
   exclusion, not by file omission.
2. **Relation.** A site is `corrected` only with a per-site record `{file, line, line_sha256,
   replacement}`, one record per site, the replacement text verified verbatim in an allowed correction
   file, and the replacement must carry the semantic qualifier ("same bytes at two instants" /
   "temporal stability not evidenced"). A token-plus-path line does not count. This removes path-coarse
   inflation and makes each correction auditable; it still proves only "a named replacement exists", so
   the semantic truth remains an outside-review act — state that limit in the output, not in a score.
3. **Invocation.** Keep two explicit classes: `exercised_match` (token equality after interpreter
   stripping) and `exercised_path_normalized` (equality only after relpath-normalizing absolute tokens
   under `--root`); record which normalization produced the match and in which receipt. Keep
   `exercised_variant` for "tool exercised, this argv not retained" (and accept string-form argv as
   evidence of exercise, not of match). M counts `unlabelled` only; publish the whole histogram. Receipt
   discovery scans every `.ufo/**/*.json` at `REV` for `argv`/`orig_argv`, with the four names as a fast
   path, not a filter.
4. **Mode binding.** Each row's first semantic clause names an exit map; require the argv mode
   (`--strict` vs default) to agree with it. Row 448 is the red fixture.
5. **Self-application.** Run the sweep at the post revision with `corpus/lessons/round-17.md` in the site
   population and correction lines excluded; a round-17 sentence re-asserting the claim must be counted
   and must fail.

Selftest red cases, sibling-shaped rather than same-instance:
- temporal: paraphrase "hashes remain unchanged across execution" in `corpus/knowledge/**`; an omnibus
  correction line naming only the file while two sites exist (must leave one unqualified); an out-of-root
  report path; a pre/post pair with a mutated file (`pins.compare` must return `equal:false`).
- invocation: a relative-path row against an absolute-path receipt under `--root` →
  `exercised_path_normalized`, not plain `exercised_match`; a pair that matches only after prefix-dropping
  against a *different* root → no match; row 448 shape (no `-I`, no `--strict`) → `unlabelled`; row 449
  shape (string argv, different flags) → `exercised_variant`, not match.

**What it would have caught in r16:** an audit of all seven rows at S/A would have classified 448
unlabelled before the four routes were declared closed (`R16:54`, `RD:184`), and the temporal search would
have produced 5 sites — not the 4 recalled artifact types — with a correction test that a marker line
cannot satisfy. At the time of writing, `temporal-sweep.py`, `pins.py`, `retain.py` and other r17 tools
exist under `.ufo/waves/round-17/tools/` (created by sibling seats, not by me), including
`invocation-audit.py`. I ran none of them: the temporal counts above are my own Git-object scan, and the
row classes are my reading of the shipped matcher against retained argv, not tool output.

**Risks of this move**

1. *Quote false positives.* Broadening the site population to search catches the defect line itself
   (`RD:183`, which quotes "unchanged during") and any correction line quoting the field name. Mitigation:
   digest-keyed exclusion entries printed in the output, so an exclusion is visible and reviewable; never
   exclude a whole file by omission.
2. *False matches from path resolution.* Relpath-normalizing absolute tokens under `--root` could equate
   two different files if the root assumption is wrong. Mitigation: require full token equality after
   normalization, print the normalized pair for each match, and never suffix-match; a pair that matches
   only after prefix-dropping against a different root is not a match.
3. *The correction record proves existence, not truth.* A per-site record proves a named replacement
   exists; it does not prove the replacement is accurate. Keep that limit in the tool's output (as
   `pins.py` already does for endpoint equality); do not let `unqualified:0` become a semantic verdict.
4. *A rising M reads as regression.* Under the shipped matcher M is 2 (448, 449), not 1. Row 449 is a
   genuine pre-existing gap (the tool was run in arc3 with a string argv and different flags), so M→0
   requires labelling or exercising it — legitimate population closure, but scope beyond the routed
   defect and it must be declared. The histogram must also keep `exercised_path_normalized` (a match
   resting on the root-relative assumption) and `exercised_variant` (a different retained argv) separate
   from `unlabelled`, and the report must not claim improvement from a lower number.
5. *Out-of-lane site.* The fleet report cannot be corrected under the lane write bound. Record it as
   `out_of_lane_unverifiable` and let the integrator own the fix, or state C1(a) lane-only; do not claim
   coverage the lane cannot execute.

## 5. Affected axes

| axis | effect | why |
|---|---|---|
| calibration | **improves** | The current counters can certify a false zero (2 of 5 temporal sites; the invocation count is 2, one the routed row 448 and one the unnamed pre-existing row 449). A relation test cannot be satisfied by a marker line; the contract text should state the path normalization the implementation already applies. |
| depth | **improves** | Makes explicit two facts the defect omits: the `--strict` mode divergence (no retained receipt ever ran the advertised probe form) and the site-population leaks; adds the endpoint-equality limit. |
| operability | neutral | Stdlib only, same CLI shape; adds one correction-record file and fixtures. |
| coverage / freshness / adjacency | neutral | No new domain ground, no provider run, no sibling or host ownership. |

No numeric proxy moves; this is a criterion/instrument correction, not a capability claim.

## 6. Contradictions (stated, not smoothed)

1. `C1(a)` says "every lane statement" (`claims.json:12`) but the fleet report site lives under
   `/home/vgpnk/Projects/shokunin`, outside `--root LANE` and outside the lane write bound. Either the
   integrator appends that correction in the fleet repo, or C1(a) must be restated lane-only with the
   report recorded `out_of_lane_unverifiable`. It cannot be claimed silently in either case.
2. `C1(b)`'s `M→0` covers two rows under the implementation (448, 449), not the one routed row. 449 is a
   genuine pre-existing gap — the tool was exercised in arc3 with a string argv and different flags — so
   closing it requires a label or an exercise. That is legitimate population closure, but it is scope
   beyond the routed defect and must be declared.
3. The `corrected` test is a marker test (`C:94-95`) — the class `R16:58` rejects. Presenting
   `unqualified:0` as route resolution would repeat the error one layer up.
4. `RD:183`'s artifact enumeration does not match committed bytes (scorecard absent; knowledge present but
   unnamed). The enumeration was recalled, not searched — the same mechanism as the defect it reports.
5. The r16 probe-mode claim: the row advertises the non-strict form, but no retained receipt exercises it
   (`--strict` in every retained form). This is a stronger pre-existing gap than `RD:184` states, and it
   changes what "align with an actual receipt" must mean.

## 7. Verification performed

Read-only, on committed objects at `b563c799d97774aae4351276fe43cb897311e349` (HEAD; `git status`
clean apart from the untracked `.ufo/waves/round-17/`):

- Git-object census of `.ufo/**/*.json` at `REV`: 34 argv-bearing files, 5 matching the four declared
  receipt names, 29 not.
- Pinned-revision regex scan of the five declared site files: 2 matches
  (`corpus/lessons/round-16.md:154`, `.ufo/waves/round-16/verification.json:419`); out-of-list matches at
  `corpus/knowledge/2026-10-20-r16-go-selection-preview.md:95` and `RD:183`; paraphrase at `LOG.md:2012`
  not matched by `C:92`.
- Registry-row extraction from `SKILL.md` (7 rows) and comparison against every retained argv array and
  string at `REV`; citation-drift forms deduplicated to two (both `--strict`, one without `-I`).
- Read-only inspection of the sibling-authored `.ufo/waves/round-17/tools/temporal-sweep.py` (352 lines):
  its site list and phrase regex match `C:91-92`; its correction logic is path-level
  (`:83-95,105,109,118,133`) and its selftest Case 2 (`:225`) asserts that one named line corrects all
  sites in a file. Not executed.
- Read-only inspection of the sibling-authored `.ufo/waves/round-17/tools/invocation-audit.py` (483
  lines): the matcher relpath-normalizes absolute tokens under `--root` (`:179-195,280-283,302-308`) and
  treats `[...]`-bracketed tokens as optional (`:87-146`), neither of which `C:81-88` states; receipt
  discovery is by basename (`:227-242,255-260`), and pathform exclusions are counted but not ingested
  (`:343`). Under that matcher row 450 is `exercised_match` and M=2. Not executed.
- `verification.json` field check: 22 command records, all carrying `argv`, `cwd` and `exit`; one
  20-entry `producer_and_fixture_sha256` map; no pre/post maps and no snapshot timestamps.
- `git show 27b8fc1:corpus/QUALITY.md` confirms row 18 is present at S; `git show 2fc1d6f` author time
  2026-10-20T05:40:52-03:00; receipt `executed_at_utc` 2026-10-20T08:36:33Z.
- Fleet report line read from `/home/vgpnk/Projects/shokunin/.ufo/reports/round-16/kaidoku.md:60`
  (commit `2d0274b`, the only commit touching that file).

Not run: REA commands, Ghidra/`analyzeHeadless`, carrier execution, any gate/selftest, any install.
Tool installs/updates: **none**.
