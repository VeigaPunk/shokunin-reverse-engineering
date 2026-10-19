# Pointer-refresh PATCH TEXT — `SHONEN.md:6` (queue-drain craft-section range)

Seat EX-04 (c1, executor) — wave `arc3-loop1-round2`, 2026-10-19.
Lane repo HEAD throughout: `14b1682b1128d2e41085ebc79c9addeb8786d420`
(`SKILL.md` 371 lines sha256 `483b0eba27458c138fdbe760d83a33f0da54b251ec028f033d83a5ae3d0175eb`;
`SHONEN.md` 12 lines sha256 `4e3ba4d2f414ded89d74ccd9849cb0b5857f61e504179691250637a3f6a618c8`).
All simulation on scratch trees under `/dev/shm/ex04/` (no lane-repo bytes written
outside this seat's claim dir; no git mutations in the lane repo).

## 0. Result

- **Exactly one live-surface file cites the queue-drain craft section's line
  range: `SHONEN.md:6`.** Every other citer is a dated row, an append-only
  record, or a frozen evidence/wave artifact, and must **not** be refreshed
  (§1).
- The refresh must fix **three** things at the rule-#14 landing, not one: the
  range end (stale), the `13/13` count (stale), and — measured at HEAD before
  any append — a **pre-existing 4-line overshoot** by which the stated end
  `243` swallows the next section heading at `:242` (§2).
- Ready-to-land patch text: §4 (verbatim line + unified diff
  `shonen-refresh-rule14.patch`, sha256 `e80f20d21c903dd91a1970110a5c4295484fac37e1a0be7aacab63aa6f53eb38`).
  It reproduces EX-01 §4.3's proposed replacement (`81-254`, `14/14`) — this
  seat re-derived those numbers from EX-01's own payload rather than copying
  them (§3, §5).
- **Revision note (this artifact, rule #14 in action):** EX-01's payload was
  revised mid-wave (v1 13 lines/896 B `a47dc38d…` → v2 15 lines/1,071 B
  `6cc388cb…`, EX-01's own revision note citing this seat's `t1-geometry.txt`
  among its inputs). This artifact was re-instantiated against v2, not
  re-worded around v1: the earlier instantiation is kept as
  `shonen-refresh-rule14.v1-superseded.patch`
  (sha256 `226b8e3493f79de5388ea453a3958a765f979a15ee7d2909ad7ff1cfde5d6a9d`,
  proposed `81-252`), superseded — never a carried-over number.
- Land it in the **same commit** as the rule append (r9 precedent,
  `SCORECARD.md:1241-1242`: "SHONEN:6 refreshed same commit (81-243, 13/13)";
  `ba06c4d` changed both together).

## 1. Enumeration — every file citing the craft section's line range

Range-aware scan (any `SKILL.md:N` or `SKILL.md:N-M` overlapping the craft
section `81-241` at HEAD), excluding frozen wave trees
`.ufo/waves`, `.ufo/reports`, `.ufo/interactive-sessions`:
receipt `receipts/enumeration-nonwave.txt`
(sha256 `487bfa600e734a635f7e9f256da2e03e174d49d1a6a4ea9dcc8270a6b6619301`).

| File:line | Stated cite | Class | Action |
|---|---|---|---|
| `SHONEN.md:6` | `` `SKILL.md:81-243` `` + `13/13` | **live current-surface promotion assertion** | **REFRESH** (§4) |
| `LOG.md:685` | `SKILL.md:211-214` | append-only history (line numbers describe past states by rule; probe `exempt` entry) | none |
| `LOG.md:735` | `SKILL.md:81-195` | append-only history | none |
| `SCORECARD.md:24` | `SKILL.md:77-191` | dated measurement row ("Line citations to pre-existing lane files refer to the baseline revision", `SCORECARD.md:16-17`); probe `sc270-dated-record` precedent | none |
| `corpus/README.md:138` | `SKILL.md:81-195` | dated Knowledge-table row (2026-10-14); r7 adjudication "E21-dispositioned NO-CHANGE" (`arc2-loop1-round7/E6.md:120`) | none |
| `corpus/knowledge/2026-10-14-r14-02-final-sweep.md:47` | `SKILL.md:77-191` | dated lesson (history) | none |
| `corpus/lessons/2026-10-15-round-1.md:37` | `SKILL.md:207-210` | baseline-frozen lesson (r7 `S1.md:127-128`) | none |
| `evidence/round-1-2026-10-15/result.json:55`, `rubric.json:61` | `SKILL.md:158-165,207-210` | frozen evidence bundle | none |
| `.ufo/rounds/interactive-r1/wave-spec.json:61-101` | `SKILL.md:82-103` … `183-191` (per-rule audit prompts) | frozen wave spec (historical session record) | none (advisory: if that audit is ever re-run post-append, those per-rule ranges are stale) |
| `.ufo/waves/**`, `.ufo/reports/**` (~250 files) | many | frozen wave history | none |

Also checked: no live-surface citation targets `SKILL.md` **below** the
insertion point (the registry row is cited by content, not line — probe entry
`skill-registry-row` is `anchor`, line deliberately unpinned; the append is
pin-safe). `PROVINCE.md` cites no `SKILL.md` lines. `SKILL.md` has no
self-citations. Census v10 does not scope `SHONEN.md` (`grep -c SHONEN
.ufo/gates/c1-census-v10.py` → 0), so the probe's `shonen-skill-range` entry is
the only instrument that could ever cover this pointer.

## 2. Pre-existing defect measured at HEAD (before any append)

```
$ python3 craft-pointer-truth.py <tree at 14b1682b>
POINTER_TRUTH A1-start             PASS stated=81 true=81
POINTER_TRUTH A2-end               FAIL stated=243 last_rule=239 next_heading=242
POINTER_TRUTH A3-count             PASS stated=13/13 counted=13
POINTER_TRUTH_VERDICT: FAIL (failed=A2-end)
```
receipt `receipts/t0-checker.txt` — and the committed probe certifies that tree
`clean findings=0` (`receipts/t0-probe.txt`). Same numbers independently found
and drafted-but-unlanded at `arc2-loop1-round10`
(`E16.md:12-18,61-78` §3.1: "one token changed (`243` → `239`)"); carried debt,
still open at HEAD. The refresh below therefore lands the correction **and**
the new end in one token change.

## 3. Post-append geometry (EX-01's real payload, re-derived)

**Instantiated against EX-01 payload v2** (current at read-back; artifact
sha256 `885fa537…`, mtime 09:13:36). **If EX-01's payload hash differs at
landing, re-run §4.2 and regenerate the diff — do not land these numbers.**

- Payload v2 extracted from `claims/c1/EX-01/rule14.patch.md` between its
  `payload-begin`/`payload-end` markers and re-hashed here: **1,071 bytes, 15
  lines, sha256 `6cc388cb61a3023e8e62a0f63c0ff2e275665706373b184ad7d4801c3c91718f`**
  — equal to EX-01's v2 claim (`receipts/r1-payload-identity.txt`; v1 was
  896 B / `a47dc38d…`, superseded by EX-01's own revision note).
- Applied with EX-01's `evidence/apply-rule14.py` (anchor form: payload + one
  blank immediately after rule #13's last line) in a fresh scratch tree:
  `SKILL.md` 371 → **387 lines**, sha256
  **`a8170b96450f871282027b9adbc89cde08611457deb3a506cae3567701cd7e28`** —
  equal to EX-01's claimed v2 post-image (`receipts/r2-apply.txt`).
- Geometry after append: heading `## Queue-drain craft` = `81`; rule #14 spans
  **`:240-254`**; 14 rule blocks; `## Config custody` heading at **`:258`**
  (was `242`); lines 1–239 byte-identical (`cmp`, `receipts/r3-geometry.txt`).

If the integrator instead lands the block *before* the heading (EX-05's
`insert-rule.py` shape), the same payload puts the craft end at `:249` and the
heading at `:253` — measured: `receipts/t3-geometry.txt` (case B:
last_rule_line moves with the block length). **Always re-derive the end at the
landing tree** with §4.2's command; do not hand-carry a number (this is rule
#14's own discipline applied to the pointer).

## 4. The patch text

### 4.1 `SHONEN.md:6` — verbatim replacement (for the §3 landing geometry)

```
  asserted: `SKILL.md:81-254` (craft section; rules #11-14 added arc2 rounds 4/7/9 + arc3 round 2); 14/14 rule blocks have resolvable citations, not a full semantic audit — `SCORECARD.md`, command A; no identified outside verifier.
```

Attribution wording follows EX-01 §4.3 verbatim (`+ arc3 round 2`) to avoid
cross-artifact divergence; the alternative spelling `+ arc3-loop1-round2`,
used in the r4/r7/r9 lineage, is equally acceptable — no instrument grades
this token. The graded parts are the range and the `N/N` count.

### 4.2 Recompute at the landing tree (one command each)

```
python3 .ufo/waves/arc3-loop1-round2/claims/c1/EX-04/craft-pointer-truth.py .
# A2 detail prints: stated=<old> last_rule=<NEW END> next_heading=<H>
# A3 detail prints: counted=<NEW COUNT>   -> write `81-<NEW END>` and `<NEW COUNT>/<NEW COUNT>`
```

### 4.3 Unified diff (instantiated for the §3 landing geometry)

Attached, and reproduced here verbatim:
`shonen-refresh-rule14.patch` (sha256 `e80f20d21c903dd91a1970110a5c4295484fac37e1a0be7aacab63aa6f53eb38`).
`git apply --check` passes at the unrefreshed post-append tree
(`receipts/r7-apply-check.txt`: `APPLY-CHECK: OK at lane-HEAD+rule14 (SHONEN
unrefreshed)`).

```diff
--- a/SHONEN.md
+++ b/SHONEN.md
@@ -3,7 +3,7 @@
 Promotion to shokunin requires all of:
 
 - [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources
-  asserted: `SKILL.md:81-243` (craft section; rules #11-13 added arc2 rounds 4/7/9); 13/13 rule blocks have resolvable citations, not a full semantic audit — `SCORECARD.md`, command A; no identified outside verifier.
+  asserted: `SKILL.md:81-254` (craft section; rules #11-14 added arc2 rounds 4/7/9 + arc3 round 2); 14/14 rule blocks have resolvable citations, not a full semantic audit — `SCORECARD.md`, command A; no identified outside verifier.
 - [~] At least one end-to-end domain task executed and logged in LOG.md
   asserted: 2026-10-15 libjq open → instruction decode → export → close, `corpus/lessons/2026-10-15-round-1.md`, Executed native smoke; complete record at `evidence/round-1-2026-10-15/rea-bundle.json`; no identified outside verifier.
 - [~] Instructions executable by an agent without oral context
```

`SHONEN.md` stays 12 lines (1 line replaced, 1 insertion/1 deletion); the
other three boxes are untouched. Post-refresh sha256 in the scratch tree:
`6813bc93b7caa606694b18b5617934a8151051c21ed10e187857bbb121f00c88` — **the
integrator must re-derive the landed identity** rather than copy this number
(the practice rule #14 lands).

## 5. Before → after measurements (commands + receipts)

Real payload (EX-01's block), scratch `sim-real`:

| State | checker | command A | probe (committed table) | probe (end-anchored scratch) |
|---|---|---|---|---|
| HEAD, no append | **FAIL** A2 (`243` vs last_rule `239`) | 13/13, 82/82, 10.0/10.0 | clean findings=0 | — |
| + rule #14 (payload v2), SHONEN unrefreshed | **FAIL** A2 (`243` vs `254`) + A3 (`13/13` vs 14) | 14/14, 82/82, 10.0/10.0 | **clean findings=0 (silent pass)** | `citation_dead entry=shonen-skill-range` exit 1 |
| + refresh `81-254`, `14/14` | **PASS** (all four) | 14/14, 82/82, 10.0/10.0 | clean findings=0 | clean findings=0 |

Receipts: `receipts/t0-checker.txt`, `t0-commandA.json`, `t0-probe.txt`;
`r4-checker-stale.txt`, `r4-commandA.json`, `r4-probe-committed.txt`,
`r4-probe-enda.txt`; `r6-checker.txt`, `r6-commandA.json`,
`r6-probe-committed.txt`, `r6-probe-enda.txt`; full consoles
`receipts/sim-real-console.txt`, `receipts/sim-console.txt`; drivers
`receipts/sim-real.sh`, `receipts/sim.sh`, `receipts/commandA.py`
(byte-verbatim recipe A from `SCORECARD.md:92-124`).

Stand-in sensitivity run (block A 8 lines / block B 3 lines):
`receipts/t1-geometry.txt`, `t3-geometry.txt` — the end must track the block
(`249` vs `243`), which is why §4.2 exists. (Note: a 3-line block would make
HEAD's stale `243` accidentally correct — hand-arithmetic is not a method.)

## 6. Attacks attempted, with verdicts

1. *Some other live file also cites the range and this artifact missed it.*
   **Refuted**: range-aware scan over the whole committed tree minus frozen
   wave trees; live-surface hits = `SHONEN.md:6` only (§1 receipt).
2. *The committed probe already catches the staleness.* **Refuted by
   measurement**: `clean findings=0` on both stale states (HEAD, and
   post-append). Its `shonen-skill-range` needle is content-anywhere (rule #13
   text at `:233`, inside `81-243`), so it grades the range interior, never the
   endpoint or the count. Same conclusion, independently measured at r10
   (`E16.md:19-29`).
3. *The census catches it.* **Refuted**: census v10 `SCOPE` has no `SHONEN.md`
   entry (`grep -c SHONEN` → 0); census output moves only `lines=371→385`,
   `loci` unchanged, verdict PASS (EX-01 §3).
4. *r10's end-anchored needle (E16 §3.2) is the complete fix; adopt it now.*
   **Partially sustained**: it fires exactly on the stale state
   (`r4-probe-enda.txt`) and clears after the refresh (`r6-probe-enda.txt`).
   But its literal r10 form is anchored to **rule #13's closing words**; run
   against a *correct* post-14 range it fires too
   (`receipts/attackF-probe-r10literal-on-correct-range.txt`: `citation_dead`
   on `81-249`). It must be re-anchored at every rule landing — churn the r10
   CR2 already warned about for state-token pins. Kept as a proposal only; the
   probe table is not to be widened this round.
5. *Refreshing SHONEN could disturb the probe's other SHONEN entries.*
   **Refuted**: line 6 is replaced same-line; `shonen-province-range`,
   `shonen-lesson-file`, `shonen-evidence-bundle` target other lines; probe
   clean after refresh; file line count unchanged (12).
6. *`243` might be a legitimate convention (e.g. "include trailing blanks")*.
   **Refuted**: `242` is the next `## ` heading; no end convention may include
   it. The tight end is the last non-blank line (`239` at HEAD, `252` after
   the append).

## 7. Recommendations (proposals — none applied by this seat)

1. **Land §4's refresh in the same commit as EX-01's rule-#14 append** (the
   r4/r7/r9 precedent records "SHONEN refreshed same commit").
2. **Run `craft-pointer-truth.py` at integration** (and re-derive the landed
   `SHONEN.md` identity). It is the only instrument measured to redden on both
   stale states; it costs one command and is ground-truth structural (heading /
   last-rule / count), so it cannot be gamed by picking a friendly needle.
3. **Do not edit `.ufo/gates/citation-drift/pointer-table.json` this round**
   (no widening). Record the needle gap as named debt with the two measured
   options: (a) re-anchored end-needle — precise but requires re-anchoring each
   rule landing (attack 4); (b) the structural checker — maintenance-free but
   external to the probe.
4. Advisory: if `.ufo/rounds/interactive-r1/wave-spec.json`'s per-rule audit
   prompts are ever re-run, their `SKILL.md:82-103 … :183-191` ranges are stale
   after any craft append (frozen record; no action now).

## 8. Files written by this seat

- `pointer-refresh.patch.md` (this file)
- `craft-pointer-truth.py` (sha256 `1df6f51001079ba3f4ec4dac96f18e63030d04e96f866aec1de827140b534333`)
- `shonen-refresh-rule14.patch` — instantiated against EX-01 payload v2 (sha256 `e80f20d21c903dd91a1970110a5c4295484fac37e1a0be7aacab63aa6f53eb38`)
- `shonen-refresh-rule14.v1-superseded.patch` — v1 instantiation, superseded by EX-01's payload revision (sha256 `226b8e3493f79de5388ea453a3958a765f979a15ee7d2909ad7ff1cfde5d6a9d`)
- `shonen-refresh-example.patch` (stand-in geometry; sha256 `c47eb099b9bb0aea65bf2edad43613aee5e848c3a9ff8eb344c9a42f84a29a69`)
- `receipts/` (20+ receipts; inventory `receipts/t5-inventory.txt`,
  `receipts/r8-inventory.txt`; the r-series was regenerated against payload v2)

Scratch (`/dev/shm/ex04/`) may be deleted at integration.
