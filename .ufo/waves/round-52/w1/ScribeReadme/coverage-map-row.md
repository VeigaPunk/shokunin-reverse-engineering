# R52-C1 — `corpus/README.md` coverage-map row draft (paste-ready)

Seat `ScribeReadme`, kaidoku round 52 wave 1 (build). **Draft only — nothing in the lane tree was
written outside this seat directory.** `corpus/README.md` is not a frozen path for round 52 (see
`plans/round-52-claims.md` → R52-C1 "Landing bindings"), so these edits are landing material the
L1 applies at the freeze/landing commit.

Base bytes read: `corpus/README.md` at lane HEAD `1842addcef3458515859b928b92d9bbd0a46c5d5`
(blob `b8a266ea52ed63dad8089294da964c6da107f87a`; sha256 of the worktree file
`aad0c5907483f38fc0fcf82cb66f63d0b15a6554c3ad2d0d6d85c6a60b5da5db`). The README blob is
**byte-identical** at the round-start base `c525de54a53eb3c4fee28ede2721da4527cf8ece`, at the
claims draft `ab0eafedc41402b43b41a4362084119578dfe7ce` and at HEAD (measured; `git rev-parse`
on the three blobs returned the same id).

Entry stem (from `plans/round-52-claims.md` → R52-C1 "Landing bindings"): entry stem
`2026-10-30-r52-avm-le-squashfs-core`; entry file
`corpus/knowledge/2026-10-30-r52-avm-le-squashfs-core.md`.

---

## 1. The row (3 cells: section | entries | state)

**Insertion point:** immediately after the round-51 coverage row
(`| SquashFS device and padding boundaries (round 51) | …`, base line 107), i.e. as the last row of
the `## Coverage map` table, before the blank line and `## Knowledge`.

> ⚠ **The row below asserts `**Core**` and `4 of 4`.** The R52-C1 data run has **not** been executed
> (the L1 alone runs it, after this wave, in the quiet window). Land this row **only if**
> `python3 -I -B tools/round-52/c1-counter.py --root <LANE> --rev <REV> --freeze <FREEZE>
> --receipts corpus/evidence/round-52/c1 --json-out <OUT>` exits **0** with `carriers_matched == 4`,
> `gaps_ok` true on every carrier, `law_shape_ok`/`census_rederived_ok`/`depth_gap_recorded` true and
> every binding true. Otherwise use the fallback row in §2 — **not** an edit of this one.

**Paste-ready (one line):**

```
| SquashFS LE AVM members (round 52) | `2026-10-30-r52-avm-le-squashfs-core` | **Core** — REA 6.5.0 `extract-firmware --max-depth 1` (unblob 26.6.4, `sasquatch` 4.5.1 on the child `PATH`) resolves the `squashfs_v4_le` handler on the four chain-pinned genuine AVM-marker little-endian members (FRITZ!Box 7581 07.18, 7582 07.18, 6490 Cable 07.57, 6430 Cable 07.30) and publishes every regular file of the independent `unsquashfs` 4.7.5 oracle at its exact path on all four, under the re-frozen device-accounting law (an unprivileged extraction creates no device nodes, fifos or sockets and emits no gap record for them, so a non-regular oracle entry carries no disposition at all) scored by `tools/round-52/c1-counter.py` (receipts `corpus/evidence/round-52/c1/`); the law's width is the four measured carriers — no fifo, socket or block-device row exists in any measured carrier — and the carrier bytes are fetched through the pinned vendor chain and never committed (AVM licence) (S243, S244, S245, S249, S250, S251, S252) |
```

### Shape check (the round-50 falsify finding: every coverage-map row is 3 cells)

Measured on the base README: the `## Coverage map` section holds **94** pipe-rows and **0** of them
have a cell count other than 3 under the frozen counter's `cells()`
(`tools/round-50/c1-counter.py:585-586`, `row.strip().strip('|').split('|')`). The line above has
4 pipes → 3 cells, and no `|` occurs inside any cell text. Verified mechanically — see
`receipts/check.log`.

### Bindings it satisfies

| binding | how |
|---|---|
| `coverage_map_row` (`tools/round-50/c1-counter.py:2479-2482`, the shape the round-52 counter ports) | the row is a `|`-starting line **inside** the `## Coverage map` section and names the entry stem |
| `map_token` (`tools/round-50/c2-record.py:490-493`) → atom **B1** (every knowledge file mapped) | the stem appears backticked in the `## Coverage map` section; the new entry is therefore mapped when it lands |
| command A `mapped` count | the row's stem token is inside the coverage-map section, so `mapped` rises with the file count (see `map-count.md`) |

### What the row deliberately does **not** assert

* no data-run number other than the predicate's own `carriers_matched == 4` — the per-carrier file
  counts are **not** written into the row (the round-50 landing script wrote them from a facts
  file it computed itself; that file exists only at the landing commit, so a row that quoted it
  before the run would be a fabricated number);
* no commit hash, no data-commit id, no `verified-at` inside the coverage row — the round-50 and
  round-41 coverage rows carry none, and the commit id belongs to the `## Knowledge` row (§3);
* no claim about fifo/socket/block devices (never exercised) — the row says so in the width clause.

---

## 2. Fallback row (paste-ready, same 3 cells) — **use this if C1 misses**

```
| SquashFS LE AVM members (round 52) | `2026-10-30-r52-avm-le-squashfs-core` | measured, not promoted — the re-frozen device-accounting law did not reach 4 of 4 carriers under the frozen counter (R52-C1 miss: `carriers_matched` < 4), so LE AVM members (`hsqs`) stay Frontier and the entry records the measurement (S243, S244, S245, S249, S250, S251, S252) |
```

With this row the `## Frontier` edit in `frontier-note.md` must **not** be applied (LE AVM members
stay Frontier; the round-50 frontier note stands unchanged) and the `## Knowledge` row §3 keeps its
"measured, not promoted" wording (its stem is the same, so the map count arithmetic in
`map-count.md` is unaffected).

---

## 3. Companion row in the `## Knowledge` index (optional, same pattern as round 50)

Round 50 carried **two** rows: the 3-cell coverage row (§1) and a 4-cell Knowledge-index row
(`| entry | topic | source | verified-at |`). The round-52 claims name only the coverage-map row as
a binding, so this row is **optional** — but the round-50/round-51 precedent is the house style and
it is the row that carries the receipt/counter pointers.

**Insertion point:** immediately after the round-51 Knowledge row
(`| `2026-10-30-r51-avm-le-squashfs-core` | …`, base line 230), as the last row of the
`## Knowledge` table.

**Paste-ready (one line, 4 cells):**

```
| `2026-10-30-r52-avm-le-squashfs-core` | genuine AVM-marker LE SquashFS v4 (`hsqs`) through REA on the four pinned vendor members — Core (R52-C1 under the re-frozen device-accounting law: 4 of 4 carriers, every oracle regular file published at its exact path) | S243, S244, S245, S249, S250, S251, S252; receipts `corpus/evidence/round-52/c1/`; counter `tools/round-52/c1-counter.py` | 2026-10-30 |
```

Two things the L1 must settle before landing this row:

1. **`S252` must exist.** At the base revision `corpus/SOURCES.md` holds 158 rows and its highest id
   is **S251**; `S252` (man7 `mknod(2)`, the CAP_MKNOD ground) is **drafted this round** by the
   `ScribeSources` seat and is not yet in the registry. The row cites `S252` because the entry is
   required to cite it (`plans/round-52-claims.md`: "C1's entry cites the round-52 SOURCES row
   S252 … plus S243/S244/S245/S249/S250/S251"). **If the S252 row does not land in the same commit,
   this cell is a false citation** — drop `S252` from the cell (and from the coverage row §1) or
   land the SOURCES row first. Measured: `grep -c '^| S[0-9]' corpus/SOURCES.md` = 158, highest id
   S251, zero hits for `S252`.
2. **`verified-at`** must equal the entry's own `verified-at:` value. The claims and the entry seat
   use `2026-10-30`; the round-50 landing wrote an **empty** cell there (a defect recorded in the
   round-50 `ScribeReadmeMap` finding F5). If the entry's own `verified-at:` ends up as the data
   commit's `%cI`, substitute that value in this cell — the two must agree.

---

## 4. Conditionality summary

| condition | coverage row | Knowledge row | `## Frontier` edit |
|---|---|---|---|
| counter exits 0, `carriers_matched == 4`, all bindings true | §1 (**Core**) | §3 with the Core wording | apply (`frontier-note.md` §2) |
| counter exits 1 (miss) | §2 (measured, not promoted) | §3 with "measured, not promoted" wording | **do not apply** |
| counter exits 2 (could not evaluate) | §2 | §2 wording | **do not apply** |
