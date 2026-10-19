# PATCH PROPOSAL (not applied) — additions to the proposed c1 knowledge entry (v2, deduped)

- Seat: CR-1 (chain c1, critic). Date: 2026-10-19.
- Base pin: EX-12's `knowledge-entry.patch.md` at
  sha256 `d662c195d75cdbdb07e3534170ce9cb2ac3f830b93d5380e7b8310bca7d8ba59`
  (mtime 07:14:01, 18,701 B) — the revision RV-3 graded. Applying its hunk A
  produces exactly the identity EX-12 claims: 9,513 bytes / 32 lines /
  sha256 `a5119120ee6a6142b8be6e297e39c85e0464fb27761c6ee0e7cc7cf8a1d5e56b`
  (re-verified by CR-1: `patch -p1` of the extracted hunk A → exit 0, same
  bytes/lines/hash). The two hunks below apply **on top of that file**.
- Patch sha256: `6f818afd280c708699e3defa9b82588c7470e478fcde07161d22409be9c0c07a`.
- Verified: `patch --dry-run` clean against the extracted base content.
- **Not included here — already proposed by others (do not duplicate):**
  the `recheck:` TMPDIR redirect is CR-2's F1
  (`claims/c1/CR-2/proposed-fixes.patch.md`) and RV-3's fix 1; apply one of
  those, not a third variant. CR-2's F3/F4/F5 (r3-07 candidate-2 refutation
  line, map-row wording, label nit) are theirs; CR-1's hunks do not touch
  those lines.

## Why (two additions unique to CR-1)

1. **The raw-of-hex trap needs its detector named.** EX-06 recorded the trap
   (`trap-raw-of-hex.json`: exit 0, 0 functions, `ev_60062ad0…`) but the entry
   does not say how a reader distinguishes a wrong-form run from an
   honest-empty run. The detector lives only in `normalized_result` (form echo,
   byte-count relation, digest identity), never in `raw_result`; and the
   `--full-output` envelope carries `ok:true` on a FAILED analysis (exit 1).
   CR-1 evidence: `CR-1/evidence/out-Ahex-raw.json`, `out-Bhex-raw.json`,
   `out-asciihex-hex.json`, `out-A-hex.json`, `fail-full.json`, `fail-plain.json`.
2. **Independent corroboration.** CR-1 compiled three further real-solc
   contracts on-host (7/7, 20/20, 64/64) and ran the masquerade controls
   (ERC-165 body constant excluded; body-level EQ/JUMPI decoy excluded;
   calldata-EQ/JUMPI constant not in any ABI IS reported — pattern-dispatch
   semantics). Strengthens the real-bytecode evidence base without changing any
   claim.

## Patch text

```diff
--- a/corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md
+++ b/corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md
@@ -22,8 +22,9 @@
 - **Observation (RESULT — Rv2Many @ 6.4.0):** `ev_d0d0b054…` — 11/11 planted selectors, zero false positives; no truncation at 11.
 - **Observation (RESULT — KdxToken @ 6.7.0):** `ev_56d89cb4…` (hex) and `ev_9259f412…` (raw) — 6/6, set-equal to the planted set; hex-shape variants (no trailing newline, `0x` prefix, uppercase) all decode to the same bytecode sha256 `9c40940e…`; every reported offset lands on byte `5b` (JUMPDEST) — the r4 offset-semantics erratum re-confirmed on real bytecode.
 - **Observation (creation code — parsed-and-empty, not excluded):** `Rv2Token.creation.hex` @6.4.0 `ev_c80379e1…` → 0 functions, `bytecode.kind:"unknown"`; `Smoke_sol_Smoke.bin` @6.4.0 `ev_f875e21e…` → 0 functions. Creation blobs carry no runtime dispatch table; these are parsed-and-empty results (`corpus/QUALITY.md:21`), not inventory exclusions.
-- **Observation (input-shape traps, KdxToken):** encoding is a positional argument (`<path> <raw|hex>` — the r3 quirk, `corpus/knowledge/2026-10-13-r3-evm-interface.md:93-96`; the `--encoding` flag-form rejection was not re-tested this round); interior whitespace / odd length / wrapped lines / CRLF → typed `invalid_request` exit 1; a raw-encoded copy of hex text decodes the file's bytes as code (exit 0, `ev_60062ad0…`, different bytecode digest); a temp-dir EDQUOT failure → typed `execution_failure` exit 1 — fail-closed, no silent success.
+- **Observation (input-shape traps, KdxToken):** encoding is a positional argument (`<path> <raw|hex>` — the r3 quirk, `corpus/knowledge/2026-10-13-r3-evm-interface.md:93-96`; the `--encoding` flag-form rejection was not re-tested this round); interior whitespace / odd length / wrapped lines / CRLF → typed `invalid_request` exit 1; a raw-encoded copy of hex text decodes the file's bytes as code (exit 0, `ev_60062ad0…`, different bytecode digest); a temp-dir EDQUOT failure → typed `execution_failure` exit 1 — fail-closed, no silent success. Form detection for the raw-of-hex case lives only in `normalized_result`: `artifact.encoding` echoes the form, and for `raw` runs `artifact.sha256 == bytecode.sha256` with equal byte counts, while `hex` runs show `artifact.bytes ≈ 2×bytecode.bytes` (±1-2 bytes of trailing newline) and differing digests; `raw_result` carries no form signal. Envelope trap: with `--full-output` a FAILED analysis is wrapped `{"ok":true,"data":{"code":"execution_failure",…}}` (exit 1) — `ok:true` is not a success indicator.
 - **Observation (independent recon):** EX-07's linear-sweep disassembler + pure-Python keccak reproduce the same selector sets and every probe offset for both carriers, all sources agree (`reconciliation-run.txt`: "VERDICT: ALL SOURCES AGREE"); RV-1 validates the keccak reference against two independent oracles and the ERC-20 vector table.
+- **Observation (independent critic compile, CR-1):** own solc `0.8.37+commit.f401782d` prefix (`/dev/shm/cr1/solc-prefix`; `soljson.js` sha256 `221d7a66…bad4c`, 9,237,611 B; npm tarball integrity `sha512-ieUYdPDRGNKMsZpCfi9tY64Q+ASoL8tyhLuvf9cFiqDs+6ijlx8Wn2CRi0N71AlCvRx0V092rlUYu3b3PuxWlA==`): `Cr1Sample` 7/7 with the ERC-165 body-level constant `0x80ac58cd` excluded (no false positive), `Many` 20/20, `Big` 64/64 (optimizer on, 3,079 B runtime) — zero missing, zero extra on all three; a body-level `EQ/JUMPI` decoy (`deadbeef`) is excluded, while a calldata-selector `EQ/JUMPI` constant not in any ABI IS reported as `dispatch:"abi"` (pattern-dispatch semantics, not a false positive). Sources: `.ufo/waves/arc3-loop1-round1/claims/c1/CR-1/evidence/{out-solc-runtime.json,out-many-opt1.json,out-big64.json,out-E2-hex.json,out-E3-hex.json}`; runtime reproduction `solc-runtime.hex` + `compile2.js`.
 - **Inference:** the recovered selectors are the compiled dispatch tables of the pinned carriers; the argument/mutability strings are upstream inferences consistent with the compiled ABIs — not verified ABI signatures, names, or source identity.
 - **Unknowns:** Vyper and other solc versions; optimizer-enabled dispatch shapes beyond the smoke compile; dispatcher prologues other than `5f3560e01c`/`60003560e01c`; the `ev_` id domain for this verb family; whether 6.7.0's CBOR metadata decode generalizes; behavior at carrier sizes above the probed ~1.8-1.9 KB runtime class; deployment/chain identity (never claimed by the tool).
 - **Limitations (tool-reported, every leg):** worker limits 256 MiB JS heap / 3 GiB address space / 30 s deadline / 16 MiB file cap; upstream-inference caveat; `kind`/hardfork/deployment-authenticity `unknown`; SHA-256 is not the Ethereum Keccak code hash; no runtime execution, chain/RPC lookup, or network request. Only the carriers and pins named above were probed.
```

Note for the applier: if the entry lands with this hunk, add
`claims/c1/CR-1/evidence/…` to its `source:` line as well (kept out of the hunk
to avoid rewriting a very long line here).
