# SEAT CR-1 | CHAIN c1 | ROLE critic — arc3-loop1-round1 (2026-10-19)

Task (seat line): attacks — (1) raw/hex encoding confusion (could a seat run the
wrong form and misread output); (2) PUSH4 data bytes masquerading as selectors in
the reconciliation; (3) partial-recovery costume (landing with K'<K as a win).
Run what I can against the actual artifacts; verdicts here.

Repo HEAD at work: `e845c2b524ad2e59871e004c51a1386e192a74ab` (same revision
EX-07/EX-11/RV-2 recorded). Writes: this report +
`.ufo/waves/arc3-loop1-round1/claims/c1/CR-1/` only. No git mutations, no
custody-path writes, no other repo file touched. All scratch outside the repo.

## 1. Work performed (each bullet with an evidence pointer)

**Attack 1 — raw/hex encoding confusion (verdict: hazard CONFIRMED, detector
identified, not yet stated in any chain artifact).**

- Built hex/raw twin carriers and ran both forms and both wrong-form directions
  with the cached pins `rea-agents@6.4.0` (`~/.npm/_npx/dea9475797100b20`),
  `6.5.0` (`ad9a3fdbcad992c6`), `6.7.0` (`a1722018f28f9df2`). Evidence:
  `CR-1/evidence/out-{A-hex,B-hex,C-hex,Ahex-raw,Bhex-raw,Abin-hex,Bbin-hex,
  A-upper-hex,A-newline-hex,asciihex-hex}.json` + carriers in the same dir.
- **Dangerous direction (hex text fed as `raw`)**: exit 0, `ok:true`,
  `functions: []` — a clean-looking empty result for a run that never parsed
  the intended bytecode (`out-Ahex-raw.json`, `out-Bhex-raw.json`).
  EX-06's own trap reproduces it: `EX-06/evidence/trap-raw-of-hex.json`
  (exit 0, `ev_60062ad0…`, 0 functions).
- **Safe direction (binary fed as `hex`)**: typed refusal, exit 1,
  `invalid_request` / `invalid_input`, "Hex carrier must be valid UTF-8"
  (`out-Abin-hex.json`, `out-Bbin-hex.json`; EX-06 `trap-hex-on-bin.json`).
- **Silent mis-decode of ASCII-hex bytes**: `asciihex.bin` = raw bytes
  `6001600101` read as `hex` decodes to the 5-byte program with decoded
  `bytecode.sha256 b20db086a5f3815c1d7e0ce53ce19fdcfa3dca129c26ba30219fe3f8b5fe54fb`
  — byte-identical to r3-07's recorded decoded hash for its carrier 1
  (`corpus/knowledge/2026-10-13-r3-evm-interface.md:23-25`), so the tool is
  deterministic across waves and my harness is faithful.
- **Detector located** (the point EX-06's trap record does not state): the
  form signal lives only in `normalized_result` — `artifact.encoding` echoes
  the form; `raw` runs have `artifact.sha256 == bytecode.sha256` and equal byte
  counts; `hex` runs have `artifact.bytes ≈ 2×bytecode.bytes` (±1-2 bytes
  trailing newline) and differing digests. `raw_result` carries no form signal
  (keys = `["functions"]` only, `out-A-hex.json`), and
  `subject.digest.sha256` is the **carrier-file** hash in both forms
  (`36dc8246…` for `carrier-A.hex` in both the hex and raw runs), so comparing
  subject digests across forms cannot catch a wrong-form run.
- **Envelope trap**: with `--full-output` a FAILED analysis is wrapped
  `{"ok":true,"data":{"code":"execution_failure",…}}` (exit 1) — `ok:true` is
  not a success indicator (`fail-full.json` vs bare-object `fail-plain.json`,
  both exit 1; `ok-full.json` exit 0 for the same command with TMPDIR set).
- Uppercase hex and a trailing newline are accepted and decode identically
  (`out-A-upper-hex.json`, `out-A-newline-hex.json`; decoded sha `a92ba152…`);
  the `--encoding` flag-form rejection was not re-tested this round (neither
  did EX-12 claim to).

**Attack 2 — PUSH4 data bytes masquerading as selectors (verdict: REFUTED on
every carrier tested; one semantic boundary recorded).**

- Hand-assembled controls: carrier A (3 dispatched selectors + decoy PUSH4
  `deadbeef` + `ffffffff` never compared) → exactly the 3 dispatched selectors
  (`out-A-hex.json`); carrier B (PUSH4 selector-looking constants only, no
  dispatch) → `[]` (`out-B-hex.json`); carrier C (1 real + decoy `aabbccdd`)
  → exactly `2b7f0c93` (`out-C-hex.json`).
- Real solc bytecode (my own on-host compile, below): the ERC-165 body-level
  constant `0x80ac58cd` (present as a PUSH4 immediate in the
  `supportsInterface` body) is **not** reported; the metadata CBOR trailer
  contributes nothing (`out-solc-runtime.json`). Chain artifacts agree:
  Rv2Token's metadata constant `16ee4b79@1900` excluded (EX-07
  `m1-rv2token-runtime.json`; RV-2 report item 4/8), KdxToken
  "M1 non-dispatch PUSH4 constants: []" (`EX-07/reconciliation-run-all-legs.txt`).
- Boundary recorded: a body-level `EQ/JUMPI` on a constant is **not** reported
  (carrier E2, `out-E2-hex.json` → only `2b7f0c93`), but a calldata-selector
  `EQ/JUMPI` comparison is reported as `dispatch:"abi"` even when the constant
  is not in any ABI (carrier E3 → `deadbeef`, `out-E3-hex.json`). That is
  correct pattern-dispatch semantics, not a false positive — but it means K must
  be defined as "source-declared dispatcher-reachable selectors" and any extra
  recovered selector must be explained, not silently dropped. The two-sided
  check in EX-07's driver does exactly this (`missing`/`extra` both printed).

**Attack 3 — partial-recovery costume (verdict: BLOCKED at the chain's driver,
but the guard lives only in a seat dir and the committed transcript was not
reproducible — defect found and patched in text).**

- Doctored-leg battery against a `/var/tmp` replay copy of EX-07's committed
  driver (`sha256 c1be2731…`, the hash EX-07 cites): dropped selector (5/6),
  phantom selector (`deadbeef` extra), wrong-form leg (0 functions + file-sha
  digest), and correct-set/wrong-digest leg — **all four → `MISMATCH PRESENT`,
  exit 1** (`CR-1/evidence/replay/leg-*-out.txt`). RV-2's independent battery
  (their item 6) reached the same verdicts. Partial recovery cannot pass as a
  win at this driver.
- Wild-partial hunt: no partial recovery observed anywhere — my own contracts
  7/7, 20/20 (optimizer off and on), 64/64 (optimizer on, binary-search-shaped
  dispatcher, 3,079 B runtime); chain carriers 5/5 (Rv2Token), 6/6 (KdxToken),
  11/11 (Rv2Many).
- K provenance checked: EX-06's `planted-K.json` (mtime 07:02:50) precedes its
  probe legs (07:09:36); RV-2's `expected-selectors.txt` precedes its first
  probe by 42 s (07:00:46 vs 07:01:28). I independently re-derived KdxToken's
  K=6 from its ABI with my own js-sha3 path → set-equal to `planted-K.json`
  (6/6). The frozen claim's "K recorded pre-probe" holds on mtimes and content.
- **Defect found (reproducibility, not fabrication)**: running EX-07's
  documented command against the committed inputs yields `PROBE:kdx.hex.json
  n= 0 MISMATCH` ×4 and `VERDICT: MISMATCH PRESENT` (exit 1;
  `replay/baseline-run.txt`), because EX-05's legs are `{ok,data,meta}`-wrapped
  and `load_probe` never unwraps them. Feeding unwrapped copies with the same
  basenames reproduces the committed transcript **byte-identically**
  (`replay/unwrapped-all6.txt` sha256 `a356c3a9a73f21abb3aa62ec79ea64262f2b9cded28d10f9a70a91d9f50a3481`
  = the committed `reconciliation-run-all-legs.txt`). The recorded run used an
  unrecorded preprocessing step; the committed command alone does not reproduce
  the committed transcript.
- **Secondary defect (misleading pass prints)**: for an unreadable leg the
  driver prints `all offsets equal` (zero offsets ⇒ no mismatch) and silently
  skips its digest row. The aggregate verdict was safe (set-equality caught it),
  but the per-leg lines mislead. My patch marks such legs and flips the verdict.
- Patch text (`EX-07-reconcile-unwrap.patch.md`, applies `-p1` clean): unwrap,
  mark-unreadable, plus form invariants from attack 1. Verified behavior: with
  the patch the **documented** command on the **wrapped committed** inputs gives
  exit 0, `ALL SOURCES AGREE`, all six legs `FORM-OK` (`replay/patched-wrapped.txt`),
  while all four doctored legs still give `MISMATCH PRESENT` exit 1.

**Independent real-solc leg (my own compile; tooling receipt).**

- Installed npm `solc@0.8.37` (name `solc`, version
  `0.8.37+commit.f401782d.Emscripten.clang`; npm tarball
  `https://registry.npmjs.org/solc/-/solc-0.8.37.tgz`, integrity
  `sha512-ieUYdPDRGNKMsZpCfi9tY64Q+ASoL8tyhLuvf9cFiqDs+6ijlx8Wn2CRi0N71AlCvRx0V092rlUYu3b3PuxWlA==`;
  `soljson.js` sha256 `221d7a667378b5068d913e75fe092507e061363cd1d23b64c49ae82febabad4c`,
  9,237,611 B). Installed into an isolated prefix at `/dev/shm/cr1/solc-prefix`
  — a declared deviation from "under the wave dir": this seat may only write its
  report and `claims/c1/CR-1/`, so the install went to scratch; nothing was
  written to the repo. Sources and reproducers committed under
  `CR-1/evidence/` (`Cr1Sample.sol`, `compile2.js`, `selectors.json`,
  `solc-runtime.hex`, `solc-creation.hex`, `big64-sels.json`).
- Compiled `Cr1Sample` (7 ABI functions incl. `supportsInterface` with ERC-165
  interface-ID constants in the body; K=7, compiler `methodIdentifiers` +
  independent js-sha3 keccak cross-check on all 7) → probe recovered **7/7**,
  zero missing/extra, all `dispatch:"abi"` (`out-solc-runtime.json`). Also
  `Many` (K=20, optimizer off/on → 20/20 both) and `Big` (K=64, optimizer on,
  binary-search dispatcher → 64/64). Creation blob (1,536 B, runtime embedded
  verbatim at byte offset 28) → **0 functions** — the wrong-artifact sibling of
  attack 1: probing `evm.bytecode.object` instead of `evm.deployedBytecode.object`
  yields a clean-looking empty result (matches EX-06's and RV-2's creation-leg
  observations).
- Version drift: 6.4.0 / 6.5.0 / 6.7.0 on my solc runtime → identical selector
  set, offsets, mutability inferences, decoded sha `d18c5a1b…` (`evidence/drift-solc-*.json`).
  No drift across the cached pins; the `ev_` id itself is version-sensitive
  (RV-2 item 3).

**Cross-reads (convergent findings, checked against my own).**

- RV-1: from-spec keccak validated against two oracles; three planted sets MATCH.
- RV-2: K/K 6/6 confirmed; comparator-sensitivity battery; defect D1 (no-`--abi`
  spurious MISMATCH); id path-sensitivity; TMPDIR hazard.
- RV-4: map-token patch line-neutral PASS (190→190 lines, tokens 81→82, prior 81
  byte-identical).
- EX-11/SC-3: command A before = `{knowledge_files: 81, mapped: 81, missing: [],
  dangling: [], citation_resolved_rules: 13, rule_blocks: 13, coverage 10.0,
  depth 10.0}` at `e845c2b`; I verified independently that HEAD has exactly 81
  `corpus/knowledge/*.md` (82 paths incl. `.gitkeep`, which command A filters).
- EX-04 landed late and now carries `keccak-receipt.txt`, closing the gap RV-2
  flagged; I did not audit its contents (outside this seat's scope).
- CR-2 (the other c1 critic): F1 = the entry's `recheck:` line fails as written
  (TMPDIR) — **same finding as mine, independently measured**; F2/F3/F4/F5 are
  language/scope fixes in `CR-2/proposed-fixes.patch.md`. RV-3 grades the entry
  ACCEPT-WITH-FIXES with the same TMPDIR fix. VZ-1 compiled EX-03's late
  `token.sol` → 9/9 (`ev_92b7e2fc…`), closing RV-1's named gap.
- **Cross-seat adjudication (entry identity, CR-2 F2)**: CR-2 measured that
  applying EX-12's hunk A yields 8,598 B / 31 lines / `d8d85949…`. I
  re-applied hunk A extracted from the **current pinned** patch
  (`d662c195…`, the revision RV-3 graded) → exit 0 and exactly EX-12's claimed
  identity: 9,513 B / 32 lines / `a5119120ee6a6142b8be6e297e39c85e0464fb27761c6ee0e7cc7cf8a1d5e56b`
  (replay dir: `ex12-hunkA.diff` + `ex12-hunkA-applycheck.txt`; the apply tree
  was scratch and is removed). So F2 does not reproduce
  against the pinned revision — it measures an earlier one (VZ-1 documented the
  mid-wave patch revision). Parent should re-measure F2 against `d662c195…`
  before acting on it; EX-12's own identity claim is correct for the current
  revision.

## 2. Proposed changes

Patch-text artifacts (NOT applied; both verified to apply cleanly):

- `claims/c1/CR-1/EX-07-reconcile-unwrap.patch.md` — target
  `claims/c1/EX-07/reconcile.py`: unwrap `{ok,data,meta}` legs (makes the
  committed transcript reproducible from the committed command), mark
  unreadable legs instead of vacuously passing, add per-leg form invariants.
- `claims/c1/CR-1/knowledge-entry-additions.patch.md` (v2, deduped) — target the
  entry proposed by EX-12 (`corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md`,
  base pin EX-12 patch sha `d662c195…` = RV-3's graded revision): the raw-of-hex
  detection rule + `ok:true` envelope trap; my independent corroboration line
  (7/7, 20/20, 64/64 with masquerade controls). The `recheck:` TMPDIR fix is
  **deliberately not duplicated** — CR-2 F1 / RV-3 fix 1 own it; apply one of
  those instead (do not stack three variants).

No other changes proposed; no repo file modified by this seat.

## 3. Before→after measurement relevant to the chain's claim

Chain claim: real-solc bytecode leg replaces the synthetic-only r3-07 record.

- **Before** (r3-07, `corpus/knowledge/2026-10-13-r3-evm-interface.md:47-76`):
  81-byte hand-assembled dispatcher, 3/3 planted selectors, `inferred_arguments:""`.
  Command A at HEAD `e845c2b` (EX-11 artifact; my independent count): 81 `.md`
  knowledge files, mapped 81, missing [], dangling [], rules 13/13, 10.0/10.0.
- **After** (chain artifacts + my independent runs): real on-host solc 0.8.37
  runtime carriers recover K/K with zero missing/extra —
  Rv2Token 5/5 (`c1081a56…`, 1,943 B), KdxToken 6/6 (`9c40940e…`, 1,789 B; my
  own sha256 of the committed `.hex`/`.bin` reproduces both the file digest
  `69a15782…` and the decoded digest), Rv2Many 11/11; **my independent
  contracts 7/7, 20/20, 64/64** with argument tuples matching the compiled ABIs
  and `dispatch:"abi"` on all.
  Measured caveats a reader must keep: `inferred_state_mutability` is wrong on
  3/7 of my `Cr1Sample` functions (approve/totalSupply/allowance reported
  `pure` where the source is nonpayable/view) — the entry's "consistent with
  the compiled ABI" phrasing is safe only for `inferred_arguments`; `kind`
  stays `unknown` even on real solc output with the CBOR trailer
  (`a2646970…` present, `out-solc-runtime.json`).
  Command A after (82/82) is not yet measurable — the records commit has not
  landed at the time of writing; the map-token half is verified line-neutral by
  RV-4 (81→82 tokens, 190→190 lines, prior 81 byte-identical).

## 4. Attacks / refutations attempted (verdicts)

1. **raw/hex confusion — CONFIRMED HAZARD, detector identified.** Wrong-form
   runs are silently `exit 0 / ok:true / functions: []` (both my carriers and
   EX-06's trap); the only discriminator is `normalized_result`
   (`artifact.encoding`, byte-count relation, decoded vs artifact digest).
   `raw_result` and `subject.digest` cannot discriminate. Envelope trap:
   `ok:true` wraps `execution_failure` under `--full-output`. Detection rule is
   in no chain artifact yet → added to the entry via patch.
2. **PUSH4 masquerade — REFUTED on 7 carriers** (hand decoys, no-dispatch
   PUSH4-only, real solc metadata, ERC-165 body constant, body-level EQ/JUMPI
   decoy). Boundary recorded: calldata-EQ/JUMPI constants not in any ABI ARE
   reported (`deadbeef`) — correct semantics; reconciliation must stay
   two-sided.
3. **Partial-recovery costume — BLOCKED at EX-07's driver** (4 doctored legs
   all exit 1) **and absent in the wild** (7/7, 20/20, 64/64, 5/5, 6/6, 11/11).
   K provenance verified (pre-probe mtimes; independent ABI→keccak re-derivation
   of KdxToken's K=6). Defect: committed transcript not reproducible from the
   committed command (unrecorded unwrap step) + vacuous pass prints — patch
   supplied and behavior-verified.
4. **Wrong-artifact sibling (creation vs runtime) — CONFIRMED HAZARD.** Runtime
   embedded verbatim in creation code still yields 0 functions when the creation
   blob is probed (`out-solc-creation.json`; EX-06/RV-2 concur). A seat probing
   the wrong member of the solc output pair reads a clean-looking 0/K.
5. **Version-drift attack — PASS.** 6.4.0/6.5.0/6.7.0 identical payloads on the
   same carrier; only the `ev_` id differs (RV-2). Reconciliation across pins is
   safe for payloads, not for ids.
6. **`--encoding` flag form** — not re-tested (no claim depends on it).
7. **Entry identity claim vs CR-2 F2 — F2 does not reproduce against the pinned
   revision.** Re-applying EX-12's hunk A from the current `d662c195…` patch
   yields EX-12's claimed identity exactly (9,513 B / 32 lines / `a5119120…`,
   exit 0); F2's 8,598 B / 31 lines measurement corresponds to an earlier
   revision (VZ-1 recorded the mid-wave change). EX-12's claim stands for the
   pinned revision; re-measure F2 before acting on it.

## 5. Blockers

- **Fleet `/tmp` usrquota exhaustion (EDQUOT)** — affects every seat's scratch
  and, critically, the **probe worker itself**: without a TMPDIR redirect,
  `inspect-evm-interface` exits 1 with
  `{"code":"execution_failure",…,"phase":"worker","reason":"Unknown system
  error -122: … write"}`. Workaround verified: `TMPDIR=/dev/shm/<dir>` (or
  `/var/tmp/<dir>`) → exit 0 (`evidence/ok-full.json` vs `fail-full.json`).
  Convergent: EX-06 transcript step 6, RV-2 blockers, EX-15 casualty census.
  Any parent re-run of the canonical probe must set TMPDIR off `/tmp`; the
  recheck-line fix is CR-2 F1 / RV-3 fix 1 (my entry patch is deduped against
  theirs, not a third variant).
- Scratch deviations, declared: `/dev/shm/cr1` (kept — holds the solc prefix and
  cited evidence), `/var/tmp/cr1` (removed at close), `/tmp/cr1` (removed at
  close; the few files that landed there were superseded by the `/dev/shm`
  copies). No repo writes outside this seat's two allowed locations.
- No other blockers. Partial evidence is complete for all three attacks; the
  one leg I could not measure is the chain's own command-A-after (records commit
  not landed when this report was written — parent-side integration step).
