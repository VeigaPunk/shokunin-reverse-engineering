# R41C1Mutants — mutation test of the exact-match prototype (round-41 wave 1)

**Verdict: DEFECTS FOUND** — not in the prototype's semantics (no mutant falsified the
exact-match behaviour itself), but in its selftest coverage: of 35 single-logic mutants,
21 are killed by the current 75 selftest cases, 11 survivors are killable and now have
**verified** killing cases (artifacts `cases-to-add.diff`, applied after the prototype diff:
86/86 cases consistent on the pristine prototype, each survivor killed by exactly its new
case), 1 survivor is a structural gap (the parameter-replay clause is untestable by any
simulated case — refactor proposed), and 2 survivors are equivalent (no case can exist).
The round-40 suffix mutant re-run reproduces its round-40 kill exactly.

## Setup (all in scratch; the lane repo was never touched)

- Sandbox clone: `git clone -q --shared /home/vgpnk/Projects/shokunin/kaidoku-shokunin $S/lane`
  (verified `git rev-parse --show-toplevel` = the clone), prototype
  `.ufo/waves/round-40/w2/artifacts/R40W2C1Refreeze/c1-counter-exact-match.diff`
  (sha256 `8fa0a813297eb5ca4f20ed449bcac61c1d3d053ef6793664c22a15e83779c0a8`) applied with
  `git apply`, committed as fixture `afd72359` inside the clone only
  (`-c user.name=fx -c user.email=fx@fx`). Base `49096c7e6f226af0c750c4b003be58883cb6049f`.
- Patched counter sha256 `8e19a016e061d7fd77b4f672e059048a54bf76dc6d1d349ad8eaa30aa0de0e9d`
  — byte-identical to the `patched_file_sha256` recorded by R40W2C1Refreeze.
- Baseline: `python3 $S/lane/tools/round-40/c1-counter.py --selftest --pkg65
  /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents` →
  `{"selftest": "c1-counter", "cases": 75, "green_ok": 7, "red_ok": 68, "failures": []}`, exit 0.
- Battery: `python3 $S/mutgen.py` (driver copied to artifacts) — 35 mutants, each a single
  asserted-unique string replacement on the patched source, each run with `--selftest`
  (4-way parallel, ~102 s). Killed = selftest exit 1 with failures (or crash).
- Per-mutant unified diffs + sha256s: artifacts `mutants/*.diff`, `results.json`.

## Table — mutant | killed? | by which case | case to add

| mutant (clause family) | killed? | by which case(s) | case to add |
|---|---|---|---|
| M01 extract-rel strips ALL leading `_extract` (extract-root derivation) | NO | — | ✅ verified: `nested extract root keeps the components after the first root` |
| M02 extract-rel strips first component unconditionally (extract-root derivation) | NO | — | ✅ verified: `chunk dir without the _extract suffix does not resolve to the oracle row` (also killed by the M04 case) |
| M03 extract-rel keeps `$output/` prefix (extract-root derivation) | NO | — | ✅ verified: `the $output prefix is stripped before the chunk extract root` |
| M04 extract-rel strips a mid-path `_extract` (extract-root derivation) | NO | — | ✅ verified: `a mid-path _extract component is not an extract root` |
| M05 same_rel adds raw `candidate == rel` escape (exact-path matcher) | NO | — | ✅ verified: `receipt path without the chunk extract root does not satisfy the oracle row` |
| M07 oracle_hits_ok `>= 1` instead of `== oracle_files` (oracle hit set equality) | YES | deeper file with the oracle row sha256 does not publish oracle bin/busy | — |
| M08 oracle_hits ignores the path, sha-only (oracle hit set equality) | YES | deeper file with the oracle row sha256 does not publish oracle bin/busy | — |
| M09 oracle_hits counts matching files, not oracle rows (oracle hit set equality) | NO | — | ✅ verified: `duplicate published row still satisfies the oracle row once` |
| M10 oracle_hits_ok drops the `oracle_ok` conjunct (oracle hit set equality) | NO | — | none — **equivalent** (see below) |
| M11 nonregular_published counts symlink kinds only (non-regular unpublished) | NO | — | ✅ verified: `regular file at the device entry path is a materialised entry` |
| M12 nonregular_unpublished_ok := True (non-regular unpublished) | YES | escaping symlink published as a regular file; regular file at the entry path itself is a materialised symlink | — |
| M13 gap rule: required-entry enforcement dropped (gap rule counts) | YES | required gap missing (symlink materialised) — **conflated**: the case also publishes at the entry path, so `nonregular_unpublished_ok` fires; a cleaner case is "unpublished-entry row kept, gap removed, nothing published" with `same_run` | sharpen existing case (optional) |
| M14 structural allowance `n >= limit` instead of `n > limit` (gap rule counts) | YES | structural gap within its frozen allowance | — |
| M15 gap path may match several entries (`len(hits) < 1`) (gap rule counts) | NO | — | ✅ verified: `same path listed with two non-regular kinds resolves to no single entry` |
| M16 gap kind allowance check dropped (gap rule counts) | YES | disallowed gap kind on a symlink entry | — |
| M17 handler_ok substring match (handler) | NO | — | ✅ verified: `chunk handler matching is exact, not a substring test` |
| M18 handler_ok = any chunk at all (handler) | YES | chunk handler is the LE handler | — |
| M19 evidence_id_ok drops the stored==recomputed equality (evidence id) | YES | evidence id stale after an edit | — |
| M20 evidence_id_ok compares only the first 24 chars (evidence id) | NO | — | ✅ verified: `evidence id differing only after char 24 is stale` |
| M21 PROJECTION_KEYS drops `diagnostics` (rerun projection) | YES | fabrication differing only in the diagnostics multiset | — |
| M22 REPLAY_PARAMS drops `--max-depth` (rerun projection) | NO | — | none possible as a `measure()` case — **structural** (see below) |
| M23 projection_diff always equal (rerun projection) | YES | oracle-only fabrication…; fabrication differing only in one published sha256; …diagnostics multiset; default profile refuses the same fabrication | — |
| M25 frozen_drift diffs endpoints only (frozen-path drift) | YES | carrier bytes changed then restored; gap-rule.json touched then restored | — |
| M26 FROZEN_PATHS drops the counter itself (frozen-path drift) | YES | counter edited after freeze | — |
| M27 frozen_drift ignores spec carrier paths (frozen-path drift) | YES | carrier bytes changed after freeze (+3 more) | — |
| M28 frozen_drift logs whole history instead of `freeze..rev` (frozen-path drift) | YES | do-nothing (freeze files only), receipt added at freeze (+many; over-sensitive) | — |
| M29 layout probe drops the AVM marker check (marker/LE-chain probe) | YES | marker-stripped genuine-LE-lengths carrier | — |
| M30 layout probe drops the `bytes_used <= size` check (marker/LE-chain probe) | YES | bytes_used beyond the file | — |
| M31 layout probe drops the v4.0 version check (marker/LE-chain probe) | NO | — | ✅ verified: `superblock version 4.1 is not the AVM v4.0 layout` |
| M32 layout probe drops the single-block identity tiebreak (marker/LE-chain probe) | YES | metadata length plausible both ways (no identity) | — |
| M34 layout probe takes LE plausibility from the BE decode (marker/LE-chain probe) | YES | ambiguous length settled by the single-block identity (+5; also breaks green) | — |
| M35 receipt_fresh allows first-add == freeze (rerun projection family) | YES | receipt added at freeze | — |
| M36 provenance_ok drops the `..` check (run provenance) | YES | provenance path climbs out with .. | — |
| M38 CLAUSES verdict drops `chunks_ok` (verdict conjunction) | YES | failed chunk | — |
| M39 met_target drops the `carriers_unchanged` conjunct (verdict conjunction) | NO | — | none — **equivalent** (see below) |
| **mutant-suffix-matcher.diff re-run** (exact-path matcher reverted to suffix rule, on top of the prototype) | YES | regular usr/bin/busy is not the symlink entry bin/busy; deeper file with the oracle row sha256 does not publish oracle bin/busy; gap on usr/bin/busy does not resolve to the symlink entry bin/busy — identical to the round-40 run (`selftest-suffixmut.txt`) | — |

## The 11 verified killing cases (exact fixture shapes)

All use the prototype's own helpers (`build`, `pub`, `entry`, `oracle_rows`, `same_run`,
`mk_same_runner`, `fsha`, `sb_carrier`, `HANDLER`, `receipt_path`) and slot in directly
before `# ---- freeze integrity`. Ready-to-apply diff: artifacts `cases-to-add.diff`
(sha256 `932bcd4e1deb377f20b477314ffa16d58cf365a7445dd0d577d355f19d8669d0`), verified:
pristine prototype + cases = 86 cases, 0 failures; each survivor mutant + cases = exit 1
with (except M02, killed by two) exactly its new case failing. Full logs: artifacts
`verify-out.json`, driver `verify.py`.

1. **M01** — `build(env_over={'V2': lambda e: pub(e, 'core_extract/usr/bin/tool', fsha(11))},
   oracle_over={'V2': oracle_rows([('core_extract/usr/bin/tool', fsha(11), 5)])})`,
   `runner=same_run(...)`, want 0. Pins: a nested extraction (`a_extract/b_extract/x`)
   keeps the components after the *first* extract root.
2. **M02** — V2 with its single file row renamed to `carrier.out/var/info.txt` (chunk dir
   without the `_extract` suffix), want 1 `want_fail='oracle_hits_ok'`, `same_run`. Pins:
   a receipt path whose first component is not `<name>_extract` resolves to nothing
   (fail closed).
3. **M03** — V2 file row renamed to `$output/firmware.bin_extract/var/info.txt`, want 0,
   `same_run`. Pins: the `$output/` prefix is stripped before the extract root.
4. **M04** — V2: `raw_pub(e, 'var/old_extract/link', fsha(12))` + `entry(e,
   'var/old_extract/link')` + `nonreg_over={'V2': 'var/old_extract/link\tsymlink\n'}`,
   want 1 `want_fail='nonregular_unpublished_ok'`, `same_run`. Pins: a mid-path
   `_extract` component is not an extract root (kills M04 via `gaps_ok` conflation on the
   mutant, cleanly on the prototype).
5. **M05** — V2: `raw_pub(e, 'core_extract/tool.bin', fsha(13))` (no chunk prefix) +
   `oracle_over={'V2': oracle_rows([('core_extract/tool.bin', fsha(13), 5)])}`, want 1
   `want_fail='oracle_hits_ok'`, `same_run`. Pins: raw equality is not a match when the
   extract root cannot be resolved.
6. **M09** — V2 with a duplicate of its single published row appended, want 0, `same_run`.
   Pins: hits count oracle rows, not matching file rows.
7. **M11** — L2: published regular file at `firmware.bin_extract/dev/console` (the device
   entry), want 1 `want_fail='nonregular_unpublished_ok'`, `same_run(recs, 'L2')`. Pins:
   every non-regular kind, not just symlinks, is materialisation-checked.
8. **M15** — V2: gap on `firmware.bin_extract/var/extra` +
   `nonreg_over={'V2': 'var/extra\tsymlink\nvar/extra\tdevice\n'}`, want 1
   `want_fail='gaps_ok'`, `same_run`. Pins: a path listed with two kinds resolves to no
   single entry (fail closed).
9. **M17** — L1: `chunks[0]['handler'] = 'xsquashfs_v4_be'`, want 1
   `want_fail='handler_ok'`, `same_run(recs, 'L1')`. Pins: exact handler membership.
10. **M20** — green L2 receipt with `evidence_id = id[:24] + '0' * 40` (tail-tweaked),
    want 1 `want_fail='evidence_id_ok'`. Pins: full-digest equality.
11. **M31** — `v41 = bytearray(sb_carrier(GZIP_ID, b'V1-v41')); v41[30:32] =
    (1).to_bytes(2, 'big')`, `build(blob_over={'V1': bytes(v41)})`, want 1
    `want_fail='layout_ok'`. Pins: the superblock version check (a v3.0 variant kills the
    same way).

## Two equivalent mutants (no case can exist — documented, not gaps)

- **M10** (`oracle_hits_ok` drops the `oracle_ok` conjunct): `oracle_ok` is independently
  in `CLAUSES`, so `matched` is false whenever the oracle is malformed regardless;
  only the reported clause set changes, never the verdict. Keep the conjunct as
  belt-and-braces or drop it as dead weight — verdict-identical either way.
- **M39** (`met_target` drops `carriers_unchanged`): `CARRIERS` is in `FROZEN_PATHS`, so
  any post-freeze change trips `frozen_drift` → exit 2 before the verdict;
  `carriers_unchanged`/`gap_rule_unchanged` are unreachable-false while `frozen_drift`
  keeps whole-range semantics. Same for the `gap_rule_unchanged` conjunct.

## Structural gap: M22 (parameter replay is invisible to the simulated selftest)

`REPLAY_PARAMS` without `--max-depth` survives every simulated case because the case
runners receive the receipt's raw `parameters` dict, not the argv the real runner builds —
`depth_runner` reads `params.get('max_depth')` directly, so it cannot see the replay. Only
`--selftest-rea` exercises the replay, and only on the one dev image. Proposal for the
round-41 counter: factor the pure function out of `make_real_runner`,

```python
def replay_argv(params):
    argv, replayed = [], {}
    if isinstance(params, dict):
        for flag, key in REPLAY_PARAMS:
            value = params.get(key)
            if isinstance(value, int) and not isinstance(value, bool):
                argv += [flag, str(value)]
                replayed[key] = value
    return argv, replayed
```

and assert it directly in `selftest` (outside the `measure()` case framework):
`replay_argv({'max_depth': 1, 'max_output_bytes': 268435456}) ==
['--max-depth', '1', '--max-output-bytes', '268435456']`;
`replay_argv({'max_depth': True}) == []` (bool excluded); `replay_argv({}) == []`.
That makes every M22-class mutant (dropping any REPLAY_PARAMS entry, or admitting bools)
killable in-sim.

## Suffix-mutant re-run (required item)

`mutant-suffix-matcher.diff` (sha256 `0a1cb6fcca5316ad1a7b7f201a4e81bc05441fdb4e83f60d69175c2a5ae2d8e4`,
verified against the R40W2C1Refreeze record) applied with `patch -p2` on top of the
prototype in `$S/suffixmut` (result sha256
`e2ad30d3d29bf04901bc0976ca04b647177c26d1823cfd9fd333c83097b37377`); `--selftest` →
exit 1, `cases: 75, green_ok: 6, red_ok: 66`, failures = exactly the three round-40
killers (regular `usr/bin/busy` vs symlink `bin/busy`; deeper file with the oracle row
sha256; gap on `usr/bin/busy`) — byte-for-byte the round-40 result. Two nuances the
DETAIL log adds (artifacts `suffix-mutant-detail.txt`):

- the **reverse-direction** case (`regular bin/busy is not the symlink entry
  usr/bin/busy (reverse)`) does **not** kill the suffix mutant — a suffix rule cannot
  confuse `…_extract/bin/busy` with `usr/bin/busy`; it is a green pin for the exact
  matcher, not a suffix killer;
- the materialised-symlink case passes under the mutant only because
  `nonregular_unpublished_ok` still fails it for the forward reason.

## Case-design footgun found while verifying

The prototype's `same_run(recs, k='V2')` defaults to V2; my first M11/M17 drafts used
`same_run(recs)` on L2/L1 fixtures, so the rerun replayed the wrong envelope and the
cases "killed" via a spurious `projection_ok`. Fixed by passing the carrier id
(`same_run(recs, 'L2')`). Recommendation to the L1: the round-41 counter's helper should
require the id explicitly (no default) so a wrong-carrier rerun cannot mask a clause.

## Restoration evidence

- Lane repo `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`: HEAD `49096c7e…` (unchanged),
  `git status --porcelain` shows only the pre-existing untracked `plans/round-41-claims.md`
  and `.ufo/waves/round-41/` — no tracked file touched, no VCS mutation performed.
- Sandbox clone `$S/lane`: prototype commit `afd72359` only; mutants and verification
  copies live in separate scratch dirs (`$S/mutants/*`, `$S/verify/*`), never in the clone.
- Scratch `$S` removed after artifact copy-down; everything cited lives under
  `.ufo/waves/round-41/w1/artifacts/R41C1Mutants/`.

## Tooling

No installs or upgrades (operator authorization unused): python3, node, git, patch, and
the pre-existing npx rea-agents@6.5.0 cache were sufficient.

## Limits

- Fixture-level: all mutants were scored by the embedded selftest on fixture carriers;
  no REA/unblob run on any reserved carrier (none touched; none needed).
- The 11 cases are verified against the prototype bytes `8e19a016…`; if the L1
  restructures the round-41 counter, the recipes (not the diff context) are what carries.
- M13's existing killer is conflated (see table); the sharpened variant is optional.
- [INFERENCE] The two equivalent mutants are equivalent under the current
  `frozen_drift`/`CLAUSES` semantics; a round-41 counter that narrows either would need
  the cases re-derived.
