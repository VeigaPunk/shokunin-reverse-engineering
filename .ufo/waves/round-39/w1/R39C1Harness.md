# R39C1Harness — R39-C1 run harness (pre-freeze build + test receipts)

**VERDICT: DONE** — `c1-run.sh` (`after` / `oracle`) and `mk-carriers.py` are written, exercised on
K1/K2 **copies only**, semantically identical to the round-38 receipts on the graded payload, and
covered by a 68-case selftest (68/68 green). Nothing frozen yet; no lane file outside this seat's
artifacts dir and this report was written.

Claim item: R39-C1 (coverage) — pre-freeze tooling. Data generation is post-freeze work owned by the
L1; this seat supplies the two tools and the receipts that prove they work.

---

## 1. Deliverables

All under `.ufo/waves/round-39/w1/artifacts/R39C1Harness/`.

| file | sha256 | role |
|---|---|---|
| `c1-run.sh` | `422dbddc5186df5bd8d602c8f06990f30db9f4c09d4ee2e88023db1eef75aa14` | run harness; **copy to `tools/round-39/c1-run.sh`** (frozen path) |
| `mk-carriers.py` | `41f7a581315dc2721eec01f911eab6a8746163771778e75471ada426a9f6ae7a` | emits `.ufo/waves/round-39/c1/carriers.json` with sha256 pins |
| `compare-after.py` | `3c94ed0953ceeb3b8955ee881d89366935aa20bbddfcbaf931582d2265a9e082` | test-only semantic comparator (graded payload, volatile fields excluded) |
| `selftest.sh` | `e181990babfdd1709b0859338ed058a7c62f29a455ee02ef6353593f0883d9f0` | 68 cases over both tools, K1/K2 copies |
| `selftest-tally.json`, `selftest-stdout.txt`, `selftest-stderr.txt` | — | selftest receipt (stderr empty) |
| `receipts/K{1,2}/{after.json,run.json}` | `K1 after.json a438da85…f1603e` (20 183 B), `K2 after.json 7c2855ae…eb9a38` (18 055 B) | harness output on K1/K2 copies |
| `oracle/K{1,2}/{oracle-check.tsv,oracle-symlinks-check.tsv,oracle-run.json}` | — | oracle-arm output |
| `compare/K{1,2}-mine-vs-round38.json` | — | `equal: true`, `diff: {}` |
| `xpin/xpin.txt` | — | evidence-id recompute under rea-agents 6.5.0 (and 6.7.0) |
| `manifest/carriers-K1-K4.test.json` | — | manifest emitted from K1–K4 **test copies** (scratch-relative paths; not the frozen manifest) |
| `receipts/failure/` | — | exit-3 and provenance-guard receipts |

No tool was installed or upgraded for this item (nothing was missing). Versions actually used:
rea-agents **6.5.0** (npx cache `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`),
unblob **26.6.4** (`/home/vgpnk/.local/share/uv/tools/unblob/bin/unblob`, sha256 `0ce7b624…cba1d09`),
`sasquatch-v4be` **4.5.1** (`/home/vgpnk/.local/bin/sasquatch-v4be`, sha256 `fac88740…b7214c6`,
version line `unsquashfs version 4.5.1 (2022/03/17)`), node v24.21.0, python 3.14.8, jq 3.1.1 (jaq).

## 2. Interfaces

### 2.1 `c1-run.sh after CARRIER OUTDIR [SCRATCH]`

Runs, exactly:

```
cd $SCRATCH && REA_UNBLOB_COMMAND=<resolved unblob> \
  npx -y rea-agents@6.5.0 extract-firmware --format json --full-output <CARRIER> $SCRATCH/extract
```

* `--full-output` is **required**: without it the CLI prints the bare `data` object and the harness
  cannot tell `ok` from a failure document. The harness validates `{ok:true, data:{…}}` and writes
  the envelope's **`data` object** to `OUTDIR/after.json` (compact, one line, exactly what the
  counter parses; `data`, not the envelope).
* Extraction root is `$SCRATCH/extract` and is never pre-created (REA refuses an existing root —
  the round-38 harness bug documented in `R38ExecAfterK1/ENV-NOTE.md`). The whole scratch, REA
  staging included, is deleted on exit; `TMPDIR` points into it so `unblob.log` lands there.
* Preconditions checked before running (exit 2, no REA run): `npx`, `$REA_UNBLOB_COMMAND`
  (default `$HOME/.local/bin/unblob`) executable, **`sasquatch-v4be` resolvable on the inherited
  PATH** (an after-arm precondition, not silently added by the harness).
* **A non-default `SCRATCH` must contain a `/kaidoku-r39/` path segment**, because the receipt's
  hashed `parameters.output_directory` is what proves the extraction ran this round. The harness
  refuses (exit 2) any other scratch; `C1_ALLOW_FOREIGN_SCRATCH=1` downgrades that to a warning and
  records `run_provenance_segment_ok:false` for dev runs.
* `OUTDIR/run.json` records: `argv` (array + shell form), `cwd`, `extraction_root`, UTC
  `start_utc`/`end_utc` + `duration_ms`, `exit`, `rea{pin,version,package_root}`,
  `unblob{env_value,command_env,sha256,version}`, `sasquatch_v4be{path,sha256,version,version_line}`,
  `child_path`, carrier `{path,sha256,size_bytes}`, `envelope{parseable,ok,sha256,bytes}`,
  `data_extracted`, `receipt_written`, `receipt{path,sha256,bytes,evidence_id,engine,…}`,
  `previous_after_json_sha256`, `run_provenance_segment_ok`, `stderr_head`.
  The receipt summary also carries `handlers`, `files`, `published_bytes`, `gaps`, `gaps_detail`,
  `unpublished_entries`, `selection_sha256`, `subject_sha256` — the exact fields the counter grades.
* `C1_KEEP_ENVELOPE=1` additionally keeps `OUTDIR/after.envelope.json` (raw `{ok,data,meta}`).
* Never deletes an existing `OUTDIR/after.json`: on failure it leaves the old receipt in place and
  writes `receipt_written: false` plus `previous_after_json_sha256` (no silent stale receipt, no
  data loss).

### 2.2 `c1-run.sh oracle CARRIER OUTDIR [SCRATCH]`

Independent cross-tool extraction with `sasquatch-v4be -be -n -o <offset> -d $SCRATCH/root`, offset
auto-detected (`sqsh`/`hsqs` in the first 1 MiB; all four round-37 carriers are at 0), then a listing
computed by the harness itself (`lstat`, symlinks never followed):

* `OUTDIR/oracle-check.tsv` — `relpath TAB sha256 TAB size`, regular files, byte-sorted. **Grammar is
  byte-compatible with the frozen `oracle.tsv`**, so `diff`/`cmp` is the check.
* `OUTDIR/oracle-symlinks-check.tsv` — `relpath TAB target TAB in-tree|escaping`, POSIX join against
  the link's own directory with the extraction root as `/`; absolute targets are `escaping` (the same
  call as the round-39 counter's `resolve_kind`).
* `OUTDIR/oracle-run.json` — offset, sasquatch pin, start/end, exit, counts
  (`regular_files`, `symlinks_in_tree`, `symlinks_escaping`, `dangling_in_tree`), TSV digests.
* This arm never calls REA, so it is the **pre-freeze-safe** dev check for K5/K6 (claim: "dev checks
  by direct `sasquatch-v4be -be` only").

### 2.3 Exit codes

`0` ok · `2` usage/environment (bad args, missing carrier, no `npx`, unblob missing, `sasquatch-v4be`
not on PATH, no squashfs magic, …) · `3` tool failure (REA non-zero or `ok:false` → no receipt;
sasquatch non-zero in the oracle arm).

### 2.4 `mk-carriers.py` and the frozen manifest

```
python3 tools/round-39/mk-carriers.py --root "$PWD" --out .ufo/waves/round-39/c1/carriers.json \
  K1 corpus/evidence/round-37/c1/K1/carrier.sqsh corpus/evidence/round-37/c1/K1/oracle.tsv corpus/evidence/round-39/c1/K1/symlinks.tsv \
  K2 corpus/evidence/round-37/c1/K2/carrier.sqsh corpus/evidence/round-37/c1/K2/oracle.tsv corpus/evidence/round-39/c1/K2/symlinks.tsv \
  K3 corpus/evidence/round-37/c1/K3/carrier.bin  corpus/evidence/round-37/c1/K3/oracle.tsv corpus/evidence/round-39/c1/K3/symlinks.tsv \
  K4 corpus/evidence/round-37/c1/K4/carrier.bin  corpus/evidence/round-37/c1/K4/oracle.tsv corpus/evidence/round-39/c1/K4/symlinks.tsv \
  K5 corpus/evidence/round-39/c1/K5/carrier.sqsh corpus/evidence/round-39/c1/K5/oracle.tsv corpus/evidence/round-39/c1/K5/symlinks.tsv \
  K6 corpus/evidence/round-39/c1/K6/carrier.sqsh corpus/evidence/round-39/c1/K6/oracle.tsv corpus/evidence/round-39/c1/K6/symlinks.tsv
```

(or the same 4-tuples as TSV lines via `--spec FILE`, optional 5th column = `kind`). Emitted shape:

```json
{"claim":"R39-C1","schema":"kaidoku-r39-c1-carriers-v1","note":"…",
 "carriers":[{"id":"K1","path":"…","sha256":"…","size_bytes":9780,
              "oracle":"…","oracle_sha256":"…","oracle_files":5,
              "symlinks":"…","symlinks_sha256":"…","symlinks_in_tree":0,"symlinks_escaping":1,
              "receipt":"corpus/evidence/round-39/c1/K1/after.json"}, …]}
```

Validation (exit 2, nothing written): `--root` containment (no `..` escape, regular files only);
repo-relative normalised paths; **BE magic `sqsh` at offset 0** by default (`--endian le|any`);
unique ids, **contiguous `K1..KN`** (`--allow-gaps` to override); **unique carrier pins and paths**;
`oracle.tsv` = 3 fields, lowercase 64-hex digest, non-negative size, no duplicates/trailing slash;
`symlinks.tsv` = 3 fields, class exactly `in-tree|escaping`, no duplicates; **no path listed both as a
regular file and as a symlink** (neither kind is ever published, so that would be a freeze bug);
`receipt` is derived, never supplied. Output is byte-deterministic (no timestamps), so regeneration
diffs cleanly. Cross-checked against the counter seat's reader (`carriers_spec`, `frozen_drift`): it
needs `id,path,sha256,oracle,symlinks` (all present) and tolerates the extra provenance keys; the
`receipt` key it reads optionally is emitted with exactly its default value.

## 3. Test receipts (K1/K2 copies, never K5/K6)

Carriers copied from `corpus/evidence/round-37/c1/K{1,2}/carrier.sqsh` into scratch, sha256
re-verified identical to the pins (`1cfb6c33…6117e`, `403cb0a8…c99154`). The development scratch
shown below was deleted after the receipts were copied here (bounds); the paths recorded inside
`run.json` are therefore historical, exactly as in the committed round-38 receipts.

```
S=/fast/scratch/hyaku/kaidoku-r39/R39C1Harness; export HYAKU_SCRATCH=$S/hy
$A/c1-run.sh after  $S/carriers/K1/carrier.sqsh $S/out/K1          # exit 0, 3.5 s
$A/c1-run.sh after  $S/carriers/K2/carrier.sqsh $S/out/K2          # exit 0, 3.6 s
$A/c1-run.sh oracle $S/carriers/K1/carrier.sqsh $S/out/K1-oracle   # exit 0
$A/c1-run.sh oracle $S/carriers/K2/carrier.sqsh $S/out/K2-oracle   # exit 0
```

| carrier | handler(s) | failed chunks | files | published bytes | gaps | evidence id |
|---|---|---|---|---|---|---|
| K1 | `squashfs_v4_be` | none | 5 | 9 656 | 0 | `ev_a59bce78faae7b868249b9b188801c421554bfe2b55a7a60f99a6e5c74d4f59a` |
| K2 | `squashfs_v4_be` | none | 3 | 10 283 | 1 | `ev_8de5ad4965bc92c8e2ba2628a15dec759c5998b8d430200adefa5b302700993e` |

* **Semantic comparison with round-38** (`compare/K*-mine-vs-round38.json`): `equal: true`,
  `diff: {}`. Graded fields: `operation`, `provider_id`, `provider_version`, `subject_sha256`,
  `selection_sha256`, `handlers`, the full `(relative_path, sha256)` file set, the
  `(kind, relative_path, handler, dependencies)` gap multiset, `chunk_failed`. Byte-level
  differences are confined to the declared volatile fields (`output_directory`, file absolute
  paths, provider blob ids, `raw_result`, and therefore `evidence_id`).
* K2's single gap: `unpublished-entry` at `firmware.bin_extract/var/lib/run-link` (link target
  `../../a/run.sh`), `unpublished_entries` = the same symlink, and no published file ends with that
  path — exactly the draft rule. K1's `link-to-hello → ../hello.txt` sits at the image root and
  therefore resolves **above** it: `escaping`, removed, **0 gaps** — which is what round-38 measured
  and what the independent symlink seat's table (`…/R39C1SymlinkK1K4/symlinks-K1.tsv`) says.
* **Evidence id**: both receipts recompute to their stored id under the frozen
  `tools/round-27/xpin-attribute.mjs` rule with `--pkg65/--pkg67 = rea-agents 6.5.0`
  (`xpin/xpin.txt`, column 2 == column 3 == column 4, `both`). This is the counter's
  `evidence_id_ok` clause, verified before the counter exists.
* **Oracle arm**: `oracle-check.tsv` is **byte-identical** to the frozen oracle —
  sha256 `0c993e7421338a8c08e311914f71e0ebf9fda2849931b4f544e3774c78f13aab` (K1, 5 rows) and
  `6567cc50d9a1dea27609c0ae2b815229317e899eaba654edf6f0880e559cb921` (K2, 3 rows) — and the
  symlink check reproduces the classification (`link-to-hello … escaping`,
  `var/lib/run-link … in-tree`).
* **Run provenance** (counter clause `run_provenance_ok`): receipts carry
  `parameters.output_directory = …/kaidoku-r39/c1-run.XXXX/extract`, i.e. the `/kaidoku-r39/`
  segment — asserted per receipt in the selftest. A foreign `SCRATCH` is refused with exit 2
  (`receipts/failure/provenance-refused.txt`); with `C1_ALLOW_FOREIGN_SCRATCH=1` it runs and records
  `run_provenance_segment_ok:false` (`provenance-nosegment-run.json`).
* Robustness: relative `--out` under `--root`, manifest overwrite, carrier/OUTDIR paths containing
  spaces (oracle TSV still byte-identical), scratch removed on every exit path
  (`ls -A $HYAKU_SCRATCH/kaidoku-r39` empty after each run).

## 4. Selftest (`selftest.sh`, 68 cases, 68 green, 45.4 s)

Groups (full case list in `selftest-tally.json`):

* **mk-carriers (16)**: 4-carrier green + byte-identical regeneration + `--spec` TSV + kind column;
  manifest grammar (required keys, derived `receipt`, repo-relative paths); pins equal the round-37
  pins; red: LE magic, id gap, duplicate id, duplicate pin/path, oracle/symlink path clash, bad
  sha, 2-column oracle, bad symlink class, missing carrier, path escaping `--root`, no carriers;
  `--endian any` and `--allow-gaps` accepted.
* **after arm (13)**: K1/K2 exit 0; handler, receipt, pin (selection == subject == carrier sha),
  file/gap counts, toolchain pins (6.5.0 / 26.6.4 / 4.5.1 / unblob sha), UTC timestamp shape,
  oracle publication (every `oracle.tsv` row published with suffix+sha), run-provenance segment,
  scratch removal, semantic equality with round-38; keep-envelope; rerun bookkeeping.
* **oracle arm (13)**: K1/K2 exit 0, TSV byte-identical to the frozen oracle, symlink tables, counts.
* **error paths (15)**: no args / bad mode / two args → 2; missing carrier → 2; no squashfs magic →
  2; truncated carrier → 3 (+ `oracle-run.json` records `counts.regular_files == 0`); PATH with
  `~/.local/bin` stripped → 2; `REA_UNBLOB_COMMAND` missing → 2; REA failure (`/bin/false` as
  unblob) → 3 with `receipt_written: false` and **no** `after.json` written; foreign scratch → 2,
  and → 0 with `C1_ALLOW_FOREIGN_SCRATCH=1` recording `run_provenance_segment_ok:false`, scratch
  removed either way.

## 5. Integration notes and risks for the L1

1. **Copy `c1-run.sh` to `tools/round-39/c1-run.sh` before the freeze.** The counter's freeze-drift
   list (`FROZEN_PATHS`) includes that path; landing it later exits 2 `frozen_path_changed`.
2. **Run the after arm with no explicit `SCRATCH`** (or one whose path contains `/kaidoku-r39/`).
   The receipt's `parameters.output_directory` is hashed into `evidence_id` and must carry that
   segment for the counter's `run_provenance_ok` clause; a foreign scratch path cannot be fixed
   afterwards without re-running REA and re-minting the id — hence the hard refusal by default.
   Cross-checked against the counter seat's three constraints (in-flight message): (i) outdir under
   the round-39 scratch segment, (ii) bare `data` object at `corpus/evidence/round-39/c1/<id>/after.json`
   first added strictly after the freeze, (iii) entries carrying `id/path/sha256/oracle/symlinks`
   (plus the derived `receipt`), ids exactly K1..K6, six distinct pins. All three hold by
   construction here.
3. **The after arm needs `sasquatch-v4be` on the inherited PATH.** If the L1's shell lacks
   `~/.local/bin` (the round-38 discovery), the harness exits 2 before calling REA — that is the
   intended fail-fast, not a regression.
4. **K5/K6 discipline**: run only `c1-run.sh oracle` on K5/K6 before the freeze (sasquatch only, no
   REA). The after receipts for all six carriers must be produced *after* the freeze (the counter's
   `receipt_fresh` clause requires first-add to be a strict descendant of `--freeze`).
   Sequencing that satisfies every binding at once: commit carriers + oracles + symlink tables +
   `carriers.json` + `tools/round-39/c1-run.sh` (+ counter, claims, docs) in the **freeze** commit;
   run the six after arms against those committed bytes; commit the six receipts afterwards. Each
   carrier must be committed **before** its receipt (the counter also checks sha256 of the git bytes
   at REV against the pin), and re-running the generator into a frozen carrier path after the freeze
   exits 2 `frozen_path_changed` — even if the bytes would come out identical.
5. **Expected gap cardinality for the frozen set** (from the rule + the symlink seat's tables):
   K1 → 0 gaps (its only link escapes), K2 → 1, K3/K4 → 0, K5 → 2 (two in-tree + one escaping),
   K6 → per its table. A receipt with a gap on K1's escaping link, or a published path at an
   escaping-symlink path, is a defect; a "materialised symlink" receipt is a control, not a pass.
6. **`mk-carriers.py` is strict on purpose**: it refuses a non-BE/`hsqs` carrier, a non-contiguous
   `K1..KN` id run, a duplicated pin/path, and any path collision between `oracle.tsv` and
   `symlinks.tsv`. If K5/K6 land with a different id spelling or an LE image, generation fails
   loudly at freeze time instead of producing an uncountable manifest. (Test-only K3/K4 symlink
   tables in the selftest are empty placeholders; the frozen ones come from `R39C1SymlinkK1K4`.)
7. **Do not commit `run.json` into `corpus/evidence/round-39/c1/<K>/`** unless intended: it records
   scratch paths (`cwd`, `extraction_root`, `child_path`) that are removed by design. It is a run
   log; the receipt the counter reads is `after.json`. (Committed run logs are harmless to the
   counter — it reads only `after.json` — but they are not evidence of lane state.)
8. The harness is mechanical: it does not grade the predicate. Subject/selection pins are recorded,
   not enforced, so a wrong-pin receipt is left for the counter (and its controls) to catch.
9. The oracle arm is independent of REA and of the independent parser, but it *is* sasquatch, i.e.
   the same extractor unblob shells out to. Treat `oracle-check.tsv` as a third-tool cross-check of
   the frozen tables; the parser-independent oracle is `R39C1IndepReader/sqfs-list.py`.

## 6. Limits of the evidence here

* `after.json` was produced from **scratch copies** of the round-37 carriers (same bytes, pins
  re-verified) — these are development receipts, not the round-39 committed receipts.
* `run.json`/`oracle-run.json` reference scratch paths that no longer exist; that is by design
  (scratch is removed) and mirrors the round-38 receipt convention.
* jq on this host is **jaq 3.1.1**; the scripts use only standard filters (`//`, `select`, `unique`,
  `endswith`, `test`, `any/all`, `--rawfile`, `--argjson`). [INFERENCE] real jq ≥1.6 behaves
  identically; this was not exercised.
* No REA run touched K5/K6, no held-out C2 carrier was built or run, and nothing in `corpus/`,
  `tools/`, `plans/` or the lane root was modified (`git status --porcelain` in the lane shows only
  the untracked `.ufo/waves/round-39/` tree and the L1's `plans/round-39-claims.md`).
* The interface was cross-checked twice: against the counter seat's draft source (its
  `carriers_spec`, `frozen_drift`, `gaps_ok`, `resolve_kind`, `run_provenance_ok` readers) and
  against the seat's own confirmation message — no divergence found.

Report: `.ufo/waves/round-39/w1/R39C1Harness.md`
