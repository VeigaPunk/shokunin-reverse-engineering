# PL-2 — C1 freshness: pacman row census

**Disposition: CORRECTED, with a gate discrepancy.** I re-derived the live package-cache count and the other mutable claims in `PROVINCE.md:50`. I did not edit `PROVINCE.md` or any protected/source path; this is patch text and evidence only. Repository HEAD was `947091d`; the source row is `PROVINCE.md:50` and the file has 162 lines.

## First-hand measurements

- Host date: `date +%F` → `2026-10-19`.
- Independent cache census:

  ```text
  archive_count=1350 signature_count=1350 missing_signature_count=0 orphan_signature_count=0
  ```

  Command: Python `Path('/var/cache/pacman/pkg').glob('*.pkg.tar.zst')` and `glob('*.pkg.tar.zst.sig')`, then pair-check each archive with its appended `.sig` and each signature with its corresponding archive. A second run reported `archive_glob=1350`, `signature_glob=1350`, `archives_without_adjacent_signature=0`, `signatures_without_archive=0`.
- The old `1,556` is retained only as the dated `2026-10-13` snapshot recorded in `corpus/knowledge/2026-10-13-pacman-packages.md:21-25`; it is not used as evidence of the live count. Recomputed arithmetic: `1350 - 1556` → `-206`.
- Installed-`jq` claim rechecked: `pacman -Q jq` → `jq 1.8.2-1`; `pacman -Qkk jq` → `jq: 25 total files, 0 altered files`. The one matching cached archive is `jq-1.8.2-1-x86_64.pkg.tar.zst`; its `.sig` exists. `gpg --homedir /etc/pacman.d/gnupg --verify ...sig ...pkg.tar.zst` → `Good signature from "Felix Yan <felixonmars@archlinux.org>" [full]`, exit 0 (GPG also warned that the trustdb was not writable). SHA-256 of the extracted `usr/bin/jq` archive member and installed `/usr/bin/jq` both independently measured as `e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806`.

## Same-line patch text

Proposed replacement for `PROVINCE.md:50` (one row remains one line; scratch verification retained the 162-line file length):

```text
| Archive/package inventory | `inspect_artifact`/`extract_artifact` (`available:true` in live session, 2026-10-13); pacman `.pkg.tar.zst` corpus 1,556 signed archives (2026-10-13 snapshot; live re-count 2026-10-19: 1,350 archives and 1,350 matching `.sig` sidecars, −206; see `corpus/knowledge/2026-10-13-pacman-packages.md:73-83`); `.MTREE` per-file sha256; `pacman -Qkk` verify | `binary_session {}` capabilities | installed `jq 1.8.2-1` byte-identical to its signed archive member (reverified 2026-10-19; SHA-256 `e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806`) |
```

The explicit live-delta pointer targets the append-only erratum at `corpus/knowledge/2026-10-13-pacman-packages.md:73-83`. The 2026-10-13 qualifier for the prior `available:true` observation follows the Core table's own scope statement at `PROVINCE.md:40` (“each verified on this host 2026-10-13”). The `jq` portion is now dated to this seat's fresh verification.

## Whole-row perishable census

- **Archive count `1556` — CORRECTED.** It is a dated 2026-10-13 snapshot, not a current count. Live count: 1,350 archives and 1,350 paired sidecars; delta −206. The live census established sidecar presence/pairing; only the `jq` archive was cryptographically verified in this seat.
- **`available:true` “in live session” — UNVERIFIABLE as a 2026-10-19 live state.** It is intrinsically perishable, but the Core-table date at `PROVINCE.md:40` dates the recorded observation to 2026-10-13. The replacement makes that scope explicit; this seat did not have a live `binary_session` probe to refresh it.
- **Installed `jq` byte identity — VERIFIED as of 2026-10-19.** This is also perishable (installed bytes/package can change); current package, `pacman -Qkk`, good archive signature, and byte identity were re-derived above, and the replacement dates it locally.
- **`.MTREE` per-file SHA-256 — VERIFIED as a format/capability statement, not a changing inventory value.** The corpus description at `corpus/knowledge/2026-10-13-pacman-packages.md:14-16` identifies `.MTREE` as carrying per-file digests.
- **`pacman -Qkk` and `binary_session {}` — not perishable values.** These are verification/probe methods in the row, not asserted outcomes. The separate installed-`jq` outcome is dated as above.

## Census instrument

The instrument hash is `e4fb740cb8153f15c623f3b9f7ca781e270053b0557be5393010359b2213b7b4` (`.ufo/gates/c1-census-v10.py`). The required PASS did **not** reproduce, either on the unmodified worktree or on a `/var/tmp` scratch root carrying the proposed same-line patch:

```text
-- UNDECLARED (1) --
  SCORECARD.md block 1833-1839 [scope None]
      :1834 [pin] None=6.7.0 -> AMBIGUOUS (no client token in clause)
SCOPE-ERRORS (marker assertions): []
FRONTIER register (G21): 14 rows asserted, errors: []
VERDICT: FAIL  (stale=0 ambiguous=0 undeclared=1 unresolved=0)
candidate_gate_exit=1
```

The new SCORECARD locus at `:1834` is beyond the instrument's declared SCORECARD scope (ending at `:1813`); the same lone failure occurs before and after the candidate row. The scratch candidate retained exactly 162 PROVINCE lines. I did not alter the gate or SCORECARD, which are outside my write scope. Therefore the row patch is measured, but “instrument still reads PASS” is a **DISCREPANCY / unmet condition**, not a pass claim.
