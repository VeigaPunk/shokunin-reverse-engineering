# CN-3 — independent adjudication, arc3-loop1-round9

**Seat:** CN-3 (verdicts/convergence)  
**Measured base:** `947091d6b6f52684faf9ca53adf94ff8a0f6b006`  
**Scope:** independent reconciliation of frozen C1/C2/C3 claims. This verdict does not modify protected corpus, gate, custody, Province, Scorecard, or peer paths.

## C1 — freshness: reproduced facts, gate criterion not met

**Observation — live package census reproduced.** At the measured base, `PROVINCE.md:50` still says `1556 signed archives` without an as-of qualifier. Counting `/var/cache/pacman/pkg/*.pkg.tar.zst` gives 1,350 files; counting `*.sig` gives 1,350 sidecar files. The live archive count is 206 below 1,556 (`1,350 - 1,556 = -206`). This establishes file counts, not cryptographic verification of every signature. The dated source for 1,556 is `corpus/knowledge/2026-10-13-pacman-packages.md:73-83`.

**Perishable row census.** `pacman -Q jq` returned `jq 1.8.2-1`; `pacman -Qkk jq` returned 25 files / 0 altered. Installed `/usr/bin/jq` and the archive member hash to the same SHA-256, `e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806`. By contrast, `available:true in live session` is **UNVERIFIABLE**: this seat had no live REA MCP session for a fresh availability probe. `.MTREE`, `pacman -Qkk`, and `binary_session {}` name a format, verification procedure, and capability probe; they are not additional current scalar claims.

**Disposition — PARTIAL / DISCREPANCY.** The proposed same-line dated correction is factually supported and its scratch copy remained 162 lines, but it was not applied to `PROVINCE.md`. More importantly, `python3 .ufo/gates/c1-census-v10.py --quiet` exits 1: `FAIL (stale=0 ambiguous=0 undeclared=1 unresolved=0)`. The sole blocker is `SCORECARD.md` block 1833-1839, line 1834: `pin None=6.7.0 -> AMBIGUOUS (no client token in clause)`; the declared scope ends at line 1813. The same failure persists against the scratch Province patch. Therefore the frozen C1 condition “instrument PASS after” is **not established**; do not describe the row as repaired or the gate as passing.

Evidence reviewed: `claims/c1/EX-1.md:7-80`; the independent live counts, `pacman` checks, and gate run recorded for this seat; peer C1 reports PL-1..4, EX-1..4, RV-1..4 converge on the count and this blocker.

## C2 — coverage: select one different-verb Evidence-ID Unknown

**Selected single landing candidate: CR-1.** The candidate is the per-verb `inspect_sqlite_database` Evidence-ID domain, not a universal REA formula. The older SQLite entry describes default schema inventory and explicitly leaves other behavior outside scope (`corpus/knowledge/2026-10-16-l7-04-inspect-sqlite-database.md:11-14`); it does not characterize that operation's Evidence-ID projection. This is the frozen candidate “another verb family” and is distinct from r7's `inspect-evm-interface` scope (`corpus/QUALITY.md:25`).

**Evidence judgment — REPRODUCED from retained first-hand records.** CR-1 records a generated 8,192-byte SQLite fixture (SHA-256 `b0db23c66fcdf957241e6ff0e62404b411a913c39178de2304dd4bed272cf85c`), repeat calls at one path yielding byte-identical envelopes and a byte-identical copy at another path yielding a distinct ID. Its independent recomputation matches the three observed IDs; after masking only `/parameters/path`, `/normalized_result/artifact/path`, and `/locations/0/path`, the path variants' projections match. The report traces the projection to cached `rea-agents@6.7.0` source and bounds the conclusion to this operation, package, fixture, and default-inventory call. Retained reproduction output ends `result=PASS` (`claims/c2/CR-1/evidence/reproduction-run.txt:2-19`). I audited that retained output and the complete draft; I did not rerun the peer's `npx` script.

The proposed entry `claims/c2/CR-1/draft-corpus-entry.md` includes `verified-at` and a `/var/tmp` `recheck` recipe. It proposes destination `corpus/knowledge/2026-10-19-arc3-r9-sqlite-evidence-id-domain.md` and token `2026-10-19-arc3-r9-sqlite-evidence-id-domain` on the Evidence model row. Command A at the measured base is **VERIFIED** at 87 knowledge files / 87 mapped, with `missing=[]`, `dangling=[]`; the after-integration 88/88 result is **UNVERIFIABLE** until the integrator lands both files and reruns Command A.

**Candidate reconciliation.** I do not count the repeated Vyper `--no-optimize` / `-O none` K8 claims (EX-7, EX-9, CR-2, CR-3, CR-4) as a new coverage move: r8 already records that these spellings match on the same pinned fixture and compiler (`corpus/knowledge/2026-10-19-arc3-r8-vyper-optimizer-dispatch-shapes.md:9,11,13-15`). EX-5, EX-6, EX-8, and EX-11 contain other plausible, bounded unknowns. I independently recompiled EX-6's 0.8.37 viaIR fallback carrier twice (366-byte runtime, SHA-256 `2948d578ae460119f777eb379febc2738dbec14d03c76d5f100777c9552ce6fc`) and re-ran REA: three ABI selectors match and the decoded runtime digest agrees. That supports the fallback candidate, but EX-6's corpus draft lacks the required `recheck:` field; it is not the single recommended landing here. Do not land multiple C2 entries as though one were required to satisfy this wave.

## C3 — calibration: pointer drift reproduced; aggregate gate still fails

**Assertion-level result — REPRODUCED.** The sole current `rea-agents@` match in live `~/.kimi-code/config.toml` is line 4126, `args = [ "-y", "rea-agents@6.7.0", "mcp" ]`. The census resolves `PROVINCE.md:18`'s Kimi pin and pointer to `current-ok` / `pins 6.7.0`. This is a first-hand location check, not an inference from the older receipt.

**Drift class — REPRODUCED in scratch.** A `path:line` pointer addresses a literal line: inserting one line before the pin moves it to 4127 while the unchanged pointer to 4126 becomes stale. Repointing the test fixture to a line containing pin 6.7.1 makes the pointer `current-ok (pins 6.7.1)`, while the unchanged Province value 6.7.0 is graded `historical (inline marker)`. Thus `current-ok` on the pointer proves the target line contains the live pin; it does not prove the adjacent recorded pin text matches it. The real config was not changed.

**Aggregate result — DISCREPANCY.** The real census run still exits 1 on the same undeclared `SCORECARD.md:1834` blocker described under C1. The pointer assertion is `current-ok`, but the whole gate is not PASS. The characterization is recorded here; the official receipt/corpus was not changed under this seat's scope.

Evidence reviewed: `claims/c3/SC-3.md:7-23,34-55`; the scratch positional and version-mismatch checks were also independently verified for this seat. The remaining C3 peers EX-13..16, SC-1..4, RV-5..8 agree on the live line, assertion-level result, and aggregate FAIL; SC-3's version-masking caveat is confirmed.

## Integration boundary and overall verdict

- The measured base remains Command A 87/87, no missing or dangling map tokens. No post-landing count exists yet.
- C1 and C3 do **not** satisfy their whole-gate PASS criterion: the common current blocker is the out-of-scope Scorecard pin at line 1834.
- C2 has one evidence-backed, bounded candidate recommended for integration (CR-1); the expected 88/88 is a prediction, not a measured result.
- This seat writes only `.ufo/waves/arc3-loop1-round9/claims/verdicts/CN-3.md`. No commit was made, and no protected or peer file was changed.
