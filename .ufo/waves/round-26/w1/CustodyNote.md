# CustodyNote — routed defect 1 (round-25 verifier spot-check)

Seat: KaidokuR26.CustodyNote (wave 1, scribe, no dispatch). Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Verified against lane tip `fe3eb4edf410244eff46151a148c8f754be1ce80`; the SKILL.md section was byte-identical at `c27f445e…`, `81f63f36…` and `c3277726…` (section blob `118f11cfac77f930ba5630ff4d8e01c8bef2165b`). Read-only git and file reads only; I edited no lane file.
**Integration status.** The L1 landed the superseding note at `c327772653badd3b19b3954e1f8713973aa3f93e`; the landed note (`SKILL.md:834-881` at the tip) is byte-identical to my first draft revision, sha256 `8253724717ab3ac24527c1f1b3af7e5853d3970f7069ded0cdfce9f9ac822a3c`, and `git diff c27f445e..HEAD -- SKILL.md` shows 49 insertions and **no deletions**, so no filed byte of the round-25 section changed. My final revision (three wording refinements, sha256 `0bfaaa75e31deea900d8b7d7e7953625474f78dbd6b1ef3d9db9f0ab62c2333e`) is the section 4a delta on the landed text; it is not needed for correctness.

## 1. Verdict

| Item | Verdict |
|---|---|
| `fafdd283` landed `tools/round-25/instrument-custody.py` | holds |
| The attempt-1 custody claim was abandoned | holds as "not continued"; "abandoned" is the routed defect's word, not the lane's |
| SKILL.md says the candidate "is not implemented at this phase" | holds; stale at the tip |
| Registry row `round25-custody-ruler` says the same | fails: the row never contains that sentence |
| A status-cell change in that row is needed | not needed; no cell in the row is factually wrong, and L1 landed none |
| An append-only superseding note after the section discharges the defect | holds; L1 landed exactly that |

## 2. Located lines (byte-exact, `git show HEAD:<path>`; file sha256 at HEAD in brackets)

**SKILL.md** [`cf047307dbab77369ffe31de3f7f4eeab797293c085253eba28d6978a735ad42`] — `780` `## Explicit instrument-reference custody — round 25 prospective authority`; `787-788` "The candidate `tools/round-25/instrument-custody.py` is not implemented at / this phase; missing candidate is unavailable2 and cases are not observed." (the stale sentence; also carries the run-together token `unavailable2`, defect 7 of the same spot-check); `783` "`62feef9c0cbd5aadafa453456c55c28832175206` before a round-25 SRT or candidate." (still true, I predates the candidate); `798-803` the prospective path and "Only actual Main first-add F can establish discovery of a twelfth freeze." (F did happen at `a4ab912a`, so it reads stale, but it is about the freeze ledger, not the candidate; the note covers it); `805` registry header `| Name | Kind / owner | Entry / verdict map | Self-invocation | Pinned values / write scope |`; `807` the `round25-custody-ruler` row — kind `gate, conformance limits disclosed / kaidoku`; entry the ruler CLI with exit map `0 original34 pairs exact, 1 observed pair mismatch, 2 unavailable/tampered/unsettled/root-state-change/unevaluable measurement`; self-invocation `None exposed: separate gate-selftest conformance is not claimed`; pinned `Ruler sha25620fe3f3d…; original34/I immutable`. **No cell says the candidate is unimplemented**; the row names the ruler only.

**SCORECARD.md** [`cfe8b5257c90b14b3f7cbe1349d6117a78494632096ab1fa2594e189038d977a`] — `2937` `## Round 25 — prospective explicit-reference custody`; `2950-2951` "Before availability must come from Main's actual receipt: an absent / candidate means cases not observed/executed0, not34 observed failures." (a rule, still true); `2954-2959` "Planned, superseding the earlier round25 queue: receive the real before / receipt, complete qualified proposal distillation, and have Main decide and / land `reports/round-25/claims.json` with I and all authority digests before / any `tools/round-25/instrument-custody.py` implementation." (stale; also names the superseded `reports/` claims path); `2972-2973` "Main's actual I ruler over B returned exit2/candidate_unavailable: / declared34, executed0, exact0, all34 not_observed, candidate SHA null." (a true historical receipt, the before state); `3050` "Attempt 1's prospective 34-case custody claim (`.ufo/waves/round-25/claims.json`) was not continued and has no after value." (the abandonment record).

**LOG.md** [`60dc8c45c4f6637de56d96aa91e8e1ac47a7184023f3ac82da43c729e8dd18f6`] — `2809` `## 2026-10-21 — round25 prospective ruler/oracle custody`; `2816` "No candidate or SRT landing is yet claimed … Absent candidate means not_observed/executed0, never34 observed failures." (stale at the tip); `2822` and `2827-2828` "candidate_unavailable, total34/executed0/exact0/34not_observed, candidate / SHA null." and "`reports/round-25/claims.json`, not yet Main-approved or landed; no candidate / implementation." (stale; also the superseded claims path); `2950` "No source/gate/fixture/candidate execution, F or code permission is claimed." (a dated 2026-10-21 entry; no later LOG entry records the landing or the abandonment).

**Lessons** — `corpus/lessons/round-25.md:29-30` "`tools/round-25/instrument-custody.py`, which does not yet exist. The candidate / must be implemented only after Main's actual claims landing and permission." (stale); `:34` "Absent candidate means unavailable, all cases `not_observed`, executed 0;" (a rule, still true); `:355` "There is still no F, candidate/code/runtime permission or admission." (stale); `:357-364` `## Attempt 3 — repair the round-24 outside verdict, then name EVM selectors` and "Attempt 1's prospective 34-case custody claim above was not / continued: it has no after value in this round and is reported as not / pursued, not as met. Everything above this heading is attempt 1's record and / stays unchanged." (the abandonment record; it says attempt-1 text above stays unchanged). `corpus/lessons/round-25-verifier-spotcheck.md:183-186` is the routed defect itself.

**Ledger** `corpus/claim-freezes.tsv:13` (unchanged at the tip): verdict `FLAGGED`, findings `INSTRUMENT_ABSENT,INSTRUMENT_REVISED`, pointer naming `fafdd283` and "froze at a4ab912a before tools/round-25/instrument-custody.py existed (added fafdd283, by that design)". Already discloses the landing; no change needed.
**Attempt-1 claims** `.ufo/waves/round-25/claims.json`: `:34` subject path, `:35` `"status_at_preregister": "absent; no stub/noop"`, `:42` claim id `R25-C1` (calibration), target `ruler_exit 0, exact 34`. Attempt-2 `.ufo/waves/round-25/a2/claims.json:12` "Attempt 2 does not continue its preregistration packet and makes no claim on its 34-case contract."

## 3. Git verification of `fafdd283`

`git show --stat fafdd283` → one file, `tools/round-25/instrument-custody.py | 514 +++++`, "1 file changed, 514 insertions(+)"; author `kaidoku-shokunin <kaidoku@shokunin.local>`, author date 2026-10-21T23:42:27-03:00, commit date 2026-10-22T00:19:50-03:00. Parent `a4ab912a956fb863fedb0e9b9bb866777af27495` (the attempt-1 claims first-add; its parent is `62feef9c…` = I); `git merge-base --is-ancestor fafdd283 HEAD` exit 0, `git branch --contains fafdd283` lists `main`.
Blob `8a6e21f18e805c7ce44e03a9a4872e9063073c32`, mode 100755, identical at `fafdd283` and at HEAD; sha256 of the bytes `54c43cdc01930fcb58f14053d8099f4b28352147656a05d811574cc74e7d34fb`, 21190 bytes. Ruler unchanged at the tip (`git show HEAD:tools/round-25/ruler.py | sha256sum` = `20fe3f3d3d68ba21c8d8bbfed175bb57db46a8618bd179b179acb6fda99d0532`); cases at I unchanged (`6c851cd704b84ef728415d674ad78ec7ff4da449883f1aeba3e4ca47631cd3e0`).
Non-main sibling commit `e164f2e8587997dbc701d7f2dfbc84a2bd70a167` has the same parent and blob, is not an ancestor of HEAD (exit 1), and is referenced only by `refs/jj/keep/e164f2e8…`; not the landed commit. Lane gate receipt `corpus/evidence/round-25/a3/after/freeze-gate-at-1e064f9b.json` records for the round-25 freeze `INSTRUMENT_ABSENT` for the path and `INSTRUMENT_REVISED` at `fafdd283…`, `disclosed: 0`, verdict `FLAGGED`.
Outside the lane, in the fleet repo, Main measured the landed subject: `/home/vgpnk/Projects/shokunin/.ufo/waves/hyaku/kaidoku25-prerequisite/parent-after-process.json` (sha256 `d15f5581a6e968121cb9963a561a95421e24a871842dd5829acb994a7d64a958`) — exit 0, `total 34, executed 34, exact 34`, finding `all_declared_pairs_exact`, at 2026-10-22T03:28:48Z, `candidate_sha256` equal to the value above, `rev` = `fafdd283…`. Its own authority record (`measurement-authority.json`) states `"admission": false`. It is not a lane receipt and carries no lane claim.

## 4. Draft text

### 4a. Superseding note — landed text and my final revision

Placed directly after the round-25 section, with no change to that section's bytes. My final revision (sha256 `0bfaaa75e31deea900d8b7d7e7953625474f78dbd6b1ef3d9db9f0ab62c2333e`, 3309 bytes, also at seat scratch `draft/skill-note.md`) differs from the landed text only in the three wording points marked below. The full draft, with spaced words and no run-together tokens, is the block below; the landed text is the same block with the three bracketed variants in place.

```markdown
## Superseding note — round 25 custody subject landed; the filed wording above is superseded

This note is appended after the round 25 section above and changes no filed byte
of that section. The section above was written at the claims freeze commit
`a4ab912a956fb863fedb0e9b9bb866777af27495`, when the subject
`tools/round-25/instrument-custody.py` did not exist. Its sentence stating that
the candidate is not implemented at this phase, that a missing candidate gives
an unavailable verdict with exit 2, and that the cases are therefore not
observed, described that moment. It is superseded from commit
`fafdd283432731a675b71e201bb9ba767c394553` onward.

What landed. Commit `fafdd283432731a675b71e201bb9ba767c394553` (parent
`a4ab912a956fb863fedb0e9b9bb866777af27495`) added one file,
`tools/round-25/instrument-custody.py`: 514 lines, 21190 bytes, sha256
`54c43cdc01930fcb58f14053d8099f4b28352147656a05d811574cc74e7d34fb`, blob
`8a6e21f18e805c7ce44e03a9a4872e9063073c32`, mode 100755. The same blob is
present at the lane tip when this note is written. [landed: "is at / the current lane tip."]
The fixed ruler and the 34 literal pairs are unchanged: the ruler sha256 at the tip is
`20fe3f3d3d68ba21c8d8bbfed175bb57db46a8618bd179b179acb6fda99d0532`, and the
cases sha256 at `62feef9c0cbd5aadafa453456c55c28832175206` is
`6c851cd704b84ef728415d674ad78ec7ff4da449883f1aeba3e4ca47631cd3e0`. The
registry row `round25-custody-ruler` above therefore keeps its entry, its exit
map and its pinned digests unchanged.

The claim was not continued. The attempt 1 calibration claim R25-C1 in
`.ufo/waves/round-25/claims.json`, the explicit caller selected 34 case
custody contract, was not continued and has no after value in this lane. The
lane's own wording is "not pursued, not as met"
(`corpus/lessons/round-25.md`, the "Attempt 3" heading, lines 361 to 364, and
`SCORECARD.md` line 3050). The freeze ledger row for round 25 is FLAGGED with
the findings INSTRUMENT_ABSENT and INSTRUMENT_REVISED, and its pointer names
`fafdd283` (`corpus/claim-freezes.tsv` line 13). The committed gate receipt
records the same two findings for the round 25 freeze, with INSTRUMENT_REVISED
at commit `fafdd283432731a675b71e201bb9ba767c394553` and disclosed 0
(`corpus/evidence/round-25/a3/after/freeze-gate-at-1e064f9b.json`). [landed: "the latter naming
`fafdd283` (`corpus/claim-freezes.tsv` line 13; receipt
`corpus/evidence/round-25/a3/after/freeze-gate-at-1e064f9b.json`)."]

One outside measurement exists and is not a lane receipt. The ruler was run over
the subject at commit `fafdd283432731a675b71e201bb9ba767c394553` and recorded
exit 0, 34 of 34 exact, finding `all_declared_pairs_exact`, at
2026-10-22T03:28:48Z. That receipt lives outside this lane, in the fleet
repository at
`/home/vgpnk/Projects/shokunin/.ufo/waves/hyaku/kaidoku25-prerequisite/parent-after-process.json`,
sha256 `d15f5581a6e968121cb9963a561a95421e24a871842dd5829acb994a7d64a958`. Its
own authority record states that admission is false. It is not a claim of this
lane, so no axis score, no admission and no custody conclusion follows here. [landed: fleet-relative path `.ufo/waves/hyaku/…`.]

Wording on the two records above. "Not implemented at this phase" was true at
the freeze and is false at the tip. The round 25 verifier spot check describes
the claim as abandoned. No committed lane record contains a retirement
decision; the lane's committed records say the claim was not continued and was
reported as not pursued, not as met. A reader of this file should use the
lane's wording. [landed: "calls the claim abandoned; … Use the lane's wording."]
```

The three bracketed points are the whole delta: (1) "present at the lane tip when this note is written" instead of "is at the current lane tip"; (2) the ledger pointer and the gate receipt split into a named pointer plus the receipt's own INSTRUMENT_REVISED commit and disclosed 0; (3) the fleet receipt path given absolute, and the closing sentence split so the lane-wording instruction is its own sentence. None changes a fact.
### 4b. Registry row `round25-custody-ruler` — status cell

**No status-cell change is needed, and none was landed.** The row has no "Status" column; the closest status-bearing cell is `Kind / owner`, currently `gate, conformance limits disclosed / kaidoku`, which is accurate. All five cells remain true: the ruler digest and oracle digest are unchanged at HEAD, the exit map describes the ruler's own exit codes, and the row never mentions the candidate. `git diff c27f445e..HEAD -- SKILL.md` confirms the L1 changed only appended lines. Had the L1 wanted the row to point at the landing, the minimal optional change would have been that one cell only: `gate, conformance limits disclosed / kaidoku` → `gate, conformance limits disclosed; round-25 custody subject landed at fafdd283, attempt-1 custody claim not continued / kaidoku`. Recommend against it: the note already carries the fact, and editing the row would break the append-only rule the routed defect states ("no edits to filed bytes").

## 5. Commands used

Read-only git: `git log --oneline -12`, `git status --porcelain`, `git rev-parse HEAD`, `git show --stat|--name-status fafdd283`, `git show -s --format=… fafdd283`, `git rev-list --parents -1 a4ab912a`, `git merge-base --is-ancestor fafdd283 HEAD` (exit 0) and `… e164f2e8 HEAD` (exit 1), `git branch --contains fafdd283`, `git for-each-ref --contains e164f2e8`, `git ls-tree -r --name-only <rev> tools/round-25/`, `git ls-tree HEAD -- tools/round-25/instrument-custody.py tools/round-25/ruler.py`, `git rev-parse HEAD:<path>`, `git cat-file -t e164f2e8`, `git log --format=… -- <path>`, `git log -S <text> -- <path>`, `git blame -L a,b --date=short -- <path>`, `git grep -n … HEAD -- '*.md'`, `git grep -c …`, `git show HEAD:<path> | sha256sum`, `git show HEAD:<path> | sed -n 'a,bp'`, `git diff --stat c27f445e..HEAD -- SKILL.md`, `git diff c27f445e..HEAD -- SKILL.md` (no deletions). Read-only file: `grep -n`, `awk`, `python3` (json/csv reads only).
Sandbox clones `…/seats/CustodyNote/clone` and `…/clone2` via `git clone -q`; inside them only: `python3 -I -B .ufo/gates/c1-census-v10.py --root . --quiet|--json`, `python3 -I -B .ufo/gates/citation-drift/citation-drift-probe.py --root .`, `python3 -I -B tools/round-26/c2-calibration.py --root . --rev <REV>`. Gate results, note appended versus pristine, both in the clone: census verdict identical (`FAIL`, stale=1 in PROVINCE.md, undeclared=1 in SCORECARD.md — both pre-existing at HEAD, none in SKILL.md; SKILL.md loci 3 before and after); citation-drift identical (5 findings, exit 0); C2 instrument identical (5 of 6 mismatches; K1/K2/K4/K5/K6 mismatch, K3 pass; craft span `SKILL.md:81-314` before and after). The note adds no gate finding.

## 6. Artifacts and scope

Seat scratch `/fast/scratch/hyaku/kaidoku-r26/seats/CustodyNote/`: `draft/skill-note.md` (final revision) `0bfaaa75e31deea900d8b7d7e7953625474f78dbd6b1ef3d9db9f0ab62c2333e`; `raw/integrated-note.md` (landed text) `8253724717ab3ac24527c1f1b3af7e5853d3970f7069ded0cdfce9f9ac822a3c`; `raw/excerpts.txt` `8a0f8ea7c26caf0399a91364b075120a1ae7dc1abb50264f4558acd8ca794b69`; `raw/SKILL.md.before` `cf047307dbab77369ffe31de3f7f4eeab797293c085253eba28d6978a735ad42`; `raw/census-before.json` `07deba8bc1f2ef13a0f921172d40d23d3c167b6ae1b4adbb57d4dfac72943243`; `raw/census-after.json` `d4014fe12faa71263625d530d9d4cdf4770f3da98e4fb82ec04ea62365181592`; `raw/c2-clone2.json` (pristine) `4abed6b5f98303be831cea3f184af7a3af2e01d8c6fd1771da517e380588144e`; `raw/c2-final.json` (note appended) `0fc58ba53b05fbe48b868532e3c6b339797997afcba8f6e1eb2e0fcdf0f9e115`.
Out of scope / not done: no lane file edited by me, no commit, no jj command, no Git write in the lane; the clone commits were inside the throwaway sandbox clone only. Routed defects 2-7 were not worked here. No new source was opened and no SOURCES row was written. No tool was installed or upgraded.
## 7. Findings for the integrator

1. Only one lane file states the candidate is unimplemented as an undated present-tense fact: `SKILL.md:787-788`. The other located statements are dated entries (`LOG.md` 2026-10-21), an explicitly frozen attempt-1 record (`corpus/lessons/round-25.md` above line 357), or true historical receipts (`SCORECARD.md:2972-2973`).
2. The routed defect's attribution of that sentence to the registry row is inaccurate; the row is silent on the candidate. Do not "fix" the row — the L1 correctly changed only appended lines.
3. The lane's vocabulary is "not continued" / "not pursued, not as met". No lane record contains a retirement decision; the landed note uses that wording and states plainly that the outside measurement is not a lane receipt and admits nothing.
4. `corpus/lessons/round-25.md:363-364` says everything above the "Attempt 3" heading stays unchanged, so the superseding note belongs in SKILL.md (append-only), not as an edit to lesson lines 27-34 or 355. `LOG.md` still has no entry recording the landing or the abandonment; recording that is a new dated LOG entry, outside this seat's scope and still open. The append-only note is gate-neutral: census, citation-drift and the C2 instrument give identical results with and without it.
