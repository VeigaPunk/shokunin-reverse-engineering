## CLAIM
Convergence diff, item 7 (r12-01 L197 main-vs-erratum): substance CONVERGENT — the erratum's four-site list is source-verified, the main text is stale, no rewrite. Open interface: whether the planned knowledge append lands (D7/G7/R2/C2/VB7 find the record already correct; C4's gate presupposes a new append) and its wording if it does.

## METHOD
Primaries first, Lane A unread: HEAD text of `corpus/knowledge/2026-10-14-r12-01-queue-b-ready.md`; worktree==HEAD (`git rev-parse`==`git hash-object`==`8768ce77…`; sha256 `0a794bc1…`==SB2.md:18); `/tmp/r12-01/`, `/tmp/r4u/` absent; r12-02=328 lines. Then every item-7 seat (Lane A D7,G7,F7,V7,R3,R2,C1,C2,C5,C7,C4,P0–P2; Lane B VB7,FB,CB10) plus an independent source spot-check of VB7's claims (rea-agents@6.4.0 dist, unblob 26.6.4; no probes).

## FINDINGS
- Convergent: `:38/:40/:42` say "exactly two" (`files[].path`, `chunks[].provider_id`); `:67` repeats two sources; erratum `:99-104` — "two classes across FOUR sites (… — 7 values)". I re-verified at source: `dist/firmware/FirmwarePublication.js:46,59` (`path=join(tree.outputRoot,…)`; `output_directory=tree.outputRoot`), `FirmwareReports.js:157,198` (`provider_id=parsed.id`; `provider_blob_id=child.blob_id`), unblob `identifiers.py:17` (`pid:counter`) → erratum right, main stale; `LOG.md:353-354` already records the four-site law. "7 values" numeral not re-derivable (envelopes gone) — do not assert as measured.
- Disposition split: D7/G7/R2/C2/C1 "no new append"; P0:16/P1:21 slot "Pending"; P2:14/C5:11/R3:10/F7:11/FB:18 want a reconciliation append; V7:10's weakening erratum ("at least… unverified") — reject, sites are now source-supported.
- Discard: V7:5's r12-02 `:750-754` (out of range; `sed -n` → 0 lines). C7:12 cites R7.md:8-10 in its r12-01 line — R7 is the firmware seat (readelf sizes, no item-7 content). P0:16/C5:11 say "four variance classes"; the erratum says two classes across FOUR sites.
- If appending (C4:15-19 needs heading `## Errata (round 5 freshness…` + 'supersedes main text','FOUR sites','7 values'): quote the erratum, attribute the numeral, name stale loci `:38/:40/:42/:67`, EOF-append only (rule 8 cites `:105-108`=EOF, CB3:9). If not, drop C4's r12-01 clause — it self-fails.
- Lane B alignment: VB7:14 same source conclusion; CB10:8 "reading either end alone is wrong"; FB:18 "append reconciles, does not rewrite".

## THREATS
Held==lane==audit byte leg unverifiable (envelopes non-durable); the source check proves variance sites, not the runs' byte diff. Wave dir live (109 .md; siblings landed mid-audit). Read-only; no tracked file touched.

## VERDICT
FINDING: item 7 substance converged (erratum source-verified; no rewrite; do not weaken); settle append-vs-no-append and, if appending, the C4-compatible wording; discard V7's out-of-range cite and the "four classes" paraphrase.
