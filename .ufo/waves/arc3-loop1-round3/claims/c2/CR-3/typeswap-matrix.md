# CR-3 — type-swap matrix around the EACCES class (seat artifact)

Seat CR-3 · chain c2 (critic) · wave `arc3-loop1-round3` · repo
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.

## Revisions under measurement (identity discipline, rule #14)

| label | revision | size | lines | how pinned |
|---|---|---|---|---|
| BEFORE | tool `112d01dc034c2d54324e7703e2d03d1d83b0c3930ed5d4f688546968b73ecefa` | 39157 B | 889 | `sha256sum .ufo/gates/custody-pair/custody-pair.py`; equals `git show HEAD:…` (HEAD `c07af80`) |
| AFTER | tool `7cd19c3cfd835c7807d5e60dece1c2592c9df6c319a78deb14469dd6ebe8ab09` | 54279 B | 1155 | stable 8×5 s from 13:13:53Z (`cr3/stability2.log` `STABLE-AT`); re-hashed after the run (same digest) |
| AFTER README | `f30df42e0a547a0aefd21590c0f975acf06d91161fcb6db77c8934960efeb193` | | 185 | `sha256sum .ufo/gates/custody-pair/README.md` at 13:15:49Z |
| BEFORE README | `fa484d573b0debb0d2ed134d076cb9593e7c3ee910ad4487d99cb9f3a8239bba` | | 132 | round-2 landed value, re-hashed at session start |

Churn observed in this session between the two anchors (intermediate, un-verdict-able
revisions; D8 hazard live): `68e30768` (918 ln) → `1287c9d6` (926) → `a8f81dcf` (943) →
`b9bd55e9` (946) → `a991f976` (946) → `9860149d` (954) → `d9be407d` (964) → `08fb6833`
(987) → `a611ede4` (989) → `ec2b2d48` (997) → `03bd6242` (1109) → `dc841464` (1106) →
**`7cd19c3c` (1155)**. A full matrix run was also taken at `03bd6242` (transcript on
file) — same classes as at `7cd19c3c` except where noted. README churn: `fa484d57` (132
ln) → `68458081` (146 ln, 13:12Z) → `039993ed` (146 ln, 13:14:01Z) → **`f30df42e`**
(185 ln, 13:15Z).

### README revision note (for the citation numbers below)

Line citations `README:N` were taken against `039993ed` (146 lines) at 13:14Z. At the
current `f30df42e` (185 lines) the same clauses sit later (exit table now
`README:115-124`, precedence now `README:130-131`, capture-exit rule now
`README:126-128`); the exit map gained the exit-14 row, the USAGE scope, the
precedence term, and a "Round-3 hardening" section. The A/B/C-table citations below
are therefore quoted against `039993ed` where they concern *behavior* (unchanged), and
the EACCES-class map hole recorded there is now **closed** at `f30df42e` — see the
declaration audit.

## Harness

`/var/tmp/cr3/run_matrix.py` (copy in this directory): copies the pinned revision to
`/var/tmp/cr3/work/tool/` (assert byte-identical), builds fixtures under
`/var/tmp/cr3/work/fix/`, runs every case as a subprocess (rc + stdout + stderr captured
verbatim), receipts under `/var/tmp/cr3/work/rec/`. Scratch is `/var/tmp` only.
Transcripts: `matrix-BEFORE.out` (54 cases), `matrix-AFTER2.out` (54 cases),
`matrix-AFTER.out` (intermediate `03bd6242`).

## Verdicts — every behavior declared or flagged

Declared citations use the AFTER revision: `tool:N` = docstring/code line of `7cd19c3c`,
`README:N` = line of README `039993ed`.

### A — broken symlink

| case | command (abridged) | before | after | verdict |
|---|---|---|---|---|
| A1 capture dangling | `capture --paths dangling` | exit 0, `TYPE: symlink`, `SHA256` = hash of the target string | same | **DECLARED** (`README:63-64`; capture exit rule `README:97-99`) |
| A2 verify unchanged | `verify receipt --live` | `MATCH 11/11 exit 0` | same | **DECLARED** |
| A3 retarget | retarget link, `verify --live` | `CONTENT-DRIFT exit 10` | same | **DECLARED** via the sha contract (`README:60`, `README:63-64`) |
| A4 referent materialized | create the dangling link's referent, `verify --live` | `MATCH exit 0` | same | **DECLARED-BY-INFERENCE** (lstat pins the link only) — consequence not spelled out → **W1** |
| A5 referent content drift | modify referent, `verify --live` | `MATCH exit 0` | same | same as A4 → **W1** |
| A6 symlink loop | capture + verify | exit 0, no hang, `MATCH` | same | no failure mode; declaration not needed (note only) |
| A7 file → symlink swap | `verify --live` | `CONTENT-DRIFT exit 10` | same | **DECLARED** (both sides carry a sha; digests differ) |
| C16 symlink into 000 dir | capture + verify | exit 0, `MATCH 11/11` | same | **FLAG W1**: the EACCES class is *not reachable* through a symlink — capture takes `os.readlink`, never opens the referent. Undeclared, but consistent; belongs in the scope sentence |

### B — directory at path (and fifo)

| case | command (abridged) | before | after | verdict |
|---|---|---|---|---|
| B1 capture dir | `capture --paths dirA` | exit 0, `TYPE: other`, **no** `SHA256` | same | **FLAG U1**: no declared meaning for `TYPE: other`; no content pin |
| B2 verify clean dir | `verify --live` | `MATCH-V1-PARTIAL compared=10/11`, `SHA256-CONTRACT: 0/0`, exit 0 | same | **FLAG U1+U2**: a v2 receipt labeled with a v1-compat class; the sha-contract line is vacuous (`0/0 agree`) |
| B3 entry added to the captured dir, dir mtime restored | `verify --live` | `METADATA-DRIFT exit 12 moved=size,ctime_ns,ctime_epoch` | same | caught, but **W2**: README:92's clause ("identification times equal but size differs") does not describe what happened (ctime moved; size + ctime are both in `moved`) |
| B4 entry added inside `dir/sub/` | `verify --live` | `MATCH-V1-PARTIAL exit 0` | same | **FLAG U1 (blind spot)**: a captured directory pins its own stat only; changes below the first level are invisible |
| B5 dir → file swap | `verify --live` | `REWRITE-DRIFT exit 11 moved=inode,mtime_ns,mtime_epoch` | same | **W3**: the `type differ` clause of METADATA-DRIFT (`README:92`) is shadowed — a type swap lands in REWRITE-DRIFT because the inode/mtime move with it |
| B6 fifo at path | capture + verify | exit 0 (no hang), `MATCH-V1-PARTIAL 0/0` | same | **FLAG U1** (as B1/B2) |
| B7 `--out` is a directory | `capture --out outdir` | `USAGE exit 2` write failed | same | **DECLARED** (`README:94`) |

### C — chmod-000 (dir component, file, write path, scratch, receipts)

| case | command (abridged) | before | after | verdict |
|---|---|---|---|---|
| C1 capture behind 000 dir | `capture --paths blocked/inner.txt` | exit 13, `EXISTS: no` + `STAT-ERROR` | **exit 14 UNEVALUABLE**, receipt written | **CLOSED** (D2) — **DECLARED** (`tool:103-105`, `tool:108`) |
| C2 verify both-sides EACCES | `verify receipt --live` | `MATCH compared=0/11 exit 0` (fail-open) | `UNEVALUABLE compared=0/11 exit 14`, note "reference+candidate side" | **CLOSED** (D2) |
| C3 EACCES receipt vs now-readable | `verify --live` | `ABSENT exit 13` | `UNEVALUABLE exit 14` (fail-closed) | **CLOSED** |
| C4b verify --live, unreadable file | file 000, dir readable | `PermissionError` traceback, exit 1 | `UNEVALUABLE exit 14` | **CLOSED** |
| C6b capture, unreadable file | file 000 | traceback exit 1, **no receipt**, no record | exit 14, receipt written with `EXISTS: yes` + `READ-ERROR` | **CLOSED** |
| C7 `--out` into a 000 parent | `capture --out blocked/out.txt` | `USAGE exit 2` (write failed) | same | **DECLARED** (`README:94`) |
| C8 `--out` parent component is a **file** | `capture --out pfile.txt/rec.txt` | `FileExistsError` traceback, exit 1 | **unchanged: traceback exit 1** (`tool:653` `out.parent.mkdir` outside any `try`) | **FLAG U3 — undeclared crash survives the revision** |
| C9 selftest scratch 000 | `selftest --scratch blocked` | `PermissionError` traceback, exit 1 | `USAGE exit 2` with message | **CLOSED** (D6 class) |
| C10 selftest scratch missing | `selftest --scratch no-such-dir` | `FileNotFoundError` traceback, exit 1 (D6) | `USAGE exit 2` | **CLOSED** (D6) |
| C11 selftest scratch is a file | `selftest --scratch pfile.txt` | `NotADirectoryError` traceback, exit 1 | `USAGE exit 2` | **CLOSED** |
| C12 receipt A unreadable | `verify <000 receipt> --live` | `USAGE exit 2` | same | **DECLARED** (`README:94`) |
| C13 receipt A behind 000 dir | `verify blockedrec/r.txt --live` | `USAGE exit 2` | same | **DECLARED** |
| C14a path genuinely absent | `capture --paths notthere` | exit 13, no `STAT-ERROR` | same | **DECLARED** |
| C14b/C15b ENOENT receipt vs chmod-000 path at verify | `verify --live` | traceback exit 1 | `UNEVALUABLE exit 14` | **CLOSED** (same D2 face, different entry: an *absence*-recorded receipt met an unreadable candidate) |

### D — round-3 declared surface, exercised adversarially

| case | command (abridged) | before | after | verdict |
|---|---|---|---|---|
| D1 `--require-paths 5` on a 1-path reference | `verify receipt --live --require-paths 5` | exit 2 — argparse `unrecognized arguments` (flag absent) | exit 2 with `REFERENCE-COVERAGE: 1/5 …; unaccounted: <5 custody paths>` | **CLOSED** (D3), **DECLARED** (`tool:47`, `tool:108`) |
| D2 `--require-paths 1` (satisfied) | as above with `1` | arg error exit 2 | proceeds → `UNEVALUABLE exit 14`; line prints `1/1 … unaccounted: <5 custody paths>` | **W4**: the `unaccounted` list is the 5-unit canonical set, printed even when the gate passes and unconsumed by it — semantics ambiguous, worth one clarifying sentence |
| D3 `--paths X --out X` | `capture --out X --paths X` | exit 0; **X clobbered** by the receipt (17 B → 1337 B) | `USAGE exit 2`; X byte-intact (`b'original bytes\n'`) | **CLOSED** (VZ-4), **DECLARED** (`README:47-50`, `tool:650-651`) |
| D4b receipt-vs-receipt, both `STAT-ERROR` | `verify pre post` | `MATCH compared=0/11 exit 0` | `UNEVALUABLE exit 14` | **CLOSED** |

## Declaration audit (the "each behavior declared" bar)

Closed with a declared class and measured: every EACCES-class behavior I could reach
(capture, `--live`, receipt-vs-receipt, mixed ENOENT-vs-EACCES) now exits 14 and never
prints `MATCH`; the write-guard, scratch guard and coverage gate are as declared; selftest
15 → 22 (`matrix-AFTER2.out:198`, case list lines 175-196 — names match `README:131-134`).

Flagged (survive the revision, measured):

- **U3 — undeclared crash, write path**: `--out` whose parent path component is a regular
  file → `FileExistsError` traceback, exit 1, outside the declared map. Same family as D6
  (fixed) but on the receipt path, not the scratch path. Repro: `matrix-AFTER2.out:603-620`.
- **U1/U2 — `TYPE: other` has no declared semantics**: a v2 directory/fifo receipt verifies
  as `MATCH-V1-PARTIAL` with `SHA256-CONTRACT: 0/0`; changes below a captured directory's
  first level are invisible; a fifo has no content pin. Not a defect of the claim's named
  set — but these are *type-swap-class behaviors that are neither declared nor flagged* in
  the tool or README.
- **README map hole (EACCES class) — RESOLVED during the round**: at `039993ed`
  (146 ln, 13:14:01Z) the README exit table (`README:87-95`) had no row for exit 14 /
  `UNEVALUABLE`, the USAGE row omitted `--require-paths` and the scratch guard, and the
  precedence line (`README:101`) omitted `UNEVALUABLE` (between CONTENT-DRIFT and ABSENT
  in `tool:115`) — while the tool returned 14 in eight measured cases. At `f30df42e`
  (185 ln, 13:15:49Z) all three are declared (`README:122,123,130-131`). Recorded as a
  caught in-flight defect of the coupled landing, with both revisions' hashes.
- **Registry row not re-derived**: `SCORECARD.md:1452-1462` still carries the round-2 row
  (cites tool `112d01dc`, 889 lines, README `fa484d57`). State observation at 13:14Z;
  the coupled landing is the implementer/parent's closing step.
- **W1/W2/W3/W4**: wording/precision gaps — symlink referent scope (W1), METADATA-DRIFT vs
  ctime-moved directory change (W2), type-swap class assignment shadowing the `type` clause
  (W3), `REFERENCE-COVERAGE` unaccounted-list semantics (W4).

Not attempted (recorded as not-run): EACCES on a *custody path* (they are read-only for
all seats — never chmod-ed, never opened for write); `--require-paths` against a real
5-path reference with one live drift (out of my seat's scope; EX-22/EX-2x cover the
coverage gate's happy path).