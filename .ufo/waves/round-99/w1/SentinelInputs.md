# SentinelInputs — adversarial input probe of `tools/round-99/upx-pe-repair.py` at Bk

Seat: SentinelInputs (sentinel, leaf). Lane: kaidoku. Round 99, attempt 1.
Revision probed: Bk = c19d57cd2e65a036478b9e78f6c5397dedfb2bcb (detached clone in scratch).
Tool sha256: ac97598a94c041199cdf2cc3f700257989e8d70545bddb56e154e51b85d518d8 (`tool-sha256.txt`).
UPX: 5.2.0 (`/usr/bin/upx`). Host state: read-only use; no install, no upgrade, no sysctl, no pacman.

## Verdict
2 violations in 705 CLI inputs plus 20,000 in-process mutants. Exit codes stayed in {0, 2}
except for one uncaught MemoryError (rc 1, traceback). One input hangs forever (killed at the
20 s cap). No stray files on rc 0. No write on rc 2. Victim behind an `--out` symlink untouched.

## Requirements and counts (CLI driver `fuzz.py`, 705 cases, 20 s wall cap each)
| requirement | result |
|---|---|
| exit only 0 or 2 | 503 rc 0; 200 rc 2; **1 rc 1** (V2); **1 timeout** (V1). 703 of 705 pass |
| no traceback on stderr | **1 case** (V2) |
| rc 0: no file besides --out | 0 stray files across 503 rc-0 cases |
| rc 2: --out not written | 0 violations across 200 rc-2 cases; `out-rodir` left the RO dir empty |
| victim untouched (symlink --out) | 3 of 3 packs untouched (`victim-untouched` True); symlink replaced by a regular file, target not followed |
| bounded time | 704 of 705 under 0.37 s; **max 20.021 s** (V1, killed at cap) |
| no tempfile leftovers | 0 `*.tmp-*` files found in the probe tree (`find -name '*.tmp-*'`) |

Input classes: header/section byte flips (450 + 180), FileAlignment 0/1/0xFFFFFFFF bare and
flipped (18), NumberOfSections 0xFFFF/0/1 (9), section rawdataptr+size overflowing 32 bits (9),
empty / 1-byte / 63-byte "MZ" files (4), wild e_lfanew (12), truncations at 10%/50%/99.9% (9),
directory as --in, FIFO with no writer, FIFO with EOF writer, dangling symlink and self-loop as
--in, `/dev/zero` as --in under RLIMIT_AS 1 GiB, symlink --out (3 packs + dangling target),
read-only --out dir, missing --out dir, --out == directory, --in == --out.

Refusal distribution (rc 2, all 200 cases, from the 705-case receipts): not-pe 40, packheader-candidates:0 24,
not-mz 14 (incl. empty, 1-byte and 63-byte inputs, and the FIFO EOF-writer case), sections 12, filealign-zero 6,
truncated (many variants) 40+, input-unreadable 3 (dir, dangling symlink, symlink loop),
output-write-failed 1 (RO dir), output-is-directory 1, output-dir-missing 1.

## Violations (with reproducers)
Both reproduce standalone: `bash .ufo/waves/round-99/w1/SentinelInputs/repro.sh`
(env `T=<repair.py>` `P=<UPX-packed PE>`; output: `V1 ... rc=124`, `V2 ... rc=1` plus `MemoryError`).

**V1 — FIFO as `--in` with no writer blocks indefinitely (rc None, killed at 20 s).**
- Repro: `mkfifo in.fifo && timeout 5 python3 -I -B upx-pe-repair.py --in in.fifo --out out.bin` → rc 124.
- Cause: `open(a.inp, "rb")` in `main()` on a FIFO blocks until a writer opens; the tool has no
  `stat`/`S_ISREG` check and no timeout. Violates "bounded time".
- Side effects: none (no output, no temp file). Severity: low (local availability only).
- Case: `in-fifo-nowriter` (cases/0693). The EOF-writer variant (`in-fifo-eof`) returns rc 2 `not-mz`
  (empty input), as expected.

**V2 — `--in /dev/zero` (unbounded input) under a 1 GiB address-space cap raises an uncaught `MemoryError` → rc 1 with traceback.**
- Repro: `prlimit --as=1073741824 --cpu=15 timeout 30 python3 -I -B upx-pe-repair.py --in /dev/zero --out z.bin` → rc 1, last stderr line `MemoryError`.
- Cause: `main()` does `data = fh.read()` with no size bound (repair.py line 163). The handler
  catches only `OSError` on the read and `(Refuse, struct.error)` in `repair()`; `MemoryError`
  escapes. Uncapped, the read grows without bound (source-level fact; not executed to avoid host
  memory pressure).
- Severity: low–medium (exit contract violated and unbounded memory for non-regular or huge inputs).
- Case: `in-devzero-capped` (cases/0697), runtime 0.192 s.

## Escape sweep (in-process, `inproc.py`)
20,000 mutants (uniform flips, header-window flips, 32-bit field writes, truncation plus flip)
across t32/w64/freeglut32dll packs, calling `repair()` directly.
- outcomes: ok 13,539; refuse truncated 5,274; packheader-candidates 770; not-pe 282; not-mz 65; sections 60; filealign-zero 10.
- Exception types escaping `(Refuse, struct.error)`: **none**.
- Worst `repair()` time 2.7 ms.

## Notes (observations, not violations)
- `--in == --out`: on an intact input, rc 0 and the file is byte-identical (`eq.bin`). On a repairable
  input the file is overwritten in place; the tool does not refuse aliasing. Not in the seat requirements.
- `--out` pointing at a symlink is replaced by `os.replace`, not followed; the victim is untouched.
  The victim-symlink cases return rc 0 (`ok intact`, `out_still_symlink` False).
- The repair accepts 366 header flips and 126 section-table flips with rc 0 (repair rule, by design).
  Correctness of those repairs is outside this seat.
- Not run: round-99 battery, C1 mismatch audit, controls g2..g8. Out of scope for this seat.

## Smallest remediation (not applied; lane tool is not mine to edit)
- V1: before `open`, `os.stat(a.inp)` and refuse unless `stat.S_ISREG` (new reason `input-not-regular`), so FIFOs/devices refuse rc 2.
- V2: after the stat check, refuse inputs whose `st_size` exceeds a documented bound (e.g. 256 MiB) with `input-too-large`, and/or catch `MemoryError` in the read path and return `refuse`.
- Add both reasons to the module docstring exit list.

## Receipts (`.ufo/waves/round-99/w1/SentinelInputs/`)
- `fuzz.py` (CLI driver), `inproc.py` (in-process sweep), `results.json` (705 per-case records, rc, secs, stderr tail, violations, victim-untouched flag)
- `repro.sh` (reproducers for V1 and V2; verified this run: `V1 rc=124`, `V2 rc=1`, exit 0)
- `tool-sha256.txt` (tool sha256 and Bk)
- Commands run (exit codes): `python3 -I -B fuzz.py` → 0 (summary `cases 705`, `violations 2`); `python3 -I -B inproc.py` → 0 (`escaped []`); `bash repro.sh` → 0 (V1 rc 124, V2 rc 1).

## Scratch
`/fast/scratch/hyaku/kaidoku-r99/SentinelInputs` (clone, packs, 705 cases, repro). Deleted at seat exit (rm -rf).
