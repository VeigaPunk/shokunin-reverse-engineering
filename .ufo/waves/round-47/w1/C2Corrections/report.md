# C2Corrections — R47-C2: the `## Record corrections — round 47` draft, and what the counter does with it

Seat `C2Corrections`, round 47, wave 1 (verification / drafting / attack, before further landing).
Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, read-only for me. Everything I ran lives
in `/fast/scratch/hyaku/kaidoku-r47/C2Corrections` (clone `repo/` + driver scripts), and is now
removed; the receipts I cite are preserved under
`.ufo/waves/round-47/w1/C2Corrections/`. No install, no `pacman`, no network.

Counter under test: `tools/round-47/record.py`, sha256
`abf352573d156ed1388683c882e40cab9897f426b9448356993bf41bf37779e7` (the A5/A7 bytes; unchanged at
the last lane HEAD I read, `09a9f912f4a639b91bce7dcd3711d8f391969d4f`). The lane HEAD moved six
times while I measured (`3186f69b` → `e856beb5` → `07d2894e` → `04469ee8` → `a0753786` → `09a9f912`);
every fixture below pins an explicit rev and every receipt names it.

## 1. What I ran

| # | command (exact) | rev | exit | utc | receipt |
|---|---|---|---|---|---|
| 1 | `HYAKU_SCRATCH=… TMPDIR=… python3 -I -B tools/round-47/record.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev 13a9e9e1f7ca3b95f2cc11f24f69d0d92a21a8a5 --json-out .ufo/waves/round-47/w1/C2Corrections/receipt.json` | `13a9e9e1` (round base) | **1** | 2026-10-28T17:49:50Z | `receipt.json` |
| 2 | same, `--rev f7d6e58d6e7f4e664bf443137c55ee08821de244` | `f7d6e58d` (pin) | **0** | 2026-10-28T18:00:43Z | `receipt-at-pin.json` |
| 3 | derivation commands (round-45 dispatch, five window ranges, knowledge count, craft-block count) | base / pin | 0 each | 2026-10-28T17:59Z | `receipts.jsonl` |
| 4 | 13-probe fixture suite (`probes.py`, clone at `/fast/scratch/…/repo`) | pins `f7d6e58d`, `13a9e9e1` | see §4 | 2026-10-28T18:03Z | `probes.json` + `probe-receipts/` |
| 5 | draft proof on a scratch copy of `SCORECARD.md` at the base rev | fixtures `6611552`, `f5c0cdf` | 0 / 1 | 2026-10-28T18:00:07Z | `draft-fixtures.json` |

Run 1 reproduces the claims file's `Before` cell exactly: `failing = ["mismatches 4 != 0",
"corrections 0 < 2"]`, `atoms 50`, `verified 46`, and the four mismatches below.

| mismatch | claimed | derived |
|---|---|---|
| `seats` round 45 (`Wave 1: 40 seats; wave 2: 32 seats`) | `[40, 32]` | `[40, 36]`, dispatch `[40, 36]` |
| `window` round 46 (`0425224..<tip> …`) | — | `unverifiable`: the window names no concrete `A..B` |
| `axes` coverage head | `133/133` | `138/138` |
| `axes` depth head | `20/20` | `23/23` |

Run 2 at the pin is green: `atoms 44`, `verified 43`, `mismatches []`, `corrections 2`,
`corrections_bad []`, `exempted 1` (the round-46 `<tip>` atom), battery
`correction_forgeries 3 / forgeries_green 0`, `met_target true`.

## 2. The draft (verbatim; also `draft-section.md`)

```markdown
## Record corrections — round 47

Append-only repair of the self-assessment atoms `tools/round-47/record.py` re-derives. Each line
below supersedes the atom it names and is itself re-derived by the counter at the measured
revision; the original sentence stays where it was written so the defect stays visible.

- corrects seats round-45: 2 waves, 76 seats total
- corrects window round-46: empty in 332f4884..58eb04b6 -- tools/round-46 plans/round-46-claims.md

The two `## Owned axes` head fractions are re-derived by the same counter and are stated here as
facts, not as exemptions (the `axes` class reads the current table; this section cannot repair it):

- coverage head `138/138` — `git ls-tree -r --name-only <rev> corpus/knowledge | grep -c '\.md$'`
  prints `138`, and the instrument's own `coverage` pair is `(138, 138)`: the `## Coverage map`
  tokens intersected with those stems.
- depth head `24/24` — the `## Queue-drain craft ` body split on `^- **` yields 24 rules and all 24
  carry a resolving file/range citation, so the instrument's `depth` pair is `(24, 24)`. This is
  the only head coupled to another claim: the same derivation reads `SKILL.md`, so block 24 with
  one unresolvable citation reads `23/24` and this row goes red with it.
```

The section that was actually landed (`SCORECARD.md` at `e856beb5` onwards) says the same two
correction lines with a trailing explanation, and adds two `- corrects axes …` lines. Those two
lines are **not parsed at all** — see D2 — so they are prose; the counter reports `corrections 2`,
never 4 (run 2, `receipt-at-pin.json`).

## 3. Per-line proof (each line re-derived, not asserted)

| line | grammar the current parser accepts | derivation I ran | value | where it shows |
|---|---|---|---|---|
| `- corrects seats round-45: 2 waves, 76 seats total` | `^- corrects (seats\|window\|path\|rev) (\S+):\s*(.+)$` (`record.py:50`) then `(\d+) waves?,\s*(\d+) seats total` (`:51`) | `w1-dispatch.json` `counts.spawn 40`, `w2-dispatch.json` `counts.spawn 36` (`receipts.jsonl` rows `seats-round45-w1`, `-w2`) | `len=2`, `sum=76` | `corrections_bad []`; without any in-place repair the atom is `exempted` and nothing else (fixture `f5c0cdf`, `draft-fixtures.json`, `P3`) |
| `- corrects window round-46: empty in 332f4884..58eb04b6 -- tools/round-46 plans/round-46-claims.md` | `empty in ([0-9a-f]{7,40})\.\.([0-9a-f]{7,40})\s+--\s+(.+)$` (`:52`) | `git log --name-status --format= 332f4884..58eb04b6 -- tools/round-46 plans/round-46-claims.md \| wc -l` | `0` (`receipts.jsonl`) | `corrections_bad []`; the alternative `58eb04b6..13a9e9e1` over the same paths is also `0` |
| coverage head `138/138` (fact, not an exemption) | `axes` is **not** in `CORR`; the head is an atom read from `## Owned axes` | `git ls-tree -r --name-only <rev> corpus/knowledge \| grep -c '\.md$'` → `138`; `record.axis_pairs` → `coverage (138, 138)` | `138/138` | `mismatches []` only when the row itself reads `138/138` (P2 exits 0, P3 exits 1) |
| depth head `24/24` (fact, not an exemption) | same `axes` class | craft body split on `^- **` → `24`; `record.axis_pairs` → `depth (24, 24)` at the pin, `(23, 23)` at the base | `24/24` at the pin, `23/23` at the base | P2 (base, `23/23`) exit 0; P1 breaks one citation → `claimed [24,24] derived [23,24]`, exit 1 |

## 4. Fixtures and attacks

All fixtures are one-commit repos on a `--no-hardlinks` clone of the lane; the clone is gone, the
receipts and the two scripts are here (`probes.py`, `driver.py` rebuild every fixture from the
commands recorded in `probes.json`).

| probe | what it changes | exit | signal |
|---|---|---|---|
| `P0` lane card at pin `f7d6e58d` | nothing | 0 | baseline green |
| `P1` block 24's `interpreter_sha256` citation renamed to `tools/round-47/missing.py` | `SKILL.md` | **1** | `mismatches 1 != 0`, `axes depth claimed [24,24] derived [23,24]` |
| `P2` my §2 draft appended + both axis heads repaired in place, base rev | `SCORECARD.md` | 0 | `corrections 2`, `corrections_bad []`, `exempted 1` (seats), battery `3/0` |
| `P3` my §2 draft appended, axis heads untouched | `SCORECARD.md` | **1** | `mismatches 2` (both heads); `exempted 2` — both correction lines fire and bind the atom they name |
| `P4` every atom repaired in place (seats sentence, window sentence, both heads) + the two true corrections | `SCORECARD.md` | 0 | `exempted 0` — two corrections, nothing corrected |
| `P5` the `<tip>` sentence deleted instead of corrected | `SCORECARD.md` | **1** | `no atoms of class(es) ['window']`, `corrections 1 < 2`, battery no-op |
| `P6` a second placeholder `is empty` sentence + one window correction | `SCORECARD.md` | 0 | `exempted 3` — one line silences two placeholders with different windows and paths |
| `P7` `- corrects axes coverage: 999/999` inserted inside the section, pin | `SCORECARD.md` | **0** | the line is invisible: `corrections 2`, `corrections_bad []` |
| `P8` window correction over `corpus/knowledge/2026-10-25-r34b-…md` instead of the round-46 paths | `SCORECARD.md` | **0** | `corrections 3`; the round-46 `<tip>` atom is exempted by a window about a different file |
| `P9` the record's original window concretised: `0425224..58eb04b6` | `SCORECARD.md` | **1** | `corrections_bad [{empty: false, window: 0425224..58eb04b6}]` |
| `P10` `- corrects seats round-46: 2 waves, 79 seats total` | `SCORECARD.md` | **1** | `derived [2,80]`, dispatch `[40,40]` |
| `P11` `- corrects path does/not/exist.md: never` | `SCORECARD.md` | **1** | two `corrections_bad` entries (path absent, atom absent) |
| `P12` `- corrects seats round-44: 2 waves, 79 seats total` (no `## Round 44` heading exists) | `SCORECARD.md` | **0** | `corrections 3`, `corrections_bad []` |

## 5. Findings

**D1 (HIGH) — R47-C2 is not causally separable from R47-C1's landing; the claims file says it is.**
`depth_pair()` reads `SKILL.md`'s `## Queue-drain craft ` body, so the `depth` head is a function of
block 24. Probe `P1`: rename one citation in block 24 and C2 exits 1 with
`claimed [24,24] derived [23,24]` (`probe-receipts/P1-craft-citation-broken.json`). The claims file
(`## Causal separability`) states C2 "never reads the craft section". Command:
`python3 -I -B tools/round-47/record.py --root <fixture> --rev <fixture tip>`.
Landing order matters: block 24 must land (with every citation resolving) before the depth head is
re-measured, or both claims go red together.

**D2 (HIGH) — `axes` corrections are dead code; a false axes statement is accepted silently.**
`CORR` (`record.py:50`) matches only `seats|window|path|rev`, while `corrects()` carries a
`if cls == "axes"` branch that no input can reach. Probe `P7`: `- corrects axes coverage: 999/999`
inserted inside the corrections section at the pin → exit 0, `corrections 2`, `corrections_bad []`.
Consequence: the two `- corrects axes …` lines in the landed section exempt nothing, count for
nothing, and could state any number. Clause 3's sentence "an `axes` correction must state
`<resolved>/<total>`" describes a check that cannot run.

**D3 (HIGH) — a window exemption is not bound to the atom it supersedes.**
`exempt()` returns `True` for any placeholder atom (`pair is None`) as soon as any `window`
correction exists; A1 removed the pair-in-card check and nothing replaced it. Probe `P8`: a window
over `corpus/knowledge/2026-10-25-r34b-…md` (empty, verified) exempts the round-46 `<tip>` claim
about `tools/round-46 plans/round-46-claims.md` → exit 0. Probe `P6`: one line exempts two
placeholders with different windows and paths (cap `exempted 3`). So the correction that supersedes
"the round-46 frozen paths were untouched" need not mention those paths.

**D4 (MED) — "at least two re-derived corrections" does not require correcting anything.**
`P4`: repair every atom in place, then append the two true correction lines → exit 0 with
`exempted 0`. `P12`: `- corrects seats round-44: 2 waves, 79 seats total` — there is no
`## Round 44` heading anywhere in `SCORECARD.md` — is accepted (`corrections 3`, `corrections_bad
[]`) because A3's historical allowance accepts any numeric round below the window. The counter's
only binding constraint is clause 1 `mismatches == []`, which is satisfiable by editing the record
text; clause 3 is documentation. If the L1 wants it load-bearing: require `exempted >= 1`, or
require each correction's key to be the key of an atom the card contains (drop the historical
allowance for rounds with no heading).

**D5 (MED) — the frozen-bytes promise is unenforceable for this counter, and "the freeze" is not
one object.** `plans/round-47-claims.md:11`: "Nothing in this file or in `tools/round-47/` changes
after the freeze: a change makes both counters exit 2 `frozen_path_changed`." `record.py` has no
`--freeze` argument and no freeze arm (`--root --rev --no-battery --selftest --json-out`), so it
cannot return 2 for that reason. Six byte states of `record.py` exist in one round:
`5017e1f7 af666ce2`, `9018c53b 787f909a`, `62e33f7d fb6d5735`, `2e4ae434 8c0abb8b`,
`1e2c3102 c704c3d4`, `07d2894e abf35257`. And `git log --format=%H -1 -- plans/round-47-claims.md`
= `62e33f7d` (A2) while the record declares the freeze A6 `f54b3b6d`; the claims file's own
freeze-derivation command and the declared freeze disagree. Sharpest form: the **frozen** `record.py`
(`af666ce2`, `git show 5017e1f7:tools/round-47/record.py`) scores the landed corrections section
**red** — `corrections_bad [{line: "- corrects window round-46: empty in 332f4884..58eb04b6 …",
detail: "window pair names no atom in scope"}]`, exit 1 — so the C2 verdict at the landing exists
only because a frozen file was edited after the freeze. (The pre-A1 measurement is preserved in
`receipt-at-e856beb5.json`'s history and in `ctl-c2-2-freeze-amendment.json`.)

**D6 (MED) — the round-46 window claim was false, not merely unverifiable.**
`git log --name-status --format= 0425224..58eb04b6 -- tools/round-46 plans/round-46-claims.md`
prints `M tools/round-46/attest.py` and `M tools/round-46/gate.py` (2 lines). Probe `P9` concretises
the placeholder to the section's own measured revision and states the same window in a correction →
exit 1, `{empty: false, window: 0425224..58eb04b6}`. The exemption route (D3) lets that claim be
superseded by an unrelated empty window without anyone stating that it was false; the prose should
say it, because the counter cannot.

**D7 (MED) — the round-47 C2 row misstates its own measurement.** The row reads "over 50 atoms …
exit 0, `atoms 50`, … `exempted 2 <= 3` … measured at `a0753786`". At `a0753786` the counter reports
`sections [round-46, round-47]`, `atoms 42`, `exempted 1`
(`probe-receipts/at-a0753786.json`); `atoms 50` / `exempted 2` are the values at `1e2c310295`, where
the last two sections are `[round-45, round-46]`. The `sections` window moves as soon as the round-47
section is appended, so every figure quoted for this claim must be re-measured at the revision that
contains that section.

**D8 (LOW, already disclosed as A2, independently reproduced)** — at `e856beb5` the
`correction-window-not-empty` forgery replaced the correction's window with `332f4884..<tip>`, which
is empty over those paths, so the "forgery" was a no-op and `forgeries_green` went to 1
(`receipt-at-e856beb5.json`). A2 now forges `root..tip`. Residual: `root..tip` is non-empty for any
path added anywhere in history, so that fixture is red by construction and no longer tests "the
stated window is not empty"; `P9` is the honest version of that attack and it does go red.

**What the counter does well (do not over-correct these):** `P5` refuses repair-by-deletion
(`no atoms of class(es) ['window']`); `P9` refuses a plausible but non-empty window; `P10` refuses a
false seat total (`derived [2,80]`); `P11` refuses a ghost path twice over; the base measurement
reproduces all four values of the claims file's `Before` cell.

## 6. Landing checklist for the L1

1. Land block 24 first, with every citation resolving; re-derive the depth head at the same rev
   (`24/24`, not `24/23` — D1).
2. Append §2 verbatim (append-only: keep the original round-45 and round-46 sentences; the seats
   line exempts the first, the window line the second).
3. Repair the two `## Owned axes` heads in place to `138/138` and `24/24`; they have **no** exemption
   path (P3 exits 1 with only the section appended).
4. Re-run the counting command at the landing rev and quote **that** rev's numbers: `failing []`,
   `corrections 2`, `corrections_bad []`, `exempted <= 3`, `battery.forgeries_green 0`, exit 0
   (D7).
5. Do not add `- corrects axes …` lines expecting them to bind (D2), and do not rely on a window
   correction to say anything about the paths the record names (D3).

## 7. Not run

C1's `exact.py` scoring (not my seat), the `--profile v2` battery, and any network fetch. I did not
edit, stage, commit or revert anything in the lane; `git status --porcelain -- SKILL.md SCORECARD.md
plans tools corpus LOG.md QUALITY.md` was empty after my last run.
