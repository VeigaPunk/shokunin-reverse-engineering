# VB1 — item-1 verifier: r4-16 L197 staleness (independent, primary sources)

## CLAIM
Round item 1: `2026-10-13-r4-16-frontier-rescan.md` `:751-752` carries a stale
two-site variance account for L197 `extract-firmware`, superseded by r12-01's
append-only errata; the fix is an append-only pointer to that errata. Verified
independently of all lane-A seats.

## METHOD
Read-only at HEAD `a280e07133f52f719b0805fc73c0b997e77b5062` (both corpus files
`git diff --exit-code HEAD` clean). Primary sources: rea-agents@6.4.0 in local
npx cache `~/.npm/_npx/dea9475797100b20` (version confirmed by package.json);
unblob 26.6.4 site-packages under `~/.local/share/uv/tools/unblob`. Receipt
existence checked (`/tmp/r12-01/`, `/tmp/r4u*`): absent. `corpus/`, `evidence/`,
`.ufo/reports/` searched for surviving envelopes: none. No probes, no network,
no writes beyond this receipt.

## FINDINGS
1. Locus exact: `:751-752` = "re-carve is identical to the held `ev_82507d8e…`
   run modulo caller output dir (`files[].path`) + per-run
   `chunks[].provider_id`" — two sites named.
2. Staleness confirmed at source. The published `extract_firmware` result has
   FOUR run-parameterized sites: `files[].path` (`FirmwarePublication.js:46` =
   `join(tree.outputRoot, …)`), `output_directory` (`:59`),
   `chunks[].provider_id` (`FirmwareReports.js:157`; schema
   `firmwareAnalysis.js:71-73`), `derivations[].provider_blob_id`
   (`FirmwareReports.js:198`; schema `firmwareAnalysis.js:117-123`). Mechanism:
   unblob ids are `pid:counter` (`identifiers.py:8-17`; `models.py:112,119`),
   never content-stable. `derivations[].provider_blob_id` is named nowhere in
   `:750-754`, so the stated method cannot reproduce its own "identical" claim.
3. Pointer target exists, committed at HEAD:
   `2026-10-14-r12-01-queue-b-ready.md:99-104` (four sites; "not 'exactly two
   values'") and `:110-120` (supersession + source pins). All five cited pins
   spot-checked line-by-line; all match.
4. r4-16 has no pointer yet: grep `output_directory|provider_blob_id|four
   sites` → 0 hits; last section is r14-01 (`:875`). The locus sits inside an
   existing errata block (r12-01's, `:728-796`) — the pointer must append at
   EOF, not in place.
5. `/tmp` receipts gone and no envelope survives in-repo: the "7 values"
   numeral stays attributed, not re-derived.

## THREATS
"Caller output dir" could charitably cover `output_directory`; but
`derivations[].provider_blob_id` is unaccounted either way, so staleness holds
at ≥1 unnamed site (2 under the strict enumeration). "7 values" untestable
(receipts gone). No REA verb re-run (no live probes) — verification is
source/record-level, not envelope-level. Tracked-file byte-identity checks
support, but do not substitute for, the lane's Command A invariant.

## VERDICT
CLEAN — staleness independently confirmed (two named sites vs four at source);
r12-01 `:97-120` is the correct pointer target; append at EOF.
