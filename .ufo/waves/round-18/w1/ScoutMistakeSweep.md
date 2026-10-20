# ScoutMistakeSweep — candidate `## Mistakes` rows mined from round 17

Seat: `KaidokuR18.ScoutMistakeSweep` (leaf, read-only). Date: 2026-10-20.
Target file: `corpus/lessons/round-18.md` `## Mistakes` (does not exist yet; `ls corpus/lessons/` ends at `round-17.md`).
Inputs compared: the r17 fleet report `/home/vgpnk/Projects/shokunin/.ufo/reports/round-17/kaidoku.md` (referred to below as **report**),
`corpus/lessons/round-17.md` (**lesson**), `corpus/lessons/round-17-verifier-spotcheck.md` (**spotcheck**).
Class vocabulary: `CORPUS.md:171-178` (`vacuous`, `survivor`, `stale-premise`, `reference-drift`, `number-drift`, `scope`, `attribution`, `landing`, `provider`).
Every claim below is labelled **[O]** observed at the cited revision or **[I]** inference. Nothing here was executed against a carrier; no REA analyze/search/decompile and no Ghidra was run.

Revision pins: lane `HEAD` = `refs/heads/main` = `9011581d84527ba34c675f9cf912e54d2e72d470` (the spotcheck commit itself; `git rev-parse HEAD refs/heads/main`, exit 0, below). r17 freeze `271167473d87ef710f07ecdd98caf0ce12091686`; first pass `da64646adcb19c1ede7537b799b8c7d283fe43da`; second-pass producer `95e34db`; r17 verification source `d0ab299`; delivered `de6c721`. The worktree is being edited by sibling round-18 seats: at 12:29 `git status --porcelain` showed `M` on five r17 tools/gates (`compare.py`, `carrier-run.py`, `log-extract.py`, `verify.py`, `citation-drift-probe.py`) and untracked `.ufo/waves/round-18/` [O]; every r17 artifact check below reads Git objects, not the worktree.

## Command log (read-only; exact argv, exit in parentheses)

`…` below elides only a repeated directory prefix (`./.ufo/waves/round-17/runs/<label>`), never a hash or a filename; every full 40-hex revision is spelled in the revision-pins paragraph or in the command itself.

```text
$ git rev-parse HEAD refs/heads/main
9011581d84527ba34c675f9cf912e54d2e72d470
9011581d84527ba34c675f9cf912e54d2e72d470                                  (exit=0)
$ git status --porcelain | head -20
 M .ufo/waves/round-17/tools/compare.py
?? .ufo/waves/round-18/                                                    (exit=0)

$ grep -n 'R17-PINMAP\|R17-VALIDATE16\|R17-SUMS-RUNLOG\|R17-REGISTRY\|R17-S032-DIGEST' corpus/lessons/round-17.md
(no output)                                                                (exit=1)
$ grep -n 'R17-PINMAP' corpus/QUALITY.md
(no output)                                                                (exit=1)

$ git show 271167473d87ef710f07ecdd98caf0ce12091686:.ufo/waves/round-17/predictions/SHA256SUMS | grep carriers
8ac38afefb60279eaf74610c03ec3526613c109cfb2b1c8fde8eb3ff5c4d3eb5  predictions/carriers.tsv   (exit=0)
$ git show 9011581d84527ba34c675f9cf912e54d2e72d470:.ufo/waves/round-17/predictions/SHA256SUMS | grep -c carriers
0                                                                          (exit=1)
$ git rev-parse 271167473d87ef710f07ecdd98caf0ce12091686:.ufo/waves/round-17/predictions/carriers.tsv HEAD:.ufo/waves/round-17/predictions/carriers.tsv
e232bf2bdcc607bcb577d1fb788b785cc6821188
e232bf2bdcc607bcb577d1fb788b785cc6821188                                  (exit=0)
$ sha256sum .ufo/waves/round-17/predictions/carriers.tsv
8ac38afefb60279eaf74610c03ec3526613c109cfb2b1c8fde8eb3ff5c4d3eb5  .../carriers.tsv   (exit=0)

$ python3 -c "…print([c['label'] for c in d['commands'] if 'receipt-validate' in c['label']])"
['selftest-receipt-validate', 'receipt-validate-calib-shfmt', 'receipt-validate-calib-esbuild-0.25.12',
 'receipt-validate-pro-notesmd-cli', 'receipt-validate-pro-aether', 'receipt-validate-pro-esbuild-0.21.5',
 'receipt-validate-pro-containerd-shim', 'receipt-validate-pro-esbuild-0.27.7', 'receipt-validate-pro-op']  (exit=0)
  -> 8 receipt runs on A receipts + 1 selftest; 0 runs on the 8 `da64646` receipts.

$ git show HEAD:.ufo/waves/round-17/runs/pro-aether/receipt.json | python3 -c "…print(pin_checks[0]); print('binding' in d,'md5_pre' in d['carrier'])"
{"changed": [], "entries": 146, "equal": true, "missing": [], "taken_at_utc": "2026-10-20T14:30:47.790881+00:00"}
False False                                                                (exit=0)
$ git show da64646:…/runs/pro-aether/receipt.json | python3 -c "…print('pin_checks' in analyze, list(carrier))"
False ['path', 'sha256_post', 'sha256_pre']                                (exit=0)

$ git show 95e34db:.ufo/waves/round-17/tools/carrier-run.py | grep -c 'md5_pre'
0                                                                          (exit=1)
$ git show d0ab299:.ufo/waves/round-17/tools/carrier-run.py | grep -n 'md5_pre' | head -3
344:        receipt["carrier"]["md5_pre"] = _md5.hexdigest()
396:                                      receipt["carrier"].get("md5_pre"))   (exit=0)

$ grep -c 'Write scope:' SKILL.md
0                                                                          (exit=1)
$ git show 9011581…:SKILL.md | grep -c 'Write scope:'
0                                                                          (exit=1)

$ git show da64646:…/runs/run-log.txt | grep -c ' start '
7                                                                          (exit=0)
$ git show da64646:…/runs/run-log.txt | tail -1
== pro-op end 2026-10-20T11:00:05-03:00 carrier-run=0 compare=0               (exit=0)
$ git show 9011581d84527ba34c675f9cf912e54d2e72d470:.ufo/waves/round-17/runs/run-log.txt | grep -c ' start '
8                                                                          (exit=0)
$ git show 9011581d84527ba34c675f9cf912e54d2e72d470:.ufo/waves/round-17/runs/run-log.txt | tail -1
run-carriers exit=0                                                        (exit=0)
$ git show 9011581d84527ba34c675f9cf912e54d2e72d470:.ufo/waves/round-17/runs/run-log.txt | grep -c calib-shfmt
2                                                                          (exit=0)
$ git show da64646adcb19c1ede7537b799b8c7d283fe43da:.ufo/waves/round-17/runs/run-log.txt | grep -c calib-shfmt
0                                                                          (exit=1)
$ git show 9011581d84527ba34c675f9cf912e54d2e72d470:corpus/SOURCES.md | grep -c 'fetch-time'
0                                                                          (exit=1)
$ git show 9011581d84527ba34c675f9cf912e54d2e72d470:SKILL.md | sed -n '448p' | cut -c1-40
| citation-drift | probe / kaidoku | …                                     (exit=0)
$ grep -o '"model"' .ufo/waves/round-17/wave-outcomes.json | wc -l
0                                                                          (exit=0)
$ grep -o 'm_swe\|m_opus\|m_sol\|m_flash\|m_haiku' .ufo/waves/round-17/wave-outcomes.json | sort | uniq -c
      2 m_swe                                                              (exit=0)
$ git show d0ab299:.ufo/waves/round-17/runs/run-log.txt | wc -l
18                                                                         (exit=0)
$ git show d0ab299:.ufo/waves/round-17/runs/run-log.txt | grep -c ' start '
8                                                                          (exit=0)
$ git log --format='%h %ad %s' --date=iso -3 -- .ufo/waves/round-17/runs/run-log.txt
d0ab299 2026-10-20 11:47:24 -0300 round-17: w2 integration … (source revision)
da64646 2026-10-20 11:06:06 -0300 round-17: carrier runs … (pre-falsify)     (exit=0)

$ git show 9011581…:corpus/SOURCES.md | grep -c '436c0f63'
1                                                                          (exit=0)
$ git show 9011581…:corpus/QUALITY.md | grep -n '^| 19 \|^| 20 '
29:| 19 | A temporal-stability statement … | 30:| 20 | A provider-log observation …   (exit=0)
```

Tool installs/updates: **none**. No pacman transaction; no network fetch; no host file outside the report path was written.

## Candidate rows (primary: each is a disagreement between the lane's own texts and the outside check)

| # | class | disagreement, with the two sides | evidence pointer | captured-by | fix the row must carry (round-18 discharge; red-before) |
|---|---|---|---|---|---|
| M1 | `vacuous` | The entry says every mid-run pin **map** is retained and "All maps are equal"; the receipt retains a comparator **verdict** (`equal`, `entries`, `changed`, `missing`), not the map. Spotcheck records the partial disagreement. | Lane: `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:30-32` [O]; `SCORECARD.md:2374` "pre/mid/post pin maps with instants" [O]; `report:35` "mid-run pin checks retained" [O]. Outside: `round-17-verifier-spotcheck.md:108` (partial disagree), `:137` [O]. Artifact: `runs/pro-aether/receipt.json` `pin_checks[0]` = verdict dict at 9011581 [O]; producer `d0ab299:.ufo/waves/round-17/tools/carrier-run.py:481-486` writes exactly those five keys [O]. | `19` — the row added this round requires "each pin map (per-path SHA-256 and size) with its UTC timestamp … including mid-run checks" (`QUALITY.md:29`); the round's own texts violate it. `18` does not cover instants (`round-17.md:81`). | Contract `R17-PINMAP` (`contract.md:29-32`) + `carrier-run.py` `map_path`/`map_sha256` (`contract.md:127-130`) + the spotcheck's correction sentence. Red-before: at 9011581 `grep -c map_sha256` on the r17 tool = 0 and `routed-defects.py --strict` exits 1 [I from contract]. Caveat [I]: check (d) is a literal, so only the validator selftest proves the mid map is written. |
| M2 | `number-drift` | Lane counts 16 validated receipts; only 8 validator runs are retained, all on A, none on `da64646`. The fleet report already says 8/8, so the lane's own documents disagree with each other. | Lane: `SCORECARD.md:2364` "all 16 receipts `receipt-validate.py` exit 0" [O]; `corpus/lessons/round-17.md:122` "All 16 receipts pass the final validator" and `:88` "all 16 receipts were validated" [O]; `report:62` "8/8 receipts valid" [O]. Outside: `round-17-verifier-spotcheck.md:71`, `:138` [O]. Artifact: `verification.json` has 8 `receipt-validate-*` labels on `calib-*`/`pro-*` (A) [O]. | `18` — execution evidence retains producing argv/measured revision/exit (`QUALITY.md:28`); 8 claimed executions have no retained run. Not a complete fit: #18 does not require one record per claimed receipt. | Contract `R17-VALIDATE16` (`contract.md:33-35`): a `evidence/validate16/summary.json` at `rev=da64646` with exactly 8 receipts carrying an int exit. Red-before: that file is absent at 9011581, so the check is open and `--strict` exits 1 [I from contract exit table]. |
| M3 | `attribution` | "Measured source revision" S=`d0ab299` is applied to second-pass receipts produced by `95e34db` tooling; those receipts lack the fields S added. | Lane: `round-17.md:122` names `d0ab299` and "the second pass started at `95e34db`" in one sentence [O]; Gate row "Every receipt has one session bound by whole log records plus the full carrier MD5" (`round-17.md:30`) [O]. Outside: `round-17-verifier-spotcheck.md:73`, `:139` [O]. Artifact: `carrier-run.py` at `95e34db` has no `md5_pre` (`grep -c` = 0, exit 1) [O]; at `d0ab299` it does (`:344`, `:396`) [O]; the A receipt has `'binding' in d` = False and `'md5_pre' in carrier` = False [O]. | `18` — "measured revision" is exactly the field that must name the producer. | Contract `R17-PRODUCER-REV` (`contract.md:36-37`): SCORECARD and the r17 entry each name the producing revision per pass with two distinct 40-hex hashes. Red-before: the entry and SCORECARD at 9011581 carry no `R17-PRODUCER-REV` line [O, grep above]. |
| M4 | `scope` (a) / `number-drift` (b) | (a) The frozen manifest lost the `carriers.tsv` line between freeze and delivery while the file itself is byte-identical; the freeze no longer covers one of its own inputs. (b) The pass-1 run log lists 7/8 carriers. | (a) `2711674:.ufo/waves/round-17/predictions/SHA256SUMS:5` has `8ac38afe… carriers.tsv` [O]; at 9011581 `grep -c carriers` = 0 (exit 1) [O]; blob `e232bf2…` identical at both revisions [O]. (b) `da64646:.ufo/waves/round-17/runs/run-log.txt` = 14 lines, 7 ` start `, `calib-shfmt` count 0 (exit 1), no aggregate `run-carriers exit=0` line (last line is the `pro-op` per-run `end … carrier-run=0 compare=0`) [O]. Outside: `round-17-verifier-spotcheck.md:74-75`, `:140-143` [O]. | `none` — no QUALITY row requires a frozen manifest to cover every frozen file, and the missing line is invisible to a Git-object no-harm control because the manifest itself changed. | Contract `R17-SUMS-RUNLOG` (`contract.md:38-40`) restores the line with the blob's sha; the `7/8` fact goes in LOG. Red-before: the line is absent at 9011581 (exit 1) [O]. [I] The contract check does not address the run-log; that is M8. |
| M5 | `reference-drift` / `survivor` | The r16-invocation fix is incomplete: the citation-drift row is registered as `probe` while its registered argv is the `--strict` gate form (can exit 1); four new r17 rows omit the protocol row fields. | Lane: `round-17.md:82` claims both rows "now advertise the isolated absolute argv that the round-17 verification pass exercised" [O]; `SKILL.md:448` second cell `probe / kaidoku` with an argv ending `--strict` [O]; `SKILL.md:540-542,545` have 5th cells but no `Write scope:` [O]; `grep -c 'Write scope:' SKILL.md` = 0 at 9011581 (exit 1) [O]. Outside: `round-17-verifier-spotcheck.md:144-146` [O]. | `none` — the missing fields are a PROTOCOL §Gate standard-row rule, not a QUALITY row; #18's "discoverable from its existing gate registry row" is adjacent for the pinned-value path but does not grade the kind mismatch. | Contract `R17-REGISTRY` (`contract.md:41-43`): four named rows gain a 5th cell containing `Write scope:`, and the citation-drift 2nd cell starts with `gate`. Red-before: the two greps return 0 / the row still says `probe` [O]. |
| M6 | `reference-drift` | S032 pins a page SHA-256 that does not reproduce; GitHub HTML is dynamic, so the digest is a fetch-time artifact presented as a stable citation. | Lane: `corpus/SOURCES.md:38` anchor cell ends `page sha256 436c0f63…` [O]. Outside: `round-17-verifier-spotcheck.md:147` (two fetches `028dbb7d…`, `f3841de0…`) [O]. | `none` — #1 requires a resolvable source (the URL resolves); #17 excludes rendered markup from machine-gradeable input but grades quotes, not page digests. | Contract `R17-S032-DIGEST` (`contract.md:44-45`): the teaches cell starts `supersedes S032 —`, the anchor contains `fetch-time`. Red-before: at 9011581 the anchor has no `fetch-time` (`grep -c` = 0, exit 1) and the teaches cell begins `Candidate mechanism…` (`SOURCES.md:38`) [O]. |
| M7 | `survivor` | The lane's close-out claims the round's own overclaims were found by w2 and fixed before close; the outside check found the same class still in the entry and SCORECARD, and none of the six routed defects appears in the 12-row table. | Lane: `report:88` "The round's own overclaims were found by w2 and fixed before close: the mid-run pin sentence…" [O]; `round-17.md:77-92` 12 rows, no `R17-*` id (`grep` exit 1) [O]. Outside: `round-17-verifier-spotcheck.md:108`, `:131` ("the one partial disagreement … is routed here as a lesson for the next round"), `:137`-`:147` [O]. | `none` — no QUALITY row grades a closure's self-verdict; #19 catches the specific sentence, not the meta-claim. | Not covered by C1 as declared (`claims.json:12` lists only the six). [I] Candidate: the Gate should say which overclaims were found by which wave and which only outside, and one row per outside disagreement. Red-before: the `R17-*` grep over the r17 lesson exits 1. |

## Secondary candidates (observed; the outside check did not route them)

| # | class | observation | evidence pointer | captured-by | fix / confidence |
|---|---|---|---|---|---|
| M8 | `landing` / `attribution` | The pass-1 aggregate run log was **replaced** at the same path by the pass-2 log; the path no longer identifies its pass. | `da64646` blob = 14 lines, 7 starts, no `calib-shfmt`, no `run-carriers exit=0` [O]; `d0ab299` and 9011581 path = 18 lines, 8 start/end, first line `started 2026-10-20T11:27:41-03:00`, last `run-carriers exit=0` [O]; `git log -- run-log.txt` shows the replacement at `d0ab299` 11:47:24 -0300 [O]. | `none` — #18 does not require a unique path per producing revision. | Name the pass (`run-log.pass1.txt`) or keep the log under the pass directory. Confidence: medium; [I] the overwrite may be intentional and pass-1 receipts are retained per label, so only the aggregate log is at issue. |
| M9 | `attribution` | The report assigns models per seat (`executor14 (m_swe)`, `simplifier2 (m_flash)`, `scribe10 (m_haiku)`, `critic6 and sentinel2 (m_opus, 8 ≤ 10)`); no retained lane dossier carries a `model` field, and the outside check notes the task keys are agent/name/task only. | Lane: `report:101-102` [O]. Artifact: `grep -o '"model"'` = 0 in `wave1-spec.json`, `wave1-registration.json`, `wave2-spec.json`, `wave1-dispatch.json`, `wave2-dispatch.json` [O]; `wave-outcomes.json` has `"model"` count 0 and `role` only per member; `m_swe` appears 2× only in the W2 error text [O]. Outside: `round-17-verifier-spotcheck.md:91` [O]. | `none` — QUALITY #8 pins tool/provider versions, not seat models. | Either cite the spawn record or label the parenthetical "orchestrator-side, not retained". Confidence: medium; [I] the routing fact may be true, the defect is the unretained pointer. |

## Not lane debt (do not add to the lane's `## Mistakes` without an L1 ruling)

| item | class | evidence | captured-by | owner |
|---|---|---|---|---|
| Template body lacks the child-lane write-scope item although `PROTOCOL.md:103-104` says it embeds all five; it arrives only via the hyaku addendum. | `reference-drift` | `round-17-verifier-spotcheck.md:47`, `:149` [O]; `report` cites the prompt at `:241-243` [O]. | `none` (fleet protocol) | operator/protocol |
| Go 1.27.3 install record does not say why pacman was bypassed; installed to `~/.local/opt` rather than `~/.local/bin`. | `scope` | `round-17-verifier-spotcheck.md:93`, `:149` [O]; `round-17.md:135-141` [O]. | `none` (host tooling directive) | host/operator |

## Considered and deliberately not counted

- **"79 commands, all with expected exits"** (`report:38`) vs 78 numeric expectations + `custody-capture` with `expected: null` (`round-17-verifier-spotcheck.md:59`). [O] The spotcheck calls the null "by construction", so this is loose wording, not a false claim. If the L1 wants it strict, class `vacuous`, captured-by `18`, evidence `verification.json` `custody-capture.expected = null`.
- **Aether Evidence-ID falsification** (`string_count 29118 → 29117`): the expectation was frozen before the run and reported falsified (`report:66`, spotcheck `:67`). [O] Honest miss, not a mistake; no row.
- **Retained-log hash check is a sample (4 per pass)**: the spotcheck says "8 of 8 sampled" and does not claim all 16 were re-hashed (`:64`). [O] No overclaim to mine.

## What the outside check did not dispute (calibration guard)

[O] 10/10 source/reject decisions agreed, including the S028 reject and the range-check reject (`round-17-verifier-spotcheck.md:131`); routes re-derived 8/8 per pass (`:66`); 16 run-bound logs all reach `REPORT: Analysis succeeded` (`:64`); no-harm tallies (15123 identical blobs, 7 modified, 0 deleted; `:79`); wave counts 78/78 and 67/69 (`:90-91`). The sweep therefore does not re-open calibration or depth; it mines only the six routed defects plus the meta-claim they falsify.

## Remaining unknowns

- **U1** [I] Whether the six routed defects become one QUALITY #21 row (C1's check requires one row whose why-cell contains `round-17-verifier-spotcheck.md` and `R17-PINMAP`) or several; the six have four different classes (`vacuous`, `number-drift`, `attribution`, `reference-drift`, `scope`) and one row cannot grade all of them.
- **U2** [I] Whether the fixed `carrier-run.py` mid-map retention is exercised by a round-18 carrier run or only by `receipt-validate.py --selftest`; the contract's `R17-PINMAP` check (d) is a literal, so the row's fix should cite the selftest case, not the literal, as its behavioural evidence.
- **U3** [O] No copy of the pass-1 aggregate run log exists in the lane tree outside Git history; only the `da64646` blob. Whether a w2 seat retained one elsewhere was not searched (out of this seat's file scope).
- **U4** [I] The per-seat model routing is not recoverable from lane artifacts; only the orchestrator's spawn record could settle M9.
