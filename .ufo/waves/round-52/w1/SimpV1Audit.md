# SimpV1Audit (r52-w1) — v1 dead-weight audit for the v2 port

Verdict: settled. The full list with file:line and KEEP/DROP/Q calls is in
`.ufo/waves/round-52/w1/SimpV1Audit/audit.md`.

## Most important findings

1. **Triage v5 cannot fail on two claimed bindings.** `evaluator_missing` is structurally zero
   (`sqfs-triage-v5.py:1301` wraps a `evaluate()` that never raises), and freeze drift is
   reported but not gated (`:1256-1281`). The executability audit and census clause do not
   exist in v5. All three are ADD work for v6, not ports.
2. **The round-51 v6 draft does not parse** (`.ufo/waves/round-51/w1/ExecTriV6/sqfs-triage-v6.py:288`
   has `CUT 1033.=1033` inside Python source). Naive ddwrt routing measured offline: moving ddwrt
   into `NO_READER_FAMILIES` flips 8 corpus labels, including 7 clean `*_ddefault` envelopes
   that the claim says keep `clean`. The `legacy-body-unreadable` route flips exactly one
   envelope (`dmg_Z3_v3ddwrt_inode_table`).
3. **Dead and round-50-only code to drop:** the v4 red-before witness and its rows
   (`V4_ROWS`, `VOCAB_V4`, `do-nothing-v4`), the REA dev-arm controls (`spec_c1b`, `spec_c3`,
   `spec_c4`, `spec_pos*`, `spec_c2x`, capture/mint/import helpers), `--selftest-rea`/`--dev-image`,
   `--pos-from-lane`, `DEFAULT_SKILL`, `PROV_SEGMENT`, `_missing_ids`, and two dead candidates in each
   of `PRIOR_PIN_CANDIDATES` and `REA_PKG_CANDIDATES` (absent at `c525de54`). The controls also
   use `npx` (`c1-controls.py:432`, against the counter's own S1 rule) and `REA_ATTEMPTS=5`
   (`:73`, vs the counter's `MAX_REA_ATTEMPTS=3`).

## Tensions for the L1 to rule on

- Counter exit on `provider_timeout` exhaustion is exit 2 (`RerunEnvError`); the claim calls an
  exhausted projection "missed". The claim is silent on the timeout case.
- The ENOENT retry, `law_shape_ok`, `census_rederived_ok`, `depth_gap_recorded` and
  `re_scored_pins` are absent from v1. They are ADD work.

## Evidence (receipts in `.ufo/waves/round-52/w1/SimpV1Audit/receipts/`)

- Triage v5 on the frozen 126-envelope corpus at `c525de54`: exit 0, `pair_mismatches 0`,
  `evaluator_missing 0`, 17 rules. The corpus has no `no-reader-failure` row at all, so that
  branch is covered only by a selftest fixture.
- Counter offline selftest: exit 0, 169 cases, green_ok 17, red_ok 152 (simulated REA runner;
  node xpin evidence-id helper only; no `extract-firmware` run).
- Not run: controls selftest, any REA run, any carrier read, `--selftest-rea`, any sasquatch or
  unsquashfs run against carriers.

## Tools and scratch

- Installed: none. `pyflakes` was already present at `/home/vgpnk/.local/bin/pyflakes` and was not
  run (AST scan used instead). No PATH directory was touched.
- Lane tree: no writes. Read-only git only.
- Scratch `/fast/scratch/hyaku/kaidoku-r52/w1-SimpV1Audit` removed after receipts were copied.

Report: `.ufo/waves/round-52/w1/SimpV1Audit.md`
Audit: `.ufo/waves/round-52/w1/SimpV1Audit/audit.md`
