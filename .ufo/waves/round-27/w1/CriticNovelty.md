# CriticNovelty — learning value of R27-C1 and R27-C2 against held round-26 knowledge

Seat KaidokuR27.CriticNovelty, wave 1, critic, leaf. 2026-10-22, times UTC. Lane HEAD `a4f674b343d8564e21f7eb8984630a95089c82d6` (`git rev-parse HEAD`, 14:55:54Z).
Attacks: the novelty of R27-C1 (depth) and R27-C2 (capability) in `.ufo/waves/round-27/claims.json`. No REA call made. Nothing installed or upgraded (read `/home/vgpnk/.omp/agent/RULES.md`, sha256 `beb647d0…99ed`; no install needed).
Read: the round-26 knowledge entry `corpus/knowledge/2026-10-22-r26-native-reader-evidence-id-identity.md`, `tools/round-26/recompute-ids.py`, `corpus/lessons/round-26-verifier-spotcheck.md`, `SCORECARD.md:3061` and `:3081` (planned fields), the drift sentinels in `/home/vgpnk/Projects/shokunin/.scratch/goal-20261022-hyaku-12h.md:163-178`, round-26 seat reports `w2/ReplayRenamedCopy.md`, `w2/PinEvidence.md`, `w2/PinDiffCheck.md`, the closure script `/fast/scratch/hyaku/closure-kaidoku-r26/recompute/r.mjs`, and `tools/round-27/c2-xpin-check.py:1-120`.

## Verdicts

| Claim | Verdict | One-line reason |
|---|---|---|
| R27-C1 | partly new | The jq half mostly repeats held data; the tinyxxd half and three jq renamed cells are new, but every verdict is predicted by the held mechanism. |
| R27-C2 | partly new (repeated as knowledge, new only as a committed tool) | Its 24-envelope answer is already published, the capability ran three times in round 26, and its test set skips the one input class where it could teach something. |

## R27-C1 — strongest objection

1. The jq base and same-path repeat rows (16 of the 24 jq runs) re-run the exact round-26 argv on the same bytes at the same pin. The held table already holds these ids, and `w2/PinEvidence.md` section 2F reproduced all eight live: "All eight ids equal the stored base ids". Observation (committed report text).
2. The jq renamed question was already asked. `w2/ReplayRenamedCopy.md` ran a copy named `jq-renamed.bin` (name and extension changed together, the same change C1 makes): `analyze`, `decompile`, `function` "SAME", `inspect-binary-layout` "DIFFERENT". The held entry records this in its Limits section (lines 121-124). `inspect` calls the same `binary_overview` operation with empty parameters as `analyze` (entry lines 49-52), so its renamed id is already implied. Only `xrefs`, `read-bytes` and `instructions` renamed on jq have no held data point. Observation for the report text; the `inspect` implication is inference.
3. The mechanism already predicts every C1 verdict. The held entry shows the hashed projection keeps subject digest, format and architecture but not the local path or display name (lines 55-60). A source-only prediction matched all eight round-26 verdicts (lines 66-70). My probe confirms that no file name reaches the hashed projection of the seven content-keyed verbs:
   - command `python3 -I -B probe_names.py` (seat scratch), 14:56:50Z, exit 0
   - excerpt: `analyze-copy.json stored_match=True subject_rename_keeps_id=True jq_strings_in_projection=0`; `xrefs-copy.json … =0`; `read-bytes-copy.json … =0`; `instructions-copy.json … =0`
   - the only `jq` strings in the `decompile` and `function` projections are the binary's own text (`"jq: error (at %s): %s\n"`), and in `inspect-binary-layout` the run path
   - rewriting `subject.name` and `subject.local_path` to `jq-r27-renamed.dat` keeps the stored id in 8 of 8 copy envelopes
   - observation for the offline rewrite. A live rename result different from this would need the provider to write the run's file name into a hashed field, which the held entry rules out for the Ghidra verbs (they run on "a private content-named byte copy", line 67). That last point is inference.
4. The claim does not predict anything. Its limits say "Any verdict counts as complete; the claim is that the 16 verdicts re-derive, not which verdict each pair gets". So the claim cannot fail on what it might teach. It can fail only on custody. Observation (`claims.json` R27-C1 `limits`).
5. It is the lane's own registered next move (`SCORECARD.md:3081`: "a renamed-copy and second-carrier extension of the identity table"). That makes it planned, not accidental, but it is the same surface as R26-C1 on the same axis (depth).

## R27-C1 — counter-evidence

- The second carrier is new ground. `git grep -l 7b1e5d0c…3ae65 HEAD -- . ':!.ufo/waves/round-27'` (14:55:54Z) finds only `tools/round-27/c1-rename-identity.py`, the round-27 counter. No earlier envelope or knowledge entry holds tinyxxd's bytes. Observation.
- The one verdict the source cannot predict is "unstable" (provider nondeterminism). Round 17 saw `analyze` give two ids for one file at one path (held entry lines 126-128). Only a new carrier can test that, and the held table has one carrier. Observation (entry text); its relevance here is inference.
- The jq renamed data from round 26 is one uncommitted, single-run replay of 4 verbs, not a table row (`ReplayRenamedCopy.md`, artifacts under `/fast/scratch/hyaku/kaidoku-r26/…`). C1 makes it 8 verbs with a repeat, in committed envelopes. Observation.
- `runs.tsv` now records `pkg_version` and `pkg_json_sha256` per call. That closes routed defect 4 of the round-26 spot-check. This is hygiene value, not new knowledge.

Judgement: partly new. About 3 of 24 jq runs (`xrefs`, `read-bytes`, `instructions` renamed) and all 24 tinyxxd runs are new measurements. Every expected verdict follows from held knowledge, so the learning value is replication on a second carrier, not a new mechanism. Impacted axes: depth (overstated if C1 is reported as new mechanism), and the drift sentinel (see below).

## R27-C2 — strongest objection

1. The answer to its 24-row test is already held and published. The held entry, lines 132-134, says "the 6.5.0 id rule reproduces 24 of 24 ids and the 6.7.0 rule 3 of 24 (all `function`…)". The spot-check, line 100, says `n=24 match_6.5.0_rule=24 match_6.7.0_rule=3`. So C2's row attributions (21 rows "6.5.0", 3 rows "both") are known before the tool exists. Observation.
2. The capability was already exercised three times in round 26, each using installed package code:
   - the closure's `r.mjs` imports each package's own `digestCanonicalValue` for both rules
   - `PinEvidence/oracle.mjs` (sha256 `0ba2c0ef…5df67`) loads each package's own `parseEvidence` and `digestCanonicalValue`
   - `PinDiffCheck/scripts/native-parse.mjs` (sha256 `d10790f1…7e49f94`) calls each package's own `parseEvidence`. That function runs the unexported `computeEvidenceId`, so it uses the package's own projection with no retyping, which is stricter than C2's "own semanticProjection source text" contract.

   Observation (files read, hashed 14:55:27Z).
3. Its "independent recompute agrees with the tool" test repeats round-26 evidence C. `PinEvidence.md` reported "Independent Python recompute of both rules … zero disagreements with B". C2's checker does the same: a Python 6.5.0 rule plus null-inserted 6.7.0 (`c2-xpin-check.py:94-100`) against package code. Observation.
4. The three red envelopes are generated by the checker's retyped rule, so they test that the tool agrees with the checker's own retyping. The lane already holds 133 real 6.7.0-only records (rounds 7, 10, 11, 12, attributed natively in `PinDiffCheck.md` S3). None of them is in C2's test set. Observation.
5. Counterexample: the test set skips the one input class where the tool and the checker disagree. The 6.7.0 projection line is `relationship_coverage: evidence.relationship_coverage,` (6.7.0 `evidence.js:178`, `sed -n 178p`, 14:57:25Z). When the key is absent, that value is undefined. The 6.7.0 package's own digest drops undefined keys:
   - command `node undef.mjs`, 14:56:58Z, exit 0
   - excerpt: `absent 015abd7f…f862`, `undefined 015abd7f…f862`, `null aafc67bb…b7da`

   The checker inserts `null` instead (`projection["relationship_coverage"] = data.get("relationship_coverage")`). I applied both forms to the lane's committed absent-key records:
   - command `python3 -I -B absent_key.py`, 14:57:18Z, exit 0
   - excerpt: 19 rows such as `claims/c2/CR-2/evidence/probe-gas-6.4.0.json stored==id65:True checker_attr=6.5.0 native_attr=both`, then `absent-key records: 19`

   Per `PinDiffCheck.md`, 16 of the 19 are 6.4.0 products, and 3 have no stated pin. The 6.7.0 parser rejects all 19 at schema.

   So on held lane data, the checker's rule labels 6.4.0 output "6.5.0" (observation of the replicated rule). A tool that meets the C2 contract would label it "both" (inference from `undef.mjs` and line 178; no C2 tool exists yet). Both labels are false. Round 26's `PinEvidence.md` already separated 6.4.0 by schema and payload literals. Rule fit alone is therefore weaker than the method the lane already used.

## R27-C2 — counter-evidence

- None of the round-26 attribution scripts is committed. `git ls-tree -r --name-only HEAD | rg 'oracle\.mjs|native-parse\.mjs|recompute_both|xpin'` (14:56:14Z) finds only `tools/round-27/c2-xpin-check.py`. The committed arc-3 scripts (for example `arc3-loop1-round12/claims/c1/EX-7/evidence/recompute-ids.mjs`) cover one pin, retype the projection, and take exactly three files. `SCORECARD.md ## Capabilities` (`:615-625`) has no attribution row. So a durable, reusable two-pin tool with a stated output contract is new to the lane. Observation.
- The 6.7.0 installed-code SOURCES row closes routed defect 1 of the round-26 spot-check. That is hygiene, not learning.

Judgement: partly new as a committed capability. As knowledge it is a repeat: none of its 24-of-24 or 3-of-3 targets can show anything the lane does not already hold. Impacted axes: operability (the capability row would overstate discrimination), calibration (false attribution of 6.4.0 records), discernment.

## Drift sentinel

The goal note, line 173, says: "Same axis+surface claim … in a lane 3 rounds running → next round must work a different frontier area". The `axis` fields in the round-23 to round-27 `claims.json` files read: r24 coverage and calibration; r25 calibration (a2 adds coverage); r26 depth and calibration; r27 depth and operability.

- Calibration ran r24, r25 and r26, which matches `claims.json` `not_claimed`. Observation.
- The evidence-ID surface is round 26 plus both round-27 claims. That is two rounds running, so not tripped.
- C2 changes the axis label but not the surface. Any round-28 claim on evidence-ID identity or attribution, under any axis label, should count as the third round. Inference.

## Smallest safe corrections (no frozen file changes)

1. C1 knowledge entry: present the jq renamed rows as replication of `w2/ReplayRenamedCopy.md` plus three new verbs. Name tinyxxd and the "unstable" test as the new ground. Do not claim a new mechanism.
2. C2: before the capability row lands, run the tool on the 19 absent-key round-7 records as a disclosed, uncounted falsifier. Disclose in the row and entry that rule fit cannot tell 6.4.0 from 6.5.0 or 6.7.0 when the key is absent, and that the checker's null insertion differs there from 6.7.0 code. Better still, have the tool also print each package's `parseEvidence` accept or reject, as `native-parse.mjs` did, which separates the 6.4.0 records.
3. Do not report C2 as learning or expansion. Report it as capability acquisition plus routed-defect closure.

This is a fixable defect, not a tradeoff for the judge to reject. C2's frozen limits ("attribution by rule fit") already exclude the 6.4.0 case, but the capability row must not imply more than that.

## Artifacts (`/fast/scratch/hyaku/kaidoku-r27/seats/CriticNovelty/`)

- `probe_names.py` `be56fb98d9212a69320c02bb257a73364939de198b74f1ced596714ce23364f9`
- `undef.mjs` `0636295b7ccb6da5f2ac77753ed65bf83ea6b39a4f877b113507bca3ae1169e4`
- `absent_key.py` `f4166e0f0d3e6aebeaf8c396c9ade4df726d361fa93751f96603e917e15b3ce8`

Unknown: what a real `xpin-attribute.mjs` prints on absent-key input. The tool does not exist at HEAD, so the "both" label above is inferred from package code, not run.
