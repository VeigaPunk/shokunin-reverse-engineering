source: S045 (GNU Binutils objdump manual, `-i`/`--info` and `-d`), S040 (installed rea-agents@6.5.0 compiled source: `list-objdump-architectures` passes `-i` with no artifact, `subject: null`); retained run and host outputs under `.ufo/waves/round-20/evidence/c2/objdump/`.
verified-at: 2026-10-20 — REA CLI rea-agents@6.5.0; host `objdump` GNU Binutils 2.47; one author-side run.
recheck: Compare `.ufo/waves/round-20/evidence/c2/objdump/architectures-json/stdout.json` `normalized_result.stdout` byte-for-byte with `comparison/objdump-i/stdout.txt`; compare `inspect-disassemble-positional/stdout.json` `raw_result.stdout` with `comparison/objdump-disassemble/stdout.txt`. Full invocations, environment, timestamps, exits and file digests are in the adjacent `receipt.json` files.

# Round 20: objdump architecture listing and disassembly boundary

## Observations

- `list-objdump-architectures --schema` has an empty argument-property set. Its `--format json` run returned `ev_4d59366d3e60960da306e5b984acca68678ca83f20dd5d2ae40cb5f4851719b7`; `subject` is null, provider is `gnu.objdump`, and provider version is null. The Evidence result is complete, exit 0 and untruncated. Its normalized stdout is byte-identical to this host's `objdump -i` output. That output identifies its BFD header as GNU Binutils 2.47.
- Host `objdump --help` reports the BFD target names in the `-i` output and a separate disassembler-architecture list: `i386`, `i386:x86-64`, `i386:x64-32`, `i8086`, `i386:intel`, `i386:x86-64:intel`, `i386:x64-32:intel`, `bpf`, `xbpf`. Treat these as distinct views: the `-i` matrix associates BFD formats with backend architecture names, while help also exposes disassembler selectors.
- `inspect-with-objdump --schema` requires positional `path` and `operation`; `disassemble` is one of seven operations, and `followDebugLinks` defaults false. An initial `--operation disassemble` attempt was refused as an unknown flag (exit 1); passing `disassemble` positionally succeeded. On `/usr/bin/jq` (`e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806`), `disassemble` returned `ev_c3fb6b4d370c85cf7c57a4b21a5ec71e914eabfbec2c1affb5b5f4ed13a01760`, exit 0, complete and untruncated; the post-run artifact hash matched and `artifact_changed` is false.
- The returned disassembly is not byte-identical to local `objdump -d /usr/bin/jq`. The retained diff shows local labels such as `_init` and `main`, while the REA result labels `.init` and `.text` and resolves many references as `stderr@GLIBC_2.2.5` (including diff lines 7-14). The REA provider version is null, so this run does not identify why the output differs.

## Limits

This establishes one host's BFD inventory and one successful `disassemble` operation on one ELF. It does not establish REA's objdump executable version, general architecture coverage, or disassembly equivalence. `format` and `architecture` remain unknown/null in the inspect Evidence. This covers an operation beyond the previously held `file_headers` example; it does not replace that record.
