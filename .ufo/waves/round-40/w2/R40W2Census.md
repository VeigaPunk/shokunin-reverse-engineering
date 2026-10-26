# R40W2Census — SOURCES registry / census / registry-immutability attack

**Verdict: CONFIRMED** — the SOURCES surface of the round-40 landing (S123–S126 appends, used-by-only edits to six base rows, census validity, registry append-only discipline between `fa6a8a3f` and `4d62ee5a`) held under every check I ran; no defect found.

Attacked: (a) the census `validate` gate on the lane at the dispatch tip; (b) the round-38 registry-immutability gate between base `fa6a8a3f85ec65946b3a54d37c0ddd1d6748664f` and dispatch tip `4d62ee5a86b4692a13f682b29ed7975e8d7e5326`; (c) the claim that SOURCES.md changed only by appends S123–S126 and used-by cells; (d) recheck-cell census validity and pipe-free cells of every new row; (e) the census-warning delta against `.ufo/waves/round-40/census-start.txt`.

## 1. Census validate (lane, working tree = dispatch tip)

Command: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku`

Output (abridged to the warning block; full copy in artifacts):

```
kaidoku	W04	S033 duplicate url github.com/NationalSecurityAgency/ghidra/pull/9348 across scopes
kaidoku	W04	S047 duplicate url go.dev/dl/?mode=json&include=all`, across scopes
kaidoku	W04	S054 duplicate url developer.android.com/ndk/guides/abis across scopes
kaidoku	W04	S062 duplicate url raw.githubusercontent.com/sigrokproject/sigrok-cli/sigrok-cli-0.7.2/doc/sigrok-cli.1 across scopes
kaidoku	W04	S069 duplicate url www.wireshark.org/docs/man-pages/tshark.html across scopes
kaidoku	W04	S083 duplicate url registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz across scopes
kaidoku	W04	S090 duplicate url registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz across scopes
kaidoku	W04	S092 duplicate url registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz across scopes
kaidoku	W04	S102 duplicate url learn.microsoft.com/en-us/windows/win32/debug/pe-format across scopes
kaidoku	W04	S112 duplicate url raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/handlers/filesystem/squashfs.py across scopes
kaidoku	W04	S117 duplicate url raw.githubusercontent.com/onekey-sec/unblob/26.6.4/README.md across scopes
kaidoku	W04	S119 duplicate url registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz across scopes
kaidoku	W04	S123 duplicate url registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz across scopes
kaidoku	ok	/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md
```

`CENSUS_VALIDATE_EXIT=0`. No E01–E12 anywhere; 13 W04 warnings (W-codes never change status per the script header). Working tree = HEAD for SOURCES.md (`git status --porcelain` clean; `cmp` of `HEAD:corpus/SOURCES.md` vs worktree equal), and no commit after `4d62ee5a` touches SOURCES.md (`git log 4d62ee5a..HEAD -- corpus/SOURCES.md` empty; HEAD `0b15c8b2`), so this run is the dispatch-tip census.

## 2. Registry-immutability gate (base → dispatch tip)

Usage read first (header of `tools/round-38/registry-immutable.sh`): run mode `registry-immutable.sh LANE BASE REV` — for every registry row present at BASE only status/recheck/used-by may differ at REV; prints offending rows (id, columns) and exits 1; this copy additionally detects base-row deletion and reordering, and has `--selftest`.

Command: `bash /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-38/registry-immutable.sh /home/vgpnk/Projects/shokunin/kaidoku-shokunin fa6a8a3f85ec65946b3a54d37c0ddd1d6748664f 4d62ee5a86b4692a13f682b29ed7975e8d7e5326` → no output, `REGISTRY_IMMUTABLE_EXIT=0`.

Selftest: `SELFTEST cases=5 pass=5 fail=0`, exit 0 (append-only 0, in-place cell 1, row deletion 1, reorder 1, allowed-cells 0) — the gate itself is trustworthy.

## 3. SOURCES.md delta decomposition (base → dispatch tip)

`git log fa6a8a3f..4d62ee5a -- corpus/SOURCES.md` → exactly two commits: `7fce3086` (freeze) and `42c10a58` (landing). Diffstat 10 insertions / 6 deletions, single hunk around lines 115–131.

- **Row counts**: 122 registry rows at base → 126 at dispatch.
- **Appends**: id-set diff gives exactly `S123 S124 S125 S126` added, **zero deletions**.
- **Per-commit attribution**: `7fce3086` adds S123 and touches no existing row; `42c10a58` rewrites S112, S114, S118, S119, S120, S121 and appends S124–S126.
- **Rewritten rows are used-by-only**: strict all-column comparison (no exclusions — stricter than the gate, which tolerates status/recheck too) shows each of the six differs **only in column 12**: `S112…S121 differs in cols: 12` (six lines, nothing else).
- **Used-by delta** (normalized, trimmed entries): additions only, no removals —
  - S112 += `corpus/knowledge/2026-10-26-r40-avm-be-squashfs-core.md`, `corpus/knowledge/2026-10-26-r40-sqfs-triage-v2.md`
  - S114 += `…r40-avm-be-squashfs-core.md`
  - S118, S119, S120 += `…r40-sqfs-triage-v2.md`
  - S121 += `…r40-avm-be-squashfs-core.md`
- **Reciprocity**: the core entry cites S112, S114, S121, S124, S125, S126; the triage entry cites S112, S118, S119, S120, S123 — exactly the rows whose used-by cells list each entry. Every used-by addition is reciprocated by a citation in the entry, and both entries' cited rows exist (E11 clean). The C1 predicate's "SOURCES row absent at the base whose used-by lists it" is satisfied by S124 (also S125, S126).

## 4. New rows S123–S126: structure and recheck validity

All four rows parse at `NF=13` with `awk -F'|'` — **no cell carries a pipe** (an embedded pipe would force NF≠13 → E01; the whole-tree validate is E01-clean, and all 122 base rows are also NF=13). Extracted cells:

| id | status | opened | recheck | used-by |
|---|---|---|---|---|
| S123 | mined | 2026-10-26 | `180d` | corpus/knowledge/2026-10-26-r40-sqfs-triage-v2.md |
| S124 | mined | 2026-10-26 | `180d` | corpus/knowledge/2026-10-26-r40-avm-be-squashfs-core.md |
| S125 | mined | 2026-10-26 | `on-release` | corpus/knowledge/2026-10-26-r40-avm-be-squashfs-core.md |
| S126 | mined | 2026-10-26 | `180d` | corpus/knowledge/2026-10-26-r40-avm-be-squashfs-core.md |

Recheck cells are census-valid per E09 (`NNd` cadence or symbolic cadence; `180d` due 2027-04-25, not due; `on-release` symbolic, reported never judged). Status/opened pass E07/E08. Used-by paths exist on disk (E11 clean in the lane run).

## 5. Census warnings vs `.ufo/waves/round-40/census-start.txt`

- **Base fidelity**: sandbox clone at `fa6a8a3f` (shared clone, `git rev-parse --show-toplevel` asserted = clone dir before checkout), `sources-census.sh validate <clone>` → **exit 0**, and its warning block is byte-identical to `census-start.txt` after normalizing the `ok` line's path. So `census-start.txt` is a faithful snapshot of the base revision: same 12 W04 warnings, exit 0.
- **Delta at dispatch tip**: exactly one added warning line, `kaidoku W04 S123 duplicate url registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz across scopes`; no warning disappeared, no existing row drifted. The S123 W04 is a new-row artifact: S123 deliberately re-uses the rea-agents 6.5.0 tgz URL in a different scope (the row itself discloses "equal to S119/S080"); W04 is a warning, not an error, and E04 (duplicate URL+scope) does not fire because the scopes differ.

## Advisory notes (not defects)

1. **`--file` mode E11 artifact**: running `validate --file <copy of base SOURCES.md>` from a scratch path floods E11 ("missing used-by") because `resolve_targets` anchors used-by resolution at `dirname(file)/..` — for a copy not placed as `<root>/corpus/SOURCES.md` every relative used-by path misses. I reproduced this even from the lane cwd. Anyone re-checking a historical SOURCES.md must use a full sandbox checkout (as in §5), not a bare `--file` copy; otherwise they will misread ~207 phantom E11s as lane defects.
2. S123's W04 duplicate-URL warning is new since round start (see §5). If the fleet wants a zero-W04 lane, S123 would need a distinct URL or a supersedes link — out of my seat's authority to change; the claims do not require it.

## Tooling record

No tools installed or upgraded (nothing needed beyond the preinstalled census script, git, gawk, coreutils). No pacman transactions. Scratch `/fast/scratch/hyaku/kaidoku-r40/R40W2Census` (incl. one throwaway clone) removed after the run; cited outputs copied to the artifacts dir. No VCS mutation in the lane or fleet; the only checkout was inside the asserted sandbox clone.

## Evidence artifacts

All under `.ufo/waves/round-40/w2/artifacts/R40W2Census/`:
`census-validate-now.txt`, `census-validate-base-clone.txt`, `census-vs-census-start.txt`, `registry-immutable-base-dispatch.txt`, `registry-immutable-selftest.txt`, `sources-diff-base-dispatch.patch`, `sources-diff-freeze-7fce3086.patch`, `sources-diff-landing-42c10a58.patch`, `new-rows-structure.txt`, `usedby-delta.txt`.

## Limits

- I verified the registry/census surface only; I did not re-run the C1/C2 counters or audit receipt contents (other seats).
- The census `validate` checks format/enum/path existence, not the truth of cell prose; anchor claims inside S123–S126 cells were not re-fetched (out of seat scope).
- [INFERENCE] The S123 W04 warning is "expected" in the sense that the row discloses the URL reuse and no rule forbids cross-scope duplicates; the judgment that this is acceptable is mine, not a rule citation.
