# Fleet corpus rules binding the round-17 knowledge entry, lesson `## Mistakes`, and fixes

Advisory author-side connector (leaf, read-only). Baseline `b563c79`; `git status` at read time showed
only `.ufo/waves/round-17/` untracked. No REA analyze/search/decompile and no Ghidra run. No tool installs.
Observation vs inference is labelled; every number carries its command.

## 0. State at read time (observations)

- `ls corpus/knowledge | grep -c '2026-10-20-r17'` → 0. Newest entries are r14/r15/r16; the contract's
  target file `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md` (contract.md:117) does not exist.
- `ls corpus/lessons` → through `round-16.md` and `round-16-verifier-spotcheck.md`; no `round-17.md`.
- `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → 23 rows, last `S023`
  (corpus/SOURCES.md:29). The Go debug/buildinfo, release-history rows C2 depends on (claims.json:29)
  are not yet opened.
- Lane provenance coverage, exact CORPUS-shaped commands run at lane root:
  - `find corpus/knowledge -type f -name '*.md' | wc -l` → 94
  - `grep -rlE '^[-* ]*source *:' corpus/knowledge | wc -l` → 92
  - `grep -rlE '^[-* ]*verified[-_ ]at *:' corpus/knowledge | wc -l` → 91
  - `grep -rlE '^[-* ]*recheck *:' --include='*.md' corpus/knowledge | wc -l` → 22
  The r17 rule is forward-only ("a **new** knowledge entry", CORPUS.md:163); 22/94 is the lane's
  inherited state, not a licence to generalize. The fleet numbers at CORPUS.md:167-170 (683/312) are a
  2026-10-19 fleet-root measurement — **inference if reused as lane facts**; do not.
- `.ufo/waves/round-17/w1/` held only `swarm-registry.json`; `DraftKnowledgeEntry`, `DraftLessonGate`,
  `DraftLessonMistakes`, `DraftQuality19`, `DraftSourcesRows`, `DraftReadmeRow` are live seats
  (wave1-assignments.json). This report is a rule matrix for them, not a draft of their files.

## A. Knowledge entry — atomic requirements

Anchors: CORPUS.md:18-19 (layout), :24-26 (rules), :34-56 (audit rules), :163-170 (kaika rule 1),
:112-125 (SOURCES contract); PROTOCOL.md:356-368; QUALITY.md:13-28.

| # | Requirement | Anchor | Checkable form |
|---|---|---|---|
| K1 | Exact path `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md` | contract.md:117 | path exists at the integration revision |
| K2 | Lines 1-3 are `source:`, `verified-at:`, `recheck:`, in that order, before any H1/prose | CORPUS.md:18, :163-165 ("come first") | `sed -n '1,3p'` matches `^source: `, `^verified-at: `, `^recheck: `; r16 precedent is `2026-10-20-r16-go-selection-preview.md:1-3`, H1 at :5 |
| K3 | External `source:` cites the `S###` row **plus** URL and anchor; local installed artifacts cite path + member/JSON pointer + anchor | CORPUS.md:164-166 | every cited `S###` resolves in `corpus/SOURCES.md` |
| K4 | Provenance is in contract shape, not prose or HTML comments, so a freshness sweep sees it | CORPUS.md:166-167; mistakes.md:469-472 | `grep -rlE '^[-* ]*recheck *:' --include='*.md' corpus/knowledge \| grep r17-go-carrier-diagnostics` → 1 |
| K5 | `recheck:` is a runnable command whose flags/paths match exercised argv, or explicitly names an unexercised variant | QUALITY.md:28; r15 routed defect `round-15-verifier-spotcheck.md:185` | compare `recheck:` argv against the retained receipt argv; the r16 defect was a missing `-I` |
| K6 | Every count is `<number> — <command> <date>` | CORPUS.md:34-38 | each numeral has a command and date within the line |
| K7 | Every negative claim carries its sweep | CORPUS.md:39-41 | "no retained log"/"no Go lines" names `find`/`grep` and scope |
| K8 | Every quote names file/member:line | CORPUS.md:42-45 | quote preceded or followed by an exact locator |
| K9 | The entry is falsifiable or explicitly marked opinion | CORPUS.md:26; QUALITY.md:12 (#2) | prediction-vs-observation table with pass/fail per field |
| K10 | Conclusions labelled observation / inference / unknown | QUALITY.md:15 (#5) | no bare behavior claim |
| K11 | Carrier identity absolute path + SHA-256; tool/provider versions pinned (`rea-agents@6.5.0`, Ghidra 12.1.4 / JDK as used) | QUALITY.md:14 (#4), :18 (#8) | per-run `carrier.sha256` present |
| K12 | REA-derived claims cite Evidence ID or the exact reproducing call (verb, target SHA, flags) | QUALITY.md:16 (#6) | `evidence_id` or argv present per run |
| K13 | Names what was not examined, including the polling-copy gap and REA's deleted runtime root | QUALITY.md:17 (#7); contract.md:46 | `log_capture_limit` text quoted into the entry |
| K14 | No runtime/execution claim: REA analyze is static import; carriers are never executed | QUALITY.md:19 (#9); claims.json:26-31 (non-claims) | absence of "observed execution" wording |
| K15 | Zero vs excluded distinguished (`no_go_analysis` from a captured log ≠ no log captured) | QUALITY.md:21 (#11); contract.md:56-58 `classification` | `classification` field per run |
| K16 | Corrections are append-only named corrections, never rewrites: any r15/r16 statement corrected must carry `R16-PROVENANCE` (or the named correction id) **and** the site's repo-relative path | CORPUS.md:53-60; PROTOCOL.md:366-367 | temporal-sweep `corrected` predicate, contract.md:91-94 |
| K17 | README index row is written only when the file exists, in the existing `entry \| topic \| source \| verified-at` shape | CORPUS.md:46-48; corpus/README.md:70-73 | row names the existing file; measure.py README-token check (contract.md:119) |
| K18 | Prediction-vs-observation table per run with mismatches reported, never hidden | claims.json:22 | one row per carrier; every `match:false` visible |
| K19 | No promotion, SHONEN `[x]`, held-capability or outside-verification claim; a capability row only after the capture runs and its receipt validates | claims.json:26-31; QUALITY.md:28; contract.md:117 | capability row absent until `receipt-validate.py` exit 0 |

## B. Lesson — atomic requirements

| # | Requirement | Anchor |
|---|---|---|
| L1 | File is `corpus/lessons/round-17.md`; lane owns it | CORPUS.md:53-60; PROTOCOL.md:138-142 |
| L2 | Carries `## Gate` with candidates, admitted, rejected-with-reasons, spot-check result | CORPUS.md:18-20 |
| L3 | Carries `## Mistakes` because the round mines at least one own mistake | CORPUS.md:171-172; PROTOCOL.md:138-141 |
| L4 | One table row per mistake, no prose-only aggregation | CORPUS.md:171-173 |
| L5 | Columns exactly class · evidence · captured-by · fix | CORPUS.md:172-173; PROTOCOL.md:140 |
| L6 | Class is one of `vacuous, survivor, stale-premise, reference-drift, number-drift, scope, attribution, landing, provider`; r16 precedent permits `<vocab> / <subtype>` with the vocabulary token leading (`round-16.md:54-59`) | CORPUS.md:173-176 |
| L7 | Evidence pointer resolves at closure: repo path, commit hash, or command output — never `/tmp`, transcript-only, or session artifact | PROTOCOL.md:356-360 |
| L8 | captured-by is the `QUALITY.md` criterion or protocol rule that should have caught it, or `none` | CORPUS.md:172-173 |
| L9 | Every fix cell satisfies section C | CORPUS.md:179-184 |
| L10 | Gate records, for every new SOURCES row, URL, access date, and a ≤25-word contiguous quote with its location | CORPUS.md:112-115 |
| L11 | Gate logs old→new for every in-place `status`/`recheck`/`used-by` change | CORPUS.md:116-119 |
| L12 | Gate records the SOURCES census before→after | PROTOCOL.md:138-139 |
| L13 | Lesson cites the round and the evidence (LOG round, commit, report) | CORPUS.md:25 |
| L14 | Rejections are kept in the Gate, not dropped (M089: no Gate = nowhere to keep a rejection) | CORPUS.md:177-178 |

## C. Fixes — "a fix is shown able to fail" (red before it counts)

| # | Requirement | Anchor |
|---|---|---|
| F1 | Exactly one red-before state per claimed repair | CORPUS.md:179-180 |
| F2 | The **same command** exits non-clean for the **named** reason in that state | CORPUS.md:180-181 |
| F3 | The fix is the only delta between red and green | CORPUS.md:181 |
| F4 | The observed failure text is **committed** (repo file, not a temp tree); timestamp at or before the shipping commit | CORPUS.md:181-182; PROTOCOL.md:356-360 |
| F5 | Rejected shapes: identical before/after splits (M027), a probe that mutates nothing (M029), a comparison that accepts an empty prior (M030) | CORPUS.md:182-184; mistakes.md:412-416 |
| F6 | Assert both exit code and a stable expected finding-id; expected values committed independent of recomputation | PROTOCOL.md:385-389 |
| F7 | Selftest green is capability, not measurement; a frozen run with committed expected verdict is the measurement | PROTOCOL.md:390-397 |
| F8 | Receipt retains argv, measured revision, stdout/stderr, exit | QUALITY.md:28 (#18) |
| F9 | The verdict names the revision measured; a run over a moving worktree is not comparable | PROTOCOL.md:393-395 |
| F10 | For r17: red measured at `b563c79` (pre-fix), green at the integration commit; the artifact lives under `.ufo/waves/round-17/` | claims.json:13; r16 precedent `.ufo/waves/round-16/documentation-red.json` |

Committed precedent for F4, observed: `round-16.md:61` cites `.ufo/waves/round-16/documentation-red.json`
(tracked: `git ls-files` lists it; introduced by commit `27b8fc1`) holding `argv`, `exit:1`, `stdout`
with `resolved: 0/4`, and the measured revision. That is the shape r17 must reproduce; a prose sentence
"the selftest prints FAILED" is not.

## D. Round-17 obligations that ride on A-C

| # | Obligation | Anchor |
|---|---|---|
| D1 | ≥3 retained carrier runs, each with pinned carrier, REA evidence id, retained log SHA-256, prediction comparison (0 → ≥3) | claims.json:22 |
| D2 | Prediction mismatches reported, never hidden | claims.json:22 |
| D3 | New SOURCES rows for Go buildinfo/source docs and Go release history; C2 is `sourced` only via those rows | claims.json:23; PROTOCOL.md:141-142 |
| D4 | No target execution; no Go 1.27 symbol-recovery promise; r16 `selection.py` reused as-is; no new selector law | claims.json:26-31 |
| D5 | Capability row for retained REA Ghidra-session log capture only if the capture runs and the receipt validates | claims.json:22; contract.md:117 |
| D6 | `temporal-sweep.py` unqualified sites N → 0, each correction naming `R16-PROVENANCE` + the site path | claims.json:13; contract.md:90-95 |
| D7 | `invocation-audit.py` unlabelled-variant registry rows M → 0; citation-drift row re-exercised with its isolated absolute argv and the receipt retained | claims.json:13; contract.md:80-84 |
| D8 | QUALITY row 19 grounded in the r16 outside lesson, present 0 → 1 | claims.json:12-13; QUALITY.md:4-5 |

## E. Contradictions and gaps (state them, do not smooth them)

1. **Selftest red ≠ committed red.** The contract's red case runs in `tempfile.mkdtemp()` and is removed
   (contract.md:7-9, :18), while the kaika rule requires the failure text to be committed and the protocol
   says tmp paths are not evidence (PROTOCOL.md:356-360). The contract names no retained-red path.
   Consequence: `DraftLessonMistakes` fix cells must cite a committed receipt, not the selftest prose;
   otherwise every "shown able to fail" claim is the r16 `vacuous / marker sufficiency` row again
   (`round-16.md:58`).
2. **Source rows precede the entry.** The entry's `source:` must cite `S###` rows that do not exist
   (23 rows, last `S023`), and SOURCES rule 4 counts only entries citing a `mined` row; a `mined` row's
   `used-by` must name a path that exists (CORPUS.md:116-125, census clause at :146-149). The rows,
   the Gate quotes, the `used-by` update and the entry must land in one integration commit; any one alone
   fails the SOURCES census.
3. **Lane-level generalisation is false.** 22/94 entries carry `recheck:`. The r17 entry can satisfy the
   trio; any sentence claiming "the lane's entries carry the trio" is a `scope`/`survivor` defect. This is
   the same failure mode as the fleet numbers at CORPUS.md:167-170 being reused off-root.
4. **Pilot is not a retained run.** `pilot/README.txt:1` says "NOT the final measured runs" and :6 says
   "pre/post carrier pins were NOT recorded". The pilot supports an OBSERVATION (shfmt log has
   `Untested Go version [1.27.0]`, `Missing Go bootstrap type info`, and the two analyzer errors at
   `pilot/shfmt-log/ghidra.log:83-89`; esbuild has `Using Go API snapshot for 1.23.12` and 4881 types at
   `pilot/esbuild-0.25.12-log/ghidra.log:63-67`), but it cannot count toward D1's 0 → ≥3 nor satisfy F8.
   Also 1 s polling and 900/1200 s timeouts differ from the contract defaults (0.5 s / 1800 s), so a
   `recheck:` quoting the contract defaults would be an unexercised variant (K5).
5. **Prose fixes have no command.** For corrections that are text-only (temporal wording, invocation
   labelling), F2's "same command" can only be the sweep at the pre-fix revision
   (`temporal-sweep.py --rev b563c79`, `invocation-audit.py --rev b563c79`). A fix cell that says only
   "text corrected" has no red state and is M029 (`CORPUS.md:182-184`).
6. **`captured-by` circularity.** C1c creates QUALITY #19 *from* the r16 outside lesson. A Mistakes row
   citing "#19" before #19 exists is `reference-drift`; either #19 lands in the same integration or the
   row cites #18 (which exists, QUALITY.md:28) or `none`.
7. **Git-objects-only measurement vs uncommitted drafts.** `measure.py`/`temporal-sweep.py`/
   `invocation-audit.py` read `git show REV:path` (contract.md:81, :91, :115-117). A red run over the
   dirty worktree is not comparable to the green run over the integration commit (PROTOCOL.md:393-395);
   the red must be measured at `b563c79` and the green at the integration revision, with the argv recorded.
8. **Do not repair r15 in place.** `corpus/knowledge/2026-10-20-r15-go-snapshot-inventory.md:3` still
   omits `-I`. It is append-only (CORPUS.md:53-60); r17's invocation fix is future guidance plus the
   citation-drift re-exercise, not an edit to the r15 header. A lesson claiming the r15 header was fixed
   would be `reference-drift`.

## F. One bounded move (synthesis, advisory)

**Revision-paired red receipts, cited by fix cells.** For each `## Mistakes` row with a fix, retain
`.ufo/waves/round-17/red/<row-id>.json` produced by the *same* tool whose post-fix state is the fix, with
`{fix_id, class, argv, revision, exit, stdout, stderr, finding_ids, named_reason}`; the red run is measured
at `b563c79`, the green at the integration revision with argv identical except the revision/extra input;
the lesson's fix cell cites `path:line` into the receipt, and `measure.py` counts red receipts whose
`exit != 0` and whose cited row exists.

- **Why non-obvious:** it converts F1-F3's "same command, fix the only delta" into a property verifiable
  across two Git revisions, which is the only form a Git-objects-only measure can check. It also closes
  the exact gap r16's own Mistakes table recorded (`vacuous / marker sufficiency`, `round-16.md:58`) and
  the contract's un-retained selftest red (contradiction 1).
- **Affected axes:** calibration (fixes become executable and revision-pinned), depth (durable receipt
  usable by later rounds). No change to the claims, the SOURCES cells, or any gate.
- **Risks:** the receipt can be hand-authored (same vacuum); mitigate with `receipt-validate.py`
  recomputation and argv-equality modulo the revision. Adds files under `W` only; `carrier-run.py` is not
  re-run (red sweeps are Git-only, no REA, so this does not violate the L1-runs-analyses-once rule).
- **Verification:** `python3 -I .ufo/waves/round-17/tools/receipt-validate.py .ufo/waves/round-17/red/*.json`
  → exit 0; every fix cell's `path:line` resolves at the integration revision
  (`git show <rev>:<path>` succeeds); `temporal-sweep.py --root . --rev b563c79` reports the named
  unqualified sites and the same command at the integration revision reports 0 with each correction named;
  `invocation-audit.py` counts show `unlabelled_variant` M → 0.
