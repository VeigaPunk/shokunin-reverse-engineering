# ArgvAndPaths (wave 2 falsify): are the 24 envelopes the frozen calls?

Seat: KaidokuR26.ArgvAndPaths (leaf), 2026-10-22. Judged at REV fe3eb4edf410244eff46151a148c8f754be1ce80 (lane HEAD at start). The envelope directory last changed in ebe2cb4a, so its bytes are identical there. claims.json blob b3d0fc23ff3ad1cdcdafab498d2b81361fff6562 matches at c27f445e and at REV.

## Verdict
Holds. All 24 envelopes pass every Work-list check; per-envelope failures: none. Gaps in what the bytes can prove are listed below; none is a failed check.

## Per-envelope checks (24 of 24 pass each)
Per envelope: ok is true; .meta.command equals the verb; subject local_path is /usr/bin/jq (base, repeat) or the alt path (copy); subject sha256 is e815667571d0...; .data.parameters equals the argv values; file sha256 is not 689680863a6e...; the runs.tsv row agrees (path, argv, exit 0, sha, evidence id, subject sha); the table id cell equals the envelope id; the blob equals the REV blob.

| verb | base | repeat | copy (sha256 prefix) | parameters (base) |
|---|---|---|---|---|
| analyze | 3b7c5e4acf86 | b65e650292b9 | be1dd0c4c57d | {} |
| inspect | 9421d1f87019 | f509fcfeb1ab | 62e09a1e8ecb | {} |
| decompile | b177af90a49a | 779d6ffce7e1 | bc8d40c38880 | procedure 0x103fa0 |
| xrefs | 125ee6d20bda | dd68e7835954 | 6587e077e6d4 | address 0x103fa0 |
| read-bytes | 3eb2f92c3d98 | b6fa9c4eae2b | 5a893e0e0b5d | address 0x103fa0, length 64 |
| function | 642c47b3134e | 40616d467649 | 6dafee18478e | procedure 0x103fa0 |
| instructions | c8852498ce38 | 00da0fb3d1b8 | f87583348512 | procedure 0x103fa0 |
| inspect-binary-layout | 4a256cc73b54 | 98a1a229f20e | bfa78b4d3a41 | path /usr/bin/jq (copy: alt path) |

All 24 sha256 values are distinct, so base, repeat and copy are pairwise distinct for every verb.
Probe: no envelope equals 689680863a6e3dbd8c5a442aee52042a4601fd37e0555aa6db66d3a8ab3b195a. The probe file (/fast/scratch/hyaku/kaidoku-r26/l1/probe-ibl.json) has that hash, and its JSON equals committed inspect-binary-layout base and repeat except meta.duration. The base row is a new run with the same content, not the probe bytes.
Command: `python3 -I -B check_argv_paths.py` (scratch), exit 0, 13:05:22Z; output `envelopes_all_checks_pass 24 of 24`, `OVERALL_PASS True`.

## Findings
### Low-1 (gap, partly mitigated): flags, TMPDIR, package version and environment are not in the bytes
- Output: `raw_token_counts_across_24 {'--full-output': 0, '--format': 0, 'TMPDIR': 0, 'rea-agents': 0, '6.5.0': 0, 'npx': 0}` and `meta_key_sets {('command', 'duration')}`. `jq -c .meta analyze-base.json` prints `{"command":"analyze","duration":"5912ms"}`.
- The flags therefore rest on seat-written records: runs.tsv argv, run_one.sh (sha256 424f8ea8de1b1e926c51809e7651e4aa27d4a7618285d3efe377e067d893c83e), driver templates and wave-1 reports. They show the intended argv, not the argv the process received.
- Partial check, analyze only: without --full-output the output is a bare payload with 16 top-level keys and no ok/data/meta wrapper (raw/ablate-analyze-no-full-output.json, 7491 bytes, exit 0, 13:08:10Z). All 24 committed envelopes carry the wrapper. Seven verbs were not ablated.
- Version: the 6.5.0 root package.json reports 6.5.0. `find -newer` against a 12:11:50Z reference stamp lists only the root directory, under both npx roots. Which root npx resolved for each run is unknown.

### Low-2 (wording): claims.json says "base and repeat use PATH=/usr/bin/jq"
- Read literally, PATH is the shell variable. The runs passed the path as the `<PATH>` argument (runs.tsv argv; driver `tmpl.format(p=path)`). Suggest "the <PATH> argument". Not gating.

### Observation-1 (disclosed): analyze and inspect are one operation
- `analyze_vs_inspect_base_diff ['/meta/command', '/meta/duration']`; same id ev_14f9d92f41c6... The knowledge entry (lines 49-52) discloses this. Eight frozen verbs give seven independent identities.

### Observation-2: "byte-distinct" holds only through the duration field
- `norm analyze base_vs_repeat_diff ['/meta/duration']`, the same for all eight verbs. Pairwise distinct 8 of 8. Under a content-distinct reading, base and repeat would fail 8 of 8. The L1 should state which reading it uses.

### Observation-3: copies differ from base in path text only, plus evidence id for inspect-binary-layout
- After swapping the alt path back to /usr/bin/jq: diff ['/meta/duration'] for seven verbs, ['/data/evidence_id', '/meta/duration'] for inspect-binary-layout. The probe-to-copy diff touches four path places; 4 x 35 = 140 = 80205 - 80065. This matches the path-sensitive verdict.

### Observation-4: run windows overlap across seats
- `run_window_overlaps 18 cross_seat_overlaps 18`; `seat_sequential True` for all four seats. The wave-1 spec says "Run your REA calls one after another, not in parallel", which is per seat. No stated rule is broken and no content shows perturbation.

## Process checks (no failure)
- Lane copies equal seat originals by sha256: 24 of 24. Seat originals were written 0.11 to 0.81 s after their recorded utc_end: 24 of 24.
- Stderr captures: 24 files, all 0 bytes. No attempt files or -attempt1 rows.
- Freeze commit c27f445e, committer 2026-10-22T09:01:20-03:00 (12:01:20Z): after the probe (11:59:16Z), before the first table run (12:11:50Z).
- Carrier /usr/bin/jq: sha e815667571d0..., 30800 bytes, inode 125895. Alt copy: regular file (not a symlink), inode 1481018327, sha equal, filecmp equal, mtime 2026-10-22T11:59:15.936886Z.

## Reproduction (my REA calls; scratch output only; one at a time; login shell)
1. `analyze /usr/bin/jq --format json --full-output`, exit 0, 13:08:03Z: JSON diff against committed analyze-base is ['/meta/duration'].
2. Same without --full-output, exit 0, 13:08:10Z: different shape (Low-1).
3. `inspect-binary-layout <alt path> --format json --full-output`, exit 0, 13:08:49Z: diff ['/meta/duration']; ev_52da4b3df646 equal.
4. `read-bytes /usr/bin/jq 0x103fa0 --length 64 --format json --full-output`, exit 0, 13:08:55Z: diff ['/meta/duration']; ev_99b0c6e1f03c equal.
Three of eight verbs reproduce as JSON equal apart from duration (sizes equal), on this host now.

## Checker history
The first run exited 1. Its normalized check allowed only meta.duration, but the inspect-binary-layout copy also differs in data.evidence_id, the path-sensitive verb. I widened the allowance for that verb only and added the analyze-versus-inspect line. The second run exited 0 at 13:05:22Z. The first run's output was not saved; raw/check_output.txt is the second run.

## Gaps
- Five verbs not reproduced (decompile, function, instructions, xrefs, inspect); flags not ablated for seven verbs; npx resolution and run environment of the committed runs not recorded.
- Parameter key names (procedure, address, path) come from the observed envelopes; the claim fixes only the argv values.

## Artifacts (sha256; scratch /fast/scratch/hyaku/kaidoku-r26/seats/w2/ArgvAndPaths/)
- check_argv_paths.py 63214529f8a8df9bb443f662b9f2e40456059191493f9cd30671eb544a34c1a1
- raw/check_output.txt and raw/run_stdout.txt bddb02f8c7559fc3059ee7203e67847329b2d006133d0c53f88585488ae1cfdd
- raw/repro-analyze-base.json 8f62c45a51c95ffb4ad7b7188834c7ea3877f1236109e20cea2037b5ec529208
- raw/ablate-analyze-no-full-output.json 4a51c1b091deb527633355c77a2cb99a361c85eaf50e954f34abbeca644aba76
- raw/repro-ibl-copy.json 75305e277e3df323aa1a217488adc24a3f5011825fd0fff46cdfdf72a2c7bb72
- raw/repro-read-bytes-base.json 995088f7f8d80fe9db02cb82190df05e8b1de0ad9fa6df84e8bf5fa7b89f8b13
- four .stderr captures e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 (empty)

## Tooling
No install or upgrade. Used python3 standard library (-I -B), /usr/bin/jq to read envelopes, read-only git (ls-tree, show, log, rev-parse, diff --name-only, hash-object without -w), find, stat and sha256sum. REA: rea-agents@6.5.0 via npx (cache ad9a3fdbcad992c6), four calls, all on /usr/bin/jq or its alt copy, no MCP. The only lane write is this report.

## For the main agent
Nothing required beyond optionally re-running check_argv_paths.py (exit 0 expected).
