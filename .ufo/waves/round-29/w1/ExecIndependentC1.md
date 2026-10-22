# R29-C1 independent primary-triple recount

## Finding

**Observation —** An independent scorer read the pinned evidence at `18be864a528873b2b70d8c94e31f880290249e90` with `git show`: heldout TSV, all 16 REA envelopes, all 16 compiled ABIs, the 152 held-out Openchain responses, and `tally.json` (186 blobs total). The scorer does not import or invoke lane counter/resolver code. It takes recovered selectors and inferred arguments from `normalized_result.functions`, then names a row only when exactly one Openchain candidate has `filtered=false` and canonical parameter types equal to REA's inferred arguments. It reads the tally only for the requested per-row/summary comparison.

**Observation —** Results: **named 122, right 122, wrong 0, no_name 30**; **args_match 125**; REA recovered **152/152** held-out selectors. Independent PyCryptodome Keccak checks matched the held-out selector for **152/152** ABI signatures. The independent summary matches the tally and there are **no row-level differences**.

**Inference — verdict: holds.** The entry's triple `named 122, right 122, wrong 0` is reproduced.

## Retained evidence

Scorer command:

```text
/fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecIndependentC1/venv/bin/python /fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecIndependentC1/score_c1.py
```

UTC: `2026-10-22T20:24:02+00:00` (emitted as `run_utc`); exit code: **0** (successful command return). Exact stdout excerpt:

```json
{
  "abi_keccak_checks": {
    "checked": 152,
    "failures": []
  },
  "args_match": 125,
  "counts": {
    "named": 122,
    "no_name": 30,
    "right": 122,
    "wrong": 0
  },
  "input_files_read": 186,
  "summary_matches_tally": true,
  "tally_row_differences": [],
  "triple_verdict": "holds"
}
```

The scorer's input-manifest SHA-256 was `3ee3c3ff87200ae2601cc573511a03a97197095ae4ef0418bb9750abda34d052`.

Artifact hashes, produced by `sha256sum` at `2026-10-22T20:24:06Z` (exit code **0**):

- `/fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecIndependentC1/score_c1.py` — `67fe683a6fb4b016837f3a00036eeb4dcf2c7d1a29e4df6a1c7022c0f1a60af9`
- `/fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecIndependentC1/run-output.json` — `49ca655cafd8ae6c47ba4f6a1b4abefce110645c729eaa680e59659ce4b5e7d8`

## Tooling, risk, blockers

- Installed `pycryptodome==4.1.0` into the scoped `uv venv` using `uv pip` (uv `0.13.0`, CPython `3.15.0`) solely for independent Keccak-256 selector checks. No pacman transaction.
- No network lookup, external source fetch, or REA run was used.
- **Risk/limitation —** Keccak confirms the 152 held-out ABI signature/selector pairs; it does not establish deployed-contract identity or independently validate REA's recovered arguments. The recount intentionally uses the pinned REA envelope fields as the assignment specifies.
- **Blockers — none.**