# Round 76 — the capability rows become a checked claim, and a printed command becomes executable

Base: `5303a662d43aac52b0667f2776cce49dfc004fcf`.
Declaration: `be99e4f9b72fb2dbae75329c0d5c55002854cbed`.
Pre-freeze instrument revision: `58316c9218e0345bcdc1ff43357c8ca815481f86`.
Freeze: `5824d5d8e135194a59db3df1533b76ff479753bf`.
Contract: `plans/round-76-claims.md` and `.ufo/waves/round-76/claims.json`.
Axes: calibration (R76-C1, the capability rows as a checked claim) and operability (R76-C2, the printed
counting command as a runnable artifact).

## Gate

Every page below was opened this round with one GET each; snapshots, byte counts and sha256s are in
`.ufo/waves/round-76/l1/sources/`. Quotes are literal excerpts with their snapshot line.

| source / decision | URL | accessed | located quote (≤25 words) | digestion |
|---|---|---|---|---|
| S286, `shlex.split`, admit (mined) | https://docs.python.org/3/library/shlex.html#shlex.split | 2026-11-04 (HTTP 200, 66 497 B, sha256 `4c1f8bf6…`) | "Split the string s using shell-like syntax." (7 words; `shlex.split` entry, snapshot line 229; **composite** — the word `s` sits inside a `<var>` tag, labelled at write) | The documented tokenizer is shell-*like*, not a shell grammar: the gate tokenises a printed argv with it and performs no expansion, substitution or execution. The row does not claim shell-semantics compatibility. |
| S287, `argparse`, admit (mined) | https://docs.python.org/3/library/argparse.html | 2026-11-04 (HTTP 200, 334 994 B, sha256 `14d33eea…`) | "terminates the program with a status code of 2." (9 words; `ArgumentParser.error`, snapshot line 2418) | Grounds the before-arm: the round-75 printed command's missing `--work` is a parser error, so rc 2 is the documented outcome rather than an instrument quirk. |
| S288, `bash(1)`, reject | https://man7.org/linux/man-pages/man1/bash.1.html (the plan named `sh(1)`, which returned HTTP 404, 196 B, on this host; the substitution is recorded in the search log) | 2026-11-04 (HTTP 200, 497 852 B, sha256 `e35fa296…`) | "word splitting and pathname expansion.  The shell" (7 words; EXPANSION, snapshot line 477) | REJECTED: the claim needs the shell the gate refuses to invoke, so the page cannot support the row's scope. Flip: the gate gains a shell path, or a claim is made about shell word-splitting semantics. Consumer search (QUALITY row 36): `grep -c 'shell=True' tools/round-76/plan-command.py` → 0. |

**Same-round source corrections (old → new, in place).** The round-76 scout seat (`ScoutSource.md` §1-§3) found
three defects in the rows this round wrote, all in wording/attribution rather than provenance (the digests and the
located quotes reproduce against an independent GET). They were corrected in place before the round's record,
because the alternative — three `supersedes` rows — would duplicate the same URLs and leave the wrong cells as the
registry's first reading; the deviation from `CORPUS.md` rule 2's append-only clause is recorded here and in the
report, and each change is logged old → new:

- **S286 `scope`** old "…performs no expansion, substitution or execution" → new "A shell-LIKE tokeniser, not a
  shell grammar: POSIX mode and comment suppression are the documented defaults, and the page's own Warning
  recommends passing an argument list to `subprocess.run()` with `shell=False`". The old cell asserted three
  negatives the page never states (`substitut` 0 hits, `glob` 0 hits on the snapshot).
- **S286 `teaches`** old "…so no shell metacharacter is ever interpreted" → new "…the gate's metacharacter refusal
  is its own `static_defects`, never a claim of this page". The old cell credited the page with the instrument's
  property; the page never uses "metacharacter".
- **S286 `anchor`** old "`<var>` tag" → new "`<em>` tag"; the served byte at line 229 is `<em>s</em>`.
- **S287 `scope`** old "…— the exit the round-75 printed command produced" → new "`ArgumentParser.error()` prints
  usage and terminates with status 2 by default (overridable, and `exit()` defaults to 0): the status-2 contract a
  usage error takes". **S287 `teaches`** old "…so rc 2 is the documented outcome, not an instrument quirk" → new
  "…it does NOT ground the round-75 probe's rc 2, which is the probe's own `return 2` at its preflight". The
  observed rc 2 is the instrument's preflight, not argparse's exit; **S287 `anchor`** gains the doc version
  (Python 3.15.2) and the quote becomes the full sentence across lines 2417-2418 (21 words, composite-labelled).
- **S288 `anchor`** old "EXPANSION, snapshot line 477; located quote: \"word splitting and pathname expansion.  The
  shell\"" → new "EXPANSION lines 1931-1936; located quote at line 1932: \"Expansion is performed on the command
  line after it has been split into words.\"" The old quote was a fragment of a sentence whose subject and
  negation it dropped ("The words between the [[ and ]] do **not** undergo …"), so it asserted the opposite.

The `corpus/knowledge/2026-11-04-r76-plan-command-executability.md` section "Why rc 2 is the right before-arm"
was rewritten to "What the observed rc 2 is, and is not" for the same reason.

**Census.** `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` at round start: exit 0,
191 rows, 23 W04 warnings (`.ufo/waves/round-76/l1/census-start.txt`). At round end: exit 0, 194 rows
(`l1/census-end.txt`). Three rows enter (S286 mined, S287 mined, S288 rejected); no existing row's
`status`/`recheck`/`used-by` changes.

**Spot-check (non-author).** The round-75 closure's outside document is the round's population, and the round-76
non-author spot-check re-opens the sample this lesson records; its verdicts are in
`corpus/lessons/round-76-verifier-spotcheck.md` (filed by the closure session, not by this lane).

## Mistakes

| class | evidence | captured-by | fix |
|---|---|---|---|
| **landing** — a self-assessment sentence written before its artifact existed, and a printed command never executed by its author. Two faces of one class: the round-75 record claimed two capability rows the card did not hold, and printed a counting command that exits 2 as printed (missing `--work`, abbreviated digest); neither was caught because no atom read the table and no instrument executed the printed text. | `corpus/lessons/round-75-verifier-spotcheck.md` §6 items 1 and 4; `.ufo/waves/round-76/pre/c1-control-r75audit-at-base.json` (the round-75 audit green at base with both rows absent); `.ufo/waves/round-76/pre/r75-printed-exec.txt` (exit 2, `missing required arguments: work`) | `D24_capability_rows` and `tools/round-76/plan-command.py` — each shown able to fail before data: six capability red fixtures (`pre/audit-selftest.json`, 17 cases) and three gate controls (`pre/controls-at-declaration.json`) | the record's repertoire claim is now a parsed atom over the table it names, and a plan's counting command is executed as printed by the gate that scores it |

A second, smaller mistake was caught **inside this round, before the freeze**: the first `missing-required-arg`
control removed `--root`, which the audit defaults, so the control could not fail (its selftest case was red). The
fix removed the required `--rev` instead and the plan's control sentence was restated to name the same argument;
the pre-freeze revision `58316c92` carries both. Class: **survivor** — a control that cannot fail is a survivor
with a green face; captured by the gate's own selftest.

## Routed-defect disposition (round-75 spot-check §6)

| # | routed defect | disposition |
|---|---|---|
| 1 | the two capability rows are not in the `## Capabilities` table | closed: both rows enter the table with resolving pointers (R76-C1), and `D24_capability_rows` re-derives them |
| 2 | the round-75 atom set dropped the round-74 D8 capability-rows atom | closed: D24 is that atom, with six red fixtures and the paragraph-level parse the round-75 claim line needs |
| 3 | two round-75 commits are missing from the Landed-changes table | closed in the round-76 report: `668e545e` (frozen-battery reproduction) and `fcf17efe` (record gate's disclosures check) are named there; the filed round-75 report stays byte-identical |
| 4 | the printed R75-C1 counter command is not executable as written | closed: `tools/round-76/plan-command.py` refuses it statically as a fixture arm and reproduces its rc 2 with the digest bound; the report prints the full executable argv |
| 5 | receipt-revision prose is loose | closed in the round-76 report: each receipt is named with the revision it records (`c1-at-landing` at the landing, `gate-at-record`/`coverage-selfcheck-at-record` at their own revisions) |
| 6 | `LOG.md` says the eight atoms re-derive routed defects 1-8 | closed: an appended correction in the round-76 LOG entry names the clause and restates it as 1-7 |
| 7 | the freeze ledger row names one disclosed instrument revision | closed: a companion row in `corpus/claim-freezes-corrections.tsv` restates it as four; the round-75 row stays byte-identical (append-only ledger, QUALITY row 100) |
| 8 | the C2 receipts do not record the exit code the predicate names | closed: both round-76 receipts carry their own `exit`; the round-75 receipts stay as filed and the report states that their exit clause is evidenced only by the wrapper log |

## What the wave found

One v1 wave `r76-w1`, 14 seats, dispatched at `06:44:50` and settled with `WAVE-DONE`; seat records in
`.ufo/waves/round-76/r76-w1-results.json`.

- **MutationTester — five survivors on the first cut, all closed.** Nine one-point mutants of the two
  instruments' own checks: `d24-a` (absent-row check made a no-op) survived because `cap-absent-row-red`'s
  fixture used an *empty* table, so the "no data rows" guard fired identically on pristine and mutant
  (guard-masked); `d24-e` (line-level claim parsing) survived because every fixture was a single line;
  `gate-h` (`$OUT` containment dropped), `gate-i` (argv allowlist dropped) and `gate-f`'s angle-placeholder
  half survived because no control exercised them. The closure (`98407fad`) populates the absent-row
  fixture, adds `cap-wrapped-claim-accepts`, and adds four gate controls (`angle-placeholder`, `escape-out`,
  `script-outside`, `shell-meta`); `tools/round-76/mutation-check.py` now scores nine mutants with **0
  survivors and eight sole detectors** (`l1/scores/mutation-check-at-tip.json`). Sub-finding kept: `gate-g`
  (`shell=True`) is killed only indirectly, by the rc-2 expectation, not by a shell-refusal case.
- **ExecCapGrammar — the grammar rejects every cosmetic construction.** Seven cosmetic SCORECARDs (absent
  named row over a populated table, `—` evidence, a one-slash token, an unresolved path, a round mismatch,
  a three-word stub, an empty table, no claim line) each return their named defect, and three accept probes
  (well-formed row, the real wrapped two-name claim, the landed card) return none
  (`.ufo/waves/round-76/w1/ExecCapGrammar.md`).
- **ExecPlanArms — C2's three arms reproduced without the gate.** The printed command's argv carries the
  ellipsis; executing it directly (no shell) exits 2 with `missing required arguments: work`; the digest-bound
  variant also exits 2; the plan's C1 block executes verbatim and returns a readable counter. It also records
  that the working-tree instruments differ from the freeze pins — the disclosed `a8908930` revision
  (`.ufo/waves/round-76/w1/ExecPlanArms.md`).
- **ScoutSource — three blocking source defects, repaired before the record.** See the Gate above.
- **ScribeRows — the rows re-derived and the W04 count corrected.** The seat re-fetched all three pages
  (digests equal to the committed snapshots), drafted the rows in the 11-cell grammar, and caught that the
  round's census receipts carry **23** W04 lines, not the 24 the L1's brief said; the round-76 statements in
  `LOG.md`, `SCORECARD.md` and this lesson were corrected to the receipt's count, and the round-72/73
  historical statements were left byte-identical (`.ufo/waves/round-76/w1/ScribeRows.md`).
- **RevengerProbe (dispatched as the labrat item) — the two named reasons are the whole set.** Four runs:
  printed (rc 2), digest bound without `--work` (rc 2), both fixed (rc 0, `survivor_count 0`, 619 ms), and
  `--work` added with the ellipsis kept (rc 2, pin refused before execution). No third defect
  (`.ufo/waves/round-76/w1/RevengerProbe.md`).
- **ConnectorCross — no overlap absorbed.** The fleet holds one instrument-class plan-command file (this
  lane's); `tsukuroi-shokunin/tools/check-self-assessment.py` checks a frozen capability-name list but treats a
  miss as `CannotEvaluate` (exit 2), never a red verdict; `chousa`'s claims audits have no
  `## Capabilities` rule class. Duplication with named divergences, nothing absorbed
  (`.ufo/waves/round-76/w1/ConnectorCross.md`).
- **Dead and incomplete seats (recorded, not counted as verification).** Four seats returned an empty output
  with no terminal error line in the results file — `ExecBaseArms`, `ExecAuditAtoms`, `ReviewerC2`,
  `SentinelScope` — cause unknown (the results record carries `note: null` and zero bytes); two returned
  mid-work prose with no artifact — `ReviewerC1` (222 bytes: it had listed its six axes and stopped) and
  `CriticClaims` (139 bytes: it had loaded the instruments and stopped). Their assignments remain unverified
  by the wave: no seat independently re-derived C1 end to end, and the security review of the plan-command
  executor did not land. What did land: the mutation battery, the grammar attack, the independent arm
  reproduction, the source scout, the probe and the connector scan.
