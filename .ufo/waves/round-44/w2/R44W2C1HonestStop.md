# R44W2C1HonestStop — adjudicating the R44-C1 honest stop against the frozen claim text; R44-C2 re-scored; M44-2 / preflight measured

Seat `R44W2C1HonestStop`, round 44 wave 2 (falsification of the landing and the record).
Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Freeze
`c48f8a4bfd449300c975668e59aae5b5538b6a84`; measured revision
`55bcce69c2f4854958d054bcab6d5f0c6fb8a6ac`; base `c29360e3ba5381a5ab69e372d0d9577970f85018`;
dispatch tip `c86ea508188c50e2645b1f9bba65df4177cda6b1`; lane tip when the seat ran
`8bb1090af3fef64477c4337855e4347472db2701` (the record commit). I changed no claim, counter,
rubric, frozen byte or production doc. Every mutation I made was in a throwaway
`git init` fixture under my own scratch, with `user.name=R44W2C1HonestStop` and
`git rev-parse --show-toplevel` asserted equal to the fixture path before the first commit;
one lane-readable `git clone` was not needed. Scratch
`/fast/scratch/hyaku/kaidoku-r44/R44W2C1HonestStop/` deleted before yield.

`--root` was always the real lane (read-only: the counters read `git show` objects and write
only to `--work`/`--json-out` under my scratch). No tool was installed (none needed); pacman
untouched.

## Verdict summary

| # | Question | Verdict |
|---|---|---|
| 1 | Are `carriers_matched 4`, `met_target false`, `exit 1`, `bindings_false` at `55bcce69` reproducible? | **CONFIRMED** — exit 1, wall 7.028 s, stdout sha256 `eea45d374bb450f15c549ca5e7c7803ac9e6c31bb982fae45d6542ee8cac9f8d` (byte-identical to peer `R44W2C1Rescore`'s run), all 22 carrier clauses `true` on all four carriers. |
| 2 | Is there a real REA run whose receipt satisfies **both** `output_directory` clauses as written? | **NO faithful one** (HS-1). The clause-faithful path fails `provenance_ok`; the producible scratch path fails item 3; the only joint string satisfaction is a scratch root *spelling* `corpus/evidence/round-44/c1/`, which the frozen runner cannot produce (`c1-run.py:331-334`). |
| 3 | Is "measured, not promoted" the only honest verdict? | **Yes as an outcome, no as recorded** (HS-2, HS-3): no faithful promotion was available, but the record's causal sentence (`PROVINCE.md:428` "does not satisfy the frozen predicate") is false and the instrument's green at `4cc1ac11` is unrecorded. |
| 4 | Did the round correctly avoid promoting on the 4/4 precursor score at `4cc1ac11`? | **Yes on the promotion question** — exit 0 there (`met_target true`, `bindings_false []`), but its receipts fail item 3, so recording it as C1's score would assert a provenance the claim text forbids. The refusal was right; the omission is the defect. |
| 5 | Could the lane have satisfied item 3 by minting the id over the committed path while keeping a scratch `output_directory`? | **No** — the mint is a function of the envelope's own `parameters.output_directory`; the hybrid is `evidence_id_ok false` (measured, HS-3 §4). |
| 6 | R44-C2: `entries_evaluated 80`, `mismatches []`, `frozen_path_changed []`, exit 0 at `55bcce69`? | **CONFIRMED**, and non-vacuous; but two clauses describe verdicts the instrument cannot emit (HS-4, HS-5). |
| 7 | M44-2: both counters exit 2 at the tip, the round measures at `55bcce69`? | **CONFIRMED** (8 paths at `c86ea508`; 9 at `8bb1090a` for C2 — `SCORECARD.md` joins from the record commit). Honest, but the record's content is wrong in one word and omits the control-evidence state (HS-7, HS-8). |
| 8 | Does `tools/round-45/frozen-path-preflight.py` catch M44-2? | **Yes, exactly** (red `c86ea508`, green `55bcce69`, red tip), but its default and docstring disagree (HS-9). |

---

## 1. The frozen text, quoted

`plans/round-44-claims.md`, wave-1 amendment item 3 (`grep -n output_directory`):

```
34:   CTL-C1-4 + provenance binding (the receipt's `parameters.output_directory` must name a
35:   `corpus/evidence/round-44/c1/` path and the evidence id must be minted over that path; the
36:   counter rejects any after-receipt byte-identical to a pre-freeze committed envelope).
```

The predicate paragraph, same file:

```
137: ... the receipt's `parameters.output_directory` names this round's
138: `/kaidoku-r44/` scratch segment and the evidence id is minted over that provenance; the runner
139: binds the scratch-produced tree to the verbatim committed copy under `corpus/evidence/round-44/c1/`.
140: A pre-freeze envelope relabelled into a round-44 receipt path is rejected by provenance and
141: evidence-id bindings (the counter does not claim a separate byte-identity comparison);
```

The data procedure:

```
162:  `tools/round-44/c1-run.sh --data-run --rea-outdir-mode scratch`; REA's output directory is in
163:  the private `/kaidoku-r44/` scratch segment, and the runner records the receipt/provenance and
164:  copies the produced tree verbatim into `corpus/evidence/round-44/c1/<id>/`; seats never run it.
```

Line 34-35 and line 137-138 name **different required values for the same field**. No line in
the file gives either precedence. Line 36 and line 141 also contradict each other on the
byte-identity control (unimplemented; only the `:141` disclaimer is true — nothing in
`c1-counter.py` compares a receipt to a pre-freeze envelope).

## 2. What the frozen counter actually binds

`tools/round-44/c1-counter.py` (sha256 `9f2cc140…fea993` at `55bcce69` **and** at the freeze,
identical blobs `9695d586…`):

* `:258` `PROV_SEGMENT = '/kaidoku-r44/'`
* `:1176-1182` `provenance_ok(output_directory)`: absolute, contains `PROV_SEGMENT`, no `..` —
  **and nothing else**. There is no `corpus/evidence/round-44/c1/` test anywhere
  (`AFTERDIR` at `:246` is the committed receipt directory the counter *reads*, not a
  provenance requirement).
* `:334-344` `BINDINGS`/`CLAUSES`: 22 carrier clauses (incl. `run_provenance_ok`,
  `evidence_id_ok`, `projection_ok`) and 20 document bindings.
* `:2128` `evidence_id_ok = stored == recomputed` under the frozen `xpin` rule, both derived
  from the receipt's own `parameters`.
* `:2216-2217` `met_target = carriers_unchanged and carriers_matched == 4 and all(BINDINGS)`;
  `:2390` exit 0 iff `met_target`.

Measured at `55bcce69` (my run, receipt `c1-at-55bcce69.json`): `carriers_matched 4`,
`bindings_false ["province_core_section","province_core_row","frontier_note"]`,
`failing []`, `frozen_path_changed []`. Every carrier clause is `true`, including
`run_provenance_ok` and `evidence_id_ok`, on the four scratch-form receipts
(`/fast/scratch/hyaku/kaidoku-r44/probe-R44C1Run/c1-run.<id>.1342995/rea-out`,
`corpus/evidence/round-44/c1/<id>/after.json`).

So the red at the measured revision is **the withheld landing** (three PROVINCE document
bindings), not provenance. That is the same finding the current working-tree lesson already
carries as wave-2 `D-5` (`corpus/lessons/round-44.md:67-75`). §4 re-measures the id-mint
dependence independently (peer `R44W2C1Satisfy` §3 measured it first); HS-2 adds the unrecorded
`4cc1ac11` green.

## 3. Answers (a)–(d)

**(a) Is there any real REA run whose receipt satisfies both clauses as written?**
No faithful one. Probe of the counter's own predicate
(`artifacts/R44W2C1HonestStop/provenance-ok-probe.txt`):

| candidate `parameters.output_directory` | `provenance_ok` | which clause it fails |
|---|---|---|
| `/fast/scratch/hyaku/kaidoku-r44/probe-R44C1Run/c1-run.v1le.1342995/rea-out` (the four receipts) | **True** | item 3 (no `corpus/evidence/round-44/c1/` segment) |
| `<LANE>/corpus/evidence/round-44/c1/v1le` (item-3 faithful, `--rea-outdir-mode evidence`) | **False** | predicate `:137-138` / `provenance_ok` |
| `/fast/scratch/hyaku/kaidoku-r44/corpus/evidence/round-44/c1/v1le/rea-out` | **True** | both prose clauses pass, but it is a *scratch* path that only spells the corpus segment (loophole, not a binding) |
| `…/kaidoku-r44/../kaidoku-r44/…` | False | `..` guard |

The third row is the only joint string satisfaction. Peer `R44W2C1Satisfy` §4 scores that same
shape green (their H2: exit 0, `met_target true`, `failing []`) and the committed-path form red on
`run_provenance_ok` only (their H1); my probe reproduces their id-mint dependence. What their
hypothetical does not test, and what decides the reading, is producibility: the frozen runner cannot
produce it —
`c1-run.py:331-334` fixes `run_dir = <scratch>/kaidoku-r44/c1-run.<cid>.<pid>` and
`:337-346` sets `rea_outdir` to `<run_dir>/rea-out` (scratch, the CLI default at `:799-801`)
or to the evidence dir (evidence mode) — never to a scratch path whose components spell
`corpus/evidence/round-44/c1/`. Producing it would require a runner edit, i.e. a freeze
violation. Therefore, under the frozen instruments, the claim has **no faithful satisfying
receipt**: the two clauses' faithful extensions are disjoint.

**(b) Is "measured, not promoted" the only honest verdict?**
The *outcome* is the only honest one: a promotion would assert item-3 compliance the receipts do
not have. But it is not "the only correct reading" of the text, and the record's reason is wrong.
The predicate paragraph `:137-139` is satisfied exactly by the four receipts (the counter is a
literal transcription of it), so `PROVINCE.md:428` — "The score therefore does not satisfy the
**frozen predicate**" — is false as written; the score fails the *amendment sub-clause* at
`:34-35`. The honest sentence is: "the frozen claim contains two incompatible `output_directory`
clauses; no receipt can satisfy both faithfully; the round declines to promote."

**(c) Did the round correctly avoid promoting on the 4/4 precursor score at `4cc1ac11`?**
Yes. My re-run (`c1-at-4cc1ac11.json`): exit **0**, `carriers_matched 4`, `met_target true`,
`bindings_false []`, `frozen_path_changed []`, counter sha unchanged. That is the frozen
**Target** (`plans/round-44-claims.md:157-158`) met at a clean post-freeze revision. Recording
it as C1's claim score would have promoted on receipts that fail item 3, so the round was right
to refuse. The defect is that the record never says the instrument went green there — the lesson
(`:1-8`, `:63-75`), `PROVINCE.md:424-430` and `corpus/README.md:104` all present only the
`55bcce69` red, and the green reading survives only as the committed
`corpus/evidence/round-44/c1/counter-at-4cc1.json` (`exit_code 0`, `met_target true`) with no
prose binding it to the decision. A reader can take that file as C1's evidence of success.
(Corroborated independently by peer `R44W2C1Satisfy` V6, which re-derived the same green at
`4cc1ac11` with the same receipt bytes.)

**(d) The freeze-time check that would have caught it (not a claim rewrite).**
A **conjunct-satisfiability preflight** run before the freeze commit — e.g.
`tools/round-45/frozen-claim-satisfiability.py`:

1. parse every frozen clause that constrains one receipt field (`output_directory`: item 3's
   `corpus/evidence/round-44/c1/` matcher, predicate's `/kaidoku-r44/` matcher, evidence-id
   minting rule);
2. enumerate the values the frozen runner can actually produce — call
   `c1-run.py:build_plan()` (no REA) for each carrier and mode, or replay one dev-arm receipt
   through `provenance_ok()` and the item-3 matcher;
3. require at least one producible value that passes **every** matcher; else exit 2 and refuse
   the freeze.

For round 44 that check fails at step 3 (table above), and it fails for the same reason for the
byte-identity clause (line 36 vs 141). It needs no change to the claim bytes.

## 4. Reverse attack: mint over the committed path, keep a scratch `output_directory`

Independently re-measured; agrees with peer `R44W2C1Satisfy` §4 (H1/H2/H3), whose variant matrix
scores the both-segments form green and the committed-path form red on `run_provenance_ok` alone.
Measured with the frozen `tools/round-27/xpin-attribute.mjs` (the counter's `XPIN`, `:261`), on
the committed `v1le` receipt wrapped as `{"data": §}`; output
`artifacts/R44W2C1HonestStop/xpin-mint-probe.tsv`:

| envelope | stored `evidence_id` | recomputed over its own parameters |
|---|---|---|
| committed receipt, scratch od | `ev_26c313fc…e8144e2` | `ev_26c313fc…e8144e2` (**match**) |
| same receipt, od rewritten to `<LANE>/corpus/evidence/round-44/c1/v1le` | `ev_26c313fc…e8144e2` | `ev_d52fabab…b691ac0` (**mismatch**) |
| same receipt, od rewritten to the both-segments scratch spelling | `ev_26c313fc…e8144e2` | `ev_e186a447…07e055fe` (**mismatch**) |

The stored id depends on the envelope's own `output_directory`; `evidence_id_ok`
(`c1-counter.py:2128`) compares stored with recomputed-from-the-same-envelope. Hence:

* "keep the scratch od, store an id minted over the committed path" → `evidence_id_ok false` on
  all four carriers → `carriers_matched 0`, exit 1. **Detectable; would not have worked.**
* "rewrite the od to the committed path and mint over it" → `provenance_ok false` (§3 table),
  same outcome.
* "point REA at a scratch path that spells `corpus/evidence/round-44/c1/<id>`" → passes
  `provenance_ok` and the id recomputes, but it is **gaming**: the string is not the committed
  evidence path (`c1-run.py:366-380` copies the tree into the lane separately), item 3's purpose
  (bind the id to the committed bytes) is unmet, and the frozen runner cannot emit it without a
  code change. A faithful reading is impossible; the spelling form is a loophole to be closed in
  the next freeze (assert the path is the *lane's* `corpus/evidence/round-44/c1/<id>` **and**
  produced under the scratch root, with the copy digest bound).

## 5. R44-C2 (calibration)

Reproduced at `55bcce69` (command in §7 receipts): `entries_evaluated 80`, `mismatches []`,
`frozen_path_changed []`, `unevaluable_count 0`, `met_target true`, exit **0**, wall 4.545 s,
`counter_sha256 == counter_sha256_at_freeze == 085192ea…36c277`, rubric sha
`e8cc0ded…f55e755e` at freeze and rev. **Confirmed.**

Independent re-derivation of the three repaired values from the freeze tree (own script, not the
rubric): `corpus/knowledge` 137 files, 137 mapped in `corpus/README.md`'s coverage map →
`137/137`; 21 craft rule blocks, 21 with resolving citations → `21/21`; craft section spans
`SKILL.md:81-543`. The three entries observe exactly those (`C2-a1/a2/a4`), and the two pinned
entries keep `133/133` and `20/20` at `e1c83313`/`52b0eb29`.

Attacks:

* **Vacuity — falsified (the rubric is not a green generator).**
  `--rev BASE --freeze BASE --pre-freeze`: exit **1**, `entries_evaluated 80`,
  `mismatches_count 3`, ids exactly `["C2-a1-owned-coverage-count",
  "C2-a2-owned-depth-count", "C2-a4-owned-depth-craft-range"]`
  (`c2-pre-freeze-base-freeze=base.json`). The three target entries really were red at base and
  the repair is what turns them green. Caveat: the literal reading of CTL-C2-0
  (`--rev BASE --freeze FROZEN --pre-freeze`) is **unevaluable**, exit 2
  `frozen_path_changed ["tools/round-44/c2-rubric.json"]`, because
  `c2-counter.py:1186-1196` runs the rubric's self-freeze comparison even in the pre-freeze arm
  and the rubric does not exist at BASE. The control works only with `--freeze BASE`; the claim
  does not say which, so the L1 must record the invocation (HS-4).
* **Free pass — none found.** Changing the English text of the `## Owned axes` row or the
  appended correction block makes `SCORECARD.md` a `frozen_path_changed` (exit 2,
  `appended_block_differs_from_expected_edit` / `not_append_only`) before any entry passes
  (`c2-wrong-note-tamper.json`). A wrong note therefore never passes.
* **Note vs value — substance holds, label does not.** `plans/round-44-claims.md:228-230`
  (and `:256`) promise a per-entry mismatch `note_value_disagrees`. No such verdict exists in
  the counter (`grep note_value_disagrees tools/round-44/c2-counter.py` → no hit); the wrong-note
  arm reaches exit 2 `appended_block_differs_from_expected_edit`, never a mismatch. The CTL-C2-4
  real-base receipt shows the same shape (arm A exit 2 `SCORECARD.md`; arm B demonstrated on a
  *dev* rubric, not the frozen one). "Never a pass" is true; the named verdict is fictional.
* **Exact bytes — not implemented.** `plans/round-44-claims.md:239-240` says
  `blob_at_REV == blob_at_FREEZE + expected_append` exactly. The rubric's
  `expected_edits["SCORECARD.md"]` carries `append` (a 7-line list), not `append_text`, and
  `c2-counter.py:572-579` compares strip-normalised **line identity**; unit probe
  (`c2-append-binding-probe.txt`): `verify_expected_edit(freeze, real_rev)` → `(True,
  'bound_edit')`, and `verify_expected_edit(freeze, rev_with_one_trailing_space_in_the_appended
  line)` → **`(True, 'bound_edit')`**. The claim's literal identity is also false: the real
  delta is `FREEZE + "\n" + block + "\n"` (667 declared bytes, 668 actual) — it needs a blank
  separator line the clause does not mention. Semantic tampering is still caught (line identity
  + `preserve` line digests), so this is a precision defect, not a free pass.

**C2 verdict: MET stands; no vacuity or free-pass found among the 80 entries.** HS-4 and HS-5
are claim-text precision defects that the next freeze must fix (use `append_text`; implement the
note-value check outside the bound block, or drop the named verdict).

## 6. M44-2, the freeze defect, and the preflight

Confirmed facts (my runs):

* `git log --oneline c48f8a4..main -- tools/round-44/` → only `c86ea508`; all **8** paths are
  status **`M`** (modified; none added) — `preflight-c86ea508.json`.
* C1 counter at `c86ea508` and at the actual tip `8bb1090a`: exit **2**,
  `frozen_path_changed` 8 paths. C2 counter: exit **2** at both, **9** paths at `8bb1090a`
  because the record commit itself appends 16 lines to `SCORECARD.md`, which is a C2 frozen path
  with only the C2 correction block tolerated. The lesson's "both exit 2 … instead of 0/1" is
  true; the measured revision is a clean ancestor (`preflight-55bcce69.json`: clean, exit 0), so
  measuring at `55bcce69` is honest and admissible.
* Preflight `tools/round-45/frozen-path-preflight.py` really catches M44-2 with
  `--pathspec tools/round-44`: exit **1** at `c86ea508` (8 `touched`, 8 `blob_changed`),
  exit **0** at `55bcce69`, exit **1** at the tip. Its merge-aware walk (`git log -m
  --diff-merges=first-parent --name-status`) plus the tree backstop match the frozen
  freeze-integrity rule.

Two record defects remain (HS-7, HS-8):

* the lesson says "added/edited 8 files"; every path is `M`, so "added" is wrong;
* the commit's *content* is not recorded. `.ufo/waves/round-44/controls/**` **first appears at
  `c86ea508`** (`git log --diff-filter=A c48f8a4..main -- .ufo/waves/round-44/controls` → only
  `c86ea508`); no committed control receipt existed at the freeze (242 files under
  `.ufo/waves/round-44` at `c48f8a4`, none in `controls/`). And the receipts that landed then
  disagree with the fixtures they describe — measured at `c86ea508`:

  | control | freeze fixture (`c48f8a4`) | post-freeze fixture (`8bb1090a`) | `.ufo/.../controls/<c>/receipt.json` tree | `w1/artifacts/R44C1Controls/.../receipt.json` tree |
  |---|---|---|---|---|
  | `c3` `…/v1le/after.json` | `adba89ea…`/10214 | `8b15697b…`/10404 | **`b3dfd5a9…`/10392** | `adba89ea…`/10214 |
  | `pos` `…/v1be/after.json` | `0cb895d5…`/13813 | `c4ede8bf…`/14439 | **`b7f968ed…`/14424** | `0cb895d5…`/13813 |

  So for `c3` and `pos` there are **three different byte streams** in the lane (freeze fixture,
  post-freeze fixture, committed `controls/` receipt) plus a second receipt set that matches the
  freeze bytes; neither receipt set is reproducible from the committed fixture. `c0/c1/c2/c4/c5`
  receipts do match their fixtures (my per-file digest comparison at `c86ea508`). This is the
  material content M44-2's row omits, and it is the reason round 45 cannot treat the C1 control
  arms as reproducible.

## 7. Numbered defects for the L1

Each carries path:line, the command, its exit code and the observed value. None changes this
round's outcome (C1 not promoted, C2 met); all are round-45 freeze inputs or record fixes.

**HS-1 (high) — the frozen claim's two `output_directory` clauses are incompatible and the
counter implements only one.** (Independently found by peers `R44W2C1Rescore` D1/D4 and
`R44W2C1Satisfy` V4/V5; this seat's contribution is the producibility constraint below.)
`plans/round-44-claims.md:34-35` (corpus path) vs `:137-138` (scratch segment);
`tools/round-44/c1-counter.py:1176-1182,258` implement the scratch form only.
Command (§7 receipt R1) → exit **1**; observed `carriers_matched 4`, all 22 carrier clauses
true, `bindings_false ["province_core_section","province_core_row","frontier_note"]`.
Fix: do not rewrite the claim; record in round 45 that the clause pair is unsatisfiable
faithfully and add the satisfiability preflight of §3(d) before the next freeze.

**HS-2 (medium) — the record omits the instrument's green at `4cc1ac11`.**
`corpus/lessons/round-44.md:1-8,63-75`; `PROVINCE.md:424-430`; `corpus/README.md:104` at
`55bcce69`. Command (§7 receipt R2) → exit **0**, `carriers_matched 4`, `met_target true`,
`bindings_false []`. The committed `corpus/evidence/round-44/c1/counter-at-4cc1.json` carries
`exit_code 0`, `met_target true` with no prose binding it to the withdrawal. Fix: one sentence
naming `4cc1ac11`, exit 0, and the reason the round declined to score on it.

**HS-3 (medium) — `PROVINCE.md:428` / `corpus/README.md:104` state a false cause.**
"The score therefore does not satisfy the frozen predicate" — the predicate paragraph
(`plans/round-44-claims.md:137-139`) is exactly what the four receipts satisfy; the failure is
the amendment sub-clause `:34-35`. Command R1 (exit 1, `run_provenance_ok true` on all four).
Fix: append a correction naming the internal contradiction (the working-tree lesson already
carries the correct qualifier at `:67-75`); do not touch the frozen claim.

**HS-4 (medium) — the C2 "exact bytes" binding is line identity, and its stated identity is off
by one blank line.**
`plans/round-44-claims.md:239-240`; `tools/round-44/c2-rubric.json`
`expected_edits["SCORECARD.md"].append`; `tools/round-44/c2-counter.py:572-579`.
Command (`c2-append-binding-probe.txt`) → `verify_expected_edit` returns `(True,'bound_edit')`
for a rev with a trailing space in the appended line; `blob_FREEZE + append` ≠ `blob_REV`
(667 vs 668 bytes). Fix: use `append_text` with the separator line, or restate the clause as
line identity.

**HS-5 (low) — `note_value_disagrees` is not a verdict the counter can emit.**
`plans/round-44-claims.md:228-230,256`; counter has no such string; measured wrong-note arm →
exit **2** `frozen_path_changed`/`appended_block_differs_from_expected_edit`
(`c2-wrong-note-tamper.json`). Fix: implement the note-value comparison outside the bound block,
or drop the named verdict and state "exit 2 by the freeze rule, never a pass".

**HS-6 (low) — CTL-C2-0's literal invocation is unevaluable.**
`plans/round-44-claims.md:251-252`; `tools/round-44/c2-counter.py:1186-1196`.
`--rev BASE --freeze FROZEN --pre-freeze` → exit **2** `frozen_path_changed
["tools/round-44/c2-rubric.json"]`; `--rev BASE --freeze BASE --pre-freeze` → exit **1**,
3 mismatches (the intended red). Fix: skip the rubric self-freeze comparison in the pre-freeze
arm and record which invocation was run.

**HS-7 (low) — M44-2's "added" is wrong.**
`corpus/lessons/round-44.md:16`; `git show --name-status c86ea508 -- tools/round-44` → 8 paths,
all `M`. Fix: "modified 8 frozen control-fixture files".

**HS-8 (high for round 45) — the control receipts landed post-freeze and disagree with their
fixtures.**
`.ufo/waves/round-44/controls/**` first added at `c86ea508`; `c3` and `pos` receipts' `tree`
digests disagree with both the freeze fixture and the post-freeze fixture (§6 table; measured by
per-file sha256 at `c86ea508`). Fix for round 45: commit control receipts **in the freeze**, and
add a freeze-time check `sha256(fixture file) == receipt.tree[rel].sha256` for every arm.

**HS-9 (low) — the preflight's default contradicts its help text, and its coverage is only its
pathspec.**
`tools/round-45/frozen-path-preflight.py:26-27` ("Default: none (tree backstop only)").
Measured on a fixture with one change **outside** `tools/round-44/`: no `--pathspec` → exit
**1** `frozen_path_changed` on `docs/doc.md`; `--pathspec tools/round-44` → exit **0** clean
(`preflight-{no-pathspec,pathspec}-outside-change.json`). The touched walk is not
pathspec-limited, so a bare call reds every commit; and it only enforces the list it is handed
(peer measurements: 557 paths at the tip; `plans/round-44-claims.md` and
`corpus/evidence/round-44/oracle/` need their own list). Fix: make `--pathspec` required (or read
the claim's frozen set), fix the help text, and wire it to one list shared with the counters.

## 8. Axis impact and what I did not do

* **Coverage (R44-C1)**: the stop's *outcome* is confirmed honest; the *uniqueness* claim is not
  (the predicate reading supports `met`, the amendment reading forbids it; no faithful receipt
  can satisfy both). The carrier-level evidence (4/4, every oracle file, exact paths/digests,
  `projection_ok`, `evidence_id_ok`) was already independently re-derived by peer
  `R44W2C1Rescore`; I reproduced the counter determinism (identical stdout sha256) and did not
  re-audit the extract trees.
* **Calibration (R44-C2)**: MET confirmed and non-vacuous; two claim clauses overstate what the
  instrument does.
* **Freeze integrity**: M44-2 is honestly measured at `55bcce69`; the preflight catches the
  instance; the control evidence it left behind is not reproducible for `c3`/`pos`, and no
  control receipt existed at the freeze.
* I did not run REA, did not touch `c1-run.sh`, and did not re-run the peer's counterfactual
  landings (I reproduced the deciding green at `4cc1ac11` instead).
* I did not re-derive `c1/c2/c4/c5` control receipts beyond their per-file digest match, and I
  did not test the 7-Zip oracle leg the claim mentions (counter binds `unsquashfs` only).

## 9. Receipts

All artifacts under
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-44/w2/artifacts/R44W2C1HonestStop/`;
`sha256-manifest.txt` covers every file there. Scratch deleted after copying; no `/tmp` evidence
path is cited.

| # | command (lane root, absolute) | exit | wall | stdout sha256 | artifact |
|---|---|---|---|---|---|
| R1 | `TMPDIR=<S>/tmp python3 -I -B tools/round-44/c1-counter.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev 55bcce69… --freeze c48f8a4b… --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents --work <S>/work/c1-final --json-out <A>/c1-at-55bcce69.json` | **1** | 7.028 s | `eea45d374bb450f15c549ca5e7c7803ac9e6c31bb982fae45d6542ee8cac9f8d` | `c1-at-55bcce69.json` sha `85561148…f807e8a` |
| R2 | same, `--rev 4cc1ac11… --work <S>/work/c1-4cc1 --json-out <A>/c1-at-4cc1ac11.json` | **0** | 7.3 s | (stdout in `c1-4cc1.log`, scratch; json retained) | `c1-at-4cc1ac11.json` sha `5d579332…0757d076` |
| R3 | same, `--rev 8bb1090a… --work <S>/work/c1-tip` | **2** | 7.6 s | — | `c1-at-tip-8bb1090a.json` sha `784e7a15…48b223` |
| R4 | `TMPDIR=<S>/tmp python3 -I -B tools/round-44/c2-counter.py --root <lane> --rev 55bcce69… --freeze c48f8a4b… --work <S>/work/c2-55 --json-out <A>/c2-at-55bcce69.json` | **0** | 4.545 s | — | `c2-at-55bcce69.json` sha `33092395…ae4328` |
| R5 | same, `--rev BASE --freeze BASE --pre-freeze --work <S>/work/c2-base2` | **1** | 4.6 s | — | `c2-pre-freeze-base-freeze=base.json` sha `2fec8fac…13a88e75`; ids `C2-a1/a2/a4` |
| R6 | same, `--rev BASE --freeze c48f8a4b… --pre-freeze` (literal CTL-C2-0) | **2** | 0.1 s | — | `c2-pre-freeze-base-freeze=frozen.json` sha `d376ee16…75ddc6` |
| R7 | same, `--rev 8bb1090a…` | **2** | 0.05 s | — | `c2-at-tip-8bb1090a.json` sha `db6630f8…d8990`; 9 paths incl. `SCORECARD.md` |
| R8 | fixture `fix2-ws2`: freeze = tree `c48f8a4b`, rev = `55bcce69` SCORECARD + one trailing space in an appended line; c2 counter | **2** (other fixture gaps) | 11 s | — | `c2-trailing-space-tamper.json` sha `a01ce9f…da27a`; `freeze_notes[SCORECARD] = bound_edit_applied` |
| R9 | fixture `fix2-note2`: same with `c2-correction-value: 999/999`; c2 counter | **2** | 11 s | — | `c2-wrong-note-tamper.json` sha `814572e7…d47e6`; `appended_block_differs_from_expected_edit` |
| R10 | `python3 -I -B tools/round-45/frozen-path-preflight.py --root <lane> --freeze c48f8a4b… --rev <c86ea508|55bcce69|8bb1090a> --pathspec tools/round-44` | 1 / 0 / 1 | <0.1 s | — | `preflight-c86ea508.json`, `preflight-55bcce69.json`, `preflight-tip.json` |
| R11 | fixture-outside: change `docs/doc.md` only; preflight without `--pathspec` | **1** | <0.1 s | — | `preflight-no-pathspec-outside-change.json` sha `14f07151…53907` |
| R12 | same with `--pathspec tools/round-44` | **0** | <0.1 s | — | `preflight-pathspec-outside-change.json` sha `ed97cf47…6c486c` |
| R13 | `node tools/round-27/xpin-attribute.mjs --pkg65 … --pkg67 … <three envelopes>` | **0** | <1 s | — | `xpin-mint-probe.tsv` sha `0b97ff0e…c7613` |

## 10. Incidents (self-reported)

While building the "outside-path" preflight fixture I used relative `mkdir`/`printf` paths once;
they executed in the shell's default cwd `/home/vgpnk/Projects/shokunin` (the fleet root) and
created two untracked paths there: `docs/doc.md` and `tools/round-44/f.txt`. Both were removed
immediately (`rm -f` + `rmdir`, directories deleted), and `git -C /home/vgpnk/Projects/shokunin
status --porcelain` no longer lists `docs/` or `tools/`. Nothing tracked was written or modified;
no commit was made in the fleet repo or in the lane. The fixture was rebuilt with absolute paths
and its toplevel asserted. No tool was installed or upgraded.

Report: `.ufo/waves/round-44/w2/R44W2C1HonestStop.md`
