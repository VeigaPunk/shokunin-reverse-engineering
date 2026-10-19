# EX-21 — proposed SKILL.md registry-row update (patch text, apply-ready; seats cannot edit SKILL.md)

Seat EX-21 · chain c2 · wave `arc3-loop1-round3` · 2026-10-19. The frozen C2 claim
requires the registry row + README + tool to land **in the same commit**
(round-8 coupled-landing precedent). The README is inside EX-21's real target and
is already updated in place; `SKILL.md` is seat-forbidden, so the row lands as
this patch text. One voice per row (round-2 D10): `claims/c2/EX-30/registry-row.patch.md`
is the scribe's merge candidate; this text is the implementer's revision-pinned
form — the parent merges one.

## Base (re-derived at write time)

- `SKILL.md` sha256 `c134afcb2e648aa3f8ff96f11d03aee2be6715811cb7edb3b7be6ac40aa0aa90`,
  390 lines; the `custody-pair` row is **line 390** and is the only line changed.
- Base row identity (sha256 of that line): re-derived by the apply script below.
- Patched result: file `5eec51c089e57f5d5806b4728261fb8c959637580a73aed7be4cddc1866b8f3f`,
  still 390 lines (line-neutral); patched row `cf5111a795a7bfee0c49534bd28307d95a8c69e64ce1bf473303e1cf9ddde14b`.

## What the row gains (each clause revision-pinned to the landed tool `7cd19c3c…`)

1. exit map `+ 14 UNEVALUABLE` (exists-but-unevaluable; classified before the
   both-absent branch — never a fail-open MATCH) and the 2 USAGE description
   extended with the `--require-paths N` coverage shortfall (+ the printed
   `REFERENCE-COVERAGE: n/N paths present in reference; unaccounted: <canonical
   paths absent from the reference>` line) and the unusable `selftest --scratch` base;
2. precedence `CONTENT-DRIFT > UNEVALUABLE > ABSENT > …`;
3. capture exit set `0 / 14 / 13` (receipt written either way);
4. `READ-ERROR`/`STAT-ERROR` recorded in the receipt instead of a silent "absent";
5. `verify … [`--require-paths <N>`]` in the command cell, and v1 references
   covered by the same gate;
6. write guard over `set(--paths) ∪ CUSTODY_PATHS` by resolved path **and inode**
   (self-harm guard, not a security boundary);
7. selftest `15 → 22 fixture cases` with the seven closure cases named by class.

## Apply

```sh
# from the repo root, after re-verifying the base identity:
sha256sum SKILL.md   # expect c134afcb2e648aa3f8ff96f11d03aee2be6715811cb7edb3b7be6ac40aa0aa90
python3 .ufo/waves/arc3-loop1-round3/claims/c2/EX-21/apply-registry-row.py SKILL.md
#   -> prints: patched line 390; file sha256 5eec51c0…; row sha256 cf5111a7…
# every anchor is asserted to occur exactly once; refusal (exit 1) on a moved base;
# a unified diff of the same edit is kept alongside as `proposed-skill-registry-row.patch`.
```

Post-apply checks (line-neutral, one occurrence each):

```sh
grep -c '14 UNEVALUABLE' SKILL.md      # 1
grep -c '22 fixture cases' SKILL.md    # 1
wc -l SKILL.md                          # 390
```

## Landing note (why this text can go stale)

The row is revision-pinned by nature (round-2 D8 shape): if another round-3
landing edits `SKILL.md` first, re-run the apply script against the new base —
anchors are phrase-level, not line-number-level, and the script refuses on any
moved anchor rather than mis-applying. The tool identity quoted in the row's
semantics (`7cd19c3c…`) must be re-derived at landing per rule #14.