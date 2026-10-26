DEFECTS FOUND — the three patched copies are byte-for-byte behaviour-identical to the round-38 tools on every recorded receipt (18/18 parity runs, 0 mismatches) and their `--selftest` modes land at 8/8 (freeze-drift) and 9/9 (intended-doc), but `registry-immutable.sh` **cannot** reach the assigned 4/4: its run mode reports exit 0 for both a deleted registry row and a reordered registry, measured on fixtures, not inferred. A 14-line variant that closes both gaps is supplied, proven 5/5 and receipt-identical; taking it is an L1 decision because it changes run-mode exit codes.

Seat: `R39CL2Selftests` (round 39, wave 1, pre-freeze). Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, base `a2f64e1da78afcf8cc39287106604dbcc270844c`. Items under test: `tools/round-38/freeze-drift.py` (sha256 `0f778d48d9925e66dde7ec53ca1d346581f2bcff9a31d6336984bccda1cde27b`), `tools/round-38/intended-doc.py` (`0a1fc3a4794abbac2dbab5187d417db571c577bd9c95fc20207ba76ffa9bb974`), `tools/round-38/registry-immutable.sh` (`2595a3970f5ccade5a7d73a378214f1213b16c21b66686d7b345b1e50314d47c`). Host tools: git 2.56.0, Python 3.14.8, GNU bash 5.3.20, GNU Awk 5.4.1. Nothing installed or upgraded; no VCS mutation; every lane file untouched.

## 1. What was written, and what the diff is

Four scripts plus evidence land only under `.ufo/waves/round-39/w1/artifacts/R39CL2Selftests/` (inventory and `MANIFEST.sha256` in §8). The assigned names are the three patched copies; `registry-immutable.fixed.sh` is an **extra, clearly labelled variant** (§5) and `parity-all.sh` is the reproduction harness.

| file | vs lane tool | diff | run-mode change |
|---|---|---|---|
| `freeze-drift.py` | `tools/round-38/freeze-drift.py` | `+151 −1` (`diff-freeze-drift.diff`) | import line gains `os, shutil, tempfile`; `main()` gains two lines (`argv` normalisation + `--selftest` branch). The drift algorithm, exit codes, `DEFAULT` set and `--json-out` writing are untouched. |
| `intended-doc.py` | `tools/round-38/intended-doc.py` | `+141 −1` (`diff-intended-doc.diff`) | same shape: import line, `os/re/shutil/tempfile`, two-line `--selftest` branch. The row parse, `TOKEN` regex, reason strings and exit codes are untouched. |
| `registry-immutable.sh` | `tools/round-38/registry-immutable.sh` | `+76 −0` (`diff-registry-immutable.diff`) | **no existing line changed.** A `--selftest` block is inserted above `lane=$1 …`; the `rows()` function and the `awk` comparison are byte-identical. |
| `registry-immutable.fixed.sh` | `registry-immutable.sh` (patched) | `+14 −2` (`diff-registry-minfix.diff`) | the variant only: `awk` gains deletion and reorder detection (§5). |

The Python additions are a docstring paragraph, an `argv` normalisation, one `if '--selftest' in argv: return selftest()`, a fixture builder, a case runner and a `finally` cleanup. Each selftest re-invokes **its own file** as a child process (`sys.executable -I -B <tool> <args>` / `bash <tool> …`), so the cases exercise the real argv parsing, real stdout and the real exit-code path — not an in-process shortcut.

## 2. `--selftest` results (logs in the artifacts dir)

```
$ python3 -I -B freeze-drift.py --selftest          # selftest-freeze-drift.log, rc=0
case clean-history: expect exit=0 got 0 PASS
case counter-edited-after-freeze: expect exit=1 got 1 PASS
case non-ancestor-range: expect exit=2 got 2 PASS
case glob-path-edited: expect exit=1 got 1 PASS
case unknown-revision: expect exit=2 got 2 PASS
case json-out-parity: expect exit=1 got 1 PASS
case empty-range: expect exit=0 got 0 PASS
case default-path-set: expect exit=1 got 1 PASS
SELFTEST cases=8 pass=8 fail=0

$ python3 -I -B intended-doc.py --selftest            # selftest-intended-doc.log, rc=0
case bound: expect exit=0 got 0 PASS
case pointer-names-another-path: expect exit=1 got 1 PASS
case stub-at-intended-path: expect exit=1 got 1 PASS
case intended-path-missing: expect exit=1 got 1 PASS
case intended-doc-edited-after-base: expect exit=1 got 1 PASS
case duplicate-unit-rows: expect exit=1 got 1 PASS
case unit-row-absent: expect exit=1 got 1 PASS
case file-absent-at-base: expect exit=2 got 2 PASS
case unknown-revision: expect exit=2 got 2 PASS
SELFTEST cases=9 pass=9 fail=0

$ bash registry-immutable.sh --selftest               # selftest-registry-immutable.log, rc=1
case append-only: expect exit=0 got 0 PASS
case in-place-cell: expect exit=1 got 1 PASS
case row-deletion: expect exit=1 got 0 FAIL
  - exit 0 != 1; output does not contain 'S003'
case row-reorder: expect exit=1 got 0 FAIL
  - exit 0 != 1; output does not contain 'S001'
case allowed-cells: expect exit=0 got 0 PASS
SELFTEST cases=5 pass=3 fail=2

$ bash registry-immutable.fixed.sh --selftest         # selftest-registry-immutable.fixed.log, rc=0
SELFTEST cases=5 pass=5 fail=0
```

Every case is a green **and** a red one: each suite contains at least one construct that must exit non-zero and at least one that must exit 0, so a tool stuck at either answer fails. Each fixture is one `git init` repo under `$TMPDIR` (`mktemp -d …/fx.XXXXXX`), built with `git -C "$D" -c user.name=fx -c user.email=fx@fx -c commit.gpgsign=false`, toplevel verified against `pwd -P` before the first commit, removed in a `trap`/`finally`. A run leaves no `fx.*` directory behind (measured: `ls -d "$TMPDIR"/fx.*` → 0 after the suite). No lane path is read or written by any fixture. With `TMPDIR` unset the suites fall back to the platform temp root and still pass (8/8, 9/9, 5/5, rc 0, no `/tmp/fx.*` left), so an L1 run does not depend on the seat's environment.

**The required constructs map exactly onto the brief**: freeze-drift clean 0 / counter edited 1 / non-ancestor 2 / glob path edited 1; intended-doc bound 0 / not-bound 1 / stub-at-path not-bound 1 / missing path 1; registry append-only 0 / in-place cell edit 1 / row deletion 1 / reorder 1. The three extra freeze-drift cases (`unknown-revision`, `--json-out` parity, `empty-range`) and two extra intended-doc cases (`duplicate-unit-rows`, `unit-row-absent`) close argv paths the four required cases would leave unexercised; the extra registry case (`allowed-cells` = status/recheck/used-by, the three columns the rule permits) is what keeps the red cases from being satisfiable by a tool that rejects every change.

## 3. The selftests can fail (mutation evidence)

Each suite was run against a deliberately broken copy of its own tool (scratch only, logs `mutation-*.log`):

| mutant | edit | result |
|---|---|---|
| freeze-drift | `finish(…, 1 if drift else 0)` → `finish(…, 0)` | `SELFTEST cases=8 pass=4 fail=4`, rc 1 — the three drift cases plus `default-path-set` go red |
| intended-doc | the `a.intended not in toks` check forced to `False` | `SELFTEST cases=9 pass=8 fail=1`, rc 1 — `pointer-names-another-path` goes red |
| registry-immutable | the exempt-column tuple also exempts column 6 (scope) | `SELFTEST cases=5 pass=2 fail=3`, rc 1 — `in-place-cell` joins the two known gaps |
| registry-immutable.fixed | the deletion `print …; hit=1` body emptied (syntax kept) | `SELFTEST cases=5 pass=4 fail=1`, rc 1 — only `row-deletion` goes red |

The first `registry` mutant I tried (start the column loop at 3 instead of 2) was **not** discriminating — column 2 is the row id, which is the comparison key and can never differ — so it was replaced by the scope-column mutant above. Reporting that here rather than hiding it: a mutant that leaves the suite green is evidence about the mutant's reach, not about the suite.

## 4. Unpatched behaviour is unchanged on the round-38 receipts

`parity-all.sh` re-runs every round-38 `l1` receipt argv against **both** the lane tool and the artifact copy and diffs stdout and exit code (`parity-all.log`):

```
parity fd-final      rc=1 stdout=identical     parity id-base    rc=1 stdout=identical
parity fd-0fc61133   rc=1 stdout=identical     parity id-final   rc=0 stdout=identical
parity fd-077e212b   rc=1 stdout=identical     parity id-0fc61133 rc=0 stdout=identical
parity fd-cb4326b2   rc=0 stdout=identical     parity id-s2      rc=0 stdout=identical
parity fd-genctrl    rc=1 stdout=identical     parity id-s2-hist rc=0 stdout=identical
parity rm-atfinal   rc=0 stdout=identical      parity rm-0fc61133  rc=1 stdout=identical
parity rm-base      rc=0 stdout=identical      parity rmfix-*      3× identical (variant)
parity usage-freeze-drift  rc=2 stdout+stderr=identical (no-argument usage path)
parity usage-intended-doc  rc=2 stdout+stderr=identical (no-argument usage path)
PARITY cases=18 mismatches=0
```

So on every recorded argv the patched copies print exactly what the lane tools print and exit with the same code — including the no-argument usage path (identical argparse message and rc 2, a spot an added flag could have broken).

Against the committed receipts themselves:

| receipt | verdict |
|---|---|
| `freeze-drift-final.json`, `freeze-drift-0fc61133.json` | byte-identical to the patched stdout |
| `freeze-drift-077e212b.json`, `freeze-drift-cb4326b2.json`, `freeze-drift-gen-controls.json` | identical after dropping `net_changed`/`ships_freeze_bytes`; these three receipts predate the commit `7a1ac7fe` that added those keys, and the same delta appears for the **unpatched** tool (parity row above), so it is receipt age, not patch drift |
| `intended-doc/base.json`, `final.json`, `landed-0fc61133.json` | byte-identical to the patched stdout |
| `registry-immutable/{at-final,at-0fc61133,base-vs-base}.txt` | body identical to the patched stdout; those files carry a trailing `exit N` line the tool never prints, and that N equals the tool's rc (0 / 1 / 0) |

`intended-doc/shortcut-s2.json` is the one receipt that does **not** reproduce, and it does not reproduce for the unpatched tool either (parity `id-s2` is identical). It records `"rev": "HEAD"` and `"verdict": "not-bound"` with reason `intended path not named in the unit row`; today both binaries at `HEAD` print `bound`/rc 0, because the `REA MCP server` row has named `.ufo/waves/round-19/evidence/doctor/` since `279e8b19` (2026-10-20), and it also already named it at `e265533e`, the commit that was `HEAD` when the receipt was written (`2026-10-26T03:53` vs receipt mtime `04:05`). A `--rev HEAD` receipt cannot be re-derived from the lane at any round-38 revision, so the S2 run must have used a doctored or non-lane `PROVINCE.md` (its own report, `.ufo/waves/round-38/w2/R38W2C2Controls.md:156`, says "`PROVINCE.md` still reads `doctor outputs in `evidence/doctor/``", which is not the lane text). [INFERENCE] the S2 receipt is a demonstration artefact, not a lane measurement; it is already flagged as a floating-revision receipt by `.ufo/waves/round-38/w2/R38W2Sentinel.md:123`. QUALITY 81 cites this file, so the L1 should know it is not reproducible as recorded.

## 5. Defect: `registry-immutable.sh` cannot see a deleted or reordered row

Measured on fixtures (§2), and directly from the source: the `awk` program iterates **rev** rows only (`NR==FNR` fills `b[id]` from base, then every rule fires inside the rev-row branch). A base row that no longer exists at REV is therefore never examined, and matching is keyed by id, so relative order is never compared. Both are append-only violations under `CORPUS.md` SOURCES rule 2 (round-38 M38-8's own rule), and both are in the brief's required case list. **No behaviour of the shipped `registry-immutable.sh` was changed to hide this** — the required copy keeps the round-38 run mode byte-identical, so its selftest is honestly red (3/5, rc 1).

`registry-immutable.fixed.sh` closes exactly those two gaps, in the same `awk` pass, adding nothing else:

```
  END { for (i=1;i<=nb;i++) if (!(order[i] in seen)) { print order[i], "row deleted (append-only)"; hit=1 }
        j=0
        for (i=1;i<=nb;i++) if (order[i] in seen) common[++j]=order[i]
        for (i=1;i<=nr;i++) if (revorder[i] != common[i])
          { print order[i] " / " revorder[i], "row reordered (append-only)"; hit=1; break }
        exit hit ? 1 : 0 }
```

The reorder test compares the surviving rows' relative order only (base ids present at REV, in base order, against REV order filtered to ids present at base), so it cannot fire spuriously when a row is appended at the end or deleted — the deletion case is reported by the first line alone. Evidence that the variant is safe to take:

- `SELFTEST cases=5 pass=5 fail=0`, rc 0.
- The three round-38 registry receipts reproduce exactly: `77091b49..7a1ac7fe` → rc 0 no output; `77091b49..0fc61133` → `S110 changed columns: 6`, rc 1; `77091b49..77091b49` → rc 0 no output (`parity rmfix-*`, 3/3 identical to the unpatched tool).
- The appended-row case is still 0 (no false positive on the legal edit).

**Decision for L1, not for me:** taking the variant changes run-mode exit codes on inputs the round-38 tool accepted (deleted/reordered rows), which the brief forbade in the assigned copy. If L1 admits the gap as a known limitation, keep `registry-immutable.sh` and its red selftest as the standing statement of it; if L1 authorises the fix, replace the tool with `registry-immutable.fixed.sh` under the same name and re-run the three receipts (already reproduced). Either way the selftest must not be relaxed to make the assigned copy green — that would encode the gap as the contract.

## 6. Limits

- Fixtures are git-version-bound (git 2.56.0, Python 3.14.8, gawk 5.4.1); the freeze-drift cases do not touch the known D1/D2/D3/D5 escapes from `.ufo/waves/round-38/w2/R38W2FreezeDriftFixtures.md` (evil merge restoring freeze bytes, `--root` at a subdirectory, non-recursive oracle glob, silent unmatched path). Those are unchanged by this seat and remain the fixtures seat's findings; the new suite deliberately does not assert on them, because asserting the current answers would freeze the defects and asserting the correct answers would fail the suite for reasons outside this ticket.
- The selftests cover argv, exit-code and JSON-shape contracts, not performance or concurrency; `--json-out` parity is asserted only for freeze-drift (the other two print to stdout only).
- `intended-doc`/`registry-immutable` cases use a single fixture repository each; no case exercises a bare or shallow repo (freeze-drift's shallow-clone behaviour is covered by the round-38 fixtures seat, not here).
- No build, lint, formatter or lane gate was run: this seat is a leaf in an editing wave and the parent owns post-integration gates.
- Scratch `/fast/scratch/hyaku/kaidoku-r39/R39CL2Selftests` removed after the runs; every cited log is in the artifacts dir with a sha256 in `MANIFEST.sha256`.

## 7. Reproduction

```
S=/fast/scratch/hyaku/kaidoku-r39/R39CL2Selftests; mkdir -p "$S"; export TMPDIR="$S"
A=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-39/w1/artifacts/R39CL2Selftests
cd "$S"
python3 -I -B "$A/freeze-drift.py" --selftest ; echo rc=$?     # 8/8, 0
python3 -I -B "$A/intended-doc.py" --selftest ; echo rc=$?     # 9/9, 0
bash "$A/registry-immutable.sh" --selftest ; echo rc=$?        # 3/5, 1
bash "$A/registry-immutable.fixed.sh" --selftest ; echo rc=$?  # 5/5, 0
bash "$A/parity-all.sh" ; echo rc=$?                           # cases=18 mismatches=0, 0
```

## 8. Files changed

Only under `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-39/w1/` — this report plus `artifacts/R39CL2Selftests/`:

`freeze-drift.py` · `intended-doc.py` · `registry-immutable.sh` (assigned, behaviour-preserving) · `registry-immutable.fixed.sh` (optional variant, §5) · `parity-all.sh` · `parity-all.log` · `selftest-freeze-drift.log` · `selftest-intended-doc.log` · `selftest-registry-immutable.log` · `selftest-registry-immutable.fixed.log` · `mutation-freeze-drift.log` · `mutation-intended-doc.log` · `mutation-registry-immutable.log` · `mutation-registry-immutable.fixed.log` · `diff-freeze-drift.diff` · `diff-intended-doc.diff` · `diff-registry-immutable.diff` · `diff-registry-minfix.diff` · `MANIFEST.sha256`.

`git -C <lane> status --porcelain` before and after this seat shows only the pre-existing untracked `.ufo/waves/round-39/` and `plans/round-39-claims.md`; no `tools/`, `corpus/`, `plans/`, `PROVINCE.md`, `SCORECARD.md`, `SHONEN.md`, `SKILL.md` or `LOG.md` write; no VCS mutation; no file outside the lane; no install or upgrade.
