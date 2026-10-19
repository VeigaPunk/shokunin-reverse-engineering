# EX-03 — Vyper steward/vault carrier (arc3-loop1-round4, chain c1)

Task as dispatched: author a Vyper contract (>=4 external functions incl. one payable
and one view; e.g. a steward/vault shape); record source sha256.
Artifact: `claims/c1/EX-03/token.vy`.

## Source pin

```
acc71444c0d544efbc8f03892c3becea8f12a718453e3be04f4a99c9af789932  token.vy
```

4666 bytes. Compiles clean on `vyper 0.4.3+commit.bff19ea2` (the round's authorized
venv, `.ufo/waves/arc3-loop1-round4/tools/vyper-venv/`, EX-02's receipt).

## External surface (dispatch-bearing)

22 selector-bearing externals + 1 payable fallback (`__default__`, no selector):

| class | count | members |
|---|---|---|
| payable | 1 (+1 payable fallback) | `deposit()`, `__default__` (fallback, selectorless) |
| nonpayable | 9 | `redeem`, `transfer`, `approve`, `transferFrom`, `mint`, `set_steward`, `set_fee`, `pause`, `unpause` |
| view | 11 | `name`, `symbol`, `decimals`, `totalSupply`, `balanceOf`, `allowance`, `steward`, `feeBps`, `paused`, `preview_fee`, `is_steward` |
| pure | 1 | `fee_of` |

Counts are the ABI's own (`abi.json`: 22 function entries = 1 payable + 9 nonpayable
+ 11 view + 1 pure, plus 1 fallback and 1 constructor).

Requirement check: >=4 external functions — 22. >=1 payable — `deposit`, plus the
payable fallback. >=1 view — 11.

## Chain placement

EX-04's `CarrierV.vy` is the ERC-20-**absent** Vyper control; this carrier is the
ERC-20-**present** one (ERC-20 selector set + steward role + payable deposit +
burn-and-send redeem). The chain therefore holds both sides of the r1 entry's
ERC-20-ambient question on Vyper, not just one.

## Read first

- `compile-receipt.txt` — flags, commands, all hashes, the decoder model, attacks, limits.
- `evidence/dispatch-decode.txt` — the K/K derivation (22/22) and both traps.
- `evidence/decode-vyper-dispatch.py` — the decoder, with its keccak self-tests.
- `MANIFEST.sha256` — `sha256sum -c` clean.
