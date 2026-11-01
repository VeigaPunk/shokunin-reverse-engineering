# Round 56 — the carry-in repair round: four round-55 closure items close, and the M55-4 rule becomes an instrument

Lane kaidoku, round 56, fresh-start binding honored (r50/r51/r52 re-read), L1-inline
on the Windows host (2026-11-01). Round base `fe3a804fa8c2d5ff078c6253a5df1bdbc2f28fca`
(the r55 spot-check commit); declaration `1e2f6cf706532ee25e0625b667011a0bfb7c6044`;
carry-in landing `31c2bd506c9c3572124799607edfe4474e8df995`; operative freeze
`19eef5ee93c14972be5756bd1d8bc1f346c3b1dd` (first commit adding
`.ufo/waves/round-56/claims.json`; the first freeze attempt was reset pre-data and
disclosed — M56-2, the M55-3 pattern). No wave (no dispatch surface on this host; the
kaidoku round-53 L0 question stays open and unanswered). Both claims are offline over
committed bytes; the executed instruments are the new frozen round-56 gate, the
V-3-revised corrections-pin, and the R29 gate.

## Gate

| row | URL / path / command and access | located quote (at most 25 words) | decision and limits |
|---|---|---|---|
| S256 | https://git-scm.com/docs/git-cat-file — fetched read-only with curl 2026-11-01 into the round scratch, snapshot bytes and sha256 committed at `.ufo/waves/round-56/l1/s256/` (git-cat-file.html `624464ef7a3d64de06038200bff85ac09389a9d217d379dd660aa6b5165048d7`) | "-e Exit with zero status if <object> exists and is a valid object." (OPTIONS, 12 words) | admit, tier A docs (the tool's own manual, consistent with S255's tiering of git-scm.com docs), mined: grounds the existence-check half of `tools/round-56/receipt-audit.py` — every claimed receipt is answered by `git cat-file -e REV:path` against the object store, never the worktree. The R55 reject-1 boundary is applied consistently: cat-file is anchored because this gate executes cat-file. Used by `plans/round-56-claims.md`, `tools/round-56/receipt-audit.py`, this lesson. |
| R56 reject 1 | anchoring the whole gate in the git-ls-tree manual (not fetched) | reject — the verdict-bearing command is `cat-file -e`; ls-tree supplies only the bare-name candidate list, so the anchor sits on the command whose semantics the verdict needs | reject row |
| R56 reject 2 | running the receipt-audit "green when landed" demo over the r55 container at `627a9c20` and calling it green | reject — the frozen shorthand never resolves in round-55 scope (its home is round-54); the run is recorded as the truthful ABSENT it is, the repair is demonstrated on this round's own container, and the correction of record for T2 is the appended block, never a container edit | reject row |
| R56 reject 3 | resetting the first freeze attempt silently (unpushed, pre-data) | reject — an unpushed reset is still a round event; the M55-3 pattern requires the false start named with its cause in LOG and FREEZE (M56-2) | reject row |
| census receipts | the host-adapted census command at round start and at the filing tip; start receipt `.ufo/waves/round-56/l1/census-start.txt` (exit 0, 19 standing W04) | 19 standing W04 warnings; exit recorded in the receipt | host-adapted form (the `kaidoku-shokunin` mapped directory does not exist here); W04 stays debt |
| do-nothing controls | `.ufo/waves/round-56/l1/scores/c1-before.txt` (all four carry-in items open at the base) and `scores/c2-before.txt` (instrument absent, 0 registry rows, 0 capability rows) | both arms red at the base, committed at the freeze | measured pre-data; a do-nothing control cannot land correction blocks, a revised pinned instrument, a new gate, or rows |

Assimilation: none — `considerthese/` does not exist in this lane (measured at round
start); the shokuknow register is unreachable from this host; the report carries
`Assimilation: none — shokuknow unreachable`.

## Mistakes

| id | class | evidence pointer | captured-by | fix / demonstrated limit |
|---|---|---|---|---|
| M56-1 | instrument-docstring drift (a receipt's parameters transcribed from memory into prose) | the r55 `corrections-pin.py` docstring said the red demo names "line 2's leading cell" and gave placeholder green parameters (`<measured rev>`, `rows_a 1`) while the frozen receipts (`records/pin-red-demo.txt`, `pin-green-demo.txt`) say line 29 and rows 2 appended 0 at `--rev 79421b75…`; no r55 check compared the docstring against the receipt bytes | the r55 non-author closure (routed defect V-3); re-fixed and re-pinned this round | V-3 executed: the docstring now transcribes the frozen receipt verbatim, both demos re-run with unchanged verdicts, new pin `22f77c34…` superseded into the r55 container. The general rule is M55-1's applied to prose: prose ABOUT a receipt transcribes the receipt, checked by diffing the two before landing |
| M56-2 | container-contract drafting (a foreign receipt referenced by bare name) | the first round-56 freeze attempt's T3 referenced `freeze-gate-tip-90f3a9b9.json` bare — the grammar the receipt-audit contract reserves for round-scoped receipt CLAIMS — and the gate's own green pre-flight exited 1 `RECEIPT_ABSENT` (the receipt lives under round-54); caught before any repair data landed, the branch reset with a compare-and-swap `git update-ref` (disclosed in LOG and FREEZE), re-frozen with the full wave path | the round-56 gate itself, pre-data | in container text every cross-round receipt reference is a full wave path (repo-wide existence check); bare names are claims about the container's own round scope. The defect class is real and now mechanically refused — the gate caught a drafting defect in the very round that introduced it |
| M56-3 | worktree-edit tooling (a content-edit script that writes a slice) | the SCORECARD capability-row insertion script first wrote back ONLY the sliced section (the write path received the tail variable, not the full content), truncating the worktree `SCORECARD.md` to 49 lines; caught by the immediate line-count + targeted-grep check run after every scripted edit | this round's L1, by the post-edit integrity check | restored byte-exact from `git show 19eef5ee:SCORECARD.md` (history untouched), re-inserted on the full content; net delta exactly 1 insertion (`git diff --stat`). Rule: a scripted content edit assembles head+tail from ONE variable holding the full bytes, and every scripted edit is followed by a line-count check before commit |
| M56-4 | helper-pathspec (receipts named by the record but never passed to the commit) | the SCORECARD record section's receipts list names `scores/freeze-gate-preflight.json` and `scores/freeze-gate-landing.json`, but neither path was passed to the record commit's helper call — both existed only in the worktree at the close; caught by the pre-filing wave-file audit (`git ls-tree -r --name-only HEAD -- .ufo/waves/round-56/` diffed against the receipts list, the exact audit M55-4 prescribes, run here AFTER the close instead of before the record) | this round's L1, by the M55-4 re-derivation applied to its own round | both receipts land in the follow-up commit with this row, each carrying its `rev` field pinning the commit it measured (preflight `19eef5ee…`, landing `6314b99b…`); rule: the receipts a record section names are cross-checked against `git ls-tree` of the wave dir BEFORE the record commit lands, not at report filing |

## Claim disposition (filled at the record commits)

C1 (calibration, the four r55-closure carry-in items): before 0-of-4 at the base
(`scores/c1-before.txt`), after 4-of-4 content-checked at the carry-in landing
`31c2bd50…` (`scores/c1-after.txt`, committed with the landing). C2 (depth,
capability acquisition — the freeze-receipt completeness gate): before absent
(`scores/c2-before.txt`), after selftest 9/0, red demo exit 1 `RECEIPT_ABSENT` on the
M55-4 event, green demo exit 0 on this round's freeze, registry row in SKILL,
capability row in SCORECARD, and this round's own freeze verified by the gate
(`scores/c2-after.txt`, committed with the record). Verdicts in SCORECARD's round-56
section and LOG.

## Freeze

First commit adding the container `.ufo/waves/round-56/claims.json`:
`19eef5ee93c14972be5756bd1d8bc1f346c3b1dd`. No amendments to the operative freeze;
the reset first attempt is disclosed above (M56-2). The frozen instruments and pins:
`tools/round-56/receipt-audit.py` `897df532…d72512`,
`tools/round-55/corrections-pin.py` `22f77c34…9ece81` (the V-3-revised bytes,
superseded into the r55 container at `31c2bd50…`), `tools/round-29/freeze-gate.py`
`25b54339…93eb2` — bytes unchanged from the claims commit `1e2f6cf7…`.
