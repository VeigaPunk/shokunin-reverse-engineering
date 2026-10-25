# ANoCredit — did the round claim any credit in its committed bytes?

Round 34, run-6 re-dispatch, wave 2. Assignment: verify no credit is claimed in the round's committed bytes
(no capability row, no axis score change, no coverage-map entry, no knowledge-index row before the stop) and
that SCORECARD/LOG/SKILL/corpus are still unchanged from the round base. Read-only on VCS; no counter, reader,
carrier or fixture was executed; no tool was installed (nothing to install, no pacman/uv/npx transaction).

**Headline.** No capability row, no owned-axis score change, and no credit-bearing coverage/index row exists in
the committed bytes at the stop commit `cd75b92e` or at either post-stop docs landing (`66b84027`,
`5a0435ff`). Two committed record defects **do** contradict their own bytes:
(a) the landing's LOG says the source census went `105→106` while the committed `corpus/SOURCES.md` still has
**105** rows and the rejected row **S105 is gone** (replaced by S106, `rejected 4→3`), and `5a0435ff`'s message
and its committed M34-12 row assert "S105 restored verbatim … end recount 106 rows" although `5a0435ff`'s
`corpus/SOURCES.md` blob is byte-identical to `66b84027`'s and still 105 rows; and
(b) `5a0435ff` deletes `QUALITY` row **73** (the receipt-binding criterion the round's own M34-11 routes to)
while inserting row 74, leaving committed rows 68–72,74.
Neither is capability/score credit. Both were closed by the later repairs `417a8211`/`b62b4767` (S105 restored →
106 rows; QUALITY 73 restored; SCORECARD count corrected to 68-74), verified at tip `1675a8d8` in §7.

The lane moved while I verified: my opening commands (before 07:32:25Z) saw `cd75b92e` as `HEAD` with the
corpus drafts already dirty; my first `HEAD` read at **07:32:27Z** already returned `66b84027`, and the landing
commit is `66b840274390d0868c913a544947f9eb40a4ffe6` (committer 2026-10-25 04:32:25 −0300 = **07:32:25Z**).
All statements below name their revision and observation UTC.

## 1. Revisions and base identity

| role | revision | note |
|---|---|---|
| round base (`claims.base_revision`, `SCORECARD` round-34 header) | `ec3125ad3d130d92f888a4128dfaa2982f36fff7` | predates all round-34 work |
| r34b inherited tip (`claims.inherited_tip`) | `f432c8e3bc58934887c83f1db2b26f9910a9d87f` | last r34a commit; `corpus` tree `a1867ebb` |
| r34b freeze | `c79bbe7b0959132b9873ff3431cf5eb313b58b33` | instruments only; no guard file |
| r34b stop | `cd75b92e583735729546b0ea3b250f2df6d0652a` | `claim-stop.json` blob `544209aa32f6f38e3152bdf16c8e563621538a75` |
| docs landing (arrived during this wave) | `66b840274390d0868c913a544947f9eb40a4ffe6` | SCORECARD/LOG/SKILL/QUALITY/SOURCES/README/lessons/knowledge; same `claim-stop.json` blob |
| repair landing (arrived during this wave) | `5a0435ffb9a8921206144e0b61fe3c12a89b59c2` | binds receipts + `claim-stop-addendum.json`, adds `w2` reports, edits `corpus/QUALITY.md` (9+/1−) and `corpus/lessons/round-34.md` (+1); SCORECARD/LOG/SOURCES unchanged from `66b84027` |
| repair landings (arrived after F1/F1b were found) | `417a8211…`, `b62b4767…`, `1675a8d848…` | restore S105 and QUALITY 73, correct the SCORECARD criteria count to `68-74`, record predicate status and LOG wording, land the last reports. Tip at close observed 07:39:30Z |

`claims.json` declares both `base_revision=ec3125ad…` and `inherited_tip=f432c8e3…`; the two are not the same
revision, and the assignment's phrase "the round base" is only unambiguous if it means the inherited tip for
r34b. Both matrices are reported.

## 2. Per-file blob hashes (git blob SHAs, `git rev-parse <rev>:<path>`)

| path | `ec3125ad` (base) | `f432c8e3` (tip) | `cd75b92e` (stop) | `66b84027` (landing) | worktree `git hash-object` @07:34:45Z |
|---|---|---|---|---|---|
| `SCORECARD.md` | `2c1fa9bcc7…` | `e2c82c1d1f…` | `e2c82c1d1f…` | `8b8f9c33ac…` | `8b8f9c33ac…` |
| `LOG.md` | `f50d715c78…` | `2b3d2b2334…` | `2b3d2b2334…` | `74f1982286…` | `74f1982286…` |
| `SKILL.md` | `289a6a147f…` | `d9dd15fcf8…` | `d9dd15fcf8…` | `c2e76469d0…` | `c2e76469d0…` |
| `PROVINCE.md` | `d453a29dde…` | `d453a29dde…` | `d453a29dde…` | `d453a29dde…` | `d453a29dde…` |
| `corpus/QUALITY.md` | `7b393506aa…` | `e1d2975daf…` | `e1d2975daf…` | `df5dcbed5c…` | `3ddc8cabb5…` (M, in flight) |
| `corpus/README.md` | `3e3157741f…` | `e25c1981dc…` | `e25c1981dc…` | `59782a47f2…` | `59782a47f2…` |
| `corpus/SOURCES.md` | `39b5983e20…` | `fd516709ac…` | `fd516709ac…` | `a7ee80725a…` | `a882542799…` (M, in flight) |
| `corpus/claim-freezes.tsv` | `0168cac269…` | `b7b4fcb55d…` | `b7b4fcb55d…` | `b7b4fcb55d…` | — |
| `corpus/claim-freezes-v2.tsv` | `fcff83c5bd…` | `518afb9c71…` | `518afb9c71…` | `518afb9c71…` | — |
| `corpus/lessons/round-34.md` | absent | `a4a55ec167…` | `a4a55ec167…` | `eab14596fc…` | `37e9ae5bef…` (M, in flight) |
| `corpus/knowledge/2026-10-23-r34-elf-version-needs.md` | absent | `03765f0273…` | `03765f0273…` | `4b41c368c0…` | `4b41c368c0…` |
| `corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md` | absent | absent | absent | `4673776d0c…` | `4673776d0c…` |

Tree hashes: `corpus` = `7eaf60a4bc87c96b36fe93da7a00151713a5b94e` (base) → `a1867ebb4853b5ca9ca84879c472595152a05ec1`
(tip = stop) → `396546c44612c6f7d4961996283a05f04e0d1cf5` (landing). `tools/round-34` is **absent** at `ec3125ad`
and `8afe0bd78039bbd85a6d2e9035ef9716edbd0856` at both `cd75b92e` and `66b84027` — the landing changed no
instrument. Full-width hashes in `/fast/scratch/hyaku/kaidoku-r34b/w2/ANoCredit/nocr-receipt-v2.json` and
`nocr-receipt-v3.json`.

Second landing `5a0435ff` (observed 07:37:4xZ): `corpus` tree `6885404f328a8f06e1081c33bd634cd68562d855`;
`corpus/QUALITY.md` `426584ca47…`, `corpus/lessons/round-34.md` `37e9ae5bef…` (this is where the in-flight
working-tree lessons blob landed); `corpus/SOURCES.md` **still** `a7ee80725a…`, `SCORECARD.md` still
`8b8f9c33ac…`, `LOG.md` still `74f1982286…`, `SKILL.md` still `c2e76469d0…`, `PROVINCE.md` still `d453a29dde…`,
`corpus/README.md` still `59782a47f2…`, r34b knowledge entry still `4673776d0c…`.

## 3. Clause-by-clause

### 3.1 No capability row — HOLDS
`SCORECARD.md` `## Capabilities` section is byte-identical at `ec3125ad` and `66b84027` (same 10 pipe-lines,
header and separator included; section sha256 `42c2f7b83c8c2e9c51d0251030f1883801fab31ece35fabb029c035780437ea2`
at both, 07:33:5xZ). The landing adds
no row there; its new section states "No capability row enters: a capability needs a passing demonstration in
the round that enters it, and this round's demonstration failed" (`SCORECARD.md:3365`). `PROVINCE.md` is
byte-identical at all four revisions. The knowledge entry's own header says `status: instrument retained;
**capability denied**` (`corpus/knowledge/2026-10-25-r34b-…-stop.md:4`); the SKILL registry block says "the
capability they were built to demonstrate was **denied**" (`SKILL.md`, added hunk).

### 3.2 No axis score change — HOLDS
Owned-axis rows (`SCORECARD.md:23-25`: coverage, depth, calibration) are byte-identical at `ec3125ad` and
`66b84027` (programmatic line comparison of lines 20–26, True at 07:33:41Z). `git diff --numstat
ec3125ad..66b84027 -- SCORECARD.md LOG.md SKILL.md PROVINCE.md` = `48 0 / 24 0 / 65 0` and PROVINCE empty:
**zero deletions** anywhere, so no existing score cell was rewritten. The single deletion vs `f432c8e3` is one
grammar sentence in the C1 section ("next counter is frozen" → "next counter freeze"). The landing's own table
records coverage `10 → 10`, depth `10 → 10`, calibration `10 → 10`, verdict `unchanged`. `claims.json`
`scores_unchanged` = `{calibration: "10 -> 10", coverage: "10 -> 10", depth: "10 -> 10"}` — consistent.

### 3.3 No coverage-map entry before the stop — HOLDS for r34b; one r34a entry predates both stops
- `corpus/README.md` (which holds `## Coverage map` at line 11 and the knowledge index at line 90) is
  byte-identical to `f432c8e3` at the stop (`e25c1981dc…`). The r34b coverage row ("Instrument admission
  (shortcut replay) … held as a tool, not as capability … no capability or score is claimed") and the r34b
  knowledge-index row were added by the post-stop landing `66b84027`.
- The round did add a **pre-stop** index artefact at `8897a67f`: the r34a knowledge entry
  `corpus/knowledge/2026-10-23-r34-elf-version-needs.md` (blob `03765f02…`, 47 lines) plus its index row and a
  one-line edit to the Native ELF coverage row (`2 1` numstat) that appends "round 34 adds sourced GNU
  version-needs detail on this existing ground, **not coverage widening**". That is before the C1 freeze
  (`54a87a51`), before the C1 stop (`abbd7604`) and before the C2 stop. It is not credit-bearing (the entry
  says "no runtime resolution or authenticity claim"), but it is literally the one knowledge-index row added
  before a stop in this round, and the assignment's clause should be read with that disclosed.

### 3.4 SCORECARD/LOG/SKILL/corpus unchanged from the round base — FALSE at `ec3125ad`, TRUE at the stop vs the inherited tip
- vs `f432c8e3` (r34b's start): **byte-identical at `cd75b92e`** for SCORECARD, LOG, SKILL, PROVINCE and the six
  corpus text files above; `git diff --stat f432c8e3..HEAD -- SCORECARD.md LOG.md SKILL.md PROVINCE.md corpus/`
  returned empty, exit 0, when `HEAD` was `cd75b92e` (observed before the 07:32:25Z landing). The r34b commits
  `c79bbe7b`, `b917ea64`, `cd75b92e` touch no guard path.
- vs `ec3125ad` (declared base): **not unchanged**. `git diff --numstat ec3125ad..cd75b92e` =
  LOG `13 0`, SCORECARD `24 0`, SKILL `51 0`, QUALITY `3 0`, README `2 1`, SOURCES `7 0`,
  claim-freezes `1 0` each, lessons `69 0`, plus a new knowledge file (`47 0`). All of it landed in r34a at
  `8897a67f`, `54a87a51`, `abbd7604`, `f432c8e3`; the `README 2 1` is the coverage-row append quoted above.
  So the "unchanged from the round base" invariant is false under the literal `base_revision` and true only
  under `inherited_tip`.
- After the landing `66b84027` (post-stop), all four categories changed again; `5a0435ff` changed only
  `corpus/QUALITY.md` (+9/−1) and `corpus/lessons/round-34.md` (+1) on top of it. §4/§5 evaluate those bytes.
  The SCORECARD/LOG/SKILL blobs at `5a0435ff` are still exactly `66b84027`'s, so §3.1–§3.2 hold unchanged at the
  newest tip.

## 4. Findings by severity

**F1 — Committed record overclaims the source census (High, record honesty; not score credit).**
At `66b84027`, `LOG.md:3100` states "Census start and end both exit 0; rows 105→106, all-A tier unchanged,
malformed 0". The committed `corpus/SOURCES.md` at that same revision has **105** data rows
(`grep -c '^| S[0-9]'`) and **no `S105` row** (`grep -c '^| S105 '` = 0), while `S106` = 1; statuses are
`mined 102 / rejected 3` versus `mined 101 / rejected 4` at `f432c8e3`. The S106 insert used the S105 row as
its anchor and overwrote the rejected gABI row; the count stayed 105 and the census still exited 0. Evidence:
`git show f432c8e3:corpus/SOURCES.md` / `git show 66b84027:corpus/SOURCES.md`, tallies at 07:34:30Z
(`f432c8e3 rows=105 A99/B5/C1 mined=101 rejected=4`; `66b84027 rows=105 A99/B5/C1 mined=102 rejected=3`;
worktree `rows=106 A100/B5/C1 mined=102 rejected=4`). The repair is already drafted but **uncommitted**
(`M34-12`, `QUALITY 74`, S105 restored verbatim ahead of S106), so the committed landing still carries the
false `105→106` and the destroyed rejection row.

At the next tip `5a0435ff` (commit message: "… the M34-12 row swap …") the committed `corpus/lessons/round-34.md`
row M34-12 says "S105 restored verbatim from the base blob `f432c8e3:corpus/SOURCES.md` ahead of S106; end
recount 106 rows, A 100/B 5/C 1, mined 102, rejected 4" — but `5a0435ff:corpus/SOURCES.md` is byte-identical
to `66b84027` (`a7ee80725a…`) and still tallies `rows=105 S105=0 S106=1 A99/B5/C1 mined=102 rejected=3`
(07:37:4xZ). So the record now asserts a repair that the same commit's tree does not contain; the restore
exists only in the working tree (`rows=106 S105=1 mined=102 rejected=4` at 07:37:44Z). `LOG.md:3100` was not
corrected at either tip.

**F1b — The repair landing deletes QUALITY row 73 and leaves four committed files pointing at it (High, record).**
`5a0435ff`'s `corpus/QUALITY.md` diff is one deletion and one insertion: `-| 73 …` / `+| 74 …`. The committed
table therefore reads 68, 69, 70, 71, 72, 74 — the receipt-binding criterion "A receipt states what produced it:
exact argv, reader digest, the commit the bytes were read at, and a UTC instant …" is gone
(`git show 5a0435ff:corpus/QUALITY.md | grep -c '^| 73 '` = 0; `grep -c "A receipt states what produced it"` = 0;
07:37:4xZ). Four committed files still cite the range: `SKILL.md` "QUALITY 68-73" (2 hits), the r34b knowledge
entry "corpus/QUALITY.md rows 67-73", `SCORECARD.md` "QUALITY 68-73", `LOG.md` "QUALITY 68-73". The working tree
restores 73 ahead of 74 (uncommitted at 07:37:44Z), so the tip again describes a state its bytes do not have.
This is the same anchor-replacement class as M34-12 — committed by the very edit that inserts QUALITY 74, the
criterion that names that class.

**F2 — Base identity is ambiguous in the claim and in the round's own prose (Medium).**
`claims.json` carries `base_revision=ec3125ad…` and `inherited_tip=f432c8e3…`; the SCORECARD header and the
lesson both cite `ec3125ad` as "Base", while the r34b wave actually starts at `f432c8e3`. A verification that
uses the declared base concludes "guard files changed"; one that uses the inherited tip concludes "unchanged".
Both statements are true of different revisions. Evidence: §1 table, §3.4 blob matrix. This is exactly the
M34-1/M34-5 family the round already routes to QUALITY 65/68, so it is a recurrence, not a new class.

**F3 — The docs landing arrived inside the verification window (Medium, process).**
`66b84027` changed SCORECARD/LOG/SKILL/corpus after the stop, so an "unchanged" check has to name its tip.
Reviewed line by line: every added block denies capability (`SCORECARD:3347-3365`, `LOG:3094-3103`,
`SKILL` registry block, `corpus/README.md` r34b rows, new knowledge entry header, `QUALITY 68-73`,
`lessons` M34-5..M34-11). The only numeric tables added state `10 → 10 / unchanged`. The only in-place edit is
the C1 grammar sentence. No score, threshold, class or label moved. So the no-credit invariant survives the
landing — but the landing is outside the "unchanged" invariant the assignment names, and it is the vehicle for
F1.

**F4 — Coverage-map and knowledge-index rows for the stopped claim are post-stop and self-disclaiming (Low).**
`corpus/README.md` coverage row: "held as a tool, not as capability — … so no capability or score is claimed";
knowledge-index row: "… capability **denied** by the round's own stop". Both satisfy the temporal clause and
carry no credit. Note only that the coverage-map `state` verb "held" is the same word used for capability
holds elsewhere; the row's own text disambiguates, and the section is titled "Instrument admission".

**F5 — Coverage score cell's count is stale but not relied upon (Low, inherited).**
`SCORECARD.md:23` (coverage) still says "116/116 knowledge files mapped at `c369242f…` (recount, round 31)",
while `corpus/knowledge` holds 122 `.md` files at `66b84027` (`git ls-tree … | grep -c '\.md$'`). The count is
explicitly revision-bound, and the new section claims coverage `10 → 10 (map/index only …)`, so no current
count is asserted; the drift is inherited from rounds 32–34. The same row's "Last-change round" cell says
"count refreshed rounds 25 and 26" while its observable cites a round-31 recount — a pre-existing internal
mismatch, unchanged by this round.

**F6 — Working-tree drafts and strays exist (Low; not committed bytes).**
At 07:34:45Z: `M corpus/QUALITY.md` (`3ddc8cab`, adds QUALITY 74), `M corpus/SOURCES.md` (`a882542799`, S105
restored), `M corpus/lessons/round-34.md` (`37e9ae5b`, adds M34-12), untracked zero-byte
`corpus/knowledge/2026-10-25-r34-pre-freeze-shortcut-replay-gate.md` (wrong name, empty; observed 0 bytes at
07:33:18Z and 07:34:45Z), plus `.ufo/waves/round-34/r34b/census-end.txt`, `w1-validator-stderr.txt`,
`w1/CtlMultiset-files/{payload_keyed.py,payload-keyed-receipt.json,nameset-green-receipt.json}`,
`after/freeze-integrity-instruments.txt` and several untracked `w2/*.md`. None claims credit; a wholesale
`git add -A` would import an empty knowledge file and drafts that a later landing must curate.

**Observation (not scored):** the landing's narrative says "quality **improved** … discernment **improved**"
(`SCORECARD.md:3365`). These are learning-trend sentences, not owned-axis scores, and they are outside the five
items the stop record lists in `not_claimed` (`capability`, `coverage`, `depth score`, `calibration score`,
`R34-C1 revival`). Flagged for the L1, not treated as a clause violation.

## 5. Commands, exits, UTC (representative; full argv in the scratch receipts)

| UTC (2026-10-25) | argv | exit | result used |
|---|---|---|---|
| 07:32:27Z | `git rev-parse --verify HEAD` | 0 | `66b84027…` (the landing; `git log -25`/`git status` two minutes earlier still showed `cd75b92e` and dirty corpus drafts) |
| 07:32:27Z | `git rev-parse {ec3125ad,f432c8e3,HEAD}:<path>` × 9 | 0/128 | §2 base/tip/landing columns |
| 07:32:27Z | `git diff --numstat ec3125ad..HEAD -- <guard paths>` | 0 | `24 0 / 48 0 / 65 0 / 9 0 / 6 1 / 12 1 / 1 0 / 1 0 / 104 0` |
| 07:32:58Z | `date -u` | 0 | `2026-10-25T07:32:58Z` |
| 07:32:59Z | `git rev-parse {ec3125ad,f432c8e3,cd75b92e,66b84027}:<path>` × 44 | 0/128 | §2 full matrix |
| 07:32:59Z | `git diff --numstat cd75b92e..66b84027 -- <guard paths> corpus/ tools/` | 0 | landing scope; `tools/` empty |
| 07:32:59Z | `git grep -c R34-C2 66b84027 -- SCORECARD.md LOG.md SKILL.md PROVINCE.md corpus/lessons/round-34.md corpus/README.md` | 0 | `2 / 1 / 1 / (none) / 2 / (none)` |
| 07:33:41Z | `git hash-object` × 9 (worktree) | 0 | §2 worktree column |
| 07:33:41Z | `git diff --numstat ec3125ad..66b84027 -- SCORECARD.md LOG.md SKILL.md PROVINCE.md` | 0 | `48 0 / 24 0 / 65 0`, PROVINCE empty |
| 07:33:41Z | `sed -n 20,26p` of `ec3125ad:SCORECARD.md` and `66b84027:SCORECARD.md` | 0 | owned-axis rows identical (True) |
| 07:33:5xZ | section hash of `## Capabilities` at both revs | 0 | `42c2f7b8…` twice, 10 rows |
| 07:34:30Z | per-revision `grep -c '^| S[0-9]'`, `| A |`, `| mined |`, `| rejected |` on `corpus/SOURCES.md` | 0 | F1 tallies |
| 07:34:45Z | `git log --oneline -2`, `git status --porcelain=v1`, `git hash-object` × 9 | 0 | final snapshot at that moment; HEAD `66b84027` |
| 07:37:26Z | `git log --oneline -2`, `git status --porcelain=v1` | 0 | new tip `5a0435ff…`; working tree M LOG/SCORECARD/QUALITY/SOURCES/lessons/knowledge |
| 07:37:4xZ | `git show --stat 5a0435ff`, `git diff --numstat 66b84027..5a0435ff -- SCORECARD.md LOG.md SKILL.md PROVINCE.md corpus/` | 0 | only `corpus/QUALITY.md 9 1` and `corpus/lessons/round-34.md 1 0` |
| 07:37:4xZ | `git show 5a0435ff:corpus/SOURCES.md` tallies (`^| S[0-9]`, `^| S105 `, `^| S106 `, tier/status) | 0 | rows 105, S105 0, S106 1, A99/B5/C1, mined 102, rejected 3 |
| 07:37:4xZ | `git show 5a0435ff:corpus/QUALITY.md \| grep -c '^| 73 '` | 0 | 0 (worktree 1) → F1b |
| 07:37:4xZ | `git grep -c 'QUALITY 68-73'` / `'rows 67-73'` at `5a0435ff` | 0 | SKILL 2, knowledge 1, SCORECARD 1, LOG 1 |

Receipts: `/fast/scratch/hyaku/kaidoku-r34b/w2/ANoCredit/nocr-receipt.json`,
`nocr-receipt-v2.json`, `nocr-receipt-v3.json`, `nocr-receipt-v4.json`.

## 6. Residual risk and verification gaps

- The round was landing while I measured: `66b84027` arrived 07:32:25Z, `5a0435ff` 07:35:10Z, and three more
  commits through `1675a8d8` 07:39:13Z. Any later commit can change the answer; §7 is the latest verified tip,
  and §2/§3 must be re-run against whatever tip the round is finally closed at.
- F1 and F1b are real in committed bytes at both tips; the working tree already contains both repairs (S105
  restored → 106 rows; QUALITY 73 restored ahead of 74). A landing that includes them closes both. A landing
  that omits either leaves a false census line, a destroyed rejection row, or a deleted criterion that four
  committed files still cite.
- I did not execute any counter, reader, carrier or fixture (out of scope and forbidden here), so I did not
  verify the claim-stop's `matched=8` / `met_target=true` observation, the frozen-clause verdict, or the five
  record defects' substance; those belong to the other wave-2 seats. I did not run builds, linters or suites.
- I did not audit r34a's instrument-level credit (`8897a67f` contents beyond the file/blob/numstat evidence
  above), nor the r34a end-census `102→105` line against its own bytes; only the guard-file and index facts
  reported here were checked.
- "Unchanged" claims are revision-specific by construction; any future statement of the form "SCORECARD/LOG/
  SKILL/corpus unchanged" must name the tip it was measured at (this is precisely QUALITY 65/M34-1).

## 7. Final tip at report close (after the repair landings)

Further landings arrived while this report was being written: `417a8211` ("restore S105 and QUALITY 73 after
anchor-replacement…"), `b62b4767` ("correct the SCORECARD criteria count to QUALITY 68-74 (seven rows)") and
`1675a8d8` (predicate status, LOG blindness wording, last reports). At tip `1675a8d848…` (committer
07:39:13Z, observed 07:39:30Z; later commits possible):

| check | result |
|---|---|
| `corpus/SOURCES.md` | **106** rows, `S105` = 1, `S106` = 1, A100/B5/C1, mined 102, rejected 4 (blob `dc7a3ccc66…`) |
| `corpus/QUALITY.md` | rows 70, 71, 72, **73**, **74** all present (blob `0d187a0663…`) |
| `SCORECARD.md` | `## Capabilities` sha256 `42c2f7b8…` and owned-axis lines sha256 `346c0208…`, both identical to `ec3125ad` (blob `2b325e0f6d…`); the defect line now reads "QUALITY 68-74 encode each (seven rows…)" |
| `LOG.md` | blob `2e2e829d…`; `:3100` still "rows 105→106, all-A tier unchanged" — the **count is now true** (106 rows) |
| `SKILL.md` | unchanged `c2e76469…`; still cites "QUALITY 68-73" twice |
| `corpus/knowledge/2026-10-25-r34b-…-stop.md` | blob `fc560ac3…`; header still cites "corpus/QUALITY.md rows 67-73" |
| `PROVINCE.md` | `d453a29d…`, unchanged since base |
| `corpus` tree | `2c4467364100bce3a369c923de9dc4b8df8a7652` |

So **F1 and F1b are closed in the final bytes**: S105 is restored verbatim (106 rows, `rejected 4`, `mined 102`)
and QUALITY 73 is back. Residual, all low: (i) "all-A tier unchanged" is numerically A 99→100
(`f432c8e3` → tip) even though the row count now matches; (ii) `SKILL.md` (2 hits) and the knowledge entry
(1 hit) still cite `QUALITY 68-73`, omitting the new row 74 — an incomplete range, not a dangling one; (iii) the
base-identity ambiguity (F2) is untouched. No step of the repair introduced a capability row or a score change:
both invariant hashes equal the base at the tip.

## 8. Tooling

No install or update: the audit used only `git` (read-only subcommands), `grep`/`sed`, `date` and `sha256sum`
already on the host. No pacman/uv/npx/pip transaction was attempted; no host service was touched.

**VERDICT: no capability row, no owned-axis score change, no score deltas, and no credit-bearing coverage-map or
knowledge-index row for R34-C2 in the committed bytes at `cd75b92e`, `66b84027` or `5a0435ff` — the no-credit
claim holds at every tip; but the record does not: the landings overclaim their own source census
(`LOG.md:3100` "rows 105→106" vs 105 committed rows, S105 destroyed, `rejected 4→3`, and `5a0435ff`'s M34-12
row asserting a restore its tree lacks) and `5a0435ff` deletes QUALITY 73 while four committed files still cite
"QUALITY 68-73"; the round base is also ambiguous between `ec3125ad` (declared) and `f432c8e3` (r34b start). The
docs are not settled until the working-tree repairs (S105 restore, QUALITY 73 restore) land and the base used
for any "unchanged" statement is named.**
