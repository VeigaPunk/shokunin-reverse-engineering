# ExecIndependentC1 — independent re-derivation of the R28-C1 primary-rule triple

## Scope
Recompute, with a freshly written script and a fresh keccak implementation, the
round-25 primary naming rule `openchain_sole_unfiltered_args_consistent` over the
187 held-out rows. Acceptance target: named 137, right 137, wrong 0, no_name 50.

## Method
Script `independent_c1.py` (sha256 below). For each heldout row it:
1. reads REA's `inferred_arguments` for the selector from
   `envelopes/<carrier>.json -> normalized_result.functions`,
2. reads openchain candidates from `db/openchain-<sel>.json ->
   result.function["0x<sel>"]`,
3. keeps a candidate only when `filtered` is False AND
   `keccak256(text)[:4] == selector` AND the candidate's top-level parameter list
   equals REA's inferred args,
4. names the selector only when exactly one candidate survives, then compares that
   text with `abi_signature` in heldout.tsv.

Keccak-256 is computed with pycryptodome `Crypto.Hash.keccak` (digest_bits=256),
installed into a `uv venv` for this seat — not the lane resolver. Parameter-list
extraction (`params_of`) and the filtered/keccak/args predicates were
re-implemented in this script, not imported.

## Result (observation)
Counts over all 187 rows:

| metric | value |
|---|---|
| named | 137 |
| right | 137 |
| wrong | 0 |
| no_name | 50 |

Agreement with the claimed triple 137/137/0/50: EXACT. Differing rows: none
(`differs` list empty). This matches committed `tally.json` rule
`openchain_sole_unfiltered_args_consistent` (named 137, right 137, wrong 0,
no_name 50).

## Cross-checks (observation)
- All 147 distinct openchain candidate texts: my pycryptodome keccak agrees with
  the lane resolver's pure-Python sponge on every text (0 disagreements), and my
  `params_of` agrees with the resolver's on every text (0 disagreements). So the
  match is not a shared-bug artifact.
- 186/187 rows are recovered by REA. The one unrecovered row is carrier h09:
  `envelopes/h09.json` is an REA error object (`code: invalid_request`, "Hex
  carrier requires complete hexadecimal byte pairs"), with no
  `normalized_result.functions`. Its heldout row is selector `395c1d44`
  (truth `useIt(uint256)`); its openchain response is `null` (no candidates), so
  it is `no_name` under my script either way.
- `heldout.tsv` sha256 = `423654f9d71feb417725a1e5a290b1e028ee53ad628141281a8c08391dab6cef`,
  equal to the counter's pin.

## Producing commands
- `.venv/bin/python independent_c1.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --json > result.json` -> exit 0, UTC 2026-10-22T18:35:12Z. Output excerpt: `{"rows":187,"named":137,"right":137,"wrong":0,"no_name":50,"differs":[]}`.
- Cross-check cell (import of `tools/round-25/a2/resolve-selectors.py` vs `Crypto.Hash.keccak`) -> exit 0: `candidate texts: 147; keccak disagreements with resolver: 0; params_of disagreements with resolver: 0`.

## Tooling installs (operator directive)
- `uv venv` -> CPython 3.15.0 at `<scratch>/.venv`; `uv pip install pycryptodome` -> pycryptodome 4.1.0. Reason: keccak-256 primitive, per assignment. `uv 0.13.0`.
- No pacman transactions (host-wide pause observed).

## Artifacts (under /fast/scratch/hyaku/kaidoku-r28/seats/a2w/ExecIndependentC1/)
- `independent_c1.py` sha256 `51f2ecdf5d9ade9f23a918c289ac0a015e73551235948b94bd59034013df9dc0`
- `result.json` (counts + per-row detail) sha256 `8b5e3cfd43bfc0ab820caa3c22944cc869bca104f0a7c943a969cb0251458643`

## Verdict
The primary-rule triple HOLDS: named 137, right 137, wrong 0, no_name 50,
independently reproduced. No row differs.

Report: .ufo/waves/round-28/a2w/ExecIndependentC1.md
