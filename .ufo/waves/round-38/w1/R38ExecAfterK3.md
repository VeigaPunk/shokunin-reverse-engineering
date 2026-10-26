# R38ExecAfterK3 — R38-C1 after-receipt for carrier K3

Seat: `R38ExecAfterK3` (leaf executor, wave 1). Lane root
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. L1 `KaidokuR38`.
Scope: produce the REA `extract-firmware` after-receipt for carrier **K3** and verify it against
the frozen predicate `P38-C1` and the frozen K3 oracle. No frozen material changed; no repair made.

## 0. Verdict first

**K3 as prescribed does not meet `P38-C1`.** The after-run names `squashfs_v4_be` and its
evidence id recomputes, but it publishes **0 of 4** oracle files and carries **1 extraction gap**
(`missing-extractor-dependency`, `dependencies=["sasquatch-v4be"]`).

Root cause is not the carrier, the oracle or the harness invocation: unblob 26.6.4's own SquashFS
handler **requires an external binary** for big-endian v4, and the frozen predicate explicitly
excludes one ("run with stock unblob 26.6.4; no external extractor dependency",
`plans/round-38-claims.md`, `tools/round-38/c1-counter.py:8-13`). With `sasquatch-v4be` reachable
the same carrier publishes 4/4 oracle files with zero gaps. So the frozen premise — the round-37
"corrected premise" that stock unblob handles standard BE v4 without any external extractor — is
**falsified**: the predicate's two clauses ("no gap" and "no external extractor dependency") cannot
both hold for a `squashfs_v4_be` carrier under unblob 26.6.4.

Reported, not repaired. Receipts below are the evidence; the arm choice and any premise re-freeze
belong to the L1 / closure.

Revision state while this seat ran: the carrier, oracle, `carriers.json` and both frozen counters are
byte-identical from freeze `e059ca93` through the new HEAD `cb4326b2`; the only lane change was the
L1's harness fix `cb4326b2` (§5), which post-dates the harness failure I measured.

## 1. Carrier and oracle pins (verified before the run)

| item | expected | observed | result |
|---|---|---|---|
| K3 carrier sha256 (frozen pin, `carriers.json`) | `9c7c523c5d1d1cafc0b679af9092ce0289d9656f6a24bc3bd0009f95b69397c0` | same, worktree and scratch copy | ok |
| K3 carrier at base `77091b49` (`git show`) | pin | `9c7c523c…397c0` | ok |
| K3 carrier at freeze `e059ca93` | pin | `9c7c523c…397c0` | ok |
| K3 carrier at HEAD `9c9d496b` | pin | `9c7c523c…397c0` | ok |
| K3 carrier at new HEAD `cb4326b2` | pin | `9c7c523c…397c0` | ok |
| `K3/oracle.tsv` freeze vs HEAD | identical | `638a6f75579ae1ff508d3152723b1b9b279a90090e180cc63a2a6a758a477d23` both | ok |
| `.ufo/waves/round-38/c1/carriers.json` freeze vs `cb4326b2` | identical | `be404a9dbc03dc4417df128d3f8c897cd8b6d27601195eec0ca56adaf9fe1be2` both | ok |
| `tools/round-38/c1-counter.py` freeze vs `cb4326b2` | identical | `a7a62b098709035607375078a12d2668bb6d36bbabfc5a7459f04d00a9516db8` both | ok |

Carrier: 4096 B, `Squashfs filesystem, big endian, version 4.0, zlib compressed, 307 bytes,
5 inodes` (unblob FileMagicReport in the envelope). Oracle: 4 rows (`apple1..4.txt`, 7 B each).

Tooling in the run (nothing installed or upgraded by this seat — both tools already present):

- `rea-agents 6.5.0`, package root `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`,
  invoked only as `npx -y rea-agents@6.5.0`.
- `unblob 26.6.4`, executable `/home/vgpnk/.local/share/uv/tools/unblob/bin/unblob`,
  sha256 `0ce7b624f540c2191ff144892584997fe3fb6ab28ab6ef6b88639f8a7cba1d09` (recorded in the
  envelope's `normalized_result.engine`).

## 2. Arm A — the prescribed after-run (claim receipt)

PATH was stripped of `/home/vgpnk/.local/bin` (where `sasquatch` and `sasquatch-v4be` live) so no
external extractor is reachable; `unblob` is supplied only through `REA_UNBLOB_COMMAND`. Verified
under that PATH: `command -v sasquatch` → not found, `command -v unblob` → not found.

```
S=/fast/scratch/hyaku/kaidoku-r38/R38ExecAfterK3
export TMPDIR="$S"
env PATH="$CLEANPATH" HOME="$HOME" TMPDIR="$S" \
  REA_UNBLOB_COMMAND="$HOME/.local/bin/unblob" \
  npx -y rea-agents@6.5.0 extract-firmware --format json "$S/carrier.bin" "$S/out" \
  > "$S/envelope.json" 2> "$S/envelope.err"
```

| fact | value |
|---|---|
| exit code | **0** (stdout is the envelope; stderr 0 B) |
| start / end (UTC) | 2026-10-26T06:17:24Z → 2026-10-26T06:17:26Z (mtime 03:17:26.065 -03:00) |
| envelope bytes | 7919 |
| envelope sha256 | `dcdfb776e8de46f46717a694776a6de16f9ed8357e4b85a38adac911ecdf16dd` |
| `subject.digest.sha256` | `9c7c523c…397c0` (matches the frozen pin) |
| `provider` / `operation` | `unblob` 26.6.4 / `extract_firmware` |
| `normalized_result.chunks[0].handler` | `squashfs_v4_be` |
| `chunks[0].extraction_failed` | `true` |
| `normalized_result.coverage` | `partial` |
| `normalized_result.files` | `[]` (0 files, `published_bytes` 0) |
| `normalized_result.extraction_gaps` | 1: `kind=missing-extractor-dependency`, `handler=squashfs_v4_be`, `dependencies=["sasquatch-v4be"]` |
| `normalized_result.diagnostics` | `ExtractorDependencyNotFoundReport`, severity ERROR, `missing_dependencies=["sasquatch-v4be"]` |
| continuation | `4ca863d0…a07a`: "REA installs nothing. Add the named dependency to your own environment and rerun extract_firmware on the same immutable input with a fresh output_directory…" |
| oracle rows matched | **0 / 4** |
| evidence id | `ev_bb5d941f43f9362d9f74379bdd90003621bd752620177622d3555240b5b8a79c`, recomputes (see §4) |

Mapped onto the counter's K3 bindings (`tools/round-38/c1-counter.py:174-191`):
`after_subject_ok` ✓, `after_operation_ok` ✓, `after_handler_ok` ✓, `after_evidence_id_ok` ✓,
`after_gaps_empty` ✗, `after_oracle_hits` = 0 ≠ 4 ✗ → `matched` false for K3, so
`carriers_matched` cannot reach 4.

Artifact (byte-identical to the scratch envelope, `cmp` clean):
`.ufo/waves/round-38/w1/artifacts/R38ExecAfterK3/after.json`
(`sha256 dcdfb776e8de46f46717a694776a6de16f9ed8357e4b85a38adac911ecdf16dd`).

Note on texture: the envelope carries the scratch `local_path` / `output_directory` of the real run;
the id recomputes from that content, and the counter's identity checks are `subject.digest` plus the
recomputed id, both of which hold, so the only counter bindings this receipt fails are
`after_gaps_empty` and `after_oracle_hits`. Nothing was written into `corpus/evidence/round-38/`.

## 3. Arms B and C — diagnostics isolating the cause (not claim receipts)

Arm B: same carrier, same REA, same unblob, ambient PATH (i.e. `sasquatch-v4be` present in
`~/.local/bin`).

```
REA_UNBLOB_COMMAND="$HOME/.local/bin/unblob" npx -y rea-agents@6.5.0 extract-firmware \
  --format json "$S/carrier.bin" "$S/out-dep" > "$S/envelope.dep.json"
```
exit 0, 06:18:12Z→06:18:15Z, 12916 B, sha256
`4d58f37bbb9a6b8dba7aae92ab57a7da1fabbd562bea0170a37080b7f335be3a`,
evidence id `ev_096b500d37e879c18ac63d856ac5a9998693ad2e048431c297876e45dc6337ed` (recomputes).
`handler=squashfs_v4_be`, `extraction_failed=false`, `coverage=complete`, `gaps=[]`,
`published_bytes=28`, 4 files, **4/4 oracle rows matched** (suffix + sha256), and the on-disk tree
`firmware.bin_extract/apple{1..4}.txt` hashes equal `oracle.tsv`.

Arm C: clean PATH plus a shim directory exposing **only** `sasquatch-v4be` (symlink to
`~/.local/bin/sasquatch-v4be`), to rule out any other `~/.local/bin` tool.
exit 0, mtime 03:18:34 -03:00, 12922 B, sha256
`822a093ad15fde595fa87328fc50cbeb8ca4ba4bf5a72658bd42cd17298b46e9`,
evidence id `ev_bcff413fd14c5d08676320797628dada11673837c22d5964fb3726a46181c12e` (recomputes),
`coverage=complete`, 4 files, `gaps=[]`, handler `squashfs_v4_be`.

Arm C pins the causal factor to exactly one binary. Arm A vs arm B/C differ in nothing else (same
carrier bytes, same REA package, same unblob executable sha256, same parameters).

Cross-tool check (harness `oracle` mode, `sasquatch-v4be -be` directly): exit 0, 4 rows,
byte-for-byte equal to the frozen `K3/oracle.tsv` (path+sha256+size). So carrier and oracle are
sound; the only missing piece is the extractor unblob requires.

Artifacts:
`diagnostic-after-with-declared-extractor.json` (B),
`diagnostic-after-shim-only-extractor.json` (C).

## 4. Why arm A is expected, from unblob's own source

`/home/vgpnk/.local/share/uv/tools/unblob/lib/python3.13/site-packages/unblob/handlers/filesystem/squashfs.py`:

```
24: class SquashFSExtractor(Extractor):
25:     EXECUTABLE = "sasquatch"
26:     V4BE_EXECUTABLE = "sasquatch-v4be"
...
34:         match endian, self.version:
35:             case Endian.BIG, 4:
36:                 executable = self.V4BE_EXECUTABLE
...
59:     def get_dependencies(self) -> list[str]:
60:         return [self.EXECUTABLE, self.V4BE_EXECUTABLE]
```

Everything on the BE-v4 path is delegated to the external `sasquatch-v4be` process (`-be` unless
the AVM heuristic `bytes_used == mkfs_time` fires); unblob 26.6.4 contains no in-process BE v4
decoder. Hence REA reports the gap, and `published_bytes=0`. [INFERENCE] the same handler and the
same declared dependency apply to K1, K2 and K4, so a clean-PATH after-run for those carriers
should fail identically; their seats measure it, this seat did not run them.

Evidence-id recomputation under the frozen rule (`tools/round-27/xpin-attribute.mjs`, pkg65 =
`/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`), same wrapper the counter uses:

```
armA.wrapped.json  ev_bb5d94…a79c  ev_bb5d94…a79c  ev_bb5d94…a79c  both
armB.wrapped.json  ev_096b50…37ed  ev_096b50…37ed  ev_096b50…37ed  both
armC.wrapped.json  ev_bcff41…c12e  ev_bcff41…c12e  ev_bcff41…c12e  both
```
exit 0, stored = recomputed for all three (the receipts are structurally valid; the only failing
axis for K3 is gaps/output).

## 5. Second, independent defect: the freeze-time harness `after` mode could not succeed (now fixed by the L1)

At freeze `e059ca93` and still at wave-1 dispatch `9c9d496b`, `tools/round-38/c1-run.sh` lines 25-28:

```
  after)
    : "${REA_UNBLOB_COMMAND:?set REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob}"
    mkdir -p "$OUT"
    npx -y rea-agents@6.5.0 extract-firmware --format json "$CARRIER" "$OUT"
```

REA requires the output root **not to exist**: `dist/artifacts/SafeOutputTree.js:56-58` calls
`mkdir(canonicalOutput, {mode:0o700})` (non-recursive) and turns `EEXIST` into
`ArtifactReaderFailure("path", "Extraction output root already exists")`. So that harness's own
`mkdir -p "$OUT"` made every `after` invocation exit 1 — including on an empty directory, which I
confirmed as my first attempt (same 526-byte error envelope, sha256
`d78ab7f71697688851a93f47f5d3730bb64604909d0b95a8381f9b29795d2475`, artifact
`rea-outdir-preexisting-error.json`). Reproducing the harness verbatim at `9c9d496b`:

```
$ bash tools/round-38/c1-run.sh after "$S/carrier.bin" "$S/out-harness" "$S/harness-scratch"
exit 1
{"code":"execution_failure", … "details":{"provider_id":"unblob","operation":"extract_firmware",
 "diagnostics":{"reason":"Extraction output root already exists"}}}
```

Artifact `harness-after-mode-failure.txt` (rewritten with the exact revision it was measured at and
the exit code). **Repo change during this seat (not mine):** while this seat was running, the L1
committed `cb4326b2` "round-38: harness fix (REA refuses existing extraction root; oracle mode
unchanged)" at 03:19:01 -03:00, replacing that line with `rm -rf "$OUT"  # REA refuses an existing
extraction root; it creates $OUT itself`. I re-read the file after the change and re-ran the fixed
harness once as a check: exit 0, 13303 B envelope, handler `squashfs_v4_be`, 4 files, 0 gaps,
`coverage=complete`, evidence id `ev_fbc3be2e963cf8670367b207ce6ee901462abe5e4aa1c33dc54e30227b4412ae`
(artifact `harness-after-mode-post-fix-ok.json`, run 06:20:24Z→06:20:26Z). That run had the ambient
PATH, i.e. `sasquatch-v4be` reachable — under a clean PATH the harness would report the §2 gap.

The receipts in §2-§3 were produced by invoking `npx -y rea-agents@6.5.0` directly with a non-existent
`out` path (identical to what the fixed harness runs). I did not touch the harness.

## 6. What the L1 has to decide (no action taken here)

1. K3's honest receipt under the frozen wording is the failing one (`after.json`, gap + 0/4). Landing
   it makes `carriers_matched < 4`; with `P38-C1`'s kill rule ("the counter, predicate, carriers and
   oracle are never changed after this commit") that reads as an honest stop for C1 unless the
   premise line is treated as a separate, reviewable defect.
2. The premise in `plans/round-38-claims.md` ("stock unblob handles standard BE v4; … the round-37
   'missing-extractor-dependency' before-arm does not reproduce on these carriers") is false as
   measured: it reproduced on K3 the moment the dependency was removed from PATH. The round-37 probe
   `ev_3c3bf52c…61fa` published 4 files because `sasquatch-v4be` was on the ambient PATH, not because
   unblob carries a BE v4 decoder.
3. If the L1 wants a passing receipt, it needs a predicate wording the extractor dependency admits
   (e.g. "stock unblob 26.6.4 **plus its declared extractor** `sasquatch-v4be`"); that is a
   re-freeze decision above this seat. Arms B/C show exactly what such a receipt looks like.
4. Harness `after` mode: already fixed in `cb4326b2` (was `mkdir -p "$OUT"`, now `rm -rf "$OUT"`);
   verified post-fix at exit 0 (§5). Nothing further needed there, but any receipt cited from the
   freeze commit `e059ca93`/`9c9d496b` harness would be an `execution_failure` envelope.

## 7. Limits

- Only K3 was measured. K1/K2/K4 untouched; §4's generalisation is `[INFERENCE]`.
- Only standard BE v4 was in scope; no AVM-BE, no vendor-mangled images, no claim about extracted
  programs.
- Arm A's PATH exclusion was done by filtering `/home/vgpnk/.local/bin`; `unblob` itself was passed
  by absolute path, so unblob's own dependency lookup still saw a PATH without `sasquatch*`.
- Nothing installed or upgraded (`npx` used from the existing cache; no pacman, no uv, no cargo).
- The lane moved under this seat once (L1 harness fix `cb4326b2`, 03:19:01 -03:00). I re-read the
  harness before re-running it; the pins in §1 were re-verified at the new HEAD.
- Scratch `/fast/scratch/hyaku/kaidoku-r38/R38ExecAfterK3` removed at the end of the seat; every
  cited byte is copied under `.ufo/waves/round-38/w1/artifacts/R38ExecAfterK3/`.

## 8. Artifacts (all under `.ufo/waves/round-38/w1/artifacts/R38ExecAfterK3/`)

| file | sha256 | what |
|---|---|---|
| `after.json` | `dcdfb776e8de46f46717a694776a6de16f9ed8357e4b85a38adac911ecdf16dd` | arm A envelope, byte-exact, the prescribed K3 claim receipt (gap, 0/4) |
| `diagnostic-after-with-declared-extractor.json` | `4d58f37bbb9a6b8dba7aae92ab57a7da1fabbd562bea0170a37080b7f335be3a` | arm B: 4/4, no gap, `sasquatch-v4be` on PATH |
| `diagnostic-after-shim-only-extractor.json` | `822a093ad15fde595fa87328fc50cbeb8ca4ba4bf5a72658bd42cd17298b46e9` | arm C: 4/4, no gap, only `sasquatch-v4be` exposed |
| `rea-outdir-preexisting-error.json` | `d78ab7f71697688851a93f47f5d3730bb64604909d0b95a8381f9b29795d2475` | REA `execution_failure` when the output root pre-exists |
| `harness-after-mode-failure.txt` | `da5e7d893655ff273dc3210f44c58a2e5d24d2d630e0d7c2d2b1c03538de02d6` | harness `after` mode at `9c9d496b`, exit 1, exact argv/exit/stdout |
| `harness-after-mode-post-fix-ok.json` | `0c670a0640ed2af00f64ac644c85f4918a30fdbc43bb3cad1fa991d1e615c5f7` | harness `after` mode at `cb4326b2` (fixed), exit 0, 4 files, 0 gaps |
| `harness-after-mode-post-fix-note.txt` | `b2856ae57143d211cd67cee47e9b4f75e3ef37f504aa276a5732b9c4781dcbf2` | the post-fix run's facts and the ambient-PATH caveat |

No file outside this report and that artifacts directory was written.
