# VZ-2 — Round 8 convergence verdict

**Review basis:** direct measurements from this worktree, whose Git `HEAD` is `904b724258fc9396a016bd9952b5cd40225fb7d8`. I did not use prior-round numeric results as evidence. The only round-8 file visible during the artifact inventory was `claims-frozen.md`; no c1/c2/c3 peer artifacts, candidate patch, receipt, or corpus entry were present to adjudicate. Conclusions below separate established base facts from unverified landing claims.

## C1 — `ptr_check` reachability and landing

**REPRODUCED — baseline collector blind spot.** `.ufo/gates/c1-census-v10.py` is 713 lines (`wc -l`) and SHA-256 `8002757078a685f515804fc6128ebf76b9925d2033be99a293621e18d14aecca` (`sha256sum`). At lines 511–514, `PTR.finditer()` is guarded by `if not occ`. A first-hand probe of the unit containing `PROVINCE.md:18` found a full path pointer (`~/.kimi-code/config.toml:3546`) and pin occurrences in that unit, so this guard skips the pointer. Current tree text is `PROVINCE.md:18`.

**VERIFIED — live and dead pointer behavior, re-derived through the gate helper.** `ptr_check()` is implemented at `.ufo/gates/c1-census-v10.py:465-481`. Direct calls using `live_pins()` returned:

```text
ptr_check(config.toml:3546)=stale; line holds no rea-agents pin: 'max_output_size = 64000'
ptr_check(config.toml:4126)=ok; pins 6.7.0
ptr_check(config.toml:999999)=unresolved; line 999999 beyond EOF (4150 lines)
```

The live config has 4,150 lines; line 4,126 is `args = [ "-y", "rea-agents@6.7.0", "mcp" ]`. The seeded out-of-range pointer is caught as `unresolved`, supporting the necessary fault-detection behavior, but this is not a measurement of a round-8 candidate patch.

**DISCREPANCY — the current gate baseline is not PASS.** Re-running `python3 .ufo/gates/c1-census-v10.py --json` on the current worktree returned exit 1 / `FAIL`, despite G21 having 14 rows and no frontier errors. The exact undeclared block is `SCORECARD.md:1776-1783`, triggered by `SCORECARD.md:1780` containing both `rea-agents@6.4.0` and `6.7.0` without a client token; the gate labels both assertions ambiguous. JSON contract remains 19 keys. This is present before any round-8 patch, so the frozen acceptance condition “PASS on the current tree” is **UNVERIFIABLE** absent a submitted patch and a demonstrated resolution or accounting for this separate blocker. I did not change the gate or any tracked file.

**UNVERIFIABLE — round-8 extension and seeded-fault scratch run.** No round-8 c1 patch text or scratch result was visible at review time; do not infer C1 landed from the direct helper calls above.

## C2 — live pin pointer and receipt

**VERIFIED — before-state discrepancy and fresh anchor.** `PROVINCE.md:18` currently points to `~/.kimi-code/config.toml:3546`. An independent byte-level read measured 4,150 config lines; line 3,546 is `max_output_size = 64000` (no pin), while line 4,126 is the live `rea-agents@6.7.0` args line shown above.

For the exact content bytes of line 4,126 **excluding the line terminator**, SHA-256 is `eb23737749a7dbd615db449daee491d821580fdb86df2660a92334df733b6cb1`. To make the newline convention explicit, SHA-256 **including its trailing LF** is `eb1c7da74fc5f870d7c6537e87beeaf043491b5cdd00ee7a2f65e426d9f2b675`.

**UNVERIFIABLE — re-anchor/receipt landing and same-commit condition.** The worktree still has the old `:3546` pointer, and no round-8 receipt or c2 peer artifact was visible. The measured hash is a fresh audit result, not evidence that a receipt was committed with C1.

## C3 — corpus coverage

**VERIFIED — baseline re-measurement.** I executed the `SCORECARD.md:88-124` Command A algorithm directly against immutable Git objects at both current `HEAD` (`904b724258fc9396a016bd9952b5cd40225fb7d8`) and the frozen prior-work commit (`7deeb36`). Both returned `knowledge_files=86`, `mapped=86`, `missing=[]`, `dangling=[]`, `rule_blocks=15`, `citation_resolved_rules=15`. Current-HEAD JSON:

```json
{"citation_resolved_rules":15,"coverage_score":10.0,"dangling":[],"depth_score":10.0,"knowledge_files":86,"mapped":86,"missing":[],"revision":"904b724258fc9396a016bd9952b5cd40225fb7d8","rule_blocks":15}
```

**UNVERIFIABLE — one-Unknown closure.** No round-8 corpus draft/entry or map-token update was visible, so the required `86 → 87` result and evidence cited inside the new entry are not established.

## Overall disposition

The frozen preconditions are partly re-confirmed: the C1 collector blind spot is real; `:3546` is stale and live `:4126` is current; and Command A currently measures 86/86. The requested C1/C2/C3 landings cannot be adjudicated from the files available at review time. In particular, the current-tree gate already fails on the undeclared SCORECARD block above, which must be considered when any C1 candidate reports clean PASS.
