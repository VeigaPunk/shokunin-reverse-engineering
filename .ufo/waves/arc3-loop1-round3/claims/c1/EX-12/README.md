# EX-12 — chain c1, executor (arc3-loop1-round3) — controls

Seat task: (a) non-bytecode file → honest typed refusal; (b) carrier A **CREATION**
code → parsed-and-empty expectation (r1 precedent); capture both envelopes.

Repo HEAD at work: `c07af80`. No git mutations; writes only in this dir + `seats/EX-12.md`.
Scratch `/var/tmp/ex12-*`; `/tmp` never used (EDQUOT hostquake, standing).

## Inputs

| carrier | source | pinned sha256s | role |
|---|---|---|---|
| **chain carrier A** (EX-03's `CarrierA`) | `../EX-03/source/carrierA.sol` | source `05b2cbb0…`; `carrierA.creation.hex` `688c5e0f…`; decoded creation `76ec07f9…`; planted K=9 (`d905412a…`) | primary control (b) target |
| seat-local second carrier `VaultA` | `VaultA.sol` (this dir) | source `75d12604…`; `VaultA.creation.hex` `43f7b81b…`; decoded creation `6885bd63…`; runtime hex `f4ac24b7…` / decoded `f76779a4…`; K=7 + payable receive/fallback | control (b) replication + control (a) input + runtime contrast |

Both compiled on-host with the receipted r1 solc prefix (re-verified this seat:
`soljson.js 221d7a66…abad4c`, `solc.js 188c3fdc…146f`, `0.8.37+commit.f401782d.Emscripten.clang`),
`--optimize --optimize-runs 200`. No install performed.

## Captured envelopes (primary, subject paths inside the repo)

| leg | exit | result | envelope |
|---|---|---|---|
| `carrierA.creation.hex` hex @6.4.0 | 0 | 0 fns, `kind:"unknown"`, decoded sha `76ec07f9…` | `probe-carrierA-creation-hex-6.4.0.json` |
| `carrierA.creation.hex` hex @6.7.0 | 0 | same payload | `probe-carrierA-creation-hex-6.7.0.json` |
| `carrierA.sol` hex @6.4.0 | 1 | typed `invalid_request` / `invalid_input` | `probe-carrierA-source-hex-6.4.0.json` |
| `carrierA.sol` raw @6.4.0 (boundary) | 0 | 2315 B as code, 0 fns (no refusal on raw path) | `probe-carrierA-source-raw-6.4.0.json` |
| `VaultA.creation.hex` hex @6.4.0 (+ byte-identical rerun) | 0 | 0 fns, `kind:"unknown"`, sha `6885bd63…` | `probe-creation-hex-6.4.0{,-rerun}.json` |
| `VaultA.creation.hex` hex @6.7.0 | 0 | same payload | `probe-creation-hex-6.7.0.json` |
| `VaultA.sol` hex @6.4.0 / @6.7.0 | 1 | typed `invalid_request` / `invalid_input` | `probe-nonbytecode-hex-6.4.0.json`, `…6.7.0.json` |
| `VaultA.abi.json` hex @6.4.0 | 1 | typed `invalid_request` / `invalid_input` | `probe-jsonfile-hex-6.4.0.json` |
| `empty.bin` (0 bytes) hex @6.4.0 | 0 | parsed-and-empty: 0 B bytecode, 0 fns | `probe-empty-hex-6.4.0.json` |
| `VaultA.runtime.hex` hex @6.4.0 / @6.7.0 (contrast) | 0 | 7/7 planted selectors | `probe-runtime-hex-6.4.0.json`, `…6.7.0.json` |
| r1 precedent `Rv2Token.creation.hex` @6.4.0 | 0 | id re-derived `ev_c80379e1d3f7…` (r1 landed) | `scratch-probe-rv2-creation-hex-6.4.0.json` |

`scratch-probe-*.json` are the earlier /var/tmp-path runs that establish the
pre-registered sequencing (see `expectations-preregistered.txt`,
`expectations-additional.txt`, `timestamps.txt`).

## Recheck recipe

```bash
export TMPDIR=/var/tmp/any-disk-backed-dir      # /tmp defaults fail EDQUOT
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
npx -y rea-agents@6.4.0 inspect-evm-interface \
  .ufo/waves/arc3-loop1-round3/claims/c1/EX-03/carrierA.creation.hex hex --format json
# expect exit 0, 0 functions, bytecode.kind "unknown", bytecode.sha256 76ec07f9db98d5…
npx -y rea-agents@6.4.0 inspect-evm-interface \
  .ufo/waves/arc3-loop1-round3/claims/c1/EX-03/source/carrierA.sol hex --format json
# expect exit 1, {"code":"invalid_request","category":"invalid_input"} (stdout JSON)
```

The `ev_` id domain for this verb family is unmeasured; compare by
`subject.digest.sha256` + function payload (ids re-derive per identical
path+bytes: creation @6.4.0 rerun → byte-identical envelope file).

## Identity discipline

- `sha256s-final.txt` lists every artifact in this dir except itself, re-derived after
  the final revision. EX-03's manifest hashes for the files probed here were re-derived by
  this seat (match: `688c5e0f…`, `05b2cbb0…`, `d905412a…`; decoded creation
  `76ec07f9…` equals EX-03's `carrierA.creation.bin`).
- Observation (id domain): identical bytes at a different subject path mint a
  different `ev_` id — scratch-path creation `ev_6f1f435a5a5d7…` vs repo-path
  `ev_e87de6c462a6…` (same bytes `43f7b81b…`, same pin). Id is not content-addressed
  on bytes alone; no identity claim beyond same-path reruns.

## Deviations / notes

- Pre-registered expectation for the 0-byte file was "typed refusal"; measured:
  exit 0, parsed-and-empty (artifact/bytecode sha = SHA-256 of empty string). The
  non-bytecode refusal control rests on text files (`.sol`, `.json`), not on
  emptiness. Recorded as a falsified expectation, not a defect.
- Non-bytecode refusal class was captured in **hex form**; the raw-form leg is
  deliberately recorded as exit 0 (bytes-as-code) so the control is not misread
  as "non-bytecode always refuses".
- Carrier A's 9 planted selectors are physically present in both the creation blob
  (embedded runtime at byte 34 of 1460) and the runtime; the probe still reports 0
  functions for the creation blob → parsed-and-empty semantics = parsed but no
  dispatch reported, not "no dispatch bytes present".