# RV-3 quality grade — drafted c1 knowledge entry (arc3-loop1-round3)

**Graded artifact:** `.ufo/waves/arc3-loop1-round3/claims/c1/records-drafts/knowledge-entry-draft.md`
sha256 `5c1818c7d13d1055f310f1f8d232c06778e5586d7c8cc473a02187f3a4b720af`, 21,704 B,
mtime 2026-10-19 13:14:42Z (mirror at `SC-2/knowledge-entry-draft.md`, byte-equal at grade time).
**Graded text:** the literal block between the BEGIN/END markers, extracted first-hand —
17,563 B / 37 lines / sha256 `189ac2a2cd564eca4c285a56e4ae649264c21733dc22dcfbfe380036834ddaf2`
(copy of the extracted text used for the rehearsal: scratch `/dev/shm/rv3r3/literal-current.md`;
`evidence/commandA-rehearsal.txt`).

**Revision pin.** The draft was revised four times inside ~5 minutes while this seat was
grading (18,501 → 20,630 → 20,607 → 21,704 B; trace with hashes in
`evidence/identity-churn.txt`). This grade covers **only** the pinned revision above; a
further revision voids it (r1 D9 precedent). The revision churn is itself fix R4 below.

**Verdict: ACCEPT-WITH-FIXES** for the literal text as a landing candidate. No hard gate
fails: every load-bearing numeric claim that this seat could re-derive independently was
re-derived and agrees, and the after-state predicate is measured end-to-end. Two accuracy
fixes (R1, R2), one citation-location fix (R3), the rule-#14 identity fix (R4), and two
minors (R5) are required before landing.

## Hard gates (all first-hand on this host unless noted)

| gate | result | evidence |
|---|---|---|
| proposed stem == map token | PASS | stem `2026-10-19-arc3-r3-evm-optimizer-shapes`; token patch `SC-2/map-token-patch.md` `333ca590…` (my re-hash), RV-4 verdict PASS both variants (`seats/RV-4.md:6,15-17`) |
| command A **before** | PASS | HEAD `c07af80f`: `{"knowledge_files":82,"mapped":82,"missing":[],"dangling":[],"citation_resolved_rules":14,"rule_blocks":14,10.0/10.0}` (`cmmdA.py`, git objects) |
| command A **after** (entry + PRIMARY token applied to a pristine tree) | PASS | `{"knowledge_files":83,"mapped":83,"missing":[],"dangling":[],"citation_resolved_rules":14,"rule_blocks":14,10.0/10.0}` — `evidence/commandA-rehearsal.txt` |
| prior-82 byte-identical / SKILL untouched / README line-neutral | PASS | per-file `cmp` over all 82 knowledge files: no diffs; SKILL identical; README 190 → 190 lines, after-sha `016b632e46e5852ab966f7d99776676f125ffbf2418a897a4f8af9e31a642281` ≡ SC-2's claim ≡ RV-4 PRIMARY |
| K/K recovered, zero extras | PASS | my own keccak re-derivation (`js-sha3` from the receipted prefix) from each ABI vs planted file vs probe envelope, set-equality on all legs: VaultB opt200 13/13, nopt 13/13; carrierB@EX-04 opt200/noopt 11/11 (hex + raw-bin); CarrierB 8/8 (hex 6.4.0/6.7.0, raw); CarrierBErr 8/8; Rv2TokenOpt 5/5 ×6; carrier-A 3/3 |
| decoded `bytecode.sha256` ≡ carrier bytes, offsets JUMPDEST | PASS | every runtime leg: decoded sha == sha256 of decoded carrier file; every reported `bytecode_offset` lands on `0x5b` (my opcode-aware sweep, `evidence/push4-census.txt`) |
| compile provenance (real solc, pinned) | PASS | byte-identical recompiles from the frozen standard-JSON inputs with the receipted prefix `0.8.37+commit.f401782d`: VaultB opt200 `aaf85cea…`/1850 B, noopt `679678e9…`/3872 B; CarrierB `b9c70178…`/1469 B; CBOR `solc 000825` in all carriers; metadata `optimizer.enabled/runs` as claimed |
| recheck line reproduces | PASS | SC-2's `recheck-opt200.json` `05f76b33…` and `recheck-rv2token.json` `f2aec424…` are byte-identical (`cmp`) to EX-10's/EX-06's captures; **I re-ran the r1-canonical command myself** (disk-backed TMPDIR) → 5/5, `dispatch:"abi"`, decoded `c1081a56…` (`evidence/recheck-r1-verbatim.json`) |
| citations resolve | **FAIL (fix R3)** | 150 brace-expansions of the literal's backticked citations; 15 resolve-shapes fail, of which 4 are real location defects (R3) and the rest are prose mentions/short forms (accepted per r1 precedent) |
| label discipline (QUALITY 5/7/11) | PASS | Observation ×11 / Inference / Unknowns / Limitations / Scope present; creation/trap legs labeled parsed-and-empty; no `held`/`works` verb in the literal text; no `grep -c`; the `/tmp` mention is inside the documented EDQUOT trap sentence and the recheck line itself carries the disk-backed `TMPDIR` |

## corpus/QUALITY.md criteria (file as written: 15 rows + 6 signals)

| # | criterion | verdict | note |
|---|---|---|---|
| 1 | resolvable source | **FAIL → R3** | `EX-04/evidence/planted-B.txt` (actual: `EX-04/planted-B.txt`, sha matches `f32393c0…`), `EX-04/evidence/offset-check-*.json` (actual: `EX-04/evidence/probe/offset-check-*.json`), 5 of 12 `optB-…-rerun.json` expansions never existed, `round1/…carrier-A.hex` shorthand |
| 2 | falsifiable / opinion | PASS | recheck line with expected outputs; every leg carries its envelope |
| 3 | domain-specific | PASS | REA/EVM only |
| 4 | absolute path + stable identity | PASS-with-fix | identities present and re-derived; the two hex-size pairs are mislabeled (R2) |
| 5 | observation/inference/unknown labels | PASS | probe mutability labeled upstream inference; the pure/view delta is stated as a probe-inference fact, not ABI truth |
| 6 | Evidence ID / reproducing call | PASS | every `ev_…` in the literal resolves to a landed envelope (all checked); ids quoted with `…` suffixes per corpus convention |
| 7 | names what was NOT examined | PASS | Unknowns: other solc/Vyper, runs≠200, viaIR, other prologue classes, id-domain formula, >3.87 KB |
| 8 | version pins + claim source | PASS | solc 0.8.37, rea-agents 6.4.0/6.7.0, evmole 0.9.3; "claim source: the sealed probe envelopes" |
| 9 | runtime-behavior provenance | PASS | no runtime behavior asserted; `runtime_execution: not-performed` in every envelope |
| 10 | "held" only on real carriers | PASS | RESULT-class scope; no availability→holding claim |
| 11 | empty vs excluded | PASS | raw-on-hex trap = parsed-and-empty, explicitly "not a carrier defect" |
| 12 | carrier bytes / recipe retained | PASS | sources + standard-JSON recipes + pinned sha256s; "byte-exactness is claimed for these pinned bytes only" |
| 13 | `grep -o … | wc -l` for counts | PASS | no `grep -c`; counts are array lengths / census outputs |
| 14 | (superseded) | — | |
| 15 | id domain per verb family, with citation | PASS | path-sensitivity measured and cited with ids; no formula claimed |

Signals 1-6: none present (no behavior-from-strings; no floating target; no docs-vs-live claim;
no static-as-runtime; no "tool broken"). The `fa41aa00`-class sweep artifacts were *not*
imported as constants by the draft (it kept `43000825` correctly framed as a trailer constant).

## Required fixes

**R1 (accuracy, must-fix — QUALITY 1/5).** Line 26, first sentence: "VaultB (**both
variants**) carries `4e487b71` (panic) plus four revert-path error constants (`1309a563`,
`1dc930eb`, `30cd7471`, `3c3332b9`)" is **false for the nopt variant** and contradicts
EX-10's own artifact. Measured (`evidence/push4-census.txt`): nopt's non-dispatch `PUSH4`
set is only the trailer-derived `43000825` (`EX-10/recon-B-nopt.json` agrees:
`non_dispatch_push4_constants: ["43000825"]`); in nopt the error/panic data occur as
**PUSH32** revert-data words (`…40517f1309a563…`, `…5b7f4e487b71…`), and `3c3332b9` does
not occur in the nopt bytes at all (0 hits over 3,163 B). opt200's set is the five
constants as claimed (`EX-10/recon-B-opt200.json`). Fix: scope the clause to the opt200
variant and state the nopt form (trailer constant only; error data as PUSH32), or split
the sentence per variant. Selector oracle used: `NotOwner()`=30cd7471, `IsPaused()`=1309a563,
`Insufficient()`=1dc930eb (js-sha3, receipted prefix); the `3c3332b9` opt200 site is a
revert-data write (`PUSH4 3c3332b9; PUSH1 0xe1; SHL` at pc 1037) — describe it as such.

**R2 (accuracy, must-fix — QUALITY 4).** Two hex-carrier size labels quote the file's
sha256 at the *hex-character* count, not the file size: `CarrierB` "hex carrier 2,938 B
`247e09f3…`" — the file is **2,939 B** (`247e09f3…` is its sha256); `Rv2TokenOpt` "hex
carrier 1,956 B `a07bef2e…`" — the file is **1,957 B**. Fix: write the file sizes
(2,939 / 1,957) or say "2,938 / 1,956 hex chars"; the identity pair must cohere (r1 D5
was the same class of labeling defect).

**R3 (citations, must-fix — QUALITY 1).** Correct the four locations: `EX-04/evidence/planted-B.txt`
→ `EX-04/planted-B.txt` (or move a copy into `evidence/`); `EX-04/evidence/offset-check-*.json`
→ `EX-04/evidence/probe/offset-check-*.json`; the `optB-{hex,raw}-{6.4.0,6.5.0,6.7.0}{,-rerun}.json`
shorthand expands to 5 non-existent names (only `optB-hex-6.7.0-rerun.json` exists) — write the
actual set; `round1/claims/c1/CR-1/evidence/carrier-A.hex` → the full
`.ufo/waves/arc3-loop1-round1/claims/c1/CR-1/evidence/carrier-A.hex` (prose shorthand otherwise).

**R4 (rule #14, must-fix).** `SC-2/README-identities.txt` (13:13:52Z) pins the draft at
20,607 B / `b9ca0310…`, but the draft is 21,704 B / `5c1818c7…` (13:14:42Z) — the
self-identity block is stale for the current revision (the r1 D9 class). Fix: re-derive the
identities after the final write (SC-2's own note says a landing must re-hash the landed
file — that remains the parent's obligation at landing regardless). The churn itself
(four revisions in ~5 minutes, two of them after the identity file was written) should be
recorded in the round section as a caught in-wave defect, not silently absorbed.

**R5 (minors, recommended).** (a) Cite the Rv2TokenOpt source path + sha
(`.ufo/waves/arc3-loop1-round1/claims/c1/RV-2/Rv2Token.sol`, `a4bc2d78…` per the r1 entry)
instead of the bare `Rv2Token.sol` mention — row 12 wants the recipe's source resolvable.
(b) `fa41aa00`-style sweep artifacts: nothing to fix, but keep the report of `43000825` as a
trailer constant — do not let a future revision promote it to a "carrier constant".

## Independent measurements performed by this seat (first-hand)

1. Recipe A from Git objects at HEAD, and the worktree variant (self-tested identical on the
   unpatched tree) — `evidence/commandA-rehearsal.txt`.
2. Keccak set derivation from every carrier ABI vs planted vs probe envelopes (7 carriers,
   12 legs) — all set-equal, zero extras.
3. Opcode-aware linear-sweep census (PUSH4 sites, duplicates, JUMPDEST at every reported
   offset) — `evidence/push4-census.txt`.
4. Byte-identical recompiles from the frozen standard-JSON inputs (VaultB opt200/noopt,
   CarrierB) with the receipted prefix; CBOR trailer + metadata optimizer settings.
5. `cmp` of SC-2's two recheck captures against the executors' envelopes; my own re-run of
   the r1-canonical recheck — `evidence/recheck-r1-verbatim.json`.
6. Citation expansion (150 names) and identity re-hashing of every SC-2 artifact quoted in
   `README-identities.txt` (all six quoted hashes reproduce; the *scope* is stale — R4).

## Attacks attempted, with verdicts

| attack | verdict |
|---|---|
| "probe outputs are transcribed, not produced" | refuted in part: envelope bytes match across independent runs (SC-2's captures ≡ executors' captures, `cmp`); full id re-derivation from source not re-run this round (r1 E4 covered the mechanism) — stated as residual, not claimed |
| "the after-state is asserted" | refuted: applied to a pristine tree, measured 83/83 |
| "the carriers are hand-assembled" | refuted: byte-identical recompiles + solc CBOR |
| "the K/K claim rides a planted table" | refuted: independent keccak from ABIs |
| "the census claims are accurate" | **partially sustained** — the nopt "(both variants)" clause (R1) |
| "every citation resolves" | **sustained** — four locations (R3) |
| "the self-identity block is current" | **sustained** — stale vs the final revision (R4) |
| "the pure/view delta is overstated" | not sustained: measured on both legs (`0x07bf89ab`: ABI `pure`, probe `view`), and the draft frames it as upstream inference |

## Scope of this grade

This seat graded a **draft**; nothing was applied to the lane repo by RV-3 (writes: this
seat's dir + `seats/RV-3.md` only). The parent must land exactly one token variant and
re-derive the landed entry's identity per rule #14.