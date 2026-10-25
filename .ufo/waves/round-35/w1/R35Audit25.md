# R35Audit25 — wave 1: reproduce indented id collision proof

Seat: R35Audit25 (executor, leaf). Wave: round-35 w1 (`r35-build`, milestone "Build evidence and first falsifications").
Item: **Reproduce indented id collision proof.** Constraints honored: lane paths read-only; outputs only in private `/tmp` and this report; no VCS mutation; no `find`/`du` under `/fast/scratch`; no subagents; no installs; no lane production writes.

## Verdict

The committed round-35 guard proof **reproduces**: the id-collision extraction pattern that accepts 0–3 leading spaces catches the indented registry row (`S002`, two leading spaces), and the staged set `{S002}` therefore yields a **nonempty** collision set `{S002}`. A column-zero-only pattern silently misses the same row (collisions empty) — the exact contrast the proof is about. No falsification of the frozen claims (C1/C2) was found; this is advisory evidence only.

## Evidence (commands, outputs, UTC 2026-10-25 16:17–16:18Z)

Fixture (lane, read-only) — `.ufo/waves/round-35/assimilation/id-guard-proof/`:

| file | sha256 | content |
|---|---|---|
| `fixture-registry.md` | `fff3b807…e5971` | header + `| S001 | x | … |` (col 0) + `  | S002 | indented row | … |` (two leading spaces, line 6) |
| `staged-ids` | `f8d01e56…65828` | `S002` |
| `reg-ids` | `cffa0c59…401806` | `S001`, `S002` |
| `collisions` | `f8d01e56…65828` | `S002` |

Indented row visible bytes (`grep -n 'S002' fixture-registry.md | cat -A`):
`6:  | S002 | indented row | docs | A | x | x | x | mined | 2026-10-25 | 180d | — |` — exactly two leading spaces before the pipe.

Reproduction (private `/tmp/r35audit25-idguard`, ran read-only against lane paths):

```
# A. column-zero-only extraction (anchored at col 0)
grep -oE '^\|[[:space:]]*S[0-9]{3,}' fixture-registry.md | grep -oE 'S[0-9]{3,}' | sort -u
→ S001            # indented S002 is MISSED

# B. maintained 0–3 leading-space extraction
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' fixture-registry.md | grep -oE 'S[0-9]{3,}' | sort -u
→ S001 S002      # indented S002 IS caught

# C. collision = extracted ∩ staged {S002}, via comm -12
#    A ∩ staged → empty (0 lines)   B ∩ staged → S002 (1 line, nonempty)
```

Fresh-vs-committed equivalence: `diff -u` of the fresh B extraction vs committed `reg-ids` → no diff; fresh `collisions` (B) vs committed `collisions` → no diff. The fresh A set differs from committed `reg-ids` exactly by the missing `S002` (the designed contrast).

Cross-check against the round-34 ancestor proof (`.ufo/waves/round-34/r34b/assimilation/guard-proof/`): `reg-ids-colzero` = `S001` only, `collisions-colzero` empty, `collisions-0to3` = `S002` — same phenomenon, recorded there with both variants; round-35 kept the 0to3 variant (committed `collisions` = `S002`). The round-35 `run-proof.log` claim ("extraction pattern accepts 0-3 leading spaces … collisions nonempty => guard works on indented rows") matches the reproduced result exactly.

Pattern provenance (read-only source reads): `scripts/sources-census.sh:40-42` documents "Maintained parser accepts 0–3 leading ASCII spaces before Markdown rows/headings; 4 or more spaces are indented code and ignored"; its selftest exercises valid indented rows at widths 0/1/2/3 (`sources-census.sh:287-316`); round-34 seat ACensusNow used the same `^ {0,3}\|` form (`r34b/w2/ACensusNow.md:111-117`).

## Observed boundary (advisory)

The frozen C1 counter's own row regex is column-zero-anchored (`tools/round-35/c1-coverage-counter.py:22-25`, `(?m)^\|\s*(S\d{3,})\s*\|`): an indented `S125`/`S129` row would fail the counter (`registry_row_missing`). The 0–3 latitude lives in the assimilation/census parser (the id guard), not in the scoring counter; the registry contract keeps data rows at column 0 (confirmed for the real `corpus/SOURCES.md` in r34 ACensusNow: "every registry row sits at column 0"). No claim impact.

## Limits

- No test suites executed (wave rules); the `sources-census.sh` contract is cited from static reads, not a selftest run.
- No writes outside this report and private `/tmp` scratch; hash values above are of the files read.
- No `find`/`du` under `/fast/scratch`; no pacman; no VCS mutation; no delegation.
