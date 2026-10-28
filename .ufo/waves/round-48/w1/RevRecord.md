# RevRecord — round-48 wave-1 (revenger seat, record-quote evidence)

Scope: reconstruct what `SCORECARD.md`'s last two `## Round N` sections (round 46,
SCORECARD.md:3599-3661; round 47, 3682-3726) claim numerically versus what the receipts
they cite actually say — the M47-9 (`record-misquotes-its-own-receipt`) class that
`record2.py`'s `quote` clause exists to close. Everything below was re-derived from
committed bytes at HEAD `ac02a79ff84133220d01ce3b59a4789b7004dbc5` (= `## Round 48` tip);
the worktree dirt in `.ufo/` does not touch any cited receipt (all 12 cited receipts are
byte-identical to their HEAD blobs, sha256-checked individually).

## 0. Freeze-identity divergence (prompt vs claims file)

- My prompt declares freeze `dc73587a8b9c1a23ba5a91dc7707ac7381a8b873` "(after disclosed
  amendment A1)". The claims file's own re-derivation
  (`git log --format=%H -1 -- plans/round-48-claims.md`) yields **`ac02a79f...`** — the A2
  commit — because amendment A2 (added by `ac02a79f`) edits the claims file itself and
  makes `ac02a79f` the declared freeze ("The declared freeze is the commit that carries
  this paragraph").
- Receipt: `record2.py --root . --freeze dc73587a… --rev ac02a79f…` exits **2**
  (`frozen_path_changed` — `tools/round-48/` differs between A1 and A2), i.e. the prompt's
  pin is unevaluable one commit late. See `RevRecord/record2-freezeA1-revA2.json`
  (stdout sha256 `2353e4ac…`, UTC 2026-10-28T18:49:41Z).
- All real evaluation used `--freeze ac02a79f… --rev ac02a79f…`. The L1 should note the
  prompt/freeze skew; the claims file is self-consistent.

## 1. Baseline: the frozen counter on the frozen card

`python3 -I -B tools/round-48/record2.py --root . --freeze ac02a79f… --rev ac02a79f…`
→ exit **1**, `failing`:

1. `round-47: no seat atom and no re-derived seats correction`
2. `no \`## Record corrections — round 48\` line re-derived`
3. `quoted numbers with no backing receipt: 1`

Receipt `RevRecord/record2-at-A2.json` (stdout sha256 `539f76ad…`):
`quotes_bad=[{round-47, "exempted 2", receipts=[c1-at-A7.json, c2-at-A7.json]}]`,
`quotes_checked=2`, `floor` round-46 `{path:4, rev:18, seats:1, window:1}` / round-47
`{path:4, rev:13, window:1}` — **round-47 has no `seats` atom at all**, oracle
`atoms 44` / `exempted len 1` / `mismatches []` / `met_target true`.
`--profile v2` on the same card exits **0** (RevRecord/record2-v2-at-A2.json) — the
ported-semantics hole is live exactly as the claims file says.

## 2. Every QUOTE-grammar number in the last two sections vs its receipts

Grammar: `\b(atoms|exempted|corrections|mismatches)\s+(\d+)\b` (record2.py:46), backed by
`\.ufo/waves/round-N/l1/scores/*.json` receipts cited in the same section (record2.py:47).

Round-46 section: **zero matches** — it quotes no record-counter keys. All four
numbers the grammar would bind are absent; nothing to falsify.

Round-47 section (SCORECARD.md:3703, R47-C2 after-cell), three matches, one cited
receipt pair `{c1,c2}-at-A7.json` (rev `a0753786`):

| quoted | card value | cited receipt cell | receipt value | verdict |
|---|---|---|---|---|
| `atoms 42` | 42 | `c2-at-A7.atoms` | 42 | backed |
| `corrections 2` | 2 | `c2-at-A7.corrections` | 2 | backed |
| **`exempted 2`** | 2 | `len(c2-at-A7.exempted)` | **1** | **DISAGREEMENT** |

## 3. THE disagreement — `exempted 2` is a franken-quote across measurement revisions

- `c2-at-A7.json` `exempted` is a **one-element list** (the round-46 `<tip>` window
  atom). `quote_value` counts list length → **1**. The card quotes **2**. This is the
  sole `quotes_bad` entry at the freeze and the exact R47-CL13/M47-9 hole.
- **Provenance (the interesting part):** `exempted 2` was *true* at the A4/L1
  measurement — `c2-at-A4.json` (rev `1e2c3102`) and `c2-at-L1.json` (rev `e856beb5`)
  both read `exempted len 2`, `atoms 50`. Commit `caafeffa` wrote the row with those
  A4 numbers (`atoms 50`, `exempted 2`, receipt `c2-at-A4.json`, `measured at 1e2c310295`).
  Commit **`6f9fd7f8`** — whose own subject reads "record quotes its own receipts
  (atoms 42, exempted 1)" — updated the cell's `atoms 50→42` and the receipt path
  `A4→A7`, and fixed `exempted 1` in the **`## Owned axes` calibration row**
  (SCORECARD.md:25) — but **left `exempted 2` standing in the claim-table cell**.
  `corpus/lessons/round-47.md:53` (M47-9) even asserts "the cells now read 42 and 1" —
  true for the Owned-axes row, false for the claim row. The repair was one cell short.
- Exact command proving the disagreement:
  `jq '.exempted | length' .ufo/waves/round-47/l1/scores/c2-at-A7.json` → `1`, vs
  `SCORECARD.md:3703` quoting `exempted 2 <= 3` citing that same file.

### Working correction (verified against the frozen functions at `ac02a79f`)

`- corrects quote round-47: exempted 1` — `_quote_correction` returns **True**:
`{key:exempted, value:1, quoted:[2], backed:true}` because the cited A7 receipt states 1
and the card quotes a different value. Negative controls behave correctly:
`exempted 2` → False ("the section already quotes that value"); `exempted 9` → False
("no cited receipt states that value"). Harness: `RevRecord/verify-corrections.py`
(sha256 `ec04b9e9…`), output `RevRecord/verify-corrections.out.json`.

## 4. Second record disagreement — `measured at` cell is stale by three receipts

The R47-C2 row's `measured at` reads **`1e2c310295`** (the A4 commit), but the section's
own header says "both claims are measured at `a0753786`" and both cited receipts carry
`"rev":"a07537869cf37963dff559fc75271dfa8fbb2542"`. Same A4→A7 update that was
half-applied in `6f9fd7f8`. Not a QUOTE-grammar key — the oracle sees `1e2c310295` only
as a `rev` atom (resolves, ancestor — green) — so **no clause binds the `measured at`
cell to the cited receipt's `rev`**. This is a *new* hole of the same class worth
routing: the quote clause binds `atoms|exempted|corrections|mismatches` only; a `rev`
cell inside a sentence is bound to ancestry, not to the receipt it cites.
(The `record-misquotes-its-own-receipt` repair taught the lane to bind numbers;
revision ids it cites remain bind-free.)

## 5. Completeness-floor evidence — round-47 seat atom

- The round-47 section contains **no seat-count sentence**: the only "seat"/"wave"
  tokens are inside the R47-C2 *before*-cell quoting round-45's wrong claim
  (`"wave 2: 32"`), which `collect()` does not parse for round 47. `floor` output:
  round-47 `{path:4, rev:13, window:1}`, `seats_via_correction:false`.
- `.ufo/waves/round-47/w1-dispatch.json` `.counts.spawn` = **75**; no `w2-dispatch`
  exists → derived `(1 wave, 75 seats total)`.
- Working correction (verified): `- corrects seats round-47: 1 wave, 75 seats total` —
  oracle `corrects()` returns True `{claimed:[1,75], derived:[1,75], dispatch:[75]}`.
  Negative control `74` → False. (Same harness/output as §3.)

## 6. Full enumeration — every other receipt-stated number in the two sections

All remaining numbers verified; **no further disagreements**. Sources: the 12 cited
receipts (all blob==worktree at HEAD), dispatch files, `git log` window checks,
`registry.py/attest.py --selftest` runs.

Round 46 (cited: `ctl-c1-0-do-nothing.json`, `ctl-c2-1-v1-scope.json`,
`{c1,c2}-at-F4.json`, `{c1,c2}-at-A4.json` via brace-path text):

| number | stated | receipt/truth | ok |
|---|---|---|---|
| C1 before `marker_occurrences 0, block_present 0, rule_blocks 22` | yes | ctl-c1-0 same | ✓ |
| C1 before `rows 0` | 0 | ctl-c1-0 `"rows": null` | ✓ (weak — key absent ⇒ null) |
| C1 `v1_green 9` | yes | c1-at-F4 `battery.v1_green=9` | ✓ (note: truth lives in the *after* receipt; the parenthetical attributes it to the round-45 clause set, not the cited ctl) |
| C1 after `rule_blocks 23, rows 13, refs 9, unresolved []`, battery `9/9/0/1`, `met_target true` | yes | c1-at-F4 identical | ✓ |
| C2 before `registered six, scope_size 6` | yes | ctl-c2-1 `scope_size:6`, registered len 6 | ✓ |
| C2 after `scope_size 38, registry_rows 38, registered 38, unregistered [], thin [], absent []`, battery `7/7/0/1` | yes | c2-at-F4 identical (registered len=38) | ✓ |
| `Waves: 40 + 40 = 80 seats` | yes | w1/w2-dispatch spawn 40+40 | ✓ (round-46's own; the round-45 correction is separate) |
| coverage `knowledge_files 138, mapped 138` | yes | `git ls-tree` + README map ∩ = 138 | ✓ |
| depth `22 → 23`, `citation_resolved_rules 23/23` | yes | ctl-c1-0 `rule_blocks:22` → c1-at-F4 `23` | ✓ |
| calibration `6 → 38` | yes | ctl-c2-1 → c2-at-F4 | ✓ |
| fidelity `22/10/8`, `45/6` | yes | ctl-c1/c2-fidelity `rule_blocks 22/rows 10/refs 8`, `registry_rows 45/scope_size 6` | ✓ |
| A4 block `rule_blocks 23, rows 13, refs 9`, `9/9/0/1`; `38` cells, `7/7/0/1` | yes | c1-at-A4/c2-at-A4 identical | ✓ |
| `cases=18 failures=0` (F5) | yes | `attest.py --selftest` → `ATTEST_SELFTEST: cases=18 failures=0` exit 0 | ✓ (`RevRecord/attest-selftest.txt`; NB `registry.py --selftest` says `cases=12`, and needs `--root/--freeze/--rev` despite the flag) |
| window `empty in 332f4884..58eb04b6 -- tools/round-46 plans/round-46-claims.md` | yes | `git log --name-status --format=` → empty | ✓ |

Round 47:

| number | stated | receipt/truth | ok |
|---|---|---|---|
| C1 before `block_present 0, rule_blocks 23, marker_occurrences 0` | yes | ctl-c1-0 identical | ✓ |
| `battery.v2_green 4` (round-46 profile) | yes | **c1-at-A7** `battery.v2_green=4`; the sentence cites only `ctl-c1-*` controls, none of which carries a battery cell | ✓ value, ✗ attribution |
| C1 after `rule_blocks 24, rows 4, refs 9, unresolved []`, battery `4/4/0/1/0` | yes | c1-at-A7 identical (rows 4, refs 9, rule_blocks 24) | ✓ |
| C2 before: `exit 1, 4 mismatches` (seats 32-vs-36, `<tip>` window, cov 133/133-vs-138/138, depth 20/20-vs-23/23) | yes | ctl-c2-0 exactly those 4 mismatches | ✓ |
| C2 after `atoms 42`, `corrections 2`, battery `3/0` | yes | c2-at-A7 | ✓ |
| C2 after `exempted 2` | **no** | `len=1` | **✗ — §3** |
| `measured at 1e2c310295` | **no** | receipt rev `a0753786` | **✗ — §4** |
| prose "4 → 0 mismatches over 50 atoms" | half | mixes ctl-c2-0 atoms(50) with A7 mismatches([]) — the after-receipt counts 42 | imprecise, not QUOTE-bound |
| Owned-axes `exempted 1` (calibration row, :25) | yes | c2-at-A7 | ✓ (the cell M47-9's fix actually reached) |
| `7 freeze commits` series | yes | `5017e1f7,9018c53b,62e33f7d,2e4ae43,1e2c3102,07d2894e,f54b3b6d` all resolve+ancestors | ✓ |

## 7. What the quote clause can and cannot see (mechanics, for the L1)

- `_quote_correction` requires the correction's stated value to be **backed by a
  receipt the corrected section cites** and **different from what it quotes** —
  `exempted 1` satisfies both (§3). The intended landing line
  `- corrects quote round-47: exempted 1` re-derives green.
- Quotes bind to the *cited receipt*, never to live truth: `atoms 42` stays green even
  though the same oracle derives **44** at `ac02a79f` (SCORECARD edits after `a0753786`
  added atoms; `c2-at-FINAL.json` already read 44). By design, but worth knowing: a
  section can be quote-honest and atom-stale simultaneously.
- `RECEIPT` only matches `…/l1/scores/*.json`: before-cell control receipts and the
  amendment line `l1/scores/{c1,c2}-at-A4.json` (brace syntax, no `.ufo/waves/` prefix)
  are invisible to the clause. `measured at` and dispatch `spawn` numbers are likewise
  unbound (§4) — same M47-9 family, next cell over.

## Receipts

`RevRecord/` — `record2-at-A2.json` (exit 1), `record2-freezeA1-revA2.json` (exit 2),
`record2-v2-at-A2.json` (exit 0), `verify-corrections.py` + `.out.json`,
`registry-selftest.txt` (`cases=12`), `attest-selftest.txt` (`cases=18`).
Commands verbatim in §§0–6; all run under
`TMPDIR=/fast/scratch/hyaku/kaidoku-r48/RevRecord`, UTC 2026-10-28T18:49–18:56Z.
No installs; python3 stdlib + git + jq only. Scratch `$S` removed after this copy.
