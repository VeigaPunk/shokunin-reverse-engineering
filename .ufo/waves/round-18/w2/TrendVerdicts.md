PARTIAL

# TrendVerdicts — round 18 LEARNING trends at REV `b2aad08ceeee8dd125ce0d316056d8bd766c7f94`

Seat: `KaidokuR18.TrendVerdicts`. This is advice from the author side, not the outside spot-check that LEARNING.md:42-46 requires.

- **Axes judged:** calibration, operability, depth.
- **Proposition tested:** "at REV, round 18 earns `improved` trends with no harm".
- **Why PARTIAL:**
  - quality improved holds;
  - expansion is `unchanged`, not `improved`;
  - discernment cannot be earned at REV.
- **Anchors:** every anchor is `git show REV:<path>` unless marked B (baseline `9011581d84527ba34c675f9cf912e54d2e72d470`). The protocol is `/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/`.
- **No lane claim yet:** at REV the lane has declared no trend verdict.
  - round-18.md, contract.md, measure.py and verify.py contain 0 trend hits.
  - The round-18 LOG and SCORECARD sections defer to "Measured records".
  - So these are first judgements, not attacks on a lane claim.

## Verdicts

| Trend | Verdict | Reason |
|---|---|---|
| expansion | **unchanged** | The Swiss-map entry adds depth on held Go ground. It sits in the existing coverage-map Go row. Its surface is PROVINCE Core, and the mechanism was already mapped as an INFERENCE. No frontier was entered and no capability row was added. SOURCES rows do not count. |
| quality | **improved** | The r17 aether INFERENCE is superseded by a replay whose rule was frozen before the run. The r17 overstatements are marked append-only. S032→S033 follows CORPUS rule 2. My re-check: 15/15 validator exit 0, and both held-out diagnostic (D-label) compares `all_match`. Caveats: F1–F3. |
| discernment | **improved — provisional, not earnable at REV** | The r17 disagreement → lesson → grounded criterion (#21) path holds, and I reproduced the red-before evidence. But the outside spot-check is `Pending` (round-18.md:47), and three Mistakes rows that no criterion caught got no new criterion (F4). |

**Reject note for the judge.** If the closure claims `expansion: improved` for the Swiss-map entry, reject it. The counterexamples are observations 1–4 under Expansion below.

## Expansion — unchanged

### Observations

1. **PROVINCE is byte-unchanged from B to REV** (C2 exit 0).
   - Core already owns the surface: `Ghidra provider` (PROVINCE.md:46) and `Native ELF via Ghidra` (:48).
   - `Cross-version compare` (:52) already cites `2026-10-20-r17-go-carrier-diagnostics.md` and the r14 entry.
   - PROVINCE's held test (:30-32) needs a `LOG.md` entry citing `evidence_id` and subject sha256. LOG r18 (LOG.md:2125ff) has 0 `ev_`/64-hex tokens (C9 exit 1).
2. **The coverage map gained no row.**
   - The README diff is 1 line changed (C3). The r18 entry is appended to the existing Go row, README:35.
   - At B that row already listed r14–r17 and said "aether's post-bootstrap symbol-markup EOF was unpredicted".
   - At REV neither Frontier list has a Go/Swiss bullet (README:170ff, PROVINCE:73ff; C5/C6 = 0, exit 1).
3. **The mechanism was mapped at B as an INFERENCE.**
   - r17 entry:145 reads "INFERENCE, aether cause" (C7). B `SKILL.md:528` reads "INFERENCE, not replayed" (C8).
   - Round 18 moves it from INFERENCE to confirmed. That is depth: claims.json:25 says `"axis": "depth"`.
   - LEARNING.md:87-88 maps depth to quality, and coverage/adjacency to expansion.
4. **The same row has an outside precedent.**
   - round-17-verifier-spotcheck.md:129: "expansion: unchanged. The new entry sits on held Go ground" (C11).
   - The Go rounds before r18 recorded expansion unchanged: SCORECARD.md:2218, 2282, 2307, 2339, 2408.
5. **No other expansion observable fires.**
   - SCORECARD round 18 has no capability row (C10 = 0).
   - S033–S036 are rows, not knowledge (CORPUS.md:123, "Expansion is knowledge, not rows").
   - S034/S035 are Go docs and code, the same kinds as S024–S031.
   - S036 (jj) is used only by `corpus/lessons/round-18.md` and `SKILL.md` (C31).

**[INFERENCE]** Calling this `improved` would count the confirmation of an already-mapped inference as uncovered ground. That conflicts with LEARNING.md:33 and :87-88, and with the r17 outside ruling.

### Harm check: does the admitted entry fail its bar?

These checks passed:
- **#20:** the route column cites the `GoApiSnapshot` line (s1246-swiss-nethttp `ghidra.log:180`), not the `GoRttiMapper` request echo (:181). The WARN fallback lines are kimi :68 and aether :92 (C19).
- **#4:** the 12-hex prefixes resolve to the full `sha256_pre` in the receipts (C17).
- **#5/#6/#7:** the Observations, Inference and Not-examined sections are present (entry:70, :99, :110).

Two text defects were found (F1, F2).

**[INFERENCE]** I put them in the routed-defect class rather than `harmed`. Precedent: R17-PINMAP was an overstatement in an admitted entry. The outside reviewer marked it partial disagree and routed it, and the r17 trends were not harmed (round-17-verifier-spotcheck.md:108, :129-131). A judge applying QUALITY #12 literally could still rule `harmed` until F1 is corrected.

## Quality — improved

**Weaker superseded by stronger.**
- The r17 INFERENCE is replaced by a replay under a frozen rule.
  - Freeze commit `eb6c266`: committer time `13:23:55-03:00`, an ancestor of REV, SHA256SUMS at 12 lines (C30).
  - First run step: `13:24:07-03:00` (`runs/run-log.txt`). All 15 runs logged carrier-run=0 and compare=0.
  - Both held-out D labels show their exact predicted read: s1246-swiss-nethttp `Invalid index: 22386945` (ghidra.log:451) and kimi-webbridge `Invalid index: 15606016` (:206).
- S032 → S033 is a new row whose teaches opens "supersedes S032 —". That is the contract form (CORPUS.md:116). Keeping S032 `mined` is compliant.

**Stale statements marked.**
- The R17-PINMAP correction is appended to the r17 entry (RB-1: B grep exit 1 → REV count 2).
- R17-VALIDATE16: `evidence/validate16/summary.json` shows 8 receipts, 8 exit 0, 2728 checks.
- SCORECARD.md:2428ff and LOG.md:2125ff carry the routed corrections.

**Re-check** (my runs; worktree confirmed equal to REV):
- `receipt-validate.py --require-mid-maps`: 15/15 exit 0.
- 22/22 mid checks carry `map_path` and `map_sha256` (C17).
- Pinned carrier bytes: 12/12 `OK` (C29).
- D-label compares are `all_match: True`, including `extra.invalid_index_reads` (C18).

No admitted entry failed its re-check in this sample. Caveat: F3 (low).

## Discernment — provisional

**The second disjunct of LEARNING.md:35 holds on author evidence.**
- The r17 outside partial disagreement (round-17-verifier-spotcheck.md:108) became round-18.md Mistakes row 1 (:62).
- It also became QUALITY #21 (QUALITY.md:31, `sharpens 19`), which cites both lessons.
- CriticDiscernment's corrections all landed:
  - the operative recheck clause;
  - an honest captured-by ("#19 by text; not applied");
  - the `--require-mid-maps` flag;
  - the `recheck:` gloss correction.

**Red-before reproduced:**
- RB-1: exit 1 at B.
- RB-2: 8 labels, 29 mid checks, all with verdict-only key sets at B.
- r17 receipts under `--require-mid-maps`: 8/8 exit 1, with 29× `mid_map_missing`.
- The same receipts without the flag: 8/8 exit 0, so no regression.

**No harm condition applies.**
- #21 has lessons behind it.
- The r12 open items are adjudication debts, not disagreements. round-12-verifier-spotcheck.md:12-13 records agree/agree, and round-18.md:73 carries the items openly.

**Not earnable at REV.**
- The outside sample is `Pending` (round-18.md:47), and "Self-assessed taste is not discernment" (LEARNING.md:42).
- My author-side preview does not count:
  - S034 admit — agree: raw lines 571-573 are exact, and the page sha256 `d35c2d52…` equals the row's.
  - go1.25 reject — agree: the page has 0 `swiss` and 0 `noswissmap`.
  - S035 quotes are exact in the local toolchain tree.
- F4 weakens the verdict further.

## Findings

### F1 — the rebuild claim outruns its cited audit

- **Axis:** calibration. **Bar:** QUALITY #12 (QUALITY.md:22).
- **Counterexample:** entry:44-47 says "12 deterministic synthetic builds … two rebuilds byte-identical, w1 `CarrierRecipeAudit.md`".
- **Evidence:**
  - The cited audit rebuilt 8 carriers. CarrierRecipeAudit.md:11 says "all 8 carriers byte-identical"; it mentions `nethttp` 0 times (C20); `evidence/carrier-buildinfo.json` has 8 labels.
  - The 4 nethttp carriers appeared later, at 12:36–12:37 (RevNotesmdMaps.md:146-149). One of them, s1246-swiss-nethttp, is a held-out D label.
  - Those 4 were only checked against their own pins (SwissMisreadTool.md:174; C29). They were never rebuilt.
- **F1b:** entry:39 lists `http.Header` among the nethttp shapes.
  - The frozen emulator inventory for s1246-swiss-nethttp holds only `*textproto.MIMEHeader` and `*url.Values` (C22).
  - This matches RevNotesmdMaps.md:151-154, which observed `http.Header` absent from all four binaries.
- **Impact:** calibration only. Outcomes stay bound to the receipts' `sha256_pre`.
- **Smallest safe correction:** an append-only correction to the entry that:
  - limits "two rebuilds byte-identical" to the 8 methods/nomethods carriers;
  - says the nethttp carriers are pinned (SHA256SUMS 12/12 OK) but were not rebuilt, and are not called deterministic (or run the two-rebuild check on them);
  - says "the source declares three shapes; the binaries carry two".

### F2 — the new entry does not meet #21's recheck clause

- **Axes:** calibration and operability. **Bar:** QUALITY.md:31.
- **Counterexample:**
  - The entry's Runs bullet makes a retention statement: "mid-run maps retained as `pins/mid-<n>.json` with `map_sha256`".
  - Its `recheck:` (entry:3) lists the validator, grep, the emulator and a rerun. None of them prints the retained keys.
  - The validator prints counts, checks and findings only (C12 output).
- **Substance holds:** 22/22 mid checks carry the keys.
- **Smallest safe correction:** add `jq -c '.steps.analyze.pin_checks|map(keys)|unique' .ufo/waves/round-18/runs/<label>/receipt.json` to the recheck.

### F3 — the r17 entry has no forward pointer

- **Axis:** quality (low).
- **Counterexample:**
  - The r17 entry never points to the r18 replay (C23 = 0, exit 1).
  - Its INFERENCE still frames the trigger as a map-type "method-info" field (r17 entry:150, :156).
  - round-18.md:19 rejects the methods trigger.
- **[INFERENCE]** The wording is ambiguous: "method info" may mean the uncommon block, which would agree with H1.
- SKILL and README:35 carry the update; the entry itself does not.
- **Smallest safe correction:** add one line to the existing "Round-18 correction" block pointing to `2026-10-20-r18-swiss-map-replay`.

### F4 — uncaught mistakes did not become criteria

- **Axis:** discernment. **Bar:** LEARNING.md:19-21.
- **Counterexample:**
  - round-18.md Mistakes rows 4 (:65), 6 (:67) and 8 (:69) have captured-by `none`. Row 5 (:66) is partly `none`.
  - QUALITY gained one row citing round-18.md (C25 = 1). That row is #21, which came from row 1, a mistake #19 had already covered by text.
  - No why-not is recorded for rows 4, 6 or 8.
- **Smallest safe correction:** add one criterion per row, each citing round-18.md, or record a why-not per row. Candidate criteria:
  - after any file is added, re-verify a frozen manifest line for line;
  - admit a counter only if a token-only fixture stays open;
  - a diagnostic design names, before the run, the labels on which H0 and H1 differ.

## Commands

cwd is the lane root. `R`=REV, `B`=baseline. C2–C31 ran with `set -o pipefail`, so a pipeline's exit is grep's when grep fails.

```
git rev-parse b2aad08ceeee8dd125ce0d316056d8bd766c7f94^{commit}        -> b2aad08…  exit 0
git rev-parse HEAD refs/heads/main                                       -> b2aad08… b2aad08…  exit 0
git diff --stat R -- .ufo/waves/round-18/runs .ufo/waves/round-17/tools .ufo/waves/round-17/runs corpus/knowledge/2026-10-20-r18-swiss-map-replay.md  -> (empty) exit 0
git status --porcelain --untracked-files=all -- (same runs/tools paths)  -> (empty) exit 0
C2  git diff --quiet B R -- PROVINCE.md                                  -> exit 0
C3  git diff --numstat B R -- corpus/README.md PROVINCE.md               -> "1 1 corpus/README.md"  exit 0
C4  git show B:corpus/README.md | grep -c -i swiss                       -> 0  exit 1
C5  git show R:corpus/README.md | awk '/^## Frontier/{f=1;next} /^## /{f=0} f' | grep -c -i -E 'swiss|maptype|map type|\bgo\b|golang'  -> 0  exit 1
C6  (C5 on R:PROVINCE.md)                                                -> 0  exit 1
C7  git show B:corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md | grep -n 'INFERENCE, aether cause'  -> 145  exit 0
C8  git show B:SKILL.md | grep -c 'INFERENCE, not replayed'              -> 1  exit 0
C9  git show R:LOG.md | awk 'NR>=2125' | grep -c -E 'ev_[0-9a-f]{8}|[0-9a-f]{64}'  -> 0  exit 1
C10 git show R:SCORECARD.md | awk 'NR>=2428' | grep -c -i capabilit      -> 0  exit 1
C11 git show R:corpus/lessons/round-17-verifier-spotcheck.md | grep -n -o 'expansion: unchanged.\*\* The new entry sits on held Go ground'  -> 129  exit 0
C12 for d in .ufo/waves/round-18/runs/*/; do python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps $d/receipt.json; echo exit=$?; done
    -> 15 receipts exit 0 ("status":"valid","findings":[]); run-log.txt (glob artifact, not a receipt) exit 2 unreadable
C13 (C12 over .ufo/waves/round-17/runs/*/receipt.json)                  -> 8/8 exit 1; mid_map_missing 4+2+3+2+4+4+2+8 = 29
C14 (C13 without --require-mid-maps)                                    -> 8/8 exit 0
RB-1 git show B:corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md | grep -n 'R17-PINMAP\|comparator verdict'  -> (no output) exit 1
     git show R:(same) | grep -c 'R17-PINMAP\|comparator verdict'       -> 2  exit 0
RB-2 for each B:.ufo/waves/round-17/runs/<l>/receipt.json: python3 -I -B -c '<pin_checks key sets>'  -> 8 labels, 29 checks, keys (changed,entries,equal,missing,taken_at_utc), all equal True  exit 0
C17 python3 -I -B -c '<r18 receipts: pin_checks keys, carrier.sha256_pre>'  -> receipts=15 mid_checks_total=22 missing_map_keys=[]; aether 06c91f55df4117e5…006e, notesmd 412dc532d278b9e4…802d  exit 0
C18 git show R:.ufo/waves/round-18/runs/<l>/compare.json | python3 -I -B -c '<walk>'  -> s1246-swiss-nethttp, real-kimi-webbridge: all_match True; extra.analyzer_errors_contain/eof_reads/invalid_index_reads match True; s1250-swiss-nethttp, s1246-noswiss-nethttp: analyzer_errors_empty match True  exit 0
C19 git show R:<run>/logs/*/ghidra.log | grep -n -E 'Using Go API snapshot|Falling back|GoApiSnapshot|Go analysis failure|Invalid index|read past EOF'
    -> s1246-swiss-nethttp :180 INFO (GoApiSnapshot) / :181 INFO (GoRttiMapper) echo / :408 / :451; kimi :68 WARN 1.24.13->1.24.6 / :69 / :73 / :206; aether :92 WARN / :93 / :97 / :177  exit 0
C20 git show R:.ufo/waves/round-18/w1/CarrierRecipeAudit.md | grep -c -i nethttp  -> 0  exit 1
    git show R:(same) | grep -n 'all 8 carriers byte-identical'          -> 11  exit 0
    git show R:.ufo/waves/round-18/evidence/carrier-buildinfo.json | python3 -I -B -c '<keys>'  -> 8 labels, no nethttp  exit 0
C21 git show R:corpus/knowledge/2026-10-20-r18-swiss-map-replay.md | grep -n -E '12 deterministic|two rebuilds byte-identical'  -> 44, 47  exit 0
C22 git show R:.ufo/waves/round-18/predictions/swiss-misread/s1246-swiss-nethttp.json | python3 -I -B -c '<strings with Header|Values>'  -> *textproto.MIMEHeader, *url.Values only  exit 0
C23 git show R:corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md | grep -c -E 'swiss-map-replay|r18-swiss|replayed'  -> 0  exit 1
C24 git show R:corpus/lessons/round-18.md | awk -F'|' '/^\| [0-9] \|/ {...captured-by...}'  -> rows 4,6,8 "none"; row 5 "none (PROTOCOL row fields) / QUALITY #4"  exit 0
C25 git show R:corpus/QUALITY.md | grep -c 'round-18.md'                 -> 1  exit 0
C26 git show R:corpus/lessons/round-18.md | grep -n '^Pending'           -> 47  exit 0
C29 cd ~/.local/share/kaidoku-r18/carriers && git -C <lane> show R:.ufo/waves/round-18/carriers/SHA256SUMS | sha256sum -c -  -> 12x OK  exit 0
C30 git log -1 --format='author=%aI committer=%cI' eb6c266               -> committer 2026-10-20T13:23:55-03:00  exit 0
    git merge-base --is-ancestor eb6c266 R                               -> exit 0;  git show eb6c266:.ufo/waves/round-18/carriers/SHA256SUMS | wc -l -> 12
C31 git show R:corpus/SOURCES.md | awk -F'|' '$2 ~ /S036/ {print $12}'   -> corpus/lessons/round-18.md, SKILL.md  exit 0
V16 git show R:.ufo/waves/round-18/evidence/validate16/summary.json | python3 -I -B -c '<count>'  -> 8 receipts; 8 exit 0; 2728 checks  exit 0
S035 sed -n 22p ~/.local/opt/go-1.25.0/src/internal/abi/map_select_swiss.go  -> "type mapType = SwissMapType"  exit 0
     sed -n 358,361p ~/.local/opt/go-1.25.0/src/internal/abi/type.go   -> "case Map: type u struct { mapType; u UncommonType"  exit 0
S034 curl -sL --max-time 25 https://go.dev/doc/go1.24 -o /tmp/kr18tv-go124.html  -> exit 0; sed -n 571,573p -> opt-out sentence verbatim; sha256 d35c2d52a864b3474451e28fb89bae013edba4adcc1fa7164796267c0e4ec4e7 (= S034 row)
go125 curl -sL --max-time 25 https://go.dev/doc/go1.25 -o /tmp/kr18tv-go125.html  -> exit 0; grep -o -i swiss | wc -l -> 0; grep -o -i noswissmap | wc -l -> 0; rm -f both -> exit 0
```

## Bounds

- **Writes:** this report only. Two transient curl downloads, `/tmp/kr18tv-go124.html` and `/tmp/kr18tv-go125.html`, were created outside the lane and the fleet repo and then removed (`rm` exit 0).
- **Validators:** run in the worktree only after confirming HEAD = `refs/heads/main` = REV, an empty `git diff --stat REV` and no untracked files for the runs and tools paths. `receipt-validate.py` writes only under `--selftest`, which I did not use.
- **Not done:** no REA or Ghidra run, no carrier executed, no jj, no git write, no subagent. No tools installed or upgraded.
