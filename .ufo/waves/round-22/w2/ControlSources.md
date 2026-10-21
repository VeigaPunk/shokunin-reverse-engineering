# ControlSources — no-harm control: prior-50 SOURCES rows byte-preserved + current census/histogram

seat: `KaidokuR22R.ControlSources-6` (w2 reviewer, leaf)
lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` (read-only; this report + `.json` are my only writes)
baseline `B = 7787fea4d6fd718726de92ed20759d11ce7b8b48`; branch `main`; HEAD at observation `2ee3d9f51c6a995d1aefe48f6a44cfd08d492d67` ("round-22: retain static frontier evidence and calibrated catalog dispositions")
axes: coverage (R22-C1 counts SOURCES rows S≥51 via `count-c1.py`) and calibration (census W/E codes must stay honest — warnings disclosed, never silenced). This is a no-harm control for both.

**Final revision does not exist.** All results below are at-snapshot observations, not final-after claims. Snapshots: file sha256 `7810a6a773ab0ef70ccf4b61d403e93f0066a7c44c7a19e1ff0a025ac4d56866` at 2026-10-21T13:10Z, unchanged on re-read at 13:10:54Z.

## Scope note — what "prior50" is

`corpus/SOURCES.md` registry: **50 rows (S001–S050) at B**, 53 at HEAD `2ee3d9f`, **54 in the live working tree** (L1 appended S054 unstaged mid-review, ~13:0xZ). `git status --porcelain corpus/SOURCES.md` → ` M`, `git diff --numstat` → `1 0` (one unstaged insertion). No row was re-checked across commits before baseline extraction; B's blob is `54a4e98`, staged blob `7a420311` (= HEAD), worktree hash `3b58ca383f44439d385dc6c302a51c9eac78590c`.

## Commands run (verbatim) and observed output

```sh
git diff --stat 7787fea4d6fd718726de92ed20759d11ce7b8b48..HEAD -- corpus/SOURCES.md
# corpus/SOURCES.md | 5 +++++   (1 file changed, 5 insertions(+), 0 deletions)
```
```sh
diff <(git show 7787fea4d6fd718726de92ed20759d11ce7b8b48:corpus/SOURCES.md | grep -oP '^\| S0(?:0[1-9]|[1-4][0-9]|50) .*') \
     <(grep -oP '^\| S0(?:0[1-9]|[1-4][0-9]|50) .*' corpus/SOURCES.md); echo $?
# 0   — every baseline row S001–S050 byte-identical AND position-preserved (lines 7–56) in the live worktree file
```
```sh
git show 7787fea…:corpus/SOURCES.md | grep -oP '^\| S0(?:0[1-9]|[1-4][0-9]|50) .*' | sha256sum
grep -oP '^\| S0(?:0[1-9]|[1-4][0-9]|50) .*' corpus/SOURCES.md | sha256sum
# both: 1ff20543bc3de1fc67a464cde417400f1085250ce4c9bab44c066b1ff3a59ad5
```
```sh
git diff 7787fea4d6fd718726de92ed20759d11ce7b8b48 -- corpus/SOURCES.md | grep -c '^-[^-]'
# 0 content deletions B→worktree. Whole-file diff = pure additions:
#   4 registry rows (S051–S054), 1 "## Paths" bullet, 1 "## Search log" bullet.
```
```sh
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file corpus/SOURCES.md; echo exit=$?
# file  W04  S033 duplicate url github.com/NationalSecurityAgency/ghidra/pull/9348 across scopes
# file  W04  S047 duplicate url go.dev/dl/?mode=json&include=all`, across scopes
# file  W04  S054 duplicate url developer.android.com/ndk/guides/abis across scopes
# file  ok   /home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md
# exit=0
```
Histogram (parse: `re.match(r"^\|\s*S\d{3}\s*\|")` over `git show REV:corpus/SOURCES.md`, fields 4/8 0-indexed from `|` split):

| rev | rows | tiers | status | kinds |
|---|---|---|---|---|
| B | 50 | A44 B5 C1 | mined48 rejected2 | — |
| worktree | 54 | A48 B5 C1 | mined52 rejected2 | code13 community4 dataset4 docs20 own-work2 paper5 spec3 tool3 |

`ids=S001..S054 seq_ok=True`.

## Findings

1. **Prior-50 rows preserved — PASS at snapshot, stronger than the canonical check.** Zero diff between B's 50 registry rows and the worktree's first 50 rows, at identical line positions (7–56). Order, ids, every cell byte-identical. `verify.py:69-73` (canonical run logic) implements this only as `old_rows_identical = all(row in new for row in old)` — a membership test that would not catch reordering. The stronger position-preserved invariant above is what L1 should keep: `diff` of the two row streams must be empty, not merely subset-equal.
2. **Whole file is append-only B→worktree.** The only `+` lines are rows S051–S054, one Paths bullet (`Static Flutter APK evidence — S052 → S051 → S053`), one Search-log bullet (round-22 recovery). No `## Paths`/`## Search log`/`## Leads` prior line was edited or dropped.
3. **Census exit 0; W04 set grew to 3.** New W04 `S054` (supersedes S052, same `developer.android.com/ndk/guides/abis` URL, different scope text → "across scopes", not E04 duplicate URL+scope). Same precedent as baseline warnings S033 (supersession of S032's PR URL) and S047 (S038's index URL). Invariant: final census `validate` exits 0 with W04 ⊆ {S033, S047, S054}; any additional code or any `E` line = defect. Calibration-relevant: S054's warning must be *disclosed* (as S033/S047 were), not hidden — the lane keeps the rejected/superseded row rather than rewriting it.
4. **S054 is uncommitted and counter-invisible — expected, flag for L1.** `count-c1.py:80-84` reads `git show REV:corpus/SOURCES.md` and counts only committed `S≥51`/`mined`/`opened=2026-10-21` rows; `verify.py:67-73` likewise evaluates `--rev` blobs for rows but runs the census script against the live worktree (`--root … kaidoku`). Until L1 commits, `rows(B)=50, rows(rev)=53` and `old_rows_identical` still passes; after committing S054 it must read `after=54`. Row S054 itself conforms: NF=13 (`E01` absent), id unique (`E03` absent), `docs`/`A`/`mined`/`2026-10-21`, used-by paths exist (`E11` absent).
5. **Search-log gap (observation, mid-flight):** the round-22 Search-log bullet covers `S051–S053` only; S054 has no log line and no `## Paths` bullet yet. Not a no-harm defect, but the curation step is visibly unfinished — L1 should land the S054 log line with the commit.
6. **Baseline had 2 queued→? none:** status histogram shows no `queued` anywhere (mined+rejected only); `sources-census` reports no E07. Malformed rows: 0.

## Invariants for L1 final-revision verification (rerun verbatim)

```sh
git diff 7787fea4d6fd718726de92ed20759d11ce7b8b48 -- corpus/SOURCES.md | grep -c '^-[^-]'   # must be 0
diff <(git show 7787fea4d6fd718726de92ed20759d11ce7b8b48:corpus/SOURCES.md | grep -oP '^\| S0(?:0[1-9]|[1-4][0-9]|50) .*') \
     <(grep -oP '^\| S0(?:0[1-9]|[1-4][0-9]|50) .*' corpus/SOURCES.md)                   # must be empty, exit 0
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file corpus/SOURCES.md  # exit 0; W04 ⊆ {S033,S047,S054}; zero E-lines
# row stream sha256 of prior 50 must stay 1ff20543bc3de1fc67a464cde417400f1085250ce4c9bab44c066b1ff3a59ad5
# final histogram may grow rows/append-only: rows≥54, tier/status deltas only from appended rows (A+4→A≥48, mined+4→≥52, B5/C1/rejected2 fixed unless new rows differ)
```

## Residual risk / verification gaps

- File is still live (unstaged S054); more rows may land — rerun all commands at final rev.
- `verify.py`'s `row in new` membership check is order-insensitive; a same-content reorder would pass it silently. L1's own check above is position-exact.
- No attempt made to verify S054's content against its source (URL liveness, quote) — outside this control's scope; the W2 `PrimaryAndroid` seat retains fetch checks per the row's anchor.

**Verdict (author-side, not admission):** at snapshot 13:10Z, the prior-50-row byte-preservation invariant holds exactly and the census is clean-with-disclosed-warnings (exit 0). No no-harm defect found in scope. Blocker to any stronger claim: the final revision does not exist; S054 is uncommitted and its Search-log line is not yet written.
