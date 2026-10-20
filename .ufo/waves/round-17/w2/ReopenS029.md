# Reopen S029 — Ghidra upstream Go range: independent re-open, 2026-10-20

Seat: wave-2 falsifier (`KaidokuR17.ReopenS029`), author-side advisory. Lane revision
`da64646adcb19c1ede7537b799b8c7d283fe43da`. Read-only: network fetches (`curl`, `git ls-remote`),
local archive reads (`unzip -p`, `strings`), no REA analyze/search/decompile, no Ghidra,
no carrier executed. All paths below are relative to
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.

Targets: `corpus/SOURCES.md:35` (row S029) and the two S029 rows at
`corpus/lessons/round-17.md:51-52` (Gate, "Opened sources and located quotes", header
`Contiguous quote (≤25 words)`).

## Verdict

**Bounded no-finding on every factual element of the row and on both quotes.** The anchor,
tier, scope, teaches and status reproduce against today's upstream; both quotes are exact,
≤25 words, and at the claimed locations. Two low-severity calibration/reproducibility gaps and
one nit follow.

## Verbatim observations

| # | Command (abridged; full URLs) | Observed |
|---|---|---|
| 1 | `curl -sSL https://github.com/NationalSecurityAgency/ghidra/releases.atom` then `sed -n '8,26p'` | HTTP 200, 12439 B. First entry: `<updated>2026-09-21T17:38:59Z</updated>`, `<title>Ghidra 12.1.4</title>`; next entries 12.1.3 / 12.1.2 / 12.1.1 / 12.1 |
| 2 | `curl -sSL https://raw.githubusercontent.com/NationalSecurityAgency/ghidra/Ghidra_12.1.4_build/Ghidra/Features/Base/src/main/java/ghidra/app/util/bin/format/golang/rtti/GoRttiMapper.java` | HTTP 200, 41672 B; `sha256sum` = `2415ceba3ea5250774fff51d43f6b22656a83713372f090701a10e49ad581d95`; line 79 = `\tpublic static final GoVerRange SUPPORTED_VERSIONS = GoVerRange.parse("1.15-1.25");` |
| 3 | same URL under `master` | HTTP 200, 41895 B; sha256 `0712837a21754b42d3b2deb19ef5e37d829ea5ea87dd59a4232445f67d7c36cd`; line 79 = `\tpublic static final GoVerRange SUPPORTED_VERSIONS = GoVerRange.parse("1.15-1.26");` |
| 4 | `unzip -p .../ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip ghidra/app/util/bin/format/golang/rtti/GoRttiMapper.java \| sha256sum` and `sed -n 79p` | `2415ceba…581d95` (byte-identical to #2); line 79 = `\tpublic static …("1.15-1.25");` |
| 5 | `git ls-remote --tags https://github.com/NationalSecurityAgency/ghidra.git` (version-sorted tail) | highest tag `Ghidra_12.1.4_build`; no 12.2/13.x tag |
| 6 | `git ls-remote … HEAD refs/heads/master refs/heads/patch refs/heads/stable` | `HEAD`/`master` = `b8e9917e4c01959fe97ba94954731ed8cf2d201c`; `patch` = `8b6bbb857accdfa20dc5b2f5dea471178c2e9fbc`; `stable` = `e46d08667b10125c191055a4de1610b1c63eb7bd` |
| 7 | `curl -sSL …/commit/385e8cd923d09f10b1a7874108e71748875fa174.patch` | HTTP 200, 10570968 B; `Subject: [PATCH] GP-6528 add support for golang 1.26`; `Date: Tue, 3 Mar 2026 19:52:38 +0000`; line 151 = `+\tpublic static final GoVerRange SUPPORTED_VERSIONS = GoVerRange.parse("1.15-1.26");` |
| 8 | `strings -a` on `Base.jar` member `ghidra/…/rtti/GoRttiMapper.class` | `grep -cE '1\.26\|1\.27'` = **0**; single constant `1.15-1.25` (line 533 of `strings`) |
| 9 | tag `Ghidra_12.1.4_build` `Ghidra/Configurations/Public_Release/src/global/docs/ChangeHistory.md` | HTTP 200, 491055 B; sha256 `c6b25301cda77dca1683a2a1802d84256d35625cf8959cdced144579486f65c4` = installed `docs/ChangeHistory.md`; line 1 `# Ghidra 12.1.4 Change History (September 2026)`; `grep -c '1\.26'` = **0**; newest Go line 585 `Added support for Golang 1.24 and 1.25. … (GP-5470)` |
| 10 | master `ChangeHistory.md` | line 1 `# Ghidra 12.2 Change History (October 2026)`; line 19 `* _Analysis_. Added support for Golang 1.26.0. (GP-6528, Issue #9013)` |
| 11 | `curl -sSI …/releases/latest` | HTTP 302 → `…/releases/tag/Ghidra_12.1.4_build` |
| 12 | master `WhatsNew.md` grep `1.26\|1.27\|Golang`; master `go1.27.0.json` / `go1.26.0.json` | no 1.26/1.27 line; `go1.27.0.json` **404**, `go1.26.0.json` **200** |

## Field-by-field on S029

- **anchor** — reproduced exactly: tag `GoRttiMapper.java:79` = 1.15-1.25 with the recorded file
  sha256 `2415ceba…581d95` (also byte-identical to the installed `Base-src.zip` member, to `patch`
  tip, and to `stable` tip — both fetched files also sha `2415ceba…` with line 79 = 1.15-1.25);
  master `:79` = 1.15-1.26; feed newest `Ghidra 12.1.4` at `2026-09-21`; no later tag
  (`git ls-remote`); `releases/latest` redirects to `Ghidra_12.1.4_build`.
- **tier `A`** — consistent with every existing `kind=code` row (S003, S004, S005, S013, S017);
  the registry has no tier-definition table, so this is a bounded consistency check, not a rule check.
- **scope** — accurate: the released line (source, compiled class, and ChangeHistory) declares
  1.24/1.25 only; 1.26 appears only on master (source line 79 + unreleased 12.2 ChangeHistory:19).
- **teaches** — all three clauses hold: (i) released line = 1.15–1.25 (source + `.class` constant
  + ChangeHistory, zero `1.26` strings); (ii) GP-6528 commit `385e8cd…` changes exactly that line
  to 1.26 and the change is in master's 12.2 section, with no 12.2 tag/release; (iii) no observed
  source declares 1.27 (GoRttiMapper master/tag/patch/stable, master ChangeHistory, master
  `go1.27.0.json` 404).
- **status `mined`**, **opened 2026-10-20**, **recheck `on-release`**, **used-by** — match registry
  convention; the knowledge entry does cite S029 (`corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:1`).

## Quotes

- `round-17.md:51` — location `https://raw.githubusercontent.com/…/Ghidra_12.1.4_build/…/GoRttiMapper.java, line 79`;
  quote `public static final GoVerRange SUPPORTED_VERSIONS = GoVerRange.parse("1.15-1.25");`.
  Verbatim check: `q1 in tag_line79` → **True**; words = **7**. Contiguous and ≤25.
- `round-17.md:52` — location `https://github.com/…/commit/385e8cd…patch, patch line 151`;
  quote `+` + tab + `public static final GoVerRange SUPPORTED_VERSIONS = GoVerRange.parse("1.15-1.26");`.
  Verbatim check: `q2 in patch_line151` → **True**; words = **8**. Contiguous and ≤25.

## Findings

### F1 — Low (calibration / provenance): the 1.26-range quote is booked under S029 but its location is S004's registered source; master's `:79` has no quote at its declared location

Evidence:
- `corpus/SOURCES.md:10` registers `https://github.com/NationalSecurityAgency/ghidra/commit/385e8cd923d09f10b1a7874108e71748875fa174` as **S004** ("Ghidra GP-6528 Go 1.26 support commit").
- `corpus/lessons/round-17.md:52` uses that same URL under ID **S029**.
- `corpus/SOURCES.md:35` asserts `master :79 "1.15-1.26"`, but neither lesson row quotes master
  at `:79`; the only 1.26 quote is the commit patch. The master quote existed upstream of the
  Gate table: w1 `.ufo/waves/round-17/w1/ScoutGhidraUpstreamGo.md` §2 quotes master `:79` directly.
- `grep -c S004 corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md` → **0**; the entry cites
  S029 for the upstream range but never cites the source that actually owns the GP-6528 change.

Impact: no fact is wrong — I independently fetched master `:79` = 1.15-1.26 — but the same commit
URL is booked under two registry IDs in the same evidence table, and the anchor's
master-side statement is evidenced by a different artifact than the one it names. This is the
origin-conflation pattern the round's C1 axis is meant to remove.

Smallest fix: in `round-17.md:52`, change the location cell to
`https://raw.githubusercontent.com/NationalSecurityAgency/ghidra/master/Ghidra/Features/Base/src/main/java/ghidra/app/util/bin/format/golang/rtti/GoRttiMapper.java, line 79`
and the quote to `public static final GoVerRange SUPPORTED_VERSIONS = GoVerRange.parse("1.15-1.26");`
(8 words; drop the `+`/tab). If the commit quote is preferred, relabel that row `S004` instead.

### F2 — Low (reproducibility): master anchor is ref-only while the tag anchor is byte-pinned

Evidence: `corpus/SOURCES.md:35` records the tag file sha256 but pins master only as `:79`.
Today master HEAD = `b8e9917e4c01959fe97ba94954731ed8cf2d201c`, master file sha256 =
`0712837a21754b42d3b2deb19ef5e37d829ea5ea87dd59a4232445f67d7c36cd`, and line 79 is 1.26.

Impact: after the next master push, a rechecker cannot tell which master state the row quoted;
the line number alone is underdetermined. The asymmetry is visible inside the same cell.

Smallest fix: append `master HEAD b8e9917e4c01959fe97ba94954731ed8cf2d201c, file sha256
0712837a21754b42d3b2deb19ef5e37d829ea5ea87dd59a4232445f67d7c36cd` to the anchor (same pattern
already used for the tag).

### N1 — Nit: quote #1 omits the line's leading tab

`round-17.md:51` quotes `public static …` while the actual line begins with a tab
(`'\tpublic static …'`). The quote is still an exact *contiguous substring* of the claimed line
(verified True), so `≤25 words` and "location correct" hold; only the indentation is not verbatim.
Smallest fix: include the tab inside the code span, or append "(leading tab omitted)".

## Adjacent corroboration (outside the row, checked because it is what S029 is cited for)

`corpus/SOURCES.md:65` says "master's unreleased 12.2 ChangeHistory names Go 1.26" — confirmed:
master ChangeHistory title is `Ghidra 12.2 Change History (October 2026)` and line 19 is the
GP-6528/Issue #9013 Go 1.26.0 entry. The installed 12.1.4 `docs/ChangeHistory.md` (sha
`c6b25301…`) is byte-identical to the tag's and contains zero `1.26`, so "released vs master"
is a real distinction, not a stale-install artifact.

## Limits

- GitHub REST API returned HTTP 403 (unauthenticated block), so commit metadata came from the
  `.patch` body (subject/date) and the master ChangeHistory, not the API.
- I did not re-run the w1 `git`-clone ancestry/pickaxe analysis; the row does not claim fork
  topology, and tag content plus `git ls-remote` already settle every element in the row.
- Master is a moving ref; observations are as of 2026-10-20 (~11:05–11:15 -03) at HEAD
  `b8e9917…`, the same HEAD recorded by w1.
- Tier `A` has no written definition table in `corpus/SOURCES.md`; checked only against existing
  `kind=code` rows.

## Tooling

No installs or upgrades. Scratch under `/tmp` (`/tmp/s029_*`, `/tmp/s029jar`). Wrote only this
report.
