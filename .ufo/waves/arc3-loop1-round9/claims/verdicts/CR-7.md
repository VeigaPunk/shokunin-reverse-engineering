# CR-7 — C1–C3 verdict and convergence

Measured base: `947091d6b6f52684faf9ca53adf94ff8a0f6b006`. This is a verdict artifact; the Province row, corpus, coverage map, gate, receipt/config custody, scorecard, skill, log, and other seats' artifacts remain read-only.

## Summary

- **C1 — PARTIAL / DISCREPANCY.** The live archive count is 1,350 (−206 from the dated 1,556 record), and the other row items were censused. The installed-`jq` byte identity rechecks; current `available:true in live session` does not. The required gate PASS is not reproduced: the instrument exits 1 on an unrelated undeclared `SCORECARD.md:1834` locus. No row patch was landed.
- **C2 — REPRODUCED, bounded; coverage landing UNVERIFIABLE.** A fresh independent compile/probe of EX-6 confirms the explicitly open r6 viaIR/fallback case for one synthetic source/settings point. The proposed entry and map token are absent and Command A remains 87/87. Recommendation: integrate only one candidate; EX-8 is the best match to the named r6 question because it compares fallback and no-fallback carriers and includes a `recheck:` recipe. EX-6 is independent corroboration, not a second entry.
- **C3 — REPRODUCED at assertion level; aggregate DISCREPANCY.** The sole live pin is at line 4126 and the pointer is `current-ok`. A synthetic insertion makes the literal old line pointer stale; a synthetic version change exposes an inline-marker masking edge. The full gate still fails at `SCORECARD.md:1834`; no receipt/corpus characterization was landed here.

## C1 — current archive row and census gate

`PROVINCE.md:40` dates the Core surface survey to 2026-10-13; `PROVINCE.md:50` still states `1556 signed archives` without an as-of qualifier. The historic value is labelled a 2026-10-13 snapshot in `corpus/knowledge/2026-10-13-pacman-packages.md:73-83`; that old cache state is not independently reconstructable now.

Fresh read-only cache pairing check:

```text
archives=1350 matching_signatures=1350 missing_signatures=0 orphan_signatures=0
current_minus_recorded=1350-1556=-206
```

This is filename/sidecar pairing, not cryptographic verification of every signature. The remaining row census:

- `available:true in live session` — **UNVERIFIABLE as current state**; no live REA MCP session was available for a new probe.
- Installed `jq` byte identity — **VERIFIED in this recheck**: `pacman -Q jq` → `jq 1.8.2-1`; `pacman -Qkk jq` → `jq: 25 total files, 0 altered files`; installed `/usr/bin/jq` and the cached archive member both hash to `e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806`.
- `.MTREE per-file sha256`, `pacman -Qkk verify`, and `binary_session {}` describe a format, procedure, and probe shape; this row contains no other live count/version scalar. The PROVINCE file remains 162 lines.

Fresh `python3 .ufo/gates/c1-census-v10.py` run (gate SHA-256 `e4fb740cb8153f15c623f3b9f7ca781e270053b0557be5393010359b2213b7b4`) ended:

```text
-- UNDECLARED (1) --
  SCORECARD.md block 1833-1839 [scope None]
      :1834 [pin] None=6.7.0 -> AMBIGUOUS (no client token in clause)
VERDICT: FAIL  (stale=0 ambiguous=0 undeclared=1 unresolved=0)
gate_exit=1
```

The gate's declared SCORECARD range ends at line 1813 (`.ufo/gates/c1-census-v10.py:274-276`), so this failure is separate from the PROVINCE row and cannot be represented as a passing post-patch result. EX-1's row census and proposed line-neutral patch are consistent with the live facts, but the patch is not landed and its scratch gate still has the same failure (`claims/c1/EX-1.md:38-80`).

## C2 — bounded candidate and one-entry integration

The r6 entry explicitly leaves “viaIR carriers with `fallback()`” unmeasured, including the SUB-leg/fall-through interaction (`corpus/knowledge/2026-10-19-arc3-r6-viair-dispatch-shape.md:30`). I independently compiled EX-6's read-only `ViaIRFallback.sol` to unique `/var/tmp` output using its `compile.js`, walked that fresh runtime, and called the already cached REA 6.7.0 CLI with `TMPDIR` under `/var/tmp`.

Fresh compile output:

```text
solc=0.8.37+commit.f401782d.Emscripten.clang
runtime_bytes=366 runtime_sha256=2948d578ae460119f777eb379febc2738dbec14d03c76d5f100777c9552ce6fc
creation_bytes=392 creation_sha256=a24cb1651e78dd159425d5b27c9ba513b50b0401f5bcf3589f259b0a70d0ba9e
ABI entry kinds=[fallback,function,function,function,receive]
method identifiers={"alpha()":"db1d0fd5","load()":"86d5c4be","store(uint256)":"6057361d"}
```

REA returned those same three ordinary selectors, with decoded runtime SHA-256 `2948d578ae460119f777eb379febc2738dbec14d03c76d5f100777c9552ce6fc`; it returned no fallback/receive function rows. The fresh opcode walk has the final selector leg `PUSH4 0xdb1d0fd5; SUB; PUSH2 0x000e; JUMPI`. At `0x000e`, empty calldata branches to the receive path at `0x0087`; nonempty calldata continues into the fallback path. This is a static source/byte interpretation, not executed contract behavior. REA classifies its function recovery as inferred, `discovery_completeness=unknown`, and `runtime_execution=not-performed`.

This reproduces EX-6's narrow technical finding, not a universal solc or fallback rule. The canonical coverage result is still **UNVERIFIABLE**: the proposed `corpus/knowledge/2026-10-19-arc3-r9-viair-fallback-dispatch.md` and EVM-map token `2026-10-19-arc3-r9-viair-fallback-dispatch` are not present (no matching destination file or map token). I reran Command A from `SCORECARD.md:88-124` against immutable HEAD:

```json
{"citation_resolved_rules":15,"coverage_score":10.0,"dangling":[],"depth_score":10.0,"knowledge_files":87,"mapped":87,"missing":[],"revision":"947091d6b6f52684faf9ca53adf94ff8a0f6b006","rule_blocks":15}
```

Do not call this 88/88 or a post-landing closure. The submitted candidates are alternatives, not multiple entries to land for one frozen C2. The R8 entry records the Vyper option equivalence for runtime/ABI/method-identifiers/settings (`corpus/knowledge/2026-10-19-arc3-r8-vyper-optimizer-dispatch-shapes.md:11`); CR-2 reports creation-bytecode comparison as an additional residual, so that proposal is not wholly redundant. Other verdict peers select K8 creation-bytecode, EX-8 fallback, EX-11 Go, or CR-1 SQLite (`VZ-1.md`, `VZ-3.md`, `CN-2.md`, `CN-3.md`, `CR-8.md`). My recommendation is one EX-8 entry/token: its peer artifact compares no-fallback and payable-fallback variants of the named r6 shape and supplies a recheck recipe (`claims/c2/EX-8.md:3-20`; draft `claims/c2/EX-8/evidence/draft-corpus-entry.md:1-17`). EX-6, independently rederived here, corroborates that same narrow area; do not land both as separate closures. The other proposed C2 domains remain alternatives, not a consensus landing decision.

## C3 — pin-pointer drift and gate disposition

A targeted search of `/home/vgpnk/.kimi-code/config.toml` found exactly one `rea-agents@` occurrence:

```text
/home/vgpnk/.kimi-code/config.toml:4126:args = [ "-y", "rea-agents@6.7.0", "mcp" ]
```

The live gate grades `PROVINCE.md:18`'s Kimi pin and pointer `current-ok` (pointer reason: `pins 6.7.0`); the containing block is `info`, not itself a PASS result. The aggregate gate remains the C1 failure at `SCORECARD.md:1834`. Gate source confirms `live_pins()` takes the first regex match (`.ufo/gates/c1-census-v10.py:324-334`) and `ptr_check()` reads the literal physical line and checks the version (`:466-482`).

Controlled synthetic checks used only a temporary config under `/var/tmp`:

```text
baseline_ptr=('ok', 'pins 6.7.0')
after_insert_old_ptr=('stale', "line holds no rea-agents pin: '# insertion before pin'")
after_insert_rekeyed_ptr=('ok', 'pins 6.7.0')
```

A separate synthetic change set the config pin to 6.7.1 while leaving the Province text unchanged. The gate classified the old `PROVINCE.md:18` pin assertion as `historical (inline marker)` and the pointer as `current-ok (pins 6.7.1)` (`INLINE_MARKER` and classification logic: `.ufo/gates/c1-census-v10.py:315,559-563`). This is a synthetic masking edge, not a live config mismatch. It shows the pointer is positional and version-checked, not self-reanchoring; current uniqueness is an observed file property, not a rule enforced by `live_pins()`.

The requested characterization is measured here, but this seat did not modify the official receipt or corpus entry. Frozen C3's canonical landing condition therefore remains outstanding for integration. The twelve C3 reports (`EX-13..16`, `SC-1..4`, `RV-5..8`) agree on the current line, assertion-level `current-ok`, and separate aggregate FAIL; SC-3's synthetic inline-marker edge matches this independent reproduction.

## Peer convergence and write boundary

At this check, delivered verdict peers were VZ-1, VZ-3, CN-2, CN-3, and CR-8. They agree on the C1 live-count/gate result and C3 pointer-vs-aggregate distinction, but disagree on which single C2 candidate to land; that is candidate selection, not disagreement about the measured 87/87 pre-integration state. CR-8's earlier “no sibling verdict files” inventory is a time-of-check statement; the five peer files above are now present.

Only this CR-7 artifact was written by this seat. No source, corpus, gate, receipt, custody, scorecard, skill, or log file was changed; no Git mutation was performed. The pre-existing `.ufo/waves/arc2-loop1-round10/C3.md` modification was left untouched.