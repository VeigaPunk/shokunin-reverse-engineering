# Round 62 claims — kaidoku (declared before any claims file; the instrument below was committed in the SAME commit, BEFORE `.ufo/waves/round-62/claims.json` — the QUALITY #33 order)

Round base: `8374754b873c1f95ffddcbbe17007b5ef8eeadfc` (the r61 verifier
spot-check commit). Carry-in: `5047ec553827fa35b85113bf1a2b7845f8318069`
(the r61 non-author closure recorded, QUALITY #34; no new routed defects;
the carried items restated). Fresh-start binding honored: the r50/r51/r52
rejected closures are re-read and spot-checked with fresh probes, receipted
at the freeze (`scores/freshstart-spotcheck.txt`).

## R62-C1 — depth, capability acquisition: the base-binding sweep

**The gap (named twice on the record).** The r60 record planned it and the
r61 record kept it: the frozen single-receipt gate
`tools/round-59/annotation-audit.py` carries a `--base-rev` option —
"optional: also re-derive each annotation's `base:` value at this
revision" — but no multi-receipt instrument ever threads it. The r60
sweep's own limits line is the documentation of the gap:
"`--base-rev` re-derivation is not swept (the base of each historical
annotation is the single gate's option, available per receipt)". So across
the lane's whole receipt corpus, no instrument has ever mechanically
checked the `base:` half of any `base: N -> record: M` annotation: the
sweep semantics verified record values only.

**The capability.** `tools/round-62/base-binding-sweep.py` — a
multi-receipt sweep that composes the FROZEN r59 gate (one argv subprocess
per receipt, `--expect-sha256` byte-pin checked before every run, the r60
pattern) and threads `--base-rev` from each receipt's OWN bytes: the r61
binding grammar (a lowercase name token, optional `commit`/`rev` word,
40-hex id, hex run-ons rejected by negative lookahead) scanned in the
receipt's committed bytes; a receipt is base-THREADED iff a binding named
exactly `base` exists (first occurrence wins); `--no-base-thread` disables
threading fleet-wide (the equivalence arm). Findings keys are identical to
the r60 key format, so the standing round-60 disposition table stays
compatible. Verdict map identical to the r60 sweep: 0 inventory complete /
1 findings uncovered / 2 could-not-evaluate (zero receipts, invocation
error, pin mismatch, git failure). A receipt with no `base` binding runs
unthreaded — unchanged r60 semantics, reported as such in the inventory.

**Sourced claim (S262).** https://git-scm.com/docs/gitrevisions (fetched
read-only this round; snapshot + sha256 at `.ufo/waves/round-62/l1/s262/`):
"The full SHA-1 object name (40-byte hexadecimal string), or a leading
substring that is unique within the repository." (locator: the `SPECIFYING
REVISIONS` h2 — verified programmatically as the nearest preceding heading
in the snapshot; plain contiguous sentence in one `<p>`, whitespace
normalized, no tag crossing — not composite). This is why the binding
grammar binds exactly 40-hex with run-on rejection: a receipt's self-named
40-hex `base` binding is a COMPLETE revision binding — the whole per-
receipt base context the threading needs — while abbreviations and
sha256-length hex strings are not object names and never bind.

**Falsifiable before → after** (counting commands run on THIS host against
committed bytes):

- BEFORE, at the base `8374754b…`:
  - `git cat-file -e 8374754b…:tools/round-62/base-binding-sweep.py`
    → rc 128 (the instrument does not exist);
  - `git show 8374754b…:SKILL.md | grep -c 'base-binding-sweep'` → 0
    (no registry row); `git show 8374754b…:SCORECARD.md |
    grep -c 'base-binding-sweep'` → 0 (no capability row);
  - `git ls-tree -r --name-only 8374754b… -- .ufo/waves |
    grep -c 'records/basesweep-'` → 0 (no receipts);
  - the gap itself, on the record:
    `git show 8374754b…:tools/round-60/annotation-sweep.py |
    grep -c 'base-rev'` → 0 (the standing sweep never threads it — its
    limits line says so, quoted above).
  All pasted in `scores/c1-before.txt` at the freeze.
- AFTER, at the round tip:
  - the instrument exists, is registered (SKILL row, 7 cells, pipe-free,
    anchored on the `/instrument-registry` marker; SCORECARD capability
    row, first-working round 62), and is pinned in the claims container;
  - `python -X utf8 -I -B tools/round-62/base-binding-sweep.py --selftest`
    → `cases 50, failures []`, exit 0;
  - the first threaded inventory over the whole wave corpus at the base
    rev: 241 receipts enumerated, 0 invocation errors; **29 receipts are
    base-threaded from their own bytes** (each binding resolving to a real
    commit); **5 base-annotation instances threaded, 4 of them
    grammar-matched probe instances the gate base-re-derives — the first
    time any instrument checks them** (the r60 sweep semantics checked 0);
    0 base-class findings (all four base re-derivations agree — the
    corpus's one annotated+bound receipt, the r58 c1-after, is internally
    true at its own bound base); the standing 5 finding keys are UNCHANGED
    (threading adds checks that pass; filed defects persist);
  - `--no-base-thread` equivalence: same 5 keys, 0 threaded, 0 base probes;
  - green with the STANDING round-60 disposition TSV unchanged: exit 0
    (5 findings, all dispositioned — no new keys, nothing planted);
  - pin fail-closed: a wrong `--expect-sha256` → exit 2, no audit run.
  All pasted in `records/basesweep-*.txt` at the freeze; the after-arm at
  the record rev lands with the close (the disclosed r59/r60/r61 ordering).

**Why a do-nothing control cannot reach it:** the correction of the record
gap requires a new instrument (the r60/r61 rejects forbid extending the
frozen gate in place), its registration rows, and a run that threads base
context no instrument has ever threaded — at the base every probe above is
red/absent. The round's receipts avoid the r59 annotation grammar and the
r61 edge grammar entirely (as in r61), so the standing findings set stays
exactly 5; any new finding would be hand-verified then dispositioned
append-only before the landing (the r60/r61 pattern).

**Lowest-axis rule:** all three owned axes are tied at 10.0 (SCORECARD
`## Owned axes`), so the depth claim is a lowest-axis claim. Stagnation
nudge not fired: capabilities entered in r60 and r61 (window N=10; this is
round 2/10 of the current window). **No wave** (no dispatch surface on
this host; the kaidoku round-53 L0 question stays open and routed around).

## Frozen paths (the QUALITY #87 discipline: every clause the instruments implement)

- `.ufo/waves/round-62/claims.json` (the container; the freeze commit is
  the one that first adds it);
- `tools/round-62/base-binding-sweep.py` (sha256-pinned in the container);
- the receipts named above (before-arms land with the freeze; after-arms
  with the close at the record rev, the disclosed ordering).

## Duty receipts expected at the freeze (the r61 pattern)

`census-start.txt` (host-adapted census, exit 0, 19 standing W04);
`records/receipt-audit-sweep.txt` (the r56 gate over the NINE containers
r53–r61 — round-61's container enters for the first time);
`records/duty-finding-dispositions.txt` (the standing bare-name findings
dispositioned before any landing — standing disclosed named debt, no copy
planted); `records/record-audit-r61.txt` (the r57 gate over the r61 record
section); `records/orphan-census.txt` (two directions);
`scores/freshstart-spotcheck.txt`; `s262/` (snapshot + digests).
The standing halfway sweep (the r60 instrument, frozen pin
`38614088…`) re-runs at the record rev and lands with the close; the
registry-drift census (census3, `a7538e5f…`) re-runs `--generate` at the
landing rev / `--check` at the record rev after the new registry row lands
(the M58-2 rule); the R29 freeze-gate runs pre-flight at the freeze
(receipt with the record) and again at the record rev with the ledger row
present (receipt with the close).

## Pre-commit dry run (QUALITY #83/#84 adapted to the compose seam)

The full sweep was dry-run end-to-end against the base rev BEFORE this
commit, on the exact bytes being committed here: the first dry run caught
a real contract defect (the sweep's 4-argument audit_fn called the gate
runner with its 5-parameter signature, so unthreaded receipts passed
`None` into the tool argv cell — a crash on the first unthreaded receipt,
selftest-invisible because the injected fakes shared the wrong shape).
Fixed before any commit; the seam now has a dedicated selftest case
(the production closure shape wired through `sweep()`); mined as M62-1.

## Correction (appended at the freeze, naming the superseded text — the plans bullet above stays as filed)

The BEFORE bullet's probe "`git show 8374754b…:tools/round-60/annotation-sweep.py | grep -c 'base-rev'` → 0" predicted **0**; the observed output at the base is **1** — the token occurs exactly once, in the r60 limits line that *documents* the gap ("`--base-rev` re-derivation is not swept…"). The claim never rested on that count; the precise statement of the gap is the argv-token probe — `grep -c '"--base-rev"'` → 0 (the r60 sweep's checker argv never carries the option) — which is what `scores/c1-before.txt` pastes, with the draft note preserving the first-draft outputs (the M61-1/M60-3 discipline applied to this round's own draft; mined as M62-2).
