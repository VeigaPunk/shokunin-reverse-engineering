# CriticC1Admission — is C1 discharged, or only satisfied by markers? (round 17, w2)

Seat: author-side advisory critic (not an outside reviewer). This was a read-only attack on lane revision `da64646adcb19c1ede7537b799b8c7d283fe43da` (baseline `b563c79`). The only file written in the lane is this report. Scratch work went to a `/tmp` git clone, which has been removed. No installs. No REA, Ghidra or carrier execution. Python was always run with `-B`.

Axes: **calibration** (do the stated claims match their evidence?) and **depth** (strongest counterexample).

## Verdict

| Part | Status at `da64646` |
|---|---|
| R16-PROVENANCE, lane sites | **Discharged.** The 4 baseline sites have 4 line-exact corrections. |
| R16-PROVENANCE, route as a whole | **Not discharged.** The fleet-report site is still open and no instrument can see it. The round's own replacement tool repeats the defect pattern (F1). |
| R16-INVOCATION | **Not discharged.** `unlabelled_variant` went 2 → **11**. custody-pair still depends on a receipt that does not exist. The claimed "M → 0" cannot be shown inside a single verification pass. |
| QUALITY #19 | **Adds a real criterion** beyond #18 (records at two named instants). However, its first and second sentences contradict each other, and the only metric for it is a presence marker. |

## Findings

### F1 — HIGH (calibration). The round's own pin tool claims "pre/mid/post maps with timestamps", but mid-run records are never kept

Anchors:
- `corpus/lessons/round-17.md:26` says "pins equal pre/mid/post".
- `corpus/lessons/round-17.md:73` says "`tools/pins.py` (pre, 30 s mid-run and post maps with timestamps)".
- `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:27-29` says "hashed before, every 30 s during, and after … no mid-run check differed".

What the code does, `.ufo/waves/round-17/tools/carrier-run.py`:
- The mid-run check runs at `:422-433`. When the maps are equal it discards the mid map, its timestamp and the check count. It writes the key `pins_changed_during_run` only when the maps differ.
- The exit decision at `:376-383` looks at `pins_cmp` (pre/post) only. A mid-run change that is reverted before post still exits 0.
- The carrier-run selftest has 2 cases (`w2/.st-carrier-run.py.out`: `SELFTEST: CLEAN cases=2`), and `grep pins_changed_during_run` finds only `:430`. So the mid-run red branch has no test, and `receipt-validate.py` never reads it.

Command:
```
python3 -B -c "...for f in glob('.ufo/waves/round-17/runs/*/receipt.json'): print(label, 'mid' in text, 'pins_changed_during_run' in text, analyze start/end, polls)"
```
Output (all 8):
```
calib-shfmt mid_in_text= False False analyze 13:47:06.688→13:47:37.309 polls 61
pro-op     mid_in_text= False False analyze 13:55:56.407→14:00:05.228 polls 496
… (8/8 False False)
```
`pro-op` receipt keys are `pins_pre`, `pins_post` and `pins_compare`. Each map has `taken_at_utc`. There is no mid map anywhere.

So "no mid-run check differed" is inferred from a key being absent. That is the same "boolean with no records at named instants" pattern that R16-PROVENANCE corrected, and it fails #19 (`corpus/QUALITY.md:29`: "records at named instants … each snapshot's UTC timestamp"). The pre/post half is genuine; the mid half is not.

Smallest fix, either one:
- **(a)** In `_run_polled`, append `{taken_at_utc, monotonic_ns, equal, changed}` for every mid check to `rec["pins_mid"]` and fold mid inequality into exit 1.
- **(b)** Without new runs: add a named append-only correction to the three sentences above saying "mid-run checks unrecorded; only pre/post instants evidenced", and reword lesson :73.

### F2 — HIGH (calibration). R16-INVOCATION is not discharged at the integrated revision; the "M → 0" metric got worse

Claim: `claims.json:13` says "invocation-audit.py: unlabelled-variant registry rows M -> 0". `corpus/lessons/round-17.md:74` says both rows were "re-exercised this round with retained argv".

Command:
```
python3 -I -B .ufo/waves/round-17/tools/invocation-audit.py --root <lane> --rev <rev>
```
Output:
```
b563c79: {'exercised_match': 5, 'unlabelled_variant': 2, 'rows': 7}   citation-drift, custody-pair
da64646: {'exercised_match': 6, 'unlabelled_variant': 11, 'rows': 17}
  citation-drift exercised_match .ufo/waves/round-16/verification.json
  custody-pair  unlabelled_variant None
  go-carrier-run … round17-structural-controls: unlabelled_variant (10 new r17 rows)
```

- `git cat-file -e da64646:.ufo/waves/round-17/verification.json` returns "does not exist".
- Yet `SKILL.md:449` (custody-pair) and `SKILL.md:448` (citation-drift) both cite `.ufo/waves/round-17/verification.json` as the exercised receipt. These are forward references to a file that does not exist.
- citation-drift matches only the **round-16** receipt. The claim says (`claims.json:12` (b)) "re-exercised … and the receipt retained". At `da64646` that has not happened.
- The round's 10 new rows (`SKILL.md:532-541`) bring back the R16-INVOCATION class in the round that claims to close it.

Specific case, go-carrier-run:
- `SKILL.md:532` advertises `bash …/run-carriers.sh <LABEL>`.
- No receipt records any `run-carriers.sh` argv. `runs/run-log.txt` shows one back-to-back sequence of all 8 labels, which suggests the script was run without a label (an inference, not observed).
- `run-carriers.sh` has also changed in the worktree since `da64646` (`out="${RUNS_DIR:-runs}/$label"`, which is uncommitted). The script that produced the receipts is therefore not the one in the worktree.

Smallest fix:
- Measure M at the final revision; do not assert it.
- For any row with no receipt yet, the route explicitly allows "explicitly distinguish intended vs exercised" (`round-16-verifier-spotcheck.md:184`). Label it `unexercised` (the audit class `labelled_unexercised`) instead of pointing it at a future file.

### F3 — MEDIUM-HIGH (depth). "M → 0" cannot be shown in one post-integration pass, and a self-written receipt passes the audit

**Ordering problem.**
- invocation-audit reads Git objects only (`contract.md:81`).
- The custody-pair row's receipt is the round-17 `verification.json`.
- Any audit recorded inside that `verification.json` was necessarily run at an earlier revision, where the file was absent. So the recorded value has to be M ≥ 1.
- `LOG.md:2066-2067` plans only "the single post-integration execution pass". An after-receipt measurement needs a second commit and a re-run (for example in `final-recheck.json`), or an outside run.

**The audit counts any JSON array named `argv`, whether or not it ran** (`contract.md:84-86`). Test in a `/tmp` clone at `da64646`:
- I added `.ufo/waves/round-17/verification.json` = `{"note":"forged: no stdout, no exit, never executed","commands":[{"argv":["python3","-I","<abs>/custody-pair.py","capture","--out","<receipt>"]}]}`. Note that `<receipt>` here is the literal placeholder copied from the row.
- Output: `custody-pair exercised_match .ufo/waves/round-17/verification.json`.
- A receipt copied from the row is enough to satisfy the row. This is the "marker-satisfied" risk in its plainest form.

**An honest re-run with `-B` does not match.** Seats are required to use `-B`. The w2 artifact `w2/citation-drift-head.json` ran `python3 -I -B …citation-drift-probe.py … --strict`. The rows advertise `python3 -I` with no `-B`, and the audit deliberately keeps `-B` as a variant (`SKILL.md:539`). With both argv forms placed in a clone receipt:
```
citation-drift exercised_match .ufo/waves/round-16/verification.json   (r17 run does not match its own row)
custody-pair  unlabelled_variant None
```

Smallest fix:
- Count an argv only if it sits inside a `retain.py`-shaped record (`exit` int, `stdout_path` and `stdout_sha256` that recompute). `receipt-validate.py` already recomputes these.
- Run custody-pair and citation-drift under `retain.py` with exactly the advertised flags, or add `-B` to both rows.
- Record the audit at the receipt-bearing revision in a separate final-recheck.

### F4 — MEDIUM (calibration). The fleet-report site stays open and cannot be measured

- Site: `/home/vgpnk/Projects/shokunin/.ufo/reports/round-16/kaidoku.md:60` (fleet commit `2d0274b`): "Producer/input hashes stayed unchanged during execution."
- Checked against the r17 `SITE_PATTERN`: `r17 SITE_PATTERN match: True`.
- This is the "report" that the routed defect names first (`round-16-verifier-spotcheck.md:183`).
- `corpus/lessons/round-17.md:89` defers it: "its correction is carried by this round's fleet report". `.ufo/reports/round-17/` does not exist.
- `temporal-sweep.py:37-50` scans only lane-relative files under `--root` git. `--extra` is a *correction* source, not a *site* source, so no tool can ever count this site.
- `claims.json:12` limits (a) to "every lane statement", so C1(a) as written can pass. But `LOG.md:2039` and `corpus/lessons/round-17.md:8-9` say the route is "discharge[d]".

Smallest fix:
- Say "lane sites 4/4 corrected; fleet site `.ufo/reports/round-16/kaidoku.md:60` open until the round-17 fleet report carries the line".
- Give L1's final message the exact correction line (`R16-PROVENANCE: .ufo/reports/round-16/kaidoku.md:60 map matches committed source-revision blobs; temporal stability not evidenced.`) so the orchestrator can copy it verbatim.
- Keep it listed as open in the routed-defect queue.

### F5 — MEDIUM (depth). temporal-sweep reports 0 new sites while missing new overclaims

Tests in a `/tmp` clone at `da64646`, each with `--sites-rev b563c79`:
- **Lesson files are not scanned.** I appended `- pins remained unchanged during execution.` to `corpus/lessons/round-17.md`. Result: `{'corrected': 4, 'new_unqualified_at_rev': 0, …} []`. The site list (`temporal-sweep.py:37-44`) includes lessons only for `round-16.md`.
- **Marker lines are exempt.** A line containing `R16-PROVENANCE` is skipped (`:127-128`). I appended `- R16-PROVENANCE: round-17 pins remained unchanged during execution.` to `LOG.md`. Result: `new_unqualified_at_rev: 0`. The same sentence without the marker gives `new_unqualified_at_rev: 1 ['LOG.md:2069']`.
- **Narrow wording.** The r17 knowledge sentence in F1 ("every 30 s during … no mid-run check differed") does not match the pattern at `:55-58`.

Smallest fix:
- Add `corpus/lessons/` to `SITE_DIRS`.
- Exempt a marker line only if it also contains `temporal stability not evidenced`.
- State in the claim that the sweep is a wording census. Its `--help` already says so.

### F6 — LOW-MEDIUM (calibration). invocation-audit results depend on the checkout path, not only on Git objects

Same revision `da64646`, different `--root`:
```
/home/vgpnk/Projects/shokunin/kaidoku-shokunin  exercised 6 unlabelled 11  quote-fidelity exercised_match
/tmp/c1a-clone                                  exercised 5 unlabelled 12  quote-fidelity unlabelled_variant
```
`_relpath` (`invocation-audit.py:179-185`) relativizes receipt paths against the local `--root`. The round-14 receipt holds absolute `/home/vgpnk/…` paths, and the row uses relative ones. So an outside reviewer working in a fresh clone gets a different M.

Smallest fix: normalize against a recorded lane-path prefix (or any path ending in the lane's top-level layout), not against the local root. Alternatively, document that `--root` must be the canonical lane path.

### F7 — MEDIUM (calibration). QUALITY #19 adds a real criterion, but contradicts itself and is measured only by a presence marker

**Is it real beyond #18? Yes.**
- #18 (`corpus/QUALITY.md:28`) requires producer, inputs, argv and exit, and "not only unexplained booleans".
- r16's single hash map plus its producer met that. Hence the verifier admitted C1 and routed the temporal overclaim separately, and `round-17.md:73` says "captured-by: none — QUALITY #18 asks for producer and inputs, not instants".
- #19's requirement of two named instants with timestamps and a comparison is new.
- The parts about lone booleans and the correction form largely restate #18 and the K16 convention. That repetition is harmless.

**Contradiction.**
- Sentence 1 of `QUALITY.md:29`: temporal-stability claims ("unchanged during/across the run") "are admitted only with records at named instants".
- Sentence 2: "Equal maps establish identical bytes at those instants, not continuity between them".
- So, given pre/post records, is the wording "unchanged during the run" admitted? Sentence 1 says yes; sentence 2 says the evidence cannot show it. A reader can admit the very wording the row exists to stop.
- F1 shows the slide in practice: "hashed … every 30 s during" plus "no check differed" reads as continuity.

**Red-run clause.**
- The only red evidence is the pins selftest on a synthetic temp file (`w2/.st-pins.py.out`: `red case observed: compare exit 1 names /tmp/pins-selftest-…/a.txt`). That file is uncommitted at `da64646`.
- No red run covers the production branch, which is carrier-run's mid-run check (F1).

**Metric.** `measure.py:48,116-117,157` counts any line matching `^\|\s*19\s*\|`. Its own selftest passes with `| 19 | r17 rule | l | — |` (`:257,287`). "QUALITY row 19 presence 0 → 1" is therefore pure presence.

Smallest fix:
- Reword the row as: "Admissible wording is 'identical bytes at <t0> and <t1>' (named UTC instants with retained maps). 'Unchanged during/throughout' is inadmissible without continuous evidence. Every instant named, including mid-run, needs its own retained map; absence of a drift key is not a record."
- Require the red run on the instrument path that the claim uses.
- Do not report the presence check as calibration evidence.

## Checked and found sound (bounded no-finding)

- **Lane corrections.** `temporal-sweep.py --rev da64646 --sites-rev b563c79` gives `{'sites': 4, 'corrected': 4, 'unqualified': 0, 'new_unqualified_at_rev': 0}`; the baseline-on-baseline run gives `{'sites': 4, 'corrected': 0, 'unqualified': 4}`. The 4 corrections are line-exact, carry the required phrase, and are append-only (`corpus/lessons/round-17.md:85-88`, `LOG.md:2059-2062`).
- **Matcher rules.** Corrections need marker + exact `file:line` + phrase (`:164-171`). Sites are read at the baseline (`:157-163`). That closes both the w1 "path-only marker" hole and the "delete the site" hole.
- **Site list completeness.** An independent `git grep` at `b563c79` for during/across/throughout, stable and `pins_unchanged` wording, outside earlier rounds, finds no further lane site in the r16 lesson, LOG, SCORECARD or knowledge. The r16 SCORECARD section `:2294-2348` has no temporal wording, so the decision not to invent a SCORECARD correction (`round-17.md:80`) holds.
- **citation-drift row.** `SKILL.md:448` at `da64646` matches the r16 strict, isolated, absolute exercised argv, and labels the non-`--strict` probe form "unexercised". The alignment itself is real; only the r17 re-exercise claim is not (F2/F3).
- **Pre/post pins.** 8/8 receipts record `pins_pre` and `pins_post` with `taken_at_utc`, and `pins_compare.equal: true` (`pro-op`: 146 entries, 13:55:55.592Z → 14:00:05.292Z).

## Impacted axes

- Calibration: F1, F2, F4, F6, F7.
- Depth: F3, F5.

No harm was found on the frontier, freshness or adjacency axes within this scope.
