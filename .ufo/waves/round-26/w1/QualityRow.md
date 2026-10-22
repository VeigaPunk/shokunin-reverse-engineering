# QualityRow — routed defect 5: QUALITY criterion for the round-24 source disagreement

Seat KaidokuR26.QualityRow (scribe, leaf). Lane read-only: no lane file edited except
this report. 2026-10-22, 12:16–12:35 UTC. Lane base a0639d8e61e486e2a716ff94cddd89a73200a02c.
Target: `corpus/lessons/round-25-verifier-spotcheck.md:196-197` — the round-24 source
disagreement (initial capinfos rejection, later S071 flip) has no QUALITY criterion;
either add one citing the r24 spot-check or record why the flip covers it.

## 1. Decision

**The S071 flip does not already encode the lesson. Draft QUALITY row 35 below.** The
flip records one *instance*; no admission criterion requires it.

- observation — the reversal is recorded in prose only: `corpus/SOURCES.md:77` (S071
  teaches cell) "the earlier rejection is reversed because its flip condition fired
  (residual review ResHonesty-2 finding 7)"; `corpus/lessons/round-24.md:85-87` "the
  capinfos rejection was wrong and its flip fired"; `corpus/SOURCES.md:137` (search log).
  None is a criterion a future row is tested against, and no QUALITY row in the file or
  in all history covers it (E8, F1, F2): the word "capinfos" never entered QUALITY.md.
- observation — the two record-keeping legs the spot-check names are unfulfilled, so the
  flip cannot stand in for them. (a) The rejected decision is not a registry row: only
  S022 and S028 carry `status=rejected` (E16); the capinfos rejection lives only at
  `corpus/lessons/round-24.md:23`, a lesson table row (E14), and S071's used-by names
  the lesson *file* while no registry cell points at the rejected decision or its flip
  clause (E10). (b) The outside reviewer's disagreement is in no lane artifact outside
  the reviewer's own file: it is absent from SCORECARD (E11) and from LOG.md, whose two
  capinfos hits (`:2770` build, `:2801` residual attribution) do not carry it.
- observation — one leg of the spot-check's ask *was* met: the historical mistaken
  rejection was preserved, not rewritten (E13, E16).
- observation — QUALITY row 34 (`corpus/QUALITY.md:44`) cites the r24 spot-check but does
  not reach this case (E9). Its clauses cover expected-red receipts, revised or replacement
  instrument results reported beside the original, and "The lane's SCORECARD and LOG record
  each outside closure decision (admitted or rejected, with the spot-check path)". The
  capinfos item is a *source* decision in the spot-check's "Outside source decisions" table
  (`corpus/lessons/round-24-verifier-spotcheck.md:44`), not the round-level closure verdict;
  the lane's behaviour shows the gap, since the disagreement is in neither SCORECARD nor LOG
  and row 34 is the only QUALITY row citing the spot-check (F3).
- inference — a criterion is the right remedy because the r24 spot-check's demand is about
  *record-keeping*, not capinfos specifically: keep the mistaken decision visible, keep the
  reversal legible as a reversal, and let the lane's ledger show where an outside reviewer
  disagreed. A one-off row would satisfy r24 and leave the next reversal ungoverned.
- unknown — whether the L1 wants the criterion scoped to source decisions only or to all
  reversed decisions (instruments included); row 34 governs the instrument case.

## 2. Located evidence (command, output excerpt, exit code, UTC)

All commands read-only from the lane root on 2026-10-22. The full log with every line
is `/fast/scratch/hyaku/kaidoku-r26/seats/QualityRow/evidence.txt` (313 lines, sections
E1–E18, C, F, G), which also carries the sha256 of each of the seven files read.

| # | Command | Output excerpt | Exit | UTC |
|---|---|---|---|---|
| E1 | `awk 'NR==44' corpus/lessons/round-24-verifier-spotcheck.md` | "**Disagree with the initial not-needed rejection; agree with its recorded flip.** … Preserve the historical mistaken rejection and corrective S071 rather than relabel it as always correct." | 0 | 12:20:32Z |
| E2 | `awk 'NR==61' corpus/lessons/round-24-verifier-spotcheck.md` | "the capinfos flip and disclosed supersession are useful, but initial rejection was wrong and the strict target remains unmet" | 0 | 12:20:32Z |
| E3 | `awk 'NR==23' corpus/lessons/round-24.md` | "\| capinfos(1) 4.6.9 \| reject as a row \| … Not needed: REA's pcap output already records counts/times. Flip: a claim that depends on capinfos semantics directly." | 0 | 12:20:32Z |
| E4 | `awk 'NR>=84 && NR<=87' corpus/lessons/round-24.md` | "`PcapProvider.js:330` reads `capinfos -M`; its counts/times support the holding, so the capinfos rejection was wrong and its flip fired: admitted S071" | 0 | 12:20:32Z |
| E5 | `awk 'NR==77' corpus/SOURCES.md` | S071: "the earlier rejection is reversed because its flip condition fired (residual review ResHonesty-2 finding 7)"; `:106` "S064 → S069 → S071 → S070 → S067"; `:137` "its exclusion is reversed: S071 admits it" | 0 | 12:20:32Z |
| E8 | `grep -n -i -E 'flip\|rejection\|source row\|capinfos\|S071\|S066' corpus/QUALITY.md` | (no matches) | 1 | 12:20:32Z |
| E9 | `awk 'NR==44' corpus/QUALITY.md` | row 34 verbatim; clause "The lane's SCORECARD and LOG record each outside closure decision (admitted or rejected, with the spot-check path)" | 0 | 12:20:32Z |
| E10 | `grep -n 'round-24.md:23' corpus/SOURCES.md` | (no match) | 1 | 12:21:28Z |
| E11 | `grep -c -i capinfos SCORECARD.md` | `0` — the disagreement is in no lane ledger | 1 | 12:21:28Z |
| E12 | `awk 'NR>=42 && NR<=49' .ufo/waves/round-24/residual/KagiR27-2.ResHonesty-2.md` | finding 7: "The capinfos rejection is factually wrong, and its own flip condition is met." | 0 | 12:21:28Z |
| E14 | `awk 'NR>=113 && NR<=116' .ufo/waves/round-24/residual/KagiR27-2.ResSources-2.md` | "The capinfos rejection lives only in the lesson, not as a registry row with `status=rejected`" | 0 | 12:21:28Z |
| E13 | `git log --oneline -L 23,23:corpus/lessons/round-24.md` | only 69e82c48 (creating commit); `git blame -L 23,23` names the same commit | 0 | 12:21:28Z |
| E17 | `awk 'NR>=196 && NR<=197' corpus/lessons/round-25-verifier-spotcheck.md` | the routed defect text | 0 | 12:21:28Z |
| F1 | `grep -nE '^\| [0-9]+ \|' corpus/QUALITY.md \| grep -icE 'flip\|rejection\|source row\|capinfos'` | `0` | 1 | 12:26:42Z |
| F2 | `git log --oneline --all -S capinfos -- corpus/QUALITY.md` | (no output); the same for `S071` | 0 | 12:26:42Z |
| F3 | `grep -nE '^\| [0-9]+ \|' corpus/QUALITY.md \| grep -c 'round-24-verifier-spotcheck'` | `1` (row 34 only) | 0 | 12:30:47Z |
| E16 | `grep -nE '^\| S[0-9]+ \|' corpus/SOURCES.md \| grep -c 'rejected'` | `2` (S022, S028) | 0 | 12:30:47Z |

Digests of the seven files read (2026-10-22): QUALITY.md e200c853a31c00fc15ff56c6889f2bffa01a612393a4ee115188c35c4e9cbfb0 · SOURCES.md 002b8e17ec0876076c9aa632c511ac2812ce72aef46f152c016b27c51b1c62dd · round-24.md 98b6e54420b8eb74d6fea48c882130cd7ce3e1a9970f6fbf3812f75f7283c1d3 · round-24-verifier-spotcheck.md 653517f846b7e166baf3b7ba71904c513ab52cb9ba2b35fbf52c689f36bdd2c5 · round-25-verifier-spotcheck.md 3d6bc116ff538843efb8556d7508c440f128096eb4788c01aeb48248bd707948 · ResHonesty-2.md a36f871265c1e6e4613040f1ebddca44069b219268c5e80924d70d47f299a1d9 · ResSources-2.md 7d463961d34645db73ce91b0d19e0f4ce5af1ebebc3caae617884264397f30f4. No external source was opened: every input is a local lane file read with plain `awk`/`grep`/`git`. No REA run, tool install, git write or jj command.

## 3. Draft QUALITY row 35 (not applied; the L1 decides)

Paste after row 34 at `corpus/QUALITY.md:44`. Style follows rows 30–34: criterion cell,
why-cell citing the lesson with paths and line numbers, supersedes cell.

```
| 35 | A source decision that a later round or an outside review reverses is recorded as a reversal, not laundered into a first-time decision: the rejected decision stays locatable with its stated reason and its flip condition, and the admitting row names the decision it reverses and the evidence that fired the flip. When an outside reviewer disagrees with a lane source decision, the lane's own SCORECARD and LOG record that disagreement with the spot-check path and line, beside the round-level verdict they already carry. Fails when the rejected decision survives only as prose in a lesson table with no registry row and no flip clause, or when the outside reviewer's source-level disagreement appears in no lane artifact other than the reviewer's own file. | `corpus/lessons/round-24-verifier-spotcheck.md:44` ("Preserve the historical mistaken rejection and corrective S071 rather than relabel it as always correct") and `:61` ("initial rejection was wrong"); `corpus/lessons/round-24.md:23` (the rejected capinfos decision and its flip clause), `:85-87` (the fired flip); `corpus/lessons/round-25-verifier-spotcheck.md:196-197` (routed defect 5) | sharpens 34 |
```

Falsifiers a reviewer can run (read-only, all observed on the current lane): the
`status=rejected` count is today `2` (S022, S028), so a lane holding the capinfos
rejection only at `corpus/lessons/round-24.md:23` fails the "locatable" clause;
`grep -n 'round-24.md:23' corpus/SOURCES.md` exits 1 today, so the admitting row names
the lesson file but not the rejected decision and the reversal is not auditable;
`grep -c -i capinfos SCORECARD.md` is today `0`, so the reviewer's source-level
disagreement is in no lane ledger; and `git log --oneline -L 23,23:corpus/lessons/round-24.md`
lists only 69e82c48 today, so a later edit to the rejected line breaks the "not laundered"
clause.

Counter-check that row 35 disturbs nothing existing: `tools/round-25/a2/c1-calibration.py:70-71`
computes I3 as `any(SPOT.split("/")[-1] in ln for ln in rows)` — an *any* test over QUALITY
rows, so a second row citing the r24 spot-check cannot turn the frozen R25-C1 counter red
(`grep -n 'any(SPOT.split' tools/round-25/a2/c1-calibration.py`, exit 0, 12:24:15Z). No
counter in `tools/` asserts a QUALITY row count (searched 12:28:36Z).

## 4. Out of scope, sibling overlap, artifacts

- `corpus/QUALITY.md`, `corpus/SOURCES.md`, `SCORECARD.md`, `LOG.md` were not edited by
  this seat; the row above is a draft for the L1. (`git status --porcelain` shows
  `M corpus/SOURCES.md` — sibling seat work adding S079/S080, not this seat.)
- Side defects noticed in the same material, listed so the L1 does not lose them: the
  S071 teaches cell says the flip condition "fired" without saying it was already met at
  rejection time (`corpus/SOURCES.md:77` vs `corpus/lessons/round-24.md:23`); the
  outside disagreement is in neither SCORECARD nor LOG; `corpus/lessons/round-24.md:23`
  has no forward pointer to the reversal at `:85-87`. No REA run (the criterion is about
  the lane's records, not REA evidence) and no instrument written (row 35 is checkable
  with plain `grep`/`git`; a machine gate is a separate seat).
- Sibling overlap: seat KaidokuR26.CapinfosFacts (reviewer) independently reached the
  same verdict — the flip records the instance, not the rule — and drafted its own row
  35 in `.ufo/waves/round-26/w1/CapinfosFacts.md` §7 (lines 61–66). That draft is a
  *different* rule: search the installed consumer code before rejecting a source as
  "not needed". Mine is the record-keeping rule and cites the r24 spot-check by path and
  line, as this card asked. Only one can be row 35; the L1 should take one as row 35 and
  the other as row 36, or merge. The two do not conflict and both cite
  `corpus/lessons/round-24.md:23`. Artifact: `/fast/scratch/hyaku/kaidoku-r26/seats/QualityRow/evidence.txt`,
  sha256 `f25c09aa64427f4b8e25444b7838510906b43bd7cedca8ae0f7bd6d5b733b80f`.
