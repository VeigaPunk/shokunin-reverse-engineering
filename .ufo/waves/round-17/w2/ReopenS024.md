# ReopenS024 — independent re-open of S024, 2026-10-20

Lane revision: `git rev-parse HEAD` → `da64646adcb19c1ede7537b799b8c7d283fe43da`; `git status --porcelain`
shows only untracked `.ufo/waves/round-17/*` files, so `corpus/SOURCES.md` and
`corpus/lessons/round-17.md` are the committed artefacts under test. Read-only lane: no REA
analyze/search/decompile, no Ghidra, no carrier executed, no installs. Scratch under `/tmp`, Python
run with `-B`.

## 1. What I actually re-opened (commands and verbatim results)

| copy | command | observed |
|---|---|---|
| pinned tag | `curl -sS -m 30 -o /tmp/r17-s024-go1273.txt -w 'http=%{http_code} bytes=%{size_download}\n' https://raw.githubusercontent.com/golang/go/go1.27.3/src/debug/buildinfo/buildinfo.go` | `http=200 bytes=16658` |
| pinned tag hash | `sha256sum /tmp/r17-s024-go1273.txt` | `5e4064efa60e5fb768ffbf49f44bb6dd037fe35d3245ba9573881adef2f9c097` |
| local GOROOT | `sha256sum /home/vgpnk/.local/opt/go-1.27.3/src/debug/buildinfo/buildinfo.go`; `cat .../VERSION`; `wc -l` | same sha256 `5e4064ef…`; `go1.27.3` / `time 2026-10-19T22:20:36Z`; `586` lines |
| live page | `curl -sS -m 30 -o /tmp/r17-s024-godev.html -w 'http=%{http_code} bytes=%{size_download}\n' https://go.dev/src/debug/buildinfo/buildinfo.go` | `http=200 bytes=78364` (sha256 `8f399db70915b42f8dcb91ca68fd53b7e42e2623277ad6cd5e1f89a593e075be`) |

`go.dev/src` render extracted from `<pre>` (line ids `L1`–`L586` plus empty `L587`) is
**identical to the go1.27.3 tag file for all 586 source lines**; the only difference is one trailing
blank line:

```
--- tag
+++ live
@@ -585,2 +585,3 @@
 	return nil, errors.New("address not mapped")
 }
+
```

So the SOURCES.md:30 parenthetical "same lines in the go1.27.3 release tree" is true **as observed
today**, and the go1.27.3 tag file is byte-identical to the host's `go1.27.3` GOROOT copy.

## 2. Verbatim lines seen (`nl -ba` on tag and local copy — identical)

```
   58	var buildInfoMagic = []byte("\xff Go buildinf:")
   97		bi.GoVersion = vers
  200			flagsVersionMask = 0x2
  201			flagsVersionPtr  = 0x0
  202			flagsVersionInl  = 0x2
  224		// Since 1.18, the flags version bit is flagsVersionInl. In this case,
  237			}
  262		if len(mod) >= 33 && mod[len(mod)-17] == '\n' {
  268		}
```

The literal on `:58` is 14 bytes (`\xff` + `" Go buildinf:"`, 13 ASCII), matching the `:55-57` comment before it, so the quote is also internally consistent with the header description.

Live-page raw HTML fragments (line id → body, tab after the number span preserved):
```
L58: <span id="L58" class="ln">    58&nbsp;&nbsp;</span>var buildInfoMagic = []byte(&#34;\xff Go buildinf:&#34;)
L97: <span id="L97" class="ln">    97&nbsp;&nbsp;</span>	bi.GoVersion = vers
L200: …		flagsVersionMask = 0x2
L201: …		flagsVersionPtr  = 0x0
L202: …		flagsVersionInl  = 0x2
L224: …	<span class="comment">// Since 1.18, the flags version bit is flagsVersionInl. In this case,</span>
L237: …		}
L262: …	if len(mod) &gt;= 33 &amp;&amp; mod[len(mod)-17] == &#39;\n&#39; {
L268: …	}
```

## 3. `corpus/SOURCES.md:30` — cell-by-cell

Verbatim row (raw read):

```
| S024 | Go `debug/buildinfo` reader — https://go.dev/src/debug/buildinfo/buildinfo.go (same lines in the go1.27.3 release tree `src/debug/buildinfo/buildinfo.go`) | code | A | How Go's own stdlib reader finds and decodes the build-info blob: magic, flags, inline version and modinfo strings, and the version it returns | go1.27.3 `buildinfo.go:58` magic; `:97` `bi.GoVersion = vers`; `:200-202` flag constants; `:224-237` inline format and decode; `:262-268` modinfo framing | Gives the reference decoder to check a version-string reader against: the version is returned raw, including any `X:` experiment token, and absence of the magic means no record at all. | mined | 2026-10-20 | on-release | corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md, corpus/lessons/round-17.md |
```

| cell | verdict | evidence |
|---|---|---|
| source (URL + parenthetical) | PASS | 586/586 lines equal to tag; empty `L587` only |
| kind `code` | PASS | it is Go stdlib source |
| tier `A` | PASS | fleet `CORPUS.md:93-95`: source code is primary/authoritative for its scope; scope is limited to the blob format, not REA/Ghidra/carriers |
| scope | PASS | matches `Read` `:88-99`, `readRawBuildInfo` `:115-271`, `searchMagic` `:339-412`, `decodeString` `:284-318` |
| anchor | PASS | every cited range at the exact line: `:58`, `:97`, `:200-202`, `:224-237` (comment begins 224, decode ends 237), `:262-268` |
| teaches clause 1 ("version returned raw … `X:` token") | TRUE as written | `:89` `vers, mod, err := readRawBuildInfo(r)` → `:97` `bi.GoVersion = vers`; `grep -n 'TrimSpace\|TrimRight'` over the file = 0 hits, so no normalisation. (That a linker writes `X:` is S026's claim; S024's contribution is the untouched pass-through.) |
| teaches clause 2 ("absence of the magic means no record at all") | TRUE as written, **but unquoted — see F1** | `:411` `return 0, errNotGoExe`; also `:259-261` empty `vers` → `errNotGoExe` |
| status `mined` | PASS | `CORPUS.md:103`: cited by ≥1 `used-by` path; both paths do cite S024 (`corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:1`, `corpus/lessons/round-17.md:43-44`) |
| opened `2026-10-20` / recheck `on-release` | PASS | re-opened today; local `VERSION` build time `2026-10-19T22:20:36Z` is consistent with S025's 2026-10-19 release date |

## 4. `corpus/lessons/round-17.md:43-44` — located quotes

Section: `## Gate` (`:20`) → `### Opened sources and located quotes (access date 2026-10-20)` (`:39`).

| path:line | claimed quote | what I saw | words | verdict |
|---|---|---|---|---|
| `round-17.md:43` | `` `var buildInfoMagic = []byte("\xff Go buildinf:")` `` | buildinfo.go:58 exactly, no leading whitespace (top-level var), single contiguous line | 6 | PASS — exact, contiguous, ≤25 |
| `round-17.md:44` | `` `bi.GoVersion = vers` `` | buildinfo.go:97 is `TAB + bi.GoVersion = vers`; the quote elides the leading TAB | 3 | PASS — exact text and location; whitespace elision is this table's established convention (cf. `round-17.md:47` quoting `main.go:197`, whose source line is three TABs) |

Both locations are correct on **both** the live go.dev page and the go1.27.3 tag. No quote is
mislocated, no quote exceeds 25 words, and no quote contains non-contiguous text.

## 5. Findings

### F1 — LOW (evidence coverage, not a content error)

- **Location**: `corpus/SOURCES.md:30` (teaches cell and anchor cell) with `corpus/lessons/round-17.md:43-44`.
- **Rule**: `/home/vgpnk/Projects/shokunin/CORPUS.md:113-114` — the Gate must record, per new row, "a
  ≤25-word quote with its location grounding `teaches`".
- **Gap**: the teaches cell makes a second, distinct behavioural claim — "absence of the magic means
  no record at all" — that neither Gate quote nor any anchor range shows. The grounding line is
  `buildinfo.go:411`:

  ```
  $ nl -ba /home/vgpnk/.local/opt/go-1.27.3/src/debug/buildinfo/buildinfo.go | sed -n '411p'
     411			return 0, errNotGoExe
  ```

  The quoted lines (`:58` magic literal, `:97` assignment) ground the magic's definition and the raw
  return, not the no-match error path. The anchor cell lists `58, 97, 200-202, 224-237, 262-268` and
  omits `searchMagic` (`339-412`). The claim is true as written; only its evidence pointer is missing.
  The clause was added during integration (w1 draft `.ufo/waves/round-17/w1/draft-sources-rows.md:17`
  taught only "the stdlib does not strip it"), which is consistent with the quote not being extended.
- **Smallest fix**: append `:339-412` (`searchMagic`) to the anchor cell, and add one Gate row:
  `| S024 | same, line 411 | `return 0, errNotGoExe` |` (3 words).

No other finding. Everything the assignment named — anchor lines, tier, scope, teaches truth,
status, and the two located quotes — re-opened correct.

## 6. Bounded no-finding — what was checked and came back clean

- `SOURCES.md:30` quotes/anchor/tier/scope/status/opened/recheck/used-by (all cells above).
- `round-17.md:43-44` exact text, contiguity, word count, line number, on two independent renderings.
- No-drift control between wave 1 and wave 2: the w1 scout reported go.dev page `78,364` bytes and
  tag `16,658` bytes / sha256 `5e4064ef…` (`.ufo/waves/round-17/w1/ScoutGoBuildinfoDocs.md:13-15`);
  my independent re-fetch on 2026-10-20 returned the same two byte counts and the same sha256, so the
  wave-1 quote was not fabricated and the page has not drifted.
- Absence of the w1 scout's warned trap: no artefact cites `617` (grep over `SOURCES.md`,
  `lessons/round-17.md`, the r17 knowledge entry returned nothing).

## 7. Observations (deliberately not filed as findings)

- `go.dev/src` renders the live tree, not a pinned tag; the parenthetical is true today (full-file
  equality) and the anchor is version-pinned to go1.27.3, so the row stays usable if master drifts.
  A pinned raw URL would be more durable, but the current form is within the CORPUS `anchor` rule
  (line + revision).
- The two Gate quotes are not the same shape: `:58` needs no indentation, `:97` elides a TAB. This
  matches the table's other rows, so it is convention, not a defect.

## 8. Residual unknowns

- I did not open the release tarball `go.dev/dl/go1.27.3.src.tar.gz`; two independent copies (GitHub
  tag blob and the host GOROOT file) agree byte-for-byte, which bounds the risk to negligible.
- Whether the `go.dev/src` renderer will continue to match the 1.27.3 tag after the next master
  commit is not knowable from today's observation; only today's equality is claimed.

## 9. Tooling

No installs or upgrades. Commands used: `curl`, `sha256sum`, `nl`, `grep`, `wc`, `git rev-parse`,
and `python3 -B` for HTML line extraction; all scratch under `/tmp`.
