# Seat report — SC-1 (chain c1, role scribe)

Wave `arc3-loop1-round4` · 2026-10-19 · HEAD `015e1bab914713568f339fd53999bc180459cc40`
at every read (`git rev-parse HEAD`; repo untouched — `git status --porcelain
corpus/ SKILL.md LOG.md SCORECARD.md` empty at each check). Writes by this seat
ONLY: `.ufo/waves/arc3-loop1-round4/seats/SC-1.md` (this report) +
`.ufo/waves/arc3-loop1-round4/claims/c1/records-drafts/{chain-ledger.draft.md,
knowledge-entry-draft.md,map-token-patch.md,records-drafts.md}` + the evidence
set and identity table in `.ufo/waves/arc3-loop1-round4/claims/c1/SC-1/`. No git
mutations; no LOG/SCORECARD/SHONEN/corpus/SKILL/PROVINCE/README edits; custody
paths never opened for writing. Scratch: `/var/tmp/sc1-r4/` only (`/tmp` EDQUOT
standing hazard).

## 1. Work performed (evidence pointers)

- **Before-state, re-measured first-hand at HEAD** (`SC-1/evidence/`):
  - command A (SCORECARD recipe A, verbatim) →
    `{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [],
    "depth_score": 10.0, "knowledge_files": 83, "mapped": 83, "missing": [],
    "revision": "015e1bab…", "rule_blocks": 14}` — matches RV-2's
    `evidence/commandA-before.txt` and VZ-1's `evidence/baseline-commandA.json`.
  - census instrument `.ufo/gates/c1-census-v10.py` → **PASS
    `stale=0 ambiguous=0 undeclared=0 unresolved=0`**, exit 0, scope-errors `[]`,
    unreadable `[]`, G2 floor 17/14/3.
  - citation-drift probe at HEAD → `reported findings=0 exit=0`; selftest
    **13/13 CLEAN**.
  - custody-pair selftest → **`CLEAN cases=22 passed=22 failed=0`**.
- **Five probe legs run first-hand** (not copied from other seats), disk-backed
  `TMPDIR=/var/tmp/sc1-r4/probe-tmp`:
  `CarrierV` hex @6.4.0 (`ev_d1792f57…`, **15/15**), raw @6.4.0
  (`ev_eac08124…`, 15/15), hex @6.7.0 (`ev_62e1b9e6…`, 15/15); `Smoke` hex
  @6.4.0 (`ev_073f845c…`, 4/4); `CarrierV` creation hex @6.4.0
  (`ev_53732d0f…`, 0 — parsed-and-empty). Envelopes at
  `SC-1/evidence/probe-*.json`.
- **Byte-level re-derivations by this seat** (independent of the seats that
  reported the same findings):
  - Vyper dispatch mechanism: prologue decode, the 13-entry `uint16` jump table
    at `0x600` (every entry a `0x5b` JUMPDEST; `0x5e7` ×3 sentinel), the
    `bucket = selector % 13` rule, the 15 `PUSH4;DUP2;XOR;PUSH2;JUMPI` compare
    sites, and the chain-walk from each bucket head to its site — all 15
    selectors reach their own site.
  - Offset rule: **0 of 15** reported offsets land on a JUMPDEST; every one is
    `push4_pc + 11` (the fall-through body entry), and the compare-site
    JUMPDEST at `offset−12` carries that function's own selector — re-derived
    on `CarrierV` (15/15) and `Smoke` (4/4).
  - Zero false positives: `08c379a0` (×6) and `69656e74` are the only
    non-selector `PUSH4` immediates; neither reported. The `__default__()`
    method-identifiers key (`89402a72`) is **ABSENT** from the runtime bytes.
  - Mutability comparison against the compiled ABI for all 15 functions: 7 agree,
  8 read `payable` (ABI: view ×5, nonpayable ×2, pure ×1), no case more
  restrictive, no selector misassigned.
- **The four draft artifacts** (the deliverable; parent lands, nothing applied):
  - `records-drafts/chain-ledger.draft.md` — the evidence-chain ledger
    (frozen inputs → R0–R8 rows with sha256 prefixes → row details → the
    before→after measurement → footer). Modeled on the r1/r3 predecessors.
  - `records-drafts/knowledge-entry-draft.md` — the round's corpus entry as
    **patch text** (RESULT-class, family-scoped, no availability→holding),
    literal text between markers, honest-stop branch stated as not triggered,
    parent notes after the markers. **Revised to rev 2 after RV-2's grade**
    (six fixes applied; see §4.10).
  - `records-drafts/map-token-patch.md` — the **ADDITIVE-ONLY, line-neutral**
    token patch for `corpus/README.md:38` (the r3 PRIMARY form), with the
    apply recipe, the rehearsal table, and the verification obligations.
    **Unchanged across both revisions** (`8e3f91e3…`), so VZ-1's snapshot of it
    still matches.
  - `records-drafts/records-drafts.md` — the LOG entry draft + SCORECARD
    round-section draft (C1 bullets and C1 axis rows complete; C2/C3 slots
    **point at the sibling drafts that landed this round**, not left blank),
    plus the merge map for the parent. **Unchanged across both revisions**
    (`a93ed42d…`), so CN-2's fold of it remains faithful.
- **Chain verdict (landed at 14:15Z, after this seat's first revision):**
  `claims/c1/verdict.md` reads **VERIFIED**; RV-2's grade
  (`claims/c1/RV-2/quality-grade.md`) reads **ACCEPT-WITH-FIXES** with all hard
  gates PASS. This seat applied the six fixes and re-measured (§4.10); the
  parent should re-grade rev 2.
- **Rehearsal (scratch tree, the lane repo never written):** `git archive HEAD`
  → `/var/tmp/sc1-r4/rehearsal/tree`; the entry literal landed as
  `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md`; the PRIMARY token
  substitution applied. Result: **84/84, missing [], dangling [], rules
  14/14**; README 190 → 190 lines with exactly one differing line (`:38`); the
  prior 83 knowledge files **byte-identical** (compared against RV-2's
  `evidence/prior-83.sha256`, 83/83 rows: added = the new stem only, removed =
  none, modified = none).
- **Census projection (this seat's own run):** base tree PASS `0/0/0/0`; merged
  tree (+ this seat's 178-line records literal) **PASS `0/0/0/0`** — zero added
  loci; control tree (+ one planted pin literal) **FAIL `undeclared=1`** — the
  check is non-vacuous.
- **Pin-free check (this seat's own run, the wave's CN-2 checker):**
  `records-drafts.md` **CLEAN** (0 tokens) and `map-token-patch.md` **CLEAN**.
  The ledger (40 tokens) and the entry draft (47 tokens) are **not landing
  surfaces** — the ledger must quote exact reproducing calls, and
  `corpus/knowledge/` is outside the census's declared scope while QUALITY #6
  requires the entry's `recheck:` line to carry the reproducing call; the r1/r3
  landed entries carry that same form (verified on the r3 pair with the same
  checker).
- **Identity discipline (rule #14):** all four draft hashes re-derived after
  the final writes — `SC-1/README-identities.txt` is the canonical table
  (drafts, literal blocks, evidence files). **VZ-1's independent snapshots are
  byte-identical to this seat's final files** (`cmp` exit 0 on both:
  `df9582ac…` entry, `8e3f91e3…` token patch). CN-2's merge fold carries this
  seat's C1 bullet and axis row.

## 2. Proposed changes

**Patch texts only** (this seat writes no repo surface):

| target | patch text | form |
|---|---|---|
| `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md` (new file) | `records-drafts/knowledge-entry-draft.md` (literal block, 32 lines / 20,325 B / `17320917…` — rev 3, after RV-2's fixes and CR-1's scope notes) | new entry, RESULT-class |
| `corpus/README.md:38` | `records-drafts/map-token-patch.md` (PRIMARY line) | ADDITIVE-ONLY, line-neutral (190 → 190) |
| `LOG.md` (EOF append) | `records-drafts/records-drafts.md` (LOG block) | new round entry; C2/C3 merged from siblings |
| `SCORECARD.md` (EOF append) | `records-drafts/records-drafts.md` (SCORECARD block) | new round section; C2/C3 merged from siblings |

**No other change is proposed.** Two tool-level observations are recorded in
the ledger's control row but **no patch text is drafted for them** (they are
not this chain's edit target): the offset-semantics reading in the r1/r3 corpus
entries is solc-scoped and would read more accurately scoped; and the
mutability inference diverges one-directionally on the Vyper family.

## 3. Before→after measurement for chain c1's claim

Claim under test: at least one Vyper-compiled contract's selectors are
recovered by `inspect-evm-interface` K/K against Vyper's own ABI-derived
selector set (or the extractor's behavior is sealed as a typed result), landing
as a corpus entry + line-neutral map token, with command A re-measuring 83 → 84
and the prior 83 byte-identical.

- **Before (measured, my run, recipe A verbatim at HEAD):**
  `{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [],
  "depth_score": 10.0, "knowledge_files": 83, "mapped": 83, "missing": [],
  "revision": "015e1bab914713568f339fd53999bc180459cc40", "rule_blocks": 14}`
  (`SC-1/evidence/command-A-before.json`).
- **Chain-side after (measured now, independent of landing):** the Vyper
  carriers' selectors **are** recovered K/K — 15/15 (`CarrierV`, three legs of
  my own), 4/4 (`Smoke`), and cross-seat 7/7 (`Ex09Vault`), 22/22
  (`StewardToken`, ERC-20-bearing), 9/9 (`CarrierW`). The claim's success
  branch is satisfied; the honest-stop branch (venv infeasible / typed refusal
  / partial recovery) was **not** triggered — the install succeeded and every
  runtime leg recovered its planted set with zero missing / zero extra.
- **After (command A 83 → 84): REHEARSED, NOT LANDED.** The scratch-tree
  rehearsal reads **84/84, 14/14, missing [], dangling []** with the prior 83
  byte-identical and README line-neutral. **GAP — parent-side:** the entry and
  the token had not landed at this seat's close, so this seat does **not**
  claim 84 at the records commit. An unrun check has not passed.

## 4. Attacks/refutations attempted, with verdicts

1. **Falsify "zero extras" by byte census.** `CarrierV`'s runtime carries two
   non-selector `PUSH4` immediates (`08c379a0` ×6, `69656e74` ×1) plus a
   phantom method-identifiers key. **Verdict: refuted** — the probe reported
   exactly the 15 planted selectors, none of the decoys; zero false positives
   holds at byte level.
2. **Falsify the r1/r3 offset reading on this family.** Checked all 15 reported
   offsets against the runtime bytes: 0 land on `0x5b`. **Verdict: the reading
   is refuted for Vyper** — it is solc-scoped. I then derived and verified the
   replacement rule (`offset = push4_pc + 11`, the compare site's fall-through
   body) on two carriers, and confirmed the compare-site JUMPDEST carries the
   function's own selector, so the offsets are still selector-bound, not noise.
3. **Falsify the dispatch-shape claim by chain-walking.** Predicted each
   selector's bucket by `% 13` and walked from the table entry to the matching
   compare site: **all 15 land correctly**, and every table entry is a
   JUMPDEST. **Verdict: holds** — the modulo jump table is the real mechanism,
   not an artifact of one site.
4. **Falsify "mutability inference is sound on this family."** Compared the
   probe's inference against the compiled ABI for all 15 functions.
   **Verdict: partially refuted** — 8 of 15 read `payable` for
   view/nonpayable/pure functions (one direction only; no selector
   misassigned). Recorded in the entry as an observed upstream-inference delta
   with its scope, not smoothed and not called a defect.
5. **Falsify "the K/K result is the extractor parroting a planted list."**
   The planted set was recorded pre-compile/pre-probe (`recorded_utc`
   14:05:46.622429Z, before the first probe file); two independent derivations
   inside that seat plus four implementations in a second seat agree; the
   probe's decoded digest equals the carrier file's own sha256 on every leg.
   **Verdict: refuted.**
6. **Falsify "the map token is line-neutral / additive-only."** Rehearsed the
   substitution on a scratch tree and diffed against `git show HEAD:corpus/README.md`:
   exactly one line differs (`:38`), 190 → 190, token occurrences 85 → 86,
   unique 83 → 84, prior 83 knowledge files byte-identical. **Verdict: holds.**
7. **Falsify the pin-free claim on my own drafts.** Ran the wave's checker:
   the records draft and token patch read CLEAN; the ledger and entry draft
   carry tokens **by design** (they are not landing surfaces — verified against
   the r3 precedent with the same checker). **Verdict: the claim is scoped
   correctly; the two landing-surface files are clean.**
8. **Falsify the census non-vacuity.** Projected my records literal onto a
   scratch tree: PASS `0/0/0/0` with zero added loci; planted-pin control FAILs
   `undeclared=1`. **Verdict: the pass is non-vacuous.**
9. **Self-identity staleness on my own artifacts (rule #14).** VZ-1 snapshotted
   my drafts independently at 14:10:48Z and both matched at that moment
   (`cmp` exit 0). **Then RV-2's grade landed and I applied six fixes, which
   invalidated the entry-draft snapshot** — the table's cross-check section now
   states that plainly rather than carrying the rev-1 claim forward (`cmp`
   exit 1 on the entry draft, exit 0 on the token patch, both re-verified).
   **Caught defect, recorded not smoothed:** while adding this report's own row
   to the identity table I typed a hash tail that did not match the file (the
   first 16 hex digits were right, the remaining 48 were not). The verification
   pass re-derived every row from disk and caught it; the row was corrected.
   Verifier: `python3 - <<'PY' … re.finditer over the table … sha256 vs quoted
   … PY` — re-run after every revision, most recently at 14:31Z,
   **rows checked: 11, BAD: 0**. A hash that was not re-derived has not been
   checked, including my own.
10. **RV-2's grade and the six fixes (applied, then re-measured).** RV-2 graded
    the entry **ACCEPT-WITH-FIXES** (all hard gates PASS; none of the fixes
    changes a measured result). Applied: **F1** the inventory citation now
    names `SC-1/c1-inventory.txt` at the seat root; **F2** the EX-09 brace
    expansion no longer over-claims (`0x`-prefixed legs exist at 6.4.0 only,
    stated inline and corrected in two further places); **F3** the
    "own five probe envelopes" wording now states that same-path legs across
    seats are byte-identical *by determinism*, not independent corroboration,
    and names the different-path legs that are; **F4** the id-domain observation
    now cites `corpus/QUALITY.md` row 15 and the two corpus files it names;
    **A1** the id-domain sentence leads with the true path-sensitivity legs;
    **A2** the ledger's stale `custody-stat-readonly.txt` pin is re-derived
    (`f9ae3dbc…` → `67b1014e…`, the producer revised the file after my read)
    with the correction recorded in the row. **Re-measured after the fixes:**
    citation resolver **0 unresolved cited paths** (was 1); rehearsal re-run
    **84/84, 14/14, prior 83 byte-identical, README 190 → 190, one line
    differs**; pin-free still **CLEAN** on both landing surfaces. The parent
    should re-grade rev 2 against the same gate list rather than trusting this
    seat's own application.
11. **CR-1's report (landed 14:23Z) and the two scope notes it required.**
    CR-1 measured that a **shape-blind extractor returns empty on a fully
    recovered Vyper carrier** — a solc-shaped `EQ;PUSH2;JUMPI` extractor gives
    0 on all 33 carriers while the probe recovers K/K on each (a "false
    honest-stop" hazard), and the round's own reconciler `EX-08/recon.py`
    parses Form A only (0/8 on `--no-optimize` and `-O codesize` while the
    probe reads 8/8 on both). Applied: the entry's EX-08 citation now carries
    the Form-A scope inline, the ledger's extraction bullet does the same, and
    the entry's Unknowns line names the uncharacterized optimizer forms. CR-1
    also measured a **count-only comparison trap** (a tampered carrier keeps
    n = K while its set changes): the ledger now states explicitly that every
    K/K statement in this chain is a **set-equality** statement, never a count.
    **Re-measured after these edits:** citation resolver **0 unresolved
    paths**; rehearsal re-run (rev 3) **84/84, 14/14, prior 83 byte-identical,
    README 190 → 190, after-sha `1cd05260…`**; pin-free still **CLEAN** on both
    landing surfaces. CR-1's finding is thus folded in as scope, not as a
    change to any measured result.
12. **Would the honest-stop branch have been needed?** Checked the environment
    the claim pre-accepted as a risk: the host has no system pip module and no
    pip on PATH, and `python3` is 3.14.7. **Verdict: not triggered** — the
    install succeeded via the stdlib venv module and the compiler runs; the
    branch stays pre-written in the entry for the parent's landing-time check.

## 5. Blockers

None for this seat's task. Named gaps at close (not mine to close):

- **The landing chain is parent-side and unlanded**: the entry file, the map
  token after-state, command A at the records commit (84), the custody
  post-pair, and the work/records commits. This seat's drafts are patch texts;
  the rehearsal is a scratch-tree measurement, not a landing.
- **Sibling seats:** at this seat's first close (14:22Z) 19/48 seat reports had
  landed and the c1 verdict was not yet written; **by 14:33Z the chain verdict
  had landed** (`claims/c1/verdict.md` **VERIFIED**; RV-2's grade
  ACCEPT-WITH-FIXES) and seat reports were at 43/48. The c1 chain's own
  verdict seats (RV-1, RV-2, VZ-1) all landed. **Gap:** CR-1 produced source
  artifacts (a Vyper recon/disassembly suite) but no seat report and no
  verdict-bearing file at this seat's close; its findings are not folded into
  this seat's drafts.
- **Landing-time obligations this seat cannot discharge** (named, not assumed):
  re-grade rev 2 against RV-2's gate list; re-derive every identity at the
  records commit from real Git objects; re-run command A at the records commit;
  capture the custody post-pair; confirm the entry stem still equals the map
  token after any parent edit.
- **Wave-level:** the dispatch defect class from the prior rounds (report
  shortfalls) may recur; this report records only its own seat's state. The
  hyper-lane 402 substitution is recorded in the freeze and in the drafts'
  dispatch bullets with cause, not as a lane signal.
- **Carried unknowns** (in the entry): Vyper versions other than the installed
  one; solc versions other than the r1/r3 pin; `viaIR`; optimizer runs other
  than 200; whether the offset rule and the payable-read delta generalize
  across Vyper versions; the `ev_` id domain for this verb family (measured
  path-sensitive, formula not derived).
