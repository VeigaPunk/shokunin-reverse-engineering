# ReopenS027 — S027 re-opened against live source, 2026-10-20

Seat: author-side falsifier (`KaidokuR17.ReopenS027`), leaf. Lane revision `da64646adcb19c1ede7537b799b8c7d283fe43da`
(`git diff --quiet -- corpus/` → clean; artifacts below are the committed bytes).

**Verdict: PASS on the assigned target.** The S027 row and the Gate quote are accurate as written. One
low-severity precision defect in `teaches`, one informational source-title paraphrase. No fabricated or
wrong-location quote found.

## What I saw (verbatim)

```
$ gh api repos/golang/go/issues/75953 --jq '{number,title,state,state_reason,created_at,closed_at,comments,milestone:.milestone.title,url:.html_url}'
{"closed_at":"2025-11-20T16:09:56Z","comments":19,"created_at":"2025-10-17T15:53:27Z",
 "milestone":"Go1.26","number":75953,"state":"closed","state_reason":"completed",
 "title":"go/version: does not support the `X:` suffix from `go env GOVERSION`",
 "url":"https://github.com/golang/go/issues/75953"}
```

Issue description (excerpt, live): `However, the \`X:\` suffix form is not supported by \`go/version\`; as of
36863d619400910a2728c07615afe91c17415ef4, the program` … and the body's run prints `true / true / false`
for `version.IsValid("go1.25.3 X:nodwarf5")`.

```
$ gh api repos/golang/go/issues/75953/comments --jq '.[5] | {user:.user.login,created_at,body}'   # 6th of 19
user: dmitshur
created_at: 2025-10-17T16:43:36Z
body-tail: 'e change might be to replace the space with a dash, like "go1.25.3-X:nodwarf5". That maintains the property that the "X:\\<GOEXPERIMENT\\>" substring is included, and follows the existing format for a non-standard toolchain version.'
```

Closing comment, 2025-11-20T16:09:56Z (dmitshur): `Closing this again since the original issue with invalid
version strings sometimes being produced is resolved.` (The thread had been reopened 2025-11-14 by qmuntal,
comment 12, "in case we want to rethink the proposed solution".)

```
$ curl -sS -L https://raw.githubusercontent.com/golang/go/go1.27.3/src/cmd/link/internal/ld/main.go   # sha256 0fe8ad02…
191	buildVersion := buildcfg.Version
192	if goexperiment := buildcfg.Experiment.String(); goexperiment != "" {
193		sep := " "
194		if !strings.Contains(buildVersion, "-") { // See go.dev/issue/75953.
195			sep = "-"
196		}
197		buildVersion += sep + "X:" + goexperiment
```

## Cell-by-cell verification — `corpus/SOURCES.md:33`

| Cell | Landed value (abridged) | Live observation | Verdict |
|---|---|---|---|
| source URL | `https://github.com/golang/go/issues/75953` | resolves; number/title match | pass |
| tier | `B` | see non-finding N6 | pass (conservative) |
| scope | rationale, dash proposal, "not normative" | dmitshur calls the produced string neither standard nor non-standard; proposes dash | pass |
| anchor | Issue description; dmitshur 2025-10-17; closed; milestone Go1.26; accessed 2026-10-20 | all four true (`state_reason: completed`, `closed_at 2025-11-20`, `milestone: Go1.26`) | pass |
| teaches | "space form was the defect and the dash form the chosen repair" | proposal is hedged; "chosen" rests outside the quoted span | **F1** |
| status | `mined` | literal test satisfied; Gate-only citation | N7 |
| opened / recheck / used-by | 2026-10-20 / 365d / lessons | matches access date and Gate access date | pass |

## Quote check — `corpus/lessons/round-17.md:49`

```
location cell: 'https://github.com/golang/go/issues/75953, dmitshur comment 2025-10-17'
quote cell   : 'A simple change might be to replace the space with a dash, like "go1.25.3-X:nodwarf5".'
byte-identical to live comment sentence: True
words: 14 (<= 25)   non-ASCII in quote: []   next source chars: ' That maintains the property t'
in issue description: False   comments containing quote: [(6,'dmitshur','2025-10-17T16:43:36Z')] (1 of 19)
```

Contiguous, sentence-bounded, unique, and at the stated location. This is the exactness the Gate claims.

## Findings

### F1 (low) — `teaches` asserts a decision the Gate quote only proposes
- Anchors: `corpus/SOURCES.md:33` (`teaches`), `corpus/lessons/round-17.md:49` (quote).
- Observation: the quote is `A simple change might be to replace the space with a dash…` — a hedged proposal
  ("might be"), verified exact. `teaches` says "the dash form **the chosen repair**". The choice is evidenced
  only outside the quoted span: gopherbot 2025-11-11, CL 719701 `cmd/link/internal/ld: make
  runtime.buildVersion with experiments valid`, and dmitshur's 2025-11-20 close.
- Why it matters: CORPUS.md:112 (rule 1) asks the Gate quote to ground `teaches`; here it grounds the
  proposal half, not the decision. The claim is true in fact (go1.27.3 `main.go:193-196` emits the dash), so
  this is precision, not falsity.
- Smallest fix: change `chosen` → `proposed` in the `teaches` cell. Alternatively add one Gate row
  (16 words, within the limit):
  `| S027 | https://github.com/golang/go/issues/75953, dmitshur comment 2025-11-20 | Closing this again since the original issue with invalid version strings sometimes being produced is resolved. |`

### F2 (informational) — `source` cell paraphrases the issue title
- Anchor: `corpus/SOURCES.md:33`. CORPUS.md:90 asks `source` to be `title — canonical URL`. The live title is
  ``go/version: does not support the `X:` suffix from `go env GOVERSION` ``; the landed text is
  ``golang/go issue #75953, `go/version` and the `X:` suffix``.
- Impact: no claim error; only exact-title searchability. w1 already had the verbatim title
  (`.ufo/waves/round-17/w1/draft-sources-rows.md:20`).
- Smallest fix: substitute the verbatim title in the `source` cell.

## Bounded non-findings (checked, no defect)

- **N1 quote exactness**: byte-identical, 14 words, sentence boundary; no Unicode substitution.
- **N2 location**: unique among 19 comments and absent from the description; only dmitshur comment on that
  date, so "dmitshur comment 2025-10-17" is a resolvable anchor.
- **N3 anchor URL/number/title**: match the live issue.
- **N4 closed + milestone**: `state=closed`, `state_reason=completed`, `milestone=Go1.26`. Reopen/reclose
  chronology (2025-11-14 → 2025-11-20) does not falsify "closed" at the 2026-10-20 access date.
- **N5 scope**: the issue body's `false` result for `go1.25.3 X:nodwarf5` is the claimed breakage; dmitshur
  frames the form as a malformed non-standard-toolchain name.
- **N6 tier B**: CORPUS.md:93-96 literally lists "maintainer statement" under A, so A was available. B still
  survives: the quoted statement is hedged, the thread was reopened to reconsider the dash, and the row
  defers shipped behavior to S026 (tier A code). Under-claiming, not a defect — do not "fix" upward.
- **N7 `mined`**: CORPUS.md:103's literal test holds (used-by path contains S027 at
  `round-17.md:28,49`). Both occurrences are Gate tables; no body citation, and
  `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:1` cites S003, S023, S024, S025, S026, S029 —
  not S027. Same pattern as S030, so it is a corpus convention question for L1, not an S027 defect.
- **N8 table shape**: 11 cells, no `|` inside any cell; every S-row in the registry has 11 cells (python check).
- **N9 "dash form" vs shipped conditional**: the tag-pinned linker uses the dash only when the version has
  no `-` (devel strings keep the space). S027 does not state the condition, but S026 does ("dash when the
  version has no `-`") and S027 explicitly defers shipped behavior to S026 — no cross-row contradiction.

## Tools / provenance

No installs or upgrades. Used `gh` (authenticated, read-only), `curl`, `python3 -B`; scratch under `/tmp`.
No REA analyze/search/decompile, no Ghidra, no carrier execution.
