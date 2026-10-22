# Round 26 wave 2: EntryCorrectionReview (falsify seat)

Seat: KaidokuR26.EntryCorrectionReview, leaf reviewer, 2026-10-22, run 12:59:45Z to 13:05Z UTC.
Target: the round-26 correction section (entry lines 177-205) appended to
`corpus/knowledge/2026-10-22-r25-evm-selector-name-resolution.md`.
Judged commit: lane HEAD `fe3eb4edf410244eff46151a148c8f754be1ce80`. The correction landed at `c327772653`.
Entry bytes: working file, HEAD blob and c327772653 blob share sha256
`066500c637c9715098becda0a58c4fc7768da8e2152cf0c45db4205dba438c63` (`sha256sum` and `git show | sha256sum`, 13:02:42Z, exit 0).
Evidence unchanged since the correction: `git diff --quiet c327772653 HEAD -- corpus/evidence/round-25 <entry>` exit 0 (13:02:42Z); the same for the six ABI paths in `carriers.tsv` exit 0 (13:03Z).
Bounds: lane read-only. All runs used the sandbox clone `/fast/scratch/hyaku/kaidoku-r26/seats/w2/EntryCorrectionReview/clone`. No REA call, no web source, no tool install, no lane git or jj write, no subagent.

## Verdict per number

| Number | Where the entry states it | Verdict | My re-derivation |
|---|---|---|---|
| 69 carrier-selector rows | lines 50, 183, 194 | HOLDS | 69 |
| 43 distinct selectors | lines 51, 184, 195 | HOLDS | 43 |
| 138 saved responses | lines 41, 194 | HOLDS | 138 |
| 16 shared selectors | line 195 | HOLDS | 16 (6 on two carriers, 10 on three) |
| Three-carrier maximum | line 205 | HOLDS | 3; none on four or more |
| "138 files hold 43 distinct 4byte bodies" | lines 196-197 | FAILS | 35 |
| "43 distinct openchain bodies" | lines 196-197 | HOLDS | 43 |
| "shared ERC-20 selectors" | line 51, not changed by the correction | FAILS as a description | 5 of the 16 are ERC-20 standard functions |

## Evidence per number [observation unless marked]

- **69.** The correction's own command `find corpus/evidence/round-25/a2/c2 -path '*/db/4byte-*.json' | wc -l` printed `69`, exit 0, 13:02:42Z. Three other routes agree. REA normalized rows per carrier are 5, 6, 13, 8, 22, 15 (sum 69; raw equals normalized; no in-carrier duplicate; `derive-clone.out`, exit 0, 13:04:03Z). The compiler ABI keccak-256 selector set of each carrier equals its REA set, with 5, 6, 13, 8, 22, 15 functions. `tally.json` `per_carrier_rows.selector_rows` is 69.
- **43.** The correction's sed-plus-`sort -u` command printed `43`, exit 0, 13:02:42Z. REA union 43 equals ABI union 43. The 43 openchain filenames give the same set, and `a3/c2/filter-true/manifest.json` has 43 entries with the same selectors. `tally.json` `distinct_selectors.selector_rows` is 43.
- **138.** `find corpus/evidence/round-25/a2/c2 -path '*/db/*' -name '*.json' ! -name 'manifest.json' | wc -l` printed `138`, exit 0, 13:02:42Z. Manifest entries are 10+12+26+16+44+30 = 138. Every file's sha256 equals its manifest value and every status is 200 (0 bad). Two times 69 is 138.
- **16 shared.** Carriers per selector: `{1: 27, 2: 6, 3: 10}`. Sum of (count minus 1) is 26, which equals 69 minus 43. For all 16 shared selectors the 4byte manifest sha256 is identical across carriers (16 of 16), and the openchain sha256 likewise (16 of 16). The 16 are 095ea7b3 0c751377 18160ddd 1aa02d59 23b872dd 24a9d853 27e235e3 2e1a7d4d 3f4ba83a 40c10f19 5c975abb 70a08231 8456cb59 8da5cb5b a9059cbb d0e30db0.
- **Three-carrier maximum.** Maximum is 3, with 10 selectors on three carriers and none on four or more. Example `095ea7b3`: `find ... -name '*095ea7b3*' | wc -l` printed `6`, exit 0, 13:04Z; the files are 4byte and openchain on rv2token, kdxtoken and stewardtoken.

## Defect 1 (FAILS): 35 distinct 4byte bodies, not 43

- Nine selectors (`0c751377 3efdef66 48a3ef5c 6e8efde2 875194ac 9c421eb5 cee38a15 d869f754 e0749a6a`) return the same 52-byte body `{"count":0,"next":null,"previous":null,"results":[]}`, manifest sha256 `0595424161ea863805d9b92c0e52d7aa1e3c46ec58cd8f0d6933759006a5fb74`. So 43 selectors give 43 minus 9 plus 1 = 35 bodies.
- Producing command: inline Python over the six db manifests, exit 0, 13:03:01Z, printed `distinct 4byte hashes: 35  distinct selectors: 43` and `4byte count==0 selectors: [...] 9`. `extras.py` repeats it: `distinct 4byte body sha256 over 69 files: 35` (`extras-clone.out`, exit 0, 13:04:32Z).
- Openchain holds at 43, because each openchain body carries its own selector key.
- Suggested wording: "43 distinct selectors, 43 distinct openchain bodies, and 35 distinct 4byte bodies, because nine selectors return the same empty result body." The sentence in the wave-1 draft (`w1/EntryCorrection.md`) carries the same error.

## Defect 2 (FAILS as a description): "shared ERC-20 selectors", line 51

- Only 5 of the 16 shared selectors are ERC-20 standard functions: approve 095ea7b3, totalSupply 18160ddd, transferFrom 23b872dd, balanceOf 70a08231, transfer a9059cbb.
- The other 11 are not: owner 8da5cb5b, pause 8456cb59, paused 5c975abb, unpause 3f4ba83a, deposit d0e30db0, feeBps 24a9d853, balances 27e235e3, withdraw 2e1a7d4d, mint 40c10f19, set_fee 1aa02d59, fee_of 0c751377 (`extras-clone.out`, exit 0, 13:04:32Z).
- The second correction fixed the number (four to three), which is right. It left this descriptor. The number is unaffected.

## Adjacent checks that hold

- Line 205, "none on four": holds (above).
- Line 95, "6 distinct selectors (7 rows) had no candidate": the six selectors with empty 4byte results and null openchain results give 7 rows (inline Python, exit 0, 13:04:42Z). Holds.
- Of the nine empty-4byte selectors, three have openchain candidates (`fee_bps()`, `hasStreamed(address)`, `feeOn(uint256)`) and six are null (inline Python, exit 0, 13:03:38Z). [observation]
- Formatting only: line 205 is 332 characters, the longest line in the entry.

## Falsification of my own derivation

- `derive.py` (standard library only, run as `python3 -I -B`): Keccak-256 self-test on three known vectors PASS; 43 checks PASS at HEAD; exit 0, 13:04:03Z; output identical to the earlier pre-fix run.
- Mutant A (095ea7b3 added to carrierb's envelope only, copy under scratch): exit 1, 11 FAIL lines, including `maximum carriers per selector: observed=4 expected=3` (13:04:03Z). So the three-carrier check can fail.
- Mutant B (one response file removed): exit 1, 5 FAIL lines, including `saved responses observed=137 expected=138` (13:04:04Z).
- My first mutant A run crashed on a KeyError (`mutantA-derive.out`, exit 1, 13:03Z). I changed the check to count a missing file as a mismatch. The crash never produced a pass.

## Artifacts (all under /fast/scratch/hyaku/kaidoku-r26/seats/w2/EntryCorrectionReview/)

- derive.py 543906662091785dbb431488e22839b652dd9ba7ef78e0997755d01fa8a86eb5
- extras.py 189f50e654d58f3c80e8819da1ef928cf43c661cb265e87996cfdc92b1c75892
- derive-clone.out 281b07c839b21ed2f1ef0b87f73ab2d315d62ffc99b9b97c95dae3d16a90f66d
- extras-clone.out c0bdeb7bfabd92df53b86275f63ce0491af0a6941be8057d224aafcd9b5e34c2
- derive-mutantA.out db472e84534c52f90bea7de44c56a73a1289e4cd2b4411590476823a77290ea9
- derive-mutantB.out 692871a8de28397f95837225ac4ed98d280bbc21da6921a78bed8d8356fca761
- mutantA-derive.out cfe683a0f221a990416cfd86b9223cc9789063d7eddb67c378b903c5f0d43997 (pre-fix crash)

## Residual risk and verification gaps

- [inference] The author's meaning of "per selector" and "up to four" is not recorded. I judged the committed words.
- The Keccak-256 code is my own pure-Python implementation. It passes three known vectors and reproduces all 69 REA selectors, but I did not cross-check it with an external library.
- Not checked: envelope subject sha256 against the runtime hex files; REA not rerun; the lane's `tally-resolution.py` not run; the entry's rule scores not re-derived (outside this target).
- Snapshot is 2026-10-22T08:28:09Z to 08:31:37Z. No live lookup was made. [unknown] whether the public databases now return different bodies.
- Tools installed: none. Sources opened: none (local committed bytes only).
