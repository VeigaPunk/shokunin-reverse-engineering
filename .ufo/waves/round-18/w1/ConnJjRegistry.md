# ConnJjRegistry — jj semantics for the SKILL.md gate registry (`SKILL.md:445-546`)

Seat `KaidokuR18.ConnJjRegistry`, round 18, w1. Read-only connector: no gate, selftest,
REA, Ghidra or carrier execution; no installs. Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.

Inputs connected: `.ufo/waves/hyaku/jj-w1/reports/JjAuditKaidoku.md` (audit) and
`JjTrialKaidoku.md` (trial) → the 17 registry rows. Baseline `9011581d84527ba34c675f9cf912e54d2e72d470`.

## 0. The move (one bounded proposal)

**One normative paragraph under the registry intro (`SKILL.md:443`) + six appended fifth-cell
clauses. No new row, no new column, no edit to any command cell.**

Why this shape and not per-row annotations (all observed):

- `invocation-audit.py:159-170` derives each row's command from the **first backticked span of
  cell 3** and counts rows whose 2nd cell matches `(probe|gate|tool) / kaidoku`. Editing cell 5
  leaves `rows` and `command` unchanged; editing cell 3 changes the audit surface.
- `temporal-sweep.py:37-43` lists **`SKILL.md` itself** as a site source (line 42), matched
  against `SITE_PATTERN` (`temporal-sweep.py:59-63`). New row prose is scanned.
- C1's `R17-REGISTRY` check owns the fifth cell of `go-route-compare`, `receipt-validate`,
  `pins`, `go-buildinfo-probe` (must contain `Write scope:`). A second editor of those cells
  must merge, not replace.

Non-obvious join: **the registry is not the tool census.** Three live `HEAD` sites exist
(audit §5) and only two have rows (`citation-drift`, `custody-pair`); the third,
`verify.py:59`, has **no row** and reaches the registry only through the "exercised argv"
citations two rows make to its output. Six rows describe tools with no `HEAD` read at all
(`go-snapshot-inventory`, `go-log-extract`, `go-route-predict`, `go-route-compare`,
`receipt-validate`, `go-buildinfo-probe`). A row-local-only treatment therefore leaves one live
`HEAD` site undocumented and over-annotates six safe ones; the invariant belongs at table level,
and the two rows that cite `verification.json` carry the unregistered producer's provenance.

## 1. Observed ground truth (command, output, exit code)

```
$ git rev-parse HEAD
9011581d84527ba34c675f9cf912e54d2e72d470                                   rc=0
$ git rev-parse --verify 'refs/heads/main^{commit}'
9011581d84527ba34c675f9cf912e54d2e72d470                                   rc=0
$ git rev-parse --verify 'refs/remotes/origin/main^{commit}'
9011581d84527ba34c675f9cf912e54d2e72d470                                   rc=0
$ git symbolic-ref -q HEAD
(no output)                                                                rc=1
$ git rev-parse --abbrev-ref HEAD
HEAD                                                                       rc=0
$ git branch --show-current
(empty)                                                                    rc=0
$ git rev-parse '@{u}'
fatal: HEAD does not point to a branch                                     rc=128
$ git merge-base --is-ancestor HEAD refs/heads/main
(no output)                                                                rc=0
$ ls -d .jj
.jj                                                                        rc=0
$ git status --porcelain
?? .ufo/waves/round-18/                                                    rc=0  (1 line)
$ git status --porcelain --untracked-files=no
(empty)                                                                    rc=0
$ git hash-object SKILL.md
cfa3b54c87d267fb4fcf14f4036804d1a8b6a0e8
$ git rev-parse 9011581d84527ba34c675f9cf912e54d2e72d470:SKILL.md
cfa3b54c87d267fb4fcf14f4036804d1a8b6a0e8                                   rc=0
```

- **Observation.** The lane is colocated and HEAD is detached, yet numerically equal to
  `main` and `origin/main` at measurement. All three `HEAD`-keyed sites are therefore **green by
  coincidence on this checkout**; the defect only appears off-branch, the state the audit
  retained (`HEAD=f87053c4…`, `main=origin/main=4c63e873…`,
  `merge-base --is-ancestor` exit 1 — `JjAuditKaidoku.md` §2 F2).
- **Observation.** `SKILL.md`'s worktree blob equals the baseline blob, so every line number in
  `:445-546` below is stable at the declared baseline.
- **Observation.** `.ufo/waves/round-17/verification.json` exists and is tracked at the
  baseline; its JSON has `source_revision: d0ab2992149a38794e5ef2474ba5d4ef5ee1e905` and
  `source_branch` / `head_equals_source` **absent** (a jq query returns `null`). Its retained
  argv that name a revision (`citation-strict`, `controls`, `temporal-sweep-source`,
  `invocation-audit-baseline`, `measure-source`) pass explicit 40-hex revisions and exit 0;
  `custody-capture` is a live capture (`--label round-17`) with no revision argument.
- **Observation.** `.ufo/waves/round-17/custody/custody-r17.v2.txt:8-9` records
  `# cwd: …/kaidoku-shokunin` and `# repo-HEAD: d0ab299…` — the same `HEAD` read.
- **Observation.** `git clone --no-local <LANE> /tmp/…/sb` of this detached-HEAD lane yields an
  **attached** clone (`symbolic-ref -q HEAD` → `refs/heads/main`, `refs/heads/main` present at
  `9011581d…`). C2's `jj-red-before.py` sandbox precondition holds; sandbox removed after the probe.
- **Inference.** `snapshot.auto-track="none()"` is the lane's live setting: not re-read here
  (`jj` in the lane is barred by contract); taken from the shared contract and
  `JjTrialKaidoku.md` step 2 (observed repo config).

## 2. Proposed table-level paragraph

Insert after `SKILL.md:443` (before the blank line and the `| Name |` header at `:445`). It covers
every row without touching a command cell.

```markdown
**jj colocation (jj 0.45.1; lane `.jj` present).** Under jj, `git rev-parse HEAD` is the
working-copy parent `@-`: detached (no branch ref), possibly off-branch and unpushed, and
`git show HEAD:<path>` still succeeds — a `HEAD`-keyed read returns data, just not the landed
tree. Every revision these rows accept is an on-branch commit: the measured revision is the
pushed branch tip (`git rev-parse --verify 'refs/heads/main^{commit}'`, and prove
`refs/heads/main == refs/remotes/origin/main`), baselines are its ancestors. Bare `HEAD`,
`@{u}`, `--abbrev-ref`, `--show-current` and `symbolic-ref` are not spellings of a revision
here. `snapshot.auto-track="none()"` snapshots only tracked paths: an untracked file is
**absent at every revision**, so a revision-scoped row reports it absent (a false red when you
expected the worktree copy), while a working-tree-scoped run reads commit `@`'s content, not
`main`'s. Cite the helper's `pushed` hash, never `committed` (a rebase-recovery rewrites it).
Entries that name a relative script path (`interactive-r1-recovery`, `quote-fidelity`) run from
the lane root.
```

The paragraph covers `interactive-r1-recovery` (:447), `quote-fidelity` (:450),
`round16-structural-controls` (:507), `round17-structural-controls` (:546),
`go-selection-preview` (:506) and `go-route-predict` (:539); the five
no-repository-state rows (:487, :538, :540, :541, :545) need no note at all. Only the six
rows in §4 need their own clause.

## 3. Row map (17 rows, exact anchors)

Class: **REV** = Git objects at an explicit revision; **WT** = working tree / cwd / live paths;
**NONE** = installed data or a supplied file only.

| `SKILL.md` | row | class | HEAD assumption | working-tree assumption | cell edit |
|---|---|---|---|---|---|
| 447 | interactive-r1-recovery | WT | none | entry path is cwd-relative; reads checkout `expected.json`/`result.json` (`verify-recovery.py:12-14` anchors the script, not the cwd) | no — paragraph |
| 448 | citation-drift | REV + WT inputs | **`--rev` default `HEAD`** (`citation-drift-probe.py:477`); the default tree is `@-` (audit R2) | `--table`/`--expected` read from the worktree, guarded by the pinned table sha256 | **yes** |
| 449 | custody-pair | WT | **`git rev-parse HEAD`** (`:327`) and **`Path.cwd()`** (`:349`); `capture` has no `--repo` (`:1315-1319`) | reads 5 live paths; header pins `# cwd:`/`# repo-HEAD:` (`:348-349`) | **yes** |
| 450 | quote-fidelity | WT | none | entry path cwd-relative; manifest/source bytes resolved from the passed path (`:274`) | no — paragraph |
| 487 | go-snapshot-inventory | NONE | none | none (installed data, absolute `--ghidra`) | no |
| 506 | go-selection-preview | WT script + NONE data | none | runs the checkout's `selection.py` + fixtures; installed data read-only | no — paragraph |
| 507 | round16-structural-controls | REV | accepts `<BEFORE> <AFTER>`; no default; `HEAD` would be accepted silently | none — "worktree is never touched" (`round-16/controls.py:6-7`) | no — paragraph |
| 537 | go-carrier-run | WT | none | reads `predictions/carriers.tsv`, writes `runs/<LABEL>/` (`run-carriers.sh:11,38`) | **yes** |
| 538 | go-log-extract | NONE | none | supplied log path only | no |
| 539 | go-route-predict | WT import + NONE data | none | imports the checkout's `selection.py` by absolute path (`predict.py:71-74,96-101`) | no — paragraph |
| 540 | go-route-compare | NONE | none | two supplied JSON files | no |
| 541 | receipt-validate | NONE | none | hashes recorded paths **now** — already correctly scoped by its own cell | no |
| 542 | pins | WT | none | live paths at two instants; `pins.py` has no Git argv | **yes** |
| 543 | temporal-sweep | REV | accepts `--rev`/`--sites-rev`; no default; `HEAD` accepted silently; `--sites-rev` defaults to `--rev` (`:416-420`) | none for data; `SKILL.md` is itself a site source (`:42`) | **yes** |
| 544 | invocation-audit | REV | accepts `--rev`; no default (`:466`); `HEAD` accepted silently | none for data (`:281-285` reads `SKILL.md` and receipts at rev) | **yes** |
| 545 | go-buildinfo-probe | NONE | none | supplied path only | no |
| 546 | round17-structural-controls | REV | accepts `<BEFORE> <AFTER>`; no default | none (`controls.py` reads objects; `HEAD` at `:442` is a fixture helper) | no — paragraph |

Answers to the two assigned questions:

- **Rows whose entries or recheck commands assume `HEAD`:** `citation-drift` (default `--rev`,
  the recheck path), `custody-pair` (the entry itself), and — without a row — `verify.py`
  (produced the `verification.json` both rows cite). `round16/round17-structural-controls` and
  `temporal-sweep`/`invocation-audit` do not *default* to `HEAD`, but accept it silently as a
  revision; `temporal-sweep` additionally couples `--sites-rev` to `--rev` when omitted.
- **Rows whose entries assume a working-tree state:** `interactive-r1-recovery`, `quote-fidelity`
  (cwd-relative entry + checkout reads), `custody-pair` (cwd + live files), `go-carrier-run`
  (predictions in, `runs/` out), `pins` (live instants), `go-selection-preview` and
  `go-route-predict` (worktree script/fixtures). `receipt-validate` is the counter-example: its
  cell already says "now", so it needs no note.

## 4. Proposed cell text (six appends; paste verbatim)

Each block is appended to the **end** of the row's fifth cell, before the closing `|`.
Each avoids the substring `unexercised` (it would trip `invocation-audit.py:321`) and avoids
`SITE_PATTERN` phrases (it would create a `temporal-sweep` site).

**`SKILL.md:448` — citation-drift**

```text
 **jj:** `<REV>` is an on-branch pushed commit, never `HEAD`; the bare recheck resolves `refs/heads/main`, and `--rev HEAD` is refused with exit 2 `head_not_branch_tip` when HEAD is not the tip (round-18 C2; before it, the default is `HEAD` = `@-`). The `--table`/`--expected` inputs come from the working tree and the table's sha256 pin is the guard; every graded path comes from `<REV>`, where a path that was never tracked is absent — `citation_file_absent` for a file visible in the editor is a tracking gap, not drift. The retained round-17 `verification.json` is a `HEAD`-derived record (`source_revision d0ab299…`, no branch field): it attests argv, not a branch tip.
```

**`SKILL.md:449` — custody-pair**

```text
 **jj:** the header pins the repo it measured by `# cwd:` and `# repo-HEAD:`; under jj `repo-HEAD` is `@-`, the working-copy parent, not necessarily `main` — cite it only with the branch identity (`--repo` names the root instead of `Path.cwd()`; `# repo-root:`, `# repo-branch:`, `# repo-branch-tip:`, `# repo-HEAD-is-branch-tip:`, `# repo-dirty:` are round-18 C2). The retained round-17 receipt records `repo-HEAD d0ab299…`, a `HEAD` read.
```

**`SKILL.md:537` — go-carrier-run**

```text
 **jj:** `predictions/carriers.tsv` and `runs/<LABEL>/` are working-tree paths (`run-carriers.sh` cds to its own directory); the "frozen in Git before the run" claim holds only when the prediction blob at the cited revision equals the bytes consumed, and an untracked `runs/` is absent at that revision — track the trees a later receipt is meant to see.
```

**`SKILL.md:542` — pins** (append **after** C1's `Write scope:` sentence; see §5b)

```text
 **jj:** the two instants are working-tree instants of `@`, not revision content; a path can move with no Git record (untracked under `auto-track="none()"`), so bind a `compare` to the commit or receipt whose tree it is meant to bound.
```

**`SKILL.md:543` — temporal-sweep**

```text
 **jj:** `--rev` and `--sites-rev` are on-branch commits, never `HEAD`; omitting `--sites-rev` defaults it to `--rev`, which collapses baseline and measured revision to one commit — supply the baseline explicitly. This file is itself a site source, so new during-run wording in a row becomes an unqualified site.
```

**`SKILL.md:544` — invocation-audit**

```text
 **jj:** reads `SKILL.md` and every receipt at `<REV>` only; under `snapshot.auto-track="none()"` a receipt written but not tracked is invisible, so the `absent`/`unreadable` accounting describes the committed set, not the worktree — integrate receipts (and the row text being audited) before citing a count, and never pass `HEAD` (`@-` resolves silently and grades an off-branch tree).
```

## 5. Second-order effects and collisions

**(a) `invocation-audit` parse surface.** `cells[3]` is the command cell; the command is its
first backticked span (`:159-170`). All six edits land in `cells[5]`: `rows` stays 17 and every
`command` value is unchanged, so `exercised_match`/`unlabelled_variant` cannot move because of
this text. The word `unexercised` would flip classification for an unmatched row (`:321`); none
of the drafts contains it.

**(b) C1 `R17-REGISTRY` collision on `pins`.** C1 requires the fifth cell of `go-route-compare`,
`receipt-validate`, `pins`, `go-buildinfo-probe` to contain `Write scope:`. None of those four
cells contains it at the baseline, so C1 edits them. The `pins` jj clause must be **appended after**
C1's sentence, never substituted for it, or `routed-defects.py`'s R17-REGISTRY check re-opens.
`citation-drift`'s kind cell changes `probe` → `gate` under C1; that is cell 2 and does not touch
the clause in §4.

**(c) `temporal-sweep` scans this registry.** `SKILL.md` is in `SITE_SOURCES`
(`temporal-sweep.py:42`), matched by `SITE_PATTERN` (`:59-63`). All six clauses and the paragraph
avoid `unchanged (during|across|throughout) (the )?(run|execution)`, `stable throughout` and
`pins_unchanged_during_run`. Any integrator rewording must re-check this, or the delivered
revision gains an unqualified site and the tool's counts move.

**(d) No-harm control.** `SKILL.md` was byte-identical to the baseline blob `cfa3b54c…` at
measurement, so the integration delta is exactly six changed lines plus one inserted paragraph.
Those seven changes must appear in `W18/controls.py`'s listed SKILL.md lines.

**(e) The unregistered producer.** `verify.py:59` is the only `HEAD`→revision conversion on the
gates' execution path and it has no registry row. Fixing it (C2) does not retroactively make
`verification.json` branch-attested: the file keeps `source_revision d0ab299…` and no branch
field. Both citation-owning rows therefore need the provenance sentence in §4; without it a reader
infers branch attestation from a field name.

**(f) Live `none()` instance.** `git status --porcelain` shows `?? .ufo/waves/round-18/`: the
entire round-18 tree is untracked. At any revision, `routed-defects.py` will not see
`.ufo/waves/round-18/evidence/validate16/summary.json` and `invocation-audit` will not see any
round-18 receipt until the integration commit names the tree. C1's own falsifiability
(`open 6 → 0`) therefore depends on integration; a run at an un-integrated revision returns
could-not-evaluate, not "closed". This is the assignment's `auto-track none()` example, observed
rather than hypothetical.

**(g) The lint cannot protect the prose.** C2's `head-rev-lint` scans tracked `*.py`/`*.sh` under
`.ufo/gates`, `.ufo/rounds`, `.ufo/waves/round-14…18`. `SKILL.md` is not a site, so these edits
leave `live_count` untouched — and nothing else enforces the paragraph's rule on future rows.

**(h) A second unpinned layer.** `verify.py:45` imports `pins.py` from the working tree, and
`predict.py:96` imports `selection.py` from the working tree; `receipt-validate.py:53` likewise
loads `pins.py` from `__file__`'s directory. A rev-pinned data read therefore still executes
worktree tool code. `verification.json` records the producer path, not its digest, so even a
`jj`-safe revision pin does not make the instrument's bytes revision-bound. Relevant to the
`go-route-predict` row only as a known limit; no cell text proposed (the row claims no revision).

**(i) Cwd fragility is elsewhere than expected.** `run-carriers.sh:11` cds to its own directory
and `predict.py:71-74` uses an absolute path, so those two rows are cwd-independent. The only
cwd-relative entries are `interactive-r1-recovery` and `quote-fidelity`, which the paragraph
names.

## 6. Verification the L1 should run (after integration)

1. `invocation-audit.py --root LANE --rev <REV>` → `rows: 17`; no row becomes
   `unlabelled_variant` because of these edits (command cells untouched).
2. `temporal-sweep.py --root LANE --rev <REV> --sites-rev <BASELINE>` → the site count must not
   gain an entry from the new lines; `grep` the seven new lines against the `SITE_PATTERN` first.
3. `routed-defects.py --root LANE --rev <REV>` → R17-REGISTRY still finds `Write scope:` in all
   four fifth cells after the `pins` merge.
4. `controls.py` (W18) → the six changed `SKILL.md` lines plus the inserted paragraph are listed.
5. `head-rev-lint.py` → `live_count` unaffected by these edits (code-only scan); it must reach 0
   only through C2's three code fixes.

## 7. Limits and disclosure

- **Probe error, disclosed:** one `jj --version` ran with cwd = the lane (contract bars `jj` in
  LANE). It is a pre-repo command; no `-R`/repo operation was requested. `.jj/working_copy` mtime
  remained `2026-10-20 12:06:58.386062960 -0300`, earlier than the probe, so no snapshot was
  taken [inference from mtime; a snapshot writes under `.jj/working_copy`]. No other `jj`
  invocation occurred.
- All other commands were read-only `git` (`rev-parse`, `symbolic-ref`, `branch --show-current`,
  `merge-base`, `status`, `hash-object`, `ls-tree`), one `git clone --no-local` into a
  `mktemp -d` under `/tmp` (removed, `cleanup_rc=0`), and file reads.
- No gate, selftest, REA or Ghidra run. All quoted lane-tool exit codes come from the retained
  `.ufo/waves/round-17/verification.json`, not from re-execution (audit §8's limitation carries
  over).
- `snapshot.auto-track="none()"` is not re-read in-lane; it is taken from the contract and
  `JjTrialKaidoku.md` step 2.
- Line numbers are baseline-stable because the worktree `SKILL.md` blob equals the baseline blob.
- `[INFERENCE]` marks: the consequence chain from `source_revision` to "what a reader assumes",
  and the no-snapshot claim from the `.jj/working_copy` mtime.

Report: .ufo/waves/round-18/w1/ConnJjRegistry.md
