## CLAIM

2nd-opinion adjudication of the L197 main-vs-erratum inconsistency in `corpus/knowledge/2026-10-14-r12-01-queue-b-ready.md`: main body (:40, echoed :42, :67) says the held-vs-lane `extract-firmware` comparison normalized "exactly two" values (`files[].path`, `chunks[].provider_id`); the append-only erratum (:99-104) says the true variance is two classes across FOUR sites, adding `output_directory` and `derivations[].provider_blob_id` ("7 values"). Which is right?

## METHOD

Drafted from primary sources only, before opening any luna-round-5 artifact: the pinned rea-agents@6.4.0 dist in the npx cache (`~/.npm/_npx/dea9475797100b20/node_modules/rea-agents/`), unblob 26.6.4 source (`~/.local/share/uv/tools/unblob/lib/python3.11/site-packages/unblob/`), and pre-round-5 corpus/LOG records. No live REA probes, no network, no repo writes. A later repo-wide grep incidentally surfaced current-wave lane fragments; the analysis above predates and does not depend on them. `/tmp/r12-01/` and `/tmp/r4u/` are empty — envelopes gone.

## FINDINGS

- `output_directory` is a real top-level `normalized_result` key set to `tree.outputRoot`, the caller-chosen dir (`dist/firmware/FirmwarePublication.js:59`); `files[].path = join(tree.outputRoot, relativePath)` (:46). Runs to `/tmp/r4u/pkg2` vs `/tmp/r12-01/pkg-out` differ in both. Main's "exactly two" omits `output_directory` — false for the full envelope.
- `chunks[].provider_id` = unblob ChunkReport.id (`dist/firmware/FirmwareReports.js:157`); unblob `Blob.id = new_id() = f"{os.getpid()}:{counter}"` (`unblob/identifiers.py`, `models.py:117-120`) — per-run, matching r12-01's own `190902:N` vs `2365564:N`.
- `derivations[].provider_blob_id = child.blob_id` (`FirmwareReports.js:198`), same id namespace as chunk ids (:179,:194; `processing.py:684` `Task(blob_id=chunk.id)`) — per-run too.
- Logical paths (`$input`/`$output/...`, `FirmwareFiles.js:195-205`) keep `chunks[].input_path`, derivation paths, `depth_limited_paths` dir-independent ⇒ the four sites are exactly the variance set for two runs sharing engine env. Erratum right; main stale.
- "7 values" plausibly = distinct values (1 dir + 3 chunk ids + 3 blob ids) but is not re-derivable without the envelopes; my occurrence arithmetic gives ≥12. Site list verified, numeral not.
- `LOG.md:354` records the audit's acceptance ("four-site normalization law for per-run ids").

## THREATS

- Envelopes gone ⇒ the held==lane==audit byte-identity leg is unverifiable; only mechanisms are verified.
- Don't propagate "7 values" as a measured count without receipts.
- :67's Findings bullet also restates the two-site version — same staleness as :40.

## VERDICT

FINDING: erratum :99-104 verified correct at source level (four sites); main :40/:42/:67 understate — append-only already corrects it, no rewrite; "7 values" numeral unverified.
