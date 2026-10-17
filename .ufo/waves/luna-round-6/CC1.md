# CC1 — compare leg 1 (lane A vs lane B)

## CLAIM
Byte-compare `receipts/leg-1.md` (lane A) vs `receipts-B/leg-1.md` (lane B) for L1: stdout identical? classes identical? Report PASS/DIVERGE.

## METHOD
`receipts-B/leg-1.md` absent at seat start; polled 10s → appeared (864 B, mtime 18:59:56). Read both receipts (`receipts/leg-1.md:1-11`, `receipts-B/leg-1.md:1-47`); no re-run of the probe. Recomputed stdout payload: `printf '6.5.0\n' | sha256sum` → `3eb8e06ca1e02f0a30b0e3eebd289494b35d4fd1466ed907b9148e03b2459b00`. Verified B's raw-bytes claim with `printf '6.5.0\n' | xxd` → `36 2e 35 2e 30 0a`. Field-level diff plus `sha256sum` of both receipt files; A's digest checked against `receipts/MANIFEST.txt`.

## FINDINGS
- **stdout identical: YES (byte-level).** Both receipts record stdout `6.5.0` with sha256 `3eb8e06ca1e02f0a30b0e3eebd289494b35d4fd1466ed907b9148e03b2459b00` (`receipts/leg-1.md:11`, `receipts-B/leg-1.md:26`); my independent recomputation of the literal `6.5.0\n` yields the same digest, and B's raw bytes `36 2e 35 2e 30 0a` (6 bytes, trailing LF) check out.
- **classes identical: YES.** B states `RESULT. MATCH.` (`receipts-B/leg-1.md:45`). A states no label (evidence gap), but records exit 0 + `6.5.0`, which maps to RESULT under the frozen L1 prediction (version 6.5.0, exit 0).
- Exit codes identical (0/0); stderr identical (empty/(empty)).
- Token set unchanged: `npx -y rea-agents@6.5.0 --version`. A ran `cd /tmp && timeout 240 …`; B ran `cd /tmp/rea-bb1 && …` — both cwds under /tmp (probe rule met).
- Receipt *documents* are not byte-identical (271 B vs 864 B); `diff` shows template/boilerplate differences only — no conflicting measured field. A's file hash `24bfd90f…` matches `receipts/MANIFEST.txt`.

## THREATS
A's class label is derived, not declared. B omits the explicit `timeout 240` wrapper (states budget honored; ~0.6s wall, npx cache hit) — latent harness gap, no exposure this leg. `sha256sum -c MANIFEST.txt` fails parsing because the manifest stores `file hash` while sha256sum expects `hash file`; the value verifies manually. Compare covers L1 only; one run per lane; both lanes resolve rea-agents via npx cache, so a shared cache could mask registry/publish drift.

## VERDICT
CLEAN — PASS: stdout byte-identical (sha256 `3eb8e06c…`), outcome class RESULT identical across lanes; differences are template formatting, cwd, and timeout-wrapper only.
