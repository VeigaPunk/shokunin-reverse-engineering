# HB4 — token guard 2: 79-token set held

## CLAIM
Second independent guard on the command-A Coverage-map token set: at HEAD `a280e07` it is 79/79, set-equal to the knowledge-file stems, and byte-identical (same README blob and token-set digest) to round-8's work commit `18dc397`; the guard fails closed on injected drift.

## METHOD
Read-only from repo root; no probes/network/`/tmp`; only write is this file. Reimplemented G3's guard (`G3.md:7-21`) over `git show` objects: section `split('## Coverage map\n',1)[1].split('\n## ',1)[0]`, regex `2026-10-\d{2}-[a-z0-9-]+`; both literals verified identical to command A (`SCORECARD.md:101-102`). Ran the guard with baseline=landing=HEAD; recounted occurrences vs unique; recomputed `sha256('\n'.join(sorted(set))+'\n')`; compared the set to `git ls-tree HEAD -- corpus/knowledge` stems; recomputed at `18dc397`; ran three in-memory mutants; reran command A verbatim.

## FINDINGS
- Guard run: `baseline=79 landing=79 equal=True added=[] removed=[]` (would exit 0).
- Recount: 79 occurrences / 79 unique / 0 dups; set == 79 stems, missing/dangling `[]`; digest `bd70aa5f639b9d2240caa057658b702df2083344bd07bfb4e35fceebb79750c4` (64 hex).
- Held: at `18dc397` count 79, set equal, same digest; `corpus/README.md` blob `5efb202a7b0aecdf182695fb8849050044e65ac9` identical at `18dc397` and HEAD.
- Guard non-vacuous (mutants all fail): drop-one → `removed=['2026-10-13-asar-surface']`; add-fake → `added=['2026-10-16-fake-entry']`; swap-one → both lists non-empty.
- Command A at HEAD: mapped=79, knowledge_files=79, citation_resolved_rules=9, rule_blocks=9, coverage/depth=10.0, missing/dangling `[]`; `git diff --quiet HEAD --` exit 0.
- **Anchor defect:** `G3.md:24`'s published digest is 63 hex chars; `claimed == computed[:63]` is True (one-char truncation). Corroborates `TB1.md:11`; a verbatim comparison against it will always mismatch.

## THREATS
Pre-integration snapshot: no append landed, so the post-landing rerun at the integration revision is pending. The guard compares sets — a duplicated existing token (80 occurrences / 79 unique) would pass; current file is 79/79 unique. Digest recipe (sorted unique + trailing LF) is inferred from G3's wording; no-LF yields `bc971a10…`. This checks the token set, not row semantics.

## VERDICT
FINDING: 79-token set verified held and stems-equal at `a280e07` (unchanged since `18dc397`); guard non-vacuous; `G3.md:24`'s anchor digest is truncated (63 hex) — use the corrected 64-char `…750c4` for the post-landing comparison.
