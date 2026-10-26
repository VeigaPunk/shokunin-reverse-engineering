# R39RevCensus — SOURCES.md registry census readiness (round 39 wave 1)

DONE — registry gate is green and append-ready: pre-check exit 0, 117 rows S001–S117
contiguous, next free id **S118**, template/rules extracted, and the scratch mirror test
passes for well-formed in-section appends while failing closed on a malformed (escaped
pipe) row. One placement rule discovered and documented: rows must be inserted inside
`## Registry` (EOF appends fail with E12).

## 1. Registry pre-check (required first step)

Command (from fleet root):

```
cd /home/vgpnk/Projects/shokunin && ./scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku
```

Output (full transcript: artifacts `validate-precheck-kaidoku.txt`):

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
kaidoku	W04	S112 duplicate url raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/handlers/filesystem/squashfs.py across scopes
kaidoku	W04	S117 duplicate url raw.githubusercontent.com/onekey-sec/unblob/26.6.4/README.md across scopes
kaidoku	ok	/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md
EXIT_CODE=0
```

Eleven pre-existing W04 warnings (same URL cited from rows with different scopes).
Per the script's own contract ("W-codes … never change status"), the lane validates **ok,
exit 0**. The stray backtick in the S047 line is printed by the validator itself
(observed output verbatim); cause not traced [INFERENCE: cosmetic artifact of the
script's URL normalization over a backtick-quoted source cell].

## 2. Contract and shape

Read: `CORPUS.md` §"SOURCES.md — where a shokunin learns" (contract v1, kaika
2026-10-19, frozen — lines 63–140 of `/home/vgpnk/Projects/shokunin/CORPUS.md`) and the
live registry header + rows S110–S117. Contract shape: one Registry table, then
`## Paths`, `## Search log`, `## Leads (unopened)` — all present in the lane file
(219 lines; S117 is the last registry row at line 123).

The exact 11-column row template, the filled-row shape, enum values, placement rule,
and gate-code cheat sheet are delivered in artifacts `S118-row-template.md`; the exact
dummy rows are in `dummy-rows-snippet.md`.

## 3. Next free id

Assignment command:

```
$ grep -cE '^ {0,3}\| S[0-9]{3}' corpus/SOURCES.md
117
GREP_EXIT=0
```

Cross-checks: the contract's own spacing-tolerant counter
`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` also prints 117; `validate` raises
no E02 (id shape) or E03 (duplicate id); the highest id present is S117 (read directly).
Ids are contiguous S001–S117, so the next free id is **S118**.

## 4. Rules for used-by / status / recheck cells

From the contract bullets, rule 2 (append-only; only `status`, `recheck`, `used-by`
change in place, logged old→new; corrections are new rows opening `supersedes S0NN —`),
and the gate's enforced semantics:

- **status** ∈ `queued` (opened, worth mining) · `mined` (cited by ≥1 path in used-by) ·
  `rejected` (kept; `teaches` reads `REJECTED: <reason>; flip: <what would change the
  verdict>`). `watch` is not a status → E07. Current lane histogram: mined=112,
  rejected=5, queued=0.
- **recheck** ∈ ISO date · `NNd` cadence (`90d`, `180d`) · symbolic (`on-release`,
  `annual`); else E09. `overdue` mode reports ISO/`NNd` rows on/after due date
  (due = opened + N days) and only REPORTS symbolic cadences.
- **used-by** — lane-root-relative repo paths of the knowledge entries/lessons citing the
  row, comma-separated, or `—`. Gate checks existence of every path on a `mined` row
  against the lane root (E11); `mined` with `—` → W03; tier-C `mined` with paths → W01.
  This lane cites 54 distinct used-by paths, all present on disk (checked; zero missing),
  under `corpus/knowledge/`, `corpus/lessons/`, `tools/round-27/`, and lane-root
  `SKILL.md`.

Full template + gate codes: artifacts `S118-row-template.md`.

## 5. Scratch mirror test (`--file` mode)

Setup: copies of the registry in scratch with the lane's 54 used-by paths symlinked at
their lane-relative locations (the gate resolves E11 paths against the tested file's
grandparent directory, verified in the script: `resolve_targets` +
`usedby_findings "$f" "$dir" "$lane"`), then:

1. **Well-formed append, inside `## Registry`** (S118, S119 inserted directly after the
   S117 line): gate prints only the 11 pre-existing W04 warnings and
   `file ok <mirror path>`, **exit 0**. Transcript: `mirror-valid-run.txt`.
2. **Malformed row** (S120, same placement, `teaches` contains an escaped pipe `\|`):
   `awk -F'|'` counts the pipe as a column separator → 13 textual cells instead of 11 →
   `file	E01	S120 fields=13`, **exit 1**. (E01's message prints awk NF−2, i.e. the
   cell count — script line 636.) Transcript: `mirror-bad-run.txt`.
3. **Placement demonstration** (S118, S119 appended at EOF after `## Paths`): both rows
   rejected with `file	E12	S118/S119 row outside Registry section`, **exit 1** — even
   though each row is individually well-formed. Transcript:
   `mirror-eof-append-E12-demo.txt`. Rule for the freeze: **insert new rows after the
   last registry row (currently S117), never at file end.**

## 6. Contract census snippets (cross-check on the live registry)

Transcript: `census-snippets-kaidoku.txt`.

```
== NF!=13 (must print 0)
0
== tier histogram
A=109 B=7 C=1
== status histogram
mined=112 rejected=5
== duplicate ids (must print nothing)
== missing used-by paths (must print nothing)
== contract row count (spacing-tolerant)
117
```

No malformed rows, no duplicate ids, no dangling used-by paths. 54 distinct used-by
paths, all present on disk.

## 7. Environment notes

- No tools installed or upgraded for this item (operator 2026-10-19 authorization
  unused): the gate needs bash + coreutils + gawk, all present; scratch file
  construction used Python stdlib only.
- Scratch `/fast/scratch/hyaku/kaidoku-r39/R39RevCensus` (mirror lanes, symlinks) was
  used for the tests and removed after transcripts were captured into the artifacts
  dir. Read-only operations on the fleet repo and the lane; no VCS mutation; no writes
  outside my artifacts dir and my report file.

## 8. Artifacts

- `validate-precheck-kaidoku.txt` — pre-check transcript + exit code
- `row-count-grep.txt` — assignment count command + exit
- `S118-row-template.md` — exact 11-column template, enums, placement rule, gate codes
- `dummy-rows-snippet.md` — the exact S118/S119/S120 test rows
- `mirror-valid-run.txt` — well-formed in-section append → ok, exit 0
- `mirror-bad-run.txt` — escaped-pipe row → E01, exit 1
- `mirror-eof-append-E12-demo.txt` — EOF append → E12, exit 1
- `census-snippets-kaidoku.txt` — contract census snippet outputs

## 9. Residual risk / verification gaps

- The 11 W04 warnings are pre-existing lane state (cross-scope duplicate URLs). They do
  not block the freeze, but if the fleet wants a warning-free census before freeze, the
  L1 should decide whether any become `supersedes` rows. Not my call; flagged only.
- The validator's URL normalization printed a stray backtick for S047 (observed); not
  traced to the exact code path [INFERENCE: cosmetic].
- E04 (duplicate URL+scope) semantics were exercised only via the script's selftest
  fixtures and docstring, not by a kaidoku-specific probe — the live registry has no
  duplicate-URL-same-scope case to trigger it. W-code/E-code coverage of the live lane
  is otherwise complete for the codes reachable by the lane's current content.

Report: .ufo/waves/round-39/w1/R39RevCensus.md
