# CtlLabels — filename lookup and size-keyed fixed-slice replay

## Result

**Decisive skip-work-control miss:** size-keyed fixed-offset replay meets the unchanged frozen predicate at **12/12, both schedules**, with `documents_ok=true`, exit **0**, `finding=version_needs_match`. Exact restoration independently repeats 12/12. Runtime performs no ELF header, section, Verneed or Vernaux decoding. The initial filename/id/source-path control remains retained and was rejected.

The frozen kill rule says: “Any fresh skip-work control meeting this predicate stops the claim before production; no target/predicate/counter amendment after production scoring.” The parent was notified of the target-met control. No counter, rule, target, approved document or production reader was repaired or run. This report supplies control evidence, not an admission judgment or production score.

## Axes and frozen contract

- Claim axis: **depth**, not coverage. Probe axes: control discrimination, bounded cost, content-read boundary and exact restoration.
- Sandbox: `/fast/scratch/hyaku/kaidoku-r34/w1/CtlLabels`.
- Freeze and measured revision, every run: `54a87a51a865ab931fd355e767303337b05cccf4`.
- Unchanged running/frozen counter SHA-256: `d7f0a8cf3ca08562437d40711d15e7ad4f6fa44edb4e8934c36f4673e4e7c45e`.
- Frozen manifest SHA-256: `f22e7e3b8f70c7a5dda784919f6df53a1feaf11cca0e4bba767509d51717974d`.

Predicate preserved verbatim:

> P34-version-needs: twelve public ELF carriers yield exactly their independently frozen GNU version-needs records on opaque paths, including randomized same-length string-table naming wherever requirements are present, and the pinned source-backed decision table is present.

## Controls

### Original assignment: label lookup, no carrier-content reads

`label_lookup.py` embeds all twelve complete frozen expected records and sixty aliases: carrier id, carrier filename, manifest path, original source path and source basename. It selects by argv text/full path or basename only; an unknown label defaults to e12's empty record. Its only calls are dictionary lookup, string splitting, JSON output and stdout/stderr writes. It never opens/stats/reads the supplied carrier or hashes its contents. The builder reads the frozen JSON manifest, not carrier bytes.

Opaque argv produces **zero alias hits in all 24 attempts**. A one-token fallback mutation, `"e12"` → `"e01"`, retains the whole lookup table but guesses the first record instead. Schedule 0 then accidentally matches e01; randomized schedule 1 matches none.

### Priority extension: size-keyed fixed-position replay

`build_size_control.py` reads the frozen manifest and public original Git blobs, verifies their size/digest, and searches each supplied string-table window for the expected strings once. It does not decode ELF structures. All twelve sizes are unique. It emits `size_lookup.py` with:

- input identity solely from `os.fstat(descriptor).st_size`;
- fixed absolute string offsets and fixed string lengths;
- memoized record topology and every `flags`, `other`, `hash` field;
- only exact-length `os.pread` string-slice reads, followed by name-dependent sorting.

Across twelve carriers, each schedule reads **395 slices / 5,741 bytes**. e12 returns empty without reading contents. Same-length string-table permutation changes the bytes at the stored positions, so this replay adapts without recovering any record structure. Neither filenames nor input-content hashes select the template. Original binary bytes remain pinned in sandbox Git at the measured freeze; no binary fixture was authored or copied into the archive.

## Observed bounded detector outputs

Schedule 0 is original metadata; schedule 1 has eleven randomized transformed inputs and unchanged empty e12. Every reader subprocess exited 0; all six counter receipts have `documents_ok=true`, and none timed out.

| Control/state | Observed UTC start | Schedule 0 matches | Schedule 1 matches | Paired carriers | Detector exit |
|---|---|---:|---:|---:|---:|
| Labels pristine | 10:55:35.589502Z | 1, e12 | 1, e12 | 1/12 | 1 |
| Labels fallback e01 | 10:55:49.984437Z | 1, e01 | 0 | 0/12 | 1 |
| Labels restored | 10:56:03.725956Z | 1, e12 | 1, e12 | 1/12 | 1 |
| Size replay pristine | 11:00:35.635552Z | 12 | 12 | **12/12** | **0** |
| Size replay offset +1 | 11:00:54.707502Z | 1, e12 | 1, e12 | 1/12 | 1 |
| Size replay restored | 11:01:17.287296Z | 12 | 12 | **12/12** | **0** |

All timestamps are 2026-10-23. Exit-1 findings are `version_needs_mismatch`; exit-0 findings are `version_needs_match`. Full receipts include both schedules' observed JSON, child argv, actual exit, stderr, input/output hashes and complete random translation tables—not only final exit codes.

## Mutants and exact restoration

- **Label fallback mutant: inconclusive as a killed-mutant test**, because its pristine baseline already fails. Separately, the label-only control is demonstrably rejected.
  - Before/restored SHA-256: `cc346fe2f04b8ac5d69f11e936ff61641b228cb28def1f6608dafe7a71a1f180`.
  - Mutated: `58e312dc9ab08cc3be8f4b83082ef99e8ebf29016c039b88fc14052c6672930b`.
- **Size replay off-by-one mutant: killed.** The smallest runtime read point changes `offset` to `offset + 1`; the same frozen detector changes green → mismatch → green. This does not erase the decisive unmutated replay miss.
  - Before/restored SHA-256: `c68511f7bc2d10b005847139a5ef70331f50634a84d3d1ae63c762c570460b22`.
  - Mutated: `4ad7dfcd72665f77afb923eca02d95164618d0635520dbff55643f6623ebdec6`.

Both controls were restored byte-for-byte. Counter hashes agree before/after every run. Every owned process group was absent when its probe returned.

## Reproducible receipt archive and containment

All evidence is under [CtlLabels-files/](CtlLabels-files/):

- `summary.json`, `restoration.json`, `build-receipt.json`, `label_lookup*.py`, `build_control.py`, `run_control_probe.py` and pristine/mutated/restored `*.receipt.json`, `*.stdout.json`, `*.stderr.txt` retain the first control.
- `size-summary.json`, `size-restoration.json`, `size-build.receipt.json`, `size_lookup*.py`, `build_size_control.py`, `run_size_probe.py` and `size-{pristine,mutated,restored}.*` retain the decisive control.
- `claims.freeze.json`, `manifest.freeze.json`, `counter.freeze.py` preserve exact frozen text inputs/instrument bytes. The size-build receipt records every original-blob Git argv, UTC, exit, size/digest and exact frozen Git object path.
- `archive-index.json` and `size-archive-index.json` record each archived artifact's byte count and SHA-256.

Each `*.receipt.json` retains the exact exercised argv and complete stdout/stderr/exit. Both runners invoke only `/usr/bin/python3 -I -B` with the unchanged frozen counter, `--root` set to this sandbox, `--rev` and `--freeze` both the revision above, and explicit `--control-reader`. Detector bounds are 35 seconds plus two-second kill grace, 512 MiB address space per process, 30 CPU seconds, 128 descriptors, 4 MiB written-file cap and process limit 4096, with only one owned child tree at a time. Builders also ran under bounded timeout/prlimit. No additional behavioral checks were run.

Lane writes are limited to this report and its named archive. Sandbox LOG records both probes; no Git writes/commits/pushes occurred. No production reader invocation, target execution, REA run, held-item reconstruction or other-seat modification occurred. No tools were installed/updated. Existing Python reports 3.14.8; prlimit reports util-linux 2.42.4. Visible answering-model context is `openai-codex/gpt-6.1-sol`; no independent provider query or fallback was observed.
