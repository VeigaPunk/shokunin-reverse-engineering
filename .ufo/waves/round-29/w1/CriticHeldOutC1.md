# CriticHeldOutC1 — held-out relative to what?

## Verdict and axes

**Attack verdict: holds as the declared, bounded coverage/completeness claim; fails as an interpretation of blind, answer-unseen generalization.** This is a scoped critic recommendation, not admission or canonical judgment.

Impacted axes: coverage breadth, epistemic independence, provenance precision, and discrimination of naming rules. The strongest objection is not that public names make measurement impossible. It is that author-selected familiar answers plus a selector-token screen establish substantially less independence than the unqualified phrase “held-out names” suggests. The frozen limits already disclose the central limitation. Do not silently replace the declared completeness target with an accuracy target.

## Findings

### 1. The answers were available before the freeze; the measured outcomes were not necessarily known

**Observation:** the frozen claims file, C1 `limits` (line 49), explicitly says the screen does not remove selectors the L1/models may know and that names are well known by design. The entry's Limits, lines 92–94, says fifteen interface lists were written by the L1 without opening their standards this round, and the compiler ABI is the ground truth. The L1 necessarily supplied the signature labels when authoring the interfaces. Freezing those labels before REA/lookups prevents retrospective relabeling; it does not blind their author.

**Inference:** the L1 could know every intended name before the freeze and reasonably anticipate database inclusion. The frozen H2 even gives that expectation. **Unknown:** whether the L1 knew the exact future lookup order, collision set, REA argument errors, or 122/122/0 outcome. Familiarity is not evidence of an undisclosed pre-freeze fetch. The receipts support temporal separation of collection, not cognitive novelty.

Smallest correction: call the evaluation author-selected and selector-token-unseen-at-base, not author-blind or answer-unseen. No retrospective replacement of frozen inputs is needed for the declared claim.

### 2. `name_seen` is sufficient for its literal token property, not semantic answer novelty

**Observation:** the screen searches whole-word eight-hex tokens, not canonical signatures or names. The independent base scan found:

```
rows=152 hex_substring=0 sig_text=3 name_call=18 any=19
```

The strongest specific counterexample is `d21220a7 token1()` (carrier n06): its full signature already appears in the base's canonical-list file. Located base quote, line 35: `"signature": "token1()",`. The list associates it with `0x0d0f30c6`, not `d21220a7`. Thus this is a genuine pre-existing answer string, **not** proof that the correct selector/name association or an openchain result for `d21220a7` was previously observed. `version()` and `description()` also have literal matches, but generic-language matches are weaker evidence and should not be called prior EVM answers.

**Inference:** `overlap=0` does not establish “no answer name was in the lane.” It does establish the narrower frozen property. The substring scan found no embedded selector occurrences for these 152 rows, so the theoretical whole-word-versus-runtime-hex gap supplies no observed counterexample here. Bare-name matches are not 18 proven contaminations.

Smallest correction: retain the frozen screen and state exactly what it screens. A future genuinely answer-unseen experiment would require independent interface selection/labels and a semantic exposure policy; merely changing this screen after observing outcomes would change this experiment's identity.

### 3. A public-name naming test can fail, but this snapshot is weak evidence about wrong-name risk

**Observation:** the reachability probe over saved rows/responses reports:

```
rows=152
A_wrong_impossible(args_match,truth_unfiltered_in_oc)=125
C_args_mismatch,no_decoy_with_rea_args=27
truth_first_in_openchain=152
truth_in_openchain=152
```

The first group cannot yield a wrong sole argument-consistent unfiltered name on these bytes: the true name is already an eligible candidate, so another eligible name forces abstention. The remaining 27 rows have no wrong unfiltered candidate matching REA's inferred arguments. This is a conditional explanation of this snapshot, not proof that selecting public interfaces guarantees success beforehand. The entry also records three same-argument collisions causing abstention and 30 total no-name rows.

**Inference:** public names do not make a naming-rule test unfalsifiable. Missing database truth, incorrect REA arguments plus a sole matching decoy, collisions, and changed database contents can lower recall or produce errors. Familiarity alone cannot make an unchanged deterministic rule bypass those inputs. However, here the true signature is present and first in openchain on every row; even `openchain_first` achieves 152/152. Consequently zero primary errors here does not isolate the value of filtering/argument checks, establish error calibration, or justify saturation of the broader reverse-engineering frontier.

The completeness claim is different: even many wrong names could satisfy its frozen target if honestly scored and reported. Its counter's lines 403–405 require complete runs/rows and tally/entry agreement, not H1 or H2. This is a disclosed coverage-learning tradeoff for the canonical judge to evaluate, not a fixable counter defect discovered by this attack.

## Evidence commands, exact excerpts, status

All paths below are absolute; all accesses were on 2026-10-22. No REA invocation, network request, judge, integration, installation, or lane mutation other than this report was performed by this review. Earlier receipts are cited as receipts, not rerun successes.

1. Producing command: `python3 /fast/scratch/hyaku/kaidoku-r29/seats/w1/CriticHeldOutC1/screen-gaps.py /home/vgpnk/Projects/shokunin/kaidoku-shokunin bacbe9cc31d09b5e58e265b0138bd75d0cdb6b47`. UTC start `2026-10-22T20:22:01Z`, exit 0; exact output: `rows=152 hex_substring=0 sig_text=3 name_call=18 any=19`. Output file line 1: `d21220a7 token1() n06 hex_substring=0 sig_text=1 e.g. corpus/evidence/round-28/c2/canonical-signatures.json name_call=1` (the relative filename is literal probe output).
2. Producing command: `python3 /fast/scratch/hyaku/kaidoku-r29/seats/w1/CriticHeldOutC1/wrong-reach.py /home/vgpnk/Projects/shokunin/kaidoku-shokunin`. UTC `2026-10-22T20:21:45Z`, exit 0; exact excerpts are the five reachability lines above. This reads working-tree evidence, not pinned Git objects; the probe does not independently certify all manifest hashes.
3. Receipt `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-29/before/preseen-c1-name.txt`: records the preseen command with `--kind name`, UTC `2026-10-22T20:01:29Z`, exit 0; exact excerpt: `kind=name rev=bacbe9cc31d09b5e58e265b0138bd75d0cdb6b47 test_selectors=152 seen_set=58720 overlap=0`.
4. Receipt `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-29/after/c1-at-18be864a.txt`: records the C1 counter at measured tip, UTC `2026-10-22T20:16:35Z`, exit 0; exact excerpts: `primary rule openchain_sole_unfiltered_args_consistent: named 122, right 122, wrong 0, no_name 30` and `runs_ok=16/16 rows_complete=152/152 tally_equal=1 entry_ok=1`.

## Smallest safe SCORECARD wording

> R29-C1 — bounded coverage/completeness learning measurement: the unchanged round-25 rule was scored on 16 freshly compiled, author-selected public-interface stubs and 152 selectors absent as standalone eight-hex tokens from lane files at the base. Saved receipt: 16/16 runs, 152/152 complete rows, tally/entry checks satisfied; primary named/right/wrong 122/122/0, abstained 30. Labels were supplied by the L1 before freezing, not hidden from it; name strings were not screened for prior exposure. This is new-carrier/public-name snapshot coverage, not blind answer-unseen validation, general error calibration, or evidence of frontier saturation. WETH9 contributes a run but no held-out scoring row.

## Primary local sources

Local URLs below mean `file://` followed by the absolute path. Access date for every row: **2026-10-22**. Quotes are contiguous and at most 25 words. No external source was opened by this seat.

| Absolute path (file URL) | SHA-256 of bytes read | Located quote |
|---|---|---|
| /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-29/claims.json | 76bc0d8f556019763157bbb74cd43b9983b9e7cf77ad9d92cae898365a60cf79 | :49 `The held-out screen removes selectors the lane wrote down, not selectors the L1 or the models may know` |
| /home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/knowledge/2026-10-22-r29-evm-fresh-selector-naming.md | fe5e8e9fe35e1f340d5cc7c3f0851436f0c91cfa79c03eb8614e2aaaadf1c82b | :93–94 `The ground truth for every row is still the compiler ABI, not the standard text.` |
| /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-29/preseen.py | 073381ca213573b8809a130cf3d958e0b253b4d56a7ce34079ef2f2b0c89d167 | :6 `every 8-hex-digit token, with or without` |
| /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-29/c1-fresh-naming.py | 6ad79d1099730185bf867d98f6bb4f32c4a4a910bb346669fa2860b36993fdda | :405 `return 0 if full else 1` |
| /home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-28/c2/canonical-signatures.json | 5572beb596c9062be042b11be4a8cbd6a875be67a518dc0046b220433878b3e2 | :35 `"signature": "token1()",` (also located by read-only git grep at the base) |
| /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-29/before/preseen-c1-name.txt | ca22991a8ce4ab42b03af61a89dbcec1d459b3321218c95c318c3186b4ae9dbc | :3 `test_selectors=152 seen_set=58720 overlap=0` |
| /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-29/after/c1-at-18be864a.txt | 6987bd9970b86d8ef63f360542e6791992326cb5b875dab9cd2fe42a40fcbdae | :4 `runs_ok=16/16 rows_complete=152/152 tally_equal=1 entry_ok=1` |

## Seat artifacts

No tools installed or updated. No proposed lane code edits. Every seat artifact is under the assigned scratch directory:

| Absolute artifact | SHA-256 |
|---|---|
| /fast/scratch/hyaku/kaidoku-r29/seats/w1/CriticHeldOutC1/screen-gaps.py | 1f6f17d271d6c19af548dd642a8e9108c3a772de9be1401d71ec96a51c7c736f |
| /fast/scratch/hyaku/kaidoku-r29/seats/w1/CriticHeldOutC1/screen-gaps.out | 96f44d6549d0ab301892fdabc8f59ab97adcbc6d3207dd06dd59444948e90b8b |
| /fast/scratch/hyaku/kaidoku-r29/seats/w1/CriticHeldOutC1/wrong-reach.py | 36c73ed2a1c4e9ee3e87bc007ff3d6b42fb486ecf06c83fc6f84ff33f1ac71e9 |
| /fast/scratch/hyaku/kaidoku-r29/seats/w1/CriticHeldOutC1/wrong-reach.out | 038224302866e65aad93e66186f97940478082faf48af875230485b5ee2b705e |
