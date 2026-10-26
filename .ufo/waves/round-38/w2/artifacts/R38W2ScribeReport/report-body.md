# kaidoku — round 38 (attempt 2) report body (draft, not filed)

Draft scope: the three sections named in the seat assignment. Integrator owns the status line,
`Sources & frontier`, `Trend verdicts`, `SHONEN` and the end census. Every pointer below was read
at the named commit with read-only git; nothing here is re-measured. [INFERENCE] marks a step
derived from counter source rather than from a stored exit code.

**Line numbers are HEAD's (`e265533e`).** While this draft was being written, another seat edited
three tracked corpus files in the worktree after HEAD — `corpus/lessons/round-38.md`,
`corpus/knowledge/2026-10-26-r38-sasquatch-be-squashfs-recursion.md`,
`corpus/knowledge/2026-10-26-unblob-format-matrix.md` (`git diff --stat HEAD`, 17 insertions /
13 deletions) — and an untracked `paths_raw.txt` appeared at the lane root. Re-anchor line numbers
after the integrator's commit; one content conflict from that drift is recorded in Receipt note 8.

## Work performed

The round froze two claims in its **first** freeze `e059ca9391642d5b71b6662cabcbdce0d9308719`
(`plans/round-38-claims.md` there, sha256 `13ea8eba917f487e0b1e876d2846f77c0c259dd0ba6066d31906284608109815`):
**R38-C1** on the **coverage** axis — standard big-endian SquashFS v4 moves from the PROVINCE
Frontier to Core, measured through REA `extract-firmware` on four frozen carriers; **R38-C2** on
the **calibration** axis — the lane's self-assessment surfaces carry zero mismatches with observed
repo state. Owned axes coverage / depth / calibration were tied at 10 and none retired, so C1 took
coverage and C2 calibration (`plans/round-38-claims.md` at `e059ca93`, ¶"Owned axes"). Both claims
are judged by the first-freeze bytes; the attempt-1 amendments `79f69347` (predicate + counter) and
`f1010f67` (gap clause) came after wave-1 seats had already scored carriers, so they are reported,
not adopted (QUALITY 79, `corpus/QUALITY.md:87`).

- **Freeze integrity measured, not assumed.** `tools/round-38/freeze-drift.py` was run over the
  first freeze against the amendment point: exit 1, drift list `f1010f677a53ecf0e671952ce1bf4f44d51e151b`
  and `79f693470eae0f2935a4bbf6e4875ef3ec40fb06` (`.ufo/waves/round-38/l1/freeze-drift-077e212b.json`);
  the same run over the harness-fix point is clean (`…/l1/freeze-drift-cb4326b2.json`, `drift: []`);
  the same run over the control generator is drift at `efd5c47a72a50b3a434783f82268fb4a96e636a1`
  (`…/l1/freeze-drift-gen-controls.json`). The frozen counter bytes hash
  `a7a62b098709035607375078a12d2668bb6d36bbabfc5a7459f04d00a9516db8`
  (`git show e059ca93:tools/round-38/c1-counter.py | sha256sum`), which is the digest the scores cite.
- **Carriers and oracle frozen before data.** K1/K2 are synthetic standard-BE v4 gzip images
  (`tools/round-37/gen-squashfs.py`); K3/K4 are the unblob 26.6.4 `squashfs_v4_be` integration
  fixtures. Oracle rows: 5 / 3 / 4 / 4 = 16 regular files
  (`corpus/evidence/round-37/c1/K{1..4}/oracle.tsv`, counted with `grep -c .`).
- **Both arms run through REA, receipts committed.** `extract-firmware` (rea-agents 6.5.0, unblob
  26.6.4 — the engine version is inside each receipt) with `$HOME/.local/bin` off PATH for the
  before arm and reachable for the after arm. Before: 0 published files and one
  `missing-extractor-dependency` [`sasquatch-v4be`] gap per carrier, all four
  (`corpus/evidence/round-38/c1/K*/before.json`, `normalized_result.extraction_gaps`);
  after: 5/5, 3/3, 4/4, 4/4 oracle files (`corpus/evidence/round-38/c1/K*/after.json`).
  Committed in `3b960fe5f9a7f1dfa22819f98dc0fa983f4260a8`.
- **First-freeze counter at the landing.** `carriers_matched 3`, `met_target false`; bindings
  `province_core_row false`, `province_core_section false`, `frontier_note true`, `entry_present true`,
  `sourced true`, `coverage_map_row true`, `entry_source_ids [S112, S113, S114]`
  (`.ufo/waves/round-38/l1/scores/c1-v1-at-3b960fe5.json`, committed at `0fc61133`). The counter
  returns 0 only when `met_target` (`tools/round-38/c1-counter.py:268` at `e059ca93`), so exit 1
  [INFERENCE; the receipt stores no exit field].
- **Why K2 fails, stated from its own receipt.** `after_gaps_empty false` with exactly one gap,
  `kind: unpublished-entry`, `relative_path firmware.bin_extract/var/lib/run-link`, and
  `normalized_result.unpublished_entries` `{kind: symlink, link_target: ../../a/run.sh}`
  (`corpus/evidence/round-38/c1/K2/after.json`). K1's symlink points out of the extraction root and
  the run logs `MaliciousSymlinkRemoved` instead, so K1 has no gap
  (`…/K1/after.json` `normalized_result.diagnostics`). "No extraction gap" is therefore unreachable
  on any carrier with an in-tree symlink — the entry says so at
  `corpus/knowledge/2026-10-26-r38-sasquatch-be-squashfs-recursion.md:33-42`.
- **C1 landed as Frontier knowledge, not as a capability.** No `## Round-38 additions to Core`
  heading exists in `PROVINCE.md` at `3b960fe5` or at HEAD (the last Core round heading is round 36,
  `PROVINCE.md:368`); the round-38 statement sits inside the existing Frontier bullet,
  `PROVINCE.md:157`, and the entry's `**Status.**` paragraph states the stop
  (`corpus/knowledge/2026-10-26-r38-sasquatch-be-squashfs-recursion.md:44-48`). SCORECARD's own
  line agrees: "No capabilities row enters" (`SCORECARD.md:3408`).
- **C2 measured at the commit that lands its section.** One mismatch at base `77091b49`
  (`evidence/doctor/` in the PROVINCE Core `REA MCP server` row), 0 mismatches at `0fc61133` with
  `guards_ok true` (receipt on disk `.ufo/waves/round-38/l1/scores/c2-at-0fc61133.json`; see the
  receipt note below — the file the scored surfaces name does not exist).
- **C2's pointer repaired to the same document, not to a same-basename decoy.**
  `PROVINCE.md:44` now reads `.ufo/waves/round-19/evidence/doctor/` (doctor-6.5.0.txt,
  doctor-6.7.0.txt); the base read `evidence/doctor/`
  (`git diff 77091b49 3b960fe5 -- PROVINCE.md`). Receipt guards: `pointers 52` vs `base_pointers 48`,
  `pointers_not_fewer true`, `missing_units []`, `unrepaired []`, `base_unresolved
  [["prov_core:REA MCP server", "evidence/doctor/"]]`.
- **Coverage proxy recounted independently.** 126 `corpus/knowledge/*.md`; all 126 stems occur in the
  `## Coverage map` section (`corpus/README.md:11-93`); no stem in the map lacks a file and none
  lacks a row. The two round-38 stems are `corpus/README.md:91` and `:92`, indexed at `:199` and
  `:200`; the receipt reports `mapped 126 / knowledge_files 126` and `resolved_rules 17 /
  rule_blocks 17` (depth proxy unchanged, `SCORECARD.md:24`).
- **Sources gated, not just listed.** S112 (unblob 26.6.4 SquashFS handler), S113 (BE v4 fixtures),
  S114 (Freetz AVM-BE note) admitted; S115 (7-Zip 26.04 refusal) rejected as an oracle; S116
  (unblob.org formats matrix) admitted through assimilation; S110's scope and used-by widened —
  rows at `corpus/SOURCES.md:116` and `:118-122`, decisions with quoted anchors at
  `corpus/lessons/round-38.md:28-34` (rows S112–S116 at `:28-32`, the S110 cell changes at `:34`).
- **Assimilation gated per entry.** From the read-only package `merge/kaidoku`: id collision check
  111 registry vs 132 staged → 6 collisions S106–S111
  (`.ufo/waves/round-38/assimilation/{reg-ids,staged-ids,collisions}`); `unblob-format-matrix`
  admitted (staged S122 → S116, staged S106 → S110 by document);
  `sasquatch-unblob-compatibility-precondition` and `sasquatch-unblob-avm-branch` refused with
  reasons (`corpus/lessons/round-38.md:36-66`); quarantine slice of 5 kaidoku rows hand-checked
  (`corpus/lessons/round-38.md:68-81`).
- **Wave 1 inherited and re-filed as evidence.** 40 seat reports plus 443 artifact files under
  `.ufo/waves/round-38/w1/`, committed at `3b960fe5`; the `w1.ready.dispatched` stamp closes R36-CL1
  (`corpus/lessons/round-38.md:92`).
- **Four mistakes mined with fixes shown able to fail.** M38-1 freeze amended after scoring
  (`corpus/lessons/round-38.md:17`), M38-2 degenerate control generator fixed after the freeze
  (`:18`), M38-3 stale "no external extractor dependency" premise (`:19`), M38-4 harness could not
  produce a receipt (`:20`). Criteria added: QUALITY 79 and 80 (`corpus/QUALITY.md:87-88`,
  `corpus/lessons/round-38.md:95-97`).

## Landed changes

Two commits, both recorded by the round's LOG entry `LOG.md:3126-3134` (attempt-1 history at
`:3128`; no tools installed or updated, `:3134`).

In `3b960fe5f9a7f1dfa22819f98dc0fa983f4260a8` — LOG `:3129` (C1), `:3130` (C2), `:3131` (sources),
`:3132` (assimilation), `:3133` (mistakes/criteria):

- `corpus/evidence/round-38/c1/K{1..4}/{before,after}.json` — the eight REA receipts the claim is
  scored on (before 0 files + `missing-extractor-dependency`; after 5/3/4/4 with K2's one
  `unpublished-entry` gap).
- `PROVINCE.md:44` — the Core `REA MCP server` row's pointer re-aimed from the non-resolving
  `evidence/doctor/` to the committed `.ufo/waves/round-19/evidence/doctor/` (same document).
- `PROVINCE.md:157` — round-38 parenthetical appended inside the Frontier *sasquatch* bullet: BE v4
  measured through `sasquatch-v4be`, not promoted, K2's in-tree symlink leaves a gap. The bullet is
  annotated, not moved; the frontier claim of the original predicate is therefore not satisfied.
- `corpus/knowledge/2026-10-26-r38-sasquatch-be-squashfs-recursion.md` — new entry, Frontier status,
  before/after arm table at `:16-17`, receipts at `:19-20`, symlink mechanism at `:33-42`, stop at
  `:44-48`.
- `corpus/knowledge/2026-10-26-unblob-format-matrix.md` — assimilated entry (97 handler sections, ten
  SquashFS variants incl. `SquashFS (v4-BE)`, "more than 30" vs "78+" count conflict disclosed). The
  `Vendor:` statistic is stated two ways and I re-opened neither read: at HEAD the entry's preamble
  called the staged "42 vendor-attributed entries" 42 occurrences of the word, not a per-handler
  count, and the uncommitted worktree revision keeps it as a per-section count (42 of 97 sections,
  one `unknown`); see Receipt note 8.
- `corpus/README.md:91-92` (coverage-map rows), `:199-200` (knowledge index rows), `:239` (Frontier
  line for `sasquatch-v4be`).
- `corpus/SOURCES.md:116` (S110 scope + used-by widened), `:118-122` (S112, S113, S114, S115-rejected,
  S116).
- `corpus/QUALITY.md:87-88` — criteria 79 (first-freeze bytes are the rule; `freeze-drift.py` must
  print zero commits before a score is cited) and 80 (controls live inside the freeze).
- `tools/round-38/freeze-drift.py` plus its three receipts under `.ufo/waves/round-38/l1/` (drift,
  drift, clean).
- `.ufo/waves/round-38/w1/` — the inherited wave-1 evidence (40 reports, 443 artifact files) and the
  `w1.ready.dispatched` stamp; assimilation id lists under `.ufo/waves/round-38/assimilation/`.

In `0fc6113376a156fddc3ec385386d71c3a4a9f690` — LOG `:3129` (scores), `:3130` (C2 receipt),
`:3133` (lesson/criteria):

- `SCORECARD.md:23` — coverage row re-stated 124/124 → 126/126 with both new entries named; depth
  `:24` and calibration `:25` left at their measured values.
- `SCORECARD.md:3399-3411` — the `## Round 38` section: base/freeze/controls line, the two-claim
  table (`:3405-3406`), owned scores (`:3408`), planned round 39 and "retired: none" (`:3410-3411`).
- `LOG.md:3126-3134` — the round-38 entry.
- `corpus/lessons/round-38.md` — mistakes M38-1..M38-4 (`:17-20`), sources Gate (`:22-34`),
  assimilation (`:36-66`), quarantine slice (`:68-81`), routed defects (`:83-93`), criteria added
  (`:95-97`).
- `corpus/README.md:229` — lessons-index row for `round-38`.
- `.ufo/waves/round-38/l1/scores/c1-v1-at-3b960fe5.json` (the rule) and
  `c1-v3-at-3b960fe5-NOT-THE-RULE.json` (information only; 4/4 under `f1010f67`), both committed.

## Before → after measurements

Both commands are the counters frozen at `e059ca93` (C1 counter sha256 `a7a62b09…16db8`; C2 counter
sha256 `7f137b66…7b0f7`, unchanged from the freeze to HEAD — `git log e059ca93..HEAD --
tools/round-38/c2-counter.py` is empty). Both counters exit 0 only when `met_target`
(`c1-counter.py:268`, `c2-counter.py:264`); exits below are [INFERENCE] where the receipt stores no
exit field.

| claim | counting command | before (revision) | after (revision) | verdict |
|---|---|---|---|---|
| R38-C1 coverage | `python3 -I -B <c1-counter.py @ e059ca93, sha256 a7a62b09…> --root <lane> --rev <REV> --freeze e059ca9391642d5b71b6662cabcbdce0d9308719 --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents --json-out <RECEIPT>` | `carriers_matched 0`, exit 1 — no claim bytes (`.ufo/waves/round-38/controls/ctl-c1-0-do-nothing.json`, `output.carriers_matched 0`) | `carriers_matched 3`, `met_target false`, exit 1 [INFERENCE]; Core bindings false, entry/sources/map/frontier bindings true (`.ufo/waves/round-38/l1/scores/c1-v1-at-3b960fe5.json`) at `3b960fe5f9a7f1dfa22819f98dc0fa983f4260a8` | **honest stop** — target 4 not met (K2 `unpublished-entry`); BE v4 stays Frontier |
| R38-C2 calibration | `python3 -I -B tools/round-38/c2-counter.py --root <lane> --rev <REV> --base 77091b492cc53f8743bd0701b1e7d5e66123dd84 --json-out <RECEIPT>` | `mismatches 1`, `guards_ok false`, exit 1, `unresolved [["prov_core:REA MCP server", "evidence/doctor/"]]` at `77091b49` (`.ufo/waves/round-38/controls/ctl-c2-0-do-nothing.json`) | `mismatches 0`, `guards_ok true`, `met_target true`, exit 0 [INFERENCE]; `pointers 52` vs `base_pointers 48`; 7 assertions, `assertion_mismatches []`; command A `126/126` mapped and `17/17` rule blocks; command B `[9, 9]`; craft `[81, 314]`, adjacent `[97, 125]` at `0fc6113376a156fddc3ec385386d71c3a4a9f690` | **met by counter** — 1 → 0 mismatch on the repaired pointer |

Axis scores (`SCORECARD.md:3408`): coverage 10 → 10 (map proxy 124/124 → 126/126; no domain surface
moved because C1 stopped), depth 10 → 10 (17/17), calibration 10 → 10 (the move is the 1 → 0
mismatch count). No capability row entered.

## Receipt notes for the integrator (must not be papered over)

These are verified against committed bytes; none of them changes either claim's verdict, but four
of them contradict text the report would otherwise repeat.

1. **The C2 "after" receipt cited by the scored surfaces does not exist.** `SCORECARD.md:3406` and
   `corpus/lessons/round-38.md:11` both cite `.ufo/waves/round-38/l1/scores/c2-final.json`;
   `git cat-file -e HEAD:.ufo/waves/round-38/l1/scores/c2-final.json` fails (exit 128) and no such
   path exists in the worktree or in `0fc61133`. The receipt that was actually produced is
   `.ufo/waves/round-38/l1/scores/c2-at-0fc61133.json`, untracked (`git status --porcelain`).
   `LOG.md:3130` says only "Final receipt in `.ufo/waves/round-38/l1/scores/`". So R37-CL1's claim
   that "every receipt this round cites is committed" (`corpus/lessons/round-38.md:85-87`) is not
   true for C2 as filed — either commit the receipt and rename the citation, or report the
   measurement as uncommitted.
2. **The C1 "before" receipt is not a first-freeze run.** `SCORECARD.md:3405` cites
   `.ufo/waves/round-38/controls/ctl-c1-0-do-nothing.json` as `carriers_matched 0`, "exit 1 at the
   freeze", but that receipt's own `argv` records `--rev f1010f677a53ecf0e671952ce1bf4f44d51e151b
   --freeze f1010f677a53ecf0e671952ce1bf4f44d51e151b` — the third freeze, not `e059ca93`. The value
   is not in doubt (the arm holds no receipts and no entry, so no carrier can match), but the
   sentence "at the freeze" is not what the receipt shows.
3. **The `frontier_note` binding is satisfied before the round.** The clause is
   `'big-endian' in line and 'superseded' in line` over PROVINCE (`c1-counter.py:208-209` at
   `e059ca93`), and `PROVINCE.md:157` already contained both words at base `77091b49`; the frozen
   control receipt shows `frontier_note true` while `entry_present false` and all bindings empty
   (`controls/ctl-c1-0-do-nothing.json`). The counter's green here is inherited, as wave-1
   `w1/R38CriticClaimsC1.md` §4 states. It does not affect the stop, which the carrier count and the
   two Core bindings already force.
4. **`PROVINCE.md:372` still calls `sasquatch-v4be` "unmeasured"** — byte-identical at base and HEAD
   — while the landed entry, `corpus/README.md:239` and four before/after receipts measure it. The C2
   counter cannot see this: it resolves pointers and counts, not prose. A reader of the Core
   `sasquatch squashfs recursion` row is told the opposite of what the corpus now holds.
5. **The predicate's premise sentence is contradicted by its own receipts.** The frozen predicate
   says the after-receipt was "run with stock unblob 26.6.4; no external extractor dependency"
   (`c1-counter.py:5-7` at `e059ca93`), while the committed before arm stops on
   `missing-extractor-dependency` [`sasquatch-v4be`] and the after arm publishes only with that
   binary reachable (M38-3, `corpus/lessons/round-38.md:19`). The counter scores the receipt, not
   the premise, so C1's stop stands; the premise sentence as frozen is false.
6. **The L1 C1 receipt names a scratch counter, not a lane path**
   (`"argv": ["/fast/scratch/hyaku/kaidoku-r38/l1/c1-counter-v1.py", …]`) and stores no digest. The
   identity rests on `SCORECARD.md:3405`'s `a7a62b09…`, which does equal the frozen blob
   (`git show e059ca93:tools/round-38/c1-counter.py | sha256sum`); whether the scratch copy held
   exactly those bytes is not recoverable from committed bytes.
7. **No end census in committed bytes.** `corpus/lessons/round-38.md:66` promises the end census "in
   the report"; only `.ufo/waves/round-38/census-start.txt` exists in the round directory. The
   integrator must either produce and commit the end census or drop the promise.

8. **The worktree and HEAD disagree on one landed statistic.** `git status --porcelain` at drafting
   time showed three tracked corpus files modified after HEAD — `corpus/lessons/round-38.md`,
   `corpus/knowledge/2026-10-26-r38-sasquatch-be-squashfs-recursion.md`,
   `corpus/knowledge/2026-10-26-unblob-format-matrix.md` (`git diff --stat HEAD`: 17 insertions, 13
   deletions) — by another seat. Two consequences for filing:
   - the `Vendor:` count in the assimilated entry is "42 occurrences of the word, not a per-handler
     count" at HEAD and "42 of 97 sections carry one `Vendor:` field, one of them `unknown`" in the
     worktree; both readings are live in the lane, and neither was re-opened by this seat;
   - the worktree lesson cites an `M38-5` in prose (unblob-format-matrix count correction) while the
     mistakes table has four rows at both revisions (`grep -c '^| M38-'` → 4), so a mistake id is
     referenced without a row.
   Committing the edit before the report is filed resolves both; otherwise the report must not cite
   the amended counting statement. Line numbers in this draft are HEAD's and shift with that commit.
