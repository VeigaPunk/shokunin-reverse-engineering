# r52-w1 · RevCounterEscape (reviewer) — attack on the v1 C1 counter and the v2 design

Full register, citations and the v2 MUST list: `.ufo/waves/round-52/w1/RevCounterEscape/escapes.md`.
Probe receipts and source digests: `.ufo/waves/round-52/w1/RevCounterEscape/receipts/`.
Read-only. Base `c525de54`, claims draft `ab0eafed`. No REA run, no `--data-run`, no install, no git mutation.

## Verdict

The v2 design as drafted cannot refuse a forged green. v1 is closed against a working-tree rule or receipt
substitution (content reads are `git show` at FREEZE/REV) and against a planted receipts directory (none exists).
v1 is open on the execution environment and the freeze anchor, which every independent-rerun and evidence-id clause trusts.

## Findings (highest first)

1. **Inherited environment forges the rerun (E2, probed).** `NODE_OPTIONS=--require hook.js` runs inside the REA child and
   the evidence-id node (2037, 686); `LD_PRELOAD` runs inside `/usr/bin/unsquashfs` (2117). Result: `projection_ok`,
   `evidence_id_ok` and `oracle_rederived_ok` can be satisfied with no truthful extraction. Fix: M-1 (minimal env).
2. **Caller-chosen toolchain and REA package (E3, E4).** `--unblob` is accepted on `--version` alone (1977-1982).
   `--pkg65` hashes only `package.json` and the lock (643-645), so the bin and lib code that both the rerun and the
   evidence-id recompute execute is unchecked. Fix: M-3, M-4 (whole-tree manifest).
3. **`git` from PATH and `refs/replace` (E1, E6, probed).** `git` is a bare name (461). A replace ref makes `git show`
   and `cat-file` return forged bytes while `rev-parse` (the drift check, 1713-1722) sees the honest blob. Fix: M-2, M-6
   (`--no-replace-objects`, refuse `refs/replace`/grafts/shallow).
4. **Freeze unanchored (E5).** `--freeze` is any commit; no expected SHA, no `is_ancestor(freeze, rev)`. A later freeze
   hides a rule edit made before it; a forged "freeze" commit with a permissive rule passes. Fix: M-5.
5. **v2 flags reopen the controls (E7).** The predicate (claims 89-90) passes `--receipts`; the draft adds `--gap-rule`,
   `--provenance-base`, `--receipt-fresh-base`. Any filesystem read makes CTL-OLD/NEW and M1-M4 forgeable, and the
   base flags change provenance and freshness. Fix: M-7 (module constants, `git show` only).

Question answers (detail in the register):
- Caller inputs: rule override is blocked in v1 (2174, 2214); receipt digest is not bound to a blob id (2310); the stale
  freeze pin is possible (E5).
- Projection rerun: a planted working-tree receipt cannot satisfy `projection_ok` (committed read, 2302). It can be
  satisfied with no genuine REA run through E2-E4.
- Prior pins: a stale pin slips through the enumeration gap (`prior_pins` 1608-1646 names two tables and three candidates;
  it misses rounds 36-40/44 tables and every receipt subject digest). Round-44 `v1le b45925fa…` and round-40 L1 `2521ded0…`
  are examples. The four round-50 pins are not in any enumerated table, but the waiver must be a separate, id-bound,
  exact key (M-10), not membership in `prior_pins`.
- Bindings: `entry_present` (2457-2458) passes an empty file; `sourced`, `province_core_row`, `frontier_note` and
  `coverage_map_row` accept single placeholder lines (E11, M-11).

## Confidence

High on E1-E8 and E11 (code citations checked at base). E2 and E6 probed on this host. E9 (retry) is medium, since the
v2 retry text is a draft. Not verified: REA's own handling of `REA_UNBLOB_COMMAND` and bin semantics; the PATH `git` shim
and the `--pkg65` replacement were not run ([INFERENCE]).

## Tooling

None installed. Probes used the host's `git`, `node` v24.21.0, `/usr/bin/unsquashfs` 4.7.5 and `gcc`, all already present.

## Report

Seat dir: `.ufo/waves/round-52/w1/RevCounterEscape/` (escapes.md, receipts/, status.json).
