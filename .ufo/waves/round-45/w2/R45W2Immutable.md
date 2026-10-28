# R45W2Immutable — falsifying `corpus/SOURCES.md` append-only across the round-45 range

Seat: leaf attack seat, round 45 wave 2. Lane root
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Assigned attack: **registry append-only**
(`tools/round-38/registry-immutable.sh`) over base `149133d47aa7e90796f96047afe6d251a3e65b2c`
→ head `f59565b782c18b0eb691bec12f52d2f80d9f5032`.

The lane tip advanced while I attacked it — `0ee50aaf` at my first measurement, `84cb9da5` at the
penultimate, `99fdb9e4` at the last (`git log --oneline 0ee50aaf..99fdb9e4` = 6 commits: `e00b9f6b`,
`b142b76b`, `17ce00f0`, `ef3edf4b`, `84cb9da5`, `99fdb9e4`, the last being the L1's repair of my own R-1). Every claim below names the revision it was measured at; the range I was given
(`149133d4..f59565b7`) is reported separately from the extra ranges I checked afterwards. Frozen paths were verified untouched at every step:
`git log f762b727..84cb9da5 -- tools/round-45 plans/round-45-claims.md` prints nothing and
`git status --porcelain` over the same paths is empty, so no receipt here is contaminated by a
post-freeze touch (including none of mine — I wrote only under
`.ufo/waves/round-45/w2/R45W2Immutable/`).

Scratch: `/fast/scratch/hyaku/kaidoku-r45/R45W2Immutable` (`TMPDIR` and `HYAKU_SCRATCH` pinned
there; every fixture asserted `git -C "$D" rev-parse --show-toplevel` == `$D` before its first
commit); removed after the receipts were copied into this directory. No tool installed; no mutating
git/jj command run on the lane. Python 3.14.8, git 2.56.0, linux 7.2.11-arch1-1.

---

## 1. The assigned attack — result

**Exact invocation** (usage is `registry-immutable.sh LANE BASE REV`; no other flags exist — `--selftest`
is the only one, and the run mode takes positionals):

```sh
bash /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-38/registry-immutable.sh \
  /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
  149133d47aa7e90796f96047afe6d251a3e65b2c \
  f59565b782c18b0eb691bec12f52d2f80d9f5032
```

| field | value |
|---|---|
| exit | **0** |
| stdout | empty |
| stdout sha256 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (= sha256 of the empty string) |
| UTC | 2026-10-28T15:59:45Z (re-run 16:24:00Z at tip) |

**No `1` was produced, so there are no changed rows to name.** That is the honest result and it
needs to be defended twice: (a) the `0` is not the "row set reads empty" failure mode the SKILL
registry row documents for an unresolvable revision, and (b) the `0` is not vacuous because the gate
cannot see rows. Both are measured:

| non-vacuity check | value |
|---|---|
| rows the gate's own `rows()` extractor sees at BASE | 139 |
| … at `f59565b7` | 141 |
| … at tip `84cb9da5` | 141 |
| attacked script blob at base vs tip | `df59ec1ca8655191f96b1eb1f7350f69e5c9f7cd` **both** — the gate is byte-identical to its base form, so this is not a doctored copy passing itself |

Receipts: `A-gate-base-to-head.txt`, `G-final-tip.txt`, `F-gate-rowcount.txt`, `INVOCATION.txt`.
(`A-gate-base-to-head.txt` shows `stdout sha256 e3b0c442…` computed by `sha256sum` over an empty
stream; `date -u` geostamp in the same file.)

### 1.1 What "a 1 lists changed rows" would mean — demonstrated on fixtures, since the range is clean

The seat spec asks me to name the column and whether CORPUS rule 2 allows it, *for each row a `1`
lists*. No row changed, so I established the mapping by mutating fixture copies instead (each
fixture: `mktemp -d -p "$S"` + `git init -q -b main`, toplevel asserted, two committed revisions):

`awk -F'|'` fields: `2` id, `3` source, `4` kind, `5` tier, `6` scope, `7` anchor, `8` teaches,
`9` status, `10` opened, `11` recheck, `12` used-by. The gate skips exactly `c==9 || c==11 || c==12`.

Captured verbatim in `H-gate-columns.txt` (`utc: 2026-10-28T16:26:07Z`, one fixture repo, base
`e3fa9508`, each mutation its own committed revision):

| mutation (fixture, both revisions committed) | exit | stdout | CORPUS rule 2 verdict |
|---|---|---|---|
| control: base vs base | 0 | — | — |
| source cell (col 3) edited in place | **1** | `S001 changed columns: 3` | not allowed → correctly red |
| tier cell (col 5) edited in place | **1** | `S003 changed columns: 5` | not allowed → correctly red |
| scope cell (col 6) widened in place | **1** | `S001 changed columns: 6` | not allowed → correctly red (the M38-8 shape) |
| teaches cell (col 8) edited | **1** | `S001 changed columns: 8` | not allowed → correctly red |
| opened cell (col 10) edited | **1** | `S002 changed columns: 10` | not allowed → correctly red |
| trailing space only, inside a guarded cell | **1** | `S001 changed columns: 3` (`I-supplementary.txt`) | not allowed → red (byte-strict: a cosmetic reflow of an old row is a false positive, never a false clean) |
| status + recheck + used-by changed together | **0** | — | **allowed** → correctly green |
| a new row appended | **0** | — | **allowed** → correctly green |
| row deleted | **1** | `S003 row deleted (append-only)` | correctly red |
| two surviving rows swapped | **1** | `S003 row deleted (append-only)` + `S001 / S002 row reordered (append-only)` | correctly red (the deletion line is spurious: the swap displaced an id out of the compared window) |
| an existing id appended again (duplicate id) | **1** | `S003 changed columns: 3 6 7 8` + ` / S003 row reordered (append-only)` | correctly red (empty id in the second line — cosmetic) |
| id renumbered `S001`→`S0011` | **1** | `S001 row deleted (append-only)` | correctly red |
| **a 12th cell appended after `used-by`** | **0** | — | not allowed, **missed** (see F-1) |

So the gate's `1` output names the changed column correctly in every non-allowed case it models, and
its allow-list is exactly rule 2's three columns. The reason strings are noisy (row-deletion and
reorder both fire on a swap; a duplicate id yields an empty id field) but every one of those exits
is 1, i.e. fail-closed.

### 1.2 The gate's `0` alone does not establish the property — three blind spots

This is where the attack lands. A `0` from this gate means "no *matched* row's fields 2–12 differ".
Three shapes escape it; I reproduced each on **a clone of the real registry**, not only on a
synthetic fixture.

| # | shape | gate | independent instrument | live exposure |
|---|---|---|---|---|
| F-1 | a **12th cell** appended after `used-by` on an existing row (`NF` 13 → 14) | **exit 0** | `sources-census.sh validate` prints `E01 S139 fields=12` | none: head has 0 malformed rows |
| F-2 | an existing row **indented 4+ spaces** edited in place (both sides invisible to `^ {0,3}\|`) | **exit 0** | census row test is `/^\|[ \t]*S[0-9]{3,}[ \t]*\|/` (`sources-census.sh:619`) — no leading space allowed, so also blind | none: `grep -nE '^ +\|' corpus/SOURCES.md` is empty |
| F-3 | a **new row re-registering an existing row's URL+scope** (the M38-8 duplicate-row half) | **exit 0** | `sources-census.sh validate` → `W04 duplicate url … across scopes` (and `E04` when the scope is identical) | none: S140/S141 add **no** new W04 (14 before, 14 after) |

F-1 reproducer (clone of the lane at `HEAD`, S139 given a genuine 12th cell; its `used-by` cell
untouched, so the gate's 2–12 loop sees no difference): `awk -F'|'` prints
`NF=14  col12=[ corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md ]  col13=[ EXTRA-CELL ]`;
`registry-immutable.sh` exits **0**; `sources-census.sh validate --file` on the same bytes prints
`E01 S139 fields=12`. So the gate is a cell-differ for columns 2–12, not a schema gate; a reader who
treats its `0` as "the registry is well-formed" is wrong, and the round's own claim text does not say
that, so this is a **scope statement, not a falsified claim**. Recorded because the round-45 lesson
and the SKILL row present this gate as the append-only instrument, and only the census catches these
shapes.

F-4 (already documented, confirming): an **unresolvable revision** exits **1** with `git fatal:` on
stdout plus every row reported deleted, not `2`. `SKILL.md:1607` already states exactly that
("an unknown or unresolvable revision is **not** detected … so a `1` must be read with its row
list"), and round 39 measured it. It holds as documented; it is a `1`-is-ambiguous hazard, not a
false clean. Also measured: SOURCES.md **absent at base** → exit 1 listing every rev row as deleted;
**deleted at rev** → exit 1.

F-5 (cosmetic): a row reindented at base vs rev is reported as **deleted**, not moved — same exit,
wrong reason string.

Receipts: `B-gate-extra-cell.txt`, `B-gate-matrix.txt`, `C-strict-parser.txt`.

### 1.3 The independent check of the same question — this is the evidence for "only S140/S141"

Because the gate ignores whole-row classes, I re-ran the property with a **deliberately different
parser** (no indent anchor; `\| *(S\d{3,}) *\|` anywhere in the line; cell-by-cell compare with no
trim), against the blob bytes at each revision:

| quantity | base `149133d4` | head `f59565b7` |
|---|---|---|
| rows (strict parser) | 139 | 141 |
| added ids | — | **`['S140', 'S141']`** |
| removed ids | — | **`[]`** |
| surviving-row relative order preserved | — | **True** |
| changed cells across the 139 survivors (any column) | — | **0** |

So: **no existing row changed at all** — not merely none outside status/recheck/used-by
(a strictly stronger result than the assignment asked me to confirm), and **the only additions are
S140 and S141**. The strict parser also finds **0** rows that the gate's `^ {0,3}` anchor would miss
(`I-supplementary.txt`), so F-2 is latent, not present in this corpus.

Two further independent confirmations:

- **Per-commit, not endpoint.** `git log`/`diff-tree --numstat` over every commit in
  `149133d4..84cb9da5` shows exactly one commit touching `corpus/SOURCES.md`: `e715263c`, with
  `2 0 corpus/SOURCES.md` (two insertions, zero deletions). No intermediate touch-and-restore exists
  for this file, so the endpoint comparison the gate performs is not hiding anything here.
- **CORPUS census.** `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` →
  `kaidoku ok`, exit 0; row count 139 → 141; `W04` duplicate-URL warnings **14 before, 14 after**
  (S140/S141 introduce none); no `E`-class finding at head. The 200+ `E11 missing used-by` lines you
  see when the same bytes are validated via `--file` are an artifact of the used-by paths being
  resolved relative to the *file's* directory — copying head bytes into scratch reproduces the same
  233 `E11`, so it is not a registry change (recorded so the next reader is not misled).

⚠ One thing the census **cannot** enforce and the gate does not either: the `anchor` cell's
**revision** requirement. See §4.

---

## 2. `covers()` is inverted — the `pathspec` arm's false clean, and a proved fix

Not the assigned attack, but it is the instrument the round's R45-C1 predicate rests on and it is
the same "append-only / freeze" family, so I attacked it. **This overlaps routed R45-CL15**
("pin `covers()`'s direction") and **R45-CL18** (the pathspec boundary) and wave-2
`R45W2PathspecArm`; my contribution is the patch receipt, not a new claim of first discovery.

Shipped blob (`tools/round-45/frozen-path-preflight.py`, sha256
`633ebc058f0ea5a7c6dec4a9d6287e062eecf497fb6da674a3898c7c7130523b`):

```
def covers(pathspecs, frozen_path):
    """True when some pathspec equals or lies under the frozen path."""
    fp = frozen_path.rstrip("/")
    return any(p.rstrip("/") == fp or p.rstrip("/").startswith(fp + "/") for p in pathspecs)
```

The docstring says "lies under"; **coverage** means the pathspec is the frozen path *or an ancestor
of it*. Both directions are observable on one fixture (frozen dir `tools/round-45/{tool.py,other.py}`,
`other.py` tampered then restored):

| pathspec | relation | `other.py` modified | `other.py` tampered **then restored** | patched copy (both cases) |
|---|---|---|---|---|
| `tools/round-45/tool.py` | **subset** (one file) | 1 (blob arm catches the net change) | **0 clean — false clean** | **2 `pathspec_required`** |
| `tools/round-45` | exact | 1 | 1 | 1 |
| `tools` | **superset** | 2 `pathspec_required` — false refusal | 2 `pathspec_required` — false refusal | **1** |
| `.` | **superset** | 2 `pathspec_required` — false refusal | 2 `pathspec_required` — false refusal | **1** |

(the subset column is the one that matters: a net *modification* still trips the blob arm, so the
false clean is specifically the **restore** shape — the exact defect R44-CL10 was routed for.)

The subset case is the dangerous one: the `--require-pathspec` guard is satisfied, the `git log`
scope narrows to one file, the tamper+restore of `other.py` never enters `touched`, and the blob arm
sees the freeze bytes at REV — **exit 0 on a real post-freeze touch-and-restore**, which is exactly
the R44-CL10 defect the round claims to have closed. Two more instances of the same class on the
real frozen set: `--freeze-path plans/round-45-claims.md --pathspec tools/round-45/` exits 0 on a
restored claims file (a **file** freeze-path is never coverage-checked at all, because `tree_at` is
false for a blob), and the same narrowing kills `--check-dirty` for an uncovered path.

Fix, proved on a scratch copy only (`covers()` direction corrected to ancestor-or-equal; the frozen
file was never written):

| | shipped | patched |
|---|---|---|
| subset pathspec on a violated dir | 0 clean | **2 `pathspec_required`** |
| superset pathspec on the same dir | 2 refused | **1 violation reported** |
| selftest | 11 cases / 0 failures | **11 cases / 0 failures** |

**The last row is the finding to carry to round 46**: the correction is *invisible* to the 11-case
selftest. Any fix to `covers()` needs a case pair (subset → 2, superset → 1); the existing set
pins neither, which is why R45-CL15's "red cases are arm-covering but not arm-isolating" is visible
here as a concrete fixed-point. Receipt: `E-pathspec-covers.txt`.

---

## 3. The freeze arm is blind to merge resolutions — confirmed at full strength

Routed as R45-CL6 (HIGH), so this is corroboration with a harsher receipt, not a new claim.

I built an **evil merge** on a clone of the measured revision `f59565b7` (both parents unrelated to
the frozen paths, so no conflict): the merge commit's own resolution appends a line to the frozen
`tools/round-45/c1-counter.py`.

| check | value |
|---|---|
| appended line present in parent 1 | 0 |
| appended line present in parent 2 | 0 |
| appended line present in **the merge commit** | **1** |
| frozen blob at `f762b727` | `4ce400b29d6e…` |
| frozen blob at the merge | `4caa0f13baf5…` — **differs** |
| `git log --name-only` (the counters' form) | **prints nothing** |
| `git log -m --diff-merges=first-parent` (the preflight's form) | `tools/round-45/c1-counter.py` |
| `c1-counter.py --freeze f762b727 --rev <merge>` | **exit 0**, `met_target true`, `frozen_path_changed []` |
| `c2-counter.py` on the same rev | **exit 0**, `met_target true`, `frozen_path_changed []` |
| `frozen-path-preflight.py` on the same rev | exit **1**, `touched` names the file |

So both scores are `met_target true` on a revision whose frozen file differs from the freeze, with
the difference introduced by a commit neither parent contains. **The measured range is safe**:
`git rev-list --merges f762b727..1f4b27f8` is empty, and `f762b727..84cb9da5` is empty too, so no
score in this round ran over a merge. The claim's satisfiability is untouched; the instrument's
guarantee is weaker than the block-22 row implies, which block 22 (A2) now states. Receipts:
`A8-c2-evil-merge.txt`, `A9-c1-evil-merge.txt`.

---

## 4. The two source rows — identity holds; the `anchor` cell breaks a CORPUS requirement

### 4.1 What holds (measured, five fetches each, UTC-stamped)

| item | S140 `git-status` | S141 `git-diff-tree` |
|---|---|---|
| HTTP | 200 | 200 |
| bytes | 99,934 | 256,810 |
| sha256 | `903e31c5…59ad9` | `f81c1e31…c9640` |
| matches the row's `anchor` cell exactly | **yes** | **yes** |
| 5 fetches (incl. one 20 s later at 16:18:51Z) | **all byte-identical** | **all byte-identical** |
| quote verbatim in the fetched bytes (whitespace-normalized) | yes | yes |
| quote word count (elision marker excluded) | **21** (recorded 21) | **20** (recorded 20) |
| named anchors resolve in the HTML | `Porcelain Format Version 1` yes; `-z` machine-parsing paragraph yes | `-z` option yes; `Raw output format` heading yes |
| per-request nonce in the page (the S138 `github.com` defect class, CL12) | **0** | **0** |

So the two rows' page identity is stronger than the S138 class the round routed: these pages are
byte-stable across fetches, so a page sha256 **is** usable identity here, unlike a `github.com` HTML
page. This is a point in the row's favour that the round did not claim and could have.

### 4.2 What fails — the `anchor` cell carries no revision

`CORPUS.md:99-100` (verbatim): "`anchor` — exact section / heading / page / line **plus revision
(version, commit, or publication date)**. Never a bare homepage."

Both cells name sections and then give a **fetch stamp**:

- S140 anchor: `Page fetched 2026-10-28 (HTTP 200, 99,934 bytes, sha256 …); anchors \`Porcelain Format Version 1\` and the \`-z\` machine-parsing paragraph`
- S141 anchor: `Page fetched 2026-10-28 (HTTP 200, 256,810 bytes, sha256 …); anchors \`-z\` and the raw output format section`

A fetch date is not one of the three things the rule names (version, commit, publication date), and
a sha256 is a byte identity, not a revision. **The revision was available and was not recorded**:
both pages carry it in their own header — `last updated in 2.53.0` (git-status) and
`last updated in 2.56.0` (git-diff-tree). The lane's own precedent for the *same source host*
records it: S073's anchor reads "merge-base OPERATION MODES --is-ancestor, **last updated 2.43.0**;
cat-file … **last updated 2.56.0**", and S074 likewise. S140/S141 are the only two rows in this
source family that do not.

**Verdict: falsified (LOW/calibration), row-shape against `CORPUS.md:99`, not against the round-45
claim text** — the claims file predicates on page identity and located quotes, and both hold.

**Fix, and the constraint on it.** `anchor` is *not* one of the three in-place-editable columns, so
the row cannot be edited; under rule 2 the correction is a new row whose `teaches` opens
`supersedes S140 —`. The cheap honest alternative used elsewhere in this lane (the S138 precedent,
`corpus/lessons/round-45.md:36-46`) is to record the revision in the lesson's `## Gate` and let the
row stand: append `; last updated 2.53.0` / `; last updated 2.56.0` to the Gate's per-row entry. I
recommend the Gate route this round and a `supersedes S140/S141` pair only if round 46 wants the
registry itself to comply.

Receipt: `D-sources-fetch.txt`. No sibling report names the revision gap (grep over
`.ufo/waves/round-45/w2/*.md` for `2.53.0`/`2.56.0` returns nothing).

---

## 5. Record checks — one defect (repaired at HEAD), one still live, the rest hold

| # | record statement | measurement | verdict |
|---|---|---|---|
| R-1 | `SCORECARD.md` A3 paragraph: "the values are **identical** at `e715263c`, `1f4b27f8`, `fedd11bf` and A3" (was `:3593-3594` at `84cb9da5`) | `block22_refs` = **6 / 7 / 8 / 8** at those four revisions (`c1-counter.py` run four times; the four committed receipts agree: `c1-at-e715263c.json` 6, `…1f4b27f8` 7, `…A2` 8, `…A3` 8) | **falsified, then FIXED** — "the values" was false for `block22_refs`. The *preceding* A2 sentence (`:3583-3584`) had already been repaired by `e00b9f6b`; the A3 sentence had not. **At HEAD `99fdb9e4` it is repaired** and the repair is accurate: `rule_blocks`, `rows`, `unresolved` and `met_target` are identical at all four and `block22_refs` reads 6/7/8/8, credited to R45W2Immutable R-1. Exact fix I proposed and the one landed agree. |
| R-2 | `LOG.md` claim ledger: "refs **7/7** resolved" at `1f4b27f8` | `block22_refs 7`, `block22_unresolved_citations []` | **holds** |
| R-3 | `SCORECARD.md`: rows `139 → 141`; `W04` 14 at round start and end | strict parser 139/141; census `W04` = 14 both | **holds** |
| R-4 | `SCORECARD.md`: "14 W04 warnings" at round end | census prints 14 | **holds** |
| R-5 | block 22 row "FREEZE equals REV (empty range) \| **all arms** \| 0 \| verdict clean" | with `--check-dirty` and a dirty frozen file, `--freeze B --rev B` exits **1** (`dirty [' M tools/round-45/tool.py']`); exits 0 only without the dirty arm armed | **falsified as written (LOW)**; routed as R45-CL24(b) at `99fdb9e4`, but that item attributes the `no dirty file` clause to **this** row — the clause belongs to the other row (`no touch, no dirty file and every frozen blob equal …`, `SKILL.md:594` at HEAD), and `SKILL.md:595` reads only `FREEZE equals REV (empty range) \| all arms`. See §8. |
| R-6 | block 22 table exit column says `1` for a touched frozen path; the counters report `2` | preflight 1, both counters 2 on the same condition | **holds as disclosed** — block 22 (A2) states "The exit column is the gate's; a scoring counter reports the same condition as `2`" |
| R-7 | block 22 names a located citation set (`block22_refs 8`) | 8 matches, **7 line-located + 1 bare** (`plans/round-45-claims.md` with no `:line`); the claim's `>= 4` counts the bare one | **holds** against the claim (`>=4`, and the bare path does resolve); the count's shape is R45-CL13(b), already routed |
| R-8 | registry row for `tools/round-44/c1-run.sh` (corrected by A3): does not run the oracle, `--dry-run` exits 0 writing nothing | `grep -c oracle tools/round-44/c1-run.py` = 0; `--dry-run` exit 0, "DRY RUN: nothing was written.", `git status --porcelain corpus/evidence/` empty; bad flag → exit 2 | **holds at A3** |
| R-9 | the six registry rows' exit cells name `0`, `1`, `2`; c2-counter green | six rows, exact first cell, all exit cells carry the three codes; `c2-counter` exit 0 with `scope_size 6`, `unregistered []`, `thin []` at `1f4b27f8` and A3 | **holds** |
| R-10 | registry row for `tools/round-44/c1-counter.py`: `--selftest --pkg65 <rea-agents 6.5.0 root>` — 47 cases, green 2026-10-28 | plain `--selftest` (no `--pkg65`) → exit 0, `cases 47`, `failures []`; **`--pkg65` variant NOT RUN** — no rea-agents 6.5.0 package root is installed on this host (`find / -maxdepth 6 -path '*rea*' -name 6.5.0` empty), and a bogus root correctly exits 1 | **holds for the case count; the documented command's exact form is `not run` here** (`I-supplementary.txt`), reason: the pinned package root is absent on this host |
| R-11 | c2-counter detects a registered instrument that does not exist at `--rev` | deleted `tools/round-44/c2-counter.py` at a clone's head; SKILL row still names it; `c2-counter` → **exit 0, `met_target true`, `registered` all six** | **holds as routed R45-CL2** (the counter checks the row, not the tool), corroborated |

Receipts: `A4`, `A5`, `A6`, `A10`, `C-strict-parser.txt`, `F-gate-rowcount.txt`.

---

## 6. Verdict table for everything I attacked

| id | attack | expected by the record | measured | verdict |
|---|---|---|---|---|
| A-1 | `registry-immutable.sh` base→head, the assigned run | 0, silent | 0, empty stdout, sha256 `e3b0c442…` | **holds** |
| A-2 | same, base→tip (`0ee50aaf`, `84cb9da5`, `99fdb9e4`) | 0 | 0 at every tip; `corpus/SOURCES.md` sha256 `70be416d…` identical at `f59565b7`, `84cb9da5` and `99fdb9e4` | **holds** |
| A-3 | the gate's `1` column naming (fixtures) | names the changed column | 3/5/6/8/10 named correctly; 9/11/12 exempt | **holds** |
| A-4 | no surviving row changed outside status/recheck/used-by | true | 0 changed cells at all, 139 survivors | **holds (stronger than claimed)** |
| A-5 | only additions are S140/S141 | true | added `['S140','S141']`, removed none, order preserved | **holds** |
| A-6 | gate `0` implies a well-formed registry | not claimed | F-1/F-2/F-3: an extra cell, a 4-space indent, or a duplicate-document append all exit 0 | **not claimed; scope limit named** |
| B-1 | preflight `pathspec`/`restored`/`dirty` under a subset pathspec | 1 violation | **0 clean** | **falsified** (routed CL15/CL18; fix proved, invisible to the selftest) |
| B-2 | counters' freeze arm vs a merge resolution | 2 `frozen_path_changed` | **0 `met_target true`** | **falsified** (routed CL6; measured range has no merge, so no score is affected) |
| C-1 | S140/S141 page identity, quote, word counts, anchors | all hold | all hold, 5/5 fetches byte-identical | **holds** |
| C-2 | S140/S141 `anchor` carries a revision | CORPUS requires one | absent in both; available on the page (`2.53.0` / `2.56.0`) | **falsified** (LOW, row-shape) |
| D-1 | SCORECARD A3 "the values are identical at four revisions" | true | `block22_refs` 6/7/8/8 | **falsified** (LOW), repaired at `99fdb9e4` |
| D-2 | block 22 empty-range row "all arms → 0" | 0 | 1 with `--check-dirty` on a dirty worktree | **falsified as written** (LOW); routed as R45-CL24(b), but against the neighbouring row (§8) |
| D-3 | LOC/SCORECARD/census counts (7/7, 139→141, 14 W04) | true | true | **holds** |
| D-4 | `c1-run.sh` semantics (A3-corrected row) | as written | as written | **holds** |
| D-5 | round-44 `c1-counter.py` selftest command with `--pkg65` | 47 cases green | 47 green *without* the flag; the flag's form is not runnable here (no package root) | **holds in substance; `not run` for the documented form** |

**Not run, with reasons**: the `--pkg65` form of the round-44 c1-counter selftest (pinned package root
absent on this host, and I will not install a 6.5.0 REA tree to satisfy a self-test count); a
`git merge --squash` reproducer for R45-CL19 (already routed with its own receipt, and CL6's evidence
supersedes it for my purposes); anything requiring network beyond the two `git-scm.com` fetches the
source rows themselves name.

---

## 7. What round 46 should carry

1. **`covers()` direction, with the case pair** (B-1): subset → 2, exact/superset → 0/1. Without the
   two cases the fix is green on both the broken and the repaired instrument (measured).
2. **Union the log scope with `--freeze-path` at file level** (CL18): today a file freeze-path is
   never coverage-checked, so a restored claims file under a narrow pathspec reads clean.
3. **The commit arm must use `-m --diff-merges=first-parent` in the counters too** (CL6): the
   preflight already does, and it is the difference between seeing and not seeing an evil merge.
4. **A registry-schema line belongs beside the append-only gate**: the gate is a cell differ for
   columns 2–12; the census is the schema instrument (F-1). Say so in the SKILL row so a future seat
   does not read the `0` as stronger than it is.
5. **Record discipline**: D-1 (`SCORECARD.md` A3 "identical values") was repaired at
   `99fdb9e4` exactly as proposed; D-2 (the block-22 empty-range row) is routed as R45-CL24(b) but
   against the wrong row (`SKILL.md:595`, not the `:594` row whose trigger names `no dirty file`).
   A grep for "identical at" and for "all arms" across the record before closing would have caught
   both without a wave-2 seat.
6. **S140/S141 `anchor` revision** (§4.2): record `last updated 2.53.0` / `2.56.0` in the lesson Gate
   now; a `supersedes S140/S141` row pair only if the registry itself must comply.

---

## 8. Reconciling with the L1's dispositions at HEAD `99fdb9e4`

While I was writing, the L1 landed `99fdb9e4` = "correct the SCORECARD A3 'identical values'
sentence (block22_refs 6/7/8/8) after wave-2 R-1, and route R45-CL24". Three of my findings are
dispositioned there; two of the dispositions carry their own factual errors, which I record because
this wave exists to disagree with the record when the bytes disagree.

**(a) R-1 is fixed, and the landed fix is accurate.** The sentence now reads "`rule_blocks`, `rows`,
`unresolved` and `met_target` are identical at `e715263c`, `1f4b27f8`, `fedd11bf` and A3, while
`block22_refs` reads 6 / 7 / 8 / 8 as citations were added" (`SCORECARD.md:3593-3595`). That matches
my measurement exactly, and the credit line names this seat. Nothing further needed.

**(b) R45-CL24(b) misdescribes which row it fixes.** It says "the row's trigger already reads 'no
dirty file', so the literal trigger is consistent, the arm cell is ambiguous". But the phrase
`no dirty file` belongs to the *other* zero-row of the table — `SKILL.md:594` reads
`| no touch, no dirty file and every frozen blob equal | all arms | 0 | verdict clean |` — while the
row my R-5 attacked is `SKILL.md:595`, `| FREEZE equals REV (empty range) | all arms | 0 | verdict
clean |`, whose trigger names no worktree condition at all. Measured on a fixture at `99fdb9e4`'s
predecessor: `--freeze B --rev B` on a clean tree → 0; with one dirty frozen file → **1**,
`dirty [' M tools/round-45/tool.py']`. So the empty-range row is false as written, not merely
ambiguous, and the fix belongs to `:595` (qualify the arm as "all arms, given a clean worktree" or
drop the row and keep `:594`).

**(c) R45-CL24(c) states a page fact that is false.** It says "the pages carry no version marker".
Both pages do: their own header line is `Latest version ▾ git-status last updated in 2.53.0` and
`Latest version ▾ git-diff-tree last updated in 2.56.0` (receipt `D-sources-fetch.txt`, line
`page revision markers:`). That matters to the disposition: if no marker existed, the honest fix
would be a fetch stamp plus the note the item gives; because a marker exists, the `anchor` cells can
and should carry `last updated 2.53.0` / `2.56.0` — which is also what the sibling rows on the same
host (S073/S074) already do. The routed fix is therefore weaker than the defect requires, not wrong
in direction.

**(d) R45-CL24(d) matches my R-10 and needs no correction**: the plain `--selftest` is 47 cases green
and the `--pkg65` form cannot run here because no rea-agents 6.5.0 root is installed.

**Still unrouted at `99fdb9e4`: F-1, F-2 and F-3** — `grep -n "registry-immutable\|extra cell\|indented row\|NF!=13"
corpus/lessons/round-45.md` returns nothing. These are the append-only gate's scope limits (a 12th
cell, a 4-space-indented row, a duplicate-document append all exit 0), and they are the one part of
this seat's attack that no CL item covers. They do not falsify a claim; they mean a reader must not
treat the gate's `0` as stronger than a cell differ for columns 2–12.

## 9. Receipts in this directory

The single-run receipts (`A*`, `B-gate-legal-append`, `B-gate-extra-cell`, `G`) each carry a
`cmd:`, `exit:`, `stdout_sha256:` and `utc:` line, and their stdout is truncated to 2,000 bytes.
The six multi-run logs (`B-gate-matrix`, `C`, `D`, `E`, `F`, `INVOCATION`) carry a provenance header,
a `utc:` stamp where the run was stamped, and a captured exit code per row; they are not single
command/exit records and are not presented as such.

| file | what it records |
|---|---|
| `INVOCATION.txt` | every exact command line, both ranges, all controls |
| `A-gate-base-to-head.txt` | the assigned run (exit 0, empty stdout, empty-string sha256) |
| `A2-gate-base-to-tip.txt` | base → tip `0ee50aaf` (and the run against `84cb9da5` in `G`) |
| `A3-gate-selftest.txt` | `SELFTEST cases=5 pass=5 fail=0` |
| `A4-c1-measured.txt`, `A5-c2-measured.txt` | both counters at `1f4b27f8`, exit 0 `met_target true` |
| `A6-c1-at-A3.txt` | c1 at A3 (`block22_refs 8`) |
| `A7-preflight-selftest.txt` | `PREFLIGHT_SELFTEST: cases=11 failures=0` |
| `A8-c2-evil-merge.txt`, `A9-c1-evil-merge.txt` | both counters exit 0 `met_target true` on the evil merge |
| `A10-c2-deleted-tool.txt` | c2 green while a registered instrument is absent at `--rev` |
| `B-gate-matrix.txt` | the 12-fixture mutation matrix with columns and rule-2 verdicts |
| `B-gate-legal-append.txt`, `B-gate-extra-cell.txt` | the two fixture endpoints at the extremes |
| `C-strict-parser.txt` | the independent parser: 139/141, added S140/S141, 0 changed cells |
| `D-sources-fetch.txt` | 5 fetches per row, byte counts, sha256s, word counts, anchors, revisions |
| `E-pathspec-covers.txt` | `covers()` as shipped vs patched, the 2×2 pathspec matrix, both selftests |
| `F-gate-rowcount.txt` | rows the gate sees at four revisions + the gate blob at base and tip |
| `G-final-tip.txt` | the final run at `84cb9da5`, exit 0, plus the SOURCES byte comparison |
| `H-gate-columns.txt` | the 13-mutation column/allow-list capture (real stdout) + the real-corpus `E01` vs gate-0 pair |
| `I-supplementary.txt` | round-44 c1-counter 47-case selftest plus the `--pkg65` form's failure and the absent package root; the strict-parser-vs-indent-anchor check; the whitespace-only mutation |
