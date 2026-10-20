PARTIAL

# ReopenS034 — SOURCES row S034 re-open (round 18, wave 2)

- **Seat:** KaidokuR18.ReopenS034. This is an author-side advisory seat, not outside review.
- **Revisions:**
  - REV `b2aad08ceeee8dd125ce0d316056d8bd766c7f94`. Lane `git rev-parse HEAD` returned REV when I checked.
  - Baseline `9011581d84527ba34c675f9cf912e54d2e72d470`.
  - C3 freeze `eb6c2668e5cb7054fd1e16d2f615cb65586d0fe0`.
- **Method:** read-only. I read every lane file with `git show REV:path`, and this report is the only file I wrote. All commands ran on 2026-10-20.
- **Column spec:** fleet `/home/vgpnk/Projects/shokunin/CORPUS.md:89-108` (the cells) and `:112-118` (the rules). This file is in the fleet working tree, not lane REV.
- **Shorthand:** `LANE=/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, `REV=b2aad08…`, `OPT=/home/vgpnk/.local/opt`. The commands below are verbatim, except that I ran them with the literal paths these variables stand for.

## Verdict

**PARTIAL.** I agree with the source, sha256, anchor, quote, kind, tier, scope, status and used-by cells. I disagree with one clause of `teaches`.

| S034 cell (`corpus/SOURCES.md:40`) | Result | Basis |
|---|---|---|
| source `https://go.dev/doc/go1.24` | HOLDS | HTTP 200, no redirect, 82634 bytes (C9) |
| anchor sha256 `d35c2d52…c4e7` | HOLDS | Two new fetches (plain and `--compressed`) both give this exact digest (C2, C7) |
| anchor `<h2 id="runtime">` raw line 560; opt-out raw 571-573 | HOLDS | Lines are exact; `id="runtime"` occurs once (C2, C9). The revision is the versioned page plus digest plus access date (CORPUS.md:99-100) |
| Gate quote, `corpus/lessons/round-18.md:35` | HOLDS | Verbatim match with tag-stripped raw 571-573. 21 words, or 24 if `-` and `=` also split words, so ≤25 (C4) |
| kind `docs`, tier `A` | HOLDS | Official docs are tier A for this scope (CORPUS.md:93-97). The row is not `community` |
| scope | HOLDS (wording nit, F4) | "Swiss Tables" at raw 567-568; opt-out at raw 571-573 |
| teaches | **PARTIAL (F1)** | The Gate quote grounds only "build-time choice". The last clause is contradicted by the lane's own tool and by the Go toolchain |
| status `mined`, used-by | HOLDS | Both used-by paths cite S034. Leaving out SKILL.md is correct under CORPUS.md:107-108 |
| anchor note "stable across 8 seat fetches and one L1 fetch" | HOLDS, with an audit gap (F3) | 12 seat fetches are recorded, not 8. No L1 fetch record is retained |

## Findings

### F1 — `teaches` overreaches its source, and its last clause is contradicted (medium-low; operability and calibration)

The row says: "The map layout is a build-time choice of the target binary, so a reader must take it from the carrier (its `GOEXPERIMENT` build setting), not from the Go release number."

**Grounding gap.** CORPUS.md:112-115 says the Gate quote must ground `teaches`.
- [Observation] The quote at `round-18.md:35` contains none of the strings `layout`, `carrier`, `binary`, `build setting`, `release` or `version` (C13; grep exit 1).
- [Observation] The quote grounds only that the map *implementation* is selected at build time.

**The lane's own predictor reads the release number.** [Observation]
- `.ufo/waves/round-18/tools/swiss-misread.py:1281`: `swiss_default = parts[0] > 1 or (parts[0] == 1 and parts[1] >= 24)`.
- `:1282`: `true_kind = "old" if noswiss or not swiss_default else "swiss"` (C11).

**A carrier records only deviations from a per-release baseline.** [Observation]
- `go-1.25.0/src/internal/buildcfg/exp.go:160-161`: `String()` returns `expList(&exp.Flags, &exp.baseline, false)`, which leaves out flags that match the baseline.
- `go-1.25.0/src/cmd/link/internal/ld/main.go:189-190`: the linker appends `" X:" + goexperiment` only when that list is non-empty.
- `go-1.25.0/src/cmd/go/internal/load/pkg.go:2473-2474`: cmd/go records the `GOEXPERIMENT` build setting only when `RawGOEXPERIMENT != ""`. `cfg/cfg.go:290` defines `RawGOEXPERIMENT` as `envOr("GOEXPERIMENT", buildcfg.DefaultGOEXPERIMENT)`.
- The baseline is `SwissMap: true` in go1.24.6 `exp.go:81` and go1.25.0 `exp.go:85` (C12, C14).
- [Inference] So a default Swiss build of 1.24 or 1.25 carries no Swiss marker at all. Classifying it as Swiss needs the release number.

**The choice exists only for Go 1.24.x and 1.25.x.** [Observation]
- Upstream `internal/abi/map_noswiss.go` and `map_swiss.go` return 200 at go1.24.0 and go1.25.0, and 404 at go1.23.0, go1.26.0 and go1.27.0 (C10).
- `internal/goexperiment/flags.go` returns HTTP 200 at every tag I checked. It has 0 `swissmap` matches at go1.23.0 and go1.26.0, and one `SwissMap bool` at go1.24.0 (C14, C15).
- Installed go1.27.3 has no SwissMap in `flags.go` or `exp.go`, and `abi/` has only `map.go` (C12, C14).
- [Inference] Outside 1.24.x and 1.25.x, the release number alone fixes the implementation. Patch releases between the tags were not checked.

**Elsewhere the lane already states the correct rule.** [Observation]
- S026 `teaches` (`corpus/SOURCES.md:32`): the `X:` token "records a non-default link-time experiment configuration … and is not part of the release number". S026 is anchored on `exp.go` `String()` leaving out baseline flags.
- The knowledge entry words it correctly: "Swiss by default from Go 1.24, old under `GOEXPERIMENT=noswissmap`" (`corpus/knowledge/2026-10-20-r18-swiss-map-replay.md:22-23`).
- Only `SOURCES.md:40` carries the "not from the Go release number" clause (C22).

**The parenthetical is incomplete.** [Observation] "(its `GOEXPERIMENT` build setting)" names only one of the two carrier records. The tool (`swiss-misread.py:1280`) and `SKILL.md:560` also read the `X:noswissmap` version suffix.

**Assessment.** [Inference]
- Read charitably, as "not from the release number alone", the clause is true for 1.24 and 1.25.
- Read literally, it is wrong guidance: an operator with a carrier that has no experiment record cannot decide its map layout without the release number.
- "Map layout" belongs to S035. S034 itself says "implementation" (raw 567, 571).
- C3's numbers should be unaffected, because the predictor implements the correct rule (`:1279-1282`). I did not re-run it.

**Suggested remedy (advisory).**
- `teaches` cannot be edited in place (CORPUS.md:116-118). The correction is a new row whose `teaches` opens `supersedes S034 —`.
- Suggested text: "supersedes S034 — Go 1.24 made the Swiss-table map the default with a build-time `GOEXPERIMENT=noswissmap` opt-out, so a 1.24 carrier's map implementation follows its recorded experiment (build setting or `X:` suffix) over its release's default; the page says nothing about descriptor layout (S035)."

### F2 — the anchor omits the Swiss Tables lines (nit)

- [Observation] The first half of the scope ("the new Swiss-table implementation") rests on raw 567-568. `grep -n -i swiss` hits lines 568 and 572 (C7).
- The anchor cites only 560 and 571-573.
- The w1 draft cited them: `.ufo/waves/round-18/w1/DraftGoNotesRow.md:11` says "Swiss sentence 567–568".
- [Inference] The scope is still reachable: 567-568 sit inside the anchored `#runtime` section (560-573), and line 572 names `noswissmap`. No action is needed; a superseding row should add these lines.

### F3 — fetch-stability provenance (nit; auditability)

- [Observation] `git grep -n -i 'd35c2d' REV --` finds the digest only in four w1 seat reports and in `SOURCES.md:40` (C5).
- Recorded seat fetches total 12, and every one gives this digest:
  - `ScoutGo124NotesSwiss.md:34-45`: 8 of 8.
  - `CriticSourcedClaim.md:125`: 2.
  - `DraftGoNotesRow.md:21`: 1.
  - `ScoutGo125MapsNotes.md:51-52`: 1.
- No L1-side record for this page exists at REV. The search log (`SOURCES.md:67`) gives L1 fetch counts only for the PR page.
- [Inference] "8" is a harmless understatement, but "one L1 fetch" cannot be audited at REV.
- This seat adds 2 more matching fetches (C2, C7).

### F4 — "no Go 1.25 claim" reads ambiguously (nit)

- As a disclaimer about the row's scope, it is correct. It is consistent with the rejected go1.25-notes row (`round-18.md:25`), and the go1.25 page has 0 `swiss` matches (C7).
- As a description of the page, it is false. The page states Go 1.25 facts at raw 463 (`aliastypeparams` removal) and raw 1060 (macOS 12), and a Go 1.26 fact at raw 591. None of them concern maps (C8).
- Suggested wording: "no Go 1.25 map claim".

## Checked and held

- **Row structure.** The row has 11 cells, matching the header (`SOURCES.md:5`), so no stray `|` is present (C4).
- **Row timing.** S034 is absent at baseline and at the C3 freeze (C6: exit 1 both times), so it was added after the predictions were frozen. CORPUS.md:112 asks only that the source is opened in the round that writes the row, and the w1 fetches satisfy that. I found no rule requiring a row before the freeze, but I did not search exhaustively.
- **used-by.**
  - CORPUS.md:107-108 limits used-by to knowledge entries and lessons. Both listed paths cite S034: `round-18.md:10,24,35` and the knowledge file `:1,23` (C5b).
  - `SKILL.md:550` also cites S034 but is not such a path.
  - S036 (`SOURCES.md:42`) is the only one of the 36 rows that lists SKILL.md (C16). That row is outside this seat's scope.
- **Paths.** The Paths entry (`SOURCES.md:49`) gives the descriptor sizes to S035 and "per-binary build choice" to S034. This matches F1's narrower reading.
- **Search log.** The negative "go1.25 notes: 0 swiss/noswissmap" (`SOURCES.md:67`) reproduces (C7).
- **Tier definitions.** No `SOURCES.md` section at REV or at baseline defines tiers (C17), although lane `corpus/QUALITY.md:44` points there for them. The definitions are in fleet `CORPUS.md:93-97`. This is a documentation-pointer gap, not an S034 defect.

## Commands (exit codes as observed)

```
C1  cd $LANE && git rev-parse HEAD && git show $REV:corpus/SOURCES.md | grep -n 'S034' ; echo "EXIT:$?"            # EXIT:0; HEAD=REV; :40, :49
C2  cd /tmp && curl -sS -o go124.html https://go.dev/doc/go1.24 ; echo "CURL_EXIT:$?" ; sha256sum go124.html ; wc -l go124.html ; nl -ba go124.html | sed -n '555,580p'
                                                                       # CURL_EXIT:0; d35c2d52a864b3474451e28fb89bae013edba4adcc1fa7164796267c0e4ec4e7; 1334 lines; 560 h2#runtime; 567-568 Swiss Tables; 571-573 opt-out
C3  cd $LANE && git show $REV:corpus/lessons/round-18.md | grep -n 'S034' ; echo "EXIT:$?"                          # EXIT:0; :10, :24, :35
C4  git show $REV:corpus/lessons/round-18.md > /tmp/r18_lesson.md && git show $REV:corpus/SOURCES.md > /tmp/r18_sources.md && python3 -I -B - <<'EOF'
    import re, html
    page = open('/tmp/go124.html', encoding='utf-8').read().split('\n')
    txt = ' '.join(html.unescape(re.sub(r'<[^>]+>', '', ' '.join(page[570:573]))).split())
    les = open('/tmp/r18_lesson.md', encoding='utf-8').read().split('\n')
    q = [c.strip() for c in les[34].strip().strip('|').split('|')][2]
    print('VERBATIM_EQUAL:', q == txt); print('WORDS:', len(q.split()), len(re.split(r'[\s\-=]+', q.strip('.'))))
    src = open('/tmp/r18_sources.md', encoding='utf-8').read().split('\n')
    sc = [c.strip() for c in src[39].strip().strip('|').split('|')]; hdr = [c.strip() for c in src[4].strip().strip('|').split('|')]
    print(len(sc), len(hdr)); [print(h, '=', c) for h, c in zip(hdr, sc)]
    EOF                                                                # EXIT:0; VERBATIM_EQUAL: True; QUOTE_IN_PAGE_TEXT: True; WORDS 21 / 24; cells 11/11
                                                                       # (excerpt of the heredoc as run; the run also printed QUOTE_IN_PAGE_TEXT)
C5  git grep -n 'd35c2d52' $REV -- ; git grep -n -i 'd35c2d' $REV --  # EXIT:0 both; 10 hits: 4 w1 seat reports + SOURCES.md:40
C5b git grep -n 'S034' $REV --                                         # EXIT:0
C6  git show 9011581d84527ba34c675f9cf912e54d2e72d470:corpus/SOURCES.md | grep -n 'S034\|S035\|S036' ; git show eb6c2668e5cb7054fd1e16d2f615cb65586d0fe0:corpus/SOURCES.md | grep -n 'S034'
                                                                       # EXIT:1, EXIT:1 (absent at baseline and at C3 freeze)
C7  cd /tmp && curl -sS --compressed -o go124b.html https://go.dev/doc/go1.24 ; sha256sum go124b.html ; curl -sS -o go125.html https://go.dev/doc/go1.25 ; grep -c -i 'swiss' go125.html ; grep -n -i 'swiss' go124.html
                                                                       # CURL2_EXIT:0 same digest; CURL125_EXIT:0; count 0 (GREP125_EXIT:1); 568, 572 (GREP124_EXIT:0)
C8  grep -n -E '1\.25|1\.26' go124.html                                # GREP_EXIT:0; 463, 591, 1060
C9  curl -sS -o /dev/null -w 'HTTP=%{http_code} size=%{size_download} redirect=%{redirect_url} url_effective=%{url_effective}\n' https://go.dev/doc/go1.24 ; grep -c 'id="runtime"' go124.html
                                                                       # CURL_EXIT:0; HTTP=200 size=82634 redirect= url_effective=https://go.dev/doc/go1.24; 1 (GREP_EXIT:0)
C10 for t in go1.23.0 go1.24.0 go1.25.0 go1.26.0 go1.27.0; do printf '%s map_noswiss.go=' $t; curl -s -o /dev/null -w '%{http_code}' https://raw.githubusercontent.com/golang/go/$t/src/internal/abi/map_noswiss.go; printf ' map_swiss.go='; curl -s -o /dev/null -w '%{http_code}\n' https://raw.githubusercontent.com/golang/go/$t/src/internal/abi/map_swiss.go; done
                                                                       # LOOP_EXIT:0; 404/404, 200/200, 200/200, 404/404, 404/404
C11 git show $REV:.ufo/waves/round-18/tools/swiss-misread.py | nl -ba | sed -n '1268,1300p'          # EXIT:0 (lines 1279-1282 quoted in F1)
C12 cd $OPT && grep -n 'SwissMap' go-1.24.6/src/internal/buildcfg/exp.go go-1.25.0/src/internal/buildcfg/exp.go go-1.27.3/src/internal/buildcfg/exp.go   # EXIT:0; 1.24.6:81, 1.25.0:85, none in 1.27.3
    grep -n -i 'swissmap' go-1.27.3/src/internal/goexperiment/flags.go                                 # EXIT:1
    grep -n -i 'swissmap' go-1.25.0/src/internal/goexperiment/flags.go                                 # EXIT:0; :115-116
    ls go-1.27.3/src/internal/abi/ | grep -i map                                                       # EXIT:0; map.go
    grep -n -A3 'func (exp \*ExperimentFlags) String' go-1.25.0/src/internal/buildcfg/exp.go           # EXIT:0; :160-161
    grep -n 'RawGOEXPERIMENT\|"GOEXPERIMENT"' go-1.25.0/src/cmd/go/internal/load/pkg.go               # EXIT:0; :2473-2474
    grep -rn -B2 -A6 'Experiment.String()' go-1.25.0/src/cmd/link/internal/ld/main.go                  # EXIT:0; :188-192
C13 cd $LANE && git show $REV:corpus/lessons/round-18.md | sed -n '35p' | cut -d'|' -f4 | grep -o -i -E 'layout|carrier|binary|build setting|release|version' ; echo "EXIT:${PIPESTATUS[3]}"
                                                                       # EXIT:1 (no match)
C14 cd $OPT && grep -n 'RawGOEXPERIMENT' go-1.25.0/src/cmd/go/internal/cfg/cfg.go                    # EXIT:0; :289-290
    for t in go1.23.0 go1.24.0 go1.26.0; do printf '%s flags.go SwissMap lines: ' $t; curl -s https://raw.githubusercontent.com/golang/go/$t/src/internal/goexperiment/flags.go | grep -c 'SwissMap bool'; done
                                                                       # 0, 1, 0 (LOOP_EXIT:1 = final grep -c printed 0)
    curl -s -o /dev/null -w '%{http_code}\n' https://raw.githubusercontent.com/golang/go/go1.26.0/src/internal/abi/map.go   # 200
    grep -n 'SwissMap' go-1.27.3/src/internal/buildcfg/exp.go                                          # EXIT:1
C15 for t in go1.23.0 go1.26.0; do printf '%s flags.go any-SwissMap: ' $t; curl -s https://raw.githubusercontent.com/golang/go/$t/src/internal/goexperiment/flags.go | grep -c -i 'swissmap'; done
                                                                       # 0, 0 (LOOP_EXIT:1)
    curl -s -o /dev/null -w '%{http_code}\n' https://raw.githubusercontent.com/golang/go/go1.23.0/src/internal/goexperiment/flags.go   # 200
    for t in go1.24.0 go1.26.0; do printf '%s flags.go HTTP=' $t; curl -s -o /dev/null -w '%{http_code}\n' https://raw.githubusercontent.com/golang/go/$t/src/internal/goexperiment/flags.go; done
                                                                       # 200, 200 (LOOP_EXIT:0)
C16 python3 -I -B -c "rows=[l for l in open('/tmp/r18_sources.md',encoding='utf-8') if l.startswith('| S0')]; print('rows', len(rows)); print('rows_with_SKILL_in_usedby', sum('SKILL.md' in l.rstrip().rstrip('|').split('|')[-1] for l in rows))"
                                                                       # EXIT:0; rows 36; 1 (S036)
    git show $REV:SKILL.md | grep -n -o -E '\bS0[0-9]{2}\b'            # EXIT:0; 550: S034 S035 S023 S003 S033
C17 grep -n '^#' /tmp/r18_sources.md ; git show 9011581d84527ba34c675f9cf912e54d2e72d470:corpus/SOURCES.md | grep -n '^#'
                                                                       # EXIT:0 both; Registry/Paths/Search log/Leads only, no tier section
C22 git grep -n -i 'release number' $REV -- ':!.ufo/interactive-sessions/**'   # EXIT:0; corpus hits only SOURCES.md:32 (S026), :40 (S034); rest are round-17 seat reports
```

I also used these read-only lookups, with no shell exit code: the `grep` tool on fleet `CORPUS.md` (match at :93), a `read` of `CORPUS.md:78-130`, and the `grep` tool on `~/.agents/skills/shokunin` for tier rules (no match).

## Remaining unknowns

- Whether the L1 fetch named in F3 happened. No record is retained at REV.
- Go patch releases between the checked tags (for example 1.25.x after 1.25.0, or 1.26.x) were not checked one by one. The version-bound statements in F1 hold at tag level.
- The page digest is evidence for fetch time only; go.dev can edit the page in place. `ScoutGo124NotesSwiss.md:45-46` reports no ETag or Last-Modified header; I did not re-check headers.

## Installs

None. `curl`, `sha256sum`, `grep`, `git` and `python3` were already present. I deleted my scratch files in `/tmp` (`go124.html`, `go124b.html`, `go125.html`, `r18_lesson.md`, `r18_sources.md`) after writing this report.
