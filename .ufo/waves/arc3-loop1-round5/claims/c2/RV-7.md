# RV-7 — C2 arc3 corpus audit

Scope is frozen at `claims-frozen.md:38-52`: the arc3 EVM entries, their errata, selector counts, SHA-256 identities, dispatch/byte-count claims, and the no-Core disclaimers. All REA probes below were fresh `rea-agents@6.4.0` invocations; scratch used `/var/tmp/rv7-*`. Byte counts and code locations were independently recomputed from the retained byte carriers, not copied from another seat's report.

## Verdict ledger

| Claim group | Verdict | Re-derivation / evidence |
|---|---|---|
| R1 real-solc counts, hashes, sizes | **VERIFIED** | Freshly re-probed Rv2Token 5, Rv2Many 11, KdxToken 6; see outputs below. Rv2Token's returned set matches `expected-selectors.txt`. |
| R1 creation/PUSH4 correction | **VERIFIED** | Direct byte scan confirms 1,971-byte initcode embeds the 1,943-byte runtime; five EQ/PUSH2/JUMPI patterns; runtime code ends at 1,890 and `16ee4b79` is at byte 1,901 in the trailer. |
| R3 selector counts, sizes, hashes, optimizer deltas | **VERIFIED** | Freshly re-probed the named primary carriers and the five additional matrix carriers; all reported counts and bytes match the entries. The VaultB opt200 returned set matches the entry's set. |
| R3 dispatch/PUSH4 and creation-byte errata | **VERIFIED** | Raw VaultB bytecode has the recorded GT/EQ split and JUMPDEST offsets; raw creation carriers independently yield the 7/9/10/11/13 EQ-site counts. |
| R4 counts, identities, sizes, dispatch/offset and inference claims | **VERIFIED** | Fresh REA runs and byte/ABI checks reproduced the counts, hashes, Vyper table/XOR shape, offset rule, 7/15 mutability agreement and 3 address-argument mismatches. |
| Ghidra 34-feature correction | **VERIFIED** | Installed directory and candidate list both enumerate exactly 34 names; `40de383` changes PROVINCE's count and appends the erratum. |
| No-Core status | **CORRECTED — parent action** | Entry disclaimers conflict with `PROVINCE.md:91-93`, which calls arc3-r1/r3/r4 carriers Core. See exact wording below; RV-7 did not edit PROVINCE or corpus. |
| Corpus inventory / claimed fourth standalone arc3-r entry | **UNVERIFIABLE** | `corpus/knowledge/2026-10-19-arc3-r*.md` currently returns only r1, r3 and r4; a search for an r2 entry returns no match. No fourth standalone arc3-r file was available to audit. |
| Secondary matrix set-equality and path-sensitive `ev_` domain claims | **UNVERIFIABLE** | This seat freshly re-ran the secondary carrier counts, but did not independently rederive every secondary ABI set, cross-pin leg or path-variant identity. These are not silently counted as verified. |

## Fresh command results

All listed CLI summaries are from this seat's live `npx -y rea-agents@6.4.0 inspect-evm-interface <path> hex --format json` invocations (or the indicated per-file path), with a disk-backed `TMPDIR`. Each summary shows decoded bytecode SHA/size and input-carrier SHA/size; `functions` counts the returned function array.

**R1** — source entry `corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md:12-25`:

```text
Rv2Token: id=ev_45849c8b11794ea0b007bd01ea3241aa9b385ca7543e514a16e82c795a106eaf; functions=5, dispatch={'abi': 5}; selectors=095ea7b3,18160ddd,23b872dd,70a08231,a9059cbb; decoded=1943 B c1081a565869b50387211b25afaf3768294aa774c35845bc3a8c0b12cfe15e74; carrier=3886 B d7f73058e2d9fb2563bf96b2f26902f233530de027a7943185e15bfdc4e1048f
Rv2Many: functions=11, all dispatch=abi; decoded=1288 B 04930d00ac26c1e523e910e6d04c5427e0d2b59de33e5a6eeb238eff58c019f4; carrier=2576 B 6a1c07d7090bba7bd01238a27e433ec308fc756a0cdbd4504674dd2c15adbcd1
KdxToken: functions=6, all dispatch=abi; decoded=1789 B 9c40940ef88c0e82349af0b0bebb31fabf0b71bf68f5117478ac07d7e44e580e; carrier=3579 B 69a15782678dccdd4d43b2f0af566c2f030fe9dee4de4ef8365bc4b6d1b29ad6
Smoke_sol_Smoke.bin (hex creation input): functions=0; decoded=685 B 08299f31203e05e5dcdcd2453f9dd5a105a97fd94f2b48194ba18e963c368ebd; carrier text=1370 B 530efc7bb166fd47e42fe9623ee347234b99a65691b0a0ad42d2682702986a5f
Rv2Token.creation.hex: functions=0; decoded=1971 B 04e07f54512cca4ac5350d5f3f2701ec8d9b125e69a5d28c79c8526352c7786b; carrier=3942 B e6517fb7db569cadfd8a586cdb5f2f838c6bb4a1b5b941640bf72f30df07400d
```

The matching byte sources are under `.ufo/waves/arc3-loop1-round1/claims/c1/RV-2/` (`Rv2Token.runtime.{bin,hex}`, `Rv2Token.creation.hex`, `expected-selectors.txt`, `probe-runtime-hex-6.4.0.json`, `attack/Rv2Many.runtime.hex`, `attack/probe-many.json`) and `EX-07/target-KdxToken.runtime.hex`; the Smoke source is `EX-02/smoke/out/Smoke_sol_Smoke.bin`.

Independent raw-byte pass on `RV-2/Rv2Token.runtime.bin` / `Rv2Token.creation.hex`:

```text
raw runtime == decoded hex: True; bytes=1943; SHA256=c1081a565869b50387211b25afaf3768294aa774c35845bc3a8c0b12cfe15e74
code_end=1890; CBOR length=51; PUSH4 opcode immediates in code=5 (exactly the five selectors above)
16ee4b79 first byte offset=1901; present in code region=False
fresh REA offsets=89,137,167,215,263; offsets at 0x5b=5/5
creation bytes=1971; embedded runtime offset=28; runtime embedded=True; raw EQ/PUSH2/JUMPI sites=5/5
```

This independently reproduces the append-only correction at r1 entry line 31: the earlier “no runtime dispatch table” creation wording and the whole-file `16ee4b79` PUSH4 reading are corrected. For the five stated r3 creation counts, a raw-byte scan of retained creation carriers found: `EX-12/VaultA.creation.hex` 7 sites; `EX-02/evidence/carrierA.creation.hex` 9; `SC-1/out/VaultCourt.opt0.creation.bin` 10; `EX-05/recompiled/noopt/VaultB.creation.hex` 11; `EX-10/out/VaultB.opt200.creation.bin` 13. Each site matched `PUSH4 selector; EQ; PUSH2; JUMPI`; these counts are byte-level presence, not proof initcode executes those embedded runtime bytes.

**R3** — source entry `corpus/knowledge/2026-10-19-arc3-r3-evm-optimizer-shapes.md:12-35`:

```text
VaultB opt200: 13 functions; runtime=1621 B b24a01153af943ff8ebf26a678a3bfc0b1d70e1fc563d17b05c7cc064ae340b6; carrier=3242 B 9a1fbfaba9e3a89c1ce8bc12291c305500beef48a73ee270e6116cd5febb1d88
VaultB nopt: 13; runtime=3163 B bcdf64abcda096e3cb7ea25d552d597a1c0f93303a66340cd270e23aaa7f77fa; carrier=6326 B 09223b238da6950692d4ab336eaca6818f5359f6a2c3bd84d98706bf0fd2651d
carrierB EX-04 opt200: 11; runtime=1850 B aaf85ceaf124bac2d3a32428927194158c9211e4472a0cf06f88a721cf239412; carrier=3701 B 7dc26d4db0fa8cde1d2f833ce968c9fbca1df18366dd15d3c8bc36c603fa424d
carrierB EX-04 noopt: 11; runtime=3872 B 679678e9a67aee701094a4bfeafd2a02311460658aa4b400202340b47d83d005; carrier=7745 B 54b8c90686aaa4ba1375830d1b87277f9c523422f5a9d11ec4708ce866f53ca8
CarrierB EX-05: 8; runtime=1469 B b9c70178069601ba766a49359981118032085b8af74861659a9edc064ebd7940; carrier=2939 B 247e09f3650aab9010b72b21c68af874b08dbc8d16bab54032d0c4a0017149cd
CarrierBErr: 8; runtime=1253 B 9715b824f9af9e1a9796c8e5b96d5fe006e5d323c7284622ddcc5d5200382eb8; carrier=2507 B 97b5333c48a1ebe50282bf57165ad0d7ba643c89f3de750ae58cd364b815fd4e
Rv2TokenOpt: 5; runtime=978 B ed6c8a76d05b230e7187325bd5165f19c118285bbd7c4a6d3d88f13018bfc2d3; carrier=1957 B a07bef2e79803a33a98d361c9e118616c90ce6ff69166c098386cf10ae7b06c1
Additional matrix fresh counts: CarrierA=9, EX-04 vaultB=11 (same opt200 file above), OptVault=5, MutMix=6, MutMixOpt=6.
```

Fresh VaultB opt200 returned sorted selectors `24a9d853,27e235e3,2e1a7d4d,3d96e276,3f4ba83a,5c975abb,69fe0e2d,7d882097,8456cb59,8da5cb5b,9c421eb5,cbf9fe5f,d0e30db0`; it matches the corpus set. Independent parse of `EX-10/out/VaultB.opt200.runtime.bin` found decoded hex identical, 1,621 B, code end 1,568 / CBOR 51; in the dispatcher prefix (`pc < 0xd6`) there are 13 EQ, 2 GT, 15 PUSH4 and 17 JUMPI opcodes. Fresh recheck returned offsets `239,279,322,353,384,404,445,476,497,517,571,602,645`, all 13 bytes are `0x5b` JUMPDESTs.

For the PUSH4 correction at r3 entry line 26: direct opcode decoding of VaultB opt200’s code region yields 24 PUSH4 sites: 15 selector occurrences (13 unique, with `69fe0e2d` and `8da5cb5b` duplicated) plus non-selector error/panic immediates. On Rv2TokenOpt, its 925-byte code region has six PUSH4 sites (five selectors plus `4e487b71` panic); the terminal CBOR data follows the code region. The other optimizer matrix counts reproduce, but their complete ABI-set equality / extra-immediate checks and cross-path `ev_` claims were not rederived by RV-7 (UNVERIFIABLE as noted above).

**R4** — source entry `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:12-30`:

```text
CarrierV (fresh id ev_d1792f577ae3611615fd8dbcb1ce2e71dae4e0346b66d72b41321f4644df963f): 15 / all dispatch=abi; runtime=1562 B 57d6fd0ae0da001975a3f58ae72804757aa36267f6e373bf9f134ecc9791dae0; hex carrier=3124 B e0b1021c68f8de8c3f049f4242769548b6f8271a00986f2ab20f049f8748a192
Ex09Vault: 7; runtime=581 B 54b14e306bbaf7614d062c06522e88327177aba576309905008e63a90ad199ee; carrier=1165 B 05a2953657736eac3ea4fc53023942e917f24f7128dfac249ddc201c349792e4
StewardToken: 22; runtime=3337 B 1846469bd2abc625ecf69567af16153f791fd6856e3c7acf32c2bf6f80967c51; carrier=6677 B cf13c82fb5b0bc73c7c27f1b2217997edda028c6f13b5ee577b9de09ae10b1eb
CarrierW: 9; runtime=829 B 67d1d88fc65824acbe75b9f7304bdaf1f122f7173b97b284d3e9f53687115858; carrier=1661 B 406e45ea3c8ab495b18e32ab9933df81ad2fc4588f78e24079ef70209cd24214
Smoke: 4; runtime=168 B 415e6b1b172a21c51a0379642acbadefcb6238c61a29d8187a1d4a8c22eecbfb; carrier=339 B 40650adfa7c94b4f7fd11a0b0558fd8f19f278ed9414c54397cd1112892bcc23
CarrierV creation: zero functions, decoded=1637 B SHA256=3c6673966d821d9d3366283ab2501c4e32167798ae89d92a21143f560994a226; hex carrier=3274 B SHA256=34f52280d3cdc74008e1a2265f367f1d0817d93df6bbbb5cdce243903c3ccd92
```

CarrierV’s fresh selector set equals the 15 function selectors in `EX-04/out/method-identifiers.json` (not its `__default__()` key). Raw `out/runtime.bin` equals decoded hex. Byte-level results: prologue/table prefix `5f3560e01c6002600d820660011b61060001601e395f5156`; 13 table words at offset `0x600`, sentinel `0x5e7` appears 3 times (empty buckets 1/7/11), other 10 words point at JUMPDESTs. The 15 selector buckets modulo 13 occupy 10 buckets (4 buckets have collisions). Parsing each current REA offset against the raw bytes gives `push4_pc + 11` on 15/15, `0x5b` at reported offset on 0/15, and compare-site JUMPDEST at offset−12 on 15/15. Among 21 PUSH4 opcode sites before the table, the only non-selector immediate is `08c379a0` at six sites.

A fresh comparison of probe results to the compiled `EX-04/out/abi.json` and method identifiers gave ABI functions=15, method-id keys=16, probe functions=15, unmapped selectors=[]; mutability matches=7/15, with payable overreads for ABI view=5, nonpayable=2, pure=1; argument tuple mismatches=3/15 and those are selectors `0776076f`, `27e235e3`, `b144adfb` (each ABI `address`, inferred `uint256`). `89402a72` is absent from the runtime. This reproduces the scope-qualified inference limitations at r4 entry lines 23-24.

## Discrepancies and limits for the parent

1. **CORRECTED (parent disposition required):** all three arc3 knowledge entries say “RESULT-class, no Core promotion” (`r1:1,33`; `r3:1,35`; `r4:1,30`), but the current PROVINCE frontier says “real solc-0.8.37 carriers (Core, arc3-r1/r3) and a vyper-0.4.3 carrier (arc3-r4)” (`PROVINCE.md:91-93`). These statements conflict. Please adjudicate the status and correct the relevant corpus/PROVINCE record; RV-7 did not write either tracked file.
2. **UNVERIFIABLE (inventory pointer missing):** the direct glob of `corpus/knowledge/2026-10-19-arc3-r*.md` returned only r1/r3/r4; grep for `2026-10-19-arc3-r2` returned no matches. The separate Ghidra erratum is in `corpus/knowledge/2026-10-13-ghidra-install.md:71-76`; if it is the intended fourth audit target, it is not an arc3-r entry. The frozen “four arc3 entries” wording needs a pointer or clarification.
3. **VERIFIED:** the Ghidra correction says 34, not 35, at `corpus/knowledge/2026-10-13-ghidra-install.md:66-76`; direct filesystem enumeration returned 34 Features directories, with the listed set equal after punctuation normalization. `PROVINCE.md:46` now says 34. `git show 40de383 -- PROVINCE.md corpus/knowledge/2026-10-13-ghidra-install.md` shows the 35→34 PROVINCE repair and appended erratum in the same work commit.
4. **UNVERIFIABLE:** this seat did not repeat every 6.4/6.7 cross-pin leg, all path-variant evidence IDs, or every secondary-carrier ABI set. Fresh counts, hashes, and bytecode facts are reported above; no stored peer matrix or prior-round number is treated as first-hand evidence.
