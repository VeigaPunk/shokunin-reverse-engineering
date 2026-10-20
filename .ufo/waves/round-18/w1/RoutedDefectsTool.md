# RoutedDefectsTool — round 18 wave 1 report (amended contract)

## Deliverable

`.ufo/waves/round-18/tools/routed-defects.py` (new, 1288 lines, Python 3 stdlib
only, `python3 -I -B` runnable, executable bit set). Implements contract C1
(`contract.md:25-47`) **as amended by the L1 on 2026-10-20**: every defect
carries a `named` check set (the token checks, which are circular on their own)
and a `substance` check set (the claim itself — anchors, non-comment code,
retained evidence). Closed requires **both** sets to pass; tokens alone can
never close a defect (`routed-defects.py:187-196`).

Reads Git objects at `--rev` only: the rev is resolved once with
`git rev-parse --verify REV^{commit}` (`:77-83`) and every subsequent read is
`git show <sha>:path` / `git cat-file -e` / `git ls-tree` / `git merge-base`;
the working tree is never consulted. Output:

```
{rev, defects:[{id, open, named_open, substance_open,
                checks:[{set, name, ok, detail}]}],
 named_open_count, substance_open_count, open_count}
```

`sort_keys=True, indent=2`; `open_count` = defects failing either set
(`:777-790`). A path absent at REV fails its check (defect open); exit 2 is
reserved for an unresolvable rev or a git failure (`:1256-1286`).

## Check inventory (contract amendment → code)

| Defect | `named` checks | `substance` checks |
|---|---|---|
| R17-PINMAP `:202` | `knowledge-names-correction`, `scorecard-names-correction` (line with `R17-PINMAP`+`comparator verdict`), `quality-admission-row` (why-cell `cells[2]` in `## Admission criteria`), `carrier-run-retains-map` | `knowledge-correction-anchored` (line also has `2026-10-20-r17-go-carrier-diagnostics.md:30-32` and `not the map`), `scorecard-correction-anchored` (`SCORECARD.md:2374` and `not the map`), `lessons18-mistakes-row` (`corpus/lessons/round-18.md` `## Mistakes` row naming R17-PINMAP), `carrier-run-map-code` (`map_sha256` in non-comment code), `receipt-validate-mid-finding` (`mid_map_mismatch` in non-comment code), `r18-receipt-pinmaps` |
| R17-VALIDATE16 `:387` | `validate16-summary` (parses, `rev`==`da64646…`, 8 receipts with int non-bool `exit`), `scorecard-names-defect`, `log-names-defect` | `summary-labels-are-run-dirs` (labels == `da64646:.ufo/waves/round-17/runs/` dirs holding `receipt.json`), `validator-sha256-pinned`, `scorecard-states-true-count`, `log-states-true-count` (`<k>/8`, k = exit-0 receipts) |
| R17-PRODUCER-REV `:499` | `scorecard-`/`knowledge-names-producing-revs` (two distinct 40-hex) | `scorecard-`/`knowledge-`/`log-names-pinned-revs` (line carries **both** pinned hashes), `producer-revs-are-ancestors` (`git merge-base --is-ancestor` for each) |
| R17-SUMS-RUNLOG `:529` | `sums-covers-carriers-tsv`, `log-names-runlog-gap` (`7/8`) | `sums-restored-from-2711674` (every historical line byte-exact), `carriers-tsv-identical` (blob equality with 2711674), `log-fraction-true` (LOG names `da64646` and the true `starts/labels` fraction) |
| R17-REGISTRY `:644` | per row `skill-row-<name>` ×5 | per row `skill-scope-<name>` ×4 (`Write scope:` + ≥3 words; backticked `.ufo/`/`corpus/` tokens exist at REV via `git cat-file -e`, `:623-642`) |
| R17-S032-DIGEST `:726` | `superseding-row` (11-cell, teaches starts `supersedes S032 —`, anchor has `fetch-time`) | `s033-anchor-commit` (same row's anchor also pins a 40-hex commit), `s032-digests-evidence` (`.ufo/waves/round-18/evidence/s032-digests.json`, ≥2 distinct 64-hex) |

Comment/docstring stripping is `tokenize`-based (`:160-185`): COMMENT, NL,
ENCODING, ENDMARKER dropped; a STRING is dropped only when it starts a
statement (docstring); real string literals are retained. Verified on a probe
where a module docstring and an inner docstring containing the tokens were
dropped while `FINDING = "mid_map_mismatch"` and `{"map_sha256": 1}` survived.
On the real baseline blobs both r17 tools yield `map_sha256=False`,
`mid_map_mismatch=False`, matching the routed defect text.

## Commands run (all observed this turn)

| Command | Exit | Result |
|---|---|---|
| `git merge-base --is-ancestor <h> 9011581…` ×2 (`271167473d…`, `95e34db62f…`) | 0, 0 | both are real ancestors of baseline |
| `git rev-parse --verify da64646^{commit}` / `2711674^{commit}` | 0, 0 | `da64646adc…`, `271167473d…` |
| `git show da64646:.ufo/waves/round-17/runs/run-log.txt` (+`wc -l`) | 0 | 14 lines, `== <label> start` format, 7 starts |
| `git show da64646:.ufo/waves/round-17/runs/pro-aether/receipt.json` | 0 | `steps.analyze` present; r17 `pin_checks` = `null` (W18 shape is new) |
| scratch-repo ref probe (`tag 2711674`, `tag <40-hex>`) | 0 / 0 tags; anc=128; show=128 | refs win for abbrev; **40-hex refnames are ignored** and cannot alias an object |
| `python3 -I -B -m py_compile <tool>` | 0 | `compile ok` |
| `python3 -I -B <tool> --selftest` | 0 | last line: `SELFTEST: CLEAN cases=17` |
| `python3 -I -B <tool> --root LANE --rev 9011581d84527ba34c675f9cf912e54d2e72d470` | 0 | `open_count 6`, `named_open_count 6`, `substance_open_count 6` |
| same + `--strict` | 1 | as specified |
| same + `--rev deadbeef` | 2 | `{"error": "cannot resolve 'deadbeef': …", "rev": "deadbeef"}` |
| `_code_text` sanity (importlib, real blobs + probe) | 0 | see above |
| `rm -rf .ufo/waves/round-18/tools/__pycache__` | 0 | removed my own `py_compile` artifact only (verified single file) |

## Baseline JSON summary (rev 9011581…, exit 0)

Exact projection of the run above (counts line verbatim; one line per check):

```json
{"named_open_count": 6, "open_count": 6, "rev": "9011581d84527ba34c675f9cf912e54d2e72d470", "substance_open_count": 6}
R17-PINMAP open=True named=True substance=True
   named     knowledge-names-correction   FAIL  corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md: no line containing 'R17-PINMAP' + 'comparator verdict'
   named     scorecard-names-correction   FAIL  SCORECARD.md: no line containing 'R17-PINMAP' + 'comparator verdict'
   named     quality-admission-row        FAIL  no admission-table data row whose why-cell names round-17-verifier-spotcheck.md and R17-PINMAP
   named     carrier-run-retains-map      FAIL  .ufo/waves/round-17/tools/carrier-run.py lacks literal 'map_sha256'
   substance knowledge-correction-anchored FAIL  corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md: no line containing 'R17-PINMAP' + '2026-10-20-r17-go-carrier-diagnostics.md:30-32' + 'not the map'
   substance scorecard-correction-anchored FAIL  SCORECARD.md: no line containing 'R17-PINMAP' + 'SCORECARD.md:2374' + 'not the map'
   substance lessons18-mistakes-row       FAIL  corpus/lessons/round-18.md absent at rev
   substance carrier-run-map-code         FAIL  'map_sha256' only in comments/docstrings or absent
   substance receipt-validate-mid-finding FAIL  'mid_map_mismatch' only in comments/docstrings or absent
   substance r18-receipt-pinmaps          FAIL  .ufo/waves/round-18/runs/ absent at rev
R17-VALIDATE16 open=True named=True substance=True
   named     validate16-summary           FAIL  .ufo/waves/round-18/evidence/validate16/summary.json absent at rev
   named     scorecard-names-defect       FAIL  SCORECARD.md: no line containing 'R17-VALIDATE16'
   named     log-names-defect             FAIL  LOG.md: no line containing 'R17-VALIDATE16'
   substance summary-labels-are-run-dirs  FAIL  summary absent/unparseable
   substance validator-sha256-pinned      FAIL  summary absent/unparseable
   substance scorecard-states-true-count  FAIL  cannot count exit-0 receipts
   substance log-states-true-count        FAIL  cannot count exit-0 receipts
R17-PRODUCER-REV open=True named=True substance=True
   named     scorecard-names-producing-revs FAIL  SCORECARD.md: no line containing 'R17-PRODUCER-REV' and two distinct 40-hex hashes
   named     knowledge-names-producing-revs FAIL  corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md: no line containing 'R17-PRODUCER-REV' and two distinct 40-hex hashes
   substance scorecard-names-pinned-revs  FAIL  SCORECARD.md: no line containing 'R17-PRODUCER-REV' + '271167473d87ef710f07ecdd98caf0ce12091686' + '95e34db62f2693c455d7ee4dfef24b8f3ebc007d'
   substance knowledge-names-pinned-revs  FAIL  corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md: no line containing 'R17-PRODUCER-REV' + '271167473d87ef710f07ecdd98caf0ce12091686' + '95e34db62f2693c455d7ee4dfef24b8f3ebc007d'
   substance log-names-pinned-revs        FAIL  LOG.md: no line containing 'R17-PRODUCER-REV' + '271167473d87ef710f07ecdd98caf0ce12091686' + '95e34db62f2693c455d7ee4dfef24b8f3ebc007d'
   substance producer-revs-are-ancestors  ok    both pinned producer revs are ancestors of REV
R17-SUMS-RUNLOG open=True named=True substance=True
   named     sums-covers-carriers-tsv     FAIL  no 'predictions/carriers.tsv' line in SHA256SUMS
   named     log-names-runlog-gap         FAIL  LOG.md: no line containing 'R17-SUMS-RUNLOG' + '7/8'
   substance sums-restored-from-2711674   FAIL  1 historical line(s) missing: b'8ac38afefb60279eaf74610c03ec3526613c109cfb2b1c8fde8eb3ff5c4d3eb5  predictions/carriers.tsv'
   substance carriers-tsv-identical       ok    carriers.tsv blob identical to 2711674
   substance log-fraction-true            FAIL  LOG.md: no line containing 'R17-SUMS-RUNLOG' + 'da64646' + '7/8'
R17-REGISTRY open=True named=True substance=True
   named     skill-row-go-route-compare   FAIL  5th cell is '`snapshot_label` is marked non-discriminating; route fields and a hand predictio'
   named     skill-row-receipt-validate   FAIL  5th cell is 'Consistency of recorded digests, pins and log binding now; not authenticity agai'
   named     skill-row-pins               FAIL  5th cell is 'Identical bytes at two instants only, never continuity'
   named     skill-row-go-buildinfo-probe FAIL  5th cell is 'Stdlib reader modelled on go1.25.0 `debug/buildinfo` (keeps the writable-segment'
   named     skill-row-citation-drift     FAIL  2nd cell is 'probe / kaidoku'
   substance skill-scope-go-route-compare FAIL  no 'Write scope:' in 5th cell
   substance skill-scope-receipt-validate FAIL  no 'Write scope:' in 5th cell
   substance skill-scope-pins             FAIL  no 'Write scope:' in 5th cell
   substance skill-scope-go-buildinfo-probe FAIL  no 'Write scope:' in 5th cell
R17-S032-DIGEST open=True named=True substance=True
   named     superseding-row              FAIL  no 11-column registry row whose teaches cell starts with 'supersedes S032 —' and whose anchor cell contains 'fetch-time'
   substance s033-anchor-commit           FAIL  no superseding row
   substance s032-digests-evidence        FAIL  .ufo/waves/round-18/evidence/s032-digests.json absent at rev
```

No defect reads closed at baseline, so no design bug to report. Two substance
**sub-checks** legitimately pass at baseline because they are true facts about
the baseline (not remediation): `producer-revs-are-ancestors` (both hashes are
ancestors of 9011581 — verified directly) and `carriers-tsv-identical`
(`carriers.tsv` is byte-unchanged between 2711674 and baseline, exactly as the
lesson says). Each defect still fails other checks, so all six stay open.

## Selftest (17 cases, `:959`)

Fixture repo under `tempfile.mkdtemp()`; git writes only inside it. Cases:
1. all-open commit → `open_count 6`, all three flags true, exit 0;
2. same under `--strict` → exit 1 (required red case);
3. all-closed commit via **CLI** → exactly one open check
   `producer-revs-are-ancestors` (see limit below);
4. all-closed via **in-process** `evaluate` with `PRODUCER_REVS` patched to real
   fixture commits → `open_count 0`, `named 0`, `substance 0`;
5-10. six *named-only* variants (one named check broken each; assert the
   expected check is among the target's failing named checks and no other
   defect's named set opens);
11-16. six *token-only* variants — **the circularity guard**: all named checks
   pass, one substance check fails, defect must stay open with
   `named_open=False, substance_open=True` (PINMAP: `map_sha256` moved into a
   comment + no lessons file + no r18 runs; VALIDATE16: wrong labels +
   non-sha validator; PRODUCER-REV: two distinct 40-hex tokens that are not the
   pinned revs; SUMS-RUNLOG: matching carriers.tsv line but tsv differs from
   2711674; REGISTRY: `Write scope:` present but 2 words / nonexistent
   `corpus/` path; S032: digest-evidence file deleted);
17. bad rev → exit 2.

## Design decisions and inferences

- **Historical pins use abbreviations** (`da64646`, `2711674`, `:58-59`). The
  real lane resolves them; fixtures satisfy them with tags. This was forced by
  the observation that Git ignores 40-hex refnames (`anc=128` in the probe), so
  a fixture can never make a literal 40-hex producer hash an ancestor.
- **Absent objects fail the ancestor check** rather than exiting 2 (`:115-121`):
  ancestry that cannot be verified leaves the defect open — the truthful
  reading, and consistent with "absent path = failing check".
- **`validator_sha256` is required to be a 64-hex string** (inference from the
  field name; the amendment only says "present"): 8-10/… would not be a digest.
- **`summary.labels`** accepts a top-level `labels` list, else the per-receipt
  `label` fields (all receipts must carry one), compared as a sorted set with
  the `da64646` run dirs that contain `receipt.json` (`:374-385`, `:445-455`).
- **`map_path` lane-relative resolution**: absolute paths are mapped by
  finding `.ufo/` (else stripping the leading `/`); relative ones are resolved
  against the receipt's lane-relative run dir; the first candidate that exists
  at REV must hash to `map_sha256` (`:289-316`, `:318-371`). A `pin_checks`
  list that is empty or missing fails.
- **`sums-restored-from-2711674`** compares bytes (no decoding) so "byte-exact"
  is literal (`:570-575`).
- **`log-fraction-true`** counts `^== \S+ start\b` lines in
  `da64646:…/run-log.txt` and non-header rows of `carriers.tsv` — observed 7/8
  at baseline, matching the lesson.
- **`rev` in the output** is the resolved commit sha.

## Risks / limits

- The all-closed CLI state for R17-PRODUCER-REV is unreachable by construction
  (40-hex refnames are ignored by Git); the selftest asserts the exact
  single-check residue instead, plus full closure in-process. A real lane can
  close it because the pinned hashes are genuine ancestors.
- Row matching is literal `|` splitting; escaped pipes in table cells would
  shift indices (none at baseline).
- `_code_text` is a token filter, not a data-flow analysis: a token mentioned
  as a bare non-docstring string literal counts as code (e.g. a log message).
  That is the amendment's stated bar.
- `Write scope:` word count is whitespace-split; a cell of only backticked
  paths still counts as words.
- All runs are read-only against LANE (`show`, `cat-file`, `ls-tree`,
  `rev-parse`, `merge-base`); no jj, no git writes outside mkdtemp. No tools
  installed (stdlib git only). The only artifact I created and removed was my
  own `__pycache__` from `py_compile`.

Report: .ufo/waves/round-18/w1/RoutedDefectsTool.md
