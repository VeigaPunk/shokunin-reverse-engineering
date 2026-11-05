# ConnectorOverlap — R95-W1 sibling-overlap scan (receipt-binding + symlink write-escape classes)

Seat: ConnectorOverlap (connector), lane kaidoku, round 95 attempt 1. Read-only: no lane or
sibling file edited. Claims frozen at 4bda1d1dd3788973f10e61212b70df18b3b14ea0 (base
b5331db1fb0ce0bf93695ce1730cf831effef6a9). Axes touched: coverage (sibling scan), depth
(block-34 evidence), freshness (sibling pins taken today).

## Method (all commands exit 0 unless noted)

- Read `plans/round-95-claims.md` and `.ufo/waves/round-95/claims.json` first (mandated).
- Sibling set: 20 sibling lanes under /home/vgpnk/Projects/shokunin/*-shokunin minus
  kaidoku. Trees with hits: tools/ in chousa, kotodama, kama, mado, mori, souji, tameshi,
  tsukuroi; scripts/ in kake, kumitate, tabi. Other siblings have no tools/ or scripts/ tree.
- Patterns: `O_NOFOLLOW|mkstemp|\.tmp|json-out|json\.dump|planted|symlink|receipt`
  (broad pass), narrowed to `\.tmp|mkstemp|O_NOFOLLOW` for classification, paged per lane.
- Lane at the frozen commit:
  `git -C kaidoku-shokunin grep -n -e 'json.dump' -e 'mkstemp' -e 'O_NOFOLLOW' 4bda1d1d... -- tools`
  (1475 matching lines) and `git grep -n -e '\.tmp"' 4bda1d1d... -- tools` (10 hits).
- Tooling note: two early grep calls using `*-shokunin/tools` glob paths plus a `!` exclusion
  returned "No matches found" — a false zero (explicit-path rescans of the same trees return
  hundreds of hits). Treat those two calls as discarded; every number below comes from
  explicit-path scans.

## Table 1 — sibling hits relevant to the two classes

| lane | path:line | class | writes receipt/like file through a predictable temp name? | claims-overlap (r95) |
|---|---|---|---|---|
| kake | scripts/instrument_receipts.py:643-646 | receipt writer, exact v4 shape: `temporary = destination + ".tmp"`, plain `open`, `os.replace`; destination `corpus/knowledge/instrument-receipts.json` (RECEIPT_PATH:95, receipt_path:365) | YES — plain open follows a planted `<dest>.tmp` symlink | no — kake freeze.md claims C1 self-assessment counter + C2 conditional contract only |
| tabi | scripts/aria-loopback-round13.mjs:103-105, 805-807 | receipt writer via `.receipt.<pid>.tmp` writeFileSync + rename (no wx flag) | YES — pid-predictable, follows symlink | no |
| tabi | scripts/webmcp-invoke-round17/18/19.mjs:2108/2979/3183 | receipt writer `.receipt.<pid>.<ts>.tmp` with flag `wx` (O_EXCL: refuses, never follows) | no — hardened by O_EXCL | no |
| tameshi | tools/bash-witness-study.py:795-797 | JSON evidence writer `path.suffix + ".tmp"` + replace | YES | no |
| mori | tools/mori-round13-regressions.py:572-574 (same shape r14:373, r15:219/229, r16:182/191; r17:324 pid-suffixed) | evidence.json writer via `<name>.tmp` / `.<name>.tmp` | YES (r13-r16 shapes) | no |
| kotodama | tools/gates/costume-era-consistency-gate.py:1494, lexicon-coverage-audit.py:1456, myth-consistency-gate.py:1072, phonology-sanity-gate.py:1281, provenance-audit.py:420 | fixture pin writer `<path>.tmp-<pid>` plain open + fsync + replace | YES — fixture bytes, not receipts | no (no plans/ or r95 claims dir) |
| souji | tools/impl-05.sh:224, cand-merge-selftest.sh:232-233, souji-round9-selftest.sh:212-213 | ledger writers `${file}.tmp.$$` + mv | YES (pid) — ledger, not receipt | no |
| souji | tools/souji-receipt-write.py:530-542, 635-638 | HARDENED receipt writer: mkstemp unique in outdir, stale `<out>.*.tmp` sweep, "a temp is never a receipt", no-stray check (r60 amendment 3) | no | no (landed r60; no r95 claim) |
| kama | tools/kama-llamacpp-live.py:337-347, 1979-1980 | HARDENED witness-announce writer: `ready.json.tmp.<pid>` + O_EXCL+O_NOFOLLOW ("a symlink planted at the temp name is never followed", r49 Sen1Witness F1); mkstemp atomic publish | no | no (remediated r49) |
| kama | plans/round-72-claims.md:67-90 | RECEIPT_TIP_BINDING claim — every cited receipt must carry a `# rev=<40-hex>` header naming an ancestor of tip (revision-binding class, the M94-f family) | read-side counter | no current-r95 claim; historical r72 claim = independent discovery of the revision-binding class |
| kumitate | scripts/receipt-bind.mjs:1-63, 287-291 | receipt↔instrument-bytes binding checker at a judged revision (`git cat-file blob`), fail-closed SYMLINK_DIR/SYMLINK_RECEIPT/SYMLINK_INSTRUMENT, O_NOFOLLOW receipt read (capability landed r87-r90) | checker, read-side | no |
| kumitate | scripts/cap-run.mjs:214-216 | verdict-file writer O_EXCL+O_NOFOLLOW (new file, never follows) | no | no |
| kumitate | scripts/make-dispatch-actual.mjs:384-386 | dispatch JSON writer `${path}.tmp-${pid}` plain writeFileSync | YES — dispatch artifact, not a receipt | no |
| kumitate | scripts/omp-census.mjs:232 | snapshot writer randomUUID temp | no | no |
| chousa | tools/build-spans.py:341-346 (also 76, 79, 284) | hardened atomic writer `.{name}.{token_hex(6)}.tmp` O_EXCL+O_NOFOLLOW, dir_fd reads, refuses leftover `.tmp` | no — random temp | no |
| chousa | tools/argv-witness.py:369-370, mechanism-witness.py:311-312 | receipt writers direct `open(--json)` (no temp) | no temp (direct final name) | no |
| chousa | tools/receipt-pin.py:44-70; tools/digest-in-tree.py:137-151 | receipt header-consistency checker; "every sha256 a receipt pins must re-derive from committed bytes" (= the pins-not-bound family, landed r65/r67) | checker, read-side | no |
| kotodama | tools/check-advance-evidence.py:772-779 | receipt writer direct open `receipt` / `receipt + ".json"` | no temp (direct final name) | no |
| kake | scripts/capture_delta.py:252-253 | response.json receipt writer (fixture builder), direct open | no temp | no |
| mado | tools/mado-options.py:1527-1531 | planted `.tmp`-directory + symlink refusal test fixture (hardened-reader testing) | n/a | no |
| kake | scripts/base_path_audit.py:242-309, canonical_audit.py:545-598, citing_set_selftest.py:445 | O_NOFOLLOW readers | read-side | no |
| mori | tools/mori-seat-terminal.py:16-27, mori-evidence-loss.py:38, mori-journal-window.py:251, mori-misroot-sweep.py:183, mori-wave-settlement.py:142 | O_NOFOLLOW descriptor-relative walks/reads | read-side | no |
| tsukuroi | tools/score-pacnew-arm-r35.py:168, r35b:307 | `.pacnew.tmp` strings are fixture log text; rest of tree is read-only verifiers | no | no |
| lore | .ufo/waves/round-95/scratch/V20/map_obligations.r94.py:70-86, 554-559 | `symlink_path` input-safety self-test (symlink refusal), not a writer | n/a | no |

## Table 2 — lane call sites at 4bda1d1d carrying the receipt-writer role

`git grep -l json.dump` → 265 files; `json_out` → 155 files; `mkstemp` → 7 files; `O_NOFOLLOW` → 1 file (round-42).

| lane | path:line | class | claims-overlap |
|---|---|---|---|
| kaidoku | tools/round-94/stop-boundary-repair-battery-v4.py:62, 65-68, 131 | receipt writer (`write_receipt`): `tmp = path + ".tmp"`, plain open, os.replace — the SentinelWrite F1 defect carrier; predictable temp, follows a planted symlink | YES — R95-C1 before-side, pinned (v4 unedited) |
| kaidoku | tools/round-95/stop-boundary-repair-battery-v5.py:76-79, 252 | receipt writer hardened: `tempfile.mkstemp(dir=d, prefix=basename, suffix=".tmp")` + fsync-family writer; unique name, planted `<json-out>.tmp` neither read nor followed | YES — R95-C1 after-side candidate |
| kaidoku | tools/round-95/symlink-probe.py:63-65, 98-99, 103-106 | probe instrument: plants `<target>.tmp` symlink, runs the writer's public CLI, records victim_intact/tmp_is_symlink; writes its own receipt via direct open | YES — R95-C1 probe |
| kaidoku | tools/round-95/c1-agreement-v2.py:181, 243, 280 | strengthened instrument: world/rec receipts direct open | YES — R95-C1 counter |
| kaidoku | tools/round-95/c1-forgery-refusal.py:131, 269 | forgery battery receipt direct open | YES — R95-C1 counting command |
| kaidoku | tools/round-93/stop-boundary-repair-battery-v3.py:352-353 | v3 verdict receipt direct open (imported by v5 by sha-pinned path) | YES — R95-C1 verdict base, pinned |
| kaidoku | tools/round-93/craft-citation-semantic.py:276-277 | depth checker receipt direct open | YES — R95-C2 counter |
| kaidoku | tools/round-42/fetch-carrier.py:276, 307 | only O_NOFOLLOW site in tools: carrier temp O_WRONLY+O_CREAT+O_EXCL+O_NOFOLLOW, re-hash O_NOFOLLOW, rename | no (landed precedent of the fix mechanics, not claimed this round) |
| kaidoku | tools/round-89/upx-field-value-repair.py:326; round-90/upx-break-repair.py:122; round-91/upx-stop-boundary-repair.py:105,145; round-90/upx-later-block-battery.py:216; round-92/upx-stop-boundary-search-repair.py:102 | mkstemp atomic payload/probe writers in repair tools (F5/F6 lineage) | no (precedent) |
| kaidoku | all other 155 `--json-out` carriers (r34-r94 counters, batteries, depth tools) | receipt writers via direct `open(json_out, "w")` at the final name — no temp step | no individually; covered by the class only at the final-name symlink variant, which no current claim covers |

## Overlap verdict

1. **Receipt world-binding class: no sibling round-95 declaration claims it.** Only three
   siblings have round-95 wave dirs: kake (freeze.md = self-assessment counter + conditional
   contract), lore (snapshot/map obligations), mori (preservation census + script inventory).
   Landed sibling instruments of the same *family* exist and should be cited as independent
   discovery, not ported: kama r72 RECEIPT_TIP_BINDING (revision binding), kumitate
   receipt-bind v4 (instrument-byte binding, fail-closed symlink rows), chousa
   digest-in-tree (pin re-derivation from committed bytes) + receipt-pin (header
   consistency). Kaidoku's four typed bindings + writer self-verification are unclaimed
   fleet-wide.
2. **Symlink write-escape in a receipt writer: no sibling round-95 claim, but the defect
   class is live in siblings while the *fix* pattern is fleet-proven.** Hardened precedents:
   souji r60 (mkstemp + stale-temp sweep + temp-is-never-a-receipt), kama r49 (O_EXCL +
   O_NOFOLLOW at the temp name), kaidoku r42 fetch-carrier, tabi webmcp r17+ (`wx`).
   Unremediated v4-shape instances still write through predictable temp names in sibling
   live trees — cleanest instance kake `scripts/instrument_receipts.py:643-646` (a receipt
   writer, plain `open(<dest>.tmp)`), then tabi aria-loopback-round13.mjs, tameshi
   bash-witness-study.py, mori r13-r16 regression writers, kotodama gate fixture pinners,
   kumitate make-dispatch-actual.mjs.

## Proposed move (one bounded synthesis)

In the R95-C2 block-34 draft the L1 lands after this wave, ground the `temp-file symlink
escape` decision-table row in fleet-wide recurrence: the knowledge entry cites the pinned
sibling instances (kake instrument_receipts.py digest 162dd6852cd5f6adbf278405365464f0b2f5c5d66100883a0974c32b0e6a68e7
at kake commit 4f443b3fd79f88fc75cfe46005c01d3ecd85c16f, last touched 2026-11-03; tabi
aria-loopback-round13.mjs digest 1d54c9e98a85022c4382d0a0eeb16e15f0256b7f561329258e7ca77152e4af9c)
alongside the S320 O_NOFOLLOW source, and the round-95 lesson records that the v4 writer
shape survives unclaimed in sibling lanes while three lanes (souji r60, kama r49, kaidoku
r42/v5) already hold the fix. This improves depth (block 34 is a fleet-recurring class, not
a single-lane anecdote) and freshness at zero cost to C1: no frozen byte moves
(tools/round-95, round-94, round-93 untouched), so the kill-rule diff clause stays empty.
Rejected alternative: aiming symlink-probe.py at kake's writer — CLI contract mismatch
(no --json-out/--rev/--expect) makes that a new instrument, outside this read-only item and
into kake's ownership.

## Risks

- Sibling bytes are mutable mid-wave (kake runs an active r95 wave); any citation must carry
  the blob digest + observed commit (given above). If kake lands a fix first, the citation
  flips to "remediated at <commit>" — the pin makes the flip checkable.
- Boundary: sibling facts were gathered read-only (grep, sha256sum, git rev-parse/log); no
  sibling file edited; the recommendation is kaidoku-side corpus text for the L1 to decide.
- Vocabulary collision: kake's r95 "forgeries refused 7/7" / "equivalence receipts" share
  words with R95-C1 but are different classes (contract-input forgeries vs receipt-triple
  forgeries). Block-34 wording should keep the two named apart.

## Second-order traces

- Runtime: v5's unique mkstemp name means a pre-planted `<json-out>.tmp` symlink is simply
  never used and left in place — the probe records `tmp_is_symlink` rather than cleaning,
  which keeps "victim intact" honest. Souji needed a stale-temp sweep only because its old
  temps were predictable-patterned; v5 needs no sweep.
- Contract: sibling binding instruments cover facets C1's bindings do not (instrument bytes,
  tip ancestry); none covers label-recompute — no weakening of R95-C1's novelty. Read-side
  fail-closed symlink refusal (kumitate SYMLINK_RECEIPT) is the natural future counterpart
  to the write-side fix — out of this round's frozen scope.
- Verification: the c1-forgery-refusal honest leg + junk-manifest control remain the
  rubber-stamp guards; sibling citations live in corpus text, so they change no counter
  input.
- Substrate/host: no host change used or needed; no pacman; no sysctls; no tool installed.

## Files written by this seat

- .ufo/waves/round-95/w1/ConnectorOverlap/overlap.md (this file)
- .ufo/waves/round-95/w1/ConnectorOverlap.md (scoped report, same content summary)
