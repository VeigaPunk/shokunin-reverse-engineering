# SimplC1 — YAGNI pass + attack on `tools/round-48/meanings.py` (R48-C1)

Seat: SimplC1. Scope: clause/function/flag keep-or-cut on the frozen C1 counter,
plus falsification of the frozen bytes.

## Operative freeze (corrected)

Prompt cited `dc73587a…` (A1). Four amendments exist on `main`; each "declared
freeze is the commit that carries this paragraph":

| commit | amendment | fix |
|---|---|---|
| `7fe11332` | initial freeze | — |
| `dc73587a` | A1 | record2 score-cell (C2 side only) |
| `ac02a79f` | A2 | drop success-guard false-red |
| `f3a7afc4` | A3 | census clause compared dict to list — **the same defect my first read flagged; already fixed** |
| `0f06251b` | A4 | `0=not met` polarity hole (C1Gold); indented registry row skipped (CritAxis/CritSeparability) |

`git log --format=%H -1 -- plans/round-48-claims.md` → `0f06251bf6a3a6964c715f67243d4df12e854258`.
All analysis below is against the **A4 bytes** (current file, 735 lines). `git status
--porcelain` on frozen paths: clean; `tools/round-48/__pycache__/` is gitignored
(`check-ignore` hit on `.gitignore:1`), so it does not trip `gate.dirty()`.

## Receipts (commands, exits, sha256)

- `python3 -I -B tools/round-48/meanings.py --root . --freeze 0f06251b… --rev 0f06251b… --json-out .ufo/waves/round-48/w1/SimplC1/counter-v3-at-freeze.json` → **exit 1**; `marker_occurrences 0`, `marker_block_count 0`, `rule_blocks 24`, `frozen_path_changed []`, battery `skipped` (red artefact short-circuit). sha256 `9c5048d2…79536`. UTC 2026-10-28T18:57:52Z. Matches the do-nothing control shape.
- Same with `--profile v2` → **exit 1** (`marker_block_count 0` only — v2's weaker check set). sha256 `8ee187a8…86ed`.
- `python3 -I -B tools/round-48/meanings.py --selftest` → **exit 0**, `MEANINGS_SELFTEST: cases=18 failures=0` (incl. new `red-opposite-polarity`, `red-hidden-row`).

## Findings — live defects at the A4 freeze

### F1 (HIGH, A3-class false-red still live): the battery's own fixture breaks `genuine_green`

`run_battery` (l. 497+) scores the genuine artefact via `_fixture_files` (l. 474),
which loads only `plans/round-48-claims.md` of the eight claims files. `census2.census_text`
reads `plans/round-4[1-8]-claims.md`; under the fixture it derives
`paths = ["tools/round-48/meanings.py"]` (1 path) vs the committed 42.
Reproduced exactly:

```
score(good_skill, battery_fixture, "v3", freeze) → code 1
failing: ["committed census2.json does not equal a fresh derivation"]
census_rederived_equal: false
=> run_battery genuine_green = 0  → clause 9 "genuine_green 0 != 1" fails
```

Consequence: at a fully-correct landing, `evaluate()` reaches the battery (the
main-path score IS green — verified below), the battery scores its own genuine
case red, and the counter exits 1 forever. **R48-C1 is unmeetable at this freeze** —
identical defect class to A3 (re-derivation fed an incomplete read surface), in the
code path A3 did not touch. Fix direction: `_fixture_files` must load all
`plans/round-4[1-8]-claims.md` files at rev (or `census_rederive` must read through
`gate.show` in the battery path). A5 candidate.

### F2 (MEDIUM): `NOTMET`/`UNEVAL` tokens are unanchored substrings — meaning binding satisfiable by non-meanings

`NOTMET` (l. 59) has no `\b` on `red`/`fail`/`refus`; `UNEVAL` (l. 60) anchors only
`usage`/`error`. Measured at the A4 bytes via `meaning_classes()`:

- `1=measured` → class `not-met` (substring `red` in "measured")
- `1=scored`, `1=prepared` → `not-met`; `1=failureware` → `not-met` (substring `fail`)
- End-to-end: registry with verdict `0=met; 1=measured; 2=error` → `score()` exit **0**,
  `meaning_rows_failed 0`. The map binds a substring, not a meaning — same weakness
  class the clause exists to close (weaker than A4's `0=not met` hole: needs a
  deliberately crafted landing, not a plausible genuine row).
- A4's `NEGATED` guard was applied to exit-0 only; exit-1/2 have no polarity check,
  and `NOTMET` still can't distinguish `1=met` from `1=not met` (relies on the
  "not met" phrase). `1=unmet` would *not* classify — no false-red, but brittle vocabulary.

### F3 (LOW, spec-vs-code delta): `SELF` citation exempt from clause 7's "each with a line selector"

`check_refs` l. 268: `if name == SELF: continue` — after `cited.add`, so a bare
`` `tools/round-48/meanings.py` `` (no selector) counts toward the ≥5 resolving
citations. Verified: artefact citing SELF without a selector → exit 0, `refs 6`,
`unresolved []`. Clause 7's literal text ("each with a line selector") is looser in
code. Defensible (the pin binds SELF byte-exact), but undocumented in the claims file.

### F4 (LOW): committed `census2.json` is stale in an unbound field

`derived == doc` is False; the only differing field is `per_claims_file` — committed
census was generated before `tools/round-47/exact.py` appeared in the r48 claims file.
`paths`/`named_but_absent` are fresh. Clause 8 binds only `paths`, so this is
consistent-but-stale: the counter's wording ("equals a fresh derivation") is narrower
than the document's actual content. Regenerating `census2.json` at landing would be
cosmetic.

### F5 (latent, unreachable on green artefacts): no-op mutation counts as a forgery

`run_battery` l. 518: a mutation returning unchanged text increments
`forgeries_total` and `v2_green`. Unreachable today (green implies distinct
segments + correct arms ⇒ all four mutations transform), but the accounting is wrong
if a fifth mutation is ever added.

## Keep/cut table — every clause, function, flag

| Element | Lines | Claim clause it serves | Verdict |
|---|---|---|---|
| `MUTATIONS` + 4 mutation fns | 88–126 | clause 5 digest; clause 9 battery (the forgeries themselves) | **keep** — each named in the claim |
| `_mut_digest` / `MUT_DIGEST` | 129–141 | clause 5 (name+body sha256) | keep |
| `craft_section`, `blocks_of` | 146–155 | clause 1 marker/block scoping; `MALFORMED` split feeds exit-2 semantics (selftest `red-malformed-heading-is-exit-2`) | keep |
| `table`, `_rows`, `_cells`, `_table_span`, `rewrite_rows` | 71–85, 158–179 | clause 2 header/row checks; `rewrite_rows` supports `permuted-arm` mutation | keep |
| `registry_rows`, `_rewrite_registry`, `ROW_START` | 182–211 | clause 8 registry binding; A4's widened row match | keep |
| `_segments`, `meaning_classes`, `SEG`, `SUCCESS`/`NOTMET`/`UNEVAL`/`BANANA`/`NEGATED` | 214–247, 57–63 | clause 8 meaning classes + distinctness + no-placeholder; A4 polarity | keep — **F2 token-anchoring weakness noted** |
| `check_refs`, `line_count`, `HARD_REF`, `ALLOW`, `MUST_CITE` | 53, 250–274 | clause 7 citation count, selectors, resolution | keep — **F3 SELF-exemption delta noted** |
| `MUST_KNOW` check (`any(c.startswith(MUST_KNOW) and HARD_REF.search(block) …)`, l. 412) | 50, 412–413 | clause 7's "at least one corpus/knowledge/ entry" | **keep check; cut the conjunct** — `HARD_REF.search(block)` is always true when `cited` is non-empty (verified: block trivially contains refs). The selector requirement it gestures at is already enforced for *all* cited refs by `check_refs` l. 264. One-line change: `any(c.startswith(MUST_KNOW) for c in cited)`. Selftest gap: no `MUST_KNOW`-absent case exists (verified red via probe: exit 1, `does not cite a corpus/knowledge/ entry`). |
| `census_doc`, `census_rederive` | 277–298 | clause 8's "committed census2.json equals a fresh derivation … at --rev" | **keep** — the re-derivation is what makes the census re-checkable rather than a hand-kept list; the exec of *committed* `census2.py` bytes is the honest-derivation pattern. Cost is trivial (regex over 8 claims files). F1 is in its *fixture feed*, not in this function. |
| `EXPECTED_ARM`, `ROUTED`, `VOCAB`, `ID` | 44–47, 56 | clauses 3–4 (per-id arm equality; vocab) | keep — the R47-CL10 repair |
| `score()` profile split (`hard = profile == "v3"`) | 303–462 | clause 9's `v2_green 4` evidence + the v3 strict set | **v2 profile: keep — load-bearing.** Clause 9 mandates `v2_green 4`: the ported round-46/47 semantics exist only as the falsification witness proving the holes were real (membership tests accepting all four forgeries). It is a measurement instrument, not a second acceptance path. Removing it would remove the claim's own evidence. |
| `run_battery`, `_fixture_files` | 468–528 | clause 9 battery | keep — **F1: `_fixture_files` under-loads claims files (fix required for claim meetability)**; `scratch_root` param is **dead** (never passed, never used) — cut |
| `evaluate()` battery gating (`if with_battery and code == 0`) | 542–548 | cost ordering: artefact-red ⇒ battery skipped, same final verdict | keep — correct and documented in receipt |
| `--no-battery` flag | 567 | none — dev iteration aid | **keep with caveat**: a green exit under `--no-battery` is not claim evidence (receipt lacks the `battery` block). Harmless; document or cut. |
| mutation `(skill, spec)` param and `overrides` return | 89–120, 517 | none — `spec` is always `None`, `overrides` always `{}` in all four mutations (verified: `overrides_all_empty_dict: true`); `and not overrides` at l. 518 is always-true | **cut**: signature `fn(skill) -> text`, drop l. 518's `not overrides`, drop `out["fixtures"]`-no-op `v2_green += 1` accounting (folds F5). Note: changing mutation bodies changes `MUT_DIGEST` → the block pin must be re-pinned at landing anyway. |
| `_fixture_files` hardcoded knowledge path (l. 471) | 470–472 | none — the marked-block ref loop already loads every cited path | **cut candidate** (cosmetic: an unconditional load that duplicates the ref-driven loop) |
| `selftest()` + fixtures | 633–718 | instrument quality; now 18 cases | keep — **coverage gaps**: no `MUST_KNOW`-absent / `MUST_CITE`-absent / `refs<5` cases; no case exercising the battery fixture's census (the F1 class); `red-census-stale` mutates the committed doc, not the read surface |
| `exit` cells bound check | ~347–349 | clause 2 | keep |
| `arm_by_id`, `routed_counts` receipt fields | ~358–377 | clause 3 evidence | keep |

## Landing implications for L1

1. **F1 must be fixed (A5) or the claim cannot go green** — the landing's own
   `run_battery` will score `genuine_green 0`. Receipts: `probe.py`/`probe.out`
   (class probes, forgery exits over real bytes) and `genuine-under-fixture.out`
   (the landing-fixture simulation) in `.ufo/waves/round-48/w1/SimplC1/`.
2. Registry section at landing must contain **exactly the 42 `census2.json` paths**
   (`paths` list verified fresh-equal post-A3); current section has ~40 rows from
   prior rounds — rows for `meanings.py`/`record2.py` to add, and any row outside
   the census fails `registry_extra`.
3. Verdict maps for the two new rows must name success/not-met/unevaluable classes
   with distinct texts and **avoid words containing `red`/`fail`/`refus` in the
   exit-0 segment** and non-token words in exit-1/2 segments (F2 substring class).
   `0=not met`-style phrasing is now correctly red (A4, verified).
4. Clause 7: ≥5 `corpus/lessons|knowledge|plans|tools/round-48/` citations with
   line selectors, incl. `corpus/lessons/round-47.md` (≥120 lines at freeze — ranges
   up to ~120 resolve) and a `corpus/knowledge/` entry. `SELF` needs no selector (F3).
5. `mutations_sha256` = `25ce025f8b2be63a5122583191cbf7588db7dc2894c869fac2ab075a84f5c1ea`
   at A4 bytes; `interpreter_sha256` = sha256 of the landing-revision file bytes
   (`00f768c52a78f18a359c193cff08728a8dd8989e45121e7d496012d93d2649d0` at freeze).
   `good_block()`/`skill_text()`/`good_registry()` in the selftest (l. 595–631)
   produce a passing artefact — verified `score() → 0` over real freeze bytes with
   `census_rederived_equal: true`, `registry_rows 42`, `refs 6`, `unresolved []`.

## Verification status

- Counter executed at freeze (v3 exit 1, v2 exit 1), selftest 18/18 — receipts in
  `.ufo/waves/round-48/w1/SimplC1/counter-{v3,v2}-at-freeze.json`.
- F1/F2/F3/F4 each demonstrated by execution against `git show` bytes at
  `0f06251b`, not by reading alone.
- Not run: `record2.py` (outside my seat's target); no fixture repos needed (all
  probes read committed bytes only).

Installs: none. Peer note: C2Floor's stray "DISALLOWED" was its own completion
artifact; no coordination conflict.
