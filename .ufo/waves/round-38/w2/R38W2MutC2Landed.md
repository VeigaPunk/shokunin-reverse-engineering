# R38W2MutC2Landed — mutation probe of the frozen C2 counter at the landed state

**VERDICT: CONFIRMED** — the claim "R38-C2 met (c2 counter at 0fc6113376a156fddc3ec385386d71c3a4a9f690: mismatches 0, guards_ok, exit 0)" reproduces exactly on the landed bytes, the same counter correctly fails at base 77091b492cc53f8743bd0701b1e7d5e66123dd84 (mismatches 1), its selftest is 14/14, and 24 single-logic mutants found no defect in the instrument — the base↔landed discrimination localizes to clauses that are all explicit in the frozen predicate (plans/round-38-claims.md:69 at first freeze e059ca9391642d5b71b6662cabcbdce0d9308719).

## Scope and method

- Attacked claim: R38-C2 met, per c2-counter at the landed commit 0fc6113376a156fddc3ec385386d71c3a4a9f690.
- Detector: `tools/round-38/c2-counter.py` **as committed at 0fc6113376a156fddc3ec385386d71c3a4a9f690** (blob 04a0bc63e9849e1ca1d6abb41814af875fad141f), copied byte-for-byte into scratch (`sha256 7f137b664984595e4d63068a7fa0be2c74a7c57fe5cd5e3a0b794918d2a7b0f7`, identical to the lane worktree file). The counter does not exist at base (this round introduced it); base probing = scoring with `--rev 77091b49… --base 77091b49…`, i.e. "what would the counter have said at the base state".
- All runs read-only (`git show` / `cat-file -e` / `ls-tree` only), run against the lane repo; mutants lived only in scratch copies. Scratch: `/fast/scratch/hyaku/kaidoku-r38/R38W2MutC2Landed` (removed at the end).
- Scoring command (per mutant and pristine):
  `python3 <counter> --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev 0fc6113376a156fddc3ec385386d71c3a4a9f690 --base 77091b492cc53f8743bd0701b1e7d5e66123dd84`
  and the same with `--rev 77091b492cc53f8743bd0701b1e7d5e66123dd84`.
- 24 mutants, one logic change each: pointer resolver (4), range bound (4), unit enumeration (3), count regexes O1–O4 (4), R1–R3 (3), guards (5), LANE gate (1). Each mutant copy asserted to differ from pristine at exactly the intended site.

## Pristine baseline (the oracle both revs must beat)

| scoring rev | met_target | mismatches | unresolved | guards_ok | exit |
|---|---|---|---|---|---|
| 0fc61133 (landed, base=77091b49) | true | 0 | — | true | 0 |
| 77091b49 (base, base=self) | false | 1 | `prov_core:REA MCP server → evidence/doctor/` | false | 1 |
| `--selftest` | 14 cases, green_ok 1, red_ok 13, failures [] | | | | 0 |

Grounded detail (full JSON in artifacts): landed pointers 52 vs base 48; command A landed 126/126 mapped, 17/17 rule blocks; command B 9/9 aligned; craft range [81,314]; Adjacent range [97,125]. Base guards show `unrepaired: [prov_core:REA MCP server, evidence/doctor]` — the exact "base 1 mismatch" the predicate sentence names.

## Mutant scores

Legend: **red**/green = met_target false/true with exit 1/0; mN = mismatches. "≡ pristine" = identical stdout JSON and exit at both revs.

| mutant | clause | at base 77091b49 | at landed 0fc61133 | reading |
|---|---|---|---|---|
| ptr-exists-true | pointer resolver (`exists` → True) | **green m0** | green m0 | **Base turns green**: base-red rests entirely on real `cat-file -e` path existence of `evidence/doctor`. Faking existence destroys all discrimination on this data. |
| ptr-rstrip-drop | pointer resolver (no trailing-slash strip) | red m1 ≡ pristine | green m0 ≡ pristine | Equivalent: git still refuses to resolve `evidence/doctor/` with the slash. |
| ptr-range-no-lo | pointer resolver (drop `1 <= lo`) | red m1 ≡ pristine | green m0 ≡ pristine | Equivalent: no pointer has a sub-1 start line. |
| ptr-range-off-by-one | pointer resolver (`hi <` line count) | red m1 ≡ pristine | green m0 ≡ pristine | Equivalent: no stated ranged pointer ends at its file's last line — boundary strictness untested by this data (coverage gap, not defect). |
| rng-adjacent-stop-h2 | range bound (Adjacent stops only at `## `) | red m2 | **red m1** (R3: stated [97,125] vs observed [97,274]) | **Landed red**: R3 rests on stopping at any `#` heading; PROVINCE `## Adjacent` has `###` subsections down to line 274. |
| rng-craft-stop-h1 | range bound (craft stops at `#`) | red m1 ≡ pristine | green m0 ≡ pristine | Equivalent: craft section contains no deeper headings — stop depth untested there. |
| rng-count-blanks | range bound (count trailing blanks) | red m4 | **red m3** (R1/R2 [81,318] vs [81,314]; R3 [97,127] vs [97,125]) | **Landed red ×3**: R1/R2/R3 all rest on the last-non-blank rule; craft carries 4 trailing blank lines, Adjacent 2. |
| rng-r1-obs-adj | R1 observed range swapped to Adjacent | red m2 | **red m1** (R1 [81,314] ≠ [97,125]) | **Landed red**: R1 is genuinely anchored to the craft range; the check is not vacuous. |
| ue-drop-frontier | unit enumeration (drop PROVINCE Frontier rows) | red m1 ≡ pristine | green m0 ≡ pristine | Equivalent: Frontier rows hold no unresolved pointers at either rev. |
| ue-shonen-cont-4 | unit enumeration (SHONEN continuation = 4 spaces) | red m4 | **red m3** (O4/R2/R3 stated → null) | **Landed red ×3**: SHONEN boxes are 2-space indented; the box parser's indentation contract is load-bearing. |
| ue-caps-nobreak | unit enumeration (caps loop no break) | red m1 ≡ pristine | green m0 ≡ pristine | Equivalent: no stray `\|` rows inside the Capabilities section. |
| o1-loose | O1 regex → `(\d+)/(\d+) knowledge files` | red m1 ≡ pristine | green m0 ≡ pristine | Equivalent: loosened regex still captures 126/126 from the row. |
| o2-typo | O2 regex → `ruleblocks` | red m2 | **red m1** (O2 stated → null, observed 17/17) | **Landed red**: O2 rests on the exact phrase "queue-drain rule blocks". |
| o3-status-overmatch | O3 observed status `!= 'superseded'` | red m1 ≡ pristine | green m0 ≡ pristine | Equivalent: all 9 obligations are `aligned`; no other statuses exist to overmatch. |
| o4-tighten | O4 regex → `queue-drain rule blocks` | red m2 | **red m1** (O4 stated → null) | **Landed red**: box 1 states "17/17 rule blocks" without "queue-drain" — O4's phrasing deliberately differs from O2's; the two are non-redundant. |
| r1-no-backtick | R1 regex without backtick anchors | red m1 ≡ pristine | green m0 ≡ pristine | Equivalent: search finds the same range. |
| r2-no-backtick | R2 regex without backtick anchors | red m1 ≡ pristine | green m0 ≡ pristine | Equivalent. |
| r3-no-backtick | R3 regex without backtick anchors | red m1 ≡ pristine | green m0 ≡ pristine | Equivalent. |
| g-any-repair | guards (repair by any resolving pointer) | red m1 (guards_ok flips **true**) | green m0 ≡ pristine | met unchanged both revs; at base the **unresolved clause**, not the repair guard, is what flags. Sub-observable only. |
| g-exact-repair | guards (repair must be exact path, no suffix) | red m1 ≡ pristine | **red m0, guards_ok false** (unrepaired: evidence/doctor) | **Landed red**: the landed repair is genuinely by same-document suffix (`.ufo/waves/round-19/evidence/doctor/` for `evidence/doctor`); exact-only repair breaks the landed green. |
| g-drop-count-guard | guards (drop `pointers_not_fewer`) | red m1 ≡ pristine | green m0 ≡ pristine | Equivalent: 52 ≥ 48 holds with margin; not the binding constraint. |
| g-drop-missing-units | guards (drop missing-units check) | red m1 ≡ pristine | green m0 ≡ pristine | Equivalent: no units removed. |
| g-tolerance-1 | guards (`mismatches <= 1`) | red m1 ≡ pristine | green m0 ≡ pristine | Equivalent at met: base stays red via `guards_ok=false`; zero-tolerance is not the sole keeper of base-red. |
| lane-drop-evidence | LANE gate (remove `evidence/` prefix) | **green m0** | green m0 | **Base turns green**: with `evidence/` out of the lane-pointer gate the base mismatch is never scanned; discrimination collapses. Base-red rests on the LANE gate including `evidence/`. |

Tally: 15/24 equivalent at met level; 7 turn landed red; 2 turn base green; 0 crashes, 0 exit-2, all 48 runs emitted well-formed JSON with empty stderr.

## Findings

1. **The verdict's discrimination rests on exactly two visible levers**: strict path existence (`cat-file -e`) and the LANE token gate including `evidence/` (mutants `ptr-exists-true`, `lane-drop-evidence`). Both are stated in the frozen predicate ("every backticked lane-repo pointer … resolves at that revision"); neither is hidden. No plausible single-logic mutant makes landed green *and* base green through any other route.
2. **Landed green is honest, not lucky**: seven independent mutants (repair-suffix guard, last-non-blank range rule, `#`-stop for Adjacent, 2-space box continuation, O2/O4 exact phrasing, R1 anchoring) each independently flip landed red — the landed state satisfies seven distinct, separable clauses simultaneously, including the PROVINCE pointer repair being a genuine same-document suffix repair rather than a coincidental resolving pointer.
3. **Redundancy (calibration note, not a contract change)**: the count guard (`pointers_not_fewer`), the missing-units guard, zero-tolerance-vs-guards conjunction, and the same-document repair arm are each individually droppable on this data without changing met at either rev — the counter would still discriminate base from landed if any one guard were removed, but not if LANE gating or existence checking were loosened. Surviving mutants are coverage findings only; per the mutation-tester contract I propose no change to the frozen counter or predicate.
4. **No post-hoc instrument risk for C2**: unlike attempt 1's c1 instrument, `tools/round-38/c2-counter.py` is unmodified in the worktree (status empty for that path; worktree identical to the landed blob; sha256 of lane file = sha256 of the blob extracted at 0fc61133 = `7f137b66…`). The counter that scored C2 is the counter that landed.

## Restoration evidence

- Lane file never edited: mutants were separate scratch copies; `git -C <lane>` used only read-only subcommands (show, cat-file, ls-tree, diff, status, log, rev-parse). No add/commit/checkout/reset/stash, no jj.
- `sha256 tools/round-38/c2-counter.py` before probe: `7f137b664984595e4d63068a7fa0be2c74a7c57fe5cd5e3a0b794918d2a7b0f7`; after probe (post-scratch-removal recheck): identical. Blob at landed rev: `04a0bc63e9849e1ca1d6abb41814af875fad141f`; `git diff --quiet 0fc61133… -- tools/round-38/c2-counter.py` clean.
- Pre-existing sibling worktree state in `tools/round-38/` (c1-counter.py, freeze-drift.py modified; intended-doc.py, registry-immutable.sh untracked) observed and left untouched.
- Selftest fixtures were pointed at my own scratch via `HYAKU_SCRATCH="$S/selftest"`; fixture repos used identity `fixture <fixture@invalid>` inside `mktemp` dirs only, per the fixture rule.

## Tooling

No tools installed or updated (operator authorization not exercised); no pacman transactions; REA not used by this probe.

## Evidence copies (survive scratch cleanup)

- Raw per-run JSON (50 files: pristine landed/base + 24 mutants × 2 revs): `.ufo/waves/round-38/w2/artifacts/R38W2MutC2Landed/out/`
- Naming: `<mutant>.landed.json` / `<mutant>.base.json`; `pristine.landed.json` / `pristine.base.json`.

— R38W2MutC2Landed, 2026-10-26
