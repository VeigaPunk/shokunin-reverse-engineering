# R44W2Distill — de-duplicated, ranked wave-2 findings

Seat `R44W2Distill` (critic). Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Freeze `c48f8a4bfd449300c975668e59aae5b5538b6a84`; admissible measured revision
`55bcce69c2f4854958d054bcab6d5f0c6fb8a6ac`; base `c29360e3ba5381a5ab69e372d0d9577970f85018`;
dispatch tip `c86ea508`; record commit `8bb1090a`; **final HEAD at write `4503fb78`**.

No claim, counter, rubric, frozen byte or production doc was changed. Every mutation lived in a
throwaway `git clone --shared` under `/fast/scratch/hyaku/kaidoku-r44/R44W2Distill/`, with
`git rev-parse --show-toplevel` asserted equal to the clone path before each commit and a throwaway
identity on every fixture commit. Scratch deleted before yield. No tool installed or upgraded
(pacman paused host-wide; nothing was needed).

## Scope and inputs

- **Peer report set: all 41 non-`Distill` registry seats are present at write time** — 41 `.md`
  files, verified against `.ufo/waves/round-44/w2/swarm-registry.json` (42 members including this
  seat). **No peer file is absent, so no absence needs explaining.** Two seats landed late relative
  to my first listings (`C1HonestStop`/`C2Rescore`/`C2Vacuity`/`C2Corrections`/`Axes`/`SentEnvelope`
  and finally `Record`); that lateness is a scheduling observation only and is **not a finding**.
- `R44W2ConnDefects.md` already produced a consolidated `R45-01..R45-43` table from 40 reports. This
  file does **not** renumber it. Where a cluster below maps 1:1 onto an `R45-nn` row I say so; where
  I merge several `R45-nn` rows into one defect, or split one row, I say that too. My job is the
  decision layer `ConnDefects` does not make: **what changes a verdict or the round-45 plan.**
- The record moved three times during the wave (`8bb1090a` → `923fa870` → `4503fb78`) as the L1
  folded peer findings in. The worktree is **clean** at write, and every "status at HEAD" below was
  measured at `4503fb78`, not inherited — a peer that quotes `8bb1090a` is describing a state that no
  longer exists.
- I re-measured the three contract items myself (receipts §7) rather than trusting any peer.

---

## 1. Ranked, de-duplicated finding list

Rank key — **P1** = changes a verdict the round report states, or must be fixed before the report
is filed; **P2** = changes the round-45 plan; **P3** = record hygiene, no verdict effect;
**DROP** = style, process, or an already-satisfied confirmation.

### C-1 (P1, KEEP) — The C1 stop is recorded as a *provenance* red; the measured red is the three withdrawn promotion-document bindings

The frozen counter at `55bcce69` returns `carriers_matched 4`, `met_target false`, exit 1 with
`failing []` and `bindings_false ["province_core_section","province_core_row","frontier_note"]`.
`run_provenance_ok` and `path_shape_ok` are **true on all four carriers**. The disputed field
(`parameters.output_directory`) was evaluated and **passed**; the red is caused by the honest-stop
landing deleting the Core row/heading/note it was itself required to hold.

- **Merged sources:** C1Rescore D1 · C1Satisfy V4/D-1 · FreezeViolation FV-1 · C1Oracle §8/§9 ·
  Province D1 · ConnCross #2 · Readme D3 · Entry D1 · C1ReceiptAudit §3.3/D4 · C1HonestStop HS-2 ·
  Simplifier §3.1 (**contradicts** — see §3) ⟶ `R45-01`.
- **Strongest evidence pointer:** `.ufo/waves/round-44/l1/c1-score-at-55bcce69.json`
  (`bindings_false`, `failing`, `carriers.*.run_provenance_ok`). Independently reproduced at §7 R1.
- **Status at HEAD `4503fb78`: half-fixed.** `LOG.md:3201` and `corpus/lessons/round-44.md` now state
  the correct cause. `PROVINCE.md:428`, `corpus/README.md:104`, `corpus/README.md:224` and
  `corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md:3-9` **still** say
  "The score therefore does not satisfy the frozen predicate" / "disagree on output-directory
  provenance". Measured: `git show HEAD:PROVINCE.md | grep -c 'does not satisfy the frozen predicate'`
  → `1`. The remedy commit's own message claims it corrected the C1 cause; it did not touch these
  three surfaces.
- **Verdict effect:** the report's C1 paragraph states a false causal chain. Must be fixed before
  filing.

### C-2 (P1, KEEP) — "No run can satisfy the whole frozen claim" / "internally unsatisfiable" is false as written

Three independent falsifiers, all measured:

1. the round's **own committed receipt** at `4cc1ac11`: exit 0, `carriers_matched 4`,
   `met_target true`, `bindings_false []`, `frozen_path_changed []`, over the **same** receipt bytes
   (evidence digests identical to the `55bcce69` run — verified field-by-field);
2. a scratch path can carry **both** strings (`…/kaidoku-r44/<run>/rea-out/corpus/evidence/round-44/c1/<id>`)
   and `provenance_ok` accepts it (peer H2, exit 0 `met_target true`);
3. **my minimal variant:** restoring only `PROVINCE.md` (3 changed lines — heading, row, frontier
   note) onto the real `55bcce69` tree, with no other change, makes the frozen counter exit **0**,
   `met_target true`, `bindings_false []` (§7 R3).
The correct statement is narrower: the clause was **unrealized by this round's receipts**, and the
frozen runner cannot produce the joint-spelling path, so no *faithful* run satisfies both.

- **Merged sources:** C1Rescore D2 · C1Satisfy V5/V6/D-1 · FreezeViolation FV-1 §7 · C1Oracle §9 ·
  Readme D3 · ScribeShonen D5 · ConnSibling D5 · C1HonestStop HS-1/HS-3 (**refines**: "no *faithful*
  run") · Simplifier §3.1 (**contradicts**) ⟶ `R45-02`.
- **Peers disagree and the disagreement is resolvable, not a defect:** `C1HonestStop` HS-1 says no
  faithful run satisfies both; `C1Satisfy` says H2 satisfies both literally. Both are true — H2 is a
  naming loophole the frozen runner cannot emit (`c1-run.py:331-334`). Merge as "jointly satisfiable
  in letter, unrealized in practice".
- **Status at HEAD: fixed in `LOG.md`/lesson (the lesson now says "not literally unsatisfiable" and
  names the H2 variant); NOT fixed in `PROVINCE.md:428`, `README.md:104/:224`, entry `:3-9`** (same
  three surfaces as C-1).
- **Verdict effect:** yes. The report must not claim unsatisfiability; it may claim "unrealized by
  this round's receipts; the landing was withdrawn rather than restated".

### C-3 (P1, KEEP, **NEW — no peer has this**) — C2's bound-edit freeze arm does not implement "a later restore does not un-block"

`plans/round-44-claims.md:78-80` states the rule for **both** claims: "…each frozen regular-file
blob at FREEZE equals the blob at REV; **a later restore does not un-block** (exit 2
`frozen_path_changed`, never `met_target`)." The two counters implement it differently:

| instrument | break → restore on a frozen path | measurement |
|---|---|---|
| `c1-counter.py:1629-1684` (`frozen_drift`) | **still exit 2**, path still listed | §7 R6 (`prior-pins.json`) |
| `c2-counter.py:636-661` (`freeze_integrity`, `edit is not None` branch) | **exit 0, `frozen_path_changed []`, 80/80, `met_target true`** | §7 R5 (`SCORECARD.md`) |

Mechanism: for a path carrying an `expected_edit`, `c2-counter.py:649` short-circuits on
`rev_bytes == freeze_bytes` → `state: unchanged` **before** consulting the `touched`/`statuses`
vector computed at `:630-635`, and `verify_expected_edit` never looks at it either. A commit in
`FREEZE..REV` that wrote anything to the path is invisible at the endpoint.

- **Why this is P1 and not a curiosity:** the L1's own M44-3 remedy **is** this shape. `8bb1090a`
  appended an unauthorized `## Round 44` section to `SCORECARD.md` (C2 then reported **9** paths);
  `923fa870` restored the blob and the record now cites "the C2 counter at the final tip lists 8
  paths with `SCORECARD.md` absent" as *proof the fix works* (`corpus/lessons/round-44.md:19`,
  "Shown able to fail: …"). Under the rule the round froze, the correct final-tip answer is **still
  exit 2 with `SCORECARD.md` listed** — history does not un-happen. The demonstration of the fix is
  therefore a demonstration of the hole.
- **Receipts:** §7 R5 (C2: `0eaa4c75` exit 2 `SCORECARD.md` → `043a83ba` exit 0 `met_target true`,
  stdout sha256 `a642ac89…`) and §7 R6 (C1: same shape still exit 2).
- **Verdict effect:** the report may keep "the round measures at `55bcce69`" (the tip is
  inadmissible either way), but it must not present "SCORECARD absent at the final tip" as proof
  that M44-3 was remediated. Round-45 plan: add an endpoint-independent touched check to C2 (and to
  the preflight) before either is trusted as a gate.

### C-4 (P1, KEEP) — The M44-2 "fix" is a detector with three holes; it does not cover the frozen class

Measured with the record's own invocation (`--pathspec tools/round-44`): exit **1** at `c86ea508`
(8 touched / 8 blob), exit **0** at `55bcce69` — so it *does* catch the incident. It does **not**
cover the claim's frozen set:

- `corpus/evidence/round-44/oracle/` is frozen by C1 (`FROZEN_PREFIXES`) but is outside the recorded
  pathspec: I committed a one-line edit to `corpus/evidence/round-44/oracle/manifest.json`; preflight
  returned **`clean`, exit 0**, while `tools/round-44/c1-counter.py` at the same revision returned
  **exit 2 `frozen_path_changed ['corpus/evidence/round-44/oracle/manifest.json']`** (§7 R4). Same
  result peers report for `plans/round-44-claims.md` and for `A`-status files.
- no `--pathspec` → the tree backstop is skipped and the walk is unfiltered: exit **1** at
  `55bcce69` with **110** touched paths (542 at `c86ea508`) — a false red on the very revision the
  record calls green (§7 R8).
- `rev == freeze` → exit 0 (`clean`); unknown rev / freeze-after-rev → exit 2. Exit semantics are
  otherwise correct (§7 R8).
- not wired: nothing invokes it; `.git/hooks` holds samples only and the lane is a **jj** repo, so a
  git hook would never fire; no dirty-tree arm, although the frozen fixtures were dirty from 09:50.
- **Merged sources:** C1Rescore D7/D8 · Preflight D-1/D-2/D-3 · C1ReceiptAudit D6 · Quality77
  D4/D5/D6 · LessonGate D7 · ScribeShonen D4 · C2Freeze F-6 · Simplifier S-2/S-3 ⟶
  `R45-08/R45-09/R45-11/R45-12`.
- **Verdict effect:** "honest and sufficient" is right on honesty and **wrong on sufficiency**. The
  round-45 plan must carry the pathspec-set requirement and the endpoint-independent walk.

### C-5 (P2, KEEP) — C2's "three repairs scored 80/80" overstates what the instrument verified

Measured by me:

- **B2 gate is unimplemented and incompatible with its own rubric:** for **71 of 80** entries the
  `asserted` string is **not** a substring of the base line the rubric names (`line_sha256` matches,
  so the line is right and the claim's B2 rule is not the implemented semantics). §7 R9.
- **The three target entries free-pass their own statement:** they read the appended
  `c2-correction-value` block instead of the row they repair. I removed two knowledge files
  (138 → 136) and the frozen counter returned **only** `C2-h2-readme-knowledge-entries-resolve` as a
  mismatch — `C2-a1-owned-coverage-count` stayed green while its subject moved (§7 R10). The three
  corrected values are also freeze-scoped: command A at `55bcce69` is `138/138`, not `137/137`
  (peer C2Corrections C-3, `R45-07`).
- Six entries are "steered" green generators (`observed` literal equals `asserted`); `C2-h1` is
  inert at REV; pinned entries read REV and compare to pinned derivations; the 80/80 fitness was
  measured in a mode that redefines the freeze (C2Vacuity, C2Rescore, `R45-34..R45-39`).
- **Merged sources:** C1Satisfy D-4 · C2Vacuity · C2Rescore · C2Corrections · ConnDefects
  `R45-07/R45-34..R45-39`.
- **Verdict effect:** the *arithmetic* verdict (`entries_evaluated 80`, `mismatches []`, exit 0) is
  confirmed — I reproduced it (§7 R2). The *meaning* is not: "mismatches repaired and scored 80/80"
  should read "80 frozen statements evaluated with 0 mismatches; the three target checks are bound
  to the correction block, not to the statements, so the score does not verify the repairs."

### C-6 (P2, KEEP) — C2's freeze set is narrower than the claim's frozen set

Neither counter freezes `plans/round-44-claims.md`, `corpus/SOURCES.md`, the round-43 port source
`tools/round-43/c1-counter.py`, or the historical receipts the `(e)` entries derive verdicts from;
C2 exits 0 `met_target true` after each is edited (C2Freeze F-1..F-5, ScribeSources D-1/D-2,
`R45-03`). The round is not blind overall (C1 enumerates the claims file), but the C2 score never
speaks to it. **Verdict effect:** none on C2's own score; it is a round-45 freeze-design item.

### C-7 (P2, KEEP) — Record numbers/digests that do not resolve

- **S138 manifest digest is wrong in two committed surfaces:** `4bc53dbb…c1a13` is cited at
  `corpus/lessons/round-44.md:24` and `corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md:12`;
  the actual file is `06a72dd5b660c79adae943917abf40c24ab16554ec6c2f14985958799a78f5fe` at every
  revision. Measured at final HEAD: both cites still wrong (§7 R11). Sources: LessonGate D1, Sources
  defect 2, `R45-17`.
- S138 gate-quote word count and "1 token" listing count are wrong (the v2 BE `__output__` has two
  dirs). D-27 is marked closed on half its exit; D-19's exit fired but is still listed open. Census
  round-start count is 13, not 14. **These are record-hygiene P3 unless the digest is used as
  evidence** — the manifest digest is, so it is P2.
- **Already remediated:** `SCORECARD:3526` C2-census pointer (section removed), QUALITY duplicate
  row 77 (renumbered 86/87), `sources-census-end.txt` (now tracked).

### C-8 (P3, KEEP) — Control-set and scratch-provenance rot

12 of 14 control receipts name `--rev` commits absent from the object DB; every control receipt
names a deleted sandbox; the frozen `pos`/`c3` fixtures cite `/tmp`; C2's 80 entry commands embed a
deleted `/tmp/c2-counter.p_yfx2x5/repo`. M44-2 restated: the 8 paths are **`M`, zero `A`**, and they
are *control inputs* re-captured to match already-recorded receipts. Sources: SentScope F1-F7,
C1Controls D-1..D-4, C1PosArm §8, C1Rescore D5/D6, C2Rescore, `R45-05/06/23`. **Verdict effect:**
none on the two scores; it is the main reason the control evidence cannot be re-derived by a third
party.

---

## 2. Findings that contradict an author verdict

| author verdict | where | contradicted by | net |
|---|---|---|---|
| C1 "honest stop … the score therefore does not satisfy the frozen predicate" (cause = provenance) | `PROVINCE.md:428`, `README.md:104/:224`, entry `:3-9`; earlier `LOG.md:3201` | C-1 (four independent reruns + the counter's own `bindings_false`) | **verdict stands, cause false** |
| "no run can satisfy the whole frozen claim" / "internally unsatisfiable on one field" | lesson as committed at `8bb1090a`, `QUALITY.md` (then-row 77) | C-2 (own `4cc1ac11` receipt; H2; my 3-line restore) | **falsified** — already corrected in LOG/lesson at `923fa870`, **not** in PROVINCE/README/entry |
| "the stop is the only correct reading" | C1 contract item 2; `Simplifier §3.1` | C-2 | **not established**; the stop is *a* policy choice consistent with the amendment clause |
| C2 "three self-assessment mismatches repaired and scored 80/80" | lesson title, LOG, ledger | C-5 | **arithmetic confirmed, meaning overstated** |
| M44-2 "the fix is `frozen-path-preflight.py`, shown able to fail" | lesson `:18`, LOG `:3203` | C-4 (false-green outside the pathspec; false red without it; unwired) | **fix exists, does not cover the class** |
| M44-3 "reverted … counter now lists 8 paths with `SCORECARD.md` absent" presented as the fix working | lesson `:19` | C-3 (restore un-blocks; C1 would still list it) | **the proof is the defect** |

**Nothing in wave 2 overturns the two score values.** `carriers_matched 4` / `met_target false` /
exit 1 at `55bcce69`, and `entries_evaluated 80` / `mismatches []` / exit 0 at `55bcce69`, reproduce
exactly (peers at byte-identical stdout sha256 `eea45d37…` and `dd7c529b…`; my runs agree). The
findings are about **causes, uniqueness, and the weight the scores can carry**, not about arithmetic.

## 3. Peer-level contradictions I had to adjudicate

1. **`R44W2Simplifier.md §3.1` ("R44-C1 — confirmed: … the stop is the only reading") is wrong.**
   It is contradicted by the round's own committed `counter-at-4cc1.json` (exit 0, `met_target true`)
   and by five other seats. Treat Simplifier's C1 verdict as an outlier, not a second opinion.
2. **`C1HonestStop` HS-1 vs `C1Satisfy` H2** is a scope difference, not a conflict (§1 C-2).
3. **`Preflight`/`Record` called the tip lists "byte-identical"**; at `8bb1090a` they were **8 vs 9**
   (C2 adds `SCORECARD.md`) — peers `C1Satisfy` D-3 and `C2Corrections` measured the 9 correctly.
   At `4503fb78` both are 8 again, but only because of C-3's hole.
4. **`Record` §2 says "all numbers reproduce, no discrepancy"** — true for the score numbers; it
   should be read with C-3/C-5/C-7, which it does not cover.

## 4. Merely style / process (DROP — no verdict, no plan change)

Record has two states during the wave (`R45-33`); detached HEAD in the lane worktree (`R45-32`);
QUALITY row wording and the row-77 number (renumbered); M44-1 column swap and artifact-digest
attribution; "measured revision" as a phrase (`D7`); S138 quote word counts; wave-1 attack-share
21.6 % vs the 25 % floor; fleet adjacency registry pin; `/scratch/…`-rooted fixture paths; log/lesson
prose phrasing. These belong in a cleanup commit at most.

## 5. Confirmations the report can rely on (no action)

Independently reproduced by me: C1 exit 1 / 4/4 at `55bcce69` and exit 0 / `met_target true` at
`4cc1ac11`; C2 exit 0 / 80 / `mismatches []` at `55bcce69`; both counters exit 2 at the final tip
with the same 8 `control-fixtures` paths; SOURCES 137 → 139; every commit hash cited in the
round-44 `LOG.md` section (9 distinct tokens) resolves; the preflight's exit codes are 0/1/2 as
documented for the cases it covers.
Peers additionally confirm: oracle re-derivation (12–13 checks per carrier), carrier pins and v1/v2
superblock decode, receipt publication exact and gap-free, evidence ids recompute, `file(1)`/`cmp -l`
hazards real but unreachable from any scored binding, C2's base census red with exactly the three
target ids.

---

## 6. What would change the round report (the decision layer)

1. **Fix the three remaining C1 cause surfaces** (`PROVINCE.md:428`, `README.md:104/:224`, entry
   `:3-9`) — they are not frozen and are the surfaces a reader hits first. (C-1, C-2)
2. **Say "unrealized by this round's receipts", never "unsatisfiable"**, and name `4cc1ac11` as the
   met precursor next to `55bcce69`. (C-2)
3. **Drop the "SCORECARD absent at the final tip proves M44-3 fixed" inference** and record that
   C2's bound-edit arm un-blocks on restore; C1 does not. (C-3)
4. **Downgrade the M44-2 fix to "detector, not gate"**, and carry the pathspec-set + dirty-tree +
   endpoint-independent-walk requirements into round 45. (C-4)
5. **Qualify the C2 headline** as arithmetic-confirmed / repair-unverified. (C-5)

---

## 7. Receipts (this seat; every command run from the seat's own clone)

Scratch root `/fast/scratch/hyaku/kaidoku-r44/R44W2Distill/`, deleted after the receipts were
captured. `pkg65` = `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`.

| # | command (abridged) | exit | observed |
|---|---|---|---|
| R1 | `c1-counter.py --rev 4cc1ac11 --freeze c48f8a4b` | **0** | `carriers_matched 4`, `met_target true`, `bindings_false []`, `frozen_path_changed []`, counter sha256 `9f2cc140…ffea993`; stdout sha256 `8742a90d9b879fbf91f77c5862273be7…`, wall 6.90 s |
| R2 | `c2-counter.py --rev 55bcce69 --freeze c48f8a4b` | **0** | `entries_evaluated 80`, `mismatches []`, `met_target true`, rubric sha256 `e8cc0ded…` = at freeze; stdout `dd7c529bb6340c364854093937bce3d9…`, wall 5.03 s |
| R3 | clone at `55bcce69`, restore only `4cc1ac11:PROVINCE.md` (3 lines), commit `e7e7a61c`, run C1 | **0** | `met_target true`, `bindings_false []` — the red is produced by the doc withdrawal alone; stdout `440f6c7a29e627c41fdb9d8e718119c4…` |
| R4 | clone at `55bcce69`, append one line to `corpus/evidence/round-44/oracle/manifest.json`, commit `126fd5cd`; preflight `--pathspec tools/round-44` | **0 / 2** | preflight `verdict clean`; **C1 counter exit 2** `frozen_path_changed ['corpus/evidence/round-44/oracle/manifest.json']` |
| R5 | clone: unauthorized append to `SCORECARD.md` → `0eaa4c75` (C2 **2**, `SCORECARD.md`, `bound_edit_violation`); restore to the bound blob → `043a83ba` (C2) | **2 / 0** | at restore: `frozen_path_changed []`, 80/80, **`met_target true`**, note `bound_edit_applied`; stdout `a642ac897a822f3f75c60c3c…`, wall 8.08 s |
| R6 | same shape on `tools/round-42/prior-pins.json` (a `FROZEN_PATHS` entry), C1 at violation and after restore | **2 / 2** | path **still listed** after restore — C1 implements "restore does not un-block", C2 does not |
| R7 | `c1-counter.py` / `c2-counter.py` at `8bb1090a`, `923fa870`, `4503fb78` | **2 / 2** | `8bb1090a`: C1 8 paths, C2 **9** (`+SCORECARD.md`); `923fa870` and `4503fb78`: both 8, `SCORECARD.md` absent |
| R8 | preflight, cases: pathspec @`c86ea508` / @`55bcce69` / no pathspec @`c86ea508` / no pathspec @`55bcce69` / @HEAD / `rev=freeze` / freeze-after-rev / unknown rev | **1 / 0 / 1 / 1 / 1 / 0 / 2 / 2** | touched 8/8 · 0/0 · 542/0 · 110/0 · 8/8 · 0/0 · – · – |
| R9 | rubric B2 audit: for each of 80 entries, `asserted in line_at_base` and `sha256(line) == line_sha256` | n/a | **71/80 fail the substring rule**; sha256 matches on all sampled lines |
| R10 | clone at `55bcce69`, delete 2 `corpus/knowledge/*.md`, commit `dc7f4fd6`, run C2 | **1** | `mismatches ['C2-h2-readme-knowledge-entries-resolve']` only — `C2-a1` stays green while its subject moves 138 → 136 |
| R11 | `sha256sum corpus/evidence/round-44/oracle/manifest.json`; grep `4bc53dbb` in lesson+entry | 0 | actual `06a72dd5…8f5fe`; wrong digest still cited in both files at `4503fb78` |

**Artifacts.** `.ufo/waves/round-44/w2/artifacts/R44W2Distill/` holds the ten small counter
receipts plus `receipts-summary.json` (per-run verdict fields, byte count and full-file sha256 for
every run, including the three ~750 KB C2 score files I did not mirror — regenerate those with the
`c2-counter.py` command in R2). Total 96 KB.

## 8. Limits

- I did not re-run REA for R3: the counter's `projection_ok` is evaluated against the committed
  receipts, and the counter-time rerun executes as part of the same run (7–8 s wall each), so R3's
  green is a full scored run, not a projection stub.
- R5/R6 fixtures are my own clones; the lane was never written to.
- The `touched`-vector mechanism in C-3 is read from `tools/round-44/c2-counter.py:616-661` and
  demonstrated end-to-end in R5; I did not attempt to exhaust other `expected_edit` paths, but
  `SCORECARD.md` is the only rubric entry carrying one.
