# ScribeKnowledge — round 93, seat report

Seat: `ScribeKnowledge` (scribe). Item: draft two knowledge entries, one per claim.
Lane repo: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Declaration commit
`92a240521bd1bf2213b75d18d9b176a8dafdc67c`, base `0a2a23da5eb50410a8a0df90c031d9f4fdadb024`.
Scratch: `S=${HYAKU_SCRATCH:-/fast/scratch/hyaku}/kaidoku-r93/ScribeKnowledge` (removed before yield).

## Files written (all under my seat directory)

| path | what |
|---|---|
| `.ufo/waves/round-93/w1/ScribeKnowledge/2026-11-05-r93-fresh-pack-oracle.md` | entry 1, R93-C1 |
| `.ufo/waves/round-93/w1/ScribeKnowledge/2026-11-05-r93-citation-semantics.md` | entry 2, R93-C2 |
| `.ufo/waves/round-93/w1/ScribeKnowledge.md` | this report |
| `.ufo/waves/round-93/w1/ScribeKnowledge/receipts/*.json` | 11 own-work receipts (listed below) |
| `.ufo/waves/round-93/w1/ScribeKnowledge/probes/*.py` | 5 unscored probes, retained so the findings stay auditable after the scratch is removed |

No lane file was edited. `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin status --porcelain`
shows only the new untracked seat directory plus `corpus/lessons/round-93.md` (the L1's own
untracked draft, not mine).

## Deliverables

### Entry 1 — `2026-11-05-r93-fresh-pack-oracle.md`

Provenance trio on lines 3-5, `source:` on line 3 (single field, the r83 grammar
`source: S318, S316, S271, S317, S313 — …`). It states the arm, what it kills (F1 and F2, with
the committed base receipts and the unscored probe cited by path), the mechanism floor it does
**not** claim, the strict typed parsing, the frozen after-label and the counting command, a
ten-item Limits section, and a five-row Gate table with the source URLs, access dates, HTTP
status/size/sha256 and located quotes. `<measured>` is left as the literal placeholder for every
value only the landing revision can pin (the `verified-at:` revision, the after-receipt revision,
the frozen after-receipt path).

### Entry 2 — `2026-11-05-r93-citation-semantics.md`

Provenance trio on lines 3-5, `source:` on line 3 (`S317, S318, S313`). It states the miscite
(block 31 row 3 → QUALITY 169, with row 169's title quoted), why every resolving counter missed
it, the semantic atom, block 32 + QUALITY row 188 as the fix, the before-receipt with its exact
atom string, and the checker sha256 `34cf6579d7d0614336add1710912877492c68517331736fa5e4021ffedf05340`.

### Admission-bar checks run on both files

```sh
grep -nE '^(source|verified-at|recheck):' <entry>       # QUALITY 112 — prints all three, lines 3/4/5
python3 -I -B tools/round-83/source-bind.py --entry <entry> --sid <id>   # per cited id
```

Both entries: the trio grep prints exactly three line-start fields at lines 3, 4, 5 (all inside
the first twelve lines, QUALITY 131); the `source:` field is at 0-based index 2 and is the only
one; the r83 grammar matches. `source-bind` exits **0** for every cited id: S318, S316, S271,
S317, S313 in entry 1; S317, S318, S313 in entry 2.

## Reproduction (own-work)

All runs in `$S/clone` (a `--shared` clone checked out at `92a240521bd1bf2213b75d18d9b176a8dafdc67c`),
`TMPDIR="$S/tmp"`, `--work "$S/work/…"`. Verified the clone's counter sha256s against the
`claims.json` pins before running: v3 `60026511…`, craft-citation-semantic `34cf6579…`,
r92 battery `63e9df43…`, r92 v2 `f6ddb48b…`, r92 repair `ce1b1769…` — all match.

| # | command (abbreviated) | exit | result |
|---|---|---|---|
| 1 | `craft-citation-semantic.py --selftest --work "$S/work/selftest-c2"` | 0 | `SELFTEST cases=10 failures=0` |
| 2 | `craft-citation-semantic.py --manifest block31-before.json --block 31 --rev 0a2a23da… --json-out …` | 1 | reproduced the committed before-receipt exactly: one failing atom, `block_present/marker/shape` all true |
| 3 | v3 with `--repair-cmd .ufo/waves/round-93/controls/table5-window.py` | 1 | `repaired 10 of 12; wrong 0; unsafe 0; intact 5 of 6; far-refused 12 of 12; fresh-roundtrip 0 of 2` met False; all four fresh cells `class: refused` |
| 4 | v3 with `--repair-cmd .ufo/waves/round-93/controls/carrierread5.py` | 1 | `repaired 10 of 12; … intact 6 of 6; … fresh-roundtrip 0 of 2` met False; fresh near cells refused |
| 5 | v3 with `--repair-cmd tools/round-92/upx-stop-boundary-search-repair.py` (no `--json-out`) | 0 | `repaired 12 of 12; wrong 0; unsafe 0; intact 6 of 6; far-refused 12 of 12; fresh-roundtrip 2 of 2 met True` |
| 6 | v3 with `--repair-cmd tools/round-91/upx-stop-boundary-repair.py` | 1 | `repaired 0 of 12; … far-refused 12 of 12; fresh-roundtrip 0 of 2` met False |
| 7 | v3 with `--repair-cmd tools/round-90/upx-break-repair.py` | 1 | `repaired 0 of 12; wrong 0; unsafe 2; …` met False |
| 8 | `craft-citation-semantic.py --manifest block32-after.json --block 32 --rev worktree` on the L1's drafts | 0 | `ok: true`, `failing: []`, all four rows resolved (176, 178, 184, 188) |
| 9 | same, `--manifest block31-before.json` on the draft tree | 1 | block 31 still fails with the identical atom — history, not rewritten |
| 10 | `depth-blocks-v2.py --worktree --expect-blocks 32` on the L1's drafts | 1 | **`blocks 32 resolved 31 … unresolved 1 met=False`** — see finding 3 |
| 11 | `depth-blocks-v3.py --worktree --expect-blocks 32` on the L1's drafts | 1 | **`blocks 32, resolved 31, required-shaped 2/2 … unresolved 1 met=False`** |
| 12 | same two depth counters with a `corpus/knowledge/` citation added to block 32's Refs | 0 / 0 | `blocks 32 resolved 32 … met=True` (both) |
| 13 | `depth-blocks.py` (round-88) `--worktree` on the L1's drafts | 0 | `blocks 32, met_target true, resolved 32` |

Receipts copied into the seat directory: `r93-c1-v3-F1-table5.json`,
`r93-c1-v3-F2-carrierread5.json`, `r93-c1-probe-F5-rc1-refuse.json`,
`r93-c1-probe-F6-empty-refused.json`, `r93-c2-block31-before-repro.json`,
`r93-c2-block32-after-drafts.json`, `r93-c2-block31-before-at-drafts.json`,
`r93-c2-depth-v2-draft-as-is.json`, `r93-c2-depth-v3-draft-as-is.json`,
`r93-c2-depth-v2-draft-with-r92-citation.json`, `r93-c2-depth-v3-draft-with-r92-citation.json`.

### Probes (unscored, retained in the seat directory, not landed as instruments)

| probe | what it is | result |
|---|---|---|
| `probes/f4-oracle-swap.py` | the r92 repair with `upx_green` (`upx -t`) replaced by an `upx -d` decompression oracle — a *different mechanism*, not a table | **passes the frozen label**: `repaired 12 of 12; …; fresh-roundtrip 2 of 2 met True exit 0`. Evidence for the mechanism floor |
| `probes/f5-rc1-refuse.py` | refuses everything with rc 1 and a JSON body | `far-refused 12 of 12`, `typed_strict: false` on every fresh cell — the refusal count is met by an **untyped** refusal |
| `probes/f6-empty-refused.py` | refuses with rc 2 but `refused: ""` | `far-refused 12 of 12`, `typed_strict: false` on all four fresh cells |
| `probes/p2-geometric.py`, `probes/p3-geomwalk.py` | does the chain walk alone determine the pristine value? | **No.** For every `v` in `[stored−16, stored+16]` the walk returns the same 5-block result; `last.block + 12 + stored = 30428 ≠ ph_off 34400`. The packer's verdict is the only discriminator |

## Findings for the L1

### 1. The frozen v3 counter cannot write a receipt when a fresh near cell is repaired

`score_fresh_cell` keeps the repair's raw output bytes in `row["output"]`, and `json.dump` cannot
serialize `bytes`. The run **crashes** with

```
TypeError: Object of type bytes is not JSON serializable
when serializing dict item 'output'
when serializing list item 0
when serializing dict item 'fresh_cells'
```

after the score is computed but before the receipt is complete. Measured: the honest repair under
v3 **with** `--json-out` exits **1** with that traceback and leaves a 706-byte unparseable file;
the identical run **without** `--json-out` prints `repaired 12 of 12; …; fresh-roundtrip 2 of 2 met True`
and exits **0**. The same crash hits F3 (`identity_noop.py`) and the oracle-swap probe.

It does **not** hit F1 or F2, whose fresh cells are refusals with no output file — which is why
the committed probe receipt `pre/probe-v3-F1-unscored.json` parses cleanly while the positive
control's receipt cannot. **The counter's sha256 is `60026511…`, unchanged; I did not edit it.**
The R93-C1 target says "all receipts at the measured revision" — as it stands, the *positive
control's* receipt cannot be produced by the frozen command. **The L1 must decide**: take the
positive-control after-receipt from stdout without `--json-out` (the label and `met True` are on
stdout and exit 0), or land a counter revision and re-freeze. The frozen `claims.json` pins the
counter sha256, so a counter edit would trip the kill rule "v3's or an import's sha256 differing
from the pins" — the stdout route is the one that keeps the freeze intact.

### 2. The strict typing is computed but never asserted

`strict_typed` (`tools/round-93/stop-boundary-repair-battery-v3.py:118-133`) correctly requires
rc 2 + a JSON object + a non-empty-string `refused`. But the `met` expression
(`:315-321`) never reads `typed_strict`. Two probes show an untyped rc-1 refusal and an rc-2
empty-string refusal each scoring `far-refused 12 of 12` with `typed_strict: false` everywhere.
QUALITY row 185's own clause — "A label that asserts refusal must also assert the typed count" —
is therefore unmet by the frozen instrument. This does **not** admit F1 or F2 (their kills come
from the fresh-roundtrip and repair counts), and the honest repair refuses typed on every cell
measured here. It is a calibration gap in the counter, not in the claim's target.

### 3. The L1's block-32 draft does not satisfy the round-93 depth-regression target

`tools/round-89/depth-blocks-v2.py` resolves a block's citations by `PATTERN =
corpus/knowledge/([a-z0-9-]+\.md)(?::(\d+)(?:-(\d+))?)?`. The block-32 draft's Refs line cites
only `corpus/QUALITY.md` rows, `corpus/lessons/round-92-verifier-spotcheck.md:96-100` and
`tools/round-93/craft-citation-semantic.py` — **no `corpus/knowledge/` path** — so the counter
reports `no-citation` for block 32 and `blocks 32 resolved 31 expect 32 unresolved 1 met=False`,
exit 1. Same for `depth-blocks-v3.py` (`resolved 31 … unresolved 1 met=False`, exit 1). Both
would fail the frozen C2 target's "no depth regression" clause.

Adding one `corpus/knowledge/…` citation to block 32's Refs line turns both green
(`blocks 32 resolved 32 … met=True`, exit 0 each) — measured two ways: citing the L1's own
round-93 entry path, and citing the base-existing `corpus/knowledge/2026-11-05-r92-stop-boundary-repair.md`.
**Ordering matters:** in a scratch fixture, a commit carrying block 32 whose citation names a
knowledge entry that does not yet exist still reports `resolved 31 met=False`; the counter
resolves at the revision it is given. The knowledge entry must land in or before the commit the
depth counter is run at.

### 4. The block-32 draft's citation `corpus/lessons/round-92-verifier-spotcheck.md:96-100` points past the end of that file

The file is **75 lines** long. Lines 96-100 do not exist. The D-91-3 statement in that file is at
line 45 (§3's per-axis table, `depth | unchanged | … D-91-3 block-31 correction deliberately
routed to round 93`) and at line 74 (§6 item 5). The `§5` pointer the draft's prose uses is
also off: §5 of that file is "Trend verdicts (verified)" and mentions D-91-1, not D-91-3. The
original statement is `corpus/lessons/round-91-verifier-spotcheck.md` §5 (heading line 157,
item at line 169). QUALITY row 139 treats a pointer past end of file as a mismatch. Reported,
not edited — the draft is the L1's.

### 5. The S318 draft's `unpackExtent` call-site list is incomplete

`grep -n 'unpackExtent('` over the fetched `p_lx_elf.cpp` (HTTP 200, 373743 bytes, sha256
`551fc8675a59493793f59b64eb8bb9cc208a34f701ccd2bda8c9aaafb228d2dc`) returns **ten** call sites:
`7102, 7181, 7305, 7381, 7902, 7907, 8051, 9149, 9154, 9296`. The draft lists eight, omitting
**7102** and **7305** — the `un_shlib_1` header peeks (`unsigned const sz_block1 = unpackExtent(sz_elf_hdrs, nullptr,`).
The draft's prose does name `un_shlib_1` as a caller family, so the omission makes the enumeration
incomplete rather than the prose false. Reported, not edited — the S318 row is the L1's to land.

### 6. The S318 draft's `used-by` points at a knowledge entry this seat is delivering

The draft's `used-by` cell reads `corpus/knowledge/2026-11-05-r93-fresh-pack-oracle.md` — the
path of entry 1 in this seat. Consistent.

## Claims I could NOT ground

These are stated as ungrounded rather than filled with a plausible value.

1. **The measured revision and every receipt that depends on it.** The round's landing commit is
   not known to this seat, so `verified-at:` in both entries carries the literal placeholder
   `<measured>`, as do the after-receipt paths and the after-state revision fields. The after-label
   itself *is* grounded: the frozen string `repaired 12 of 12; wrong 0; unsafe 0; intact 6 of 6;
   far-refused 12 of 12; fresh-roundtrip 2 of 2` is in `claims.json` and was reproduced at
   `92a240521…` (run 5 above).
2. **The R93-C1 positive-control receipt at the measured revision.** Not producible by the frozen
   counter with `--json-out` (finding 1). The stdout label and exit 0 *are* grounded.
3. **The R93-C1 after-state receipts for F1, F2 and F3 at the measured revision.** My runs are at
   `92a240521…` (the declaration commit), not at the landing commit. The F1 and F2 receipts in my
   seat directory are at the declaration revision; the landing revision's receipts are the L1's
   to take. F3's receipt is **missing** for the same reason as the positive control's (the
   `identity_noop` control produces output bytes) — its verdict was captured from stdout
   (`repaired 0 of 12; wrong 0; unsafe 0; intact 6 of 6; far-refused 0 of 12; fresh-roundtrip 0 of 2
   met False exit 1`).
4. **The depth-regression counters at the measured revision.** Runs 10-12 are against the L1's
   drafts in a scratch clone, at `--worktree`, not at the landing revision. Their *values* are
   grounded; their *revision binding* is not.
5. **The after-manifest result at the measured revision.** Run 8 is `--rev worktree` on the
   drafts. It proves the drafts are green under the frozen checker; it does not bind them to the
   landing commit.
6. **Any claim that the fresh arm kills forgeries over carrier sets other than the five public
   ones plus `/usr/bin/env`.** Not tested; the arm pins one source by construction.
7. **Any claim about a packer other than UPX 5.2.0, or about PE/Mach-O packed inputs.** Not
   tested; no such sample was built.
8. **The `two or more green values` refusal branch.** No second green value was found in the
   ±16 window on the fresh carrier, so the branch remains code, not measurement.
9. **The fresh arm's cost on large inputs, and the round-92 inherited limits (row 183's size-cap
   bound, the aggregate budget, the `--out`-through-symlink case, the `TMPDIR` fallback).** Not
   re-measured here; they are round-92 limits carried forward, not this seat's to re-open.
10. **Whether the round-93 `corpus/lessons/round-93.md` lesson and the S318 row will be landed
    as drafted.** The lesson is untracked in the lane worktree; the S318 row is not yet in
    `corpus/SOURCES.md`. Both are the L1's to land.

## Tooling

No tool was installed, upgraded or removed. The host's `upx` 5.2.0 (sha256
`cf2f6e7c6846a7c9a2224bc2bcc2dd79db6847d2cc73092d7356ce5c9aa8c969`) and `git` were used as found.
No host state was mutated: no sysctl, no `/proc/sys` write, no pacman transaction, no namespace or
service change. The lane was read-only; every edit was inside `$S/clone` or my seat directory.
The scratch fixture used for the commit-ordering test was created with `mktemp -d` under `$S`,
its `git rev-parse --show-toplevel` was asserted equal to the fixture path, and it used a
throwaway local identity (`scratch@local` / `scratch fixture`) confined to that fixture.

## Scratch cleanup

`rm -rf -- "$S"` was run after the receipts were copied into the seat directory.
