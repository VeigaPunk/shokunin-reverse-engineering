# R44W2C1Satisfy — is the frozen R44-C1 predicate satisfiable?

Seat `R44W2C1Satisfy` (wave 2, role: revenger / satisfiability probe). Lane root
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Read-only against the lane; all scratch work under
`/fast/scratch/hyaku/kaidoku-r44/w2-R44W2C1Satisfy/` (deleted at exit). No claim, counter, rubric,
frozen byte or production doc was modified. No mutating git/jj command was run outside my own scratch
clone (verified `git -C <clone> rev-parse --show-toplevel` = the clone before every `commit-tree`).

Pinned inputs: admissible measured revision `55bcce69c2f4854958d054bcab6d5f0c6fb8a6ac`, freeze
`c48f8a4bfd449300c975668e59aae5b5538b6a84`, base `c29360e3ba5381a5ab69e372d0d9577970f85018`,
dispatch tip `c86ea508188c50e2645b1f9bba65df4177cda6b1`, live lane HEAD at probe time
`8bb1090af3fef64477c4337855e4347472db2701`.
`tools/round-44/c1-counter.py` sha256 = `9f2cc140e1fa7875bcd9dc80ce2ff5a1006e8ee73c7e1207580f88a97ffea993`
at **every** one of those five revisions (byte-frozen; no tool drift).

## 0. Verdicts

| # | proposition under attack | verdict | one-line evidence |
|---|---|---|---|
| V1 | the frozen counter at `55bcce69` returns `carriers_matched 4`, `met_target false`, exit 1 | **CONFIRMED** | replay: exit 1, `carriers_matched 4`, `failing []`, §5.1 |
| V2 | the four REA receipts publish every oracle file, no gap | **CONFIRMED** | `oracle_hits_ok`/`gaps_ok`/`projection_ok`/`path_shape_ok` true on all four, §3 |
| V3 | the receipts carry the scratch `output_directory` form | **CONFIRMED** | §3, all four `…/kaidoku-r44/probe-R44C1Run/c1-run.<id>.1342995/rea-out` |
| V4 | the exit 1 is produced by the `output_directory` / provenance contradiction | **FALSIFIED (as causation)** | `run_provenance_ok` true on all four; the three false bindings are `province_core_section`, `province_core_row`, `frontier_note` (§5.2) |
| V5 | "the frozen R44-C1 text is internally unsatisfiable on one field" / "no real run can satisfy" | **FALSIFIED** | variant **H2** (an outdir naming both strings) scores `met_target true`, exit 0 (§4) |
| V6 | "the honest stop is the only correct reading" | **NOT ESTABLISHED** | the same frozen counter returned `met_target true`, exit 0 at `4cc1ac11` with the **same receipt bytes**; two readings exist (§5.3) |
| V7 | the record says exactly that | **PARTLY** — instrument result and the three false bindings are recorded; the "unsatisfiable / no real run" sentence survives and is false; the tip-freeze account omits `SCORECARD.md` (§6) |
| V8 | R44-C2 at `55bcce69`: 80 entries, `mismatches []`, exit 0 | **CONFIRMED**; not vacuous | replay exit 0; CTL-C2-1 replay with a real `LOG.md` mutation → exit 1 with the exact entry id (§7) |
| V9 | M44-2: both counters exit 2 at the tip; `tools/round-45/frozen-path-preflight.py` catches it | **CONFIRMED with a material omission** | C1 list 8 paths, C2 list **9** (`+SCORECARD.md`, from the round's own closing commit `8bb1090a`) (§8) |

## 1. Method

* One live clone, `git clone --shared` of the lane at lane HEAD, used read-only as `--root` for both
  counters and as the fixture repo for the variant commits.
* The counter's own module was loaded from the frozen blob at `55bcce69`
  (`git show 55bcce69:tools/round-44/c1-counter.py`), so conditions were evaluated by the frozen code
  itself, not by a retyped model.
* The counter-time REA rerun is real: every `projection_ok` below is an actual
  `npx -y rea-agents@6.5.0 extract-firmware` run (rea-agents 6.5.0 at
  `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`, unblob
  `461e1fd9…b1677c`-pinned on the frozen `FIXED_PATH`), not an oracle-substituted comparison.
* Variants were committed as children of `4cc1ac11` (the docs-green C1 landing) so that the three
  PROVINCE bindings are green and the `output_directory` field is the only variable under test.

## 2. Every condition that reads `parameters.output_directory` (source enumeration)

| # | condition | code site | what it reads | implemented? |
|---|---|---|---|---|
| C-a | `run_provenance_ok` | `tools/round-44/c1-counter.py:1176-1182` (`provenance_ok`), consumed at `:1966`, member of `CLAUSES` at `:343` | `os.path.isabs(od)`, `'/kaidoku-r44/' in od`, no `'..'` component | yes |
| C-b | trusted run root | `:1185-1193` (`trusted_run_root`), used by `:1326-1348` (`diagnostic_rel`) inside `:1490` (`disposition_check`) → `gaps_ok`, and by `d['removals']` at `:1948-1952` | isabs, no `'..'` (only reached when the receipt carries a removal diagnostic) | yes, but **unreached** on these carriers: `diagnostics_n == 0` and `gaps_n == 0` on all four (§3), so `od` never enters this path |
| C-c | receipt location | `:246` (`AFTERDIR = 'corpus/evidence/round-44/c1'`), `:2070` | the *receipt file* path `corpus/evidence/round-44/c1/<id>/after.json`; **never** `od` | yes — and it is the only place the string `corpus/evidence/round-44/c1` is used for an input |
| C-d | evidence-id mint | `:596-630` (`evidence_ids`), compared at `:2143-2146` | the envelope's own `parameters` (so `od` transitively), under the frozen rea-agents 6.5.0 `semanticProjection` | yes |
| C-e | claim clause "`od` must name a `corpus/evidence/round-44/c1/` path" (`plans/round-44-claims.md:34-35`) | — | — | **NO. Absent.** `grep -n "corpus/evidence/round-44/c1" tools/round-44/c1-counter.py` → `:246`, `:2070`, `:2856` (selftest), docstrings only |
| C-f | claim clause "the runner binds the scratch-produced tree to the verbatim committed copy under `corpus/evidence/round-44/c1/`" (`plans/round-44-claims.md:139`) | — | — | **NO. Absent.** The committed extract trees are never opened; §4.4 measures the consequence |

So of the two mutually exclusive prose clauses, the counter implements exactly one (C-a). C-e has no
code, which is why the instrument went green on receipts that violate the prose.

## 3. Truth table — the four real receipts, each condition in isolation

Loaded with the frozen module (`os.environ` + `importlib`), receipts from
`git show 55bcce69:corpus/evidence/round-44/c1/<id>/after.json`. Artifact
`artifacts/R44W2C1Satisfy/truth-table.{txt,json}` (stdout of the probe script, counter sha256 recorded
in it).

| id | isabs | has `/kaidoku-r44/` | no `..` | `provenance_ok` (C-a) | `trusted_run_root`≠None (C-b) | claim A (scratch segment) | claim B (`corpus/evidence/round-44/c1/`) | A∧B | `diagnostics_n` | `gaps_n` | stored == recomputed id |
|---|---|---|---|---|---|---|---|---|---|---|---|
| v1le | T | T | T | **T** | T | T | **F** | **F** | 0 | 0 | **T** (`ev_26c313fc…8144e2`) |
| v1be | T | T | T | **T** | T | T | **F** | **F** | 0 | 0 | **T** (`ev_e7e3a71f…cdc44`) |
| v2le | T | T | T | **T** | T | T | **F** | **F** | 0 | 0 | **T** (`ev_603145b2…92fed2`) |
| v2be | T | T | T | **T** | T | T | **F** | **F** | 0 | 0 | **T** (`ev_89b83ee7…e9ee5e`) |

`output_directory` of all four:
`/fast/scratch/hyaku/kaidoku-r44/probe-R44C1Run/c1-run.<id>.1342995/rea-out`.

**The evidence id is a function of `output_directory`** (measured, not assumed): re-minting `v1le` with
`od = /fast/scratch/hyaku/kaidoku-r44/od-probe/x` yields
`ev_f2dc20b4d9687d3783ccfb585aa1c91e5254fc35f8ab8b11ab5c087a12263e4a` instead of
`ev_26c313fc…8144e2`. So `evidence_id_ok` proves *consistency with whatever provenance the envelope
carries*, never that a run wrote to that path — which is exactly why a re-minted variant is a fair
satisfiability witness.

## 4. Variant matrix — one receipt set per hypothesis, scored by the frozen counter

Each variant is a child of `4cc1ac11` (docs green) that rewrites only
`parameters.output_directory` on all four receipts and re-mints the evidence id with the frozen
`tools/round-27/xpin-attribute.mjs` through the package's own 6.5.0 rule. `ids re-minted` is the count
that changed when `od` changed.

| tag | `output_directory` shape | ids re-minted | commit | `carriers_matched` | `met_target` | exit | failing |
|---|---|---|---|---|---|---|---|
| **H1** | absolute **committed** path `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-44/c1/<id>` | 4 | `3f32eef5bb8b7e263a54ffadac0c116391b4689b` | **0** | false | **1** | `<id>:run_provenance_ok` ×4 |
| **H2** | path naming **both**: `/fast/scratch/hyaku/kaidoku-r44/probe-R44C1Run/c1-run.<id>.1342995/rea-out/corpus/evidence/round-44/c1/<id>` | 4 | `3c22fe423529486874a0cc25be2e4cadd1f1d2fb` | **4** | **true** | **0** | `[]` |
| **H3** | the shipped scratch path, verbatim (control) | 0 | `372a2da5b885a9c426ce1fb2d9796ba2a3a79cf8` | **4** | **true** | **0** | `[]` |

### 4.1 The frozen predicate is satisfiable — three independent ways

* **H3** is the shipped receipts scored at the docs-green revision: exit 0, `met_target true`,
  every binding true. So the *instrumented* predicate was already satisfied by the bytes this round
  produced; nothing about the receipts is deficient under the counter.
* **H2** satisfies the counter **and** the literal wording of the amendment clause
  (`plans/round-44-claims.md:34-35`): the string `corpus/evidence/round-44/c1/` is present, the path is
  absolute, it is inside `/kaidoku-r44/`, and the id is minted over it. Exit 0.
* The pre-existing committed receipt `corpus/evidence/round-44/c1/counter-at-4cc1.json` (argv-pinned,
  `counter_sha256 9f2cc140…ea993`) reports the same green at `4cc1ac11`; I re-derived it independently
  (§5.2).

**Therefore "internally unsatisfiable" / "no real run can satisfy" is false.** A real run writing into
`…/kaidoku-r44/<run>/rea-out/corpus/evidence/round-44/c1/<id>` satisfies both prose clauses and the
counter. The L1's own live amendment already concedes this ("a substring-shaped scratch path … passes
both prose clauses and the counter"), while the same paragraph still opens with "internally
unsatisfiable" — the paragraph contradicts itself. The accurate word is **unrealized by this round's
receipts**, not unsatisfiable.

*Caveat I state rather than hide:* if "must name a `corpus/evidence/round-44/c1/` path" is read as
"must resolve to the lane's committed directory", H2 is a loophole and not the intended binding. The
frozen text does not say that; the word "committed" appears in my brief, not in
`plans/round-44-claims.md:34-35`. Either way the satisfiability verdict stands: the conjunction is
satisfiable under the frozen wording, and the fix is an outdir naming decision, not a re-freeze.

### 4.2 An outdir satisfying the prose clause alone reds only one clause
H1 (committed path) → **only** `run_provenance_ok` false, `carriers_matched 0`. Every other per-carrier
clause stays true, including `evidence_id_ok` and `projection_ok`. So the instrument is decisive about
which of the two clauses an outdir satisfies, and blind to the other.

### 4.3 H1 vs H3 is the whole contradiction in one table
`run_provenance_ok` is the *only* clause that separates the two prose clauses; it is true for the
receipts as shipped and false for the amended form. That is why the same receipt set is "met" and "not
met" depending only on which prose clause is enforced.

### 4.4 The "verbatim committed copy" clause is unenforced (measured)
Child of `4cc1ac11` = `4e9880d486195fd677de1e98556a08b9788e1f83`, mutating one committed extract-tree
byte — `corpus/evidence/round-44/c1/v1le/firmware.bin_extract/apple.txt`, `apple\n` → `XXXle\n`:

```
python3 -I -B tools/round-44/c1-counter.py --root <clone> --rev 4e9880d4… --freeze c48f8a4b… \
    --pkg65 <rea-agents> --work <scratch>
→ exit 0; carriers_matched 4; met_target true; failing []; frozen_path_changed []
```

The committed evidence tree can be corrupted and the frozen counter still returns the target. The
`plans/round-44-claims.md:139` binding has no code path; `AFTERDIR` is used only to read `after.json`
(`:2070`). (`corpus/evidence/round-44/c1/**` is deliberately not a frozen path, so no freeze red
masks this.) This is a second, independent instance of "a frozen claim conjunct the instrument does not
implement".

## 5. The C1 verdict and its record

### 5.1 The verdict itself is confirmed
Replay of the frozen counter on the frozen clone at `55bcce69`: exit **1**, `carriers_matched 4`,
`target 4`, `met_target false`, `carriers_unchanged true`, `frozen_path_changed []`,
`failing []`, `bindings_false ['province_core_section', 'province_core_row', 'frontier_note']`;
all 22 `CLAUSES` true on all four carriers (`matched true`), wall 8.45 s, stdout sha256 `eea45d37…cac9f8d`.
`met_target false` is entailed by `bindings_false` (`c1-counter.py:2200-2211`), not by any receipt-side
failure.

### 5.2 Where the red actually comes from
The only commits in `4cc1ac11..55bcce69` are `9d3d1862` (adds the score receipt), `75a5cb42`,
`e9e3abd1` (control receipts), `55bcce69`. `git diff --name-status 4cc1ac11 55bcce69 --
corpus/evidence/round-44/c1/` → **`A counter-at-4cc1.json` only**: the four `after.json` blobs are
identical at both revisions. `55bcce69` changes exactly three files:
`PROVINCE.md` (6 lines), `corpus/README.md` (6 lines), the knowledge entry (83 lines).

At `4cc1ac11` `PROVINCE.md:424` is `## Round-44 additions to Core` → `province_core_section` true,
`province_core_row` true, `frontier_note` true (the note carries the entry stem). At `55bcce69` the
same line is `## Round-44 measured, not promoted (R44-C1 honest stop)` and the note drops the stem →
all three bindings false. Replay of the frozen counter at `4cc1ac11`:

```
python3 -I -B tools/round-44/c1-counter.py --root <clone> --rev 4cc1ac11… --freeze c48f8a4b… --pkg65 <rea-agents> --work <scratch>
→ exit 0; carriers_matched 4; met_target true; failing []; bindings_false []
```
(wall 6.64 s, stdout sha256 `8742a90d…fee6a`; identical verdict to the committed
`counter-at-4cc1.json`).

**Consequence for the record:** the recorded exit 1 at the measured revision does not corroborate the
stop. Under the reading the round adopted, rewriting PROVINCE is *required* (you may not leave a Core
heading for a claim you say is not met), and that rewrite is what flips the counter. The score is a
restatement of the verdict, not evidence for it. The only measurement of the receipt-side predicate is
the green one at `4cc1ac11`, and the round's own entry (`corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md:3-9`)
and SCORECARD row (`SCORECARD.md:3525`) already say so.

### 5.3 "The only correct reading" is not established
Two readings are each supported by frozen bytes:
* **R1 (instrument-governed):** `plans/round-44-claims.md:157` defines the target *as*
  `carriers_matched == 4`, every binding true, `frozen_path_changed []`, `met_target true`, exit 0 —
  and `:120` calls `tools/round-44/c1-counter.py` the predicate. All true at `4cc1ac11`. → met.
* **R2 (amendment-governed):** `:34-35` requires the committed `corpus/evidence/round-44/c1/` path in
  `parameters.output_directory`, which the receipts do not carry. → not met.

The round chose R2, which is defensible and conservative, but it is a *choice* between two frozen
sentences, and R1 has the stronger textual anchor (the claim's own Target line). R2 also cannot be
verified by the frozen counter (C-e absent, §2). The record should say "the conservative reading of a
self-contradictory frozen text", not "the only correct reading".

## 6. Numbered defects for the L1 (none of these is fixed here)

**D-1 (record, must fix).** `corpus/lessons/round-44.md:69` (worktree at probe time; line 63 in the
committed `8bb1090a` blob) and `SCORECARD.md:3525` assert
"internally unsatisfiable on one field" / "no real run can satisfy". Falsified by H2
(`3c22fe42…`, exit 0, `met_target true`) and by the amendment's own loophole sentence in
`corpus/lessons/round-44.md:77-79`. Recommended wording: "unrealized by this round's receipts; the
conjunction is satisfiable by an output-directory naming decision (and the strict-intent reading is a
binding the counter does not implement)". Command: §4 H2 row. Observed: exit 0, `failing []`.

**D-2 (instrument, must record).** `plans/round-44-claims.md:139` ("the runner binds the
scratch-produced tree to the verbatim committed copy under `corpus/evidence/round-44/c1/`") is
unimplemented: `tools/round-44/c1-counter.py:246`/`:2070` read only `after.json`; mutating
`corpus/evidence/round-44/c1/v1le/firmware.bin_extract/apple.txt` at a child of `4cc1ac11`
(`4e9880d4…`) still yields exit 0 / `met_target true` / `carriers_matched 4`. Either implement the
tree binding or strike the clause from the next freeze; carrying it as prose is the same defect class
as R44-CL2.

**D-3 (record, must fix).** The tip freeze account is incomplete. At the committed lane tip
`8bb1090af3fef64477c4337855e4347472db2701`:
* C1 `frozen_path_changed` = 8 paths (all `tools/round-44/control-fixtures/**`, status `M` from
  `c86ea508`), exit 2, wall 0.074 s, stdout sha256 `0e1c1f55…e3845`;
* C2 `frozen_path_changed` = **9** paths — the same 8 **plus `SCORECARD.md`**, exit 2, wall 0.083 s,
  stdout sha256 `0a81b8b2…a064c64`.
`symmetric difference = ['SCORECARD.md']`. Cause: `8bb1090a` appended a 16-line
`## Round 44 — …` section at `SCORECARD.md:3519-3534`, which the frozen rubric explicitly forbids —
`tools/round-44/c2-rubric.json` `expected_edits["SCORECARD.md"].note`: *"The round-44 landing section
cannot ALSO be appended to SCORECARD.md under the current counter contract … the L1 must either land it
elsewhere or re-freeze with it bound."* So the round's own closing commit is a second freeze violation,
not named by `corpus/lessons/round-44.md:16` (which attributes the tip red solely to `c86ea508`'s 8
files) and not visible in `SCORECARD.md`'s M44-2 paragraph ("wrote/modified 8 files"). Either move the
section out of `SCORECARD.md` (the rubric's own instruction) or record the ninth path. Command and exit
codes: §9 rows 10-11. `git show --name-status c86ea508 -- tools/round-44/` = 8 × `M` (no `A`: the
worktree's corrected "modified 8 files (no file was added)" is right).

**D-4 (instrument, record).** The C2 claim's B2 sentinel (`plans/round-44-claims.md`, "else exit 2
`asserted_not_in_base_line`", `line_sha256 == sha256(line_at_base)`) and the `pin_rev` rule are
implemented nowhere: `grep -rn "asserted_not_in_base_line" tools/round-44/` → no hits;
`grep -n "line_sha256\|line_at_base\|pin_rev" tools/round-44/c2-counter.py` → no hits; and 0 of the 80
embedded check scripts mention those keys (`line_sha256`/`line_at_base` are dead rubric fields). Not a
free-pass — a wrong `asserted` reds as a mismatch (§7) — but the claimed exit-2 guard does not exist.
Amend the claim text to describe the instrument that exists, or implement B2 centrally.

**D-5 (report cross-check, informational).** `.ufo/waves/round-44/w2/R44W2Preflight.md:55` records the
C2 tip run as "same 8 `frozen_path_changed` paths" and concludes the "byte-identical" claim holds. The
stdout it cites (`sha256 0a81b8b2…a064c64`) contains **9** paths (`+SCORECARD.md`), and the `c86ea508`
run contains 8 (`b789895b…ef004`). The two lists are not identical at the tip. (The lesson's
"byte-identical" sentence has since been removed in the worktree; the sibling report still carries the
wrong count.)

**Not defects (checked and cleared).** `corpus/evidence/round-44/c1/counter-at-4cc1.json` is a *score*
receipt, not an evidence envelope; it is cited openly by the entry, and `evidence_envelope_ok` only
reads `after.json`, so its presence does not corrupt the counter. The two `c2-score-9d3d.json` copies
(`corpus/evidence/round-44/c1/` and `…/c2/`) differ only in `wall_seconds` and per-check timings
(`0c051cc3…` vs `56df064f…`); no verdict field differs.

## 7. R44-C2 — falsification attempt (vacuity / free-pass / note-vs-value)

* **Replay at `55bcce69`:** `entries_evaluated 80`, `entries_count 80`, `mismatches []`,
  `unevaluable []`, `frozen_path_changed []`, `claim_score true`, exit **0**, `wall_seconds 4.654986`;
  `counter_sha256 == counter_sha256_at_freeze == 085192ea…c277`;
  `rubric_sha256 == …_at_freeze == …_at_rev == e8cc0ded…e755e`. **CONFIRMED.**
* **Vacuity / free-pass:** not found. `python3 -I -B tools/round-44/c2-counter.py --selftest` → exit 0,
  `ok true`; the self-test includes a seeded reality mismatch (exit 1), a seeded claim mismatch
  (exit 1), "a note alone never repairs" (still exit 1) and a note + independent re-derivation (exit 0),
  and the counter rejects a check that reads the rubric's own asserted value as circular
  (`c2-counter.py:855`).
* **Independent fitness witness (my own, not the round's):** child of `55bcce69` =
  `26a288be2465cfe626b61ac1288b19911a06dabd` mutating `LOG.md:3184`
  (`## 2026-10-27 — round 43` → `round 43x`) and nothing else →
  `mismatches ['C2-d17-sharpen-log-round43-entry']`, `frozen_path_changed []`, `entries_evaluated 80`,
  exit **1**. So the d17 check is a live derivation, and `LOG.md`'s non-frozen status is as declared.
* **Not attacked (out of this seat's budget, stated as a limit):** I did not replay all 80 mutations. I
  sampled one seeded control and the whole self-test; the rubric's `fitness.entries_witnessed 80 /
  fails_as_required 80` remains an author-declared number that I did not re-measure entry by entry.
* **Note-vs-value:** the mechanism exists (`c2-counter.py:1504-1513`, arms 8 and 9) and the note is read
  as text with the value re-derived; no free-pass found.

## 8. M44-2 and the preflight gate

* `git show --name-status c86ea508 -- tools/round-44/` → 8 × `M`, no `A`. So the frozen claim's
  "a file added under it after the freeze is a change" is not the clause that fires; the modification
  clause does. The worktree lesson's corrected wording ("modified 8 files (no file was added)") is
  right.
* **Preflight reproduces the fix** (`tools/round-45/frozen-path-preflight.py`):
  * `--freeze c48f8a4b --rev c86ea508 --pathspec tools/round-44/` → exit **1**,
    `verdict frozen_path_changed`, `touched 8`, `blob_changed 8` (exactly the 8 `M` paths);
  * `--rev 55bcce69 --pathspec tools/round-44/` → exit **0**, `verdict clean`;
  * `--rev c86ea508 --pathspec tools/round-44/c1-counter.py` (an exact-file pathspec) → exit **0**.
* **Sufficiency conditions the record must state:**
  1. the gate only fires on *added* files under a frozen **directory** when the caller passes the
     directory pathspec (`:29-30`, default `[]` = "tree backstop only"; `:69-70` the backstop can only
     see paths that existed at FREEZE). A hook wired from the claims' enumerated file list would have
     missed M44-2 exactly as the counters did;
  2. with **no** `--pathspec` the gate exits 1 on *any* range with changes — it flags every touched
     path, including unrelated `.ufo/waves/round-44/controls/…` — so the default is a permanent false
     red, not a usable gate.
* **Is "measure at `55bcce69`" honest and sufficient?** Admissible: YES — freeze is an ancestor and
  `frozen_path_changed []` at that revision for both counters (C1 verified, C2 exit 0). Disclosed: YES
  (`corpus/lessons/round-44.md:16`, R44-CL1, QUALITY 77). Sufficient: **NO as landed** — the round's
  own closing commit adds a ninth frozen-path violation (§6 D-3), so "the tip is red because of
  `c86ea508`" is an incomplete account of the tip it describes.

## 9. Receipts (command, exit, stdout sha256, wall)

Clone: `/fast/scratch/hyaku/kaidoku-r44/w2-R44W2C1Satisfy/lane` (`git rev-parse --show-toplevel`
verified before the first `commit-tree`); counter for C1 is the frozen blob at `55bcce69`
(sha256 `9f2cc140…ea993`), for C2 the frozen `tools/round-44/c2-counter.py` (sha256 `085192ea…c277`).

| # | run | rev | exit | stdout sha256 | wall |
|---|---|---|---|---|---|
| 1 | C1 frozen counter | `55bcce69` | **1** | `eea45d374bb450f15c549ca5e7c7803ac9e6c31bb982fae45d6542ee8cac9f8d` | 8.45 s |
| 2 | C1 frozen counter | `4cc1ac11` | **0** | `8742a90d9b879fbf91f77c5862273be788911ace1d2228e79cd6b9ad2d8fee6a` | 6.64 s |
| 3 | C1, variant H1 | `3f32eef5` | **1** | `ed1d1a5f396aee906820f724caeb1570e0b328041747012e7ea9806ee4d356e4` | ≤21.58 s (batch) |
| 4 | C1, variant H2 | `3c22fe42` | **0** | `25670cd6978063ab993d2424146636ee24b90115a8b36552c6ceeaac412de952` | ″ |
| 5 | C1, variant H3 | `372a2da5` | **0** | `9c3d684286f7125df1cf59d7f3b896781a6914474c9039f2f94f147bf2a3226a` | ″ |
| 6 | C1, committed-tree mutation | `4e9880d4` | **0** | `962cbcf0e506000245e68f3be992d84129c6566dd92b7a72992ed6f8cd0d7b98` | 7.15 s |
| 7 | C2 frozen counter | `55bcce69` | **0** | `dd7c529bb6340c364854093937bce3d90ec980ebdea951263bb38dc52316a9b3` | 4.65 s |
| 8 | C2, CTL-C2-1 replay | `26a288be` | **1** | `2f687eed0446d84d9459ceb42fde718d63a899e2a52640136a14e8c146619bf3` | 4.58 s |
| 9 | C2 frozen counter | `c86ea508` | **2** | `b789895baa6f59c0faad7d60fbec56063bd082bf1f54b3daa7ddf309b13ef004` | ~4 s |
| 10 | C1 frozen counter | `8bb1090a` (tip) | **2** | `0e1c1f556d375f025f83bd0405e8dbb52de5021a9e69c2838d22eb832e4e3845` | 0.074 s |
| 11 | C2 frozen counter | `8bb1090a` (tip) | **2** | `0a81b8b2e85b08914b5a2f1b3856601f53d8c6f491ae5e00794c9bcf9a064c64` | 0.083 s |
| 12 | C2 `--selftest` | — | **0** | (report on stdout; `ok true`) | — |
| 13 | preflight red | `c86ea508` | **1** | artifact `preflight-c86ea508.json` (`touched 8`, `blob_changed 8`) | — |
| 14 | preflight green | `55bcce69` | **0** | artifact `preflight-55bcce69.json` (`verdict clean`) | — |
| 15 | preflight exact-file pathspec | `c86ea508` | **0** | artifact `preflight-exactfilepaths.json` | — |

Artifacts (all under `.ufo/waves/round-44/w2/artifacts/R44W2C1Satisfy/`): the 15 rows above plus
`truth-table.{txt,json}`, `variants.json`, `tip-timings.json`.
Scratch `/fast/scratch/hyaku/kaidoku-r44/w2-R44W2C1Satisfy/` deleted at exit (no clone, work dir or
fixture left). No tool was installed or upgraded for this seat (nothing was needed; `pacman` was not
invoked).

## 10. Confidence and limits

* **High:** V1-V5, V8, V9 — each is a replay of the frozen instrument on a byte-pinned revision with
  stdout hashes; V4/V5 are additionally differential (same receipts, two revisions; one field, two
  variants).
* **High:** the tip-list asymmetry (V9/D-3) — two JSON parses of two frozen counters' own stdout.
* **Medium:** V6/V7 are readings of prose, not measurements. I argue R1 is textually supported by
  `plans/round-44-claims.md:157` and `:120`; an L1 ruling that the amendment supersedes the Target line
  would make R2 canonical — it would not make it "the only correct" reading.
* **Not covered (stated):** the 80-entry C2 fitness census was sampled, not re-measured; C1's
  CTL-C1-1..CTL-C1-5 red arms and CTL-C1-POS positive arm were replayed by sibling seats
  (`R44W2C1PosArm`, `R44W2C1Rescore`) and not duplicated here; the four-carrier disclosure limits
  (D-01/D-07/D-08/D-09) are untouched by this probe.
