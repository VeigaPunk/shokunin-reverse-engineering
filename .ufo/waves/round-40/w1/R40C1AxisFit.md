# R40C1AxisFit — attack on the draft R40-C1 predicate (pre-freeze)

**Verdict: DEFECTS FOUND** — the draft R40-C1 cannot be frozen as written: one clause is
*unsatisfiable* (the rerun binding names REA's `semanticProjection`, which provably differs between
any two runs), one clause is *unsound* (the "first metadata block length decodes LE" test passes on
the claim's own marker-only kill control and on valid standard-BE images), and the target counts two
sourceless synthetic carriers toward a **coverage** move. Ten defects are itemized in §7 (D1-D3
are the three summarized here). The carrier class itself is sound and the rerun binding is the right fix for R39-CL5
once re-specified: every finding below has a measured counterexample and a smallest safe correction,
and the replacement predicate in §8 is fully enumerable.

Seat: critic (leaf). Wrote only this file and
`.ufo/waves/round-40/w1/artifacts/R40C1AxisFit/`. Scratch
`/fast/scratch/hyaku/kaidoku-r40/R40C1AxisFit` removed at exit. No tool installed or upgraded; no
pacman transaction; `sasquatch`, `sasquatch-v4be`, `unblob`, REA untouched. Read-only git only; no
VCS mutation; shokuknow read-only (the 4096 B round-11 image was read in place, never copied).
**Frozen-carrier discipline honoured:** no REA and no unblob run on V1's AVM-BE member, on any
second vendor member, or on any lane-built AVM carrier; REA/unblob ran only on round-39 K1/K5
copies and on synthetic trees I built in scratch. §6 discloses the *reads* I made of vendor bytes:
a superblock parse and a metadata-header walk of one candidate V2 member (no extraction).

## Axes named (Godspeed)

| axis | what this review moves |
|---|---|
| **coverage** | whether the claim's numeric target measures the surface it names (vendor AVM-BE) or a fixture the lane can already count |
| **depth** | the discriminator: first-header plausibility (unsound) → metadata-header chain + format invariants (decisive, measured) |
| **calibration** | whether "the receipt is real" is replaced by "the behaviour is real"; three clauses currently assert more than they can prove |

---

## 1. (a) Is genuine AVM-BE Frontier → Core a coverage move, or re-scoring held ground?

**Verdict: a coverage move — conditional on three fixes.**

Ground check (all read this session):

| surface | state at base `fa6a8a3f` |
|---|---|
| `PROVINCE.md:156-157` | the `- **sasquatch** — …` bullet: "big-endian/AVM stays here" |
| `PROVINCE.md:384` | "AVM-BE bodies and vendor-mangled images stay Frontier" |
| `corpus/README.md` `## Frontier` | "sasquatch-v4be — … round 39: … Still frontier: AVM-BE bodies, vendor-mangled images" |
| `corpus/knowledge/` | **no AVM entry**: `ls corpus/knowledge | grep -i avm` → empty; `grep -rli avm` hits five entries only as asides |
| `corpus/knowledge/2026-10-26-r39-be-squashfs-v4-core.md:44-45` | "Not held: AVM-BE bodies, vendor-mangled SquashFS" |

So the *class* is unheld, named Frontier in two places, and the round-39 `planned` row names it as
the second choice. Under prompt §6 item 9 a coverage claim "names the surface it moves (frontier →
core … or a new edge class)" — satisfied.

What is **already** held, and therefore cannot be re-sold as the coverage content: the handler branch
(round 39 Core entry, `:40`), the marker mechanism (S114), and — measured this session — the AVM
layout's extractability. Three commands already prove the branch at 80-file scale:

```
avm-80-gzip.sqsh   (LE headers + marker, gzip)  unblob 26.6.4 rc=0, 80 files, no failed chunk
markeronly-80.sqsh (BE headers + marker, gzip)  unblob 26.6.4 rc=0,  0 files, ExtractCommandFailedReport
sw-80.sqsh         (BE headers, no marker)      unblob 26.6.4 rc=0, 80 files
```

(`evidence/extract-matrix.txt`.) The claim's real new content is therefore **the vendor class**: two
vendor-origin members, xz, thousands of files, multi-block tables, published through REA. The
predicate must be written so that this — not the branch — is what `carriers_matched` counts (§5).

**Blocking contradiction.** The round-39 Core entry closes with a universal:

> `corpus/knowledge/2026-10-26-r39-be-squashfs-v4-core.md:40` — "An image whose `mkfs_time` equals
> `bytes_used` loses `-be` and fails; see the triage entry above."

That sentence is false for the class R40-C1 promotes (a genuine AVM-BE carries the marker *and*
extracts — round-39 E4 measured 2942 files; I measured it at 80 and 200 files). If the new Core row
lands without correcting it, the corpus will hold two Core statements that contradict each other and
the new entry's citation chain inherits a false claim. **Smallest safe correction:** bind the r39
entry's correction (qualified, with a two-way pointer, QUALITY #35/#36) into the same predicate, and
have the counter assert the corrected text.

## 2. (b) Do lane-built AVM carriers add discriminating power, or is vendor-only stronger?

**Verdict: they add almost none to a coverage claim, and one of the two drafted does not exist in
the format. Vendor-only is stronger; keep at most one synthetic as a cheap rerun/oracle arm.**

Measured, from the authoritative format note (Freetz, `evidence/freetz-avm-be-format.txt`, 1496 B,
sha256 `c1c43f6f…`):

> line 8: "the only data field stored in the little-endian format is the block length value at the
> beginning of each block"
> line 9: "compression method is hardcoded to be XZ (aka LZMA2)"
> line 16: "user id table is always stored uncompressed"
> line 5: "have COMP_OPT flag unset"

1. **The gzip synthetic is not an AVM image.** AVM-BE is XZ by definition. `L2` as drafted
   ("lane-built genuine AVM-layout carriers (gzip and xz)") names a format that cannot exist. It is a
   legitimate test of unblob's *branch* (marker + LE headers with the builtin gzip decompressor) but
   it must be labelled a branch control, not a carrier of the AVM class.
2. **The lane's own generator cannot produce the case that matters.** `gen-squashfs.py` writes valid
   images up to 200 files and *fails* above it (`evidence/generator-sweep.txt`: n=200 ok, n=250-400
   `rc=1`, "get_metadata: failed to read block / read_inode"). So every lane-built carrier has
   single-block metadata tables. The multi-block case — exactly where round 39 said "only
   plausibility separates them" — is exercised *only* by the vendor members (the 6490 BE member:
   inode table > 1 block, round-39 critic; candidate V2 below: directory table = 2 blocks, measured).
3. **Writer and oracle share one reading of the format.** A synthetic carrier's ground truth is the
   lane's own writer and the lane's own reader; a shared misreading is caught only by `sasquatch`,
   which is the tool the claim is measuring. That is not independent evidence, and prompt §6 item 9
   is explicit: "counting rows a sourceless fixture also counts is never coverage".
4. **What the synthetic genuinely adds:** (i) a KB-sized arm for the counter's rerun (the vendor
   members are MB); (ii) an oracle cross-check against a known tree (`tree-s80.tar`; the intended
   content is known exactly, so an oracle bug is detectable in a way it is not on vendor bytes);
   (iii) proof that the transform is cheap — `avmize.py` converts a standard BE image to the AVM
   layout by swapping **3** metadata headers (no offset moves, no payload change), and the result
   extracts (`sasquatch-v4be` noflag: 80 files; `-be`: 0; unblob: 80 files). That kills any argument
   that a synthetic carrier is expensive.

**Correction:** carriers are typed. `vendor` carriers (V1, V2) are the coverage surface and are what
`carriers_matched` counts; at most one `synthetic` carrier (xz + LE headers + marker) rides as a
supplementary arm and never counts as vendor coverage. Drop the gzip synthetic or relabel it a branch
control.

**The carrier-cost problem the draft does not address.** Any committed carrier is a lane-repo blob.
V1's AVM-BE member is 5.44 MB: under the helper's 10 MiB `--allow-large` threshold, but above the
1 MiB per-file skip inside a named directory, so the carrier files must be named explicitly in the
commit, not by directory. The V2 candidate I found is 35 MB (§6), which needs `--allow-large` and
permanently enlarges history. The claim must state a per-carrier and total size budget, and the L1
must measure candidates before the freeze.

## 3. (c) Is the rerun binding a real fix for R39-CL5, or does it move trust to the counter's run?

**Verdict: it is the right fix, but as drafted it is unsatisfiable; and yes, it moves trust — to the
right place — provided the predicate stops claiming what a receipt can prove.**

### 3.1 The clause as written can never pass

The draft says the fresh run "yields the same **semantic projection** as the committed receipt
(projection fields fixed in the freeze)". `semanticProjection` is REA's own term for the object it
hashes into `evidence_id` (`rea-agents/dist/domain/evidence.js:156-182`), and it contains
`parameters`, `raw_result` and `normalized_result` — all of which embed absolute run paths.

Measured (`evidence/projection.txt`; REA 6.5.0, unblob 26.6.4, run in `$S`, each rc=0, 2-3 s):

| comparison | differing leaf paths | `evidence_id` equal | derived D equal |
|---|---|---|---|
| K1: two fresh runs of the same file | 79 | no | **yes, 0 diffs** |
| K1: committed round-39 receipt vs fresh rerun | 82 | no | **yes, 0 diffs** |
| K5: two fresh runs of the same file | 162 | no | **yes, 0 diffs** |
| K5: committed round-39 receipt vs fresh rerun | 165 | no | **yes, 0 diffs** |

Differing subtrees in every case: `parameters`, `raw_result`, `normalized_result` (and `subject` when
the carrier path differs). Sample leaves: `parameters.output_directory`,
`normalized_result.output_directory`, `files[].path`, `raw_result[].task.path`, and the per-run REA
temp directory name `rea-firmware-XXXXXX` inside `diagnostics[].report.link/target`.

Consequence: a claim frozen with that clause is not a claim, it is a guaranteed honest stop — and the
temptation at scoring time is to narrow it after data, which §6 item 9 forbids ("Never narrow a
target after landing").

### 3.2 The fix is a named, path-normalized projection D (measured stable)

`projection-diff.py` computes D from the two envelopes and reports zero differences in all four
comparisons:

```
D = subject.digest.sha256, subject.format,
    provider.id, provider.version, operation,
    engine[name, version, executable_sha256, worker_count],
    selection[offset, length, sha256], coverage, published_bytes,
    sorted chunks[range.offset, range.length, handler, encrypted, extraction_failed],
    sorted files[relative_path, size, sha256],
    sorted gaps[kind, relative_path, dependencies, continuation_id],
    sorted unpublished_entries[relative_path, kind, link_target],
    sorted diagnostics report objects with link/target normalized at the '/extracted/' anchor,
    sorted derivations[parent_path, child_path] (both normalized), locations
EXCLUDED: parameters.*, raw_result, normalized_result.output_directory, files[].path,
          derivations[].provider_blob_id, files[].mime_type, files[].analysis_depth, timings
```

`derivations[].provider_blob_id` (measured `2559184:1`, `3028394:1`) and `mime_type` (libmagic) are
excluded deliberately: they are host/tool-version derived, not content derived. `locations` and
`continuation_id` were stable across runs *and* across the day boundary (committed receipt vs
today's rerun), so both may stay in D.

### 3.3 What the rerun actually closes, and what it does not

Round 39's fabricator (`w2/R39W2C1Fabricate.md`) built six receipts **from `oracle.tsv` and
`symlinks.tsv` alone** — no REA, unblob or sasquatch process — and scored 6/6. Under D its receipts
fail on `engine` (null vs unblob 26.6.4 + executable sha256), `coverage` (complete vs partial),
`diagnostics` (relative vs absolute link/target), `derivations` (6 vs 10) and the per-file records.
So the rerun closes that attack.

It does **not** close a fabricator who runs the pinned toolchain once and hand-assembles a receipt
whose D matches. That is not a hole to plug with more fields — reproducing D *is* the extraction
work, and if a seat can run REA on the carrier it has done the claim's work. The honest consequence
is the one the predicate must state:

> met_target rests on the counter's own run. The committed receipt is evidence of *consistency*, not
> of provenance. No clause may say the receipt "was produced by" the pinned toolchain.

**Who runs the counter, and what that implies.** The L1 at scoring time and the non-author closure
afterwards, both executing the same frozen script. Its bytes are therefore load-bearing: freeze
`c1-counter.py`, `c1-run.sh`/runner, `carriers.json`, the oracle tool, the oracle/symlink tables and
the knowledge entry, and reject any post-freeze edit (exit 2 `frozen_path_changed`).

**Scoring-time environment must be pinned, because the counter now does the extraction:**
- REA: invoke the local package root (`--pkg65`, as round 39 did), not `npx`; record
  `package.json.version` (6.5.0) and the sha256 of `scripts/rea.mjs` (`bin` → `scripts/rea.mjs`).
  `npx -y` at scoring puts network resolution inside the measurement.
- unblob: `REA_UNBLOB_COMMAND` absolute; `normalized_result.engine.executable_sha256` already
  records it — compare it to the freeze pin. Measured here: `unblob --version` 26.6.4, launcher
  sha256 `0ce7b624…1d09`, handler `squashfs.py` sha256 `2d7b901b…9287`.
- **Both** squashfs extractors: `squashfs.py`'s `get_dependencies()` returns
  `[EXECUTABLE, V4BE_EXECUTABLE]`, i.e. `sasquatch` **and** `sasquatch-v4be`. The draft binds only
  `sasquatch-v4be`. Record both paths + versions + sha256. Measured here: both 4.5.1;
  `sasquatch` sha256 `ad02d27a…4754` (382 824 B), `sasquatch-v4be` sha256 `fac88740…14c6`
  (436 232 B).
- Drift ⇒ exit **2** (`environment_drift`), never 1.

**Nondeterminism policy.** D was stable on 26 KB carriers on one host. Vendor-scale stability (2942
files) is untested here — the wave-1 bound forbids carrier runs — so it is `[INFERENCE]` that it
holds. Therefore: on the first D mismatch the counter reruns the carrier once and, if still
mismatched, exits **2** with reason `rerun_unstable` and records both D digests. A flaky environment
must not read as a falsified claim, and a silent retry-until-pass must not read as a met one.

## 4. (d) Is "first metadata block length decodes LE" sound on multi-block inode tables?

**Verdict: no — it is unsound in both directions, and it is satisfied by the claim's own kill
control.**

### 4.1 The killer: the draft's test passes on `markeronly-80.sqsh`

That file is `gen-squashfs.py --endian avm --comp gzip` — the draft's own kill control ("a
marker-only standard-BE carrier receipt relabelled"). Measured:

| image | layout | marker | first inode-table header LE / BE | draft clause | chain (LE / BE) |
|---|---|---|---|---|---|
| `markeronly-80.sqsh` | **BE** headers | **YES** | **139 / 2944 — both plausible** | **PASSES** | LE fails ×4 blocks, BE lands |
| `sw-80.sqsh` | BE headers | no | 139 / 2944 — both plausible | passes on the length half alone | LE fails, BE lands |
| `sw-20.sqsh` | BE headers | no | 4227 / 784 — both plausible | ambiguous | LE fails, BE lands |
| `avm-80-gzip.sqsh` | **LE** headers | YES | 2944 / 139 — both plausible | ambiguous | **LE lands**, BE fails |
| `avm-200-xz.sqsh` | LE headers | YES | 7328 / 8348 | LE (BE impossible) | **LE lands**, BE fails |
| round-11 `avm-be.squashfs` | LE headers | YES | 116 / 29696 | LE | **LE lands** (dir table 2 blocks) |
| 7490 07.62 member (candidate V2) | LE headers | YES | 804 / 9219 | LE | **LE lands** (dir table 2 blocks), BE fails |

(`evidence/chain.txt`.) Two *valid* BE images (`sw-20`, `sw-80`, both extract 20/80 files with
`-be`) are indistinguishable from an AVM body by the drafted clause, and the marker-only control
satisfies it outright. On the vendor members it happens to work (the BE reading is > 8192), which is
exactly what makes it dangerous: it passes for the wrong reason and cannot tell the carrier class
from the control.

### 4.2 The sound test: walk the header chain, then the format invariants

Two facts make this exact:

1. **Metadata blocks are always 8 KiB** (`SQUASHFS_METADATA_SIZE`), independent of the superblock's
   data `block_size` (4096/65536 on the images above). A header value outside `(0, 8192]` is
   impossible under any reading. (My first pass used `block_size` and mis-rejected a valid
   `block_size=4096` image with 8192-byte metadata blocks; the corrected script is in artifacts.)
2. **The stored length is the on-disk length**, so a chain walk advances `2 + len` and must land
   *exactly* on the next table's start. The fragment and id tables are reached through a `u64` index,
   so only two chains are adjacent: `inode_table_start → directory_table_start` and
   `directory_table_start → fragment_table_start` (skip the second when `fragments == 0`).

On multi-block tables this is decisive: `avm-be.squashfs`'s directory table spans 2 blocks and lands
under LE only; `avm-200-xz`/`filesystem.image`'s BE walk dies within 2 blocks. The r39 entry's
"only plausibility separates them" was an artefact of reading one header; the chain removes the
plausibility step entirely.

**Add the format invariants the source states, which are cheaper than the chain and independent of
it** — all measured on the 7490 member: `flags & 0x400 == 0` (COMP_OPT unset); every id-table
metadata block has the uncompressed bit (`0x8000`) set (measured header `0x8004`; the BE reading
`0x0480`/len 1152 is both wrong and implausible); compression id 4 (xz) for vendor carriers.

## 5. (e) Universal clauses the counter does not enumerate

Each is a clause whose quantifier the frozen counter must be able to close over a set that exists at
the freeze. Sorted by severity.

| # | clause as drafted | problem | enumerable fix |
|---|---|---|---|
| **U1** | "yields the same semantic projection" | unsatisfiable (§3.1) | named D, path-normalized, sorted (§3.2) |
| **U2** | "its first metadata block length decodes as little-endian" | passes on the kill control and on valid BE images (§4) | header chain + invariant triple |
| **U3** | "publishes every regular file of the frozen independent oracle" | no clause forbids **extra** published files: a receipt may publish the oracle set plus junk | published regular-file set **equals** the oracle set, modulo the extraction prefix and the gap rule |
| **U4** | "carries only the extraction gaps the frozen gap rule allows (rule fixed in the freeze from development recon)" | a *kind* whitelist is enumerable but vacuous: any count of any allowed kind passes | compute the expected gap multiset from the oracle's symlink table (exactly one `unpublished-entry` per in-tree link, nothing else, no escaping path published) — carrier-independent, as round 39 already did |
| **U5** | "first added in a commit descending from the freeze" | round 39's `git log --diff-filter=A` returns the **oldest** add, so overwriting a receipt that was first added after the freeze passes (that is how R39W2C1Fabricate stayed green) | require: absent at FREEZE **and** the blob at REV equals the blob introduced by its first add (no later modification) |
| **U6** | "a round-40 frontier note supersedes the AVM part of the Frontier text" | not decidable from bytes: the check is a marker-string presence test; the sentence can exist and supersede nothing | state it as a presence binding, and add the two-way content check: the r39 Core entry's false universal is **absent or qualified** (§1) |
| **U7** | "no frozen C1 path changed after the freeze" | the draft never names the set; the oracle tool and the oracle/symlink tables are not in round 39's tuple, and the knowledge entry is not frozen | enumerate: claims, counter, runner, `carriers.json`, `tools/round-40/sqfs-list.py`, every `oracle.tsv`/`symlinks.tsv`, the carrier blobs, the r40 entry, PROVINCE/README/SOURCES citations |
| **U8** | "sasquatch-v4be 4.5.1 on the child PATH" | unblob requires **both** `sasquatch` and `sasquatch-v4be`; a missing `sasquatch` changes the reported gaps for reasons unrelated to the carrier | bind both, with path + version + sha256; drift ⇒ exit 2 |
| **U9** | "carriers_matched == 4" | counts 2 synthetic carriers toward a coverage move (§2) | split `vendor_matched` from `supplemental_matched` |
| **U10** | "Command that shows it unmoved: the counter at the freeze exits 1" | only true if the counter, `carriers.json`, the oracle tool and the oracle/symlink tables are all in the **freeze** commit | freeze them together; otherwise the before-arm is exit 2 (`unevaluable`), not 1 |

## 6. Candidate V2 — obtainable, but the draft has no size budget

No extraction was run: this is a superblock parse plus a metadata-header walk on a *different*
vendor image, which is not (and need not become) a carrier. The member was read into memory for
those checks; nothing was written outside my scratch and artifacts directories.

- `https://download.avm.de/fritzbox/fritzbox-7490/other/fritz.os/FRITZ.Box_7490-07.62.image` —
  HTTP 200, 38 092 800 B, sha256 `2ab05656…f8ee9`
- tar member `./var/tmp/filesystem.image` — **35 012 616 B**, sha256 `58d73b2f…74e5`
- superblock: `sqsh`, major 4, comp **4 (xz)**, block_size 65 536, `mkfs_time == bytes_used`
  (**marker YES**), `flags 0x2c0` (**COMP_OPT unset**), `fragments 1`, `no_ids 1`, `inodes 105`
- chain: LE lands on both adjacent tables (directory table **2 metadata blocks**), BE fails
- id-table metadata block header `0x8004` → uncompressed (BE reading `0x0480` impossible)

Two things for the L1: (i) the naive version swap is not a route — `-07.57` for 7490/7590/6690/5590
all 404; the current files are 07.62 and 08.25, and only a per-model listing finds them; (ii) the
35 MB member is a **commit-size problem** the draft does not mention. `inodes 105` is surprising for
a 35 MB member and must be confirmed by the oracle's regular-file count before V2 is pinned
(`[INFERENCE]` on my part: it may be an initramfs-style image; the class is still AVM-BE). If no
candidate yields a small member, state the repo growth and use `--allow-large`; do not discover it at
the freeze.

## 7. Defect list (what must change before the freeze)

1. **D1** Replace "same semantic projection" with the named D of §3.2 — otherwise the target is
   unreachable by construction (measured 79/82/162/165 differing leaves; `evidence_id` differs).
2. **D2** Replace the first-header endianness test with the header-chain walk + invariants of §4.2.
3. **D3** Split vendor from synthetic in the target; relabel or drop the gzip synthetic (AVM-BE is
   XZ by definition).
4. **D4** Source the layout definition: no lane row quotes the block-length sentence. S112 quotes the
   `case Endian.BIG, 4` branch but **not** the marker branch; S114 quotes the marker but not the
   block-length sentence, its `used-by` lists only the r38 entry, and its URL is an **unpinned
   `master`** (`https://raw.githubusercontent.com/Freetz/freetz/master/...`, 1496 B, sha256
   `c1c43f6f…`). Add a new pinned row (commit sha + sha256) quoting line 8, with `used-by` naming the
   r40 entry; that also satisfies §2b's "sourced claim" honestly rather than by date collision with
   round 39's rows (both rounds are dated 2026-10-26).
5. **D5** Bind the correction of `2026-10-26-r39-be-squashfs-v4-core.md:40` (false universal) with a
   two-way pointer.
6. **D6** Do not keep a receipt-freshness clause that overwriting satisfies (U5).
7. **D7** Add set equality on published files (U3) and the computed gap multiset (U4).
8. **D8** Pin both squashfs extractors and the REA package by path + sha256; no `npx` at scoring;
   drift ⇒ exit 2.
9. **D9** Nondeterminism policy: one rerun, then exit 2 `rerun_unstable` with both D digests.
10. **D10** State a carrier size budget and pin V2 before the freeze (§6).

## 8. Replacement predicate (P40-C1 v2)

> At the measured revision, for each of the four frozen carriers, with all C1 paths frozen at F:
>
> **Identity** (computed by the counter from carrier bytes, no extraction): I1 magic `sqsh`, major 4,
> minor 0; I2 `mkfs_time == bytes_used`; I3 the 2-byte LE metadata-header walk from
> `inode_table_start` lands exactly on `directory_table_start` and from `directory_table_start`
> exactly on `fragment_table_start`, every length in (0, 8192], and on each **vendor** carrier at
> least one of those tables spans ≥ 2 metadata blocks; I4 walking the same two chains with **BE**
> headers does **not** land on both table starts (the wrong-endian walk must fail, which is what
> makes I3 decisive rather than plausible); I5 `flags & 0x400 == 0`; I6 every id-table metadata
> block carries the uncompressed bit; I7 compression id 4 (xz) on vendor carriers.
>
> **Receipt** (`corpus/evidence/round-40/c1/<id>/after.json`): R1 parses; operation
> `extract_firmware`, provider `unblob` 26.6.4; R2 the path is absent at F and the blob at REV equals
> the blob of its first add; R3 `subject.digest.sha256` equals the carrier pin and `evidence_id`
> recomputes under the frozen 6.5.0 rule; R4 a chunk names `squashfs_v4_be` and no chunk has
> `extraction_failed`; R5 the published regular-file set **equals** the oracle set (same relpath
> suffix, same sha256, no extras) modulo the gaps of R6; R6 the gap multiset is exactly one
> `unpublished-entry` per in-tree symlink of the frozen table, and no published path ends with an
> escaping symlink's relpath.
>
> **Rerun** (the R39-CL5 binding): W1 the counter materializes each carrier from `git show REV:path`
> into scratch (hash-checked against the pin) and runs REA 6.5.0 `extract-firmware` itself from the
> pinned local package root, with `REA_UNBLOB_COMMAND` = pinned unblob and **both** `sasquatch` and
> `sasquatch-v4be` pinned on the child PATH, one fresh outdir per carrier; W2 the run's derived
> projection D (§3.2) equals the receipt's D; W3 the same run satisfies R4–R6 in its own right;
> W4 on a D mismatch the counter reruns once, then exits 2 `rerun_unstable` recording both digests;
> W5 environment pins match the freeze record, else exit 2 `environment_drift`.
>
> **Documentation**: B1 PROVINCE holds `## Round-40 additions to Core` with a row naming the AVM
> layout and citing the r40 entry; B2 the entry exists, cites a SOURCES row **first added this
> round** whose `used-by` lists it, and carries a Limits sentence naming what is not held; B3 the
> r39 entry's universal sentence is corrected with a two-way pointer; B4 a r40 frontier note exists
> naming the AVM-BE text it supersedes (presence binding); B5 `corpus/README.md` maps the entry
> stem; B6 no frozen C1 path changed after F.
>
> **Target**: `vendor_matched == 2 ∧ supplemental_matched == 2 ∧ every binding true`, where
> `matched` = I1–I7 ∧ R1–R6 ∧ W1–W5.
>
> **Honest limit the entry must state**: the rerun shows the carrier extracts through the pinned
> toolchain **now**; it does not show the committed receipt was produced by that toolchain. Provenance
> of a receipt is not provable from bytes and is not claimed.

## 9. Evidence

Artifacts (all in `.ufo/waves/round-40/w1/artifacts/R40C1AxisFit/`):

| file | what it is | sha256 (prefix) |
|---|---|---|
| `projection-diff.py` | D vs full-projection comparator | `19774ade…` |
| `meta-chain.py` | header-chain + first-length comparator | `6c4060c5…` |
| `avmize.py` | standard BE → AVM-layout converter (header swap + marker) | `1b2aac80…` |
| `evidence/projection.txt` | the four comparisons above | — |
| `evidence/chain.txt` | chain table for 8 images | — |
| `evidence/extract-matrix.txt` | sasquatch ×2 flags, unblob, 5 images | — |
| `evidence/generator-sweep.txt` | generator validity + first-length verdicts, n=5..400 | — |
| `evidence/v2-candidate-7490.txt` | candidate V2 superblock, shas, invariants | — |
| `evidence/freetz-avm-be-format.txt` | the format note (1496 B) | `c1c43f6f…` |
| `evidence/avm-80-gzip.sqsh` / `avm-80-gzip-nomarker.sqsh` / `avm-200-xz.sqsh` | AVM-layout synthetics | `a019a08d…` / `4581651b…` / `32db63f0…` |
| `evidence/markeronly-80.sqsh` / `sw-80.sqsh` / `sw-20.sqsh` | the control and its two BE parents | `6ffbb577…` / `f2c214f0…` / `c4b7ee4e…` |
| `evidence/rea-K1-run1.json`, `evidence/rea-K5-run1.json`, `evidence/rea-K5-run2.json` | raw REA envelopes | — |
| `evidence/tree-s80.tar` | the 80-file tree the synthetics carry | — |
| `evidence/commands.txt` | every command behind the above | — |

Key commands and exit codes:

```
npx -y rea-agents@6.5.0 extract-firmware --format json --full-output $S/in/K5.sqsh $S/runs/K5-run1/extract   # rc 0, 3 s
python3 .../projection-diff.py runs/K5-run1/raw.json runs/K5-run2/raw.json
  -> evidence_id_equal false, full_projection_diff_count 162, derived_diff_count 0
sha256sum .../unblob/handlers/filesystem/squashfs.py -> 2d7b901b…   (lines 41-52: is_avm branch;
                                             get_dependencies -> [sasquatch, sasquatch-v4be])
~/.local/bin/sasquatch-v4be [-be] -f -d OUT IMAGE     # matrix in evidence/extract-matrix.txt
~/.local/bin/unblob -e OUT/extract IMAGE              # rc 0 even on extraction failure
python3 .../meta-chain.py ...                          # chain table in evidence/chain.txt
```

Wave-1 limits observed: no REA/unblob on V1's member, on any second vendor member, or on any
lane-built AVM carrier; vendor-scale rerun stability untested (`[INFERENCE]`, mitigated by W4);
`unblob`'s AVM branch was exercised only on my own synthetics and on no carrier.

## 10. Freeze-time checklist for the L1 (short)

1. Pin V2 and record its image/member shas + size; confirm the member count with the oracle; set the
   carrier size budget.
2. Freeze in one commit: claims, counter, runner, `carriers.json`, `tools/round-40/sqfs-list.py`,
   oracles + symlink tables, carrier blobs, the r40 entry, and the r39-entry correction.
3. Add the pinned Freetz row (commit sha + sha256) and quote line 8.
4. Freeze the environment record: unblob version + executable sha256, both sasquatch binaries, REA
   package version + `scripts/rea.mjs` sha256.
5. Seed the counter's D implementation with `projection-diff.py`'s exclusion list; run the counter at
   F and commit the exit-1 receipt as the before-arm.
6. Build the two rerun-stability receipts on **development** inputs only; the carrier reruns happen
   after the freeze.
