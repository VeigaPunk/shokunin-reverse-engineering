# R44Shonen — report `## SHONEN` skeleton (round 44, wave 1, pre-freeze)

Seat `R44Shonen` (scribe). Authored at lane HEAD `f5fb8d590f0dd6afc0847e1a63e8a3953bef8717`;
**the lane advanced during this seat** through `f18bdfb9fc8bb451ebab826c058049254d508483` and
`9a8de923053978342fdba6ce047e1cca4eda9dd2` — L1 commits `3b0fcaa9` (frozen `carriers.json` + unblob
`__output__` oracle trees), `f18bdfb9` (v2.1 LE/BE carriers, 6 total) and `9a8de923` (wave-1 seat
outputs incl. the probe-404 receipt). Observations below name the HEAD they were taken at; the
4-carrier rows are the `f5fb8d59` state, the 6-carrier rows the `f18bdfb9` state. Assignment base is
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
| C1 carrier pins | `tools/round-44/carriers.json` — **at `f5fb8d59`** sha256 `cb0f417b…` with **4** carriers (v1le/v1be/v2le/v2be); **at `f18bdfb9`** sha256 `2f61554e8d7ba631998982d6df79ed5cd6b1ff5ee2c32f946ccc62926e532278` with **6** carriers (`v21le`/`v21be` added, `squashfs_v2`, bytes under `corpus/evidence/round-44/carriers/`). **6/6 `sha256` pin_match true**, handlers `squashfs_v1`/`squashfs_v2`, `unsquashfs -s` exit 0 on all six (`2:1` for the v21 pair), `-lls` regular-file counts 3/3/4/4/4/4 = `expected_regular` | `obs-receipts.md` §carrier pins and §carriers.json at HEAD |
| C1 second oracle | unblob 26.6.4 `__output__` trees **committed at `3b0fcaa9`** under `corpus/evidence/round-44/oracle/`: 22 files, 7 distinct sha256, 152 content bytes, 10 listings, `failures 0`; v2 dirs carry **v2.0 and v2.1** extract trees per endian (see F4) | `corpus/evidence/round-44/oracle/manifest.json` `counts` |
| C1 target text | `PROVINCE.md:410` `## Round-42 additions to Core`; `:416` frontier note ends "Still Frontier: SquashFS v1/v2, …" — the text `## Round-44 additions to Core` must supersede | `PROVINCE.md:410,416` |
| C1/C2 counters | **absent at authoring** (wave-1 HEAD, and at base): `tools/round-44/c1-counter.py`, `c2-counter.py`, `c1-run.sh`, `c2-rubric.json` do not exist; `tools/round-44/` holds only `carriers.json` (08:12) | `ls tools/round-44/` |
| C2 census (landed at `9a8de923`) | rubric **not frozen yet** (`tools/round-44/c2-rubric.json` absent; counter absent — a draft sits at `w1/artifacts/R44C2Counter/c2-counter.py`, 1341 lines, not installed). Census outputs: `R44C2Shonen.json` 44 assertions / `n_stale_without_marker 0`; `R44C2Plan.json` 16 plan rows, `mismatches 2` (rounds 29, 30), 31 numbered sections; `R44C2SentReview.md` unresolved pointers SCORECARD 12 + README 1, and the frozen `tools/round-38/c2-counter.py` at BASE reports **5** owned-axes mismatches; `R44C2Sentinel.md` records command A at base = 137/137, 21/21 | `w1/R44C2{Shonen.json,Plan.json,SentReview.md,Sentinel.md}` |
| prior round | round 43 C1 scored `78/78`, `exit_code 0`, `met_target true`, freeze `f3f8db38`, revision `77d196c6` | `.ufo/waves/round-43/l1/scores/c1-at-77d196c6.json` |

**First claim-data commit:** `⟦slot: commit that first adds the round-44 C1 after-receipt⟧`.
**Pins at freeze:** `⟦slot: carriers.json sha256 at FREEZE⟧`, `⟦slot: c1-counter.py sha256⟧`,
`⟦slot: c2-counter.py sha256⟧`, `⟦slot: c2-rubric.json sha256⟧`.

---

## 4. What the frozen counters measure (targets, not results)

Paste-ready template — L1 replaces the right-hand column only.

| claim | counting command | target | result at REV |
|---|---|---|---|
| R44-C1 | `python3 -I -B tools/round-44/c1-counter.py --root <LANE> --rev <REV> --freeze <FREEZE> --pkg65 <rea-agents 6.5.0 root> --work <SCRATCH> --json-out <OUT>` | `carriers_matched == 4` per the draft — **must be reconciled with the 6-carrier frozen file (F6)**; every binding true, `frozen_path_changed []`, `met_target true`, exit 0 | `⟦slot: exit / carriers_matched / bindings_false / frozen_path_changed⟧` |
| R44-C2 | `python3 -I -B tools/round-44/c2-counter.py --root <LANE> --rev <REV> --freeze <FREEZE> --work <SCRATCH> --json-out <OUT>` | `mismatches == 0` over the frozen rubric, every check evaluable, `frozen_path_changed []`, exit 0 | `⟦slot: exit / mismatches / unevaluable⟧` |

Receipt fields that must be quoted for each (round-41 closure D4 + contract): `exit_code`,
`counter_sha256`, `counter_sha256_at_freeze`, sha256 of every post-freeze control receipt cited,
`stdout_sha256`, wall time. A receipt missing any of these is not evidence for this section.

**Slot, if C1 lands:** the promoted capability sentence, with the exact handler names and the
Core-row pointer —
`⟦slot: "SquashFS v1 (`squashfs_v1`) and v2 (`squashfs_v2`) Frontier → Core through REA 6.5.0
extract-firmware on 6 frozen MIT fixtures (v1 1.0 and v2 2.0/2.1, le/be each), independent oracle /usr/bin/unsquashfs 4.7.5;
PROVINCE.md:NNN; knowledge entry …; receipts corpus/evidence/round-44/c1/…"⟧`.

---

## 5. What stopped (or must stop) — the kill rules, stated before data

1. **C1 counterfactual controls.** If any of CTL-C1-0 (do-nothing), CTL-C1-1 (round-42 v3 receipts
   copied to round-44 paths), CTL-C1-2 (fabricated oracle-only envelope), CTL-C1-3 (sasquatch
   stripped from the child PATH) reaches the full carrier count with every binding true, C1 stops
   before data. Score all four at the freeze: `⟦slot: CTL-C1-0..3 exits and headline fields⟧`.
2. **C2 do-nothing control.** If the frozen rubric finds **zero** mismatches at base, C2 stops
   honestly — the do-nothing control reached the target, which proves the predicate wrong. Report
   the zero, do not loosen: `⟦slot: mismatches at base⟧`. Observed census candidates at base are
   **non-zero** (`R44C2Plan.json` 2; frozen `tools/round-38/c2-counter.py` at BASE 5; 13 unresolved
   pointers), so a zero would be a rubric-construction surprise — the frozen rubric's own count
   decides, not the census.
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

## 6. The mined mistake (class `stale-premise`) — attributed this wave

Draft text (`plans/round-44-claims.md:198-202`): the pre-freeze probe fetched
`squashfs_v2.0_be.expected` by guessing the fixture API shape (**HTTP 404**) before reading the
directory listing; captured-by = the frozen-URL convention (a URL is pinned only after a successful
open, never guessed); fix = verify URL existence via the directory-listing API first, with a red
(404) and green (200 listing) receipt shown able to fail.

**Status — resolved this wave by seat `R44MistakeHunt`, which reproduced both arms with URL, command
and sha256** (`.ufo/waves/round-44/w1/R44MistakeHunt.md:25-28`). The final report phrases it only as:

- Red: `curl -sS "https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/tests/integration/filesystem/squashfs/squashfs_v2/big_endian/__output__/squashfs_v2.0_be.expected"`
  → HTTP 404, body `404: Not Found` (14 B), wall 0.235 s; body sha256
  `d5558cd419c8d46bdc958064cb97f963d1ea793866414c025906ec15033512ed`
  (`.ufo/waves/round-44/w1/artifacts/R44MistakeHunt/guessed-expected-404.body`).
- Green: the correct listing URL returns HTTP 200 (221 745 B); page members are
  `squashfs_v2.0_be.bin_extract` and `squashfs_v2.1_be.bin_extract`, and `grep -c '.expected'` = 0
  (`tree-200.html` sha256 `e3ea23b9…2f46`; `member-names.txt` sha256 `99232795…0176`). Corroborated
  by the committed 200 listing `.ufo/waves/round-44/w1/R44SrcOracle/listings/squashfs_v2__big_endian__output__.json`.
- Corroboration: `.ufo/waves/round-44/l1/probe-fixture-404.txt` now exists and its 14-byte body has
  the **same sha256** `d5558cd4…`; the file itself names no URL, so cite R44MistakeHunt for
  attribution and this file only as body-hash corroboration.
- Fix, shown able to fail: verify URL existence against the directory-listing API before pinning —
  the red arm fails (404), the listing arm passes (200). Never pin a guessed member name.

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
for all six, which agrees with `unsquashfs`. **Action for L1:** correct the draft sentence before
the freeze; a counter frozen to expect "uncompressed" for `v2be` would fail a valid carrier, and a
counter frozen to accept two contradictory answers is not a predicate.

**F2 — `carriers.json` `superblock_layout` is v3/v4, not v1/v2 (still present at `f18bdfb9`).**
Subject: `tools/round-44/carriers.json` sha256 `2f61554e…` at `f18bdfb9` (was `cb0f417b…` at
`f5fb8d59`; the layout block is unchanged across both).
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
Freeze requirement (cross-check from seat `R44RevFreeze`): corrected `carriers.json` must also carry
`toolchain.unsquashfs` sha256 plus the frozen superblock text, so no counter or report needs a live
`file(1)` call for a frozen property.

**F3 — resolved this wave (recorded for the judge).** The originally cited
`.ufo/waves/round-44/l1/probe-fixture-404.txt` was absent when this seat started; it now exists
(14 B, sha256 `d5558cd4…`, body `404: Not Found`) and its body hash matches seat
`R44MistakeHunt`'s attributed red arm (URL + command in `w1/R44MistakeHunt.md:25-28`, artifacts
`guessed-expected-404.body` / `tree-200.html`). The l1 file alone names no URL — cite R44MistakeHunt
for attribution. No further action unless the judge wants the l1 file replaced by the attributed one.

**F4 — the oracle tree is wider than each carrier, so binding must be per-carrier exact.**
`corpus/evidence/round-44/oracle/squashfs_v2/` holds **two** extract dirs per endian —
`squashfs_v2.0_{le,be}.bin_extract` (4 files each) and `squashfs_v2.1_{le,be}.bin_extract` (4 files
each). Since `f18bdfb9` the v2.0 pair **and** the v2.1 pair are carriers, so both are legitimate —
but `v2le` must bind the v2.0 dir and `v21le` the v2.1 dir. A `*squashfs_v2*` glob would cross-wire
four carriers; match the exact extract-dir name (same trap class the fixture audit flagged for the
`v2ns-*` basenames). `carriers.json`'s `output_tree` fields are currently correct per carrier.

**F5 — paths are now committed; the draft's frozen-path list is stale.**
At `f5fb8d59` the oracle and `tools/round-44/carriers.json` were untracked (`??`); they landed in
`3b0fcaa9`, and the two v2.1 carrier blobs in `f18bdfb9`. The draft's frozen-path list names only
the four `corpus/evidence/round-42/c2/fixtures/*.bin` carrier files — it does **not** name
`corpus/evidence/round-44/carriers/*.bin`, which are now carrier bytes and must be frozen too.
Checklist: freeze must include `corpus/evidence/round-44/carriers/` (2 blobs) and the committed
oracle tree.

**F6 — the draft targets 4 carriers; the frozen `carriers.json` holds 6.**
Draft: "**Frozen carriers** … four frozen carriers", "Target: `carriers_matched == 4`", "four 4 KiB
fixtures with 3–4 regular files each". Committed state at `f18bdfb9`: `carriers.json` lists
`v1le, v1be, v2le, v2be, v21le, v21be` — **6** carriers, and the v2.1 pair's bytes are new
(`corpus/evidence/round-44/carriers/`, `fixture_id` `v2.1-le`/`v2.1-be`, source unblob 26.6.4
`__input__`). All 6 verify: `sha256` pin match, `unsquashfs -s` exit 0 (v21 pair = valid `2:1`),
`-lls` regular files 3/3/4/4/4/4 = `expected_regular`. **Action for L1:** amend the claim text and
the target to the 6-carrier set before the freeze (draft §"Changes from the draft" is still empty),
or state explicitly why the counter scores 4 of the 6 frozen carriers. A counter frozen to
`carriers_matched == 4` against a 6-entry frozen file is a count mismatch of the round-43 M43-2 class.

**F7 — C2 category (b) has two incompatible readings; both wave-1 attack seats flag it.**
`R44C2Sentinel.md` §B1: reading (b) as "reproduce under command A **at REV**" makes
`SCORECARD.md:23`'s "133/133 … at `e1c83313`" a **false** mismatch at BASE, and the sanctioned
"append a dated note" repair then greens it while the frozen cell contradicts itself — an exploit,
plus the same mechanism can rewrite history (B5 demo). `R44C2SentReview.md` G1: the same reading
yields **zero** mismatches (pins reproduce at their own pins), whereas the frozen predecessor
`tools/round-38/c2-counter.py` at BASE reports **5**. **Action for L1 before the freeze:** bind the
reading (stated-at-pin vs observed-at-REV) in the rubric contract, otherwise the calibration claim
either scores a false mismatch or scores nothing — and either way the SHONEN line cannot say
"calibration measured" honestly.

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
  entry; REA 6.5.0 extract-firmware on 6 carriers; carriers_matched/exit; receipt dir⟧`.
- [~] **Box 3 — instructions executable by an agent without oral context:** prior evidence
  `.ufo/waves/round-43/l1/scores/c1-at-77d196c6.json` (`exit_code 0`, `matched 78`, `met_target true`).
  Round 44: `⟦slot: c1-counter.py --selftest case counts + exit; c2-counter.py --selftest case
  counts + exit; CTL-C1-0..3 and CTL-C2-0..3 exits⟧`.
- [~] **Box 4 — no cross-domain bleed (`PROVINCE.md` accurate):** refusal list `PROVINCE.md:97-125`
  unchanged; round-43 frontier note `PROVINCE.md:418`; round 44 appends Core/status text only.
  `⟦slot: git diff BASE..REV -- PROVINCE.md row identities + confirmation that no Adjacent line
  moved; v2ns and the other Frontier rows still listed⟧`.

**Section-level honesty line (mandatory, fill one):**
- If both claims land: "R44-C1 `⟦6/6, exit 0⟧`; R44-C2 `⟦mismatches 0 at REV, exit 0⟧`; no axis
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
