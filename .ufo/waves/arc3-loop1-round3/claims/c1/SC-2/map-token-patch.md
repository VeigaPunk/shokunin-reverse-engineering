# Map-token patch — line-neutral EVM row extension (arc3-loop1-round3, C1 chain)

Seat SC-2 · chain c1 · role scribe · 2026-10-19. **DRAFT for the PARENT; not
applied — `corpus/README.md` was not touched by this seat.** Revision 1
(2026-10-19T~13:12Z). This file records its own byte-identity only in the
revision log below, re-derived after every revision (rule #14).

Target: `corpus/README.md`, the EVM row — `corpus/README.md:38` at HEAD
`c07af80fcf3a60f9c6a0ca09b6e23fb5794d3311` (README 190 lines, sha256
`6ac43e838bca7d08cc7ac3c24cff60042cb174d92b08363db0798fa844163577`; captured
verbatim by RV-4 at `claims/c1/RV-4/README.before.md`, byte-identical to HEAD —
this seat re-ran the diff, `IDENTICAL`).

Form: **line-neutral** — same physical line count (190 → 190), exactly one line
differs (`:38`). The entry file must land with the stem named in the token; the
stem and token are paired r1-precedent (the r1 D4 lesson: stems must agree).

## Old line (:38, verbatim)

```
| EVM | `2026-10-13-r3-evm-interface`, `2026-10-19-arc3-r1-evm-real-solc` | held — EVMole selectors recovered from a synthetic dispatcher (r3-07) and from real solc-0.8.37-compiled runtime carriers (arc3-r1); positional encoding quirk |
```

## New line — PRIMARY (success form; applies if the round's optimizer carriers recover K/K)

```
| EVM | `2026-10-13-r3-evm-interface`, `2026-10-19-arc3-r1-evm-real-solc`, `2026-10-19-arc3-r3-evm-optimizer-shapes` | held — EVMole selectors recovered from a synthetic dispatcher (r3-07), real solc-0.8.37-compiled runtime carriers (arc3-r1), and optimizer-enabled non-ERC-20-shaped carriers (arc3-r3); positional encoding quirk |
```

## New line — HONEST-STOP variant (only if the optimizer leg defeats the extractor)

```
| EVM | `2026-10-13-r3-evm-interface`, `2026-10-19-arc3-r1-evm-real-solc`, `2026-10-19-arc3-r3-evm-optimizer-shapes` | held (scoped) — EVMole selectors recovered from a synthetic dispatcher (r3-07) and real solc-0.8.37 runtime carriers (arc3-r1); arc3-r3 optimizer-enabled leg recorded as an honest stop (see entry); positional encoding quirk |
```

Parent: land exactly ONE variant, matching what the round's probe envelopes
show, and keep the token == the landed entry's file stem.

## Apply recipe

```bash
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
# 1) place the entry file first (corpus/knowledge/2026-10-19-arc3-r3-evm-optimizer-shapes.md),
#    then apply this one-line replacement, e.g.:
python3 - <<'PY'
import pathlib
p = pathlib.Path('corpus/README.md')
lines = p.read_text().splitlines(keepends=True)
old = "| EVM | `2026-10-13-r3-evm-interface`, `2026-10-19-arc3-r1-evm-real-solc` | held — EVMole selectors recovered from a synthetic dispatcher (r3-07) and from real solc-0.8.37-compiled runtime carriers (arc3-r1); positional encoding quirk |\n"
assert lines[37] == old, lines[37]
lines[37] = "<new line verbatim + newline>"
p.write_text(''.join(lines))
PY
```

(Any equivalent single-line substitution is fine; do not insert or delete lines.)

## Verification obligations (parent-side, at the records commit)

1. `wc -l corpus/README.md` → 190 both sides; `diff` of before/after shows one
   changed line only (`:38`).
2. Command A re-measures `knowledge_files/mapped = 83/83`, `missing []`,
   `dangling []`, rules 14/14 — see the entry draft's rehearsal notes (this seat
   rehearsed the pair on a scratch tree; the parent must re-measure from real
   Git objects at the records commit).
3. Citation-drift probe findings = 0 at HEAD in both modes (the token adds no
   graded `path:line` citation; the entry's own citations are probed per the
   C3 chain's table work).
4. Prior-82 knowledge files byte-identical (only the one new file added).

## Revision log (self-identity, re-derived per revision)

| rev | utc | sha256 of this file | note |
|---|---|---|---|
| 1 | 2026-10-19T13:12Z | (computed at final revision only — see the entry draft's final identity block; earlier revs superseded) | initial draft: line-neutral mechanic + primary/honest-stop variants |