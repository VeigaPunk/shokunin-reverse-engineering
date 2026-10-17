# FB1-FB7 composite seat — append-point audit, 7 round-5 targets

## CLAIM
Per-file append point (final line, last heading, tail sha256) and errata precedent recorded from primary sources; zero tracked-file writes.

## METHOD
At HEAD `cfc84c2`: `wc -l`; `grep -n '^#'|tail`; `sha256sum` for whole file and final line; `git show HEAD:<path>|sha256sum` (worktree==HEAD, all 7); EOF-byte check; sibling errata-style scan; `python3` arithmetic check. No network/probes.

## FINDINGS
All 7 end with LF; appends go after the stated line. Tail = whole-file sha256 / final-line sha256.

1. `corpus/knowledge/2026-10-13-asar-surface.md` — :91; last heading `## Provenance anchor (round-14 sweep, 2026-10-14, append-only)` :85; `a55fc71cc009b6e33e04a9656c3f4df201b6835dad019818d4c25ff2beb6eec9` / `ae7e06602d2cdf5a04af8a6e5406e9b766481f15418e405fe34c1b1c82ac8d76`. Precedent: in-file `## Errata (round 2)` :80-83 (bullet + `(audit-C)` attribution); sibling bold-lead form at `corpus/knowledge/2026-10-13-r3-renderer-asar.md:109`.
2. `corpus/knowledge/2026-10-13-r4u-01-firmware-deep.md` — :119; `## Errata (round 6, 2026-10-13, append-only)` :114; `d565f690dfb5d97f819a9489895736291ec8b6b0bd9d1986f0e0a66bafeca5ce` / `4babfc920be3c2e2db8aeef220d4ac928a5ece2c0bdef047a7fa3997f38db506`. Second-section precedent: `corpus/knowledge/2026-10-13-r2-firmware-probe.md:107,115`. Decimals verified: `0x1c01dc8`=29,367,752 (file :41: 29,358,536); `0x505b000`=84,258,816 (84,242,432).
3. `PROVINCE.md` — :155; `### Round-4 frontier (post-unlock)` :126; `cd6c62292f09829fda76b396f9f791605d7cfcafbead15b348436f9d9c7bdca5` / `578abc9baacf6fac2b80e309d822696e3d308a3849e1ef69348a611e89578fe8`. Current-surface edit, not append: P0 sites :31-32,:58; house form inline audit tags `[r5-audit C8: …]` :118, `[r5-audit C1]` :49,:69-73, `**round-12 audit correction**` :117.
4. `corpus/README.md` — :173; `## Known gaps` :166; `43a392ebe7361e51bc982ef6cdc5e789abd847b1ceefe71bf193660d0d9d30f4` / `a10d5ed3dd686b2c9d439fd53df90070d194a181720c2d60fda13cab86b8b3fd`. Repairs are in-place cell rewrites (pattern :53), never errata sections; append fallback after :173. Texts: :131 = r14-02 lessons row; :163 = "Runtime-obs extended: … managed `verify`/`project` ops, native call-target resolution …". Keep all 72 map tokens (command A, `SCORECARD.md:92-123`).
5. `corpus/knowledge/2026-10-14-r9-02-queue-a-ops-2.md` — :375; `## Census note (rows taken, concurrency, final state)` :352; `0e60215518c214f5a1e1ea4d7031269f1e8e24e84d504bfd2dd3f7f4a51e928d` / `1a9de5e3123038422f42772e954dfe90702174a15a4a23039025ece1dfc9bbb4`. Tension confirmed: :215-216 "four statuses" complete vs :82-84 `inferred:0` (never observed). No in-file errata; sibling form `corpus/knowledge/2026-10-13-r8-02-queue-a-ops-2.md:297`.
6. `corpus/knowledge/2026-10-13-r5-02-call-targets-jq.md` — :194; `## Summary` :175; `7387e01cc9cde9f06df0e9c1370d348d83b0d45667181ba77de3848c34138689` / `f8c3a79019cdf4407cd7ed2ed95f48be26c20ab073524e2c2ee61c69dbba7efe`. :152-153 "283 call sites" vs :18-19 census (286=284 call+2 jmp): truth 283 sites = 281 calls + 2 jmps. Precedent: `corpus/knowledge/2026-10-13-r5-01-riscv-bypass.md:98`.
7. `corpus/knowledge/2026-10-14-r12-01-queue-b-ready.md` — :108; `## Errata (round-12 audit, 2026-10-14, append-only)` :97; `0a794bc13e8ab9cf635b882e39c9c6f06e3dedf31d22cd7760e43d93e89f5b80` / `9b78fe26b0d403f3f5c8cc08cf08be79997ef7e8f9d63672c76d0b6403e2e917`. L197 main :40-44 ("exactly two values") vs erratum :99-104 (four sites/7 values): append reconciles, does not rewrite.

## THREATS
Anchors HEAD-pinned; any landing edit invalidates line numbers — re-derive before appending. PROVINCE/README append point is advisory. Earlier-section insertion shifts later refs.

## VERDICT
CLEAN — all 7 append points, tail hashes, precedents recorded.
