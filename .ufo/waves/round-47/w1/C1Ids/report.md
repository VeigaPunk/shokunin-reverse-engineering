# Seat C1Ids — R47-C1 clause 4 (routed-id cardinality) on the frozen counter

Lane `kaidoku-shokunin`, round 47 wave 1. Freeze `5017e1f7299c3a812e87e7950148f54313dd279e`,
base `13a9e9e1f7ca3b95f2cc11f24f69d0d92a21a8a5`, measured lane revision
`3186f69b49798f2cc05727bbfd1604505fcee03b`. Read-only on the lane tree: `SKILL.md`, `plans/`,
`tools/`, `corpus/` were read, never written; every candidate block was scored inside a
one-commit fixture repo under `/fast/scratch/hyaku/kaidoku-r47/C1Ids/fx/` (removed with the
scratch root after the receipts below were copied out). No installs, no package operations.

**Verdict on the clause.** Clause 4 is implemented exactly as the claims file states it and it
fires on every cardinality defect I could construct — three forgeries red with clause-4
messages, a block that satisfies it green, and a block that breaks only the clauses *after*
it keeps clause 4 green. It is also **not sufficient for the defect it claims to close**:
three forgeries that keep the id multiset correct while pairing ids with the wrong holes (the
worst: four distinct ids, four distinct arm tokens, one hole repeated four times) score
`met_target: true`, exit 0, with the four-forgery battery still 4/4/0. Details in §3.

## 1. Runs retained

Freeze and measured-revision runs (the commands the L1 will re-run):

| run | command | exit | stdout sha256 | when |
|---|---|---|---|---|
| freeze | `exact.py --root <lane> --freeze 5017e1f… --rev 5017e1f… --json-out .ufo/waves/round-47/w1/C1Ids/receipts/freeze-run.json` | 1 | `88fafc603579d0e32679d6df708f92a471c2be5fbe154884937ac556054f28ba` | 2026-10-28 14:48 -0300 (17:48Z), file mtime |
| committed tip | same with `--rev 3186f69b…` → `receipts/head-commit-run.json` | 1 | `01078be64033e0fde024054dc1dd8df4e061613fe3d91a5f56dc6c256f7b64f0` | 2026-10-28 14:49 -0300 (17:49Z), file mtime |

Both exit 1 with `block_present 0`, `rule_blocks 23`, `marker_occurrences 0`, `failing` =
`["marker_occurrences 0 != 1", "marker_block_count 0 != 1"]`, `frozen_path_changed []`,
`touched 0`. At neither revision does a committed tree carry block 24:
`git show 3186f69b:SKILL.md | grep -c 'exactness-table v3'` = `0` and the craft section has 23
blocks; the block that exists in the worktree is uncommitted (`git status --porcelain SKILL.md`
→ ` M SKILL.md`). The `failing` list above is short because `score()` returns at the marker
gate (`exact.py:186-188`), not because clauses 2–9 pass.

Fixture grid, `--profile v3`, `freeze == rev == <fixture commit>`, one commit per case
(receipt `receipts/clause4-v3.json`, 12 cases):

| case | exit | utc | stdout sha256 | fixture rev |
|---|---|---|---|---|
| `full` | 0 | 2026-10-28T17:53:11Z | `4dfa6eb280d28947398ff06e678f299d90b9acff68bfddb86703b862ccfa6022` | `f0f292f4ae4c` |
| `partial-header-digest-ref` | 1 | 2026-10-28T17:53:11Z | `48662468f8e4b22579b55c5d85853c6f56c76410ef2d6e9d7e340b730753f0fa` | `47bda1e14c3c` |
| `dup-id` | 1 | 2026-10-28T17:53:11Z | `67bedf2b4e33a6c6e302a45d9010bcdfa92e1c91fa8cc39a432e1e5d822a7369` | `42bcf4bd96e6` |
| `multi-id-cell` | 1 | 2026-10-28T17:53:12Z | `825e345cc356ff59d5bab6f8cc30aa28574c3e5a973201dc56cc12f8345cee93` | `9f67cf75aaac` |
| `id-in-hole-cell` | 1 | 2026-10-28T17:53:12Z | `d64b3983dd296f1f15d823c867cb3044ebc7163c1b72e5a99f359f19baf54c0a` | `f80ab983927c` |
| `permute-ids` | 0 | 2026-10-28T17:53:12Z | `ca2c8c767ed71a6058bb2aae566390530f73c5841fd885936c3848c497eb876f` | `3b524c265b6d` |
| `copyrow` | 0 | 2026-10-28T17:53:12Z | `7c501600fd6b17c74330c70a2108ba983b1985cc7040faace51db272caf17f1b` | `16e96b2b61c9` |
| `dup-arm` | 0 | 2026-10-28T17:53:12Z | `64da1f37c73f6439ecce6563e163809f253d9b695c488ed5fca4204ac5484866` | `518252475214` |
| `one-hole-four-ids` | 0 | 2026-10-28T17:53:13Z | `277da3fba66bbc58085ff03225e8157a387295e80d6891af8380e3a6a1439d42` | `bea7ccea7adc` |
| `cite-gate46` | 1 | 2026-10-28T17:53:13Z | `4b3764e7f7d71546ec10696348470eb9e865adb7a7db365af5930bcc4eb256ad` | `3a7a76fe1115` |
| `landed-worktree-draft` | 0 | 2026-10-28T17:53:13Z | `7e48bf5af514b29dc08d020a14b3f14f404136cf5b62f3a67f149539b804b32e` | `839a1df90999` |
| `landed-draft-plus-rows` | 0 | 2026-10-28T17:53:13Z | `271318260d602c190db210c6f744f6da2fa247838c6f1ba85206b27414a53bf2` | `374a849fe13b` |

Same fixtures under `--profile v2` (receipt `receipts/clause4-v2.json`):

| case | exit | utc | stdout sha256 | `failing` |
|---|---|---|---|---|
| `dup-id` (v2) | 1 | 2026-10-28T17:52:25Z | `9bb829d3832764857e6041b7627bf4f5f439d8dfc676d8d8637936ca57aea371` | `routed ids not named by any row: ['R46-CL3']` |
| `multi-id-cell` (v2) | 1 | 2026-10-28T17:52:25Z | `7fb7df820bbfe306be32c0e8336284a399d0c14cc0567a652d1a14204947ca7c` | `battery genuine_green 0 != 1` |
| `id-in-hole-cell` (v2) | 1 | 2026-10-28T17:52:25Z | `ae502d00a43d6739b6ec71af3a054ce23cd812524e0ff3fbaf1e51fcf418afc2` | `routed ids not named by any row: ['R46-CL3']` |
| `permute-ids` (v2) | 0 | 2026-10-28T17:52:25Z | `3e201fed947571dee54e530169034f139599b1d227bfd695e317f6777eb56a5c` | `[]` |
| `landed-worktree-draft` (v2) | 0 | 2026-10-28T17:52:26Z | `b49a99da3cd60322ddca02362c77128be0f995ef2261b56311e778b86ff911bd` | `[]` |

Each receipt line carries the exact `cmd`, `exit`, `utc`, `stdout_sha256`, `block_sha256`,
`skill_sha256` and the counter's whole JSON. The driver that rebuilds every fixture from
`git show 3186f69b:…` is at `receipts/drive.py` / `receipts/drive-v2.py`.

## 2. Clause 4 holds where it is tested

- **It fires.** `dup-id` → `routed cardinality {'R46-CL2': 2, 'R46-CL4': 1, 'R46-CL6': 1} != each of ['R46-CL2', 'R46-CL3', 'R46-CL4', 'R46-CL6'] exactly once`. `multi-id-cell` → `rows naming != 1 routed id: [1]` plus the cardinality message. `id-in-hole-cell` (id printed in the v2-hole cell instead of the trigger cell) → `rows naming != 1 routed id: [1]`. Exit 1 in each, as the claim requires.
- **It is satisfied by a block that satisfies it.** `full`: exit 0, `routed_counts {CL2:1, CL3:1, CL4:1, CL6:1}`, `arm_tokens ["symbol","once","digest","order"]`, battery `forgeries_total 4 / v2_green 4 / v3_green 0 / genuine_green 1 / crash 0`.
- **It is independent of the rest.** `partial-header-digest-ref` keeps correct trigger cells and breaks the header (clause 2), the digest pin (clause 6) and the citation set (clause 8): `failing` = those three messages only, in that order, with no clause-4 message and `routed_counts` intact. This is the "failing list shrinks to the other clauses" check: clause 4 contributes nothing to that list.
- **The claim text and the code agree** on the two things the clause states. Two things it does not state and I verified by reading the code: the id scan is `r[0]` only (an id in the hole or arm cell is invisible), and `R46-CL\d+` is greedy so `R46-CL20` fails the multiset rather than aliasing onto `R46-CL2`.

## 3. Where clause 4 is falsifiable — three green forgeries

All three are `exit 0`, `met_target true`, battery 4/4/0 (`receipts/clause4-v3.json`):

1. **`permute-ids`** — the `R46-CL2` and `R46-CL3` trigger ids exchanged between their rows,
   every hole and arm left in place. The multiset over trigger cells is identical, so the
   table now says `R46-CL2` beside `R46-CL3`'s hole. `routed_counts` is `{CL2:1, CL3:1,
   CL4:1, CL6:1}`; `failing []`.
2. **`copyrow`** — rows 2–4 are row 1's hole and arm with trigger ids `CL3/CL4/CL6`
   (`arm_tokens ["symbol","symbol","symbol","symbol"]`). Green in v3 **and** in v2.
3. **`one-hole-four-ids`** — the sharpest: four distinct ids, four distinct arm tokens
   `symbol/once/digest/order`, and **all four v2-hole cells are R46-CL2's hole**. One defect
   described four times, every token the claim names present, exit 0.

`dup-arm` (correct ids, arms `order`×4) is also exit 0 and that is consistent with the frozen
text — the claim requires each arm cell to be *one token of* the vocabulary, not a distinct
one. Taken with the three above, the block-24 table has no pairing constraint at all: neither
id→hole nor id→arm is bound. `corpus/lessons/round-46.md:60-62` states the routed defect as
"a row may claim a group it does not really address"; clause 4 closes only the duplicate-token
manifestation of that, and the round's kill rule ("a block with the same routed id in two rows
fails clause 4") is met literally while a strictly weaker table passes whole.

This is a property of the frozen instrument, not of the block: no draft can fix it, and I did
not try. The reported consequence for the L1 is that a green `failing == []` at the landing
revision certifies the token multiset, not the matrix's content; if the round wants that
binding it needs a clause the freeze does not have (e.g. a per-row `id must equal the id the
hole quotes` check, or deriving the id from the row's own text).

## 4. Adjacent frozen-spec findings worth more than the pass

- **`ALLOW` refuses the file clause 7 reads.** `ALLOW` (`exact.py:36`) is `corpus/lessons/`,
  `corpus/knowledge/`, `plans/`, `tools/round-47/`. Clause 7 reads `tools/round-46/gate.py`,
  and a block that cites it — the natural way to witness the `-m, --diff-merges=first-parent`
  literal — fails clause 8 with `unresolved or unvalidated citations: 1`,
  `tools/round-46/gate.py: outside the validated path set` (`cite-gate46`, exit 1, stdout
  sha256 `4b3764e7…`). The order arm's evidence can only be pointed at indirectly, which the
  block in `rows.md` does through `corpus/lessons/round-46.md:27-31` and by quoting the
  literal.
- **`--profile v2` is not a lenient escape.** `run_battery` scores the genuine block with the
  **v3** scorer (`exact.py:346`), so a block that is legal under v2's structural clauses but
  red in v3 exits 1 under `--profile v2` with `battery genuine_green 0 != 1`
  (`multi-id-cell` (v2)). The v2 profile therefore cannot be used to demonstrate a forger's
  "v2 green" for a block that is v3-red for a non-battery reason.
- **The worktree draft changed under this seat.** At 2026-10-28T17:51:11Z the block at
  `SKILL.md:632-641` carried prose in its arm cells and a fixture copy scored **exit 1**
  with `arm cells not exact vocabulary tokens: ['symbol: the arm cell must equal one token of
  the fixed vocabulary, …` (clause 5). `SKILL.md` was rewritten at 2026-10-28 14:51:41 -0300
  (size 303,655); the arm cells are now single backticked tokens and the same fixture scores
  **exit 0** (`landed-worktree-draft`, block sha256 `b9bb18e0…`, 17:53:13Z). The pre-edit
  bytes were uncommitted worktree state and are not retained, so that first observation is
  quoted from this session's output rather than from a receipt.

## 5. Deliverables for the landing

- `.ufo/waves/round-47/w1/C1Ids/rows.md` — the four ready-to-paste rows (§5 there), the whole
  block measured green (§6, block sha256 `df731f78…`), the verified citation selectors, the
  pins, and the reproduction commands.
- `receipts/freeze-run.json`, `receipts/head-commit-run.json` — the real-repo runs.
- `receipts/clause4-v3.json`, `receipts/clause4-v2.json` — the 11-case v3 grid and the 5-case
  v2 grid, each entry carrying cmd/exit/utc/stdout sha256 and the full counter JSON.
- `receipts/drive.py`, `receipts/drive-v2.py` — the fixture builders (each asserts
  `git -C <fx> rev-parse --show-toplevel` equals the fixture path before the first commit).

Pins computed here and read back equal from receipts: `interpreter_sha256`
`dcef54f1b14326c33b89a4c55e766832c2a938241968c1d3db1389f9b26c412c`; `mutations_sha256`
`19a2166e47c5231997063a7bc21a7224dda1aa0773bab9c6ffa80ea453d5a112`.

## 5b. The lane advanced to `caafeffa` during the wave — three real-repo runs

While this seat was drafting, block 24 landed (`e856beb5`), the arm cells were rewritten to
single tokens (`62e33f7d`, matching the mid-wave edit recorded in §4), and the frozen set
itself was amended. The wave prompt's freeze no longer scores the tip. Measured at
2026-10-28T17:55-17:56Z:

| run | freeze | rev | exit | `reason` / `failing` | stdout sha256 |
|---|---|---|---|---|---|
| A | `5017e1f7299c3a812e87e7950148f54313dd279e` (the wave's freeze) | `caafeffa330a15e59412bc037591f6942b51e5aa` | 2 | `frozen_path_changed`; `touched` = `plans/round-47-claims.md`, `tools/round-47/record.py` | `0f5dfd70bdecf9e5fc483a015f32ccd5496e6f4cf4626637b0c43c166d67a8b8` (`receipts/at-tip-stale-freeze.json`) |
| B | `9018c53b16503c8d06d398b75503406508119946` (A1, the freeze the claims file declares) | `caafeffa…` | 2 | `frozen_path_changed`; same two paths | `2782b5fd934c354c5c3c3bab467e08f4789affda23a4e92a99a650764fe67acf` (`receipts/at-tip-a1-freeze.json`) |
| C | `1e2c3102952dc636650095643c1963c833859019` (A4, the newest commit touching a frozen path) | `caafeffa…` | **0** | `failing []`, `met_target true`, `routed_counts {CL2:1,CL3:1,CL4:1,CL6:1}`, `arm_tokens ["symbol","once","digest","order"]`, battery 4/4/0, `gate_order_literal 1` / reversed `0` | `10f49044a7a44c8eb8f6644d3f86dd4fb9b38fce0dac3447e967b680d3c14df0` (`receipts/at-tip-a4-freeze.json`) |

Exact commands (C, the one that scores):

```sh
python3 -I -B tools/round-47/exact.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
  --freeze 1e2c3102952dc636650095643c1963c833859019 \
  --rev caafeffa330a15e59412bc037591f6942b51e5aa \
  --json-out .ufo/waves/round-47/w1/C1Ids/receipts/at-tip-a4-freeze.json
```

Findings that follow, all re-derivable from the receipt values above:

1. **The declared freeze cannot score its own landing.** The claims file says the freeze is
   "a series of two … the commit that carries this paragraph" (A1, `9018c53b`). A2 (`62e33f7d`),
   A3 (`2e4ae434`) and A4 (`1e2c3102`) then edited `tools/round-47/record.py` and appended to
   `plans/round-47-claims.md`, so run B exits 2 `frozen_path_changed`. Under the file's own
   rule ("a change makes both counters exit 2") the only freeze that reaches a verdict at this
   tip is the newest one, A4 — run C. The series is four, not two, and the sentence naming A1
   as the freeze is false at `caafeffa`.
2. **Clause 4 is green on the landed bytes**, so the matrix's routed-id multiset is satisfied
   exactly as landed (`routed_counts` all 1). Everything in §3 still applies: the landed table
   passes, and so would `one-hole-four-ids`.
3. Both counters' claims depend on the same frozen set, so this is a round-level freeze
   bookkeeping defect, not a C1-only one.

## 6. Risks and limits

- Block 24 has since **landed** (`e856beb5`, arm cells rewritten at `62e33f7d`), and the tip
  scores exit 0 from freeze A4 (§5b). The wave prompt's freeze `5017e1f…` no longer reaches a
  verdict: run A exits 2 `frozen_path_changed`, and so does the freeze the claims file itself
  declares (run B). A green number for this round has to name a freeze from which no frozen
  path changed, and at `caafeffa` that is only A4.
- `tools/round-47/__pycache__/` exists in the worktree (gitignored, so `gate.dirty()` does not
  see it). It holds a stale `record.cpython-314.pyc`; honouring `-B` keeps it from mattering
  and no `__init__` import path reads it, but a future run without `-B` would leave new pyc
  files inside a frozen directory.
- I did not run the C2 counter (`tools/round-47/record.py`); that is another seat's clause.
- Not run here (out of scope for a leaf seat): the build/lint/format gate. Nothing to build;
  no source file was modified.

## 7. Files changed

Only inside my wave directory:
`.ufo/waves/round-47/w1/C1Ids/{report.md,rows.md,receipts/{freeze-run.json,head-commit-run.json,clause4-v3.json,clause4-v2.json,at-tip-stale-freeze.json,at-tip-a1-freeze.json,at-tip-a4-freeze.json,drive.py,drive-v2.py}}`
and the report pointer `.ufo/waves/round-47/w1/C1Ids.md`. Lane tree unmodified (`git status
--porcelain SKILL.md plans tools corpus SCORECARD.md LOG.md` empty after the run); scratch root
`/fast/scratch/hyaku/kaidoku-r47/C1Ids` removed after the receipts were copied out.
