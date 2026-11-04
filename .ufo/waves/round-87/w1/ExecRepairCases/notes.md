# ExecRepairCases — round 87 (kaidoku), seat notes

Axes: coverage (more packing modes repaired), depth (structural edge cases pinned in the selftest), calibration (false-accept rate on plain ELFs).

## Candidate
- Path: `.ufo/waves/round-87/w1/ExecRepairCases/candidate/upx-magic-repair.py`, sha256 `c2083af51712080e4bf196300aef576df14a0e9537e8bd9fb9ec7f3ed0e4fdca`.
- Base: `tools/round-87/upx-magic-repair.py` @ b5c7a49e (sha256 `f4ebd152…c49723`). Production file unchanged.
- Full diff: `receipts/candidate.diff`.

### Production-logic change (minimal, named): "mixed-method chain"
Out-of-population probe finding: on `libz.so.1.3.2` packed with `upx --lzma` or `upx --best --brute`, the base tool refused with `b_info chain does not reach an end-of-chain sentinel`. The program chain starts with an NRV2B block (method 2: `blk 9304 (680, 201, 2, …)`) followed by LZMA blocks (method 14: `blk 9517 (63157, 30483, 14, 73, 6, 0)`). The PackHeader method is 14. `walk_chain` required every block to use the first block's method, and the resume scan did the same. The after-loader chain (method 14, `cand 58716 -> sentinel 59360`) was therefore never accepted.

Fix: a block's method may be the first block's method **or the PackHeader's method**. Changed lines in the candidate:
- L70: `find_packheader` also returns `"method": h[6]`.
- L75-81: `walk_chain(..., alt=None)` signature and docstring.
- L92: `elif meth != method and meth != alt:` (was `meth != method`).
- L109-116: `find_sentinel(..., ph_method=None)` signature and docstring; the first walk passes `ph_method`.
- L123-124: resume candidates accept `d[s + 8] in (method, ph_method)` (was `== method`).
- L126: the resumed walk passes `ph_method`.
- L143: `find_linfo` passes `ph["method"]`.

Nothing else changed. No new search window, no new anchor, and the write rule is the same.

### Selftest (non-logic)
`check` now counts cases, so the printed `cases=` is computed instead of hard-coded `9`. The 9 existing cases are kept. Added cases:

| case | expectation |
|---|---|
| mixed-per-anchor | l_info=`KDK!`, b_info_end=`00000000`, packheader=`ffffffff`; restored == clean; each `was` recorded |
| single-packheader / single-b_info_end / single-l_info | each anchor tampered alone (`KDK!`, zero, `a55aa55a`) → only that anchor restored, at the expected offset |
| truncated-every-cut-refused | every prefix `[:n]`, `n < len-4`, of the clean and T1 fixtures → Refused |
| truncated-pad-only-repairs | T1 fixture minus its 4 trailing pad bytes → repaired to `clean[:-4]` |
| refuses-spliced-block-{clean,t1,foreign} | 4 bytes cut out of a compressed block, header unchanged → Refused |
| chance-window-validates | sanity: the planted tail window does validate as a PackHeader |
| refuses-chance-window-no-linfo | plain ELF + checksum-valid tail window, no p_filesize match → Refused |
| refuses-chance-window-linfo-version-mismatch | p_filesize present, l_version/l_format wrong → Refused |
| refuses-chance-window-linfo-no-chain | matching l_info/p_info + implausible b_info (sz_cpr > sz_unc) → Refused |
| refuses-chance-window-linfo-chain-no-sentinel | matching l_info + 1 plausible block, chain runs off → Refused |
| refuses-overflow-first / overflow-second | sz_unc=0xFFFFFFFF, sz_cpr=0xFFFFFFF0 → Refused |
| refuses-szcpr-gt-szunc | first block sz_cpr > sz_unc → Refused |
| refuses-zero-advance | first block sz_cpr = 0 (no-progress) → Refused |
| resume-past-loader | 16 junk bytes between chains → resume at the shifted block, all 3 anchors restored |
| payload-magic-untouched | `UPX!` inside a compressed block stays as-is, only the 3 anchors are rewritten |
| refuses-ph-only / refuses-elf-header-plus-ph-only | a bare PackHeader, or an ELF header + PackHeader → Refused |
| mixed-method-chain | method 2 first block + method 14 (= PackHeader method) → repaired |
| refuses-foreign-method-chain | method 2 then method 7 (neither) → Refused |

Chain loop: a cycle is structurally impossible, because `q` grows by ≥ 13 every step and the walk is capped by `MAX_BLOCKS`. The zero-advance and overflow cases pin the cases where a naive walker would stall or overrun.

Output (`receipts/selftest.txt`): `SELFTEST cases=33 failures=0`

## Frozen counter, no REA (`counter-norea.json`)
Command:
`python3 -I -B tools/round-87/upx-tamper-battery.py --root <lane> --repair-cmd <candidate> --work /fast/scratch/hyaku/kaidoku-r87/ExecRepairCases/work/counter --no-rea --json-out .../counter-norea.json`
- counter sha256 `0f2d2bd8…5384b0`; repair_sha256 `c2083af5…e4fdca`; upx 5.2.0 sha256 `cf2f6e7c…c969`.
- In all 8 cases, repair_rc0, windows_only, test_ok and identity are true. The only false arm is `rea_recover`, which is false by construction (`REA disabled (--no-rea)`), so the label reads `recovered 0 of 8` and `met=False`. That is expected under `--no-rea`.
- controls_ok: N1 true (4/4 rc 2), N2 true (repair rc 0 on all 4 but never recovered), N3 true (4/4 byte-identical).
- The same run on the selftest-only candidate (repair sha `9ae811ac…`, before the method fix) gave identical arms: `receipts/counter-norea-selftest-only.json`. The fix does not move the in-population result.

## Out-of-population probe (report only, not a claim)
Script: `receipts/probe.py`. For each carrier, a scratch copy is packed with `upx <mode> -q`, tampered by global `UPX!`→value replacement (T1 zero, T2 `KDK!`), repaired with the candidate, then checked with `upx -t`, with `upx -d` sha256 identity against the pin, and by running the executable (`--version`/`-v`) and comparing its rc and output hash with the original. `--best --brute` packed in ≤ 3.8 s, so no mode was skipped. All tampered inputs fail `upx -t` before repair (rc 2). Full rows with sha256s: `receipts/probe-after-fix.json`.

| carrier | mode | tamper | magic offsets | unrestored | repair rc | windows-only | upx -t | identity | runs like orig |
|---|---|---|---|---|---|---|---|---|---|
| jq | --best | T1/T2 | 556, 10971, 13992, 14000 | 10971 | 0 | ✓ | 0 | ✓ | ✓ |
| jq | -1 | T1/T2 | 556, 11611, 14745, 14756 | 11611 | 0 | ✓ | 0 | ✓ | ✓ |
| jq | --lzma | T1/T2 | 556, 13953, 13964 | – | 0 | ✓ | 0 | ✓ | ✓ |
| jq | --best --brute | T1/T2 | 556, 13953, 13964 | – | 0 | ✓ | 0 | ✓ | ✓ |
| xxd | --best | T1/T2 | 556, 16499, 19513, 19524 | 16499 | 0 | ✓ | 0 | ✓ | ✓ |
| xxd | -1 | T1/T2 | 556, 17491, 20616, 20624 | 17491 | 0 | ✓ | 0 | ✓ | ✓ |
| xxd | --lzma | T1/T2 | 556, 19330, 19340 | – | 0 | ✓ | 0 | ✓ | ✓ |
| xxd | --best --brute | T1/T2 | 556, 19330, 19340 | – | 0 | ✓ | 0 | ✓ | ✓ |
| libz | --best | T1/T2 | 9284, 63721, 65544 | – | 0 | ✓ | 0 | ✓ | n/a (.so) |
| libz | -1 | T1/T2 | 9284, 66813, 69640 | – | 0 | ✓ | 0 | ✓ | n/a |
| libz | --lzma | T1/T2 | 9284, 59364, 61448 | – | 0 (base tool: **2, refused**) | ✓ | 0 | ✓ | n/a |
| libz | --best --brute | T1/T2 | 9284, 59364, 61448 | – | 0 (base tool: **2, refused**) | ✓ | 0 | ✓ | n/a |
| dinit | --best | T1/T2 | 556, 357738, 357748 | – | 0 | ✓ | 0 | ✓ | ✓ |
| dinit | -1 | T1/T2 | 556, 395747, 400282, 400292 | 395747 | 0 | ✓ | 0 | ✓ | ✓ |
| dinit | --lzma | T1/T2 | 556, 300629, 300640 | – | 0 | ✓ | 0 | ✓ | ✓ |
| dinit | --best --brute | T1/T2 | 556, 300629, 300640 | – | 0 | ✓ | 0 | ✓ | ✓ |

Candidate: 32/32 rows pass test and identity. Base tool b5c7a49e: 28/32, with libz `--lzma` and `--best --brute` refused on both tampers (`receipts/probe-before-fix.jsonl`). In that before-run the xxd rows failed to pack because `/usr/bin/xxd` is a symlink to `/usr/bin/tinyxxd` and upx skips symlinks. That was a probe harness artifact, fixed by copying the carrier into scratch first, and not a tool result.

## Findings (report only; frozen files untouched)
1. **Coverage gap (fixed in candidate):** an LZMA-packed shared object has a mixed-method b_info chain. The base tool refuses it. `upx --best --brute` selects LZMA for libz, so the gap shows up even with a `--best`-family flag.
2. **Fourth `UPX!` word not restored, in the population too:** jq and xxd `--best` (in the frozen population) carry 4 magic words. The 4th (jq 10971, xxd 16499; odd offsets) lies between the first-chain stop and the resume offset, which is inside the embedded loader. The repair leaves it tampered, so `repaired_equals_packed` is false for jq/xxd in the counter. `upx -t`, `upx -d` identity and execution are unaffected. The frozen arms do not require byte-identity with the packed file. [INFERENCE] the loader does not consult that word.
3. **Execution is not a discriminator:** the *tampered* (unrepaired) executables already run identically to the originals. The tamper only defeats `upx -t/-d`, not the program.
4. **N2 is carried by upx, not by the repair:** the repair returns rc 0 on all 4 corrupt-payload inputs, because it is structural only. The control passes because `upx -t/-d` rejects the flipped byte.
5. **Calibration:** across 5369 plain ELFs in /usr/bin and /usr/lib, 10 have a tail window that passes the PackHeader checksum by chance (e.g. pg_dump, rpcinfo, libmujs.so), but 0 are accepted by `repair` (`receipts/plainscan-after-fix.json`; same before the fix). The l_info/chain cross-check is what carries N1.

## Tools installed
None.

## Scratch
`/fast/scratch/hyaku/kaidoku-r87/ExecRepairCases/` was removed before the yield. No packed or tampered binaries were committed or copied; they are cited by sha256 in `receipts/probe-after-fix.json`.
