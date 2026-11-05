# SentinelRepair — security/robustness review of the round-91 write and search surface

Seat: SentinelRepair (sentinel), lane kaidoku, round 92, attempt 1.
Subject: `tools/round-91/upx-stop-boundary-repair.py` at declaration commit `11f8606178dfd9e72001b31daf412c5463106a63`
(base `73a882712907606eba074377b536c6dd82517e25`). Read-only on the lane; all probes ran on a `git clone --shared` checkout of that commit in scratch, which has since been removed.

Scope note: this seat's item is the security/robustness review. Building the R92-C1 candidate and running the R92-C1/C2 counters are assigned to other seats and were not run here.

## Environment and pins

| item | value | rc / evidence |
|---|---|---|
| `/usr/bin/upx` | `upx 5.2.0`, sha256 `cf2f6e7c6846a7c9a2224bc2bcc2dd79db6847d2cc73092d7356ce5c9aa8c969` (matches the battery pin) | `sha256sum`, `upx --version` rc 0 |
| Python | 3.14.8 | `python3 --version` |
| Scratch | `/fast/scratch/hyaku/kaidoku-r92/SentinelRepair` (nvme, 398 G free at start), removed at end | `df`, `rm -rf` |
| Clone HEAD | `11f8606178dfd9e72001b31daf412c5463106a63` | `git -C $S/clone rev-parse HEAD` |
| Carrier | `xxd` packed with `upx --best`, 38928 -> 19560 bytes, sha256 `1727faf91c38130249156aa1cdecc0845d67d49add0d89cc363ed3ad24eb89ff` | `receipts/carrier-packed-xxd.sha256` |

Tools installed or upgraded: none. No pacman, sysctl or host-state change. The probes never wrote under `/tmp` at all, except the one check described in (b) that deliberately reproduces the broken-`TMPDIR` fallback, which writes only a few KB.

## Harness notes (not tool findings)

- `probe_b.py` first run crashed on a format-string bug in my own probe (`set` formatting). Fixed and re-run; the re-run (`receipts/probe_b.log`) is the receipt.
- `probe_c.py` first run failed an assertion on a wrong payload byte in my own fruitful-chain builder. Fixed and re-run; the re-run (`receipts/probe_c.log`, `probe_c.json`) is the receipt.
- Packing a zero-padded ELF (`bigA`, `upx --best` rc 0, 173088 bytes) produced a file that its own `upx -t` rejects (`CantUnpackException: p_info corrupted`). That is a fixture-construction limit, not a tool result. It is why the verdict-cost measurement below uses a real ELF.
- `upx --best` on 96 MiB of `/dev/urandom` exceeded a 280 s budget (rc 124). Pack-side datum only.

## (a) Symlink and path confinement — `probes/probe_a.sh`, `receipts/probe_a.log`

`checked_target` uses `os.path.abspath` (not `realpath`) and checks `os.path.islink` on the immediate parent only. `write_atomic` writes a `mkstemp` in that parent and then `os.replace`s it onto the final path.

| case | command shape | rc | result | time |
|---|---|---|---|---|
| A0 baseline | `--in packed --out work/base-out` | 0 | `intact`, identical copy, 19560 B | <0.5 s |
| A1 `--out` is a symlink to a file outside work | `--out work/out` -> `work/outside/victim.bin` | 0 | Victim file **unchanged** (`VICTIM-ORIGINAL`). The symlink itself was **replaced by a regular file** (`symlink-survives=false`). | <0.5 s |
| A2 immediate parent is a symlink | `--out work/a2link/out` -> `a2real` | 2 | Refused `--out parent is a symlink`; `a2real` empty. | <0.5 s |
| A3 **ancestor** is a symlink that escapes | `mkdir work/esc/sub` where `work/esc` -> `outside/escape`; `--out work/esc/sub/out` | **0** | Output **written outside the work tree** (`outside/escape/sub/out`, 19560 B). The check only inspects the immediate parent, so the ancestor symlink passes. | <0.5 s |
| A4 `..` component | `--out work/sub/../out4` | 2 | Refused `carries a '..' component`. | <0.5 s |
| A5 refused input leaves `--out` alone | `--in` non-ELF, pre-existing `--out` | 2 | Pre-existing content `PRE-EXISTING` intact. | <0.5 s |
| A6 `--out` is a symlink to a directory | `--out` -> `dir-target` | 2 | Refused `--out is a directory`; `dir-target` empty. | <0.5 s |

Findings:
- **F-A3 (MED).** A3 demonstrates that the symlink guard holds only for the final parent. An ancestor symlink lets rc 0 write a file outside the declared work directory. The threat model is an operator-supplied `--out` (single-user lab), so impact is limited, but the refusal text promises a guard that does not hold. Remediation: `realpath` the parent and require it to be inside an allowed root, or walk and reject every symlink component.
- **F-A1 (LOW).** A caller's `--out` symlink is silently replaced by a regular file with rc 0 (the link is not followed, so the target is safe). Remediation: document, or refuse a symlink at the final path.
- **F-A-TOCTOU (LOW).** `checked_target` runs before `os.replace`, which is a check-then-use window. Not exploited here; relevant only to a hostile local writer.

## (b) Temp-file safety — `probes/probe_b.py`, `receipts/probe_b.log`, `receipts/probe_e.log`

- `upx_test` calls `tempfile.mkstemp(prefix=".r91-test-", dir=tempfile.gettempdir())`. The name is random, not predictable: 200 of 200 `mkstemp` calls gave distinct names, mode `0o600`. Clobbering a pre-existing file by name is not possible through this path.
- `gettempdir()` honours `TMPDIR` when it is set and usable: the probe observed `/fast/.../tmp` and no leftovers after `upx_test`. The CLI run left only `out` in the scratch tmpdir.
- **F-B1 (MED).** A set-but-missing `TMPDIR` falls back silently to `/tmp`. Command: `TMPDIR=$S/does-not-exist python3 -c 'import tempfile;print(tempfile.gettempdir())'` prints `/tmp`, rc 0. The CLI with a broken `TMPDIR` still returned rc 0 (`probe_b.log`). The verdict copy is the **whole input** (up to 256 MiB, the read cap), so on a shared `/tmp` this is an unbounded-by-policy disk write per `upx_test` call. Only the branch that reaches `upx_test` does this, so it is not every call. The size claim beyond the probed 19.5 KB is [INFERENCE] from the code (`fh.write(d)`). Remediation: fail typed when `TMPDIR` is set but not a writable directory, or pass an explicit scratch dir.
- **F-B2 (LOW).** `_clean_env()` sets `HOME=tempfile.gettempdir()`, so the packer's config lives in the same fallback directory.
- **F-B3 (LOW, verified by injection, `probe_e.py`).** `subprocess.run(..., timeout=600)` in `upx_test` raises `TimeoutExpired`. Injecting that exception on the no-successor branch gives: rc **1**, typed `error: TimeoutExpired`, no output written, `output written = False`. The `finally` unlink runs on that path. This is the correct behaviour; the 600 s bound is per verdict (see (c)).

## (c) Resource bounds for a window search — `probes/probe_c.py`, `receipts/probe_c.json`, `receipts/probe_c.log`

Timings are wall-clock on this host. The walker is `round-91`'s `classify`/`longest_prefix` via `stop-boundary-battery.layout` and the tool CLI.

**C1 — `sz_unc` near 2^31, 4-byte window.** Patched block 0's `sz_unc` to `0x7FFFFF00` in the round-87 fixture and ran the tool: rc **2** in **0.067 s**, typed `stop-boundary` refusal. Layout walk: **0.0 s**. Code reading: the walkers compare `sz_unc` only as a bound and never allocate proportional to it, so the header claim does not drive memory. [INFERENCE] `upx -t` decompression cost depends on the real stream, not the header claim; not measured.

**C2 — linear chain (rare pattern, 13-byte records).** Layout walk time scales linearly, about 0.47 µs per block:

| records | file bytes | blocks walked | layout wall |
|---|---|---|---|
| 100,000 | 1,300,136 | 100,000 | 0.044 s |
| 200,000 | 2,600,136 | 200,000 | 0.096 s |
| 400,000 | 5,200,136 | 400,000 | 0.187 s |

**C3 — candidate-fruitful chain (every record is an `l_info` candidate).** Quadratic. Layout time roughly fits `T ≈ 1.0e-7 · N²`:

| records | file bytes | layout wall | full tool wall (rc) |
|---|---|---|---|
| 5,000 | 140,100 | 2.53 s | 4.90 s (2) |
| 10,000 | 280,100 | 9.99 s | 19.74 s (2) |
| 20,000 | 560,100 | 40.76 s | 83.95 s (2) |

- **F-C1 (HIGH, availability).** Time is not bounded by the 256 MiB input cap. At 28-byte fruitful records, a full 256 MiB file has roughly 9.6 M records, which extrapolates to on the order of 10^7 s (about 3 months) for one tool run. [INFERENCE] from the fit; not run at that size. A single crafted shipped artifact can pin a worker. The cause is `derive_break` calling `chain_ok` per candidate offset, and each `chain_ok` walks the chain again. Remediation: cap candidate count or walk length (the round-87 walker already has `MAX_BLOCKS = 1 << 16`, but round-88/90 walkers do not), and add a wall-clock budget.

**C4 — per-cell verdict cost (`upx -t`), valid carriers.**

| artifact | bytes | `upx -t` rc | wall |
|---|---|---|---|
| `packed-xxd` (carrier) | 19,560 | 0 | 0.003 s |
| `cc1` packed, 48 MB unpacked | 17,726,636 | 0 (3 runs) | 0.19 s, 0.13 s, 0.13 s; RSS about 56 MB |
| zero-padded, 96 MiB overlay (invalid pack) | 173,088 | 1 (`p_info corrupted`) | 0.00 s |

Pack-side cost for the same 48 MB `cc1` at `--best`: **234.5 s** (rc 0). This matters only if a future seat packs per cell; the frozen battery packs each carrier once.

**The 33-candidate bound.** For a ±16 window (33 values), each candidate needs one `upx -t` verdict on a private copy. Measured verdict cost is 0.003 s to 0.19 s for carriers up to 17.7 MB, so the verdict is cheap for these sizes. The bound is set by the **hard timeout**: `upx_test` allows 600 s per verdict and there is **no aggregate budget**, so a hung packer yields 33 x 600 s = 5.5 h per cell before any refusal. Separately, if each candidate re-runs the walker (as `derive_break` does), the layout cost multiplies by 33: for the 20k-record fruitful case that is about 33 x 40.8 s = 22 min of walker time for one cell, with no bound on N (see F-C1).

- **F-C2 (MED).** No aggregate time or count budget across the 33 candidates; per-verdict bound is 600 s. Remediation: a single deadline for the whole search, and a candidate pre-filter that the walker can decide without the packer.

## (d) `read_input` cap — `probes/probe_d.sh`, `receipts/probe_d.log`

`MAX_INPUT = 256 << 20` = **268,435,456** bytes (checked by `python3 -c 'print(256 << 20)'`).

| case | rc | result | time / memory |
|---|---|---|---|
| D1 cap+1 (268,435,457 B, sparse) | 2 | `input exceeds 268435456 bytes`; no read; no output | <0.1 s |
| D2 exactly cap (sparse zeros) | 2 | Read fully, then `not a little-endian ELF` | read 0.20 s, max RSS 282,792 kB |
| D3 `--in` is a directory | 2 | `input is not a regular file` | <0.1 s |
| D4 `--in` is a symlink to a regular file | 2 | `input is not a regular file` (`lstat` sees the link) | <0.1 s |
| D5 `--in` missing | 2 | `cannot stat input: No such file or directory` | <0.1 s |

- **F-D1 (LOW, passes).** The cap is enforced before the read at cap+1 with a typed refusal. At the cap, peak RSS is about 1.05x the cap, and the read is fully in memory; that is the stated design, not a defect.
- Note: `lstat`-based S_ISREG means a symlink `--in` is refused even when it points at a regular file. Intended.

## Severity summary

| id | sev | check | one-line |
|---|---|---|---|
| F-C1 | HIGH | (c) | Walker is quadratic in fruitful records; time is not bounded by the 256 MiB cap (about 3 months extrapolated for a max-size crafted input). |
| F-A3 | MED | (a) | Ancestor-symlink escape: rc 0 writes outside the work tree. |
| F-B1 | MED | (b) | Missing `TMPDIR` falls back to `/tmp`; `upx_test` copies the whole input there. |
| F-C2 | MED | (c) | No aggregate budget across the 33-candidate search; 600 s per verdict. |
| F-A1 | LOW | (a) | `--out` symlink at the final path is silently replaced (target safe). |
| F-A-TOCTOU | LOW | (a) | Check-then-replace window (local attacker only). |
| F-B2 | LOW | (b) | `HOME` set to the temp directory, so packer config lands in the fallback `/tmp`. |
| F-B3 | LOW | (b) | Timeout raises typed rc 1, no output; behaviour correct. |
| F-C-ok | LOW | (c) | `sz_unc ≈ 2^31`: rc 2 in 0.067 s; linear walker about 0.47 µs/block. |
| F-D1 | LOW | (d) | Cap at 256 MiB enforced before read; cap+1 rc 2, no output. |

Passing checks (no defect): A2 (immediate-parent symlink refused), A4 (`..` refused), A5 (refused input leaves `--out` untouched), A6 (directory `--out` refused), B mkstemp naming and mode, D1 to D5.

## Smallest remediations (in priority order)

1. Bound the layout walk: a per-invocation candidate and step budget, plus a deadline across the whole search (F-C1, F-C2).
2. Resolve `--out` and `--info` with `realpath` against an allowed root, and reject any symlink component (F-A3).
3. Fail typed when `TMPDIR` is set but not a writable directory, and pass an explicit scratch directory to `upx_test` (F-B1, F-B2).

These are findings only; no lane file was changed. Remediation belongs to whichever seat owns the candidate build.

## Receipts (seat directory)

- `receipts/probe_a.log` — A0 to A6 (rc and output per case)
- `receipts/probe_b.log` — mkstemp naming, `TMPDIR` honour, CLI with broken `TMPDIR`
- `receipts/probe_c.log`, `receipts/probe_c.json` — C1 to C4 timings and rc
- `receipts/probe_d.log` — D1 to D5
- `receipts/probe_e.log` — timeout injection
- `receipts/carrier-packed-xxd.sha256` — carrier sha256
- `probes/probe_a.sh`, `probes/probe_b.py`, `probes/probe_c.py`, `probes/probe_d.sh`, `probes/probe_e.py` — the probe sources
- `SHA256SUMS` — checksums of every receipt and probe file

Inline commands for reproduction: `bash probes/probe_a.sh`, `python3 probes/probe_b.py`, `python3 probes/probe_c.py`, `bash probes/probe_d.sh`, `python3 probes/probe_e.py`. Each expects the scratch clone and carrier from the setup step, which was removed; regenerate them from the commit above to rerun.
