# R22-C2 counter probe review

## Verdict

No actionable finding for the assigned attack against the current `count-c2.py`. The current check binds all three command identities: frozen T2 row `verb`, row `probe`, and receipt `meta.command`. In `check()` at lines 127–128, `row["probe"] != row["verb"]` returns `probe_mismatch` before an observation can match. The docstring at lines 10–11 describes the same contract.

This equality guard is material: the pre-guard counter at revision `75f04a4` accepted the same attack (14/14, exit 0); current code rejects it (13/14, exit 1). This is evidence for the guard, not a finding against the current version.

## Probe evidence

All counter runs were against `/tmp/r22c2probe/lane`, a private scratch clone. The current worktree counter was copied there; its SHA-256 was `0a5f2a41a9801e2ac421fd61766ec926cc69f7f96d66be8a18b7ced780b8f7a0`, equal to the scratch copy at execution. No production source, PROVINCE, or receipt was changed.

The positive case used revision `2ee3d9f51c6a995d1aefe48f6a44cfd08d492d67`:

```text
argv: ["python3", "-I", "-B", "/tmp/r22c2probe/lane/.ufo/waves/round-22/tools/count-c2.py", "--root", "/tmp/r22c2probe/lane", "--rev", "2ee3d9f51c6a995d1aefe48f6a44cfd08d492d67"]
exit: 0
stderr: ""
stdout bytes: 5751
```

The adversarial scratch revision `034df7ddb2d3dcc3a2efc2ba53126ea10ec80ec6` changed only the test fixture to `verb=inspect-packet-fields`, `probe=inspect-pcap-client`, and receipt `meta.command=inspect-pcap-client` (the probe command); the receipt's matching `capability_unavailable` outcome was otherwise retained. Current code returned `probe_mismatch` for `inspect-packet-fields`, `accounted_count: 13`, `mismatched: ["inspect-packet-fields"]`, exit 1:

```text
argv: ["python3", "-I", "-B", "/tmp/r22c2probe/lane/.ufo/waves/round-22/tools/count-c2.py", "--root", "/tmp/r22c2probe/lane", "--rev", "034df7ddb2d3dcc3a2efc2ba53126ea10ec80ec6"]
exit: 1
stderr: ""
stdout bytes: 5756
```

For a differential control, the frozen pre-guard counter from `75f04a4` was first confirmed to lack the `row["probe"] != row["verb"]` guard, then run against that exact adversarial revision. It accepted all 14 rows, with no mismatches, exit 0:

```text
argv: ["python3", "-I", "-B", "/tmp/r22c2probe/count-c2-before-guard.py", "--root", "/tmp/r22c2probe/lane", "--rev", "034df7ddb2d3dcc3a2efc2ba53126ea10ec80ec6"]
exit: 0
stderr: ""
```

The exact unabridged stdout for each command, stderr, argv, exit code, revisions, and source hashes are retained as JSON string fields in `C2Probe.json` (including the 5,751- and 5,756-byte current outputs and pre-guard output). No build, lint, or broader test suite was run; these were the requested bounded positive and adversarial probes.

## Residual risk and verification gaps

- The counter checks the receipt envelope's self-declared `meta.command`; it does not authenticate how the receipt was produced or cross-check `.run.json` command provenance. The current source explicitly limits its claim to observed fields/codes and says run metadata needs manual review. That is a declared boundary, not a defect in the assigned row/probe equality check.
- No LSP device is mounted: `read xd://lsp` returned “No such tool” and listed the mounted devices without LSP. Therefore references, definitions, and diagnostics were unavailable. A literal text search located `verify.py`'s counter invocation only; that is not semantic caller proof.
- No runtime rerouting/saturation or resume-continuity behavior is exercised by this static counter attack. No tools were installed or updated.
