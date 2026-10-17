## CLAIM
Hash all ten canonical leg receipts and record their file SHA-256 values in `receipts/MANIFEST.txt`.

## METHOD
Confirmed `leg-1.md` through `leg-10.md` were present with `Glob`. Ran `sha256sum .ufo/waves/luna-round-8/receipts/leg-{1..10}.md`; the ten returned basenames and digests are recorded in the manifest.

## FINDINGS
Manifest contains exactly ten canonical receipt entries. Three supplemental `leg-6-RV3-replay.md`, `leg-7-RV3-replay.md`, and `leg-8-RV3-replay.md` files were not included because the assignment specified all ten `leg-N.md` receipts.

## THREATS
These hashes identify the receipt-file bytes at audit time; they do not validate probe outcomes or embedded stdout hashes. Later changes to any receipt require regenerating its manifest entry.

## VERDICT
CLEAN
