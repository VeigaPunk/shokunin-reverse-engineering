# C1LandingMap — receipts (seat C1LandingMap, kaidoku round 50 wave 1)

UTC of receipt batch: 2026-10-28T23:38:11Z (`date -u +%Y-%m-%dT%H:%M:%SZ`, exit 0).
Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. All commands read-only; no edits made to the lane tree; no git mutation run.

| # | command (exact) | exit | output / sha256 |
|---|---|---|---|
| 1 | `git -C <lane> rev-parse HEAD` | 0 | `7c678ae6d97aedb969fd253b52b3d2882ef1e186` |
| 2 | `bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` | 0 | `/fast/scratch/hyaku 31%, 555.4G free` |
| 3 | `mkdir -p /fast/scratch/hyaku/kaidoku-r50/C1LandingMap` (+ `TMPDIR`, `HYAKU_SCRATCH` exports) | 0 | dir created (removed before yield) |
| 4 | `git -C <lane> status --porcelain` | 0 | exactly one line: `?? .ufo/waves/round-50/` (untracked wave dir; tree otherwise clean) |
| 5 | `git -C <lane> diff --stat 7c678ae6d97aedb969fd253b52b3d2882ef1e186 -- PROVINCE.md corpus/README.md SKILL.md SCORECARD.md corpus/SOURCES.md tools/round-49/c1-counter.py tools/round-49/c1-controls.py` | 0 | empty output — all cited files byte-identical to base; every line number below is a base-revision line |
| 6 | grep-tool searches (each exit 0, hits recorded in evidence-lines.md): `hsqs` and `AVM` in PROVINCE.md; `AVM` in SKILL.md; `AVM` in SCORECARD.md; `Frontier|Coverage map` in corpus/README.md; `LE AVM` in PROVINCE.md and corpus/README.md; `additions to Core` lane-wide; `sqfs-triage-table v|avm-marker-be-dropped|Layout pre-check|outcome triage v4 (round 42)` and `Local round-evidence gate registry` in SKILL.md; `PROVINCE|README\.md|Coverage map|additions to Core|Frontier` in tools/round-49 | 0 | hit lists in `evidence-lines.md` |
| 7 | `wc -l PROVINCE.md corpus/README.md SKILL.md SCORECARD.md tools/round-49/c1-counter.py tools/round-49/c1-controls.py` | 0 | 438 / 296 / 1762 / 3772 / 3415 / 1549 |
| 8 | `sha256sum` (working tree = base blob for each) | 0 | PROVINCE.md `d8425c0a99730986b0ebf0ad04338a8dd054ac003b271c8fa69d482c940a01f1`; corpus/README.md `a702bfdd6a32b89427d672b4522878742810e21dbe3f6db2b36c60268e1d2274`; SKILL.md `04a3a8657d2a3c7a76569b8f12f0589fca055d91b605c3eba77e36f34d0b132e`; SCORECARD.md `b7bc3f84e7b4899b7dbf8d77ce3d4d6145e8856f4c25abd00115ee4577935cb1`; corpus/SOURCES.md `ae3c1e17a3c8fcfc39209b8fa2d2d4623347ced88da5b54c46e011885db54c11`; tools/round-49/c1-counter.py `ac83715b199100774873389ea33fb4819231e1f963225416e86ad422f69d287f`; tools/round-49/c1-controls.py `937b9de1339f137c78aff8d9a0d3d5e6e2e32f314f11df191cee7a82fcca99e5` |
| 9 | read-tool reads incl. `:raw` whole-line reads of PROVINCE.md:438, corpus/README.md:278, corpus/README.md:105 | 0 | verbatim lines in `evidence-lines.md` |

Not run (honestly): no data run, no counter execution, no fixture commits, no carrier downloads — out of this seat's scope (landing map only).
Tool installs: none (no tool installed or upgraded; nothing to record under the 2026-10-19 authorization).
