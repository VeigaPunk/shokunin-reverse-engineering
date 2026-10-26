# R38ExecAfterK4 — R38-C1 carrier K4 after-receipt

Leaf seat, wave 1. Scope: produce the R38-C1 `after.json` for carrier **K4** and report; no
counter, carrier, oracle or frozen predicate was changed. Nothing was written outside
`.ufo/waves/round-38/w1/artifacts/R38ExecAfterK4/` and this report.

## 1. Revisions and lane state

| item | value |
|---|---|
| lane | `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` |
| base | `77091b492cc53f8743bd0701b1e7d5e66123dd84` |
| freeze (claims/counters/harness/carriers/instruments) | `e059ca9391642d5b71b6662cabcbdce0d9308719` (`git cat-file -t` → `commit`) |
| control receipts | `efd5c47a72a50b3a434783f82268fb4a96e636a1` |
| wave-1 spec/dispatch | `9c9d496b73cf066b02639dc54647934a0ba4297a` |
| harness fix landed mid-session (not mine, §7 F2) | `cb4326b2aa4c2024af0651fe6115b82d0c4de3df` — `round-38: harness fix (REA refuses existing extraction root; oracle mode unchanged)` |
| HEAD when the receipt was produced | `9c9d496b` (the fix landed at 03:19:01, after the after-run) |
| counter/carriers drift since freeze | `git diff --stat e059ca93 HEAD -- tools/round-38/c1-counter.py tools/round-38/c2-counter.py .ufo/waves/round-38/c1/carriers.json` → empty (0 lines); `tools/round-27/xpin-attribute.mjs` also unchanged |
| lane cleanliness | `git status --porcelain` → only untracked `.ufo/waves/round-38/{assimilation,w1.ready,w1/}`; no tracked modification from this seat |

## 2. Frozen inputs (verified, not assumed)

- Carrier: `corpus/evidence/round-37/c1/K4/carrier.bin`, 307 B.
  `sha256sum` → `a29ddc15f5a6abcabf28b7161837eb56b34111e48420e7392e648f2fdfe956ed`, **equal to the
  pin** in `.ufo/waves/round-38/c1/carriers.json:8`. Same value measured on the scratch copy used
  for the cross-check run. `carriers.json` bytes are identical at `e059ca93` and in the working
  tree (`sha256 be404a9d…` both).
- Oracle: `corpus/evidence/round-37/c1/K4/oracle.tsv`, 4 rows (`apple1..4.txt`, each 7 B);
  copy used for scoring kept as artifact `oracle.tsv.used`, `sha256 638a6f75…`.
- Extractor binaries on this host: `~/.local/bin/unblob` → uv-tool install,
  `unblob-26.6.4.dist-info`, `unblob --version` → `26.6.4`;
  `sasquatch-v4be` `sha256 fac88740f49b3460db6a67be93aa21e7390e2845b1e2f348265a95419b7214c6`,
  self-report `unsquashfs version 4.5.1 (2022/03/17)`; `sasquatch` `sha256 ad02d27a…` (matches the
  digest already recorded in `PROVINCE.md:372`). REA CLI: `npx -y rea-agents@6.5.0 --version` →
  `6.5.0`.

## 3. Runs — exact commands, exit codes, timestamps (all `-03:00`)

Scratch `S=/fast/scratch/hyaku/kaidoku-r38/R38ExecAfterK4`, `TMPDIR` under `$S`, removed at the end (§9).

| run | command (as executed) | start → end | exit |
|---|---|---|---|
| R0 (invalid) | REA with `$S/out` pre-created via `mkdir -p` | 03:17:10 → 03:17:12 | **1** — `{"code":"execution_failure",…,"diagnostics":{"reason":"Extraction output root already exists"}}` |
| **R1** (assigned literal form: scratch copy of the carrier) | `REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob npx -y rea-agents@6.5.0 extract-firmware --format json "$S/carrier.bin" "$S/out" > "$S/envelope.json"` | 03:17:21 → 03:17:23 | **0** |
| **R2** (canonical receipt; carrier path = committed lane file) | same, carrier `$L/corpus/evidence/round-37/c1/K4/carrier.bin`, outdir `$S/out-lane` | 03:17:48 → 03:17:50 | **0** |
| H1 (harness `after`, committed bytes at `9c9d496b`) | `bash tools/round-38/c1-run.sh after "$S/carrier.bin" "$S/hout" "$S/hscratch"` | 03:18 | **1** (see §7 F2) |
| H2 (harness `after`, post-fix bytes = `HEAD:tools/round-38/c1-run.sh`, blob `a95a1a9e…`, run from a pinned copy) | same on outdir `$S/hout2` | 03:19:10 → 03:19:12 | **0**, valid envelope |

**Canonical receipt = R2**, because its `subject.local_path` is the committed carrier path a
reader can re-open (the round-37 K3 receipt at `.ufo/waves/round-37/probes/rea-k3.json` uses the
same convention). R1 is kept as a cross-check; its `normalized_result` is identical to R2's
(path-insensitive comparison: equal chunk list, equal file list, equal gaps/coverage/bytes).
No `sasquatch`/`sasquatch-v4be` was added to `PATH` by me — but both were already in
`~/.local/bin` at session start; §7 F1 measures the consequence instead of asserting it.

## 4. Receipt verification (R2, every predicate field)

| check | observed |
|---|---|
| `subject.digest.sha256` == frozen pin | `a29ddc15f5a6abcabf28b7161837eb56b34111e48420e7392e648f2fdfe956ed` — **equal** |
| `subject.local_path` | `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-37/c1/K4/carrier.bin` |
| `operation` / `provider` | `extract_firmware` / `unblob` `26.6.4` |
| `normalized_result.chunks[].handler` | `["squashfs_v4_be"]` (single chunk) |
| `normalized_result.extraction_gaps` | `[]` |
| `normalized_result.coverage` / `published_bytes` | `complete` / `28` (= 4 × 7 B) |
| oracle hits (relative-path suffix + sha256, counter's `matched()` rule) | **4 / 4** — `apple1.txt 6181259c…`, `apple2.txt 919fc82d…`, `apple3.txt 2d95014e…`, `apple4.txt 08d9b05b…` (all under `firmware.bin_extract/`) |
| on-disk bytes re-hashed after the run | the four files' `sha256sum` equal the oracle rows; `cmp` against the committed `K4/apple{1..4}.txt` → identical (durable copy at `artifacts/…/extracted/firmware.bin_extract/`) |
| `evidence_id` recompute under the rea-agents 6.5.0 rule | `node tools/round-27/xpin-attribute.mjs --pkg65 … --pkg67 …` → stored `ev_3d1197d1126eaa4660a5e9e44c97c4185ad75bad716d8862a4d9154dce14abdd` == recomputed == recomputed-6.7 == `both`, exit 0 |
| determinism | R1 stored `ev_de83842f0a59d15165021fb191c481e5b16cd0fbf8e5a2ca3672b839fe123f30`, recomputes `both`; same `normalized_result` as R2 |

## 5. Counter integration check (read-only, in a scratch clone)

`git clone --shared` of the lane at `9c9d496b` into scratch, receipt placed at
`corpus/evidence/round-38/c1/K4/after.json`, one local commit `3442572d`, then
`python3 -I -B tools/round-38/c1-counter.py --root <clone> --rev 3442572d --freeze e059ca93… --pkg65 <rea-agents 6.5.0> --json-out …`
→ **exit 1** (correct: K1..K3 receipts absent), `carriers_matched = 1`, `carriers_unchanged = true`, and

```
"K4": {"after_present": true, "after_subject_ok": true, "after_operation_ok": true,
       "after_handler_ok": true, "after_gaps_empty": true, "after_oracle_hits": 4,
       "after_evidence_id_ok": true, "oracle_files": 4, "oracle_frozen": true, "matched": true}
```

Negative control in the same clone: replacing K4's `after.json` with the R0/§7 F1 gap envelope
(commit `d6640578`) → `after_gaps_empty false`, `after_oracle_hits 0`, `"matched": false`,
`carriers_matched = 0`, exit 1. So the receipt is required and sufficient for the K4 leg, and the
counter is not blind to a gap. Receipt copies: `artifacts/…/c1-sim-k4-only.json`.

## 6. Deliverable

`artifacts/R38ExecAfterK4/after.json` — byte-exact copy of R2's envelope (`cmp` clean),
`sha256 ca329ef33df933910350ed9c5d341b88397fd376e0d316051af3b6198a1d89cc`, 13 178 B, single line +
trailing newline (same framing as the committed `rea-k3.json`).

L1 action: `cp .ufo/waves/round-38/w1/artifacts/R38ExecAfterK4/after.json corpus/evidence/round-38/c1/K4/after.json`.

Other artifacts in the same directory (all `sha256`-listed in the shell transcript):

| file | sha256 |
|---|---|
| `after-scratchcopy-crosscheck.json` (R1) | `ccb7a92c36eb7ae1c9ba5c3ac73081855a30f42a7ba38b8f3c8893724dedd290` |
| `oracle.tsv.used` | `638a6f75579ae1ff508d3152723b1b9b279a90090e180cc63a2a6a758a477d23` |
| `extracted/firmware.bin_extract/apple{1..4}.txt` | the four oracle digests |
| `dep-probe/env-nosasq-gap.json` / `env-leonly-gap.json` / `env-v4beonly-ok.json` | `9c822f05…` / `44f14110…` / `837d31db…` |
| `c1-sim-k4-only.json` | `d79caa6a368500201717740ca981437882e01e4be69b9cc4aabbbacb96f789ac` |
| `harness-after-head9c9d496b-failure.json` | `d78ab7f71697688851a93f47f5d3730bb64604909d0b95a8381f9b29795d2475` |

## 7. Findings (reported, not repaired)

**F1 — HIGH, predicate prose is false: the BE v4 path has a hard external-extractor dependency.**
`plans/round-38-claims.md` says "(run with stock unblob 26.6.4; no external extractor dependency)"
and "measured probes … show the `squashfs_v4_be` handler publishing all oracle files without any
external extractor — the round-37 'missing-extractor-dependency' before-arm does not reproduce on
these carriers". The installed handler does the opposite:

- `unblob/handlers/filesystem/squashfs.py:26` `V4BE_EXECUTABLE = "sasquatch-v4be"`;
  `:41` `executable = self.V4BE_EXECUTABLE` for `Endian.BIG, 4` (and `:69` lists both binaries as
  `get_dependencies()`); `:65-66` builds `Command(executable, "-no-exit-code","-f","-d",…)`.
  There is no in-process BE v4 extractor.
- Measured dependency matrix (K4, same REA command, only `PATH` varied; envelopes in `dep-probe/`):

| `PATH` contents | exit | handler | gaps | files | published bytes |
|---|---|---|---|---|---|
| `~/.local/bin` (both binaries; R1/R2) | 0 | `squashfs_v4_be` | `[]` | 4 | 28 |
| only `sasquatch-v4be` | 0 | `squashfs_v4_be` | `[]` | 4 | 28 (`ev_bf11969e…`) |
| only `sasquatch` (LE) | **0** | `squashfs_v4_be` | `[{"kind":"missing-extractor-dependency","dependencies":["sasquatch-v4be"],…}]` | 0 | 0 |
| no sasquatch at all | **0** | `squashfs_v4_be` | same `missing-extractor-dependency` / `["sasquatch-v4be"]` | 0 | 0 |

So the round-37 before-arm **does** reproduce exactly when `sasquatch-v4be` is off `PATH`, and
`sasquatch` (LE) alone is not enough. Consequences for L1: (a) the predicate text must be corrected
at the next freeze to state the dependency (or the claim narrowed), since `PROVINCE.md:372` already
says unblob runs `sasquatch` from `PATH`; (b) the receipt's validity is host-dependent — the same
command on a host without `sasquatch-v4be` yields a gap-carrying envelope that the counter rejects;
(c) the killed/failed distinction in the claim narrative ("does not reproduce") should not be used.
The counter itself is unaffected (it *does* catch the gap, §5), so C1 can still be scored — it is
the prose that is wrong.

**F2 — MEDIUM, harness `after` mode was broken; already fixed by another seat, not mine.**
The `c1-run.sh` committed at `9c9d496b` did `mkdir -p "$OUT"` before invoking REA; REA 6.5.0
refuses an existing extraction root, so **every** harness `after` run failed:
H1 exit `1`, stdout = the `execution_failure` envelope with
`"diagnostics":{"reason":"Extraction output root already exists"}` (kept as
`harness-after-head9c9d496b-failure.json`), stderr empty. Commit `cb4326b2` (03:19:01,
`kaidoku-shokunin`) changed the line to `rm -rf "$OUT"  # REA refuses an existing extraction root`;
re-measured on those bytes (H2) → exit **0**, handler `squashfs_v4_be`, gaps `[]`, 4/4 oracle hits,
`evidence_id ev_7aacb79c0e864ca89eabb4fe303a8805e3e33ac110624fec8990b0856fa8d4e2`. My canonical
receipt was produced with the direct REA command, so it is unaffected.

**F3 — MEDIUM, C1's `frontier_note` binding is vacuous at the base.**
`tools/round-38/c1-counter.py:208` sets `frontier_note` from `any('big-endian' in l and
'superseded' in l …)` over all of `PROVINCE.md`, and `:236` makes it a required member of
`bind_ok`. Unmodified base text already satisfies it: `PROVINCE.md:157` reads
"[2026-10-26: superseded for LE SquashFS v4 — see `## Round-36 additions to Core`;
big-endian/AVM stays here.]". Measured: in the clone at rev `3442572d` (only my K4 receipt added,
no PROVINCE edit) the counter reports `"frontier_note": true`. A do-nothing PROVINCE therefore
passes that binding, so the frozen predicate cannot distinguish "the round-38 note supersedes the
big-endian Frontier bullet" from the round-36 note. The other bindings behaved as intended in the
same run (`province_core_section false`, `province_core_row false`, `entry_present false`,
`sourced false`, `coverage_map_row false`). Counter is frozen — report only.

**F4 — LOW, REA exit code 0 does not mean success.** With a gap the CLI exits `0` (F1 table, rows 3–4)
while publishing zero files. Any `set -e` harness (the frozen `c1-run.sh` included) will pass such
a run; receipts must be judged by `extraction_gaps`/`files` (the counter does that).

## 8. Limits / inference

- The canonical envelope embeds transient paths: `parameters.output_directory` and
  `raw_result.report[].task.path` point into `$S` (REA stages in `TMPDIR`), which is removed per the
  scratch rule. Durable evidence is `normalized_result` (relative paths + digests + the recomputing
  `evidence_id`) plus the digest-verified extracted tree copied into the artifacts directory.
  `[INFERENCE]` The counter is insensitive to these paths (it reads only relative_path/sha256, gaps,
  handler, subject digest and the id recompute); that is why a byte-identical re-run elsewhere yields
  a different `evidence_id` yet the same verdict.
- Only K4 was run; K1..K3 are other seats'. Nothing about AVM-BE, vendor-mangled images, or the
  extracted programs is claimed here. `unsquashfs` 4.7.5 was not used.
- Timestamps for the F1 `PATH` probes were not captured; their envelopes and digests are committed
  instead. Everything else in §3 is a captured timestamp.
- No tool was installed or upgraded in this seat (no pacman, no uv/npx install beyond the
  already-cached `npx -y rea-agents@6.5.0`); `sasquatch`/`sasquatch-v4be` were left untouched.

## 9. Scratch

`/fast/scratch/hyaku/kaidoku-r38/R38ExecAfterK4` (clone, envelopes, fixtures, counter temp) removed
before yielding; nothing cited here depends on it except the transient paths disclosed in §8.
