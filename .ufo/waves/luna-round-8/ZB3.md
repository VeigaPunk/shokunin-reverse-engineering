# ZB3 — leg-3 repair text (luna-round-8, lane B)

## CLAIM
Deliver the exact corrected stdout display block for `.ufo/waves/luna-round-8/receipts/leg-3.md` from `/tmp/kaidoku-luna-round-8-leg-3-mcp.stdout`, or a precise correction spec. Finding: the on-disk receipt already holds the exact corrected bytes (no parent edit required); the block is reproduced verbatim below, and the historical defect is reconstructed exactly as an 18-byte transcription drop.

## METHOD
Read-only; no probes. In `receipts/`: `sha256sum leg-3.md` vs `MANIFEST.txt:3` / `CA6.md:10`; `sed -n '21,22p' leg-3.md` piped to `sha256sum` and `cmp` against the `/tmp` artifact; counterfactual rebuild `sed 's/"prompts":{"listChanged":true}/"prompts":{}/' leg-3.md`, whole-file and block hashes compared to `census-pre.txt:97` and `RE1.md:9`.

## FINDINGS
- Corrected block = leg-3.md lines 21–22 + one trailing LF: 623 B, sha256 `5c68209953fb9d1444209e286ee7de0a67661ae087f222977165d30f76d5a569` = hash claimed at `leg-3.md:6`; `cmp` against `/tmp/kaidoku-luna-round-8-leg-3-mcp.stdout` (623 B, mtime 20:53) exits 0, byte-identical. Whole file: 1448 B, sha256 `1be7e4f9…` = `MANIFEST.txt:3` = `CA6.md:10` (10/10 census).
- Root cause: the transcribed id-1 line omitted `"listChanged":true`. The counterfactual yields exactly 1430 B / `d641e3d3…` (= `census-pre.txt:97` leg-3 entry) and block hash `ac7470f9…2223` (= `RE1.md:9`). Both pre-repair observations are fully explained; current bytes are the repaired state.
- Correction spec (if any consumer still holds pre-repair text): in line 21 only, replace `"prompts":{}` with `"prompts":{"listChanged":true}`; the file then hashes `1be7e4f9…`, the block `5c682099…`.
- Independent re-verification: `sed -n '21,22p' receipts/leg-3.md | sha256sum` must print the claimed value above.
- Exact corrected block below (623 B incl. final LF; display fence only; keep the single final LF — variants hash `08576144…`, `6a382eff…`, `225d67cc…`):

```text
{"result":{"protocolVersion":"2024-11-05","capabilities":{"tools":{"listChanged":true},"completions":{},"prompts":{"listChanged":true}},"serverInfo":{"name":"rea","version":"6.4.0"},"instructions":"REA provides reverse-engineering tools for local artifacts, native binaries, managed code, browser pages, and runtimes. Use the tool that directly answers the question; discover targets or inspect inventory only when needed. Tool results include inline Evidence and report their coverage and limitations."},"jsonrpc":"2.0","id":1}
{"jsonrpc":"2.0","id":2,"error":{"code":-32602,"message":"Tool inspect_go_binary not found"}}
```

## THREATS
mtime 20:59:03 predates `MANIFEST.txt` (21:02:41, repaired hash) and `census-pre.txt` (21:06:07, pre-repair hash), so mtimes cannot order the repair; census-pre self-describes as a "pre-state control census", matching pre-repair values. I verified content, not repair authorship. The 528-char id-1 line invites soft-wrap corruption in paste paths — hash the file, not a rendered copy; re-run the verification after any re-touch.

## VERDICT
CLEAN — leg-3.md already carries the byte-exact corrected stdout (block 623 B `5c682099…a569` = claimed = `/tmp` artifact via `cmp`; whole file `1be7e4f9…` = MANIFEST/CA6); defect was an 18-byte `prompts` transcription drop, already repaired; no parent edit required.
