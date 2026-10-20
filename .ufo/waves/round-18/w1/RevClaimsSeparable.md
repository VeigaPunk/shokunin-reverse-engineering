# RevClaimsSeparable — C1/C2/C3: separability, axes, falsifiers

Seat `KaidokuR18.RevClaimsSeparable`, 2026-10-20. Author-side advisory review of
`.ufo/waves/round-18/claims.json` (mtime 12:18:40) against `.ufo/waves/round-18/contract.md`
(mtime 12:37:59, including the "Amendments at wave-1 integration" block at `:148-152`), the
routed-defect source, the delivered W18 tools, and baseline Git objects at `9011581`.
Read-only: no lane file edited, no jj/git write, no REA, no Ghidra, no carrier executed. Only
this report was written. The worktree moved during the review; observations that name
worktree files are the bytes at the last read and are labeled so.

## Bottom line

1. **C1 is not separable from C3.** C1's R17-PINMAP closure requires check (d): the literal
   `map_sha256` in `.ufo/waves/round-17/tools/carrier-run.py` (`contract.md:32`). C3 owns the
   only edit that adds it (`contract.md:128-130`), and that edit landed mid-review. C1's
   terminal zero therefore closes through C3's file. The dependency is one-directional.
2. **C2's after-zero is a false negative.** `claims.json:20` says "3 at 9011581 -> 0"; the
   12:40 tool yields 3 at baseline (credit), but its `--selftest` fails
   (`SELFTEST: FAILED (14, …)`, exit 1), and a delivered-shape test yields `live_count: 0`
   while two intra-file wrapper-wrapped `HEAD` reads (`revpin.py:108`, `verify.py:82`) vanish
   from `sites`. The 0 comes from a scanner blind spot, not from removing the reads.
3. **C3's claim is stale against its own contract.** `claims.json:26-27` still says eight
   synthetic carriers and `0 -> 8`; the amended contract specifies 12 synthetic + 2
   calibration labels, an H1/H0 decision rule, and the D set (`contract.md:151`).
4. **Axes are distinct labels**, but only C1/C3 sit on owned axes (calibration and depth, both
   at the 10.0 ceiling); C2's operability is an explicitly unowned fleet proxy.

| Claim | Axis | Verifiable without the others? | Counting command | Verdict |
|---|---|---|---|---|
| C1 | calibration | **No** — `(d)` is a content test on C3's `carrier-run.py` (atom landed mid-review) | `routed-defects.py` named (baseline 6 confirmed); QUALITY 20→21 half is `controls.py`'s job | joint C1+C3 |
| C2 | operability | **Yes** vs C1/C3; **no** vs its own after-zero | `head-rev-lint.py` named (baseline 3 matches; after 0 is a false negative; selftest red) | after not falsifiable |
| C3 | depth | **Yes** — no C1/C2 file read | none named; `measure.py` projection counts field presence | stale count |

## Axis check [observation]

- `SCORECARD.md:23-25` — Owned axes: coverage `9.72 → 10.0`, depth `10 → 10`, calibration
  `0 → 10`; current values tie at 10.0, matching `claims.json:7`.
- `SCORECARD.md:469,490` — operability is labelled "fleet axis, unowned proxy"; C2 cannot
  move an owned score. Say that in the claim.
- Calibration is at its ceiling; round 17 recorded `10.0→10.0, delta 0` (`SCORECARD.md:2363`).
  C1 is defect-discharge credit, not a score increase.
- C3's change set is half operability plumbing (`log-extract.py`, `compare.py`,
  `carrier-run.py`, `run-carriers.sh`; `contract.md:123-137`). Do not double-count that as
  depth; the depth atom is the prediction↔log comparison.

## Findings

### P1 — C1's terminal zero is gated on C3's `carrier-run.py` (hard coupling)

[observation] `contract.md:29-32` closes R17-PINMAP only if all four checks pass; `(d)` is
"`.ufo/waves/round-17/tools/carrier-run.py` contains the literal `map_sha256`"
(`contract.md:32`). At the baseline it is absent:

```
$ git grep -n 'map_sha256' 9011581 -- .ufo/waves/round-17/tools/carrier-run.py
(no output)                                  exit 1
```

The delivered checker implements that gate and confirms 6 open at baseline:

```
$ python3 -I -B .ufo/waves/round-18/tools/routed-defects.py --root . --rev 9011581
{... "open_count": 6 ...}                    exit 0
$ ... --strict                               exit 1
$ ... --selftest
SELFTEST: CLEAN cases=10                     exit 0
```

Check (d) is `carrier-run-retains-map`, `.ufo/waves/round-18/tools/routed-defects.py:144-151`,
reading `CARRIER_RUN` at REV (`:35`). Mid-review the atom arrived from C3's side: the
worktree now has `carrier-run.py:511 check["map_sha256"] = ...` and `git status --porcelain`
lists `M .ufo/waves/round-17/tools/carrier-run.py`; at review start the worktree matched
9011581 (`grep` → exit 1). C1's zero therefore closes through C3's file, not C1's.

Two consequences:

- The routed defect offers a disjunction — "Either retain mid maps (or their digest) or
  append a named correction" (`corpus/lessons/round-17-verifier-spotcheck.md:137`) — but the
  contract requires both branches: `comparator verdict` text in `(a)/(b)` and the retention
  literal in `(d)`. The connector's chosen sentence says "mid-run instants retain the
  comparator verdict against the retained pre map, **not the map**"
  (`DraftPinmapCorrection.md:31`). Green C1 can therefore assert both that mid maps are not
  retained and that the tool retains them.
- C3's **claim text** (`claims.json:26`) covers carriers, predictions and logs only; the
  mid-map retention is contract-only work not claimed by C3. Nothing in the claims allocates
  it, so a later edit could remove `map_sha256` and reopen C1 while C3 stays green.

The contract's own remedy is only half implemented: `contract.md:149` says routed-defects
reports `named_correction` **and** `substance` per defect, but the 12:34 tool bytes emit only
the old check names (`knowledge-names-correction`, `carrier-run-retains-map`, …) — no
`named_correction` or `substance` field in the JSON I ran. So C1's stated closure predicate
and its measuring tool currently disagree.

Fix: pick one owner for the `map_sha256` atom. Preferred: drop `(d)` from truth-closure and
record the retention as C3's atom (add it to C3's claim and falsifier); keep C1 on the
correction text plus the QUALITY row. If the joint verdict is wanted, say so in
`falsifiable_before_after` ("`open_count 0` at the delivered rev, conditional on C3") and
make `(a)/(b)` branch-consistent: retention route → require `mid` + `map` + `retained` and
reject "not the map"; correction route → no `(d)`. Implement the `named_correction`/
`substance` split before measuring, or withdraw it from the contract.

### P1 — C2's after-zero is a false negative, and its selftest is red

[observation] `claims.json:20` states "live HEAD-as-revision call sites 3 at 9011581 -> 0".
The tool at its 12:40 revision yields exactly 3 at the baseline, so the **before** number
reproduces (credit; the 12:38 bytes yielded 7 before the seat-dir exclusions landed):

```
$ python3 -I -B .ufo/waves/round-18/tools/head-rev-lint.py --root . --rev 9011581
{"live_count": 3, "fixture_count": 6, "annotated_count": 0,
 "files_scanned": 27, "excluded": [10 paths], ...}                  exit 0
$ ... --strict                                                      exit 1
```

Live: `citation-drift-probe.py:477` (default-HEAD), `custody-pair.py:327`
(rev-parse-HEAD), `round-17/verify.py:59`. The w[0-9]/ seat dirs and `/fixtures/` paths are
listed under `excluded` (10 paths), as `contract.md:150` requires.

The selftest is red. At 12:40 it crashed with `AttributeError` at `:539` because
`_fixture_git` (`:520-526`) had no `return`; the 12:43 bytes fix that and now print the
contract's failure form:

```
$ python3 -I -B .ufo/waves/round-18/tools/head-rev-lint.py --selftest
SELFTEST: FAILED (14, [ {site...}, ... ])                            exit 1
```

The payload is a 14-site result, not the single expected case the assertion wants, so the
tool still fails its own acceptance and still has no green case proving the amended rules.

The after-number is the problem. A delivered-shape test — the current bytes of `revpin.py`,
`verify.py`, `controls.py`, `custody-pair.py`, `citation-drift-probe.py` committed in a
mkdtemp repo outside LANE — reports:

```
{"live_count": 0, "annotated_count": 4, "fixture_count": 4,
 "files_scanned": 5, ...}                                            exit 0
annotated citation-drift:304, custody-pair:381/1350/1353
fixture   citation-drift:452, custody-pair:1352, controls:442, revpin:218
```

Two real HEAD-as-revision reads are **absent from `sites` altogether**:
`revpin.py:108` (`_resolve(lane, "HEAD^{commit}")`, helper `:79-84` runs
`git rev-parse --verify --quiet <rev>`) and `verify.py:81-82`
(`_git_or_none("rev-parse","--verify","HEAD^{commit}")`). Both are intra-file wrapper call
sites with a literal `HEAD`; the tool's own `limits` excuse only cross-module wrappers, so
this is a false negative, not a documented boundary. `live_count: 0` is therefore produced by
invisibility, not by the absence of the reads, and the claim's after-zero inherits that
ambiguity.

[inference] A delivered-rev run of this lint can report `live_count: 0` while both real
witness reads still exist. The number then measures the scanner's field of view, not the
lane's exposure.

Fix, in order: (1) `return subprocess.run(...)` in `_fixture_git`, then re-run `--selftest`;
(2) add detection for the two intra-file wrapper call-site forms (`helper(name, "HEAD…")`
and `helper("rev-parse", …, "HEAD…")`) with red cases that must be caught — today they
vanish; (3) make the lint list `annotated` sites (it now reports only the count) and require
`live_count: 0` to be reported alongside `annotated` plus a declared wrapper allowlist;
(4) in claims.json, state "baseline 3 at tool revision X; after 0 under the same rule, with
annotated sites listed" rather than a bare 0, so the after cannot be satisfied by a blind
spot. Annotating `revpin.py:108` is acceptable only if the annotation list is part of the
evidence.

### P1 — claims.json was not updated with the contract amendments (C1/C2/C3 drift)

[observation] `claims.json` mtime 12:18:40; `contract.md` mtime 12:37:59. The amendment block
(`contract.md:148-152`) changes all three falsifiers, but the claims still carry the old text:

- **C1** (`claims.json:11`) still says "tool fixes" although the only W17 tool fix is C3's;
  the amended closure predicate is `named_correction` AND `substance` (`contract.md:149`).
- **C2** (`:20`) still says "3 at 9011581 -> 0"; the contract now says "The baseline number
  is whatever this rule yields; it is not tuned to 3" (`contract.md:150`). The 12:40 tool
  happens to yield 3, so the before-number is currently right, but the claim names neither
  the rule revision nor the annotated sites, and its after-0 rests on the blind spot above.
- **C3** (`:26-27`) still says "eight deterministic synthetic carriers … 0 -> 8"; the
  contract now specifies "12 synthetic + 2 calibration labels", H1/H0 per-carrier
  predictions, D = carriers where H1 and H0 differ, and a frozen
  `W18/predictions/decision-rule.json` (`contract.md:151`).

A verifier replaying claims.json will measure the wrong quantities, and C3 will fail its own
contract by construction. Fix: regenerate claims.json from the amended contract before
integration (numbers, carrier set, and the C1 predicate), and keep the two files'
timestamps/order explicit.

### P2 — validate16 evidence is pinned by the artifact, not by the check

[observation] `contract.md:33-35` defines `summary.json` as `{rev, receipts:[{exit:int}]}`
only, and the delivered check verifies only `rev`, the eight int exits, and the two text
lines. The receipts at `da64646` are 8 (`git ls-tree -r --name-only da64646 | grep -c
'/receipt.json$'` → 8, exit 0). Credit: the produced artifact goes further — it carries
`validator_rev = 9011581…` and `validator_sha256 = 618448…`, and that sha equals
`sha256(git show 9011581:.ufo/waves/round-17/tools/receipt-validate.py)` (`sha256sum` →
`618448…`, exit 0). The worktree validator is a different blob (`3add13…`), so the retained
exits provably come from the baseline validator, not C3's edit. That removes the
order-dependence I expected.

What remains: (i) `routed-defects.py` neither requires nor verifies the pin, so an unpinned
summary still closes R17-VALIDATE16; (ii) QUALITY #18 ("Execution evidence retains the
producing argv/snippet, measured revision, stdout/stderr and exit", `corpus/QUALITY.md:28`)
is met by the executor's care, not by the contract. Fix: add
`validator_rev`/`validator_sha256` (plus `argv`, `cwd`) to the schema and require both in the
check, asserting the sha against the blob at `validator_rev`.

### P2 — C3 has no counting command; the projection measures schema adoption

[observation] `claims.json:27` names no command and gives "0 -> 8 (compare exit per carrier
reported, match or not)". The shared instrument counts `W18/runs/*/compare.json` files whose
`fields[]` carry an `extra.eof_reads` or `extra.analyzer_errors_empty` entry
(`contract.md:139-141`), and `measure.py` says of itself: "C3 counts compare.json `fields[]`
entries whose `field` is exactly one of the two names; it re-derives no all_match and
re-reads no run log", and "C3 all_match is the value the artifact itself records, copied, not
verified" (`measure.py:66-68`; projection `:12-14`, `:377-445`). That is schema adoption, not
a prediction-versus-log comparison. At review start `W18/predictions`, `runs` and `tools`
were absent (`ls` exit 2); mid-review `predictions/carriers.tsv` and `tools/` appeared,
`runs/` has not. So the baseline "0" is could-not-evaluate, and a total refutation still
scores 8.

Fix: name the command in the claim and make it measure the amended C3: `labels_total` (12
synthetic + 2 calibration), `predictions_frozen_rev`, `labels_compared`,
`D = |{carrier: H1 differs from H0 on a logged field}|`, per-label `match`, and the
frozen-rule verdict; require each run's recorded rev to descend from the freeze rev (else
exit 2); report the baseline as `exit 2, no predictions/runs`, not 0.

### P2 — C1's two-part falsifier is split across two instruments

[observation] "QUALITY data rows 20 → 21 with rows 1-20 byte-identical" (`claims.json:13`)
is not measured by `routed-defects.py`; `contract.md:142-145` assigns it to `controls.py`,
which the claim does not name. The numbers are right: QUALITY has exactly 20 admission data
rows at baseline (max id 20; `awk NR 11-31` count → 20, exit 0). Fix: add `quality_rows` and
`quality_prefix_identical` (rows 1-20 at REV vs 9011581) to `routed-defects.py`, or name
`controls.py` in the claim.

### P3 — C1 check `(c)` under-constrains the QUALITY row

`contract.md:30-31` tests only that the why-cell contains the two literals. The connector's
draft chooses `sharpens 19` and cites `corpus/lessons/round-18.md`
(`DraftQualityRow21.md:10,22,28`), which does not exist yet; a row with `—` and a dangling
lesson link would pass, violating the table header (`corpus/QUALITY.md:9-10`) and QUALITY #1
(`corpus/QUALITY.md:11`). Fix: require the supersedes cell to contain `19`, and that every
`corpus/lessons/*.md` path named in the row exists at REV.

### P3 — C2 `--repo` default is off by one directory

`custody-pair.py` is at `LANE/.ufo/gates/custody-pair/custody-pair.py`; `Path(...).parents`
are `[custody-pair, gates, .ufo, LANE]`, so "the lane root two levels above the script"
(`contract.md:78-79`) resolves to `LANE/.ufo`. The new `# repo-root:` would record the wrong
root (git still works by walking up, hiding it). Fix: `parents[3]` or
`git rev-parse --show-toplevel`, asserted against the expected lane root.

### P3 — C2's receipt format should state the v2 outcome

`contract.md:81` says `compare` "must treat these as metadata exactly as it treats
`# repo-HEAD:`". `compare` skips every `#` line (`custody-pair.py:465`) and
`RECEIPT_VERSION = 2` (`custody-pair.py:187`). Keeping v2 is correct; say so, so an executor
does not bump the version and break the retained r17 receipts.

### P3 — C2 citation root ambiguous; `sourced` ids not machine-checkable

`.ufo/waves/hyaku/jj-w1/reports/JjAuditKaidoku.md` does not exist under LANE
(`ls .ufo/waves/hyaku/` → exit 2); it exists at
`/home/vgpnk/Projects/shokunin/.ufo/waves/hyaku/jj-w1/reports/JjAuditKaidoku.md`. The lane
does cite bare fleet-root docs (`CORPUS.md`, `PROTOCOL.md`), so this is ambiguity, not a dead
pointer; prefix it. Also: SOURCES has 32 rows `S001-S032` (`grep -c '^| S[0-9]'` → 32, exit
0); S033 does not exist yet. C1 names S033; C2 (`:21`) and C3 (`:28`) name no id, so the
`frontier_step` requirement "C1-C3 cite rows opened this round" cannot be checked. Assign
provisional ids and assert existence at REV.

### P3 — `jj-red-before` step (3) still needs a non-repo cwd

The amendment removes the clone's origin and isolates HOME/XDG (`contract.md:152`), which is
good. Step (3) still says "baseline vs fixed custody-pair `capture` against `sb`"
(`contract.md:94-95`). If the harness runs with cwd = LANE, the baseline `Path.cwd()` defect
does not show. Run the baseline invocation from an empty `mkdtemp` so it records `(none)`/
the wrong repo, and the fixed `--repo sb` records the sandbox.

## Commands and exits

All read-only; baseline reads use `9011581:` Git objects. The worktree changed mid-review
(see residual risk), so worktree results are timestamped by state.

1. `git rev-parse --verify 9011581^{commit}` → the hash, **exit 0**; `HEAD` and
   `refs/heads/main` both resolve to it; `git status --porcelain -uno` → 0 lines at review
   start.
2. `git grep -n 'map_sha256' 9011581 -- .ufo/waves/round-17/tools/carrier-run.py` →
   **exit 1** (no match); worktree `grep` → **exit 1 at review start**, now matches
   `carrier-run.py:511` after C3's edit.
3. `python3 -I -B .ufo/waves/round-18/tools/routed-defects.py --root . --rev 9011581` →
   `open_count: 6`, **exit 0**; `--strict` → **exit 1**; `--selftest` →
   `SELFTEST: CLEAN cases=10`, **exit 0**.
4. `head-rev-lint.py --root . --rev 9011581` (12:43 bytes) → `live 3, fixture 8,
   annotated 0, files 27, excluded 10`, **exit 0**; `--strict` → **exit 1**. Live:
   citation-drift:477, custody-pair:327, round-17/verify:59. The 12:38 bytes gave `live 7`
   (seat dirs not yet excluded); that run is superseded.
5. `head-rev-lint.py --selftest` (12:43 bytes) → `SELFTEST: FAILED (14, [...])`, **exit 1**.
   At 12:40 the same command crashed with `AttributeError` at `:539` (`_fixture_git` had no
   `return`); that bug is fixed, the selftest still fails.
6. Temp-repo delivered-shape lint (12:43 bytes): `live 0, annotated 4, fixture 4, files 5`,
   **exit 0**; annotated citation-drift:304, custody-pair:381/1350/1353; fixture
   citation-drift:452, custody-pair:1352, controls:442, revpin:218. `revpin.py:108` and
   `verify.py:81-82` are absent from `sites` although they are intra-file wrapper call sites
   with literal `HEAD`. Output has `annotated_count` and `excluded` keys.
7. `git config --get init.defaultBranch` → `master`, **exit 0**. The selftest passes
   `git init -b main`, so the default branch is not the failure cause; the 12:40 crash was
   the missing `return`, the 12:43 failure is a payload mismatch.
8. `sha256sum` of `git show 9011581:.ufo/waves/round-17/tools/receipt-validate.py` →
   `618448…`, equal to `summary.json`'s `validator_sha256`; worktree blob `3add13…`;
   **exit 0**.
9. `git ls-tree -r --name-only da64646 | grep -c '/receipt.json$'` → `8`, **exit 0**.
10. QUALITY admission rows: `awk 'NR>=11 && NR<=31 && /^\| /' corpus/QUALITY.md | wc -l` →
    `20`, **exit 0**; SOURCES `grep -c '^| S[0-9]'` → `32`, **exit 0**.
11. `git show 9011581:.ufo/waves/round-17/predictions/SHA256SUMS` → **exit 0**; no
    `carriers.tsv` line; `carriers.tsv` blob sha256 = `8ac38afe…` (R17-SUMS-RUNLOG red at
    baseline).
12. Six routed ids in `SCORECARD.md LOG.md SKILL.md corpus/knowledge corpus/SOURCES.md
    corpus/QUALITY.md` at 9011581: each `git grep -l` produced no file (`git grep` exits 1
    on no match; the `| head` pipeline exits 0); `grep -c 'Write scope:'` in SKILL.md → `0`,
    **exit 1**.
13. `command -v jj` → **exit 0**, `jj 0.45.1-7c41cdeb…`; `python3 -V` → 3.14.8. The
    jj-red-before prerequisites are present; the sandbox itself was not run here.
14. `git status --porcelain` → 7 `M` entries (`citation-drift-probe.py`, `custody-pair.py`,
    `carrier-run.py`, `compare.py`, `log-extract.py`, `receipt-validate.py`, `verify.py`)
    plus untracked W18 files; this report is untracked. **exit 0**. `stat` mtimes:
    claims 12:18:40, contract 12:37:59.

## Residual risk and gaps

- The worktree moved during the review: the contract was amended at 12:37 (after
  `claims.json` at 12:18), C3's `carrier-run.py` edit landed, `verify.py` changed shape
  twice (a `git log -n1` form, then `rev-parse --verify HEAD^{commit}` with a
  `# head-rev-lint: compare-only` marker), and `head-rev-lint.py` changed at 12:40 and
  12:43 (the 12:40 selftest crashed; the 12:43 one fails). Baseline claims here are read
  from `9011581:` objects; worktree observations are the bytes at the last read.
- `head-rev-lint.py --selftest` is red; `jj-red-before.py` exists but was not run (it clones
  the lane; not needed for this review). `swiss-misread.py` is still absent, so C3's
  emulator could not be inspected.
- The baseline count moved during review: the 12:38 lint (37 files, live 7) predates the
  seat-dir exclusion; the 12:40 revision reports live 3 over 27 files and matches the claim.
  My independent scan of the same baseline (37 files, live 7) used the pre-amendment rule and
  is superseded; it is retained only to show which sites the amendment had to remove.
- The temp-repo test is a reconstruction from current bytes, not the delivered rev; it tests
  the lint's rule, not the lane's final commit.
- No REA analyze/search/decompile, no Ghidra, no `analyzeHeadless`, no carrier execution.
  No installs or updates were needed or performed.
