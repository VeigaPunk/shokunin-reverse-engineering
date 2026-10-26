# R36W2ExecCensusEnd — end census vs `census-start.txt`, registry tallies at `cab59f22` vs `01a44dbf` (QUALITY 74)

Seat: leaf executor, godspeed posture. Read-only against the lane: `git show`/`log`/`diff`/`rev-parse`/`cat-file` only; no `git add|commit|checkout|reset|stash|pull|push`, no jj mutation. Scratch `S=/fast/scratch/hyaku/kaidoku-r36/R36W2ExecCensusEnd` (removed at close); nothing cited below lives under scratch or `/tmp`. No tools installed, no pacman/uv/npx. One baseline axis (registry census) taken at `HEAD = 01a44dbf45913a1bdcabbbfb85b7bb9d232cb930`; single-run session, runs stamped 2026-10-26 (~05:00Z).

## 1. End census — exact command, output, exit code

Command (verbatim; `--root` is the fleet root, target lane `kaidoku`):

```
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku
```

stdout (10 lines, unmodified):

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
kaidoku	ok	/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md
```

`EXIT=0`. Nine W04, no E-codes, `ok` line present — i.e. every `used-by` on every mined row resolves on disk at the tip (E11 clean), no duplicate id (E03), no enum violations (E02/E05/E06/E07), no date defects (E08/E09), no row outside `## Registry` (E12), no E01.

## 2. Compared with `.ufo/waves/round-36/census-start.txt`

`census-start.txt` content: line 1 `2026-10-26T04:12:08Z`, line 2 `rev=cab59f221fe19726b5692bfa4d9a9679e96b8a73`, then the **same nine W04 lines with the same ids and same order**, the same `kaidoku	ok	…/kaidoku-shokunin/corpus/SOURCES.md` line, and a literal `EXIT=0` trailer.

Normalized comparison (`grep -v '^2026-10-26T'` / `grep -v '^rev='` on the start file vs my captured stdout+exit):

```
11d10
< EXIT=0
```

The only difference is my own `EXIT=0` trailer, which the start file carries and my stdout capture kept separately. **The finding set is byte-identical: 9 W04, same ids, same order, `ok`, exit 0.**

Receipt identity: `git rev-parse <rev>:.ufo/waves/round-36/census-start.txt` = `277caa6f03fbd505925fba95f801580c6f743f26` at `790561d4` (freeze), at `01a44dbf` (tip) and in the two jj snapshots `787926b6`/`c341c6f8`; `git diff --stat 790561d4 01a44dbf -- .ufo/waves/round-36/census-start.txt` is empty. The receipt was not edited after the freeze.

Precondition the lesson claims — start census captured before the first registry edit — holds on the committed graph: the only commit in `cab59f22..01a44dbf` touching `corpus/SOURCES.md` is `ffc81341` (2026-10-26T01:47:29-03:00), and `790561d4` (freeze, 01:21:38-03:00) is its ancestor and carries the receipt. `787926b6` and `c341c6f8` are `refs/jj/keep/*` snapshots (same timestamp, not ancestors of the tip, no branch contains them) with the identical receipt blob — no divergence.

## 3. Registry tallies, base vs tip (QUALITY 74: count **and** per-status/per-tier)

Two independent implementations agree exactly — the frozen script's own row pass, and an awk one-liner over `git show`-extracted blobs:

```
git show cab59f22…:corpus/SOURCES.md > $S/base/corpus/SOURCES.md
git show 01a44dbf…:corpus/SOURCES.md > $S/tip/corpus/SOURCES.md
sources-census.sh census --file $S/{base,tip}/corpus/SOURCES.md     # rc=0 both
```

| metric | base `cab59f22` | tip `01a44dbf` | delta |
|---|---|---|---|
| rows | 106 | **111** | +5 |
| tier.A | 100 | 104 | +4 |
| tier.B | 5 | 6 | +1 |
| tier.C | 1 | 1 | 0 |
| tier.invalid | 0 | 0 | 0 |
| status.queued | 0 | 0 | 0 |
| status.mined | 102 | 107 | +5 |
| status.rejected | 4 | **4** | **0** |
| status.invalid | 0 | 0 | 0 |

Independent recount of the tip table body (lines 4–119, i.e. `## Registry` at line 3 up to `## Paths` at line 120): 113 pipe rows − header − separator = **111**, and the only rows that do not start with `| S<3+d>` are the header and the separator. So the script's 111 is not counting anything outside the id-bearing rows. Id set is `S001..S111`, contiguous, no gaps, no duplicates (`sort | uniq -d` empty).

Observations inside the tally (reported, not defects): the registry holds **zero `queued` rows** at both ends — intake lands directly as `mined` (5/5 this round); the single tier-C row is unchanged.

## 4. Which rows were added

`git diff --numstat cab59f22 01a44dbf -- corpus/SOURCES.md` → `5	0	corpus/SOURCES.md`; one hunk, `@@ -110,6 +110,11 @@`, inserted after S106 and before the blank lines + `## Paths`.

| id | tip line | kind | tier | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|
| S107 | 113 | code | A | mined | 2026-10-26 | on-release | `corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md` |
| S108 | 114 | code | A | mined | 2026-10-26 | on-release | `corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md` |
| S109 | 115 | dataset | A | mined | 2026-10-26 | on-release | `corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md` |
| S110 | 116 | docs | A | mined | 2026-10-26 | on-release | `corpus/knowledge/2026-10-26-unblob-sasquatch-dependency.md` |
| S111 | 117 | docs | B | mined | 2026-10-26 | 180d | `corpus/knowledge/2026-10-26-unblob-sasquatch-dependency.md` |

Sources (first cell): S107 onekey-sec/sasquatch release tag `sasquatch-v4.5.1-6`; S108 unblob `squashfs.py` at tag 26.6.4; S109 neovim `v0.12.6` release; S110 unblob `README.md` at 26.6.4; S111 devttys0/sasquatch `README.md`. Both used-by entries exist at the tip (`git cat-file -e 01a44dbf:…` → present), which is also what the exit-0 E11 pass in §1 establishes.

Tier/status deltas reconcile with the row set exactly: 4×A + 1×B = A+4/B+1; 5×mined = mined+5; rejected and C unchanged.

## 5. No pre-existing row changed — three independent checks

1. `git diff cab59f22 01a44dbf -- corpus/SOURCES.md` is additions only (`5 insertions(+), 0 deletions`); a moved/edited row would appear as a deletion+addition pair in the numstat, so no reordering and no in-place edit either.
2. Set difference of whole lines: `grep -vxF -f base tip` yields exactly the five new `| S107 … |` … `| S111 … |` lines and nothing else — every one of the 106 base lines survives verbatim in the tip.
3. The M34-12 swap signature is absent: `status.rejected` stays **4 → 4** (the round-34 failure was a `rejected` row overwritten by an insert, visible only as rejected 4→3 at an unchanged count). Here the count rose by exactly the number of inserted rows with the rejected population untouched, and `status.C`/`tier.C` are unmoved.

Structural placement also re-verified after the edit (`## Registry` 3, new rows 113–117, `## Paths` 120): the insert sits inside the Registry section, so E12 is silent — consistent with exit 0.

Blob-level separation of "validates" from "paths exist": validating the two extracted blobs with `--file` (mirror dir, so every used-by path is missing by construction) gives base `191 E11 + 9 W04`, tip `196 E11 + 9 W04`, exit 1 both, **no E01–E10 and no E12 in either blob**. The +5 E11 equals the 5 new rows × 1 used-by each. So the tip blob has the same finding profile as the base, and the worktree run in §1 is what proves those paths resolve.

## 6. Validator identity across the two censuses

`sha256sum /home/vgpnk/Projects/shokunin/scripts/sources-census.sh` = `3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30`; `git -C /home/vgpnk/Projects/shokunin status --porcelain -- scripts/sources-census.sh` empty; last commit touching it `f47ad6ba` (2026-10-25T09:29:03-03:00), i.e. before both the 04:12:08Z start capture and this run. The comparison in §2 is therefore against the same validator bytes, not merely the same script name.

## 7. Disagreements / residual findings

1. **`corpus/lessons/round-36.md:52` — the parenthetical is not in the receipt it attributes it to.** The line reads "…r34 D-1 (start census in its own file before the first registry edit) — `.ufo/waves/round-36/census-start.txt` (106 rows, exit 0, 9 W04)". The file contains a timestamp, `rev=cab59f22`, the nine W04 lines, `ok`, `EXIT=0` — **no row-count line**, because it is `validate` output and only `census` mode emits `rows`. The "106" is true of the base (I re-derived it in §3) but is not receipted by the cited file. Same residual was already named by wave 1 (`.ufo/waves/round-36/w1/R36CriticRoutedCoverage.md:109`, "the receipt records no row count (106); put it in the end census/report") and is still unaddressed at the tip. This report supplies the missing number (106 → 111); the lesson sentence itself is left as written — not mine to edit.
2. **Receipt-completeness, calibration:** neither the start receipt nor any stored census output carries the validator digest or the `--today` value in force, so "same tool, same UTC day" is not receipted — it is established here from git history (§6) and the session clock (start 04:12:08Z, end ~05:00Z on 2026-10-26). No behavioural consequence observed; recorded because a future end-census diff would otherwise be unable to exclude a validator change.
3. **Nothing else disagrees.** The task's premises are confirmed exactly: row count 106 → 111, five added rows S107–S111, `git diff` shows only additions, no pre-existing row altered, and the end census is the same 9 W04 + `ok` + exit 0 as the start census.
4. [INFERENCE] Routed to nobody: since `status.queued == 0` at both ends, a reader could not tell from tallies alone whether a new row was ever queued and later mined; the defensible check for this round was the id-set + line-identity check in §5, which is what QUALITY 74's per-status requirement is protecting.
5. Adjacent, not re-measured here (other seats own it): the S107 row's scope cell ("asset set") records only the amd64 deb — `R36W2ScoutS107.md` §"Scope-cell checks".

## Commands retained (all read-only)

`sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` (exit 0); `sources-census.sh census --file` on both extracted blobs (exit 0); `sources-census.sh validate --file --today 2026-10-26` on both extracted blobs (exit 1, E11-mirror + W04 only); `git rev-parse/diff --numstat/diff/log/show/cat-file/merge-base --is-ancestor/for-each-ref/branch --contains/status --porcelain` in the lane and `git -C /home/vgpnk/Projects/shokunin status/log` for the validator; `grep`/`awk`/`sed -n`/`sha256sum`. No write outside this report file; scratch removed.
