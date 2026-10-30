# R51-C1 — `corpus/README.md` coverage-map row draft (paste-ready)

Seat `ScribeReadme`, kaidoku round 51 wave 1 (build). Draft only — nothing in the lane tree was
written; `corpus/README.md` is **not** a frozen path for round 51 (see
`plans/round-51-claims.md` → R51-C1 "Landing bindings"), so these edits are landing material the
L1 applies at the freeze.

Base bytes read: `corpus/README.md` at lane HEAD `39f41d4f15a87689a41c16c5c17ed885fbfb7da3`
(sha256 `7ede85426c4baa5f205482375cf2966abfc21290b587d45ef6cdbdebf80786c4`; the worktree copy is
byte-identical to `HEAD`, `git status --porcelain` shows no modified tracked file).

Entry stem (from `plans/round-51-claims.md` → R51-C1 landing bindings):
`2026-10-30-r51-avm-le-squashfs-core`; entry file
`corpus/knowledge/2026-10-30-r51-avm-le-squashfs-core.md`.

---

## 1. The row (3 cells: section | entries | state)

**Insertion point:** immediately after the round-50 coverage row
(`| SquashFS LE AVM members (round 50) | …`, line 106), i.e. as the last row of the
`## Coverage map` table, before the blank line and `## Knowledge`.

**Paste-ready (one line):**

```
| SquashFS LE AVM members (round 51) | `2026-10-30-r51-avm-le-squashfs-core` | **Core** — REA 6.5.0 `extract-firmware --max-depth 1` (unblob 26.6.4, `sasquatch` 4.5.1 on the child `PATH`) resolves the `squashfs_v4_le` handler on the four chain-pinned genuine AVM-marker little-endian members (FRITZ!Box 7581 07.18, 7582 07.18, 6490 Cable 07.57, 6430 Cable 07.30) and publishes every regular file of the independent `unsquashfs` 4.7.5 oracle at its exact path on all four (R51-C1 `carriers_matched 4`, `gaps_ok` true on every carrier, every binding true); the gap accounting is now the device-accounting law, re-frozen from the per-carrier-class derivation (`tools/round-51/gap-rule.json`, `tools/round-51/c1-counter.py` v2) — an unprivileged extraction creates no device nodes, fifos or sockets and emits no gap record for them, so a non-regular oracle entry carries no disposition at all — not the round-50 detail whitelist that generalised `247:0` from the Cable class; the carrier bytes are fetched through the pinned chain and never committed (AVM licence), so the durable evidence is the committed receipt set `corpus/evidence/round-51/c1/<id>/run.json` (`<id>` = `c6430`, `c6490`, `g7581`, `g7582`), the frozen oracle tables and the pin chain; the before/after scores are `.ufo/waves/round-51/l1/scores/c1-{before,after}.json`; LE AVM kernels, the ~13k-file LE AVM rootfs under REA's 120 s limit and the other still-frontier SquashFS variants stay Frontier |
```

**Shape check (the round-50 falsify finding: every coverage-map row is 3 cells):** the line above has
4 pipes → 3 cells under the frozen counter's `cells()` (`tools/round-50/c1-counter.py:585-586`,
`row.strip().strip('|').split('|')`). No `|` occurs inside any cell text, so `cells()` returns
exactly 3 fields. Verified mechanically — see `receipts/readme-patch-check.log`.

**B1 mapping (`tools/round-50/c2-record.py:490-517`):** the entry stem appears backticked in the
`## Coverage map` section, so `map_token('2026-10-30-r51-avm-le-squashfs-core')` matches and the
new knowledge file is mapped. With the landing entry present, `corpus/knowledge/` holds **141**
`.md` files (140 today + this one), so the `## Owned axes` coverage row in `SCORECARD.md` must read
`141/141 knowledge files mapped` — the claims already plan that head.

**Counter binding it satisfies:** `coverage_map_row`
(`tools/round-50/c1-counter.py:2479-2482`) — any `STEM in l` for a `|`-starting line inside the
`## Coverage map` section.

---

## 2. Conditionality (must not be dropped)

This row asserts `**Core**` and `carriers_matched 4`. The R51-C1 data run has **not** been executed
at the time of writing (the L1 runs it in the quiet window after the wave). Land this row **only
if** `python3 -I -B tools/round-51/c1-counter.py --root <LANE> --rev <REV> --freeze <FREEZE>
--receipts corpus/evidence/round-51/c1 --json-out <OUT>` exits **0** with `carriers_matched == 4`,
`gaps_ok` true on every carrier and every binding true.

If C1 misses, replace the row with the *measured, not promoted* form in the house style of the
round-44 row (`2026-10-28-r44-squashfs-v1v2-core`), and **drop** the `## Frontier` edit in
`frontier-note.md` (LE AVM members stay Frontier; the still-frontier list keeps the
`LE AVM members (`hsqs`)` clause).

**Fallback row (paste-ready, same 3 cells):**

```
| SquashFS LE AVM members (round 51) | `2026-10-30-r51-avm-le-squashfs-core` | **Measured, not promoted** — the re-frozen device-accounting rule did not reach 4 of 4 at the landing revision (R51-C1 miss: `carriers_matched` < 4, `<failing carriers>`); LE AVM members (`hsqs`) stay Frontier, and the entry records the measurement (S243, S244, S245, S249) |
```

---

## 3. Companion row in the `## Knowledge` index (optional, same pattern as round 50)

Round 50 carried **two** rows: the 3-cell coverage row (§1) and a 4-cell Knowledge-index row
(`| entry | topic | source | verified-at |`, line 228). The round-51 claims name only the coverage
map row as a binding, so this one is **optional** — but the round-50 precedent is the house style,
and it is the row that carries the receipt/counter pointers.

**Insertion point:** immediately after the round-50 Knowledge row
(`| `2026-10-28-r50-avm-le-squashfs-core` | …`, line 228), as the last row of the `## Knowledge`
table.

**Paste-ready (one line, 4 cells):**

```
| `2026-10-30-r51-avm-le-squashfs-core` | genuine AVM-marker LE SquashFS v4 (`hsqs`) through REA on four pinned vendor members — Core (R51-C1 under the re-frozen device-accounting rule: 4 of 4 carriers, every oracle regular file published at its exact path) | S243, S244, S245, S249, <S??? round-51 device-node source row(s)>; receipts `corpus/evidence/round-51/c1/`; counter `tools/round-51/c1-counter.py` | 2026-10-30 |
```

`<S??? …>` is a placeholder: the round-51 SOURCES row id(s) for the unsquashfs / squashfs-tools
device-node grounding are opened by another seat and must be filled with the real id(s) before the
row lands. Leaving a literal `<S???` in a landed row would be a false citation — replace it.

Note: the round-51 `used-by` column in `corpus/SOURCES.md` must carry
`corpus/knowledge/2026-10-30-r51-avm-le-squashfs-core.md` (or the stem) for every row the entry
cites — the counter accepts either (`ENTRY in used or STEM in used`,
`tools/round-50/c1-counter.py:2474-2476`), and it additionally requires the row's `opened` date to
be in the round's opened-date set.
