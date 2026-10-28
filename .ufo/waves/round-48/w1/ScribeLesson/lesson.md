# Round 48 — the verdict digit becomes a meaning, and the record re-derives its own completeness

Lane `kaidoku`, round 48, attempt 1. Base `61b87d742032e65fca9c38267d7d6ed7e555edad`.
Declared freeze `0f06251bf6a3a6964c715f67243d4df12e854258` (A4) — a disclosed series
`7fe11332` → A1 `dc73587a` → A2 `ac02a79f` → A3 `f3a7afc4` → A4 `0f06251b` (see
`plans/round-48-claims.md` A1–A4 and the disclosures below). Instruments
`tools/round-48/{meanings,record2}.py` with `census2.{py,json}`; landing surfaces
`SKILL.md` craft block 25, the instrument-registry meaning rows, `SCORECARD.md`
`## Round 48` + `## Record corrections — round 48` and the Owned-axes head.

The round exists because the round-47 spot-check routed two HIGH defects
(`corpus/lessons/round-47.md:36-44`): R46-CL7 (the registry bound the digits 0/1/2,
not their meanings — `0=banana` scored met) and R47-CL10 (both round-47 predicates
were satisfiable by an artefact that does no work — membership, never keyed
correctness; consistency, never completeness). R48-C1 binds each verdict digit to a
meaning class and each routed row to its expected arm; R48-C2 re-derives the record
with a per-class completeness floor, receipt-bound quotes, an `axes`-correction
grammar and a score-cell binding.

## Mistakes

| id | class | evidence pointer | captured-by | fix (shown able to fail) |
|---|---|---|---|---|
| M48-1 | `vacuous-clause` — `record2.axis_scores()` read the *evidence* cell where it meant the *score* cell, so clause 5 iterated zero rows: `axis_score_cells {}` with `axis_score_bad []` is green over nothing, the same "accepts every candidate" shape as round-47's A2/A5 `no-op-forgery` rows (M47-2) — a stale Owned-axes score would have passed untouched | `plans/round-48-claims.md` amendment A1; `.ufo/waves/round-48/controls/ctl-c2-a1-before.json` (`axis_score_cells: {}`, `met_target: false`, rev `7fe11332`) | `none` at freeze time — the pre-freeze satisfiability check still asks "can the counter compute a value", never "does the value come from the cell the clause names"; the `axes-score-cell-off` forgery existed in the battery but batteries do not run while the artefact fails an earlier clause (see R48-CL3) | A1 `dc73587a` reads `cell[0]`; wave receipts at the A1 bytes report non-empty `axis_score_cells` (`coverage 138/138 → 10.0`, `depth 24/24 → 10.0`) with `axis_score_bad []` — `w1/C2Axes/receipt.json`, `w1/C2Battery/receipt.json` |
| M48-2 | `type-confusion-equality` — clause 8's freshness check compared the re-derived census **object** with the committed `paths` **list** (`derived == doc["paths"]`), so `census_rederived_equal` could never be true: a clause that fails by construction on a correct artefact, unreachable in any committed receipt while block 25 is absent | `plans/round-48-claims.md` amendment A3; `.ufo/waves/round-48/controls/ctl-c1-a3-simulation.json` (`census_rederived_equal: true` on a path-equal registry, failing names the clause at the A2 bytes); wave-1 `w1/C1Census.md` (the `derived == doc["paths"]` line at the A1 bytes) | `none` — no do-nothing control can reach a clause guarded by an absent artefact; found by seats running the counter's own `score()` over synthetic inputs (`C1Census`, `LabC1Meaning`) | A3 `f3a7afc4` compares `derived["paths"]`; residual routed as R48-CL2 (the clause text still says the committed census *equals* the derivation while the check binds only the `paths` list — the `named` map may drift silently) |
| M48-3 | `false-green-class-pair` — two checks accepted what they should reject: (a) the exit-0 classifier matched `\bmet\b`, which also matches inside `not met`, so `0=not met; 1=violation; 2=usage` scored as success/not-met/unevaluable — an opposite-polarity false green; (b) `registry_rows()` recognised only rows whose stripped line starts ``| ` ``, so a row written ``|  `path` `` was skipped by the path-set and meaning checks | (a) `w1/C1Gold.md` (the exact map); (b) `w1/CritAxis.md` (the fixture mutation) and `w1/CritSeparability.md`; `plans/round-48-claims.md` amendment A4 | adversarial wave seats — the selftest's 16 cases passed while both holes were open (`w1/C1SelfTest.md`: `cases=16 failures=0`); grammar tests asked "is this well-formed", not "is a misformed variant refused" | A4 `0f06251b` adds `NEGATED` (`not met` / `no verdict`) to the exit-0 guard, widens `ROW_START` to `^\|\s*`` ` and fails closed on a non-7-cell row, plus selftests `red-opposite-polarity` / `red-hidden-row`; residual routed as R48-CL1 (NEGATED is a two-phrase closed vocabulary; exits 1/2 carry no negation guard) |

## Measured before the landing (wave-1 receipts)

- C1 at the A1 bytes: exit 1, `marker_occurrences 0 != 1`, `marker_block_count 0 != 1`,
  `rule_blocks 24` — `controls/ctl-c1-0-do-nothing.json`, `w1/C1Battery-2/receipt.json`
  (stdout sha256 `95c01672…`, UTC 2026-10-28T18:47:34Z via `w1/C1Gold.md`). The registry
  holds 40 rows for 42 census paths; `tools/round-48/meanings.py` and `record2.py` have
  none (`w1/C1Census.md`, `w1/ExecCensus.md` — the committed census *does* equal a fresh
  derivation at the freeze, sha256 `403b4c14…`).
- C2 at the A1 bytes: exit 1 — `round-47: no seat atom and no re-derived seats
  correction`, `no ## Record corrections — round 48 line re-derived`, `quoted numbers
  with no backing receipt: 1` (the card quotes `exempted 2`; both cited round-47
  receipts read `exempted 1`). The round-47 oracle executed from `--rev` bytes is green
  (`atoms 44`, `mismatches []`, `met_target true`). Identical receipt sha256
  `f0bf3d66…` across `w1/C2Floor`, `w1/C2Battery`, `w1/C2Corr`, `w1/C2Axes`, `w1/C2Quote`.
- `--profile v2` accepts the same freeze card (`controls/ctl-c2-1-v2-profile.json`,
  `met_target: true`) — the hole the claim closes, committed as a control.
- `w1/C2Oracle` stubbed the worktree `tools/round-47/record.py` and got byte-identical
  output: the oracle genuinely executes committed bytes (R47-CL1 closed for the oracle).
- `w1/C2Quote` measured the quote grammar: a `corrects quote round-47: exempted 1` line
  re-derives and clears `quotes_bad`; an already-right correction is refused
  (`the section already quotes that value`); an out-of-window round is refused
  (`no round-45 section in scope`).
- `w1/C1Pins` verified the mutations pin now covers each mutation's name **and body**
  (body-bearing digest `80010be3…` ≠ names-only `dbf00169…`; a scratch body edit moves
  the digest) — R47-CL4 closed as specified. Block pin in `l1/block25.md`:
  `mutations_sha256:25ce025f…`, `interpreter_sha256:74b8da35…` — the interpreter pin
  equals the **A2** bytes; A4's bytes are `cd4dbad8…`, so the pin must follow the freeze
  the landing is scored at (R47-CL8 recurrence, see routed list).
- ScribeLesson probe over the frozen A4 classifier (`w1/ScribeLesson/classifier-probe.json`,
  command in the seat report): `0=not clean`, `0=never passed`, `1=not failed`,
  `2=no error` all classify green — the A4 fix refuses exactly the two phrases it was
  shown, not the class.

## Freeze series (disclosed, not folded)

| amendment | defect | red-before |
|---|---|---|
| A1 `dc73587a` | the axis-score clause read the evidence cell, so it scored nothing (M48-1) | `controls/ctl-c2-a1-before.json` |
| A2 `ac02a79f` | the exit-0 classifier rejected a legitimate success meaning (`0=met with failing empty` — `failing` in prose tripped the not-met guard) | 16-row list at the A1 bytes, `plans/round-48-claims.md` A2 |
| A3 `f3a7afc4` | the census clause compared a derived object with a committed list (M48-2) | `controls/ctl-c1-a3-simulation.json`, `w1/C1Census.md` |
| A4 `0f06251b` | the exit-0 classifier accepted `0=not met`; the row parser skipped ``|  `path` `` (M48-3) | `w1/C1Gold.md`, `w1/CritAxis.md` |

The freeze is a series again — five commits in the round, four of them after the wave
was already running: every wave receipt above was captured at the A1 bytes while the
operative freeze is A4 (the wave's seat prompts declare `dc73587a`; the claims file's
own rule — the last commit touching `plans/round-48-claims.md`/`tools/round-48/` —
derives `0f06251b`). R47-CL5/R47-CL11 recur verbatim; routed below.

## Gate

The L1's staged rows (uncommitted `corpus/SOURCES.md` + `corpus/lessons/round-48.md`)
are S145/S146 (unmodified). Wave seats filed three further rows: S147/S148 by
`w1/ScribeSources/sources.md`, and provisional S149 (`argparse` admit) / S150
(`sysexits` FreeBSD reject) filed by `w1/ScoutSources.md` — provisional because ids
are not skipped: they hold iff S147/S148 land first. If the L1 lands a subset,
renumbering is mechanical.

### Sources opened this round (2026-10-28)

| row | source | accessed | located quote (≤25 words) | decision |
|---|---|---|---|---|
| S145 | https://plato.stanford.edu/entries/popper/ (SEP, *Karl Popper*, §2 The Problem of Demarcation; sha256 `2c2d48c6891418c4…`) | 2026-10-28 | "if a theory is incompatible with possible empirical observations it is scientific; conversely, a theory which is compatible with all such observations" (22 words) | **admit** (tier A, `mined`). Grounds the round's own defect class — a clause that cannot fail is not a check — which is exactly M48-1/M48-2 (a green clause over zero rows; an equality false by construction). Province check: grounds the lane's instrument discipline, no RE surface claim; cited by this lesson only. |
| S146 | https://man7.org/linux/man-pages/man3/sysexits.h.3.html | 2026-10-28 | none — HTTP 404 (196-byte body, sha256 `80c3fe2ae1062abf…`) | **reject** (tier C, `rejected`). Unreachable at this URL, so no locator exists to quote; `unreachable` is not fabrication, but it is also not evidence. Flip (as the registry row has it): open `man 3 sysexits` locally or the FreeBSD handbook page and quote the `EX_USAGE` line; then the row can ground exit 2 as a usage refusal. Row unchanged this round — the mirrors that flip names were opened by wave seats and are filed as their own row (S150): quoting `EX_USAGE` returns **64**, which falsifies the predicted admit rather than satisfying it. |
| S147 | https://docs.python.org/3/builtins/functions.html#exec (requested `3/library/functions.html`, which 301-redirects to `3/builtins/functions.html`; sha256 `41a0311cc1d5a7dcdeba4fe80a9ffda90c770b77e1a30b4434502f62a118c084` is the final builtins page) | 2026-10-28 | "This function supports dynamic execution of Python code. source must be either a string or a code object." (18 words) | **admit** (tier A, `mined`). Grounds R48-C2's oracle clause: `record2.py:62-71` runs `exec(compile(body, ORACLE, "exec"), ns)` over `git show <rev>` bytes — the committed bytes themselves, never the worktree file (the R47-CL1 repair). |
| S148 | https://docs.python.org/3/library/runpy.html (HTTP 200, 38,257 B, sha256 `69465f0d5587d68437b735018335ddbc8db625122e36453a928259ce59b56bde`) | 2026-10-28 | "Execute the code at the named filesystem location and return the resulting module's globals dictionary." (15 words) | **reject** (tier C, `rejected`). Every entry point resolves a path or module name — the worktree-execution indirection R47-CL1 routed; no `exec` token in the rendered text and no from-bytes primitive. Flip: an edition that accepts a source string or code object directly. |
| S149 (provisional — the next free id iff S147/S148 land; ids are not skipped) | https://docs.python.org/3.14/library/argparse.html#argparse.ArgumentParser.error | 2026-10-28 | "This method prints a usage message, including the message, to sys.stderr and terminates the program with a status code of 2." (21 words) | **admit candidate** (tier A; filed by `w1/ScoutSources.md`, HTTP 200, 330,759 B, sha256 `896dc9a8dfd24109060f0453d899830e361040f536878aa9c727be221b4dd55b`; this seat's parallel capture of `3/library/argparse.html`, 334,734 B, sha256 `521adff647…`, is uncited). Status `queued` until the landed lesson cites the row; `used-by corpus/lessons/round-48.md` once it lands. Scope is `ArgumentParser.error` only: status 2 *for that method* — `--help` prints `usage:` and exits 0 — it does not define exit 1 as not-met and does not ground `absent`, `unreadable`, `could-not-evaluate` or `frozen_path_changed`. |
| S150 (provisional — next after the argparse row) | https://man.freebsd.org/cgi/man.cgi?query=sysexits&sektion=3&manpath=FreeBSD+14.3-RELEASE (HTTP 200, sha256 `51978a07e38901d90aecd7639d4d3e3ecb0aefb99e7e6d7b3d62cfd8937da8f8`, `w1/ScoutSources.md`) | 2026-10-28 | "EX_USAGE (64) The command was used incorrectly, e.g., with the wrong number of arguments" (14 words); also "The successful exit is always indicated by a status of 0, or EX_OK." (13 words) | **reject** (tier C, `rejected`). Candidate grounding for the registry's 0/1/2 meanings — but `sysexits` binds usage to **64**, not 2, and the FreeBSD page says the interface "has been deprecated" and its use "is discouraged", so it contradicts the registry's `2=unevaluable` class rather than grounding it. This is the row S146's flip pointed at; the located quote falsifies the predicted admit, so the row enters as a second, scoped rejection. Flip: a published sysexits that defines the integer 2 as incorrect usage or as could-not-evaluate. |

Search log (screened, no rows): this seat's own capture of the OpenBSD mirror
`https://man.openbsd.org/sysexits.3` (HTTP 200, 12,147 B, sha256 `4cf3eb9d…`,
quote "A few programs exit with the following non-portable error codes. Do not use
them.") corroborates S150 without being part of its row; `sys.html`
(`sys.exit`, zero/nonzero only, sha256 `867b5a26…`) and this seat's
`3/library/argparse.html` capture (sha256 `521adff647…`) are screened duplicates —
no rows.

- **Assimilation: none taken in this draft.** The merge package
  (`/home/vgpnk/Projects/shokuknow/merge/kaidoku/`) stages 77 knowledge entries and 132
  rows against the lane's 138 knowledge files and 144 committed rows; wave-1
  `ScoutAssim`/`CritAssim` verdicts were not in the report directory when this lesson was
  drafted. The staged lesson skeleton states no adoption; nothing here contradicts it.
- **Census before → after:** committed `corpus/SOURCES.md` rows 144 → staged 146
  (S145 mined, S146 rejected) → 148 if S147/S148 land (`w1/ScribeSources/sources.md`),
  → 150 if the `argparse` admit and the FreeBSD `sysexits` reject also land
  (`grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md` → 146 in the staged
  worktree). Status/recheck/used-by changes to existing rows: none. Round-end census:
  `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku`
  (run by the L1 at landing; not run by this seat).

## Routed defects (for round 49)

Filled from the wave's reports; each item names the seat that found it. CL numbering
continues the lane series.

- **R48-CL1 (HIGH; wave-1 `ScribeLesson`, measured; `C1Gold`/`C1RowsB`/`C1Semantic`
  source-concurring).** A4 fixed the two demonstrated negations, not the class:
  `NEGATED` is exactly `\bnot\s+met\b|\bno\s+verdict\b` and only guards digit 0, so
  `0=not clean`, `0=never passed` classify as success and `1=not failed`,
  `2=no error` classify as not-met / unevaluable
  (`w1/ScribeLesson/classifier-probe.json`, at the A4 bytes). Distinctness compares
  raw segment text, not meanings (`C1RowsB`), and a segment may carry tokens of other
  classes unpenalised. Closing it needs polarity handled per class (a negated mention
  of any token rejects that segment), or an allowlist of whole-segment values; add the
  maps above to the battery/selftest.
- **R48-CL2 (MEDIUM; wave-1 `C1Census`/`ExecCensus`, measured).** The A3 check binds
  only `derived["paths"]` while clause 8 reads "the committed `census2.json` equals a
  fresh derivation" — the `named`/`named_but_absent` map may drift unobserved:
  `w1/ExecCensus.md` shows the worktree derivation differs from committed
  (`round-48` names 5 vs 4 paths; doc sha256 `36556d11…` vs `403b4c14…`) with an
  identical path set, so `census_rederived_equal` stays true over a different
  document. Compare the whole document, or narrow the clause text to "path set".
- **R48-CL3 (MEDIUM; wave-1 `C2Battery`/`C2Floor`/`C1Battery-2`, measured).** Every
  battery is conditional on a fully green genuine artefact: `evaluate()` skips the
  battery on any nonzero score (`battery.skipped` in every wave receipt; C2
  `record2.py:443-471` by `w1/C2Battery.md`), so the kill rules were never exercised
  before the landing and a weak battery cannot be distinguished from an unrun one.
  The claimed control `ctl-c1-1-v2-profile.json` is named in the frozen claims file
  but absent under `controls/` (`w1/C1V2.md`) — a named-evidence gap of the same
  class. A per-mutation standalone mode (`--battery-only` against synthetic genuine
  inputs, which `C1Census`/`C2Quote` already drove by hand) would make the kill rule
  testable pre-landing.
- **R48-CL4 (HIGH, inherited recurrence; wave-1 `C2Oracle`/`C2OracleLimit`, measured +
  source).** R47-CL1 is closed for the *oracle* (a stubbed worktree
  `tools/round-47/record.py` produced byte-identical output — `w1/C2Oracle`), but
  `record2.py:35-37` still inserts the worktree `tools/round-46/` on `sys.path` and
  imports `gate` from the checkout: a worktree `gate.py` is still an unexamined
  instrument that can flip the freeze gate, the committed-byte reads and the verdict
  (`w1/C2OracleLimit.md`; the executed round-47 oracle resolves `gate` through the same
  already-populated `sys.modules`). Same for the counter scripts themselves, which
  still execute from the worktree. Closing it: execute the round-46 gate from committed
  bytes too, or state the narrowed claim.
- **R48-CL5 (HIGH, R47-CL11 recurrence; wave-1 `CritClaims`/`C2LandingGate`, and this
  round's own series).** The declared freeze is a moving target mid-wave: the wave ran
  against `dc73587a` (A1) while the claims file's own derivation rule — the last commit
  on the frozen pathspec — resolves `0f06251b` (A4), and each amendment rewrites the
  artefacts receipts were measured against. All receipts cited above are measurements
  of a superseded freeze and must be re-taken at the landing revision. The recurrence
  also re-opens R47-CL8 in practice: `l1/block25.md`'s `interpreter_sha256` pin equals
  the A2 bytes (`74b8da35…`) while A4's are `cd4dbad8…`, so each counter amendment
  still forces a landing edit. A freeze series needs a receipt-rebaseline step or a
  declared freeze in an artefact the counter does not freeze.
- **R48-CL6 (MEDIUM; wave-1 `C1Semantic`, source-reviewed).** The three-class
  partition is forced onto instruments without a three-way verdict: probes that write
  receipts, tools that propagate a child's status, and a library (`gate.py`) with no
  standalone exit map must still invent success/not-met/unevaluable cells that satisfy
  the regexes without being true of the tool. A `n/a` class or a per-row exemption
  with a stated reason is more honest than a grammatical verdict.
- **R48-CL7 (LOW; wave-1 `C1Refs`/`C2Oracle`, measured).** `--json-out` refuses any
  path outside the lane root (exit 2), which forces evidence into `.ufo/` and couples
  receipt custody to the lane tree — awkward for fixture clones (`D=$(mktemp -d)`)
  where a receipt then lands inside the fixture. Not a verdict defect; a `--stdout`
  mode or a scratch-allowlisted output root would decouple it.
- **Inherited, still open:** R46-CL1 (squash-invisible tamper), R46-CL5 (registry
  `purpose` cell unchecked — the wave added nothing; a forged purpose cell still
  passes), R46-CL8 (`--selftest` non-runnable form from the claims file), R47-CL1
  residual (see R48-CL4), R47-CL3 (`CORR_MIN` floors count, not materiality),
  R47-CL5/CL11 (freeze-as-series; see R48-CL5), R47-CL8 (pin coupling; see R48-CL5),
  R47-CL9 (`--profile` is not a pure selector — the ported-profile control must run
  `--no-battery`; unverified in this round's battery because every battery skipped),
  R47-CL15 (fixture-builder directory-citation crash — `plans/:N` still unhandled;
  not retested).

### Landing gates the record must satisfy (from the wave's measured reds)

- a re-derived `seats` correction for round 47 (the oracle collects no seat atom for
  it; grammar form `<n> waves, <total> seats total`, `w1/C2Corr.md`);
- a `corrects quote round-47: exempted 1` line citing the receipt the section cites
  (`w1/C2Quote/misquote-repaired.json` re-derives it);
- every other `atoms|exempted|corrections|mismatches N` quoted in `## Round 48` backed
  by a cited receipt cell;
- `## Record corrections — round 48` present with every line re-deriving, including an
  `axes` line only if it names the card's real pair;
- the C1 pin read at the **landing** revision, not A2 (`w1/C1Pins.md`, `l1/block25.md`).

## Axes

- coverage: all 25 landed wave-1 reports read plus the L1 staging (`block25.md`,
  `scores/`), the six committed controls, the claims file in full, and the frozen
  counters' relevant bodies at base/A1/A2/A4 bytes.
- depth: defects verified against the frozen bytes (`meaning_classes` executed over A4
  source in `w1/ScribeLesson/classifier-probe.json`; `registry_rows`, `ROW_START`,
  `census_rederive` and the `derived["paths"]` comparison inspected at
  `7fe11332`/`dc73587a`/`ac02a79f`/`0f06251b`); A3/A4 read as amendments, not just
  commit titles.
- calibration: every quoted receipt value above (`exempted 1` vs quoted `exempted 2`,
  `axis_score_cells {}`, sha256 `f0bf3d66…`/`403b4c14…`/`74b8da35…`/`cd4dbad8…`,
  `cases=16`) was taken from a named receipt or `git show` output; unmeasured items are
  marked "not run" or "source-level".
