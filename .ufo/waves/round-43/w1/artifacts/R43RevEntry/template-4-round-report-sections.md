# Template 4 — Round report required sections (round prompt §4)

Source: `/home/vgpnk/Projects/shokunin/.ufo/prompts/kaidoku-round-43.md` §4
*Report contract*. Report path (fleet repo, L1-written):
`/home/vgpnk/Projects/shokunin/.ufo/reports/round-43/kaidoku.md`.

Required sections, IN THIS ORDER (verbatim headings from the prompt):

1. **Work performed** — opens by naming the round's declared claims (1–3) and
   their target axes or capability; then one bullet per work item, each
   carrying an evidence pointer (path:line, command output, or commit hash).
2. **Landed changes** — every change tied to a LOG.md entry and to the commit
   hash that carries it.
3. **Before → after measurements** — one per claim, each with the counting
   command and the commit it was measured against.
4. **Sources & frontier** — `SOURCES.md` rows before→after with the counting
   command, rows added by tier, rows touched old→new, frontier rows advanced;
   a lane with no `corpus/` writes a line beginning `SOURCES: unchanged —`
   that names why (main-repo lanes: `SOURCES: unchanged — main-repo lanes
   hold no corpus/`). This is a conformance item, not a report marker
   predicate.
5. **Trend verdicts** — one verdict each for `expansion`, `quality`, and
   `discernment` (`improved`, `harmed`, `unchanged`, `unprovable-but-better`),
   with evidence; no scalar.
6. **SHONEN** — one line per box of your SHONEN.md checklist: `[x]` only with
   a named non-author verifier, `[~]` with a resolvable evidence pointer,
   `[ ]` if untouched.

Marker rule (quote the L1 must heed):
> **Marker rule:** a contentless report (placeholder text, missing required
> sections other than **Sources & frontier** and **Trend verdicts**, or no
> evidence pointers) counts as the round **failed** — the driver relaunches
> the same round. A report that names real committed work but skips those
> sections is `ok` plus a minimum-content conformance defect, logged as one;
> neither section is a marker predicate.

Round-43 specifics the L1 must not forget inside those sections:
- **Work performed** opens by naming R43-C1 (depth) and R43-C2 (coverage)
  with their counting commands; wave-1 items each carry an evidence pointer
  into `.ufo/waves/round-43/w1/` or a commit hash.
- **Before → after measurements**: C1 before = the freeze-state exit 2
  `no_manifest_at_rev` (CTL-C1-0) and the round-42 stop receipt at
  `eb8215ac` (78/78 matched, exit 1 on the declared-tuple binding); after =
  the round-43 score receipt at `<<REV>>`. C2 before = gate exit 1 with
  `rows_failed` 18 at the freeze; after = gate exit 0, `rows_failed []`.
- **Sources & frontier**: census before→after via
  `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku`
  (exit 0 required at round end; both outputs pasted with exit codes —
  start census already at `.ufo/waves/round-43/census-start.txt`); S135 added
  (tier A, `mined`); touched rows old→new logged in the lesson; assimilation
  admit + quarantine slice + the `considerthese/`: absent line.
- **Trend verdicts**: evidence per verdict, no scalars. Round-42 closure set
  `discernment: improved` / coverage improved / depth unchanged as the
  non-author reference; the round-43 verdicts are the L1's own with evidence.
- **SHONEN**: check SHONEN.md's current boxes; each line names the box, the
  marker and the verifier or pointer.
