# C1Sizing: R26-C1 statement versus its counting rules

Seat KaidokuR26.C1Sizing (critic), 2026-10-22, lane HEAD c27f445e70cedbaf5300b2fd0a53e821d9b659a9.
Attacked: the R26-C1 `statement` against `rules` in .ufo/waves/round-26/claims.json.
Verdict: **fails**. The statement is wider than its counter on six clauses: the pin, the base path, the same-path repeat, the alternate path, verb identity and a new SOURCES row. In four of the false accepts below the frozen rules accept a forged table. In one of them (FA2) the forgery changes a verdict.
Labels: (obs) means observation, (inf) means inference, (unk) means unknown. The skill file `skill://godspeed` could not be found on this host, so this seat ran without it. Tools installed: none.

## Evidence runs (all in seat scratch, REA 6.5.0 CLI, one after another, every exit 0)
Each run used `TMPDIR=/fast/scratch/hyaku/kaidoku-r26/seats/C1Sizing/tmp npx -y rea-agents@6.5.0 <argv from verbs_argv>`. Base runs were on /usr/bin/jq. The two copy runs were on /fast/scratch/hyaku/kaidoku-r26/carrier/alt/jq. UTC 12:14:01Z to 12:15:36Z.
| envelope | evidence_id (first 12 hex) | .meta.command | .data.operation | parameters |
|---|---|---|---|---|
| read-bytes-base | ev_99b0c6e1f03c | read-bytes | (not read) | address 0x103fa0, length 64 |
| read-bytes-copy | ev_99b0c6e1f03c | read-bytes | (not read) | same |
| function-base | ev_b2b7e9e4313e | function | (not read) | procedure 0x103fa0 |
| inspect-binary-layout-repeat (/usr/bin/jq) | ev_294a449cecf2 | inspect-binary-layout | inspect_binary_layout | path /usr/bin/jq |
| inspect-binary-layout-copy | ev_52da4b3df646 | inspect-binary-layout | inspect_binary_layout | path .../alt/jq |
| analyze-base | ev_14f9d92f41c6 | analyze | binary_overview | {} |
| inspect-base | ev_14f9d92f41c6 | inspect | binary_overview | {} |
| decompile-base | ev_03d786185306 | decompile | procedure_pseudo_code | procedure 0x103fa0 |
| xrefs-base | ev_d591ef8c4f9a | xrefs | xrefs | address 0x103fa0 |
| instructions-base | ev_b20a0f25f149 | instructions | read_function_instructions | procedure 0x103fa0 |
All 10 envelopes have `ok` true and `.data.subject.digest.sha256` = e8156675...7806 (obs).
- `jq -c .meta` on the L1 probe prints `{"command":"inspect-binary-layout","duration":"192ms"}`. The probe has 0 matches for `6.5.0|rea-agents`. No envelope field names the package version (obs).
- REA 6.5.0 `dist/domain/evidence.js:182` defines `computeEvidenceId = ... ev_${digestCanonicalValue(semanticProjection(evidence), "Evidence")}`. The projection at lines 156-180 includes `parameters` and `normalized_result` and leaves out `subject.local_path` (obs).
- `python3 -I -B recompute-id.py <envelope>` matched every one of the 11 envelopes (the 10 above plus the L1 probe) under the 6.5.0 projection. For example, on the probe it printed `6.5.0 ev_294a449c...71bd match` (obs, 12:13:51Z). Under the 6.7.0 projection 10 of the 11 printed `differs`. function-base printed `match` under both projections, because its `relationship_coverage` is not null (obs).
- `diff <(jq -S 'del(.meta)' analyze-base.json) <(jq -S 'del(.meta)' inspect-base.json)` printed `data identical`. The same comparison of the inspect-binary-layout repeat against the L1 probe printed `ibl repeat data identical to L1 probe`. In both pairs the bytes differ only in `.meta` (obs).
- `git show HEAD:corpus/SOURCES.md`, parsed by header name: rows S074, S075, S076, S077 and S078 have `opened` 2026-10-22 and status `mined` at c27f445e (obs). corpus/lessons/round-26.md and the C1 entry are absent at HEAD (obs).

## Clause-to-rule table
| # | statement clause | rule that checks it | status |
|---|---|---|---|
| S1 | At rea-agents@6.5.0 | none. `invocation` is prose, and no envelope carries a version | unchecked |
| S2 | on /usr/bin/jq (the run path) | only `diagnostics_not_gating` | unchecked |
| S3 | 30,800 B, sha256 e8156675... | row_complete compares the subject sha with the carrier sha. The size follows from the sha (inf) | checked |
| S4 | committed table corpus/evidence/round-26/c1/table.tsv | inputs (Git objects at REV) | checked |
| S5 | one row for each of the 8 frozen verbs | row_complete checks only that the verb is one of the 8. Nothing checks uniqueness or coverage, and rows_total is undefined | partial |
| S6 | each row's verdict re-derives | derived_verdict, plus row_complete's equality of table verdict and derived verdict | checked |
| S7 | from three committed envelopes | inputs, plus row_complete's exist, parse and ok checks | checked, but the three need not be distinct runs |
| S8, S9 | base, same-path repeat | the file name only. Nothing checks the path or that the runs are distinct | unchecked |
| S10 | byte-identical copy | the subject sha equals the carrier sha | checked |
| S11 | at the alternate path | only `diagnostics_not_gating` | unchecked |
| S12 | (implied) the envelope comes from that verb with its frozen argv | none. `.meta.command`, `.data.operation` and `.data.parameters` are not read | unchecked |
| S13 | (implied) the ids are genuine REA ids | only the prefix `ev_`. The id is never recomputed | weak |
| S14 | A knowledge entry | entry_ok, at one fixed path (narrower than the statement) | checked, narrower |
| S15 | cites the table | entry_ok: the `source:` line names the table path | checked (substring) |
| S16 | a SOURCES row opened 2026-10-22 | entry_ok: the `opened` cell. Nothing checks that the row is new, its status, its used-by cell or its quote | partial |
| S17 | id appears in round-26.md under ## Gate | entry_ok: the id appears. The section bounds and heading match are not defined | partial |

## False accepts (the rules allow these; each has a concrete counterexample)
- FA1, wrong pin (S1). Commit 24 envelopes produced by `npx -y rea-agents@6.7.0` with the same argv. Every row_complete condition reads fields that 6.7.0 also emits (inf, because 6.7.0 was not run). Nothing in the rules can tell 6.7.0 from 6.5.0. A recompute under the 6.5.0 projection catches it for verbs whose `relationship_coverage` is null, but not for function (obs, from the projection test above).
- FA2, copy made by duplicating base (S11, verdict-changing). The genuine alternate-path inspect-binary-layout run has id ev_52da... and base has ev_294a..., so the true verdict is path-sensitive (obs). Commit the base bytes as inspect-binary-layout-copy.json and set copy_id to ev_294a.... Every rule passes and the row reads content-keyed (inf, rule walk). For read-bytes, a duplicated copy is indistinguishable by id, because the genuine copy id is equal too (obs). Only `.data.subject.local_path` differs, and it does not gate.
- FA3, one run copied three times, the "table copied from one run" case (S8, S9). Commit one envelope as base, repeat and copy for every verb. The `unstable` verdict can then never appear, and every verb reads content-keyed. A genuine repeat differs from base only in `.meta.duration` (obs, the repeat versus the L1 probe).
- FA4, swapped verb or drifted argv (S12). analyze and inspect envelopes have identical `.data` (obs). The inspect row passes when built from analyze's envelopes. An inspect-binary-layout envelope saved as analyze-base.json also passes, because the operation is not read. So does read-bytes run with `--length 16` or with an address other than 0x103fa0.
- FA5, forged id (S13). Change one evidence_id to `ev_x` in both the envelope and the table cell. The rules accept it and the verdict changes. The 6.5.0 recompute rejects it (obs: 11 of 11 genuine envelopes match, so the check is feasible).
- FA6, duplicate rows (S5). A table with 8 read-bytes rows, all pointing at the read-bytes envelopes, gives 8 complete rows, because nothing requires the 8 verbs to be distinct.
- FA7, reuse of the pre-freeze probe. claims.json says the probe is "never used as a table row", but no rule rejects an envelope with sha256 689680863a6e3dbd8c5a442aee52042a4601fd37e0555aa6db66d3a8ab3b195a.
- FA8, an old SOURCES row (S16). Write an entry whose `source:` line is `corpus/evidence/round-26/c1/table.tsv; S075`, and a round-26.md `## Gate` line that names S075. entry_ok is then 1 with no new row, because S075 is already opened 2026-10-22 at base (obs). This contradicts `causal_separation`, which says C1 "lands ... a SOURCES row".
- FA9, a Gate mention without substance (S16, S17). A line under `## Gate` such as `- S079 not yet opened`, with no quote and no sha, passes. Status is not read either: a row with status `rejected` but an opened date of 2026-10-22 passes, and 2 `rejected` rows already exist at base (obs).
- FA10, substring matching. A `source:` line naming `corpus/evidence/round-26/c1/table.tsv.old` passes a plain substring check. So does S0790 when S079 is the id sought (inf, depending on how the instrument matches).
- Holds: an envelope from a different carrier fails the subject-sha equality. A forged sha passes the rules but fails the recompute, because `subject.digest` is part of the projection (obs, code).

## False rejects
- FR1 was tested and holds. The suspicion was that address 0x103fa0 lies outside a 30,800 B file's link range. In fact all 8 verbs returned `ok` true with the carrier sha, and decompile names `FUN_00103fa0` (obs). Ghidra uses its rebased address.
- FR2, an eager fallback crash. `normalized_result` is a string for decompile and an array for xrefs (obs). A counter that evaluates `.data.normalized_result.artifact.sha256` before checking whether the field is present raises an error and exits 2. The "first present" rule needs short-circuit evaluation (inf).
- FR3, a no-id row. Comparing an id cell with an absent `.data.evidence_id` is undefined, so an honest no-id row is rejected or crashes the counter. This was not observed at 6.5.0: all 11 envelopes carry ids (obs).
- FR4, both `<verb>-<run>.json` and `.json.gz` present. The rules do not say which one wins.
- FR5, a correct entry at a different file name gives entry_ok 0, although the statement says "a knowledge entry". Likewise a `## Gate` heading written as `## Gate (round 26)`, or an `opened` cell written as `2026-10-22 UTC`, is rejected under exact matching.
- FR6, table formatting. CRLF line endings, an extra notes column, or verdicts in a different case are rejected, or parsed differently, depending on the parser.

## Smallest safe correction
The frozen rules must not be re-defined. Two corrections fit inside them.
- The instrument: count each frozen verb at most once, short-circuit the subject-sha fallback, define the `## Gate` section bounds, read SOURCES columns by header name, and fail when both .json and .gz exist. Each of these resolves an ambiguity in the rules without adding a gate.
- The judge: treat S1, S2, S8, S9, S11, S12 and the newness part of S16 as **not measured** by the counter. They count only if the falsify wave's direct checks below pass. Otherwise the admitted statement must be narrowed to "verdicts re-derive from three committed envelopes whose subject sha equals the carrier". This is a tradeoff the judge must reject if it is left unaddressed, not a defect that wording can fix.

## Checks the falsify wave must run directly
1. Recompute every committed envelope's evidence_id under the 6.5.0 projection with recompute-id.py (sha below). Expect 24 of 24 to match.
2. Per envelope, `.meta.command` must equal the verb, and `.data.parameters` must match verbs_argv: procedure or address 0x103fa0, length 64, and the run path for inspect-binary-layout.
3. Per envelope, `.data.subject.local_path` must be /usr/bin/jq for base and repeat, and /fast/scratch/hyaku/kaidoku-r26/carrier/alt/jq for copy (24 checks).
4. Per verb, the base, repeat and copy files must be byte-distinct. No envelope may hash to the probe sha 6896...195a. analyze and inspect should share `.data`; treat them as one observation in the entry.
5. The table must have exactly 8 data rows, its verb set must equal the frozen 8, and its header must match exactly.
6. Producing records for all 24 runs: argv, UTC, exit and TMPDIR, plus the package version resolved by `npx -y rea-agents@6.5.0`.
7. An independent replay of at least inspect-binary-layout and read-bytes across base, repeat and copy at 6.5.0. This seat observed inspect-binary-layout as path-sensitive and read-bytes as content-keyed (obs, this seat's scratch runs only, not table rows).
8. The cited S### must be absent from SOURCES.md at c27f445e (S001 to S078), have status `mined` and a used-by cell naming the entry. Its Gate line must carry a located quote of at most 25 words and a sha256. The entry body's verdicts must agree with table.tsv.
9. A mutation run: feed the committed counter FA2, FA3, FA4, FA6 and FA8, and record that it accepts them. That acceptance is the disclosed limitation of the frozen rules, not a pass.

## Artifacts (/fast/scratch/hyaku/kaidoku-r26/seats/C1Sizing/)
- recompute-id.py 2e5b630c63ef4c13d2585153ed95ffcf755c79d8189c6d12cb9149d2b8dca8ae
- raw/analyze-base.json 5e87b736f62fffeef512ecc4ba2b12719a81f0a2a2a99ffa681c317f50d0feeb
- raw/inspect-base.json 3c0c3529cf076f8d5e55f3e5ee8e603c217faa831e4f8892552b75c3ba21f452
- raw/decompile-base.json 40bfe9e9d876d81221d24a400f22a93a9f3b0cb9abb6447726bd1371a5f4bb63
- raw/xrefs-base.json 56465a0c61386ba2b2a4dc051273042807c8c438cec447c7c86d889dc00cf595
- raw/instructions-base.json 6fd5dcc3b1a2be8d344b2ac5f328383c3a6987d19113d7ce2511314a88e057cc
- raw/function-base.json 529c4b48288580a53ed3881dfc40e20f1ae62b35223a18922675c8ffa5f8ca1c
- raw/read-bytes-base.json dbafc3638d31483efe811c205a77cd6e0f08e629a270de805ca34bcb2fa13976
- raw/read-bytes-copy.json 2c7800b34d6c4bea05be59f7406628ba59211b8bf3dc3aa9cb22e31212a14e39
- raw/inspect-binary-layout-repeat.json 19c5b5044c86bcbba7b440139c009a0c4f7b1dbd330852f6fb320e991d7995ef
- raw/inspect-binary-layout-copy.json 354cabfb07d719a5ee522ba7e6c5f5ff5fcc509359a5e51b814ea755968e6a32
- The raw/*.err stderr files sit next to each envelope. Sources opened: local files only (REA 6.5.0 and 6.7.0 `dist/domain/evidence.js`, sha256 f992d93e...dcff and a3fb9f02...c0fb, plus 6.5.0 `canonicalDigest.js`), accessed 2026-10-22.
