# R38ExecIdCollision — assimilation id-collision check (kaidoku round 38, wave 1)

Seat `R38ExecIdCollision`, executor, leaf. Advisory only: no lane file was changed except this
report and the artifacts named below; no VCS mutation; no REA/campaign tool was run in
`shokuknow`; nothing was installed.

- Lane root: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, HEAD `cb4326b2aa4c2024af0651fe6115b82d0c4de3df` (read, unmodified).
- Registry read: `corpus/SOURCES.md`, sha256 `5a4c1c8c3ed0a5fd01e03bc57e93b00a563b35f8e5dc791e966e4f4251b92ef6`.
- Staged read (shokuknow, read-only): `merge/kaidoku/SOURCES.append.md`, sha256 `b82d1276d837867d3a39f56e57a255249802b9d0665b230f1bc87c9424510449`.
- Host time at measurement: 2026-10-26T03:22:01-03:00.

## Axes worked

- **coverage** — the check is the append guard for C1's sourced claim: a registry append that
  reuses `S106`–`S111` would bind the new entry's citations to six unrelated documents
  (binutils `readelf`, the sasquatch release tag, the unblob handler, the neovim release, the
  unblob README, the devttys0 README). The measurement is the gate, so this seat lands the
  collision set and the renumber-by-document map before any append.
- **calibration** — the package's own stated premise ("registry holds 105 rows; first staged id
  is S106") is measured against the registry as it stands (111 rows) and shown stale, with the
  two commits that moved it.

## Command run (verbatim, as assigned)

```
A=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-38/assimilation; mkdir -p "$A"
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' /home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort > "$A/reg-ids"
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' /home/vgpnk/Projects/shokuknow/merge/kaidoku/SOURCES.append.md | grep -oE 'S[0-9]+' | sort > "$A/staged-ids"
comm -12 "$A/reg-ids" "$A/staged-ids" > "$A/collisions"
```

Exit status: all four stages 0 (`grep`/`sort`/`comm` all return 0 here; `comm` returns 0 even
when the intersection is empty, so the non-empty `collisions` file — not an exit code — is the
signal).

## Result: both id lists and the collision count

| list | rows | range | contiguous | sha256 |
|---|---|---|---|---|
| `assimilation/reg-ids` (registry `corpus/SOURCES.md`) | 111 | `S001`…`S111` | yes | `015e600e…b17a9f3` |
| `assimilation/staged-ids` (staged `SOURCES.append.md`) | 132 | `S106`…`S237` | yes | `93841167…c5da089b` |
| `assimilation/collisions` | **6** | `S106 S107 S108 S109 S110 S111` | — | `b184a461…31d5fb72` |

Full lists are the two committed id files under `.ufo/waves/round-38/assimilation/` (also copied
to `w1/artifacts/R38ExecIdCollision/`). Neither file contains an internal duplicate id, and
neither contains a row the 0–3-space pattern misses (proof §C below).

**Collision count: 6.**

## Guard proof (required — indented row must still be caught)

Pattern on both sides: `^ {0,3}\|[[:space:]]*S[0-9]{3,}`, mechanism
`grep -oE <pattern> | grep -oE 'S[0-9]+' | sort` then `comm -12`.

Case A — scratch registry holding a **2-space-indented** `  | S002 |` row against a scratch
staged set that also holds `S002`:

```
registry file:            staged file:
| S001 | r1 |             | S001 | s1 |
  | S002 | r2 two-space |   | S002 | s2 two-space |
| S004 | r4 |             | S003 | s3 |

reg ids    : S001 S002 S004
staged ids : S001 S002 S003
collisions : S001 S002     (count 2, file 10 bytes)
```

`S002` is present in the collisions file, so indentation inside the 0–3-space window does not
hide a row. Indentation matrix (same pattern, `S002` on both sides):

```
case b: registry 2-space,  staged flush      -> collisions=1  bytes=5   (caught)
case c: registry flush,    staged 2-space    -> collisions=1  bytes=5   (caught)
case d: registry 3-space,  staged flush      -> collisions=1  bytes=5   (caught, window edge)
case e: registry 4-space,  staged flush      -> collisions=0  bytes=0   (control: outside window)
case f: registry tab,      staged flush      -> collisions=0  bytes=0   (control: outside window)
```

Coverage of the pattern over the two real files (so the "6" is not an artefact of indentation):

```
registry rows indented >=4 spaces : 0        staged rows indented >=4 spaces : 0
registry tab-indented S rows      : 0        staged tab-indented S rows      : 0
registry S-id rows not matched    : 0        staged S-id rows not matched    : 0
```

Boundary statement: the 0–3-space window is deliberate (3 is the Markdown code-block-adjacent
indent limit for a table row); cases e/f show it is *not* indentation-tolerant beyond 3 spaces
or tabs. That is safe here only because both real files have zero such rows — measured, not
assumed. If the append ever indents a row by ≥4 spaces or a tab, the guard goes blind.

## Renumber-by-document map (URL/anchor is the evidence)

The six colliding numbers hold **six different documents** on the registry side. The map below
is keyed by document, and no id is obtained by adding a constant to another id.

| id | staged document (URL) | registry occupant of that number | same document already in the registry? | final registry id |
|---|---|---|---|---|
| S106 | unblob README — `raw.githubusercontent.com/onekey-sec/unblob/HEAD/README.md` (§ Features, § Installation) | binutils `readelf.c` @ `6ce87bbc` | yes, by the registry's own note: S110 = "staged as package S106, renumbered by document" (unblob README re-pinned to tag `26.6.4`) | **S110** |
| S107 | devttys0 sasquatch README — `raw.githubusercontent.com/devttys0/sasquatch/master/README.md` (§ Prerequisites, § Installation) | onekey-sec sasquatch release tag `sasquatch-v4.5.1-6` | yes, twice over: **identical URL** to registry S111, and S111 carries "staged as package S107, renumbered by document" | **S111** |
| S108 | Linux `core(5)` man page — `man7.org/linux/man-pages/man5/core.5.html` | unblob `squashfs.py` @ tag `26.6.4` | no (distinct document) | fresh id at append (`S112`+ in adoption order) |
| S109 | Binwalk v3 README — `raw.githubusercontent.com/ReFirmLabs/binwalk/HEAD/README.md` | neovim release `v0.12.6` | no (distinct document) | fresh id at append (`S112`+) |
| S110 | dncil README — `raw.githubusercontent.com/mandiant/dncil/main/README.md` | unblob README @ tag `26.6.4` | no (distinct document — the staged unblob README is the *other* row, S106) | fresh id at append (`S112`+) |
| S111 | jadx README — `raw.githubusercontent.com/skylot/jadx/HEAD/README.md` | devttys0 sasquatch README | no (distinct document) | fresh id at append (`S112`+) |

Evidence that the first two rows of the map are already applied, not proposed:

- `corpus/SOURCES.md:116` anchor cell ends `(staged as package S106, renumbered by document)`; `:117` ends `(staged as package S107, renumbered by document)`.
- `corpus/knowledge/2026-10-26-unblob-sasquatch-dependency.md:8` — "staged ids renumbered by document (staged S106 → S110, staged S107 → S111)". That entry is the one registry S110/S111 both list in `used-by`.

So the precedent is *per-document, at adoption time*: two rows were adopted in round 36, they took
the registry's then-free `S110`/`S111`, and the remaining 130 staged labels were left untouched.
The check does not license an `+6` shift of the staged block (that would move 126 rows that
collide with nothing and would rewrite every staged citation); the only rows that move are the
documents that actually collide.

Rule for the open four (`S108`–`S111` of the staged file), stated so the L1 can apply it to
whichever rows its Gate admits:

1. A staged row is a *label*, not an id. Its number may be reused only if the registry row at that
   number is the same document; otherwise the document gets a fresh registry id.
2. Fresh ids are assigned **from the registry's next free number, in adoption order** — at this
   revision `S112`, then `S113`, … (registry max `S111`). The staged labels `S112`–`S237` are
   other documents, so they neither reserve nor consume those numbers.
3. `S106`/`S107` are not re-appended; if the round wants the HEAD-anchored or A-tier variant, it
   amends `S110`/`S111` rather than adding a duplicate (see the tier note below).
4. Every citation of a moved id is re-pointed in one simultaneous pass (the campaign's
   `renumber-staged.py` does this because a chained remap lands citations on the wrong row). The
   lane's own map file is `ID-REMAP.md` at adoption time.

For the theme actually in play this round, only two of the 28 sasquatch/unblob/AVM staged rows
collide (`S106`, `S107`); `artifacts/R38ExecIdCollision/theme-rows.tsv` lists all 28 with their
staged id, opened date and collision status.

## Findings beyond the count

1. **Why the collision exists — stale packaging premise (calibration).**
   `merge/kaidoku/MERGE-REPORT.json` states `existing_rows: 105`, `first_id: "S106"`,
   `renumbered: []`, and `MERGE-REPORT.md` says "lane registry currently holds **105** rows;
   first staged id is **S106**". Both are true of the tree the package was cut from and false of
   the tree it would append to: `git show 66b84027^:corpus/SOURCES.md | grep -c '^ *| S'` → `105`,
   and the six numbers were then spent by `66b84027` (round 34, adds S106) and `ffc81341`
   (round 36, adds S107–S111, including the two rows that renumber staged S106/S107). The
   package renumbered nothing at build time, so its `S106..S237` block now starts inside the
   registry's own id space.
2. **`S107` is a duplicate document, not merely a colliding number.** Its URL is byte-identical
   to registry `S111` (`…/devttys0/sasquatch/master/README.md`). Adopting it as any new id would
   put one document in two rows. Tier note for the Gate: staged `S107` is tier `A`, registry
   `S111` is tier `B`; if the staged row's evidence is richer, amend `S111`, do not add a row.
3. **`S106` is already adopted with a stronger anchor.** Registry `S110` re-pinned the unblob
   README to tag `26.6.4` (commit `1fcc7a0a…`, sha256 `6544d60f…`) where the staged row floats on
   `HEAD`; the adopted entry records three pre-admission corrections, one of which was exactly
   "pins by document instead of a floating `HEAD`". Re-appending the HEAD row would undo that.
4. **One internal staged duplicate sits inside the theme.** Staged `S183` and `S189` carry the
   same URL (`…/onekey-sec/unblob/main/python/unblob/handlers/filesystem/squashfs.py`) — two
   labels, one document, and registry `S108` already holds the same file at tag `26.6.4`. Other
   staged same-URL pairs, outside the theme: `S128`/`S138`, `S131`/`S143`, `S141`/`S158`,
   `S194`/`S204`, `S224`/`S237`.
5. **The staged rows cannot serve C1's "opened 2026-10-26" SOURCES row.** Staged `opened` values
   are 54 rows `2026-10-23` and 78 rows `2026-10-24`; none is `2026-10-26`. So `P38-C1`'s "row
   opened 2026-10-26" must be a new lane row, whether or not an assimilation row is appended —
   the append can supply provenance, not the claim's dated row.
6. **Registry-side duplicate URLs are unchanged and consistent with the census.** `census-start.txt`
   lists 9 `W04` rows over 7 distinct URLs; my independent scan finds exactly 7 distinct registry
   URLs with >1 row (the `rea-agents` tarball URL accounts for 3 of the 9). Not a defect this
   move introduces or must fix — recorded so a later count difference is not read as drift.

## Citation re-pointing (only if a row actually moves)

Staged knowledge entries citing ids in `S106`–`S111` (measured, `grep -oE '\bS[0-9]{3}\b'`):

| staged entry | cites | becomes (per the map) |
|---|---|---|
| `unblob-sasquatch-dependency.md` | `S106`, `S107` | `S110`, `S111` |
| `unblob-format-matrix.md` | `S106`, `S107`, `S122` | `S110`, `S111`, `S122` (no change for S122) |
| `sasquatch-prebuilt-package-inventory.md` | `S107`, `S130` | `S111`, `S130` (no change for S130) |

The first entry is already adopted in the lane (as `2026-10-26-unblob-sasquatch-dependency.md`)
with the re-pointed ids, so re-adopting the staged file as-is would re-introduce `S106`/`S107`.

## Limits

- Measured at lane HEAD `cb4326b2` on the working tree, not at the claims base `77091b49`; the
  registry at the base is also 111 rows `S001`–`S111` (`git show 77091b49:corpus/SOURCES.md`), so
  the collision set does not depend on which of the two is used, but the two files were not
  byte-compared.
- Column reads on the staged file must honour its escaping: in-cell pipes are written `\|`, so a
  naive `.split('|')` over-counts cells (S127 reads 13 cells naively, 11 escape-aware). With
  escaping honoured, all 132 staged rows carry the 11-column schema and the `opened` split is
  54 × `2026-10-23` / 78 × `2026-10-24`. The id column is the first cell in every row either way,
  which is why the guard pattern is safe.
- The check is number-level plus a URL-identity pass. It does not verify the staged rows'
  *content* (quotes, counts, reachability) — that is the per-entry Gate and the quarantine slice,
  a different seat.
- `comm` needs sorted input; both files are produced by `sort` in the pipeline, and I re-ran the
  intersection against freshly `sort`ed copies of the committed id files (same 6 ids), so a
  locale-sort ordering issue is excluded for this input size.
- No defect was repaired: `plans/round-38-claims.md`, `corpus/SOURCES.md`, the staged file and
  the census are untouched. The two rows whose map entry is already applied were found, not
  changed.

## Files written (all under the lane, none of them corpus/evidence)

- `.ufo/waves/round-38/w1/R38ExecIdCollision.md` (this report)
- `.ufo/waves/round-38/assimilation/{reg-ids,staged-ids,collisions}` — the commanded outputs,
  committed as wave evidence
- `.ufo/waves/round-38/w1/artifacts/R38ExecIdCollision/{guard-proof.txt,receipt.txt,collision-table.md,renumber-map.tsv,theme-rows.tsv,reg-ids,staged-ids,collisions}`

Scratch `/fast/scratch/hyaku/kaidoku-r38/R38ExecIdCollision` removed before finishing; nothing
cited here lives only in scratch. No tool installed or updated. No `agent://` message sent.
