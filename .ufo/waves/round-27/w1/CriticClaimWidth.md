# CriticClaimWidth — round 27 wave 1: claim width against counters

Seat: KaidokuR27.CriticClaimWidth (critic, leaf). Attacks: the `statement` of R27-C1 and R27-C2 in
`.ufo/waves/round-27/claims.json` (sha256 ff45e9ce…62b2, frozen at a4f674b3) against
`tools/round-27/c1-rename-identity.py` (e0a07995…bb7, equal to the pin) and `tools/round-27/c2-xpin-check.py`
(d8de667f…bd3, equal to the pin), under the sizing rule in `/home/vgpnk/Projects/shokunin/.ufo/prompts/kaidoku-round-27.md`
section 6 item 9 (file sha256 600b952f…f28f), quote at line 345: "Use no universal clauses ("all", "complete",
"every", "no harm anywhere") unless the counting command enumerates the full set."

## Overall verdict

- R27-C1: **holds with one over-wide clause.** Every universal ("each of 16", "each row", "complete") is enumerated by
  the counter. The opening "At rea-agents@6.5.0" is wider than anything the counter measures. The verdict labels are
  also wider than the decision rule behind them (a tradeoff to disclose, not a counter defect).
- R27-C2: **holds with one over-wide universal.** "for each round-26 envelope" is wider than the counted set of 24
  committed files. Separately, the `tool_contract` (not the statement) promises exit 0, and the checker does not count that.
- No item needs a counter change for admission. Each needs only a disclosed narrowing, because the freeze cannot change.

## R27-C1, sentence by sentence

| # | Sentence or clause | Checked by | Verdict |
|---|---|---|---|
| 1a | "At rea-agents@6.5.0" | Partly by the counter, see F1 | **fails as worded** |
| 1b | "the committed table … has one complete row for each of 16 frozen (carrier, verb) pairs: 8 verbs on /usr/bin/jq and on /usr/bin/tinyxxd" | Counter: the CARRIERS × VERBS constants enumerate the 16 pairs, and `len(trows) != 1` is a fail (lines 222-227). Reads Git at REV only | holds |
| 2a | "Each row's verdict (content-keyed, rename-sensitive or unstable) re-derives from three committed envelopes" | Counter lines 300-314: verdict derived from the three ids and compared with the table cells | holds (re-derivation). Label meaning: see F2 |
| 2b | "base path, same-path repeat, and a byte-identical copy under another directory, file name and extension" | Counter: run path equals the frozen constants (line 238). The envelope's own path is present and the other path absent (292-295). The envelope's subject sha256 equals the carrier (284-291) | holds. "Byte-identical" rests on the sha256 that REA reports, which is a proxy [inference] |
| 3a | "A knowledge entry cites the table" | Counter `check_entry`: fixed ENTRY path, first `source:` line names `corpus/evidence/round-27/c1/table.tsv` | holds |
| 3b | "and a SOURCES row new since the base, opened 2026-10-22, status mined, listed in corpus/lessons/round-27.md ## Gate" | Counter: S### on the source line, absent at base, `row[7]=="mined"`, `row[8]=="2026-10-22"`, id is a table row in `## Gate`. Column order checked against the header at a4f674b3 (`id|source|kind|tier|scope|anchor|teaches|status|opened|recheck|used-by`): index 7 is status, 8 is opened | holds narrowly. "opened" is the cell value. No stated reviewer item checks that the source was actually opened, or the Gate URL, quote or sha256 |

**F1 — the version pin is not measured (observation, with an inference).**
- The counted argv is the verb template only (counter lines 61-70 and 240). The `npx -y rea-agents@6.5.0` prefix is never recorded.
- Envelopes carry no version field. Command (2026-10-22T14:56:41Z, exit 0): a per-envelope scan of the 24 round-26
  envelopes printed `meta_keys=command,duration ver_fields=` for every file.
- The `pkg_version` and `pkg_json_sha256` cells are read from a fixed path inside the 6.5.0 install, per `invocation`.
  That path holds 6.5.0 whatever package actually ran, so the cells are constants, not measurements.
- That leaves the 6.5.0 rule fit as the only discriminator. It cannot tell the pins apart when `relationship_coverage`
  is set. `diff` of the two `dist/domain/evidence.js` files (14:55:47Z, exit 1) shows the only projection change:
  `< ...(evidence.relationship_coverage === null ? {} : {...})` against `> relationship_coverage: evidence.relationship_coverage,`.
  `canonicalDigest.js` is identical in both pins (`diff -q`, 14:56:11Z, exit 0).
- Counterexample: `python3 -I -B rule-overlap.py` (14:58:07Z, exit 0) printed `function-base.json stored_fits_65=True
  rules_coincide=True` (likewise for `-copy` and `-repeat`), then `rules_coincide=3/24`.
- So for the `function` rows, a 6.7.0-produced envelope passes every C1 gate [inference: assumes the round-27 `function`
  envelopes also carry coverage, as round 26's did. No 6.7.0 run was made].
- Impacted axes: depth (claim provenance).

**F2 — the labels are wider than the rule (tradeoff; inference from code).**
- "content-keyed" is decided as `renamed == base == repeat`. That shows the id is path-invariant under this one rename.
  No run varies content, and the counter never compares jq ids with tinyxxd ids.
- "rename-sensitive" rests on a single equal repeat, so run-to-run variance hitting only the renamed run is not excluded.
- The labels are lane terms from round 26 (`tools/round-26/c1-id-identity.py:150`). `limits` already says the verdict
  values are not claimed. Disclose the meaning; do not change the counter.

Note (observation): "native reader verbs" in the `kind` field is lane-defined as these eight since round 26 (for
example `corpus/knowledge/2026-10-22-r26-native-reader-evidence-id-identity.md:7`). It is not an REA category. The 6.5.0
`dist/cliCommandNames.js` (sha256 41963156…5dd3) also lists `inspect-native-instruction`, `inspect-native-load-image`,
`search-bytes` and `address-to-file-offset`. The statement itself says "8 verbs", so it is not over-wide.

## R27-C2, clause by clause

| # | Clause | Checked by | Verdict |
|---|---|---|---|
| a | "tools/round-27/xpin-attribute.mjs, committed at REV" | Checker: `show(REV, TOOL_PATH)`, run with node from a temporary copy | holds |
| b | "prints for each round-26 envelope" | Checker: `ls-tree` of `corpus/evidence/round-26/c1/envelopes/`, with exactly 24 required | **fails as worded**, see F3 |
| c | "the stored id, the id under the 6.5.0 rule, the id under the 6.7.0 rule and the attribution" | Checker compares all four cells with its own recompute (lines 141-150). Its 6.7.0 model matches the 6.7.0 projection diff (see F1). The key-absent case is untested: all 24 envelopes carry the key (21 null, 3 set) | holds for the 27 counted cases |
| d | "agreeing with the checker's independent recompute on 24 of 24 … and on 3 of 3 generated red envelopes" | Checker counts A and B | holds. Tool exit status is not counted, see F4 |
| e | "SCORECARD ## Capabilities has a row naming the tool" | Checker: any pipe-led, non-separator line in the section that contains the path | holds. A header line would also match [inference, line 199] |
| f | "SOURCES has a row new since the base, opened 2026-10-22, status mined, naming the installed 6.7.0 package root a1722018f28f9df2, listed in the round-27 ## Gate" | Checker: the hash fragment appears in the source cell, plus status, opened and the Gate table row | holds |
| — | "own exported digestCanonicalValue … not a retyped projection" (`tool_contract`) | The stated reviewer item in `limits` | reviewer-only, already disclosed |

**F3 — "each round-26 envelope" is wider than the counted set (observation).**
- Command (14:57:45Z, exit 0): `rg -l --glob '*.json' … '"evidence_id": ?"ev_' /fast/scratch/hyaku/kaidoku-r26` found
  uncommitted round-26 REA envelopes outside the counted set, for example 9 in `seats/ReplayA/envelopes`, 11 in
  `seats/ReplayB/envelopes`, 10 in `seats/C1Sizing/raw`, and 1 in `l1`.
- In the lane, `corpus/evidence/round-26` holds 30 `.json` files: the 24 envelopes plus 6 counter receipts
  (`after/c2-at-46ebfd2f.json` begins `"instrument": "tools/round-26/c2-calibration.py"`).
- Impacted axis: operability (claim width only, not capability).

**F4 — the tool's exit code is not counted (observation, demonstrated).**
- Command (14:58:08Z, exit 1): `python3 -I -B c2-xpin-check.py --root <lane> --rev a4f674b3 --tool-cmd "python3 -I -B exit1-tool.py"`,
  where the stub prints correct rows and then exits 1. Output: `FAIL tool exit 1:` and
  `r26_rows_ok=24/24 red_ok=3/3 capability_row=0 source_row=0`.
- The checker exits 1 here only because the capability and source rows are absent at a4f674b3.
- At a REV where those rows exist it would return 0 [inference from line 273]. The `tool_contract` "exit 0" is
  therefore checked by nothing. The statement does not promise exit 0.

Sizing bullet 1 (tradeoff, inference): C2 re-derives over committed bytes plus two host npx installs. The checker fails
closed (exit 2) if their `package.json` or `evidence.js` change, but it does not pin `canonicalDigest.js`. A change there
would surface as a miss, not a false pass.

## Narrowest disclosed wording (cannot change the freeze; disclose in the lesson and SCORECARD row)

1. R27-C1, replace "At rea-agents@6.5.0," with: "With runs attributed to rea-agents@6.5.0 by the seat's command line
   (not recorded in the counted argv) and every id fitting the 6.5.0 minting rule — which excludes the 6.7.0 rule only
   for envelopes whose relationship_coverage is null; the `function` rows are not pin-discriminated —".
2. R27-C1, after the verdict list, add: "(labels as decided by the counter: content-keyed = renamed id equals base and
   repeat ids under this one combined rename; no content-varying control)".
3. R27-C2, replace "for each round-26 envelope" with "for each of the 24 committed envelopes under
   corpus/evidence/round-26/c1/envelopes/".
4. R27-C2 `tool_contract`, disclose: "exit 0 is a contract term the checker reports but does not count".
5. R27-C1 sentence 3, disclose: "opened 2026-10-22 means the row's opened cell. The act of opening and the Gate
   URL, quote and sha256 are wave-2 reviewer duties, not counter checks".

## Artifacts (all under /fast/scratch/hyaku/kaidoku-r27/seats/CriticClaimWidth/)

| file | sha256 |
|---|---|
| exit1-tool.py | 27a1023ef76b98eb885b76c41428811599b679b9153fff178b04fbdff7cc0b16 |
| rule-overlap.py | 45d736f1a178a400b2b7667752de204f625041fbaf3ecde0096f0d06518de3bc |
| rule-overlap.out | c212bb8ebc65397f890bdde9b1280f6e257e1823f63beb4f5562cd7bdcbf9cdf |
| exit1-checker.out | ca56e00a783265abc559f069b5922780bc18da8f7cb2d02e65afe1d35d408d7c |
| recompute-ids.py (copy of tools/round-26 at a4f674b3) | 89afa3756a9b101c8ef6c5274f7ed68dc3533a306812906780949941fd60208b |
| c2-xpin-check.py (copy at a4f674b3) | d8de667ff82a46d5c0c9a19d4fc2f5a3c36c12fa037f9a32287046a377209bd3 |

No REA calls, no lane writes other than this report, no tool installs, no sources opened beyond local files.
