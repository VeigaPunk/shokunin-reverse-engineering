# R35Audit21 — r4-07 held `.jsc` ground comparison

Scope: read-only comparison of the prior held Typora `.jsc` ground against current Round-35 C1 target and fetched-source claims. No production/corpus/counter/plan/claims files or VCS state changed; this report is the sole write.

## Finding

**Observed in the lane's r4-07 record:** `corpus/knowledge/2026-10-13-r4-07-jsc-bytecode.md` identifies Typora 1.14.9 `atom.compiled.dist.jsc` as a V8 14.8 code-cache, SHA-256 `6a0cb7b32270498ed190c589ca29c990a0e4b5f06f0cd6a5516e19a715c2dfe9`, 388,080 bytes. It records `ELECTRON_RUN_AS_NODE=1 npx -y electron@42.2.0` accepting the cache (`cachedDataRejected=false`) and `--print-bytecode` yielding 530,020 bytes/116 function blocks on one run; its appended r5 erratum explicitly records rerun variability (531,851 bytes/115 blocks). The entry therefore supports a real, already-held bytecode/disassembly baseline, but does not itself establish readable source mapping.

**Observed in the captured jsc2js README** (`.ufo/waves/round-35/prep/jsc-sources/jsc2js-readme.md`, English lines 115–157): the project documents two components—a patched `d8` with `loadjsc()` to print Ignition bytecode, and customized View8 translating disassembly to *approximate* JavaScript. It explicitly warns identifiers/control flow may differ and reconstruction is not exact (lines 205–208). This is technically distinct from r4-07's already-held Electron disassembly path and provides evidence for the missing mapper stage, not proof that this mapper successfully reconstructs this particular Typora artifact.

**Observed in current Round-35 capture:** `releases-page1.json` is 100 objects and page 7 is 77 objects. Filtering each captured page's `tag_name` for `^1[34]\\.` returned `[]`; filtering page 1 for `14.8` also returned `[]`. Thus these two retained pages do not demonstrate a matching V8 14.8 release. The captures are not a complete release inventory: page 1 is newest-first through August 2026 and page 7 contains older 12.x tags; intervening pages are not present here. No conclusion about all upstream releases or current live availability follows.

## First falsifications / limits

- The tempting statement “r4-07 already solved `.jsc` → source mapping” is **falsified by scope**: its record says the output is low-level Ignition disassembly and calls View8/jsc2js a next step. It is valid held ground for compatible cache loading and disassembly only.
- The prep README's general support/version-compatibility claims are repository-authored documentation. They do not verify a matching patched `d8` for V8 `14.8.178.14`, a successful run against the r4-07 hash, or View8 fidelity on Typora's cache.
- The release capture alone cannot justify saying no matching release exists: only pages 1 and 7 were retained. It does falsify any assertion that these captures themselves show a V8 14.8 tag.
- No fresh run, fetch, or source-tree inspection was performed. REA capability, complete upstream release status, output accuracy, and successful mapping of the held asset remain unverified here.

## Evidence / commands and output

Commands executed (read-only):

1. `grep 'r4-07|r4-7|R4-07|R4-7'` over lane located the held entry and the PROVINCE frontier references.
2. `read corpus/knowledge/2026-10-13-r4-07-jsc-bytecode.md` — inspected the full held record and run log, including lines 117–146 and erratum lines 212–220.
3. `read .ufo/waves/round-35/prep/jsc-sources/jsc2js-readme.md` — inspected README; printed claims at lines 115–157 and limitations at 199–208.
4. `read .../releases-page1.json?q=[.[] | .tag_name | select(test("^1[34]\\."))]` → `[]`; analogous page 7 query → `[]`; page1 `startswith("14.8")` query → `[]`.
5. `read .../releases-page1.json?q=keys` → array indices 0–99; page7 → indices 0–76; type query confirmed 100 and 77 objects, respectively.
6. `grep 'S106|S125|S129' corpus/SOURCES.md` — S106 is present; S125/S129 are not in the current worktree registry at inspection. This is consistent with the staged-row status and is not a judgment on later wave edits.
7. `glob .../merge/*` → path not found; no `merge/kaidoku/` subtree exists in the lane. This confirms the round-plan note that the source-theme name is absent here, not that the topic is absent from other repositories.
8. `grep 'jsc|Frontier' PROVINCE.md` — Frontier still names `.jsc`→source mapping as future View8/jsc2js-style work (lines 146–148); adjacent table records r4-07 disassembly (line 129).

## Advisory

Retain r4-07 as the ground control for V8 cache acceptance and Ignition disassembly, not as evidence that readable-source mapping was achieved. C1's proposed mapper-contract/release-inventory entries address a distinct frontier gap, but the captured docs/releases do not establish an end-to-end mapping result on the held Typora bytes. Avoid repeating “current matching release exists” or “mapper validated on target” without a matching pinned release artifact and target-specific run. No claim predicate or scope change recommended.

Report: `.ufo/waves/round-35/w1/R35Audit21.md`
