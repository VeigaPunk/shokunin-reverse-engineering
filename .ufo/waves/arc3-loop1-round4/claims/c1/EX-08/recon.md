# recon.md — CarrierV 3-way reconciliation (planted vs probe vs independent extraction)

Seat EX-08 · chain c1 · role executor · wave `arc3-loop1-round4` · 2026-10-19 ·
repo `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Scratch `/var/tmp/ex08-r4/`
(never `/tmp`). No git mutations; custody paths never opened; no installs by this
seat (the venv was EX-02's authorized install, read-only use here). Write footprint:
this seat dir + `seats/EX-08.md` only.

**Task (seat line):** 3-way reconciliation: planted (EX-05) vs probe (EX-06/07) vs an
independent extraction from the runtime bytes (scan for the planted selector values as
PUSH4 immediates / chained-comparison parse); report K/K or the exact partial set.

**Verdict: K/K — 15/15 on every leg, zero missing, zero extra, zero false positives.**

## 0. Carriers, identities, re-derivation (rule #14)

| artifact | bytes | sha256 (re-derived first-hand) |
|---|---|---|
| `EX-04/src/CarrierV.vy` (source of the pinned bytes) | — | `f4f94727653508fdae2cbc12cb9fcc4de5c8c8bdb29b6bb90feabcab9bdb4b63` |
| `EX-04/out/runtime.hex` (probe subject, hex carrier) | 3,124 | `e0b1021c68f8de8c3f049f4242769548b6f8271a00986f2ab20f049f8748a192` |
| `EX-04/out/runtime.bin` (decoded runtime) | 1,562 | `57d6fd0ae0da001975a3f58ae72804757aa36267f6e373bf9f134ecc9791dae0` |
| `EX-04/out/creation.hex` | 3,274 | `34f52280d3cdc74008e1a2265f367f1d0817d93df6bbbb5cdce243903c3ccd92` |
| `EX-04/out/abi.json` | — | `c7902147808d31861bb8cf82837554c4700e675f85ef3b6010d82639cc17550b` |
| `EX-04/evidence/planted-K.json` (recorded 14:05:46.622Z, PRE-COMPILE) | — | `5161b95081076fc6fd8930b95a62de79c9f8318b61042b8352a778070b49e81b` |
| `EX-05/planted.txt` | — | `07b89ba77487e85a64fe803cb9a889a09c031a9b032883d6e6aefd69f7b0820e` |
| `EX-06/planted-K-CarrierV.json` (final) | — | `f9c4a1cbc1c6887bab5ba856a692ebf9599cf1ee3784408b6692bd2628799445` |
| `EX-07/legs/V-hex-6.4.0.json` ≡ `EX-05/probe-pins/my-probe-carrierV-hex-6.4.0.json` ≡ `EX-06/probe/CarrierV-hex-6.4.0.json` | — | `68415a3de767d58ee176bf6bfdd1ffb1719173041997a5d3fa49ce6f614a99ec` (byte-identical, same `ev_d1792f57…`) |

Full receipt: `identity-receipt.txt` (24 files). Compiler receipt (EX-04):
vyper `0.4.3+commit.bff19ea2`, venv `.ufo/waves/arc3-loop1-round4/tools/vyper-venv/`,
source sha re-derived = the file above; `EX-04/out/compile-receipt.txt`.

## 1. The three methods

- **PLANTED** — EX-04's `planted-K.json` (15 selectors, `recorded_utc`
  `2026-10-19T14:05:46.622429Z`, i.e. **before** the first compile finished at
  14:05:59Z and before any probe envelope existed). Cross-checked by EX-05's own
  two-implementation `planted.txt` (`js-sha3@0.8.0` + `node:crypto`, ALL AGREE) and
  by EX-06's source-derived file.
- **PROBE** — every available `inspect-evm-interface` envelope for the CarrierV
  runtime: EX-07's 8 V-legs (hex/raw × 6.4.0/6.5.0/6.7.0 + 2 scratch-path legs),
  EX-05's 3 pinned legs, EX-06's 6 legs (6.4.0/6.7.0 hex, 6.4.0 raw, rerun,
  0x-prefixed, alt-path) — **17 legs, all n=15**. (`EX-06/probe/…-upper-…` and
  `…-0xupper-…` also n=15 per EX-06's analysis; not re-parsed here.)
- **INDEPENDENT (this seat, probe never invoked)** — `recon.py`:
  - **M1** own linear-sweep disassembler + **Vyper XOR-chain parse**:
    `PUSH4 <sel> DUP2 XOR PUSH2 <next_test> JUMPI` (11-byte stride; on match the
    body falls through at +11). This is the shape the runtime actually uses.
  - **M2** planted-value PUSH4-immediate scan (each planted value searched as a raw
    PUSH4 immediate; all 15 found, each at exactly one site).
  - **M3** pure-Python keccak-256 over the source-declared signatures
    (`sigs-CarrierV.txt`, pre-registered at 14:05:50Z before any probe read) → 15/15
    selectors equal to the planted set (set-equality asserted in
    `evidence-recon-CarrierV-preprobe.txt`).
  - Harness self-test: `evidence-regression-r3.txt` (keccak vectors PASS).

## 2. Result — K/K 15/15 (all sources)

`evidence-recon-final.txt` (21 sources) and `evidence-recon-CarrierV.txt`:

```
M1_vyper_chain        n=15  MATCH  missing=[] extra=[]
M3_keccak_sigs        n=15  MATCH  missing=[] extra=[]
M2_planted_scan       n=15  MATCH  missing=[] extra=[]
PLANTED (EX-04)       n=15  MATCH  missing=[] extra=[]
PLANTED (EX-05 txt)   n=15  MATCH  missing=[] extra=[]
PLANTED (EX-06)       n=15  MATCH  missing=[] extra=[]
17 PROBE legs         n=15  MATCH  missing=[] extra=[]   (each: offsets equal, digest SAME, form OK)
VERDICT: ALL SOURCES AGREE (sets+offsets+pins)
```

Offsets: every probe leg's `bytecodeOffset` equals my M1 `body_offset`
(`push4_site + 11`) — full table in `evidence-offset-table.txt`, uniform
`off == body` 15/15 and `code[off-1] == 0x57` (JUMPI) 15/15. Digests: every leg's
decoded `normalized_result.bytecode.sha256` = `57d6fd0a…` (my sha over the decoded
bytes). Form: hex legs 2×bb ≤ artifact_bytes ≤ 2×bb+4; raw legs artifact == bytecode.

### 2.1 The dispatcher, reconstructed from the bytes (the round's new class)

```
5f 35 60 e0 1c            PUSH0 CALLDATALOAD PUSH1 0xe0 SHR
60 02 60 0d 82 06         PUSH1 2 PUSH1 13 DUP3 MOD       ; bucket = selector % 13
60 01 1b 61 06 00 01      PUSH1 1 SHL; PUSH2 0x0600 ADD  ; table base 0x600
60 1e 39                  PUSH1 30 CODECOPY               ; 13 x uint16 -> mem[0]
5f 51 56                  PUSH0 MLOAD JUMP
```

Table at 0x600 (13 entries): `029c 05e7 050b 0400 05ac 043f 053d 05e7 0590 0574
0382 05e7 0018` — every entry a JUMPDEST (checked). Per bucket, a chain of
`JUMPDEST PUSH4<sel> DUP2 XOR PUSH2<next> JUMPI <12-byte body>`; the last
`next_test` is 0x5e8 (1512) = the fallback (`__default__`) head. Walking all 13
buckets from their table entries reaches exactly the 15 planted selectors, no
more, no fewer (`evidence-bucket-walk-CarrierV.txt`, `ALL BUCKETS MATCH: True`).

**Offset-semantics class (recorded):** on this Vyper-shape carrier the probe's
`bytecodeOffset` is the **body entry** (fall-through after the match test), i.e.
`push4_site + 11`, and `code[offset]` is a body opcode (`0x60`/`0x34`), **not** a
JUMPDEST — 0/15 JUMPDEST, unlike the solc-convention carriers of r1/r3 where every
offset was a JUMPDEST. EX-06's analysis (§4) and EX-07's own `compare-legs.out`
(`V: byte@off-1==JUMPI 15/15`) measured the same reading independently. The r1/r3
"offsets land on JUMPDEST" reading is hereby **scoped to solc-convention
carriers**; the carrier-A control (PUSH1-jump-immediate class) remains the other
known exception (regression: `evidence-regression-r3.txt` last line).

### 2.2 Zero false positives / zero false negatives at byte level

- 21 PUSH4 immediates: 15 selectors + 6× `08c379a0` (`Error(string)` revert
  prefix — a string-constant, not a function). Nothing else. No `4e487b71`, no
  CBOR constant as PUSH4 (the trailer constant sits inside the CBOR blob, not as a
  PUSH4 in code — confirmed by the census: `push4_count 21, distinct 16`).
- The loose EQ/GT/LT scan produces **one** site on this carrier (`d0e30db0 @25`,
  from the body's `PUSH0 SLOAD PUSH1 01 EQ` paused-check being within the window) —
  excluded as a Vyper-chain site by construction (the chain parse is the stricter
  reading). Recorded so the exclusion is visible, not silent.

## 3. Bonus second Vyper carrier — StewardToken (EX-03, K=22)

Same methods on `EX-03/runtime.hex` (3,337 B, `1846469bd2abc625…`, table at
0x0cdd, 22 entries): my chain parse finds **22/22**, all slot-reachable
(`evidence-bucket-walk-StewardToken.txt`), matching the probe legs
`EX03-token-hex-{6.4.0,6.7.0}` (`ev_6b8a15c4…`/`ev_b07b8971…`) 22/22 with offsets
equal (`evidence-recon-StewardToken.txt`). **Notable cross-check:** EX-03's own
in-tree decoder (`evidence/dispatch-decode.txt`) recovered only 13/22 — its
walking strategy missed the multi-entry-bucket chains (e.g. slot 1's three-member
chain, slots 13/17/21). My parse + the probe independently confirm the full 22.
This is a peer-artifact finding for the round report, not a defect of the carrier.

## 4. Adjudications recorded (all measured)

1. **`__default__()` is not a selector-bearing function.** vyper's
   `method_identifiers` emits `__default__(): 0x89402a72`; the runtime contains
   **zero** occurrences of `89402a72` (searched as raw bytes and as PUSH4
   immediates). The fallback is dispatched by fallthrough (last `next_test` →
   0x5e8). Correct K = method_identifiers minus `__default__`. (Same finding,
   independently, in EX-06 §3.)
2. **vyper's `method_identifiers` strips leading zeros in the hex string** —
   `fee_of` prints `0xc751377` and `is_owner` `0x776076f` (7 chars). A raw string
   comparison against probe selectors would report 2 spurious mismatches; both are
   `0c751377`/`0776076f` after left-padding to 8 digits (my M3 derives the padded
   forms; sets equal 15/15).
3. **Creation code (VC-legs) reports n=0 — expected, not a defect.** The creation
   blob is a 20-byte constructor wrapper + the runtime at offset 20 (byte-identical
   round-trip) + a 55-byte CBOR trailer. The probe reads the creation head; the
   dispatcher only exists inside the embedded runtime. `evidence-creation-embedding.txt`.
4. **EX-06's superseded first-pass planted file (adjudicated).**
   `EX-06/evidence/planted-K-CarrierV-firstpass-superseded.json` parameterized the
   public-var getters (`owner(address)`, `total_deposits(uint256)`,
   `fee_bps(uint256)`, `paused(bool)`) → 4 selectors (`666e1b39`, `82e2e7ff`,
   `837150cf`, `e26f0bfe`) that occur **nowhere** in the bytes. Their final file
   fixed the parameterization; my parse matches it 15/15. The supersession was
   correct.
5. **Trap legs reproduce** (not this seat's runs; read-only): raw-on-hex-file
   (`EX-06/probe/CarrierV-trap-raw-on-hex.json`, `ev_64a69c28…`: 0 functions,
   decoded sha == the hex file's own sha `e0b1021c…`) — the r1/r3 parsed-empty
   trap class; hex-on-bin → typed refusal `invalid_input`/`invalid_format`.
6. **Envelope deltas at pins** (EX-07 `compare-legs.out` §6): `relationship_coverage`
   absent at 6.4.0, present (null) at 6.5.0/6.7.0; limitation list 6 vs 7 lines.
   Consistent with r3.

## 5. Attacks / refutations attempted (with verdicts)

| attack | method | verdict |
|---|---|---|
| A1 selector-byte mutation | flip low bit of `d0e30db0`'s last immediate byte in a scratch copy | chain set tracks the mutation exactly: `d0e30db0` gone, `d0e30db1` present, n stays 15 (`evidence-attacks-mutation.txt`) |
| A2 shape mutation | `XOR`(0x18)→`AND`(0x16) at one site in scratch | that site drops from the chain (14), selector absent — parser is shape-sensitive, not value-blind |
| A3 truncation | runtime cut to the 24-byte prologue | 0 chain sites, 0 PUSH4 — no phantom extraction from the prologue |
| A4 planted-value false-positive hunt | M2 scan for all 15 values | each found at exactly 1 site; no value appears elsewhere (incl. bodies) |
| A5 probe-trust inversion | all sets built from probe envelopes only, compared against my parse | equal on every leg (this is the 3-way result itself) |
| A6 id-domain confusion | same envelope bytes at 3 seats' paths | ids differ by path (`ev_d1792f57…` repo path vs `ev_7492bd99…` alt-path vs `ev_3be0282d…` 0x-prefix), payload identical — compare by decoded bytecode sha + payload, as r3 recorded |
| A7 r3 regression | full reconciler on 4 r3 solc carriers + carrier-A control after parser edits | all 4 still ALL-AGREE (JUMPDEST landing); carrier-A still flags the known 3 non-JUMPDEST landing (PUSH1-jump class) — no regression, anomaly detector alive |

## 6. Limitations (honest)

- The Vyper XOR-chain parse is validated on two carriers (15 and 22 functions) from
  one compiler version (vyper 0.4.3) on this host. Bucket-count 13 and 22 are both
  prime; behavior for other table sizes / chain layouts is unvisited.
- M2 is a value-scan (confirmation, not derivation): it cannot find selectors the
  planted set lacks. The derivation legs are M1 and M3.
- M3 derives from the source-declared signature list, which I authored from the .vy
  file before probing; the file is cited and hashed.
- I did not re-run the probe myself (probe legs are the other seats' sealed
  envelopes, read-only, hashed here); my independence is on the extraction side.
- The StewardToken reconciliation used EX-06's envelopes (not EX-03's own); EX-03's
  in-tree decoder finding (13/22) is reported as a peer finding without re-running
  their script.

## 7. Files (this seat)

- `recon.py` — extractor + reconciler (`keccak-test | extract | scan4 | keccak-sigs | reconciler`)
- `sigs-CarrierV.txt`, `sigs-CarrierV.selectors.txt`, `sigs-StewardToken.txt`,
  `planted-values-CarrierV.txt` — inputs
- `evidence-recon-final.txt`, `evidence-recon-CarrierV.txt`,
  `evidence-recon-CarrierV-preprobe.txt`, `evidence-recon-StewardToken.txt` — transcripts
- `evidence-vyper-dispatcher.txt`, `evidence-bucket-walk-CarrierV.txt`,
  `evidence-bucket-walk-StewardToken.txt`, `evidence-offset-table.txt`,
  `evidence-creation-embedding.txt`, `evidence-attacks-mutation.txt`,
  `evidence-regression-r3.txt`, `identity-receipt.txt`
