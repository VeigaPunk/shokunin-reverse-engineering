# Round 90 — the interior later-block `b_info.sz_cpr` class, craft rule block 30, and the round-89 closure's routed defects

Lane `kaidoku-shokunin`, round 90, attempt 1 on this host (three earlier attempts of the same round died
on provider failure at 22:12/22:31/22:32 -03:00 and left the declaration, its receipts and the wave spec
in the tree; they were re-verified here, not re-declared). Base `fc52cc9dc`; declaration
`18b21f092429383d498572a422bc7294beb0ce7e`; measured work commits are named in the SCORECARD round-90
record. Claims frozen in `plans/round-90-claims.md` and `.ufo/waves/round-90/claims.json`.

## Gate

Every row below was opened by this lane this round; the quote is located, ≤25 words, and reproduces
from the fetched bytes (scratch `/fast/scratch/hyaku/kaidoku-r90/l1/src`, deleted on exit; digests in
the row).

| id | source and opening | located quote | verdict |
|---|---|---|---|
| S313 | https://raw.githubusercontent.com/upx/upx/v5.2.0/src/p_unix.cpp — opened 2026-11-04, HTTP 200, 24181 bytes, sha256 `bf83c4133c27d394…` | line 472 `// Consumes b_info header block and sz_cpr data block from input file 'fi'.` (12 words); line 485 `fi->readx(&hdr, szb_info);`; line 504 `fi->readx(ibuf+j, sz_cpr);` | **admits** (tier A, code): the consumer's loop is the chain law — a twelve-byte header, then exactly `sz_cpr` payload bytes, so an in-range wrong value desynchronises the suffix |
| S314 | https://raw.githubusercontent.com/upx/upx/v5.2.0/src/p_lx_elf.h — opened 2026-11-04, HTTP 200, 31147 bytes, sha256 `895da5cd72da32bf…` | line 107 `unsigned o_binfo;  // offset to first b_info` (7 words) | **admits** (tier A, code): the packer names the first block's start, which is why a derivation searches forward from a boundary instead of anywhere |
| S315 | https://raw.githubusercontent.com/upx/upx/v5.2.0/NEWS — opened 2026-11-04, HTTP 200, 26202 bytes, sha256 `7eafd96adc1674a3…` | searched for `b_info`, `sz_cpr` and block-size statements: none | **rejects** (tier C, docs): user-visible change prose makes no statement about the block format or the walk; flip: a release entry that changes the block format or its bounds |

Status changes, old → new: `src/p_unix.cpp` as a whole (`PackUnix::unpack`) stays **rejected** from
rounds 87 and 89 — its flip condition ("a carrier class unpacked through the base class") is still
unmet, since the executables call `PackLinuxElf64::unpack`; this round's S313 is a *different scope* on
the same URL (`PackUnix::unpackExtent`, the block consumer every executable path calls at
`src/p_lx_elf.cpp:7902,7907,8051`), absent → mined. `src/p_lx_elf.h` absent → mined (S314). `NEWS`
absent → rejected (S315). Census `validate --root … kaidoku`: exit 0 before (217 rows, receipt
`.ufo/waves/round-90/pre/sources-census-before.txt`) and exit 0 after (220 rows; A 190→192, C 8→9;
mined 194→196, rejected 23→24).

## Mistakes

- **M90-1 — a parameterised seat prompt shipped with its placeholder unsubstituted.** Class: template
  substitution applied to one field only. Evidence: the first validated dispatch
  (`r90-w1-dispatch.json` before the fix) carried a literal `{LANE}` in 11 of 13 seat tasks, while the
  same file's header had absolute paths; my first rewrite pass touched `items[].task` and changed
  nothing because the payload field is `items[].prompt` (`rewrote 0 items`). Captured-by: a pre-dispatch
  scan for `\{[A-Z][A-Z0-9_]*\}` over the *dispatch* bytes, not the spec — a scan over the spec's
  `task` key would have found nothing. Fix: rewrite every string field of every item, re-validate,
  re-scan; the scan must print `[]` before `.ready` is written (it did, and the second dispatch carries
  no placeholder).
- **M90-2 — the freeze precheck cannot read an uncommitted container.** Class: an instrument's input
  resolution assumed. Evidence: `freeze-precheck.py --container .ufo/waves/round-90/claims.json` at the
  declaration tip returned `CONTAINER_BLOB_ABSENT` / `UNREADABLE`, exit 2, because it reads the
  container through `git show <rev>:<path>`. Captured-by: the tool's own finding code. Fix: commit the
  declaration first, then precheck at that revision — `18b21f09` returns `CLEAN` for round 90 and
  `FLAGGED` (`CLAIM_NO_COUNTER_PATH:R83-C1`) for the red control, `met true`, exit 0
  (`.ufo/waves/round-90/pre/freeze-precheck-at-declaration.json`). The order is now part of the
  declaration recipe.
- **M90-3 — a partial mirror makes the census lie.** Class: a check run on a stand-in that lacks the
  tree it validates against. Evidence: `sources-census.sh validate --file <mirror>/corpus/SOURCES.md`
  on a corpus-only copy of the declaration commit reported E11 for rows whose `used-by` files are
  `SKILL.md`, `tools/round-*.mjs` and wave paths; the same registry is exit 0 in the lane. Captured-by:
  E11 naming files that exist in the lane and not in the mirror. Fix: extract the whole declaration
  commit with `git archive <rev> | tar -x -C $S` (915 MB, 3.7 s), run the census there, delete the
  tree — exit 0; the receipt is `.ufo/waves/round-90/pre/sources-census-before.txt`.

- **M90-5 — a supersession reason claimed a field the receipt never carries.** Class: bookkeeping
  written from the diff's intent rather than from the produced artifact. Evidence: the round-90
  battery's `rev_state()` computes the worktree's dirty-path count, but `pins.pop("rev_state")` consumes
  it to resolve the commit, so no receipt field carries it, while the supersession reason in
  `claims.json` said it did; `jq '.pins.rev_state' c1-at-499d2183.json` → `null`. Captured-by: reading a
  produced receipt's keys against the sentence that describes it (the QUALITY 162 rule applied to a
  receipt instead of a docstring). Fix applied: the reason now says what the receipt carries; the
  field itself is a round-91 repair.

## Round-89 closure defects — dispositions

| id | disposition |
|---|---|
| D-89-1 (marker report) | Not repairable retroactively: `.ufo/reports/round-89/kaidoku.md` stays as filed. This round's report carries the evidence the marker lacked, and the round-89 record below is written now. |
| D-89-2 (attribution: a hyaku sweep committed the report under the lane identity) | Recorded here and in the SCORECARD; the lane's own round-90 report is committed through `fleet-commit.sh --as kaidoku` with this round's message. |
| D-89-3 (no landing measurement) | Fixed in kind: both frozen counters are re-run at this round's measured revision and their receipts committed under `.ufo/waves/round-90/l1/scores/`; round 89's own missing receipts stay missing. |
| D-89-4 (uncommitted round work) | Already committed at `c40a36f21` before this round opened (wave evidence, lesson, LOG entry); the lesson's `## Wave r89-w1 — seat results` placeholder was replaced in that commit. Verified at the base revision. |
| D-89-5 (no LOG/SCORECARD record) | LOG: the round-89 entry exists at `LOG.md` (checked at the base revision). SCORECARD: a retroactive round-89 record is appended in this round, labelled as written at round 90. |
| D-89-6 (dead pointers in an admitted entry) | Repaired: `verified-at` now points at the round-89 `LOG.md` entry and the receipts (with the correction noted in place), and the matrix producer is named by its real path `.ufo/waves/round-89/w1/ExecMatrix/field_matrix_r89.py` (the `tools/round-89/field-class-matrix.py` name never existed); `matrix.json` is committed. |
| D-89-7 (post-completion advance) | Recorded in this round's LOG entry: the lane pushed `fd9f840b` after the round-89 completion line, editing the round-89 entry and adding QUALITY 166-167; the receipts it cites are committed. |

## Wave r90-w1 — seat results

One v1 wave, 13 seats (executor 4, scribe 2, scout 1, reviewer 2, critic 1, mutation-tester 1,
sentinel 1, connector 1), attack roles 5/13 = 38.5 %, one connector; validated under
`scripts/hyaku/ufo-wave-policy.json` (13 spawn, 0 resume) and dispatched through the inline handoff
(`.ready` → orchestrator spawn → WAVE-DONE). The L1 held the planner seat (the validator refuses
`planner`). Wave evidence under `.ufo/waves/round-90/w1/`; every seat wrote only its own directory and
scratch, and two seat receipts that landed at the lane root were relocated to
`w1/ReviewerC2/receipts/misrooted/` byte-identical (M90-4).

| seat | delivered | what it changed in the round |
|---|---|---|
| CriticClaims | report + receipts | four defects against the frozen instruments: (1) the battery's `met` did not require the REA arm, so `--no-rea` produced the same label with `met_target true`; (2) `--rev` was a free string (`deadbeef…` → `met`, exit 0); (3) the battery docstring claimed isolation holds `["in"]` while the code accepts `["in","out"]`; (4) the repair docstring called the `u_len` bound "a preference, never a filter" while the code filters. All four closed by the instrument supersession at `499d2183` before the landing measurement. It also measured that the C2 predicate does not entail "decision table": a prose block citing `QUALITY 99999-100000` still scores 30/30 (QUALITY 175). |
| ExecBlind | report + receipts | the `carrier_blind` arm hides the pinned carrier paths and the run root but not the sibling `boxes` tree, which holds `cand-*` copies of the intact packed bytes; a repair reading those would score inside the "blind" sandbox. QUALITY 174; the claim's sentence is still true as written (pinned paths hold decoys, the probe proves it, `cheat_repack` is killed) and the report does not claim more. |
| ScribeEntry | report + entry draft + receipts | an independent battery run returned `P1 6 of 6; P2 3 of 4; P3 4 of 4` (REA 1267 vs 1268 on docker-init), reruns 1268 — the flake the report discloses; and a real repair defect: a *last-block* tamper falls through to the round-89 law, which writes the `UPX!` sentinel word (jq 10,094; libz 60,124) with rc 0 and `upx -t` still red. QUALITY 176, routed to round 91; the frozen counter scores interior cells only. |
| ScribeBlock30 | report + block draft + receipts | the landed block 30 (ten rows), verified at a scratch candidate, with three red worlds and a base-presence gate that refuses worlds the counter alone passes (`corpus/lessons/round-89.md` and `tools/round-90/` absent at base, `QUALITY 999`). Integrated verbatim at `8346eacc`. It also established that `corpus/lessons/round-89.md` is absent at base, so a block citing it would fail QUALITY 159 — the reason the block cites QUALITY rows instead. |
| ExecMutation | report + mutant table + replay driver | 17 declared-case mutants on the two instruments: 2 killed, 15 survived, each with the selftest case that would kill it (harness-level `score()` cases, decoy-successor, chain-gap fixtures). Depth limit recorded; the case set is a round-91 candidate. |
| ExecMatrix | report + matrix + receipts | 20 in-class interior cells across the four carriers: 18 recovered, 2 leave-alone (the last-block shapes), 0 refused; block layout and `u_len` re-derived per carrier. |
| ExecDeriveIndep | report + independent derivation and receipts | an independent from-scratch derivation of the break-point law and its comparison against the lane's repair. |
| ReviewerC2 | report + receipts | block 30 green at the landed revision and red at both base revisions, plus three negative probes the counter passes and the base-presence gate refuses (QUALITY 175 evidence); record-keeping nit on two base receipts differing only in the revision echoed. |
| ConnectorOverlap | report + receipts | sibling-scope sweep: 0 exact matches for the packed-ELF/instrument-revision ground across the fleet's PROVINCE/README files; no `considerthese/` in this lane (`Path not found`); `merge/kaidoku/` carries no UPX entry. |
| SentinelScope | notes + receipts | hostile-input and cost probing of the repair; its findings are carried in the entry's limits and QUALITY rows. |
| ReviewerC1, MutCounter, ScoutUpxPack | PENDING_WAVE |

