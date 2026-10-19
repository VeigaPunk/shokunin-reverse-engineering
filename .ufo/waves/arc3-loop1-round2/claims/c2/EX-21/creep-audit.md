# EX-21 — external creep audit of the landed v11 census diff

Seat EX-21 (chain c2, executor, external auditor). Task: diff audit of the landed
v11 census diff in `scope-diff.py` form — **every SCOPE bound byte-stable, 0 creep
flags** — performed independently of EX-16's own audit. Round `arc3-loop1-round2`,
2026-10-19.

## Verdict

**HOLDS.** The SCOPE table is byte-identical across the v10→v11 diff (literal
sha256 `000b74e2…` on both sides), 20/20 rows, 0 added / 0 removed / 0 changed,
scoped file set unchanged, all ten detector regexes unchanged, and **0 creep flags
from two independent implementations**. Behaviourally, the declared bound still
bites (planted locus past `:855` → `UNDECLARED` FAIL exit 1). Only remark: the flag
check is a *byte* check and the run-invariance check has no teeth against widening
(§5) — the bytes are the load-bearing evidence, and they are unchanged.

| item | value |
|---|---|
| audited before | `/var/tmp/ex21/census-v10-baseline.py` = `.ufo/gates/c1-census-v10.py` at HEAD `14b1682` |
| before identity | sha256 `6f1d19ff4b0878adfcdf0e38523aa79db461e74942eaafc018036a504163cc8b`, 490 L, 23939 B |
| audited after | `d0772ce8…` = `.ufo/gates/c1-census-v10.py` in the worktree (EX-16's declared FINAL) |
| after identity | sha256 `d0772ce892223690d571448eeed81778d4a631b58a297d2633c31d241c8d97b5`, 610 L, 31906 B, ino 32864921 (in-place rewrite; same inode as before), mtime=ctime 1792412294 |
| target hash across the audit | identical before and after (`sha256sum` pre/post in `receipts/after/identities.txt` + the shell transcript) |
| SCOPE literal sha256 | `000b74e28bf1017ab24a93d9958f3e8e56cae75d19d9bcec5cce4cc79a1339e2` — **same both sides** |

Commands (all from the repo root; receipts under
`.ufo/waves/arc3-loop1-round2/claims/c2/EX-21/receipts/{before,after}/`):

```
python3 claims/c2/EX-21/scope-audit.py compare <before> <after>      # exit 0 = SCOPE literal identical
python3 claims/c2/EX-21/cr5-tool/scope-diff.py <before> <after>      # round-1 CR-5 differ, verbatim
python3 claims/c2/EX-21/diff-surface.py <before> <after> [--diff]
python3 claims/c2/EX-21/scope-audit.py invariance <before> <after> <root>
bash    claims/c2/EX-21/run-audit.sh <before> <after> <repo> <outdir>
```

## 1. SCOPE table byte-identity (`receipts/after/scope-audit-compare.out`)

```
scope-literal-sha256 before=000b74e28bf1017ab24a93d9958f3e8e56cae75d19d9bcec5cce4cc79a1339e2
scope-literal-sha256 after =000b74e28bf1017ab24a93d9958f3e8e56cae75d19d9bcec5cce4cc79a1339e2
rows before=20 after=20   ADDED (0)  REMOVED (0)  CHANGED (0)
scoped files before=['PROVINCE.md', 'SCORECARD.md', 'SKILL.md'] after= same
CREEP FLAGS: []
exit=0
```

Row parsing here is `ast.literal_eval` per row (not the round-1 regex), so a row
rewritten into a non-literal form would fail loudly (exit 2) rather than be skipped.
No row was unparseable on either side.

Detector constants: all ten (`PIN`, `VER`, `PTR`, `CACHE`, `REA_GATE`,
`INLINE_MARKER`, `HOLDING`, `HOLDING_OK`, `RECEIPT`, `ANCHORS`) compare `same`
byte-for-byte; none was narrowed or broadened (a narrowed `REA_GATE` would be a
detection-creep signature even with the table fixed).

## 2. Code surface (`receipts/after/diff-surface.out`)

```
CHANGED  main   bb8cc619657d -> 2c1a40742938   lines 427-490 -> 503-610
BLOCKS: total_after=29 changed=1 same=28
```

Only `main()` carries code; the rest of the delta is the header/docstring text
(EX-16's r9 provenance block and title/usage lines). File-read surface unchanged:
the landed instrument opens only the three scoped files via
`os.path.join(args.root, f)` (landed line 518) plus `live_pins()`'s pre-existing
custody/package reads in unchanged blocks; `files = sorted({s[0] for s in SCOPE})`
is unchanged, so the instrument cannot quietly read a wider input set.

The recorded patch is a faithful image of the audited bytes: applying EX-16's
`receipts/after/landing-diff.patch` to my own baseline copy regenerates the
audited file byte-for-byte (`cmp` clean; both `d0772ce8…`;
`receipts/after/patch-roundtrip.out`). Its frozen before-side
(`tools/census-before.py`) also hashes to my baseline `6f1d19ff…`, so the diff
chain has no identity gap.

## 3. Creep flags — two independent implementations, both empty
My rules (superset of the round-1 form): open-ended bound (end ≥ 9000), bound
reaching the file's last line, added DATED row wider than 150 lines, row removal
(coverage loss), widen-by-add/remove, bound movement in *either* class, marker-line
moved later, marker regex changed, DATED→CURRENT merge flip, scoped file set change.

```
EX-21 scope-audit.py : CREEP FLAGS: []   (exit 0)
CR-5  scope-diff.py  : CREEP FLAGS: []   (exit 0, verbatim round-1 tool)
```

EX-16's own certificate says the same (`receipts/after/scope-diff.txt`); note its
tool is a byte-copy of the round-1 CR-5 differ, which is why this seat wrote a
second implementation rather than re-running the same code.

## 4. Behavioural envelope — why the byte check is necessary but not sufficient

`receipts/after/bound-teeth.out`: a scratch tree whose `SCORECARD.md` gains one
appended locus (`rea-agents@6.3.0` at line 1418, past the declared `769-855`
bound) reads

```
VERDICT: FAIL  (stale=0 ambiguous=0 undeclared=1 unresolved=0)   exit=1
```

on both instruments. So the declared envelope still bites after the diff: had the
diff widened a bound to absorb the tail, the appended locus would have been
swallowed as `historical` and this test would have flipped to PASS.

## 5. Measured limit of the run-invariance check (auditor honesty)

`scope-audit.py invariance` compares per-file `lines`/`loci`, verdict, counters,
`live` anchors and current-ok counts between the two instruments at HEAD. It
reports `INVARIANCE: HOLDS` (PASS exit 0 both; `6/9/2`; current-ok blocks 5;
historical 5). But a positive control shows it has **no teeth against scope
widening**: widening the `769-855` row to `769-1336` changes nothing, because
`SCORECARD.md:856-1400` is locus-free in the census unit (measured: 0 matches for
`rea-agents@x.y.z` / bare `6.x.y` / `~`- or `/`-absolute `path:line`). The check
therefore catches detection-code drift only — the SCOPE byte comparison (§1) and
the bound-teeth test (§4) are the creep evidence. Stated so the certificate is not
read as stronger than it is.

## 6. Independent re-runs of the round-1 silent-PASS classes

Each case is a scratch root under `/var/tmp`; both instruments were run on the
same bytes. Exit codes measured, not asserted
(`receipts/{before,after}/{h1-absent,truncation,h3-blind}.out`):

| injection | v10 before | v11 after |
|---|---|---|
| `SKILL.md` absent | **PASS exit 0**, `lines=0 loci=0` (silent) | FAIL exit 1, `UNREADABLE … ['SKILL.md: FileNotFoundError']`, `DECLARED FAIL CLASSES: ['UNREADABLE']` |
| `PROVINCE.md` / `SCORECARD.md` absent | FAIL exit 1 (marker uncheckable) | FAIL exit 1 (+ declared UNREADABLE) |
| `PROVINCE.md` cut to 130 lines (< declared max 131) | **PASS exit 0** (silent shrink) | FAIL exit 1, `UNREADABLE … ['PROVINCE.md: 130 lines < declared max 131 (rows beyond EOF)']` |
| `SKILL.md` cut to 19 lines (< declared max 20) | **PASS exit 0** (silent shrink) | FAIL exit 1, declared UNREADABLE |
| `SCORECARD.md` cut to 850 lines (< declared max 855) | **PASS exit 0** (silent shrink) | FAIL exit 1, declared UNREADABLE |
| `PIN`/`VER`/`PTR` neutered | **PASS exit 0** with `loci=0` all files, `G2 … ok` | FAIL exit 1, `G2 … SUSPECT (… per file 0/0/0 …)`, `DECLARED ['BLIND-INSTRUMENT']` |
| ordinary tree at HEAD | PASS exit 0, 0/0/0/0 | PASS exit 0, 0/0/0/0 (identical) |

The three truncation cases are **new measurements** contributed by this seat: the
round-1 H1 reproduction named absent-file only, and all three shrink cases were
silent PASSes on v10 (the declared rows past EOF were absorbed). On v11 all three
are a declared class.

Text-contract check (`receipts/after/../`, my own runs): the ordinary-run stdout
delta is exactly three lines (new `UNREADABLE` line, extended `G2` line, new
`DECLARED FAIL CLASSES` line); the per-file `lines=/loci=` lines and the `VERDICT:`
line are byte-identical between instruments. Independent reproduction of EX-16's
declared full-run stdout sha: my run of the landed bytes gives
`1db2ec31e8f8896031f1f80a2d90f7e2801af645c4f685d2c55100534d1b7cc0` — equal to the
value in its seat report §3.

## 7. Attacks on the auditor itself

- **Positive controls (must fire).** Three injected fixtures — DATED end widened
  (`769-855`→`769-900`), open-ended added row (`856-99999`), CURRENT→DATED flip
  with a moved marker — each produced flags from both implementations (mine also
  flags the row removal, which the round-1 tool does not). Exit 1.
- **Negative control.** Baseline vs itself: 0 flags, exit 0.
- **Benign control.** Comment-only edits: 0 flags, exit 0, and the SCOPE literal
  sha unchanged — i.e. the audit is inert to changes that are not scope moves.
- **Mid-flight revisions.** EX-16 landed and then revised three times
  (`82fb807e` → `df9ffdf9` → `a4c16763` → `d0772ce8`). I ran a provisional audit at
  `df9ffdf9`, then re-ran everything on the final bytes; the final run's receipts
  are the ones kept. The provisional run agreed on every check, so no finding here
  is pinned to a superseded revision.
- **Residue self-check.** Reading/importing the round-1 tool created
  `__pycache__` directories under `arc3-loop1-round1/claims/c3/CR-5/tools/` and my
  own artifact dir; both were removed (`git status` shows no such untracked dirs
  from me).

## 8. Residuals / handoff pins

- **Pin.** The audited revision is `d0772ce8…` (610 L). Any other seat's receipt or
  verdict pinned to `82fb807e…` (560 L) or `df9ffdf9…` (601 L) is superseded by the
  final bytes; EX-16's own §5 names this gap for the parent.
- **Not covered by this audit** (named, not closed): H4 instrument self-widening —
  the certificate stays the external differ, as the code docstring states; DATED
  shelter (a false current claim inside a DATED range reads `historical`, PASS on
  both sides — I reproduced the bound-teeth test only for the past-bound case);
  PIN-only or VER-only partial blindness (EX-16 §4 A7).
- The floor unit is current-ok **detections** (17/14/3 per file at HEAD), so a file
  whose detections all read `historical` would fail the floor by design; no scoped
  file is in that state at HEAD (measured above).

## 9. Receipt index

```
receipts/before/00-identity.txt              baseline sha/wc/stat
receipts/before/scope-literal-before.txt     baseline SCOPE literal + sha256
receipts/before/h1-absent-before.out         absent-file classes on v10
receipts/before/h3-blind-before.out          neutered-needle class on v10
receipts/before/w-bound-teeth-before.out     planted-locus envelope on v10
receipts/before/ordinary-before.out          v10 at HEAD + JSON counters
receipts/after/{identities,scope-audit-compare,cr5-scope-diff,diff-surface,
                invariance,h1-absent,truncation,h3-blind,bound-teeth,head-runs,
                patch-roundtrip}.out
tools: scope-audit.py, diff-surface.py, run-audit.sh, cr5-tool/scope-diff.py
```
