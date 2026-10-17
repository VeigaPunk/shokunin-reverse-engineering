## CLAIM
Replay only assigned legs L6–L8 on the live REA 6.5.0 MCP surface. Each preregistered prediction was RESULT.

## METHOD
From `/tmp`, launched a fresh `npx -y rea-agents@6.5.0 --mcp` process per leg, sent MCP initialize and tool-call frames, used a 240-second response deadline, closed stdin, and confirmed server exit code 0. Receipts contain complete stdout/stderr, exit code, and verified stdout SHA-256. L6 was repeated once to repair receipt capture; its final receipt records the second identical-output run. Carriers: `/tmp/luna-round-6-leg-6.sqlite` (generated valid SQLite database), `/bin/true` (ELF), `/usr/bin/jq` (ELF).

## FINDINGS
- L6 `inspect_sqlite_database`: typed schema and sampled row result; evidence `ev_e0eb446a8de2f3749a0be949b881ff66a62dba26ed8c5cfe0159501ab435b3c8`. Receipt `.ufo/waves/luna-round-6/receipts/leg-6.md`; stdout SHA-256 `9a1445b4caa25e0b8e3ab93fb5c90a31ed5a5a6682eecae5115bd89627c70160`.
- L7 `open_binary` + `search_bytes` for `7f 45 4c 46`: hit at address `0x100000`, `file_offset: 0`; evidence `ev_4b0badc6b166fb6e6196ec561521d48873af50c2f41329deca72ccc685eab903`. Receipt `leg-7.md`; stdout SHA-256 `3492d27d66e086d683935f396ea05fce4cbddc660874052a955c9133866629a8`.
- L8 `inspect_with_objdump` (`file_headers`) returned `elf64-x86-64`, architecture `i386:x86-64`, exit 0, `artifact_changed:false`; evidence `ev_aa75cc2e36b149a82b41e763b92697efc1e2c432571d14c003e3a7bff0219c2f`. Receipt `leg-8.md`; stdout SHA-256 `e0b2d5058e2a28ed41857cc3672d9b7e3354072bc474a8eb349c7065333c232b`.

## THREATS
L6 used a locally generated valid database, not an application-shipped snapshot. L7 resolved to `/usr/bin/true`. This seat did not audit system-wide host mutation, operator-config drift, command A, or map-token invariance, and makes no claim about the remaining seven legs or full-battery threshold.

## VERDICT
CLEAN — all three assigned RESULT predictions matched; no full-battery verdict inferred.
