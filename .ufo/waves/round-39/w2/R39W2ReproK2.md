# R39W2ReproK2 — provenance re-run of the committed R39-C1 receipt for carrier K2

**Verdict: CONFIRMED.** An independent REA 6.5.0 / unblob 26.6.4 after-arm re-run of the frozen K2
carrier (pin `403cb0a827966bbe17a70e08af7d39b43260da8201d1b9001bbc4228cbc99154`, 1606 bytes)
reproduces **every** semantic field of the committed receipt
`corpus/evidence/round-39/c1/K2/after.json`, the receipt's `evidence_id` recomputes under the
rea-agents 6.5.0 rule, and an independent `sasquatch-v4be -be` extraction matches the frozen
`oracle.tsv` and `symlinks.tsv` byte-for-byte on the fields they carry. No falsification.

Seat bounds observed: read-only git, writes only into my artifacts dir and this report, no VCS
mutation, no subagents, no new tool installs.

## 1. Carrier pin (copied into scratch, verified before the run)

```
$ cp <lane>/corpus/evidence/round-37/c1/K2/carrier.sqsh $S/carrier.sqsh
$ sha256sum $S/carrier.sqsh ; stat -c '%s' $S/carrier.sqsh
403cb0a827966bbe17a70e08af7d39b43260da8201d1b9001bbc4228cbc99154  carrier.sqsh
1606
```

Matches `.ufo/waves/round-39/c1/carriers.json` `K2.sha256` / `size_bytes` exactly, and the freeze
blob `7f126958…` stored at `8fcda41c` hashes to the same sha256:

```
$ git rev-parse 8fcda41c:corpus/evidence/round-37/c1/K2/carrier.sqsh   -> 7f12695807ae266c2eab5df83f3687932847065b
$ git cat-file blob 7f126958 | sha256sum
403cb0a827966bbe17a70e08af7d39b43260da8201d1b9001bbc4228cbc99154  -
```

Also re-verified: `oracle.tsv` pin `6567cc50…` and `symlinks.tsv` pin `0a03d6e1…` match
`carriers.json`; both blobs plus the carrier are **SAME** at `8fcda41c` and `HEAD`
(`5ef0d600…`, `31862cda…`, `7f126958…`), and `carriers.json` has sha256 `df9eb8a6…` at both
revisions. So no frozen C1 path for K2 was touched after the freeze.

## 2. Independent after-arm (context command, fresh outdir)

```
$ S=/fast/scratch/hyaku/kaidoku-r39/R39W2ReproK2; cd "$S"
$ REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob npx -y rea-agents@6.5.0 extract-firmware \
    --format json --full-output "$S/carrier.sqsh" "$S/out" > "$S/rea.json" 2> "$S/rea.err"
EXIT=0   start 2026-10-26T17:27:18Z   end 2026-10-26T17:27:21Z   stderr empty (0 bytes)
```

Envelope `{"ok":true,"meta":{"command":"extract-firmware","duration":"2126ms"}}`, 15459 bytes;
`data` extracted to `mine-data.json` (15382 bytes).

## 3. Semantic comparison vs the committed receipt

`compare.py` (artifacts) normalizes only path/id strings (scratch outdir, REA temp dir, carrier
path, unblob `pid:counter` blob ids) and compares:

| field | committed | my re-run | equal |
|---|---|---|---|
| `chunks[].handler` | `squashfs_v4_be` | `squashfs_v4_be` | yes |
| `chunks[].extraction_failed` | `false` | `false` | yes |
| `chunks[].encrypted` | `false` | `false` | yes |
| `chunks[].range` / `root_file_range` | `{0,1606}` | `{0,1606}` | yes |
| `(relative_path, sha256)` in `files` | 3 rows, prefix `firmware.bin_extract/` | identical 3 rows/shas | yes |
| `extraction_gaps` (`kind`, `relative_path`, `continuation_id`, `dependencies`) | 1 × `unpublished-entry` on `firmware.bin_extract/var/lib/run-link`, `602c674b…` | identical | yes |
| `unpublished_entries` (`relative_path`, `link_target`, `kind`) | `…/var/lib/run-link`, `../../a/run.sh`, `symlink` | identical | yes |
| `diagnostics` `__typename__` set | `∅` (empty list) | `∅` (empty list) | yes |
| `coverage` / `published_bytes` | `partial` / `10283` | `partial` / `10283` | yes |
| `selection` / `engine` / `provider` / `limitations` / `confidence` / `authority` / `analysis_profile` / `environment` / `locations` / `evidence_links` | — | — | yes |
| `parameters` minus `path`/`output_directory` | `max_depth 3`, `max_output_bytes 268435456`, `max_output_files 10000` | identical | yes |
| `raw_result` (normalized) | — | — | yes |

`compare.out`:

```
committed_vs_mine_semantic_equal            true
raw_result_committed_vs_mine_normalized     true
nonpath_field_differences_mine              []
published_bytes_sum_check                   true   (22 + 21 + 10240 = 10283)
```

The only byte-level differences are the ones REA derives from paths and the provider's process
state, all excluded by construction or by evidence:

- `evidence_id` (`ev_a77e1e9e…` vs mine `ev_87010a68…`): `semanticProjection`
  (`rea-agents/dist/domain/evidence.js:156-180`) includes `parameters`, whose
  `output_directory` is the round-39 scratch path, so the id is path-scoped by design.
- `parameters.path` / `parameters.output_directory` / `subject.local_path` /
  `normalized_result.output_directory` / `raw_result` and `execution.args` paths.
- `chunks[].provider_id` = `derivations[].provider_blob_id` = `2674572:1` (committed) vs
  `3904941:1` (mine). Source: unblob `identifiers.py new_id()` returns
  `f"{os.getpid()}:{counter}"`, i.e. the unblob **PID**; REA copies it verbatim
  (`FirmwareReports.js:297`, `:355`). Per-run process state, never reproducible — correctly
  non-semantic.

## 4. Receipt authenticity under the frozen 6.5.0 id rule

`recompute-id.mjs` imports `dist/domain/canonicalDigest.js` from the pinned package and transcribes
`semanticProjection` verbatim:

```
$ node recompute-id.mjs <lane>/corpus/evidence/round-39/c1/K2/after.json
{"stored":"ev_a77e1e9ef8ad12b64b4e495b8dc11c54a012335fde5086cf28bc0aa2893d88cc",
 "recomputed":"ev_a77e1e9ef8ad12b64b4e495b8dc11c54a012335fde5086cf28bc0aa2893d88cc","match":true}
$ node recompute-id.mjs mine-data.json
{"stored":"ev_87010a68…","recomputed":"ev_87010a68…","match":true}
```

The committed payload is internally consistent under the frozen rule (not a payload edited around
a fixed id), and the pinned subject digest `403cb0a…` is inside the hashed projection.

Second recorded run: the wave-1 harness receipt
`.ufo/waves/round-39/w1/artifacts/R39C1Harness/receipts/K2/after.json` (run 2026-10-26T16:55:15Z,
**before** the freeze at 17:12:51Z, own scratch dir, 18055 bytes) also recomputes
(`ev_8de5ad49…`, `match:true`) and its semantic payload is **identical** to the committed one
(`committed_vs_w1_semantic_equal true`). Three runs — w1 16:55Z, committed 17:16:46Z, mine
17:27:18Z — agree on every compared field.

## 5. Oracle check (independent of REA and unblob)

```
$ sasquatch-v4be -be -no-exit-code -f -d "$S/x" "$S/carrier.sqsh"     # EXIT=0
"Reading a different endian SQUASHFS filesystem … created 3 files / 6 directories / 1 symlink"
$ <sha256 listing of x, sorted> vs <oracle.tsv sorted>                # diff empty -> FILES: IDENTICAL
$ <rel,target listing of x> vs <symlinks.tsv cols 1,2>                # diff empty -> LINKS: IDENTICAL
files=3 links=1 dirs=6
```

- regular files: `a/run.sh ca9988b8… 22`, `space name.txt 72d0bbc9… 21`,
  `var/lib/data.bin e96760a8… 10240` — all three rows byte-identical to the frozen `oracle.tsv`,
  and their sizes sum to the receipt's `published_bytes` 10283.
- symlinks: exactly one row, `var/lib/run-link → ../../a/run.sh`, classified **in-tree**; it
  resolves to `a/run.sh` inside the image (its sha256 equals `a/run.sh`'s `ca9988b8…`), so it is
  neither dangling nor escaping. sasquatch keeps it — correct; there is no escaping row for K2, so
  the "escape removed only by unblob" clause has nothing to act on here. unblob kept it as an
  `unpublished-entry` gap and published no path for it, exactly the frozen symlink rule.

## 6. `K2/run.json` internal consistency

| item | value | check |
|---|---|---|
| `argv` | `npx -y rea-agents@6.5.0 extract-firmware --format json --full-output <carrier> <extraction_root>` | 8 elements; `argv[6]` == `extraction_root`; `cwd` == its parent (`…/K2-scratch`) |
| `run_provenance_segment_ok` | `true` | scratch path contains `/kaidoku-r39/` ✔ |
| `start_utc` / `end_utc` | `17:16:46Z` / `17:16:50Z` | both **after** the freeze commit `8fcda41c` at `2026-10-26T14:12:51-03:00` = `17:12:51Z`; both before the receipt commit `6fdaf4f1` at `14:18:32-03:00` = `17:18:32Z` |
| `duration_ms` | 4055 | fits the 4 s start/end window |
| `exit` | 0 | consistent with `data_extracted`/`receipt_written` true |
| `sasquatch_v4be` | `sha256 fac88740…`, `4.5.1`, `unsquashfs version 4.5.1 (2022/03/17)` | equals the actual binary (`/home/vgpnk/.local/bin/sasquatch-v4be`, sha `fac88740…`, same version line) |
| `unblob` | `env_value ~/.local/bin/unblob` → `command_env …/uv/tools/unblob/bin/unblob`, sha `0ce7b624…`, `26.6.4` | `~/.local/bin/unblob` is a symlink to that realpath; its sha256 is `0ce7b624…`; equals `normalized_result.engine.executable_sha256` |
| `rea` | pin `rea-agents@6.5.0`, version `6.5.0`, package_root `…/_npx/ad9a3fdbcad992c6/node_modules/rea-agents` | package.json `version` = `6.5.0` |
| `receipt` | `sha256 f520b0a5…`, `17236` bytes, `evidence_id ev_a77e1e9e…` | working-tree `after.json` is exactly `f520b0a5…`/17236; blob `ea6e972a…` identical at `41aee041`, `6fdaf4f1`, `52b0eb29`, `HEAD`; id == the file's own id |
| `selection_sha256` / `subject_sha256` | both `403cb0a8…` | equals the carrier pin |
| `envelope` | `ok true`, `parseable true`, `17313` bytes, sha `c0b1de0a…` | bytes minus `after.json` = **77**, exactly my measured wrapper overhead (18-byte `{"ok":true,"data":` + 59-byte `,"meta":{…duration":"2126ms"}}` = 77 on my own run) — arithmetically consistent |
| `child_path` | contains `/home/vgpnk/.local/bin` | sasquatch-v4be reachable on the child PATH, as the predicate requires |
| `stderr_head` | `""` | my re-run also produced an empty stderr |
| `previous_after_json_sha256` | `null` | outdir was fresh at that run |

Cross-check with the frozen counter receipt only (not re-run by me, out of seat):
`.ufo/waves/round-39/l1/scores/c1-at-6fdaf4f1.json` records `carriers_matched 6`, `met_target true`,
`frozen_path_changed []`, and for K2 `matched true`, `oracle_hits 3/3`, `published_files 3`,
`gaps_note "1 gaps == 1 in-tree symlinks"`, `run_provenance_ok true`, `evidence_id_ok true`,
`receipt_first_add 6fdaf4f1`.

## 7. Findings and limits (none falsifying)

1. **Duplicate receipt blob in an unreachable commit.** `41aee041f0b2cd8fef11f5ea8bca45231ff44eaa`
   (parent `3c07eed7`, same parent as `6fdaf4f1`, **not** an ancestor of `HEAD`, no branch
   contains it) carries the *identical* K2 `after.json`/`run.json` blobs. Content is unchanged and
   the counter's first-add walks reachable history, so nothing about the receipt is wrong — but
   `git log --all -- corpus/evidence/round-39/c1/K2/` shows two commits for the same bytes, which
   can mislead a provenance reader. Observation only, no defect found.
2. **Envelope sha256 is not independently re-derivable** (`c0b1de0a…`): the envelope file was not
   kept (`C1_KEEP_ENVELOPE` unset), so only its size arithmetic (77-byte overhead, exact) can be
   checked. The extracted `after.json` *is* re-verifiable and was re-derived from a fresh run.
3. **`provider_id` is process state.** `2674572:1` is unblob's `pid:counter`. Any future counter or
   receipt diff that treats `provider_id`/`provider_blob_id` as semantic will false-fail on a
   re-run; the frozen C1 predicate correctly ignores it.
4. **Directory `StatReport` sizes** in `raw_result.report` (`a`=29, `a/b`=15, `a/b/c`=6) are
   filesystem `st_size` values; they matched only because my extract dir is on the same
   `/fast/scratch` filesystem. Not used by any predicate.
5. **My own procedural deviation (disclosed).** Session variables do not persist between my `bash`
   calls, so the REA invocation did not have `TMPDIR=$S` exported; REA's per-run temp dir landed in
   `/tmp/rea-firmware-RQv6ml` instead of scratch (removed by REA on exit). Consequence: `execution.args`
   and `report[].task.path` in my envelope name `/tmp`, whereas the committed one names
   `…/K2-scratch/rea-firmware-8t1CES`. No payload field is affected; those paths are normalized in
   `compare.py`.
6. **[INFERENCE]** Because the committed receipt's own payload, a second pre-freeze run, and my
   post-freeze re-run agree field-for-field while the receipt's id binds its own subject digest, the
   documented disclosed limit (a re-minted fabrication defeats a receipt-only counter) is *not* what
   is on disk for K2: the committed payload is a genuine unblob 26.6.4 extraction of the pinned
   carrier. This is inference from reproductions, not a formal proof of authorship.

No new tools installed or upgraded by this seat.

## 8. Artifacts

`.ufo/waves/round-39/w2/artifacts/R39W2ReproK2/`

- `rea.json` — my full REA envelope (`ok:true`), sha256 of the extracted `data` = `mine-data.json`
- `mine-data.json` — my re-run's receipt payload (the post-run `after.json` equivalent)
- `compare.py` / `compare.out` — normalized three-way semantic comparison and its result
- `recompute-id.mjs` — 6.5.0 id recomputation for committed, mine and w1 receipts
- `oracle-check.tsv`, `oracle.tsv.sorted`, `oracle-links.tsv`, `symlinks.rt` — sasquatch-v4be
  extraction vs frozen oracle/symlink tables (diffs empty)
- `sasquatch.log` — `-be -no-exit-code -f` run output (sha256 `6a7d3925…`)
- `pins-and-commits.txt` — pin, blob-id, commit-time and tool-identity receipt
