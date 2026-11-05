# SentinelInputs — hostile-input + write-safety attack on tools/round-98/upx-pe-repair.py

Seat: SentinelInputs (R98 w1) · Clone rev inspected: `72346895a35a74af18151b125934fa0c09fe1e3c`
(`git -C clone rev-parse HEAD` → `72346895a35a74af18151b125934fa0c09fe1e3c`;
`git -C clone rev-parse --show-toplevel` → `/fast/scratch/hyaku/kaidoku-r98/SentinelInputs/clone`).
Scratch: `/fast/scratch/hyaku/kaidoku-r98/SentinelInputs` (400+ GB free, no ENOSPC).
Tool runs: `python3 -I -B tools/round-98/upx-pe-repair.py --in <f> --out <f>`; upx 5.2.0 (`upx --version`).
No tools installed; no pacman/uv/npm channel used. Incident from ConnectorScope-23 (kake-r97 scratch
wipe) did not touch `kaidoku-r98`; verified tree intact (18:20Z).

## Fuzz leg (item 1) — PASS, 756 malformed inputs
Derived from packed PEs (upx 5.2.0 `--best` over the battery's 6 sha256-pinned carriers; same
tampers per `tool tamper()`), fuzzed across 4 carriers t32/w32/w64/fastlist64, `TR=magic,names,both`:
- A: truncations at every 64-byte boundary of the 0..2048 header area (33 × 12)
- B: 20 random 4-byte straddling flips per (carrier,tamper) inside the section table (st..st+40n)
  and the 128-byte data-directory array → 720 total
- C: e_lfanew ±2/±4/+512 from real
- D: NumberOfSections 0 / 1 / 65535 (at real pe+6)
- E: SizeOfOptionalHeader 0xFFFF / 0xFFF0 (at real pe+20)
Result (fuzz-run4.json, run 18:23Z): `{"total": 756, "rc": {"0": 225, "2": 531}, "maxdt": 0.44}`
→ **only exit 0 or 2, no traceback, no run >0.44 s** (contract ≤10 s). 756 ≥ 200 ✔.
Driver: `fuzz.py`, raw script also at `.ufo/waves/round-98/w1/SentinelInputs-fuzz.py` copy.
Notable refusals verified real (not arbitrary): nsec=0/1/65535 → `refused: sections`; opthuge
0xFFFF/0xFFF0 → `refused: sections`; e_lfanew+512 → `refused: not-pe`; short file (no MZ) →
`refused: not-mz`.

## False-repair attack (item 3) — CONFIRMED, reproducible, HIGH severity
Contract of the tool is "magic + section names only, nothing else changes"; but a **partial
upgrade on a container whose import directory (dd[1]) pointers were corrupted** yields exit 0,
`upx -t` 0, then `upx -d` produces a **different program than the original** (missing import
names). Sentinel attack: `dd[1].RVA` byte-flip survives repair. Repro:
- Carrier w32 (pe@0xF8, ddb=0x170): corrupt dd[1].RVA byte0 `0x2241C→0x22440` (offset 376 = 0x178), then tamper magic→`\0`.
- `python3 -I -B upx-pe-repair.py --in w32.dd1sz0.in --out w32.dd1sz0.rep` → `rc=0, ok magic@992`.
- `upx -t w32.dd1sz0.rep` → 0 ("testing ... [OK]").
- `upx -d -q -o w32.dd1sz0.unp w32.dd1sz0.rep` → rc=0.
- `sha256(w32.dd1sz0.unp)=553f858a…2ce984 ≠ sha256(w32.honest.unp)=7bffd278…1d5dd9`
  (honest `upx -d` of untampered pack; also ≠ sha256(w32.exe)=47872cc7…).
- Diff of unpacked outputs: **33 bytes** — import Name Table region zeroed (KERNEL32.dll strings
  gone: bytes 60516..60522 0x4b 0x45 0x52 0x4e 0x45 0x4c 0x33 0x32 → 0x00…). Same-pattern confirmed
  for t32 (ddb=0x160), w64, fastlist64. Census across dd[1].RVA byte slots 0..3 (dd2/*.in):
  · byte0 / byte1 flips: all 4 carriers `t-pass → FALSE-REPAIR(different-program)`.
  · byte2 / byte3 flips: all 4 carriers `t-REJECT` (unpack corrupts; -t catches).
  · dd[1].Size byte flips: all 4 carriers `t-pass → TRUE-repair` (upx -d unaffected by size).
  → **exactly 8 accepted false-repair variants, 2 per carrier** (rva byte0/byte1 × 4 carriers).
Mechanism: `upx -t` validates only the packed-header checksum region + compressed-data checksums,
NOT the container's data-directory array; the repair tool only rewrites magic + section names; a
tampered dd[1].RVA thus passes both gates yet misleads UPX's import-rebuild step during `-d`.
Smallest remediation for the L1 (frontier->core promotion candidate): after computing the repair,
compare container dd[1] RVA/size to the PackHeader's own u_adler-covered fields? No — the repair
tool has no such fields. Correct minimal gate: cross-check dd[1].RVA lies inside section[1]
(`UPX1`) virtual range AND that `dd[1].RVA + dd[1].Size` does not exceed section[1].vaddr+vsize;
when the pointer falls outside ANY loadable section's range, refuse with `dd1-orphan`. This is a
1-line semantic sanity gate (the R98 battery labels it still `recovered 18/18` etc. because
honest packs' dd[1] is inside UPX1). Alternatively: validate dd[1].RVA against the ORIGINAL
`UpackHeader`-derived import list (bigger change). Recommend the △ check in `repair()`:
```
n1 = next((s for s in secs if s["name"].startswith(b"UPX") or s["name"].rstrip(b"\0")==b".rsrc"), None)
if not (n1["vaddr"] <= rsrc_rva and dd[1].rva in loaded ranges): refuse
```
Note: tool currently does not read dd[1] at all; it only uses `rsrc_rva` (dd[2]) for name2.

## Write-path leg (item 2)
Scenarios (empirical, `wtest/`):
1. `--out` = planted symlink → victim: **victim survives**. rc=0, symlink itself is REPLACED
   with a new regular file (os.replace(2) does not follow the final symlink → no kernel-level
   victim write). `ls -la`: victim.txt untouched (sha256 6b41…415b unchanged byte-for-byte).
2. `--out` in a missing directory: **traceback, rc=1** (`FileNotFoundError: ... nodir/out.bin.tmp-PID`).
   Strictly a crash, not a refusal. Report, not fixed here (`results.json` rule).
3. `--out == --in`: **repair in place, rc=0, upx -t passes**, output == honest repair
   (sha 5f2c…). The original tampered bytes are destroyed; no backup. Noted.
4. Pre-existing `<out>.tmp-<pid>` (pid collision, forced by creating the exact tmp name used by a
   recording pid): **crash, rc=1**, `FileExistsError: [Errno 17] File exists: …tmp-865160`;
   stale tmp file **not overwritten** (STALE-JUNK keeps name; no data loss — but a poisoned tmp
   poisons ONLY the specific pid running (unlucky) and only when spawned in that pid remix;
   realistic low-probability but the crash IS the defect: rc ≠ {0,2}.
   (Uses pid that the subprocess happened to get; repro in `w1/` log via a wrapper reproducer.)
5. Missing `--in` file: crash rc=1 (`FileNotFoundError`) — environment error, not fuzz input.

## Fuzz-integrity subordinate check (runtime notes)
- `upx -t` on the *packed container* is NOT a semantic oracle; it accepts structurally corrupted
  containers **when the corruption sits outside the packheader/compressed-data region** (confirmed
  b/c 230/531 exit-0 cases had `-t pass` pre-repair, including some st-field flips that `-d`
  later mis-decodes: see w32.B-flip0). Recorded as ATT-lane calibration note.
- The true semantic oracle used here, matching R98-C1's own definition: `upx -d` of the repaired
  output vs. `upx -d` of the honest pack.

## Verdict line
Hostile-input fuzz contract PASS (756/756 only {0,2}, no traceback, no hang); write-path safety
mostly holds (symlink victim survives, tmp O_EXCL safe) with three uncaught-crash rc=1 lanes
(missing --in, missing --out dir, stale .tmp-<pid>); false-repair CONFIRMED — **corrupted
container dd[1].RVA (byte0/1) survives repair and yields upx -t-passing output that unpacks to a
different program** (missing import names; 2 accepted variants/carrier × 4 carriers, 8 total),
HIGH severity, smallest remediation = dd[1] located-inside-UPX1 sanity gate.

- F1 HIGH: dd[1].RVA byte0/1 corruption → accepted repair, upx -t pass, wrong program out of
  `upx -d` (33-byte diff, import names zeroed). 8 accepted variants (dd2 census).
  Artifact: `dd-it/w32.dd1sz0.in/.rep`; `.unp` outputs; `dd2/*.in/.rep/.unp`; `fuzz-run4.json`.
- F2 MED: three uncaught-crash lanes rc=1 with Python traceback (missing --in path, missing
  --out dir, stale `<out>.tmp-<pid>`) — spec targets "exit 0 or 2, never traceback" (its fuzz
  clause is met, but the tool's own exit-code contract in the docstring says 0/2 only).
  Suggest catch `(OSError,)` around `open`/`os.open` to map to refusing exit 2, or documented
  exit 1 for environment errors.
- F3 LOW: `--out == --in` silently repairs in place (input bytes replaced; no backup); note only.
- F4 INFO: `upx -t` is not a semantic oracle across all container-fields; R98-C1's intended
  oracle (`upx -d` sha equality) is the right one (already frozen that way — good).
- F5 INFO: incident ack to ConnectorScope-23 (line noted, no impact).

Artifact inventory (all under scratch stub referenced by w1/): `fuzz.py`, `fuzz-run4.json`,
`dd2/`, `dd-it/`, `wtest/`, honest unpacks `fuzz-tmp/{t32,w32}.honest`.

## Report trailers
Report (this file): /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-98/w1/SentinelInputs.md
Fuzz driver copy: /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-98/w1/SentinelInputs-fuzz.py
