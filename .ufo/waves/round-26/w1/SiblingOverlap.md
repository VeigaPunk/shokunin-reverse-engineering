# SiblingOverlap — kaidoku round 26, wave 1

Seat: KaidokuR26.SiblingOverlap (connector, leaf). Window 2026-10-22T12:11:41Z to 12:17:36Z UTC.
Target: sibling-lane overlap with R26-C1 (REA evidence-id identity, rea-agents 6.5.0, carrier /usr/bin/jq) and R26-C2 (SCORECARD `## Owned axes` rows and the SHONEN no-cross-domain-bleed line).
Scope read: committed HEAD of 20 sibling lanes under /home/vgpnk/Projects/shokunin/*-shokunin (kaidoku excluded), their working trees for the tightest patterns, and fleet MANIFEST.json (sha256 94ec978ef6141f8be51f7c10e15cc2d1f112c232568f797b561420437daca24b, 13,300 lines, last commit 3b549bee).
Bounds kept: read-only everywhere. No REA run, no jj, no Git writes, no sibling messages. No tools installed or updated.

## Verdict

- R26-C1: no sibling lane holds evidence-id identity work for the eight native reader verbs, at 6.5.0, on /usr/bin/jq, at 0x103fa0, or with the alternate carrier. Two sibling surfaces state the identity rule that R26-C1's copy run tests, and both state it more broadly than kaidoku's current rule. Overlap kind: same claim, older wording. No sibling owns the result.
- R26-C2: no sibling reads or scores kaidoku's `## Owned axes` rows, the K1 to K6 items, or C1Cherrypick. Sibling line pointers into kaidoku SCORECARD.md sit below the edited section, so they drift if C2 changes that section's line count.
- MANIFEST: no admitted sibling round cites evidence-id identity, rea-agents 6.5.0 native verbs, or this carrier. Every admitted row naming these terms is a kaidoku row.

## Search commands (all exit 0 unless stated)

1. `bash /fast/scratch/hyaku/kaidoku-r26/seats/SiblingOverlap/search.sh`, run 12:13:13Z to 12:13:51Z. Per lane and pattern it runs `git -C <lane> grep -n -I -E -e <p> HEAD -- . ':(exclude)**/sandboxes/**' ':(exclude)**/node_modules/**'`. There are 16 patterns, including the full carrier sha256 and its 12-hex prefix, `/usr/bin/jq`, `kaidoku-r26`, `0x103fa0`, `rea-agents@6\.5\.0`, `ev_[0-9a-f]{64}`, `content-keyed`, `path-sensitive` and `R26-C[12]`. Zero hits for the full carrier sha256, `kaidoku-r26`, `R26-C1` and `R26-C2` in every lane (observation). `0x103fa0` hits only in tsukuroi's round-19 `l1-capture` copies of kaidoku's own PROVINCE.md (observation).
2. Working-tree `rg` excluding .git, .jj, sandboxes, node_modules and l1-capture, for the full carrier sha256, `kaidoku-r26`, `0x103fa0`, `R26-C[12]`, `c1-id-identity`, `c2-calibration.py` and `native-reader-evidence-id`, at 12:14:55Z: exit 1, no match (observation). `git diff HEAD --name-only` shows 0 changed tracked files in revenger, tameshi, tsukuroi, mori and kotoba at 12:17:11Z (observation).
3. C2 sweep, 12:15:15Z: `git grep` over HEAD for `C1Cherrypick`, `## Owned axes`, `Queue-drain craft`, `rule_blocks` and `citation_resolved_rules` gives zero sibling hits (observation). `No cross-domain bleed` hits most lanes. It is the fleet SHONEN template line, scored by each lane on its own repo, so it is not overlap (inference).
4. MANIFEST walk, 12:14:25Z: a Python scan of `rounds[]` for evidence id, rea-agents, /usr/bin/jq, path-sensitive, content-keyed and family-scoped (results below).

A first tree-wide `rg -c` pass (12:11:53Z) was swamped by kagi's nested sandbox clones under `.ufo/waves/round-28/sandboxes`. Command 1 replaced it for the findings. When it finished at 12:17:59Z, it agreed on the points that matter: across all working trees, sandboxes included, the full carrier sha256 and `kaidoku-r26` gave exit 1 (no match), and `0x103fa0` and `inspect-binary-layout` hit only the tsukuroi `l1-capture` copies of kaidoku's PROVINCE.md (observation).

## Overlaps with path:line

| # | Sibling path:line (HEAD) | What it says | Kind | Bears on |
|---|---|---|---|---|
| O1 | tameshi-shokunin/corpus/knowledge/verification-patterns-fleet.md:35 | "identity claim strength = the id's full domain `f(content, path, params)` (kaidoku-shokunin/corpus/QUALITY.md:24 ...)" and "one r9-02 observation ... flagged unresolved, U4" | same claim, cites kaidoku's superseded rule 14 | C1 |
| O2 | same file :34 | "re-runs re-mint ids exactly (`ev_f4e02f93…` ...)": this is the 6.4.0 `analyze` on cli-arm64.exe (kaidoku corpus/knowledge/2026-10-13-r4-12-godot-arm64-scale.md:111) | same-path repeat claim, other carrier and pin | C1 |
| O3 | revenger-shokunin/LOG.md:720; SCORECARD.md:160; reports/round-1/scribe.md:267 | "`evidence_id` is path-sensitive (same bytes elsewhere → `ev_50038b96…`) — `ev = f(content, path, params)`" | same claim, universal wording, PE verb `inspect-pe-resources` | C1 |
| O4 | revenger-shokunin/SCORECARD.md:142-144 | "holds only for this lane's `inspect-pe-resources` family. It is not a universal rule (fleet `MANIFEST.json:2782` ...)" | correction already in place; agrees with kaidoku rule 15 | C1 |
| O5 | revenger-shokunin/.ufo/waves/kaika-r1/connector.md:19,83-97,130 | "Evidence-ID Identity: Universal vs. Family-scoped ... same claim / contradiction ... defer / cite correction" | earlier connector scan of this exact contradiction | C1 |
| O6 | mori-shokunin/.ufo/waves/round-14/build/JournalSentinel.md:218 | "`/usr/bin/jq` (`root`, 30 800 B, sha256 `e815667571d0…f7806`) ... `jq-1.8.2`" | same carrier bytes, a tool-resolution fact, no REA | C1 carrier only |
| O7 | tameshi-shokunin/corpus/knowledge/verification-patterns-fleet.md:34,44 | live pointers `kaidoku-shokunin/SCORECARD.md:37` and `:73-81` | pointer into SCORECARD below `## Owned axes` | C2 |
| O8 | kotoba-shokunin/.ufo/round-21/scouts/C2.md:83,127; round-22/scouts/C2.md:31-34; round-23/scouts/C2.md:33-34,112; round-24/scouts/C3.md:37-39,75; round-26/scouts/C2.md:33 | pointers `kaidoku-shokunin/SCORECARD.md:617,628,631,633,634,638,1272` | seat-report pointers below `## Owned axes` | C2 |

Pointer checks against kaidoku base a0639d8e (`git show a0639d8e…:SCORECARD.md | sed -n …`, 12:15:43Z; observation):
- `## Owned axes` runs from line 19 to line 32, and `## Reconciled current state` starts at line 33.
- Kotoba's anchors hold at base: :628 "Saturation line: 10.0 …", :631 "Stagnation window N: 10 …", :634 "window resets from here.", :638 "the first round of the reset", :1272 "Round 10 of the reset window".
- Tameshi's two anchors are already stale. :37 reads "They are assessment obligations, not nine independent domain discoveries.", and :73-81 is "Fleet-only history" / "Historical scope bleed" text, not "audit VERIFIED ×2".

Benign hits, not overlap (observation from command 1 output, saved in out/):
- kumitate: 6.5.0 appears only in dispatch prompt boilerplate, and `.ufo/waves/round-36/build/ConnectorOutOfProvince.md:18` says round 36 has zero REA work items.
- kotoba `.ufo/waves/round-47/build/C1OpencodeProvenance.md:33` labels the 6.5.0 npx root "unrelated".
- tabi `.ufo/waves/round-16/w1/ConnMcpAdjacency.md:35` reads 6.5.0 browser tool contracts, not native readers.
- kagi `.ufo/round-20/pane-attestation.json:43` records a 6.5.0 MCP process.
- revenger's 6.5.0 hits are MCP-registration freshness rows (`corpus/knowledge/seed.md:62`).
- game-dev-3d's evidence ids are 6.4.0 zip-carrier envelopes (`corpus/artifacts/zip-r10/rea-positive.json:1`).
- mori, souji, kengaku and mado use `/usr/bin/jq` as a shell tool. kasegi, kotodama and souji use `evidence_id` in unrelated schemas.

## MANIFEST.json rows (path:line)

- Admitted rows that cite these terms are all kaidoku closures (`rounds[]` indices 280, 290, 292, 294, 358, 370, 424). Example: MANIFEST.json:5072 "ev_ Evidence-ID formula CLOSED ... 8/8 envelopes recomputed". The kaidoku train row MANIFEST.json:2782 reads "family-scoped evidence-id identity. Removed the false universal 'evidence ids are f(content, path, params)'" (observation).
- Sibling rows that hit a term are unrelated (observation):
  - MANIFEST.json:2444 (mori round 5 closure, "content-keyed forgery"), not evidence ids.
  - MANIFEST.json:4262 (kotodama round 33, admitted, "SKILL.md content-keyed re-key"), a filename keying.
  - MANIFEST.json:10533 (mori round 20, rejected-harmed), `/usr/bin/jq` as a counting tool.
- Revenger round 1 (MANIFEST.json:5604, admitted, commit `revenger-shokunin@cf0241927`): the notes do not cite evidence ids. However, `git merge-base --is-ancestor 35b2e8b cf0241927` gives rc 0, and 35b2e8b is the last commit of the O5 connector. So the admitted round carries O3 to O5 without the manifest citing them (observation).
- Tameshi O1, O2 and O7 were last committed in 58e5d53 ("round-18: build landing …"). Whether tameshi's admitted round 18 row covers that commit is unknown, because it was not checked.

## Contested scope to name

- C1 domain wording (contested, live). Kaidoku corpus/QUALITY.md at base has two rows. Rule 14 at :24 says "Evidence-id identity claims state the id's full domain: `f(content, path, params)`". Rule 15 at :25 supersedes it: "never a universal formula ... `analyze`/`inspect` and `analyze_function` ids are content+params-keyed".
  - Tameshi O1 still cites rule 14 as current and leaves r9-02 as open U4.
  - Revenger O3 keeps the universal wording in LOG and in the SCORECARD planned line, and is corrected only at SCORECARD.md:142-144.
  - R26-C1's copy run gives a per-verb verdict (content-keyed or path-sensitive) for analyze and inspect at 6.5.0 on jq. That either settles or contradicts tameshi's U4 for those two verbs (inference). Kaidoku must not edit tameshi or revenger. This is an adjacency note for the L1 or integrator to route.
- Ownership (contested, unresolved, not this round's to settle). tsukuroi-shokunin/PROVINCE.md:51 lists ADJ-06 with "protocol integrator — kaidoku/revenger ownership unresolved", and :128-129 name both PROVINCE files (OUT-008, OUT-009). R26-C1 stays inside kaidoku's declared native-ELF reader surface, while revenger's evidence-id work is PE `inspect-pe-resources` (O3, O4). So no shared verb was observed.
- C2: no contest. Sibling lanes score their own SHONEN line; nobody claims kaidoku's.

## Proposed move (one, bounded)

Land the C2 SCORECARD repair as in-place cell edits that keep `## Owned axes` at exactly lines 19 to 32, so `## Reconciled current state` stays at line 33.
- Evidence: O7 and O8 hold seven sibling line pointers below line 32. The five kotoba anchors verified above hold at base, and any added or removed line inside 19 to 32 shifts all of them.
- Affected axes: calibration improves, because C2 lands without creating new sibling-pointer drift. Depth and coverage are unchanged, and the K1 to K6 rules and the C1 coupling to K4 are untouched, because each row stays one table line.
- Risk: the depth or coverage evidence cell may need more text. A table row is one line anyway, so the cost is only a longer line. If the L1 inserts any new line or section above line 1272, the kotoba anchors shift regardless (inference).
- Verification: `git show <REV>:SCORECARD.md | grep -n '^## Reconciled current state'` must give `33:`, and `git show <REV>:SCORECARD.md | sed -n '628p;631p;634p;638p;1272p'` must equal the same command on a0639d8e.
- Not proposed: any edit to tameshi or revenger, or repairing tameshi's two pointers that were already stale. Those are sibling-owned.

## Artifacts (/fast/scratch/hyaku/kaidoku-r26/seats/SiblingOverlap/)

| file | sha256 |
|---|---|
| search.sh | e8b12749c17df5fc42eb0816f804708c729e1d274eada6994f573f1ed27cc890 |
| search-summary.txt (per lane and pattern hit counts, HEAD shas) | 733b5e7b3ba62a3e68383c6edc579f0fac32ed0bcc28e37928fab54943fc0d1c |
| search-counts.txt (noisy first pass, completed 12:17:59Z, 1,513 lines) | 121161e8fe709bbd0581e9540fe4f27bd400084816ee3a85b859968e8b2b2c66 |
| out.tar (320 raw git-grep outputs, out/<lane>.p<N>.txt) | 556ee563fec420bce0f6f1920bb40223fd50025e5edf2b48acd4d93f3acb30ff |
