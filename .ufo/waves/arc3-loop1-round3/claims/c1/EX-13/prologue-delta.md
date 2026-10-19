# EX-13 — prologue / dispatch-shape delta: optimizer-enabled carriers vs r1's recorded prologue classes

Seat EX-13 (chain c1, executor) — arc3-loop1-round3, 2026-10-19.
Task: compare the optimizer-enabled carriers' dispatcher bytes vs r1's recorded
prologue classes (`5f3560e01c` / `60003560e01c`); document the delta as the round's
shape finding.

Headline: **the prologue class does not shift under `--optimize --optimize-runs 200`
— every round-3 carrier (optimizer on and off) emits the r1-recorded PUSH0 prologue
`5f3560e01c`, at anchor pc 25 (nonpayable preamble) or pc 13 (payable/receive
preamble); zero `60003560e01c` and zero `60043560e01c` occurrences exist in any of
the 26 compiled runtimes.** The measured delta lives one level up: a second
dispatcher-topology class — **pivot-GT sorted binary search** at K ≥ 7 selectors
(linear-EQ only at K ≤ 6) — which is *not* an optimizer effect (present optimizer-off
too) and does not defeat the extractor (K/K on every probed leg, up to K=33 /
3,040 B runtime).

## 1. Toolchain and custody (verified before use)

| item | identity | check |
|---|---|---|
| solc prefix (r1 reuse, no install) | `.ufo/waves/arc3-loop1-round1/tools/solc-prefix/` | `solcjs --version` → `0.8.37+commit.f401782d.Emscripten.clang` |
| `soljson.js` | sha256 `221d7a667378b5068d913e75fe092507e061363cd1d23b64c49ae82febabad4c` | == r1 EX-02 install-receipt pin |
| `solc.js` | sha256 `188c3fdca72bbb8ec1c70373427ad4536e117341c48944dae9185f9cf035146f` | == r1 EX-02 install-receipt pin |
| probe bin 6.4.0 | `~/.npm/_npx/dea9475797100b20/.../rea.mjs` sha256 `3554288a08c455fa419dad662d73710fb17debe94b9e71dd1282761117c5981e` | == EX-08 r1-recorded identity (npx cache, no install/network) |
| probe bin 6.7.0 | `~/.npm/_npx/a1722018f28f9df2/.../rea.mjs` sha256 `ed06cee49505b95a3cc5fceb1b4b279167e26df86227c644bb366ffffdbaf738` | == EX-08 r1-recorded identity |
| provider | `evmole-interface` / evmole@0.9.3 | probe envelopes |
| evmVersion (default) | `osaka` (metadata of every on200 leg) | matches EX-04's independent reading |

Compile path validation: Rv2Token compiled optimizer-off from the r1-retained source
(`src/Rv2Token.sol`, sha256 `a4bc2d78…`) reproduces r1's recorded bytes exactly —
runtime 1,943 B sha256 `c1081a565869b50387211b25afaf3768294aa774c35845bc3a8c0b12cfe15e74`
(= r1 `c1081a56…`) and hex-carrier file sha256 `d7f73058…` (= r1 `d7f73058…`). The
pipeline is therefore validated against the r1 record before any delta claim below.
Scratch: `/var/tmp/ex13` (host `/tmp` is quota-broken; probes ran with
`TMPDIR=/var/tmp/ex13/tmp`). Custody paths untouched by this seat.

## 2. Carrier matrix (26 compiled runtimes; all sha256-pinned)

| tag | contract | K | optimizer | runtime B | runtime sha256 (prefix) | prologue class | topology | anchor pc |
|---|---|---|---|---|---|---|---|---|
| rv2-off | Rv2Token | 5 | off | 1943 | `c1081a56…` | PUSH0 | linear-EQ | 25 |
| rv2-on200 | Rv2Token | 5 | on, runs 200 | 978 | `ed6c8a76…` | PUSH0 | linear-EQ | 25 |
| gau-off | Gauge (+internal lib) | 6 | off | 1152 | `10110071…` | PUSH0 | linear-EQ | 25 |
| gau-on200 | Gauge | 6 | on, runs 200 | 555 | `aa3dcc48…` | PUSH0 | linear-EQ | 25 |
| tre-off | Treasury (payable receive+fallback) | 8 | off | 2480 | `bd5a6545…` | PUSH0 | pivot-GT | 13 |
| tre-on200 | Treasury | 8 | on, runs 200 | 1233 | `13fa3a62…` | PUSH0 | pivot-GT | 13 |
| fk5-off/on200 | FineK5 | 5 | off / on | 722 / 376 | `85431cd5…` / `25d1b7db…` | PUSH0 | linear-EQ | 25 |
| fk6-off/on200 | FineK6 | 6 | off / on | 802 / 418 | `2670aea3…` / `8e92c45e…` | PUSH0 | linear-EQ | 25 |
| fk7-off/on200 | FineK7 | 7 | off / on | 898 / 475 | `709449e6…` / `dbe01b01…` | PUSH0 | **pivot-GT** | 25 |
| fk8-off/on200 | FineK8 | 8 | off / on | 978 / 517 | `ad9581fb…` / `4f8311c7…` | PUSH0 | **pivot-GT** | 25 |
| pk6-off/on200 | PayK6 (receive) | 6 | off / on | 873 / 488 | `85870b69…` / `815e14c3…` | PUSH0 | linear-EQ | 13 |
| pk7-off/on200 | PayK7 (receive) | 7 | off / on | 981 / 557 | `501cd482…` / `4ca893c0…` | PUSH0 | **pivot-GT** | 13 |
| sw8-off/on200 | Sweep8+total | 9 | off / on | 1024 / 536 | `4c3dd6ec…` / `f15ba2ac…` | PUSH0 | **pivot-GT** | 25 |
| sw16-off/on200 | Sweep16+total | 17 | off / on | 1696 / 902 | `57c46253…` / `fe3ebef9…` | PUSH0 | **pivot-GT** | 25 |
| sw32-off/on200 | Sweep32+total | 33 | off / on | 3040 / 1634 | `f4fe2892…` / `d72b0b37…` | PUSH0 | **pivot-GT** | 25 |

Full 64-hex shas in `evidence/summary.json`, `evidence/fine-summary.json`,
`evidence/sweep-summary.json`, and the `out/*.runtime.bin` files (manifest-covered).
Sources: `src/Rv2Token.sol` (r1-retained copy, `a4bc2d78…`), `src/Treasury.sol`
(`54d87df0…`), `src/Gauge.sol` (`c84e06d8…`), FineK5–8, PayK6/7, Sweep8/16/32.

## 3. Findings (delta vs the r1 record)

**F1 — prologue class unchanged by the optimizer; legacy class absent.**
26/26 runtimes carry exactly one `5f3560e01c` anchor; `60003560e01c` and
`60043560e01c` occur 0 times in all 26. r1's recorded classes
(`5f3560e01c`/`60003560e01c`, entry Unknowns line) therefore gain: the PUSH0 class is
stable under `runs=200`, and the legacy class did not re-materialize at solc 0.8.37 /
default evmVersion `osaka` (see §6 residuals).

**F2 — a second, orthogonal preamble class (anchor offset, not class).**
- nonpayable-only carriers: `6080604052 348015 <pc> 57 5f5ffd 5b 50 60043610 <pc> 57`
  then anchor at pc 25 (CALLVALUE guard + calldatasize<4 guard).
- payable receive/fallback carriers: `6080604052 60043610 61007e 57` then anchor at
  pc 13; the `< 4` target (0x7e) begins `5b 36 61 <pc> 57` — the receive/fallback
  split. Same prologue *class* (PUSH0), different anchor offset.

**F3 — dispatch topology class: linear-EQ for K ≤ 6, pivot-GT for K ≥ 7.**
- K=5,6 (rv2, gau, fk5, fk6, pk6): chain of `80 63 <sel> 14 61 <dest> 57` legs, no
  GT/LT compare.
- K=7 (fk7, pk7): first leg is `80 63 <pivot> 11 61 <dest> 57` (GT split), the pivot
  selector then appears again as an EQ leg; remaining legs EQ, stride 11 B.
- K=8,9,17,33 (tre, sw8/16/32): pivot tree; measured pivot counts 1/1/3/7 for
  K=8/9/17/33 (matches a balanced split over the sorted selector set).
- Threshold identical optimizer-off and optimizer-on, and identical in both preamble
  classes (pk6 linear / pk7 pivot) — so it is a selector-count property of the
  compiler's dispatcher, not an optimizer artifact.

**F4 — what the optimizer does change.**
Runtime size shrinks ~44–51% (e.g. 1943→978, 2480→1233, 1152→555 B); destination PCs
move (rv2: EQ dests 89/137/167/215/263 → 89/129/147/166/206; tre-on200 EQ dests
268/301/341/398/418/470/524/532); compare order stays sorted by selector; prologue
class, anchor offset, and topology class are invariant. Optimizer-on code introduces
`4e487b71` (Panic(uint256)) constants (e.g. rv2-on200 @0x363) absent from the off leg.

**F5 — extractor behavior on the new shapes (the claim's honest-stop branch, measured).**
16 probe legs (12 carriers × 6.4.0; 4 carriers × 6.7.0): **K/K, zero missing, zero
extra**, for every leg — including pivot-GT dispatchers (tre 8/8, sw8 9/9, sw16 17/17,
sw32 33/33) and optimizer-on bytes. Per-leg checks (all true, `evidence/compare.json`):
decoded `bytecode.sha256` == compiled runtime sha256; `artifact.sha256` == carrier hex
file sha256; every reported `bytecodeOffset` is a JUMPDEST (`5b`) and equals the
destination my independent disassembler parsed for that selector's compare leg
(per-selector equality; GT-node targets are never reported). Zero false positives
extend to optimizer-on bytes: non-compare PUSH4 immediates exist (`16ee4b79` metadata
@0x76c off-leg; `4e487b71` @0x363 on-leg; `ffffffff` masks in gau-off) and none was
reported. Representative envelope: `evidence/probes/tre-on200-Treasury.runtime.6.4.0.json`
(sha256 `b67bfa92…`); all 16 envelopes + `.err` under `evidence/probes/`.

**F6 — pivot lead-in, in bytes (tre-on200, 1233 B, `13fa3a62…`).**
`...57 5f3560e01c` + `80 63 75807250 11 61 004d 57` (pivot 75807250 GT → 0x4d) +
`80 63 75807250 14 61 01a2 57` (EQ leg) + … — i.e. the probe's decoded bytecode hex
shows the same structure it recovers (verified against `normalized_result.bytecode.hex`).

**F7 — size class above r1's probed band (partial discharge of an r1 Unknown).**
r1's Unknown "behavior at carrier sizes above the probed ~1.8–1.9 KB runtime class"
gains: sw32-off (3,040 B runtime, 33 selectors, pivot tree) and sw16-off (1,696 B)
probe K/K at 6.4.0 — so the extractor was exercised above the r1 band.

## 4. Delta statement (the round's shape finding, one paragraph)

r1 recorded two prologue classes (`5f3560e01c` PUSH0 / `60003560e01c` legacy) and only
linear dispatch chains (carriers had K=5,6). Round 3 adds, on measured bytes: the
PUSH0 class is invariant under the optimizer (26/26 carriers; legacy 0/26); a second
preamble offset class (13 for payable receive/fallback vs 25 for nonpayable-only);
and a **second topology class — pivot-GT sorted binary search at K ≥ 7** — which is
compiler-side (present optimizer-off) and extractor-transparent (K/K at K up to 33,
zero extras, JUMPDEST-equal offsets). The claim's honest-stop branches are therefore
**not taken**: "optimizer dispatch shape defeats the extractor" measured false; "the
probed prologue class differs from the r1 recorded classes" measured false (class-wise
— the delta is the preamble offset and the topology class, recorded here).

## 5. Evidence index (sha256-pinned; full manifest in `manifest.sha256.txt`)

| file | sha256 | content |
|---|---|---|
| `evidence/summary.json` | `d133e2ee…` | main compiles (rv2/tre/gau off+on200) |
| `evidence/fine-summary.json` | `9d6cdb85…` | fk5–8 (threshold) |
| `evidence/sweep-summary.json` | `5b1acf79…` | sw8/16/32 |
| `evidence/prologues.json` | `39cb1b11…` | 26-runtime class/topology/anchor record (my disassembler) |
| `evidence/compare.json` | `92687ed2…` | 16 probe legs vs ABI ground truth, all checks |
| `tools/prologues.py` | `c572e10d…` | class/topology analyzer (no third-party deps) |
| `tools/compare.py` | `aa757d7b…` | probe comparator |
| `tools/run-probes.sh` | `ecd779a1…` | probe runner (TMPDIR disk-backed) |
| `tools/compile.js` / `selectors.js` | `25a1fb6c…` / `92fbd245…` | compile harness / ABI→selector (js-sha3) |
| `tools/selector-recon.py` | `99c3c32d…` | EX-07 r1 tool (copied verbatim); `compare.py` takes its keccak + `selector()` from it |

Reproduce note: the scripts carry `/var/tmp/ex13` scratch paths (compile outputs,
probe envelopes); either re-create that scratch or adjust paths. The pinned inputs
and outputs are the copies in this seat dir (`src/`, `out/`, `evidence/`); a
third-party re-derivation is: compile `src/*.sol` with the receipted solc prefix,
run `tools/prologues.py -o … out/*.runtime.bin`, then `tools/compare.py` against the
envelopes in `evidence/probes/` (`TMPDIR` must be disk-backed for the probes).

## 6. Residuals / what was NOT measured (honest bound)

1. **Legacy class not re-materialized**: default evmVersion `osaka` yields PUSH0 in all
   arms; a `paris`/`shanghai`-targeted compile (or Vyper) would test the legacy path —
   not run this seat. The r1 Unknown "dispatcher prologues other than
   `5f3560e01c`/`60003560e01c`" remains open (only EX-08's synthetic `60043560e01c`
   control exists in-tree).
2. The K≤6 / K≥7 threshold is measured (8 carriers per side across two preamble
   classes and both optimizer settings) but **not source-cited** to the solc
   implementation; it is a measurement, not a mechanism claim.
3. Probes: rea-agents 6.4.0/6.7.0 only (evmole@0.9.3), no Vyper, no carrier above
   3,040 B runtime, no creation-blob legs (out of scope here).
4. Cross-seat corroboration (cited, not my own measurement): EX-04's independent
   VaultB (K=11, opt200 `aaf85cea…` / noopt `679678e9…`) reports the same EQ+GT
   binary-search dispatcher and K/K on both legs; VZ-1's `probe-rv2tokenopt` decodes
   to exactly my `ed6c8a76…` bytes (decoded-level identity across seats); EX-10's
   VaultB (`b24a0115…`) K/K at 6.4.0.

## 7. Before → after (chain c1 claim, this seat's leg)

- BEFORE (r1 record): Unknowns "optimizer-enabled dispatch shapes beyond the smoke
  compile" + "dispatcher prologues other than `5f3560e01c`/`60003560e01c`"; recorded
  dispatch evidence = linear chains on K=5/6 nonpayable carriers only.
- AFTER (this seat, commands in §1/§2, evidence §5): optimizer-enabled ERC-20 (K=5,
  `ed6c8a76…`) and optimizer-enabled non-ERC-20 carriers (payable receive/fallback
  K=8 `13fa3a62…`; library-bound K=6 `aa3dcc48…`) compiled on-host and probed K/K;
  class/topology matrix over 26 runtimes; threshold pinned; delta documented above.
- The C1 claim's acceptance flip (command A 82 → 83) is the landing step of other
  c1 seats; this seat wrote no corpus file (patch text proposed separately).

Scratch hygiene: all scratch under `/var/tmp/ex13`; no repo target modified; custody
paths only read (not needed by this seat's method); no git mutations.