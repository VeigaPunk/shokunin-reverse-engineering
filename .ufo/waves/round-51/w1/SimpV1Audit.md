# SimpV1Audit — v1 counter dead-weight audit (round 51, wave 1)

Seat: SimpV1Audit · lane: `kaidoku-shokunin` · base rev audited:
`f04b51ddb8d5fedb234a5e40a2c38b016f07a4ab`.

## Verdict

**The v1 counter's core disposition machinery is exactly what the round-51 law
needs — keep it; the port's work is in the constants and the flags, not the
algorithms.** Offline measurement against the *committed* round-50 receipts and
oracle tables, with the v1 code unmodified: the round-50 frozen rule → 2 of 4
(the committed miss, reproduced); a law-shaped rule → 4 of 4; a 12-of-13
whitelist → still red (the M50 partial-widening trap holds). `disposition_check`
needs **no change** to express the law.

**Audit yield:** 7 DROP, 9 RE-POINT, 5 KEEP-with-question, plus **4 defects the
port must not inherit** — see the three most important below.

## The three most important findings

1. **The draft v2's `--controls` mode scores the M1 mutant GREEN.**
   `law_shape_ok` exists only in the `measure()` bindings path
   (`tools/round-51/c1-counter.py:2662-2678`); `controls_mode` (`:2703-2795`)
   never computes it, so it evaluates only `gaps_ok ∧
   nonregular_unpublished_ok`. Measured: the all-thirteen whitelist → exit 0,
   4/4 — but the claim requires M1 **red**, "red by the frozen rule-shape
   clause". Since M1 is extensionally identical to the law over the measured
   data, the shape clause is the *only* thing that can separate them, and the
   kill rule reads "any mutant green that should be red → stop before the data
   run". **Fix before the freeze.**

2. **The claim's stated predicate command omits `--pkg65`, but the counter
   requires it.** `plans/round-51-claims.md:87-88` gives
   `… --root --rev --freeze --receipts … --json-out …`; the draft v2's `main()`
   (`:2871`) still exits 2 with `usage: --root --rev --freeze --pkg65 required`.
   Also, `--receipts` is honoured **only** in `--controls` mode (`:2861`); the
   main path resolves receipts from the per-carrier `receipt` key or `AFTERDIR`
   (`:2353`). The claim text and the instrument must be reconciled before the
   freeze (the claim requires them to be the same sentence).

3. **Two "never existed" candidate paths, and a missing frozen family.**
   `tools/round-4{9,50}/{prior-pins,rea-pkg}.json` have **never existed in
   git** (`git log --all --diff-filter=A` → empty); at the round-50 freeze only
   `tools/round-42/rea-pkg.json` existed, so the round-50 counter silently
   resolved to the round-42 pin. Separately, `tools/round-51/` currently holds
   only `c1-counter.py` and `c1-run.sh` — **no `carriers.json`, no
   `gap-rule.json`, no `rea-pkg.json`, no `prior-pins.json`** — yet both the
   claim and the draft read them. Measured: `controls_mode` exits 2
   ("carriers table absent") until a round-51 carriers table exists.

Also worth the L1's attention: the round-50 receipts fail `receipt_fresh` by
construction (added at `646d29c9`, an ancestor of the base rev — measured),
and all four fail `run_provenance_ok` under a round-51 prefix. The claim's
rule-scoped control design (F2) is the correct answer to both; the trap is a
`--controls` mode that runs the *full* predicate, which would report 0/4 for
both rules and fire the kill rule on a measurement artefact.

## Deliverable

Full audit — every item with file:line, evidence and a keep/drop
recommendation — at
`.ufo/waves/round-51/w1/SimpV1Audit/audit.md` (284 lines).

Structure: **A** DROP (7) · **B** RE-POINT (9) · **C** KEEP (6) ·
**D** DO NOT INHERIT (4) · **E** KEEP-with-question (5) ·
**F** the v1 selftest cases the port should carry over (freeze-drift,
exact-vs-legacy, structural gaps, projection refusals, provenance refusals) ·
**G** evidence index · **H** cleanup.

## Contract compliance

* Wrote only inside `.ufo/waves/round-51/w1/SimpV1Audit/` (the audit) and this
  report file. **No lane `tools/`, `plans/`, `corpus/`, `SKILL.md`,
  `PROVINCE.md`, `LOG.md`, `SCORECARD.md` or `SHONEN.md` was touched.** No
  commit, push, stage, stash or mutating git/jj command anywhere.
* **No REA run**: no `npx rea-agents`, no `rea`, no invocation of the package
  at `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`. The
  v1 `--selftest` was **not run** (it executes the frozen `xpin` tool against
  that package); `--selftest-rea` was **not run** (it needs REA). Both are
  recorded as "not run" in the audit's honest-limits paragraph.
* Downloads: none. Fixture repos: one `git clone --shared` into scratch, with
  `git rev-parse --show-toplevel` asserted against the fixture dir before the
  first commit; `user.name`/`user.email` set in that clone only.
* Scratch `S=/fast/scratch/hyaku/kaidoku-r51/w1-SimpV1Audit`, `TMPDIR=$S`;
  `/home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` consulted
  before the passes. **Scratch removed** after the receipts were recorded.
* Lane tree unchanged by this seat: `git status --porcelain` shows only the
  pre-existing `?? .ufo/waves/round-51/` and the siblings' untracked drafts.
* Tooling: none installed, none needed (stdlib Python + `git` only) — no
  pacman/`uv`/`npx`/`cargo` transaction was run, so there is no tool/version/
  channel/reason entry to record.
