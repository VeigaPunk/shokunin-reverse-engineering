# Source060 — S060 own-work scope / used-by / Gate (R23-C1)

Seat: `KaidokuR23.Source060` · leaf source review, author-side (not an independent admission).
Candidate: `2838351450ff1ee4baa620c962a1153450d53311` · baseline B: `aa1450b82f9ede35aada63efe8a34e01c6e02f72`.
Method: read-only git plumbing against the candidate only (`git show REV:path`, `git cat-file -e`, `git grep -l -F`, `git ls-tree -r --name-only`, `git rev-parse REV:path`) plus in-memory JSON parse and sha256 of blobs. Every cited read returned exit 0. Not executed: `count-c1.py` (Run seat only), `describe-signals.py`, REA / rea-agents, sigrok-cli, any decoder, any APK. The moving worktree was not used for evidence.

## Verdict

- **Quote-110 concern: PASS with a wording caveat.** The 110 "returned" decoder records do not include `signature`; the failed module is disclosed in diagnostics and in the entry. Only the lesson's word "loaded" over-reads (F4).
- **Original envelope vs detached copy: originals PASS.** Each committed S060 envelope is byte-identical to the stdout in its adjacent `.run.json`. Detached derivative copies exist under `verify/initial/` at a different `source_rev`; they are not gate-admissible (F5).
- **Gate predicates for S060: PASS.** Counter preconditions PASS. The three counted envelopes should bind by source reading; the counter was not run (F8).
- **Open defects are admission, scope, wording, and typography, not count-changing defects.** F1 (no lesson admission decision for the two decode witnesses) and F2 (S060 source list under-enumerates what the entry relies on) are MEDIUM; F3–F6 are LOW; F7 is stale W1 text.

## Findings

### F1 — MEDIUM · observed · manual admission gap for the two decode witnesses
- `corpus/lessons/round-23.md:16–18` is the only S-row admission table for S058–S060 (columns: Source | URL/location | Located quote | Decision). The S060 row (`:18`) admits only `.ufo/waves/round-23/evidence/c1/inventory.envelope.json` (`output_window`, `"returned":110,"has_more":false`).
- Lesson-wide grep at the candidate for `S060|offline-signal|uart-help|signal` returns lines 18 and 24 only. No decision exists for `decode-uart-hi.envelope.json` or `decode-official-uart.envelope.json`, the two envelopes the counter binds to `decode-signal-recording` (F8).
- Their relevance rests only on `corpus/knowledge/2026-10-21-r23-offline-signal-envelopes.md:48` (uart-hi original envelope) and `:73–78` (official original envelope).
- Falsifier at stake: "new source relevance or ownership unsupported". The counter does not check this; it is manual.
- For L1 (not performed here): add decision rows for both decode envelopes, or record the relevance basis in the lesson.

### F2 — MEDIUM · observed · S060 source list under-enumerates evidence the entry relies on (ownership gap; no count effect)
- `corpus/SOURCES.md:66` cell 2 (source) enumerates three paths only: `inventory.envelope.json`, `decode-uart-hi.envelope.json`, `decode-official-uart.envelope.json`. Cell 6 (anchor): "Original ok/meta.command/data records and adjacent producing .run.json".
- The entry relies on the following, none enumerated by S060:
  - `uart-help.envelope.json`: entry `:29–31` (RX-optional statement).
  - `decode-invalid-decoder.envelope.json`: entry `:84–86` (rejected control).
  - `uart-hi.bin`: entry `:38` (sha256 `4a2e729f514482287c17596cff3b29f07141fae9e86353680c99b1065e861727`; equals the decode-uart-hi subject digest).
  - `hello_world_8n1_9600.sr`: entry `:66–67` (sha256 `01b72610cdc4510dd46c8ce82b163947adbbab5b9883aea164c00e15af900b61`; equals the decode-official subject digest).
  - `generate-uart.run.json`: entry `:43`.
  - AppImage sha256 `49d2f597ec3ed3d71bfeb0465474ec2aac084fa1f66cbb132d996f7c9f50b614`: entry `:92`. Present in `.ufo/waves/round-23/sigrok-extraction.json` and `tools/setup-sigrok.py`. No S row registers it at the candidate.
  - sigrok-cli ELF pin `10fed05ae399d36a49ee9558440192023f842f3edbce0472a7f1ed15405ccebd`: entry `:103–104`. Present in `tool-runtime-pins.json`. No S row registers it.
- Counter effect: none for counted witnesses. The uart-help eid `ev_4be13793b8a767184ddcfb301b3f0e06c1333e12e533347c68eb1b53d169e94a` is absent from the entry (`git grep -l -F` hits: `uart-help.envelope.json`, `uart-help.run.json`, `verify/initial/signal-records.json`, `w1/CoverageMap.md`, `w1/PlannerDataWalk.md`). `decode-invalid-decoder` has no evidence_id (`ok:false`, `error` only).
- Reviewer effect: the RX-optional help statement (F3) and the tool pins have no S-row owner.
- Suggested fix for L1: enumerate them in the S060 source cell, or drop the reliance.

### F3 — LOW · observed text + unlabeled inference · entry `:30–31`
- Entry `:30–31`: "RX is optional because TX is another supported direction; at least one actual direction is still required."
- `uart-help.envelope.json` `normalized_result.help_lines` (81 lines; `output_window` examined 81, returned 81). Lines 45–49 read: "Required channels:" / "None." / "Optional channels:" / "- rx (RX): UART receive line" / "- tx (TX): UART transmit line". This supports "RX optional" and "TX supported".
- No retained help line says "at least one actual direction is still required". No retained run exercises a zero-channel request. The clause is [INFERENCE]. It also sits awkwardly beside "Required channels: None." It needs an inference label or retained evidence.

### F4 — LOW · observed · "loaded" / "installed" wording (quote-110 verdict PASS)
- Observed in `inventory.envelope.json` (sha256 `5f80218747c3f7c3308adef59216dea9559cada8c93a1ff543ebea6134a43d35`):
  - `data.normalized_result.decoders`: 110 records, 110 unique ids, `signature` absent, `uart` present. Per-record keys are only `id` and `name`.
  - `output_window`: `{unit: decoders, examined: 110, matching: 110, returned: 110, has_more: false}`.
  - `diagnostics` (12 lines): `srd: SyntaxError: Failed to load decoder signature … (pd.py, line 138)` with the traceback at `0b0000_0010_1001_0001`. Banner: Python 3.5.2 / 0x30502f0.
- Entry `:17` (reports110), `:19` ("installed catalog discovery only"), `:21–23` (signature failure; "That module is excluded from the returned catalog; an exhausted window does not mean every installed module loaded"). Careful and accurate.
- Overread 1: `corpus/lessons/round-23.md:18` "Admit exact returned loaded-decoder window". The envelope has no per-decoder load status, so "loaded" is [INFERENCE]. Suggested wording: "returned decoder catalog window".
- Overread 2: `corpus/SOURCES.md:66` teaches "Discovery records an installed decoder catalog". The catalog excludes an installed module whose load failed, so "installed" over-describes it. Suggested wording: "returned decoder catalog".
- The installed-module total is unknown. `examined` is the producer's count, not an installed total. [unknown]

### F5 — LOW · observed · detached derivative copies carry S060 ids outside the gate
- Originals PASS. Each committed S060 envelope equals the `stdout` string in its adjacent `.run.json` byte-for-byte (exit codes 0, 0, 0, 0, and 1 for the invalid-decoder control):
  - `inventory.envelope.json` `5f80218747c3f7c3308adef59216dea9559cada8c93a1ff543ebea6134a43d35` (9391 B)
  - `decode-uart-hi.envelope.json` `a40c947cf337319411b55c43e8e0270437e29324038a67bacb17232b9311a884` (4821 B)
  - `decode-official-uart.envelope.json` `7d5e07cca64ba60aa66ae25b8402ffe70a1bfc49bcce5c9a16f67826f768358e` (362104 B)
  - `uart-help.envelope.json` `462bc694a020c6b6eb9eeb171c5d7bfcf48c30a733ffe07c7df186b9d58c4d90` (8504 B)
  - `decode-invalid-decoder.envelope.json` `04697e72e9cabc9dae1385731ea3f2becf8a4bb94dc2334f067180b3b1008292` (991 B)
- Detached copies (FLAG; not admissible):
  - `.ufo/waves/round-23/verify/initial/signal-records.json` sha256 `16e02d1167e9b7a7144824b1bd5b5aebcf340f9fe8e1a32facef5b5d7d35a144` (11955 B). `describe-signals.py` output embedded as a string (stdout 10649 B, sha256 prefix `341352a713950503`), `source_rev` `6615aeae642aec36959180e7ea940b2794c7f1cb`.
  - `.ufo/waves/round-23/verify/initial/after-c1.json` sha256 `9e7397be7ee56de347d5da58b1191c104ce6e2c33fe5ad0f4464a3c536d795b6` (3043 B). `count-c1.py` run, exit 1, `source_rev` `6615aeae…`.
  - Both embed S060 eids. Neither embedded stdout equals any committed S060 envelope (checked against all four). Neither is cited by the S060 row, the entry, or the lesson. The counter's ROOTS are `evidence/c1` directories only, so neither is counted. Both predate the candidate and are not candidate measurements.

### F6 — LOW · observed · glued letter–digit text (typography; no gate regex impact)
- `corpus/SOURCES.md:64` scope "sigrok-cli0.7.2"; `:66` scope "REA6.5.0", anchor "opened2026-10-21"; `:111` LOG "identified5 … screened5, included4 rows S058–S061, excluded1 … for6.5.0".
- Entry `:17` "reports110", `:20` "or110", `:76` "retains12885", `:78` "sample5512".
- Bytes checked: ASCII letter immediately followed by digit, with no space. Zero-width / thin-space / NBSP codepoints across entry and SOURCES: 0. The entry has 185 letter→digit occurrences in total; this count includes legitimate tokens such as `sha256`.
- Counter effect: none found by reading the regexes (`ev_` lookbehind `(?<![A-Za-z0-9_])`, `command_pattern` lookbehind `(?<![a-z0-9_-])`, first-line `\bS[0-9]{3,}\b`, cited-path class). Quote fidelity and readability are affected: "retains12885" reads as one token. Origin: [unknown] (drafting artifact or sanitization).

### F7 — LOW · observed · stale W1 proposal text
- `w1/ConnectOutsideDebt.md:365` states "S060 = AppImage". At the candidate S060 is the own-work envelope row (`corpus/SOURCES.md:66`). The AppImage pin is unregistered (`w1/SourceRegistry.md:147–148`, `:261` S068 proposal not landed). Do not reuse.

### F8 — INFO · gate predicates PASS (observed); counter binding (inferred; counter not executed)
Observed:
- S060 row (`corpus/SOURCES.md:66`; cells 1, 4, 8, 9, 11): id S060 (60 ≥ 58); tier `A`; status `mined`; opened `2026-10-21`; used-by = `[corpus/knowledge/2026-10-21-r23-offline-signal-envelopes.md, corpus/lessons/round-23.md]`. The eligibility clause in round-23 `count-c1.py` `measure()` (`row[4] in ('A','B') and row[8] == 'mined' and row[9] == '2026-10-21' and entry in used-by`) evaluates true for S060.
- Entry line 1: `source: S058 …; S059 …; S060 …`. Reciprocal: `corpus/lessons/round-23.md:18` cites S060.
- Cited `.json` paths exist at the candidate: `inventory`, `decode-uart-hi`, `decode-official-uart`, `uart-help`, `decode-invalid-decoder`. The `.sr` and `.bin` carriers also exist; they are not `.json` and are not counted.
- Eids in the entry and in their originals:
  - `ev_940cf7bbd6ba6e8def3e7f29dad9dc03bccbd0f39a094a4787d3dd563164fdd0` (inventory)
  - `ev_bcadf773da826e70bfb79c492ddf111cd3f226fdd30addb4a15aabdc3602bd3e` (decode-uart-hi)
  - `ev_1d361f25aeaa07b5c03ffbbd43c61d061407b96c6c62bf783913d03a62c67e5c` (decode-official-uart)
- Each of the three envelopes: `ok: true`; `meta.command` equals the verb; `data.operation` equals the verb with `-`→`_`. A key walk finds no `error`, `errors`, `exit_code`, `code`, `status`, or `completion_status` key; the only related key is `data.raw_result: null`.
- Subject digests equal committed bytes: `sigrok-cli.sh` `50fe43590a7b8f88…` (698 B); `uart-hi.bin` `4a2e729f5144…` (2500 B; `artifact.bytes` 2500); `hello_world_8n1_9600.sr` `01b72610cdc4…` (58381 B; `artifact.bytes` 58381).
- Counter preconditions PASS:
  - legacy `count-c1.py` sha256 `c925918fb871151f86065aa5b3e9d10334ab845ed67c265ae0977f05e09b1879` equals `LEGACY_SHA256`;
  - round-22 evidence tree `b83fc459dca64a8356480b1ebc8309b4de65de71` is identical at baseline and candidate;
  - `verb-coverage.json` catalog bytes are equal;
  - the 57 baseline SOURCES rows are an exact prefix; S058–S061 are appended.
- `decode-invalid-decoder`: `ok:false`, exit 1, `error.code` = `execution_failure`, no data record, so it is never bound.

Inferred (not executed): `bind_cli` (`.ufo/waves/round-22/tools/count-c1.py:69–99`) and `r21` `bind`/`records`/`refused` (`.ufo/waves/round-21/tools/verb-coverage.py:39–101`) should return 0 for the three eids. That yields `inspect-signal-decoders` and `decode-signal-recording` held, plus the historical `identify-flutter-build`: 3/6, against a target of ≥2 and not 6/6. Only L1's single Run seat can confirm.

### F9 — INFO · falsifier spot-checks
- "Same verb double counted": the two decode eids collapse to one verb; counts are per verb.
- "Mere mention counts": verbs count only through bound eids. The debugger verbs are not named in the entry (`:117` "both debugger verbs remain unheld").
- "Copy erases parent refusal": the invalid-decoder control is excluded, and no copy of a refused envelope is cited.
- "Inherited identify lost": the historical identify path is preserved (round-22 tree equality).

## Stale W1 proposal findings — re-evaluated against `2838351450ff…`

| W1 item | Status at candidate |
|---|---|
| `w1/PlannerDataWalk.md:164–165`, `:312–313` (S060 scope omits uart-help) | Still true. See F2. |
| `w1/PlannerDataWalk.md:325`; `w1/ReviewSourceQuality.md:7`; `w1/SourceRegistry.md:75`; `w1/ConnectSourceChain.md:57`, `:285` (E11: lesson path missing) | Resolved by presence: `corpus/lessons/round-23.md` exists (9801 B, sha256 `8327a21fbae3c976af820e10063d973f1862a945a041d4b02a90906700a70723`). Census not run by this seat; no census result claimed. |
| `w1/PlannerDataWalk.md:139–140`, `:174`; `w1/ReviewRegistryHome.md:60–61` (S058–S060 eligibility; entry first line) | Verified at candidate. See F8. |
| `w1/ConnectOutsideDebt.md:365` ("S060 = AppImage") | Superseded. See F7. |
| `w1/CoverageMap.md:213–220`; `w1/ReviewSourceQuality.md:13` (S058/S059 id proposal) | Superseded. Candidate rows: S058 manual (`:64`), S059 dataset (`:65`), S060 envelopes (`:66`). |
| `w1/SourceRegistry.md:147–148`, `:261` (AppImage pin as S068) | Not landed; still open. See F2. |
| `w1/PlannerDataWalk.md:309–310` (no S row covers uart `pd.py` decoder source) | Still true. The entry does not claim decoder source, so this is outside S060 scope. |

## Produced files and hashes

- `.ufo/waves/round-23/w2/Source060.md` (this report). sha256: recorded in the seat's final message, which I computed after writing this file.
- No other files were written by this seat. A scratch file `/tmp/s060_rows.txt` was created early, outside the allowed write roots, and was removed before analysis continued.

## Installs or none

None. No tool was installed or updated. Host `python3` was used only for in-memory reads and hashes of candidate blobs.

## Open risks

1. Counter not run. The 3/6 result is inferred from source. L1's single Run seat must confirm; expected result is `c1_incomplete` (not 6/6).
2. F1 admission gap for the decode witnesses is manual; the counter does not check per-envelope admission.
3. F2 scope gap is manual; the registry edit belongs to L1. This seat made no registry edit.
4. Census not run. E11 resolution rests on file presence only.
5. Origin of the glued letter–digit text (F6) is unknown.
6. The entry's "at least one actual direction is still required" (F3) may be true in practice; it is unevidenced in the retained artifacts.
7. The `verify/initial/` copies (F5) could be cited by later reviewers despite not being candidate measurements.
8. Author-side review only; no independent admission is claimed.
