# R41C2Grammar — v3 triage grammar review before the freeze

VERDICT: **DEFECTS FOUND** — the `**Label precedence**` list (plans/round-41-claims.md:72-88) **is**
encodable as a first-match table in the draft v3 grammar (contains form `kind+`, exact comma-sets,
`none`, `*`, no default row), but two steps are **not encodable as written** (step 2's negated handler
glob; step 3's membership test on `D`) and the feature definitions the evaluator seat must implement
(BE n/a-vs-no, SR, P, H membership) are **unstated in the claims text**. (A third flag raised
mid-review — the kill rule's `*` default row control looking vacuous — was closed by the v3 counter's
strict no-row binding; see F6.) All remaining items are fixable by one-clause text/grammar amendments
before the freeze; 53 feature-tuple vectors with mechanically re-derived expected pairs are delivered
for both selftests, with 53/53 three-way agreement against the interpreter seat's independent oracle.

Axes held (godspeed): **coverage** = every precedence step and order-sensitive pair pinned by a
vector; **depth** = how much of the precedence the draft grammar actually captures (the encodability
table below); **calibration** = divergence risk between evaluator (precedence-literal), table
(first-match) and interpreter (feature extraction) on tuples outside the planned held-out classes.

## Scope and method

Read-only review; no REA/unblob run, no carrier built, no VCS mutation, nothing installed.

- Inputs: `plans/round-41-claims.md` (draft, uncommitted `??` at base 49096c7e6f226af0c750c4b003be58883cb6049f)
  lines 72-88 (precedence), 90-101 (predicate + kill rule); the wave items `R41C2Interp` (grammar
  change spec), `R41C2TableDraft`, `R41C2Eval` (action map), `R41C2Gen` (18 classes),
  `R41C2ControlTables` (control list) in `.ufo/waves/round-41/w1-spec.json`; the frozen v2 interpreter
  `tools/round-40/sqfs-triage-v2.py` (grammar `_parse_set_cell` :245-258, features :516-597, matching
  :599-634); `SKILL.md:361-375` (v2 block); round-40 closure (`corpus/lessons/round-40.md:104-115`
  R40-CL5, `round-40-verifier-spotcheck.md:89` D3) and wave-2 reviews (`R40W2C2TableReview.md` M1-M3/L1-L7,
  `R40W2C2AxisFit.md` F4-F6); the 26 observed held-out tuples
  (`.ufo/waves/round-40/w2/artifacts/R40W2C2TableReview/features-26-heldout.json.txt`); the four C1
  carrier tuples re-extracted from `corpus/evidence/round-40/c1/{V1,V2,L1,L2}/after.json`; REA 6.5.0
  sources (`dist/domain/firmware/firmwareAnalysis.js:79-99` gap enum + `dependencies` field,
  `dist/firmware/FirmwarePublication.js:57-88` files = kind `file` only, :238-313 gap minting with
  `dependencies: []` for extractor-failure/depth-limited/unpublished-entry,
  `dist/firmware/FirmwareReports.js:170-203,299-348` dependency-gap minting and kind selection);
  unblob 26.6.4 sources (`handlers/filesystem/squashfs.py:24-69` extractor + AVM branch +
  `get_dependencies` returning BOTH executables, :454-575 handler names incl. `squashfs_v4_broadcom`,
  `models.py:496-499`); `tools/round-40/c2-counter.py` (:1241-1243 the `*` default row control case).
- I did **not** read the round-40 independent evaluator (`eval-v2-indep.py` — my item does not allow
  it), any round-41 sibling artifact, or any generator class map, so the expected labels below come
  from the precedence text alone (same discipline as the evaluator seat).
- Ran: `validate-vectors.py` against `grammar-vectors.json` → first pass `ok: 52 vectors`, then
  `ok: 53 vectors, 53 unique ids, steps covered [1..12]`, exit 0, after G56 was added mid-review
  (both runs in the transcript artifact).

## The draft v3 grammar (as specified by the R41C2Interp item)

Marker `<!-- sqfs-triage-table v3 -->` + `<!-- sqfs-triage-actions: … -->` inside `## Queue-drain
craft`; same twelve columns; the `gap kinds` cell gains a CONTAINS form `kind+` / `kind1,kind2+`
("the set contains these kinds, others allowed") beside the exact-set form, `none` and `*`;
`published files` keeps `0` / `>0` / `*`; rows are first-match top to bottom; no match →
(`unclassified`, `none`); v2 marker, duplicate labels and out-of-vocabulary actions are refused
(exit 2); no embedded table copy (R40-CL5 M1). Handler cell unchanged from v2: `*`, `none`, or one
fnmatch pattern matched against **any** member of H (`rule_matches`, sqfs-triage-v2.py:608-634 — so a
handler cell is already membership-style). Dependencies cell unchanged: `*`, `none`, or an exact set.

## Encodability: which step needs order, contains, exact

| step (claims:75-88) | condition | row cells | form needed | encodable as drafted |
|---|---|---|---|---|
| 1 | OP ≠ `extract_firmware` ∨ PR ≠ `unblob` | — | implicit: every row pins OP+PV; interpreter default | yes |
| 2 | no `squashfs_v4_*` handler in H | handler | **negated glob** | **NO** (F1) |
| 3 | me-d ∈ G; D names v4be / sasquatch | gaps contains, deps **membership**, two rows be-first | contains (gaps) + **contains (deps)** | **NO** for D-both-named (F2) |
| 4 | ef ∈ G ∧ P > 0 | gaps contains `extractor-failure+`, files `>0` | contains + order | yes |
| 5 | ef ∈ G ∧ P=0 ∧ BE=no ∧ be ∈ H | gaps contains, BE `no`, files `0`, handler `squashfs_v4_be` | contains + order | yes |
| 6 | ef ∈ G ∧ P=0 | gaps contains, files `0` | contains + order | yes |
| 7 | dl ∈ G | gaps contains `depth-limited+` | contains + order | yes |
| 8 | SR=yes ∧ ue ∈ G | SR `yes`, gaps contains `unpublished-entry+` | contains + order | yes |
| 9 | SR=yes ∧ G=∅ | SR `yes`, gaps `none` | exact-empty + order | yes |
| 10 | G = {ue} | gaps exact `unpublished-entry`, SR `no` | exact singleton | yes |
| 11 | G=∅ ∧ P>0 / P=0 | gaps `none`, files `>0`/`0` | exact-empty | yes |
| 12 | else | — | interpreter default (no row) | yes |

Order-sensitive pairs (all pinned by vectors): 2<3, 2<9, 2<11b, 3be<3le, 3<4, 3<7, 4<5, 4<7, 4<8,
5<6 (via BE and via handler), 5<9, 6<7, 7<8, 7<9, 8<9, 8<10, 9-G-pin, 10-exact. Not order-sensitive:
9 vs 10, 10 vs 11 (disjoint conditions).

## Findings

**F1 (HIGH) — step 2 is not encodable: "no `squashfs_v4_*` handler in H" needs a negated handler
cell the draft grammar does not have.** The handler cell forms are `*`, `none`, pattern; `none` means
H = ∅, but the precedence's condition is "no member matches the glob". unblob 26.6.4 ships
`squashfs_v1`, `squashfs_v2(+_nonstandard)`, `squashfs_v3(+_ddwrt/_broadcom/_nonstandard)`,
`squashfs_v4_le/_be/_broadcom` (squashfs.py:101-575), and the v2 `features()` collects every handler
starting with `squashfs` (:536-541) — so H = `["squashfs_v3_le"]` is a representable tuple where the
precedence answers `no-squashfs-chunk` (vector G07) while any draft-grammar table answers `clean` or
`unclassified`. The hazard is not only the plain no-chunk case: with the step-2 row encoded as
handler `none`, an H = `["squashfs_v3_le"]` envelope carrying `extractor-failure`, P>0 falls past the
no-chunk row into the partial row (`handler *`) — the precedence says `no-squashfs-chunk` (step 2
precedes step 4), the table says `partial-body-failure`. Two resolutions:
(a) **recommended** — pin H's membership in the claims features sentence: "handler set H = the
`squashfs_v4_*` chunk handlers" (one clause). Step 2 then *is* H = ∅, the existing `none` cell encodes
it exactly, evaluator and interpreter agree by construction, and the interpreter's collection filter
changes `startswith('squashfs')` → `startswith('squashfs_v4_')` (a disclosed one-line carve-out of the
interp item's "feature extraction identical to v2"; the no-chunk row's cause prose must say "no chunk
carries a squashfs **v4** handler"). Verbatim clause for the L1 to lift (R41C2Interp's report is
frozen at its yield and asks the freeze to pick from mine): in the claims features sentence, replace
"handler set H" with "handler set H (the `squashfs_v4_*` chunk handlers; the v2 collector's
`startswith('squashfs')` narrows to `startswith('squashfs_v4_')` — disclosed)". (b) add a negated
handler cell form (e.g. `none-of:squashfs_v4_*`)
— more grammar surface, more selftests, no textual gain. Vector G07 is marked `needs-amendment`; under
resolution (a) it is withdrawn (the tuple stops being representable). G08 pins that
`squashfs_v4_broadcom` **is** a `squashfs_v4_*` member (step 2 does not fire for it) under either
resolution.

**F2 (HIGH) — step 3's "D names X" is a membership test, and the dependencies cell has no contains
form.** Two consequences. (i) *Both named*: `SquashFSExtractor.get_dependencies()` returns
`[sasquatch, sasquatch-v4be]` (squashfs.py:67-69, wired through models.py:496-499), so a host with
**neither** flavor processes a BE image into a dependency gap naming both — D = `{sasquatch,
sasquatch-v4be}` is REA-reachable, not synthetic. A precedence-literal evaluator answers
`dep-missing-be` (the first-listed branch); an exact-set deps cell matches neither row → unclassified.
Latent evaluator/table disagreement outside the planned held-out classes (the generator strips one
flavor, never both). (ii) *Prefix trap*: `sasquatch` is a prefix of `sasquatch-v4be`; "names" must be
exact element equality, never a prefix/substring test — vector G10 catches a prefix-matching
implementation. Resolution: **recommended** — extend the contains form to the dependencies cell
(`sasquatch-v4be+`), be row first; the grammar change is symmetric with the gap-kinds change the item
already specifies. Fallback — amend the text to exact sets ("D = {sasquatch-v4be} / D = {sasquatch}")
and accept that the both-missing host falls through to `unclassified`, which loses the
`install-extractor-be` action on a trivially fixable, reachable state — exactly the class of hole v3
exists to close. **Sharper consequence of the fallback, measured by R41C2Interp's three-way run:**
when the both-named dep gap is *accompanied* by `extractor-failure` (P>0) or `depth-limited`, the
exact-deps table does not stop at `unclassified` — it falls through to the partial/body/depth rows
and emits a **wrong action** (`salvage-partial`/`preserve-failure`/`raise-depth` where the precedence
says `install-extractor-be`), an action divergence on a reachable tuple, not a mere refusal. That is
why both seats recommend extending CONTAINS to `dependencies` over documenting the limit. Also pin
the neither-named fall-through in the text (vector G13: me-d ∈ G, D = ∅ →
continue to step 4; the exact deps cells produce this naturally, but the evaluator must implement the
same reading, and FirmwareReports.js:180-193 shows an unnamed-producer row with `dependencies: []` is
in the minting code, so the tuple is not purely hypothetical [INFERENCE on 6.5.0 reachability]).

**F3 (HIGH) — over-constraint traps: every cell the precedence is silent on must be `*`.** The v2
rows pin cells the v3 precedence leaves free; carrying those habits into v3 creates evaluator/table
disagreements on reachable tuples:
- dep rows: v2 pins handler (`squashfs_v4_be`/`squashfs_v4_le`), BE `n/a`, SR `no`. The precedence
  keys the dep label on **D only** (that is the R40-CL5 "dependencies decides" repair) and says
  nothing about BE/SR/P/handler. Vector G14 (broadcom handler, D = {sasquatch-v4be}) and G15 (BE=yes,
  SR=yes, P=1 — a second chunk ran sasquatch and a link was removed beside the dep gap) are
  REA-reachable and fail a v2-habit row.
- escaping row: v2's gaps cell is `*`; the precedence's step 9 requires **G = ∅** (the AxisFit L5
  repair). Vector G38 (SR=yes, G = {unknown-chunk-handler}) is REA-reachable: v2 answers
  `expect-link-absent`, the precedence answers `unclassified`.
- clean/in-tree/mixed/avm/body/partial rows: v2 pins deps `none`; the precedence is silent. Under the
  REA 6.5.0 minting the only gap kind that carries dependencies is `missing-extractor-dependency`
  (FirmwarePublication.js:254-310 mints extractor-failure/depth-limited/unpublished-entry with
  `dependencies: []`), so on every tuple that reaches steps 4-12, D = ∅ and `none` ≡ `*` — the pin is
  harmless *on reachable tuples* but unfaithful; vector G44 (constructible, unreachable-by-construction)
  pins the form check. Uniform rule for the table author: **`*` in every cell the precedence does not
  constrain; exact/contains only where it does.**

**F4 (MEDIUM) — the contains/exact asymmetry between steps 8 and 10 is faithful to the text and must
not be "uniformized".** Step 8 is membership (`unpublished-entry` ∈ G), step 10 is the exact singleton
(G = {unpublished-entry}). A table author "harmonizing" both to contains flips G46
(G = {unpublished-entry, unknown-chunk-handler}, SR=no) from `unclassified` to
`in-tree-symlink-metadata`; harmonizing both to exact breaks the combined sets G35/G38 rely on. The
claims text already states the asymmetry; the table rationale (R41C2TableDraft) should call it out
row by row.

**F5 (MEDIUM) — contains-form parser pins.** (i) For single-member cells the trailing `+` is the
*only* marker between contains and exact: `extractor-failure+` (contains) vs `extractor-failure`
(exact) decide whether combined envelopes label or fall through — a lost plus silently answers
`unclassified` on exactly the envelopes v3 exists for. The interpreter selftests must include both
spellings on the same tuple (vectors G16/G17 pair). (ii)/(iii) *Resolved by the implemented
signature (R41C2Interp, cross-confirmed below)*: exact sets keep v2's plus-join (`a`, `a+b`);
contains is the comma-joined list with one trailing `+` (`a+`, `a,b+`); `none`/`*` are reserved
words, not members. This keeps v2 tables transcribing verbatim and is the right resolution of the
separator ambiguity the item text leaves open (this review's first draft read — comma everywhere,
`+` a pure suffix operator — was the other reading; the frozen grammar text must still state the
chosen signature explicitly, since `a,b` (comma without trailing `+`) and `a+b+` are then malformed
while `a+` and `a` differ in semantics). Refuse explicitly: `a,b` (comma, no trailing `+`), `a+b+`,
`none+`, `*+`, a bare `+`, empty or repeated members, inner spaces. (iv) CTL-C2-2 (v2 table
transcribed verbatim) is unaffected under either reading: no v2 cell has a multi-member set (all gap
cells are single-kind/`*`/`none`, all deps cells single/`none`/`*`).

**F6 (raised MEDIUM → RESOLVED by the v3 counter's binding) — the "`*` default row" control.**
Raised against the v2 counter, whose `row_decisions_consistent` binding tolerates a row index on the
no-match pair (c2-counter.py:753-760): there, a trailing `*` row carrying (`unclassified`, `none`) is
behaviorally identical to the interpreter default, reaches the target, and — the kill rule stopping C2
when *any* control hits target (claims:99-101) — would spuriously kill the claim. The v2 counter's own
selftest built the control with a non-default pair for exactly that reason ("best table plus a `*`
default row instead of the domain guard", exit 1, c2-counter.py:1241-1243). **Closed mid-review by
R41C2Counter**: the v3 port binds the no-match pair strictly — `row_decisions_consistent` requires the
(`unclassified`, `none`) pair to resolve to NO row (`v == {None}`) — so a default-pair `*` row fails
that binding (their selftest case 47, exit 1) and a `*` row with a non-default pair fails `matched`
instead; both constructions fail, there is no spurious kill, and their mutation sweeps M4/M8
(relaxing, respectively unbinding, that strictness) are both killed. Residual: the claims' control
list need not pin the `*` row's pair for correctness, though stating the construction stays good
practice; and the counter's `class_expected_matches_evaluator` binding makes the generator's
cross-check load-bearing — a generator/evaluator disagreement surfaces as a claim failure, not a
silent pass (R41C2Counter's note for the L1).

**F7 (LOW) — BE must be defined, and "BE = no" must exclude n/a.** The claims name the feature
("`-be` in a recorded child argv BE (yes/no/n/a)") but never define collection. The de-facto rule is
v2 `features()` (:516-597, :439-455): commands = every recorded `command` under
normalized_result.diagnostics / data.diagnostics reports plus any `command` key in raw_result, whose
shlex-tokenized basename starts with `sasquatch`; BE = yes iff some such command has the exact token
`-be` (token equality, not substring); no iff such a command exists and none has it; n/a iff none is
recorded. Two pins matter: (i) **successful extractions record no command**, so every
clean/escaping/in-tree/mixed/dep tuple observed has BE=n/a (all 26 held-out tuples confirm) — an
evaluator reading "BE=no" as "not yes" mislabels G23 (`avm-marker-be-dropped` instead of
`body-extractor-failure`); (ii) the timeout corner: `ExtractorTimedOut` records `cmd`, not `command`
(R40W2C2TableReview verification note), so a timed-out run reads BE=n/a → body-extractor-failure
[INFERENCE: whether a timeout mints `extractor-failure` was not verified by a run]. State the
definition in the claims features sentence or cite the v2 features() rule by name.

**F8 (LOW) — SR must be defined.** SR = yes iff a report with `__typename__`
`MaliciousSymlinkRemoved` appears under normalized_result.diagnostics, data.diagnostics or anywhere in
raw_result (v2 :569-580). Pin: the removal itself records **no gap** (so SR=yes with G=∅ is the
escaping row), and an **empty-target** symlink is removed silently with no report (S118; round-40 L6)
— such an envelope is SR=no, G=∅, P>0 → `clean`.

**F9 (LOW) — P must be defined.** P = len(normalized_result.files); REA publishes only entries with
kind === "file" (FirmwarePublication.js:57-88), so len(files) **is** "published regular files" — the
precedence's qualifier is already satisfied by the field, but say so, and keep `unpublished_entries`
out of P. "P with partial publishes": step 4 is P>0 with everything else free (G18: partial + SR=yes
→ partial; the removed link is subsumed), and the escaping/mixed/in-tree/depth rows carry files `*`
(G34/G37/G40/G32) — v2 already had `*` there; do not narrow.

**F10 (LOW) — step 5's handler pin excludes `squashfs_v4_broadcom`, which shares the extractor and
the AVM-marker branch.** A broadcom-magic marker image (BE=no, ef, P=0) answers
`body-extractor-failure`/`preserve-failure` under the precedence (vector G50) although its cause is the
same handshake. Synthetic population; do not widen the row — disclose broadcom in the entry's Limits
next to the existing not-covered list.

**F11 (LOW) — the action map is not in the frozen text yet.** The precedence determines labels; the
(la­bel → action) map lives in the R41C2Eval item prompt and (per label) in the table's action column.
Add one clause to the claims (or state the map in `corpus/knowledge/2026-10-26-r41-sqfs-triage-v3.md`)
so the pair is determined by frozen text alone, and record that the vocabulary grows to 12 tokens
(v2's 11 + `raise-depth`).

**F12 (INFO) — does `dependencies` decide anything? Yes — exactly one branch, and only there.** D
decides the step-3 label (be vs le). On every REA-reachable tuple D is a function of the handler's
resolved extractor plus the host environment (be-family → {sasquatch-v4be}, le-family → {sasquatch},
neither installed → both), and D ≠ ∅ ⟺ `missing-extractor-dependency` ∈ G (only dep gaps carry
dependencies). Consequence for calibration: a shortcut table keying the dep rows on the handler
instead of D still scores the full held-out set (the generator never builds a broadcom or both-missing
carrier) — the R40-CL5 repair is verifiable **only** on selftest vectors (G12/G14), not on the scored
set. Say this in the entry's Scoring paragraph; it is the honest form of "dependencies now decides".

**F13 (INFO) — step 1 is implicit and its pair coincides with the no-match pair.** Every row pins
OP/PV; a domain-mismatched envelope matches nothing and takes the interpreter default
(`unclassified`, `none`) — the same pair as step 12 (round-40 L7, disclosed). Vectors G01-G03/G55 pin
it; the counter separates the two only via the row index, not the scored pair.

**F14 (INFO) — step 5 still conflates two populations (inherited, disclosed).** A doctored marker on
a standard-BE body and a *damaged genuine AVM body* share step 5's entire feature tuple; the
(label, action) pair cannot separate them without a layout feature the envelope does not carry. The
round-40 M2/M3 repairs are prose-side (cause + Limits) and unscored; the v3 precedence inherits the
conflation. Keep the disclosure; do not add a layout column to v3.

**Cross-confirmation (R41C2Interp, received after this review's first pass).** The interpreter seat's
exhaustive synthetic-tuple sweep (11,520 tuples) agrees with the claims' precedence on 10,836 and
diverges on exactly the two families this review flags as HIGH — its K1 (non-v4 squashfs handler in H
= F1) and K2 (dependency gap naming both binaries = F2) — and its draft 12-row table is
precedence-exact outside those limits. It independently recommends extending the contains form to the
`dependencies` column (F2's recommended resolution). Its implemented signature resolves F5(ii)/(iii)
as recorded above. Two follow-ups for the L1: (1) pick F1's resolution — the H-pin (text clause +
disclosed one-line filter carve-out) makes K1 vanish without grammar change, otherwise the negated
handler form is the faithful encoding; (2) interface check with R41C2Counter — the v2 counter's
`--table-only` parser expects `{"rules": [{index, label} …]}` JSON or `N. label` lines
(c2-counter.py:352-363), while the v3 interpreter prints `rules: N` / `actions: …` prose lines; the
v3 counter must agree on the shape or lose the row-index fallback.

**Second exchange — R41C2Interp ran the 52 vectors three-way** (its interpreter + draft table vs my
`expected` vs its own independent oracle `check-precedence.py`, written from the same 12-step text
without reading my file): **my expected and its oracle agree on all 52** — the two independent
readings of the precedence text coincide; its interpreter+table agree on 49/52, with the three
divergences exactly the ones this review marked: G07 = K1/F1 (`needs-amendment` as tagged), G12 = K2/F2
(`needs-amendment` as tagged), and G44 — which is a **recipe artefact, not a table difference** (its
table, its oracle and my expected all answer `clean/none`; only my `envelope_recipe` could not realize
G=[] with D=['sasquatch']). Fixed: the JSON's envelope_recipe now carries the kindless-gap escape
hatch (`{'dependencies': [...]}` with no `kind` key — features() reads kind and dependencies
independently; REA never mints such a gap). Its parser pins are **executed and enforced in both
directions**: `a,b` → exit 2 malformed member; `a+b+` → exit 2 malformed contains member; `none+`/`*+`
→ exit 2 reserved word; `+`/`a,,b+` → exit 2 empty contains member; `a,a+` → exit 2 repeats; `a b+` →
exit 2 malformed member; valid forms `a+`→contains{a}, `a+b`→exact{a,b}, `a,b+`/`a,b,c+`→contains —
so the lost-plus hazard is refused, not silently reinterpreted, and `a+` vs `a` is pinned by its
`c_contains_versus_exact_differ` selftest (my F5(i)). Its interface measurement **resolves my
heads-up**: `--table-only` keeps v2's exact line shape (`marker line: … rules: N`, `actions: …`, then
`1. label` at column 0); exec'd against the v2 counter's own `parse_table_only` it returns 12
label→row pairs, 1-based, identical to v2 — `infer_index_base` keeps voting +1 and
`row_source='table_only'` survives; relayed to R41C2Counter as "port the two-branch parser
unchanged". Its dep rows carry handler `squashfs_v4_*` (the v4 glob) rather than `*` — equivalent
given row 1 sits above (the difference only shows inside the K1 family) and self-documenting; its G14
bonus stands: v2's dep rows pinned exact handlers (`squashfs_v4_be`/`_le`) and would have missed a
broadcom handler, so v3's glob + D-keying is what makes G14 label at all. It also supplies the
depth-limited minting citation I had only via the schema and `FirmwarePublication.js:254-310`:
per R41C2Interp, REA 6.5.0 mints `depth-limited` at `dist/cli-runtime/cli.js:14271-14276` from
`normalized.depth_limited_paths`, with `MAX_EXTRACTION_DEPTH = 10` at `:14073` (their measurement; not
re-verified here). One residual ambiguity its run exposed and my vector set did **not** discriminate:
step 3's neither-named reading (fall-through vs immediate-unclassified) — G13 answers `unclassified`
under *both* readings, so it cannot tell them apart; added vector **G56** (me-d ∈ G, D = ∅, ef ∈ G,
P=2 → `partial-body-failure` under the documented fall-through, `unclassified` under the
immediate-unclassified reading) to pin it; the JSON now carries 53 vectors, validator exit 0. G24
already discriminates step 5's set-vs-singleton reading (H = {be, le}: membership → `avm-marker-be-dropped`,
equality → `body-extractor-failure`).

**Convergence closure (third exchange).** R41C2Interp verified G56 against its draft table — row 4
fires after rows 2/3 decline on the exact deps cells — and its frozen sweep ledger already carries the
same tuple at P=3 (`precedence-check-reachable.tsv:387`, t00387, oracle = table = agree) with the P=0
sibling t00386 pinning the step-4/6 split on that exact gap set; G44 now realizes through the kindless
gap and answers `clean/none` via row 11 on all three sources. Final state: **53/53 agreement** across
its interpreter + draft table, these vectors, and its independent oracle; the only remaining deltas
are the two documented grammar limits (K1 non-v4 handler, K2 both-named dependency) and the two freeze
decisions above (F1's H-pin with the verbatim clause; F2's deps-CONTAINS extension, argued from the
measured wrong-action consequence). Its artifacts are frozen at digest (`sqfs-triage-v3-table.md`
`880594199e1954…`, interpreter `8b68a85ae27f30…`). Its final handoff adds three calibration numbers
for the freeze record: agreement with the claims' precedence is 10,836/11,520 over the full synthetic
space and **4,680/5,040 over the REA-reachable subspace** (100% outside K1/K2); the frozen v2 table
transcribed into the v3 grammar (control CTL-C2-2) **misses 482/5,040 reachable tuples** — the
combined-class repair is load-bearing, so that control fails non-trivially; and **both** the v2 and
the draft v3 table score 26/26 on the committed round-40 C2 envelopes, so the v2 13-class held-out
set cannot discriminate v2 from v3 — the five combined classes are what the R41-C2 score is about
(the D3 depth argument, now measured).

**Provenance and counter precision (fourth exchange).** R41C2Interp pins the 482/5,040 figure's
provenance: it is from its run of the v2 `TABLE_BLOCK` lifted via
`git show 49096c7e:tools/round-40/sqfs-triage-v2.py` with only the marker rewritten (its artifacts
`control-v2-transcribed-run-reachable.txt` + `control-v2-transcribed-reachable.tsv`, exit 1 by
design; reproducible via `control-v2-transcribed.py --rev 49096c7e… && check-precedence.py
--reachable --table <out>`) — if the claims' control list numbers it differently from `CTL-C2-2`, the
citation follows the claims' numbering; the control's *content* is what matters. R41C2Counter
confirms the parser relay was already the case (v2 `parse_table_only` ported byte-for-byte, measured
on real bytes: 11 label→row pairs 1-based off the real v2 interpreter's `--table-only`,
`infer_index_base` voting +1, `--json` entries parsing verbatim) and that its strict no-match binding
(F6, above) plus the load-bearing `class_expected_matches_evaluator` binding close the spurious-kill
and silent-pass risks respectively; it does not import these label-semantics vectors into the counter
battery (the counter owns table↔evaluator agreement, not label semantics).

## Recommended v3 row list (the encoding the vectors validate)

No default row; interpreter default (`unclassified`, `none`). `*` in every cell the precedence is
silent on (F3). Contains (`…+`) where the precedence says ∈; exact where it says =; `none` where it
says ∅.

| # | label | op | provider | handler | gap kinds | deps | -be | SR | files | action |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | no-squashfs-chunk | `extract_firmware` | `unblob` | `none` | `*` | `*` | `*` | `*` | `*` | inspect-input |
| 2 | dep-missing-be | `extract_firmware` | `unblob` | `*` | `missing-extractor-dependency+` | `sasquatch-v4be+` | `*` | `*` | `*` | install-extractor-be |
| 3 | dep-missing-le | `extract_firmware` | `unblob` | `*` | `missing-extractor-dependency+` | `sasquatch+` | `*` | `*` | `*` | install-extractor-le |
| 4 | partial-body-failure | `extract_firmware` | `unblob` | `*` | `extractor-failure+` | `*` | `*` | `*` | `>0` | salvage-partial |
| 5 | avm-marker-be-dropped | `extract_firmware` | `unblob` | `squashfs_v4_be` | `extractor-failure+` | `*` | `no` | `*` | `0` | wrap-extractor-be |
| 6 | body-extractor-failure | `extract_firmware` | `unblob` | `*` | `extractor-failure+` | `*` | `*` | `*` | `0` | preserve-failure |
| 7 | depth-limited-nested | `extract_firmware` | `unblob` | `*` | `depth-limited+` | `*` | `*` | `*` | `*` | raise-depth |
| 8 | mixed-symlinks | `extract_firmware` | `unblob` | `*` | `unpublished-entry+` | `*` | `*` | `yes` | `*` | audit-symlinks |
| 9 | escaping-symlink-removed | `extract_firmware` | `unblob` | `*` | `none` | `*` | `*` | `yes` | `*` | expect-link-absent |
| 10 | in-tree-symlink-metadata | `extract_firmware` | `unblob` | `*` | `unpublished-entry` | `*` | `*` | `no` | `*` | count-gap |
| 11 | clean | `extract_firmware` | `unblob` | `*` | `none` | `*` | `*` | `no` | `>0` | none |
| 12 | clean-empty | `extract_firmware` | `unblob` | `*` | `none` | `*` | `*` | `no` | `0` | confirm-empty |

Rows 2/3's deps cells need the F2 amendment (contains on the dependencies column); with exact cells
the table is precedence-correct on every tuple except G12 (both named). Rows 4-12 are encodable as
drafted. Rows 9-11 keep SR `no`/`yes` pins that are order-equivalent to `*` — kept for readability;
if rows are ever reordered, `*` is the safe form.

## The vectors artifact

`artifacts/R41C2Grammar/grammar-vectors.json` — 53 feature-tuple vectors, each with the full tuple
(OP, PR, H, G, D, BE, SR, P), the expected (label, action) from the precedence text, the deciding
step, order pins, the boundary it pins, an origin tag (`rea-observed` with the exact committed
carrier where one exists — G01/G04/G09/G10/G16/G21/G22/G29/G33/G36/G39/G41/G43 are exact observed
tuples incl. C1's L2 and held-out H01/H04-H26 shapes — `rea-reachable`, `synthetic-only`,
`unreachable-by-construction`), and a `draft_grammar` tag (`encodable` / `needs-amendment` with the
amendment named). Header documents the feature definitions, the three documented resolutions, an
envelope recipe for realizing any tuple as a synthetic REA-shaped envelope, the action map and the
12-token vocabulary. `validate-vectors.py` re-derives every expected pair from a direct transcription
of steps 1-12 and checks structure: **53/53 agree, all 12 steps covered, exit 0** (final run; the
52-vector first pass is in the transcript).

Coverage of the 18 planned held-out classes (claims:93-95, R41C2Gen): clean G41/G42, clean-empty G43,
escaping G36/G37, in-tree G39/G40, mixed G33/G34, dep-be G09/G11/G15, dep-le G10, avm G21/G26/G53,
body G22/G23/G25/G27/G50, partial G16/G20, no-chunk G04/G05/G06/G47, out-of-domain G01/G02/G03/G55,
partial-in-tree G17, partial-mixed G18, depth-limited-alone G28, depth-limited-in-tree G29 (exact C1
L2 tuple), depth-limited-mixed G30. Every order-sensitive pair listed above has ≥ 1 vector.

Consumption: the evaluator seat feeds tuples through `indep-eval-v3.py`'s precedence implementation;
the interpreter seat realizes each tuple as a synthetic envelope (recipe in the JSON header), runs
its draft v3 table, and compares pairs. Filter on `draft_grammar` until the F1/F2 amendments land;
`needs-amendment` vectors are expected to fail under the unamended draft grammar — that failure is
the finding, not a bug in the seat.

## Verification

- `python3 -I -B validate-vectors.py` (cwd scratch) → final run `ok: 53 vectors, 53 unique ids, steps
  covered [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]`, exit 0 (52-vector first pass also in the
  transcript).
- C1 carrier tuples re-extracted read-only from committed `after.json`: V1/V2/L1/L2 all
  `H=[squashfs_v4_be], G=[depth-limited, unpublished-entry], D=[], SR=no, P=697/8/7/6` — G29 is L2's
  exact tuple; v2 labels all four `unclassified` (AxisFit F6), v3 labels them
  `depth-limited-nested`: the concrete depth delta the entry's Scoring paragraph should cite.
- No REA/unblob run, no carrier built, no reserved image touched, no VCS mutation, no pacman
  transaction, nothing installed/upgraded (tooling record: empty).

## Residual risk and verification gaps

- The step-3 both-named tuple (G12) and the unnamed-dependency tuple (G13) rest on source reading
  (unblob `get_dependencies`, REA `dependencyRows`), not on a measured run; both are outside the
  planned held-out classes, so the scored predicate is unaffected either way.
- Whether the held-out generator can produce H with two squashfs chunks (G24) or a broadcom carrier
  (G08/G14/G50) is generator-owned; those vectors are `synthetic-only` and pin the grammar, not the
  score.
- The F1 resolution changes the interpreter's handler-collection filter; the interp item's "feature
  extraction identical to v2" clause needs the disclosed carve-out, and the no-chunk row's cause prose
  must drop the plain-"squashfs handler" wording.
- I did not verify REA's `depth-limited` minting conditions beyond the schema and minting site (the
  recon-depth seat owns the measured tuples); my depth vectors use its stated hypothesis shape.
