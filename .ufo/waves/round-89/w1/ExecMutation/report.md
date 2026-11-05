# ExecMutation — round-89 declared-case mutation table (R89-C1 + R89-C2)

Seat: `.ufo/waves/round-89/w1/ExecMutation/` · L1: KaidokuR89 · 2026-11-04
Lane base rev `0ec2bb4016655f605657d6e0e700ec2e6893ac27`; lane tip moved to
`5068ba6417f3cfc6693ca5e4dbe106c08e305174` during the seat (wave in flight); all
rev-pinned arms name explicit revs, never the moving tip.

## 0. Method

Both instruments were copied into scratch (`/fast/scratch/hyaku/kaidoku-r89/ExecMutation/run/tools/round-89/`,
with symlinks `run/tools/round-87` and `run/tools/round-88` → the lane's pinned modules, because
the repair resolves `ROOT` three dirnames up and loads R87/R88 by path). Copies hash-verified:

```
332917f2b620da7a659b78db5bf498c8af2eba6ae529d872c2518b62ad6b1070  upx-field-value-repair.py
359f15e1c87f5106aa3fcbef211568ab7a970564ea0d7ed877299ca706dcf18f  depth-blocks-v2.py
f6f5ed61f47e055b7cfa6b58c2e29064d8e4eb31859ff1963a8e80393cd0b720  upx-field-battery.py (counter, run pristine)
```

**Pin discrepancy (for the L1):** the dispatch header pins the repair at `048e2c8e…`; the on-disk
file, the frozen plan's instrument list, and the pristine battery receipt's `repair_sha256` all say
`332917f2…070`. The plan pin matches disk; the header pin does not match anything I could hash.

28 single-anchor mutants (14 per instrument), each built by exact-string replacement with a
one-hit anchor assertion (`mutants/manifest.json`, hashes in `receipts/mutants-sha256.txt`).

Arms exercised per mutant:
- **Repair mutants:** `--selftest` (in-process fixture, no upx) + the full pristine C1 battery
  (`upx-field-battery.py --expect-recovered 4`, REA on) — run for **all 14** repair mutants, not
  just selftest survivors, so arm-level policing is measured for every row.
- **Depth mutants:** `--selftest` + four declared arms + five supplementary demo worlds:
  - `base-red`: `--root <lane> --rev 0ec2bb40… --expect-blocks 29` (pristine exit 1, blocks 28)
  - `stub-red`: base content + 5-word/1-span stub block, `--worktree --expect-blocks 29` (pristine exit 1, blocks 29 resolved 28 — same shape as `pre/c2-control-stub-world.json`)
  - `green`: `--root <lane> --rev 8bbb40cc… --expect-blocks 29` (pristine exit 0, blocks 29 resolved 29)
  - `no-target`: `--expect-blocks` omitted (pristine rc 2)
  - demos: `span-poor` (31 words, 1 span), `stray` (`- **` bullet after the next `## ` section),
    `range-inverted` (`:3-2` of a 3-line file), `overcount` (30 valid blocks, expect 29),
    `gitrev` (git fixture: rev1 green / broken worktree).

Kill = exit-code (or selftest-failure) deviation from the pristine arm in the detecting direction.
A mutant no *declared* arm catches is a named coverage gap even if a supplementary demo kills it.

## 1. Pristine green proofs (all run this seat)

| check | command (abbreviated) | rc | verbatim |
|---|---|---|---|
| repair selftest | `python3 -I -B tools/round-89/upx-field-value-repair.py --selftest` | 0 | `SELFTEST cases=16 failures=0` |
| depth selftest | `python3 -I -B tools/round-89/depth-blocks-v2.py --selftest` | 0 | `SELFTEST cases=10 failures=0` |
| C1 battery green | battery `--repair-cmd tools/round-89/upx-field-value-repair.py --expect-recovered 4` | 0 | `recovered 4 of 4 controls_ok={'N1-refuse-plain': True, 'N2-corrupt-payload': True, 'N3-intact-idempotent': True, 'isolation': True} met=True exit=0` (wall 197 s; regression arm `recovered 4 … met=True`) |
| depth base-red | `--rev 0ec2bb40… --expect-blocks 29` | 1 | `blocks 28 resolved 28 expect 29 unresolved 0 met=False exit=1` |
| depth stub-red | fixture, `--worktree --expect-blocks 29` | 1 | `blocks 29 resolved 28 expect 29 unresolved 1 met=False exit=1` |
| depth green | `--rev 8bbb40cc… --expect-blocks 29` | 0 | `blocks 29 resolved 29 expect 29 unresolved 0 met=True exit=0` |
| depth green (live) | `--root . --worktree --expect-blocks 29` on the lane | 0 | `blocks 29 resolved 29 expect 29 unresolved 0 met=True exit=0` |
| depth no-target | flags minus `--expect-blocks` | 2 | stderr: `could-not-evaluate: --expect-blocks N is required (QUALITY 157)` |

## 2. Repair mutants (`upx-field-value-repair.py`) — 14 rows

Battery column: `met` / false arms on the failing carriers. All battery runs used the pristine
counter (`f6f5ed61…`), REA on, `--expect-recovered 4`.

| id | single-anchor edit | selftest | battery | verdict — killing case |
|---|---|---|---|---|
| R01 | drop `derived <= sz_unc0` bound | rc 0 | met=True exit=0 | **survived all declared arms — gap G1** |
| R02 | drop `fits_u_len` key (`key=(total,-derived)`) | rc 0 | rc 1, 3 of 4 | **killed**: case `dinit` arms `test_ok` (`upx: …/field.repaired: Exception: compressed data violation`) + `identity`; control `N3-intact-idempotent` false on dinit; regression arm unmet (r88 battery 3) |
| R03 | last candidate wins (`best=(key,…)` unconditional) | rc 0 | rc 1, 3 of 4 | **killed**: same triple as R02, carrier `dinit` |
| R04 | first candidate wins (`if best is None:`) | rc 0 | rc 1, 3 of 4 | **killed**: same triple as R02, carrier `dinit` |
| R05 | drop the `stored == derived` intact early-return | rc 1 | met=True exit=0 | **killed by selftest only**: `intact-class`, `magic-class-composed` (battery blind — output stays byte-identical) |
| R06 | invert `stored == derived` → `!=` | rc 1 (11 cases) | rc 1, 0 of 4 | **killed by both**: selftest `wrong-nonzero-recovered` et al.; battery all 4 carriers `test_ok`+`identity` false |
| R07 | drop re-validation through the anchor path | rc 0 | met=True exit=0 | **survived all declared arms — gap G2** |
| R08 | swap `chain-geometry` condition (`== 0` → `!= 0`) | rc 1 | met=True exit=0 | **killed by selftest only**: `zeroed-class`, `wrong-nonzero-class`, `wrong-out-of-range-class`, `corrupt-payload-not-structural` |
| R09 | drop method-byte filter `d[s1+8] not in (m0, method)` | rc 0 | met=True exit=0 | **survived all declared arms — gap G3** |
| R10 | drop `if b0 + 12 > ph_off: continue` | rc 0 | met=True exit=0 | **survived (equivalent on population)** — the inner `range(b0+13, ph_off-12)` is empty whenever the dropped guard would fire |
| R11 | drop `if sz_unc0 == 0: continue` | rc 0 | met=True exit=0 | **survived (equivalent on population)** — `0 < sc <= su` subsumes it (`su == 0` admits nothing) |
| R12 | delta sign flip (`stored - derived`) | rc 1 | met=True exit=0 | **killed by selftest only**: `wrong-nonzero-delta` |
| R13 | patch offset `block0 + 4` → `+ 8` | rc 1 (crash) | rc 1, 0 of 4 | **killed by both**: selftest aborts with uncaught `Refused: corrected bytes still implausible: p_info is not followed by a plausible b_info`; battery all 4 carriers `field_only` false (`byte 584 changed outside the sz_cpr window 580-584`; libz: `byte 9312 … 9308-9312`) + `test_ok`/`identity` |
| R14 | drop the sentinel gate (try/except → bare call) | rc 0 | met=True exit=0 | **survived all declared arms — gap G4** |

## 3. Depth mutants (`depth-blocks-v2.py`) — 14 rows

| id | single-anchor edit | selftest | killing arm(s) — exact case | verdict |
|---|---|---|---|---|
| D01 | `met_target = not unresolved` (the M88-7 defect) | rc 0 | **base-red**: `blocks 28 … met=True exit=0`; also demo-overcount | **killed** |
| D02 | drop `resolved == expect` conjunct | rc 0 | none | **survived — equivalent**: with `resolved = blocks − |unresolved|`, `blocks == expect ∧ ¬unresolved` implies `resolved == expect`; the conjunct is redundant |
| D03 | drop the word floor | rc 1 | selftest: `stub-refused-by-shape`, `two-spans-short-refused` | **killed** |
| D04 | drop the span floor | rc 0 | declared arms: none; **demo-span-poor**: `blocks 1 resolved 1 … met=True exit=0` | **declared-arms gap G5** (killed only by my supplementary world) |
| D05 | accept `start > end` ranges | rc 0 | declared arms: none; **demo-range-inverted**: green flip | **declared-arms gap G6** |
| D06 | absent citation file treated as ok | rc 1 | selftest: `absent-file` | **killed** |
| D07 | citation-less block counts | rc 1 | selftest: `no-citation` | **killed** |
| D08 | bare citation `start = 0` | rc 1 | selftest `bare-file-line1`; **green**: `blocks 29 resolved 27 … unresolved 2 met=False exit=1` (two landed blocks cite bare files); demos | **killed** |
| D09 | drop the `\n## ` section-end split | rc 0 | **green**: `blocks 37 resolved 31 … unresolved 6 met=False exit=1` (8 stray `- **` bullets after the craft section at the landed rev); demo-stray | **killed** (selftest's `block-split` alone would NOT catch it — no bullet after `## next` in that case) |
| D10 | `==` → `>=` in `met_target` | rc 0 | declared arms: none; **demo-overcount**: `blocks 30 … met=True exit=0` | **declared-arms gap G7** |
| D11 | drop the `--expect-blocks` required guard | rc 0 | **no-target**: rc 2 → rc 1 (`blocks 29 resolved 29 expect None unresolved 0 met=False exit=1`) — refusal text lost, red stays red | **killed** (only by the no-target arm; my declared arms always passed the flag) |
| D12 | `rev = None` (always read the worktree) | rc 0 | **base-red**: reads the green worktree → `met=True exit=0` on a red arm; **demo-gitrev**: `blocks None … met=False exit=1` on a green rev | **killed** |
| D13 | `MIN_WORDS = 0` | rc 1 | selftest: `stub-refused-by-shape`, `two-spans-short-refused` | **killed** |
| D14 | `MIN_SPANS = 0` | rc 0 | declared arms: none; **demo-span-poor**: green flip | **declared-arms gap G5** (same gap as D04, second anchor) |

## 4. What the survivors say about the instruments' guards

**Repair (C1).**
- **G1/R01, G3/R09, G4/R14 — the derivation's defensive filters have no red arm anywhere.** The
  `sz_unc0` bound, the method-byte filter and the sentinel gate are never the deciding filter on
  the declared population (fixture or the four carriers): dropping each still recovers 4 of 4 with
  every control true. They are guards against *adversarial* candidate fields (a decoy `s1` with a
  foreign method byte, a chain that fails the sentinel walk, a `derived` beyond `sz_unc0`), and no
  selftest case or battery carrier contains one. Suggested fix: one selftest fixture with a decoy
  candidate per filter (three small cases), or a battery carrier whose chain contains a decoy.
- **G2/R07 — the re-validation guard is unpoliced.** On every declared input the corrected bytes
  re-validate, so `repair()`'s "corrected bytes still implausible" refusal is never observed by any
  arm; the mutant is outcome-equivalent on the battery (`met=True`) because a bad correction that
  would have been refused instead fails `test_ok`/`identity` — same exit, different `false_arms`.
  The distinction (refuse vs write-garbage) is visible only in arm labels, which `met_target` ignores.
- **The selection law is policed only through identity-shaped arms on one carrier.** R02/R03/R04
  (drop `fits_u_len`, last-wins, first-wins) are all caught — but solely by `dinit` (docker-init),
  via the case arms `test_ok`+`identity`, the `N3-intact-idempotent` control (the mutated selection
  derives a value ≠ stored *on the intact file*, so the repair "corrects" an intact file), and the
  round-88 regression arm. jq/xxd/libz chains are single-candidate: first/last/best coincide there.
  The frozen predicate's strength on the selection law rests entirely on the dinit carrier.
- **The battery does not police the repair's info fields.** R05 (intact file rewritten — bytes
  identical, `class` mislabeled `field-value`), R08 (class labels swapped) and R12 (delta sign
  flipped) pass the full battery: `N3-intact-idempotent` checks byte-identity only, and no arm reads
  `info["class"]`/`info["delta"]`. The class label is part of the claim's semantics
  (`chain-geometry` vs `field-value`), so a counter arm asserting label consistency
  (e.g. `field-value ⇒ delta ≠ 0`, `chain-geometry ⇒ stored == 0`) would close R05/R08/R12 at the
  counter level; today only the repair's own selftest holds that line.

**Depth (C2).**
- **The target-aware `met_target` is genuinely guarded by the base-red arm** — D01 (the exact
  round-88 target-blind defect) flips it green at 28 blocks, and the declared base arm catches that.
  But the **over-count direction is not**: D10 (`>=`) survives base-red, stub-red, green and
  selftest; only a blocks>expect world (my demo-overcount) catches it. The selftest's
  `target-encodes-count` case asserts `len(blocks) == 2` without touching `met` arithmetic.
- **The span floor's red path is undeclared.** D04/D14 survive every declared arm: the stub world is
  words-red (5 < 25), the base blocks all carry ≥ 2 spans, and the selftest has a spans-ok/words-short
  case (`two-spans-short-refused`) but no words-ok/spans-short case. A 31-word/1-span block is green
  under both mutants. Same shape for **G6/D05** (no `start > end` citation anywhere) — the range
  ordering check has no red arm.
- **D11 shows the QUALITY-157 refusal guard is only exercised when the flag is omitted** — none of
  the declared arms omit it; the no-target arm (rc 2 → rc 1, refusal text
  `could-not-evaluate: --expect-blocks N is required (QUALITY 157)` lost) is the only catch.
- **Two load-bearing behaviors are guarded only by the live green arm, not by the selftest:**
  D09 (section-end split — the landed SKILL.md has 8 `- **` bullets after the craft section; the
  selftest's `block-split` case has none) and D08 (bare citations — two landed blocks cite bare
  files; only `bare-file-line1` covers them in selftest). If the landed block content changes,
  these guards silently weaken; a selftest case with a trailing-section bullet and a bare-citation
  block would pin them statically.
- **D02 is an equivalent mutant**: `resolved == expect` is implied by the other two conjuncts
  (`resolved = blocks − |unresolved|`). Harmless, but it is dead weight in the conjunct — either
  give it independent meaning or drop it.

**Score:** 28 mutants, 22 killed (13 repair / 9 depth… precisely: repair 8 killed, 6 survived of
which 3 equivalent-on-population and 3 gap; depth 11 killed, 3 survived of which 1 equivalent and
2 gap-anchors), 6 declared-arms gaps named (G1–G4 repair, G5–G7 depth). No mutant turned a declared
green arm green except through the gaps named; no mutant produced a false `met=True` on the C1
battery except R01/R07/R09/R10/R11/R14 (which are exactly G1–G4 + the two equivalents).

## 5. Receipts (beside this file, in `receipts/`)

`battery-pristine.json` · `battery-<R-id>.json` ×14 (each records the mutant's `repair_sha256`) ·
`battery-mutants-summary.json` (batch 1) · `battery-mutants-batch2-summary.json` ·
`repair-selftests.json` (rc + verbatim selftest lines for pristine + 14 mutants) ·
`depth-mutation-runs.json` (every arm's rc/stdout/stderr for pristine + 14 mutants) ·
`mutants-sha256.txt` · `mutants-manifest.json` (exact old/new anchor strings per mutant).

Mutant sources themselves lived only in scratch and are deleted with it; each is reproducible from
the manifest's anchor strings against the pinned instrument sha256.

## 6. Declarations

- No tool installed or upgraded (none needed) — nothing to record under the 2026-10-19 authorization.
- No pacman transaction; no host service touched.
- No mutating git/jj command anywhere except the sanctioned scratch git fixture
  (`worlds/gitrev`, `rev-parse --show-toplevel` asserted equal to the fixture dir before its commit;
  deleted with scratch). Lane git usage strictly read-only (`rev-parse`, `status`, `log`,
  `cat-file -e`, `show`).
- Nothing written outside the seat dir, its `receipts/`, and the seat scratch
  `/fast/scratch/hyaku/kaidoku-r89/ExecMutation/` (deleted before yield; nothing a report cites
  was ever written under `/tmp`).
- Scratch tree at yield: **removed** (verified by `ls`).
