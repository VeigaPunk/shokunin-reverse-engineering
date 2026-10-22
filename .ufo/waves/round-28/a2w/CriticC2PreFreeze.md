# CriticC2PreFreeze: R28-C2 pre-registration (critic, round 28 attempt 2)

Attacked: the claim that the R28-C2 fetch made after the freeze at 86fa8526 (17:21:55Z) is a fresh, pre-registered test of the Sourcify `filtered` rule. Lane tip read: 9db24c9e (entry, lesson and QUALITY rows 41 to 43 landed at 18:23:33Z).

## Verdict: weakened (not invalid)

The counted result (mismatches 0 of 246, predicted_true 59) stands as a correct count. But the fetch after the freeze carries no new candidate or flag information beyond what was on disk or already observed before the freeze. So it is a second-instant re-observation of a code-derived rule, not a held-out prediction. The entry at 9db24c9e does not say this.

## Counterexample (observation)

Every one of the 230 counted responses holds the same multiset of (name, filtered) pairs as bytes the L1 had already fetched or probed before the freeze:
- The 43 round-25 selectors match the committed round-25 openchain responses on all 43 selectors. The pre-freeze probe ran the rule on exactly those responses. All 10 canonical-key selectors, and so all 59 predicted-true entries, belong to this set. The true branch of the claim was fully observed before the freeze.
- The 187 held-out selectors match the C1 lookups on all 187 selectors. The C1 lookups used the identical URL (`...lookup?function=0x<sel>&filter=false`). 125 of those 187 were fetched before the freeze, from 17:17:28Z, with 104 entries, 0 `filtered=true` and 0 rule mismatches. The other 62 were fetched while the C2 fetch was running, until 17:24:10Z.
- The claims file records the fact that rules out a held-out true branch before the data: "0 of the 187 held-out selectors are" canonical keys (claims-c2.json, `pre_freeze_probe.what`).

Evidence, from `python3 -I -B prefreeze-overlap.py` (scratch), exit 0, 2026-10-22T18:23:54Z:
```
c1_openchain_heldout_pre_freeze=125 post_freeze=62
pre_freeze_c1: entries=104 filtered_true=0 rule_mismatches=0
c1_vs_c2_heldout (name,filtered) multiset: same=187 differ=0 []
r25_vs_c2 (name,filtered) multiset: same=43 differ=0 []
c2 set=r25 selectors=43 entries=99 predicted_true=59 filtered_true=59 canonical_keys=10
c2 set=r28-heldout selectors=187 entries=147 predicted_true=0 filtered_true=0 canonical_keys=0
```
The probe reproduces, from `python3 -I -B probe-repro.py`, exit 0, 2026-10-22T18:25:06Z: `r25_responses=69 entries=216 mismatches=0 predicted_true=147 canonical_selectors=10`.

## Why weakened and not invalid

- Observation: the rule's inputs were not tuned to the probe. The pinned `canonical-signatures.json` is byte-identical to upstream. `curl -sS https://raw.githubusercontent.com/argotorg/sourcify/189cd726f7ed8fb3d2f503402d5c133e0f50e1fd/services/4byte/src/utils/canonical-signatures.json` returned http=200, exit 0, at 2026-10-22T18:25:30Z, with sha256 `5572beb5...b3e2`, the same as the lane pin. Quote at line 111: `"signature": "name()",` (under `"0x06fdde03"` at line 110).
- Observation: the selector list is a fixed union (round 25's 43 plus round 28's 187 held-out), not chosen by outcome: `cut -f2 selectors.tsv | sort | uniq -c` gives 43 r25 and 187 r28-heldout.
- Observation: the counter sha256 `4fdf7db8...60ef` is the same at 86fa8526 and at a2673116 (`git show <rev>:tools/round-28/c2-filtered-flag.py | sha256sum`). The counter has no later commit.
- Inference: what the claim does test is that the service answered with the same flags at a second instant (17:22Z to 17:26Z) and that the frozen counter recomputes the probe's result on new bytes. What it does not test is a prediction on data nobody had seen.
- Inference, about the bias the probe could introduce: a forking-path or optional-stopping bias. The claim was declared only after a 0-mismatch probe. A failing probe could have led to a different claim, canonical copy or selector set, and the freeze cannot exclude that. The rule being read from code limits this risk, but the probe made the outcome known in advance on 100% of the true branch and on 125/187 held-out responses.

## QUALITY rows 33 and 38

- Row 33 (instruments pinned at freeze): holds on manual check, but the gate never ran on R28-C2. Observation: `freeze-gate.py --root . --rev a2673116` exits 0 (18:24:21Z), and its `freezes` list holds `.ufo/waves/round-28/claims.json` but no `claims-c2.json`. The cause is the gate regex `^\.ufo/waves/(round-[0-9]+)/claims\.json$` (freeze-gate.py:45). `corpus/claim-freezes.tsv` has no round-28 row (grep, no match). The row 33 check for C2 is therefore unrun and has not passed. It must be reported as "manual check only, gate blind to a second claims file".
- Row 38 (counter before the data it counts): holds literally. The counter was committed at 17:21:55Z, every C2 manifest utc is later (17:22:05Z to 17:25:57Z), the files were first committed at a2673116, and the counter refuses earlier fetches and commits (selftest case red-early-fetch). The row's guard only sees the counted files. The same bytes reached the L1 by two other paths before the freeze (the round-25 committed data, and the C1 lookups, which were fetched from 17:17:28Z and committed at 17:25:49Z). Inference: row 38 does not catch data the L1 has already seen when it arrives under another directory. That is a gap in the row, not a breach of it.

## Provenance defect (observation)

The probe time in claims-c2.json is impossible as written. `git show 86fa8526:.ufo/waves/round-28/claims-c2.json` gives `"utc": "2026-10-22T17:24Z"`, which is 2 minutes after its own commit (`git show -s --format=%cI 86fa8526` gives 14:21:55-03:00, that is 17:21:55Z). The probe ran before the freeze, as the file says, so the recorded time is wrong. The real time is unknown. It must be corrected in a later disclosure (never by editing the frozen file) or labelled unknown.

## Exact disclosure the report must carry

Put this in the C2 entry Limits, the SCORECARD R28-C2 line and the round-28 lesson:

> Pre-registration was weakened. Before the freeze (86fa8526, 17:21:55Z), the L1 ran this rule on the 69 committed round-25 openchain responses (216 entries, 0 mismatches; the recorded probe time "17:24Z" is wrong, because it is later than the freeze commit, and the true time is unknown). It had also fetched 125 of the 187 held-out openchain `filter=false` responses for R28-C1, from 17:17:28Z (104 entries, 0 flagged). The fresh 230 responses repeat those (name, filtered) pairs on every selector (43 of 43 round-25 and 187 of 187 held-out). All 59 predicted-true entries come from the 10 round-25 canonical selectors already probed. None of the 187 held-out selectors is a canonical key, which was known before the freeze. So this is a re-observation at a second instant of a rule read from code, not a held-out prediction. 26 of the 36 canonical keys remain untested. The row 33 freeze gate does not audit `claims-c2.json`.

## Smallest safe correction

No recount. Add the disclosure above. Relabel R28-C2 in SCORECARD as "confirmation (pre-seen data)" rather than as a fresh held-out test. Route two hygiene items: the gate must audit every `claims*.json`, and row 38 or a new row must require that a pre-registered test set exclude responses already fetched by any path. A real held-out test needs selectors from the 26 canonical keys not yet observed, frozen before any fetch.

Impacted axes: depth (R28-C2 learning claim strength), provenance (probe utc), gate coverage (row 33 tool).

## Artifacts (/fast/scratch/hyaku/kaidoku-r28/seats/a2w/CriticC2PreFreeze/)

- prefreeze-overlap.py `1f63653d72634ed0c021bed63c3449528dfcfb338f256a1bff5845d25d786ed1`
- overlap.out `ea4ddc42deb88edcb5c7d117c7b9eada3fbe9324a460c5a2232a1dd35f5e7fe4`
- probe-repro.py `c5ddfd5ab0204126132348954523e4a487916e5b9bb3e62cce30f856942a69b0`
- probe-repro.out `c9e0adbc9edd8a350b00eb96aa800d5c94cca4e217877c38b43ea71bd4128729`
- freeze-gate.out `ec69e6e40935d3294ed4fe987ebfd79b403eb919eacc2b690cc9c99ebd185f99`
- upstream-canonical-signatures.json `5572beb596c9062be042b11be4a8cbd6a875be67a518dc0046b220433878b3e2` (source S085, accessed 2026-10-22)

Tools installed or updated: none. Network: one GitHub raw fetch, and no requests to 4byte.directory or openchain. REA: not used.
