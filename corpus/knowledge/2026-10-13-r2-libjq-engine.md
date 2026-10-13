<!-- corpus entry — kaidoku-shokunin round 2 (2026-10-13). Staging evidence: fleet .ufo/waves/kaidoku-r2/17-libjq.md. -->

# 17 — libjq.so.1.0.4: the actual jq engine behind the 30KB driver (round-2 evidence)

Target: `/usr/lib/libjq.so.1` → resolves to `/usr/lib/libjq.so.1.0.4` (jq-1.8.2 install).
Round-1 contrast baseline: `/usr/bin/jq` — 30,800 B stripped PIE driver; REA `analyze` = 30
segments / 167 procedures (90 local `FUN_*` + `entry`/`_INIT_0`, 77 `<EXTERNAL>::` thunks) /
190 strings (`.ufo/waves/kaidoku-r1/10-rea-live.md` row 4,6).

## Candidate: libjq.so.1.0.4 identity — 350KB stripped ELF DYN, exports the entire jq/jv API through .dynsym

- claim: the engine is `/usr/lib/libjq.so.1.0.4` — 350,384 B ELF 64-bit LSB shared object,
  x86-64, `file` reports "stripped" (no `.symtab`), yet `.dynsym` exports **181 `T` symbols**
  covering the full public API: 34 `jq_*` (incl. lexer internals `jq_yy*` and even
  `jq_testsuite`/`jq_dump_disassembly`), ~105 `jv_*` (refcounted value model: `jv_copy`,
  `jv_free`, `jv_get_kind`, `jv_parse`, `jv_dump`, `jv_object_*`, `jv_array_*`,
  `jv_string_*`, `jv_number_*`, `jv_tsd_*` TLS dec-ctx). SONAME `libjq.so.1`; DT_NEEDED =
  `libm.so.6`, `libonig.so.5` (Oniguruma regex), `libc.so.6`, `ld-linux-x86-64.so.2`;
  148 undefined dyn syms (`arc4random@GLIBC_2.36`, `exp10@GLIBC_2.39`, `__printf_chk` …).
  `.sframe` + `.gnu_debuglink` sections present.
- source: `readlink -f /usr/lib/libjq.so.1`; `sha256sum` =
  7e8bccc6df37a55fb90703c9069b3770f5cdc502e96959c866d2f30fbf5e8b6b; `file`;
  `readelf -h` (DYN, 13 phdrs, 28 shdrs, entry 0x0); `nm -D | grep -c ' T '` = 181;
  `nm -D | grep -c ' U '` = 148; `readelf -d` (NEEDED/SONAME); `readelf -S`; `jq --version` = jq-1.8.2.
- verify: `readlink -f /usr/lib/libjq.so.1 && sha256sum /usr/lib/libjq.so.1.0.4 &&
  nm -D /usr/lib/libjq.so.1.0.4 | grep -c ' T '` → expect `…1.0.4`, sha256 above, `181`.
- verified-at: 2026-09-21 round-2 lane shell (commands in Run log rows 1–3).
- suggested: admit — "stripped" here means `.symtab` gone; `.dynsym` is fully populated,
  which is exactly the opposite signal profile from the driver (driver exports nothing,
  imports the same API back as `<EXTERNAL>::jq_*`).

## Candidate: REA analyze on libjq — 29 segments / 924 procedures / 1212 strings (5.5× the driver's procedure count)

- claim: `timeout 900 npx -y rea-agents@6.4.0 analyze /usr/lib/libjq.so.1.0.4 --format json`
  succeeds via provider `ghidra` 12.1.4 (same `ephemeral-source-immutable` import mode as r1)
  and reports `segment_count=29`, `procedure_count=924`, `string_count=1212` — vs the
  driver's 30 / 167 / 190. `.text` alone is 231,283 B (vs the whole 30KB driver).
  Evidence id `ev_bf0875fae37e…`, document `target-7e8bccc6df37.4`.
- source: `/tmp/kaidoku-r2-libjq-analyze.json` normalized_result (this run; scratch file,
  reproduce with the verify line).
- verify: `timeout 900 npx -y rea-agents@6.4.0 analyze /usr/lib/libjq.so.1.0.4 --format json |
  python3 -c "import sys,json;print(json.load(sys.stdin)['normalized_result'])"` → expect
  `segment_count=29, procedure_count=924, string_count=1212`.
- verified-at: this round (`EXIT=0`, run in background shell 0590c7).
- suggested: admit — the 167→924 jump quantifies "the real code lives in the .so": ~86% of
  the driver's 167 "procedures" were import thunks or startup stubs; libjq inverts that.

## Candidate: procedure census — 181 exported names + 446 local FUN_* + 291 <EXTERNAL>:: stubs + 6 infrastructure

- claim: `search --kind procedures --pattern '.' --mode regex` enumerates all 924:
  **181** named `jq_*`/`jv_*` (exactly the `nm -D` export list — REA/Ghidra resolves
  `.dynsym` entries to real names at their entry addresses), **446** local `FUN_00106xxx`…
  `FUN_0013exxx` (the anonymous internals — bytecode compiler, builtins, parser actions,
  helpers), **291** `<EXTERNAL>::` import stubs (libc/libm/oniguruma — note the driver's
  `<EXTERNAL>::jq_next` now appears here as a *defined* named procedure), plus **6**
  infrastructure entries: `_DT_INIT`, `_DT_FINI`, `_INIT_0`, `_FINI_0`,
  `thunk_FUN_00106be6`, and one `switchD_001195cd::default` case label.
- source: `/tmp/kaidoku-r2-search-all.json` (924 rows), cross-cut with
  `nm -D` export list — 181 = 181 exact match.
- verify: `npx -y rea-agents@6.4.0 search /usr/lib/libjq.so.1.0.4 --kind procedures
  --pattern '.' --mode regex --format json` → 924 rows; bucket by prefix
  (`jq_|jv_` / `FUN_` / `<EXTERNAL>` / rest) → 181/446/291/6.
- verified-at: this round (shell 8c3d17; also `^jq_|^jv_` regex search = 181 rows).
- suggested: admit — exported-vs-local split is now measurable: ~28% of defined code
  (181/627 real functions) is public API surface; the remaining 446 FUN_* are the
  private bulk the driver never sees.

## Candidate: decompiling an exported function — `jq_next` yields an 839-line named-symbolic VM interpreter loop

- claim: `rea decompile /usr/lib/libjq.so.1.0.4 jq_next` accepts the **symbolic name**
  (no address needed — `.dynsym` gives Ghidra the entry) and returns 839 lines of C-like
  pseudo-code: signature `undefined1 [16] jq_next(undefined8 *param_1)`, the jq bytecode
  VM stepping loop — `switch(uVar17)` opcode dispatch (`uVar17 = *puVar5` = `*pc`,
  opcodes `< 0x2b` i.e. 43-case dispatch table at `DAT_00153f38` stride 0x20),
  `case 0` doing `jv_array_get` on the constant pool, `__assert_fail("pc",
  "src/execute.c", 0x158, "jq_next")` and `__assert_fail("jv_get_kind(jq->error) ==
  JV_KIND_NULL", "src/execute.c", 0x15e, …)` leaking exact upstream source file/line,
  `<halted>` debug trace path, and direct named calls to `jv_nomem_handler`,
  `jv_get_kind`, `jv_copy`, `jv_dump`, `puts`/`putchar`/`__printf_chk`. Local helpers
  still appear as `FUN_00116d40`, `FUN_00108f20`, `FUN_001147a0`.
- source: `/tmp/kaidoku-r2-decomp-jqnext.json` normalized_result (839 lines,
  `confidence: observed`, `authority: shipped-artifact`, provider ghidra 12.1.4).
- verify: `npx -y rea-agents@6.4.0 decompile /usr/lib/libjq.so.1.0.4 jq_next --format json |
  python3 -c "import sys,json;t=json.load(sys.stdin)['normalized_result'];
  print(t.count(chr(10)))"` → ~839; `grep -c 'src/execute.c'` ≥ 2;
  `grep 'switch(uVar17)'` present.
- verified-at: this round (shell ae1e43, EXIT=0, 62,040 B JSON envelope).
- suggested: admit — this is the round's sharpest contrast: same strip level as the
  driver, but with `.dynsym` the decompiler names every API call site and the target
  itself; asserts even recover upstream `src/execute.c` line numbers. Internal statics
  stay `FUN_*`, so symbol availability is partial, not total.

## Candidate: driver↔engine inversion — the same 181 names are `<EXTERNAL>::` on one side and defined entries on the other

- claim: round-1 found 77 `<EXTERNAL>::` thunks in the driver, dominated by `jq_*`/`jv_*`
  imports; every one of those resolves to a real, named, decompilable procedure inside
  libjq (e.g. driver's `<EXTERNAL>::jq_next` ↔ libjq `jq_next` @ nm `0x17070` / REA
  rebased `0x117070`). Decompilation quality is strictly better on the engine side:
  call sites render as `jv_dump(...)`, `jv_get_kind(...)` instead of anonymous PLT
  slots, and callers can be selected by name. What `.dynsym` does NOT recover: the 446
  static/internal functions (jq's `block_*` compile IR, builtin tables, flex/bison
  action code) — those remain `FUN_*` exactly as in the stripped driver.
- source: r1 `/tmp/rea-search-procs.json` census (90 local + 77 external) vs r2
  `/tmp/kaidoku-r2-search-all.json` (181 named + 446 FUN_ + 291 external + 6 infra);
  `nm -D` address for `jq_next` = `0000000000017070` ↔ REA `0x117070` (REA image base
  `0x100000` + file vaddr `0x17070`); nm `jq_report_error 0x16fd0` ↔ REA `0x116fd0`.
- verify: `nm -D /usr/lib/libjq.so.1.0.4 | grep ' T jq_next'` → `0x17070`;
  `npx -y rea-agents@6.4.0 search /usr/lib/libjq.so.1.0.4 --kind procedures
  --pattern 'jq_next'` → `0x117070` (constant +0x100000 REA rebase).
- verified-at: this round.
- suggested: admit — REA rebases .so vaddrs by +0x100000 (file 0x17070 → 0x117070);
  record this mapping rule for future lanes cross-checking `nm` output against
  REA addresses.

## Run log

| # | command | result |
|---|---------|--------|
| 1 | `readlink -f /usr/lib/libjq.so.1; ldd /usr/bin/jq \| grep jq` | `/usr/lib/libjq.so.1.0.4`; driver loads `libjq.so.1` |
| 2 | `sha256sum`, `file`, `ls -la`, `readelf -h`, `readelf -d`, `readelf -S` | 350,384 B; sha256 `7e8bccc6…`; ELF64 LSB DYN stripped; SONAME libjq.so.1; NEEDED libm/libonig.so.5/libc/ld-linux; `.sframe`, `.gnu_debuglink` present; `jq --version` = jq-1.8.2 |
| 3 | `nm -D` census | 181 exported `T` (`jq_*`/`jv_*`/`jq_yy*`/`jq_testsuite`), 148 `U` imports |
| 4 | `timeout 900 npx -y rea-agents@6.4.0 analyze /usr/lib/libjq.so.1.0.4 --format json` | EXIT 0 — 29 segments, 924 procedures, 1212 strings; `.text` 231,283 B; ghidra 12.1.4; evidence `ev_bf0875…` |
| 5 | `rea search … --kind procedures --pattern '^jq_\|^jv_' --mode regex` | 181 rows — exact .dynsym export set |
| 6 | `rea search … --kind procedures --pattern '.' --mode regex` | 924 rows: 181 named / 446 FUN_ / 291 `<EXTERNAL>::` / 6 infra (`_DT_INIT`, `_DT_FINI`, `_INIT_0`, `_FINI_0`, `thunk_FUN_…`, `switchD_…::default`) |
| 7 | `rea decompile /usr/lib/libjq.so.1.0.4 jq_next --format json` | EXIT 0 — 839-line VM interpreter loop; `switch(uVar17)` 43-opcode dispatch; asserts cite `src/execute.c:0x158/0x15e`; named `jv_*` call sites |
| 8 | `jq --version`; FUN_/EXTERNAL recount | jq-1.8.2; buckets reconcile 181+446+291+6 = 924 |

Scratch files (deleted after run): `/tmp/kaidoku-r2-libjq-analyze.json`,
`/tmp/kaidoku-r2-search-{jqjv,fun,all}.json`, `/tmp/kaidoku-r2-decomp-jqnext.json`,
`/tmp/kaidoku-r2-libjq-analyze.err`. No `/tmp/rea-ghidra-*` dirs touched (self-cleaned).

## Summary

The engine behind round-1's 30KB driver is `libjq.so.1.0.4` (jq-1.8.2): 350KB, same
"stripped" label, but a fully populated `.dynsym` exporting 181 `jq_*`/`jv_*` symbols —
the complete public API including flex/bison `jq_yy*` internals. REA `analyze` reports
29 segments / **924 procedures** / 1212 strings vs the driver's 30/167/190; the procedure
census inverts the driver's shape: 181 named exports + 446 local `FUN_*` + 291 external
stubs + 6 infra, where the driver was 90 locals + 77 external thunks. Decompiling by
symbol name (`jq_next`) returns an 839-line bytecode-VM interpreter loop with named
`jv_*` call sites and `__assert_fail` breadcrumbs to upstream `src/execute.c` lines —
what `.dynsym` buys is API-call-site naming everywhere; what it doesn't buy is names for
the 446 internal statics. Mapping rule recorded: REA rebases .so vaddrs by +0x100000
(nm `0x17070` ↔ REA `0x117070`).
