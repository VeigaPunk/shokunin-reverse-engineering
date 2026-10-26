# Round 42 — SquashFS v3 (`squashfs_v3`, `squashfs_v3_ddwrt`) promoted to Core on four published LZMA rootfs images; triage table v4 matches its evaluator 78/78 but stops on one combo's declared gap set

Base `c4a38ea2fcd7a7da096358f9bf462c9a4be3c33c` (round-41 L1 landed `ae5dc3f3` at 21:44Z, after this round began).
Draft `fdabdfa4`. Freeze `d1681696dd63ca4f9b8a09ffa8fa3e2de5e2b51b` (`plans/round-42-claims.md`, `tools/round-42/*`,
C1 carriers/fetch receipts/oracles, C2 fixtures, dev arm and controls, SKILL rule block 21 + entry, S130, dry runs,
wave-1 evidence). Controls `b024051c`. Data `d5e22b51`. C1 landing `eb8215ac` (measured revision). Scores `d4b4b4fb`.
L1 `KaidokuR42`. Wave 1: 43 seats (`.ufo/waves/round-42/w1/`, all settled). No wave 2 (see report).

Author verdicts (closure pending):

- **R42-C1 met.** `tools/round-42/c1-counter.py` at `eb8215ac`: `carriers_matched 4` of 4, every binding true,
  `frozen_path_changed []`, exit 0, with a counter-time REA rerun of each carrier (`.ufo/waves/round-42/l1/scores/c1-at-eb8215ac.json`).
  Before: CTL-C1-0 0/4 exit 1; CTL-C1-1 (round-41 receipts relabelled) 0/4 exit 1 (`.ufo/waves/round-42/controls/c1/`).
  OW-A8092 409 files, OW-X86FS 403, DW-MEGA 447, DW-FONERA 569; one `unpublished-entry` per symlink, one `depth-limited`.
- **R42-C2 not met — honest stop.** `tools/round-42/c2-counter.py` at `eb8215ac`: `matched 78` of `n 78`, but
  `observed_features_match_declared` false, exit 1 (`.ufo/waves/round-42/l1/scores/c2-at-eb8215ac.json`): combo C02's
  manifest declares gap kinds {extractor-failure, unpublished-entry}; REA observed {depth-limited, extractor-failure,
  unpublished-entry}. Both sets decide the same label (`partial-body-failure`), so the table is not wrong there; the
  generator's predictor of when REA mints `depth-limited` beside a failing chunk is. The rule is not changed after scoring.

## Mistakes

| id | class | evidence pointer | captured-by | fix (shown able to fail) |
|---|---|---|---|---|
| M42-1 | a probe frozen on fixtures of one writer: the C1 counter's compression test read only zlib/LZMA-alone headers, and squashfs-lzma 3.0 (OpenWrt, DD-WRT) writes raw LZMA1 metadata with no header, so every real carrier read `compression undetermined`; a symmetric first header (`0x0606`) also left byte order ambiguous | `.ufo/waves/round-42/l1/dryrun-c1-pre.json` (dev arm 0/4, then 3/4) | QUALITY 84 (dry run before the freeze) — it caught it | behavioural raw-LZMA1/zlib decode and whole-chain walk in `tools/round-42/c1-counter.py`; same dev arm 4/4 (`l1/dryrun-c1.json`); QUALITY 85 |
| M42-2 | a generator's declared feature tuple predicted from factors instead of measured: C02 lacks `depth-limited` that REA mints when a sibling extraction reaches the ceiling (R42C2Gen's own wave-1 note 2) | `l1/scores/c2-at-eb8215ac.json` `declared_features.mismatch` | QUALITY 84 checks the key, not the predictor; the dev arm happened not to draw this shape | QUALITY 85: the generator must refuse to write a manifest whose declared tuple differs from the observed one in its own `--run` pass (red: this manifest; green: a manifest built after that check) — routed R42-CL1 |
| M42-3 | interface seams between three seats' tools found only by the end-to-end dry run: the counter never materialised the committed fixtures for regeneration, and its legacy binding rejected the dev arm's own `no-squashfs-chunk` class | `l1/dryrun-c2-pre.json` (exit 2 `generator_failed`), `l1/dryrun-c2-pre2.json` (78/78, one binding false) | QUALITY 84 | both fixed before the freeze; `l1/dryrun-c2.json` exit 0 |

## Gate

### Sources opened this round (2026-10-26)

| row | URL | opened | located quote |
|---|---|---|---|
| S130 | https://github.com/onekey-sec/unblob/tree/26.6.4/tests/integration/filesystem/squashfs | 21:50:43Z (`w1/R42SrcUnblob.md`) | tree API listing of the v1–v3 fixture paths; LICENSE quote in `w1/artifacts/R42SrcUnblob/LICENSE-quote.txt` |
| S131 | https://archive.openwrt.org/kamikaze/8.09.2/atheros/ | 22:53:30Z (L1) | md5sums line 6 "b931dabdcf55adb7d1115ae6f1e27924  openwrt-atheros-root.squashfs" |
| S132 | https://archive.openwrt.org/kamikaze/8.09/x86/ | 22:53:32Z (L1) | md5sums line 7 "0118b7fa4992698780a4ac2e774d78b9  openwrt-x86-squashfs.fs" |
| S133 | https://download1.dd-wrt.com/dd-wrtv2/downloads/v24/Broadcom/Linksys/WRT54GL_1.0/ | 22:53:34Z (L1) | "dd-wrt.v24_mega_generic.bin 24-May-2008 11:48 6017024"; MD5SUMS line 68 |
| S134 | https://download1.dd-wrt.com/dd-wrtv2/downloads/v24/Atheros%20WiSoc/Fonera/ | 22:53:35Z (L1) | "linux.bin 20-May-2008 00:37 6684672"; MD5SUMS line 12 |

Registry 129 → 134 rows, all tier A, `mined`; each fetched image's md5 equals its publisher line. Rejected as carriers:
the D-Link legacyfiles images (`w1/R42C1ImgVendor.md`) — no valid https (certificate chain fails), flip: an https
mirror by the publisher. `used-by` changes on existing rows: none.

### Assimilation

Assimilation: none adopted this round. `w1/R42Assim.md` reviewed the AVM-LE and sasquatch candidates (2 admit, 2
reject recommended); adoption needs re-grounding of shokuknow host-local work files and was not landed for lack of
round capacity — the review stays as the starting point. Id-collision check (`w1/R42AssimIds.md`): collisions 24
(S106–S129); 0–3-space guard proven on an indented fixture; quarantine slice 5 rows, byte-identical to round 41.

### considerthese

No `considerthese/` directory exists in this lane.

## Round-41 spot-check disposition

| id | state | where |
|---|---|---|
| R41-CL1 | fixed | one key `declared_features` (counter reads only it; selftest red on `declared`) — C2 still stopped, on M42-2 |
| R41-CL2 | fixed | `c1-run.sh` passes summaries through files, never `--argjson` |
| R41-CL3 | prepared, not landed | `w1/R42LocalSrc.md`: 18 rows resolvable with in-lane copies (gate exit 0 in a clone) |
| R41-CL4 | fixed in the table | block 21 handler-family cells; legacy chunks never `no-squashfs-chunk` (dev arm) |
| D1 | resolved | round-41 L1 commit `ae5dc3f3`; `tools/round-42/prefile-gate.py` (12/12 selftest) |
| D2 | resolved | `w2/R41W2C2Table.md` committed (`w1/R42Late41.md`) |
| D3 | addressed | report carries a cross-domain line |
| D4 | fixed | every round-42 score receipt carries `counter_sha256` |
| D5 | fixed | segment-bounded paths; fetch tool never writes through a symlink |
| R40-CL2 | open | the rerun proves consistency, not provenance |

## Routed defects into round 43

| id | defect | evidence |
|---|---|---|
| R42-CL1 | generator declares tuples it did not observe (M42-2) | C02 |
| R42-CL2 | no wave 2 attacked the landing | report |
| R42-CL3 | R41-CL3 copies prepared but not landed | `w1/R42LocalSrc.md` |

## Criteria added

- QUALITY 85 (M42-1, M42-2).
