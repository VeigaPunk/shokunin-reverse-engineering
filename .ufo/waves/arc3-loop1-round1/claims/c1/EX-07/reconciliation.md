# EX-07 — 3-way selector reconciliation (chain c1, arc3-loop1-round1)

Seat: EX-07 (executor). Date: 2026-10-19. Repo HEAD at work: `e845c2b524ad2e59871e004c51a1386e192a74ab`.

## Verdict

**K/K = 6/6.** On the C1 main target (KdxToken runtime bytecode,
sha256 `9c40940ef88c0e82349af0b0bebb31fabf0b71bf68f5117478ac07d7e44e580e`)
all eleven independent source-sets agree exactly — my dispatch-table parse,
my keccak scan, the planted list, the solc ABI, **six probe legs** (EX-05 ×4
including a rerun and a renamed-file replay, EX-06 ×2), with **zero missing,
zero extra**, and
every probe leg's byte offsets equal my independently parsed dispatch-target
offsets, every leg's decoded-bytecode digest pin equal to my sha256. No mismatch.

Replication on a second, independently authored contract (RV-2's `Rv2Token`,
5 selectors): 5/5 across five sources, same offset equality.

## Target and inputs (all sha256-pinned)

| role | path | sha256 |
|---|---|---|
| runtime bytecode (hex carrier) | `/dev/shm/ex06/KdxToken.runtime.hex`; identical copy at `EX-05/kdx-runtime.hex` and `EX-07/target-KdxToken.runtime.hex` | `69a15782678dccdd4d43b2f0af566c2f030fe9dee4de4ef8365bc4b6d1b29ad6` (= probe `subject.digest.sha256`) |
| runtime bytecode (raw carrier) | `/dev/shm/ex06/KdxToken.runtime.bin`; identical at `EX-05/kdx-runtime.bin` and `EX-07/target-KdxToken.runtime.bin` | `9c40940ef88c0e82349af0b0bebb31fabf0b71bf68f5117478ac07d7e44e580e` (= probe `normalized_result.bytecode.sha256`, all legs) |
| planted list (K=6) | `.../EX-06/evidence/planted-K.json` | `063eb723c90a1edf6b0cd273425b198db1ddf431ee5ea4b2aa490e628b333b52` |
| solc ABI | `/dev/shm/ex06/abi.json`; identical at `EX-05/kdx-abi.json` and `EX-07/target-KdxToken.abi.json` | `40ad881eff2a8cbd267fba51a21c1057f82653f51e823698c84daa12e40c2019` |
| probe legs EX-06 | `EX-06/evidence/run-hex-6.7.0.json`, `run-raw-6.7.0.json` | `5188d59f…`, `b374ec27…` |
| probe legs EX-05 | `EX-05/kdx.hex.json`, `kdx.raw.json`, `kdx.raw.rerun.json`, `kdx.raw.renamed.json` | `93188f83…`, `f8be246a…`, `a5d2e542…`, `e45d7778…` |

Two seats (EX-05, EX-06) independently compiled the same source and produced
**byte-identical carriers** (both sha256s above match EX-05's and EX-06's
artifacts), so all probe legs probed the same bytes.

Naming note: **no file named `planted-selectors.txt` exists** in the repo or
`/dev/shm` (exhaustive `find . /dev/shm -name 'planted-selectors*'` → empty).
The planted artifact for the main leg is `planted-K.json`; EX-02's smoke leg
carries `selectors.txt` (K=5). Both were used where applicable.

Evidence self-containment: the reconciled carriers are copied into this seat
dir as `target-KdxToken.runtime.hex` / `.bin` / `.abi.json`, and the driver
re-runs against the local copies
(`reconciliation-run-local-copies.txt`) with the same `VERDICT: ALL SOURCES
AGREE`, so the reconciliation stays reproducible if `/dev/shm` is cleaned.

## Method M1 — dispatch-table parse (independent of the probe)

Own EVM linear-sweep disassembler (`selector-recon.py`; PUSH1..PUSH32 consume
their immediates), plus a strict chain parser anchored on the dispatcher
prologue. Findings:

- **solc 0.8.37 emits the `PUSH0` prologue `5f3560e01c`** (PUSH0; CALLDATALOAD;
  PUSH1 0xe0; SHR), at offset 25; the legacy `60003560e01c` anchor is absent
  (`-1`). The strict chain is 11-byte stride `DUP1 PUSH4 <sel> EQ PUSH2 <dest> JUMPI`.
- Extracted (PUSH4 site → JUMPDEST dispatch target):
  `095ea7b3@31→100`, `18160ddd@42→148`, `23b872dd@53→178`, `40c10f19@64→226`,
  `70a08231@75→254`, `a9059cbb@86→302`.
- These PUSH4 sites are **exactly** `planted-K.json`'s `push4_site_pc`
  (31/42/53/64/75/86) — derived from bytecode, not read from the file.
- Non-dispatch PUSH4 constants in this bytecode: none.
- EQ-site mode (PUSH4 followed by EQ within 3 instrs, JUMPI within 6) yields the
  same 6-element set.

## Method M2 — keccak scan (independent)

Own **pure-Python keccak-256** (`selector-recon.py`, reference-derived sponge,
no third-party deps) computes `keccak256(sig)[:4]` from the solc ABI signatures,
then searches the raw bytecode for each 4-byte selector. Cross-validation:
my keccak matches **js-sha3** (from solc's own dep tree,
`.ufo/waves/.../tools/solc-prefix/node_modules/js-sha3`) on all 7 probe strings
with full-hash equality (`keccak-vs-jssha3.txt` → `AGREEMENT 7/7`), and matches
the standard vectors (`selector-recon.py keccak-test` → `VECTORS PASS`).

Result: **6/6 found**, first-occurrence offsets 32/43/54/65/76/87 (PUSH4 opcode
at 31/42/53/64/75/86 — immediate byte follows the opcode).

## Source-set comparison (driver: `reconcile.py`, output: `reconciliation-run-all-legs.txt`)

| source | n | vs M1 |
|---|---|---|
| M1 chain (strict parse) | 6 | reference |
| M1 EQ-sites (loose parse) | 6 | MATCH |
| ABI-derived selectors (M2 input) | 6 | MATCH |
| PLANTED `planted-K.json` | 6 | MATCH |
| PROBE EX-06 `run-hex-6.7.0.json` | 6 | MATCH |
| PROBE EX-06 `run-raw-6.7.0.json` | 6 | MATCH |
| PROBE EX-05 `kdx.hex.json` | 6 | MATCH |
| PROBE EX-05 `kdx.raw.json` | 6 | MATCH |
| PROBE EX-05 `kdx.raw.rerun.json` | 6 | MATCH |
| PROBE EX-05 `kdx.raw.renamed.json` | 6 | MATCH |
| M2 keccak scan (presence in code) | 6 | MATCH |

`missing=[] extra=[]` for every row. Verdict line emitted by the driver:
`VERDICT: ALL SOURCES AGREE`. (EX-05's JSONs are `{ok,data,meta}`-wrapped; the
driver unwraps them.)

## Offset agreement (strongest evidence)

The probe's `raw_result.functions[].bytecodeOffset` (100/148/178/226/254/302)
equals my parsed JUMPDEST dispatch targets **exactly, for all 6, on all six
legs**. This independently confirms the r4 errata semantics
(`corpus/knowledge/2026-10-13-r3-evm-interface.md:149-155`): the field records
the dispatch-target position, not the PUSH4 comparison site.

Encoding convergence re-derived by me: my `raw`-mode extraction of
`KdxToken.runtime.bin` gives the same code sha256 and the identical chain as
`hex` mode. EX-05 separately re-ran my `selector-recon.py` against its own
probed carrier and recorded byte-identical output (`EX-05/ex07-crosscheck.txt`,
sha256 `c695a93c…`; captured 10:05:49Z by EX-05) — a fourth-party run of the
extractor reproducing M1/M2 exactly.

## Controls / attacks attempted

1. **Keccak independence** — own implementation vs js-sha3: 7/7 agree; vectors PASS.
2. **Tamper control** — flipped byte 87 (`a9`→`aa`) in a `/var/tmp` copy:
   M1 then reports `aa059cbb@86` and M2 drops to 5/6 (missing `a9059cbb`).
   The agreement is byte-sensitive, not parroting the planted list.
3. **Dispatch-less control** — carrier `6001600101`: no anchor, empty chain,
   empty EQ set (no false positives).
4. **Extra-PUSH4 control (Rv2Token)** — a PUSH4 `16ee4b79@1900` sits in the
   CBOR/ipfs metadata trailer and is correctly excluded from the dispatch set.
5. **Digest pins** — all six legs pin `9c40940e…` as decoded bytecode sha256;
   my sha256 of the same file is identical; hex carrier file sha256
   (`69a15782…`) equals every leg's subject digest.
6. **Creation-vs-runtime** — probes on **creation** code return
   `functions: []` (RV-2's `probe-EX02-smoke-bin-6.4.0.json`; EX-05's
   `kdx-creation.raw.json`, sha256 `e6f1b60a…`). All reconciliation here is
   against runtime bytecode, the correct carrier class.
7. **Encoding-mismatch control** — `hex` encoding applied to the binary
   `.bin` file (EX-05 `kdx.hex-on-bin.json`, sha256 `ab073b51…`) returns a
   typed refusal (`invalid_request` / `invalid_input`, retryable) — the probe
   fails closed rather than mis-decoding.

## Replication on a second target (Rv2Token)

`.../claims/c1/RV-2/Rv2Token.runtime.hex` (sha256 `d7f73058…`): my M1 chain
`095ea7b3@31→89, 18160ddd@42→137, 23b872dd@53→167, 70a08231@64→215, a9059cbb@75→263`
— the destinations equal the probe `bytecodeOffset`s in RV-2's 6.4.0/6.7.0
hex+raw runs; M2 5/5; ABI 5/5; RV-2's `expected-selectors.txt` 5/5.

## Gaps

- None blocking. Residual notes: `planted-selectors.txt` (exact name) does not
  exist — `planted-K.json` used; the probe legs are all rea 6.4.0/6.7.0
  (EVMole 0.9.3) — no 6.5.0 leg was probed by any seat this round.

## Reproduce

Note: EX-05's evidence JSONs are `{ok,data,meta}`-wrapped, so unwrap the four
legs first (pure `data` extraction; upstream hashes are recorded above):

```bash
cd .ufo/waves/arc3-loop1-round1/claims/c1/EX-07
python3 selector-recon.py keccak-test
python3 selector-recon.py extract ./target-KdxToken.runtime.hex hex
python3 selector-recon.py scan ./target-KdxToken.runtime.hex hex /var/tmp/ex07/kdx-sigs.txt
mkdir -p /var/tmp/ex07/ex05-unwrapped
python3 -c 'import json,sys,os
for s in sys.argv[1:]:
    d=json.load(open(s)); assert d.get("ok") is True and "data" in d, s
    json.dump(d["data"], open("/var/tmp/ex07/ex05-unwrapped/"+os.path.basename(s),"w"))' \
  ../EX-05/kdx.hex.json ../EX-05/kdx.raw.json ../EX-05/kdx.raw.rerun.json ../EX-05/kdx.raw.renamed.json
python3 reconcile.py --code ./target-KdxToken.runtime.hex hex \
  --abi ./target-KdxToken.abi.json --planted ../EX-06/evidence/planted-K.json \
  --probe ../EX-06/evidence/run-hex-6.7.0.json ../EX-06/evidence/run-raw-6.7.0.json \
          /var/tmp/ex07/ex05-unwrapped/kdx.hex.json /var/tmp/ex07/ex05-unwrapped/kdx.raw.json \
          /var/tmp/ex07/ex05-unwrapped/kdx.raw.rerun.json /var/tmp/ex07/ex05-unwrapped/kdx.raw.renamed.json
```

`reconciliation-run-reproduce.txt` is exactly this run and is **byte-identical**
(sha256 `a356c3a9…`) to `reconciliation-run-all-legs.txt`, which was produced by
the same driver with in-file unwrapping before it was reverted — see the
manifest note below.

Manifest note: EX-14's `MANIFEST.draft.check.sha256` and
`claims/c1/receipts/MANIFEST.draft.txt` pin seven files in this seat dir
(captured 10:02:05–10:04:25Z). This seat restored `reconcile.py` to the pinned
bytes (`c1be2731…`, 4979 B) after briefly editing it for the unwrap, and
regenerated the pinned `__pycache__/selector-recon.cpython-314.pyc`
(`4be5e6ab…`, via the importlib path that created it) — all seven pinned
entries verify with `sha256sum -c`. Any future edit to `reconcile.py` must
re-pin those manifests.

Artifacts in this dir: `selector-recon.py` (sha256 `99c3c32d…`), `reconcile.py`
(`c1be2731…`), `reconciliation-run.txt` (`ddf5b5c7…`),
`reconciliation-run-all-legs.txt` (`a356c3a9…`),
`m1-kdxtoken-runtime.json` (`a0b63490…`), `m2-kdxtoken-keccak.json`
(`1a293f88…`), `m1-rv2token-runtime.json`, `keccak-vs-jssha3.txt`
(`169252c7…`), `target-KdxToken.runtime.{hex,bin}`, `target-KdxToken.abi.json`.
