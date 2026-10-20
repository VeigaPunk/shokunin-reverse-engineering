# CompareNewFields — r18 w2 falsify report

HOLDS

`compare.py --selftest` is CLEAN (23 cases), and a full re-run over all 15 r18
pairs and all 8 r17 pairs at lane revision `b2aad08ceeee8dd125ce0d316056d8bd766c7f94`
reproduces every retained `compare.json` byte-identically with every retained
`compare.exit` (all 0). The wave-1 `extra_expectations` machinery (new fields
`analyzer_errors_empty`, `eof_reads`, `invalid_index_reads` at
`.ufo/waves/round-17/tools/compare.py:201-216`, all line numbers from
`git show b2aad08:…`) exercised the new-field path on all 15 r18 pairs and
stayed dormant on the 8 r17 pairs. No differences found.

## Commands run (observation)

### 1. Tool identity at REV — unchanged since wave-1

    git log --oneline --all -- .ufo/waves/round-17/tools/compare.py   → last touch eb6c266 (frozen wave-1 commit)
    git show b2aad08:.ufo/waves/round-17/tools/compare.py | sha256sum → 582a77f3…
    sha256sum .ufo/waves/round-17/tools/compare.py                    → 582a77f3…  (exit 0, identical)

### 2. Selftest

    python3 -I -B .ufo/waves/round-17/tools/compare.py --selftest
    stdout: SELFTEST: CLEAN cases=23
    exit 0

23 = the 15 original cases + 8 wave-1 cases anchored at `compare.py:411-448`
(`extra_analyzer_errors_empty_{green,red,…}`, `extra_eof_reads_green`,
`extra_eof_reads_order_red`, `extra_eof_reads_observation_missing_red`,
`extra_invalid_index_reads_{green,observation_missing_red}`); summary emitted
at `compare.py:503`.

### 3. All 8 r17 pairs — byte-identical to retained compare.json

Run from `.ufo/waves/round-17/` (the retained `compare.json` records relative
`prediction`/`observation` paths, so the same cwd reproduces the bytes):

    python3 -I -B tools/compare.py --prediction predictions/<l>.prediction.json \
        --observation runs/<l>/observation.json > $TMP/<l>.compare.json
    cmp -s $TMP/<l>.compare.json runs/<l>/compare.json

| label | new exit | retained exit | stdout vs retained compare.json |
|---|---|---|---|
| calib-esbuild-0.25.12 | 0 | 0 | IDENTICAL |
| calib-shfmt | 0 | 0 | IDENTICAL |
| pro-aether | 0 | 0 | IDENTICAL |
| pro-containerd-shim | 0 | 0 | IDENTICAL |
| pro-esbuild-0.21.5 | 0 | 0 | IDENTICAL |
| pro-esbuild-0.27.7 | 0 | 0 | IDENTICAL |
| pro-notesmd-cli | 0 | 0 | IDENTICAL |
| pro-op | 0 | 0 | IDENTICAL |

Only `pro-esbuild-0.27.7.prediction.json` carries `extra_expectations` (4 r17
keys: `language_compiler`, `invalid_version_strings`,
`bootstrap_attempts_at_least`, `analyzer_errors_contain`); the other 7 r17
predictions carry none, so the new `compare.py:201-216` blocks are skipped —
the byte-identical outputs confirm the wave-1 additions are dormant under the
r17 prediction shape (observation; wave-1's dormancy claim in
`w1/CompareEofFields.md` holds).

### 4. All 15 r18 pairs — byte-identical to retained compare.json

    python3 -I -B $LANE/.ufo/waves/round-17/tools/compare.py \
        --prediction $LANE/.ufo/waves/round-18/predictions/<l>.prediction.json \
        --observation $LANE/.ufo/waves/round-18/runs/<l>/observation.json > $TMP/<l>.compare.json
    cmp -s $TMP/<l>.compare.json runs/<l>/compare.json

| label | new exit | retained exit | stdout vs retained compare.json |
|---|---|---|---|
| calib-aether | 0 | 0 | IDENTICAL |
| calib-notesmd-cli | 0 | 0 | IDENTICAL |
| real-kimi-webbridge | 0 | 0 | IDENTICAL |
| s1246-noswiss-methods | 0 | 0 | IDENTICAL |
| s1246-noswiss-nethttp | 0 | 0 | IDENTICAL |
| s1246-noswiss-nomethods | 0 | 0 | IDENTICAL |
| s1246-swiss-methods | 0 | 0 | IDENTICAL |
| s1246-swiss-nethttp | 0 | 0 | IDENTICAL |
| s1246-swiss-nomethods | 0 | 0 | IDENTICAL |
| s1250-noswiss-methods | 0 | 0 | IDENTICAL |
| s1250-noswiss-nethttp | 0 | 0 | IDENTICAL |
| s1250-noswiss-nomethods | 0 | 0 | IDENTICAL |
| s1250-swiss-methods | 0 | 0 | IDENTICAL |
| s1250-swiss-nethttp | 0 | 0 | IDENTICAL |
| s1250-swiss-nomethods | 0 | 0 | IDENTICAL |

All 15 compares carry 8 fields each (5 base/route + 3 extra); every
`extra.*` verdict is `match: true` (observation, parsed from retained
`compare.json`).

## New-field coverage actually exercised (observation)

The compare is not vacuously green — observed values came from the updated
`log-extract.py` output:

| label | observed `eof_reads` | observed `invalid_index_reads` | extra verdicts |
|---|---|---|---|
| calib-aether | `[[17645861, 111938854]]` | `[]` | contain:OK eof:OK idx:OK |
| s1246-swiss-nethttp | `[]` | `[22386945]` | contain:OK eof:OK idx:OK |
| real-kimi-webbridge | `[]` | `[15606016]` | contain:OK eof:OK idx:OK |
| other 12 | `[]` | `[]` | empty/contain + eof + idx all OK |

The aether EOF pair `17645861, 111938854` reproduces in the calib-aether
observation exactly as the frozen prediction expected (`predicted` ==
`observed`, `match: true`). `s1246-swiss-nethttp` and `real-kimi-webbridge`
each observed one non-empty `invalid_index_reads`, predicted and matched —
i.e. all three C3 diagnostic carriers ({calib-aether, s1246-swiss-nethttp,
real-kimi-webbridge} per claims.json amendment) produced their anomalous read
signature and the compare layer records it mechanically rather than by review
(INFERENCE: mechanism-relevant verdict belongs to the decision-rule seat, not
this one; I report compare-layer facts only).

## Notes / boundaries

- `runs/run-log.txt` under round-18 is a plain log file (a `runs/*/` glob
  catches it); it is not a pair and is excluded — the 15 pair labels come from
  `predictions/*.prediction.json` ∩ `runs/*/compare.json`, which is exactly 15.
- r17 byte-identity is sensitive to cwd because `compare.py:242-243` echoes the
  argv paths into the JSON. Re-run with the same relative-path invocation used
  originally (`predictions/…`, `runs/…` from the round-17 dir). Re-running from
  another cwd with different path spellings would legitimately produce
  different bytes for two lines per file — not a correctness defect, but worth
  noting for anyone re-running (INFERENCE).
- `git status --short` shows no modifications to any lane file read here;
  untracked entries are w2 scaffolding (`gen-wave2.py`, `wave2-*.json`, `w2/`,
  `carriers/bin/`), pre-existing before this seat ran.
- One artifact of the environment: every read/loop ran inside a throwaway
  mktemp dir for outputs; no lane file was written besides this report.
- No installs needed; Python 3 stdlib only. `python3 --version`: system
  `python3` (3.x, exact minor not needed — tool is stdlib-only).

## Verdict basis

- Acceptance "re-run selftest": PASS (CLEAN cases=23, exit 0).
- Acceptance "15 r18 pairs": 15/15 fresh exits 0, fresh stdout byte-identical
  (`cmp -s`) to retained `compare.json`, new-field verdicts all `match: true`.
- Acceptance "8 r17 pairs byte-identical": 8/8 byte-identical, exits 0=0.

Report: .ufo/waves/round-18/w2/CompareNewFields.md
