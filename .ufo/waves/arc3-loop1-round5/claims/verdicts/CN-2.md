# CN-2 — round-5 convergence check

## Scope and evidence boundary

The frozen roster assigns CN seats to verdicts/convergence (`claims-frozen.md:81-86`); dispatch instructions put seat artifacts below `claims/<chain>/<SEAT>/` (`dispatch-plan.md:4-6`). The current direct inventory contains 16 individual C2 reports (CR-1/2/3/4, EX-5/6/7/8/9/10/11/12, RV-5/6/7/8), plus C1 `SC-2`, C3 `PL-4`, and verdict `VZ-4`, which I read and reconcile below. The required aggregate `claims/c2/audit.md` is absent. The three dated arc3 EVM entries are r1/r3/r4; the Ghidra entry's appended errata form the fourth audit unit, but no separate dated arc3-r2 file is present. The full C2 coverage claim therefore remains **UNVERIFIABLE as specified**; individual seat audits are not a substitute for the frozen aggregate artifact.

I also read the round-4 `claims/cross/consistency.md` and `claims/cross/wave-summary.md` as historical context only. They refer to an earlier HEAD; I do not use their numbers as evidence for this round. All values below were re-derived from Git objects, current files, or read-only instruments.

## Independent checks

### Command A — REPRODUCED

I reran the recipe at `SCORECARD.md:88-124` against each supplied object and current HEAD (same Git-object reads; `-B` prevents bytecode writes). Exact JSON outputs:

```json
{"citation_resolved_rules": 13, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 82, "mapped": 82, "missing": [], "revision": "fbbbd45", "rule_blocks": 13}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 82, "mapped": 82, "missing": [], "revision": "28aa7a9", "rule_blocks": 14}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 83, "mapped": 83, "missing": [], "revision": "5be4a26", "rule_blocks": 14}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 83, "mapped": 83, "missing": [], "revision": "c418be0", "rule_blocks": 14}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 84, "mapped": 84, "missing": [], "revision": "40de383", "rule_blocks": 14}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 83, "mapped": 83, "missing": [], "revision": "520341d", "rule_blocks": 14}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 84, "mapped": 84, "missing": [], "revision": "71668cc", "rule_blocks": 14}
```

Commit metadata independently exposes a label discrepancy in the supplied key-facts grouping: `git show --no-patch --format='%H%n%P%n%s' 5be4a26` identifies `5be4a265cb089eb086d74c5eece1ad622128848d`, parent `c418be02006314a464e2961542542bccd5df254d`, subject `hygiene: drop committed pyc + root-ignore __pycache__`. `git diff --stat c418be0 5be4a26` shows only `.gitignore` and deletion of the generated `.pyc`. Thus 5be4a26 is a hygiene child of the r3 work commit, not an r2 work commit. Its measured Command-A output is recorded above, but its round label should not be used as supplied.

### Current gates — REPRODUCED at HEAD `71668cc`

- Census: `TMPDIR=/var/tmp PYTHONDONTWRITEBYTECODE=1 python3 -B .ufo/gates/c1-census-v10.py --root .` ended with `VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)`; it also reported `PROVINCE.md lines=162`, `SCORECARD.md lines=1631`, `SKILL.md lines=390`.
- Citation drift, default: `TMPDIR=/var/tmp PYTHONDONTWRITEBYTECODE=1 python3 -B .ufo/gates/citation-drift/citation-drift-probe.py --root .` → `CITATION_DRIFT_VERDICT: reported findings=0 exit=0`.
- Citation drift, strict: `TMPDIR=/var/tmp PYTHONDONTWRITEBYTECODE=1 python3 -B .ufo/gates/citation-drift/citation-drift-probe.py --root . --strict` → `CITATION_DRIFT_VERDICT: clean findings=0 exit=0`.
- The task's `python3 -B .ufo/gates/custody-pair/custody-pair.py --selftest` invocation is a **DISCREPANCY**: it exits 2 with `usage: custody-pair.py [-h] {capture,verify,selftest,paths} ...` and `error: the following arguments are required: cmd`. The source requires a positional subcommand (`custody-pair.py:1313`) and registers `selftest` (`:1329-1333`). Corrected invocation `TMPDIR=/var/tmp PYTHONDONTWRITEBYTECODE=1 python3 -B .ufo/gates/custody-pair/custody-pair.py selftest` is **VERIFIED**: `CUSTODY_PAIR_SELFTEST: CLEAN cases=28 passed=28 failed=0 exit=0`.

## Peer reconciliation

### C1 — SC-2 (`claims/c1/SC-2.md`)

- **Shared checks agree.** SC-2's seven Command-A JSON rows (`SC-2.md:12-18`) exactly match my Git-object re-runs above. Its census, both citation-drift modes and corrected custody invocation (`:25-37`) match my independent live outputs.
- **Nine stale-literal claim — DISCREPANCY confirmed.** I searched the exact nine needles in the source list (`arc3-loop1-round4/claims/c2/PL-2/plan.md:77-87`) against the current full `PROVINCE.md`. Eight have no match: `Reserve: 91MB Godot ARM64 template`, `all 3 organic cores`, `real solc/vyper-compiled bytecode untested`, `Next: raise \`REA_GHIDRA_STARTUP_TIMEOUT_MS\``, `probe-refused since r2`, `pacman pairs beyond expac unexercised`, `absent: \`7z\``, and `35 features incl. PyGhidra/BSim`. The remaining literal does match: `PROVINCE.md:88` reads `JEB (unprobed). Engine installs are operator-owned.` This is the current alternate-provider status, so the broad whole-file absence assertion is false; do not delete the current status to satisfy it. SC-2's 8/9 discrepancy (`SC-2.md:41-55`) is reproduced.
- **Vyper evidence spot-check — VERIFIED for the claims tested.** I independently hashed and parsed `arc3-loop1-round4/claims/c1/EX-04/out/runtime.bin` plus the three sealed probe JSONs and `evidence/planted-K.json`. My exact output:

```text
runtime_bytes=1562 runtime_sha256=57d6fd0ae0da001975a3f58ae72804757aa36267f6e373bf9f134ecc9791dae0
prologue_24=5f3560e01c6002600d820660011b61060001601e395f5156
table_offset=0x600 entries=13 targets=0x29c,0x5e7,0x50b,0x400,0x5ac,0x43f,0x53d,0x5e7,0x590,0x574,0x382,0x5e7,0x18
all_targets_jUMPDEST=True
empty_bucket_sentinel_0x5e7_count=3
probe-6.4.0-hex.json: count=15 unique=15 missing=[] extra=[] all_dispatch_abi=True decoded_bytes=1562 decoded_sha256=57d6fd0ae0da001975a3f58ae72804757aa36267f6e373bf9f134ecc9791dae0
probe-6.4.0-raw.json: count=15 unique=15 missing=[] extra=[] all_dispatch_abi=True decoded_bytes=1562 decoded_sha256=57d6fd0ae0da001975a3f58ae72804757aa36267f6e373bf9f134ecc9791dae0
probe-6.7.0-hex.json: count=15 unique=15 missing=[] extra=[] all_dispatch_abi=True decoded_bytes=1562 decoded_sha256=57d6fd0ae0da001975a3f58ae72804757aa36267f6e373bf9f134ecc9791dae0
```

These are read-only checks of committed binary/evidence, not fresh REA provider runs. They corroborate the limited SC-2 Vyper claims (`SC-2.md:57-71`); no broader Vyper claims are made here.

### C2 — peer reconciliation (`claims/c2/*.md`)

- **Frozen deliverable remains absent.** The current direct inventory has 16 individual reports: CR-1/2/3/4, EX-5/6/7/8/9/10/11/12, and RV-5/6/7/8. There is still no `claims/c2/audit.md`, so the frozen C2 per-entry aggregate deliverable is **UNVERIFIABLE as specified**, despite substantial per-seat findings.
- **r1 Smoke carrier — CORRECTED, byte domains reproduced.** `EX-02/smoke/out/Smoke_sol_Smoke.bin` is 1,370 bytes of ASCII hex, SHA-256 `530efc7bb166fd47e42fe9623ee347234b99a65691b0a0ad42d2682702986a5f`; decoding gives 685 bytes, SHA-256 `08299f31203e05e5dcdcd2453f9dd5a105a97fd94f2b48194ba18e963c368ebd`. The r1 entry `:15` pairs the decoded length with the text-carrier digest. I independently recomputed both hashes and lengths; EX-7, EX-11, CR-2, RV-5/6 and CR-4 identify the same correction.
- **r1 creation erratum — CORRECTED at `:31`; line `:24` is still false.** The entry's original `:24` says “Creation blobs carry no runtime dispatch table”; its append at `:31` correctly explains that the zero-function probe is parsed-and-empty and the embedded runtime remains in the creation bytes. My byte check above re-derived the 1,971-byte creation, 1,943-byte runtime at offset 28, and zero probe functions. This corrects the earlier CN-2 wording (which had wrongly described `:24` as corrected).
- **r3 CBOR/PUSH4 — DISCREPANCY reproduced.** Opcode-aware parsing of the retained runtime binaries shows `43000825` is trailer data, not an executable PUSH4: VaultB nopt is 3,163 bytes, code ends at 3,110, has 15 code-region PUSH4 sites (all selector occurrences), and the marker is at 3,157; Rv2TokenOpt is 978 bytes, code ends at 925, has six code-region PUSH4s (five selectors plus `4e487b71`), and the marker is at 972. Thus r3 entry `:26` is wrong to count the CBOR token among code PUSH4s. Sources: `EX-10/out/VaultB.nopt.runtime.bin`, `EX-07/Rv2TokenOpt.runtime.bin`, `corpus/knowledge/2026-10-19-arc3-r3-evm-optimizer-shapes.md:26`. CR-1, EX-6, RV-6 and CR-4 independently report this correction.
- **r4 initcode claim — CORRECTED; EX-12's r3 pointer is wrong.** The false “initcode carries no runtime dispatch table” sentence is at r4 `:17`, not r3 `:24` (which is the Rv2TokenOpt result; the r3 entry has no initcode phrase). Independent byte checks: CarrierV creation 1,637 bytes embeds its 1,562-byte runtime at offset 20; Ex09Vault creation 659 bytes embeds its 581-byte runtime at offset 24 (`54b14e306bbaf7614d062c06522e88327177aba576309905008e63a90ad199ee`). Both creation probes return zero functions (`EX-06/probe/CarrierV-creation-6.4.0.json`, `EX-09/probe/vy-creation-hex-6.4.0.json`), which says parsed-and-empty only, not that runtime dispatch bytes are absent or executed by initcode. Sources: `EX-04/out/{creation.bin,runtime.bin}`, `EX-09/vyper/{Ex09Vault.creation.hex,Ex09Vault.runtime.hex}`, r4 entry `:17,21`, EX-12 `:31-33`.
- **Ex09Vault carrier-text identity — representation difference, not runtime mismatch.** The checked-in prefixed `.runtime.hex` is 1,165 bytes / `05a29536…`; the saved probe copy is 1,163 bytes / `aee38762…` and exactly equals the checked-in file after removing its leading `0x`. Both decode to 581 bytes / `54b14e306bbaf7614d062c06522e88327177aba576309905008e63a90ad199ee`. This confirms CR-2's provenance difference while resolving the cause: the two-byte prefix is the only carrier-text difference.
- **Ghidra feature count — VERIFIED locally.** A direct filesystem count returned 34 directories / 34 entries under `~/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features`, matching the append-only Ghidra correction and `PROVINCE.md:46`. This resolves CR-2's out-of-scope count for the current host; it does not attest install provenance.
- **Ex09Vault dispatch — EX-10's unresolved claim does not reproduce.** I decoded the 581-byte runtime's table at `0x239` (heads `[24,516,544,489,247,440]`) and followed the actual `JUMPDEST; PUSH4; DUP2; XOR; PUSH2; JUMPI` nodes. The seven planted selectors all occur in their `%6` bucket chains: bucket 0 `24:d0e30db0 -> 219:2ddbd13a`; bucket 1 `516:5c975abb`; bucket 2 empty; bucket 3 `489:8da5cb5b`; bucket 4 `247:0ff5ce72 -> 412:191a62d4`; bucket 5 `440:2bec1547`. Thus the two “missing” selectors in `EX-09/analysis/dispatch-structure.txt:14,16,63,65` are a false negative of that walk, not a bytecode/probe contradiction; all seven compare sites are present and correctly bucketed. This resolves EX-10 `:19` against the bytes; the runtime 7/7 result remains supported.
- **Auxiliary matrix — mixed verdict, not wholly unverifiable.** I parsed the saved alternate probe envelopes, recomputed selector Keccak sets against ABI/source signatures, and compared decoded hashes to `VZ-1/evidence/kk-matrix.json:45-108`: CarrierA 9/9 (`9f7392acccea72cd`), OptVault 5/5 (`544469b7bebfda4e`), MutMix 6/6 (`6267ef53adf978e5`), MutMixOpt 6/6 (`200bc9db76cc8592`); each set is equal. The alternate envelopes are under `EX-02/evidence/` and `PL-1/evidence/` and carry different path-sensitive IDs from the matrix. Exact matrix IDs appear only in `kk-matrix.json`, not in retained individual envelopes; so CR-2/CR-4/RV-7 are right that those exact IDs and matrix `extras_push4` fields are **UNVERIFIABLE**, but their broader K/K-row uncertainty is too broad for these four rows. EX-5/6/7 and CR-1 also report K/K results; this direct check corroborates the counts and decoded identities, not the missing matrix IDs.
- **Core-status wording — UNRESOLVED cross-file contradiction; no promotion verdict.** The r1 and r3 corpus entries explicitly scope themselves to RESULT-only and disclaim Core promotion (`corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md:33`; r3 `:35`). `PROVINCE.md:75` says Frontier items are claimed but “not yet held,” with each move to Core requiring a `LOG.md` entry citing corpus entries; yet its r1/r3 Frontier bullet (`:91-93`) labels those carriers “(Core, arc3-r1/r3).” `git show 40de383 -- PROVINCE.md` confirms that contradictory label landed with the r4 work commit. The r1/r3 LOG entries record the knowledge items landing (`LOG.md:1396-1412,1457-1471`), but not a distinct Core promotion; therefore neither the labels nor the disclaimers establish uncontested current status. This matches CR-3's unresolved classification and requires parent adjudication. PROVINCE names the r4 Vyper carrier without an explicit Core tag, so claims that r4 is itself marked Core are unsupported; no corpus/PROVINCE edit was made.
- **Corpus inventory ambiguity.** Only three dated `2026-10-19-arc3-r*.md` files (r1/r3/r4) exist; the Ghidra entry's append-only errata are the fourth audited unit. No separate dated r2 entry was found. If the frozen “r2/r3 errata” means a distinct missing r2 target, it remains **UNVERIFIABLE** until pointed out.
- Other C2 seats broadly agree on the principal selector/hash/dispatch checks. This convergence does not independently validate live REA reruns, compiler-install provenance, or every ancillary inference that individual reports mark out of scope.

### C3 — PL-4 (`claims/c3/PL-4.md`)

- **Mid-leg retest — STOPPED-with-reason is supported.** My independent `free -b` check returned:

```text
               total        used        free      shared  buff/cache   available
Mem:     32483102720 10402562048  1049780224  1112829952 22623657984 22080540672
Swap:    36779188224  4199067648 32580120576
```

The `free` column is 1,049,780,224 B while `available` is 22,080,540,672 B, so the threshold depends on which reading “free RAM” means. In addition, no affirmative operator host-cost authorization is recorded in the material inspected. Both conditions are required by `claims-frozen.md:60-66`; no retest was launched. This supports PL-4's honest stop (`PL-4.md:5-16`).
- **r10 deficit — count REPRODUCED; rationale DISCREPANCY.** I parsed `receipts/roster-frozen.txt:3` (64 logical slots) and directly enumerated current `*.md` reports in `arc2-loop1-round10/`:

```text
roster_ranges=[('P', '1', '4'), ('C', '1', '4'), ('E', '1', '28'), ('S', '1', '2'), ('SC', '1', '2'), ('R', '1', '8'), ('CR', '1', '8'), ('V', '1', '6'), ('Z', '1', '2')]
expanded_roster=64 reports=59 absent=5 unrostered=0
absent_names=CR1,E1,E17,E28,R7
unrostered_names=
```

The five-seat shortfall count in PL-4 (`:18-29`) reproduces. The names differ from the old `receipts/roster-reconciliation.txt:1` note (which says P1 is absent); current `P1.md` exists. The R5 freeze explicitly permits `DISCHARGED-BY-PRECEDENT` unless this sweep shows r10 findings are needed (`claims-frozen.md:67-70`), but PL-4's “per the counting lesson” rationale is inaccurate: the cited lesson says to re-dispatch exactly one replacement per unresolved logical seat for a true shortfall and states no operator-interruption exception (`corpus/lessons/2026-10-18-wave-dispatch-counting.md:39-51`). The frozen R5 option may authorize the recorded disposition; it does not make the lesson citation support it. No R10-specific need appears in the C1/EX-12 findings I reviewed, but the aggregate C2 audit is still missing.
- **Full C3 census — CARRIED-forward with cause supported.** Independent archive searches `Glob(.ufo/waves, arc2-loop1-round{1,2,3,4}/**/*dispatch*)` and `Glob(.ufo/waves, arc2-loop1-round{1,2,3,4}/**/*.jsonl)` both returned **No matches found**. The current census table still has `<fill>` cells at `arc2-loop1-round10/E19.md:214-217`. This supports PL-4's local-evidence limitation (`PL-4.md:31-40`), but establishes only that those captures are absent from the checked-in paths, not that no external session log exists.

### Verdict peer — VZ-4 (`claims/verdicts/VZ-4.md`)

- VZ-4's shared C1 findings agree with the independent checks above. Its earlier statement that no C2 report existed (`VZ-4.md:69-73`) is superseded by the current 16-report inventory; the required aggregate `audit.md` is still absent.
- VZ-4 also flags the r10 counting-lesson rationale and report-identity mismatch (`:78-87`). I independently confirmed the lesson's redispatch rule at `corpus/lessons/2026-10-18-wave-dispatch-counting.md:39-51`; the round-5 freeze itself nevertheless explicitly permits a discharge-by-precedent ruling. This is a rationale discrepancy, not authority to override the frozen choice. Its local-census partial finding agrees with my archive search and the `<fill>` cells at `arc2-loop1-round10/E19.md:214-217`.
- I did not independently re-run VZ-4's remaining per-seat reconciliations; no additional cross-seat result is inferred from them.

## Convergence ruling

- C1: Command A and landed census/probes **REPRODUCED**; custody behavior **VERIFIED** only with the positional `selftest` subcommand (the specified `--selftest` form is a **DISCREPANCY**); the whole-file stale-literal claim is **DISCREPANT (8/9)**; the Vyper runtime identity, selectors and table claims I checked are **VERIFIED**.
- C2: Sixteen individual reports are present, but `claims/c2/audit.md` is absent, so full frozen coverage remains **UNVERIFIABLE**. I reproduced the Smoke file/decoded-byte discrepancy, the r1 `:31` creation erratum, the r3 CBOR/PUSH4 error, the r4 initcode embedding, and all seven Ex09Vault bucket-chain sites. Four secondary K/K matrix rows reproduce from alternate same-byte probes; their exact VZ matrix IDs and extra-PUSH4 fields remain **UNVERIFIABLE**. Core status for r1/r3 remains **UNRESOLVED**: PROVINCE calls the Frontier items not yet held but labels them Core, while the corpus entries disclaim promotion; r4 has no explicit Core tag. No separate dated r2 entry was found, leaving scope ambiguous.
- C3: The faithful retest **STOPPED-with-reason** and full census **CARRIED-forward** are supported. The r10 shortfall count is **REPRODUCED**; the missing-name snapshot and “per the counting lesson” rationale are **DISCREPANCIES**. The freeze allows `DISCHARGED-BY-PRECEDENT`, but the final relevance condition should be recorded against that explicit rule, not attributed to the generic counting lesson.
- Overall: **UNVERIFIABLE** pending the required aggregate C2 audit and clear C3 debt rationale, with the C1/C2 discrepancies above. Round-4 reports remain historical context only, not evidence for these round-5 results.

No tracked file was modified by this seat. The observed pre-existing `M .ufo/waves/arc2-loop1-round10/C3.md` was left untouched; all test scratch used `/dev/shm`/`/var/tmp`.
