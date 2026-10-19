# EX-21 — proposed SKILL.md registry-row update (patch text; seats cannot write SKILL.md)

Seat EX-21 · chain c3 · wave `arc3-loop1-round4` · 2026-10-19. The C3 claim requires
the registry row + README + tool to land **in the same commit** (round-8 coupled-landing
precedent). The README and the tool are inside EX-21's real target and are updated in
place; `SKILL.md` is seat-forbidden, so the row lands as this patch text.

## Base (re-derived at write time)

- `SKILL.md` sha256 `5eec51c089e57f5d5806b4728261fb8c959637580a73aed7be4cddc1866b8f3f`, 390 lines; the `custody-pair` row is the only line changed
  (line-neutral).
- Base row identity (sha256 of that line): `a94e79d9a4d34795cf7db985ebb58cf46e416dcdb3e38144fc7e5828fc91db89`.
- Patched result: `patch/skill-registry-row.patched.md`, sha256 `8e56f3d9ce21d16b2c46a398ad52aa2723c295008a76145b928265bdc88a68bf`, same line count.
- Patched row identity: `8f8e5408648c7aacfb0c161eee54c86514f35570f3a8e332526ca5fec136fa0e`.

## Apply

Replace the single `| custody-pair |` line in `SKILL.md` with the line of the same
prefix in `patch/skill-registry-row.patched.md`. Every substitution anchor is
asserted to occur exactly once by the generating step; a moved base must be
re-derived rather than force-applied.

## What the row gains (each clause revision-pinned to the landed tool `29bb45ae…`)

1. the both-absent ruling clause (only error-carrying stanzas are `UNEVALUABLE`);
2. `--require-paths N` is a **distinct resolved paths** gate (round-4 residual (c));
3. the USAGE row gains the receipt/sidecar/neighbour scope and the uncreatable
   receipt directory (residuals (a) and (b));
4. the write-guard cell names the derived sidecar and the sidecar-shaped neighbour;
5. selftest `22 → 28 fixture cases` with the six new closures named by class;
6. the selftest cell gains the duplicate/distinct coverage pair, the sidecar and
   neighbour refusals, the uncreatable receipt dir, and the both-absent control.

## Landing note (rule #14)

The row is revision-pinned by nature: the tool identity quoted in its semantics
(`29bb45ae…`) must be re-derived at landing, and the pointer-table anchor
`skill-registry-custody-pair-row` (precedence phrase) must stay alive — it is
unchanged by this edit (verified: the precedence clause is untouched).
