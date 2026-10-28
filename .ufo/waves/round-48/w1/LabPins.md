# LabPins — r48 w1: verify / attack / falsify the two frozen counters

Seat: LabPins (leaf, no subagents). Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Date of pass: 2026-10-28 UTC. System python: 3.14.8; also 3.11.17/3.12.15/3.13.16 via `~/.local/bin`.
No installs (pacman paused; nothing needed). Scratch: `/fast/scratch/hyaku/kaidoku-r48/LabPins` (removed before yield; receipts copied to `w1/LabPins/`).

## 0. Freeze identity — the assignment's freeze is stale; the claims file rules A4

- Assignment pins `dc73587a` (A1). At run start HEAD was `ac02a79f` (A2); **during the run** A3 (`f3a7afc4`), A4 (`0f06251b`) and two evidence commits (`0d76deed`, `663f30ee`) landed. Current HEAD `663f30ee`.
- The claims file is the rule: each amendment declares "the commit that carries this paragraph". Latest paragraph is **A4 ⇒ declared freeze = `0f06251bf6a3a6964c715f67243d4df12e854258`** (`plans/round-48-claims.md` + `tools/round-48/`).
- A4 closed the two holes its own disclosure cites (opposite-polarity `0=not met`; indented registry row skip). **All findings below are against the A4 bytes** and are *not* the ones A4 fixed.
- A1 receipt snapshots also captured: `w1/LabPins/c1-a1.json`, `c2-a1.json` (both exit 1, matching ctl-c1-0/ctl-c2-0 shape).

## 1. Verification reproductions (A4, exit codes semantic)

| run | cmd | exit | receipt |
|---|---|---|---|
| C1 do-nothing at A4 | `meanings.py --root . --freeze 0f06251b --rev 0f06251b` | 1 | `marker_occurrences 0 != 1` (block absent) — matches ctl-c1-0 shape |
| C2 do-nothing at A4 | `record2.py --root . --freeze 0f06251b --rev 0f06251b` | 1 | floor: `round-47 no seat atom…`, `no Record corrections`, `quoted numbers… 1` — matches ctl-c2-0 |
| C2 v2 at A4 | `record2.py … --profile v2 --no-battery` | 0 | oracle-only profile green — the hole being closed |
| C1 selftest | `meanings.py --selftest` | 0 | `cases=18 failures=0` |
| C2 selftest | `record2.py --selftest` | 0 | parsers only (documented) |
| C1 freeze A1 rev A4 | (dry) | — | `frozen_path_changed` non-empty ⇒ exit 2 by construction (amendments A2–A4 touch `tools/round-48/`) — the freeze pin mechanism itself verified working |

Worktree `tools/round-48/` clean; `git status --porcelain` shows unrelated `.ufo/` edits only (siblings'). One transient `probe-untracked.txt` I created to test `dirty()` was removed in the same step; tree clean (verified).

## 2. Assigned hypothesis — `meanings.MUT_DIGEST` stability

H: "the mutation digest is stable across runs and Python versions."
**Mostly confirmed; three real-world falsifications found.**

| probe | result |
|---|---|
| same file, 4 versions (3.11.17 / 3.12.15 / 3.13.16 / 3.14.8), separate processes | identical `25ce025f…f5c1ea` |
| `-O`, `-OO` | identical (getsource reads `.py`, not bytecode) |
| `__pycache__` present/absent, fresh `.pyc` | identical |
| different cwd with abs `sys.path` | identical (`co_filename` absolute since import) |
| repeat import same process | identical |
| **exec of committed bytes** (`exec(compile(bytes, "a1-meanings","exec"),ns)`) | **OSError "source code not available"** — module unimportable by construction; digest can't be computed from `--rev` bytes at all |
| **stale `.pyc` + edited `.py`** | digest = `a16aab85…` (new text) while *executing* the stale bytecode — **the digest describes disk text, never the code actually running** |
| **linecache staleness** (rewrite same mtime+size) | cached `AAAA` line returned after file reads `BBBB` — `stale: True` |

Mechanics: `inspect.getsource` resolves `co_filename` → `linecache` → the `.py` at that path *at call time*. Digest is computed at module import of the **worktree** file, not at `--rev`. `interpreter_sha256` pins `--rev` bytes. Neither binds what executes. See finding C1-F5.

Digest A1 ≡ A4 (`25ce025f…` both): A2–A4 changed no `_m_*` body, so the pin survives amendments — but `interpreter_sha256` differs every amendment (5 changes so far).

## 3. R48-C1 findings

### C1-F1 [HIGH — kill-class] exit-0 segment: opposite-polarity via unlisted success tokens → green

A4's `NEGATED` whitelist blocks only `\bnot\s+met\b` and `\bno\s+verdict\b`. `SUCCESS` has 10 tokens. `meaning_classes` on the A4 bytes:

```
"0=not verified; 1=violation; 2=usage" -> {0:success,1:not-met,2:unevaluable}
"0=not clean / not green / not passed / not succeeded" -> same
"0=met, unless not verified" -> success
```

End-to-end proof (fixture `$S/f1-min`, receipts `w1/LabPins/f1-min-{genuine,forged}.json`):
- genuine landed fixture → `evaluate` exit **0** (`genuine_green 1, v3_green 0, v2_green 4`)
- identical fixture with every registry verdict map `0=not verified, the target was never checked; 1=not met, a clause is false; 2=could-not-evaluate, the revision or a frozen file is unusable` → **exit 0, `met_target: true`, `meaning_rows_failed: 0`**.

An artifact whose exit-0 maps read "not verified" scores met — the exact R46-CL7 class the claim exists to close. A4 whitelists two phrases; the negation class is *syntactic*, not enumerated. Any `not <token>` / `unverified` / `unmet` / `disproven` wording passes.

### C1-F2 [P0 — clause unmeetable on the real lane] `run_battery` starves its own census re-derivation

`run_battery` scores genuine + forgeries through `_fixture_files(root,rev)` — a limited map: `CLAIMS`(r48 only), `SELF`, `CENSUS`, `CENSUS_TOOL`, `MUST_CITE`, one hardcoded knowledge file, plus **whatever the landed block cites**.

Clause 8's `census_rederive` runs `census2.census_text(read)` where `read = files(p)` on that limited map. On the real lane:

- `plans/round-41..47-claims.md` are **not** in `_fixture_files` unless block 25 cites them.
- `census_text` treats missing files as `present: False` (still derives) — so claims files don't hard-fail, but every tool path outside `ALLOW` **cannot be citable**: `check_refs` rejects refs outside `corpus/lessons/|corpus/knowledge/|plans/|tools/round-48/`.
- 39 of 42 real census paths are `tools/round-4[1-7]/…` → `present` test fails → `derived.paths` ⊆ round-48 tools ≠ committed `paths` (42) → `census_rederived_equal: False` → inner `genuine_exit 1` → `battery genuine_green 0 != 1` → **evaluate exit 1 forever**.

Measured: minimal fixture needed the block to cite all 8 claims files **and** keep its whole census inside `tools/round-48/` to get `genuine_green 1`. On the real lane no citation can satisfy `present` for `tools/round-4[1-7]` paths (they'd be rejected as bad refs first — `unresolved or unvalidated citations: 1` observed on the attempt). **R48-C1 clause 9 (`genuine_green 1`) is unsatisfiable at A4.** L1 cannot land C1 green under these bytes.

### C1-F3 [HIGH] `--rev` grades old artifacts with *worktree* code — and the two can disagree

`evaluate` runs the module from the worktree; `--rev` only chooses graded bytes + pin expectations. Proven divergence on the *same* cell, A1-vs-A4 frozen bytes:

```
"0=met with failing empty; 1=not met…; 2=could-not-evaluate, usage"
  A1 classifier: {"error":"exit 0 segment names no success meaning"}   (NOTMET false-positive on 'failing')
  A4 classifier: {"0":"success","1":"not-met","2":"unevaluable"}
```

Running `--rev <A1>` today executes A4 code and reports A4's verdict on A1's artifact while pinning A1's interpreter hash — self-consistent only because the pin compares rev-bytes vs rev-bytes. The R47-CL1 hole ("execute their own code from the worktree") persists for the *self* instrument; only the oracle was bound. Frozen-path repair requires another amendment.

### C1-F4 [MED] `interpreter_sha256`/`mutations_sha256` pin source text, not executed code

`.gitignore` excludes `__pycache__/`/`*.pyc` ⇒ `dirty()` is blind to stale bytecode under the frozen pathspec (verified: `git check-ignore` hits; an untracked `?? probe` *was* caught). A `.pyc` newer than its `.py` executes stale code while `MUT_DIGEST`/interpreter pin happily describe the current text (receipt §2). Exit-code semantics survive, but the pins do not bind the executing module — bytearray-verified claim, code-executed verdict.

### C1-F5 [LOW] `mutations_sha256` covers only `_m_*` def bodies; outside-mutation text is unhashed

Mutation *names* need only occur as text in block 25 (a comment satisfies "names appear"). Commentary/docstring edits anywhere outside the four function bodies leave both pins intact while changing what `evaluate`/`score` do — covered *only* by `interpreter_sha256` (text hash, so still detected — but the *digest* clause alone would not isolate the change). Minority observation, clause-compliant.

## 4. R48-C2 findings

### C2-F1 [P0 — clause unmeetable at every landing] `axes-correction-forged` is structurally invisible

`_m_axes_correction_forged` appends a **second** `## Record corrections — round 48` heading + forged line to card tail. `corrections_section` reads `split(CORR_HEAD,1)[1].split("\n## ",1)[0]` = the **first** heading's body, terminated by the second heading. The forged line is never parsed:

```
forged_heading_count: 2 ; forged_line_parsed: False
```

End-to-end on the genuine fixture (`f2-genuine.json`): `axes-correction-forged → v3_exit 0`, contributing `v3_green: 3`. **Any card carrying the required `## Record corrections — round 48` heading makes v3 green on this forgery ⇒ `v3_green 0` ⇒ `battery` clause fails ⇒ R48-C2 unmeetable at A4.** The landing requirement *forces* the heading's existence — the claim kills itself by construction.

### C2-F2 [HIGH] `axis_scores` last-row-wins masks a forged Owned-axes score cell

`axis_scores` collects `(coverage|depth)` rows **throughout the Owned-axes body**; later same-axis rows overwrite `out[axis]`. A card whose genuine coverage row reads `| coverage | 4.0 -> 4.0 | 1/1 … |` plus a second `| coverage | 10.0 -> 10.0 | 1/1 … |` yields `score:[10,10] frac:[1,1]` → `cell_bad []` → **green with a forged score cell** (`f2-masked.json`: `axis_score_cells.coverage.score = [10.0, 10.0]` while the first row is 4.0). Clause 5 (R47-CL2) is binding the *last* row, not "the" score cell.

### C2-F3 [HIGH] quote binding forgives wrong values, and `key=N` syntax escapes entirely

(a) `QUOTE = \b(atoms|exempted|corrections|mismatches)\s+(\d+)\b` — `atoms=44` / `atoms: 44` never parse. `f2-eqquote.json`: trailing `atoms=44 and exempted=9` unbound → `quotes_bad []`, green.

(b) Forgiveness is blanket: quote `k V` passes if a receipt states `fixed[k]` **and** `V != fixed[k]` — i.e., any *wrong* value for a corrected key is excused, not just the specific stale one. `quote-off-by-one` scored **v3 green** on my fixture for exactly this reason (receipt `f2-genuine.json`, fixture row `('quote-off-by-one',0,0)`). The clause that exists to bind R47-CL13 lets a wrong quote ride on a correction that names the right value.

### C2-F4 [MED] `axes-score-cell-off` is a conditional no-op — and `gold-tautology` is lane-bound

- `axes-score-cell-off` replaces the *first* `sm.group(2)` match in the row text: on `10.0 -> 10.0` it produces `9.0 -> 10.0` (score[1] untouched → clause green). It only binds when `from != to` textually — on the real card (`9.72 -> 10.0`) it would hit the `9.72`… actually `sm` matches `9.72 -> 10.0`, `sm.group(2)` is `10.0`, `row.replace("10.0","9.0")` hits the *first* literal `10.0` — which is `score[2]`. So it works there, but the mechanism is fragile: it decrements whichever literal appears first, not the score cell's second number.
- `gold-tautology` injects hardcoded lane constants: path `.ufo/waves/round-N/w1/` (a *directory* — `files()` uses `git show`, which fails for trees → path-atom mismatch on any repo without that tree) and rev `` `1e32827b` `` (a lane ancestor; unresolvable on foreign repos → rev-atom mismatch). Fixture: `v2 1/v3 1` with 4 oracle mismatches. On the real card the same constants resolve — i.e., **v2_green depends on lane history, not on the tautology's semantics**; the "ported round-47 semantics" portability claim is false.

### C2-F5 [MED] oracle "executed from the bytes at --rev" — partially false

`oracle()` does `exec(compile(body, ORACLE, "exec"), ns)` in-process; `ns["__file__"]=ORACLE` (relative). The exec'd module then `import gate` → resolves through *record2's own* `sys.path` (the worktree's `tools/round-48/` then `tools/round-46/`) — measured: `oracle gate file: /home/vgpnk/…/tools/round-46/gate.py` (worktree). The docstring's "in a scratch file" never happens (no scratch is created). The oracle's *decision code* is from `--rev`, but its `gate` support code, `sys.modules` and `subprocess` bindings are the worktree's — a worktree `gate.py` difference changes atom derivation under `--rev`. On the lane gate is round-46-frozen, so latent; the mechanism violates R47-CL1's stated fix.

### C2-F6 [LOW] correction classes `rev`/`path` bind no statement

`corrects rev <k>` → only `rev-parse` of the key; `corrects path <k>` → only `files(k)` exists. The correction text after `:` is ignored (unlike `seats`/`window`/`axes`/`quote` which re-derive the statement). `- corrects rev <sha>: renamed to the wrong thing` still passes. Claim's "every line re-derives" is only half-true for these two classes (same hole shape as R47-CL14's inert `axes`, now for `rev`/`path`).

### C2-F7 [LOW] shared-line fragility of `seats-moved`; receipt-path lockdown

- `SEATS_LINE` strips the *whole line* containing a seat claim. If a seat sentence shares its line with a `rev` token a `corrects rev` line targets, the mutation leaves `corrections_bad` — the forgery measures line layout, not the floor clause. My fixture hit exactly this (`seats-moved v2=1` on shared-line card vs `v2=0` expectation on the real card's layout). Landing hazard: the L1 must keep each class's atoms on disjoint lines or the battery's `v2_green 5` becomes layout-dependent.
- `RECEIPT` only matches `.ufo/waves/round-N/l1/scores/*.json` — quotes bound to receipts elsewhere are unbindable (strictness, not a hole, but undocumented in the claim).

## 5. Controls vs findings — how each lands

| clause | mechanism | verdict at A4 |
|---|---|---|
| C1 battery `genuine_green 1` | `_fixture_files` ∩ `ALLOW` ∩ census-presence | **unsatisfiable on real lane** (C1-F2) |
| C1 battery `v3_green 0` | meaning classes | **violated** by `0=not verified` (C1-F1, e2e exit 0 on forged repo) |
| C2 battery `v3_green 0` | corrections_section first-heading | **unsatisfiable** — forged heading invisible (C2-F1) |
| C2 clause 4 quotes | `QUOTE` syntax + correction forgiveness | `key=N` escapes; wrong values forgiven (C2-F3) |
| C2 clause 5 score cell | `axis_scores` | last-row masks (C2-F2) |

## 6. Drafting notes for L1 (landing evidence)

- **C1 cannot land green at A4**: needs A5+ — (a) `NEGATED` → syntactic negation of `SUCCESS` (e.g., reject `not\s+\w+|un\w+` before token match, or require the segment's *first* polarity word), (b) `_fixture_files` must load all census paths + all 8 claims files (or bypass ALLOW for census-only loads).
- **C2 cannot land green at A4**: needs A5+ — `_m_axes_correction_forge`d must place the forged line *inside* the first corrections section (insert after `CORR_HEAD` first occurrence), and `corrections_section` should arguably merge/flag duplicate headings.
- If a C2 re-amendment lands: also fix `axis_scores` to bind the first `| axis |` row (or fail on duplicates), QUOTE to `(\w+)\s*[=: ]\s*(\d+)` or bind `key N` *and* `key=N`, and the quote-forgiveness to exact stale-value matching.
- The seated drafting shortcut for F1 exists but is a trap: citing all claims files + tools in block 25 rescues `genuine_green` **only** where the census ⊆ `tools/round-48/` — impossible on the real census (42 paths). Do not attempt; re-amend.
- `dirty()` correctly catches untracked non-ignored files under the frozen dir (`?? probe` seen); gitignored `.pyc` invisible — residual integrity gap (C1-F4).
- A5 would change `tools/round-48/` again → freeze moves again; every probe here is reproducible in ≤5 commands per fixture dir (see receipts).

## 7. Receipts index (in `w1/LabPins/`)

| file | content |
|---|---|
| `c1-a1.json` `c2-a1.json` | counters at assignment-pinned freeze A1 (do-nothing; exit 1) |
| `f1-genuine.json` `f1-forged.json` | engineered-census fixtures pre-citation workaround |
| `f1-min-genuine.json` `f1-min-forged.json` | **decisive**: genuine exit 0; forged-meaning exit 0 |
| `f1-forged-cited.json` | citation-surfaced variant showing the ALLOW wall |
| `f2-genuine.json` | C2 genuine card + full battery (`v3_green 3` — forgeries green under v3) |
| `f2-masked.json` `f2-eqquote.json` | masked-score-cell and `atoms=44` forged cards, both clause-silent |
| `f1-min-tip.txt` | fixture tip sha |

All commands were run with `TMPDIR=HYAKU_SCRATCH=$S`; every run printed its exact argv inline; sha256-of-stdout taken for the key receipts above. Nothing under `/tmp` was used. No lane file was mutated (one transient probe file created+removed within a single step to test `dirty()`; verified clean).
