# Report: ExecHeldOut — out-of-population probe of tools/round-98/upx-pe-repair.py (round 98, findings only)

- Seat: ExecHeldOut (executor, lane kaidoku). Item: probe only, no claim change.
- Clone: `git clone --shared /home/vgpnk/Projects/shokunin/kaidoku-shokunin $S/clone` rc 0;
  `git -C $S/clone checkout --detach 72346895a35a74af18151b125934fa0c09fe1e3c` rc 0;
  `git -C $S/clone rev-parse HEAD` = `72346895a35a74af18151b125934fa0c09fe1e3c` rc 0;
  `git -C $S/clone rev-parse --show-toplevel` = `$S/clone` rc 0 (asserted before any write).
- Env: `/usr/bin/upx --version` → `upx 5.2.0` rc 0 (matches battery preflight; no install needed, no pacman/uv/binary installs performed, nothing written to PATH dirs); `python3` 3.14.8; `/usr/bin/jq` is jaq 3.1.1 (ELF x86-64, noted); free space seen: /fast 406G, /home 707G (no ENOSPC).
- Scratch: `$S=/fast/scratch/hyaku/kaidoku-r98/ExecHeldOut`; TMPDIR under it; all work in `$S/work`; deleted after report. Harness note: first ELF attempt copied jq via `copyfile` (lost exec bit → upx CantPack rc 1); corrected in probe2 with `os.chmod(0o755)`; the bad edge run was discarded and `probe-edge.json` rewritten with corrected data.

## Method (mirrors frozen battery `pe-upx-tamper-battery.py` @ L)
Pack `upx <mode> -q -o packed orig`; ref = sha256(`upx -d -q`); tamper bytes; `upx -t -q tampered` rc≠0 ⇒ effective;
repair = `python3 -I -B $S/clone/tools/round-98/upx-pe-repair.py --in tampered --out rep` (battery invocation);
recovered = repair rc 0 ∧ `upx -t -q rep` rc 0 ∧ sha256(`upx -d rep`) == ref (packer is the oracle).
Tampers: battery T1 magic (first `UPX!`→00000000), T2 names (UPX* sections→.text/.data/.rdata by position), T3 both;
my two: magicrand (first `UPX!`→random 4 bytes, this run `0e919f96`), sec2 (rename section 2 `.data` only if it is `UPX2*`).

## Matrix (every cell; cell = t_rc/repair_rc/post_t_rc/recovered; NA = not constructible; sha12 = packed sha256 prefix)
| carrier | mode | pack | packed sha12 | intact | magic | names | both | magicrand | sec2 |
|---|---|---|---|---|---|---|---|---|---|
| wallace-src (PE32 i386, 7 sec) | best | 0 | 6a7a30002774 | 0/0/0/1 | 1/0/0/1 | 1/0/0/1 | 1/0/0/1 | 1/0/0/1 | NA (.rsrc) |
| wallace-src | -1 | 0 | 374b1538fcf3 | 0/0/0/1 | 1/0/0/1 | 1/0/0/1 | 1/0/0/1 | 1/0/0/1 | NA (.rsrc) |
| wallace-src | --lzma | 0 | 262b7b967ea7 | 0/0/0/1 | 1/0/0/1 | 1/0/0/1 | 1/0/0/1 | 1/0/0/1 | NA (.rsrc) |
| wallace-src | --best --brute | 0 | d372c9ce26a7 | 0/0/0/1 | 1/0/0/1 | 1/0/0/1 | 1/0/0/1 | 1/0/0/1 | NA (.rsrc) |
| wallace-v2 (PE32 i386, 7 sec) | best | 0 | dd3c40c96b49 | 0/0/0/1 | 1/0/0/1 | 1/0/0/1 | 1/0/0/1 | 1/0/0/1 | NA (.rsrc) |
| wallace-v2 | -1 | 0 | 719ca8be5263 | 0/0/0/1 | 1/0/0/1 | 1/0/0/1 | 1/0/0/1 | 1/0/0/1 | NA (.rsrc) |
| wallace-v2 | --lzma | 0 | f3e3d96ebfef | 0/0/0/1 | 1/0/0/1 | 1/0/0/1 | 1/0/0/1 | 1/0/0/1 | NA (.rsrc) |
| wallace-v2 | --best --brute | 0 | 42e3a4be7051 | 0/0/0/1 | 1/0/0/1 | 1/0/0/1 | 1/0/0/1 | 1/0/0/1 | NA (.rsrc) |
| fastlist86 (pnpm vendor, x86) | best | 0 | 4bbb7d0ae2cd | 0/0/0/1 | 1/0/0/1 | 1/0/0/1 | 1/0/0/1 | 1/0/0/1 | NA (.rsrc) |
| fastlist86 | -1 | 0 | f9c9e956061c | 0/0/0/1 | 1/0/0/1 | 1/0/0/1 | 1/0/0/1 | 1/0/0/1 | NA (.rsrc) |
| fastlist86 | --lzma | 0 | 30d9f10d8edc | 0/0/0/1 | 1/0/0/1 | 1/0/0/1 | 1/0/0/1 | 1/0/0/1 | NA (.rsrc) |
| fastlist86 | --best --brute | 0 | 7bbff0bb7a5a | 0/0/0/1 | 1/0/0/1 | 1/0/0/1 | 1/0/0/1 | 1/0/0/1 | NA (.rsrc) |
| t64-arm (PE32+ ARM64, 6 sec) | all 4 modes | 1 | — | — | — | — | — | — | — |
| w64-arm (PE32+ ARM64, 6 sec) | all 4 modes | 1 | — | — | — | — | — | — | — |
Totals: packable cells 12 (carrier×mode); intact 12/12 ok; tamper cells run 48, effective 48/48, recovered 48/48, unpack sha256 == ref in every recovered cell; sec2 NA ×12. Refunpack refs: wallace-src `c238fb59db4a`, wallace-v2 `74a132f399ab`, fastlist86 `f2bb7a4b837e` (identical across pack modes, as expected). Carrier sha256s in `probe-env.json` (packheader found at offset 992 in every packed file).

## Edge probes
| input | repair | evidence |
|---|---|---|
| packed ELF (`upx --best -q` on jq/jaq x86-64, 30800→14036, `upx -t` rc 0) | rc 2, no --out | `refused: not-mz` |
| raw ARM64 t64-arm.exe / w64-arm.exe (unpacked, not UPX) | rc 2 ×2, no --out | `refused: packheader-candidates:0` |
| ARM64 pack attempt, all modes | upx rc 1 | `upx: ...t64-arm.orig: CantPackException: win64/arm64 is not yet supported` |
| packed wallace-src.best truncated −96 B (10752→10656, ≥ c_len 8113) | **rc 0, --out written, `ok intact`** | post `upx -t` rc 1; out sha256 c6ef63738a51... |
| truncated to exactly c_len (8113 B) | **rc 0, `ok intact`** | post `upx -t` rc 1 |
| truncated to c_len−1 (8112 B); truncated to half (5376 B) | rc 2 ×2, no --out | `refused: packheader-candidates:0` |

## Findings (findings-only; no claim change)
1. **Generalization holds out-of-population**: 48/48 tamper cells effective and recovered, 12/12 intact arms clean, across 3 unfrozen win32/pe carriers (2 Ghidra Wallace, 1 pnpm fastlist x86) × 4 pack modes (`--best`, `-1`, `--lzma`, `--best --brute`). Pack mode and method choice do not move the PackHeader out of the tool's two structural windows. Supports R98-C1 coverage beyond the frozen six; the C1 predicate itself untouched.
2. **Truncated-PE false accept** (new, minor): `upx-pe-repair.py` exits 0 "ok intact" on a packed PE truncated to any size ≥ c_len (verified at −96 B and at exactly 8113 B; out file written; `upx -t` then fails rc 1). Its only size sanity is `c_len <= len(b)` (≤, not integrity-checked). Inside the battery this is harmless (upx -t re-checked before scoring), but standalone "exit 0 = repaired/intact" is wrong for truncated payloads. Boundary is exact: refuses at c_len−1 with `packheader-candidates:0`.
3. **sec2/UPX2 branch unexercised out-of-population**: every win32/pe pack here names section 2 `.rsrc` at pack time (12/12), so the UPX2-rename tamper is not constructible on these carriers; the tool's resource-RVA heuristic branch (`name2` → `.rsrc` vs `UPX2`) was only hit via `.rsrc`-passthrough. In-population win64/pep (fastlist64) remains the only UPX2 exercise; if a future carrier is a PE32 without a resource directory, that branch would matter.
4. **Refusals correct on non-targets**: packed ELF → rc 2 `not-mz`; raw non-UPX ARM64 PE → rc 2 `packheader-candidates:0`; both with no --out, matching the refused-arm contract (exit 2 semantics) outside the frozen population.
5. **No packed-ARM64 population exists for UPX 5.2.0** (`CantPackException: win64/arm64 is not yet supported`, rc 1, all four modes, both distlib ARM64 launchers) — the ARM64 distlib carriers are structurally out of reach for this tamper class until UPX gains win64/arm64.
6. Harness note, not a tool finding: `copyfile`-based carrier copies lose exec bits and upx then refuses to pack ("file not executable; try 'chmod +x'"); the frozen battery avoids this by scoring only PE/ARM carriers, irrelevant there.

## Commands cited (all run this session, exit codes inline)
- `git -C /fast/scratch/hyaku/kaidoku-r98/ExecHeldOut/clone rev-parse HEAD` rc 0 → 72346895a35a74af18151b125934fa0c09fe1e3c
- `/usr/bin/upx --version` rc 0 → upx 5.2.0; `file <4 carriers>` rc 0 → PE32 i386 / PE32+ ARM64 / ELF x86-64
- pack (representative): `upx --best -q -o $W/wallace-src.best.upx $W/wallace-src.orig` rc 0
- tamper test (representative): `upx -t -q $W/wallace-src.best.magic.tam` rc 1 (effective)
- repair (representative): `python3 -I -B $S/clone/tools/round-98/upx-pe-repair.py --in $W/wallace-src.best.both.tam --out $W/wallace-src.best.both.rep` rc 0, msg `ok magic@992,name0,name1`
- post: `upx -t -q <rep>` rc 0; `upx -d -q -o <unp> <rep>` rc 0; sha256 == ref (all 48 cells)
- edges: repair on `jq2.upx` rc 2; on raw ARM64 rc 2; `upx --best -q -o arm.try t64-arm.orig` rc 1 (exact stderr quoted above); truncation sweep rc 0/0/2/2 as tabled.

## Receipts (all under /home/vgpnk/Projects/shokunin/kaidoku-shokunin)
- .ufo/waves/round-98/w1/ExecHeldOut/probe-env.json — env, clone HEAD, carrier sha256/sizes, upx/python, free bytes
- .ufo/waves/round-98/w1/ExecHeldOut/probe-cells.json — all 80 matrix records (12 intact, 48 tamper, 12 sec2-NA, 8 pack-fail)
- .ufo/waves/round-98/w1/ExecHeldOut/probe-edge.json — ELF/ARM64/truncation edges (probe2, corrected)
- .ufo/waves/round-98/w1/ExecHeldOut.md — this report

## Risks / blockers
- No blockers. Frozen artifacts untouched (tools/round-98, .ufo/waves/round-98/pre, .ufo/waves/round-98/l1, corpus/, plans/ all read-only for this seat); no git mutations anywhere except the mandated clone checkout; no host changes (no sysctl, no pacman). Finding 2 is advisory for the L1 only; it does not weaken C1 because the battery re-tests with `upx -t`.
