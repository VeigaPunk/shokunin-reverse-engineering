# R38W2ReproK4 — independent re-run of the committed C1 receipts for carrier K4 (wave 2)

**Verdict: CONFIRMED.** The committed round-38 C1 receipts for K4
(`corpus/evidence/round-38/c1/K4/{before,after}.json` at `3b960fe5`) are reproduced
exactly by a non-author seat: my before-arm and after-arm REA envelopes differ from the
committed ones in **0 semantic fields**, the after-arm publishes **4/4 oracle files with
matching sha256**, and both stored evidence ids recompute under the vendored
rea-agents 6.5.0 rule. No landing drift, no hand-edit, no receipt defect found. Two caveats
are recorded below (§9 wording risk, §10 measurement fragility) that a hostile reader could
raise but that do not falsify the claim.

Seat: leaf, advisory. Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, lane HEAD during
the work `e265533ea3a7cd4d9a75a24ef737c2ff0e98e95f`. Nothing outside
`.ufo/waves/round-38/w2/R38W2ReproK4.md` and
`.ufo/waves/round-38/w2/artifacts/R38W2ReproK4/` was written; no VCS mutation, no frozen file
read-mutated, no counter/predicate/carrier/oracle changed.

## 1. Revisions, pins, and what "committed" means here

| item | value |
|---|---|
| first freeze (claims rule) | `e059ca9391642d5b71b6662cabcbdce0d9308719` |
| landed C1/C2 rev | `3b960fe5f9a7f1dfa22819f98dc0fa983f4260a8` |
| base | `77091b492cc53f8743bd0701b1e7d5e66123dd84` |
| lane HEAD during work | `e265533ea3a7cd4d9a75a24ef737c2ff0e98e95f` |
| `git status --porcelain corpus/evidence/round-38/c1/K4/` | empty → committed bytes = worktree bytes |

Pins recomputed from git objects, not copied from the manifest:

| object | pin |
|---|---|
| `corpus/evidence/round-37/c1/K4/carrier.bin` @ `3b960fe5` | sha256 `a29ddc15f5a6abcabf28b7161837eb56b34111e48420e7392e648f2fdfe956ed`, 307 bytes |
| `.ufo/waves/round-38/c1/carriers.json` K4 pin | `a29ddc15…56ed` → **identical to the recomputed carrier** |
| `carriers.json` @ freeze vs @ rev | `be404a9dbc03dc4417df128d3f8c897cd8b6d27601195eec0ca56adaf9fe1be2` both → unchanged |
| `corpus/evidence/round-37/c1/K4/oracle.tsv` @ freeze vs @ rev | `638a6f75579ae1ff508d3152723b1b9b279a90090e180cc63a2a6a758a477d23` both → oracle frozen |
| committed `K4/before.json` | sha256 `000adcfb928a2032395bc47fbab175d1a1e356277db28eb26022f4d5012131e5`, blob `d42a0929b664b8dff5116876e561d0976b1151b6` |
| committed `K4/after.json` | sha256 `d26830916167ff1cee8ddd089605e6e4024f7b77ad56cf4e86907bda1622e28d`, blob `93079cfc5809f9fb03db0b842919e2271badb42d` |

## 2. The two runs (exact commands, exit codes)

Scratch `S=/fast/scratch/hyaku/kaidoku-r38/R38W2ReproK4` (removed at the end); the carrier was
copied to `$S/K4/carrier.bin` and its sha256 re-verified there
(`a29ddc15f5a6abcabf28b7161837eb56b34111e48420e7392e648f2fdfe956ed`, 307 bytes) before either
run. The absolute `REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob` was passed in both arms. Each
output dir did not exist beforehand, so REA created it.

**(a) before-arm.** `CLEANPATH` = `$PATH` with exactly one entry removed,
`/home/vgpnk/.local/bin` (verified: the removal list contains only that path). Under
`CLEANPATH`, `command -v sasquatch-v4be` → nothing.

```
env PATH="$CLEANPATH" REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob \
  npx -y rea-agents@6.5.0 extract-firmware --format json \
  $S/K4/carrier.bin $S/out-before > $S/env_before.json
```
→ exit **0**, stderr empty. Envelope `ev_854527ec55fbb4dfeae033e9f8c3400c101acde2ab9debaeb1f43e732c4f0056`.

**(b) after-arm.** Default PATH, `command -v sasquatch-v4be` → `/home/vgpnk/.local/bin/sasquatch-v4be`.

```
env REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob \
  npx -y rea-agents@6.5.0 extract-firmware --format json \
  $S/K4/carrier.bin $S/out-after > $S/env_after.json
```
→ exit **0**, stderr empty. Envelope `ev_071c77df9b5fe712c8f9df7d077e550f0c3616ce6e9afcb12ede7f195b8d187f`.

Engine recorded in both envelopes: unblob 26.6.4,
`executable_path /home/vgpnk/.local/share/uv/tools/unblob/bin/unblob`, `executable_sha256
0ce7b624f540c2191ff144892584997fe3fb6ab28ab6ef6b88639f8a7cba1d09`, `worker_count 1` — the same
`executable_sha256` the committed receipts carry, i.e. the receipts came from this exact binary.

## 3. Semantic payload comparison — 0 diffs in each arm

Fields compared (each against the committed receipt of the same arm): engine
(name/version/executable_sha256/worker_count), selection, coverage, published_bytes, chunks
(handler/input_path/range/root_file_range/encrypted/extraction_failed), the set of
(relative_path, sha256, size) in `normalized_result.files`, extraction_gaps
(kind/relative_path/dependencies/handler), diagnostics (stage/missing_dependencies/report),
unpublished_entries, depth_limited_paths, derivation child paths, continuation ids.

**Result: 0 semantic diffs, before and after.** Reproducible with
`artifacts/R38W2ReproK4/compare.py` (`compare.out`: `TOTAL semantic diffs across both arms: 0`).

Payload the committed receipts assert, and that I reproduced:

| field | before | after |
|---|---|---|
| `coverage` | `partial` | `complete` |
| `published_bytes` | 0 | 28 |
| `files` | `[]` | 4 |
| `unpublished_entries` | `[]` | `[]` |
| chunk `handler` | `squashfs_v4_be` | `squashfs_v4_be` |
| chunk `extraction_failed` | `true` | `false` |
| chunk `range` / `root_file_range` | `{offset 0, length 307}` | `{offset 0, length 307}` |
| `extraction_gaps` | 1 × `missing-extractor-dependency`, `dependencies ["sasquatch-v4be"]`, `relative_path null` | `[]` |
| `diagnostics` | 1 × `ExtractorDependencyNotFoundReport`, `severity ERROR`, stage `squashfs_v4_be`, `missing_dependencies ["sasquatch-v4be"]` | `[]` |
| `extraction_continuations` | 1 × `id 4ca863d04cc06d61e7be38d0811847a15f55c70f028fdf45e8fefdf75957a07a` | `[]` |
| `derivations` | `[]` | 4 child paths under `$output/firmware.bin_extract` |

## 4. After-arm files vs the frozen oracle

`normalized_result.files` (both mine and committed):

| relative_path | sha256 | size | `oracle.tsv` row |
|---|---|---|---|
| `firmware.bin_extract/apple1.txt` | `6181259c6b2ca629a56920b422e9a8f212a4d0bcead923df92dbd66fbb7e1c30` | 7 | match |
| `firmware.bin_extract/apple2.txt` | `919fc82d6f1031d305dbce2fc5a74a6df5ddf2da472ee4d137c681cef28d4aff` | 7 | match |
| `firmware.bin_extract/apple3.txt` | `2d95014ed3f24e86ce5fc3a4529f057d7b2318d9b24b54f2e9476b154bd21ec6` | 7 | match |
| `firmware.bin_extract/apple4.txt` | `08d9b05b15b998f2dbc741399fef4350c7863cc85df2305d7da4e83e8c8a959d` | 7 | match |

Sets equal (4 = 4), **no extra published file**, and `cmp` on the bytes I extracted against the
committed round-37 `K4/apple*.txt` files reports *IDENTICAL* for all four. `reported_sha256`
equals `sha256` in every record. The predicate's "same relative-path suffix" wording is what
legalises the `firmware.bin_extract/` prefix; the frozen counter implements exactly that
(`fp == rel or fp.endswith('/' + rel)` at `tools/round-38/c1-counter.py:139`), and under it K4
scores 4/4.

Per the frozen counter's clause list (`c1-counter.py:157-192`), every K4-local clause is
satisfied by the landed bytes as I re-measured them: `oracle_frozen` ✓, `oracle_files` 4 ✓,
`after_present` ✓, `after_subject_ok` (subject digest = `a29ddc15…`, the carrier pin) ✓,
`after_operation_ok` (`extract_firmware` / provider `unblob`) ✓, `after_handler_ok`
(`squashfs_v4_be` in handlers) ✓, `after_gaps_empty` ✓, `after_oracle_hits == 4` ✓,
`after_evidence_id_ok` ✓ (§5). I did **not** run the counter itself (another seat owns the
rescore); this is a clause-by-clause read of the frozen source against my measured values.

## 5. Evidence ids: authenticated, not trusted

I did not reimplement the digest. I imported the package's own `parseEvidence`
(`dist/domain/evidence.js`, whose schema `superRefine`s
`computeEvidenceId(withoutId) === evidence_id`) and replayed it over all four envelopes
(`artifacts/R38W2ReproK4/checkid.mjs`):

```
env_before.json: PASS id=ev_854527ec55fbb4dfeae033e9f8c3400c101acde2ab9debaeb1f43e732c4f0056
env_after.json:  PASS id=ev_071c77df9b5fe712c8f9df7d077e550f0c3616ce6e9afcb12ede7f195b8d187f
K4/before.json:  PASS id=ev_c4444070ecf5d3832fb8607464c85cdb6c6ff6cb2a71f1a85f9464d13c0bf8a1
K4/after.json:   PASS id=ev_4348dcafae0806d8c098b00b18eef0765aa074fe1c1712f45ff0d5a49bfbae2e
```

So the "recomputes to its stored evidence id" clause holds for K4: the committed receipts
are internally authenticated, not hand-edited into a passing state.

*Method note (self-corrected).* I first tried a standalone Python transcription of the
RFC 8785 / `emitCanonical` digest. It disagreed — including for **my own freshly emitted**
envelope, which proves the transcription was wrong, not the receipts. I discarded it and used
the vendor code, which is the authoritative implementation. Anyone recomputing these ids
third-party must match JS number formatting and UTF-16 key ordering exactly, or they will
manufacture false mismatches. [INFERENCE] That is a live trap for a future auditor, worth a
line in the lesson.

## 6. Attribution: the before→after delta is `sasquatch-v4be` reachability, nothing else

Because the before-arm is defined by "a stripped PATH", I added a 2×2 control so the delta
cannot be attributed to "some binary in `~/.local/bin`". `$S/bin-v4be-only` and
`$S/bin-sasquatch-only` are directories holding one symlink each, appended to `CLEANPATH`:

| PATH state | `sasquatch-v4be` | `sasquatch` (v1–4) | coverage | files | gap |
|---|---|---|---|---|---|
| `$HOME/.local/bin` stripped | no | no | `partial` | 0 | `missing-extractor-dependency ["sasquatch-v4be"]` |
| stripped + only `sasquatch-v4be` | **yes** | no | `complete` | 4, oracle-matching | none |
| stripped + only `sasquatch` | no | yes | `partial` | 0 | `missing-extractor-dependency ["sasquatch-v4be"]` |
| default PATH (both) | yes | yes | `complete` | 4, oracle-matching | none |

`sasquatch-v4be` alone is **sufficient**; the older `sasquatch` binary alone is **not**. The
recorded difference is therefore exactly the dependency REA names, and the R38-C1 entry title
(`…r38-sasquatch-be-squashfs-recursion`) describes the real mechanism.

Binary pins observed: unblob 26.6.4 `0ce7b624…a1d09`; `sasquatch-v4be` 4.5.1
`fac88740f49b3460db6a67be93aa21e7390e2845b1e2f348265a95419b7214c6`; `sasquatch` 4.5.1
`ad02d27a3d8424b2f67ae88d479dba57334974527943e5f1e305423c4c774754`.

## 7. Landing integrity cross-checks

- Committed `K4/after.json` is **not** a byte copy of the wave-1 author artifact
  (`.ufo/waves/round-38/w1/artifacts/R38ExecAfterK4/after.json`, sha256 `ca329ef3…`) — but it
  is **semantically identical** to it: full-envelope equality after canonicalising
  paths/blob-ids/id, with the sole differing parameter being `output_directory`
  (`R38ExecAfterK4/out-lane` → `l1-receipts/K4-after`). So the integration step re-ran the
  after-arm rather than hand-editing, and the id changed only because the output path is inside
  the digested record. Third independent production of the same payload.
- Committed `K4/before.json` is full-envelope equal to **both** wave-1 before-arm envelopes
  (`envelopes/h-K4-stripped.json`, `envelopes/direct-K4-stripped.json`).
- Committed receipts vs **my** envelopes: 0 semantic diffs (§3). Count of independent
  productions of the identical before-payload: 4 (2 wave-1 + committed + mine); after-payload:
  3 (wave-1 artifact, L1 re-run, mine).

## 8. Every difference observed (the assignment asks for the complete list)

1. `parameters.path` — mine is the scratch copy `$S/K4/carrier.bin`, the committed one is the
   lane carrier. **Same bytes** (sha256 `a29ddc15…`, 307 B); this is the only `parameters` key
   that differs between my envelopes and the committed ones apart from (2).
2. `parameters.output_directory` — `$S/out-{before,after}` vs
   `/fast/scratch/hyaku/kaidoku-r38/l1-receipts/K4-{before,after}`. Identical keys
   `max_depth 3`, `max_output_bytes 268435456`, `max_output_files 10000`.
3. REA staging directory names (`rea-firmware-XXXXXX`) inside `raw_result.execution` — random
   per run, in `raw_result.report[].task.path` and the unblob `--report/--log/--extract-dir`
   args.
4. Provider blob ids: mine `2833995:1` (after run 1), `2850260:1` (run 2); committed
   `3179813:1` (after), `3166410:1` (before). Not pinnable, and not pinned by the counter.
5. `evidence_id` — differs by construction (it digests `parameters`, hence the output dir).
6. `subject.name` / `subject.local_path` — display fields, excluded from the semantic id.

Nothing else differs. A determinism control (second after-arm run, `env_after2.json`) produced
a semantic payload identical to the first; only items 2–5 moved.

## 9. One wording risk I am obliged to flag (does not falsify the claim)

The frozen predicate's parenthetical says the after-receipt is "run with stock unblob 26.6.4;
**no external extractor dependency**" (`plans/round-38-claims.md`, first freeze). My 2×2 table
shows the after-arm is only achievable **with** `sasquatch-v4be` present on PATH. The operative
counter reading is the gap-freedom clause (`after_gaps_empty = gaps(env) == []`,
`c1-counter.py:178,189`) plus oracle hits — and the receipt satisfies that; but the
parenthetical's plain-English reading would be unsatisfied, and the counter cannot measure it
from a receipt at all (the receipt records no PATH inventory). The landed receipt and the
round-38 entry do not hide the dependency — the entry stem literally names
`sasquatch-be-squashfs-recursion` — so this is a **calibration/wording** exposure for the L1,
not a defect in my remit to fix: if a hostile judge reads the parenthetical strictly, the
defence is that the only measurable form of "no external extractor dependency" is REA's own
dependency report, which is empty. I did not and could not change the frozen text.

## 10. Residual risks and limits

- **Fragility of the before-arm definition.** "Strip `$HOME/.local/bin`" produced a genuine
  before-arm on *this* host because that directory is the only one holding
  `sasquatch`/`sasquatch-v4be` (checked with `command -v` under `CLEANPATH`). On a host where
  `sasquatch` also sits in `/usr/local/bin` or a uv tool dir, the same instruction would
  silently produce an after-arm. My run proves the contrast holds here, not that the recipe is
  host-portable.
- **Single host, single user, same day.** I claim reproducibility of the payload, not
  cross-machine invariance. `worker_count` is 1 and unblob's per-run ordering (blob ids,
  staging names) varies by design; only the canonicalized payload is stable.
- **My scope is K4 only.** K1–K3, the C1 aggregate (`carriers_matched 3`, `met_target false`),
  the PROVINCE/frontier/SOURCES/README bindings and the C2 receipt were not re-measured here;
  another seat owns the rescore. K4's own clauses passing says nothing about them.
- **`unpublished_entries` is empty in both arms**, so the K2-style "one unpublished-entry gap"
  is not K4's failure mode; I did not investigate K2's gap (out of scope).
- **Inference markers.** [INFERENCE] that L1 re-ran rather than edited the receipt (deduced
  from the sole `output_directory` divergence + the `l1-receipts/` path name); [INFERENCE] that
  the parenthetical in the predicate was intended in the REA-visible sense (§9).

## 11. Calibration note

Predicted before measuring: (i) the receipts could have drifted at integration if L1 copied a
file and then touched it — **found no semantic drift**; (ii) provider blob ids and staging
names would differ run to run — **confirmed, 5 distinct blob ids across my 5 runs**
(`2830550:1`, `2833995:1`, `2850260:1`, `2895806:1`, `2899128:1`); (iii) the evidence ids would
recompute under the vendor rule — **confirmed**, and my own first transcription of that rule was
wrong in a way that only a self-control on my own fresh envelope exposed. Net: my prior on
"landing receipts are faithful" was right for K4; my prior on "a third party can recompute the
id from the spec" was wrong without the vendor code.

## 12. Tooling authorization record (operator directive, 2026-10-19)

Nothing installed, nothing upgraded — no channel used, so no `pacman` transaction was attempted
(the host-wide pause was never in play). Tools consumed as already present:
`npx` → `rea-agents@6.5.0` (cached at `$HOME/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`,
`package.json` version `6.5.0`, confirmed); `unblob` 26.6.4 via `~/.local/bin/unblob` →
`~/.local/share/uv/tools/unblob/bin/unblob`; `sasquatch`/`sasquatch-v4be` 4.5.1 in
`~/.local/bin` — never reinstalled, moved or removed. REA was reached only through the CLI
(no `xd://mcp__rea_*`).

## 13. Artifacts (under `.ufo/waves/round-38/w2/artifacts/R38W2ReproK4/`)

`env_before.json`, `env_after.json`, `env_after2.json` (determinism), `env_v4be_only.json`,
`env_sasquatch_only.json` (attribution), `checkid.mjs` (vendor id replay), `compare.py` +
`compare.out` (reproduces §3/§4), `SUMMARY.md` (pins, matrix, sha256 index).

Scratch `/fast/scratch/hyaku/kaidoku-r38/R38W2ReproK4` was removed; nothing cited here lives in
scratch.

## 14. Bounds compliance

Wrote only this report and the artifact directory above. No `git add/commit/checkout/reset/
stash/pull/push`, no mutating `jj`; all git use was `show`/`ls-tree`/`rev-parse`/`log`/`status`
(read-only). No write to `corpus/`, `PROVINCE.md`, `SCORECARD.md`, `SHONEN.md`, `LOG.md`,
`tools/`, the fleet repo outside the lane, sibling lanes, or `/home/vgpnk/Projects/shokuknow`.
No subagent, no background job, no `agent://all` message. Advisory throughout: no frozen
predicate, counter, carrier or oracle was changed.
