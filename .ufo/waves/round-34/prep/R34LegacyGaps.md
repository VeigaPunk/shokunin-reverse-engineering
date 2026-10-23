# R34LegacyGaps — five r32 wrapper mutants and the archived secondary-gate selftest gaps

- **Seat:** `KaidokuR34.R34LegacyGaps` (UFO-FSD executor, leaf; no subagents, no background jobs, no delegation).
- **Contract read first:** `/home/vgpnk/.omp/agent/RULES.md`, then the seat target. Base named by the round-34 card: `ec3125ad3d130d92f888a4128dfaa2982f36fff7`.
- **Lane:** `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. All paths below are absolute unless the trailer line.
- **Window:** 2026-10-23 ≈10:05Z–10:35Z UTC. `date -u` anchors 10:31:19Z and 10:32:47Z; final harness receipt 10:35:01Z.
- **Output directory:** `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-34/prep/R34LegacyGaps-files/` — the only path this seat wrote. No build, lint, formatter, lane gate, REA, carrier, parser, or frozen instrument was run.
- **Held item** `U064N008Hf47eb933` was not inspected, named in a task, or touched. Nothing was installed or updated.

## 1. Inputs read

| Input | What was taken from it |
|---|---|
| `corpus/lessons/round-33-verifier-spotcheck.md:129-137` | Defect 3 (five open r33 instrument limits) and defect 4: “Carried from round 32 and still open: five round-32 wrapper mutants and the archived secondary-gate selftest gaps (pe_own_compare, verify_quotes, independent-pe).” |
| `corpus/lessons/round-32-verifier-spotcheck.md:111-117` | Defect 5 wording: five C1/C2 selftest mutants survive, archived secondary gates lack separate selftests. |
| `.ufo/waves/round-32/a2audit/A2SelftestHoles.md` | Mutation table: 24 invocations, 3 killed / 5 survived; exact clause locations and replacements; the C1 selftest invokes only `judge` and `province_ok`. |
| `.ufo/waves/round-33/prep/R33MutantLimits.md` §1-4 | Bound-vs-repair analysis, the archived-gate inventory, and the recommendation not to repair C2v3. |
| `tools/round-32/c1-arm64x-positive.py` (lines 109-135, 222-277) | Re-read the four clauses and the selftest body. `entry_ok` and `committed_check` appear only at measure-time call sites (lines 200, 219); the selftest calls `judge` and `province_ok` only. Zero selftest cases — measured with `grep -n` / `awk`, not inferred. |
| `tools/round-32/c2-capability-calibration-v3.py` (lines 45, 163-180, 235-268) | Threshold at line 168; selftest has no row with exactly five shared description words. |
| `.ufo/waves/round-32/independent-pe/compare.py` | 238 lines; globals `TSV`/`BASE` hardcoded; no `selftest` flag; reads `indep.json`, `oracle.stdout.jsonl`, `readobj-<id>.txt`, `carriers.tsv`; calls `llvm-readobj --version`; inputs are text/JSON only. |
| `.ufo/waves/round-32/final-c1-witness/pe_own_compare.py` | `own_parse(path)` opens carrier `.dll` bytes (`open(path,'rb')`), so any selftest needs binary PE content. `parse_readobj` is text; `sys.argv[1..4]`; no selftest. |
| `.ufo/waves/round-32/source-reopen/verify_quotes.py` | No `__main__` guard; last statement is `sys.exit(1 if bad else 0)` at line 233, so importing executes the gate. Absolute `SNAP`, `C1IN`, `/fast/scratch/.../reopen` constants. Several rows pass a literal `True` predicate (`drift:html:*`), so the row count overstates checks. |
| `SKILL.md:1077, 1083-1084, 1100-1101` | Current registry disclosures: compare.py “ignores argv” and has no selftest mode; pe_own_compare has “no separate selftest mode”; verify_quotes has “no separate selftest mode”; pe_own_compare needs the live pinned carrier bytes that the captures do not reconstruct. |

Frozen instrument bytes were only hashed, never opened for write and never downgraded to “conformant”:

```
7a534be655f940728879e1d25e43a20685371e25232ded94eeb2d5bcc0800f1a  tools/round-32/c1-arm64x-positive.py
5955e8ace76d93c7891a43ca282f129c8874cd1878a05c9f29e0b81d3cab2f9f  tools/round-32/c2-capability-calibration-v3.py
b955f90849192ceeeee26b2849f2ec8dc1d4032e9fd05bf02e9e039cf9ed4209  .ufo/waves/round-32/independent-pe/compare.py
587dadc65d756ccc25d9b05cbbdec0b61fb38b742ee651ebe278e06e1b023251  .ufo/waves/round-32/final-c1-witness/pe_own_compare.py
a41689cc875ca28ea5bd3566bcf5c93eba3c6c54ce532b977960c07f0bc20e73  .ufo/waves/round-32/source-reopen/verify_quotes.py
```

The two C1/C2 hashes equal the frozen pins in `A2SelftestHoles.md`; the three archived files equal the hashes taken again after the harness run (`run-receipt.json` → `source_sha256_unchanged: true`).

## 2. The five r32 survivors — exact disposition

| ID | File : line | Clause → mutant (as recorded by A2SelftestHoles) | Round-34 disposition | Discriminating input now present |
|---|---|---|---|---|
| **C1-1** | `c1-arm64x-positive.py:132` | `if CLAIM_ROW not in text:` → `if not text:` | **repaired by successor** `wrapper_successor.py::entry_cite` | Non-empty entry that names the evidence id but omits `S099` must fail |
| **C1-2** | `:121` | `if strip_meta(committed) != strip_meta(live):` → `if committed.get("data") != (live or {}).get("data"):` | **repaired by successor** `::envelope_equal` + `::committed_json` | Same `data`, changed top-level `ok`; same `data`, extra outer field; non-object committed JSON fails cleanly instead of raising `AttributeError` |
| **C1-3** | `:124` | `if not eid or eid not in entry_text:` → `if not eid:` | **repaired by successor** `::evidence_id` | Live `evidence_id` omitted from the entry text must fail |
| **C1-4** | `:115` | `if freeze_ct is None or added is None or added <= freeze_ct:` → `added < freeze_ct:` | **repaired for the comparison predicate only** `::post_freeze` | `added == freeze_ct` must fail; `added == freeze_ct + 1` must pass. The git acquisition path is *not* exercised — see §6 |
| **C2-1** | `c2-capability-calibration-v3.py:168` | `len(shared) < MIN_DESC_WORDS` → `<=` | **open bounded limit; deliberately not repaired** | Boundary pair specified: exactly 5 shared words must match, 4 must not |

Why C2-1 is not repaired: C2v3 is falsified as a semantic measure and barred from admission (QUALITY 58; round-32 spotcheck defect 4, “Do not reuse C2v3 as admission evidence”; `R33MutantLimits` §3 says “Bound only — recommend no repair of C2v3 itself”). Shipping a successor threshold clause would resurrect a banned counter without the denial/word-bag/off-topic controls a v4 must freeze before data. Only a specification is retained, in `legacy-gap-matrix.json`.

Every repair is in a new file; the frozen r32 instruments are byte-identical to their pins. The old instruments are **not** called conformant: their four clauses still have zero selftest cases and C2-1 still survives on the frozen bytes.

## 3. Archived secondary gates

| Gate | Disposition | Evidence | What is still not covered |
|---|---|---|---|
| `independent-pe/compare.py` | **Separate selftest added; green and red both demonstrated** | Isolated text/JSON fixture, archived file imported read-only, only `TSV`/`BASE` rebound: `carriers=1 checks=31 passed=31 failed=0`, exit 0. Tampered `sha256` in `indep.json`: `label_sha256` fails, exit 1. | One carrier of twelve; the recorded 372/372 run stays a single-measure observation. The replay needs the host `llvm-readobj` for a version string (LLVM 23.1.3 here). The archived bytes are unchanged; the shim lives in this seat's directory. |
| `source-reopen/verify_quotes.py` | **Not repairable in place; successor core only; archived script excluded from round-34 admission** | `quote_support_successor.py`: 9 embedded cases, 0 failures; 7 support + 2 informational rows green; tampered case file exits 1 with 2 failures; Q-1/Q-2 mutants killed. | Source identity sets, live-drift census, the S099/S100 HTML/Markdown rows, and the archived verdict map. Its unconditional diagnostics are *not* copied: the successor prints `INFO` and excludes them from the check count. |
| `final-c1-witness/pe_own_compare.py` | **Open bounded limit; excluded from round-34 admission; not executed** | `run-receipt.json` → `not_run` record with reason and archived sha. | `own_parse` needs the pinned carrier DLL bytes, which the captures do not reconstruct (SKILL.md:1100). Secondary text gaps also unrepaired: positional TSV split raises `IndexError` on a short row rather than failing cleanly; readobj parsing is reachable only through the binary-gated path. |

`verify_quotes` cannot be replayed from an isolated fixture without editing it: it executes at import and hardcodes three absolute directories, one of them a `/fast/scratch` path. Editing it in place would destroy the archived bytes the round-33 registry cites, so the mechanical support predicate was re-stated in a successor instead, and the archived verdict is explicitly **not** treated as conformance evidence.

## 4. Files produced

All under `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-34/prep/R34LegacyGaps-files/`.

| File | Role |
|---|---|
| `wrapper_successor.py` | Successor to the four r32 C1 acceptance-wrapper clauses; `--selftest` (20 cases) and `--input RECORD.json` (outer CLI) |
| `quote_support_successor.py` | Successor core for the archived quote gate's mechanical support predicate; `--selftest` (9 cases) and `--root/--cases` (outer CLI) |
| `replay/indep_pe_replay.py` | Read-only import shim for the archived independent-pe comparator; rebinds only `TSV`/`BASE` |
| `run_checks.py` | Outer CLI selftest: 19 subprocess checks + 1 explicit not-run record |
| `fixtures/wrapper/*.json` | 1 green + 6 red acceptance records (text/JSON only) |
| `fixtures/quote/{source.md,cases.json,cases-tampered.json}` | 7 support rows (5 negative) + 2 informational rows; one tampered expectation file |
| `fixtures/indep-pe/*` | Bounded copies of round-32 text/JSON captures for `k01`, with `provenance.json` (source sha256, filters, fixture sha256) |
| `receipts/*.txt` | Per-check argv, exit, stdout, stderr, bound settings |
| `run-receipt.json` | Machine-readable run record, bounds, source hashes, not-run record |
| `legacy-gap-matrix.json` | Decision table for all five mutants and all three gates |

SHA-256 of the authored files:

```
eefaa3c962c890d7fcb581f5eb56b666a68fef2e7c71f94c0eb19cd9e189f2d2  wrapper_successor.py
e280d7b7179fab9dbd82c0e7df9d669c0726b99afbfecd5867d303e6d716b04a  quote_support_successor.py
3a4ab63c685ac8d52409ce031f631a41e93a741ff56c1da82370f36962d63bd8  replay/indep_pe_replay.py
f51572aa3dda0fc15fed0724056f32b4ca4ff036fe40976c34095c6ff940d1f3  run_checks.py
336dac9627162a3bf77f0d8f9efdd11e28bdf9207ad239dc026772b40e425945  legacy-gap-matrix.json
```

No binary content is authored anywhere in this tree; `provenance.json` records `binary_content: false` and reproduces the source sha256 of every copied capture.

## 5. Red/green, run once

Exact command and exit:

```
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-34/prep/R34LegacyGaps-files
timeout --kill-after=10s 300s python3 -I -B run_checks.py
→ checks=19 passed=19 failed=0 not_run=1 source_unchanged=True ; EXIT=0
```

Each inner check is itself bounded as
`timeout --kill-after=5s 120s prlimit --as=2147483648 --fsize=4194304 -- python3 -I -B <script>`,
with `GIT_DIR`, `GIT_WORK_TREE` and `GIT_INDEX_FILE` removed from the child environment.

Observed tallies (full stdout in `receipts/`):

| Check group | Observed |
|---|---|
| A — successor selftest | `selftest cases=20 failures=0`, exit 0 |
| B — JSON records | `accept-good` exit 0; `bad-source` → `FAIL entry_cite`; `bad-envelope-ok` / `bad-envelope-extra` → `FAIL envelope_equal`; `bad-evidence` → `FAIL evidence_id`; `bad-freeze-boundary` → `FAIL post_freeze`; `bad-committed-list` → `FAIL committed_json`; all exit 1 |
| C — r32 C1 mutants on private copies | C1-1 → `FAIL C1-1 kill: entry without the claim row`; C1-2 → `FAIL C1-2 kill: same data, committed top-level ok differs`; C1-3 → `FAIL C1-3 kill: live evidence_id omitted from the entry`; C1-4 → `FAIL C1-4 kill: first-added exactly at the freeze commit time`; all exit 1 |
| D — quote core selftest | `selftest cases=9 failures=0`, exit 0 |
| E — quote cases | green `cases=9 support=7 informational=2 failures=0` exit 0; tampered exit 1 with 2 failures |
| F — quote mutants | Q-1 (word cap 25→26) and Q-2 (exact-line equality) each exit 1 with their named case failing |
| G — archived independent-pe | green `carriers=1 checks=31 passed=31 failed=0` exit 0; tampered `label_sha256` exit 1 |
| H — pe_own_compare | not run; recorded as `open-bounded-limit` |

The mutant copies were created in `R34LegacyGaps-files/tmp/run-<pid>/` and deleted in a `finally` block; `tmp/` is empty after the run. Mutants are applied to **successor** copies only, never to the frozen instruments, so no restoration step is needed and no archived byte moved.

## 6. Remaining limits (must stay open)

1. **C1-4 git acquisition is unexercised.** The successor tests the predicate `added > freeze_ct` on two caller-supplied epoch seconds. `first_added()` (`git log --diff-filter=A --format=%ct`) and its committer-clock blind edge (A2FreezeBytes finding 3) remain outside any selftest. A future end-to-end case would need a synthetic git fixture, which this seat did not create (no git writes).
2. **C1-1/C1-3 remain substring clauses.** A wrong-but-present token still passes; requiring the id to sit in an evidence field would be a semantic change not authorized here.
3. **Frozen instruments still have the identical gaps.** The four C1 mutants were killed against the successor's selftest, not against `c1-arm64x-positive.py`. That file still has zero cases for `entry_ok`/`committed_check`; C2v3 still has no exactly-five-word row. Neither may be described as selftested.
4. **C2-1 remains bound-only.** No calibration instrument, no successor threshold, no data. Any v4 must freeze the boundary pair (5 matches / 4 does not) plus the QUALITY-58 denial, word-bag and off-topic controls before data.
5. **`pe_own_compare.py` has no selftest and no replay path without binary content.** Its TSV schema gap (short row → `IndexError`, i.e. could-not-evaluate rather than clean fail) is disclosed, not repaired.
6. **`verify_quotes.py` is not repaired.** Only the mechanical support predicate has a successor. Identity, live-drift, census and the archived verdict map remain unselftested, and its literal-true rows still overstate its check count in the archived receipt.
7. **independent-pe evidence is ability-to-fail, not the archived replay.** One carrier, 31 comparisons; the historical 372/372 remains a single-measure observation, and the shim's global rebinding is disclosed rather than hidden.
8. **No round-34 claim may cite these receipts as a claim outcome.** They are repair evidence for a routed defect only.

## 7. Round-34 admission recommendations

- **Exclude** any reuse of C2v3 as admission evidence; the C2-1 boundary stays open.
- **Exclude** `pe_own_compare.py` from admission while it remains binary-dependent and lacks a selftest; cite its 144/144 only as a corroborating comparison, never as a verdict.
- **Exclude** `verify_quotes.py`'s archived verdict map from admission. If quote checking is needed, use the successor core as a probe, and state that identity/drift rows are uncovered.
- **Allow** the independent-pe comparator to be cited as corroborating comparison now that a red path exists; do not upgrade “ability to fail” to “the archived run was reproducible”.
- The four repaired wrapper clauses may be cited as *repair evidence*, not as a rerun of the round-32 C1 claim.

## 8. Tooling record

- Installed/updated: **none** (pacman is paused host-wide; nothing else was needed).
- Executed versions: Python 3.14.8, GNU coreutils 9.12-2 (`timeout`), util-linux 2.42.4 (`prlimit`), LLVM 23.1.3 (`llvm-readobj --version`, consumed by the archived comparator for a version string only).
- No network access, no REA, no carrier execution, no `/fast/scratch` traversal, no git/jj write, no build/lint/formatter run.

Report: `.ufo/waves/round-34/prep/R34LegacyGaps.md`
