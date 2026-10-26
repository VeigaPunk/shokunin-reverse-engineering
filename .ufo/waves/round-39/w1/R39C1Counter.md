# R39C1Counter — `c1-counter.py` for P39-C1 (pre-freeze build)

**VERDICT: DONE.** The counter is written, its 33-case selftest passes with every red case failing
on exactly the clause it targets (verified clause-by-clause, not just by exit code), and it was run
against the **real** committed K1–K4 carriers, oracles and round-38 receipts in a scratch git repo.
Three clauses beyond the draft sentence are required for the predicate to be non-vacuous and
copy-proof; their exact sentences are in §2 for the L1 to paste into `plans/round-39-claims.md`
before the freeze (already messaged to `KaidokuR39`, `R39C1AxisFit` and `R39C1Harness`).

Seat `R39C1Counter` (leaf). Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, base
`a2f64e1da78afcf8cc39287106604dbcc270844c`. No lane file outside my artifact dir and this report was
written; no VCS mutation; no REA run on K5/K6 or on any held-out carrier; no held-out carrier built.
Tools installed or upgraded: **none** (python 3.14 stdlib, `git`, `node` with the already-pinned
`rea-agents@6.5.0` npx cache, `tools/round-27/xpin-attribute.mjs`).

## 1. Deliverables

All under `.ufo/waves/round-39/w1/artifacts/R39C1Counter/`:

| path | what it is |
|---|---|
| `c1-counter.py` | the counter (43,128 B). → copy to `tools/round-39/c1-counter.py` |
| `selftest/dev-after.json`, `selftest/dev-oracle.tsv`, `selftest/dev-symlinks.tsv` | dev fixture: the committed round-38 K2 `after.json` transformed to two in-tree gaps + one escaping row; the committed K2 `oracle.tsv`; the symlink table |
| `selftest/r38-k2-after.json` | the committed round-38 K2 receipt, byte-identical, used by the two copy controls |
| `selftest-output.json`, `selftest-time.txt` | clean selftest run and its wall/user/sys |
| `selftest-detail.txt` | `C1_SELFTEST_DETAIL=1` run: per case the exit code, carriers matched, the exact failing clause keys and the false bindings (this is the discrimination evidence in §4) |
| `sim-real-copy.py`, `sim-round38-copy.json`, `sim-real-copy.out` | the real-receipt integration check of §5 (rebuildable: rebuilds its scratch repo, never writes the lane) |
| `base-rev.json` | the counter at the base revision (§6) |

Deployment is `tools/round-39/c1-counter.py` **plus** `tools/round-39/selftest/` (the selftest reads
`selftest/dev-*`, `selftest/r38-k2-after.json` and locates `../round-27/xpin-attribute.mjs`).
Verified in that exact layout: `cd <repo>/tools/round-39 && python3 -I -B c1-counter.py --selftest
--pkg65 …` → `33 cases, green_ok 1, red_ok 32, exit 0`.

## 2. Freeze-time decisions — three sentences the draft does not yet carry

The counter is stricter than the current draft sentence in three places. All three are properties of
frozen data or of a hashed field, so they cannot false-fail an honest run; all three are needed to
refuse a control. Paste them (or tell me to drop them) so predicate and counter freeze identical.

| # | clause | sentence to add to P39-C1 | why it is required (measured) |
|---|---|---|---|
| a | `run_provenance_ok` (per carrier) | “and its `parameters.output_directory` is an absolute path inside this round's scratch segment `/kaidoku-r39/` with no `..` segment” | §5: byte-copied round-38 receipts on the real K1–K4 carriers satisfy **every other** clause (oracle hits 5/5, 3/3, 4/4, 4/4; K2's gap; ids recompute). With genuine K5/K6 receipts they would reach 6/6. `parameters` is in the hashed 6.5.0 projection, so the field cannot be edited without breaking the id |
| b | `symlink_coverage` (binding) | “across the six frozen symlink tables at least two in-tree rows and at least two escaping rows, and at least one carrier with at least two in-tree rows” | an empty table satisfies both symlink clauses; `R39C1AxisFit` measured `gen-squashfs` silently dropping a link whose target is a directory. Intended set satisfies it: in-tree K2 1 + K5 2 + K6 1 = 4, escaping K1 1 + K5 1 + K6 2 = 4, max 2 |
| c | `xz_leg` (binding) | “and at least one carrier whose own superblock is big-endian SquashFS v4 (`sqsh`, major 4, minor 0) with the xz compression id” | otherwise six gzip images satisfy “six standard-BE v4 carriers” and K6's xz leg is unbound. **Measured id: 2** — `tools/round-37/gen-squashfs.py:8` `COMP = {'gzip': 1, 'xz': 2}`; `--endian be --comp xz` writes u16 at offset 20–21 == 2 (`out-xz.sqsh`: 2, `out-gzip.sqsh`: 1). The counter accepts {2, 4} (4 = upstream `mksquashfs -comp xz`) and records the actual id per carrier in `bindings.xz_leg_detail`, so a closure must read the id, not the word “xz” |

Two smaller strictnesses, same status: `carriers_spec_ok` (exactly ids K1…K6, six distinct pins —
refuses “six copies of K1” and “K5/K6 as decoration”) and `oracle_ok` (oracle.tsv must hold ≥ 1
regular file, so “every oracle file published” cannot be vacuously true).

**Freeze the counter last.** `tools/round-39/c1-counter.py` is in the frozen set, so any commit after
the freeze that touches it exits 2 `frozen_path_changed`. Freeze it in the freeze commit and never
edit it afterwards.

## 3. Clause map — draft sentence → code → what it reads

All lane bytes come from `git show REV:path` (never the working tree); scratch is
`$HYAKU_SCRATCH/kaidoku-r39/counter` (removed per run); `--json-out` receives the full result.

| draft fragment | key in `--json-out` | implementation |
|---|---|---|
| six carriers from `.ufo/waves/round-39/c1/carriers.json` | `carrier_ids`, `carriers_spec_problems` | `carriers_spec()`; entry keys `id, path, sha256, oracle, symlinks` (+ optional `receipt`, default `corpus/evidence/round-39/c1/<id>/after.json`) |
| subject digest equal to the frozen carrier pin | `subject_pin_ok` | `subject.digest.sha256 == sha256` pin |
| the pinned bytes are the committed bytes | `carrier_pin_ok` | `sha256(git show REV:path)` — no round-38 counter checked the carrier bytes |
| operation extract_firmware, provider unblob | `operation_ok` | `operation == 'extract_firmware' and provider.id == 'unblob'` |
| names the `squashfs_v4_be` handler with no failed chunk | `handler_ok`, `chunks_ok` | handler present in `normalized_result.chunks[]`; no chunk with `extraction_failed` true |
| every oracle regular file published (suffix + sha256) | `oracle_hits` vs `oracle_files` | `same_rel()` suffix rule (`p == rel` or `p.endswith('/'+rel)`) |
| gaps exactly one `unpublished-entry` per in-tree symlink, nothing else | `gaps_ok`, `gaps_note` | `gaps_ok()` builds the multiset of matched in-tree rows and compares to the table; any other kind, an unmatched path, an ambiguous suffix or an escaping path fails |
| publishes no path for an escaping symlink | `escaping_ok`, `escaping_published` | `escaping_published()` over `normalized_result.files[]` |
| receipt first added in a strict descendant of the freeze | `receipt_fresh`, `receipt_first_add` | `git log --diff-filter=A --format=%H REV -- path` (oldest) + `git merge-base --is-ancestor` + `add != freeze` |
| recomputes to its evidence id | `evidence_id_ok` | `tools/round-27/xpin-attribute.mjs` **as frozen at `--freeze`**, `--pkg65` = `--pkg67` = the 6.5.0 root |
| `## Round-39 additions to Core` row naming `squashfs_v4_be`, citing the entry | `province_core_section`, `province_core_row` | first table cell must match `(?<![A-Za-z0-9_-])squashfs_v4_be(?![A-Za-z0-9_-])`, row must contain the entry path |
| entry `source: S###` names a SOURCES row opened 2026-10-26 whose used-by lists the entry | `sourced`, `entry_source_ids`, `opened_source_rows` | exact id token (`S1120` cannot match `S112`), `col8 == 2026-10-26`, used-by contains the entry path **or** the stem |
| round-39 frontier note supersedes the BE part | `frontier_note` | one line containing both `Round-39 frontier note` and the entry stem |
| README coverage-map row names the entry stem | `coverage_map_row` | row inside `## Coverage map` |
| no frozen C1 path changed after the freeze | `frozen_path_changed` (exit 2) | `git log --pretty=format: --name-only --no-renames FREEZE..REV` ∩ {4 fixed paths + every `path`/`oracle`/`symlinks` in the frozen carriers.json}; a touch-and-revert trips it too |

Non-gating diagnostics: `symlink_kind_recompute_mismatch` (`resolve_kind()` re-derives each class
under unblob 26.6.4's rule — absolute targets lose the leading `/` and resolve from the extraction
root, relative targets resolve against the link's directory, no normaliser clamping; measured
`/hello.txt` → in-tree, `/../out.txt` → escaping, `../hello.txt` at depth 0 → escaping) and
`oracle_error` / `symlinks_error` (TSV shape).

## 4. Selftest — 33 cases, runtime 8.07 s

`python3 -I -B c1-counter.py --selftest --pkg65 …/rea-agents` →
`{"selftest": "c1-counter", "cases": 33, "green_ok": 1, "red_ok": 32, "failures": []}`, exit 0,
`real 0m8.068s user 0m14.957s sys 0m4.360s`. Every case is a fresh fixture repo under
`$HYAKU_SCRATCH` (identity via `-c user.name=fx -c user.email=fx@fx` inside the fixture only,
toplevel verified before the first commit); envelopes are minted with the frozen xpin rule, never by
running REA. The “fires” column is the measured failing clause from `selftest-detail.txt` — each red
case fails on its intended clause only.

| case | exit | matched | fires |
|---|---|---|---|
| green | 0 | 6 | — |
| do-nothing (freeze files only) | 1 | 0 | receipt_present etc. on all six |
| receipt missing (K6) | 1 | 5 | K6: receipt_present… |
| receipt added at freeze | 1 | 0 | receipt_fresh ×6 |
| receipt added before freeze | 1 | 0 | receipt_fresh ×6 |
| round-38 receipts copied, K5/K6 absent | 1 | 0 | K2–K4: evidence_id_ok, gaps_ok, run_provenance_ok, subject_pin_ok |
| strong copy: round-38-provenance receipts for K1–K4, genuine K5/K6 | 1 | 2 | K1–K4: run_provenance_ok **only** |
| provenance path climbs out of the round-39 segment with `..` | 1 | 2 | K1–K4: run_provenance_ok |
| materialised in-tree symlink (published file, no gap) | 1 | 5 | K2: gaps_ok |
| extra gap kind (extractor-failure) | 1 | 5 | K3: gaps_ok |
| missing gap for an in-tree symlink | 1 | 5 | K4: gaps_ok |
| escaping symlink published | 1 | 5 | K5: escaping_ok |
| wrong chunk handler (LE) | 1 | 5 | K6: handler_ok |
| failed chunk | 1 | 5 | K1: chunks_ok |
| subject digest mismatch | 1 | 5 | K2: subject_pin_ok |
| frozen pin wrong (carrier untouched) | 1 | 5 | K1: carrier_pin_ok, subject_pin_ok |
| carrier bytes changed after freeze | 2 | — | `frozen_path_changed` |
| oracle changed after freeze | 2 | — | `frozen_path_changed` |
| carriers.json changed after freeze | 2 | — | `frozen_path_changed` |
| counter edited after freeze | 2 | — | `frozen_path_changed` |
| edited files list breaks evidence id | 1 | 5 | K3: evidence_id_ok |
| no xz carrier (every superblock gzip) | 1 | 6 | binding xz_leg |
| no escaping symlink row anywhere | 1 | 6 | binding symlink_coverage |
| no carrier exercises two in-tree symlinks | 1 | 6 | binding symlink_coverage |
| province row outside round-39 section | 1 | 6 | province_core_section + province_core_row |
| province row without handler in first cell | 1 | 6 | province_core_row |
| province row absent | 1 | 6 | province_core_row |
| province row cites another entry | 1 | 6 | province_core_row |
| frontier note absent | 1 | 6 | frontier_note |
| S-id substring S1120 | 1 | 6 | sourced (decoy row S112 is present and used-by names the entry) |
| source row opened earlier (2026-10-25) | 1 | 6 | sourced |
| used-by lacks entry | 1 | 6 | sourced |
| coverage map lacks stem | 1 | 6 | coverage_map_row |

## 5. Real-receipt integration check (`sim-real-copy.py`)

A scratch git repo (`/fast/scratch/hyaku/kaidoku-r39/R39C1Counter/sim`, removed) freezes the **real**
K1–K4 bytes: committed `carrier.sqsh|carrier.bin`, committed `oracle.tsv`, a `symlinks.tsv` carrying
the classes frozen by `R39C1SymlinkK1K4` (K1 `link-to-hello ../hello.txt escaping`; K2
`var/lib/run-link ../../a/run.sh in-tree`; K3/K4 empty), this counter, the plan, and doc bindings that
satisfy every PROVINCE/SOURCES/README clause (so only per-carrier clauses are in question). Then the
four committed `corpus/evidence/round-38/c1/K*/after.json` files are byte-copied into
`corpus/evidence/round-39/c1/K*/after.json` **after** the freeze.

```
$ python3 -I -B c1-counter.py --root <sim> --rev <head> --freeze <freeze> --pkg65 …/rea-agents --json-out sim-round38-copy.json
exit 1 (sim_exit=1)
```

| carrier | pin | subject | handler | chunks | gaps | escaping | id | oracle | fresh | provenance | matched |
|---|---|---|---|---|---|---|---|---|---|---|---|
| K1 | ✓ | ✓ | ✓ | ✓ | 0 gaps == 0 in-tree | ✓ not published | ✓ | 5/5 | ✓ | **✗** | ✗ |
| K2 | ✓ | ✓ | ✓ | ✓ | 1 gap == 1 in-tree | ✓ | ✓ | 3/3 | ✓ | **✗** | ✗ |
| K3 | ✓ | ✓ | ✓ | ✓ | 0 == 0 | ✓ | ✓ | 4/4 | ✓ | **✗** | ✗ |
| K4 | ✓ | ✓ | ✓ | ✓ | 0 == 0 | ✓ | ✓ | 4/4 | ✓ | **✗** | ✗ |

`symlink_kind_recompute_mismatch` is empty on all four (the diagnostic agrees with the frozen
classes), `symlink_coverage_detail = {in_tree: 1, escaping: 1, max_in_tree_per_carrier: 1}`,
`xz_leg_detail = {K1: 1, K2: 1, K3: 1, K4: 1}`, `frozen_path_changed: []`. So on the real set the
non-vacuity bindings also bind: K1–K4 alone cannot satisfy them, and a K5/K6 that lacks the promised
links or the xz image cannot either.

## 6. Exit codes at the base and on error paths

| invocation | output | exit |
|---|---|---|
| `--rev a2f64e1 --freeze a2f64e1` on the lane | `{"detail": "carriers.json absent at freeze", "reason": "unevaluable"}` (`base-rev.json`) | 2 |
| no arguments | `usage: --root --rev --freeze --pkg65 required` | 2 |
| `--rev deadbeef` | `{"detail": "git cat-file -e deadbeef^{commit}: fatal: Not a valid object name …"}` | 2 |
| frozen C1 path touched after the freeze | `{"reason": "frozen_path_changed", "frozen_path_changed": [...paths]}` | 2 |
| target not met | per-carrier + binding JSON on stdout, full result in `--json-out` | 1 |
| target met | same | 0 |

At the base the counter therefore cannot report met (no frozen carrier list yet); once
`carriers.json` exists but the receipts do not, it reports 1 with `carriers_matched 0`.

## 7. Residual risks and exact knobs

1. **`chunks` wording.** The draft says “names the `squashfs_v4_be` handler with no failed chunk”; the
   wave item's phrasing (“every chunk handler named `squashfs_v4_be`”) could mean *every* chunk's
   handler is that. Implemented the draft reading (present + no `extraction_failed: true`). On all
   four committed receipts the chunk list is exactly `['squashfs_v4_be']`, so both readings coincide
   on the intended data; the strict reading is one line —
   `set(chunk_handlers(env)) == {HANDLER}` — but it would refuse an honest K5/K6 if unblob ever
   reports a nested/padding chunk. Decide at the freeze.
2. **`PROV_SEGMENT = '/kaidoku-r39/'`.** Module constant, and the only clause that depends on a path
   convention outside the git tree. `R39C1Harness` confirmed (message, this wave) that the delivered
   `c1-run.sh` defaults REA's root to `${HYAKU_SCRATCH:-/fast/scratch/hyaku}/kaidoku-r39/c1-run.XXXXXX/
   extract` and now *refuses* (exit 2, reason naming `run_provenance_ok`) any non-default `SCRATCH`
   without that segment, so the clause is satisfied by construction rather than by convention. Its
   `mk-carriers.py` enforces what `carriers_spec_ok` enforces (contiguous K1..K6, distinct pins and
   paths) and emits the same default `receipt` path the counter falls back to.
3. **PROVINCE first-cell regex** requires the literal token with non-identifier boundaries; a row
   whose first cell reads only “big-endian SquashFS v4” fails. The frontier note needs both the
   marker and the stem on the same line.
4. **used-by is a substring test** (the item says “contains the entry path or stem”); S-id matching is
   an exact token, so `S1120` cannot satisfy a `S112` row.
5. **`resolve_kind` is diagnostic-only** — it never gates. Kept that way deliberately: the class is
   frozen data, and both directions of a doctored table already break `gaps_ok`/`escaping_ok`.
6. **Absolute-target corner** (`/hello.txt` in-tree vs `/../out.txt` escaping) is implemented per
   `R39C1SymlinkK1K4`'s measurement but only shows up in the diagnostic; no frozen carrier holds an
   absolute link, so it matters only if K5/K6 introduce one.
7. **`carriers_spec_ok`** hardcodes ids K1…K6 and distinct pins. If the L1 renames carriers, edit the
   `IDS` tuple before the freeze.
8. The counter is **self-freezing** (§2): a post-freeze edit of `tools/round-39/c1-counter.py` exits 2.

## 8. Reproduction

```
export HYAKU_SCRATCH=/fast/scratch/hyaku
cd .ufo/waves/round-39/w1/artifacts/R39C1Counter
python3 -I -B c1-counter.py --selftest --pkg65 ~/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents
C1_SELFTEST_DETAIL=1 python3 -I -B c1-counter.py --selftest --pkg65 …   # per-case clause detail
python3 -I -B sim-real-copy.py                                          # real K1-K4 receipts, exit 1
python3 -I -B c1-counter.py --root <LANE> --rev <REV> --freeze <FREEZE> \
  --pkg65 ~/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents --json-out <path>
```

Measured limits: selftest 8.07 s wall (33 fixture repos, 46 `node` invocations for minting and id
recomputation); one measured revision costs one `git show` per frozen file plus one `node` call.
