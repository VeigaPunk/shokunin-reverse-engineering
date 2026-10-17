## CLAIM
Audit every available receipt file under `.ufo/waves/luna-round-6/receipts/`, create a path + SHA-256 manifest, and flag any mismatch between a receipt's recorded stdout SHA-256 and its captured stdout bytes.

## METHOD
`Glob(pattern="leg-*.md", path=".ufo/waves/luna-round-6/receipts")` returned only `leg-1.md`. `sha256sum .ufo/waves/luna-round-6/receipts/leg-1.md` returned `24bfd90fb0463c2085e455964521cc85f1cff53bec638d3893e596c2869e2e91`. Parsed the `Full stdout` block and recorded digest: `3eb8e06ca1e02f0a30b0e3eebd289494b35d4fd1466ed907b9148e03b2459b00`; recomputed digest of `b'6.5.0\n'` matched exactly. Wrote the inventory to `receipts/MANIFEST.txt`.

## FINDINGS
The sole available receipt has a matching recorded stdout hash. Manifest entry: `leg-1.md 24bfd90fb0463c2085e455964521cc85f1cff53bec638d3893e596c2869e2e91`.

## THREATS
Only L1 was present when audited; legs 2–10 remain unaudited, so the manifest is a partial snapshot and must be regenerated when their receipts arrive. The round-6 directory was initially absent at the first inventory check; later it contained `EX1.md` and `receipts/leg-1.md`.

## VERDICT
FINDING: only the L1 receipt is present; legs 2–10 are not yet auditable.
