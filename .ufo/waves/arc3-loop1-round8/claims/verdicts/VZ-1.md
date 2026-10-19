# VZ-1 — arc3-loop1-round8 reconciliation verdict

Independent verdict seat, chain `verdicts`. All measurements below were re-derived from the current checkout/live config; peer reports were used only for reconciliation, not as evidence. Git was read-only. This artifact is the only file written by this seat.

## Per-claim rulings

- **C1 operability — REPRODUCED blind spot; DISCREPANCY on current-tree PASS; candidate landing UNVERIFIABLE.** The pointer collector does not reach `ptr_check()` when a matching unit already has a pin/version (`.ufo/gates/c1-census-v10.py:511-514`). On the present `PROVINCE.md:18`, I independently observed a full PTR match and a pin match but no pointer assertion. Direct `ptr_check()` accepts the actual live line `:4126` and rejects the dead re-key `:999999`. However, the unmodified gate currently exits 1 / FAIL for an unrelated undeclared SCORECARD block (`SCORECARD.md:1776-1783`), so a C1 patch must account for this before claiming its required clean PASS. No R8 C1 patch or seeded-fault artifact was present when I checked `claims/c1/`; the actual extension and seeded-fault result remain UNVERIFIABLE.
- **C2 freshness — VERIFIED live line and receipt hash; CORRECTED pointer proposal; same-commit/shared-receipt landing UNVERIFIABLE.** `PROVINCE.md:18` still has `:3546`; the live Kimi pin is at `~/.kimi-code/config.toml:4126`. The replacement changes only the pointer digits on line 18 (198 characters before and after; zero line delta). I independently computed the live line hash and confirmed it matches the R8 seat receipts. EX-3, EX-4, EX-5 and CR-1 agree on the pointer and hash. Their diffs/receipts are proposals/evidence, not a landed same-commit change. `.ufo/receipts/` does not exist in this checkout, so a shared durable receipt is still outstanding.
- **C3 coverage — baseline VERIFIED; requested closure UNVERIFIABLE / not yet delivered.** Command A yields 86 knowledge files, all 86 mapped, no missing/dangling tokens at both HEAD and the measured work commit. The `claims/c3/` directory currently has research scripts and partial output, but no corpus-entry draft (`claims/c3/**/*.md` returned no matches); thus neither the required 86→87 change nor a closed Unknown is established.

## First-hand measurements

Revision and gate identity:

```text
$ git rev-parse HEAD
904b724258fc9396a016bd9952b5cd40225fb7d8
$ git rev-parse '7deeb36^{commit}'
7deeb36045209f3fbeb4460edd7aef5b5270af22
$ wc -l .ufo/gates/c1-census-v10.py
713 .ufo/gates/c1-census-v10.py
$ sha256sum .ufo/gates/c1-census-v10.py
8002757078a685f515804fc6128ebf76b9925d2033be99a293621e18d14aecca  .ufo/gates/c1-census-v10.py
```

Direct import/classification and live pointer checks:

```text
live={'devin': '6.5.0', 'omp': '6.5.0', 'kimi': '6.7.0'}
PROVINCE.md:18 PTR_matches=['~/.kimi-code/config.toml:3546']
PROVINCE.md:18 PIN_matches=['6.7.0']
classify_pointer_assertions=[]
ptr_check(~/.kimi-code/config.toml:4126)=('ok', 'pins 6.7.0')
ptr_check(~/.kimi-code/config.toml:3546)=('stale', "line holds no rea-agents pin: 'max_output_size = 64000'")
ptr_check(~/.kimi-code/config.toml:999999)=('unresolved', 'line 999999 beyond EOF (4150 lines)')
```

The direct unmodified command `python3 .ufo/gates/c1-census-v10.py --json` exited 1. Its compacted output was:

```json
{"verdict":"FAIL","frontier_rows":14,"frontier_errors":[],"current_ok_per_file":{"PROVINCE.md":17,"SCORECARD.md":14,"SKILL.md":3},"pointer_assertions":[],"undeclared":[{"file":"SCORECARD.md","block":"1776-1783","asserts":[{"kind":"pin","value":"6.4.0","line":1780,"disp":"AMBIGUOUS"},{"kind":"bare","value":"6.7.0","line":1780,"disp":"AMBIGUOUS"}]}]}
```

C2 live-line receipt measurement (SHA-256 scope: exact line content, excluding the terminator):

```text
file=/home/vgpnk/.kimi-code/config.toml line=4126 bytes=b'args = [ "-y", "rea-agents@6.7.0", "mcp" ]\n'
line_content_sha256_no_newline=eb23737749a7dbd615db449daee491d821580fdb86df2660a92334df733b6cb1
line_record_sha256_with_newline=eb1c7da74fc5f870d7c6537e87beeaf043491b5cdd00ee7a2f65e426d9f2b675
line_count=4150
```

The proposed `PROVINCE.md:18` substitution was checked in memory: line length `198 → 198`, line-count delta `0`, and only the `:3546` pointer token changes to `:4126`. Receipt copies with the same content hash are present at `claims/c2/EX-3/receipt.txt:1-10` and `claims/c2/CR-1/evidence/live-config-receipt.txt:1-18`; EX-4/EX-5 report the matching hash as well. The tracked PROVINCE line remains unchanged in this checkout.

Command A was executed with the recipe at `SCORECARD.md:88-124` against both resolved revisions:

```json
{"citation_resolved_rules":15,"coverage_score":10.0,"dangling":[],"depth_score":10.0,"knowledge_files":86,"mapped":86,"missing":[],"revision":"904b724258fc9396a016bd9952b5cd40225fb7d8","rule_blocks":15}
{"citation_resolved_rules":15,"coverage_score":10.0,"dangling":[],"depth_score":10.0,"knowledge_files":86,"mapped":86,"missing":[],"revision":"7deeb36045209f3fbeb4460edd7aef5b5270af22","rule_blocks":15}
```

## Peer reconciliation and remaining integration work

- **C1:** no R8 C1 peer artifact was available in `claims/c1/` at final inspection. The direct collector/anchor checks above confirm the baseline defect and expected live/dead pointer classifications, but do not substitute for a candidate patch run on scratch with the refreshed pointer. Separately, the current gate FAIL at `SCORECARD.md:1776-1783` must be reconciled before accepting a required whole-gate PASS.
- **C2:** EX-3, EX-4, EX-5 and CR-1 independently propose the same line-neutral `3546 → 4126` update and same content hash. This seat independently reproduces the live line and digest. Their own-seat receipt files do not demonstrate registration at a shared receipt path or co-landing with C1.
- **C3:** available files were `claims/c3/EX-7/characterize.py`, `EX-8/rederive.sh`, `EX-9/rederive.py` and `EX-9/rederive-output.txt`; the latter currently contains only `keccak_vectors=2/2` and a source hash (`:1-2`), not a result set or corpus entry. No Unknown closure is accepted from these artifacts yet.

No gate, `PROVINCE.md`, corpus entry/map, `SKILL.md`, `SCORECARD.md`, `LOG.md`, or receipt outside this seat's artifact directory was changed.