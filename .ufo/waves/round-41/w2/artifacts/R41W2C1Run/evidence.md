# Evidence transcript — R41W2C1Run

All commands ran from scratch
`S=/fast/scratch/hyaku/kaidoku-r41/R41W2C1Run` (exported `TMPDIR=$S`,
`HYAKU_SCRATCH=/fast/scratch/hyaku`). Lane root
`L=/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. No git mutation; only
read-only `git show/log/ls-files`. No tools installed (nothing to record).

## 1. Carrier build (synthetic, many-symlink AVM-genuine)

```
python3 -I -B gen-synth-carrier.py $S/synth-tree $S/synth-carrier.sqsh
> files 640 links 1600 dirs 160 bytes 265864 sha256 c1336c15e8e3a6d9564e945f5aff233e5f7a707682d4d00708ec1d1a08494f15
` (writer printed "wrote ... 265864 bytes, inodes 2401 mode avm-genuine", exit 0)
```

## 2. Reproduction with the FROZEN harness

```
cd $S && mkdir -p out-synth \
  && C1_KEEP_ENVELOPE=1 bash $L/tools/round-41/c1-run.sh after \
       $S/synth-carrier.sqsh $S/out-synth $S/harness-scratch > harness-run.log 2>&1
echo $?   -> 126
cat harness-run.log
> /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-41/c1-run.sh: line 547: /home/vgpnk/.local/bin/jq: Argument list too long
ls $S/out-synth   -> after.json only (859130 bytes); NO run.json
```

Matches the V4 state byte for byte: `l1/c1-run-V4.log` and
`corpus/evidence/round-41/c1/V4/run-harness-failure.log` are identical
(sha256 `879b7325977987d61c17461c48547cb1fe72a10c2c39507b9fa84864c6b07f3c`,
86 bytes): `tools/round-41/c1-run.sh: line 547: /home/vgpnk/.local/bin/jq: Argument list too long`.

## 3. Same-run envelope identity (instrumented scratch copy)

A scratch copy (not the repo file) added `cp envelope.json outdir/env-before-failure.json`
right after the `mv` of after.json. Same failure point (line 548 in the copy):

```
bash $S/c1-run-instrumented.sh ... -> exit 126, error at line 548
sha256sum $S/out-synth2/after.json
> 96cb2e357e978634fddb38be52d5c524d66c2d1b48560213fba4b15ae01670a8
jq -c '.data' $S/out-synth2/env-before-failure.json | sha256sum
> 96cb2e357e978634fddb38be52d5c524d66c2d1b48560213fba4b15ae01670a8
```

=> after.json == the complete REA `data` object of the same run.

## 4. Independent REA run, projection equality

```
cd $S && mkdir -p rea-work-1 && ( cd rea-work-1 \
  && REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob \
     npx -y rea-agents@6.5.0 extract-firmware --format json --full-output --max-depth 1 \
       $S/synth-carrier.sqsh extract ) > rea-work-1/env.json
exit 0
python3 -I -B project-compare.py $S/out-synth2/after.json $S/rea-work-1/env.json
> equal: True
> files: 640 gaps: 1601 unpublished: 1600
> subject_sha256: c1336c15e8e3a6d9564e945f5aff233e5f7a707682d4d00708ec1d1a08494f15
> engine: {'name': 'unblob', 'version': '26.6.4', ...}
> published_bytes: 163840 coverage: partial
```

(counter's plus-extractor profile: files/chunks/gaps/unpublished/diagnostics +
subject, derivations, engine, published_bytes, coverage).

## 5. Summary-size table (harness's exact `summary` jq filter)

| receipt | summary bytes | > MAX_ARG_STRLEN (131071)? |
|---|---|---|
| V3 | 18441 | no |
| V4 | 146561 | **yes** |
| L3 | 1479 | no |
| L4 | 1465 | no |
| synth | 316046 | yes |

## 6. E2BIG boundary proof (jq 1.8.2, /home/vgpnk/.local/bin/jq)

```
for N in 131071 131072; do S="$(printf 'x%.0s' $(seq 1 $N))"; jq -n --arg s "$S" '{len:($s|length)}' >/dev/null 2>err; echo "N=$N exit=$? $(cat err)"; done
> N=131071 exit=0
> N=131072 exit=126 error: failed to execute command '/home/vgpnk/.local/bin/jq': Argument list too long (os error 7)
jq -n $(for i in $(seq 1 2000); do printf -- '--arg a%d x ' $i; done) true   -> exit 0
```

=> the failure is the per-argument cap (MAX_ARG_STRLEN = 131072 incl. NUL), not
total argv size.

## 7. Fixed harness validation (same synthetic carrier)

Run `c1-run-fixed.sh` (= original + the fix diff in this artifacts dir):

```
bash $S/c1-run-fixed.sh after $S/synth-carrier.sqsh $S/out-fixed2 $S/harness-fixed2 -> exit 0
ls $S/out-fixed2 -> after.json, after.envelope.json, run.json
jq -c '{exit, receipt_written, data_extracted, summary_files: .envelope_data_summary.files, receipt_sha: .receipt.sha256, receipt_bytes: .receipt.bytes}' $S/out-fixed2/run.json
> {"exit":0,"receipt_written":true,"data_extracted":true,"summary_files":640,"receipt_sha":"d32b9c6537eb059e1ec37545daea61aa2434fa7fa5a65c33f5df7f6ce66100aa","receipt_bytes":858479}
sha256sum $S/out-fixed2/after.json
> d32b9c6537eb059e1ec37545daea61aa2434fa7fa5a65c33f5df7f6ce66100aa
jq -c '.data' $S/out-fixed2/after.envelope.json | sha256sum
> d32b9c6537eb059e1ec37545daea61aa2434fa7fa5a65c33f5df7f6ce66100aa
```

V4-scale check (receipt-style jq via `--slurpfile` with the real V4 summary,
146561 bytes):

```
jq -n --arg sha deadbeef --argjson bytes 2852279 --slurpfile summary sum-V4.json \
  '{path:"after.json",sha256:$sha,bytes:$bytes} + $summary[0]' | jq -c '{path, sha256, bytes, files: .files, gaps: .gaps, unpublished: (.unpublished_entries|length)}'
> {"path":"after.json","sha256":"deadbeef","bytes":2852279,"files":6349,"gaps":612,"unpublished":611}
```

## 8. Counter dependence on run.json

- `grep -n 'run\.json' tools/round-41/c1-counter.py tools/round-41/c1-extra.py` -> no matches.
- Lane-wide grep for `run.json` consumers: only writers (`tools/round-41/c1-run.sh`
  lines 16/80/600/603) and unrelated heldout generators / older rounds
  (round-36/37/39/40). `plans/round-41-claims.md` mentions only `oracle-run.json`.
- c1-counter.py bindings (`receipt_present`, `subject_pin_ok`, `operation_ok`,
  `handler_ok`, `chunks_ok`, `oracle_hits_ok`, `gaps_ok`, `nonregular_unpublished_ok`,
  `run_provenance_ok` (reads `parameters.output_directory` from after.json),
  `evidence_id_ok`, `projection_ok`) all consume after.json + oracle/nonregular
  tables + docs. c1-extra.py reads no receipts at all.
- Score receipt `l1/scores/c1-at-e9a24d07.json` records V4 `receipt_present true`,
  `projection_ok true` (counter-time REA rerun, `projection_diff: []`), 4/4
  matched, exit 0.

## 9. V4 after.json is a complete REA data object

Committed file sha256 `1efa815f5cf2412e979b85b3e20842606239858efb67a3e195ed1fc32b20d60e`
(2852279 bytes). Top-level keys exactly equal a fresh REA 6.5.0 data object
(`analysis_profile, authority, confidence, environment, evidence_id,
evidence_links, limitations, locations, normalized_result, operation, parameters,
predicate_type, provider, raw_result, relationship_coverage, subject`); identical
`normalized_result` key set; `files 6349`, `gaps 612`, `unpublished 611`,
`diagnostics 4` (MaliciousSymlinkRemoved), one `squashfs_v4_be` chunk with
`extraction_failed false`, `subject == carrier pin ce27ebca…087f`, `operation
extract_firmware`, `provider unblob`, `parameters.max_depth 1 / max_output_files
10000`, output_directory under a `/kaidoku-r41/` scratch segment.

## 10. Intermittent REA/unblob ENOENT flake (separate finding)

Two runs failed with `execution_failure` / `ENOENT: no such file or directory,
readlink '<stage>/extracted/firmware.bin_extract/dN0/lNN'` (different directories
each time) while eleven runs on the same bytes succeeded (fresh outdirs). A
pre-existing outdir triggers a different, deterministic refusal
(`Extraction output root already exists`). Both are REA/unblob-environment
phenomena, not harness logic; the counter-time rerun on V4 was unaffected
(projection_ok true at e9a24d07).
