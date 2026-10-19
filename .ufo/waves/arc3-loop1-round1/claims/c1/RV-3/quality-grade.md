# RV-3 quality grade — `claims/c1/EX-12/knowledge-entry.patch.md` (chain c1)

**Graded revision:** sha256 `d662c195d75cdbdb07e3534170ce9cb2ac3f830b93d5380e7b8310bca7d8ba59`
(18,701 B, mtime 2026-10-19 07:14:01 -03). An earlier revision (16,454 B, 07:11) was also
measured mid-grade; its §4 self-identity was stale (claimed 8,316 B / `f95c5a05…`, actual
apply 8,598 B / `d8d85949…`) and the **current revision resolves that** — see Fixes §0.
If EX-12 edits the artifact again, this grade covers the pinned revision only.

**Verdict: ACCEPT-WITH-FIXES** — no hard gate fails; the entry is admissible and its
content verifies end-to-end on this host. Two named fixes below (one must-fix line in the
entry, one accuracy line); both are one-line edits.

## Hard gates (frozen claim + wave couplings)

| gate | result | evidence |
|---|---|---|
| patch applies to HEAD `e845c2b` | PASS | `patch -p1` dry-run + apply, exit 0 (scratch tree `/home/vgpnk/.cache/rv3-arc3/patched2`) |
| stem == frozen map token `2026-10-19-arc3-r1-evm-real-solc` | PASS | applied file name; token line `corpus/README.md:38` (RV-4 `map-token.frozen.patch` VERDICT PASS) |
| command A after apply: 82/82, missing [], dangling [], 13/13 | PASS | `{"knowledge_files": 82, "mapped": 82, "missing": [], "dangling": [], "citation_resolved_rules": 13, "rule_blocks": 13, "coverage_score": 10.0, "depth_score": 10.0}` (worktree recipe A, same script as recipe A read from files) |
| prior-81 byte-identical | PASS | per-file sha256 head-tree vs patched: only README changed + 1 file added |
| map edit line-neutral | PASS | README 190 → 190 lines; 1 hunk, 1 line changed (token appended) |
| K/K recovered, `dispatch:"abi"` | PASS | Rv2Token 5/5, Rv2Many 11/11, KdxToken 6/6, zero extra — I recomputed each set-equality from the envelopes |
| both encodings verified | PASS | hex+raw legs on Rv2Token/KdxToken; decoded bytecode sha equal across legs |
| entry self-identity claim | PASS (current rev) | applied file = 9,513 B / 32 lines / `a5119120ee6a6142b8be6e297e39c85e0464fb27761c6ee0e7cc7cf8a1d5e56b` — matches §4 exactly |
| no fabricated citation | PASS | all 9 `ev_` ids and all 18 8-hex tokens resolve to landed c1 artifacts; 33/34 path citations resolve (the 34th, `Smoke_sol_Smoke.bin`, is a name-only reference whose full path appears in the same entry) |

## corpus/QUALITY.md admission criteria (as written: 15 rows + 6 signals)

| # | criterion | verdict | note |
|---|---|---|---|
| 1 | resolvable source | PASS | every claim cites wave paths that resolve; §10 self-attack claim reproduced by me at 33/34 |
| 2 | falsifiable / opinion | PASS | commands + expected outputs (recheck line; per-leg envelopes) |
| 3 | domain-specific | PASS | REA/EVM specifics only |
| 4 | absolute path + stable identity | PASS | full paths + sha256 prefixes; full hashes live in cited artifacts (corpus convention, r3-07 precedent) |
| 5 | observation/inference/unknown labels | PASS | 10 Observation bullets, 1 Inference, explicit Unknowns; EVMole output labeled upstream inference |
| 6 | Evidence ID / exact reproducing call | PASS | 9 ids resolve; my corrected recheck reproduced `ev_45849c8b…` bit-exactly |
| 7 | names what was NOT examined | PASS | Unknowns + Limitations bullets (Vyper, other solc versions, optimizer-enabled shapes, other prologues, id domain, >1.9 KB carriers) |
| 8 | version pins + claim source | PASS | solc `0.8.37+commit.f401782d`, rea-agents 6.4.0/6.7.0, `evmole@0.9.3`; "claim source: the sealed probe envelopes, not skill text" |
| 9 | runtime-behavior provenance | PASS | no runtime behavior asserted; `runtime_execution: not-performed` stated in the limitations bullet |
| 10 | "held" on a real carrier this round | PASS | real solc carriers probed this round; scope line: RESULT-class, no Core promotion, no availability→holding claim; language scan found no held/works verbs |
| 11 | empty vs excluded | PASS | creation legs = "parsed-and-empty results (`corpus/QUALITY.md:21`), not inventory exclusions" |
| 12 | carrier bytes / recipe retained | PASS | compile recipes stated (standard-JSON input, `solcjs --bin --abi --optimize`); byte-exactness claimed only for pinned bytes |
| 13 | `grep -o … | wc -l` for counts | PASS | no `grep -c`; counts are array lengths and were reproduced by me |
| 14 | (superseded) | — | — |
| 15 | id domain per verb family, with citation | PASS-with-fix | no universal content-addressed claim is made (correct); but "was not measured" is stale — see Fix 2 |

Weak-material signals 1-6: none present (no behavior-from-strings, no floating target, no
docs-vs-live availability claim, no static-as-runtime, no "tool broken").

## Structure vs r3-07

The entry follows the **current corpus template** (`2026-10-16-l7-01-inspect-go-binary.md`,
`2026-10-18-arc2-r7-pe-wall.md`: title → `source:` → `verified-at:` → `recheck:` → pin →
carriers → Observation/Inference/Unknowns/Limitations → `Sources:`), not r3-07's older
`## Candidates`/`## Run log`/`## Summary` form. r3-07's load-bearing elements are all
present in modern form: header staging comment (line 1), explicit per-claim source +
verify + verified-at, honest limitations, and a frontier-closure statement (the "delta vs
r3-07" bullet is the entry's core, satisfying the CR-(c) attack requirement). The
r3-07-specific section names are **not required** by QUALITY.md and no 2026-10-16+
entry carries them; no fix requested on structure.

## Required fixes

**Fix 1 (must-fix, one line).** Entry line 7 `recheck:` does not reproduce as written:
the verbatim command `cd /tmp && npx -y rea-agents@6.4.0 inspect-evm-interface … hex
--format json` fails on this host **today** — exit 1, `execution_failure` (worker phase),
because the EVM worker's temp writes hit the fleet-wide `/tmp` usrquota EDQUOT (the entry
itself documents this trap in its input-shape bullet; every other seat this wave redirects
TMPDIR). With `TMPDIR=/var/tmp/rv3-tmp` the same command exits 0 and reproduces the entry's
recorded expectations **exactly**: `ev_45849c8b…`, 5 functions, all `dispatch:"abi"`,
decoded `c1081a56…`, offsets 89/137/167/215/263. Evidence:
`claims/c1/RV-3/evidence/recheck-verbatim.out` (678 B, failure) and
`recheck-fixed.out` (9,399 B, success). Fix: add the TMPDIR redirect to the recheck line
(e.g. `cd <writable-dir> && TMPDIR=<writable-dir> npx -y rea-agents@6.4.0 …`), or state
the requirement in-line.

**Fix 2 (accuracy, one line; recommended).** Entry lines 21/28 say "The `ev_` id's full
domain for `inspect_evm_interface` was not measured". The wave's own EX-09 artifact
(`claims/c1/EX-09/rerun-compare.md` §5) did measure it: a bit-exact re-derivation of
`ev_4dd5ea20…` from the envelope via the pinned package's `semanticProjection` +
RFC-8785 canonical digest (display fields `subject.name`/`local_path` excluded; semantic
mutations change the id; path changes key it via `parameters.path`). Fix: cite EX-09
(e.g. "domain re-derived on the KdxToken raw envelope: `claims/c1/EX-09/rerun-compare.md`
§5 — path-keyed; display fields excluded") or scope the sentence to "not measured by this
entry's sources". Not admissibility-blocking: the entry correctly avoids a universal
identity claim.

**Fix 0 (already resolved; recorded for the audit trail).** The 07:11 revision's §4
claimed an entry identity (8,316 B / `f95c5a05…`) that its own patch text did not produce
(8,598 B / `d8d85949…`; the scratch file `/var/tmp/ex12-apply-test/…` holds the older
revision). The graded 07:14 revision matches its §4 exactly (9,513 B / 32 lines /
`a5119120…`) — no action needed, recorded so the intermediate defect is not silently lost.

## Independent verification performed (all re-run by this seat)

- Recipe A on HEAD (verbatim script) → 81/81, 13/13, 10.0/10.0.
- Keccak recompute (wave-prefix `js-sha3`): EX-02 Smoke 5/5 signatures → the recorded
  selectors; EX-06 keccak anchors PASS (independently corroborated by RV-1's from-spec
  Keccak).
- Byte checks: Rv2Token offsets 89/137/167/215/263 → `5b` (JUMPDEST) each; KdxToken
  100/148/178/226/254/302 → `5b` each; every planted selector occurs once in each carrier;
  KdxToken metadata trailer = 51 B, `000825` solc marker + `1220` ipfs multihash.
- Carrier hashes re-derived: Rv2Token `a4bc2d78/c1081a56/d7f73058/e6517fb7`, KdxToken
  `c2980385/9c40940e/69a15782`, Rv2Many `6a1c07d7`, Smoke `530efc7b`, soljson
  `221d7a66…` — all match the entry and the chain ledger.
- Set-equality: Rv2Token 5/5 (ABI-consistent args/mutability), Rv2Many 11/11 zero extra,
  KdxToken 6/6; EX-07's m1 shows the sole non-dispatch PUSH4 `16ee4b79@1900` unreported.
- Pre-probe timing: `expected-selectors.txt` mtime 07:00:46.98 vs first envelope
  07:01:28.58 = 41.6 s ("42 s before" holds).
- Evidence-id domain (EX-05 twins): same path → identical id; renamed path → different id
  (`ev_4dd5ea20…` vs `ev_b2937090…`, same bytes) — consistent with the entry's caution.

## Attacks attempted, with verdicts

| attack | method | verdict |
|---|---|---|
| token without file / file without token | worktree recipe A negatives | correctly dangling/missing (harness self-test; token+file = 82/82) |
| stale self-identity in the artifact | sha256 of applied file vs §4 claim | caught on the 07:11 revision (Fix 0); current revision passes |
| recorded recheck non-reproducible | ran it verbatim | FAIL as written (EDQUOT), PASS with TMPDIR — Fix 1 |
| "id domain unmeasured" overstated | cross-read EX-09 §5 | Fix 2 |
| fabricated citations | 9 ids + 18 hex tokens + 34 paths | all resolve |
| r3-07 reconstruction byte-exactness | EX-08's recon differs from the recorded r3-07 carrier-3 sha (`3e2fd6ca…` vs `41165b34…`) | NOT cited by the entry (the entry cites EX-05's byte-exact 5-byte carrier-1 recon only) — no action |
| "re-run dressed as a move" (CR-c) | read the delta bullet against r3-07:59-70 | PASS — the entry's core is the real-bytecode signal (view×2/nonpayable×3 + argument tuples where the stub returned `pure`/empty), and the citation resolves |
