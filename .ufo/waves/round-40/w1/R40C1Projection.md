# R40C1Projection — rerun-binding semantic projection for R40-C1 (routed R39-CL5)

**Verdict: DEFECTS FOUND.** The rerun hypothesis is **CONFIRMED** — three runs per carrier in
three independent scratch roots (five carriers, plus a fourth root with a renamed input) give one
projection, zero semantic drift, and the committed round-39 receipts project identically. But the
*six-field projection named in the R40-C1 draft is oracle-closed*: an oracle-only fabrication that
never runs REA/unblob/sasquatch **passes it on all five carriers** (K1, K2, K4, K5, K6) while also
passing every non-rerun R39-C1 clause with a validly re-minted `evidence_id`. Adding the run's own
content fingerprints — `files[].mime_type` + `files[].md5` + `files[].sha1` from `raw_result` —
refuses the same fabrication on **5/5** carriers and stays invariant over 16/16 matrix runs
(renamed-input probe included) and the 5 committed receipts.
A second, separate limit is measured: a byte copy of a round-39 receipt *is* projection-identical
to a fresh run, so the rerun binding cannot kill the draft's "round-39 receipts copied" control.

Seat `R40C1Projection` (executor, leaf). Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`,
base `fa6a8a3f85ec65946b3a54d37c0ddd1d6748664f`. Nothing frozen, nothing committed: the L1
integrates. All writes are in
`.ufo/waves/round-40/w1/artifacts/R40C1Projection/` and this report. Scratch
`/fast/scratch/hyaku/kaidoku-r40/R40C1Projection` was removed after the artifacts were written.

Cross-domain evidence encountered: none. No R40-C2 path (`SKILL.md`, its interpreter/generator,
C2 held-out data) was read; the two claims stay separable.

## Axes named (Godspeed)

| axis | what this seat moves |
|---|---|
| **depth** | an executable rule the corpus does not hold: *a projection is only a binding if at least one of its fields is not derivable from the frozen inputs* — measured by building the strongest fabrication the frozen inputs allow and testing each candidate field. |
| **coverage** | 17 REA invocations (5 carriers × 3 scratch roots + 1 fourth root with a renamed input + 1 PATH-starved probe), 3 fabrication strengths × 4 projection profiles × 5 carriers, 2 failure shapes. |
| **calibration** | the six named fields are exactly the six a fabricator can compute from `carriers.json` + `oracle.tsv` + `symlinks.tsv`; that is not an accident of the phrasing, it is the whole content of the finding. |

## 1. Hypothesis, operationalised

Hypothesis (falsifiable, from the task): *two REA 6.5.0 `extract-firmware` runs of the same carrier
into different scratch output directories yield identical semantic projections*, where the
projection is

| field | definition used (`projection.py`, profile `core`) |
|---|---|
| `subject_sha256` | `subject.digest.sha256` |
| `files` | sorted `[suffix, sha256, size]` over `normalized_result.files` |
| `chunks` | sorted `[handler, start, end, extraction_failed]` |
| `extraction_gaps` | sorted `[kind, suffix, sorted(suffix(dependencies))]` |
| `unpublished_entries` | sorted `[kind, suffix]` |
| `diagnostics` | sorted multiset of `diagnostics[*].report.__typename__` |

`suffix` = the path after the first path component ending in `_extract` (the chunk extract
directory), after removing a leading `$output/`. `firmware.bin_extract/usr/x` → `usr/x`. A nested
extraction keeps its inner `*_extract` component (selftest `nested-extract-visible`), so the rule
does not silently flatten depth.

Three further profiles exist **only** because the core result below is negative; they are
measurements for the freeze decision, not the default:

| profile | adds |
|---|---|
| `plus-mime` | `files[].mime_type` (libmagic via unblob — absent from the oracle) |
| `plus-content` | `plus-mime` + `files[].md5`, `files[].sha1` (joined from `raw_result.report[*]` `HashReport` by the task path — the oracle publishes **sha256 only**) |
| `plus-extractor` | `plus-content` + ordered derivation edges + engine name/version + `published_bytes` + `coverage` |

## 2. Bounds compliance (what did *not* run)

- No REA/unblob on V1, the second vendor member, or any round-40 carrier (V1/L1/L2, the AVM-BE
  member). No C2 held-out carrier was built or run. REA ran **only** on byte-copies of the round-39
  development carriers K1/K2/K4/K5/K6, each copy pin-checked inside the driver before the run.
- No install, upgrade, `pacman` transaction, host service, VCS mutation, or write outside the two
  allowed trees. No subagents, no background jobs, no `agent://all`.
- REA only via the CLI with `REA_UNBLOB_COMMAND` absolute and cwd inside scratch (so
  `unblob.log` never lands in the lane); every run into a fresh, non-existent output directory.
- Tools of record: REA `rea-agents@6.5.0` (`/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`,
  `package.json` version 6.5.0), unblob 26.6.4 (`0ce7b624…`), `sasquatch-v4be` 4.5.1 reachable on
  the child PATH (`/home/vgpnk/.local/bin`).

## 3. Run matrix — 5 carriers, 3 scratch roots (+2 probes), 17/17 exit 0

`run-matrix.sh` gives each (carrier, run) its own directory under its own root **and its own
`TMPDIR`**, so the REA temp dir (`rea-firmware-XXXXXX`), the output directory, the input path and
the cwd all differ between runs. Full records (paths, exits, durations, envelope and receipt
sizes/sha256) are in `run-matrix.tsv`; one row per run:

| carrier | runs | roots / TMPDIRs | exit | duration ms | envelope bytes (identical per carrier) | envelope sha256 (differs) | receipt bytes |
|---|---|---|---|---|---|---|---|
| K1 | r1,r2,r3 | r1/r2/r3, each `tmp/` | 0/0/0 | 3530/3378/3674 | 19484 | 3 distinct | 24551 |
| K2 | r1,r2,r3 | same | 0/0/0 | 4213/3755/4845 | 17448 | 3 distinct | 21816 |
| K4 | r1,r2,r3 | same | 0/0/0 | 5868/3503/4105 | 13307 | 3 distinct | 16619 |
| K5 | r1,r2,r3,r4 | r1/r2/r3 + r4 (`r40-probe.bin`) | 0/0/0/0 | 4868/3633/3630/2267 | 35588 (r4 35591) | 4 distinct | 44463 (r4 44466) |
| K6 | r1,r2,r3 | r1/r2/r3 | 0/0/0 | 3750/3616/3551 | 30147 | 3 distinct | 37823 |

Runs r1–r3 per carrier ran **concurrently**; K5 r4 ran after the barrier. Same projection either
way. K5 r4 is the renamed-input probe (`r40-probe.bin` instead of `carrier.sqsh`): `subject.name`
changes, the projection does not — so the counter's fresh run may use any temp basename.

Seventeen invocations were made in total: the 16 matrix runs, plus
`receipts/K5-pathstarved.json` from a K5 run with `$HOME/.local/bin` stripped from the **child**
PATH (REA exit 0, envelope `ok:true`, but `chunks[0].extraction_failed=true`, 0 files, gap
`missing-extractor-dependency` with `relative_path: null`, diagnostic
`ExtractorDependencyNotFoundReport`). That probe measures the PATH precondition and forces the
projection to be total over failure shapes (see §6.4).

## 4. Invariance and drift

`analyze.py` (`analysis.json`):

| carrier | fresh-vs-fresh, all profiles | fresh-vs-committed (`corpus/evidence/round-39/c1/K*/after.json`) | core projection sha256 | plus-content projection sha256 |
|---|---|---|---|---|
| K1 | **identical** (r1=r2=r3) | **equal at core, plus-mime, plus-content, plus-extractor** | `d0d055c6b11fd448…` | `9650603b6d812902…` |
| K2 | **identical** | **equal (all 4)** | `97d070299541e208…` | `884e5f6001ced825…` |
| K4 | **identical** | **equal (all 4)** | `fe8db349fd5c3b18…` | `1a33738c8706b915…` |
| K5 | **identical** (r1=r2=r3=r4) | **equal (all 4)** | `032057e89ceb6374…` | `a288b5c4db17b2d8…` |
| K6 | **identical** | **equal (all 4)** | `1ee9c7125976a176…` | `c4f77aff7621875a…` |

So the semantic projection is reproducible across scratch roots, TMPDIRs, concurrency, input
basename, and against receipts produced hours earlier in a different scratch segment
(`/kaidoku-r39/…` vs `/kaidoku-r40/…`).

Content, not just listing: on the live extractions, every published file rehashes to
`files[].sha256` (K5 r1 10/10, K4 r1 4/4) and to the `raw_result` `HashReport` `md5`/`sha1`
(K5 10/10, K4 4/4). Cross-carrier discrimination is non-vacuous:
`projection.py compare receipts/K5-r1.json receipts/K6-r1.json` → exit 3, differing fields
`chunks, diagnostics, extraction_gaps, files, subject_sha256, unpublished_entries`.

## 5. Everything that varies run to run (must be excluded) — measured, not assumed

Exact structural diff of run 1 against every other run and against the committed receipt
(`analysis.json` → `structural_diff_vs_run1`): K1 82 differing leaves, K2 76, K4 47 (48 vs
committed), K5 165 (166 for the renamed probe), K6 143. **Semantic differing leaves: 0 in every
pair.** The collapsed inventory (19 distinct paths, all run-identity) is:

| class | paths | example (K5) |
|---|---|---|
| scratch path | `parameters.path`, `parameters.output_directory`, `normalized_result.output_directory`, `normalized_result.files[].path`, `raw_result.report[].task.path`, `raw_result.report[].reports[].path`, `raw_result.report[].subtasks[].path`, `subject.local_path` | `/fast/scratch/hyaku/kaidoku-r39/l1/c1runs/K5-scratch/extract` → `/fast/scratch/hyaku/kaidoku-r40/R40C1Projection/r1/K5/extract-K5-r1` |
| scratch path, embedded | `raw_result.execution.args[]`, `normalized_result.diagnostics[].report.link`, `.target`, `raw_result.report[].reports[].link`, `.target` | `…/rea-firmware-8WPLS1/extracted/firmware.bin_extract/usr/share/demo/escape` |
| pid-derived blob id (`f"{os.getpid()}:{n}"`) | `normalized_result.chunks[].provider_id`, `normalized_result.derivations[].provider_blob_id`, `raw_result.report[].task.blob_id`, `raw_result.report[].subtasks[].blob_id`, `raw_result.report[].reports[].id` | `3028394:1` → `398770:1` |
| receipt id | `evidence_id` | `ev_b69020cd…` → `ev_25f6743e…` |
| input basename (probe only) | `subject.name` | `carrier.sqsh` → `r40-probe.bin` |

Two facts this measurement settles, which the draft leaves implicit:

1. **The receipt body carries no wall-clock field.** There is no timestamp anywhere in
   `evidence.data`; the only time value is the envelope wrapper's `meta.duration`
   (e.g. `1955ms` vs `2242ms`), which is outside the receipt the counter hashes. So the exclusion
   list is "paths, pid ids, evidence id, name" — timestamps only matter if the counter compares
   whole envelopes.
2. **The whole `raw_result` layer except paths/pids is semantically invariant**, including
   `execution.stdout.text` (the unblob banner), `execution.stderr` (0 bytes),
   `execution.exit_code`, and every `reports[].magic/mime_type/md5/sha1/sha256/size`. That is what
   makes `plus-content` a legal (invariant) field, not a guess: 16/16 matrix runs and 5/5 committed
   receipts agree at that profile (§4).

## 6. Fabrication: does the projection refuse it?

### 6.1 Construction (oracle-only, no carrier byte read)

`fabricate-oracle-only.py` opens **only** `carriers.json`, `oracle.tsv`, `symlinks.tsv` per carrier
(closure recorded in `fabricated-<mode>/manifest.json`: `carrier_bytes_read: 0`,
`processes_started: []`). Three strengths, each for K1/K2/K4/K5/K6:

- **min** — files/gaps/unpublished/chunks/subject from the metadata; no diagnostics, no
  derivations, no engine, extension-guessed mime.
- **full** — the R39 `CTL-C1-3` shape: `min` + `MaliciousSymlinkRemoved` diagnostics inferred from
  the escaping rows + a full directory-edge derivation tree + engine copied as a host constant +
  derived `coverage`/`published_bytes`; `evidence_id` re-minted with `tools/round-27/xpin-attribute.mjs`
  (the frozen 6.5.0 rule). Stored id == recomputed id on all five
  (`ev_6f9c4cd4…`, `ev_6737ae97…`, `ev_27aefd54…`, `ev_e4b61348…`, `ev_b9dc6cb4…`).
- **full2** — `full` with the derivation tree restricted to published files and in-tree link paths
  (a forger who has read `R39W2C1Fabricate.md` and knows REA emits no derivation for the link it
  removed).

The fabricated `output_directory` values do not exist on disk (`ls -d …/fab-full2/K5-after` →
ENOENT), exactly like the round-39 control.

Every non-rerun R39-C1 clause passes on `full2` (`mirror-r39-clauses.py`, a re-implementation of
`tools/round-39/c1-counter.py`'s helpers):

| carrier | subject | operation | handler | chunks | oracle | gaps | escaping | ALL |
|---|---|---|---|---|---|---|---|---|
| K1 | ok | ok | ok | ok | 5/5 | ok | ok | **PASS** |
| K2 | ok | ok | ok | ok | 3/3 | ok | ok | **PASS** |
| K4 | ok | ok | ok | ok | 4/4 | ok | ok | **PASS** |
| K5 | ok | ok | ok | ok | 10/10 | ok | ok | **PASS** |
| K6 | ok | ok | ok | ok | 8/8 | ok | ok | **PASS** |

So the rerun-binding clause is the **only** clause that could refuse this fabrication.

### 6.2 Result — the projection as drafted does not refuse it

`fabrication-check.py` (exit 1 by design: `all_fabrications_refused_core: false`):

| carrier | mode | core (draft six fields) | plus-mime | plus-content | plus-extractor |
|---|---|---|---|---|---|
| K1 | min | **REFUSED** `diagnostics` | REFUSED `diagnostics,files` | REFUSED `diagnostics,files` | REFUSED 6 fields |
| K1 | full / full2 | **ACCEPTED** | REFUSED `files` | REFUSED `files` | REFUSED `files` (`full` also `derivations`) |
| K2 | min | **ACCEPTED** | REFUSED `files` | REFUSED `files` | REFUSED 5 fields |
| K2 | full / full2 | **ACCEPTED** | REFUSED `files` | REFUSED `files` | REFUSED `files,derivations` |
| K4 | min / full / full2 | **ACCEPTED** | **ACCEPTED** | REFUSED `files` | REFUSED `files` (`min` also 4 more) |
| K5 | min | **REFUSED** `diagnostics` | REFUSED `diagnostics,files` | REFUSED `diagnostics,files` | REFUSED 6 fields |
| K5 | full / full2 | **ACCEPTED** | REFUSED `files` | REFUSED `files` | REFUSED `files` (`full` also `derivations`) |
| K6 | min | **REFUSED** `diagnostics` | REFUSED `diagnostics,files` | REFUSED `diagnostics,files` | REFUSED 6 fields |
| K6 | full / full2 | **ACCEPTED** | REFUSED `files` | REFUSED `files` | REFUSED `files` (`full` also `derivations`) |

Reading the table:

- **The `full`/`full2` fabrication is accepted by `core` on 5/5 carriers.** Which field differences
  are *impossible* for it? None: `min` is caught only on the four carriers that happen to have an
  escaping link (`diagnostics`), and K4 — no symlinks at all — is accepted even by `min`.
- `plus-mime` refuses 4/5 at `files` (`mime_type`) but **accepts K4**, whose four files are plain
  ASCII text and therefore extension-guessable. mime alone is not a binding.
- `plus-content` refuses **5/5 at `files`**, including K4, where the only difference is
  `md5`/`sha1` being absent in the fabrication:
  `["apple1.txt","6181259c…",7,"text/plain",null,null]` vs
  `[…,7,"text/plain","0674b58408c005869019548da6eaf1b8","ab450dfe5d73877069fa8f3f2696db22cc41c932"]`.
- Where mime does discriminate (measured, real libmagic values vs the extension guess):
  K1 `bin/run` `text/x-shellscript` (guess `application/octet-stream`), `empty` `inode/x-empty`;
  K2 `var/lib/data.bin` **`image/x-tga`** (guess `application/octet-stream`);
  K5 `config/app.conf` `text/plain`, `empty.flag` `inode/x-empty`,
  `usr/share/demo/assets/manifest.json` **`application/json`**, `var/log/last.log` `text/plain`;
  K6 `etc/config.ini`, `var/log/app.log`, `var/log/repeat.log` `text/plain`.
- `plus-extractor` against `full` additionally catches a wrong *derivation* choice (the escaping
  link as a tree child) — inferable-but-wrong structure. Against `full2` it matches `plus-content`
  everywhere **except K2**, where `derivations` refuses on its own: the real run carries two
  directory edges my file-path reconstruction cannot state, `a → a/b` and `a/b → a/b/c`, because
  **`a/b` and `a/b/c` are empty directories** — the oracle lists regular files only, so an empty
  directory is not derivable from any frozen table. That is a genuine (if carrier-dependent)
  oracle-blind structural channel; it does not exist on K1/K4/K5/K6, whose directory tree is
  exactly the set of file parents.

### 6.3 Why — the six named fields are exactly the oracle's span

Every core field is a function of frozen inputs:

| core field | frozen input that determines it |
|---|---|
| `subject_sha256` | `carriers.json` pin |
| `files[suffix, sha256, size]` | `oracle.tsv` |
| `chunks[handler, 0, size, false]` | the handler name (round-39 constant) + `size_bytes`; every carrier's chunk is `0..size` |
| `extraction_gaps[kind, suffix, deps]` | `symlinks.tsv` in-tree rows (`kind` = `unpublished-entry`, `deps` = `[]`) |
| `unpublished_entries[kind, suffix]` | `symlinks.tsv` in-tree rows (`kind` = `symlink`) |
| `diagnostics` multiset | `symlinks.tsv` escaping rows (`MaliciousSymlinkRemoved`, one per row) |

The two fields the draft does *not* name behave differently, which is why they were measured:
`mime_type` and the `md5`/`sha1` pair are content-determined and absent from every frozen table;
the `derivations` edge set is nearly derivable (file paths + in-tree links) but empty directories
are not (§6.2, K2).

The projection is therefore **oracle-closed**: it adds no discrimination over the oracle clauses
the counter already re-derives (`oracle_hits`, `gaps_ok`, `escaping_ok`). That is exactly the
R39-CL5 failure mode re-expressed: the draft says a re-minted fabricated receipt "must now fail the
rerun binding", and with these six fields it does not.

### 6.4 Projection totalness (a real bug the failure probes found)

`missing-extractor-dependency` gaps carry `relative_path: null` (K5 PATH-starved run). A projection
that raises on a null path would make the counter crash instead of refusing. `projection.py` now
preserves `null` and is covered by selftest `null-gap-path-total`. The PATH-starved receipt is
refused at core on 5 fields (`chunks` `[...,false]`→`[...,true]`, `files`, `extraction_gaps`,
`unpublished_entries`, `diagnostics`), which is the measurement that the projection binds the
`sasquatch-v4be`-on-PATH precondition of the predicate.

## 7. Findings for the freeze

**P1 (blocking, R40-C1).** The draft's six-field projection is oracle-closed (§6.2–6.3): a receipt
fabricated from the frozen metadata with a re-minted evidence id is accepted on 5/5 carriers, so
the clause "a receipt not produced by a run of the pinned carrier cannot match" is **false as
drafted**. Recommended freeze wording — add the run's content fingerprints to the projection:

```
projection v1 =  subject_sha256
              + files: sorted [suffix, sha256, size, mime_type, md5, sha1]
              + chunks: sorted [handler, start, end, extraction_failed]
              + extraction_gaps: sorted [kind, suffix, sorted(dependency suffixes)]
              + unpublished_entries: sorted [kind, suffix]
              + diagnostics: sorted multiset of report __typename__
   where md5/sha1 come from raw_result.report[*].reports[HashReport] joined by
   task.path -> suffix, and mime_type from normalized_result.files[*].mime_type
```

Measured properties of that v1: invariant on 16/16 matrix runs and 5/5 committed receipts (§4); refuses
the oracle-only fabrication 5/5 (§6.2); computable on both sides of the comparison (every committed
round-39 receipt carries exactly one `HashReport` per published file: K1 6, K2 4, K4 5, K5 11,
K6 9 = files + input).

**P2 (blocking, R40-C1 kill-control list).** A **byte copy of a real round-39 receipt projects
identically to a fresh run** (`fresh_vs_committed equal=True` at every profile, all five carriers).
The rerun binding therefore cannot kill the draft's "round-39 receipts copied" control; only a
round-scoped clause can (e.g. `parameters.output_directory` must name this round's scratch
segment). State that in the claim, and note that an edited+re-minted copy is indistinguishable from
an oracle fabrication — the same P1 boundary.

**P3 (residual limit, must be disclosed).** With `plus-content`, matching requires *the extracted
bytes*: `md5`/`sha1` are not invertible from the oracle's `sha256`, and unexpected libmagic values
(`image/x-tga`, `application/json`, `inode/x-empty`) are not inferable from a path. But anyone who
extracts the carrier — with sasquatch directly rather than REA — can produce the same projection.
So the honest predicate is: *the receipt equals what an extraction of the pinned carrier publishes*;
authorship ("REA produced it") is not locally provable, exactly as R39W2C1Fabricate §3 concluded
for the receipt as a whole.

**P4 (precision, optional).** `diagnostics` as a bare `__typename__` multiset loses *which* link
was removed: K6 has two escaping links and the projection sees only `[MSR, MSR]`. The link suffixes
are invariant (`rel_suffix(diagnostics[*].report.link)`; they contain the `*_extract` component) and
would make the field exact — but they are also derivable from `symlinks.tsv`, so this buys precision,
not resistance. Freeze only if the extra strictness is wanted.

**P5 (craft).** The projection must be total: `relative_path: null` occurs in real REA output
(§6.4). Any frozen implementation needs that case plus a selftest for it.

**P6 (freeze mechanics).** Give the counter the same frozen projection tool and compare
`committed evidence.data` against its own fresh run's `evidence.data` with
`projection.py compare A B --profile plus-content` (exit 0 equal / 3 differ / 2 bad input), and
record that exit code in the score receipt (R39-CL6). The counter must compute both sides itself;
comparing a committed projection to another committed projection would re-open the same hole.

## 8. Deliverables (all in `.ufo/waves/round-40/w1/artifacts/R40C1Projection/`)

| file | sha256 | what it is |
|---|---|---|
| `projection.py` | `48929bda5790b6c9b3f1aa306a9ca11a1914b71cb4012d5bc424e3f0533a045b` | pure-stdlib projection + `compare` + `--selftest` (24 cases, 0 fail, `selftest.txt`) |
| `analyze.py` | `d1f56175d774071e6f6ed711de640b1b9e4b264fb50fdb9b3f72770a7cab4b3d` | invariance, drift, exact field variance → `analysis.json`, `field-variance.tsv` |
| `fabricate-oracle-only.py` | `9667c18ea3aab7ce0fffe6e1e6a4bb8f5ab66ea97553f83b17b7039919e6ddbe` | oracle-only receipt builder, modes `min/full/full2`, xpin re-mint |
| `fabrication-check.py` | `3865e707042c1f844ede584238831aed23577f12522001e7f8bde45600d4edae` | the acceptance/refusal matrix |
| `mirror-r39-clauses.py` | `f4ad794d193d307c2309672ffa096bda652b5ab7b36598cc820aec36eab9b44f` | non-rerun R39-C1 clauses on the fabrication |
| `run-matrix.sh` | `474b96e1649b28b85fc9fb6f4d2692f6c5826d07f33d78de329f4311549164ce` | 16-run matrix driver (honours TMPDIR, no `/tmp` literals) |
| `run-matrix.tsv` | — | one row per invocation |
| `receipts/` | — | 16 fresh matrix `evidence.data` documents + `K5-pathstarved.json` |
| `logs/` | — | 17 envelopes and 17 stderr captures (all stderr 0 bytes) |
| `fabricated-{min,full,full2}/` | — | 5 receipts each + `manifest.json` (input closure, ids) |
| `analysis.json`, `field-variance.tsv` | — | §4/§5 data |
| `fabrication-check.json`, `mirror-r39-clauses.json` | — | §6 data |
| `selftest.txt`, `commands.txt` | — | selftest transcript; exact commands, exits, pins |

Rebuild in one pass (scratch `S=/fast/scratch/hyaku/kaidoku-r40/R40C1Projection`):

```
bash $A/run-matrix.sh $LANE $S $A
python3 -I -B $A/analyze.py --artifacts $A --lane $LANE --json-out $A/analysis.json --tsv-out $A/field-variance.tsv
for m in min full full2; do python3 -I -B $A/fabricate-oracle-only.py \
  --manifest $LANE/.ufo/waves/round-39/c1/carriers.json --lane-root $LANE --mode $m \
  --out $A/fabricated-$m --only K1,K2,K4,K5,K6 --outdir-base $S/fab-$m \
  --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents; done
python3 -I -B $A/fabrication-check.py --artifacts $A --json-out $A/fabrication-check.json   # exit 1 = finding
```

## 9. Risks and blockers

- The recommendation is measured on five standard-BE carriers. The round-40 AVM carriers (V1,
  L1/L2) were **not** run (bounds) and are, by hypothesis, exactly the shape where the projection
  matters most. Expectation to be checked after the freeze, on development inputs only: the AVM
  layout changes extraction *content*, not the projection machinery; the six core fields remain
  oracle-derived, so P1 applies a fortiori. [INFERENCE, grounded on §6.3: those six fields are
  functions of the same frozen tables.]
- `plus-content` inherits two environment pins: libmagic's database (through `mime_type`) and
  unblob 26.6.4's `raw_result` shape. Both are already pinned by the predicate; if the counter's
  fresh run uses a different libmagic build, `mime_type` could differ legitimately. The `md5`/`sha1`
  pair is content-only and carries the load-bearing discrimination.
- No blocker: every input needed for this seat was reachable. Nothing here depends on V1 data.
