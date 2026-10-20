PARTIAL

# SearchLogAudit — round-18 search-log entry, `corpus/SOURCES.md:67`

Seat `KaidokuR18.SearchLogAudit`. Round 18, wave 2 (falsify). This is an author-side advisory seat. It is read-only, and this file is its only write.
REV is `b2aad08ceeee8dd125ce0d316056d8bd766c7f94`; baseline is `9011581d84527ba34c675f9cf912e54d2e72d470`. Every lane anchor is a line of `git show REV:<path>`.
I ran no REA, no Ghidra, no carrier, no `jj` and no git write, and installed nothing.

Axes:
- **Calibration:** do the four numbers rebuild from the entry's own named sources?
- **Operability:** can each count be re-derived with one command?
- **Depth:** do the w1 reports hold candidates that the entry does not account for?

## Verdict

- **Holds**
  - included = 4 is exact. The registry grows from 32 to 36 rows, and the four new rows are exactly S033–S036 (`SOURCES.md:39-42`).
  - identified = screened = 11, and 4 + 7 = 11.
  - Every included row traces to a w1 draft.
  - Five of the six written exclusion reasons are backed by evidence. I re-ran two of them myself.
- **Does not hold**
  - The exclusions cannot be rebuilt from the entry's text. Six reason clauses cover "excluded 7".
  - GoReSym v3.4.1 is in the entry's "Where searched" list but gets no disposition. Every grouping that makes 4 + 7 = 11 leaves GoReSym either as the 7th exclusion with no reason, or as a searched source that was never counted (F1).
  - The w1 reports also contain one drafted candidate row that the entry neither counts nor excludes (F2).

## Pins (observation)

- `git rev-parse HEAD` → `b2aad08c…`, exit 0. HEAD = REV.
- `git status --porcelain | wc -l` → 9, exit 0.
  - All nine entries are `??` round-18 wave-2 artifacts (`carriers/bin/`, `gen-wave2.py`, `w2/`, `wave2-*`).
  - No tracked file is modified, so the tracked bytes equal REV.

## What holds

| # | Check | Evidence | Label |
|---|---|---|---|
| H1 | included 4 = the new rows | Command 3 prints `32a33,36` and exactly `> \| S033` … `> \| S036`. `corpus/lessons/round-18.md:43` says "New rows S033–S036 … Rows 32 → 36". | observation |
| H2 | identified = screened, and 4 + 7 = 11 | Command 2 prints `('11', '11', '4', '7')`, range `S033`–`S036`. | observation |
| H3 | Each included row has a w1 source | S033 ← `w1/DraftS033Row.md:10`, `w1/ScoutPr9348Reopen.md:172`<br>S034 ← `w1/DraftGoNotesRow.md:11`, `w1/ScoutGo124NotesSwiss.md:60`<br>S035 ← `w1/ScoutAbiSwissLayout.md:102`. It also covers `w1/DraftAbiRow.md:10`, which drafts the same source and is correctly not counted twice.<br>S036 ← `w1/ScoutJjColocation.md:74`, `w1/ScoutJjRevsetsTrunk.md:207` | observation |
| H4 | "three L1 fetches, three digests" | `.ufo/waves/round-18/evidence/s032-digests.json`:<br>`:6-10` three distinct page digests<br>`:11-14` two equal `.patch` digests<br>`:15` `ls-remote` pull head | observation |
| H5 | Clauses 1, 2, 4, 5 and 6 are backed by evidence | **(1) go1.25 notes.** Re-fetched now: sha256 `c9d872d3…38fd`, which equals S031's recorded digest (`SOURCES.md:37`). The `swiss\|noswissmap` count is 0 (command 10). Also `w1/ScoutGo125MapsNotes.md:15`.<br>**(2) jj `latest` is 0.46 content.** `w1/ScoutJjColocation.md:11`.<br>**(4) "no lane claim rests on" git docs.** The only hit across `corpus/`, `SKILL.md`, the round-18 tools and the contract is `SOURCES.md:67` itself (command 5).<br>**(5) gore.** `w1/ScoutGoReSymSwiss.md:200-205`; lead at `SOURCES.md:76`.<br>**(6) Ghidra master supports Go 1.26 only.** `w1/ScoutGoReSymSwiss.md:17`. | observation. I re-ran (1) and (4); (2), (5) and (6) come from w1 observations. |

## Findings

### F1 — MEDIUM (calibration): GoReSym v3.4.1 has no disposition, so "excluded 7" cannot be rebuilt

**Observation.** `SOURCES.md:67` names "GoReSym v3.4.1" under "Where searched". It then gives six exclusion clauses for "excluded 7":

1. go1.25 notes
2. jj `latest` docs
3. jj revsets/bookmarks and config defaults
4. git docs
5. gore Swiss parser
6. Ghidra master

GoReSym is the only named source with no disposition. The parser prints `GoReSym where_searched=True exclusions=False`.

Both readings that close the arithmetic leave GoReSym without a disposition:

| How clause 3 is read | What the 7 exclusions are | GoReSym |
|---|---|---|
| One source (revsets/bookmarks/config) | clauses 1-6 + GoReSym | counted, **no reason** |
| Two sources (revsets/bookmarks; config), as w1 split them in `w1/ScoutJjRevsetsTrunk.md:12-13` | clauses 1-6, with clause 3 counted twice | **not counted**, although searched |

No reading gives every named source both a count and a reason. `/home/vgpnk/Projects/shokunin/CORPUS.md:126-128` (fleet HEAD `2618bfb6…`, file unmodified) requires both: "identified / screened / included / excluded counts, exclusion reasons".

**Observation.** w1 has a finding for GoReSym: v3.4.1 has no Swiss handling (`w1/ScoutGoReSymSwiss.md:16`; a tree-wide grep for `swiss` found no matches, `:88`). SOURCES.md records that finding nowhere.
- GoReSym appears at `:11`, `:36`, `:48`, `:65`, `:67` and `:73`.
- Only `:67` is round-18 text, and it is the bare where-searched mention.
- `:73` is unchanged. The baseline→REV diff adds only `:76-77` to Leads (command 9).

**Inference (likely cause).**
- S030 (`:36`) already covers GoReSym releases ("latest release `v3.4.1`"). GoReSym may have been treated as reuse of an existing row, the round-17 convention ("S003/S023 were reused, not re-counted", `:65`).
- But the same entry counts two other already-covered sources as exclusions: go1.25 notes, which is S031's own page (`:37`), and Ghidra master, which S029 covers (`:35`).
- The treatment is inconsistent under either reading.

No registry row or round claim depends on this gap (observation: `claims.json` amendments `sourced` cites only S033, S036, S034 and S035).

**Advisory repair (append-only):**
- Add one clause, for example "GoReSym v3.4.1 (no Swiss handling in the v3.4.1 tree; S030 covers the release)".
- State whether clause 3 counts as one candidate or two.

### F2 — LOW (depth/calibration): one w1-drafted candidate row is neither counted nor excluded

**Observation.** `w1/ScoutGo125MapsNotes.md:155` opens "Draft source row", and `:164` drafts an 11-cell row "Go 1.25.0 source tree, map-experiment selection". The row covers `buildcfg/exp.go`, `reflectdata/reflect.go`, `map_select_noswiss.go` and `runtime/map_noswiss.go`.

The w1 integration seat treated it as a separate candidate family:
- `w1/ConnSourcesPaths.md:66`: "S038 (optional)".
- `:84`: listed in `I-go`.
- `:87`: `EXC-go` expects "optional 1.25 row if not admitted", "each with a reason".

At REV, `buildcfg` and `reflectdata` appear neither in the where-searched list nor in the exclusions at `:67` (parser output). The list mentions only generic "toolchain trees". The admitted S035 row does not cover those files: command 7 counts 0 matches, exit 1.

So the candidate was neither admitted nor excluded with a reason.
- Command 4 finds 13 drafted 11-cell rows across 9 distinct source families.
- `:67` gives a disposition for 8 of those families. This one is the ninth.

**Inference (consistency with the entry's own convention).**
- The entry counts a release-notes page with 0 matches as identified and excluded (go1.25, clause 1).
- The same w1 sweep found 0 `swiss` matches in the go1.26 and go1.27 notes (`w1/ScoutGo125MapsNotes.md:70`).
- The integration skeleton listed both pages under "where searched" and `EXC-go` (`w1/ConnSourcesPaths.md:73`, `:87`).
- Both pages are missing from `:67`. This breaks no rule: they are not row candidates on their own, and the entry makes no claim about 1.26/1.27. But under the entry's own convention they would add 2 to identified and 2 to excluded.

**Effect.**
- By w1 evidence, identified is at least 12: the 11 families including GoReSym, plus this drafted row.
- It reaches 15 if clause 3 is split and the 1.26/1.27 pages are counted the way go1.25 was.
- The stated 11 can be reproduced only from the entry's own list, and only by accepting F1's gap.

### F3 — LOW (accuracy of one reason): clause 3's reason for revsets/bookmarks contradicts the registry's own lead

**Observation.** Clause 3 calls jj revsets/bookmarks and config defaults "leads for sandbox validity, not pin correctness" (`:67`).

The registry's own lead for the same two files (`:77`) says something different: "a pushed check against `origin/main` proves 'matches the last fetch', not live remote state". That limits what a pin tool can claim. It says nothing about sandbox validity.

That pushed check exists in C2's pin module at REV:
- `.ufo/waves/round-18/tools/revpin.py:28` names the finding `branch_not_pushed`.
- `:32-33` defines "Pushed" as every commit on `refs/heads/<branch>` being contained in `refs/remotes/origin/<branch>`.
- `:120-121` raises it.

No round-18 tool qualifies that check as last-seen state: command 6b finds no hits, exit 1.

w1 drew a different line between the two sources:
- revsets/bookmarks "bounds the fix's truth claim", so a row is deserved (`w1/ScoutJjRevsetsTrunk.md:12`, `:209-213`).
- config holds "sandbox-validity facts only", so it stays a lead (`:13`, `:215`).

**Inference.** Leaving revsets/bookmarks out of the registry is L1's call. But the stated reason fits only config. No count changes.

## Reconciliation: each candidate family and its disposition at `SOURCES.md:67`

| Family | w1 evidence | Named in where-searched? | Disposition |
|---|---|---|---|
| PR #9348 | `DraftS033Row.md:10`, `ScoutPr9348Reopen.md:172` | yes | included as S033 |
| Go 1.24 notes | `DraftGoNotesRow.md:11`, `ScoutGo124NotesSwiss.md:60` | yes | included as S034 |
| go1.24.6/1.25.0 `internal/abi` | `ScoutAbiSwissLayout.md:102` (+ `DraftAbiRow.md:10`) | yes | included as S035 |
| jj v0.45.1 git-compatibility | `ScoutJjColocation.md:74`, `ScoutJjRevsetsTrunk.md:207` | yes | included as S036 |
| go1.25 notes | `ScoutGo125MapsNotes.md:15` | yes | excluded, clause 1 |
| jj `latest` | `DraftJjRow.md:41` | yes | excluded, clause 2 |
| jj revsets + bookmarks | `ScoutJjRevsetsTrunk.md:213` | yes | excluded, clause 3 (see F3) |
| jj config / `misc.toml` | `ScoutJjRevsetsTrunk.md:215` | yes (`config.md`) | excluded, clause 3. One candidate or two? |
| git-rev-parse + gitrevisions | `ScoutGitRevParseDocs.md:253` | yes | excluded, clause 4 |
| gore v0.14.7 | `ScoutGoReSymSwiss.md:205` | yes | excluded, clause 5 |
| Ghidra master `GoMapType` | `ScoutGoReSymSwiss.md:17` | yes | excluded, clause 6 |
| GoReSym v3.4.1 | `ScoutGoReSymSwiss.md:16`, `:88` | yes | **none (F1)** |
| Go 1.25.0 map-experiment selection tree | `ScoutGo125MapsNotes.md:164`, `ConnSourcesPaths.md:66` | only as generic "toolchain trees" | **none (F2)** |
| go1.26 / go1.27 notes (0 matches) | `ScoutGo125MapsNotes.md:70` | no | none (F2, inference) |

All w1 paths in the table are under `.ufo/waves/round-18/w1/`.

## Commands

Commands are verbatim, with exit codes. The working directory is the lane root unless noted, and `REV` stands for the full sha.

1. `git show REV:corpus/SOURCES.md | cat -n; echo "EXIT:$?"` → `EXIT:0`. The entry is at `:67`; the new rows are at `:39-42`.
2. Count and clause parser → `EXIT:0`:
   ```
   git show REV:corpus/SOURCES.md | python3 -I -B -c '
   import sys,re
   line=sys.stdin.read().splitlines()[66]
   assert line.startswith("- 2026-10-20 round 18"), line[:40]
   m=re.search(r"Identified (\d+) candidate sources; screened (\d+); included (\d+) rows \((S\d+)\u2013(S\d+)\); excluded (\d+) as rows: (.*?)\. Stop:", line)
   print("identified,screened,included,excluded =", m.group(1,2,3,6), "included_range =", m.group(4,5))
   ex=m.group(7); parts=[]; depth=0; cur=""
   for ch in ex:
       depth += (ch=="(") - (ch==")")
       if ch=="," and depth==0: parts.append(cur.strip()); cur=""
       else: cur+=ch
   parts.append(cur.strip())
   print("exclusion_reason_clauses =", len(parts))
   for i,p in enumerate(parts,1): print(" ", i, p)
   ws=line.split("Where searched:")[1].split("Identified")[0]
   for name in ["GoReSym","gore","Ghidra master","go1.25","git-rev-parse","latest","revsets","config.md","go1.26","go1.27","buildcfg","reflectdata","redress"]:
       print("%-14s where_searched=%-5s exclusions=%s" % (name, name in ws, name in ex))
   '; echo "EXIT:$?"
   ```
   Output (excerpt):
   ```
   identified,screened,included,excluded = ('11', '11', '4', '7') included_range = ('S033', 'S036')
   exclusion_reason_clauses = 6
   GoReSym        where_searched=True  exclusions=False
   go1.26         where_searched=False exclusions=False
   buildcfg       where_searched=False exclusions=False
   reflectdata    where_searched=False exclusions=False
   ```
3. Registry ids, baseline vs REV → `32a33,36` followed by `> | S033`, `> | S034`, `> | S035`, `> | S036`. `EXIT:1` means differences were found:
   ```
   diff <(git show 9011581d84527ba34c675f9cf912e54d2e72d470:corpus/SOURCES.md | grep -o '^| S0[0-9][0-9]') <(git show REV:corpus/SOURCES.md | grep -o '^| S0[0-9][0-9]'); echo "EXIT:$?"
   ```
4. Drafted rows in w1 → 26 lines (13 are 11-cell registry drafts; the rest are gate quotes and an allocation table). `EXIT:0`:
   ```
   git grep -n -E '^\| S0[0-9]{2}( \(provisional\))? \| [A-Za-z]' REV -- .ufo/waves/round-18/w1/ | cut -c1-230
   ```
   - 4b. Cell widths of the same lines → all 13 drafts are 11 cells. The other lines are 4-cell (`ConnSourcesPaths.md:61-64`) or 3-cell (gate quotes). `EXIT:0`:
     ```
     git grep -n -E '^\| S0[0-9]{2}( \(provisional\))? \| [A-Za-z]' REV -- .ufo/waves/round-18/w1/ | awk -F'|' '{split($1,a,":"); print a[2]":"a[3], NF-2}'
     ```
5. Git docs citations → one hit, `corpus/SOURCES.md:67`. `EXIT_A:0`:
   ```
   git grep -n -i -E 'git-scm\.com|gitrevisions' REV -- corpus SKILL.md .ufo/waves/round-18/tools .ufo/waves/round-18/contract.md | cut -c1-200
   ```
6. `git grep -n -E 'require_pushed|branch_not_pushed|refs/remotes/origin|last-seen|remote_last_seen' REV -- .ufo/waves/round-18/tools | cut -c1-200` → hits in `revpin.py` (`:12,20,28,33,57,94,109,120,121,…`) and in `jj-red-before.py`. `EXIT_B:0`.
   - 6b. `git grep -n -i -E 'last-seen|last seen|remote_last_seen|last fetch' REV -- .ufo/waves/round-18/tools` → no output, `EXIT:1`.
7. `git show REV:corpus/SOURCES.md | sed -n '41p' | grep -c -E 'buildcfg|exp\.go|reflectdata|reflect\.go'` → `0`, `EXIT_E:1`.
8. `git show REV:corpus/SOURCES.md | grep -n -o -E 'GoReSym[^|;]{0,50}'` → lines 11, 36, 48, 65, 67, 73. `EXIT_D:0`.
9. `git diff 9011581d84527ba34c675f9cf912e54d2e72d470 REV -- corpus/SOURCES.md | grep -E '^[+-]' | grep -vE '^[+-]{3}' | cut -c1-120 | cat -n` → four rows added, the Paths edits, the `:67` entry and two leads. `EXIT:0`.
10. go1.25 notes re-fetch:
    - `curl -sSL --max-time 30 https://go.dev/doc/go1.25 | sha256sum` → `c9d872d374a3d52bbd5e1fad7d99b9eb44a7dac45d7032314d8cacd0702d38fd`, exit `0/0`.
    - `curl -sSL --max-time 30 https://go.dev/doc/go1.25 | grep -c -i -E 'swiss|noswissmap'` → `0`, exit `0/1` (grep found no match).
11. `git show REV:.ufo/waves/round-18/evidence/s032-digests.json` → `EXIT:0`.
12. `git show REV:corpus/lessons/round-18.md | grep -n -i -E 'identified|screened|excluded|census|36 rows|32 rows|rows S0|S033|S036|GoReSym|search log' | cut -c1-260` → `:10`, `:24`, `:26`, `:27`, `:34`, `:38`, `:42`, `:43`, `:56`, `:68`. None restates the 11/11/4/7 counts. `EXIT:0`.
13. Fleet repo, cwd `/home/vgpnk/Projects/shokunin`:
    - `git rev-parse HEAD` → `2618bfb6641e245b0044644944c91ed6adb92fa3`.
    - `git status --porcelain -- CORPUS.md` → empty.
    - `sed -n '126,128p' CORPUS.md` → rule 5.
    - Exit 0 each.

## Residual risk and verification gaps

- **Counting unit.** The entry never defines its counting unit (URL, page or row family). F1 holds under every grouping I tried. F2's "≥ 12" assumes the drafted selection row is its own family, which is how `w1/ConnSourcesPaths.md:84` treats it.
- **Not re-checked.** GoReSym's lack of Swiss handling, gore, Ghidra master and jj `latest` rest on w1 observations; I did not re-clone or re-fetch them. Only the go1.25 page was re-fetched.
- **No semantic tooling.** The LSP check does not apply, because the subject is Markdown registry prose, not code. Text grep is a literal check here, not semantic proof.
- **Out of scope; may interest `KaidokuR18.UsedByResolve`.** S033's `used-by` (`:39`) lists only `corpus/lessons/round-18.md`. `corpus/knowledge/2026-10-20-r18-swiss-map-replay.md` contains the token `S033` twice. I counted the tokens only and did not read their context.

## Tooling

No installs or upgrades. I used the existing `git`, `python3 -I -B`, `curl`, `grep`, `sed`, `diff` and `sha256sum`.
