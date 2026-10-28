# R44Shonen — report `## SHONEN` skeleton (round 44, wave 1, pre-freeze)

Seat `R44Shonen` (scribe). Authored at lane HEAD `f5fb8d590f0dd6afc0847e1a63e8a3953bef8717`;
**the lane advanced during this seat** to `f18bdfb9fc8bb451ebab826c058049254d508483` by two L1
commits (`3b0fcaa9` frozen `carriers.json` + unblob `__output__` oracle trees; `f18bdfb9` v2.1 LE/BE
carriers, 6 total). Observations below name the HEAD they were taken at; the 4-carrier rows are the
`f5fb8d59` state, the 6-carrier rows the `f18bdfb9` state. Assignment base is
`c29360e3ba5381a5ab69e372d0d9577970f85018`, lane `main`.
**Wave 1 is pre-freeze: nothing below is a claim score.** Every `⟦slot: …⟧` is filled by L1 after
the freeze + after the L1's C1 data run; a slot with no post-freeze receipt degrades to `[ ]`, never
to prose. Observations recorded here each name their command; the full receipts (seat, command,
exit code, stdout sha256, wall time) are in
`.ufo/waves/round-44/w1/R44Shonen/obs-receipts.md` (`.json` beside it).

Axes named: **coverage** (C1), **calibration** (C2), **depth** (neither claim touches it; watch for harm).
Do-nothing control of the whole section: if the freeze lands and no counter runs, every slot stays
`⟦unfilled⟧` and the section is four `[ ]` lines — the skeleton cannot pass itself.

---

## 1. Phrasing discipline this section obeys

Derived from `corpus/lessons/round-43.md` (M43-1, M43-2), the report contract
(`.ufo/prompts/kaidoku-round-44.md` §4) and `SHONEN.md`'s own checklist form:

1. **One line per `SHONEN.md` box** (4 boxes). `[x]` **only** with a named non-author verifier;
   `[~]` only with a resolvable evidence pointer; `[ ]` if untouched. No `[x]` in this round unless
   a wave-2 seat is named in the line itself.
2. **Numbers carry their command.** A count without the command that produced it is not a claim
   (round-43 M43-2: a `3\t0` expectation against a real `4\t0` diff is the failure mode).
3. **No axis scalar is claimed to rise.** `coverage`, `depth` and `calibration` are all at their
   ceiling (10/10/10) at the base; a round moves the *observable* (Core rows, carriers matched,
   mismatches counted), not the score.
4. **Stops are reported as stops.** An honest stop is a result with a receipt; "improved",
   "shored up", "hardened" without an exit code is an unfalsifiable claim and does not appear.
5. **Exit-code semantics are part of the sentence.** `0` met/clean, `1` failed, `2`
   could-not-evaluate; a `2` never counts toward the target (QUALITY; contract §9).

---

## 2. Axis deltas at base (observed, not scored)

Evidence: `SCORECARD.md:23-25` (`## Owned axes`), `SCORECARD.md:3508` (last command-A record).

| axis | score at base | ceiling | round-44 observable that can move | counter / receipt |
|---|---|---|---|---|
| coverage | 10.0 (`9.72 → 10.0`, round 41) | 10 | `carriers_matched` 0 → `⟦slot: 0–6⟧` (frozen `carriers.json` now holds 6, see §3/F6); `PROVINCE.md` `## Round-44 additions to Core` rows 0 → `⟦slot: 0–1⟧`; `corpus/knowledge` mapped `137/137` → `⟦slot: 137…138⟧` | `tools/round-44/c1-counter.py` (absent at authoring, see §3) |
| depth | 10 (`10 → 10`) | 10 | nothing claimed by C1/C2; harm control = `citation_resolved_rules 21/21` unchanged at REV | command A (`SCORECARD.md:3508`) |
| calibration | 10 (`0 → 10`) | 10 | rubric `mismatches` at base → `⟦slot: 0…⟧` at REV; 0 at base = honest stop | `tools/round-44/c2-counter.py` (absent pre-freeze) |

Last measured command A (`SCORECARD.md:3508`, revision `8de80f1daec68260eb256eb68375e2c33af759a9`):
`knowledge_files=137`, `mapped=137`, `missing=[]`, `dangling=[]`, `coverage_score=10.0`,
`citation_resolved_rules=21/21`, `depth_score=10.0`. Observed at base: `corpus/knowledge/*.md` = **137**
files and `corpus/SOURCES.md` = **137** rows (`S138`/`S139` = 0 rows) — i.e. the round-44 frontier
step has not landed yet.

> **Falsifiable sentence for L1:** "coverage stays at ceiling 10.0 and calibration at 10; the round's
> measurable delta is `carriers_matched 0 → ⟦n⟧` and `mismatches ⟦b⟧ → ⟦m⟧`, both from receipts named
> below." Anything else (e.g. "coverage improved") is banned by rule 3.

---

## 3. What moved (pre-freeze state, observed)

| item | observed state | pointer / command |
|---|---|---|
| C1 carrier pins | `tools/round-44/carriers.json` (sha256 `cb0f417b4ca41356f41db51fc7d0a008d349c433427c4e62abbf0a9058d1822b`), 4 carriers, **4/4 `sha256` pin_match true**, ids `v1le/v1be/v2le/v2be`, handlers `squashfs_v1`/`squashfs_v2` | `obs-receipts.md` §carrier pins |
| C1 second oracle | unblob 26.6.4 `__output__` trees committed under `corpus/evidence/round-44/oracle/`: 22 files, 7 distinct sha256, 152 content bytes, 10 listings, `failures 0`; **untracked at authoring** (`git status` → `?? corpus/evidence/round-44/`) | `corpus/evidence/round-44/oracle/manifest.json` `counts` |
| C1 target text | `PROVINCE.md:410` `## Round-42 additions to Core`; `:416` frontier note ends "Still Frontier: SquashFS v1/v2, …" — the text `## Round-44 additions to Core` must supersede | `PROVINCE.md:410,416` |
| C1/C2 counters | **absent at authoring** (wave-1 HEAD, and at base): `tools/round-44/c1-counter.py`, `c2-counter.py`, `c1-run.sh`, `c2-rubric.json` do not exist; `tools/round-44/` holds only `carriers.json` (08:12) | `ls tools/round-44/` |
| C2 rubric | not enumerated yet; seats R44ScoutCalib / R44C2Shonen / R44C2Readme / R44C2Plan own the census | `.ufo/waves/round-44/w1-spec.json` |
| prior round | round 43 C1 scored `78/78`, `exit_code 0`, `met_target true`, freeze `f3f8db38`, revision `77d196c6` | `.ufo/waves/round-43/l1/scores/c1-at-77d196c6.json` |

**First claim-data commit:** `⟦slot: commit that first adds the round-44 C1 after-receipt⟧`.
**Pins at freeze:** `⟦slot: carriers.json sha256 at FREEZE⟧`, `⟦slot: c1-counter.py sha256⟧`,
`⟦slot: c2-counter.py sha256⟧`, `⟦slot: c2-rubric.json sha256⟧`.

---

## 4. What the frozen counters measure (targets, not results)

Paste-ready template — L1 replaces the right-hand column only.

| claim | counting command | target | result at REV |
|---|---|---|---|
| R44-C1 | `python3 -I -B tools/round-44/c1-counter.py --root <LANE> --rev <REV> --freeze <FREEZE> --pkg65 <rea-agents 6.5.0 root> --work <SCRATCH> --json-out <OUT>` | `carriers_matched == 4`, every binding true, `frozen_path_changed []`, `met_target true`, exit 0 | `⟦slot: exit / carriers_matched / bindings_false / frozen_path_changed⟧` |
| R44-C2 | `python3 -I -B tools/round-44/c2-counter.py --root <LANE> --rev <REV> --freeze <FREEZE> --work <SCRATCH> --json-out <OUT>` | `mismatches == 0` over the frozen rubric, every check evaluable, `frozen_path_changed []`, exit 0 | `⟦slot: exit / mismatches / unevaluable⟧` |

Receipt fields that must be quoted for each (round-41 closure D4 + contract): `exit_code`,
`counter_sha256`, `counter_sha256_at_freeze`, sha256 of every post-freeze control receipt cited,
`stdout_sha256`, wall time. A receipt missing any of these is not evidence for this section.

**Slot, if C1 lands:** the promoted capability sentence, with the exact handler names and the
Core-row pointer —
`⟦slot: "SquashFS v1 (`squashfs_v1`) and v2 (`squashfs_v2`) Frontier → Core through REA 6.5.0
extract-firmware on 4 frozen MIT fixtures (le/be each), independent oracle /usr/bin/unsquashfs 4.7.5;
PROVINCE.md:NNN; knowledge entry …; receipts corpus/evidence/round-44/c1/…"⟧`.

---

## 5. What stopped (or must stop) — the kill rules, stated before data

1. **C1 counterfactual controls.** If any of CTL-C1-0 (do-nothing), CTL-C1-1 (round-42 v3 receipts
   copied to round-44 paths), CTL-C1-2 (fabricated oracle-only envelope), CTL-C1-3 (sasquatch
   stripped from the child PATH) reaches `carriers_matched == 4` with every binding true, C1 stops
   before data. Score all four at the freeze: `⟦slot: CTL-C1-0..3 exits and headline fields⟧`.
2. **C2 do-nothing control.** If the frozen rubric finds **zero** mismatches at base, C2 stops
   honestly — the do-nothing control reached the target, which proves the predicate wrong. Report
   the zero, do not loosen: `⟦slot: mismatches at base⟧`.
3. **C2 seeded-mismatch / malformed-rubric controls.** CTL-C2-1 must exit non-zero on a seeded
   mismatch; CTL-C2-2 must exit 2 on a malformed rubric; CTL-C2-3 (rubric edited mid-round) must
   re-red via `frozen_path_changed`. `⟦slot: exits⟧`.
4. **Retained Frontier.** `squashfs_v2_nonstandard` (`v2ns-*`) stays Frontier: no independent reader
   (measured: `/usr/bin/unsquashfs -s` exits 1 on both `v2ns-le`/`v2ns-be` fixtures — "Can't find a
   valid SQUASHFS superblock"; `7z` 26.04 (x64) exits 2 — "Cannot open the file as archive";
   backhand has no v2ns profile), and a same-tool oracle is not an oracle. Receipts in
   `obs-receipts.md` §v2ns refusal. Also still Frontier: `squashfs_v3_broadcom`,
   `squashfs_v3_nonstandard`, `squashfs_v4_broadcom`, gzip v3, LE AVM (`hsqs`), AVM kernels, nested
   sub-images below depth 1.
5. **First-freeze drift.** No commit in `FREEZE..REV` may touch a frozen path; a later restore does
   not un-block (exit 2 `frozen_path_changed`, never `met_target`). `⟦slot: frozen_path_changed⟧`.

---

## 6. The mined mistake (class `stale-premise`) — declared, evidence unresolved at authoring

Draft text (`plans/round-44-claims.md:198-202`): the pre-freeze probe fetched
`squashfs_v2.0_be.expected` by guessing the fixture API shape (**HTTP 404**) before reading the
directory listing; captured-by = the frozen-URL convention (a URL is pinned only after a successful
open, never guessed); fix = verify URL existence via the directory-listing API first, with a red
(404) and green (200 listing) receipt shown able to fail.

**Status at authoring — the red side does not resolve.** `.ufo/waves/round-44/l1/` is empty and the
string `probe-fixture-404` appears only inside the claims file itself (fleet-wide grep). The green
side does exist: 10 listing receipts under `.ufo/waves/round-44/w1/R44SrcOracle/listings/` (4 of
them `__output__` directory listings), all `http_status 200`, 0 failures. Therefore the final report
may phrase the mistake **only** as:

- Red: `⟦slot: 404 receipt path + http_status + command, captured before the listing⟧`
- Green: `POST /repos/onekey-sec/unblob/contents/.../__output__` → 200, listing receipt
  `.ufo/waves/round-44/w1/R44SrcOracle/listings/squashfs_v2__big_endian__output__.json` (2 entries,
  `http_status 200`).
- Fix, shown able to fail: the counter or pin step must reject a URL that was not opened.

If the red receipt is never captured, the report says **"declared, unbacked at freeze"** and the
mistake is mined from an observed one instead — it is not restated as fact.

A second, **observed** mistake-class candidate L1 may mine instead or additionally (F2 in §7):
`tools/round-44/carriers.json` described v1/v2 superblocks with v3/v4 offsets and carried a
`compression` field that does not exist in the v1/v2 layout — the same `stale-premise` class
(assuming a familiar struct shape). It has a red/green pair available: wrong offsets → decoded
`bytes_used` ≠ file size; correct offsets → `176/177/196/201` = file sizes.

---

## 7. Findings that must be settled before the freeze (verbatim conflicts)

These are reported, not repaired (scribe seat). The canonical judge decides.

**F1 — draft's "v2be uncompressed" is refuted by the independent reader.**
Draft (`plans/round-44-claims.md:85-86`): "`v2be` is uncompressed (measured 2026-10-28: `file`
reports \"version 2.0, uncompressed\"); that is an oracle property, not a counter assumption."
Measured: `/usr/bin/unsquashfs -s` (squashfs-tools 4.7.5) exits 0 on all four carriers and prints
"**Data is compressed**" for each — including `v2be` and `v1be` (`obs-receipts.md`). `file(1)`'s
"uncompressed" on the two **big-endian** images is a v3/v4-layout misparse: the v1/v2 superblock has
no flags/compression field at all
(`~/.local/share/uv/tools/unblob/lib/python3.13/site-packages/unblob/handlers/filesystem/squashfs.py:123-137`).
`carriers.json` says `gzip`
for all four, which agrees with `unsquashfs`. **Action for L1:** correct the draft sentence before
the freeze; a counter frozen to expect "uncompressed" for `v2be` would fail a valid carrier, and a
counter frozen to accept two contradictory answers is not a predicate.

**F2 — `carriers.json` `superblock_layout` is v3/v4, not v1/v2.**
Declared: `compression_offset 20 len 2`, `bytes_used_offset 40 len 8`. Actual v1/v2 struct
(`unblob` `C_DEFINITIONS`,
`~/.local/share/uv/tools/unblob/lib/python3.13/site-packages/unblob/handlers/filesystem/squashfs.py:123-137`):
`s_magic[4]; inodes; bytes_used; uid_start;
guid_start; inode_table_start; directory_table_start; s_major; s_minor` — i.e. `bytes_used` at **8**,
`s_major`/`s_minor` at 28/30, and **no compression field**; offset 20 is `inode_table_start`.
Measured: `bytes_used@8` = 176 / 177 / 196 / 201, exactly the `file` sizes; `inode_table_start@20` =
71 / 71 / 88 / 88; `s_major@28` = 1 / 1 / 2 / 2. **Consequence:** a counter built on the declared
layout would read `inode_table_start` as "compression" and garbage as `bytes_used`. The draft
predicate also requires the superblock to read "compression" — v1/v2 has no such field, so the
predicate must either drop it or define compression from `unsquashfs -s` / `fixtures.json`.

**F3 — the mined-mistake evidence pointer does not resolve.** See §6: claims cite
`.ufo/waves/round-44/l1/probe-fixture-404.txt`; the directory is empty and no such file exists
anywhere in the fleet.

**F4 — the oracle tree is wider than the frozen carriers.** `corpus/evidence/round-44/oracle/squashfs_v2/`
contains **two** extract dirs per endian — `squashfs_v2.0_{le,be}.bin_extract` (4 files, the frozen
carriers) **and** `squashfs_v2.1_{le,be}.bin_extract` (4 files, not carriers). The counter must bind
the exact extract-dir name for the carrier it checks; a `*squashfs_v2*` glob would pull in v2.1
files (same trap class the fixture audit flagged for the `v2ns-*` basenames).

**F5 — pre-freeze paths are untracked.** `git status --porcelain` at authoring:
`?? corpus/evidence/round-44/`, `?? tools/round-44/carriers.json`. The draft requires both committed
before the freeze. Checklist item, not a defect yet.

---

## 8. Paste-ready `## SHONEN` section (one line per `SHONEN.md` box)

> L1: copy the four bullets below into the round report's `## SHONEN` section, fill the slots, and
> check `grep -c '^## SHONEN' <report>` prints 1 (prompt §5).

- [~] **Box 1 — decision tables, error patterns, checklists, cited sources:** `SKILL.md:525`
  carries `<!-- sqfs-triage-table v4 -->`; last measured command A at `8de80f1d` returns
  `citation_resolved_rules=21/21` (`SCORECARD.md:3508`). Round 44 adds a v1/v2 Core row and an
  oracle identity, not a new triage block: `⟦slot: rule-block count at REV (expect 21)⟧`; no
  non-author verifier named unless a wave-2 seat is named here.
- [~] **Box 2 — at least one end-to-end domain task logged in `LOG.md`:** prior entry
  `LOG.md:3184` (round 43, C1 `78/78` at `77d196c6`). Round 44: `⟦slot: LOG.md line of the round-44
  entry; REA 6.5.0 extract-firmware on 4 carriers; carriers_matched/exit; receipt dir⟧`.
- [~] **Box 3 — instructions executable by an agent without oral context:** prior evidence
  `.ufo/waves/round-43/l1/scores/c1-at-77d196c6.json` (`exit_code 0`, `matched 78`, `met_target true`).
  Round 44: `⟦slot: c1-counter.py --selftest case counts + exit; c2-counter.py --selftest case
  counts + exit; CTL-C1-0..3 and CTL-C2-0..3 exits⟧`.
- [~] **Box 4 — no cross-domain bleed (`PROVINCE.md` accurate):** refusal list `PROVINCE.md:97-125`
  unchanged; round-43 frontier note `PROVINCE.md:418`; round 44 appends Core/status text only.
  `⟦slot: git diff BASE..REV -- PROVINCE.md row identities + confirmation that no Adjacent line
  moved; v2ns and the other Frontier rows still listed⟧`.

**Section-level honesty line (mandatory, fill one):**
- If both claims land: "R44-C1 `⟦4/4, exit 0⟧`; R44-C2 `⟦mismatches 0 at REV, exit 0⟧`; no axis
  scalar moved (ceiling); the capability delta is the two Core handler names."
- If C2 finds zero mismatches at base: "R44-C2 **stopped honestly** — frozen rubric scored
  `0` mismatches at base (`⟦receipt⟧`), so a do-nothing round reached the target; not loosened."
- If C1 misses: name the failed binding **and** the exit code: `⟦slot⟧`. A `2` is written as
  could-not-evaluate, never as a partial pass.

---

## 9. Fill protocol (so the section cannot drift)

1. Replace every `⟦slot: …⟧` with a value **and** its receipt path; a value with no receipt stays a
   slot and the box degrades to `[ ]`.
2. Do not upgrade a slot into a claim because the counter is expected to pass — the freeze decides,
   not the draft.
3. Keep one line per box; `grep -c '^## SHONEN'` must print 1 in the final report.
4. If F1/F2 are repaired after the freeze, they are **post-freeze corrections** and go into the
   report's findings, not into frozen claim text (append-only correction discipline).
