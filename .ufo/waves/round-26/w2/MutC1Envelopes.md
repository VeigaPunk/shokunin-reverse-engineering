# MutC1Envelopes — R26-C1 counter envelope checks, wave 2 mutation test

Seat `KaidokuR26.MutC1Envelopes` (mutation tester, leaf). Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, read-only. Claims frozen at `c27f445e70cedbaf5300b2fd0a53e821d9b659a9`, read first; the `R26-C1` `rules` block binds the readings below.

## Method

Sandbox clone `git clone -q <lane> .../seats/w2/MutC1Envelopes/clone`. Baseline commit `fe3eb4edf410244eff46151a148c8f754be1ce80` (lane HEAD at probe time; carries the C1 landing `ebe2cb4a` and the instrument `bd0c84bc`). Instrument under test: the committed `tools/round-26/c1-id-identity.py`, sha256 `11c274220fb5df41ef4467f595cf20a02c8e24240e37c6639308e2816fa918fa`, copied byte-identically into the seat scratch. Detector, once per mutant commit: `python3 -I -B c1-id-identity.py --root <clone> --rev <mutant rev>`. Each mutant is a commit changing only envelope or table bytes; the detector reads Git objects at that commit. Killed = detector turned red (exit 1, `rows_complete` 8 to 7). Survived = detector stayed green (exit 0, 8 of 8) on a mutant that should have been caught. Crash = detector died on an unhandled exception. Per-mutant revs, before/after sha256 and reason lists are in `out/CONSOLIDATED.json`.

**Baseline observation** (2026-10-22T12:59:25Z, `out/baseline.json`): `exit=0 rows_complete=8 entry_ok=1`, stderr empty, tree `784215f955cca6bc678d98d35d9e845f269132df`. The lane instrument against the lane root at the same revision also gives exit 0, 8 of 8, entry_ok 1.

## Mutant table: 52 mutants — 36 killed, 11 survived, 5 crashed

Grouped by mutation class; every mutant id is named, one verdict each.

| Mutants | Change to envelope or table bytes | Exit | rows | Verdict |
|---|---|---|---|---|
| M1, M8, M27, M33 | `ok` false, then `"true"`, then absent, then a dict | 1 | 7 | killed |
| M2, M9, M20 | subject digest sha256 wrong, null, then null with a good `normalized_result` | 1 | 7 | killed |
| M3, M25, M32 | `evidence_id` deleted, then a number, then the bare `ev_` | 1 | 7 | killed |
| M4, M10, M11, M29, M30 | envelope truncated, a JSON array, empty, `.data` a list, `.data.subject` a string | 1 | 7 | killed |
| M38, M39, M40, M41, M42, M50 | 2000 nested arrays, 2000 nested objects, invalid UTF-8, UTF-8 BOM, NUL byte, 50000 nested arrays | 1 | 7 | killed |
| M7, M43 | `.json.gz` that is not a gzip stream, then a gzip stream with trailing garbage | 1 | 7 | killed |
| M12, M35, M36 | only `.json.gz` present: wrong id, `ok` false, wrong subject sha | 1 | 7 | killed |
| M26 | only a `.json.gz` holding `{}` | 1 | 7 | killed |
| M24, M34 | stale truncated `.json` masking a valid `.json.gz`, then a wrong `.json` beside a right `.json.gz` | 1 | 7 | killed |
| M18, M21, M22 | verdict flips: repeat id differs, path-sensitive copy id forced equal to base, `analyze` verdict flipped | 1 | 7 | killed |
| M23, M31 | `analyze` table base id cell emptied, then its table row cut to two cells | 1 | 7 | killed |
| M47, M48 | `analyze-base.json` replaced by `xrefs-base.json`, then by `decompile-base.json` | 1 | 7 | killed |
| M44, M45, M49, M51, M52 | 200000, 500000, 200000-via-`.json.gz`, 100000, 150000 nested arrays | 1 | — | **CRASH** |
| M5 | `analyze-base.json` replaced by an identical `.json.gz` | 0 | 8 | survived (expected) |
| M19 | sha only under `.data.normalized_result.artifact.sha256` | 0 | 8 | survived (expected) |
| M16, M28 | every `evidence_id` stripped (one verb, then all eight), rows set `no-id` | 0 | 8 | survived (expected) |
| M17 | copy id forced equal to base id on `analyze` | 0 | 8 | survived (ineffective mutant) |
| M6, M13 | `.json` plus `.json.gz` with different ids, then with `ok` false and a different id | 0 | 8 | survived (gap) |
| M14, M37 | stray `analyze-base.json.orig`, then `.json.bak`, carrying `ok` false and a different id | 0 | 8 | survived (gap) |
| M15, M46 | `analyze-base.json` replaced by `inspect-base.json` | 0 | 8 | survived (gap) |

### The crash (headline finding)

`json.loads` raises `RecursionError`, not `ValueError`, and the row parser guards only `except ValueError` (`tools/round-26/c1-id-identity.py:318-322`). Uncaught, it aborts the run (M44 at 2026-10-22T13:03:24Z): `RecursionError: Stack overflow (used 8144 kB) while decoding a JSON array from a unicode string`, traceback ending at `c1-id-identity.py:318 obj = json.loads(text)`. The detector still exits 1, so the frozen exit rule holds by luck, but stdout is empty: a caller parsing the JSON report gets nothing and cannot tell a crash from a legitimate red. M50 (50000) parses fine, so the threshold sits between 50k and 60k nesting levels here (`python3 -I -B`, recursionlimit 1000). Coverage finding, not a licence to change the frozen rule.

### Why the survivors survived

M5, M19, M16, M28 are expected: the rule names `.json` **or** `.json.gz`, names `.data.normalized_result.artifact.sha256` as the second subject source, and makes `no-id` a legal derived verdict of which "any verdict counts as complete". M17 was an ineffective mutant — `analyze` was already `content-keyed`, so the bytes changed but the verdict did not (M21 is the real flip, killed).

M6 and M13 are the `.json` plus `.json.gz` ambiguity: the counter loops over the two suffixes and takes the first that exists (`c1-id-identity.py:291-295`), so a committed `.json.gz` with a different `evidence_id` is silently ignored. The frozen rule does not say which wins when both are present, so this is a reading, not a violation — worth disclosing.

M14 and M37: a file named `analyze-base.json.orig` or `analyze-base.json.bak` carrying `ok` false and a different id is never read. The rule names exactly two suffixes, so this is the rule's silence rather than its text.

M15 and M46: `analyze` and `inspect` both report operation `binary_overview` and share evidence id `ev_14f9d92f41c6a4218108768927a622dbd7057ade4bcd305d083e0d6826b3d328`; their envelopes differ in only two leaves, `meta.command` and `meta.duration`. The counter reads neither, so swapping `inspect-base.json` into the `analyze` slot leaves the count at 8 of 8. M47 and M48, substituting an envelope from a verb with a *different* id, are killed. The gap is exactly the one colliding pair, not the envelope checks generally. No crashes elsewhere: every mutant run had empty stderr except the five crashes, and every non-crash mutant produced a well-formed JSON report.

## Restoration evidence

After each batch the clone was returned to baseline with `git checkout -f <base> && git reset --hard <base> && git clean -fd`. `out/restore*.json` (10 records) all show `tree_equal: true`, `git_status: ""`, and `analyze-base.json` back at `3b7c5e4acf86e41402803cc763da8cc66b64626798d9d2ee39ae919788efc2fb`. Final clone tree `784215f955cca6bc678d98d35d9e845f269132df` equals the baseline tree. The lane was never written to by this seat except this report; lane `git status` shows no change under `corpus/evidence/round-26/`, `tools/round-26/` or `corpus/knowledge/`. No `jj` write, no lane Git index write.

## Verdict

The claim's envelope checks **hold** against every envelope-level mutation the frozen rule names: `ok`, subject sha256, `evidence_id`, JSON well-formedness and gzip integrity are all gated, and every verdict flip is caught. The counter's coverage gaps are a crash on deeply nested JSON, an ambiguous `.json` plus `.json.gz` pair resolved silently, stray envelope filenames never read, and the `analyze`/`inspect` evidence-id collision that makes one verb-swap invisible. None is a defect in the instrument's stated contract; each is a place where the frozen rule is silent and the counter chose one reading.

## Artifacts

All under `/fast/scratch/hyaku/kaidoku-r26/seats/w2/MutC1Envelopes/`. The complete per-file listing with a sha256 for each of the 82 files is `MANIFEST.sha256` (`ad3f6de798c34d4f810690a11d62ed9baed6430b24fdebc295b8030e74b27e83`); the 53 per-mutant `out/M*.json` and 10 `out/restore*.json` records are listed there rather than repeated here. Key hashes — instrument `c1-id-identity.py` `11c274220fb5df41ef4467f595cf20a02c8e24240e37c6639308e2816fa918fa`; `out/CONSOLIDATED.json` `4b7121abf0f51de5f06649af46669b127da9f99908733f6c4f6e6e020964491f`; `out/baseline.json` `6ce89b41dc1c577d4d673bc455cdd48ddf0fe2ae77499fc8126ceb1c8eb4f455`; `out/M44_stderr.txt` `adc7c0d9ada04a1dc167a2428954e044a9e25999911266f2c281605867192ee0`; `out/M44_lane_instrument_stderr.txt` `91cff6aba16aee21a85d3ca5b83e982b1af5ac61b86c1951223646f93c5cd388`; `out/M44_stdout.txt` (empty) `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. Harness scripts: `mutate.py` (M1-M7) `b5409e3f4394b55258aaecc942e29b91d066bb955045d8291373aa649e88a2b5`; `mutate2.py` (M8-M14) `ed48078f246003b3a989c2566185e84d9796d14601b973be50a240c203a2bd9a`; `mutate3.py` (M15-M20) `ff5069e5a3d0ec4466d0dd82de863f1928b78cf2a54213c36860f2c7b43613fc`; `mutate4.py` (M21-M27) `fec4a77896d9f25fca65e3f61c272579f87e7c044c5dc6dffba5af1369745ca2`; `mutate5.py` (M28-M33) `2a5b154bb65a26ed2a98b27aa2f56a010e2a93630cc0610104454c73ee85c17a`; `mutate6.py` (M34-M37) `7bc20df8831a669e074511a591437d917fe64aa814922ee70459c7870fbc9a39`; `mutate7.py` (M38-M43) `68a524ed65a6ad544b473ed7353b53c3caa02fbd2793b011e163a5cd3fab2525`; `mutate8.py` (M44-M45) `0d0403a4fa0258ea76f3a6916ebc22cd4a66d6cae14b1dea6de1b1d2fbb5b4c2`; `mutate9.py` (M46-M48) `7af84d2fa2047211a99dae2892b312634b0b17138c32879f630ec1e10c48d103`; `mutate10.py` (M49-M52) in `MANIFEST.sha256`.

## Tools

No tool was installed or upgraded by this seat. `python3` 3.14 and `git` (system). The REA CLI was not needed: this probe attacks the committed envelopes, not the tool that produced them.
