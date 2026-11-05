# ExecGeomIndep — independent derivation of `T4-chain-szcpr-wrong` block-0 `sz_cpr` (round 89, kaidoku)

Seat: ExecGeomIndep (executor, leaf). Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, base `0ec2bb40…`.
Scratch: `/fast/scratch/hyaku/kaidoku-r89/ExecGeomIndep/` (deleted before yield; receipts copied here first).

## 0. What was built and what was not used

- `derive_szcpr.py` (this seat): derivation written from the stated law. Stdlib only. Imports nothing from
  `tools/round-87`, `round-88` or `round-89`. Its PackHeader and l_info locators are its own.
- `mkvariants.py` (this seat): writes the four inputs from the packed file. It imports `derive_szcpr` only.
- Not imported by the derivation: `tools/round-89/upx-field-value-repair.py`, `tools/round-88/upx-chain-repair.py`.
  The round-89 repair was run as a black box, only for comparison (§4).
- Tools installed: none. No pacman, uv, npm or cargo activity. Existing `/usr/bin/upx` 5.2.0 and `python3` used.
- Labrat: not dispatched.

## 1. Pins verified before use (all matched)

| path | sha256 | expected | match |
|---|---|---|---|
| tools/round-89/upx-field-value-repair.py | 332917f2b620da7a659b78db5bf498c8af2eba6ae529d872c2518b62ad6b1070 | 332917f2… | yes |
| tools/round-89/upx-field-battery.py | f6f5ed61f47e055b7cfa6b58c2e29064d8e4eb31859ff1963a8e80393cd0b720 | f6f5ed61… | yes |
| tools/round-87/upx-magic-repair.py | 96da7d8e981b04f5a598dc7eb8ec3f05eeae4b1498f769c83e72c67f6babec24 | 96da7d8e… | yes |
| /usr/bin/upx | cf2f6e7c6846a7c9a2224bc2bcc2dd79db6847d2cc73092d7356ce5c9aa8c969 | cf2f6e7c… | yes (`upx 5.2.0`) |
| /usr/bin/jq | e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806 | e8156675… | yes |
| /usr/bin/xxd | 7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65 | 7b1e5d0c… | yes |
| /usr/lib/libz.so.1.3.2 | 6c78c5e58c3bb49a1cd151a95cdf1a17fe07a91a57a59e0279b984c533075ca9 | 6c78c5e5… | yes |
| /usr/bin/docker-init | 0bd49c8d4da5601ce955c24a515917c9a132404df633c1e2fa28855cc2e3e115 | 0bd49c8d… | yes |

Packed outputs (`upx --best -q -o packed/<c> carriers/<c>`, all exit 0) are in `receipts/carrier-hashes.txt`.
Block 0 sits at `l_magic + 20` with `l_magic` at 556 (jq, xxd, docker-init) or 9284 (libz); the true `sz_cpr`
is the word at block0+4, and `u_len`/`u_file_size` come from the PackHeader.

## 2. Derivation

Law, as implemented in `derive_szcpr.py` (`derive()`):

1. Locate the PackHeader: last `UPX!` in the 512-byte tail window whose 32 bytes pass version ≥ 10,
   non-DOS format, header checksum `sum(bytes[4:31]) % 251`, and positive `c_len`/`u_len`/`u_file_size`.
2. Candidates: every `p_filesize == u_file_size` occurrence at `p` whose `l_magic = p-12` reads `UPX!` and
   whose version/format bytes (`l_magic+6`, `+7`) match the PackHeader.
3. For each candidate: `b0 = l_magic + 20`; `sz_unc0 = u32(b0)`; skip if `sz_unc0 == 0`.
   Scan `s1` in `[b0+13, ph_off-12)` for a plausible block (`0 < sc <= su`, fits before PackHeader, method
   in {block0 method, PackHeader method}); `derived = s1 - (b0+12)`, requiring `0 < derived <= sz_unc0`.
4. Write `derived` into a copy at `b0+4`; walk that copy from `b0` (contiguous), and where the walk stops at the
   embedded loader, resume at the best later plausible chain that reaches an end sentinel. Keep candidates
   that reach a sentinel.
5. Survivor key `(total <= u_len, total, -derived)`, where `total` is the sum of `sz_unc` over the contiguous
   segment plus the resumed segment. Maximum wins.

**Stored-value blindness.** The stored word at `b0+4` is read into the report record only. It is overwritten in
the working copy before any walk. The scan starts at `b0+13`, so it never reads `[b0+4, b0+8)`. The locator reads
`l_magic+12` (= `b0-8`), not `b0+4`. The only other block-0 read is `sz_unc0` at `b0`.

**Step counts** (`stats` in each receipt; identical across the four inputs of a carrier):

| carrier | l_magic | block0 | lmagic_candidates | scan_offsets | plausible_next | resume_candidates | walk_steps | sentinel_survivors | total (sum of stats) |
|---|---|---|---|---|---|---|---|---|---|
| jq | 556 | 576 | 1 | 13,399 | 10 | 3,890 | 22 | 1 | 17,323 |
| xxd | 556 | 576 | 1 | 18,923 | 10 | 3,881 | 22 | 1 | 22,838 |
| libz.so.1.3.2 | 9,284 | 9,304 | 1 | 56,215 | 8 | 5,404 | 18 | 1 | 61,647 |
| docker-init | 556 | 576 | 1 | 357,147 | 9 | 346,399 | 57 | 3 | 703,616 |

## 3. Agreement table (carrier × input) — my derivation

Input: `intact` = packed file; `zero` = `sz_cpr := 0`; `minus8` = `sz_cpr := true − 8`; `fff0` = `sz_cpr := 0xFFFFFFF0`.
Cell = derived `sz_cpr` (class label from this seat's classifier; receipt `receipts/derive-<c>-<input>.json`).

| carrier | intact | zero | minus8 | fff0 | all four agree |
|---|---|---|---|---|---|
| jq | 252 (intact) | 252 (chain-geometry) | 252 (field-value) | 252 (field-value-outofrange) | **yes** |
| xxd | 249 | 249 | 249 | 249 | **yes** |
| libz.so.1.3.2 | 201 | 201 | 201 | 201 | **yes** |
| docker-init | 226 | 226 | 226 | 226 | **yes** |

Accounting for the derived candidate (`uncompressed_accounted / u_len`, fits): jq 30,800/30,800 yes;
xxd 38,928/38,928 yes; libz 98,592/108,560 yes (named limit: appended data is not chain data); docker-init
851,288/851,288 yes. On docker-init the three survivors are (136: 123,942,159 no), (226: 851,288 yes),
(440: 850,696 yes); 226 wins on `(fits, total, -derived)`.

Repaired bytes: for every non-intact input, my output `cmp` equals the intact packed file (12 cells, all exit 0).
`upx -t` on the tampered inputs (§6) refuses, so the repaired outputs are the only way back to a passing pack.

Sweep (stronger than the four inputs): for each carrier, 55 stored values (0, 1, 2, 7, 8, 9, true±1, true, true±8,
0x7FFFFFFF, 0x80000000, 0xFFFFFFFF, 0xFFFFFFF0, 20 random 32-bit, 20 random < 4096) all derive to the true value:
jq 55/55 → 252; xxd 55/55 → 249; libz 55/55 → 201; docker-init 55/55 → 226
(`receipts/ablation.json`).

## 4. Comparison with the repo round-89 repair

`python3 -I -B tools/round-89/upx-field-value-repair.py --in X --out Y --info Z` (16 cells, all exit 0;
`receipts/repo-<c>-<input>.info.json`, `compare-repo-vs-mine.json`):

| carrier | intact | zero | minus8 | fff0 |
|---|---|---|---|---|
| jq | derived 252, class intact | 252, chain-geometry | 252, field-value | 252, field-value |
| xxd | 249, intact | 249, chain-geometry | 249, field-value | 249, field-value |
| libz.so.1.3.2 | 201, intact | 201, chain-geometry | 201, field-value | 201, field-value |
| docker-init | 226, intact | 226, chain-geometry | 226, field-value | 226, field-value |

`info.derived_sz_cpr` equals mine in all 16 cells. The repo classifier does not separate `0xFFFFFFF0` from
ordinary wrong values (`field-value`); my classifier labels it `field-value-outofrange`. This is a labelling
difference only; the derived value is identical. The repo `anchor_class` is `None` on zero/fff0 (round-87 anchor
refused) and `intact` on intact/minus8.

## 5. Ablation — does the stored value change the result?

**Answer: no, for the derivation as written.** Mechanism: `derive()` copies the input and writes the candidate
into `b0+4` before any walk, so no walk or gate reads the stored word; the scan starts at `b0+13`; the locator
does not touch `b0+4`. Measured: the 55-value sweep per carrier gave one derived value each (§3).

**Mutant (scratch only, `mut_stored_visible.py`):** identical except the write at `b0+4` is removed, so the walk
reads the stored word. Derived value per input (`receipts/ablation.json`, `mutant_stored_visible`):

| carrier | intact | zero | minus8 | fff0 |
|---|---|---|---|---|
| jq | 252 | refused (no l_info candidate…) | 252 | refused |
| xxd | 249 | refused | 249 | refused |
| libz.so.1.3.2 | 201 | refused | 201 | refused |
| docker-init | **136** (wrong; u_len-violating candidate) | refused | **136** | refused |

So a stored-reading derivation changes its outcome with the stored value: zero and 0xFFFFFFF0 are refused on all
four carriers, and on docker-init it returns the wrong candidate (136) for both intact and minus8. The
stored-blind derivation is the one that agrees across inputs. The mutant is a control for the ablation, not a
candidate repair.

## 6. `upx -t` on the four inputs (Python subprocess runs; receipts `upxt-*.txt`, `upxt-summary.json`)

- intact (all four carriers): rc 0, `Tested 1 file.`
- zero: rc 1, `CantUnpackException: b_info corrupted`
- minus8: rc 1, `Exception: compressed data violation`
- fff0: rc 1, `CantUnpackException: b_info corrupted`

Note: the `minus8` refusal is at the payload stage (`compressed data violation`), the class the round-88 `upx -t`
precondition describes for in-range wrong values. Zero and fff0 are refused at the structural stage.

## 7. Commands and exit codes (all run from the scratch dir unless noted)

| # | command (abbreviated) | exit |
|---|---|---|
| 1 | `sha256sum` over the three tool files and five host objects (§1) | 0 |
| 2 | `upx --version \| head -3` | 0 (pipeline) |
| 3 | `cp /usr/bin/{jq,xxd,docker-init} /usr/lib/libz.so.1.3.2 carriers/` | 0 |
| 4 | `upx --best -q -o packed/<c> carriers/<c>` ×4 | 0 ×4 |
| 5 | `sha256sum carriers/* packed/*` → `receipts/carrier-hashes.txt` | 0 |
| 6 | `python3 -I -B mkvariants.py packed/<c> variants/<c>` ×4 | 1 ×2 (first attempts: `ModuleNotFoundError` — module name, then my own l_magic offset bug); **0 ×4 after fixes** |
| 7 | `python3 -I -B derive_szcpr.py --in variants/<c>/<v> --json … --out ….fixed` ×16 | 0 ×16 |
| 8 | `cmp variants/<c>/<v>.fixed packed/<c>` ×12 | 0 ×12 |
| 9 | `python3 -I -B tools/round-89/upx-field-value-repair.py --in … --out … --info …` ×16 | 0 ×16 |
| 10 | `upx -t variants/<c>/<v>` ×16 (via Python subprocess) | 0 ×4 (intact), 1 ×12 (tampered) |
| 11 | in-process sweep + mutant (`eval`, Python) | completed; `receipts/ablation.json` |
| 12 | `python3 -I -B derive_szcpr.py --in carriers/xxd --json …` (refusal control, unpacked) | 2; stderr `refused: no PackHeader validated in the tail window` |
| 13 | final check: `derive_szcpr.py --in variants/docker-init/zero --out final-check.bin` + `cmp` vs packed | 0 / 0; derived 226, class chain-geometry |

Bash loops for `upx -t` returned exit 1 with no output after the first iteration in the persistent shell; I
re-ran the same 16 checks from a Python subprocess (row 10). The earlier shell output is not cited as evidence.

## 8. Defects in my own first pass (disclosed)

- The first locator used `p_filesize-12` as the candidate offset but tested the version byte at `+2`/`+3`
  (wrong layout, zero candidates). Fixed to the l_magic layout (version `+6`, format `+7`), which matches the
  repo tool (`m+6`, `m+7`). That fix changed the output from refused to derived; the derived values were then
  checked against the round-88 record (jq 252, xxd 249, libz 201, dinit 226), which matches.
- A docstring named an `oracle-packheader.py` I never wrote; corrected. No oracle was run by the derivation.
- A pycache directory was created by an in-process import; removed.

## 9. Limits (within this seat's scope)

- One field, four carriers, one packer version. Uniqueness on other carriers is not established; the
  docker-init survivor set (three candidates, one fits `u_len`) is the only ambiguity measured.
- The derivation does not decompress; `upx -t`/`upx -d` are the guards (§6).
- Round-89's C2 (depth block 29) was not in this seat's assignment and was not examined.

## 10. Verdict for the claim under test

Independent derivation: the derived value does not depend on the stored value (sweep 55/55 per carrier; four
inputs agree on 4 of 4 carriers). The repo repair's derived value agrees with mine in 16 of 16 cells, with one
label difference (`0xFFFFFFF0`). The stored-reading mutant shows the stored word would matter if it were read.
