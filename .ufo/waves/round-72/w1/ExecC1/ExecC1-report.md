# ExecC1 — Report

Report: R72-C1 landing-side evidence independently re-derived GREEN with my own
harness (own shims, own launcher trace, own env parser; seam-probe.py neither
run nor read). Checker-mode children at rev 6316c105…: census {git: 1,
readelf: 4}; all five shim-witnessed exec-boundary environments carry exactly
HOME/LANG/PATH/TMPDIR, no KAIDOKU_ENV_CANARY (exported in caller env, proven),
HOME=`<work>/home` and TMPDIR=`<work>/tmp` exactly — contained under the
checker's `--work`, never /tmp. My per-child records are dict-identical to the
instrument's launcher JSONL, and the checker's own summary
(`checker_child_env`: all_allowlisted true, canary_present false,
home_under_run true, tmpdir_under_run true, records 5) agrees with my census.
Checker rc=0, met=true, failing=[], all clauses true. Four-key allowlist holds
for every checker-mode child; no extra key observed in any corrected record.
Harness finding: a plain `cat /proc/self/environ` inside a `#!/bin/sh` (=bash)
shim reports the cat child's environment augmented with `_/SHLVL/PWD` — a
shim-authored artifact, documented and corrected with an fd-based shim (subrun 1
receipts kept as the artifact record). No tool installs; no git writes; scratch
deleted.

```json
{
  "files_changed": [
    ".ufo/waves/round-72/w1/ExecC1.md",
    ".ufo/waves/round-72/w1/ExecC1/subrun2-fd-records/ (5 exec-boundary records)",
    ".ufo/waves/round-72/w1/ExecC1/subrun2-checker-launcher.jsonl",
    ".ufo/waves/round-72/w1/ExecC1/subrun2-checker-stdout.json",
    ".ufo/waves/round-72/w1/ExecC1/subrun2-analysis.json",
    ".ufo/waves/round-72/w1/ExecC1/subrun2-rc.txt",
    ".ufo/waves/round-72/w1/ExecC1/subrun1-rawcat-records/ (superseded artifact run, 5 records)",
    ".ufo/waves/round-72/w1/ExecC1/subrun1-checker-launcher.jsonl",
    ".ufo/waves/round-72/w1/ExecC1/subrun1-checker-stdout.json",
    ".ufo/waves/round-72/w1/ExecC1/subrun1-analysis.json",
    ".ufo/waves/round-72/w1/ExecC1/subrun1-rc.txt",
    ".ufo/waves/round-72/w1/ExecC1/shims-v2-fd/git",
    ".ufo/waves/round-72/w1/ExecC1/shims-v2-fd/readelf",
    ".ufo/waves/round-72/w1/ExecC1/shims-v1-rawcat/git",
    ".ufo/waves/round-72/w1/ExecC1/shims-v1-rawcat/readelf",
    ".ufo/waves/round-72/w1/ExecC1/caller-env.txt",
    ".ufo/waves/round-72/w1/ExecC1/sha256sums.txt"
  ],
  "behavior": "Independent re-derivation of R72-C1 landing-side evidence: checker-mode children (git x1, readelf x4) at rev 6316c1053f927a1a1cdc3e0960b70acab5f56381 all run under the four-key allowlist HOME/LANG/PATH/TMPDIR with canary absent and HOME/TMPDIR exactly <work>/home and <work>/tmp; checker rc=0 met=true clauses all true; claim verdict GREEN.",
  "evidence": "ExecC1.md (this wave dir) + ExecC1/sha256sums.txt over subrun2-fd-records/*.environ, subrun2-checker-launcher.jsonl, subrun2-checker-stdout.json, subrun2-analysis.json (c1_verdict true), subrun1-* (documented bash-cat artifact run).",
  "risks": "Coverage limited to --check-receipt mode's child census at this revision (no upx/node children there; score mode out of scope). receipt_capsule clause observed true but not independently re-audited (C3 seat scope). Shell-based shims measuring via plain `cat /proc/self/environ` see bash-authored _/SHLVL/PWD keys — other seats' harnesses must use the fd-open (or exec) pattern before calling extra keys a checker violation."
}
```
