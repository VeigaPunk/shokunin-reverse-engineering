# CriticCensusRekey — attack on any re-key that turns the census FAIL→PASS for SCORECARD 2380-2382 / SKILL 511-519

Role: UFO-FSD critic, read-only. Test rig: `/tmp/kr20-CriticCensusRekey` clone at baseline `14f0260a` (rev-parse confirms, exit 0) plus gate variants under `/tmp/gate-v*.py`. No installs.

## Observed baseline

`cd /tmp/kr20-CriticCensusRekey && python3 -I -B .ufo/gates/c1-census-v10.py --root . --quiet` → `VERDICT: FAIL (stale=0 ambiguous=0 undeclared=2 unresolved=0)` (observation; text-mode wrapper masks exit 1, JSON run confirms verdict FAIL/exit 1). The two undeclared loci (observation, `--json`):

- `SCORECARD.md` block 2380-2382: bare `6.5.0` (:2380) + bare `6.7.0` (:2381), no client token → AMBIGUOUS each, block UNDECLARED. Text = round-17 Limits bullets.
- `SKILL.md` block 511-519: bare `6.5.0` (:512) → AMBIGUOUS, block UNDECLARED. Text = retained round-17 corpus guide.

Live anchors re-derive to `{devin,omp,kimi}=6.7.0`; caches hold 6.5.0+6.7.0 (observation: `ls ~/.npm/_npx` + package.json grep).

## Re-key shapes measured (all in the clone; SCOPE-table edits only)

| variant | change | verdict | notes |
|---|---|---|---|
| v1 `gate-v1-dated.py` | `("SCORECARD.md",2370,2394,"DATED",2374,r"round-17")` + `("SKILL.md",509,530,"DATED",509,r"round 17")` | **PASS** exit 0 | `:2380/6.5.0`→historical(dated), `:2381/6.7.0`→current-ok (G16 live-anchor), block→info; `:512/6.5.0`→historical |
| v2/v5 `gate-v5-current.py` | both regions CURRENT | FAIL ambiguous=2 | no client token in clause; CURRENT cannot pass the text as written |
| v3 `gate-v3-tail.py` | `SCORECARD 856-2567`, `SKILL 21-623` DATED | **PASS** exit 0 | the exact "tail expansion" refuse at gate docstring :26-33 |
| v4 `gate-v4-shadow.py` | DATED 2370-2394 **then** `("SCORECARD.md",2380,2382,"CURRENT",…)` | **PASS** + needle historical | first-match-wins shadow |
| v6 `gate-v6-degenerate.py` | DATED rows marker=`r"6\.5\.0"` keyed on the locus line | **PASS** exit 0 | G15/G18 satisfied, marker dates nothing |

Creep differ (`scope-diff.py gate-base.py gate-v1-dated.py`, exit 1): v1 → `CREEP FLAGS: []` (row additions only); v3 → two `CREEP wide added DATED row` flags.

## Suppression counterexamples (observed on the clone)

1. **DATED-shelter — the primary suppression class.** Plant `omp pins rea-agents@6.3.0 on this host.` inside the new row (SCORECARD :2382): v1/v3/v4 all return `VERDICT: PASS` with the det reading `historical (dated scope)`. Base gate reads it `STALE (live omp=6.7.0)` inside the UNDECLARED block. This is the declared tradeoff at gate docstring :26-33 ("t5-dated-shelter / widen-swallow") — the instrument's DATED class means "literals are immutable facts of a past observation", so any DATED re-key converts live-claim grading into record-keeping for every literal in span.
2. **First-match shadowing.** `scope_of()` returns on first matching row (gate :400-404). A patch that adds *both* an honest-looking `CURRENT` row and a `DATED` row earlier in SCOPE silently grades DATED: v4 PASSes with the client-attributed stale pin historical. `scope-diff.py` cannot see this (it compares row sets, not overlap order).
3. **Degenerate marker.** G15 checks regex-on-marker-line, G18 checks line-in-range (gate :407-424); nothing requires the marker to be a date/round token. `r"6\.5\.0"` keyed on the locus line itself passes and the row still shelters (v6). Standing rule (docstring :41-45) says "the section's own date/round token" — it is a convention, not an enforced check.
4. **`--json` drops `info` blocks.** `main()` JSON keys (:700-710) omit `info`. The clean v1 run puts block 2380-2382 in `info` (mixed historical+current-ok); a reviewer reading only the D5 `--json` record sees zero trace of either new DATED row's grading. Fixable defect: add `info` to the JSON keys.
5. **Differ docstring vs code.** `scope-diff.py:6` claims to flag "end is the last line of file"; the code (:39-43) implements only `e >= 9000`. Cosmetic here — any fixed end fails closed on growth — but the advertised flag is not a witness.
6. **Fail-closed bound holds** (observation): pin planted just past v1's row end → `undeclared=1` FAIL exit 1.

## Classification: what is suppression vs acceptable

- **Suppression**: any DATED row covering version literals that are *live-state claims* (who/what is pinned or used now), the tail-capture pattern (v3, refuse-listed), shadow-order rows (v4), degenerate/self-referential markers (v6), or any text edit to the locus files shipped as part of the "re-key" (a CURRENT pass requires laundering: add a client token → STALE if wrong, or a G17 keyword `doctor|expects|skill|reports|aligned|stale` → `current-ok` via cache check for the *stale* value — worst outcome, it *blesses* stale).
- **Acceptable (narrowest honest)**: a per-region DATED row whose every version literal is a fact-of-record. Both loci qualify — SKILL's `REA 6.5.0 analyze` describes the immutable round-17 run bound to `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md` (observation: SKILL.md:511-519 names the 8 bound runs S003/S023/…); SCORECARD's `REA 6.5.0's … session directory` is a fact of the round-17 capability row (SCORECARD.md:2370-2394), while `6.7.0` stays graded via G16 → current-ok. `CURRENT` is *not* the true class for either: the text fails the run as written (v5), so a CURRENT patch is only PASSable by rewriting the statement — evidence the statement is a record, not a live surface.

## What the reviewer must see to accept

1. `scope-diff.py before after` output with `CREEP FLAGS: []`, `REMOVED (0)`, `CHANGED (0)` — i.e., *added rows only*, no CURRENT→DATED flip, no widening, both added DATED rows ≤150 lines (differ :42) and ending inside the file, not at an EOF-adjacent open bound.
2. Each new row's `marker_line` inside its own range (G18) carrying that record section's *own* round/date token — `round-17` at :2374 for SCORECARD, `round 17` at :509 for SKILL — not a content literal like `6\.5\.0` (v6 hole) nor a date lifted from another row's range.
3. The row diff confined to the `SCOPE = [` table — no needle/verdict/out-key changes; and **no file-text diffs** to SCORECARD.md/SKILL.md in the same patch.
4. A per-detector listing of the two formerly-UNDECLARED blocks under the new key (text mode `--quiet` hides it): `:2380/6.5.0→historical`, `:2381/6.7.0→current-ok` (live-anchor, keeps reconciling), `:512/6.5.0→historical`; each cited literal shown time-invariant.
5. No overlapping earlier DATED row covering the same span — diff alone is insufficient; reviewer must check *order and overlap* in the full SCOPE table (v4).
6. Explicit acceptance of the standing residual: any *future* version literal appended inside the new span grades historical, not live (my planted `rea-agents@6.3.0` proved it); the only guards are span tightness and the records-commit rule (docstring :41-45). This is a tradeoff the canonical judge must knowingly accept, not a defect the author can fix without a new check.

## Smallest safe correction

Two added DATED rows, section-tight: `("SCORECARD.md", 2370, 2394, "DATED", 2374, r"round-17")` and `("SKILL.md", 509, 530, "DATED", 509, r"round 17")` — measured PASS exit 0, `undeclared=0`, creep-differ clean. Even tighter rows bound to the locus bullets alone (SCORECARD 2380-2382 / SKILL 511-519) shrink the shelter surface further and are the strictly safer variant if the reviewer prefers locus-granularity over section-granularity; both read PASS. Optional instrument hardening outside re-key scope: emit `info` in `--json` and reject non-date/round marker regexes (closes holes #4/#3).
