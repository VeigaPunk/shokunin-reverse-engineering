# R45W1CritC1 — R45-C1 falsification before data

Seat: critic (`R45W1CritC1`), round 45 wave 1. Lane root
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Freeze
`f762b7273e3f6ca3c710bb37d5de92a4a4417aec`; scored revision `faa875bc0eb839d15b83c4afa6078819e5a7b381` (HEAD at review).
Instrument under attack: `tools/round-45/c1-counter.py` sha256
`2cfc5a4853585879b0924f4c002ed4581dced02f061068d325c2cd3da130a509` (byte-identical scratch copy;
`preflight-real.py` = `633ebc058f0ea5a7c6dec4a9d6287e062eecf497fb6da674a3898c7c7130523b`).
Toolchain: Python 3.14.8, git 2.56.0. No installs or upgrades were made.

## Verdict in one paragraph

The **landed artefact at HEAD is genuine** — I read it: block 22 carries ten real rows whose arms match
the interpreter's five declared arms, and the real interpreter's `--selftest` builds eleven git fixtures
whose red cases are real (`c1-counter.py` exit 0, `cases=11 failures=0`, receipt sha256
`0c83a7b3…`). But the **predicate is not a discriminator**. Ten distinct forgery fixtures score
`met_target: true`, including one 44-line artefact with garbage rows, four one-line citations and a
four-line stub interpreter that prints `PREFLIGHT_SELFTEST: cases=11 failures=0`. So `failing == []`
is a *presence* check on markup, never evidence that the depth work was done. The claim file's
predicate section should say this; the graded block already does (SKILL.md:587-589). One clause
(crash → exit 1 instead of 2) is also semantically dishonest against the exit-code contract.

## Attacks (each = {attack, expected if the predicate were sound, observed})

Fixtures are private git repos under `$S=/fast/scratch/hyaku/kaidoku-r45/R45W1CritC1`; every run is
`python3 -I -B <frozen counter copy> --root <fixture> --freeze <root commit> --rev <tip>`. Receipts,
with stdout sha256 and UTC, are in `receipts.json` next to this report.

| # | attack | expected if sound | observed | verdict |
|---|---|---|---|---|
| 1 | do-nothing SKILL.md: 21 plain bullets, no marker, real interpreter | exit 1 | **exit 1**, `rule_blocks 21 != 22`, `block22_present 0`, `rows 0`, `refs 0` | **sound** |
| 1b | do-nothing on the *real* lane (freeze..freeze) | exit 1 | **exit 1**, identical failing list | **sound** |
| 2 | eight dataframe rows of garbage (`\| lorem i \| ipsum \| i%3 \| dolor \|`) under a correct header, four line-less citations, real interpreter | exit 1 | **exit 0**, `met_target true`, rows 8, refs 4, selftest ok | **UNSOUND** |
| 3a | 19 real rules + marker block labelled **"7."** + two unrelated `- **scratch note.**` bullets = 22 blocks | exit 1 (not block 22, and two "rules" are not rules) | **exit 0** | **UNSOUND** |
| 3b | correct row count, header `\| triggered \| harm \| exits \| receipts \|` | exit 1 (columns are not trigger/arm/exit/receipt) | **exit 0**, `header_ok true` | **UNSOUND** |
| 3c | 22 genuine rules + a genuine block → 23 `- **` bullets | exit 0 | **exit 1**, `rule_blocks 23 != 22` | **false negative**: any unrelated bullet, or a `###` subheading bullet inside craft, fails a real block |
| 4 | four refs that resolve but are off-topic (`…core.md:1-2`, `round-44.md:1`, `…spotcheck.md:39`, `claims.md:2-3`) | exit 1 (nothing about freeze integrity) | **exit 0**, `unresolved []`, refs 4 | **UNSOUND** |
| 4b | four self-citations: `plans/round-45-claims.md:1..4` | exit 1 (provenance loop, not evidence) | **exit 0**, refs 4 | **UNSOUND** |
| 4c | bare paths with **no line selector at all** (attack-2 fixture) | exit 1 ("located citations") | **exit 0**, refs 4 | **UNSOUND**: claim text "located citations" is not enforced |
| 5 | interpreter = 4-line stub printing `PREFLIGHT_SELFTEST: cases=11 failures=0`, exit 0 | exit 1 (no arms exist) | **exit 0**, `selftest {cases:11, failures:0, ok:true}` | **UNSOUND** |
| 6 | **cheapest green**: 21 plain bullets + garbage block + four `:1` refs + stub interpreter | exit 1 | **exit 0** | **the scoring artefact** |
| 7 | marker twice inside one block | exit 1 (docstring: marker "exactly once") | **exit 0**, `block22_present 1` | minor: counts blocks, not occurrences |
| 8 | header cell `\| trigger \| arm \| no-exit-code \| receipt \|` + garbage rows | exit 1 | **exit 0** (`"exit" in "no-exit-code"`) | **UNSOUND** |
| 9 | refs live only inside table cells, one per row | exit 1 (cells are not citations) | **exit 0**, refs 8 | minor |
| 10 | frozen path touched *only* by an evil merge commit (append to both frozen paths during `--no-commit`) | exit 2 | **exit 2**, `frozen_path_changed: [claims.md, preflight.py]` | **sound** (strongest merge counterexample I could build; the arm holds) |
| 11 | SKILL.md heading written `## Queue-drain craft` (no trailing space) | exit 2 (could-not-evaluate) | **exit 1**, IndexError, **empty stdout** | **UNSOUND exit semantics** |

## Cheapest artefact that scores green

`$S/fx-a6-cheapest-green` — **44 lines, zero freeze-integrity content**, exit 0
(`met_target: true`, receipt sha256 `34336cf7…`, UTC 2026-10-28T15:42:01Z):

```
- **22. Freeze integrity.** <!-- freeze-integrity-table v1 --> S140 tools/round-45/frozen-path-preflight.py

| trigger | arm | exit | receipt |
|---|---|---|---|
| lorem 0 | ipsum | 0 | dolor |          … 8 rows, exit cells cycling 0,1,2
  Refs: corpus/lessons/round-44.md:1, plans/round-45-claims.md:1, …(2 more):1
```
plus a 4-line `tools/round-45/frozen-path-preflight.py` that prints
`PREFLIGHT_SELFTEST: cases=11 failures=0` and exits 0.

Every clause is satisfied by *shape*: `rule_blocks` counts `^- \*\*`; `block_table` takes any
`|`-prefixed lines; `exit_col` is `next(h for h in header if "exit" in h)`; `header_ok` is substring
membership; `REF` accepts a bare path with no line; `run_preflight` parses one printed line.

The frozen-path arm does not close this hole: it only forbids *changing* `tools/round-45/` after the
freeze, so a content-free freeze passes forever. That is exactly the failure mode of a freeze created
from a forged artefact, and the real freeze was itself created in the same way.

## Why this is a predicate defect, not a landed-artefact defect

- The real block's rows are semantic and map to the interpreter's arms
  (`commit`/`restored`/`blob`/`dirty`/`pathspec`), and the real selftest has one red case per arm
  (`frozen-path-preflight.py:265-275`: `red-touched`, `red-restored`, `red-dirty`,
  `red-dirfreeze-no-pathspec`, `red-unknown-freeze`, `red-nonancestor`, `red-bulk-sweep`).
- The counter's **own golden case uses the stub**: `STUB_OK` (`c1-counter.py:251-253`) is what
  `green()` (`:274-276`) is scored against. The instrument's canonical green fixture *is* the
  forgery, so its own `--selftest` cannot demonstrate the binding.
- The graded surface already states the limit (SKILL.md:587-589): "this instrument's 'actionable
  table' test is structural … a table of structurally valid but empty rows would pass it."
  That disclosure is honest and should be cited by the landing. It does **not** reach the claims
  file, whose "Satisfiability preflight" says "provenance is stated as exact path equality, never as
  'names a path'" — attack 4c shows a *line-less* path satisfies the citation clause, and 4b shows a
  self-citation to the claims file does too. One of the real block's own seven refs is off-topic
  (`corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md:40-66` is about SONAME
  content multisets, not freeze integrity), which the counter accepts by design.

## Impacted axes

- **depth (the claim's own axis)**: the score certifies the presence of a marker, a header and eight
  pipe-lines, not a decision table. A depth row landed on this evidence is over-credited unless the
  report states the structural limit in the same breath.
- **calibration**: `crash → exit 1` (attack 11) breaks the contract that a 2 means
  could-not-evaluate; a scorer keyed on exit codes reads a broken instrument as "claim not met", and
  a scorer keyed on `met_target` gets an empty stdout. `craft_blocks` (`c1-counter.py:59-61`) indexes
  `split(...)[1]` with no guard.
- **provenance**: four refs can be four lines of `plans/round-45-claims.md`; refs need not be
  located at all.

## Smallest safe correction (for a *new* freeze — do not edit the frozen bytes)

One clause kills attacks 5 and 6 and costs ~10 lines: in `run_preflight`, keep the parsed JSON
selftest lines and require the seven named red cases to appear with `"ok": true`
(`red-touched`, `red-restored`, `red-dirty`, `red-dirfreeze-no-pathspec`, `red-unknown-freeze`,
`red-nonancestor`, `red-bulk-sweep`). A stub that prints one summary line then fails.

Two optional one-liners, both satisfied by the real artefact and neither by the forgeries:
(1) require `0`, `1` and `2` to each appear in the exit column and every `arm` cell to contain one of
the interpreter's declared arm tokens (kills 2/3b/8); (2) require every counted ref to carry an
explicit `:line` (kills 4c/4b). Wrap `craft_blocks` in `try/except` returning 2 (kills 11).

Because `tools/round-45/` is a frozen directory pathspec, any of these makes the current counters exit
2 `frozen_path_changed`; they are a round-46 instrument, not a wave-1 edit.

## Not run / limits

- I did not score C2; another seat owns it.
- I did not test a *renamed* frozen directory, a submodule, or a shallow/replace-object history.
- Merge-commit blindness was my strongest structural hypothesis against the freeze arm; the fixture
  refuted it (attack 10 → exit 2), so I report no defect there.
- All fixtures are private repos under `$S` with local throwaway identity; no git mutation was run in
  the lane tree, which stayed read-only (`git log` over `FREEZE..HEAD -- plans/round-45-claims.md
  tools/round-45/` printed nothing, i.e. the frozen bytes are untouched).

## Receipts

| label | exit | stdout sha256 | UTC |
|---|---|---|---|
| fx-a1-do-nothing | 1 | `46a7bb868437ed7f8526b9ca6bfe5b6d4fc76d8b9b4fbadb2297c146b9d45057` | 2026-10-28T15:41:59Z |
| fx-a2-garbage-rows | 0 | `2c34c9a56f1355e363ff90085c3595bfec4e691d9ae0f1bbcfe193c4aea0e7b9` | 2026-10-28T15:41:59Z |
| fx-a3a-unrelated-bullets (23) | 1 | `79c985ff2de7fb7b37c3ba09fc5cc15f2f348f5b8119d1352aee6d698b055d82` | 2026-10-28T15:42:00Z |
| fx-a3b-header-substring | 0 | `b8b13f73623e324dbc24479f73456a525279bd5d2600dca43b103a8fde0c6837` | 2026-10-28T15:42:00Z |
| fx-a3c-inflated-denominator | 1 | `c1087a96e6aab4ff9ead6f98002916a11f5c45f18293053287aacf22dee83801` | 2026-10-28T15:42:01Z |
| fx-a4-irrelevant-refs | 0 | `c72562135b83b32e85ad01078d2fb2187004b0708fda8f3e10dbe9d7d15ea1f3` | 2026-10-28T15:42:01Z |
| fx-a4b-self-citation | 0 | `b9059bac601dc43984542ba3019238d2a8829cb0fc1c467b852e098c401656b2` | 2026-10-28T15:42:01Z |
| fx-a5-stub-interpreter | 0 | `f1827de02af576ec16d55a4b2c6b0dd8da795b8df8f6370137d12980df128839` | 2026-10-28T15:42:01Z |
| **fx-a6-cheapest-green** | **0** | `34336cf79d729e6a85a3ac7a3eda998388011213f33aaa1cba2d8187fcefc7d3` | 2026-10-28T15:42:01Z |
| fx-a7-evil-merge | 2 | `7b7104bc23f7e63d80e1c4b6ac13614a71286896fe7b19458908ed82e2ea3efe` | 2026-10-28T15:42:02Z |
| fx-a8-heading-crash | 1 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (empty) | 2026-10-28T15:42:02Z |
| fx2-a10-marker-twice | 0 | `d3687127c4556bcf406bc36278caccf340f2610c09509f202a0632ced060274b` | 2026-10-28T15:42:02Z |
| fx2-a12-header-no-exit-code | 0 | `ca3dabc2d3ba3a5e0bde3edae96da299f5c6f93f5d83780781a1c22cc6716444` | 2026-10-28T15:42:02Z |
| fx2-a13-refs-inside-cells | 0 | `ff945e03eab722f5c448525c321409e1a225622130d65f5e19f31833f21445fd` | 2026-10-28T15:42:03Z |
| fx2-a3a-unrelated-bullets-22 | 0 | `6354bed5ed7517d8561ac4dcc736febb76134e097005894acfa42a07c2abb3d7` | 2026-10-28T15:42:03Z |
| real-freeze-do-nothing | 1 | `e2731609959b489750a703fc12a5605ad4538395c5f808424e142dfff41fb4e1` | 2026-10-28T15:42:03Z |
| real-head | 0 | `0c83a7b3fc340e8f65f6d052b5d1b2905e6e1e4bf4d836788e3257394226ce14` | 2026-10-28T15:42:04Z |
| counter-selftest | 0 | `296734f224877a86e8d216bcde5382bbe0f18ff1dadddb1d18099f3754fdac6d` | 2026-10-28T15:42:04Z |

Harness digests: `attacks.py` `1e5c9ce9…`, `receipts.py` `56dc113f…`. `receipts.json` holds the exact
command line, cwd, exit, stdout sha256, stderr sha256 and UTC for every row above.
