# R66 counter review (ReviewerClosure, w1, round 66)

Read-only review of the two frozen counters against the two frozen predicates.
Nothing outside this report directory was written; no scratch was created; no tools
were installed. No `lsp` device/server was available for these `.py` files in this
session — all checks are text + programmatic (ast constant extraction, sha256, git
read-only), recorded per role rules; grep output below is text evidence, never
semantic proof.

Evidence commands run: `sha256sum` over both counters and both r65 instruments
(all four pins match the declared values: `3c5cfb03…`, `1be9d046…`, `79a4dca4…`,
`9434888e…`); a python3/ast extraction that hashed every predicate sentence site;
read-only git (`log --diff-filter=A`, `merge-base --is-ancestor`, `diff --stat`,
`ls-tree -r`, `status --porcelain`, `cat-file`); full reads of both counters, the
plan, the container, all six `l1/pre` + `l1/controls` bytes, the r65 instrument
(anchor ranges), and the r65 reviewer report.

## 1. Clause-to-line trace (QUALITY #87)

### R66-C1 — `tools/round-66/closure-boundary.py` (473 lines)

| clause | implementing lines | verdict |
|---|---|---|
| a1 guarded probe leaves `closure.ok` true with an empty cache | `run_verify` a1 block 237–246: fixture built 238 (`write_fixture` 172–179), `closure_state` 239–242, condition `ok is True and cache_present == [] and count_ok is True` 243–244; guarded `-B` argv 185 + env 187–188 (`mod.SUBPROCESS_ENV` = `PYTHONDONTWRITEBYTECODE=1`, r65 L129); post-probe cache scan 138, folded into `ok` 156–157 | implemented |
| a2 same probe unguarded makes `ok` false and names a `.pyc` | a2 block 248–258: `guarded=False` 252, env pops 189–191, `named_pyc` 254, condition `ok is False and bool(named_pyc) and probe ok` 255–256 | implemented |
| a3 frozen 30-entry manifest verifies with `count_ok` true | a3 block 263–268: `closure_state(mod, toolchain, …, dict(mod.CLOSURE), COUNT, real_probe…)` 263–264; count `entries = len(manifest)+3` / `count_ok` 139–140; condition 265–266; `COUNT = 30` L67 | implemented |
| a4 one-short manifest reports `entries 29 != 30` and `ok` false | a4 block 269–278: truncated manifest 270–272 (drops lexicographically first key), condition 275–277 requires the literal `count 29 != 30`, emitted only by `closure_state` 154–155 | implemented |
| a5 `--skip-run` emits no closure object claiming ok | `skip_run_receipt` 316–321 (`closure: None`, `closure_claimed: False`); arm 282–286; CLI dispatch `main` 438+ (`if args.skip_run` → same constructor → `emit` 324–329) | implemented |
| kill-rule support: r65 drift refusal | `load_v1` 92–104 (pin check 98–99); absent toolchain → exit 2 at 260–262 | implemented |

### R66-C2 — `tools/round-66/coverage-selfcheck.py` (438 lines)

| clause | implementing lines | verdict |
|---|---|---|
| `recipe_a_equivalent` true | `recipe_a_equivalence` 191–211: extraction 173–188, subprocess 196–201 (`sys.executable -I -B`, cwd=root), `diffs` over `RECIPE_A_KEYS` 206–207 (keys 73–75), flag `not diffs` 208; `--equiv` gate 408–413; `selfcheck` gate 269–270, emitted 271–273 | implemented |
| `recipe_a_hidden` non-empty | `recipe_hidden` 153–156 (sorted name list), emitted 267 + 274–277, gate `bool(hidden)` 269–270; also emitted by `--recipe a` 415–421 | implemented |
| `mismatches` 0 across the two atoms | atoms A1/A2 built 257–264, `mismatches = sum(1 for a in atoms if not a["ok"])` 268, gate 269–270, exit 0/1 in the selfcheck return 271–280 | implemented |
| base arm (cited-fraction atom false at base) | same atom code 257–264 evaluated at `--rev <base>` by external invocation; **no dedicated enforcing line inside the counter** — the demonstration is the committed receipt `l1/pre/dryrun-c2-selfcheck-at-base.json` (A2 `ok:false`, claimed `[142,142]` vs observed `[145,145]`). Per #87 this is a claim-process arm backed by a receipt, not a counter-internal check | implemented externally (named) |
| could-not-evaluate shapes | `parse_row` raises 229–243; `main` catch → exit 2 (429–436) | implemented |

No clause of either predicate is without an implementing line (the C2 base arm is
implemented externally and is named above, as #87 requires).

## 2. Boundary hunt — can any arm pass without its defect present?

- **a1**: cannot pass with a broken guard — an unguarded write makes `post_cache`
  non-empty → `ok` false (156–157) → arm red. a1 cannot detect the *ordering* defect
  C1-F1 (a guarded run never writes cache, so scan order is unobservable here); that
  is a2's job, and a2 does it: with a pre-probe-only scan `st2.ok` would be true
  (`cache_before == []`), the arm condition 255 would fail — exactly what the
  committed control shows (`c1-do-nothing.json` a2: `r65_order_state.cache_present: []`,
  `control_meets_r66_arm: false`). No bypass.
- **a2**: no bypass found. The fixture state is constructed so the *only* source of
  `ok:false` is `post_cache`: the manifest is the pre-probe pins of a fresh root
  (`write_fixture` refuses an existing root, 173–174), count is exactly 5 = 2+3, and
  probe success is asserted separately (256). Removing the post-probe check flips
  `ok` true and fails the arm. The probe's only write surface is `root/__pycache__`
  (`PYTHONPYCACHEPREFIX` popped both branches, 191).
- **a3**: not vacuous — `count_ok`/`entries` are computed inside `closure_state`
  (139–140); a counter that dropped the count computation would KeyError the arm
  condition (crash, no receipt), not pass. Constants cross-checked by selftest
  (`count-constant`, `v1-closure-entries`, selftest-c1.txt PASS 30/30).
- **a4**: no bypass. The required finding literal `count 29 != 30` (277) can only be
  produced by the count-emission line (154–155) with `entries==29, expected==30`;
  dropping the lexicographically-first key leaves the file on disk (no
  missing/pin noise), so the count finding is the sole red driver — a clean isolation
  of C1-F2. `ok:false`/`count_ok:false` hold structurally.
- **a5**: passes iff the new counter's own receipt claims no closure — the repair is
  structural (`closure: None`, 318–320), so no defect-present pass exists. Residual
  (F11): a5 exercises the constructor in-process (282), not a CLI spawn+parse of
  `--skip-run`; and the r65 `--skip-run` remains defective on this host by design
  (frozen bytes) — the claim repairs by replacement, not removal.
- **C2 equivalence**: identity over the nine declared keys (206–207) is the declared
  equivalence; extra block keys are ignored but recorded (`recipe_a_block_keys`,
  210) for forensics. A crashing block is exit 2, never a pass (199–201).
- **C2 hidden list**: the list itself is the repair of M65-4 (names, not an integer);
  non-emptiness gated at 269–270.
- **C2 mismatches**: both atoms bind the row to the stem recipe at the same rev, so
  a stale row cannot pass — except one first-match vector: `parse_row` takes the
  **first** `<n>/<n> knowledge files` in the row (239). A row rewritten to carry a
  fresh fraction *ahead of* a stale one would pass A2 while a stale number remains.
  The row is controlled text written by the same round; flagged as F9.
- **Base arm**: enforced by receipt inspection only (see trace); nothing prevents a
  future run from skipping it — it is outside the counter's exit computation by
  design.

## 3. QUALITY #68 — predicate byte-identity (sha256 of the sentence bytes, no trailing newline)

| site | location | sha256 |
|---|---|---|
| C1 plan | `plans/round-66-claims.md:35` | `f8c8edb4bcc8a075e1d2e95cfe42403d9bc35fddf9d53116966035e838cdf342` |
| C1 container | `.ufo/waves/round-66/claims.json:16` (`.claims.R66-C1.predicate`) | `f8c8edb4…cdf342` (identical) |
| C1 counter constant | `closure-boundary.py:68–76` (`PREDICATE`) | `f8c8edb4…cdf342` (identical) |
| C1 receipt | `l1/pre/dryrun-c1-verify.json` `.predicate` | `f8c8edb4…cdf342` (identical) |
| C2 plan | `plans/round-66-claims.md:74` | `d5df2ccd668648dcac02eace85aeac2e82d7c89066ce1174570669ce9ace8c24` |
| C2 container | `claims.json:24` | `d5df2ccd…ace8c24` (identical) |
| C2 counter constant | `coverage-selfcheck.py:60–65` | `d5df2ccd…ace8c24` (identical) |
| C2 receipt | `l1/pre/dryrun-c2-selfcheck-at-base.json` `.predicate` | `d5df2ccd…ace8c24` (identical) |

Byte-identity holds at every site that carries a sentence. Two row-68 deviations:

- **Mechanism clause unimplemented (F1).** Row 68 requires the counting command to
  "read the predicate from the claim file rather than echoing a constant". Neither
  counter opens `claims.json` (grep: zero reads; `json.loads` appears only for the
  equiv subprocess stdout); both echo their `PREDICATE` constants into receipts
  (`closure-boundary.py:289`, `coverage-selfcheck.py:271/410/417/425`). A future
  container-side predicate edit would not be caught by the counters.
- **"Every receipt" is over-broad (F2).** `l1/controls/c1-do-nothing.json` and
  `c2-do-nothing.json` carry no predicate field or sentence (committed at 78fa9666,
  73 s before the sentence was frozen at 7b63dd5d — they could not carry it), and
  `selftest-c2.txt` carries no full sentence (only the `mismatches 0` fragment is
  asserted against the constant). `selftest-c1.txt` does embed the C1 sentence twice
  (skiprun-predicate got/want). True only if "receipt" means counter-emitted
  receipts.
- Doc nit (F12): `claims.json` A6 renders the banner as `**A - source-derived
  controls.**` (hyphen) while the counter constant is `**A — source-derived
  controls.**` (em dash, `coverage-selfcheck.py:69`); extraction matches the
  constant, so no functional impact.

## 4. QUALITY #83/#84 — pre-freeze dry run

- **Frozen counter itself:** both dryrun receipts name the two frozen tools in
  `tool`, carry the byte-identical predicates, and the C1 receipt carries
  `v1_pin 79a4dca4…` (the r65 pin). No receipt records the *counters'* own sha256 at
  run time; the identity of dry-run bytes to the frozen bytes rests on: instruments
  first-added at 78fa9666 (21:12:31Z), zero drift `78fa9666..HEAD` over
  `tools/round-66/` + `l1/controls/` (git diff empty), and the receipts' embedded
  constants matching the committed constants. Supported, not hash-bound inside the
  receipt (advisory note).
- **Frozen shape:** C1 dryrun ran the real toolchain manifest (a3 `entries 30`,
  a4 dropped `d8-14.7.173/d8`) plus fresh fixture roots; C2 dryrun measured the base
  rev `311079d8…` itself (`rev` field). Yes — data of the frozen shape.
- **Bindings named:** C2's receipt shows every atom binding (claimed/observed/ok),
  stem, hidden list, equivalence diffs (empty) and block sha `1d697af1…`. The C1
  receipt's a2/a3/a4/a5 details show every field their conditions read; **a1's
  condition reads `count_ok` but its detail omits it** (implied by `ok:true`, since
  `closure_state.ok` includes `count_ok`) — nit F7. The C1 dryrun records its
  `scratch`; the C2 dryrun records no `--work`/scratch field, so the `--equiv`
  subprocess scratch location is unrecorded — nit F8. The do-nothing controls name
  every field they read (`count_ok_field_present`, `r65_manifest.entries`,
  `population_dropped`, `r66_arm_would_pass`): satisfied.
- **#84 clause 2 (ls-tree vs disk):** the freeze commit 7b63dd5d contains all nine
  `l1` bytes plus both counters and the plan (git ls-tree verified). Post-freeze
  untracked: `l1/records/r66-order.txt` (the receipt frozen_atom A0 names),
  `l1/census-start.txt`, and the `w1/` seat tree — landing-time items while the wave
  is in flight (F10).

## 5. r65 reviewer residuals A1/A3/A5 (`.ufo/waves/round-65/w1/ReviewerClosure/review.md`)

- **A1 (wrong default probe → guaranteed pin mismatch on `--manifest`): DISPOSED.**
  The r66 counter's default `--probe` is `.ufo/waves/round-64/inputs/probe-electron.jsc`
  (`closure-boundary.py:444`), the file r65's `PROBE_PIN a86f6ea0…`
  (`jsc-closure-matrix.py:110`) pins; the committed dryrun a3 passed with default
  args and `findings: []`, so the default binds to the pin. The r65 bytes were
  correctly left frozen.
- **A3 (uncaught spawn errors → traceback exit 1, no receipt, where exit 2 is
  promised): PARTIALLY DISPOSED.** r66 guards its own fixture probe
  (192–199 catch `OSError`/`TimeoutExpired` → finding) and inherits r65
  `python_probe`'s guard (`jsc-closure-matrix.py:261–265`) for the real probe. But
  `run_verify`/`run_manifest` have no outer guard (try only around `load_v1`, plus
  the toolchain-existence check): an unexpected `OSError` mid-arm (unreadable
  toolchain file inside `sha256_file`) or a dirty `--work` (`write_fixture`
  FileExistsError, 173–174) still yields a traceback, exit 1 ("not verified"
  semantics) and **no receipt** — the r65 A3 wrong-exit-class pattern on a narrower
  surface (F4/F5). No false pass is possible on this path.
- **A5 (symlink-blind census): DISPOSED BY OMISSION, WITH A DOC COST.** r66 re-hosts
  no census — `census` appears only in the docstring (`closure-boundary.py:22`),
  never in code — so nothing in r66 depends on symlink traversal. Costs: the
  docstring claims a census re-host that does not exist (F3), and with neither
  census nor post-probe re-pin, the a3/a4 real-manifest arms detect only
  `__pycache__/*.pyc` writes by the probe; a probe mutation of a pinned toolchain
  file between the pre-probe pin check (120–135) and the post-probe scan (138) would
  be invisible (r65's before/after census had that power). Mitigation: the probe is
  the same guarded `from parse import parse` import r65 verified, and the five-arm
  predicate never claims write-detection. Advisory.

## 6. Findings

| id | severity | finding |
|---|---|---|
| F1 | advisory | Row 68's mechanism clause unimplemented: counters echo `PREDICATE` constants, never read the claim file (`closure-boundary.py:68–76,289`; `coverage-selfcheck.py:60–65,271`; zero `claims.json` reads). Byte-identity at the freeze holds (§3). |
| F2 | advisory | "byte-identical … and every receipt" (`plans/round-66-claims.md:20–22`; docstrings 33–34 / 35–36) is false for `l1/controls/c{1,2}-do-nothing.json` and `selftest-c2.txt` (no sentence; controls predate the freeze by 73 s). True under "receipt = counter-emitted receipt". |
| F3 | advisory | Docstring claims census re-hosting; code has none (`closure-boundary.py:22` vs `closure_state` 112–161). Consequence: real-manifest arms detect only bytecode writes; no post-probe re-pin of the 30 entries + 3 externals. |
| F4 | advisory | Unguarded arms: unexpected `OSError`/`FileExistsError` mid-`run_verify`/`run_manifest` → traceback exit 1, no receipt, where the docstring (57–59) declares exit 2 could-not-evaluate; try only around `load_v1` (224–227) and the toolchain check (260–262). |
| F5 | advisory | Dirty `--work` re-run: `write_fixture` raises FileExistsError (173–174) before `emit`, so the previous `--out` receipt stays on disk — a stale-green receipt can survive beside a failed re-run. |
| F6 | advisory | Scratch leaks on CLI paths: `scratch_dir` mkdtemp `r66-c1-` (210–217) and `r66-c2-` (`main`) are never removed (selftests clean up; verify/manifest/selfcheck do not). |
| F7 | nit | C1 dryrun a1 detail omits the `count_ok` binding its condition reads (`dryrun-c1-verify.json` arms[0]; implied by `ok:true`). |
| F8 | nit | C2 dryrun receipt records no scratch/`--work` field (C1's does), so the `--equiv` subprocess scratch is unrecorded. |
| F9 | nit | `parse_row` takes the FIRST `<n>/<n> knowledge files` in the row (`coverage-selfcheck.py:239`): a fresh fraction placed before a stale one would pass A2. Controlled text today; first-match semantics frozen. |
| F10 | observation | `l1/records/r66-order.txt` (cited by frozen_atom A0) is untracked at HEAD=7b63dd5d (`git status --porcelain`); must land with the round's landing commit. |
| F11 | observation | r65 `--skip-run` still fabricates `closure.ok true` on this host (frozen by design); a5 checks the new counter's constructor in-process (282), not a CLI spawn+parse. |
| F12 | nit | `claims.json` A6 banner rendered with hyphen vs the counter's em dash constant (`coverage-selfcheck.py:69`); descriptive prose only. |

**Blocking findings: none.** Both predicates are fully implemented by the frozen
bytes; kill rules are wired (v1 pin 92–104, arm conditions, exit classes 289–294 and
269–280/429–436); the order chain holds (instruments+controls at 78fa9666 → ancestor
of freeze 7b63dd5d → no post-freeze drift → claims.json unchanged since the freeze).
F1–F6 are counter-design and landing-prose items for a future round or the L1's
landing text — none is a reason to touch the frozen bytes (the M65-4 rule holds:
repair by new freeze, never post-freeze edit).

VERDICT: both frozen counters are fit for the operative run as frozen; no blocking
defect; twelve advisory items above, each with a path:line pointer.
