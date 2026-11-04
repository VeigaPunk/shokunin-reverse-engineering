# ConnectorCross — sibling overlap scan for round-77 R77-C1 / R77-C2

Read-only. Nothing outside this evidence dir was written. Every sibling path below was read at
the sibling lane's working tree (never written); every round number was confirmed against the
owning lane's `SKILL.md` registry row where one exists. Frozen bytes (`plans/round-77-claims.md`,
`.ufo/waves/round-77/claims.json`, both instruments) were read only.

## 1. Bottom line (three sentences)

1. **Neither instrument is a novel rule.** `verdict-bind.py` is a stronger *execution* of a rule
   mado already declares and already runs (criterion 23 + the registered `mado-label-check`,
   `mado-shokunin/SKILL.md:745`), and of a stated↔observed counter tsukuroi has run since round 26
   (`check-self-assessment.py` K01–K27).
2. **`prefile-receipt.py` is a weaker duplicate on three of its five binding legs** (argv, rev,
   exit, stdout digest) and genuinely novel on exactly two (the `env_keys` assertion recorded
   inside the receipt, and A3's newest-round-dir discovery of `gate-*` receipts). souji's round-23
   `souji-receipt-run.py` and tameshi's `command-binding.py` / `receipt-revision-gate.py` /
   `receipt-bytes-bind.py` already bind those four legs, two of them more strictly.
3. **The round's five routed defects map to its arms 4/5**, and the uncovered one is defect 2
   (loose tip-receipt revision prose) — which is uncovered *by construction*, because C2's A2 arm
   calls `check_receipt(receipt)` with no `expect_rev` (`tools/round-77/prefile-receipt.py:236`)
   while the frozen predicate only says the filing receipt "exists at `--rev` and passes with
   exit 0". A sibling already mechanizes that leg.

## 2. Sibling hits (what each binds, and what it does not)

| Lane | Path | Round | Binds | Does not bind |
|---|---|---|---|---|
| mado | `.ufo/waves/round-17/label-check.py` (+ registered row `mado-shokunin/SKILL.md:745`; claims `label-claims.json`) | 17 | a *citing sentence's* attributed verdict token → the cited receipt's **outcome token** (`MADO_<NAME>:` word, `finding` value, got-side), doc read at `rev`, receipt at `rev_receipt`, optional `measured_commit` | no automatic grammar extraction (claims file is hand-written per claim); no typed field equality; no N-of-M, atom-`ok`, or `validate defect-free` clause |
| kumitate | `corpus/QUALITY.md:931-936` (Q55) | 60/61 | prose criterion: cited receipt exists at tip, `rev=` equals report's measured revision, quoted verdict/held/exit is a **fixed-string substring** of the receipt bytes | **no instrument** — grep of `kumitate-shokunin/tools/*.py` for `quoted`/`tip-receipt`/`after-receipt` returns nothing; criterion is reader-executed |
| tsukuroi | `tools/check-self-assessment.py` | 26 | stated numbers parsed out of SCORECARD/AXES cells (`stated_in`, `stated_case_count`, `:572-600`) → observed state via `git show`/`ls-tree`; `mismatch` carries stated, observed and line numbers | reads corpus/ls-tree state, never a receipt JSON's fields; no declared population scope |
| kama | `tools/capability-repertoire-audit.py` (+ `SKILL.md:1424`) | 34 | `unsubstantiated` = canonical `## Capabilities` row whose **evidence cell carries no repo-relative path that resolves at the evaluated revision** — this *is* the D24 atom kaidoku says is insufficient | never reads the verdict written beside the resolving path |
| chousa | `tools/lane-preflight.py` G05 (+ `SKILL.md:154`) | 63 | every `corpus/ tools/ .ufo/` path in the evidence cell of a SCORECARD `## Capabilities` row exists under ROOT (worktree) | worktree, not a revision; path only |
| kengaku | `plans/round-6*-claims.md` (10 probes, 9 with `--check-receipt`) | 59–72 | re-derives a probe's own text fields from a receipt and prints `PREDICATE RNN-C1 pass|fail` | receipt may be fabricated: carried named limit, r64 `:102`, r65 `:126` and `:246` ("a fabricated receipt passes `--check-receipt`"; "cannot prove a live run") |
| souji | `tools/souji-receipt-run.py` | 23 | **runs** a command at a durable rev in a private `--no-local` clone; receipt binds `rev`, `tool`, `tool_sha256` **at that rev**, `cmd`, `rc`, stdout/stderr; refusals include `RECEIPT-REV-NOT-DURABLE` (not reachable from heads/tags/remotes) and `TOOL-CHECKOUT-DIFFERS` | no env allowlist recorded; no round-dir population discovery |
| souji | `tools/souji-gate-check.py` | 22 | entry gate quotes resolve in the committed snapshot; slice verdict rows `present|accepted|unverifiable|refused` | unrelated to gate receipts |
| tameshi | `tools/command-binding.py` | 23 | bundle + digest-pinned `--expected`: name, **argv (no shell normalization)**, canonical absolute cwd, full revision, integer exit, required stdout tokens | validates retained declarations, not producer authenticity (stated in its docstring) |
| tameshi | `tools/receipt-revision-gate.py` | 54/55 | one `rev=` per receipt → `--certified` (or byte-identical `--paths`); codes `RECEIPT_REV_MISMATCH`, `RECEIPT_REV_CONTENT_DRIFT`, `RECEIPT_REV_NOT_DURABLE` class, `RECEIPT_REQUIRED_LINE_MISSING` | no argv; no env |
| tameshi | `tools/receipt-bytes-bind.py` | 79 | recorded `tool_sha256` → committed blob at `measured_rev`, or a declared `measured_bytes_rev` correction, or a declared design block; states `bound/corrected/design/unbound` | no execution leg |
| tameshi | `tools/defect-bind.py` | 80 | routed-defect register rows measured over committed bytes (`tree-paths`, `tree-bytes`, `receipt-tokens`, `sources-cell`, `doc-contains`), empty manifest refused exit 2 | no gate-receipt population |
| tameshi | `tools/receipt-exists.py`, `tools/check-*` | 64 | cited receipt paths resolve at a pinned rev (`git cat-file -e`) | existence only |
| chousa | `tools/receipt-pin.py` | 65 | `REVISION=`/`EXIT=`/`SHA256=` header → committed blob at the selected revision; states in-docstring: *"Header consistency is NOT execution authenticity"* | no argv tokens, no env keys |
| kama | `tools/round33-gate-receipts.py` | 32/33 | **capture + audit complete gate receipts** for a registry gate: a declared `CASES` dict mapping each case to `(file, expected exit, expected stdout line)` plus `EXPECTED_STDOUT`, replayed from a pinned source revision | population is a hard-coded dict, not discovered by round directory |
| kama | `tools/round73-receipt-claim-binding.py` | 73 | grades **citing lines** carrying a tip claim: each cited receipt's own `tip=`/`rev=` header must equal the resolved tip; exit 2 if the record cites no receipt | grades the revision leg only, never a value |
| kama | `tools/gate-registry-check.py` | 32 | registry rows: occurrence **and** meaning (`thin-row`, `empty-entry`, `empty-exit-map`, `missing-path`) over committed bytes | — |
| tsukuroi | `tools/check-report-receipts.py` (+ `SKILL.md:2671`) | 30 | every revision-cited `[rev, tool]` pair in a report has a **committed receipt** | does not read the verdict the report states |
| tsukuroi | `tools/check-cited-receipts-r62.py` | 62 | every `.ufo/waves/round-<N>/…` path a round's committed bytes cite exists as a blob at the same rev | citation existence only |
| kotodama | `tools/check-receipt-seq.py` | 67 | `stamped == evaluated == measured` + tree + counter sha256; `--lands` reads committed bytes; `moved_past` is computed and **deliberately never changes a verdict** | no argv, no env, no value clauses |
| mori | `tools/mori-receipt-complete.py` | 63 | a receipt's `failed=` anchor list is complete/untruncated | one file's shape |
| mori | `tools/mori-gate-registry.py` | 45 | every audited tool has a registry row **and** a real `--selftest` argv branch (comment/docstring occurrence is not a branch) | — |
| mado | `tools/mado-receipt-citecheck.py` | 64 | repo-relative citations inside a named artifact resolve at `--rev` | value legs |
| chousa | `tools/freeze-check.py` | 60 | frozen claims ↔ dispatch payload byte-render equality, digest presence/stray, ready identity | receipt legs |
| kaidoku (in-lane) | `tools/round-47/record.py` | 47 | the lane's own atom-by-atom SCORECARD re-derivation: `seats/window/path/rev/axes`, appended `## Record corrections` exemptions, exit 0/1/2 | parenthesised annotation grammar; JSON receipt fields |

Kama's own cross-lane rule text already settles part of this surface:
`kama-shokunin/corpus/knowledge/cross-lane-scope.md:137` — *"Receipt → revision is owned by
tameshi"*, naming `receipt-revision-gate.py`, `receipt-commit-bind.py`, `receipt-window.py`,
souji r57, chousa `receipt-pin.py`, tsukuroi, kotodama, plus kama's own round-72 delta rule. That
file also records kaidoku's `round-42/prefile-gate.py` as one of three split round-scope opinions.

## 3. Novelty, per instrument

### R77-C1 `tools/round-77/verdict-bind.py` — **weaker duplicate of a rule, stronger execution of it**

- Rule prior art: **mado criterion 23** (`mado-shokunin/corpus/QUALITY.md:111`), whose runnable
  check is the registered `mado-label-check` (`mado-shokunin/SKILL.md:745`,
  `.ufo/waves/round-17/label-check.py`). Same sentence class, same `git show` doc/receipt legs,
  same outcome-token semantics.
- Counter prior art: `tsukuroi-shokunin/tools/check-self-assessment.py` (stated↔observed with
  line numbers); `kumitate-shokunin/corpus/QUALITY.md:931` (Q55, prose-only).
- Population prior art: `kama-shokunin/tools/capability-repertoire-audit.py` (the exact D24 atom —
  evidence cell path resolves at rev — with **no** value leg) and
  `chousa-shokunin/tools/lane-preflight.py` G05 (same cell, worktree).
- In-lane prior art: `tools/round-47/record.py` and `corpus/QUALITY.md:152` (row 95: *"a scoring
  step requires the receipt to exist and parse, never a zero exit"*).
- **Delta legs that are genuinely first in the fleet** (verified absent from every sibling read):
  (i) a **closed grammar** over parenthesised annotations with automatic extraction — every
  sibling form either hand-writes a claims file (mado) or matches one number against ls-tree state
  (tsukuroi); (ii) typed equality against named **top-level JSON receipt fields** including
  atom-`ok` indirection, `N of M` totals, survivor/mismatch counts and `validate defect-free`;
  (iii) a declared **round-scoped population** (`## Capabilities` rows with first-working-round
  ≥ 73 plus PROVINCE `- **Core — ` bullets) with `bound/unbound` accounting instead of silent
  skips.
- Named limits that must travel with it (all grounded in a sibling that refuses the class):
  a committed hand-written JSON whose fields merely agree passes; no tool-sha/provenance binding —
  tameshi `receipt-bytes-bind.py` does that and kaidoku does not.

### R77-C2 `tools/round-77/prefile-receipt.py` — **weaker duplicate on four legs, first on two**

| Leg | Prior art | Comparison |
|---|---|---|
| `argv` | souji `souji-receipt-run.py` (`cmd=`, `verify` re-parses and requires exact argv membership), tameshi `command-binding.py` (no shell normalization, canonical abs cwd) | kaidoku records argv and checks it names the gate + root; **weaker**: no cwd canonicalisation, no argv-membership refusal on verify |
| `rev` | souji (`RECEIPT-REV-NOT-DURABLE` against heads/tags/remotes), tameshi `receipt-revision-gate.py`, `receipt-bytes-bind.py` | kaidoku records `git -C lane rev-parse HEAD` (`prefile-receipt.py:110`) and compares it only when `expect_rev` is passed. **Weaker**: `HEAD` is a mutable ref; no durability predicate, no ancestor/content-drift check |
| `exit` | tameshi `command-binding.py`, kama `round33-gate-receipts.py` (per-case expected exit), souji (`rc=`) | equal in kind; kama's per-case expected exit is stronger than "carries an exit" |
| `stdout` digest | chousa `receipt-pin.py` (digest ⇒ **committed blob**); kaidoku's `stdout_sha256` ⇒ **the receipt's own `stdout` field** | **weaker, and self-referential**: a forger who edits `stdout` recomputes `stdout_sha256` and passes; chousa's own docstring names this boundary: *"Header consistency is NOT execution authenticity"* |
| `env_keys` assertion | none found: kama builds allowlists (`CHILD_ENV_KEYS = ('PATH','HOME','LANG','LC_ALL','TMPDIR')`, `kama-context-capacity.py:64`; `round64-c1-counter.py:159`), tsukuroi defines the round-32 allow-list base — **no sibling records the key names inside the receipt as a checked clause** | **first** |
| A3 population | kama `round33-gate-receipts.py` uses a hard-coded `CASES` dict; tsukuroi `check-report-receipts.py` derives pairs from report prose | **first** for *discovering* the population as `l1/scores/gate-*.{json,txt}` in the newest round dir at `rev` and requiring each to carry its wrapper's `exit` |
| A1 execution leg | souji `souji-receipt-run.py` runs and verifies in a private clone | equal in kind; souji is stricter (tool-sha, durable rev) |

Also relevant: `mori-receipt-complete.py` proves the lane class "the receipt's bytes may silently
lose a field at capture" is a *recurring* fleet class, not a kaidoku-only one.

## 4. Contradiction stated, not smoothed

The round repairs five routed defects. Mapping its own predicates onto them:

| Routed defect (round-76 lesson §6) | Covering arm |
|---|---|
| 1 landing receipt cited as green in three files | C2 A2 (+ C1 value leg) |
| 2 loose tip-receipt revision prose in the filed report | **none** |
| 3 gate-at-tip `exit 0` not in its receipt | C2 A3 + A4 (`red-no-exit`) |
| 4 prefile check retains no receipt | C2 A1 + A2 |
| 5 D24 admits a false verdict beside a resolving path | C1 |

Defect 2 is uncovered **by construction**: A2 calls `check_receipt(receipt)` with no `expect_rev`
(`tools/round-77/prefile-receipt.py:236`), and `check_receipt`'s rev clause only fires when
`expect_rev is not None` (`:160`). The frozen predicate is not violated — it only says the filing
receipt "exists at `--rev` and passes with exit 0" — but the round should not read as "all five
routed defects are now mechanised". The sibling that covers this leg is
`tameshi-shokunin/tools/receipt-revision-gate.py` (`RECEIPT_REV_MISMATCH`,
`RECEIPT_REV_CONTENT_DRIFT`) and, for prose claims specifically,
`kama-shokunin/tools/round73-receipt-claim-binding.py` (a citing line that says "at the tip" must
cite a receipt whose own `tip=`/`rev=` header equals the tip). Kumitate Q55 declares the same rule
in prose and, like this round, has no instrument for it — the class is fleet-wide and repeatedly
solved piecemeal.

Second contradiction, smaller: kaidoku's `tools/round-77/*.py` cite **no sibling at all** (grep for
`tameshi|souji|kama|chousa|mado|kumitate|kotodama|sibling|cross-lane` over `tools/round-77/*.py`
returns zero hits), while kama's cross-lane discipline (`cross-lane-scope.md:137`) exists precisely
so a lane claims only its delta. Round 76's routed defect 2 is *unqualified record prose*; an
unqualified novelty/ownership claim over legs siblings already own is the same mistake class in a
new surface.

## 5. Proposed move (one, bounded, additive)

**Land a prior-art-and-limits block as an appended disclosure in `corpus/lessons/round-77.md`
only** — never in `plans/round-77-claims.md`, never in `.ufo/waves/round-77/claims.json`, never in
either instrument. Precedent for the form: `corpus/lessons/round-53.md` M53-6 disclosure (cited by
`corpus/claim-freezes-corrections.tsv:2`). Three parts, each carrying its sibling anchor:

1. **Prior-art table** (the §2 rows that bear on C1/C2, lane + path + round + leg) and a narrowed
   novelty sentence per instrument using the §3 delta legs.
2. **Three named limits**, each already refused by a named sibling:
   L1 `--check-receipt` proves internal consistency, not execution authenticity
   (chousa `receipt-pin.py` docstring wording); `stdout_sha256` digests the receipt's own `stdout`.
   L2 A2 does not bind the filing receipt's `rev` to `--rev`; routed defect 2 is therefore
   uncovered — route it to round 78 citing tameshi `receipt-revision-gate.py` /
   kama `round73-receipt-claim-binding.py`. **Do not** add `expect_rev` mid-round: a frozen
   instrument strengthened after its freeze is the lane's own row-34 defect.
   L3 `verdict-bind` binds receipt *fields*, not provenance; a committed hand-written JSON passes.
3. **One scope-ownership line**: kama owns the `## Capabilities` evidence cell's path leg
   (`capability-repertoire-audit`, r34); tameshi owns receipt→revision
   (`cross-lane-scope.md:137`); C1 claims the value leg only, C2 claims `env_keys` + A3 population
   discovery only.

Affected axes: **calibration improves** (two silent limits become disclosed ones and an
unqualified novelty claim becomes a delta claim — the same repair shape as routed defects 1/2);
**depth neutral** (the block is a lesson disclosure, not a `## Queue-drain craft` block; if the L1
chooses to land it as a craft block it must cite a knowledge entry **with a line range** or it
lowers the proxy it claims, `corpus/QUALITY.md:145` row 77a); **coverage neutral** (no new
knowledge entry). No frozen byte, predicate, arm or receipt changes.

## 6. Risks

- **Tip movement.** Appending to `corpus/lessons/round-77.md` moves the rev. C2's A2 still passes
  (its rev clause is inert, §4), but the round's *record* would then carry a filing receipt whose
  `rev` predates the lesson — the exact class tameshi `receipt-bytes-bind.py` (r79) was built for.
  Sequence: land the block **and** the re-generated `prefile-at-filing.json` in the same commit, or
  disclose the ordering in the same block.
- **Gradeable as a claim edit.** If anyone folds the block into `claims.json`,
  `tools/round-29/freeze-gate.py` re-reads that file at MEASURED and the round's CLEAN row must be
  re-audited (`--disclosures`); the frozen `instruments` pins are unaffected, but an edited-claims
  surface invites the row-100 argument.
- **Scope pushback.** If the block is skipped, kama's cross-lane discipline and mado's registered
  `label-check` make "first fleet instrument binding a claimed verdict to its receipt" read as an
  overclaim in either lane's next spot-check.
- **Not a score move.** The block changes no counter; presenting it as calibration *improvement*
  beyond "overclaim removed" is itself an overclaim under row 34.

## 7. Verification (executable, read-only until the L1 lands)

1. Every cited sibling reference resolves: 23 concrete files `test -f` under their lane roots; 3 are
   line-anchored (`mado corpus/QUALITY.md:111`, `kumitate corpus/QUALITY.md:931`,
   `kama corpus/knowledge/cross-lane-scope.md:137`) and were opened at the cited line; kengaku's is
   the glob `plans/round-6*-claims.md` (10 files, 9 carrying `--check-receipt`). All resolve as of
   the round-77 base `188562d4`.
2. Round numbers in §2 match the owning registry row where present: `mado SKILL.md:745`,
   `kama SKILL.md:1424`, `chousa SKILL.md:154`, `tsukuroi SKILL.md:2671`.
3. After the L1 lands the block: `git diff --stat` for `.ufo/waves/round-77/claims.json`,
   `plans/round-77-claims.md`, `tools/round-77/verdict-bind.py`, `tools/round-77/prefile-receipt.py`
   → empty.
4. `python3 -I -B tools/round-77/verdict-bind.py --root . --rev <measured> --json-out <scratch>` at
   the new rev → `mismatch_count 0`, `bound_clauses >= 18`, `in_scope_rows >= 11`, defect-free
   `validate`, **identical** to the pre-block receipt (a lesson lands no `## Capabilities` row and
   no PROVINCE bullet).
5. `python3 -I -B tools/round-77/prefile-receipt.py --root . --rev <new> --work <scratch> --battery`
   → `arms_ok 6/6`.
6. `python3 -I -B tools/round-29/freeze-gate.py --rev <new> --disclosures corpus/claim-freezes-v2.tsv`
   → round-77 row still CLEAN, findings `-`.
7. Grep the landed block for the two forbidden edit targets (`claims.json`,
   `plans/round-77-claims.md`) — zero hits asserting a change; and for the L2 sentence, which must
   say *routed to round 78*, not *repaired in round 77*.
