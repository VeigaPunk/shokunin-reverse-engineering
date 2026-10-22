# SupersedeConsistency: older evidence-id identity statements against the round-26 6.5.0 table

Seat KaidokuR26.SupersedeConsistency (critic, leaf, read-only). Bytes judged at lane commit
`fe3eb4edf410244eff46151a148c8f754be1ce80` (`git rev-parse HEAD`, 13:02:31Z, exit 0). No REA call,
no install, no lane write except this file. All commands are read-only `git show` / `git grep`
piped to `jq`, `awk`, `grep`; all exited 0 except the pointer census (exit 1, from a final grep with
no match, which is the finding). Times are 2026-10-22 UTC.

## Verdict

Fails, with a counterexample. None of the six assigned statements contradicts the table, but four
of them are unqualified (no pin, no pointer to the table). The strongest local counterexample sits
one step outside the assigned list. `SKILL.md:86-93` is a live craft rule, and it uses the very id
the table now labels path-sensitive as its example of content addressing. Neither that rule nor its
source entry points at the table. Wave-1 seat IdentityClaimsMap missed it: its F5 says
`inspect-binary-layout` has "no identity statement anywhere in the lane", which is wrong (see C1).

## Contradicted, no pointer to the table (observation)

C1. `SKILL.md:86-93`, rule "**Evidence ids are content-addressed per verb family**". It cites
"an id held across a day and re-derives byte-exact `corpus/knowledge/2026-10-14-r12-01-queue-b-ready.md:11`".
That line reads "`inspect-binary-layout` … `ev_294a449c…60a71bd` reproduced byte-exact … (content-addressed
family extends to pwntools-elf)". `checks2.txt` shows the full id at r12-01:21 compared with the
table's `inspect-binary-layout` base id: `EQUAL`. The table labels that verb `path-sensitive`, with copy id
`ev_52da4b3d…`. The rule's taxonomy (lines 94-106) has two kinds of id: content-addressed ids,
checked byte-exact, and per-run ids, normalized. A path-sensitive native reader fits neither, so
`SKILL.md:105` ("verify byte-exact (content-addressed)") predicts the wrong result across paths.
Blame: `0f377e84`, 2026-10-14. Round 26 did not change these lines.

C2. `corpus/knowledge/2026-10-14-r12-01-queue-b-ready.md:11` ("content-addressed family extends to
pwntools-elf") and its source `corpus/knowledge/2026-10-13-r4-16-frontier-rescan.md:735-737`
("content-addressing extends to pwntools-elf"). Both labels rest on same-path repeats only
(`checks2.txt`, `ibl-prior.txt`). Under the R26-C1 frozen rule, the table's copy run shows
the verb is path-sensitive. Pointer census: both files have 0 references to the r26 entry or to
`round-26/c1` (`pointer-check.txt`). QUALITY #14 already ruled the bare "content-addressed" label
inadmissible.

## Assigned statements: not contradicted, but unqualified

| path:line | relation to the table | qualifier missing |
|---|---|---|
| `corpus/QUALITY.md:24` (#14) | universal `f(content, path, params)`; seven rows refute it | none; row 15 marks it superseded |
| `corpus/QUALITY.md:25` (#15) | agrees: `analyze`, `inspect`, `function` content-keyed | no pin; no pointer; the "recorded" list lacks the first path-sensitive native reader (`inspect-binary-layout`) |
| `SKILL.md:407-419` | agrees | under heading "Known limits (r4)", no pin, no pointer |
| `SCORECARD.md:61-67`, `:327-372` | dated luna-round-3 record; "no family beyond the recorded ones is claimed" still true | none needed (historical round record); its "active-surface universal hits 0" did not cover C1, which is family-scoped but now has the wrong member |
| `corpus/knowledge/2026-10-14-r9-02-queue-a-ops-2.md:146-183` | agrees with the `function` row | pin unstated (line 67 names 6.4.0 for another candidate) |
| `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:116-122` | see U1 | vocabulary, plus a same-pin counterexample with no pointer |

All six files have 0 references to the r26 entry (`pointer-check.txt`). Only `corpus/README.md:206`
got a round-26 sub-bullet (`git diff a0639d8e fe3eb4ed -- corpus/README.md`).

U1 (observation). r17 is the same pin (6.5.0), the same operation (`binary_overview`) and the same
`rea-workflow` provider as the table's `analyze` row (`providers.txt`). On `/usr/bin/aether` it gave
same path, same sha256 `06c91f55…`, ids `ev_ae9f7086…` versus `ev_247261e8…`, with `string_count`
29118 versus 29117 (`checks3.txt`). Round 18 got `ev_247261e8…` again
(`r18-swiss-map-replay.md:105-107`). Under R26-C1's derived_verdict, base != repeat means that
carrier is `unstable`. Yet r17:118 calls it "consistent with the content-keyed `analyze` id". The
table is not wrong, because its Limits scope it to one carrier. But the C1 entry (lines 73-74,
"provider determinism") and README:75/206 never point at this same-pin unstable case, and r17
never points at the table.

U2 (observation). r9-02 already ran `function` on a renamed byte copy (`libc.so.6` to
`libsystem_c.so`, r9-02:28, :298), with the same id and the pin unstated. The C1 entry
Limits (lines 110-111), `README.md:75` and the planned row `SCORECARD.md:3081` say a different file
name was "not tested". That is true at 6.5.0, but none of them cites the r9-02 run.

U3 (observation, plus inference). r12-01:26 ran `inspect-binary-layout` with `rea-agents@6.4.0`
and recorded the same id the table records at 6.5.0. The README:75 phrase "ids are pin-specific"
holds for 6.5.0 against 6.7.0, the only pair the entry measured. [INFERENCE] It does not hold for
6.4.0 against 6.5.0 on this verb.

Impacted axes: depth, because a live craft rule contradicts the new table (C1). Calibration, because
self-description sites lack pin and pointer (#15, `SKILL.md:407-419`). Wave-1 provenance, because
IdentityClaimsMap F5 and its row 16 are false negatives.

## Smallest safe correction

Fixable defect, not a tradeoff:
1. Under QUALITY never-rewrite governance, append QUALITY row 36 superseding #15's "recorded" clause.
   It should cite the r26 entry, add `inspect-binary-layout` path-sensitive at 6.5.0 on
   `/usr/bin/jq`, and make the unit per verb at a named pin.
2. Add a SKILL.md superseding note after the craft bullet at `SKILL.md:86-107`. It should say that
   the r12-01:11 example is path-sensitive (it cannot be checked byte-exact across paths) and add
   path-sensitive as a third class. Add a pointer at `:419`.
3. Append correction sections to r12-01 and r4-16 pointing at the table. Append one to r17 that
   names aether as `unstable` under the R26 rule.
4. Optional: have the C1 entry cite r17 aether, r9-02's renamed copy, and the 6.4.0 equal id.

Unknowns: I did not test whether the 6.4.0 `inspect-binary-layout` id is path-sensitive (no
two-path run exists at 6.4.0), and I did not re-read the `/tmp` scratch files behind r9-02.

## Artifacts (in `/fast/scratch/hyaku/kaidoku-r26/seats/w2/SupersedeConsistency/`, sha256 at 13:02:31Z)

statements.txt f05aca4445337ce88cd76280867bc16a791ae0818cd7f87c47235c9bba69ebbb, providers.txt ffc4421fb03f601778a0950a2e73aed5cca6b6a3d1998c0893ee5d91c8dbb84b,
grep-hits.txt e09385f6b3487465e37845f54208d40b55973b128288acfb48823a4046008c83, r7-01-r12-01.txt 2e215b11e6fe30db139f62a1507dc8688010bcc2db0ad917a1cc0cf278f892a3,
ibl-prior.txt 70e3b63496ee0d42e5182070fe6ba65c7685d3e0d5a5e90be042a0cb952b3372, checks2.txt 7d60753c0bdfd8884a6e6c2026b5e861583452943f47694f65a80d05d8a1c0fc,
checks3.txt 264251ed54ffd6640e5cf4faf97363ca0bc0eb41eb25e89bae3a6bd7dcff6ee1, pointer-check.txt b3c89480eeaa44ccb099d893b95cdcbdca02b9e1eb3481bd3ff211dea4375bbd,
r17-r18.txt 5a2f94f179492ce2300380ca0e6ab26d8bebd39a1e6ac90d1c75daed0f23f629. Tooling: none installed or updated.
