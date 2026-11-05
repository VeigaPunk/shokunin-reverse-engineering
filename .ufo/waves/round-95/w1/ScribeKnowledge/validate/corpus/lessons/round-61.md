# Round 61 — the routed edge mislabel closes append-only, and the edge-numstat class becomes an instrument

Lane kaidoku, round 61, fresh-start binding honored (r50/r51/r52 re-read and
spot-checked), L1-inline on the Windows host (2026-11-01). Round base
`2d976fba2bfc3b85dcc0546f9ec8e149fa2185fe` (the r60 verifier spot-check
commit); carry-in `319e5244f088fc01cca7b0b8259f0ce5085e7b48` (the r60
outside decision recorded per QUALITY #34 before any claim was measured;
the closure's status-neutral note 1 accepted as the round's routed
correction target D60-1, with the two sibling sites named in the same
entry); declaration `9eb5f0e4cb134a320abbd2e9679c69d4dea8c6b6` (the plans +
the new instrument, the QUALITY #33 order); operative freeze
`5286dccf86bdb598af23fd3a034592af5a5c97b6` (the first commit adding
`.ufo/waves/round-61/claims.json`); landing
`e97e621e21bd285bbff2cc95c184c16f10efb04a` (the correction append + the
correction receipt + the SKILL row + the capability row; the
subject-alternation pipes in the registry-row draft self-caught by the
recount before any commit — M61-2). No wave (no dispatch surface on this
host; the kaidoku round-53 L0 question stays open and unanswered). Eight
frozen instruments (seven unchanged, one new:
`tools/round-61/numstat-edge-audit.py`, pin `6b967e20…`).

## Gate

| row | URL / path / command and access | located quote (at most 25 words) | decision and limits |
|---|---|---|---|
| S261 | https://git-scm.com/docs/git-diff — fetched read-only with curl 2026-11-01 into the round scratch, snapshot bytes and sha256 committed at `.ufo/waves/round-61/l1/s261/` (git-diff.html `5ae80d1deee5dc2c1acafff5491c5ba019629b9a785e6781a3e8a411cf9e22ed`, 229155 bytes) | "Similar to --stat, but shows number of added and deleted lines in decimal notation and pathname without abbreviation, to make it more machine friendly." (24 words; locator: the `OPTIONS` heading, the nearest preceding h1–h6 before the `--numstat` option definition, verified programmatically against the snapshot; labelled **composite** per QUALITY #42 — the token `--stat` sits inside an inline code span between plain-text words; contiguous in the tag-stripped, whitespace-collapsed snapshot text) | admit, tier A docs (tool documentation — the category is the official git reference, the authority for the numstat semantics the edge gate re-derives with); mined: an edge-labeled `A B` numstat claim is a function of the (X, Y, path) triple alone — mechanical re-derivation — and the docs' binary sentence (binary files output two `-` instead of saying `0 0`) is why a binary edge is NUMSTAT_BINARY fail-closed in the gate, never compared as `0 0`. Used by `plans/round-61-claims.md`, `tools/round-61/numstat-edge-audit.py`, this lesson. |
| R61 reject 1 | correcting the two sibling sites (the LOG r60-close entry, the SCORECARD T7 atom) by editing those filed bytes in place | reject — LOG is append-only (a correction is a NEW entry that names what it corrects, the S254 log model) and SCORECARD's landed sections stay as filed (the "Record corrections" pattern); the siblings are corrected in the new round-61 LOG entry and the round-61 SCORECARD section, each naming the site by path/line with the corrected reading | reject row |
| R61 reject 2 | planting the `freeze-gate-tip-90f3a9b9.json` bytes under round-58 or round-60 scope so the duty sweep stops firing on the two quoted bare-name findings | reject — the same finding r58 reject 1, r59 reject 1 and r60 reject 2 refused to shape away; the r59 non-author closure ruled the flip condition does NOT fire (the T4/T5 sentences are quotations naming their true scope); this round's eight-container sweep names the r60 container for the first time and the finding is hand re-verified (the bytes exist under round-54 and round-55, byte-identical `b508a78a…`) and dispositioned BEFORE the landing — the fourth refusal to plant | reject row |
| R61 reject 3 | giving the new edge gate a whole-revision mode that scans LOG.md and SCORECARD.md without caller-supplied name bindings (to "catch" the siblings automatically) | reject — the sections print abbreviated hashes with ellipsis, so the names cannot resolve from the bytes alone; an auto-mode would either fire unresolvable-name noise or manufacture bindings; the receipts-and-argv model (one receipt per run, `--name` overrides disclosed as caller context) keeps every finding hand-explainable — the siblings are demonstrated red WITH disclosed overrides instead | reject row |
| census receipts | the host-adapted census command at round start and at the filing tip; start receipt `.ufo/waves/round-61/l1/census-start.txt` (exit 0, 19 standing W04, 167 rows) | 19 standing W04 warnings; exit recorded in the receipt | host-adapted form (the `kaidoku-shokunin` mapped directory does not exist here); W04 stays debt |
| do-nothing control | `.ufo/waves/round-61/l1/scores/c1-before.txt` (correction absent rc=128; mislabel as filed 1/1/1; no correction block grep 0; the true edges re-derived) and `scores/c2-before.txt` (instrument absent rc=128, 0 registry rows, 0 capability rows, 0 edge receipts) | both arms are red at the base, committed at the operative freeze | measured pre-data; a do-nothing control cannot produce the correction, the gate, the demos, or the registrations |

Assimilation: none — `considerthese/` does not exist in this lane (measured
at round start); the shokuknow register is unreachable from this host; the
report carries `Assimilation: none — shokuknow unreachable`.

## Mistakes

| id | class | evidence pointer | captured-by | fix / demonstrated limit |
|---|---|---|---|---|
| M61-1 | an edge written where the probe's edge belongs — the routed D60-1 class, in this round's own before-arm draft, caught BEFORE any commit | `scores/c1-before.txt` closing probe: first drafted against the r60 ROUND base 48c41830 with prose claiming an empty edge; the probe actually prints `37 0` there (the c1-after file's own creation during round 60); the corrected probe runs against the r60 close tip `1c1d6880` where the edge IS empty, and the draft note is preserved in the receipt | this round's L1, re-deriving every pasted output against the rev its prose names before anything was committed (the M60-3 rule applied to the freeze draft) | the receipt lands with the corrected edge and the draft note; the lesson records that the D60-1 class fires on BEFORE-arms too, not only on registration notes — a baseline must name the rev its "unchanged" claim is measured against, and "unchanged since X" means diff X→tip, not diff round-start→tip |
| M61-2 | the instrument's own grammar literal smuggled structural characters into a structural record — the SKILL registry row's first draft carried the gate's subject alternation `(SKILL|LOG|SCORECARD|PROVINCE)`, whose three literal pipes made the row read 10 cells | the seven-cell recount read 11 pipes on the new row (8 structural + 3 in the alternation); the pipe-position dump located all three inside the grammar literal | this round's L1, BEFORE any commit (the M60-1 recount rule applied) | the alternation is spelled out in words ("the four subject words SKILL, LOG, SCORECARD and PROVINCE"); post-repair: r61 row 7 cells, the r60 neighbor row 7 cells. Rule: a structural row's cells carry no metacharacters from the content they describe — when a row must name a grammar containing the record's own delimiter, the delimiter is elided in words, and the recount covers both the new row and its neighbor before landing |
| M61-3 | a `$ git diff` probe pasted into a receipt shows `0 37` against the stale index on this host (`git diff HEAD -- <path>` goes through the unreliable index and reports the file deleted), which would have been misread as a rewrite of filed bytes | the landing verification: `git diff --numstat HEAD -- .ufo/waves/round-60/l1/scores/c1-after.txt` printed `0 37` while the worktree file was byte-verified as the HEAD blob's 37 lines plus a 14-line append (prefix sha256 `873c447f…` re-hashed both sides); the honest measurement is the POST-COMMIT numstat between two revs — freeze→landing printed exactly `14 0` | this round's L1, on the immediate re-read (the contract's warning that the index is unreliable, confirmed live) | the landed-bytes discipline on this host: verify worktree-vs-blob identity by hash (head-bytes vs `git show REV:path` piped to sha256sum), never by `git diff` against HEAD; verify landed deltas by `git diff --numstat <rev> <rev>` between commits only |

## Claim disposition (filled at the record commit)

C1 (calibration): before all open at the base (`scores/c1-before.txt`),
after the correction block is appended (additions-only, `14 0`), the
correction receipt exists with three true edge claims, the siblings are
corrected in the new LOG entry and the SCORECARD section, and the gate's
green arm over the correction receipt exits 0 (3 claims, all re-derive;
`records/edge-green-correction.txt`) while the defect's own receipt keeps
firing at line 10 only (`records/edge-persistent-c1after.txt` — a
correction does not clear filed bytes, the r58 pattern). C2 (depth,
capability acquisition): before all open at the base (`scores/c2-before.txt`),
after the gate is registered (SKILL row 7 cells pipe-free, capability row,
container pin `6b967e20…`), the demos stand: selftest 25/0; red on the
routed defect (MISMATCH@10, internal bindings), red on both siblings
(MISMATCH@4606, MISMATCH@3857) with the r59 true claims green on the same
runs; fail-closed 2× NAME_UNRESOLVED; zero-claims exit 2. The duty ran to
dispositions: the eight-container sweep (six clean + TWO same-class
bare-name findings — the r60 container named for the first time, hand
re-verified and dispositioned before the landing, no copy planted, the
fourth refusal), the record-audit (r60 named 21 missing 0 clean), and the
orphan census (3 worktree-only dispositioned + 15 wave-in-progress + the
50-path aux/ class). census3 `--generate` 66 paths at the landing rev,
`--check` at the record rev exit 0. Verdicts in SCORECARD's round-61 section
and LOG.

## Freeze

Operative freeze: `5286dccf86bdb598af23fd3a034592af5a5c97b6` — the first
commit adding `.ufo/waves/round-61/claims.json`. No amendments to the
operative freeze. The frozen instruments and pins:
`tools/round-61/numstat-edge-audit.py` `6b967e20…` (new, committed at the
declaration `9eb5f0e4…` before the claims file),
`tools/round-60/annotation-sweep.py` `38614088…`,
`tools/round-59/annotation-audit.py` `ba9ccbb9…` (the frozen gate the sweep
composes, `--expect-sha256` checked before every sweep run),
`tools/round-51/census3.py` `a7538e5f…`, `tools/round-56/receipt-audit.py`
`897df532…`, `tools/round-57/record-receipt-audit.py` `3a5fff9a…`,
`tools/round-55/v6-block-digest.py` `22785c1e…`,
`tools/round-29/freeze-gate.py` `25b54339…` — bytes unchanged from the
claims commit through the tip.
