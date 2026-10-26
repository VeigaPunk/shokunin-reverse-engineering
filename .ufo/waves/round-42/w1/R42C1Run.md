# R42C1Run — round-42 C1 run harness (port of tools/round-41/c1-run.sh)

**Verdict: DONE.** `c1-run.sh` is ported to round 42, the routed defect R41-CL2 is fixed and measured
(round-41 harness `exit 126` / `jq: Argument list too long` on a 316232-byte summary; round-42 harness
`exit 0` with `run.json` written), and both arms are proven end-to-end on DEVELOPMENT inputs only:
unblob 26.6.4 v3-family fixtures (five magic variants) and the designated OpenWrt Kamikaze 7.09 x86
image. Nothing was run on any published C1 carrier.

Artifact root: `.ufo/waves/round-42/w1/artifacts/R42C1Run/` (55 files including `checksums.txt`,
2.6 MB; `sha256sum -c checksums.txt` passes).
Key pins: `c1-run.sh` sha256 `60fccdf36efa865215a05edadfd971878c187a807486ca97c983e32ce70b4fb4`;
`final-evidence.log` sha256 `38af3eaf3ae260b56ab0eddb8230bee7ff409159e86f8cf9745ee0ba69f59470`;
`synth/synth-v4le.sqsh` sha256 `f342f747ce094e833740c45266fde158d1c21358963f44c0e3c499237004c99e`.
Oracle tool used for the last battery: `R42C1Oracle/sqfs3-oracle.py` sha256
`61fd53b7ddcca109581d094cb002aeb78472c5bda41e82915f6ab46745372871` (I also measured it at
`77d9e123…` and `f7beb56e…`; all three honour the same contract).

## 1. Delta vs round 41 (every change the ticket names)

| requirement | implementation | proof |
|---|---|---|
| scratch segment `/kaidoku-r42/` | default root `${HYAKU_SCRATCH:-/fast/scratch/hyaku}/kaidoku-r42`; an explicit SCRATCH without the segment is refused (exit 2) unless `C1_ALLOW_FOREIGN_SCRATCH=1`, which records `run_provenance_segment_ok:false` | F5 (exit 2, message); A/B receipts show `parameters.output_directory …/kaidoku-r42/A/extract` |
| output under `corpus/evidence/round-42/c1/<id>` | a bare `<id>` argument resolves to `$C1_EVIDENCE_ROOT/<id>` (default `<lane>/corpus/evidence/round-42/c1`; lane root found by walking up to the dir holding `corpus/evidence` + `plans`); an OUTDIR outside that root is refused (exit 2) unless `C1_ALLOW_FOREIGN_OUTDIR=1`; `outdir_under_evidence_root` is recorded in both receipts | F7 (`DEVX` → `…/corpus/evidence/round-42/c1/DEVX`, `outdir_under_evidence_root:true`); F4 (exit 2) |
| REA `--max-depth 1`, 6.5.0, absolute `REA_UNBLOB_COMMAND` | argv is `npx -y rea-agents@6.5.0 extract-firmware --format json --full-output --max-depth 1 <carrier> <fresh extract root>`; a relative `REA_UNBLOB_COMMAND` is refused (exit 2), the absolute path is resolved + hashed into `run.json` | A/B/C argv arrays; F2/F3 (exit 2); receipts show `parameters.max_depth 1` |
| precondition = plain `sasquatch` (not `sasquatch-v4be`) | `sq_pin` resolves `sasquatch` on the child PATH and records path/sha256/version; `sasquatch-v4be` is never located, used or required | A `sasquatch.version "4.5.1"`, sha `ad02d27a…`; F1 exit 2 with "sasquatch-v4be is NOT a substitute" while `sasquatch-v4be` is on PATH |
| oracle arm calls `sqfs3-oracle.py` (C1_ORACLE; default `tools/round-42/sqfs3-oracle.py`) and accepts `hsqs`, `sqsh` + vendor magics | the arm validates the tool's `--help` for `--work/--files/--nonregular/--json`, then runs `python3 -I <oracle> --work … --files … --nonregular … --json … [--offset N] <carrier>`; magic scan accepts `hsqs sqsh hsqt tqsh shsq qshs zlqs sqlz` | D (five magics, all exit 0), E (magic at offset 512 ⇒ `--offset` passed), F11 (help without `--json` ⇒ exit 2) |
| R41-CL2: no receipt-sized value through argv | the summary and the receipt are written to files under the scratch and read by jq with `--slurpfile` (`$summary[0]`, `$receipt[0]`); the oracle's own report is also read via `--slurpfile` | §2 |
| `run.json` keeps argv, UTC timing, exit codes, sasquatch path/sha256/version, REA+unblob versions, carrier pin, superblock summary, envelope and receipt digests | all present, plus `depth_ok`, `summary_error`, `receipt_error`, `previous_after_json_sha256`, `child_path`, `outdir_under_evidence_root`, `carrier.superblock` | A receipt excerpt in §4; `final-evidence.log` |
| prove on DEVELOPMENT input | unblob v3 fixtures (MIT) + OpenWrt Kamikaze 7.09 `openwrt-x86-2.6-squashfs.image` | A–E |

Additions beyond the literal ticket (kept because each closes a measured hole, all small):
`previous_outputs` cleanup in the oracle arm (a failed run cannot leave an older `oracle.tsv` in
the evidence dir — F9/G), a `parameters.max_depth == 1` assertion on every receipt (`depth_ok`,
fail-closed), and a measured compressor field (see §3).

## 2. R41-CL2 fixed and measured (same carrier, same flags)

The carrier is my own synthetic v4 LE gzip image (`synth/synth-v4le.sqsh`, 640 regular files, 1600
in-tree relative symlinks, 160 dirs; rebuild with `synth/gen-synth-tree.sh TREE OUT.sqsh`).

```
# round-41 harness (unchanged lane bytes), same carrier, /kaidoku-r41/ scratch:
bash tools/round-41/c1-run.sh after synth-v4le.sqsh ev-old3 $S/kaidoku-r41/run-old3
  exit 126
  stderr: tools/round-41/c1-run.sh: line 547: /home/vgpnk/.local/bin/jq: Argument list too long
  outdir: after.json only (no run.json)

# round-42 harness:
C1_ALLOW_FOREIGN_OUTDIR=1 bash …/R42C1Run/c1-run.sh after synth-v4le.sqsh \
    ev/corpus/evidence/round-42/c1/dev-synth-manylinks $S/kaidoku-r42/B
  exit 0
  run.json: receipt_written true, summary_bytes 316232, receipt_bytes 856518,
            files 640, unpublished 1600, summary_error null, receipt_error null
```

316232 B is 2.4× the per-argument cap that killed V4 in round 41 (146561 B on the real AVM rootfs);
the summary and receipt now reach jq only through files. jq 1.8.2 here still enforces the same
`MAX_ARG_STRLEN`, so the comparison is like-for-like.

## 3. Superblock summary: v3 layout measured, and the "compression" wording problem

`superblock_summary` parses the packed v1–v3 superblock (unblob 26.6.4 `SquashFSv3Handler`
`C_DEFINITIONS`) and the v4 layout, endianness from the magic, version from `s_major` at offset 28.
Offsets were verified field-by-field against the v3 LE fixture:
`mkfs_time@39=1637662965` (unsquashfs: Tue Nov 23 10:22:45 2021 UTC), `root_inode@43=64`,
`block_size@51=65536`, `fragments@55=1`, `bytes_used@63=258` — every one equal to
`unsquashfs -s` ("Filesystem size 258 bytes", "Block size 65536", "Number of fragments 1",
"Number of inodes 3"). A truncated carrier yields `superblock: null` instead of a traceback (F13).

**Draft defect to fix at the freeze:** P42-C1 says the carrier's "superblock reads the frozen
magic/major/compression". A v1–v3 superblock has **no compressor field** (v3 is gzip by definition;
LZMA-patched v3 images exist and are indistinguishable from the superblock). The harness therefore
records `s_major`/`s_minor`/`magic` from the superblock, `compression: null` plus
`compression_note: "v3 superblock has no compressor field"`, and a **measured** compressor from
`7z l -slt` on a 4-byte-magic-normalized copy (`compression: "ZLIB"`,
`compression_source: "7z l -slt on a 4-byte-magic-normalized copy"`; `C1_COMPRESSION_PROBE=0`
disables it). Recommendation: bind `compression` to `carrier.superblock.compression` (measured,
`"ZLIB"` on every fixture) or drop "superblock" for that field. This is evidence-shape feedback for
R42C1Counter, not a harness blocker.

## 4. Proof on DEVELOPMENT inputs (exact commands, exits, numbers)

All commands from `S=/fast/scratch/hyaku/kaidoku-r42/R42C1Run`, harness at its artifact path;
dev runs set `C1_ALLOW_FOREIGN_OUTDIR=1` because the evidence layout is a scratch copy.

| id | input | command tail | exit | salient receipt facts |
|---|---|---|---|---|
| A | unblob v3 LE fixture `hsqs`, 4096 B, sha `0161351c…` | `after FX ev/…/dev-v3-le $S/kaidoku-r42/A` | 0 | `handlers ["squashfs_v3"]`, `files 2`, gaps `["depth-limited"]`, `max_depth 1`, `subject == carrier sha`, `output_directory …/kaidoku-r42/A/extract`, `sasquatch 4.5.1`, `rea 6.5.0`, `unblob 26.6.4`, `compression "ZLIB"` |
| B | synthetic v4 LE, 640 f / 1600 l, sha `f342f747…` | `after synth-v4le.sqsh ev/…/dev-synth-manylinks …/B` | 0 | ARG_MAX proof (§2); `files 640`, `unpublished 1600` |
| C | OpenWrt Kamikaze 7.09 x86 `openwrt-x86-2.6-squashfs.image` (dev input), sha `a0a4fcf3…`, 5529092 B | `after fx/openwrt-7.09-x86-squashfs.image ev/…/dev-openwrt-7.09-x86 …/C` | 0 | `handlers ["extfs","padding","squashfs_v3"]`, `squashfs_v3` chunk `offset 4677120 length 786432 extraction_failed false`, `files 145`; `carrier.superblock null` (magic sits at 4.6 MB, outside the 1 MiB window — expected for a container image) |
| D | five v3-family fixtures | `oracle FX ev/…/dev-oracle-<magic> …` | 0 ×5 | `hsqs`/`sqsh` (v3.0), `tqsh` (ddwrt, v3.1), `shsq` (broadcom), `zlqs` (nonstandard); each `producers_equal true`, `mismatch 0`, tables copied, `compression "ZLIB"` |
| E | v3 LE fixture with 512-byte prefix | `oracle fx/offset512.bin …` | 0 | `magic_offset 512`, `argv` contains `--offset 512`, `files 2` |
| F8 | v3 LE fixture | `oracle … C1_ORACLE_CROSSCHECK=1` | 0 | `extractor_crosscheck {extract_exit 0, files_equal true, check_files 2}` (advisory: sasquatch is the extractor under test, never an oracle) |

Receipt path A (one line, from `run.json`):
`{"receipt_written":true,"depth_ok":true,"handler":["squashfs_v3"],"files":2,
"gap_kinds":["depth-limited"],"max_depth":1,"subject":"0161351caec8e9…",…,"sb":{"magic":"hsqs",
"version":"3.0","compression":"ZLIB"}}`.

## 5. Oracle-arm contract and failure mapping (agreed with R42C1Oracle in-wave)

```
python3 -I sqfs3-oracle.py --work DIR --files OUT.tsv --nonregular OUT.tsv --json OUT.json [--offset N] IMAGE
```
exit 0 = two non-sasquatch producers agree and both tables are written; 2 = unreadable/unsupported;
3 = producer disagreement. Harness mapping: tool 0 + valid tables → 0; tool 2 → harness **2** ("cannot
become a frozen carrier"); any other nonzero → **3**; tables malformed/missing with tool 0 → **3**
after `oracle-run.json` is written (`table_error`, `tables_copied:false`). The harness re-validates the
round-41 table grammar (3 tab fields, 64-hex sha256, bytewise-sorted unique relpaths, closed kind
vocabulary, no regular/non-regular overlap) so a malformed table cannot reach a freeze. The tool's
verdict is read from its own report (`cross_check.verdict == "agree"`, `cross_check.mismatch_count`)
and mirrored into `oracle-run.json` as `crosscheck.producers_equal` / `mismatch_count`, with the whole
tool report carried as `crosscheck.tool_report` and digested as `outputs.oracle_inner_json`.

## 6. Negative battery (all on the shipped harness bytes `60fccdf3…`)

`bash -n` 0, `shellcheck -S warning` 0, `shellcheck` (all checks) 0.

| probe | exit | evidence |
|---|---|---|
| F1 plain `sasquatch` stripped from PATH (v4be still present) | 2 | "plain sasquatch is not resolvable … sasquatch-v4be is NOT a substitute" |
| F2 `REA_UNBLOB_COMMAND=unblob` (relative) | 2 | "must be an absolute path" |
| F3 absolute but missing unblob | 2 | "missing or not executable" |
| F4 OUTDIR outside the round-42 evidence root | 2 | names `corpus/evidence/round-42/c1` and the escape flag |
| F5 SCRATCH without `/kaidoku-r42/` | 2 | run-provenance message |
| F6 oracle on a container image (magic beyond 1 MiB) | 2 | lists the 8 accepted magics |
| F7 bare id `DEVX` in an installed-style lane | 0 | outdir under `<lane>/corpus/evidence/round-42/c1/DEVX`, `outdir_under_evidence_root true` |
| F9 tool exits 3 (disagreement) | 3 | `run.json` written, `producers_equal false`, `tables_copied false` |
| F10 tool exits 0 with a duplicate relpath | 3 | `run.json` written, `table_error` set, no tables copied |
| F11 tool `--help` without `--json` | 2 | names the missing flag |
| F12 `C1_ORACLE` points at nothing | 2 | names the default install path |
| F13 8-byte carrier (magic only) | 2 | `superblock null`, `oracle.exit 2`, run.json written |
| G same outdir: success → failing tool | 3 then 0 | failing run removes the old `oracle.tsv`, records its sha in `previous_outputs`; clean rerun restores |

## 7. Risks, limits, and what I did not run

- **REA many-symlink flake (observed, not harness-caused).** On the 1600-symlink synthetic, 1 run
  of 4 failed with `execution_failure` / `ENOENT … readlink '<stage>/extracted/firmware.bin_extract/dN0/lNN'`,
  `retryable:false`; a fresh scratch+outdir succeeded identically (round-41 w2 measured 2/13 of the
  same shape). A counter-time REA rerun on a large-symlink carrier should treat that exact error as
  retryable-in-practice with a fresh outdir. The failed run still leaves an honest `run.json`
  (`receipt_written:false`, envelope `ok:false`, structured error), never a stale receipt.
- **1 MiB magic window.** The oracle arm accepts a carrier only when the magic is in the first 1 MiB;
  a container image must be carved first (F6). The after arm accepts any carrier (REA discovers
  chunks) but then reports `superblock: null` when the magic is outside the window (C).
- **Compression is measured, not superblock-derived** for v1–v3 (§3); the draft wording needs the
  amendment there.
- **No real v3 vendor carrier was run.** Reserved-carrier policy honoured: REA/unblob/sasquatch ran
  only on unblob MIT fixtures, my own synthetic tree, and the designated OpenWrt Kamikaze 7.09 dev
  input. Carrier selection, oracle freezing and REA-on-published-image belong to R42C1Img*/R42C1Oracle.
- **Oracle tool is live.** Three revisions (`77d9e123…`, `f7beb56e…`, `61fd53b7…`) all satisfied the
  contract; if the L1 freezes a later revision, re-run one oracle arm (D) to refresh the receipt.
- The advisory sasquatch cross-check (F8) is evidence, never a gate; a disagreement is recorded and
  does not change the exit status.
- Tools installed this wave: **none** (no pacman, no uv/npx installs, no writes to `~/.local/bin`).

## 8. Integration notes for the L1

- Install `artifacts/R42C1Run/c1-run.sh` at `tools/round-42/c1-run.sh` with the executable bit
  (already set in the artifact). Default `C1_ORACLE` is then the sibling `tools/round-42/sqfs3-oracle.py`.
- Runtime dependencies: `bash`, `jq` (≥1.6; `--slurpfile`), `python3`, `sha256sum`, `stat`, `realpath`,
  `npx`, `timeout`; the after arm needs plain `sasquatch` on PATH and an absolute `REA_UNBLOB_COMMAND`;
  the oracle arm needs the oracle tool (which needs `unsquashfs` + `7z`); `7z` is also used for the
  optional compressor probe.
- `tools/round-42/c1-run.sh` and the oracle tool both belong on the C1 frozen-path list
  (`plans/round-42-claims.md` already names `c1-run.sh` and "the oracle tools").
- `run.json` schema is `kaidoku-r42-c1-run-v1`, claim `R42-C1`; no counter clause is known to read it
  (round-41 w2 established that), so the added fields are additive evidence, not a counter interface.
- Dev receipts in `receipts/` exist only to prove the harness; they are not round-42 carrier evidence
  (`outdir_under_evidence_root:false`, paths under `/fast/scratch/hyaku/kaidoku-r42/`).
