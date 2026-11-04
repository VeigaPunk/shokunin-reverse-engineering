# ReviewerC2 — round-88 (kaidoku) — R88-C2 attack record

Reviewer: ReviewerC2 (leaf, no dispatch). Scope: R88-C2 only (depth: packed-ELF
refusal-signature rule block; counter `tools/round-88/depth-blocks.py`; evidence
`tools/round-88/field-tamper-matrix.py`). Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Base `0cf8e3243059e0bc510b90c880d13d191e78d732`; review-time HEAD moved
`d190c5b57 → 6d235a4cf → 01ffb9376` while I worked (v2 landing).
Instrument pins verified before any run: all four `tools/round-88/*.py` sha256 match
`claims.json` (`depth-blocks 458eeabd…`, `field-tamper-matrix 0e055486…`,
`upx-chain-repair 59ee51b0…`, `upx-chain-battery a01ed622…`), r87 module `96da7d8e…` matches.
SKILL.md is byte-identical at base, HEAD and worktree: craft section holds 27 blocks; the
promised 28th (packed-ELF refusal signatures) has not landed.

## Per-attack verdicts

### Attack 1 — make a block resolve without content: **SUCCEEDED**
One-line knowledge file whose only line is `.`, cited by a content-free block:
`28 blocks / 28 resolved / unresolved [] / exit 0` (bare citation and `:1-1` both).
A block that only *names* (or forbids citing) a real knowledge file also resolves
(regex mention = citation). The floor is real but thin: a **0-byte** cited file fails
(`range:2026-01-01-nothing.md:1-1 of 0`). The counter checks existence+range, never meaning.

### Attack 2 — make a real block unresolved (parser mis-split): **SUCCEEDED (latent), no live false negative**
- Filename charset: real 5-line file `2026-01-01_R88_Note.md:2-3` → `no-citation`
  (PATTERN `[a-z0-9-]+\.md` is blind to `_`/uppercase/nested paths).
- Nested path `corpus/knowledge/sub/2026-01-01-real.md:1-2` → `no-citation`.
- A fenced do-NOT-ship example line inside the craft section becomes a phantom block:
  `29 blocks / 28 resolved / exit 1` — kills the real block it documents.
- The plan's own "matrix receipt path" citation can never resolve: the receipt is JSON
  outside `corpus/knowledge/` → `no-citation`.
Live-corpus check: all 170 `corpus/knowledge/*.md` names match PATTERN (only `.gitkeep`
excluded), all files clean UTF-8 with no `\v \f \x1c` (no splitlines under/over-count),
so the 27 base blocks have no live false negative; defects are latent in the parser.

### Attack 3 — the 68-cell matrix claim vs the instrument: **population confirmed, vocabulary claim falsified then superseded**
- Population: exactly 4 carriers × 17 fields = 68 cells (`population.cells=68, expected=68`
  in my run and both committed receipts). Fields are a 4×17 sample, **not** all reachable
  fields (see Attack 3b).
- Vocabulary: **not closed over reality for the pinned v1 instrument.** My v1 run
  (`field-tamper-matrix.py`): `per_class = {header-corrupted 35, p-info-corrupted 4,
  b-info-corrupt-field 4, b-info-corrupted 8, compressed-data-violation 4, tolerated 8,
  other-refusal 5}`, `met=False`, **exit 1**. The 5 unclassifiable cells are deterministic
  and identical to the executor's committed v1 receipt (0/68 class differences):
  `b0-method` on all 4 carriers → `CantUnpackException: bad method 0 at 0x…`, and libz
  `l-checksum` → `IOException: bad seek`.
- `tolerated` semantics: unreachable is impossible (any offset past EOF raises
  `offset_out_of_range`); `tolerated` = `upx -t` exit 0. But in v1, **5 of the 8 tolerated
  cells were no-op writes** (`p_progid` already zero on all 4 carriers; libz `ph-filter`
  was already `0x00`) — they prove UPX ignores nothing. The 3 genuine ignores are
  `l-checksum`(=l_lsize) on jq/xxd/dinit. v2 (`field-tamper-matrix-v2.py`, sha
  `9386711b…`, committed 6d235a4cf with declared supersession in `claims.json`) fixes
  exactly this: 10 labels, 63 effective cells, 5 `noop`; my v2 rerun reproduces the L1
  receipt cell-for-cell (0 differences), `met=True exit=0`, selftest 13/13.
- Carrier dependence: the same logical field l_lsize is tolerated on jq/xxd/dinit but
  crashes `IOException: bad seek` on libz — a flat decision-table row would be wrong.

### Attack 3b — independent cell probes (fresh jq pack, r87 locators, `upx -t`):
`packheader@14000, l_magic@556, sentinel@13988`:
- `l-checksum` FIELDS entry (+4,w2) tampers **l_lsize** (`was 380c` → rc 0 tolerated);
  the real l_checksum (m−4, `was f48eb603`) is **unmeasured** and tolerated.
- `l-size` FIELDS entry (+8,w4) tampers **p_progid** (`was 00000000` → no-op).
  `l-p_filesize`(+12)→`p_info corrupted` and `l-p_blocksize`(+16)→`corrupt b_info` are
  correctly named. (r87 layout: l_info = {l_checksum@0, l_magic@4, l_lsize@8w2,
  l_version@10, l_format@11}; p_info at l_info+12.)
- Fields **outside** the 17-field set print typed refusals outside even v2's 10-label
  vocabulary: `l_magic` → `CantUnpackException: l_info corrupted`; `ph-version` →
  `CantUnpackException: I am not compatible with older versions`; `ph-filter_cto` →
  `header corrupted`. "Every field a tamperer can reach" (v1+v2 docstrings) is false;
  notably `l_info corrupted` is the r87 repair's own primary anchor and cannot be triaged
  from the measured vocabulary.
- Verified good rows: ph-checksum→`header corrupted 3`, sentinel-sz_cpr (was `UPX!`)→
  `compressed data violation`, l-p_filesize→`p_info corrupted`, l-p_blocksize→`corrupt b_info`.

### Attack 4 — the promised block is writable with base-resolving citations: **CONFIRMED**
Base SKILL.md bytes + one refusal-signature block citing only
`corpus/knowledge/2026-11-04-r87-upx-magic-tamper-repair.md:8-20` (125 lines at base;
8-20 carries the structure law) → `28/28, unresolved [], exit 0`. R88-C2 does **not**
need R88-C1. Caveat: the block's "matrix receipt" mention can only be prose — the
receipt (`.ufo/waves/round-88/l1/scores/c2-matrix-at-declaration.json`, JSON) is invisible
to the citation regex; a resolving receipt citation would require committing it as a
`corpus/knowledge/*.md` (then it is base-absent and unresolved until it lands, measured).

### Attack 5 — which axis moves, can a do-nothing control reach it: **DEPTH-AS-BLOCK-COUNT; YES for exit, one-liner for the label**
`met_target = not unresolved` — the untouched tree already exits 0 at base and HEAD
(measured via `--rev` both: `27/27, exit 0`; matches frozen `c2-depth-at-base.json`,
which also records `met_target: true`). The 27→28 increment lives only in the label
literal, and a content-free one-line citation reaches it (Attack 1). The refusal-signature
*content* is bound solely by the freeze's block-text declaration (kill rule "block text
changed"), i.e. review-side, not instrument-side. Axis actually moved: count of
citation-resolvable rule blocks; the claimed decision-table depth is not machine-bound.

## Findings by severity

- **F1 (high, contradicts plan text)**: frozen claim "68 cells, closed 7-label vocabulary"
  is false for its own pinned instrument: v1 exits 1 with 5/68 `other-refusal`. The v2
  supersession (10 labels / 63 effective, declared in `claims.json`
  `instrument_supersessions`, predicates unchanged) is honest and reproducible, but
  `plans/round-88-claims.md` was never reconciled — the round cannot both cite the v2
  receipt and keep the 7-label sentence. The landed block must document 10 labels (or
  scope the 7-label subset explicitly).
- **F2 (high, depth content)**: `l-checksum`/`l-size` misname the tampered fields
  (actually l_lsize / p_progid); real l_checksum unmeasured. Decision-table rows keyed on
  these names will misattribute refusals.
- **F3 (high, closure)**: reachable fields outside the 17 produce typed refusals outside
  even v2's vocabulary — `l_info corrupted` (l_magic, the r87 anchor), `I am not
  compatible…` (ph-version). The claim "triaged by the refusal UPX itself prints" holds
  only for the 17-field sample, not the surface.
- **F4 (medium)**: counter exit is do-nothing-satisfiable; label reachable content-free
  (Attack 1); mention-as-citation false positive.
- **F5 (medium, latent)**: charset/nested-path citation blindness; fenced example becomes
  a phantom block and false-kills; JSON receipt citation unresolvable. No live corpus hit.
- **F6 (low)**: v1 `tolerated` conflated 5 no-ops with 3 real ignores (v2 fixed; receipts
  agree); l_lsize behaviour is carrier-dependent (tolerated ×3, bad-seek on libz).
- **F7 (info)**: v2 `met` tolerates up to 17 noop cells (`len(noops) <= len(FIELDS)`).

## Commands run (all from the lane unless noted; no mutating git anywhere)

```
sha256sum tools/round-88/{depth-blocks,field-tamper-matrix,upx-chain-repair,upx-chain-battery}.py tools/round-87/upx-magic-repair.py
git rev-parse HEAD; git status --porcelain; git log --oneline --stat base..HEAD
git show base:SKILL.md > scratch/SKILL_base.md   # read-only export
python3 tools/round-88/depth-blocks.py --selftest            # cases=7 failures=0
python3 tools/round-88/field-tamper-matrix.py --selftest     # cases=11 failures=0
python3 tools/round-88/field-tamper-matrix.py --root <lane> --work <scratch>/matrix-work --json-out <scratch>/matrix-ReviewerC2.json   # exit 1, other-refusal 5
python3 tools/round-88/field-tamper-matrix-v2.py --selftest  # cases=13 failures=0
python3 tools/round-88/field-tamper-matrix-v2.py --root <lane> --work <scratch>/matrix-work2 --json-out <scratch>/matrix-v2-ReviewerC2.json  # exit 0, 63 effective
python3 tools/round-88/depth-blocks.py --root <lane> --rev HEAD                       # 27/27 exit 0
python3 tools/round-88/depth-blocks.py --root <lane> --rev 0cf8e3243059e0bc510b90c880d13d191e78d732   # 27/27 exit 0
python3 <scratch>/attack_depth.py    # 11 fixture attacks, --worktree (plain dirs, no git)
python3 <scratch>/probe_cells.py     # 10 independent jq-cell probes with r87 locators
```
Fixture attacks (driver at `attack_depth.py`, results in `attack-results.json`,
scratch `/fast/scratch/hyaku/kaidoku-r88/ReviewerC2/`, deleted after this report):
base-untouched 27/27 exit0 · A1a one-line-nothing bare 28/28 exit0 · A1b :1-1 28/28 exit0 ·
A1c zero-byte 27/28 exit1 · A1d mention 28/28 exit0 · A2a underscore 27/28 exit1 ·
A2b nested 27/28 exit1 · A2c json-receipt 27/28 exit1 · A2d fenced 29/28 exit1 ·
A4 promised-block-at-base 28/28 exit0 · A4b +absent-receipt-cite 27/28 exit1.

Cross-checked committed evidence: `.ufo/waves/round-88/w1/ExecMatrix/matrix.json` (v1,
identical classes), `.ufo/waves/round-88/l1/scores/c2-matrix-at-declaration.json` (v2,
identical classes), `pre/c2-depth-at-base.json`, `pre/c2-control-junk-blocks.json` (both
reproduced), `claims.json instrument_supersessions[0]` (read, honest, matches my numbers).

Nothing installed; no pacman; no tool changes (none needed).
