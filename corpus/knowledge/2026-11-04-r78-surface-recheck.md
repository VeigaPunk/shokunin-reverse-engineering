source: S293 — https://docs.python.org/3/library/tomllib.html — Python 3.15.2 docs, module introduction, line 221; opened 2026-11-04
verified-at: 2026-11-04
recheck: 180d

# A surface value is re-derived from the live object its record names, never from a token in the text

## The record's prose is a claim; the live object is the evidence

`PROVINCE.md` records the three client `rea` pins, the Ghidra provider and the JDK as prose. A token
grep answers "does the string appear", not "does the named client request this package": the OMP
config carries `disabledServers: ["rea"]` beside a `rea` entry whose args still say
`rea-agents@6.7.0`, and the round-77 text said the live file no longer recorded the disable. The
round-78 recheck parses each recorded value with a declared pattern and reads the object the record
names, so the disable is its own check (`omp-rea-disable`) and a value that appears only in a comment
or another client is not a match. The control `--control token-grep` accepts a forged
`ghidra_version 8.5` because `application.gradle.min=8.5` sits in the same live file
(selftest case `red-token-grep-accepts`).

## TOML is parsed, not grepped

The Kimi pin lives in `~/.kimi-code/config.toml`. The docs: "This module provides an interface for
parsing TOML 1.1.0 … This module does not support writing TOML." (`tomllib.html`, snapshot line 221,
34 923 B, sha256 `d98e62f7…`). The recheck loads the file with `tomllib`, reads
`mcp_servers.rea.args` and matches `rea-agents@<version>` in the joined args; it never writes the file
and never dumps its `env` block (the receipt records the pin, the `disabledServers` presence and the
declared source path only — QUALITY row 128). A parse failure is an `unparsed` id, never a pass.

## Two live drifts the recheck found at the base revision

- `jdk-version`: the record said `openjdk version "21.0.12.1"` (2026-10-20); the host returns
  `openjdk version "21.0.13" 2026-10-20`.
- `omp-rea-disable`: the record said the live OMP file no longer records the disable; the live file
  records it in `disabledServers: ["rea"]`.

Both are corrected in `PROVINCE.md` with the round-78 receipt pointer, and the after receipt is
`.ufo/waves/round-78/l1/scores/c2-at-record.json` (`checks_total 8, matched 8, mismatches 0`). The
receipt carries `checked_at`: a later host change invalidates the observation, and the next round
re-runs the command rather than trusting the date.
