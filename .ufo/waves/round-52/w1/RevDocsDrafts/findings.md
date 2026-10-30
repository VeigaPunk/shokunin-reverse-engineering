# RevDocsDrafts — scoped docs-binding review

Recommendation: no actionable defect found in the reviewed landing-binding specification; actual scribe drafts were unavailable. This is not admission of the future documents or measurements.

Axes: evidence honesty; constant consistency; source existence/provenance; coverage arithmetic.

## Numbered findings (severity order)

1. **No concrete overstatement in the fallback binding.** `plans/round-52-claims.md:162-174` describes requirements at the future landing REV, not an already-observed round-52 result. Its 142/142 and fresh receipt references are prospective acceptance conditions. They need not be placeholder-marked inside this claim declaration. Any drafted landing prose asserting measured success must remain explicitly pending until the L1 receipts exist.
2. **No constant mismatch in the fallback specification.** `plans/round-52-claims.md:163-169` consistently names entry stem `2026-10-30-r52-avm-le-squashfs-core`, heading `## Round-52 additions to Core`, and marker `Round-52 frontier note`. Actual document constants were not checked because the assigned drafts did not exist when inspected.
3. **No phantom-source presentation in the fallback specification.** The live SOURCES rows include S250/S251 (`corpus/SOURCES.md:163-164`); the inspected registry has no S252. The claim explicitly calls S252 “opened this round” (`plans/round-52-claims.md:54,264-268`) and requires the new row and used-by binding at landing (`:166-171`). Therefore S252 is an in-round obligation, not evidence that the row already exists. Do not convert this to a historical/existing source claim when integrating.
4. **141 → 142 arithmetic is supported only as a conditional projection.** The immutable claims-draft revision has 141 knowledge Markdown files, all 141 mapped, missing `[]`, dangling `[]`; the proposed r52 entry does not already exist. Adding exactly that one file and its map token yields 142/142. This does not measure a future landing revision. Exact commands, exit codes, UTC timestamps, stdout hashes and raw stdout are in `count-receipt.json`.

## Review coverage and gaps

All five requested paths were absent on direct directory reads: `ScribeEntryC1/`, `ScribeProvince/`, `ScribeReadme/`, `ScribeScorecard/`, `ScribeBlock27/` under `.ufo/waves/round-52/w1/`. As explicitly permitted by the assignment, reviewed claims landing bindings instead (`plans/round-52-claims.md:162-174`), plus C2 and source obligations (`:197-234,264-268`). No actual draft diff was reviewed. Drafts appearing later are outside this snapshot and need integration review before use.

LSP device unavailable: `read xd://lsp` returned “No such tool”; no status/references/definition/diagnostics calls were possible. Literal text inspection is not semantic-callsite proof. Runtime identity, resume continuity, saturation admission and canonical-run behavior are not affected by this documentation-only fallback review and were not exercised.

## Count command

The performed commands were:

```text
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin ls-tree -r --name-only ab0eafedc41402b43b41a4362084119578dfe7ce -- corpus/knowledge
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show ab0eafedc41402b43b41a4362084119578dfe7ce:corpus/README.md
```

Both exited 0. Count derivation matches `SCORECARD.md:98-102`: form the set of `.md` path stems; extract the `## Coverage map` section up to the next level-two heading; collect regex `2026-10-\d{2}-[a-z0-9-]+`; calculate file count, intersection size and both set differences. Result: knowledge_files=141, mapped=141, missing=[], dangling=[].

No REA, downloads, synthetic probes, builds, tests or instrument scoring were run. No tools installed. No scratch directory was created; no cleanup was necessary. Only own report/evidence paths were written.
