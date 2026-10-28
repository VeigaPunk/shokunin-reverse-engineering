# ConnSiblings — round 47 wave 1 (connector seat)

Lane `kaidoku-shokunin`. Read-only on the lane tree; every write landed inside
`.ufo/waves/round-47/w1/ConnSiblings/`. Scratch `S=/fast/scratch/hyaku/kaidoku-r47/ConnSiblings`
(`HYAKU_SCRATCH`/`TMPDIR` set for every run), removed after the receipts below were copied.
No install, no package-manager transaction, no fleet-repo write, no mutating git verb on the lane.

Base `13a9e9e1f7ca3b95f2cc11f24f69d0d92a21a8a5`. Ticket's freeze
`5017e1f7299c3a812e87e7950148f54313dd279e`. The lane was **live** while I measured: `HEAD` moved
`a631bba0 → 31b092d1 → 09a9f912` during the session and the worktree `SKILL.md`
`interpreter_sha256` changed under me (`dcef54a7…`→`01a4bca7…` between two reads ~90 s apart).
Every receipt below therefore carries the resolved revision it measured, and green C1 fixtures
that were invoked with `--rev HEAD` record `"rev": "HEAD"` (see §6, R-1).

---

## 1. What was measured

Both frozen instruments were executed at the revisions named, plus eight forgery fixtures built
from `git clone --no-hardlinks` of the lane (toplevel asserted equal to the fixture dir before the
first fixture commit, throwaway identity configured **inside** the fixture only).

| run | command | rev | exit | receipt |
|---|---|---|---|---|
| C1 @ ticket freeze | `python3 -I -B tools/round-47/exact.py --root <lane> --freeze 5017e1f7 --rev HEAD` | `31b092d1` | **2** `frozen_path_changed` | `c1-ticket-freeze.json` |
| C1 @ A1 | same, `--freeze 9018c53b` | `31b092d1` | **2** `frozen_path_changed` | `m-9018c53b.json` |
| C1 @ A2 | `--freeze 62e33f7d` | `31b092d1` | **2** | `m-62e33f7d.json` |
| C1 @ A3 | `--freeze 2e4ae434` | `31b092d1` | **2** | `m-2e4ae434.json` |
| C1 @ A4 | `--freeze 1e2c3102` | `31b092d1` | **2** | `m-1e2c3102.json` |
| C1 @ A5 | `--freeze 07d2894e` | `31b092d1` | **2** | `m-07d2894e.json` |
| C1 @ A6 | `--freeze f54b3b6d` | `31b092d1` | **0** (`rule_blocks 24`, `rows 4`, `marker 1`, `failing []`) | `c1-A5.json`, `m-f54b3b6d.json` |
| C2 | `python3 -I -B tools/round-47/record.py --root <lane> --rev HEAD` | `a631bba0` | **0** (`atoms 42`, `verified 41`, `corrections 2`, `exempted 1`) | `c2-A5.json` |

The freeze ratchet is the first finding, already routed as **R47-CL11**: six of the seven
frozen-path commits make the instrument exit 2 at the tip; only `f54b3b6d` (A6) is a usable
`--freeze`. `frozen_path_changed` at the ticket freeze: 3 entries
(`plans/round-47-claims.md`, `tools/round-47/`, `tools/round-47/record.py`).

## 2. C1 clause matrix (rev `31b092d1`, freeze `f54b3b6d`)

| clause | claim | observed | verdict |
|---|---|---|---|
| 1 marker/block/last/title | `marker_occurrences 1`, block is last, title `24. ` | 1 / true / true | **met** |
| 2 header equality | `trigger | v2 hole | v3 arm | exit` | exact | **met** |
| 3 rows / cells / exit ∈ {0,1,2} | 4 rows, 4 cells, exit digit | 4/4/4, all exits `1` | **met but unbound** — F-G1 |
| 4 routed-id cardinality | exactly one id per row, each of the four once | `{R46-CL2:1, CL3:1, CL4:1, CL6:1}` | **met** |
| 5 arm token equality | one of `symbol once digest order` | exact | **met** (membership only — R47-CL6) |
| 6 `mutations_sha256` | digest over the counter's own names + all four names named | `19a2166e…` matches; 4 names present | **met but self-signed** — F-F1 |
| 7 gate flag order | `"-m", "--diff-merges=first-parent"` ×1, reversed ×0 | 1 / 0 | **met textually only** — F-F5 |
| 8 refs + pins | ≥3 selector-carrying, path set validated, round-46 cited, both pins | 9 occurrences / 4 distinct, all resolve, both pins match | **met** (occurrence-counted — R47-CL7) |
| 9 battery | 4 / v2 4 / v3 0 / genuine 1 / crash 0 | exactly that | **met** — and reachable with zero discrimination (F-F1) |

## 3. C2 clause matrix (rev `a631bba0`)

| clause | claim | observed | verdict |
|---|---|---|---|
| 1 mismatches == [] | none disagreeing, none `unverifiable` | `mismatches []` | **met** |
| 2 `classes` covers five | five classes | receipt has **no `classes` key**; it prints `atoms_by_class` | **met functionally, unreadable by the claim's own name** — R-2 |
| 3 `corrections >= 2`, each re-derives; `axes` correction states `<resolved>/<total>` | 2 | `corrections 2`, `corrections_bad []` | **met for 2 of 4 in-card lines** — the two `- corrects axes …` lines are *not parsed at all* (F-F2) |
| 4 `exempted <= 3` | 1 | `exempted 1` | **met**, but a window exemption ignores the round key (F-W1) |
| 5 last two `## Round N` | round-46, round-47 | same | **met** |
| 6 battery 3 forgeries / 0 green | 3 / 0 | 3 / 0 | **met**; the battery forges only *corrections*, never an atom |

## 4. Forgery table — what a forger gets for free

Every row is a one-commit fixture clone; the patch is stated so the L1 can rebuild it.
`P` = path inside the fixture, `→` = replacement.

| id | target clause | patch | counter exit | receipt | status vs routed list |
|---|---|---|---|---|---|
| **F-F1** | C1 cl. 6+9 | `tools/round-47/exact.py`: after `MUTATIONS`, insert `MUTATIONS = [(n, (lambda b, s: (b, {}))) for n, _ in MUTATIONS]`; re-pin block 24's `interpreter_sha256` to the new bytes | **0**, `battery {forgeries_total 4, v2_green 4, v3_green 0, genuine_green 1, crash 0}`, all four fixtures `{"error": "mutation was a no-op"}` | `receipts/c1-noop-battery.json` | **contradicts R47-CL4 as written** |
| **F-F2** | C2 cl. 3 | `SCORECARD.md`: `- corrects axes coverage: 138/138` → `9999/9999`; `- corrects axes depth: 24/24` → `0/0` | **0**, `corrections 2`, `corrections_bad []` | `receipts/c2-axes-corrections-forged.json` | **new** |
| **F-F2b** | C2 cl. 3 | delete both `- corrects axes …` lines | **0**, `corrections 2`, `exempted 1` — identical verdict | `receipts/c2-axes-corrections-deleted.json` | **new** (the lines are dead text) |
| **F-G1** | C1 cl. 3 | block 24: every exit cell `1` → `0` | **0**, `failing []` | `receipts/c1-exit-cells-all-zero.json` | same class as R47-CL10 (confirm) |
| **F-G2** | C1 cl. 8 | `Refs:` line → one citation repeated three times | **0**, `refs 9`, `cited` 4 distinct | `receipts/c1-refs-duplicated.json` | R47-CL7 (confirm) |
| **F-F5** | C1 cl. 7 | `tools/round-46/gate.py`: `history_touched` argv loses `-m --diff-merges=first-parent`; the pair is left once in a comment | **0**, `gate_order_literal 1`, `gate_order_reversed 0`; the merge arm is gone from the code | `receipts/c1-flag-order-comment.json` | **new** |
| **F-W1** | C2 cl. 4 | `SCORECARD.md`: add to the round-47 section ``A fresh placeholder: `git log 1e2c310..<tip> -- tools/round-47/` is empty.`` | **0**, `exempted 2` (both window atoms, both `key 46`), window atoms 3 | `receipts/c2-second-placeholder-window.json` | **new** |
| **F-F3** | C2 instrument | `record.py` `derive()` axes branch → `return True, {}`; card coverage head `138/138` → `7/7` | **0**, `failing []`, battery still 3/0 | `receipts/c2-tampered-derive.json` | **new** (C2 has no freeze argument at all) |

### The five that are new, stated as contradictions

1. **F-F1 breaks R47-CL4's stated consequence.** The routed defect says a name-preserving body edit is
   "invisible to the pin, though the battery's `v2_green` count would move" — implying detection.
   It moves **up**: `run_battery` (`exact.py:365-371`) counts a no-op mutation as `forgeries_total += 1`
   **and** `v2_green += 1` and `continue`s, so a fully gutted battery prints `4 / 4 / 0 / 1 / 0`,
   every clause green, exit 0. The pin over *names* plus a battery that scores an unrun mutation as a
   measured hole compose into a green counter that discriminates nothing.
2. **F-F2 / F-F2b: `CORR` cannot parse the class the claim governs.**
   `CORR = r"^- corrects (seats|window|path|rev) (\S+):"` (`record.py:50`) omits `axes`, while
   `corrects()` has an `axes` branch (`record.py:280-289`) and a *second, dead* copy of the same branch
   inside it (`record.py:292-298`, references an undefined `atom`) — the branch is unreachable from
   the parser and the copy is unreachable from anything. Consequence: the two `- corrects axes …` lines the
   landed card already carries are **prose**, not claims; falsifying them (9999/9999, 0/0) leaves the
   counter green, and deleting them leaves it green with `corrections 2` — the axes atoms re-derive
   on their own (`axes 2` verified). Clause 3's sentence "an `axes` correction must state
   `<resolved>/<total>`" describes a check no input can reach.
3. **F-F5: clause 7 binds a string, not an argv.** The literal is required once and the reversed pair
   zero times anywhere in `gate.py`; moved into a comment and removed from `history_touched`, the
   clause is green and the merge-resolution arm (the whole point of R46-CL6) is gone. A containment
   test over the file's text, in the block whose first row is "an equality, not a containment".
4. **F-W1: a window exemption is key-blind.** `exempt()` returns `True` for any `window` atom whose
   `pair` is `None` without comparing the round key, so one `- corrects window round-46: …` line
   exempts a placeholder window the round-47 section adds later. The record can keep growing
   unverifiable window claims until `exempted` hits 3.
5. **F-F3: C2 has no freeze clause at all.** `plans/round-47-claims.md:11` states "a change makes
   **both** counters exit 2 `frozen_path_changed`". `record.py` accepts no `--freeze`, never calls
   `gate.freeze_state` (the string does not occur in the file), and exits 0 after four post-freeze
   commits rewrote its own bytes — and again after a fifth commit taught `derive()` to trust its
   `axes` atoms while the card's coverage head read `7/7`. R47-CL11 covers the *stale declared freeze*
   (C1's side); this is the other half: on C2 the freeze arm does not exist, so the sentence is false
   for one of the two counters it names.

## 5. Overlap: sibling lanes and the lane's own prior art

Searched read-only: `grep -rEn 'exactness-table|interpreter_sha256|frozen_path_changed|freeze_state|
mutations_sha256|corrects (seats|window|path|rev|axes)|^- corrects '` across
`/home/vgpnk/Projects/shokunin/*-shokunin/` (excluding `.git`, `.ufo`, `__pycache__`).

| surface | fleet hits | verdict |
|---|---|---|
| `- corrects <class> <key>:` grammar | **kaidoku only** (SCORECARD 3669-3677 + record.py) | unique; nothing to retire |
| `exactness-table`, `mutations_sha256`, `interpreter_sha256`, `freeze_state`, `frozen_path_changed` | **kaidoku only** (4 / 16 / 7 / 8 / 238 lines) | unique instrument family |
| record-vs-repo reconciliation | `kama-shokunin/tools/round41-scorecard-reconcile.py` (SCORECARD `## Axes`: HASH/LINES/RUN/PATH facts, `hollow` rows), `round42-selfdesc-reconcile.py` (banner, Planned, Retired, Capabilities, README, PROVINCE), `chousa-shokunin/tools/store-record-audit.py` ("judge the capture store and the fetch record as ONE evidence set") | **adjacent, no code duplication** — cite, do not reinvent |
| digest / freeze / append-only auditors | `kama-shokunin/tools/round42-digest-audit.py`, `round41-pinwatch-audit.py`, `manifest-crosscheck.py`, `append-only-audit.py`, `gate-registry-check.py`, `citation-provenance.py` | present; only the first two were read at docstring level |
| post-freeze correction practice | `revenger-shokunin/reports/round-71/post-freeze-corrections.md` (append-only post-freeze correction of `used-by`/`format-layout`), `chousa-shokunin/SCORECARD.md:1591,1676,1715` ("This corrects …") | prior art for the *narrative* half of C2 |

**The overlap that matters is in-lane, and it contradicts the claim.** R47-C2's *Prior state* says
"the lane had no command that could have caught any of them: every counting command the lane owns
reads the artefact, none reads the record." That is false against `tools/`:

- `tools/round-36/c2-counter.py` — "the SCORECARD `## Owned axes` rows, the SCORECARD `## Capabilities`
  table rows and the SHONEN.md boxes … carry zero mismatches with observed repo state".
- `tools/round-38/c2-counter.py` — the same, plus `PROVINCE.md` Core/Frontier.
- `tools/round-44/c2-counter.py` — a frozen rubric re-derived, **with a freeze-integrity walk**,
  `expected_edit` blob equality, and the rule "A NOTE IS NEVER EVIDENCE".

So C2 is not a new capability but a re-derivation with a narrower scope, and it is a **regression**
against round 44 on exactly the clause it lacks: `record.py` takes no `--freeze` and never calls
`gate.freeze_state`, which is why F-F3 is free. The honest landing sentence is "re-derives a
*narrower* atom set than R36/R38/R44 with append-only corrections", not "the lane had no command".

**Should the lane cite rather than reinvent? For round 47: cite, do not absorb.** The fleet tools
solve different populations (kama `## Axes` fact grammar, chousa capture store) and importing them
would widen C2's scope mid-round and break causal separability. The citation belongs in two places:
(a) the R47-C2 prior-state sentence, corrected against `tools/round-36|38|44/c2-counter.py`;
(b) round 48's extension, which should adopt kama's `hollow`-row test (a row with zero HASH and zero
RUN facts) and R44's freeze walk rather than invent a second dialect.

## 6. Receipt-quality observations (no action this round)

- **R-1.** `exact.py` writes the `--rev` *argument* into `counter/rev` (`"rev": "HEAD"`), while
  `freeze_state` resolves the tip into `freeze`. A green receipt therefore need not name the commit
  it measured; only the lane's habit of passing full SHAs keeps `l1/scores/*` self-locating.
- **R-2.** The claims' clause 2 names a receipt field `classes`; the counter emits `atoms_by_class`.
  A reviewer reading the claim looks for a key that never exists — the same claims↔receipt drift the
  round exists to remove.
- **R-3.** `containment` vs `equality` is enforced on the artefact (`SKILL.md`) and not on the
  instrument's own proof surface: clause 7 is a `str.count` over `gate.py`, clause 6 a digest over
  names. Both are containments inside a rule block titled "an equality, not a containment".

## 7. One bounded move

**M-ConnSiblings-1 — the corrections section states its own parsed grammar, and carries only lines in it.**

Two atomic edits to `SCORECARD.md` `## Record corrections — round 47`. No frozen byte, no
`SKILL.md` change, no counter change, no new file:

1. Re-prefix the two `- corrects axes …` lines as plain prose — `- repaired axes coverage: 138/138 — …`
   / `- repaired axes depth: 24/24 — …` — keeping the sentence, the derived value and the receipt
   pointer, and removing only the machine-claim prefix `CORR` cannot parse.
2. Add one sentence under the section heading:
   "`tools/round-47/record.py` re-derives `- corrects seats|window|path|rev …`; an `axes` repair is
   carried by the `## Owned axes` head itself, never by an exemption line (R47-CL12)."

**Affected axes.** calibration only. Depth is untouched: block 24, its four rows, both pins and all
citations stay byte-identical, so command A keeps `rule_blocks 24` / `citation_resolved_rules 24`
(the M47-6 trap is not re-entered). Calibration improves in the only way this round can still
improve it — the record stops carrying syntax that reads as machine-checked and is invisible to the
counter, and it names the grammar it does carry.

**Second-order effects.**
- *Runtime*: `record.py` verdict unchanged — `corrections 2` (still `>= CORR_MIN`), `corrections_bad []`,
  `exempted 1`, `mismatches []`, exit 0. Verified pre/post: F-F2b already runs the post state.
- *Contract*: no clause, threshold or kill rule moves; `exempted <= 3` unchanged; clause 3's `axes`
  sentence becomes honestly unexercised instead of silently unsatisfiable.
- *Substrate*: the two correction lines currently imply the axes heads were repaired by exemption;
  they were repaired in the rows themselves (F-F2b, `axes 2` verified). The prose form keeps the
  history and drops the false implication.
- *Verification*: the edit is diff-visible in one hunk and re-measured by the same command the claims
  already name.

**Risks.**
1. A reader may think the axes repairs were withdrawn → keep the sentence, value and receipt pointer;
   only the prefix changes.
2. `CORR_MIN = 2` becomes exactly met. R47-CL3 already routes the floor; disclose in the same edit
   rather than letting a later reader discover it.
3. This does **not** repair the `CORR` regex, and deleting the instances could normalize the gap.
   Mitigation is the sentence's R47-CL12 reference plus a `corpus/QUALITY.md` row; a regex fix is a
   frozen-byte change and belongs to round 48.
4. It leaves F-F1, F-F3, F-F5 and F-W1 open. They are counter/claims defects, not record defects;
   each is named above with a receipt and a rebuildable patch, and none is folded into this move.

**Verification the L1 runs after landing.**

```sh
python3 -I -B tools/round-47/record.py --root <lane> --rev <landing> --json-out <out>
# expect exit 0, corrections 2, corrections_bad [], exempted 1, mismatches []
python3 -I -B tools/round-47/exact.py  --root <lane> --freeze f54b3b6d --rev <landing> --json-out <out>
# expect exit 0, failing [] (depth untouched)
git -C <lane> diff -- SCORECARD.md    # 2 prefix edits + 1 added sentence, nothing else
```
Negative control for the reason the lines move: re-add `- corrects axes depth: 0/0`, rerun
`record.py`; it must still exit 0 (`corrections 2`) — which is precisely why the line must not wear
a `corrects` prefix.

## 8. Not run (honest list)

- `exact.py --selftest` (16 cases) and `record.py --selftest` — not run; the claims cite their own.
- `--profile v2 --no-battery` (the `ctl-c1-1-v2-profile` control) — not run.
- kama/chousa/revenger counters beyond docstrings — not executed; no sibling lane was measured.
- No `git add/commit/checkout` outside fixture clones; no `pacman`/`uv`/`npx` install was needed, so
  none was made.

## Receipts

`receipts/` in this directory holds the eight forgery receipts (`sha256` below) plus the direct-run
receipts `c1-ticket-freeze.json`, `c1-A1.json`, `c1-A5.json`, `m-<freeze>.json` (×6), `c2-A5.json`.
Fixture clones are ephemeral and were removed with the scratch root; the patch column in §4 is the
rebuild recipe.

```
9c2661e8a707494c023600c6a3fa2921ba892a25b61bc1251ba3268846f82bb6  c1-noop-battery.json
caa35d8dcb4d08200eda9f6a1912bc11bc9e7bf79eb371b8f44468e56a3db9a1  c2-axes-corrections-forged.json
f3458dc2e78049f165d0d6eebcb62445044a56af5a6bdbf30163048f7841e90d  c2-axes-corrections-deleted.json
ace0b788d2e2ce8a81c2a7b6eddc531f0d09ee44a5d25429f37047de69999d75  c1-exit-cells-all-zero.json
d005ec93b436821bbcc6800fad6afad806fc8d6fa417778d9a2bb36ca88feb30  c1-refs-duplicated.json
8038b761650be2088991e05c618c90201953cb0dbde1b78afe29713c8962b8cb  c1-flag-order-comment.json
04ed24c2c3a08d29cf5ad0dcaf17a31a69e848dd74ef3ec1402433a839cae740  c2-second-placeholder-window.json
585f09022e27f5355d0c78e57202afcf8a38d474d532cc9aff796dfac7cdca0d  c2-tampered-derive.json
```
