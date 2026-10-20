# ReviewQuality1920 — QUALITY rows 19–20 (falsify)

Seat: `KaidokuR17.ReviewQuality1920` (leaf, read-only). Target: `corpus/QUALITY.md:29-30` at `da64646adcb19c1ede7537b799b8c7d283fe43da`; baseline `b563c799d97774aae4351276fe43cb897311e349`. No `lsp` device is mounted in this seat; all checks are Git-object/byte/text reads, so no LSP-semantic claim is made. No installs or updates. Read-only: `git show`/`git diff`, direct text reads, and the round-17 tools `receipt-validate.py` and `temporal-sweep.py` against retained files. No REA analyze/search/decompile, no Ghidra, no carrier executed.

## New findings

### F1 (low) — row 19's quoted trigger forms omit the two canonical r16 wordings
- Anchor: `corpus/QUALITY.md:29` — `Temporal-stability claims ("unchanged during/across the run", "stable throughout") …`.
- The row's parenthetical is narrower than both the class and the lane's own matcher. `.ufo/waves/round-17/tools/temporal-sweep.py:57-60` matches `unchanged (during|across|throughout) (the )?(run|execution)|stable throughout|pins_unchanged_during_run`.
- Command/output (Python `re`, quoted forms only):
  - `Producer/fixture hashes remain unchanged across execution.` → `unchanged during/across the run` **False**, `stable throughout` **False**; sweep pattern **True** (`LOG.md:2012`).
  - `All producer/fixture pins remained unchanged during execution.` → **False/False**; sweep pattern **True** (`corpus/lessons/round-16.md:154`).
- Impact: a reader keying on the quoted shapes misses both sites; `corpus/lessons/round-17.md:75` records that the contract regex made exactly this `across execution` omission.
- Smallest fix: parenthetical → `("unchanged during/across/throughout a run or execution", "stable throughout")`.

### F2 (low) — the Gate cell row 20 cites miscites its Mistakes rows
- Anchor: `corpus/lessons/round-17.md:27` — `… #20 from this round's attribution and echo findings (Mistakes rows 3, 6)`.
- The Mistakes data rows are at `:73-81`: row 3 (`:75`) is the temporal-sweep scope finding; the echo finding is row 6 (`:78`); the attribution finding (unbound session logs) is row 7 (`:79`). Row 3 has no #20 content.
- Command/output: `awk 'NR>=69&&NR<=81{printf "%d: %s\n",NR,substr($0,1,90)}' corpus/lessons/round-17.md` → rows 73–81, with `:79` = `attribution — unbound session logs`.
- Impact: the only admission record linking #20 to its findings names the wrong row; the content still exists at `:78-79`, so grounding is not lost, only its pointer.
- Smallest fix: `(Mistakes rows 6, 7)`.

### F3 (low) — row 20's supersedes cell asserts a #9 relation the row does not contain
- Anchor: `corpus/QUALITY.md:30` cell 5 — `sharpens 5, 6, 9`; #9 is `corpus/QUALITY.md:19` (`Runtime-behavior claims … runtime-evidence provenance … never from a static graph`).
- Row 20's clauses are (a) log bound by its own bytes, (b) request-echo line is not selection evidence, (c) absence bounded by the last retained line. None concerns target runtime behavior; the closest sibling for the absence clause is #7 (examined coverage/truncation), not #9.
- Command/output (token n-gram): `row20 vs row9: max shared word-run=0`. Row 20 contains no `runtime` token.
- Smallest fix: cell 5 → `sharpens 5, 6` (or add the missing sentence "a provider log is evidence about the provider run, not target runtime" if 9 is intended).

## Peer findings independently checked (not new)

### P1 — validator rejects every carrier receipt (already reported; confirmed)
- Anchors: `.ufo/waves/round-17/tools/receipt-validate.py:98` (`isinstance(receipt.get("steps"), list)`); `.ufo/waves/round-17/tools/carrier-run.py:275,309,349` writes `steps` as a mapping; `.ufo/waves/round-17/runs/pro-aether/receipt.json` `steps` keys are `analyze`, `inspect-go-binary`.
- Command/output: `python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py .ufo/waves/round-17/runs/pro-aether/receipt.json` → `EXIT=1`; `{'invalid': 1, 'receipts': 1, 'unreadable': 0, 'valid': 0}`; `[('unknown', [{'code': 'unrecognized_shape', 'detail': 'receipt matches neither retain nor carrier shape', 'where': '$'}])]`. Same for the other seven.
- Row impact: `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:3` documents this command as the recheck for the entry row 20 cites; it returns invalid. `w1/CriticCapabilityPreclaim.md:89` required exit 0 on these receipts.
- Already reported at `w2/DraftReportR17.md:10`, `w2/DraftLessonEvidence.md:25`, `w2/ConnScorecardCapability.md:28`, `w2/CriticC2Depth.md:93`; not repeated as a new finding here.

### P2 — row 19 admits the wording it then says cannot be shown (already reported; confirmed)
- Sentence 1 of `corpus/QUALITY.md:29` admits `"unchanged during/across the run"`/`"stable throughout"` claims with records at named instants; sentence 2 says equal maps establish `identical bytes at those instants, not continuity between them`. With pre/post maps present, sentence 1 admits an interval claim sentence 2 says the evidence cannot support. Peer analysis: `w2/CriticC1Admission.md:140-160`.
- My independent check: the two sentences are adjacent in the same cell; the fallback sentence applies only `without such records`, so it does not resolve the case where the records exist.
- Smallest fix (agreeing with the peer): make the row say the admissible wording is `identical bytes at <t0> and <t1>`; `unchanged during/throughout` is inadmissible without continuous evidence. This is the blocking calibration defect in row 19.

### P3 — row 20 unrequested/outside the measure (already reported); "circular" not confirmed
- Confirmed: `.ufo/waves/round-17/claims.json:13` lists only `QUALITY row 19 presence 0 -> 1`; `.ufo/waves/round-17/measure.py:48,116-117` matches only `^\|\s*19\s*\|`. Peer reports: `w2/DraftReportR17.md:66-68`, `w2/DraftScorecardR17.md:65`. The L1 already discloses it at `w2/draft-report.md:24`.
- Not confirmed: "circular". `corpus/QUALITY.md:5-7` requires every criterion to cite the lesson that produced it; rows 16–18 cite their producing lessons/artifacts the same way. The knowledge entry is the round's evidence for the finding, not a second copy of the rule. "Unrequested/not measured" stands; "circular" should not be carried into the fleet report.

## Bounded no-findings (checked; no defect found)

- **Rows 1–18 byte-identical.** `git diff b563c799… da64646… -- corpus/QUALITY.md` → `1 file changed, 2 insertions(+)` (the two new rows). Prefix (lines 1–28, through row 18) sha256 `61e8654f3ecfd8200f21ce4f27f235e7161ba0f9d3923b04e70c828a3b0f4844` equal at both revs; suffix sha256 `d1c3c7083921e963bc9ead9e7c926c5dd18cdd5cabfd3d8f13bc2745d9c686e3` equal. Working-tree blob equals the rev blob: `ed8bc1740cbca7a32132bbc5793120426aed7920a33b25a32ea610d89950f0ff`.
- **Table shape.** Rows 19 and 20 each have 5 unescaped pipes / 4 cells (Python pipe count over all rows; row 13's 6-pipe debt is pre-existing and unchanged).
- **Grounding anchors resolve.** `corpus/lessons/round-16-verifier-spotcheck.md:183` starts the R16-PROVENANCE item; `.ufo/waves/round-16/verification.json:419` is `"pins_unchanged_during_run": true,`; `corpus/lessons/round-17.md` has `## Gate` at `:20` and `## Mistakes` at `:69`; the four named corrections are at `:85-88`.
- **Non-duplication (literal).** Longest shared word-run: row 19 vs 18/5/6 = 0; row 19 vs 9 = 4 words, `are admitted only with` (the corpus's generic admission phrase, not a rule); row 20 vs 18/5/6/9 = 0. Row 19 does not restate #18's invocation rule; row 20 does not restate #5's labelling, #6's evidence-id rule, or #9's runtime-provenance rule. Row 19's "lone hash map/boolean" sentence is the temporal instance of #18's "not only unexplained booleans", which is why the row says `sharpens 18`.
- **Row 19 is enforceable with the retained artifacts.** `pins.py` snapshots record `sha256`, `size`, `mtime_ns`, `taken_at_utc`; `compare` returns `equal/changed/missing/errors` plus pre/post UTC (`pins.py:62-106`). A Python loop over the eight `runs/*/receipt.json`: every `pins_compare.equal` is true, every `pins_pre`/`pins_post` has `taken_at_utc`, every receipt has the carrier under both pre/post (8/8). `temporal-sweep.py --rev da64646…` → `sites: 4, corrected: 4, unqualified: 0, new_unqualified_at_rev: 0`, `correction_rule: R16-PROVENANCE + exact file:line + 'temporal stability not evidenced'`. The red-run line is committed at `w1/PinsTool.md:21`: `red case observed: compare exit 1 names /tmp/pins-selftest-e8vz7xs0/a.txt` with `SELFTEST: CLEAN cases=7` / `EXIT=0`; the raw w2 `.st-pins.py.out` is not at the rev (`git cat-file -e da64646:.ufo/waves/round-17/w2/.st-pins.py.out` → 128), so the w1 transcription is the rev-retained witness.
- **Row 20's log claims are accurate and enforceable.** Installed `Base-src.zip`: `GoApiSnapshot.java:160` `Msg.warn("Falling back from %s to %s for Go API snapshot")`, `:163` `Msg.info("Using Go API snapshot for %s")`; `GoRttiMapper.java:180` `Msg.info("Using Go API snapshot for version %s")` (request echo). Across the 8 run logs + 2 pilot logs, the only `GoApiSnapshot` shapes are those INFO/WARN lines (no third shape); the no-base carriers have no `GoApiSnapshot` line and log `Missing Go bootstrap type info`. Python loop over the eight receipts: every `ghidra.log` contains `Using log file:` whose dirname equals the receipt's `session_dir`; every `IMPORTING: …/target-<prefix>.bin` prefix equals the pinned carrier sha256[:12]; every recorded log sha256 equals the recomputed file; every receipt has `bound_sessions` length 1 and `unbound_sessions` 0 (8/8).
- **Row 20's absence bound.** The retained logs end at `ANALYZING changes made by post scripts` (aether `:244`, the last line), and all Go lines precede it (`:91-93`); "absence only up to the last retained line" is the conservative form of the recorded prefix limit in the receipt (`log_capture_limit`) and `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:133`.

## Residual risk / verification gaps

- P2 (row 19's internal contradiction) is the blocking calibration defect; fix it before admitting the row into any SCORECARD justification.
- P1 blocks the documented recheck of row 20's evidence, even though the underlying logs/digests are intact and hand-checkable.
- Row 19's red-run witness is a prose transcription in `w1/PinsTool.md:21`; no raw selftest stdout/exit is committed at the rev. If #18-grade retention is wanted, commit the selftest output (the `SELFTEST: CLEAN cases=7` + red line + exit).
- Row 20 has no measure at the rev (`measure.py` matches only row 19) and no claims.json after-state; the L1 already lists it as a non-claim addition, but an integration drop would be undetected.
- I did not run `pins.py --selftest` or any carrier (the contract restricts selftests to tool executors); the red-run evidence above is the committed w1 report plus the source.

No installs/updates.
