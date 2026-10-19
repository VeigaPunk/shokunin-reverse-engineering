# EX-06 — proposed patch text (NOT applied)

Seat EX-06 | chain c1 | wave arc3-loop1-round1 | 2026-10-19.
These are **proposals as patch text only**. This seat wrote no repo target other than its
own report and artifact directory. Evidence: `claims/c1/EX-06/comparison.md` and
`claims/c1/EX-06/evidence/`.

---

## P1 — fragment for the C1 knowledge entry (new file, e.g. `corpus/knowledge/2026-10-19-<c1-slug>.md`)

Insert as a candidate/section in the new entry. Numbers are measured, not projected.

```markdown
### Candidate — hex vs raw encoding on real solc bytecode (run)

- **claim:** on one real solc-compiled runtime, `inspect-evm-interface <file> hex` and
  `inspect-evm-interface <file> raw` return the same functional payload; the hex form's
  decoded bytecode is byte-identical to the raw carrier.
- **source:** `KdxToken.sol` (sha256 `c2980385…dccba`), solc 0.8.37+commit.f401782d
  (soljson sha256 `221d7a66…bad4c`); runtime 1789 B sha256 `9c40940e…580e`, hex carrier
  sha256 `69a15782…9ad6`. K = 6 planted selectors, computed pre-probe with an
  independent keccak (validated against `keccak256("")` and the r3-07 ERC-20 selectors),
  each found at a PUSH4 immediate site (31/42/53/64/75/86).
- **verify:** both forms, rea-agents@6.7.0 (and @6.4.0), recover 6/6 —
  `095ea7b3/18160ddd/23b872dd/40c10f19/70a08231/a9059cbb`, all `dispatch:"abi"`, with
  `arguments` and `stateMutability` agreeing with the compiler ABI; offsets
  100/148/178/226/254/302 all land on `0x5b` (JUMPDEST). Envelopes are deep-equal after
  normalizing carrier-bound fields; the only differing field is `locations[0].path`.
- **input shape:** accepted — trailing newline, no newline, `0x` prefix, UPPERCASE;
  refused (exit 1, `invalid_request`/`invalid_format`) — interior whitespace, odd length,
  wrapped lines (e.g. `xxd -p` default), CRLF. Message: "Hex carrier requires complete
  hexadecimal byte pairs, an optional 0x prefix and outer ASCII whitespace; interior
  separators are invalid."
- **asymmetry (carry as a hazard):** hex text passed to `raw` → exit 0 with
  `functions: []` (silent empty, no refusal); binary passed to `hex` → typed
  `invalid_request` "Hex carrier must be valid UTF-8."
- **environment:** a writable `TMPDIR` is required; with the quota-exhausted `/tmp`
  tmpfs both forms fail closed as `execution_failure` (exit 1, `retryable:false`,
  errno −122 EDQUOT). Set `TMPDIR` to writable scratch.
- **verified-at:** 2026-10-19 (arc3-loop1-round1, seats EX-05/EX-06; receipts
  `claims/c1/EX-05/`, `claims/c1/EX-06/`).
```

Optional frontier sentence, only if the entry claims the metadata decode:

```markdown
- **metadata caveat:** the terminal CBOR trailer decodes independently to `solc` 0.8.37
  and an `ipfs` digest, but that digest matches neither sha256 nor keccak-256 of the
  re-derived metadata JSON nor of the CBOR blob — do not describe it as "the IPFS hash of
  the metadata file" without a further receipt.
```

## P2 — `PROVINCE.md` EVM row (line 54 at `e845c2b`), proposed replacement text

```diff
-| EVM interface | `rea inspect-evm-interface <file> <raw|hex>` — encoding is POSITIONAL (no `--encoding` flag despite schema); bundled EVMole 0.9.3/WASM | synthetic hex carrier → selector extraction | hand-assembled 81-byte dispatcher recovered all 3 planted ERC-20 selectors; `dispatch:"abi"` (r3-07) |
+| EVM interface | `rea inspect-evm-interface <file> <raw|hex>` — encoding is POSITIONAL (no `--encoding` flag despite schema); bundled EVMole 0.9.3/WASM; carrier must be one unbroken hex line; requires writable `TMPDIR` | real solc 0.8.37-compiled runtime (1789 B) → selector + argument + mutability recovery | 6/6 planted selectors recovered from both encodings, `dispatch:"abi"`, `arguments`/`stateMutability` ABI-consistent, hex ≡ raw after normalizing carrier-bound fields (arc3-loop1-round1, EX-05/EX-06); r3-07's synthetic 81-byte carrier remains the historical floor |
```

## P3 — optional one-line addition to the C1 receipts draft

If the entry keeps a receipts section, this is the EX-06 receipt line:

```text
EX-06 (hex-form twin): rea-agents@6.7.0 + 6.4.0; carriers runtime/creation, 4 hex shapes
+ raw twin + traps; cross-seat diff vs EX-05 (0 diffs, 4 pairs); EDQUOT/TMPDIR control;
evidence claims/c1/EX-06/evidence/ (manifest.sha256.txt).
```
