# Seat MutBlock24 — craft block 24 mutated row by row, under v3 and v2

Role: UFO-FSD mutation tester, round 47 wave 1. Leaf seat: no subagent dispatch.
Lane root: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Measured revision: `31b092d17e77f5064c919383a9bc1e6cbfd2d1ff` (UTC 2026-10-28T18:00:21Z).
Detector bytes: `tools/round-47/exact.py` @ `31b092d1` = `01a4bca7a60bb598b57a0c99f41b912ff1967badaa002d289ea1fe450bc5bcd5`
(pinned into scratch; the worktree copy is the same blob and `tools/round-47/` was clean).
Mutated artefact: the single marked craft block, sha256
`a1018174547c94e55db218692ea54d7af803577db62fc5557c569f24e6d6e879`.
Exit codes: 0 met, 1 not met, 2 could-not-evaluate.

## Headline

1. **The core discrimination table holds: 13/13 mutations killed by v3, 12/13 green under v2.**
   Every category the seat names (token, id, cells, exit, title, marker, header, digest, pin,
   refs) has at least one mutation that v3 catches and v2 does not.
2. **11 of 27 supplementary mutations SURVIVE v3.** The block's *row* semantics are unbound:
   the routed id, the arm token and the exit digit are three independent multisets. All four
   arm cells may read `order`; all four exits may read `2`; any id may sit on any row. Only the
   id multiset is a bijection. Clause 5 is membership, not assignment.
3. **The declared freeze cannot measure the landing.** `--freeze 5017e1f7` and the
   claims-derived freeze `62e33f7d` both exit 2 `frozen_path_changed` at `31b092d1`; only
   `--freeze <rev>` (base == tip) is green, and there the drift arm is vacuous.
4. **Causal separability is false through the freeze arm.** C1 derives the directory
   `tools/round-47/`, which contains C2's `record.py`; a C2-only repair makes the C1 counter
   exit 2 naming `record.py`.

## Command

```sh
S=/fast/scratch/hyaku/kaidoku-r47/MutBlock24; export TMPDIR="$S" HYAKU_SCRATCH="$S"
L=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
REV=$(git -C $L rev-parse HEAD)
D=$S/detector-$REV; mkdir -p "$D/tools/round-47" "$D/tools/round-46"
git -C $L show $REV:tools/round-47/exact.py > "$D/tools/round-47/exact.py"
git -C $L show $REV:tools/round-46/gate.py > "$D/tools/round-46/gate.py"
DETECTOR=$D python3 -I -B $L/.ufo/waves/round-47/w1/MutBlock24/mut13.py \
  $L $REV $S $L/.ufo/waves/round-47/w1/MutBlock24/receipts/mut13-at-landing.json
# exit 0, stdout sha256 a6ff96e54852c14c5e15ba3dd6b031a12796fe668d0c9824311c022c033e2302
# table receipt sha256 a0816cf76c23a99b9ba1e78950b615371c0f978bf1a1894a7b73056916bb945e
```

Driver: `.ufo/waves/round-47/w1/MutBlock24/mut13.py`. Each mutation edits exactly one defect
class in the marked block (or, for `flag-order-swapped`, the fixture's `gate.py`), is written
into a fresh one-commit fixture repo built from the measured revision's own bytes
(`exact._fixture_files` + `exact._repo`, `git -C "$D"` throughout, toplevel asserted by
`_repo`), and is scored by **the frozen counter's own `score()`** under `--profile v3` and
`--profile v2`. Nothing in the lane tree is written; `SKILL.md` is read through
`git show <rev>:SKILL.md`.

## Controls

| control | result | receipt |
|---|---|---|
| genuine block, v3, same fixture shape | exit **0**, `failing []` | `mut13-at-landing.json` (`genuine.v3`) |
| genuine block, v2, same fixture shape | exit **0**, `failing []` | `mut13-at-landing.json` (`genuine.v2`) |
| frozen counter end-to-end, `--freeze $REV --rev $REV --profile v3` (battery on) | exit **0**; `forgeries_total 4, v2_green 4, v3_green 0, genuine_green 1, crash 0` | `landing-v3-battery.json`, sha `918a12a8f991800c73ff55579b75424d04f2a6007b0a34be9b8983cae065b7da` |
| frozen counter, `--profile v2` at `07d2894e` | exit **0** (v2 is not "always red") | `real-v2.json`, sha `d3035f5cd808beb58b9d06b21165e7767a5d76d1b2a0c739247ed0967cdc5a32` |
| counter's own `--selftest` | exit **0**, `cases=16 failures=0` | `selftest.stdout`, sha `0249b80f58085f0d52cca3f7ae3f731d88d38dd4daaca6f84cefa023e3028aaa` |
| table stability across the A6/A7 amendments | at `07d2894e` (detector `dcef54f1`) the 35 mutations common to both runs have **identical** v2/v3 exits | `mut13-pinned.json` vs `mut13-at-landing.json` |

The table was first measured at `07d2894e` with the worktree detector, then re-measured with
the detector bytes pinned out of `git show <rev>:tools/round-47/exact.py` — identical exits,
so no worktree contamination. `07d2894e` block sha `996c118b…`, `31b092d1` block sha
`a1018174…` (A6/A7 changed the interpreter pin and added one knowledge citation; the table,
header and digest are unchanged).

## Table 1 — the 13 core mutations (one per seat category)

| # | mutation | category | v3 exit | v2 exit | detected by (v3 clause) |
|---|---|---|---|---|---|
| 1 | `token-substring` (every arm cell `order-ish`) | token | 1 | 0 | c5 |
| 2 | `token-synonym` (row 1 arm `symbolic`) | token | 1 | 0 | c5 |
| 3 | `id-duplicate-row` (fifth row re-claims `R46-CL2`) | id | 1 | 0 | c3, c4 |
| 4 | `id-two-per-cell` (row 1 trigger names `R46-CL2` and `R46-CL3`) | id | 1 | 0 | c3, c4 |
| 5 | `cells-five` (row 2 carries a fifth cell) | cells | 1 | 0 | c3 |
| 6 | `exit-out-of-range` (row 1 exit `3`) | exit | 1 | 1 | c3 |
| 7 | `title-unnumbered` (title loses `24. `) | title | 1 | 0 | c1 |
| 8 | `marker-duplicated` (marker twice in the block) | marker | 1 | 0 | c1 |
| 9 | `header-reordered` (`exit \| v3 arm \| v2 hole \| trigger`) | header | 1 | 0 | c2 |
| 10 | `digest-stale` (digest over three of four mutations) | digest | 1 | 0 | c6 |
| 11 | `pin-mismatch` (`interpreter_sha256` → 64 zeros) | pin | 1 | 0 | c8 |
| 12 | `refs-no-selector` (first citation loses `:57-66`) | refs | 1 | 0 | c8 |
| 13 | `refs-must-cite-missing` (all `round-46.md` → `round-45.md`) | refs | 1 | 0 | c8 |

v3 kills 13/13. v2 is green on 12/13 — the only v2 kill is `exit-out-of-range`, because the
`{0,1,2}` check is shared by both profiles. That is the measured discrimination the block
claims, reproduced independently of the counter's own four forgeries.

## Table 2 — supplementary 27 (survival is the finding)

| # | mutation | category | v3 exit | v2 exit | detected by (v3 clause) |
|---|---|---|---|---|---|
| 1 | `exit-semantics-0` (row 1 exit `1`→`0`) | exit | **0** | 0 | none — survives |
| 2 | `hole-cell-empty` (row 2 `v2 hole` cell emptied) | cells | **0** | 0 | none — survives |
| 3 | `arm-permuted` (arms of rows 1 and 4 swapped) | token | **0** | 0 | none — survives |
| 4 | `id-permuted` (triggers of rows 1 and 3 swapped) | id | **0** | 0 | none — survives |
| 5 | `id-substituted-unrouted` (`R46-CL7` in row 4) | id | 1 | 1 | c4 |
| 6 | `cells-three` (row 3 loses its hole cell) | cells | 1 | 1 | c3, c5 |
| 7 | `marker-missing` | marker | 1 | 1 | c1 |
| 8 | `header-renamed` (`v3 arm`→`arm`) | header | 1 | 1 | c2 |
| 9 | `digest-absent` (pin removed) | digest | 1 | 0 | c6 |
| 10 | `pin-absent` (pin removed) | pin | 1 | 0 | c8 |
| 11 | `title-renumbered` (`25. `) | title | 1 | 0 | c1 |
| 12 | `mutation-name-extra` (`fifth-forgery` added) | digest | **0** | 0 | none — survives |
| 13 | `refs-outside-allowlist` (`corpus/QUALITY.md:45-113`) | refs | 1 | 1 | c8 |
| 14 | `refs-unresolvable-line` (`round-46.md:57-9999`) | refs | 1 | 1 | c8 |
| 15 | `refs-two` (Refs line cut to two citations) | refs | **0** | 0 | none — survives |
| 16 | `digest-reordered` (same names, reversed) | digest | 1 | 0 | c6 |
| 17 | `mutation-name-dropped` (one name removed, digest correct) | digest | 1 | 0 | c6 |
| 18 | `flag-order-swapped` (fixture `gate.py` reversed pair) | digest | 1 | 0 | c7 |
| 19 | `header-extra-cell` (fifth header cell `note`) | header | 1 | 0 | c2 |
| 20 | `arm-token-case` (`Symbol`) | token | 1 | 0 | c5 |
| 21 | `self-ref-line-past-eof` (`exact.py:9999` cited) | refs | **0** | 0 | none — survives |
| 22 | `refs-only-self` (all Refs point at `exact.py:1..3`) | refs | **0** | 0 | none — survives |
| 23 | `composite-block23-relabelled` (block 23 text as `24. `) | composite | 1 | 1 | c2,c3,c4,c5,c6,c8 |
| 24 | `rows-three` (one row deleted) | cells | 1 | 1 | c3, c4 |
| 25 | `arm-all-order` (every arm cell `order`) | token | **0** | 0 | none — survives |
| 26 | `arm-duplicate-symbol` (`symbol, symbol, once, order`) | token | **0** | 0 | none — survives |
| 27 | `exit-all-two` (every exit cell `2`) | exit | **0** | 0 | none — survives |

Full `failing` text for every row: `receipts/tables.md` (generated from
`mut13-at-landing.json`, no hand transcription).

The claims kill rule is confirmed: `composite-block23-relabelled` fails clauses 2–6 (and 8:
block 23's citations do not all resolve under block 24's obligations) under v3.

## Surviving mutants — what each one proves

All eleven are **coverage findings**: the frozen predicate is satisfied by the mutation, so the
clause is exactly as written and I changed no frozen byte. Each is a forgery the landed block
cannot distinguish from the genuine article.

1. **`exit-all-two` / `exit-semantics-0`** — the exit column is a digit-membership check
   (`r[3] in {"0","1","2"}`), not a claim about the defect. A table where every row claims
   `2` (could-not-evaluate) scores met. The block's four rows currently say `1`; nothing binds
   that to `gate.py`'s or `exact.py`'s actual exit for the forgery.
2. **`arm-all-order` / `arm-duplicate-symbol` / `arm-permuted`** — clause 5 is
   `a in VOCAB` per cell, not a bijection over `{symbol, once, digest, order}` and not an
   assignment to the row's defect. Four `order` cells, or `symbol, symbol, once, order`
   (with `digest` absent), both score met. Only the *id* set is bijective.
3. **`id-permuted`** — cardinality without association: `R46-CL2` may sit on the row about
   `R46-CL6`'s flag order. Clause 4 counts a multiset; it never reads the row's `v2 hole` text.
4. **`hole-cell-empty`** — the `v2 hole` column is never read by any clause. A row may state
   no hole at all.
5. **`mutation-name-extra`** — clause 6 requires the four names to be *substrings* of the
   block; extra names are unconstrained, so the prose may pin a list the counter does not own.
6. **`refs-two` / `refs-only-self`** — `refs` counts every `HARD_REF` match anywhere in the
   block, including the intro prose. Cutting the `Refs:` line to two citations still yields
   `refs >= 3`, and `MUST_CITE` is satisfied by a prose mention of `round-46.md`. The `Refs:`
   line itself is not the citation set the clause names.
7. **`self-ref-line-past-eof`** — `check_refs` `continue`s on `SELF` **before** the line
   selector is validated, so `tools/round-47/exact.py:9999` resolves. Clause 8 says every
   reference carries a selector that resolves; the interpreter reference is exempt from
   resolution (defensible via its sha256 pin, but broader than the predicate text).

Net: the matrix binds four *sets* (ids bijectively, arms by membership, exits by membership,
refs by count) and does not bind a *row*. A row's three cells can be mutually inconsistent and
the block still scores met. If the landing wants the table's discrimination measured rather
than asserted, the cheapest closure is a clause that the arm token multiset equals
`{symbol, once, digest, order}` and that each row's exit equals the exit the counter records
for that row's forgery.

## Freeze findings (blocking for the landing's own re-measurement)

**F1 — the declared freeze is red at the landing, and only a vacuous freeze is green.**

```sh
git -C $L log --format=%H -1 -- plans/round-47-claims.md      # -> 62e33f7d… (A2's commit)
git -C $L log --format='%h %s' 62e33f7d..HEAD -- tools/round-47/ plans/round-47-claims.md
#   f54b3b6d A6  (tools/round-47/exact.py + _fixture_files)
#   07d2894e A5  (tools/round-47/record.py)
#   1e2c3102 A4  (tools/round-47/record.py)
#   2e4ae434 A3  (tools/round-47/record.py)
```

| freeze | rev | exit | receipt |
|---|---|---|---|
| `5017e1f7` (the prompt's freeze) | `31b092d1` | **2** `frozen_path_changed` `[plans/round-47-claims.md, tools/round-47/, exact.py, record.py]` | `freeze-5017-v3.json`, sha `f55cd2fd…` |
| `62e33f7d` (claims-derived) | `31b092d1` | **2** `frozen_path_changed` `[tools/round-47/, exact.py, record.py]` | `freeze-declared-v3.json`, sha `688f7a8c…` |
| `62e33f7d` | `62e33f7d` | 0 met | `fx-a2-freeze-at-a2.json`, sha `607f55c0…` |
| `62e33f7d` | `2e4ae434` (A3) | **2** `frozen_path_changed` | `fx-a2-freeze-at-a3.json`, sha `b976b396…` |
| `31b092d1` | `31b092d1` | 0 met (battery 4/4/0/1/0) | `landing-v3-battery.json`, sha `918a12a8…` |

`plans/round-47-claims.md` at `31b092d1` carries **only** `Freeze amendment A1` and
`Freeze amendment A2`; A3–A6 changed frozen bytes without a claims commit, so the rule the file
states (`git log --format=%H -1 -- plans/round-47-claims.md` re-derives the freeze) now names a
freeze that is red at every later revision. `--freeze <rev>` is legal
(`merge-base --is-ancestor X X` → 0) and makes the arm vacuous: `history_touched` over `X..X`
is empty and `blob_changed` compares identical objects, so **no drift can be detected**. A green
measurement of this landing therefore cannot come from the freeze arm; it needs a new disclosed
amendment commit that touches the claims file (advancing the derived freeze past A6), or an
explicitly stated measured freeze.

Also recorded: at A1's freeze (`9018c53b`) the landing `e856beb5` was **exit 1**, clause 5,
because the arm cells still carried sentences (`symbol: the arm cell must equal …`). A2's
"arm cells carry only the token" is what made the block green — `fx-a1-freeze-at-landing.json`,
sha `ecfc3e92…`.

**F2 — causal separability fails through the freeze arm.** The claims file says C1 "never
reads `SCORECARD.md`" and "either lands and scores without the other". True of the scoring
code; false of the freeze arm. C1 derives the directory `tools/round-47/`, which contains
C2's `record.py`. A3/A4/A5 are record-only repairs, and `freeze-declared-v3.json` (a C1 run)
exits 2 with `frozen_path_changed` naming `tools/round-47/record.py`. A C2-only repair blocks
the C1 verdict. If separability is to be a claim, each counter's frozen set must be its own
file, not the shared directory.

## Restoration evidence

- No lane file was written by this seat. `SKILL.md` is read only through `git show <rev>:SKILL.md`;
  `git -C $L status --porcelain -- SKILL.md` is empty, and the block's bytes at the measured
  revision hash to `a1018174…` (recorded in `mut13-at-landing.json`).
- The mutated bytes exist only inside one-commit fixture repos under
  `/fast/scratch/hyaku/kaidoku-r47/MutBlock24/`, each removed by the driver (`shutil.rmtree`)
  after scoring. No fixture is cited as evidence; the receipts are.
- `tools/round-47/` and `plans/round-47-claims.md` were never written (read-only `git show`
  only). The scratch root is removed before yield; receipts are copied under
  `.ufo/waves/round-47/w1/MutBlock24/receipts/`.
- No git/jj mutation was run in the lane or the fleet repo; every fixture git call used
  `-C "$D"` after `_repo` asserted `rev-parse --show-toplevel == d`.

## Not run / limits

- Not run: C2 (`record.py`) scoring — out of this seat's scope; the freeze receipts above only
  show C2's frozen file inside C1's `frozen_path_changed`.
- Not run: any mutation of `plans/round-47-claims.md` or `tools/round-47/*.py` themselves
  (frozen; mutation of the detector is not this seat's probe).
- The table is measured at `31b092d1`; HEAD is live and advanced four times during this seat
  (`07d2894e` → `a0753786` → `31b092d1`). The 35-mutation intersection was identical at
  `07d2894e`, so the table is stable across A6/A7, but a re-measure at the final landing
  revision should be re-run with the same command.

## Installs

None. No package, tool or binary was installed; no PATH directory was touched.
