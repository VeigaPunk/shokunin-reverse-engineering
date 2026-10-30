# ScribeEntryC1 — R52-C1 knowledge-entry draft (round 52, wave r52-w1)

**Verdict: settled.** The full text of the R52-C1 knowledge entry
`corpus/knowledge/2026-10-30-r52-avm-le-squashfs-core.md` is drafted at
`.ufo/waves/round-52/w1/ScribeEntryC1/entry.md` (the path the L1 copies at the
freeze). Every number in it carries its command, exit code, stdout sha256 and
UTC time; every unmeasured cell is a `<PLACEHOLDER — L1: …>` marker; nothing in
the draft asserts that the data run succeeded.

## What the draft contains

Provenance trio first (`source:` lines for S243/S244/S245/S249, S250, S251 and
S252, each with its scope narrowed; `verified-at: 2026-10-30`; `recheck:` the
claims' predicate command), then: the two-round miss history (round 50's
decided miss at `carriers_matched 2` exit 1 with both independent `g7581`
causes; round 51's honest stop with no instrument and no data run); the
device-accounting law and the per-class census (Cable 1, FRITZ!Box 13); the
branch ground (S250's reader-side branches and S252's kernel-side `CAP_MKNOD`
gate); the pre-freeze controls as a table of expected-vs-measured; the fresh
data-run placeholders with per-carrier receipt pointers; the promotion
statement **conditional on `carriers_matched == 4`**; and the honest width
statement (fifo/socket/block unexercised; reached-scope limit).

## The three most important findings

**1. All four R52 carrier pins are already in the counter's prior-pin set.**
`tools/round-50/carriers.json` is itself one of the frozen `PRIOR_CARRIER_TABLES`,
so `g7581`, `g7582`, `c6490` and `c6430` all report `IN_PRIOR` against the prior
tables (receipt `carrier-pins-in-prior-set`, exit 0, sha256 `40f522c2…`). A v2
counter that computes `carrier_fresh_ok` as "pin not in prior" without the
frozen `re_scored_pins` allow-list scores **0 of 4** on exactly the four
carriers the claim re-measures. The allow-list must be explicit, frozen and
receipt-visible — the claims' F1 says so, and this makes it load-bearing rather
than cosmetic.

**2. The wave-1 counter draft cannot run and lacks every clause the predicate
names.** `ExecCounterV2/c1-counter.py` fails to import (`NameError: name
'TARGET' is not defined`, exit 1); an AST scan shows `TARGET`, `IDS` and
`PROV_BASE` are read but never assigned; `law_shape_ok`, `census_rederived_ok`,
`depth_gap_recorded` and `re_scored_pins` are absent (0 occurrences each); the
`--gap-rule` / `--receipts` / `--provenance-base` / `--receipt-fresh-base` flags
the control driver pins (claims F2) are absent (0 occurrences each); and the
claim-label grammar is not widened — two sites still compare against
`'R50-C1'`, so the frozen rule with `"claim": "R52-C1"` is unparseable by the
counter that must score it (claims F10).

**3. The M1 mutant is green on the disposition check; only the rule-shape
clause can make it red.** Measured over the committed envelopes, the
all-thirteen whitelist scores **4 of 4** on the measured 13-row census (and 3 of
4 on the M2 14-row census). The law rule scores 4/4 on both; CTL-OLD (the
round-50 rule) scores 2/4 and reproduces the committed miss; M3 and M4 score
2/4; the junk rule scores 0/4. With no `law_shape_ok` in the draft counter, M1
would be green and the claims' kill rule would trip. The empty allowance is
also what makes the law fail closed: with a synthetic device gap injected into
the committed `g7581` envelope the law rule goes **red** ("not allowed for
'char-device' entry 'dev/led' (allowed [])"), which a merely-exempting rule
would not.

## Two landing actions the L1 must not miss

- **S252 must land** in `corpus/SOURCES.md` with `opened` 2026-10-30 and this
  entry's path in `used-by`. It is **absent** from the registry today, so the
  counter's `sourced` binding is unreachable. The L1's own draft row is at
  `.ufo/waves/round-52/l1/s252-row.md`; the fetched body (16,407 bytes, page
  sha256 `f867026f…`) is committed at `.ufo/waves/round-52/l1/mknod.2.html`.
- **S250's and S251's `used-by` cells must be amended** to name this entry.
  Both are opened 2026-10-30 (inside the counter's window) but currently name
  only the round-51 entry; without the amendment the entry's citations of them
  are unbacked by the registry's own bookkeeping. S243/S244/S245/S249 are opened
  2026-10-28 and fall outside the window — they stay correct citations, but the
  binding does not rest on them.

## Gate / honesty notes

- The entry asserts the promotion **only conditionally** on
  `carriers_matched == 4`; the fresh-run table's every non-frozen column is a
  placeholder; the "What was NOT examined" section is scoped to what the L1's
  data run will cover.
- The width statement is honest against its own sources: the law is measured
  for **char-device rows only (28 of 28)**; no block-device, fifo or socket row
  exists in any of the four carriers; and S250 + S252 make the generalisation
  **weaker**, not stronger — the FIFO and socket `mknod` calls sit outside the
  reader's root test and `mknod(2)` permits unprivileged FIFO and UNIX-domain
  socket creation, so the `CAP_MKNOD` reason does not transfer to those kinds.
  The rule's treatment of them is a rule-shape choice, stated as such.
- The draft-time numbers are measurements of the **round-50 bytes under
  round-52-shaped rules**, computed with the round-50 counter's own
  `gap_rule_model` / `disposition_check`. They are not the L1's control run, not
  a run of the frozen v2 counter, and not a carrier measurement. The entry says
  so in its own limits (limit 12).
- The reached-scope limit is carried: the `depth-limited` gap's `relative_path`
  is **null** and its `input_path` is the chunk extract root, so a device-only
  subtree never descended into cannot be distinguished from one reached and
  correctly producing no gap; the v2 counter's `depth_gap_recorded` clause is
  named as the place where the limit stays visible.

## Verification actually run

All read-only over committed lane bytes; no REA, no download, no vendor byte, no
lane write. 26 receipts (`.ufo/waves/round-52/w1/ScribeEntryC1/receipts.tsv`),
each with id, UTC, exit code, stdout sha256 and exact command; 25 exit 0, one
exit 1 (`counter-draft-import`, the draft counter's own import failure, which is
the finding, not a probe error). `entry-binding-check.py` exits 1 with
`VERDICT needs-l1-fill` — the draft's shape passes, and the two unresolved
items are the L1's to fill (the 10 `<PLACEHOLDER` markers and the `sourced`
binding above).

## Out of scope for this seat

No freeze, no commit, no push, no instrument landed, no `tools/round-52/` file
written, no data run, no REA invocation, no download, no corpus/SOURCES.md or
PROVINCE.md or SCORECARD.md edit. This seat drafts; the L1 lands.

## Artifacts

- `.ufo/waves/round-52/w1/ScribeEntryC1/entry.md` — the entry draft (the text to
  land at `corpus/knowledge/2026-10-30-r52-avm-le-squashfs-core.md`)
- `.ufo/waves/round-52/w1/ScribeEntryC1/entry-probes.py` — read-only probe over
  committed bytes (census, device dispositions, rule-scoped verdicts, fail-closed,
  SOURCES state)
- `.ufo/waves/round-52/w1/ScribeEntryC1/receipts-collect.py` — the receipt
  collector
- `.ufo/waves/round-52/w1/ScribeEntryC1/entry-binding-check.py` — the entry's
  shape / `sourced` / placeholder check
- `.ufo/waves/round-52/w1/ScribeEntryC1/receipts.tsv` — the 26-row ledger
- `.ufo/waves/round-52/w1/ScribeEntryC1/probes.stdout` — the probe's raw output
- `.ufo/waves/round-52/w1/ScribeEntryC1/entry-binding-check.stdout` — the shape /
  `sourced` / placeholder check output
- `.ufo/waves/round-52/w1/ScribeEntryC1/status.json` — the wave accounting file

Scratch `/fast/scratch/hyaku/kaidoku-r52/w1-ScribeEntryC1` was removed after the
receipts were copied into the seat directory.
