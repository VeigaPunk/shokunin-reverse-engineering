# ReviewerScore — review of the drafted `## Round 48` + `## Record corrections — round 48` vs R48-C2

Method: read `tools/round-48/record2.py` + `tools/round-47/record.py` (the oracle) line by
line, then scored candidate and sibling drafts inside a full fixture clone
(`/fast/scratch/hyaku/kaidoku-r48/ReviewerScore/lane-fixture`, `git clone file://` of the
lane at `663f30ee`, wave evidence + receipts committed on top). Fixture history:
`db4f58ad` wave evidence → `59fb22df` pre-card c2 receipt → `96e57833`/`5d4776ae` card
drafts. Receipts copied to `.ufo/waves/round-48/w1/ReviewerScore/receipts/`.

## Verdict up front

**The drafts can satisfy clauses 1–5 (verified green in the fixture) but clause 6 is
unmeetable as frozen: the battery scores `v3_green 3 != 0` on every possible landing.**
Three of the five forgeries are invisible to the v3 clause set *by construction*, two of
them regardless of any card text. R48-C2 cannot score green at the declared freeze. It
needs freeze amendment A5 (or a declared battery repair).

Measured: `battery {'forgeries_total': 5, 'v2_green': 5, 'v3_green': 3, 'genuine_green': 1, 'crash': 0}`
(receipt `c2-draft2-full.json`; genuine card = the draft at fixture rev `5d4776ae`).

### Battery defect B1 — `axes-score-cell-off` is invisible to clause 5 (v3_green always ≥ 1)

`record2.score(text, files, …)` calls `axis_scores(files)`, which reads
`files('SCORECARD.md')` — the **committed** card at `--rev`, not the mutated `text`.
Every other clause scores `text`; clause 5 alone re-derives from committed bytes. The
mutation decrements a score cell in the forged text (`| coverage | 9.72 → 9.0 | …`) and
v3 returns 0 with `axis_score_bad []`. Proven in fixture: mutated row shown + `score()`
exit 0. **No landing content can make this forgery red — `v3_green` is ≥ 1 on every
card. This alone makes clause 6 unsatisfiable.**

### Battery defect B2 — `axes-correction-forged` lands in a dead section (v3_green always ≥ 1)

The forgery appends `\n## Record corrections — round 48\n\n- corrects axes depth: 999/999…`
at end of file. `corrections_section(card)` does
`card.split(CORR_HEAD, 1)[1].split("\n## ", 1)[0]` — it reads only the text between the
**first** `## Record corrections — round 48` and the *next* `## ` heading. The real
corrections section (mandatory: clause 3 reds on zero re-derived lines) is always the
first occurrence, so the forged second section is never parsed, its `axes` correction
never re-derived. v3 exit 0 on the assembled card. **Unsatisfiable by any draft — the
clause that forces the real section to exist is the same clause that shadows the
forgery.**

### Battery defect B3 — `quote-off-by-one` mutates out-of-scope bytes (v3_green, landing-dependent)

`QUOTE.sub(…, count=1)` rewrites the **first** `(atoms|exempted|corrections|mismatches) N`
match in the *entire card*, but clause 4 only checks quotes inside the last two round
sections. At `663f30ee` the first match is `corrections 2` in the `## Owned axes`
calibration row (SCORECARD.md line 25 — `Owned axes` is before every `## Round` heading).
Earlier matches also exist in `## Round 25` (`mismatches 5`, line 3061), `## Round 28`
and `## Round 29` (`mismatches 0`, lines 3150/3188) — all outside scope. The forgery is
a no-op against every v3 clause: exit 0. A draft can only make this forgery visible if
**every** pre-scope `QUOTE` match in the card is neutralized (append-only makes that
impractical); honestly it needs the same A5 fix (scope the mutation to the last two
sections, or extend clause 4 to the whole card).

### What the two surviving forgeries show

`gold-tautology` and `seats-moved` **are** caught (v3 exits 1: claim-ids floor, seats
floor). Fixture receipts: `v3_failing` for each in `c2-draft2-full.json`. The battery is
half-alive — the kill rule will fire with `v3_green 3` on a correct landing.

## Freeze-ID hazard (the draft's single biggest correctness landmine)

The prompt declares freeze `dc73587a`. That commit is no longer usable: `freeze_state`
unions `touched`+`blob_changed` over `freeze..rev`, and every later amendment commit
touches the frozen paths. Measured at `663f30ee`:

- `--freeze dc73587a --rev ac02a79f` → **exit 2** `frozen_path_changed`
  (`plans/round-48-claims.md`, `tools/round-48/`, `tools/round-48/meanings.py`;
  receipt `c2-dc73-at-head.json`).
- Only `--freeze 0f06251b` (A4, the last amendment carrying a claims paragraph) is
  viable at `663f30ee` (receipt `c2-A4-at-663-nobat.json`, `frozen_path_changed []`).
  If more amendments land, the viable freeze slides to the newest one.
- Consequence for the draft: naming `dc73587a` as "the declared freeze" in the card is
  **false as a counting command** — any counter run with it exits 2, not 1. The draft
  must name the last amendment commit (`0f06251bf6a3a6964c715f67243d4df12e854258` today)
  and the counting command must use it. ScribeScore's draft does this correctly.

## Review of the sibling drafts (assembled per their own paste rules)

ScribeScore draft (`w1/ScribeScore/score.md` § `## Round 48`) + ScribeCorrections block
(`w1/ScribeCorrections/corrections.md`) scored on the fixture card at `5d4776ae`:

### F1 — STALE WINDOW, clause 1 fail (must fix)

Learning-trends line: "the corpus/PROVINCE window over `61b87d74..0f06251b` is empty".
The oracle derives `git log 61b87d74..0f06251b --` with **empty pathspec** (the text has
no `-- paths` after the pair) — that covers every commit in the range, which includes
the frozen-path commits A1–A4, so `empty False` → oracle mismatch, clause 1 red.
Proven: `derive()` returns `(False, {'window': '61b87d74..0f06251b', 'pathspec': [],
'empty': False})`. **Fix: name the expansion window base→measured-rev with an explicit
pathspec, e.g. `` `git log --name-status --format= 61b87d74..<MEAS> -- corpus/knowledge PROVINCE.md` is empty `` — and the window must be non-frozen paths so the
landing doesn't falsify itself.**

### F2 — SECTION ORDER, clause 3 fail if pasted per ScribeCorrections' own instruction

ScribeCorrections says paste the block AFTER the `## Round 48` section. But
ScribeScore's draft text **inline-mentions** `## Record corrections — round 48` inside a
table row (backticked) *before* the real heading. `corrections_section` splits at the
first literal occurrence — the inline mention wins, `body` ends at the real heading,
**zero lines parse** → `no re-derived line` + the `seats` floor fails + the `exempted 2`
fix never lands. Measured (variant A): 4 clause failures. With corrections before the
round section (variant B): only the F1 mismatch. **Fix: either place the corrections
block before `## Round 48` (house precedent: round-47 corrections precede `## Round 47`
at SCORECARD.md:3663), or strip the inline backticked mention from the claim table.**

### F3 — heading literal, silent pass-through (counter weakness, paste hazard)

If the section is pasted with the draft's literal `## \`## Round 48 — …\`` heading
(backticks included), `^## Round (\d+)` never matches it — the whole draft swallows into
the round-47 body and the counter still exits 0 (`sections: [round-46, round-47]`,
claim-ids `{R46-C1,R46-C2,R47-C1,R47-C2}` all 'unique'). A card with **no** `## Round 48`
heading scores green. This is a counter defect (positional `heads[-2:]`, no per-round
key) — and a paste hazard: the heading must start `## Round 48 ` bare.

### What the drafts get right (verified in fixture)

- Corrections grammar: `- corrects seats round-47: 1 wave, 75 seats total` re-derives
  `(1,75)` vs dispatch `[75]` ✓; `- corrects quote round-47: exempted 1` re-derives and
  heals `exempted 2` → `quotes_corrected` ✓ (variant B, exit 0 once F1 patched).
- Seat line `Waves: 75 + 0 = 75 seats.` satisfies `SEATS_SUM` vs `[75]` ✓
  (also `Wave 1: 75 seats; wave 2: 0 seats.` satisfies `SEATS_PAIR` — verified).
- Claim ids `R48-C1`/`R48-C2` only in the new section; `R46-CL7`/`R47-CL10` are safe
  (`\bR\d\d-C\d\b` needs a digit after `-C`) ✓.
- Path atoms cited are all committed or will be; `.ufo/waves/round-48/` was untracked at
  `663f30ee` (ScribeScore's own appendix caught this: path atoms + `dispatch_counts` need
  the wave evidence committed BEFORE the measured revision). The `.ufo/waves/round-N/`
  template token must not survive into the section (path atom `round-N` would mismatch).
- `exempted 1`/`exempted 2` tokens inside the correction bullet are safe (clause 4 scans
  round sections, not the corrections body). In-section they avoid `atoms|exempted|
  corrections|mismatches N` quoting entirely — good (see clause-4 notes).

## Clause-by-clause draft requirements (everything a wrong draft fails)

1. **Oracle (`evaluate_text` from `--rev` bytes)** — every atom must re-derive TRUE:
   - every `` `hex7-40` `` must `rev-parse` and be `merge-base --is-ancestor` of the
     measured rev (no `<FILL>`, no typos — my first draft had `f3a7af4c` → mismatch);
   - every `.ufo/waves/round-N/…` token must exist at rev (commit wave evidence first);
   - every `…is empty…` line is a window atom: no hex pair = unverifiable BUT exempted
     (see L1 hole below); a hex pair must actually yield an empty `git log` over its
     own `--`-separated pathspec (F1);
   - seat atoms derive from `w{i}-dispatch.json` `counts.spawn` (needs it committed);
   - axes atoms derive from `axis_pairs` — coverage 138/138, depth 24/24 pre-landing
     (25/25 once block 25 lands; the Owned-axes head must carry the post-landing
     fraction or the axes atom mismatches);
   - `missing_classes` requires ≥1 atom of each class overall: without the draft's seat
     line there are **zero** seats atoms anywhere → oracle red even with 0 mismatches.
2. **Floor** — per-section seats (atom or `seats round-N` correction), ≥1 path atom,
   ≥1 rev atom, ≥1 claim id; ids unique across the pair. `seats round-48` correction
   does NOT heal the round-47 floor (verified — needs `round-47` key).
3. **Corrections** — ≥1 re-derived line under the literal head; first-`## `-bounded
   section (F2); quote correction must state a value not already quoted and backed by
   the corrected round's own cited receipts.
4. **Quoted numbers** — `(atoms|exempted|corrections|mismatches) N` inside a round
   section binds to **top-level** receipt cells only: a `record2` receipt nests
   `atoms`/`exempted`/`mismatches` under `oracle`, so those three keys are unquoteable
   from it; only `corrections N` (and a raw oracle receipt's cells) quote safely.
   Receipts cited must exist at rev (parseable or not).
5. **Score cells** — `cell[0]` `a → b` vs first `n/d` in `cell[1:]`: keep `→ 10.0` with
   `138/138` and `25/25`.
6. **Battery** — unsatisfiable as frozen (B1/B2/B3 above): `v3_green 3` minimum.

## Latent counter defects found while fuzzing (route candidates)

- **L1: any `…is empty…` line lacking a hex pair is exempted by *any* window
  correction, no key bind** — `exempt()` returns True for `pair-None` atoms
  unconditionally; round-47's `window round-46` correction silently exempts a round-48
  `…<tip>…is empty` placeholder (proven: exit 0, `exempted` contains the round-48 atom).
  `<tip>`/placeholder windows are *admissible* to the oracle, not red.
- **L2: swallowed `## Round N` heading invisible** (F3 above) — sections are positional.
- **L3: `corrections_section` first-occurrence semantics** — an inline backticked
  mention of the head earlier in the card amputates the real section (F2). Same class
  the claims file routed as R47-CL5's ghost-atom family, now in the section parser.

## Receipts

`.ufo/waves/round-48/w1/ReviewerScore/receipts/`:
- `c2-dc73-at-head.json` — exit 2 `frozen_path_changed` for prompt-declared freeze.
- `c2-A2-at-head-nobat.json`, `c2-A4-at-663-nobat.json` — pre-landing baseline, exit 1
  (3 structural fails: round-47 seats floor, corrections absent, `exempted 2` unbacked).
- `c2-draft1-full.json` — my draft, oracle mismatches (typo'd hash, missing receipt).
- `c2-draft2-full.json` — all clauses green, battery `v3_green 3`.
- `card-B.md` — assembled scribe drafts (corrections-then-section) used for A/B runs.
Counter runs used `python3 -B tools/round-48/record2.py --root . --freeze 0f06251b
--rev <REV>` inside the fixture clone; no lane bytes written. Scratch
`/fast/scratch/hyaku/kaidoku-r48/ReviewerScore` removed after copying receipts.
No installs; read-only git on the lane (`log`, `show`, `status --porcelain`,
`clone file://` to scratch).
