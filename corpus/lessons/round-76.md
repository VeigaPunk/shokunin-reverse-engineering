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

**Census.** `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` at round start: exit 0,
191 rows, 24 W04 warnings (`.ufo/waves/round-76/l1/census-start.txt`). At round end: exit 0, 194 rows
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

(pending the r76-w1 wave; appended when the wave settles)
