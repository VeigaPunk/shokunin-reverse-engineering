# R51 wave-1 docs-binding review

Axes: evidence honesty; binding-constant identity; source-reference existence; coverage arithmetic. Recommendation only, not admission.

## Findings by severity

No actionable defect found in the reviewed fallback surface. This is NOT clearance of the unavailable drafts.

1. **Measurement overstatement: none in the landing-bindings fallback.** `plans/round-51-claims.md:47-58,84-102` describes a future claim, a post-freeze L1-only run, and bindings required at the landing REV. Its `carriers_matched == 4` is a target, not a measured result. Lines 59-61 explicitly identify the already-committed round-50 measurement instead. Do not convert the prospective language into an observed-success statement before fresh receipts exist. A future draft's measured-result cells must remain explicitly pending/placeholder-marked until L1 has those receipts.
2. **Constants: no internal mismatch in the fallback.** `plans/round-51-claims.md:90-99` consistently requires entry stem `2026-10-30-r51-avm-le-squashfs-core`, heading `## Round-51 additions to Core`, frontier marker `Round-51 frontier note`, opened date `2026-10-30`, and provenance base `/fast/scratch/hyaku/kaidoku-r51`. These are requirements, not evidence that the target files/sections already exist. Actual draft spellings could not be inspected.
3. **Source citations: no phantom existing row asserted by the fallback.** Existing `corpus/SOURCES.md:159-162` contains S243/S244/S245/S249. Claims lines 94-99 and 187-191 require additional round-51 source rows and `used-by` bindings prospectively, without assigning nonexistent row IDs or claiming the rows have already landed. No claim is made here that the new rows have been opened or their source contents verified.
4. **Coverage arithmetic: baseline confirmed; landing result unmeasured.** At assigned base `f04b51ddb8d5fedb234a5e40a2c38b016f07a4ab`, 140 knowledge Markdown files intersect all 140 coverage-map stems; missing `[]`, dangling `[]`. One distinct new knowledge file plus its map row yields 141/141 arithmetically. This is conditional, not a landing measurement. Claims lines 98-99 put 141/141 at the landing REV. Existing `SCORECARD.md:23` reports 140/140; `corpus/README.md:9` says a row is written when its file exists. A 141/141 head must not be reported as measured merely because this one-file increment is planned.

## Exact count command and receipt

Executed (both exit 0):

```sh
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin ls-tree -r --name-only f04b51ddb8d5fedb234a5e40a2c38b016f07a4ab corpus/knowledge
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show f04b51ddb8d5fedb234a5e40a2c38b016f07a4ab:corpus/README.md
```

Count the first command's paths ending `.md`, using their stems as a set. From the second command select the section between `## Coverage map\n` and the next `\n## `, then collect distinct `2026-10-\d{2}-[a-z0-9-]+` tokens. Count intersection and both set differences. This follows the coverage-map extraction in `SCORECARD.md:100-102`, rather than treating token occurrence count as semantic coverage proof. Machine receipt: `count-receipt.json` beside this report, with exact argv, exit codes, UTC timestamp and both stdout SHA-256 digests.

## Review scope and residual risk

All four assigned draft directories were absent when directly opened: `.ufo/waves/round-51/w1/ScribeEntryC1/`, `ScribeProvince/`, `ScribeReadme/`, `ScribeScorecard/`. For EACH, reviewed `plans/round-51-claims.md:90-99` instead, as the assignment permits; did not substitute another seat's directory. No actual draft diff was available. Thus draft-level overstatement, wrong spellings and source-ID references remain unassessed, not passed. No future/landing count or fresh extraction was run.

The `xd://lsp` discovery request returned `No such tool`; language-server status/references/definition/diagnostics were unavailable. Text reads/searches were the literal fallback, not semantic caller proof. This Markdown-only binding scope has no runtime/rerouting/resume-continuity behavior to inspect. No REA, downloads, fixture execution, package installs, lane mutations or git mutations occurred.
