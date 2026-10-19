# CU-1 — seat report (chain cross, role custody)

Wave `arc3-loop1-round4`, lane devin (declared fallback; recorded in the freeze).
Window: 2026-10-19 11:04–11:08 local (-03). Task: corroborate the custody half of the
round (recompute the 5 paths against any landed pair) **and** corroborate the one
authorized install (no custody path touched, no system python modified; the venv
lives under the wave dir).

Artifacts: `.ufo/waves/arc3-loop1-round4/claims/cross/CU-1/` (evidence + `MANIFEST.sha256`,
61 files, `sha256sum -c` clean). No writes outside that directory and this report.
No git mutations. All custody operations performed on a scratch copy of the tool at
`/dev/shm/cu1/tool/`; the real `.ufo/gates/custody-pair/` was read-only (hash/stat).

Report identity (rule #14): the report's own sha256 is re-derived after the final edit
and recorded in `evidence/final-sweep.txt` (a file cannot carry its own post-edit
digest without circularity; the receipt is the authoritative pointer).

---

## 1. Work performed (evidence pointers)

**Identity of the instrument (re-derived, not cited).** At round-4 open, and throughout my
custody measurements, the target was the r3 revision:
`sha256sum .ufo/gates/custody-pair/custody-pair.py` →
`7cd19c3cfd835c7807d5e60dece1c2592c9df6c319a78deb14469dd6ebe8ab09`;
`README.md` → `f30df42e0a547a0aefd21590c0f975acf06d91161fcb6db77c8934960efeb193`, both
equal to the r3 EX-21 manifest (`.ufo/waves/arc3-loop1-round3/claims/c2/EX-21/sha256s.txt`).
**At 11:09:25 C3's EX-21 wrote the r4 revision**: tool →
`29bb45ae0fd795e54e85d8749a163159aead181b42e9d3af399326b968b30acf` (65,902 B, 1343 lines),
README → `9d9400da…` (267→272 lines, still settling while I probed; the tool held
byte-stable across 4 polls). Everything in §1 below labelled "before/landed" refers to
`7cd19c3c…`; everything under §3 "after-state" refers to `29bb45ae…`. Both identities are
re-derived at write time (`evidence/final-identity.txt`, `evidence/after-revision/`).

**Scratch tool copy is byte-identical** to the target (`evidence/strace-capture.txt`
run directory `/dev/shm/cu1/tool/`, hash re-checked before every run). Selftest on the
scratch copy: `CUSTODY_PAIR_SELFTEST: CLEAN cases=22 passed=22 failed=0 exit=0`
(`evidence/selftest.out`).

**Custody read-only proof at syscall level.** `strace -f` over a full `capture` and over
a `verify --live --require-paths 5`: each of the 5 paths is opened **exactly once**,
every time `O_RDONLY|O_CLOEXEC`; zero `open(O_WRONLY/O_RDWR/O_CREAT)`, zero `unlink`,
`rename`, `chmod`, `utime*`, `truncate` against any of them (`evidence/strace-capture.txt`,
`evidence/strace-verify.txt`).

**Recompute of the 5 paths vs the landed r3 pair** — my own parser, not the tool's:
`evidence/verify-r3post-live.out` and the independent recompute block in
`evidence/final-identity.txt` re-derive sha256, size, inode, ctime_ns and mode for all 5
from the live filesystem and compare field-by-field against
`config-post-pair-ex21.txt`: **5/5 OK, 0 mismatch**. Both r3 sidecars re-derive
(`sha256sum -c` OK). Receipt-level checks with the scratch tool:
- r3 pre vs r3 post → `MATCH 5/5 exit 0`
- r3 post vs **live** → `MATCH 5/5 exit 0` (no drift since the r3 landing)
- my pre-install receipt vs r3 post → `MATCH 5/5 exit 0`
- my pre vs my post (spanning the install) → `MATCH 5/5 exit 0`
- my post vs live → `MATCH 5/5 exit 0`

**Venv install corroboration.** Venv appeared at 11:05 with
`pyvenv.cfg: include-system-site-packages = false`, `home = /usr/bin`, python 3.14.7;
`pip freeze` → vyper 0.4.3 + cbor2 5.9.0, asttokens 3.0.2, immutables 0.21, lark 1.3.1,
packaging 26.3, pycryptodome 3.24.1, wheel 0.48.0; `pip check` → "No broken requirements
found". The vyper wheel body is still in pip's HTTP cache:
`~/.cache/pip/http-v2/4/9/3/5/3/493539a37764e4837c6939e20787ef135f4d2f111071df088b7518eb.body`,
403104 bytes, `sha256 = 3b9671727c888363740dc678e60336759871487d0e4e9fdd973048fa9635c4fd`
(confirmed to contain `vyper-0.4.3.dist-info/METADATA`). Installed
`vyper-0.4.3.dist-info/RECORD` = `8bc98248714c40f899823bb568fc3f11b659ed013f375a863bb2cc9ce13cdceb`;
a spot check of `vyper/__init__.py` matches its RECORD line exactly
(`6QYENxhNLn6ARwdcHIo2hKMCtOvtYLjpR9mi_19NYa8`). Venv `bin/python3 -> /usr/bin/python3`,
i.e. the venv consumes the system interpreter read-only; the venv adds no interpreter of
its own. `evidence/final-identity.txt`.

**Nothing else was installed.** The only `pyvenv.cfg`/`activate`/`site-packages` anywhere
under the wave dir is `tools/vyper-venv/` (`evidence/final-identity.txt`); no second venv,
no repo-local site-packages.

**The venv actually runs (exercised, not just inspected).** CU-1 compiled EX-02's
`Smoke.vy` on scratch with the venv's `vyper` and reproduced their artifacts bit-for-bit
(creation and runtime), and recomputed the four ABI selectors with a real keccak256 —
details in §5. `evidence/cu1-venv-exercise.txt`, `evidence/cu1-smoke-runtime.hex`,
`evidence/cu1-runtime2.hex`.

**EX-02's receipt corroborated against my own measurement.** Their
`claims/c1/EX-02/custody-stat-readonly.txt` lists the same custody-dir census and the same
tool/README hashes I derived independently, and their "untouched since 11:04" claim matches
my census (`find .ufo/gates -newermt 11:00` → empty, both at 11:05 and 11:06).

---

## 2. Proposed changes

**none.** This seat is corroborative: no patch text, no target write. Two residuals in the
custody tool are *reproduced* below as C3's before-state, not repaired here.

---

## 3. Before → after measurement for the chain's claim

My seat measures the **custody half** of the cross claim. The cross-chain claim is
corroboration; the number that matters is custody stability across the install.

| quantity | before install (11:04:38) | after install (11:06:15) | verdict |
|---|---|---|---|
| 5 paths sha256 | 16f496e6…, 38d2a1d0…, bc66d543…, 7d2ca28a…, 6c6be761… | identical | **IDENTICAL 5/5** |
| 5 paths size/inode/mode/uid/gid | baseline | identical | **IDENTICAL** |
| 5 paths mtime/ctime_ns | baseline | identical (max mtime 1792414665 = 09:57, pre-window) | **IDENTICAL** |
| custody tool sha256 | 7cd19c3c… | 7cd19c3c… | unchanged |
| custody README sha256 | f30df42e… | f30df42e… | unchanged |
| `.ufo/gates/` files modified in window | — | **none** | PASS |
| system python binary | d78f9cf7… | d78f9cf7… | unchanged |
| `/usr/lib/python3.14` tree manifest | 98317190… | 98317190… | unchanged |
| system python has vyper / pip | no / no | **no / no** | unchanged |
| `site-packages` mtime | 1791920279.4357069 | same value | unchanged |
| live pair verify | — | `MATCH paths=5/5 drift=0 exit=0` | PASS |

The tool's own live pair across the install window:
`CUSTODY_PAIR_VERIFY: MATCH paths=5/5 drift=0 exit=0` (`evidence/post-install-verify.out`).

C3's *before* state, independently reproduced on the landed revision (so the parent can
check the after-state against a same-seat baseline rather than C3's own claim):

| residual | reproduction | observed |
|---|---|---|
| (a) sidecar path not scope-checked | `capture --out X.conf.sha256 --paths X.conf` | exit **0**, the neighbour `X.conf.sha256` **clobbered** by the receipt (`evidence/A6a.out`) |
| (b) `out.parent.mkdir` outside guarded try | `capture --out X.conf/sub/r.txt` | raw **traceback**, `NotADirectoryError`, exit **1** (`evidence/A6b.out`) |
| (c) coverage gate counts stanzas | 1 distinct path padded to 5 stanzas + `--require-paths 5` | exit **0**, `MATCH paths=1/1`, **no** `REFERENCE-COVERAGE` line; 5 unrelated paths also pass (`evidence/A1-padded.out`, `A2-noncanonical.out`) |
| (d) both-sides-absent MATCH semantics | absent-path receipt vs itself | exit **0** `MATCH 1/1`; vs live → exit 13 `ABSENT`; vs a different live set → exit 13 (`evidence/A3a-ghost-live.out`, `evidence/A3b-ghost-ghost.out`, `evidence/A3c-ghost-vs-custody.out`) |
| (d) sharp form (RV-8's case) | capture over an already-absent path, then `verify --live` | exit **0** `MATCH 1/1`, `compared=0/11` (`evidence/D2-both-absent-live.out`) |
| (c)+(d) compound | 5 absent paths, `verify --live --require-paths 5` | exit **0** `MATCH 5/5`, `SHA256-CONTRACT: 0/0` — **a reference that examines nothing passes the 5-path gate** (`evidence/E2-absent5-gate.out`) |

The distinction that matters: if the reference records the path as present and the live
filesystem says absent, the class is `ABSENT` exit 13 (my A3a). Only when **both** sides say
absent does it read `MATCH`. I reproduced RV-8's exact formulation and their result holds
verbatim; my A3a is the one-sided case and is not a contradiction of it.

### After-state: the revised tool landed mid-run (`29bb45ae…`)

C3's implementer wrote the real target at 11:09:25 (tool) / 11:09:31–11:10:12 (README).
I detected it on a routine sweep and re-ran the whole battery against the landed revision
on a fresh scratch copy; the revision then held byte-stable across 4 consecutive 20 s polls
(`/dev/shm/cu1/poll-stable.log`). Evidence in `evidence/after-revision/`.

| leg | before (`7cd19c3c…`) | after (landed `29bb45ae…`) |
|---|---|---|
| selftest | `CLEAN cases=22` | **`CLEAN cases=28`** (claim was ≥24) |
| (a) sidecar clobber, spelling B | exit 0, neighbour **clobbered** | **exit 2**, neighbour **intact** |
| (a) sidecar clobber, spelling A | exit 0, measured file replaced | **exit 2**, measured file **intact** |
| (b) `mkdir` under a non-directory | exit 1, raw **traceback** | **exit 2** USAGE, **0 tracebacks** |
| (c) padded reference + `--require-paths 5` | exit 0, silent pass, no coverage line | **exit 2**, `REFERENCE-COVERAGE: 1/5 … unaccounted: <all 5>` |
| live pair, new tool | — | `MATCH paths=5/5 drift=0 exit=0` (pre vs post2, and post2 vs live) |

The revised tool's receipts self-pin the new sha (`# tool: custody-pair.py sha256 29bb45ae…`),
and EX-21's own r4 live pair verifies `MATCH 5/5` — including against my independently
captured receipt and against the live filesystem (`evidence/after-revision/corroboration.txt`).
The r3 post receipt still verifies `MATCH 5/5` against live under the new tool, i.e. the
custody set is stable across the tool revision.

**(c)+(d) compound — still open, but adjudicated.** Five absent paths with
`--require-paths 5` still reads `MATCH 5/5 exit 0` at the landed revision. This is *not* an
unadjudicated residual: the new README carries a ruling section ("The both-absent `MATCH`",
authored by EX-26, adopted by EX-21) declaring cleanly-absent-both-sides `MATCH` as the
declared design, distinguishing it from the error-carrying fail-open the debt named, and
naming the consequence in its own words — the pair is "a weak witness by construction: no
content is compared", with the advice to pair an all-absent reference with a present-path
reference. My verdict: the residual is **closed as adjudicated**, and the ruling is honest
about the weak-witness limit. I verified the ruling text survives the README's later edits
(still present at `9d9400da…`).

Control (guard still works pre-fix): `capture --out ~/.bashrc` → USAGE exit 2, `.bashrc`
digest unchanged (`evidence/A5-out-bashrc.out`).

**Cross-check against RV-8's live-state note (C3 chain).** RV-8 reports live drift at
`~/.kimi-code/config.toml` (`8cbacd48…` → `bc66d543…`, mtime 2026-10-19 09:57:45), and that
the r1 v1-shape receipts therefore read `CONTENT-DRIFT`. I reproduced that: the r1 canonical
stanza and pipe receipts both read `CONTENT-DRIFT 10` with `SHA256-CONTRACT: 4/5`
(`evidence/r1-config-pre-pair.txt.out`, `evidence/r1-config-pre-pair-metadata.txt.out`). This is **operator-side, pre-wave** (09:57, before the
11:04 round open) and is fully consistent with my 5/5 MATCH: my pair is anchored on my own
11:04 baseline, which already contains `bc66d543…`. The two measurements are not in
conflict — the r1 receipts are 8 h stale, mine are same-window.

---

## 4. Attacks / refutations attempted, with verdicts

1. **"The tool secretly writes to a custody path."** strace on capture *and* verify.
   **Refuted** — every custody open is `O_RDONLY`, one per path per run; no
   write/rename/chmod/utime/truncate on them.
2. **"The r3 receipts are stale forgeries / the pair was hand-edited."** Independent
   recompute of all 5 paths from the live filesystem against the receipt fields, plus
   `sha256sum -c` of both sidecars. **Refuted** — 5/5 match on sha256+inode+ctime_ns+size+mode.
3. **"The install mutated a custody path."** Exact baseline diff (stat + sha256) before and
   after. **Refuted** — all 5 `IDENTICAL`, including ctime_ns (a same-content rewrite would
   move ctime even with mtime restored).
4. **"The install polluted the system python."** Binary hashes, whole
   `/usr/lib/python3.14` tree manifest, site-packages mtime, and `import vyper` /
   `-m pip` probes. **Refuted** — all byte-identical; system python still has neither.
5. **"The venv is not isolated / it reaches back into system or custody state."**
   `sys.path` inspection (single venv site-packages), `include-system-site-packages=false`,
   and an import of a system-only module (`btrfsutil`) → `ModuleNotFoundError`. strace of
   `import vyper`: **zero** opens of any of the 5 custody paths. **Refuted.**
6. **"The receipt-vs-live check is a tautology that would pass even if a path changed."**
   Attempted by injecting a same-content rewrite and a content change on scratch fixtures
   (round-2/3 selftest cases `same-content-rewrite-inplace-ctime-pin`,
   `same-content-rewrite-rename-inode-pin`, `content-drift-detected` all PASS in
   `evidence/selftest.out`). **Refuted** — the instrument's own mutation battery
   discriminates, so the 5/5 MATCH is informative.
7. **"CU-1's own scratch activity perturbed the custody paths."** Verified that the only
   files this seat wrote are under `claims/cross/CU-1/` and that all custody-tool demos ran
   from `/dev/shm/cu1/tool/`. **Refuted.**

**Residual attack that succeeded** (reported, then closed by the landed revision): the
padded-reference attack defeats `--require-paths` as a *coverage* gate at `7cd19c3c…`. This
is C3's residual (c), reproduced here independently; my verdict was that it was **real and
open at the r3 revision**, and that a passing `--require-paths 5` on a non-canonical or
padded reference must not be read as "the 5 custody paths were examined". At the landed r4
revision (`29bb45ae…`) the same attack reads **exit 2** with the coverage line printed — the
residual is closed, and my r3 measurement stands as its before-state. The (c)+(d) compound
survives but is adjudicated in the README (see §3).

One caveat worth flagging to the parent: `.ufo/gates/custody-pair/__pycache__/custody-pair.cpython-314.pyc`
exists (mtime 10:27, r3 window) inside the custody dir. It is git-ignored (`git check-ignore`
confirms `.gitignore:1:__pycache__/`) and was **not** written by this round's custody work:
at the time I measured it, no `.ufo/gates` file had an mtime after 11:00 (the r4 target write
came later, at 11:09). Its presence means a process **imported** `custody-pair.py` as a
module at 10:27 (running it as a script writes no cache for `__main__`); it is a write
inside the custody dir, by a non-round-4 process, and the parent may want the round's census
to account for it explicitly.

---

## 5. Blockers

None for this seat.

**Wheel provenance — closed by triangulation (was open at first write).** I hashed the vyper
wheel body from pip's HTTP cache; seat EX-01 (chain c1, report landed 11:06) independently
downloaded the wheel to `/var/tmp` and re-derived the same digest, byte-identical to PyPI's
declared digest. Three-way agreement on
`3b9671727c888363740dc678e60336759871487d0e4e9fdd973048fa9635c4fd` (my cache body ==
EX-01's download == PyPI declaration; `evidence/cu1-venv-exercise.txt`, and
`claims/c1/EX-01/env-census.txt` §7).

**Independent venv exercise (CU-1 ran the venv, not just inspected it).** Compiling EX-02's
`Smoke.vy` on scratch with the venv's own `vyper` reproduced their bytecode exactly:
`vyper -f bytecode` → `c6f5b7f2…` == their `Smoke.bytecode.hex` (499 B, creation);
`vyper -f bytecode_runtime` → `40650adf…` == their `Smoke.runtime.hex` (339 B, runtime);
`vyper --version` → `0.4.3+commit.bff19ea2`. Selectors recomputed from their ABI with a real
keccak256 (`claims/c1/EX-05/keccak_ref.py`) match their `method-identifiers.txt` on all four
(`increment() 0xd09de08a`, `get() 0x6d4ce63c`, `owner() 0x8da5cb5b`, `counter() 0x61bc221a`).
Note the trap: `-f bytecode` emits *creation* bytecode, which is why it matches
`Smoke.bytecode.hex` and not `Smoke.runtime.hex` — a reader comparing the two without
knowing this would see a spurious "mismatch" (I hit it first pass). Custody paths and system
python re-checked immediately after the compile: unchanged.

Two dependency notes for the parent's record: (i) this report's corroboration is of the
custody half of the cross claim, and it covers **both** revisions — `7cd19c3c…` (the r3
bytes I measured the before-state on) and `29bb45ae…` (the r4 revision that landed at
11:09:25, whose live pair I verified `MATCH 5/5`); the README's later settling does not
affect the tool's verdicts, and the ruling text I cite survives at `9d9400da…`; (ii) sibling
reports read — EX-01 (wheel digest, three-way agreement), EX-02 (install receipt + smoke
artifacts, byte-for-byte reproduced), EX-05 (consumed the venv read-only, took no custody
capture), EX-10 (never accessed custody paths), RV-8 (residuals + r1 drift note, both
reproduced), EX-26 (the (d) ruling's author — its report and the README ruling agree), RV-7
(independent residual matrix; its table matches my before/after rows exactly). None
contradict my measurements.
