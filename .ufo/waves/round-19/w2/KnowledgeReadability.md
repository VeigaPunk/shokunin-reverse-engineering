# W2 KnowledgeReadability — falsification pass on `2026-10-20-r19-go125-toolchain-replay.md`

- Seat: KaidokuR19.KnowledgeReadability-3 (author-side reviewer; no outside verification claimed).
- Target: `corpus/knowledge/2026-10-20-r19-go125-toolchain-replay.md` (64 lines, committed in 4f6c73f, ancestor of main `d0690fd44f46d8a7fe9da5f01c6be723d12abd41`; working tree content identical to main — `git diff refs/heads/main -- <file>` empty, exit 0; the porcelain ` M` flag is stat-dirty only, no content difference).
- Axes: calibration (every claim re-derived from retained bytes), freshness (all cited paths/digests live now), depth (replay of the doc's own recheck instructions, including its expected-failure prediction).
- LSP: no language server answers a markdown corpus file; all checks are text/structural/git — grep is the literal fallback and this is recorded as such.
- Verdict: **the entry survives falsification on substance** — every path, line anchor, digest, count, exit code, index, and byte-decode claim I tested reproduced exactly. Two Low calibration/wording findings (F1, F2) and one Info verifiability note (F3). No High or Medium findings.
- Tooling directive: no tool installed or updated this session (none needed). No carrier executed, no REA/Ghidra run, no production edits, no LANE writes except this report.

## Findings by severity

### F1 — Low (calibration): freeze timestamp `15:57:47 -03` is not anchored to any retained artifact; git says committer `15:57:44`

- Doc line 17: "Predictions and rule committed and pushed as `a1140e76…`, 15:57:47 -03". Observation:
  - `git log -1 --format='%H %cI %ci %s' a1140e76fffdc1be032d9d813dbb686157803bbc` → `author=2026-10-20T15:37:18-03:00 committer=2026-10-20T15:57:44-03:00`, exit 0.
  - Grep for `15:57:47` across `.ufo/waves/round-19/` and `corpus/` hits only two prose files: the target doc itself (line 17) and `corpus/lessons/round-19.md:26` ("freeze pushed 15:57:47"). No run artifact, receipt, or log records that second.
- Inference: 15:57:47 is plausibly a push wall-clock (3 s after the 15:57:44 commit); git records commit time, not push time, so this cannot be confirmed or refuted from retained objects. Ordering claims are unaffected (freeze at 15:57:44 still precedes the first run at 15:57:51, `runs/run-log.txt:1`). Fix: state "committed 15:57:44 (git committer date)" or anchor the push time to a retained record.

### F2 — Low (calibration/readability): the line-3 recheck instruction is insufficient as written — reconstructing producer bytes is not enough; they must be restored at the recorded path

- Doc line 3: "reconstruct the a1140e7 producer bytes before replaying the validator." The operative requirement — restore at the pinned path — appears only in the line-46 narrative ("bytes restored at its recorded path during validation"). Empirically demonstrated (observation, this session):
  - Variant 1, current validator at `/tmp/kr19-w2-krv-cur/tools/` against `runs/t1250-vet/receipt.json` with `--require-mid-maps` → exit 1, findings `sha256_mismatch` (expected `70672eb3…`, actual `6afb7ef6…`) and `size_mismatch` (expected 46047, actual 52682) on `.ufo/waves/round-17/tools/receipt-validate.py`. Matches the doc's own prediction verbatim ("SHA-256/size mismatch").
  - Variant 2, byte-identical a1140e7 producer validator (`git show a1140e7:…receipt-validate.py`, sha `70672eb3…` confirmed) run from `/tmp/kr19-w2-krv-frozen/tools/` → **exit 1 with the identical findings** — because `receipt-validate.py` re-hashes every file at its recorded absolute LANE path, not at the replay copy.
- Consequence: a re-player following line 3 alone (reconstruct to a scratch copy) lands in the same confusing invalid state as the current-bytes case. Fix: line 3 should say "restore the a1140e7 bytes at `.ufo/waves/round-17/tools/receipt-validate.py` (the recorded path) before replaying."

### F3 — Info (verifiability): retained receipt-validation JSONs do not record which validator bytes ran

- `evidence/receipt-validation/*.json` carry `tool: "receipt-validate.py"` and `pins_path: "/tmp/pins.py"` but no digest of the validator itself, so "which bytes validated" is not self-evident from the retained records. The line-46 restore-at-path claim is the only procedure consistent with the retained exit-0 results given F2's mechanism (inference), but this seat cannot re-execute the passing direction: it requires writing the producer bytes into the LANE tree, which the wave contract forbids. The doc already discloses this class of limitation ("Retained validations prove consistency against the producer snapshot, not … authenticity"); no change requested, recorded as a residual gap below.

## Verification matrix — every tested claim (all OBSERVATION unless marked)

| Doc anchor | Claim | Check run (exit code) | Result |
|---|---|---|---|
| :1 | S038 go.dev JSON, sha `2852af0cb20a13139b3448992e69b868e50ed0f8a1e5940ee1de9e19a123b613`, size 59659213 | `grep -n 'S038' corpus/SOURCES.md` (0) — row at `corpus/SOURCES.md:44`, same sha/size/fetch date; corroborated by `corpus/lessons/round-19.md` Installs section | MATCH |
| :1–:1 | S035/S023/S003 cited | `corpus/SOURCES.md:41,29,9` — descriptions match (internal/abi map descriptors; installed `go1.25.0.json`; Ghidra Base-src.zip) | MATCH |
| :2 | rea-agents@6.5.0 pin, Ghidra 12.1.4, sessions 18:57:51–19:07:07Z (= 15:57:51–16:07:07 −03) | `grep -l 'rea-agents@6.5.0' runs/t1250-*/receipt.json \| wc -l` → 8 (0); `grep -l 'ghidra_12.1.4_PUBLIC' runs/t1250-*/logs/*/ghidra.log \| wc -l` → 8 (0); `runs/run-log.txt` first start 15:57:51, last end 16:07:07, sequential start==previous end | MATCH |
| :3 | 8 valid receipt validations, re-hash logs against receipts | 8 files, each `exit 0`, `counts.valid 1`, `require_mid_maps: true` (0); all 8 `ghidra.log` re-hashed vs `receipt.json retained_logs…sha256` — 8/8 OK (0); mtimes 16:07:55–56, after the last run (16:07:07) | MATCH |
| :11 | toolchain ELFs, artifact-held-out; 1.25.0 in r18 synthetics; r18 held-out = 1.24.x | `corpus/knowledge/2026-10-20-r18-swiss-map-replay.md:5,48,53-58` (grep, 0) | MATCH |
| :11 | `bin/go version` execution disclosed, lesson Mistakes row 5, unused as outcome evidence | `corpus/lessons/round-19.md` Mistakes row 5 (line 9 of section) — exact disclosure present, "no C3 measurement uses it" | MATCH |
| :15 | installed root; W1 re-download matched all nine members | `/home/vgpnk/.local/opt/go-1.25.0/bin/{go,gofmt}` present (0); `w1/SourcesRowsDraft.md:35` "nine members … hash identically", go `b93cdfdb…`, vet `9b9d776e…` | MATCH |
| :17 | predictions/rule at a1140e7; pushed | `git merge-base --is-ancestor a1140e7 refs/heads/main` (0); contained in `origin/main` (0); commit message "frozen C3 predictions and decision rule … runner (pre-run)" | MATCH (time → F1) |
| :17 | first run 15:57:51 −03 | `runs/run-log.txt:1` | MATCH |
| :17 | prescan before freeze, not outcome observation | prescan committed at 85589ac (committer 15:37:18 −03, ancestor of a1140e7), files tracked (9), mtimes 15:32:11 −03 | MATCH |
| :17–:18 | `link` excluded: no build info, emulator exit 2, sha retained in decision-rule | `predictions/decision-rule.json` `excluded[0]`: cause/emulator_exit 2/sha `a4286eaf…`; live link binary hashes to `a4286eaf…` (0); `predictions/swiss-misread/t1250-link.json` committed at a1140e7 | MATCH |
| :18 | D = {t1250-vet} from H1 true / H0 false; `diagnostic:false` absorbs walk-only failure | `predictions/swiss-misread/t1250-vet.json`: `predicted_failure_h1: true`, `predicted_failure_h0: false`, `diagnostic: false`; `decision-rule.json` `diagnostic_set_D: ["t1250-vet"]`, D_definition; `w1/H0H1Semantics.md:7,15` states the mechanism | MATCH |
| :19 | H1-only {13902080, 852107777}; walk 1801722468838924630 | `decision-rule.json` `h1_only_invalid_indexes.t1250-vet` and `walk_invalid_indexes_both_hypotheses` (raw read, exit 0) | MATCH |
| :21–:33 table | 7 silent + vet invalid_index; carrier-run 0 all; compare 1 vet only | 8× `carrier-run.exit`=0, `compare.exit` 0×7 + 1×vet (0); `grep -L 'Go analysis failure' runs/t1250-*/logs/*/ghidra.log` → exactly the 7 controls (0); run-log per-label `carrier-run=0` and `compare=1` only for vet; `aggregate exit=1` | MATCH |
| :34 | count command → 8 | `find .ufo/waves/round-19/runs -name compare.json \| wc -l` → **8**, exit 0 | MATCH |
| :34 | only mismatch `extra.invalid_index_reads`; frozen full list [13902080, 852107777, 1801722468838924630], observed [13902080]; all snapshot-route fields match | `runs/t1250-vet/compare.json`: `all_match: false`, every other field `match: true`, mismatch field exactly as stated; `runs/t1250-go/compare.json` `all_match: true` | MATCH |
| :34 | 7/8 full compares match | 7 `all_match: true` (compare.exit 0), vet false (exit 1) | MATCH |
| :38 | log `…/rea-ghidra-CSKBVG/ghidra.log`: line 186 Go analysis failure; line 229 `EOFException: Invalid index: 13902080`; line 243 `GoName.getPkgPath`; sha `a5de7622…`, 282 lines; Invalid-index not EOF-pair | `wc -l` → 282 (0); `sha256sum` → `a5de7622…` (0); read :180-250 — all three anchors exact (186 ERROR, 229 `Caused by: java.io.EOFException: Invalid index: 13902080`, 243 `GoName.getPkgPath`); receipt records same log sha; compare `eof_reads` observed [] | MATCH |
| :42 | `per_type[144]` = `*types.valueMap`, addr 7793536, slot 40; H0 7793648/pkg_path 17673 silent; H1 7793624 (24 early)/pkg_path 40 → Invalid index 13902080 | Python over frozen JSON: `per_type` len 153, valueMap at index 144, addr 7793536, slot_size 40; H0 `{addr: 7793648, pkg_path: 17673, outcome: silent}`; H1 `{addr: 7793624, pkg_path: 40, detail: "Invalid index: 13902080"}` (0); 7793648−7793624 = 24 | MATCH |
| :42 | log does not name `*types.valueMap`; link is INFERENCE | Doc labels it INFERENCE; log lines 186–250 contain no descriptor-name mention — correctly labelled | LABELLING CORRECT |
| :46 | 8 validations exit 0 under --require-mid-maps; after all runs; corrected validator from /tmp; restore-at-recorded-path; live recheck flags producer digest | All 8 exit 0/valid (0); mtimes after runs; replay variant 1 reproduces the flagged sha256+size mismatch exactly (exit 1); variant 2 shows reconstruction alone is insufficient → F2; "restored at recorded path" corroborated only indirectly → F3 | MATCH except F2 wording |
| :48–:51 | vet analyze.json = binary_overview Evidence `ev_3dc824…`, subject `9b9d776e…`, abs vet path; log failure is provider-log evidence, not overview field | Python containment in `runs/t1250-vet/analyze.json`: all four strings present (0); live vet binary hashes to `9b9d776e…` (0), equals `carriers.tsv:8` and `carrier.sha256_pre==sha256_post` in receipt | MATCH |
| :54–:63 decision table | per-row limits correctly scoped | Confirmed rule matches `decision-rule.json` `confirmed`/`h0_consistent`/`refuted`; "never call this 8/8" matches observed 7/8; pins `runs/*/pins/mid-*.json` exist | MATCH |
| :64 | one REA version/Ghidra/one pass; provider logs outside Evidence model; receipt linkage is producer assertion | 8/8 receipts pinned 6.5.0; 8/8 logs from ghidra_12.1.4_PUBLIC; `receipt.json log_capture_limit` field itself marks logs as best-effort polling copy; r17/r18 anchors exist (`corpus/lessons/round-17.md:31` QUALITY #20 bound provider logs; `corpus/lessons/round-18.md:23` QUALITY #21 retention claims) | MATCH |
| (freeze integrity, cross-cutting) | prediction blobs unchanged from freeze | All 25 blobs (`predictions/*.json`, `carriers.tsv`, `SHA256SUMS`, `swiss-misread/*.json`) byte-identical between working tree and a1140e7 — zero DRIFT (exit 0) | MATCH |
| (tool identity, cross-cutting) | "Unchanged round-18 `tools/swiss-misread.py`; producer digests in each run's `producer.json`" | `sha256sum .ufo/waves/round-18/tools/swiss-misread.py` = `git show 8a8da7e:…` = `git show a1140e7:…` = all 8 `producer.json tool_sha256` = `14924bd6…` (0); `python3 -I -B …swiss-misread.py --selftest` → `SELFTEST: CLEAN cases=15`, exit 0 | MATCH |

## Commands pasted (representative; all run 2026-10-20, cwd LANE unless noted)

```
find .ufo/waves/round-19/runs -name compare.json | wc -l        # → 8, exit 0
wc -l .ufo/waves/round-19/runs/t1250-vet/logs/rea-ghidra-CSKBVG/ghidra.log   # → 282, exit 0
sha256sum .ufo/waves/round-19/runs/t1250-vet/logs/rea-ghidra-CSKBVG/ghidra.log
# → a5de762231722468bcf265d5cd13ad9669f3a6d59a2746c73373e18a1a1a79c2, exit 0
git log -1 --format='%H %cI %ci %s' a1140e76fffdc1be032d9d813dbb686157803bbc
# → author=2026-10-20T15:37:18-03:00 committer=2026-10-20T15:57:44-03:00 …, exit 0
sha256sum /home/vgpnk/.local/opt/go-1.25.0/pkg/tool/linux_amd64/vet
# → 9b9d776e7569c910de714790a1b9bab1287b49fdc210973158f3076cee683bf7, exit 0
sha256sum /home/vgpnk/.local/opt/go-1.25.0/pkg/tool/linux_amd64/link
# → a4286eaff6094de7f88d55299a61a14d5aae2bfbd19687ba6d5330a730aee983, exit 0
python3 -I -B .ufo/waves/round-18/tools/swiss-misread.py --selftest
# → SELFTEST: CLEAN cases=15, exit 0
python3 -I -B /tmp/kr19-w2-krv-cur/tools/receipt-validate.py --require-mid-maps \
  .ufo/waves/round-19/runs/t1250-vet/receipt.json               # → exit 1 (sha256_mismatch + size_mismatch on receipt-validate.py)
python3 -I -B /tmp/kr19-w2-krv-frozen/tools/receipt-validate.py --require-mid-maps \
  .ufo/waves/round-19/runs/t1250-vet/receipt.json               # → exit 1, identical findings (producer bytes, scratch path — see F2)
```

Validator replays ran on `/tmp` copies only; the LANE tree was never written and no carrier was executed.

## Residual risk and verification gaps

1. The passing-direction validation (producer bytes at the recorded LANE path → exit 0) could not be independently re-executed by this seat: it requires a temporary write to `LANE/.ufo/waves/round-17/tools/receipt-validate.py`, forbidden for wave-2 seats. The retained `evidence/receipt-validation/*.json` exit-0 records are accepted as producer assertions, exactly as the doc's own limit states. [INFERENCE: it would pass, per the F2 mechanism and the line-46 narrative.]
2. The `15:57:47` push wall-clock (F1) is unverifiable from retained objects; git gives commit time only. Low residual risk: orderings do not depend on it.
3. The knowledge doc's round-18 characterization ("confirmed the Swiss/OldMapType mechanism on held-out Go 1.24.x") was checked against the r18 knowledge file's title/cohort/decision rows, not by re-deriving r18's runs — out of scope for this ticket (r18 has its own corpus entry and wave history).
4. The go.dev S038 endpoint is time-varying; the sha256/size were verified against the SOURCES row, the lesson's install record, and the wave-2 `ReopenS038` re-fetch pin, not by a fresh network fetch this session (network fetch adds nothing: three retained, mutually consistent records already pin it).

No actionable finding remains in scope. Recommended (non-blocking) doc fixes: F1 timestamp wording, F2 line-3 recheck wording.
