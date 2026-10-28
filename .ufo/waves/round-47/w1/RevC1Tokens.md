# RevC1Tokens — clause 5 attack (`v3 arm` cell), round 47 wave 1

Seat: reviewer, leaf. Scope: **R47-C1 predicate clause 5 only** (`plans/round-47-claims.md:97-99`,
`tools/round-47/exact.py:235-243`), plus the counter-level consequences of what clause 5 does and
does not bind. Read-only on the lane; every write below this directory.

Time of measurement: 2026-10-28, tip `1e2c3102` ("A4 — the historical-correction selftest fixture
gets its round-3 dispatch"). The lane was moving under me; every rev is quoted in full.

## 0. Verdict in one line

Clause 5 is implemented as a real equality and is **not** satisfiable by a forged *cell* (only
`symbol`, `once`, `digest`, `order` survive `--profile v3`), but it is **satisfiable by a forged
matrix**: it does not bind the arm token to the routed id, does not require a permutation, and
leaves the `v2 hole` column completely unchecked. The frozen **kill rule** names a witness
(`blobberish`) that fails *both* profiles, so the claim's own discriminator is false as written.

## 1. Revs and instrument identity

| what | value |
|---|---|
| lane tip at final measurement | `1e2c3102952dc636650095643c1963c833859019` (A4) |
| matrix pinned at | `62e33f7dd75c8e3285967b26419842c106f6c965` (A2) |
| `SKILL.md` sha256 at matrix rev | `bf94d1b53a255d2e7bf50b0516ff679b3cd1e63e4e9b573d9fac5b54c3a3fae8` |
| `SKILL.md` sha256 at tip | `bf94d1b53a255d2e7bf50b0516ff679b3cd1e63e4e9b573d9fac5b54c3a3fae8` (identical → block 24 unchanged) |
| instrument executed | `tools/round-47/exact.py` sha256 `dcef54f1b14326c33b89a4c55e766832c2a938241968c1d3db1389f9b26c412c` |
| instrument at rev (`git show <rev>:tools/round-47/exact.py`) | same `dcef54f1…` — worktree bytes == committed bytes |
| block 24 text sha256 (from `- **24. ` to section end) | `692b6d6847b88e17aee75fe280d2fb8d61261f797bd11ad9953e9c58b58f0292` |
| landed arm tokens at tip | `['symbol', 'once', 'digest', 'order']` |
| landed pins at tip | `interpreter_sha256:dcef54f1…` (matches bytes at rev), `mutations_sha256:19a2166e…` (matches `MUT_DIGEST`) |

## 2. The code path clause 5 actually runs

```
tools/round-47/exact.py:235  # clause 5: arm token, exactly
tools/round-47/exact.py:236  arm = [r[2].strip("` ") if len(r) > 2 else "" for r in rows]
tools/round-47/exact.py:239      if any(a not in VOCAB for a in arm):        # v3: membership
tools/round-47/exact.py:242      if any(not any(t in a.lower() for t in VOCAB) …  # v2: substring, case-folded
tools/round-47/exact.py:35   VOCAB = ("symbol", "once", "digest", "order")
tools/round-47/exact.py:130  _cells: [c.strip() …]   # whitespace already stripped by the parser
```

Consequences for accuracy of the claim text:

- The claim (`plans/round-47-claims.md:97`) says "stripped of **backticks and spaces**". In the
  code, spaces were already removed by the table parser (`exact.py:130`, `c.strip()`), so the
  clause's `strip("` ")` removes only backticks in practice. Harmless, but the claim describes two
  mechanisms as one.
- `strip()` is character-set based, not delimiter-aware: the unbalanced cell `` `order `` is
  accepted by v3 (exit 0, fixture `fx-unbalanced_backtick`). Cosmetic only.

## 3. The matrix (one-commit fixture repos, frozen instrument executed from the lane worktree)

Every fixture is the lane's own bytes at `62e33f7d` for `SKILL.md`, `plans/round-47-claims.md`,
`tools/round-47/exact.py`, `tools/round-46/gate.py`, `corpus/lessons/round-46.md`,
`corpus/lessons/round-45.md`, with **one arm cell of row 1 (R46-CL2) rewritten and nothing else**.
Fixture repos were built with `git init` in scratch, `--freeze == --rev ==` the fixture's own
single commit, `--no-battery` (the battery is irrelevant to clause 5 and is measured separately in
§5). Command shape, identical for every row:

```sh
python3 -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-47/exact.py \
  --root <fixture> --freeze <fixture-rev> --rev <fixture-rev> --profile {v3|v2} --no-battery
```

| case | v3 exit | v2 exit | v3 `failing` / receipt |
|---|---|---|---|
| genuine (landed block) | **0** | **0** | — `02b3d6aa…` / `dc6e0e9d…` |
| row1 arm = `order` | **0** | 0 | — `d3b94697…` |
| row1 arm = `order-ish` | **1** | **0** | `arm cells not exact vocabulary tokens: ['order-ish', 'once', 'digest', 'order']` — `a769b7c6…` / `d9ce5b08…` |
| row1 arm = ` order ` | **0** | **0** | — `a3af8435…` / `1968b62f…` |
| row1 arm = `` `order` `` | **0** | **0** | — `cab13c42…` / `62e55bc5…` |
| row1 arm = `order,once` | **1** | **0** | `arm cells not exact vocabulary tokens: ['order,once', …]` — `cfac9caf…` / `4a82bcc1…` |
| row1 arm = `ORDER` | **1** | **0** | `arm cells not exact vocabulary tokens: ['ORDER', …]` — `f12f7079…` / `1f982c21…` |
| row1 arm = `` (empty) | **1** | **1** | `arm cells not exact vocabulary tokens: ['', …]` / v2 `arm cells outside the vocabulary` — `1d6ce8b7…` / `43f3e67a…` |
| all four arms = `order` | **0** | **0** | — `2aeef200…` |
| arms permuted (`once,digest,order,symbol`) | **0** | **0** | — `453cf0cc…` |
| row1 arm = `blobberish` | **1** | **1** | `arm cells not exact vocabulary tokens: ['blobberish', …]` / v2 `arm cells outside the vocabulary` — `c4616a30…` / `84c08fa7…` |
| row1 arm = `` `order `` (unbalanced) | **0** | **0** | — `5b84ebb0…` |
| row1 arm = backticked `order` + HTML comment | **1** | 0 | `arm cells not exact vocabulary tokens: ['order\`<!-- digest -->', …]` — `282650d7…` |
| all four `v2 hole` cells = "no known defect here" | **0** | — | — `8654232e…` |
| all four `v2 hole` cells = "nothing routed" | **0** | — | — `154d88de…` |
| row1 arm = `order` **and** row1 hole = "nothing" | **0** | — | — `65e7092d…` |

**Answer to the seat's question.** Under `--profile v3` these reach exit 0: `order` (genuine token),
` order ` and `` `order` `` (the claim's own denuding) — and, wrongly, `order` in a row whose id is
`R46-CL2`. Under `--profile v2` six reach 0: `order`, `order-ish`, ` order `, `` `order` ``,
`order,once`, `ORDER`; only the empty cell is red in both. **The difference set is exactly
{`order-ish`, `order,once`, `ORDER`}** — the three cells that *name* a token but are not exactly it.
That is the hole clause 5 closes, and it is closed.

## 4. Findings

### F1 — HIGH, frozen kill rule is false: `blobberish` does not discriminate

`plans/round-47-claims.md:129-130` states: "A block with `blobberish` in a v3-arm cell fails clause
5 while the v2 profile passes it." Measured (fixture `fx-blobberish`, mutated block sha
`c60f7c833d5975aa9c3427def640bece5661d03cd746f48592b9aa8bc567bcec`, row 1 arm := `blobberish`):
**v3 exit 1 and v2 exit 1**. `blobberish` contains no round-47
vocabulary token at all; `blob` is a *round-46* token (`tools/round-46/attest.py:46`,
`ARMS = ("commit", "blob", …)`). The kill rule was carried over from round 46 and its witness does
not exist in this round's vocabulary. Clause 5 itself is fine — the *claim's discriminator* is not,
which is exactly the failure mode the round is meant to catch.

What the claim would have to say: "A block with `order-ish` in a v3-arm cell fails clause 5 while
the v2 profile passes it" (equivalently `order,once` or `ORDER`; all three measured 1/0 above).
The residual evidence risk: the mandate's "measured, not asserted" claim for `v2_green 4`
(`plans/round-47-claims.md:125-127`) is unaffected — the battery forgery uses `order-ish`
(`tools/round-47/exact.py:70-72`), which really is v2-green. Only the prose witness is wrong.

### F2 — HIGH, clause 5 is vacuous about *which* arm closes *which* hole

`exact.py:236-239` checks membership only. Measured, both profiles: all four rows `order`
(exit 0, `arms ['order','order','order','order']`), and a full permutation that assigns every row
another row's token (exit 0, `arms ['once','digest','order','symbol']`). Row 1 is `R46-CL2`, whose
v3 arm is `symbol`; the counter accepts `order` there and cannot tell the difference from the
landed block. The landed block's *own* last row already carries `order`
(`R46-CL6`), so the wrong assignment creates a duplicate that nothing notices.

Consequence for R47-C1: the "exactness matrix" can be semantically wrong in every arm cell and
still score `failing == []`, i.e. clause 5 binds a *vocabulary*, not a *mapping*. Note that the
battery cannot expose this either: `substring-arm` rewrites **all** rows to `order-ish`
(`exact.py:70-72`), so the one arm forgery is the trivial uniform-superstring case.

What the claim would have to say (either is sufficient and cheap to implement):

- "the four v3-arm cells are a **permutation** of the four tokens" — kills the duplicate and the
  all-`order` matrix; or, strictly better,
- "row *i*'s arm cell is the token the routed id of row *i* is bound to: `R46-CL2→symbol`,
  `R46-CL3→once`, `R46-CL4→digest`, `R46-CL6→order`" — kills every wrong assignment.

With F1 and F2 together, note the asymmetry: a *duplicate routed id* is caught (clause 4,
battery `duplicate-routed-id` red in v3), a *duplicate arm* is not.

### F3 — MEDIUM, the `v2 hole` column is entirely unconstrained

No clause reads column 2. Measured: all four hole cells replaced by "no known defect here" → v3
exit 0; all four replaced by "nothing routed" → v3 exit 0; combined with the F2 duplicate arm →
v3 exit 0. So the block may assert, per row, that there is no defect while the id and exit cell
say there is one, and the counter is green. Half of the matrix's content is therefore decoration
and the claim's "the **exactness** matrix over the four round-46 routed instrument defects" is not
what the counter certifies.

What the claim would have to say: either bind the hole cell (e.g. it must cite a line selector in
`corpus/lessons/round-46.md` resolving at `--rev`, which the round already knows how to check —
`check_refs`), or drop the column from the claimed surface and let the block state only trigger,
arm, exit.

### F4 — MEDIUM (process, cross-cutting to both counters): no derivable `FREEZE` value except the tip

Measured at rev `1e2c3102` (v3, `--no-battery`), all with the frozen instrument:

| `--freeze` | exit | reason |
|---|---|---|
| `5017e1f7299c3a812e87e7950148f54313dd279e` (the prompt's freeze) | **2** | `frozen_path_changed` = `['plans/round-47-claims.md', 'tools/round-47/', 'tools/round-47/record.py']` |
| `9018c53b16503c8d06d398b75503406508119946` (A1) | **2** | same list |
| `62e33f7dd75c8e3285967b26419842c106f6c965` (A2, *the commit the claims file names*) | **2** | same list |
| `2e4ae43463aabdae707f8c8a4daa41441ad67a71` (A3) | **2** | same list |
| `1e2c3102952dc636650095643c1963c833859019` (A4 = tip) | **0** | `failing: []` |

The frozen-path series after the nominal freeze is A1 → A2 → A3 → A4
(`git log --format='%h %s' 13a9e9e1..HEAD -- plans/round-47-claims.md tools/round-47/`), but the
claims file declares only A1 (`plans/round-47-claims.md:23`) and A2 (`:35`). A3 and A4 touch
`tools/round-47/record.py` with **no claims paragraph**, and the claims' own freeze-derivation line
(`plans/round-47-claims.md:8-11`, `git log --format=%H -1 -- plans/round-47-claims.md`) returns
`62e33f7d` — a commit that exits 2. `plans/round-47-claims.md:10-11` ("Nothing in this file or in
`tools/round-47/` changes after the freeze: a change makes both counters exit 2
`frozen_path_changed`") is therefore true four times over, and the registered derivation is stale
by three commits.

What it would have to say: the derivation line must name both paths —
`git log --format=%H -1 -- plans/round-47-claims.md tools/round-47/` — and each amendment that
touches a frozen path needs its paragraph *in the claims file* (the file is the only derivation
source), or the series must be folded before the landing is measured. This is the L1's own
amendment series and was still moving while I measured (`5017e1f`@14:45 → A4@14:52); flagging it
because it is exactly what will make the landing re-measurement exit 2 if it is not closed.

### F5 — LOW, the prior-state prose understates the v2 hole

`plans/round-47-claims.md:54` and the R47-C1 "Prior state" paragraph describe the hole as a
"substring test". Measured, v2 also **case-folds**: `ORDER` is v2-green (exit 0) and v3-red. The
profile is faithful to round 46 (`tools/round-46/attest.py:218-219` also `.lower()`), so nothing is
mis-measured — the prose should say "case-folded substring" so the port and the description agree.

### F6 — INFO, cosmetic acceptance of unbalanced backticks

`` `order `` (and `` order` ``, ``` ``order`` ```) are accepted by v3 (exit 0). No semantic hole —
the stripped value really is the token — but it means a row may render as broken Markdown and still
score met. No claim change required; noted so no seat re-derives this as a new finding.

## 5. What I verified clean (positive receipts)

- **Landed block at tip `1e2c3102` scores the C1 target**: `--freeze <tip> --rev <tip> --profile v3`
  (full battery) → **exit 0**, `failing: []`, `rows 4`, `arm_tokens ['symbol','once','digest','order']`,
  `battery {forgeries_total 4, v2_green 4, v3_green 0, genuine_green 1, crash 0}`, and every forgery's
  v3 `failing` names its own clause (`substring-arm` → clause 5; `duplicate-routed-id` → rows/clause 4;
  `stale-mutations-digest` → clause 6; `flag-order-drift` → `gate.py flag order: 0 correct, 1 reversed`
  → clause 7). Receipt `receipts/lane-target.json`.
- **Pins are honest at the tip**: `interpreter_sha256:dcef54f1…` equals the sha256 of
  `tools/round-47/exact.py` at that rev, and `mutations_sha256:19a2166e…` equals the counter's own
  `MUT_DIGEST` over `MUTATIONS` in order.
- **Worktree == committed bytes** for the executed instrument (both `dcef54f1…`), and
  `git status --porcelain SKILL.md tools/round-47 plans/round-47-claims.md` was empty at measurement
  time, so the receipts are not taken against a dirty frozen tree.
- The genuine block is green under **both** profiles (v3 0, v2 0), so no clause outside the measured
  hole is what reds the v2 forgery — the discrimination really comes from clause 5.

## 6. Residual risk and verification gaps

- **Not run**: `tools/round-47/record.py` (R47-C2) — outside this seat. `plans/round-47-claims.md`
  claims the two counters are causally separable; nothing I ran contradicts that, and my fixtures
  never contained `SCORECARD.md`.
- **Not run**: the counter's `--selftest`. My fixtures exercise the same `score()` path through the
  CLI, which is stronger evidence than the selftest for my clause, but the selftest's
  `red-arm-substring` case is the only arm case it carries — it inherits F2 (it never tests a
  wrong-but-valid token).
- The lane moved three times during the measurement (A2 → A3 → A4). The matrix was pinned at
  `62e33f7d`; `SKILL.md` is byte-identical at `1e2c3102` (`bf94d1b5…`), so the matrix still describes
  the landed block, but **any further edit to block 24 invalidates §3** and the fixtures must be
  rebuilt from the new rev with `receipts/drive.py` (one `PIN_REV` file).
- `strip("` ")` with a non-ASCII lookalike (e.g. U+2018) is rejected; I did not exhaustively test
  Unicode confusables because the acceptance set is a closed four-string equality, which no
  confusable can join.
- Severity call on F4 is process-level; if the L1 intends the landing to be measured only at the
  amendment tip, F4 collapses to "the derivation line in the claims file must name
  `tools/round-47/`", which is a one-line fix and should still be made — otherwise the documented
  recipe is unrunnable.

## 7. Reproduction

`receipts/drive.py` is the whole matrix driver (cells, vacuity probes, full-battery run). It reads
`PIN_REV` and takes every byte from `git show <PIN_REV>:<path>` in the lane, so no lane write and no
scratch reuse is required:

```sh
S=/fast/scratch/hyaku/kaidoku-r47/RevC1Tokens
mkdir -p "$S" && export S TMPDIR="$S" HYAKU_SCRATCH="$S"
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin rev-parse HEAD > "$S/PIN_REV"
python3 -B receipts/drive.py > "$S/out.json"
```

Fixture repos are transient (`fx-*` under `$S`, removed before yield); the differing artefact of
each decisive fixture is preserved verbatim at `receipts/fixture-skills/<case>.SKILL.md`, so the
finding can be replayed byte-for-byte against the same rev.

## 8. Sources

- `plans/round-47-claims.md:8-11` (freeze derivation line), `:23` (A1), `:35` (A2), `:54` (prior
  state), `:81` (landed-surface wording), `:97-99` (clause 5), `:125-127` (v2 battery claim),
  `:129-133` (kill rule).
- `tools/round-47/exact.py:35` (VOCAB), `:70-72` (`_m_substring_arm`), `:129-130` (`_cells`),
  `:235-243` (clause 5 body), `:444-449` (selftest GOOD_ROWS/GOOD_REFS).
- `tools/round-46/attest.py:46` (round-46 ARMS, contains `blob`), `:218-219` (the v2 semantics the
  profile ports).
- `SKILL.md` block 24 at `1e2c3102` (`- **24. An instrument's binding is an equality…`, marker
  `<!-- exactness-table v3 -->`), table rows `R46-CL2 … R46-CL6`.
- Frontier step cited, not claimed (`plans/round-47-claims.md` Non-goals): none added by this seat.

## 9. Installs

None. No package was installed or updated for this seat; only `python3`, `git` and the frozen
instrument were used.
