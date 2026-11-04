# ReviewerC3 — adversarial review of R84-C3 (nested container chain)

Seat `ReviewerC3` (reviewer, round-84 wave `r84-w1`) · lane `kaidoku-shokunin` · L1 `KaidokuR84`
Base `043b89a25241710a68b45526c3287fb3c8d907c3` · declaration `e0de2088a7bddc16305357f90ac7e889fa0a0d11` · first container `a5663ddedd157bb9113928f5fe80509d6f3fc7a1` · HEAD at review `fa92d34aec31ae59cb19a8a6ea9e6c0ac7a2392f`
Claim: **R84-C3** (coverage — nested sub-images below depth 1) · freeze `.ufo/waves/round-84/pre/c3-pilot.json`.

**Bottom line.** The receipt reproduces. I rebuilt the fixture chain from the recipe (frozen pins
matched; a different invocation also stayed byte-identical), extracted each level with
`unsquashfs 4.7.5`, ran `rea-agents@6.5.0 extract-firmware` at `--max-depth 3` and `4` into
verified-absent directories, hashed the published trees and re-scored the raw envelopes with the
frozen scorer. A1–A9 and the control all hold; the frozen counter run end-to-end produced a
receipt **byte-identical to the pilot** (`sha256 f45f018cdee6ce47daca6acbfb96674a9c0150fff834cc631fe6b25f5fb9cffa`,
zero divergence in any arm/observed field). The findings below are provenance and
counter-strength issues for L1, not failures of this run — with one live exception: during this
review the lane working tree's copy of the frozen counter was edited by another actor (F0). Every
arm, receipt and fixture number in this report was produced from the pinned blob `08353f36…`
before that edit; the only post-edit numbers are the drift observations in F0 and
`lane-state.json`.

## 1. Method and exact commands

All work under `/fast/scratch/hyaku/kaidoku-r84/ReviewerC3/` (removed before yield); receipts
copied to `w1/ReviewerC3/` (`verify.json`, `raw3.json`, `raw4.json`, `toolrepro.json`,
`oracle.sha256`, `variant.sha256`, `lane-state.json`).

```sh
S=/fast/scratch/hyaku/kaidoku-r84/ReviewerC3
# 1. rebuild with the receipt recipe (same content, same order)
mkdir -p $S/build/{leaf,mid,outer}
printf 'leaf-alpha\n' > $S/build/leaf/alpha.txt
printf 'leaf-beta\n'  > $S/build/leaf/beta.txt
python3 -c "open('$S/build/leaf/gamma.bin','w').write(''.join(f'row-{n:03d}\n' for n in range(200)))"
mksquashfs $S/build/leaf $S/build/c.sqfs -noappend -comp gzip -b 4096 -quiet -repro-time 1760000000
cp $S/build/c.sqfs $S/build/mid/inner-c.sqfs
printf 'mid-one\n' > $S/build/mid/one.txt; printf 'mid-two\n' > $S/build/mid/two.txt
mksquashfs $S/build/mid $S/build/b.sqfs -noappend -comp gzip -b 4096 -quiet -repro-time 1760000000
cp $S/build/b.sqfs $S/build/outer/inner-b.sqfs
printf 'outer-x\n' > $S/build/outer/x.txt
mksquashfs $S/build/outer $S/build/a.sqfs -noappend -comp gzip -b 4096 -quiet -repro-time 1760000000

# 2. independent oracle (three separate extractions, recursive sha256)
unsquashfs -d $S/oracle/a $S/build/a.sqfs
unsquashfs -d $S/oracle/b $S/build/b.sqfs
unsquashfs -d $S/oracle/c $S/build/c.sqfs

# 3. REA into absent dirs (verified absent first; separate TMPDIRs; parallel)
test ! -e $S/out3 && TMPDIR=$S/tmp3 PYTHONDONTWRITEBYTECODE=1 \
  npx -y rea-agents@6.5.0 extract-firmware $S/build/a.sqfs $S/out3 --max-depth 3 --format json >$S/raw/raw3.json 2>$S/raw/raw3.err
test ! -e $S/out4 && TMPDIR=$S/tmp4 PYTHONDONTWRITEBYTECODE=1 \
  npx -y rea-agents@6.5.0 extract-firmware $S/build/a.sqfs $S/out4 --max-depth 4 --format json >$S/raw/raw4.json 2>$S/raw/raw4.err

# 4. different invocation (all three levels): -processors 1 and no -quiet
#    rebuilt leaf/mid/outer with "-noappend -comp gzip -b 4096 -repro-time 1760000000 -processors 1"

# 5. frozen counter end-to-end (same rev value as the pilot)
python3 -I -B tools/round-84/nested-sqfs.py --rev 043b89a25241710a68b45526c3287fb3c8d907c3 \
  --work $S/toolrun --json-out $S/toolrepro.json
```

Results: both REA runs exit 0 with empty stderr; both output directories were absent before the
run; `raw3.json`/`raw4.json` retained. The frozen-counter run exits 0; its full receipt and the
pilot are identical after JSON normalization (both sha256 `f45f018c…`), including fixture pins,
`expected`, all sub-arms, `observed`, `runs`, `toolchain` and `control`.

**Timing.** The frozen-counter run above finished before the worktree drift recorded in F0; the
receipt it produced carries `instrument.sha256 08353f36…`. The later worktree bytes
(`938801ba…`) were not used for any number in this report.

**Why the recipe is trusted:** a second build with a different invocation (`-processors 1`, no
`-quiet`) produced the same all-three pins
`a e82c5995…`, `b 7d2dd0e7…`, `c f68b42fa…`. I did not change compressor or block size: that would
change the fixture class rather than test reproducibility.

## 2. What verified (independent of the counter)

| check | result |
|---|---|
| oracle counts by level | outer 2, mid 3, leaf 3 (8 members) |
| nested carrier identity | `inner-b.sqfs` in oracle-a == pin b; `inner-c.sqfs` in oracle-b == pin c |
| path set, depth 3 and 4 | exactly 8/8 oracle paths after stripping the shared `firmware.bin_extract/` root |
| byte identity | envelope `sha256` == on-disk sha256 == oracle sha256 for all 8 at both depths; on-disk sum 9837 both |
| `coverage` | `partial` at depth 3, `complete` at depth 4 |
| `depth_limited_paths` | exactly one at depth 3: `$output/firmware.bin_extract/inner-b.sqfs_extract/inner-c.sqfs_extract`; none at depth 4 |
| `extraction_gaps` | exactly one at depth 3, `kind: depth-limited`, same `input_path`, `continuation_id 3b54e297…b442ab`; none at depth 4 |
| `analysis_depth` per file | d3: `x.txt`/`inner-b.sqfs` = 1, mid files/`inner-c.sqfs` = 2, the three level-3 files = **null**; d4: same except the three level-3 files = **3** |
| engine block | identical both runs: unblob 26.6.4, `executable_sha256 0ce7b624…1d09` |
| unpublished entries / diagnostics | `[]` / `[]` both runs |
| exit / stderr | 0 / empty both runs |
| frozen-counter receipt | exit 0, `met true`, control fires, 9/9 arms; exact pilot match |

The three `analysis_depth null` files are exactly the files with `reported_sha256: null` and
`mime_type: null` at depth 3; at depth 4 the same three carry provider-reported sha256/mime and
`analysis_depth 3`. unblob's own summary counts 6 extracted files at depth 3 and 9 at depth 4
while REA publishes 8 at both depths — an independent corroboration that the level-3 bytes are
written out without being analyzed at depth 3.

## 3. The boundary questions

**Is "8/8 at depth 3" compatible with `coverage: partial`?** Yes, and the mechanism is explicit.
REA computes firmware `coverage` in `dist/firmware/FirmwareReports.js:419-423` as
`partial` iff depth-limited paths, diagnostics, or null/encrypted chunks exist — not from the
published file count. The depth-3 extractor wrote the level-3 files but did not report/analyze
them; publication and analysis are different sets. The receipt's `coverage` and
`depth_limited_paths` are the completeness signal; the file list is not.

**Does the receipt's control actually fire?** Yes. On the raw depth-3 envelope `files == 8` and
`coverage == "partial"`, so the cheap rule "published count equals oracle count, therefore
complete" is falsified by the provider's own coverage field. It is a data-derived statement, not
a second execution; it also does not fire when I synthesize `coverage: complete` (so it is not
tautological), and it still fires on an 8-file partial envelope whose paths are all wrong — by
design of a count-only rule. It demonstrates the failure mode of the cheap rule, not extraction
correctness.

**Is `analysis_depth: null` a real field or a parsed artifact?** Real, for this receipt. The
schema declares `analysis_depth: bytes.nullable()` (`dist/domain/firmware/firmwareAnalysis.js:133`);
publication sets `analysis_depth: reported?.depth ?? null` (`dist/firmware/FirmwarePublication.js:96`).
All 8 file objects in both raw envelopes carry the key; the three level-3 files carry explicit
`null` at depth 3 and `3` at depth 4. The counter, however, reads it with `.get()` — see F3.

**Is the fixture class overstated?** Not in the claim or predicate: both say lane-built,
three-level, standard little-endian SquashFS v4, gzip, mksquashfs 4.7.5, REA 6.5.0/unblob 26.6.4.
The PROVINCE/knowledge notes also exclude vendor/external images, other compressors, other block
sizes, AVM/BE layouts, several containers per level, other providers, and provider budget limits.
A vendor image would change: compressor (xz/lzo/zstd), block size (typically 128 KiB), endianness
and vendor magic (AVM `hsqs`, Broadcom), entry classes (symlinks, device nodes, hardlinks, xattrs),
fragments/sparse/duplicate extents, member counts and byte budgets, nesting depth/containers per
level, and offsets/appended data. The measured fixture has none of those: it is 4 KiB per image
with only regular small files. The class is narrow and the text is mostly honest about it; the one
wording defect is F4.

## 4. Findings

**F0 — High — the frozen C3 counter was edited in the lane working tree during the wave; the
current bytes are not the pinned predicate.**
At 16:51:44 (after this review's `verify.json` was written at 16:50:44),
`tools/round-84/nested-sqfs.py` in the lane worktree became 19,955 B /
`938801ba9cb2760105fa0b3518e340a93eed30d6ee28dd085ca9e7776d608b96`. The committed blob at HEAD
(and the digest pinned in `claims.json`) is 19,320 B /
`08353f361ebc687abfde7609a310184cdbcf8c69da3767886f15580ea3b5d4b0`. The diff is not cosmetic: it
removes the unused `import tempfile`, changes A4's `deepest-unanalyzed` predicate to require
`"analysis_depth" in by_path[p]` (a present key with `null`, instead of `.get() is None`), and adds
a `dropped-analysis-depth-fails` selftest; its comment cites "round-84 ReviewerC3 probe
d3_level3_key_drop". This is a semantic counter/predicate change, which the wave rules forbid
("never change a predicate, counter") and C3's kill rule names ("a changing predicate"). The
claims container still pins `08353f36…`, so the worktree no longer matches the freeze. SentinelScope
recorded an earlier, cosmetic drift at 16:48:09 (`e0364dde…`, import removal only) and its report
documents that state; this second, semantic drift post-dates the report and no wave-dir candidate
copy accounts for it. My review modified nothing: the frozen-counter run (Section 1) used the pinned
blob and its receipt carries `instrument.sha256 08353f36…`; the drifted version was not used for
any number here. L1 must either restore the path from the pinned blob or declare a supersession /
re-freeze (new digest in a new container, receipt regenerated, disclosed); a landing receipt
produced from the current worktree would measure a different predicate and must not be attributed
to R84-C3 as frozen.

**F1 — Medium — the pilot's `rev` is not the revision of the executed counter.**
`c3-pilot.json` records `rev: 043b89a2…`, but `git show 043b89a2:tools/round-84/nested-sqfs.py`
fails; the executed blob's digest `08353f36…` is present at `e0de2088`, `a5663dde` and HEAD, and
is the digest pinned in `claims.json`. The tool writes `--rev` verbatim and never checks or uses
it. The pilot is reproducible, but its `rev` field cannot authenticate the instrument. For L1:
the landing receipt should record `--rev` at a revision where the pinned digest is a blob
(`e0de2088` or later) or explicitly label the field as the round base; do not cite the pilot as an
"at BASE" artifact. The C1 binding itself is intact: the container pins `08353f36…`, and that
blob exists at `a5663dde`.

**F2 — Medium-Low — `met` does not enforce fixture identity.**
`fixture_pins` is recorded but never compared to any frozen value. Probe: replacing all three
pins in the `chain` object with zeros still yields `met true` and all arms true. The tool builds
one chain and reuses it for both depths, so the kill rule "fixture digests changing between the
two depth runs" is structurally unable to fire within a run; cross-run identity rests on the
reported pins matching the pilot (they do, and my rebuild matches) and on the rechecker comparing
them, not on `met`. The landing verifier should compare the three pins explicitly.

**F3 — Low — A4 accepts an absent `analysis_depth` key as if it were `null`.**
`deepest-unanalyzed` and the observed map use `.get()`; dropping the key from only the three
level-3 files (keeping levels 1–2 correct) still yields `met true`, `A4 true`. The current raw
envelopes carry explicit nulls (8/8 keys present in both runs), so the claim's wording is
satisfied by this receipt; but the receipt alone cannot prove field presence. The unpinned
worktree edit in F0 makes exactly this change and adds the selftest; the fix is real, but it is
not the frozen predicate and cannot serve as evidence for the frozen claim without a declared
re-freeze. Retain the raw envelopes with the landing receipt (as this review does), or adopt the
fix only through a new freeze.

**F4 — Low — the README's class bound still says "depth beyond four".**
`PROVINCE.md` and the knowledge entry were corrected at 16:51:58 to "chains of more than three
levels", which covers the four-level case; `corpus/README.md` line 360 still ends "Still frontier:
… depth beyond four …", so a four-level chain remains outside the Core statement and is not
literally "beyond four". Align the README line with the other two. The claim itself is not
overstated.

**F5 — Info — counter checks that are weaker than their prose.**
A3's gap/root checks are suffix-only (`endswith(DEEPEST_ROOT)`), so a path elsewhere ending in
that suffix would pass; the observed path is exact. A9 pins unblob's identity but not the
`sasquatch` child that actually decodes v4 (the host's `sasquatch` reports as `unsquashfs 4.5.1`);
both runs are same-host, so this is a cross-host reproducibility gap, not an intra-run one. The
oracle's independence is at binary/version level (`unsquashfs 4.7.5` vs unblob's `sasquatch`
4.5.1 lineage), not a different decoder lineage; it still validates REA's path/byte plumbing.

**F6 — Integration — the landing receipt is absent at review time.**
The knowledge entry cites `.ufo/waves/round-84/l1/scores/c3-at-landing.json`; it does not exist
yet (expected mid-wave). L1 must produce it before the entry's status line is verifiable, and it
should record a rev whose blob matches the frozen pin (see F1) plus the raw envelopes (see F3).

## 5. Residual risk and verification gaps

- One host, one toolchain pair (mksquashfs/unsquashfs 4.7.5, REA 6.5.0, unblob 26.6.4); no second
  host or second decoder lineage.
- No vendor/external image, no non-gzip compressor, no other block size, no AVM/BE layout, no
  four-level chain, no multiple containers per level, no symlink/device/hardlink/xattr/fragment
  fixtures.
- The landing receipt (`c3-at-landing.json`) was absent; this review verifies the pilot and the
  frozen counter, not L1's final landing artifact.
- The landing receipt must be produced from the pinned bytes (`instrument.sha256 == 08353f36…`),
  not the drifted worktree; otherwise the claim is measured by a different predicate (F0).
- Raw envelopes contain scratch-absolute paths (the receipt does not); they are retained for
  field-level evidence with the scratch directory removed.

## 6. Scope and tooling

- Writes confined to `.ufo/waves/round-84/w1/ReviewerC3/` and `.ufo/waves/round-84/w1/ReviewerC3.md`
  (plus scratch, removed). No production edits, no fleet/sibling-lane writes, no LOG/SCORECARD/
  MANIFEST writes, no PATH-directory writes, no git/jj mutations (read-only `show`/`cat-file`/
  `log` only), no commits/pushes, no `task` spawns, no `agent://all`.
- Nothing installed or upgraded. The npx invocation resolved `rea-agents@6.5.0` from the existing
  npx cache `ad9a3fdbcad992c6` (the cache's injected `.bin` path confirms it); the host's other
  caches/global install hold 6.7.0 and were not used.
- Frozen bytes read only: `tools/round-84/nested-sqfs.py`, `.ufo/waves/round-84/pre/c3-pilot.json`,
  `claims.json`, `plans/round-84-claims.md`; I modified no frozen file. The lane worktree's
  `tools/round-84/nested-sqfs.py` was modified by another actor at 16:51:44 (F0), after my
  evidence write; the other two frozen tools also show worktree drift (`freeze-precheck.py`
  16:46:03, `mutation-closure.py` 16:50:26), outside this claim's scope but noted for L1.

## 7. Receipts

`w1/ReviewerC3/`:

| file | sha256 |
|---|---|
| `verify.json` | `45b3e43a628da5ffcfbcc5f5f5c9d8f999b2bb4151c51f8b21c243c4b525d816` |
| `toolrepro.json` | `f45f018cdee6ce47daca6acbfb96674a9c0150fff834cc631fe6b25f5fb9cffa` (== pilot) |
| `raw3.json` | `77f55593ca4ef789d3184e8409268905122e0758be8c5626ed2a6004574e09fd` |
| `raw4.json` | `6d4d589da73758e21db6c4b2b026b9980714017c7040343f466801deb1f9b973` |
| `oracle.sha256` | `5bd15160ea36a02252210b455ecdea5f995389c2af97f2f7444a56e4b0c5c03c` |
| `variant.sha256` | `5c2a0d9e2c693c29ead86f7af48ffe496b3138566f629c737111229cafc26f7f` |
| `lane-state.json` | `05951432e59caaf87ae2cd77a440a00e6a5144fbaeca92e54237ce565c50fe53` |
