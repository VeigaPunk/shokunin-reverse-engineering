# RV-6 — seat report (chain c3, reviewer) · wave `arc3-loop1-round4`

Seat RV-6 · chain c3 · role reviewer · task: code-review the three closures in the
landed tool — correctness, declared classes reachable, no regressions.

Lane note: this seat ran on the devin lane (the declared fallback; the hyper lane
returned 402 out-of-credits on the whole roster at first dispatch — recorded in
`claims-frozen.md`, not a lane signal).

Repo `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`; HEAD `015e1ba` (the landing
is in the worktree, uncommitted — `git status --porcelain .ufo/gates/` shows
` M .ufo/gates/custody-pair/{custody-pair.py,README.md}`; the commit is the
parent's). Scratch under `/var/tmp/rv6/w4`; `/tmp` never used. Custody paths
opened for reading only; no git mutation; no file outside
`.ufo/waves/arc3-loop1-round4/{seats,c3/RV-6}` written by this seat.

## Revisions under measurement (identity, re-derived by this seat)

| object | revision | lines / bytes | how pinned |
|---|---|---|---|
| tool BEFORE | `7cd19c3cfd835c7807d5e60dece1c2592c9df6c319a78deb14469dd6ebe8ab09` | 1155 / 54279 | copied from the worktree before the landing, sha re-derived |
| tool AFTER | `29bb45ae0fd795e54e85d8749a163159aead181b42e9d3af399326b968b30acf` | 1343 / 65902 | copied from the worktree at 14:12Z, sha + `wc` re-derived; stable over a 100 s window (5 samples) |
| README AFTER | `9d9400dab7ff7072375c13fad43c02dde0f3923a58cf3af0d50fa3384535022a` | 272 / 15293 | same, stable over the same window |
| SKILL.md | `5eec51c089e57f5d5806b4728261fb8c959637580a73aed7be4cddc1866b8f3f` | 390 | unchanged (claimed unchanged by EX-21; re-derived) |

## 1. Work performed (evidence pointers)

All artifacts in `.ufo/waves/arc3-loop1-round4/claims/c3/RV-6/`.

1. **Independent BEFORE measurement** on the frozen base, before the landing
   existed (`before-probe.out`, `before-battery.out`, `before-*.json`). The base
   was snapshotted to `/var/tmp/rv6/w4/tool-r3-7cd19c3c.py` at 14:04Z; the worktree
   tool was still `7cd19c3c…` then (measured, not assumed).
2. **Independent AFTER measurement** on the landed bytes
   (`after-probe.out`, `after-battery.out`, `after-*.json`).
3. **Arm-for-arm diff** of the two runs: `arm-diff.txt` — 33 arms, base
   `hold=27 fail=5`, landed `hold=32 fail=0`, the 5 base failures all `CLOSED`.
4. **Sabotage arms** (`sabotage-arms/`): five scratch copies, each reverting one
   closure, run through the shipped selftest.
5. **Attack battery** on the new guard: 17 vectors (§4).
6. **Third-party harness re-run**: EX-27's `regress-r4.py`
   (`57f04e349240beeceed8d68fe7497e9d694eda0d702cffd9567c8bb4011e1c94`) run by
   this seat against the landed bytes — `rows=75 hold=74 fail=0` in the r4 phase
   (reproducing EX-21's recorded tally), and against the M5 sabotage copy —
   `rows=75 hold=74 fail=1` with exactly `G/b2-out-empty-arg` red (`m5-finding.txt`).
7. **Rule #14 identity re-derivation**: every line of EX-21's `sha256s.txt`
   carrying a digest was re-derived by this seat — 25/25 `OK`, 0 drift (§5).
8. **Doc-vs-code checks**: README case count (28 named), README exit map covers
   every declared `EXIT_*` constant, registry-row patch is line-neutral (§6).

## 2. Proposed changes (patch texts)

**None.** This seat writes no tool code, no README, no SKILL. The findings in §4
are reported for EX-21 / the parent; one of them (M5) has a one-case patch shape
described in §4 but is deliberately left as text, not applied.

## 3. Before → after measurement for the chain's claim

Frozen claim (C3): "(a)-(c) are closed with declared classes (selftest 22 → ≥24
with the new fixtures; sabotage arms), (d) is adjudicated with the ruling text
landed in the README; the registry row + README re-derived same-commit; the
round's live pair (revised tool) verifies MATCH 5/5; every receipt self-pins the
new tool sha256; command A unchanged."

| leg | before (base `7cd19c3c`) | after (landed `29bb45ae`) | verdict |
|---|---|---|---|
| **(a) sidecar scope** — `capture --paths vic.sha256 --out vic` | exit **0**, `SIDECAR: …/vic.sha256`, victim bytes destroyed (sha `140aba39…` → `5dbcef16…`) | exit **2**, USAGE refusal, victim sha `140aba39…` unchanged | **CLOSED** |
| **(a2)** second spelling (`--paths vic2.sha256 --out vic2`) | exit 0, clobbered | exit 2, intact | **CLOSED** |
| **(a3)** ordinary `--out` still writes its sidecar | exit 0, sidecar present | exit 0, sidecar present | no regression |
| **(b) mkdir** — `--out <regular-file>/sub/r.txt` | **`NotADirectoryError` traceback, exit 1** (outside the declared map) | exit **2**, `USAGE: cannot create the receipt directory ([Errno 20] …)` | **CLOSED** |
| **(b2)** `--out ''` (CR-4 item 6's trap) | exit 2 (`Is a directory: '.'`) | exit 2, `USAGE: --out carries no usable name …` | preserved, better message |
| **(b3)** read-only parent dir | traceback, exit 1 | exit 2, USAGE | **CLOSED** |
| **(b4)** legal nested `--out` | exit 0, receipt created | exit 0, receipt created | no regression |
| **(c) coverage basis** — 5× duplicate stanza, `--require-paths 5` | exit **0**, `VERDICT: MATCH paths=1`, **no coverage line** | exit **2**, `REFERENCE-COVERAGE: 1/5 …`, `USAGE: reference covers 1 of the required 5 distinct paths` | **CLOSED** |
| **(c3)** canonical 5 paths under the gate | exit 0 | exit 0 | no false positive |
| **(c4)** 1-of-5 reference under the gate | exit 2 (r3 D3 close) | exit 2 | preserved |
| **(c5)** no flag = declared default, no gate | exit 0 | exit 0 | unchanged |
| **(d) both-absent MATCH** | reproduced first-hand: `verify ghost.txt --live` → `MATCH 1/1 exit 0`, `SHA256-CONTRACT: 0/0` | `MATCH 1/1 exit 0` **plus** the row note `both sides record the path absent — the MATCH is an agreement on absence…`; ruling text in README §"The both-absent `MATCH`" | **adjudicated, annotated** |
| selftest | `CLEAN cases=22 passed=22 failed=0` | `CLEAN cases=28 passed=28 failed=0` | 22 → 28 (claim: ≥24) |
| live pair (landed tool) | — | `MATCH paths=5/5 drift=0 exit=0`, identical with `--require-paths 5`; both sidecars `sha256sum -c` OK | **MATCH** |
| receipt self-pin | — | `# tool: … sha256 29bb45ae…` == independent `sha256sum` | **pinned** |
| declared classes 0/10/11/12/13/14/2/3 | all reachable | all reachable (same arms) | unchanged |
| command A | — | recipe reads Git objects under `corpus/` + `SKILL.md` only; `.ufo/gates/` is outside its read set; SKILL.md unchanged `5eec51c0…` | **unaffected** |

Base-state battery summary: `arms=33 hold=27 fail=5` — the 5 failures are exactly
the three declared residuals (a, a2 / b, b3 / c1), i.e. the claim's "before"
is reproduced, not accepted on trust. Landed: `arms=33 hold=32 fail=0` (1 arm is
an `n/a` informational row).

## 4. Attacks / refutations attempted, with verdicts

| # | attack | verdict |
|---|---|---|
| A1 | "the sidecar arm is a literal-string check that a second spelling defeats" — probe `--paths X.sha256 --out X` under three spellings, plus `./`-relative | **REFUTED** — all refused; the guard compares *resolved* paths and the inode arm, not literal strings (base revision fails all three) |
| A2 | "the derived sidecar can still land on a measured file via a hardlink alias" — pre-create `rec.txt.sha256` as a hardlink of the measured file, then `--out rec.txt` | **REFUTED** — exit 2, refusal names the sidecar; both names keep sha `1b23b207…`, same inode throughout |
| A3 | "a symlinked `--out` defeats the resolved-path arm" | **REFUTED** — exit 2, target intact |
| A4 | "the neighbour arm only covers one level" — `--paths X.sha256 --out X.sha256.sha256` | **REFUTED** — exit 2 |
| A5 | "the custody paths' `.sha256` neighbours are unguarded" — `--out ~/.bashrc.sha256` | **REFUTED** — exit 2, refused by the neighbour arm |
| A6 | "the new guard is over-broad and breaks legitimate use" — `--out legit-name.sha256` (no scope conflict), `--out -`, relative `--out`, nested `--out` | **REFUTED** — all succeed; `--out -` writes no sidecar, as before |
| A7 | "the mkdir guard closes one errno and leaves others" — ELOOP via a self-symlink, EACCES via a 0500 parent, `--out` on an existing directory, `--out '..'`, `--out '/'` | **REFUTED** — every vector is a declared USAGE exit 2 with a message, zero tracebacks |
| A8 | "the coverage fix breaks the r3 D3 close or the declared default" — 1-of-5 under the gate; no flag at all; v1 sums reference with 5 duplicate rows | **REFUTED** — 1-of-5 still exit 2 with the same line; no flag still ungated (`MATCH`); the v1 dup-rows reference now reads `1/5` and exits 2 (the fix reaches the v1 shapes too) |
| A9 | "the coverage fix introduces a false positive on the real 5 paths" | **REFUTED** — canonical 5 under `--require-paths 5` → exit 0; the round's live pair → `MATCH 5/5` |
| A10 | "the both-absent ruling silently weakens severity precedence" — mixed pair (one drifted path + one both-absent) | **REFUTED** — `VERDICT: CONTENT-DRIFT … exit=10`; the absent row does not outrank the drift |
| A11 | "a forged stanza can exploit the both-absent branch" — take a real receipt and rewrite `EXISTS: yes` → `EXISTS: no` while keeping `SHA256`/`SIZE`/`INODE` | **NOT REFUTED, but not a new hole** — the row reads `MATCH compared=11/11`. The stanza is *not* cleanly absent (it still carries `SHA256`), and the instrument's `ref_exists/cand_exists` predicate is `EXISTS == yes or 'sha256' in sec`, so the both-absent branch is never entered; the comparison is a full 11/11 field comparison. Same behaviour on the base revision. Recorded as a *pre-existing semantics note*, not a round-4 regression: the README's "cleanly absent" definition ("records no `SHA256` and carries no error key") is the operative one, and this stanza is not that. |
| A12 | "the empty-`--out` guard is load-bearing but unguarded by the suite" — revert it on a scratch copy | **SUSTAINED — the one finding** (M5, below) |
| A13 | "the new revision leaves the shipped selftest vacuous somewhere" — four other reverts | **REFUTED for four** — each of the four reverts (coverage basis, mkdir guard, sidecar arm, neighbour arm) turns exactly the case that names it red, and nothing else; the suite is non-vacuous on those four |
| A14 | "the documented exit map drifts from the code" | **REFUTED** — every `EXIT_*` constant in the tool (`0,2,3,10,11,12,13,14`) has a README row; the README names all 28 cases and the exact `cases=28 … exit=0` summary line |
| A15 | "EX-21's identity table is self-claimed, not re-derived" | **REFUTED** — 25/25 digests reproduce exactly, including the two real targets, the r3 base copy, both live receipts + sidecars, all harness/driver digests, and SKILL.md |
| A16 | "the registry row patch is not line-neutral" | **REFUTED** — `skill-registry-row.patched.md` is 390 lines, same as `SKILL.md`; exactly one row replaced; the row text names the new classes and the (d) ruling |
| A17 | "the round's live pair is stale relative to the landed bytes" | **REFUTED at write time** — EX-21's pair self-pins `29bb45ae…`; this seat's own fresh pair on the landed bytes also reads `MATCH 5/5 exit=0` with both sidecars verifying |

### M5 — the finding (sustained)

**Statement.** The `--out`-with-no-usable-name guard (the `try: sidecar =
out.with_name(...) except ValueError: … EXIT_USAGE` block at
`.ufo/gates/custody-pair/custody-pair.py`) is load-bearing for the declared exit
map, and **no case in the shipped 28-case selftest exercises it**.

**Measurement** (`m5-finding.txt`): reverting the guard on a scratch copy
(`sabotage-arms/M5-empty-out-guard-reverted.py`, sha256 `a3d09ae9…`) makes
`capture --out ''` die with a raw `ValueError: PosixPath('.') has an empty name`
traceback at **exit 1** — outside the declared map — while the shipped selftest
still reads `CLEAN cases=28 passed=28 failed=0 exit=0`. The other four reverts
each go red.

**Why it still counts as covered, but not by the tool's own suite.** EX-27's
independent `regress-r4.py` (a different harness, run by this seat against the
same sabotage copy) **does** catch it: `[FAIL] G/b2-out-empty-arg exit=1
traceback=True expect=USAGE exit 2`, tally `74/75`. So the wave's cross-harness
coverage holds; the gap is that the artifact the tool ships with itself — the
selftest a future reader runs — cannot see this regression.

**Patch shape (text only; not applied by this seat).** One fixture case in
`cmd_selftest`, mirroring case 24's structure:

```python
    def case_out_empty_name():
        tool = str(Path(__file__).resolve())          # rule-#14 identity arm
        p = subprocess.run([sys.executable, tool, "capture", "--out", "",
                            "--paths", str(fixture)], capture_output=True, text=True)
        assert p.returncode == EXIT_USAGE, "expected USAGE exit %d, got %d" % (EXIT_USAGE, p.returncode)
        assert "Traceback" not in p.stderr, "raw traceback for an --out with no usable name: %s" % p.stderr
    run_case(cases, "out-with-no-usable-name-usage-exit", case_out_empty_name)
```

Severity: low — the vector is an operator typo (`--out ""`), the class is
already correct on the landed bytes, and an independent harness in the same wave
covers it. It is a coverage note, not a defect in the revision.

## 5. Rule #14 identity re-derivation (this seat's own run)

Every digest-bearing line of `.ufo/waves/arc3-loop1-round4/claims/c3/EX-21/sha256s.txt`
was re-derived by this seat at 14:14Z: **25/25 OK, 0 drift** — the two real
targets (`29bb45ae…`, `9d9400da…`), the r3 base copy (`7cd19c3c…`), both live
receipts and both sidecars, `gen-patch.py`, `before-probes.sh`, both diffs, both
patch-text files, all five cross-seat driver digests, `SKILL.md`, and the three
PL-3 comparison artifacts. The `# generated:` timestamp in that file
(`2026-10-19T14:11:43Z`) precedes this seat's read, and the two targets are
stable across a 100 s window of five samples — so the table is not a stale
snapshot of a moving file.

## 6. Other measured observations (no action requested)

- **`--out` inside a measured directory self-invalidates** (not a regression):
  `capture --paths dir --out dir/rec.txt` → exit 0, then `verify rec.txt --live`
  → `REWRITE-DRIFT exit 11`, because the receipt and its sidecar changed the
  directory's mtime. Identical on the base revision — a pre-existing property of
  a directory stanza's stat-only pin (CR-3 §2's declared "one stat, not a tree").
  Recorded so the parent does not read it as a round-4 regression.
- **CR-4 item 8 (inode arm fails open when the scoped side is unstattable) is
  still open**, reproduced first-hand on the landed bytes: scoped path with a
  000 parent + hardlink alias as `--out` → exit 14 (`UNEVALUABLE`) *and* the
  receipt lands on the measured inode (both names sha `29cc983f…`). This is not
  in the r4 claim's letter (the claim names (a)-(d)), and the r3 verdict recorded
  it as a docstring-scope matter; named here for completeness.
- **CR-3 W4 wording residual stands**: the `REFERENCE-COVERAGE` line is still
  printed only on the gate's failure path (0 occurrences on a passing gated run),
  which the round-3 README declares as the intended behaviour.

## 7. Blockers

None. Two polling gaps, named per the seat line: EX-21's `claims/c3/EX-21/`
directory was empty at this seat's first 60 s check and populated at 14:10:33Z;
the README continued to move for two samples after the tool settled
(`f36c3c31…` → `125e7e02…` → `9d9400da…` at 14:11:48Z) and was then stable. This
seat's AFTER measurements were taken on the settled pair (`29bb45ae…` /
`9d9400da…`), both re-derived at 14:12–14:13Z and again at 14:14Z. If the parent
lands a further README edit, the ruling-text and exit-map checks in §3/A14 must
be re-run against the new bytes; the tool-side results are unaffected.

## 8. Artifact index (this seat's dir, sha256 re-derived at write time)

| file | sha256 |
|---|---|
| `probe.py` | `ee5806e8a23c1312ecbdc242f360f7190de394ec6184529fc95a7a0b62104411` |
| `battery.py` | `af32e3e05cced3efed0b22e3c18736bf74942f2962ffef8b5dab0c8b476ae363` |
| `before-battery.json` / `after-battery.json` | `9975cd46c60de3aacbe651c1ee2e646f6432d50acc5867fdaaa4336cebea9743` / `884895d7ec1b420f5ef6431bd5b20120466a8505ab3da33e44444cf3e9d03c7a` |
| `before-probe.json` / `after-probe.json` | `6e03138fbbe32e07ea9d87b7be95d97791ce059f1d0c60b4ce6b0e22f4c8ebe8` / `98862f0186e123515b6e0d96c36d8948bcb5f380cdfde2ac750303fccbc70c23` |
| `before-battery.out`, `after-battery.out`, `before-probe.out`, `after-probe.out` | raw transcripts of the runs above |
| `arm-diff.txt` | the 33-arm before/after table |
| `sabotage-arms/*.py` | the five revert copies (M5 = `a3d09ae9526ba0a95a53870bb8345147a25fb34d5214df52c221e8f015ed65f8`) |
| `m5-finding.txt` | the M5 transcript (landed vs sabotage vs base, in-tool selftest, EX-27's harness) |
