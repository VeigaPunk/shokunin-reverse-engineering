# kaidoku round 37 — intended claim and honest-stop record (attempt 1)

L1 `KaidokuR37` (holds the §3 planner seat). Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.

## Intended claim (declared before wave dispatch; NOT frozen, NOT landed)

**R37-C1 — coverage**: big-endian SquashFS v4 (`squashfs_v4_be`) through
`sasquatch-v4be` via REA `extract-firmware` (rea-agents 6.5.0, unblob
26.6.4) — Frontier → Core, successor counter fixed per QUALITY 77/78
(every-occurrence matching, intended-document repair, package-root pin,
provenance by independent non-author reproduction).

Carrier set (committed, `corpus/evidence/round-37/c1/`): K1/K2 synthetic
standard-BE v4 gzip images built by `tools/round-37/gen-squashfs.py`
(expected record = committed source trees); K3/K4 unblob 26.6.4 integration
fixtures `squashfs_v4_be` `squashfs_v4.bin` / `squashfs_v4.nopad.bin`
(expected record = the unblob `__output__` apple1..4 regular files).

## Honest stop — why nothing landed this attempt

The run budget (200 requests) ended while the round was in the pre-freeze
probe phase. Therefore: no claims frozen, no counters scored, no after
receipts committed, no waves dispatched (the inline spawn handoff was never
used), no L2 seats ran, no census before/after, no lesson/assimilation rows.
This file and the wave dir are the record of what was probed; they are not a
landing. Report verdict: **not completed (honest stop at probe stage)**.

## Probe evidence (dev, pre-freeze; not counted as claim data)

- `tools/round-37/gen-squashfs.py` — deterministic SquashFS v4 writer (LE /
  BE / AVM-BE), validated: LE gzip images extract byte-identical with
  `/usr/bin/unsquashfs` (4.7.5); BE gzip images extract byte-identical with
  `~/.local/bin/sasquatch-v4be -be`; AVM-BE (LE metadata length fields,
  mkfs_time == bytes_used) fails on `sasquatch-v4be` without `-be` and on
  unblob's no-flag AVM branch (`ExtractCommandFailedReport`, stderr:
  "different endianess / failed to read id table block") — AVM stays
  Frontier with this evidence.
- REA `extract-firmware` after-runs on all four carriers succeeded and
  published every expected file: K1 5/5 (`firmware.bin_extract/...`,
  `squashfs_v4_be` handler, 0 gaps), K2 3/3 regular files + 1
  `unpublished-entry` symlink, K3/K4 4/4 apples (`.ufo/waves/round-37/probes/rea/`).
- Before-arm shape verified on K3: with every PATH dir containing
  `sasquatch`/`sasquatch-v4be` removed, REA returns `extraction_gaps[].kind`
  = `missing-extractor-dependency`, `dependencies = ["sasquatch-v4be"]`,
  `handler = squashfs_v4_be`, `coverage partial`, `published_bytes 0`.
- 7-Zip 26.04 does not open BE v4 images (refuses; recorded as rejection
  candidate for SOURCES / Gate flip).
- Fixture/unblob tag verified: `be-squashfs_v4.bin` (sha256
  `9c7c523c…97c0`) is the 26.6.4 test input; apples 1..4 sha256 recorded in
  `K{3,4}/oracle.tsv`.

## Gaps (must be closed by the next attempt)

- Freeze `plans/round-37-claims.md` (predicate sentence, counter, selftest,
  kill rule, controls) and score do-nothing controls first.
- Commit before receipts, dispatch wave 1 (build + first falsifiers) via the
  inline ready file, then wave 2, then land entry/rows/PROVINCE/README/SKILL/
  lesson/ASSORECARD/LOG; census start before any SOURCES edit.
- Assimilation id-collision check + quarantine slice are still due.
