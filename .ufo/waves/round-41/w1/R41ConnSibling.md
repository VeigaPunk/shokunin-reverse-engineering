# R41ConnSibling — sibling-overlap scan (read-only) for round 41 surfaces

Seat: `R41ConnSibling` (leaf; no subagents, no background jobs). Lane: kaidoku-shokunin
round 41 wave 1 (pre-freeze). Verdict: **DONE** — no sibling lane holds AVM / FRITZ!Box /
SquashFS / unblob / sasquatch / REA `extract-firmware` ground or an outcome-triage table on
this domain; the round-41 V3/V4/L3/L4 carriers and the v3 combined-gap-set table do not
duplicate any sibling's Core ground, and no sibling tree shows any run against the reserved
5490/5491/7560/3490 images. Four sibling-recorded defect patterns match classes this
round's counters must not repeat (suffix/basename path matching; fabricated-receipt
acceptance; frozen-path drift; post-freeze monitor drift) — detailed in
`artifacts/R41ConnSibling/defect-patterns.md`. Contested scope unchanged: tsukuroi ADJ-06
kaidoku/revenger arbitration remains unresolved and must not be settled by this round.

Bounds compliance: this report plus `artifacts/R41ConnSibling/{scan-evidence.txt,
defect-patterns.md}` were written; nothing else. No VCS mutation; no REA/unblob runs (a
read-only scan needs none — and the reserved carriers forbid it); no tool installs
(built-in `read`/`grep`/`bash` only). Scratch `$S` created and removed; no scratch paths
cited as evidence.

## 1. Method (exact commands; all read-only, run 2026-10-26)

1. Lane inventory: `ls -d /home/vgpnk/Projects/shokunin/*-shokunin` → 21 lanes; sibling
   set = all except `kaidoku-shokunin` (20 lanes).
2. Carrier/AVM reference scan: `grep -rlE '5490|5491|7560|3490|6490|6820|7430|6590|FRITZ|fritzbox'`
   over every sibling lane, then `grep -nE` context on every content hit; plus
   `grep -rn 'download.avm.de|avm.de|filesystem.image|filesystem_core'` outside kaidoku.
3. Domain ground scan: `grep -rln 'squashfs|sasquatch|sqfs|unsquashfs'` over all 20
   sibling `tools/` dirs; `grep -rn 'extract_firmware|inspect_firmware'` over
   revenger `corpus/` + `SCORECARD.md` + `SKILL.md`; `grep -c 'decision table' */SKILL.md`.
4. Routing/scope reads: `tsukuroi-shokunin/PROVINCE.md` (ADJ-06/OUT-008/OUT-009/R20-OUT009),
   `kotoba-shokunin/PROVINCE.md:61`, `game-dev-3d-shokunin/PROVINCE.md` (REA lines),
   `revenger-shokunin/corpus/README.md:69-74` (C07), `corpus/knowledge/round-64-firmware-region-byte-evidence.md`.
5. Defect-pattern hunts: `grep -rnE 'suffix|basename'` and `grep -rnE 'frozen.?path|frozen_path'`
   over sibling `corpus/lessons`; targeted reads of tameshi r25/r26, chousa r26, kagi r13,
   kake r20/r24/r26/r45/r47, revenger r63/r64/r68/r70, tsukuroi r18; closure check
   `grep -l firmware revenger-shokunin/corpus/lessons/round-{65..70}*.md` and
   `grep -n 'MtGuardGaps|basename|commonprefix' tameshi round-27..48 lessons`.
6. shokuknow (read-only): `ls /home/vgpnk/Projects/shokuknow/merge/kaidoku/knowledge/corpus/knowledge/ | grep -i avm`;
   `grep -rln '5490|5491|7560|3490'` there.

Full captured output: `artifacts/R41ConnSibling/scan-evidence.txt`.

## 2. AVM / FRITZ!Box / vendor-firmware extraction ground — none in siblings

- **Zero sibling references to any reserved or development carrier.** Every content hit
  from scan 2 is a false positive inside git-object hex or sha256 digests (e.g.
  `revenger-shokunin/corpus/lessons/round-68.md:4` hash `f165908a…` contains the substring
  "6590"; `chousa-shokunin/corpus/knowledge/audit-r11.md:307,311` hash fragments
  `46534902…`/`e3490cf4…`). `download.avm.de`, `filesystem.image`, `filesystem_core`
  appear nowhere outside kaidoku. So no sibling has run REA/unblob against 5490/5491
  (V3/V4 source images), 7560/3490, or any AVM image — consistent with the reserved-carrier
  bound holding fleet-wide.
- **shokuknow merge package** (producer/campaign records, read-only): the six AVM entries
  under `/home/vgpnk/Projects/shokuknow/merge/kaidoku/knowledge/corpus/knowledge/`
  (`avm-image-extraction.md`, `avm-le-image-genuine-marker.md`,
  `avm-le-variant-reachability.md`, `avm-firmware-image-unblob.md`,
  `avm-image-build-blocker.md`, `sasquatch-unblob-avm-branch.md`) are unchanged.
  `avm-firmware-image-unblob.md:4-23` measures the **6490 Cable** (round-40 V1) only;
  `grep '5490|5491|7560|3490'` over the merge tree returns nothing — the round-41 V3/V4
  carriers have **no prior measurement anywhere**; the round's own carve stands alone.
- **revenger-shokunin** declares firmware in its RE domain (`PROVINCE.md:3-7`) and its
  README C07 row (`corpus/README.md:71-74`) names REA `inspect_firmware_regions` /
  `extract_firmware` as a *need*, but its only firmware ground is the authored 2048-byte
  synthetic fixture `corpus/fixtures/firmware-r63/` with one saved
  `inspect_firmware_regions` record (round-63, Binwalk 3.1.0). Its knowledge entry
  (`corpus/knowledge/round-64-firmware-region-byte-evidence.md:5,10`) states explicitly:
  "This entry does not cover the REA `extract_firmware` route, vendor or device firmware
  families, any container format" and (:203) "does not absorb kaidoku Core's live
  `inspect-firmware-regions` / `extract-firmware` surface". Rounds 65-70 added nothing
  (`round-70.md:95-96` is an assimilation *theme* about firmware-extractor upstream facts
  with "Adoption: none appended"). M34 (`round-63.md:219`; `SKILL.md:592-593`) — a shaped
  JSON with a fabricated `evidence_id` + `operation` satisfies its presence predicate,
  the same fabrication limit kaidoku recorded as R39-CL5 — remains disclosed, unfixed.
- **tsukuroi-shokunin** owns the driver/firmware *health* plane only and refuses internals
  (`PROVINCE.md:4,11-12,26-27`); **game-dev-3d-shokunin** uses REA as supporting static
  inspection for 3D evidence, pins `rea-agents@6.4.0` "within authorized scope", and
  refuses live-target analysis (`PROVINCE.md:8-12,30-41,70,78`).
- **mori-shokunin** routes "driver/firmware and boot state (→ tsukuroi)" (`PROVINCE.md:13`)
  and names tsukuroi the owner of "host OS, package, systemd-unit, driver, firmware, and
  boot diagnosis" (`PROVINCE.md:66`) — host health, not artifact RE.

## 3. SquashFS layout readers / writers — only kaidoku

`grep -rln 'squashfs|sasquatch|sqfs|unsquashfs'` over all 20 sibling `tools/` dirs: zero
hits (scan-evidence.txt §3). kaidoku's `tools/round-36..40/` remain the fleet's only
SquashFS readers/writers (`gen-squashfs.py`, `sqfs-list.py`, `mk-l-carriers.py`,
counters). No sibling instrument exists to collide with the round-41 AVM-layout writer or
the exact-match counter port.

## 4. REA extract-firmware receipts — only kaidoku

Only kaidoku's `corpus/evidence/round-36..40/c1/` holds `extract-firmware` receipts
(K1-K6, V1/V2/L1/L2). No sibling receipt exists on any image, vendor or synthetic —
revenger's synthetic fixture never ran `extract_firmware` (§2). The round-41 claim that
"none of V3/V4/L3/L4 was touched by any REA or unblob run before the freeze" cannot be
contradicted by anything in a sibling tree.

## 5. Outcome-triage / decision-table instruments — none on this domain

Twelve sibling SKILL.md files carry decision-table instruments (scan-evidence.txt §4:
game-dev-3d 1, kagi 3, kasegi 2, kengaku 1, kumitate 1, lore 1, mado 2, mori 4, revenger 1,
tabi 10, tameshi 1, tsukuroi 12). None covers SquashFS/REA envelopes, a scored
`(label, action)` vocabulary, an `operation`/`provider` domain guard, or combined-gap-set
rows. Closest shapes (unchanged from the round-40 scan): kotodama's closed-vocabulary
`to-verify-triage-protocol.md`, tabi's `check-decision-table.mjs` gate, kasegi's
finding-triage table, mori's journal classification, tsukuroi's health-verdict table.
R41-C2's v3 combined classes (partial+in-tree, partial+mixed, depth-limited+{in-tree,
mixed, alone}) have no sibling precedent; the repair of R40-CL5 and the
independent-evaluator scoring (D3) are likewise kaidoku-unique — with one precedent *shape*:
kake's round-26 closure parser was "independently written from the reviewed rule rather
than importing the lane module" (`kake-shokunin/corpus/lessons/round-26-verifier-spotcheck.md:33`),
and tsukuroi's round-18 used a "Same independent evaluator on baseline"
(`tsukuroi-shokunin/corpus/lessons/round-18.md:9`). The generator/evaluator split is a
pattern siblings have used and validated, not contested ground.

## 6. Defect patterns a sibling recorded that this round's counters could repeat

Full table with quotes: `artifacts/R41ConnSibling/defect-patterns.md`. Summary:

1. **Suffix/basename path-matching (R40-CL1 class)** — tameshi MtGuardGaps
   (`corpus/lessons/round-25.md:88-92`): 17 weakenings incl. "cwd
   prefix/basename/commonprefix" and "revision prefix or suffix compare" survive its gate
   selftest; **still open** (`round-26.md:78` recheck 0/17 killed; never closed through
   round-48). chousa R26-M2 (`corpus/lessons/round-26.md` `## Mistakes`): basename
   matching vs required repo-relative exact paths, fixed with negative same-basename
   controls — the same fix shape as the round-41 exact-match port. kagi r13
   (`corpus/lessons/round-13.md:102`): prefix-match mutation `R12-03a`→`R12-03`, fixed
   with whole-word extraction + `verify-suffixed-id`/`verify-prefixed-id` selftest cases.
   kake r47 (`corpus/lessons/round-47.md:102`): "basename-matcher and doctored-index
   shortcuts can pass".
2. **Fabricated-receipt acceptance (R39-CL5 class)** — revenger M34
   (`corpus/lessons/round-63.md:219`; `SKILL.md:592-593`): fabricated
   `evidence_id`+`operation` JSON satisfies the predicate; revenger's routed fix
   ("receipt/Evidence-ID binding check", `round-64.md:200`) is still unlanded. Kaidoku's
   scoring-time REA rerun already addresses this for C1; the sibling record corroborates
   the threat is real and live elsewhere.
3. **Frozen-path drift (freeze-integrity rule class)** — kake SentinelFrozen
   (`.ufo/waves/round-45/w1/SentinelFrozen.md:13`): "preserve the original
   `before.sha256` … Do not replace the baseline to bless this drift" — the sibling
   statement of kaidoku's "a later restore does not un-block". kake r20/r24: suffix
   additions that rewrite historical lines were rejected; hash-bound sidecar corrections
   preserve original bytes. tameshi r48 (`corpus/lessons/round-48.md:404`): a claim's own
   record edits moved a pre-registered no-harm monitor after freezing, silently dropping
   credited counts 60→57 — monitors pinned before the freeze must keep their pinned
   inputs.

None of these is absorbed; they are corroboration that the round-41 draft's exact-match
port, both-direction collision selftests, scoring-time rerun and freeze-integrity rule
(target classes, not borrowed code).

## 7. Contested scope (unchanged; the round must not settle it)

- **tsukuroi ADJ-06** (`tsukuroi-shokunin/PROVINCE.md:51`): "shipped-artifact reverse
  engineering beyond health inventory" → "protocol integrator — kaidoku/revenger ownership
  **unresolved**". OUT-008 (kaidoku declaration) / OUT-009 (revenger declaration) at
  `:127-129`; R20-OUT009 at `:148-152`: "Kaidoku/Revenger arbitration remains unresolved;
  ask the protocol integrator before an internals handoff." No change since the round-40
  scan.
- **kotoba** (`kotoba-shokunin/PROVINCE.md:61`): "kaidoku's only open split is with
  revenger".
- **revenger's declaration** (`revenger-shokunin/PROVINCE.md:3-7`) includes firmware in
  its RE domain, but with zero vendor-image/SquashFS/extract-firmware ground (§2/§4) — a
  declaration, not held ground.

## 8. Cross-domain items the round report should name (R40-CL6-style line)

1. shokuknow merge AVM record (producer/campaign, not a lane): six entries; the only
   measured vendor image is the 6490 Cable (round-40 V1). V3 (5490) / V4 (5491) are
   unmeasured anywhere; do not cite the producer as prior art for them.
2. tsukuroi ADJ-06 / OUT-008 / OUT-009 / R20-OUT009 — arbitration open (§7).
3. revenger's firmware declaration + M34 fabrication disclosure + its deferred
   receipt/Evidence-ID binding check (§2/§6).
4. Adjacent instrument shapes: kake/tsukuroi independent-evaluator split (§5);
   kotodama/tabi/kasegi/mori decision tables; tameshi/chousa/kagi path-matching defect
   records (§6) — adjacency, not absorption.

## 9. Second-order notes for the L1

- The draft's V4 fallback ("the nested `filesystem_core.squashfs` of the 5491 … if it is
  AVM-BE and fits REA's entry budget at depth 1") is decision-shaped pre-freeze; nothing
  in any sibling tree informs that budget — [INFERENCE] the entry-budget probe must be
  kaidoku's own (as the draft already plans).
- No sibling gate or counter would be invalidated by R41-C1/C2 landing; the only
  ownership item the report should explicitly not resolve is tsukuroi ADJ-06.
- The tameshi MtGuardGaps record (17 surviving weakenings, unfixed through its round-48)
  is worth one line in the round report's cross-domain section: it is the same defect
  class as R40-CL1 observed live in a sibling's shipped gate — evidence the class is
  easy to ship and hard to selftest away.

## 10. Evidence backstop

Scans and reads above are reproducible with the commands in §1; all cited sibling paths
were read at working-tree bytes on 2026-10-26. Captured outputs:
`artifacts/R41ConnSibling/scan-evidence.txt` (34 lines) and
`artifacts/R41ConnSibling/defect-patterns.md`. No REA/unblob/git-mutating commands were
run; no tools installed (nothing to record under the tooling rule); scratch
`/fast/scratch/hyaku/kaidoku-r41/R41ConnSibling` removed at finish.
