# R38ExecAfterK2 — R38-C1 after-receipt for carrier K2

Seat: leaf executor (leaf: no dispatch, no background jobs, no `agent://all`). Advisory only.
Assignment: produce the R38-C1 claim receipt for carrier K2 (REA `extract-firmware` after-arm),
verify handler / gaps / oracle coverage, land the envelope byte-exact under the seat artifact dir.

**Bottom line: the receipt is produced and is self-consistent (exit 0, `squashfs_v4_be`,
3/3 oracle regular files byte-identical, evidence id recomputes), but it carries ONE
`extraction_gaps` entry — the committed symlink `var/lib/run-link` — so the frozen counter's
`after_gaps_empty = gaps(env) == []` clause evaluates **False** for K2. Under P38-C1 as frozen,
K2 does not match. That is reported, not repaired.**

Secondary: the harness `after` mode at the freeze commit could not run at all (exit 1); I measured
that at 03:18:34 and the lane fixed it upstream in `cb4326b2` at 03:19:01, after which it exits 0 and
reproduces the same single gap (§5).

## 1. Inputs and pin check

Manifest `.ufo/waves/round-38/c1/carriers.json` (read-only) — K2:

| field | value |
|---|---|
| path | `corpus/evidence/round-37/c1/K2/carrier.sqsh` |
| oracle | `corpus/evidence/round-37/c1/K2/oracle.tsv` |
| sha256 pin | `403cb0a827966bbe17a70e08af7d39b43260da8201d1b9001bbc4228cbc99154` |
| kind (manifest text) | "synthetic standard-BE v4 gzip (tree2, symlink + unicode name)" |

```
$ sha256sum corpus/evidence/round-37/c1/K2/carrier.sqsh
403cb0a827966bbe17a70e08af7d39b43260da8201d1b9001bbc4228cbc99154  …/c1/K2/carrier.sqsh
$ sha256sum $S/carrier.sqsh
403cb0a827966bbe17a70e08af7d39b43260da8201d1b9001bbc4228cbc99154  …/K2-after/carrier.sqsh
$ file $S/carrier.sqsh
Squashfs filesystem, big endian, version 4.0, zlib compressed, 1606 bytes, 10 inodes,
blocksize: 4096 bytes, created: Tue Nov 14 22:13:20 2023
```

Pin **matches**. Carrier 1606 B; oracle.tsv 248 B (sha256 `6567cc50d9a1dea27609c0ae2b815229317e899eaba654edf6f0880e559cb921`).
Oracle rows (3): `a/run.sh`, `space name.txt`, `var/lib/data.bin`.

Manifest description nit: the "unicode name" is ASCII — `space name.txt` (`73 70 61 63 65 20 …`),
i.e. a space, not a non-ASCII name. Pinned bytes and oracle are unaffected; only the prose kind differs.

Tooling (no install done): `rea-agents` 6.5.0 (package root
`/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`, `package.json` version `6.5.0`),
`unblob` 26.6.4 via `REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob`
(binary sha256 `0ce7b624f540c2191ff144892584997fe3fb6ab28ab6ef6b88639f8a7cba1d09`, as recorded in
the envelope's `normalized_result.engine`). `node v24.21.0`. No sasquatch on PATH; stock unblob
handled the image, `squashfs_v4_be` reported by the provider itself.

## 2. After-arm run

Scratch `S=/fast/scratch/hyaku/kaidoku-r38/R38ExecAfterK2/K2-after`, `TMPDIR=$S`.
2026-10-26T03:17:16-03:00 first attempt, 03:17:26-03:00 successful run.

First attempt used an **existing** (empty, `mkdir -p`ed) output root and failed:

```
$ mkdir -p "$S/out"; REA_UNBLOB_COMMAND=… npx -y rea-agents@6.5.0 extract-firmware \
    --format json "$S/carrier.sqsh" "$S/out" > "$S/envelope.json"   # exit 1
{"code":"execution_failure", … "details":{"provider_id":"unblob","operation":"extract_firmware",
 "diagnostics":{"reason":"Extraction output root already exists"}}}
```

Successful run passes a **non-existent** output root:

```
$ rm -rf "$S/out"; REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob \
    npx -y rea-agents@6.5.0 extract-firmware --format json \
    "$S/carrier.sqsh" "$S/out" > "$S/envelope.json"     # exit 0, 1.91 s wall
$ stat -c%s "$S/envelope.json"; sha256sum "$S/envelope.json"
17295
263d1d11ef7e78352696fe46286b27f1f9ddeed465892baed5f77e91491bf690  "$S/envelope.json"
```

Envelope identity: `evidence_id` `ev_4d478254a54b7c732ae585baddb7ad8a9472b86737893823fa66527d219f73be`,
`operation` `extract_firmware`, `provider` `{id: unblob, version: 26.6.4}`, `predicate_type`
`rea.analysis`, `authority` `shipped-artifact`, `confidence` `observed`, `environment` null,
`limitations` 5 entries, `evidence_links` `[]`, `locations` `[{file-offset-range 0..1606}]`.

## 3. Verification of the four required checks

| check | required | observed | verdict |
|---|---|---|---|
| `normalized_result.chunks[].handler` | all `squashfs_v4_be` | 1 chunk: `{offset 0, length 1606, handler "squashfs_v4_be", provider_id "1553881:1", extraction_failed false, root_file_range 0..1606}` | **pass** |
| `extraction_gaps == []` | empty | **1 gap** (see §4) | **FAIL** |
| every oracle row (suffix + sha256) in `normalized_result.files` | 3/3 | 3/3 (`matched()` = 3 of 3) | **pass** |
| receipt recomputes to its stored evidence id (rea-agents 6.5.0 rule) | equal, `ev_` | `node tools/round-27/xpin-attribute.mjs --pkg65 <pkg65> --pkg67 <pkg65>` exit 0 → `ev_4d4782…` = stored, 6.5.0 and 6.7.0 rules agree (`both`) | **pass** |

Published files (`relative_path`, sha256, size) — all three byte-identical to the committed source tree:

| relative_path | sha256 | size | oracle |
|---|---|---|---|
| `firmware.bin_extract/a/run.sh` | `ca9988b82e0c964aa5acb5d99625bbdd9b8fa09bd7949128b92ed7fe602a4084` | 22 | OK |
| `firmware.bin_extract/space name.txt` | `72d0bbc9b23d127ca15949787b21e469494483890b8fccf81e7e94d3f6c4c85d` | 21 | OK |
| `firmware.bin_extract/var/lib/data.bin` | `e96760a87768717bcebcfd25ddc7d46b4dbc95a4b0014def080c08539f7d90d0` | 10240 | OK |

`published_bytes` 10283 = 22+21+10240. `diff -r K2/src <out>/firmware.bin_extract` reports only
`Only in src: a/b` (empty directory, never published — REA publishes regular files only) and
`Only in src/var/lib: run-link` (the symlink, §4). No content difference.

## 4. Falsifier 1 (claim-level): K2's after-receipt is not gap-free

```
$ jq -c '.normalized_result.extraction_gaps' after.json
[{"kind":"unpublished-entry","input_path":"$output/firmware.bin_extract/var/lib/run-link",
  "relative_path":"firmware.bin_extract/var/lib/run-link","handler":null,"provider_id":null,
  "range":null,"root_file_range":null,"dependencies":[],
  "continuation_id":"602c674b7f83f4acd6bf01c5655a5dd669f206d33ee3bc9b8bc2c0ba9f08cfca"}]
$ jq -c '.normalized_result.unpublished_entries' after.json
[{"relative_path":"firmware.bin_extract/var/lib/run-link","kind":"symlink",
  "link_target":"../../a/run.sh"}]
$ jq -r '.normalized_result.coverage' after.json
partial
```

Source of the gap: the frozen carrier tree itself contains a symlink (`K2/src/var/lib/run-link`,
a 14-byte link to `../../a/run.sh`; target length matches `../../a/run.sh` = 14). REA/unblob 26.6.4
retains symlinks as metadata and publishes only regular files (provider limitation text:
"only regular files are published, without executable permission bits"; continuation 602c674b…
says the same), so **any** carrier with a symlink produces a gap under this provider.

Evaluated through the **frozen counter's own code path** (`import` of `tools/round-38/c1-counter.py`,
read-only, no edits):

```
chunk_handlers              : ['squashfs_v4_be']
HANDLER in handlers         : True
after_gaps_empty (gaps==[]) : False
oracle_files                : 3
after_oracle_hits           : 3 of 3
subject digest == pin       : True
operation/provider          : extract_firmware unblob
```

`measure()` computes `matched = oracle_frozen and oracle_files>0 and after_present and
after_subject_ok and after_operation_ok and after_handler_ok and after_gaps_empty and
`after_evidence_id_ok and after_oracle_hits==oracle_files` (`c1-counter.py:186-192`), so **K2's
`matched` is False** despite a fully successful, byte-identical extraction. With K2 false,
`carriers_matched` cannot reach the target 4; P38-C1 is an honest miss unless the L1 judges the
gap clause differently (the counter and predicate are frozen — not mine to change).

Reproduced a second time at a different output root (`$S/out2`, 03:18:14-03:00, exit 0): identical
handler, identical 3 published files, identical `published_bytes`, **same single gap**
`firmware.bin_extract/var/lib/run-link`, `coverage` `partial`. Not flaky. That second envelope's
`evidence_id` differs (`ev_e16b0efbb456270cc82c5d004ede37bc7ddb6cae7d3e7802d0d7969f649e55c2`,
17295 B vs 17300 B) because the evidence id folds the absolute `parameters.path` /
`output_directory` / `files[].path`; the stored id still recomputes from the stored bytes, so the
counter's clause is self-consistent — see Falsifier 3.

**Cross-carrier inference [INFERENCE, high]:** K1's source tree also holds a symlink
(`K1/src/link-to-hello` → 12-byte target; round-37 verifier recorded `link-to-hello -> ../hello.txt`),
so K1's after-receipt will very likely carry the same `unpublished-entry` gap and also fail
`after_gaps_empty`. If so, at most 2 of 4 carriers (K3/K4, no symlinks) can match. Not measured by
this seat (K1 belongs to `R38ExecAfterK1`) — flagging for the L1 to cross-check before scoring.

## 5. Falsifier 2 (harness-level, already fixed upstream during the wave): `c1-run.sh after` at the freeze could not produce a receipt

At the freeze commit `e059ca93`, `tools/round-38/c1-run.sh:26` read `mkdir -p "$OUT"` before
`npx … extract-firmware … "$CARRIER" "$OUT"` (line 27). REA 6.5.0 refuses an existing output root,
so that harness failed on every invocation. Measured at 2026-10-26T03:18:34-03:00:

```
$ REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob HYAKU_SCRATCH=/fast/scratch/hyaku \
    bash tools/round-38/c1-run.sh after "$S/carrier.sqsh" "$S/harness-out" "$S/…/harness-scratch"
exit=1
{"code":"execution_failure", … "diagnostics":{"reason":"Extraction output root already exists"}}
$ ls -ld "$S/harness-out"
drwxr-xr-x 2 vgpnk vgpnk 6 …  harness-out      # created empty by the harness, then rejected
```

**The lane owner fixed this independently while I was measuring.** `git log` shows
`cb4326b2 round-38: harness fix (REA refuses existing extraction root; oracle mode unchanged)`,
committed `Mon Oct 26 03:19:01 2026 -0300` (file mtime 03:18:53), i.e. 19 s after my failing run; the
diff replaces line 26 with `rm -rf "$OUT"  # REA refuses an existing extraction root; it creates $OUT itself`
and updates the usage header. The working tree is clean against HEAD for `tools/round-38/`, so this
is the lane's fix, not mine (`git status --porcelain -- tools/round-38 plans/round-38-claims.md`
prints nothing; I wrote only this report and the artifact).

Confirmed on the fixed script at 2026-10-26T03:20:14-03:00 with a non-existent OUTDIR:

```
$ bash tools/round-38/c1-run.sh after "$S/carrier.sqsh" "$S/out" "$S/scratch"
exit=0, envelope 17583 B
{"handler":["squashfs_v4_be"],"coverage":"partial","gaps":1,
 "gap_paths":["firmware.bin_extract/var/lib/run-link"],"published_bytes":10283,
 "subject":"403cb0a827966bbe17a70e08af7d39b43260da8201d1b9001bbc4228cbc99154"}
```

Same extraction as my receipt; the extra 288 B over the artifact envelope are longer absolute
scratch paths (including REA's random `rea-firmware-xSD56d` temp dir), and the run also shows
`provider_blob_id` varying between runs (`1553881:1` vs `1886511:1`) — see §6. Consequence for the
claim: the harness `after` mode works at HEAD but was broken at the freeze; the per-carrier receipt
must be produced by a working invocation, and the gap finding in §4 is unchanged on both paths.

## 6. Falsifier 3 (receipt portability, informational): absolute scratch paths inside the envelope

The envelope embeds my scratch paths and will keep them when committed:
`subject.local_path`, `parameters.path`, `parameters.output_directory`,
`normalized_result.output_directory`, and each `files[].path`, e.g.
`/fast/scratch/hyaku/kaidoku-r38/R38ExecAfterK2/K2-after/out/firmware.bin_extract/a/run.sh`.
The frozen counter is unaffected (`published()` reads `relative_path`, and receipt identity uses
`subject.digest.sha256`, per R36-CL6), and the evidence id recomputes from the stored bytes. But the
committed receipt will cite a deleted scratch tree, and its `evidence_id` is location-bound: three
runs of the same 1606 B carrier produced `ev_4d4782…` (artifact), `ev_e16b0e…` (`out2` rerun) and
`ev_b3bc88…` (fixed-harness run), differing in the absolute paths **and** in the provider blob ids
(`1553881:1` vs `1886511:1` in `chunks[0].provider_id` and every `derivations[].provider_blob_id`,
`raw_result` task/subtask ids). The extraction itself is invariant: same handler, same three
published `relative_path`s with the same sha256s, `published_bytes` 10283, same single gap. If the
L1 wants path-stable receipts, the after-run must be re-executed at the final stable location
**before** integration; nothing in the predicate requires it.

## 7. Landed artifact

```
$A = .ufo/waves/round-38/w1/artifacts/R38ExecAfterK2/after.json
17295 bytes
sha256 263d1d11ef7e78352696fe46286b27f1f9ddeed465892baed5f77e91491bf690
cmp <scratch envelope> "$A/after.json"   → byte-identical (exit 0)
```

Nothing was written to `corpus/evidence/round-38/`, `corpus/knowledge`, `PROVINCE.md`,
`corpus/SOURCES.md`, `corpus/README.md`, `SCORECARD.md`, `SHONEN.md`, `LOG.md`, or anywhere outside
the seat artifact dir and this report. No VCS mutation; no tool installed or upgraded. Scratch
(`/fast/scratch/hyaku/kaidoku-r38/R38ExecAfterK2/`) removed at exit; the only surviving copy of the
receipt is the artifact above, and every number quoted here is reproduced from it or from the
committed lane bytes.

## 8. Exact retained evidence summary

- Carrier sha256 = pin `403cb0a8…`, `file` = big endian v4.0 zlib, 1606 B.
- Receipt: exit 0, 17295 B, sha256 `263d1d11…`, `evidence_id ev_4d4782…` (recomputes equal under 6.5.0).
- Handler `squashfs_v4_be` on the single chunk; `coverage` `partial`; `published_bytes` 10283.
- Oracle 3/3 by relative-path suffix and sha256; `diff -r` content-identical.
- `extraction_gaps` = 1 (`unpublished-entry`, symlink `firmware.bin_extract/var/lib/run-link`,
  continuation `602c674b…`) → frozen `after_gaps_empty` False → K2 `matched` False.
- Harness `after` mode at freeze `e059ca93` exited 1 ("Extraction output root already exists");
  fixed upstream in `cb4326b2` (03:19:01), re-run exit 0 with the identical extraction and gap.
- Concurrent-change note: `tools/round-38/c1-run.sh` changed under me at 03:18:53
  (HEAD `cb4326b2`). I made no lane writes (`git status --porcelain -- tools/round-38
  plans/round-38-claims.md` empty); counter `c1-counter.py` untouched (mtime 03:05:51).
