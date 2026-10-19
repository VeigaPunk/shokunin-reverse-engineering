# EX-06 — hex-encoding form of the C1 EVM probe vs the raw form

Seat EX-06 | chain c1 | role executor | wave arc3-loop1-round1 | 2026-10-19.
Deliverable required by the seat line: *run the hex-encoding form of the same probe;
compare against EX-05's raw-form output (equivalence or documented difference)*.

**Verdict: EQUIVALENT.** On the identical carrier bytes, `hex` and `raw` produce
envelopes that are deep-equal after normalizing the four carrier-bound fields
(`evidence_id`, `subject.{name,local_path,digest}`, `parameters.{path,encoding}`,
`normalized_result.artifact`, `locations[*].path`). The functional payload — selector
set, `bytecodeOffset`, `dispatch`, `arguments`, `stateMutability`, decoded-bytecode
sha256, CBOR metadata — is identical, and the hex form's decoded bytecode is
byte-identical to the raw carrier (sha256 `9c40940e…580e` both ways).
Documented non-equivalences are all input-shape or envelope-shape, never decoding
(§5), plus one asymmetry hazard (§5.2).

All probe runs were executed on scratch copies (`/dev/shm/ex06`, see §7); no repo
target was written by this seat.

---

## 1. Artifact under test

| Item | Value | Evidence |
|---|---|---|
| Source | `KdxToken.sol` (ERC-20-style, 6 external functions), sha256 `c29803852501641cbb1b6c6e42ecdaef0497e9addf9950069138fa43cd3dccba` | `evidence/KdxToken.sol`; transcript step 1 |
| Compiler | solc **0.8.37**+commit.f401782d.Emscripten.clang (`soljson.js` sha256 `221d7a667378b5068d913e75fe092507e061363cd1d23b64c49ae82febabad4c`, wave-local prefix `tools/solc-prefix`, EX-02's install) | transcript header |
| Runtime bytecode | 1789 B, sha256 `9c40940ef88c0e82349af0b0bebb31fabf0b71bf68f5117478ac07d7e44e580e` | transcript step 1 |
| Creation bytecode | 1817 B, sha256 `6aeba8d7fe1c4a871fb0fdabde1f47de91408c1006bd29050d937b3b74c8e84c` | transcript step 1 |
| Hex carrier | 3579 B ASCII, sha256 `69a15782678dccdd4d43b2f0af566c2f030fe9dee4de4ef8365bc4b6d1b29ad6` | transcript step 1 |

The carrier is **byte-identical to EX-05's probe subject**: their `kdx-runtime.bin`
sha256 `9c40940e…580e` and `kdx-runtime.hex` sha256 `69a15782…9ad6` match mine exactly
(`sha256sum claims/c1/EX-05/kdx-runtime.*`). The cross-seat comparison in §4 therefore
runs on one shared artifact, not on two lookalikes.

## 2. Planted K recorded pre-probe (independent of the probe)

K = **6** selectors, computed from the compiler ABI with a keccak-256 implementation
written for this seat (`evidence/keccak.js`), validated against four independent
anchors before use — `keccak256("")` = `c5d24601…a470`, and the three ERC-20 selectors
recorded in the lane's own corpus (`transfer`/`balanceOf`/`approve`, r3-07 entry)
(`evidence/keccak-anchors.txt`: all four PASS). Cross-check: the same implementation
reproduces EX-02's independently computed `Smoke.sol` selector set 5/5 (`diff` against
`claims/c1/EX-02/smoke/selectors.txt` → identical apart from EX-02's trailing `K=5` line).

| Selector | Signature | ABI mutability | PUSH4 site (linear scan of the compiled runtime) |
|---|---|---|---|
| `0x095ea7b3` | approve(address,uint256) | nonpayable | 31 |
| `0x18160ddd` | totalSupply() | view | 42 |
| `0x23b872dd` | transferFrom(address,address,uint256) | nonpayable | 53 |
| `0x40c10f19` | mint(address,uint256) | nonpayable | 64 |
| `0x70a08231` | balanceOf(address) | view | 75 |
| `0xa9059cbb` | transfer(address,uint256) | nonpayable | 86 |

(`evidence/planted-K.json`; 6/6 selectors found at PUSH4 immediates, 6 PUSH4 sites total.)

## 3. Runs (rea-agents@6.7.0 unless noted; TMPDIR=/dev/shm/ex06/tmp)

| Run | Form | Carrier | Carrier sha256 | exit | decoded bytecode sha256 | functions |
|---|---|---|---|---|---|---|
| `run-raw` | raw | `KdxToken.runtime.bin` | `9c40940e…580e` | 0 | `9c40940e…580e` | 6 |
| `run-hex` | hex | `KdxToken.runtime.hex` (trailing LF) | `69a15782…9ad6` | 0 | `9c40940e…580e` | 6 |
| `run-hex-nonl` | hex | no trailing LF | `64572cc6…1dfc6` | 0 | `9c40940e…580e` | 6 |
| `run-hex-0x` | hex | `0x`-prefixed | `2cca62df…0afd` | 0 | `9c40940e…580e` | 6 |
| `run-hex-upper` | hex | UPPERCASE | `370447c1…3ab81` | 0 | `9c40940e…580e` | 6 |
| `run-hex-repeat` | hex | repeat of `run-hex` | `69a15782…9ad6` | 0 | `9c40940e…580e` | 6 |
| `run-creation-hex` / `-raw` | hex / raw | creation blob | — | 0 / 0 | `6aeba8d7…e84c` | 0 |
| `run-hex-6.4.0` / `run-raw-6.4.0` | hex / raw | @6.4.0 | — | 0 / 0 | `9c40940e…580e` | 6 |

Recovered payload (identical in every run above; transcript step 4):

```
095ea7b3 offset 100 dispatch=abi args=address,uint256      stateMutability=nonpayable
18160ddd offset 148 dispatch=abi args=                    stateMutability=view
23b872dd offset 178 dispatch=abi args=address,address,uint256 stateMutability=nonpayable
40c10f19 offset 226 dispatch=abi args=address,uint256      stateMutability=nonpayable
70a08231 offset 254 dispatch=abi args=address             stateMutability=view
a9059cbb offset 302 dispatch=abi args=address,uint256      stateMutability=nonpayable
```

K/K = 6/6 in every form; `dispatch` is `"abi"` for all six. `arguments` and
`stateMutability` agree with the compiler ABI's declared types/mutability — the
frontier signal r3-07 could not obtain from hand-assembled stubs (there: `arguments:""`,
`stateMutability:"pure"` artifacts).

## 4. Equivalence measurement (commands + output)

Normalized deep comparison (`evidence/compare.js`, transcript step 4):

- `run-raw` vs `run-hex`: **1 diff**, `.locations.0.path` (`…runtime.bin` vs `…runtime.hex`).
  Everything else, including all six function records and the metadata block, is equal.
- Same single-path diff for `run-hex-nonl`, `run-hex-0x`, `run-hex-upper`, `run-hex-repeat`.
- `run-hex` vs `run-hex-repeat`: **0 diffs** (byte-identical stdout, 9961 B both) —
  the probe is deterministic for a fixed carrier path; `evidence_id` is stable across repeats.
- Byte-identity check: `Buffer.from(<hex text>.trim(),'hex').equals(<raw bytes>)` → `true`.

Cross-seat comparison (`evidence/compare-ex05.js` → `evidence/ex05-cross-seat-comparison.txt`;
EX-05 envelopes are wrapped `{ok,data,meta}`, read as `.data`):

| Pair | Result |
|---|---|
| EX-05 `kdx.raw.json` vs my hex run on EX-05's bytes | **0 diffs** after normalization |
| EX-05 `kdx.raw.json` vs my raw run on EX-05's bytes | **0 diffs** |
| EX-05 `kdx.hex.json` vs my hex run on EX-05's bytes | **0 diffs** |
| EX-05 `kdx.raw.json` vs EX-05 `kdx.hex.json` | **0 diffs** |

So the equivalence holds both within one seat's pair and across two seats' independent
invocations, at 6.7.0 and at 6.4.0.

## 5. Documented differences (none are decoding differences)

### 5.1 Input-shape acceptance (`evidence/traps-summary.txt`)

Accepted (exit 0, identical payload): trailing LF, no trailing LF, `0x` prefix,
UPPERCASE hex. Refused (exit 1, typed `invalid_request`, `reason:"invalid_format"`):
interior whitespace, odd-length hex, 64-char line wrapping, CRLF wrapping.
Message (verbatim): *"Hex carrier requires complete hexadecimal byte pairs, an optional
0x prefix and outer ASCII whitespace; interior separators are invalid."*
Practical consequence for the C1 knowledge entry: a hex dump produced by a wrapping tool
(`xxd -p` default output) is **not** a valid carrier; the carrier must be one unbroken line.

### 5.2 Shape-mismatch asymmetry — a hazard worth recording

- **hex text fed to the `raw` form**: exit **0**, 0 functions, no refusal
  (`evidence/trap-raw-of-hex.json`: subject sha256 = the ASCII file, bytecode sha256 = the
  ASCII bytes, `functions: []`). A silent-empty success — a caller that passes the wrong
  encoding here gets a plausible envelope with no selectors instead of an error.
- **binary fed to the `hex` form**: exit **1**, typed refusal
  (`evidence/trap-hex-on-bin.json`: *"Hex carrier must be valid UTF-8."*), independently
  reproduced and also present in EX-05's `kdx.hex-on-bin.json`.

The claim's honest-stop branch "encoding mismatch (positional raw|hex — verify both)" is
therefore **not triggered** — both forms were verified on the real artifact — but the
mismatch direction is not symmetric, which is worth one sentence in the entry.

### 5.3 Envelope differences across tool versions (payload unchanged)

6.4.0 vs 6.7.0 on the same hex carrier: the functional payload is identical
(bytecode sha256, all six function records, metadata); the differences are
`limitations` wording/order and the presence of `relationship_coverage` at 6.4.0 only
(transcript step 4 comparison of `run-hex.json` vs `run-hex-6.4.0.json`).
No decoding difference; version context for any receipt.

### 5.4 `evidence_id` binds carrier path and encoding

`ev_…` differs between the raw and hex runs of the same bytes and differs again for a
renamed copy (EX-05's `kdx.raw.renamed.json` = `ev_b2937090…` vs their `kdx.raw.json` =
`ev_4dd5ea20…`); it is stable across repeats at a fixed path. Hex-vs-raw equality is a
payload property, not an evidence-id property.

### 5.5 Environmental: a writable `TMPDIR` is required (EDQUOT)

With `TMPDIR` unset (system temp = `/tmp`, a 16 GiB tmpfs whose `usrquota` is exhausted
by fleet scratch: `df /tmp` → 13G used; a 1-byte control write to `/tmp` fails with
`Disk quota exceeded`), both forms fail closed:

```
{"code":"execution_failure","category":"execution_failure","retryable":false,
 "details":{"provider_id":"evmole-interface","operation":"inspect_evm_interface",
 "diagnostics":{"phase":"worker", … "reason":"Unknown system error -122: … write"}}}
```

exit 1, for `raw` and for `hex` alike (transcript step 6). errno −122 = EDQUOT.
Setting `TMPDIR` to writable scratch makes both succeed with no other change. The
failure is encoding-independent and environmental; the probe's own runtime root is
what writes. `LOG.md:1163` already records the `/tmp` tmpfs quota as a known condition.

### 5.6 `bytecodeOffset` semantics re-confirmed on real solc output

All six recovered offsets (100/148/178/226/254/302) land on byte `0x5b` (JUMPDEST) —
the r4 erratum's correction (offset = dispatch-target position, not the PUSH4 site)
holds on real compiler output, not only on the r3 hand-assembled carrier.

### 5.7 Metadata trailer: independent decode agrees; one digest unexplained

Independent CBOR decode of the carrier's terminal metadata (`cborg`, transcript step 8)
reproduces the probe's `metadata` block exactly: `cborLength 51`, `metadataStart 1736`,
`solc` = bytes `000825` (0.8.37), `ipfs` digest `02c77fc1412b672dc777d172eae5a260a387164e27c83e6cc41208ce3f7d3ecc`.
**Unresolved:** that ipfs digest matches neither sha256 nor keccak-256 of the metadata
JSON re-derived from the same compilation (`9128fa3e…` / `0490a768…`) nor of the CBOR
blob (`44e987b8…` / `b0e92443…`). Not investigated further this seat; flagged so the
knowledge entry does not over-claim "IPFS hash of the metadata file" without a receipt.

## 6. What this does and does not establish

- Establishes (C1 claim items b, c, and the encoding branch): a real on-host solc
  compile, K = 6 planted pre-probe, 6/6 recovered with `dispatch:"abi"` and
  ABI-consistent `arguments`/`stateMutability`, from **both** encodings, reproducibly,
  at 6.4.0 and 6.7.0, cross-checked against EX-05's independent invocation on the same bytes.
- Does **not** establish: command A's 81 → 82 knowledge count, the map token, the
  receipts, or the corpus entry itself — none of which this seat may touch. EX-11 holds
  the pre-state (81/81, 13/13, `claims/c1/EX-11/command-A-before.txt`).
- `bytecode.kind` remains `"unknown"` for both runtime and creation code on real solc
  output — the classification frontier named in r3-07 is still open.

## 7. Environment and deviation from the stated scratch location

`/tmp` is a 16 GiB tmpfs with `usrquota`, ~13 GiB consumed by other seats; this seat's
writes there fail with EDQUOT (`printf … > /tmp/…` → `Disk quota exceeded`), so all
scratch was placed in `/dev/shm/ex06` (also tmpfs) and the wave dir stayed untouched
except this seat's own artifact directory. `evidence/repro.sh` reproduces every number
above and sets `TMPDIR` accordingly.

## 8. Evidence files (`evidence/`)

| File | Content |
|---|---|
| `transcript.txt` | full run of `repro.sh` (environment, compile, planted K, all runs, comparisons, traps, EDQUOT control, offset check, metadata decode) |
| `repro.sh` | reproduction script (scratch-only; `TMPDIR` set) |
| `run-raw-6.7.0.json`, `run-hex-6.7.0.json` | primary envelopes |
| `run-hex-6.4.0.json`, `run-raw-6.4.0.json` | version cross-check |
| `run-creation-hex.json`, `run-creation-raw.json` | creation-blob runs |
| `my-hex-on-ex05-bytes.json`, `my-raw-on-ex05-bytes.json` | my runs on EX-05's exact carrier bytes |
| `ex05-cross-seat-comparison.txt`, `compare-ex05.js` | cross-seat diff output and script |
| `compare.js`, `keccak.js`, `plant.js`, `compile.js`, `KdxToken.sol` | tooling + source under test |
| `keccak-anchors.txt`, `planted-K.json`, `traps-summary.txt` | anchor validation, planted K, trap results |
| `trap-hex-on-bin.json`, `trap-raw-of-hex.json` | mismatch-asymmetry receipts |
| `manifest.sha256.txt` | sha256 of every file in this directory |
