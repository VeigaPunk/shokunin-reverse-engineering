# R52-C1 — `corpus/README.md` frontier-note edit draft (paste-ready)

Seat `ScribeReadme`, kaidoku round 52 wave 1 (build). **Draft only — nothing in the lane tree was
written outside this seat directory.**

Base bytes: `corpus/README.md` at lane HEAD `1842addcef3458515859b928b92d9bbd0a46c5d5` (blob
`b8a266ea52ed63dad8089294da964c6da107f87a`; worktree sha256
`aad0c5907483f38fc0fcf82cb66f63d0b15a6554c3ad2d0d6d85c6a60b5da5db`). The blob is byte-identical at
the round-start base `c525de54…` and at the claims draft `ab0eafe…`.

**What has to move:** LE AVM members (`hsqs`) leaves the Frontier list. Round 52 re-freezes the
gap-accounting rule from the per-carrier-class derivation (the device-accounting law) and, **only if
the round-52 counter exits 0 with `carriers_matched == 4`**, the four pinned LE AVM members are
promoted to Core.

> ⚠ **Conditional.** Every replacement below asserts a promotion. Apply them **only if**
> `python3 -I -B tools/round-52/c1-counter.py --root <LANE> --rev <REV> --freeze <FREEZE>
> --receipts corpus/evidence/round-52/c1 --json-out <OUT>` exits **0** with `carriers_matched == 4`,
> `gaps_ok` true on every carrier and every binding true. On a miss, apply **none** of §2/§3; LE AVM
> members stay Frontier and the round-50 note stands unchanged.

---

## 0. The two LE-AVM frontier items — do not confuse them

The README carries **two different** frontier items that both start with "LE AVM". Only one of them
leaves the list in round 52:

| item | what it is | round-52 fate |
|---|---|---|
| **LE AVM members (`hsqs`)** | the four chain-pinned vendor members (FRITZ!Box 7581/7582 07.18, 6490/6430 Cable 07.57/07.30) measured on every round since 50 | **leaves the list** (promoted, conditional on `carriers_matched == 4`) |
| **LE AVM rootfs of ~13k files under REA's 120 s limit** | the *unmeasured* FRITZ!Box 7530/7590 rootfs — an observed load-dependent timeout, never a claim | **stays Frontier** (unchanged; nothing in round 52 measures it) |

Every replacement below removes only the first and keeps the second. This is the one place where a
careless "remove the LE-AVM clause" edit would silently drop a still-frontier item.

---

## 1. Old lines (verbatim, with line numbers at the base revision)

**L274** — round-40 dated bullet (history):

```
- sasquatch-v4be — 2026-10-26 round 40: genuine AVM-layout BE v4 **measured, not promoted** (`2026-10-26-r40-avm-be-squashfs-core`): every oracle file on four carriers, but R40-C1 stopped at 3/4 on a counter suffix false negative. Still frontier: AVM-BE promotion, LE AVM members, nested `filesystem_core` images below depth 1, other vendor-mangled images.
```

**L275** — round-41 dated bullet (history):

```
- sasquatch-v4be — 2026-10-26 round 41: the genuine AVM layout is **Core** (`2026-10-26-r41-avm-be-squashfs-core`), superseding the round-40 `measured, not promoted` line above; that stop was a counter suffix false negative (R40-CL1), not an image property. Still frontier: LE AVM members (`hsqs`), AVM kernel images, nested sub-images below depth 1, other vendor-mangled images.
```

**L282** — round-44 dated bullet (history):

```
- sasquatch — 2026-10-28 round 44: SquashFS v1/v2 was measured on four standard fixtures but **remains Frontier** (R44-C1 honest stop: frozen-claim/counter output-directory provenance mismatch; `2026-10-28-r44-squashfs-v1v2-core`). Still frontier: `squashfs_v2_nonstandard`, `squashfs_v3_broadcom`/`squashfs_v3_nonstandard`, gzip v3, v4 Broadcom, LE AVM members, AVM kernels and nested sub-images below depth 1.
```

**L283** — round-49 dated bullet (the **last** bullet of the `## Frontier` section; history — and
the section's current statement):

```
- sasquatch — 2026-10-28 round 49: SquashFS v1/v2 (`squashfs_v1`, `squashfs_v2`, four standard fixtures) is **Core** (`2026-10-28-r49-squashfs-v1v2-core`), superseding the round-44 line above. Scope: the four standard v1.0/v2.0 fixtures only. Supersedes the round-42 and round-44 lines above for v1/v2. Still frontier: `squashfs_v2_nonstandard`, `squashfs_v3_broadcom`/`squashfs_v3_nonstandard` (and the DD-WRT no-pad/4k-pad v3 images), gzip v3, v4 Broadcom, v2.1 images, LE AVM members (`hsqs`), AVM kernels and nested sub-images below depth 1.
```

**L303** — the `Round-50 frontier note` paragraph (the file's last line; history; **outside** the
`## Frontier` section — it sits after `## Known gaps`):

```
Round-50 frontier note, 2026-10-29: LE AVM members (`hsqs`) were measured on four chain-pinned vendor carriers (`2026-10-28-r50-avm-le-squashfs-core`; REA published every oracle regular file on all four) and **stay Frontier** — R50-C1 measured 2 of 4 under the frozen gap-accounting rule (twelve `char-device` entries per FRITZ!Box carrier with no disposition; the rule was generalised from the Cable-carrier class). Still Frontier: LE AVM members (`hsqs`), LE AVM rootfs of ~13k files under REA's 120 s limit, AVM kernels, nested sub-images below depth 1, `squashfs_v2_nonstandard`, `squashfs_v3_broadcom`, `squashfs_v3_nonstandard`, gzip v3 bodies, v4 Broadcom. This note adds the round-50 measurement to the LE-AVM clause of the round-49 note and supersedes nothing else.
```

**L97 / L106** — the round-41 and round-50 **coverage-map** rows (history; they are *not* in the
`## Frontier` section, so a `## Frontier`-scoped check never sees them — see §4):

```
| Genuine AVM-layout big-endian SquashFS v4 through REA (round 41) | `2026-10-26-r41-avm-be-squashfs-core` | **Core** — `extract-firmware --max-depth 1` publishes every oracle regular file at its exact path relative to the chunk extract root (no suffix matching) on four frozen carriers (V3 FRITZ!Box 5490 07.31, V4 FRITZ!Box 5491 07.31, L3/L4 lane-built with both-direction path collisions); gaps one `unpublished-entry` per retained symlink plus one `depth-limited`; repairs round-40's suffix false negative (R40-CL1) and binds `member_sha256` in the vendor fetch chain (R40-CL6) scored by `tools/round-41/c1-counter.py` after the landing commit; LE AVM members and AVM kernels stay Frontier |
| SquashFS LE AVM members (round 50) | `2026-10-28-r50-avm-le-squashfs-core` | measured, not promoted — REA published every oracle regular file on all four pinned vendor carriers, and the frozen gap-accounting rule matched only the two Cable carriers (2/4, `gaps_ok` false on g7581/g7582: twelve char-device entries with no disposition); LE AVM members (`hsqs`) stay Frontier, and the entry records the measurement (S243, S244, S245, S249) |
```

**Everywhere else in the file the LE-AVM clause appears** (measured:
`grep -n "LE AVM\|hsqs" corpus/README.md`): L97, L106, L229, L274, L275, L282, L283, L303. L229 is
the round-50 `## Knowledge` index row (history). No other line names `hsqs` as still-Frontier.

---

## 2. The replacements — 2a new dated bullet (recommended)

**Insertion point:** immediately after L283 (the round-49 bullet), before the blank line and
`## Known gaps` (L285). This is the section's current statement of what is still frontier.

**Paste-ready (one line):**

```
- sasquatch — 2026-10-30 round 52 (Round-52 frontier note): LE AVM members (`hsqs`) moved Frontier → Core (`2026-10-30-r52-avm-le-squashfs-core`; REA 6.5.0 `extract-firmware --max-depth 1` publishes every regular file of the independent `unsquashfs` 4.7.5 oracle at its exact path on all four chain-pinned vendor carriers — FRITZ!Box 7581/7582 07.18 and 6490/6430 Cable 07.57/07.30 — and R52-C1 re-froze the gap accounting from the per-carrier-class derivation, the device-accounting law: an unprivileged extraction creates no device nodes, fifos or sockets and emits no gap record for them, so a non-regular oracle entry carries no disposition at all). This supersedes the LE-AVM clause of the round-40/41/44/49 lines above and of the round-50 frontier note below, and nothing else. Still frontier: LE AVM rootfs of ~13k files under REA's 120 s limit (observed, not claimed), AVM kernels, nested sub-images below depth 1, `squashfs_v2_nonstandard`, `squashfs_v3_broadcom`, `squashfs_v3_nonstandard`, gzip v3 bodies, v4 Broadcom.
```

**Binding shape.** The line carries the three strings a frontier-note binding looks for — the mark
`Round-52 frontier note` (the `frontier_mark` constant named in `plans/round-52-claims.md`), the
entry stem `2026-10-30-r52-avm-le-squashfs-core`, and a literal `LE AVM` token (searched with the
stem removed, so the stem's own `avm-le` cannot satisfy it — the round-50/41 counters search
`PROVINCE.md` this way: `tools/round-50/c1-counter.py:2454-2456`,
`tools/round-41/c1-counter.py:1695`). It contains no `|` inside its text.

**Still-frontier items kept:** LE AVM rootfs of ~13k files under REA's 120 s limit, AVM kernels,
nested sub-images below depth 1, `squashfs_v2_nonstandard`, `squashfs_v3_broadcom`,
`squashfs_v3_nonstandard`, gzip v3 bodies, v4 Broadcom. **Dropped:** the `LE AVM members (`hsqs`)`
clause only.

## 3. The replacements — 3a new dated trailing note (house precedent, optional)

The round-50 landing put its dated note as a **trailing paragraph at end of file** (L303), not as a
`## Frontier` bullet. Same shape, same role:

**Insertion point:** as the last line of `corpus/README.md`, after the round-50 frontier note.

**Paste-ready (one line):**

```
Round-52 frontier note, 2026-10-30: LE AVM members (`hsqs`) moved Frontier → Core (`2026-10-30-r52-avm-le-squashfs-core`; REA published every oracle regular file on all four chain-pinned vendor carriers, and R52-C1 re-froze the gap accounting from the per-carrier-class derivation — the device-accounting law: an unprivileged extraction creates no device nodes, fifos or sockets and emits no gap record for them, so a non-regular oracle entry carries no disposition at all — so the counter matched 4 of 4 under the law-derived rule). This note supersedes the LE-AVM clause of the round-50 frontier note above (2 of 4 under the round-50 detail whitelist, which generalised `247:0` from the Cable-carrier class) and of the round-40/41/44/49 `## Frontier` lines, and nothing else. Still Frontier: LE AVM rootfs of ~13k files under REA's 120 s limit (observed, not claimed), AVM kernels, nested sub-images below depth 1, `squashfs_v2_nonstandard`, `squashfs_v3_broadcom`, `squashfs_v3_nonstandard`, gzip v3 bodies, v4 Broadcom.
```

## 4. In-place edits to the historical lines — the choice that the L1 must make

§2/§3 supersede; they do not **remove** the clause from the historical lines. L274, L275, L282,
L283 and L303 therefore still read "LE AVM members (`hsqs`)" as still-Frontier, and L97/L106 (the
coverage rows) still say "LE AVM members … stay Frontier". That is true history (those lines were
true on their dates), but it is also why the **round-51 critic's finding F15** — "the v1
`frontier_note` binding cannot distinguish *promoted* from *not promoted*" — exists: a counter that
only greps for the mark cannot see whether the class really left the list.

Two self-consistent options:

| option | what lands | a counter can check |
|---|---|---|
| **A — append-only** (§2 + §3 only) | the two new dated lines; every historical line keeps its wording | "the newest dated frontier line names the promotion" — **not** "the LE-AVM clause is gone" |
| **B — supersede + in-place removal** (§2 + §3 + §4c below) | the two new dated lines **and** the LE-AVM clause removed from L274/L275/L282/L283/L303 (with a dated pointer), plus the pointer on L97/L106 | "no `## Frontier` line lists LE AVM members (`hsqs`) as still-Frontier" — a real removal check |

**Recommendation: B**, because the round-52 claims require the promotion to be *visible as a
promotion* ("LE `hsqs` leaves the Frontier list") and because the round-51 critic asked for a
binding that can distinguish promoted from not-promoted. Option B keeps the history truthful by
adding a dated pointer to every edited line instead of rewriting it. The cost is that §4c touches
dated lines — the lane has done exactly this before (`corpus/README.md:268` carries the
"[2026-10-28: the `v1/v2` item below is superseded by the round-49 line further down]" prefix on the
round-42 bullet, and the round-49 note itself supersedes the round-42/44 lines above it).

### 4c. The exact old → new string pairs for option B

Each old string is unique in the file (measured). The replacements drop **only** the LE-AVM-members
clause and keep every other still-frontier item, including the ~13k-file rootfs clause.

| line | old string (unique) | replacement |
|---|---|---|
| L274 | `Still frontier: AVM-BE promotion, LE AVM members, nested `filesystem_core` images below depth 1, other vendor-mangled images.` | `Still frontier: AVM-BE promotion, nested `filesystem_core` images below depth 1, other vendor-mangled images (LE AVM members left this list on 2026-10-30 — see the Round-52 frontier note).` |
| L275 | `Still frontier: LE AVM members (`hsqs`), AVM kernel images, nested sub-images below depth 1, other vendor-mangled images.` | `Still frontier: AVM kernel images, nested sub-images below depth 1, other vendor-mangled images (LE AVM members (`hsqs`) left this list on 2026-10-30 — see the Round-52 frontier note).` |
| L282 | `gzip v3, v4 Broadcom, LE AVM members, AVM kernels and nested sub-images below depth 1.` | `gzip v3, v4 Broadcom, AVM kernels and nested sub-images below depth 1 (LE AVM members left this list on 2026-10-30 — see the Round-52 frontier note).` |
| L283 | `gzip v3, v4 Broadcom, v2.1 images, LE AVM members (`hsqs`), AVM kernels and nested sub-images below depth 1.` | `gzip v3, v4 Broadcom, v2.1 images, AVM kernels and nested sub-images below depth 1 (LE AVM members (`hsqs`) left this list on 2026-10-30 — see the Round-52 frontier note).` |
| L303 | `Still Frontier: LE AVM members (`hsqs`), LE AVM rootfs of ~13k files under REA's 120 s limit,` | `Still Frontier (as of 2026-10-29; LE AVM members (`hsqs`) left this list on 2026-10-30 — see the Round-52 frontier note below): LE AVM rootfs of ~13k files under REA's 120 s limit,` |
| L97 | `; LE AVM members and AVM kernels stay Frontier |` | `; LE AVM members and AVM kernels stay Frontier (the LE-AVM clause was superseded on 2026-10-30 — see the Round-52 frontier note) |` |
| L106 | `; LE AVM members (`hsqs`) stay Frontier, and the entry records the measurement (S243, S244, S245, S249) |` | `; LE AVM members (`hsqs`) stayed Frontier at this round (superseded on 2026-10-30 — see the Round-52 frontier note), and the entry records the measurement (S243, S244, S245, S249) |` |

**Note on L97/L106 (coverage-map rows):** these are inside the `## Coverage map` table, not the
`## Frontier` section. A `## Frontier`-scoped counter never sees them; they are edited only so the
*file* does not contradict itself. Each edit is a parenthetical pointer — the row keeps its
"measured, not promoted" / Core wording of its own date.

**Note on the `~13k`-file clause:** it appears in L303 only, and §4c keeps it. If the L1 instead
prefers to delete the LE-AVM clause *and* the 7530/7590 rootfs clause from L303, that would drop a
still-frontier item that round 52 does not measure — do not.

---

## 5. What I checked offline (no REA, no lane write, no git mutation)

* the two new lines carry the mark `Round-52 frontier note` + the entry stem + a literal `LE AVM`
  token (checked with the stem removed, the way the frozen counters search it);
* neither new line contains a `|` inside its text (the frontier bullets are prose, not table rows);
* the new bullet lands as the **last** bullet of the `## Frontier` section, and its still-frontier
  list contains **no** `LE AVM members (`hsqs`)` clause while keeping the `~13k`-file clause;
* under option B, after the five in-place edits, **no** `## Frontier` line lists LE AVM members
  (`hsqs`) as still-Frontier, and every edited line carries a dated pointer;
* `unique_section` for `## Coverage map` / `## Knowledge` / `## Frontier` → 1 / 1 / 1 before and
  after the patch;
* the patch is insertions + 7 in-place string replacements, and touches nothing else in the file.

Full log: `receipts/check.log`; the patched copies and their unified diffs: `receipts/`.

**Not run:** the round-52 counter (it does not exist yet; its scoring needs the freeze and the data
run — the L1's job), the four-carrier data run, any REA invocation (forbidden this wave), and the
`PROVINCE.md` twin of this edit (another seat's surface: `## Round-52 additions to Core` +
`Round-52 frontier note`).
