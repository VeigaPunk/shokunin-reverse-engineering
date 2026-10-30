# R51-C1 — `corpus/README.md` frontier-note edit draft (paste-ready)

Seat `ScribeReadme`, kaidoku round 51 wave 1 (build). Draft only — nothing in the lane tree was
written.

Base bytes: `corpus/README.md` at lane HEAD `39f41d4f15a87689a41c16c5c17ed885fbfb7da3`
(sha256 `7ede85426c4baa5f205482375cf2966abfc21290b587d45ef6cdbdebf80786c4`).

What has to move: **LE AVM members (`hsqs`)** leaves the Frontier list. The round-50 entry measured
them on four chain-pinned vendor carriers and did not promote them (R50-C1, 2 of 4 under the frozen
gap-accounting rule). Round 51 re-freezes that rule from the per-carrier-class derivation (the
device-accounting law) and, **if the counter exits 0 with `carriers_matched 4`**, the class is
promoted to Core.

Two edits, in the house style of the lane:

* **2a** — a new dated bullet in the `## Frontier` section (the list's current statement);
* **2b** — a new dated paragraph at the end of the file (the `Round-50 frontier note` shape).

Both lines carry the three strings a frontier-note binding looks for — the mark
`Round-51 frontier note`, the entry stem `2026-10-30-r51-avm-le-squashfs-core`, and an LE-AVM token
(`LE AVM`) — so a counter that searches the README (the round-41/round-50 counters search
`PROVINCE.md` for this binding: `tools/round-50/c1-counter.py:2454-2456`,
`tools/round-41/c1-counter.py:1695`) finds them in the README too, in the `## Frontier` section
**and** at the file end. The token is searched with the stem removed, so the stem's own
`avm-le` cannot satisfy it — the literal `LE AVM` in the text does.

---

## 1. Old lines (verbatim, with line numbers at the base revision)

**L106** — the round-50 coverage row (history; superseded by the new §1 row of
`coverage-map-row.md`, not edited):

```
| SquashFS LE AVM members (round 50) | `2026-10-28-r50-avm-le-squashfs-core` | measured, not promoted — REA published every oracle regular file on all four pinned vendor carriers, and the frozen gap-accounting rule matched only the two Cable carriers (2/4, `gaps_ok` false on g7581/g7582: twelve char-device entries with no disposition); LE AVM members (`hsqs`) stay Frontier, and the entry records the measurement (S243, S244, S245, S249) |
```

**L271** — round-40 dated bullet (history):

```
- sasquatch-v4be — 2026-10-26 round 40: genuine AVM-layout BE v4 **measured, not promoted** (`2026-10-26-r40-avm-be-squashfs-core`): every oracle file on four carriers, but R40-C1 stopped at 3/4 on a counter suffix false negative. Still frontier: AVM-BE promotion, LE AVM members, nested `filesystem_core` images below depth 1, other vendor-mangled images.
```

**L272** — round-41 dated bullet (history):

```
- sasquatch-v4be — 2026-10-26 round 41: the genuine AVM layout is **Core** (`2026-10-26-r41-avm-be-squashfs-core`), superseding the round-40 `measured, not promoted` line above; that stop was a counter suffix false negative (R40-CL1), not an image property. Still frontier: LE AVM members (`hsqs`), AVM kernel images, nested sub-images below depth 1, other vendor-mangled images.
```

**L279** — round-44 dated bullet (history):

```
- sasquatch — 2026-10-28 round 44: SquashFS v1/v2 was measured on four standard fixtures but **remains Frontier** (R44-C1 honest stop: frozen-claim/counter output-directory provenance mismatch; `2026-10-28-r44-squashfs-v1v2-core`). Still frontier: `squashfs_v2_nonstandard`, `squashfs_v3_broadcom`/`_nonstandard`, gzip v3, v4 Broadcom, LE AVM members, AVM kernels and nested sub-images below depth 1.
```

**L280** — round-49 dated bullet (the **last** bullet of the `## Frontier` section; history):

```
- sasquatch — 2026-10-28 round 49: SquashFS v1/v2 (`squashfs_v1`, `squashfs_v2`, four standard fixtures) is **Core** (`2026-10-28-r49-squashfs-v1v2-core`), superseding the round-44 line above. Scope: the four standard v1.0/v2.0 fixtures only. Supersedes the round-42 and round-44 lines above for v1/v2. Still frontier: `squashfs_v2_nonstandard`, `squashfs_v3_broadcom`/`_nonstandard` (and the DD-WRT no-pad/4k-pad v3 images), gzip v3, v4 Broadcom, v2.1 images, LE AVM members (`hsqs`), AVM kernels and nested sub-images below depth 1.
```

**L300** — the `Round-50 frontier note` paragraph (the file's last line; history):

```
Round-50 frontier note, 2026-10-29: LE AVM members (`hsqs`) were measured on four chain-pinned vendor carriers (`2026-10-28-r50-avm-le-squashfs-core`; REA published every oracle regular file on all four) and **stay Frontier** — R50-C1 measured 2 of 4 under the frozen gap-accounting rule (twelve `char-device` entries per FRITZ!Box carrier with no disposition; the rule was generalised from the Cable-carrier class). Still Frontier: LE AVM members (`hsqs`), LE AVM rootfs of ~13k files under REA's 120 s limit, AVM kernels, nested sub-images below depth 1, `squashfs_v2_nonstandard`, `squashfs_v3_broadcom`, `squashfs_v3_nonstandard`, gzip v3 bodies, v4 Broadcom. This note adds the round-50 measurement to the LE-AVM clause of the round-49 note and supersedes nothing else.
```

**Everywhere else in the file the LE-AVM clause appears** (verified by `grep -n "LE AVM" corpus/README.md`):
L97 (round-41 coverage row, history), L106 (above), L271, L272, L279, L280, L300. No other line
mentions `hsqs` as still-Frontier.

---

## 2. The replacements

### 2a. New dated bullet — append as the **last** bullet of the `## Frontier` section

**Insertion point:** immediately after L280 (the round-49 bullet), before the blank line and
`## Known gaps` (L282). This is the section's current statement of what is still frontier.

**Paste-ready (one line):**

```
- sasquatch — 2026-10-30 round 51 (Round-51 frontier note): LE AVM members (`hsqs`) moved Frontier → Core (`2026-10-30-r51-avm-le-squashfs-core`; REA 6.5.0 `extract-firmware --max-depth 1` publishes every regular file of the independent `unsquashfs` 4.7.5 oracle on all four chain-pinned vendor carriers — FRITZ!Box 7581/7582 07.18 and 6490/6430 Cable 07.57/07.30 — and R51-C1 re-froze the gap accounting from the per-carrier-class derivation, the device-accounting law: an unprivileged extraction creates no device nodes, fifos or sockets and emits no gap record for them, so a non-regular oracle entry carries no disposition at all; the carrier bytes are fetched and never committed, AVM licence). This supersedes the LE-AVM clause of the round-49 line above and the LE-AVM clause of the round-50 frontier note below (2 of 4 under the round-50 detail whitelist `removed.silent.char-device: ["247:0"]`). Scope: four pinned carriers, one vendor, xz bodies, depth 1. Still frontier: the LE AVM rootfs of ~13k files under REA's 120 s limit (FRITZ!Box 7530/7590), AVM kernels, nested sub-images below depth 1, `squashfs_v2_nonstandard`, `squashfs_v3_broadcom`/`_nonstandard` (and the DD-WRT no-pad/4k-pad v3 images), gzip v3 bodies, v4 Broadcom, v2.1 images.
```

### 2b. New dated note — append after L300 (end of file)

**Insertion point:** as the last line of `corpus/README.md`, after the round-50 frontier note. Same
shape and same role as the round-50 note (the lane's trailing dated note).

**Paste-ready (one line):**

```
Round-51 frontier note, 2026-10-30: LE AVM members (`hsqs`) moved Frontier → Core (`2026-10-30-r51-avm-le-squashfs-core`; REA published every oracle regular file on all four chain-pinned vendor carriers, and R51-C1 re-froze the gap accounting from the per-carrier-class derivation — the device-accounting law: an unprivileged extraction creates no device nodes, fifos or sockets and emits no gap record for them, so a non-regular oracle entry carries no disposition at all — so the counter matched 4 of 4 under the law-derived rule). This note supersedes the LE-AVM clause of the round-50 frontier note above (2 of 4 under the round-50 detail whitelist, which generalised `247:0` from the Cable-carrier class) and the LE-AVM clause of the round-40/41/44/49 notes' Still-Frontier lists, and nothing else. Still Frontier: LE AVM rootfs of ~13k files under REA's 120 s limit (FRITZ!Box 7530/7590), AVM kernels, nested sub-images below depth 1, `squashfs_v2_nonstandard`, `squashfs_v3_broadcom`, `squashfs_v3_nonstandard`, gzip v3 bodies, v4 Broadcom.
```

### 2c. Optional in-place edits to the historical lines — **not recommended** (see §3)

If the L1 wants the stale clause visibly removed from the historical lines instead of only
superseded, the exact edits are (old string → replacement), each preserving the line's history and
adding a forward pointer:

| line | old string (unique) | replacement |
|---|---|---|
| L280 | `v4 Broadcom, v2.1 images, LE AVM members (`hsqs`), AVM kernels and nested sub-images below depth 1.` | `v4 Broadcom, v2.1 images, AVM kernels and nested sub-images below depth 1 (LE AVM members (`hsqs`) left this list on 2026-10-30 — see the Round-51 frontier note).` |
| L300 | `Still Frontier: LE AVM members (`hsqs`), LE AVM rootfs of ~13k files under REA's 120 s limit,` | `Still Frontier (as of 2026-10-29; LE AVM members (`hsqs`) left this list on 2026-10-30 — see the Round-51 frontier note below): LE AVM rootfs of ~13k files under REA's 120 s limit,` |
| L272 | `Still frontier: LE AVM members (`hsqs`), AVM kernel images, nested sub-images below depth 1, other vendor-mangled images.` | `Still frontier (as of 2026-10-26; LE AVM members (`hsqs`) left this list on 2026-10-30 — see the Round-51 frontier note): AVM kernel images, nested sub-images below depth 1, other vendor-mangled images.` |
| L279 | `gzip v3, v4 Broadcom, LE AVM members, AVM kernels and nested sub-images below depth 1.` | `gzip v3, v4 Broadcom, AVM kernels and nested sub-images below depth 1 (LE AVM members left this list on 2026-10-30 — see the Round-51 frontier note).` |
| L271 | `Still frontier: AVM-BE promotion, LE AVM members, nested `filesystem_core` images below depth 1, other vendor-mangled images.` | `Still frontier (as of 2026-10-26; LE AVM members left this list on 2026-10-30 — see the Round-51 frontier note): AVM-BE promotion, nested `filesystem_core` images below depth 1, other vendor-mangled images.` |
| L97 | `; LE AVM members and AVM kernels stay Frontier |` | `; LE AVM members and AVM kernels stay Frontier (the LE-AVM clause was superseded on 2026-10-30 — see the Round-51 frontier note) |` |
| L106 | `; LE AVM members (`hsqs`) stay Frontier, and the entry records the measurement (S243, S244, S245, S249) |` | `; LE AVM members (`hsqs`) stayed Frontier at this round (superseded on 2026-10-30 — see the Round-51 frontier note), and the entry records the measurement (S243, S244, S245, S249) |` |

**Recommendation: skip 2c.** The lane's precedent is append-only for dated frontier notes: the
round-49 bullet still says "Still frontier: … v1/v2 …" for a class round 49 promoted to Core, and
the round-50 `PROVINCE.md` note says outright that "the LE-AVM clause of the round-40/41/42/44/49
notes' Still-Frontier lists is unchanged by this round" (`PROVINCE.md:448`). Rewriting those
clauses would make history say something that was not true on its date; superseding them with a
dated note is the established mechanism, and §2a/§2b do exactly that. The two drafts are supplied
so the L1 can apply them either way.

---

## 3. Conditionality (must not be dropped)

Both new lines assert a promotion. Land them **only if** the round-51 counter exits **0** with
`carriers_matched == 4`, `gaps_ok` true on every carrier and every binding true
(`python3 -I -B tools/round-51/c1-counter.py --root <LANE> --rev <REV> --freeze <FREEZE>
--receipts corpus/evidence/round-51/c1 --json-out <OUT>`).

If C1 misses: **do not** apply §2a/§2b (or §2c); LE AVM members (`hsqs`) stay in the frontier
lists and the round-50 note stands unchanged. The `## Coverage map` row then takes the
*measured, not promoted* fallback text in `coverage-map-row.md` §2.

The `PROVINCE.md` twin of this edit (the `## Round-51 additions to Core` section and its frontier
note, `core_heading` = `## Round-51 additions to Core`, `frontier_mark` = `Round-51 frontier note`)
belongs to another seat; this draft covers the README side only.

---

## 4. What I checked (offline, no REA, no lane writes)

Full log: `receipts/readme-patch-check.log`; the patched copy and its unified diff:
`receipts/README.patched.md`, `receipts/readme-r51.patch`.

* the new coverage row has exactly 3 cells under the frozen `cells()`
  (`tools/round-50/c1-counter.py:585-586`), no `|` inside any cell;
* `map_token('2026-10-30-r51-avm-le-squashfs-core')` matches the row inside the `## Coverage map`
  section, so the B1 mapping atom (`tools/round-50/c2-record.py:490-517`) maps the new entry and
  every one of the 140 existing knowledge files stays mapped;
* `unique_section` for `## Coverage map`, `## Knowledge`, `## Frontier` → one section each, before
  and after the patch;
* the new dated bullet is the last bullet of the `## Frontier` section and its still-frontier list
  contains **no** `LE AVM members (`hsqs`)` clause, while every historical line keeps its original
  wording (residue reported, not edited);
* one line in the patched README carries `Round-51 frontier note` + the entry stem + an `LE AVM`
  token (the frontier-note binding shape, checked with the stem removed from the searched text);
* the patch touches exactly three insertion points in `corpus/README.md` and nothing else.

Not run: the round-51 counter itself (it does not exist yet; its scoring needs the freeze and the
data run — the L1's job), any REA run (forbidden this wave), and the round-51 data run.
