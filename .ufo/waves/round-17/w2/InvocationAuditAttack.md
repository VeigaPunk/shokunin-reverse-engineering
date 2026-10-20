# InvocationAuditAttack — falsify report (wave 2, calibration/depth)

Target: `.ufo/waves/round-17/tools/invocation-audit.py` (483 lines, rev da64646).
Harness: `.ufo/waves/round-17/w2/audit-attack.py` — builds one throwaway git repo
per case under `tempfile.mkdtemp()`, runs the tool as `python3 -I -B TOOL --root
<repo> --rev HEAD`, compares emitted row class to an honest class. All scratch
under /tmp; nothing executed except `git` plumbing and the tool itself.

## A. Real run at the target rev

```
python3 -B .ufo/waves/round-17/tools/invocation-audit.py \
  --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
  --rev da64646adcb19c1ede7537b799b8c7d283fe43da
exit=0
```

counts: `{rows:17, exercised_match:6, labelled_unexercised:0,
unlabelled_variant:11, receipt_files:20, argv_records:74,
unreadable_receipts:0, receipt_glob_pathform_excluded:71}`

Per-row classes:

| name | SKILL.md line | class |
|---|---|---|
| interactive-r1-recovery | 447 | exercised_match (gate-results.json) |
| citation-drift | 448 | exercised_match, `row_says_unexercised:true` (r16 verification.json) |
| custody-pair | 449 | unlabelled_variant |
| quote-fidelity | 450 | exercised_match (r14 verification.json) |
| go-snapshot-inventory | 487 | exercised_match (r15 verification.json) |
| go-selection-preview | 506 | exercised_match (r16 verification.json) |
| round16-structural-controls | 507 | exercised_match (r16 verification.json) |
| go-carrier-run | 532 | unlabelled_variant |
| go-log-extract | 533 | unlabelled_variant |
| go-route-predict | 534 | unlabelled_variant |
| go-route-compare | 535 | unlabelled_variant |
| receipt-validate | 536 | unlabelled_variant |
| pins | 537 | unlabelled_variant |
| temporal-sweep | 538 | unlabelled_variant |
| invocation-audit | 539 | unlabelled_variant |
| go-buildinfo-probe | 540 | unlabelled_variant |
| round17-structural-controls | 541 | unlabelled_variant |

As expected, every round-17 row is unlabelled_variant: no round-17
verification/final receipt exists at rev (the only `*receipt*.json` files are the
8 `runs/*/receipt.json`, whose argvs are `npx rea-agents …` steps plus the
`carrier-run.py` wrapper `orig_argv` — none match a registry command). Note the
custody-pair row (SKILL.md:449) already asserts an "exercised argv retained in
`.ufo/waves/round-17/verification.json`" — a file that does not exist at rev; the
audit correctly stays unlabelled, but this is a live example of the stale-claim
pattern the C1(b) discharge relies on the audit catching later.

## B. Findings — 22/26 fixture rows misclassified or dropped

Verdicts from `audit-attack.py` (exit 1): FALSE-MATCH ×7, FALSE-LABEL ×1,
FALSE-VARIANT ×12, SILENT-OMISSION ×2. Anchors in
`.ufo/waves/round-17/tools/invocation-audit.py`.

### HIGH — audit over-credits (exercised_match/labelled where honesty demands otherwise)

- **F1 `argv` under failed/skipped steps counts as exercised.**
  `iter_exercised_argvs` (lines 227–241) harvests *any* `argv`/`orig_argv`
  list-of-strings anywhere in any eligible receipt; no exit/status/success
  gating. Fixture `argv-failed-step` (`argv` beside `"exit": 2, "error":
  "spawn failed"`) and `argv-skipped-plan` (`argv` inside `"skipped": true`)
  both yield `exercised_match`. An attempted invocation that never ran
  discharges the C1(b) obligation.
- **F2 Basename `*receipt*.json` admits provenance-free argv sources.**
  `receipt_eligible` (line 246) accepts any file whose basename contains
  `receipt` anywhere under `.ufo/` (lines 43–44). Fixture `glob-planted`:
  `.ufo/waves/round-99/w2/attack-notes-receipt.json` containing
  `{"argv":["python3","tools/never.py"]}` produces `exercised_match` for a
  command that was never run. Any seat that writes a `*-receipt.json` artifact
  (notes, drafts, attack output) silently enrolls its argv keys as exercised
  commands.
- **F3 The "unexercised" label check is a raw substring over the whole row.**
  Line 314: `"unexercised" in entry["raw"].lower()` — any column, any context.
  Fixture `label-denial`: row text "…there is no unexercised variant of this
  command" with **no matching argv anywhere** reports `labelled_unexercised`.
  To satisfy claim C1(b) "explicitly labelled as an unexercised variant" a row
  need only contain the word — denial, citation, or stray mention in the 4th
  cell all qualify. Label-gaming the M→0 metric without exercising anything.
- **F4 `orig_argv` credited as an exercised command.**
  Line 233 keys `orig_argv` into the same pool. Observation: in
  `.ufo/waves/round-17/runs/calib-shfmt/receipt.json`, `orig_argv` =
  `["python3","-I","-B","tools/carrier-run.py","--carrier",…]` — the receipt
  *producer's* command line, not the exercised child. Fixture
  `orig-argv-recorder` (child `argv` = `tools/child.py`, `orig_argv` =
  `tools/writer.py`) yields `exercised_match` for `writer`. Latent: a future
  registry row documenting `retain.py`/`carrier-run.py` by its wrapper
  spelling would be auto-credited by every receipt in the tree.
- **F5 Rows are silently dropped from the audit, not classified.**
  `parse_registry` requires `len(cells) >= 5` (line 161). A row with no
  trailing `|` (4 cells) or a truncated 3-cell row never reaches `rows[]` —
  `counts.rows` under-counts the registry and the omission is invisible in
  output. Fixture `row-shape`: two dropped rows, `counts.rows` still clean.
  Combined with F3, a registry can show "0 unlabelled" while containing
  unaudited rows.

### MEDIUM — under-credit (honestly exercised rows reported unlabelled_variant)

- **F6 Interpreter flags `-I`/`-B` are never normalized.** `normalize_tokens`
  strips only the interpreter basename (lines 187–194); same on the pattern
  side (lines 306–307). `python3 -I tools/iso.py --x` run vs `python3
  tools/iso.py --x` documented → `unlabelled_variant` (case `i-dropped`);
  partial-flag mismatch `-I -B` vs `-B` same (case `ib-combo`). This is a
  *documented* limitation — SKILL.md:539 states "-I/-B/--strict differences
  stay variants" — but it means the audit cannot tell "same command, cleaner
  doc spelling" from "genuinely different invocation," so every flag-spelling
  drift lands in the class claim C1 wants driven to 0.
- **F7 `--opt=val` vs `--opt val` never equal; `--opt=<VAL>` is inexpressible.**
  Tokens compare literally (line 217). Cases `eq-doc` (doc `=`, argv split) and
  `space-doc` (inverse) both report `unlabelled_variant` for identical
  invocations. `eq-ph`: `--limit=<N>` is a single literal token —
  `PLACEHOLDER_RE` (line 47) only matches whole tokens — so the natural
  placeholder spelling can never match `--limit=5`.
- **F8 Quoting is fragile and silent.** Quotes must be preserved in the
  registry cell for the match to hold (`doc-unquoted` → FALSE-VARIANT). An
  *unclosed* quote swallows the rest of the cell into one token with no
  diagnostic (`unclosed-quote` → FALSE-VARIANT); the tokenizer (lines 118–127)
  never reports malformed input.
- **F9 Command cell fixed at index 3; first backtick wins.**
  `parse_registry` reads only `cells[3]` (line 165) and `first_backtick_span`
  returns the *first* span (lines 148–150). Case `cmd-in-4th`: backticked
  command in the 4th cell → `command: None` → `unlabelled_variant` despite a
  matching argv. Case `decoy-first`: `tools/decoy.py` backticked before the
  real command in the same cell → the exercised `tools/real.py --run` is never
  audited. Real SKILL.md rows (447–541) put the command first, but the audit
  gives no warning when a row's command sits elsewhere.
- **F10 Basename rule creates a blind spot for real receipt files.**
  A real exercised argv inside a `receipts/` directory whose basename lacks
  `receipt` is excluded (line 246). Case `glob-blindspot` → FALSE-VARIANT.
  Lane counterpart at rev: `.ufo/rounds/interactive-r1/gate-before.json`
  contains `{"argv": ["python3",".ufo/rounds/interactive-r1/verify-recovery.py"]}`
  and is excluded — 71 files sit in `receipt_glob_pathform_excluded`, some
  argv-bearing (`git grep -l '"argv"'` lists gate-before.json,
  gate-correction-results.json, wave-validation.json, luna receipts/*.md).
- **F11 Literal `[`/`]` inside an argument corrupts the pattern.**
  Any `[` sets `tok_optional` and bracket chars are stripped (lines 128–136).
  Case `lb`: documented `--filter name[0]` becomes optional token `name0`;
  the real argv token `name[0]` can never equal it → `unlabelled_variant`
  even though the argv matches the documented command token-for-token.

### LOW — documented matcher semantics that still skew classification

- **F12 Optional-collapse credits minimal invocations.** Each bracketed token
  is independently optional (lines 214–217); `[--deep --verify]` row matches a
  bare `tools/opt2.py` argv → `exercised_match` (case `opt2`). The class cannot
  distinguish "full documented command ran" from "shortest form ran" —
  spec'd behavior, but it overstates what was exercised.
- **F13 Placeholder matches any single token, flags included; arity fixed at
  one.** `<FILE>` accepts `--delete-all` (case `ph` → FALSE-MATCH under strict
  reading) and `<ARGS>` can never match a multi-token tail (case `mt` →
  FALSE-VARIANT). Whole-token-only placeholders are the documented contract.
- **F14 Empty pattern is vacuously satisfiable.** A row whose command cell is
  just `` `python3` `` strips to `[]` and matches any interpreter-only
  normalized `orig_argv` (`["python3"]` is `sys.orig_argv` for plain
  interactive runs; case `bare-interp` → `exercised_match`). Degenerate but
  free credit.

### OK controls (correct classifications)

`i-kept`, `quoted-ok`, `label-stale-vs-exercised` (exercised beats label; the
`row_says_unexercised` flag at lines 314/322–323 is the right mitigation — the
live citation-drift row 448 exercises exactly this path), `abs-vs-rel`
(`_relpath` convergence on both sides works).

## C. Summary judgment

The audit's exercised/labelled distinction is gameable in *both* directions.
High-severity for claim discharge: any `argv` under any basename-matching JSON
counts as exercised regardless of status or provenance (F1, F2, F4), and the
label escape hatch is a bare substring (F3) — M→0 can be reached by fabrication
or accident rather than exercise. Medium-severity for calibration: spelling
drift (-I/-B, `--opt=val`, quotes, cell position, brackets) converts exercised
commands into unlabelled_variant (F6–F11), creating pressure to "fix" rows with
labels rather than evidence — which F3 then accepts uncritically. Rows can also
vanish from the audit entirely (F5). The tool's own selftest covers none of
these shapes.

Instals/updates: none (Python 3 stdlib + system git only).
Files written: `.ufo/waves/round-17/w2/audit-attack.py`,
`.ufo/waves/round-17/w2/InvocationAuditAttack.md`.
