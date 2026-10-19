# RV-6 — seat report (chain c3, reviewer)

Wave `arc3-loop1-round4` · seat RV-6 · 2026-10-19 · repo
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin` · HEAD `015e1ba` (the landing is
in the worktree, uncommitted: `git status --porcelain .ufo/gates/` → ` M
.ufo/gates/custody-pair/{custody-pair.py,README.md}`; the commit is the parent's).
Lane: devin (the declared fallback — the hyper lane returned 402 out-of-credits on
the whole roster; recorded in `claims-frozen.md`, not a lane signal).

Task: code-review the three closures in the landed tool — correctness, declared
classes reachable, no regressions.

**Verdict: PASS on all three closures — each is correct, reachable as its
declared class, and load-bearing. No regression found on any of the 33 battery
arms or 17 attack vectors. One coverage finding (M5): the `--out`-with-no-usable-name
guard is load-bearing but has no case in the shipped selftest — EX-27's
independent harness catches it, the tool's own 28-case suite does not.**

No git mutation. Scratch `/var/tmp/rv6/w4`; `/tmp` never used. Custody paths
opened for reading only. This seat wrote only `seats/RV-6.md` and
`claims/c3/RV-6/`.

## Revisions under measurement (identity, re-derived)

| object | revision | lines / bytes |
|---|---|---|
| tool BEFORE | `7cd19c3cfd835c7807d5e60dece1c2592c9df6c319a78deb14469dd6ebe8ab09` | 1155 / 54279 |
| tool AFTER | `29bb45ae0fd795e54e85d8749a163159aead181b42e9d3af399326b968b30acf` | 1343 / 65902 |
| README AFTER | `9d9400dab7ff7072375c13fad43c02dde0f3923a58cf3af0d50fa3384535022a` | 272 / 15293 |
| SKILL.md | `5eec51c089e57f5d5806b4728261fb8c959637580a73aed7be4cddc1866b8f3f` | 390 |

The BEFORE copy was taken at 14:04Z while the worktree tool was still
`7cd19c3c…` (measured, not assumed). The AFTER pair was stable across five 20 s
samples (14:12:17–14:13:37Z) and re-derived again at 14:14Z and at write time.

## 1. Work performed (evidence pointers)

All artifacts under `.ufo/waves/arc3-loop1-round4/claims/c3/RV-6/`:

| artifact | role |
|---|---|
| `probe.py` (`ee5806e8…`) | revision-agnostic injection probe: the three residuals + selftest + live pair |
| `battery.py` (`af32e3e0…`) | 33-arm battery: every declared class 0/10/11/12/13/14/2/3, the closures, the r2/r3 guard regressions, live pair, sidecars, self-pin, selftest |
| `before-battery.json` / `after-battery.json` | the two runs (`9975cd46…` / `884895d7…`) |
| `before-probe.json` / `after-probe.json` | the two probe runs (`6e03138f…` / `98862f01…`) |
| `before-battery.out`, `after-battery.out`, `before-probe.out`, `after-probe.out` | raw transcripts |
| `arm-diff.txt` (`35f3b058…`) | the 33-arm before→after table |
| `sabotage-arms/*.py` | five scratch reverts (M1 coverage basis, M2 mkdir guard, M3 sidecar arm, M4 neighbour arm, M5 empty-`--out` guard) |
| `m5-finding.txt` (`61e7a0b9…`) | the M5 transcript: landed vs sabotage vs base, in-tool selftest, EX-27's harness |
| `report.md` | the full review write-up (this file is its seat-report form) |

Commands run: `python3 probe.py <tool> <scratch> <outdir>` and
`python3 battery.py <tool> <scratch> <outdir>` against both revisions; the five
sabotage copies through `selftest`; EX-27's `regress-r4.py` (sha
`57f04e349240beeceed8d68fe7497e9d694eda0d702cffd9567c8bb4011e1c94`) run by this
seat in `--phase r4` and `--phase r3`, against the landed bytes and against the M5
sabotage copy; `sha256sum` over every digest-bearing line of EX-21's `sha256s.txt`.

## 2. Proposed changes

**None applied by this seat** (reviewer; writes no tool code, README, or SKILL).
One patch shape is proposed as text in §4 (M5): a single selftest case
`out-with-no-usable-name-usage-exit`. Apply decision belongs to EX-21 / the parent.

## 3. Before → after measurement for the chain's claim

Frozen claim (C3): (a)-(c) closed with declared classes, selftest 22 → ≥24 with
new fixtures + sabotage arms; (d) adjudicated with the ruling text in the README;
registry row + README re-derived same-commit; the round's live pair (revised tool)
verifies MATCH 5/5; every receipt self-pins the new tool sha256; command A unchanged.

| leg | before (`7cd19c3c`) | after (`29bb45ae`) | verdict |
|---|---|---|---|
| **(a)** `capture --paths vic.sha256 --out vic` | exit **0**; `SIDECAR: …/vic.sha256`; victim sha `140aba39…` → `5dbcef16…` (**destroyed**) | exit **2**; USAGE refusal naming the sidecar; victim sha `140aba39…` **unchanged** | **CLOSED** |
| **(a2)** second spelling `--paths vic2.sha256 --out vic2` | exit 0, clobbered | exit 2, intact | **CLOSED** |
| **(a3)** ordinary `--out` still writes its sidecar | exit 0, sidecar present | exit 0, sidecar present | no regression |
| **(b)** `--out <regular-file>/sub/r.txt` | **`NotADirectoryError` traceback, exit 1** | exit **2**, `USAGE: cannot create the receipt directory ([Errno 20] …)`, no traceback, no partial receipt | **CLOSED** |
| **(b2)** `--out ''` | exit 2 (`Is a directory: '.'`) | exit 2, `USAGE: --out carries no usable name …` | preserved (better message) |
| **(b3)** read-only parent dir | traceback, exit 1 | exit 2, USAGE | **CLOSED** |
| **(b4)** legal nested `--out` | exit 0, created | exit 0, created | no regression |
| **(c)** 5× duplicate stanza, `--require-paths 5` | exit **0**, `VERDICT: MATCH paths=1`, **no coverage line** | exit **2**, `REFERENCE-COVERAGE: 1/5 …`, `USAGE: reference covers 1 of the required 5 distinct paths` | **CLOSED** |
| **(c2)** 5 distinct non-canonical paths | exit 0 | exit 0 (count-gate semantics, unchanged) | unchanged |
| **(c3)** canonical 5 under the gate | exit 0 | exit 0 | no false positive |
| **(c4)** 1-of-5 under the gate | exit 2 | exit 2, same line | preserved |
| **(c5)** no flag (declared default) | exit 0, no gate | exit 0, no gate | unchanged |
| **(d)** both-absent MATCH | reproduced first-hand: `MATCH 1/1 exit 0`, `SHA256-CONTRACT: 0/0` | `MATCH 1/1 exit 0` **plus** the row note `both sides record the path absent — the MATCH is an agreement on absence…`; ruling text in README §"The both-absent `MATCH`" (detector hits 10) | **adjudicated + annotated** |
| selftest | `CLEAN cases=22 passed=22 failed=0` | `CLEAN cases=28 passed=28 failed=0` | 22 → 28 (claim: ≥24) |
| live pair, landed tool | — | `MATCH paths=5/5 drift=0 exit=0`, identical under `--require-paths 5`; both sidecars `sha256sum -c` OK | **MATCH** |
| receipt self-pin | — | `# tool: … sha256 29bb45ae…` == independent `sha256sum` | **pinned** |
| declared classes 0/10/11/12/13/14/2/3 | all reachable | all reachable | unchanged |
| command A | — | the recipe reads Git objects under `corpus/knowledge` + `corpus/README.md` + `SKILL.md`; `.ufo/gates/` is outside its read set; SKILL.md `5eec51c0…` unchanged | **unaffected** |
| registry row (patch text) | — | `skill-registry-row.patched.md` 390 lines == `SKILL.md` 390; one row replaced | **line-neutral** |

Battery summary: base `arms=33 hold=27 fail=5` — the 5 failures are exactly the
three declared residuals (a, a2 / b, b3 / c1). Landed `arms=33 hold=32 fail=0`
(one informational `n/a` row). The claim's "before" is therefore reproduced, not
accepted on trust, and every failing arm flipped.

## 4. Attacks / refutations attempted, with verdicts

| # | attack | verdict |
|---|---|---|
| A1 | the sidecar arm is a literal-string check a second spelling defeats | **REFUTED** — `--paths X.sha256 --out X`, `--paths X --out X.sha256`, and `./`-relative spellings all refused; the guard compares *resolved* paths plus the inode arm |
| A2 | the derived sidecar can still land on a measured file via a hardlink alias | **REFUTED** — pre-created `rec.txt.sha256` as a hardlink of the measured file: exit 2, refusal names the sidecar, both names keep sha `1b23b207…`, same inode throughout |
| A3 | a symlinked `--out` defeats the resolved-path arm | **REFUTED** — exit 2, target intact |
| A4 | the neighbour arm covers only one level (`--paths X.sha256 --out X.sha256.sha256`) | **REFUTED** — exit 2 |
| A5 | the custody paths' `.sha256` neighbours are unguarded (`--out ~/.bashrc.sha256`) | **REFUTED** — exit 2 |
| A6 | the new guard is over-broad and breaks legitimate use | **REFUTED** — `--out legit-name.sha256` (no conflict), `--out -`, relative `--out`, nested `--out` all succeed; `--out -` writes no sidecar, as before |
| A7 | the mkdir guard closes one errno and leaves others (ELOOP, EACCES, existing dir, `..`, `/`) | **REFUTED** — every vector is a declared USAGE exit 2 with a message, zero tracebacks |
| A8 | the coverage fix breaks the r3 D3 close or the declared default | **REFUTED** — 1-of-5 under the gate still exit 2 with the same line; no flag still ungated; a v1 *sums* reference with 5 duplicate rows now also reads `1/5` and exits 2 (the fix reaches the v1 shapes) |
| A9 | the coverage fix false-positives on the real 5 paths | **REFUTED** — canonical 5 under the gate exit 0; the live pair `MATCH 5/5` |
| A10 | the both-absent ruling silently weakens severity precedence | **REFUTED** — mixed pair (one drifted path + one both-absent) → `VERDICT: CONTENT-DRIFT … exit=10` |
| A11 | a forged stanza exploits the both-absent branch (`EXISTS: yes` → `no`, keeping `SHA256`) | **NOT REFUTED, not a round-4 hole** — the row reads `MATCH compared=11/11`, i.e. a full 11-field comparison, not the both-absent branch (the `ref_exists` predicate is `EXISTS == yes or 'sha256' in sec`, so the branch is never entered). Same on the base revision. A pre-existing semantics note; the README's "cleanly absent" definition (no `SHA256`, no error key) is the operative one and this stanza is not that. |
| A12 | the empty-`--out` guard is load-bearing but unguarded by the suite | **SUSTAINED — the one finding (M5)** |
| A13 | the shipped selftest is vacuous somewhere | **REFUTED for four of five reverts** — M1 coverage basis → `coverage-gate-rejects-duplicate-stanzas` red; M2 mkdir guard → `out-parent-not-a-directory-usage-exit` red; M3 sidecar arm → `refuses-sidecar-over-measured-file` red; M4 neighbour arm → `refuses-receipt-over-sidecar-neighbour` red. Each fires exactly its own case, nothing else. M5 is the exception. |
| A14 | the documented exit map drifts from the code | **REFUTED** — every `EXIT_*` constant (`0,2,3,10,11,12,13,14`) has a README row; the README names all 28 cases and the exact summary line |
| A15 | EX-21's identity table is self-claimed, not re-derived | **REFUTED** — 25/25 digest-bearing lines reproduce exactly (both real targets, the r3 base copy, both live receipts + sidecars, all harness/driver digests, SKILL.md, the three PL-3 artifacts); 0 drift |
| A16 | the registry row patch is not line-neutral | **REFUTED** — 390 lines both sides, one row replaced |
| A17 | the round's live pair is stale relative to the landed bytes | **REFUTED at write time** — EX-21's pair self-pins `29bb45ae…`; this seat's own fresh pair on the landed bytes also reads `MATCH 5/5 exit=0` with both sidecars verifying |
| A18 | the r3-phase regression leg is red on the new revision | **EXPECTED, not a defect** — `regress-r4.py --phase r3` on the landed bytes reports 6 FAILs (`D/selftest-case-count` 28 vs expected 22, and the five G checks that now read CLOSED vs their r3 "expect OPEN"). Those are the pre-state assertions of the *previous* round's phase; the r4 phase is the one that governs this landing and reads `hold=74 fail=0` (this seat's own run). On the base revision the same r3 phase reads `hold=70 fail=1` — the residual being the not-yet-existing ruling text. |

### M5 — the finding (sustained)

**Statement.** The `--out`-with-no-usable-name guard (the
`try: sidecar = out.with_name(...) / except ValueError: … EXIT_USAGE` block in
`cmd_capture`) is load-bearing for the declared exit map, and **no case in the
shipped 28-case selftest exercises it**.

**Measurement** (`m5-finding.txt`): reverting the guard on a scratch copy
(`sabotage-arms/M5-empty-out-guard-reverted.py`, sha
`a3d09ae9526ba0a95a53870bb8345147a25fb34d5214df52c221e8f015ed65f8`) makes
`capture --out ''` die with a raw `ValueError: PosixPath('.') has an empty name`
traceback at **exit 1**, while the shipped selftest still reads
`CLEAN cases=28 passed=28 failed=0 exit=0`. The landed revision returns
`USAGE: --out carries no usable name …` exit 2 on the same command; the base r3
revision also returns exit 2 (`Is a directory: '.'`). So the unguarded form is
**worse than the revision it hardened** — precisely CR-4 item 6's warning class.

**Why it is still covered, but not by the tool's own suite.** EX-27's independent
`regress-r4.py`, run by this seat against the same sabotage copy, **does** catch
it: `[FAIL] G/b2-out-empty-arg exit=1 traceback=True expect=USAGE exit 2`, tally
`rows=75 hold=74 fail=1`. Cross-harness coverage therefore holds; the gap is that
the artifact the tool ships with — the selftest a future reader runs — cannot see
this regression. This is consistent with RV-7's verdict (its three claim-level
mutants are caught by the shipped suite); M5 is a narrower sub-guard the claim
does not name.

**Patch shape (text only).** One fixture case in `cmd_selftest`, mirroring case
24's structure:

```python
    def case_out_empty_name():
        tool = str(Path(__file__).resolve())          # rule-#14 identity arm
        p = subprocess.run([sys.executable, tool, "capture", "--out", "",
                            "--paths", str(fixture)], capture_output=True, text=True)
        assert p.returncode == EXIT_USAGE, "expected USAGE exit %d, got %d" % (EXIT_USAGE, p.returncode)
        assert "Traceback" not in p.stderr, "raw traceback for an --out with no usable name: %s" % p.stderr
    run_case(cases, "out-with-no-usable-name-usage-exit", case_out_empty_name)
```

Severity: low. The vector is an operator typo, the class is correct on the landed
bytes, and an independent harness in the same wave covers it. A coverage note,
not a defect in the revision. Taking it would move the selftest 28 → 29 and
require the README case count and the registry row's case list to be re-derived.

### Two further measured observations (no action requested)

- **`--out` inside a measured directory self-invalidates** (not a regression):
  `capture --paths dir --out dir/rec.txt` → exit 0, then `verify rec.txt --live`
  → `REWRITE-DRIFT exit 11`, because the receipt and its sidecar move the
  directory's mtime. Identical on the base revision — the pre-existing property
  of a directory stanza's stat-only pin (CR-3 §2's "one stat, not a tree").
- **CR-4 item 8 (inode arm fails open when the scoped side is unstattable) is
  still open**, reproduced first-hand on the landed bytes: scoped path under a
  000-mode parent + hardlink alias as `--out` → exit 14 (`UNEVALUABLE`) *and* the
  receipt lands on the measured inode (both names sha `29cc983f…`). Outside the
  r4 claim's letter (the claim names (a)-(d)); named here for completeness.

## 5. Blockers

None. Two polling gaps, named per the seat line: EX-21's `claims/c3/EX-21/` was
empty at this seat's first 60 s check and populated at 14:10:33Z; the README
continued to move for two samples after the tool settled (`f36c3c31…` →
`125e7e02…` → `9d9400da…` at 14:11:48Z), then held. All AFTER measurements were
taken on the settled pair (`29bb45ae…` / `9d9400da…`), re-derived at 14:12–14:14Z
and at write time. If the parent lands a further README edit, the ruling-text and
exit-map checks (A14, and the (d) row of §3) must be re-run against the new
bytes; the tool-side results are unaffected.
