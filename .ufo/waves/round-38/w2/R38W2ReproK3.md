# R38W2ReproK3 — independent re-run of the committed K3 C1 receipts

**Verdict: CONFIRMED — the committed K3 `before.json`/`after.json` semantic payloads reproduce
exactly under a non-author re-run (payload-identical; full envelope byte-identical after
normalizing scratch staging paths, `output_directory`, provider blob ids, `evidence_id` and
`subject.local_path`). One predicate-premise defect remains, measured here and already reported
by wave 1: reproducing either arm requires the external `sasquatch-v4be` 4.5.1 binary on `PATH`,
so the frozen predicate's "(run with stock unblob 26.6.4; no external extractor dependency)" and
the claims file's "the round-37 missing-extractor-dependency before-arm does not reproduce"
note are false. No receipt defect; the receipts themselves are reproducible bytes.**

Seat: leaf, advisory. No file in the lane was written except this report and
`.ufo/waves/round-38/w2/artifacts/R38W2ReproK3/`. No VCS mutation. No tool installs.

## 1. Artifact and tool identity

| item | value |
|---|---|
| carrier named for K3 (`c1/carriers.json`) | `corpus/evidence/round-37/c1/K3/carrier.bin` |
| carrier sha256 (required pin) | `9c7c523c5d1d1cafc0b679af9092ce0289d9656f6a24bc3bd0009f95b69397c0` — **matches** the copied scratch file, and the committed bytes at base `77091b49`, freeze `e059ca93`, landing `3b960fe5` (all three identical) |
| receipts under test | `corpus/evidence/round-38/c1/K3/{before,after}.json`; working-tree bytes equal the blobs at `3b960fe5` (`before` 45e2df5d…, `after` 09d5b85b…) |
| REA | `npx -y rea-agents@6.5.0`; package root `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`, `package.json` sha256 `a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c`, version 6.5.0 |
| unblob | 26.6.4 at `/home/vgpnk/.local/share/uv/tools/unblob/bin/unblob`, executable sha256 `0ce7b624f540c2191ff144892584997fe3fb6ab28ab6ef6b88639f8a7cba1d09` (same value recorded in both committed receipts and in every fresh envelope) |
| external extractor | `sasquatch-v4be` 4.5.1 at `~/.local/bin/sasquatch-v4be`, sha256 `fac88740f49b3460db6a67be93aa21e7390e2845b1e2f348265a95419b7214c6`; `type -a` resolves exactly one such binary on `PATH` |
| scratch | `/fast/scratch/hyaku/kaidoku-r38/R38W2ReproK3` (removed at end; everything cited here is in the artifacts dir) |

## 2. Commands and exit codes

All runs used `REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob` (absolute, never resolved through the
stripped PATH). "strip" = `$PATH` minus the literal entry `$HOME/.local/bin` (verified with
`env -i PATH=<stripped> sh -c 'command -v sasquatch-v4be'` → not found).

```
# v1 arms: scratch copy of the carrier as input
env PATH=<stripped> REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob \
  npx -y rea-agents@6.5.0 extract-firmware --format json $S/in/carrier.bin $S/out-before \
  > env-before.json                                  # CLI rc=0, 7919 B, envelope emitted
env PATH=<default> REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob \
  npx -y rea-agents@6.5.0 extract-firmware --format json $S/in/carrier.bin $S/out-after \
  > env-after.json                                   # CLI rc=0, 12876 B

# v2 arms: the committed lane carrier path as input (same `parameters.path` as the receipts)
env PATH=<stripped> REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob ... K3/carrier.bin $S/out2-before
                                                     # CLI rc=0, 7981 B
env PATH=<default>   REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob ... K3/carrier.bin $S/out2-after
                                                     # CLI rc=0, 12102 B

# direct unblob probes (unblob invoked by absolute path)
unblob --process-num 1 --depth 3 --extract-dir … --report … --log … <carrier>   # per carrier below
```

Recorded inner processes (from each envelope's `raw_result.execution`):

| arm | unblob child exit | matches committed receipt |
|---|---|---|
| before v1 / v2 | **1** | committed before `execution.exit_code = 1` |
| after v1 / v2 | **0** | committed after `execution.exit_code = 0` |

## 3. Semantic payload comparison (committed vs fresh)

Normalization for payload equality: drop `normalized_result.output_directory`; drop
`chunks[].provider_id`, `extraction_gaps[].provider_id`, `derivations[].provider_blob_id`,
`files[].path`. Full-envelope scrub additionally replaces REA/unblob staging dirs, `\d+:\d+`
blob ids, `evidence_id`, `subject.local_path`.

| arm | payload equal | full envelope equal (scrubbed) |
|---|---|---|
| before, v1 (scratch input) | **yes** | no — sole difference `parameters.path` (scratch copy vs lane path) |
| after, v1 (scratch input) | **yes** | no — sole difference `parameters.path` |
| before, v2 (lane path input) | **yes** | **yes** (6693 B canonical JSON both sides) |
| after, v2 (lane path input) | **yes** | **yes** (10425 B canonical JSON both sides) |

Field-by-field, committed and fresh agree on every element the seat was asked to compare:

* **chunk handler**: `squashfs_v4_be`, `encrypted: false`; chunk `range` `{offset:0,length:4096}`,
  `root_file_range` identical; `extraction_failed=false` (after) / `true` (before). Before-arm
  `continuation_id` `4ca863d04cc06d61e7be38d0811847a15f55c70f028fdf45e8fefdf75957a07a` reproduces
  byte-identically.
* **`normalized_result.files`** (after): 4 entries, `(relative_path, sha256)` set equal —
  `firmware.bin_extract/apple{1..4}.txt` with the four committed oracle hashes,
  `size=7`, `reported_sha256 == sha256`, `mime_type=text/plain`, `analysis_depth=1`.
* **`extraction_gaps`**: after = `[]`; before = exactly one
  `{"kind":"missing-extractor-dependency", "handler":"squashfs_v4_be",
  "dependencies":["sasquatch-v4be"], "input_path":"$input", "relative_path":null,
  "range"/"root_file_range":{0,4096}}`; `unpublished_entries = []` in both.
* **`coverage`**: `complete` (after) / `partial` (before); `published_bytes` 28 / 0;
  `diagnostics` `[]` / one `ExtractorDependencyNotFoundReport{"dependencies":["sasquatch-v4be"]}`.
* **`derivations`** (after): 5 entries (`$input → $output/firmware.bin_extract` with handler
  `squashfs_v4_be` and `parent_file_range {0,4096}`, plus 4 child files), identical.
* **`selection`**: `{offset:0, length:4096, sha256:9c7c523c…}` in both.
* **`engine`**: name/version/executable_path/executable_sha256/worker_count identical.
* **`parameters`** modulo `output_directory`: identical (`max_depth 3`, `max_output_bytes
  268435456`, `max_output_files 10000`, same `path` in the v2 arms).
* **`raw_result.report`** (1 entry before, 6 after): identical after normalizing staging paths
  and blob ids, including the squashfs magic string
  ("Squashfs filesystem, big endian, version 4.0, zlib compressed, 307 bytes, 5 inodes,
  blocksize: 131072 bytes, created: Wed Mar  2 12:07:37 2022") and all file hash/magic reports.

**Differences found in the semantic payload: none.** The only byte differences anywhere are the
volatile fields named above.

## 4. Oracle cross-check and evidence-id recompute

`corpus/evidence/round-37/c1/K3/oracle.tsv` (4 rows) vs receipt files, matching by relative-path
suffix **and** size:

| source | equal to oracle | only-oracle | only-receipt |
|---|---|---|---|
| committed `after.json` | yes | — | — |
| fresh after v1 | yes | — | — |
| fresh after v2 | yes | — | — |

On-disk bytes of my v2 extraction dir are exactly `b'apple1\n' … b'apple4\n'` (7 B each), hashes
equal to the oracle.

Evidence-id recompute, done independently of `tools/round-27/xpin-attribute.mjs` by importing the
6.5.0 package's own `dist/domain/canonicalDigest.js#digestCanonicalValue` and evaluating the
package's own `const semanticProjection` statement from `dist/domain/evidence.js`
(id = `ev_` + digest of the projection): stored id **matches** the recomputed id for all six
envelopes — committed `before` `ev_18d7d6ef…341ed2`, committed `after` `ev_e31cb700…0fcaa66`,
and each fresh envelope recomputes to its own id.

Reading of that clause (rederived from the package, see `evidence-id-rule.txt`): the projection
includes `parameters`, `raw_result` and `normalized_result` **verbatim**, i.e. the run's
`output_directory`, staging paths, argv and provider blob ids. The id therefore authenticates the
stored record against tampering (self-recompute) and is not a cross-run payload fingerprint:
(a) swapping the fresh v2 record's `output_directory` for the committed one still yields
`ev_d0c1051d…`, (b) additionally copying the committed `provider_id`/`provider_blob_id`
values still yields `ev_f1b06663…`, never the committed id. Cross-run id equality is thus neither
achievable nor required by the predicate; the payload comparison in §3 is the provenance check.

## 5. Premise defect independently confirmed (already reported by wave 1)

Running the *same* unblob with the same command line but with `sasquatch-v4be` unreachable
reproduces the committed before-arm gap exactly — for **all four** carriers, not just K3:

| probe (unblob 26.6.4, absolute path, stripped PATH) | exit | regular files | dependency report |
|---|---|---|---|
| K3 `carrier.bin` | 1 | 0 | `Can't run extract command … dependencies=['sasquatch-v4be']` |
| K1 `carrier.sqsh` | 1 | 0 | same |
| K2 `carrier.sqsh` | 1 | 0 | same |
| K4 `carrier.bin` | 1 | 0 | same |
| K3, default PATH | 0 | 4 | log: `command='sasquatch-v4be -be -no-exit-code -f -d …/carrier.bin_extract …/carrier.bin'` |

Installed handler source (`…/site-packages/unblob/handlers/filesystem/squashfs.py:24-26,34-36,59-60`)
selects `V4BE_EXECUTABLE = "sasquatch-v4be"` for big-endian v4 and `get_dependencies()` returns
both `sasquatch` and `sasquatch-v4be`; unblob 26.6.4 has no in-process BE v4 decoder. Consequences:

* `plans/round-38-claims.md` (first freeze `e059ca93`, "Not claimed" paragraph: "stock unblob
  handles standard BE v4 … the round-37 'missing-extractor-dependency' before-arm does not
  reproduce on these carriers and is reported as a corrected premise") is **false for K3 and for
  K1/K2/K4**: the gap reproduces deterministically, and the before-receipt it is contradicted by
  is the very file committed beside it.
* The frozen predicate's "(run with stock unblob 26.6.4; no external extractor dependency)" is
  unattainable as worded: every oracle-publishing after-run necessarily had the external
  `sasquatch-v4be` on `PATH`. This does not change the author verdict (K2's `unpublished-entry`
  gap is the honest-stop reason), but the predicate as frozen cannot be satisfied literally.
* The landed knowledge entry (`corpus/knowledge/2026-10-26-r38-sasquatch-be-squashfs-recursion.md`,
  "**Why the dependency is structural**", "Status") already states this correctly and records the
  before-arm table, so the attempt-2 prose repair is real; only the frozen claim file and counter
  docstring still carry the false parenthetical and cannot be edited post-freeze.

## 6. Calibration notes (advisory)

1. **Receipts record no environment.** `environment` is `null` in both committed receipts, and
   unblob's `report.json` carries no extractor command (only the log does). The receipt therefore
   cannot disclose that an external `sasquatch-v4be` produced its files, nor which build.
   Reproduction proves an oracle-correct payload, not that the identical extractor binary ran;
   that step is `[INFERENCE]` (exactly one `sasquatch-v4be` resolves on `PATH` on this host, and my two independent
   arms plus the author's receipt agree byte-for-byte).
2. **K3 and K4 oracles are byte-identical** (`cmp` of the two `oracle.tsv` files is empty; same
   four `apple{1..4}.txt` hashes). The four-carrier set therefore carries two identical payload
   oracles; K3/K4 are distinguished only by carrier digest (`9c7c523c…` vs `a29ddc15…`) and chunk
   range (4096 vs 307). A swap of the K3/K4 `normalized_result.files` blocks would not be
   detectable through the oracle dimension — a distinctness blind spot of the frozen design, not
   of these receipts (subject digest and chunk range do differ today, as committed).
3. `before.json` is supplementary: the predicate does not require it, and it is not part of the
   matched count. Its value is exactly the premise evidence in §5.

## 7. Limits

* One non-author seat, one host, x86_64 Linux; two arms plus the two v2 arms; not a second
  machine. Determinism of the REA/unblob stack on this carrier is shown by four agreement points
  (author receipt + v1 + v2 + direct-unblob payload).
* The after-arm was run with the default ambient `PATH` (as instructed) which contains
  `~/.local/bin`; the before-arm stripped exactly that directory and nothing else. I did not try
  to isolate any other `~/.local/bin` binary in the after-arm beyond the wave-1 shim experiment.
* REA refuses pre-existing output dirs; every run used a fresh directory, so `output_directory`
  necessarily differs from the committed receipt. That field alone changes the evidence id, which
  is why id equality is asserted as "each stored id recomputes", not "same id" (§4).
* No claim is made here about K1/K2/K4 receipt payloads beyond the dependency probe in §5; their
  seats own that comparison.

## 8. Files changed (this seat only)

* `.ufo/waves/round-38/w2/R38W2ReproK3.md` (this report)
* `.ufo/waves/round-38/w2/artifacts/R38W2ReproK3/` — `env-before.json`, `env-after.json`
  (v1 arms), `env2-before.json`, `env2-after.json` (v2 arms), `payload-diff.txt`,
  `oracle-check.txt`, `id-recompute.txt`, `evidence-id-rule.txt`, `dependency-probes.txt`,
  `MANIFEST.sha256` (`59a924a6…`, `dfb409c7…`, `ba8d9c49…`, `4affdab1…`, `c726c305…`,
  `1d3e2606…`, `93fb8050…`, `31e4a911…`, `d16e4ec6…` in manifest order).

Nothing under `corpus/`, `PROVINCE.md`, `SCORECARD.md`, `SHONEN.md`, `LOG.md`, `tools/`, and
nothing outside the lane, was written. Scratch `/fast/scratch/hyaku/kaidoku-r38/R38W2ReproK3`
was removed.

## 9. Tooling performed

No installs, no upgrades. `npx -y rea-agents@6.5.0` resolved from the existing npm cache
(version 6.5.0 confirmed from `package.json`); `unblob` 26.6.4 and `sasquatch-v4be` 4.5.1 were
used as found in `~/.local/bin` and the uv tool tree; no pacman/uv/npm install transaction ran.

## 10. Blockers / risks

None blocking. The residual risk is interpretive: if the L1 reads the predicate parenthetical as
"the receipt declares no missing dependency" rather than "no external extractor is involved", the
§5 defect is moot; as worded, and as the claims file's own "corrected premise" sentence states it,
it is false and is reproducible with one command per carrier.
