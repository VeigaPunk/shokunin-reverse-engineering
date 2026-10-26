# R41C2Interp — v3 triage interpreter + drafted v3 table, scored against the draft claims' precedence

**DONE** — `sqfs-triage-v3.py` (marker `<!-- sqfs-triage-table v3 -->`, exact + CONTAINS `gap kinds`,
v2/v1 markers refused with exit 2, no embedded table) passes **69/69** selftest cases; the drafted
12-row v3 table agrees with the claims' `**Label precedence**` list on **10836/11520** synthetic
feature tuples and on **11520/11520 outside two documented grammar limits** (full domain), and on
**4680/5040** with **5040/5040 in-domain** (reachable domain). The frozen round-40 v2 table,
transcribed into v3 grammar, misses **482 of those 5040** reachable tuples, so the new grammar and
the new row are load-bearing rather than cosmetic.

Seat `R41C2Interp`, wave 1 (pre-freeze). Base `49096c7e6f226af0c750c4b003be58883cb6049f`.
Nothing frozen; no VCS mutation; no REA, unblob, sasquatch or other extractor was run on anything
(see §9).

---

## 1. Delivered artifacts

All under `.ufo/waves/round-41/w1/artifacts/R41C2Interp/`:

| file | bytes | sha256 | what it is |
| --- | --- | --- | --- |
| `sqfs-triage-v3.py` | 76382 | `8b68a85ae27f308e9f1e2c0ebc01a5ab843dfc28b12e5cf1a67a41346cb96052` | the interpreter: 1772 lines, 69 selftest cases |
| `sqfs-triage-v3-table.md` | 15778 | `880594199e19543f7086ad0aa3a75e50209624dd0d9923889224c48d19bbcad7` | the drafted rule block 20 with the 12-row v3 table, the step→row map and the prose repairs |
| `check-precedence.py` | 18814 | `64728e87a7a2a0b9013f57e1ba32c2f876560ba0a575616637ba34c2c7b2c751` | precedence oracle (from the claims text only) + tuple sweep driver |
| `control-v2-transcribed.py` | 2777 | `d8f3d4f0a720df14b15755e81c48987409fe884721f902bb1cfcf5fbc13cd8e6` | builds the claims' "v2 table transcribed into v3 grammar" control from `git show` |
| `cross-check-r40.py` | 3241 | `0ae5f8fb32b0773455a46e1bd79f3d6d93fc5e08fd44ca56e4627dd1c894cc7b` | runs a table on the committed round-40 C2 envelopes vs their manifest |
| `selftest-v3.txt` | 1936 | — | final `--selftest` transcript (`SELFTEST cases=69 pass=69 fail=0`) |
| `draft-table-parse.txt` | 9282 | — | `--table-only` on the draft table: 12 rules, 12 actions |
| `precedence-run-full.txt`, `precedence-check-full.tsv` | 4812 / 1722820 | — | full-domain sweep output and the 11520-line per-tuple ledger |
| `precedence-run-reachable.txt`, `precedence-check-reachable.tsv` | 4809 / 763024 | — | reachable-domain sweep output and ledger |
| `control-v2-transcribed-run-full.txt` | 14415 | — | control, full domain (exit 1) |
| `control-v2-transcribed-run-reachable.txt`, `control-v2-transcribed-reachable.tsv` | 15221 / 761906 | — | control, reachable domain (exit 1) + ledger |
| `cross-check-r40.txt`, `cross-check-r40-control-v2.txt` | 4578 / 4577 | — | 26 committed round-40 C2 envelopes: draft table vs v2 control |
| `cross-check-r40-c1.txt` | 1247 | — | the four committed round-40 C1 carriers under both tables |
| `base-skill-refusal.txt` | 201 | — | the "unmoved" command: base `SKILL.md` under the v3 interpreter |

Tooling: nothing installed or upgraded (no `pacman`, no `uv tool`, no `npx`); the task needed only
`git show`, `python3` and the already-installed packages. Scratch
`/fast/scratch/hyaku/kaidoku-r41/R41C2Interp` was removed at the end; every number below is
reproducible from the artifacts with the commands in §10.

## 2. The interpreter: what changed from v2 and what did not

`sqfs-triage-v3.py` was written from `git show 49096c7e:tools/round-40/sqfs-triage-v2.py`. Structure,
column order, envelope readability rules and exit-code discipline are the v2 ones. The deltas:

1. **Marker.** `MARKER = '<!-- sqfs-triage-table v3 -->'`. Selection rule, in order:
   (a) the first v3 marker inside `## Queue-drain craft` selects its table; (b) with no v3 marker, a
   **v2** marker in that section is **REFUSED** — `exit 2`, `refused marker '<!-- sqfs-triage-table
   v2 -->' … a superseded table is never evaluated as v3`; (c) then a v1 marker, same refusal; (d) else
   `exit 2` "marker absent". The v3-wins rule exists because `SKILL.md` keeps its v1 block (line 336)
   and its v2 block (line 361) inside the same section as history, and the L1's integrated v3 block
   must be readable with those blocks still present (`c_v3_marker_selects_its_table_over_earlier_v2_block`).
2. **`gap kinds` CONTAINS form** beside the v2 exact form: `none`, `*`, exact `a` / `a+b`, contains
   `a+` / `a,b+`. `+` joins an exact set and `,` joins a contains set, so a comma in an exact cell is a
   malformed member, never an alternate syntax. `none` and `*` are reserved members in both forms
   (`none+`, `a+none` → exit 2) so a cell cannot name a gap kind that cannot exist.
3. **`dependencies` keeps the v2 exact form**, as the seat brief specifies (`c_deps_cell_has_no_contains_form`).
4. **No embedded table.** `TABLE_BLOCK` and `--print-table` are deleted (R40-CL5 M1). `--print-table`
   is not an unknown-arg accident that still works: argparse exits 2 (`c_print_table_removed`), and
   `c_no_embedded_table` scans this module's own source for the header-row literal and for a
   `TABLE_BLOCK =` assignment.
5. `published files` keeps `0` / `>0` / `*`; duplicate labels, undeclared actions, malformed cells,
   missing/misplaced vocabulary line and unreadable envelopes are still hard `exit 2`.
6. `--json` payload keeps the v2 keys (`label`, `action`, `rule`, `row`, `features`) and `--table-only`
   keeps `rules: N` / `actions: …`, so the round-41 counter can reuse v2-shaped parsing. `_spec_text()`
   prints `any` / `none` / `exact{…}` / `contains{…}` instead of the raw tuple repr.

Copied verbatim from v2 (so a diff against the v2 file is mostly deletions):
`clean_cell`, `_is_h2`, `craft_bounds`, `split_row`, `parse_actions_line`, `_parse_handler_cell`,
`_parse_domain_cell`, `_parse_enum_cell`, `_as_list`, `_iter_dicts`, `command_tokens`,
`names_sasquatch`, `extractor_commands`, `_has_normalized_result`, `envelope_data`, `features`,
`load_envelope`, `match_set` (plus the `contains` branch), `rule_matches`, `classify`, `decision`,
`_read_skill`, `_run` (minus `--print-table`). **Feature extraction is identical to v2** — the sweep
re-derives every tuple's features through the interpreter and asserts `OP/H/G/D/BE/SR/P` equal the
tuple it wrote (§4), 11520/11520 and 5040/5040.

## 3. Selftest: 69 cases, tables built inline

`python3 -I -B sqfs-triage-v3.py --selftest` → `SELFTEST cases=69 pass=69 fail=0`, exit 0
(`selftest-v3.txt`). The selftest never reads a lane fixture: it writes synthetic SKILL variants and
synthetic envelopes into `$TMPDIR` and deletes them. Coverage, by group:

* **contains form (25)** — single-kind contains vs singleton and vs superset; pair requires both;
  pair matches a superset; triple; exact-single rejects a superset; exact-pair matches its set and
  rejects a subset; `contains` and `exact` answering differently on one tuple; `none` rejects a
  superset and accepts the empty set; `*` accepts any; `dependencies` rejects the contains form;
  malformed contains (empty member, trailing comma, repeated member, space, `a+b+`); exact comma;
  reserved words as contains and as exact members; `--table-only` printing both spec forms.
* **markers/refusals (9)** — v2 refused (stderr names v2 *and* "refused"), v1 refused, v3 wins over an
  earlier v2 block, marker absent, marker outside the craft section, no craft section, marker without
  a table, `--print-table` gone.
* **table validation (13)** — duplicate label, unknown action, missing vocabulary line, vocabulary
  separated by prose, duplicated vocabulary token, malformed header, malformed operation cell,
  malformed published-files cell, empty action, cause without `->`, cell count, first-match order,
  first-table-wins.
* **envelope features (16)** — domain guard on operation / on provider / with no `normalized_result`;
  `extract_firmware` without `normalized_result` → exit 2; unreadable envelopes (missing, `{}`, bad
  JSON, scalar); bare vs full envelope; BE `yes`/`no`/`n/a`; `-be` tokenised, not substring-matched;
  string command with a real `-be` token; `MaliciousSymlinkRemoved` from `raw_result`; `0` vs `>0`
  published files; handler `none` rejecting a squashfs chunk and matching a handler-less envelope;
  fnmatch handler; `--json` shape; CLI invocation guards.
* **combined gap sets (5)** — partial+in-tree, partial+mixed, depth-limited (alone and beside a mixed
  set), missing-dependency+extractor-failure, and `c_full_precedence_shape`, a twelve-row table shaped
  like the draft that asserts 14 tuples (including `mystery-gap` → `unclassified` and a
  domain-mismatched envelope) in one case.
* **real document (1)** — `SKILL.md` parses when a v3 block is present, and exits 2 naming a marker
  version when it is not (so the case is green both before and after the L1 integrates).

Case count by function name is 69 (`grep -c '^def c_'`); the printed total is what the run reports.

## 4. The drafted table and its agreement with the claims' precedence

`sqfs-triage-v3-table.md` carries the `## Queue-drain craft` heading (so it is a readable `--skill`
surface on its own), the numbered item 20, the v3 marker, a 12-token vocabulary ending in
`raise-depth`, the twelve v2 columns in the v2 order and twelve rows. `--table-only` reports
`rules: 12` with the vocabulary `none inspect-input install-extractor-be install-extractor-le
wrap-extractor-be preserve-failure salvage-partial audit-symlinks expect-link-absent count-gap
confirm-empty raise-depth` (`draft-table-parse.txt`).

Row order and the precedence step each row realizes:

| # | label | action | gap-kinds cell | narrowing cells | precedence step |
| --- | --- | --- | --- | --- | --- |
| 1 | no-squashfs-chunk | inspect-input | `*` | handler `none` | 2 |
| 2 | dep-missing-be | install-extractor-be | `missing-extractor-dependency+` | deps `sasquatch-v4be` | 3 |
| 3 | dep-missing-le | install-extractor-le | `missing-extractor-dependency+` | deps `sasquatch` | 3 |
| 4 | partial-body-failure | salvage-partial | `extractor-failure+` | files `>0` | 4 |
| 5 | avm-marker-be-dropped | wrap-extractor-be | `extractor-failure+` | handler `squashfs_v4_be`, BE `no`, files `0` | 5 |
| 6 | body-extractor-failure | preserve-failure | `extractor-failure+` | files `0` | 6 |
| 7 | depth-limited-nested | raise-depth | `depth-limited+` | — | 7 |
| 8 | mixed-symlinks | audit-symlinks | `unpublished-entry+` | SR `yes` | 8 |
| 9 | escaping-symlink-removed | expect-link-absent | `none` | SR `yes` | 9 |
| 10 | in-tree-symlink-metadata | count-gap | `unpublished-entry` (exact) | SR `no` | 10 |
| 11 | clean | none | `none` | files `>0` | 11 |
| 12 | clean-empty | confirm-empty | `none` | files `0` | 11 |

Steps 1 and 12 are realized by the *absence* of a matching row: every row carries exact
`extract_firmware` / `unblob` domain cells (the R39-CL1 guard), so a foreign verb or provider matches
nothing and the default pair `unclassified`/`none` is the step. `dependencies` is `*` on every row
except 2 and 3, because the precedence text reads `D` only at step 3 — a deliberate v2 change (v2's
`none` there made the clean and symlink rows reject a dependency-carrying envelope).

`check-precedence.py` writes one REA envelope per feature tuple, labels batches of 400 through
`sqfs-triage-v3.py --skill <table> --json`, and compares `(label, action)` with an oracle written from
the numbered precedence list alone. Its only non-precedence input is the label→action map, taken from
the committed round-40 `heldout/manifest.json` `label_actions` plus the claims' new
`depth-limited-nested` → `raise-depth`; the run prints all thirteen pairs so the reader can audit them.
The oracle also records which step fired, and the run prints one exemplar tuple per step. **All twelve
steps agree** (verbatim from `precedence-run-full.txt`):

```
step 1  t02880  unclassified/none                      table unclassified/none                      agree
step 2  t00000  no-squashfs-chunk/inspect-input        table no-squashfs-chunk/inspect-input        agree
step 3  t00780  dep-missing-le/install-extractor-le    table dep-missing-le/install-extractor-le    agree
step 4  t00625  partial-body-failure/salvage-partial   table partial-body-failure/salvage-partial   agree
step 5  t01204  avm-marker-be-dropped/wrap-extractor-be table avm-marker-be-dropped/wrap-extractor-be agree
step 6  t00624  body-extractor-failure/preserve-failure table body-extractor-failure/preserve-failure agree
step 7  t00720  depth-limited-nested/raise-depth       table depth-limited-nested/raise-depth       agree
step 8  t00672  mixed-symlinks/audit-symlinks          table mixed-symlinks/audit-symlinks          agree
step 9  t00576  escaping-symlink-removed/expect-link-absent table …                                  agree
step 10 t00674  in-tree-symlink-metadata/count-gap     table in-tree-symlink-metadata/count-gap     agree
step 11 t00578  clean-empty/confirm-empty              table clean-empty/confirm-empty              agree
step 12 t00768  unclassified/none                      table unclassified/none                      agree
```

Domains swept (`11520 = 2 ops × 2 providers × 5 handler sets × 12 gap-kind sets × 4 dependency sets ×
3 BE × 2 SR × 2 P`): `H ∈ {∅, {v4_le}, {v4_be}, {v3}, {v4_le,v4_be}}`,
`G ∈ {∅, {extractor-failure}, {unpublished-entry}, {depth-limited}, {missing-extractor-dependency},
{extractor-failure,unpublished-entry}, {depth-limited,unpublished-entry},
{depth-limited,extractor-failure}, {missing-extractor-dependency,extractor-failure},
{missing-extractor-dependency,depth-limited}, {mystery-gap}, {unpublished-entry,mystery-gap}}`,
`D ∈ {∅, {sasquatch}, {sasquatch-v4be}, both}`, `P ∈ {0, 3}`. The **reachable** domain (`--reachable`)
drops tuples where `D` is non-empty without a `missing-extractor-dependency` gap, because unblob
records dependencies *on* a gap, so such an envelope cannot exist: `5040` tuples.

Result: `10836/11520` agree in the full domain and `4680/5040` in the reachable domain, with **zero**
unexpected divergences (the driver exits 0 only when every mismatch is one of the two documented
grammar limits, §5). Including the two limits, agreement is `11520/11520` and `5040/5040` of what the
grammar can express.

## 5. Two documented grammar limits, and two precedence-text ambiguities

Both limits are out of the held-out envelope domain, both are counted and printed by name, and both
are written into `sqfs-triage-v3-table.md` rather than papered over.

* **K1 — a non-v4 squashfs handler** (`H = {squashfs_v3}`, `576` full-domain / `252` reachable tuples).
  Precedence step 2 labels it `no-squashfs-chunk`; row 1's handler cell `none` means "no squashfs
  handler at all", a handler cell can only match a pattern (never "no handler matching a pattern"),
  and a second row with the same label is refused (duplicate labels are exit 2). Table → `unclassified`.
* **K2 — a dependency gap naming both binaries** (`{sasquatch, sasquatch-v4be}` with
  `missing-extractor-dependency ∈ G`, `108` tuples in both domains). Precedence step 3 tests
  `sasquatch-v4be` first → `dep-missing-be`; the `dependencies` cell is exact-set by design, so no
  dependency row matches and the table falls through to whatever the other gaps match — `unclassified`
  when the dependency gap is alone, `partial-body-failure` / `body-extractor-failure` /
  `depth-limited-nested` when one of those kinds accompanies it. This is the one limit whose wrong
  answer is an *action*, not just a refusal.
  **Recommendation for the freeze:** extend the CONTAINS form to `dependencies` as well (`sasquatch+`),
  which is a two-line change in `_parse_set_cell` and closes K2 outright. I did not do it because the
  seat brief scopes CONTAINS to the `gap kinds` cell; if the freeze takes it, the same brief line and
  the table's limit note need updating together.

Precedence-text ambiguities (no table change can fix them; the freeze should state a reading):

* **Step 3 has no else branch.** `missing-extractor-dependency ∈ G` with a `D` that names neither
  binary matches no clause. The oracle continues at step 4 (and therefore lands on `unclassified` when
  nothing else fires), which the sweep shows the table agreeing with. The alternative reading —
  emit `dep-missing-*` anyway — would prescribe installing a binary that was not named.
* **Step 5 names one handler while `H` is a set.** For `H = {squashfs_v4_le, squashfs_v4_be}` the
  oracle reads "handler `squashfs_v4_be`" as *that handler is in `H`*, matching row 5's fnmatch cell;
  the sweep shows agreement. If the freeze means "`H` is exactly that singleton", both the oracle and
  row 5 must gain a singleton test.

## 6. Control: the frozen v2 table transcribed into v3 grammar

`control-v2-transcribed.py --rev 49096c7e…` lifts the v2 `TABLE_BLOCK` out of
`tools/round-40/sqfs-triage-v2.py` via `git show`, rewrites only the marker, and re-emits it as a
readable document (11 rules, 12 tokens — `raise-depth` absent, correctly reported as a note). Running
the same sweeps on it:

| domain | draft v3 table | v2 transcribed | delta |
| --- | --- | --- | --- |
| full (11520) | 10836 agree + 576 K1 + 108 K2 | 9544 agree + 576 + 108 → **1292 unexplained** (11.2 %) | 1292 |
| reachable (5040) | 4680 agree + 252 K1 + 108 K2 | 4198 agree + 252 + 108 → **482 unexplained** (9.6 %) | 482 |

Reachable-domain misses, by `oracle → control` pair (from `control-v2-transcribed-reachable.tsv`):

```
54  depth-limited-nested -> unclassified                  54  depth-limited-nested -> escaping-symlink-removed
54  dep-missing-le  -> escaping-symlink-removed           54  dep-missing-be  -> escaping-symlink-removed
50  dep-missing-le  -> unclassified                       50  dep-missing-be  -> unclassified
36  unclassified    -> escaping-symlink-removed           27  partial-body-failure -> unclassified
27  partial-body-failure -> escaping-symlink-removed      21  body-extractor-failure -> unclassified
21  body-extractor-failure -> escaping-symlink-removed    18  mixed-symlinks -> escaping-symlink-removed
 6  avm-marker-be-dropped -> unclassified                  6  avm-marker-be-dropped -> escaping-symlink-removed
 4  partial-body-failure -> avm-marker-be-dropped
```

Four distinct v2 behaviours show up, and each is one of the round-41 prose repairs:

1. **No `depth-limited` row at all** (108 tuples) → `unclassified` or the over-broad
   `escaping-symlink-removed` row. This is the new row's whole justification.
2. **Combined gap sets** (108 + 27 + 27 + 21 + 21 = 204 tuples) — v2's rows use exact gap-kind sets, so
   a dependency gap beside another kind, a partial failure beside `unpublished-entry`, or an AVM
   failure beside another kind matches nothing and lands in `unclassified` or in the `*`-gap symlink
   row. The CONTAINS form is what fixes these.
3. **The `*`-gap symlink rows over-label** (36 + 18 tuples): v2's `escaping-symlink-removed` row has
   `gap kinds = *` and `mixed-symlinks` needs an exact `{unpublished-entry}`, so an unrelated gap kind
   beside a removed link is silently read as an escaping-link story, and a mixed link image with any
   extra kind is read as a purely escaping one. The draft's rows 9/10 use `none` / exact
   `unpublished-entry` and SR as a narrowing cell instead.
4. **v2's AVM row does not constrain published files** (4 tuples): `| avm-marker-be-dropped | … |
   extractor-failure | none | no | * | * |` has `published files = *`, so a `squashfs_v4_be` failure
   that *did* publish three files and whose argv dropped `-be` is labelled `avm-marker-be-dropped`
   instead of `partial-body-failure`, contradicting precedence step 4 (P > 0 precedes step 5). The
   draft's `0` cell is exactly R40-CL5 M3's repair, and this is the concrete tuple that shows it.

## 7. Real-envelope cross-checks (dev data only)

`cross-check-r40.py` runs a table over the 26 committed round-40 C2 envelopes and compares with the
committed manifest:

* draft v3 table: **26/26 agree**; rows fired `{1,2,3,4,5,6,8,9,10,11,12, default}` — every row except
  7, which has no round-40 envelope (`cross-check-r40.txt`).
* v2 transcribed control: **26/26 agree**, rows `{1…11, default}` (`cross-check-r40-control-v2.txt`).

**Calibration finding:** the committed round-40 held-out set cannot separate v2 from v3 — both score
26/26 — because its 13 classes contain no combined gap set and no `depth-limited` envelope. The
round-41 held-out set therefore *must* carry the combined classes the claim names (partial+in-tree,
partial+mixed, depth-limited+in-tree, depth-limited+mixed, depth-limited alone), not as extra depth but
as the only part of the set that discriminates. A held-out set without them would certify v3 by scoring
v2 (this is round-40 closure D3's point restated as a measurement).

The four committed round-40 **C1** carriers are the sharpest evidence, because they are real
AVM-layout successes inside the round-40 gap rule (`gap-rule.json` allows exactly
`structural: {depth-limited: 1}` beside symlink gaps):

| envelope | H | G | BE | SR | P | v2 table | draft v3 table |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `round-40/c1/V1/after.json` | squashfs_v4_be | depth-limited + unpublished-entry | n/a | no | 697 | `unclassified`/`none` | `depth-limited-nested`/`raise-depth` |
| `V2` | squashfs_v4_be | same | n/a | no | 8 | `unclassified` | `depth-limited-nested`/`raise-depth` |
| `L1` | squashfs_v4_be | same | n/a | no | 7 | `unclassified` | `depth-limited-nested`/`raise-depth` |
| `L2` | squashfs_v4_be | same | n/a | no | 6 | `unclassified` | `depth-limited-nested`/`raise-depth` |

(`cross-check-r40-c1.txt`.) So the v2 table silently refused to label the round-40 coverage carriers
that R41-C1 is about, and the v3 draft labels them. Two consequences for the freeze worth stating in
the block's own words:

* a **Core-promoting** carrier envelope can carry a `depth-limited` gap (V1 does, within the frozen gap
  rule), and under the claims' precedence 7 such an envelope is `depth-limited-nested` — i.e. the label
  says "shallow at the carve point, rerun deeper", not "in-tree symlinks only". C2's knowledge entry
  should say that in one sentence, because it reads oddly beside a C1 row that promotes the same
  carrier.
* `P` is large (697) in that envelope, which is why row 7 is above rows 8-12 and why it must stay
  above them: otherwise the mixed/in-tree rows would win on the symlink gap alone.

`depth-limited` is not a guess. REA 6.5.0 mints it: `dist/cli-runtime/cli.js:14271-14276`
(`...normalized.depth_limited_paths.map(input_path => ({kind: "depth-limited", …}))`), with the
continuation text at `:14069` ("Rerun extract_firmware with a higher max_depth (up to 10) and a fresh
output_directory…") and `MAX_EXTRACTION_DEPTH = 10` at `:14073`. The row's cause and source cells now
carry those three citations, plus the ceiling behaviour (at depth 10 the continuation restarts the
budget from an eligible published child). `extractor-failure` is likewise minted twice by REA
(`:14259-14266` from `failed_extraction_stages` and `:14268` from chunk-level
`extraction_failed`), which is another reason the gap-kind cells are set-valued.

## 8. Findings for the freeze (ranked)

1. **Precedence step 3 needs an else clause** and **step 5 needs "∈ H" wording** (§5). Without them the
   evaluator the claim requires has to invent a reading; with them, an independent evaluator can be
   written mechanically from the text, which is what makes the independence claim real.
2. **Extend the CONTAINS form to `dependencies`** (or state that a dependency gap names exactly one
   binary). K2 is the only place where the draft's wrong answer is an incorrect *action* rather than a
   refusal, and the fix is smaller than the paragraph that documents it.
3. **Say in the C2 knowledge entry which label the round-40 C1 envelopes take**, and that
   `depth-limited` may legitimately appear on a Core-promoting carrier (§7). A reader comparing the C1
   and C2 rows will otherwise think one of them is wrong.
4. **The base-`SKILL.md` assertion must be `exit 2`, not a phrase.** The claim text says "exits 2 (no
   v3 marker)"; the interpreter exits 2 with `refused marker '<!-- sqfs-triage-table v2 -->'`
   (`base-skill-refusal.txt`, line 361 of the current `SKILL.md`). If the C2 counter at the freeze
   greps for "no v3 marker" it will fail against a correct interpreter. Either loosen the counter to
   the exit code or align the wording.
5. **Keep the v3 marker ahead of the v1/v2 blocks on integration.** The rule that a v3 marker selects
   its own table is what lets the historical blocks stay in the section; the alternative (refuse
   whenever an older marker is present) would have made the base document un-integratable.
6. **The drafted row 7 is the only row the committed evidence cannot exercise** (no round-40 envelope
   has a `depth-limited` gap). Its first real test is the round-41 held-out set; a `depth-limited`
   envelope should be generated with and without an accompanying `unpublished-entry` gap, and with a
   `P > 0` body, because those are the three cells that decide it.

## 9. Bounds honoured / what I did not do

* **No extraction run of any kind.** No REA, unblob, sasquatch, sasquatch-v4be or unpacker was
  executed; no reserved carrier (FRITZ!Box 3490/5490/5491/7560, L3/L4) and no vendor image or member
  was read, fetched or copied. Every envelope used is a committed JSON file under
  `corpus/evidence/round-40/`; every table is text I authored.
* **Independence preserved.** I did **not** read
  `.ufo/waves/round-40/w2/artifacts/R40W2C2IndepEval/eval-v2-indep.py`; my oracle comes from the
  claims' precedence prose alone, and the only other input is the committed `label_actions` map.
* **Writes** are confined to `.ufo/waves/round-41/w1/R41C2Interp.md` and
  `.ufo/waves/round-41/w1/artifacts/R41C2Interp/`; scratch lived under
  `/fast/scratch/hyaku/kaidoku-r41/R41C2Interp` with `TMPDIR` set there and is removed. No write to
  `corpus/`, `tools/`, `plans/`, `SKILL.md`, `PROVINCE.md`, `SCORECARD.md`, `SHONEN.md`, `LOG.md`, to
  `~/.local/bin`, or outside the lane.
* **No VCS mutation**: only read-only `git show` / `git rev-parse --short`. No commit, no sandbox
  clone was needed (the counter sandbox is C1's business), no `jj`.
* **Tooling changes: none.** Nothing installed or upgraded, so there is no channel/version to record;
  `python3` (stdlib only), `git` and the already-present REA/npx package tree were enough.
* **No subagents, no background jobs, no `agent://all`.**

## 10. Reproduction

```
S=/fast/scratch/hyaku/kaidoku-r41/R41C2Interp; mkdir -p "$S"; cd "$S"; export TMPDIR="$S"
A=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-41/w1/artifacts/R41C2Interp
L=/home/vgpnk/Projects/shokunin/kaidoku-shokunin

python3 -I -B "$A/sqfs-triage-v3.py" --selftest                        # 69/69, exit 0
python3 -I -B "$A/sqfs-triage-v3.py" --skill "$A/sqfs-triage-v3-table.md" --table-only
python3 -I -B "$A/sqfs-triage-v3.py" --skill "$L/SKILL.md" --table-only # exit 2, names v2
python3 -I -B "$A/check-precedence.py" --ledger "$S/lf.tsv"            # exit 0, 10836/11520
python3 -I -B "$A/check-precedence.py" --reachable --ledger "$S/lr.tsv"# exit 0, 4680/5040
python3 -I -B "$A/cross-check-r40.py"                                  # exit 0, 26/26
python3 -I -B "$A/control-v2-transcribed.py" --rev 49096c7e6f226af0c750c4b003be58883cb6049f \
        --out "$S/ctl-v2-le.md"
python3 -I -B "$A/check-precedence.py" --reachable --table "$S/ctl-v2-le.md"  # exit 1, 482 misses
python3 -I -B "$A/check-precedence.py" --table "$S/ctl-v2-le.md"             # exit 1, 1292 misses
python3 -I -B "$A/cross-check-r40.py" --table "$S/ctl-v2-le.md"              # exit 0, 26/26
```

`check-precedence.py` takes any table path, so the remaining C2 kill controls are one command each:
the catch-all table, the rotated-actions table, the no-contains table and the `*`-default table are
built by mutating the draft `.md` in a scratch copy and re-running the same sweep; the control must
lose tuples, and any control that still agrees everywhere kills C2 before the held-out run.

## 11. Known limits of this report

* My oracle follows my reading of the precedence text; where the text is silent or set-vs-singleton
  ambiguous (§5) I recorded the reading and showed the table agrees with it. A frozen evaluator written
  by another seat may resolve those two points differently — that difference is exactly what the two
  items in §8.1 are for.
* The swept domain is a finite cross-product of representative sets, not the space of all envelopes; it
  is dense where the precedence distinguishes cases (every step has an exemplar, every combined class
  in the claim has a tuple) and it deliberately includes unreachable tuples so the table's behaviour
  out of domain is measured rather than assumed.
* The `label_actions` map is a committed round-40 artifact; the round-41 held-out generator may choose
  a different action for `depth-limited-nested` (the claims name `raise-depth`, which is what the draft
  and the oracle use). [INFERENCE] If the freeze renames it, the table, the vocabulary line and the
  oracle map must move together.
