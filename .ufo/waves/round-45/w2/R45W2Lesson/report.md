# R45W2Lesson — adversarial falsification of `corpus/lessons/round-45.md`

Lane `kaidoku`, round 45, wave 2. Seat: lesson critic (read-only on the lane tree and the fleet repo;
all writes are this seat's dir and `/fast/scratch/hyaku/kaidoku-r45/R45W2Lesson`).

| input | value |
|---|---|
| freeze | `f762b7273e3f6ca3c710bb37d5de92a4a4417aec` |
| landing / amendment A1 | `e715263cb51b713c342ab992d527fe9d61d6f8ff` / `1f4b27f82353d6544dc0c8048b3cfdadd8525d12` |
| lane HEAD read | `0ee50aaff516571aa607769bbbdf19a3db90dfa5` |
| `corpus/lessons/round-45.md` sha256 | `7deab95a0934cad7902f0ac9c72072aeec3653ad44de45c1b40e1bc70cea49b5` |
| `plans/round-45-claims.md` sha256 | `56bacf3143e904ae1c9683c61f0d3f30900257c6fd90d38965d735c7c50b915e` |
| `tools/round-45/frozen-path-preflight.py` sha256 | `633ebc058f0ea5a7c6dec4a9d6287e062eecf497fb6da674a3898c7c7130523b` |
| frozen-path drift freeze→HEAD | `git diff --stat f762b727..HEAD -- tools/round-45 plans/round-45-claims.md` → empty, exit 0 |

Exit codes are read semantically: 0 met/clean, 1 not met/violation, 2 could-not-evaluate. A 2 is
never treated as a pass. Every mutation was made on a **copy** under `$S`; the frozen paths were
only read (`cat`, `sha256sum`, `git show`).

## Verdicts (one per attack)

| # | attack (what it falsifies) | verdict | one-line evidence |
|---|---|---|---|
| A1 | M45-1 fix cell: "deleting the dirty arm makes `red-dirty` return 0 and the selftest fails 1 of 11" | **holds** | copy without the `if check_dirty:` body → exit 1, `red-dirty` got 0, `cases=11 failures=1` (R2) |
| A2 | M45-1 fix cell: "deleting the pathspec check makes `red-dirfreeze-no-pathspec` return 0" | **holds** | copy without the `require_pathspec` block → exit 1, case got 0, `failures=1` (R3) |
| A3 | M45-1 fix cell lists `red-restored` among the red cases as evidence for the `restored` classifier | **falsified** | deleting the `restored` branch alone → exit 0, `cases=11 failures=0`, stdout **byte-identical** to the pristine selftest (same sha256 `9f03df65…`) (R10) |
| A4 | M45-1 evidence pointer: "the re-derived audit … in `.ufo/waves/round-45/w1/R45W1InhSweepEvidence/`" | **falsified** | directory absent; `r45-w1-results.json` says the seat "never spawned: host job-cap refusal … wave completed without it". The 432/8/stamp facts themselves are true (R7, R8) and live in other seats |
| A5 | M45-1 captured-by: "the lane's own commit helper never looked at the worktree" | **falsified as worded** (operation holds) | the lane commit helper *does* call `git status --porcelain --ignored -z -- <files>` (`scripts/hyaku/jj-lane.sh:721`), pathspec-limited; it never gated the frozen pathspec |
| A6 | M45-2 honest limit: "the only thing an instrument could check is that a Gate block exists per new row" | **stated, one clause falsified** | a refetch check is mechanical and this seat ran it: S140/S141 sha256 reproduced **exactly** (R4, R5) and both quotes resolved (R9) |
| A7 | M45-2 evidence pointers ("round-44 closure routing item 4"; "the claim is in `corpus/lessons/round-44.md` `## Gate`") | **falsified** | no artifact in the lane contains a numbered "closure routing item 4"; round-44 `## Gate` (lines 21–53) never says the listings are descendants, not the URL. The claim is at `corpus/lessons/round-44-verifier-spotcheck.md:155` and `.ufo/waves/round-44/w2/R44W2LessonGate.md:118` (§D3) |
| A8 | M45-2 fix: "the located quote is recorded" | **partial** | the S138Fix receipt's own verdict is "**none**" for a top-page quote that supports the row's scope; only the 9-word `<title>` is quotable, and the lesson's Gate cell records neither status/bytes/sha nor a quote |
| A9 | M45-2 correction: "the cell's claim is true as of 2026-10-28" | **partial** | the cell's stamped window is `11:10:29Z–11:12:37Z` (contents API); the fetch that makes it true is `15:39:00Z`, outside the cell's window and not named in the correction |
| A10 | M45-3 captured-by / fix columns | **low-severity non-conformance** | captured-by names the prompt requirement, not a capturer; fix is a routing + counterfactual. Its checkable parts hold: my reconstruction of `fx-a6` exits 0 `met_target:true` (R11), the stub is 4 lines, sha256 `76eb1773…` ≠ `633ebc05…` |
| A11 | Gate: every quote ≤25 words and resolves on refetch | **holds** | S140 21 words, S141 20 words; both exact substrings on pages refetched byte-identically (R4, R5, R9) |
| A12 | Gate: "Both rows are cited by the round's R45-C1 landing" | **holds** | `SKILL.md:586` cites S141 (commit arm), `SKILL.md:589` cites S140 (dirty arm) |
| A13 | Gate census and rows: 139 → 141 rows, 14 W04 at both ends, rows `mined`/A/`on-release`/used-by lesson | **holds (end measured)** | 139 at base `149133d4`, 141 at freeze and tip; census exit 0, exactly 14 W04, no S140/S141 line; each new URL occurs once (R6, R12) |
| A14 | Lesson's cited line ranges point at the content claimed | **holds** | `round-44.md:18` = M44-2 row with the 09:57:16/10:43:43 stamp pair; `:63` = R44-CL1; (claims file) `:88` = R44-CL10 append-then-restore; spotcheck `:89-92` = break-then-restore unimplemented (R13) |
| A15 | *(adjacent, landed bytes)* `SKILL.md:607` cites `corpus/lessons/round-45.md:12-17` for the operator/integrator placement limit | **falsified** | lines 12–17 are `## Mistakes` + header + M45-1/M45-2 rows; the placement limit is at **70–73** (`R45-CL1`). A resolving but off-topic citation — the class the round routed as R45-CL13(b) |
| A16 | *(same lesson)* R45-CL1: "the gate's `--check-dirty` arm catches the precursor (eight dirty files)" | **falsified as worded** | `--dirty-pathspec other.txt` with dirty `frozen/b.txt` → exit **0** `clean` (scope is *replaced*, not unioned). The same lesson discloses this in R45-CL15 but CL1's summary omits the qualifier (R14) |

Summary: **2 falsified evidence pointers** (A4, A7), **1 false evidence claim** (A3), **3
overclaims as worded** (A5, A6, A16), **3 precision gaps** (A8, A9, A10), **1 adjacent off-topic
citation in the graded surface** (A15). The two testable M45-1 deletion claims and every Gate quote
**hold exactly**.

## Detail

### A1/A2 — M45-1's two deletion claims are exact (holds)

Scratch copy of the frozen interpreter (`$S/pf.py`, sha256 `633ebc05…`, identical to the lane file),
`TMPDIR=$S`:

```sh
python3 -I -B $S/pf.py --selftest          # exit 0, PREFLIGHT_SELFTEST: cases=11 failures=0
```

Mutation "delete the dirty arm" = remove the whole `if check_dirty:` body, keep `dirty = []`
(the only deletion shape that leaves the module importable):

```sh
python3 -I -B $S/pf_nodirty.py --selftest  # exit 1
# {"expect": 1, "got": 0, "ok": false, "selftest": "red-dirty"}
# PREFLIGHT_SELFTEST: cases=11 failures=1
```

Mutation "delete the pathspec check" = remove the `if require_pathspec:` block:

```sh
python3 -I -B $S/pf_nopathspec.py --selftest  # exit 1
# {"expect": 2, "got": 0, "ok": false, "selftest": "red-dirfreeze-no-pathspec"}
# PREFLIGHT_SELFTEST: cases=11 failures=1
```

Both numbers in the lesson are right, including the "1 of 11". The only admissible caveat: deleting
the `dirty` *variable* (not the arm body) crashes all 11 cases with `NameError`; the claim is true
for the semantic deletion of the arm, which is the natural reading.

### A3 — `red-restored` does not bind the `restored` classifier (falsified)

Deleting only

```python
        elif any(t["path"] == path for t in touched):
            restored.append(path)
```

leaves `--selftest` at exit 0, `cases=11 failures=0`, and the **entire stdout is byte-identical to
the pristine run** (`9f03df6538de49b733ecc71415bbb192a30aa428b82953f4ea064342389ec06c`, R10). The
`touched` arm absorbs the kill, exactly as R45-CL15 states ("`restored` and `blob` have zero unique
detection"). The defect in the lesson is narrower than the instrument: the M45-1 row offers
`red-restored` inside its `--selftest` list as part of the "shown able to fail" evidence for a cell
that also claims "the `restored` classifier", without the CL15 qualifier. A reader of the row alone
would conclude all four named red cases are arm-binding; two of them are not.

Smallest correction: in M45-1's fix cell, mark `red-restored`/`red-restored`'s evidence as
"arm-coverage only — zero unique detection (R45-CL15)", or delete it from the "shown able to fail"
clause.

### A4 — M45-1's evidence directory does not exist (falsified provenance)

```
ls .ufo/waves/round-45/w1/R45W1InhSweepEvidence/   → No such file or directory
```

`.ufo/waves/round-45/r45-w1-results.json` records the seat as:

> "note": "never spawned: host job-cap refusal during wave fill; wave completed without it
> (partial-fill loss recorded by L1)"

The lesson therefore attributes the re-derived audit to an artifact that was never produced. The
**facts** in that clause are true and I re-derived them myself (R7/R8):

```sh
git show --name-only --format= c86ea508 | grep -c .                          # 432
git show --name-only --format= c86ea508 | grep -c tools/round-44/control-fixtures/  # 8
git show -s --format='%ad | %cd' --date=iso c86ea508
# 2026-10-28 09:57:16 -0300 | 2026-10-28 10:43:43 -0300
```

and two seats that did run carry the audit:
`.ufo/waves/round-45/w1/R45W1PreflightDirtyReplay.md:286-289` (F-10: 432, eight fixtures, exactly
one touching commit) and `.ufo/waves/round-45/w1/R45W1PreflightReplay.md:75-76`.

Smallest correction: replace the pointer with `R45W1PreflightDirtyReplay.md` §F-10 (and
`R45W1PreflightReplay.md` §"…432 paths") — the facts are sound, only the provenance is false. This
is the exact failure class the lesson itself names in M45-3 and R45-CL12: a claim whose *citation*
does not resolve is not repaired by the claim being true.

### A5 — "the lane's own commit helper never looked at the worktree" (overbroad)

`scripts/hyaku/jj-lane.sh` (`cmd_commit`, defined at :598) filters the worktree over the paths it is
about to commit:

```sh
left=$(git status --porcelain --ignored -z -- "${files[@]}" ...)   # :721
```

so it does look at the worktree — for the requested paths only, and only to drop ignored/untracked
entries. It never consults the frozen pathspec, which is why the eight swept files were invisible
to it. The operationally important half of the claim holds; the literal half does not. Correct
wording: "the lane's commit helper is pathspec-limited (`jj-lane.sh:721`) and nothing gated the
frozen pathspec."

Not verified: the helper's content *at round 44* (the fleet repo is outside this seat's writable
tree and I did not date the line); the statement above is about the helper as read at tip.

### A6 — M45-2's honest limit is stated, but its impossibility clause is false (falsified clause)

The row does the right thing structurally: it labels the limit "Honest limit: this fix cannot fail
mechanically — it is a receipt discipline … Recorded here rather than claimed." That is disclosure,
not hiding (question 2 answered **yes**). But the second half — "the only thing an instrument could
check is that a Gate block exists per new row" — is refuted by this seat's own two-command check:

| check | result |
|---|---|
| `curl -sS -o s140.html -w '%{http_code} %{size_download}' https://git-scm.com/docs/git-status` | `200 99934`, sha256 `903e31c5…` = the Gate's recorded value, **exactly** |
| same for S141 | `200 256810`, sha256 `f81c1e31…` = recorded, **exactly** |
| quote substrings on the tag-stripped pages | S140 both fragments present; S141 exact sentence present |

So an instrument can check, mechanically: HTTP status, byte count, page sha256 (for static pages),
quote presence, and word count ≤25. What it cannot check is whether the *author read* the page — the
honest limit is "no instrument is written this round", not "no instrument could exist". The lesson's
own R45-CL12 already explains why the sha step must be skipped for a `github.com` HTML page
(667-byte drift between fetches); that nuance is exactly the kind of thing a future checker can
encode, and it makes the flat "cannot fail mechanically" a calibration defect.

Smallest correction: replace with "no checker exists this round; this seat demonstrated that a
refetch compares HTTP status, bytes and sha256 exactly for both static pages, and quote presence
mechanically — an HTML page (S138) is the one case where the digest must be replaced by the quote."

### A7 — both halves of M45-2's evidence pointer miss (falsified)

1. "round-44 closure routing item 4" — the string "closure routing" occurs in exactly one file in
   the lane (`corpus/lessons/round-45.md` itself); round 44's routed list is bulleted `R44-CL1…`
   (`corpus/lessons/round-44.md:55-92`), and its wave-2 reports contain no numbered "routing item
   4". The pointer names nothing a reader can open.
2. "the claim is in `corpus/lessons/round-44.md` `## Gate`" — that Gate (lines 21–53) contains the
   S138 row with "contents API, 10 listings + 22 members" (line 27) but never states that the
   listings are descendants of the row URL rather than the URL. The claim lives at
   `corpus/lessons/round-44-verifier-spotcheck.md:155` ("S138 'opened' cell = descendant-listing
   replay (top URL never fetched by the lane)") and at
   `.ufo/waves/round-44/w2/R44W2LessonGate.md:118` (§D3, same sentence as a finding).

Smallest correction: cite those two, not the round-44 Gate table.

### A8/A9 — M45-2's fix and correction overstate what was recorded

- The fix cell says "the located quote is recorded". The S138Fix receipt's §3 heading is
  "A located quote from the TOP page that supports the row's scope — verdict: **none**", and §4 is
  "Does the row's stated quote live on the top page? **No**". What is recorded is the page `<title>`
  (9 words), which supports only the subject. The lesson should carry the verdict word "none" or it
  repeats, in miniature, the over-credit M45-2 describes.
- The correction says the cell's claim is "true as of 2026-10-28 and false as of
  2026-10-28T11:12Z". The cell's stamped window is `11:10:29Z–11:12:37Z` over the **contents API**;
  the top-URL fetch is `15:39:00Z` (receipt R1) — a different endpoint and a different time. The
  row-level reading ("this row was opened this round") is now true; the cell-level reading is not,
  and the correction does not name the 15:39 fetch time it relies on. Add the timestamp; the
  strongest available precision is one clause.

### A10 — M45-3: captured-by is not a capturer; the fix is a counterfactual (low)

- The table has **three** `## Mistakes` rows, not two (the prompt's "both" undercounts). M45-1 and
  M45-2 each fill captured-by with a "none" **and** the blind spot that made capture impossible —
  conforming. M45-3's captured-by cell reads "prompt §9 requires 'the cheapest control that skips
  the claimed work'; this round read that as a do-nothing control only…" — that is the moment of
  non-capture, not who captured it. The actual capturers are in the evidence column
  (`R45W1CritC1`/`R45W1CritC2`).
- The checkable half of the fix holds: a reconstruction with the critic's own components (21 plain
  bullets, 8 garbage rows, four `:1` refs, the 4-line stub) scores exit **0**, `met_target: true`
  today (R11); the stub is 4 lines and its sha256 `76eb1773…` differs from the frozen
  interpreter's `633ebc05…`, so the pinned-sha counterfactual's premise is sound. But the column
  header promises "fix (shown able to fail)": a rule that does not exist cannot be shown, so the
  honest label is "not shown; premise verified; rule routed as R45-CL13".
- The critic's alternative (require the seven named red cases with `"ok": true`) is already
  mechanically decidable with the stub in hand: the stub's `--selftest` emits **zero** case lines
  (`grep -c '"selftest":'` = 0), so that rule would fail it without inventing a sha pin. Suggest
  citing that instead.

### A11 — Gate quotes (holds)

| row | words | ≤25 | resolves on refetch |
|---|---|---|---|
| S140 | 21 (elision excluded, as the cell says) | yes | both fragments found in the `Porcelain Format Version 1` section; page sha `903e31c5…` reproduced byte-for-byte |
| S141 | 20 | yes | exact sentence found in the `-z` option paragraph; page sha `f81c1e31…` reproduced byte-for-byte |

The S140 elision replaces "This makes it" — a neutral connector, no qualifier dropped. No other
quote cells exist in this round's Gate table. (The frozen claims file's own gloss — "the commit arm
parses that [`-z` output]" — is false at tip because the arm passes no `-z`; the **lesson** already
discloses this in R45-CL11, and its Gate wording is careful, so this is a note, not a new defect.)

### A12/A13 — Gate's "cited by the landing", census, registry rows (hold)

- `SKILL.md:586` "commit (`git log --name-status`, S141)"; `SKILL.md:589` "dirty (`git status
  --porcelain -z`, S140)". The source rows exist for exactly those arms.
- Row census with the lesson's own command: **139** at base `149133d4`, **141** at freeze and at
  tip. `sources-census.sh validate --root … kaidoku` → exit **0**, `kaidoku<TAB>ok<TAB><path>`,
  exactly **14** `W04` lines and **0** lines naming S140/S141; each new URL occurs once in
  `corpus/SOURCES.md`. Row cells: status `mined`, tier `A`, opened `2026-10-28`, recheck
  `on-release`, used-by `corpus/lessons/round-45.md` — as the lesson states.
- Not measured: the **round-start** 14 (would need the base tree materialised; the row count at
  base and the end-state 14 are measured, and the lesson's own correction says the start was also
  14).

### A14 — cited line ranges (hold; attribution note)

The **lesson** cites only `corpus/lessons/round-44.md:18` and `:63`; both point at the claimed
content (M44-2 row with the stamp pair; R44-CL1). The `:88` and `…-verifier-spotcheck.md:89-92`
ranges are cited by the frozen claims file (`plans/round-45-claims.md:35,37`), not by the lesson;
both also point at the claimed content (R44-CL10's append-then-restore sentence; the
"a later restore does not un-block is unimplemented" finding). Note the spotcheck range is a
superset: `:91-92` continue into R44-CL7/CL9 — acceptable for a `first-last` range, worth knowing.

### A15 — an off-topic citation in the graded block (adjacent finding, falsified)

`SKILL.md:607` ends "… so it stays an operator/integrator request and the report says so
(`corpus/lessons/round-45.md:12-17`)." Lines 12–17 of the lesson are `## Mistakes`, the table
header, and the M45-1/M45-2 rows. The operator/integrator statement is at **70–73** (`R45-CL1`).
The citation resolves by the frozen counter's regex (file + line range exist) and therefore
demonstrates in the landed bytes the exact class R45-CL13(b) routed: "the regex validates path+line,
not topicality". Fix: `:70-73`. (This is C1 surface, reported here because it is a claim about the
lesson's own line numbering and it falsifies a citation the lesson's reader is sent to.)

### A16 — R45-CL1's dirty-arm sentence is unconditional where the instrument is conditional
### (falsified as worded)

The lesson, lines 74–76: "the gate's `--check-dirty` arm catches the precursor (eight dirty files)
before a sweep exists." Reproducer on a scratch fixture (`frozen/a.txt`, `frozen/b.txt` at freeze;
`other.txt`; `frozen/b.txt` then dirtied):

| input | exit | verdict | `dirty[]` |
|---|---|---|---|
| `--check-dirty` (no `--dirty-pathspec`) | 1 | `frozen_path_changed` | `[" M frozen/b.txt"]` |
| `--check-dirty --dirty-pathspec other.txt` | **0** | **`clean`** | `[]` |
| both files dirty + `--dirty-pathspec other.txt` | 1 | `frozen_path_changed` | `[" M other.txt"]` |

`evaluate()` does `scope_paths = dirty_pathspecs or pathspecs` — replacement, not union. The same
lesson discloses this in R45-CL15 ("a **false-clean** under `--dirty-pathspec`"); R45-CL1's summary
sentence does not carry the qualifier, so the lesson contains a true statement and an unqualified
one that a supported invocation falsifies. (Round 44's defect shape used no `--dirty-pathspec`, so
the *historical* claim is unaffected — this is a wording/qualifier defect, not a re-litigation of
the landing.)

## Receipts

`TMPDIR=/fast/scratch/hyaku/kaidoku-r45/R45W2Lesson` for every run; lane root
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`; all fixtures created with
`git init -q` under `$S` and `rev-parse --show-toplevel` asserted equal to the fixture before the
first commit (true for `fx-a6-repro`, printed; true for `fx-false-clean`, `assert`ed in the driver).

| id | command (abridged) | exit | stdout sha256 | UTC |
|---|---|---|---|---|
| R1 | `python3 -I -B $S/pf.py --selftest` | 0 | `9f03df6538de49b733ecc71415bbb192a30aa428b82953f4ea064342389ec06c` | 2026-10-28T16:04:48Z |
| R2 | `… $S/pf_nodirty.py --selftest` | 1 | `cc07ca8a2129088f866af8c2f53c1349de92febe3942f96606ccf426938ea33e` | 2026-10-28T16:04:48Z |
| R3 | `… $S/pf_nopathspec.py --selftest` | 1 | `0c12452781ff284dba51edfe79693f4bf1dacae34a4c04a3d7cd5345d1ddd6a4` | 2026-10-28T16:04:48Z |
| R4 | `curl -sS -o s140.html -w '%{http_code} %{size_download}' https://git-scm.com/docs/git-status` | 0 | page `903e31c527d443ab4051f7b4e0225058efd96a45d0400538f6ba19b5c9c59ad9`, `200 99934` | 2026-10-28T16:04:48Z |
| R5 | same for `…/git-diff-tree` | 0 | page `f81c1e3141b2e8e2cfc5790b8923881862f964ae5e3f85c157299b71f80c9640`, `200 256810` | 2026-10-28T16:04:49Z |
| R6 | `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` | 0 | `9f32a8a84ef13933a0539a92a4475534aeb2ae858a407d35b176aa26662acf19` (14 W04) | 2026-10-28T16:04:49Z |
| R7 | `git show --name-only --format= c86ea508` | 0 | `3194620b4c784779…` (432 paths, 8 fixtures) | 2026-10-28T16:04:49Z |
| R8 | `git show -s --format='%ad \| %cd' --date=iso c86ea508` | 0 | `c8824574b93350bf…` | 2026-10-28T16:04:49Z |
| R9 | tag-strip + `in` tests + word counts on R4/R5 pages | — | S140 q1/q2 both true, S141 exact true, 21/20 words | 2026-10-28T16:04:49Z |
| R10 | delete `restored` branch on a copy, `--selftest` | 0 | `9f03df65…` (**byte-identical to R1**) | 2026-10-28T16:06:11Z |
| R11 | frozen `c1-counter.py --root $S/fx-a6-repro --freeze/--rev <fixture>` | 0 | `06c78c60199f8bd8196dfb00527eec8f4891c9dba201408c9eec7e361d0c93a2`, `met_target: true` | 2026-10-28T16:04:55Z |
| R12 | row census: `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}'` at `149133d4` and at tip | 0 | 139 / 141 | 2026-10-28T16:04:49Z |
| R13 | `awk` of `round-44.md:18,63,88` and `…spotcheck.md:89,92` | 0 | quoted in A14 | 2026-10-28T16:04:49Z |
| R14 | preflight on dirty fixture, three flag shapes | 1 / **0** / 1 | verdicts in A16 table | 2026-10-28T16:05:13Z |

Artifacts copied into this seat's dir: `receipts.json`, `pf_nodirty.py`, `pf_nopathspec.py`,
`pf_norestored.py`, `pf_*.out`, `s140.html`, `s141.html`, `census.out`, `fx-a6-repro.json`,
`fx-a6-SKILL.md`, `stub.py`, `fx-false-clean/`.

## Not run (and why)

- **A13 round-start W04 = 14**: the census reads a worktree; the base tree is not checked out here
  and materialising it is a checkout operation this seat may not perform. End-state 14 and the base
  row count 139 are measured.
- **Byte-identical rebuild of the critic's `fx-a6`**: the critic's scratch is gone; my reconstruction
  uses the same components but is 40 SKILL lines vs the report's 44, so it reproduces the **verdict**
  (exit 0) and not the receipt hash `34336cf7…`. Stated rather than papered over.
- **S138 top-URL refetch**: outside this seat's four questions; the S138Fix receipt already records
  200 / 238,102 B / 15:39:00Z and its own negative verdict on a scope quote, which is what A8/A9
  rest on.
- **Merge-introduced freeze touch** (R45-CL6), **the fleet helper's round-44 bytes** (A5), and the
  counters' own predicates: other seats own them; no lesson claim in scope depends on them.
- **`tools/sources-census.sh` URL-open checking**: not executed as a mutation; the script's E-code
  set (E07 status enum, E08 opened date) contains no endpoint-identity check, consistent with the
  lesson's claim.

## Cleanup

`$S` was removed after the artifacts above were copied. No writes to `SKILL.md`, `plans/`, `tools/`,
`corpus/`, `LOG.md`, `SCORECARD.md`, `.ufo/state/`, or any sibling lane; no git/jj mutation; no
installs (pacman paused; nothing needed).
