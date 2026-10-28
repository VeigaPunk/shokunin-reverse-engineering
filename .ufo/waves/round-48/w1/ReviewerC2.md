# ReviewerC2 — surgical correctness review of `tools/round-48/record2.py`

Seat scope: `_round_sections` offsets after in-place mutation, `_split_corrections`
(`corrections_section`), `quote_value` on bools/lists, the `quote_fixes` path,
`axis_scores` cell indexing, and the oracle exec namespace — with the
five-forgery battery traced end-to-end.

**Headline: the R48-C2 kill rule is unsatisfiable by construction.** On a card
that passes every v3 clause (all six), three of the five frozen forgeries score
`v3_exit 0`. `evaluate()` can therefore never exit 0 at any landing revision:
`battery v3_green 3 != 0`. The instrument falsifies itself.

## 0. Operative freeze

The prompt's declared freeze `dc73587a` is **stale**. The claims file's own
re-derivation rule (`git log --format=%H -1 -- plans/round-48-claims.md`) yields
`0f06251b` — A4 carries a `## Freeze amendment A4` section (claims file
HEAD:160-201) that the prompt's copy lacks; amendments A3 (`f3a7afc4`) and A4
(`0f06251b`) both declare the freeze forward. Running with `--freeze dc73587a`
exits 2 `frozen_path_changed` (receipt below). All findings use `0f06251b`.
The reviewed `record2.py` is byte-identical at `dc73587a` and HEAD
(sha256 `eb7dc887fd285fce8710dc66ebd01712c364fedbac66ffaae957643be0038581`),
so every finding applies at either freeze.

## 1. Harness: genuine-green landing card (fixture)

The battery only runs when the card passes all v3 clauses, so the kills needed a
card that is green. Fixture: `git clone` of the lane at `663f30ee` into scratch +
two commits (`241110ec`, `acb1ed82`) adding `.ufo/waves/round-48/w1-dispatch.json`
(spawn 5), a `c2-at-landing.json` receipt, `## Record corrections — round 48`
(the two corrections the frozen landing requirement mandates: `seats round-47`,
`quote round-47`) and `## Round 48` (seat/window/path/rev/claim atoms).
Rebuild: `w1/ReviewerC2/rebuild-fixture.sh`.

Command (lane worktree, unmodified frozen bytes):
```
cd <LANE> && HYAKU_SCRATCH=<S> python3 -I -B tools/round-48/record2.py \
  --root <S>/fixture --freeze 0f06251bf6a3a6964c715f67243d4df12e854258 \
  --rev acb1ed829263585c0c10c4178a69b2fc563441e4
```
Exit 1. Receipt `w1/ReviewerC2/c2-simulated-landing.out.json`
(sha256 `ab623edbe6b3012065dc733078df9a904258759172f8ecd8aa36bed4c27c2f88`,
captured 2026-10-28T19:03Z):

- `failing` = `["battery v3_green 3 != 0"]` — the *only* failure; every clause
  (oracle, floor incl. `seats_via_correction`, corrections, quotes, axes cells,
  claim ids) is green; `genuine_green 1`, `v2_green 5`, `crash 0`.
- v3 exits per forgery: `gold-tautology` **1** (red, works), `seats-moved` **1**
  (red here — see §4 for its degenerate twin), `quote-off-by-one` **0**,
  `axes-score-cell-off` **0**, `axes-correction-forged` **0**.
- `--profile v2` on the same card: exit 0 (`c2-sim-landing-v2.out.json`,
  sha256 `4178f79c29b816d1a7c9d55b1b91bcbe8d3a0334bd7e9b5809c3483955e14656`).
- Stale freeze check: `--freeze dc73587a --rev acb1ed82 --no-battery` → exit 2,
  `reason frozen_path_changed` (`plans/round-48-claims.md`, `tools/round-48/`).

## 2. CRITICAL — the three unconditional forgery kills

### F-A `axes-score-cell-off` is invisible to clause 5 — `record2.py:304`
`score(card, files, …)` passes the mutated text as `card`, but clause 5 calls
`axis_scores(files)` and `axis_scores` (line 141) does `card = files(CARD)` — it
re-reads the **committed** SCORECARD.md, never the text under evaluation. In
`run_battery` (line 447) `files` reads bytes at `--rev`, so clause 5 measures the
genuine card while the mutation edits the forged one. The forgery designed to
test R47-CL2 can never fail: on any green card `axis_score_bad` is `[]` for every
mutation, `v3_exit 0`, `v3_green` ≥ 1. Measured: `v3_exit 0` in the receipt.

Reproducing input: any card whose `| coverage |` row carries `9.72 → 10.0` and
`138/138`; `_m_axes_cell_off` produces `9.72 → 9.0`, and clause 5 still sees
`score [9.72, 10.0]`.

### F-B `axes-correction-forged` lands outside every parsed section — `record2.py:101,416-419`
`corrections_section` does `card.split(CORR_HEAD, 1)[1].split("\n## ", 1)[0]`:
it takes text after the **first** `CORR_HEAD` occurrence, bounded at the next
`\n## `. The mutation appends a *second* `## Record corrections — round 48`
heading at EOF plus its forged `axes` line. The first section's body terminates
at that second `\n## `, so the forged line is unreachable by both parsers —
the oracle's own `corrections()` (record.py:246, same construction) and
record2's `corrections_section` (line 101). `corrs` is identical to the genuine
run; v3 exit 0. Unconditional for every card containing the heading — which the
landing requirement mandates — whether or not the section is last. Measured:
`v3_exit 0`.

Reproducing input: genuine card + `"\n## Record corrections — round 48\n\n
- corrects axes depth: 999/999 — …"` appended.

### F-C `quote-off-by-one` mutates text no clause inspects — `record2.py:396-397`
`_m_quote_off` is `QUOTE.sub(…, card, count=1)` — the **first `key N` match
card-wide**, not inside the last two round sections that clause 4 scans
(`for rnd, text in secs`, line 275). At the card's current layout the first match
is `corrections 2` at byte 5746, inside the `## Owned axes` **calibration** row
(line 25: `` `corrections 2`, `exempted 1 <= 3` ``) — a row `axis_scores`
skips (regex is `coverage|depth` only, line 48), `collect_axes` ignores, and the
oracle never parses. `corrections 2` → `corrections 3` is a real change that
nothing inspects: `v3_exit 0` (measured). Even if layout shifts the first match
into round-47's `exempted 2`, F-D's laundering still scores it green. The
forgery is red only in the narrow case where the first match is an in-scope
quote for a key with no `quote` correction.

Reproducing input: current card bytes; `_m_quote_off` edits offset 5746.

## 3. HIGH — the `quote_fixes` laundering hole (R47-CL13 re-opens)

`_quote_correction` (lines 159-177) plus the quote clause (lines 285-291) make
**every** number quoted under a corrected key pass: for a quoted `key val` where
`val` matches no cited receipt, acceptance needs only `int(val) != fixed[key]`
and a cited receipt stating `fixed[key]`. So once a `quote` correction exists
for `(round, key)`, any wrong value for that key in that section is "corrected".

End-to-end proof (P14): fixture card with `exempted 2 <= 3` → `exempted 99 <= 3`
in the round-47 section exits **0**, `quotes_corrected` shows
`{'quote': 'exempted 99', 'corrected': 1}`. The landing *requires* a `quote`
correction for round-47's `exempted` cell, so this hole is live at every landing.

Sub-defect (P2): `_quote_correction` binds the **first** `key N` match in the
statement (`QUOTE.search`, line 161). Statement `atoms 42 — also exempted 9`
binds `atoms/42`, not `exempted`; a correction intended for one key can
contribute `quote_fixes` for another (and `value` need only be receipt-backed
and un-quoted — no check that it shares the intended key).

Asymmetry: `quote` corrections are limited to rounds in `secs` (line 165-167 —
"no round-N section in scope"), while `seats`/`window` corrections for rounds
older than the window are valid via the oracle's `historical` rule. A `quote`
correction for round 45 fails `bad_corr` — inconsistent scope treatment.

## 4. HIGH — `seats-moved` verifies because an atom's round is its position

The moved atom re-derives for whichever section it lands in, because `collect`
assigns `key` from the enclosing section text, not from history: `Waves:
40 + 40 = 80 seats.` dropped into round-47's section verifies as a round-47 atom
(measured: `v2_exit 0` — v2 has no per-section floor, so a moved atom is
indistinguishable from a written one). On the mandated landing the forgery is
honest only because round-48 satisfies its seats floor with a *line*: the
mutation removes it and the floor goes red (`round-48: no seat atom`). The red
outcome is therefore **layout-dependent**, not forgery-essential:

- If round-48's floor is satisfied via a `seats` *correction* instead of a seats
  line (a landing the grammar permits), the mutation removes only a cosmetic
  line, every floor stays satisfied, and the forgery scores `v3_exit 0` — a
  fourth kill in that layout.
- If the removal plus re-insertion leaves the text byte-identical,
  `run_battery` lines 457-461 record `forgeries_total += 1` and
  `v2_green += 1` for a mutation that never ran — `v2_green 5` passes while
  that forgery class is unmeasured.

Related latent defect (`record.py:45,195-200`, shared grammar): `SEATS_SUM` can
only express `A + B = T`. For a round with ≥3 dispatch files,
`_m_seats_moved` writes `Waves: s0 + s1 = sum(all)` — displayed arithmetic that
is false (`5 + 3 = 10`) and still verifies, because the oracle binds the three
tokens positionally, not the arithmetic. Latent: no round currently has >2 waves
(dispatches at HEAD: ≤2 per round).

`_round_sections` itself is **correct**: mutations apply in `reversed()` document
order (line 353) so earlier spans stay valid; `_m_seats_moved` recomputes
`_round_sections(out)` after mutation (line 390) rather than reusing stale
offsets. No defect there.

## 5. HIGH — `corrections_section` substring parsing (`_split_corrections`)

- **First-occurrence capture** (line 99-101): `CORR_HEAD in card` + `split` is a
  *substring* test. A prose mention `see ## Record corrections — round 48` before
  the real heading, or a deeper `#### Record corrections — round 48` heading,
  captures the wrong offset: the real lines are never parsed → `corrs []` →
  `no '## Record corrections — round 48' line re-derived` false-red on a
  conforming card. Probe (P3): `corrections_section` returns `[]` for the
  prose-mention card; for the `####` variant it returns the line nested under
  the sub-heading and never the real section's lines.
- **Indented-line parsing** (line 104): `line.strip()` before `CORR.match`
  accepts `  - corrects …` — a line inside a fenced block or a nested list in
  the corrections section is parsed as a real correction. Probe (P3): an
  indented line parses.

## 6. MEDIUM — `axis_scores` is position- and layout-fragile (`record2.py:140-156`)

- `cell[0]` after `rest.split("|")` assumes the score cell immediately follows
  the axis name. A row `| coverage | 138/138 | 9.72 → 10.0 | ev |` (fraction
  first) yields `axis_scores {}` — clause 5 then scores **vacuous green over
  zero rows**, the same class of hole A1 was declared to fix. Probe (P5).
- Rows lacking a trailing `|` in the fraction cell (`len(cell) < 2`) are skipped
  silently — same vacuous green.
- `FRAC.search("|".join(cell[1:]))` binds the first `n/d` *anywhere* in the
  remaining cells; spec says "the first n/d fraction in that row" — a fraction
  embedded earlier in the evidence text wins the bind (false green/red by
  ordering).
- Independently of F-A: `axis_scores(files)` reads committed bytes, so in
  `evaluate()` clause 5 tests the card at `--rev` (correct) but in
  `run_battery` it tests nothing about the mutation (the kill).

## 7. MEDIUM — `quote_value` dtype gaps (`record2.py:127-137`)

`list → len`, `bool → None`, `int → int`, everything else → `None`. A receipt
carrying `"exempted": 1.0` (JSON float), `"atoms": "42"` (numeric string), or a
dict count can never back a quote and can never back a `quote` correction —
such receipts are un-evaluable for clause 4 while remaining cited (probe P1:
`5.0 → None`, `"2" → None`, `{"a":1} → None`, `[1,2,3] → 3`). List-length is
*intended* for `exempted`/`mismatches` list cells, and record2 relies on it for
the mandated round-47 `exempted 1` correction — but the same flattening makes a
list cell's *value* irrecoverable and a bool cell silently unevaluable rather
than reported.

## 8. MEDIUM — claim-id mentions counted as declarations (`record2.py:45,219,236-239`)

`CLAIM_ID.findall(text)` treats every `R\d\d-C\d` token in a section as a claim
id. A cross-reference `(extends R47-C1)` inside `## Round 48` makes
`claim_ids {'R47-C1': 2}` and fails `claim ids claimed by both sections`
(false-red, probe P12). Inversely a section that only *mentions* `R4x-Cy` in
prose satisfies the "names its claims" floor without declaring any claim
(false-green credit).

## 9. LOW — remaining defects

- `RECEIPT` (`record2.py:47`) is not end-anchored: a citation of
  `…/c2-at-A7.json.bak` binds `c2-at-A7.json` — a different file than cited
  (probe P4). Also receipts outside `l1/scores/` are invisible → false-red
  `cites no receipt that exists at rev`.
- `seats_via_correction` credits *presence* of a parseable `seats` correction,
  not a re-derived one (lines 212, 220): a `9 waves, 99 seats total` line still
  satisfies the floor seat atom while failing `corrections_bad` (probe P13 —
  the receipt floor row then contradicts the failing list; the claim text says
  "a **re-derived** seats correction").
- Oracle `exec` namespace (`record2.py:70-71`): `__file__` is set to the relative
  string `tools/round-47/record.py`, so `record.py`'s own
  `sys.path.insert(abspath(__file__)…)` lines push **cwd-dependent dead paths**
  into the host process (`<cwd>/tools/round-47/`, `<cwd>/tools/round-46/`) and
  they stay for the process lifetime (probe P6). Inert today only because
  `record2` already imported the real `gate` into `sys.modules` before the exec;
  from a cwd containing a `tools/round-47/gate.py` the import order still wins,
  but the namespace pollution and a later `import gate` in a re-exec'd module
  would silently bind the wrong module. `__name__` is `round47_record`, not a
  package — acceptable, but worth naming.
- `evaluate()` scores the card twice when the battery runs (lines 484, 489);
  deterministic, just wasted work.
- `run_battery` no-op branch (lines 457-461): a degenerate mutation counts as a
  `v2_green` forgery — battery totals can pass with a forgery class unexercised.
- `selftest` (lines 526-540) has no assertions — prints `corr_parse true` and
  exits 0 unconditionally.

## 10. Residual risk and verification gaps

- All three kills are conditional on *one* thing: the real landing card. My
  simulated card satisfies every v3 clause and mirrors the layout the frozen
  landing requirement describes (corrections section + round section appended,
  Owned-axes head unchanged). If the L1 lands a materially different card —
  e.g. rewrites the Owned-axes calibration row so the first `key N` match moves
  into round-47 — `quote-off-by-one` may turn red while `seats-moved` may turn
  green on a *pre*-landing variant (its degenerate mode in §4). The kills F-A
  and F-B are unconditional in all layouts that contain the mandatory
  corrections section; F-C/F-D hold in every realistic layout.
- Not run: any mutation of frozen bytes (contract-forbidden — all mutations ran
  on fixture copies); `meanings.py` / R48-C1 (other seats' scope); the real
  landing revision (does not exist yet). The lane's own `--selftest` was run:
  exit 0, assertion-free.
- `--json-out` note: `gate.out_path` requires the path inside `--root`; with
  `--root` a fixture, receipts land inside the fixture. Citeable evidence was
  captured via stdout redirect into `.ufo/waves/round-48/w1/ReviewerC2/`.

## 11. Receipts (all in `.ufo/waves/round-48/w1/ReviewerC2/`)

| file | sha256 | what |
|---|---|---|
| `c2-simulated-landing.out.json` | `ab623edbe6b3012065dc733078df9a904258759172f8ecd8aa36bed4c27c2f88` | full v3 run on simulated landing card: `failing = battery v3_green 3 != 0` |
| `c2-sim-landing-v2.out.json` | `4178f79c29b816d1a7c9d55b1b91bcbe8d3a0334bd7e9b5809c3483955e14656` | `--profile v2` same card: `met_target true` |
| `unit-probes.out.json` | `84bd8ca476a5b290eb137c2845d3bc7c5fae054bef68c8c993e7d770e1a1c40e` | P1/P2/P5/P6/P12/P13/P14/P15 probe values |
| `rebuild-fixture.sh` | — | fixture reproduction |

Fixture commits: `241110ecd715bc145cf52ae93c5466f843bb5a77` (card + .ufo files),
`acb1ed829263585c0c10c4178a69b2fc563441e4` (w1 dir for the path atom), on
`663f30ee` clone head. All runs `python3 -I -B`; UTC 2026-10-28T19:03–19:05Z.
No installs (nothing needed; pacman paused per RULES). Scratch
`/fast/scratch/hyaku/kaidoku-r48/ReviewerC2` removed after receipt capture.
