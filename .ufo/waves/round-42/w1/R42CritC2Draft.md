# R42CritC2Draft — attack on the round-42 C2 draft (R42-C2, SquashFS triage v4)

**VERDICT: DEFECTS FOUND** — the draft's C2 claim is not yet a sound depth claim. The
handler-family widening is mostly a re-score of the v3 rules on new inputs (quality), with exactly one
genuinely new decision row (step 6); that row is real but uncited and its machine-readable partition is
undefined. The anti-enumeration target (`lookup_combo_below_half`) is degenerate: a do-nothing control
satisfies it, so it binds nothing; and the legacy class universe (built from a small fixture pool) is
enumerable by a named-class lookup, so the widened combo family as designed will not defeat one. The
`dep-missing-le` label for a big-endian v3 chunk is CONFIRMED correct (source + real REA envelope). All
five seat questions answered below with concrete predicate changes.

Note: this report attacks the draft; the L1 integrates. I wrote only this report, the artifacts dir
`artifacts/R42CritC2Draft/` and scratch. No REA/unblob run touched a reserved carrier — every REA run
below is on unblob 26.6.4 SquashFS test fixtures (designated development inputs for C2) or scratch copies
of them. No tools installed/upgraded (no pacman, no writes to `~/.local/bin` or any PATH dir); used
existing `npx -y rea-agents@6.5.0` cache, `unblob` 26.6.4, `unsquashfs` 4.7.5, `7z`. `git` read-only
only (none actually needed). All REA runs had cwd = scratch so `unblob.log` lands there.

---

## 1. Q1 — is a table extended to v1–v3 handlers a depth move or a re-score of v3?

**Verdict: as drafted it is a re-score of v3 (quality work), not a depth move, except for one new row
(step 6) that is not yet sourced or machine-specified.**

Evidence:

- The v4 precedence (draft, `plans/round-42-claims.md:71-86`) differs from the frozen v3 precedence
  (`plans/round-41-claims.md` `**Label precedence**`) in only three places:
  1. step 2's test changes from "no `squashfs_v4_*` handler in H" to "F = ∅" (F = `squashfs_*`
     handlers). This is the R41-CL4 fix (v1–v3-only chunks mislabeled `no-squashfs-chunk`). It changes
     what an *old* decision returns, it does not add a decision.
  2. step 3 changes from exact-set dependency cells to membership ("D holds"). This repairs the R41-W2
     F1 cause-cell falsehood. Same two labels/actions.
  3. step 6 is a NEW (label, action) pair: `legacy-body-failure` / `cross-read-legacy`. This is the
     only new decision in the table.
- Every other step (4–12) is the v3 decision on a widened handler domain. That is precisely "re-scoring
  a rule the lane already holds on new inputs" — prompt §9 says that is quality work, never depth.
- AXES.md depth = "decision tables with real thresholds, named error signatures, cited sources". The one
  new decision has no cited source in the draft (see Q2) and no machine-readable handler partition. So
  the depth increment is currently neither sourced nor implementable as written.

**Concrete predicate changes:**

- (P1) Reframe the claim honestly: name the move "re-score of the v3 triage across the v1–v3 handler
  family (R41-CL4/R41-CL1/R41-CL2 fixes) plus one new decision row (`legacy-body-failure`)". If the
  round's depth obligation is to be met, the claim must carry a second genuinely new, sourced decision —
  or explicitly declare the round's depth kernel to be step 6 only, with the rest scored as quality.
- (P2) Do not claim "new table" as depth by itself; the freeze-integrity/`v4 marker` mechanics are
  scaffolding, not decision content.

## 2. Q2 — is step 6 (`legacy-body-failure`, `cross-read-legacy`) a real decision or a renamed body-failure?

**Verdict: it is a real decision, not a renamed `body-extractor-failure` — but it is uncited, its
handler partition is not machine-readable, and its action (cross-read) has reader-coverage limits.**

Evidence (real decision):

- unblob 26.6.4 `handlers/filesystem/squashfs.py` (S112): only the `Endian.BIG, 4` branch enters the
  AVM marker check and resolves `sasquatch-v4be` (lines 40-50); every v1–v3 chunk — BE or LE — resolves
  plain `sasquatch` and always appends `-be` (line 51-52) or `-le` (line 53-54). Therefore a v1–v3
  failure **cannot** be a byte-order handshake artifact: there is no AVM/marker/dropped-`-be` state for
  v<4, so the v4 `avm-marker-be-dropped` row and the `body-extractor-failure` handshake reasoning do
  not apply. The draft's "[the AVM layout pre-check does not apply to a v1–v3 superblock]" is correct.
- The action differs operationally: `preserve-failure` keeps the failing command and never re-runs;
  `cross-read-legacy` explicitly calls a second reader (`unsquashfs`) to split "extractor build fault"
  from "image damage" — a different repair branch.
- Reachability proven with a real envelope: I zeroed the inode-table region of the pinned v3 LE fixture
  (offsets 132..179) and ran
  `cd $S && REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob npx -y rea-agents@6.5.0 extract-firmware --format json --full-output <damaged fixture> <fresh outdir>`.
  Result (ev `artifacts/R42CritC2Draft/probes/rea-v3le-damaged.json`): `chunks[0].handler =
  squashfs_v3`, `extraction_failed=true`; `extraction_gaps = [{kind: extractor-failure, handler:
  squashfs_v3, dependencies: []}]`; `files: []` (P=0); diagnostics contains `ExtractCommandFailedReport`
  with `command: "sasquatch -le -no-exit-code -f -d ..."`, `exit_code: 1`. Under the draft precedence,
  step 5 does not fire (handler is not `squashfs_v4_be`), step 6 fires →
  `(legacy-body-failure, cross-read-legacy)`. The row is reachable and distinguishable.
- Notably the same probe also falsifies any claim that v3 failure is always damage: the failing command is
  recorded and the fault may be sasquatch-specific; cross-reading with `unsquashfs` (which read the v3
  superblock cleanly, see Q5 evidence) is a meaningful separator.

Defects in the draft's step 6:

- No source citation (AXES depth requires cited sources). Fix: cite S112 `squashfs.py:40-54` (the
  version gating) and the reader support facts (unsquashfs 4.7.5 reads v1–v3 gzip; 7z reports a
  SquashFS handler; both read the v3 fixtures — verified, below).
- "failing handler a v1–v3 handler" is not machine-readable: the table grammar needs a handler-cell
  pattern. All reachable legacy handler names observed at runtime: `squashfs_v1`, `squashfs_v2`,
  `squashfs_v2_nonstandard`, `squashfs_v3`, `squashfs_v3_broadcom`, `squashfs_v3_ddwrt`,
  `squashfs_v3_nonstandard` (probes below). A cell pattern like `squashfs_v[1-3]*` matches all of them
  and no v4 name (`squashfs_v4_*` starts `v4`), and step 5 already claims `squashfs_v4_be` before step
  6 runs, so the rows are order-separated.
- If vocabulary: the v4 block's `<!-- sqfs-triage-actions: ... -->` line must add `cross-read-legacy`;
  the v3 line doesn't have it.
- Reader-coverage limit: the cross-read remedy is only as strong as the second reader. `unsquashfs`
  4.7.5 validates the superblock of the v3 LE/BE fixtures, and 7z lists them; for lzma-based v3
  fixtures (e.g. `squashfs_v3_adaptive/__input__/squashfs_v3_le.lzma.bin`), the fixture resolves to
  handler `squashfs_v3` and extracts cleanly via sasquatch, but `unsquashfs` has no LZMA support —
  the predicate should say "cross-read with a reader that supports the image's compression" rather than
  naming `unsquashfs` unconditionally.

## 3. Q3 — is `dep-missing-le` the right label for a BIG-endian v3 chunk that resolves plain sasquatch?

**Verdict: CONFIRMED — yes. Verified from source and from a real REA envelope.**

Evidence:

- Source chain: `SquashFSExtractor` (unblob `squashfs.py:24-69`) resolves `executable =
  sasquatch` for every non-4 version, including `Endian.BIG` (line 51-52) where it appends `-be`; only
  `Endian.BIG, 4` resolves `sasquatch-v4be` (line 40-41). The command spawned is
  `Command("sasquatch", "-be", ...)`. `unblob/extractors/command.py:66-76` catches `FileNotFoundError`
  and builds `ExtractorDependencyNotFoundReport(dependencies=self.get_dependencies())`; `Command.get_dependencies`
  (`command.py:100-103`) returns `[self._executable]` = `["sasquatch"]`. The `SquashFSExtractor.get_dependencies`
  returning both names (`squashfs.py:68-69`) is used only for the CLI preflight print, not for the report.
- Real envelope: I ran REA on the pinned v3 BE fixture with `$HOME/.local/bin` removed from the child
  PATH (kept the fnm/npm dirs so npx still runs):
  `... extract-firmware --format json --full-output <squashfs_v3_be.bin> <fresh outdir>`.
  Result (`artifacts/R42CritC2Draft/probes/rea-v3be-nodep.json`): gap `{kind: missing-extractor-dependency,
  handler: squashfs_v3, dependencies: ["sasquatch"]}`; diagnostics `ExtractorDependencyNotFoundReport`
  with `dependencies: ["sasquatch"]`. So for a BE v3 chunk the envelope's D is exactly `{sasquatch}`;
  `dep-missing-le` is correct, and the draft's "(to be confirmed by wave 1 on real REA envelopes)" is now
  confirmed. Same mechanism already evidenced for v4 LE by the frozen round-36 receipt
  (`corpus/evidence/round-36/c1/K1/before.json`: `dependencies: ["sasquatch"]`).
- Corollary for the precedence rewrite: because D is reported per missing executable of the resolved
  command, D is a singleton on every single-chunk envelope; the membership form and exact-set form agree
  on real envelopes. The membership form still fixes the R41-W2 F1 synthetic superset
  (`D={sasquatch, sasquatch-v4be}` → `dep-missing-be` first-match), which is the right outcome. Keep the
  membership form, and add a note that D is the per-gap missing-executable list; a multi-chunk envelope
  with gaps on different handlers can union two singletons (e.g. `{sasquatch}` from a v3 chunk and
  `{sasquatch-v4be}` from a v4 BE chunk) — first-match then decides dep-missing-be for the whole
  envelope, which is a genuine ambiguity the draft should name (the v3 table had the same class of
  multi-chunk ambiguity; see R41W2C2Table F2).

**Concrete predicate changes:**

- (P3) Keep `dep-missing-le` for v1–v3 (both endians) and v4 LE; state the resolved-executable rule in
  the cause cell; drop the "[to be confirmed]" bracket or replace with the confirmed statement.
- (P4) Define D as the union of per-gap `dependencies` lists (already the v3 convention) and explicitly
  document the multi-gap union first-match consequence.

## 4. Q4 — does `lookup_combo_below_half` bind something a do-nothing or lookup control cannot reach?

**Verdict: no — the target is degenerate. A do-nothing control scores 0 < half, so the binding cannot
certify anti-enumeration and adds no constraint a shortcut cannot satisfy.**

Evidence:

- Target text (draft `:100`): "the frozen lookup control CTL-C2-7 (named-class tuples from the dev set,
  exact) scores strictly fewer than half of the held-out combos".
- A control that labels every envelope `(unclassified, none)` scores 0/12 = 0 < 6, satisfying the
  binding trivially. The binding therefore does not distinguish "combos are not enumerable" from
  "nothing labels combos". The claimed anti-enumeration property is not what the target measures.
- Separately, the main predicate `matched == n` already forces the real table to match the evaluator on
  every held-out envelope; the lookup binding is the only anti-shortcut witness, and it is vacuous for
  do-nothing. It also has no floor: a lookup with a majority-class fallback (one extra catch-all row,
  e.g. `partial-body-failure`) could score > half again, so the exact-only wording is fragile.
- The R41 precedent confirms the measurement problem: CTL-C2-7 scored 8/12 on combos, and only 4/12
  combos have tuples outside the 27 distinct named-class tuples (recomputed from the frozen manifest;
  see `artifacts/R42CritC2Draft/manifest-stats.txt`).

**Concrete predicate changes:**

- (P5) Bind the family directly: require the held-out generator to report, per combo, whether its
  observed tuple lies outside the union of dev named-class declared tuples, and bind a **count**
  `unseen_combos >= ceil(n_combos/2)` (or a stronger fraction). This is the property a do-nothing
  cannot satisfy (it does not change the family) and is the real anti-enumeration witness.
- (P6) Keep CTL-C2-7 < 50% as a secondary check, and add an upper-bound control CTL-C2-7b (lookup +
  majority-label fallback) that must also score < 50%, so a fallback shortcut cannot slip through.
- (P7) State in the predicate that the lookup control is built from the frozen dev named-class declared
  tuples only (exact cells, no fallback) — i.e. define CTL-C2-7's construction in the claim, not in a
  control artifact.

## 5. Q5 — can the legacy classes, built from a few fixtures, be enumerated by a lookup?

**Verdict: yes — the legacy class universe is small and closed, so a named-class lookup built from the
dev set will enumerate the held-out legacy combos unless the generator deliberately forces non-colliding
factor draws (which the draft does not require).**

Evidence:

- Fixture inventory (unblob 26.6.4 tree at 1fcc7a0, `tests/integration/filesystem/squashfs/`): 43
  v1–v3 input files, but with heavy byte redundancy — e.g. `squashfs_v3/little_endian/__input__/squashfs_v3_le.bin`,
  `squashfs_v3_ddwrt/little_endian/__input__/squashfs_v3_le.bin` and
  `squashfs_v3_nonstandard/little_endian/__input__/squashfs_v3_le.bin` are byte-identical
  (sha256 `0161351c…`); `squashfs_v3_broadcom/big_endian/__input__/squashfs_v3_be.bin` equals plain
  `squashfs_v3_be.bin` (sha256 `4e9493d9…`).
- Runtime handler resolution on the fixtures (REA envelopes in `artifacts/R42CritC2Draft/probes/`):
  `squashfs_v1`, `squashfs_v2`, `squashfs_v2_nonstandard`, `squashfs_v3` (plain LE/BE and the
  `_adaptive` lzma fixtures), `squashfs_v3_broadcom`, `squashfs_v3_ddwrt`, `squashfs_v3_nonstandard` —
  at most 7 distinct legacy handler names, no symlink/device cases in the legacy fixture set (the only
  symlink fixture is v4 LE `bad_symlink.squashfs`).
- Feature-space consequence: legacy SR=no always; D∈{∅,{sasquatch}}; G∈{∅, missing-extractor-dependency,
  extractor-failure, depth-limited}; BE is determined by endianness when a command ran (BE→yes, LE→no)
  or n/a when none did; P∈{0,>0}. The Cartesian product of handler × state is small (a few dozen
  tuples). Dev classes ("clean per handler, dependency missing, zero-file, partial body damage") built
  from these fixtures cover that product, so the dev named-class tuple inventory contains every tuple a
  held-out legacy combo can realize from the same factor pool. A lookup over the dev declared tuples
  then scores near-complete on legacy combos.
- The R41 measured baseline already shows the collision problem with v4-only factors: 8/12 combos have
  tuples inside the named-class inventory (manifest-stats). Adding the handler family as a factor mostly
  relabels those collisions into legacy handlers; it does not enlarge the tuple space enough to push a
  lookup below half unless the factor draws are engineered to miss the dev inventory — which a seeded
  random draw will not reliably do.

**Concrete predicate changes:**

- (P8) Require the generator to verify at build time that the count binding (P5) holds — i.e. the
  generator must fail loudly if fewer than half the combos land outside the dev named-class tuple union.
  Otherwise the `lookup_combo_below_half` target is unachievable or vacuous, and the freeze would ship a
  claim that cannot be met (or is met by degenerate controls).
- (P9) Pin the legacy fixture set and note the byte-redundancy (several named variants share bytes); if
  the "clean per handler" classes are built from byte-identical inputs, they collapse to the same
  handler+tuple and the class count overstates the distinct surface. Define "per handler" by the
  *runtime handler name* observed in a dev-arm REA envelope, not by the fixture directory name.
- (P10) Because the legacy universe has no symlink/device states, the v4 symlink rows (9–11) are not
  reachable on legacy envelopes; state this limit so the claim does not imply otherwise.

## 6. Additional defects found (bonus)

- (D1) The draft's step 2 uses F = "set of SquashFS handler names in H (`squashfs_` prefix)". With the
  v3 interpreter's handler cells this is fine, but the evaluator must use the same F definition; the v3
  evaluator tested for `squashfs_v4_*` prefix, so the v4 evaluator must change step 2 to F = ∅. This is
  a one-line consistency requirement between interpreter and evaluator (R41-CL4 fix).
- (D2) The v4 block's action vocabulary must add `cross-read-legacy` (not in the v3 line).
- (D3) The draft's legacy classes include "zero-file" — my damaged-v3 probe is exactly that class
  (P=0 extractor-failure); clarify that "zero-file" means P=0 failure, distinct from the empty-tree
  `clean-empty` class, so the manifest's declared tuples stay unambiguous.
- (D4) The `--max-depth 1` C1-style run on a single top-level v3 chunk produces a `depth-limited` gap
  even when extraction succeeded (probe `rea-v3le-clean.json`: P=2, G={depth-limited}, because the
  extract path `firmware.bin_extract` is at depth 1). The legacy class recipes must pin `max_depth`
  (default 3) for clean/damaged classes, or every legacy envelope will land on the `depth-limited` row.
- (D5) C1 oracle feasibility (adjacent, not scored here): `unsquashfs` 4.7.5 read the v3 BE and LE
  superblocks ("valid little endian SQUASHFS 3:0 superblock" / "valid big endian SQUASHFS 3:0
  superblock"), and `7z l` listed the v3 contents (apple.txt/cherry.txt) — the two non-sasquatch
  readers agree on the v3 fixtures, supporting the C1 oracle design.

## 7. Evidence and limits

- All REA runs used the prescribed CLI form; each with cwd = scratch and a fresh outdir; exit codes 0.
  Envelope artifacts copied to `artifacts/R42CritC2Draft/probes/` (12 envelopes).
- Fixture hashes in `artifacts/R42CritC2Draft/fixture-sha256.txt`; manifest stats in
  `artifacts/R42CritC2Draft/manifest-stats.txt`.
- Source citations: unblob 26.6.4 `handlers/filesystem/squashfs.py:24-69` and
  `extractors/command.py:66-76,100-103` (verified by reading the installed package at
  `~/.local/share/uv/tools/unblob/lib/python3.13/site-packages/unblob/`).
- [INFERENCE] The claim that a seeded random combo draw will not reliably keep >50% of combos outside
  the dev named-class union is a projection from the R41 measured 8/12 collision rate and the small
  legacy feature space; it was not exercised by re-running a v4 generator because the v4 generator does
  not exist yet. The predicate changes (P5/P8) make this verifiable at generation time instead.
- No reserved carrier was touched; no REA/unblob/sasquatch run outside fixtures/scratch copies; no git
  mutation; no lane files written outside this report and the artifacts dir.
