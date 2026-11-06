# SentinelInputs — adversarial inputs for `tools/round-100/upx-pe-repair.py`

Seat: SentinelInputs (sentinel), lane kaidoku R100 attempt 1. Tool attacked at
A1 = `a610671d7a01e1d762eb7103e6ee9f8a2be287ed`, read from a fresh
`git clone --shared` checkout in scratch (toplevel verified; `git status
--porcelain` empty; `git -C <lane> diff --stat A1 HEAD -- <tool>` empty, so the
bytes tested are the bytes frozen at A1). 2026-11-05. Host: `upx 5.2.0`,
`strace`, Python 3.14.8. No tools installed or updated; no pacman, no sysctl;
only scratch + this wave dir written; read-only git in the lane.

Predicate tested: every invocation exits 0 or 2 only, no Traceback, no stray
files (dir diff before/after), no write outside `--out`. Base: carrier `t32`
(sha256 pin verified) packed `upx --best -q -f` → 58 880 B, `upx -t` OK,
PackHeader at 992, c_len=35 016, c_adler=8091af36.
## Result: 2 violations in 17 crafted cases; fuzz 5000/5000 clean

| case | rc | verdict |
|---|---|---|
| c_len=0xFFFFFFFF (u_len raised) | 2 `packheader-candidates:0` | PASS |
| c_len=0 | 2 `packheader-candidates:0` | PASS |
| c_len=1, stale c_adler | 2 `checksum: 00800080 != 8091af36` | PASS |
| c_len=1, c_adler fixed to byte | 0 `ok intact`, --out written | PASS (exit 0 allowed) |
| PackHeader at file end (c_len=1,u_len=2) | 2 `truncated: ends 1025 > file 1024` | PASS |
| checksum valid, c_adler=0 | 2 `checksum: 8091af36 != 00000000` | PASS |
| two valid headers | 2 `packheader-candidates:2` | PASS |
| FIFO --in, no writer | never exits (timeout-kill) | **VIOLATION F2** |
| FIFO --in, writer closes empty | 2 `not-mz` | PASS |
| FIFO --in carrying the pack | 0 `ok intact` | PASS |
| --in /dev/zero (VA cap 4 GiB) | 1 MemoryError traceback | **VIOLATION F1** |
| 0-byte file | 2 `not-mz` | PASS |
| --out symlink→file | 0; symlink replaced by regular file, target sha unchanged | PASS |
| --out symlink→dir | 2 `output-is-directory` | PASS |
| --out dangling symlink | 0, regular file created at path | PASS |
| --out in read-only dir | 2 `output-write-failed`, no temp left | PASS |
| in-bounds huge c_len (256 MiB file, c_len=0x10000000) | 2 `checksum` in ~1 s, MAXRSS 1 063 656 KB | PASS |

Fuzz: 5000 mutations of the packed carrier (seed `0xA5A50001+idx`; 1–3 ops per
case from: 1–16 byte flips, 1–64 B block writes, truncation, 1–4096 B appends,
c_adler/c_len/u_len patches with checksum-byte fixup, compressed-data byte
corruption, 32 B zero chunks; Pool(16)): rc ∈ {0,2} in all 5000, zero
Tracebacks, zero stray/temp files, --out written iff rc 0. 0 violations.

Write-path audit (strace, `%file` + rename/unlink, full log in wave dir): the
rc 0 path makes exactly one write-mode syscall — mkstemp
`out.bin.tmp-XXXXXXXX` `O_RDWR|O_CREAT|O_EXCL|O_NOFOLLOW` in the `--out`
directory, then `os.replace`; refusal paths make zero write-mode syscalls. No
write outside the case dir in any run.

## F1 (medium) — `--in /dev/zero`: unbounded read → uncaught MemoryError, exit 1 + traceback

- Exploit: any driver/fixture that controls the `--in` path names an endless
  character device (`/dev/zero`, `/dev/urandom`). `main()` reads
  `data = fh.read()` (tool line 188) with no size bound and catches only
  `OSError`/`Refuse`/`struct.error`, so allocation failure escapes.
- Evidence (run, VA cap 4 GiB, 1.1 s): `Traceback ... line 188, in main;
  data = fh.read(); MemoryError`, rc=1. Without the cap the same code grows
  until the OOM killer SIGKILLs it [INFERENCE: exit 137; not run, to protect
  the host]. Both non-contract statuses ("exit only 0 or 2"); unbounded read
  is a local memory-DoS on the invoking process.
- Smallest remediation: catch `MemoryError` next to `OSError` → `refuse()`
  (exit 2); optionally pre-`os.stat` the input and refuse non-regular files.
- Reproducer: `repro-devzero.sh` in this wave dir (extracts tool bytes from
  the lane at A1; observed rc=1, traceback reproduced).

## F2 (low) — `--in` FIFO with no writer: blocks in `open()` forever

- Exploit: `mkfifo in.fifo` and pass it as `--in` with no writer. `open(a.inp,
  "rb")` blocks in the kernel before any Python exception path; the process
  never exits (contract: exit 0 or 2). `timeout 5` kills it (rc 124).
- Evidence: run with `timeout 5` → rc 124, empty output; reproducer
  `repro-fifo-nowriter.sh` (observed script rc 124). With a writer it behaves
  correctly (empty stream → 2 `not-mz`; real pack piped → 0).
- Impact: liveness only — the frozen battery wraps candidates in a 600 s
  timeout, so a hang wastes a cell but cannot fake a pass. Severity low.
- Smallest remediation: refuse non-regular inputs (`stat.S_ISREG`), or open
  with `O_NONBLOCK` and treat `ENXIO` as `input-unreadable`.

## Observations (no contract breach)

- O1 `--out` symlink semantics: a symlink at `--out` is replaced, not
  followed; the pointed-to file is untouched (sha verified); dangling symlink
  → regular file; symlink→dir refused. Matches the docstring's documented
  mkstemp-in-`--out`-dir atomic replace; temp is cleaned on failure
  (read-only-dir case left no temp).
- O2 Memory amplification is linear in input size: the 256 MiB probe peaked at
  ~1.04 GB RSS (~4.1×) from `data` + `bytearray` + `bytes` slice, refused in
  ~1 s. `c_len=0xFFFFFFFF` itself can only pass `ph_ok`'s `c_len <= len(b)`
  guard with a >4 GiB input, where the same ~4× amplification would be ~16 GB
  [INFERENCE — not run]. Bounded by attacker-supplied file size; a size cap
  would close even that.
- O3 All header-field attacks behave per the frozen rule: `0 < c_len < u_len`
  and `c_len <= len(b)` in `ph_ok`; the header checksum byte covers c_adler
  but not the magic; two `ph_ok` headers in the two gate windows refuse with
  `candidates:2`; a header with no byte after it refuses `truncated` from the
  compressed-data length check.
- O4 c_len=1 with a matching single-byte Adler reaches the repair path and
  exits 0 writing `--out` — a structurally absurd "pack" is accepted. Out of
  scope for the frozen predicate (exit 0 allowed), noted for the lane.

## Artifacts (wave dir `SentinelInputs/`)

`repro-devzero.sh`, `repro-fifo-nowriter.sh` (run, verified),
`repro-clen-ffffffff.bin`, `repro-two-headers.bin`, `repro-ph-at-end.bin`,
`repro-cadler-zero.bin`, `repro-clen-1-fixed.bin` (crafted inputs, ≤58 KB),
`gen-big-clen.py` (256 MiB probe rebuild), `adv.py` + `fuzz.py` (drivers),
`adv-results.json` (full per-case records incl. stderr), `strace-repair-
write-audit.log`, `fuzz-summary.txt`.

## Commands cited (all run; exact rc observed)

1. `git clone --shared <lane> $S/clone && git -C $S/clone checkout --detach a610671d...` — rc 0; `rev-parse --show-toplevel` = clone path.
2. `upx --version` → `upx 5.2.0`; `upx --best -q -f -o base.packed <DL>/t32.exe` — rc 0, 58 880 B; `upx -t -q` — rc 0 "Tested 1 file.".
3. `python3 adv.py` — rc 0, `VIOLATIONS: ['fifo_nowriter', 'devzero']`.
4. strace repair run — rc 0; strace refusal run — rc 2, zero write-mode syscalls.
5. `python3 fuzz.py` — rc 0, `fuzz cases: 5000, violations: 0`.
6. `sh repro-devzero.sh` — rc 1, MemoryError traceback; `sh repro-fifo-nowriter.sh` — rc 124.

Scratch `/fast/scratch/hyaku/kaidoku-r100/SentinelInputs` deleted after
evidence was copied into this wave dir.
