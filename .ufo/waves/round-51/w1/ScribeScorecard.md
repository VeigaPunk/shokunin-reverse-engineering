# ScribeScorecard — round 51 wave 1 (SCORECARD section draft)

**Verdict: draft delivered, with two measured findings the L1 must carry into the freeze.**
The `## Round 51 (2026-10-30)` section skeleton is at
`.ufo/waves/round-51/w1/ScribeScorecard/section.md`. Every BEFORE cell is filled from
committed bytes; every AFTER / verdict / measured-at cell that depends on a receipt the
L1 will produce is marked `[FILL:L1]`.

## Artifacts (all under my seat directory, nothing else in the lane tree)

| path | what it is |
|---|---|
| `.ufo/waves/round-51/w1/ScribeScorecard/section.md` | the draft section (the deliverable) |
| `.ufo/waves/round-51/w1/ScribeScorecard/derive-before.py` | read-only script that re-derives every BEFORE figure from committed bytes |
| `.ufo/waves/round-51/w1/ScribeScorecard/before.json` | its stdout (the derivation receipt) |
| `.ufo/waves/round-51/w1/ScribeScorecard/meanings-at-base.json` | the round-48 counter run at the base, as independent evidence for finding F2 |
| `.ufo/waves/round-51/w1/ScribeScorecard/probe-device.py` + `.out` | F0 probe: the device-kind rule shapes on a minimal device-only census |
| `.ufo/waves/round-51/w1/ScribeScorecard/probe-full.py` + `.out` | F0 probe: the same shapes over the **four committed envelopes** with the unmodified round-50 counter |
| `.ufo/waves/round-51/w1/ScribeScorecard/probe-mutations.py` + `.out` | F0 probe: the claim's own mutation set (M1–M4) under both shapes |
| `.ufo/waves/round-51/w1/ScribeScorecard/probe-census-join.py` + `.out` | F3 probe: the reader-census → FAILED-body join, measured |
| `.ufo/waves/round-51/w1/ScribeScorecard/probe-v2.py` + `.out` | post-fix verification: the **amended** `tools/round-51/c1-counter.py` on both rule shapes |

Nothing was written into `tools/`, `plans/`, `corpus/`, `SKILL.md`, `PROVINCE.md`,
`LOG.md`, `SCORECARD.md`, `SHONEN.md` or the fleet repo. No git mutation, no commit, no
push, no REA invocation, no download.

## Receipts (exact command, exit code, stdout sha256, UTC time)

```
command : python3 -I -B .ufo/waves/round-51/w1/ScribeScorecard/derive-before.py \
            --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
            --rev f04b51ddb8d5fedb234a5e40a2c38b016f07a4ab
exit    : 0
stdout  : sha256 9060d481b4c67a5d1ec8168c6b3f617517c7b45e456e9a38abc0bbdcc8c72162
          (copied to .ufo/waves/round-51/w1/ScribeScorecard/before.json, same sha256)
utc     : 2026-10-30T05:01:02Z
```

```
command : python3 -I -B tools/round-48/meanings.py --root . \
            --rev f04b51ddb8d5fedb234a5e40a2c38b016f07a4ab \
            --freeze f04b51ddb8d5fedb234a5e40a2c38b016f07a4ab --no-battery \
            --json-out .ufo/waves/round-51/w1/ScribeScorecard/meanings-at-base.json
exit    : 1   (not met — registry rows outside the census)
stdout  : sha256 6b940cf8f8e67cbc65adda5ea53114fb9e5853ad0a54f0d2044d5af950963e5f
          (the --json-out file; the counter prints its receipt to stdout too)
utc     : 2026-10-30 (same working session)
```

```
command : python3 -I -B tools/round-48/census2.py --root . \
            --rev f04b51ddb8d5fedb234a5e40a2c38b016f07a4ab \
            --out $S/census2-rederived.json
exit    : 0
result  : paths 42, named_but_absent []  -> the committed census2.json's `paths` set is
          byte-set-identical to a fresh derivation at the round base
utc     : 2026-10-30 (same working session)
```

F0 probes — all three import the **unmodified** `tools/round-50/c1-counter.py` and read only
committed bytes (the four round-50 envelopes, the frozen oracle/non-regular tables, the
round-50 gap rule); they write nothing.

```
command : python3 -I -B $S/probe-device.py
exit    : 0
stdout  : sha256 f1ff9460d88410abffad255f9a18849e08e4d28fbceff9de80c7c8295369119b
utc     : 2026-10-30T05:16:20Z
```

```
command : python3 -I -B $S/probe-mutations.py
exit    : 0
stdout  : sha256 788cb95aa1f870b071c6028b1a8f1052336dec9299785b7efb94cb9af86a40a3
utc     : 2026-10-30T05:16:20Z
```

```
command : python3 -I -B $S/probe-full.py
exit    : 0
stdout  : sha256 fc2c7637afdfe5aff28efbe6d5547471fda14dfd7c14163bc362f2ac15020474
utc     : 2026-10-30T05:17:20Z
```

```
command : python3 -I -B $S/probe-census-join.py
exit    : 0
stdout  : sha256 d13315581c6b134b4735871dfd00b923f4b0f06c4e4c1629b59637b4c3776d96
utc     : 2026-10-30T05:18:12Z
```

```
command : python3 -I -B $S/probe-v2.py     # post-fix verification, amended v2 counter
exit    : 0
stdout  : sha256 62ddb35c1bc1abfdf162894b6bce19180da9cf3282749bae7b6ddd6836c133e2
utc     : 2026-10-30T05:19:18Z
```

`$S = /fast/scratch/hyaku/kaidoku-r51/w1-ScribeScorecard` (`TMPDIR` exported to it for every
command). The scratch is removed after the receipts above were copied into the seat
directory. Nothing under `/tmp` was written or cited.

## BEFORE columns — what the committed bytes say

**R51-C1 (coverage).** From `.ufo/waves/round-50/l1/scores/c1-after-attempt2.json`:
`carriers_matched 2` of `target 4`, `exit_code 1`, `met_target false`,
`failing ["g7581:gaps_ok","g7581:projection_ok","g7582:gaps_ok"]`,
`bindings_false ["province_core_section","province_core_row"]`, `gaps_ok` true on `c6430`
and `c6490` and false on `g7581`/`g7582`; measured at `646d29c9…` against freeze
`435d41fd…`, counter sha256 `9820811b…`. The other committed arm,
`.ufo/waves/round-50/l1/scores/c1-before-attempt2.json`, reads `carriers_matched 0`, exit 1,
at the freeze `435d41fd…`. Both are cited in the draft's BEFORE cell with their paths.

The device-accounting derivation the re-freeze rests on is independently re-derivable from
the frozen oracle tables: the Cable class (`c6430`, `c6490`) carries **one** char-device
(`dev/led 247:0`); the FRITZ!Box class (`g7581`, `g7582`) carries **thirteen**
(`dev/led 247:0`, `dev/pts/0-7` `136:0-7`, `dev/tiatm` `230:0`, `dev/ttyp0-2` `3:0-2`).
Counted with `awk -F'\t' '$2=="char-device"' tools/round-50/oracle/<id>.nonregular.tsv`.
So the round-50 `removed.silent.char-device: ["247:0"]` is the Cable-class census
generalised to a second class — the miss has a per-class derivation, not a defect detail.

**R51-C2 (depth).** The committed before-state is the v5 route, read from
`.ufo/waves/round-50/c3/c3-after.json` (126 envelopes, `pair_mismatch_count 0`): the FAILED
no-pad ddwrt body `dmg_Z3_v3ddwrt_inode_table` carries `table_label legacy-body-failure`,
`table_action cross-read-legacy`, `features_F ["squashfs_v3_ddwrt"]`,
`features_G ["extractor-failure"]` — a cross-read prescribed on a body whose readers
refuse. The census drift is **13**: 55 registered paths inside the
`<!-- instrument-registry v2 -->` markers of `SKILL.md` at the base, 42 in
`tools/round-48/census2.json`, 13 absent (six `tools/round-49/*`, six `tools/round-50/*`,
`tools/round-50-c3/sqfs-triage-v5.py`).

The claim's own before-arm (`executability_violations 1`, `census_outside 13`, exit 1) is
**declared, not yet measured** — the executability audit is a round-51 instrument, so the
before-arm receipt `.ufo/waves/round-51/l1/scores/c2-before.json` is `[FILL:L1]`. The draft
says exactly that rather than presenting the declared number as an observed one.

## Four findings for the L1 (all measured, not inferred)

**F0 — CRITICAL: the wave-1 amendment F3 rule shape makes the law rule RED on all four
carriers, so CTL-NEW would be 0 of 4 and the kill rule would fire before the data run.**

F3 (`## Wave-1 amendment record`) sets `allowed[char-device] = allowed[block-device] =
allowed[fifo] = allowed[socket] = []` and says "`required` unchanged from round 50". Round
50's `required["char-device"]` is **`true`**. Under the frozen counter's own
`disposition_check` semantics (`tools/round-50/c1-counter.py:1458`; `need = required.get(kind,
bool(allowed.get(kind)))` at :1546; a required entry must carry exactly one disposition — an
allowed gap, a removal, or a `removed.silent` detail at :1470-1484), a device row with **no**
gap and **no** removal is `missing` → `gaps_ok false`. With `allowed[char-device] = []` there
is no admissible gap kind, and the law admits **no** device detail under `removed.silent`, so
there is no silent admission either: **every** device row is unaccounted, not just the twelve.

Measured against the four committed round-50 envelopes
(`corpus/evidence/round-50/c1/<id>/after.json`) and the frozen oracle/non-regular tables,
using the **unmodified** `tools/round-50/c1-counter.py`:

| rule shape | c6430 | c6490 | g7581 | g7582 |
|---|---|---|---|---|
| round-50 frozen | true | true | **false** | **false** (the committed miss) |
| **F3 as amended** (`required["char-device"]` = true) | **false** | **false** | **false** | **false** |
| F3 with `required["char-device"] = false` | true | true | **true** | **true** |

So the amended shape scores **0 of 4**, not the claim's 4 of 4. The claim's own mutation set
confirms the same defect from the other side: under the amended shape **M1 (the all-thirteen
whitelist) is disposition-GREEN** and **M2 (a fourteenth unlisted device) is RED under the law
rule** — the opposite of what the claim states for both. Under
`required["char-device"] = false` every mutation lands exactly as the claim declares: CTL-NEW
4 of 4, M1 red by `law_shape_ok`, M2 green under the law and red under any whitelist, M3 and
M4 red.

**The fix:** the law's own sentence is "a char-device/fifo/socket oracle entry carries **no
disposition at all**" — so the entry is not *required* to carry one. The frozen rule should set
`required["char-device"] = false` (equivalently, leave `required` unset for the device kinds:
`need = required.get(kind, bool(allowed.get(kind)))` and an empty `allowed` list already
defaults to not-required). The alternative — changing the disposition semantics so a device
kind with an empty `allowed` list needs no disposition — is a **counter** change rather than a
rule change, and is the L1's call to make explicitly before the freeze. Either way the freeze
must not carry the shape as amended.

**Also missing from the counter:** the current `ExecCounterV2` draft
(`.ufo/waves/round-51/w1/ExecCounterV2/c1-counter.py`) has **no** `law_shape_ok`, **no**
`census_rederived_ok` and **no** `depth_gap_recorded` — all three are named in the claims'
predicate. M1's red has no mechanism until `law_shape_ok` exists (and note that with
`required["char-device"] = false`, M1 is disposition-green and *must* be caught by that clause
rather than by the disposition check — the two are not interchangeable).

**Resolution (L1, pre-freeze, acknowledged and applied).** The L1 accepted this finding and
fixed it in the worktree copy of `plans/round-51-claims.md` `## Wave-1 amendment record` F3:
the "`required` unchanged from round 50" clause was a propagation error from the attack text,
and F3 now states `required['char-device'] = false` as a deliberate change from round 50's
`true`, citing these probe receipts. The amended v2 counter
(`tools/round-51/c1-counter.py`) now carries the `law_shape_ok` binding, which enforces all
three law clauses (empty `allowed` per device kind, empty `removed.silent` per device kind,
`required["char-device"] is False`). **Verified after the fix** against the four committed
round-50 envelopes with the amended v2 counter itself (receipt
`.ufo/waves/round-51/w1/ScribeScorecard/probe-v2.out`, sha256 `62ddb35c…`, exit 0):

| rule shape | c6430 | c6490 | g7581 | g7582 | `law_shape_ok` |
|---|---|---|---|---|---|
| F3 as amended (`required["char-device"]` = true) | false | false | false | false | **false** (`required[char-device] is not False`) |
| F3 fixed (`required["char-device"]` = false) | **true** | **true** | **true** | **true** | **true** |

So the fixed shape scores 4 of 4 and the `law_shape_ok` clause rejects the wrong one — the
kill-rule fire is avoided. **F0 is closed as a pre-freeze finding; it rides the freeze
commit's amendment record.** The residual items for the L1 are the two F3 counter-bindings
still to come (`census_rederived_ok`, `depth_gap_recorded`) and the frozen rule file itself
(`tools/round-51/gap-rule.json` is not yet in the tree).

### F1 — the `depth` Owned-axes head is already stale at the round base

The head reads
"25/25 queue-drain rule blocks have resolvable file/range citations at the round-48
landing". Command A at `f04b51dd…` reads **`rule_blocks 26`, `citation_resolved_rules 25`,
`depth_score 9.62`**: the 26th block (rule block 26, the v5 triage table) carries **no**
`corpus/knowledge/…` citation at all — only `SKILL.md table v4 row N` and `S112`/`S119`/
`S120`/`S121` source rows. The round-50 attempt-2 section already concedes the 25/25 figure
is "a historical statement and is not re-run this round", but the head still presents it as
the current observable. The round-51 head must state the re-derived base pair (26 / 25) and
the landing pair, and **rule block 27 (v6) should carry a resolvable `corpus/knowledge/…`
citation** — otherwise the landing reads 27 blocks / 25 resolved (`depth_score 9.26`), a
silent regression the head must not hide.

### F2 — the registry-census drift cannot reach 0 under the round-48 census rule

The round-48 rule (`tools/round-48/census2.py`) derives the census from the paths **named in
the claims files**. Widening it to `plans/round-4[1-9]` / `round-50` / `round-51` still leaves
**three registered paths unnameable**: `tools/round-49/c1-controls.py`,
`tools/round-49/c1-oracle.py` and `tools/round-49/c1-run.py` are named in **no** claims file
(they exist only in `.ufo/waves/round-49/draft/` and in the round-49 registry rows). A
claims-file-scoped re-derivation therefore lands at `census_outside 3`, not the claimed 0.
The target is reachable only if the round-51 census rule is **registry-derived** (enumerate
the rows inside the `<!-- instrument-registry v2 -->` markers and make the census the
registered set), or if the three round-49 paths are named in a claims file by the freeze
commit. Independent confirmation the drift is real: the round-48 counter exits **1** at the
base with `registry_rows 55`, `census_paths 42`, `registry_extra` = exactly those 13 paths
(`failing ["registry rows outside the census: …"]`).

### F3 — the C2 executability audit has no committed, joinable reader census

The claims require the v6 audit to "check every FAILED-body envelope's prescribed action
against **the family's reader census**" and to report `executability_violations 1` at the
base. The only reader census in the lane is
`.ufo/waves/round-50/w3/ExecTriageV5/receipts/reader-census.txt` (committed), and it has
**two** properties that make the declared before-state unreachable as specified:

1. **It is FIXTURE-level, not envelope-level.** Its rows are keyed
   `family | fixture | sha256[:12] | unsquashfs | 7z | verdict` over the 31 **round-42
   fixture** files. The nine FAILED-body envelopes in the corpus are **derived** bodies whose
   own subject digests appear in **no** census row: for `dmg_Z3_v3ddwrt_inode_table` the
   envelope's subject digest is `839c17a83b70…` (a recipe-derived body — "zero bytes
   144..203" of the BE nopad fixture), while the census row for that parent fixture
   (`squashfs_v3_ddwrt` / `squashfs_v3.be.nopad.bin`) is keyed `daa8e72d355d…`. The join
   runs through the round-42 manifest's `input.parent` name, which is ambiguous without the
   family: the parent name `squashfs_v3.be.nopad.bin` occurs under **four** families with
   **four different verdicts** (readable-by-both / PARTIAL / NO-READER / NO-READER). Only
   `dmg_Z3_v3ddwrt_inode_table` and `dmg_F1_v3_fixture_fragment` join at all; the other seven
   FAILED bodies have parents (`wrt54gs-v3.squashfs`, `squashfs_v1.0_le.bin`,
   `squashfs_v2.0_le.bin`) that are in **no** census row — the census covers only the four
   v3 families.
2. **The family-level verdict cannot separate the ddwrt case.** The census's family roll-up
   is `squashfs_v3_ddwrt: 6 no-reader, 1 readable-by-both` — i.e. **not** "all refuse". So a
   family-scoped rule ("the family's readers ALL refuse", as the claim words it) does **not**
   select `dmg_Z3_v3ddwrt_inode_table`; the discriminating fact is per-body (its parent
   fixture is one of the six no-reader ones), and the scored features expose no body variant
   (v5's own disclosure: "the handler name cannot carry that distinction — the scored
   features do not expose a body variant"). The round-50 what-if receipt already recorded
   this: under a fixture-correct rule **8** labels move, not 1.

**Consequence for the freeze:** the v6 audit needs a committed, machine-readable,
per-body reader census (or an explicit, frozen binding rule from envelope → parent fixture
→ census row, keyed by family) as a **frozen tool input**. The claims' registry clause
allows exactly one v6 instrument row and one census re-derive row, and no other code files
under `tools/round-51/` — so the census input must either be a named artifact inside the
v6 instrument or be frozen outside `tools/` with its path pinned. Without it the audit's
`executability_violations 1` at the base is a **declared** number with no re-derivable
mechanism, and the after-state `0` could be reached by making the audit vacuous. Note also
that the v5 receipt's own reader verdict is *raw-fixture* based while the round-42 oracle
runs show the ddwrt fixtures readable after **magic normalisation** — the census and the
oracle are measuring different byte forms, so the audit's rule must state which one it uses.

### Out-of-scope observation — a fleet-root stray (M50-9 class)

`git -C /home/vgpnk/Projects/shokunin status --porcelain` shows `?? kaidoku-r51/`, i.e.
`/home/vgpnk/Projects/shokunin/kaidoku-r51/w1-MutGapRule/amended-law-battery.py` — a
sibling seat's script (header: "Seat: MutGapRule (kaidoku round 51, wave 1)") written at a
relative path into the **fleet repo root** instead of its own seat directory. It is not mine
(my scratch was `/fast/scratch/hyaku/kaidoku-r51/w1-ScribeScorecard`; everything I wrote is
under `.ufo/waves/round-51/w1/ScribeScorecard/`). I did not touch it — deleting another
seat's artifact is not this seat's to do, and I run no mutating git in the fleet repo.
Reported to the L1: routed defect 5's `tools/round-51/misroot-sweep.sh` exists to classify
exactly this kind of stray by content, and the owner seat should re-emit the file under its
own seat directory.

Also worth the L1's attention, minor: the claims file declares its base as
`1aa273694f…` while the dispatch base is `f04b51ddb8d…`. The two differ only by
`plans/round-51-claims.md` and `.ufo/waves/round-51/l1/sources-census-start.txt` (`SKILL.md`
and `tools/` are byte-identical), so the C2 before-arm is byte-equivalent at either — but
the freeze should state one base and use it in both counting commands. **Update:** the
worktree copy of `plans/round-51-claims.md` has since been amended by the L1 (wave-1
amendment record F1–F11 present, F11 naming `f04b51dd…` as the C2 before-arm base), so the
base point is resolved; the draft reflects it. Finding 2 below is stated against the
amended text — it now says the re-derive "enumerates the registered instrument paths from
the registry markers at REV", which is the reachable wording, but the **port must not import
`census2.py`'s claims-file-naming rule**.

## Section shape (mirrors the round-50 attempt-2 section)

`## Round 51 (2026-10-30)` → base + declared freeze `[FILL:L1]` + wave shape (w1 = 36 seats
from `.ufo/waves/round-51/w1-spec.json`: executor 8, scribe 6, reviewer 5, critic 5,
mutation-tester 3, scout 4, connector 2, sentinel 1, revenger 1, simplifier 1 — attack
9/36 = 25%; w2 falsify `[FILL:L1]`) → the claims table (claim / axis+surface / before /
after / counting command / measured at) → the two claims' pre-freeze control lists with the
kill rules → the freeze-drift-gating paragraph → the four findings (F0 critical rule shape,
F1 stale depth head, F2 census drift, F3 reader-census join) → Owned scores with the
coverage head **140/140 → 141/141** and the depth head correction → learning trends
`[FILL:L1]` → Limits `[FILL:L1]` → `planned (round 52)` `[FILL:L1]` / `retired: none` →
the LOG / lesson / SOURCES / README / PROVINCE pointers.

Coverage head: measured at the base — **140** knowledge `.md` files at `f04b51dd…`, all 140
mapped, `missing []`, `dangling []`. The round-51 entry
`corpus/knowledge/2026-10-30-r51-avm-le-squashfs-core.md` is the 141st, so the head moves
**140/140 → 141/141** when it lands and is mapped.

LOG pointer: `LOG.md` gets a `## 2026-10-30 — round 51 (KaidokuR51): …` entry (freeze
revision, both counting commands and receipts, the coverage-head move, the
`PROVINCE.md` `## Round-51 additions to Core` landing with LE `hsqs` leaving the Frontier
list, the routed-defect repairs — the `646d29c9` correction entry, the `SHONEN.md`
regeneration, the two freeze-drift gates, the `fetch-vendor.py` network-guard selftests, the
`misroot-sweep.sh` sweep helper, the carried L0 cookie note — and the wave-2 falsify
dispatch). Lessons pointer: `corpus/lessons/round-51.md` `## Mistakes` rows (class ·
evidence · captured-by · fix), a fix counting only once shown able to fail. Exact wording
of both is `[FILL:L1]`; the draft names the surfaces and the required content, not the
sentences.

## Limits of this draft

- No claim was scored and no instrument was run in the wave-1 sense: the draft is a
  skeleton plus a measured BEFORE column. Every AFTER cell is a placeholder by design.
- The C1 BEFORE is a **committed** round-50 measurement, not a re-measurement; the C2
  BEFORE is a committed v5 label set plus a **declared** audit count. The draft marks the
  difference.
- The depth/depth-head figures come from command A re-run at the base; the landing pair
  must be re-derived at the landing REV (the draft says so).
- **The F0 probe measures the rule shape, not the v2 counter.** It imports the **unmodified**
  `tools/round-50/c1-counter.py` and evaluates candidate rule shapes with it, because the
  v2 counter does not exist yet and its `disposition_check` is byte-identical to the v1's
  (`diff` of the two functions over the v2 draft: no change in the `need = required.get(...)`
  line or the `missing` branch). If the L1 changes the disposition semantics in the v2
  counter instead of the rule, F0's conclusion must be re-derived against that counter —
  the finding is "the amended *rule* shape is not green under the frozen *disposition
  semantics*", which is a statement about the pair.
- **F3 is a reachability finding, not a claim that the audit is impossible.** A per-body
  reader census can be landed in the freeze; what cannot happen is the freeze landing
  without one, because then `executability_violations 1` (the declared before-state) and
  `0` (the after-state) are both unre-derivable and the after-state is reachable by making
  the audit vacuous.
- The `meanings.py` run at the base and the `census2.py` re-derivation are read-only
  invocations of the lane's own frozen instruments; no REA, no network, no vendor bytes.
- Tooling: no install, no upgrade, no pacman transaction. Nothing was needed beyond the
  lane's own `python3` and `git`.

**Paths:** draft `.ufo/waves/round-51/w1/ScribeScorecard/section.md`; receipts
`.ufo/waves/round-51/w1/ScribeScorecard/before.json`,
`.ufo/waves/round-51/w1/ScribeScorecard/meanings-at-base.json`,
`.ufo/waves/round-51/w1/ScribeScorecard/probe-{device,full,mutations,census-join}.out`;
scripts `.ufo/waves/round-51/w1/ScribeScorecard/{derive-before,probe-device,probe-full,probe-mutations,probe-census-join}.py`.
