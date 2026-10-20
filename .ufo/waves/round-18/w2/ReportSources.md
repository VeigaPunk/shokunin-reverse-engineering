PARTIAL — the headline numbers hold exactly at both revisions from Git objects: rows 32→36, tiers A28/B3/C1→A31/B4/C1, status mined30/rejected2→mined34/rejected2, census and validate exit 0, and S001–S032 are byte-identical. Four things are wrong or incomplete. (1) At REV, validate does not produce the same output as at B: it adds a W04 line. (2) S003, S023 and S033 omit the r18 knowledge entry from their `used-by`, even though the entry's `source:` line cites all three. (3) S003 is cited outside its registered scope. (4) The search log declares 7 exclusions but names only 6 groups.

# ReportSources — round 18, wave 2: draft of "Sources & frontier"

Seat: `KaidokuR18.ReportSources`, a scribe on the author side (advisory only). REV is `b2aad08ceeee8dd125ce0d316056d8bd766c7f94` and B is `9011581d84527ba34c675f9cf912e54d2e72d470`. Lane HEAD = REV, and the worktree has 0 tracked modifications (`git status --porcelain --untracked-files=no | wc -l` → 0). Every lane `path:line` below is therefore the REV blob (`git show REV:path`). Fleet-repo files (`CORPUS.md`, `scripts/sources-census.sh`, the r17 report) are cited at their on-disk lines. This file is the only thing I wrote.

Axes: calibration (do the numbers and tiers match the registry?), operability (can each line be reproduced with one command?), depth (forward and reverse used-by, scope, anchors).

## Draft

### Sources & frontier

- **Census commands, run from Git objects** (`git archive <rev> -- corpus SKILL.md` into mkdtemp, then `scripts/sources-census.sh census|validate <dir>`):
  - Round start, B `9011581`: census gives rows 32, tier A28/B3/C1, status mined30/rejected2, exit 0. Validate gives `ok`, exit 0.
  - Round end, REV `b2aad08`: census gives rows 36, tier A31/B4/C1, status mined34/rejected2, exit 0. Validate gives `W04 S033 duplicate url github.com/NationalSecurityAgency/ghidra/pull/9348 across scopes` and then `ok`, exit 0.
    - A W-code never changes the exit status (`scripts/sources-census.sh:16,33`).
    - The W04 comes from S033 narrowing its scope relative to S032 (finding F1). It is not an E04: S033's teaches cell opens `supersedes S032 —` (`scripts/sources-census.sh:646-649`).
  - The frozen census (`CORPUS.md:134-147`, extracted verbatim) at B and REV gives the same counts, with 0 malformed rows, no duplicate ids, no enum or tier-inflation hits, and no missing used-by paths.
  - The end run will also be retained as verify label `sources-census` (`.ufo/waves/round-18/verify.py:250-252`). That run is validate mode on the working tree, so it does not retain these histograms (F6).
- **Rows:** 32 → 36 (`corpus/lessons/round-18.md:43`).
  - Tiers: A28/B3/C1 → A31/B4/C1.
  - Status: mined30/rejected2 → mined34/rejected2. No row is queued.
- **Rows added, by tier.** All four were opened 2026-10-20. Their quotes are recorded in `corpus/lessons/round-18.md:30-38`: 5 quotes of 4–25 words.
  - **A:**
    - S034, Go 1.24 Release Notes `#runtime` (docs), `corpus/SOURCES.md:40`.
    - S035, go1.24.6/go1.25.0 `internal/abi` map descriptors (code), `corpus/SOURCES.md:41`. Its anchor digests and lines reproduce locally.
    - S036, jj 0.45.1 Git compatibility (docs), `corpus/SOURCES.md:42`.
  - **B:** S033, Ghidra PR #9348 at head `a214355…` (community), `corpus/SOURCES.md:39`. Its teaches cell opens `supersedes S032 —`, and its anchor keeps the page digest as fetch-time only (`.ufo/waves/round-18/evidence/s032-digests.json`).
- **Rows changed in place (old→new): none.**
  - S001–S032 are byte-identical between B and REV.
  - S032 is logged `mined → mined, used-by unchanged` (`corpus/lessons/round-18.md:42`).
  - If the L1 applies F2, this line becomes: "S003, S023 `used-by` appended `corpus/knowledge/2026-10-20-r18-swiss-map-replay.md`", logged old→new under `corpus/lessons/round-18.md:40`.
- **Paths: 8 → 10.**
  - The route-diagnosis path drops S032 (B `corpus/SOURCES.md:44` → REV `:48`).
  - Added `Swiss-map replay — S034 → S035 → S023 → S003 → S033` (`:49`).
  - Added `Revision pins under jj — S036` (`:50`).
- **Search log:** one entry added (`corpus/SOURCES.md:67`). It reports identified 11, screened 11, included 4 (S033–S036), excluded 7. F4 disputes the 7.
- **Frontier advanced:**
  - The r17 aether lead S032 was keyed on a rendered-page digest that does not reproduce. It is now re-anchored as S033, on title, state, head commit and a byte-stable `.patch` digest (`corpus/SOURCES.md:39`).
  - Two study paths were added (`:49-50`).
  - Leads went 5 → 7. None of B's 5 leads was resolved (B `:63-67` = REV `:71-75`), and 2 were added (`:76` gore v0.14.7 Swiss parser, `:77` jj revsets/bookmarks).
  - Carried open: the r12 C1 entry still has no `S###` row (`corpus/lessons/round-18.md:73-75`).
  - LOG records the C3 mechanism as `confirmed` under the frozen rule (`LOG.md:2150-2158`). That is the author's record; this seat did not re-verify it.
- **Sourced claims** (`.ufo/waves/round-18/claims.json:40`):
  - C1 rests on S033, C2 on S036, and C3 (the filed sourced claim) on S034/S035.
  - The C3 entry's `source:` line also cites S023, S003 and S033 (`corpus/knowledge/2026-10-20-r18-swiss-map-replay.md:1`).
  - "Opened this round" is shown by the Git diff (S033–S036 are absent at B), not by the `opened` cell (F5).
- **Mined mistakes:** `corpus/lessons/round-18.md:58-69`, ## Mistakes, 8 rows. Three are marked "this round".

## Findings (each with a reproducing command; labels O = observation, I = inference)

**F1. Validate output changed between the two revisions (disclosure only).**
- [O] B prints only `ok`. REV prints a `W04` line for S033 and then `ok`. Both exit 0.
- [O] I copied REV into /tmp and set S033's scope cell equal to S032's. Validate then printed only `ok`, exit 0, so the scope rewording alone causes the W04. The E04 is suppressed by `supersedes S032` (`scripts/sources-census.sh:645-649`).
- [I] The narrower scope ("a lead, not a mechanism proof") is a calibration gain, not a defect.
- Consequence: r17's wording "Round end: same output" (`/home/vgpnk/Projects/shokunin/.ufo/reports/round-17/kaidoku.md:72`) must not be reused. The draft names the W04 line.

**F2. `used-by` is incomplete for the new knowledge entry (low–medium).**
- [O] The entry's `source:` line (`corpus/knowledge/2026-10-20-r18-swiss-map-replay.md:1`) cites S003, S023, S033, S034 and S035.
  - Only S034 and S035 list the entry in `used-by`.
  - S003 (`corpus/SOURCES.md:9`), S023 (`:29`) and S033 (`:39`) omit it.
- [O] Precedent: in the same situation, r17 appended its entry to S003 and S023 (r17 report `:77`; B's S003 and S023 cells list `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md`).
- [O] The rules allow the fix: `CORPUS.md:107-108` defines `used-by` as the citing knowledge entries or lessons, `CORPUS.md:116-117` allows in-place `used-by` changes that are logged old→new, and `contract.md:143-144` lets controls change `used-by` on S001–S032.
- [O] Reverse audit over Git objects: file/row pairs where a corpus file (or SKILL.md) cites a row but is missing from that row's `used-by` went 42 → 53. 11 are new and 0 disappeared:
  - 3 are this entry.
  - 5 are the round-18 lesson. S001 (`:42`), S031 (`:25`) and S032 (`:42`) appear only in gate-log mentions, which by r14 precedent do not require listing (`.ufo/waves/round-17/w2/CensusRun.md:51-56`). S003 and S023 at `:10` are claim-level mentions.
  - 3 are SKILL.md citing S033–S035 (`SKILL.md:528,550`).
- [O] S036 alone lists `SKILL.md` (`corpus/SOURCES.md:42`). At B, no row listed SKILL.md.
- [I] SKILL.md is neither a knowledge entry nor a lesson, so `CORPUS.md:107` does not cover it, and the convention is now inconsistent.
- Validate and census cannot see any of this: E11 only checks that a listed path exists.
- Fix (L1):
  - Append the entry to S003, S023 and S033.
  - Log old→new at `corpus/lessons/round-18.md:40-43`.
  - Either drop `SKILL.md` from S036 or add it to S033–S035.
  - Census counts do not change.

**F3. S003 is cited outside its scope (low–medium).**
- [O] S003's scope cell is "Installed Ghidra 12.1.4 Go RTTI version gate and snapshot bootstrap behavior". Its anchors are `GoRttiMapper.java:79` and `GoApiSnapshot.java:get` (`corpus/SOURCES.md:9`).
- [O] Round 18 cites S003 for map-type reading instead:
  - in `corpus/SOURCES.md:49` ("the installed reader reads at the bound struct's end");
  - in the entry's `:1`: `GoMapType.java:32-34`, `GoType.java:137-149`, `GoName.java:79-126`, `GoRttiMapper.java:1053-1075` and `MemoryByteProvider.java:302,312`.
- [O] `CORPUS.md:93,98` say tier applies to the stated scope, never globally.
- [O] Wave 1 flagged this case: `w1/ConnSourcesPaths.md`, "Conditional variants", says to keep S003 out of this path. The integrated path includes it anyway.
- [I] No tier-A judgment is registered for the map-reader use.
- Fix:
  - Either add a new row scoped to the installed 12.1.4 Go type readers with those anchors (rule 2, `CORPUS.md:116-118`, forbids changing S003's scope in place; a local-path source triggers no W04),
  - or drop S003 from `:49` and cite the reader lines as tool basis.

**F4. Search-log ledger count (low).**
- [O] `corpus/SOURCES.md:67` declares "excluded 7 as rows" but names only 6 top-level groups:
  1. go1.25 notes
  2. jj `latest` docs
  3. jj revsets/bookmarks and config defaults
  4. git docs
  5. gore Swiss parser
  6. Ghidra master
- [O] "GoReSym v3.4.1" appears under "Where searched" but has no disposition.
- [I] 4 + 7 = 11 works only if one group counts twice. This is the r17 count-defect class (`w1/ConnSourcesPaths.md`, count ledger). `CORPUS.md:126-128` requires the counts to come with exclusion reasons.
- Fix: list the exclusions 1:1 and give GoReSym v3.4.1 a disposition.

**F5. "Opened this round" cannot be read from the `opened` cell (info).**
- [O] 14 rows carry `opened` 2026-10-20 at REV (S023–S036); B had 10. The date cannot tell round 17 from round 18.
- Round membership is the Git diff.

**F6. The after-census histograms are not retained at REV (info / operability).**
- [O] REV has no round-18 verification record. `SCORECARD.md:2433-2434` defers measured values to a later step.
- [O] `verify.py:250-252` runs `validate` only. It is guarded by revpin `:92` and the tracked-clean check `:101`.
- Fix: retain census-mode output at close, or cite this report's command.

**Claims that hold:**
- `claims.json:31` frontier_step: before exit 0 with 32 rows; after exit 0; new rows carry gate quotes; mistakes are mined; C1–C3 cite this round's rows. One caveat: `w1/CriticSourcedClaim.md:34-37` notes that S033 re-opens an r17 subject.
- `corpus/lessons/round-18.md:42-43`.
- `LOG.md:2164`.
- The S035 anchors (`map_swiss.go:32`, `map_noswiss.go:25`, `map_select_swiss.go:5,22`, `type.go:358-363`): their three sha256 values match, and 1.24.6 is byte-identical.

## Commands and exit codes

Shorthand: `L=/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, `S=/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`, `R=b2aad08…`, `B=9011581…`.

```
git -C $L rev-parse HEAD                                             # b2aad08…  exit 0
git -C $L status --porcelain=v1 --untracked-files=no | wc -l         # 0         exit 0
for rv in $B $R; do d=$T/${rv:0:7}/kaidoku-shokunin; mkdir -p $d; git -C $L archive $rv -- corpus SKILL.md | tar -x -C $d
  bash $S census $d; bash $S validate $d; done                       # B: 32/A28 B3 C1/mined30 rej2, ok; R: 36/A31 B4 C1/mined34 rej2, W04+ok; all exit 0
bash $S validate --root /home/vgpnk/Projects/shokunin kaidoku        # W04 S033 … ; ok   exit 0 (worktree = REV)
bash $S census   --root /home/vgpnk/Projects/shokunin kaidoku        # rows 36 … FLEET missing 0   exit 0
sed -n 134,147p /home/vgpnk/Projects/shokunin/CORPUS.md > frozen.sh  # sha256 0af57265…6a; (cd <archived B|R> && bash frozen.sh) → 32|36, 0, tiers, status; exit 0 both
diff <(grep -E '^\| S0(0[1-9]|[12][0-9]|3[0-2]) ' B-blob) <(… R-blob)   # no output, exit 0 (32 rows each)
python3 -I -B ReverseAudit.py (body below)                           # reverse pairs base 42 rev 53 new 11 gone 0   exit 0
git -C $L show $R:corpus/knowledge/2026-10-20-r18-swiss-map-replay.md | sed -n 1p | grep -oE 'S0[0-9]{2}' | sort -u   # S003 S023 S033 S034 S035  exit 0
git -C $L show $R:corpus/SOURCES.md | awk -F'|' '$2 ~ /S0(03|23|33|34|35) / {print $2, ($12 ~ /r18-swiss-map-replay/ ? "lists-entry" : "OMITS-entry")}'   # S003/S023/S033 OMITS; S034/S035 lists  exit 0
git -C $L show $R:corpus/SOURCES.md | sed -n 9p | cut -d'|' -f6       # S003 scope (version gate + bootstrap)  exit 0
W04 probe: copy of REV with S033 scope := S032 scope; bash $S validate <copy>   # ok only, exit 0
python3 -I -B: count top-level groups after "excluded 7 as rows:" on SOURCES.md:67   # declared 7, named 6; GoReSym searched, undispositioned  exit 0
sha256sum go-1.25.0/…/abi/{map_swiss,map_noswiss,map_select_swiss}.go go-1.24.6/…/abi/{map_swiss,map_noswiss}.go   # match S035 anchor  exit 0
awk opened==2026-10-20 over B and R SOURCES                         # B 10 rows, R 14 rows  exit 0
git -C $L show $R:.ufo/waves/round-18/verify.py | grep -nE 'sources-census|porcelain|resolve_source'   # :250, :101, :11/:92  exit 0
```

`ReverseAudit.py`, run verbatim through stdin (`python3 -I -B - <<'PY' … PY`); it reads Git objects only:

```python
import re,subprocess
L='/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
def show(rev,p): return subprocess.run(['git','-C',L,'show',f'{rev}:{p}'],capture_output=True,text=True,check=True).stdout
def ls(rev): return subprocess.run(['git','-C',L,'ls-tree','-r','--name-only',rev,'--','corpus','SKILL.md'],capture_output=True,text=True,check=True).stdout.split()
def audit(rev):
    rows={}
    for l in show(rev,'corpus/SOURCES.md').splitlines():
        if re.match(r'^\|\s*S\d{3,}\s*\|',l):
            c=l.split('|'); rows[c[1].strip()]=[p.strip() for p in c[11].split(',')]
    out=set()
    for p in ls(rev):
        if not p.endswith('.md') or p=='corpus/SOURCES.md': continue
        for i in set(re.findall(r'(?<![A-Za-z0-9_])S\d{3}(?![0-9])',show(rev,p))):
            if i in rows and p not in rows[i]: out.add((p,i))
    return out
b=audit('9011581d84527ba34c675f9cf912e54d2e72d470'); r=audit('b2aad08ceeee8dd125ce0d316056d8bd766c7f94')
print('reverse pairs base', len(b), 'rev', len(r), 'new', len(r-b), 'gone', len(b-r))
for x in sorted(r-b): print('NEW', *x)
```

## Touched surfaces, out of scope, tooling

- **Written:** this file only. All scratch under `/tmp/r18*` was removed (exit 0). No lane file was edited, no `jj` was run, no git write was made, and nothing ran in the fleet repo outside this path.
- **Out of scope / not done:**
  - No network re-fetch of S033, S034 or S036 digests.
  - No C3 verdict check.
  - No `controls.py` run (S001–S032 identity was shown by diff instead).
  - No REA, no Ghidra, no carrier execution.
- **Tools:** git (read-only show/archive/ls-tree/diff/status/rev-parse/log/cat-file), gawk, grep, sed, sha256sum, and `python3 -I -B` with the standard library only.
- **Installs or upgrades:** none.
