# R39W2ReproK1 — provenance attack on the committed R39-C1 receipt, carrier K1

**Verdict: CONFIRMED** — every semantic field of `corpus/evidence/round-39/c1/K1/after.json` is reproduced by an
independent REA 6.5.0 after-run of the pinned K1 carrier, the committed bytes are byte-identical to the run's own
surviving output artifacts, and the receipt is internally consistent with `run.json`, the frozen pins, the
independent `sasquatch-v4be` oracle and the frozen 6.5.0 evidence-id rule. No fabrication signature found.

Seat: R39W2ReproK1 (leaf). Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`; measured revision
`6fdaf4f162aff156fcef0e52998a5469c64fd6f0`; freeze `8fcda41c96cbf00b113d2c8e136cc14e7fcaba0b`.
Artifacts: `.ufo/waves/round-39/w2/artifacts/R39W2ReproK1/` (`k1-provenance.json`, `k1-fresh-envelope.json`,
`repro.txt`, `c1-counter-at-6fdaf4f1.json`, `c1-counter.stdout|stderr`). Scratch `S=/fast/scratch/hyaku/kaidoku-r39/R39W2ReproK1`
removed at the end. No `corpus/`, `tools/`, `plans/`, `PROVINCE.md`, `SKILL.md`, `LOG.md` byte was read-modified and
no VCS mutation was run (only `show`/`log`/`cat-file`/`ls-tree`/`diff`/`rev-parse`/`merge-base`/`for-each-ref`).

## 1. Carrier pin and frozen inputs

| item | expected (carriers.json / freeze) | measured |
|---|---|---|
| `carrier.sqsh` sha256 (scratch copy and working tree) | `1cfb6c33f915aa64255465fba9f2074bb0f294a192f3e3058cb34bea8286117e` | same |
| carrier blob `49f5924` at freeze **and** at HEAD (`git cat-file -p … \| sha256sum`) | same pin | `1cfb6c33…` |
| `size_bytes` | 9780 | 9780 |
| `oracle.tsv` blob `4ee5525` | `0c993e7421338a8c08e311914f71e0ebf9fda2849931b4f544e3774c78f13aab` | same |
| `K1/symlinks.tsv` blob `3165033` | `3680e6931d79cc5b8be635d35083091e0b4ef8e0c90404a1062001442629f71d` | same |
| committed `after.json` | — | `3f4506879a6e48a2b4327e27c5cf9b7e786676c854b955e3033777d80883d9ee` (19238 B) |

`git diff --name-status 8fcda41c 6fdaf4f1` over the frozen C1 paths (`carriers.json`, `c1-counter.py`,
`c1-run.sh`, `plans/round-39-claims.md`, `corpus/evidence/round-37/c1/K1/`) is **empty**: no frozen byte moved
between freeze and measured revision, so the pin I attacked is the pin the claim froze.

## 2. Independent after-run (the discriminator a receipt-only counter lacks)

```
cd "$S" && REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob \
  npx -y rea-agents@6.5.0 extract-firmware --format json --full-output "$S/carrier.sqsh" "$S/out1"
exit=0   fresh outdir   envelope 17252 B   stderr 0 B
```

Tool identity of my arm, matching `run.json`: `unblob` 26.6.4 sha256 `0ce7b624f540c2191ff144892584997fe3fb6ab28ab6ef6b88639f8a7cba1d09`
(`$HOME/.local/bin/unblob` is a symlink to `…/uv/tools/unblob/bin/unblob` — this explains the
`unblob.env_value` vs `unblob.command_env` pair in `run.json`, so it is not a discrepancy),
`rea-agents` 6.5.0 at `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`,
`sasquatch-v4be` sha256 `fac88740f49b3460db6a67be93aa21e7390e2845b1e2f348265a95419b7214c6`, `-version` line
`unsquashfs version 4.5.1 (2022/03/17)` — all three equal to the `run.json` records.

Comparison of my fresh envelope against committed `after.json` (script `k1-provenance.json`):

| semantic field | result |
|---|---|
| `normalized_result.files` — set of (`relative_path`, `sha256`, `size`, `mime_type`, `analysis_depth`) | **equal**, 5/5 (`firmware.bin_extract/{bin/run, docs/readme.md, docs/deep/nested/file.dat, empty, hello.txt}`) |
| `normalized_result.chunks` — (`input_path`, `handler`, `encrypted`, `extraction_failed`, range) | **equal**; one chunk, handler `squashfs_v4_be`, `extraction_failed: false`, range 0..9780. Differs only in `provider_id` (`2559184:1` vs my `3963589:1`), a per-run blob counter, not semantic |
| `normalized_result.extraction_gaps` — (`kind`, `relative_path`) | **equal**, `[]` in both (K1 has 0 in-tree symlinks, so 0 `unpublished-entry` gaps is the right cardinality) |
| `normalized_result.unpublished_entries` — (`relative_path`, `link_target`) | **equal**, `[]` in both |
| `normalized_result.diagnostics` — `__typename__` set | **equal**, exactly `{MaliciousSymlinkRemoved}` (one WARNING naming `…/firmware.bin_extract/link-to-hello` → `…/extracted/hello.txt`); the absolute paths differ, as they must between two runs |
| `normalized_result.derivations` | **equal** on (`parent_path`, `child_path`, `handler`), incl. the root edge `$input → $output/firmware.bin_extract` with handler `squashfs_v4_be` and range 0..9780; only `provider_blob_id` differs |
| `coverage` / `published_bytes` | `partial` / 9656 in both; 9656 = Σ file sizes exactly |
| `engine`, `selection`, `provider`, `operation`, `confidence`, `authority`, `limitations`, `locations` | equal |
| `parameters` except `path`/`output_directory` (`max_depth` 3, `max_output_bytes` 268435456, `max_output_files` 10000) | equal |

`selection.sha256` and `subject.digest.sha256` are both the K1 carrier pin, so the envelope is bound to this
carrier, not to another round-39 carrier or to oracle-derived data.

## 3. Oracle check (`sasquatch-v4be`, independent of unblob and of the receipt)

```
cd "$S" && sasquatch-v4be -be -no-exit-code -f -d x carrier.sqsh   # exit 0, "6 inodes (6 blocks)", created 5 files, 5 dirs, 1 symlink
```
Files: `bin/run 299001868f…`, `docs/deep/nested/file.dat b7e769c3…`, `docs/readme.md 98f8c3bf…`,
`empty e3b0c442…`, `hello.txt 0da24910…` — **5/5 sha256 and size equal to `corpus/evidence/round-37/c1/K1/oracle.tsv`**.
Links: exactly one, `link-to-hello -> ../hello.txt`, **escaping**, equal to `K1/symlinks.tsv` (`symlinks_in_tree: 0`,
`symlinks_escaping: 1`). `sasquatch` materialises the escaping link; my unblob arm removed it
(`MaliciousSymlinkRemoved`) and the published tree on disk equals the oracle exactly (5 files, no `link-to-hello`),
i.e. the claim's division of labour ("removed only by unblob, not by sasquatch") holds on this carrier.

## 4. `run.json` internal consistency

* `argv` = `npx -y rea-agents@6.5.0 extract-firmware --format json --full-output <frozen carrier> <…/K1-scratch/extract>`
  — the authorised CLI shape, single arm, no `--` rewrite; `cwd` and `extraction_root` and
  `parameters.output_directory` in `after.json` are all `/fast/scratch/hyaku/kaidoku-r39/l1/c1runs/K1-scratch[/extract]`,
  so `run_provenance_ok` (`/kaidoku-r39/` segment) is genuine and **every** `files[].path` is a prefix-extension of
  `extraction_root` (checked, 0 exceptions).
* Times: `start_utc 2026-10-26T17:16:39Z`, `end_utc 17:16:43Z`, `duration_ms 4183` (internally coherent).
  Freeze commit committer time `2026-10-26T14:12:51-03:00` = `17:12:51Z`; receipt commit
  `6fdaf4f1` = `17:18:32Z`. The run therefore sits **4 min after the freeze and 2 min before its own commit** —
  after-freeze, before-data-commit ordering holds.
* `exit 0`, `stderr_head ""` (the run's own log `/fast/scratch/hyaku/kaidoku-r39/l1/c1runs/K1.log` is 0 bytes),
  `envelope.parseable/ok true`, `data_extracted true`, `receipt_written true`.
* `receipt.sha256 3f450687…` **equals** the actual sha256 of the committed `after.json`;
  `receipt.evidence_id ev_2ed128…` equals `after.json.evidence_id`; `receipt.handlers ["squashfs_v4_be"]`,
  `files 5`, `gaps 0`, `published_bytes 9656` all agree with the receipt body.
* `previous_after_json_sha256: null` — consistent with a first, non-amending run (no overwritten prior receipt).
* `sasquatch_v4be` and `unblob` path/sha256/version fields match the installed binaries byte-for-byte (§2).
* `envelope.sha256 8c2948fc…` / `bytes 19315`: the file is not retained (`c1-run.sh` copies
  `after.envelope.json` only under `C1_KEEP_ENVELOPE=1`), so the digest itself is not recheckable. Its **size is
  arithmetically exact**: committed `after.json` is `jq -c` compact output, 19237 B + trailing LF = 19238 B, and
  19315 − 19237 = **78** B of envelope wrapper (`{"ok":true,"data":…,"meta":{"command":…,"duration":…}}`) — my own
  6.5.0 envelope gives 17252 − 17174 = **78** B for the same wrapper. [INFERENCE] that 19315 is a real 6.5.0
  envelope byte count; the digest cannot be re-derived without the file.
* `[INFERENCE]` the extraction tree itself was removed with the scratch, so the recorded absolute
  `files[].path`/`diagnostics.link` targets cannot be re-hashed post hoc; their *contents* are re-established by
  §2/§3 against the oracle.

## 5. Provenance chain: committed bytes are the run's bytes, not a later edit

`/fast/scratch/hyaku/kaidoku-r39/l1/c1runs/K1-out/` still exists (mtime Oct 26 14:16 local = 17:16Z, i.e. between
the run's start/end timestamps):
`cmp` of `K1-out/after.json` vs the committed receipt and `K1-out/run.json` vs the committed `run.json` are both
**identical** (`3f450687…`, `5761e619cc6f0721ec1995a494779dd34003b54f2d1a54a9b7ec6eac35a5b365`). The committed
files are therefore a byte copy of the artifacts the run wrote, and the receipt body was not re-minted after the
commit — the failure mode CTL-C1-3 exploits.
`after.json` is byte-stable across `6fdaf4f1`, `41aee041` and `HEAD` (`git show <rev>:… | sha256sum` all
`3f450687…`). `41aee041` is a stray jj working-copy commit (only `refs/jj/keep/…` contains it; not an ancestor of
`HEAD`, no branch), so `git log --all -- corpus/evidence/round-39/c1/K1/after.json` shows two hits while the
measured history holds exactly one.

## 6. Evidence-id rule (6.5.0) re-applied independently

`node tools/round-27/xpin-attribute.mjs --pkg65 <rea-agents 6.5.0 root> --pkg67 <same> wrap_{theirs,mine}.json`

```
wrap_theirs.json  ev_2ed128bee22a7262f47ba5323016a2617e4c6a765958da428f05d95a0f5dbe4c  … … both
wrap_mine.json    ev_8e1df365b9c92be9a90eefef32f0737f45db05892b461f6a1e6348b4cc0e116e  … … both
```
Both envelopes recompute to their stored ids under the frozen rule (which imports the pin's own
`semanticProjection`/`digestCanonicalValue`; nothing was retyped by me). The committed receipt is a
self-consistent hashed envelope, and — because `parameters.output_directory` is inside that projection — its
`/kaidoku-r39/…` provenance segment cannot have been edited without breaking the id.

## 7. Frozen counter re-run at the measured revision (independent, read-only)

```
HYAKU_SCRATCH=$S TMPDIR=$S python3 -I -B tools/round-39/c1-counter.py --root <lane> --rev 6fdaf4f1… \
  --freeze 8fcda41c… --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents  → exit 0
```
`met_target: true`, `carriers_matched: 6`, `frozen_path_changed: []`, `carriers_unchanged: true`; K1 has **no false
clause** (`receipt_fresh: true`, first add `6fdaf4f1`, `gaps_note "0 gaps == 0 in-tree symlinks"`,
`published_files 5 == oracle_hits 5`, `superblock_compression 1` = gzip). This is byte-for-byte the author's
`l1/scores/c1-at-6fdaf4f1.json` verdict, so the counter is reproducible — but it remains receipt-only, which is
why §2/§5 carry the verdict.

## 8. Findings and limits

* **No defect found on the K1 receipt.** No field diverges, no path/order/handler/gap anomaly, no escaping-symlink
  leak, no extra or missing published file, no stale or re-minted evidence id, no post-freeze frozen-path edit.
* Non-findings, for the record: `coverage: partial` with one non-failed chunk is what this single-chunk carrier
  produces in my arm too, so it is not a truncation signal; `provider_id`/`provider_blob_id` and the diagnostics'
  absolute paths differ between runs by design and were excluded from the equality set.
* Limits: the two post-hoc-unverifiable items are the envelope digest (`8c2948…`, file not retained) and the
  extraction tree's on-disk existence (scratch removed); both are bounded by §4's byte arithmetic and §2/§3's
  content agreement. This seat attacked K1 only — K2..K6 receipts, the `PROVINCE.md`/entry/README doc clauses and
  R39-C2 are other seats' surface.
* No tools installed or upgraded in this wave (`unblob`, `sasquatch-v4be`, `npx rea-agents@6.5.0` were already
  present and unmodified; their hashes match the ones `run.json` records).
