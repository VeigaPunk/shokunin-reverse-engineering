# SEAT SC-1 — chain c1, role scribe — arc3-loop1-round3 (2026-10-19)

**Task:** evidence-chain ledger (compiler check → compile → probe → reconcile →
controls → rerun, each with sha256). **Artifact:** `claims/c1/receipts/chain-ledger.draft.md`
+ byte-identical copy at `claims/c1/SC-1/receipts/chain-ledger.draft.md`.

## 1. Work performed (evidence pointers)

- **Draft ledger** (200→203 lines after the close-time tracker correction), 15,690 B,
  sha256 `634b52a4d0dc1f2b47506e19746e1ca5636864c9403fac17e3849d035b244b09`
  at **both** placements (`cmp` exit 0 between them; `sha256sum` quoted identical).
  Per the seat line the primary path is `claims/c1/receipts/`; the copy under the seat
  dir hedges the per-seat-artifact rule. Layout follows the r1 predecessor
  (`arc3-loop1-round1/claims/c1/receipts/chain-ledger.draft.md` `6d9427cc…`).
- **Reference rehearsal** — I ran the whole chain myself (not just compiled the ledger
  from other seats' outputs), scratch at `/var/tmp/sc1-r3`, landed copy at
  `claims/c1/SC-1/{src,out,tools,evidence}`:
  - S0 compiler check: r1 receipt re-verified — tarball sha256 `0e1a1ab6…` **re-derived**
    from the npm cache content file for registry integrity `ieUYdPDR…`/sha512
    `89e51874…`; prefix tree hashes equal the r1 ledger pins
    (`package.json` `b4205b08…`, `package-lock.json` `9f6dcab2…`, `solc.js` `188c3fdc…`,
    `soljson.js` `221d7a66…`); `solcjs --version` = `0.8.37+commit.f401782d.Emscripten.clang`.
    No install performed (frozen rule).
  - S1 compile: 4 legs, pinned solc — leg A = r1 `Rv2Token.sol` (`a4bc2d78…`),
    leg B = this seat's non-ERC-20 carrier `VaultCourt.sol` (`1af58859…`,
    payable receive/fallback + mixed mutability; planted K=10 vs A's K=5).
    **opt0 control MATCHES r1's pinned runtime `c1081a56…` byte-exactly**; opt200 deltas:
    A 1,943→978 B (`ed6c8a76…`), B 3,197→1,529 B (`66024ee3…`); compile re-run
    deterministic (`cmp` exit 0).
  - S2 probe: 13 legs (12 + rename) with disk-backed `TMPDIR`. K/K zero-extras on every
    clean leg: A opt200 5/5 @6.4.0 `ev_42cd9da2…` and @6.7.0 `ev_25238e85…`;
    B opt200 10/10 hex `ev_d1d0bc1c…` / raw `ev_e1aa1a50…` @6.4.0 and @6.7.0
    `ev_1d504cbc…`. Decoded `bytecode.sha256` = carrier file sha256 on every leg;
    `kind` stays `unknown`; B mutability `{payable:1, nonpayable:2, view:7}` (pure reads
    back as view — conservative inference, recorded).
  - S3 reconcile: own M1 (r1 EX-07 tool `99c3c32d…` byte-identical copy) + M2 keccak —
    5/5 and 10/10; A opt200 probe offsets `{89,129,147,166,206}` set-equal to M1 chain
    dests; all 10 B offsets land on `5b`; K=10 dispatcher is binary-search (strict chain
    parse 0, EQ parse 10) in **both** opt modes — count-driven, not optimizer-driven.
  - S4 controls: 8 controls, all behaved (see §4).
  - S5 rerun: identical invocation → byte-identical envelope (`cmp` exit 0), same id;
    renamed path → different id, same subject; different bytes → different ids.
  - Cross-wave pin: `EX-06/evidence/recheck-rv2token-hex-6.4.0.json` (`f2aec424…`) is
    byte-identical (`cmp` exit 0) to r1's `RV-2/probe-runtime-hex-6.4.0.json`.
  - Tree integrity: `claims/c1/SC-1/` copy verified **85/85** by
    `sha256sum -c evidence/MANIFEST.sha256.txt` (manifest `5c41ab22…`);
    command A run recorded into the same tree.
- **Command A (own run)** at HEAD `c07af80fcf3a60f9c6a0ca09b6e23fb5794d3311`:
  stored at `claims/c1/SC-1/evidence/command-A-before-c07af80f…json`.
- **Polls:** first poll 13:09Z (`seats/` = EX-22 only; EX-11 dir 0 files), close poll
  13:11:57Z (7 reports: CU-1, EX-04, EX-11, EX-22, EX-25, PL-1, SC-5; EX-12/VZ-1 still
  empty). The ledger's wave-tracker carried the 13:09 picture and was corrected at close
  (line 167-170) — both states are recorded in-file.

## 2. Proposed changes

**none.** No repo-surface change is proposed by this seat. Two tool-level findings are
recorded in the ledger's hygiene section (the `selector-recon.py` `scan` docstring vs
argv order mismatch; the `--format json` unwrapped-vs-wrapper envelope shapes) — both are
observations with evidence, no patch text drafted.

## 3. Before→after measurement for chain c1's claim (commands + outputs)

Claim under test: optimizer-enabled carrier + non-ERC-20 carrier recover **K/K** on the
pinned solc; landing step re-measures command A 82 → 83.

- **Before (measured, my run, command A recipe at `c07af80f`):**
  `python3 - "$REV" <<'PY' … PY` (SCORECARD §Measurement recipes A) →
  `{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score":
  10.0, "knowledge_files": 82, "mapped": 82, "missing": [], "revision":
  "c07af80f…", "rule_blocks": 14}` — equal to RV-4's `command-A-before.txt` (`9de3cbdd…`).
- **Chain-side after (measured now, independent of landing):**
  `npx -y rea-agents@6.4.0 inspect-evm-interface out/Rv2Token.opt200.runtime.hex hex --format json`
  → 5 functions, set-equal to planted K=5, `missing=[] extra=[]` (selector-recon `compare`
  output "MATCH"); same carrier @6.7.0 → MATCH. B: `…out/VaultCourt.opt200.runtime.hex hex`
  → 10 functions, MATCH; raw leg and @6.7.0 MATCH. The claim's K/K requirement for an
  optimizer-enabled carrier **and** a non-ERC-20-shaped carrier is satisfied by this
  rehearsal; the opt0 control proves the pipeline that produced those bytes is the r1 one.
- **After (command A 82 → 83): GAP — parent-side.** The knowledge entry and the map token
  had not landed at my close (knowledge-entry patch: GAP; `records-drafts/map-token-patch.md`
  `333ca590…` is a draft). I do not claim 83 — an unrun check has not passed.

## 4. Attacks/refutations attempted, with verdicts

1. **Tamper (single selector byte** `d0e30db0→d0e30db1` **@75)** → probe reports exactly the
   substituted selector, zero other drift; M1 reports same substitution; carrier digest
   changes (`d5e63b0c…` vs `66024ee3…`). **Verdict: refuted** — detection is byte-sensitive,
   not parroting a planted set.
2. **Dispatch-less blob** (`6001600101`) → 0 functions, exit 0. **Verdict: refuted**
   (no false-positive dispatch read).
3. **Creation-code shortcut** → 0 functions, parsed-and-empty. **Verdict: refuted**
   (creation code carries no runtime dispatch table; not an exclusion either).
4. **Encoding mismatch** (bin probed as hex) → typed refusal `invalid_input`/`invalid_request`,
   exit 1. **Verdict: holds** — fail-closed, no silent success.
5. **Rename-path identity attack** (same bytes, different path) → different id
   (`ev_8bc302e0…` vs `ev_42cd9da2…`), same subject digest `a07bef2e…`. **Verdict:**
   `ev_` ids are path-sensitive for this verb family — no universal content-addressing
   claim admissible (rule #14/#15); consistent with the r1 EX-05 renamed leg.
6. **Optimizer-as-extractor-defeat** (the claim's pre-written honest-stop branch) →
   **refuted** for K=5 and K=10 at both pins on this host; the genuine delta found is the
   K=10 binary-search dispatcher defeating M1's *strict chain* parse (EQ-site parse and
   the probe both read 10/10) — recorded as the round's delta, not a defect.
7. **Prologue-class delta branch** → not triggered: both legs sit in the r1-recorded
   `5f3560e01c` class (anchor @25 / @13).
8. **r1-pin drift** → opt0 recompile equals `c1081a56…`; EX-06 r3 recheck byte-identical
   to the r1 probe envelope. **Verdict: refuted** — the r1 pins stand.
9. **Planted-set-after-probe** → planted-K written 13:07:38.511Z, first probe file
   13:08:00.949Z (Δ 22.4 s, mtimes quoted). **Verdict: refuted.**
10. **Self-identity staleness on my own ledger (rule #14)** → the ledger's first revision
    cited an 84-file manifest and a stale seat-reports row; both were re-derived after
    revision (manifest 85 files `5c41ab22…`; ledger re-hashed to `634b52a4…` after the
    close-time correction; `cmp` byte-identity of both placements re-checked).
    **Verdict: discipline held; two revisions recorded.**

## 5. Blockers

None for this seat. Named gaps at close (not mine to close):
the landing chain (knowledge entry, map token after-state, command A 83, custody
post-pair) is parent-side and unlanded; `claims/c1/EX-12/` and `claims/c1/VZ-1/` were
0-file at 13:11:57Z; the reconcile/controls links carry independent producer artifacts
only partially (per the ledger's tracker, `partial` rows). The ledger is a draft snapshot;
the parent's integration-time ledger at the records commit is the arbiter for every GAP.