# C1ScribeProvince — R49-C1 landing blocks and draft binding check (pre-freeze, wave 1)

**Verdict: DRAFT NOT FREEZE-READY on the landing and binding side.** The draft counter's regexes accept all three draft landing blocks (exit 0), but draft block B names the wrong superseded note and draft block C carries the round-44 label; both are corrected in `C1ScribeProvince/block-b.md` and `block-c.md`, which pass the same regexes and compose into the base `PROVINCE.md`/`corpus/README.md`. Two binding gaps (frontier-note token and province row) are satisfiable by text that contradicts the claim; they should be folded into the draft counter before the freeze.

Lane base `e4f2cfa5ebff863a4d5d13c040cb0c41be6a40f9`. Draft counter `c1-counter.py` sha256 `d6d70cb7ecc789b5ac0b0cbb7ee5b656abeea395cea9a158249d9a4723a95779`. Nothing under the lane was edited; no git mutation; no data run; no installs (no tools added).

## Findings

| # | Sev | Finding | Evidence (exact command → result) | Action for L1 |
|---|---|---|---|---|
| F1 | high (landing) | Draft block B says it supersedes "the round-42 frontier note above". The assignment and the plan's round-44 history name the round-44 `measured, not promoted` section (`## Round-44 measured, not promoted (R44-C1 honest stop)`, base `PROVINCE.md:424-430`) as the note being superseded. Round-42 `PROVINCE.md:416` also carries the v1/v2 Frontier clause. | `git show e4f2…:PROVINCE.md \| sed -n '424,430p'`; draft `round-49/w1/artifacts/R49C1Doc/block-b-…md` text "supersedes the `SquashFS v1/v2` clause of the round-42 frontier note above and nothing else" | Use `w1/C1ScribeProvince/block-b.md` (names round-44 section, round-44 frontier note and round-42 v1/v2 clause). Counter is unchanged by this (token check still passes). |
| F2 | med (landing) | Draft block C labels the new README row `SquashFS v1/v2 through REA (round 44)`. Every existing row names its own round (`README.md:101,103,104`). The row is also inserted after the round-44 row, which stays as history (same convention as rows 91/93 and 96/97). | `git show e4f2…:corpus/README.md \| sed -n '104p' \| cut -c1-60` → round 44 row; draft block-c first cell `(round 44)` | Use `w1/C1ScribeProvince/block-c.md`: `(round 49)`; insert after README line 104, before the blank line preceding `## Knowledge` (line 106). |
| F3 | high (binding) | Frontier-note token is vacuous. `SQFS12_TEXT_RE` (`c1-counter.py:327`) matches `squashfs-v1` inside the entry stem `2026-10-28-r49-squashfs-v1v2-core` itself, which the same line must carry. A line with only the stem and "moved Frontier -> Core" passes; so does a line saying SquashFS v1/v2 "stays Frontier". The module docstring says the frontier note "supersedes the `SquashFS v1/v2` Frontier text" (docstring ~line 30) — the binding (`c1-counter.py:2161-2162`) checks only a token, not supersession or direction. Plan vs counter disagreement. | `python3 -I -B C1ScribeProvince/vacuity.py` → `V1 … True squashfs-v1`; `V1b … True`; `token from stem -> squashfs-v1` (exit 0; `vacuity.out` sha256 `77159235…`) | Before freeze: require the frontier line to contain `supersedes` and a round-44 anchor (`Round-44` or `2026-10-28-r44`), or drop "supersedes" from the docstring and plan prose. Keep the round-44 anchor check since it is the claim's own predecessor. |
| F4 | med (binding) | Core-row binding accepts a row that says the opposite. `province_core_row` (`c1-counter.py:2156-2158`) checks only `squashfs_v1` + `squashfs_v2` literals, a SQFS12 match (satisfied by the entry path, see F3) and the entry path. A row reading "still Frontier, NOT Core" passes. The plan's sentence does not require Core wording, so this is a plan-level gap, not a plan/counter mismatch. | `vacuity.py` → `V2 contrary Core row passes: True` | Pre-freeze decision: add a not-Frontier/`not promoted` exclusion on the row, or state in the plan that the row is an index row and the claim's Core status rests on the `## Round-49 additions to Core` heading plus the receipt. |
| F5 | high (binding; plan says "re-opened") | `sourced` does not discriminate a round-49 re-open. Base `corpus/SOURCES.md` rows S138 and S139 already carry `opened` = `2026-10-28` (cell 8) and `used-by` = the round-44 entry. The counter (`c1-counter.py:2185`) accepts the date and any `used-by` containing the r49 entry; the plan says the rows were "re-opened this round (access date in `corpus/lessons/round-49.md` `## Gate`)", and no binding reads that Gate. A landing that only appends the r49 path to `used-by` passes. | `git show e4f2…:corpus/SOURCES.md \| python3 -c …` → S138 `col8='2026-10-28' col10='corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md'`; S139 same | Pre-freeze: bind the re-open to a row-level fetch stamp that differs from round 44 (e.g. a `fetched` cell with the round-49 sha256 or a `snapshot` path under `corpus/evidence/round-49/`), or disclose as a limit. |
| F6 | low | Block-A's AFTER-DATA marker pre-states the expected headline (`carriers_matched 4`, exit 0). A landing that is not replaced would carry the prediction; the counter does not read landing numbers, so nothing binds them to the receipt. | `compose_check.out`/`regex_check.out` show the marker | Marker wording should not contain the target value; L1 replaces every marker with the receipt before commit of the landing. |
| F7 | low | Block-B is headline-conditional on the data run. Draft text asserts "moved Frontier -> Core" unconditionally. | block-b draft | `block-b.md` wraps that phrase in an AFTER-DATA marker; the regexes still pass (see below). |

## Regex evidence (counter constants imported from the draft counter; no bytecode written)

Command: `python3 -I -B C1ScribeProvince/regex_check.py` → exit 0, output in `C1ScribeProvince/regex_check.out` (sha256 `15248c2fc55be428f42937de4bcfb384e856ef662d834d40ec24fabd7264c96f`).

- constants: `CORE_HEADING` = `## Round-49 additions to Core`; `FRONTIER_MARK` = `Round-49 frontier note`; `STEM` = `2026-10-28-r49-squashfs-v1v2-core`; `ENTRY` = `corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md`
- `SQFS12_TEXT_RE` = `squashfs[ _-]?v?1(\.0)?|squashfs[ _-]?v?2(\.0)?|squashfs\s+[12]`
- draft block A: section found; row `squashfs_v1`/`squashfs_v2` True, SQFS12 match `'squashfs_v1'`, ENTRY in row True → `province_core_row = True`
- draft block B: frontier line matched, SQFS12 match `'SquashFS v1'` → `frontier_note lines matched = 1`
- draft block C: `coverage_map_row = True`, 3 cells, label `(round 44)`
- AFTER-DATA markers found in drafts A and C (2)

Composed check against base: `python3 -I -B C1ScribeProvince/compose_check.py` → exit 0 (`compose_check.out`, sha256 `b660c7fde4b6d58ee3fe13a859a003256e623e754f18b3b39106f4ef1d282a7e`):
- `province_core_section = True`, `province_core_row = True`, `frontier_note = True`, `coverage_map_row = True`
- composed files: `C1ScribeProvince/PROVINCE.composed.md`, `README.composed.md` (base + corrected blocks, block A appended after the round-44 note, block B after it, block C after README line 104)

Corrected blocks (same regexes, same counter):
- `block-a.md` sha256 `a3a0baf7…` (= draft text plus one trailing blank line; diff exit 1 only on that line)
- `block-b.md` sha256 `ca3256cb…` (supersedes the round-44 section and frontier note, the round-42 v1/v2 clause; AFTER-DATA on the Core verb)
- `block-c.md` sha256 `625531b8609469f326bf7be45f73d429735720e864c59009f4156df8ca312797` (label `(round 49)`)

## Source re-open (pre-freeze, status + size + sha256; body not stored in the report)

| source | command | result |
|---|---|---|
| S108 unblob `squashfs.py` @26.6.4 | `curl -s -m 40 https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/handlers/filesystem/squashfs.py` | HTTP 200, 19842 B, sha256 `2d7b901b54e2ad28c28df2cbbdaeb4bcedb58670fb4c4478f9578a0dd5599287` = S108 row hash; locators block A cites verified in snapshot `round-38/w1/artifacts/R38ScoutUnblobHandler/squashfs.py.26.6.4.txt`: :24-26 EXECUTABLE/V4BE names, :51-54 `-be`/`-le`, :68-69 `get_dependencies`, :101-102 `squashfs_v1` class/NAME, :158-159 `squashfs_v2` NAME (all exact) |
| S139 squashfs-tools releases API | `curl … https://api.github.com/repos/plougher/squashfs-tools/releases` | HTTP 200, 48840 B, sha256 `2d444a95680bcf680907813f388c5cda69f01c0bbb808a354ec70f6b01b36d72`; not parsed for the 4.7.5 entry (not run) |
| S138 unblob git tree @1fcc7a0a | `curl … https://api.github.com/repos/onekey-sec/unblob/git/trees/1fcc7a0a584a70a96c31f5a276c20944d199a089` | HTTP 200, 7993 B, sha256 `a54cb319f1cdc7dae029f65b4777a642a46d60b1ea7b1771820d4bbe10cf2fe1`; member-level re-derivation not run |
| carriers | `sha256sum` of `git show e4f2…:corpus/evidence/round-42/c2/fixtures/{v1-le,v1-be,v2-le,v2-be}…` | all 4 at 4096 B; prefixes `b45925fa…`, `529e1077…`, `7c62dbe3…`, `79c0f388…` equal `carriers.json` sha256 values; block-A pins cite these prefixes correctly |
| oracle | `/usr/bin/unsquashfs -version` | `unsquashfs version 4.7.5 (2026/03/01)` |
| sasquatch | `command -v sasquatch` | `/home/vgpnk/.local/bin/sasquatch`, 382824 B; version string not checked (not run) |

## Not run

- Full draft counter run (`c1-counter.py` on a clone) — out of scope pre-freeze; regex-level and composed binding checks only.
- Data runs (`c1-run.sh --data-run`) — forbidden for seats.
- Full S138/S139 member/row re-derivation beyond status, size and hash.

## Tools / installs

None installed or upgraded (no tool gap in this seat's scope).

## Artifacts (`.ufo/waves/round-49/w1/C1ScribeProvince/`)

`block-a.md`, `block-b.md`, `block-c.md` (landing text); `PROVINCE.composed.md`, `README.composed.md` (composed base); `regex_check.py`/`.out`, `vacuity.py`/`.out`, `compose_check.py`/`.out` (evidence). Scratch `/fast/scratch/hyaku/kaidoku-r49/C1ScribeProvince` removed after copy.

## Housekeeping note

One copy was initially written into a nested path inside this seat's directory and moved to the correct level in place; no lane path outside `w1/C1ScribeProvince/` was touched.
