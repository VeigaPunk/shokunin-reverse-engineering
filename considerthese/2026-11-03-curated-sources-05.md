# kaidoku: compilation-based concolic analysis across generations

Date: 2026-11-03 · Batch 5

**Unassimilated reading; assimilation awaits the user's explicit instruction.** Source research only. No target, compiler, emulator, solver or fuzzing workload was executed.

## Timeline: three different bottlenecks

- **August 2020:** Poeplau and Francillon's [SymCC](https://www.usenix.org/conference/usenixsecurity20/presentation/poeplau) places symbolic handling into compiled LLVM programs instead of repeatedly interpreting the intermediate representation. Read the design and evaluation conditions. Source/build access is an important applicability boundary, not a minor installation detail.
- **February 2021:** their [SymQEMU paper](https://www.ndss-symposium.org/wp-content/uploads/ndss2021_2B-2_24118_paper.pdf) brings compilation-based symbolic handling to binary translation. It modifies QEMU's intermediate representation before host-code generation. The evaluated implementation targets Linux user-mode programs; possible extension to full-system emulation is not demonstrated support for every firmware target.
- **August 2024:** Qi et al.'s [SymFit](https://www.usenix.org/conference/usenixsecurity24/presentation/qi) identifies another cost: ordinary concrete instructions still pay symbolic-monitoring overhead. Its lightweight concrete mode and Concrete Memory Lookaside Buffer reduce that cost, switching modes when symbolic values are encountered. Read §§2–5 and the evaluation: pure-concrete speed, symbolic tracing, solving and end-to-end coverage are separate measurements. Published comparisons with SymQEMU do not establish a universal 2026 winner.

## Current source checks and practical limits

The [SymCC README at 522c4807](https://github.com/eurecom-s3/symcc/blob/522c48070bc312aeb621a631ff130ded71507d6d/README.md), committed 2026-10-28T23:35:39Z, describes best-effort maintenance, incomplete libc modeling and QSYM-backend pruning that is not sound. The [SymQEMU README at 6e37dd2c](https://github.com/eurecom-s3/symqemu/blob/6e37dd2c3bace02997f358a7fb5d2b23bf4a5b59/README.md), committed 2025-05-05T11:51:14Z, describes a QEMU 8.1 base, x86-64 use and experimental AArch64 support. Both snapshots were resolved on 2026-11-03. Architecture-independent design is not proof of complete architecture support.

**What changes and survives:** moving instrumentation from compilation to translation changes which artifacts can be examined; optimizing the concrete path changes where time is spent. Neither removes path-selection, environment-modeling or solver limits. Earlier compiler instrumentation remains a useful comparison when source and dependencies can be rebuilt, avoiding a binary-only requirement that the task does not have. Preserve older results only with their original workload and version boundaries. Faster execution is not exhaustive coverage, a safety proof or evidence that a particular defect exists.

## Original future comparison question

After explicit assimilation authorization, could a paper selection ledger distinguish a rebuildable program, a binary-only user-mode artifact and an unsupported full-system target? Record available source, library models, architecture, concrete/symbolic workload mix and the exact outcome each published comparison measures. An incompatible target should remain unsupported, not inherit another benchmark's success. No execution is proposed here.

**Rights and novelty:** SymCC states GPL-3.0-or-later with component exceptions; SymQEMU's added files are GPL-2.0-or-later while existing files retain their licenses. Those software terms do not establish reuse rights for the papers. Original commentary and links only. These three method families were absent from supplied inventories and four prior batches.

