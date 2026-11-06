# MutationC1 — mutation testing of R100-C1 surfaces (round 100, attempt 1)

Seat: MutationC1 (mutation-tester). Lane: kaidoku. Candidate: `tools/round-100/upx-pe-repair.py` at A1 `a610671d7a01e1d762eb7103e6ee9f8a2be287ed` (blob sha256 `15ada0b0…a37`). Counter: `tools/round-100/pe-upx-corrupt-battery.py` at A1 (blob sha256 `8f148d33…183`), identical to F (`git diff F A1 -- battery` empty). Frozen predicate: label == TARGET and exit 0.

## Method
- Mutants are single-point edits applied to a scratch clone (`git clone --shared`, detached at A1), committed in the scratch clone only. The lane was not written to; no mutating git ran in the lane.
- Repair mutants (R1-R15): scored by the frozen battery command, unmodified, against the mutated candidate: `python3 -I -B <battery> --root <clone> --repair tools/round-100/upx-pe-repair.py --rev <mutant-commit> --work <run>/work --json-out <run>/receipt.json`. Receipt `repair_sha256` equals the mutant's sha, confirming the mutant ran.
- Battery mutants (B1-B13): the counter file is copied with one edit (`counter_sha256` in each receipt differs from the frozen counter, confirming the mutant ran) and scored against the TRUE candidate at A1 (repair_sha `15ada0b0…`).
- Survivor probes (X1-X5, crafted layout): cross-checks that pair a surviving battery mutant with a harmless true-candidate defect, plus a crafted-layout input to exercise repair()'s own bound checks. Kill definition: a mutant is killed if its exit code or label differs from the pristine scoring of the same input.
- Pristine baseline on A1 (driver `baseline`): exit 0, label == TARGET, `met: true`, 154 traced invocations, 0 exec violations. Baseline validated before any mutant was scored.
- Commands and status: `python3 -I -B src/driver.py baseline` exit 0, `MET`; `python3 -I -B src/driver.py all` completed (bg_10465; 28 runs, per-run exit in `summary.json`); `python3 -I -B src/probes.py` completed (bg_10783); `python3 -I -B src/probes2.py` completed (bg_10995; re-authored exec-leg probes, see F4).
- Tooling: none installed. Used existing `python3` 3.14.8, `upx 5.2.0`, `strace 7.2`. Pacman untouched.

## Results on the true candidate (28 mutants)

| Mutant | Surface | Change | Verdict | Binding arm(s) |
|---|---|---|---|---|
| R1 | offset | `cs = i + 31` | KILLED | recovered 0/30, intact 0/10 |
| R2 | offset | `cs = i + 33` | KILLED | recovered 0/30, intact 0/10 |
| R3 | `!=`→`==` | `if got == c_adler` | KILLED | corrupt 0/40 |
| R4 | c_len slice | `cs:cs+c_len-1` | KILLED | recovered 0/30 |
| R5 | c_len slice | `cs+1:cs+c_len` | KILLED | recovered 0/30 |
| R6 | struct fmt | `">III"` (big-endian) | KILLED | corrupt 0/40, recovered 0/30 |
| R7 | refuse token | `"cheksum:"` | KILLED | corrupt 0/40 (token check) |
| R8 | struct offset | read u_adler at i+8 | KILLED | recovered 0/30 |
| R9 | adler seed | `adler32(..., 0)` | KILLED | recovered 0/30 |
| R10 | bound | `cs + c_len >= len(b)` | **SURVIVED** | see F1 |
| R11 | checksum fn | `zlib.crc32` | KILLED | recovered 0/30 |
| R12 | refuse token | `"cut: compressed data…"` | **SURVIVED** | see F1 |
| R13 | refuse msg | `"checksum: %08x != %08x"` | **SURVIVED** | see F2 |
| R14 | bound | `c_len = len(b) - cs` (clamp) | **SURVIVED** | see F1 |
| R15 | struct fmt | `"<IIH"` (16-bit c_len) | KILLED (partial) | recovered 21/30, intact 7/10, corrupt 40/40 |
| B1 | corrupt off | `off = cstart - 1` | KILLED | corrupt 0/40 |
| B2 | corrupt xor | `x = 0` | KILLED | corrupt 0/40, effective 99/119 |
| B3 | corrupt off | `off = cstart + c_len` | KILLED | corrupt 0/40, effective 99/119 |
| B4 | rc test | `rrc != 0` | SURVIVED (true) | killed by X4, see F3 |
| B5 | token | `"check" in msg` | SURVIVED (true) | killed by X5, see F3 |
| B6 | output test | drop `not os.path.exists(out)` | SURVIVED (true) | killed by X3, see F3 |
| B7 | cells | `for k in ("a",)` | KILLED | corrupt 20/40 |
| B8 | exec | `extra = execs[2:]` | SURVIVED (true) | killed by X1b, see F4 |
| B9 | exec filter | drop `execveat` from trace | SURVIVED (true) | exec-cell miss on X2b, see F4 |
| B10 | exec | `violations = []` | SURVIVED (true) | killed by X1b, see F4 |
| B11 | corrupt window | `return i + 31, c_len` | SURVIVED (true) | sampling-equivalent, see F6 |
| B12 | corrupt off | `c_len` read at i+24 | KILLED (crash) | IndexError, no receipt (exit 1) |
| B13 | counter | `n["corrupt"] += 1` | SURVIVED (true) | killed by X5 and X3, see F3 |

Killed on the true candidate: 16 of 28 (11 repair, 5 battery incl. B12 crash). Survived on the true candidate: 12 (4 repair, 8 battery).

## Survivor analysis

**F1 — repair's own compressed-data bound branch is unreached by the battery (R10, R12, R14).** The battery's truncated arm is refused by `sections()` (`truncated: file N bytes < aligned end of last section`), which runs first. No battery cell reaches `if cs + c_len > len(b)`, so that branch's comparison, token and clamp are untested. Crafted probe (`t32.upx`, last section header rptr/rsize zeroed so the section guard passes; file truncated to `cs+c_len` = 36040, and to 36039):

| candidate | len 36040 (`eq`) | len 36039 (`minus1`) |
|---|---|---|
| true | rc 0, `ok intact` | rc 2, `refused: truncated: compressed data ends at 36040 > file 36039` |
| R10 `>=` | rc 2, `truncated … 36040 > file 36040` (wrongly refused) | rc 2 (same) |
| R12 `cut:` | rc 0 | rc 2, `refused: cut: …` (token fails the battery's `truncated` check if reached) |
| R14 clamp | rc 0 | rc 2, `refused: checksum: adler32 … != c_adler …` (wrong token) |

R10 is a real behavioural difference on a crafted layout, not an equivalent mutant; R12/R14 change the refusal token on that layout. The battery cannot see any of them because it never produces such an input. This is the main coverage gap of C1: the `truncated` arm exercises only the sections guard.

**F2 — refusal message detail is outside the predicate (R13, equivalent under the frozen predicate).** The battery tests the substring `"checksum"`. R13 keeps the token and drops "adler32 of compressed data". The message is user-visible; the frozen check does not observe it. Equivalent for the predicate, not for the message contract.

**F3 — battery's refusal oracle is weak (B4, B5, B6, B13 survive the true candidate).** The true candidate never emits rc≠0,2, never emits a message containing "check" without "checksum", never writes an output while refusing, and never breaks the corrupt count. Probes on true-candidate-plus-one-defect:
- X4 (`RuntimeError("checksum…")`, uncaught, rc 1): pristine `corrupt 0 of 40` (exit 1); B4 `corrupt 40 of 40` MET → KILLED.
- X5 (`"integrity check: …"`, rc 2): pristine `corrupt 0 of 40`; B5 MET and B13 MET (`corrupt 40 of 40`) → KILLED.
- X3 (writes `--out` then refuses on checksum): pristine `corrupt 0 of 40`; B6 MET and B13 MET → KILLED.
The frozen counter is correct on these defects; the four mutants are detector-strength gaps the true candidate cannot expose.

**F4 — exec leg kills need a real extra exec; B9 is blind to execveat (B8, B9, B10).** The true candidate performs no extra exec, so `execs[1:]`, `execs[2:]` and `violations=[]` all give 0 violations. Probe X1b (one extra `execve("/bin/true")` via an `os` alias; static screen clean): pristine `exec_ok=False`, not met solely on exec; B8 and B10 MET → KILLED. Probe X2b (one extra `execveat(AT_FDCWD,"/bin/true")` via ctypes `syscall(322, …)`): pristine `exec_ok=False`; B9 `exec_ok=True` → missed at the exec cell. Full-verdict kill is masked because `ctypes` is in FORBIDDEN (static arm fails by design), so B9 is evidenced at the exec cell only. Python 3.14 exposes no `os.execveat`; an execveat-only candidate can only be built via ctypes, which the static screen catches. Residual gap: `trace=execve` silently omits execveat in the exec leg.

**F5 — the corrupt arm is not a sharp checksum oracle (R4, R5, R9, R11, R15 all pass corrupt 40/40).** Any Adler mismatch emits `checksum`, so a candidate that checksums the wrong slice passes the corrupt arm; sharpness comes from the intact/recovered arms. Observation, not a survivor.

**F6 — B11 is sampling-equivalent.** Shifting the corrupt window to `[i+31, cstart+c_len-1)` changes the drawn set by one byte at each end. Only the draw `off = cstart-1` (PackHeader checksum byte) distinguishes; per-run kill probability = Σ_carriers 4/c_len = 0.000899 over 10 carriers (`probes.json`). A kill would need pinned boundary offsets. Survived.

**F7 — B12 crashes without a receipt.** `IndexError: bytearray index out of range` in `corrupt()` (c_len read at i+24 is the wrong field). The run exits 1 with no label and no receipt. Counted as killed; it is a robustness gap in the counter's failure mode (a crash, not a clean not-met).

## Verdicts
- KILLED on the true candidate: R1-R9, R11, R15, B1, B2, B3, B7, B12 (16 incl. the crash).
- Cross-check KILLED (full verdict): B4@X4, B5@X5, B6@X3, B8@X1b, B10@X1b, B13@X5, B13@X3.
- Cross-check KILLED (exec cell only): B9@X2b.
- SURVIVED, equivalent under predicate: R13 (F2), B11 (F6, sampling).
- SURVIVED, non-equivalent on crafted layout, unreached by battery: R10, R12, R14 (F1).

## Evidence
- Receipts: `.ufo/waves/round-100/w1/MutationC1/receipts/<name>.json` (46 files: 27 mutant-run receipts, BASELINE, 18 probe-run receipts; B12 crashed before writing a receipt). Summary: `MutationC1/summary.json`; probes: `MutationC1/probes.json`, `MutationC1/probes2.json`.
- Sources and hashes: `MutationC1/src/` (`driver.py`, `probes.py`, `probes2.py`, pristine candidate and counter, `SHA256SUMS`). Pristine repair `15ada0b0…a37` and counter `8f148d33…183` match the A1 blobs (`git show A1:<path> | sha256sum`, read-only in the lane).
- L1 receipt for context: `MutationC1/c1-l1-receipt-A1.json` (copied from `.ufo/waves/round-100/l1/scores/c1-at-a610671d….json`).
- Scratch `/fast/scratch/hyaku/kaidoku-r100/MutationC1` deleted on exit after copying the above. Free space seen: /fast 388G available.

## Findings
7 (F1-F7). Recommended next step for C1: pin one repair-side crafted layout (`cs+c_len == EOF` and `cs+c_len == EOF-1`) into the counter's truncated arm, and add a write-then-refuse cell and an extra-execveat cell to the exec leg. Not done here: seats do not re-freeze counters.
