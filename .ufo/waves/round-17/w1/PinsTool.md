# PinsTool — W/tools/pins.py (R16-PROVENANCE fix)

## Files changed
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/tools/pins.py` (new, 298 lines, stdlib only; no other file touched).

## Behavior vs contract (contract.md:12-20)
Observed, all exercised:
- `snapshot(paths)` → `{taken_at_utc (µs ISO-8601), monotonic_ns, entries{abs_path: {sha256,size,mtime_ns}|{error}}}` — pins.py:62-72; per-path entry builder pins.py:37-59 with a stat→hash→stat recheck that reports `changed during read` instead of a false pin (pins.py:51-53).
- `compare(pre, post)` → `{equal, changed, missing, errors, pre_taken_at_utc, post_taken_at_utc}` — pins.py:75-106. `equal` false on any sha256/size diff, any path absent from either snapshot, or any error entry — including *identical* errors on both sides (errored pins can never prove same-bytes, pins.py:87-95). Extra `errors` list added beyond contract's minimum keys; contract keys unchanged.
- Deleted-file classification: `FileNotFoundError` opposite a real entry lands in `missing`, not `errors` (pins.py:91-93) — inferred that "missing" should mean vanished-from-disk; flagged by the first selftest run.
- CLI `snapshot --out FILE PATH...`: writes atomically (`.tmp` + `os.replace`, pins.py:118-123) and also emits JSON on stdout; exit 0, exit 2 on unwritable out dir.
- CLI `compare PRE POST`: JSON on stdout, exit 0/1/2; differing paths also named on stderr (pins.py:155-159).
- `--help` epilog states the honesty boundary: "only 'same bytes at two instants'; it never proves a path was unchanged throughout" (pins.py:280-282; verified in `pins.py --help` output).
- Selftest pins.py:160-269, 7 cases: API green/CLI green compares, the required CLI red case (snapshot → mutate temp file → snapshot → compare → exit 1, path in `changed`, pins.py:232-249), API missing, API identical-error-not-equal, CLI exit-2s (unreadable input, invalid JSON, nonexistent out dir). Fixtures under `tempfile.mkdtemp`, removed in `finally`.

## Selftest runs (observed)
1st run (before FileNotFoundError classification fix): `SELFTEST: FAILED api-missing: ...` exit 1 — deleted file classified as `errors`, not `missing`. Fixed at pins.py:87-95.

Final run, exact output:
```
red case observed: compare exit 1 names /tmp/pins-selftest-e8vz7xs0/a.txt
SELFTEST: CLEAN cases=7
EXIT=0
```
(Red case: `compare` exited 1 and its JSON `changed` list named the mutated temp path, as required.)

## Design notes / limits
- Paths canonicalized via `os.path.realpath` (pins.py:66): keys are abs canonical; a symlinked and direct spelling of one file dedupe to one entry [inference: matches contract "abs_path" intent].
- Two errors on the same path never compare equal (pins.py:87-95): a permission-blip pair is not evidence of stable bytes.
- `equal` never depends on mtime_ns (pins.py:96): sha256+size decide; mtime is recorded for context only. A same-bytes rewrite is invisible — consistent with "same bytes at two instants".
- Limit: pin pairs are endpoint evidence only; cannot exclude modify-and-restore within the interval, or adversarial size+mtime preservation. This is exactly the R16-PROVENANCE boundary now stated in `--help`.
- Limit: `snapshot` emits JSON to stdout *and* writes `--out`; `retain.py` consumes the API, so no receipt ambiguity.
- No carrier binaries executed; no REA/Ghidra invoked; subprocesses in selftest are `sys.executable -I pins.py` only.

## Installs
None. Host untouched.
