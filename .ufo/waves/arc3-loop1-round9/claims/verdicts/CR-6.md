# CR-6 — Round-9 verdict and convergence

Measured revision: `git rev-parse HEAD` → `947091d6b6f52684faf9ca53adf94ff8a0f6b006`.

Scope: frozen verdict/convergence roster (`claims-frozen.md:60-63`). This file is the only CR-6 deliverable. I did not change source, corpus, gate, custody, or peer-seat artifacts, and made no Git mutation. The lane worktree already had `M .ufo/waves/arc2-loop1-round10/C3.md` and an untracked `.ufo/waves/arc3-loop1-round9/` at the start; those were preserved. Scratch experiments were under `/var/tmp`.

## Per-claim verdicts

### C1 — freshness

**Live archive count: REPRODUCED. Frozen gate-PASS condition: DISCREPANCY. Row repair: NOT LANDED.**

At HEAD, `PROVINCE.md:50` still says `1556 signed archives`. I independently counted direct-child regular files and rechecked the other potentially perishable row item:

```text
$ python3 - <<'PY'
from pathlib import Path
p = Path('/var/cache/pacman/pkg')
fs = [x for x in p.iterdir() if x.is_file()]
a = [x for x in fs if x.name.endswith('.pkg.tar.zst')]
s = [x for x in fs if x.name.endswith('.pkg.tar.zst.sig')]
print(f'archive_regular_files={len(a)}')
print(f'signature_regular_files={len(s)}')
print(f'delta_to_PROVINCE_1556={len(a)-1556:+d}')
PY
archive_regular_files=1350
signature_regular_files=1350
delta_to_PROVINCE_1556=-206

$ pacman -Q jq
jq 1.8.2-1
$ pacman -Qkk jq
jq: 25 total files, 0 altered files
$ sha256sum /usr/bin/jq
... e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806  /usr/bin/jq
$ tar -xOf /var/cache/pacman/pkg/jq-1.8.2-1-x86_64.pkg.tar.zst usr/bin/jq | sha256sum
... e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806  -
```

The `−206` delta is arithmetic against the dated value in `PROVINCE.md:50`, not an independently reconstructed historical cache. Matching `.sig` filenames do not verify cryptographic signatures. The installed `jq` hash equals the cached archive member in this recheck. `available:true in live session` remains **UNVERIFIABLE as current** without a live `binary_session` observation. The candidate same-line patch text remains a draft; PL-4 dates only the archive phrase (`claims/c1/PL-4.md:24-29`), while EX-4 dates the availability observation and the fresh jq check too (`claims/c1/EX-4.md:23-38`). Prefer a single row replacement that does not leave those volatile statements appearing current. Peer measurements agree on the archive count and delta (including `claims/c1/RV-4.md:7-18`).

The required gate condition is independently false at this HEAD. `python3 .ufo/gates/c1-census-v10.py --json` returned exit 1 and:

```text
"verdict": "FAIL"
counts: PROVINCE.md 162 lines / 6 loci; SCORECARD.md 1870 lines / 11 loci; SKILL.md 413 lines / 2 loci
undeclared: SCORECARD.md block 1833-1839; pin 6.7.0 at line 1834 (scope null; no client token in clause)
frontier_rows=14; frontier_errors=[]; g2_ok=true
```

The extra SCORECARD block lies beyond the declared SCORECARD census end at `.ufo/gates/c1-census-v10.py:276` (line 1813). This is separate from the PROVINCE count. C1's frozen requirement that the instrument still read PASS is therefore **not met**; no row-only patch can be reported as a gate pass.

### C2 — coverage

**Compiler boundary: REPRODUCED for the measured K8/Vyper pair. Corpus landing and the frozen 88/88 coverage after-state: UNVERIFIED / PENDING.**

I independently recompiled the K8 source (SHA-256 `62549f79b9efb6677e5b24769296e812ec321914816cb5e78699091fdfe6ea7d`) with Vyper `0.4.3+commit.bff19ea2` (executable SHA-256 `615f792c6bc1bdf87cbc4612420a331ec108246d9debadbb3f3b9efa8209dd10`). Two builds per spelling compared equal; cross-spelling `cmp` succeeded for `bytecode`, `bytecode_runtime`, `abi`, `method_identifiers`, and `settings`. Both settings say `optimize: none`. The runtime text hash was `1dfe2699e61e8d82570dc3272d9679880e5a2fa765a0e4ce9169331ecedd939c` (1,237 bytes); decoded runtime hash was `1a7bf2cdc83e171f0a8485c894286ea59289de9bd45f1c124e1ed6888ef14ffc` (617 bytes). REA 6.7.0 / EVMole 0.9.3 returned 8 functions for each input, matching the compiler selector set and decoded runtime identity. This is limited to the source, tool build, outputs, and static analyzer measured; it is not a universal Vyper rule or runtime-execution result. The independently inspected R8 entry already records runtime equivalence (`corpus/knowledge/2026-10-19-arc3-r8-vyper-optimizer-dispatch-shapes.md:11`); the R9 residual is additional compiler-output coverage.

Command A at immutable HEAD (`SCORECARD.md:88-124`) was re-run and returned:

```json
{"citation_resolved_rules":15,"coverage_score":10.0,"dangling":[],"depth_score":10.0,"knowledge_files":87,"mapped":87,"missing":[],"revision":"947091d6b6f52684faf9ca53adf94ff8a0f6b006","rule_blocks":15}
```

No corpus entry or EVM map token is landed, and no post-landing 88/88 result exists. C2's end-to-end coverage move is not complete until one entry and its matching token land and Command A is rerun on that revision.

**Integration recommendation: select only EX-10's Vyper output-boundary draft**, destination `corpus/knowledge/2026-10-19-arc3-r9-vyper-noopt-none-boundary.md`, token `2026-10-19-arc3-r9-vyper-noopt-none-boundary` (`claims/c2/EX-10/evidence/entry-draft.md:1-7`). It is the most informative surviving Vyper residual: EX-10 reports a 31-format sweep, raw equality in 28 formats, and distinguishes equal JSON values / archive-member payloads from non-identical AST renderings / ZIP containers (`claims/c2/EX-10/evidence/entry-draft.md:13-17`). That broader result complements my direct five-output recompile. **Before landing, normalize the count claims to the corpus rule** (`/home/vgpnk/.kimi-code/skills/shokunin/protocol/CORPUS.md:33-37`): for example, the 31-format, 124-run, 28/31, and seven-member counts must each be written with their counting command and date. The EX-10 draft as read does not yet use that required count form.

Peer reconciliation: all 12 C2 seat reports are present. Six (CR-2, CR-3, CR-4, EX-7, EX-9, EX-10) measure the Vyper boundary; alternatives propose SQLite (CR-1), solc 0.8.28/0.8.36 viaIR (EX-5/EX-12), viaIR fallback (EX-6/EX-8), or Go Evidence-ID behavior (EX-11). The verdicts disagree on one landing: CN-1, CR-7, and VZ-3 prefer EX-8; CN-2 prefers EX-11; CN-3 prefers CR-1; CN-4 prefers EX-6; VZ-2 prefers EX-5; CR-5 and VZ-4 select EX-10; VZ-1 favors the Vyper creation-bytecode residual; CR-8 supports the bounded Vyper residual (`claims/verdicts/CN-1.md:46-73`, `CN-2.md:63-96`, `CN-3.md:17-25`, `CN-4.md:38-83`, `CR-5.md:40-93`, `CR-7.md:40-63`, `CR-8.md:82-110`, `VZ-1.md:44-68`, `VZ-2.md:67-94`, `VZ-3.md:36-48`, `VZ-4.md:59-91`). CN-4 and VZ-2 argue the Vyper alias is already resolved, while VZ-1 and CR-5 support measuring a residual beyond R8. The R8 record explicitly re-runs runtime output and names settings/ABI/method identifiers; it does not report `bytecode` creation-output comparison (`corpus/knowledge/2026-10-19-arc3-r8-vyper-optimizer-dispatch-shapes.md:7-17`). I independently compared creation `bytecode` as well as those four outputs, and EX-10's broader sweep records the remaining raw-output distinctions across formats. I therefore retain EX-10 as the one recommended candidate under frozen option (c), not as peer consensus. Do not co-land any competing candidate or duplicate Vyper token; Command A must still verify the selected single entry and map token after landing.

### C3 — calibration

**Live pointer disposition: REPRODUCED as current. Drift behavior: REPRODUCED in an isolated fixture. Full-gate status: DISCREPANCY. Requested receipt/corpus landing: PENDING.**

A filtered live search returned one match at `/home/vgpnk/.kimi-code/config.toml:4126:args = [ "-y", "rea-agents@6.7.0", "mcp" ]`. I independently imported the current gate and ran its pointer helper against the live file:

```text
live_anchors={'devin': '6.5.0', 'omp': '6.5.0', 'kimi': '6.7.0'}
PROVINCE.md:18 pointer=('ok', 'pins 6.7.0')
```

The gate maps pointer-helper `ok` to `current-ok` (`.ufo/gates/c1-census-v10.py:538-544`). The complete `python3 .ufo/gates/c1-census-v10.py --json` run still exits 1 for the separate SCORECARD block `1833-1839` / line 1834 documented under C1; this does not make the targeted PROVINCE pointer stale.

I exercised the actual `ptr_check()` with a minimal temporary `~/.kimi-code/config.toml` under `/var/tmp`:

```text
baseline line2=('ok', 'pins 6.7.0')
after insertion old line2=('stale', "line holds no rea-agents pin: '[mcp_servers.rea]'")
after insertion moved line3=('ok', 'pins 6.7.0')
duplicate same-version line4=('ok', 'pins 6.7.0')
```

This confirms a literal-line, version comparison: inserting a line before the pin stales the old address, while re-anchoring succeeds. `live_pins()` takes a first regex match (`.ufo/gates/c1-census-v10.py:324-334`); `ptr_check()` examines the nominated line and compares its version with that anchor (`:466-482`). The checker does not bind the citation to a stanza, enforce uniqueness, or validate the receipt's line hash. Duplicate acceptance is a synthetic result, not a claim that the live file has duplicates.

I also independently exercised `classify()` with a synthetic Kimi config pinned to `6.7.1`, retaining the current Province text at line 18 (HOME and config existed only under `/var/tmp`). The gate returned:

```text
live_kimi=6.7.1
block=15-26 disposition=UNRESOLVED
line18 pin '6.7.0' -> historical (inline marker)
line18 ptr '~/.kimi-code/config.toml:4126' -> current-ok (pins 6.7.1)
```

This is a calibration caveat: the line-18 `historical` marker can suppress a mismatching Province version as historical while the pointer independently follows the live target version. It is a synthetic mismatch, not a claim about the current live config. The relevant marker detection and mismatch classification are `.ufo/gates/c1-census-v10.py:315,518-521,559-564`.

The receipt already notes that the pointer is perishable (`.ufo/receipts/arc3-loop1-round8-kimi-rea-line.txt:3-10`), but that prior note does not contain the insertion/duplicate or marker-masking characterization. The frozen request asks for the characterization to land as a corpus erratum or measured receipt note (`claims-frozen.md:44-56`). Current C3 reports characterize the result in seat artifacts; no corpus or receipt update was made, so that exact placement is **not verified as complete** within CR-6's write boundary. Historical line positions are also bounded: available snapshots show movement through 2940, 3227, 3298, and 3157 before the current 4126, but the cited intermediate 3546 is not present in the available snapshot set (`claims/c3/SC-1.md:38-62`). Do not treat the full chronology or the cause of each movement as independently proven.

Peer reconciliation: the C3 seats and verdicts agree on the live line, targeted current result, positional insertion behavior, and separate whole-gate FAIL; SC-3, VZ-1, CR-7, and VZ-4 also record the synthetic inline-marker caveat (`claims/c3/SC-3.md:14-23`, `claims/verdicts/VZ-1.md:50-56`, `CR-7.md:64-84`, `VZ-4.md:93-116`). The receipt/corpus placement remains pending.

## Current evidence boundary

At this final inventory pass, all 12 C2 seat reports and all 12 verdict-seat artifacts (CN-1..4, CR-5..8, VZ-1..4, including this CR-6 file) are present. C1/C3 technical facts converge, but the gate and canonical landing conditions remain discrepancies or pending work. C2 has a reproduced bounded result, conflicting candidate choices, and no integrated coverage result. No scalar round verdict is assigned here.
