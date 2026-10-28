# kaidoku — round 48 report

Lane `kaidoku`, round 48, attempt 1. Lane repo `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.

## Work performed

**Declared claims:** R48-C1, a `depth` move in craft rule block 25 plus meaning-bound instrument-registry rows; and R48-C2, a `calibration` move in the record counter (committed-byte oracle, per-section floor, receipt-bound quotes/corrections, and score-cell check). Coverage was not claimed; the three finite owned proxies were tied at 10.

- Added block 25, the two routed-id keyed arms, 16 repaired verdict-map class prefixes, two round-48 registry rows, and the round-48 census re-derivation; measured at commit `2e785632863f043a985f7953775b6aca191f1169` and rechecked at `33f65a913cfd21a4491a4f8b7ccc8f00069f058d`. Evidence: `SKILL.md`, `.ufo/waves/round-48/l1/scores/c1-final-33f65a91.json`.
- Added the round-47 seats and quote corrections to `SCORECARD.md`; measured the record floor and five-forgery battery at the same revisions. Evidence: `SCORECARD.md`, `.ufo/waves/round-48/l1/scores/c2-final-33f65a91.json`.
- Preliminary measurement at `165d45d1` produced C1 exit 0 but C2 exit 1 because the drafted scorecard contained literal `<REV>` paths, which the oracle treated as absent path atoms (`.ufo/waves/round-48/l1/scores/c2-at-165d45d1.json`). The scorecard was changed to concrete receipt paths; the final C2 measurements at `2e785632` and `33f65a91` both exit 0.
- Curated two source rows (one admitted, one rejected), mined M48-1, and added QUALITY row 79. Evidence: `corpus/SOURCES.md` S145–S146, `corpus/lessons/round-48.md`, `corpus/QUALITY.md` row 79.
- Resolved inherited uncommitted late seat writes from rounds 45–47, not new domain work: commits `0d76deedd7ce9dd17c510494c33b7b00c3282554` and `663f30ee7516942a0120e7de68fe88356e680822`. The first contains the three wave directories; the >1 MiB receipt was explicitly named in the second.
- Dispatched one v2 wave (`r48-w1`): 75 seats, 75 settled; role mix: executor 22, scribe 16, reviewer 9, scout 9, critic 6, mutation-tester 6, connector 2, revenger 2, simplifier 2, sentinel 1. Attack roles were 21/75 (28%). L1 held the planner seat. 73 seats produced reports; C1Battery-2 and ScribeReportNumbers had no report; C2Floor reported, then its later completion loop was cancelled. Dead seats: 0. Results: `.ufo/waves/round-48/r48-w1-results.json`.
- **Freeze chronology caveat:** the wave was dispatched against A1 (`dc73587a`); A2–A8 were made while seats were running A1 control checks. No after-state landing verdict had been scored before A8, but the control evidence did precede the final freeze. The claims below are measured against final freeze A8; strict admission under the frozen-before-data rule remains for the operator to judge.

## Landed changes

| change | LOG entry | commit |
|---|---|---|
| Freeze and counter series A1–A8; final declared freeze A8 | `plans/round-48-claims.md`, `LOG.md:3436-3439` | `7fe11332781356ec3d5b0b314698de27dd25b50d`, `dc73587a8b9c1a23ba5a91dc7707ac7381a8b873`, `ac02a79ff84133220d01ce3b59a4789b7004dbc5`, `f3a7afc42c1da2457ab0ffd1883c5bdb822f2962`, `0f06251bf6a3a6964c715f67243d4df12e854258`, `04f9d4b7698deb9bff04380e781ae5090ea9bb76`, `24b4e5cbe22e1eafd93d3a5a1706ec381c77f563`, `c8d7da5539157bf719fa29aa71d8a540fb5c136b`, `b6f7ca2a6391964dfdedd477cd560bd42159873a` |
| Block 25, registry repairs/rows, SOURCES S145/S146, lesson, QUALITY row 79, scorecard and settled wave evidence | `LOG.md:3442-3444` | `2e785632863f043a985f7953775b6aca191f1169` |
| Scorecard measured pointers and first claim receipts | `LOG.md:3440-3441` | `c093e798106eba7e5372f63108ec32748bdc115f` |
| Do-nothing and v2 controls at final freeze | `LOG.md:3439` | `33f65a913cfd21a4491a4f8b7ccc8f00069f058d` |
| Wave accounting/log disclosure and final recheck receipts | `LOG.md:3446-3449` | `577a02a52b68b02d33374e8a3f9a913a257fee7d`, `8847042a140b044dbf335210c965bf7b06b09b4f` |
| Inherited late round-45/46/47 seat evidence (custody only) | `LOG.md:3449` | `0d76deedd7ce9dd17c510494c33b7b00c3282554`, `663f30ee7516942a0120e7de68fe88356e680822` |

## Before → after measurements

Both counters were measured at final recheck revision `33f65a913cfd21a4491a4f8b7ccc8f00069f058d`, freeze `b6f7ca2a6391964dfdedd477cd560bd42159873a`. Receipts are committed at `8847042a140b044dbf335210c965bf7b06b09b4f`.

| claim | before | after | counting command | receipt / result |
|---|---|---|---|---|
| R48-C1 (depth) | freeze control exit 1: marker absent, 24 blocks; control `.ufo/waves/round-48/controls/ctl-c1-0-do-nothing.json` | exit 0: 25 blocks; 42 registry rows = 42 census paths; `meaning_rows_failed 0`; battery `4/4/0/1/0` (total/v2-green/v3-green/genuine/crash) | `python3 -I -B tools/round-48/meanings.py --root . --freeze b6f7ca2a6391964dfdedd477cd560bd42159873a --rev 33f65a913cfd21a4491a4f8b7ccc8f00069f058d` | `.ufo/waves/round-48/l1/scores/c1-final-33f65a91.json`; exit 0; stdout SHA-256 `3cc2d72d8f6564545a7d9f32c86a4d3a81bf5367f8b55bdb15075e60401e8f77`; 2026-10-28T19:33:47Z |
| R48-C2 (calibration) | freeze control exit 1: round-47 seat atom absent, no round-48 corrections, one unsupported `exempted` quote; v2 profile exit 0 (`ctl-c2-0-do-nothing.json`, `ctl-c2-1-v2-profile.json`) | exit 0: oracle mismatches `[]`; two corrections re-derived; `quotes_bad []`; `axis_score_bad []`; battery `5/5/0/1/0` | `python3 -I -B tools/round-48/record2.py --root . --freeze b6f7ca2a6391964dfdedd477cd560bd42159873a --rev 33f65a913cfd21a4491a4f8b7ccc8f00069f058d` | `.ufo/waves/round-48/l1/scores/c2-final-33f65a91.json`; exit 0; stdout SHA-256 `c30628ae7c439754f570476d570ed57db3361c1a3b5178ecb1c97f065c1e1ce8`; 2026-10-28T19:33:47Z |

Both claims **met under the final A8 predicates**; admission caveat above is not hidden. Owned scores remain coverage 10, depth 10, calibration 10. No axis harm was observed.

## Sources & frontier

SOURCES count command:

```sh
grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md
```

Before: `144` rows (exit 0). Census output at round start (exit 0):

```text
kaidoku W04 S033 duplicate url github.com/NationalSecurityAgency/ghidra/pull/9348 across scopes
kaidoku W04 S047 duplicate url go.dev/dl/?mode=json&include=all`, across scopes
kaidoku W04 S054 duplicate url developer.android.com/ndk/guides/abis across scopes
kaidoku W04 S062 duplicate url raw.githubusercontent.com/sigrokproject/sigrok-cli/sigrok-cli-0.7.2/doc/sigrok-cli.1 across scopes
kaidoku W04 S069 duplicate url www.wireshark.org/docs/man-pages/tshark.html across scopes
kaidoku W04 S083 duplicate url registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz across scopes
kaidoku W04 S090 duplicate url registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz across scopes
kaidoku W04 S092 duplicate url registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz across scopes
kaidoku W04 S102 duplicate url learn.microsoft.com/en-us/windows/win32/debug/pe-format across scopes
kaidoku W04 S112 duplicate url raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/handlers/filesystem/squashfs.py across scopes
kaidoku W04 S117 duplicate url raw.githubusercontent.com/onekey-sec/unblob/26.6.4/README.md across scopes
kaidoku W04 S119 duplicate url registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz across scopes
kaidoku W04 S123 duplicate url registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz across scopes
kaidoku W04 S138 duplicate url github.com/onekey-sec/unblob/tree/26.6.4/tests/integration/filesystem/squashfs across scopes
kaidoku W04 S142 duplicate url git-scm.com/docs/git-log across scopes
kaidoku ok /home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md
```

After: `146` rows (exit 0). The same census command exits 0 with the same 15 W04 duplicate-URL warnings and final `kaidoku ok /home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md`. Added by tier: one tier-A mined row (S145, SEP Popper; the 22-word quote is in `corpus/lessons/round-48.md` `## Gate`) and one tier-C rejected row (S146, man7 sysexits URL returned HTTP 404; flip condition is recorded in the lesson). Existing rows touched: none. Domain frontier rows advanced: none; no knowledge entry, coverage-map row or PROVINCE change. Assimilation: none — no `considerthese/` directory; the staged merge package was not adopted wholesale.

Mistake mined (M48-1): `vacuous-clause` — evidence `controls/ctl-c2-a1-before.json` (`axis_score_cells {}`); captured-by `none`; fix: parse the score cell directly and verify the score-cell mutation fails while the genuine record passes (`l1/scores/c2-final-33f65a91.json`). Full lesson: `corpus/lessons/round-48.md` `## Mistakes`.

## Trend verdicts

- **Expansion — unchanged.** Knowledge files remain 138/138 mapped; no new knowledge or coverage-map row. `S145` is method documentation, not a new reverse-engineering surface; `S146` is rejected.
- **Quality — improved (instrument scope only).** C1's four forgeries score v2-green/v3-red and the genuine artefact green; C2's five forgeries score v2-green/v3-red and the genuine record green. Limits: a lexical `0=met` can still contradict the tool's actual behavior; C2's gate helper remains worktree-sourced; the battery skips when the genuine record is red.
- **Discernment — improved.** The round found and disclosed eight instrument amendments before the final landing, mined M48-1 with a red-before receipt, and recorded both one admission and one rejection. The final claim predicates differ from the A1 bytes the wave initially saw; the strict freeze chronology caveat remains for operator adjudication.

## SHONEN

[~] Decision-table depth: `SKILL.md` block 25 and final C1 receipt; no semantic source-truth claim (`SKILL.md`, `c1-final-33f65a91.json`).
[~] End-to-end domain task: prior round-42 REA evidence remains the latest named end-to-end execution; round 48 did not execute a new domain task (`SHONEN.md`, round-42 entry).
[~] Executable instructions: block 25 and both counters ran against committed bytes; finite instrument evidence only (`SKILL.md`, `tools/round-48/`, final receipts).
[~] Province boundary: `PROVINCE.md` unchanged; round 48 added no domain surface (`PROVINCE.md`, lane diff/commit `2e785632`).

**Stale-lane:** respawn-per-round driver; no other mission of this lane is open. **Tool installs:** none. **Fleet misroot sweep:** `git -C /home/vgpnk/Projects/shokunin status --porcelain` found no round-48 kaidoku seat output at the fleet root; all remaining entries were `.scratch/`/other-lane artifacts and were left untouched.

**Lane tip:** `8847042a140b044dbf335210c965bf7b06b09b4f` (remote `refs/heads/main` verified at this hash).
