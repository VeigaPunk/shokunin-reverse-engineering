# SEAT CR-3 — chain c2 — critic — type-swap matrix around the EACCES class (arc3-loop1-round3)

Repo `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Task as given: attack the
type-swap matrix around the EACCES class — broken symlink, directory at path,
chmod-000 dir component — with every behavior **declared or flagged**.

Writes by this seat: this report + `claims/c2/CR-3/**` only. Scratch `/var/tmp/cr3`
(never `/tmp`). No git mutation. Custody paths never written, chmod-ed, renamed or
`utime`d — the harness uses explicit `--paths` on `/var/tmp` fixtures; the only
custody-path touch anywhere is the tool's own selftest guard case (stats `~/.bashrc`,
refuses to write).

## 1. Work performed (evidence pointers)

Inputs read: `claims-frozen.md`; round-2 `claims/c3/verdict.md` (D1–D7);
`EX-40/proposed-edge-classes.patch.md`; `seats/EX-22.md`; the tool + README at every
named revision.

Artifacts (all under `.ufo/waves/arc3-loop1-round3/claims/c2/CR-3/`):

| file | sha256 | what |
|---|---|---|
| `run_matrix.py` | `40112270942e244e785281feca32901bc07d2c6de7116f13d94829a030d8ff76` | 54-case harness; copies the pinned revision (asserts byte-identity), runs every case as a subprocess, captures rc+stdout+stderr verbatim |
| `matrix-BEFORE.out` | `c322a880dfbd1b4de72904dcac9f3df897ee2fa81b0ff9239d4fd0304b8b3ee6` | full matrix at `112d01dc` (git HEAD) |
| `matrix-AFTER2.out` | `10d27a9feecc4039717bf01fed28db54035926caf7061681a789ab4ca13050ac` | full matrix at `7cd19c3c` |
| `matrix-AFTER.out` | `41c3551208ec57b5de4db7caaee532e6b01fc9c5bdf9fd2d078699791abb9f7b` | full matrix at intermediate `03bd6242` |
| `churn-stability-1.log`, `churn-stability-2.log` | `06387e16…`, `7b83c64f…` | 5-second revision pollers (churn record) |
| `typeswap-matrix.md` | `75997cf7960dd3d07bab5a2c534f24c3ad4debc49b43b1de4a10ed6c7c3b2610` | verbatim case table + declaration audit |
| `typeswap-declarations.patch.md` | `46c7f78cda597469e0047cabb8307123540f022fb6289fc1106c0e495503bce7` | proposed declaration texts (§1 resolved in-flight; §2–§5 open) |

Final identities of this report and every artifact are re-derived (rule #14) in
`claims/c2/CR-3/identity-rederivation.out`, written after this report's last revision.

Revisions named by sha256 (rule #14; every measurement re-derived):

- tool BEFORE `112d01dc034c2d54324e7703e2d03d1d83b0c3930ed5d4f688546968b73ecefa`
  (889 ln, 39157 B) = `git show HEAD:…`, HEAD `c07af80`.
- tool AFTER `7cd19c3cfd835c7807d5e60dece1c2592c9df6c319a78deb14469dd6ebe8ab09`
  (1155 ln, 54279 B) — stable 8×5 s from 13:13:53Z, re-hashed unchanged at 13:15:49Z.
- README AFTER `f30df42e0a547a0aefd21590c0f975acf06d91161fcb6db77c8934960efeb193`
  (185 ln, 13:15:49Z); README BEFORE `fa484d57…` (132 ln).
- Churn inside my window (D8 hazard, live): tool 889 → 918 → 926 → 943 → 946 → 946 →
  954 → 964 → 987 → 989 → 997 → 1109 → 1106 → 1155 lines; README 132 → 146 → 146 → 185.
  Intermediate revisions are un-verdict-able; my AFTER verdicts are pinned to `7cd19c3c`
  only.

## 2. Proposed changes

**Patch text only** — `claims/c2/CR-3/typeswap-declarations.patch.md` (real target is
EX-21's; this seat wrote nothing under `.ufo/gates/custody-pair/`):

- §2 declare the content-pin scope: `TYPE: other` has no `SHA256` (stat-identity only),
  a captured directory pins one stat not a tree, a symlink pins the link not the referent.
- §3 tool: wrap `out.parent.mkdir(...)` (`tool:653` at `7cd19c3c`) in the declared
  USAGE class — closes the surviving `FileExistsError` traceback (C8 below).
- §4 three selftest cases (dangling/retarget, directory-no-content-pin,
  out-parent-not-a-directory) — count sentences must be re-derived if added.
- §5 wording W2/W3/W4. §1 (README exit-14 row) was **resolved in-flight** by EX-21 at
  `f30df42e`; kept as the record, marked do-not-apply.

## 3. Before → after measurement for the chain's claim

Commands: `python3 run_matrix.py` with `CR3_SRC` = pinned revision (tool copied,
byte-identity asserted). Same 54 cases both sides; full transcripts cited above.

| case (my label) | before `112d01dc` | after `7cd19c3c` | note |
|---|---|---|---|
| C1 capture behind chmod-000 dir | exit 13, `EXISTS: no`+`STAT-ERROR` | exit **14** `UNEVALUABLE`, receipt written | D2 → its class |
| C2 verify both-sides EACCES `--live` | **`MATCH compared=0/11 exit 0`** (fail-open) | `UNEVALUABLE exit 14`, note "reference+candidate side" | the claim's headline hole, closed |
| C3 EACCES receipt vs now-readable | `ABSENT exit 13` | `UNEVALUABLE exit 14` | fail-closed direction |
| C4b verify `--live`, chmod-000 file | `PermissionError` traceback, exit 1 | exit 14 | |
| C6b capture, chmod-000 file | traceback exit 1, **no receipt** | exit 14, receipt with `READ-ERROR` | record survives |
| C14b/C15b ENOENT-recorded receipt vs chmod-000 live | traceback exit 1 | exit 14 | D2's second entry, closed |
| D4b receipt-vs-receipt unevaluable | `MATCH 0/0 exit 0` | exit 14 | parser reads both error keys |
| C9/C10/C11 selftest scratch 000 / missing / file | tracebacks exit 1 | `USAGE exit 2` + messages | D6 class |
| D3 `--paths X --out X` | exit 0, **X clobbered** (17 B → 1337 B) | `USAGE exit 2`, X byte-intact | VZ-4 |
| D1 `--require-paths 5` on 1-path ref | flag absent (argparse exit 2) | exit 2 + `REFERENCE-COVERAGE: 1/5 …` | D3 |
| C0 selftest | `CLEAN cases=15` | `CLEAN cases=22` | ≥17 required |
| C8 `--out <file>/rec.txt` | `FileExistsError` traceback exit 1 | **unchanged: traceback exit 1** | flagged, open |
| B-group (dir at path, fifo) and A-group (broken symlink) | classes below | identical classes | see §4 |

Headline: **every EACCES-class injection I could reach now lands on a declared class
(exit 14, never `MATCH`), and the write/scratch/coverage guards behave as declared.**
The chain's falsifiable line reproduces at my revision: fail-open / traceback / clobber
all closed; selftest 15 → 22.

## 4. Attacks / refutations attempted, with verdicts

Verdict vocabulary: **DECLARED** (behavior matches a declared class, citation given) /
**FLAGGED** (undeclared or misdescribed behavior, patch text given) / **CLOSED** (was a
named hole; now declared).

A — broken symlink:

| attack | result (before = after unless noted) | verdict |
|---|---|---|
| dangling symlink capture | exit 0, `TYPE: symlink`, sha = hash(target string) | DECLARED (`README:65-66`) |
| retarget to a different (also missing) target | `CONTENT-DRIFT exit 10` | DECLARED via sha contract |
| materialize the referent | `MATCH 11/11 exit 0` | W1: declared-by-inference; consequence (referent never opened) not spelled out |
| change the referent's content (live symlink) | `MATCH 11/11 exit 0` | W1 |
| symlink loop (`a→b→a`) | capture + verify fine, no hang | no failure mode; note only |
| symlink whose referent sits behind a chmod-000 dir | exit 0, `MATCH 11/11` | W1: EACCES class unreachable through a symlink (readlink, never open) |
| file → symlink swap | `CONTENT-DRIFT exit 10` | DECLARED |

B — directory at path (and fifo):

| attack | result | verdict |
|---|---|---|
| capture dir / fifo | exit 0, `TYPE: other`, **no SHA256**, no hang | U1: `TYPE: other` undeclared, no content pin |
| verify clean dir / fifo | `MATCH-V1-PARTIAL compared=10/11`, `SHA256-CONTRACT: 0/0`, exit 0 | U1+U2: a **v2** receipt labeled with a v1-compat class; the sha contract line is vacuous |
| entry added to the captured dir, mtime restored | `METADATA-DRIFT exit 12 moved=size,ctime_ns,ctime_epoch` | W2: caught, but the README clause "identification times equal" doesn't describe it |
| entry added inside `dir/sub/` | `MATCH-V1-PARTIAL exit 0` **blind** | U1: one stat, not a tree |
| dir → file / dir → symlink / file → dir swap | `REWRITE-DRIFT exit 11` (inode+mtime carry it) | W3: the `type differ` clause of METADATA-DRIFT is shadowed on type swaps |
| `--out` is a directory | `USAGE exit 2` | DECLARED |

C — chmod-000 (beyond §3's closed cases): C7 `--out` into a 000 parent → `USAGE 2`
(declared); C12/C13 receipt A unreadable → `USAGE 2` (declared, contrasts with the
pre-fix path-read crash); **C8 `--out` parent component is a regular file → traceback
exit 1 at both revisions → FLAGGED U3** (`tool:653` `mkdir` outside the try; patch §3).

D — round-3 surface: D1/D3/D4b CLOSED; D2 satisfied-gate still prints
`unaccounted: <5 custody paths>` (W4, wording).

Declaration-layer attack: at `039993ed` (13:14:01Z, 146 ln) the README exit table had
**no exit-14 row**, the USAGE row omitted the coverage gate and scratch guard, and the
precedence line omitted UNEVALUABLE — while the tool returned 14 in eight measured
cases. **FLAGGED then; resolved by `f30df42e` (13:15:49Z) at `README:122,123,130-131`.**
Recorded as a caught in-flight defect of the coupled landing with both hashes.
`SCORECARD.md:1452-1462` still carries the round-2 registry row (tool `112d01dc`, README
`fa484d57`) — the coupled landing's registry half is not yet re-derived at my
measurement time (state observation, parent/EX-21 closing step).

Refutations that failed (i.e., could not break the after-revision): no `MATCH` could be
forced out of any EACCES-side (live, receipt-vs-receipt, ENOENT-vs-EACCES); no hang on
loop/fifo; no write to a guarded or measured path; receipts survive every unevaluable
case; `7cd19c3c` selftest 22/22 CLEAN.

## 5. Blockers

- **Revision churn (D8, live).** The real target moved ≥13 times during my run
  (`churn-stability-*.log`); intermediate revisions are un-verdict-able, and README line
  citations shift between revisions (my citation map notes both `039993ed` and
  `f30df42e`). All verdicts are pinned to named shas; anything after `7cd19c3c`/`f30df42e`
  must be re-derived by the parent (rule #14).
- **U3 open** at `7cd19c3c`: the `--out`-parent-is-a-file traceback needs EX-21's or the
  parent's decision (patch §3 supplied). Not this seat's write target.
- **U1/U2/W1–W4 open**: declaration-only; patch §2/§5 supplied.
- Landing hygiene: `.ufo/gates/custody-pair/__pycache__/custody-pair.cpython-314.pyc`
  exists (created 13:09:15Z by a seat importing the module) — exclude from the wave
  artifacts commit (D9 recurrence); `.ufo/gates/citation-drift/__pycache__/` likewise.
- Cross-seat: CR-4 (write-guard bypass hunt) and EX-25 (clobber after-state) cover the
  guard from the evasion side; my C8 is adjacent but distinct (write-path crash, not a
  guard bypass). No overlap found with my case set.