# R42C2EntryReview — what table v4 must supersede or keep in the round-41 v3 surfaces (at c4a38ea)

VERDICT: **DEFECTS FOUND** — the S112 citations are exact (`:102`/`:159`/`:245` are the `squashfs_v1`/`squashfs_v2`/`squashfs_v3` handler NAME lines; the installed copy's sha256 equals the SOURCES pin) and the keep/supersede map below is complete, but the draft carries defects to fix before the freeze: **D1** the `dependencies` grammar cannot express the draft's own step-3 membership rule (R41W2 F1 recurs in v4), **D2** the R41-CL4 paraphrase conflates evaluator and interpreter, **D3** `H` is defined two different ways across the v3 surfaces, **D4** the legacy-row/pre-check bracket is grounded on the wrong fact, **D5/D6** wording and a combo-reach interaction.

## 0. Method, pinned bytes, bounds

- Every round-41 surface was read from `git show c4a38ea2fcd7a7da096358f9bf462c9a4be3c33c:<path>` into scratch: `SKILL.md` (1479 lines), `corpus/knowledge/2026-10-26-r41-sqfs-triage-v3.md` (111), `tools/round-41/sqfs-triage-v3.py` (1772), `plans/round-41-claims.md` (211), `corpus/lessons/round-41.md` (95), `corpus/lessons/round-41-verifier-spotcheck.md` (100), `corpus/SOURCES.md`. Working tree HEAD is `fdabdfa` (detached, 3 dirty paths, `SKILL.md` clean); c4a38ea is an ancestor of HEAD. The draft claims file does not exist at c4a38ea (it is new wave work); read from the working tree.
- Installed unblob 26.6.4 `unblob/handlers/filesystem/squashfs.py` sha256 `2d7b901b54e2ad28c28df2cbbdaeb4bcedb58670fb4c4478f9578a0dd5599287` — equals the pin recorded in the SOURCES S112 row (`tag 26.6.4 = commit 1fcc7a0a584a70a96c31f5a276c20944d199a089`, `corpus/SOURCES.md:118`). All source line checks are on that copy; copies of everything cited are in `artifacts/R42C2EntryReview/`.
- Executed at the c4a38ea bytes (`artifacts/R42C2EntryReview/probe-entry.py`, results verbatim in `probe-results.json`): the frozen v3 interpreter's `--table-only` on the c4a38ea `SKILL.md` → rc 0, `marker line: 434  actions line: 435  table line: 436  rules: 12`; six synthetic envelopes (its own `_env` builder) through the same interpreter, rc 0 each:

| probe | envelope | v3 precedence says | v3 interpreter (c4a38ea bytes) said |
|---|---|---|---|
| legacy-clean | H={squashfs_v3}, G=∅, P=2 | `(no-squashfs-chunk, inspect-input)` (step 2, F = v4-only) | `unclassified none` |
| legacy-dep-sasquatch | H={squashfs_v3}, dep gap D={sasquatch} | `(dep-missing-le, install-extractor-le)` | `unclassified none` |
| legacy-dep-both | H={squashfs_v3}, dep gap D={sasquatch, sasquatch-v4be} | `(dep-missing-be, install-extractor-be)` (step 3 arm 1) | `unclassified none` |
| v4be-dep-both | H={squashfs_v4_be}, same both-names gap | `(dep-missing-be, install-extractor-be)` | `unclassified none` |
| legacy-ddwrt-failure | H={squashfs_v3_ddwrt}, extractor-failure, P=0 | v3: `(body-extractor-failure, preserve-failure)`; v4 draft step 6: `(legacy-body-failure, cross-read-legacy)` | `unclassified none` |
| v4be-clean | H={squashfs_v4_be}, clean, P=2 | `(clean, none)` | `clean none` (harness control) |

- No REA/unblob/sasquatch run, no carrier touched (reservation respected), no VCS mutation, no subagents, no background jobs. Tooling record: **nothing installed, upgraded or removed; no pacman transaction.** Scratch `/fast/scratch/hyaku/kaidoku-r42/R42C2EntryReview` removed at the end.
- Interpreter facts used below (read from the c4a38ea copy): `H` is built from `normalized_result.chunks[].handler` **only** (:588-590; docstring :95); `dependencies` cells are exact-set only (:407 `contains=False`; selftest `c_deps_cell_has_no_contains_form` exits 2 on `sasquatch+`); handler cell `none` = empty H (:667-669); a handler pattern fnmatches **any** H member (:670).

## 1. S112 :102/:159/:245 — confirmed, and the family they under-cite

Exact lines in the pinned copy (`artifacts/R42C2EntryReview/S112-line-pins.txt`):

| line | content | check |
|---|---|---|
| :102 | `NAME = "squashfs_v1"` (class at :101) | **confirmed** — v1 handler NAME line |
| :159 | `NAME = "squashfs_v2"` (class at :158) | **confirmed** — v2 handler NAME line |
| :245 | `NAME = "squashfs_v3"` (class at :244) | **confirmed** — v3 handler NAME line |
| :463 / :522 | `68 73 71 73 [24] 04 00` / `73 71 73 68 [24] 00 04` | **confirmed** — the v4 LE/BE magic pattern lines row 1's cause cites |
| :199-200 / :318-319 / :363-364 / :409-410 | `squashfs_v2_nonstandard`, `squashfs_v3_ddwrt`, `squashfs_v3_broadcom`, `squashfs_v3_nonstandard` | **present, uncited** — the rest of the legacy family |
| :454-455 / :513-514 / :548-549 | `squashfs_v4_le`, `squashfs_v4_be`, `squashfs_v4_broadcom` | the v4 family (v4_broadcom uncited anywhere; its magics at :561/:569) |

The SquashFS handler family in 26.6.4 is **ten** NAMEs, and the extractor each resolves is decided at :36-41 (`match endian, self.version`; only `case Endian.BIG, 4` picks `V4BE_EXECUTABLE = "sasquatch-v4be"`, everything else keeps `EXECUTABLE = "sasquatch"`; `get_dependencies()` always lists both, :68-69):

| handler (NAME line) | EXTRACTOR line | version | resolves |
|---|---|---|---|
| squashfs_v1 (:102) | inherited :75 | 3 | `sasquatch` `-be`/`-le` |
| squashfs_v2 (:159) | inherited :75 | 3 | `sasquatch` |
| squashfs_v2_nonstandard (:200) | :204 | 2 | `sasquatch` |
| squashfs_v3 (:245) | inherited :75 | 3 | `sasquatch` |
| squashfs_v3_ddwrt (:319) | :323 | 3 | `sasquatch` |
| squashfs_v3_broadcom (:364) | :368 | 3 | `sasquatch` |
| squashfs_v3_nonstandard (:410) | :414 | 3 | `sasquatch` |
| squashfs_v4_le (:455) | inherited :75 | 3 | `sasquatch` `-le` |
| squashfs_v4_be (:514) | :527 | 4 | BE → `sasquatch-v4be` (+ is_avm branch :42-53) |
| squashfs_v4_broadcom (:549) | :553 | 4 | BE → `sasquatch-v4be` (+ is_avm); LE → `sasquatch` `-le` |

Consequences v4 must absorb:

1. The three cited NAME lines are exactly what the cause cell claims, but they are **not the whole v1–v3 family**: a DD-WRT `tqsh`/`hsqt` image (the C1 draft's own carrier example) is found by `SquashFSv3DDWRTHandler` (:318-323, BIG_ENDIAN_MAGIC `0x74_71_73_68`) and reports handler **`squashfs_v3_ddwrt`**, never `squashfs_v3`. Any v4 row or evaluator phrase keyed on the literal `squashfs_v3` misroutes it; fnmatch `squashfs_v[123]*` covers all seven legacy NAMEs and excludes all three v4 NAMEs (checked against the table above).
2. The draft's step-3 bracket "every v1–v3 chunk and every v4 LE chunk resolves plain `sasquatch`" is **source-true and incomplete**: `squashfs_v4_broadcom` LE also resolves plain `sasquatch` (version-4 extractor falling to the `Endian.LITTLE, _` arm), and its **BE** chunk resolves `sasquatch-v4be` like `squashfs_v4_be` `[INFERENCE: from :553 + :39-41; no committed broadcom envelope]`. Exact wording v4 needs: *only a `(BIG, 4)` resolution — `squashfs_v4_be` always, `squashfs_v4_broadcom` when big-endian — reaches `sasquatch-v4be`; every other chunk resolves plain `sasquatch`.*
3. The "drop without a report" half of row 1's cause (truncated image, `bytes_used` past end, non-4 major) was verified against the same pin by the round-41 wave-2 review (`R41W2C2Table.md` §3 row 1); not re-derived here.

## 2. SKILL.md block 20 (:387–449) row by row — keep / supersede / wrong, with the v4 replacement

Marker :434, actions line :435, header :436, separator :437, rows :438–449 (one row per line; re-confirmed by `--table-only` at these bytes).

| :line | row | verdict for v4 | exact replacement / note |
|---|---|---|---|
| :438 | no-squashfs-chunk | **KEEP cells, SUPERSEDE cause.** Under the draft's widened F (all `squashfs_` names) step 2 and the `none` cell finally mean the same thing — the CL4 divergence closes without touching the cell. | cause: "no `squashfs_*` chunk was carved …"; delete "while a v1-v3 chunk (S112 :102,:159,:245) is not a v4 chunk" — a legacy chunk now has rows of its own and never lands here. Keep the truncated/past-end/non-4 drop facts and the :463/:522 pins; consider citing the full family NAME set or the class list, not three lines. |
| :439 | dep-missing-be | **KEEP semantics.** Only `(BIG,4)` arms resolve `sasquatch-v4be`, and both such handlers (`squashfs_v4_be`, `squashfs_v4_broadcom`) fnmatch `squashfs_v4_*`, so the handler cell stays correct. | deps cell → `sasquatch-v4be+` if D1's grammar fix is adopted (see §5); cause otherwise unchanged. |
| :440 | dep-missing-le | **WRONG cause (R41W2 F1), SUPERSEDE handler cell.** Executed again here: a both-names D is `unclassified` in the interpreter while the precedence's "D holds" sends it to the BE row; and with H={squashfs_v3} even a sasquatch-only dep is `unclassified` because the cell reads `squashfs_v4_*`. | handler cell → `squashfs_*`; deps cell → `sasquatch+` (BE row above it already first) under the D1 fix; cause: "the chunk resolved plain `sasquatch` — every v1–v3 chunk, every v4 LE chunk and a v4 Broadcom chunk read little-endian; only the `(BIG,4)` arms resolve `sasquatch-v4be` (S112 :36-53)" — and the sentence "a dependency list naming both resolves to the BE row above, not here" becomes true **only** with the contains deps cell; without it, it must be replaced by an honest fall-through disclosure. |
| :441 | partial-body-failure | **SUPERSEDE handler cell → `squashfs_*`.** Draft step 4 (P>0) fires before step 6, so a legacy partial failure is `partial-body-failure`; with the v3 cell it falls past every row to `unclassified`. Contains gap cell and `>0` stay. |
| :442 | avm-marker-be-dropped | **KEEP unchanged.** v4-only population; the layout pre-check governs. R41W2 F2 (failing-chunk handler on multi-chunk tuples) is carried, now with wider reach — see D6. |
| — | **legacy-body-failure (new)** | **ADD, above the body row** (draft steps 6 < 7). | `\| legacy-body-failure \| extract_firmware \| unblob \| squashfs_v[123]* \| extractor-failure+ \| * \| * \| * \| 0 \| cross-read-legacy \| …\|`; the actions line (:435) gains `cross-read-legacy` (12 → 13 tokens). Executed here: H={squashfs_v3_ddwrt} + extractor-failure + P=0 is `unclassified` today. |
| :443 | body-extractor-failure | **KEEP cells; reorder below the legacy row.** `squashfs_v4_*` stays correct once the legacy row sits above it (v4_broadcom still matches here). Cause may add "a v1–v3 failing handler is the row above". |
| :444 | depth-limited | **SUPERSEDE handler cell → `squashfs_*`.** REA mints `depth-limited` per path regardless of chunk version (`--max-depth 1` is exactly the C1 setting). |
| :445 | mixed-symlinks | **SUPERSEDE handler cell → `squashfs_*`.** Cells otherwise unchanged (`unpublished-entry+`, SR `yes`). |
| :446 | escaping-symlink-removed | **SUPERSEDE handler cell → `squashfs_*`.** Exact `none` gap cell and SR `yes` stay (the R40 L5 repair). |
| :447 | in-tree-symlink-metadata | **SUPERSEDE handler cell → `squashfs_*`.** Exact singleton stays. |
| :448 | clean | **SUPERSEDE handler cell → `squashfs_*`.** `none`/`no`/`>0` stay. |
| :449 | clean-empty | **SUPERSEDE handler cell → `squashfs_*`.** `0` stays. |

Block-20 prose:

- **:387-394 intro** ("same eight envelope fields … seven of the eight decide") — **KEEP** the mechanism; the redundancy parenthetical ("a `squashfs_v4_be` dependency gap always names `sasquatch-v4be`, a `squashfs_v4_le` one always names `sasquatch`") needs the family extension from §1.2 (v4_broadcom split; a v1–v3 gap always names `sasquatch`).
- **Contains-grammar paragraph** — **KEEP** for gap kinds. The clause "the `dependencies` cell stays an exact set" (also knowledge :20, interpreter docstring :43-44) is the exact sentence D1 supersedes if the grammar is extended; either way that sentence changes.
- **"New rows: `depth-limited` …"** — **KEEP** as v3 history; block 21 carries its own new-row paragraph (legacy row).
- **Row-order sentence** ("a failure row above the depth row, the depth row above both symlink rows, `mixed` above `escaping`, the AVM row above the body row") — **SUPERSEDE**: add "the legacy row above the body row".
- **"The reader is this block … no embedded copy"** — **KEEP verbatim** as the v4 principle (round-40 M1 guard).
- **Layout pre-check (:416–432)** — **KEEP** for the two v4-BE failure rows; **SUPERSEDE its scope**: add that it decides only those rows, and that the legacy row is out of scope **because a v1–v3 chunk never runs `sasquatch-v4be` and the AVM branch is consulted only under `case Endian.BIG, 4` (S112 :36-53)** — not for the reason D4 shows false. R41W2 F3 (the drop-`-be` wrapper delivery is unmeasured) and F6 (the walk is not stated BE-scoped) should be repaired in the same paragraph while v4 is being written.

## 3. Knowledge entry `2026-10-26-r41-sqfs-triage-v3.md` — statement dispositions

| statement (line) | verdict for v4 |
|---|---|
| :22-25 "The handler cell `none` means no chunk handler starting `squashfs`; a chunk whose only SquashFS handler is v1-v3 therefore matches no row and is `unclassified` here, where the precedence's step 2 says `no-squashfs-chunk` — a disclosed divergence the generator never produces" | **SUPERSEDE — this is the R41-CL4 record** (round-41.md:89 files it as exactly this two-sided divergence). v4 closes it by widening F; the v4 entry states it as history. Note the sentence confirms the divergence, not a one-way send — see D2. |
| "The label precedence is the authority (round-40 closure D3)" (evaluator written from the text only) | **KEEP** — indep-eval-v4 is written from the draft's precedence text the same way. |
| "row order is clause order (no-chunk, dep, partial, AVM marker, body, depth, mixed, escaping, in-tree, clean, clean-empty)" | **SUPERSEDE**: v4 clause order inserts legacy between the AVM marker and body rows (draft steps 5, 6, 7). |
| "Twelve rows carry twelve labels and twelve action tokens" | **SUPERSEDE**: 13/13 with `cross-read-legacy`. |
| Combined-gap-sets section (contains cells load-bearing, 18/18 vs 7/18) | **KEEP** — v4 inherits the contains form; CTL-C2-4 (exact sets only) stays meaningful against it. |
| `depth-limited` row section | **KEEP**. |
| Layout pre-check section | **KEEP** + the §2 scope sentence. |
| Limits: "Clause 2 labels an image whose only SquashFS chunk is v1-v3 `no-squashfs-chunk`" | **WRONG under v4 — must not be carried**: with F over the whole family, a v1–v3-only chunk proceeds to the family rows. |
| Limits: "`dependencies` column … redundant with `handler` on every measured class" | **KEEP with the §1.2 family mapping** (redundancy survives; the map is no longer version→binary one-to-one). |
| Limits: "Gap kinds with no row — `unknown-chunk-handler`, `encrypted-chunk`, … are `unclassified`/`none`" | **KEEP**. |
| Scoring section (20 classes × 2 + 12 combos; factors endianness/in-tree/escaping/partial/depth) | **SUPERSEDE** by the v4 generator: widened factors including the handler family (spotcheck D5, CTL-C2-7 8/12 — the refreeze must beat the lookup control on combos). |

R41-CL1 (the `declared`/counter key mismatch): **nothing in block 20 or the knowledge entry causes or repairs it** — it is a generator/counter interface defect, as R41W2C2Table §7 already scoped. The v4 claims' single key `declared_features` is new surface; no supersession needed in these two surfaces.

## 4. R41W2C2Table.md residuals — disposition in v4

| finding | disposition |
|---|---|
| F1 (MEDIUM, dep cause vs exact deps cells) | **Must be fixed by v4 — the draft does not currently fix it.** See D1. Re-executed here at c4a38ea bytes (`v4be-dep-both` → `unclassified none`). |
| F2 (LOW, avm row matches any H member vs the failing-chunk handler the evaluator reads) | **Carried, with wider reach** — the widened combos can contain two squashfs handlers of different families, which is exactly F2's tuple shape (e.g. failure on the v3 chunk, H also holding `squashfs_v4_be`, BE=no, P=0: evaluator → step 6 legacy row; interpreter → the avm row fires first because its pattern matches the *other* member). See D6. |
| F3 (LOW, drop-`-be` wrapper delivery unmeasured) | **Carried** — v4's pre-check paragraph repeats the drop instruction; measure it or keep the R41W2 marker. |
| F4 (LOW, block-19 supersession sentence overgeneralizes v2's partial+link fate) | **Template for v4's new block-20 supersession sentence**: verb precision — say exactly which envelopes v4 relabels (legacy-chunk ones) and that no all-v4 envelope changes its pair (verified by clause comparison: v4 steps 2-12 agree with v3 steps on every v4-family envelope; the only relabelled population is legacy chunks). |
| F5 (INFO, disclosed row-1 divergence) | **Closed by v4** (widened F makes step 2 and the `none` cell coextensive). |
| F6 (INFO, pre-check walk not stated BE-scoped) | **Carried** — one-word repair in the v4 paragraph. |

## 5. Draft defects to fix before the freeze

- **D1 (blocks C2's core binding) — step 3's membership rule is unimplementable in the inherited table grammar.** The draft's step 3 says "D holds `sasquatch-v4be`" / "else D holds `sasquatch`" (membership), but the v4 table inherits exact-only deps cells (interpreter :43-44, :407; selftest refuses `sasquatch+`). A both-names D therefore scores `(dep-missing-be, …)` on the evaluator and `unclassified` on the interpreter — R41W2 F1 verbatim, re-executed here. Fix: extend the deps column with the same contains form as gap kinds (`sasquatch-v4be+` above `sasquatch+` — the existing BE-first order then reproduces the precedence exactly), touching the interpreter's `_parse_set_cell(dep, contains=True)`, the grammar paragraph, the knowledge sentence, and the selftests; **or** keep exact cells and rewrite the dep-missing-le cause plus an explicit disclosure that a both-names tuple matches no dep row. Pick one at draft time: CTL-C2-4 (exact-sets-only control) mutates differently under the two choices and must stay meaningful.
- **D2 — the R41-CL4 paraphrase is one-sided.** Draft (and ticket) wording "v3 sends every v1–v3 chunk to `no-squashfs-chunk`" is true of the v3 **precedence/evaluator** (step 2, F = v4-only) and false of the v3 **interpreter/table**, which returns `unclassified` (knowledge :22-25; round-41.md:89 words it as a divergence; executed here, `legacy-clean` → `unclassified none`). The freeze text should state the two-sided divergence; CTL-C2-0b's "labels every legacy-chunk envelope `no-squashfs-chunk` **or** `unclassified`" is accurate precisely because of the two sides — keep the OR.
- **D3 — `H` is defined two ways in the surfaces v4 inherits.** v3 claims :103-108: H = `chunks[].handler` ∪ `extraction_gaps[].handler` (nulls dropped); the interpreter builds H from **chunks only** (:588-590, docstring :95) and the knowledge entry says "chunk handlers". The draft's F ("SquashFS handler names in H") inherits the ambiguity. Pin one definition in the v4 claims — recommend chunks ∪ gaps, matching evaluator step 5's "the failing chunk's handler (else H)" and REA's per-chunk failure-gap payload (S119 `FirmwarePublication.js:288-293`) — and make the v4 interpreter read both lists.
- **D4 — the legacy-row bracket's ground is checkably wrong as stated.** "the AVM layout pre-check does not apply to a v1–v3 superblock" invites a struct check that fails it: `squashfs3_super_block_t` **has** `mkfs_time`, `inode_table_start` and `directory_table_start` (v3 `C_DEFINITIONS`, right after :245; only the v1 struct lacks `mkfs_time`). The true ground: the pre-check exists to overturn a `-be` handshake decision, and unblob's v1–v3 extraction path never makes one — the AVM branch lives only under `case Endian.BIG, 4` and a v1–v3 chunk always runs plain `sasquatch` (S112 :36-53). Re-ground the sentence.
- **D5 (wording) — step 3's bracket "every v1–v3 chunk and every v4 LE chunk resolves plain `sasquatch`"** is source-true but incomplete (misses `squashfs_v4_broadcom` LE) and the label `dep-missing-le` is about the *executable*, not the chunk's endianness (a v3 **BE** chunk missing `sasquatch` lands there). The draft's own "[label wording may change]" flag covers this; the exact replacement is in §1.2.
- **D6 (conditional on the widened combos) — F2's failing-handler mismatch becomes held-out-reachable.** Steps 5/6 of the draft correctly name the **failing** handler, but the table's handler cells fnmatch any H member, so a two-family combo with the failure on the legacy chunk and `squashfs_v4_be` elsewhere in H sends the interpreter to the avm row and the evaluator to the legacy row. Either give the v4 interpreter failing-chunk-handler semantics for the three failure rows (read the `extractor-failure` gap's handler first, else H — the evaluator's own rule), or scope the combo factors to a single failing chunk and disclose. Decide before the held-out generator is frozen, not after.

## 6. Residual risk and verification gaps

- All probes are feature-level on synthetic envelopes through the frozen interpreter; no REA/unblob/sasquatch run and no carrier was touched, so nothing here measures what REA actually emits for legacy chunks (that is C1/wave work). The claim "every v4-family envelope keeps its v3 pair" is a clause-by-clause comparison of the two precedence texts, not an executed replay [INFERENCE — mechanical, no semantic step changed for v4 handlers].
- `squashfs_v4_broadcom` dependency behavior (`:553` → `sasquatch-v4be` on BE) is read from source with no committed envelope; marked in §1.2.
- Row 1's "drops … without a report" clause and the round-39 knowledge anchors were verified by the round-41 wave-2 review against the same pin, not re-derived here.
- The v3 evaluator (`indep-eval-v3.py`) was not re-read; its step-5 failing-handler semantics are taken from R41W2C2Table's executed selftest record.
- Artifacts: `artifacts/R42C2EntryReview/{probe-entry.py, probe-results.json, S112-line-pins.txt, SKILL-c4a38ea.md, r41-sqfs-triage-v3-knowledge.md, round-41.md, round-41-verifier-spotcheck.md, round-41-claims.md, sqfs-triage-v3.py}`. Scratch removed.
