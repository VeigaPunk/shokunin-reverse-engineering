# Round 59 — the routed D58-1 annotation contradiction closes append-only, and the annotation-consistency gate becomes an instrument

Lane kaidoku, round 59, fresh-start binding honored (r50/r51/r52 re-read and
spot-checked), L1-inline on the Windows host (2026-11-01). Round base
`df62b6f986fb460847037482e0199cdf1541e393` (the r58 verifier spot-check
commit); declaration `0a131b97a37880ac29c33252c4bfdbc778aa8bfd` (the plans +
the new instrument, the QUALITY #33 order: the instrument is committed before
the claims file); operative freeze
`b6dadbd255907557c0c3ed8ff441d192cc06310e` (the first commit adding
`.ufo/waves/round-59/claims.json`); landing `2ff5d30800df0184c0a63c778bb166c1650aa3a3`;
landing fixup `203c07a7b68d683e8536b8f103c9f2c35d787168` (one stray blank
line removed from the SKILL insertion, disclosed); receipt-prose fixup
`945373723aa842a4d8ae27947708e5ce4205065a` (disclosed, self-caught by the
round's own instrument — M59-3). No wave (no dispatch surface on this host;
the kaidoku round-53 L0 question stays open and unanswered). Both claims are
offline over committed bytes; five frozen instruments unchanged, one new
instrument (`tools/round-59/annotation-audit.py`, pin `ba9ccbb9…`).

## Gate

| row | URL / path / command and access | located quote (at most 25 words) | decision and limits |
|---|---|---|---|
| S259 | https://www.gnu.org/software/grep/manual/grep.html — fetched read-only with curl 2026-11-01 into the round scratch, snapshot bytes and sha256 committed at `.ufo/waves/round-59/l1/s259/` (grep.html `517177d02c39c446470c898273036a7616f705e4cbdcb6486b76a25700675f37`, 248692 bytes) | "Suppress normal output; instead print a count of matching lines for each input file." (the `-c`/`--count` option, section 2.1.3 General Output Control, 14 words; served with a line break after "output;", contiguous in the snapshot bytes) | admit, tier A docs (tool documentation — the category is the grep manual, the authority for what the lane's counting probes print and return); mined: `grep -c` counts matching LINES (BRE) and exits 1 when none are selected, so a pasted count is a function of the pattern AND the bytes probed — a pattern/wording mismatch (D58-1's exact class) is detectable by re-deriving the count from the same bytes, which is what `tools/round-59/annotation-audit.py` does (the system grep re-runs as an argv subprocess on stdin bytes; no shell, no worktree). Used by `plans/round-59-claims.md`, `tools/round-59/annotation-audit.py`, this lesson. |
| R59 reject 1 | planting a third byte-identical copy of `freeze-gate-tip-90f3a9b9.json` under `.ufo/waves/round-58/` so the round-56 bare-name grammar stops firing on the r58 container's quoted finding name | reject — T4's sentence quotes the r58 sweep's finding ("…in round-55 scope…"), it does not commit the file under round-58; planting bytes solely to flip the grammar is the r53 "disclosed verbatim rather than shaped away" class; disclosed named debt with the flip condition recorded (`records/w58-sweep-finding-disposition.txt`, recorded BEFORE the landing) | reject row |
| R59 reject 2 | editing `tools/round-59/annotation-audit.py` to skip parenthesis-led lines that merely QUOTE the `base: N -> record: M` shape (which would have turned the persistent-finding receipt green) | reject — the instrument is frozen at its declaration pin `ba9ccbb9…`; the flagged prose lines ARE lines its grammar reads as annotations, and fail-closed is the contract; the limit is documented and receipted (`records/annotation-selfcatch.txt`, `records/annotation-persistent-finding.txt`, M59-3) instead | reject row |
| R59 reject 3 | amending the frozen round-53 container to add receipt claims (the r58 planned "receipts_checked-0 vacuous-clean" follow-up) | reject — a historical container is frozen; amending it is the amendment class every freeze forbids, and its FLAGGED INSTRUMENT_NONE finding is disclosed verbatim rather than shaped away (the r53 ruling); the container already audits clean on its full-path receipts at this round's base (`records/receipt-audit-sweep.txt`) | reject row |
| census receipts | the host-adapted census command at round start and at the filing tip; start receipt `.ufo/waves/round-59/l1/census-start.txt` (exit 0, 19 standing W04, 165 rows) | 19 standing W04 warnings; exit recorded in the receipt | host-adapted form (the `kaidoku-shokunin` mapped directory does not exist here); W04 stays debt |
| do-nothing controls | `.ufo/waves/round-59/l1/scores/c1-before.txt` (D58-1 open at the base: no correction block, the defective annotation as filed, the cited probe returning 0 where its annotation claims 1; the duty's finding open) and `scores/c2-before.txt` (instrument absent rc=128, 0 registry rows, 0 capability rows, selftest 23/0, the red demo exit 1 on the D58-1 defect itself) | both arms red at the base, committed at the operative freeze | measured pre-data; a do-nothing control cannot append the correction, replace the marker probe with patterns that match, run the duty to a disposition, or land a registered demonstrated instrument |

Assimilation: none — `considerthese/` does not exist in this lane (measured
at round start); the shokuknow register is unreachable from this host; the
report carries `Assimilation: none — shokuknow unreachable`.

## Mistakes

| id | class | evidence pointer | captured-by | fix / demonstrated limit |
|---|---|---|---|---|
| M59-1 | writer grammar ≠ reader grammar, AGAIN (a NEW registry row drafted with raw pipe characters inside backticked grammar text — nine cells to the seven-cell census3 parser, the exact M58-2 class r58 repaired via S258) | the r59 SKILL row's first draft carried "`git show REV:path | grep -c PAT`" inside its description cell; the seven-cell recount (`awk -F'|'` on the drafted row) printed 9, not 7 | this round's L1, BEFORE any commit (the recount is now part of writing a registry row) | the grammars reworded pipe-free ("the show-piped form (`git show REV:path` piped to `grep -c PAT`)"); the landed row parses at 7 cells and census3 `--generate` derives 64 paths at the fixup rev. Rule: a registry row is drafted pipe-free and recount-checked BEFORE landing — S258's lesson governs writers, not only repairs |
| M59-2 | insertion residue (the SKILL row insertion carried one stray blank line, so the landing's SKILL delta read 2/0 against the frozen atom "exactly the one added registry row") | `git diff --numstat b6dadbd2 2ff5d308 -- SKILL.md` → `2 0` at the landing; the fixup `203c07a7` removes the blank (delta `1 0` freeze→fixup) | this round's L1, by the immediate numstat re-derivation of the landing commit (the M55-4 rule applied to the SKILL edit) | the landing commit stays as filed; the disclosed landing-fixup commit lands the one-line removal; the record section cites the freeze→fixup delta. Rule: a single-row insertion is verified by numstat against its intended shape immediately, and residue is removed in a disclosed fixup, never by rewriting the landed commit |
| M59-3 | quotation mimics the checked grammar (receipt prose that opens a line with `(` and quotes the `base: N -> record: M` shape is indistinguishable from an annotation to the extractor) | the instrument flagged THIS round's own prose twice: the correction receipt's closing line (bound to the preceding wc-form probe: ANNOTATION_OUTPUT_MISMATCH@27 + COMMAND_UNREEXECUTABLE@22, `records/annotation-selfcatch.txt`) and the appended r58 correction's disclosure line (bound to the r58 numstat probe: OUTPUT_MISSING@25 + COMMAND_UNREEXECUTABLE@21, `records/annotation-persistent-finding.txt`) | the round's own instrument, during the green and persistent demonstrations — the gate caught its author | the correction receipt's prose reworded in the disclosed receipt-prose fixup `94537372` (the green demo then exits 0); the appended r58 disclosure line stays as filed (append-only) and its two findings are disclosed in the persistent receipt. Rule: a receipt quotes the annotation shape only inside lines that do not open with `(`; an auditor reading such a receipt treats the quote-shaped prose as a finding to explain, never as a pass |

## Claim disposition (filled at the record commit)

C1 (calibration, D58-1 + the duty): before all open at the base
(`scores/c1-before.txt`), after the correction block lands appended to the
r58 receipt (filed bytes stay as filed; `git diff --numstat` shows 0
deletions at the close), the marker probe is replaced by patterns that match
their targets — the note's wording 0 → 2 at the record rev, the
note-of-record bullet 0 → 1 — and the duty runs to dispositions: the sweep
names the r58 container's quoted bare name (disclosed named debt, no copy
planted, flip condition recorded BEFORE the landing), the record-audit is
green (named 18, missing 0), and the orphan census dispositions 4
worktree-only paths and the 50-path aux/ host boundary. C2 (depth,
capability acquisition): the instrument lands registered (SKILL row, 7
cells, pipe-free; capability row; container pin `ba9ccbb9…`), selftest 23/0,
red on the D58-1 defect itself (exit 1, two findings on line 6), green on
the correction receipt at `94537372` (exit 0, 4 annotations), the persistent
finding disclosed (exit 1, four findings, all accounted), census3
`--generate` 64 paths / `--check` at the record rev exit 0. Verdicts in
SCORECARD's round-59 section and LOG.

## Freeze

Operative freeze: `b6dadbd255907557c0c3ed8ff441d192cc06310e` — the first
commit adding `.ufo/waves/round-59/claims.json`. No amendments to the
operative freeze; the two post-landing fixups (`203c07a7`, `94537372`) are
disclosed one-line commits that remove insertion residue and receipt-prose
mimicry, never amendments to claims, container, or instruments. The frozen
instruments and pins: `tools/round-59/annotation-audit.py` `ba9ccbb9…` (new,
committed at the declaration `0a131b97` before the claims file),
`tools/round-51/census3.py` `a7538e5f…` (unchanged since r51),
`tools/round-56/receipt-audit.py` `897df532…` (unchanged since r56),
`tools/round-57/record-receipt-audit.py` `3a5fff9a…` (unchanged since r57),
`tools/round-55/v6-block-digest.py` `22785c1e…` (unchanged since r55),
`tools/round-29/freeze-gate.py` `25b54339…` (unchanged since r29) — bytes
unchanged from the claims commit through the tip.
