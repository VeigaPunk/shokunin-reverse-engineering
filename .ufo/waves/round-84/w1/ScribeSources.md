# ScribeSources — round84 scoped findings

Lane `kaidoku-shokunin`; round 84; L1 `KaidokuR84` integrates. Seat `ScribeSources`, wave
`r84-w1`. Declaration `e0de2088a7bddc16305357f90ac7e889fa0a0d11`; first container
`a5663ddedd157bb9113928f5fe80509d6f3fc7a1`. Frozen plan `plans/round-84-claims.md`.

## Behavior

I drafted the round-84 `corpus/SOURCES.md` delta in the registry's exact 11-column grammar, plus a
used-by change log, and I ran the maintained census against private mirrors of it. I did **not**
write `corpus/`. The delta is a draft for the L1 to land.

**Delta drafted** (`.ufo/waves/round-84/w1/ScribeSources/SOURCES-delta.md`) — two new rows,
appended at the end of the `## Registry` table; no existing row is edited, renumbered or
superseded; every cell free of literal or escaped `|`; both rows verified to carry exactly 11
fields under the census's `gawk -F'|'` split.

**S301 (admit, tier A, status mined)** — the mksquashfs(1) man page,
`https://man.archlinux.org/man/mksquashfs.1.en`. Opened 2026-11-04, HTTP 200, 57 790 B, sha256
`3ea8c1a1b429a5da35c7ffa0719ee2dade48ab8566c099c02b2c25bbe2052765`. Located quote for
`-repro-time TIME`, read at derived-text lines 168-174 of the served bytes:

> build a reproducible filesystem image. This is equivalent to specifying -mkfs-time TIME and
> -inode-time TIME, which achieves reproducibility by setting all timestamps to TIME.

(24 words, ≤ 25.) I kept the quote long enough to be specific to `-repro-time`: the neighbouring
`-repro` entry at derived-text lines 163-167 opens with the same first sentence, so a shorter
quote would not distinguish the two options. Snapshot kept at
`.ufo/waves/round-84/w1/ScribeSources/receipts/mksquashfs.1.en.html`; I confirmed it is
byte-identical (same sha256) to the L1's snapshot at `.ufo/waves/round-84/l1/sources/` and to a
fresh live refetch. The page's own footer carries `mksquashfs version 4.7.5` and `4.7.5-1`,
consistent with the plan's `mksquashfs 4.7.5` fixture toolchain.

**S302 (reject, tier A, status rejected)** — the REA npm package tarball as an authority for the
`depth-limited` gap-kind taxonomy. Opened 2026-11-04,
`https://registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz`, HTTP 200, 5 634 033 B, sha256
`531717a06e92ca651aab52691190f916fac044272c01f875e22c5e293218e699` — the same digest the
registry already records for this package. Reason: the URL is already held in five registry
scopes and the packed bytes expose no stable anchor; the gap taxonomy is reachable only by
unpacking a member path, not by addressing a locator in a served document. Flip: a published REA
documentation URL that anchors the gap-kind taxonomy.

## Gates

All gates below were executed; each result is observed, not inferred.

| gate | command | exit | finding |
|---|---|---|---|
| census validate, assignment-literal delta on the HEAD baseline | `scripts/sources-census.sh validate --file <mirror>` | **0** | no E-codes; one `W04` (the tarball URL already appears across scopes) |
| census, same file | `scripts/sources-census.sh census --file <mirror>` | 0 | rows 207 / A189 B10 C8 / mined 185 rejected 22 |
| assignment-literal delta on the **landed** tree | `validate --file <mirror>` | **1** | `E03 S301 duplicate id`, `E03 S302 duplicate id` |
| landed tree with S302/S303 swapped | `validate --file <mirror>` | 0 | no E-codes; rows 208 / A190 B10 C8 / mined 186 rejected 22 (id order becomes non-monotonic; the census does not enforce order) |
| landed tree as-is (lesson + knowledge entry now on disk) | `validate --file <LANE>/corpus/SOURCES.md` | 0 | no E-codes; rows 208 / A190 B10 C8 / mined 186 rejected 22 |
| maintained parser selftest | `scripts/sources-census.sh selftest` | 0 | 96 killed, 0 survived, last line `selftest ok`; `TMPDIR` pointed inside scratch, not `/tmp` |

**E03 / E04 findings, explicitly.** The only E-codes I observed anywhere were the two `E03`
duplicate-id findings in the third row of the table above — and they arise only from applying the
assignment's numbering on top of the rows the L1 had already landed. There were **no E04**
duplicate-URL-within-scope findings in any variant: S302's URL is already held, but in *different*
scopes, so the census reports it as the cross-scope warning `W04`, not `E04`. The only `E04`
path in the parser requires the same URL **and** the same scope with a non-superseding row, and
no such pair exists.

**Parser indentation, verified.** I inserted the two delta rows into a HEAD-baseline mirror at
each indentation width and re-ran both census and validate:

| leading spaces | rows counted | validate exit |
|---|---|---|
| 0 | 207 | 0 |
| 1 | 207 | 0 |
| 2 | 207 | 0 |
| 3 | 207 | 0 |
| 4 | 205 | 0 (rows ignored — indented code) |

So the maintained parser accepts **0-3 leading spaces** and ignores 4+, exactly as its header
documents. The maintained selftest independently exercises the same widths (36 indent-width
cases, all killed).

**Used-by audit.** The lane's forward convention is that each mined row's `used-by` path must
exist on disk and the file must literally contain the row's own id. For the two new rows: S301's
two destinations exist and cite `S301` (1 and 3 lines); S302's destination exists and cites
`S302` (4 lines). Pre-existing violations I did not touch and did not repair: S081, S246, S248
(×2), S254, S257, S259, S260, S261, S262, S263.

**One proposal withdrawn.** I had drafted an S119 `used-by` extension naming the round-84
knowledge entry. It fails the forward literal-cite audit — that entry does not contain `S119` —
so I withdrew it and left S119's cell unchanged.

## Id-binding conflict for the L1 (the one decision needed)

The frozen plan says two rows: "S301 (mksquashfs(1) `-repro-time`; mined, tier A …) and S302
(rejected: the REA npm tarball …)". My assignment says the same. **While I worked, the L1 seat
landed three rows** into the lane working tree (`corpus/SOURCES.md` lines 217-219, receipt
`.ufo/waves/round-84/l1/sources/round-84-sources.json`):

| id | landed content | vs. the assignment |
|---|---|---|
| S301 | mksquashfs(1) manual page — `docs`, A, `mined` | **matches** S301; only `source` and `scope` wording differ (all other cells byte-identical) |
| S302 | installed package file `FirmwarePublication.js:17` — `code`, A, `mined` | **not in the assignment** |
| S303 | the npm tarball rejection — `code`, A, `rejected` | the assignment's **S302** content, id shifted by one |

I verified the landed S302 independently rather than taking it on trust: the installed file and
the tarball member `package/dist/firmware/FirmwarePublication.js` are both 17 416 B with sha256
`bb4f3246bee70a5b32b048e5ef956e649626b6449b1d457454440739a8d51029`, and line 17 reads
`"depth-limited": "Rerun extract_firmware with a higher max_depth (up to 10) and a fresh output_directory to descend into this path."`. It is a genuinely distinct source (an installed file, not the tarball URL) with a line-level anchor, so it is not a duplicate.

The landed numbering is already bound into four other artifacts, so adopting the
assignment-literal numbering means editing all of them: the round-84 knowledge entry's two
`source:` lines, the lesson's Gate table and its M84-2 mistake row, the `corpus/README.md`
round-84 frontier note, and the `SKILL.md` instrument-registry row for
`tools/round-84/nested-sqfs.py`.

**Recommendation: keep the landed numbering.** The landed tree already validates at exit 0 with
no E-codes, and the landed S303 carries this seat's rejection reason and flip condition in
substance. Applying my delta literally on top of it is the only outcome that fails the census
(`E03`, exit 1). If the L1 instead renumbers so the tarball reject takes S302, the `teaches`
cross-reference must be updated too ("S302 is the anchored authority" → the id that actually
holds it) — a stale cross-reference is the failure mode the delta file calls out explicitly.

## Touched surfaces / artifacts

All paths relative to the lane. Only my own seat's wave directory was written:

- `.ufo/waves/round-84/w1/ScribeSources/SOURCES-delta.md` — the drafted delta, used-by change
  log, used-by audit, and the id-binding conflict section
- `.ufo/waves/round-84/w1/ScribeSources/receipts/receipt.json` — every command, exit code,
  digest and finding, machine-readable
- `.ufo/waves/round-84/w1/ScribeSources/receipts/mksquashfs.1.en.html` — the source snapshot
  (sha256 `3ea8c1a1…`, byte-identical to the L1's copy)
- `.ufo/waves/round-84/w1/ScribeSources.md` — this report

**No lane writes.** `corpus/SOURCES.md` was not written; its sha256 at the end of my work is
`594e0094b56f46f84591510fe6e164a890176f42f6beadd31901e8825f738459`, unchanged by this seat
(verified by re-reading it and re-running `validate`, exit 0).

## Out of scope / not done

- `corpus/SOURCES.md` was **not** edited — drafting only, per the seat spec.
- The `## Search log` line is drafted inside the delta file for the L1 to append; I did not
  append it myself.
- The `SKILL.md` instrument-registry rows for the three round-84 tools are the L1's standing
  duty; I did not write them.
- No predicate, counter, mutant table, fixture or frozen file was read for editing or changed.
  Frozen bytes I read: `tools/round-82/conjunction-gate.py`, `tools/round-82/printed-command.py`,
  `tools/round-83/source-bind.py`, `tools/round-84/freeze-precheck.py`,
  `tools/round-84/mutation-closure.py`, `tools/round-84/nested-sqfs.py`,
  `.ufo/waves/round-84/mutants.json`, `.ufo/waves/round-84/claims.json`,
  `plans/round-84-claims.md`.
- No git or jj mutation: read-only `git show`, `git diff`, `git status`, `git log` only. No
  commit, push, publish or deploy. No `task` spawn, no `agent://all`.
- No build, test, linter or formatter was run beyond the census's own `--file` modes and its
  `selftest`. No product code was touched.
- No tool was installed or upgraded: `scripts/sources-census.sh` and `gawk` were already present
  and sufficient. (Tooling authorization read at `/home/vgpnk/.omp/agent/RULES.md`; nothing
  needed installing, so there is no tool/version/channel/reason record to report.)
- Scratch was confined to `/fast/scratch/hyaku/kaidoku-r84/ScribeSources/`, the receipts were
  copied into the wave directory, and the scratch directory was removed before this report.

## Findings

1. **The census is clean on the delta as drafted.** Assignment-literal delta on the HEAD
   baseline: `validate` exit 0, no E-codes, one expected `W04`. The only E-codes seen anywhere
   were the two `E03`s caused by applying that numbering on top of rows already landed.
2. **No E04 anywhere.** The tarball URL is held in five other scopes, not the same scope, so the
   duplicate-URL finding is the cross-scope `W04` warning, never `E04`. The rejection reason and
   the five-scope claim are both accurate as written.
3. **The parser accepts 0-3 leading spaces** (0-3 → 207 rows counted; 4 → 205, ignored), with
   the maintained selftest passing 96/96.
4. **The id binding in the lane working tree differs from the plan and from my assignment.** The
   landed tree binds S302 to an installed package file the plan did not name and pushes the
   tarball rejection to S303. Four other artifacts already cite those ids. Recommendation to the
   L1: keep the landed numbering; it validates at exit 0 and needs no cross-artifact edits.
5. **The used-by cells of the new rows satisfy the lane's forward literal-cite audit**, and an
   S119 extension I initially drafted would not have — it is withdrawn, not silently dropped.
6. **Pre-existing forward-audit violations** in eleven mined rows (S081, S246, S248 ×2, S254,
   S257, S259-S263) are reported for the L1's disclosure sweep; this seat did not repair them,
   since they are outside the round-84 delta.
7. **The source evidence is independently reproducible.** The mksquashfs snapshot matches the
   L1's copy and a fresh refetch byte-for-byte; the tarball digest matches what the registry
   already records; the installed `FirmwarePublication.js` and the tarball member are
   byte-identical, so the landed S302's anchor is real and not merely asserted.

## Self-assessment

Axes named: source fidelity, registry-grammar conformance, census verifiability, conflict
transparency, scope discipline.

- Source fidelity 5/5 — every quote, digest, byte count, line range and anchor in the delta was
  read from the served bytes in this session and re-verified; the S302 anchor was checked
  against both the installed copy and the tarball member.
- Registry-grammar conformance 5/5 — 11 fields per row, no literal or escaped pipe in any cell,
  verified mechanically; the delta validates at exit 0.
- Census verifiability 5/5 — six measured variants plus the maintained selftest, all exits and
  E/W codes recorded in the receipt.
- Conflict transparency 5/5 — the id-binding conflict is reported verbatim, with the landed
  rows quoted cell-for-cell and the four dependent artifacts named; the recommendation is given
  but the decision is left to the L1.
- Scope discipline 5/5 — no lane writes, no production edits, no git mutation, no spawns, no
  installs; scratch removed.

Overall 5.0/5. The remaining risk is entirely in the L1's hands: whether to keep the landed
S301/S302/S303 numbering (recommended) or renumber to the plan's two-row binding, which would
require coordinated edits to four artifacts that already cite those ids.
