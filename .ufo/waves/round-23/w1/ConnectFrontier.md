# ConnectFrontier — where the round-23 signal addition has to go

Seat: `KaidokuR23.ConnectFrontier` (connector, leaf). Read-only except this
report. No REA probe, no carrier run, no device, no delegation, no install.
Author-side findings; **nothing here is outside verification, and the proposed
move is not claimed as verified.**

Axes named from `.ufo/waves/round-23/claims.json:5-10`: **coverage 10** (the
axis the lowest-axis rule assigns), **depth 10**, **calibration 10**. This seat
proposes one bounded move aimed at *calibration* and *coverage legibility*; it
does not manufacture k and must not be counted as coverage evidence.

Base: `git rev-parse HEAD` → `a3c92eb6bc70984e90ae5b895412de978840b2c5`,
exit 0. Blob sha256 at that rev (`git show a3c92eb:<path> | sha256sum`, exit 0):

| path | sha256 |
|---|---|
| `PROVINCE.md` | `dbf757fec564e1fdb5497cf773dbd11021a5f464ecab2802f780a1c78691ed97` |
| `SKILL.md` | `4898fa74bd691e82ff89bb91caa51bd6673d567288243fd59d21d848a13a8ad8` |
| `corpus/README.md` | `33c979d3c9d0ccf886f0bac423d3e5540c27b74d59a292538a50d0a1d1a0812d` |
| `corpus/SOURCES.md` | `5ae5e7ed539d092d801d1c521cb3a0cfa6d89ff82e38b8d86c0c8d5b4f777ebd` |

Line counts at that rev: `SKILL.md` 706, `PROVINCE.md` 218, `corpus/README.md`
196, `corpus/SOURCES.md` 115. The live worktree changed during this seat's run
(O12): `corpus/README.md` and `corpus/SOURCES.md` are modified and a new
round-23 knowledge entry exists; all anchors below are stated twice — committed
rev `a3c92eb`, and live-worktree line where it differs.

## Evidence

**O1 — the only lane-level sigrok disposition is one present-tense sentence.**
`git grep -n -i sigrok a3c92eb -- '*.md'` exits 0. In the lane's own documents
the only hit is `PROVINCE.md:217-218` (wrapping there):

> "The sigrok verbs remain unexercised; no recording decode or hardware
> contact is claimed."

Every other hit is a round-22 w2 seat report, a luna receipt, or a tool listing
(`.ufo/waves/round-22/w2/PrimarySigrok.md`, `SchemaDecodeSignalRecording.md`,
`.ufo/waves/luna-round-2/L13.md:15`). `corpus/`, `SKILL.md` and `LOG.md` contain
**no** sigrok row, bullet or route. The R22 seat that mined the sigrok page
already mispoints this sentence: `.ufo/waves/round-22/w2/PrimarySigrok.md:7`
says "`PROVINCE.md` line 205 still holds: the remaining signal verbs stay
unclaimed", but `:205` is now the `### Round-22 narrowly added static ground`
heading, not the sigrok text. [Observation]

**O2 — that sentence is an instant claim inside a section R22's verifier
byte-pins.** It lives in `### Round-22 narrowly added static ground`
(`PROVINCE.md:205`). R22's verifier proves its own partition by string
concatenation: base `PROVINCE.md` + `### Round-22 catalog dispositions` +
`### Round-22 narrowly added static ground` == final file
(`.ufo/waves/round-22/verify.py:183-190`, check
`province-section-partition-exact`). Consequence [inference]: any edit inside
those blocks, or insertion above them, breaks that check; a **third** `###`
appended after `:218` is swallowed by the `static` split and leaves the
concatenation true.

**O3 — the Dart refusal is stated without its cause.** `PROVINCE.md:211-212`
says `inspect-dart-aot` "refused Saber's missing dynamic snapshot symbols" and
stops there. The installed REA 6.5.0 reader searches exactly four pre-3.13
dynamic names — `_kDartVmSnapshotData`, `_kDartVmSnapshotInstructions`,
`_kDartIsolateSnapshotData`, `_kDartIsolateSnapshotInstructions` —
`flutter/FlutterBuildProvider.js:598-603` (read directly; the package root
`/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist` is the
S048 root). Peer seat `KaidokuR23.CriticSource` supplied, as **their**
observation (not re-run here), the version pins: tag 3.12.0
`98116461144f4429ab873f8497023a5ec3b08127` still has `_kDartVmSnapshotData`
in `runtime/include/dart_api.h` (sha256 `da42f9d2…`); tag 3.13.0
`da6595cd6bb5d4c0a185d759a025e879ff06e631` has only
`_kDartSnapshot{BuildId,Data,Text,Bss}` (`dart_api.h` sha256 `d5009bb2…`,
same bytes as 3.13.6); rename commit `d36adbacafee01d9852cf8e960cf2d8654d91e7e`
kept old-name aliases that are gone by tag 3.13.0. Consequence [**inference**]:
a carrier that does not export the four legacy names in `.dynsym` refuses; the
reader does not establish Dart absence, source recovery or execution. CriticSource's
correction is kept: "a carrier needs Dart <=3.12" is an inference, not an
observation, because legacy-name *export* is per-carrier.

**O4 — SKILL's decision table cannot take a row without renumbering 20
citations.** The table ends at `SKILL.md:66`; a script over `git ls-files`
(`*.md,*.json,*.py,*.txt`, `.ufo/` excluded — this repo's own citation style
`FILE.md:<n>[-<m>]`) counts 27 citation sites into `SKILL.md`, **20 of them at
or after line 66**, maximum cited line 540. Exit 0. [Observation]

**O5 — README's index regions are mid-file and heavily cited.** Coverage-map
rows end `corpus/README.md:71`; Knowledge rows end `:158`; Frontier `:176-187`;
EOF `:196`. The same script counts 29 citation sites into
`corpus/README.md`, **23 at or after line 71**. `PROVINCE.md` has 65 sites but
none at/after `:205` — so an EOF append to PROVINCE moves nothing, and an
insertion anywhere earlier moves many. [Observation]

**O6 — five pointer-table entries are already dead at the frozen rev, from
exactly this growth.** Of the 12 `extracted` entries that name `corpus/README.md`,
`SCORECARD.md` or `SKILL.md`, 5 fail. Hand-replicating `check_entry`'s `extracted` branch
(`.ufo/gates/citation-drift/citation-drift-probe.py:252-305`) against a3c92eb
gives:

| entry | citing line | resolves to | verdict |
|---|---|---|---|
| `sc69-readme-177` | `SCORECARD.md:69` → `corpus/README.md:180` | `.jsc → source mapping` bullet | MISMATCH (needs "held, not frontier"; that bullet is now `README:186`) |
| `sc72-readme-nitrow` | `SCORECARD.md:72` → `corpus/README.md:138` | `r14-01-queue-b-residual` row | MISMATCH (nit row is now `README:140`) |
| `readme175-sc1217` | citing line `corpus/README.md:175` | now the `round-22` **Lessons** row | CITATION_DEAD (pattern absent) |
| `readme175-r7range` | same | same | CITATION_DEAD |
| `readme175-r8e2` | same | same | CITATION_DEAD |

The other 7 extracted entries that touch these files resolve OK. The
`>90MB PE` frontier bullet moved `175 → 181 → 186` across rounds. [Observation]

**O7 — the probe's verdict is fail-open without `--strict`.** `Findings.verdict`
returns CLEAN for any non-CNE finding when `strict=False`
(`.ufo/gates/citation-drift/citation-drift-probe.py:100-122`). A non-strict exit
0 therefore says "no unevaluable class", **not** "citations resolve"
(QUALITY #21 discipline). [Observation of source; consequence for any R23
"citation gate green" statement.]

**O8 — the right form is already written down in the table, and was only
partly applied.** `readme38-arc3r1-token` and `skill-registry-row` are `anchor`
kind with the line **deliberately unpinned**; the table's own note says "the
coverage map grows by rows and its numbering moves (the r10 `readme175`
lesson) … a row insertion is not drift here"
(`.ufo/gates/citation-drift/pointer-table.json`, those two entries). The
SCORECARD pointers and the frontier bullet never got converted — that is the
debt O6 measures. [Observation]

**O9 — the signal surface is env+version gated, file-only, and the provider
digest is independently re-derived.** `cli-runtime/cli.js:1192` pins
`sigrok-cli@0.7.2`; `:1234-1236` requires Linux and an **absolute**
`REA_SIGROK_COMMAND`; `:1240-1241` an absolute `REA_SIGROK_PRLIMIT_COMMAND`
(default `/usr/bin/prlimit`); `:1294` requires `--version` stdout to match
`^sigrok-cli 0\.7\.2` and contain `libsigrokdecode`. Contract text:
decoder discovery is "no recording, binary target, hardware scan or
acquisition" and "Each call probes again; decoder modules are trusted, not
fully fingerprinted"; recording decode is "File-only analysis; no hardware
acquisition or device communication. Empty output does not prove absence of
traffic", 50-line default windows, `line_limit:null` returns the rest
(`contracts/signals/signalToolContracts.js:5-38`). `sha256sum
signals/SigrokRecordingProvider.js` → `7979bafb84b463d0fc3040d3643e08362326d67fd4543ee690679dc88b2dced7`,
339 lines, matching R22 w2's recorded digest. [Observation; no verb run.]

**O10 — R22 already flagged the calibration hole this wave's synthetic decode
lands in.** `.ufo/waves/round-22/w2/SchemaDecodeSignalRecording.md:5`
("Calibration gap (new)") records that a success with
`output_window.total_lines: 0` is a bound non-refused record and the counter
would count it, while REA's own limitation says empty output does not establish
absence. [Observation of that report; inference that R23's UART payload must
decode to non-empty annotations and that prose must not call a zero-line window
a decoded payload.]

**O11 — a sigrok source row was mined in round 22 and did not land at the
frozen rev.** `.ufo/waves/round-22/w2/PrimarySigrok.md:51-57` drafts `S0xx`
(sigrok-cli wiki page, MediaWiki revision `16563`, contiguous 10-word quote,
"L1 assigns the id — the highest current is S053"). `corpus/SOURCES.md` at
`a3c92eb` still ends at `S057` (`:63`); S054–S057 are Flutter/Dart rows. O12
shows the live tree now appends `S058–S060`, but the R22 wiki-page draft is
**not** among them (S058 is the repo-pinned 0.7.2 manual), so re-using the draft
would be a new row, not a duplicate, and its `used-by` still names only the
seat report. Only 4 tracked non-`.ufo` line citations
into `SOURCES.md` exist (all `:30-:37`, one knowledge file), so an `S058+` row
appended after `:63` moves no cited line. [Observation]

**O12 — the live worktree changed under this seat: the signal addition is
already partly integrated, in-table, with net-zero line compensation.** After
the base hashes above were taken, `git status --porcelain` shows
` M corpus/README.md` and ` M corpus/SOURCES.md`, plus a new
`corpus/knowledge/2026-10-21-r23-offline-signal-envelopes.md`
(sha256 `7598d2cb436ceee4b6dc01c10869a9db0cd0f49afaf971aa02eb9f771aee6c35`)
and round-23 `evidence/c1/` envelopes. Observed state:

- `corpus/README.md` live sha256 `db0df6c5…`, still **196 lines**. Round-23
  rows sit at live `:72` (coverage map), `:159` (Knowledge), `:176` (Lessons).
  Each insertion is offset by deleting the blank line after the next heading,
  so `## Knowledge` moved `72→73`, `## Lessons` `159→160`, `## Frontier`
  `176→177`, while every *content* line below each insertion (table rows and
  Frontier bullets, incl. the `held, not frontier` bullet at `:186`) keeps its
  committed position. Measured by `nl -ba`. Consequence: no pointer-table entry
  targets those heading lines, and the `readme175-*` / `sc69-readme-177` /
  `sc72-readme-nitrow` pointers resolve exactly as they did at `a3c92eb`
  (already dead or already OK, unchanged). [Observation]
- `corpus/SOURCES.md` live sha256 `0b927b97…`, 118 lines (committed 115):
  `S058` sigrok-cli 0.7.2 manual, `S059` sigrok-dumps `hello_world` README,
  `S060` round-23 own-work envelopes, appended after `S057`. The four
  `SOURCES.md` line citations are above the insertion and unmoved.
- `PROVINCE.md` and `SKILL.md` are **not** modified — so the only lane-level
  sigrok sentence (`PROVINCE.md:217-218`, "unexercised") now directly
  contradicts the live README row that says the offline signal envelopes are
  "held narrowly". That contradiction is the remaining integration defect.
- The live Lessons row `round-23` exists while `corpus/lessons/round-23.md`
  does **not** (`ls` → "No such file or directory"). Recorded, not judged:
  README's own rule (`:9`) is "A row is written when its file exists, never
  before"; whether the lesson file lands in the same commit is L1's decision.
- This seat did not create or modify any of those files (read-only seat); the
  entry's counts were read, not re-run. [Observation]

## The gap, site by site

| site | current text | why an append-only addition (not an edit) |
|---|---|---|
| `PROVINCE.md:217-218` | "The sigrok verbs remain unexercised; no recording decode or hardware contact is claimed." | Present tense inside a byte-pinned R22 section (O2). A successful R23 decode makes it false as *current state*; deleting or rewriting it breaks the partition check and the no-harm rule. It can only be date-superseded by an appended block. |
| `PROVINCE.md:211-212` | Saber `inspect-dart-aot` refusal, no cause | The missing cause is a carrier-selection condition (O3), not a new capability. Appending the four-name gate changes no historical wording. |
| `SKILL.md:44-66` | decision table, no recorded-signal row; `:70-83` error table, no `REA_SIGROK_COMMAND` gate | A row at `:66` renumbers 20 citation sites (O4). The same content can live in an appended section with its own mini-table. |
| `corpus/README.md:71/:158/:176-187` | coverage-map tail, Knowledge tail, Frontier | **Already integrated in the live tree (O12)**: rows at live `:72`/`:159`/`:176`, each insertion offset by a removed blank line so content lines below keep their committed positions. Do not insert again and do not "improve" the placement in this round; the net-zero invariant is what keeps O6's pointer set from growing. |
| `corpus/SOURCES.md:63` | registry tail, S057 | **Already integrated live (O12)**: `S058–S060` appended after `S057`; the claim's `sourced:` requirement (QUALITY #29) is satisfiable from those rows. The R22 wiki-page draft remains unlanded and separate. |

## Proposed move (one bounded proposal)

**Two trailing blocks are still missing; land those and change nothing already
integrated.** `corpus/README.md` and `corpus/SOURCES.md` already carry the
round-23 signal addition in the live tree (O12) — preserve their net-zero
placement rather than re-litigating it. What remains is `PROVINCE.md` (its only
sigrok sentence now contradicts the live README row) and `SKILL.md` (no
recorded-signal route at all). For both, append at EOF: PROVINCE's 65 citation
sites all point above `:205` and the R22 partition check pins the section
boundaries (O2); SKILL has 20 sites at/after `:66` (O4). Then register the new
row token as an `anchor`-kind pointer, never a line pointer (O7/O8).

Draft text follows. `<…>` is L1's to fill from the retained envelope and the
write-time clock; nothing below may claim "held" before the counted record
exists.

**(A) `PROVINCE.md`, after `:218`** — new `###` section, nothing above edited:

```markdown
### Round-23 signal and Dart dispositions (appended 2026-10-21)

The `Round-22 narrowly added static ground` paragraphs above record the
round-22 instant and are not rewritten. Current state, appended here:

- `inspect-signal-decoders` / `decode-signal-recording`: exercised per
  `corpus/knowledge/2026-10-21-r23-offline-signal-envelopes.md` and its
  original envelopes under `.ufo/waves/round-23/evidence/c1/`. Discovery's
  subject is the launcher, not a recording, and its catalog retains a
  `signature` decoder load failure; decode retains literal sample-range
  annotations for the synthetic UART file and a 12,885-line window for the
  public recording, which is not described as a lossless payload. Gate read
  from the installed package:
  absolute `REA_SIGROK_COMMAND`; `--version` stdout must start
  `sigrok-cli 0.7.2` and contain `libsigrokdecode`; absolute
  `REA_SIGROK_PRLIMIT_COMMAND` (default `/usr/bin/prlimit`)
  (`dist/cli-runtime/cli.js:1192,1234-1241,1294`;
  `dist/contracts/signals/signalToolContracts.js:5-38`; provider sha256
  `7979bafb…`). File-only; no hardware acquisition. A window that decodes zero
  lines is a bound empty record, not decoded traffic.
- `inspect-dart-aot`: the Saber refusal was the four pre-3.13 dynamic names,
  which are the only names the installed reader searches
  (`dist/flutter/FlutterBuildProvider.js:598-603`). A carrier that does not
  export them in `.dynsym` refuses: a carrier-selection condition, not evidence
  of Dart absence, source recovery or execution. (Version-pin evidence for the
  3.12/3.13 rename is peer-observed, not this lane's run.)
- `debug-with-gdb` / `debug-with-rizin` remain **Adjacent and not held**.
  Nothing appended here grants tracer, process-attach, device or hardware
  ownership.
```

**(B) `SKILL.md`, after `:706`** — new route section with its own mini-table:

```markdown
## Recorded signals and Dart symbol names — round 23

| Target | First move | Status |
|---|---|---|
| Recorded logic/signal file | `inspect-signal-decoders` (list, or `decoder` + `query` help; `offset`/`limit`, default 50) -> `decode-signal-recording <path>` with explicit `--input-format`, samplerate, channel map and decoder stack (`uart:rx=RX:baudrate=9600`) | <L1 status from the retained envelope; never from availability> |

Gate and limits (installed 6.5.0 source): absolute `REA_SIGROK_COMMAND`; its
`--version` stdout must match `^sigrok-cli 0\.7\.2` and contain
`libsigrokdecode`; `REA_SIGROK_PRLIMIT_COMMAND` defaults `/usr/bin/prlimit`
(`dist/cli-runtime/cli.js:1192,1234-1241,1294`). File-only: no hardware
acquisition or device communication; decoder modules are trusted, not
fingerprinted. Output windows are 50 display lines by default;
`line_limit:null` returns the remaining lines without shortening decoding;
empty output does not prove absence of traffic
(`dist/contracts/signals/signalToolContracts.js:5-38`).

A typed refusal (`capability_unavailable` for the env gate,
`execution_failure` for a non-zero sigrok exit) is not a held decode, and a
zero-line window is not decoded payload. Discovery's subject is the launcher,
not a recording, and its catalog can retain a decoder load failure while still
returning a partial list; say which module failed rather than calling the list
complete.

Dart AOT: the installed reader searches only `_kDartVmSnapshotData`,
`_kDartVmSnapshotInstructions`, `_kDartIsolateSnapshotData`,
`_kDartIsolateSnapshotInstructions`
(`dist/flutter/FlutterBuildProvider.js:598-603`); a carrier that does not export
them in `.dynsym` refuses, which is a selection condition, not evidence of Dart
absence. Do not infer a Dart version from an unmapped snapshot hash and do not
count the refusal.
```

If L1 lands a round-23 counter, give it its own
`### Round-23 measurement registry` table in this appended section — do not add
a row to the round-22 registry at `:679-686` (that table is line-cited and its
content is `ReviewRegistryHome`'s, not this seat's).

**(C) `corpus/README.md` — already integrated; do not land the EOF form below.**
The live tree carries the round-23 rows in-table with net-zero compensation
(O12, live `:72`/`:159`/`:176`). The block below is the counterfactual EOF form
this seat proposed before observing that integration; keep it as a record of
the alternative, **not** as a pending patch.

```markdown
## Round-23 additions (appended; regions above stay frozen)

Appended rather than inserted because the index above is line-cited: the
coverage map ends with the round-22 "Partial Flutter positive and Dart refusal"
row, the Knowledge table with the matching entry, and the Frontier list with
the Blocked-on-operator bullet. Moving those lines is the defect class the
citation table already records (`readme175-*`, `sc69-readme-177`). A row is
still written only when its file exists.

| section | entries | state |
|---|---|---|
| Recorded signals (offline, sigrok-cli 0.7.2) | `knowledge/<entry>` | <state — env+version gate, file-only, zero-line caveat> |

| entry | topic | source | verified-at |
|---|---|---|---|
| `<entry>` | <one-line topic> | S0xx (sigrok-cli wiki, rev 16563) + S0yy (round-23 own-work envelope) | <date> |

Frontier additions:
- Dart AOT symbol naming — the installed reader resolves only the four
  pre-3.13 names; a newer carrier is a selection problem, not a decode result.
- Recorded-signal decode — the gate is an absolute env binary plus a version
  string; hardware acquisition remains out of scope.
```

If a second round-23 index row is ever needed, this trailing form is preferable
to another in-table insertion; for this round, no action.

**(D) `corpus/SOURCES.md` — already integrated; preserve (no action).**
`S058` (sigrok-cli 0.7.2 manual), `S059` (sigrok-dumps `hello_world` README)
and `S060` (round-23 own-work envelopes) are appended after `S057` in the live
tree, and the round-23 entry's `source:` line cites them, so QUALITY #29's
linkage is satisfiable from the landed rows. Do not touch `S051–S057` or any
earlier row. The R22 wiki-page draft
(`.ufo/waves/round-22/w2/PrimarySigrok.md:51-57`) remains unlanded and is **not**
a duplicate of S058 (different document: wiki page vs repo-pinned manual); if
L1 wants it, it is a new row with its `used-by` extended, not a copy.

**(E) `.ufo/gates/citation-drift/pointer-table.json` — one `anchor` entry, not a
line pointer** (instrument file; `SourceRegistry`/L1's to land): id
`readme-r23-signal-token`, kind `anchor`, file `corpus/README.md`,
`must_match` `2026-10-21-r23-offline-signal-envelopes`, note "round-23 row
token; line deliberately unpinned because the index grows by rows". This is the
same form the table already uses for `readme38-arc3r1-token` (O8). If L1 elects
not to touch the instrument this round, record the omission — do not pin the
row's line instead.

## Affected axes

| axis | effect | basis |
|---|---|---|
| calibration | **improves** — resolves the live contradiction between `PROVINCE.md:217-218` ("unexercised") and the landed README row ("held narrowly"), adds the Dart carrier-selection cause without touching historical text, and keeps every new reference token-anchored | O2, O3, O12, O6, O10 |
| coverage | **no k, legibility only** — the two verbs count only from the retained envelopes already cited by the landed entry; the remaining PROVINCE/SKILL blocks are prose and cannot move the counter | O9, O11, O12; counter reads evidence/SOURCES/knowledge |
| depth | neutral — no new probe content | this seat ran none |

## Risks and contradictions

1. **Append-only cannot make a present-tense sentence true.** After a
   successful decode, `PROVINCE.md:217-218` is false as current state while
   remaining correct as the round-22 instant. The appended block must name it
   as that instant (draft A does). If L1 instead rewrites `:217-218`, the R22
   partition check and the "historical claims unchanged" no-harm clause both
   fail; the contradiction is real and must be chosen, not smoothed.
2. **The landed in-table placement is net-zero, not line-free.** It moved three
   heading lines (`## Knowledge` 72→73, `## Lessons` 159→160, `## Frontier`
   176→177; O12) and paid for each inserted row by deleting a blank line. No
   pointer targets a heading today, but any later insertion without the same
   compensation moves the Frontier bullets that `readme175-*` and
   `sc69-readme-177` depend on. Re-measure those headings and bullet lines
   before any further index row.
3. **The citation gate is fail-open.** Without `--strict` it exits 0 with these
   findings present (O7). This move neither repairs nor worsens the five dead
   entries; do not report it as repairing them, and do not cite a non-strict
   exit 0 as resolution.
4. **PROVINCE/SKILL must stay pure additions.** For those two files the change
   must have deletions 0 (`git diff --numstat`); an in-table SKILL row or a
   PROVINCE edit above `:205` renumbers 20 / 65 citation sites.
5. **Source-linkage is landed but the lesson file is not.** The entry's
   `source:` cites S058–S060 and those rows name the entry, satisfying QUALITY
   #29 at the frozen rev's successor. Open: the README `round-23` Lessons row
   exists while `corpus/lessons/round-23.md` does not (O12); either land the
   file in the same commit or record the rule exception. The R22 wiki-page
   draft stays a separate, unlanded row.
6. **Empty-decode and window semantics.** The landed synthetic decode is
   non-empty (two literal annotations) so the O10 empty-record hole is not
   exercised by it; the public recording is explicitly not described as a
   lossless payload. Whether a `has_more:false` window of 12,885 lines counts
   as complete output is still L1's predicate to state, not this report's.
7. **Timestamp rule.** The appended block's date must be at/before the landing
   commit's committer time (QUALITY #23); use `date -u` at write time.
8. **Boundary bleed.** Nothing here changes the adjacent/unresolved dynamic
   ownership: no tracer run, no attach, no device, and the signal verbs are
   file-only. Draft A repeats that sentence so the appended block cannot be
   read as a capability grant.

## Verification L1 should run (not run by this seat)

1. **Pure additions where the move applies.** `git diff --numstat a3c92eb..<rev> -- PROVINCE.md SKILL.md`
   → deletions `0` for both. For `corpus/README.md` / `corpus/SOURCES.md`, do not
   diff against `a3c92eb`: their integration is already in the live tree (O12).
   Verify instead that the landed hunk is exactly three README rows plus three
   blank-line removals and three SOURCES rows — any other hunk is out of scope.
2. **Prefix identity (no line moved).** `PROVINCE.md` and `SKILL.md`:
   `git show a3c92eb:<f> > /tmp/b; git show <rev>:<f> > /tmp/n; cmp -n "$(stat -c%s /tmp/b)" /tmp/b /tmp/n`
   → exit 0; the base hashes `dbf757fe…` / `4898fa74…` still match `/tmp/b`.
   For the two integrated files, pin the landing hashes and re-run `nl -ba` on
   the three heading lines (`## Knowledge`, `## Lessons`, `## Frontier`) and the
   `held, not frontier` bullet before attributing any further movement.
3. **R22 partition still exact.** Replicate `.ufo/waves/round-22/verify.py:183-190`
   against `<rev>` → `province-section-partition-exact` true.
4. **Pointer table.** `python3 -I -B .ufo/gates/citation-drift/citation-drift-probe.py --root <lane> --rev <rev> --strict`
   → finding-id set identical to the same command at `a3c92eb` (the five O6 ids
   plus whatever else already exists). The README insertion was net-zero, so any
   *new* id is a real defect, not expected drift. A non-strict exit 0 alone is
   not evidence (O7).
5. **Census.** `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku`
   → exit 0, same W04 scope duplicates as `start-census.json`.
6. **Counter independence.** `grep -n "README\|PROVINCE\|SKILL" .ufo/waves/round-23/tools/count-c1.py`
   → expected no match; the doc blocks must not move k. Any match must be read
   before the doc landing is called count-neutral.
7. **Timestamp gate if evidence is added.** `python3 -I -B .ufo/waves/round-20/tools/evidence-timestamps.py --root <lane> --rev <ship-rev> --path .ufo/waves/round-23 --strict`
   → exit 0.
8. **Read-back.** `sed -n '211,218p' PROVINCE.md` byte-identical to the base
   blob; `sed -n '700,706p' SKILL.md` likewise; and the appended PROVINCE block
   starts after the base file's final newline, not inside the R22 section.
9. **Lessons-row dependency.** `test -f corpus/lessons/round-23.md` → either
   exit 0 in the landing commit, or the exception to README's `:9` rule is
   recorded explicitly. Do not leave the row standing alone silently.

## Produced files

- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-23/w1/ConnectFrontier.md`
  (this report; its sha256 is reported in the seat's final message — a
  self-referential digest inside the file would change on insertion).
- No other file written; no sandbox, no output directory.

## Installs

None. No tool installed or updated; no pacman transaction; no config edit.

## Open risks / unknowns (kept as unknowns)

- The Dart 3.13.0 rename pins (tag commits, `dart_api.h` hashes, commit
  `d36adbac…`) are `CriticSource`'s observation, not re-verified here; only the
  four-name array at `FlutterBuildProvider.js:598-603` was read by this seat.
- The landed entry reports two literal annotations for the synthetic UART file
  and a 12,885-line `has_more:false` window for the public recording. This seat
  read those numbers from the entry and the evidence listing; it did not re-run
  the producer, so they are the entry's evidence, not this report's.
- The choice for `PROVINCE.md` / `SKILL.md` is still open: EOF append (this
  proposal) or an in-file insertion with re-point work. `corpus/README.md` and
  `corpus/SOURCES.md` are already settled in the live tree.
- The live worktree changed during this seat's run (O12); any verdict on the
  anchors above must re-pin the worktree hashes first, not reuse this report's
  line numbers unqualified.
- `corpus/lessons/round-23.md` is absent while its README row exists; whether
  that is a deferred close-out or a rule exception is unstated.
- The five pre-existing dead pointer entries stay dead under this proposal;
  repairing them is a separate, citation-instrument change.
