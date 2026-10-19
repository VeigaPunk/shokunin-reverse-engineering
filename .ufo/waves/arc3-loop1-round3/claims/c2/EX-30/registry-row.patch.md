# EX-30 — registry-row + README patch texts for the revised custody-pair tool

Seat EX-30 · chain c2 · role executor · wave arc3-loop1-round3 · 2026-10-19.
Repo: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. **Patch text only** — this
seat wrote neither `SKILL.md` nor the gate README (the C2 implementer, seat
EX-21, owns `.ufo/gates/custody-pair/`; SKILL.md is nobody's seat write target).

Base files (HEAD `c07af80`, worktree byte-identical for both at emission time):

| file | base sha256 | patched sha256 | diff sha256 |
|---|---|---|---|
| `SKILL.md` | `c134afcb2e648aa3f8ff96f11d03aee2be6715811cb7edb3b7be6ac40aa0aa90` | `0383272358727e6f0707f7dd853a6d49bd3df9b49f831afcf39463cdf1340ba9` | `7c4a7a68fc035b4149d0e56accea1c302a5c2a884466d26ca426b4f63bbea1f5` |
| `.ufo/gates/custody-pair/README.md` | `fa484d573b0debb0d2ed134d076cb9593e7c3ee910ad4487d99cb9f3a8239bba` | `42b07ee57bace8f53673e567276c29c07c906311875d1cd55bb81ad86dffc599` | `e61f0a2ffa9f453683bc32b82f616dc03c6bf90b00f7a425dea0815d5fc06953` |

Instrument under description: `.ufo/gates/custody-pair/custody-pair.py`, worktree
revision **`7cd19c3cfd835c7807d5e60dece1c2592c9df6c319a78deb14469dd6ebe8ab09`** (1155 lines) — revision chain observed inside one hour: d164d49f… → d9be407d… → 57dffff1… → 03bd6242… → this digest; re-derive the digest immediately before apply. Committed base revision
`112d01dc034c2d54324e7703e2d03d1d83b0c3930ed5d4f688546968b73ecefa` (round 2). Selftest at the observed revision:
`CUSTODY_PAIR_SELFTEST: CLEAN cases=22 passed=22 failed=0 exit=0`
(this seat's own run). The 7 closure cases this revision adds to the 15 r2
cases: unreadable-path-is-unevaluable, unevaluable-never-matches, parsed-unevaluable-reference-never-matches, partial-reference-require-paths-gate, refuses-to-write-over-scoped-path, selftest-missing-scratch-usage-exit, refuses-write-through-hardlink-alias.

Rule-#11 discipline: neither patched file pins a line number into an
operator-mutable file, and neither patch text cites one. Diff hunk headers below
are diff mechanics, not pinned citations; every behavioral clause names a
subcommand, flag, finding id, or exit class — never a tool line number (the tool
is under revision and its line numbers are not a contract).

## 1. Why the row must change (`registry-row.patch.md`)

The C2 claim closes four named round-2 holes; the registry row's verdict map and
self-invocation cell at HEAD describe the pre-revision tool (15 cases, no exit
14, no coverage flag, write guard scoped to the canonical five only). A row that
still describes the old map is the stale-identity class rule #14 names. The row
must land **in the same commit** as the tool revision (the claim's
coupled-landing clause; the r8 precedent landed a lesson + index row + a coupled
re-point as one pair — `SCORECARD.md`, section `arc2-loop1-round8`).

Measured deltas the row takes, each confirmed against the revised tool's own
docstring, constants, and this seat's runs at revision `7cd19c3cfd835c7807d5e60dece1c2592c9df6c319a78deb14469dd6ebe8ab09`:

| r2 row says | revised tool does | row clause |
|---|---|---|
| exit map 0/10/11/12/13/2/3 | `+ 14 UNEVALUABLE` | "14 UNEVALUABLE (a path exists but could not be evaluated …)" |
| precedence `CONTENT-DRIFT > ABSENT > …` | `CONTENT-DRIFT > UNEVALUABLE > ABSENT > …` | precedence clause updated |
| capture "0 at 5/5, else 13" | `0` at 5/5, `14` when ≥1 path is present-but-unevaluable, else `13` | capture clause updated |
| no coverage notion | `verify --require-paths N` → exit 2 + `REFERENCE-COVERAGE: n/N …` | USAGE clause extended |
| write scope = the custody paths | `set(--paths) ∪ CUSTODY_PATHS`, resolved path **and inode** | write-scope cell extended |
| selftest 15 cases | 22 cases (the 15 r2 cases + 7 closure cases) | case list extended |
| `--paths` "fixture runs only" | unchanged, now also guarded | kept verbatim |

## 2. The patch — unified diff against `SKILL.md` at HEAD

Apply from the repo root: save the fenced body to a file and run
`patch -p1 < registry-row.diff` (or `git apply`). Line effect: **390 → 390
lines** (line-neutral; the row is one physical line, replaced in place).

```diff
--- a/SKILL.md
+++ b/SKILL.md
@@ -387,4 +387,4 @@
 |---|---|---|---|---|
 | interactive-r1-recovery | gate / kaidoku | `python3 .ufo/rounds/interactive-r1/verify-recovery.py`; 0 clean, 1 failed, 2 could-not-evaluate; `--admission` checks this recovery's unresolved prerequisites and returns 2, never native judgment | same command with `--selftest`; asserts isolated subprocess exit codes and stable finding IDs | `.ufo/rounds/interactive-r1/expected.json` pins every snapshot input and expected outcome; normal entry read-only in this repo; selftest creates and removes only its isolated fixture directory under `.ufo/rounds/interactive-r1/` |
 | citation-drift | probe / kaidoku | `python3 .ufo/gates/citation-drift/citation-drift-probe.py --root . --rev <REV> --table .ufo/gates/citation-drift/pointer-table.json --expected .ufo/gates/citation-drift/expected.json`; **probe semantics: 0 reported (drift is reported, never failed) and 2 could-not-evaluate; `--strict` restores the gate map 0 clean / 1 failed / 2 could-not-evaluate**; **frozen-run preflight: the table's sha256 must match the digest pinned in `expected.json` — a tampered table (exit 2, finding `pointer_table_tampered`) or an absent table (exit 2, finding `pointer_table_unreadable`) is could-not-evaluate before any entry is graded; a baseline that pins no digest is exit 2, finding `pointer_table_unpinned`; drift reporting is unchanged (rc 0)** | same command with `--selftest`; 13 isolated-fixture cases asserting exit code and a stable finding id (the eleventh is dead/absent `--rev` → exit 2, finding `revision_unresolvable`; the twelfth is a tampered table → exit 2, finding `pointer_table_tampered`; the thirteenth is an absent table → exit 2, finding `pointer_table_unreadable`), the case table committed in `expected.json` rather than in the script | `.ufo/gates/citation-drift/pointer-table.json` pins every in-repo citation and `expected.json` pins the self-test case table **and the sha256 of `pointer-table.json` (frozen-run guard; any edit to the table must re-pin the digest in the same commit)**; normal entry read-only over the tree it grades; selftest writes only isolated temp fixture repos; **no line number into an operator-mutable file is pinned** (rule #11) |
-| custody-pair | tool / kaidoku | `python3 .ufo/gates/custody-pair/custody-pair.py capture --out <receipt> [--label <L>]` — read-only sha256+stat over the five operator paths → a v2 receipt (SHA256; MTIME_EPOCH/NS with MTIME_UTC_RENDER and MTIME_LOCAL_RENDER labeled separately — the v1 local-under-`MTIME_UTC` defect gone; CTIME_EPOCH/NS; INODE; MODE/UID/GID; the receipt self-pins the instrument's sha256 and receipt-version 2) + a `.sha256` sidecar; `paths` prints the canonical five; `verify <receipt_a> <receipt_b>` or `verify <receipt_a> --live` — **worst-finding map: 0 MATCH, 10 CONTENT-DRIFT (sha256 moved), 11 REWRITE-DRIFT (sha256 equal, inode/ctime/mtime moved — a same-content rewrite), 12 METADATA-DRIFT (mode/uid/gid/size/type, extra path, inconsistent epoch/render, reproduced v1 LABEL-DEFECT), 13 ABSENT; 2 USAGE (bad args, unreadable or unparsable receipt, refused write); precedence CONTENT-DRIFT > ABSENT > REWRITE-DRIFT > METADATA-DRIFT > MATCH; capture is 0 at 5/5, else 13 with the receipt still written, and it refuses to write a receipt over a custody path; v1 receipts still compare on their sha256 — a sums-form v1 reads MATCH-V1-PARTIAL exit 0, a v1 stanza reproducing the round-1 label defect reads METADATA-DRIFT/LABEL-DEFECT exit 12 with its sha256 contract intact (5/5)** | same command with `selftest`; 15 fixture cases — capture/receipt shape/sidecar self-hash, verify-vs-live clean, the two same-content-rewrite pins (in-place ctime, rename inode) → 11, content → 10, absent → 13, metadata → 12, TZ-independent UTC render, the three v1 parse shapes, unparsable → 2, refuse-to-write-over-custody-path → 2; scratch root `$CUSTODY_PAIR_SCRATCH` else `/dev/shm` else `/var/tmp` (`/tmp` never — EDQUOT hazard); exit 3 if any case fails, 0 clean | the five path identities are pinned in the instrument (`CUSTODY_PATHS`, fixed order, printed by `paths`); **normal entry writes nothing under the custody paths — files opened for reading only, never renamed, mtime never touched; writes only the requested receipt + its `.sha256` sidecar (outside the custody set) and, under `selftest`, its isolated fixture root; `--paths` exists for fixture runs only** |
+| custody-pair | tool / kaidoku | `python3 .ufo/gates/custody-pair/custody-pair.py capture --out <receipt> [--label <L>] [--paths <P>…]` — read-only sha256+stat over the five operator paths → a v2 receipt (SHA256; MTIME_EPOCH/NS with MTIME_UTC_RENDER and MTIME_LOCAL_RENDER labeled separately — the v1 local-under-`MTIME_UTC` defect gone; CTIME_EPOCH/NS; INODE; MODE/UID/GID; a path that exists but cannot be evaluated is recorded with `READ-ERROR`/`STAT-ERROR`, never silently as absent; the receipt self-pins the instrument's sha256 and receipt-version 2) + a `.sha256` sidecar; `paths` prints the canonical five; `verify <receipt_a> <receipt_b>` or `verify <receipt_a> --live` [`--require-paths <N>`] — **worst-finding map: 0 MATCH, 10 CONTENT-DRIFT (sha256 moved), 11 REWRITE-DRIFT (sha256 equal, inode/ctime/mtime moved — a same-content rewrite), 12 METADATA-DRIFT (mode/uid/gid/size/type, extra path, inconsistent epoch/render, reproduced v1 LABEL-DEFECT), 13 ABSENT, 14 UNEVALUABLE (a path exists but could not be evaluated — EACCES on open or a stat error other than ENOENT; classified before the both-absent branch, so an unreadable path can never read as a fail-open MATCH); 2 USAGE (bad args, unreadable or unparsable receipt, a reference below `--require-paths N` — with `REFERENCE-COVERAGE: n/N paths present in reference; unaccounted: <list>` printed — refused or failed write, unusable selftest scratch dir); precedence CONTENT-DRIFT > UNEVALUABLE > ABSENT > REWRITE-DRIFT > METADATA-DRIFT > MATCH; capture is 0 at 5/5, 14 when ≥1 path is present-but-unevaluable, else 13 with the receipt still written, and it refuses to write a receipt over a custody path; v1 receipts still compare on their sha256 — a sums-form v1 reads MATCH-V1-PARTIAL exit 0, a v1 stanza reproducing the round-1 label defect reads METADATA-DRIFT/LABEL-DEFECT exit 12 with its sha256 contract intact (5/5), and `--require-paths` applies to v1 references too** | same command with `selftest`; 22 fixture cases — capture/receipt shape/sidecar self-hash, verify-vs-live clean, the two same-content-rewrite pins (in-place ctime, rename inode) → 11, content → 10, absent → 13, metadata → 12, TZ-independent UTC render, the three v1 parse shapes, unparsable → 2, plus the closure cases: an unreadable path and a parsed unevaluable reference → 14 (never a MATCH), a reference below `--require-paths` → 2, the write guard over a `--paths` override and through a hardlink alias → 2, and `selftest --scratch` on a missing/unusable directory → 2 (not a traceback); scratch root `$CUSTODY_PAIR_SCRATCH` else `/dev/shm` else `/var/tmp` (`/tmp` never — EDQUOT hazard); exit 3 if any case fails, 0 clean | the five path identities are pinned in the instrument (`CUSTODY_PATHS`, fixed order, printed by `paths`); **normal entry writes nothing under the custody paths — files opened for reading only, never renamed, mtime never touched; it writes only the requested receipt + its `.sha256` sidecar and, under `selftest`, its isolated fixture root; the guard refuses to write the receipt over `set(--paths) ∪ CUSTODY_PATHS` by resolved path and by inode, so `--paths X --out X` and a hardlink alias exit 2 — a self-harm guard, not a security boundary; the sidecar path (`<out>.sha256`) is not part of the guard (treat it as an output path only); `--paths` exists for fixture runs only** |
```

The patched row in full (one physical line, 5 cells):

```
| custody-pair | tool / kaidoku | `python3 .ufo/gates/custody-pair/custody-pair.py capture --out <receipt> [--label <L>] [--paths <P>…]` — read-only sha256+stat over the five operator paths → a v2 receipt (SHA256; MTIME_EPOCH/NS with MTIME_UTC_RENDER and MTIME_LOCAL_RENDER labeled separately — the v1 local-under-`MTIME_UTC` defect gone; CTIME_EPOCH/NS; INODE; MODE/UID/GID; a path that exists but cannot be evaluated is recorded with `READ-ERROR`/`STAT-ERROR`, never silently as absent; the receipt self-pins the instrument's sha256 and receipt-version 2) + a `.sha256` sidecar; `paths` prints the canonical five; `verify <receipt_a> <receipt_b>` or `verify <receipt_a> --live` [`--require-paths <N>`] — **worst-finding map: 0 MATCH, 10 CONTENT-DRIFT (sha256 moved), 11 REWRITE-DRIFT (sha256 equal, inode/ctime/mtime moved — a same-content rewrite), 12 METADATA-DRIFT (mode/uid/gid/size/type, extra path, inconsistent epoch/render, reproduced v1 LABEL-DEFECT), 13 ABSENT, 14 UNEVALUABLE (a path exists but could not be evaluated — EACCES on open or a stat error other than ENOENT; classified before the both-absent branch, so an unreadable path can never read as a fail-open MATCH); 2 USAGE (bad args, unreadable or unparsable receipt, a reference below `--require-paths N` — with `REFERENCE-COVERAGE: n/N paths present in reference; unaccounted: <list>` printed — refused or failed write, unusable selftest scratch dir); precedence CONTENT-DRIFT > UNEVALUABLE > ABSENT > REWRITE-DRIFT > METADATA-DRIFT > MATCH; capture is 0 at 5/5, 14 when ≥1 path is present-but-unevaluable, else 13 with the receipt still written, and it refuses to write a receipt over a custody path; v1 receipts still compare on their sha256 — a sums-form v1 reads MATCH-V1-PARTIAL exit 0, a v1 stanza reproducing the round-1 label defect reads METADATA-DRIFT/LABEL-DEFECT exit 12 with its sha256 contract intact (5/5), and `--require-paths` applies to v1 references too** | same command with `selftest`; 22 fixture cases — capture/receipt shape/sidecar self-hash, verify-vs-live clean, the two same-content-rewrite pins (in-place ctime, rename inode) → 11, content → 10, absent → 13, metadata → 12, TZ-independent UTC render, the three v1 parse shapes, unparsable → 2, plus the closure cases: an unreadable path and a parsed unevaluable reference → 14 (never a MATCH), a reference below `--require-paths` → 2, the write guard over a `--paths` override and through a hardlink alias → 2, and `selftest --scratch` on a missing/unusable directory → 2 (not a traceback); scratch root `$CUSTODY_PAIR_SCRATCH` else `/dev/shm` else `/var/tmp` (`/tmp` never — EDQUOT hazard); exit 3 if any case fails, 0 clean | the five path identities are pinned in the instrument (`CUSTODY_PATHS`, fixed order, printed by `paths`); **normal entry writes nothing under the custody paths — files opened for reading only, never renamed, mtime never touched; it writes only the requested receipt + its `.sha256` sidecar and, under `selftest`, its isolated fixture root; the guard refuses to write the receipt over `set(--paths) ∪ CUSTODY_PATHS` by resolved path and by inode, so `--paths X --out X` and a hardlink alias exit 2 — a self-harm guard, not a security boundary; the sidecar path (`<out>.sha256`) is not part of the guard (treat it as an output path only); `--paths` exists for fixture runs only** |
```

## 3. Coupling tokens — re-derive immediately before apply

| token | value at emission | where | must be true when it lands |
|---|---|---|---|
| tool sha256 | `7cd19c3cfd835c7807d5e60dece1c2592c9df6c319a78deb14469dd6ebe8ab09` | README revision line | equals the digest every round-3 receipt self-pins (`# tool: custody-pair.py  sha256 …`), re-derived at landing (EX-21 was observed at three revisions inside one hour: `d164d49f…` → `d9be407d…` → `57dffff1…` → `7cd19c3c…`) |
| case count | `22` | row self-invocation cell, README selftest section | equals the count in `CUSTODY_PAIR_SELFTEST: CLEAN cases=N` at landing; claim floor is ≥17 |
| exit number/name | `14` / `UNEVALUABLE` | row map, README exit table | confirmed in the tool's constants and docstring at `7cd19c3cfd835c7807d5e60dece1c2592c9df6c319a78deb14469dd6ebe8ab09` |
| coverage flag | `--require-paths N`, exit 2 | row, README usage + coverage section | confirmed; the tool prints `REFERENCE-COVERAGE: n/N paths present in reference; unaccounted: <list>` |
| write guard | `set(--paths) ∪ CUSTODY_PATHS`, resolved path + inode | row write-scope cell, README write-scope section | confirmed; the inode arm refuses a hardlink alias |

Re-derivation (rule #14 — every artifact that claims byte-identity re-derives it
after each revision):

```sh
sha256sum .ufo/gates/custody-pair/custody-pair.py                      # TOOL_SHA
python3 .ufo/gates/custody-pair/custody-pair.py selftest               # CLEAN cases=N exit=0
```

then re-run `/var/tmp/ex30/build.py` and this emitter; both print the new
digests of every derived file.

## 8. Verification performed by this seat on the two artifacts (scratch copies)

Scratch root `/var/tmp/ex30`; the lane repo was only ever read. A scratch clone
of the lane repo at `c07af80` lives under `/var/tmp/ex30/root`; the cloned HEAD
plus the two base files were re-hashed after every run: `SKILL.md`
`c134afcb2e648aa3f8ff96f11d03aee2be6715811cb7edb3b7be6ac40aa0aa90`, `README.md` `fa484d573b0debb0d2ed134d076cb9593e7c3ee910ad4487d99cb9f3a8239bba` — unchanged.

```
$ python3 build.py                     # builds both revised files from the HEAD copies
SKILL.head.md    lines=  390 sha256=c134afcb2e648aa3f8ff96f11d03aee2be6715811cb7edb3b7be6ac40aa0aa90
SKILL.v1.md      lines=  390 sha256=0383272358727e6f0707f7dd853a6d49bd3df9b49f831afcf39463cdf1340ba9
README.head.md   lines=  132 sha256=fa484d573b0debb0d2ed134d076cb9593e7c3ee910ad4487d99cb9f3a8239bba
README.v1.md     lines=  188 sha256=42b07ee57bace8f53673e567276c29c07c906311875d1cd55bb81ad86dffc599
row cells: 5 | one physical line: True

$ diff -u SKILL.head.md SKILL.v1.md > registry-row.diff     # rc 1 (differs, expected)
$ wc -l registry-row.diff → 8 ; sha256sum → 7c4a7a68fc035b4149d0e56accea1c302a5c2a884466d26ca426b4f63bbea1f5
$ wc -l readme.diff → 122 ; sha256sum → e61f0a2ffa9f453683bc32b82f616dc03c6bf90b00f7a425dea0815d5fc06953

$ cp SKILL.head.md t2.skill.md; patch -s t2.skill.md < registry-row.diff   # rc 0
$ cmp t2.skill.md SKILL.v1.md → byte-identical ; wc -l t2.skill.md → 390   # line-neutral
$ cp README.head.md t2.readme.md; patch -s t2.readme.md < readme.diff      # rc 0
$ cmp t2.readme.md README.v1.md → byte-identical
```

Instrument-in-the-loop (scratch clone, patched files committed **in the clone
only**, clone rev `26ff6888`; the lane repo's git state untouched — its HEAD,
`git status`, and both base-file digests were re-read afterwards):

```
$ python3 .ufo/gates/citation-drift/citation-drift-probe.py --root . --rev 26ff6888 …
CITATION_DRIFT_VERDICT: reported findings=0 exit=0
$ … --strict
CITATION_DRIFT_VERDICT: clean findings=0 exit=0
$ … --selftest
CITATION_DRIFT_SELFTEST: CLEAN cases=13 passed=13 failed=0 exit=0
$ python3 .ufo/gates/c1-census-v10.py --root .
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)
```

Entry-level simulation against the patched `SKILL.md` (the two pointer-table
entries that touch it): `skill-registry-row` anchors the *sibling*
`interactive-r1-recovery` row — content present in the patched file: True;
`shonen-skill-range` reads `SKILL.md:81-255` (SHONEN.md's own assertion) — the
row edit sits at 390, outside the range, and the range needle is intact: True.
The census's `SKILL.md` scope rows are the craft/discipline ranges at the file
head, untouched by a registry-table row at the tail.

## 9. Attacks / refutations attempted on this artifact

1. **"The row edit breaks the citation-drift probe"** — REFUTED: the probe's only
   `SKILL.md` entry is an unpinned sibling-row anchor; a full probe run against
   the patched clone reads findings=0 in both modes, selftest 13/13.
2. **"A one-line row replacement shifts lines other instruments pin"** —
   REFUTED: 390 → 390; the census PASSes in the patched clone (0/0/0/0); the
   SHONEN range simulation holds.
3. **"The row promises behavior the tool does not have"** — REFUTED at the
   current revision and *re-declared as the earlier hazard*: at first emission
   (tool `d164d49f…`) only the docstring had landed and the row would have been
   ahead of the code; the closure hunks and the six cases have since landed and
   every claim the row makes was measured by this seat (section 7). The token
   table remains the correction procedure if EX-21 revises again.
4. **"The row's count 17+ is enough"** — REFUTED against the claim: the row
   states an exact count; `22` is the landed exact count and is substituted
   everywhere.
5. **"The write-scope cell overpromises a security property"** — REFUTED by
   phrasing: the cell says self-harm guard, not a security boundary; the inode
   arm is stated as the scope extension it is.
6. **"The README revision line's sha256 is a self-reference that will go stale"**
   — TRUE by construction and handled: the README is landed by EX-21 together
   with the tool revision, and the sha it prints must equal the digest the tool
   self-pins into receipts; the emitter re-derives it on every run, and the value
   here is bracketed by a 60 s stability watch (section 3 token table).

## 7. Before → after injections measured by this seat (revised tool, scratch only)

All runs read-only against the worktree tool at revision `7cd19c3cfd835c7807d5e60dece1c2592c9df6c319a78deb14469dd6ebe8ab09`; every
fixture lives under `/var/tmp/ex30` (never `/tmp`), and no custody path was
touched (the tool's own `paths` output was the only custostat read).
Round-2 "before" values are quoted from the r2 verdict's named debt.

| hole | round-2 "before" (r2 verdict, D2/D3/guard/D6) | measured "after" here | exit |
|---|---|---|---|
| D2 EACCES capture | `exists=no` + `STAT-ERROR` recorded, path unreadable | `EXISTS: yes` + `READ-ERROR: [Errno 13] Permission denied: …`; `CUSTODY_PAIR_CAPTURE: UNEVALUABLE paths=1/1 … exit=14` | 14 |
| D2 EACCES verify | fail-open `MATCH compared=0/11 exit=0` | `VERDICT: UNEVALUABLE paths=1 UNEVALUABLE=1 exit=14` (`CUSTODY_PAIR_VERIFY: UNEVALUABLE paths=0/1 drift=1 exit=14`) | 14 |
| D3 1-of-5 reference | reads exit 0 with four custody paths unexamined | unchanged without the flag (`MATCH paths=1/1 exit=0`); `--require-paths 5` → `REFERENCE-COVERAGE: 1/5 paths present in reference; unaccounted: <the five>` | 2 |
| write guard `--paths X --out X` | silent clobber of the scoped file | `USAGE: refusing to write a receipt over a path it measures or a custody path (path or inode): <path>`; file content unchanged (`p1`) | 2 |
| write guard, hardlink alias (r2 D7) | resolved-path guard evaded by a hardlink | same refusal for the alias path, via the inode arm (`real content after: five`, intact) | 2 |
| D6 `selftest --scratch <missing>` | raw `FileNotFoundError` traceback | `USAGE: scratch base is not a directory: <path>` | 2 |

```
$ python3 custody-pair.py selftest --scratch /var/tmp/ex30/inj/st
CUSTODY_PAIR_SELFTEST: CLEAN cases=22 passed=22 failed=0 exit=0
$
$ python3 custody-pair.py capture --paths /var/tmp/ex30/inj/d2/guard.txt --out /var/tmp/ex30/inj/d2/receipt.txt
CUSTODY_PAIR_CAPTURE: UNEVALUABLE paths=1/1 label=(none) exit=14          # rc 14
$ python3 custody-pair.py verify /var/tmp/ex30/inj/d2/receipt.txt --live --require-paths 1
CUSTODY_PAIR_VERIFY: UNEVALUABLE paths=0/1 drift=1 exit=14               # rc 14
$ python3 custody-pair.py verify /var/tmp/ex30/inj/d3/one.txt --live --require-paths 5
REFERENCE-COVERAGE: 1/5 paths present in reference; unaccounted: <5 paths>
                                                                          # rc 2
$ python3 custody-pair.py capture --paths /var/tmp/ex30/inj/d3/p1.txt --out /var/tmp/ex30/inj/d3/p1.txt
USAGE: refusing to write a receipt over a path it measures or a custody path (path or inode): …
                                                                          # rc 2, file intact
$ python3 custody-pair.py selftest --scratch /var/tmp/ex30/inj/missing
USAGE: scratch base is not a directory: /var/tmp/ex30/inj/missing          # rc 2
```

## 10. Required semantics → clause traceability (C2 claim)

| claim wording | clause |
|---|---|
| "each named hole is closed with a declared exit class" | row: `14 UNEVALUABLE` + "2 USAGE (… unusable selftest scratch dir)" |
| "EACCES → its class, no fail-open MATCH" | row: "classified before the both-absent branch, so an unreadable path can never read as a fail-open MATCH" |
| "verify coverage declared" | row + README: `--require-paths N` → exit 2 with the `REFERENCE-COVERAGE:` line |
| "write-guard extended to `set(paths) ∪ CUSTODY_PATHS`" | row write-scope cell + README **Write scope** |
| "selftest scratch-guard → USAGE" | row case list + README selftest section (must exist, not create) |
| "selftest grows 15 → ≥17 cases" | `22` stated in both files |
| "registry row + README updated in the SAME commit" | the two artifacts are one patch pair, applied with the tool revision |
| "every receipt self-pins the revised tool's sha256" | README revision line states the digest and says so |

## 12. Artifact revision history (rule #14)

| rev | identity | status | why superseded |
|---|---|---|---|
| v1 | `registry-row.patch.md` `9c5ff61a3933b1eda0ee3c2d222875db85e3b708d2ce0e0e2dd642ef59bca0a8`; `readme.patch.md` `8941cbd91d5f11752ac9cb739692c1d35fa5e4099758ff80b539ad1bd20a93c6` | superseded | reviewed by seat RV-8 against tool `7cd19c3c…`; two clauses were false of the code (see below), and the tool's revision token was three revisions stale |
| **v2** | `registry-row.patch.md` `0ac7e58cd745d90128063d272274292bc1a5e566f80e0db951ed53f6cfb8f129`; `readme.patch.md` `1a5c4b121b65c7178bcbf8e670c393b917f05da36f74d1daa032ec0ce9f1b0f0` | superseded | RV-8's two corrections applied, RV-8's identity note applied (tokens re-derived live from the target), case names derived from the landed table |
| **v3** | `registry-row.patch.md` `0c0b817e9e483e6f522f89c32284b33c3d476c82ff40e5fc74df79c230c0d27a`; `readme.patch.md` `f8d1229c05eb4f3fb51ad9d44a3f3a21f0987bfcfe01ab01ffd8a8b225e5a01a` — digests of the **v3 body, before the §13 append** (a file cannot carry its own post-append digest; the final digests are recorded in `seats/EX-30.md`) | **current** | late-join seat EX-30 re-verified every byte-identity first-hand; one evidence digit corrected (`readme.diff` 114 → **122** lines — the digest `e61f0a2f…` was already right); superseded §8 clone evidence replaced by the §13 re-runs against the current emission. Diff bodies, patched digests and every behavioral clause are byte-unchanged from v2. |

RV-8 (`claims/c2/RV-8/rv8-corrections.patch.md`) measured two gaps; both were
re-measured first-hand by this seat at `7cd19c3c…` and both are now fixed in the
README patch text:

1. **Coverage claim corrected.** v1's `## Reference coverage` sentence read
   "without it, coverage is reported but not enforced". Measured: 0
   `REFERENCE-COVERAGE` lines print without the flag (`grep -c` → 0 on a 1-of-5
   reference that reads `MATCH … exit=0`). v2 adopts RV-8's phrasing: without the
   flag the comparison covers exactly the reference's paths and no coverage line
   is printed.
2. **Sidecar write-guard claim dropped, residual named.** v1 said the guard
   refuses "a receipt or sidecar" over a measured path. Measured: `capture
   --paths X.sha256 --out X` exits **0** and writes 68 bytes over the measured
   `X.sha256` (which the receipt it produced still describes as a 0-byte file).
   v2 states the receipt-path guard and its inode arm truthfully and names the
   sidecar path as an unguarded residual, with the instruction to treat
   `<out>.sha256` as an output path only.

The v1 review also flagged stale revision tokens; v2 removes that class of error
by deriving the digest, the line count, the case count and the case names from
the real target on every emission (section 3).

## 11. Self-identity

Re-emitted by `/var/tmp/ex30/emit.py` after every revision; each run re-derives
this file's sha256, the two diff digests, and the four file digests printed
above, then the seat report records them. The emitter's own re-run is the
re-derivation the C1 rule-#14 discipline requires of any artifact that claims
its own byte-identity.

## 13. Late-join re-verification (seat EX-30, 2026-10-19, after the wave's token-plan lane hit quota)

This seat re-joined the wave after the interruption and **verified** the landed
artifacts rather than redoing them. Everything below was re-derived first-hand;
nothing is copied from the earlier emission or from another seat.

**What was missing and what this seat completed.** The two patch texts existed
(v2); the seat report `seats/EX-30.md` was missing. This seat re-derived every
byte-identity, corrected one evidence digit, re-ran the instrument-in-the-loop
checks against the **current** emission, measured the base "before" state on the
base blob itself, and wrote the seat report.

**Stale §8 note (rule #14).** §8's clone evidence was produced at clone rev
`26ff6888` against an *earlier* emission: that clone holds SKILL.md
`cf5c3991…` (a 19-case row with `precedence CONTENT-DRIFT > UNEVALUABLE > ABSENT
> …` — see the clone's line 390) and a README carrying the literal placeholder
`<TOOL-SHA256>`. It is a valid record of what was tested then, but it is **not**
evidence for the current bytes. §13 supersedes it as the landing-time evidence.

**Re-derivation (all read-only; scratch `/var/tmp/ex30v`, never `/tmp`).**

| identity | value | how |
|---|---|---|
| tool sha256 | `7cd19c3cfd835c7807d5e60dece1c2592c9df6c319a78deb14469dd6ebe8ab09` | `sha256sum .ufo/gates/custody-pair/custody-pair.py` (1155 lines) |
| tool selftest | `CUSTODY_PAIR_SELFTEST: CLEAN cases=22 passed=22 failed=0 exit=0` | own run, `--scratch /var/tmp/ex30v/...`; the 22 case names printed one per line |
| `SKILL.md` base / patched | `c134afcb…` / `03832723…` | `git show HEAD:SKILL.md` → `patch -p1 <` extracted body; 390 → 390 lines |
| `README.md` base / patched | `fa484d57…` / `42b07ee5…` | `git show HEAD:.ufo/gates/custody-pair/README.md` → apply; 132 → 188 lines |
| diff digests | `registry-row.diff` `7c4a7a68…` (8 lines); `readme.diff` `e61f0a2f…` (**122** lines) | extracted fenced bodies, `sha256sum`, `wc -l` |
| round-3 pair | `MATCH 5/5 exit=0` with and without `--require-paths 5`; post vs live `MATCH 5/5 exit=0` | revised tool over `EX-21/receipts/` |
| receipt self-pins | every `# tool:` line in the round-3 c2 tree reads `7cd19c3c…` (the sole live revision) | `grep -rh '# tool:'` over the wave tree |
| sidecars | `d59224bd…` / `0632a808…` == their receipts | `sha256sum` vs sidecar |
| command A | `82/82, missing [], dangling [], 14/14, 10.0/10.0` | SCORECARD recipe, `REV=c07af80…` |
| probe at HEAD (landed 57-entry table) | `reported findings=0 exit=0`; selftest `CLEAN cases=13` | read-only run |
| census at HEAD | `VERDICT: PASS (stale=0 ambiguous=0 undeclared=0 unresolved=0)` | read-only run |

**Correction applied by this seat.** §8's `wc -l readme.diff → 114` was wrong
(the digest `e61f0a2f…` was right; the body is **122** lines). Corrected in both
artifacts. This is an evidence-digit fix only — no diff body, no patched digest,
no behavioral clause changed.

**Coupled-landing hazard re-confirmed against the current emission (authority
instrument, not a replica).** The row edit rewrites the custody row's precedence
clause, which is exactly the string C3's landed table pins in the anchor
`skill-registry-custody-pair-row`. Measured with the real probe against a
scratch clone carrying this emission's patched `SKILL.md` + EX-21's landed tool
and README, evaluated against the **landed** 57-entry table:

```
CITATION_DRIFT: citation_dead entry=skill-registry-custody-pair-row SKILL.md: no line matches 'precedence CONTENT-DRIFT > ABSENT > REWRITE-DRIFT > METADATA'
CITATION_DRIFT_VERDICT: reported findings=1 exit=0      (--strict: failed findings=1 exit=1)
```

Direct regex evaluation over all three `SKILL.md` anchors: `skill-registry-row`
OK, `skill-registry-citation-drift-row` OK, `skill-registry-custody-pair-row`
**DEAD** — 1 collision. This agrees with CN-1 §3g and EX-32 §1.

**The fix verified end-to-end (EX-32's re-anchor, reproduced byte-for-byte).**
Re-derived from the landed table by applying EX-32's stated change
(`must_match` gains the optional group `(UNEVALUABLE > )?`, note replaced) with
the canonical byte form `json.dumps(obj, indent=2, ensure_ascii=False) + "\n"`:

| object | re-derived | EX-32 claims |
|---|---|---|
| re-anchored table sha256 | `a810bd17ea416fe0f3ed9e053e1e470ae833718f457b6d39399478c93de91a7b` | identical |
| pattern vs round-2 row / revised row | `True` / `True` | both worlds hold |
| landed table sha256 | `bfc42f1bb131cbe3a972a16647d24b1f16d936083dd61496589540e791d58bb7` | identical |
| landed expected.json sha256 | `d97dd60a942eaf53771c8224e84a9e8cdaf976dc66c3a543a450b1f1fa3827e2` | identical |

Then, with the re-anchored table in the clone and the digest re-pinned in a copy
of `expected.json` (`expected.json` is a single line, no trailing newline; only
`pointer_table.sha256` moves), the **real probe** reads
`reported findings=0 exit=0` and `--strict: clean findings=0 exit=0`. Control:
the re-anchored table against the **old** expected pin reads
`pointer_table_tampered … exit=2` — i.e. the re-pin is load-bearing, not
cosmetic. The four custody-README anchors are green against **both** this
emission's patched README and EX-21's landed README.

**Before → after measured by this seat (base blob vs landed revision).**
Base = `git show HEAD:…` blob `112d01dc…` (889 lines); after = the worktree
revision `7cd19c3c…`. Each injection was run twice, once per revision, on
scratch fixtures:

| hole | base (`112d01dc…`) | landed (`7cd19c3c…`) |
|---|---|---|
| D2a blocked parent dir | capture `13` + `EXISTS: no` + `STAT-ERROR`; verify vs live **`MATCH exit 0`** (fail-open) | capture `14` + `EXISTS: yes` + `READ-ERROR`; verify `UNEVALUABLE exit 14` |
| D2b mode-000 file | `PermissionError` traceback, `rc=1`, no receipt | capture `14`, receipt written, `READ-ERROR` recorded |
| D3 1-of-5 reference | plain `MATCH exit 0`; `--require-paths` unrecognised (argparse `2`) | plain `MATCH exit 0` (declared default); gated `2` + `REFERENCE-COVERAGE: 1/5 … unaccounted: <five>` |
| guard `--paths X --out X` | `rc=0`, X **clobbered** (now begins `# custody-pair receipt`) | `USAGE: refusing to write …`, `rc=2`, X intact |
| guard, hardlink alias | (r2 D7) resolved-path guard evaded | same refusal via the inode arm, target intact |
| D6 `selftest --scratch <missing>` | `FileNotFoundError` traceback, `rc=1` | `USAGE: scratch base is not a directory: …`, `rc=2` |
| selftest count | `CLEAN cases=15` | `CLEAN cases=22` |

No custody path was read, renamed or `utime`d; the only custostat reads are the
tool's own `paths` output and the receipts. The lane repo was read-only for this
seat apart from the two patch-text files it owns and this seat report.
