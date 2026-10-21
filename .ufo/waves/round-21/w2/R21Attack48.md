# R21Attack48 — R21-C2 retrospective compatibility, retained R20 label t1246-preprofile

Seat: leaf reviewer/verifier, godspeed. Axes: **calibration** (exact-artifact reproduction of one frozen R20 retrospective result under the R21 comparator) and **depth** (grounding the bounded-null observation against the raw log and cross-checking carrier/version identity). Retrospective regression only — never a fresh forecast. No production edits, no installs/updates performed, no REA, no native carrier execution.

## Assignment (executed as named, nothing more)

1. Hash the bound retained log from `.ufo/waves/round-20/runs/t1246-preprofile/comparison-log-binding.json`.
2. Run `.ufo/waves/round-21/tools/compare-first-failure.py` with the original `.ufo/waves/round-20/tools/first-failure-extract.py` on that log and the frozen prediction `.ufo/waves/round-20/predictions/swiss-misread-v2/t1246-preprofile.json`.
3. Retain argv, stdout, stderr, exit, and digest match.

## 1. Digest match — PASS

Binding (`comparison-log-binding.json`): `log_sha256 = 717744d468bace50903c8b082600bb435482a5082da929ee65a1abb0dd25172f`, `log_path = .ufo/waves/round-20/runs/t1246-preprofile/logs/rea-ghidra-JcCFCG/ghidra.log`, `verified: true`.

```
argv : sha256sum .ufo/waves/round-20/runs/t1246-preprofile/logs/rea-ghidra-JcCFCG/ghidra.log
       (plus wc -c)
stdout: 717744d468bace50903c8b082600bb435482a5082da929ee65a1abb0dd25172f  .../ghidra.log
        15963 (bytes)
exit : 0
```

Recomputed digest equals the bound value exactly. 15963 bytes, 163 newline-terminated lines.

## 2. Assigned comparator run — PASS (exit 0, `failure_match`)

cwd `kaidoku-shokunin`; all paths below relative to it.

```
argv : python3 -I -B .ufo/waves/round-21/tools/compare-first-failure.py
         --prediction .ufo/waves/round-20/predictions/swiss-misread-v2/t1246-preprofile.json
         --log .ufo/waves/round-20/runs/t1246-preprofile/logs/rea-ghidra-JcCFCG/ghidra.log
         --extractor .ufo/waves/round-20/tools/first-failure-extract.py
stdout: {"finding": "failure_match", "last_line": 163, "match": true, "observed": null, "predicted": null}
stderr: (empty)
exit : 0
```

Semantics: the frozen prediction declares `first_failure.h1 = null` (and `h0 = null`, `predicted_failure = false`, `predicted_failure_kind = "none"`, `predicted_eof_reads = []`). The comparator invokes the original extractor itself (`sys.executable -I -B extractor <log>`), validates the `first_failure`/`last_line` envelope, and evaluates kind/index only. Predicted null ∧ observed null → `failure_match`, declared exit 0. Null here means "no qualifying failure through last_line 163", which is exactly the prediction's claim shape — the R21 envelope discipline preserves the frozen R20 semantics rather than silently reinterpreting bounded silence as analysis success.

Supporting standalone extractor run (same named extractor, same bound log; the comparator performs this internally, recorded here for transparency):

```
argv : python3 -I -B .ufo/waves/round-20/tools/first-failure-extract.py
         .ufo/waves/round-20/runs/t1246-preprofile/logs/rea-ghidra-JcCFCG/ghidra.log
stdout: {"cause_line": null, "first_failure": null, "first_failure_line": null,
         "last_line": 163, "log_path": ".../ghidra.log", "other_errors": []}
stderr: (empty)
exit : 0
```

## 3. Depth grounding — the null is a genuine bounded-clean observation

Independent checks against the raw log (inert Python tools + grep counts):

- 163 lines, all newline-terminated → extractor `last_line = 163` is the exact file-final bound (empty-file bound 0 not exercised; N/A here).
- 68 timestamped records match the extractor's `LOG_RE`; the remainder are continuation lines.
- 0 lines contain `ERROR`, `Exception`, or `Go analysis failure` → `other_errors: []` is honest: no Go failure and no unrelated analyzer errors exist in this log at all.
- 17 Go-component records (GoRttiMapper / GoTypeManager / Golang*), all INFO — the log genuinely contains Go analyzer activity, so the null is not "no Go data was ever processed". Sampled: `GoRttiMapper Reading Go binary info: target-789192d566a4.bin`, `Using Go API snapshot for version 1.24.6`, `GoTypeManager Discovered 26 unindexed Go types`, `Found 1152 Go types`.

Same-identity cross-checks against the frozen prediction: `target-789192d566a4.bin` carries the prefix of the prediction's carrier `sha256 = 789192d566a4128506…` (preprofile, go1.24.6); snapshot `1.24.6` matches `go_version`/`go_version_buildinfo` and `snapshot_status = exact_diff` against `go1.24.0.json` + `go1.24.6.json.diff`. The log is the same run the prediction was bound to.

## Verdict

One exact-artifact result: **retained R20 label t1246-preprofile is C2-retrospective-compatible** — frozen `first_failure.h1 = null` vs. observed bounded null through line 163 → `failure_match`, exit 0, digest-verified log. This is 1 of the retained nineteen; the other eighteen labels are out of this seat's scope (separate assignments).

## Caveats, residual risk, verification gaps

- Acceptance caveat honored in both directions: unrelated analyzer errors do not establish success — here there are none (`other_errors` empty), and the match rests on bounded-null vs bounded-null kind/index agreement, not on error absence.
- Not run (outside the named assignment): `compare-first-failure.py --selftest` and `first-failure-extract.py --selftest`; the comparator's malformed-envelope branches (`comparison_unevaluable`, exit 2) were not exercised on this seat — other seats/mutation lanes cover those.
- The bound `last_line = 163` is file-final; the result cannot speak beyond the retained log, and no post-log activity is claimed by the prediction.
- Harness note: the comparator run executed in a temporary shell (session shell busy); no effect on argv/stdout/exit captured above.
- No tool installs/updates; ALL PACMAN TRANSACTIONS PAUSED respected; lane Git/jj/index untouched; only file written is this report.
