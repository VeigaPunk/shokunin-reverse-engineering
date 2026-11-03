source: S264 — https://raw.githubusercontent.com/xqy2006/jsc2js/01fc264d22055865a460b322399a15d84b71f5aa/README.md — English matching-d8 note, line 199; opened 2026-11-03
verified-at: 2026-11-03
recheck: 90d

# jsc2js pipeline: dumped bytecode is not executable recovered JavaScript

Assimilated from `merge/kaidoku/knowledge/corpus/knowledge/jsc-mapper-cli-contract.md` (staged S125, renumbered by URL to S264).

The upstream commands are `./d8 -e "loadjsc('path/to/xxx.jsc')" > xxx.txt`, followed from the repository's `View8/` directory by `python view8.py --disassembled ../xxx.txt ../xxx.js`. The README requests a matching V8 build; it does not establish correctness on any artifact.

Round-64 observations: `.ufo/waves/round-64/w1/ExecMatrixRun/matrix-run.json` records 18 runs over two artifacts and three builds, three repetitions per cell. The synthetic Electron 42.2.0 cache dumped under d8 14.8.178.14 and 14.8.178.1; View8 emitted 213-byte pseudo-code that failed `node --check`. The previous-minor 14.7.173 build died with signal 11. All three builds aborted with signal 6 on the shipped Typora cache (SHA256 6a0cb7b32270498ed190c589ca29c990a0e4b5f06f0cd6a5516e19a715c2dfe9). These outcomes do not diagnose why Typora fails.

Static header equality is limited to observed words 0, 1 and 4, not authenticated semantic field meanings: `.ufo/waves/round-64/w1/ExecHeaderTable/header-table.md`.

The instrument reproduced its label target, but its stronger pin predicate did not survive review: D2/D3 companion files and transitive View8 modules were not pinned. See `.ufo/waves/round-64/w1/ReviewerMatrix/review.md` F1/F2. R64-C1 is therefore unprovable under its frozen wording; no general reconstruction capability is registered. Typora source mapping remains Frontier.
