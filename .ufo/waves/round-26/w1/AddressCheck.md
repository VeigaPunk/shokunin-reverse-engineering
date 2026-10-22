# R26-C1 AddressCheck — is 0x103fa0 a function on /usr/bin/jq

Seat: KaidokuR26.AddressCheck (leaf). Host tools only (readelf, objdump, nm, xxd, python byte scan), no REA run.
Carrier pin: /usr/bin/jq, 30,800 B, sha256 e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806; the
alternate copy /fast/scratch/hyaku/kaidoku-r26/carrier/alt/jq has the same size and sha256, mode 755, read only.

**Verdict: holds.** File VA 0x3fa0 is a genuine function entry, proven by the carrier's own .eh_frame with no symbols
and no network; it is the static helper `process` (main.c line 175) per build-id-matched debug info; two direct calls
from `main` reach it, so `xrefs` at 0x103fa0 is not trivially empty. 0x103fa0 is the right form for all five verbs.

## 1. Address space: 0x3fa0 lies in .text and maps 1:1 to file offset 0x3fa0

`readelf -h`, `readelf -SW`, `readelf -lW /usr/bin/jq` (2026-10-22T12:12Z, exit 0):

    Type:                DYN (Position-Independent Executable file)
    Entry point address: 0x3cf0
    [11] .text   PROGBITS  0000000000002020 002020 002529 AX
    LOAD 0x002000 0x0000000000002000 0x0000000000002000 0x002559 R E

So 0x3fa0 is inside .text [0x2020, 0x4549) and p_offset == p_vaddr for that segment, giving file offset 0x3fa0.

## 2. Function start, from the shipped bytes alone

`readelf --debug-dump=frames /usr/bin/jq` (2026-10-22T12:13Z, exit 0):

    000000a4 000000000000002c 000000a8 FDE cie=00000000 pc=0000000000003fa0..00000000000044a9
    0xffffffffffffdc20 (offset: 0x3fa0) -> 0xec fde=[    a4]

The preceding FDE ends at 0x3f91, and 0x3f91..0x3f9f is alignment padding (a 4 byte nopl then a 12 byte nopw that ends
exactly at 0x3fa0). `env -u DEBUGINFOD_URLS objdump -d --start-address=0x3fa0 --stop-address=0x3fd0 /usr/bin/jq`
(2026-10-22T12:13Z, exit 0):

    0000000000003fa0 <.text+0x1f80>:
        3fa0: 55                 push   %rbp   ; 3fa1: 48 89 e5   mov %rsp,%rbp
        3fa4: 41 57              push   %r15   ; 3fc1: ff 15 41 3f 00 00  call *0x3f41(%rip)  # 7f08 <jq_start>

A frame-pointer prologue at a 0x20 aligned boundary; the unwind table, which only enumerates real function starts,
names 0x3fa0 exactly. Neither fact depends on symbols or the network.

## 3. Which function: `process`; not a PLT stub, not .init/.fini/_start/main

`objdump -t /usr/bin/jq` (2026-10-22T12:12Z, exit 0), and `readelf -sW` on the debug file:

    0000000000002020 0000000000001cc4 main
    0000000000003cf0 0000000000000026 _start
    0000000000003fa0 0000000000000509 process
    7: 0000000000003fa0 1289 FUNC LOCAL DEFAULT 11 process

Ruled out explicitly: .init is 0x2000, .fini 0x454c, `_start` 0x3cf0, `main` 0x2020..0x3ce4 (FDE range matching its
7364 byte symbol size). No .plt, .plt.sec or .plt.got section exists; imports are called GOT-indirect, matching the
recorded `-fno-plt` compile flag, so 0x3fa0 cannot be a PLT stub. Size 0x509 = 1289 equals the FDE span 0x3fa0..0x44a9.

Name provenance, observed: the shipped file is stripped (readelf -SW finds 0 symtab sections; `nm /usr/bin/jq` prints
`no symbols`, exit 0, and `objdump -t` prints `no symbols` once DEBUGINFOD_URLS is cleared). These names come from
binutils 2.47 auto-loading separate debug info for BuildID cc56d2fd644ddd549b5339882e77f22f781525d3 out of the host
debuginfod cache. DWARF corroborates the address: `DW_AT_low_pc: 0x3fa0`, `DW_AT_high_pc: 0x509`, abstract origin
`process`, `DW_AT_decl_file : 9`, `DW_AT_decl_line : 175`, CU `src/main.c`, file table entry 9 = main.c. That this is
jq's own src/main.c `process` is inference; only the build's DWARF was read, not upstream source.

## 4. References: two calls from main, no pointer-table entry

`objdump -d /usr/bin/jq`, grep for the target (2026-10-22T12:12Z, exit 0, 2 matches):

    29d4: e8 c7 15 00 00   call   3fa0 <process>      # inside main FDE 0x2020..0x3ce4
    303d: e8 5e 0f 00 00   call   3fa0 <process>      # inside main FDE 0x2020..0x3ce4

Address-taken checks, all negative: `readelf -rW | grep -c 3fa0` prints 0 (grep exit 1; 79 R_X86_64 relocations
scanned, none with addend 0x3fa0); a byte scan of the whole file finds 0 occurrences of 0x3fa0 as an 8 byte or 4 byte
little-endian literal; .init_array holds 0x3de0 (frame_dummy) and .fini_array holds 0x3d90.

## 5. Image base 0x100000, confirmed from this wave's REA envelopes (read as files, not my runs)

- analyze-base.json (RunAnalyzeInspect), ok true, ev_14f9d92f...: `"image_base": "0x100000"`, so 0x103fa0 is VA 0x3fa0 on this PIE.
- xrefs-base.json (RunXrefsInstructions), ok true, ev_d591ef8c...: sources `0x1029d4`, `0x10303d`, `0x1063b4`, `0x106474`; minus 0x100000 these are 0x29d4 and 0x303d (my two CALL sites), 0x63b4 (.eh_frame_hdr FDE table) and 0x6474 (.eh_frame): two CALL and two unwind-metadata references.
- read-bytes-base.json (RunReadBytesLayout), ok true, ev_99b0c6e1...: `address 0x103fa0 requested 64 returned 64 complete True`, bytes_hex `554889e541574989ff415641befcffffff...` identical to `xxd -s 0x3fa0 -l 64 /usr/bin/jq`.
- instructions-base.json (RunXrefsInstructions), ok true, ev_b20a0f25...: `procedure 0x103fa0 FUN_00103fa0 contains_entry True total 1269 span 1289`, 304 instructions `0x103fa0: PUSH RBP` .. `0x1044a4: JMP`; no DWARF names imported, hence FUN_00103fa0.

## 6. Per verb: is the call well formed for this target

| verb (argv in claims.json) | well formed | reason |
|---|---|---|
| decompile 0x103fa0 | yes | exactly a function entry; the bridge tries the entry first (`functionAtOrContaining`, ReaGhidraBridge.java:2238) |
| xrefs 0x103fa0 | yes | 4 incoming references observed (2 CALL, 2 unwind data) |
| read-bytes 0x103fa0 --length 64 | yes | 64 bytes inside .text, exact translation to offset 0x3fa0, returned complete |
| function 0x103fa0 | yes | exact entry, so `getFunctionAt` succeeds instead of falling back to containing |
| instructions 0x103fa0 | yes | decodes from the prologue; 304 instructions end at 0x1044a4 inside body end 0x1044a8 |
| inspect-binary-layout | n/a | takes no address argument |

The bridge parses a bare `0x...` as an offset in the program default address space and says source coordinates need `--file-offset=0x...` instead (ReaGhidraBridge.java:2234), so 0x103fa0 is the intended form, not a file offset.

## 7. Unknowns

- Which of the four xref sources Ghidra types as CALL versus DATA is not in the envelope (source addresses only); my
  typing (two CALL, two data) rests on host disassembly plus section ranges.
- Upstream jq main.c was not opened; only the build's DWARF names line 175 of main.c.
- Analysis-created functions other than `process` are outside this question.

## 8. Sources opened (access date 2026-10-22)

1. /usr/bin/jq, sha256 e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806; quote
   "FDE cie=00000000 pc=0000000000003fa0..00000000000044a9" (.eh_frame, FDE offset 0xa4).
2. /home/vgpnk/.cache/debuginfod_client/cc56d2fd644ddd549b5339882e77f22f781525d3/debuginfo, sha256
   722996b246edf48dbaf81da84567a6210382b4ce5612662be374ab74593cdd2d, 64,256 B, pre-existing cache file (mtime
   2026-06-20), read locally; quote "7: 0000000000003fa0 1289 FUNC LOCAL DEFAULT 11 process" (.symtab entry 7).
3. /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/bridge/ghidra/ReaGhidraBridge.java, sha256
   db16aed4d16ab94da883843281ef7a8a33a244cd8379bd4013e8dee479c0a105; quote "Repeat the original target options. For
   decompile, select source coordinates explicitly with --file-offset=0x..." (line 2234).

## 9. Scratch artifacts (all under /fast/scratch/hyaku/kaidoku-r26/seats/AddressCheck/evidence/)

    8827c628f5156053cae6e06b7c3df178308afc13bb9305807d2663e9afa9afd7  01-carrier-and-layout.txt
    a733d50594d769e48b1e25d07ed54fceb090f8007b5095776e40e0788d059885  02-symbols-relocs-checks.txt
    057abde8686c0584956c6963de25531d2281547c175cbc9398ccb8ece4497a23  03-disasm-unwind.txt
    c9561c8a9a29529a28fe5e92c66a32fc3313c9c86f0b82a2b8917835e0b61715  04-debuginfo.txt
    5946b84cc85ddf801fa5a34b820d7cc811986dc3e3512ae723dfb98a848b39b9  05-sibling-envelopes.txt

Sibling envelope files cited, sha256 of the bytes I read: analyze-base.json 3b7c5e4acf86e41402803cc763da8cc66b64626798d9d2ee39ae919788efc2fb, xrefs-base.json 125ee6d20bda824ce80c16a9b061305dc8e4f1ac6b803330f2e7b024c59130df, read-bytes-base.json 3eb2f92c3d98761c421c3867b22aaceefb8a5299585b73fc93b4b59f9c711552, instructions-base.json c8852498ce38f9c3a5f353aec00fb72e7abef7bc9a8644d753bb33cac411fb11.

Tooling: nothing installed or upgraded. Nothing written in the lane except this report; no git, no jj, no REA.
