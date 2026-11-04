# ExecC3 — scoped findings: R69-C3 carrier-class evidence, independently re-derived

Seat: ExecC3 (leaf verifier, wave r69-w1). Claim attacked as frozen: **R69-C3** (coverage — a pinned
packed shared-object carrier enters Core beside the two executables). Measured revision
`3f3d20fc065b5be62f676028b9a38d316ddfe8fd`; freeze `f15998102f1ce3569e61faa2ac6f286bc414538e`;
base `d7d9a62cc70935304e600ed0dee864fc4f1751f7`.

**Verdict: predicate met as written — observation, not inference.** Every clause was observed by this
seat driving `upx 5.2.0`, `readelf 2.47` and REA 6.5.0 itself, on bytes copied and measured here.
No recorded count, format, ratio, pin or packed hash disagreed with my derivation. Full command
transcript and tables: `.ufo/waves/round-69/w1/ExecC3/verify.md`; machine-readable numbers:
`.ufo/waves/round-69/w1/ExecC3/derivation.json`.

## What I ran (not reused from the route)

1. `/usr/lib/libz.so.1.3.2`: pin, `readelf -h`, `readelf -SW`/`-lW`, `upx --best`, `upx -l`,
   `readelf -SW` on the packed copy, `upx -d`, sha256 + `cmp` against the original, and three
   independent `rea analyze` runs (original / packed / recovered).
2. The same for the two executable carriers `jq` and `xxd`, because the predicate's ratio clause is
   "every carrier's".
3. A second shared object as a generalisation probe: `/usr/lib/liblzma.so.5.8.4` (pinned, packed,
   listed, unpacked, byte-verified, inventoried). Not claim input.
4. The landing receipt was **absent** (`.ufo/waves/round-69/l1/scores/` was empty), so I ran the
   frozen route to produce `.ufo/waves/round-69/w1/ExecC3/c3-at-landing-exec3.json` and scored it with
   `--check-receipt`.
5. The before-arm: `--check-receipt` over `.ufo/waves/round-68/l1/scores/c2-at-landing.json`.
6. Clause-strength probes of the frozen checker on three synthetic receipts in scratch.

## Independent numbers

| carrier | kind | pin (= host bytes) | orig counts | packed counts | recovered | packed sections | control `upx -l`/`-d` on orig | size | ratio (ceiling/orig) |
|---|---|---|---|---|---|---|---|---|---|
| jq | executable, `DYN (PIE)` | `e8156675…f7806` | 167/30/190 | 3/3/3 | 167/30/190 | 0 | 2 / 2 | 30800→14036 (45.57%) | 10/167 = 0.0599 |
| xxd | executable, `DYN (PIE)` | `7b1e5d0c…ae65` | 99/29/103 | 3/3/6 | 99/29/103 | 0 | 2 / 2 | 38928→19560 (50.25%) | 10/99 = 0.101 |
| **libz** | **shared-object, `DYN (Shared object file)`** | `6c78c5e5…075ca9` | **184/29/199** | **98/6/136** | **184/29/199** | 0 | 2 / 2 | 108560→65580 (60.41%) | **120/184 = 0.6522** |

libz specifics: 27 sections / 11 program headers original; 0 sections / 11 program headers packed;
`file(1)` "ELF 64-bit LSB shared object, x86-64, stripped"; unpack rc=0 and sha256 back to the pin,
`cmp` byte-identical; 27 sections restored. `upx -l` on the packed copy rc=0. The route's recorded
`packed_sha256` for **all three** carriers equals my own independently produced packed bytes
(jq `e8b6c9e7…`, xxd `1727faf9…`, libz `a9c544e6…`), so its artifacts are reproducible, not bespoke.

## Landing receipt and comparison

`.ufo/waves/round-69/l1/scores/c3-at-landing.json` did not exist, so the route was run by this seat:
`python3 -I -B tools/round-69/packed-elf.py --root … --rev 3f3d20fc… --pkg …/rea-agents --work <scratch>
--json-out .ufo/waves/round-69/w1/ExecC3/c3-at-landing-exec3.json` → rc 0.

Receipt: `target 3`, `carriers_matched 3`, `control_ok true`, `met_target true`, `failing []`,
`kinds ["executable","shared-object"]`, `before_ceilings` 0.0599 / 0.101 / 0.6522, packer
`upx 5.2.0` sha `cf2f6e7c…` with `pin_enforced true`, instrument sha `4ac0d83b…` at rev `616a5f2f…`.
`--check-receipt` on it → `met true`, rc 0.

Field-by-field against my derivation: pin, format (all four `elf_format` fields), packed section
count, `upx_list_rc`, ceiling and ratio, all three count triples, packed sha256, control rcs — **all
equal; no mismatch**. The three-carrier receipt is not merely self-consistent, it is reproducible from
the host bytes.

## Before-arm

`--check-receipt .ufo/waves/round-68/l1/scores/c2-at-landing.json` → `met false`, rc 1, `target 2`,
`carriers_matched 2`, `kinds [null]`, failing =
`["target 2 != 3", "carriers_matched 2 != 3", "no shared-object carrier: kinds [None]",
"jq: before_ceiling_ratio None > 0.75", "xxd: before_ceiling_ratio None > 0.75"]`.
The round-68 receipt has ids `["jq","xxd"]`, `carrier_classes null`, `kind_fields [null,null]`; the
round-68 instrument's `CARRIERS` has two entries and no `kind`; the base tree has no `tools/round-69/`.
The before-clause is satisfied as written.

(Note: `.ufo/waves/round-69/l1/pre/c3-at-base.json` is a logged check output with the `+ python3 …`
command as its first line, not JSON; re-scoring it exits 2 — it cannot masquerade as a receipt. Its
content agrees with the run above.)

## Generalisation probe (not claim input)

`/usr/lib/liblzma.so.5.8.4`, pin `6e4dae5b099ec0e40a56beead2e51f858535aa794b5a8574a6723dfc1da8a3c1`:
ELF64 `DYN (Shared object file)`, 27 sections / 11 phdrs, 219344→127204 bytes (57.99%), packed
sha256 `2acab019…`, 0 sections packed, `upx -l` rc 0, `upx -d` rc 0 with sha256 equal to the pin and
`cmp` byte-identical, REA 417/29/227 → 175/6/177 → 417/29/227.

Two findings:

- The packed-shared-object cycle generalises beyond libz: a second, larger `.so` detects, lists,
  unpacks byte-identically and recovers its full inventory.
- **The stub ceiling is genuinely per-carrier, not per-class.** libz's 120-procedure ceiling leaves
  22 procedures of headroom over its 98-procedure stub; the same constant applied to liblzma would be
  false (packed 175 > 120). The transferable bound is the ratio: 98/184 = 0.5326 and
  175/417 = 0.4197, both ≤ 0.75. This is the number a future fourth carrier must re-derive, and it
  corroborates the route's declared-per-carrier design.

## Clause-strength probes of the frozen checker (synthetic, not claim input)

- `syn-met` (three carriers, arms true) → `met true`, rc 0.
- libz ratio set to 0.9 → `met false`, rc 1, failing exactly `["libz: before_ceiling_ratio 0.9 > 0.75"]`.
- all kinds set to `executable` → `met false`, rc 1, failing exactly
  `["no shared-object carrier: kinds ['executable']"]`.
- Renaming the shared-object carrier id to `not-libz` while keeping `kind: shared-object` still scores
  `met true`: the counter enforces the *class*, not the claim's parenthetical `(libz)` naming.
- A receipt mixing a missing `kind` with a string `kind` raises
  `TypeError: '<' not supported between instances of 'str' and 'NoneType'` at `sorted({…})`
  (packed-elf.py:292), exiting 1 with a traceback rather than a named clause or the route's typed
  exit 2.

## Risks / observations for the L1 (none blocks the claim)

1. **Counter is class-only, not carrier-identity-specific** (above). This receipt names `libz` because
   the frozen `CARRIERS` table does; the counter alone would accept any shared object. Advisory, not a
   predicate proposal.
2. **Mixed-kind receipts crash untyped** (above). Fails closed; neither frozen receipt can reach it
   (round-68 all `None`, round-69 all strings). Advisory for the instrument, not for this round.
3. **`before_ceiling_ratio` is declared-ceiling/original, not measured-packed/original** (0.6522 vs
   0.5326 for libz). The predicate names the declaration-level ratio, so the clause is met either way;
   recorded so the L1 does not over-read the number as a measurement of the stub. The measured
   relation is stronger, not weaker.
4. **`section_count` in the receipt is the packed count only.** The original's 27 sections / 11 phdrs
   are not carried in the receipt; they are real (verified here) but the receipt does not evidence
   them. If a future predicate wants original shape recorded, that is a round-N+1 design note.
5. Packer pin was observed enforced *and* equal to the host packer (`upx 5.2.0`, sha `cf2f6e7c…`); the
   instrument bytes at the freeze commit hash identically to the current bytes, and
   `git diff f1599810..HEAD` over `tools/round-69/*.py` is empty — no post-freeze edit.

## Tooling, blockers, cleanup

- Tools installed: **none**. Only `upx 5.2.0`, GNU binutils 2.47, `jq`, `git` and the pinned
  `node /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/scripts/rea.mjs` (6.5.0) were
  used; no pacman transaction was attempted.
- Blockers: none. No L0 question.
- Writes: this seat wrote only `.ufo/waves/round-69/w1/ExecC3/{verify.md,derivation.json,
  c3-at-landing-exec3.json}` and this report; scratch
  `/fast/scratch/hyaku/kaidoku-r69/ExecC3/` removed before yield. No tracked file, index, commit or
  jj/git state was touched **by this seat**.
- Observed concurrent activity (not mine, not reverted): during this seat's window the lane tree
  gained `M PROVINCE.md`, `M corpus/README.md`, `M corpus/SOURCES.md`,
  `?? corpus/knowledge/2026-11-03-r69-packed-route-contract.md` and `?? corpus/lessons/round-69.md`
  (mtimes 23:36:20–23:38:19; `git diff --stat HEAD` = 13 insertions, 2 deletions). None of these
  paths was opened for writing by this seat; they are sibling-seat landings. The L1 should attribute
  them to their authors, not to ExecC3. `git rev-parse HEAD` remained
  `3f3d20fc065b5be62f676028b9a38d316ddfe8fd` throughout.
- Retained evidence: the route receipt (rc 0), `verify.md` (commands + tables + the base/after checker
  outputs), `derivation.json` (independent numbers, before-arm, probes, verdict).
