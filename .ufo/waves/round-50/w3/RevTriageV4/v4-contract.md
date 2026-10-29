# v4 contract — `tools/round-42/sqfs-triage-v4.py` and the v4 triage table, reconstructed for the v5 port

Seat RevTriageV4, round 50 attempt 2 wave 3, 2026-10-29. Read-only on the lane; every
measured value below was produced this wave (receipts in this directory).

Anchors (sha256):

| object | sha256 | note |
|---|---|---|
| `tools/round-42/sqfs-triage-v4.py` | `497bab6766a0b0c6d6f36cb58cadc531bddf9dd3231f6100bf46cf6ff552a2e9` | frozen interpreter, 2839 lines, read in full |
| `SKILL.md` at base `f890bbea` = worktree | `19046cf204ce999e5dccb1ebe86eebe9921e84ded8443dd87abc5a693fd8c974` | rule block 21 lines 526–544 |
| `SKILL.md` at C1 freeze `435d41fd` | `04a3a8657d2a3c7a76569b8f12f0589fca055d91b605c3eba77e36f34d0b132e` | differs from base by **+12 lines, all instrument-registry rows** (`git diff --stat 435d41fd f890bbe -- SKILL.md` = `12 ++++++++++++`; every hunk is a `tools/round-4x/*.py` registry row). The craft-section v4 table is byte-identical; craft line numbers 526–544 hold at the freeze, at the base and at HEAD `03f852b9629c` (`git diff --stat f890bbe HEAD -- SKILL.md` empty; worktree clean). |
| `tools/round-42/indep-eval-v4.py` (frozen evaluator) | `7a135dd36b3cab29d4dfa5b5d6dcf2199c026989549683933f4e6c1fa64dd301` | the scored R42-C2 evaluator; also kept as `.ufo/waves/round-42/w1/artifacts/R42C2Eval/indep-eval-v4.py` |
| `.ufo/waves/round-42/w1/artifacts/R42C2ControlTables/preview-precedence.py` (DEV replica) | `47a6bed5c3d49c2bf3c6b0603c57c79f9198a850f80326beb7e76ce04a6517b1` | differs from the frozen evaluator (1477 diff lines, a rewrite); carries the readable `PRECEDENCE` text and `classify()` cited below |
| `tools/round-42/c2-controls.py` | `09b3c013b84d2488c6e160ae8087ce37df9a97a8ea88f26e189e5134c1c57e07` | REF_ROWS = the 13 draft steps 2..12 encoded first-match (lines 64–161) |

Citation convention: `v4:N` = `tools/round-42/sqfs-triage-v4.py` line N; `SKILL:N` =
`SKILL.md` line N; `eval:N` = `tools/round-42/indep-eval-v4.py` line N; `rep:N` =
`preview-precedence.py` line N.

## 1. Surfaces the interpreter reads, and nothing else (v4:2-12)

1. A `SKILL.md` document: the FIRST markdown table after the FIRST line containing
   `<!-- sqfs-triage-table v4 -->` (v4:203) inside the `## Queue-drain craft` section,
   plus the closed action vocabulary on the line directly above that table.
2. REA envelopes (bare `data` object or full `{ok, data, meta}`).

It never invokes REA/unblob/sasquatch, never reads a carrier, never writes (v4:8-9).

## 2. Marker grammar and section bounds

- Craft bounds: the first `## ` heading whose text (after `## `, lowercased) starts
  `queue-drain craft` opens the section; the next `## ` heading (not `###`) closes it
  (`craft_bounds`, v4:295-309; `_is_h2` v4:291; `CRAFT_PREFIX` v4:209).
- Marker select: the first line in the section containing `MARKER`
  (`<!-- sqfs-triage-table v4 -->`) wins (v4:503-508). A second v4 block later in the
  section is dead text.
- Refusal: with NO v4 marker present, a retained `v3`/`v2`/`v1` marker
  (v4:204-206) is a refusal, exit 2, naming the version found (v4:509-517); no marker
  at all is exit 2 `absent`. A superseded table is never silently evaluated (docstring
  v4:23-28; cases `c_v3_marker_refused` v4:1419, `c_v2_marker_refused` v4:1431,
  `c_v1_marker_refused` v4:1443, `c_marker_absent` v4:1479).
- Table select: the first lstrip-`|` line after the marker (v4:519-524); consecutive
  `|` lines form the table (v4:533-536). A markerless second table never wins
  (`c_first_table_wins` v4:1567).
- Actions line: scanning upward from the table start over blank lines only, the
  nearest non-blank line must contain `<!-- sqfs-triage-actions:` (v4:526-532). One
  blank line between vocabulary and table is fine; any prose between is exit 2
  (`c_actions_line_separated_by_prose` v4:1526).
- Vocabulary grammar: tokens after the prefix up to `-->`, whitespace-separated, each
  matching `^[a-z][a-z0-9]*(-[a-z0-9]+)*$`, no duplicates, non-empty (v4:400-425,
  `_ACTION_RE` v4:280). The lane's vocabulary (SKILL:527, 15 tokens): `none
  inspect-input install-extractor-be install-extractor-le wrap-extractor-be
  cross-read-legacy isolate-residue preserve-failure salvage-partial raise-depth
  audit-symlinks expect-link-absent count-gap confirm-empty`.

## 3. Column order — 13 columns, exact header names (v4:210-212, `HEADER`)

```
label | operation | provider | handler | failing handler | gap kinds | dependencies |
-be in child argv | symlink removed | published files | action | cause | source
```

- Header comparison is case-insensitive, names exact, count exact (v4:432-436); the
  12-column v3 header (no `failing handler`) is malformed (case `c_twelve_column_table_refused`,
  v4:2279).
- Separator row: 13 cells each matching `^:?-+:?$` (v4:437-440; `_SEPARATOR_RE` v4:272).
- **Scored condition columns (9):** `operation`, `provider`, `handler`, `failing handler`,
  `gap kinds`, `dependencies`, `-be in child argv`, `symlink removed`, `published files`
  (`rule_matches`, v4:790-813, tests exactly these).
- **Output columns (2):** `label` + `action` of the first matching row
  (`classify` v4:815-820, `decision` v4:822-826).
- **Documentation-only columns (2):** `cause` (must be non-empty and contain `->`,
  v4:466-470) and `source` (non-empty, v4:471-472). They are never matched.
- Cells are split on `|` after stripping leading/trailing `|`; a literal pipe inside a
  cell is not supported (docstring Limits v4:131; `split_row` v4:312-318). Surrounding
  backticks and whitespace are stripped (`clean_cell` v4:283-288, one balanced pair).

## 4. Cell grammar per column

Shared regexes (`_regexes`, v4:270-281): name `^[A-Za-z0-9][A-Za-z0-9_.\-]*$`;
handler-cell `^[A-Za-z0-9_?*.\-\[\]]+$`; operation `^[a-z][a-z0-9_.\-]*$`; provider
`^[A-Za-z0-9][A-Za-z0-9_.\-]*$`. Everything is compared case-sensitively except the
header (docstring v4:132-133).

| column | allowed cells | parse | match |
|---|---|---|---|
| `operation` | `*` or exact token | `_parse_domain_cell` v4:383-390 | equality with feature `OP` (v4:791-792) |
| `provider` | `*` or exact token | `_parse_domain_cell` | equality with `PV` (v4:793-794) |
| `handler` | `*`, `none`, validated glob | `_parse_handler_cell` v4:361-381 | `match_glob` over **F** (v4:780-788) |
| `failing handler` | `*`, `none`, validated glob | `_parse_handler_cell(failing)` | `match_glob` over **HF** (v4:795-796) |
| `gap kinds` | `*`, `none`, exact `a`/`a+b`, contains `a+`/`a,b+` | `_parse_set_cell(contains=True)` v4:321-359 | `match_set` over **G** (v4:769-778) |
| `dependencies` | same four forms (contains form is the v4 delta) | `_parse_set_cell(contains=True)` | `match_set` over **D** (v4:797-798) |
| `-be in child argv` | `yes`/`no`/`n/a`/`*` (`BE_VALUES` v4:213) | `_parse_enum_cell` v4:392-397 | equality with `BE` (v4:799-800) |
| `symlink removed` | `yes`/`no`/`n/a`/`*` | `_parse_enum_cell` | equality with `SR` (v4:801-802) |
| `published files` | `0`/`>0`/`*` (`FILES_VALUES` v4:214) | `_parse_enum_cell` | `0` ⇔ P==0, `>0` ⇔ P>0 (v4:803-806) |

- Set cells (`_parse_set_cell`): `*`=any, `none`=empty set; exact `a+b` is **set
  equality** (an extra envelope member rejects); contains `a+`/`a,b+` is
  **superset-tolerant membership** (payload ⊆ G/D). Members match the name regex,
  must not be `none`/`*` (`RESERVED_MEMBERS` v4:215), no empty member, no repeats.
  Contains members may not themselves end in `+` (`a+b+` malformed, case v4:1239).
- `label`: non-empty name-regex token; **duplicate labels refused** (v4:455-459).
- `action`: non-empty and must be declared in the vocabulary line (v4:460-464);
  an undeclared token makes the whole run unevaluable, exit 2 — it is never a
  per-envelope mismatch.

### Glob semantics — `fnmatch.fnmatchcase`, not a custom matcher (with two guards)

- Matching (`match_glob` v4:780-788): `*` matches ANY set **including the empty set**;
  `none` matches only the empty set; any other cell matches iff **at least one member**
  of the set satisfies `fnmatch.fnmatchcase(member, pattern)` — a positive set test,
  not set equality, and there is no negation ("no handler matching p" is inexpressible,
  docstring Limits v4:139-141).
- Parse-time validation (`_parse_handler_cell` v4:361-381), both handler columns:
  1. syntax guard: must match `^[A-Za-z0-9_?*.\-\[\]]+$`;
  2. prefix guard: must begin `squashfs` (`gzip*` is a dead cell, exit 2);
  3. liveness guard: the pattern must `fnmatch.fnmatchcase`-match **≥1 of the ten
     `KNOWN_HANDLERS`** (v4:226-240, pinned to unblob 26.6.4: `squashfs_v1`,
     `squashfs_v2`, `squashfs_v2_nonstandard`, `squashfs_v3`, `squashfs_v3_ddwrt`,
     `squashfs_v3_broadcom`, `squashfs_v3_nonstandard`, `squashfs_v4_le`,
     `squashfs_v4_be`, `squashfs_v4_broadcom`). `squashfs_v9*`, `squashfs_v4_BE`
     (case), `squashfs_V4*` are all exit 2 (cases v4:1339-1371).
- `squashfs_v[123]*` is a standard fnmatch pattern (character class + trailing `*`).
  It is live (matches 7 of the 10 handlers: v1, v2, v2_nonstandard, v3, v3_ddwrt,
  v3_broadcom, v3_nonstandard) — which is exactly the F1 defect: it cannot
  distinguish the three no-reader families.
- `squashfs_v[123]` (no trailing star) is also live and matches only `squashfs_v1`,
  `squashfs_v2`, `squashfs_v3` — **it misses `squashfs_v3_ddwrt`**. Load-bearing for
  the v5 port (§9).

## 5. Feature derivation from an envelope (`features`, v4:695-752)

- Envelope readability (`envelope_data` v4:624-655): a bare object with a
  `normalized_result` dict is preferred; else the `data` member of a full
  `{ok,data,meta}` envelope if `data` is a dict; else a bare object with a string
  `operation`. An `extract_firmware` envelope must carry a `normalized_result` dict
  (exit 2 otherwise); a domain-mismatched envelope may omit it (v4:711-716,
  cases v4:1613-1645).
- `OP` = `data.operation` if str else `''`.
- `PV` = `provider.id` (dict) / `provider` (str) / `''`. (The DEV replica and the
  round-42 w1 artifacts name this feature `PR`; the frozen interpreter renamed it `PV`
  — a v5 receipt reader must not treat the names as different fields.)
- `H` (`_handler_names` v4:657-669) = every `chunks[].handler` and
  `extraction_gaps[].handler` string, nulls/empties dropped, first-seen order,
  deduplicated.
- `F` = the `squashfs`-prefixed members of H (v4:717-719).
- `HF` (`_failing_handlers` v4:671-681) = the squashfs-prefixed handlers of gap rows
  with `kind == "extractor-failure"`; **falls back to F when no such row records a
  handler** (`candidates = failing or squashfs_names`, v4:720). `--json` prints both
  F and HF so a receipt shows which set decided (docstring v4:143-145).
- `G`, `D` = the union of gap-row `kind`s and gap-row `dependencies[]` strings
  (v4:721-732). D reads gap rows ONLY (divergence from the evaluator, §7).
- `BE` (`extractor_commands` v4:596-621 + v4:733-743): every sasquatch-naming child
  argv is collected from `normalized_result.diagnostics[]` and `data.diagnostics[]`
  (each entry plus its nested `report`; keys `command`/`argv`/`args`; a string is
  shlex-split) and from any dict under `raw_result` carrying those keys; a command
  counts only if a token's basename starts `sasquatch`. `yes` if any such argv has a
  standalone `-be` token (never a substring: `-be=1` is not `-be`, case v4:1700);
  `no` if argvs exist and none has it; `n/a` if none recorded.
- `SR` (`_symlink_removed` v4:684-692): `yes` iff a `__typename__ ==
  "MaliciousSymlinkRemoved"` appears on a diagnostics entry, its nested `report`, or
  any dict under `raw_result`. **A stdout-text substring is deliberately NOT
  accepted** (docstring v4:104-109); else `no`.
- `P` = `len(normalized_result.files)`; absent list reads 0 (v4:744-745).

## 6. Row precedence and decision

- `classify` (v4:815-820) tries rules **top to bottom in table order; the first rule
  whose all nine condition cells match supplies BOTH label and action**
  (docstring v4:121-123; case `c_first_match_order` v4:1495). No tie-break exists
  beyond order; two failing handlers in HF are resolved by clause order, deliberately
  (case `c_two_failing_handlers_first_row_wins` v4:2131 and its flipped twin).
- No match ⇒ `unclassified` / `none` (v4:217-218, docstring step 13).
- Malformed anything (header, separator, cell, dead glob, duplicate label, unknown
  action, missing/misplaced vocabulary line) or an unreadable envelope ⇒ the whole
  run exits 2, never a silent non-match (v4:151-156).
- Exit codes: 0 ok (including `--table-only`), 1 ONLY for a failed `--selftest`,
  2 unevaluable (v4:183-186; `main` v4:2813-2838).
- The lane table (SKILL:530-544, 15 rows in order): container-depth-limited,
  no-squashfs-chunk, dep-missing-be, dep-missing-le, partial-body-failure,
  avm-marker-be-dropped (SKILL:535: handler `squashfs_*`, failing `squashfs_v4_be`,
  be `no`, files `0`), legacy-body-failure (SKILL:536: handler `squashfs_*`,
  **failing `squashfs_v[123]*`**, gaps `extractor-failure+`, files `0`, action
  `cross-read-legacy`), body-extractor-failure, unknown-residue, depth-limited,
  mixed-symlinks, escaping-symlink-removed, in-tree-symlink-metadata,
  clean (SKILL:543: handler `squashfs_*`, failing `*`, gaps `none`, deps `*`, be `*`,
  sr `*`, files `>0`, action `none`), clean-empty (SKILL:544).

## 7. The evaluator side — how the expected label is derived (frozen `indep-eval-v4.py`)

The evaluator reads NO table. It computes the same feature tuple from the envelope and
applies the claim's numbered precedence; the action is a **fixed label→action map**
(`rep:74-92` `ACTION_BY_LABEL`; the frozen file inlines the same pairs, eval:86-101),
so the evaluator carries no table-derived knowledge and can never produce an
(action) outside the map (rep:71-73).

Fields (rep:55-66 docstring; frozen `extract_features` eval:161): OP, PR (=PV),
H, HF, G, D, BE, SR, P as in §5, with these evaluator-side widenings —
**divergences a v5 port must decide on deliberately**:

1. **D is wider in the evaluator**: gap `dependencies[]` PLUS
   `diagnostics[].missing_dependencies[]` and `diagnostics[].report.dependencies[]`
   (rep:308-320). Interpreter D = gap rows only.
2. **SR accepts the stdout fallback in the evaluator** (`raw_result.execution.stdout.text`
   substring, rep:216-222) and rejects it in the interpreter (deliberate, R41W2C2 K8).
3. **BE sources differ**: evaluator reads `normalized_result.diagnostics[]` only
   (rep:174-191); interpreter also sweeps `data.diagnostics[]` and `raw_result`.
4. **H has a raw fallback in the evaluator** (`raw_result.report[].reports[].handler_name`
   when no chunk/gap names a handler, rep:270-283); the interpreter does not.
5. **Legacy set matcher differs**: evaluator `LEGACY_HANDLER = re.compile(r"squashfs_v[123]($|_)")`
   (eval:~118) — prefix regex, `$` or `_` after the digit; interpreter a validated
   fnmatch glob over `KNOWN_HANDLERS`. **Both match all three no-reader families**
   (`squashfs_v2_nonstandard` has `_` after `v2`; the glob has `*`). The frozen
   evaluator's selftest even pins the mis-route as expected:
   `("s6 legacy v2_nonstandard failure", …, "legacy-body-failure", "cross-read-legacy", 6)`
   (eval:564-567). The defect is shared by table AND evaluator — they agree on it
   (§8), so nothing at the base can self-detect it.
6. HF fallback to F is identical in both (`hf = {…} or squashfs`, rep:352;
   selftest `PASS A1 HF falls back to F, not H`, measured this wave).

Classification (`classify`, eval:238-283; mirror `rep:358-422`), steps in order,
first match returns, **no tie-breaks beyond order**:

1. `OP != extract_firmware or PR != unblob` → `unclassified`/`none` (step 1).
2. `F = ∅ ∧ depth-limited ∈ G` → `container-depth-limited`/`raise-depth` (step 2).
3. `F = ∅` → `no-squashfs-chunk`/`inspect-input` (step 3).
4. `missing-extractor-dependency ∈ G`: `sasquatch-v4be ∈ D` → `dep-missing-be`
   (tested FIRST — BE before LE, rep:384-388 comment; exact membership, never
   substring, because `sasquatch` ⊂ `sasquatch-v4be`); else `sasquatch ∈ D` →
   `dep-missing-le`; else fall through (step 4).
5. `extractor-failure ∈ G ∧ P > 0` → `partial-body-failure`/`salvage-partial` (step 5).
6. `extractor-failure ∈ G ∧ P = 0 ∧ BE = no ∧ squashfs_v4_be ∈ HF` →
   `avm-marker-be-dropped`/`wrap-extractor-be` (step 6; BE `n/a` never satisfies).
7. `extractor-failure ∈ G ∧ P = 0 ∧ HF ∩ legacy ≠ ∅` →
   `legacy-body-failure`/`cross-read-legacy` (step 7; legacy = the §7.5 matcher).
8. `extractor-failure ∈ G ∧ P = 0` → `body-extractor-failure`/`preserve-failure` (step 8).
9. `unknown-chunk-handler ∈ G` → `unknown-residue`/`isolate-residue` (step 9,
   deliberately before depth).
10. `depth-limited ∈ G` → `depth-limited`/`raise-depth` (step 10).
11. `SR ∧ unpublished-entry ∈ G` → `mixed-symlinks`/`audit-symlinks` (step 11).
12. `SR ∧ G = ∅` → `escaping-symlink-removed`/`expect-link-absent` (step 12).
13. `G = {unpublished-entry}` → `in-tree-symlink-metadata`/`count-gap` (step 13).
14. `G = ∅`: `P > 0` → `clean`/`none`; `P = 0` → `clean-empty`/`confirm-empty` (step 14).
15. else `unclassified`/`none` (step 15).

P absent reads 0 (`p = feats.get("P") or 0`, rep:365). The evaluator's CLI accepts a
directory of envelope subdirs, prefers `envelope.json` (or `rea-full.json` with
`--full`), and prints per-id `{label, action, step, features}` records.

## 8. What counts as a mismatch: pairs, not fields

- The scored comparison is the **(label, action) PAIR** per envelope
  (c2-controls.py:31-36: `--interp` pair vs `--eval` pair; the R43/R50 predicate
  counts `pair_mismatches` and requires `table_labels == evaluator_labels` per
  envelope — `plans/round-50-attempt2-claims.md:65-72`).
- A **label-only** mismatch happens when the table routes to a different row than the
  evaluator's step (e.g. v3-era `squashfs_v4_*` handler cells vs step 7).
- An **action-only** mismatch happens when the row's label matches but its action
  cell was swapped (the `rotated`/swapped-action controls, c2-controls.py:211-217;
  the C3 control list names a swapped-action mutant,
  `plans/round-50-attempt2-claims.md:93-94`). Because the evaluator's action is a
  fixed map, any action the table invents is either declared in the vocabulary (and
  then mismatches the map) or undeclared (and then the run exits 2 — an
  unevaluable, not a mismatch).
- The four v2ns `_ddefault` rows are a **both-field** mismatch under v5: v4 pair
  `(clean, none)` vs v5 pair `(clean-unverified, record-unverified)`.

## 9. The four v2ns `_ddefault` envelopes — measured, not assumed

Files (exact, under `.ufo/waves/round-42/w1/artifacts/R42C2ReconLegacy/envelopes/`,
one `envelope.json` per directory):

| envelope id | envelope.json sha256 |
|---|---|
| `squashfs_v2_nonstandard_squashfs_v2.0_be_ddefault` | `636f84f5964952644e551d41f79bfb56d8a9bd66e019aa8f3351c6b88f24336e` |
| `squashfs_v2_nonstandard_squashfs_v2.0_le_ddefault` | `6f21e6addf3b3f0540b6bb36074a0df5b858101ee324f95fe31f9fc993b27c1c` |
| `squashfs_v2_nonstandard_squashfs_v2.1_be_ddefault` | `55375dca76cb2c6b075bc5b390c395d5055320a75fe1175528de11e55bdd8cc2` |
| `squashfs_v2_nonstandard_squashfs_v2.1_le_ddefault` | `57bb013f784168f6a61540015c3d87e098c87b4dad6cbf43f1c90b9ed28a7f71` |

These are the only four `v2ns *_ddefault` envelopes in the lane (the recon corpus has
4 v2ns × ddefault and 4 v2ns × d1; the claim names the `_ddefault` four).

**v4 today (measured, exit 0, receipts `v4-v2ns-ddefault.json/.err` here):** all four
label **`clean` / `none`** via rule 14 (SKILL:543). Declared/observed tuple deciding it,
identical for the four: `OP=extract_firmware`, `PV=unblob`, `H=F={squashfs_v2_nonstandard}`,
`HF={squashfs_v2_nonstandard}` (fallback to F; no extractor-failure gap exists),
`G=∅`, `D=∅`, `BE=n/a` (no sasquatch argv recorded), `SR=no`, `P=4`.
Row walk: rows 1–4 refuse on handler `none` / missing gap kinds; rows 5–8 refuse on
missing `extractor-failure`; rows 9–13 refuse on G/SR; row 14 `clean` matches
(handler `squashfs_*` fnmatches `squashfs_v2_nonstandard`; `none` G; `*` D; `*` BE;
`*` SR; P=4 > 0).

**Frozen evaluator today (measured, exit 0, `indep-eval-v4-recon.json` here, n=126,
skipped=[]):** all four → `clean` / `none` / step 14. **Table and evaluator agree on
the wrong pair** — consequence for the L1: the C3 do-nothing control ("v4 table at
base → red") can only fire against the **v5 evaluator's new precedence**; the frozen
v4 evaluator will never produce the mismatch by itself.

**v5 evaluator (from the frozen claim precedence text,
`plans/round-50-attempt2-claims.md:74-83`):** `squashfs_v2_nonstandard` is a
no-independent-reader family, so step 14's clean arm routes to the new label:
`G = ∅ ∧ P = 4 > 0` → **`clean-unverified` / `record-unverified`** ("run completed,
gaps none, >0 files; uncorroborated, never clean"). The deciding fields are: family
membership (F ∩ {v2ns, v3_broadcom, v3_nonstandard} ≠ ∅), G = ∅, P > 0, plus the
unchanged domain guard OP/PV. `BE=n/a` and `HF` (fallback) are unconsulted on this
arm. The failure arm (`no-reader-failure` / `preserve-unresolved`) would need
`extractor-failure ∧ P = 0`; none of the four is in that shape — under v4 it would
have been `legacy-body-failure`/`cross-read-legacy` (F1 mis-route), under the v4
evaluator step 7 (its selftest pins exactly that, eval:564-567).

## 10. Divergences and porting constraints the v5 build must not inherit silently

1. **Docstring over-claims a refusal the code does not implement.** v4:130 and v4:154
   say a "duplicate label or handler glob" makes the run unevaluable; the code only
   refuses duplicate labels (v4:455-459). Two rows with the same handler glob parse
   fine and clause order decides. The v5 docstring/selftest must either implement the
   glob-duplication refusal or drop the claim.
2. **The reader-backed legacy set is NOT expressible as one validated v4 glob.**
   Reader-backed v1–v3 = {v1, v2, v3, v3_ddwrt}; no-reader = {v2ns, v3_broadcom,
   v3_nonstandard}. Candidate cells: `squashfs_v[123]*` = all 7 (the defect);
   `squashfs_v[123]` = {v1, v2, v3} — misses `squashfs_v3_ddwrt`; no alternation
   exists in the handler-cell grammar. A v5 row that narrows the cell must therefore
   either (a) add a second row for `squashfs_v3_ddwrt` with the same behaviour under a
   DIFFERENT label (duplicate labels are refused), or (b) extend the cell grammar
   (e.g. a comma-alternation like the set columns), or (c) change the matcher. Any of
   these is a grammar change the v5 selftest must pin; a silent `squashfs_v[123]`
   narrowing silently drops ddwrt.
3. **PR→PV rename**: artifacts at R42 w1 use `PR`; the frozen interpreter uses `PV`.
   Receipt keys must be pinned in the v5 instrument so before/after receipts stay
   comparable.
4. **Evaluator divergences (§7.1-7.5)**: a v5 evaluator "ported from
   tools/round-42/sqfs-triage-v4.py written from the claim's precedence text" (claim
   :74-83) will differ from `indep-eval-v4.py` in D/SR/BE/H sources and the legacy
   matcher. That is intended (the claim says "written from this claim's precedence
   text"), but the v5 selftest must state each choice; otherwise a green selftest can
   hide a different D than the R42 evaluator's on diagnostics-carried dependencies.
5. **Agreement on the defect**: at the base, table and evaluator agree on all four
   rows (§8/§9). The do-nothing control and the before-run's `pair_mismatches` are
   meaningful ONLY against the v5 evaluator; scoring the v4 table with
   `indep-eval-v4.py` at the base reads 0 mismatches (measured: interpreter and
   evaluator both `clean`/`none` on all four).
6. `--table-only` must be re-run after any craft-section edit (W2Skill §3 already
   flagged this); measured here: exit 0, 15 rules, marker line 526, actions line 527
   (`table-only-v4.out` here).
7. KNOWN_HANDLERS is pinned to unblob 26.6.4; a 12th handler would make narrow globs
   dead cells (exit 2) — a freeze-coupled pin the v5 must carry forward deliberately.

## 11. Receipts (exact commands, exit codes, output sha256)

| # | command (cwd = lane root) | exit | stdout sha256 | UTC (file mtime) |
|---|---|---|---|---|
| R1 | `python3 -I -B tools/round-42/sqfs-triage-v4.py --skill SKILL.md --table-only > table-only-v4.out` | 0 | `65abca784fbaafc0318df5d05eee97036081f8a1a6aff96d38b5c2cbc76c510f` | see file mtime |
| R2 | `python3 -I -B tools/round-42/sqfs-triage-v4.py --skill SKILL.md --json <4 v2ns ddefault envelope.json> > v4-v2ns-ddefault.json` | 0 | `3120ebb94f41d17b66ee373a7cb7fd940ff960c08ae8097127115e140ec07909` | see file mtime |
| R3 | `python3 -I -B tools/round-42/indep-eval-v4.py --selftest > indep-eval-v4-selftest.out` | 0 (`45/45 cases; 0 failure(s)`) | `b8971b6aaf22a93a962522b29da4e5a377c81329d7a0e6fcd333a7f801703040` | see file mtime |
| R4 | `python3 -I -B tools/round-42/indep-eval-v4.py --envelopes .ufo/waves/round-42/w1/artifacts/R42C2ReconLegacy/envelopes --out indep-eval-v4-recon.json` | 0 (n=126, skipped=[]) | `a36149a030ed18aaeee56e1f549933e88563affdb405a2d40c476f17029d0425` | see file mtime |
| R5 | `git diff --stat 435d41fd f890bbe -- SKILL.md` (read-only) | 0 | `12 insertions(+)`, all registry rows | — |
| R6 | `git show <rev>:SKILL.md \| sha256sum` for 435d41fd / f890bbe (read-only) | 0 | `04a3a865…` / `19046cf2…` | — |

No REA run, no download, no tool install, no lane mutation. Scratch removed after
receipts were copied here.
