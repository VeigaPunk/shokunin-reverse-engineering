# R40W2HarmCheck — harm check on coverage / depth / calibration, `fa6a8a3f..4d62ee5a`

**DEFECTS FOUND** — coverage and depth are **not harmed** (the proxies improve: 128/128 → 130/130 mapped,
18/18 → 19/19 resolved, both still 10.0); the **calibration self-assessment surface is harmed**: the lane's
own calibration counters go from 1 to 5 assertion mismatches at the tip, with four new stale statements that
the round-40 commits introduced and none of them repaired. I attacked the landing with a full command-A
recount at seven revisions and with both generations of the lane's calibration instrument; I did not run any
claim counter, REA, unblob or vendor fetch.

- Seat: `R40W2HarmCheck` (leaf; no subagents, no background jobs, no `agent://all`).
- Base `fa6a8a3f85ec65946b3a54d37c0ddd1d6748664f`; tip `4d62ee5a86b4692a13f682b29ed7975e8d7e5326`
  (dispatch rev; lane HEAD at review time `0b15c8b2c593b7954efda92249ef3fa895c79f99` adds only the wave-2
  spec/generator — `git log --name-only fa6a8a3f..4d62ee5a` and `git show --stat 0b15c8b2` confirmed no
  self-assessment surface changed after the tip).
- Receipts in `.ufo/waves/round-40/w2/artifacts/R40W2HarmCheck/`.

## 1. Command A recount (the assignment's observable)

Implementation: `.ufo/waves/arc3-loop1-round2/claims/c1/RV-1/recipeA-tree.py`
(sha256 `0f90d8ff…`, full list in `instruments.sha256`), whose regular expressions and counting semantics
are the same as `command_a()` in `tools/round-36/c2-counter.py` and `tools/round-38/c2-counter.py`; the two
implementations agree exactly on every count reported below. Each revision was
extracted with read-only `git archive <rev> | tar -x` into scratch and the recipe run with `-I -B`; no VCS
mutation.

| revision | `knowledge_files` | `mapped` | `missing` | `dangling` | `rule_blocks` | `citation_resolved_rules` | coverage | depth |
|---|---|---|---|---|---|---|---|---|
| `fa6a8a3f` (base) | 128 | 128 | `[]` | `[]` | 18 | 18 | 10.0 | 10.0 |
| `52b0eb29` (round-39 measured) | 128 | 128 | `[]` | `[]` | 18 | 18 | 10.0 | 10.0 |
| `7fce3086` (round-40 freeze) | 129 | 129 | `[]` | `[]` | 19 | 19 | 10.0 | 10.0 |
| `45e89864`, `2d1ac5bc`, `73c7bf9c` (data commits) | 129 | 129 | `[]` | `[]` | 19 | 19 | 10.0 | 10.0 |
| `42c10a58` (landing) | 130 | 130 | `[]` | `[]` | 19 | 19 | 10.0 | 10.0 |
| `4d62ee5a` (tip) | 130 | 130 | `[]` | `[]` | 19 | 19 | 10.0 | 10.0 |

Commands (one per revision, all exit 0):

```
python3 -I -B "$S/recipeA.py" "$S/<rev>"        # recipeA = the copied recipeA-tree.py
```

Per-revision JSON: `artifacts/R40W2HarmCheck/commandA-{fa6a8a3f,52b0eb29,7fce3086,45e89864,2d1ac5bc,73c7bf9c,42c10a58,4d62ee5a}.json`.

### 1a. What changed and why it cannot harm the two proxies

- **Coverage denominator 128 → 130**, two entries, both mapped and both with a `corpus/README.md` coverage-map
  row (`:95` v2 triage, `:96` AVM-BE) and a Knowledge-index row (`:207`, `:208`); provenance trio present
  (`artifacts/.../trio-r40-entries.txt`). `missing []` and `dangling []` at every revision: no orphan entry
  and no dangling map token. `corpus/README.md:1`'s "A row is written when its file exists" holds.
- **Depth 18 → 19 rule blocks**, block 19 at `SKILL.md:348-378` inside `## Queue-drain craft` (section now
  `81-375`, the 81 start and block 18 at `316-345` unchanged). Block 19 cites
  `corpus/knowledge/2026-10-26-r40-sqfs-triage-v2.md` at five resolving ranges; `citation_resolved_rules 19`.
  Structural check of the block: header `label | operation | provider | handler …`, 11 unique labels,
  11 unique action tokens on the `<!-- sqfs-triage-actions: … -->` line (`SKILL.md:362`), and
  `python3 -I -B tools/round-40/sqfs-triage-v2.py --skill SKILL.md --table-only` reads `rules: 11`, exit 0.
- **Scores do not move on either proxy** (10.0/10.0 at base and tip). The knowledge-index and map additions
  are append-only; the guard `pointers_not_fewer true`, `unrepaired []` in both calibration counters.

**Verdict on coverage and depth: no harm.** Both got strictly more information at the same score, no entry
lost a map row, no block lost a citation.

## 2. Counterexample that does land: the calibration surface

Run the lane's own calibration instruments (they read only git objects) at base and tip:

```
python3 -I -B tools/round-36/c2-counter.py --root <LANE> --rev <REV> --base fa6a8a3f… --json-out <OUT>
python3 -I -B tools/round-38/c2-counter.py --root <LANE> --rev <REV> --base fa6a8a3f… --json-out <OUT>
```

| revision | r36 counter | r38 counter | mismatches |
|---|---|---|---|
| `fa6a8a3f` (base) | exit 1 | exit 1 | 1 (`R1`, pre-existing) |
| `52b0eb29` | exit 1 | — | 5 (stated round-38 values vs round-39 bytes; historical, not this landing) |
| `7fce3086` (freeze) | exit 1 | — | 5 (`O1` 128 vs 129, `O2` 18 vs 19, `O4` 18 vs 19, `R1`, `R2`) |
| `42c10a58` (landing) | exit 1 | — | 5 (`O1` 128 vs **130**, `O2` 18 vs 19, `O4` 18 vs 19, `R1`, `R2`) |
| `4d62ee5a` (tip) | **exit 1** | **exit 1** | **5**; `guards_ok true`, `unresolved []` |

Tip output (identical from both generations; `artifacts/.../cal-at-tip.json`, `cal38-at-tip.json`,
`cal-base.json`, `cal38-base.json`):

```json
{"assertion_mismatches": [
 {"check": "O1 coverage mapped/files", "stated": [128,128], "observed": [130,130]},
 {"check": "O2 depth resolved/rules", "stated": [18,18], "observed": [19,19]},
 {"check": "O4 SHONEN box1 rule blocks", "stated": [18,18], "observed": [19,19]},
 {"check": "R1 depth row craft range", "stated": [316,343], "observed": [81,375]},
 {"check": "R2 SHONEN box1 craft range", "stated": [81,343], "observed": [81,375]}],
 "guards_ok": true, "met_target": false, "mismatches": 5, "revision": "4d62ee5a…", "unresolved": []}
```

`R1` is **pre-existing** at the base (the row's `SKILL.md:316-343` is block 18's range, compared by the
instrument against the whole-section range); round 40 did not introduce it, but widened its observed side
(343 → 375). The round-40 delta is therefore **+4 new mismatches (`O1`, `O2`, `O4`, `R2`)**, all four caused
by the two knowledge entries and block 19 landing without a matching edit to the surfaces the counters read.

## 3. Every self-assessment statement now stale or contradicted

None of the six round-40 commits touched `SCORECARD.md`, `SHONEN.md` or `LOG.md`
(`git log --name-only fa6a8a3f..4d62ee5a`: only `PROVINCE.md`, `corpus/README.md`, `corpus/SOURCES.md`,
two `corpus/knowledge/*.md`, `SKILL.md`, `plans/`, `tools/round-40/`, `.ufo/…`). Statements at `4d62ee5a`:

1. **`SCORECARD.md:23` (coverage row) — STALE.** "128/128 knowledge files mapped after the round-39
   landing"; observed 130/130. Its last-change cell "count refreshed rounds 25, 26, 31, 36, 38 and 39"
   omits round 40. Precedent defeats the "it is a historical measurement" reading: the same row already
   carries "126/126 after the round-38 landing" — i.e. even the round-38 honest stop refreshed it — and the
   round-39 wave-2 record (`SCORECARD.md:3430-3431`) records this exact omission as a defect.
2. **`SCORECARD.md:24` (depth row) — STALE as a current count.** "18/18 queue-drain rule blocks … at
   `52b0eb29` (… new block 18 at `SKILL.md:316-343`)"; observed 19/19 with the section at `81-375`. The
   pinned `52b0eb29` sub-fact is true; the count and the "count refreshed rounds 25, 26 and 39" cell are one
   round behind, and block 19 is not mentioned at all.
3. **`SHONEN.md:6` (box 1) — CONTRADICTED by round-40 bytes.** "`SKILL.md:81-343` (craft section; 18/18
   rule blocks …) at `52b0eb29` … rule block 18 is the machine-readable SquashFS `extract-firmware`
   outcome-triage table (marker `<!-- sqfs-triage-table v1 -->`, eight labels, `SKILL.md:316-343`)".
   Block 18 itself now says "Superseded for routing by rule block 19 (table v2, round 40)"
   (`SKILL.md:331-335`); the live table is v2 with 11 labels and a scored action column, and the section is
   `81-375`. A promotion gate that says the v1 table *is* the machine-readable table now misnames the
   instrument.
4. **`SHONEN.md:10` (box 3) — STALE (superseded, true at its pin).** "the bounded scope is the ten generator
   classes … labels 20 of 20 held-out envelopes … the smallest table that also scores 20/20 is 8 rows /
   7 cells". Round-40 v2 scores 26/26 on 13 classes × 2 with an 11-row table (score receipt
   `l1/scores/c2-at-42c10a58.json`: `matched 26`, `n 26`, `met_target true`, `exit_code 0`). The gate's
   statement of what the lane can execute is now one instrument generation behind.
5. **`SCORECARD.md:3432` (forward plan) — STALE/CONTRADICTED.** "planned (round 40, after a steer): … (a) a
   counter clause that binds a C1 receipt to an in-round re-run of its carrier … (b) an out-of-set envelope
   the triage table must label `unclassified`". Both shipped in round 40: P40-C1 carries the
   scoring-time `plus-extractor` re-run binding, and v2's out-of-domain class
   (`inspect-firmware-regions`/`binwalk`) maps to `(unclassified, none)` and is scored in the 26/26 set. The
   bullet still reads as pending work.
6. **`SCORECARD.md:3433` (saturation line) — STALE by omission.** "…the last capability entries are round
   39." Literally still true (round 40 entered no capability row), but with §3.5 and the absence of any
   `## Round 40` section the surface reads as if round 40 never happened.
7. **Absence, `SCORECARD.md` / `LOG.md` — STALE by omission.** No `## Round 40` section; `grep -n "round
   40\|round-40" LOG.md` → no hits. The round-39 closure set the precedent that a landing records its move
   ("`w2/R39W2C1AxisFit.md` D1 … this section and the `## Owned axes`/`## Capabilities` rows enter that
   record"). `[INFERENCE]` the wave-2 scribe (`.ufo/waves/round-40/w2-spec.json` item `R40W2Scorecard`,
   "draft (do not write into the lane)") repairs the round section; a round section alone does **not** clear
   `O1/O2/O4/R2`, because those read the owned rows and SHONEN box 1, not the round sections.
8. **`SHONEN.md:12` (box 4) — not contradicted, but the asserted boundary no longer covers the new
   surface.** "`PROVINCE.md:97-125` … range unchanged from round 36 and byte-identical at `52b0eb29`" and
   "round-39 additions are appended at `PROVINCE.md:378-384`" both still hold at tip (`R3` passes; the
   round-40 hunks start at `:383+`), but the new round-40 PROVINCE region (`:386-396`, including the
   demoted AVM row) is outside every asserted range. Disclosed by "asserted boundary only"; listed for
   completeness, not as a defect.

Checked and **consistent** (no action): `PROVINCE.md:392/394` "measured, not promoted" and
`corpus/README.md:96/208/250` agree with the C1 score receipt (`exit_code 1`, `carriers_matched 3`,
`target 4`, `met_target false`); `PROVINCE.md:157` and `:384` (AVM-BE stays Frontier) agree with the
demotion; the r40 AVM entry's "Measured; R40-C1 stopped, not promoted" and its table agree with the four
`after.json` receipts the entry cites; `SCORECARD.md:25` calibration 9/9 still matches command B at tip
(`[9,9]`); every SKILL instrument-registry selftest count I could run is exact — `sqfs-triage-v2` 45 (claimed
45), `c2-counter` 42 (42), `c1-extra` 7 (7), `fetch-vendor` 8 (8), `round-36/c2-counter` 13 (13),
`round-38/c2-counter` 14 (14), `round-39/sqfs-triage` 35 (35 in `SHONEN.md:6`); both new entries carry the
`source:`/`verified-at:`/`recheck:` trio and both `recheck:` commands execute for the one I ran
(`sqfs-triage-v2.py --table-only` → `rules: 11`, exit 0).

## 4. Impacted axes

| axis | proxy at base → tip | harmed? | why |
|---|---|---|---|
| coverage | 128/128 → 130/130 (10.0 → 10.0) | **no** | two entries added, both mapped, `missing []`, `dangling []`; row text is stale (§3.1) but the observable improved |
| depth | 18/18 → 19/19 (10.0 → 10.0) | **no** | block 19 resolves its five knowledge citations, table parses to 11 rows/11 actions; row text is stale (§3.2) |
| calibration | command B 9/9 (10.0 → 10.0); calibration counter 1 → 5 mismatches, exit 1 at both ends | **yes, on the statement surface** | four new mismatches (`O1`, `O2`, `O4`, `R2`) introduced by round-40 bytes and reproducible with two independent counter generations; plus the unrecorded round-40 outcome and the stale forward-plan bullet. The calibration *score* does not move (its row's own proxy is command B), so the harm is to the lane's self-assessment accuracy — the thing the calibration axis exists to measure |

`[INFERENCE]` This is the same defect class as round-39 `w2/R39W2C1AxisFit.md` D1 (axis move not recorded
where the lane scores it), and the round-40 landing repeats it: the freeze added a rule block and one entry,
the landing added the second entry, and no commit in `fa6a8a3f..4d62ee5a` touched `SCORECARD.md` or
`SHONEN.md`.

## 5. Smallest safe correction

Apply in one bookkeeping commit (the scribe's draft covers only the round section; these three edits are the
part that clears the counter):

1. `SCORECARD.md:23` → `130/130` with the two round-40 stems and the round-40 revisions; last-change cell
   gains round 40.
2. `SCORECARD.md:24` → `19/19`, block 19 at `SKILL.md:348-378`, section `81-375`, measured at
   `4d62ee5a`; last-change cell gains round 40.
3. `SHONEN.md:6` → keep the `52b0eb29` pin as history only, and state the current range/count
   (`81-375`, `19/19`) with block 19/v2 (`tools/round-40/sqfs-triage-v2.py`, 45 cases) as the live table;
   mark `SCORECARD.md:3432` performed and add the `## Round 40` section + LOG entry (C1 3/4 honest stop,
   C2 26/26).

After that both counters read exactly one mismatch (`R1`), the same pre-existing convention mismatch present
at the base — so the repair must **not** be credited as clearing the calibration axis; `R1`'s convention
(block range vs section range in the depth row) is a separate, older decision.

## 6. Working-tree note (observed, not authored here)

At review time the lane working tree carried one tracked modification I did not make: `SKILL.md` `+19` lines
after `:1384` (uncommitted `### Round-40 instrument registry`, `git diff --stat SKILL.md` → `19 +++++`).
It is a concurrent sibling's edit, not part of `4d62ee5a`, and it does not change any figure above: the
insertion is at end-of-file, after the craft section, so the section stays `81-375`, block 18 stays
`316-345`, block 19 stays `348-378`; the added rows' counts are the ones I verified independently
(`sqfs-triage-v2` 45, `c2-counter` 42, `c1-extra` 7, `fetch-vendor` 8), so the uncommitted registry would
create no new stale statement — had it landed at the landing it would have closed the "registry does not
name the v2 interpreter" gap. `SHONEN.md` and `SCORECARD.md` were unmodified in the tree, so §3 stands.

## 7. Limits

- Command A was run through the wave-artifact implementation `recipeA-tree.py`; it agrees exactly with
  `command_a()` in both lane counter generations at `4d62ee5a` (`130/130`, `19/19`, section `81-375`), so the
  numbers do not depend on one script.
- The counters check presence/count/range resolution, never whether a cited range *supports* its sentence;
  "not harmed" on coverage/depth means the proxies are intact, not that block 19's prose is correct.
- I did not run any claim counter, REA, unblob, sasquatch, or vendor fetch; no vendor bytes were read,
  copied or cited. `PROVINCE.md`'s "measured, not promoted" row was checked against the committed C1 receipt
  only, not re-derived.
- No tool was installed or upgraded (nothing was needed); `pacman` untouched; no host service restarted.
- Scratch `/fast/scratch/hyaku/kaidoku-r40/R40W2HarmCheck` removed after copying the receipts cited above.
