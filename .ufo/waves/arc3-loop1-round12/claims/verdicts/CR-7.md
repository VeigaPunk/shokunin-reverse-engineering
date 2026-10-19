# CR-7 — convergence verdict, arc3-loop1-round12

verified-at: 2026-10-19  
status: evidence reconciliation and integration recommendation; no landing receipt

This seat re-checked the live round before writing. At review time the C1/C2/C3 reports were present, including late `EX-8.md` and `PL-1.md`; `CN-2.md` and `CN-4.md` were the only verdict reports visible. Their earlier inventory statements that EX-8/PL-1 were unavailable are now stale. The frozen roster assigns CR-7 to verdicts (`claims-frozen.md:65-70`). No corpus entry, map, skill, gate, custody file, scorecard, or log was changed.

## Frozen baseline and acceptance boundary

I re-ran Command A from `SCORECARD.md:88-124` against both immutable revisions. Exact output:

```json
{"citation_resolved_rules": 16, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 90, "mapped": 90, "missing": [], "revision": "0436f4940283072db08e73c0117195847c50d31d", "rule_blocks": 16}
{"citation_resolved_rules": 16, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 90, "mapped": 90, "missing": [], "revision": "5ee13b358d0a1112d31808b9bae3d8ddd1b46875", "rule_blocks": 16}
```

These are pre-integration baselines. C1's 91/91 after-state and C2's 17-rule/17-citation after-state are **UNVERIFIABLE** until their drafts are integrated and Command A is run on the landing revision. The live citation-drift table/pin is likewise unchanged; its integration result is **UNVERIFIABLE**.

## C1 — select one Unknown

**REPRODUCED; recommend the fourth-family `inspect_go_binary` entry.** Frozen C1 permits one new Unknown and one entry/token (`claims-frozen.md:18-29`). I independently ran the cached REA 6.7.0 `inspect-go-binary <path> --format json --full-output` on `/usr/bin/docker` twice and on byte-identical copies at two `/var/tmp` paths:

- The original file and both copies had SHA-256 `70f68a7702346cf4bb1a2568091cfee92216cc8498a627a488c4b212bc5f45c9`.
- Both original-path calls returned `ev_87621921fc54a38ee60f85c9f81a47508dcdebd1c6f70569ec78da3a3a055dcd`.
- `/var/tmp/kaidoku-cr7-r12-go/same-name/docker` returned `ev_64cfe94ca1a22fe6d3a3c10e95cbcc1bfbdf97ebb2ba14ab998a0febcfb5d218`; `/var/tmp/kaidoku-cr7-r12-go/other-name/docker-copy` returned `ev_1e314730c85e5ec0d83605856ecd7ac417a70122c5cbdef176644140f2626cc8`.

The result is bounded to this operation/version/input and was independently re-derived from the returned envelopes. REA's projection is `ev_` plus SHA-256 over canonical JSON (`/home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents/dist/domain/evidence.js:159-183`; canonical digest: `/home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents/dist/domain/canonicalDigest.js:8-25,60-76`). The Go service/provider place the selected path in `parameters.path`, `normalized_result.artifact.path`, and the artifact-path location (`/home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents/dist/application/go/GoBinaryService.js:54-77`; `/home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents/dist/go/GoBinaryProvider.js:157-165`). This is a static metadata read; Docker was not executed.

The independently reproduced path-stable `analyze_function` candidate is **not selected** as a new C1 closure: its path-not-hashed behavior is already recorded in `corpus/QUALITY.md:25` and the `analyze_function` entry at `corpus/knowledge/2026-10-14-r9-02-queue-a-ops-2.md:146-169`. My fresh CR-2 rerun also confirmed that bounded case: `bash .ufo/waves/arc3-loop1-round12/claims/c1/CR-2/evidence/recheck.sh` returned the same `ev_a40a1cd1b5cd7c0600862a878a024d3cdf18eed765c0cf3573c007cfb69c3001` for `/usr/bin/jq` and two byte-identical copies; projection equality was `True`, and recursive scans returned `path_named_fields_in_semantic_projection=[]` and `absolute_paths_in_semantic_projection=[]` (`CR-2/evidence/recompute-output-path-audit.txt:1-14`). This is a reproduced remeasurement, not the clearest remaining Unknown.

Recommend one corpus draft, CR-4's `inspect_go_binary` entry (`claims/c1/CR-4.md:11-35`) and its single Evidence-model token `2026-10-19-arc3-r12-go-evidence-id-domain`; do not also land CR-2's path-stable entry or duplicate Go entries/tokens. CR-4's source-supported four-call battery is a strong durable recheck; EX-8 and the other Go reports are corroborating drafts. Different alternate-path IDs in CR-4, EX-8, CN-2, CN-4, and my calls are expected: those calls selected different path strings. Their shared byte digest and repeated original-path ID agree; do not compare alternate IDs across different path inputs. Corpus/map landing and 91/91 remain **UNVERIFIABLE**.

## C2 — rule #17 synthesis

**REPRODUCED; recommend one projection-local rule synthesizing EX-10 and EX-16.** Proposed rule text:

> Derive Evidence-ID field sensitivity at the exact operation's semantic-projection boundary, not from a field name or the `ev_` prefix. Pin the package version, call shape, and artifact bytes; recompute IDs from complete envelopes; compare a same-path repeat with a byte-identical alternate-path call; and report the exact changed projection pointers, including nested result fields. When attributing causality, mutate the candidate pointer or field set; if that change does not reproduce the alternate-call ID, diff the remaining projection and do not attribute the whole delta to the candidate. Distinguish excluded top-level display metadata from same-named nested values, and bound each conclusion to the measured operation and version.

My independent projection recomputation supports the isolation caveat: for the r7 and r10 alternate-path envelopes, `parameters.path`, `normalized_result.artifact.path`, and `locations[0].path` co-varied; no one of those fields mutated alone reproduced the alternate ID. For r11, the projection differed at `normalized_result.inspection_id` and `normalized_result.substeps[0].evidence.subject.local_path`. The nested path alone changed the hash but did not reproduce the alternate ID; `inspection_id` alone did not either, while changing both did. These are distinct measured operation results, not a universal `ev_` rule. See the underlying corpus passages r7 `:11,:17-22`, r10 `:13-15,:19-22`, and r11 `:17-20`, plus `corpus/QUALITY.md:25`.

**CORRECTED — citation range for integration:** EX-16 currently cites r11 `:19-23` (`claims/c2/EX-16.md:8`). Do not carry that range forward: r11 line 23 contains a stale/misphrased 90/90 post-integration status, while my measured baselines above are 90/90 and the proposed co-landed state is 91/91. Use r11 `:19-22` instead. The r7/r10 measured ranges above avoid their status prose as well. No `SKILL.md` edit was made; rule #17 and its 17/17 after-state remain **UNVERIFIABLE**.

## C3 — citation-drift patch and scratch test

**VERIFIED gap; REPRODUCED scratch behavior; recommend RV-4's one three-row patch set.** My live census found 57 `entries`, 5 `quoted`, table SHA-256 `1b3ab955478b5d40f428d733bc482e4037f83bceaa1a39e9046ef82ca6d42d4b`, matching the `expected.json` pin. Each of the three source files has one `recheck:` line (r7 `:5`, r10 `:7`, r11 `:7`), and no current `entries` or `quoted` row names any of those files as `file` or `target`. The unchanged strict command

```text
python3 .ufo/gates/citation-drift/citation-drift-probe.py --root . --rev 0436f4940283072db08e73c0117195847c50d31d --table .ufo/gates/citation-drift/pointer-table.json --expected .ufo/gates/citation-drift/expected.json --strict
```

returned `CITATION_DRIFT_VERDICT: clean findings=0 exit=0`; clean only means registered pointers passed, not that the unregistered rechecks were graded.

I reran `PYTHONDONTWRITEBYTECODE=1 TMPDIR=/var/tmp python3 .ufo/waves/arc3-loop1-round12/claims/c3/RV-4/seeded-measurement.py` against the real gate checker. Exact output:

```text
CONTROL: no findings; strict_exit=0
SEEDED arc3r7-evm-recheck: citation_dead entry=arc3r7-evm-recheck; strict_exit=1
SEEDED arc3r10-rust-recheck: citation_dead entry=arc3r10-rust-recheck; strict_exit=1
SEEDED arc3r11-artifact-recheck: citation_dead entry=arc3r11-artifact-recheck; strict_exit=1
SCRATCH: /var/tmp only; no Git writes; live instrument/table/expected unchanged
```

Recommend only `claims/c3/RV-4/proposed-entries.json`: its exact-line rows pin the r7 expected Evidence ID and scratch requirement, r10's command source/recomputation/read-only cue, and r11's pinned package/calls/recomputation/never-`/tmp` cues. I re-serialized the live table with those rows: 60 entries and candidate SHA-256 `b3156b0a89c8b2e67ba4ca372e3dd179dab6d5e1ef78312938b028f784374d40`. This is a **candidate** `expected.json` pin only; the live pin remains unchanged. CN-2 recommends PL-4 and CN-4 recommends RV-6; those are alternative row bytes and hashes, not compatible add-ons. For integration, use one complete row set and its matching digest (or recompute if any byte changes), then run the strict probe at the landing revision.

The citation-drift `--selftest` reports in peer drafts are not accepted as evidence under the wave's Git-read-only constraint: the implementation creates temporary repositories and runs `git init`, `git add`, and `git commit` (`.ufo/gates/citation-drift/citation-drift-probe.py:347-368`). I did not run it. The scratch overlay helper above uses only read-only `git show` and `/var/tmp`; no `/tmp` scratch or Git writes were used. Live table/expected after-state remains **UNVERIFIABLE**.

## Integration boundary

- C1: land exactly one Go corpus entry plus its Evidence-model map token; then rerun Command A and verify 91/91.
- C2: land one rule #17 with corrected, resolving citations; rerun Command A and verify 17/17.
- C3: land one complete three-row pointer-table variant plus its matching `expected.json` digest in the same change; run the strict probe at that revision.

All recommendations are bounded to the measurements stated above. No target runtime behavior, universal Evidence-ID rule, or integrated after-state is claimed.