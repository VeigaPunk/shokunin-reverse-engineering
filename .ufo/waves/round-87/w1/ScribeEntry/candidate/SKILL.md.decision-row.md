<!-- Candidate for SKILL.md. Two placements; the L1 picks one.
     (a) one row appended to `## Decision table (this host, r3-verified)` (3-column shape, after the AppImage/ELF rows);
     (b) the standalone rule block below, placed after the round-83 block near line 1979. -->

(a) row for `## Decision table (this host, r3-verified)`:

| UPX-packed ELF, `UPX!` magic tampered (no section headers, runs, `upx -l` → `NotPackedException`, high entropy, REA `analyze` a ~3-procedure stub) | `python3 -I -B tools/round-87/upx-magic-repair.py --in <f> --out <f.fixed> --json` → `upx -t <f.fixed>` rc 0 → packed-ELF route (`upx -d`, sha256, `rea analyze`) | held r87 on 4 carriers × 2 tampers (`corpus/knowledge/2026-11-04-r87-upx-magic-tamper-repair.md`; <MEASURED> of 8); UPX 5.2.0 `--best`, LE x86-64 only; entry-altered stubs, other packers, BE/PE frontier |

(b) standalone block:

### Round-87 UPX magic-tamper rule

| Symptom | Action | Status |
|---|---|---|
| ELF with **no section header table** that **runs**, `upx -l`/`upx -t` answer `NotPackedException: not packed by UPX`, the bytes are high-entropy, and REA `analyze` returns a stub-sized inventory (3 procedures on the round-68/70 carriers) | Do not read "not packed" as the answer. Run `python3 -I -B tools/round-87/upx-magic-repair.py --in <f> --out <f.fixed> --json` on a scratch copy. Exit 0 → `upx -t <f.fixed>` must exit 0 → continue on the packed-ELF route (`2026-11-03-r68-packed-elf-route`): `upx -d -q -o <out> <f.fixed>`, sha256 against any pin, `rea analyze --format json <out>`. Record the repair's `--json` (`anchors`, `restored`, `walk`) beside the receipt | held r87 (<MEASURED> of 8; counter `tools/round-87/upx-tamper-battery.py`) |
| The repair exits 2 (`no validated PackHeader`, `no l_info/p_info matching the PackHeader`, `b_info chain does not reach an end-of-chain sentinel`) | The file is not a magic-only tamper of a UPX 5.2.0 LE ELF (an altered entry/stub, altered header fields, another packer, or not packed). Nothing was written; stop and report the refusal text. Never patch bytes by hand or replace every 4-byte token globally (the cheap rule scores 4/8 and refuses nothing) | frontier |
| The repair exits 0 with `intact true` | The magic was never tampered: the output is byte-identical. Any `upx -t` failure is a different defect (payload corruption); the repair does not reach it (N2 control) | held r87 (N3 <MEASURED> of 4) |
| After repair, `cmp` against a pristine packed copy differs by 4 bytes (jq, xxd) | Expected: a non-anchor `UPX!` occurrence in the loader code is not restored. Compare the **unpacked** bytes to the pin, never the packed bytes | limit r87 |
