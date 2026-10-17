## CLAIM
At HEAD `f0e8cde`, with all ten lane-A receipts now present, I review XG1/XG2 (version pinning) and CE1/CE2 (census-pre): is all-leg 6.5.0 pinning evidenced, and is the census measurement sound? My checks: pinning holds; census reproduces; XG findings were snapshot-limited and are superseded by the later receipts.

## METHOD
Read XG1, XG2, CE1, CE2, legs 1–10 headers, MANIFEST.txt, census-pre.txt, result.json, SCORECARD.md:92-123. Read-only: per-leg grep for `rea-agents@` specifiers and npm config/cache mutations; extracted the census-pre heredoc to `/tmp/rb8-census/census_pre.py`, re-ran it at f0e8cde, recomputed stdout and token digests; ran canonical Recipe A with REV=f0e8cde and diffed its stdout against the census COMMAND_A line; recomputed L1 and leg-9 hashes. No repo writes; HEAD unchanged.

## FINDINGS
- Pins: all ten recorded commands carry exactly `rea-agents@6.5.0` (no other specifiers); 7 legs quote serverInfo 6.5.0. Invocation style varies (`--mcp` on L4/6/7/8, `mcp` subcommand elsewhere) under the same pin.
- No config mutation: only L2/L3 set env `npm_config_cache=/tmp/kaidoku-luna-round-6-npm-cache` + `TMPDIR=/tmp`; no npmrc, registry, or install edits.
- XG1/XG2 were accurate for their 18:16–18:19 snapshot (only leg-1 existed); legs 2–10 landed 18:19–18:28, closing the gap they flagged. I verified the pins directly in those receipts, so their findings are superseded, not contradicted.
- Census: re-running the receipt script reproduces its stdout sha256 `93d3a82cd9dc09d940b098b0b953b7a7ad5a84a31df20545444bab9b57e20373` byte-for-byte and token digest `c538284bd40fec6c039b6c2f18e7202f6390e0ca1ce92ea8a0c50e20a58651a0`; canonical Recipe A at f0e8cde yields the identical COMMAND_A JSON (72/72 mapped, 9/9 rules, 10.0/10.0). L1 stdout (`3eb8e06c…`) and leg-9 frame (`2b596b31…`) hashes recompute clean.
- Caveat: census-pre is an output-extended rewrite of Recipe A (rev via `rev-parse HEAD`, cwd pinned), so CE2's "unchanged Python recipe" wording is imprecise though output-equivalent; f0e8cde is not a result.json fixture revision (6645…/c265…), i.e. off-spec usage that CE1 explicitly scopes as pre-state.

## THREATS
Receipts arrived during inspection (leg-10 18:28; receipts-B/leg-1 18:59); later edits are outside this snapshot. Spec-pinning is not hash-pinning: registry/cache substitution within version 6.5.0 is not excluded, and L2/L3 used an isolated cache. I did not re-run npx (BB seats own re-runs).

## VERDICT
CLEAN: ten-leg 6.5.0 pinning verified with no config mutation; census-pre reproduces byte-for-byte at f0e8cde (CE2 wording caveat noted).
