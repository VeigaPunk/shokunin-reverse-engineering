# R46W1RegG — three instrument-registry rows (round 46, wave 1, tag `reg-g`)

Seat scope: produce three READY-TO-PASTE rows for the round-46 C2 census, one per
instrument, in the 7-cell house format. Lane root
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Read-only on the lane tree; the only
writes are this report and `R46W1RegG/`.

**Deliverables**

- `.ufo/waves/round-46/w1/R46W1RegG/rows.md` — exactly three table rows,
  sha256 `2b358de9f6401b5e70ad44ca8f6b94db971b08788adc7a60b963ed908a6d8db4`.
- `.ufo/waves/round-46/w1/R46W1RegG/receipt.md` — every command, exit code, stdout sha256,
  UTC.
- `.ufo/waves/round-46/w1/R46W1RegG/receipts/` — raw `commands.tsv`, selftest captures,
  `validate.out`, `audit.out`, `freeze-evidence.out`.

---

## 1. The three rows, verbatim (paste these as-is)

| `tools/round-41/gen-squashfs.py` | probe — deterministic SquashFS v4 writer for the four endian modes le, be, avm and avm-genuine; the carrier generator for the round-41 held-out images | 0=image written with the single summary line wrote OUT N bytes inodes K mode M, or every selftest check passed; 1=a selftest check failed, or the writer raised before writing any image (uncaught KeyError on a missing or non-directory tree, OSError on an unwritable out path, so an input error is not distinguishable from a failed check); 2=argparse usage error (tree or out missing, or an invalid --endian or --comp choice) | python3 -I -B tools/round-41/gen-squashfs.py --selftest — 71 checks, 0 failed, exit 0 on 2026-10-28 | none — byte stability rests on fixed constants in the source (MKFS_TIME 1700000000, UID 1000, block size 4096) plus the selftest's deterministic-rebuild check, never on an in-repo pin file | the out image path given as the second positional only; selftest trees and images under $TMPDIR | kaidoku |
| `tools/round-42/indep-eval-v4.py` | probe — independent evaluator that maps one triage envelope to the round-42 (label, action) step 1-15 classification without invoking the extractor | 0=one record printed or written for the single envelope, or the batch payload emitted for a directory; 1=at least one selftest case failed; 2=usage or I/O error (no envelope and no --envelopes, unreadable or non-object JSON, or a --envelopes path that is not a directory) | python3 -I -B tools/round-42/indep-eval-v4.py --selftest — 45/45 cases, 0 failures, exit 0 on 2026-10-28 | none — the 15-step precedence table and its label-action vocabulary are constants in the source, not a pin file | the --out file only; stdout when --out is absent; selftest needs no writes outside $TMPDIR | kaidoku |
| `tools/round-45/c2-counter.py` | gate — R45-C2 calibration: every instrument listed in the frozen scope file owns a SKILL.md registry row whose verdict cell names 0, 1 and 2 | 0=met (unregistered, thin and scope_size all clean); 1=not met (a scope path unregistered, a thin verdict cell, or scope_size other than 6), and also the exit of an uncaught OSError when --json-out points into a missing directory, so an IO failure is not distinguishable from a scored not-met; 2=could-not-evaluate (unknown revision, freeze not an ancestor of rev, SKILL.md or the scope file absent at rev, or frozen_path_changed) | python3 -I -B tools/round-45/c2-counter.py --selftest — 7 cases, 0 failures, exit 0 on 2026-10-28 | tools/round-45/registry-scope.json (6 paths) with plans/round-45-claims.md as the frozen set | the --json-out file only; selftest fixture repositories under $HYAKU_SCRATCH or $TMPDIR | kaidoku |

The section's header row must be exactly (hyphen, not em dash):

`| tool | gate or probe - purpose | verdict map (exit codes) | self-test command | pinned-value path | write scope | owner |`

with separator `|---|---|---|---|---|---|---|`. Those seven names are
`registry.HOUSE`; any deviation fails clause 2 before a row is even read.

---

## 2. Why each row says what it says — source at the freeze, clause by clause

All three instruments were read at `31820472784284727546808acc31b3ea1e73919b` via
`git show <freeze>:<path>` and are **byte-identical at `31820472`, `50862e4a`, `65678df0` and
`e3dfdbad`** (sha256 prefixes `309c502d`, `7a135dd3`, `50212d0f`), so the freeze ambiguity
reported in §4 F1 does not move any of these rows.

### `tools/round-41/gen-squashfs.py` (651 lines)

- CLI (`:636-651`): two optional positionals `tree` and `out`, `--endian {le,be,avm,avm-genuine}`,
  `--comp {gzip,xz}`, `--selftest`, `--ref-writer`, `--sasquatch`, `--keep`.
- `--selftest` (`:647-648`) `sys.exit(selftest(...))`; `selftest()` prints
  `selftest: N passed, M failed` (`:629`) and returns **1** when anything failed (`:632`),
  **0** otherwise (`:633`).
- No `tree`/`out` → `ap.error(...)` (`:650`) → argparse exits **2**; unknown `--endian`/
  `--comp` value also exits **2** (argparse `choices`).
- Otherwise `build_image(...)` (`:651`) returns `None` → process exits **0**; it prints one
  summary line `wrote <out> N bytes, inodes K mode M`.
- **Documented conflation**: `build_image` raises `ValueError` (`:169`, `:298`) and hits
  `KeyError`/`OSError` on bad inputs, and an uncaught Python exception exits **1** — the same
  code as "a selftest check failed". Measured: missing tree, tree-is-a-file and unwritable
  out path all exit 1 with a traceback (`receipts/receipts-extra.tsv` rows 16-18).
- Pinned-value path: **none**. Byte stability is by construction (fixed `MKFS_TIME`, `UID`,
  block size) plus the selftest's determinism check (`deterministic[...]` cases), not by an
  in-repo pin file; the only sha256s in the file are prose in the docstring.

### `tools/round-42/indep-eval-v4.py` (765 lines)

- Docstring states the contract at `:67-68` — *Exit codes: 0 ok, 1 selftest failure,
  2 usage/IO error* — and the code matches it.
- CLI (`:715-727`): optional positional `envelope`, `--envelopes DIR`, `--out FILE`, `--full`,
  `--selftest`.
- `--selftest` → `return selftest()` (`:723`), which returns `1 if failures else 0` (`:709`).
- Single-envelope and batch paths both wrap `OSError`, `JSONDecodeError`, `ValueError` and
  return **2** (`:734`, `:749`); the no-mode fallthrough prints usage to stderr and returns
  **2** (`:759-761`). Success returns **0** (`:738`, `:753`).
- Discipline is clean here: every malformed input I tried — no args, missing file, non-JSON,
  JSON array, `--envelopes` on a non-directory — exits **2**, never a traceback
  (`receipts/receipts-extra.tsv` rows 19-21). A bare data object (`{"operation":"x"}`) is
  deliberately accepted and scored `unclassified`, exit 0.
- Pinned-value path: **none** — the 15-step precedence table and the label/action vocabulary
  are constants in the source.

### `tools/round-45/c2-counter.py` (268 lines)

- Docstring `:11-13` states *0 met; 1 not met; 2 could-not-evaluate (unknown revision, freeze
  not an ancestor, SKILL.md or the scope file absent, frozen_path_changed for a commit inside
  FREEZE..REV touching the claims file or `tools/round-45/`)*.
- `evaluate()` returns **2** for: unknown freeze/rev (`:73`), freeze not an ancestor (`:77`),
  `git log` failure (`:80`), `frozen_path_changed` (`:82`), scope file absent (`:86`),
  scope unreadable (`:90`), `SKILL.md` absent (`:93`).
- It returns **0** when the reason list is empty and **1** otherwise (`:129`); the receipt
  carries `met_target = not reasons`.
- `main()`: `--selftest` → `run_selftest()` (`:251-252`); missing `--root/--freeze/--rev`
  prints a `could_not_evaluate` JSON line and returns **2** (`:253-256`).
- **Documented conflation**: `--json-out` into a missing directory raises `FileNotFoundError`
  at `:260-262`, so it exits **1** — indistinguishable from a scored not-met. Measured
  (`receipts/receipts-extra.tsv` row 24).
- Pinned-value path: `tools/round-45/registry-scope.json` (the 6-path scope). Write scope:
  `--json-out` only, plus fixture repos the selftest creates under `$HYAKU_SCRATCH`/`$TMPDIR`.

---

## 3. Verification actually run (not "should pass")

`python3 -I -B` throughout, `TMPDIR=$HYAKU_SCRATCH=<scratch>`, cwd = lane root, lane tree
untouched (no `__pycache__`).

| instrument | probe | exit |
|---|---|---|
| gen-squashfs | `--selftest` → `selftest: 71 passed, 0 failed` | **0** |
| gen-squashfs | `--endian bogus` | **2** |
| gen-squashfs | no `tree`/`out` | **2** |
| gen-squashfs | `--help` | **0** |
| gen-squashfs | build a 1-file tree → `wrote … 265 bytes, inodes 3 mode le` | **0** |
| indep-eval-v4 | `--selftest` → `45/45 cases; 0 failure(s)` | **0** |
| indep-eval-v4 | `--help` / empty `--envelopes` dir | **0** |
| indep-eval-v4 | no args / missing file / non-JSON / JSON array / `--envelopes` on a file | **2** |
| c2-counter | `--selftest` → `C2_SELFTEST: cases=7 failures=0` | **0** |
| c2-counter | no args | **2** |
| c2-counter | unknown rev; freeze not an ancestor | **2** |
| c2-counter | read-only score of the real lane at `FREEZE=31820472 --rev 8757865679e62` (the HEAD when run) | **0** (`met_target true`, 45 rows; round-45's own frozen set is `plans/round-45-claims.md` + `tools/round-45/`, so round-46's freeze touch does not affect it) |

**Row format verified by the frozen scorer itself**, not by eye.
`receipts/validate.out` imports `tools/round-46/registry.py` from a scratch copy and calls
`score(skill, files, "r46", "v2", rev, battery=None)`:

- census = only my three paths → exit **0**, `registered` = all three, `unregistered []`,
  `thin []`, `absent_at_rev []`, `failing []`, header accepted.
- census = all 38 frozen paths, only my three rows present → exit **1** with the single
  clause `unregistered: 35 of 38` — proof that my three are counted and satisfy clauses 3/4/5,
  and that the other 35 are the rest of the wave's work, not a defect in mine.
- Re-run against `registry.py` from `65678df0` (the bytes the lane actually measures with;
  `50862e4a`→`65678df0`→`e3dfdbad` are identical for this file): exit **0**, same receipt.
  The only `registry.py` change `31820472`→`50862e4a` is in `evaluate()`'s battery ordering
  (`git diff --stat` = 8 insertions, 4 deletions, one hunk); `score()` — the clause set my
  rows are judged by — is unchanged.

`receipt.md` carries the full `utc | exit | stdout-sha256 | command` table
(`receipts/commands.tsv`, sha256 `b8dd9059fd9bb953faa902e2af867e6412adb36e971e7e27d356234de576550e`).

---

## 4. Findings for the L1

### F1 (blocking for C2, mechanical): the stated freeze cannot be scored — the measured freeze is `65678df0`

The prompt (and `plans/round-46-claims.md`) name
`31820472784284727546808acc31b3ea1e73919b`. But `tools/round-46/` was touched by **three**
commits after it:

```
$ git log --format='%H %s' -- tools/round-46/
65678df0 round-46 F3: the freeze is the instrument that can actually be scored — …
50862e4a round-46: complete the freeze — … declared as the authoritative freeze …
31820472 round-46: freeze — …
```

`gate.freeze_state` (bytes at `65678df0`), read-only:

```
[FREEZE=31820472 REV=31820472]        exit=0
[FREEZE=31820472 REV=50862e4a]       exit=2  reason: frozen_path_changed
[FREEZE=31820472 REV=HEAD(e3dfdbad)] exit=2  reason: frozen_path_changed
    frozen_path_changed: ['tools/round-46/', 'tools/round-46/attest.py',
                          'tools/round-46/gate.py', 'tools/round-46/registry.py']
    blob_changed: ['tools/round-46/']   restored: the three files
[FREEZE=65678df0 REV=HEAD]            exit=0
```

So a score at any `REV >= 50862e4a` with `--freeze 31820472` exits **2
`frozen_path_changed`** and prints no `met_target` — a 2 never counts, so the C2 target is
unreachable with the prompt's freeze value. `65678df0 ... --rev HEAD` is clean (exit 0).
The lane has already moved here in substance: `6e018068` ("A2: re-pin block 23 to the
measured freeze's interpreter bytes (65678df0)"). The claims file's own derivation line —
*`git log --format=%H -1 -- plans/round-46-claims.md` re-derives it* — returns `31820472`
(the claims file is only ever in that one commit), i.e. **the stated derivation rule yields
the unscorable commit**. Reported, not fixed.

### F2 (blocking for C2, format): the six already-landed round-44/45 rows are thin under v2

Measured with the frozen scorer, using the six rows as they stand in `SKILL.md` today:

```
exit=1  thin: [all six]  failing: ['thin verdict-map cells: 6']
```

The landed cells read `` `0` met; `1` not met; `2` could-not-evaluate ``, while v2's
`EXITMAP = re.compile(r"\b([012])\s*[=:]")` requires `0=`/`1=`/`2=`. Wrapping the existing
`### Round-44/45 instrument registry` section in the v2 markers verbatim therefore lands
**six thin rows** and the target fails. Those six must be rewritten in the `=` style, exactly
like my three rows.

### F3 (blocking for C2, shadowing): `tools/round-45/c2-counter.py` already has an exact-cell-0 row

`SKILL.md:1677` is `| \`tools/round-45/c2-counter.py\` | … | \`0\` met; … |` in the old
section. `rows_in_section` only reads between the markers, so it is invisible to v2 as long as
it stays outside — but `by_path.setdefault(...)` means **the first row for a path wins**. If
that old row is copied into the new section ahead of mine, it is thin and shadows my correct
row, and the file still reports 38 registered rows. Paste my row (or a `=`-formatted
rewrite), do not copy the line at `:1677`.

### F4 (calibration): two of the three instruments conflate "not met" with "could not evaluate"

- `gen-squashfs.py`: missing tree, tree-is-a-file, unwritable out path → uncaught
  `KeyError`/`OSError` → **exit 1**, i.e. the same code as a failed selftest check.
- `c2-counter.py`: `--json-out` into a missing directory → uncaught `FileNotFoundError` →
  **exit 1**, i.e. the same code as a scored not-met.
- `indep-eval-v4.py` is disciplined: every IO/usage path is **2**.

Both conflations are stated inside the `1=` cell of the affected rows rather than hidden, so
the registry does not advertise a cleaner contract than the tool has. If the L1 would rather
tighten the instruments than document the conflation, that is an instrument change and must
not land inside the frozen directory before scoring.

### F5: no instrument reaches an exit code outside {0,1,2}

Every argument, input and IO path I could reach yields 0, 1 or 2. (Interpreter-level codes
such as 130 under SIGINT are not part of any tool's contract and are out of scope.)

### F6: `gen-squashfs.py --selftest` stdout is not byte-stable

It prints the randomised `tempfile.mkdtemp` path, so two identical runs give different
stdout sha256 (`4edff26e…`, `113ef98b…`). A stdout sha is a *run receipt*, never a pin; the
stable evidence is the line `selftest: 71 passed, 0 failed`. The other two instruments'
selftest output is stable apart from scratch paths in the c2-counter fixture dump.

### F7: census provenance for my three paths

The three paths are named in their own frozen claim files — `git show <freeze>:<claims> |
grep -c <name>` gives `plans/round-41-claims.md` 3, `plans/round-42-claims.md` 2,
`plans/round-45-claims.md` 4 — and all **38** census paths exist at `e3dfdbad` (checked with
`git cat-file -e`), so clause 5 cannot fail for any of them at the current rev.

---

## 5. Limits of this seat's evidence

- **Not run**: the round-46 C2 target itself. Only 3 of the 38 census paths have a row from
  me; clause 3 needs all 38. Receipt B quantifies exactly what remains: `unregistered: 35 of 38`.
- **Not run**: `registry.py`'s seven-forgery battery (clause 6). It needs a complete artefact
  to mutate; there is no marker-bound section in `SKILL.md` yet (`grep instrument-registry`
  → no match).
- **Not run, not my surface**: `tools/round-46/attest.py`, `SKILL.md` block 23 and R46-C1.
- **Not verified**: the exit meanings of the other 35 census instruments — other seats' rows.
- No package was installed; `python3`, `git` and the existing
  `sasquatch`/`sasquatch-v4be` binaries in `~/.local/bin` were sufficient. Nothing was
  written to `/tmp`, `~/.local/bin`, `.ufo/state/`, `.ufo/watchdog.log` or `.scratch/`.

## 6. Read-back check of my own file

`receipts/audit.out` re-reads `rows.md` and reports, per row: `cells=7`,
`backticks=2` (the cell-0 path and nothing else), `cell0_ok=True`,
`exitmap=['0','1','2']` — and the frozen scorer independently reaches exit 0 on a 3-path
census with `thin []`. No literal `|` occurs inside any cell (a `|` would split the row and
`cells` would exceed 7).

## 7. Read-only attestation

No mutating git/jj command was run in the lane: only `rev-parse`, `log`, `show`, `cat-file`,
`diff`, `diff --stat` and `status --porcelain`. `tools/round-46/` and
`plans/round-46-claims.md` were copied out of the object store, never edited. Scratch
`/fast/scratch/hyaku/kaidoku-r46/R46W1RegG` was removed after the receipts above were copied
into `R46W1RegG/receipts/`.
