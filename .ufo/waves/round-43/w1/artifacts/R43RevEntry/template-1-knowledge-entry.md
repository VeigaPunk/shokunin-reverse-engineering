# Template 1 — `corpus/knowledge/2026-10-27-r43-sqfs-triage-v4-scored.md`

Copyable template for the L1. `<<L1:...>>` marks numbers only the L1 can fill
(measured at scoring time). Everything else is format-correct as written.

Front-matter order is the R42-V5 correction: the provenance trio
(`source:` / `verified-at:` / `recheck:`) comes FIRST; `status:` comes LAST,
after the trio. The round-42 v4 entry (`6b9e64fe:corpus/knowledge/2026-10-26-r42-sqfs-triage-v4.md`)
is compliant (sources lines 3–10, `verified-at:` line 11, `recheck:` line 12,
no `status:`); the violation to not repeat is the round-42 v3-core entry
(`status:` line 3 before `source:` line 5 — R42-V5,
`corpus/lessons/round-42-verifier-spotcheck.md:92`).

```markdown
# SquashFS `extract-firmware` outcome triage v4, scored: the frozen table re-frozen byte-identical and matched 78/78 on a fresh freeze-seeded held-out set under a generator that refuses to declare a tuple its own run did not observe (round 43)

source: S112 — https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/handlers/filesystem/squashfs.py — `SquashFSExtractor` lines 24-70, the seven v1-v3 handler names, v4 handler names and magics, v4 BE extractor, v4-broadcom extractor — as cited by the round-42 v4 entry; the table bytes are frozen so the citation set is inherited, re-read 2026-10-27 from the installed unblob 26.6.4 tree, not re-fetched
source: S118 — https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/extractor.py — `is_recursive_link`, `fix_symlink`, `carve_unknown_chunk` — inherited citation, re-read 2026-10-27 from the installed tree
source: S119 — https://registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz — `FirmwarePublication.js` gap kinds (`unknown-chunk-handler`, `extractor-failure`, `depth-limited`, `unpublished-entry`), `MAX_EXTRACTION_DEPTH` — inherited citation, re-read 2026-10-27 from the installed 6.5.0 package
source: S120 — https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/report.py — `ExtractCommandFailedReport`, `ExtractorDependencyNotFoundReport`, `ExtractorTimedOut`, `MaliciousSymlinkRemoved` — inherited citation, re-read 2026-10-27 from the installed tree
source: S121 — https://raw.githubusercontent.com/onekey-sec/sasquatch/sasquatch-v4.5.1-6/squashfs-tools/unsquashfs.c — the `-be` swap flag and `sasquatch-v4be` second build — registry row only, not re-fetched this round
source: S130 — https://github.com/onekey-sec/unblob/tree/26.6.4/tests/integration/filesystem/squashfs — the MIT unblob 26.6.4 SquashFS v1–v3 fixtures the held-out generator pins (`tools/round-42/fixtures.json`, copies under `corpus/evidence/round-42/c2/fixtures/`) — opened 2026-10-26T21:50:43Z (`.ufo/waves/round-42/w1/R42SrcUnblob.md`)
source: S135 — https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/LICENSE — the MIT license text covering the fixture bytes the round-42/43 generators embed — opened 2026-10-27T<<L1:hh:mm:ssZ>> (this round; R43SrcLicense seat capture, HTTP 200, 1068 B, sha256 `67303bbde385e13f69e8019f6f8bc77d4ebfce58c2a409952645e3fe4f4d922e`)
verified-at: 2026-10-27
recheck: 180d — `python3 -I -B tools/round-42/sqfs-triage-v4.py --skill SKILL.md --table-only` -> 15 rules, exit 0 (the interpreter stays the round-42 frozen bytes); the scored state re-derives with `python3 -I -B tools/round-43/c1-counter.py --root <LANE> --rev <REV> --freeze <<L1:FREEZE>> --json-out <OUT>`
status: R43-C1 — scored by `tools/round-43/c1-counter.py` against the round-43 freeze `<<L1:FREEZE>>`; the score receipt and its revision are in SCORECARD `## Round 43` and `.ufo/waves/round-43/l1/scores/`

**What stopped at round 42.** The v4 table matched its independent evaluator
78/78 on the round-42 held-out set, but the round stopped on
`observed_features_match_declared`: combo C02's manifest declared the gap set
`{extractor-failure, unpublished-entry}` while the generator's own REA `--run`
observed `{depth-limited, extractor-failure, unpublished-entry}` — a declared
tuple predicted from factors instead of measured (M42-2,
`corpus/lessons/round-42.md`; stop receipt
`.ufo/waves/round-42/l1/scores/c2-at-eb8215ac.json`; routed R42-CL1).

**What changed (one generator property; no table byte).** `tools/round-43/heldout-gen-v4r43.py`
(QUALITY 85, `corpus/QUALITY.md` row 85; a port of `tools/round-42/heldout-gen-v4.py`)
extracts the observed six-field tuple from each envelope its own `--run`
produced and refuses to write the manifest unless every observed tuple equals
the tuple the manifest would declare: exit 3 `declared_tuple_unobserved`, no
manifest write, per-carrier diff list on stdout. Red/green demonstrated in the
committed controls (CTL-C1-2: the round-42 C02 manifest refused red; the data
run's own manifest is the green). The manifest records the check under
`generator.tuple_check` (per-carrier observed/declared verdicts, all equal).

**The table stayed frozen.** The v4 table region of `SKILL.md` (from the line
containing `<!-- sqfs-triage-table v4 -->` through the end of the first
markdown table after it) is byte-identical to the round-42 freeze
`d1681696dd63ca4f9b8a09ffa8fa3e2de5e2b51b`: region sha256
`<<L1:region sha256 at d1681696>>` at the freeze vs
`<<L1:region sha256 at measured rev>>` at `<<L1:REV>>`. The interpreter
`tools/round-42/sqfs-triage-v4.py` and the evaluator
`tools/round-42/indep-eval-v4.py` are the frozen bytes at all three revisions;
no commit in `d1681696..<<L1:REV>>` touches them or the region.

**The round-43 score.** Held-out set `corpus/evidence/round-43/c1/heldout/`,
78 carriers (27 named classes × 2 plus 24 combos), seed = the round-43 freeze
`<<L1:FREEZE>>`, same `declared_features` single-key contract; every carrier
regenerates byte-identically from the seed and every envelope's subject digest
equals its carrier's sha256. The frozen interpreter gives every envelope the
same (label, action) pair as the frozen evaluator: `matched <<L1:matched>>` of
`n 78`, `observed_features_match_declared true`, every binding of
`tools/round-43/c1-counter.py` true, `frozen_path_changed []`, exit
`<<L1:exit>>` (`.ufo/waves/round-43/l1/scores/c2-at-<<L1:REV>>.json`,
`counter_sha256 <<L1:counter sha256>>`, `counter_sha256_at_freeze
<<L1:counter sha256 at freeze>>`). The frozen lookup control
`.ufo/waves/round-42/controls/c2/CTL-C2-7-lookup.md` still scores strictly
fewer than half of the held-out `combo` envelopes (`combo_unseen_majority`
<<L1:combo_unseen_majority>> of 24) — the named-class lookup cannot reach the
target on combos.

**Controls before data** (`.ufo/waves/round-43/controls/c1/`, scored at the
freeze): CTL-C1-0 do-nothing exit 2 `no_manifest_at_rev`; CTL-C1-1 the
round-42 manifest copied to the round-43 path rejected (seed ≠ freeze;
manifest not first-added after the freeze); CTL-C1-2 the refusal red/green;
CTL-C1-3 the round-42 shortcut controls re-scored by the frozen round-43
counter stay below 78. No control reaches the target.

**Limits.** Carried from the round-42 entry: agreement with an independent
evaluator cannot tell this table from any other table labelling the same
envelopes the same way; the claim measures that the frozen table implements
the frozen precedence on real REA envelopes under a generator that cannot
declare the unobserved, not that the precedence is the best triage. The C02
shape is a property of REA 6.5.0's gap minting beside a failing chunk at the
depth ceiling; the observed tuple is authoritative, whatever it is. The other
twelve limits of the round-42 entry stand unmodified.
```

Evidence the filled entry must cite (checklist for the L1):
- `.ufo/waves/round-42/l1/scores/c2-at-eb8215ac.json` — the round-42 stop receipt (C02).
- `corpus/lessons/round-42.md` M42-2; `corpus/QUALITY.md` row 85; routed defect R42-CL1 (`corpus/lessons/round-42.md` `## Routed defects`).
- Region byte-identity: SKILL.md v4 table region at `d1681696` vs measured rev (sha256 pair recorded in the round-43 score receipt or a sibling receipt).
- `.ufo/waves/round-43/l1/scores/c2-at-<REV>.json` — the round-43 score receipt (matched/n, exit, counter_sha256, counter_sha256_at_freeze, frozen_path_changed).
- `.ufo/waves/round-43/controls/c1/` — CTL-C1-0..CTL-C1-3 receipts.
- `corpus/evidence/round-43/c1/heldout/` + manifest `generator.tuple_check` (all equal).
- S135 row in `corpus/SOURCES.md` (appended this round; HTTP 200, 1068 B, sha256 `67303bbd…`).
- `tools/round-42/fixtures.json` + `corpus/evidence/round-42/c2/fixtures/` (MIT fixture basis).
