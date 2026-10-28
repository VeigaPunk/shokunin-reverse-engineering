# R44C1Run — R44-C1 after-freeze data procedure (author + install)

Seat `R44C1Run`, round 44 wave 1. Deliverable: `tools/round-44/c1-run.sh` + `tools/round-44/c1-run.py`
(authored in `.ufo/waves/round-44/w1/artifacts/R44C1Run/`, installed into `tools/round-44/` at the
L1's request). The data procedure itself was **not** run by this seat: only `--dry-run` and the
write guard were executed. `corpus/evidence/round-44/c1/` holds **0 files**.

## Installed artifacts

| path | sha256 |
|---|---|
| `tools/round-44/c1-run.sh` | `c35d4b9bca6cd12e7ff1a89717da033841797dde5cf3f8bd3b262d3e9860b263` |
| `tools/round-44/c1-run.py` | `55e2692a3085537c2a1dc40f987c3ad8b3d7478519ddbc8a4543926fa4b061a7` |

The artifacts-directory copies are byte-identical (verified: same digests both sides). Per-check
receipt (command, exit code, stdout sha256, wall time) in
`artifacts/R44C1Run/verification-receipt.json`.

The documented command is `tools/round-44/c1-run.sh --data-run --rea-outdir-mode scratch` — the
form the L1 wrote into the claims text; `--rea-outdir-mode scratch` is also the default, so the
flag is belt-and-braces rather than required.

## Provenance contradiction found and resolved before the freeze

While authoring I found the claims text and the then-installed counter binding
`parameters.output_directory` to two mutually exclusive paths:

- claims text as amended in wave 1 **at that moment**: `plans/round-44-claims.md:35` and `:137-138`
  said the receipt's `parameters.output_directory` must name a `corpus/evidence/round-44/c1/` path,
  and CTL-C1-4 (`:176-177`) expected the counter to refuse "any `output_directory` not under
  `corpus/evidence/round-44/c1/`";
- counter `tools/round-44/c1-counter.py:258` `PROV_SEGMENT = '/kaidoku-r44/'`, enforced by
  `provenance_ok()` (`:1176-1182`) as the `run_provenance_ok` clause (`:343`), docstring `:156`.

No single path satisfies both. I measured it against the counter's own function, unmodified
(`importlib` of `tools/round-44/c1-counter.py`, calling `provenance_ok`):

| `parameters.output_directory` | `provenance_ok` |
|---|---|
| `/fast/scratch/hyaku/kaidoku-r44/.../c1-run.v1le.1221176/rea-out` (real receipt from my dev arm) | **True** |
| `<lane>/corpus/evidence/round-44/c1/v1le` | **False** |

I reported this to the L1 (`agent://KaidokuR44`) with those line numbers and shipped a
`--rea-outdir-mode {scratch,evidence}` switch so either binding could be adopted without editing a
frozen file. **The L1 resolved it in favour of the counter**: the claims text now reads
`plans/round-44-claims.md:138` "the receipt's `parameters.output_directory` names this round's
`/kaidoku-r44/` scratch segment and the evidence id is minted over that provenance; the runner
records `provenance.json` binding the scratch-produced tree to the verbatim committed copy under
`corpus/evidence/round-44/c1/`", `:163` names the data procedure, and `:180` states the counter
refuses any `output_directory` not under the exact round-44 `/kaidoku-r44/` segment. The runner's
default therefore follows that text. `evidence` mode remains available and writes the receipt with
the evidence path instead, should the counter ever move.

## What the tool does

Per carrier id in `tools/round-44/carriers.json`:

1. resolves the fixture (`path` field, else the fixture directories by id with case and separators
   ignored — `v1le` finds `v1-le--squashfs_v1.0_le.bin`, `v2le` never finds `v2ns-le--…`) and
   verifies the bytes hash to the frozen `sha256`; a mismatch fails that carrier **without** running
   REA on unverified bytes (exit 1, never a silent pass);
2. creates a fresh REA output root under `<scratch-base>/kaidoku-r44/probe-R44C1Run/` — REA 6.5.0
   refuses an existing output root (measured: `{"code":"execution_failure", … "reason":
   "Extraction output root already exists"}`), so it is never pre-created; an existing evidence
   directory fails closed (exit 2) unless `--force`;
3. runs `REA_UNBLOB_COMMAND=<unblob> npx -y rea-agents@6.5.0 extract-firmware --format json
   --full-output <fixture> <scratch>/rea-out` with the child `PATH` fixed to the counter's
   `FIXED_PATH` (so the extractor that resolves is the one the counter's rerun resolves) and
   `TMPDIR` in the same private scratch dir;
4. captures stdout/stderr byte-for-byte and writes into the evidence directory:
   - `firmware.bin_extract/…` — the produced tree, copied **verbatim** (bytes, symlinks, modes,
     mtimes preserved);
   - `envelope.json` — the exact stdout bytes; `after.json` — the envelope's `data` object (the
     shape the counter reads); `stdout.log`/`stderr.log` — the same bytes, explicitly;
   - `unblob.log` — unblob's own log, copied out of REA's task directory by the tee;
   - `extract-env.json` — the toolchain that actually ran; `extract-tree.tsv` — relpath/kind/size/
     sha256 of every produced entry, snapshotted **before** the receipts were written;
   - `provenance.json` — binds the scratch `output_directory` to the verbatim committed copy;
   - `run.json` — `command`, `exit_code`, `stdout_sha256`, `wall_s`, `carrier`, `rev_at_run`, plus
     argv, pins and digests;
5. writes `<evidence-root>/manifest.json` mapping carrier → outdir, run.json path, receipt, extract
   tree, command and per-carrier exit code / stdout sha256 / wall time.

Scope handling: `carriers.json`'s `scope.target_ids` is the default working set
(`v1le, v1be, v2le, v2be` = the four preregistered carriers). `scope.exploratory_ids`
(`v21le, v21be`) run only with `--include-exploratory`, and the manifest records `skipped_ids`
either way — writing receipts for the exploratory pair would put unscoreable evidence in the
receipts directory.

### The extractor log (`extract-env.json`)

REA runs `unblob` with `--log <task dir>/unblob.log` and deletes the task directory afterwards, so a
successful envelope never shows which extractor ran. The runner sets `REA_UNBLOB_COMMAND` to a
transparent tee generated in the scratch: it runs the real unblob (`$HOME/.local/bin/unblob`) with
REA's arguments unchanged, copies the log out, and exits with unblob's own exit code. The receipt
records the real unblob's `path`/`sha256`/`version`, the sasquatch `path`/`sha256`/`version`, the
fixed `PATH`, `log_tee`, and `unblob_log.{path,sha256,command_line}` — the keys the counter's
`extract_env_ok` clause reads. `--no-unblob-log-tee` (or `C1_UNBLOB_LOG_TEE=0`) runs unblob directly
and records the log line as absent, honestly.

### Guards

- Writing into the committed `corpus/evidence/round-44/c1/` requires `--data-run` or
  `KAIDOKU_C1_DATA_RUN=1`; otherwise exit 2 with the reason (a pre-freeze receipt breaks the
  counter's `receipt_fresh` binding). Measured: exit 2, zero writes.
- `--dry-run` prints every command, the REA output root, the verbatim-copy target and the receipt
  list, and writes nothing — not even the scratch directory (measured).
- Exit codes are semantic: 0 every carrier produced a receipt, 1 a carrier failed (REA nonzero, no
  receipt, or pin mismatch), 2 could-not-evaluate (bad arguments, missing/unparsable
  carriers.json, unresolvable fixture, occupied outdir).

## Evidence retained

Dev-arm validation of the **installed** code, real REA 6.5.0, scratch evidence root
(`/fast/scratch/hyaku/kaidoku-r44/probe-R44C1Run/final2`), command
`tools/round-44/c1-run.sh --data-run --rea-outdir-mode scratch`: **exit 0**, 4/4 carriers ok,
14.4 s total (3.3–3.7 s/carrier).

| carrier | handler (exact) | published regular files | oracle match | gaps/unpub/diags | sasquatch flag | counter `provenance_ok` |
|---|---|---|---|---|---|---|
| v1le | `squashfs_v1` | 3 (6/7/7 B) | exact | 0/0/0 | `-le` | **True** |
| v1be | `squashfs_v1` | 3 (6/7/7 B) | exact | 0/0/0 | `-be` | **True** |
| v2le | `squashfs_v2` | 4 (7/7/7/7 B) | exact | 0/0/0 | `-le` | **True** |
| v2be | `squashfs_v2` | 4 (7/7/7/7 B) | exact | 0/0/0 | `-be` | **True** |

"oracle match" compares every published `(sha256, size)` against the frozen
`carriers.json.oracle.members` (e.g. `303980bc…`/6, `5a81483d…`/7, `86baf352…`/7 for v1;
`6181259c…`, `919fc82d…`, `2d95014e…`, `08d9b05b…` for v2) — exact equality in both directions.
`extract-tree.tsv` digests re-hash to the files on disk (0 mismatches). `envelope.json` and
`stdout.log` are the same bytes as `run.json.stdout_sha256`. `xpin-attribute.mjs` printed each
stored evidence id under both the 6.5.0 and 6.7.0 rules (`both`). `provenance_ok` is the counter's
own function, imported unmodified.

Failure paths exercised: a non-squashfs carrier produced a receipt with `ok:true` and no chunk (the
counter's `handler_ok` reds it — the runner does not invent a handler); a stub REA exiting 7
produced `exit_code 7`, `receipt_written false`, tool exit 1; re-running into an occupied evidence
dir exits 2 with the reason; `--force` replaces it and succeeds.

Nothing was installed or updated on the host; no network fetch beyond the already-cached
`rea-agents@6.5.0`. All scratch work is under `/fast/scratch/hyaku/kaidoku-r44/probe-R44C1Run/`.

## Risks

1. `sasquatch-v4be` is absent from this host. None of the four carriers needs it (all are v1/v2 and
   use plain `sasquatch -le|-be`); `extract-env.json` records the absence explicitly.
2. In `scratch` mode the receipt's `files[].path` values point into the scratch root, which the
   runner deletes after the run; the published tree is still committed verbatim in the evidence
   dir and `provenance.json` binds the two. The counter compares `relative_path`, not absolute
   paths, so this is its expected shape.
3. `corpus/evidence/round-44/c1/<id>/` gains a `firmware.bin_extract/` tree alongside the receipts
   (20–28 bytes of published payload). The counter reads `after.json`; a reader must not mistake
   the tree for receipt files.
4. REA's own `raw_result` records absolute scratch paths for the task directory. Those paths are
   reaped with the scratch, exactly as in round 42; the counter's projection excludes absolute
   paths, and its `run_provenance_ok` clause reads `parameters.output_directory` (the round
   segment), not `raw_result`.
5. The working-tree `tools/round-44/carriers.json` was uncommitted at authoring time (4 carriers
   with per-carrier `oracle.members`, `scope`, `toolchain`) while `HEAD`'s copy had 6 carriers and
   no per-carrier oracle rows. The counter reads `carriers.json` at `--rev`, so scoring before that
   table is committed reports `carriers_spec_ok false` / `oracle_files 0`. Freezing the
   working-tree copy clears it; the receipts themselves already score `handler`/`layout_ok`/
   `evidence_id_ok`/`gaps_ok` true.
