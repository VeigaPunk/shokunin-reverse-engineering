# Round 62 — the receipt corpus's base half becomes checkable: the base-binding sweep threads the frozen gate's --base-rev from each receipt's own bytes

Lane kaidoku, round 62, fresh-start binding honored (r50/r51/r52 re-read and
spot-checked with fresh probes), L1-inline on the Windows host (2026-11-02).
Round base `8374754b873c1f95ffddcbbe17007b5ef8eeadfc` (the r61 verifier
spot-check commit); carry-in `5047ec553827fa35b85113bf1a2b7845f8318069`
(the r61 outside decision recorded per QUALITY #34 BEFORE any claim was
measured; the closure routed NO new defects — the carried items restated:
19 standing W04, the r53 L0 open and routed around, the two standing
bare-name findings, the host adaptations); declaration
`dd193e888462d6bdfae38191fde1abadaac81036` (the plans + the new
instrument, the QUALITY #33 order); operative freeze
`b866cd8672f505c894c3c07f6496f30cfb720255` (the first commit adding
`.ufo/waves/round-62/claims.json`); landing
`f3adef27383ef7acc20ad98064b167c7e6b521dd` (the SKILL row + the
capability row; the seven-cell recount covers both the new row and the
r61 neighbor — M60-1/M61-2 applied). No wave (no dispatch surface on this
host; the kaidoku round-53 L0 question stays open and unanswered). Nine
frozen instruments (eight unchanged, one new:
`tools/round-62/base-binding-sweep.py`, pin `18273023…`), which COMPOSES
the frozen `tools/round-59/annotation-audit.py` (pin `ba9ccbb9…`,
byte-checked via `--expect-sha256` before every sweep run) instead of
duplicating it. The claim is offline over committed bytes.

## Gate

| row | URL / path / command and access | located quote (at most 25 words) | decision and limits |
|---|---|---|---|
| S262 | https://git-scm.com/docs/gitrevisions — fetched read-only with curl 2026-11-02 into the round scratch, snapshot bytes and sha256 committed at `.ufo/waves/round-62/l1/s262/` (gitrevisions.html `1ab7124a99e6919e6882be82f77c629ac8fe623bb36af56a749fd4db1919070b`, 74654 bytes) | "The full SHA-1 object name (40-byte hexadecimal string), or a leading substring that is unique within the repository." (18 words; locator: the `SPECIFYING REVISIONS` heading, the nearest preceding h1–h6 before the `<sha1>` item, verified programmatically against the snapshot; **plain** — contiguous in one `<p>` after whitespace normalization, no tag crossing, not composite) | admit, tier A docs (tool documentation — the category is the official git revision-syntax reference, the authority for what a complete revision binding is); mined: a receipt that binds a name to a 40-hex id binds a COMPLETE revision — the whole per-receipt base context the sweep threads into the frozen gate's `--base-rev`; abbreviations and sha256-length run-ons are not object names and never bind, so a threaded receipt always names an exact commit. Used by `plans/round-62-claims.md`, `tools/round-62/base-binding-sweep.py`, this lesson. |
| R62 reject 1 | extending the FROZEN `tools/round-60/annotation-sweep.py` (or the frozen r59 gate) with base threading instead of writing a new instrument | reject — the r60 planned field itself says threading "needs the frozen single-receipt gate's option threaded through a new instrument and its own freeze"; the gate is frozen at `ba9ccbb9…`, the sweep at `38614088…`; the new sweep COMPOSES the frozen gate (one argv subprocess per receipt, `--expect-sha256` pin check) so the per-receipt semantics stay byte-identical to the standing runs | reject row |
| R62 reject 2 | treating the sweep's zero base-class findings as "the corpus is verified base-true" | reject — the threaded set covers only receipts whose OWN bytes bind `base` (29 receipts, of which exactly ONE carries annotations in the frozen grammar): the other 28 threaded receipts are unevaluable (no annotation), and unbound receipts' base values stay unchecked by design; the honest claim is the capability delta (4 base probe instances re-derived for the first time, all agreeing), never a corpus-wide base-true verdict | reject row |
| R62 reject 3 | making the inventory's base statistics (annotation/probe instances) the verdict | reject — the mirror extractor/grammar in the sweep is REPORTING-ONLY (a verbatim copy of the frozen gate's shapes, labeled as such in the tool): the verdict always comes from the gate subprocess; a mirror drift could miscount the inventory but cannot flip any receipt's class | reject row |
| census receipts | the host-adapted census command at round start and at the filing tip; start receipt `.ufo/waves/round-62/l1/census-start.txt` (exit 0, 19 standing W04, 168 rows) | 19 standing W04 warnings; exit recorded in the receipt | host-adapted form (the `kaidoku-shokunin` mapped directory does not exist here); W04 stays debt |
| do-nothing control | `.ufo/waves/round-62/l1/scores/c1-before.txt` (instrument absent rc=128 at the base; 0 SKILL rows; 0 capability rows; 0 basesweep receipts; the r60 sweep's argv never carries the option — the argv-token probe 0 — with the limits line verbatim) | the arm is red at the base, committed at the operative freeze | measured pre-data; a do-nothing control cannot produce the instrument, the threading, the registration, or the first threaded inventory |

Assimilation: none — `considerthese/` does not exist in this lane (measured
at round start); the shokuknow register is unreachable from this host; the
report carries `Assimilation: none — shokuknow unreachable`.

## Mistakes

| id | class | evidence pointer | captured-by | fix / demonstrated limit |
|---|---|---|---|---|
| M62-1 | a compose seam contract mismatch that selftests with injected fakes cannot see — the sweep's 4-argument audit_fn contract called the gate runner's 5-parameter signature positionally, so on the FIRST unthreaded receipt the tool-path cell received `None` and the subprocess spawn crashed (`list2cmdline: expected str… not NoneType`) | the pre-commit dry run of the full sweep against the base rev (stderr traceback preserved in the round scratch); the selftest was green 46/0 at the same bytes because the injected fakes shared the wrong shape — the M46-3 rule ("one selftest case must reach the scored path with the production argument set") had a hole exactly where two frozen shapes meet | this round's L1, on the QUALITY #83/#84 dry-run discipline (the frozen counter itself, end to end, before the freeze); fixed BEFORE any commit | the fix re-orders the runner's signature to match the sweep contract (base_rev fourth, tool fifth) and adds a dedicated seam selftest case (the production closure shape wired through `sweep()` asserting the tool cell and the threaded argv both bound and unbound); post-fix selftest 50/0; the committed bytes were hash-verified worktree-vs-blob identical at the declaration (`18273023…` both sides, pasted in the round scratch) |
| M62-2 | arithmetic written where the probe's output belongs — in this round's own plans draft (the M60-3 class, caught BEFORE the freeze) | `plans/round-62-claims.md` BEFORE bullet predicted `grep -c 'base-rev'` → 0 on the r60 sweep; the pre-close re-derivation printed 1 — the token occurs exactly once, in the limits line that DOCUMENTS the gap; the precise probe is the argv token `'"--base-rev"'` → 0 (pasted in `scores/c1-before.txt` with the draft note preserved, the M61-1 pattern) | this round's L1, re-running the before-arm's own probes against the base before the freeze commit (the M57-1/M60-3 lineage) | the plans file gains an appended correction at the freeze naming the superseded text (the filed bullet stays as filed); the receipt lands with the corrected probe and the draft note; rule: a gap-documentation quote contains the very token a "never mentions it" grep would count — grep the BEHAVIOR (the argv token), not the mention |
| M62-3 | a verification snippet aborted mid-receipt (an index bug in the snippet itself, not in the data) and its traceback would have landed inside a receipt | the s262 digests receipt's first quote-verification run (`prev[2]` on a 2-tuple) crashed after printing two of four checks; re-run fixed pre-commit, the receipt rewritten with the note (nothing had landed — no correction-by-append was needed) | this round's L1, on the immediate re-read of the receipt bytes before the freeze | the landed receipt carries the four fixed-run outputs plus the aborted-first-run note; rule: a receipt assembled by a helper script is re-read line-by-line before commit — a traceback inside a receipt is a landing defect even when the data it verifies is true |

## Claim disposition (filled at the record commit)

C1 (depth, capability acquisition): before all open at the base
(`scores/c1-before.txt`), after the instrument is registered (SKILL row
7 cells pipe-free with the neighbor recounted, capability row, container
pin `18273023…`), the demonstrations stand: selftest 50/0
(`records/basesweep-selftest.txt`); the first threaded inventory at the
base — red exit 1 with no dispositions, 241 receipts, 0 invocation errors,
29 receipts threaded from their own bindings, 5 base annotation instances,
4 grammar-matched base probes re-derived for the first time (the r60
semantics checked 0), 0 base-class findings, the standing 5 finding keys
unchanged (`records/basesweep-inventory-red.txt`); green exit 0 with the
STANDING r60 disposition TSV unchanged — no uncovered keys, no orphans
(`records/basesweep-green-and-nothread.txt`); the `--no-base-thread`
equivalence arm — same 5 keys, 0 threaded, 0 base probes, per-receipt
classes identical; the pin fail-closed arm — a wrong `--expect-sha256`
exits 2 before any audit (`records/basesweep-pin-mismatch.txt`). The
duties ran to dispositions: the nine-container receipt-audit sweep (SEVEN
clean — the r61 container clean on first entry — plus the TWO standing
bare-name findings, dispositioned before the landing, no copy planted, the
fifth refusal), the record-audit over the r61 record section (clean), and
the two-direction orphan census (4 worktree-only dispositioned + 8
in-progress wave files + the 50-path aux/ class). census3 `--generate`
67 paths at the landing rev, `--check` at the record rev. The standing
halfway sweep re-runs at the record rev with the close. Verdicts in
SCORECARD's round-62 section and LOG.

## Freeze

Operative freeze: `b866cd8672f505c894c3c07f6496f30cfb720255` — the first
commit adding `.ufo/waves/round-62/claims.json`. No amendments to the
operative freeze; the plans correction (M62-2) is an append carried BY the
freeze commit, never a rewrite of the landed bullet. The frozen instruments
and pins: `tools/round-62/base-binding-sweep.py` `18273023…` (new,
committed at the declaration `dd193e88…` before the claims file),
`tools/round-61/numstat-edge-audit.py` `6b967e20…`,
`tools/round-60/annotation-sweep.py` `38614088…`,
`tools/round-59/annotation-audit.py` `ba9ccbb9…` (the frozen gate the sweep
composes, `--expect-sha256` checked before every sweep run),
`tools/round-51/census3.py` `a7538e5f…`, `tools/round-56/receipt-audit.py`
`897df532…`, `tools/round-57/record-receipt-audit.py` `3a5fff9a…`,
`tools/round-55/v6-block-digest.py` `22785c1e…`,
`tools/round-29/freeze-gate.py` `25b54339…` — bytes unchanged from the
claims commit through the tip.
