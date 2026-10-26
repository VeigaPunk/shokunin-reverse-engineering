# R41-C2 precedence ambiguities — R41C2Eval, round 41 wave 1

Source of the text: `plans/round-41-claims.md`, `**Label precedence**` steps 1–12 (draft).
Source of the envelope structure: committed envelopes under
`corpus/evidence/round-40/c2/heldout/*/envelope.json`,
`corpus/evidence/round-40/c1/{V1,V2,L1,L2}/after.json`, and rea-agents 6.5.0
`dist/firmware/{FirmwarePublication,FirmwareReports,FirmwareFiles}.js`.

Each item states the defect class, the reading `indep-eval-v3.py` implements, the
evidence, and a wording the frozen claims can adopt. **BLOCKING** = two literal
readings give different labels on an envelope shape the v3 generator can mint;
**CLARIFY** = one reading is natural but the text does not say it; **CONFIRM** = the
text is already explicit and the code just follows it.

| # | step | class | hole |
|---|---|---|---|
| A1 | 2 | BLOCKING | `H` never defined |
| A2 | 3 | BLOCKING | "D names" — exact name or substring |
| A3 | 3 | CLARIFY | which field carries D |
| A4 | 4 | CLARIFY | `P` — run-wide or chunk-scoped |
| A5 | 4 | CONFIRM | combined sets resolved by order |
| A6 | 5 | BLOCKING | `BE = no` vs `BE = n/a` |
| A7 | 5 | BLOCKING | `-be` token vs substring |
| A8 | 5 | BLOCKING | "handler `squashfs_v4_be`" — H or the failing chunk |
| A9 | 8,9 | BLOCKING | `SR` never defined or observable-stated |
| A10 | 9 | CLARIFY | step 9 has no `P` condition |
| A11 | 9 | BLOCKING | `SR = yes` with an unrelated gap falls to step 12 |
| A12 | 10 | BLOCKING | `unpublished-entry` also covers non-symlink entries |
| A13 | 11 | CLARIFY | `clean` is handler-agnostic |
| A14 | 1 | CLARIFY | exact, case-sensitive OP/PR match |
| A15 | 12 | BLOCKING | gap kinds outside the four |
| A16 | 3 vs 4 | CLARIFY | order when dependency and body failure coexist |
| A17 | 4,11 | CLARIFY | `P` when `files` is absent rather than empty |

---

## A1 — step 2: what is `H`? — BLOCKING

**Text.** "no `squashfs_v4_*` handler in H".

**Hole.** `H` is introduced in the preamble only as "handler set". A run can carry chunk
handlers, gap handlers, and (producers other than unblob) neither.

**Resolution.** `H` = the union of `normalized_result.chunks[].handler` and
`normalized_result.extraction_gaps[].handler`, nulls ignored; when `normalized_result`
carries neither, the fallback is `raw_result.report[].reports[].handler_name` on
`ChunkReport`. Step 2 then tests `name.startswith("squashfs_v4_")`.

**Consequence worth freezing.** `unknown-chunk-handler` gaps always have `handler: null`
(`FirmwarePublication.js:286`), so an unknown chunk trips step 2 and can never reach
step 12. State that, or a v3 row for "unknown chunk" will contradict step 2.

**Frozen wording.** "H is the set of handler names in
`normalized_result.chunks[].handler` ∪ `normalized_result.extraction_gaps[].handler`
(nulls dropped)."

## A2 — step 3: "D names `sasquatch-v4be`" — BLOCKING

**Text.** "`missing-extractor-dependency` ∈ G → `dep-missing-be` if D names
`sasquatch-v4be`, `dep-missing-le` if D names `sasquatch`."

**Hole.** `sasquatch` is a substring of `sasquatch-v4be`, so a substring reading labels
every BE dependency `dep-missing-be` *and* `dep-missing-le` (first match wins only by
accident of clause order). The text also does not say what happens when D names both, or
neither.

**Resolution.** Exact set membership. `sasquatch-v4be` is tested first, because the text
names it first. Both present → `dep-missing-be`. Neither present → step 3 emits nothing
and the envelope falls through to steps 4–12 (on the observed shapes: step 12,
`unclassified`) — there is no `dep-missing-other` label.

**Frozen wording.** "D is compared by exact dependency name, never substring;
`sasquatch-v4be` is tested before `sasquatch`; a dependency gap naming neither yields no
label at step 3 and continues at step 4."

**Selftest.** `s3-LE-substring-must-not-match-be` (`sasquatch-v4be-x`),
`s3-be-substring-must-not-match-le` (`xsasquatch`), `s3-dep-both-be-first`,
`s3-dep-other-name-falls-through`.

## A3 — step 3: which field carries D — CLARIFY

**Resolution.** Union of `extraction_gaps[].dependencies[]`,
`diagnostics[].missing_dependencies[]`, and `diagnostics[].report.dependencies[]`. REA
writes the same names into all three (`FirmwareReports.js:109-119`,
`FirmwareReports.js:56-77`), so no observed envelope depends on the choice; naming the
sources stops a trimmed `normalized_result` from silently degrading to "neither".

## A4 — step 4: `P` scope — CLARIFY

**Text.** "`extractor-failure` ∈ G and P > 0", with `P` from the preamble as "published
regular files P".

**Resolution.** `P = len(normalized_result.files)` — the whole run. REA publishes only
regular files (`limitations[3]` of every receipt), and `files[]` has no gap/kind field to
exclude. On the two partial carriers the whole-run count equals the generator's own file
count (H21: 5, H22: 3), so run-wide is the reading the evidence supports. If
chunk-scoping is ever wanted it must be spelled out (`files[].original_file_range` exists,
but a multi-chunk carrier would then need a stated rule).

## A5 — step 4: combined sets — CONFIRM

"whatever other gaps or removed links accompany it" is explicit: with `extractor-failure`
and `P > 0`, partial beats depth-limited (step 7) and mixed (step 8). Covered by
`s4-partial-plus-in-tree`, `s4-partial-plus-mixed`, `s7-partial-precedes-depth`.

## A6 — step 5: `BE = no` vs `BE = n/a` — BLOCKING

**Text.** preamble: "`-be` in a recorded child argv BE (yes/no/n/a)"; step 5 requires
"BE = no".

**Hole.** A task-level failure records no child argv at all (`ExtractorExecutionErrorReport`
at `FirmwareReports.js:257-265` creates the failed stage before any chunk report exists),
and a dependency gap has none either. Treating `n/a` as `no` would relabel every
no-argv body failure as `avm-marker-be-dropped`.

**Resolution.** Only a *recorded* argv that lacks the `-be` token satisfies step 5.
`n/a` falls to step 6 (`body-extractor-failure`). Selftests `s5-boundary-no-argv`,
`b-be-token-substring-trap`.

**Frozen wording.** "BE = no requires at least one recorded child argv; BE = n/a never
satisfies step 5."

## A7 — step 5: what counts as `-be` — BLOCKING

**Hole.** A substring test on the command string is wrong twice over: `sasquatch-v4be`
carries the letters `be` but not the token `-be`, and `-no-exit-code` carries neither. A
naive `"-be" in command` is *also* wrong in the other direction for any path containing
`-be`.

**Resolution.** `shlex.split` each recorded argv (`diagnostics[].report.command`;
list form `.report.argv` / `.argv`) and require `"-be"` as its own token. Any recorded
argv for the run carrying it ⇒ `yes`.

**Frozen wording.** "`-be` is an argv token, not a substring, in
`normalized_result.diagnostics[].report.command`."

## A8 — step 5: whose handler? — BLOCKING

**Text.** "handler `squashfs_v4_be`" inside the `extractor-failure` clause.

**Hole.** `H` is run-wide; a carrier can hold an LE and a BE chunk, and only one of them
fails. Read against `H`, an LE failure next to a healthy BE chunk becomes
`avm-marker-be-dropped`; read against the failing gap, it does not.

**Resolution.** Prefer the `extractor-failure` gap's own `handler` (feature `HF`,
`extraction_gaps[].handler` where `kind == "extractor-failure"`, set from
`ChunkReport.handler_name` at `FirmwarePublication.js:292`); fall back to `H` when that
row's handler is null (task-level failure, `FirmwareReports.js:257-265`). No effect on the
26 held-out envelopes (single handler each); selftests
`b-step5-uses-failing-chunk-handler`, `b-step5-failing-chunk-is-be`.

## A9 — steps 8/9: `SR` is never defined — BLOCKING (largest hole)

**Text.** preamble: "symlink removed SR"; steps 8 and 9 consume it.

**Hole.** Nothing in the precedence says how SR is observed, and the obvious inference is
wrong: an escaping/empty-target symlink leaves **no** `extraction_gaps` row. Only an
in-tree symlink appears as `unpublished-entry`; a removed one is silently dropped from the
publication (that silence is R40-CL6/L6). Two evaluators can therefore both be "literal"
and disagree on H07/H08/H11/H12 — exactly the classes step 8 and step 9 exist for.

**Resolution.** `SR = yes` iff some `normalized_result.diagnostics[].report` has
`__typename__ == "MaliciousSymlinkRemoved"` (keys `__typename__`, `type`, `kind`, `name`
accepted), with a fallback on the same token in `raw_result.execution.stdout.text`.
Observation: H07's receipt carries
`diagnostics[0].report = {severity: "WARNING", link: ".../rsvo1-", target: ".../6a2xyp5_p", __typename__: "MaliciousSymlinkRemoved"}`
and its stdout prints the same line; H11 (mixed) carries it *and* an in-tree
`unpublished_entries[]` row; H09 (in-tree only) carries no such diagnostic. REA passes
producer reports through verbatim (`FirmwareReports.js:65-74,253-255` — anything not in
`known` becomes a diagnostic), which is why this report survives into the envelope.

**Frozen wording.** "SR = yes iff a `MaliciousSymlinkRemoved` producer report is present in
`normalized_result.diagnostics`; removal is not a gap kind."

## A10 — step 9 has no `P` condition — CLARIFY

`SR = yes`, `G = ∅`, `P = 0` ⇒ `escaping-symlink-removed`, not `clean-empty`. Kept
literal, and it is the better label: a carrier whose only entry was a symlink is not
"empty", it lost its entry. Selftest `s9-boundary-escaping-p0`. Freeze the intent so v3
does not "fix" it into `clean-empty`.

## A11 — step 9 with an unrelated gap — BLOCKING

`SR = yes` with `G = {encrypted-chunk}` (or any kind other than the ones steps 3–8 name)
matches no step: 9 needs `G = ∅`, 10 needs a singleton `unpublished-entry`, 11 needs
`G = ∅` ⇒ step 12 `unclassified`. Literal and consistent, but it means SR evidence is
*silently discarded* whenever any unrelated gap coexists. Selftest
`s9-boundary-sr-with-unrelated-gap`. Either accept `unclassified` in the frozen text or
add a row; unreachable in the current classes, which is not the same as unreachable.

## A12 — step 10: `unpublished-entry` is not only symlinks — BLOCKING (can mislabel)

**Hole.** Step 10 says `G = {unpublished-entry}` → `in-tree-symlink-metadata`, but REA
records `unpublished_entries[].kind ∈ {symlink, file, special}` (`FirmwareFiles.js:178-183`:
links are retained as metadata; device nodes land as `special`). A squashfs holding one
device node and no other gap would be labelled a symlink-metadata case.

**Resolution.** Literal: no `kind` test, because the text performs none. Flagged because
this is the one item where the literal reading can be *wrong* rather than merely
under-specified.

**Frozen wording (recommended).** "…and every `unpublished_entries[]` entry among them has
`kind == "symlink"`", or rename the label to `in-tree-nonregular-metadata`.

## A13 — step 11: `clean` is handler-agnostic — CLARIFY

`clean` fires for both `squashfs_v4_le` (H03/H04) and `squashfs_v4_be` (H01/H02) with no
gaps. That is right — the label describes the outcome, not the layout — but say so, or a
v3 row keyed on the BE handler will disagree.

## A14 — step 1: exact OP/PR match — CLARIFY

"OP ≠ `extract_firmware` or PR ≠ `unblob`" is read as a case-sensitive exact comparison;
`extract-firmware` (hyphen) is `unclassified` (selftest
`s1-op-spelling-extract-firmware`). Worth stating so a spelling drift in a carrier or a
generator is caught by step 1 instead of silently sliding into a squashfs row.

## A15 — step 12: gap kinds outside the four — BLOCKING

REA 6.5.0 emits six gap kinds: the precedence's four plus `unknown-chunk-handler` and
`encrypted-chunk` (`FirmwarePublication.js:286-287`; continuations at `:14-15`). The
precedence names only four. `unknown-chunk-handler` trips step 2 (null handler);
`encrypted-chunk` on a squashfs handler reaches step 12 (`unclassified`). Freeze the closed
set explicitly: a v3 table row invented for encrypted chunks would otherwise have no
counterpart in the evaluator, and a disagreement would read as a table defect.

## A16 — step 3 before step 4 — CLARIFY

`missing-extractor-dependency` and `extractor-failure` can coexist (a dependency gap on one
chunk, a body failure on another). The numbered order gives the dependency label even when
files were published; kept literal. State it, since "partial + dep" is a plausible v3
combined set and step 4's "whatever other gaps" sentence reads as if it outranks everything.

---

## A17 — steps 4/11: `P` when `files` is absent, not empty — CLARIFY

**Hole.** `P` is a count, so a `normalized_result` that carries no `files` array at all is
indistinguishable from one that carries `files: []`. A receipt trimmed of its file list
would then read `clean-empty` ("confirmed empty") — a claim about the image made from a gap
in the receipt.

**Resolution.** `P = len(files if isinstance(files, list) else [])`, i.e. absent reads as 0,
which is the only value the text allows; no observed envelope lacks `files` (checked: all
26 held-out and all 4 C1 dev receipts carry one), so this is a robustness boundary, not an
observed ambiguity. If v3 ever scores a receipt shape it built itself, the frozen text
should say "a `normalized_result` without `files` is `unclassified` (step 12), not
`clean-empty`" — that is the difference between "no files published" and "no publication
record".

---

## Action-map note (not a precedence ambiguity, but it blocks scoring)

`ACTION_BY_LABEL` here is total over 13 labels and includes `raise-depth` for the new
`depth-limited-nested`. The committed v2 held-out action vocabulary
(`corpus/evidence/round-40/c2/heldout/manifest.json`, `action_vocabulary`) lists eleven
actions and **has no `raise-depth`**. If v3 reuses that vocabulary, the new labels have no
expected action and the counter cannot compare actions for
`depth-limited`/`depth-limited+nested` envelopes. The freeze should extend the vocabulary
(or state that v3 maps `depth-limited-nested → raise-depth`).
