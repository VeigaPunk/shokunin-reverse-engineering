# KaidokuR32A2.A2Capability13 — C2 statement round-13 source registry: independent evidence re-open

- Seat: `KaidokuR32A2.A2Capability13` (UFO-FSD reviewer, leaf; no subagent dispatch).
- UTC start: `2026-10-23T06:46:18Z`; UTC evidence close: `2026-10-23T06:52:28Z`.
- Assignment: for C2 v3 statement key 13 (round-13 source registry), independently open MANIFEST at fleet
  `cef00867ab3279ac2c2d10421e3e62c0e5d693f3` and matching append-only SCORECARD records at base
  `283aad7fe56d82f4ed4f8e43f099c2e1ceed5525`; re-open every frozen anchor path (`claims-v3.json`
  `anchors_at_freeze["13"]` = `corpus/SOURCES.md`, `corpus/lessons/round-13.md`); locate evidence
  demonstrating capability (not file existence alone); draft the faithfully copied summary row only if
  evidence exists; no summary repair run, no lane edit; state semantic vs lexical overlap limits.

## Sandbox and materialized artifacts (all unique scratch)

Scratch: `/fast/scratch/hyaku/kaidoku-r32/a2audit/A2Capability13` (1 MiB write bound respected; no
installation performed — no tool install was needed).
- Lane clone: `lane.git` (full `git clone --no-checkout` of `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`);
  clone HEAD (rev-parse) = `f382e3b7978e6091a19ca93277c15a75c0016b43` (freeze commit).
- Fleet clone: `fleet.git` (full `git clone --no-checkout` of the fleet colocated git dir
  `/home/vgpnk/Projects/shokunin/.git`, as resolved by jj `store/git_target` = `../../../.git`);
  clone HEAD = `575bcedac44943fae1cd43f9030aea7662ddb6be`.
- All git reads ran inside these clones with `-C <abs>` and `GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE`
  unset; no git/jj write anywhere; no lane/fleet file touched.
- Commits verified present in clones: fleet pin `cef00867ab3279ac2c2d10421e3e62c0e5d693f3`; base
  `283aad7fe56d82f4ed4f8e43f099c2e1ceed5525`; freeze `f382e3b7978e6091a19ca93277c15a75c0016b43`.
- Materialized file hashes (full sha256 of committed blobs via `git show <rev>:<path>`):

| file (scratch) | rev | bytes | sha256 | git blob |
|---|---|---|---|---|
| manifest-fleet.json | cef00867 MANIFEST.json | 1242275 | `2e089615936dae60d1b4ab3883dbbc8ed7608018b9c7f4694209207d84b3207f` | e6fc0394f5d5 |
| scorecard-283aad7f.md | 283aad7f SCORECARD.md | 274232 | `bba9f55de85001d6259ed728bdec82a20dd49830ccb9e01634909bb14c9c38e3` | e90a5a0157ed |
| scorecard-f382e3b7.md | f382e3b7 SCORECARD.md | 274232 | identical to base (same blob e90a5a0157ed) | e90a5a0157ed |
| SOURCES-f382e3b7.md | f382e3b7 corpus/SOURCES.md | 114182 | `4bf494f8c38b6bfb44980f5b3f493063fc08d50aad8ce9f867907a57654e3970` | e9e8ff2875fb |
| SOURCES-283aad7f.md | 283aad7f corpus/SOURCES.md | 114182 | identical to freeze (same blob e9e8ff2875fb) | e9e8ff2875fb |
| lessons-round-13-f382e3b7.md | f382e3b7 corpus/lessons/round-13.md | 11412 | `b2ae45a87e574a25a0ba1505014b9909d3b3dd1a3741db01e20a9a260994ffb3` | b588e4ef3617 |
| lessons-round-13-283aad7f.md | 283aad7f corpus/lessons/round-13.md | 11412 | identical to freeze (same blob b588e4ef3617) | b588e4ef3617 |
| c2-capability-calibration-v3.py | f382e3b7 tools/round-32/c2-capability-calibration-v3.py | 15665 | `5955e8ace76d93c7891a43ca282f129c8874cd1878a05c9f29e0b81d3cab2f9f` (matches instrument pin in claims-v3.json) | d450cb9fa013 |

Anchor paths are identical at base and freeze (same blobs): no drift between the base that the counter
reads and the freeze that pins the anchors.

## 1. MANIFEST open at fleet cef00867 (exercised)

`git -C fleet.git show cef00867:MANIFEST.json` → parsed (rounds list, 515 entries). Round-13 kaidoku
**closure** entry (type=closure, admitted=true, verdict=`admitted-capability-only`, commit
`767adafb97e2eef6980e2ad873d357e16721c467`):

- `capabilities_added[0]` = `"source-curation registry (22 opened rows, scoped tiers, ordered study paths, reasoned rejection; no domain-operation claim)"` — verbatim item (quote ≤25 words: the item is 20 words).
- `verification.reviewer` = `"KaidokuR13Review (all22 rows reopened, admit/reject agree; 2 citation errata appended)"`; `critic` = `"KaidokuR13Critic (expansion objection accepted)"`; `parent_smoke` = `"integrated sources census validate exit0 after3b5fea8"`.
- `notes` (excerpt): "No newknowledgeentry, noARM64X/targetexecution, no promotion. S017splice/S018location corrected append-only; WAF fetch limitdisclosed."

The statement set at the pin: 4 kaidoku `capabilities_added` items (rounds 13, 14, 17, 27) — matches
`statements=4` frozen target.

## 2. SCORECARD at base 283aad7f (exercised)

- `## Capabilities` section (`:615-624`): 5 rows at `:619-623` (luna-round-6, luna-round-8, arc2-loop1-round2, arc2-loop1-round7, round 27). The only outside-recorded capability credited there is round 27 (`tools/round-27/xpin-attribute.mjs`). Rounds 13/14/17 are absent from the section.
- The earlier observation the claim cites exists at `:3116`: section holds 4 rows (at that writing) vs 7 capability rows card-wide `:619,:620,:621,:622,:2135,:2207,:2374`; "a reader of `## Capabilities` alone undercounts by 3".
- Append-only capability table for round 13 at `:2134-2136`:

```
| Capability | What it can now do | Evidence pointer | First-working round |
| curated source registry for existing REA frontier | Keeps opened, scoped study sources, ordered paths, recheck cadences, an auditable bounded search, and a source rejection with evidence and flip; source text is not held-capability evidence | `corpus/SOURCES.md`; `corpus/lessons/round-13.md`; `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --today 2026-10-19 --root /home/vgpnk/Projects/shokunin/.tower/worktrees/kaika/kaidoku-shokunin /home/vgpnk/Projects/shokunin/.tower/worktrees/kaika/kaidoku-shokunin` | arc3-loop1-round13 |
```

- This is the only table row card-wide whose first cell matches key pattern `/source(-curation)? registry/` (case-insensitive; verified by scan over all `|`-rows of the base card).

## 3. Frozen anchors re-opened (exercised; evidence of capability, not existence)

### 3a. `corpus/SOURCES.md` (f382e3b7 / 283aad7f, same blob e9e8ff2875fb)

- `## Registry` table (11-column Contract v1 header) rows S001–S022 opened **2026-10-19** with tier/scope/anchor/teaches/status/opened/recheck/used-by columns; S022 is the reasoned rejection (`status=rejected`):
  - Quote (≤25 words, verbatim, at S022 row): "REJECTED: its own page requires browser upload and states Electron 17–38 coverage" — followed by reason and flip condition ("flip: reconsider if a verifiable local/no-upload workflow and reproducible evaluation cover Electron 42/V8 14.8").
- `## Paths`: four ordered study paths (REA route; Go ≥1.26 recovery; arm64X/Linux Mach-O route; etc.) plus per-path scope notes ("These sources do not establish a Go 1.26 recovery run…").
- `## Search log`: 2026-10-19 entry records query, first-10-results boundary, 5 deduplicated screened, 1 included (S008), 4 excluded with reasons, stop rationale — the "auditable bounded search" evidence.

### 3b. `corpus/lessons/round-13.md` (same blob b588e4ef3617)

- Gate: census before/after (verbatim, :20): "SOURCES rows: **0 → 22** — … (2026-10-19). Before: the script reported the registry missing and `FLEET.rows 0` (exit 1). After: rows 22, tiers A=20/B=1/C=1, statuses mined=21/rejected=1, invalid tiers/statuses=0 and missing registries=0 (exit 0). No older row was edited or superseded."
- "Freshly opened sources" table (S001–S022): every row an excerpt ≤25 words quoted with exact source location (e.g. S003: `` `SUPPORTED_VERSIONS = GoVerRange.parse("1.15-1.25");` — `GoRttiMapper.java:79` ``).
- Decision and limits (:53, verbatim ≤25 words): "The rejected source is not presented as evidence for a lane finding."
- Non-author re-open recorded: `KaidokuR13Review` re-opened S003/S008 and the S022 rejection and agreed; caught two quote-fidelity defects (S017 quote splice, S018 location), corrected append-only in the same file (lines 61-76).
- Explicit scope: "No `corpus/knowledge/` file, `corpus/README.md`, PROVINCE frontier, or numeric axis score changed… No ARM64X sample was sought or required; no target binary or artifact was executed, and no live REA provider/session was probed."

### 3c. Anchor resolution and match conditions (exercised)

Counter logic (c2-capability-calibration-v3.py, verified sha256 = instrument pin) `anchors_for` for
round 13 = rel_paths(MANIFEST item) ∪ rel_paths(evidence cell of every base row matching the key,
ticked). Item has no relative paths; the matching row's ticked relative evidence paths are exactly
`corpus/SOURCES.md`, `corpus/lessons/round-13.md`; both exist in the base tree (`git cat-file -e
283aad7f:<path>` exit 0) and in the freeze tree (`git cat-file -e f382e3b7:<path>` exit 0).

Manual predicate check for key 13 (all hold):
- first cell matches key pattern only (one key, no multi-key overlap);
- last cell `arc3-loop1-round13` → `round[- ]?(\d+)(?!\d)` names exactly round 13;
- evidence cell names both resolving anchor paths;
- what-it-can-do cell shares 6 words with the anchored description (`{opened, ordered, paths, rejection, scoped, study}` ≥ 5): `{opened, ordered, paths, rejection, scoped, study}` — lexical overlap test passes.

Frozen counter exercised at rev=base in the scratch clones (exact argv, exit 1, full stdout):

```
argv=["python3","-I","-B","/fast/scratch/hyaku/kaidoku-r32/a2audit/A2Capability13/c2-capability-calibration-v3.py","--root","/fast/scratch/hyaku/kaidoku-r32/a2audit/A2Capability13/lane.git","--rev","283aad7fe56d82f4ed4f8e43f099c2e1ceed5525","--fleet","/fast/scratch/hyaku/kaidoku-r32/a2audit/A2Capability13/fleet.git"]
round-13	P2-mismatch	no `## Capabilities` row matches /source(-curation)? registry/ naming round 13
round-14	P2-mismatch	no `## Capabilities` row matches /quote.{0,40}regression audit/ naming round 14
round-17	P2-mismatch	no `## Capabilities` row matches /Ghidra-session log capture/ naming round 17
round-27	P2-match	row 5 anchor evidence tools/round-27/xpin-attribute.mjs; description words 16
statements=4 match=1 target=4 reverse_mismatch=0
exit=1
```

This matches the claim's `unmoved_command` observation (statements=4 match=1, exit 1): round-13's
mismatch is only the missing `## Capabilities` row; every other frozen condition for statement 13
(anchors, evidence paths, round naming, description overlap) already holds at base.

## 4. Drafted summary row (evidence exists; faithful copy, no lane edit performed)

Evidence for the capability exists (registry content, census, opened quotes with locations, reasoned
rejection with flip, bounded search log, non-author re-open — 3a/3b). Drafted `## Capabilities` row,
copied from the MANIFEST item name and the already-landed append-only row, as the repair-pending row:

```
| Capability | What it can now do | Evidence pointer | First-working round |
| source-curation registry (22 opened rows, scoped tiers, ordered study paths, reasoned rejection; no domain-operation claim) | Keeps opened, scoped study sources, ordered paths, recheck cadences, an auditable bounded search, and a source rejection with evidence and flip; source text is not held-capability evidence | `corpus/SOURCES.md`; `corpus/lessons/round-13.md` | arc3-loop1-round13 |
```

- Name: verbatim MANIFEST `capabilities_added[0]` (matches key pattern `/source(-curation)? registry/`).
- Description: verbatim current append-only row's what-it-can-do cell (shares 6 words with the anchored description — the predicate's lexical check).
- Evidence: the two frozen anchor paths (also the only resolving relative paths the counter requires).
- First-working round: `arc3-loop1-round13` (MANIFEST round 13; counter regex resolves to exactly 13).
- No summary repair run was executed; no lane file was edited; this row is a draft for L1's later repair.

## 5. Semantic vs lexical overlap limits

- The predicate's description check is **lexical**: a ≥5 shared-word overlap (case-insensitive word tokens, 4+ letters) between the row's what-it-can-do cell and the anchored description. A row that copies the anchored description passes by construction — the v3 limit text says exactly this ("a row that copies the anchored description passes (that copy is the claimed repair)"). It does not verify that the described behavior is real.
- This seat's re-open adds **semantic** evidence: the anchors' content demonstrates the capability substance (registry rows with scope/anchor/teaches structure; census 0→22 with exit 0; opened quotes with exact locations; rejection with reason and flip; search log with bounded stop; non-author re-open agreement). The row's description words overlapping the manifest item are the content words of that demonstrated capability (opened/scoped/ordered/paths/rejection/study).
- Residual limits (honest bounds):
  - The lexical test cannot distinguish truthful from fabricated description overlap; semantic confidence here rests on the anchor contents, not on the word overlap.
  - The anchors show the *curation records*; they do not by themselves re-prove that every cited URL fetched or that the census output was produced honestly (that rests on the lesson's Gate, the cited command, and the parent smoke `sources census validate exit0 after 3b5fea8`; none were re-executed by this seat).
  - The `## Capabilities` section at base still undercounts (rounds 13/14/17 absent) — the exact gap the claim targets; this seat only drafts, and does not repair.
  - Statement bound: C2 v3 covers the 4 hyaku-numbered kaidoku rounds; luna/arc rows in the section are outside the statement set (as the claim's limits state).

## 6. Findings by severity

1. **[KEY-13 evidence confirmed]** The round-13 source-registry capability has demonstrating evidence at the frozen anchors (`corpus/SOURCES.md`, `corpus/lessons/round-13.md`, identical at base and freeze), and every C2 v3 condition for statement 13 except the missing `## Capabilities` row holds at base. The drafted row in §4 is faithful and evidence-backed.
2. **[No defect found]** No discrepancy observed between the claim's frozen text (anchors, key pattern, match semantics, unmoved_command outcome) and the opened sources. Counter run at base reproduces the documented `match=1, exit 1`.
3. **[Lexical-check limit (known, per claim limits)]** The ≥5-word overlap check is lexical; semantic demonstration is provided by the anchor re-open, not by the check itself (see §5).

## Verification gaps

- The census command `sources-census.sh validate …` and the anchor URLs were not re-executed/fetched (out of scope for this seat; frozen evidence read-only).
- The lane `## Capabilities` section was not edited (repair belongs to L1 after controls land).
- Clone heads recorded above are the sandbox state; lane/fleet production trees were not mutated.

## Trailer

- Report path (relative to lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`): `.ufo/waves/round-32/a2audit/A2Capability13.md`
- Scratch: `/fast/scratch/hyaku/kaidoku-r32/a2audit/A2Capability13`
- UTC close: `2026-10-23T06:52:28Z`
