# R42C2Eval — independent evaluator v4 (round 42 wave 1)

**Verdict: DONE** — `artifacts/R42C2Eval/indep-eval-v4.py` (sha256 `06a21de6fe9dd95075561d9026b3fceec2de247d442c3a13a18590d0d8bf077f`) is written from the draft label
precedence alone, passes **37/37** hand-written selftest cases covering steps 1–13 and every `(label, action)`
pair, and agrees with the round-41 frozen expectations on **40/40** named-class envelopes. The draft's two
bracketed uncertainties (`step 3` "to be confirmed by wave 1", `step 6` "wave 1 confirms or replaces") are
**CONFIRMED** on 17 fresh real REA 6.5.0 envelopes; six draft/table defects are recorded below for the freeze.

---

## 1. Deliverable

| item | value |
|---|---|
| file | `.ufo/waves/round-42/w1/artifacts/R42C2Eval/indep-eval-v4.py` |
| sha256 | `06a21de6fe9dd95075561d9026b3fceec2de247d442c3a13a18590d0d8bf077f` |
| size / lines | 29 789 B / 742 lines, Python 3.14 stdlib only, no lane import |
| CLI | `indep-eval-v4.py [ENVELOPE] [--envelopes DIR] [--out FILE] [--full] [--selftest]` |
| selftest | `python3 indep-eval-v4.py --selftest` → `37/37 cases; 0 failure(s)`, exit 0 |
| exit codes | 0 ok · 1 selftest failure · 2 usage/IO error |

`--envelopes DIR` walks each subdirectory (like round 41) and also accepts flat `*.json` files; `--full` prefers
`rea-full.json`, then `envelope.json`, then `after.json`. Non-envelope JSON in the directory (`manifest.json` and
the like) is **skipped and listed**, not scored — see §7 for why that matters on the round-41 held-out set. Output
record: `{id, envelope, label, action, step, features{OP,PR,H,F,G,D,BE,SR,P,FH}}`; the top level carries `n`,
`labels` (histogram), `vocabulary` and `skipped`.

Single-envelope demo (output trimmed):

```
$ python3 indep-eval-v4.py corpus/evidence/round-41/c1/L4/after.json
{"id":"after.json","label":"depth-limited","action":"raise-depth","step":8,
 "features":{"OP":"extract_firmware","PR":"unblob","H":["squashfs_v4_be"],
             "F":["squashfs_v4_be"],"G":["depth-limited","unpublished-entry"],
             "D":[],"BE":"n/a","SR":"no","P":14,"FH":["squashfs_v4_be"]}}
```

## 2. Independence (what was and was not opened)

Read: `plans/round-42-claims.md` (`## R42-C2`, steps 1–13); `plans/round-41-claims.md:100-135` (the feature
definitions the draft cites, `:109-115`); committed envelopes under `corpus/evidence/round-41/c2/heldout/*/` and
`corpus/evidence/round-41/c1/*/after.json`; REA 6.5.0 envelope semantics from `rea-agents/dist/cli-runtime/cli.js`
(gap-kind producers) and unblob 26.6.4 `handlers/filesystem/squashfs.py`, `extractors/command.py`. Round-41's
evaluator was read **only** as `--help` (four lines: `--envelopes`, `--out`, `--full`, `--selftest`).

Not opened: `SKILL.md` (any block), `tools/round-39..41/*` source, other seats' artifacts.

After the file was final, the round-41 held-out `manifest.json` `carriers[].label/action` were read **once**, as an
after-the-fact calibration check (§7). No rule, constant or case in the evaluator changed after that read; the only
later edit was the batch-mode non-envelope guard (§1), after which the selftest was re-run to 37/37.

## 3. Feature extraction (envelope field → feature)

| feature | read from | rule |
|---|---|---|
| OP | `operation` | exact string |
| PR | `provider.id` | exact, case-sensitive |
| H | `normalized_result.chunks[].handler` ∪ `normalized_result.extraction_gaps[].handler` | ordered unique, null/empty dropped |
| F | H | members with the `squashfs_` prefix |
| G | `normalized_result.extraction_gaps[].kind` | set |
| D | `normalized_result.extraction_gaps[].dependencies` | union, exact names (never substring) |
| BE | `normalized_result.diagnostics[].report.command` | shell tokens of every recorded argv (string or list): `yes` if any token is `-be`; `no` if argvs exist and none has it; `n/a` if no argv is recorded |
| SR | `normalized_result.diagnostics[].report.__typename__` | `yes` iff `MaliciousSymlinkRemoved` appears (a removal is a diagnostic, never a gap kind) |
| P | `normalized_result.files` | `len(...)`; absent list reads 0 |
| FH (helper, not a feature) | `extraction_gaps[].handler` where `kind == extractor-failure` | ordered unique; falls back to H when no failure gap names a handler |

A v1–v3 handler is `squashfs_v1*`, `squashfs_v2*` or `squashfs_v3*`. Implements the draft's 13 steps verbatim, with
four literal readings it does not spell out:

1. step 3 is evaluated before step 4, so a dependency gap wins over an extractor failure **even when P > 0**;
2. D is a set tested in the draft's order, so D holding both names answers `dep-missing-be`;
3. step 6 carries no BE condition → a failing v1–v3 chunk answers `legacy-body-failure` whatever its argv shows;
4. step 5 requires `BE = no`, so a v4 BE chunk that failed **with** `-be` falls through to step 7.

## 4. Real-envelope evidence (the draft's "wave 1 confirms" items)

17 envelopes produced by the real CLI (`cd $S`, `REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob npx -y
rea-agents@6.5.0 extract-firmware --format json --full-output --max-depth N <fixture> <fresh dir>`), fixtures from
unblob 26.6.4 (MIT) — all artefacts copied to `artifacts/R42C2Eval/dev-envelopes/` and
`artifacts/R42C2Eval/dev-fixtures/` with `SHA256SUMS`.

| envelope | H | G | BE | P | step | v4 pair |
|---|---|---|---|---|---|---|
| v3le_full (depth 1) | squashfs_v3 | depth-limited | n/a | 2 | 8 | depth-limited / raise-depth |
| v3le_d3 (depth 3) | squashfs_v3 | – | n/a | 2 | 12 | clean / none |
| v1le_full / v1le_d3 | squashfs_v1 | depth-limited / – | n/a | 3 | 8 / 12 | depth-limited / clean |
| v2le_full | squashfs_v2 | depth-limited | n/a | 4 | 8 | depth-limited / raise-depth |
| v3be_full | squashfs_v3 | depth-limited | n/a | 2 | 8 | depth-limited / raise-depth |
| v3lzma_le | squashfs_v3 | – | n/a | 2 | 12 | clean / none |
| v2nonstd_le | squashfs_v2_nonstandard | – | n/a | 4 | 12 | clean / none |
| v3nonstd_le | squashfs_v3_nonstandard | – | n/a | 2 | 12 | clean / none |
| v3le_no_sasq (PATH without `sasquatch`) | squashfs_v3 | missing-extractor-dependency, D=[sasquatch] | n/a | 0 | 3 | dep-missing-le / install-extractor-le |
| v3le_no_both (both sasquatch binaries off PATH) | squashfs_v3 | missing-extractor-dependency, D=[sasquatch] | n/a | 0 | 3 | dep-missing-le / install-extractor-le |
| v3le_no_v4be (`sasquatch` present, `sasquatch-v4be` absent) | squashfs_v3 | depth-limited | n/a | 2 | 8 | depth-limited / raise-depth |
| v4le_no_sasq | squashfs_v4_le | missing-extractor-dependency, D=[sasquatch] | n/a | 0 | 3 | dep-missing-le / install-extractor-le |
| v4le_no_v4be | squashfs_v4_le | – | n/a | 2 | 12 | clean / none |
| v3le_bodydead (metadata zeroed from 0x78) | squashfs_v3 | extractor-failure | no | 0 | 6 | legacy-body-failure / cross-read-legacy |
| v3be_bodydead (same, BE fixture) | squashfs_v3 | extractor-failure | **yes** | 0 | 6 | legacy-body-failure / cross-read-legacy |
| v3le_corrupt (bytes 200–3499 overwritten) | squashfs_v3 | extractor-failure, unknown-chunk-handler | no | 2 | 4 | partial-body-failure / salvage-partial |

Recorded argv on failure: `sasquatch -le -no-exit-code -f -d …` (LE), `sasquatch -be -no-exit-code -f -d …` (BE),
`sasquatch-v4be -no-exit-code -f -d …` (AVM BE, no `-be`), `sasquatch-v4be -be -no-exit-code …` (BE non-AVM, from
the committed round-41 `C01`/`H19`). `sasquatch-v4be` never appears on a v1–v3 chunk.

### Confirmations

- **C-1 — step 3's endianness pairing is exact.** The gap's `dependencies` names only the executable the chunk's
  endianness selects, because the report is built inside the per-chunk `Command` instance
  (`unblob/extractors/command.py:65-73`) whose `get_dependencies()` returns `[self._executable]` (`:101-102`);
  `SquashFSExtractor.get_dependencies()` returning both names is used only by the CLI's dependency banner
  (`dependencies.py`, `get_dependencies`, called from `cli.py:116`). Consequences measured: a v3 chunk with only
  `sasquatch-v4be` missing yields **no gap**
  and extracts (`v3le_no_v4be`); with both binaries absent the gap still names `sasquatch` only
  (`v3le_no_both`); a v4 LE chunk with only `sasquatch-v4be` missing extracts clean (`v4le_no_v4be`). The draft's
  wording "every v1–v3 chunk and every v4 LE chunk resolves plain `sasquatch`" is correct and needs no change.
- **C-2 — step 6 is reachable and correctly shaped.** Both endiannesses give P = 0 with a single
  `extractor-failure` gap on handler `squashfs_v3`; the BE case shows `BE = yes` and still resolves to step 6, which
  is what the draft intends (the AVM pre-check cannot apply to a v1–v3 superblock).
- **C-3 — step 5 remains reachable after the insertion.** Committed `H17`/`H18` (AVM BE, P = 0, argv without
  `-be`) → `avm-marker-be-dropped`; they are the only two `avm-marker-be-dropped` labels in the 52-envelope set.
- **C-4 — C1's extractor note holds.** v1–v3 use `sasquatch -be|-le`; only v4 BE uses `sasquatch-v4be`
  (`-be` for non-AVM, no flag for the AVM layout).

## 5. Defects and draft amendments (attack of the draft)

**D-1 (blocking for the table/generator) — no `_le`/`_be` suffix exists on the legacy handler names.** unblob
26.6.4 emits `squashfs_v1`, `squashfs_v2`, `squashfs_v2_nonstandard`, `squashfs_v3`, `squashfs_v3_ddwrt`,
`squashfs_v3_broadcom`, `squashfs_v3_nonstandard` (`handlers/filesystem/squashfs.py:102,159,200,245,319,364,410`);
endianness lives only in the argv. A block-21 cell or interpreter written as `squashfs_v3_le|squashfs_v3_be` can
never match, and CTL-C2-9's "handler cell left at `squashfs_v4_*`" must be paired with the real legacy name list.
Also: unblob's `squashfs_v3_ddwrt/` and `squashfs_v3_broadcom/` fixture trees ship **byte-identical copies** of the
plain v3 fixtures (`squashfs_v3_ddwrt/little_endian/__input__/squashfs_v3_le.bin` = `0161351c…`, identical to
`squashfs_v3/squashfs_v3_le.bin`; broadcom BE = `4e9493d9…` = plain v3 BE), so no fixture produces a `ddwrt` or
`broadcom` chunk; those two names are unreachable for a generator that only replays fixtures. The 5 reachable legacy
names from fixtures are `squashfs_v1`, `squashfs_v2`, `squashfs_v2_nonstandard`, `squashfs_v3`,
`squashfs_v3_nonstandard` (all 5 measured clean, §4). The draft's "clean per handler" must enumerate these five, or
it produces a class that never materialises.

**D-2 (ambiguity) — "failing handler" is undefined for a multi-failure envelope.** v3's text said "the failing
chunk's handler (else H)" (singular). With two failing chunks of different families (plausible for an image holding
a v3 rootfs and a v4 member; not present in the committed evidence — [INFERENCE] latent) an interpreter that picks
"the first failing chunk" and one that tests the set can disagree on steps 5 vs 6. This evaluator uses
`FH = handlers of extractor-failure gaps, else H` and tests membership, so step 5 wins. Block 21 should say
"any failing chunk's handler".

**D-3 (ambiguity) — step 3's continuation clause must appear in the table.** `dependencies: []` is producible
(REA has an `UNNAMED_DEPENDENCY_CONTINUATION` branch, `cli.js:14189`); with the literal text such an envelope falls
past steps 4–12 to step 13 (`unclassified`). The draft prose has "else continue"; a table that merely lists the two
name rows will let an interpreter stop at step 3.

**D-4 (wording) — step 2 must key on the `squashfs_` prefix, not on "a SquashFS chunk".** Real envelopes carry
null handlers for unidentified regions (`v3le_corrupt`: chunks `[null, squashfs_v3]`), and a squashfs handler can
appear only on a gap. An interpreter that reads `chunks[].handler` alone reproduces exactly the R41-CL4 shape.

**D-5 (generator) — `encrypted-chunk` is unreachable for SquashFS.** REA emits it only for `chunk.encrypted ===
true` (`cli.js:14270`) and unblob reports `encrypted: false` for every squashfs chunk in the committed evidence; no
committed envelope carries that kind. The step-13 catch-all class must be built from `unknown-chunk-handler`
(real and reproducible — `v3le_corrupt` above) or a removal beside an unrelated gap, never from a fabricated
encrypted flag.

**D-6 (generator) — depth 1 cannot exercise the clean legacy rows.** At `--max-depth 1` every successful legacy
extraction produces `depth-limited` → step 8 (5 of the 9 depth-1 envelopes). The same fixtures at depth 3 are
`clean` with `G = ∅`. Legacy clean / clean-empty / in-tree-symlink classes must be generated at `max_depth 3`
(the round-41 manifest already used `3` for its clean classes and `1` for the depth-limited ones).

**D-7 (generator) — the "zero-file body damage" recipe must be the measured one.** Overwriting bytes after the
superblock (200–3499) left a null-handler region and 2 published files → step 4 `partial-body-failure`, not step 6.
Zeroing every byte from `0x78` (all metadata descriptors) leaves the superblock valid and yields exactly one
`extractor-failure` gap with P = 0 → step 6. Both fixtures are in `dev-fixtures/` with the recipe above.

**D-8 (minor) — the `dep-missing-be` tie-break branch is dead for real envelopes.** Since D can hold only the
selected executable (C-1), the "D holds both" case cannot come from a real REA run; it stays harmless but the
generator must not attempt to build that class from a live capture (only a synthetic envelope reaches it).

## 6. No-regression on the v3 surface (shadow check)

`shadow-v3.py` (in the artifacts, written only from `plans/round-41-claims.md`) re-implements the v3 precedence on
the same extracted features so the two texts can be compared without touching the frozen round-41 evaluator.

| set | n | v3 vs v4 differences |
|---|---|---|
| round-41 held-out envelopes | 52 | **0** |
| round-41 C1 receipts (V3, V4, L3, L4) | 4 | **0** |
| 17 fresh dev envelopes | 17 | 15 — every legacy envelope: v3 `no-squashfs-chunk` → v4 `clean`/`depth-limited`/`legacy-body-failure`/`partial-body-failure`/`dep-missing-le`; the 2 v4-LE envelopes agree |

So v4 is a strict extension: identical pairs on everything v3 covered, and it replaces R41-CL4's
`no-squashfs-chunk` on 15/15 real v1–v3 envelopes with four distinct, non-degenerate rows.

## 7. Calibration

- **Named classes: 40/40 exact.** The round-41 held-out set is 20 named classes × 2 replicates + 12 `combo`
  carriers (`manifest.json`: 52 carriers; my earlier `n = 53` was `manifest.json` itself being scored — the guard
  in §1 now skips it). My evaluator reproduces the frozen expected `(label, action)` of all 40 named-class
  replicates; the 12 combos carry `label: null` in the manifest (their expectation is evaluator/interpreter
  agreement), so there is nothing to contradict there — my pairs on them: 6 `partial-body-failure`,
  4 `depth-limited`, 1 `in-tree-symlink-metadata`, 1 `mixed-symlinks`.
- **Distribution on the 52** (steps in brackets): `partial-body-failure` 14, `depth-limited` 10, `clean` 4,
  `body-extractor-failure` 4, `mixed-symlinks` 3, `in-tree-symlink-metadata` 3, `avm-marker-be-dropped` 2,
  `dep-missing-be` 2, `dep-missing-le` 2, `escaping-symlink-removed` 2, `clean-empty` 2, `no-squashfs-chunk` 2,
  `unclassified` 2. Steps 1,2,3,4,5,7,8,9,10,11,12 are exercised; **6 and 13 are the new/legacy space** — step 6
  is exercised by the dev envelopes in §4 and step 13 by the synthetic catch-all cases in `--selftest`.
- **C1 receipts:** `depth-limited` for all four (V3, V4, L3, L4 — each `G = {depth-limited, unpublished-entry}`;
  `V4` additionally `SR = yes`), i.e. step 8 outranks step 9 there. Same pair the v3 text gives.
- **Selftest coverage:** 37 envelopes, every step 1–13 and every one of the 14 `(label, action)` pairs in the
  draft's vocabulary, plus the CLI-envelope unwrap, the `BE = n/a` guard, and the legacy name family
  (`squashfs_v1`, `squashfs_v2_nonstandard`, `squashfs_v3`, `squashfs_v3_ddwrt`, `squashfs_v3_broadcom`).

## 8. What block 21 must say to be unambiguous (for the table author)

1. Step 2: "no handler in H (chunks ∪ gaps) carries the `squashfs_` prefix".
2. Step 3: both name rows, then the explicit continuation sentence; D compared by exact name.
3. Step 5/6: "any handler of an `extractor-failure` gap (else any handler in H)".
4. Step 6: the five reachable legacy names, or the three-family glob spelled out (`squashfs_v1*`, `squashfs_v2*`,
   `squashfs_v3*`) — not `_le`/`_be` pairs.
5. Step 5 keeps the `BE = no` condition; step 6 states that it has none.
6. Step 11: "exactly `{unpublished-entry}`".
7. Never introduce `coverage` or `depth_limited_paths` as inputs — neither appears in the precedence.

## 9. Tooling, bounds, cleanliness

- No installation, upgrade or removal: REA 6.5.0 came from the existing npm cache
  (`/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`), unblob 26.6.4 and sasquatch/sasquatch-v4be
  4.5.1 were used in place. No pacman, no `~/.local/bin` write; the PATH-stripped runs used symlink dirs inside my
  own scratch and the child `PATH` only (e.g. `PATH=$S/bins_sasq:$NPMBIN:/usr/local/bin:/usr/bin:/bin`,
  `REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob` absolute).
- Nothing third-party was copied into the lane except unblob's MIT fixtures (14 files, 60 KB) plus three fixtures I
  generated from them (`v3le-corrupt`, `v3le-bodydead`, `v3be-bodydead`, 4 KB each) — all under `dev-fixtures/`
  with `SHA256SUMS`; the 17 REA envelopes (180 KB) are under `dev-envelopes/`. No published C1 candidate was
  touched; every input here is a development input per the carrier rules.
- Scratch `/fast/scratch/hyaku/kaidoku-r42/R42C2Eval` removed (`ls -d` now reports it absent). The REA runs made
  before `TMPDIR` was exported staged under `/tmp/rea-firmware-*`; REA removed its own staging directories
  (`ls -ld /tmp/rea-firmware-*` finds none), so nothing of mine is left under `/tmp`.
- Report path: `.ufo/waves/round-42/w1/R42C2Eval.md`.

## 10. Risks / open items for the L1

- **Frozen-table token drift.** The evaluator's action tokens are the draft's exactly
  (`install-extractor-be`, `install-extractor-le`, `salvage-partial`, `wrap-extractor-be`, `cross-read-legacy`,
  `preserve-failure`, `raise-depth`, `audit-symlinks`, `expect-link-absent`, `count-gap`, `none`,
  `confirm-empty`, `inspect-input`). If the freeze renames `legacy-body-failure`/`cross-read-legacy` (the draft
  allows it), the evaluator file must be regenerated, not patched only in the table — otherwise both sides agree
  only by accident of spelling.
- **`tools/round-42/indep-eval-v4.py`** is the frozen path the draft names; this file is the candidate for that
  path (byte-identical copy expected at integration, sha256 above).
- The generator must not emit a task whose expected label comes from this evaluator (independence); the v4
  predicate compares it against the interpreter, which is the point of the pair.
