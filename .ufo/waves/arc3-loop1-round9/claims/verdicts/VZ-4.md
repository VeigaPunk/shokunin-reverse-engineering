# VZ-4 — independent C1/C2/C3 convergence verdict

Wave: `arc3-loop1-round9` · frozen claims: `.ufo/waves/arc3-loop1-round9/claims-frozen.md:14-56`  
Measured repository HEAD: `947091d6b6f52684faf9ca53adf94ff8a0f6b006`  
Verified: 2026-10-19  
Scope: reconcile delivered chain claims and verdicts; source, gate, custody, corpus, and peer paths remained read-only. This file is the only repository artifact written by this seat. Reproduction scratch stayed under `/var/tmp`.

## Verdicts at a glance

- **C1 — STALE COUNT VERIFIED; ROW CORRECTION PROPOSED BUT NOT LANDED; required gate PASS is a DISCREPANCY.** The current cache contains 1,350 `.pkg.tar.zst` files and 1,350 matching `.pkg.tar.zst.sig` files; `PROVINCE.md:50` still says `1556 signed archives` without a local date. The historical 1,556 is a 2026-10-13 snapshot, not a current count. The installed `jq` byte-identity check re-verified today. The current-session `available:true` value was not re-probed. The census gate is **FAIL** on an unrelated undeclared `SCORECARD.md:1834` assertion.
- **C2 — REPRODUCED for the bounded K8/Vyper output boundary; canonical coverage move is NOT LANDED.** I select the frozen Vyper candidate and recommend the comprehensive EX-10 draft. Creation/runtime bytecode and parsed output content agree for this exact K8 source and Vyper build, but raw stdout is not identical in every compiler format: `ast`, `annotated_ast`, and `archive` differ byte-for-byte. The baseline remains Command A 87/87; no post-landing 88/88 result exists.
- **C3 — REPRODUCED at the live-pointer and drift-mechanism level; durable landing remains pending.** The one live `rea-agents@` occurrence is at config line 4126, and the instrument grades the `PROVINCE.md:18` pointer `current-ok`. A controlled insertion before the pin makes the old physical-line pointer stale. The full gate remains **FAIL** for the same SCORECARD locus; no corpus/receipt characterization was landed.
- **Overall: incomplete.** Do not report the requested C1 gate PASS, C2 post-land coverage increase, or C3 canonical landing as achieved.

## C1 — pacman inventory and PROVINCE row

Fresh read-only checks against the current worktree:

```text
$ git rev-parse HEAD
947091d6b6f52684faf9ca53adf94ff8a0f6b006
$ wc -l PROVINCE.md
162 PROVINCE.md
$ grep -n '1556' PROVINCE.md
50:| Archive/package inventory | `inspect_artifact`/`extract_artifact` (`available:true` in live session); pacman `.pkg.tar.zst` corpus 1556 signed archives; `.MTREE` per-file sha256; `pacman -Qkk` verify | `binary_session {}` capabilities | installed `jq` verified byte-identical to signed archive member |
$ ls /var/cache/pacman/pkg/*.pkg.tar.zst | wc -l
1350
$ ls /var/cache/pacman/pkg/*.pkg.tar.zst.sig | wc -l
1350
$ pacman -Q jq
jq 1.8.2-1
$ pacman -Qkk jq
jq: 25 total files, 0 altered files
$ sha256sum /usr/bin/jq
 e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806  /usr/bin/jq
$ bsdtar -xOf /var/cache/pacman/pkg/jq-1.8.2-1-x86_64.pkg.tar.zst usr/bin/jq | sha256sum
 e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806  -
```

The live pathname counts confirm 1,350 archives and 1,350 matching sidecars, a delta of −206 from the dated 1,556 snapshot. Sidecar presence is not cryptographic verification of every cached signature. `corpus/knowledge/2026-10-13-pacman-packages.md:73-83` already calls 1,556 a dated snapshot and records the 1,350/−206 erratum. The independent historical 2026-10-13 cache cannot be reconstructed from the present cache.

Other row claims: `available:true` is session-scoped; `PROVINCE.md:40` dates the table survey to 2026-10-13, and I did not have a live `binary_session {}` probe to establish present availability. The installed-`jq` comparison is verified for 2026-10-19 as above and should be dated. `.MTREE` per-file sha256, `pacman -Qkk verify`, and `binary_session {}` describe a format, procedure, and probe shape rather than additional live counts.

**Integration recommendation:** use the more complete same-line proposal in `.ufo/waves/arc3-loop1-round9/claims/c1/PL-2.md:20-34` (or preserve its qualifications): date `available:true` to the 2026-10-13 session, retain 1,556 only as the dated snapshot, state the 1,350 recount and −206 delta with the pointer to the corpus erratum, and date the fresh `jq` result. This remains proposal text; no `PROVINCE.md` edit was made. Peer scratch-patch checks preserve 162 lines, but they do not establish an applied correction.

The v10 census was rerun on the unmodified source. Instrument identity: SHA-256 `e4fb740cb8153f15c623f3b9f7ca781e270053b0557be5393010359b2213b7b4`. Exact relevant output:

```text
-- UNDECLARED (1) --
  SCORECARD.md block 1833-1839 [scope None]
      :1834 [pin] None=6.7.0 -> AMBIGUOUS (no client token in clause)
      :18 [ptr] __ptr__=~/.kimi-code/config.toml:4126 -> current-ok (pins 6.7.0)
VERDICT: FAIL  (stale=0 ambiguous=0 undeclared=1 unresolved=0)
gate_exit=1
```

The `SCORECARD.md` scope ends at line 1813 (`.ufo/gates/c1-census-v10.py:276-277`), so the line-1834 finding is outside scope and is separate from the pacman row. C1's frozen “instrument still reads PASS” after-condition is therefore a **DISCREPANCY**, not a pass.

## C2 — select the residual Vyper output boundary

The frozen C2 claim asks for exactly one bounded Unknown and explicitly names the Vyper `--no-optimize` vs `-O none` residual-output boundary (`.ufo/waves/arc3-loop1-round9/claims-frozen.md:30-42`). I select this candidate, using EX-10's all-format measurement rather than the narrower runtime-only conclusion. Six delivered C2 reports (CR-2/3/4 and EX-7/9/10) converge on the K8/Vyper boundary. Other delivered seats propose distinct valid candidates: solc/viaIR questions (EX-5/6/8/12) and different-verb Evidence-ID questions (CR-1 and EX-11). Verdict peers disagree: CN-1, VZ-3, and CR-7 recommend EX-8; CN-2 recommends EX-11; CN-3 recommends CR-1; CN-4, CR-5, and CR-6 recommend EX-10; VZ-2 recommends EX-5; VZ-1 and CR-8 support the narrower five-output K8 comparison. These remain alternatives, not multiple entries to land for this one frozen move. I prefer EX-10 because it is the explicit frozen option (c), has the strongest repeated C2-seat support, and measures residuals across 31 output forms rather than only the narrower rechecks.

I independently re-ran the Vyper comparisons using a copied EX-10 evidence tree under `/var/tmp/vz4-r9-ex10.Od15Bf/evidence`. The source was `.ufo/waves/arc3-loop1-round8/claims/c3/EX-8/evidence/K8.vy`; source-copy check: `source-copy-equal=True bytes=580 sha256=62549f79b9efb6677e5b24769296e812ec321914816cb5e78699091fdfe6ea7`. Compiler: Vyper `0.4.3+commit.bff19ea2`, wrapper SHA-256 `615f792c6bc1bdf87cbc4612420a331ec108246d9debadbb3f3b9efa8209dd10`. To keep copied outputs and TMPDIR inside `/var/tmp`, I changed only the scratch copy of EX-10's driver to run from its scratch evidence directory and pass `K8.vy` as a relative source path. Successful invocation: `TMPDIR=/var/tmp/vz4-r9-ex10.Od15Bf/tmp PYTHONDONTWRITEBYTECODE=1 python3 /var/tmp/vz4-r9-ex10.Od15Bf/evidence/rederive.py`. The first copied run using an absolute `/var/tmp` source from the lane-root cwd hit `CompilerPanic: Invalid path` on `solc_json` and `archive`; the corrected scratch-only invocation then completed all formats. No peer directory was written by this recheck.

Fresh measurement summary (`/var/tmp/vz4-r9-ex10.Od15Bf/evidence/measure.txt`; full per-format comparison: `/var/tmp/vz4-r9-ex10.Od15Bf/evidence/compile/comparison.json`):

```text
formats-tested=31 compile-calls=124
bytecode: exits-zero=True cross-flag-raw-equal=True bytes=1377 sha256=e9e624957eecca5907bb429a7d99a639dfd3c94a04a473357172cdd3ff122dac
bytecode_runtime: exits-zero=True cross-flag-raw-equal=True bytes=1237 sha256=1dfe2699e61e8d82570dc3272d9679880e5a2fa765a0e4ce9169331ecedd939c
creation bytecode decoded: noopt=687 B b09398d8eb89f1ec1a73de9cbec27a54ce79d185094a4253a384cfffe62e2598; none=687 B same SHA-256; byte-identical=True
runtime decoded: noopt=617 B 1a7bf2cdc83e171f0a8485c894286ea59289de9bd45f1c124e1ed6888ef14ffc; none=617 B same SHA-256
ast: exits-zero=True cross-flag-content-equal=True cross-flag-raw-equal=False basis=canonical JSON values
annotated_ast: exits-zero=True cross-flag-content-equal=True cross-flag-raw-equal=False basis=canonical JSON values
archive: exits-zero=True cross-flag-content-equal=True cross-flag-raw-equal=False basis=archive member payloads; ZIP timestamps excluded
archive_member_count=7 archive_member_sha256_equal=True
```

The two AST raw encodings differ but canonical JSON compares equal. The two archive containers differ byte-for-byte, while all seven member payload hashes match; observed member timestamps vary across repeated calls. The evidence does **not** attribute every changed ZIP-container byte exclusively to timestamps. Thus the accurate boundary is: **deployable and runtime bytecode are byte-identical; compiler content is equal under the tested canonical-JSON/archive-member comparisons; not every raw compiler-format output is byte-identical.** The recheck's complete run and comparison files preserve the raw hashes and per-format statuses.

REA 6.7.0 / EVMole 0.9.3 on the two fresh runtimes returned the same eight `dispatch:"abi"` selectors — `2ae1431c, 364605a1, 9adbf691, 9b7c2962, bf3724af, cf35f823, d7531d91, d7b7913b` — and decoded SHA-256 `1a7bf2cdc83e171f0a8485c894286ea59289de9bd45f1c124e1ed6888ef14ffc`. The envelope marks the rows inferred, completeness unknown, and runtime execution not performed. A separate recheck of the inferred mutability found compiler ABI `view` versus REA-inferred `payable`; treat that as an inference discrepancy, not a compiler-ABI result. No deployment or runtime behavior was tested.

**One integration candidate:** EX-10's `.ufo/waves/arc3-loop1-round9/claims/c2/EX-10/evidence/entry-draft.md` proposes `corpus/knowledge/2026-10-19-arc3-r9-vyper-noopt-none-boundary.md` and EVM-map token `2026-10-19-arc3-r9-vyper-noopt-none-boundary`. It includes `source:`, `verified-at:`, and `recheck:` metadata (`.ufo/waves/arc3-loop1-round9/claims/c2/EX-10/evidence/entry-draft.md:5-7`); preserve the archive caveat above if integrating. Do not add the overlapping CR-2/3/4 or EX-7/9 Vyper drafts, nor a second unrelated candidate, as part of this single move. No C2 draft or map token is canonical yet.

I reran Command A from `SCORECARD.md:88-124` against immutable HEAD. Exact output:

```json
{"citation_resolved_rules":15,"coverage_score":10.0,"dangling":[],"depth_score":10.0,"knowledge_files":87,"mapped":87,"missing":[],"revision":"947091d6b6f52684faf9ca53adf94ff8a0f6b006","rule_blocks":15}
```

This is the before/integration baseline only. The expected 88 files / 88 mapped with empty missing/dangling lists is **UNVERIFIABLE** until one entry and matching map token land and Command A is rerun.

## C3 — live pointer and drift behavior

Read-only live config checks:

```text
$ grep -n 'rea-agents@' /home/vgpnk/.kimi-code/config.toml
4126:args = [ "-y", "rea-agents@6.7.0", "mcp" ]
$ grep -c 'rea-agents@' /home/vgpnk/.kimi-code/config.toml
1
$ wc -l /home/vgpnk/.kimi-code/config.toml
4150
```

The current config has one match at line 4126. The census gate grades `PROVINCE.md:18` (`~/.kimi-code/config.toml:4126`) `current-ok (pins 6.7.0)`, but its `live_pins()` anchor is a first-match search (`.ufo/gates/c1-census-v10.py:324-334`), not an instrument guarantee of uniqueness. Available read-only config snapshots place the same pin text at different physical lines (backups at 2915, 2932, 2940, 3227, 3298, 3298, and 3157); these observations establish line-coordinate movement, not the exact cause or chronology of each edit.

I independently exercised the actual `ptr_check()` against a synthetic config under an auto-removed `/var/tmp` directory; live config was untouched:

```text
baseline_line=4126 result=('ok', 'pins 6.7.0')
after_insert_old_line=4126 result=('stale', "line holds no rea-agents pin: '# synthetic fixture'")
after_insert_shifted_line=4127 result=('ok', 'pins 6.7.0')
```

This is a physical-line pointer: inserting material before the pin stales the old coordinate until it is re-anchored (`.ufo/gates/c1-census-v10.py:466-482`). The gate-level assertion is current now; the complete gate is not. The frozen C3 asks for the characterization to land as a corpus erratum or measured note on the receipt (`.ufo/waves/arc3-loop1-round9/claims-frozen.md:48-56`). This VZ verdict and peer claim files are not that canonical landing; it remains pending for authorized integration.

## Inventory, disagreement, and scope boundary

The frozen C2 roster has 12 seats; all main C2 reports are now present for EX-5 through EX-12 and CR-1 through CR-4. Current verdict artifacts are CN-1 through CN-4, CR-5 through CR-8, and VZ-1 through VZ-4; they disagree on one C2 candidate. The VZ-4 selection above is an adjudication, not evidence of unanimous verdict-seat consensus. Command A and the source tree remain unchanged at HEAD.

Before this write, Git showed the pre-existing `M .ufo/waves/arc2-loop1-round10/C3.md` and the existing untracked `.ufo/waves/arc3-loop1-round9/` tree. No tracked source, gate, corpus, PROVINCE, SCORECARD, SKILL, LOG, custody config, or peer artifact was edited; no commit or Git mutation was performed.
