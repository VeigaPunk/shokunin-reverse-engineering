# EX-24 — mkdir-after: the mkdir-guard injection → declared class (no traceback)

Seat EX-24 · chain c3 · role executor · wave `arc3-loop1-round4` · 2026-10-19.
Repo `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` · no git mutations · scratch
under `/var/tmp/ex24-r4` only (`/tmp` never) · custody paths read-only
(`sha256`/`stat` only; the instrument's own read-only pass).

Task: **after-state** — the residual `out.parent.mkdir(...)` outside the guarded
region (r3 R4 / CR-3 §3 / CR-4 §2 item 5) must land as a **declared class with no
traceback**.

Verdict: **closed on both my independently-built injection and the landed
revision.** The three shapes that tracebacked at exit 1 before (non-directory
parent component, unwritable parent, symlink loop) read a declared exit 2 with a
message and zero traceback lines after; the selftest grows to cover the shape on
two independent case sets, and each fix is load-bearing under a single-hunk
revert. One measured qualification: `--out` naming an **existing regular file**
reads exit 0 and overwrites that file — a clobber class, not a traceback, and
outside this claim's letter (named in §5).

## 0. Revisions, copies, method

| item | value |
|---|---|
| BEFORE (base) | `.ufo/gates/custody-pair/custody-pair.py` sha256 `7cd19c3cfd835c7807d5e60dece1c2592c9df6c319a78deb14469dd6ebe8ab09` (1155 lines, 54,279 B, mtime 10:13:20-0300) — the round-3 landed revision |
| AFTER (my injection) | `30451e3a2ca9b93ad29f70f6f3202227fd17ca6f8d202afbce469811dac72a6d` (1155 lines) — the mkdir moved inside the guarded `try` (1-hunk move, `evidence/after.diff` 12 lines) |
| AFTER (my fixture revision) | `ac2cd74efe02c61c4e57cfd3dbbc48184f44db8d067d9c8431fab826c2bdcdcc` (1183 lines) — injection + 2 selftest cases (`evidence/fixture.diff` 37 lines) |
| AFTER (landed, EX-21) | `.ufo/gates/custody-pair/custody-pair.py` sha256 `29bb45ae0fd795e54e85d8749a163159aead181b42e9d3af399326b968b30acf` (1343 lines, 65,902 B, mtime 11:09:25-0300) — explicit guarded block, the CR-3 §3 shape |
| alternative shape tested | `dadda060d2a6e98be7ba8b9d1b450a55f25afa06d7b79e116d906f96d677fb22` — `is_dir()` pre-check (`evidence/flag-only.diff`) |
| CR-3 §3 sketch, built and run | `f7dda34bb8ff11cc28d8acd95bb3288179d33119ed12af52cd226212383ac9da` (`attacks/cr3-sketch-revision.py`) |
| sabotage arms | `7cd19c3c…` (injection reverted, byte-identical to base), `675dcd08…`/`a6273c28…` (cases without the fix), `b252f5f4…` (landed fix reverted, single hunk) |
| base revision re-derived | at 14:04Z, 14:05Z, 14:08Z, 14:09Z — unchanged `7cd19c3c…` until the landing at 11:09:25-0300; the landed tool re-hashed at 14:12Z (`29bb45ae…`) |
| scratch | `/var/tmp/ex24-r4/` (variants, legs, attacks, logs); nothing written under the custody paths or the repo's custody dir by any leg |
| harness | `harness/build-injection.sh`, `harness/build-after2.sh`, `harness/run-legs.sh` (13 legs), `harness/mkdir-cases.py.txt` (the 2 case bodies) |
| repo HEAD | `015e1bab914713568f339fd53999bc180459cc40` throughout; `git status` shows no mutation by this seat |

Every leg runs the tool as a **scratch copy**; no leg writes a custody path. The
one `--paths`-scoped capture that lands a receipt writes it under `/var/tmp`.

## 1. BEFORE → AFTER, per leg

`harness/run-legs.sh` runs the same 13 legs against each revision; the full
matrices are `before/matrix.txt`, `after/matrix.txt`,
`after/fixture-rev-matrix.txt`, `after/landed-matrix.txt`,
`sabotage/reverted-matrix.txt`, `sabotage/flag-only-matrix.txt`.

| leg | command shape | BEFORE `7cd19c3c` | AFTER injection `30451e3a` | AFTER landed `29bb45ae` |
|---|---|---|---|---|
| L1 | `--out <regular-file>/sub/r.txt` | **`NotADirectoryError` traceback, exit 1**, no receipt | `USAGE: write failed (…)`, exit 2, 0 traceback | `USAGE: cannot create the receipt directory (…)`, exit 2, 0 traceback |
| L3 | `--out <read-only-dir>/deep/r.txt` | **`PermissionError` traceback, exit 1** | `USAGE: write failed (…)`, exit 2 | `USAGE: cannot create the receipt directory (…)`, exit 2 |
| A1 | `--out <symlink-loop>/r.txt` | **`OSError` ELOOP traceback, exit 1** | `USAGE: write failed (…)`, exit 2 | `USAGE: cannot create the receipt directory (…)`, exit 2 |
| A3c | `--out <existing-dir>/<regular-file>/sub/r.txt` | **traceback, exit 1**; parent file left intact | `USAGE: write failed (…)`, exit 2; parent file byte-intact | exit 2; parent file intact |
| L2 | `--out` is itself an existing regular file | exit 0 (writes the receipt into it) | exit 0 (unchanged) | exit 0 (unchanged) — see §5 Q1 |
| L4 | `--out <fresh>/sub/r.txt` | exit 0, `OK paths=1/1` | exit 0 (mkdir still creates the chain) | exit 0 |
| L5 | `--paths X --out X` | exit 2, guard refusal | exit 2 (unchanged) | exit 2 (sidecar-aware wording) |
| L6 | normal capture, fresh file | exit 0, `OK paths=1/1` | exit 0 | exit 0 |
| L7 | `--out -` stdout mode | exit 0 | exit 0 | exit 0 |
| L8 | `--out ''` | exit 2 `USAGE: write failed (…)` | exit 2 (unchanged) | exit 2 (`--out carries no usable name…`) |
| L9/L10 | `verify --live` / receipt-vs-receipt | exit 0 `MATCH` | exit 0 `MATCH` | exit 0 `MATCH` |
| L11 | `selftest --scratch <dir>` | CLEAN 22/22 | CLEAN 22/22 (injection alone adds no case) | **CLEAN 28/28** |
| L12 | `selftest --scratch <missing>` | exit 2 (D6, unchanged) | exit 2 | exit 2 |
| L13 | `--paths X.sha256 --out X` (sidecar residual) | exit 0, measured file **clobbered** | exit 0, clobbered (unchanged by this injection) | exit 2, file intact (closed by EX-21's r4 sidecar guard) |

Selftest with the fixtures this seat authored:

| revision | selftest | note |
|---|---|---|
| base `7cd19c3c` | `CLEAN cases=22 passed=22` | cannot see the shape at all |
| injection only `30451e3a` | `CLEAN cases=22` | behaviour fixed, no case yet |
| `ac2cd74e` (injection + my 2 cases) | **`CLEAN cases=24 passed=24 failed=0`** | the two new cases PASS |
| `a6273c28` (my 2 cases, fix reverted) | **`DIRTY cases=24 passed=22 failed=2 exit=3`** | the two new cases FAIL — load-bearing |
| landed `29bb45ae` | **`CLEAN cases=28 passed=28 failed=0`** | its own `out-parent-not-a-directory-usage-exit` PASS |
| landed + my 2 cases grafted | **`CLEAN cases=30 passed=30 failed=0`** | independent case set agrees on the landed fix |
| landed with the mkdir guard reverted (`b252f5f4`, 1 hunk) | **`DIRTY cases=28 passed=27 failed=1`** | exactly `out-parent-not-a-directory-usage-exit` FAIL; L1 back to traceback exit 1 |

The last row is the attack that matters: **EX-21's landed fix is load-bearing
under a single-hunk revert**, and this seat's independent case set catches the
same revert — two case sets, one behaviour.

## 2. Why the injected shape is "move it into the guarded `try`"

The declared map (`README` exit table) gives the write path exactly two classes:
`USAGE 2` for a refused/failed write, `14 UNEVALUABLE` for an unevaluable path.
Exit 1 is not in the map. The guarded `try` already catches `OSError` and prints
`USAGE: write failed (…)` — `NotADirectoryError`, `PermissionError`,
`FileExistsError` and `ELOOP` are all `OSError` subclasses, so the one-line move
inherits the declared class with **no new message, no new exit code and no new
branch**. Measured consequences: the declared map is unchanged; `--out ''` keeps
its pre-existing USAGE (the message stays `write failed (…)`, not a new string);
and a fresh, creatable parent still gets created (L4).

The alternative shape — an explicit `is_dir()` pre-check (`dadda060…`,
`evidence/flag-only.diff`) — also reaches exit 2, but **over-refuses**: L4 (a
fresh parent that the tool must create) reads exit 2 instead of 0. That is a
regression on the common path, so it is filed as a rejected alternative, not a
candidate. EX-21's landed revision takes a third shape (explicit
`try/except OSError` around the `mkdir` alone, with its own message) which keeps
L4 working and is behaviourally equivalent to the injected shape on all 13 legs;
its only cost is a new message string. This seat built that shape independently
(`f7dda34b…`) before the landing appeared, and it reproduces the same classes
(L1/L3 exit 2, L4 exit 0).

## 3. Attacks / refutations attempted

| # | attack | verdict |
|---|---|---|
| A1 | **symlink loop** `--out loop/r.txt` | before: `OSError` ELOOP traceback exit 1; after: declared exit 2, no traceback. Fixed by the injection (and by the landing). |
| A2 | **symlink to a real directory** `--out dirlink/r.txt` | after: exit 0, receipt written through the link — no over-refusal introduced. |
| A3 | **partial chain** `--out newA/newB/pfile/sub/r.txt` where only `newA/newB` are fresh | exit 0 on both sides: `mkdir(parents=True)` creates the whole chain up to the final component, so the "fresh chain" shape is **not** a failure — my first A3 probe was mis-specified as a failure leg; corrected as A3c (pre-existing regular file in the chain) → exit 2, parent file byte-intact (`attacks/A3-misspecified-control-*.out`, `A3c-*`). |
| A4 | **`--out` is an existing directory** | after: exit 2 `USAGE: write failed (…)` (unchanged class). |
| A5 | **deep fresh chain** `--out x/y/z/r.txt` | after: exit 0, `OK paths=1/1` — the fix does not break legitimate creation. |
| A6 | **"the fix is cosmetic — nothing can catch a revert"** | **refuted**: the reverted-fix arms read DIRTY on both case sets (mine 22/24; landed 27/28). Unlike r3's R1 (a sabotage arm that stayed CLEAN), this one is load-bearing. |
| A7 | **"the fix regresses the declared map"** | refuted on the legs that matter: `--out ''` exit 2, L4 exit 0, L5–L7 unchanged, verify legs unchanged. The only new exit code anywhere is 2. |
| A8 | **"the landed revision moved under the measurement"** | measured: the landing appeared at 11:09:25-0300 mid-run; every landed figure in this artifact was re-measured **after** it (tool `29bb45ae…`, README `125e7e02…` at 14:12Z). Base-revision figures come from `7cd19c3c…`, re-derived at four timestamps before the landing. |
| A9 | **"`--out <existing file>` is the same hole"** | **partly sustained, then bounded**: exit 0 and the file is overwritten — measured, unchanged by the injection, and *outside this claim's letter* (no traceback; the class is the pre-existing "writes where you pointed it" behaviour). Named in §5 Q1. |

## 4. Proposed changes (patch texts)

| artifact | sha256 | status |
|---|---|---|
| `evidence/after.diff` | `806117ae…` | the injection (1-hunk move) — **superseded**: the landed revision closes the residual by the CR-3 §3 shape; filed for the record, not for application |
| `evidence/fixture.diff` | `9289c649…` | the 2 selftest cases as a patch text on top of the injection — superseded by EX-21's landed `out-parent-not-a-directory-usage-exit` (28 cases); filed as the independent case set |
| `evidence/flag-only.diff` | `5f4e2e43…` | rejected alternative (`is_dir()` pre-check over-refuses L4) — filed with its counter-measurement |
| `evidence/skill-row.diff` (+ `SKILL.proposed.md` `68435482…`) | `c369f73d…` | **still applicable**: the SKILL.md custody-pair row (`SKILL.md` `5eec51c0…`, 390 lines) still says `22 fixture cases` and carries no write-path bullet; the patch is line-neutral (390 → 390) and applies cleanly to a pristine copy (`patch -p0`, verified byte-identical to the intended result) |
| `evidence/readme.diff` (+ `README.proposed.md` `7ac6f9c4…`) | `9207e548…` | **superseded** — built against the pre-landing README `f30df42e…`; the landed README (`9d9400da…` at write time) already declares residual (b) (`- **(b) receipt-directory failures → USAGE 2.**`) and `cases=28`. Not for application. |

The SKILL row patch touches the row's *declared classes* sentence
(`refused write — including a receipt directory that cannot be created …`), its
selftest count (`22 → 24 fixture cases`) and its case list (adds
`a non-directory --out parent → 2 (in-process and subprocess)`). If the parent
prefers to track EX-21's landed 28-case revision instead, the count/case-list
clauses should read 28 with the landed case name
(`out-parent-not-a-directory-usage-exit`); the declared-class clause is
revision-independent.

## 5. Measured qualifications (named, none voids the claim)

1. **`--out` naming an existing regular file reads exit 0 and overwrites it**
   (L2, both sides, `before/logs/L2.out` / `after/logs/L2.out`). No traceback and
   no exit-1 class — the write simply lands where `--out` pointed. The write
   guard's scope is `set(--paths) ∪ CUSTODY_PATHS` by resolved path and inode, so
   an unguarded existing file is written. A clobber-class residual, distinct from
   the mkdir class this seat owns; recorded so the r4 record does not read "the
   write path is fully guarded".
2. **`--out ''` message moved with the landing.** Before and with the injection
   it reads `USAGE: write failed ([Errno 21] Is a directory: '.')`; on the landed
   revision it reads `USAGE: --out carries no usable name …`. Same class (2),
   different message — noted so a message-grep does not read as a class change.
3. **`/var/tmp` variant copies are the objects measured.** Every sha256 in §0
   for my own revisions names a `/var/tmp/ex24-r4/` path; the landed copy is
   archived at `evidence/landed-29bb45ae.py` (`29bb45ae…`, byte-identical to the
   repo tool at 14:12Z) so the after-state is re-derivable without the scratch dir.
4. **`evidence/README.proposed.md` and `evidence/SKILL.proposed.md`** are the
   patched documents this seat generated; they are artifacts under the seat's
   own dir, not writes to the scoped files.
5. **The landed README moved twice while this seat wrote** (`c8bdfc91…` 11:09:33
   → `125e7e02…` 11:10:12 → `9d9400da…` 11:11:35-0300; the tool did not move,
   `29bb45ae…` throughout). Citations into it are therefore given as **text
   anchors, not line numbers**: the residual-(b) bullet opens
   `- **(b) receipt-directory failures → USAGE 2.**`, the count reads
   `28 cases:` and the terminal line reads
   `CUSTODY_PAIR_SELFTEST: CLEAN cases=28 passed=28 failed=0 exit=0` — all three
   present in `9d9400da…`, the revision current at write time. My §4/§5 numbers
   were re-anchored after the second move.

## 6. Identity re-derivation (rule #14)

All figures below were re-derived at write time (14:11–14:12Z) from the files on
disk, not quoted from earlier in this run; commands are `sha256sum` / `stat` /
`wc -l` / `patch -p0` against the paths named.

```
base   .ufo/gates/custody-pair/custody-pair.py  7cd19c3cfd835c7807d5e60dece1c2592c9df6c319a78deb14469dd6ebe8ab09  1155 lines  54279 B
landed .ufo/gates/custody-pair/custody-pair.py  29bb45ae0fd795e54e85d8749a163159aead181b42e9d3af399326b968b30acf  1343 lines  65902 B
landed .ufo/gates/custody-pair/README.md        125e7e0225133738b9b780d6edbb37ded54b4a19de3263cf1c29911d97188186
SKILL  SKILL.md                                 5eec51c089e57f5d5806b4728261fb8c959637580a73aed7be4cddc1866b8f3f   390 lines
mine   variants/after/custody-pair.py            30451e3a2ca9b93ad29f70f6f3202227fd17ca6f8d202afbce469811dac72a6d
mine   variants/after2/custody-pair.py           ac2cd74efe02c61c4e57cfd3dbbc48184f44db8d067d9c8431fab826c2bdcdcc
mine   variants/sabotage2/custody-pair.py        a6273c285c8c008345ead2dc9b0972e39037ae608060f000706b085b989fb59d
landed variants/mutlanded/mut-b.py               b252f5f45ee8c9df3d7b2999463ad75545d572a7470e2150fcd45789e91e2664
live   after/landed-live.txt                    af09f9db52a9929b28125b429b71f5a9b62f62ca9f1075853673e26a08473dee   (self-pins tool 29bb45ae…)
```

Custody paths were read by the instrument's own hash/stat pass only; this seat's
`stat` sweep of the five paths (recorded in `evidence/identities.txt`) shows the
same epoch/ctime values as the receipts, i.e. no write reached them.

Command A (SCORECARD recipe) at HEAD `015e1bab914713568f339fd53999bc180459cc40`:

```json
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0,
 "knowledge_files": 83, "mapped": 83, "missing": [], "revision": "015e1bab914713568f339fd53999bc180459cc40",
 "rule_blocks": 14}
```

i.e. unchanged at the round's HEAD; `git status` reports `corpus/knowledge` clean
(no tracked knowledge file touched by this seat).
