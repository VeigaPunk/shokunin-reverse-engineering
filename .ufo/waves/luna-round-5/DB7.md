# DB7 — r12-01 L197 erratum draft (2nd opinion, from VB7.md)

## CLAIM
Round item 7 (r12-01 L197 main-vs-erratum inconsistency), adjudicated from `VB7.md` as designated source: VB7's verdict holds — erratum `corpus/knowledge/2026-10-14-r12-01-queue-b-ready.md:99-104` is correct at source level, main `:40/:42/:67` understate — and the one surface VB7 missed is the rescan's r12-01 erratum, which still carries the uncorrected count.

## METHOD
Read `VB7.md` (appeared 16:41) as designated source only; spot-checked its load-bearing claims against primaries, no full re-pass: pinned dist `~/.npm/_npx/dea9475797100b20/node_modules/rea-agents/` (package.json: "6.4.0"), unblob 26.6.4 sources (`~/.local/share/uv/tools/unblob/.../unblob/`), r12-01/rescan/LOG at HEAD cfc84c2. No Lane A reading; no REA probes, MCP, or network; no tracked-file writes. `/tmp/r12-01`, `/tmp/r4u` both absent (envelopes gone).

## FINDINGS
- Source anchors verify line-exact: `FirmwarePublication.js:46` (`join(tree.outputRoot, entry.relativePath)`), `:59` (`output_directory: tree.outputRoot`); `FirmwareReports.js:157` (`provider_id: parsed.id`), `:194/:198` (`child.blob_id` matched into the chunk-id namespace, exported as `provider_blob_id`); `FirmwareFiles.js:195-205` (`$input`/`$output/<rel>` logical paths, dir-independent); unblob `identifiers.py:8-17` (`f"{os.getpid()}:{__last_id}"` — VB7's `{counter}` is a variable paraphrase), `models.py:117-120`, `processing.py:684` (`Task(blob_id=chunk.id)`). No pointer drift found.
- Completion: the two-value account echoes at FIVE surfaces — add table `:13` and heading `:38` to VB7's `:40/:42/:67`.
- Propagation gap (absent from VB7): rescan `2026-10-13-r4-16-frontier-rescan.md:750-754` still states "modulo caller output dir (`files[].path`) + per-run `chunks[].provider_id`"; the rescan has no round-12-audit errata and never names `output_directory`/`provider_blob_id`. Optional one-line append (parent-owned, append-only): "Errata (luna-round-5): L197 — the count above understates; four sites per `2026-10-14-r12-01-queue-b-ready.md:99-104`."
- `LOG.md:354` ("four-site normalization law") re-confirmed. "7 values" unre-derivable (VB7 ≥12; mine 1+5+3+3=12 under the same assumption) — do not propagate the numeral.

## THREATS
Mechanism-only: with envelopes deleted, the held==lane byte-identity leg is unverifiable; "exactly four sites" rides on VB7's source-level variance argument (checked at the cited functions, engine env held constant), not envelope diffs. No Lane A reading (2nd-opinion posture).

## VERDICT
FINDING: VB7 verified line-exact; erratum `:99-104` stands as the correction, no r12-01 rewrite; residual staleness = rescan `:750-754` (optional one-line append); "7 values" not re-derivable, do-not-propagate.
