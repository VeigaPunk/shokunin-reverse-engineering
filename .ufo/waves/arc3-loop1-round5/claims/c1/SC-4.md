# SC-4 — C1 calibration correctness sweep

**Verdict:** All six frozen C1 checks were re-derived on immutable commits or the landed tree. All substantive measurements reproduced; one supplied custody command spelling is unsupported, and the supported subcommand passes. No corpus or custody claim correction was needed.

**Tree:** HEAD `71668ccd2c920b907672b5c40efaafe7c2e75bd1`.

## (a) Command A — REPRODUCED

Replayed the `SCORECARD.md:88-124` recipe with `git show`/`git ls-tree` independently at all six supplied commit IDs. Exact JSON output:

```json
{"citation_resolved_rules": 13, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 82, "mapped": 82, "missing": [], "revision": "fbbbd45", "rule_blocks": 13}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 82, "mapped": 82, "missing": [], "revision": "28aa7a9", "rule_blocks": 14}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 83, "mapped": 83, "missing": [], "revision": "5be4a26", "rule_blocks": 14}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 83, "mapped": 83, "missing": [], "revision": "c418be0", "rule_blocks": 14}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 84, "mapped": 84, "missing": [], "revision": "40de383", "rule_blocks": 14}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 83, "mapped": 83, "missing": [], "revision": "520341d", "rule_blocks": 14}
```

Full object IDs resolved locally: `fbbbd45` → `fbbbd45c1769a05ec644964d254c24655ae27c84`; `28aa7a9` → `28aa7a98683287afa4ccbad50f1d28bcf89ba7b1`; `5be4a26` → `5be4a265cb089eb086d74c5eece1ad622128848d`; `c418be0` → `c418be02006314a464e2961542542bccd5df254d`; `40de383` → `40de38343398eee72aeebad7429f3bb99ab0a8dd`; `520341d` → `520341df2b1a192b5245015d723689a822bc5c13` (`git rev-parse`). Every state has `mapped == knowledge_files`, no missing/dangling names, and the emitted scores match the recipe's ratios.

## (b) custody-pair selftest — REPRODUCED (CLI spelling noted)

The supplied `python3 .ufo/gates/custody-pair/custody-pair.py --selftest` form exits 2: `usage: custody-pair.py [-h] {capture,verify,selftest,paths} ...` / `error: the following arguments are required: cmd`. The parser exposes a `selftest` subcommand, so I ran `python3 .ufo/gates/custody-pair/custody-pair.py selftest` instead; exact final output: `CUSTODY_PAIR_SELFTEST: CLEAN cases=28 passed=28 failed=0 exit=0`.

## (c) citation-drift probe — REPRODUCED in both modes

`python3 .ufo/gates/citation-drift/citation-drift-probe.py --root .`:

```text
CITATION_DRIFT_ROOT: .
CITATION_DRIFT_REVISION: HEAD
CITATION_DRIFT_TABLE: /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/gates/citation-drift/pointer-table.json
CITATION_DRIFT_VERDICT: reported findings=0 exit=0
```

With `--strict`, the same root/revision/table printed `CITATION_DRIFT_VERDICT: clean findings=0 exit=0`.

## (d) census v10 — REPRODUCED

`python3 .ufo/gates/c1-census-v10.py --root .` ended:

```text
PROVINCE.md    lines=162  loci=6
SCORECARD.md   lines=1631  loci=9
SKILL.md       lines=390  loci=2
SCOPE-ERRORS (marker assertions): []
UNREADABLE (could-not-evaluate): []
G2 positive-assertion guard: ok (current-ok loci per file: PROVINCE.md=17, SCORECARD.md=14, SKILL.md=3; total loci=17; floor=1/file)
G7 configured!=held warnings: []
G11 current-ok without receipt language: []
DECLARED FAIL CLASSES: []
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)
```

## (e) PROVINCE hold and nine stale-literal absences — REPRODUCED

`wc -l PROVINCE.md` → `162 PROVINCE.md`. I derived the old literal needles from the `40de383^` → `40de383` `PROVINCE.md` diff (old-side loci below), then searched each exact string against current `PROVINCE.md`; each dedicated Grep exact-pattern query returned `No non-sensitive matches found`:

1. `35 features incl. PyGhidra/BSim` (old `PROVINCE.md:46`)
2. `pinned on host: obsidian ×2, signal, 1Password, electron39/43 stubs, typora ×3 (r1 sweep missed them)` (old `:49`)
3. `absent: \`7z\`, \`cabextract\`, \`xxd\`, radare2/rizin, strace/ltrace, upx, pacman-contrib` (old `:62`)
4. `Reserve: 91MB Godot ARM64 template` (old `:83`)
5. `all 3 organic cores exceed the cap` (old `:84-86`)
6. `real solc/vyper-compiled bytecode untested` (old `:92`)
7. `Next: raise \`REA_GHIDRA_STARTUP_TIMEOUT_MS\` to` (old `:139`)
8. `probe-refused since r2` (old `:157`)
9. `multi-version pacman pairs beyond expac unexercised` (old `:158`)

Search-tool note: these were exact literal-pattern searches with special regex characters escaped; the content verdict is reproduced, though this is not a shell `grep -F` transcript. A broader `91MB Godot ARM64 template` substring remains once in the corrected `held, arc2-r7` wording at current `PROVINCE.md:83`; the stale `Reserve: 91MB ...` literal itself is absent.

## (f) Vyper evidence spot-check — REPRODUCED

I made fresh REA CLI calls against `.ufo/waves/arc3-loop1-round4/claims/c1/EX-04/out/runtime.hex` (`hex --format json`), with separate fresh `TMPDIR`s under `/var/tmp`:

- `TMPDIR=/var/tmp/kaidoku-sc4-r5-rea64.2mQAXX npx -y rea-agents@6.4.0 inspect-evm-interface .ufo/waves/arc3-loop1-round4/claims/c1/EX-04/out/runtime.hex hex --format json > /var/tmp/kaidoku-sc4-r5-rea64.2mQAXX/result.json` → exit 0, evidence `ev_d1792f577ae3611615fd8dbcb1ce2e71dae4e0346b66d72b41321f4644df963f`; `functions=15`, `dispatch_abi=15`, planted K size 15, `K/K=True`, missing `[]`, extra `[]`.
- `TMPDIR=/var/tmp/kaidoku-sc4-r5-rea67.cBmHgL npx -y rea-agents@6.7.0 inspect-evm-interface .ufo/waves/arc3-loop1-round4/claims/c1/EX-04/out/runtime.hex hex --format json > /var/tmp/kaidoku-sc4-r5-rea67.cBmHgL/result.json` → exit 0, evidence `ev_62e1b9e6e4d254f3a0a7f874bc068847b2fcc00f47b85151f540ab879bfbae47`; same `15`, `15`, `15`, exact K/K and empty missing/extra sets. Both runs returned the same 15 selectors: `0776076f, 0c751377, 1aa02d59, 27e235e3, 2e1a7d4d, 3f4ba83a, 4643c56b, 48a3ef5c, 5c975abb, 6e8efde2, 8456cb59, 8da5cb5b, b144adfb, d0e30db0, e0749a6a`.
- Independently hashing `EX-04/out/runtime.bin` yielded `bytes=1562 sha256=57d6fd0ae0da001975a3f58ae72804757aa36267f6e373bf9f134ecc9791dae0`; each REA result's decoded `bytecode.bytes` and `bytecode.sha256` matched.
- Direct byte-stream decode: prefix `5f3560e01c6002600d820660011b61060001601e395f5156` decodes to `PUSH0 CALLDATALOAD PUSH1 0xe0 SHR PUSH1 0x02 PUSH1 0x0d DUP3 MOD PUSH1 0x01 SHL PUSH2 0x0600 ADD PUSH1 0x1e CODECOPY PUSH0 MLOAD JUMP`. This indexes a 13-entry, 2-byte table at offset `0x600` (runtime length `0x61a`); all 13 table targets are JUMPDESTs. Following the chains from the raw bytes found 15 unique selector legs, every one `PUSH4/DUP2/XOR/PUSH2/JUMPI`; that selector set equals both the planted K set and the fresh REA set. The measured shape is therefore modulo-indexed table + XOR compare chains.

One initial scratch decoder attempt used incorrect immediate offsets and raised `IndexError`; I corrected the byte offsets and re-ran the raw-byte derivation above. It did not alter the target or evidence. REA limitations retained: selectors are upstream inferences, not verified signatures; bytecode kind, hardfork, deployment authenticity are unknown; no execution, chain/RPC lookup or network request occurred (`evmole-interface`, `evmole@0.9.3`, confidence `inferred`).
