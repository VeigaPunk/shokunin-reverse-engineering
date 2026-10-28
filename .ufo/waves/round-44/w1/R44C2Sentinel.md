# R44C2Sentinel — adversarial review of the R44-C2 rubric + counter design

Seat `R44C2Sentinel` (sentinel). Base `c29360e3ba5381a5ab69e372d0d9577970f85018`; drift checked at
HEAD `3b0fcaa9` (review time). Read-only: this seat wrote only this report and its own probe
scratch (`/fast/scratch/hyaku/kaidoku-r44/probe-R44C2Sentinel`, `probe-` prefix honored). No REA
run, no network, no lane mutation, no new fixture driver.

## What was reviewed, and what did not exist yet

- `plans/round-44-claims.md` at `fc5eb54a` (the draft; R44-C2 at `:128-166`, landing mechanics at
  `:224-233`, frozen-path list at `:207-222`).
- The C2 seat contracts in `.ufo/waves/round-44/w1-spec.json` (`R44C2Rubric`, `R44C2Counter`,
  `R44C2Controls`) — these carry the rubric schema and the counter's step list, which the claims
  file only summarises.
- Prior counters `tools/round-39..43/*-counter.py` for the freeze-walk and `counter_sha256`
  conventions the port must inherit.
- **Not present at review time:** `tools/round-44/` does not exist; no `c2-rubric.json` and no
  `c2-counter.py` draft in `.ufo/waves/round-44/w1/artifacts/`. "Does the counter catch it?" below
  therefore means *the behaviour the frozen contract prescribes* (claims + seat contract step list),
  plus what an implementation following that text literally will do. Re-check the landed artifacts
  against §Checklist before the freeze.

## Measured ground truth (command A, frozen recipe, git objects only)

| rev | knowledge_files / mapped | citation_resolved_rules / rule_blocks | what SCORECARD asserts for it |
|---|---|---|---|
| `c29360e3` (R44 base) | 137 / 137, `missing []`, `dangling []` | 21 / 21 | — (no pin) |
| `4d62ee5a` | 130 / 130 | 19 / 19 | `SCORECARD.md:23` "130/130 … command A at `4d62ee5a`" ✓ |
| `e1c83313` | 133 / 133 | 20 / 20 | `SCORECARD.md:23` "133/133 … at `e1c83313`" ✓; `:24` "20/20 … at `e1c83313`" ✓ |
| `8de80f1d` | 137 / 137 | 21 / 21 | `SCORECARD.md:3508` "`knowledge_files=137`, `mapped=137` … `citation_resolved_rules=21/21`" ✓ |

Every pinned value reproduces **at its own revision** and differs at REV. That is correct
self-assessment, and it is the exact input to B1.

Also measured: 12 sampled `## Capabilities` evidence pointers all resolve at base (`.ufo/waves/
luna-round-6/receipts`, `…/luna-round-8/receipts`, `…/arc2-loop1-round2/receipts/config-pre-pair.txt`,
`corpus/evidence/round-36/c1`, `tools/round-36/c1-run.sh`, `tools/round-41/c1-counter.py`,
`.ufo/waves/round-41/l1/scores/c1-at-e9a24d07.json`, `.ufo/waves/round-40/l1/scores/c2-at-42c10a58.json`,
`tools/round-27/c2-xpin-check.py`, `.ufo/waves/round-27/w1/BuildXpinTool.md`,
`.ufo/waves/round-14/verification.json`, `.ufo/waves/round-17/run-carriers.sh`). Pointer existence
is therefore currently green *and* uninformative — see H2.

---

# Blocking findings

## B1 — Rev-mixing turns every historical pin into a false mismatch, and the sanctioned repair rewrites history

**Contract text.** `plans/round-44-claims.md:136-137` makes category (b): "the `## Owned axes`
row's pinned counts reproduce under its own `command A` **at REV**". `:229-230` makes a mismatch
repairable because "the rubric's check is re-run against the appended note". Target `:161` is
`mismatches == 0`.

**Exploit.** Entry `C2-b-coverage-133`, `asserted = "133/133"`, check = command A at REV.
- At BASE the check returns 137/137 → mismatch. It is a **false** mismatch: `SCORECARD.md:23` says
  133/133 *after the round-41 landing … command A at `e1c83313`*, which is true (measured 133/133).
- "Repair": append a dated note carrying 137/137. Per `:229` the check is re-run against the note /
  at REV, sees 137/137, and the entry is green.
- Net state: the frozen cell still asserts a pin at `e1c83313`, the appended note contradicts that
  pin inside the same cell, the round reports a calibration repair, and the counter reports
  `mismatches == 0`. Nothing in the counter reads the `at <rev>` qualifier, so the contradiction is
  invisible.
- Identical path for depth: `SCORECARD.md:24` "20/20 … at `e1c83313`" — measured 20/20 there, 21/21
  at REV.

Worse, the same mechanism falsifies *history*: B5's demo variant replaces the round-43 closure
correction "R43-C2 … not met" with "R43-C2 was met …" and appends the correction block; the note
check passes.

**Does the frozen counter catch it?** No. It compares one observed value to one transcribed asserted
value at one revision. There is no rev-qualifier binding and no contradiction check.

**Smallest fix.** Rubric entry gains three fields and the counter enforces them:
1. `pin_rev` extracted from the *same base line* (regex `at\s+\`([0-9a-f]{7,40})\``); if the entry
   declares a different `pin_rev`, exit 2 (`pin_rev_disagrees_with_line`).
2. A pinned entry is checked **only** at its pin (materialise that rev, H4). A REV-state entry is
   checked only when the line carries no rev qualifier.
3. An entry's `asserted` must be a byte substring of the BASE blob's `line_at_base` (see B2).
4. The appended block may not contain a value for a pinned entry (a pinned statement is immutable
   history; only a *new* dated statement can supersede it, and the superseding statement must itself
   be a REV-state entry with its own re-derivation).

**Evidence.** Measured table above; receipts R-01..R-05. `SCORECARD.md:23,24,3508`;
`plans/round-44-claims.md:136-137,229`.

## B2 — `asserted` has no provenance binding: the rubric can be authored to match the wrong value or to manufacture the base mismatch

**Contract text.** Rubric schema (`.ufo/waves/round-44/w1-spec.json` → `R44C2Rubric`):
`{id, file, line_at_base, asserted, check:{argv,cwd}, expected, note}`; counter step (2) compares
check output to `asserted`. `asserted` is a free transcription with no link to the base blob.

**Exploit A — green without work.** Author writes `asserted = "137/137"` for `SCORECARD.md:23`
(the line says 133/133). At REV observed 137/137 → match → no mismatch; the frozen statement is
still falsified in future rounds and the counter says "clean".
**Exploit B — manufactured work.** Author writes `asserted = "136/136"` for the same line. Base
mismatch is guaranteed, so CTL-C2-0 is red by construction and the do-nothing control proves
nothing; one appended note repairs it (B3).
**Exploit C — census conformance.** `R44C2Rubric`'s instruction is "assemble from R44ScoutCalib's
census". A census row with a transcribed `observed` that does not equal the check's own output is
indistinguishable from a genuine mismatch, and the census JSON is authored, not derived.

**Does the frozen counter catch it?** No. It never reads the BASE blob against `asserted`.

**Smallest fix (three bindings, all cheap):**
1. Pre-score: for every entry, `asserted.encode() in blob(BASE, entry.file)` restricted to
   `line_at_base`, and `entry.line_sha256 == sha256(that line)`; otherwise exit 2
   (`asserted_not_in_base_line`).
2. Pre-score: the counter re-runs the entry's check at BASE and requires the result to equal the
   census's committed `observed_at_base` (the census is committed in the freeze, so drift is
   visible); disagreement is exit 2, not a mismatch.
3. `mismatch` requires `observed_at_rev != asserted` **and** `observed_at_rev` re-derived by the
   frozen check from git objects — never from the note (B3).

## B3 — A correction note forgives any mismatch and the note needs no truth value

**Contract text.** `plans/round-44-claims.md:229-230`; seat contract `R44C2Counter` step (3):
"a mismatch = check output != asserted AND no appended supersession/correction note at REV makes
the check pass".

**Exploit (demonstrated).** Delete a capability evidence path at REV (or simply leave a dead
pointer) and append `- C2-a-01: corrected`. Under the weakest reading — the entry id appears in an
appended block → repaired — the entry is green although the pointer still does not exist. The same
weak rule is green for a note carrying a *wrong* value:

```
weak rule  (mismatch unless id appears in appended note): deleted pointer → True, note "corrected to 999/999" → True
hard rule  (mismatch unless the pinned check re-derives the asserted value): deleted pointer → False, wrong-value note → False
```

`R44RevKill.md` K6 reaches the same conclusion from the control side; this report fixes the exact
rule.

**Does the frozen counter catch it?** No, as written. The note is treated as evidence of repair.

**Smallest fix.**
1. A note is never evidence. The check must be re-run on the repo state at REV and must pass on its
   own output (`observed == asserted` after the entry's own derivation).
2. If a note is allowed to declare the authoritative value, the counter must independently re-derive
   that value and compare: the note is a *declaration*, the derivation is the *proof*. A note whose
   number disagrees with the derivation is a mismatch (`note_value_disagrees`) — not a pass.
3. Control: append a note carrying a wrong value; expect exit 1 with that entry id
   (`R44RevKill` K6 asks for the same control).

## B4 — `check.argv` is free-form: trivially green, and it executes committed data as a command

**Contract text.** Schema `check:{argv, cwd:'scratch-clone'}`; counter materialises REV and runs
the argv. No allow-list, no script pin, no env scrub.

**Exploit 1 — trivially green (always-true).**
`{"id":"X","asserted":"137/137","check":{"argv":["sh","-c","echo 137/137"],"cwd":"scratch-clone"}}`
matches on every revision without reading the repository. `["true"]`, `["test","-e",…]` and a
`grep` of the asserting file itself are the same class. The frozen counter cannot distinguish these
from a real check; CTL-C2-1 (one seeded entry) does not sample the other entries, so any number of
degenerate entries passes.
**Exploit 2 — degenerate inventory.** Empty rubric, or all entries `expected:"superseded"` →
`mismatches == 0` → target met with `entries_evaluated == 0` (H1).
**Exploit 3 — data-supplied execution.** The counter executes `argv` from committed JSON with
`cwd` in the scored tree. A pre-freeze-corrupted rubric can run `git checkout`/writes inside the
clone, read absolute paths outside it (an answer file under `/tmp` or the lane), or fetch a precomputed
answer over the network. `python3 -I -B` on the *counter* constrains nothing about the child.
**Exploit 4 — environment leakage.** A check that reads `$HOME`, `$HYAKU_SCRATCH` or a sibling
lane can be satisfied by bytes that are not in the scored tree.

**Does the frozen counter catch it?** No — all four are schema-legal.

**Smallest fix.**
1. Replace `argv` with `{script: "tools/round-44/checks/<name>.py", script_sha256, args:[…]}`; the
   counter requires `blob(REV, script)`'s sha256 to equal the frozen `script_sha256`, else exit 2
   (`check_script_drift`).
2. Execute `[sys.executable, "-I", "-B", script, *args]` with `shell=False`, `cwd` = the materialised
   tree, `env` = a fixed minimal dict (`PATH` pinned, no `HOME`, no proxy vars, `TMPDIR` under
   `--work`), and reject any arg that is absolute or resolves outside the tree.
3. Fitness gate at freeze: every check must be shown able to fail on *its own* entry (mutate the
   entry's asserted value in a scratch tree, expect mismatch). One mutation per entry, not one per
   control. This is the only defence against a rubric full of always-true entries.

## B5 — The `frozen_path_changed` relaxation cannot be implemented as specified; every implementable weakening admits an arbitrary in-place edit

**Contract text.** `plans/round-44-claims.md:224-233`: the frozen blobs "stay equal at FREEZE and
REV" *and* repairs are appended; then "the `frozen_path_changed` arm for that file is relaxed ONLY
for the rubric-named paths and the diff is bound to equal exactly the rubric's expected edit bytes
… row-identity checks over the appended block, never raw numstat".

**Why the exact-bytes form cannot cover this round.** The SCORECARD/SHONEN landing the round needs
— a claim table carrying the measured revision, receipt paths and score hashes — is produced
*after* REV by definition (`SCORECARD.md:3470-3486` is the round-42 example; the committed-table
values are score outputs). Those bytes cannot be in the pre-freeze rubric. So `expected_edit` can
only bind the *census-derived* corrections; the round landing must sit outside the frozen set. If it
is left inside with a weakened arm, the weakened arm is what the round actually exercises.

**Demonstration (real `SCORECARD.md` base blob).** `E` = a plausible correction block. `A` =
base + `E`. `B` = base with the round-43 closure line replaced by a fabricated verdict
("R43-C2 was met at `77d196c6`; the frozen scorer was overstrict") + the same `E`.

| guard | A | B |
|---|---|---|
| "E is a suffix of the blob" | true | **true — arbitrary edit accepted** |
| "blob == base + E, byte-for-byte" | true | **false — rejected** |
| numstat-shaped (`git diff --numstat`) | `1\t0` | `2\t1` — rejected only if deletions are forbidden |

Receipt R-06. `B`'s edit is precisely the fraud class the round must not admit: it retracts a frozen
"not met" verdict and no appended block reveals it. And the repo has already paid for numstat-bound
frozen checks: round 43's R43-C2 failed on `3\t0` vs `4\t0` (`SCORECARD.md:3489-3497`).

**Does the frozen counter catch it?** Only under the exact-bytes form. The three weakenings the text
invites — "expected block present", "append-only region", "row-identity over the appended block" —
do not.

**Smallest correct relaxation (all clauses, none optional):**
1. `tools/round-44` stays a **directory** freeze prefix in the walk (git pathspec on the directory,
   not an explicit file list), so a post-freeze added check script or rubric sibling is a change;
   apply the `A` rule to a new file under a frozen directory and record each blob.
2. For `SCORECARD.md`/`SHONEN.md`/`corpus/README.md`/`corpus/SOURCES.md`: drop whole-blob equality.
   Freeze `line_sha256` for every cited line; require every cited line byte-identical at REV;
   require `blob_at_REV` to start with `blob_at_FREEZE` (zero deletions) and every added line to
   begin after the FREEZE blob's final byte.
3. For repairs whose bytes are known pre-freeze (the census-derived corrections): `expected_append`
   exact bytes in the rubric, `expected_append_sha256` frozen, and the requirement
   `blob_at_REV == blob_at_FREEZE + expected_append` byte-for-byte. No region, no marker, no
   containment, no count.
4. The round-44 landing section is not a repair: it lands in a commit after REV or in a separate
   file outside C2's frozen set. Never a region-scoped relaxation.
5. Any file frozen by *both* C1 and C2 (README, SOURCES) is irreconcilable as drafted — `R44RevKill`
   K1/S1 and `R44ConnSibling` already flag the landing contradiction; the C2-specific addition is
   that the only correct resolution is **per-claim frozen sets** (C2 must not freeze bytes C1's
   landing must change) plus B6's attribution, not a shared relaxation.

## B6 — `mismatches == 0` is hostage to C1's landing, and the counter cannot attribute a mismatch

**Contract text.** `plans/round-44-claims.md:183` makes the row-count check read the count at REV
(correct), but C1's landing adds one knowledge file *and* one index row. Measured: base 137/137; a
correct C1 landing gives 138/138; a file-only landing gives 138 files / 137 mapped → mismatch.
**Exploit / failure.** C2's target becomes unreachable because of a sibling's partial landing; per
B3 the tempting "repair" is an appended note about C1's surface — C2 editing a surface it does not
own, and (with B5) an appended block that the relaxation cannot police.

**Does the frozen counter catch it?** No. It reports a count, not an origin.

**Smallest fix.** The check derives both sides at REV and reports
`{knowledge_files, mapped, missing[], dangling[]}`; the counter records `mismatch_origin` (the first
commit that introduced the state, or `sibling:<claim>` when the path belongs to another claim) and
reports `mismatches_self` and `mismatches_sibling` separately. The claim target is
`mismatches_self == 0`; a sibling-caused mismatch stops the claim honestly and does not license a
note on the sibling's row.

## B7 — CTL-C2-0 and the honest-stop gate are unevaluable under the frozen command shape

**Contract text.** `plans/round-44-claims.md:162` gives the C2 counting command as
`--rev <REV> --freeze <FREEZE> --work <SCRATCH> --json-out <OUT>`; CTL-C2-0 scores **BASE**
(`:155-157`) and the kill rule (`:164-165`) is "CTL-C2-0 green before data (0 mismatches at base)
stops C2".

**Measured.** Freeze-integrity requires FREEZE to be an ancestor of REV. For round 43,
`base → freeze` is an ancestor (exit 0) and `freeze → base` is not (exit 1). So
`--rev BASE --freeze FREEZE` hits `freeze_not_ancestor_of_rev` → exit 2, and a counter that always
exits 2 there satisfies "exits non-zero". The honest-stop gate — the one control that would end C2
if the census found nothing — cannot run with the specified command and cannot be witnessed in a
receipt.

**Fix.** An explicit pre-freeze mode: `--rev BASE --freeze FREEZE --pre-freeze` (or `--base BASE`),
which skips the walk, records `freeze_walk: skipped_pre_freeze` in the receipt, and still emits
`entries_evaluated`, `mismatches`, `mismatches_by_category`, `mismatches_self`. The gate reads:
`mismatches_at_base == 0 ⇒ stop C2`. The receipt must show the counts, not just an exit code.

---

# Hardening (non-blocking, but each is a concrete false-green today)

**H1 — degenerate rubric.** `mismatches == 0` is vacuous for an empty rubric or an all-`superseded`
one. Bind a frozen `inventory_sha256` over the census's sorted entry ids; the rubric's id set must
equal it exactly; `entries_evaluated == len(entries)`; `superseded` entries are counted and reported
as a headline; a `superseded` entry needs a resolvable at-BASE reference (blob/path or cited line
sha) or it is exit 2.

**H2 — pointer existence is not evidence.** 12/12 sampled capability pointers resolve at base, so
`test -e` is green now and stays green for a stub: create an empty file at a dead pointer path at
REV. Freeze the pointer's blob hash at BASE (`git cat-file -e BASE:path` plus the blob sha) and
report it; a pointer created at REV is `fabricated_pointer` (exit 1), not a repair.

**H3 — self-reference discriminator.** The question is not "does the check read a file" but "is
there a second source of truth". SCORECARD's `137/137` must be checked by counting
`git ls-tree corpus/knowledge` and command A's mapped stem set — never by grepping SCORECARD/README
for `137`. For SHONEN's "`PROVINCE.md:97-125` byte-identical at `52b0eb29`" there is no second copy:
either freeze a reference blob hash and name the other side of the comparison, or drop the entry
with a recorded reason.

**H4 — pinned-rev checks need git objects.** The contract materialises REV with `git archive`
(no `.git`), so a check that re-runs command A at a pinned rev fails (`git` not a repository; this
seat hit exactly that: exit 1 / git 128 when run from a non-repo cwd) and a naive implementation
falls back to the worktree — which is B1's false mismatch. Materialise each distinct rev once
(`git archive <rev> | tar -x`), pass `--tree <dir>`, and list `rev_trees` in the receipt.

**H5 — category (e) trusts a mutable receipt field.** A cited receipt is committed JSON; editing
`exit_code` 1→0 flips "not met" to agreement. Freeze every cited receipt blob and its counter blob;
require the receipt's `counter_sha256` to equal the frozen counter blob's hash, and (cheap) re-run
the frozen counter at that rev and compare the whole receipt. Rounds 42/43 counters already record
their own exit code — reuse that, do not trust it.

**H6 — category (d) fuzzy match is a green generator.** Keyword overlap between a
`planned (round N+1)` row and the next round's section is near-always true. Concretely:
`planned (round 43)` promises a R42-C2 refreeze and a wave-2 attack; round 44 worked SquashFS
v1/v2 — an honest round steered away (`SCORECARD.md:3498, :3507`). Score only token-bound
statements: the plan row must name `R{N+1}-C{k}` or an existing knowledge/evidence path/stem, and
the check is membership of that token in the N+1 section. Prose plans are dropped with a reason.

**H7 — receipt completeness.** The C2 receipt must carry seat, command, exit, stdout sha256, wall,
`counter_sha256`, `counter_sha256_at_freeze`, `rubric_sha256`, `rubric_sha256_at_freeze`,
`entries_evaluated`, `mismatches_by_id`, `mismatches_self`/`mismatches_sibling`, `rev_trees`, and the
`frozen_path_changed` list. Without `rubric_sha256_at_freeze` the rubric freeze is not provable from
the receipt (round-41 D4 class).

---

# What this review does **not** call a bypass

- Reading the same *file* is not self-reference when both sides are independently derived: the
  README row-count check is legitimate because `knowledge_files` comes from `git ls-tree` and
  `mapped` from command A's stem extraction. The failure mode is only reading the asserted value out
  of the text that carries the claim.
- Freezing `c2-rubric.json` under `tools/round-44/` does work as CTL-C2-3 claims, *provided* the
  freeze prefix is the directory (B5.1). The residual risk is the pre-freeze authorship window
  (B2/H1), not mid-round editing.
- `expected:"superseded"` is legitimate when its reference resolves at BASE; it is a shrink lever
  only without H1's inventory binding.

# Freeze checklist (apply to the landed rubric + counter)

1. `asserted` is a byte substring of `blob(BASE, file)` at `line_at_base`, and `line_sha256` matches
   (B2).
2. Every entry has a `pin_rev` extracted from its own line, or none; pinned entries are scored only
   at the pin (B1).
3. `check` is `{script, script_sha256, args}`, `shell=False`, scrubbed env, tree-contained args (B4).
4. Each entry's check is shown able to fail on its own entry (one mutation per entry) (B4.3).
5. `expected_append` byte-equality — not containment, not a region, not numstat (B5).
6. Per-claim frozen sets; no file frozen by both C1 and C2 (B5.5); `tools/round-44` frozen as a
   directory (B5.1).
7. `--pre-freeze` mode exists and CTL-C2-0's receipt carries `entries_evaluated` and
   `mismatches_at_base` (B7).
8. Receipt carries `rubric_sha256_at_freeze` and per-category mismatch counts (H7).

# Receipts

All commands run by seat `R44C2Sentinel`; `sha256_stdout` is the first 16 hex of the stdout sha256;
`exit` is semantic (0 clean, 1 not met, 2 unevaluable).

| id | command | exit | sha256_stdout | wall | stdout (trimmed) |
|---|---|---|---|---|---|
| R-01 | command A `--rev c29360e3` | 0 | `ae2fa5a4f6dd103b` | 0.10s | `knowledge_files 137, mapped 137, missing [], dangling [], citation_resolved_rules 21/21` |
| R-02 | command A `--rev 4d62ee5a` | 0 | `963a187dbd28e2a4` | 0.10s | `130/130, 19/19` |
| R-03 | command A `--rev e1c83313` | 0 | `d70a5800cf6407f4` | 0.10s | `133/133, 20/20` |
| R-04 | command A `--rev 8de80f1d` | 0 | `ae2fa5a4f6dd103b` | 0.10s | `137/137, 21/21` |
| R-05 | 12 capability pointers via `git cat-file -e c29360e3:<path>` | 0 | `f4d3f1452008dd4f` | 0.02s | 12× `EXISTS` |
| R-06 | relaxation demo (suffix-containment vs exact blob) | 0 | `6e6f326f0b3b97d6` | 0.02s | `A_suffix True, B_suffix True, A_exact True, B_exact False`; `A_sha fda5aae496385cb2`, `B_sha 04825d2820064181` |
| R-07 | `git merge-base --is-ancestor 6b9e64fe f3f8db38` (base→freeze) | 0 | `01ba4719c80b6fe9` | 0.00s | (empty) |
| R-08 | `git merge-base --is-ancestor f3f8db38 6b9e64fe` (freeze→base) | 1 | `01ba4719c80b6fe9` | 0.00s | (empty) |
| R-09 | `git log -1 --format=%H` (lane HEAD at review) | 0 | `d72cc836adbe6e43` | 0.00s | `3b0fcaa9e03bda6059d247bcb99a3d5d9fde94f7` |

Scratch: `/fast/scratch/hyaku/kaidoku-r44/probe-R44C2Sentinel/` (`cmdA.py`, `relax.py`,
`scorecard.base.md`, `expected.block.md`, `scorecard.A.md`, `scorecard.B.md`, `receipts.tsv`).

# Residual risk

- The review is contract-level: no `c2-rubric.json` or `c2-counter.py` existed when it ran, so
  "counter catches it" answers describe the frozen contract. If the landed counter deviates from the
  contract in a way that closes or widens a vector, this report understates or overstates that
  vector; re-run §Checklist against the artifacts before the freeze.
- No REA, no network, no C1 data procedure. The only derived values here come from command A and git
  object reads.
- The base mismatch inventory is not enumerated by this seat (the census seats own it). What was
  verified here is that pinned values reproduce at their pins and differ at REV — the condition that
  makes B1 live — not how many genuinely stale statements exist.
