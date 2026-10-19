# EX-32 — proposed re-anchor: `skill-registry-custody-pair-row` (pointer-table entry)

Seat EX-32 · chain c2 · role executor · wave arc3-loop1-round3 · 2026-10-19.
**Proposal only — not applied.** `.ufo/gates/citation-drift/pointer-table.json`
and `expected.json` are EX-41's (C3's) real-path target; this seat wrote neither.
Patch text to be applied by EX-41 / the parent under the C3 chain's ownership,
with the digest re-pin in the same commit (the frozen-table coupling the probe
enforces with `pointer_table_tampered`).

## 1. The collision this closes (measured)

At the round's work commit, C2's required registry-row update (exact patch text:
`../EX-30/registry-row.patch.md`, patched SKILL.md `8efd8a87…`, line-neutral,
independently re-derived by this seat) rewrites the custody row's precedence
clause `CONTENT-DRIFT > ABSENT > …` to `CONTENT-DRIFT > UNEVALUABLE > ABSENT >
…` (new exit-14 class). C3's landed 57-entry table (EX-41, `bfc42f1b…`) anchors
`skill-registry-custody-pair-row` on the round-2 clause verbatim → at the
coupled landing the probe reads:

```
CITATION_DRIFT: citation_dead entry=skill-registry-custody-pair-row SKILL.md: no line matches 'precedence CONTENT-DRIFT > ABSENT > REWRITE-DRIFT > METADATA'
CITATION_DRIFT_VERDICT: reported findings=1 exit=0        (--strict: failed findings=1 exit=1)
```

(`evidence/original-sim.out`;
independently replicated by cross seat CN-1, `claims/cross/CN-1/consistency.md`
§3g — their evaluator and the probe agree on the same single finding.)

## 2. The patch (13-line diff, one entry)

`pointer-table-reanchor.diff` — renders to:

```diff
-      "must_match": "precedence CONTENT-DRIFT > ABSENT > REWRITE-DRIFT > METADATA-DRIFT > MATCH",
-      "note": "the round-2 custody-pair registry row's declared worst-finding precedence. Line unpinned for the same reason as its sibling row."
+      "must_match": "precedence CONTENT-DRIFT > (UNEVALUABLE > )?ABSENT > REWRITE-DRIFT > METADATA-DRIFT > MATCH",
+      "note": "the round-2 custody-pair registry row's declared worst-finding precedence, anchored with the optional UNEVALUABLE group so the needle holds both before and after the same-commit row revision (coupled landing; the collision is EX-32-measured)."
```

The `must_match` stays a regex (the probe grades with `re.search`,
`citation-drift-probe.py:181`); the optional group keeps the pinned
precedence order true in both worlds — pre-landing (round-2 row) and
post-landing (revised row). Verified against both texts:
`re.search(candidate, old_row)` and `re.search(candidate, new_row)` both True
(this seat, python3, 2026-10-19T13:15Z).

## 3. Re-pin procedure (same commit; canonical byte form)

The landed table's exact byte form is
`json.dumps(obj, indent=2, ensure_ascii=False) + "\n"` — reproduced
byte-identically by this seat before proposing (`ln 30348` round-trip check);
the landed `expected.json` is a single line with no trailing newline and only
the digest value moving. With the entry patched:

| object | value |
|---|---|
| re-anchored table sha256 | `a810bd17ea416fe0f3ed9e053e1e470ae833718f457b6d39399478c93de91a7b` |
| landed table sha256 (for contrast) | `bfc42f1bb131cbe3a972a16647d24b1f16d936083dd61496589540e791d58bb7` |
| landed expected.json sha256 | `d97dd60a942eaf53771c8224e84a9e8cdaf976dc66c3a543a450b1f1fa3827e2` |

Regenerate with EX-41's own builder (`claims/c3/EX-41/build-table.py`) after
editing the entry, then move the `pointer_table.sha256` pin to the new digest —
same-commit, per the frozen-run guard. This seat's scratch pair
(`/var/tmp/ex32r3/fix/`) is a byte-level demonstration of the procedure, not a
landable artifact (scratch only).

## 4. Post-fix measurement (landing simulation, real probe)

Clone `/var/tmp/ex32r3/clone` at `c07af80f` carrying: EX-30's patched SKILL.md
(`8efd8a87…`) + EX-21's tool revision (as of 13:15Z, `7cd19c3c…`) + EX-21's
README revision. Probe run against that tree:

- with the landed table: `reported findings=1 exit=0` (`evidence/original-sim.out`);
- with the re-anchored table + re-pinned scratch expected:
  `reported findings=0 exit=0` and `clean findings=0 exit=0`
  (`evidence/reanchored-sim.out`, `evidence/reanchored-sim-strict.out`).

## 5. Options note (parent's call; CN-1 §3g enumerates the same three)

1. **This patch (C3 re-anchors, re-pin same commit)** — cheapest; keeps C2's
   row describing the revised tool and C3's table self-consistent at landing.
2. C2 writes the old precedence chain into the new row (rejected here: the row
   would then describe the wrong map).
3. Serialize landings (C2 first, C3 re-derives) — equivalent outcome, more
   steps; the pre-registered re-run applies either way: probe at the work
   commit must read findings=0 both modes, and this seat's clone harness
   (`/var/tmp/ex32r3/`) reproduces the prediction for free.