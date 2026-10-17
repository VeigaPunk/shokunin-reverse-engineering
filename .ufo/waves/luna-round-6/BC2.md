# BC2 — receipts-B manifest + BB-claim verification (lane B)

## CLAIM
Froze `receipts-B/MANIFEST.txt` (10 receipts: path + sha256 + byte size) and verified every hash claimed in BB1–BB10 against its cited receipt's bytes. 28/29 claims resolve; one mismatch (BB8) plus a receipt-custody defect on legs 7–8.

## METHOD
- `sha256sum`/`wc -c` over `leg-1..10.md`; manifest written with repo-root-relative paths (self excluded — self-hash impossible).
- Re-hashed embedded blocks (fenced and BEGIN/END-marker, ±trailing newline; script `/tmp/rea-bc2/verify.py`) and matched them against all full 64-hex and truncated `h…h` claims in BB1–BB10; cross-checked the pre-existing name+hash manifest.
- Compared each receipt's seat line and mtime with the report citing it.

## FINDINGS
- 10/10 files hashed; the prior manifest (19:06) reproduces 10/10; the new manifest adds paths + byte sizes (re-verified 10/10 after write).
- Embedded stdout re-hash byte-exact for legs 1–7, 9, 10 (e.g. leg-1 `3eb8e06c…` 6 B; leg-2 `38d44bf8…` 3,089,024 B; leg-3 `75b83edf…4d01` 12,904 B; leg-4 `84d489f7…` 7,879 B; leg-7 `3492d27d…` 19,151 B; leg-9 `2a20c456…` 772 B; leg-10 `e4cf0833…` 2,577 B). BB4/BB5 receipt-file digests match the files exactly (`162b4831…`, `57ac0124…`).
- Mismatch — BB8 claims stdout `e0b2d505…3c232b` (5,301 B); no block or text in `leg-8.md` carries it. That file embeds a 5,301 B `/usr/bin/jq` stdout hashing to `9c47f056…`, noting the envelope hash differs from lane A's `e0b2d505…` because its session negotiated protocolVersion 2025-06-18 (vs 2025-03-26; equal length → equal byte count, different digest). `e0b2d505` is lane A's digest (`receipts/leg-8.md:13`), never embedded in receipts-B.
- Attribution: `leg-7.md`/`leg-8.md` are headed "Seat: CC7/CC8" (compare assignments) yet BB7/BB8 cite them as their own receipts; BB7's reported stderr timings (20.5 / 5131.59 ms) are absent (file: 18.89 / 5072.89 ms). Mtimes: BB7 19:01:44 → leg-7 19:02:16; BB8 19:02:35 → leg-8 19:03:24 — compare seats wrote last; BB7/BB8's originals are gone.

## THREATS
- BB7/BB8 originals unrecoverable; leg-7's hash match is cross-session determinism, not custody.
- External digests (carriers, wasm inputs, harness scripts) verified only as identical in-receipt records; not re-derived (no live probes).
- If wave convention made CC receipts canonical, the defect is stale BB pointers, not falsified measurement — flagged for L1.

## VERDICT
FINDING — BB8's claimed stdout digest `e0b2d505…` is absent from its cited receipt (`leg-8.md` embeds `9c47f056…` for that 5,301 B run); leg-7/leg-8 receipts are self-attributed to CC7/CC8, so BB7/BB8 custody is broken.
