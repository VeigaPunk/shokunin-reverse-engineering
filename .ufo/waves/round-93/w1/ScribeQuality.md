# ScribeQuality — round 93, seat report

Lane `kaidoku`, round 93, wave `r93-w1`, seat `ScribeQuality` (scribe).
Scope: validate and refine the L1's draft corpus material against the house gates.

## What this seat did

Validated the three L1 drafts named in the seat spec, re-derived every frozen
counter and gate against the lane's committed bytes, attacked the drafts with
the house's own instruments, and delivered refined versions of all three plus
the two skeletons the seat spec asked for.

**Axis walk.** The frontier moved on two surfaces: (a) the QUALITY-93 /
SOURCES `teaches`-cell rule for a `supersedes` row, and (b) the caller map of
`PackUnix::unpackExtent` at UPX 5.2.0. Both are load-bearing for R93-C2's
candidate and both are inside the drafts the L1 landed.

## Evidence — every command run, with exit codes

Scratch `S=${HYAKU_SCRATCH:-/fast/scratch/hyaku}/kaidoku-r93/ScribeQuality`.
Every counter ran in a clone of the lane at a named revision, with
`TMPDIR="$S/tmp"` and `--work "$S/work"` where the tool accepts it. Clones:
`$S/clone` (declaration `92a2405`), `$S/cloneA` (drafts as given), `$S/cloneB`
(my first refinement), `$S/cloneC` (L1's landed working tree), `$S/cloneH`
(L1's HEAD), `$S/cloneD` (my delivered refinement). No lane file was created,
edited, or deleted; `git status --porcelain` in the lane shows only
`?? .ufo/waves/round-93/l1/scores/` and `?? .ufo/waves/round-93/w1/ScribeQuality/`
(plus the L1's own untracked wave artefacts), and `git log --oneline` is
unchanged by this seat.

### Frozen counter, R93-C2 (`tools/round-93/craft-citation-semantic.py`)

| run | command | exit | result |
|---|---|---|---|
| selftest | `python3 -I -B tools/round-93/craft-citation-semantic.py --selftest --work $S/work/selftest-c2` | 0 | `SELFTEST cases=10 failures=0` |
| before-manifest @ base | `... --manifest .ufo/waves/round-93/manifests/block31-before.json --block 31 --rev 0a2a23da5eb50410a8a0df90c031d9f4fdadb024 --json-out $S/work/before-at-base.json` | 1 | `row 'intact input refused by mistake': QUALITY 169 lacks ['never refuse an intact input', "packer's verdict"]` — reproduces the frozen pre-receipt atom |
| after-manifest @ L1 HEAD | `... --manifest .ufo/waves/round-93/manifests/block32-after.json --block 32 --rev HEAD --json-out $S/work/H-after.json` | 0 | `ok` |
| before-manifest @ L1 HEAD | `... --manifest .ufo/waves/round-93/manifests/block31-before.json --block 31 --rev HEAD --json-out $S/work/H-before.json` | 1 | same named atom — block 31 stays history |
| after-manifest @ my refinement | `... --manifest .../block32-after.json --block 32 --worktree --json-out $S/work/D-after.json` (cloneD) | 0 | `ok` |
| before-manifest @ my refinement | `... --manifest .../block31-before.json --block 31 --worktree --json-out $S/work/D-before.json` (cloneD) | 1 | same named atom |

Counter sha256 re-derived: `sha256sum tools/round-93/craft-citation-semantic.py`
→ `34cf6579d7d0614336add1710912877492c68517331736fa5e4021ffedf05340`, equal to
the pin in `.ufo/waves/round-93/claims.json` (`counter_sha256`).

### Depth-regression counters (the R93-C2 "no depth regression" target)

| run | command | exit | label |
|---|---|---|---|
| v2 @ base | `python3 -I -B tools/round-89/depth-blocks-v2.py --root . --rev 92a240521bd1bf2213b75d18d9b176a8dafdc67c --expect-blocks 31 --json-out $S/work/d2-base.json` | 0 | `blocks 31 resolved 31 expect 31 unresolved 0 met=True` |
| v3 @ base | `python3 -I -B tools/round-91/depth-blocks-v3.py --root . --rev 92a240521bd1bf2213b75d18d9b176a8dafdc67c --expect-blocks 31 --json-out $S/work/d3-base.json` | 0 | `blocks 31, resolved 31` |
| **v2 @ L1's drafts as given** | `... --root . --worktree --expect-blocks 32 --json-out $S/work/A-d2.json` (cloneA) | **1** | `blocks 32 resolved 31 expect 32 unresolved 1 met=False` — the draft as given **failed** the depth target |
| v3 @ L1's drafts as given | `... --root . --worktree --expect-blocks 32 --json-out $S/work/A-d3.json` (cloneA) | 1 | `blocks 32, resolved 31, required-shaped 2/2 expect 32 unresolved 1 met=False` |
| v2 @ L1 HEAD | `... --root . --rev HEAD --expect-blocks 32 --json-out $S/work/H-d2.json` | 0 | `blocks 32 resolved 32 expect 32 unresolved 0 met=True` |
| v3 @ L1 HEAD | `... --root . --rev HEAD --expect-blocks 32 --json-out $S/work/H-d3.json` | 0 | `blocks 32, resolved 32, required-shaped 2/2 expect 32 shaped_required 2/2 unresolved 0 met=True` |
| v2 @ my refinement | `... --root . --worktree --expect-blocks 32 --json-out $S/work/D-d2.json` (cloneD) | 0 | `blocks 32 resolved 32 expect 32 unresolved 0 met=True` |
| v3 @ my refinement | `... --root . --worktree --expect-blocks 32 --json-out $S/work/D-d3.json` (cloneD) | 0 | `blocks 32, resolved 32, required-shaped 2/2 expect 32 shaped_required 2/2 unresolved 0 met=True` |

The failure in cloneA is **finding 1** below; the L1 fixed it in its own
landed block 32 before this seat's second pass, and my delivered block 32
keeps the fix.

### SOURCES census (`scripts/sources-census.sh`)

| run | command | exit | result |
|---|---|---|---|
| lane's own before-census | `cat .ufo/waves/round-93/census-before.txt` | — | 30 `W04` lines + `kaidoku ok` + `census-exit=0` |
| L1 HEAD SOURCES | `scripts/sources-census.sh validate --file $S/cloneH/corpus/SOURCES.md --today 2026-11-05` | 0 | `file ok`, 31 `W04` (one new: S318 duplicate URL across scopes), 223 rows |
| my refined SOURCES | `scripts/sources-census.sh validate --file $S/cloneD/corpus/SOURCES.md --today 2026-11-05` | 0 | `file ok`, 31 `W04`, 223 rows |
| E04 negative control (finding 2) | a duplicate-URL+scope row `S900` whose `teaches` does **not** open `supersedes` | 1 | `E04 S900 duplicate url … within scope …` — the census's `E04` exemption reads the **`teaches`** cell only |
| E04 positive control | the same duplicate `S901` whose `teaches` **does** open `supersedes S318 —` | 0 | no `E04` — the exemption is real and is keyed on `teaches` |

### Registry immutability (SOURCES append-only, CORPUS rule 2)

A python re-derivation over `git show 92a2405:corpus/SOURCES.md` vs the landed
tree, comparing every row's eleven columns by name: only `S271 used-by` and
`S317 used-by` changed (both in the allowed set `status|recheck|used-by`),
one new row `S318`, row order preserved. `tools/round-38/registry-immutable.sh`
was not usable as a CLI here (`line 101: $1: unbound variable` when invoked
with no arguments), so the same atoms were re-derived directly; that script's
own column map (`2 id, 3 source, 4 kind, 5 tier, 6 scope, 7 anchor, 8 teaches,
9 status, 10 opened, 11 recheck, 12 used-by`, only `9`, `11`, `12` mutable) is
what the check applied.

### Source bytes fetched and re-derived (for the S318 scope and the anchor)

Fetched with `curl -fsSL` from `raw.githubusercontent.com/upx/upx/v5.2.0/src/`
(2026-11-05), sizes and sha256 as recorded:

| file | bytes | sha256 | verified |
|---|---|---|---|
| `p_unix.cpp` | 24181 | `bf83c4133c27d39433db63bf604daf577d429d734c542d29c0b9cc8ed229642e` | matches S313's anchor |
| `p_lx_elf.cpp` | 373743 | `551fc8675a59493793f59b64eb8bb9cc208a34f701ccd2bda8c9aaafb228d2dc` | matches S317's anchor |
| `p_lx_interp.cpp` | — | `d42652569dca6a2f3ff816348d5537539ce6a1a431e806b9179dd42cb2388548` | new, recorded in the refined row |
| `p_mach.cpp` | — | `348edf8ec350bb797d965619344f0137249d5e3bacf724f35f1a1bc931624c15` | new, recorded in the refined row |

`grep -n unpackExtent` over the whole upstream `src/` tree (all 257 `.cpp`/`.h`
files listed by the `v5.2.0` git tree, fetched and grepped): the only files
containing the token are `p_unix.cpp` (the definition at 476, plus the
declaration in `p_unix.h:86`), `p_lx_elf.cpp`, `p_lx_interp.cpp` and
`p_mach.cpp`. Call sites: `p_lx_elf.cpp` at 7102, 7181, 7305, 7381, 7902, 7907,
8051, 9149, 9154, 9296 (ten); `p_lx_interp.cpp` at 258, 263, 272, 278 (four);
`p_mach.cpp` at 1576, 1624 (two). `p_unix.cpp` line 496 and line 681 are the
two block-size bound sites (`sz_cpr > sz_unc` / `sz_unc > blocksize`).
Enclosing functions re-derived by scanning backwards for the defining
signature: `p_lx_elf.cpp` 7102/7181 are in `PackLinuxElf64::un_shlib_1`,
7305/7381 in `PackLinuxElf32x86interp`/`un_shlib_1`, 7902/7907/8051 in
`PackLinuxElf64::unpack`, 9149/9154/9296 in `PackLinuxElf32::unpack`;
`p_lx_interp.cpp` 258–278 are in `PackLinuxElf32x86interp::unpack`;
`p_mach.cpp` 1576/1624 in `PackMachBase<T>::unpack`. Class chain re-derived
from the upstream headers: `PackLinuxElf32x86interp : PackLinuxElf32x86`,
`PackLinuxElf32x86 : PackLinuxElf32Le : PackLinuxElf32 : PackLinuxElf :
PackUnix`; `PackMachBase : PackUnix`; `PackLinuxI386 : PackUnixLe32` and
`PackBSDI386 : PackLinuxI386` carry no `unpack` override, so
`PackUnix::unpack` (with its own bound at 681) is what the plain-unix
carriers reach.

### Pointer resolvability (every path in the delivered drafts, at the revision named)

`git cat-file -e <rev>:<path>` for each, at base `0a2a23da` / declaration
`92a2405` / HEAD:

| path | base | declaration | HEAD |
|---|---|---|---|
| `.ufo/waves/round-93/pre/r93-c2-block31-before.json` | MISS | OK | OK |
| `tools/round-93/craft-citation-semantic.py` | MISS | OK | OK |
| `corpus/lessons/round-93.md` | MISS | MISS | OK |
| `corpus/knowledge/2026-11-05-r93-citation-semantics.md` | MISS | MISS | OK |
| `corpus/knowledge/2026-11-05-r93-fresh-pack-oracle.md` | MISS | MISS | OK |
| `corpus/lessons/round-91-verifier-spotcheck.md` | OK | OK | OK |
| `corpus/QUALITY.md` | OK | OK | OK |
| `SKILL.md` | OK | OK | OK |

This table is the source of **finding 3**.

## Findings

### Finding 1 — the L1's block-32 draft, as given, failed the R93-C2 depth target (fixed by the L1 before this seat's second pass; kept fixed in my delivery)

`tools/round-89/depth-blocks-v2.py` and `tools/round-91/depth-blocks-v3.py`
resolve a block's citations through the pattern
`corpus/knowledge/([a-z0-9-]+\.md)(?::(\d+)(?:-(\d+))?)?` — i.e. **only**
`corpus/knowledge/` paths count, and the cited line range must be inside the
file. The L1's `block32-draft.md` as handed to this seat cited only
`corpus/QUALITY.md` rows, `corpus/lessons/round-92-verifier-spotcheck.md:96-100`
and `tools/round-93/craft-citation-semantic.py`. None of those is a
`corpus/knowledge/` path, so the block resolved to nothing and the counter
reported `no-citation` (cloneA, exit 1, `blocks 32 resolved 31`, `met=False`).

Two further problems in that draft's refs line, both now corrected:
`corpus/lessons/round-92-verifier-spotcheck.md` has **75 lines**, so the cited
range `96-100` is out of file; and the D-91-3 statement it points at is not in
that file's §5 at all (that file's §5 is "Trend verdicts (verified)", which
does not mention D-91-3 — `grep -c 'D-91-3'` over lines 62–67 returns 0). The
D-91-3 item lives in `corpus/lessons/round-91-verifier-spotcheck.md:169`, and
in the round-92 file at `:45` and `:74`.

The L1's landed block 32 fixed this on its own (it cites
`corpus/knowledge/2026-11-05-r93-citation-semantics.md`), and at HEAD both
depth counters are green. My delivered block 32 keeps a `corpus/knowledge/`
citation and points the D-91-3 statement at `corpus/lessons/round-91-verifier-spotcheck.md:169`.

### Finding 2 — S318 puts `supersedes S313 —` in the **`scope`** cell; QUALITY 93 and the census both key on the **`teaches`** cell

Landed row `S318` (`corpus/SOURCES.md:234`) opens its **scope** cell with
`supersedes S313 — …` and leaves its **teaches** cell as
`Cite the call site before citing the loop: …`. Every other `supersedes` row
in the registry — all sixteen of them, S033, S054, S057, S062, S063, S069,
S070, S072, S147, S148, S246, S247, S248, S271, S300, S305 — puts the marker
in **column 7, `teaches`**; S318 is the only one in column 5, `scope`.

This is a house-rule defect with a measured consequence, not a style nit:

- **QUALITY 93** (`corpus/QUALITY.md:101`) requires that a routed registry
  defect "is closed by a new row whose `teaches` opens `supersedes S0NN —` and
  names the defect". S318's `teaches` cell opens with neither.
- **`scripts/sources-census.sh` reads only `teaches`** for its `E04`
  duplicate-URL-within-scope exemption (`teaches !~ /supersedes S[0-9]{3}/`).
  Proven with two fixtures over the same duplicate-URL+scope pair: a row whose
  `teaches` lacks the marker gets `E04` (exit 1); a row whose `teaches` opens
  `supersedes S318 —` is exempt (exit 0). So S318 as landed carries **no
  `E04` exemption of its own** — any later row reusing its URL+scope hits
  `E04` unless it independently opens `supersedes S318 —`.

My delivered `s318-draft.refined.md` moves the marker into `teaches` (opening
with `supersedes S313 — S313's scope said …`, which also names the defect as
QUALITY 93 requires) and reduces `scope` to what the source covers.

### Finding 3 — Row 188 cites a receipt "at base" that is not a blob at base

Landed `Row 188` (`corpus/QUALITY.md:319`) reads: "before-receipt
`.ufo/waves/round-93/pre/r93-c2-block31-before.json` (exit 1, the named atom)
at base `0a2a23da5eb50410a8a0df90c031d9f4fdadb024`". The receipt's own
`revision` field is indeed base, but the **blob** was committed at the
declaration `92a240521bd1bf2213b75d18d9b176a8dafdc67c`, and
`git cat-file -e 0a2a23da…:.ufo/waves/round-93/pre/r93-c2-block31-before.json`
fails. The same row cites `tools/round-93/craft-citation-semantic.py` without
naming the revision it is pinned at, and `corpus/lessons/round-93.md` (M93-a),
which is a HEAD-only file — a reader following the pointer at the base
revision finds nothing. This is the round-91 D-5 / QUALITY 181 class (a
pointer must resolve at the revision it names), pointed at by the round's own
new rule.

My delivered `row188-draft.refined.md` keeps the same evidence and names both
revisions: the receipt's own `revision` field is base `0a2a23da…`, its blob is
committed at declaration `92a2405…`, the checker is pinned at the declaration
`sha256 34cf6579…`, and the lesson is marked "written this round". Every path
in the delivered row resolves at the revision it now names (table above).

### Finding 4 — the landed S318 scope under-states the caller map, and lesson M93-b repeats the understatement

Landed S318's scope says `unpackExtent` "is the consumer the ELF families reach
through `p_lx_elf.cpp`", and its anchor cell lists only
`p_lx_elf.cpp` (ten sites). The upstream tree says more: `p_lx_interp.cpp`
(four sites, `PackLinuxElf32x86interp::unpack` — an ELF family, since
`PackLinuxElf32x86interp : PackLinuxElf32x86 : PackLinuxElf32Le : PackLinuxElf32
: PackLinuxElf : PackUnix`) and `p_mach.cpp` (two sites,
`PackMachBase<T>::unpack`, `PackMachBase : PackUnix`) also call it.

This matters because the whole point of S318 is to replace S313's over-broad
"every executable carrier's unpack path" wording with a per-family statement.
A scope that says "the ELF families reach it through `p_lx_elf.cpp`" and omits
the ELF-interpreter family (whose file is `p_lx_interp.cpp`) and Mach-O
re-introduces the same defect one level down: a reader is told the ELF
families reach the loop through one file when one of them does not.

`corpus/lessons/round-93.md` M93-b makes the same understatement ("called
only from `p_lx_elf.cpp` (callers at :7181, :7381, :7902, :7907, :8051,
:9149, :9154, :9296)") — that list is also eight sites against the file's
ten (it omits 7102 and 7305, the two `un_shlib_1` header reads). The lesson is
in the lane's corpus and is not this seat's to edit.

My delivered `s318-draft.refined.md` states the caller map as the bytes give
it, names all three consumer files with their sha256s and line numbers, and
keeps `PackUnix::unpack`'s own bound at 681 as the plain-unix carriers' path.

### Finding 5 — Row 188's manifest keyword `semantic atom` lives only on a continuation line

The after-manifest pins the keyword `semantic atom` for the `citation resolves
but mis-states` row. The landed Row 188 satisfies it only through line 320, an
indented continuation of the bullet, not through the row's own line 319. The
counter's `_quality_row` reads from `- **Row 188 (` up to the next
`- **Row N (` or `## ` heading, so the continuation line is inside the row's
text and the manifest passes — this is a formatting fragility, not a failure.
The ten continuation lines in `corpus/QUALITY.md` are all in the
`## Corrections appended — round 20 wave 2` section; the Admission-criteria
rows are single-line. Reported, not changed: the landed row passes, and
restructuring it would risk the frozen keyword.

## What was delivered

All under `.ufo/waves/round-93/w1/ScribeQuality/deliverables/`:

| file | what it is |
|---|---|
| `row188-draft.refined.md` | QUALITY row 188, revised: the receipt, checker and lesson pointers now name the revision at which each resolves (finding 3) |
| `block32-draft.refined.md` | craft block 32, revised: keeps the `corpus/knowledge/` citation the depth counters need and points D-91-3 at `corpus/lessons/round-91-verifier-spotcheck.md:169` (finding 1) |
| `s318-draft.refined.md` | SOURCES row S318, revised: `supersedes S313 —` moved from `scope` to `teaches` (finding 2); the scope and anchor state the full caller map (finding 4) |
| `log-round-93-entry.skeleton.md` | the LOG.md round-93 entry skeleton, mirroring round 92's shape: motive, declaration `92a240521bd1bf2213b75d18d9b176a8dafdc67c`, measured/candidate placeholders, sources and frontier, quality rows, wave seats, named limits. Placeholders stay literal |
| `lesson-gate-table.skeleton.md` | the lesson Gate table skeleton: the sources table (row, URL, access date, HTTP/size/sha256, located quote ≤25 words, used for), the admit/reject rows, the row-changes paragraph, assimilation, the census before/after placeholders, and the spot-check line. Placeholders stay literal |

The three refined drafts were validated together in cloneD (lane bytes at HEAD
with the three deliverables applied): after-manifest exit 0, before-manifest
exit 1 with the frozen atom, depth v2 `blocks 32 resolved 32` met, depth v3
`blocks 32, resolved 32, required-shaped 2/2` met, census `ok` exit 0 with 31
`W04` and 223 rows.

## Gates and house rules checked

- Row 188: bullet format `- **Row 188 (title).**` ✓; zero `|` characters ✓;
  names the lesson that produced it (`corpus/lessons/round-93.md`, M93-a) ✓;
  every evidence pointer resolvable at the revision it names (after the
  finding-3 fix) ✓.
- Block 32: decision-table shape — header + separator + 4 body rows of 4 cells
  ✓; v2 floor 406 words ≥ 25 and 18 backticked spans ≥ 2 ✓; the marker
  `stop-boundary-supersedes-citation v1` present exactly once ✓; no `|` in any
  cell ✓; the four criterion cells end with `QUALITY 176` / `178` / `184` /
  `188`, one `QUALITY <N>` each ✓; the frozen after-manifest parses it and
  exits 0 ✓.
- S318: 11 columns (`awk -F'|' NF==13`) ✓; no literal or escaped `|` inside
  any cell ✓; `supersedes S313 —` opens the `teaches` cell ✓ (revised);
  status `mined` ✓; ISO opened date `2026-11-05` ✓; recheck `on-release` ✓;
  used-by names `corpus/knowledge/2026-11-05-r93-fresh-pack-oracle.md` ✓.
- SOURCES append-only: only `status`, `recheck`, `used-by` changed on
  existing rows; one new row; order preserved ✓.
- Registry marker placement: `supersedes` in the `teaches` cell, per QUALITY 93
  and the census `E04` exemption ✓ (revised).

## Out of scope for this seat

- R93-C1's fresh-pack battery, its forgeries, and the frozen label — owned by
  the executor and reviewer seats; this seat did not score them.
- The L1's own commits `2d4c89f9b` and `ca5aa6a2c`, and the lane's
  `corpus/lessons/round-93.md` M93-b wording — lane files, not this seat's to
  edit; reported in finding 4.
- The non-author closure (`corpus/lessons/round-93-verifier-spotcheck.md`).

## Known limits of this report

- The upstream caller map was re-derived from `v5.2.0` source fetched on
  2026-11-05; it is a statement about that tag, not about UPX master.
- The census `E04` fixtures were built by adding rows to a **copy** of
  `corpus/SOURCES.md` under scratch; the lane's registry was never modified.
- `tools/round-38/registry-immutable.sh` could not be run as a CLI here (it
  requires three positional arguments and aborts with `$1: unbound variable`
  when given none), so the append-only atoms were re-derived directly against
  that script's own column map. The equivalent check was not exercised
  through the script's own exit code.
- No tool was installed or upgraded by this seat; none was needed.
