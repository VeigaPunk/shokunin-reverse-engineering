## R39C2LabDeterminism — verdict: H1 CONFIRMED · H2 CONFIRMED (restated: ids are run-nondeterministic, outdir is not the driver) · H3 CONFIRMED · DEFECTS FOUND (draft C1 symlink rule; id-based freshness)

Seat: R39C2LabDeterminism (leaf, wave 1 = pre-freeze). Lane root
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, base/HEAD `a2f64e1da78afcf8cc39287106604dbcc270844c`
(`git rev-parse HEAD` = that commit; lane not moved during this seat). Nothing frozen, nothing committed,
nothing written outside `.ufo/waves/round-39/w1/` (report) and `.ufo/waves/round-39/w1/artifacts/R39C2LabDeterminism/`
(evidence + one instrument). No VCS mutation. No package installs or upgrades were needed
(tool record: none). Held-out discipline observed: no REA run on K5/K6 (they do not exist), no REA run on
K1–K4 (development carriers only, built in scratch from my own trees).

Scratch: `S=/fast/scratch/hyaku/kaidoku-r39/R39C2LabDeterminism`, `export TMPDIR=$S`; removed at the end of
this seat (`rm -rf -- "$S"`, verified). Everything cited below was copied out of scratch into the artifacts dir
before removal; scratch paths appear in quotes only as historical receipt content.

---

## 1. H1 — `gen-squashfs.py` byte determinism → CONFIRMED (and stronger than claimed)

Command shape (all runs identical to):

```
python3 /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-37/gen-squashfs.py TREE OUT.sqsh --endian le|be|avm --comp gzip|xz
```

Tree `t1`: `etc/a.conf`, `bin/tool`, `usr/share/blob` (9000 B), `bin/link1 -> ../etc/a.conf`,
`bin/escape -> /etc/passwd`, `bin/dangling -> missing`. Two builds per (endian, comp) pair, exit 0 each:

| endian/comp | build 1 sha256 | build 2 |
|---|---|---|
| le/gzip | `c78feec747c26e2b3d472f75d0c125a88de5193560841bda8f8e4e8a8cb77042` | identical |
| be/gzip | `7ea6c6781015b635d23b6fa11375c459a6d4909bc2e87b38b231b0cfd1ffcd39` | identical |
| avm/gzip | `83cb641da99282c7c386734f19b3673d45be522e46dd0831ba07b03fbc45f672` | identical |
| le/xz | `368ac2b5b546916d183b63941d4c52aadb1e29a7ed5e16fc0056f12a09fb7188` | identical |
| be/xz | `66c5e8064e597a081321ac057d531551acbcf756ed937ce6a1c19b53575dcfb3` | identical |
| avm/xz | `bbb6202456c6356e7f73b232c6d7178650e6b92167459fdb24b1aa18fceadcbd` | identical |

Insensitivity axes exercised (same content, names; deliberately *different* everything else), all
`be/gzip` = `7ea6c67…cd39`:

- tree copied to `deep/t2` (different parent path), every mtime forced to `2001-02-03 04:05:06`,
  symlinks unlinked and recreated in reverse order → `o2_be_gzip.sqsh` identical.
- tree re-created from scratch in reverse alphabetical order with modes changed (`755`/`600`/`700`,
  dir `700`) → `o3_be_gzip.sqsh` identical. So modes are **not** encoded at all (writer hardcodes
  `0o100644` files / `0o40755` dirs / `0o120777` links); "same modes" is not even required.
- 400-file tree spanning multiple 8 KiB metadata blocks (image 26 138 B), built twice plus once in
  reverse creation order with mtimes `1999-12-31 23:59:59`:
  `le` all three = `d7dd6354e131bae622ea9ed3effd345d6668f518676f2190330ee86bf900cd54`,
  `be` all three = `fa400d0d8d9278c7c9d895953993f13b8cd7769d9dcb02a45b9f97d0ea80c3e1`.

Why (source, `tools/round-37/gen-squashfs.py`): `MKFS_TIME = 1700000000` and `UID = 1000` are constants,
`os.walk` results are sorted (`dnames.sort(); fnames.sort()`), inode numbers come from
`sorted(dirs, key=(depth, path))` / `sorted(files)` / `sorted(links)`, metadata blocks are stored
**uncompressed** (`UNCOMPRESSED | size` meta headers), and only `os.path.relpath` of each entry is written —
no absolute path, no mtime, no mode, no uid/gid from the host. `zlib.compressobj(9)` and the raw LZMA2
preset-6 filter are deterministic for a given zlib/lib lzma build. [INFERENCE] The only residual
cross-machine risk is a libz/lib lzma version producing different compressed bytes for the same input;
same-host rebuilds are bit-identical, which is all the C2 "regenerates byte-identically from the seed"
clause needs if the generator runs on the same host/toolchain as the freeze.

Side fact that matters for C2 recon: `--endian avm` differs from `--endian be` in **exactly 4 bytes**,
offset 8–11, the `mkfs_time` field (`be` 1700000000 vs `avm` = 763 = `bytes_used`); magic is `sqsh` in
both, nothing else changes (`evidence/avm-vs-be-byte-delta.txt`). The "AVM marker" is therefore a
structural predicate (`mkfs_time == bytes_used` / a small mkfs_time), not a magic-byte class.

Verbatim evidence: `evidence/h1-generator-hashes.txt`, `evidence/avm-vs-be-byte-delta.txt`.

## 2. H2 — evidence_id vs output directory → CONFIRMED by isolated experiment, but the real finding is larger

The 6.5.0 id rule digests the whole `semanticProjection`, which includes `parameters` verbatim:
`node_modules/rea-agents/dist/domain/evidence.js:156` (`const semanticProjection = …`),
`:168` (`parameters: evidence.parameters,`), `:182` (`computeEvidenceId = ev_${digestCanonicalValue(…)}`).
`subject` contributes only `{digest, format, architecture}` — the subject's path is *not* digested;
`parameters.path` (the carrier's invocation path) and `parameters.output_directory` are.

Isolated test with the instrument `mint-id.mjs` (evaluates the pin's own projection + `digestCanonicalValue`,
validated first by reproducing a stored id exactly):

| record | change | stored | recomputed |
|---|---|---|---|
| `evidence/E.json` (run E) | none | `ev_0dc65a4e…26ea3` | `ev_0dc65a4e…26ea3` (instrument validated) |
| `evidence/E_noop.json` | byte-identical rewrite | `ev_0dc65a4e…` | `ev_0dc65a4e…` (control) |
| `evidence/E_outdironly.json` | **only** `parameters.output_directory` | `ev_0dc65a4e…` | `ev_5abdc10c6331a58397250d25fd50e047f94381aa492fcbda2abb91c9c315b03f` → id moves |
| `evidence/K2_subjectpath.json` | **only** `subject.local_path` (round-38 K2 receipt) | `ev_e93867…028914` | `ev_e93867…028914` → id unmoved |
| `evidence/K2_paramspath.json` | **only** `parameters.path` | `ev_e93867…` | `ev_9220c272533dae4b35896d0aea0d736714bb0a778d3c723302b3bfc930d54717` → id moves |

Empirical, end-to-end: five REA 6.5.0 runs on one development carrier
(`$S/h2/carrier.sqsh`, sha256 `7ea6c678…cd39`, built in scratch), all exit 0:

| run | carrier path | output_directory | evidence_id |
|---|---|---|---|
| A | `…/h2/carrier.sqsh` | `…/h2/A_out` | `ev_824714f9…69d51` |
| B | same | `…/h2/B_out` | `ev_7870f546…6bbf4` |
| C | same | `…/h3/rootA/out` | `ev_89787b06…489d0` |
| D | same | `…/h3/rootB/out` | `ev_505b0782…63bc4b` |
| E | same | `…/h3/rootA/out` (**same string as C**, `out` removed first) | `ev_0dc65a4e…26ea3` |
| G | `…/h5/payload.bin` (byte-identical copy, relative arg `payload.bin`) | `…/h5/out` | `ev_eebc213e…4fd326` |

So the hypothesis as written is confirmed — a different output directory alone moves the id — **but the
stronger, true statement is that the id is not reproducible at all**: C and E have *identical `parameters`
and identical subject* and still differ, because

- `raw_result.execution.args[…11,12,7,9]` embeds REA's random staging dir `rea-firmware-<6 alnum>`
  (`rea-firmware-7rvxKv` vs `rea-firmware-EMHM7S`), which sits under `TMPDIR` and is fresh per run;
- `normalized_result.chunks[].provider_id` / `derivations[].provider_blob_id` (and `raw_result`'s
  `task.blob_id`) are unblob blob ids = `f"{os.getpid()}:{counter}"`
  (`unblob/identifiers.py:8-17`, `new_id()`), i.e. the *process id*, fresh per run
  (`3514819:1` vs `3928488:1` in C vs E).

Field families that differ between two runs with identical parameters
(`evidence/h2-C-vs-E-nondeterministic-fields.txt`):
`/evidence_id`, `/normalized_result/chunks[].provider_id`, `/normalized_result/derivations[].provider_blob_id`,
`/raw_result/execution/args`, `/raw_result/report[].{task,reports,subtasks}.{path,blob_id,id}`.
Nothing semantic differs: same handler set, same `files[].relative_path` + `sha256`, same gap set, same
diagnostics, same `subject.digest`.

Also measured: `parameters.path` is **absolutised** (run G passed `payload.bin` from its cwd and the receipt
records the absolute path), and `normalized_result.files[].path` / `normalized_result.output_directory` are
absolute and outdir-derived. Only `relative_path` is location-independent. `environment` is `null`
(`provider` is recorded, PATH is not — see §5).

Consequences for the C1 claim (as drafted, "recomputes to its stored evidence id under the rea-agents 6.5.0 rule"):
the binding is a *self-consistency* check on the committed bytes. It cannot be satisfied by re-running, and a
receipt can never be "reproduced"; it also cannot be used to compare two receipts of the same carrier.

## 3. H3 — same outdir *name* in different scratch roots → CONFIRMED

Runs C (`…/rootA/out`) and D (`…/rootB/out`) — same carrier path, same relative outdir name `out`, different
root — and additionally A/B/E/G, all yield the identical published set
(`relative_path`, `sha256`), same handler `squashfs_v4_be`, same gap set:

```
firmware.bin_extract/bin/tool        f4870b140ffecf6bb423dc6fbc7b4f176e0b3ba0823419cc08036fe506483b81
firmware.bin_extract/etc/a.conf      5891b5b522d5df086d0ff0b110fbd9d21bb4fc7163af34d08286a2e846f6be03
firmware.bin_extract/usr/share/blob  e797e2af6f05c24cdd064793ce60a9d01302d9a3b0e5dff5bb0c046b87f2f668
```

`evidence/h3-relfile-sets.txt` shows `relfiles(A)==relfiles(X): True` for X ∈ {A,B,C,D,E,G}; the extraction
root prefix is always `firmware.bin_extract/…` regardless of the input file name (`carrier.sqsh` in A–E,
`payload.bin` in G) because REA stages the input as `firmware.bin`.

So: `normalized_result.files` (`relative_path`, `sha256`) is root-invariant; the evidence id is not.
A suffix match against an oracle is therefore stable; anything keyed on `path`, `output_directory`,
`provider_id`, `blob_id`, diagnostic `link`/`target`, or the id is not.

## 4. The decision question: can a receipt-only counter tell a copied receipt from a fresh run?

**No — not with the bindings drafted for either C1 or C2.** Evidence, all from the 6.5.0/xpin rule
(`evidence/h2-mint-and-xpin.txt`, instrument `mint-id.mjs`):

| experiment on committed round-38 K2 receipt | stored | xpin verdict |
|---|---|---|
| unmodified | `ev_e93867…028914` | `both` (= self-consistent under 6.5.0; all four K1–K4 receipts are) |
| a published `sha256` mutated, id left alone | `ev_e93867…` | `none` → tampering *is* caught |
| same mutation, id recomputed ("minted") | `ev_55f07a7a…697dd` | `both` → a fabricated receipt passes |
| rehomed into a round-39-shaped outdir (`parameters.output_directory`, `normalized_result.output_directory` and every `files[].path` rewritten), id minted | `ev_b27d559a…dae20` | `both`; oracle hits 3/3, `unpublished-entry` gap and `squashfs_v4_be` handler preserved |

Because `id = ev_ + digest(projection(record))` and the projection is the record itself, *any* content is
mintable into a self-consistent receipt; the id only proves the record was not edited after minting. A
copied round-38 receipt keeps its valid id, and a copied-and-rehomed receipt is mintable back to validity.

What *does* work, and is cheap:

1. **Freshness by id-absence at the freeze.** A genuine fresh run always produces an id that cannot exist
   in the freeze tree (random staging dir + pid). Verified feasible: all four round-38 after-receipt ids
   occur exactly once in the base tree (`git grep -l <id> a2f64e1 -- corpus` → 1 file each), and no
   round-39 evidence path exists at base (`git ls-tree -r a2f64e1 -- corpus/evidence/round-39
   .ufo/waves/round-39` → 0 entries). `evidence/id-at-base-scan.txt`. A counter rule "no after-receipt
   `evidence_id` may occur anywhere in the freeze tree" kills the drafted "round-38 receipts copied into
   round-39 paths" control *at the receipt level*, for K1–K4 as well as K5/K6 — this matters because the
   current kill control only fails that cheat via "K5/K6 absent", i.e. it would stop passing if someone
   also minted K5/K6 receipts from K1/K4 bodies.
2. **Git provenance for the receipt path** (`first added in a commit descending from the freeze`) is a
   history check, not a receipt check — it does not by itself catch a copy into a *new* round-39 path,
   because that path's first add also descends from the freeze. Pair it with (1).
3. **Never require reproduction.** Any counter clause of the form "re-running must yield this id" or
   "ids must match across carriers/runs" is unsatisfiable — C vs E prove it with identical parameters.
4. For C2: the triage interpreter must key only on stable envelope fields — `chunks[].handler`,
   `normalized_result.files` (`relative_path`, `sha256`), `extraction_gaps[].kind` +
   `relative_path`, `diagnostics[].report.__typename__`, `subject.digest`. Not `chunks[].status` (it is
   `null` in every observed class, including failures), not `chunks[].provider_id` (pid), not diagnostic
   `link`/`target` (they contain `rea-firmware-XXXXXX` staging paths — see §5), not absolute paths.

## 5. Defects found in the draft (must be fixed before the freeze, not after)

### D1 — the C1 symlink rule is wrong for absolute-target symlinks (blocking if K5/K6 use one)

Draft rule: "a symlink whose target resolves inside the extraction root is kept as metadata and recorded as
one `unpublished-entry` gap; a symlink that escapes is removed by unblob (`MaliciousSymlinkRemoved`) and
recorded as no gap", with `escaping` decided by POSIX resolution against the link's own directory (so an
absolute target always escapes).

Measured (development carrier `syms_be.sqsh`, standard BE v4, gzip, built with the round-37 generator;
REA 6.5.0 + unblob 26.6.4 + `sasquatch-v4be`, exit 0; `evidence/symlink-classes-t4.txt`, envelope
`evidence/rea-symlink-classes-H.json`, image `evidence/syms_be.sqsh`):

| link in image | target kind | published? | gap | diagnostic |
|---|---|---|---|---|
| `bin/intree -> ../etc/a.conf` | relative, resolves inside | no | `unpublished-entry` `…/bin/intree` | — |
| `bin/rel-escape -> ../../../../hello.txt` | relative, resolves outside | no | **none** | `MaliciousSymlinkRemoved` |
| `bin/abs-escape -> /etc/passwd` | absolute | no | **`unpublished-entry`** `…/bin/abs-escape` | **none** |
| `bin/dangling -> missing` | relative, nonexistent inside | no | `unpublished-entry` `…/bin/dangling` | — |

Root cause (unblob `extractor.py:50-92`): `fix_symlink` only removes a link when
`is_safe_path(outdir, target)` fails; for absolute targets it does
`target = Path(raw_target.as_posix().lstrip("/"))` (line 74-75) and joins it under `outdir`, so an absolute
target is *always* "safe", rewritten to a relative link and kept — and then never published as a regular
file, hence an `unpublished-entry` gap. Only relative targets that resolve outside are removed
(`MaliciousSymlinkRemoved`, e.g. K1's `src/link-to-hello -> ../hello.txt`, which is exactly the round-38
K1 receipt's `[… ] diag ['MaliciousSymlinkRemoved'], gaps []`). The frozen K1–K4 do not exercise the
absolute case (`K1/src` has only `link-to-hello -> ../hello.txt`; `K2/src` only
`var/lib/run-link -> ../../a/run.sh`), so K5/K6 are the risk.

Recommendation for the freeze text (pick one, state before data):
(a) define `escaping` as *relative-target resolution only*, and state explicitly that an absolute-target
link is rewritten by unblob and recorded as one `unpublished-entry` gap (measured behaviour), or
(b) forbid absolute-target symlinks in K5/K6 and in the held-out C2 generators. Either way the
`symlinks.tsv` third column needs the three-way outcome (`in-tree-gap` / `escaping-removed` /
`absolute-kept-gap`) or a fourth `kind` column, otherwise the C1 predicate
"gaps exactly on the in-tree symlinks and no other gap" is unsatisfiable for a correct run on such a carrier.

### D2 — the C2 class set needs the gap-kind discriminator, and one class carries no path

Measured class signatures on development carriers (all stable, none pid/path-derived), for the triage table:

| class | handler | files | `extraction_gaps[].kind` | `diagnostics[].report.__typename__` | source |
|---|---|---|---|---|---|
| clean | `squashfs_v4_be` | all oracle files | — | — | K3/K4 receipts; dev runs A–E |
| in-tree-symlink-metadata | `squashfs_v4_be` | oracle files | `unpublished-entry` (per link, `relative_path` set) | — | K2 receipt; `symlink-classes-t4.txt` |
| escaping-symlink-removed (relative target) | `squashfs_v4_be` | oracle files | — | `MaliciousSymlinkRemoved` | K1 receipt; t4 |
| dep-missing-be (`sasquatch`/`sasquatch-v4be` off the child PATH) | `squashfs_v4_be` | 0 | **`missing-extractor-dependency`** (no `relative_path`) | `ExtractorDependencyNotFoundReport` | run F, `evidence/rea-env-F-no-sasquatch.json` |
| avm-marker-be-dropped | `squashfs_v4_be` | 0 | **`extractor-failure`** (no `relative_path`) | `ExtractCommandFailedReport` | round-38 probe `rea-k1-avm.json` |
| absolute-target-symlink (new, see D1) | `squashfs_v4_be` | oracle files | `unpublished-entry` | — | t4 |

Two consequences: the handler name alone separates nothing (`squashfs_v4_be` appears in the clean, dep-missing
and AVM-dropped classes, and `chunks[].status` is `null` in all of them); and gap `relative_path` is `null`
for the two extraction-failure kinds, so a table keyed on gap path cannot express them. `dep-missing-le` and
`body-extractor-failure` were not probed by this seat (out of scope here; LE dependency is
`unsquashfs`, not sasquatch, and would need a PATH without squashfs-tools).

### D3 — `environment` is null, so a receipt does not record what decided the outcome

Same carrier, same parameters except the child PATH (sasquatch reachable vs stripped, `REA_UNBLOB_COMMAND`
absolute in both): published files 3 → 0, gaps `[]`+no diagnostic → `missing-extractor-dependency` +
`ExtractorDependencyNotFoundReport`, `environment` field `null` in both
(`evidence/env-sensitivity-and-round38-corpus.txt`). Two receipts of the same carrier can therefore disagree
while claiming identical parameters and identical environment. The C1 predicate's
"sasquatch-v4be 4.5.1 reachable on the child PATH" clause is only recoverable from the *result* (files
published), never from the receipt's environment — worth saying so rather than implying the receipt records it.

### D4 — note for the round-39 counter when it is forked from round-38

`tools/round-38/c1-counter.py:181` binds `after_gaps_empty`, which the round-39 predicate replaces with the
gap-shape rule; a straight port would fail K2 (`unpublished-entry` on `var/lib/run-link`) and D1's absolute
case. Round-38 K1–K4 receipts at base: K1 gaps `[]` + `MaliciousSymlinkRemoved`, K2 gaps
`['unpublished-entry']`, K3/K4 clean (`evidence/env-sensitivity-and-round38-corpus.txt`).

## 6. Freeze-time recommendations (concrete, ordered)

1. Freeze `symlinks.tsv` with a three-way outcome (D1) or restrict K5/K6 to relative targets; state the
   absolute-target behaviour in the same paragraph as the rule, before data.
2. Add the receipt-level freshness rule from §4.1 ("no after-receipt `evidence_id` occurs in the freeze
   tree") next to the copy-control; keep the git-provenance clause but do not rely on it alone.
3. In both counters, drop any expectation that ids reproduce; treat `evidence_id` purely as a tamper seal
   on the committed bytes.
4. In `sqfs-triage.py`, forbid unstable keys (`path`, `output_directory`, `provider_id`, `blob_id`,
   `diagnostic.link`/`target`, `chunks[].status`); require `relative_path` for file and gap matching and
   `__typename__` + gap `kind` for class separation (D2).
5. If C2's held-out generator reuses `gen-squashfs.py`, ship the generator's sha256 with the manifest: same
   tree ⇒ same bytes on this host for le/be/avm × gzip/xz (§1), but the compressed payload depends on the
   linked zlib/liblzma build, so "regenerates byte-identically from the seed" should be pinned to the
   recorded toolchain, not just the seed.

## 7. Limits and inferences

- Measured only: standard BE v4 gzip carriers (plus one byte-identical copy under a different name), one
  xz/LE structure check at generator level only (no REA run on xz or LE images by this seat).
- No REA run on K1–K4 (item says development trees only) and none on K5/K6 (they do not exist); I did not
  and cannot test the frozen carriers' receipts beyond their committed bytes.
- No AVM image was run through REA by this seat; the AVM row in D2 comes from the round-38 probe's committed
  envelopes (`R38W2AvmProbe/rea-k1-avm.json`), read only.
- `[INFERENCE]` items: cross-host compression-bit stability (§1); the claim that D1 would fail the drafted
  C1 gap rule for a correct run, which follows from the measured gap set plus the draft's `escaping`
  definition — if the freeze instead defines an absolute target as `in-tree`, D1 becomes a wording issue
  only, but the `symlinks.tsv` definition quoted in the draft resolves absolute targets outside the root.
- ~3.0–3.7 s wall per REA run on ~800 B carriers (single worker, includes `npx` startup); REA refuses a
  pre-existing outdir (`ok:false`, `execution_failure`, exit 1 —
  `evidence/rea-refuses-existing-outdir.json`), so every run needs a fresh path.

## 8. Artifacts

`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-39/w1/artifacts/R39C2LabDeterminism/`

- `mint-id.mjs` — instrument: evaluates the pin's own `semanticProjection` + `digestCanonicalValue`
  (`--pkg <rea-agents root> [--write] ENVELOPE…`); reproduces stored ids exactly.
- `evidence/h1-generator-hashes.txt` — all generator hashes above.
- `evidence/avm-vs-be-byte-delta.txt` — 4-byte `mkfs_time` delta.
- `evidence/rea-h2-A.json`, `rea-h2-B.json`, `rea-h3-C-rootA.json`, `rea-h3-D-rootB.json`,
  `rea-h3-E-rootA-repeat.json`, `rea-h5-G-relative-input.json` — full CLI envelopes (`{ok,data,meta}`)
  for the five dev runs.
- `evidence/h3-relfile-sets.txt` — id/outdir/inpath per run, cross-run published-set equality, handler/gap/
  diagnostic sets.
- `evidence/h2-C-vs-E-nondeterministic-fields.txt` — field-level diff of two identical-parameter runs.
- `evidence/h2-mint-and-xpin.txt` — mint validations, isolated deltas, xpin verdicts for tampered,
  minted, rehomed, subject-path and params-path variants.
- `evidence/E.json`, `E_noop.json`, `E_outdironly.json`, `K2_subjectpath.json`, `K2_paramspath.json`,
  `K2_tampered_raw.json`, `K2_tampered_minted.json`, `K2_rehomed.json` — the experiment records.
- `evidence/rea-env-F-no-sasquatch.json`, `evidence/env-sensitivity-and-round38-corpus.txt` — PATH
  sensitivity and the committed round-38 class signatures.
- `evidence/rea-symlink-classes-H.json`, `evidence/symlink-classes-t4.txt`, `evidence/syms_be.sqsh` —
  D1 carrier and result.
- `evidence/id-at-base-scan.txt` — receipt ids present exactly once at `a2f64e1`; zero round-39 evidence
  paths at base.
- `evidence/rea-refuses-existing-outdir.json` — pre-existing-outdir refusal.

Report path: `.ufo/waves/round-39/w1/R39C2LabDeterminism.md` (this file).
