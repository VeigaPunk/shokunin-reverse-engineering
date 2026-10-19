# EX-3 — C1 freshness: PROVINCE row 50

Chain: `c1`  
Seat: `EX-3`  
Measured worktree: `947091d6b6f52684faf9ca53adf94ff8a0f6b006` (`git rev-parse HEAD`)  
Scope: produce a same-line `PROVINCE.md:50` patch proposal and census the other row claims. No shared or tracked source was edited.

## First-hand measurements

- `ls /var/cache/pacman/pkg/*.pkg.tar.zst | wc -l` → `1350`
- `ls /var/cache/pacman/pkg/*.sig | wc -l` → `1350`
- Independent filename pairing (`*.pkg.tar.zst` against `*.pkg.tar.zst.sig`) → `archives=1350 signatures=1350 missing_signatures=0 orphan_signatures=0`. This establishes sidecar presence/pairing, not cryptographic validity of all signatures.
- Arithmetic recheck: `1350 - 1556` → `delta=-206`. The 1,350 inventory is re-derived above. The 1,556 historical baseline is not independently reconstructable from the current cache; the original dated record is `corpus/knowledge/2026-10-13-pacman-packages.md:21-25`, which records its source command but not a retained raw listing. I do not treat that previous measurement as fresh evidence.
- `wc -l PROVINCE.md` → `162 PROVINCE.md`.
- `grep -n 'rea-agents@' ~/.kimi-code/config.toml` (searched with the workspace Grep tool) → `/home/vgpnk/.kimi-code/config.toml:4126:args = [ "-y", "rea-agents@6.7.0", "mcp" ]`.
- `pacman -Q jq` → `jq 1.8.2-1`; `pacman -Qkk jq` → `jq: 25 total files, 0 altered files`.
- `sha256sum /usr/bin/jq` and an in-memory `tar -xOf` hash of the matching cached archive member both returned `e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806` (current byte identity re-derived 2026-10-19).

## Row census (`PROVINCE.md:50`)

1. **Pacman archive count — CORRECTED (proposal only; not landed).** `1556 signed archives` is presented without a local as-of qualifier and reads as a live count. The live inventory is 1,350 archives; there are 1,350 matching sidecars with no unmatched names. The `1,556` historical count remains only as a dated recorded value; the independent historical filesystem state could not be reconstructed. Link the live delta to `corpus/knowledge/2026-10-13-pacman-packages.md:73-83` as requested.
2. **`available:true` in a live session — UNVERIFIABLE as a current claim.** This is perishable REA-session availability, but the seat has no live `binary_session` tool to remeasure it. The enclosing table is explicitly dated `verified on this host 2026-10-13` at `PROVINCE.md:40`, and the census declares the row `DATED` (`.ufo/gates/c1-census-v10.py:257,259`). The patch makes the date explicit and avoids presenting it as current.
3. **Installed `jq` byte comparison — VERIFIED for 2026-10-19.** `pacman -Qkk` plus equal independently calculated installed/archive-member SHA-256 values support the same result today. It is still a perishable state claim, so the patch dates the recheck.
4. **`.MTREE` per-file SHA-256 and `pacman -Qkk` verify — no additional perishable result found.** These are the row's format/tool-capability descriptions, not live counts or fresh tool-availability outcomes. `binary_session {}` is likewise the probe reference, not a reported current result.

## Proposed patch text (same physical line; not applied)

```text
| Archive/package inventory | `inspect_artifact`/`extract_artifact` (`available:true` recorded in the 2026-10-13 live session; not current-session evidence); pacman `.pkg.tar.zst` corpus: 1,556 archives (recorded 2026-10-13); re-read 2026-10-19: 1,350 archives + 1,350 matching `.sig` sidecars, −206 vs recorded snapshot (see `corpus/knowledge/2026-10-13-pacman-packages.md:73-83`); `.MTREE` per-file sha256; `pacman -Qkk` verify | `binary_session {}` capabilities | installed `jq` matched its signed archive member (2026-10-13 record; rechecked 2026-10-19) |
```

## Census gate result

Baseline command: `python3 .ufo/gates/c1-census-v10.py` (read-only). Exit **1**, not PASS:

```text
live anchors (re-derived): {'devin': '6.5.0', 'omp': '6.5.0', 'kimi': '6.7.0'}
PROVINCE.md    lines=162  loci=6
SCOPE-ERRORS (marker assertions): []
FRONTIER register (G21): 14 rows asserted, errors: []
G2 positive-assertion guard: ok (current-ok loci per file: PROVINCE.md=20, SCORECARD.md=17, SKILL.md=3; total loci=19; floor=1/file)
DECLARED FAIL CLASSES: []
VERDICT: FAIL  (stale=0 ambiguous=0 undeclared=1 unresolved=0)
```

The live `PROVINCE.md:18` pointer to `~/.kimi-code/config.toml:4126` is `current-ok` in that output. The blocking finding is elsewhere: `SCORECARD.md` block `1833-1839`, line `1834`, has `6.7.0 -> AMBIGUOUS (no client token in clause)` and is outside the gate's declared SCORECARD scope (`.ufo/gates/c1-census-v10.py:264-277`).

I applied the proposed same-line text only to a `/var/tmp` scratch copy and ran the same gate with `--root` pointing there. Scratch check: `lines 162 -> 162`; the gate still exited 1 with `undeclared=1` at `SCORECARD.md:1834`. The PROVINCE patch therefore preserves line count, but cannot satisfy the frozen “instrument PASS after” condition by itself. The separate SCORECARD scope finding is outside this seat's write authority and remains for integration/adjudication.

## Per-item verdict summary

- Live pacman inventory: **VERIFIED** — 1,350 archive files and 1,350 exactly paired `.sig` sidecars.
- Historical 1,556 baseline: **UNVERIFIABLE** from current filesystem; retained only as an explicitly dated source-record value in the patch proposal.
- PROVINCE row-50 correction: **CORRECTED** as patch text only; source file intentionally unchanged.
- Current `jq` archive comparison: **VERIFIED** for the 2026-10-19 recheck.
- REA `available:true` current status: **UNVERIFIABLE** without a live REA session; proposed text dates the historical observation.
- Census acceptance: **DISCREPANCY** — expected PASS is blocked by the independently measured undeclared `SCORECARD.md:1834` locus; both baseline and scratch-after runs fail identically.
