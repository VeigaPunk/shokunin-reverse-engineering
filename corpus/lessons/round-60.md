# Round 60 — the halfway receipt-corpus sweep: the multi-receipt annotation-consistency instrument, and the first complete inventory of the lane's own receipts

Lane kaidoku, round 60, fresh-start binding honored (r50/r51/r52 re-read and
spot-checked), L1-inline on the Windows host (2026-11-01) — the campaign's
halfway round for this lane. Round base
`48c418305b71ea603e58f4fe9bd0dfbf2aafa9e4` (the r59 verifier spot-check
commit); carry-in `ec9d93d7dcf72ba2aff88b3d72a3e39910bbc820` (the r59
outside decision recorded per QUALITY #34, and the orphaned r59 selfcatch
receipt lands byte-identically with provenance — the r58-R2 pattern; the
disclosed provenance-receipt fixup is
`691460faa2f326df71407ed88bfe0a6152a10a3f`); declaration
`eb4f6a7f8b37bc8a8843bcade7cbe959dc7dfff9` (the plans + the new instrument,
the QUALITY #33 order); operative freeze
`8e58366300aa30c097c81e68df2d0d30c689ed6f` (the first commit adding
`.ufo/waves/round-60/claims.json`); landing
`bbdb03abdafd777b10767071f3a16267bcccf866` (the SKILL row + the capability
row; the glued-insertion self-catch repaired before any commit — M60-1). No
wave (no dispatch surface on this host; the kaidoku round-53 L0 question
stays open and unanswered). The claim is offline over committed bytes; six
frozen instruments unchanged, one new instrument
(`tools/round-60/annotation-sweep.py`, pin `38614088…`), which COMPOSES the
frozen `tools/round-59/annotation-audit.py` (pin `ba9ccbb9…`, byte-checked
before every run) instead of duplicating it.

## Gate

| row | URL / path / command and access | located quote (at most 25 words) | decision and limits |
|---|---|---|---|
| S260 | https://docs.python.org/3/library/subprocess.html — fetched read-only with curl 2026-11-01 into the round scratch, snapshot bytes and sha256 committed at `.ufo/waves/round-60/l1/s260/` (subprocess.html `6e86cc82712142d8adc374042d96c706886e1606faac803366e693575d09685b`, 208624 bytes) | "The recommended approach to invoking subprocesses is to use the run() function for all use cases it can handle." (19 words; locator: the `Using the subprocess Module` heading, first paragraph under it; labelled **composite** per QUALITY #42 — the words `run()` sit inside an inline literal span between plain-text words; contiguous in the tag-stripped, whitespace-collapsed snapshot text) | admit, tier A docs (tool documentation — the category is the Python standard library reference, the authority for the process-composition semantics the sweep is built on); mined: the recommended invocation helper is `run` with argv args, so a driver can compose the frozen single-receipt gate as one argv subprocess per receipt — the checker's bytes execute exactly as the standing r59 demos ran them, with no shell between driver and tool (`sys.executable -X utf8 -I -B`, the sweep's `audit_one`). Used by `plans/round-60-claims.md`, `tools/round-60/annotation-sweep.py`, this lesson. |
| R60 reject 1 | extending the FROZEN `tools/round-59/annotation-audit.py` with a multi-receipt sweep mode instead of writing a new instrument | reject — the gate is frozen at its declaration pin `ba9ccbb9…`; the r59 planned field itself states "a multi-receipt sweep mode would need a new instrument and its own freeze"; the sweep COMPOSES the frozen gate (one argv subprocess per receipt) so the per-receipt semantics stay byte-identical to the standing demos | reject row |
| R60 reject 2 | planting a third byte-identical copy of `freeze-gate-tip-90f3a9b9.json` under `.ufo/waves/round-58/` so this round's receipt-audit duty (which re-named the bare-name finding over the seven containers) stops firing | reject — the same finding r58 reject 1 and r59 reject 1 refused to shape away; the r59 non-author closure ruled the flip condition does NOT fire (the T4 sentence is a quotation naming its true scope); the finding persists as disclosed named debt at every rev this round ran | reject row |
| R60 reject 3 | generating the disposition-table texts mechanically (emitting uniform "disclosed" boilerplate per finding from the sweep itself) | reject — the sweep's own contract states disposition text is not truth-checked: a disposition's honesty rests on the citations it names, which a non-author re-derives; each of the five rows is hand-written and cites a standing receipt, the appended correction block, or a fresh hand re-verification (`records/sweep-first-inventory.txt`) | reject row |
| census receipts | the host-adapted census command at round start and at the filing tip; start receipt `.ufo/waves/round-60/l1/census-start.txt` (exit 0, 19 standing W04, 166 rows) | 19 standing W04 warnings; exit recorded in the receipt | host-adapted form (the `kaidoku-shokunin` mapped directory does not exist here); W04 stays debt |
| do-nothing control | `.ufo/waves/round-60/l1/scores/c1-before.txt` (instrument absent rc=128 at the base, 0 registry rows, 0 capability rows, 188 receipts enumerated, 0 complete inventories, the red run's 5 findings named) | the arm is red at the base, committed at the operative freeze | measured pre-data; a do-nothing control cannot produce the inventory, the disposition table, the green arm, or the registration |

Assimilation: none — `considerthese/` does not exist in this lane (measured
at round start); the shokuknow register is unreachable from this host; the
report carries `Assimilation: none — shokuknow unreachable`.

## Mistakes

| id | class | evidence pointer | captured-by | fix / demonstrated limit |
|---|---|---|---|---|
| M60-1 | insertion anchor ≠ insertion point (the SKILL row's edit anchored on the SHARED row-tail string — the two final cells every registry row ends with, `--json-out` write-scope plus `kaidoku` owner, together with the registry marker — which glued the new row onto the r59 row and consumed the r59 row's last two cells) | the seven-cell recount read 12 cells on the glued line; the pipe-position dump showed the r59 row ending mid-tail at `d581-correction.txt` with the next cell opening the NEW row's path | this round's L1, BEFORE any commit (the M59-1 recount rule applied to the neighbor too) | the repair restored the r59 tail cells and put the new row on its own line; post-repair: r59 row 7 cells (tail intact), r60 row 7 cells, SKILL delta vs the freeze exactly `1 0` (numstat-verified). Rule: an insertion into a table anchors on the UNIQUE structural marker (the registry comment line), never on a repeated row suffix — and the recount covers BOTH the new row and its neighbor before landing |
| M60-2 | a receipt written before the commit it cites carried a literal placeholder (`<carry-in commit>`) where a sha belongs | `.ufo/waves/round-60/l1/records/selfcatch-provenance.txt` landed in the carry-in commit with the placeholder in its post-landing-verification section (the chicken-and-egg: the receipt is provenance FOR the commit that carries it) | this round's L1, on the immediate re-read of the landed bytes | the disclosed one-line fixup `691460fa…` fills the carry-in sha and pastes the rc=0 + byte-identity re-derivations; the landing copy stays as filed (append-only). Rule: a receipt that must cite a commit created by its own landing either names the filling as the next commit's explicit job or is written after — never a placeholder in a filed byte |

## Claim disposition (filled at the record commit)

C1 (depth, capability acquisition): before all open at the base
(`scores/c1-before.txt`), after the instrument is registered (SKILL row
7 cells pipe-free, capability row, container pin `38614088…`), the first
complete inventory exists (red exit 1: 188 receipts, 2 green, 2
findings-class, 184 unevaluable, 0 invocation errors, 5 findings), the
disposition table covers exactly the 5 keys with citations (green exit 0),
the same corpus flips back to exit 1 with one row removed (the fail-closed
demo), the first-inventory finding is hand re-verified before its
disposition (the bound command re-runs to 1 at the rev it names), and the
duty runs to dispositions: the seven-container sweep (six clean + the r58
standing finding, no copy planted), the record-audit (r59 named 21 missing
0 clean), and the orphan census (the selfcatch discovery repaired
byte-identically in the carry-in; the r55 orphan retained-and-disclosed;
two gitignored caches; the 50-path aux/ class). census3 `--generate` 65
paths at the landing rev, `--check` at the record rev exit 0. Verdicts in
SCORECARD's round-60 section and LOG.

## Freeze

Operative freeze: `8e58366300aa30c097c81e68df2d0d30c689ed6f` — the first
commit adding `.ufo/waves/round-60/claims.json`. No amendments to the
operative freeze; the disclosed fixup (`691460fa…`, the provenance receipt's
sha filled) is a new one-line commit, never a rewrite of a landed byte. The
frozen instruments and pins: `tools/round-60/annotation-sweep.py`
`38614088…` (new, committed at the declaration `eb4f6a7f…` before the
claims file), `tools/round-59/annotation-audit.py` `ba9ccbb9…` (unchanged
since r59; the frozen gate the sweep composes, `--expect-sha256` checked
before every sweep run), `tools/round-51/census3.py` `a7538e5f…` (unchanged
since r51), `tools/round-56/receipt-audit.py` `897df532…` (unchanged since
r56), `tools/round-57/record-receipt-audit.py` `3a5fff9a…` (unchanged since
r57), `tools/round-55/v6-block-digest.py` `22785c1e…` (unchanged since r55),
`tools/round-29/freeze-gate.py` `25b54339…` (unchanged since r29) — bytes
unchanged from the claims commit through the tip.
