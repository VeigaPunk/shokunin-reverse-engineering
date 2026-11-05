# Round 58 — the r57-closure routed carry-in closes with receipts, and the registry-drift census runs again

Lane kaidoku, round 58, fresh-start binding honored (r50/r51/r52 re-read and
spot-checked), L1-inline on the Windows host (2026-11-01). Round base
`42c794afc5cdf2f72d80edb839cfbcbfe32e6bad` (the r57 verifier spot-check commit);
helper attempts `634d12d6…` / `9e8ee220…` landed no payload and are disclosed
(M58-1); operative freeze `37e49cf33537ff182265c42f3fa546b1c0c0c0fa` (the first
commit adding `.ufo/waves/round-58/claims.json`, which also carries the
declaration bytes, both LOG entries, and the removal of the attempts' bogus
`C:` directory); landing `05865b6d63b43b6f732e9013c86980d79ddcb52c`. No wave
(no dispatch surface on this host; the kaidoku round-53 L0 question stays open
and unanswered). Both claims are offline over committed bytes; every executed
instrument is a frozen tool pinned in the container — no new instrument this
round.

## Gate

| row | URL / path / command and access | located quote (at most 25 words) | decision and limits |
|---|---|---|---|
| S258 | https://github.github.com/gfm/ — fetched read-only with curl 2026-11-01 into the round scratch, snapshot bytes and sha256 committed at `.ufo/waves/round-58/l1/s258/` (gfm.html `b153d814fdfc8624bb6da7449162c1cd707a637f7d1c1b636eb44b9cf63fa220`, 508310 bytes) | "Include a pipe in a cell’s content by escaping it, including inside other inline spans:" (Tables extension, 15 words) | admit, tier A spec (the markdown dialect's own specification, the authority for what a table cell may contain), mined: grounds M58-2's grammar conflict — the r55 v6-block-digest registry row's purpose cell used the spec-legal escaped-pipe form, while the frozen census3 parser splits rows on the plain pipe character with no GFM unescaping, so the row read as eight cells and the registry failed closed in its own drift census from r55 until the r58 data-side reword. The repair side follows the spec boundary: the PARSER is frozen (the r51 authority note; census3's own docstring says the tool does not modify or repair frozen meanings), the DATA is repaired into the reader's grammar. Used by `plans/round-58-claims.md`, the reworded SKILL registry row, this lesson. |
| R58 reject 1 | landing the orphaned first-chain receipt `freeze-gate-tip-25b5b256.json` together with the sweep's finding | reject — nothing committed names it (grep rc=1 receipted); landing it would put an in-tree receipt no record claims, the M56-2 pre-claiming class; retained on disk and disclosed in `records/orphan-census.txt` instead | reject row |
| R58 reject 2 | declaring the r55 container's bare-name claim satisfied because the receipt exists REPO-WIDE (under round-54) | reject — the receipt-audit contract is explicit: bare names are claims about the container's OWN round scope (M56-2's rule); the only honest repair makes the scoped claim true, which takes the byte-identical landing at the named path, done this round | reject row |
| R58 reject 3 | repairing M58-2 by teaching the frozen census3 parser GFM unescaping | reject — the parser is frozen and pinned since r51; the defect is data written in a grammar the reader never spoke; the row is reworded data-side and the parser's bytes and pin are untouched (selftest 20/0 at the same sha256) | reject row |
| census receipts | the host-adapted census command at round start and at the filing tip; start receipt `.ufo/waves/round-58/l1/census-start.txt` (exit 0, 19 standing W04, 164 rows) | 19 standing W04 warnings; exit recorded in the receipt | host-adapted form (the `kaidoku-shokunin` mapped directory does not exist here); W04 stays debt; the routed "census-safe W04 supersedes set" closes vacuous-as-named (`records/w04-supersedes-probe.txt`: the supersedes guard exists in the E04 branch only) |
| do-nothing controls | `.ufo/waves/round-58/l1/scores/c1-before.txt` (the routed carry-in set open at the base: R1 marker count 0, no round-58 hygiene receipts, 3-path orphan census, no w04 probe/table) and `scores/c2-before.txt` (census3 --check at the base exit 2, selftest 20/0, the malformed row located) | both arms red at the base, committed at the operative freeze | measured pre-data; a do-nothing control cannot land a precision correction note, a byte-identical receipt landing with its sweep receipt, a 19-row disposition table, or a parseable registry with a green drift check |

Assimilation: none — `considerthese/` does not exist in this lane (measured at
round start); the shokuknow register is unreachable from this host; the report
carries `Assimilation: none — shokuknow unreachable`.

## Mistakes

| id | class | evidence pointer | captured-by | fix / demonstrated limit |
|---|---|---|---|---|
| M58-1 | helper-argument grammar (absolute paths passed to a repo-relative helper) | the two helper attempts `634d12d622e71f51c604704dfef66c88091ed441` / `9e8ee220ce399fa11b23e1617862e3247d993491` carry base-tree + one bogus empty `C:` directory and no payload (their `declaration_pointer`-named files are absent from their trees); both are ancestors of main and pushed | this round's L1, by the immediate diff-tree re-derivation of the freeze commit (the M55-4 re-derivation rule applied to the helper itself: landed paths vs intended list) | disclosed in LOG, the container's declaration_pointer, and FREEZE; never cited as evidence; the branch heals forward — the recovery freeze `37e49cf3…` carries every intended path and REMOVES the bogus `C:` entry (the helper's own missing-on-disk removal clause, used deliberately). Rule: every treecommit invocation passes repo-relative paths, and every commit is diff-tree verified immediately after landing |
| M58-2 | writer grammar ≠ reader grammar (a registry row written in GFM-escape form the frozen parser does not implement) | the r55 v6-block-digest registry row at SKILL.md:1845 read as EIGHT cells to `tools/round-51/census3.py` (CensusError, exit 2 — `scores/c2-before.txt`), so the routed registry-drift census was unrunnable from the r55 landing until this round, while r55/r56/r57 kept routing it | the r57 planned item's own instrument, finally run this round at the base (`census3.py --check --rev 42c794af…`) | the row is reworded data-side (the escaped-pipe fragment becomes "table-pipe-leading"; the parser stays frozen, selftest 20/0 at the unchanged pin `a7538e5f…`); `--generate` at the landing derives 63 paths and `--check` at the record rev exits 0 (receipts under `records/`); the r55 section's own instruments record the "supersedes the unreproducible r54 16-hex value" history unchanged. Rule: a registry row is written in the reader's grammar — no escaped pipes in any instrument-registry cell; a routed census is executed (not re-routed) before the next round inherits it |
| M58-3 | list-diff quoting trap (string-comparing git's default-quoted output against raw filesystem names) | the first orphan census reported FIVE worktree-only paths, naming the two COMMITTED non-ASCII round-39 fixture paths (`…/icons/アイコン.txt`) as orphans — git's default `core.quotepath=on` prints them as `"\343…"` escapes that never string-match the worktree names; with `-c core.quotepath=off` both resolve in HEAD's tree (2 and 2) and the true orphan count is 3 (`records/orphan-census.txt`) | this round's L1, before anything acted on the false orphans (the disposition receipt had already been drafted with the wrong count and was rewritten) | the census of record runs `git -c core.quotepath=off ls-tree -r --name-only`; the drafted-then-corrected receipt pair is itself the demonstration. Rule: any probe that string-compares git listing output to filesystem names must disable path quoting first |

## Claim disposition (filled at the record commit)

C1 (calibration, the r57-closure routed carry-in set R1–R4): before all four
open at the base (`scores/c1-before.txt`), after all four closed with
committed, append-only artifacts — R1's correction note is the landing LOG
entry's first bullet (marker re-derived in `scores/c1-after.txt`); R2's sweep
named one live finding and the repair landed byte-identically at the landing
`05865b6d…` (receipt-audit on the r55 container → clean, checked 4;
record-audit "Round 55" → named 13, missing 0, re-run at the record rev in
`records/record-audit-green-r55.txt`); R3's probe + 19-row table and R4's
named-debt continuation landed at the freeze. C2 (depth, the registry-drift
census repair): before exit 2 unparseable at the base (`scores/c2-before.txt`),
after the row parses (63 rows / 0 malformed), `--generate` at the landing
derives 63 paths, `--check` at the record rev against the committed inventory
exits 0 (`records/census58-at-landing.json` + `scores/c2-after.txt`), the
historical mode stays exit 1 (frozen census2, the r51 authority note), and the
v6 triage-table digest `946e5359…` is byte-identical at base and landing
(no-harm). Verdicts in SCORECARD's round-58 section and LOG.

## Freeze

Operative freeze: `37e49cf33537ff182265c42f3fa546b1c0c0c0fa` — the first commit
adding `.ufo/waves/round-58/claims.json` (the recovery landing after the
M58-1 attempts; the attempts themselves land nothing and are disclosed, never
amended). No amendments to the operative freeze. The frozen instruments and
pins: `tools/round-51/census3.py` `a7538e5f…`, `tools/round-56/receipt-audit.py`
`897df532…`, `tools/round-57/record-receipt-audit.py` `3a5fff9a…` (unchanged
since r57), `tools/round-55/v6-block-digest.py` `22785c1e…` (unchanged since
r55), `tools/round-55/corrections-pin.py` `22f77c34…` (unchanged since r56),
`tools/round-29/freeze-gate.py` `25b54339…` (unchanged since r29) — bytes
unchanged from the claims commit through the tip.
