# PL-2 — C2 plan: custody-pair hardening (D2 + D3 + write-guard scope + D6)

Seat PL-2 · chain c2 · role planner · wave `arc3-loop1-round3` · 2026-10-19.
Repo `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, HEAD
`c07af80fcf3a60f9c6a0ca09b6e23fb5794d3311`. No git mutation; no custody path
written, renamed or `utime`d (read-only sha256/stat capture only); scratch
`/var/tmp/pl2` + `mktemp -d /var/tmp/pl2-matrix-*` (never `/tmp` — standing
EDQUOT rule). Only artifacts under this seat's directory were written.

Base revision for every hunk and line number below:
`.ufo/gates/custody-pair/custody-pair.py`, 889 lines, sha256
`112d01dc034c2d54324e7703e2d03d1d83b0c3930ed5d4f688546968b73ecefa` (the
round-2 landed revision, unchanged at HEAD — re-verified this seat:
`sha256sum .ufo/gates/custody-pair/custody-pair.py`). README base:
`fa484d573b0debb0d2ed134d076cb9593e7c3ee910ad4487d99cb9f3a8239bba`.

Artifacts in this directory (identities re-derived at write time):

| file | what | sha256 |
|---|---|---|
| `plan.md` | this plan | not self-hashable — digest in the seat report |
| `candidate.patch` | unified diff base → candidate (360 lines) | `838f98fbc1d63d17d4c703521b66a2e25b283887acb08e95da4c21955aa49aec` |
| `gen-candidate.py` | anchored generator (every anchor asserted unique; regenerates the candidate) | `2bf88ecb5f29c1be819d52add5e89c22f8f7eff28a540addf411817393e8e6fb` |
| `verify-candidate.sh` | re-runnable injection matrix (`<tool> <outdir>`) | `2d552eb07e262b45e5ff69f9247edacc707fed406dabc938331711d2464ba55d` |
| `matrix-before.txt` | matrix at `112d01dc…` (before) | `7a1819614253ba1ff03f2d01b39e7c8ae206dd413e4ec7b117b02b8141c31f4a` |
| `matrix-after.txt` | matrix at candidate `6b377964…` (after) | `b2725a198055783c368cee2a9fd69f491e752f641e2e538ed6cfd536fb0dd7a5` |
| `selftest-candidate.out` | 22-case transcript of the candidate | `53d83a1f1d87383d171478f4b6590b05d293f457f2eaf39463eccc288545a459` |
| `live-pre.txt` / `live-post.txt` (+ sidecars) | candidate-revision live pair over the 5 custody paths | `f890b7f6650e3ced8a66e293daca83e8697c1b2a9d31858905946772000813d6` / `d9cd37a9539bae5af0fbb19eefc0de4ac4a8cd5b999cb3c2ccf8177108a6e645`; sidecars `cd9e51237f0dc11cef87c6fd71bb5b34fbb3c75ee41e8f5d0534ebaeecad9ec5` / `d96ad00b692cf106af1801b8d8e44c7d98f10cdba99757acad237e7bc3ee0194` |
| `commandA-head.json` | command A at HEAD (round baseline) | `9de3cbddb68f19ad99003ad329b87b6670c6c83eb7b6f7aef14e1f7af7473cc1` |

Candidate identity (rule #14 — re-derived after the last revision, and it is
*expected to change* when EX-21 applies the payload to the real path):
candidate tool `6b37796457279e2465ce7f44edabf0f859d4ec5d3dea5d3050cfe8c4d83c3730`,
1,070 lines.

## 0. Verdict

All four named holes are closed by one patch, each with a **declared exit
class**, a fenced selftest case, and a before→after measurement taken by this
seat against the same fixtures (`matrix-before.txt` / `matrix-after.txt`). The
selftest grows **15 → 22** (21 required, 1 optional). Every declared class is
reachable and was reached; the ordinary live flow (5/5 pair, MATCH exit 0) is
unchanged; v1 receipt comparison is unchanged at the field level. Two gaps in
the inherited patch texts (EX-40's parser arm; the selftest case-7 identity
arm) are closed here and named in §2 — adopting EX-40's patch verbatim would
leave the receipt-file fail-open open.

Declared exit map **after** the patch (superset of the base map; nothing removed):

| code | class | reachable by |
|---|---|---|
| 0 | `MATCH` / `MATCH-V1-PARTIAL` | all compared paths agree |
| 10 | `CONTENT-DRIFT` | sha256 differs |
| 11 | `REWRITE-DRIFT` | sha equal, inode/ctime/mtime moved |
| 12 | `METADATA-DRIFT` | mode/uid/gid/size/type, EXTRA-PATH, LABEL-INCONSISTENT, LABEL-DEFECT |
| 13 | `ABSENT` | ≥1 reference path missing on the candidate side |
| **14** | **`UNEVALUABLE`** | **a path exists but could not be evaluated (`STAT-ERROR`/`READ-ERROR`); capture writes the receipt either way** |
| 2 | `USAGE` | bad args, unreadable/unparsable receipt, refused write, **missing scratch base**, **`--require-paths` coverage shortfall** |
| 3 | `SELFTEST-FAIL` | a selftest case failed |

Severity precedence (verify): `CONTENT-DRIFT(5) > UNEVALUABLE(4) > ABSENT(3) >
REWRITE-DRIFT(2) > METADATA-DRIFT(1) > MATCH(0)`. Capture: `0` all present and
evaluable, `14` ≥1 present-but-unevaluable, else `13` ≥1 absent.

## 1. The four closures as declared exit classes

| # | debt (round-2 verdict) | before at `112d01dc…` (measured, this seat) | declared class after | code locus (base lines) | hunks | fencing case |
|---|---|---|---|---|---|---|
| D2 | unreadable-path fail-open | blocked parent dir: capture `exit 13` (`EXISTS: no`+`STAT-ERROR`) then `verify --live` → **`MATCH exit 0`**; chmod-000 file: capture and `verify --live` die with `PermissionError` traceback, **exit 1**, no receipt written | **`UNEVALUABLE` exit 14**, receipt written with `STAT-ERROR`/`READ-ERROR`; never `MATCH` | docstring `:59-73`; constants `:119-142`; `capture_path` `:217-219`; `render_receipt` `:270-273`; `compare_section` `:427-428`; `cmd_capture` `:556-557` | H1a H1b H2a-c H3 H4 H5a-b H6 H7 H8 H8b | `unreadable-path-is-unevaluable`, `unevaluable-never-matches`, `parsed-unevaluable-reference-never-matches` |
| D3 | partial-reference coverage | 1-of-5 canonical receipt: `verify … --live` → **`MATCH exit 0`** (`paths=1/1`), other 4 custody paths unexamined; `--require-paths` unrecognised (argparse exit 2, wrong reason) | **`USAGE` exit 2** under `--require-paths N` when the reference carries < N stanzas, with `REFERENCE-COVERAGE: n/N … unaccounted: …`; **no flag = declared unchanged default** | docstring `:81-90` (new paragraph); `cmd_verify` `:591` area; `main` `:874`; `_run_verify` `:841-846` | H1c H10 H11a H11b | `partial-reference-require-paths-gate` |
| WG | write-guard scope (VZ-4 A11) | `capture --out X --paths X` → **`exit 0`, X clobbered by its own receipt** (sha `8ff46be8…`→`8396195d…`); hardlink alias writes through the shared inode (RV-11 F2) | **`USAGE` exit 2**, target bytes unchanged | `cmd_capture` `:562-566` | H9 (+H9b optional) | `refuses-to-write-over-scoped-path` (+`refuses-write-through-hardlink-alias`) |
| D6 | selftest scratch guard | `selftest --scratch <missing dir>` → **raw `FileNotFoundError` traceback, exit 1** outside the declared map | **`USAGE` exit 2**, no traceback, nothing written | `cmd_selftest` `:627-630` | H12 | `selftest-missing-scratch-usage-exit` |

Closure detail:

- **D2** adopts EX-40's measured design (`proposed-edge-classes.patch`, chain c3
  round 2 — its patched selftest 17/17 and edge matrix 11/17→17/17) as the
  declared class `14 UNEVALUABLE`. `capture_path` records an exists-but-
  unreadable regular file as `EXISTS: yes` + `READ-ERROR`; an EACCES `lstat`
  (blocked parent directory) keeps the base shape `EXISTS: no` + `STAT-ERROR`,
  which the new class treats as unevaluable, never as absent.
  `compare_section` short-circuits `UNEVALUABLE` **before** the both-absent
  `MATCH` branch (the measured fail-open), on either side; `cmd_capture` exits
  14 and still writes the receipt. The repair is fail-closed by construction:
  an unevaluable stanza can never be counted as a pass.
- **D3** adopts EX-35's `--require-paths N` (`proposed-v1-verify-adapter.patch.md`
  Change 2, measured gap A5) with the exit class **USAGE 2** and a
  `REFERENCE-COVERAGE` line that also lists the canonical paths the reference
  does not cover. Opt-in by design: the default comparison stays "exactly the
  reference's paths", which keeps every fixture workflow and the v1 shapes
  unchanged. EX-35's Change 1 (v1 compliance mode returning exit 0) and Change 3
  (blanket dispatch wrapper) are **not adopted** — see §6 A4/A5.
- **WG** extends the write guard from `CUSTODY_PATHS` to
  `set(args.paths or CUSTODY_PATHS) ∪ CUSTODY_PATHS`, resolved on both sides,
  so a receipt can never be written over a path the same invocation measures.
  Message updated to name the broader rule (`refusing to write a receipt over a
  path it measures`); the existing case asserts the exit class and byte
  invariance, not the message, so it stays green. The optional inode arm (H9b,
  RV-11 F2) refuses a hardlink alias of a measured path; it is out of the frozen
  claim's text, costs 10 lines and one case, and is the only way the third
  injection's *aliased* form closes.
- **D6** adopts EX-34's Option A (fail closed with the declared USAGE class)
  over RV-12's mkdir variant, because the frozen claim names the after-state as
  `USAGE`; the mkdir variant turns the injection into exit 0 and would not
  satisfy it. `--scratch /proc/nope` (exists but not a directory) takes the same
  class: the guard is `not base.is_dir()` — measured, candidate `exit 2` +
  `USAGE: scratch base is not a directory: /proc/nope`; base `exit 1`,
  traceback.

## 2. Two gaps the inherited patch texts leave open (closed here)

1. **The parser arm (D2).** EX-40's patch teaches `capture_path`,
   `compare_section` and `cmd_capture` about unevaluable stanzas but never
   teaches `parse_receipt`/`_parse_section` to read `READ-ERROR`/`STAT-ERROR`.
   A **receipt file** carrying the unreadable stanza therefore parses with no
   error marker, and a comparison against a readable candidate still reads as
   `MATCH-V1-PARTIAL` — measured first-hand: base tool
   `verify ref-hidden.txt victim-open.txt` → `MATCH-V1-PARTIAL exit 0` where
   `ref-hidden.txt` is `victim-open.txt` minus its `SHA256:` line plus a
   `READ-ERROR:` line (`matrix-before.txt` L4). Candidate: `UNEVALUABLE exit 14`
   (`matrix-after.txt` L4). Hunks H5a/H5b add the two key patterns and the two
   `_parse_section` keys. Without them the claim's "no fail-open MATCH" is
   satisfied only on the live path, not on the receipt-file path the tool
   itself writes.
2. **The identity arm (selftest case 7).** `case_label`
   (`custody-pair.py:733`) hardcodes `Path(__file__).resolve().parent /
   "custody-pair.py"` as the tool it spawns under three TZs — a *sibling name*,
   not the running bytes. Measured on a renamed base copy
   (`/var/tmp/pl2/probe/renamed/renamed-tool.py`): case 7 FAILs with
   `can't open file '<dir>/custody-pair.py'` →
   `DIRTY cases=15 passed=14 failed=1 exit=3`; where a sibling of that name
   exists, it is *that* file which gets tested. Either way the case does not
   measure the bytes under test (a rule-#14 surface). H13 replaces it with
   `TOOL_PATH` (already defined at `:108`); the same renamed candidate copy then
   reads `CLEAN cases=22 passed=22 failed=0 exit=0`. This matters for this
   round's own workflow: EX-21 works on a scratch copy.

## 3. Selftest growth: 15 → 22 (21 required + 1 optional) with case names

Existing 15 cases (base `:646-824`) are unchanged. New cases, inserted before
`passed = sum(...)` (`:826`), each asserting exactly one declared class:

| # | case name | asserts | hunk |
|---|---|---|---|
| 16 | `unreadable-path-is-unevaluable` | chmod-000 file → capture `14`, receipt keeps `EXISTS: yes` + `READ-ERROR`, no crash (skipped trivially under euid 0) | H14 |
| 17 | `unevaluable-never-matches` | blocked dir → capture `14`, `verify --live` `14`, `VERDICT: MATCH` absent | H14 |
| 18 | `parsed-unevaluable-reference-never-matches` | parsed receipt with `READ-ERROR` vs an open receipt → `14`, no `MATCH` (the §2.1 gap) | H14 |
| 19 | `partial-reference-require-paths-gate` | 1-stanza reference: no flag → `0` (declared default); `--require-paths 5` → `2` with `REFERENCE-COVERAGE: 1/5` | H14 |
| 20 | `refuses-to-write-over-scoped-path` | `--out X --paths X` → `2`, X byte-unchanged (the VZ-4 clobber) | H14 |
| 21 | `selftest-missing-scratch-usage-exit` | in-process `cmd_selftest(scratch=<missing>)` → `2` (base: `FileNotFoundError` → case FAILs) | H14 |
| 22 | `refuses-write-through-hardlink-alias` *(optional, with H9b)* | hardlink alias of a measured path → `2`, target byte-unchanged | H14 |

Measured: `CUSTODY_PAIR_SELFTEST: CLEAN cases=22 passed=22 failed=0 exit=0`
(`selftest-candidate.out`; candidate sha `6b377964…`).

Two design notes for EX-21:
- Case 21 is **in-process** on purpose. The subprocess form EX-34 sketched is
  safe only because the child's scratch is missing; with an *existing* scratch
  the child would recurse into the same case. In-process cannot recurse: the
  guard returns before `mkdtemp`.
- Under euid 0 the three permission cases return trivially (mode 000 does not
  block root) — declared, as in EX-40. They are the count's only
  environment-conditional rows.

## 4. Coupled-landing list (same commit, or the claim's coupling clause fails)

The round-8 precedent (`arc3-loop1-round2` C1: payload + `SHONEN.md:6` + records
in one commit) applies. The set that must land together:

1. **Tool** — `.ufo/gates/custody-pair/custody-pair.py` = base + H1a…H14
   (`candidate.patch`; regenerate with `gen-candidate.py` after re-verifying the
   base sha256). All identities in this plan are re-derived at landing.
2. **README** — `.ufo/gates/custody-pair/README.md` clauses that go stale and
   must be re-pinned to the landed revision:
   - exit table `:78-86`: add `| 14 | \`UNEVALUABLE\` | … STAT-ERROR/READ-ERROR …|`;
   - capture-exit paragraph `:88-90`: add the `14` case;
   - precedence sentence `:92-95`: insert `UNEVALUABLE` after `CONTENT-DRIFT`;
   - usage `:21-36`: add `verify … [--require-paths N]`, and state that an
     explicit `--scratch` base must already be a directory;
   - write scope `:38-41`: state the guard covers `set(--paths) ∪ CUSTODY_PATHS`
     (path or inode) — a receipt is never written over a path it measures;
   - selftest paragraph `:114-125`: `15` → `22`, naming the new cases.
3. **Registry row** — `SKILL.md:390` (the `custody-pair` row landed in round 2;
   one line, replacement is line-neutral, no reflow): exit map `+14
   UNEVALUABLE` and the new precedence; self-invocation clause `15 fixture
   cases` → `22 fixture cases` with the new names; pinned-values/write-scope
   clause `+` the write-guard scope (`--out` refused over any measured path,
   path or inode) and `--require-paths N` (USAGE 2 coverage gate). **One voice
   lands the row** (round-2 D10: two seats drafted it; the parent merged). PL-2
   drafts no competing row text.
4. **Round receipts** — the live pre/post pair captured **by the revised tool**
   (each receipt `# tool: … sha256 <landed sha>`), verified
   `verify pre post --require-paths 5` → `MATCH 5/5 exit 0`, plus both
   `.sha256` sidecars; the revision-pinned self-pin is the rule-#14 clause the
   claim names ("every receipt self-pins the revised tool's sha256").
5. **v1 verification** — re-run the v1 shapes against the landed revision. The
   *declared* statement stays the round-2 ruling: verifiability is the
   `SHA256-CONTRACT: n/m` line, not exit 0. **New measurement this round:**
   against live, the round-1 receipts now read `CONTENT-DRIFT exit 10` with
   `SHA256-CONTRACT 4/5` because custody path 3 (`~/.kimi-code/config.toml`) is
   now `bc66d543…` — the operator-side Kimi-config drift recorded in round 2,
   live at HEAD. Records must quote it as the live catch, or isolate the v1
   control runs on the EX-35 fixture set (as this plan's L8 does: `sums` and
   `v1-partial-1of5` shapes keep their pre-drift classes on scratch fixtures).
6. **Records + gates at the work commit** — command A `82/82`, `14/14`,
   `10.0/10.0` (HEAD baseline measured here, `commandA-head.json`); census
   `PASS 0/0/0/0`; probe `findings=0` both modes + selftest 13/13. C2's edits
   live entirely under `.ufo/gates/`, outside command A's measured read set
   (round-2 EX-24 §3 audited this structurally), so the invariance is expected
   and still must be re-measured at the commit.

Revision-pinned clauses to re-derive after **every** tool revision (rule #14):
the case count (22) and case-name list, the exit map, the `--require-paths`
default, the tool sha256 quoted in receipts and records, and this plan's
candidate identity. An artifact that quotes `6b377964…` after the payload lands
unmodified is right; one that quotes it after any edit is stale by construction.

## 5. Before → after measurement (the claim's falsifiable unit)

Runner: `verify-candidate.sh <tool> <outdir>`; transcripts `matrix-before.txt`
(base `112d01dc…`) and `matrix-after.txt` (candidate `6b377964…`), same fixtures,
same host, same minute (13:10:3xZ).

| injection | before | after | declared? |
|---|---|---|---|
| L1 D6 missing scratch | `exit 1`, 1 traceback | `exit 2`, 0 tracebacks, `USAGE:` line | yes — USAGE |
| L2 D2a blocked dir | capture `13`; verify **`MATCH exit 0`** | capture `14`; verify `14`, `VERDICT: UNEVALUABLE`, no MATCH | yes — 14 |
| L3 D2b chmod-000 file | capture `exit 1`, **no receipt** | capture `14`, receipt with `EXISTS: yes` + `READ-ERROR` | yes — 14 |
| L4 D2 parsed receipt | **`MATCH-V1-PARTIAL exit 0`** | `UNEVALUABLE exit 14` | yes — 14 |
| L5 D3 1-of-5 | plain `0` (declared); gated run unrecognised | plain `0` (declared); `--require-paths 5` → `2` + `REFERENCE-COVERAGE: 1/5 … unaccounted: 4 paths` | yes — USAGE |
| L6 scoped clobber | `exit 0`, target rewritten | `exit 2`, target byte-identical | yes — USAGE |
| L6 hardlink alias | `exit 0`, target rewritten | `exit 2`, target byte-identical | yes — USAGE |
| L0 selftest | `CLEAN 15/15 exit 0` | `CLEAN 22/22 exit 0` | 15 → 22 |
| L7 live pair ×2 + gate | `MATCH 5/5 exit 0` (gate unrecognised) | `MATCH 5/5 exit 0`; `--require-paths 5` → `MATCH 5/5 exit 0` | unchanged + declared gate |
| L8 v1 fixtures (11 shapes) | exit classes 2/10/12 per shape | identical to the row | unchanged |
| L9 custody digests | `16f496e6…, 38d2a1d0…, bc66d543…, 7d2ca28a…, 6c6be761…` | identical | read-only |

Receipt self-pin (rule #14 in-line): candidate pair header
`# tool: custody-pair.py  sha256 6b37796457279e2465ce7f44edabf0f859d4ec5d3dea5d3050cfe8c4d83c3730`
(matches `sha256sum` of the candidate, re-derived). Custody paths: 4/5 at the
round-1 pins; path 3 carries the recorded operator drift (above), unchanged by
every run in this matrix — the block is read-only.

Command A at HEAD (round baseline, canonical recipe `SCORECARD.md:92-123`):
`{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [],
"depth_score": 10.0, "knowledge_files": 82, "mapped": 82, "missing": [],
"rule_blocks": 14}` — census `PASS 0/0/0/0`, probe `findings=0`.

## 6. Attacks / refutations attempted (verdicts)

| # | attack | verdict | receipt |
|---|---|---|---|
| A1 | "EX-40's patch alone closes D2" | **REFUTED** — the receipt-file path still verifies `MATCH-V1-PARTIAL exit 0` (L4 before) because the parser never reads `READ-ERROR`; H5a/H5b required | `matrix-before.txt` L4 |
| A2 | "the candidate's clean selftest is a rubber stamp" | **REFUTED (spot-checked)** — each new case fails on the base tool: case 21 raises `FileNotFoundError`, cases 16–18 see exits 13/1/0, cases 19/20 see 0-and-clobber. The 15 legacy cases stay green on both revisions (L0), so the growth is additive | `matrix-before.txt` L0-L6 |
| A3 | "the D3 gate breaks the fixture/v1 workflows" | **REFUTED, by making it opt-in and measuring both sides** — plain `verify` on the EX-35 `v1-partial-1of5` fixture reads `MATCH-V1-PARTIAL exit 0` (declared default); with the gate it reads `USAGE 2` + `REFERENCE-COVERAGE 1/5` | `matrix-after.txt` L5/L8 |
| A4 | EX-35 Change 1 (v1 compliance mode → exit 0) as part of this closure | **DECLINED** — the round-2 verdict ruled v1 verifiability is the `SHA256-CONTRACT` line, not an exit-0 promise, and both numbers must keep being quoted together; adding a second exit-0 path invites a gate that can no longer distinguish a label-defective v1 stanza from a clean pair | verdict.md §"Wording ruling"; this plan §4.5 |
| A5 | EX-35 Change 3 (blanket `try/except` around dispatch → exit 2) | **DECLINED** — it would present genuine programming errors as USAGE and hide the very defect class D2 closed; the residual crash class is now typed by construction | this plan §1 D2 |
| A6 | "the D2 class swallows absent paths" | **REFUTED** — an `ENOENT` keeps `EXISTS: no` with no error marker and stays `ABSENT 13`; the base case `absent-path-detected` (legacy case 5) is green on the candidate, and L2/L3 differ only by the error markers | `selftest-candidate.out`; `matrix-after.txt` L2/L3 |
| A7 | "the write-guard extension over-refuses the tool's own receipts" | **REFUTED** — receipts written next to a fixture (`--out …/pre.txt`) are never in `set(paths)`; every legacy selftest case writes receipts beside its fixtures and the 22/22 run proves no over-refusal | `selftest-candidate.out` |
| A8 | "selftest case 7 tests anything real" | **CONFIRMED DEFECT (base)** — a renamed copy's case 7 spawns the sibling *name*: measured `FAIL (capture failed under TZ=UTC: can't open file '<dir>/custody-pair.py')` → `DIRTY cases=15 passed=14 failed=1 exit=3`; where a sibling of that name exists, that file is what gets tested. Closed by H13 (`TOOL_PATH`): the renamed candidate copy reads `CLEAN cases=22 passed=22 exit=0` | `custody-pair.py:733`; `/var/tmp/pl2/probe/renamed.out`, `renamedcand.out` |
| A9 | "the v1 statement holds unchanged at HEAD" | **PARTIALLY REFUTED** — the sha256 *contract* holds (`SHA256-CONTRACT` prints, drift caught) but the round-1 receipts now read `CONTENT-DRIFT exit 10 / 4-of-5` against live, because of the recorded operator Kimi-config drift; the plan states the live number and isolates class control runs on fixtures | L8; §4.5 |
| A10 | "the candidate moved a custody path" | **REFUTED** — L9 digests identical to the pre-matrix state and to the round-1 pins except the pre-existing path-3 drift; all runs read-only | `matrix-before.txt`/`matrix-after.txt` L9 |

## 7. Residuals this plan does NOT close (named, for the round record)

- **D1** capture TOCTOU (2/300), **D4** receipt self-authentication (the
  sidecar is not an anchor), **D5** out-of-band/root class (tripwire for
  attribution, not an integrity control against a shared trust domain), **D7's**
  TOCTOU remainder — unchanged by this patch; the inode arm closes only the
  *static* alias case.
- The **sidecar path** is not scope-checked (`--out X.sha256 --paths X` can
  still aim a sidecar at a measured file's neighbour); out of scope, stated so
  the row does not claim more than the code does.
- `--require-paths 0` / negative N is treated as "no gate" (falsy). Optional
  USAGE arm left to EX-21; unconditional refusal would be stricter but is not
  what the claim names.
- Under euid 0 the three permission cases pass trivially — the declared exit
  classes arm only for non-root runs; the matrix and selftest runs here were
  non-root (`vgpnk`).
- **Coupled-record risk**: the README/registry clauses in §4 are
  revision-pinned by nature; if EX-21 adapts the payload (e.g. drops H9b), the
  case count becomes 21 and every downstream count must move in the same
  commit.
- Command A / census / probe at the *work commit* are parent-side re-runs; the
  values here are the HEAD baseline, not the landing.

## 8. Application recipe for EX-21

```sh
# 1. verify the base identity first (the generator refuses a moved base)
sha256sum .ufo/gates/custody-pair/custody-pair.py   # expect 112d01dc…, 889 lines
python3 <this-dir>/gen-candidate.py .ufo/gates/custody-pair/custody-pair.py /var/tmp/ex21/candidate.py
#    or: patch -p0 < <this-dir>/candidate.patch   (paths a/ b/ are repo-relative)
# 2. measure the candidate exactly as this plan did
bash <this-dir>/verify-candidate.sh /var/tmp/ex21/candidate.py /var/tmp/ex21/out
# 3. only if every declared class reproduces: install the candidate bytes into
#    .ufo/gates/custody-pair/custody-pair.py, then re-derive every identity
#    (tool sha, case count, receipts) and land the §4 coupled set.
```

The generator asserts every anchor occurs exactly once (22/22 ok at
`gen-candidate.py` run, output in the seat report), so a moved base cannot
mis-apply silently. Dropping the optional hardlink arm = deleting the `H9b` and
case-19 entries from the generator's transform table; the rest is independent.

## 9. Landing status (measured 13:12–13:14Z — the real target is live)

EX-21 is landing the hardening directly while this plan was being written. Every
revision below was copied read-only to `/var/tmp/pl2` (never `/tmp`), two reads
per revision identical, and measured by this seat:

| revision | lines | selftest (measured here) | state vs this plan |
|---|---|---|---|
| `112d01dc…` | 889 | `CLEAN cases=15 passed=15 failed=0 exit=0` | the plan's base — every "before" column above |
| `73c15b84…` | 1109 | **`DIRTY cases=21 passed=20 failed=1 exit=3`** — `require-paths-blocks-partial-reference`: `TypeError: _run_verify() got an unexpected keyword argument 'require_paths'` | interim: the four closures are present, but the claim's "selftest … at exit 0" clause was unmet at this revision; two fixes measured, record `landed-fix.patch.md` |
| `7cd19c3c…` | 1155 | `CLEAN cases=22 passed=22 failed=0 exit=0` | **full convergence**: the four closures reproduce exactly as declared in §1, the 22 case names are this plan's §3 set verbatim, and case 7 now uses `TOOL_PATH` (the §2.2 identity arm) |

Independent verification of the landed bytes this seat ran
(`matrix-landed2.txt`, against the `7cd19c3c…` snapshot): L1 `USAGE 2` (no
traceback), L2/L3/L4 `UNEVALUABLE 14` with `VERDICT: MATCH` absent everywhere,
L5 plain `0` / gated `USAGE 2` + `REFERENCE-COVERAGE: 1/5 … unaccounted: 4
paths`, L6 both guards `USAGE 2` with target bytes unchanged, L7 live pair
`MATCH 5/5 exit 0` with and without `--require-paths 5`, L8 v1 fixture classes
identical to the base, L9 custody digests unchanged. The declared classes are
therefore the **landed behaviour**, not a proposal; the parallel candidate
`6b377964…` remains this plan's proof-of-measurement and is no longer the
artifact of record.

Still owed for the claim's same-commit coupling (checked 13:14Z; `landed-fix.patch.md`
carries the same list):
- `.ufo/gates/custody-pair/README.md`: `grep -c UNEVALUABLE` = **0** — the exit
  table (`:87-95`) has no `| 14 | UNEVALUABLE |` row, the capture paragraph
  (`:96-98`) still reads `0`/`13` only, and the precedence line (`:101-102`)
  still omits `UNEVALUABLE`; the selftest paragraph is already `22 cases`
  (`:124-135`).
- `SKILL.md:390`: the row still says `15 fixture cases`, its worst-finding map
  has no `14`, and its precedence string omits `UNEVALUABLE` (one voice lands
  the merged row — round-2 D10).
- The round's live pre/post pair must be captured by the **landed** revision so
  each receipt self-pins `7cd19c3c…` (or whatever revision lands); the pair in
  this directory pins the candidate `6b377964…` and is evidence for this plan,
  not the round's receipt.