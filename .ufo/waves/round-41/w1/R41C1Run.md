# R41C1Run — round-41 `c1-run.sh` port (R41-C1 receipt harness)

**VERDICT: DONE** — `c1-run.sh` is ported to round 41 (scratch segment `/kaidoku-r41/`, claim
`R41-C1`, schema `kaidoku-r41-c1-run-v1`, output contract `corpus/evidence/round-41/c1/<id>/`),
run end-to-end on a development input only (the round-40 lane-built `L1` carrier), and proven
structurally identical to the frozen round-40 receipts: **run.json 130/130 key paths, after.json
250/250 key paths, zero type mismatches**, every leaf difference in an allowed class (paths,
timestamps, durations, digests, schema/claim). No reserved carrier, source image or member was
read, extracted or invoked.

Seat: R41C1Run (leaf). Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, base
`49096c7e6f226af0c750c4b003be58883cb6049f`. Nothing was frozen, no VCS mutation, nothing
installed or upgraded.

---

## 1. Axes (Godspeed)

| axis | what this seat moved |
|---|---|
| **coverage** | the round-41 C1 receipt producer exists and is exercised: one command turns a carrier file into `after.json` (the REA `data` object the counter scores) + `run.json` (argv, pins, exit, timing, envelope digest) inside a scratch tree whose segment satisfies the counter's `run_provenance_ok` clause. |
| **depth** | the port is proven, not asserted: exact port diff (10 hunks, identity-only), per-key structure diff against both frozen round-40 L1 artifacts, a 4-receipt projection equality check, and 9 exercised negative gates (foreign scratch refusal + escape, bad mode, missing carrier, pre-created extraction root → exit 3 with the structured REA reason, `hsqs` refusal, no-magic refusal, reader `--help` gate, scratch cleanup on success *and* failure). |
| **calibration** | every claim in this report is a recorded exit code, digest or key-path count; the two things not measured here (REA behaviour on the reserved vendor members, the round-41 reader) are named as limits instead of assumed. |

## 2. Deliverables (`.ufo/waves/round-41/w1/artifacts/R41C1Run/`)

| file | sha256 | role |
|---|---|---|
| `c1-run.sh` | `bdb97632d21bac71d603b73f13372264efb89c84baaf07d902ead6f33149cc7f` | the port; **copy to `tools/round-41/c1-run.sh`** |
| `port.diff` | `cafa56ef9bd467fba12bb4f195c7f15698edd3c3a5b8cd236609a0aeb64c5dcc` | `diff -u` of base `tools/round-40/c1-run.sh` → this file (evidence that only identity changed) |
| `json-struct-diff.py` | `aacb0eaa708ef6ef70551228b5bb255907e0a4b7386c07e205621423d6034cb0` | structure comparer used in §5 (key paths, types, leaf diffs); **not** a frozen tool |
| `projection-compare.py` | `d23552ab41ba267809500d9b12d33d87382ca33b2e2ff875a439846b0c2b4ea4` | extract-root-relative projection comparer used in §6; **not** a frozen tool |
| `evidence/after-L1/{run.json,after.json}` | `4589ff36…e2a84` / `60f74d8b…38e438` | the development run of §4 |
| `evidence/after-L1/struct-diff-{run,after}.txt` | — | outputs of §5 |
| `evidence/after-L1/projection-compare.txt` | — | output of §6 (4 receipts, one digest) |
| `evidence/oracle-L1/{oracle.tsv,nonregular.tsv,oracle-check.tsv,oracle-run.json}` | `c3c77fc0…cc9751` / `b97ae59f…d612` / `c3c77fc0…cc9751` / `67aa9439…5c3d2` | the oracle arm of §7 |
| `evidence/oracle-L1/struct-diff-oracle-run.txt` | — | §7 structure diff |
| `evidence/negative/*` | see §8 | logs and `run.json`s of the negative gates |

Total 168 KB; no artifact exceeds the 5 MB cite-by-digest threshold, and nothing copied here is
vendor bytes (the carrier used is lane-built `L1`, sha256 `2521ded6d06ff12dbe70533598dbe5f3f3b0e58ae1cfe8f80b88c4f0849c1a0d`).

## 3. The port (exact)

Source: `git show 49096c7e6f226af0c750c4b003be58883cb6049f:tools/round-40/c1-run.sh`
(sha256 `de3f4af8305a56376da4f424192b6fe8c0c98353959e6976512db7034639dbdd`, 604 lines).
`port.diff` has **10 hunks / 141 diff lines, all comment text, path strings and two jq arguments**:

1. header: `R41-C1 … ported from tools/round-40/c1-run.sh`; output locus named as
   `corpus/evidence/round-41/c1/<id>/`;
2. reader is described as carried from round 40, default `tools/round-41/sqfs-list.py` (once frozen);
3. `/kaidoku-r40/` → `/kaidoku-r41/` in the provenance prose, usage text, `scratch_root`, the
   `case` pattern, the refusal and warning messages, and the `R40-C1` → `R41-C1` clause names;
4. `reader not found` / `not readable` messages say "round-41 reader";
5. `--arg schema kaidoku-r40-c1-run-v1` → `kaidoku-r41-c1-run-v1` (all three writers: oracle
   reader-failure receipt, oracle receipt, after receipt);
6. `--arg claim R40-C1` → `R41-C1` (same three writers);
7. the `--max-depth 1` rationale comment is re-dated to round 41, still citing round-40's
   `R40C1ReconGaps §6` as the origin of the parameter.

**No executable logic changed.** Not changed, deliberately:

* the after arm still does **not** reject an `hsqs` carrier — it records the superblock
  (`magic`, `byte_order`, `mkfs_time`, `bytes_used`, `avm_marker`) and lets the counter decide;
  adding a BE-only gate to the *receipt producer* would make a control arm (LE/relabelled
  receipts) unable to produce the receipt that falsifies it;
* the REA invocation is byte-identical:
  `npx -y rea-agents@6.5.0 extract-firmware --format json --full-output --max-depth 1 <carrier> <scratch>/extract`,
  `REA_UNBLOB_COMMAND` absolute (default `$HOME/.local/bin/unblob`), cwd = scratch, `TMPDIR` = scratch;
* the oracle arm (independent reader + `sasquatch-v4be -f -no-exit-code -n`, **no `-be`**,
  table grammar validation, `files_equal` gate) is kept whole;
* the exit map stays `0` ok / `2` usage+environment / `3` tool failure;
* `C1_KEEP_ENVELOPE`, `C1_ALLOW_FOREIGN_SCRATCH`, `C1_READER`, `HYAKU_SCRATCH` are unchanged.

### 3.1 `run.json` contract (unchanged field set, round-41 schema)

Top-level keys, in emission order (25, verified on the produced receipt):
`schema mode claim carrier{path,sha256,size_bytes,superblock{magic,byte_order,mkfs_time,bytes_used,avm_marker}} outdir argv argv_shell cwd run_provenance_segment_ok extraction_root start_utc end_utc duration_ms exit rea{pin,version,package_root} unblob{env_value,command_env,sha256,version} sasquatch_v4be{path,sha256,version,version_line} child_path envelope{parseable,ok,sha256,bytes,error} envelope_data_summary data_extracted receipt_written receipt previous_after_json_sha256 stderr_head`.

Why the segment renaming is the load-bearing change: the frozen counter's
`run_provenance_ok` clause is a substring test on the receipt's `parameters.output_directory`
(`tools/round-40/c1-counter.py:200` `PROV_SEGMENT = '/kaidoku-r40/'`,
`:596-603` `provenance_ok`), and `parameters` sits inside the hashed semantic projection, so the
extraction root must carry this round's segment or `evidence_id_ok`/`run_provenance_ok` cannot both
hold. With the port, the default scratch is
`${HYAKU_SCRATCH:-/fast/scratch/hyaku}/kaidoku-r41/c1-run.XXXXXX`, so
`parameters.output_directory` = `…/kaidoku-r41/c1-run.XXXXXX/extract` — demonstrated in §4.

## 4. Proof run (development input only)

Input: the round-40 lane-built `L1` carrier, copied into a scratch copy of the round-41 evidence
layout (no reserved carrier was touched):

```
S=/fast/scratch/hyaku/kaidoku-r41/R41C1Run; export TMPDIR="$S" HYAKU_SCRATCH=/fast/scratch/hyaku
mkdir -p "$S/evidence/round-41/c1/L1"
cp <lane>/corpus/evidence/round-40/c1/L1/carrier.sqsh "$S/evidence/round-41/c1/L1/carrier.sqsh"
bash .../R41C1Run/c1-run.sh after "$S/evidence/round-41/c1/L1/carrier.sqsh" "$S/evidence/round-41/c1/L1"
```

Result: **exit 0**, no stdout/stderr, `after.json` (11097 B) + `run.json` (6471 B). Receipt facts:

| field | value |
|---|---|
| `schema` / `claim` | `kaidoku-r41-c1-run-v1` / `R41-C1` |
| carrier | `2521ded6…84f0849c1a0d`, 230884 B, superblock `sqsh`/big, `mkfs_time = bytes_used = 230884`, `avm_marker true` |
| `run_provenance_segment_ok` | `true`; `extraction_root` `/fast/scratch/hyaku/kaidoku-r41/c1-run.Zjpkub/extract` |
| argv | `npx -y rea-agents@6.5.0 extract-firmware --format json --full-output --max-depth 1 …` (11 elements, index 7 = `--max-depth`, 8 = `1`, 9 = carrier, 10 = `<scratch>/extract`) |
| pins | rea `6.5.0` at `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`; unblob `26.6.4` sha256 `0ce7b624…cba1d09`; sasquatch-v4be `4.5.1` sha256 `fac88740…b7214c6` |
| envelope | parseable, `ok true`, `error null`, 11174 B |
| receipt | evidence id `ev_63c5f440…0f01b09`, `coverage partial`, handlers `["squashfs_v4_be"]`, files 7, gaps 3 (1 `depth-limited` + 2 `unpublished-entry`), published_bytes 238530, `subject.digest.sha256` = carrier pin |

Timing recorded: `duration_ms 2009`, `start 2026-10-26T20:19:47Z`, `end 20:19:49Z`.

## 5. Structure diff vs the frozen round-40 L1 artifacts

```
python3 -I -B artifacts/R41C1Run/json-struct-diff.py \
  <lane>/corpus/evidence/round-40/c1/L1/run.json    "$S/evidence/round-41/c1/L1/run.json"
python3 -I -B artifacts/R41C1Run/json-struct-diff.py \
  <lane>/corpus/evidence/round-40/c1/L1/after.json  "$S/evidence/round-41/c1/L1/after.json"
```

| document | key paths A / B / common | only-A | only-B | type mismatch | list-length mismatch | verdict |
|---|---|---|---|---|---|---|
| `run.json` | 130 / 130 / 130 | 0 | 0 | 0 | 0 | `STRUCTURE_EQUAL` |
| `after.json` | 250 / 250 / 250 | 0 | 0 | 0 | 0 | `STRUCTURE_EQUAL` |

Leaf differences, exhaustively in the allowed classes (full lists in
`evidence/after-L1/struct-diff-*.txt`):

* `run.json`, 20 leaves: `schema`, `claim`, `carrier.path`, `outdir`, `argv[9]`, `argv[10]`,
  `argv_shell`, `cwd`, `extraction_root`, `start_utc`, `end_utc`, `duration_ms`,
  `envelope.{sha256,bytes}`, `receipt.{sha256,bytes,evidence_id,output_directory}`,
  `envelope_data_summary.{evidence_id,output_directory}`. Everything else — pins, `child_path`,
  `superblock`, `run_provenance_segment_ok`, `data_extracted`, `receipt_written`,
  `previous_after_json_sha256`, and the whole scored `envelope_data_summary` body (coverage,
  handlers, files, published_bytes, gaps, gap details, unpublished entries, selection/subject
  digests) — is **identical**.
* `after.json`, 26 leaves: `evidence_id`, five REA-internal blob ids (`chunks[0].provider_id`,
  `derivations[0].provider_blob_id`, `report[0].task.blob_id`, `report[1].reports[3].id`,
  `report[1].subtasks[0].blob_id`), every absolute path under
  the scratch root (`parameters.path`, `parameters.output_directory`,
  `normalized_result.output_directory`, `files[*].path`, `raw_result.*` paths, `subject.local_path`).
  All semantic fields (chunk handler/range/`extraction_failed`, file relpaths/sha256/size, gap
  kinds and relative paths, unpublished entries, published bytes, coverage) are identical.

## 6. Receipt determinism (4 receipts, one projection)

`projection-compare.py` strips the scratch root and digests the scored projection
(operation, provider, engine+sha256, selection/subject digest, coverage, chunk list, per-file
relpath+sha256+size, gaps, unpublished entries, published bytes, depth-limited paths):

```
78f053611595c321100bfbb31786c5e3388b3d5ee8d2e57990482e6cf6e2d4b9  <lane>/…/round-40/c1/L1/after.json
78f053611595c321100bfbb31786c5e3388b3d5ee8d2e57990482e6cf6e2d4b9  $S/evidence/round-41/c1/L1/after.json     (default scratch)
78f053611595c321100bfbb31786c5e3388b3d5ee8d2e57990482e6cf6e2d4b9  $S/out-t1b/after.json                    (foreign scratch, escape path)
78f053611595c321100bfbb31786c5e3388b3d5ee8d2e57990482e6cf6e2d4b9  $S/out-t6/after.json                     (second run into an existing OUTDIR)
=> PROJECTIONS_EQUAL  (files=7 gaps=3 unpublished=2 coverage=partial handlers=['squashfs_v4_be'] published_bytes=238530)
```

Receipts (and evidence ids) differ between runs because the scratch temp name is hashed in; the
projection does not. That is the property the counter's `projection_ok` clause relies on.

## 7. Oracle arm still intact (same development carrier)

```
C1_READER=<lane>/tools/round-40/sqfs-list.py bash c1-run.sh oracle \
  "$S/evidence/round-41/c1/L1/carrier.sqsh" "$S/out-t5"     # exit 0
```

* `oracle.tsv` and `nonregular.tsv` are **byte-identical** to the frozen round-40 L1 tables
  (`c3c77fc0…cc9751`, `b97ae59f…d16d612`); this round-41 run's `oracle-check.tsv` has the same
  digest as `oracle.tsv`, i.e. the `sasquatch-v4be` (no `-be`) cross-check agreed on every row.
* `oracle-run.json` structure-diff vs frozen round-40 L1 `oracle-run.json`: **125/125 key paths,
  0 only-A/B, 0 type mismatch, 0 list-length mismatch → `STRUCTURE_EQUAL`**; the 16 differing
  leaves are `schema`, `claim`, `carrier.path`, `outdir`, `scratch_root`, reader/sasquatch argv
  scratch paths, UTC times, `reader.duration_ms`, `reader_inspect.image`.
* The reader used is the round-40 frozen reader via `C1_READER`: **no round-41 reader exists yet**,
  so the arm's default (`$SCRIPT_DIR/sqfs-list.py`) cannot resolve in this artifacts directory
  (that is also what the `reader not found` gate reported in T9/T10 first attempt — see §8).

## 8. Negative gates exercised (dev inputs, no reserved carrier)

| # | invocation | exit | observed |
|---|---|---|---|
| T1 | `after` with `SCRATCH=/fast/scratch/hyaku/foreign-R41C1Run/scratch` | **2** | `SCRATCH … lacks a /kaidoku-r41/ segment: a receipt written from it fails the R41-C1 run-provenance clause…`; no scratch dir created |
| T1b | same + `C1_ALLOW_FOREIGN_SCRATCH=1` | **0** | warning on stderr, `run_provenance_segment_ok: false`, receipt still written (7 files, `squashfs_v4_be`) |
| T2 | `bogus` mode | **2** | usage text on stderr |
| T3 | missing carrier path | **2** | `carrier is not a regular file: …` |
| T4 | pre-created `<scratch>/extract` (REA refuses an existing root) | **3** | `run.json` written with `exit 1`, `envelope.ok false`, `envelope.error.details.diagnostics.reason = "Extraction output root already exists"`, `data_extracted false`, `receipt_written false`, `receipt null`; **no** `after.json`; scratch removed by the trap afterwards |
| T5 | `oracle` on L1 with `C1_READER` = round-40 reader | **0** | tables + `oracle-run.json`, `files_equal` |
| T9 | `oracle` on a 4 KiB `hsqs`-magic file | **2** | `oracle arm is for AVM-layout BIG-ENDIAN images (sqsh); … has hsqs at 0` |
| T10 | `oracle` on a 4 KiB no-magic file | **2** | `no squashfs magic (sqsh|hsqs) in the first 1 MiB …` |
| T11 | `oracle` with a reader whose `--help` omits `--layout` | **2** | `reader does not advertise --layout in --help: …` |
| T7 | `C1_KEEP_ENVELOPE=1` | **0** | `after.envelope.json` written (11174 B, parseable) alongside `after.json`/`run.json` |
| T8 | second `after` run into the same OUTDIR | **0** | `previous_after_json_sha256` = `6319637221a017281a23423a55dc126ba1f4a04f89ccfbb089e527be59e5de1e` = the first run's `receipt.sha256` (pre-overwrite chain works) |

Side observations (not defects): OUTDIR is `mkdir -p`-ed before an arm dispatches, so T9/T10 left
empty outdirs; unblob.log/REA staging always land inside the scratch and die with it (no
`kaidoku-r41/c1-run.*` directories remained after any run — checked after §4, T1b, T4, T8).

## 9. Lint / syntax

* `bash -n c1-run.sh` → rc 0.
* `shellcheck -S style c1-run.sh` → rc 1 with exactly one finding, `SC1007` at
  `SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd -P)`. **Pre-existing**: the frozen
  `tools/round-40/c1-run.sh` reports the same single finding (rc 1). It is a false positive
  (`CDPATH=` is a command-scoped assignment prefix, not a spaced assignment). Left untouched to
  keep the port diff identity-only; `shellcheck -S style -e SC1007` and
  `shellcheck -S warning -e SC1007` both exit **0**.

## 10. Tooling, environment, limits

* **Nothing installed, upgraded or moved.** Versions observed at run time are the pins in §4;
  no `pacman` transaction, no `uv`/`npx` install (`npx -y rea-agents@6.5.0` reused the existing
  `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`).
* Reserved carriers: **not read, not extracted**. The only carrier bytes hashed/parsed here are the
  lane-built round-40 `L1` carrier; the two synthetic 4 KiB files exist only to reach the magic gates.
* Not measured by this seat, and therefore not claimed:
  * behaviour of the port on the reserved `V3`/`V4` vendor bytes or on `L3`/`L4` (the `--max-depth 1`
    budget reasoning is carried as a comment, not re-derived here) — [INFERENCE] it holds, since the
    argv and the REA/unblob/sasquatch pins are unchanged and the vendor-member budget was measured
    in round 40 (`R40C1ReconGaps §6`);
  * the round-41 independent reader / counter / classifier: the oracle arm was proven with the
    round-40 frozen reader through `C1_READER`. When the round-41 reader lands, running
    `c1-run.sh oracle <carrier> <outdir>` with no `C1_READER` is the acceptance check that the
    default resolves;
  * anything about PROVINCE/README/SOURCES or the C2 table — other seats.
* Evidence caveat: the receipts copied into `evidence/` reference scratch paths
  (`/fast/scratch/hyaku/kaidoku-r41/…`) that were removed after the runs, as required; the carrier
  they describe is reproducible from its sha256 `2521ded6…c1a0d` at
  `<lane>/corpus/evidence/round-40/c1/L1/carrier.sqsh`.

## 11. Integration notes for L1

1. Copy `c1-run.sh` → `tools/round-41/c1-run.sh` (mode 0755 / `git update-index --chmod=+x` as the
   lane does for round-40), next to the round-41 `sqfs-list.py` so the oracle arm's default resolves.
2. Freeze it with the other C1 tools; the counter's `FROZEN_PATHS` must then name
   `tools/round-41/c1-run.sh` and its `PROV_SEGMENT` must be `/kaidoku-r41/`. **Observed, out of my
   scope**: the round-41 counter artifact still lists `'tools/round-40/c1-run.sh'`
   (`artifacts/R41C1Counter/c1-counter.py:243`) — its owner has to re-point that tuple, otherwise
   freezing this file cannot be detected as a frozen-path change.
3. Per-carrier receipt procedure after the freeze (one carrier, one outdir):
   `bash tools/round-41/c1-run.sh after <carrier bytes> corpus/evidence/round-41/c1/<ID>` — default
   scratch gives the `/kaidoku-r41/` provenance segment; do not pass a fourth argument unless it
   contains that segment.
