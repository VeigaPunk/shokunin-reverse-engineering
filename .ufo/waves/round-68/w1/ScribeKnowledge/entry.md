# UPX-packed ELF through a detect → unpack → identity → recover route: the packed-ELF triage surface, Core for two pinned x86-64 carriers (round 68, R68-C2)

status: R68-C2, the round-68 packed-ELF route — Core for the two carriers named below iff
`tools/round-68/packed-elf.py` (sha256 `48ef4c68…`) reports `carriers_matched 2` of `target 2`,
`control_ok true`, every arm true on both carriers (`detected`, `before_ok`, `identity_ok`,
`recovery_ok`, and `refusal_ok` on the carrier that pins `0x103fa0`), both packed carriers at exactly
3 procedures, and the non-packed originals neither listed nor decompressible by the packer, at the
measured revision (SCORECARD `## 2026-11-03 — round 68`; the scored receipt is the L1's after-arm
under `.ufo/waves/round-68/l1/scores/`). A false carrier clause, a drifted packer or carrier pin, an
unrestored byte, or a post-freeze instrument edit replaces this line and the PROVINCE row with the
honest stop; the miss is reported, never narrowed.

source: S269 — UPX 5.2.0 documentation, the plain-text manual `doc/upx-doc.txt` at tag `v5.2.0` — https://raw.githubusercontent.com/upx/upx/v5.2.0/doc/upx-doc.txt — `NOTES FOR LINUX/ELF386` (heading line 433), fetched-bytes lines 441-442, byte offset 18 963: "Packed programs will be byte-identical to the original after uncompression." (10 words; the sentence wraps after "after") — the format-scoped statement for `linux/elf386`, the format both carriers use; the general Linux section repeats the claim at lines 383-384 (offset 16 437), the `--exact` bound sits at lines 101-106, `-d` is described at lines 73-75 and `-l` at lines 84-88; re-read 2026-11-03 (37 208 B, sha256 `4dc547edc7201f205ce904f373518b6fcaef608d5aafd8a4a7564d42993b8c42`)
source: S269 (same manual, other shipped forms, opened by this seat) — `doc/upx.pod` at the same tag (https://raw.githubusercontent.com/upx/upx/v5.2.0/doc/upx.pod; 35 451 B, sha256 `cc93ccea8e9e9f4721b1b1cd983d960deea432c7d4913f1efe35f33d2a1c31c2`): `NOTES FOR LINUX [general]` lines 459-461, byte offset 15 849, "UPX keeps your original program untouched. This means that after decompression you will have a byte-identical version" (17 words), `=head2 Decompress` line 94, `=head2 List` line 107, `--exact` line 126; the installed man page (decompressed `upx.1`, 40 077 B, sha256 `09552b3cf4e9073c288060b8f50ed1c1dde3dca89dcaf1230367b6c3e15d4e25`) carries the ELF386 sentence at line 263
verified-at: 2026-11-03 (the landing commit that first adds this entry; the pre-freeze route receipt `.ufo/waves/round-68/l1/pre/c2-dryrun-at-base.json`, the controls receipt `.ufo/waves/round-68/l1/pre/controls-at-base.json`, and the score receipt under `.ufo/waves/round-68/l1/scores/`)
recheck: on-refetch — `curl -fsSL https://raw.githubusercontent.com/upx/upx/v5.2.0/doc/upx-doc.txt -o upx-doc.txt && sha256sum upx-doc.txt` (expect `4dc547ed…`) and `grep -n 'Packed programs will be byte-identical' upx-doc.txt` (ELF386 at 441-442); the pod form `doc/upx.pod` at the same tag re-fetches to `cc93ccea…` and `grep -n 'UPX keeps your original program untouched' upx.pod` is line 459. The scoring recheck is `python3 -I -B tools/round-68/packed-elf.py --root <LANE> --rev <REV> --pkg /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents --work <SCRATCH> --json-out <OUT>` → exit 0 with `carriers_matched 2` and `control_ok true`; both carriers are host binaries pinned by sha256 and are never committed.

## What moved, and only what moved

[observation] At the base `fcbe200f6739c38939e0dabf3f251de2cc6bd727`, `upx` appears only in PROVINCE's host-fallback-readers row (`PROVINCE.md:62`, `git grep -n -i upx fcbe200f -- PROVINCE.md SKILL.md tools`), and no packed-binary instrument exists at that revision (`git cat-file -e fcbe200f:tools/round-68/packed-elf.py` exits 128; `git ls-tree -r --name-only fcbe200f -- tools | grep -i 'pack\|upx'` returns nothing).

[observation] REA analyzes the bytes it is given: on the packed copy of `/usr/bin/jq` it reports `procedure_count 3`, `segment_count 3`, `string_count 3`, where the same binary before packing reports `167 / 30 / 190`; on the packed copy of `/usr/bin/xxd` the packed inventory is `3 / 3 / 6` against `99 / 29 / 103`. [observation] An address-level verb separates the two states: `rea decompile <packed> 0x103fa0` exits 1 with envelope `code: invalid_request`, while the same address on the restored copy exits 0 with 4 841 bytes of pseudocode containing `FUN_00103fa0`. [inference] The stub inventory is not an empty result and not an analyzer error: it is a parsed inventory of a loader stub whose section header table does not exist, and the route's value is that it turns that state into the original's.

[inference] The surface the round moves is therefore the **route**, not REA's reader: REA gains no packed-binary key. The route is a pre-step — detect, restore bytes outside REA, then hand the restored file to `rea analyze` — and the Core claim below is scoped to that route on the two pinned carriers.

## The route, arm by arm

| arm | command (instrument order) | `jq` | `xxd` |
|---|---|---|---|
| detect | `upx -l <packed>` **and** `readelf -SW <packed>` section count | rc 0; 0 sections ("There are no sections in this file") | rc 0; 0 sections |
| before | `rea analyze --format json <packed>` | 3 / 3 / 3 procedures/segments/strings, below the floor 50 | 3 / 3 / 6, below the floor 25 |
| unpack | `upx -d -q -o <out> <packed>` | rc 0, 30 800 → 14 036 B, `linux/amd64` | rc 0, 38 928 → 19 560 B, `linux/amd64` |
| identity | `sha256(<out>) == pin` | `e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806` | `7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65` |
| recover | `rea analyze --format json <out>` | 167 / 30 / 190, equal to the original on all three counts | 99 / 29 / 103, equal |
| refusal | `rea decompile <packed> 0x103fa0` vs `<out> 0x103fa0` | packed rc 1 / `invalid_request`; unpacked rc 0, 4 841 B, `FUN_00103fa0` present | arm absent (no pinned address) |
| control | `upx -l <orig copy>` and `upx -d <orig copy>` | rc 2 and rc 2 (`NotPackedException: not packed by UPX`), nothing written | rc 2 and rc 2 |

[observation] The two floors are half the carriers' pinned `min_orig_procedures` (100 and 50), so `before_ok` asserts the packed inventory is a stub relative to the original, not merely "small". [observation] The originals' own section tables are intact: `readelf -SW` counts 28 section headers on `/usr/bin/jq` and 27 on `/usr/bin/xxd` (measured 2026-11-03), against 0 on the packed copies.

[observation] The instrument copies each carrier out of its host path before packing (`shutil.copy` to `orig-<basename>`, mode 0755) and runs every arm on that copy; `/usr/bin/xxd` is a symlink to `/usr/bin/tinyxxd` (`ls -l /usr/bin/xxd`), which `upx` refuses directly with `IOException: is a symlink -- skipped` (rc 1), while a dereferenced copy of the same bytes gives `NotPackedException` rc 2 on `upx -l` and rc 2 on `upx -d` with nothing written (measured 2026-11-03) — the control the receipt records is earned on the dereferenced copy, not on the live symlink path. [inference] A route that ran `upx` on the live path would misclassify that carrier's control arm as a route failure.

## The identity rule, and what the manual bounds

[observation] The manual states the general Linux property (S269, pod lines 459-461): UPX "keeps your original program untouched", so "after decompression you will have a byte-identical version". [observation] It states the format-scoped property for `linux/elf386` (S269, txt lines 441-442): "Packed programs will be byte-identical to the original after uncompression." [observation] The two carriers' restored sha256 equal their pins exactly, which is the measurement the `identity_ok` arm performs; the arm does not infer identity from the manual.

[inference] Because the restored bytes are the original bytes, the inventory recovered from them describes the program the packed file ships, not a reconstruction or an estimate. [observation] The manual bounds its own guarantee elsewhere: `--exact` ("require to be able to get a byte-identical file after decompression with option `-d`") is documented as work in progress and "not supported for all formats yet" (S269, pod line 126), so byte identity is a per-format, per-carrier measured property, not a promise to assume.

## The two carriers (host binaries, pinned, never committed)

[observation] Both carriers are x86-64 PIE executables from the Arch package set: `/usr/bin/jq` (30 800 B, pin `e8156675…`) and `/usr/bin/xxd` → `/usr/bin/tinyxxd` (38 928 B, pin `7b1e5d0c…`). [observation] At the base both are below their declared floors when packed (3 procedures against 100 and 50), which is what makes the before-arm falsifiable rather than decorative. [observation] The packed copies are rebuilt inside `--work` on every run and are never committed; the receipt records their sha256 (`e8b6c9e7…` for jq, `1727faf9…` for xxd) so the packed bytes themselves are reproducible to the extent UPX 5.2.0 is deterministic.

## The controls that keep the route honest

[observation] Two do-nothing arms are red in `.ufo/waves/round-68/l1/pre/controls-at-base.json`: `c2-packed-only` (verdict from the packed arm alone) reports `carriers_matched 0`, `met_target false`, with `identity_ok` and `recovery_ok` false on both carriers; `c2-no-identity` (unpack and recovery, identity dropped) also reports `carriers_matched 0`, `met_target false`, with `identity_ok` false while `recovery_ok` is true. `c2-real` reports `carriers_matched 2`, `control_ok true`, `met_target true`. [inference] Neither shortcut reaches the target, so a green score cannot be produced by skipping the identity step or by reading only the stub.

## The counter's own boundary

[observation] The pre-freeze route receipt `.ufo/waves/round-68/l1/pre/c2-dryrun-at-base.json` records `instrument.sha256 7ee286c03391dc464c90a3f24498258bfef09dd89300aa9a246fd35ac85ef25c` and `instrument.rev null`, and its `rev` is the branch name `main`; the frozen instrument's sha256 is `48ef4c68…`, so that receipt demonstrates the route with an earlier instrument revision and is not the frozen counter's scored run. [observation] The `--skip-run` receipt `.ufo/waves/round-68/l1/pre/c2-skiprun.json` carries yet another instrument sha (`ff11d8ec…`) and correctly emits `closure null`, `verdict_claimed false`, `met_target null`.

[unknown] This seat did not run the frozen counter at the measured revision; whether the after-arm reproduces the dryrun's counts and whether it names both `rev` (a commit) and `instrument.rev` (atom A9) is observed only in that receipt, not here.

## Limits

- One packer: UPX 5.2.0 (`/usr/bin/upx`, sha256 `cf2f6e7c6846a7c9a2224bc2bcc2dd79db6847d2cc73092d7356ce5c9aa8c969`; UCL 1.03, zlib 1.3.1.1-motley). No other packer was measured.
- No packed PE or Mach-O carrier; no packed shared library and no packed static binary. The two carriers are both x86-64 PIE `linux/elf386` and nothing else.
- No anti-UPX-modified stub: an altered magic, a patched entry, or a stub that makes `upx -d` refuse by design was not built or measured. `upx -l` is UPX-specific, so a different packer's output would read as "not packed" rather than as another class.
- Inventory equality is equality of three integer counts (`procedure_count`, `segment_count`, `string_count`) between the restored file and the original; it is not semantic equality of the recovered program, and no byte-level comparison of REA's two envelopes is claimed (their `evidence_id` values differ with the path).
- The identity arm is only as strong as the pin: both carriers are host paths that drift with package upgrades, so the route is pinned by carrier sha256 and refuses (exit 2) on pin drift rather than scoring a changed file.
- No artifact is committed; every run needs `node`, `/usr/bin/upx`, and both host binaries at their pins, so a future host without them cannot reproduce the score.
- The manual's `--exact` caveat is not exercised: no format whose round trip UPX documents as incomplete was measured.

## Unknowns

[unknown] Whether an anti-UPX stub can be routed at all — no such carrier was built.
[unknown] Whether the route holds for a packed `.so` or a packed static binary — neither was measured, and UPX refuses some of them before analysis starts.
[unknown] Whether a packed carrier with a section header table still present (a packer that keeps sections) would pass `detected` — the both-conditions rule would report it not packed, and no such carrier was measured.
[unknown] Whether the after-arm at the measured revision reproduces `before_procedures [3, 3]`, `carriers_matched 2` and `control_ok true`, and whether it records a commit in `rev` and `instrument.rev`; the L1's scored receipt is the only observer.
[unknown] Whether a third carrier probed elsewhere in the wave is inside the route's class; it is outside this claim's two pinned carriers and this seat did not examine it.
[unknown] Whether REA's recovered inventory would differ if the restored bytes differed only outside the code sections; the route never had such a pair.

## Evidence

- Instrument: `tools/round-68/packed-elf.py`, sha256 `48ef4c688a14faf381abbd2cc2b29061035f38c97815e2365957843433e5276e`; `--selftest` printed `{"cases": 13, "failed": [], "ok": true}` and exited 0 on 2026-11-03 (run by this seat).
- Route receipt: `.ufo/waves/round-68/l1/pre/c2-dryrun-at-base.json` — `closure {carriers_matched 2, target 2, control_ok true, met_target true}`, `failing []`, `before_procedures [3, 3]`, per-carrier arms and counts as tabled above.
- Controls: `.ufo/waves/round-68/l1/pre/controls-at-base.json` — six arms, `c2-packed-only` and `c2-no-identity` not met, `c2-real` met; `.ufo/waves/round-68/l1/pre/c2-skiprun.json` — `closure null`.
- Carrier pins: `jq e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806`, `xxd 7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65`; sources `/usr/bin/jq`, `/usr/bin/xxd` (→ `/usr/bin/tinyxxd`).
- Packer pin: `/usr/bin/upx`, `upx 5.2.0`, sha256 `cf2f6e7c…`.
- REA pin: rea-agents 6.5.0, `package.json` sha256 `a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c`, invoked as `node <pkg>/scripts/rea.mjs`; node v24.21.0; the npx cache-level lock is recorded (`lock_recorded_not_pinned true`, `lock_sha256 null`) and never pinned (QUALITY #110).
- Source pins: S269 txt 37 208 B `4dc547ed…` (pod form of the same tag 35 451 B `cc93ccea…`); installed man page 40 077 B (decompressed) `09552b3c…`.

## Coverage-map row (for `corpus/README.md`, `## Coverage map`)

```markdown
| UPX-packed ELF triage (round 68) | `2026-11-03-r68-packed-elf-route` | **Core** — detect (`upx -l` rc 0 and no section-header table), unpack (`upx -d`), identity (restored sha256 equals the carrier pin) and recovery (REA inventory equals the original's) on two pinned x86-64 carriers: packed stub 3 procedures against originals 167/30/190 and 99/29/103; the pinned address `0x103fa0` refused (`invalid_request`, rc 1) on packed bytes and recovered (rc 0, 4 841 B, `FUN_00103fa0`) after unpack; the originals neither listed nor decompressible (rc 2 on both); instrument `tools/round-68/packed-elf.py` (sha256 `48ef4c68…`, 13-case selftest), scored receipt `.ufo/waves/round-68/l1/scores/`; limits: UPX 5.2.0 only, two host carriers, count equality not semantic equality |
```

## PROVINCE Core row (for `PROVINCE.md`, `## Round-68 additions to Core`)

```markdown
| Surface | Ports / keys | Probe | Verified evidence |
|---|---|---|---|
| UPX-packed ELF triage — detect (packer listing plus the absence of a section-header table), unpack with sha256 identity against the carrier pin, recover the original's REA inventory, and keep the packed-bytes stub as the before-arm; two pinned x86-64 host carriers (`/usr/bin/jq`, `/usr/bin/xxd` → `tinyxxd`) | no new REA key — a pre-step outside REA: `/usr/bin/upx` 5.2.0 (sha256 `cf2f6e7c…`) for `-l`/`-d`, then rea-agents 6.5.0 via `node <pkg>/scripts/rea.mjs` (never `npx -y`, which rewrites the npx cache lock); REA refuses an address-level `decompile` on the packed bytes (`invalid_request`) and returns code after unpack | `tools/round-68/packed-elf.py` (sha256 `48ef4c68…`) — `carriers_matched 2` of `target 2`, `control_ok true`, every arm true on both carriers | scored receipt `.ufo/waves/round-68/l1/scores/` (after-arm at the measured revision) and route demonstration `.ufo/waves/round-68/l1/pre/c2-dryrun-at-base.json` (`before_procedures [3, 3]`; packed 3/3/3 and 3/3/6 against originals 167/30/190 and 99/29/103; refusal `0x103fa0` rc 1 → rc 0 with 4 841 B and `FUN_00103fa0`; originals rc 2 on `upx -l` and `upx -d`); entry `corpus/knowledge/2026-11-03-r68-packed-elf-route.md` (S269) |

Round-68 frontier note, 2026-11-03: packed-ELF triage is **Core** for the two pinned x86-64 carriers under UPX 5.2.0 (`2026-11-03-r68-packed-elf-route`; S269). Still Frontier: any packer other than UPX, an anti-UPX stub whose magic or entry is altered (no such carrier measured), packed PE/Mach-O, packed libraries and packed static binaries, and semantic equality of a recovered inventory (the route measures count equality only).
```
