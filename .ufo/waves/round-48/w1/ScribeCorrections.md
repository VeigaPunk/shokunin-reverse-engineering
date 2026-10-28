# ScribeCorrections — `## Record corrections — round 48` draft + verification (R48-C2 lane)

Round-48 w1 seat. Deliverable: `.ufo/waves/round-48/w1/ScribeCorrections/corrections.md` —
the two correction lines, verified against the frozen instruments' own derivation paths.

## Behavior (what was done)

Drafted and machine-verified two `- corrects` lines for `SCORECARD.md`:

1. `seats` correction for round 47: `1 wave, 75 seats total` — round-47's section names no
   seat total; `.ufo/waves/round-47/w1-dispatch.json` (the only dispatch file) reports
   `counts.spawn 75`. Re-derives `(1, 75)` through the oracle's `dispatch_counts`/`corrects`
   and satisfies `record2`'s completeness floor (`seats_via_correction` for round-47).
2. `quote` correction for round 47's `exempted` cell: `exempted 1` — the section quotes
   `exempted 2`; the cited receipt `.ufo/waves/round-47/l1/scores/c2-at-A7.json` carries
   `exempted` as a **list of one atom** (the exempted window atom `key 46`), so
   `quote_value = len = 1`. `_quote_correction` accepts (value not already quoted, backed by
   a cited receipt), and clause 4 then binds the stale quote →
   `quotes_corrected [{round-47, "exempted 2" → 1}]`.

Both lines are single-line bullets under `## Record corrections — round 48`; paste block and
mandatory placement rules are in `corrections.md`.

## Gates exercised (commands, exit codes, evidence)

All runs read-only on the lane (`git show/rev-parse/merge-base/log` inside the counters).

| command | exit | output sha256 |
|---|---|---|
| `python3 -I -B verify.py` (scratch, rev=HEAD=`663f30ee`) — checks A–E below | 0 | `fb69e8db…10afdc` (`receipts/verify-out.json`) |
| `python3 -I -B tools/round-48/record2.py --root <lane> --freeze 0f06251bf6a3a6964c715f67243d4df12e854258 --rev HEAD` (do-nothing reproduction) | 1 | `263d46ba…9de44e` (`receipts/cli-donothing.json`) |
| placement probe (F) + round-47 quote inventory (G) | — | `5cee0ec2…a09a5e` (`receipts/probe-placement.json`) |

- **A (before)**: `score()` on the committed card → exit 1, failing
  `round-47: no seat atom and no re-derived seats correction`;
  `no Record corrections — round 48 line re-derived`;
  `quoted numbers with no backing receipt: 1` (`exempted 2`, receipts c1/c2-at-A7).
  The real CLI run reproduces all three at declared freeze `0f06251b`.
- **B (candidate)**: card + block → exit 0, `corrections 2`, `corrections_bad []`,
  `quotes_bad []`, `quotes_corrected` as above, `quotes_checked 3`,
  round-47 floor `seats_via_correction true`.
- **C (forged quote)**: a correction stating `exempted 2` → rejected
  (`the section already quotes that value`; `backed false` — `c1-at-A7.json` has no
  `exempted` cell, `c2-at-A7.json`'s is 1).
- **D (forged seats)**: `2 waves, 75` / `1 wave, 74` / `1 wave, 76` all rejected against
  derived `(1, 75)`; `75 seats` rejected on grammar.
- **E (post-landing sim)**: card + minimal `## Round 48` section + block → exit 0, sections
  `[round-47, round-48]`, both corrections re-derive with round-47 still in scope.
  (Sim overlays the uncommitted `.ufo/waves/round-48/` dispatch + control files the landing
  will commit.)

## Findings for the L1 / attack surface

1. **Placement is load-bearing (measured).** Inserting the corrections heading inside the
   `## Round 47` body truncates the section at `\n## ` → `round-47: no path atom`,
   `no rev atom`, `names no claim id`, **and** the `quote` correction no longer re-derives
   (`no cited receipt states that value`, because the receipt citation lived in the truncated
   claims table). The block must be appended **after** a complete `## Round N` section —
   same convention as `## Record corrections — round 47` (sits between the Round-46 and
   Round-47 sections).
2. **`quote` binds the first `key N` token only.** `_quote_correction` uses
   `QUOTE.search`: `exempted 1` must be the first `atoms|exempted|corrections|mismatches N`
   token in the statement. Reordering the prose silently rebinds (verified: `exempted 2`
   first → rejected). Only the first match counts; later same-key numbers in prose are
   inert. This is a real footgun for landing edits.
3. **`seats` correction is invisible to the round-47 oracle.** The oracle's
   `## Record corrections — round 47` grammar parses only `seats|window|path|rev` inside its
   own section; round-48's section is a different `CORR_HEAD`, and `quote` isn't in the
   oracle's `CORR` alternation at all. The lines cannot disturb `atoms 42 / exempted 1 /
   mismatches []`.
4. **Two-receipt nuance.** The round-47 section cites `c1-at-A7.json` and `c2-at-A7.json`;
   only `c2` carries `exempted` (`c1` receipt has no such key → `quote_value None`).
   `backed` is an `any` over cited receipts, so the correction binds whichever receipt
   carries the key — the prose name in the statement is not itself checked.
5. **Freeze drift.** Prompt names `dc73587a` (A1); the file has since declared
   **A4 `0f06251b`** (`git log -1 -- plans/round-48-claims.md`). `record2.py` is
   byte-identical between `dc73587a` and `HEAD` (last touched at `dc73587a`), so the
   grammar verified here is the A4 grammar. Note `--rev HEAD` now resolves past the freeze
   (`663f30ee`, `f3a7afc`, `0d76deed` — `.ufo` receipt commits only); `freeze_state` is
   clean (`frozen_path_changed []`) for `--freeze 0f06251b`.
6. Head-of-file facts re-derived: `SCORECARD.md` unchanged between `f3a7afc` and `663f30ee`;
   `w1-dispatch.json` round-47 `{spawn:75, resume:0, total:75}` committed at HEAD;
   `w2-dispatch.json` absent → `(1, 75)`.

## Touched surfaces (written by this seat)

- `.ufo/waves/round-48/w1/ScribeCorrections/corrections.md` (the draft)
- `.ufo/waves/round-48/w1/ScribeCorrections/receipts/{verify.py,verify-out.json,cli-donothing.json,probe-placement.json,receipts-sha.txt}`
- this report

## Out of scope (left to other seats / L1)

- `## Round 48 — …` section content, `## Owned axes` head update, `SKILL.md` block 25,
  registry meaning repair (R48-C1 seats), the 5-forgery battery at landing rev, the actual
  append to `SCORECARD.md` (L1 only — read-only contract honored; nothing outside this seat
  dir was modified).
- Not run: battery (`record2` skips it while the card is red); `meanings.py` (C1).

## Known limits

- Verification rev is `HEAD` (`663f30ee`); the landing rev adds committed sections +
  receipts, but the correction derivation depends only on round-47 artifacts committed
  long ago, so the lines are rev-stable (E simulates exactly this).
- `dispatch_counts` tolerance: a future `w2-dispatch.json` for round 47 would change the
  derived tuple — impossible here (round closed, file absent at rev).

## Installations

None (no tool installs; pacman paused per RULES.md).
