# Round 30 mined mistake and QUALITY criterion — scoped draft

## Draft texts

### Proposed `## Mistakes` entry for `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/lessons/round-30.md`

| id | class | evidence pointer | captured-by | fix and how it was shown able to fail |
|---|---|---|---|---|
| M30-1 | A re-score of an already-held rule on new author-built inputs was called a coverage move, while the completeness-only target was also met by the trivial baseline. | `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/lessons/round-29-verifier-spotcheck.md:44,50-56,123-124` | Round-29 outside verifier spot-check, routed defects 1–2. | Require a coverage claim to identify a newly governed surface and a base-comparison command; score the do-nothing, junk-row, all-false, no-reader and id-keyed shortcut controls before data, and re-design before data if any control meets the target. Designated fix: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-30/axis-fit-gate.py` (assigned to ExecAxisFitGate; not built or run by this scribe). No control-failure demonstration was produced by this scribe. |

### Proposed QUALITY row 48 for `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/QUALITY.md`

| 48 | A coverage claim names the surface it moves and a command that shows it unmoved at the base. Every claim's counter is scored on the do-nothing, junk-row, all-false, no-reader and id-keyed shortcut controls before data, with receipts committed before the first data commit; a control that meets the target forces a re-design before data. Fails when a claim does not identify a surface newly governed against its base state, a control is omitted or its receipt is committed after the first data commit, or a control meets the target and data proceeds without a re-design. Round-29 case: C1 re-scored an already-held rule on new author-built inputs without moving a surface; the frozen completeness target was also met by the trivial baseline (`openchain_first` scored 152/152/0). | `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/lessons/round-29-verifier-spotcheck.md:44,50-56,123-124` | — |

## Evidence and provenance

- **Observation — re-score is not a coverage move; target lacks discrimination.** Producer: `functions.read` on `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/lessons/round-29-verifier-spotcheck.md:35-57`. Exact returned excerpts: line 44 says `openchain_first` is `named 152, right 152, wrong 0`, the trivial baseline does at least as well as the primary rule, and the frozen target counts completeness only; lines 50–56 rule that no surface, tool, operation or edge class entered governance, characterize C1 as replication of an already-held rule on new author-picked inputs, and conclude coverage was unchanged. Tool status: excerpt returned; no process exit code or event timestamp is exposed by the read tool.
- **Observation — routed defects.** Producer: `functions.grep` on `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/lessons/round-29-verifier-spotcheck.md`, pattern `routed defects|axis misfit|coverage|target|baseline|outside`. Exact returned excerpts, lines 123–124: `A re-score of an already-held rule on new author-built inputs is not a coverage move` and `The C1 target cannot fail on rule quality: openchain_first scored 152/152/0`; defect 2 requires a target that both a rule naming nothing and the trivial baseline fail. Tool status: matching lines returned; no process exit code or event timestamp is exposed by the grep tool.
- **Format references.** `functions.read` returned `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/lessons/round-29.md:44-48` (the `## Mistakes` table and existing entries) and `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/QUALITY.md:43-57` (criteria 43–47 and the row-48 insertion point). These are formatting references, not additional findings.
- Explicit UTC time check: command `timeout 5 date -u '+%Y-%m-%dT%H:%M:%SZ'` returned `2026-10-23T02:42:28Z`. This is the report-session time check, not an asserted timestamp for the earlier read/grep events; those tools expose no event time or numeric exit code.

## Behavior, gates, surfaces, and limits

- Behavior: drafted the requested M30-1 and QUALITY row 48 only. No product or gate behavior was implemented.
- Gates: no counter, REA run, axis-fit gate, control, or pre-data receipt was executed or created by this scribe. No control pass/fail or target outcome beyond the cited round-29 evidence is claimed.
- Touched surface: this report only, at `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-30/w1/ScribeMistakeAxisMisfit.md`. No other lane or fleet files were written. No tools were installed. No scratch artifacts were created.
- Out of scope: building `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-30/axis-fit-gate.py`, editing the lesson or QUALITY source files, running any carriers or mutants, and collecting round-30 data.
