# ExecRedControls — red-control battery over the committed round-50 envelopes

Seat: ExecRedControls · round 67 · wave w1 · base `a7a4ce6902204d5c6cc6c4e3e78b4bffe8312b92`,
operative freeze `3663e6b21dccf4c4957f459301156664d8b151d6`.

The wrapper's own `--control` covers two red fixtures (a dropped symlink gap and a
materialised char-device path). This battery extends the rejection surface across the class
boundaries, the three disposition families, the structural allowances, the removal family and
the publication check. It calls the pinned round-50 engine **directly** —
`disposition_check`, `nonregular_published`, `gap_rule_model` — imported by path under
sha256 `9820811bf29f2de988f8ddb2513cf365f30a89a36f2bb465f96f1926ef9bd813`, not through the
wrapper.

Machine-readable result: `red.json` (this directory). Harness: `red_controls.py`.
Run: `cd .ufo/waves/round-67/w1/ExecRedControls && TMPDIR=<scratch> python3 red_controls.py`
(writes `red.json`, exits 0 iff green).

## Instrument and rule at run time (both moved during this wave)

The dispatch card pins the counter at `f78ed365…` and the rule at `e66ba02…`. Both are the
blobs committed at the operative freeze; three disclosed corrections followed, so the card's
numbers no longer describe what the score will run:

| commit | counter | rule v2 | change |
|---|---|---|---|
| `3663e6b2` (freeze) | `f78ed365…` | `e66ba02…` | the dispatch pins |
| `1e7fe7b7` | `55decb51…` | `e66ba02…` | `patch_engine` passed an absolute gap-rule path; the engine reads `GAPRULE` through `git show <rev>:<path>`, which exits 128 for an absolute path (*gap-rule.json absent at freeze*). Now lane-relative. |
| `ecc4de0e` | `e44cacf5…` | `e66ba02…` | REA package re-pin: the r42 lock `d42d56f0` is no longer reproducible; `REA_PKG_R67` pins version + `package.json` sha256 + the lock this host resolves, and `patch_engine` replaces `mod.rea_package_problems`. |
| `7cfe83e4` | `5d6cc82a…` | `b55d5e87…` | rule `removed.silent` restored (`char-device ["247:0"]`, inert under the class rule); `RULE_V2_PIN` enforced in `--score`; the engine clause set used **unchanged** (all 23, `carrier_fresh_ok` no longer dropped); the commit's control receipt bound as the predicate's second conjunct |

At run time: counter `5d6cc82a…` = HEAD blob = claims-declared pin; rule `b55d5e87…` = HEAD blob
= `claims.json` pin = the counter's own `RULE_V2_PIN` (all four agree); no undisclosed instrument
commit.  The battery therefore pins by *HEAD-blob equality at run time* and records the chain
(`red.json → instrument_pins`), never by a number copied from the card.

Static checks of the corrections (all pass):

- `patch_engine` yields `tools/round-67/gap-rule-v2.json`; `git show <freeze>:<that path>`
  resolves to the same `b55d5e87…` bytes, so the engine's `gap_rule_unchanged` can hold.  The
  absolute-path form exits 128 at the freeze and at HEAD — the defect was real.
- `REA_PKG_R67` matches the host: `rea-agents` 6.5.0, `package.json` `a5003023…`,
  `…/.npm/_npx/ad9a3fdbcad992c6/package-lock.json` `815c18f1…`.
- `carrier_fresh_ok` (now a live clause) holds: the engine's prior-pin harvest at the freeze
  returns 18 pins from three sources, none of them one of the four carrier pins.

## Step 1 — the wrapper's control reproduces

`python3 -I -B tools/round-67/avm-le-counter.py --control --rev <base>` exits 0,
**gaps_ok_round50 = 2, gaps_ok_round67 = 4**, `control_ok true` (fresh receipt
`814f960c…`, this directory's `wrapper-control.json`).

The committed before record, `.ufo/waves/round-67/l1/pre/control-dryrun.json`
(`69cb4a99…`), carries the **same numbers and the same per-carrier table** but two stale
digests: it was generated with counter `e44cacf5…` and rule `e66ba02…`, not the current
`5d6cc82a…` / `b55d5e87…`.  The differing top-level fields are exactly
`counter` and `rule_v2_sha256`; `gaps_ok_round50`, `gaps_ok_round67`, `control_ok`,
`per_carrier`, `rule_r50_sha256` and `target` are identical (see finding F7).

The superseded freeze blob `f78ed365…` produces the same numbers again; the only JSON delta is
its own `counter.sha256`, which is what makes the corrections `--score` fixes and not control
fixes.

The same 2/4 was recomputed independently from the raw envelopes without the wrapper:
`c6430`/`c6490` pass under both rules; `g7581`/`g7582` fail only under round 50, on
`['dev/pts/0' … 'dev/pts/7']` — the class the round-67 rule stops requiring.

## Fixtures

Each fixture is built from a committed envelope at the base revision and rewritten onto **its
own extract root** and **its own trusted run root** under scratch (e.g.
`fx-c0-structural-kind-with-path/firmware.bin_extract`, `…/run/rea/<root>/…` with
`parameters.output_directory = …/run/extract`).  The rewrite is asserted to resolve under the
round-67 rule *before* any mutation, so a fixture cannot pass vacuously.  Every expectation
checks the returned note text, not only the boolean: a failure must come from the clause the
fixture targets.

| # | fixture | spec | carrier | mutation | r67 | r50 | clause / note |
|---|---|---|---|---|---|---|---|
| 1 | base-g7581 | — | g7581 | none | pass | **fail** | `required entry with no disposition … ['dev/pts/0' …]` — the measurement the claim repairs |
| 2 | base-c6490 | — | c6490 | none | pass | pass | cable carrier: one char device, silently admitted in round 50 |
| 3 | a0-block-device-no-gap | (a) | c6490 | + block-device row, no gap | **pass** | pass | class boundary: `block-device` is not required |
| 4 | a1-block-device-with-gap | (a)+ | g7581 | + block-device row with `unpublished-entry` | fail | fail | `gap kind 'unpublished-entry' not allowed for 'block-device' entry 'dev/sda1' (allowed [])` |
| 5 | b0-fifo-with-gap | (b)-before | c6490 | + fifo row with its gap | pass | pass | the gap is admitted for a non-required class |
| 6 | b1-fifo-gap-removed | (b) | c6490 | + fifo row, gap **absent** | **pass** | pass | class boundary: `fifo` is not required |
| 7 | b2-fifo-wrong-gap-kind | (b)+ | g7581 | + fifo row with `missing-extractor-dependency` | fail | fail | `not allowed for 'fifo' entry … (allowed ['unpublished-entry'])` |
| 8 | c0-structural-kind-with-path | (c) | g7581 | symlink gap kind → `depth-limited` (path kept) | fail | fail | `structural gap kind 'depth-limited' carries a path …` |
| 9 | c1-gap-on-empty-allowed-kind | (c)+ | g7581 | `unpublished-entry` gap on a `dir` row | fail | fail | `not allowed for 'dir' entry 'bin' (allowed [])` |
| 10 | c2-foreign-kind-with-path | (c)+ | g7581 | `missing-extractor-dependency` on a symlink | fail | fail | `not allowed for 'symlink' entry 'bin/adsl'` |
| 11 | c3-pathless-foreign-kind | (c)+ | g7581 | path-less `missing-extractor-dependency` | fail | fail | `has no path and no structural allowance` |
| 12 | c4-structural-allowance-exceeded | (c)+ | g7581 | second path-less `depth-limited` | fail | fail | `structural gaps over allowance {'depth-limited': [2, 1]}` |
| 13 | c5-zero-allowance-kind | (c)+ | g7581 | path-less `unknown-chunk-handler` | fail | fail | `structural gaps over allowance {'unknown-chunk-handler': [1, 0]}` |
| 14 | d1-removal-names-char-device | (d) | g7581 | removal link → `dev/led` (char device) | fail | fail | `removal at 'dev/led' names a 'char-device' entry; removed.kinds is ['symlink']` |
| 15 | d2-removal-names-fifo | (d)+ | g7581 | removal link → fifo row | fail | fail | `names a 'fifo' entry; removed.kinds is ['symlink']` |
| 16 | d3-gapped-and-removed | (d)+ | g7581 | gap added on an entry already removed | fail | fail | `entry 'dev/log' is both gapped and removed` |
| 17 | d4-removal-outside-trusted-root | (d)+ | g7581 | link outside `parameters.output_directory`'s parent | fail | fail | `removal diagnostic without a path under the root` |
| 18 | d5-removal-names-no-row | (d)+ | g7581 | link to a path with no row | fail | fail | `removal resolves to 0 non-regular entries at 'dev/ghost'` |
| 19 | e1-char-device-new-detail | (e) | c6490 | char-device detail `247:0` → `999:9`, no gap | **pass** | **fail** | round 50's `silent` row is per-row; round 67 admits any char device |
| 20 | h1-kind-spelling-drift | (h) | c6490 | row kind `char_device` | pass | pass | unknown kinds default to not-required at function level — caught at score level by `gap_rule_ok` |

Supplementary (not numeric fixtures):

- **f-publication** — `nonregular_published` names a published regular file at the path of a
  symlink, char device, dir, fifo and block device (all five), and does **not** name a regular
  file at a path that is not a non-regular entry. The class waiver cannot materialise any
  non-regular row.
- **g-root-none** — `disposition_check(..., root=None)` fails closed
  (`no extract root: paths cannot be resolved`); losing the root cannot be traded for a waiver.

Verdict: `battery_green` — 20/20 fixtures fire as declared, both supplementary checks correct,
control reproduced with the current instrument and rule, 2/4 recomputed independently.

## Which of (a)–(d) the round-67 rule admits, and which it rejects

- **(a) block-device row, gap removed — ADMITTED.** `required.block-device` is false; a
  block-device row with no disposition passes. Not new to round 67: round 50 already had
  `required.block-device false`.  The boundary is that a block-device row may carry **no** gap —
  `allowed.block-device` is `[]`, so the recorded form of by-design non-publication is rejected
  (finding F3).
- **(b) FIFO row, `unpublished-entry` gap removed — ADMITTED.** `required.fifo` is false; the
  gap, when present, is allowed and counted. Also unchanged from round 50.
- **(c) a gap whose kind is not allowed for its entry kind — REJECTED.** Verified four ways:
  a structural kind carrying a path, a gap on a kind whose allowed list is empty (`dir`), a REA
  gap kind naming a symlink/fifo, and a path-less kind with no structural allowance; plus both
  structural allowances (`depth-limited` 1, `unknown-chunk-handler` 0) are enforced exactly.
- **(d) `MaliciousSymlinkRemoved` naming a char-device entry — REJECTED.**
  `removed.kinds` is `['symlink']`; redirecting one of g7581's three genuine removals to
  `dev/led` fails with the `removed.kinds` message, and the negative controls (a fifo target,
  an entry both gapped and removed, a link outside the trusted run root, a link to no row) all
  fail too.

So the rule is designed to admit exactly the silent, by-design absence of the device classes
(char/block/fifo/socket), and to reject every *recorded* form of misbehaviour: foreign gap kinds,
structural gaps carrying paths, allowance overruns, removals naming a non-symlink, removals that
cannot be resolved, and any publication of a non-regular path as a regular file.

Dispatch-card defect: the seat asks for "three NEW red fixtures" and then lists four, two of which
(a, b) it says must fail and then says must not fail.  Read literally as four fixtures each
expected to fail, (a) and (b) do not fire — by design.  Read per item (a/b = boundaries,
c/d = must fire), all four behave exactly as written.  Nothing in the rule is ambiguous; the
card's sentence is.

## What actually produces 4/4 (rule decomposition)

- The model differs from round 50 in exactly one `required` entry:
  `char-device: true → false`.  `allowed`, `structural`, `removed.diagnostic`,
  `removed.kinds` **and** `removed.silent` are identical.
- Flipping that single boolean back to `true` reproduces round 50 exactly: **2/4**, failing on
  `g7581`/`g7582` and `dev/pts/0…7`.  So the class waiver is the whole operative delta.
- Restoring round 50's `removed.silent` row on the round-67 rule changes no carrier (4/4 either
  way): the silent row only ever covered the two cable carriers' single `247:0`.  Its restoration
  in `7cfe83e4` is evidence-neutral, as predicted here before it landed.
- `class_disposition`, `round` and `supersedes` are **not** parsed by `gap_rule_model`
  (c1-counter.py:771): they are prose.  Only `allowed`/`required`/`structural`/`removed` bind.
- The rule must stay **claim-less**: adding `"claim": "R67-C1"` produces
  `claim 'R67-C1' != R50-C1` and would fail `b:gap_rule_ok` (the engine hard-codes `R50-C1`).

## Can the admitted classes hide a real extraction failure?

Not a content failure, but they can hide a silent loss of the node itself.  Precisely:

1. **Materialisation is caught.** `nonregular_published` (c1-counter.py:1427) compares every
   published regular file path against every non-regular row, kind-independent; fixture
   f-publication shows all five kinds named.  A device published as a regular file fails
   `nonregular_unpublished_ok` under either rule.
2. **The receipt records nothing for these rows.** On all four carriers
   `normalized_result.unpublished_entries` contains **only symlinks** (g7581/g7582 636, c6490 612,
   c6430 567) and **zero** char devices.  The 13 devices per FRITZ carrier appear in no gap and in
   no unpublished-entry list; their only record is the frozen `*.nonregular.tsv`.  So the waiver
   is not hypothetical — it formally accepts the measured silent skip.
3. **`gaps_ok` does not consult `unpublished_entries`.** `disposition_check`
   (c1-counter.py:1458) reads gaps, diagnostics and the frozen non-regular table only.
4. **The non-regular table is frozen, not re-derived.** `rederive_oracle`
   (c1-counter.py:2094) re-derives **regular files only** — `if os.path.islink(full) or not
   os.path.isfile(full): continue` (:2127) — and its docstring says device nodes are left out.
   What protects the table is `frozen_drift` (:1661) plus `_frozen_paths` (:1649): each carrier's
   `nonregular` path is a frozen path, edits under `tools/round-50/` are drift, and every frozen
   blob must be byte-identical at REV.  A table that was *wrong at the freeze* would not be
   caught by re-derivation.
5. **What still catches a real failure.** `chunks_ok` (no `extraction_failed`), `oracle_hits_ok`
   (every regular file published at its exact path/sha/size and no extra regular file),
   `depth-limited` allowance 1 (a second truncated task fails), `unknown-chunk-handler` 0,
   per-row symlink requirement, `path_shape_ok`, the removal family, and the publication check.
   None of those is weakened by the class waiver.

Residual risk, stated narrowly: for a char/block/fifo/socket row, an extractor that neither
publishes nor records the row is indistinguishable from a deliberate, by-design skip.  That is
the measured state of the 26 FRITZ char devices, so it is what the claim must accept if it wants
4/4 — but the rule text should not claim a compensating re-derivation that the engine does not
perform (F2).  Nothing here can hide the loss of a regular file, which is the claim's substance.

## Findings

- **F1 — dispatch pins are stale (not a rule defect).** The card's counter `f78ed365…` and rule
  `e66ba02…` are three disclosed corrections behind; the live pins are `5d6cc82a…` and
  `b55d5e87…`, and they agree across the file, HEAD, `claims.json` and the counter's own
  `RULE_V2_PIN`.  Any seat or gate that hard-codes the card's numbers aborts on a hash mismatch
  before doing work.  Fix the card or point it at `claims.json → instruments`.
- **F2 — the rule's justification overstates the engine.** `class_disposition` says the
  char-device class is "accounted for by the re-derived oracle table (every char-device row
  re-derived from the carrier bytes by unsquashfs)".  The pinned engine re-derives regular files
  only and explicitly leaves device nodes out.  The waiver's real compensating controls are the
  frozen table (drift-protected) and `nonregular_published`.  The prose is inert (F4), so the
  score is unaffected, but the *stated* reason is wrong and should be corrected in the next rule
  revision.
- **F3 — block-device asymmetry (latent).** `class_disposition` calls block devices
  "not-publishable-by-design, same reason" as char devices, yet `allowed.block-device` is `[]`:
  a *recorded* `unpublished-entry` gap for a block device is rejected (fixture a1) while a silent
  row passes (fixture a0).  The four carriers have zero block-device rows, so R67-C1 is not
  affected; a fifth carrier with block devices would fail on its own evidence.  Either list the
  gap kind for block devices or say explicitly that no evidenced block-device row is admissible.
- **F4 — `class_disposition`/`round`/`supersedes` are prose.** Not modelled, not validated, and
  the rule must omit `claim` because the engine hard-codes `R50-C1`.  Recorded so no later round
  treats those keys as enforced.
- **F5 — the numbered patch list omits the REA replacement.** The module docstring now says
  "patching exactly five things" and the function says "The five disclosed patches", but
  `patch_engine` also replaces `mod.rea_package_problems` (the round-67 REA re-pin).  That
  substitution *is* disclosed in `REA_PKG_R67`'s comment and in the receipt's `patches.rea_pkg`,
  so this is a documentation gap, not a hidden patch — but the enumeration should include it.
- **F6 — unknown non-regular kinds are unrequired at function level.**
  `need = required.get(kind, bool(allowed.get(kind)))` (c1-counter.py:1552) makes any kind absent
  from `required` and `allowed` optional; a spelling drift (`char_device`) would admit the row in
  `disposition_check`.  At score level `gap_rule_ok` computes `kinds_seen − allowed` and fails, so
  there is no scoring hole — recorded because the isolated function is not sufficient evidence.
- **F7 — the committed control receipt is one revision stale, and `--score` binds it anyway.**
  `.ufo/waves/round-67/l1/pre/control-dryrun.json` at HEAD was generated with counter
  `e44cacf5…` and rule `e66ba02…`; the instrument is `5d6cc82a…` and the rule `b55d5e87…`.  Its
  numbers are unchanged (2/4, `control_ok true`), so the counter's new second-conjunct binding
  passes — but the receipt the score will cite was not produced under the rule being scored.
  Either re-take it with the current pair (my `wrapper-control.json` is that run: `814f960c…`,
  differing from the committed file only in `counter` and `rule_v2_sha256`) or have `--score`
  also compare the bound receipt's rule digest.  The commit `7cfe83e4` message says "before
  records re-taken" but does not include this file in its diffstat.

## Limits

- No `--score` and no REA run: the L1 owns the data run.  Only the control path was exercised
  dynamically; the score-side GAPRULE patch was checked statically (lane-relative name resolves
  through `git show` at the freeze).
- Fixtures are data-level over the committed round-50 envelopes; block-device/fifo/socket rows do
  not exist on the four carriers and are labelled synthetic (`dev/sda1`, `dev/fifo-test`).
- The instrument and the rule both changed during the wave (four counter blobs, two rule blobs).
  This battery pins by HEAD-blob equality at run time and records the chain; if either moves
  again, `red.json` describes this run, not the later file.
- Scratch (`/fast/scratch/hyaku/kaidoku-r67/ExecRedControls`) is deleted; `red.json` records
  scratch-relative fixture paths only.
