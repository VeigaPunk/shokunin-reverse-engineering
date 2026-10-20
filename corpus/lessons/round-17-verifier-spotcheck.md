author: hyaku closure (non-author integrator, @m_opus)

# Round 17 — independent closure and admit/reject spot-check

Date: 2026-10-20. Status **ok**; **admitted** for the bounded C1 calibration and C2 depth (+ capability `retained REA Ghidra-session log capture`) claims. Six status-neutral defects are routed below. No promotion, mint, `[x]`, recovery-quality claim or Ghidra-cause claim is authorized.

## Revisions and scope

- Baseline B: `b563c799d97774aae4351276fe43cb897311e349`.
- Predictions frozen: `271167473d87ef710f07ecdd98caf0ce12091686`.
- Verification source S: `d0ab2992149a38794e5ef2474ba5d4ef5ee1e905`; evidence `b31975de62de5413a6f2d244f2690eaeb3d18c25`.
- Delivered A: `de6c721be61bf6e8b4001021f09a9cdea38166dd`.
- Fleet report: `.ufo/reports/round-17/kaidoku.md`, committed as `kaidoku-shokunin` in fleet commit `7807afe5005e640d1c23933f3dcfffd52c39cd8b` (2026-10-20T11:51:18-03:00).
- Read-only re-check seats dispatched by this closure (not by the lane): `ClosureKaidokuR17.PromptFidelityR17`, `.C1RemeasureR17`, `.C2EvidenceR17`, `.SpotcheckSourcesR17`, `.WavesInstallsR17`, `.NoHarmR17`. I adjudicated their findings and re-ran the decisive ones myself (marked "own").

Committed dispatch/completion digest (the mutable watchdog log is not the durable pointer):

```text
2026-10-20T10:14:11-03:00 launch kaidoku round=17 pgid=11845 driver=hyaku-inline attempt=1
2026-10-20T11:51:47-03:00 complete kaidoku round=17; hyaku-inline attempt=1
```

Not executed by this closure: any lane tool, gate or selftest (`run-carriers.sh`, `carrier-run.py`, `receipt-validate.py`, `pins.py`, `temporal-sweep.py`, `invocation-audit.py`, `measure.py`, `controls.py`, `verify.py`, citation-drift, quote-fidelity). Their outputs below are committed evidence verified. I executed Git-object censuses, the shared sources census, and web/local source re-opens. No tools installed or updated by this closure.

## Step-1 conformance

Own commands and outputs:

```text
git -C /home/vgpnk/Projects/shokunin log --format='%an %ae %H %s' -- .ufo/reports/round-17/kaidoku.md
kaidoku-shokunin kaidoku@shokunin.local 7807afe5005e640d1c23933f3dcfffd52c39cd8b round-17: kaidoku report

/home/vgpnk/Projects/shokunin/scripts/hyaku/jj-lane.sh state /home/vgpnk/Projects/shokunin/kaidoku-shokunin
state branch=main local=de6c721be61bf6e8b4001021f09a9cdea38166dd remote=de6c721be61bf6e8b4001021f09a9cdea38166dd ahead=0 behind=0 head=attached tracked=0 untracked=0   (exit 0)

git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin status --porcelain
(empty, before closure writes)

git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin ls-remote origin refs/heads/main
de6c721be61bf6e8b4001021f09a9cdea38166dd	refs/heads/main
```

- Ancestry: `git cat-file -t` = commit and `git merge-base --is-ancestor <h> refs/heads/main` = 0 for B, `2711674…`, `da64646`, `95e34db`, S, `b31975d…`, `8e7642c`, A. The report commit is an ancestor of fleet HEAD.
- Ordering: lane commits 10:46:45 → 11:50:03 (-03:00), all authored `kaidoku-shokunin`. `refs/remotes/origin/main` reflog shows each pushed 2 s after commit, the last (A) at 11:50:05. The report followed at 11:51:18. Report lands last.
- Report content: work, LOG-tied changes, Sources & frontier, trend verdicts, and `## SHONEN` with exactly four `[~]` lines. Not a marker.
- Prompt: `.ufo/prompts/kaidoku-round-17.md`, committed in `3091c4056db592b81e2ce7dcca6a729936b82768` at 10:14:09. Lines 1–140 are byte-equal to `templates/round-prompt.md` rendered for kaidoku/17 (`diff` exit 0); §6 addendum starts at line 141. Every round-level item and child-lane item is present: claims/axes :11–16, L2 ≥8 one batch :82, commit-then-push :133, push scope :135–137, L0 :138–140, report path :101, SHONEN :118, hash citation :106–107/:261, write scope :241–243. No stale L2 bucket map: §1–§5 defer to the host route table, and fleet `MISSION.md:61-65` equals canonical `MISSION.md:72-76`.
- Template-level note (operator-side, not a lane defect): the template body has no distinct lane write-scope item; it reaches lanes only through the hyaku addendum (:241). PROTOCOL.md:103-104 says the template embeds all five child-lane items. Routed to protocol/operator below.
- Stale-lane: open 97 min. The report rates it progressing (seven lane-authored commits); confirmed.

## Claims — independent re-check

### C1 calibration — improved (re-measured)

Own/seat Git-object census, with no lane tool run:

- **R16-PROVENANCE.** At B, `git grep -n -I -i` over temporal-stability phrasing returns exactly the four named r16 assertion sites: `LOG.md:2012`, `corpus/lessons/round-16.md:154`, `corpus/knowledge/2026-10-20-r16-go-selection-preview.md:95`, `.ufo/waves/round-16/verification.json:419`. The other hits are routed-defect text or are review-scoped. Those filed bytes are unchanged at A: equal blob ids, and the LOG diff has 0 removed lines (`cmp` prefix-exact, 2031→2123 lines). At A, `corpus/lessons/round-17.md:96-99` carries one line-exact `R16-PROVENANCE:` correction per site, duplicated at `LOG.md:2059-2062`. **4 unqualified → 0**, and no new r16 assertion. The fleet-report site `.ufo/reports/round-16/kaidoku.md:60` is corrected in the r17 report (line 53) as an erratum, not a rewrite.
- **R16-INVOCATION.** A seat re-implemented the row/argv definition from reading `invocation-audit.py` source and ran it over `git show` blobs. Result: B has 7 rows (5 match, 2 unlabelled_variant at `SKILL.md:448`/`:449`); A has 17 rows (17 exercised_match). This equals the committed `final-recheck/invocation-audit-final.receipt.json` (rev `8e7642c`: 17/17).
- **QUALITY.** Rows 18 → 20. A grep over rows 1–18 hashes `ab3e52c2…4910` at both revisions. #19's why-cell cites `round-16-verifier-spotcheck.md:183`.
- **Red-before (evidence-verified).** `verification.json` retains `selftest-*` commands with exit-as-expected for `pins.py` and `receipt-validate.py`. It contains 79 commands: 78 have a numeric expectation and all 78 match; `custody-capture` has expected `null` by construction. `unexpected_exits: []`, revision S, run 14:47:30–14:48:08Z (after S was pushed at 14:47:26Z and before `b31975d`). The committed `final-recheck` shows temporal-sweep at 4 sites/4 corrected/0 new and citation-strict clean.

### C2 depth + capability — improved (evidence-verified, logs re-read)

- **Frozen before measured.** `2711674` was committed 13:46:45Z and pushed 13:46:47Z with zero `runs/` files. The earliest first-pass step is 13:47:05.97Z. Prediction blobs are identical from `2711674` to A (16 files). `replicate-expectations.json` was committed at `95e34db` (14:27:35Z), before the second pass's first step at 14:27:41.94Z.
- **Runs.** There are 8 receipts at `da64646` and 8 at A: 16 distinct blobs. `carrier-run.exit`, `compare.exit` and `observation.exit` are 0 for 8/8 in each pass, and `all_match` is true for 8/8 in each pass. Retained `ghidra.log` sha256 equals the receipt record in 8 of 8 sampled (4 per pass, including aether: `5e6d8563…2939`). All 16 logs contain `REPORT: Analysis succeeded`.
- **Logs are committed** under `runs/<label>/logs/<session>/`. `/tmp/kr17-rea-*` appears only as `session_dir`, so there is no tmpfs evidence pointer.
- **Routes re-derived from raw log lines** (not from `compare.py`): info {esbuild-0.25.12, esbuild-0.21.5}, fallback {aether, notesmd-cli} (`Falling back from` ×1), none {shfmt, containerd-shim, op, esbuild-0.27.7} (`Untested Go version` + `Missing Go bootstrap`). This is 8/8 versus the frozen predictions in both passes.
- **aether.** The normalized results across passes differ only in `string_count` (29118 → 29117), so the Evidence ID changed (`ev_ae9f7086…` → `ev_247261e8…`). The frozen replicate expectation is therefore falsified for aether and held for 7/8, as reported. Both logs carry `Caused by: java.io.EOFException: Unable to read past EOF: 17645861, 111938854` at line 177. The knowledge entry (:145–163) labels the cause INFERENCE. Honest misses, honestly carried.
- **Capability.** `| Capability |` table data rows go 6 → 7. `measure.py:46` text matches 0 → 1 (`SCORECARD.md:2374`). REA 6.5.0 and Ghidra 12.1.4 appear in 16/16 receipts.

Limits found, routed below and not claim-breaking:
- Only 8 of the "all 16" receipt validations are retained.
- Mid-run pin checks keep verdicts, not maps.
- Second-pass receipts were produced by `95e34db` tooling; S is the verification revision.
- The pass-1 `run-log.txt` lists 7/8 carriers (it omits calib-shfmt, whose receipt is present).
- The frozen `predictions/SHA256SUMS` dropped its `carriers.tsv` line. `carriers.tsv` itself is unchanged.

### No-harm (B→A)

- 15130 B blobs: 15123 identical, 7 modified, 0 deleted.
- All 94 prior knowledge files, 20 prior lesson files and 5 prior verifier files are byte-identical.
- `SCORECARD.md`: numstat `78 0`, append-only, no score decreased.
- `SKILL.md`: 41 additions; the only 2 deletions are the in-place `:448`/`:449` alignments, and no cited table was removed.
- `README.md` 190/190 and `PROVINCE.md` 162/162 lines; the knowledge map goes 94/94 → 95/95 with 0 missing.
- SOURCES rows go 23 → 32. Tiers go A21/B1/C1 → A28/B3/C1; statuses go mined22/rejected1 → mined30/rejected2. Of S001–S023, only S003/S023 changed, as `used-by` appends.
- 0 `__pycache__`/`.pyc` files are committed.
- Max evidence timestamp precedes its shipping commit: 14:48:08Z < `b31975d`, and 14:49:54Z < A.

### Waves and installs

- **W1:** `wave1-dispatch.json` holds one `taskCall` with 78 tasks: executor14/scout20/reviewer12/connector8/revenger4/simplifier2/scribe10/critic6/sentinel2. 78/78 completed and 78 reports are present. Attempts at 10:25:15 and 10:28:15 were refused at the job cap; the 10:31:15 attempt spawned. The payload file is unchanged.
- **W2:** 69 tasks, with 67 completed. `PinsAttack` and `TemporalSweepAttack` failed on `resource_exhausted … (m_swe)` and have no report file. Task keys are only agent/name/task, with no per-seat `model`. 147 seats ≤ 200, and the L2 floor is met in W1.
- **Go 1.27.3 install — in scope and recorded.** It was needed to read the pinned go1.27.3 stdlib source (S024/S026) and to run the file-reading `go version -m` cross-check. The recorded tarball sha256 `65efbc80…9b40` (`w1/draft-sources-rows.md:5`) equals the official `go.dev/dl/?mode=json&include=all` entry. It sits at `~/.local/opt/go-1.27.3` (mtime 10:32:19, inside the round) and is not on PATH (`command -v go` → none). The tool, version, channel, sha and reason are recorded in `round-17.md:135-141` and the report.
  - The deviation is immaterial: a multi-file toolchain installed to `~/.local/opt` rather than `~/.local/bin`, and invoked by absolute path. Pacman was paused, and its candidate is 1.27.2. The record does not state why pacman was bypassed (minor).
  - `rea-agents@6.7.0` is in `~/.npm/_npx` only and is recorded.

## Outside discernment sample

Sources re-opened 2026-10-20. "Own" means I re-opened it personally; the other rows were re-opened by a closure seat and adjudicated here.

| Item | Gate decision | Re-opened source | Outside decision | Reason |
|---|---|---|---|---|
| S024 Go `debug/buildinfo` (own) | admit (mined) | `curl https://raw.githubusercontent.com/golang/go/go1.27.3/src/debug/buildinfo/buildinfo.go` line 411 → `return 0, errNotGoExe`; seat: :58/:97 exact, upstream = local GOROOT sha | agree | Reference decoder quotes exact at cited lines; quotes 6/3/3 words (≤25) |
| S028 Go 1.27 notes (own) | reject (row kept) | `curl -sL https://go.dev/doc/go1.27`: sha256 `a4c56ba5…393e` equals row; `grep -oic dwarf` → 0; quoted `nosizespecializedmalloc` sentence present | agree | The page cannot ground `X:nodwarf5`; S026/S031 do. Reproducible to the byte |
| "1.15–1.25 range check stops Go analysis" | reject | Installed/tag `GoRttiMapper.java:170-172`: `Msg.error(... "Untested Go version ...")`, no throw/return; continues to `GoApiSnapshot.get` :176 | agree | Source shows log-only; runs cannot separate range from missing base |
| S029 Ghidra range | admit | tag `Ghidra_12.1.4_build` and master `b8e9917` `GoRttiMapper.java:79` → `"1.15-1.25"` / `"1.15-1.26"`; file sha256 match row | agree | Release vs master status kept separate |
| S031 Go 1.25 DWARF5 | admit | `https://go.dev/doc/go1.25#dwarf5-support`, sha equals row, quote at page :628–629 | agree | 15-word quote exact |
| S025/S026/S027/S030/S032 | admit | release page anchors; `main.go:197`, `exp.go:158`; issue 75953 comment; GoReSym v3.3 body; PR #9348 title (OPEN) | agree | All quotes exact and ≤25 words; S032 is correctly tier B and a lead only |
| Knowledge entry (pin sentence, `…r17-go-carrier-diagnostics.md:28-33`) | admit | `runs/pro-aether/receipt.json` `.steps.analyze.pin_checks` → `{changed:[],entries:146,equal:true,missing:[],taken_at_utc}` ×3; `carrier-run.py:481-486` | **partial disagree** | Route/log substance agreed; but "each pin map is retained … all maps are equal" overstates: mid-run instants keep a comparator verdict and count, not the per-path map QUALITY #19 itself requires |

Required census (own):

```text
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku
kaidoku	ok	/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md
exit=0
```

## Axis and trend verdicts

| Axis | Verdict | Scope / evidence |
|---|---|---|
| calibration | improved | C1 re-measured: 4 → 0 unqualified r16 sites, 2/7 → 0/17 unlabelled registry rows, QUALITY 18 → 20 with rows 1–18 identical. New overstatements are routed (R17-PINMAP, R17-VALIDATE16), and they are smaller than what was discharged |
| depth | improved | 16 committed run-bound logs; routes re-derived 8/8 per pass against bytes frozen before the run; honest aether misses |
| coverage | unchanged | 94/94 → 95/95 is index integrity on held Go ground |
| operability | unchanged | No declared operability claim. Capability is credited under C2 and registry alignment under C1, not double-counted |
| freshness | unchanged | Upstream status re-read (S029/S030); no broad runtime-freshness claim |
| adjacency | unchanged | Nothing absorbed; the revenger/kaidoku contest is unchanged (integrator-owned) |

- **expansion: unchanged.** The new entry sits on held Go ground. The capability row is repertoire, and the LEARNING `improved` bar (entries on uncovered ground) is not met.
- **quality: improved.** r14–r16 source-model predictions are superseded by runtime-retained observations. The four r16 temporal sites are line-exactly corrected. The sampled retained logs (8/8, 4 per pass) re-verify against their recorded hashes, all 16 reach `Analysis succeeded`, and no admitted entry failed its route recheck. The pin-map wording is now marked and routed.
- **discernment: improved.** Both r16 outside disagreements became grounded QUALITY #19 plus working fixes. This sample agrees on 10/10 source/reject decisions (S024–S032 incl. the S028 reject, plus the range-check reject). The one partial disagreement (pin sentence) is routed here as a lesson for the next round, not left unlearned.

SHONEN is **not** fully checkable by a non-author: instructions are not outside-executed, and province accuracy hinges on the unresolved revenger contest. All four `[~]` remain, and promotion is operator-owned.

## Routed defects (kaidoku, next round; status-neutral)

1. **R17-PINMAP.** The second-pass mid-run `pin_checks` retain `{taken_at_utc, equal, entries:int, changed, missing}`, not per-path maps (`carrier-run.py:481-486`). Yet these texts say each pin map is retained: `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:30-32` ("each pin map is retained … All maps are equal"), `SCORECARD.md:2374` ("pre/mid/post pin maps with instants") and QUALITY #19 (which requires the map). Either retain mid maps (or their digest) or append a named correction: "mid-run instants retain the comparator verdict against the retained pre map, not the map".
2. **R17-VALIDATE16.** `SCORECARD.md:2364` says "all 16 receipts `receipt-validate.py` exit 0", and `round-17.md:122` says "All 16 receipts pass the final validator". `verification.json` retains 8 `receipt-validate-*` runs, all on the A receipts. The 8 `da64646` receipts have only w2 seat prose. Retain the validator run over `git show da64646:…/runs/*/receipt.json`, or correct the count to 8.
3. **R17-PRODUCER-REV.** The second-pass receipts (14:27:41–14:40:02Z) were produced by `95e34db` `carrier-run.py`: they lack `carrier.md5_pre`/`binding.md5_ok`, which were added before S. S (14:47:24Z) is the verification revision. Name the producing revision per pass wherever "measured source revision" is cited.
4. **R17-SUMS-RUNLOG.**
   - `predictions/SHA256SUMS` lost its `carriers.tsv` line between `2711674` and A. The file is unchanged, but the frozen manifest no longer covers it.
   - The pass-1 `runs/run-log.txt` at `da64646` lists 7/8 carriers and has no final exit line.
   - Restore coverage and append the correction.
5. **R17-REGISTRY.**
   - 4/10 new SKILL registry rows (go-route-compare, receipt-validate, pins, go-buildinfo-probe; `SKILL.md:540-542,545`) give no pinned-value path or write scope (PROTOCOL §Gate standard row fields).
   - The citation-drift row (`:448`) is registered `probe` while its registered `--strict` entry can exit 1, which makes it a gate.
6. **R17-S032-DIGEST.** S032's page sha256 `436c0f63…` cannot be reproduced: two fetches gave `028dbb7d…` and `f3841de0…`, because GitHub HTML is dynamic. Anchor the row on title and state, or qualify the digest as fetch-time only.

Operator/protocol (not lane debt): `templates/round-prompt.md` lacks a distinct child-lane write-scope item, which reaches lanes only via the hyaku addendum. Either PROTOCOL.md:103-104's "embeds all five" or the template needs correcting. Minor install-record gap: say why the official tarball was chosen over pacman (pacman paused; candidate 1.27.2).
