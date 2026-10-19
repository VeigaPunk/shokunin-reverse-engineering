# Proposed change (PATCH TEXT — NOT APPLIED) — EX-12 / chain c1

Seat: EX-12 (c1 executor). Task: draft the corpus knowledge entry for the C1 claim
("real solc-compiled bytecode leg") as patch text — RESULT-class per `corpus/QUALITY.md`,
modeled on the 2026-10-16 entries. Targets: new file
`corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md` + the line-neutral coverage-map
token at `corpus/README.md:38`. Verified to apply to HEAD
`e845c2b524ad2e59871e004c51a1386e192a74ab`; scratch-tree command A after apply:
`{"knowledge_files": 82, "mapped": 82, "missing": [], "dangling": []}`.

## Patch text

Applies with `patch -p1` **or** `git apply -p1` from the repo root (both exit 0, verified).
Hunk B is byte-identical to EX-13's rehearsal (`claims/c1/EX-13/_scratch/README.patched`;
`git diff --no-index` exit 0) — **land it once, not twice**; EX-13 owns the map-token
artifact, this hunk is carried here only for self-containedness. No `## Knowledge` table
row is proposed: the frozen claim specifies one line-neutral map token, and the arc2
precedent (r6/r7/r8) landed the map token only.

```diff
diff --git a/corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md b/corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md
new file mode 100644
index 0000000..d3ef6dd
--- /dev/null
+++ b/corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md
@@ -0,0 +1,32 @@
+<!-- corpus entry — kaidoku-shokunin arc3-loop1-round1 (2026-10-19). Staging: .ufo/waves/arc3-loop1-round1/claims/c1/{RV-2,EX-06,EX-07,RV-1,EX-02}. The real-solc EVM leg r3-07 left as frontier; RESULT-class, no Core promotion. -->
+
+# inspect-evm-interface on real solc bytecode — selectors recovered K/K on on-host 0.8.37 compiles (5/5, 6/6, 11/11)
+
+source: `.ufo/waves/arc3-loop1-round1/claims/c1/RV-2/probe-runtime-hex-6.4.0.json`, `probe-runtime-raw-6.4.0.json`, `probe-runtime-hex-6.7.0.json`, `probe-rerun-a.json`, `probe-rerun-b.json`, `probe-cwd-root-6.4.0.json`, `probe-creation-hex-6.4.0.json`, `probe-EX02-smoke-bin-6.4.0.json`, `.ufo/waves/arc3-loop1-round1/claims/c1/RV-2/attack/probe-many.json`, `.ufo/waves/arc3-loop1-round1/claims/c1/RV-2/attack/expected-many.txt`, `expected-selectors.txt`; `.ufo/waves/arc3-loop1-round1/claims/c1/EX-06/evidence/run-hex-6.7.0.json`, `run-raw-6.7.0.json`, `planted-K.json`, `transcript.txt`; `.ufo/waves/arc3-loop1-round1/claims/c1/EX-07/reconciliation-run.txt`; `.ufo/waves/arc3-loop1-round1/claims/c1/RV-1/validation-sha3-and-vectors.txt`; `.ufo/waves/arc3-loop1-round1/claims/c1/EX-02/install-receipt.txt`
+verified-at: 2026-10-19
+recheck: `cd /tmp && npx -y rea-agents@6.4.0 inspect-evm-interface /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round1/claims/c1/RV-2/Rv2Token.runtime.hex hex --format json` → expect 5 functions, all `dispatch:"abi"`, decoded `bytecode.sha256 c1081a56…`; the sealed id `ev_45849c8b…` was re-derived across same-request reruns — the `ev_` id domain for this verb family was not measured, so if a fresh run mints a different id, compare by `subject.digest.sha256` + function payload instead.
+
+REA pin: `rea-agents@6.4.0` (Rv2Token hex + raw; Rv2Many; both creation legs) and `rea-agents@6.7.0` (Rv2Token hex re-derivation; KdxToken hex + raw). Provider `evmole-interface` / "REA EVM interface adapter", EVMole `evmole@0.9.3` (WASM-bundled). Claim source: the sealed probe envelopes, not skill text.
+
+Carriers — all compiled on this host with solc `0.8.37+commit.f401782d` (wave-isolated npm prefix `.ufo/waves/arc3-loop1-round1/tools/solc-prefix/`; install receipt: tarball sha256 `0e1a1ab6…575a51`, tree byte-identical to the pre-existing ambient install) from the retained sources at the pinned sha256s, via solc standard-JSON input (Rv2Token `solc-input.json`, optimizer disabled; KdxToken `compile.js`, `evm.deployedBytecode.object`) and `solcjs --bin --abi --optimize` (Smoke); byte-exactness is claimed for these pinned bytes only:
+- `Rv2Token` (ERC-20 shape, 5 external functions, optimizer disabled): source `a4bc2d78…`; runtime 1,943 B `c1081a56…`; hex carrier 3,886 B `d7f73058…`; creation blob 3,942 B `e6517fb7…`; ABI `e9a58020…`. Planted set K=5 recorded pre-probe (`expected-selectors.txt` written 42 s before the first probe envelope).
+- `Rv2Many` (attack carrier, 11 selectors): runtime hex `6a1c07d7…`; planted set K=11 (`.ufo/waves/arc3-loop1-round1/claims/c1/RV-2/attack/expected-many.txt`).
+- `KdxToken` (ERC-20 + mint, 6 external functions): source `c2980385…`; runtime 1,789 B `9c40940e…`; hex carrier 3,579 B `69a15782…`; planted set K=6 keccak-anchored (`planted-K.json`; transcript step 2 precedes the probe runs).
+- `Smoke` (install smoke leg, EX-02): solcjs `--bin` output 685 B `530efc7b…` — probed once (creation-code bytes).
+
+- **Observation (RESULT — Rv2Token hex @ 6.4.0):** Evidence `ev_45849c8b…`; `normalized_result.functions` (count = array length) = 5, set-equal to the planted K=5 (`095ea7b3`, `18160ddd`, `23b872dd`, `70a08231`, `a9059cbb`), zero missing / zero extra, `dispatch:"abi"` on all five. `inferred_arguments`/`inferred_state_mutability` are populated and consistent with the compiled ABI (`Rv2Token.abi.json`); offsets 89/137/167/215/263 are dispatch-target JUMPDESTs (r3 erratum, `corpus/knowledge/2026-10-13-r3-evm-interface.md:149-155`); decoded `bytecode.sha256 c1081a56…` = the runtime bytes; the bytecode's sole non-dispatch PUSH4 constant (`16ee4b79` @1900) was not reported — zero false positives (EX-07 `m1-rv2token-runtime.json`). r3-07's "no real signal for argument/mutability inference" frontier closes for this carrier.
+- **Observation (delta vs r3-07 — this entry's core):** where the r3 synthetic stub bodies returned `inferred_state_mutability:"pure"` for every selector and `inferred_arguments:""` (`corpus/knowledge/2026-10-13-r3-evm-interface.md:59-70`), this real carrier returns per-function mutability (`view` ×2, `nonpayable` ×3) and argument tuples — signal that exists only because the bytes are compiler output, not a hand-assembled stub. This is a fresh real-bytecode leg, not a re-run of r3.
+- **Observation (RESULT — Rv2Token raw @ 6.4.0):** `ev_3aacd424…` — identical function payload and offsets; on the raw path the carrier sha256 equals the decoded bytecode sha256 (`raw` ≡ decode).
+- **Observation (RESULT — Rv2Token hex @ 6.7.0):** `ev_19d7d3cb…` — same 5/5; 6.7.0 additionally reports terminal CBOR metadata as an independently decoded candidate (its own `limitations` say that is not proof of Solidity origin or deployment).
+- **Observation (id re-derivation):** same-request reruns a/b and a repo-root-CWD run re-derive `ev_45849c8b…`; the 6.7.0 rerun re-derives `ev_19d7d3cb…`; different carrier bytes yield different ids. The `ev_` id's full domain for `inspect_evm_interface` was not measured — no content-addressed identity claim is made (`corpus/QUALITY.md:24-25`).
+- **Observation (RESULT — Rv2Many @ 6.4.0):** `ev_d0d0b054…` — 11/11 planted selectors, zero false positives; no truncation at 11.
+- **Observation (RESULT — KdxToken @ 6.7.0):** `ev_56d89cb4…` (hex) and `ev_9259f412…` (raw) — 6/6, set-equal to the planted set; hex-shape variants (no trailing newline, `0x` prefix, uppercase) all decode to the same bytecode sha256 `9c40940e…`; every reported offset lands on byte `5b` (JUMPDEST) — the r4 offset-semantics erratum re-confirmed on real bytecode.
+- **Observation (creation code — parsed-and-empty, not excluded):** `Rv2Token.creation.hex` @6.4.0 `ev_c80379e1…` → 0 functions, `bytecode.kind:"unknown"`; `Smoke_sol_Smoke.bin` @6.4.0 `ev_f875e21e…` → 0 functions. Creation blobs carry no runtime dispatch table; these are parsed-and-empty results (`corpus/QUALITY.md:21`), not inventory exclusions.
+- **Observation (input-shape traps, KdxToken):** encoding is a positional argument (`<path> <raw|hex>` — the r3 quirk, `corpus/knowledge/2026-10-13-r3-evm-interface.md:93-96`; the `--encoding` flag-form rejection was not re-tested this round); interior whitespace / odd length / wrapped lines / CRLF → typed `invalid_request` exit 1; a raw-encoded copy of hex text decodes the file's bytes as code (exit 0, `ev_60062ad0…`, different bytecode digest); a temp-dir EDQUOT failure → typed `execution_failure` exit 1 — fail-closed, no silent success.
+- **Observation (independent recon):** EX-07's linear-sweep disassembler + pure-Python keccak reproduce the same selector sets and every probe offset for both carriers, all sources agree (`reconciliation-run.txt`: "VERDICT: ALL SOURCES AGREE"); RV-1 validates the keccak reference against two independent oracles and the ERC-20 vector table.
+- **Inference:** the recovered selectors are the compiled dispatch tables of the pinned carriers; the argument/mutability strings are upstream inferences consistent with the compiled ABIs — not verified ABI signatures, names, or source identity.
+- **Unknowns:** Vyper and other solc versions; optimizer-enabled dispatch shapes beyond the smoke compile; dispatcher prologues other than `5f3560e01c`/`60003560e01c`; the `ev_` id domain for this verb family; whether 6.7.0's CBOR metadata decode generalizes; behavior at carrier sizes above the probed ~1.8-1.9 KB runtime class; deployment/chain identity (never claimed by the tool).
+- **Limitations (tool-reported, every leg):** worker limits 256 MiB JS heap / 3 GiB address space / 30 s deadline / 16 MiB file cap; upstream-inference caveat; `kind`/hardfork/deployment-authenticity `unknown`; SHA-256 is not the Ethereum Keccak code hash; no runtime execution, chain/RPC lookup, or network request. Only the carriers and pins named above were probed.
+- **Scope:** RESULT-class exercise only — no Core promotion, no availability→holding claim. Family-scoped to solc-0.8.37-compiled runtime carriers compiled on this host this round, under the two REA pins named.
+
+Sources: `.ufo/waves/arc3-loop1-round1/claims/c1/RV-2/probe-runtime-hex-6.4.0.json` + `probe-runtime-raw-6.4.0.json` + `probe-runtime-hex-6.7.0.json` + `probe-rerun-a.json` + `probe-rerun-b.json` + `probe-cwd-root-6.4.0.json` + `probe-creation-hex-6.4.0.json` + `probe-EX02-smoke-bin-6.4.0.json` + `.ufo/waves/arc3-loop1-round1/claims/c1/RV-2/attack/probe-many.json` + `.ufo/waves/arc3-loop1-round1/claims/c1/RV-2/attack/expected-many.txt` + `expected-selectors.txt`; `.ufo/waves/arc3-loop1-round1/claims/c1/EX-06/evidence/run-hex-6.7.0.json` + `run-raw-6.7.0.json` + `planted-K.json` + `transcript.txt`; `.ufo/waves/arc3-loop1-round1/claims/c1/EX-07/reconciliation-run.txt` + `m1-rv2token-runtime.json` + `m1-kdxtoken-runtime.json` + `m2-kdxtoken-keccak.json`; `.ufo/waves/arc3-loop1-round1/claims/c1/RV-1/validation-sha3-and-vectors.txt`; `.ufo/waves/arc3-loop1-round1/claims/c1/EX-02/install-receipt.txt` + `.ufo/waves/arc3-loop1-round1/claims/c1/EX-02/smoke/out/Smoke_sol_Smoke.bin`.
--- a/corpus/README.md
+++ b/corpus/README.md
@@ -35,7 +35,7 @@
 | `knowledge/2026-10-13-r4-10-real-version-pair` | full compare pipeline at 41-43MB (`op` 2.34.1→2.40.0, ~6-7min per verb — every verb re-imports fresh); CLI `rea compare` caps at `status:unknown` vs domain `compareBundles`+`record_pairs` → `status:changed`; Go bump (1.25.7→1.26.8) collapses symbol recovery 33,060→11,595 procs — pair by ELF role/address, not symbol name | `rea analyze`/`search`/`function`/`compare` + domain `compareBundles`/`compareFunctions` |
 | Runtime observation | `2026-10-13-r3-runtime-observation` | held — CDP enumerate/inspect on self-launched chromium + electron; scenario capture ran |
 | `knowledge/2026-10-13-r4-08-observe-verbs` | observe/reconcile legs closed: `observe-web-session` (self-scopes origins), `observe-web-execution` (perturbing counter-reset coverage, no self-scope), `observe-javascript-runtime` + `reconcile-javascript-runtime` held end-to-end; `capture-electron-scenario` typed refusal (`cleanup_incomplete`); node `--inspect` targets need a real file | live CDP (:9222 chromium) + V8-inspector (:9229 node) probes |
-| EVM | `2026-10-13-r3-evm-interface` | held — EVMole selectors recovered from synthetic dispatcher; positional encoding quirk |
+| EVM | `2026-10-13-r3-evm-interface`, `2026-10-19-arc3-r1-evm-real-solc` | held — EVMole selectors recovered from synthetic dispatcher; positional encoding quirk |
 | Host anomaly triage | `2026-10-13-r2-jq-shadow-verdict`, `2026-10-13-r3-jq-provenance` | resolved — byte-identical upstream + provenance traced to kimi swarm bootstrap 2026-10-03 |
 | Synthesized carriers | `2026-10-13-r3-keyed-archive-carriers` | held — keyed-archive/interface-builder/dylib-trace all work on Linux synths; recipes recorded |
 | Evidence model | `2026-10-13-r2-evidence-bundle-schema` | held — snapshot envelope vs inner bundle schema, content-addressed ev_ ids |
```

## Evidence map — every filled field and its source

| entry field | value (abridged) | source |
|---|---|---|
| primary evidence id | `ev_45849c8b…` | `claims/c1/RV-2/probe-runtime-hex-6.4.0.json` |
| raw twin id | `ev_3aacd424…` | `claims/c1/RV-2/probe-runtime-raw-6.4.0.json` |
| 6.7.0 re-derivation id | `ev_19d7d3cb…` | `claims/c1/RV-2/probe-runtime-hex-6.7.0.json` |
| Rv2Many id (attack) | `ev_d0d0b054…` | `claims/c1/RV-2/attack/probe-many.json` |
| creation-leg ids | `ev_c80379e1…`, `ev_f875e21e…` | `claims/c1/RV-2/probe-creation-hex-6.4.0.json`, `probe-EX02-smoke-bin-6.4.0.json` |
| KdxToken ids | `ev_56d89cb4…`, `ev_9259f412…` | `claims/c1/EX-06/evidence/run-hex-6.7.0.json`, `run-raw-6.7.0.json` |
| raw-of-hex trap id | `ev_60062ad0…` | `claims/c1/EX-06/evidence/transcript.txt` step 5 |
| carrier sha256s | Rv2Token runtime `c1081a56…`; Rv2Token hex `d7f73058…`; creation `e6517fb7…`; KdxToken runtime `9c40940e…`; hex `69a15782…`; Rv2Many hex `6a1c07d7…`; Smoke `.bin` `530efc7b…` | `sha256sum` outputs; `claims/c1/receipts/MANIFEST.draft.txt:33-36`; `EX-06/evidence/transcript.txt` |
| solc pin | `0.8.37+commit.f401782d`, tarball sha256 `0e1a1ab6…575a51` | `claims/c1/EX-02/install-receipt.txt` §1–§5 |
| pre-probe planted sets | K=5 / K=11 / K=6 | `RV-2/expected-selectors.txt` (mtime 42 s before the first probe envelope), `RV-2/attack/expected-many.txt`, `EX-06/evidence/planted-K.json` |
| id re-derivation | reruns a/b + repo-root CWD, same id | `RV-2/probe-rerun-a.json`, `probe-rerun-b.json`, `probe-cwd-root-6.4.0.json` |
| independent recon | all sources agree; offsets 89/137/167/215/263 = parsed JUMPDEST dests | `EX-07/reconciliation-run.txt`, `m1-rv2token-runtime.json`, `m1-kdxtoken-runtime.json`, `m2-kdxtoken-keccak.json`, `RV-1/validation-sha3-and-vectors.txt` |

## Verification performed (commands + results)

1. **Patch application.** Pristine scratch tree (`/var/tmp/ex12-apply-test`, README from
   `git show HEAD:corpus/README.md` + the 81 knowledge stems): `git apply --check -p1
   combined.patch` → exit 0; `patch -p1` → exit 0, both files created/patched.
2. **After-state.** Tree recipe-A on the patched tree →
   `{"knowledge_files": 82, "mapped": 82, "missing": [], "dangling": []}`.
3. **Before-state (independent reproduction of EX-11's landed artifact).** Tree recipe-A
   on the pristine tree → 81/81, missing [], dangling [] — matches
   `claims/c1/EX-11/command-A-before.txt` on the counted fields.
4. **Entry file identity.** `corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md`:
   9,513 bytes, 32 lines, sha256
   `a5119120ee6a6142b8be6e297e39c85e0464fb27761c6ee0e7cc7cf8a1d5e56b`.
5. **Set-equality (planted vs probe).** `normalized_result.functions[].selector` sets:
   Rv2Token hex/raw/6.7.0 = 5/5 (zero missing, zero extra); Rv2Many 11/11; KdxToken
   hex/raw = 6/6; creation legs 0 functions, `bytecode.kind:"unknown"` (parsed-and-empty).
6. **Offset cross-check.** Probe offsets (89/137/167/215/263) equal EX-07's independently
   parsed dispatch-chain `dest` values (`m1-rv2token-runtime.json`), 5/5.
7. **Name convergence.** Patched README line is byte-identical to EX-13's
   `README.patched` (`git diff --no-index` exit 0).
8. **Language scan.** `grep -iE '\bheld\b|\bworks\b|\bsupported\b|\bavailable\b|\bcapability\b|\bproves\b|\bproven\b'`
   on the new file → no matches. The word "held" inside Hunk B is pre-existing row text,
   untouched by the edit. The entry carries an explicit scope line: RESULT-class, no Core
   promotion, no availability→holding claim, family-scoped to the probed family.
9. **Scratch.** `/tmp` is quota-blocked this wave (EDQUOT reproduces inside the probe's
   own runs); scratch used `/var/tmp/ex12-*` and was removed after use.
10. **Citation resolvability (self-attack).** Every path-like backticked citation in the
    entry resolves from the repo root — 11/11 after fixes; the check caught four relative
    paths in the first draft and two more `attack/…` paths in the Sources line, all
    prefixed to full repo-relative form.
11. **Evidence resolvability (self-attack).** All 9 `ev_…` id prefixes and all 11 sha256
    prefixes in the entry resolve inside the wave's landed artifacts (mechanical scan over
    `.ufo/waves/arc3-loop1-round1/` excluding `tools/solc-prefix`); nothing was fabricated.
12. **Stem independence.** The entry body contains no self-reference to its own stem
    (`grep -c` → 0), so the name-divergence substitution below touches only this patch's
    diff-header lines and Hunk B.

## Integrator notes

- **Name divergence (resolved toward the frozen stem; PL-1's plan text is stale).** This
  artifact uses `2026-10-19-arc3-r1-evm-real-solc` — matching RV-4's frozen map token
  (`claims/c1/RV-4/map-token.frozen.patch`, VERDICT PASS), EX-13's final primary artifact
  (`claims/c1/EX-13/map-token.primary.patch` + `README.primary.md:38`), RV-3's hard gate
  (`claims/c1/RV-3/quality-checklist.md`), and SC-3's records drafts. Only
  `claims/c1/PL-1/plan.md:273,364` still says `…-evm-solc` (the plan predates the freeze);
  EX-13's `map-token.patch.md:84-102` records the divergence and the measured equivalence
  of both stems. If the parent instead picks the plan stem, substitute that single string
  in this patch's two `corpus/knowledge/…` diff-header lines and in Hunk B's token; the
  entry body has no self-reference (verified, §12).
- **Honest-stop branch not needed**: every runtime leg recovered K/K; the creation-code
  legs are honest empty results and are recorded in the entry as such.
- If a reviewer refutes any leg before landing, rewrite the affected bullet to the frozen
  honest-stop branch — do not land a partially-refuted bullet.
- This seat wrote only this artifact and `seats/EX-12.md`; nothing was applied.
