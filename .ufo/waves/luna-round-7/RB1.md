## CLAIM
Entries 1-2 (`l7-01 inspect_go_binary`, `l7-02 inspect_rust_binary`): every cited receipt path + hash + SC sha256 resolves at HEAD 411175e; hashes recomputed and matched.

## METHOD
Recomputed `git cat-file blob HEAD:<path> | sha256sum` and worktree `sha256sum` for all cited receipt files; compared to recorded values in `.ufo/waves/luna-round-6/receipts/census-final.txt` (`RECEIPT_SHA256 A/B 3,4`) and `receipts-B/MANIFEST.txt`; read every cited range in E1D/E1V/G1/E2D/E2V/G2 (plus Z1/Z2/K3/M1 rows); `git cat-file -e HEAD:` for SC1/SC2; `git grep` for recorded SC hashes. Read-only; no probes.

## FINDINGS
- All four cited receipts are tracked at HEAD and recompute-match records: A leg-3 `01063004…e9171f`, A leg-4 `99a1c690…ae29ff`, B leg-3 `97855851…1d8dc20`, B leg-4 `162b4831…59afbcb` (census-final.txt RECEIPT_SHA256 lines; receipts-B/MANIFEST.txt for B).
- Every cited line range lands on supporting content; max cited line ≤ file length (A leg-3 181≤222; A leg-4 43≤43; B leg-3 95≤96; B leg-4 71≤71; SC1 18≤19; SC2 15≤17). Evidence IDs (`ev_6718…596a4b`, `ev_0618…c99d3`, `ev_9ea97685…1bff2`) and artifact hashes (docker `70f68a77…f45c9`, signal `1b44ed53…d1f7`, rg `d006acfe…ecae42`) present verbatim.
- SC1.md/SC2.md exist on disk only: `git cat-file -e HEAD:.ufo/waves/luna-round-6/SC1.md` → "exists on disk, but not in 'HEAD'" (same SC2). No tracked file records their sha256 (`git grep` for `4a94d2fc`/`2005e475` → no hits). Recomputed on-disk: SC1 `4a94d2fc…2dc23`, SC2 `2005e475…767db`. G2's CC4.md is likewise untracked.
- Minor: E2D cites `SC2.md:12-15` for the "candidate" label that sits at `SC2.md:2` (G2 cites `:2` correctly).
- Minor: E1D's METHOD says E1V.md absent; E1V.md exists (already caught by Z1).

## THREATS
SC files are untracked under the wave convention, so "SC sha256 resolves at HEAD" cannot hold literally unless SC1–SC6 are landed with the entries or citations are re-anchored to tracked receipts (A leg-3.md:5 itself points to SC1). My SC hashes pin only current worktree bytes; no recorded hash exists to compare. Content checks are reads of cited ranges, not a semantic re-audit of the battery.

## VERDICT
FINDING: receipt citations for entries 1-2 verified at HEAD (paths, hashes, line ranges); SC1/SC2 citations are untracked at HEAD with no recorded sha256 — land SC1/SC2 or re-anchor before the coverage claim holds.
