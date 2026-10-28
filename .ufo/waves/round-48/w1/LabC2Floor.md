# LabC2Floor — R48-C2 completeness-floor falsification

Seat: `LabC2Floor` (leaf, godspeed). Scope: `tools/round-48/record2.py` clause 2
(completeness floor, R47-CL10 C2 side) — falsifiable hypothesis: *"the floor can be
satisfied without a real record"*, plus whatever the battery exposes on a minimal
green card. Read-only on the lane; fixture repo in scratch only.

All receipts: `.ufo/waves/round-48/w1/LabC2Floor/receipts/` (each `*.env.json`
carries the exact command, exit, UTC, stdout sha256; the `*.stdout` file is the
verbatim receipt bytes).

## Verdict on the hypothesis: TRUE — and harmless by itself

Card A is the strictest stub the hypothesis allows: the last two `## Round N`
sections each carry **only** a claim id, one real `.ufo/waves/` path, one
resolvable rev, and a seat total — no window line, no receipt cite, no
corrections, no quotes.

```
== A-strict-floor-only: exit 1   (receipt sha efe03075…, tag A-strict-floor-only)
floor rows: round-47 {path 1, rev 1, seats 1, claims [R47-C1]}
            round-48 {path 1, rev 1, seats 1, claims [R48-C1, R48-C2]}
            → no floor clause failed
oracle sub-receipt: met_target false (window 0 atoms; corrections 0 < 2)
failing: ["the round-47 atom oracle does not accept the card (mismatches 0)",
          "no `## Record corrections — round 48` line re-derived"]
```

Card A2 removes even the seat total from round 48 and substitutes a single
correction line (`- corrects seats round-48: 1 waves, 3 seats total`):
`seats_via_correction: true`, floor still fully green (tag
`A2-seats-via-correction`).

**The floor is a pure presence check.** `atoms_by_class` counts `collect()` hits
before `derive()` runs; a false seats line counts exactly like a true one. Truth
is delegated: the oracle clause binds every atom's value, the corrections clause
re-derives every correction, the quote clause binds quoted numbers to cited
receipts, the axes clause binds score cells to fractions.

**Floor's unique bite (measured, not inferred):** card B = oracle-green card
(`met_target true`, 10/10 atoms verified) with claim ids removed → exit 1,
failing = *only* `round-47: names no claim id` and `round-48: names no claim id`
(tag `B-oracle-green-floor-red`). That is the whole of the floor's independent
contribution: claim-id presence + uniqueness + per-section seats/path/rev
granularity (the oracle only requires classes *globally*).

**Residual gap** (what a floor-green stub still owes): a `window` atom (oracle
requires the class globally), ≥2 parseable `## Record corrections — round 47`
lines, ≥1 re-deriving `## Record corrections — round 48` line, all cited
receipts existing at rev, Owned-axes rows deriving coverage+depth pairs with the
score cell = `round(10·n/d, 2)`.

Card C/C2 adds exactly those items and reaches **exit 0 with `--no-battery`**
(tags `C-minimal-green-nobattery`, `C2-minimal-green-nobattery`) — i.e. the whole
v3 contract is satisfiable by a stub card. Minimal, honest, green.

## BLOCKING: the frozen battery has two unconditional v3-survivors

On the minimal-green card the battery reports
`{forgeries_total 5, v2_green 4, v3_green 2, genuine_green 1, crash 0}` →
`battery v3_green 2 != 0` → **R48-C2 can never exit 0 at any landing**
(tag `C2-minimal-green-withbattery`). Both survivors are defects of frozen code,
independent of card contents:

1. **`axes-score-cell-off` — counter defect.** `score()` calls
   `axis_scores(files)` where `files(p) = gate.show(root, rev, p)` — the
   *committed* SCORECARD, not the mutated `text`. The clause scores the genuine
   card, so the mutation is invisible and v3 exits 0 on every green card.
   Repro: `record2._m_axes_cell_off(CARD,ctx)` then `score(text,files,…,"v3")` →
   exit 0, `failing []` (tag `CF` family; hand-run line in driver output).
2. **`axes-correction-forged` — mutation defect.** `_m_axes_correction_forged`
   appends `\n## Record corrections — round 48\n\n- corrects axes depth: 999/999…`
   to the card. `corrections_section()` splits on the *first* head and truncates
   at the next `\n## ` — so on every card that already carries the (mandatory)
   section, the forged line lands in a dead duplicate and is never parsed.
   Hand-applied to card C and scored v3: **exit 0, failing []**
   (tag `CF-axes-forgery-on-landed-card`).

Both defects exist at the declared freeze bytes (sha of the frozen file under
`tools/round-48/record2.py` at `ac02a79f`). Consequence for the L1: **do not
land — the frozen kill rule makes the claim unsatisfiable**; this needs an
amendment A3 (score the text under test in `axis_scores`; inject the forged
correction into the live first section or parse all duplicate heads), in the
same disclosed-amendment style as A1/A2, declared before claim data. The
green-path clauses themselves are otherwise sound: `seats-moved` fails v3 on
`round-48: no seat atom…`, `quote-off-by-one` fails v3 on `quoted numbers with
no backing receipt: 1`, `gold-tautology` fails v3 (oracle + claim ids + quote
correction all red).

Note (fixture artifact, not a lane defect): `v2_green 4 != 5` because
`gold-tautology` embeds the lane commit `1e32827b`, unresolvable in my fixture;
on the lane it resolves and this forgery is v2-green as designed.

## Lane baseline at the operative freeze

- `python3 tools/round-48/record2.py --root . --freeze ac02a79f… --rev ac02a79f…
  --profile v3 --no-battery` → **exit 1** (tag `lane-v3-at-A2-freeze`):
  `round-47: no seat atom and no re-derived seats correction`,
  `no ## Record corrections — round 48 line re-derived`,
  `quoted numbers with no backing receipt: 1`. Oracle `met_target true` on the
  last two sections (round-46, round-47): the card is consistent; the floor and
  corrections machinery are the new work. This is exactly the red the landing
  requirement describes (a re-derived `seats` correction for round 47, a
  `quote` correction for round 47's `exempted` cell).
- Same args, `--profile v2` → **exit 0** (tag `lane-v2-at-A2-freeze`): the
  ported profile accepts the current card — the hole being closed.
- `--freeze dc73587a… --rev ac02a79f…` → **exit 2 `frozen_path_changed`**
  (`plans/round-48-claims.md`, `tools/round-48/`, `tools/round-48/meanings.py`)
  (tag `lane-v3-prompt-freeze-stale`). **The prompt's declared freeze
  `dc73587a` is stale**: amendment A2 inside the claims file re-declares the
  freeze as "the commit that carries this paragraph" = `ac02a79f`, which is also
  what `git log --format=%H -1 -- plans/round-48-claims.md` re-derives. Every
  seat should measure against `ac02a79f`.

## Method / limits

Fixture: `git init` in `$S/fix1`, F-commit = byte-copies of
`plans/round-48-claims.md` + `tools/round-48/` (frozen set, verified unchanged
F..rev by `freeze_state`), rev commits add `tools/round-47/record.py` (the
oracle, executed by the counter from committed bytes) and minimal support files
(`corpus/knowledge/2026-10-28-x.md`, `corpus/README.md` coverage map, `SKILL.md`
one resolving craft rule, `tools/x.py`, dispatch JSONs, one receipt JSON). Every
git call named `-C $D`; `rev-parse --show-toplevel` asserted before first
commit. Counter executed unmodified from the lane worktree (read-only);
mutations applied in-memory via the counter's own `MUTATIONS` where noted.
Not run: `meanings.py` (C1 counter — sibling scope), full battery against the
real lane card (battery is skipped until a green landing exists, which the
survivors above block).

## Receipt inventory (under `receipts/`)

| tag | exit | sha256 (stdout) | what |
|---|---|---|---|
| A-strict-floor-only | 1 | efe030751cc1e0ab… | hypothesis card, floor all-green, exit 1 |
| A2-seats-via-correction | 1 | 28a6c7f844f6d443… | seats leg via correction line only |
| B-oracle-green-floor-red | 1 | ea9ece70f311c668… | oracle-green, floor bites only claim ids |
| C-minimal-green-nobattery | 0 | 0abfb9c90650c964… | minimal stub reaches v3 green |
| C-minimal-green-withbattery | 1 | 82a335b0874f0eff… | battery v2 3 / v3 2 |
| C2-minimal-green-nobattery | 0 | 67a5fa48076962c2… | same, realistic layout |
| C2-minimal-green-withbattery | 1 | 1ed93c1651ec6f70… | battery v2 4 / v3 2 — two survivors |
| CF-axes-forgery-on-landed-card | 0 | hand-applied | forged axes correction survives v3 |
| lane-v3-at-A2-freeze | 1 | 45282c9bbee50ffc… | lane baseline, true freeze |
| lane-v2-at-A2-freeze | 0 | 79834524bcf7419f… | ported profile green on the hole |
| lane-v3-prompt-freeze-stale | 2 | 2353e4ac63b2ac70… | frozen_path_changed on stale freeze |

Tooling: nothing installed; `python3 3.14.8` + `git` only.
