# ExecSweep — standing receipts at freeze

Axes: receipt completeness, named-path integrity, registry conformance, source hygiene, fixture safety.

Freeze: `b827a8b5d54f2885ec9be7786389f356c59226ce`. Instruments were extracted with `git show FREEZE:path` into the exclusive scratch root, not executed from drifting worktree bytes. Every revision-aware audit read the lane's committed objects at that freeze. `freeze-registry-entries.txt` preserves its registered rows; `frozen-instrument-sha256.json` preserves instrument hashes. No source repair, git mutation, tool installation, or external-state change was made.

## Results

| Duty | Exit | Observed verdict |
|---|---:|---|
| Freeze receipt completeness, round-71 container | 1 | `"verdict": "failed"`; 9 checked; one absent bare name |
| Named-path audit, latest committed round-70 SCORECARD section | 0 | `"verdict": "clean"`; named 2, missing 0 |
| Frozen round-51 census3 | 2 | `{"error": "registry row must have seven cells", "exit": 2}` |
| Round-68 conformance census | 1 | `"ok": false`, `"mismatches": 5` |
| Round-71 grammar-v2 census | 1 | `"ok": false`; rows 88, paths 88; six nonconformant rows |
| Sources validation (requested live-root command) | 0 | `kaidoku\tok\t/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md` |
| Sources row-count census (supplemental) | 0 | rows 179 |

The named-path audit deliberately selects the latest section present at freeze: `2026-11-04 — round 70: the readers are bound to their producers, the seam is safe, and a static executable joins the carriers`. There is no committed round-71 SCORECARD section at freeze; this result does not validate an unwritten round-71 record.

Census3's seven-cell failure is routed M70-7, not a new surprise. Round-68 conformance names five unregistered paths: all five `tools/round-71/` instruments. Its duplicate_rows, row_absent and thin sets are empty; scope_size 84, registry_rows 88. Its historical named_but_absent set is retained verbatim in its JSON, not miscounted as five new mismatches.

The round-71 census identifies exactly the six round-70 rows (`packed-elf.py`, `mutation-check.py`, `contract-probe.py`, `seam-probe.py`, `forged-receipts.py`, `controls.py`) with `['pinned-empty']`; duplicates are empty, multicell_rows is 4. Thus the freeze is still the pre-repair registry state. Expected/pending work is not a clean bill, and no landing-state result is claimed.

## Source census and W04 erratum

Validation: exit 0, malformed/E01 count **0**, W04 count **21**. Supplemental census: **179 rows**, tier A/B/C = 165/9/5, mined/rejected = 170/9. The true observed count is 21, not the round-70 report's “same 20”. This command intentionally reads the requested live fleet root rather than a scratch replacement; its result is a live observation, not a claim of immutable freeze-source bytes.

## Fixture safety

The requested temporary-directory pattern audit was performed using the required specialized regex-search tool rather than shell grep. Pattern `mkdtemp\(dir="/tmp"\)|/tmp/`, recursively over both the live `tools/round-71/` directory and the five files extracted from the frozen tree: **No matches found** in either search. Hits: **0**; consequently there are no literal/comment hits to classify. This is a lexical check, not proof that computed temporary paths are impossible. The tool search exposes no subprocess exit code; no shell exit code is fabricated.

## Persistent bare-name disposition

Exact finding object from `receipt-audit.json`:

```json
{"finding": "RECEIPT_ABSENT", "name": "package.json", "scope": "round-71"}
```

The frozen container's A5 explicitly calls this `REA package 6.5.0 package.json sha256 ...`: it is an external package metadata pin, not a promised wave receipt. The frozen audit's documented bare-name rule and BARE_NAME regex nevertheless include every bare JSON filename in container strings. Honest next step: **declare a narrowly scoped exception for this external package-metadata mention**, or disclose a future semantic extractor fix with evidence. Do not manufacture an in-wave package file to quiet the gate; do not call exit 1 clean. No exception is claimed to have been approved or implemented by this seat.

## Exact commands and retained evidence

Each `.txt` below retains stdout, stderr and exit independently. `commands.json` bundles the same unabridged observations. Executable locations under scratch are frozen-byte copies of the same relative registered instruments.

### receipt-audit

```sh
python3 -I -B /fast/scratch/hyaku/kaidoku-r71/ExecSweep/tools/round-56/receipt-audit.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev b827a8b5d54f2885ec9be7786389f356c59226ce --claims .ufo/waves/round-71/claims.json --json-out /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-71/w1/ExecSweep/receipt-audit.json
```

Exit: 1. Evidence: `receipt-audit.txt` and `receipt-audit.json`.

### named-path-audit

```sh
python3 -I -B /fast/scratch/hyaku/kaidoku-r71/ExecSweep/tools/round-57/record-receipt-audit.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev b827a8b5d54f2885ec9be7786389f356c59226ce --record SCORECARD.md --heading '2026-11-04 — round 70: the readers are bound to their producers, the seam is safe, and a static executable joins the carriers' --json-out /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-71/w1/ExecSweep/named-path-audit.json
```

Exit: 0. Evidence: `named-path-audit.txt` and `named-path-audit.json`.

### census3

```sh
python3 -I -B /fast/scratch/hyaku/kaidoku-r71/ExecSweep/tools/round-51/census3.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev b827a8b5d54f2885ec9be7786389f356c59226ce --check
```

Exit: 2. Evidence: `census3.txt`.

### registry-conformance

```sh
python3 -I -B /fast/scratch/hyaku/kaidoku-r71/ExecSweep/tools/round-68/registry-conformance.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev b827a8b5d54f2885ec9be7786389f356c59226ce --json-out /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-71/w1/ExecSweep/registry-conformance.json
```

Exit: 1. Evidence: `registry-conformance.txt` and `registry-conformance.json`.

### registry-census

```sh
python3 -I -B /fast/scratch/hyaku/kaidoku-r71/ExecSweep/tools/round-71/registry-census.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev b827a8b5d54f2885ec9be7786389f356c59226ce --generate --out /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-71/w1/ExecSweep/registry-census.json
```

Exit: 1. Evidence: `registry-census.txt` and `registry-census.json`.

### sources-census

```sh
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku
```

Exit: 0. Evidence: `sources-census.txt`.

### sources-count

```sh
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin kaidoku
```

Exit: 0. Evidence: `sources-count.txt`.

## Bounds and assessment

Reports stay in the binding exclusive `w1/ExecSweep/` directory; the trailing request for sibling-level `w1/ExecSweep.md` conflicts with that write boundary, so no sibling-level file was created. No LSP symbols were changed or refactored; LSP was not required for these CLI executions. All frozen scratch copies are removed after receipts are retained. No builds, linters, formatters or unrelated tests were run.

Self-assessment: accuracy 4/5 (live source census is explicitly separated from frozen-object audits); completeness 4/5 (the shell grep exit is unavailable because the required specialized search replaces it); clarity 4/5 (full commands are necessarily long); actionability 5/5 (named failures and disposition are explicit); conciseness 4/5 (raw evidence is separate). Overall 4.2/5. Improvement: parent should retain this freeze baseline beside its eventual post-integration receipts; user agreement expected because no pending failure is represented as clean.

VERDICT: not-met at freeze — receipt-audit package.json absent, routed M70-7 census3 error, five unregistered round-71 tools and six pinned-empty round-70 rows; named-path audit clean; sources 179/0 malformed/21 W04; temporary-path lexical hits 0.
