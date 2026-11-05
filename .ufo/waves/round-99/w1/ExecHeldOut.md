# ExecHeldOut — held-out soundness probe of `tools/round-99/upx-pe-repair.py` at Bk

Seat: ExecHeldOut (executor, leaf). Date: 2026-11-05. Lane: kaidoku-shokunin round 99, attempt 1.
Target: `tools/round-99/upx-pe-repair.py` read from freeze Bk `c19d57cd2e65a036478b9e78f6c5397dedfb2bcb`
via `git show Bk:tools/round-99/upx-pe-repair.py`; candidate sha256
`ac97598a94c041199cdf2cc3f700257989e8d70545bddb56e154e51b85d518d8`. Packer oracle: `/usr/bin/upx` 5.2.0
(`upx --version` → `upx 5.2.0`). No tool installed/updated (RULES.md read; none needed). No pacman, no
sysctl, no writes outside scratch `/fast/scratch/hyaku/kaidoku-r99/ExecHeldOut` and the wave directory.

## Method
1. `git clone --shared /home/vgpnk/Projects/shokunin/kaidoku-shokunin $S/clone`; `checkout --detach Bk`;
   `git rev-parse --show-toplevel` = `$S/clone` (TOPLEVEL-OK); `git status --porcelain` empty.
2. 9 held-out carriers, all disjoint from the battery's 10 pinned carriers (pinned `freeglut32.vc14`,
   `gle64.vc9`, `llio_i386`, `lib7-Zip-JBinding`, `WinHelloCPP.exe` etc. excluded). Copied to scratch,
   packed with `upx --best -q -f` (9/9 rc 0), `upx -t` 9/9 rc 0. Source sha256 in
   `.ufo/waves/round-99/w1/ExecHeldOut/carrier-sha256.txt`.

| carrier | source (absolute) | PE | packed B | seed |
|---|---|---|---|---|
| freeglut32vc10 | /usr/lib/python3.14/site-packages/OpenGL/DLLS/freeglut32.vc10.dll | PE32 | 78848 | 990100 |
| freeglut32vc9 | .../freeglut32.vc9.dll | PE32 | 79360 | 990101 |
| freeglut64vc10 | .../freeglut64.vc10.dll | PE32+ | 94208 | 990102 |
| gle32vc14 | .../gle32.vc14.dll | PE32 | 29696 | 990103 |
| gle64vc14 | .../gle64.vc14.dll | PE32+ | 39936 | 990104 |
| gle64vc10 | .../gle64.vc10.dll | PE32+ | 38400 | 990105 |
| llio64amd | /opt/ghidra/GPL/DMG/data/os/win_x86_64/llio_amd64.dll | PE32+ | 32256 | 990106 |
| wallace_src | /opt/ghidra/docs/GhidraClass/ExerciseFiles/VersionTracking/WallaceSrc.exe | PE32 | 10752 | 990107 |
| wallace_v2 | .../VersionTracking/WallaceVersion2.exe | PE32 | 10752 | 990108 |

5 PE32+ DLLs, 4 PE32 carriers (5 DLL + 2 EXE Ghidra + 2 EXE-type DLL sets); 6 carriers are DLLs beyond
the seat minimum of 6 total. Matrix per carrier: 20 cut points uniform in [1, size-1] (`random.Random(seed)`,
seeds above, recorded), 3 appended overlays (`os.urandom`, lengths from same seed, 1..65536), each in two
variants — untampered and battery-`tamper("both")` (first `UPX!` zeroed; UPX-prefixed section names renamed
to `.text`/`.data`/`.rdata`; tamper applied to the full pack before cutting, battery order) — plus intact and
tampered-intact extras: 48 cells/carrier, 432 total. Driver: `python3 -I -B driver.py candidate.py probe`
(TMPDIR in scratch), battery semantics for oracle runs, rc-0 output testing (`upx -t`), and `upx -d`
unpack-equivalence as a secondary check.

## Results — axes
**SOUND: 72/72.** Exactly 72 cells got candidate rc 0 (per carrier 8: intact, tampered-intact, 3 untampered
overlays, 3 tampered overlays). Every rc-0 output passed `upx -t` (rc 0), and all 72 matched the reference
`upx -d` sha256 (untampered pack for repairs; pack+same-overlay for overlay inputs). unpack_mismatch 0.
**No unsound cell exists; list empty.**

**OVER-REFUSAL: 0/432.** All 36 oracle-passing inputs (27 untampered overlays + 9 intact packs) were
accepted rc 0, as were all 54 overlay-arm cells including the 27 tampered repairs, and all 9 tampered
intact packs. No rc 2 on any input where `upx -t` passes or would pass after the round-98 repair.
**Over-refused cell list empty.**

**COMPLETE: 360/360 cut inputs refused rc 2, no output written; 354/360 with the `truncated` label.**
All 9 packs have aligned_end == file size (overlay 0), so every cut is a length failure; the candidate
refused every one. Oracle failure texts observed (cited from runs):
- near-end cuts → `OverlayException: invalid overlay size; file is possibly corrupt` (the claim's S326
  signal) — all refused `truncated`.
- mid cuts, untampered → `CantUnpackException: header corrupted` (PackHeader u_len/c_len no longer fit the
  short file — truncation-induced, `src/packhead.cpp`) — all refused `truncated`.
- tampered cuts → `CantUnpackException: (file is possibly) modified/hacked/protected` (gate fires first) —
  all refused `truncated` (mixed tamper+truncation; refusal correct).
- 6 header-region cuts below PE-parse minimums refused by earlier structural gates instead: gle32vc14
  cut@501 B (`sections`, tamper=none and both), gle64vc14 cut@210 B (`not-pe`, none/both), wallace_src
  cut@203 B (`not-pe`, none/both). For these the oracle itself never reaches overlay arithmetic:
  `IOException: file is too small -- skipped` (203/210 B) or PE-table parse failure (501 B). Not length-
  overlay failures per the oracle's own text; recorded as a label nuance, zero rc 0, zero soundness risk.

Totals: `{"cells": 432, "sound_violations": 0, "over_refusal": 0, "complete_miss": 0, "candidate_error": 0,
"unpack_mismatch": 0}` (driver tally; oracle-length-class cells 29, substance-complete 360/360 refused).

## Per-carrier counts (cells 48 each: 40 cut + 6 overlay + 2 intact)
| carrier | rc0 sound | unsound | over-ref | `truncated` | other-label rc2 |
|---|---|---|---|---|---|
| freeglut32vc10 | 8 | 0 | 0 | 40 | 0 |
| freeglut32vc9 | 8 | 0 | 0 | 40 | 0 |
| freeglut64vc10 | 8 | 0 | 0 | 40 | 0 |
| gle32vc14 | 8 | 0 | 0 | 38 | 2 (`sections`) |
| gle64vc14 | 8 | 0 | 0 | 38 | 2 (`not-pe`) |
| gle64vc10 | 8 | 0 | 0 | 40 | 0 |
| llio64amd | 8 | 0 | 0 | 40 | 0 |
| wallace_src | 8 | 0 | 0 | 38 | 2 (`not-pe`) |
| wallace_v2 | 8 | 0 | 0 | 40 | 0 |

## Coverage limits (held-out set)
- Every held-out pack places the PackHeader at offset 992 — the battery's g4 forgery (non-992 anchor)
  remains the only guard for that axis; this probe adds no non-992 sample (none occur in these carriers).
- Packs carry no native overlay (aligned_end == size); overlay tolerance was exercised only via the 54
  appended-overlay cells (lengths 1..65536 from the seeds, `os.urandom` bytes).
- Candidate integrity at Bk: single PackHeader candidate enforced (packheader-candidates gate); no decoy
  cells in this probe (battery g5/g6/g8 cover size-cache/lazy-anchor/oracle-caller).

## Verdict
Held-out probe of the R99-C2 candidate at Bk over 9 unseen carriers (432 cells): SOUND 72/72, COMPLETE
360/360 refused (354 `truncated`, 6 early-gate structural on unparseable header cuts), OVER-REFUSAL 0/432,
unpack-equivalence 72/72, candidate errors 0. No defect found; one label nuance recorded (6 cells above).

Receipts: `.ufo/waves/round-99/w1/ExecHeldOut/heldout-summary.json` (per-carrier seeds, cuts, overlay
lengths, pack geometry), `heldout-cells.json` (all 432 cells), `carrier-sha256.txt` (9 source sha256 +
candidate sha256). Scratch deleted after this report.
