# R28-C1 h09 miss cause reproduction (seat ExecH09Probe)

UTC window: 2026-10-22T18:23:43Z to 2026-10-22T18:28:36Z. Lane: /home/vgpnk/Projects/shokunin/kaidoku-shokunin (read-only; only this report written).

## Files changed

Only this report: /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-28/a2w/ExecH09Probe.md. No lane file was edited, no git write, no commit, no index change. All scratch work is under /fast/scratch/hyaku/kaidoku-r28/seats/a2w/ExecH09Probe/.

## Carrier and placeholder inventory

Carrier h09 runtime: `.ufo/waves/arc3-loop1-round3/claims/c1/CR-1/out/Cr1LibUser.noopt.runtime.hex`, 1149 bytes, sha256 `f9dc4ccf369a7595bcc1344371737a771ced7922f129d5ae2db0b8b5287c6c68` (matches `runtime_sha256` in `corpus/evidence/round-28/c1/carriers.tsv:10`).

- Placeholder count: 1.
- Token: `__$a2bad93077572174e8e5044433a5a7d5f3$__`, exactly 40 characters (`__$` + 34 hex + `$__`).
- Text offsets in the file: characters 194 to 233 inclusive (end exclusive 234), the only placeholder in the file.
- Decoded-runtime offsets: the placeholder occupies bytes 97 to 116 (20 bytes) of the 574-byte runtime, and it is the operand of the `PUSH20` opcode `0x73` at byte 96.
- Byte census of the whole file: 1149 bytes, of which 1142 are hex digits, 1 is the trailing newline, and exactly 6 are non-hex, all inside this placeholder: four `_` and two `$` at character offsets 194, 195, 196, 231, 232, 233. No spaces, tabs or carriage returns. So the placeholder container is the only reason the file is not valid hexadecimal.
- Census of all 61 carriers: h09 is the only carrier with a `__$...$__` placeholder and the only one whose non-hex characters are not the `0x` prefix. 31 carriers carry exactly one non-hex character, the `x` of a leading `0x` that REA's own error message lists as allowed, and 29 are pure hex. Only h09 has interior non-hex characters, and it is the only carrier with a placeholder.

## Both REA runs (observations)

Command form: `TMPDIR=<seat>/tmp npx -y rea-agents@6.5.0 inspect-evm-interface <file> hex --format json`, package 6.5.0 at /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/.

Run 1, original file, 2026-10-22T18:24:00Z to 18:24:01Z, exit 1. stdout was a REA error document, stderr was empty (sha256 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855). Error text, verbatim from the JSON:

```
{"code":"invalid_request","category":"invalid_input","message":"Analysis input is invalid. Check the arguments and try again.","retryable":true,...,"details":{"operation":"inspect_evm_interface","issues":[{"path":["path"],"reason":"invalid_format","message":"Hex carrier requires complete hexadecimal byte pairs, an optional 0x prefix and outer ASCII whitespace; interior separators are invalid."}],"captured_output":{"stdout":"","stderr":"","truncated":false}}}
```

This output is byte-identical to the committed envelope `corpus/evidence/round-28/c1/envelopes/h09.json` at lane commit a2673116 (both sha256 `640322f6abc1afc02d38af445765b16f52b84c702af55af91e9d2926e45f4764`, `cmp` reports no difference). The reproduction therefore re-derives the recorded refusal exactly.

Run 2, linked copy, 2026-10-22T18:24:11Z to 18:24:12Z, exit 0. stderr empty. The linked copy is byte-for-byte the original except that the 40-character placeholder is replaced by 40 zeros; the file length is unchanged at 1149 bytes, all other characters are identical, sha256 `1897b1f26e9a05774f87a1d02c273423b0ebc1676c56bc714736addda87ae91d`.

Recovered selector list for the linked copy (exactly one entry, from `normalized_result.functions`):

```
[{"selector":"0x395c1d44","bytecode_offset":45,"dispatch":"abi","inferred_arguments":"uint256","inferred_state_mutability":"nonpayable"}]
```

Provider `evmole@0.9.3`, operation `inspect_evm_interface`, subject digest `1897b1f2...`, decoded bytecode 574 bytes, terminal CBOR metadata decoded with solc release bytes `0.8.37`.

## Held-out selector 395c1d44

Recovered: yes. The linked copy recovers `395c1d44` as its only function, with dispatch `abi`, inferred arguments `uint256` and inferred mutability `nonpayable`. `heldout.tsv` row `395c1d44  useIt(uint256)  h09` is the single held-out selector on carrier h09, so the linked copy recovers 1 of 1 h09 held-out selectors.

Independent confirmation, computed with a pure-Python Keccak-256 written in the seat: `keccak256("useIt(uint256)")` = `395c1d448715f4789f8c510310d3eee2ebd55d86cb9709f350007bbeb9ef39ea`, so the first four hex digits are `395c1d44`, matching `heldout.tsv`. The same implementation reproduces the known vectors `keccak256("")` = `c5d2460186f7233c...` and `keccak256("transfer(address,uint256)")` = `a9059cbb...`, so it is not a self-fulfilling check.

Byte-layout check, computed by decoding the linked runtime: the `PUSH4 395c1d44` opcode sits at byte 31 with the selector bytes at 32 to 35, the compare and `JUMPI` follow, and the jump target 0x2d = 45 is a `0x5b` JUMPDEST. That matches REA's reported `bytecode_offset` 45, which is therefore the function body entry, not the selector constant position.

## Control run isolating the cause

A third run replaced the placeholder with a real 40-character hex address `de0b295669a9fd93d5f28d9ec85e40f4cb697bae` instead of zeros (2026-10-22T18:25:15Z to 18:25:16Z, exit 0, sha256 `c2cc11a4512464f361d3b40793769a1d4a8d5c0db659a687a004081a1992d21b`). It recovered the same single selector `395c1d44`. Conclusion, labelled inference: the refusal is caused by the non-hex placeholder text itself, not by the unresolved library link as such, and not by the zero address. Replacing the placeholder with any well-formed hex restores a clean inspection.

## Findings, labelled

- Observation: the cause of the h09 exit 1 is REA's hex-carrier format check rejecting the 6 non-hex characters of the unlinked-library placeholder, reported as `reason: "invalid_format"`.
- Observation: with the placeholder neutralised, REA recovers `395c1d44` from the h09 runtime, the one held-out selector on that carrier, so the h09 row failure is a carrier-format problem and not a selector-recovery problem.
- Observation: the committed tally at a2673116 shows `recovered_by_rea: false` and null rule outputs for row 395c1d44, and the committed 4byte and openchain lookups for 395c1d44 both contain no name (4byte returns `{"count":0,...}`, openchain returns `{"0x395c1d44":null}`). Even with a repaired carrier this row would produce no database name, so it would stay in the "no name" group of the primary rule rather than becoming a wrong name.
- Observation: the runtime also contains `PUSH4 3cf3bbf4` at byte 117. That value is `keccak256("twice(uint256)")[0:4]`, the selector of the library function that the contract delegate-calls. It is not a dispatch selector of the carrier, and REA correctly does not report it as one.
- Inference: if the carrier file were replaced in the lane by a hex-clean copy, the counter would still record the run as invalid, because `check_runs` compares the envelope subject digest and local path against the pinned `runtime_sha256` and the frozen argv path in `corpus/evidence/round-28/c1/carriers.tsv`. Any such repair must therefore change the frozen carrier list and re-freeze, which is outside this seat's scope and outside the claim's frozen data.

## Risks

- The frozen target for R28-C1 stays unreachable on the frozen data. runs_ok stays 60 of 61 and rows_complete stays 186 of 187 unless the L1 re-freezes the carrier list with a hex-clean h09 runtime and re-runs the counter. This seat's evidence does not make the frozen target met and must not be counted as data.
- A tempting wrong move is to swap in the linked copy silently. That would change the carrier file the counter pins by sha256 and path, so the run record would fail the counter's own checks. Report the miss rather than patch it.
- The linked copy is scratch evidence about tooling behaviour only. It is not a substitute carrier and must not enter `corpus/evidence/`.

## Blockers

None for this assignment. The L1 decision on whether to re-freeze carriers with a hex-clean h09 runtime is outside this seat.

## Artifacts (all under /fast/scratch/hyaku/kaidoku-r28/seats/a2w/ExecH09Probe/)

- placeholders.py — placeholder counter and linker: 82331e934f44e895d47ec247650c31335767dfa910676734d2f28779b729b70b
- scratch/placeholders.json — count and offsets report: 099be28ad6626916ad748454cfce4d5718dcbe22ec6c0039e19e4b5bfc753dda
- scratch/Cr1LibUser.noopt.linked.runtime.hex — 40 zeros in place of the placeholder: 1897b1f26e9a05774f87a1d02c273423b0ebc1676c56bc714736addda87ae91d
- scratch/Cr1LibUser.noopt.hexaddr.runtime.hex — control copy with a real hex address: c2cc11a4512464f361d3b40793769a1d4a8d5c0db659a687a004081a1992d21b
- scratch/orig.json — REA output for the original file, exit 1: 640322f6abc1afc02d38af445765b16f52b84c702af55af91e9d2926e45f4764
- scratch/linked.json — REA output for the linked copy, exit 0: db913986801e9ef6c51abe0703cdcbfd23d47259f24ddc5bee893afe9ba09a0e
- scratch/ctrl.json — REA output for the control copy, exit 0: 076ae915abdd3541bf92d36f90aaa1da641cea2339c6a1a94572933817232bca
- scratch/h09_committed.json — committed envelope pulled read-only from a2673116, byte-identical to scratch/orig.json: 640322f6abc1afc02d38af445765b16f52b84c702af55af91e9d2926e45f4764
- scratch/orig.stderr, scratch/linked.stderr, scratch/ctrl.stderr, scratch/placeholders.stderr — empty: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

Tooling: no install, no upgrade, no network fetch. Only the host python3, git and the already-cached npx package rea-agents 6.5.0 were used. No request was made to 4byte.directory or api.openchain.xyz.

Report: .ufo/waves/round-28/a2w/ExecH09Probe.md
