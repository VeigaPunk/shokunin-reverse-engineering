# RevOracleVsReadobj — oracle `locate()` vs llvm-readobj / objdump / llvm-objcopy

Seat: KaidokuR30.RevOracleVsReadobj (reviewer). Scope: does the independent oracle
locate each carrier's `.dep-v0` section exactly as two other readers do, and is it
independent of REA. All times UTC; host is UTC-3, so file mtimes shown +3h.

## Disclosure — I am the writer that altered 4 carriers (L1 question answered)

At 02:42:35Z and 02:43:14Z my `llvm-objcopy --dump-section <sec>=<out> <input>`
invocations were run **without an output-object argument**. llvm-objcopy then
rewrites the input file in place. First batch (manual probe, 02:42:35Z) hit
`elf-x86_64-uvx`, `pe-x86_64-uvx`, `macho-x86_64-uvx`; second batch (my
`compare.py` run, 02:43:14Z) reached `elf-x86_64-uv` before aborting on a stale
sha256 assert. The 0444 mode did not protect (file rewrite, not write(2)); L1
restored all 4 from wheel members at ~02:46Z and set chattr +i — verified:
`lsattr` shows `----i` on all 16 and all 16 sha256 now MATCH the frozen TSV.

The rewrite was byte-level normalization only: on my drifted snapshot copies,
`oracle.locate` still finds `.dep-v0` at the same offset/size and the section
payload is **byte-identical** to canonical (same slice sha256). No data was lost
for the `.dep-v0` question, but the carrier files were not the frozen bytes;
L1's restore was correct and necessary. Driver now always passes an explicit
output object (`compare.py` `objcopy_dump`, comment at line 51-52).

Evidence: drifted-vs-canonical `cmp` showed 849/761/2626/484 differing byte
positions plus EOF truncation; recovered wheel members reproduce the frozen
sha256 exactly (e.g. `elf-x86_64-uv` wheel member →
`3e801df8…d592df0`, `pe-x86_64-uvx` → `3489d693…a4acc89`).

## Method

For each of the 16 frozen carriers (bytes verified sha256 == carriers.tsv col 7
at run time, all `----i` immutable):

1. `oracle.locate(data)` → `{offset, size}`; slice `data[off:off+size]` hashed.
2. `llvm-readobj --sections` (LLVM 23.1.3) → per-format mapping: ELF `Offset:`/`Size:`;
   Mach-O `Offset:`/`Size:`; PE `PointerToRawData:` and `min(VirtualSize,RawDataSize)`
   (the oracle's own `size = rawsize if vsize == 0 else min(vsize, rawsize)`).
3. `objdump -h` (GNU binutils 2.47) where it recognizes the format: ELF (all 6),
   PE x86_64 (3). Unsupported: PE arm64 (3), Mach-O (4) — `file format not recognized`.
4. `llvm-objcopy --dump-section` (`__DATA,.dep-v0` for Mach-O) with an explicit
   output path, dump bytes sha256-compared against the oracle slice.

Command: `timeout 600 python3 -I -B compare.py` (exit 0, 1.82 s, 2026-10-23T02:46Z).

## Results — 16 rows, zero disagreements (observation)

RO = llvm-readobj offset+size equal; OD = objdump size+fileoff equal;
OC = llvm-objcopy dump sha256 == oracle slice sha256.

| carrier              | fmt   | oracle off | size | readobj | objdump | objcopy sha |
|----------------------|-------|-----------:|-----:|---------|---------|-------------|
| elf-x86_64-uv        | elf   | 0x25dcc98  | 9870 | eq      | eq      | eq          |
| elf-x86_64-uvx       | elf   | 0x4e0cf    | 9870 | eq      | eq      | eq          |
| elf-aarch64-uv       | elf   | 0x201ff54  | 9871 | eq      | eq      | eq          |
| elf-aarch64-uvx      | elf   | 0x4628c    | 9871 | eq      | eq      | eq          |
| elf-riscv64-uv       | elf   | 0x229db8b  | 9737 | eq      | eq      | eq          |
| elf-riscv64-uvx      | elf   | 0x45d49    | 9737 | eq      | eq      | eq          |
| pe-x86_64-uv         | pe    | 0x1f9e600  | 9943 | eq      | eq      | eq          |
| pe-x86_64-uvx        | pe    | 0x4d400    | 9943 | eq      | eq      | eq          |
| pe-x86_64-uvw        | pe    | 0x4d200    | 9943 | eq      | eq      | eq          |
| pe-arm64-uv          | pe    | 0x1f4e400  | 9938 | eq      | NA      | eq          |
| pe-arm64-uvx         | pe    | 0x49a00    | 9938 | eq      | NA      | eq          |
| pe-arm64-uvw         | pe    | 0x49800    | 9938 | eq      | NA      | eq          |
| macho-x86_64-uv      | macho | 0x26fb828  | 9666 | eq      | NA      | eq          |
| macho-x86_64-uvx     | macho | 0x4b350    | 9666 | eq      | NA      | eq          |
| macho-arm64-uv       | macho | 0x1b8e218  | 9667 | eq      | NA      | eq          |
| macho-arm64-uvx      | macho | 0x48d40    | 9667 | eq      | NA      | eq          |

PE note: readobj `RawDataSize` is 10240 for all PE carriers vs oracle/effective
size 9943/9938 (`min(VirtualSize, RawDataSize)`); `llvm-objcopy --dump-section`
emits exactly the effective size, byte-identical to the oracle slice. The oracle's
min() convention is the one the LLVM writer round-trips — agreement is real, not
coincidental padding luck.

## REA independence (observation)

`tools/round-30/rust_dep_oracle.py` AST imports: `json`, `struct`, `zlib` only.
Grep for `subprocess|npx|rea|exec\(|eval\(|socket|urllib|requests` → no hits
outside the docstring ("Shares no code with REA"). It is a pure-Python struct
parser; it cannot invoke REA's npm CLI or share code with it. The module also
loads under `python3 -I -B` (isolated) via `importlib.util.spec_from_file_location`
from the lane path with no package deps.

## Verdict

**HOLDS.** On all 16 carriers the oracle's `locate()` offset and size equal
llvm-readobj's on every format, equal objdump's on all 9 formats binutils
recognizes, and the sliced bytes are sha256-identical to llvm-objcopy's dumped
section on all 16. The oracle imports nothing from REA and shares no code with it.
No disagreement → no findings in scope. Residual: none observed; the only anomaly
was my own carrier mutation, disclosed above and fully remediated by L1.

## Artifacts (all under /fast/scratch/hyaku/kaidoku-r30/seats/w1/RevOracleVsReadobj/)

- `compare.py` — driver; sha256 aa287a2053aacdd6a42e370e8320ee99bf6d4085c569f7063c81856467a2c5f2
- `results.json` — full per-carrier measurements; sha256 023a27831baedb8c02f46c649c4009cdd368c5daa713f8c2c9f46653e25bd2b1
- `snap-sha256.txt` — snapshot hashes incl. drifted copies; sha256 c72c39a47d307571e93935c5509a9882ebe9f4523e5b12b744485fe290a89e32
- `section-hashes.txt` — per-carrier oracle slice sha256; sha256 7647a8d5623101ce13d4418bd8f8874c21fac38b3895af5d29575145a1c935ff
- `snap/` — byte copies of all 16 carriers as observed (4 drifted + 12 canonical)
- `snap/*.orig` — canonical members re-extracted from verified wheels (4 files)
- `dump/*.bin`, `dump/*.objout` — llvm-objcopy outputs

Installs: none (llvm-readobj/llvm-objcopy 23.1.3 and GNU objdump 2.47 preinstalled).
No REA run; no git/jj writes; lane touched read-only except this report.
