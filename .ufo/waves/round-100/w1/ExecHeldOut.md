# ExecHeldOut — R100-C1 held-out generalization (2026-11-05)

Seat: ExecHeldOut (executor, leaf). Item: attack the R100-C1 candidate
`tools/round-100/upx-pe-repair.py` on held-out PEs outside the battery's
CARRIERS. Revision used: A1 `a610671d7a01e1d762eb7103e6ee9f8a2be287ed`
(shared clone; `git rev-parse --show-toplevel` verified == clone before any
write; CARRIERS read from `pe-upx-corrupt-battery.py` at the same rev).
Host: upx 5.2.0 (/usr/bin/upx), strace 7.2, python 3.14.8. No tool installs
needed (pacman untouched; no writes to PATH dirs). Scratch
`/fast/scratch/hyaku/kaidoku-r100/ExecHeldOut` with TMPDIR pointed into it;
deleted after receipts were copied out. Free space seen: 379G on /fast (no ENOSPC).

## Held-out carriers (9 paths, none in CARRIERS — asserted in driver)

| slug | file (absolute) | sha256 (original) | size | pack |
|---|---|---|---|---|
| llio64-amd64 | /opt/ghidra/GPL/DMG/data/os/win_x86_64/llio_amd64.dll | e489648829326402adb68d415be6b98c2d0e48a8602bca3764371f3a9058a6ef | 64000 | -1 |
| llio64-i386 | /opt/ghidra/GPL/DMG/data/os/win_x86_64/llio_i386.dll | e855478acf0d36f846befb48bfd239b7ef46e568e2408091591adec274ed0879 | 61952 | --best |
| llio32-amd64 | /opt/ghidra/GPL/DMG/data/os/win_x86_32/llio_amd64.dll | e489648829326402adb68d415be6b98c2d0e48a8602bca3764371f3a9058a6ef | 64000 | --best |
| wallace-src | /opt/ghidra/docs/GhidraClass/ExerciseFiles/VersionTracking/WallaceSrc.exe | 168a175ccf74e80899d2519bbe6e1ae8b0fa2489af70e8cc0720afab1ad8b0ab | 33792 | --lzma |
| wallace-v2 | /opt/ghidra/docs/GhidraClass/ExerciseFiles/VersionTracking/WallaceVersion2.exe | 94510664e6578bec7391d6023af414e2d2d8c4ff58ed3f618dd549ff648015cf | 33792 | --best |
| agent-browser | /home/vgpnk/.local/share/fnm/node-versions/v24.21.0/installation/lib/node_modules/agent-browser/bin/agent-browser-win32-x64.exe | a6a9a3654c41ee19c05961b73489db98cff9eae88a77436986df08a7a7a73786 | 17694720 | -1 |
| dbghelp-amd64 | /home/vgpnk/.local/share/uv/tools/flare-capa/lib/python3.12/site-packages/vtrace/platforms/windll/amd64/dbghelp.dll | abd6a38e9d73b0ed73372e80819eca9134534c17722ced453e5e1cbffef03ec2 | 1532048 | --best |
| dbghelp-i386 | /home/vgpnk/.local/share/uv/tools/flare-capa/lib/python3.12/site-packages/vtrace/platforms/windll/i386/dbghelp.dll | 58f3cbcede6bbc4aa98f272baa8bba5b6141c762642e0c00ed5d24bce172991b | 1231000 | --lzma |
| symsrv-amd64 | /home/vgpnk/.local/share/uv/tools/flare-capa/lib/python3.12/site-packages/vtrace/platforms/windll/amd64/symsrv.dll | 62e6e7efba96592e2e13af4c7f3ec7aaa0750f10e63984c26c7f26e11a0e528e | 142992 | --best |

Methods: --best ×5, --lzma ×2 (wallace-src, dbghelp-i386), -1 ×2
(llio64-amd64, agent-browser); all packed rc0 with `upx <flags> -q -f -o`.
Disclosure: llio64-i386 is byte-identical to carrier `llio32dll`
(win_x86_32/llio_i386.dll, Ghidra duplicate distribution) and
llio64-amd64 == llio32-amd64; path-held-out for all 9, content-new for 8.
Full pack facts (packed sha256/size, PackHeader offset, c_len) in manifest.json.

## Cases: 9 files × 11 = 99 (seed 20261105, rng = Random(SEED*1000+crc32(slug)))

Per file: intact; 6 random single-byte flips inside the compressed data
[PackHeader+32, PackHeader+32+c_len) — located with the candidate's own
`sections()`/`find_packheader()` imported from the A1 clone; 2 section-table
flips (UPX0 name byte, UPX1 VirtualSize byte); PackHeader magic tamper
(UPX!→ABCD); random overlay append (64–256 B). Oracle `upx -t` ran on every
input and, when the candidate returned rc0, on its `--out`. Candidate invoked
as `python3 -I -B upx-pe-repair.py --in <i> --out <o> --json` (TMPDIR in scratch).

## Verdicts

- SOUND (rc0 ⇒ `upx -t` of output rc0): 45 rc0 outputs, 45/45 oracle rc0. Violations: 0.
- COMPLETE (`upx -t` checksum error ⇒ refuse `checksum`): 54/54 payload flips
  → oracle rc1 "Exception: checksum error"; candidate rc2 with
  `{"refused": "checksum: adler32 of compressed data <got> != c_adler <hdr>"}`
  in all 54, no `--out` written. Violations: 0.
- OVER-REFUSAL (refuse where oracle input rc0): 0 — every intact / vsize-flip /
  overlay input passed the oracle and the candidate returned rc0.
- Candidate exit statuses seen: {0, 2} only; crashes 0; unpacked/negative
  paths not needed (all files packed).

| case kind | n | `upx -t` input | candidate | `upx -t` output |
|---|---|---|---|---|
| intact | 9 | 9 ok | 9 rc0, no changes | 9 ok |
| payload0–5 (6×9) | 54 | 54 checksum error | 54 rc2 refuse `checksum` | n/a |
| UPX0-name flip | 9 | 5 CantUnpackException / 4 ok | 5 repaired `name0` / 4 rc0 intact | 9 ok |
| UPX1-vsize flip | 9 | 9 ok | 9 rc0 intact | 9 ok |
| magic UPX!→ABCD | 9 | 9 CantUnpackException | 9 repaired `magic@<ph>` | 9 ok |
| overlay append | 9 | 9 ok | 9 rc0 intact | 9 ok |

--lzma and -1 packs behaved identically to --best packs on every case kind
(per-case rows in results.json carry the method).

## Findings

Adverse disagreements: **0**. Supporting:
1. Repairs are byte-exact and deterministic: the dbghelp-amd64 UPX0-name
   repair output sha256 `c9fa5567337699b4873071cea5c68444210bb6562dfa1baa0f7ce745fc5ceed6`
   equals the untampered pack's sha256; two runs on the same input produced
   identical output sha256.
2. The 5/4 split on UPX0-name flips is exactly the S324 unpack gate: flips in
   name bytes 0–2 ("UPX") make the oracle throw CantUnpackException and the
   candidate repair them; flips in NUL padding (byte 4–6) keep
   `memcmp(name,"UPX",3)` true — oracle passes, candidate leaves the file
   untouched. Candidate and packer agree on which names matter.
3. Process-level exec guard generalizes: `strace -f -e trace=execve` over a
   refused payload run shows exactly one execve — the launcher python3
   itself; the candidate spawns nothing (execve-strace.txt).

## Cited commands (all run; full CMD/RC transcripts in per-case logs)

- `upx -t cases/dbghelp-amd64-payload0/input.bin` → rc1
  `upx: …: Exception: checksum error`
- `python3 -I -B …/upx-pe-repair.py --in cases/dbghelp-amd64-payload0/input.bin --out …/out.bin --json`
  → rc2 `{"refused": "checksum: adler32 of compressed data e7fa6bc6 != c_adler e7046c23"}`
- `upx -t cases/agent-browser-magic/input.bin` → rc1
  `CantUnpackException: file is possibly modified/hacked/protected`
- candidate on that magic input → rc0 `{"packheader": 517, …, "changes": ["magic@517"]}`;
  `upx -t cases/agent-browser-magic/out.bin` → rc0 `[OK]`
- `upx -t cases/dbghelp-amd64-intact/input.bin` → rc0 `[OK]`

## Files written

- Report: .ufo/waves/round-100/w1/ExecHeldOut.md (this file)
- Supporting: .ufo/waves/round-100/w1/ExecHeldOut/{manifest.json,results.json,run.log,execve-strace.txt}
- results.json: 99 case records with exact flip offset/old/new, oracle rcs and
  verdict lines, candidate rc/refusal strings, output shas.
- Scratch deleted after copies. No lane file outside my wave dir touched; no
  git/jj mutation anywhere (read-only git in the shared clone only).

## Risks / limits

- Single host, single packer build (upx 5.2.0); tamper points chosen
  structurally (section table, PackHeader), not fuzzed exhaustively.
- Forged-c_adler (payload corrupted AND c_adler repatched) is out of the
  candidate's reach by design (docstring; u_adler needs the codec) and was
  not probed beyond the item's case list.
