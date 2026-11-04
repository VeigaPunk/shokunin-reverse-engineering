# ReviewerClauses — r67 w1 — clause-to-line review of both frozen instruments

Seat: ReviewerClauses (reviewer, attack seat). Scope: read-only clause-to-line review of
`R67-C1`/`R67-C2` against the frozen instruments, predicates and pre-freeze receipts, plus the
four wave questions. Review window 21:49–22:02 -03; the lane moved **twice during the review**
(data run `a4c1d0fc`, instrument supersession `1e7fe7b7`+`6dcc447e`) — every finding below states
which instrument generation it attaches to.

Method note: no `lsp` device is mounted in this session (recorded per role); clause tracing is by
full file reads + `git` object reads + **executed probes** (stronger than static tracing — each
verdict-relevant behavior below was run, not just read). Probe receipts preserved under
`w1/ReviewerClauses/probes/`.

---

## 0. State of the pins (verified)

| file | assignment/freeze pin | state at review close |
|---|---|---|
| `tools/round-67/avm-le-counter.py` | `f78ed365…` (freeze `3663e6b2`) | **superseded**: worktree/HEAD = `55decb51…` (commit `1e7fe7b7`), claims.json pin updated at `6dcc447e` |
| `tools/round-67/mutation-battery.py` | `cabc0a0b…` | unchanged, worktree = HEAD = pin |
| `tools/round-67/gap-rule-v2.json` | `e66ba022…` | unchanged; freeze-tree blob = pin (`git cat-file` verified) |
| `tools/round-67/c1-run.sh` | `00be5a87…` | unchanged; fork delta vs `tools/round-50/c1-run.sh` is exactly the 18 r50→r67 rename lines (`kaidoku-r50/67`, `round-50/67`, `R50-C1/R67-C1`, schema `kaidoku-r67-c1-run-v1`) |
| `tools/round-50/c1-counter.py` (engine) | `9820811b…` | unchanged |
| `tools/round-66/closure-boundary.py` | `3c5cfb03…` | unchanged |
| `tools/round-66/coverage-selfcheck.py` | `1be9d046…` | unchanged |

Order facts (read-only git): claims.json first-add = `3663e6b2` = operative freeze = HEAD-at-review-start;
instruments+controls commit `39a91a99` 12 s earlier (QUALITY #33 order ✓); base `a7a4ce6` is an
ancestor of the freeze ✓. At review close HEAD = `6dcc447e` (3 commits past the freeze).

Predicate sentences (whitespace-normalized sha256, all sites byte-equal as sentences):

| sentence | sha256 | sites verified |
|---|---|---|
| C1 | `9cbbc4e31508208463f7d3fee3cd57e307b1e2994009b4686fe71739ca28168c` | plan blockquote == claims.json == counter `PREDICATE` (raw joined strings exact-equal) — **unchanged after the supersession** |
| C2 | `babeca7bb484ac24b36ba7dc7c9d673b62012362b16c87e2cf144c95f5fbabf1` | plan == claims.json == battery `PREDICATE` == `score-dryrun-at-base.json` receipt (raw exact-equal) |

---

## 1. Blocking findings

### B1 — RESOLVED-BY-SUPERSESSION during this review: the frozen C1 counter's `--score` arm was DOA

**Which clause the frozen bytes falsify:** the C1 trace-table row "run under the round-67 gap
rule" (plan §R67-C1). Its implementing line could not read the patched name, so the predicate's
first half could never evaluate on the frozen instrument → R67-C1 would have been
not-verifiable (exit 2) at the after-arm.

Mechanism (frozen bytes `f78ed365…` at `3663e6b2`): `patch_engine()` set
`mod.GAPRULE = str(rule)` — an **absolute** path (`rule = Path(args.gap_rule).resolve() … else
repo / RULE_V2`, always absolute). The pinned engine reads its rule through git objects:
`tools/round-50/c1-counter.py:2174` `plan_raw = show(root, freeze, GAPRULE)`,
`:2197` `gap_rule_unchanged = show(root, rev, GAPRULE) == plan_raw`. `git show REV:/home/…`
fails (`fatal: path '…' exists on disk, but not in '3663e6b2'`, rc 128) → `plan_raw is None` →
`raise Unevaluable('gap-rule.json absent at freeze')` → counter exits 2 before scoring anything.

**Empirical reproduction on the true freeze blob** (`git cat-file blob
3663e6b2:tools/round-67/avm-le-counter.py`, sha re-verified `f78ed365…`; probe receipt
`probes/doa-frozen-blob-f78ed365.json`):

```
exit_code: 2
"unevaluable": "gap-rule.json absent at freeze"
```

**Resolution already committed while this review ran** (verified, not assumed): `1e7fe7b7`
patches `patch_engine()` to compute the **lane-relative** name (`rule.resolve().relative_to(repo)`
→ `tools/round-67/gap-rule-v2.json`) and to refuse any rule outside the lane (`Unevaluable`), and
re-takes `l1/pre/control-dryrun.json`; `6dcc447e` swaps the claims.json pin to `55decb51…`, adds
atom **A10** and an `instrument_supersessions[]` block whose reason states the exact mechanism I
reproduced. Post-fix checks I ran: the corrected counter reads the rule via relative git show
(1357 bytes); `--control` rerun with the committed bytes reproduces the committed before-record
verdict-for-verdict (`gaps_ok_round50 2 / round67 4`, all three red controls true, exit 0; probe
`probes/c1-control-rerun-55decb51.json` — only my probe's `rev` field differs: I probed at the
freeze, the record names the base). The L1 must treat `55decb51…` as the operative instrument;
any after-arm receipt must carry that counter sha.

### B2 — LIVE: the R67-C2 battery never reads the claims file (QUALITY #68 refusal absent)

**Which sentence this falsifies:** the plan preamble's "each predicate sentence is byte-identical
in this file, `.ufo/waves/round-67/claims.json`, the instrument's `PREDICATE` constant and every
receipt **(QUALITY #68; the instruments read the predicate from the claims file and refuse on a
mismatch — the r66 reviewer's routed F1 pattern)**". For the battery that parenthetical is false:
`mutation-battery.py` contains no claims-file read at all (grep over the file: the only `claims`
hits are docstring lines 31–32), `--score` stamps the constant `PREDICATE` into its receipt and
never compares it to `.ufo/waves/round-67/claims.json`; an amendment that drifted the C2
predicate in claims.json would be invisible to the battery (it would still exit 0). The battery
docstring's own "byte-identical in … claims.json" self-description inherits the same overstatement.

Contrast, C1: the counter implements #68 and I exercised it — `--score --claims` with a mutated
predicate → exit 2, `"claims predicate differs from PREDICATE: 'R67-C1 is verified iff DRIFTED
SENTENCE.' != …"` (`probes/claims-refusal-exit2.json`).

Severity ruling: this falsifies a **plan-sentence**/QUALITY #68 instrument assertion, **not**
either predicate clause — the R67-C2 predicate sentence itself contains no claims-file clause and
every clause of it is otherwise implemented (§3). The L1 routes it: either a disclosed plan
correction scoped to that sentence, or a battery supersession that adds the claims read (the
battery is otherwise clean; its bytes still match the pin). Note the r65 precedent recorded the
same class as a conformance disclosure ("the C2 counter carries no predicate constant and no
receipt carries the frozen sentence — QUALITY #68 covered claim and plan only").

---

## 2. Advisory findings

**A1 — "every receipt" overstatement.** 4 of the 5 committed pre-freeze receipts carry **no
predicate field** (`control-dryrun.json`, `control-dryrun-c2.json`, `selftest-c2.json`,
`selftest-r50.txt`); only `score`-shape receipts embed the sentence (`score-dryrun-at-base.json`
verified byte-equal). The plan's "and every receipt" is false as written for the before-records.

**A2 — A5 wording vs rule delta.** `gap-rule-v2.json` **drops** the r50 rule's
`removed.silent: {char-device: ["247:0"]}` while claims atom A5 and the counter docstring say
`allowed/removed/structural` are "unchanged/keeps". Behavior verified equivalent on these
carriers: the re-taken control record shows Cable carriers `1 removals, 1 silent → 0 silent`
with `gaps_ok` unchanged (the 247:0 row is covered by `required.char-device=false`). Also
`gap_rule_model()` (engine :805-807) only rejects a *wrong* `claim` value — an absent one (v2's
shape) passes, so the docstring's "with claim R50-C1" is stale for v2.

**A3 — the C1 second conjunct has no revision binding.** "the four frozen envelopes scored under
the round-50 rule report gaps_ok on 2 of 4" is evaluated **only** by `control()` (before-record at
rev = base `a7a4ce6`); the after-arm's `--score` receipt never re-evaluates it, and the r50
envelopes (`corpus/evidence/round-50/c1/*/after.json`) are **not** in the engine's freeze-drift
set (`FROZEN_PATHS`/`FROZEN_PREFIXES` cover tools/round-50/**, plans/round-50-claims.md,
carriers.json, the rule, XPIN, rea-pkg — not the evidence envelopes). A post-freeze edit of the
r50 envelopes would silently stale that half. Cheap L1 action: re-run `--control` at the measured
rev (no REA needed — ~2 s) or record freeze-vs-measured envelope digests beside the after-arm.

**A4 — pkg65 pin is an operational trip-wire for the after-arm.** Probe of the corrected counter
with the auto-located npx-cache package: exit 2, `"package-lock.json sha256 815c18f1… != frozen
d42d56f0…"`. The npx-cache rea-agents 6.5.0 does not match the frozen `tools/round-42/rea-pkg.json`
pin (`tools/round-50/rea-pkg.json` and r49 candidates do not exist at the freeze — `git cat-file`
verified). Fail-closed (exit 2, never a false green), but the L1 must pre-resolve the matching
package root for `--pkg65` or the after-arm is could-not-evaluate.

**A5 — trace-table wording vs superseded bytes.** The plan's C1 trace row "patch_engine() sets
mod.GAPRULE = RULE_V2" describes the pre-supersession patch; the current instrument sets the
lane-relative `rule_rel` (same semantic name, strictly stronger refusal). The plan was not
amended (`declaration_pointer` "no amendments" holds; `plans/round-67-claims.md` untouched by the
three post-freeze commits). No action required; recorded for QUALITY #87 accuracy. Similarly,
claims.json still says "No amendment series." while carrying `instrument_supersessions[]` — the
sentence targets claim amendments and A10 discloses the instrument supersession; defensible, noted.

**A6 — mid-flight worktree churn observed (not certified).** Between 21:57:31 and ~22:00 a third
counter revision (sha `e44cacf5…`) transiently existed **uncommitted**; at review close
`git status` shows `.ufo/waves/round-67/l1/pre/control-dryrun.json` **modified** (worktree copy
records counter sha `e44cacf5…` ≠ HEAD/pin `55decb51…`) while the counter worktree itself is
clean at the pin. HEAD's committed record **does** match the pin (verified from the HEAD blob).
If the L1 intends another supersession, repeat the QUALITY #33 disclosure; if not, restore the
receipt. All my verdicts are stated against HEAD (`55decb51…` + its committed record).

**A7 — data-run state.** `a4c1d0fc` committed `run.json` ×4 only; the four `after.json`
(mt 21:54–21:57) sit **untracked** under `corpus/evidence/round-67/c1/`. Consistent with atom A6's
flow and harmless for `receipt_fresh` (any future first-add descends from the freeze), but the L1
owns landing them; I did not verify the `after.json` envelope digests against the committed
`run.json` records (the score arm binds that). No seat-scope attribution attempted — writer
identity is not determinable from mtimes alone.

**A8 — junk-rule disclosure (already honest, restated for Q4).** The control record truthfully
reports `junk_rule_would_pass: true`: red fixture 1 (one removed symlink gap) cannot alone prove
symlink scoping. Scoping rests on `required.symlink: true` in the pinned rule bytes plus the
2-of-4 control half (§3, C1-8).

---

## 3. Per-clause tables (verified against HEAD instrument bytes)

### R67-C1 — counter `tools/round-67/avm-le-counter.py` sha `55decb51…` (frozen `f78ed365…` superseded per B1), engine `tools/round-50/c1-counter.py` sha `9820811b…`

| # | clause | implementing line(s) | verification |
|---|---|---|---|
| C1-1 | pinned round-50 scoring engine | counter `load_engine()` — `sha256_file(path) != ENGINE_PIN` raises; receipt carries `engine {path, sha256}` | engine bytes at freeze hash `9820811b…` ✓ (my sha256sum + receipt `engine.sha`) |
| C1-2 | run under the round-67 gap rule | `patch_engine()` sets lane-relative `GAPRULE` (`1e7fe7b7`); engine `:2174` `plan_raw = show(freeze, GAPRULE)`, `:2214` `model = gap_rule_model(plan_raw)`; `:2197` `gap_rule_unchanged` | **frozen bytes: DOA (B1, reproduced)**; superseded bytes: rule read via git = 1357 B ✓; outside-lane `--gap-rule` refused ✓; working-tree tamper inert (model + unchanged check read git objects only) |
| C1-3 | round-67 documentation bindings | `patch_engine()` sets `ENTRY/STEM/CORE_HEADING/FRONTIER_MARK/OPENED_DATES` (+AFTERDIR, PROV_*); engine `:2423-2461` evaluates `province_core_section/row`, `frontier_note`, `entry_present`, `sourced`, `coverage_map_row` | lines verified in both files; evaluation deferred to the after-arm (bindings land with the record) — not yet exercisable |
| C1-4 | carriers_matched 4 of 4 | engine `:2475-2479` `matched` over `CLAUSES`, with counter patch `CLAUSES − carrier_fresh_ok` (disclosed in `patches.dropped_clauses`) | patch verified in code; both receipts show the drop list |
| C1-5 | met_target true | engine `:2494-2496` conjunction (carriers_unchanged ∧ gap_rule_unchanged ∧ matched==4 ∧ BINDINGS) | verified; `gap_rule_unchanged` compares git blob rev-vs-freeze — a committed rule tamper flips it ✓ |
| C1-6 | exit 0 at the measured revision | counter `score()` `:225` `exit_code = 0 if met_target`; receipt `rev`; engine `receipt_fresh` (first-add descends from freeze) | exit contract exercised (0/1/2 paths all observed in probes) |
| C1-7 | 2 of 4 under the round-50 rule | counter `control()` `:231-328`: `disposition_check(gaps, diags, nonreg, model_r50, …)` over the four committed r50 envelopes; `ok` requires `gaps_ok_round67==4 ∧ gaps_ok_round50==2` ∧ both red controls | before-record reproduced by my rerun (verdict-identical; A3 notes the missing revision binding) |
| C1-8 | no pass with the defect absent (Q4) | — | see §4: with the frozen bytes the arm passes **nothing** (DOA); with the superseded bytes a symlink-waiving rule cannot be injected (outside-lane refused; working-tree tamper inert; committed tamper → `gap_rule_unchanged` false → `met_target` false) |

### R67-C2 — battery `tools/round-67/mutation-battery.py` sha `cabc0a0b…` (unchanged), pins `3c5cfb03…` / `1be9d046…` verified

| # | clause | implementing line(s) | verification |
|---|---|---|---|
| C2-1 | battery kills both survivors | `score()` `:300-384`; `killed_after` `:351` = `after_rc != 0 ∧ EXPECTED_CASE[name] ∈ failed_cases`; `ok` `:380-381` requires `killed_after==2 ∧ killed_before==0 ∧ pristine green ∧ battery==0` | `score-dryrun-at-base.json`: killed_after 2 with exactly the named cases (`arm-false-bound`; `equiv-doctored-bound`+`equiv-doctored-diffs`) ✓ |
| C2-2 | closure survivor (`arm()` always passes) | `closure_mutant()` rewrites the unique `'"passed": bool(passed)'` line (`closure-boundary.py:220`, single occurrence verified) → `"passed": True`; killed by `check("arm-false-bound", cm.arm("ctl", False, {})["passed"], False)` | mutant rebuilt byte-identical (`5e84208a…` == receipt); battery on the mutant: `SELFTEST FAILED cases=7 failures=1` = `arm-false-bound` ✓ (`probes/c2-selftest-m5-mutant.json`) |
| C2-3 | coverage survivor (equivalence without running) | `coverage_mutant()` `replace_span` over the unique anchors (`coverage-selfcheck.py:200` and `:211`, single occurrences verified) → constant equivalent-true return (r66 M2 semantics) | mutant rebuilt byte-identical (`2b98a7f7…` == receipt); killed by the two named cases in the dryrun receipt ✓ |
| C2-4 | both pristine counters stay green | `selftest()` `closure/coverage-selftest-green`; `score()` `:353-358` pristine block | my pristine rerun: `SELFTEST CLEAN cases=9 failures=0`, receipt **byte-identical** to committed `selftest-c2.json` (`6e3a66f2…`) ✓ |
| C2-5 | r66 selftests alone leave both alive (0 of 2) | `control()` `:257-296` `killed_before`/`survived_before` | my rerun **byte-identical** to committed `control-dryrun-c2.json` (`3570d2e0…`): killed_before 0, survived_before 2, 30+26 cases CLEAN ✓ |
| C2-6 | no pass on a merely-broken mutant (Q4) | `score()` builds mutants only by fixed anchors from **pinned** bytes (`:305-308` pin refusal); an import failure yields no cases → not `killed_after` | demonstrated: `--selftest --closure <syntax-error>` → `SELFTEST FAILED could-not-evaluate invalid syntax` (rc 1) — a broken mutant is could-not-evaluate, never "killed", never a pass ✓ |
| C2-7 | #68 claims-file refusal | **absent** | **B2 (blocking for the plan sentence)** |

---

## 4. Q4 answers (can an arm pass while the defect it names is absent?)

- **C1:** with the frozen bytes, `--score` reaches **no verdict at all** (exit 2 DOA — B1,
  reproduced on the pin blob), so the question was moot-by-brokenness. With the superseded bytes:
  a symlink-waiving rule **cannot** reach 4/4. Injection paths closed: `--gap-rule` outside the
  lane → `Unevaluable` (exit 2); uncommitted working-tree tamper → inert (the model and both
  unchanged checks read git objects, engine `:2174/:2197/:2214`); a *committed* tamper →
  `gap_rule_unchanged` false → `met_target` false → exit 1. The remaining honest weakness is
  disclosure-level only (`junk_rule_would_pass true`, A8).
- **C2:** the battery **cannot** pass on a merely-broken mutant: mutants are derived by fixed,
  anchor-verified rewrites of sha-pinned pristine bytes (both generated mutants are syntactically
  valid — `py_compile` verified — and byte-identical to the disclosed mutant hashes); a
  syntax-error instrument is `could-not-evaluate` (rc 1, no cases) and `killed_after` additionally
  requires the *named* case in `failed_cases`, so a crash (rc≠0, `failed_cases=[]`) is not
  counted as a kill.

## 5. Residual risk / verification gaps (honest limits)

- The C1 after-arm was **not** run end-to-end: the correct `--pkg65` root is unresolved (A4) and
  the documentation bindings do not exist yet by design. Everything up to the REA machinery was
  exercised via the exit-2 probes.
- The 2-of-4 half at the measured revision is not re-evaluated by any mechanism (A3) — L1 action
  recommended.
- `after.json` ↔ `run.json` envelope-digest binding unchecked by me (A7); the score arm binds it.
- The battery's #68 refusal is absent (B2) — routing decision belongs to the L1.
- Claims-file refusal verified for C1 with a mutated `--claims` copy; the battery has no
  equivalent surface to test (B2).
- No `lsp` device in this session; all line citations come from full reads and the executed
  probes archived under `probes/`.

## 6. Probe evidence index (`w1/ReviewerClauses/probes/`)

| file | sha256 | what it proves |
|---|---|---|
| `doa-frozen-blob-f78ed365.json` | `7857fd53…` | frozen counter `--score` → exit 2 "gap-rule.json absent at freeze" |
| `claims-refusal-exit2.json` | `cda23490…` | C1 #68 refusal fires on a drifted claims predicate |
| `c1-control-rerun-55decb51.json` | `18068bb3…` | corrected counter `--control` reproduces the before-record verdicts (probe used rev=freeze vs record's rev=base — sole delta) |
| `c2-control-rerun.json` | `3570d2e0…` | battery `--control` rerun **byte-identical** to committed `control-dryrun-c2.json` |
| `c2-selftest-pristine.json` | `6e3a66f2…` | battery pristine selftest **byte-identical** to committed `selftest-c2.json` (9/0) |
| `c2-selftest-m5-mutant.json` | `953dfe24…` | M5 mutant killed by `arm-false-bound` (7 cases, 1 failure) |
| `mutant-closure-m5.py` | `5e84208a…` | rebuilt M5 mutant, byte-identical to disclosed mutant hash |
| `mutant-coverage-m2.py` | `2b98a7f7…` | rebuilt M2 mutant, byte-identical to disclosed mutant hash |
