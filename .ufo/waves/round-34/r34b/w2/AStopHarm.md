# AStopHarm — harm audit of the R34-C2 stop, and attack on its evidence

Seat: `L1Kaidoku34-2.AStopHarm` (reviewer, wave 2). Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Scope: the stop at `.ufo/waves/round-34/r34b/claim-stop.json` (landed `cd75b92e`), the range
`ec3125ad..cd75b92e`, the five disclosed record defects and the repair routes. **No claim reopened,
no instrument repaired, no score awarded.**
Lane VCS: read-only (`git diff`/`log`/`show`/`cat-file`/`rev-parse`/`ls-tree`/`status` only — no add,
commit, stash, checkout, reset, pull, push, no jj). All configs, gates and receipts I produced live in
`/fast/scratch/hyaku/kaidoku-r34b/w2/AStopHarm/`; my only lane write is this file.
No R34-C1 production reader and none of its twelve carriers were executed, read as programs or scored.
Readers were executed only as `python3` children of the pinned counters. Canonical runtime:
`/usr/bin/python3` = **Python 3.14.8** (same interpreter the counters spawn through `sys.executable`;
the gate pins `PATH=/usr/bin:/bin`). No tool was installed, upgraded or restarted; pacman untouched.
**UTC window of this audit: 2026-10-25T07:28Z – 07:35Z.** HEAD moved from `cd75b92e` to `66b84027`
during the audit (see §8); every doc-state claim below carries its own timestamp.

## 0. Axes named (Godspeed)

| axis | proxy | direction |
|---|---|---|
| A1 pre-existing content | paths deleted / lines deleted outside superset edits | zero is the only acceptable value |
| A2 score and doc mutation | SCORECARD/LOG/SKILL/QUALITY/SOURCES/README hunk shape; owned-axis cells | append-only, no cell moved |
| A3 frozen-byte identity | 26 pins, tree blobs, claims blob across revisions, C1's 21 pins | all identical |
| A4 stop-evidence truth | re-run the decisive counterexample and the frozen counter at tip | exit 0, 8/8, `clauses_failed=-` |
| A5 record attribution | does each stop-record field name the rule/file/target it actually used | exact |

A1/A2/A3 are the harm question; A4/A5 are the stop question.

## 1. Range and census (exact commands)

```
$ git -C <LANE> diff --numstat ec3125ad cd75b92e        # exit 0, 2026-10-25T07:28:01Z / re-run 07:34:28Z
897 rows;  insertions = 210201,  deletions = 2      (54 rows are binary: `-  -`, not deletions)
$ git -C <LANE> diff --name-status ec3125ad cd75b92e   # exit 0, same stamps
897 rows;  888 A,  9 M,  0 D,  0 R,  0 C
$ git -C <LANE> diff --shortstat ec3125ad cd75b92e    # exit 0
897 files changed, 210201 insertions(+), 2 deletions(-)
```

Round base `ec3125ad3d130d92f888a4128dfaa2982f36fff7` is the last round-33 commit
(`ec3125ad round-33 verifier spot-check`); tip `cd75b92e583735729546b0ea3b250f2df6d0652a` is the stop.
Eight round-34 commits: `8897a67f`, `54a87a51`, `d52e2404`, `abbd7604`, `f432c8e3`, `c79bbe7b`
(freeze), `b917ea64` (receipts + pin container), `cd75b92e` (stop).

**Deleted paths: none.** `0 D` over the whole range. The two deleted *lines* are both superset
replacements (§3).

### Modified files (9)

`.ufo/waves/round-33/prep/R33ChpeParser-independent.json`, `LOG.md`, `SCORECARD.md`, `SKILL.md`,
`corpus/QUALITY.md`, `corpus/README.md`, `corpus/SOURCES.md`, `corpus/claim-freezes.tsv`,
`corpus/claim-freezes-v2.tsv`.

### Added paths (888)

| group | count | notes |
|---|---|---|
| `.ufo/waves/round-34/w1/**` | 476 | attempt-1 seat artifacts of the C1 wave |
| `.ufo/waves/round-34/prep/**` | 259 | source captures, expected-record authors, decision table |
| `.ufo/waves/round-34/r34b/**` | 82 | C2 freeze, receipts, controls, w1 seats, prompts, pin container |
| `.ufo/waves/round-34/*` (root) | ~26 | claims, claim-stop (C1), dispatch/settle/spawn/spec/census records |
| `tools/round-34/**` | 37 | `replay-gate.py`, `c2-shortcut-gate-counter.py`, `elf-version-needs.py`, `version-needs-counter.py`, `freeze-integrity.py`, two gate configs, `mini-fix/{build,spec,expected}`, 8 `.mrec` fixtures, 9 readers |
| `corpus/**` | 14 | 12 carrier copies `corpus/evidence/round-34/elf/e01..e12.bin`, `corpus/knowledge/2026-10-23-r34-elf-version-needs.md`, `corpus/lessons/round-34.md` |
| `glibc-tag-object.json` (lane root) | 1 | the misrooted tag object, M34-5 |

Counts are from `git diff --name-status` grouped by directory prefix; 845 changes under `.ufo/`,
52 outside it (44 additions + 8 modifications).

## 2. Probes actually run (argv, exit, UTC)

| # | argv (cwd = lane unless stated) | UTC | exit | observed |
|---|---|---|---|---|
| P1 | `/usr/bin/python3 -I -B tools/round-34/c2-shortcut-gate-counter.py --root . --rev c79bbe7b0959132b9873ff3431cf5eb313b58b33 --json-out /fast/scratch/…/c2-at-tip.json` | 07:29:32–34Z | **0** | `GATE_COUNTER_OK finding=shortcut_gate_discriminates selftest_failures=0 mutants_killed=3 red=REPLAY_GATE_REFUSED green=REPLAY_GATE_CLEAN green_positive_matched=8 clauses_failed=-` — byte-identical to `r34b/after/c2-at-instruments.txt` |
| P2 | `/usr/bin/python3 -I -B tools/round-34/mini-fix/mini-counter.py --root . --control-reader .ufo/waves/round-34/r34b/w1/CtlMultiset-files/nameset.py --seed {kaidoku-r34-mini-v1 \| alt-1 \| alt-2}` | 07:29:32Z | **0 / 0 / 0** | `matched 8`, `target 8`, `met_target true`, `finding records_match` on all three seeds |
| P3 | `/usr/bin/python3 -I -B tools/round-34/replay-gate.py --root . --config <scratch: gate-config-mini + 8th class nameset-replay>` | 07:31:47Z | **2** | `REPLAY_GATE_REFUSED finding=shortcut_meets_target shortcuts_below_target=7 shortcuts_over_target=nameset-replay` |
| P4 | `/usr/bin/python3 -I -B tools/round-34/freeze-integrity.py --root . --round 34 --claims .ufo/waves/round-34/r34b/claims.json --rev c79bbe7b…` | 07:30:15Z | **3** | `ERROR schema code=instruments_missing claims=…/r34b/claims.json where=instruments` |
| P5 | same with `--claims .ufo/waves/round-34/r34b/instruments.json --rev c79bbe7b…` | 07:31:47Z | **2** | `ERROR no commit adds .ufo/waves/round-34/r34b/instruments.json at c79bbe7b…` |
| P6 | same with `--claims …/instruments.json --rev HEAD` | 07:32:10Z | **0** | `freeze-integrity: CLEAN pins=26 freeze=b917ea64ebbe rev=HEAD` |
| P7 | `/usr/bin/python3 -I -B tools/round-34/freeze-integrity.py --root . --round 34` (C1 map, default) | 07:30:15Z | **0** | `CLEAN pins=21 freeze=54a87a51a865 rev=HEAD`, every row `commits_after_freeze=0` |
| P8 | `replay-gate.py --root . --config <scratch: mini, 3 weak classes>` | 07:30:15Z | **0** | `REPLAY_GATE_CLEAN … shortcuts_below_target=3` |
| P9 | `replay-gate.py --root . --config <scratch: naive, 3 weak classes, label-memorization dropped>` | 07:30:16Z | **0** | `REPLAY_GATE_CLEAN … shortcuts_below_target=3` (red case satisfied by a thin class set) |
| P10 | `python3 -I -B /fast/scratch/…/gate-m3.py --selftest` (frozen gate copied to scratch, `for item in config["shortcuts"]:` → `[:-1]`) | 07:30:02Z | **0** | `{"cases": 12, "failed": [], "failures": 0, "mutants": 3, "mutants_killed": 3}`; mutant sha `9ffbb7e9df0fa6a02da98cb4b6dacef79eeecb099002b8a94805b3d738b78844` |
| P11 | `gate-m3.py --root . --config tools/round-34/gate-config-naive.json` | 07:30:04Z | **0** | `REPLAY_GATE_CLEAN … shortcuts_below_target=6` — **red inverted to CLEAN** |
| P12 | `replay-gate.py --root . --config <scratch: naive with `label-memorization` relabelled `structural`>` | 07:34:05Z | **0** | `REPLAY_GATE_CLEAN … shortcuts_below_target=6`; rows contain **two** `class=structural`, both `matched 8`, `met_target true` |
| P13 | pin recompute over all 26 `instruments.json` pins + claims/nameset digests (read-only python) | 07:34:28Z | **0** | `pins=26 mismatches=0`; `claims.json` sha256 `de3afbfb…` **=** `frozen_claims_sha256`; `nameset.py` sha256 `2e8feaea…` **=** `decisive_counterexample.source_sha256` |
| P14 | per-blob identity of the whole frozen tree: `git rev-parse c79bbe7b:<f>` vs `cd75b92e:<f>` for every `tools/round-34` path; plus `git diff --stat c79bbe7b cd75b92e -- tools/round-34` | 07:34:28Z | **0** | diff empty; `blob_mismatches=0` |
| P15 | `git rev-parse {c79bbe7b,b917ea64,cd75b92e,HEAD}:.ufo/waves/round-34/r34b/claims.json` | 07:34:28Z | **0** | all four = `98596f137e6cc174d8e70f27fbbea886975e705c` |
| P16 | `git diff --stat abbd7604 cd75b92e -- .ufo/waves/round-34/claim-stop.json`; `git log -1 -- <that path>` | 07:31:47Z | **0** | empty; only `abbd7604` — the C1 stop record was **not** overwritten by the C2 stop |
| P17 | doc hunk shape: `git diff -U0 ec3125ad cd75b92e -- {SCORECARD,LOG,SKILL,corpus/QUALITY,corpus/SOURCES,corpus/README,corpus/claim-freezes*.tsv}` | 07:28Z | **0** | every hunk is `@@ -N,0 +M,K @@` (pure insertion) except `corpus/README.md` (one line extended, §3) |

## 3. Deletions — the two lines, verbatim

Both deleted lines are replaced by supersets; **no pre-existing value is lost** (checked by reading the
`-`/`+` pair of each hunk, `git diff -U3 ec3125ad cd75b92e -- <path>`, exit 0, 07:28Z):

1. `corpus/README.md` (`2 +, 1 -`): the `| Native ELF |` row keeps all four prior knowledge-entry names
   verbatim and appends `2026-10-23-r34-elf-version-needs` plus one clause. Old text is a strict prefix
   of the new text.
2. `.ufo/waves/round-33/prep/R33ChpeParser-independent.json` (`8 +, 1 -`): the deleted line is
   `"claim_status": "Stopped, not evaluated"` **with no trailing comma**; the new line is the same
   string with a comma plus an appended `round_34_appended_pin_correction` block that embeds
   `"old_sha256_preserved_above": "af5d86f15c22f9d1fc148d2a6b81004eb76967d50c314c9078633bc6ccee32ac"`.
   This is an append-only correction of a round-33 pin, not a rewrite (matches lesson M34-3).

## 4. Score and document mutation (A2)

- `SCORECARD.md`: one insertion hunk at EOF `@@ -3321,0 +3322,24 @@`, **0 deletions**. The round-34
  block states `Existing scores stay 10→10`; the C1 row states `owned scores 10→10, delta 0`.
  **No R34-C2 capability row exists in `SCORECARD.md` at `cd75b92e`, and none exists at `HEAD`
  either** — at `HEAD` the new block's table is verdict-only and the owned-axis table is
  `coverage 10 → 10`, `depth 10 → 10 (no numeric proxy moved; the capability was denied)`,
  `calibration 10 → 10`, each `unchanged`.
- `LOG.md` `@@ -3079,0 +3080,13 @@`, `SKILL.md` `@@ -1156,0 +1157,51 @@`, `corpus/QUALITY.md`
  `@@ -74,0 +75,3 @@`, `corpus/SOURCES.md` three pure insertions, `corpus/claim-freezes.tsv`
  `@@ -20,0 +21,1 @@`, `corpus/claim-freezes-v2.tsv` `@@ -25,0 +26,1 @@` — **all insertions, zero
  deletions**. Every hunk sits at the file tail or inside the append-only registries, so no existing
  paragraph, row or score cell was reformatted.
- Net: the stop moved no score and rewrote no document. **The stop's own claim "no capability row enters
  SCORECARD; owned scores stay 10→10" is true at `cd75b92e` and still true at `66b84027`.**

## 5. Frozen bytes (A3)

- `tools/round-34` is **byte-identical** from the freeze to the stop: `git diff --stat c79bbe7b
  cd75b92e -- tools/round-34` is empty and a per-file blob comparison over the whole frozen tree
  reports `blob_mismatches=0` (P14).
- **26/26 pins** in `r34b/instruments.json` match the worktree bytes (P13); the same map's
  `frozen_claims_sha256` equals the actual `claims.json` digest, and the pinned counterexample source
  digest equals `nameset.py` (P13).
- `.ufo/waves/round-34/r34b/claims.json` has the **same blob id at `c79bbe7b`, `b917ea64`, `cd75b92e`
  and `HEAD`** (P15) — the freeze was never edited, including by the receipts commit.
- The C1 stop record `.ufo/waves/round-34/claim-stop.json` is untouched since `abbd7604` (P16), and
  C1's frozen map still verifies at `HEAD`: `freeze-integrity --round 34` → `CLEAN pins=21
  freeze=54a87a51a865`, all rows `commits_after_freeze=0` (P7). **Stopping C2 did not disturb C1.**
- The receipts commit `b917ea64` and the record commit `66b84027` touched no instrument, no
  `claims.json`, no `claim-stop.json`, no `instruments.json` (P14, P15, P16 and the
  `cd75b92e..HEAD` stat over those four paths is empty, exit 0, 07:33Z).

## 6. The stop's evidence, re-derived

**The decisive counterexample is real and reproduces exactly as recorded.** `nameset.py` scans the
input for SONAME-shaped tokens (`TOKEN = [A-Za-z0-9_.+-]+\.so(\.[0-9]+)+`), sorts the *set*, joins it
into a key and replays a hard-coded 8-entry `name → (flags,value)` table. It reads no header, no
record entry and no `name_off`; the association comes from the table. `mini-counter.py`'s only
transformation is `permute()`, which reorders the name pool and rewrites each record's `name_off`
while preserving size, record order and every `flags`/`value` byte — so the name multiset, and
therefore the key, is invariant. Result: **8/8 at three seeds, exit 0** (P2), on the frozen bytes
(P13, P14). The claim-stop's `observed` block is therefore accurate, including its seed map.

**The "unregistered" clause is also accurate, in both directions.** The pinned green config registers
seven shortcut classes (none is a content-multiset class); adding `nameset-replay` to a copy of that
config and running the frozen gate flips the same gate to `REPLAY_GATE_REFUSED
… shortcuts_over_target=nameset-replay`, exit 2 (P3). So "the green clause is satisfied only because
this class is unregistered" is literally true: the refusal branch bites, the registry is what was
thin. This is the strongest form the stop's finding could take, and it survives re-derivation.

**The frozen six clauses are all true** on the frozen bytes at the tip: P1 reproduces the committed
receipt line character-for-character. The stop says this too
(`frozen_counter_verdict.note`: "the six frozen clauses hold on the frozen bytes; that is not the
whole test"). **No clause failed.**

**The wave-1 defect claims I re-derived:**
- *F1 (pins declarative / wrong container):* P4 → exit 3 `instruments_missing`. True.
- *F3 (class drop invisible):* P8 and P9 → both CLEAN at the three-class floor, including the red
  counter with the only over-target class removed. True.
- *F4 (gate mutant M3 survives its selftest and inverts the red case):* P10 → selftest exit 0,
  12/12, 3/3; P11 → red case CLEAN. The mutant I built independently hashes to the same digest the
  seat reported (`9ffbb7e9…b78844`). True.
- Not re-run by me (cited only): CritCounterLimits probe E (a 1,979-byte gate that runs no reader
  satisfies all six clauses) and probe C (an 8/8 reader relabelled `structural`); MutShortcutClasses'
  payload/value/record-signature classes; the four `+1 -1`-style controls under `r34b/controls/`.
  **An unrun check has not passed** — I make no claim about those beyond "the seat's receipt exists
  and its defect is consistent with the source I read".

## 7. Findings, by severity

### R1 — MEDIUM — `kill_rule_applied` names a rule that did not fire

`claim-stop.json.kill_rule_applied` reads *"Frozen before data: a target met by a control that skips
the claimed work is not an improvement."* That is **not** the frozen kill rule. The frozen kill rule
is `claims[0].kill_rule` (`r34b/claims.json:22`): *"if any of the six clauses … is false at the
measured revision, the claim is a miss and stops honestly; no target, counter, predicate or label may
be changed afterwards, and no shortcut class may be dropped to reach CLEAN."* Its trigger is a false
clause; **all six clauses are true** (P1), so the frozen kill rule did not fire. What fired is the
standing supra-rule ("a target reached by a control that skips the work is not an improvement"), which
the round's own durable text cites as §9 / r29-C1 precedent. The stop is defensible on that rule — and
is the conservative disposition, since it credits nothing — but the field that names the rule should
name the right one. Mitigation already in the record: `frozen_counter_verdict.note` says the six
clauses hold. A reader who reads only `kill_rule_applied` would believe a frozen clause failed, i.e.
would believe the claim's own kill rule fired when it did not.

### R2 — MEDIUM — the F1 repair cannot be verified at the freeze revision

`record_defects_disclosed[F1].repair_landed` says `r34b/instruments.json` plus "freeze-integrity
receipt over it". Reproduced outcomes:

- over the frozen claims file: **exit 3 `instruments_missing`** (P4);
- over the new container **at the freeze revision**: **exit 2**,
  `ERROR no commit adds .ufo/waves/round-34/r34b/instruments.json at c79bbe7b…` (P5) — the container
  did not exist at the freeze, so the instrument cannot anchor to it;
- over the container **at `HEAD`**: exit 0, `CLEAN pins=26 freeze=b917ea64ebbe` (P6) — the receipt's
  own freeze anchor is `b917ea64`, i.e. **a commit made after the freeze and after three wave-1
  audits**.

No committed receipt of any such run exists under `r34b/` (`grep -rn
"claims=.ufo/waves/round-34/r34b/instruments.json"` → only the prose citation in `claim-stop.json`;
`ScribeSkillRegistry.md:112` records the exit-2 outcome). The repair is therefore a **container plus a
passing run whose freeze label is post-freeze**; the pre-freeze pin identity rests on (a) the manual
26/26 audits and (b) VCS blob identity, which I verified independently (P13, P14, P15). The claim is
true; the repair as described is not.

### R3 — MEDIUM — the decisive counterexample has no receipt

`claim-stop.json.decisive_counterexample` carries argv, class, observation and the reader's sha256, but
**no receipt path** — unlike the C1 stop, which binds `size-pristine.receipt.json`. Nothing under
`r34b/` records the nameset run in machine form: `grep -rl nameset .ufo/waves/round-34/r34b
--include='*.json' --include='*.txt'` returns only `claim-stop.json` and `w2-spec.json`. The F5 repair
landed the *other* receipts; this one was never created. The evidence is reproducible (P2) and I
reproduced it, so the finding stands on bytes; but the record itself cannot show the run to a
checker that does not re-execute it.

### R4 — MEDIUM — at the stop tip, two of the five defect citations are untracked files

`git cat-file -e cd75b92e:<path>` over every `.ufo/…` path the stop record cites:
`MutGateBranches.md` (evidence for F4) and `RevFreezeOrder.md` (evidence for F5) → **absent** at the
stop tip. A clean checkout at `cd75b92e` therefore cannot read the evidence for two of the five
disclosed defects; F1/F2/F3 citations are tracked. Both files were committed later at `66b84027`
(§8). The stop's own F5 ("receipts were untracked at first audit time") scopes untrackedness to
*receipts*; the seat reports the stop leans on were untracked at the stop commit itself.

### R5 — MEDIUM — the canonical stop record's defect list is narrower than the record it lands, and omits the only live false-pass defect

`claim-stop.json` discloses **five** defects: (F1) declarative pins/wrong container, (F2) predicate
identity false, (F3) class drop invisible, (F4) gate mutant M3 survives its selftest, (F5) receipts
untracked. The record actually landed for the same stop (`SCORECARD.md` round-34 run-6 block, `LOG.md`
2026-10-25 entry, lesson `M34-5..M34-12`, `QUALITY 68-73`) lists **six**: pins container; predicate
identity; class drop; **a shortcut relabelled `structural` prints CLEAN even on the red config**; **a
gate that runs no reader satisfies all six clauses, and `met_target` is never cross-checked with
`matched`**; `--rev` is an echo and receipts carried no argv. Three items in each list are absent from
the other.

That is not a bookkeeping difference: the omitted *relabel* defect is a **live false pass on the
production-class red branch**, and I reproduced it — relabelling the single over-target
`label-memorization` row to `structural` makes the frozen gate print `REPLAY_GATE_CLEAN`, exit 0,
with two rows of `class=structural` both at `matched 8` (P12). The exemption is name-based
(`row["class"] != positive_spec["class"]`) and the duplicate-class guard checks only the shortcut list,
not the positive control's class. The defect the stop records (F4) is the weaker, mutant-only cousin of
this one. Also omitted from the stop record although reported in tracked wave-1 reports:
`RevClaimsVsInstruments.md` F4 (claim `target` field not bound to the clause — `green_positive_matched`
is a literal `8`) and F5 (pinned reader `label_keyed.py` registered nowhere — a dead pin), and
F6/`ExecRecountC2` F2 (`--rev` echoed, never checked). `record_defects_disclosed` reads as an
exhaustive list; it is not.

### R6 — LOW — stop-time evidence content is not VCS-verifiable

The seat reports that *are* the stop's evidence were untracked at `cd75b92e`, so their content at stop
time has no baseline. Their later commit (`66b84027`) reflowed 3 lines of `ExecAntiVacuityProbe.md` and
replaced a heading (`## 7. Tooling record`) in `RevScopeNoHarm.md`. I cannot distinguish those edits
from edits made before the stop. This is the same class of gap as F5, one layer up.

### R7 — LOW (post-stop, in the record landing) — the S105 source row was overwritten, and at HEAD it is still missing

Commit `66b84027` adds `S106` **on top of** the `S105` row in `corpus/SOURCES.md`:
`git diff cd75b92e HEAD -- corpus/SOURCES.md` shows `-| S105 …` / `+| S106 …`. At `HEAD` the table has
`S103, S104, S106` — the pre-existing rejected row `S105` (System V gABI draft, `REJECTED`) is gone,
while the row count (105) and the census exit code (0) stay unchanged. This is disclosed and routed as
lesson **M34-12** ("a registry append replaced the previous row … `rejected` fell 4→3"), and the row is
**restored in the uncommitted worktree** at my snapshot (`grep -n '^| S10[3-6]' corpus/SOURCES.md` →
`S103, S104, S105, S106`; `git status --porcelain` → ` M corpus/SOURCES.md`). At `HEAD`, however, it is
still absent. This is the round's only deletion of pre-existing *content* (beyond the two superset
lines of §3), and it happened while landing the stop's record, not while stopping.

### R8 — INFO — the durable stop record landed after the stop, and the SCORECARD row rests partly on seats I did not re-run

At `cd75b92e` (and until `66b84027`, ~07:33Z) no `LOG.md`/`SCORECARD.md` entry recorded the C2 stop;
VCS-durable record of it was `claim-stop.json` alone. That is now fixed. The new SCORECARD row states
"five unregistered structure-blind classes reach the green 8/8"; I re-derived one of them (the
decisive one) and left the other four as cited-not-run.

### R9 — INFO — the strongest supporting argument is not cited in the stop's rationale

`RevPredicateIdentity.md` LOW-1 observes that sentence A names a "finite structural-decoding counter"
while the measured object is the synthetic mini counter, which the claim's own
`instrument_notes.no_production_reader_run` excludes from domain evidence. That is a cleaner
statement of why a registry-relative CLEAN cannot be credited than the stop's own
`why_this_falsifies_the_surface`. It belongs in the stop's rationale; its absence does not weaken the
stop, since the counterexample argument is stronger.

## 8. HEAD moved during the audit — the record commit, checked

At 07:33:05Z `git rev-parse HEAD` returned `66b840274390d0868c913a544947f9eb40a4ffe6` (L1 landing the
stopped claim's record). Thus **two tips** are audited:

| range | files | insertions | deletions |
|---|---|---|---|
| `ec3125ad..cd75b92e` (the stop) | 897 (888 A / 9 M / **0 D**) | 210,201 | 2 (both supersets, §3) |
| `cd75b92e..66b84027` (the record landing) | 69 | 6,675 | 7 |

The 7 deletions: `SCORECARD.md` 1 (the round-34 paragraph "Main approved the stop…" replaced by the
same paragraph with "next counter freeze" wording plus the new run-6 section — no score cell touched);
`corpus/SOURCES.md` 2 (**R7**, plus one `jj …` caution line extended, not removed);
`ExecAntiVacuityProbe.md` 3 and `RevScopeNoHarm.md` 1 (reflow inside the seats' own reports, **R6**).
Frozen identity at the new HEAD is unchanged: `git diff cd75b92e HEAD -- tools/round-34
.ufo/waves/round-34/r34b/{claims,claim-stop,instruments}.json` → empty, exit 0. Worktree at the end of
my audit was still dirty on `corpus/SOURCES.md` and `corpus/lessons/round-34.md` (the S105 restore and
late lesson text), so doc content at `HEAD` and in the worktree differ.

## 9. Did stopping harm any axis? — verdict

**NO. The R34-C2 stop harmed no axis, and no pre-existing content was deleted by it.** Concretely, with
evidence:

1. **No pre-existing path deleted** in `ec3125ad..cd75b92e`: `0 D` of 897 name-status rows; the only
   two deleted lines are supersets that retain their old text verbatim (§3).
2. **No score moved**: `SCORECARD.md` is a single 24-line insertion at EOF in the stop range with no
   capability row for R34-C2; owned axes read `coverage 10→10`, `depth 10→10`, `calibration 10→10`
   (§4). The stop record's own `scores_unchanged` matches the file.
3. **No document rewritten**: every `LOG/SKILL/QUALITY/SOURCES/claim-freezes` hunk is a pure insertion
   (`@@ -N,0 +M,K @@`); `corpus/README.md`'s single edit is a strict superset of the replaced line (§4).
4. **Frozen bytes unchanged**: `tools/round-34` blob-identical `c79bbe7b→cd75b92e`; 26/26 pins;
   `r34b/claims.json` one blob id at four revisions; C1's stop record untouched since `abbd7604`; C1's
   21-pin freeze still CLEAN with `commits_after_freeze=0` at HEAD (§5).
5. **The stop's evidence is true**, not merely plausible: the counterexample reproduces at three seeds
   (8/8, exit 0) and the gate refuses the class once registered; the frozen six clauses are all true
   (§6). A stop that credits nothing, on evidence that survives independent re-derivation, costs the
   lane nothing it was entitled to.
6. **The one real content loss of the round is post-stop and already disclosed**: the `S105` row
   overwrite in the record-landing commit, recorded as M34-12 and restored in the worktree, still
   absent at `HEAD` (**R7**). It is a landing-commit defect, not a stop defect, and it is not yet
   durable — it should be committed.

## 10. Residual risk and verification gaps (stated, not papered over)

- **Unrun:** CritCounterLimits probes C and E, MutCounterClauses F4, the four committed control gates,
  and the three non-decisive shortcut classes. Their defects are reported by seats with receipts; I
  cite them and do not certify them.
- **Forbidden and unnecessary, therefore not done:** any execution of the R34-C1 production reader or
  its twelve carriers; any execution of `.mrec` fixtures, `.bin` carriers or ELF files as programs.
- **No baseline for stop-time seat-report content** (untracked at `cd75b92e`) — R6.
- **Moving target:** HEAD advanced mid-audit and two docs are dirty in the worktree; all doc claims
  above carry timestamps, and the `66b84027` state is reported separately from the stop tip.
- **Scope:** I read instruments, configs, receipts and seat reports; I did not re-author, re-freeze or
  repair anything, and I award no score.

**VERDICT: STOP_HARM_CLEAN — the R34-C2 stop deleted no pre-existing path or content (0 D of 897;
2 deleted lines, both supersets), moved no score (owned axes 10→10, no capability row), rewrote no
document (pure insertions at EOF), left every frozen byte identical (26/26 pins, `tools/round-34`
blob-identical, `claims.json` one blob at four revisions, C1's stop record and 21-pin freeze intact
and CLEAN at HEAD), and its decisive counterexample reproduces exactly (8/8, three seeds, exit 0) with
the gate refusing the class once registered; the stop is sound, but its record carries five
attribution defects to route — R1 the `kill_rule_applied` misnaming (the frozen kill rule did not
fire; all six clauses are true), R2 the F1 container unverifiable at the freeze revision (exit 2 at
`c79bbe7b`, passing only with `freeze=b917ea64`), R3 no receipt for the decisive counterexample, R4
two of five defect citations untracked at the stop tip, R5 a defect list that omits the live
red-branch false pass (relabelled `structural` → CLEAN) and three tracked wave-1 defects — plus R7,
the post-stop `S105` row overwrite, disclosed as M34-12 and still uncommitted at audit end.**
