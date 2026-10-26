# R39W2ReproK4 — provenance attack on the committed R39-C1 K4 after-receipt

**Verdict: CONFIRMED** — every demanded semantic field of `corpus/evidence/round-39/c1/K4/after.json`
is reproduced by an independent REA after-run on a re-copied, pin-verified K4 carrier; the
sasquatch oracle check matches file-for-file; `run.json` is internally consistent and its claimed
receipt sha256/bytes match the committed bytes; the stored `evidence_id` recomputes from the
committed payload under the frozen rea-agents 6.5.0 rule. No falsification found.

Seat scope: K4 only (`corpus/evidence/round-37/c1/K4/carrier.bin`, pin
`a29ddc15f5a6abcabf28b7161837eb56b34111e48420e7392e648f2fdfe956ed`, 307 bytes), receipt first added
in `6fdaf4f162aff156fcef0e52998a5469c64fd6f0` (blob `cfff572069006a4a9cbc24750bc224d5bd827444`,
unchanged at HEAD). Freeze `8fcda41c96cbf00b113d2c8e136cc14e7fcaba0b` (2026-10-26T14:12:51-03:00 =
17:12:51Z).

## 1. Carrier pin and fixture identity

| check | command | result |
|---|---|---|
| pin | `cp corpus/evidence/round-37/c1/K4/carrier.bin $S/ && sha256sum` | `a29ddc15…dfe956ed` = frozen pin, `stat -c %s` = 307 = frozen `size_bytes` (exit 0) |
| pin at freeze | `git show 8fcda41c…:corpus/evidence/round-37/c1/K4/carrier.bin \| sha256sum` | `a29ddc15…dfe956ed` (identical at freeze and at HEAD; last touched by round-37 commit `77091b49`) |
| `carriers.json` immutability | `git rev-parse 8fcda41c…:.ufo/…/carriers.json HEAD:.ufo/…/carriers.json` | both `061de280…` — frozen pin table untouched since freeze |
| BE v4 / no-pad, independent parse | hand-parse of the 96-byte superblock (no REA, no unsquashfs) | `magic=b'sqsh' inodes=5 block_size=131072 frags=1 comp=1 block_log=17 flags=192 ids=1 version=4.0 root_inode=128 bytes_used=307 pad=0` |
| K3/K4 relation | `head -c 307 …/K3/carrier.bin \| sha256sum`; `tail -c +308 …/K3/carrier.bin \| tr -d '\000' \| wc -c` | `a29ddc15…` and `0` → K3 is exactly K4 + 3789 NUL bytes, matching the frozen kinds "4k padded" vs "no padding" |
| fixture provenance (corroborated, not re-fetched) | `corpus/SOURCES.md:119` (S113) | unblob 26.6.4 LFS pointer for `squashfs_v4.nopad.bin`: `oid sha256:a29ddc15…dfe956ed / size 307` — same pin and size [INFERENCE: LFS object itself not fetched] |

## 2. Independent REA after-run

Invocation (scratch, `cd "$S"` first so `unblob.log` lands in scratch):

```
REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob npx -y rea-agents@6.5.0 extract-firmware \
  --format json --full-output $S/carrier.bin $S/re/out1     # exit 0, 12083 B envelope
```

Repeated into a second fresh outdir (`re/out2`, exit 0) to separate per-run fields from content.
Envelope hashes retained: `re-env2.json` `255302472bcf…bf82657`, `re-env3.json` `dbd790d3e7f7…1b2fa161`.

Comparison against `corpus/evidence/round-39/c1/K4/after.json` (committed bytes
`34a1869e796a92a2ceab6c2fee9d21bec1049b909891c8a4e2e3aab887aa43b0`, 13145 B — equals `run.json`'s
claimed `receipt.sha256` / `receipt.bytes`).

| demanded field | committed | fresh run | match |
|---|---|---|---|
| chunk handlers | `["squashfs_v4_be"]` | `["squashfs_v4_be"]` | yes |
| chunk `extraction_failed` | `[false]` | `[false]` | yes |
| chunk range / root_file_range | `{0,307}` / `{0,307}` | identical | yes |
| `(relative_path, sha256)` set in `normalized_result.files` | `firmware.bin_extract/apple{1..4}.txt` → `6181259c…`, `919fc82d…`, `2d95014e…`, `08d9b05b…` | identical 4/4 (also identical `size=7`, `mime_type=text/plain`, `analysis_depth=1`, `reported_sha256`) | yes |
| `extraction_gaps` `(kind, relative_path)` | `[]` | `[]` | yes |
| `unpublished_entries` `(relative_path, link_target)` | `[]` | `[]` | yes |
| `diagnostics` `__typename__` set | `[]` | `[]` | yes |
| raw-report `__typename__` set | `ChunkReport, FileMagicReport, HashReport, StatReport` | identical | yes |
| magic line | `Squashfs filesystem, big endian, version 4.0, zlib compressed, 307 bytes, 5 inodes, blocksize: 131072 bytes, created: Wed Mar 2 12:07:37 2022` | identical | yes |
| `coverage` / `published_bytes` / `selection` / `subject.digest` | `complete` / 28 / `{0,307,a29ddc15…}` / `a29ddc15…` | identical | yes |
| envelope-level `authority`, `confidence`, `limitations`, `locations`, `evidence_links`, `relationship_coverage`, `provider`, `operation`, `predicate_type`, `analysis_profile`, `environment`, `parameters` (modulo paths) | — | identical | yes |

Whole-payload checks (files retained in artifacts):

* `strict.diff` (0 lines) — `jq -S` of the committed receipt vs the fresh envelope's `.data`, after
  tokenising only transient paths (`/fast/scratch/hyaku/kaidoku-r39/…`, `/tmp/rea-firmware-…`),
  per-run blob ids (`"<digits>:1"`) and `"ev_<hex>"`. **Zero residual differences** across
  `normalized_result`, `raw_result`, `limitations`, `locations`, everything.
* `ko.diff` (0 lines) — same normalisation on **insertion-order** compact JSON, so key ordering is
  preserved too: the committed `after.json` is byte-shaped like REA's `.data`, not a hand-authored
  object.
* Wrapper arithmetic: fresh envelope 12083 B − `.data` 12006 B = **77 B**; committed envelope claim
  13222 B − 13145 B = **77 B** — identical wrapper overhead (`{"ok":true,"data":…,"meta":{…}}`).
* Only genuine per-run variance observed: `evidence_id`, `subject.local_path`, `parameters.path`,
  `parameters.output_directory`, `normalized_result.output_directory`, `…/rea-firmware-XXXXXX`
  working paths, and `provider_id`/`provider_blob_id` (`2889070:1`, `795735:1`, `1427089:1` across
  three runs — a run-scoped blob id; no frozen clause binds it, and `c1-counter.py` never reads it).

## 3. Oracle check — `sasquatch-v4be` independently of unblob/REA

```
$HOME/.local/bin/sasquatch-v4be -be -no-exit-code -f -d $S/or/x $S/carrier.bin    # exit 0
# Reading a different endian SQUASHFS filesystem … created 4 files / created 1 directory /
# created 0 symlinks / created 0 devices / created 0 fifos / created 0 sockets / created 0 hardlinks
```

* `sha256sum or/x/apple*.txt` vs the `(relpath, sha256)` rows of `corpus/evidence/round-37/c1/K4/oracle.tsv`
  (oracle file sha256 `638a6f75…477d23`): `diff` **empty** → 4/4 files, 4/4 digests, sizes 7 B
  (`apple1\n` … `apple4\n`).
* Symlinks: `find or/x -type l | wc -l` = **0**; `corpus/evidence/round-39/c1/K4/symlinks.tsv` is a
  0-byte file (sha256 `e3b0c442…b855` = empty-input digest), consistent with `carriers.json`
  `symlinks_in_tree: 0, symlinks_escaping: 0`. Nothing for sasquatch to keep and nothing for unblob
  to remove, so the "in-tree kept / escaping removed only by unblob" rule is vacuously satisfied on
  K4 — and the receipt therefore carries zero `unpublished-entry` gaps, exactly as required.
* Cross-check: receipt `files[].relative_path` are `firmware.bin_extract/appleN.txt`, i.e. the
  oracle rows match on relative-path **suffix** as the frozen `oracle_hits` clause requires.

## 4. `run.json` internal consistency

| item | check | result |
|---|---|---|
| argv vs argv_shell | strip the `REA_UNBLOB_COMMAND=… ` prefix from `argv_shell`, compare to `argv` joined | `true` (npx -y rea-agents@6.5.0 extract-firmware --format json --full-output ⟨lane K4 carrier⟩ ⟨K4-scratch/extract⟩) |
| cwd / extraction_root / output_directory | `cwd = /fast/scratch/hyaku/kaidoku-r39/l1/c1runs/K4-scratch`, `extraction_root = …/K4-scratch/extract` = `parameters.output_directory` = `normalized_result.output_directory` | consistent; outdir is under this round's `/kaidoku-r39/` segment |
| UTC times | `start_utc 2026-10-26T17:17:00Z`, `end_utc 17:17:04Z`, `duration_ms 3972` | start is **4 min 9 s after** the freeze commit time 17:12:51Z; end−start = 4 s matches duration_ms; both precede the recording commit `6fdaf4f1` (17:18:32Z) |
| sasquatch-v4be | claimed `sha256 fac88740f49b3460db6a67be93aa21e7390e2845b1e2f348265a95419b7214c6`, `version 4.5.1` | actual binary sha256 **matches**; `-version` prints `unsquashfs version 4.5.1 (2022/03/17)` = claimed `version_line` |
| unblob | claimed `0ce7b624f540c2191ff144892584997fe3fb6ab28ab6ef6b88639f8a7cba1d09`, 26.6.4 | actual matches; `env_value` `/home/vgpnk/.local/bin/unblob` is a symlink whose `readlink -f` = claimed `command_env` `/home/vgpnk/.local/share/uv/tools/unblob/bin/unblob` |
| reachability | `child_path` contains `/home/vgpnk/.local/bin` | `true` → sasquatch-v4be was on the child PATH |
| receipt | claimed `sha256 34a1869e…aa43b0`, 13145 B, `evidence_id ev_138122bb…7058` | actual file sha256/bytes/evidence_id **match**; `previous_after_json_sha256: null` is consistent with the file's git history (single first-add) |
| envelope_data_summary | compared against the receipt itself | `files 4`, `published_bytes 28` (=4×7), `gaps 0`, `handlers ["squashfs_v4_be"]`, `coverage complete`, `unpublished_entries []`, `selection_sha256 = subject_sha256 = carrier pin`, same `output_directory`, same `evidence_id` — all consistent |
| envelope record | `envelope.sha256 a7c33238…`, `bytes 13222` | **not independently verifiable** (raw envelope not committed). Plausibility: 13222 − 13145 = 77 = the wrapper delta my own runs exhibit exactly, and the payload hash matches. [INFERENCE] consistent, unproven |

## 5. Extra provenance checks (beyond the assignment)

1. **Evidence-id recompute under the frozen rule** (`tools/round-27/xpin-attribute.mjs`, 6.5.0
   `semanticProjection` + `digestCanonicalValue`, run from scratch):
   * committed `after.json` → `ev_138122bb…7058` (stored) == recomputed `ev_138122bb…7058` under
     both 6.5.0 and 6.7.0 → attribution `both`;
   * my fresh envelope `.data` → stored `ev_7cdd13cb…f4f4cf4f` == recomputed `ev_7cdd13cb…` → `both`.
   So the receipt is content-addressed (including `parameters` and `raw_result`), which is why its id
   cannot be transplanted onto a re-minted payload, and why an edit to a hashed field must change it.
2. **Before-arm (negative control) to prove causality of the sasquatch clause.** Same command with
   `/home/vgpnk/.local/bin` removed from the child PATH (node/npx still reachable, `REA_UNBLOB_COMMAND`
   still absolute) → exit 0, but `coverage: "partial"`, `files: 0`, `extraction_failed: true`, and one
   gap `{kind: "missing-extractor-dependency", dependencies: ["sasquatch-v4be"]}`. The committed
   receipt's clean 4/4 therefore reflects a real sasquatch-backed run, not an oracle-derived
   fabrication. (Envelope retained: `before-env.json`, `7068a4d5…729e30`.)
3. **Receipt lineage**: the only commits touching `K4/after.json` are `6fdaf4f1` and its jj keep twin
   `41aee041` (`refs/jj/keep/…`, same commit timestamp, same blob `cfff5720…`) — the receipt has not
   been rewritten after landing; `8fcda41c…` is an ancestor of `6fdaf4f1`, which is an ancestor of HEAD.
4. **Not a round-38 copy**: `corpus/evidence/round-38/c1/K4/after.json` is byte-different
   (`ev_4348dcaf…`, outdir `/fast/scratch/hyaku/kaidoku-r38/l1-receipts/K4-after`); the round-39 receipt
   names `…/kaidoku-r39/l1/c1runs/K4-scratch/extract` and its id recomputes to that payload.
5. **Per-carrier discrimination**: `selection`/chunk range lengths are 9780/1606/4096/307/26813/15867
   for K1..K6, so K4's `{0,307}` receipt cannot be an alias of the padded K3 receipt (4096) even
   though both publish the same four apple files (verified: their file-time sha256 sets are identical,
   which is expected — K3 is K4 plus NUL padding).
6. **Frozen predicate shape** (read-only): `c1-counter.py` validates receipt fields plus
   `run_provenance_ok` (outdir under `/kaidoku-r39/`) and `evidence_id_ok`; it never re-executes REA on
   the carrier. So this seat's independent re-run is exactly the provenance evidence the counter
   cannot supply — and it agrees.

## 6. Anomalies / limits (none fatal)

* **REA first-call behaviour (reproducer trap, not a lane defect):** pointing `--full-output` at a
  path whose parent directory does not exist fails with exit 1 and
  `{"code":"execution_failure", "details":{"diagnostics":{"reason":"Extraction output parent is unavailable"}}}`
  — it does *not* create parents. `mkdir -p` the parent, then pass a non-existent *leaf* outdir.
* `run.json`'s `envelope.sha256`/`bytes` are unverifiable from stored evidence (above); everything
  else in `run.json` is confirmed against the live filesystem.
* `provider_blob_id`/`provider_id` are run-scoped; two identical-input runs differ. No frozen clause
  or counter check reads them, so this is not a defect, but a future counter that bound them would be
  non-reproducible.
* K4 exercises no symlink leg (`symlinks.tsv` empty): the "escaping links removed only by unblob,
  in-tree kept" behaviour is untested here by construction and must be judged on K1/K2/K5/K6.

## 7. Retained evidence (artifacts dir)

`.ufo/waves/round-39/w2/artifacts/R39W2ReproK4/`

| file | content |
|---|---|
| `committed-after.json` | byte copy of `corpus/evidence/round-39/c1/K4/after.json` (sha256 `34a1869e…`) |
| `re-env2.json`, `re-env3.json` | two independent fresh after-arm envelopes |
| `before-env.json` | negative control (no sasquatch on child PATH) |
| `strict.diff`, `ko.diff` | 0-line diffs (sorted and insertion-order) vs committed payload |
| `oracle.tsv`, `mine.tsv` | sasquatch `-be` extraction digests vs frozen oracle, `diff` empty |
| `superblock.txt` | hand-parsed K4 and K3 superblocks (magic/version/comp/bytes_used/pad) |
| `xpin.txt` | evidence-id recompute, committed and fresh payloads |
| `env-shas.txt` | sha256 of the three envelopes |

## 8. Tooling record

No installs, upgrades or removals. Used as found: `rea-agents@6.5.0` from the npx cache
`/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`; `unblob 26.6.4`
(`/home/vgpnk/.local/share/uv/tools/unblob/bin/unblob`, via `~/.local/bin/unblob`);
`sasquatch-v4be 4.5.1` (`fac88740…14c6`); node/npx from the fnm multishell path; `python3`, `jq`,
`sha256sum`, `diff`, `od`. No pacman transaction, no host service touched, no VCS mutation (read-only
`git show/log/rev-parse/merge-base`).

**Risks carried forward for the integration owner:** the `envelope.sha256` field in each round-39
`run.json` is unverifiable by construction (envelope not committed); if a gate ever verifies it, the
raw envelope must be retained. K4 cannot support any symlink-gap conclusion.
