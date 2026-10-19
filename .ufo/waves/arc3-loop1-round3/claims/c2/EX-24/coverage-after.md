# EX-24 — coverage-after: 1-of-5 receipt verify (chain c2, wave arc3-loop1-round3)

Seat EX-24 · chain c2 · role executor · 2026-10-19.
Task: **after-state** — a 1-of-5 receipt `verify` must land on a *declared class*
(or the `--require-paths` behaviour, per the landed design), and the four custody
paths outside the receipt must **not** read as verified.

Verdict summary: **the landed gate does what its README declares** — a 1-of-5
reference under `--require-paths 5` is a USAGE exit 2 that *names* the unaccounted
paths — and the four unaccounted paths are never classified `MATCH`.
Two measured residuals qualify the close: the gate is **opt-in** (declared as
such, README:98-100) so the flag-absent path still reads `MATCH exit=0`; and the
gate **counts stanzas, not distinct paths**, so a padded receipt passes it
silently (patch text filed, §4).

## 0. Instrument, revision, method

| item | value |
|---|---|
| AFTER tool revision | `7cd19c3cfd835c7807d5e60dece1c2592c9df6c319a78deb14469dd6ebe8ab09` (54,279 B, mtime 2026-10-19 10:13:20 -03) |
| BEFORE tool revision | `112d01dc034c2d54324e7703e2d03d1d83b0c3930ed5d4f688546968b73ecefa` (39,157 B) — the landed round-2 revision |
| revision timeline | `watch.log` (every distinct sha with UTC timestamp), `stable-poll.log` (stability checks) |
| tool copies under test | `tools/before/custody-pair.py`, `tools/after/custody-pair.py` (byte-identical to the above; re-hashed in `IDENTITY-after.txt`) |
| harness | `harness/run-matrix.sh` — 24 legs, one command per phase |
| adjudicator | `harness/checks.py` — 12 criteria, PASS/FAIL with quoted evidence (`before/checks-*.json`, `after/checks-*.json`) |
| scratch | `/var/tmp/ex24-after/` only (never `/tmp`); custody paths read-only (the tool's own sha256/stat pass); no git mutation |
| repo HEAD | `c07af80fcf3a60f9c6a0ca09b6e23fb5794d3311` throughout (no commits during the leg) |

Revision history seen live: `112d01dc` (round-2 landed) → `7b848eaf` → `68e30768`
→ `22122801` → `1287c9d6` → `d5e72049` → `460a01f0` → `b9bd55e9` → `a991f976` →
`d9be407d` → `08fb6833` → `a611ede4` → `f2412aaa` → `57dffff1` → `03bd6242` →
`dc841464` → `89bfebec` → **`7cd19c3c`** (stable ≥ 7 min at measurement; cited as
the hand-off revision by EX-28, EX-25, CR-4, PL-2). Mid-flight revisions
measured only as interim probes (`tools/interim/`), never as results.

### The "four other paths must not read as verified" criterion

The r2 debt D3 is a *scope* hole: `verify` compared only the paths present in
reference A, so a receipt naming 1 of 5 custody paths verified clean and the other
four were unexamined (H1 shape). "Not verified" is a property of the output text,
so it is measured as such: (i) no line may classify any unaccounted custody path
as `MATCH`/`MATCH-V1-PARTIAL`, and (ii) the run must either refuse or declare its
coverage. Criterion C5 is (i); C1–C4 and C12 are (ii).

## 1. BEFORE → AFTER for the seat's claim

| leg | command (tool revision) | BEFORE `112d01dc` | AFTER `7cd19c3c` |
|---|---|---|---|
| M1 | `verify <v1 1-of-5> --live` | `MATCH-V1-PARTIAL paths=1/1 drift=0 exit=0` | unchanged: `MATCH-V1-PARTIAL paths=1/1 exit=0` |
| M3b | `verify <v2 1-of-5> --live` | `MATCH paths=1/1 drift=0 exit=0` | unchanged: `MATCH paths=1/1 exit=0` |
| M2 | `… --require-paths 5` (v1) | `unrecognized arguments`, exit 2 (flag absent) | **exit 2**; `USAGE: reference covers 1 of the required 5 paths`; `REFERENCE-COVERAGE: 1/5 paths present in reference; unaccounted: ~/.omp/agent/mcp.json ~/.kimi-code/config.toml ~/.bashrc ~/.profile` |
| M3c | `… --require-paths 5` (v2) | flag absent | exit 2; `REFERENCE-COVERAGE: 1/5 … unaccounted: <all five canonical>` |
| M6 | unaccounted-path scan over every 1-of-5 output | four paths never named (no declaration) | **0 MATCH-classified mentions**; the four are named as `unaccounted` |
| M4c/M4d | canonical 5/5 pair / vs live | `MATCH paths=5/5 exit=0` | `MATCH paths=5/5 exit=0` (unchanged — no false positive) |
| M10 | `--require-paths 1` on 1-of-5 | flag absent | exit 0 (threshold, not a blanket refusal) |
| M9b | `--require-paths 5` on 4-of-5 | flag absent | exit 2, `REFERENCE-COVERAGE: 4/5 …` |
| M8b | `--require-paths 5` on 5 scratch paths | flag absent | exit 0 (count-based, see §4 R3) |
| M7a | `selftest` | `CLEAN cases=15` | **`CLEAN cases=22 passed=22 failed=0 exit=0`** |
| M7c | `selftest --scratch <missing>` | `FileNotFoundError` traceback, exit 1 | `USAGE: scratch base is not a directory: …`, exit 2 (D6 closed) |
| M17 | round-3 pre-pair receipt, `--require-paths 5` | flag absent | `MATCH paths=5/5 exit=0` (the intended usage on the round's own artifact) |
| M15/M16 | round-1 canonical v1 stanza receipt, with/without the gate | `CONTENT-DRIFT exit=10` | `CONTENT-DRIFT exit=10`, 5/5 present — identical; the exit-10 is the *known live drift* on `~/.kimi-code/config.toml` plus 4 `LABEL-DEFECT`s, i.e. the r2-declared v1 contract, not a regression |

Adjudicator: **before 2 pass / 10 fail → after 10 pass / 2 fail.** The two
remaining failures are C1 and C2 — the *flag-absent* 1-of-5 legs — for the
declared opt-in reason (§3 R1).

## 2. Attacks attempted, with verdicts

| # | attack | result | verdict |
|---|---|---|---|
| A1 | "the gate is a blanket refusal that breaks real receipts" | M4c/M4d/M17/M8b/M10 all pass at exit 0 | **refuted** — threshold semantics, verified at 1, 4, 5 and 6 paths |
| A2 | "the refusal line is a bare count; the operator still cannot tell *which* paths are missing" | M2/M3c/M9b name all unaccounted paths (C12) | **refuted** |
| A3 | "stanza padding defeats the gate" — 5× duplicate stanza for ONE path (v1 sums + v2 shapes), `--require-paths 5` | **exit 0**, `MATCH paths=1/1`, other four custody paths unexamined, **no coverage line at all** (M18/M19). At revision `03bd6242…` the same pass printed `REFERENCE-COVERAGE: 5/5 … unaccounted: <4 paths>` (self-contradictory line; `interim/M8b-*.out`), i.e. the count and the unaccounted list disagree | **CONFIRMED — residual R2**, patch text `proposed-coverage-count.patch.md` |
| A4 | "the gate establishes *canonical-set* coverage" — 5 unrelated scratch paths, `--require-paths 5` | exit 0 (M8b), no coverage line on the pass path | **CONFIRMED — residual R3** (count, not identity) |
| A5 | "a consumer who omits the flag is safe" | M1/M3b: bare `MATCH exit=0`, zero coverage output | **CONFIRMED — residual R1**; README:98-100 declares it ("Opt-in: without the flag the comparison is exactly the reference's paths, unchanged") |
| A6 | "the gate masks real drift" — covered path drifted, 1-of-5, `--require-paths 5` | M13b: exit 2 (coverage) instead of reporting the drift | **confirmed but benign** — the refusal is the fail-closed direction; the same drift without the gate is still `CONTENT-DRIFT exit=10` (M13) |
| A7 | "the fix is inert elsewhere" — canonical pair, round pre-pair, v1 receipts | M4c/M4d/M17/M15/M16 identical before/after | **refuted** — no collateral change on the surfaces measured here |
| A8 | "the tool's self-claims (selftest) are stale/red" | `CLEAN 22/22`, transcript re-run twice; EX-28 independently refuted the transient `89bfebec` DIRTY | **refuted at `7cd19c3c`** |
| A9 | harness artifact: renaming a tool copy breaks selftest case 10 (`Path(__file__).parent / "custody-pair.py"`, line 733) | reproduced, then avoided by keeping the canonical filename | **refuted as a tool defect** — needs the canonical filename only in a renamed-copy setup; recorded for the record |

## 3. Residuals (measured)

- **R1 — the gate is opt-in.** Flag-absent `verify` of a 1-of-5 reference still
  reads `MATCH exit=0` with no coverage declaration (C1, C2 fail). The README
  *declares* this ("Opt-in: without the flag the comparison is exactly the
  reference's paths, unchanged", `README.md:98-100`), so it is a declared design
  choice, not an undeclared fail-open. The round-2 D3 sentence ("a 1-of-5 receipt
  reads exit 0") is therefore closed **only for callers that pass the flag**; any
  gate keyed on `verify` exit codes must pass `--require-paths 5`. Recommendation
  for the parent: state that in the round report, and if a fail-closed default is
  wanted, take it up as a new claim (patch text offers two options).
- **R2 — the gate counts stanzas, not distinct resolved paths.** 5 duplicate
  stanzas of one path pass `--require-paths 5` and print no coverage line
  (M18/M19). Root cause read from the landed source: `reference_coverage()`
  returns `len(ref_sections) >= required` while its own `unaccounted:` list is
  built from the resolved-path set. The one-line fix (and a selftest vector pair)
  is in `proposed-coverage-count.patch.md`. Note the README says "fewer than N
  stanzas", so implementation and documentation agree — the *unit* is the weak
  point, not the code/documentation contract.
- **R3 — count, not identity.** Any 5 paths satisfy the gate (M8b), so passing it
  does not establish that the *custody set* was covered. Same root cause as R2;
  the optional identity gate in the patch text closes it.
- **Observation (not this seat's claim):** the round-1 canonical v1 receipt no
  longer sha256-matches live — one custody path (`~/.kimi-code/config.toml`)
  reads `CONTENT-DRIFT` (M15/M16, exit 10). This is the known live drift already
  recorded in `SCORECARD.md:1470`, not a tool regression; flagged here only
  because the after-state legs in this artifact read exit 10 for that receipt.

## 4. Evidence index

- `after/` — 24 legs + `matrix.out` + `checks-after.json` + `M6-unaccounted-scan.out`
- `before/` — the same matrix on `112d01dc` (before-state) + `checks-before.json`
- `harness/` — `run-matrix.sh`, `checks.py`
- `tools/` — `before/`, `after/`, `interim/` copies (each re-hashed at capture)
- `interim/` — the mid-flight matrix at `03bd6242…` (design-evolution evidence for A3)
- `fixtures/` — `v1-dupe-5x.txt`, `v2-dupe-5x.txt` (crafted attack receipts), the
  r2 `v1-partial-1of5.txt` copy
- `watch.log`, `stable-poll.log` — revision timeline and stability
- `proposed-coverage-count.patch.md` — R2/R3 patch text (patch text only; the
  target is EX-21's write path)
- `IDENTITY-*.txt` — re-derived sha256 of every evidence file and both tool copies

Identity (rule #14): re-derived after the last revision of this artifact — see
`IDENTITY-after.txt`.