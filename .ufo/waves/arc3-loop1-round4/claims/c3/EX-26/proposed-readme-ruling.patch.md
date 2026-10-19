> **STATUS: SUPERSEDED — DO NOT APPLY.** EX-21 landed its own ruling text at
> 11:09Z (README `a418675b…` → `125e7e02…`), an edited version of this proposal.
> Applying this patch on top would duplicate the ruling section. Retained as the
> provenance of the wording, not as a pending change. See `EX-26/ruling.md` §3 A8
> and §4 R-4.

# proposed patch text — the (d) both-absent ruling in the gate README (seat EX-26, chain c3)

Target: `.ufo/gates/custody-pair/README.md`
Base revision under test: **sha256 `f30df42e0a547a0aefd21590c0f975acf06d91161fcb6db77c8934960efeb193`**
(185 lines, 9,603 B, mtime epoch `1792415712` — the r3 bytes at HEAD `015e1ba`).
This seat proposes text only and has applied nothing to the real target; every
measurement below ran on a scratch clone (`/var/tmp/ex26/clone`, `git clone
--shared` of this repo, commits local to the clone). Evidence:
`EX-26/evidence/evidence-{1,2,3}.txt`, block `evidence/ruling-block.txt`.

## Why a text-only change is the right class

The (d) debt is a **documentation** gap, not a behavior gap. The live tool already
does the declared thing, measured first-hand on 14 scratch fixtures
(`evidence-1.txt` §3, `evidence-2.txt` §5-8): a cleanly-absent stanza on both sides
is `MATCH exit 0`; an error-carrying stanza is `UNEVALUABLE exit 14`; a cleanly-absent
reference against an error-carrying candidate is `UNEVALUABLE 14`, never `MATCH`. So
this patch adds no code and changes no class. It lands the adjudication the frozen
claim asks for ("(d) is adjudicated with the ruling text landed in the README").

## The patch

Insert the block below immediately **before** the line
`## Exit codes (declared)`. The block is byte-exact in
`evidence/ruling-block.txt` (1,834 B, sha256
`8e0a88ee293209da05529ba73c9f55e62232a2d9877cd2507be94a4f8de4fe77`).

```diff
@@ before `## Exit codes (declared)` @@
+## The both-absent `MATCH` (ruling, arc3-loop1-round4)
+
+The round-2 D2 debt named the `MATCH exit 0` on a both-sides-absent path as part of
+the fail-open class. This instrument adjudicates that reading, and the adjudication
+is the declared design: **only error-carrying stanzas are `UNEVALUABLE`; a cleanly
+absent stanza on both sides is `MATCH`.**
+
+- *Cleanly absent* means the stanza records no `SHA256` and carries no
+  `READ-ERROR`/`STAT-ERROR` on either side. The `MATCH` rests on the two stanzas'
+  own recorded existence state (`EXISTS: no` on both) — that is the fact the
+  both-absent branch tests, and it is the only branch that can produce this row.
+  The row prints `compared=0/11` because there is nothing further to compare, not
+  because the comparison is empty. Absence on one side only is `ABSENT` (13): a
+  reference path that appears later is still caught.
+- *Error-carrying* is the fail-open class the debt named: a stanza carrying
+  `READ-ERROR` or `STAT-ERROR` on either side is `UNEVALUABLE` (14), classified
+  **before** the both-absent branch, so an unreadable path can never read as a
+  `MATCH`. This holds receipt-vs-live and receipt-vs-receipt (the parser reads both
+  error keys).
+- Severity is unchanged: a cleanly-absent stanza never outranks `UNEVALUABLE` or
+  `CONTENT-DRIFT` in the verdict — a mixed pair reports the worst class it found.
+
+A receipt pair over cleanly-absent paths is therefore a positive record ("absent on
+both sides"), not a vacuous pass — but it is a weak witness by construction: no
+content is compared. That is also why the coverage gate is a *stanza* gate —
+`--require-paths N` counts stanzas, not distinct paths (measured: one path repeated
+N times satisfies it). Pair an all-absent reference with a present-path reference
+when the witness is meant to carry content.
+
```

## Measured before → after (scratch clone, all first-hand)

| quantity | before | after |
|---|---|---|
| README sha256 | `f30df42e…` | `f54d9467030bb250f85f11f18d8575e7eec9082ab76610de9681bf0fef847e10` |
| README bytes / lines | 9,603 / 185 | 11,437 / 214 (+29 lines) |
| EX-27's own (d) check, `readme_ruling()` hit count | **0** | **6** |
| citation-drift probe, default mode | `reported findings=0 exit=0` | `reported findings=0 exit=0` |
| citation-drift probe, `--strict` | `clean findings=0 exit=0` | `clean findings=0 exit=0` |

The (d) check is the wave's own instrument, run verbatim from
`claims/c3/EX-27/harness/regress-r4.py` (`readme_ruling`, its `README_WORK` path
repointed at the two files) — before: `hits=0`; after: `hits=6`.

## Citation safety (checked, not assumed)

- **No line-pinned citation into the custody README exists.** The four
  `custody-readme-*` entries in `.ufo/gates/citation-drift/pointer-table.json` are
  all `kind: anchor` (no line pin), and no `exact`/`extracted` entry names
  `.ufo/gates/custody-pair/README.md`; the census instrument
  `.ufo/gates/c1-census-v10.py` contains no reference to it either. So a +29-line
  insertion cannot move a pinned line. Verified by grep at 14:09Z.
- **The four anchors survive the insertion** — the probe reads clean on the patched
  clone in both modes (above).
- **The anchors have teeth** (control, `evidence-3.txt` §9c): neutering each anchor
  in turn reddens exactly its own entry (`citation_dead
  entry=custody-readme-{rewrite-identity,precedence,scratch-never-tmp}`, exit 1);
  the `v2-fieldset` needle (`MTIME_UTC_RENDER`) has 2 occurrences and needs both
  neutered to redden, which is a property of the anchor substring semantics, not of
  this patch. Restoring returns `clean findings=0 exit=0`.

## Landing notes for EX-21 / the parent

1. Insert verbatim from `evidence/ruling-block.txt`; do not retype — the block is
   the artifact, its digest is the identity.
2. The patch is additive and line-shifting only *below* the insertion point. It
   touches nothing above `## Exit codes (declared)`, so the Usage section and the
   v1-compat table keep their bytes.
3. If EX-21 lands a different ruling wording, this text is a **proposal** and should
   be superseded, not merged — two ruling paragraphs would be worse than one. The
   operative content to preserve is: cleanly-absent-both-sides = `MATCH` by design;
   error-carrying = `UNEVALUABLE`, classified before the both-absent branch; the
   qualifier "cleanly" is load-bearing (an error on either side, including a
   `STAT-ERROR` against a cleanly-absent reference, is `UNEVALUABLE`, not `MATCH`).
4. Re-run the probe (both modes) after landing; re-derive the README digest. This
   seat's after-digest binds only the scratch-clone bytes.
5. No registry-row (SKILL.md) change is needed for (d): the row already carries the
   UNEVALUABLE-before-both-absent clause and its anchor needle
   (`skill-registry-custody-pair-row`) is untouched by this patch.
