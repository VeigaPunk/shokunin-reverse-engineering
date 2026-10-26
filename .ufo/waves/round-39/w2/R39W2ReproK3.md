# R39W2ReproK3 — independent re-run provenance attack on R39-C1 / carrier K3

**Verdict: CONFIRMED** — every semantic field of the committed `corpus/evidence/round-39/c1/K3/after.json` reproduces from an independent `rea-agents@6.5.0 extract-firmware` run on the pinned carrier; the 47 differing leaves are all absolute paths, the non-deterministic unblob blob handle, or the evidence digest derived from them. No fabricated field, no oracle divergence, no receipt/run.json internal inconsistency.

## Target and pins (all verified read-only)

| item | value | check |
|---|---|---|
| freeze | `8fcda41c96cbf00b113d2c8e136cc14e7fcaba0b` | `git show -s --format=%cI` → `2026-10-26T14:12:51-03:00` = `17:12:51Z` (committer) |
| receipt commit | `6fdaf4f162aff156fcef0e52998a5469c64fd6f0` | committer `2026-10-26T14:18:32-03:00` = `17:18:32Z` |
| carrier | `corpus/evidence/round-37/c1/K3/carrier.bin` | `sha256 9c7c523c5d1d1cafc0b679af9092ce0289d9656f6a24bc3bd0009f95b69397c0`, 4096 B — matches `carriers.json` and `git cat-file -p 8fcda41c:…/carrier.bin` |
| oracle | `corpus/evidence/round-37/c1/K3/oracle.tsv` | `sha256 638a6f75…`, 4 rows; unchanged at freeze |
| symlinks | `corpus/evidence/round-39/c1/K3/symlinks.tsv` | 0 B, `e3b0c442…`; unchanged at freeze |
| carriers.json | `.ufo/waves/round-39/c1/carriers.json` | `df9eb8a6…` ≡ `git show 8fcda41c:…`; `git status --porcelain` on `.ufo/waves/round-39/c1`, `corpus/evidence/round-39`, `corpus/evidence/round-37`, `tools/round-39` → empty |
| tools | unblob `26.6.4` `0ce7b624…`; sasquatch-v4be `4.5.1` `fac88740…`; rea-agents `6.5.0` at `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents` | identical to the values recorded in `run.json` |

Scratch: `S=/fast/scratch/hyaku/kaidoku-r39/R39W2ReproK3` (`mkdir -p`; TMPDIR/`HYAKU_SCRATCH` set; removed at the end). No installs, no upgrades — nothing to record under the tooling directive.

## Commands (exact)

```
cp corpus/evidence/round-37/c1/K3/carrier.bin "$S/carrier.bin"          # sha256 9c7c523c…, 4096 B
cd "$S" && REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob \
  npx -y rea-agents@6.5.0 extract-firmware --format json --full-output \
  "$S/carrier.bin" "$S/out" > "$S/rea.stdout.json"            # exit 0, stderr 0 B, 12054 B envelope
cd "$S" && ~/.local/bin/sasquatch-v4be -be -no-exit-code -f -d "$S/x" "$S/carrier.bin"
                                                                        # exit 0, 4 files, 1 dir, 0 symlinks
```
A second REA run into `$S/out2` (same command, different outdir) was used only to measure field determinism.

## 1. Semantic comparison vs the committed receipt

Author envelope `after.json` = 13140 B, `sha256 dade9766…` (equals `run.json.receipt.sha256`). Compared against my envelope's `data` object, leaf-by-leaf (`raw_result`, `normalized_result`, envelope level):

* chunk handlers: `["squashfs_v4_be"]` both; `extraction_failed: [false]` both; `range/root_file_range {offset 0, length 4096}` both; `encrypted false`
* `normalized_result.files`: 4 entries; `(relative_path, sha256)` set **identical**, and the full records (minus `path`) identical — `analysis_depth 1`, `mime_type text/plain`, `size 7`, `reported_sha256 == sha256`
* `extraction_gaps`: `[]` both (`(kind, relative_path)` set equal, empty)
* `unpublished_entries`: `[]` both (`(relative_path, link_target)` set equal, empty)
* `diagnostics`: `[]` both — `__typename__` set equal (empty) in `normalized_result.diagnostics` and in `raw_result.report` the multiset is identical: `{StatReport 6, FileMagicReport 5, HashReport 5, ChunkReport 1}`, same per-task depth shape (5×depth 1 with 4 subtasks on the directory, 1×depth 0 root)
* `coverage complete`, `published_bytes 28`, `depth_limited_paths []`, `extraction_continuations []`, `derivations` (5 rows: dir←handler, 4 files←none) equal after path normalization
* `selection {0,4096,9c7c523c…}`, `subject.digest/format/architecture`, `provider {unblob,Unblob,26.6.4}`, `engine {unblob,26.6.4,executable_sha256 0ce7b624…,worker_count 1}`, `parameters {max_depth 3, max_output_bytes 268435456, max_output_files 10000}`, `confidence observed`, `authority shipped-artifact`, `limitations` (5 strings, byte-equal), `locations [{file-offset-range 0..4096}]`, `evidence_links []`
* `raw_result.execution`: `exit_code 0`, `signal null`, `command = /home/vgpnk/.local/share/uv/tools/unblob/bin/unblob`, `resource_limiter /usr/bin/prlimit`, stderr 0 B both; `version_execution` stdout `26.6.4` both; stdout summary text identical

**Every differing leaf (mechanical enumeration, `diff-leaves.txt`): 47 total**

| count | class |
|---|---|
| 25 | absolute paths (`subject.local_path`, `parameters.path/output_directory`, `files[].path`, `derivations[].child_path` root, `report[].task.path`, `report[].subtasks[].path`, `output_directory`, 4× REA staging tmpdir `args[7,9,11,12]`) |
| 16 | unblob blob handle `2779683:1` vs `166849:1` (`chunks[].provider_id`, `derivations[].provider_blob_id`, `report[].task.blob_id`, `subtasks[].blob_id`, `ChunkReport.id`) — **non-deterministic, see §4** |
| 1 | derived `evidence_id` (digest over the paths + blob ids above) |

No semantic leaf differs.

## 2. Envelope digest closed by reconstruction

`run.json.envelope = {parseable true, ok true, sha256 53f460dcaf2bff90ede9ae0edd89d3987123ea548f5f4cc6a61077f3543163b4, bytes 13217}`. The envelope was not kept (`C1_KEEP_ENVELOPE` unset; `previous_after_json_sha256: null`), so I rebuilt it from the receipt using the writer's measured format (`c1-run.sh:295` `jq -c '.data'`; verified on my own run: `jq -c .data` output == raw `data` substring + `\n`, byte-identical):

```
{"ok":true,"data":<after.json minus trailing newline>,"meta":{"command":"extract-firmware","duration":"2411ms"}}\n
```

→ 18 + 13139 + 60 = **13217 bytes**, `sha256 = 53f460dc…` **exact match**. The only unknown was REA's own `meta.duration`; a 0–9999 `NNNNms` sweep found `2411ms` uniquely. This proves the committed `after.json` is byte-for-byte the `.data` payload of a genuine REA envelope, and that `run.json`'s envelope block is arithmetically and cryptographically consistent (`envelope 13217 − after.json 13140 = 77 = wrapper overhead − 1`). Note the harness wall `duration_ms 4056` vs REA `meta.duration 2411ms` — both plausible (npx startup + teardown outside REA's own timer), and neither is the other's bound.

## 3. `evidence_id` reproduced from the REA rule

Rule (`rea-agents@6.5.0`, `dist/cli-runtime/reconstructionObligationLedgerSchemas-Bao0xMr-.js:30,536,557`): `evidence_id = "ev_" + sha256(canonicalJson(semanticProjection(record)))`, keys sorted, scalars via `JSON.stringify`, `subject` limited to `{digest, format, architecture}`, but `parameters`/`raw_result`/`normalized_result` included **verbatim** (so absolute paths and blob ids are inside the digest).

| record | recorded | recomputed | match |
|---|---|---|---|
| my run (`$S/rea.stdout.json`) | `ev_a4ae125784c241d2b23678659b2cc05634dc4209d67c413c258d5b6eea045bcb` | same | **yes** (method validated) |
| committed `K3/after.json` | `ev_af856f0838c652ed398dfbb77f3d16c489132376f2dadcaa86dd6bbe498c66e4` | same | **yes** |

So the receipt was not hand-edited after its identifier was computed: any field change without the full canonicalisation (including the original `output_directory`, REA staging tmpdir and blob ids) breaks it. This is self-consistency, not fabrication-proof on its own — the canonicaliser is public — hence the independent re-run below.

## 4. Non-determinism measured (why blob handles cannot be compared)

Three runs, same 4096-byte carrier, same unblob `26.6.4`/`0ce7b624…`: blob handle = `166849:1` (my run 1), `1641265:1` (my run 2), `2779683:1` (author). My two runs are otherwise **identical** (`files`, `chunks` apart from `provider_id`, derivations). Conclusion: `provider_id`/`provider_blob_id`/`blob_id`/`ChunkReport.id` are per-run handles and carry no provenance; every other field in the receipt is stable. `[INFERENCE]` the handle is an in-process id counter allocated before extraction, so it scales with the staging work done.

## 5. Oracle (independent extractor)

`sasquatch-v4be -be -no-exit-code -f -d $S/x carrier.bin` → exit 0, "created 4 files / 1 directory / 0 symlinks", 4 inodes decompressed.

| relpath | sasquatch sha256 | oracle.tsv |
|---|---|---|
| `apple1.txt` | `6181259c…7e1c30` | identical |
| `apple2.txt` | `919fc82d…28d4aff` | identical |
| `apple3.txt` | `2d95014e…154bd21ec6` | identical |
| `apple4.txt` | `08d9b05b…e8c8a959d` | identical |

File set + sha256 + size: **4/4 exact, no extra, no missing** — and the same set/sha/size is what the committed receipt publishes (`published_bytes 28 = 4×7`). REA's own outdir bytes re-hash to the same four digests, so `reported_sha256` is not a claimed list, it is what is on disk.

Symlinks: the image contains **none** (`sasquatch: created 0 symlinks`; superblock "5 inodes" = 4 files + root dir; committed `symlinks.tsv` 0 B). So the "in-tree kept / escaping removed only by unblob" arm is vacuous for K3 — vacuously consistent (`unpublished_entries []`, `extraction_gaps []`). That semantics is exercised by K1/K5/K6, not here.

Structural aside (supports the `carriers.json` label "4k padded"): `K3[:307] == K4` byte-for-byte, and `K3[307:]` is all zeros; K3/K4 share oracle sha `638a6f75…`.

## 6. `run.json` internal consistency

* `start_utc 17:16:53Z` → `end_utc 17:16:57Z` (Δ4000 ms), `duration_ms 4056` covers it; `start` is **+4m02s after the freeze landing** (`17:12:51Z`) and `end` is **−1m35s before the receipt commit** (`6fdaf4f1`, `17:18:32Z`); `after.json` mtime 14:16 local = 17:16Z. Ordering is right.
* `argv` (13 elements) is literally `npx -y rea-agents@6.5.0 extract-firmware --format json --full-output <carrier> <scratch>/extract`; `extraction_root == argv[12]`; `cwd == scratch`; outdir `K3-out` holds `after.json`+`run.json` only (envelope deleted, as documented).
* `run_provenance_segment_ok: true` and `parameters.output_directory (/fast/scratch/hyaku/kaidoku-r39/l1/c1runs/K3-scratch/extract)` contains `/kaidoku-r39/` — and that string is inside `evidence_id` (§3), so it is bound to the receipt.
* `receipt {sha256 dade9766…, bytes 13140, evidence_id ev_af856f08…}` matches the file on disk; `carrier {sha256 9c7c523c…, size 4096}` matches the pin; `child_path` contains `/home/vgpnk/.local/bin` (sasquatch on PATH precondition met); tool pins match the live binaries (§pins).
* K3's receipt is not a copy of a sibling: `evidence_id`/`subject.digest`/`selection.length` (4096 vs K4 307)/`output_directory` differ from K4 while `relative_path` lists coincide — expected (identical payload, different carrier).

## 7. Counter sensitivity probes (scratch clone only — lane VCS untouched)

`git clone -q --shared <lane> "$S/clone"` → `git -C "$S/clone" rev-parse --show-toplevel` = `$S/clone`; all mutations committed **inside the clone**.

| probe | result |
|---|---|
| baseline `--rev 6fdaf4f1` | `met_target true`, `carriers_matched 6`, K3 `matched true`, `run_provenance_ok true` — reproduces the author's score |
| A: `K3/run.json` `start_utc/end_utc` backdated to `2026-10-20T00:00:0xZ` (pre-freeze) | `met_target true`, `carriers_matched 6`, K3 `matched true`, `run_provenance_ok **true**` — **the counter does not bind run times to the freeze** |
| B: `after.json` `raw_result.execution.exit_code 0→1`, `evidence_id` not recomputed | `met_target false`, `carriers_matched 5`, K3 `matched false`, `evidence_id_ok false` — naive tampering is refused |

Probe A is the measured basis for QUALITY 78 and for this seat existing: receipt-only clauses plus a public oracle cannot refuse a *consistent* re-mint. What the counter cannot see — timing, staging paths, blob handles, envelope digest — is exactly what an independent re-run pins, and in K3's case it reproduces.

## 8. Limits of this attack (stated, not hedged)

* The envelope file was never committed, so its digest is only checkable by reconstruction; I closed it (§2) but that check depends on my reimplementation of the wrapper, which I validated on my own envelope.
* Blob handles are unverifiable by construction (§4); I exclude them explicitly rather than treating the mismatch as a defect.
* `normalized_result.files[].path` / `parameters.*` point into the author's deleted scratch (`K3-scratch/extract`, gone; only `K3-out` survives). Verified instead through `relative_path` + `sha256` against my own run and the sasquatch oracle.
* K3 has zero symlinks, so nothing here tests symlink publication/escaping; that arm belongs to K1/K5/K6.
* I did not re-run the author's exact `c1-run.sh` (bounds: writing into `/fast/scratch/.../l1/c1runs/` is outside my scratch), so my run reproduces the REA layer, not the harness's `jq`/digest bookkeeping — the bookkeeping was instead closed arithmetically in §2/§3/§6.

## 9. Files

Artifacts: `.ufo/waves/round-39/w2/artifacts/R39W2ReproK3/` — `reconstructed-envelope.json` (`53f460dc…`, 13217 B), `rea.stdout.json` (my 12054 B envelope), `diff-leaves.txt` (all 47 differing leaves), `oracle-check.txt`, `evidence-id-recompute.txt`, `counter-probes.txt`, `base-score.json`, `mutA-score.json`, `mutB-score.json`.

Lane writes: this report + that artifacts directory only. No VCS mutation in the lane or fleet; the clone, its two fixture commits and all REA/unblob output lived in `$S` and were removed.
