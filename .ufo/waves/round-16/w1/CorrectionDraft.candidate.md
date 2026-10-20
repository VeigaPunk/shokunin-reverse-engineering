## Round-16 correction — r15 snapshot-inventory recheck invocation (append-only)

Scope: this correction qualifies the `recheck:` line (line 3) and the "Executed inventory" paragraph (lines 52–53) of this entry. Those lines are not rewritten. It discharges round-15 verifier routed defect 1 (`corpus/lessons/round-15-verifier-spotcheck.md:185-186`, "Invocation consistency"). It adds no new run, target, or capability claim.

Two invocations are distinguished. They are not interchangeable as evidence.

**1. Exact recorded invocation (executed, retained).** Argv as recorded in `.ufo/waves/round-15/verification.json`, commands labelled `snapshot-inventory` (lines 28–44) and `inventory-determinism` (lines 45–61), at source revision `7ad23fe1735cd868ec203d93deb13bb2c42889ad`:

```text
python3 -I /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/snapshot-inventory.py --ghidra /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC --select 1.24.7 1.25.7 1.26.8
```

Both runs exited 0 (`verification.json:41,58`). `verification.json:159` records `inventory_equal: true`, and `:180` records the inventory SHA-256 `ad06fadc0166e172d65325e3366375e2d4a9730d714d154bbcd98137539bb2fe`. This is the only argv that this entry's inventory result rests on.

An earlier run with the same `-I` absolute-path argv, at the failed revision `856d193b8c21d3f7aeff3cb8a27b55a715ab897e`, exited 1 with a traceback at the `scan_directory` sort (`.ufo/waves/round-15/verification-initial.json:41-43,58-60`; the retained stderr is truncated before the exception type). That failure was repaired in code and is not a failure of the invocation form. The repaired sort is at `snapshot-inventory.py:321` in the current file.

**2. Source-only preview (the `recheck:` line, not an executed argv).** Line 3 reads:

```text
python3 .ufo/waves/round-15/snapshot-inventory.py --ghidra /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC --select 1.24.7 1.25.7 1.26.8
```

This is the probe's own CLI surface (`snapshot-inventory.py:406-417` argparse: `--ghidra`, `--select`), written as a relative path with no interpreter isolation flag. No retained record executes this exact string. Therefore the statement in lines 52–53 that "the `recheck:` command above ran twice" is an overstatement of the literal string. What ran twice is the `-I` absolute-path form in part 1.

**What is and is not observed.** Observed: the part-1 argv exited 0 twice with equal output at the stated revision. Not observed: that the part-2 spelling produces the same bytes, and whether `-I` changes any output. The probe imports only standard-library modules (`snapshot-inventory.py:55-61`) and emits `sort_keys=True` output with absolute paths. On that basis the flag is expected to be output-neutral, but that is `[INFERENCE]`, not a measurement. `-I` isolates the interpreter by ignoring `PYTHON*` environment variables and omitting the script directory from `sys.path`. The source directory is not imported here, so the probe's own import path does not depend on it.

**Consequence for future rechecks.** A recheck of this entry should run the part-1 argv verbatim, with `-I` and the absolute script path, and compare the regenerated stdout with `.ufo/waves/round-15/inventory.json` (filename, size, SHA-256, parsed summaries). A relative-path or non-isolated run is an unrecorded variant. It may be used as a diagnostic, but it must be labelled as such and cannot replace the recorded invocation. A changed result is drift to investigate, as the entry's `recheck:` line already says. It is not an automatic failed verdict.

Retained-record pointers: `.ufo/waves/round-15/verification.json`, `.ufo/waves/round-15/verification-initial.json`, `.ufo/waves/round-15/snapshot-inventory.py`.
