# EX-36 — SKILL.md registry-row patch text: `custody-pair` (third registry row)

Seat EX-36 · chain c3 · role executor · wave arc3-loop1-round2 · 2026-10-19.
Target: `SKILL.md` — the "Local round-evidence gate registry" table (third row,
appended after the `citation-drift` row at `:371`) plus the registry preamble
(`:364-366`, rewritten line-neutral, 3→3 lines). **NOT APPLIED by this seat** —
patch text only, per the wave's seat discipline (no seat but the designated
implementer writes a real target, and SKILL.md is not this chain's target).

Base revision: `14b1682b1128d2e41085ebc79c9addeb8786d420` (HEAD; repo SKILL.md
byte-identical to HEAD, sha256 `483b0eba27458c138fdbe760d83a33f0da54b251ec028f033d83a5ae3d0175eb`).
Instrument the row is verified against: `.ufo/gates/custody-pair/custody-pair.py`
sha256 `112d01dc034c2d54324e7703e2d03d1d83b0c3930ed5d4f688546968b73ecefa`
(889 lines) + EX-31's `README.md` (its own usage/exit documentation). EX-31
revised the tool mid-seat (`9aad4c5a…`/38917 B → `4862f642…`/38651 B/12 cases →
`112d01dc…`/889 lines/15 cases); every number below is measured on `112d01dc…`,
sha-bracketed before and after the runs (`evidence/sha-bracket.txt`). Corroborated
by `seats/EX-31.md` §1 (same sha) and `seats/EX-35.md` §1.

Seat-line deviation (named): the seat line said "self-invocation = `--selftest`".
The landed interface has no `--selftest` flag — self-invocation is the
`selftest` **subcommand** (`--help`: `capture | verify | selftest | paths`). The
row spells it as the code does.

## 1. Why the row must exist

C3's frozen claim (`claims-frozen.md:57-64`) lands `.ufo/gates/custody-pair/` as
a committed verdict instrument (v2 custody receipts over the five operator
paths). The registry (`SKILL.md:361-371`) declares two scripts, and its preamble
enumerates two — "the interactive-r1 recovery gate and the citation-drift probe
… Neither validates REA correctness …". With a third instrument registered,
"Neither" is false; a third instrument without a row is unregistered. Round-1
precedent for registry-row patch text: `arc3-loop1-round1/claims/c2/EX-20/registry-row.patch.md`.

## 2. The patch (primary) — unified diff against HEAD

Apply from the repo root: `patch -p1 < registry-row.diff` (or `git apply`).
Verified on a copy: `patch -p1` → rc 0, result byte-identical to the intended
file. Line effect: 371 → 372 lines (preamble 3→3 lines, row appended at `:372`).

Patched file sha256 `2ff458dd7083b7086bbc08940f508a6cdbd01caf4557c2312bced81213cd028a`;
diff sha256 `db652720ce35fc0f6d80ae4d3cb0e859718072ed5f0766feb9b46b7a34d99c81`.

```diff
--- a/SKILL.md
+++ b/SKILL.md
@@ -361,11 +361,12 @@
 ## Local round-evidence gate registry
 
 The rows below are this lane's registered verdict scripts: the interactive-r1
-recovery gate and the citation-drift probe. Neither validates REA correctness,
-outside review, canonical judgment, or fleet acceptance. Evidence and limits:
-`corpus/lessons/2026-10-15-round-1-recovery.md`; `LOG.md`, Interactive round-1 recovery.
+recovery gate, the citation-drift probe, and the custody-pair tool — none of
+them validates REA correctness, outside review, canonical judgment, or fleet
+acceptance. Evidence and limits: `corpus/lessons/2026-10-15-round-1-recovery.md`; `LOG.md`, Interactive round-1 recovery.
 
 | Name | Kind / owner | Entry / verdict map | Self-invocation | Pinned values / write scope |
 |---|---|---|---|---|
 | interactive-r1-recovery | gate / kaidoku | `python3 .ufo/rounds/interactive-r1/verify-recovery.py`; 0 clean, 1 failed, 2 could-not-evaluate; `--admission` checks this recovery's unresolved prerequisites and returns 2, never native judgment | same command with `--selftest`; asserts isolated subprocess exit codes and stable finding IDs | `.ufo/rounds/interactive-r1/expected.json` pins every snapshot input and expected outcome; normal entry read-only in this repo; selftest creates and removes only its isolated fixture directory under `.ufo/rounds/interactive-r1/` |
 | citation-drift | probe / kaidoku | `python3 .ufo/gates/citation-drift/citation-drift-probe.py --root . --rev <REV> --table .ufo/gates/citation-drift/pointer-table.json --expected .ufo/gates/citation-drift/expected.json`; **probe semantics: 0 reported (drift is reported, never failed) and 2 could-not-evaluate; `--strict` restores the gate map 0 clean / 1 failed / 2 could-not-evaluate**; **frozen-run preflight: the table's sha256 must match the digest pinned in `expected.json` — a tampered table (exit 2, finding `pointer_table_tampered`) or an absent table (exit 2, finding `pointer_table_unreadable`) is could-not-evaluate before any entry is graded; a baseline that pins no digest is exit 2, finding `pointer_table_unpinned`; drift reporting is unchanged (rc 0)** | same command with `--selftest`; 13 isolated-fixture cases asserting exit code and a stable finding id (the eleventh is dead/absent `--rev` → exit 2, finding `revision_unresolvable`; the twelfth is a tampered table → exit 2, finding `pointer_table_tampered`; the thirteenth is an absent table → exit 2, finding `pointer_table_unreadable`), the case table committed in `expected.json` rather than in the script | `.ufo/gates/citation-drift/pointer-table.json` pins every in-repo citation and `expected.json` pins the self-test case table **and the sha256 of `pointer-table.json` (frozen-run guard; any edit to the table must re-pin the digest in the same commit)**; normal entry read-only over the tree it grades; selftest writes only isolated temp fixture repos; **no line number into an operator-mutable file is pinned** (rule #11) |
+| custody-pair | tool / kaidoku | `python3 .ufo/gates/custody-pair/custody-pair.py capture --out <receipt> [--label <L>]` — read-only sha256+stat over the five operator paths → a v2 receipt (SHA256; MTIME_EPOCH/NS with MTIME_UTC_RENDER and MTIME_LOCAL_RENDER labeled separately — the v1 local-under-`MTIME_UTC` defect gone; CTIME_EPOCH/NS; INODE; MODE/UID/GID; the receipt self-pins the instrument's sha256 and receipt-version 2) + a `.sha256` sidecar; `paths` prints the canonical five; `verify <receipt_a> <receipt_b>` or `verify <receipt_a> --live` — **worst-finding map: 0 MATCH, 10 CONTENT-DRIFT (sha256 moved), 11 REWRITE-DRIFT (sha256 equal, inode/ctime/mtime moved — a same-content rewrite), 12 METADATA-DRIFT (mode/uid/gid/size/type, extra path, inconsistent epoch/render, reproduced v1 LABEL-DEFECT), 13 ABSENT; 2 USAGE (bad args, unreadable or unparsable receipt, refused write); precedence CONTENT-DRIFT > ABSENT > REWRITE-DRIFT > METADATA-DRIFT > MATCH; capture is 0 at 5/5, else 13 with the receipt still written, and it refuses to write a receipt over a custody path; v1 receipts still compare on their sha256 — a sums-form v1 reads MATCH-V1-PARTIAL exit 0, a v1 stanza reproducing the round-1 label defect reads METADATA-DRIFT/LABEL-DEFECT exit 12 with its sha256 contract intact (5/5)** | same command with `selftest`; 15 fixture cases — capture/receipt shape/sidecar self-hash, verify-vs-live clean, the two same-content-rewrite pins (in-place ctime, rename inode) → 11, content → 10, absent → 13, metadata → 12, TZ-independent UTC render, the three v1 parse shapes, unparsable → 2, refuse-to-write-over-custody-path → 2; scratch root `$CUSTODY_PAIR_SCRATCH` else `/dev/shm` else `/var/tmp` (`/tmp` never — EDQUOT hazard); exit 3 if any case fails, 0 clean | the five path identities are pinned in the instrument (`CUSTODY_PATHS`, fixed order, printed by `paths`); **normal entry writes nothing under the custody paths — files opened for reading only, never renamed, mtime never touched; writes only the requested receipt + its `.sha256` sidecar (outside the custody set) and, under `selftest`, its isolated fixture root; `--paths` exists for fixture runs only** |
```

The appended row on its own (line 372; row sha256
`f4ff2f4c46325c7081fc370e5de1468a452f907e033aaf89b14cc4e9f52b47f2`, 6 pipes = 5 cells):

```markdown
| custody-pair | tool / kaidoku | `python3 .ufo/gates/custody-pair/custody-pair.py capture --out <receipt> [--label <L>]` — read-only sha256+stat over the five operator paths → a v2 receipt (SHA256; MTIME_EPOCH/NS with MTIME_UTC_RENDER and MTIME_LOCAL_RENDER labeled separately — the v1 local-under-`MTIME_UTC` defect gone; CTIME_EPOCH/NS; INODE; MODE/UID/GID; the receipt self-pins the instrument's sha256 and receipt-version 2) + a `.sha256` sidecar; `paths` prints the canonical five; `verify <receipt_a> <receipt_b>` or `verify <receipt_a> --live` — **worst-finding map: 0 MATCH, 10 CONTENT-DRIFT (sha256 moved), 11 REWRITE-DRIFT (sha256 equal, inode/ctime/mtime moved — a same-content rewrite), 12 METADATA-DRIFT (mode/uid/gid/size/type, extra path, inconsistent epoch/render, reproduced v1 LABEL-DEFECT), 13 ABSENT; 2 USAGE (bad args, unreadable or unparsable receipt, refused write); precedence CONTENT-DRIFT > ABSENT > REWRITE-DRIFT > METADATA-DRIFT > MATCH; capture is 0 at 5/5, else 13 with the receipt still written, and it refuses to write a receipt over a custody path; v1 receipts still compare on their sha256 — a sums-form v1 reads MATCH-V1-PARTIAL exit 0, a v1 stanza reproducing the round-1 label defect reads METADATA-DRIFT/LABEL-DEFECT exit 12 with its sha256 contract intact (5/5)** | same command with `selftest`; 15 fixture cases — capture/receipt shape/sidecar self-hash, verify-vs-live clean, the two same-content-rewrite pins (in-place ctime, rename inode) → 11, content → 10, absent → 13, metadata → 12, TZ-independent UTC render, the three v1 parse shapes, unparsable → 2, refuse-to-write-over-custody-path → 2; scratch root `$CUSTODY_PAIR_SCRATCH` else `/dev/shm` else `/var/tmp` (`/tmp` never — EDQUOT hazard); exit 3 if any case fails, 0 clean | the five path identities are pinned in the instrument (`CUSTODY_PATHS`, fixed order, printed by `paths`); **normal entry writes nothing under the custody paths — files opened for reading only, never renamed, mtime never touched; writes only the requested receipt + its `.sha256` sidecar (outside the custody set) and, under `selftest`, its isolated fixture root; `--paths` exists for fixture runs only** |
```

## 3. Required semantics → row clause (traceability)

| requirement | row clause | measured? |
|---|---|---|
| kind tool / kaidoku | cell 2: `tool / kaidoku` | n/a (registration) |
| entry / verdict map | `capture --out <receipt> [--label <L>]`; `verify <a> <b>` or `verify <a> --live`; `paths`; worst-finding map 0/10/11/12/13 + 2 USAGE, precedence, `capture` 0 at 5/5 else 13 (receipt still written), refuse-to-write-over-a-custody-path | §4: MATCH exit 0 (pair + live), REWRITE-DRIFT exit 11, CONTENT/METADATA classes read from `custody-pair.py:59-78` (docstring) and `:119-143` (constants), corroborated by EX-31 README exit table and `seats/EX-31.md` §3 |
| self-invocation | `selftest`; 15 fixture cases, one per exit class; scratch `$CUSTODY_PAIR_SCRATCH` else `/dev/shm` else `/var/tmp` (`/tmp` never); exit 3 if any fails, 0 clean | §4: `CLEAN cases=15 passed=15 failed=0 exit=0` on the pinned sha; exit-3 branch code-read (`custody-pair.py:827-828`), not fired |
| pinned values | five path identities (`CUSTODY_PATHS`, fixed order, printed by `paths`); every receipt self-pins the instrument's sha256 + receipt-version 2 | §4: `paths` rc 0 (5 lines); receipt header `# tool: … sha256 112d01dc…`, `# receipt-version: 2`; `.sha256` sidecar = receipt's own digest |
| write scope — READ-ONLY over custody paths | opened for reading only, never renamed, mtime never touched; writes only the requested receipt + `.sha256` sidecar (outside the custody set); `--paths` for fixture runs only | §4: the five paths' sha256 byte-identical before/after every run (pre/post evidence files); refusal measured by selftest case `refuses-to-write-over-custody-path` |
| C3 claim's "v1 receipts remain verifiable against the tool's sha256 fields" | "v1 receipts still compare on their sha256 — a sums-form v1 reads `MATCH-V1-PARTIAL` exit 0, a v1 stanza reproducing the round-1 label defect reads `METADATA-DRIFT`/`LABEL-DEFECT` exit 12 with its sha256 contract intact (5/5)" | §4 both shapes; matches EX-35 §3's measured caveat (live-mode exit 12 from the reproduced defect) |

## 4. Verification evidence (commands run against the real instrument; custody read-only)

```
$ python3 .ufo/gates/custody-pair/custody-pair.py capture --out /var/tmp/ex36/v2tool/pre.txt --label ex36-rev2-pre    → rc 0, OK paths=5/5
$ python3 .ufo/gates/custody-pair/custody-pair.py capture --out /var/tmp/ex36/v2tool/post.txt --label ex36-rev2-post  → rc 0, OK paths=5/5
$ python3 .ufo/gates/custody-pair/custody-pair.py verify pre.txt post.txt → VERDICT: MATCH paths=5 exit=0            (evidence/verify-pair.out)
$ python3 .ufo/gates/custody-pair/custody-pair.py verify pre.txt --live   → VERDICT: MATCH paths=5 exit=0            (evidence/verify-live.out)
$ python3 .ufo/gates/custody-pair/custody-pair.py selftest --scratch /var/tmp/ex36/selftest → CLEAN cases=15 passed=15 failed=0 exit=0 (evidence/selftest.out)
$ python3 .ufo/gates/custody-pair/custody-pair.py paths → rc 0, the canonical five, fixed order                                 (evidence/paths.out)
$ python3 .ufo/gates/custody-pair/custody-pair.py verify <scratch sums-v1 receipt> --live → MATCH-V1-PARTIAL exit=0            (evidence/verify-sums-live.out)
$ python3 .ufo/gates/custody-pair/custody-pair.py verify <round-1 CU-1 stanza-v1 receipt> --live
    → METADATA-DRIFT exit=12, 5× LABEL-DEFECT, SHA256-CONTRACT: 5/5 agree                                                      (evidence/verify-v1stanza-live.out)
# scratch-only same-content rewrite (os.replace identical bytes, sha unchanged)
$ … verify fx/pre.txt fx/post.txt → VERDICT: REWRITE-DRIFT paths=1 moved=inode,mtime_ns exit=11                               (evidence/verify-rewrite.out)
```

Read-only proof: `sha256sum` of the five custody paths identical before and
after the whole run set (`evidence/custody-pre.txt` == `evidence/custody-post2.txt`).

Collateral (does the row edit break anything that reads SKILL.md?):
scratch clone of the repo at `14b1682` + the patch committed (`8649f3a0…`) —

```
$ citation-drift-probe.py --root . --rev 8649f3a0…             → reported findings=0 exit=0   (evidence/clone-probe-sim.out)
$ citation-drift-probe.py --root . --rev 8649f3a0… --strict    → clean findings=0 exit=0      (evidence/clone-probe-sim-strict.out)
$ python3 .ufo/gates/c1-census-v10.py --root .                 → VERDICT: PASS (stale=0 ambiguous=0 undeclared=0 unresolved=0), rc 0 (evidence/clone-census-sim.out)
# control at 14b1682 (unpatched): probe findings=0 (evidence/clone-probe-ctrl.out)
# manual needle sim on the patched file: skill-registry-row anchor hits :370 (untouched);
# shonen-skill-range :81-243 still contains its must_match (evidence/needle-sim.txt)
```

All git operations confined to the disposable clone under `/var/tmp/ex36`; the
real repo was never mutated (SKILL.md sha unchanged at close; `git status` shows
only EX-16's census edit, the standing `arc2-loop1-round10/C3.md` line, and
untracked wave/gate dirs).

## 5. Attacks / refutations attempted

- **A1 tool revised mid-seat** — ATTEMPTED, handled: an in-scratch first draft
  said "12 cases" (revision `4862f642…`); before any artifact was written the
  revision `112d01dc…` landed and every check was re-run against it. No stale
  number reached the artifact. Residual: if EX-31 revises again before records,
  re-run §4 and correct the case count only (§6).
- **A2 first-drafted v1 clause was wrong** ("a v1 receipt compares as
  MATCH-V1-PARTIAL" as a blanket claim) — CONFIRMED WRONG by measurement: the
  round-1 CU-1 stanza-v1 receipt reproduces the label defect and exits 12; only
  the sums form exits 0. The row now states both shapes. The frozen claim's
  wording ("verifiable against the tool's sha256 fields") holds — the SHA256
  CONTRACT line prints 5/5 in every shape — but "compares" ≠ "exit 0" for
  label-defective v1 stanzas. Matches EX-35 §3 independently.
- **A3 `selftest --scratch <nonexistent>` crashes** — real instrument edge defect:
  uncaught `FileNotFoundError` traceback, exit 1 (not USAGE exit 2), reproduced on
  the pinned revision (`evidence/selftest-badscratch.out`). Row unaffected (its
  clause names the default resolution order, whose roots exist). EX-31's target;
  flagged for the chain close, not fixed here.
- **A4 "the row promises more than the code"** — clause-by-clause against the
  code and EX-31's README: verbs/flags, field names, exit map, precedence, the
  15 case names, scratch order, the custody-path write refusal — all match. No
  `expected.json` exists and the row does not claim one (its "pinned values"
  clause is exactly the code constant + the receipt self-pin).
- **A5 line-shift vs C1's rule #14** — C1's insert (`c1/EX-05/insert-rule.py`)
  lands a block immediately before the "## Config custody for live-probe rounds
  (SOP)" header (`:242`), shifting my hunk's context. Simulated an 8-line insert
  at index 241 + applied this diff: `patch rc 0`, insert block intact, patched
  tail byte-equal to the intended tail (`evidence/c1sim-robustness.txt`).
  Apply-order either way is safe.
- **A6 append-only needle safety** — REFUTED as a hazard: probe findings=0 in
  both modes and census PASS 0/0/0/0 on the committed simulation; manual needle
  sim green (§4).
- **A7 "the preamble rewrite moves pinned lines"** — REFUTED: 3→3 lines; the
  SKILL.md needles are an unpinned-line anchor and a range outside the edited
  block; probe+census green on the committed sim.

## 6. Coupling tokens for the records commit

- Case count `15` and the case list are as of instrument sha256 `112d01dc…`
  (`custody-pair.py` 889 lines). If EX-31 lands a further revision, re-run §4's
  command set; correct the count/ordinals only if they moved.
- The row is line-number-free: it pins no `path:line` anywhere (rule #11
  spirit), so C1's rule-#14 insert and any records reflow cannot stale it.
- Residual (named): the instrument's selftest is not pinned by an
  `expected.json` case table the way the citation-drift probe is; "15 fixture
  cases" is a revision-pinned measurement, not a standing guarantee.

## 7. What this patch does NOT do

- Never writes SKILL.md; touches no gate file, census, receipt, or custody path.
- Does not re-claim: the round pair (EX-31/EX-32 own it), the formal
  same-content-rewrite attack (EX-33), or the v1 adapter proposal (EX-35).
- Does not fix A3 (EX-31's file, not this seat's).
