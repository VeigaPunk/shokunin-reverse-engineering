HOLDS

# W2 falsify: independent re-derivation of `s1246-swiss-nomethods`

Seat: `KaidokuR18.Runs1246swissnomethods`, an advisory seat on the author side. This verdict is a recommendation, not an admission.
REV `b2aad08ceeee8dd125ce0d316056d8bd766c7f94`; freeze `eb6c2668e5cb7054fd1e16d2f615cb65586d0fe0`; baseline `9011581`.
Lane HEAD = `refs/heads/main` = REV. `git status --porcelain -- .ufo/waves/round-18/runs/s1246-swiss-nomethods/` is empty. Every run file in the worktree is byte-identical to its REV blob (sha256 compared file by file).
Every `path:line` below is at REV (`git show REV:path`) unless marked otherwise. `R` = `.ufo/waves/round-18/runs/s1246-swiss-nomethods`, `LOG` = `R/logs/rea-ghidra-nUpjsE/ghidra.log`, `PRED` = `.ufo/waves/round-18/predictions/s1246-swiss-nomethods.prediction.json`.

## Verdict per field (observed by me from raw log lines; not read from `observation.json`)

| Field | Frozen prediction (`PRED` @ freeze) | Raw-log observation | Verdict |
|---|---|---|---|
| snapshot_route | `info` (`PRED:34`) | Only one `(GoApiSnapshot)` record in the log: `LOG:112` `INFO … Using Go API snapshot for 1.24.6`. No `Falling back from` line, so no WARN route. This is the INFO branch of `GoApiSnapshot.java:158-164` (Base-src.zip) | HOLDS |
| snapshot_label | `1.24.6` (`PRED:33`) | `1.24.6` (`LOG:112`; GoRttiMapper echo at `LOG:113`) | HOLDS. Does not discriminate: it echoes the requested version, as `compare.json:60` itself says |
| fallback_to | `null` (`PRED:31`) | 0 `Falling back from` lines | HOLDS |
| untested_version | `null` (`PRED:35`) | 0 `Untested Go version` lines. 1.24.6 is inside `SUPPORTED_VERSIONS` (`GoRttiMapper.java:170-171`) | HOLDS |
| missing_bootstrap | `false` (`PRED:32`) | 0 `Missing Go bootstrap` lines. `Reading Go binary info` appears once (`LOG:111`), and `LOG:115` reads `Found 776 Go types` | HOLDS |
| `Go analysis failure` (analyzer_errors_empty) | `true` (`PRED:38`) | 0 `Go analysis failure` lines. 0 `ERROR (Golang*` records. The Golang analyzers finished: timings at `LOG:5807-5812`, then `Analysis succeeded` at `LOG:5823` | HOLDS |
| `Invalid index:` values | `[]` (`PRED:40`) | None, across all 5,829 lines including stack-trace continuation lines | HOLDS |
| `Unable to read past EOF:` values | `[]` (`PRED:39`) | None | HOLDS |
| carrier sha256 | `c0ca2748…5789a909` (`PRED:28`) | `sha256sum` of the carrier gives the same value. It also matches `.ufo/waves/round-18/carriers/SHA256SUMS:6`, and the host `SHA256SUMS` is byte-identical to the lane copy (`diff` exit 0) | HOLDS |
| Log binding: session | — | `LOG:2` `Using log file: /tmp/kr17-rea-4c2p8n02/rea-ghidra-nUpjsE/ghidra.log`. That basename equals the retained directory name and matches `receipt.json:2-4` (bound_sessions) and `:1911` (session_dir). The log names exactly one session, 12 times. No other round-18 run directory contains `rea-ghidra-nUpjsE`. `unbound_sessions` is `[]` (`:1989`); baseline and leftovers are `[]` (`:1914`, `:1916`) | HOLDS |
| Log binding: `target-<sha12>` | — | `LOG:46` `IMPORTING: …/target-c0ca274873af.bin`, which is sha256[:12] of the carrier. That is the only target name in the log | HOLDS |
| Log binding: MD5 | — | `LOG:64` `MD5=ab78afb578121465e7eec05901ec24d1`. This equals `md5sum` of the carrier and `receipt.json:6` (`md5_pre`). `receipt.json:1893-1895` records all three binding checks as true | HOLDS |
| Prediction frozen | — | The blob sha256 is `23b9b069…ddcb76` at freeze, at REV, in the worktree, in the mid pin map entry and at `predictions/SHA256SUMS:11`. Only one commit touches `PRED`: `eb6c266`, which is an ancestor of REV. The `main` reflog moved to `eb6c266` at 13:23:55-03:00, before the run started at 13:27:07-03:00 (`runs/run-log.txt:12`; `producer.json:5` records `branch_tip` = `eb6c266`) | HOLDS |
| receipt-validate `--require-mid-maps` | Exit 0 is a binding gate (`predictions/decision-rule.json:2`) | Exit 0: 360 checks, `findings: []`. All 5 negative controls turn the result red (see below) | HOLDS |
| C3 h0/h1 = `none`, `diagnostic: false` (`PRED:16-24`) | — | No failure and no reads. This matches both H0 and H1, so the label cannot discriminate between them (by construction) | HOLDS, but does not discriminate |

The C3 count rule (`decision-rule.json:8`) is met for this label: it has a bound retained log, and `compare.json:43` carries `extra.eof_reads`.

## Commands (cwd = lane root unless shown; exit codes are what I observed)

1. `grep -n -E 'GoApiSnapshot|Go analysis failure|Invalid index:|Unable to read past EOF:|Falling back from|Untested Go version|Missing Go bootstrap' "$LOG"`, exit 0. Only line 112 matches.
2. `for p in 'Go analysis failure' 'Invalid index:' 'Unable to read past EOF:' 'Falling back from' 'Untested Go version' 'Missing Go bootstrap'; do printf '%s=%s\n' "$p" "$(grep -c -F "$p" "$LOG")"; done`, exit 0. Every count is 0.
3. `grep -c -E ' ERROR +\(Golang' "$LOG"` printed `0`, exit 1 (no match).
4. `sed -n '2p;46p;64p' "$LOG"`, exit 0. `sha256sum` and `md5sum` of `~/.local/share/kaidoku-r18/carriers/s1246-swiss-nomethods`, exit 0. `grep -o -E '/tmp/kr17-rea-[A-Za-z0-9_]+/rea-ghidra-[A-Za-z0-9]+' "$LOG" | sort | uniq -c` printed `12 /tmp/kr17-rea-4c2p8n02/rea-ghidra-nUpjsE`, exit 0.
5. `git show REV:$LOG | sha256sum` gave `62d3f710…470915`, exit 0. This equals `receipt.json` `files.ghidra.log.sha256` and `observation.json:161`.
6. `git show eb6c266:$PRED | sha256sum` and `git show b2aad08:$PRED | sha256sum` both gave `23b9b069…`, exit 0. `git log --format='%h %cI' -- $PRED` printed only `eb6c266 2026-10-20T13:23:55-03:00`, exit 0. `git merge-base --is-ancestor eb6c266 b2aad08`, exit 0. `git reflog show --date=iso refs/heads/main`, exit 0.
7. `python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps .ufo/waves/round-18/runs/s1246-swiss-nomethods/receipt.json`, **exit 0**: `"checks_performed": 360, "findings": [], "status": "valid"`. The validator's sha256 `70672eb3…` is the same in the worktree, at REV, at freeze and in the producer pin.
8. `(cd ~/.local/share/kaidoku-r18/carriers && git -C <lane> show REV:.ufo/waves/round-18/carriers/SHA256SUMS | sha256sum -c -)`, exit 0. All 12 carriers OK.
9. Negative controls. Scratch copies in a mkdtemp directory, removed afterwards. Each copy was checked with the same validator command as step 7. The script is a short Python one-liner that mutates the receipt and reruns the validator; the lane was only read. Overall exit 0:
   - `m0` unmodified: exit 0, `[]`
   - `m1` carrier sha set to the noswiss twin's: exit 1, `binding_mismatch, carrier_not_pinned, sha256_mismatch`
   - `m2` retained log sha zeroed: exit 1, `sha256_mismatch`
   - `m3` mid-map sha zeroed: exit 1, `mid_map_sha256_mismatch, sha256_mismatch`
   - `m4` pin_checks dropped: exit 1, `mid_checks_absent`
   - `m5` bound session renamed: exit 1, `binding_mismatch`

   So exit 0 on the real receipt is a result that discriminates, not a vacuous pass.
10. Twin cross-check, run in `runs/` (exit 0):

    | Label | `map_swiss.go` | `map_noswiss.go` | `GOEXPERIMENT` |
    |---|---|---|---|
    | s1246-swiss-nomethods | 27 | 0 | none |
    | s1246-noswiss-nomethods | 0 | 116 | `noswissmap` (inspect-go) |

    This agrees with `true_kind: swiss` (`PRED:23`). These background signals are the same for all four s1246 synthetic twins, so they carry no Swiss-specific signal the frozen fields could have missed:
    - DWARF ERRORs: 47
    - GoTypeManager WARNs: 3 (`LOG:3481-3483`)
    - `Go missing type names: 2`
    - `ERROR (Golang` records: 0
    - GoFuncData overlap ERRORs track code size only: 5554 swiss vs 5448 noswiss.

I also wrote my own extractor (scratch, not using any lane tool). It reproduced every field of `observation.json` (`:2, :8, :155, :163-170`) and every row of `compare.json` (`all_match: true`, `:2`). Exit 0.

## Findings (by severity)

There are no HIGH or MEDIUM findings. The run's fields, its binding and the freeze all hold.

**F1 LOW (calibration), adjacent to this run.** The knowledge entry gives the wrong reason for this label's predicted `none`.

- `corpus/knowledge/2026-10-20-r18-swiss-map-replay.md:80` gives all 8 methods/nomethods labels the H1 reason "none (slot 24 lands on a pkgPath-free name)".
- For this label, the frozen emulator output has `map_types 11`, `misread_map_types 0`, `uncommon_map_types 0` (`.ufo/waves/round-18/predictions/swiss-misread/s1246-swiss-nomethods.json:46,47,253`), and no `per_type` entry has `uncommon`. No uncommon read happens at all, so the "slot 24" path is never reached.
- That reason holds only for the swiss-methods labels (`*main.Counts`, slot_size 24, outcome `silent`).
- For noswiss labels there is no misread at all, because `true_kind` is `old`.
- The outcome columns in that row (INFO exact, no failure, 0 reads) do hold for this label.

Reproduce (exit 0):

```
git show REV:corpus/knowledge/2026-10-20-r18-swiss-map-replay.md | sed -n 80p
for t in s1246-swiss-nomethods s1246-swiss-methods; do git show REV:.ufo/waves/round-18/predictions/swiss-misread/$t.json | python3 -I -B -c "import json,sys;d=json.load(sys.stdin);print('$t',d['map_types'],d['misread_map_types'],d['uncommon_map_types'],[(p['name'],p['slot_size'],p['h1']['outcome']) for p in d['per_type'] if p['uncommon']])"; done
```

Output:

```
s1246-swiss-nomethods 11 0 0 []
s1246-swiss-methods 12 1 1 [('*main.Counts', 24, 'silent')]
```

Suggested fix: say "no uncommon map type" for the nomethods and noswiss rows.

## Residual risk and verification gaps

- **The mid-run map does not cover the Ghidra read window.** Observation:
  - `R/pins/mid-1.json` was taken at 16:27:08.216Z (`receipt.json:1940`). That is 45 ms after the analyze step started (`:1963`).
  - It precedes the first log line (13:27:09-03:00) and the GoApiSnapshot read (`LOG:112`, 13:27:11-03:00, about 2.78 s later).
  - Cause: `carrier-run.py:470` sets `last_pin_check = 0.0` against `time.monotonic()`, and `:39` sets `PIN_CHECK_S = 30.0`, which is longer than the 21.09 s analyze step. The result is exactly one check, taken at about t=0.
  - `receipt-validate.py:25` ignores timestamps, and `:33-36` with `--require-mid-maps` only requires that a map exists.

  Inference: for this run, the guard over the window when typeinfo was read is the equal pre/post pin maps, mtime_ns included (`receipt.json:346-352`). The mid map is effectively a second pre-snapshot. No field verdict changes.

  Reproduce: `sed -n '39p;470p;484p' .ufo/waves/round-17/tools/carrier-run.py` plus the analyze `started/ended/pin_checks` timestamps from `receipt.json`. Exit 0.
- **The log is a polling copy.** `receipt.json:24` discloses this. `LOG:5829` (`ANALYZING changes made by post scripts`) is the final line, and all 15 round-18 logs end on that same line. Inference: the Go symbol analyzer's catch at `GolangSymbolAnalyzer.java:181-183` sits inside the initial auto-analysis, which finished before `LOG:5823`, so any failure from it would already be in the copy. Lines written after the final poll at 16:27:28.761Z (`receipt.json:1909`) are not observed.
- **This label does not discriminate.** H0 and H1 both predict `none`, so "HOLDS" is not evidence for the mechanism.
- **Not checked:**
  - `resume_continuity_v1` does not apply: this run has no resume path.
  - The binding is MD5 plus a 48-bit sha prefix; the full sha256 comes from the on-disk carrier. That is accepted, not independently proven.
  - Commit timestamps and the reflog are self-reported by the local clock.
- No tools were installed or updated. Read-only use: Python 3.14.8 and Ghidra 12.1.4 `Base-src.zip` via `unzip -p` (source only). `rea-agents` 6.5.0 was identified from the npx cache `package.json`; I did not invoke it.
