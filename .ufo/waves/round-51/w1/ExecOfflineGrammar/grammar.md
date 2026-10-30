# R51 C1 offline receipt-ingestion grammar

## Evidence scope and source

Source counter: `tools/round-50/c1-counter.py`, header (receipt/subject/projection model) and `disposition_check` (three disposition families). Inspected committed `corpus/evidence/round-50/c1/<id>/run.json` for c6430, c6490, g7581, g7582; the actual normalized envelope is in each sibling `after.json` referenced by that run receipt. This distinguishes harness metadata from the payload read by the counter: v2 `--controls` must ingest the payload and each oracle table, not infer semantics from `run.json` summary fields.

## Per-carrier paths / fields to read

Input pair per ID `I`:

* `corpus/evidence/round-50/c1/I/run.json`: identity and proof of committed run; relevant top-level `id`, `carrier.sha256`, `exit`, `receipt.path`, `receipt.sha256`, `receipt.evidence_id`, `start_utc`, `end_utc`. `run.json`'s `receipt` is summary metadata, not the normalized result.
* `corpus/evidence/round-50/c1/I/after.json`: parsed evidence envelope. Subject digest is `.subject.sha256` (also `.parameters.sha256` / `.parameters.selection_sha256` where present; these agree in each inspected envelope). Handler list is `.normalized_result.chunks[].handler`. Published-file list is `.normalized_result.files[]`, each record's `relative_path`, `sha256`, `size`; v2 core disposition uses the paths, while oracle matching also needs sha256/size. Gap list is `.normalized_result.extraction_gaps[]`, fields `kind` and `relative_path` (null denotes structural bookkeeping). Removal diagnostics are `.normalized_result.diagnostics[]`, filtered by `.report.__typename__`; for `MaliciousSymlinkRemoved`, resolve path from `.report.link` (the path is not `.input_path`, which is `$input` in these committed receipts), with `.report.target` descriptive only.
* `tools/round-50/oracle/I.nonregular.tsv`: oracle non-regular entries; columns are relative path, kind, optional detail. Details matter only to `removed.silent` matching. `tools/round-50/oracle/I.tsv` supplies regular-file oracle paths/digests/sizes for publication matching, not disposition.

All four committed run receipts' `.receipt.path` is `after.json`; all four report `exit: 0`, have a carrier sha matching `.subject.sha256` in the envelope, and report `squashfs_v4_le`. IDs: c6430, c6490, g7581, g7582. Receipt manifest carrier hashes respectively `da1c804940f49fcfb3727efbd4f79a4788f86c5819ddda23b5a8221fb898b46f`, `880370e7f7e15d70b165a96ae3e6efef0cb8dc3e9a6b27b0b925c7fa62caf2d7`, `968d997d5401a483a9250ab0e4e34bd632a40bee000af3419a2b8d0e29fa6845`, `a119b64428e7128e376317472c504605f17f81a2b802439e32194431d94a5bd0`.

## Three-family disposition interpretation

Mirror the counter's `disposition_check`: (1) path-resolved gap must exactly map to one nonregular row and its kind be allowed for row kind; (2) null-path structural gap must have a structural allowance and remain within its limit; (3) named removal diagnostic must resolve under the handler extract root to exactly one nonregular row whose kind is allowed for removal, and cannot share a gapped entry. Then required rows need exactly one gap/removal unless their kind/detail is explicitly silent. This is why a failed char-device with no disposition is lawfully admissible by the producer-derived rule, rather than encoded as a device-detail exception.

## Dry-run proof

Standalone script: `disposition-dryrun.py`; stdout captured as `dryrun.stdout` in scratch. It consumes the four committed `after.json` envelopes and nonregular TSVs. R51 comparison rule is the law's semantic change from R50: char devices are not required to receive a disposition and no char-device detail whitelist is needed; other frozen clauses are retained.

Exact command:

`python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-51/w1/ExecOfflineGrammar/disposition-dryrun.py`

Exit: `0`; stdout SHA-256: `65b623e76f0e6d327f421a5607289d9fa474c8657c0fcd36b71710666888e100`; UTC: `2026-10-30T04:58:19Z`.

Results: R50 2/4 (Cable c6430/c6490 pass; FRITZ!Box g7581/g7582 fail, each exactly 12 missing char-device dispositions); law-derived R51 4/4. The per-carrier table/counts are preserved verbatim in `dryrun.stdout` in scratch at `/fast/scratch/hyaku/kaidoku-r51/w1-ExecOfflineGrammar/dryrun.stdout` (will be copied into this artifact directory before handoff). No live REA run performed.
