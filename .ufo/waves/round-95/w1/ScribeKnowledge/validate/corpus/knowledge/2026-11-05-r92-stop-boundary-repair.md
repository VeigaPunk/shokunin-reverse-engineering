# Packed-ELF last-block `sz_cpr`: a stop-boundary tamper within ±16 is repaired by the packer's own verdict, and the refusal label stops admitting three named counterfeits (round 92, R92-C1 coverage, R92-C2 calibration)

verified-at: `a3d3c649ddfef2b4c850ec950e9f633194f08efc` (tool `tools/round-92/upx-stop-boundary-search-repair.py`, sha256 `ce1b1769d56c1d90fcf2ee0800ca508476b45eddc2e8a6d7e2f01aa8d12a70c1`); declaration `11f8606178dfd9e72001b31daf412c5463106a63`; base `73a882712907606eba074377b536c6dd82517e25`.
source: S313 — UPX 5.2.0 `src/p_unix.cpp` `PackUnix::unpackExtent` block loop (the 12-byte header read, the bound, the payload read). It supplies no stop-boundary verdict.
source: S317 — UPX 5.2.0 `src/p_lx_elf.cpp` `PackLinuxElf64::unpack`, the end-of-file trailer check after the last extent. This is the caller-side check that decides the stop-boundary class.
recheck: 180d, and on any UPX release. Master drift is recorded under Limits.

## The class

A packed UPX 5.2.0 `--best` little-endian ELF whose **last** `b_info` block before the chain stop has `sz_cpr` moved by −7 or +7, both in range (`0 < value <= sz_unc`). Round 91 refused this class (`refused 8 of 8`). The frozen round-92 counter scores five carriers: `jq`, `xxd`, `libz`, `dinit` (`/usr/bin/docker-init`), and `xz` (`/usr/bin/xz`, named by no round-91 carrier list, cheat table or hash table), two directions each (ten near cells), plus ten far cells at ±40 and five intact controls.

## The rule as implemented

- Input that `upx -t` accepts: returned byte-identical, rc 0 (the round-91 intact path, unchanged).
- Input that the round-91 path refuses: for every `v` in `[stored−16, stored+16]` with `0 < v <= sz_unc`, write `v` as the four-byte little-endian `sz_cpr` of the last block on a private copy and run `upx -t` on it. The candidate values are the packer's verdicts, not a geometric rule.
- Exactly one green value `v* != stored`, an output that differs from the input only inside the four-byte window, and a green output: write that output, rc 0.
- Zero green values, or two or more: typed refusal, rc 2, last stdout line a JSON object with `refused`, no output file.
- The last block is `blocks[-1]` of the round-90 longest-prefix walk. The chain ends thousands of bytes before the PackHeader on all five carriers, so the walk steps through the tampered block in both directions. A first draft that assumed the chain ends at the PackHeader refused all twenty cells (`.ufo/waves/round-92/w1/ExecRepair/probe1-firstdraft-failure.json`); the probe measured the geometry and the draft was corrected before any counter run.

## Measured

| claim | before (base `73a882712`) | after (`a3d3c649`) | receipt |
|---|---|---|---|
| R92-C1 frozen label `repaired 10 of 10; wrong 0; unsafe 0; intact 5 of 5; far-refused 10 of 10` | `repaired 0 of 10; wrong 0; unsafe 0; intact 5 of 5; far-refused 10 of 10`, met False, exit 1 (round-91 repair as the do-nothing control) | same label, met True, exit 0 | `.ufo/waves/round-92/pre/c1-control-do-nothing-round91-repair.json`; `.ufo/waves/round-92/l1/scores/c1-at-a3d3c649ddfef2b4c850ec950e9f633194f08efc.json` |
| R92-C2 admitted counterfeits (CHEAT-A carrier-read, CHEAT-B hash table, CHEAT-C exit 1), frozen label `refused 10 of 10; typed 10; unsafe 0; intact 5 of 5` on v2 | round-91 label admits 3 of 3 (`refused 8 of 8; unsafe 0; intact 4 of 4`, met True ×3) | v2 admits 0 of 3 (A and B `intact 4 of 5`; C `typed 0`; all met False). Positive control, round-91 refusal tool under v2: met True | `.ufo/waves/round-92/pre/c2-do-nothing-v1-counterfeit-{A,B,C}.json`; `.ufo/waves/round-92/l1/scores/c2-counterfeit-{A,B,C}-v2-at-a3d3c649…json`; `…c2-positive-v2-round91-at-a3d3c649…json` |
| Round-90 regression arm on the candidate `P1 6 of 6; P2 4 of 4; P3 4 of 4` | (round-91 tool met at base) | met True, REA control true | `.ufo/waves/round-92/l1/scores/regress-candidate-at-a3d3c649…json` |
| Premise probe, five carriers | — | exactly one packer-green value in `[stored−16, stored+16]`, equal to the stored value; `stored±40` red on all five; packing byte-deterministic | `.ufo/waves/round-92/w1/ExecProbe/premise.json` |
| Supplementary, not the frozen label: carriers no table names (`bzip2`, `gzip`, `patch`) | — | near ±7 repaired 2 of 2 on each; far ±40 refused 2 of 2 on each | `.ufo/waves/round-92/l1/scores/supp-unseen-carriers-at-a3d3c649….json` |

Candidate selftest at `a3d3c649`: `SELFTEST cases=6 failures=0`, rc 0; the two-green fixture was not constructible (see Limits).

## Counting command

```sh
python3 -I -B tools/round-92/stop-boundary-repair-battery.py --root . \
  --repair-cmd tools/round-92/upx-stop-boundary-search-repair.py \
  --work <scratch> --rev a3d3c649ddfef2b4c850ec950e9f633194f08efc \
  --expect "repaired 10 of 10; wrong 0; unsafe 0; intact 5 of 5; far-refused 10 of 10" \
  --json-out <receipt>
```

Exit 0 means the label equals `--expect` and the counter's own conditions hold. The do-nothing control is the same command with `--repair-cmd tools/round-91/upx-stop-boundary-repair.py` at `73a882712` (exit 1, measured above). The R92-C2 counter is `tools/round-92/stop-boundary-battery-v2.py` with the same carrier set and `--expect "refused 10 of 10; typed 10; unsafe 0; intact 5 of 5"`. The round-91 instruments are unchanged (`git diff --stat 73a882712 a3d3c649 -- tools/round-91` is empty).

## Limits (measured where stated; none is closed here)

1. **The window is a cap, not a packer property.** `±16` is the tool's bound; the frozen far arm (`±40`) measures that cap. The packer's verdict decides which in-window value is pristine. The critic measured `±17..±56` refused on `jq` and `xz` through the round-91 tool (`.ufo/waves/round-92/w1/CriticClaims/receipts/p2-r91-refusal-probes.json`).
2. **A pinned-image table passes the frozen C1 label.** A repair that writes the five pinned packed images and refuses otherwise meets `repaired 10 of 10` (measured by the critic, `c1-table-repair-5.json`, met True; and by MutCounter N1i). The four-carrier table fails only on `xz`. The C1 credit is therefore the five pinned carriers; the out-of-set probe above is the evidence that the search is not a table on the bytes the table cannot name. A fresh-pack oracle is the fix for a later round, and no frozen counter was changed to add it.
3. **C2 covers three named counterfeits, not the calibration class.** A carrier-read over all five carriers (CHEAT-D) and a five-entry hash table (CHEAT-E, MutCounter M2) pass v2 (met True). Both fall in the claim's declared "unseen-carrier table" limit. The claim's headline is "stops admitting the three named round-91 counterfeits".
4. **The two-green refusal path has no measured instance.** A ±64 sweep around the pristine value on `xxd` found no second green value, so the `two or more` branch is not exercised by any fixture. Its refusal is code, not measurement.
5. **Inherited from round 91, not changed here.** The round-90 walker's cost is quadratic in the number of fruitful records, so a maximum-size crafted input is not bounded by the 256 MiB cap in practice (SentinelRepair F-C1, HIGH; QUALITY 183). There is no aggregate budget across the 33 verdicts (F-C2, MED). `--out` written through an ancestor symlink lands outside the work tree with rc 0 (F-A3, MED). A missing `TMPDIR` falls back to `/tmp` (F-B1, MED). These are routed to round 93.
6. **Non-ELF packed inputs are not measured.** The host UPX refuses a .NET DLL as `unsupported machine 0xfd1d`; no PE or Mach-O packed sample was built.
7. **Packer dependence.** The result depends on UPX 5.2.0 (sha256 `cf2f6e7c6846a7c9a2224bc2bcc2dd79db6847d2cc73092d7356ce5c9aa8c969`). The oracle is UPX itself. [INFERENCE] A packer whose `upx -t` verdict disagreed with its own decoder would change the outcome.
8. **The caller, not S313, decides the stop boundary.** S313's loop reads each header and its `sz_cpr` payload and does no position check against the next header. The last-block verdict comes from `PackLinuxElf64::unpack`'s trailer check (S317). The S313 teaching sentence "the next header immediately after it" is accurate for the loop and does not by itself prove the stop-boundary verdict. On `master` (`7c7bea44`, 2026-11-05) the S313 lines have moved: the payload read is `fi->readx(cbuf, sz_cpr)` at line 506 (the row's line 504 is v5.2.0-only). A recheck against master must cite 506.

## Gate

| row | URL | access date | HTTP / size / sha256 | located quote (≤25 words) | used for |
|---|---|---|---|---|---|
| S313 | https://raw.githubusercontent.com/upx/upx/v5.2.0/src/p_unix.cpp | 2026-11-05 (re-opened this round by ScoutSource; sha re-derived by the lane) | 200 / 24181 / `bf83c4133c27d39433db63bf604daf577d429d734c542d29c0b9cc8ed229642e` | line 496: `if (sz_cpr > sz_unc \|\| sz_unc > (int)blocksize)` | the per-block bound and the payload read; limit 8 |
| S317 | https://raw.githubusercontent.com/upx/upx/v5.2.0/src/p_lx_elf.cpp | 2026-11-05 (opened this round by the lane; `curl -fsSL` exit 0) | 200 / 373743 / `551fc8675a59493793f59b64eb8bb9cc208a34f701ccd2bda8c9aaafb228d2dc` | line 8065: `if (sz_cpr != UPX_MAGIC_LE32)  // sz_cpr must be h->magic` | the caller's end-of-file trailer check that decides the stop boundary |

Line numbers verified by `sed -n '8055,8070p'` on the fetched bytes: 8057 `// check for end-of-file`, 8058 `fi->readx(&bhdr, szb_info);`, 8062 `if (sz_unc == 0)`, 8065 the magic test, 8066 `throwCompressedDataViolation();`, 8068 `else { // extra bytes after end?`, 8070 the throw.

Round-91 entry this extends: `corpus/knowledge/2026-11-05-r91-stop-boundary-refusal.md`. Its "refusal is the capability" sentence is superseded for the declared ±16 window only, and only at the measured revision above.
