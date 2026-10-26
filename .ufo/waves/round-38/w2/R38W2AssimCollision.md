# R38W2AssimCollision — addendum §10 id-collision re-run (kaidoku round 38, attempt 2, wave 2)

**VERDICT: DEFECTS FOUND.** The guard itself is correct and contract-aligned, and the renumber
map is verified by document — but the committed collision receipt no longer reproduces at the
commit that ships it (6 vs 11 at `3b960fe5`), `LOG.md:3132` states the pre-append count
unqualified, and the landing appended a second registry row for a document the registry already
held (S108/S112), a duplicate the number guard cannot see. Details as D1–D4 below.

Seat `R38W2AssimCollision`, executor, leaf. Advisory only. No lane file changed except this
report and the artifacts directory named at the end; no VCS mutation (read-only `git show`/
`git log`/`git ls-tree` only); no REA command; nothing run inside `shokuknow` (read-only reads
of `SOURCES.append.md`); nothing installed or updated; no `agent://all` message.

Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, HEAD `0fc6113376a156fddc3ec385386d71c3a4a9f690`.
Frozen state measured against: first freeze `e059ca9391642d5b71b6662cabcbdce0d9308719`.
Host time at measurement: 2026-10-26T04:00-03:00.

## Axes worked

- **coverage** — re-run the exact §10 command against the registry as it stands now, so the
  collision set is a measurement of the landed tree, not a replay of the freeze-time one.
- **calibration** — decide, per id, whether a numerical collision is a *document* collision;
  publish the number/file identities that make the answer checkable, and state which of the
  landed statements the new number falsifies.

## 1. The commanded check, re-run against the current registry

Exact pipeline (verbatim, `S=/fast/scratch/hyaku/kaidoku-r38/R38W2AssimCollision`, reproduced
as `artifacts/R38W2AssimCollision/repro.sh`):

```
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md                        | grep -oE 'S[0-9]+' | sort > reg-ids-now
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' /home/vgpnk/Projects/shokuknow/merge/kaidoku/SOURCES.append.md | grep -oE 'S[0-9]+' | sort > staged-ids
comm -12 reg-ids-now staged-ids > collisions-now
```

All stages exit 0 (`comm` exits 0 even on an empty intersection, so the non-empty file is the
signal, not the exit code).

| list | rows | range | contiguous | sha256 |
|---|---|---|---|---|
| `reg-ids-now` (`corpus/SOURCES.md` at HEAD/worktree) | **116** | `S001`…`S116` | yes | `faf34681…dd340b` |
| `staged-ids` (`SOURCES.append.md`, unchanged) | **132** | `S106`…`S237` | yes | `93841167…c5da089b` |
| `collisions-now` | **11** | `S106`…`S116` | yes | `872a9093…b5a8f81d` |

`staged-ids` is byte-identical to the committed `.ufo/waves/round-38/assimilation/staged-ids`
(`cmp` clean), so the staged side has not drifted since wave 1.

**Collision count: 6 → 11. The delta is exactly `S112 S113 S114 S115 S116`** — the five ids this
round's own append allocated.

## 2. Guard proof on a scratch registry (indented `  | S002 |` must be caught)

Pattern `^ {0,3}\|[[:space:]]*S[0-9]{3,}`, mechanism `grep -oE <pattern> | grep -oE 'S[0-9]+' |
sort` then `comm -12`. Full transcript `artifacts/R38W2AssimCollision/guard-proof.txt`:

| case | registry indent | staged indent | collisions | caught? |
|---|---|---|---|---|
| A (both sides 2-space `S002`) | 2 | 2 | `S001 S002` (count 2, 10 B) | **yes** |
| B (registry 2-space only) | 2 | 0 | `S002` (1, 5 B) | yes |
| C (staged 2-space only) | 0 | 2 | `S002` (1, 5 B) | yes |
| D (window edge, 3-space) | 3 | 0 | `S002` (1, 5 B) | yes |
| E (control, 4-space) | 4 | 0 | — (0, 0 B) | no |
| F (control, tab) | tab | 0 | — (0, 0 B) | no |

**Alignment with the maintained parser (new measurement).** Cases E/F are not a guard defect:
they are the census contract. `scripts/sources-census.sh` states "Maintained parser accepts 0–3
leading ASCII spaces before Markdown rows/headings; 4 or more spaces are indented code and
ignored". Measured on scratch fixtures
(`census --root` over a one-row registry at each indent width):

```
indent=2  census rows=1   guard ids=S002
indent=4  census rows=0   guard ids=
```

So the guard's window is exactly the census's window — a row invisible to the guard is a row
invisible to the census too. Wave 1 flagged ≥4-space/tab indentation as a "blind spot"; that
framing is too strong: it is a deliberate, documented contract limit, matched on both sides.
It remains true that an append which indents a row by ≥4 spaces would be invisible to *both*,
i.e. it would silently leave the registry.

Real-file coverage (no row hides in either file):

```
SOURCES.md          : S-id rows total=116 matched=116 depth>=4=0 tab-indented=0
SOURCES.append.md   : S-id rows total=132 matched=132 depth>=4=0 tab-indented=0
```

## 3. Comparison with the committed artifacts, and what changes now

The committed `.ufo/waves/round-38/assimilation/{reg-ids,staged-ids,collisions}` were captured
before `S112`–`S116` existed. Reproducing the pipeline at three revisions (`git show <rev>:corpus/SOURCES.md`):

| revision | registry rows | collisions | id-list sha256 | equal to committed? |
|---|---|---|---|---|
| `e059ca93` (first freeze) | 111 | **6** (`S106`–`S111`) | `015e600e…b17a9f3` | `reg-ids` **identical**, `collisions` **identical** (`cmp` clean, `b184a461…31d5fb72`) |
| `3b960fe5` (the landing commit) | 116 | **11** (`S106`–`S116`) | `faf34681…dd340b` | **differs** |
| `0fc61133` (HEAD) | 116 | **11** | `faf34681…dd340b` | **differs** |

So the committed `collisions` file is a faithful *freeze-time* snapshot (it is byte-equal to what
the command yields at `e059ca93`), and it is also the artifact set committed *by* `3b960fe5` —
the same commit that adds `S112`–`S116`. The consequence is exact and reproducible:

> Running the documented §10 command at `3b960fe5` (or at HEAD) yields 11 collisions, not the 6
> the committed `collisions` file records. The receipt does not reproduce at its own commit.

What changes now, precisely:

1. **The number is 11, not 6.** Every citation of "6" is a freeze-time reading.
2. **The five new collisions are all document-distinct.** Measured URL per id (lane side vs
   staged side, exact strings in `doc-collision-matrix.tsv`):
   `S112` unblob `squashfs.py` @26.6.4 ↔ staged `S112` Apktool README;
   `S113` unblob BE fixtures tree ↔ staged `S113` `developer.android.com/tools/adb`;
   `S114` Freetz AVM-BE note ↔ staged `S114` `bbs.kanxue.com/forum-4.htm`;
   `S115` 7-Zip refusal (own-work, no URL) ↔ staged `S115` `bbs.kanxue.com/forum-161.htm`;
   `S116` `unblob.org/formats/` ↔ staged `S116` `gihyo.jp` ebook page.
   **No document collision was introduced by the append.**
3. **The count's meaning flips.** The registry has now entered the staged block (`S106`–`S237`).
   Every further registry id up to `S237` will collide numerically with a staged label while
   colliding by document with nothing. A rising `collisions` count is therefore no longer
   evidence of anything; the informative metric is the document-level pair list in §5.

## 4. Renumber map verified by document (the commanded two checks)

| check as assigned | measured | verdict |
|---|---|---|
| staged `S122` URL == lane `S116` URL | both exactly `https://unblob.org/formats/` | **equal, exact** |
| staged `S106` URL == lane `S110` URL (or same document at a pinned tag) | staged `…/unblob/HEAD/README.md`, lane `…/unblob/26.6.4/README.md` — same repository + path, ref `HEAD` vs tag `26.6.4` | **same document at a pinned tag** |

Corroboration, read from the registry itself (not inferred): `corpus/SOURCES.md:116` (S110) ends
its anchor "(staged as package S106, renumbered by document)"; `:122` (S116) ends "(staged as
package S122, renumbered by document)". The assimilated entry's front matter repeats both
(`corpus/knowledge/2026-10-26-unblob-format-matrix.md:1-2,10-11`), and its one bare `S112`
citation (`:34`) points at the *lane* handler row, which is the correct new id.

Citation hygiene holds: no landed file cites a staged label without the "staged …" qualifier —
checked `corpus/knowledge/2026-10-26-*`, `corpus/lessons/round-38.md`, `PROVINCE.md`,
`SCORECARD.md`, `LOG.md` for `S106|S107|S122`.

## 5. Findings

**D1 (evidence reproducibility).** `assimilation/collisions` is a pre-append snapshot shipped
inside the post-append commit. The claims require the check "before any append", so the *timing*
is compliant; the defect is that the shipped artifact set has no companion post-append snapshot,
so a reader who runs the stated command at `3b960fe5` gets a different number from the file next
to it. Cheapest fix for L1: land a `collisions-at-3b960fe5` beside the existing one, or label the
existing file `collisions-pre-append`.

**D2 (stale statement).** `LOG.md:3132` reads "Collisions S106–S111 (6)" with no pre-append
qualifier, in the round's Sources bullet, i.e. as the round's result — while the registry that
bullet describes yields 11. `corpus/lessons/round-38.md:38-39` is safer because it pins the input
("registry ids S001–S111 (111)"), but it sits six lines above `:34` "Rows 111 → 116 (S112–S116
appended)", so the two halves of one section describe different registries. This is a wording
defect, not a fabricated number: 6 is exactly right at `e059ca93`.

**D3 (duplicate registry row the number guard cannot see).** The landing appended `S112` for
`https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/handlers/filesystem/squashfs.py`
— **the exact URL already held by lane `S108`**, same kind `code`, same tier `A`, same tag commit
`1fcc7a0a…`, and the same digest (`2d7b901b…9287`, per the Gate's own re-open). Worse, `S112`'s
scope is a strict subset of the row it duplicates:

- `S108` scope: "How unblob 26.6.4 names and invokes its SquashFS extractors (sasquatch,
  **sasquatch-v4be**), the **LE/BE argv** and the AVM test only…"
- `S112` scope: "v4 BE extractor dependency and argv for unblob 26.6.4 only…"

The fact `S112` was added to carry ("`V4BE_EXECUTABLE`", "`get_dependencies()` returns
`sasquatch` + `sasquatch-v4be`") is already inside `S108`'s stated scope and its anchor text
("lines 24-26 EXECUTABLE and V4BE_EXECUTABLE … 68-69 get_dependencies"). So the second row adds
no scope the registry did not have. This is disclosed (`corpus/lessons/round-38.md:28`: "same URL
as S108 with a BE-v4 dependency scope; census W04 (across scopes), not E04") and it is legal
under SOURCES-CONTRACT-v1 (W04, not E04) — but it is inconsistent with the rule this same round
applied to the staged side in wave 1: "`S106`/`S107` are not re-appended; if the round wants the
… variant, amend `S110`/`S111` rather than adding a duplicate"
(`.ufo/waves/round-38/w1/R38ExecIdCollision.md` §renumber rule 3). Under that rule the BE fact
should have been cited to `S108` (or `S108`'s scope widened), not given `S112`.

Measured census effect, same script and `--today` on a replica of each revision
(`artifacts/…/census-freeze-e059ca93.txt`, `census-end-head.txt`; the freeze replica reproduces
the committed `census-start.txt` line-for-line apart from the fixture path):

```
freeze  e059ca93 : exit 0, 9 W04,  rows 111  (A 104, B 6, C 1; mined 107, rejected 4)
HEAD    0fc61133 : exit 0, 10 W04, rows 116  (A 108, B 7, C 1; mined 111, rejected 5)
new line         : kaidoku  W04  S112 duplicate url raw.githubusercontent.com/onekey-sec/
                   unblob/26.6.4/python/unblob/handlers/filesystem/squashfs.py across scopes
```

The claims require "End census is pasted in the report" and record the start as "exit 0, 9 W04".
**The end census is 10 W04, and the single delta is `S112`.** An end census pasted as 9 would be
wrong; pasted as 10 it must name D3 as its cause.

**D4 (guard scope).** The number-intersection check cannot see a same-document pair at different
numbers. Full 116×132 document matrix (`doc-collision-matrix.tsv`, URL normalised for ref
`HEAD|main|master` and tag `26.6.4`) yields 8 pairs, of which the number guard sees at most the
two already-applied ones:

| staged | lane | match | status |
|---|---|---|---|
| `S107` | `S111` | exact URL | resolved (not appended; renumber rule) |
| `S106` | `S110` | same doc, pinned tag | resolved (renumbered by document) |
| `S122` | `S116` | exact URL | resolved (admitted as `S116`) |
| `S192` | `S114` | **exact URL** (Freetz AVM-BE note) | refused entry, not appended — but **not named in the wave-1 map** |
| `S183`, `S189` | `S108`, `S112` | same doc at unpinned `main` vs tag `26.6.4` | refused entry, not appended |

`S192` is new information relative to wave 1: the wave-1 collision report records `S183`/`S189`
as a staged-internal duplicate pair but never notices that staged `S192` is byte-for-byte the same
document as lane `S114`. No harm landed (the round-9 entry carrying it was refused), but the map
an L1 would reuse to adopt that entry is incomplete: adopting staged `S192` would duplicate
`S114` exactly as `S107` would have duplicated `S111`.

## Limits

- URL identity is a proxy for document identity; I compared URL strings with one ref
  normalisation (`HEAD|main|master` and `26.6.4` → `REF`). Two different URLs pointing at one
  document (mirror, redirect) would be missed; two refs of one patch-set (`sasquatch-v4.5.1-{1..6}`)
  are treated as distinct, which matches the registry's own scoping.
- One measurement run was invalidated and redone: an early guard-proof fixture in the same
  scratch directory overwrote `staged-ids`, producing a spurious `S001 S002 S003` intersection.
  The fixture was renamed, `staged-ids` regenerated, and every number in this report comes from
  the corrected run (its sha matches the committed `staged-ids` exactly, which is the cross-check
  that the file is the real one). No number from the invalidated run survives here.
- The census replica root sits in scratch with symlinks to the lane's `corpus/*` and top-level
  entries, so the `ok` line prints the fixture path; all finding lines are byte-compared against
  the committed `census-start.txt`.
- Not judged here: whether C1 stopped correctly, whether C2 met its target, or whether the
  per-entry Gate's admits are sound. This seat attacks the id-collision surface only.

## Files written (all under the lane; nothing in `corpus/`, `plans/`, `tools/`)

- `.ufo/waves/round-38/w2/R38W2AssimCollision.md` (this report)
- `.ufo/waves/round-38/w2/artifacts/R38W2AssimCollision/`: `reg-ids-now.txt` (116),
  `reg-ids-committed.txt` (111), `staged-ids.txt` (132), `collisions-now.txt` (11),
  `collisions-at-freeze-e059ca93.txt` (6, `b184a461…`), `collisions-at-landing-3b960fe5.txt` (11),
  `collisions-at-head-0fc61133.txt` (11), `collisions-committed.txt` (6),
  `guard-proof.txt`, `doc-collision-matrix.tsv`, `census-freeze-e059ca93.txt`,
  `census-end-head.txt`, `repro.sh`

Scratch `/fast/scratch/hyaku/kaidoku-r38/R38W2AssimCollision` removed before finishing; every
file cited above lives in the lane. No tool installed or updated.
