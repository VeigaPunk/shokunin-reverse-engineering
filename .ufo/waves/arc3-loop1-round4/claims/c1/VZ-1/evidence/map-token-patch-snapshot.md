# Map-token patch — line-neutral EVM row extension (arc3-loop1-round4, C1 chain)

Seat SC-1 · chain c1 · role scribe · 2026-10-19. **PATCH TEXT for the PARENT;
not applied — `corpus/README.md` was not touched by this seat.** Revision 1
(2026-10-19T14:14Z). This file records its own byte-identity only in the
revision log below, re-derived after every revision (rule #14).

Target: `corpus/README.md`, the EVM row — `corpus/README.md:38` at HEAD
`015e1bab914713568f339fd53999bc180459cc40` (README 190 lines, sha256
`a451ad1664cda0cb87f3a76e974de818a1e401387bad6251b98cd6b0df8ede3a`; RV-2
independently pinned the same value in `evidence/baseline-pins.txt`).

Form: **line-neutral** — same physical line count (190 → 190), exactly one
line differs (`:38`). The token is **ADDITIVE-ONLY**: exactly one token
appended to the row's token cell, every other byte of `:38` unchanged. This is
the r3 PRIMARY form (`arc3-loop1-round3/claims/c1/records-drafts/map-token-patch.md`
rev 2 — the form the r3 verdict's debt #2 selected as the r1-form-safe choice).
The entry file must land with the stem named in the token.

## Old line (`:38`, verbatim)

```
| EVM | `2026-10-13-r3-evm-interface`, `2026-10-19-arc3-r1-evm-real-solc`, `2026-10-19-arc3-r3-evm-optimizer-shapes` | held — EVMole selectors recovered from a synthetic dispatcher (r3-07) and from real solc-0.8.37-compiled runtime carriers (arc3-r1); positional encoding quirk |
```

## New line — PRIMARY (ADDITIVE-ONLY, line-neutral)

```
| EVM | `2026-10-13-r3-evm-interface`, `2026-10-19-arc3-r1-evm-real-solc`, `2026-10-19-arc3-r3-evm-optimizer-shapes`, `2026-10-19-arc3-r4-evm-vyper-leg` | held — EVMole selectors recovered from a synthetic dispatcher (r3-07) and from real solc-0.8.37-compiled runtime carriers (arc3-r1); positional encoding quirk |
```

## New line — SECONDARY (reworded state cell; only if the parent prefers it)

Rewriting the state cell would state the Vyper leg's two deltas (the third
dispatcher shape; the offset reading's solc scope). It **fails** the
additive-only criterion — prose is rewritten — so it is kept only as an
alternative, not as the recommended form:

```
| EVM | `2026-10-13-r3-evm-interface`, `2026-10-19-arc3-r1-evm-real-solc`, `2026-10-19-arc3-r3-evm-optimizer-shapes`, `2026-10-19-arc3-r4-evm-vyper-leg` | held — EVMole selectors recovered from a synthetic dispatcher (r3-07), real solc-0.8.37-compiled runtime carriers (arc3-r1), optimizer-enabled non-ERC-20 carriers (arc3-r3), and Vyper-0.4.3-compiled carriers incl. a modulo-indexed jump-table dispatcher (arc3-r4; the "offsets land on JUMPDESTs" reading is solc-scoped); positional encoding quirk |
```

## New line — HONEST-STOP variant (only if the Vyper leg had failed)

Not applicable this round: every Vyper runtime leg recovered its planted set
K/K (this seat's own runs: 15/15 three legs, 4/4, 0/0 creation). Kept only so
the parent has the branch if a landing-time re-measure contradicts the tree:

```
| EVM | `2026-10-13-r3-evm-interface`, `2026-10-19-arc3-r1-evm-real-solc`, `2026-10-19-arc3-r3-evm-optimizer-shapes`, `2026-10-19-arc3-r4-evm-vyper-leg` | held (scoped) — EVMole selectors recovered from a synthetic dispatcher (r3-07) and real solc-0.8.37 runtime carriers (arc3-r1); arc3-r4 Vyper leg recorded as an honest stop (see entry); positional encoding quirk |
```

Parent: land exactly ONE variant and keep the token == the landed entry's
file stem.

## Apply recipe

```bash
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
# 1) place the entry file first (corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md),
#    then apply this one-line substitution:
python3 - <<'PY'
import pathlib
p = pathlib.Path('corpus/README.md')
lines = p.read_text().splitlines(keepends=True)
old = "| EVM | `2026-10-13-r3-evm-interface`, `2026-10-19-arc3-r1-evm-real-solc`, `2026-10-19-arc3-r3-evm-optimizer-shapes` | held — EVMole selectors recovered from a synthetic dispatcher (r3-07) and from real solc-0.8.37-compiled runtime carriers (arc3-r1); positional encoding quirk |\n"
assert lines[37] == old, lines[37]
lines[37] = "| EVM | `2026-10-13-r3-evm-interface`, `2026-10-19-arc3-r1-evm-real-solc`, `2026-10-19-arc3-r3-evm-optimizer-shapes`, `2026-10-19-arc3-r4-evm-vyper-leg` | held — EVMole selectors recovered from a synthetic dispatcher (r3-07) and from real solc-0.8.37-compiled runtime carriers (arc3-r1); positional encoding quirk |\n"
p.write_text(''.join(lines))
PY
```

Do not insert or delete lines. Any equivalent single-line substitution is fine.

## Rehearsal (this seat, on a scratch tree — the lane repo was never written)

`git archive HEAD` → `/var/tmp/sc1-r4/rehearsal/tree`; the literal entry text
extracted to `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md`; the
PRIMARY substitution applied. Measured:

| observable | before | after |
|---|---|---|
| `corpus/README.md` lines | 190 | **190** |
| lines differing (`diff` vs `git show HEAD:corpus/README.md`) | — | exactly `:38`, one line |
| coverage-map token occurrences | 85 | **86** |
| coverage-map unique tokens | 83 | **84** |
| knowledge files | 83 | **84** (one added, zero removed, zero modified) |
| command A (filesystem form) | 83/83, 14/14 | **84/84, 14/14**, `missing []`, `dangling []` |
| prior-83 knowledge files | — | **byte-identical** (compared against RV-2's `evidence/prior-83.sha256`, 83/83 rows: added = the new stem only, removed = none, modified = none) |
| README after-state sha256 | `a451ad16…` | `1cd052605e9d27f38e8c9b9b164fa64d0482b61d4acf0a2b80223cb4cec29d1e` |
| entry file literal | — | 18,166 B / 32 lines, sha256 `da42d9a23eaea87104ad71c7beacf0465a04f27482dd063d625b8e54a7161ebc` |

Rehearsal deviation from recipe A (stated, per the r3 precedent): the scratch
form reads the filesystem tree instead of Git objects. The parent must
re-measure at the records commit from real Git objects — an unrun check has not
passed.

## Verification obligations (parent-side, at the records commit)

1. `wc -l corpus/README.md` → 190 both sides; `diff` of before/after shows one
   changed line only (`:38`).
2. Command A re-measures `knowledge_files = mapped = 84`, `missing []`,
   `dangling []`, rules 14/14 — with the prior 83 byte-identical.
3. Citation-drift probe findings = 0 at HEAD in both modes (the token adds no
   graded `path:line` citation; the entry's own citations are the C3 chain's
   table work).
4. The landed entry's file stem equals the token exactly:
   `2026-10-19-arc3-r4-evm-vyper-leg`.
5. The entry's first line is the staging HTML comment (as in the r1/r3
   entries); the map row and the stem are the pair.

## Revision log (self-identity, re-derived per revision)

| rev | utc | sha256 of this file | note |
|---|---|---|---|
| 1 | 2026-10-19T14:14Z | see `SC-1/README-identities.txt` (re-derived after the final write) | initial draft: line-neutral mechanic; PRIMARY additive-only; SECONDARY reworded; honest-stop variant retained (not applicable); rehearsal table from this seat's scratch run |
