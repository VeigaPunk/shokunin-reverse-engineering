# C3 outcome — t1250-gofmt (raw ghidra.log vs frozen prediction)

Seat: KaidokuR19.OutcomeGofmt-3 (wave 2, read-only scout). No delegation, no production
edits, no REA/MCP device, no carrier execution, no installs.

- Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` (read-only).
- Observed main tip: `d0690fd44f46d8a7fe9da5f01c6be723d12abd41` (`git rev-parse refs/heads/main`, exit 0).
- C3 freeze commit: `a1140e76fffdc1be032d9d813dbb686157803bbc`; contract baseline
  `8a8da7e19375aadc66c6bcbff0bbcbb596048fb0`.
- Scope: `.ufo/waves/round-19/runs/t1250-gofmt/` (retained log + observation) against
  `.ufo/waves/round-19/predictions/t1250-gofmt.prediction.json` and
  `predictions/decision-rule.json`. Binding-gate receipt validation is the BindingGofmt seat's
  job and was not repeated here.

## Verdict

- **Automated comparison: exact match, 8/8 fields, exit 0** [OBSERVATION]. The retained
  `compare.json` records `"all_match": true`; rerunning compare.py against the frozen
  prediction and the retained observation produced the same eight field records and exit 0.
- **Raw log is silent in the frozen failure class** [OBSERVATION]: zero `Go analysis failure`
  records, zero `Invalid index:` lines, zero `Unable to read past EOF:` pairs, zero `ERROR`
  records. The only warnings are four `GoTypeManager` "Failed to get subtype" lines
  (`ghidra.log:128-131`).
- **GoApiSnapshot route is `info` for `1.25.0`** [OBSERVATION], matching
  `prediction.expected.snapshot_route` (`t1250-gofmt.prediction.json:40`); no fallback record,
  no `Untested Go version`, no missing-bootstrap record.
- **The frozen mechanism rule holds for this label** [OBSERVATION applied to the rule text]:
  t1250-gofmt is non-D (`decision-rule.json:42 "d": false`), and the rule's non-D conjunct —
  "every non-D label shows no Go analysis failure" (`decision-rule.json:5`) — is satisfied.
  The refutation clause "a non-D label fails" (`:28`) is not triggered. This seat does **not**
  adjudicate the D clause (t1250-vet) or the overall C3 verdict.
- **Ordering holds by blob ancestry, not by author timestamps** [OBSERVATION + INFERENCE]:
  the prediction blob is byte-identical at `a1140e7` and in the worktree, and `a1140e7` is an
  ancestor of the commit that first retains this log. One evidence-integrity caveat is recorded
  in §5: the log's adding commit has an author date earlier than the log's own timestamps.
- **One divergence, non-refuting** [OBSERVATION + INFERENCE]: the emulator's synthetic full
  walk fails at index `5730496` under both H0 and H1, but Ghidra logs no failure at that index
  (or anywhere). The frozen rule's failure class is the map-path Invalid-index/EOF report, so
  this is not a prediction mismatch; it means the log cannot corroborate the walk record.

## 1. Raw log facts and anchors

Path: `.ufo/waves/round-19/runs/t1250-gofmt/logs/rea-ghidra-kDM6dB/ghidra.log`
(19119 bytes, 182 lines, final byte `10`, sha256
`6fbfca76994019c5387ae2384ef65bee8321715251eb0a6d56f85411317f7066`).

| line | level/component | record |
|---|---|---|
| 2 | LoggingInitialization | `Using log file: /tmp/kr17-rea-haesrlku/rea-ghidra-kDM6dB/ghidra.log` |
| 46 | HeadlessAnalyzer | `IMPORTING: file:///tmp/kr17-rea-haesrlku/rea-ghidra-kDM6dB/target-2aa4122abbd1.bin` |
| 118 | HeadlessAnalyzer | `ANALYZING all memory and code: …target-2aa4122abbd1.bin` |
| 122 | GoRttiMapper | `Reading Go binary info: target-2aa4122abbd1.bin` |
| 123 | **GoApiSnapshot** | `Using Go API snapshot for 1.25.0` (INFO) |
| 124 | GoRttiMapper | `Using Go API snapshot for version 1.25.0` (INFO; request echo) |
| 125 | GoTypeManager | `Discovered 23 unindexed Go types` |
| 126 | GoTypeManager | `Found 1458 Go types` |
| 127 | GolangSymbolAnalyzer | `Go version 1.25.0` |
| 128-131 | GoTypeManager | 4 × `WARN … Failed to get subtype '…' in *…` |
| 132-142 | Golang analyzers/fixups | NoReturn 4; 1337 snapshot + 470 method signatures; RTTI fixup 1252/1227/0; closures 25/5; `Go strings found: 2026`; `Go missing type names: 5` |
| 176 | HeadlessAnalyzer | `REPORT: Analysis succeeded for file: file:///…/target-2aa4122abbd1.bin` |
| 143-173 | AutoAnalysisManager | analysis timing table; `Total Time   25 secs` at `:173` |

Marker counts over the whole file (raw-line scans, the same scope log-extract.py uses):

```
$ grep -c -F 'Go analysis failure' <log>        -> 0 (grep exit 1)
$ grep -n -F 'Invalid index' <log>              -> no lines (grep exit 1)
$ grep -n -F 'EOF' <log>                        -> no lines (grep exit 1)
$ grep -n -E 'ERROR|SEVERE|Exception|Caused by' <log> -> no lines (grep exit 1)
$ grep -c -E 'WARN ' <log>                      -> 4
$ grep -n -F 'Untested' <log>                   -> no line (exit 1)
$ grep -n -E '\(GoApiSnapshot\)|Falling back|Missing Go bootstrap' <log>
123:2026-10-20 16:00:04 INFO  (GoApiSnapshot) Using Go API snapshot for 1.25.0
```

The analysis-completion evidence is not just the absence of a marker: the Go background
fixups ran at 16:00:23-16:00:30 (`ghidra.log:138-142`) and the headless analyzer reports
`Analysis succeeded` at `:176`. "Silent" here is post-analysis silence, not a truncated log.

## 2. Frozen prediction (unchanged from the freeze commit)

`predictions/t1250-gofmt.prediction.json` (sha256
`f946efe245464b55dbe417a134effb2a597eb0a93bcc8fbc663f88a9dc5869de`, also listed at
`predictions/SHA256SUMS:8`):

- carrier sha256 `2aa4122a…40a80` (`:34`) = installed `gofmt` bytes (re-hashed, exit 0).
- `expected`: label `1.25.0`, route `info`, fallback `null`, missing_bootstrap `false`,
  untested_version `null` (`:37-43`).
- `extra_expectations`: analyzer_errors_empty `true`, eof_reads `[]`, invalid_index_reads `[]`
  (`:44-46`).
- `c3` (`:15-31`): `h1_kind "none"` (`:25`), `h0_map_path_failure false` (`:20`),
  `h1_map_path_failure false` (`:26`), `misread_map_types 1` (`:28`), `true_kind "swiss"`
  (`:29`).
- Decision-rule table row (`decision-rule.json:41-51`): `d:false`, `route:"info"`,
  `h1:"none"`, `invalid_index_reads_h1:[]`, `invalid_index_reads_h0_incl_walk:[]`,
  `eof_reads_h1:[]`, `fallback_to:null`.

The frozen emulator output (`predictions/swiss-misread/t1250-gofmt.json`) has the same
map-path booleans, `misread_map_types 1`, and `true_kind_witness` = 25 `map.group[`, 0
`map.bucket[`. Independent byte read of the carrier: 25 `map.group[`, 0 `map.bucket[`, 131
`internal/runtime/maps`, 4 `SwissMap` (grep -a, read-only; no carrier executed) — the Swiss
premise is present in the artifact, not only asserted by the emulator.

## 3. Exact comparison

Retained `runs/t1250-gofmt/compare.json` (compare.exit `0`) and an independent rerun
(`python3 -I -B .ufo/waves/round-17/tools/compare.py --prediction …prediction.json
--observation …observation.json`, **exit 0**) agree field for field:

| field | predicted | observed | match | discriminating? |
|---|---|---|---|---|
| `snapshot_route` | `info` | `info` | yes | yes — GoApiSnapshot INFO at log:123 |
| `snapshot_label` | `1.25.0` | `["1.25.0"]` | yes | no (request echo; compare rule says so) |
| `fallback_to` | `null` | `[]` | yes | yes — no fallback record |
| `missing_bootstrap` | `false` | `false` | yes | yes — no bootstrap warning |
| `untested_version` | `null` | `[]` | yes | weak (contains-or-both-empty) |
| `extra.analyzer_errors_empty` | `true` | `[]` | yes | yes |
| `extra.eof_reads` | `[]` | `[]` | yes | yes (searched raw lines) |
| `extra.invalid_index_reads` | `[]` | `[]` | yes | yes (searched raw lines) |

Extraction fidelity: re-running `log-extract.py --log <retained log>` (exit 0) reproduced
`observation.json` exactly for `log_sha256`, `language_compiler`
(`x86:LE:64:default:golang`), `snapshot_route`, `snapshot_labels`, `snapshot_fallbacks`,
`go_version_logged`, `untested_versions`, `missing_bootstrap`, `analyzer_errors`,
`eof_reads`, `invalid_index_reads`, `symbol_analysis_failures` (all empty), `mapper_errors`,
`invalid_version_strings`, `classification` (`snapshot_loaded`), and all 21 `go_lines`.
The empty lists are therefore not an extractor miss; they are the log's content.

**Concurrent second pass (replication, not claim evidence)** [OBSERVATION, read at ~16:30]:
while this seat worked, an untracked `runs/pass2/t1250-gofmt/` appeared (pass-2 run-log
`16:23:58`–`16:24:29`). It uses the same carrier sha (`2aa4122a…40a80`) and independently
reproduces the outcome: `compare.exit` 0, `all_match true` on the same eight fields,
`observation.snapshot_route "info"`, and a distinct retained log
(`logs/rea-ghidra-DttY3R/ghidra.log`, sha `d3fa1232…8773`, 182 lines) with again 0
`Go analysis failure`, 0 `Invalid index`, 0 `EOF`, and `GoApiSnapshot` INFO `1.25.0` at
`:123`. The C3 count rule counts the pass-1 retained run; pass 2 is reported here only as a
replication check (and pass-2 vet was still running when observed, so no vet conclusion is
drawn).

Not compared by compare.py: `c3.h1_kind`, `c3.misread_map_types`, `c3.true_kind`,
`c3.h0/h1_map_path_failure`, and the emulator `walk` record. The decision rule is explicit
that the mechanism verdict is decided from the bound log, not from compare.json
(`decision-rule.json:4`), so the match above is a route/silence match, not by itself a
mechanism confirmation.

## 4. Frozen mechanism rule

Rule text (verbatim anchors):

- `decision-rule.json:2` — D is "map-path booleans: predicted_failure_h1 true and
  predicted_failure_h0 false".
- `:5 confirmed` — "every D label's bound ghidra.log reports a Go analysis failure whose
  Invalid index value(s) include at least one h1_only_invalid_indexes value and no index
  outside the frozen H1 list, AND every non-D label shows no Go analysis failure".
- `:20 h0_consistent` — D failure only at the both-hypotheses walk indexes.
- `:28 refuted` — "a D label shows no Go analysis failure, OR a non-D label fails, OR a D
  label fails with an index or EOF read predicted under neither hypothesis".
- `:125 unresolved` — route mismatch, unbound log, timeout.

t1250-gofmt is non-D. For this label the rule needs only "shows no Go analysis failure".
The operational failure class used by the retained tooling is
`symbol_analysis_failures` (message text `Go analysis failure`), `invalid_index_reads`
(`Invalid index: N`), and `eof_reads` (`Unable to read past EOF: A, B`) — `log-extract.py`
docstring, lines 12-24; all three are empty in the raw log. The D-clause wording equates a
"D failure" with "reports … Invalid index value(s)", so the same Invalid-index/EOF class is
the rule's failure class; the four `GoTypeManager` subtype WARNs at `:128-131` are not that
class: the same WARN class occurs 3-4 times in 12 of the 15 round-18 retained logs, silent
and diagnostic alike (eleven `s1246-*/s1250-*` logs plus `calib-notesmd-cli`; only
`calib-aether`, `real-kimi-webbridge`, and `s1246-swiss-nethttp` show 0). For contrast, the
D label's log does show the class:
`runs/t1250-vet/logs/rea-ghidra-CSKBVG/ghidra.log:186` `ERROR (GolangSymbolAnalyzer) Go
analysis failure …` and `:229` `Caused by: java.io.EOFException: Invalid index: 13902080`.

**Conclusion for this label** [OBSERVATION of log + application of the frozen text]:
the non-D conjunct holds; gofmt neither confirms nor refutes the H1 mechanism on its own,
it is a predicted-silent control that stayed silent. Overall C3 confirmation still rests on
the vet D clause and is outside this seat.

## 5. Binding and freshness evidence

- Carrier: `sha256_pre == sha256_post ==
  2aa4122abbd1593ee7c9e184366feef7cb06e52ce790b5ef2119e8aee8640a80`
  (`runs/t1250-gofmt/receipt.json`), equals the prediction's carrier digest (`:34`), the
  analyze subject digest (`analyze.json`), and the inspect-go artifact digest
  (`inspect-go.json`; build info `go1.25.0`, `cmd/gofmt`, `CGO_ENABLED=0`).
- Log: retained path sha `6fbfca76…f7066` = `observation.log_sha256` = receipt
  `retained_logs[0].files.ghidra.log.sha256` = worktree Git blob `3e68b443…`
  (`git hash-object`), and the worktree file bytes equal the blob at `4f6c73f`, `5e364bd`,
  and `d0690fd`.
- Prediction freeze: `git show a1140e7:.ufo/waves/round-19/predictions/t1250-gofmt.prediction.json
  | sha256sum` = worktree sha `f946efe2…5869de`, exit 0. The path is absent at `85589ac`,
  the freeze commit's parent (`git rev-parse a1140e7^`).
- Ancestry: `git merge-base --is-ancestor a1140e7 4f6c73f` → exit 0. `4f6c73f` is the commit
  that first adds the retained log path (`git log --diff-filter=A`); the log blob there is
  byte-identical to the worktree. So in this history the prediction content is committed
  before the log content.
- **Caveat — author dates are not wall-clock evidence** [OBSERVATION + INFERENCE]:
  `4f6c73f` has author `2026-10-20T15:57:44-03:00` but committer `2026-10-20T16:09:17-03:00`;
  the log it contains carries internal timestamps `16:00:04`–`16:00:30` (`ghidra.log:122-142`,
  mtime `16:00:31.99`) and `runs/run-log.txt` records the gofmt run `16:00:00`–`16:00:33`.
  The commit's author date therefore precedes content it contains by ~2m47s. The round-19
  chain's author dates equal the previous commit's committer date
  (`a1140e7` committer 15:57:44 = `4f6c73f` author; `4f6c73f` committer 16:09:17 = `5e364bd`
  author; `5e364bd` committer 16:10:41 = `d0690fd` author), i.e. dates were rewritten/backdated
  in the commit chain. The freeze-before-analyze claim is supportable from ancestry + blob
  identity; it must **not** be argued from author timestamps.

## 6. Divergences, vacuity, and limits

- **Walk divergence (non-refuting).** The frozen emulator's full walk fails under both
  hypotheses at index `5730496`, kind `invalid_data`, detail `invalid Go type`, path
  `type@0x54ebc0 → func.param[0] → elem` (`predictions/swiss-misread/t1250-gofmt.json`
  `walk.h0`/`walk.h1`; prescan identical). The Ghidra log has no `Invalid index` or EOF at
  that or any index. The emulator's own comment says the walk "is not folded into the
  boolean" because Ghidra filters non-map references it only approximates
  (`round-18/tools/swiss-misread.py:1461-1464`); the prediction's booleans and kinds are
  map-path. So the silence is consistent and the walk record is unverifiable from this log —
  the same split w1 `H0H1Semantics.md` found on vet, now observed on a held-out carrier.
- **Type-count divergence** [OBSERVATION, unexplained]: Ghidra reports `Found 1458 Go types`
  (`ghidra.log:126`); the emulator's `walk.indexed_types` is 1432 (H1) and 1382 (H0). The
  difference 1458 − 1432 = 26 happens to equal `map_types`, but map types are enumerated
  **from** the H1 index (`swiss-misread.py:1348-1352,1412`), so they are a subset of that
  index, not an addend; the coincidence has no compositional meaning. The two counts measure
  different procedures (Ghidra gap-scan discovery vs the emulator walk index). No conclusion
  is drawn, and the frozen comparison does not test these counts.
- **Silent ≠ safe.** The log itself records 23 unindexed Go types (`:125`), 5 missing type
  names (`:142`), and 4 subtype failures (`:128-131`). The rule does not classify these as
  failures, and they are baseline noise, but the C3 lesson should not read gofmt's silence as
  "types recovered correctly".
- **Compare vacuity.** For a predicted-silent label the empty-list fields can match because
  nothing was extracted as easily as because nothing was logged. That is closed here by
  (a) raw-line greps at file scope, (b) byte-identical re-extraction, and (c) the
  post-analysis completion lines. It remains a structural weakness of a silence-only match.
- **Scope limits.** The claim-counted evidence is one retained pass on one host (pass 2
  replicates it but is untracked and outside the count rule); no independent Ghidra rerun (and
  none is permitted in this lane); no carrier execution; binding gate
  (`receipt-validate.py --require-mid-maps`) not re-run here (BindingGofmt seat). No `lsp`
  device was exposed to this seat and no language server applies to a Ghidra log/JSON
  artifact, so all checks are byte/text-level with exact anchors; no semantic-reference
  query was available or applicable.

## 7. Commands (observed exits)

```
$ git rev-parse refs/heads/main                                   # exit 0: d0690fd44f46d8a7fe9da5f01c6be723d12abd41
$ git show a1140e7:<prediction> | sha256sum                       # exit 0: f946efe2…5869de
$ sha256sum <prediction>                                          # exit 0: f946efe2…5869de (identical)
$ sha256sum /home/vgpnk/.local/opt/go-1.25.0/bin/gofmt            # exit 0: 2aa4122a…40a80
$ sha256sum <ghidra.log>                                          # exit 0: 6fbfca76…f7066
$ grep -c -F 'Go analysis failure' <ghidra.log>                   # exit 1, count 0 (absent)
$ grep -n -F 'Invalid index' <ghidra.log>                         # exit 1 (absent)
$ grep -n -F 'EOF' <ghidra.log>                                   # exit 1 (absent)
$ grep -n -E 'ERROR|SEVERE|Exception|Caused by' <ghidra.log>      # exit 1 (absent)
$ grep -c -E 'WARN ' <ghidra.log>                                 # exit 0, count 4 (all GoTypeManager)
$ grep -n -E '\(GoApiSnapshot\)|Falling back|Untested Go' <ghidra.log>  # exit 0; one INFO line 123
$ python3 -I -B .ufo/waves/round-17/tools/log-extract.py --log <ghidra.log>  # exit 0; equals observation.json
$ python3 -I -B .ufo/waves/round-17/tools/compare.py \
    --prediction .ufo/waves/round-19/predictions/t1250-gofmt.prediction.json \
    --observation .ufo/waves/round-19/runs/t1250-gofmt/observation.json        # exit 0, all_match true
$ git merge-base --is-ancestor a1140e7 4f6c73f                    # exit 0
$ git cat-file -p 4f6c73f:<log> | sha256sum                       # exit 0: 6fbfca76…f7066 (= worktree)
$ git show -s --format='author=%aI committer=%cI' 4f6c73f         # exit 0: author 15:57:44, committer 16:09:17
$ grep -a -o -F 'map.group[' /home/vgpnk/.local/opt/go-1.25.0/bin/gofmt | wc -l   # exit 0, 25
$ grep -a -o -F 'map.bucket[' /home/vgpnk/.local/opt/go-1.25.0/bin/gofmt | wc -l  # exit 0, 0
# concurrent pass 2 (read-only; not claim evidence)
$ cat .ufo/waves/round-19/runs/pass2/t1250-gofmt/compare.exit    # 0
$ grep -c -F 'Go analysis failure' <pass2 ghidra.log>           # exit 1, count 0
$ grep -n -F 'Invalid index' <pass2 ghidra.log>                 # exit 1 (absent)
$ grep -n -F 'EOF' <pass2 ghidra.log>                           # exit 1 (absent)
$ grep -n -E '\(GoApiSnapshot\)|Falling back|Untested Go' <pass2 ghidra.log>  # exit 0; INFO 1.25.0 at :123
```

Tool installs/upgrades: none. No REA analyze/search/decompile, no Ghidra headless, no MCP
device, no carrier execution, no writes outside this report.

## 8. Remaining unknowns

- No per-type diagnostic in the retained log says what Ghidra did with the one misread map
  type (`*ast.CommentMap`, the `uncommon` map in `swiss-misread/t1250-gofmt.json`); its
  silence is consistent with H1's "silent misread" outcome but is not a positive observation
  of the misread.
- Why Ghidra discovers 1458 Go types while the emulator's H1 index holds 1432: the counts
  use different procedures (gap-scan discovery vs walk index) and the frozen comparison does
  not test them.
- The author-date rewrite in the commit chain (and whether it affects other round-19
  commits) is outside this seat's scope but is flagged to L1 as an evidence-ordering caveat.

Report: .ufo/waves/round-19/w2/OutcomeGofmt.md
