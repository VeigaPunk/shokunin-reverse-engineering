# SEAT RV-2 | CHAIN c1 | ROLE reviewer

Task (seat line): re-run EX-05's probe command myself; verify the K/K
selector-match claim, the dispatch field, and the envelope's evidence id;
compare against EX-07's reconciliation. Verdict in this report.

**VERDICT: K/K CONFIRMED (6/6, zero missing, zero extra). `dispatch:"abi"`
CONFIRMED (6/6 both legs). EVIDENCE ID CONFIRMED — both EX-05 primary ids and
both EX-06 ids reproduce byte-exactly under my independent re-run on the same
carrier paths. EX-07's reconciliation CONFIRMED (I ran their driver myself;
their offsets are JUMPDEST-verified; their cited sha256 pins check out) with
one tool defect found (below).**

Repo HEAD at work: `e845c2b524ad2e59871e004c51a1386e192a74ab` (same as EX-11's
recorded before-sha). All my artifacts: `.ufo/waves/arc3-loop1-round1/claims/c1/RV-2/`.
No repo writes outside that dir + this report; no git mutations; custody paths
read-only (not touched by this seat).

## 1. Work performed (each bullet with evidence pointer)

- **Independent carrier authored + compiled on-host** with the wave's solc
  0.8.37 prefix (read-only use): `claims/c1/RV-2/Rv2Token.sol` (sha256
  `a4bc2d784b249df6…`), 5 external functions; runtime 1943 B
  (`Rv2Token.runtime.hex` `d7f73058e2d9fb25…`, `Rv2Token.runtime.bin`
  `c1081a565869b503…`), creation 1971 B (`e6517fb7db569cad…`).
- **Expected K computed pre-probe** from the solc ABI via js-sha3 (solc's own
  dep tree): `expected-selectors.txt` (sha256 `85af43370d995e98…`), K=5.
- **Probe re-run myself** — `node <rea-agents>/scripts/rea.mjs
  inspect-evm-interface <file> <raw|hex> --format json` — on my carrier:
  hex@6.4.0 `ev_45849c8b11794ea0…` (`probe-runtime-hex-6.4.0.json`), raw@6.4.0
  `ev_3aacd424f092ccbf…`, hex@6.7.0 `ev_19d7d3cb29183523…`. All 5/5, all
  `dispatch:"abi"`.
- **EX-05's primary legs re-run on EX-05's exact paths**: my
  `rv2-verify-ex05-kdx-raw.json` / `rv2-verify-ex05-kdx-hex.json` are
  **field-identical to EX-05's recorded `.data` envelopes** (`diff` empty) and
  reproduce their evidence ids exactly: `ev_4dd5ea2051a41e8a…` and
  `ev_2a79dd2500416eab…`.
- **EX-06's legs re-run on EX-06's exact paths**: `rv2-rerun-kdx-hex-6.7.0.json`
  (sha256 `5188d59f70a560f7…`) and `rv2-rerun-kdx-raw-6.7.0.json`
  (`b374ec2798117c72…`) are **byte-identical** (diff empty; same sha256 as
  EX-07's `reconciliation.md` pins) to `claims/c1/EX-06/evidence/run-hex-6.7.0.json`
  / `run-raw-6.7.0.json`; ids `ev_56d89cb49a214f15…`, `ev_9259f412064538fc…`
  reproduce exactly.
- **K/K set check**: my re-run selectors vs EX-06's `planted-K.json` —
  `diff` empty, 6/6 (`kdx-planted.sorted` vs `kdx-probe.sorted`).
- **Digest binding check**: `subject.digest.sha256` = sha256 of the carrier
  file (`69a15782…` hex / `9c40940e…` raw); `normalized_result.bytecode.sha256`
  = sha256 of the decoded runtime (`9c40940e…`), bytes 1789 — all verified by
  `sha256sum` in my shell, not trusted from the envelope.
- **EX-07's reconciler executed by me**: `ex07-reconcile-rv2.txt` (sha256
  `560aea5ad11b7eb2…`) → `VERDICT: ALL SOURCES AGREE` across M1-chain,
  M1-EQ-sites, ABI, PLANTED, 3 probe legs, M2-keccak (8 sources).
- **EX-07's M1 offsets verified independently**: all six `dest` values
  (100/148/178/226/254/302) are byte `0x5b` JUMPDEST in the runtime; their
  `code_sha256` (`9c40940e…`) matches my `sha256sum` of the runtime bin.
- **EX-05 `evidence-ids.txt` consistency**: all 10 recorded ids match the ids
  inside their JSON files (10/10 MATCH, scripted check).
- **EX-07's cited pins checked**: `abi.json` `40ad881e…` = EX-05 `kdx-abi.json`
  = `/dev/shm/ex06/abi.json`; `planted-K.json` `063eb723…` as cited.

## 2. Proposed changes

- **None applied.** One patch-text proposal (not a repo target; reviewer
  finding): `claims/c1/RV-2/EX-07-reconcile-no-abi.patch.md` — guards the M2
  row in `claims/c1/EX-07/reconcile.py` so a run without `--abi` does not
  spuriously report MISMATCH (defect D1 below).

## 3. Before→after measurement (chain c1 claim)

BEFORE (r3-07 baseline, quoted from `corpus/knowledge/2026-10-13-r3-evm-interface.md:47-76`):
synthetic 81-byte hand-assembled dispatcher, 3/3 planted selectors,
`dispatch:"abi"`, `inferred_arguments:""`, `stateMutability:"pure"`.

AFTER (this seat, real solc 0.8.37 output; canonical target = KdxToken runtime
`9c40940e…`):

```
$ node rea.mjs inspect-evm-interface /dev/shm/ex05/kdx-runtime.bin raw --format json   # my re-run
evidence_id = ev_4dd5ea2051a41e8a952c571d068efde878e21a0f6296dd1ccecd91516b651a6a
              (== EX-05 recorded id; whole envelope field-identical to their .data)
functions   = 6/6: 095ea7b3 18160ddd 23b872dd 40c10f19 70a08231 a9059cbb
dispatch    = "abi" × 6
arguments   = address,uint256 / (empty) / address,address,uint256 / address,uint256 / address / address,uint256
stateMutability = nonpayable / view / nonpayable / nonpayable / view / nonpayable
bytecode sha256 = 9c40940ef88c0e82349af0b0bebb31fabf0b71bf68f5117478ac07d7e44e580e (1789 B)

$ diff <(jq -S . my-rerun.json) <(jq -S '.data' /dev/shm/ex05/kdx.raw.json)   # empty
$ diff my-rerun-ex06-hex.json EX-06/evidence/run-hex-6.7.0.json               # empty (byte-identical)
$ diff kdx-planted.sorted kdx-probe.sorted                                    # empty → K/K = 6/6
```

Contrast with r3-07 synthetic: `arguments`/`stateMutability` now carry real
signal (r3-07 had `""` and `"pure"` artifacts of stub bodies). This is the
frontier advance the C1 claim asserts, measured.

## 4. Attacks / refutations attempted (verdicts)

1. **False-positive attack (larger dispatch table, r3-07 named debt)** —
   11-function contract `attack/Rv2Many.sol` (K=11): probe recovered 11/11,
   `dispatch:"abi"`, zero extra. Verdict: PASS.
2. **Carrier-class attack** — probe on *creation* bytecode returns
   `functions: []` (my `Rv2Token.creation.hex`: 0; EX-02 smoke `.bin`: 0;
   EX-05's `kdx-creation.raw.json`: 0; `recon.out.json` 5-byte carrier: 0).
   Verdict: PASS with caveat — the claim's carrier MUST be runtime
   (deployed) bytecode; a creation-blob probe would read 0/K and is not a
   probe failure.
3. **Version-drift attack** — same carrier, 6.4.0 vs 6.7.0: same selector set,
   same dispatch, same bytecode sha; but **different evidence id**
   (`ev_45849c8b…` vs `ev_19d7d3cb…`). Verdict: id must be re-derived with
   the SAME rea version to be comparable (see 5).
4. **Id determinism attack** — 3× rerun same version+path: byte-identical
   including id; renamed copy of identical bytes → different id
   (`ev_39f5fbfd…`); cwd change → same id; `--format json` (flat) vs wrapped
   output → same id. Verdict: id is deterministic per (rea version, absolute
   carrier path, encoding) — reproducible, not random; cite it with the
   version+path.
5. **Path-sensitivity in EX-05's own twins** — their rerun id == original id
   (determinism), their renamed-file id differs (path binding). Matches my
   independent result. Verdict: PASS.
6. **Comparator-sensitivity attack on EX-07's driver** — (a) probe json with
   one selector dropped → `MISMATCH missing=['a9059cbb']`, exit 1; (b) digest
   pin flipped to `deadbeef…` → `DIFFER` + `MISMATCH PRESENT`, exit 1;
   (c) planted list + bogus `deadbeef` → `extra=['deadbeef']`, exit 1.
   Verdict: PASS (detects all three tampers).
7. **Defect D1 found in EX-07's `reconcile.py`** — run WITHOUT `--abi` on a
   clean carrier: the M2 row is unconditionally emitted as an empty set and
   compared to the M1 reference →
   `M2_keccak_scan n=0 MISMATCH missing=[…5 sels…]`, `VERDICT: MISMATCH
   PRESENT`, exit 1. Repro: `python3 claims/c1/EX-07/reconcile.py --code
   claims/c1/RV-2/Rv2Token.runtime.hex hex --planted
   claims/c1/RV-2/expected-selectors.txt --probe
   claims/c1/RV-2/probe-runtime-hex-6.4.0.json` → exit 1 despite a clean
   carrier (their own canonical run passed `--abi`, so their recorded verdict
   is unaffected). Patch text: `EX-07-reconcile-no-abi.patch.md`.
8. **K/K refutation attempt via independent tooling** — EX-07's M1/M2 on my
   carrier and on the KdxToken carrier reproduce the probe's selector set and
   JUMPDEST destinations exactly; M2's first-occurrence offsets are the PUSH4
   immediate bytes (32/43/54/65/76/87 = site+1), not the JUMPDESTs — no
   confusion between the two offset families. Verdict: no mismatch exists.
9. **`bytecodeOffset` semantics** — all 16 offsets across my carriers are
   `0x5b` JUMPDEST bytes (r4 errata `2026-10-13-r3-evm-interface.md:149-155`
   confirmed independently).
10. **Bookkeeping check on EX-07's cited tool hash** — their report cites
   `reconcile.py` sha `c1be2731…`; the file on disk (mtime 07:06:48, after
   their report) is `647395a0f8a2d00e73f02c242186a3b17f0396713b3a00d2caf0fca82e87b9a6`.
   I re-ran their exact reproduce command with the current revision against
   their local carrier copies → `VERDICT: ALL SOURCES AGREE`, identical to the
   recorded `reconciliation-run-local-copies.txt` verdict. Verdict: the
   recorded result still reproduces; the cited hash names a pre-final
   revision (cosmetic, worth a parent-side hash refresh, not a measurement
   defect).

## 5. Blockers

- **EX-05 seat report LANDED at 10:09Z (poll check 7)** — read and
  cross-checked after my first draft. Their headline numbers match my
  independent reproduction exactly (K=6/6, `dispatch:"abi"` ×6, ev
  `ev_4dd5ea20…` / `ev_2a79dd25…`); their attacks 1-6 agree with mine where
  they overlap (creation-blob 0 functions, version stability, id
  path-sensitivity). Two notes for the parent: (i) their seat line pointed at
  **EX-04's bytecode, which never landed** — they substituted EX-06's
  `KdxToken` recompiled byte-identically (`9c40940e…`), a documented
  divergence (`claims/c1/EX-05/README.md`); EX-04's owed artifact
  (`keccak-receipt.txt`) is a chain-level gap they name. (ii) Their canonical
  command carried `--full-output`; my re-runs used `--format json` **without**
  it and produced the identical evidence ids and envelopes (their
  `{ok,data,meta}` wrapper vs my flat envelope — id independent of output
  wrapper).
- **`/tmp` tmpfs per-user quota is exhausted fleet-wide** (EDQUOT on 1-byte
  writes; EX-15 casualty census lists 63+ seat scratch losses). This is not
  cosmetic: **the probe worker itself fails without a TMPDIR redirect** —
  `npx -y rea-agents@6.4.0 inspect-evm-interface <file> hex` without TMPDIR
  exits 1 with `{"code":"execution_failure",…"reason":"Unknown system error
  -122: Unknown system error -122, write"}` (EDQUOT inside the EVMole
  worker). With `TMPDIR=/var/tmp/rv2` (or `/dev/shm/...` as EX-05/EX-06 used)
  the same command exits 0. Any parent re-run of the canonical probe MUST set
  TMPDIR to a non-/tmp path. My scratch lived in `/var/tmp/rv2` (declared
  deviation from "scratch under /tmp", which is unwritable) and was removed
  at close (`ls /var/tmp/rv2` → not found); my earlier `/tmp/rv2-c1` residue
  was removed earlier (confirmed gone).
- No other blockers. My seat is complete; all evidence is in
  `claims/c1/RV-2/` and reproducible from the commands above.
