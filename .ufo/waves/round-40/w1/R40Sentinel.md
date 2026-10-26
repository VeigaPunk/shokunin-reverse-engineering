# R40Sentinel — round-40 wave-1 seam check

**VERDICT: DEFECTS FOUND** — the round-start seam is mostly clean (no kaidoku work leaked into the fleet
root, no real secret, no VCS mutation, no frozen-carrier REA run), but four seam defects and three
out-of-band risks need action before the freeze, two of them inside the R40-C1 draft's own predicate.

Seat: `R40Sentinel` (leaf). Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, HEAD
`fa6a8a3f85ec65946b3a54d37c0ddd1d6748664f`, `main` = `fa6a8a3f` (jj `@` = `lxzrukpp 682ffc01` empty,
parent `ynwzrmtz`). Scratch `S=/fast/scratch/hyaku/kaidoku-r40/R40Sentinel` (removed at exit).
Artifacts: `.ufo/waves/round-40/w1/artifacts/R40Sentinel/` (files cited below by their `NN-` prefix).

Nothing was installed; no `pacman`, `uv`, `npx -g`, no tool upgrade was needed. No VCS command beyond
read-only `git` (`status`, `log`, `ls-files`, `ls-tree`, `grep`, `rev-parse`, `count-objects`,
`cat-file`, `show`) and one `jj status` (see §3-N4 for the post-check that it wrote nothing).

---

## 1. The six seam items

### 1.1 Fleet root — clean (one unrelated file)

`git -C /home/vgpnk/Projects/shokunin status --porcelain -uall` returns exactly one entry
(`01-fleet-root.txt`):

| path | size | first line | names kaidoku / round-39 / round-40 |
|---|---|---|---|
| `.ufo/reports/round-48/tameshi.md` | 11014 | `# tameshi — round 48 report (attempt 3, L1 TameshiR48a3)` | **0 matches** |

No kaidoku round-39/40 file sits outside the lane. `.ufo/reports/round-40/` does not exist yet;
`.ufo/reports/round-39/kaidoku.md` (15280 B, 14:57) is the round-39 closure. `.ufo/state/` and
`.scratch/` were not read (bounds).

### 1.2 Leftover scratch and `/tmp` — three leftovers, one of them a cross-round reuse

Top level of `/fast/scratch/hyaku/` (`ls -la`, no find/du): `kaidoku-r37`, `kaidoku-r38`,
`kaidoku-r40` (this round), plus other lanes. No `kaidoku-r39` (round 39 cleaned correctly).

| leftover | content | age | note |
|---|---|---|---|
| `/fast/scratch/hyaku/kaidoku-r37/selftest/green/` | a `.git` fixture repo + `PROVINCE.md` (75 B) | **14:41 today** | written *during the round-39 window* (13:00–14:57), i.e. a round-39 seat used a **round-37** scratch path |
| `/fast/scratch/hyaku/kaidoku-r38/{controls-c1-1,controls-c1-2,controls-c2-1..3}/` | 5 empty dirs | 13:44 / **14:42** | same: round-39 seats created dirs under the round-**38** root |
| `/fast/scratch/hyaku/kaidoku-r38/mint.wrapped.json` | 11246 B, REA **MCP** envelope `{"data": {"evidence_id": "ev_6edec5a4…", "subject": {"local_path": "/fast/scratch/hyaku/kaidoku-**r36**/L1-probe/sq/le-xz.sqsh"…}}}` | **14:41 today** | an `ev_` receipt-shaped object whose subject was produced in round 36 and no longer exists |
| `/tmp/kaidoku-r39-census-start.txt` | 1205 B, sha256 `fbb81df1…09ba5` | 13:07 | byte-identical to the committed `.ufo/waves/round-39/census-start.txt` → redundant copy, safe to delete |

A per-seat scratch convention (`kaidoku-r<N>/<seat>`), created today at 15:17, is being honoured by
round 40 at the top level, but the r37/r38 writes show the convention was **not** enforced last round.

### 1.3 Lane status — only the draft and its wave tree are untracked

`03-lane-status.txt`:

```
$ git status --porcelain
?? .ufo/waves/round-40/
?? plans/round-40-claims.md
$ git status --ignored --porcelain | head
?? .ufo/waves/round-40/
?? plans/round-40-claims.md
!! .jj/
!! .ufo/waves/round-34/r34b/w1/CtlMultiset-files/__pycache__/
!! tools/round-34/mini-fix/__pycache__/ … tools/round-38/__pycache__/   (6 pycache dirs)
```

Loose entries at the lane root that `git add -A` would also see: `unblob.log` (**tracked**, see §2.4),
`res/` (empty, untracked), `kaidoku-r26/` (tracked, 1 file), `glibc-tag-object.json` (tracked),
`evidence/` (tracked, 4 files). `git count-objects -v`: 10540 loose, 4 packs, 20053 in-pack — a loose
object pile that the L1's commit will not gc.

### 1.4 Secrets — no real secret; 16 pattern hits are all self-referential; absolute paths are systemic

`04-secrets.txt`. Scope 1941 tracked files under `.ufo/waves/round-39/` + 147 under
`corpus/evidence/round-39/`.

| pattern family | hits in `.ufo/waves/round-39` | hits in `corpus/evidence/round-39` |
|---|---|---|
| `ghp_/gho_/ghs_/github_pat_/sk-…/xox[baprs]-/AKIA…/npm_…/BEGIN … PRIVATE KEY/op://` | **16** (5 files) | **0** |
| `Authorization: Bearer` or `(api_key|secret|password|token) =/:` | 0 files | 0 files |
| real private-key blocks anywhere in the lane | 5 files, all sentinel/hygiene reports quoting the pattern | — |

All 16 hits are the patterns **quoted as text** inside `w1-gen.py`, `w1-spec.json`, `w1-dispatch.json`,
`R39Sentinel.md`, `04-secrets.txt`, `R39W2Sentinel.md` (e.g. `op:///xox`, `"3_secrets": "ZERO. sk-/ghp_/…`).
Zero credentials. **But absolute paths are endemic**: `/home/vgpnk` appears in **72** evidence files and
**670** wave files; `/fast/scratch` in **52** evidence files and **713** wave files. That is the lane's
own convention (C1's `run_provenance_ok` *depends* on the receipt recording `/kaidoku-r39/`), so it is
not a defect — it is the reason §2.1 matters: the path inside a receipt is an assertion, not evidence.

### 1.5 `~/.omp/agent` config — unchanged inside both round windows

`05-omp-config.txt`. `mcp.json` mtime **2026-10-25 02:32**, `config.yml` **2026-10-26 00:50**; round 39
started 13:00:45 and round-40 wave 1 at ~15:17, so **no mid-round config drift**. Nothing edited.
The static content is the hazard, not a change: `mcp.json` mounts `"rea": {"command": "npx", "args":
["-y", "rea-agents@**6.7.0**", "mcp"]}` — the device the bounds forbid is live, and it is **not** the
pinned 6.5.0. Host REA trees under `~/.npm/_npx/*/node_modules/rea-agents`: `ad9a3fdbcad992c6` = **6.5.0**
(the pinned root), `dea9475797100b20` = **6.4.0**. Two live `rea-agents@6.7.0 mcp` servers have been up
8200 s. So three REA versions resolve on this host and only one is pinned (see §2.3).

### 1.6 Carrier size vs the lane repo, and the LFS state

`06-repo-size-lfs.txt`.

| quantity | value |
|---|---|
| tracked files / bytes | 26472 / 372,523,119 B |
| `.git` / `.git/objects` | **143 MB** / 136 MB (4 packs, 10540 loose) |
| largest tracked blob | 10.7 MB (`round-20/w1/patches/WasmCompareLeg-2.patch`) |
| existing committed *binary* precedent | 26 KB `K5/carrier.sqsh`, 2.3 MB jsonl, 6.2 MB json |
| round-39 cost of a scored round | waves 12,537,967 B + evidence 2,133,040 B; **carriers 1,204,162 B / 22 files** |
| round-40 tree at 15:24 (untracked) | **10,255,742 B**, of which 5,442,392 B is one carrier |
| V1 carved carrier in the tree | `artifacts/R40C1VendorV1/carrier-v1-be.sqsh` = **5,442,392 B**, sha256 `ac4098bd…e95` |
| V1 tar member / V1 image | 5,443,592 B / **39,741,440 B** (live `HEAD`: `Content-Length: 39741440`, 2026-09-04) |
| V2 candidates (measured by `R40C1VendorScout/candidates.tsv`) | AVM-BE members **21.2–35.8 MB** for 3490/5490/5491/6820/7430/7560/7581/7582/7590, **5.44 MB** for the 6490/6590 `var/remote/var/tmp` member |
| `.gitattributes` | **absent** in the lane **and** in the fleet root; 0 tracked paths match |
| git-lfs | `git-lfs/3.8.0` **installed**, **0** pointer files, no `.git/lfs`, no `pre-push` hook |
| remote | `https://github.com/VeigaPunk/shokunin-reverse-engineering.git` |
| second VCS in the lane root | `.jj` (store type `git`, so no duplicate object store) |

Arithmetic for the freeze: V1 5.44 MB + V2 (21–36 MB if a different model is chosen) + L1/L2 (KB) ≈
**27–42 MB of already-compressed binary**, i.e. **+19–29 %** on today's 143 MB `.git` in one commit,
with no delta compression possible. V1 alone grows the tree 13× the whole round-39 carrier set.
GitHub's 50 MB warning / 100 MB rejection are documented platform limits **[INFERENCE: not re-fetched
this round]**; the 39.7 MB image is under both but the 35.8 MB 7590 member plus the image would not be.

---

## 2. Defects and exploit paths (ranked)

### 2.1 HIGH — R40-C1's rerun binding is content-only, so a *byte-identical* carrier lets a copied round-39 receipt pass without any REA run

Evidence: `09-carriers-and-identity.txt`, `07-projection-invariance/projection-invariance.txt`,
`08-xpin-forgery/xpin.txt`.

Measured: three receipts of the **same bytes** — two fresh REA 6.5.0 runs of an unmodified copy of
`corpus/evidence/round-39/c1/K5/carrier.sqsh` in two different scratch dirs, plus the committed
round-39 K5 `after.json` — project **identically** under the run-invariant projection (73 leaves,
`RESULT: INVARIANT`). So a restricted projection is reproducible; that is what makes the draft's rerun
binding work at all.

Measured, the other way: the whole 6.5.0 `semanticProjection` (`rea-agents/dist/domain/evidence.js:156`)
**diverges between two runs of identical bytes in 163 of 763 leaves** — every `parameters.output_directory`,
every `normalized_result.files[].path`, every `report[].task.path`, every `provider_blob_id`
(`3669366:1` vs `3696185:1`, a wall-clock:counter id), every `execution.args[]` temp dir. The three
whole-record ids are all different: `ev_ac684920…`, `ev_b4e0f407…`, `ev_b69020cd…`.

Consequence for the draft as written ("a fresh REA run … yields the same semantic projection as the
committed receipt (projection fields fixed in the freeze)"): if the freeze takes the 6.5.0
`semanticProjection` verbatim, the predicate is **unsatisfiable by construction**; if it trims to the
restricted set, the predicate becomes a statement about *content* only. And for content-only, this
attack needs no fabricator: for any carrier whose bytes equal a committed round-39 carrier K\*, take
K\*'s genuine receipt, change only `parameters.output_directory` to this round's segment, store the
recomputed id. `08-xpin-forgery/xpin.txt` stage 2 shows that exact record verifying as **`both`**
(stored id == recomputed id) under `tools/round-27/xpin-attribute.mjs`, while stage 1 shows the same
edit *without* a re-mint caught as **`none`** — i.e. `evidence_id_ok` stops an editor, not a re-minter,
and `run_provenance_ok` is a string test that an editor controls. With the restricted projection that
receipt is byte-for-byte projectively equal to a real run of those bytes, so **every** binding passes
and no REA ran.

Smallest remediation (freeze-time, cheap): assert that no round-40 carrier's sha256 is in the K1–K6
pin set (the set is printed in `09-carriers-and-identity.txt`; `tools/round-39/gen-squashfs.py:27,28,185`
fixes `MKFS_TIME = 1700000000`, `UID = 1000`, `mkfs = bytes_used` in avm mode and reads no source mtime,
so a reused tree reproduces bytes exactly and the check is not vacuous). The draft's kill control
"round-39 receipts copied" only covers a copied receipt for a *different* carrier; state that it is
byte-identity that makes it a control.

### 2.2 MEDIUM-HIGH — the freeze must define the projection over measured run-invariant fields, not over all path-bearing ones

`07-projection-invariance/projection-v2.txt`, `v2-divergence.txt`. Starting from the working projection
(73 leaves) I added the extraction bounds and the child exit codes. That variant diverges in **exactly
one leaf**: `bounds[0] = 'k5.sqsh'` vs `'carrier.sqsh'` — the *work filename* a seat chose to copy the
carrier to, not content. Dropping the basename restores invariance, and `receipt_exit = [0, None, 0]`
(exit code, signal, version-check exit) is invariant too.

So the measured run-invariant set is: `subject.digest.sha256`, `subject.format`, `provider.{id,version}`,
`operation`, `engine.{name,version,executable_sha256}`, `selection.{offset,length,sha256}`, `coverage`,
`published_bytes`, `chunks[].handler`, `files[] = (path relative to the extraction root, sha256, size)`,
`extraction_gaps[]` with paths relativised and `provider_blob_id` dropped, `unpublished_entries[]`
relativised, `diagnostics[].report.__typename__` sorted, `depth_limited_paths`, `derivations_n`,
`parameters.{max_depth,max_output_bytes,max_output_files}`, `raw_result.execution.exit_code/signal`,
`raw_result.version_execution.exit_code`. Everything else is run-local and must be excluded: `evidence_id`,
`parameters.path`, `parameters.output_directory`, `normalized_result.output_directory`, all absolute
paths, `provider_blob_id`/`provider_id`, `report[].id/link/target`, `execution.args`,
`execution.command`, stdout/stderr. `projection.py` (73-leaf variant) and `projection-v2.py`
(+bounds/exit-codes, minus basename) in `07-projection-invariance/` are runnable and reproduce the
result from the two runs plus the committed K5 receipt.

Also state in the claim what the binding does **not** prove: a receipt whose provenance *string* is
fabricated but whose content is a real outcome of those bytes passes, because the string is excluded by
construction. That is acceptable — the claim is about the extraction outcome — but "produced by a run of
the pinned carrier" must not be read as run attestation.

### 2.3 MEDIUM — the REA version is not attested anywhere inside a receipt

`04-secrets.txt` tail, `05-omp-config.txt`, and `corpus/evidence/round-39/c2/heldout/H01/{rea-full,run}.json`:
a receipt's `meta` is `{"command": "extract-firmware", "duration": "2526ms"}`; there is no `rea-agents`
version field, no package root, no CLI digest. `provider.version = "26.6.4"` is **unblob's** version.
The version lives only in the seat-written `run.json` field `rea_argv: ["rea-agents@6.5.0", …]`. With
6.4.0 and 6.5.0 trees in `~/.npm/_npx`, 6.7.0 mounted as the MCP device, and an unpinned
`npx -y rea-agents` resolving to latest, one typo produces a receipt indistinguishable from the pinned
one by content — and the claim's "REA 6.5.0 after-receipt" would still read true.

Smallest remediation: the harness records the resolved `node_modules/rea-agents/package.json` `version`
+ the resolved directory (or the `dist/domain/evidence.js` sha256) in `run.json` — a value the harness
computes, never a seat string — and round 40's predicate cites that field. No install/move of any tool.

### 2.4 MEDIUM — a tracked `unblob.log` sits at the lane root; the CWD rule is one slip from embedding a new one in the round-40 commit

`10-unblob-log.txt`. `unblob.log` is **tracked** (2652 B, mode 644, mtime 03:56, sha256
`2d651a4a…9299`, first added in round-38's remediation commit `7a1ac7fe` "…misroot unblob.log"). It is
a *deliberate quarantine* (documented at `corpus/lessons/round-38.md:38`, M38-7), not an accident — but
it is a debug log with absolute scratch paths and extraction-sandbox rules at the repo root, and unblob
writes `./unblob.log` into its CWD. If any round-40 seat runs unblob or REA from the lane root, it
overwrites round-38's frozen bytes and the L1's `git add -A` commits the overwrite as round-40 evidence.
Working tree is clean now (0 local modifications). Same class at the root: the empty `res/` dir and the
one-file `kaidoku-r26/` — `git add -A` sweeps whatever appears in them.

Smallest remediation: the L1 checks `git status --porcelain unblob.log res` before the freeze commit;
no file moves (the quarantine is documented and must keep its bytes).

### 2.5 LOW-MEDIUM — two wave-1 reports are routed inside the artifacts tree

`artifacts/R40SrcAvmVendor.md` (4214 B) and `artifacts/R40SrcReaOps.md` (13359 B) are **regular files
at the top of the artifacts directory**; every other seat's report is at `w1/<Seat>.md`. As-is they
would be committed as artifacts, and the seat would look report-less to any check that globs
`w1/*.md`. Smallest remediation: the L1 relocates them (or their seats do) before the freeze; if they
are moved, the artifact dir keeps the data files it already has.

### 2.6 LOW — stale scratch carries an `ev_`-shaped envelope whose subject is deleted

`mint.wrapped.json` (§1.2) is an REA **MCP**-minted evidence envelope (`ev_6edec5a4…`, subject
`/fast/scratch/hyaku/kaidoku-r36/…/le-xz.sqsh`) that now cannot be re-verified by anyone: the subject
bytes are gone, and per §2.3 the record attests no producer version. It survives under a *round-38*
scratch root, written at 14:41 today. Impact is latent — nothing reads it — but it is exactly the
artifact shape a counter that globs a scratch root for "receipts" would mis-take for evidence. It also
shows the same `tools/round-36|38/selftest/dev-after.json` records inside the tracked tree, so the
pattern is not confined to scratch. No action needed beyond removing the scratch dirs; do not copy it.

---

## 3. What held (negative results, all re-checked)

- **N1** Fleet root carries no kaidoku round-39/40 work (§1.1). Round-38's fleet missroots stay fixed.
- **N2** No real credential in either round-39 tree; 0 hits in evidence; the 16 wave hits are quoted
  patterns (§1.4).
- **N3** `mcp.json`/`config.yml` unchanged since 2026-10-25 02:32 / 2026-10-26 00:50, both before the
  round-39 window (§1.5).
- **N4** No VCS mutation by me: after my one read-only `jj status`, `git rev-parse HEAD` is still
  `fa6a8a3f85ec…`, `git status --porcelain` still shows only the two round-40 entries, and
  `.jj/repo/op_heads` mtime is still **15:04** (`heads/` dir 15:04) — the jj call wrote nothing
  (`03-lane-status.txt`).
- **N5** No REA/unblob run against a C1 carrier is visible in the wave tree: no `rea-*`, `report.json`,
  `unblob.log` or `extract*` entry under `.ufo/waves/round-40/`, and the only V1-derived content is the
  carved carrier itself plus a pure-Python `sq-list` listing (`R40C1VendorV1/sq-list-noflag.txt`,
  108 KB) and the seat's own reports. The frozen-carrier discipline holds at 15:24.
- **N6** No stray round-39 process survives: the only kaidoku `unblob`/`npx rea-agents@6.5.0` processes
  in `ps` belong to live round-40 peers and other lanes. No orphaned sasquatch.
- **N7** `corpus/evidence/round-39` is 2.1 MB of text/JSON; git-lfs is unnecessary at that scale.

## 4. Corrected / confirmed facts for the L1 (not my claim to make, but measured)

- V1's committed carrier is a **`bytes_used` prefix**, not the tar member: carrier 5,442,392 B sha256
  `ac4098bd…e95` vs member 5,443,592 B sha256 `334e56df…3d4` (1200 B of tail dropped;
  `equals_member_prefix: true`). The pin must therefore name the carve basis
  (`superblock.bytes_used` at offset 40..48) and the carrier sha; a reader that expects
  `carrier.sha == member.sha` would call a genuine carrier tampered. The prefix length varies per
  image (5,442,392 here), so it must be computed, never hardcoded.
- The round-39 writer is deterministic (`gen-squashfs.py:27,28,185`); lane-built carriers are
  reproducible and can therefore repeat a pinned sha — see §2.1.
- Round 40 will add ~27–42 MB of binary to a 143 MB `.git` with no `.gitattributes` and no LFS
  (§1.6). If the lane wants LFS it must be decided before the freeze commit, not after.

## 5. Limits

- I did not download or open the V1 image; its size is a live `HEAD` `Content-Length` and its sha is
  the seat's pin, not my measurement.
- I did not run REA or unblob on V1/V2/L1/L2, and built no C2 held-out carrier. My REA runs are on an
  unmodified copy of the round-39 K5 carrier (a development input), in `S`, `cd "$S"` first,
  `REA_UNBLOB_COMMAND` absolute, two runs, exit 0 each, 34324 B of JSON each.
- The V2 size range is the scout's `candidates.tsv`; I did not fetch those images.
- `[INFERENCE]` marks: GitHub platform size limits (§1.6), writer byte-reproducibility from the source
  lines (§2.1), and the claim that the byte-identity check is non-vacuous for a reused tree.
- I did not touch `.ufo/state/`, `.scratch/`, frozen carrier paths, or any path outside my report and
  artifacts.
