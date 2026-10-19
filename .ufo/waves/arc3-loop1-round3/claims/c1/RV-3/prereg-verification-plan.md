# RV-3 pre-registration — grading method + independent verification plan (arc3-loop1-round3)

Seat RV-3, chain c1, role reviewer. Task: grade the drafted entry against
`corpus/QUALITY.md` + r1 precedent; list required fixes.

## Authorities

- `corpus/QUALITY.md` as written: 15 admission rows (`:9-25`), 6 weak-material
  signals (`:29-36`). (The round-2 record's "16 criteria" is stale; RV-3 r1 D8.)
- r1 precedent entry `corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md`
  (10,225 B / 33 lines / sha256 `dd986f56…` at HEAD `c07af80f`) + its grade
  `.ufo/waves/arc3-loop1-round1/claims/c1/RV-3/quality-grade.md`.
- Frozen C1 claim `claims-frozen.md:16-36`.

## Method (pre-registered before the draft lands)

1. Baseline before-state: recipe A at HEAD `c07af80f` —
   `{"knowledge_files": 82, "mapped": 82, "missing": [], "dangling": [],
   "citation_resolved_rules": 14, "rule_blocks": 14, 10.0/10.0}` (measured
   13:06Z; script `/var/tmp/rv3-r3/cmmdA.py`). After-state must read 83/83,
   rules 14/14, prior-82 byte-identical.
2. Apply the drafted patch to a pristine HEAD tree (`/dev/shm/rv3r3/head`,
   extracted via `git archive`); measure with the worktree recipe
   (`/var/tmp/rv3-r3/cmdA-wt.py`, self-tested equal to recipe A on the
   unpatched tree: identical JSON, 13:06Z).
3. Independent evidence re-derivation (not a reading of the draft's claims):
   - re-hash every artifact the entry pins; keccak-recompute the planted
     selector sets from the compiled ABIs (`js-sha3` from the wave solc
     prefix, same tool as r1); set-equality vs the probe envelopes;
   - re-run the entry's `recheck:` command verbatim (disk-backed TMPDIR;
     `/tmp` is EDQUOT on this host) and compare its output to the recorded
     expectations;
   - verify the solc prefix receipt: `soljson.js` sha256 `221d7a66…abad4c`,
     package.json `b3a90035…3491`, `solcjs --version` = 0.8.37+commit.f401782d
     (all re-measured 13:06Z — matches the r1 receipt).
4. Criterion table against QUALITY.md rows 1-15 + signals 1-6; hard gates:
   patch applies clean; stem == map token; line-neutral README edit (190→190,
   prior tokens byte-identical); command A after; K/K with zero extras on the
   optimizer carrier and the non-ERC-20 carrier; `dispatch:"abi"` retained;
   entry self-identity fresh after every revision (rule #14).
5. Red-flag scan: `grep -c`; bare `/tmp` in recheck; bare line ranges into
   in-place-rewritten files (rule #11 form); universal content-addressed
   claims; held/works verbs; behavior-from-strings; floating targets.

## Status

- Baseline + solc receipt + r1 recheck (`ev_45849c8b…` family: 5/5,
  `dispatch:"abi"`, decoded `c1081a56…`) re-measured at 13:06-13:08Z.
- Draft not yet landed at 13:08Z (c1 dirs: EX-04, EX-05, EX-06, EX-10, EX-14,
  PL-1, RV-4, VZ-1). Polling 60 s cadence (max 25 checks), log
  `/var/tmp/rv3-r3/poll.log`.
