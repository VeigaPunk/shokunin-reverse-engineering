# kaidoku round 60 — claims (the halfway receipt-corpus sweep: the multi-receipt annotation-consistency instrument)

Round base `48c418305b71ea603e58f4fe9bd0dfbf2aafa9e4` (lane `main` tip at round
start, pushed = origin/main; the round-59 verifier spot-check commit, which
admitted r59 with no new routed defects and four status-neutral notes). The
carry-in repair landed at `ec9d93d7dcf72ba2aff88b3d72a3e39910bbc820` BEFORE
this declaration (the orphaned r59 selfcatch receipt, byte-identical landing
+ provenance, the r58-R2 pattern; disclosed in LOG). This file is the round
declaration; the **freeze** is the single commit that first adds the round-60
wave artifacts (census-start receipt, before-arm, sweep receipts, duty
receipts, the S260 snapshot) and the claims container
`.ufo/waves/round-60/claims.json`, recorded in `LOG.md` and
`.ufo/waves/round-60/l1/FREEZE` before any claim data lands. One new
instrument is introduced: `tools/round-60/annotation-sweep.py` (the r59
planned candidate: a multi-receipt sweep mode needs a new instrument and its
own freeze), committed BEFORE this claims file per QUALITY #33 and pinned in
the container. L1-inline round: no wave surface exists on this host (the
kaidoku round-53 L0 question stays open and unanswered; routed around, never
treated as answered).

## Claims

- **R60-C1 — depth, capability acquisition (the halfway receipt-corpus
  audit).** `tools/round-60/annotation-sweep.py`: enumerate every committed
  receipt under `.ufo/waves/round-N/l1/(scores|records)/` at ONE revision
  (188 at the base), run the FROZEN single-receipt gate
  `tools/round-59/annotation-audit.py` (pin `ba9ccbb9…`, worktree bytes
  hashed before every run, `--expect-sha256` mismatch is exit 2) on each via
  `subprocess.run`'s argv form (no shell), and require every named finding
  to be covered exactly by a committed disposition TSV — a missing key or an
  orphan key is exit 1; zero receipts or any invocation error is exit 2,
  never vacuously clean (the QUALITY #66 boundary). Demonstrated on the
  committed base: red with no dispositions → exit 1, the first complete
  inventory, 5 findings across 2 receipts (2 green, 184 unevaluable,
  0 invocation errors); green with the disposition table → exit 0 (5
  findings all dispositioned); red with one disposition row removed → exit 1
  naming the uncovered key; selftest 28 cases 0 failures. Registration:
  SKILL registry row (seven cells, pipe-free), SCORECARD capability row,
  census3 drift census re-run (the M58-2 rule). A do-nothing control cannot
  reach it: the instrument, its registry and capability rows, the inventory
  and the disposition table are absent at the base (`scores/c1-before.txt`).
  The same claim operates the round's orphaned-evidence duty and
  dispositions everything it names (below). Claims: one this round — the
  sweep's dispositions ARE its green condition, so a separate
  disposition-claim would not be causally separable, and one genuine
  verified claim beats an inflated pair.

## Fresh-start compliance (operator rule)

The rendered prompt §7 binds this round as a fresh-start round and lists the
last three rejected closures: r50, r51, r52 (all `rejected-honest-stop`). All
three fleet reports were re-read before declaring, and spot-checked against
the lane record (probes run this round, outputs pasted in the round report):

1. r50: `.ufo/waves/round-50/l1/scores/c1-after-attempt2.json` at HEAD
   carries `carriers_matched 2`, `target 4`, `met_target false`,
   `exit_code 1` — the attempt-2 C1 miss as filed (the JSON key is
   `exit_code`; the r59 closure's precision note applied).
2. r51: `python -X utf8 -I -B tools/round-51/census3.py --root . --rev
   f04b51ddb8d5fedb234a5e40a2c38b016f07a4ab --historical` → exit 1, registry
   55 / census 42 / outside 13 — exactly the r51 report's diagnostic numbers.
3. r52: `00d0bfd00b2778c3e0b22b7d0f6ade11abcb07a2` is an ancestor of
   `refs/heads/main` (merge-base rc=0) and carries
   `plans/round-52-claims.md` (cat-file rc=0).

Ruled out this round, with reasons:

1. **AVM LE-SquashFS Frontier→Core (the r50/r51/r52 twin claim).** The
   measurably-absent host surfaces are unchanged (PROVINCE `## Host
   migration — 2026-10-31`); three consecutive rounds died on it; the routed
   findings stay routed, untouched.
2. **New wave-based claims of any kind.** No dispatch surface on this host
   (the r53 L0 question stays open and unanswered); r51/r52's wave
   accounting was itself a rejection ground.
3. **Resuming the r51/r52 triage-v6 executability drafts.** Twice rejected
   as incomplete-instrument claims; the drafts stay wave evidence, not
   production instruments.
4. **Amending any frozen container, instrument, or filed receipt.** The r58
   sweep-finding flip condition stays on record with the r59 non-author
   closure's not-firing ruling; the r53 container's receipts_checked-0 shape
   stays disclosed verbatim (r59 reject 3); a correction never edits filed
   bytes — this round's only landing into historical scope is the r59
   selfcatch receipt that existed only in the worktree, landed
   byte-identically in the disclosed carry-in commit `ec9d93d7`.

## Sourced claim

**S260** (Python `subprocess` module documentation,
https://docs.python.org/3/library/subprocess.html, opened this round, snapshot
bytes + sha256 at `.ufo/waves/round-60/l1/s260/`) grounds R60-C1's
composition: the sweep drives the frozen gate through `subprocess.run`'s argv
form — the documented recommended helper ("The recommended approach to
invoking subprocesses is to use the run() function for all use cases it can
handle.", 19 words, section heading `Using the subprocess Module`, labelled
**composite** per QUALITY #42: the words `run()` sit inside an inline literal
span between plain-text words in the served HTML) — so the checker's bytes
execute exactly as the standing r59 demos ran them, with no shell
interpretation between the sweep and the pinned tool. The row lands with the
record commit, used-by targets in the same commit (the M53-4 rule).

## The duty's findings, named before any disposition lands

1. **The sweep's first inventory (red run at the base, exit 1) names 5
   findings across 2 receipts** (`.ufo/waves/round-58/l1/scores/c1-after.txt`
   and `.ufo/waves/round-59/l1/scores/c1-after.txt`): the persistent D58-1
   pair at r58 line 6 (disclosed in the same file's appended r59 correction
   block, `records/annotation-persistent-finding.txt`, and re-derived
   independently by the r59 non-author spot-check §2 R1); the M59-3
   prose-mimicry pair at r58 lines 21/25 (the receipt's own quoted-shape
   disclosure line read as an annotation by the frozen grammar); and ONE
   finding named for the FIRST time — r59 c1-after.txt:37
   COMMAND_UNREEXECUTABLE (the r59 after-arm landed at the r59 close, after
   the r59 demos). The new finding is hand re-verified BEFORE its
   disposition row was written (`records/sweep-first-inventory.txt`: pasted
   output 1 = record 1; the exact bound command re-runs to 1 at the rev it
   names) — the finding is the frozen gate's documented fail-closed grammar
   boundary, not a contradiction. Dispositions:
   `records/sweep-dispositions.tsv` (5 rows, each citing its standing
   disclosure or the fresh re-verification).
2. **The receipt-audit sweep over the SEVEN host-era containers r53–r59 at
   the base** (`records/receipt-audit-sweep.txt`): six clean + the r58
   container's quoted bare name (`RECEIPT_ABSENT freeze-gate-tip-90f3a9b9.json`
   in round-58 scope) — the standing disclosed finding; the bytes exist under
   round-55 and round-54; the r59 non-author closure ruled the flip condition
   does NOT fire; disclosed named debt, no copy planted.
3. **The record-audit over the r59 record section at the base**
   (`records/record-audit-r59.txt`): named 21, missing 0, clean.
4. **The two-direction orphan census** (`records/orphan-census.txt`):
   direction 1 at the base named FIVE worktree-only paths outside round-60 —
   the live discovery being `.ufo/waves/round-59/l1/records/annotation-selfcatch.txt`
   (on disk since r59, never committed; cat-file rc 128 at the base), which
   the carry-in commit `ec9d93d7` lands byte-identically with provenance
   (sha256 `175ef241…`); the r55 first-chain orphan stays retained-and-
   disclosed (r58 reject 1); two gitignored `.pyc` caches; and this round's
   own instrument, which the declaration commit lands. Direction 2: the
   50 committed-not-on-disk paths are exactly the PROVINCE-documented
   `EX-08/aux/` reserved-name class (the host checkout boundary, disclosed
   since r53).

## §9 sizing (do-nothing controls)

The before-arm is committed at the freeze: `scores/c1-before.txt` (the sweep
instrument absent at the base rc=128, 0 SKILL registry rows, 0 SCORECARD
capability rows, 188 receipts enumerated at the base with 0 complete
inventories). A round that did nothing would leave that arm exactly as
measured; the green arm (inventory complete, 5 findings all dispositioned)
is unreachable without the instrument, the table, and the registration.

## Commit order (the r56/r57/r58/r59 shape)

1. carry-in: `ec9d93d7` (landed before this file; its provenance-receipt
   fixup `691460fa` is disclosed one commit later).
2. declaration: plans (this file) + `tools/round-60/annotation-sweep.py`
   (the instrument, before the claims file) + LOG declaration entry.
3. freeze: claims container + FREEZE + census-start + the before-arm + the
   sweep receipts (selftest, red-nodispo, green, red-missing-key,
   dispositions TSV, first-inventory) + duty receipts (receipt-audit sweep,
   record-audit, orphan census) + s260/ + LOG freeze entry.
4. landing: the SKILL registry row + the SCORECARD capability row + LOG
   landing entry.
5. record: SCORECARD round-60 section + lesson + SOURCES S260 + ledger row +
   gate pre-flight receipt (run at the freeze) + census generate receipt +
   LOG record entry.
6. close: after-arms + census check receipt + gate landing receipt +
   census-end + LOG close entry.

No amendments after the freeze. Every helper call passes repo-relative
forward-slash paths (M58-1's rule), and every commit is diff-tree verified
against its intended path list immediately after landing (the M55-4 rule).
