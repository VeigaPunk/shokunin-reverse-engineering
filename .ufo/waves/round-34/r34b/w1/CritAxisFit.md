# CritAxisFit — R34-C2: is the moved surface really `depth`?

Seat: `L1Kaidoku34-2.CritAxisFit` (critic, read-only). Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Frozen claim: R34-C2, `axis: depth`, `type: capability acquisition`, frozen at `c79bbe7b0959132b9873ff3431cf5eb313b58b33`
(`.ufo/waves/round-34/r34b/claims.json:7,8,69`). Inherited R34-C1 untouched: no production reader, no carrier and no
C1 fixture was executed or scored by this seat.

All times UTC, 2026-10-25. Working copy for execution:
`/fast/scratch/hyaku/kaidoku-r34b/w1/CritAxisFit/` (pin-verified copy of `tools/round-34`, see §5). The lane worktree was
read only, never mutated.

---

## 1. The axes, named

| Axis (fleet `AXES.md`) | Definition that bites here | Signal |
|---|---|---|
| `depth` (`AXES.md:11`) | "Verifiable technical detail — decision tables with real thresholds, named error signatures, **cited sources**" | "A reader can act on **SKILL.md alone**" |
| `operability` (`AXES.md:13`) | "Runnable artifacts: checklists that are executable, commands that exist, scripts that run" | "A checklist item can be run and produces the stated outcome" |
| `calibration` (`AXES.md:15`) | "Self-assessment quality: gaps named honestly … overreach caught" | "SHONEN/SCORECARD entries match observed repo state" |

Lane-owned axes (SCORECARD `## Owned axes`): coverage, depth, calibration — all three finite proxies tied at 10.0
(`SCORECARD.md:634`, saturation line 10.0). So `depth` is a tied-lowest owned axis; that part of `axis_basis`
(`claims.json:8`) is accurate. The contested half is the next clause of the same sentence: *"the surface this round
moves is the lane's structural-counter **admission instrument**, not a numeric proxy score."*

## 2. The claim's own wording, quoted

- `claims.json:8` (axis_basis): "… the surface this round moves is **the lane's structural-counter admission
  instrument**, not a numeric proxy score."
- `claims.json:52` (predicate_identity): "**The same sentence** is the gate config's `predicate` field, the C2
  counter's PREDICATE constant and the receipt label …"
- `claims.json:53-57`: declared scores `depth 10 -> 10`, `coverage 10 -> 10`, `calibration 10 -> 10`.

## 3. Strongest counter-reading

**The moved surface is instrument operability (and, secondarily, calibration), not depth.** AXES.md admits capability
acquisitions as claims but does not exempt them from axis fit: "it still lands a per-axis verdict" (`AXES.md:40-41`),
and a claim is "one axis-move: pick the axis, land one verifiable improvement" (`AXES.md:27-30`). The artifact that
landed is a generic subprocess harness. Its content is: load a JSON config, run a counter argv, read the counter's own
receipt fields, sort classes over/under target, print one of three verdicts. That is the operability signal verbatim —
commands that exist, scripts that run, a checklist item that can be run and produces the stated outcome — and its
purpose (refuse a freeze when a memorizing reader meets the target) is the calibration signal, "overreach caught".

### 3.1 Strongest defence, and why it fails

*Defence:* depth also includes "decision tables with real thresholds, named error signatures". The gate ships a verdict
table (CLEAN/REFUSED/UNEVALUABLE → 0/2/3), real thresholds (`target` 8, `MIN_SHORTCUTS = 3` at `replay-gate.py:31`,
`TIMEOUT = 300`), and named error signatures (`config_shortcut_count`, `config_shortcut_duplicate_class`,
`counter_receipt_unreadable`, `counter_receipt_fields`, `counter_target_mismatch`, `positive_control_absent`,
`shortcut_absent:<class>`). If those land as a SKILL/corpus decision table, depth moves.

*Why it fails at the measured revision:*

1. **The depth surface carries nothing about the gate at `c79bbe7b`.**
   `git show c79bbe7b:SKILL.md | grep -c 'REPLAY_GATE\|replay-gate'` → `0`.
   `git grep -n 'replay-gate\|REPLAY_GATE' c79bbe7b -- corpus` → no output.
   The +51 SKILL lines in `ec3125ad..c79bbe7b -- SKILL.md` are the stopped **C1** GNU version-needs table and the
   round-34 instrument registry for `elf-version-needs.py` / `version-needs-counter.py` / `freeze-integrity.py`
   (`git diff` reviewed whole). The gate has no SKILL registry row, no knowledge entry, no citation. A reader at the
   measured revision cannot act on the gate from SKILL.md — the depth signal is literally absent.
2. **The depth proxy does not move.** Command `A` (`SCORECARD.md` "Measurement recipes", run read-only against Git
   objects) at both revisions:

   | revision | rule_blocks | citation_resolved_rules | depth_score | coverage_score |
   |---|---|---|---|---|
   | `ec3125ad` (base) | 17 | 17 | 10.0 | 10.0 (120/120) |
   | `c79bbe7b` (freeze) | 17 | 17 | 10.0 | 10.0 (121/121) |

   Depth 17/17 both sides, exactly as the claim itself declares (`10 -> 10`).
3. **The counting command cannot detect a depth move even if one occurred.** Every clause of
   `c2-shortcut-gate-counter.py` is an instrument clause: `selftest_clean`, `mutants_killed` (mutants of the gate's own
   branches), `red_refused`, `green_clean`, `green_positive_meets_target`, `gate_present`. There is no citation check,
   no decision-table content check, no field/threshold check. `gate_present` is even hardcoded `True` after the early
   return (`c2-shortcut-gate-counter.py:119`), so it is a tautology in every scored run.
4. **The gate does not certify structure; it certifies a registry and a report** — see §4 counterexamples. Its CLEAN is
   a function of (a) which classes are listed in the config and (b) what the counter prints. Neither is domain detail.
5. **No cited source binds to the instrument.** `S106` (binutils `readelf.c`, this round's opened source) appears in
   `claims.json:60` only: `git grep -n S106 c79bbe7b -- tools corpus` → no output. The only "source" inside the gate is
   the obligation label `QUALITY 67` (`replay-gate.py:4`). Depth's definition asks for cited sources; the gate cites a
   lesson, not a source, and the source it opened is not referenced by any gate file.
6. **Lane precedent already names this class of move `operability`.** Four earlier capability acquisitions were
   recorded as operability, each with "SKILL.md registry row + capability row entered": `SCORECARD.md:688` (C2),
   `:750` (C3), `:913` (citation-drift probe), `:1207` (contained-analyze). R34-C2 is the same shape of move
   (a committed probe/gate + a registry row), with the difference that the registry row is missing at the measured
   revision. Labelling it `depth` diverges from the lane's own convention for identical artifacts.

### 3.2 What the depth label is doing

`AXES.md:32-34` requires at least one claim on the lowest-scoring non-retired owned axis, waived only by the stagnation
nudge. The nudge waives it only when the window is exhausted; the card's last recorded capability entry is round 17
(`SCORECARD.md:2464`), and the group is not retired. So the `depth` label is what makes this round satisfy the
lowest-axis obligation on paper. The label is load-bearing while the surface behind it is not: the move is an
unowned-proxy capability move (as rounds luna-round-8 / arc2 rounds 1-4 recorded operability as a *fleet* axis with
"unowned proxy", e.g. `SCORECARD.md:688`), and unowned-proxy moves do not discharge the lowest-axis rule. That is the
real harm: a *calibration* defect created by an axis label, not by a score (no score was overclaimed: `10 -> 10`).

## 4. Counterexamples (strongest available from local evidence)

All run on a pin-verified scratch copy (§5), absolute `--root`, `python3` = Python 3.14.8.

**C4a — an unregistered structure-blind class meets the target on the "identity-defeating" green surface.**

The green counter permutes the name pool and rewrites each `name_off`; that preserves (i) the *set* of name strings and
(ii) the ordered `(flags, value)` list. The sorted string bag is therefore an invariant. Reader written by this seat:
`/fast/scratch/hyaku/kaidoku-r34b/w1/CritAxisFit/namebag_keyed.py` — it never resolves `name_off`, keys a memorized
answer on the sorted printable-string bag.

```
python3 -I -B <R>/tools/round-34/mini-fix/mini-counter.py --root <R> \
  --control-reader <R>/tools/round-34/mini-fix/readers/namebag_keyed.py
-> {"matched": 8, "target": 8, "met_target": true, "finding": "records_match"}   exit 0   (07:20:26Z)
```
Registered as an eighth class in a scratch copy of the green config:
```
python3 -I -B root/tools/round-34/replay-gate.py --root <R> --config <R>/tools/round-34/gate-config-plus-namebag.json
-> REPLAY_GATE_REFUSED finding=shortcut_meets_target shortcuts_below_target=7 shortcuts_over_target=string-bag  exit 2 (07:20:28Z)
```
So the green surface defeats the seven *registered* keys only. That is exactly what the frozen predicate says
("registered structure-blind shortcut readers … none meets the target"), so the predicate survives — but the property
being demonstrated is registry coverage, i.e. harness operability, not structural depth.

**C4b — the gate certifies a report, not a decode.** A counter that never reads a fixture and answers by the reader's
basename:
```
python3 -I -B root/tools/round-34/replay-gate.py --root <R> --config <R>/tools/round-34/gate-config-reader-keyed.json
-> REPLAY_GATE_CLEAN finding=no_shortcut_meets_target shortcuts_below_target=7 shortcuts_over_target=-  exit 0 (07:20:43Z)
```
`run_counter` trusts `matched`/`target`/`met_target` from the counter's stdout (`replay-gate.py:76-101`); nothing
checks that the counter executed the reader. This is a design limit of a self-declared-field harness (defensible for a
pre-freeze instrument, but it is not evidence of ELF comprehension). It reinforces that the moved surface is
instrument plumbing + a self-assessment gate.

**C5 — `predicate_identity` is false on its own terms.** Two distinct sentences, not one:

| site | sha256[:16] | chars |
|---|---|---|
| `claims.json` `predicate` | `7c6c17f0cca6c680` | 237 |
| `gate-config-mini.json` / `gate-config-naive.json` `predicate` | `7c6c17f0cca6c680` | 237 |
| `c2-shortcut-gate-counter.py` `PREDICATE` (`:23`) | `8340aea51154fc0e` | 351 |
| production receipt `after/c2-at-instruments.json` `predicate` | `8340aea51154fc0e` | 351 |

The config sentence states the *obligation* ("a finite … counter is frozen only after …"); the counter/receipt sentence
states the *instrument test* ("the committed replay gate refuses the shape-only counter … and its selftest kills every
mutant of its own branches"). The claim's assertion that these are one sentence is index-inaccurate. The verdict
labels themselves are frozen and stable (verified: `REPLAY_GATE_CLEAN`/`REFUSED`/`UNEVALUABLE` appear verbatim).

**C7 — operability defect in the delivered instrument (bounded).** With a relative `--root`, the gate resolves the
reader path against its own cwd but runs the counter with `cwd=<root>` (`replay-gate.py:76-80`), so the reader is not
found and the failure surfaces as a *misspelled* finding:
```
python3 -I -B root/tools/round-34/replay-gate.py --root root --config root/tools/round-34/gate-config-mini.json
-> REPLAY_GATE_UNEVALUABLE finding=counter_receipt_fields shortcuts_below_target=0 -   exit 3   (07:20:14Z, reproduced twice)
```
The truthful finding is `shortcut_absent:`/`positive_control_absent`; `counter_receipt_fields` is misleading. Absolute
`--root` (the production invocation) is correct and CLEAN. A reader of SKILL.md alone cannot learn this, because the
gate has no SKILL row at the measured revision (§3.1.1).

## 5. Reproduction receipts

Pin check first (read-only, lane worktree): 26/26 pinned paths match `claims.json.pins` (sha256, `ABSENT` = none;
`pins: 26, mismatch: []`). Scratch copy: `cp -a tools/round-34 root/tools/round-34` under the seat scratch root.

| # | command (root `R=…/CritAxisFit/root`) | exit | UTC |
|---|---|---|---|
| 1 | `replay-gate.py --root "$R" --selftest` | 0 (12 cases, `failures: 0`, `mutants_killed: 3/3`) | 07:19:47Z |
| 2 | `replay-gate.py --root "$R" --config "$R/tools/round-34/gate-config-mini.json"` | 0 `REPLAY_GATE_CLEAN … shortcuts_below_target=7` | 07:20:00Z |
| 3 | `replay-gate.py --root "$R" --config "$R/tools/round-34/gate-config-naive.json"` | 2 `REPLAY_GATE_REFUSED … shortcuts_over_target=label-memorization` | 07:20:02Z |
| 4 | `mini-counter.py --control-reader …/label_replay_full.py` | 1 (`matched 0`, as designed) | 07:20:04Z |
| 5 | `mini-counter.py --control-reader …/namebag_keyed.py` | 0 (`matched 8/8`) | 07:20:26Z |
| 6 | gate + `gate-config-plus-namebag.json` | 2 (`over=string-bag`) | 07:20:28Z |
| 7 | gate + `gate-config-reader-keyed.json` | 0 (`CLEAN`, zero decoding) | 07:20:43Z |
| 8 | gate `--root root` (relative) | 3 (`counter_receipt_fields`) | 07:20:14Z and 07:20:16Z |
| 9 | command A at `ec3125ad` and `c79bbe7b` | 0 / 0 (depth 17/17 both) | 07:20:38Z |
| 10 | five control receipts (`…/r34b/controls/*.txt`) read: do-nothing `gate_absent`/exit 2; four gate mutants `MISS` with the named failing clauses | n/a (records) | 07:22:08Z |

The lane's own production receipt (`after/c2-at-instruments.json`, measured `c79bbe7b`) is consistent with #1-#3:
all six clauses true, `green_positive_matched: 8`, `shortcuts_below_target: 7`. Its arithmetic was not falsified here.

## 6. Impacted axes

| Axis | Impact | Detail |
|---|---|---|
| `depth` | **label unsupported; no harm to the score** | Surface absent at the measured revision (0 SKILL/corpus hits), proxy 17/17 → 17/17, declared `10 -> 10`. The depth label satisfies `AXES.md:32-34` on paper only. |
| `operability` | **actually moved, unowned proxy, not documented** | New runnable harness reproduced clean; but no SKILL registry row at the freeze, one misleading finding on relative `--root`, and a self-declared-field verdict (C4b). Lane precedent (`SCORECARD.md:688,750,913,1207`) would record exactly this as an operability capability acquisition. |
| `calibration` | **harmed (wording, not score)** | `predicate_identity` (`claims.json:52`) asserts one sentence where there are two (C5); `axis_basis` names the disqualifying fact ("admission instrument") in the same clause that claims depth. Both are self-assessment statements that do not match the repository. |

No axis score was overclaimed and no target/predicate was relaxed: the numerical part of the claim is honest.

## 7. What evidence would settle it — and what it showed

Settling test (falsifiable, cheap): *does the depth surface move at the revision the claim measures?* Operationally:
a SKILL decision table (verdict map + finding names + thresholds) or a corpus knowledge entry for the gate, cited and
resolvable, present at `c79bbe7b`, plus a counting command that resolves it. **Result: absent** — zero mentions at the
freeze; the only new depth surface in `ec3125ad..c79bbe7b` belongs to the stopped C1. The second settling test — does a
structure-blind reader the registry omits meet the target on the green surface — **result: yes** (C4a), which moves the
demonstrated property from "structural decoding" to "registry coverage".

Residual possibility, stated for the L1: if the wave's SKILL/knowledge drafts (assigned to the scribe seats in
`w1-spec.json`) land **before round admission**, a depth surface genuinely appears. That would be a *separate, later*
surface with its own measurement (e.g. a rule-block/citation growth under command A or an explicit content check);
it is not what the frozen counting command measures and does not retroactively convert this claim's instrument clauses
into depth evidence.

## 8. Smallest safe correction (reported, not applied; no wording fixed)

The claim is frozen; the kill rule forbids changing target, counter, predicate or label afterwards, and this seat has no
authority to relabel. The smallest safe correction is therefore at recording level, all L1-owned:

1. **Admission record:** land R34-C2's per-axis verdict as *no owned axis moved* (`depth` 10→10, proxy 17/17 both sides;
   `coverage` 10→10; `calibration` unchanged) and enter the gate as a **capability row** only. Do not let the `depth`
   axis field discharge the `AXES.md:32-34` lowest-axis obligation for this round.
2. **Doc landing before any depth credit:** if the gate's verdict table is to count as depth, land it in SKILL.md/corpus
   with the gate's finding names, thresholds and `QUALITY 67`, and measure it with a citation/content check — not with
   `c2-shortcut-gate-counter.py`, whose six clauses cannot see a document.
3. **Append-only wording correction:** record in LOG/round report that `predicate_identity` is index-inaccurate — the
   config sentence (237 chars, `7c6c17f0…`) and the counter/receipt sentence (351 chars, `8340aea5…`) differ — without
   editing `claims.json`.
4. **Lesson/QUALITY addendum:** REGISTER the two limits found here (unregistered string-bag class meets 8/8 on the
   green surface; a counter that reports by reader basename yields CLEAN) and the relative-`--root` misleading finding.
   These bound the capability's reach; omitting them repeats r32's "cannot tell structure from shape" family at one
   remove.

## 9. Tooling

Nothing was installed or upgraded; no pacman/uv/npm transaction was attempted (pacman is paused host-wide). Executed
with `/usr/bin/python3` = Python 3.14.8 and the lane's existing pinned instruments. No ELF carrier, fixture or reader
was executed as a program of interest: readers were run as `python3` by the counters, fixtures stayed static 0644
bytes. No lane file other than this report was written; no VCS command other than read-only `git show/ls-tree/diff/
grep/rev-parse` was run.

---

**VERDICT:** `AXIS_FIT_FAIL depth` — the surface R34-C2 actually moves at `c79bbe7b` is a structural-counter admission
*instrument* (operability, unowned proxy) with a self-reported-verdict boundary, not `depth`: the depth surface has zero
gate content at the measured revision, the depth proxy is 17/17 → 17/17, and the claim's own `axis_basis` names the
disqualifier. The claim's wording does **not** survive (`axis_basis` self-defeating; `predicate_identity` false, two
sentences 237/351 chars). No score overclaim, no target/counter relaxation: the numbers are honest, the axis label is
not. Smallest safe correction is admission-level recording plus a doc-and-citation landing before any depth credit;
nothing in the frozen claim was edited by this seat.
