# Round-50 attempt-2 — `corpus/README.md` bindings (drafts, paste-ready)

Seat `ScribeReadmeMap`, wave 3 (build). Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Base README bytes (lane HEAD `6f4aba63`): sha256 `a702bfdd6a32b89427d672b4522878742810e21dbe3f6db2b36c60268e1d2274`.
`corpus/README.md` is **not** a frozen path (see `plans/round-50-claims.md` → "Frozen paths"), so
these edits are legal landing material.

---

## 0. READ FIRST — the entry stem in this seat's dispatch text is stale

The dispatch text for this seat names the entry stem `2026-10-29-r50-le-avm-hsqs-core`.
**That stem is wrong and must not be used.** The frozen counter pins a different one:

```
$ git show 435d41fd4ad9211d1579fc447936fb33d2b74467:tools/round-50/c1-counter.py | grep -n "^ENTRY\|^STEM"
377:ENTRY = 'corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md'
378:STEM = '2026-10-28-r50-avm-le-squashfs-core'
```

`tools/round-50/c1-counter.py` is byte-identical at HEAD and at the freeze
(sha256 `9820811bf29f2de988f8ddb2513cf365f30a89a36f2bb465f96f1926ef9bd813` at both revisions), and
the L1 already corrected the claims file in commit `6f4aba63` ("attempt-2 claims corrected — entry
stem pinned to the frozen counter constants"): the counter, not the dispatch text, is the rule.

The counter's `coverage_map_row` binding is literally
`any(STEM in l for l in section(readme, '## Coverage map') if l.lstrip().startswith('|'))`
(`tools/round-50/c1-counter.py:2479-2482`), and `tools/round-50/c2-record.py`'s atom **B1** requires
every `corpus/knowledge/**.md` file to be mapped by its backticked stem inside the same
`## Coverage map` section (`b1()`, `tools/round-50/c2-record.py:496-517`). A row keyed to the stale
stem would leave `b:coverage_map_row` red and take R50-C1 to a miss.

**All three drafts below use `2026-10-28-r50-avm-le-squashfs-core`.**
Sibling seats dispatched with the stale stem (`ScribeEntryC1` — entry file path; `ScribeRowsSources`
— `used-by` cell) must use the same stem; the `used-by` cell must carry
`corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md` (the counter accepts the full path or the
stem: `ENTRY in used or STEM in used`, `tools/round-50/c1-counter.py:2474-2476`).

---

## 1. `## Coverage map` row

**Insertion point:** immediately after the round-49 coverage row
(`| SquashFS v1/v2 through REA (round 49) | …`), i.e. as the last row of the `## Coverage map`
table (line 105 of the base README; the section ends at the blank line before `## Knowledge`).

**Paste-ready (one line):**

```
| SquashFS LE AVM members (round 50) | `2026-10-28-r50-avm-le-squashfs-core` | **Core** — on four pinned vendor carriers, bounded: REA 6.5.0 `extract-firmware --max-depth 1` (unblob 26.6.4, `sasquatch` 4.5.1 on the child `PATH`, no `-be` binary) resolves the `squashfs_v4_le` handler on the four chain-pinned genuine AVM-marker little-endian members (FRITZ!Box 7581 07.18, 7582 07.18, 6490 Cable 07.57, 6430 Cable 07.30), publishing every regular file of the independent `unsquashfs` 4.7.5 oracle at its exact path with no extra file (R50-C1 `carriers_matched 4`); the carrier bytes are fetched through the pinned chain and never committed (AVM licence), so the durable evidence is the committed receipt set, the frozen oracle tables and the pin chain; bound: four carriers, one vendor, xz bodies, depth 1 (the LE AVM rootfs of ~13k files under REA's 120 s limit stays Frontier); supersedes the round-49 note's LE-AVM clause (which listed LE AVM members, `hsqs`, as still Frontier) |
```

**Conditionality (must not be dropped):** this row asserts `**Core**` and `carriers_matched 4`.
The R50-C1 data run has **not** been executed at the time of writing (the L1 runs it, in the quiet
window, after this wave). Land this row **only if** `tools/round-50/c1-counter.py` exits 0 with
`carriers_matched 4` at the landing revision. If C1 misses, the row must become a *measured, not
promoted* row in the house style of the round-44 row (`2026-10-28-r44-squashfs-v1v2-core`), and the
`## Frontier` edit in §2 must be dropped (LE AVM members stay Frontier).

**B1 consequence:** with the landing entry file present, `corpus/knowledge/` holds 140 files and the
`## Owned axes` coverage row in `SCORECARD.md` must read `140/140 knowledge files mapped`
(the attempt-2 claims already plan that head); the row above supplies the mapping the atom checks.

---

## 2. `## Frontier` edit

Two parts: (2a) a new dated round-50 line, (2b) the in-place removal of the LE-AVM `hsqs` clause
from the round-49 line.

### 2a. New line — append as the **last** bullet of the `## Frontier` section
(after the round-49 line, before the blank line and `## Known gaps`).

**Paste-ready (one line):**

```
- sasquatch — 2026-10-29 round 50: genuine AVM-marker little-endian SquashFS v4 members (`hsqs`) are **Core** (`2026-10-28-r50-avm-le-squashfs-core`: REA 6.5.0 `extract-firmware --max-depth 1` on four chain-pinned vendor carriers — FRITZ!Box 7581/7582 07.18 and 6490/6430 Cable 07.57/07.30; the carrier bytes are fetched and never committed, AVM licence), superseding the LE-AVM clause of the round-49 line above (which listed LE AVM members, `hsqs`, as still Frontier). Scope: four pinned carriers, one vendor, xz bodies, depth 1. Still frontier: the LE AVM rootfs of ~13k files under REA's 120 s limit (FRITZ!Box 7530/7590 08.25), `squashfs_v2_nonstandard`, `squashfs_v3_broadcom`/`_nonstandard` (and the DD-WRT no-pad/4k-pad v3 images), gzip v3, v4 Broadcom, v2.1 images, AVM kernel images and nested sub-images below depth 1.
```

This line does the three things the seat spec asks of the Frontier edit: it **removes the LE-AVM
`hsqs` clause from the current frontier** (by superseding it), **keeps the ~13k-file clause** (the
`LE AVM rootfs of ~13k files under REA's 120 s limit` item, quoted from
`plans/round-50-claims.md` → "Carrier swap, before the freeze": the FRITZ!Box 7530/7590 08.25
members hold ~13.4k regular files and stay Frontier), and **names the superseding entry**
(`2026-10-28-r50-avm-le-squashfs-core`).

### 2b. In-place removal from the round-49 line (recommended, optional)

**Old string (unique, in the round-49 frontier line):**

```
v4 Broadcom, v2.1 images, LE AVM members (`hsqs`), AVM kernels and nested sub-images below depth 1.
```

**New string:**

```
v4 Broadcom, v2.1 images, AVM kernels and nested sub-images below depth 1 (its LE-AVM clause is superseded by the round-50 line below).
```

**Rationale / tradeoff (the L1's call):** the lane's habit is "a correction is a new line, never a
rewrite" (`plans/round-50-claims.md` → R50-C2 B3/B4/B5/B11: the round's correction lines are new
lines). If the L1 prefers that discipline strictly, **drop 2b** and land only 2a — 2a alone already
supersedes the clause explicitly and names the entry. Landing 2b as well means the only remaining
`LE AVM members (\`hsqs\`)` string inside `## Frontier` is the **round-41 dated line** (base line
270, itself superseded for this clause by the round-44/49 lines); a falsify check that greps the
whole section for the clause must therefore either ignore dated history lines or expect that one
residue. Verified residue list is in `receipts.primary.log`.

**Optional 2c (same treatment, historical line):** if the L1 wants the section free of the clause,
the round-41 line's `LE AVM members (\`hsqs\`)` can also be dropped with the pointer
`(its LE-AVM clause is superseded by the round-50 line below)`; not recommended — it rewrites a
superseded 2026-10-26 history line for no binding gain.

---

## 3. `## Knowledge` index row

**Insertion point:** immediately after the round-49 knowledge row
(`| \`2026-10-28-r49-squashfs-v1v2-core\` | …`), i.e. as the last row of the `## Knowledge` table
(base README line 226; the section ends before `## Lessons`).

**Paste-ready (one line):**

```
| `2026-10-28-r50-avm-le-squashfs-core` | SquashFS LE AVM (`hsqs`) members through REA on four chain-pinned vendor carriers, Core (R50-C1; supersedes the round-49 note's LE-AVM clause) | S243, S244, S245, S249; receipts `corpus/evidence/round-50/c1/`; counter `tools/round-50/c1-counter.py` | {{DATA_COMMIT_CI}} |
```

House-style anchors used: the round-49 row
`| \`2026-10-28-r49-squashfs-v1v2-core\` | SquashFS v1/v2 through REA on four frozen fixtures, Core (R49-C1 under a predicate stated once; supersedes the round-44 not-promoted entry) | S112, S138, S139; receipts \`corpus/evidence/round-49/c1/\`; counter \`tools/round-49/c1-counter.py\` | 2026-10-28 |`
— same four cells, same source-cell shape (`S…` ids; `receipts \`corpus/evidence/round-NN/c1/\`;
`counter \`tools/round-NN/c1-counter.py\``), same `verified-at` date shape.

**Two coordination points on this row (not resolvable by me):**
- **`verified-at`**: the dispatch text says `2026-10-29`; `ScribeEntryC1` reports that the entry's
  own `verified-at:` is a `<REV>` placeholder — the data commit that first adds the entry and the
  four `after.json` receipts — because QUALITY 23 wants the evidence timestamp at or before the
  committer time. The index row must carry the **same** value as the entry. Substitute the data
  commit's committer time: `git show -s --format=%cI <data-commit>`, and replace the
  `{{DATA_COMMIT_CI}}` token below with it (fallback if the L1 prefers a plain date: `2026-10-29`,
  the landing day — but then the entry and the row must agree).
  The counter's documentation bindings do not read `verified-at` (`OPENED_DATES` applies to the
  SOURCES `opened` cell, not to this column).
- The source ids `S243, S244, S245, S249` must be the ids the entry's `source:` lines actually
  cite (`S243` Freetz AVM_LE/AVM_BE patch, `S244` the AVM download index, `S245` unblob 26.6.4 LE
  handler, `S249` the AVM licence — attempt-2 claims, "Frontier step"). The counter's `sourced`
  binding requires the entry's `source:` ids to be a subset of SOURCES rows whose `used-by` cell
  carries the entry path or stem and whose `opened` cell is in `2026-10-28..2026-10-29`.

---

## 4. LANDING-SCRIPT HAZARD (L1-owned; found by me, not fixable by me)

The L1's own landing scripts under `.ufo/waves/round-50/l1/` carry a **third** stale entry stem and
would write the README rows with it, so the counter's documentation bindings would come out red:

```
$ grep -n "r50-le-avm-members-core\|r50-avm-le-squashfs-core" .ufo/waves/round-50/l1/land_c1.py .ufo/waves/round-50/l1/land_sources.py
.ufo/waves/round-50/l1/land_c1.py:17:STEM = '2026-10-28-r50-le-avm-members-core'
.ufo/waves/round-50/l1/land_sources.py:11:STEM = '2026-10-28-r50-le-avm-members-core'
```

Consequences if the scripts run unchanged:
- `land_c1.py` writes the entry file, the `## Coverage map` row, the `## Knowledge` row and the
  `## Frontier` line with `2026-10-28-r50-le-avm-members-core` → `b:entry_present`,
  `b:coverage_map_row` and (in PROVINCE) `b:province_core_row`/`b:frontier_note` are all red
  against the frozen counter's `STEM`/`ENTRY`; C2 atom **B1** would also report the new knowledge
  file as unmapped.
- `land_sources.py` filters the four C1 rows out of the SOURCES append
  (`S = {k: S[k] for k in ('S246','S247','S248')}`) → `b:sourced` red.
- `land_c1.py`'s `## Knowledge` row is written with an **empty** `verified-at` cell; house style and
  the entry's own `verified-at:` want a value.
- `land_c1.py`'s PROVINCE Core row does not embed the entry path, while the counter requires
  `ENTRY in row` (`tools/round-50/c1-counter.py:2447-2451`) — a PROVINCE-side defect, reported here
  only because the same script writes my README rows.

**The fix is the L1's**: set `STEM = '2026-10-28-r50-avm-le-squashfs-core'` in both scripts (and
`ENTRY` follows from it), drop the `S246/S247/S248` filter in `land_sources.py` so S243/S244/S245/
S249 land with `used-by = corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md` (unbackticked,
per the census rule), and fill the `verified-at` cell. Then either land the script's rows (its
coverage-map section name is `LE AVM-marker SquashFS v4 through REA (round 50)`) or land the drafts
above (section name `SquashFS LE AVM members (round 50)`, per this seat's spec) — **not both**;
two rows naming the stem in `## Coverage map` is harmless for the binding but sloppy for the map.

---

## 5. What I verified (offline, no REA)

All of it ran on a scratch clone of the lane at HEAD (`git clone --shared` →
`checkout --detach 6f4aba63`), never on the lane tree. Full logs:
`receipts.primary.log` (variant "primary" = §1 + §2a + §2b + §3) and `receipts.appendonly.log`
(variant "append-only" = §1 + §2a + §3, no §2b); patched copies and diffs beside them.

| check | result |
|---|---|
| counter `STEM`/`ENTRY` == drafted stem | `2026-10-28-r50-avm-le-squashfs-core` / `corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md` (True) |
| counter's own `coverage_map_row` logic on the patched README | **True** (exactly 1 row in `## Coverage map` names the stem) |
| `c2-record.py` `unique_section` for `## Coverage map`, `## Knowledge`, `## Frontier` | unique / unique / unique |
| `c2-record.py` `map_token(STEM)` matches the `## Coverage map` section | True |
| B1 mapping simulation, 139 knowledge files at HEAD | 0 unmapped |
| B1 mapping simulation, 140 files with the landing entry present | 0 unmapped (the new entry is mapped by the §1 row) |
| drafted row cell counts | coverage row 3 cells; knowledge row 4 cells; frontier line 0 pipes inside the text |
| `## Frontier` after the edit | last bullet is the round-50 line; contains the `~13k` clause; names the entry |
| residue after §2b | only the round-41 dated line still contains `LE AVM members (\`hsqs\`)` (historical) |

Not run: REA (forbidden this wave), the counter's own `--rev` scoring (needs the data run and the
carrier cache; the L1's job), `tools/round-50/c1-counter.py --selftest` (not needed for a
documentation-binding draft; the counter bytes are frozen and were not modified).
