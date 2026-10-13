<!-- corpus entry — kaidoku-shokunin round 3 (2026-10-13). Staging evidence: fleet .ufo/waves/kaidoku-r3/15-verb-coverage.md. -->

# 15 — Verb-family coverage on libjq.so.1.0.4 (round-3: xrefs / trace / read-bytes / function / instructions / list-*)

Target: `/usr/lib/libjq.so.1.0.4` (jq-1.8.2, 350,384 B, sha256 `7e8bccc6…`,
ELF64 DYN stripped, `.dynsym` exports 181 `T` syms). REA analysis state from r2
(`.ufo/waves/kaidoku-r2/17-libjq.md`): 29 segments / 924 procedures / 1212
strings, provider ghidra 12.1.4, image rebase **REA addr = file vaddr +
0x100000** (`jq_next` nm `0x17070` → REA `0x117070`). Every REA invocation
re-imports via ephemeral Ghidra (~30–90 s per call here).

## Candidate: `xrefs` — exercised; inbound-only list of 26 references to `jq_next`, resolvable by address AND symbol name

- claim: `xrefs <path> <addr-or-name>` returns `normalized_result` = flat list of
  26 addresses referencing `jq_next`. `xrefs … 0x117070` and `xrefs … jq_next`
  return **byte-identical** lists (symbol-name resolution works). The 26
  decompose into three mechanical classes: **23 code refs** — all `call
  *disp(%rip)` indirect calls through GOT slot `0x55d98` (vaddr; file off
  `0x54d98`, RW LOAD maps 0x52ef0→0x53ef0), whose `readelf -rW` entry is
  `R_X86_64_GLOB_DAT 0x17070 jq_next + 0` and whose file bytes are zeros
  (reloc-populated); **2 unwind refs** — `0x14b35c` inside `.eh_frame_hdr`
  (0x4a8c8–0x4bc53) binary-search table (`a8 c7 fc ff` = pcrel|sdata4 →
  readelf decodes `offset: 0x17070`, fde ptr 0x3da4 → FDE `2a14`), and
  `0x14e674` inside `.eh_frame` (0x4bc58–0x5260f) = jq_next's own FDE
  `pc_begin` field (`fc 89 fc ff` sdata4 at field base → `0x17070`; readelf
  -wf: `FDE 00002a14 pc=0x17070..0x18cc5`); **1 GOT data ref** —
  `0x155d98` = the slot itself (Ghidra emits slot→target edge from the
  relocation). Call sites live in `test_pthread_run`,
  `test_jq_start_resets_state.constprop.0`, `run_jq_tests`, and
  `jq_testsuite`'s non-contiguous body — the testsuite, not the VM core.
  **FROM direction is not expressible**: the verb has no direction flag;
  outbound edges come from `function` (`outgoing_references` = 903,
  `callees` = 45).
- source: `/tmp/r3-xrefs-addr.json` (EXIT=0, 3,228 B, evidence
  `ev_ce745d78…`); `objdump -d` at sites 0x21b04/0x21b21/0x21c94/0x22b6d/0x2303d
  (all `call *…(%rip) # 55d98`); `readelf -rW` row 220; `od` at file
  0x54d98; `readelf -SW` `.eh_frame_hdr`/`.eh_frame`/`.got` ranges;
  `readelf -wf` FDE decode tail.
- verify: `npx -y rea-agents@6.4.0 xrefs /usr/lib/libjq.so.1.0.4 0x117070
  --format json` → 26-elem list; `objdump -d --start-address=0x21b04
  --stop-address=0x21b14 /usr/lib/libjq.so.1.0.4` → `call *0x3428e(%rip) #
  55d98 <jq_next@@Base+0x3ed28>`; `readelf -rW | grep jq_next` →
  `55d98 GLOB_DAT 17070 jq_next`.
- verified-at: 2026-10-13 round-3 lane (shell ccdc0a EXIT=0; name-form shell
  e80824 identical output).
- suggested: admit — xrefs answers "who points at X" precisely and includes
  non-code reference classes (GOT slot, DWARF unwind) a grep would miss;
  document that it is **inbound-only** and that exported-symbol call sites on
  ELF are GOT-indirect edges, not `call <jq_next>` (objdump `call 17070`
  count = 0).

## Candidate: `trace` — exercised; a literal-feature reference tracer (rea-workflow provider), not a call-path engine

- claim: `trace <path> --query '<literal>'` runs provider
  `rea-workflow` ("REA composed investigation workflow", wraps the ghidra
  profile) with `operation: trace_feature`, `search_mode: literal`. Query
  `jq_init` returned 2 matches (`{"type":"string", address 0x103239}`,
  `{"type":"procedure", address 0x11de50}`) and **9 references** each typed
  `{target_address, source_address, containing_procedure{found, procedure
  {name, body ranges}}}`: 6 code refs in `FUN_00121a50`, `FUN_00121be0`,
  `FUN_001227b0`, `jq_testsuite` (3 sites), plus the same GOT
  (`0x155aa0`)/unwind (`0x14b58c`, `0x14f424`) non-code edges the xrefs verb
  emits. The requested "call path entry → jq_init" shape does not exist —
  there is no from/to form; trace = search + per-hit reference edges with
  typed containers. `jq_init` is library API: its inbound code refs are
  testsuite wrappers, matching upstream jq.
- source: `/tmp/r3-trace.json` (EXIT=0, 6,239 B, evidence `ev_0e340220…`).
- verify: `npx -y rea-agents@6.4.0 trace /usr/lib/libjq.so.1.0.4 --query
  jq_init --format json` → `matches:2`, `references:9`; `nm -D | grep
  ' jq_init'` → `0x1de50` (REA `0x11de50`, +0x100000 rule holds).
- verified-at: this round (shell 190239 EXIT=0).
- suggested: admit — exercised and useful (returns xref+container typing in
  one shot), but record the semantic gap: "trace" ≠ path/call-chain tracing;
  call-path questions need `function` caller/callee sets composed by hand.

## Candidate: `read-bytes` + `address-to-file-offset` — exercised; provider bytes verify byte-exact against objdump/od ground truth

- claim: positional `read-bytes /usr/lib/libjq.so.1.0.4 0x117070 --length 64`
  returns `bytes_hex
  f30f1efa554889e54881ecf0000000488b770848895dd864488b1c252800000048895dc84889fb488b3fff1578eb03004889dfe898fcffff4885c00f8471f9fe`
  (`returned_bytes=64, complete:true`) — **byte-for-byte identical** to
  `objdump -d` raw columns at vaddr 0x17070 (ENDBR64…through the first 4 of
  the 6 `je` bytes; 64 B boundary mid-instruction, no alignment complaint).
  `address-to-file-offset … 0x117070` returns `file_offset: 94320` =
  `0x17070`, matching the R E LOAD (Offset 0x6000 == VirtAddr 0x6000) and
  confirming the +0x100000 REA rebase; the verb uses "Ghidra source-byte
  mappings, not virtual-address arithmetic". Flag form is rejected:
  `--address 0x117070` → typed `{"code":"UNKNOWN","message":"Unknown flag:
  --address"}` on both verbs (address is positional, `required[2]`).
- source: `/tmp/r3-readbytes.json` (evidence `ev_7d523c6c…`),
  `/tmp/r3-a2fo.json` (`ev_657d1d54…`); ground truth `objdump -d
  --start-address=0x17070` bytes; `readelf -lW` LOAD table.
- verify: `npx -y rea-agents@6.4.0 read-bytes /usr/lib/libjq.so.1.0.4
  0x117070 --length 64 --format json | grep bytes_hex` → hex above;
  `od -A x -t x1 -j 0x17070 -N 64 /usr/lib/libjq.so.1.0.4` → same bytes.
- verified-at: this round (shells 13643f, 556744 EXIT=0; flag-form refusals
  d1a461, 42c053 EXIT=1 typed error).
- suggested: admit — strongest verification of the round: REA memory image =
  shipped bytes at this address; positional-arg pitfall worth logging in
  PROVINCE/runbook (schema `required[2]` = positional, flags absent).

## Candidate: `function` — exercised; the dossier verb that subsumes decompile+instructions+xrefs in one 6.2 MB envelope

- claim: `function /usr/lib/libjq.so.1.0.4 --procedure jq_next` returns a
  dossier whose `normalized_result.value` carries: `procedure` (name,
  `external:false`, provenance `ghidra-function-manager`, non-contiguous body
  ranges incl. cold split at `0x16a9a`), `pseudocode` (the same 839-line VM
  loop r2 got via `decompile`), `assembly[1621]`, `callers[5]` =
  `FUN_00121a50`, `FUN_00121be0`, `FUN_001227b0`, `FUN_00123330`,
  `jq_testsuite` (the 23 GOT call sites collapse to 5 procedures),
  `callees[45]` (named `jv_get_kind`, `jv_copy`, `jv_dump`, `jv_object_iter*`,
  `jv_nomem_handler`, …), `incoming_references[26]` (**identical list to the
  standalone `xrefs` verb**), `outgoing_references[903]` (incl. `stack:`
  pseudo-targets), `referenced_strings[14]` (`\t<halted>`,
  `\t<backtracking>`, `Range bounds must be numeric`, `V%d = ` ×4…),
  `referenced_names[676]`, `basic_blocks[179]`, `native_api` (signature
  `undefined1[16] jq_next(undefined8 *param_1)`, confidence `low`, storage
  `RDX:8,RAX:8`, source `default`), `native_value_flow`. Limitations are
  typed: indirect flows without targets are not edges; thunk/external
  classification doesn't resolve targetless calls.
- source: `/tmp/r3-function.json` (EXIT=0, 6,209,733 B, evidence
  `ev_56f289ad…`); python field census in Run log row 7.
- verify: `npx -y rea-agents@6.4.0 function /usr/lib/libjq.so.1.0.4
  --procedure jq_next --format json | python3 -c "import sys,json;
  v=json.load(sys.stdin)['normalized_result']['value'];
  print(len(v['assembly']),len(v['callers']),len(v['callees']),
  len(v['incoming_references']),len(v['outgoing_references']))"` →
  `1621 5 45 26 903`.
- verified-at: this round (shell 20ea37 EXIT=0).
- suggested: admit — this is the highest-information-per-invocation verb
  seen so far; one call replaces separate decompile/instructions/xrefs/
  callers/strings passes. Cost: 6.2 MB envelope — pair with
  `--filter-output` for agent contexts.

## Candidate: `instructions` — exercised; raw listing, 1621 rows for `jq_next`, decompiler-free fast path

- claim: `instructions <path> --procedure jq_next` returns
  `{procedure{…}, instructions[1621], limitations[2]}` of flat
  `"0xADDR: MNEMONIC operands"` strings: first `"0x117070: ENDBR64"`, last
  `"0x118cc0: JMP 0x00106a9a"` (tail-jump into the cold block —
  `jq_next.cold`, file vaddr 0x6a9a; consistent with objdump `je 6a22` in
  the prologue). Limitations state text is Ghidra-representation and "the
  fast path does not invoke the decompiler or scan whole-program names and
  strings" — a cheaper verb than `function`/`decompile`.
- source: `/tmp/r3-instr.json` (EXIT=0, 111,226 B, evidence `ev_e41fbebd…`).
- verify: `npx -y rea-agents@6.4.0 instructions /usr/lib/libjq.so.1.0.4
  --procedure jq_next --format json | python3 -c "import sys,json;
  i=json.load(sys.stdin)['normalized_result']['instructions'];
  print(len(i),i[0],i[-1])"` → `1621 0x117070: ENDBR64 0x118cc0: JMP
  0x00106a9a`.
- verified-at: this round (shell a9d3c3 EXIT=0).
- suggested: admit — linear listing only (no flow, no operands decoded);
  complements `function.assembly` which carries the same 1621 count inside
  the richer dossier.

## Candidate: `list-*` family — refused on this target: `list-architectures` is macOS-only; no `list-segments`/`list-functions` verb exists

- claim: `list-architectures /usr/lib/libjq.so.1.0.4` fails with the typed
  envelope `{"error":"Analysis failed","code":"capability_unavailable",
  "category":"unsupported_provider","message":"This analysis is unavailable
  for the current target…","retryable":false,"details":{"provider_id":
  "ghidra","operation":"list_architectures","reason":"Native macOS
  utilities require macOS."}}` — a **refused** family for ELF/Linux (the
  verb wraps Hopper-era macOS tooling despite the ghidra provider id).
  Full `rea --help` census: the only other `list-*` verbs are
  `list-adb-{devices,directory,features,packages,processes,services}`,
  `list-browser-targets`, `list-electron-targets`,
  `list-javascript-runtime-targets`, `list-jeb-units` — all
  platform-scoped, none applicable to a local ELF path (**not-applicable**).
  There is no `list-segments` / `list-procedures` / `list-symbols` verb;
  segment/procedure/string inventory is served by `analyze` and
  `inspect-binary-layout` (r1/r2 already exercised).
- source: `/tmp/r3-archs.json` (EXIT=1, typed refusal); `rea --help` verb
  list (rows 83–93 of help output).
- verify: `npx -y rea-agents@6.4.0 list-architectures
  /usr/lib/libjq.so.1.0.4 --format json` → `capability_unavailable` reason
  `Native macOS utilities require macOS.`; `npx -y rea-agents@6.4.0 --help |
  grep '^  list-'` → 10 verbs, none ELF-generic.
- verified-at: this round (shell 259ed2 EXIT=1).
- suggested: admit — record `list-architectures` as refused-on-Linux-ELF
  (typed, non-retryable); inventory needs are met by `analyze` segment_count
  + `inspect-binary-layout`, not a missing capability.

## Run log

| # | command | result |
|---|---------|--------|
| 1 | `rea {xrefs,trace,read-bytes,function,instructions,list-architectures,address-to-file-offset} --schema` | arg shapes: address is **positional** on read-bytes/a2fo/xrefs; `function`/`instructions` take `--procedure`; `trace` takes `--query` (literal); `list-architectures` path-only, Mach-O-scoped |
| 2 | `rea read-bytes … --address 0x117070` / `address-to-file-offset … --address` | EXIT=1 typed `{"code":"UNKNOWN","message":"Unknown flag: --address"}` — flag form refused |
| 3 | `rea xrefs /usr/lib/libjq.so.1.0.4 0x117070` | EXIT=0 — 26 inbound refs; `xrefs … jq_next` (name form) → identical list |
| 4 | `objdump -d` @0x21b04/…/0x2303d; `readelf -rW`; `od` @0x54d98; `readelf -SW`/`-wf` | 23× `call *(%rip)`→GOT 0x55d98 (`GLOB_DAT jq_next`), 2× unwind refs (.eh_frame_hdr 0x4b35c + FDE 2a14 pc_begin 0x4e674 → pc 0x17070), 1× GOT slot ref; `objdump` direct `call 17070` count = 0 (GOT-indirect edges only) |
| 5 | `rea read-bytes … 0x117070 --length 64`; `rea address-to-file-offset … 0x117070` | EXIT=0 — 64 B hex == objdump/od bytes at file 0x17070; `file_offset: 94320` |
| 6 | `rea trace … --query jq_init` | EXIT=0 — provider `rea-workflow`, 2 matches + 9 typed references (6 code in FUN_*/jq_testsuite, 2 unwind, 1 GOT); no from/to call-path form |
| 7 | `rea function … --procedure jq_next` | EXIT=0 — 6.2 MB dossier: pseudocode 839 lines, assembly×1621, callers×5, callees×45, in_refs×26 (== xrefs verb), out_refs×903, strings×14, BBs×179, native_api sig |
| 8 | `rea instructions … --procedure jq_next` | EXIT=0 — 1621 rows `0x117070: ENDBR64` … `0x118cc0: JMP 0x00106a9a`; fast path, no decompiler |
| 9 | `rea list-architectures /usr/lib/libjq.so.1.0.4` | EXIT=1 typed refusal `capability_unavailable` — "Native macOS utilities require macOS.", retryable:false |

Scratch (left in /tmp for reproducibility, not repo): `/tmp/r3-xrefs-addr.json`,
`/tmp/r3-{readbytes,a2fo,function,instr,trace,archs}.json` + `.err` twins.

## Summary

Verb-family coverage on `/usr/lib/libjq.so.1.0.4` after this pass:

| family | status | note |
|--------|--------|------|
| `xrefs` | **exercised** | inbound-only, addr-or-symbol; 26 refs to jq_next (23 GOT-indirect calls + 2 DWARF unwind + 1 GOT slot); FROM-direction = use `function.outgoing_references` |
| `trace` | **exercised** | literal-feature tracer (`rea-workflow`), matches + typed containing_procedure refs; not a call-path engine |
| `read-bytes` | **exercised** | 64 B at REA 0x117070 verified byte-exact vs objdump/od; positional addr (`--address` flag refused) |
| `address-to-file-offset` | **exercised** | 0x117070 → 94320 (0x17070); source-byte mapping, confirms +0x100000 rebase |
| `function` | **exercised** | the dossier verb: decompile+asm+callers/callees+xrefs both ways+strings+BBs+signature in one 6.2 MB envelope |
| `instructions` | **exercised** | flat 1621-row listing, decompiler-free fast path |
| `list-architectures` | **refused** | typed `capability_unavailable` — macOS-only verb on ELF, non-retryable |
| `list-segments`/`list-procedures`/`list-symbols` | **not-applicable** | verbs do not exist; inventory via `analyze`/`inspect-binary-layout` (r1–r2) |
| other `list-*` (adb×6, browser, electron, V8, jeb) | **not-applicable** | platform-scoped, no ELF-file meaning |
| `xrefs FROM jq_next` | **not-applicable** | no direction flag; outbound edges live in `function` (903 out-refs, 45 callees) |

Combined with r1–r2 (analyze, search, decompile, compare, inspect*), the
native ELF verb surface now exercised end-to-end: analyze / search /
decompile / compare / inspect / **xrefs / trace / read-bytes /
address-to-file-offset / function / instructions**. Notable pitfall for
runbook: several verbs take the address as a **positional** arg — `--address`
is a typed refusal, and exported-symbol calls are GOT-indirect so `xrefs`
is the tool that reveals callers (objdump direct-call grep finds none).
