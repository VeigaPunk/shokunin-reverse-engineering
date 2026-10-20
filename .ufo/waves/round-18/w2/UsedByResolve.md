HOLDS

# UsedByResolve: do mined-row `used-by` paths resolve at REV? (round 18, wave 2, author-side advisory)

Scope: every `mined` row in `REV:corpus/SOURCES.md`, every comma-separated `used-by` path, tested with `git cat-file -e REV:<path>`.
REV `b2aad08ceeee8dd125ce0d316056d8bd766c7f94`; baseline `9011581d84527ba34c675f9cf912e54d2e72d470`; intermediate `eb6c2668e5cb7054fd1e16d2f615cb65586d0fe0`.
Labels: **OBS** means I observed it in command output. **INF** means inference.

## Verdict basis

- **OBS:** `REV:corpus/SOURCES.md:7-42` holds 36 rows, S001–S036. 34 are `mined`. S022 (`:28`) and S028 (`:34`) are `rejected`.
- **OBS:** The mined rows produce 65 (row, path) pairs over 12 distinct paths. For all 65, `git cat-file -e` exits 0. All are `100644 blob`. **Missing: none.**
- **OBS:** Two separate parsers agree: a Python cell split (11 cells on every row) and the `CORPUS.md:147` awk rule (`NF==13`, split on `[,;]`). No `used-by` cell contains `;`.
- **OBS:** Each of the 65 files contains its row's id at REV (`git grep -c -w <id>` ≥ 1). So `CORPUS.md:103` ("`mined` (cited by ≥1 path in `used-by`)") holds for all 34 mined rows.
- **OBS:** No commit in baseline..REV has a dangling `used-by`. At `9011581` and `eb6c266`: 32 rows, 58 pairs, 0 missing. At REV: 36 rows, 65 pairs, 0 missing. `eb6c266` does not touch `corpus/` or `SKILL.md`. REV adds `corpus/knowledge/2026-10-20-r18-swiss-map-replay.md` and `corpus/lessons/round-18.md` in the same commit that adds the rows citing them, so the round-15 "premature used-by" mistake does not recur.
- **OBS:** The fleet validator on a pristine REV checkout prints `ok`, exit 0.

Confidence in the verdict: high. It rests on two parsers, the fleet validator, and a red test showing the check can fail.

## Commands and exit codes

All run in `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` unless noted. `REV=b2aad08ceeee8dd125ce0d316056d8bd766c7f94`.

1. `git cat-file -e $REV && echo REV_EXISTS` → `REV_EXISTS`, exit 0.
   `git rev-parse HEAD` → REV. `git log -1 refs/heads/main` → REV.
2. Main check, exit 0, last line `pairs=65 missing=0`:

   ```sh
   git show $REV:corpus/SOURCES.md | awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF==13 {s=$9; gsub(/[[:space:]]/,"",s); if (s=="mined") {id=$2; gsub(/[[:space:]]/,"",id); n=split($12, a, /[,;]/); for (j=1;j<=n;j++) {p=a[j]; gsub(/^[[:space:]]+|[[:space:]]+$/,"",p); if (p!="" && p!="—") print id, p}}}' | { pairs=0; miss=0; while read -r id p; do pairs=$((pairs+1)); git cat-file -e "$REV:$p"; rc=$?; [ $rc -ne 0 ] && miss=$((miss+1)); printf '%s %s cat-file-e=%s type=%s cites=%s\n' "$id" "$p" "$rc" "$(git cat-file -t "$REV:$p" 2>&1)" "$(git grep -c -w "$id" $REV -- "$p" | awk -F: '{print $NF}')"; done; echo "pairs=$pairs missing=$miss"; }
   ```

   Every row printed `cat-file-e=0 type=blob cites>=1`.
   - Citation-line counts range from 1 to 8. Many pairs sit at 1, for example S002 `round-13.md`, S036 `SKILL.md` (`REV:SKILL.md:570`), S003 `round-17.md` and S023 in the r17 entry.
   - The maximum, 8, is S003 `round-16.md` and S024 `round-17.md`.
3. Each distinct path, `git cat-file -e $REV:<path>`, all exit 0:

   | path | rows |
   |---|---|
   | `SKILL.md` | S036 |
   | `corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md` | S001 S003 S004 S007 |
   | `corpus/knowledge/2026-10-20-r15-go-snapshot-inventory.md` | S003 S007 S023 |
   | `corpus/knowledge/2026-10-20-r16-go-selection-preview.md` | S003 S023 |
   | `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md` | S003 S023 S024 S025 S026 S029 S031 S032 |
   | `corpus/knowledge/2026-10-20-r18-swiss-map-replay.md` | S034 S035 |
   | `corpus/lessons/round-13.md` | S001–S021 |
   | `corpus/lessons/round-14.md` | S001 S003 S004 S007 S017 S018 |
   | `corpus/lessons/round-15.md` | S003 S007 S023 |
   | `corpus/lessons/round-16.md` | S003 S023 |
   | `corpus/lessons/round-17.md` | S003 S024 S025 S026 S027 S029 S030 S031 S032 |
   | `corpus/lessons/round-18.md` | S033 S034 S035 S036 |

4. `git ls-tree $REV -- <the 12 paths>`: all `100644 blob`, exit 0.
   `git diff --quiet $REV -- SKILL.md corpus/`: exit 0. The working tree equals REV for these paths, so a disk-based census in the lane agrees.
5. The same awk loop at each commit. Exit 0; 0 missing at each.
   - `9011581`: `rows=32 mined_pairs=58`
   - `eb6c266`: `rows=32 mined_pairs=58`
   - REV: `rows=36 mined_pairs=65`
6. `git diff --name-status eb6c266 $REV -- corpus/SOURCES.md corpus/lessons/round-18.md corpus/knowledge/2026-10-20-r18-swiss-map-replay.md SKILL.md` → `M SKILL.md`, `M corpus/SOURCES.md`, `A …r18-swiss-map-replay.md`, `A corpus/lessons/round-18.md`, exit 0.
   `git diff --name-status 9011581 eb6c266 -- corpus/ SKILL.md` → empty, exit 0.
7. Fleet validator on a pristine REV checkout:
   - Setup: `git clone -q --no-local --no-checkout <lane> $T/kaidoku-shokunin`, then `git remote remove origin` (`remote -v` empty), then `checkout --detach $REV`. `$T` came from `mktemp -d`.
   - `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate $T/kaidoku-shokunin` → `W04 S033 duplicate url …pull/9348 across scopes` and `ok`, exit 0. W04 is a warning that S033 and S032 share the PR URL; it is not about `used-by`.
   - `CORPUS.md:147` run verbatim from the clone root: no output, exit 0.

## Red test: the check can fail, and where it can't

All of this ran in the throwaway clone, as local commit `31b3a91c98dbd6df0b5e6255cf9be4d98349c1e7`.
- Mutation 1: appended `corpus/knowledge/2026-10-20-r18-MISSING.md` to S034.
- Mutation 2: appended the directory `corpus/lessons` to S036.

| case | `git cat-file -e` | fleet `validate` |
|---|---|---|
| missing file | exit 128, counted `missing=1` | `E11 S034 missing used-by …MISSING.md`, exit 1 |
| directory path | exit 0; `cat-file -t` says `tree` | silent (no E11) |
| file untracked on disk, absent from the commit | exit 128 ("exists on disk, but not in '31b3a91…'") | `ok`, exit 0 |

- **OBS:** Neither `git cat-file -e` nor E11 (`[ ! -e "$dir/$path" ]` at `scripts/sources-census.sh:566`) rejects a directory. Only `cat-file -t` or a blob check does.
- **OBS:** E11 reads the disk, not a revision. An untracked file satisfies it.
- **OBS (REV impact: none):** all 65 targets are tracked blobs, and the lane tree is clean for them (command 4).

## Adjacent findings (outside the literal existence target; they do not change the verdict)

### F1 — The r18 knowledge entry is missing from three rows' `used-by`

- **OBS:** `REV:corpus/knowledge/2026-10-20-r18-swiss-map-replay.md:1` (`source:`) cites S034, S035, S023, S003 and S033. S023 appears again at `:21`, S033 at `:107`.
- **OBS:** Only S034 (`REV:corpus/SOURCES.md:40`) and S035 (`:41`) list the entry. S003 (`:9`), S023 (`:29`) and S033 (`:39`) do not.
- **OBS:** The same check finds 0 gaps for the r14, r15, r16 and r17 entries. Round 18 is the first knowledge entry whose `source:` rows omit it.
- **OBS:** `CORPUS.md:107` defines `used-by` as "repo-relative paths of the knowledge entries or lessons citing the row". `REV:SKILL.md:550` lists the entry's sources as "(S034/S035/S023/S003/S033)".
- **OBS:** `REV:corpus/lessons/round-18.md:42` records "No in-place S001–S032 cell changed". Previous rounds appended in place and logged it (`REV:corpus/lessons/round-17.md:72-73`).
- **OBS:** No wave-1 report at REV proposes this append. The matching lines from `git grep used-by` over `.ufo/waves/round-18/` (json and py excluded) are `w1/ConnCorrectionPlacement.md:151`, `w1/ConnSourcesPaths.md:68,99`, `w1/DraftS033Row.md:14-15` and `w1/SimplifyRoutedDefects.md:82`. The draft row at `w1/DraftS033Row.md:10` sets S033's `used-by` to `corpus/lessons/round-18.md` only.
- **INF:** This looks like an omission, not a decision. S033 is the clearest case: it is a new row from the same round whose siblings S034/S035 list the entry.
- **INF (impact):** Anything that reads `used-by` to find a row's dependents misses this entry, for example a recheck of S003 or S023. The Rule 4 expansion count reads `source:` (`CORPUS.md:124`), so it is unaffected.
- Confidence: high on the observation; medium that it violates the contract, since that depends on reading `CORPUS.md:107`.
- Reproduce (exit 0; prints `S003 SOURCES.md:9 NOT-listed`, `S023 …:29 NOT-listed`, `S033 …:39 NOT-listed`, then S034 and S035 `listed`):

  ```sh
  F=corpus/knowledge/2026-10-20-r18-swiss-map-replay.md; for id in $(git show "$REV:$F" | sed -n '1p' | grep -oE '\bS[0-9]{3}\b' | sort -u); do printf '%s SOURCES.md:%s %s\n' "$id" "$(git show $REV:corpus/SOURCES.md | grep -nE "^\| $id \|" | cut -d: -f1)" "$(git show $REV:corpus/SOURCES.md | grep -E "^\| $id \|" | awk -F'|' -v f="$F" '{print (index($12,f)?"listed":"NOT-listed")}')"; done
  ```

- Fix (proposal, not applied):
  - Append the entry path to the `used-by` cells of S003, S023 and S033.
  - Log each change old→new in the round-18 lesson (Rule 2, `CORPUS.md:116-118`), with an appended correction to the claim at `:42`.
- A weaker case of the same gap: `REV:corpus/lessons/round-18.md:10` cites S023, S003 and S033 for C3, but S003 and S023 do not list `round-18.md`. The lane has accepted this pattern before: the round-17 CensusRun residual for S023 and `round-17.md:73`.
- Full reverse sweep (Python over `corpus/lessons` and `corpus/knowledge` at REV): 39 (file, id) mentions are not reflected in `used-by`.
  - Only 8 are in files new at REV: the r18 entry (S003, S023, S033) and `round-18.md` (S001 range mention at `:42`, S003/S023 at `:10`, S031 at `:25`, S032 at `:8,24,42,56`).
  - The other 31 predate this round. The same sweep at baseline `9011581` gives exactly 31, and all 31 persist at REV (0 baseline-only). They are verifier-spotcheck lessons (never listed), `round-14.md:55` S005/S006, and `round-17.md:73` S023.

### F2 — `SKILL.md` in S036's `used-by` doesn't fit the contract (low)

- **OBS:** `REV:corpus/SOURCES.md:42` has S036 `used-by` = `corpus/lessons/round-18.md, SKILL.md`. This is the only `used-by` path at REV outside `corpus/lessons/` and `corpus/knowledge/`. `CORPUS.md:107` limits `used-by` to knowledge entries and lessons.
- **OBS:** `REV:SKILL.md` cites 15 rows: S001 S003 S004 S007 S023 S024 S025 S026 S029 S031 S032 S033 S034 S035 S036. Only S036 lists it.
- Either `SKILL.md` counts as a user, and then 14 rows are incomplete, or it doesn't, and then S036's entry is out of contract.
- Existence and `mined` status hold either way. The file exists, cites S036 at `:570`, and `round-18.md` independently cites S036.
- Reproduce: `git show $REV:corpus/SOURCES.md | awk -F'|' '/^\| S[0-9]{3} \|/ {gsub(/ /,"",$2); n=split($12,a,/,/); for(j=1;j<=n;j++){p=a[j]; gsub(/^ +| +$/,"",p); if (p !~ /^corpus\/(lessons|knowledge)\//) printf "%s:%s ", $2, p}}'` → `S036:SKILL.md`, exit 0.

## Provenance and housekeeping

- Fleet files cited: `CORPUS.md:103,107-108,116-118,124,147` and `scripts/sources-census.sh:562,566-567`.
  - Both are clean at fleet HEAD `2618bfb6641e245b0044644944c91ed6adb92fa3` (`git diff --quiet HEAD -- …` exit 0).
  - Fleet HEAD moved from `d21e61f5…` during the session. Neither file changed between the two (`diff --quiet` exit 0).
- Writes outside this report:
  - The mkdtemp clone `/tmp/usedby-r18.9QsZpD`. Origin was removed before checkout; it held one local red commit and one untracked red file.
  - One scratch dump, `/tmp/k18_sources_rev.md` (`git show REV:corpus/SOURCES.md`). It falls outside "report only"; I am disclosing it here.
  - Both were deleted: `ls` → "No such file or directory".
- Nothing was written in the lane except this report. No `jj` and no git write in the lane. No REA or Ghidra. No installs or upgrades.
- Open questions:
  - Is `SKILL.md` an intended `used-by` target? `CORPUS.md` says nothing beyond `:107`.
  - Does a mention in a lesson's Claims line count as "citing" for `used-by`? Lane precedent is mixed.
