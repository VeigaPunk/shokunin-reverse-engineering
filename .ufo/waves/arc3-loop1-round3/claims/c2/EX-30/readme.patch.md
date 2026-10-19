# EX-30 — README patch text for the revised custody-pair tool

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

## 4. Why the README must change (`readme.patch.md`)

The gate README is the instrument's own contract document; at HEAD it documents
the pre-revision exit map, the 15-case selftest, and a write scope limited to
the canonical five. Every section the claim touches has a stale clause. The
patch moves the README to the revised contract in one artifact: a revision line
with the tool's self-pinned sha256, the usage block, the exit table (+14), the
capture exit paragraph, the severity precedence, a new **Reference coverage**
section, a new **Write scope** section, the selftest case list with its CLEAN
line, and the round-evidence pointer.

Deliberate detail: the selftest paragraph states that an explicit `--scratch`
must be an **existing** usable directory — the revised tool chose the
fail-closed repair (USAGE) over creating operator-named directories, and the
README must not imply the friendlier variant.

## 5. The patch — unified diff against `.ufo/gates/custody-pair/README.md` at HEAD

Apply from the repo root: `patch -p1 < readme.diff` (or `git apply`). Line
effect: 132 → 188 lines (new sections and lines only; no line inside
an untouched paragraph moves).

```diff
--- a/.ufo/gates/custody-pair/README.md
+++ b/.ufo/gates/custody-pair/README.md
@@ -11,6 +11,13 @@
 ~/.profile
 ```
 
+Revision (wave `arc3-loop1-round3`, seat EX-21, from seat EX-30's patch text):
+closes round-2 debt D2 (unevaluable paths), D3 (`--require-paths` reference
+coverage), the write-guard scope finding (`set(--paths) ∪ CUSTODY_PATHS`, by
+resolved path and inode) and D6 (`selftest --scratch` guard). Revised tool
+sha256 `7cd19c3cfd835c7807d5e60dece1c2592c9df6c319a78deb14469dd6ebe8ab09` — every receipt this revision writes self-pins that
+digest, and the round's post-pair must be captured by this revision.
+
 `custody-pair.py` is the committed instrument. It is **read-only over every path
 it inspects**: files are opened for reading only (sha256), never for writing,
 never renamed, and no `utime` is ever called on them. Capturing a receipt changes
@@ -28,7 +35,11 @@
 # verify a receipt against the live filesystem
 python3 custody-pair.py verify receipt-A.txt --live
 
-# fixture-based selftest (never touches a custody path)
+# fail closed when the reference covers fewer than N of the canonical paths
+python3 custody-pair.py verify receipt-A.txt --live --require-paths 5
+
+# fixture-based selftest (never touches a custody path; an explicit --scratch
+# must be an existing usable directory — otherwise USAGE, exit 2)
 python3 custody-pair.py selftest [--scratch /dev/shm]
 
 # print the 5 canonical paths
@@ -82,18 +93,40 @@
 | 11 | `REWRITE-DRIFT` | digest equal but `inode`/`ctime`/`mtime` moved on ≥1 path (same-content rewrite) |
 | 12 | `METADATA-DRIFT` | digest + identification times equal but `mode`/`uid`/`gid`/`size`/`type` differ, or an `EXTRA-PATH` appears on the candidate side, or a receipt's own epoch/render pair is inconsistent (`LABEL-INCONSISTENT`), or a v1 label defect is reproduced (`LABEL-DEFECT`) |
 | 13 | `ABSENT` | ≥1 reference path is missing on the candidate side |
+| 14 | `UNEVALUABLE` | a path exists but could not be evaluated (EACCES on open, or a stat error other than ENOENT) — classified before the both-absent branch, never a fail-open `MATCH`; the receipt is still written with `READ-ERROR`/`STAT-ERROR` on that path |
 | 2 | `USAGE` | bad arguments, unreadable/unparsable receipt, or a refused/failed write |
 | 3 | `SELFTEST-FAIL` | a selftest case failed |
 
-`capture` exits `0` with every requested path present (5/5 for the default set)
-and `13` when at least one requested path is absent — the receipt is written
-either way, recording `EXISTS: no`.
+`capture` exits `0` with every requested path present (5/5 for the default set),
+`14` when at least one path is present but unevaluable, else `13` when at least
+one requested path is absent — the receipt is written either way, recording
+`EXISTS: no`, or `READ-ERROR`/`STAT-ERROR` for an unevaluable path (an absent
+path is never invented from a read failure).
 
 Severity precedence for the verdict of a `verify` run: `CONTENT-DRIFT` >
-`ABSENT` > `REWRITE-DRIFT` > `METADATA-DRIFT` > `MATCH`. The report always prints
+`UNEVALUABLE` > `ABSENT` > `REWRITE-DRIFT` > `METADATA-DRIFT` > `MATCH`. A
+path unevaluable on either side is classified `UNEVALUABLE` (exit 14) before
+any field comparison — an unreadable path can never read as a clean `MATCH`. The report always prints
 per-path classes, a `SHA256-CONTRACT: n/m paths agree on sha256` line, and a
 final `CUSTODY_PAIR_VERIFY: <class> paths=… drift=… exit=…` line.
 
+## Reference coverage
+
+`verify` compares the paths the reference receipt carries. A reference that
+covers only part of the canonical set therefore verifies clean over what it
+carries and says nothing about the rest. `--require-paths N` makes that
+explicit: when the reference's path count is below N, the run prints
+
+```
+REFERENCE-COVERAGE: n/N paths present in reference; unaccounted: <list>
+```
+
+and exits 2 (`USAGE`) instead of comparing — the round's own pre/post pair is
+gated with `--require-paths 5`. The flag applies to v1 and v2 references
+alike; without it, the comparison covers exactly the reference's paths and no
+coverage line is printed (RV-8 measured 0 lines on a 1-of-5 reference with
+`MATCH … exit=0`).
+
 ## v1 compatibility
 
 Three v1 shapes are parsed and compared on the fields they actually carry:
@@ -114,19 +147,42 @@
 ## Selftest
 
 `selftest` builds all fixtures in a scratch dir (never a custody path) and runs
-15 cases: capture shape + sidecar identity, receipt-vs-live clean, same-content
+22 cases: capture shape + sidecar identity, receipt-vs-live clean, same-content
 rewrite in place (ctime pin) and via rename (inode pin), content drift, absent
 path, mode drift, TZ-independence of the UTC render, v1-stanza/v1-sums/v1-pipe
-compatibility with mutation detection, unparsable-receipt usage exit, and the
-refusal to write a receipt over a custody path. It ends with
+compatibility with mutation detection, unparsable-receipt usage exit, the
+refusal to write a receipt over a custody path, and the closure cases — an
+exists-but-unreadable path → `UNEVALUABLE` (never a fail-open `MATCH`), a
+reference below `--require-paths` → `USAGE`, `selftest --scratch` on a missing
+or unusable directory → `USAGE` (not a traceback), and the write guard over a
+`--paths` override → `USAGE`. It ends with
 
 ```
-CUSTODY_PAIR_SELFTEST: CLEAN cases=15 passed=15 failed=0 exit=0
+CUSTODY_PAIR_SELFTEST: CLEAN cases=22 passed=22 failed=0 exit=0
 ```
 
+## Write scope
+
+The write guard covers `set(--paths) ∪ CUSTODY_PATHS`, matching on the resolved
+path and on the inode: `capture` refuses (exit 2, `USAGE`) to write its
+receipt over any path it is measuring — including a hardlink alias — so the
+`--paths X --out X` override cannot silently clobber the file it measures. The
+guard is a self-harm guard, not a security boundary; same-privilege writers and
+TOCTOU are outside it (see the round-2 threat-model boundary note).
+
+Named residual (RV-8, re-measured by seat EX-30 at the same revision): the
+guard checks the receipt path only. The sidecar path (`<out>.sha256`) is not
+guarded, so `capture --paths X.sha256 --out X` exits 0 and overwrites the very
+file it measured. Treat `<out>.sha256` as an output path, never as a measured
+path, until the guard covers the sidecar too.
+
 ## Round evidence
 
-`../waves/arc3-loop1-round2/claims/c3/EX-31/` holds the live pre/post pair
+The round's own live pre/post pair, its injection transcripts (the four named
+holes reproduced as their declared classes), and the revision map when the
+pair spans tool revisions are committed under
+`.ufo/waves/arc3-loop1-round3/claims/c2/`. `../waves/arc3-loop1-round2/
+claims/c3/EX-31/` holds the round-2 live pre/post pair
 (`capture-pre.txt`, `capture-post.txt` + sidecars, both 5/5 exit 0), the
 matching `verify` runs, the v1-compat runs, the six-attack harness
 (`attacks.sh` → `attacks.out`), and the selftest transcript.
```

## 6. What the README patch does NOT claim

It does not assert the round's own pair is green (the pair is captured and
verified by other seats), and it does not name round-3 receipt filenames (they
land with the receipts). The round-evidence paragraph is written so a pair that
spans tool revisions is described by a revision map rather than presented as
same-revision — the r2 debt D8 shape.

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
nothing is copied from the earlier emission or from another seat. The full
evidence block (identities, instrument runs, before→after table, collision and
re-anchor proofs) is in `registry-row.patch.md` §13 — the two artifacts are one
patch pair and share the same base/identity tables.

**What was missing and what this seat completed.** The two patch texts existed
(v2); the seat report `seats/EX-30.md` was missing. This seat re-derived every
byte-identity, corrected one evidence digit, re-ran the instrument-in-the-loop
checks against the **current** emission, measured the base "before" state on the
base blob itself, and wrote the seat report.

**Stale §8 note (rule #14).** §8's clone evidence was produced at clone rev
`26ff6888` against an *earlier* emission — that clone's README carries the
literal placeholder `<TOOL-SHA256>` and its SKILL.md is `cf5c3991…` (a 19-case
row). It is a valid record of what was tested then, but it is **not** evidence
for the current bytes. §13 supersedes it as the landing-time evidence.

**Re-derived identities for this artifact's own subject matter.**

| identity | value |
|---|---|
| landed worktree README (EX-21, supersedes this patch's base) | `f30df42e0a547a0aefd21590c0f975acf06d91161fcb6db77c8934960efeb193`, 185 lines |
| this patch's base README | `fa484d57…` (132 lines) — `git show HEAD:` |
| this patch's target README | `42b07ee5…` (188 lines) |
| tool under description | `7cd19c3c…`, 1155 lines, `CLEAN cases=22` |

**Supersession, re-confirmed (the landing decision this artifact feeds).** The
worktree README is EX-21's; applying this patch's diff on top of it is not the
landing path. Clause-by-clause the landed README carries every semantic element
this patch proposes — `UNEVALUABLE`, `--require-paths` (×6), `REFERENCE-COVERAGE`,
`READ-ERROR`/`STAT-ERROR`, the inode-arm guard, `cases=22`, the never-`/tmp`
rule — and adds the `selftest --scratch` and write-scope sections. Two
differences the parent should weigh, both **deliberate in this artifact and both
verified against the landed tool**:

1. **Coverage line.** This patch states that without `--require-paths` no
   coverage line is printed (measured: 0 lines on a 1-of-5 reference that reads
   `MATCH exit 0`; the call site is inside the flag branch). EX-21's README says
   the comparison is "exactly the reference's paths, unchanged" — true, and it
   does not promise the line, so the two texts do not contradict.
2. **Sidecar residual.** This patch names the sidecar path (`<out>.sha256`) as
   an unguarded residual (`capture --paths X.sha256 --out X` exits 0 and
   overwrites the measured file). EX-21's README makes no sidecar claim, so
   landing EX-21's text neither ships nor contradicts the finding; the residual
   remains **open** and unrecorded in the landed README — worth a one-line
   follow-up if the parent wants the record complete.

**The fix verified end-to-end** (EX-32's pointer-table re-anchor, reproduced
byte-for-byte: table `a810bd17…`, pattern true against both the round-2 and the
revised row; with the digest re-pinned the real probe reads `findings=0` in both
modes, and the un-re-pinned control reads `pointer_table_tampered exit=2`). The
four custody-README anchors are green against **both** this patch's target
README and EX-21's landed README. Details: `registry-row.patch.md` §13.

No custody path was read, renamed or `utime`d. The lane repo was read-only for
this seat apart from the two patch-text files it owns and this seat report.
