# R44W2ScribeCensus — census annex (round 44, wave 2)

Seat `R44W2ScribeCensus` (scribe). Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Generated 2026-10-28T14:24Z. Nothing in this annex changes a claim, counter, rubric, frozen byte
or production doc; the two numbered defects below are record findings for the L1.

| revision | commit | `corpus/SOURCES.md` blob |
|---|---|---|
| base (round start) | `c29360e3ba5381a5ab69e372d0d9577970f85018` | `d0e6770a85f4be9a5e09865f4e8cce5934c2b7fe` |
| freeze | `c48f8a4bfd449300c975668e59aae5b5538b6a84` | `c513fad08543075d304c49af212005153d64a22e` |
| tip at dispatch (assignment) | `c86ea508188c50e2645b1f9bba65df4177cda6b1` | `c513fad08543075d304c49af212005153d64a22e` |
| observed HEAD at run time | `8bb1090af3fef64477c4337855e4347472db2701` | `c513fad08543075d304c49af212005153d64a22e` |

The observed HEAD is one commit past the assignment's tip (it is the wave-2 dispatch commit).
`git diff --diff-filter=D --name-only c86ea508 8bb1090` prints 0 deletions; the interval only
modifies `LOG.md`/`SCORECARD.md`/`corpus/QUALITY.md` and adds the lesson, `tools/round-45/` and
wave-2 files, so the census inputs are the same on both. `corpus/SOURCES.md` is clean against HEAD
(`git diff --quiet -- corpus/SOURCES.md`).

Census tool: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`,
sha256 `3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30`
(GNU bash 5.3.20, GNU Awk 5.4.1). This tool lives in the fleet repo and is **not** covered by the
lane's frozen-path set; its digest is pinned here so the two runs are reproducible.

## 1. The two required runs

**Run A — round start, reproduced from the BASE tree** (the original round-start run cannot be
re-run; no start receipt is committed — see CEN-2):

```
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /fast/scratch/hyaku/kaidoku-r44/R44W2ScribeCensus/base-root kaidoku
```

- exit **0**
- 13 `W04` lines, then `kaidoku	ok	/fast/scratch/hyaku/kaidoku-r44/R44W2ScribeCensus/base-root/kaidoku-shokunin/corpus/SOURCES.md`
- stdout sha256 `f6e06d8ee0b1c6db56caf1534967abd1c939a85297f5c9499f650762d7c20202` (1424 B)
- stderr empty (sha256 `e3b0c442…b855`), wall 220 ms

Reproduction setup: `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin archive
c29360e3ba5381a5ab69e372d0d9577970f85018 | tar -x -C <scratch>/base-root/kaidoku-shokunin`, plus
a one-lane fixture `shokunin.conf` (`kaidoku|kaidoku-shokunin|base fixture lane`, kept as
`artifacts/R44W2ScribeCensus/base-root-shokunin.conf`). The lane id and the `ok` line's warning
semantics are preserved; only the `ok` line's directory is the fixture path.

**Run B — current tip:**

```
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku
```

- exit **0**
- 14 `W04` lines, then `kaidoku	ok	/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md`
- stdout sha256 `9f32a8a84ef13933a0539a92a4475534aeb2ae858a407d35b176aa26662acf19` (1518 B)
- stderr empty, wall 239 ms

Run B is byte-identical to the cited round-end receipt
`.ufo/waves/round-44/l1/sources-census-end.txt` (sha256 `9f32a8a8…acf19`, 1518 B). The 13 base
warning identities are a subset of the 14 tip identities; no warning disappeared.

Exit-code semantics (script header): `0` clean or warnings, `1` E/overdue findings, `2`
usage/env/missing registry; `W04` is "same URL across scopes" and a W-code never changes status.

## 2. Row counts

Counting command (the frozen one; no new regex):

```
grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md
```

| tree | cwd | output |
|---|---|---|
| BASE `c29360e3` | `<scratch>/base-root/kaidoku-shokunin` | **137** |
| tip `8bb1090` | `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` | **139** |

Cross-check with the census's own counter (`census` mode, same `--root` forms), exit 0 both:

| metric | BASE | tip |
|---|---|---|
| rows | 137 | 139 |
| tier.A | 129 | 131 |
| tier.B | 7 | 7 |
| tier.C | 1 | 1 |
| status.mined | 132 | 134 |
| status.rejected | 5 | 5 |
| status.queued | 0 | 0 |

`git diff c29360e3 8bb1090 -- corpus/SOURCES.md` is 3 insertions, 0 deletions: S138, S139, and one
blank line. Parsed row-level delta (`registry-row-delta.txt`): added `S138,S139`; removed none;
changed existing rows none. So "no `status`/`recheck`/`used-by` cell of an existing row was changed"
holds.

## 3. Warning list at the tip, one-line classification each

All 14 are `W04` (same normalized URL on rows in different scopes); 13 are present at BASE, and
exactly one (S138) is new this round. Partner rows are computed with the census's own `url_of`
normalization (`w04-classification.tsv`).

| # | row | warning (verbatim body) | one-line classification |
|---|---|---|---|
| 1 | S033 | `duplicate url github.com/NationalSecurityAgency/ghidra/pull/9348 across scopes` | Pre-existing W04; same URL as S032 (Ghidra PR 9348); distinct ids. |
| 2 | S047 | ``duplicate url go.dev/dl/?mode=json&include=all`,` across scopes`` | Pre-existing W04; same URL as S038; the trailing backtick+comma is captured because the source cell uses inline-code punctuation (census URL-regex artefact, present on both rows). |
| 3 | S054 | `duplicate url developer.android.com/ndk/guides/abis across scopes` | Pre-existing W04; same URL as S052 (Android NDK ABI list). |
| 4 | S062 | `duplicate url raw.githubusercontent.com/sigrokproject/sigrok-cli/sigrok-cli-0.7.2/doc/sigrok-cli.1 across scopes` | Pre-existing W04; same URL as S058 (sigrok-cli man page). |
| 5 | S069 | `duplicate url www.wireshark.org/docs/man-pages/tshark.html across scopes` | Pre-existing W04; same URL as S065 (tshark man page). |
| 6 | S083 | `duplicate url registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz across scopes` | Pre-existing W04; one of five rows on the rea-agents 6.5.0 tarball (S079,S083,S090,S092,S119,S123), distinct scopes. |
| 7 | S090 | same URL as #6 | Pre-existing W04; same rea-agents tarball group. |
| 8 | S092 | same URL as #6 | Pre-existing W04; same rea-agents tarball group. |
| 9 | S102 | `duplicate url learn.microsoft.com/en-us/windows/win32/debug/pe-format across scopes` | Pre-existing W04; same URL as S100 (PE format spec). |
| 10 | S112 | `duplicate url raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/handlers/filesystem/squashfs.py across scopes` | Pre-existing W04; same URL as S108 (unblob squashfs handler source). |
| 11 | S117 | `duplicate url raw.githubusercontent.com/onekey-sec/unblob/26.6.4/README.md across scopes` | Pre-existing W04; same URL as S110 (unblob README). |
| 12 | S119 | same URL as #6 | Pre-existing W04; same rea-agents tarball group. |
| 13 | S123 | same URL as #6 | Pre-existing W04; same rea-agents tarball group. |
| 14 | S138 | `duplicate url github.com/onekey-sec/unblob/tree/26.6.4/tests/integration/filesystem/squashfs across scopes` | **New this round**; same URL as pre-existing S130; not a duplicate id; S138 is the round's second oracle row (tier A, dataset, mined). |

## 4. Rows added

From `git show 8bb1090:corpus/SOURCES.md` (fields parsed with the census's 11-column layout):

| id | kind | tier | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|
| S138 | dataset | A | mined | 2026-10-28 | 180d | `corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md` |
| S139 | docs | A | mined | 2026-10-28 | on-release | `corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md` |

Both `used-by` targets exist at the tip (the entry is first added at `4cc1ac11`), so the tip run has
no `E11`. At the freeze tree the entry is still absent; see CEN-1's triangulation.

## 5. Findings for the L1

### CEN-1 (record) — the lesson's round-start warning count is not reproducible from the round-start tree

- Where: `corpus/lessons/round-44.md:47` — "round-start … → `kaidoku ok`, exit 0, 14 W04
  duplicate-URL warnings (pre-existing; S138 is the 14th …)" (paragraph at lines 44-50).
- Command run (this seat): `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /fast/scratch/hyaku/kaidoku-r44/R44W2ScribeCensus/base-root kaidoku`; exit **0**; observed **13** `W04` lines, not 14 (stdout sha256 `f6e06d8e…c20202`).
- Triangulation, same command family, three tree states:

  | tree | rows | W04 | E11 | exit |
  |---|---|---|---|---|
  | BASE `c29360e3` (round start) | 137 | **13** | 0 | 0 |
  | FREEZE `c48f8a4b` | 139 | 14 | **2** (`S138`,`S139` missing used-by — the entry does not exist yet) | **1** |
  | tip `8bb1090` (≥ `4cc1ac11`, entry landed) | 139 | 14 | 0 | 0 |

  The cited "ok, exit 0, 14 W04" state is first reachable at `4cc1ac11` (the commit that first adds the C1 entry),
  not at round start. The parenthetical is also self-contradictory: if S138 is the 14th warning,
  then 13 (not 14) are pre-existing. Suggested record fix (no claim change): state "13 W04 at
  round start (BASE), 14 at close (S138 added)" — or cite the start replay explicitly.
- Supplementary evidence (not owned by this seat, untracked, and **not** a clean receipt):
  `.ufo/waves/round-44/l1/sources-census-start-replay.txt:1` begins with
  `ERROR: config not found: /fast/scratch/hyaku/kaidoku-r44/l1/shokunin.conf` and then a
  `baseclone` run (13 W04, `ok`, exit not recorded); its mtime `2026-10-28 11:20:34 -0300` places
  it in wave 2. It corroborates 13 but cannot serve as a round-start receipt.

### CEN-2 (record) — the cited round-end census receipt is untracked

- Where: `.ufo/waves/round-44/l1/sources-census-end.txt:1`, cited at
  `corpus/lessons/round-44.md:48-49`.
- Command run: `git ls-files .ufo/waves/round-44/l1/sources-census-end.txt`; exit **0**; observed
  **empty output** (file present on disk: 1518 B, sha256 `9f32a8a8…acf19`, identical to this
  annex's tip stdout, but not committed). No round-start receipt exists to be cited at all.
- Risk if the round closes as-is: the lesson's census evidence is only in an untracked file; commit
  it at close (and note the start replay separately) or drop the citation.

## 6. Artifacts

All under `.ufo/waves/round-44/w2/artifacts/R44W2ScribeCensus/`; `receipt.json` carries every
command, cwd, exit code, stdout/stderr sha256, byte count and wall time.

- `census-validate-base.{stdout,stderr,exit,wall_ms}` — Run A
- `census-validate-tip.{stdout,stderr,exit,wall_ms}` — Run B
- `census-validate-freeze.{stdout,stderr,exit,wall_ms}` — triangulation (auxiliary; see CEN-1)
- `census-mode-{base,tip}.{stdout,stderr,exit,wall_ms}` — counter cross-check
- `rowcount-base.txt`, `rowcount-tip.txt` — the counting command's output
- `w04-base.txt`, `w04-tip.txt`, `w04-new.txt`, `w04-gone.txt`, `w04-classification.tsv`
- `sources-blobs.txt`, `sources-diff-base-tip.patch`, `registry-row-delta.txt`
- `base-root-shokunin.conf`, `run-context.txt`, `receipt.json`

## 7. Limits

- Run A is a replay on an extracted BASE tree with a one-lane fixture conf; its `ok` line names the
  fixture path, and `census`-mode `FLEET` lines are lane-local. The `validate` warning set and exit
  code are the values under test.
- The census script is a fleet-repo tool, not a lane-frozen path; only its sha256 is pinned here.
- `--today` defaulted to 2026-10-28 for both runs (opened-date validation). The BASE and FREEZE
  trees were extracted whole, so `E11` used-by existence was evaluated against real targets.
- No mutating git command was run; no claim, counter, rubric, frozen byte or production doc was
  touched. Scratch `/fast/scratch/hyaku/kaidoku-r44/R44W2ScribeCensus/` is removed at exit.
