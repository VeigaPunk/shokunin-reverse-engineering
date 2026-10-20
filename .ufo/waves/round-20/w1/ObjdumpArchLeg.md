# ObjdumpArchLeg — round 20 C2 (author-side)

**Calibration:** `list-objdump-architectures --schema` declares an empty args object (`.ufo/waves/round-20/evidence/c2/objdump/architectures-schema/stdout.txt:1-4`). The JSON run returned `ev_4d59366d3e60960da306e5b984acca68678ca83f20dd5d2ae40cb5f4851719b7`, `subject:null`, provider `gnu.objdump`, version `null`, complete/untruncated, exit 0 (`.ufo/waves/round-20/evidence/c2/objdump/architectures-json/receipt.json:2,13-20`; `.ufo/waves/round-20/evidence/c2/objdump/architectures-json/stdout.json:1`). Its normalized stdout matches host `objdump -i` byte-for-byte (`.ufo/waves/round-20/evidence/c2/objdump/comparison/comparison-results.txt:1`). Host BFD output says GNU Binutils 2.47 (`.ufo/waves/round-20/evidence/c2/objdump/comparison/objdump-i/stdout.txt:1`); `objdump --help` separately lists the same target names and architecture selectors/aliases (`.ufo/waves/round-20/evidence/c2/objdump/comparison/objdump-help/stdout.txt:98-99`). The pathless listing itself has no subject SHA; the paired artifact-bearing Evidence below provides one.

**Coverage:** `inspect-with-objdump --schema` requires `path` and `operation`; `disassemble` is among seven operations (`.ufo/waves/round-20/evidence/c2/objdump/inspect-schema/stdout.txt:4-21`). An initial `--operation` spelling was rejected (exit 1; `.ufo/waves/round-20/evidence/c2/objdump/inspect-disassemble/receipt.json:2,13-19`, `.ufo/waves/round-20/evidence/c2/objdump/inspect-disassemble/stdout.json:1`); the schema-shaped positional call succeeded on `/usr/bin/jq` (`.ufo/waves/round-20/evidence/c2/objdump/inspect-disassemble-positional/receipt.json:2,13-23`). Evidence `ev_c3fb6b4d370c85cf7c57a4b21a5ec71e914eabfbec2c1affb5b5f4ed13a01760` binds subject SHA-256 `e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806`; provider exit 0, complete and untruncated, artifact hash unchanged (`.ufo/waves/round-20/evidence/c2/objdump/inspect-disassemble-positional/stdout.json:1`, `.ufo/waves/round-20/evidence/c2/objdump/inspect-disassemble-positional/receipt.json:18-23`).

**Depth / limitation:** REA `disassemble` output is not byte-identical to local `objdump -d /usr/bin/jq` (`.ufo/waves/round-20/evidence/c2/objdump/comparison/comparison-results.txt:2`). The retained diff shows local `_init` vs REA `.init` and different branch-symbol references (`.ufo/waves/round-20/evidence/c2/objdump/comparison/disassembly.diff:7-14`). REA provider version remains null, so the cause is unknown; do not claim output equivalence or general support from this one ELF (`.ufo/waves/round-20/evidence/c2/objdump/inspect-disassemble-positional/receipt.json:20-23`). Carrier hash, host executable identity, and version are retained (`.ufo/waves/round-20/evidence/c2/objdump/comparison/objdump-executable.txt:1-3`; `.ufo/waves/round-20/evidence/c2/objdump/comparison/objdump-version/stdout.txt:1`).

**Source:** Official GNU Binutils objdump manual, `https://sourceware.org/binutils/docs/binutils/objdump.html` (`-i`, `-d`); its new SOURCES row ID is left for L1 integration as specified by `.ufo/waves/round-20/claims.json:24-25`. No tools were installed or upgraded.

**Patch:** `.ufo/waves/round-20/w1/patches/ObjdumpArchLeg.patch` (base `14f0260ad319ecc26994381b2415d5a999003375`; adds the knowledge entry and retained run evidence under `.ufo/waves/round-20/evidence/c2/objdump/`). No tests/builds were run.

Cached diff stat (exact output):

```text
git diff --stat: 28 files +4640 -0
 .../c2/objdump/architectures-json/receipt.json     |   21 +
 .../c2/objdump/architectures-json/stderr.txt       |    0
 .../c2/objdump/architectures-json/stdout.json      |    1 +
 .../c2/objdump/architectures-schema/receipt.json   |   20 +
 .../c2/objdump/architectures-schema/stderr.txt     |    0
 .../c2/objdump/architectures-schema/stdout.txt     |    4 +
 .../c2/objdump/comparison/comparison-results.txt   |    2 +
 .../c2/objdump/comparison/disassembly-diff.stderr  |    0
 .../c2/objdump/comparison/disassembly.diff         | 2076 +++++++++++++++++++
 .../comparison/objdump-disassemble/stderr.txt      |    0
 .../comparison/objdump-disassemble/stdout.txt      | 2174 ++++++++++++++++++++
 .../c2/objdump/comparison/objdump-executable.txt   |    3 +
 .../c2/objdump/comparison/objdump-help/stderr.txt  |    0
 .../c2/objdump/comparison/objdump-help/stdout.txt  |  133 ++
 .../c2/objdump/comparison/objdump-i/stderr.txt     |    0
 .../c2/objdump/comparison/objdump-i/stdout.txt     |   94 +
 .../objdump/comparison/objdump-version/stderr.txt  |    0
 .../objdump/comparison/objdump-version/stdout.txt  |    5 +
 .../inspect-disassemble-positional/receipt.json    |   25 +
 .../inspect-disassemble-positional/stderr.txt      |    0
 .../inspect-disassemble-positional/stdout.json     |    1 +
 .../c2/objdump/inspect-disassemble/receipt.json    |   20 +
 .../c2/objdump/inspect-disassemble/stderr.txt      |    0
 .../c2/objdump/inspect-disassemble/stdout.json    |    4 +
 .../c2/objdump/inspect-schema/receipt.json         |   20 +
 .../evidence/c2/objdump/inspect-schema/stderr.txt  |    0
 .../evidence/c2/objdump/inspect-schema/stdout.txt  |   21 +
 .../2026-10-20-r20-objdump-architecture-list.md    |   16 +
 28 files changed, 4640 insertions(+)
```
