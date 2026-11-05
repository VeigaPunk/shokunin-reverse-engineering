# Round 89 — a wrong-value `b_info.sz_cpr` is the same redundancy as a zeroed one (R89-C1 met 4 of 4; R89-C2 met 29 of 29)

Base `0ec2bb4016655f605657d6e0e700ec2e6893ac27`; declaration `9da6c980` (plan, three instruments, base and
control receipts); freeze `4ab027b2` (container; prefreeze gate CLEAN at `18b6a2a4` with its red control);
block 29 and its cell receipt `8bbb40cc`. The round-88 non-author spot-check
(`corpus/lessons/round-88-verifier-spotcheck.md`) is the input: its routed defects D1–D4 and D6 shaped the
round, and its §9 promotion note is not a promotion.

Claim: **R89-C1** (coverage, capability — the wrong-value field class enters Core): `recovered 4 of 4`,
`N1`/`N2`/`N3`/`isolation` true, round-88 class regression `4 of 4`, exit 0
(`.ufo/waves/round-89/pre/c1-candidate-at-declaration.json`); the unchanged round-88 repair scores 0 of 4 on
the same population with every control true (`pre/c1-base-r88-repair.json`). **R89-C2** (depth): craft rule
block 29 lands and `tools/round-89/depth-blocks-v2.py --expect-blocks 29` reports `blocks 29, resolved 29,
unresolved []`, where the base arm is red at 28 and a citation-only stub is red by the shape floor.

## Mistakes

| id | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| M89-1 | a superseding repair that did not compose the class it superseded: the first candidate scored `recovered 4 of 4` on its own class with every control true while the round-88 class regression arm was unmet (`recovered 0 of 4`), because it derived the field without running the round-87 anchor path first, so a magic-tampered carrier was returned unchanged | `.ufo/waves/round-89/pre/c1-candidate-first-run.log` (`recovered 4 of 4 … met=False exit=1`); the composed repair's selftest case `magic-class-composed` | the pre-freeze candidate run — no QUALITY criterion asked for it, so `none` at the time; QUALITY 161 is written from it this round | `repair()` runs the anchor path first, falls back to the derivation on the original bytes when that walk refuses, and re-validates the corrected bytes through the anchor path; the regression arm is part of the frozen predicate, not a no-harm sentence. Shown able to fail: the first-run receipt above |
| M89-2 | a frozen instrument's docstring documents the rule its code falsified (round-88 spot-check D1): `tools/round-88/upx-chain-repair.py:13-18` still says "the smallest offset above `block0 + 12` … prefers candidates whose `l_info` carries `p_filesize == PackHeader.u_file_size`", while `:70-78` makes that equality a hard precondition and `:136` keys on `(fits, total, -derived)` | round-88 spot-check §7 D1; the round-88 lesson's M88-3 records the same rule as wrong | QUALITY 162 (written this round) — the pre-existing bar had no docstring-vs-code clause; M88-6 corrected a plan sentence, not the file | QUALITY 162 requires the docstring to state the code's rule at the same revision; the round-88 bytes stay frozen (they are a measured instrument), so the correction lands as a criterion and as the round-89 module's own docstring, which states the accounting key and the stored-value-blind gate |
| M89-3 | a depth counter whose target lived in prose (round-88 spot-check D3): `tools/round-88/depth-blocks.py` reported `met_target true` and exit 0 at the base state (27 blocks) and on a one-line citation-only stub (28 blocks) | `pre/c2-depth-at-base.json` (28 blocks, expect 29, met false, exit 1) and `pre/c2-control-stub-world.json` (`blocks 29, resolved 28`, the stub refused by the shape floor, exit 1) — the same two worlds the round-88 counter passed | QUALITY 157 (round 88) | `tools/round-89/depth-blocks-v2.py` requires `--expect-blocks N`, computes `met_target = blocks == N and resolved == blocks and not unresolved`, and declares the shape floor; both red worlds are committed receipts |
| M89-4 | a counter that left the answer beside the input (round-88 spot-check D4): the round-88 battery wrote `packed`/`n3.out` into the repair's input directory, so a sibling-copy repair scored 4 of 4 with zero packer probes | `tools/round-89/upx-field-battery.py` `apply_repair` (one `mkdtemp` per invocation, only `in` written) and its `isolation` control, which `met` requires; the control's listing is in every case receipt | QUALITY 163 (written this round from D4 + M88-8) | each invocation sees exactly one path; the round-88 sibling-copy cheat cannot see its sibling. Shown able to fail: the control reports the listing it observed, and the frozen `met` is false when any listing is not `["in"]` |
| M89-5 | a round that landed instruments without registry rows: the round-88 record names `tools/round-88/upx-chain-repair.py` and `upx-chain-battery.py` in SCORECARD and in the decision table, but neither carried an `<!-- instrument-registry -->` row | `grep -c "round-88" SKILL.md` at the round-89 base → 2 matches, neither a registry row (row 47 is the decision-table row, row 719 is craft block 28) | R85-2 / QUALITY 151's neighbourhood — the pre-existing criteria bind a *registered* row's command, not the registration itself; `none` for this case | both round-88 instruments and the three round-89 instruments now carry registry rows; the row text says the round-88 pair is registered late (this row), not that the round-88 record claimed it |
| M89-6 | the packer's refusal string is not a class key: `b_info corrupted` covers a zeroed `sz_unc` and a zeroed `sz_cpr`, `header corrupted` covers `sz_cpr = sz_unc + 1`, and the recoverable in-range wrong value answers a *third* text, `compressed data violation` | `.ufo/waves/round-89/l1/scores/block29-cells.json` (nine classes, two carriers, verbatim messages) and `pre/c1-base-r88-repair.json` `precondition.tail` (four carriers, `compressed data violation`) | QUALITY 156 (round 88) covered the two-field `b_info corrupted` case; the third text was new | QUALITY 164 and craft block 29: the class is defined by the tamper's value domain and the arm that decides it, never by the message |
| M89-7 | "tolerated" is not "a no-op", and not "harmless to the lane": a tampered `l_info.version` or `l_info.format` passes `upx -t` (rc 0, `Tested 1 file.`) yet breaks this lane's own locator, which cross-checks those bytes | `l1/scores/block29-cells.json` (`l_info.version^=0xFF`, `l_info.format^=0xFF`, rc 0 on both carriers); the repair refuses both | QUALITY 154 (round 88) defined `noop` as "the bytes were already equal", which does not cover a tolerated-but-consumed field | QUALITY 165 and block 29's last clause: report the cell as tolerated, name the consumer that does care, refuse it |

## Gate

Sources opened 2026-11-04 by the L1 (`curl`, HTTP status and byte count recorded). The scout seat's
independent fetch is in `w1/ScoutUpxSrc/`.

| source | decision | opened 2026-11-04 | located quote and judgment |
|---|---|---|---|
| S311 UPX v5.2.0 `src/p_lx_elf.cpp`, https://raw.githubusercontent.com/upx/upx/v5.2.0/src/p_lx_elf.cpp | **admit** (code, tier A, new row; same URL as S307, different scope → census W04) | HTTP 200, 373743 bytes, sha256 `551fc8675a59493793f59b64eb8bb9cc208a34f701ccd2bda8c9aaafb228d2dc`; lines 7060-7068 (the `l_info`/`p_info`/`b_info` header read), 7098 (`unpackExtent(sz_elf_hdrs, …)` peek), 7105 and 7308 (`throwCantUnpack("corrupt b_info");`) | lines 7096-7104: "Peek: unpack into ibuf, but do not write" then "if (sz_block1 < sz_elf_hdrs)"; the throw is the block walk's short-peek test, so the message names the walk, not one field |
| S312 UPX v5.2.0 `src/p_unix.h`, https://raw.githubusercontent.com/upx/upx/v5.2.0/src/p_unix.h | **admit** (code, tier A, absent → mined; scope corrected in-round to the **NE32** copy, old→new below) | HTTP 200, 6651 bytes, sha256 `73bd992ec0fb46022e299ec4b2cd696545412453a654573e6246034cf4881a88`; NE32 `packed_struct(b_info)` lines 109-111, NE32 `packed_struct(l_info)` line 118, NE32 `packed_struct(p_info)` line 126 with `NE32 p_progid;` 128, `NE32 p_filesize;` 129, `NE32 p_blocksize;` 130 (LE32 twin 192-204, BE32 160-171) | line 126: "packed_struct(p_info) { // 12-byte packed program header" with `p_progid`/`p_filesize`/`p_blocksize`; grounds why `u_file_size` sits twelve bytes after `l_magic` and `b0` is `l_info + 20` |
| UPX v5.2.0 `src/headers.h` (re-checked) | **reject — unchanged** (no row; round-88 rejection stands) | HTTP 404 | the path does not exist at tag `v5.2.0`; `src/packhead.h` is where the struct lives. Flip: the file appears at a later tag |
| UPX v5.2.0 `src/p_unix.cpp` (re-opened) | **reject — unchanged** (no row; round-87 rejection stands) | HTTP 200, 24181 bytes, sha256 `bf83c413…` | its `corrupt b_info` checks live in `PackUnix::unpack`; the shared-object carriers unpack through `PackLinuxElf64::un_shlib_1`/`PackLinuxElf32::un_shlib_1` (S311), so r87's flip condition ("a carrier class unpacked through the base class") is still unmet |

Status changes: S311 and S312 absent → mined, used-by
`corpus/knowledge/2026-11-04-r89-binfo-field-value-class.md` (both new rows, no recheck change to an
existing row). Recheck cadence 180d (tag-pinned URLs). Census before exit 0, 215 rows
(`pre/sources-census-before.txt`) → after exit 0, 217 rows, one new W04 (S311 vs S307, cross-scope).

**S312 scope correction, in-round (logged old→new).** The row was first written against the LE32
`packed_struct(p_info)` copy (`src/p_unix.h:200-203`) because that is the variant the file's third
block shows. The scout's tier-A adjudication (`w1/ScoutUpxSrc.md` §3) traces the carriers'
class chain — `PackLinuxElf64amd : PackLinuxElf64Le : PackLinuxElf64 : PackLinuxElf : PackUnix`
(`src/p_lx_elf.h:518,489,315,40`) — so the **NE32** copy (lines 109-130) is the one in force, and the
LE32 copy belongs to `PackUnixLe32`, reached only by `PackLinuxI386` (`linux.exec/i386`). Old scope:
"the little-endian `packed_struct(p_info)` … the LE32 copy"; new scope: "the **NE32**
`packed_struct(p_info)` … not the LE32 copy (reached only by `PackLinuxI386`/`PackUnixLe32`)". The
anchor cell's line numbers moved with it (126/128/129/130, with the twins named), the id, status,
opened date, recheck and used-by are unchanged, and the census still exits 0 with the same single W04.
The same adjudication keeps `src/headers.h` rejected (404 at `v5.2.0`; the tree's only
`*headers.h*` path is `src/util/system_headers.h`) and adds `src/packhead.h`'s limit: it contains no
`b_info` at all, so S309 is cited for the PackHeader fields only, never for the block layout.

**Sourced claim.** R89-C1's knowledge entry cites S311 and S312, both opened this round (§2b item 4).

**Assimilation: none.** `merge/kaidoku/` was not consumed this round (two-claim budget plus the
frontier step); no package entry was opened. No `considerthese/` directory exists in this lane.

## Wave `r89-w1` — seat results

## Wave `r89-w1` — seat results

Fourteen seats in one v1 wave (dispatch 21:42, results `r89-w1-results.json`). What the delivered
seats established:

- **ExecGeomIndep** (independent derivation, stdlib only, no import of the round-87/88/89 tools):
  derived block-0 `sz_cpr` = jq 252, xxd 249, libz 201, docker-init 226 — the round-88 record values —
  and **16 of 16** cells agree with `upx-field-value-repair.py --info` across four inputs (intact,
  `:= 0`, `:= true-8`, `:= 0xFFFFFFF0`). Ablation: the stored word is never read by any walk or gate; a
  mutant that leaves it in place refuses two classes and returns the wrong candidate (136) on
  docker-init, so reading it *would* change the result.
- **ExecMatrix** (field-class matrix, 48 cells = 4 carriers × 12 classes, exit 0, 0 skipped): every
  wrong-value `sz_cpr` class (zero, `true±8`, `0xFFFFFFF0`, `sz_unc+1`) is recovered on all four
  carriers; `sz_unc := 0`, `p_filesize` and the PackHeader class are refused; `method` and
  `p_blocksize` are out of the repair's remit (`repair rc 0`, `repaired_tests_clean false`). The
  `sz_unc+1` message is carrier-dependent: `header corrupted` on jq/xxd/dinit, `corrupt b_info` on libz
  (QUALITY 166).
- **ExecMutation** (28 single-anchor mutants, 14 per instrument, on the declared bytes): the mutant
  table and its survivors are the round's declared-case evidence for the instruments' guards.
- **ExecRegress88** (no-harm): the round-88 class through the round-89 repair `recovered 4 of 4` with
  its nested round-87 regression `8 of 8` (204.9 s); the round-87 class with the round-87 repair
  `8 of 8` (135.2 s); four selftests green (33/11/6/22 cases, failures 0); the `--no-rea` ablation
  differs only in the `rea_recover` arm.
- **ScoutUpxSrc**: eleven URLs opened with HTTP status/bytes/sha256 and a release-tarball cross-check;
  tier-A adjudication traced the carriers' class chain (`PackLinuxElf64amd : PackLinuxElf64Le :
  PackLinuxElf64 : PackLinuxElf : PackUnix`) and showed that the **NE32** `p_unix.h` copy is the one in
  force — which corrected S312's scope in-round — that `src/packhead.h` contains no `b_info` at all,
  and that `src/headers.h` is a 404 at the tag.
- **ReviewerC2** (attack on C2): re-derived both arms (base 28/28 expect 29 red, worktree 29/29 green at
  the block-29 commit), added a negative target control (`--expect-blocks 28` → red), six red worlds
  (stub, one-span, past-EOF, absent-doc, duplicate, fenced), the floor sweep (blocks 1-28: 39-2,902
  words, 2-354 spans, none below the floor), and separability (block 29 cites only base-present
  documents). Findings: duplicate and fence blindness (no live instance), `--worktree` trusts the moving
  tree, and MED-1 (the container named a matrix path that did not exist at review time).
- **ReviewerC1** (attack on C1): reproduced the frozen predicate at both repair revisions (`4 of 4`,
  met, exit 0); scored seven cheap rules — the round-88 sibling copy 0 of 4 (N3 false), three packer
  oracles 4 of 4 with the regression arm unmet except the full-range oracle with the round-88 locator,
  which **meets** the predicate, `stored + 8` 4 of 4 with N3 false, a `stored`-reading hybrid gated by
  `upx -t` which **meets** the predicate, and `u_len` arithmetic 0 of 4. Defects: the isolation
  control snapshots before the run (D1), the repair pin is recorded but not compared (D2), the counter
  does not force the technique (D4), the tamper population is one offset (D5), the repair reads the
  stored value to *classify* (D6 — the derivation is blind, the classification is not).
- **SentinelR89** (hostile inputs, cost, receipt integrity): twelve hostile-input classes; the
  declared-bytes repair hung on a FIFO, raised `MemoryError` on `/dev/zero`, and let the round-87
  `Refused` escape as a traceback on every plain LE ELF; `--out`/`--info` accepted `..` and absolute
  paths, and a planted `<out>.tmp` symlink was followed. All of it is fixed in the two in-round
  revisions. Cost: Θ(N · ph_off), measured 8.4 s at 800 candidates and 125.5 s at 3,200 (15× for 4×),
  with the 12,800 point left as an unmeasured extrapolation at the seat's yield.
- **ConnectorR89**: no sibling lane holds this ground (`sz_cpr`/`sz_unc`/`stored-value-blind`/`chain
  geometry`: 0 hits across 20 sibling lanes).
- **ScribeEntry / ScribeBlock29 / ScribeLesson**: the entry draft (101 lines, every number
  receipt-backed), the block-29 revision candidate (399 words, 55 spans, base-present citations only),
  and the QUALITY rows — three of which (the guard-set, the isolation snapshot and the rank-key rows)
  were verified by that seat first-hand and are integrated as Rows 169-171.

Unverified partial findings carried into the routed list, not admitted: CriticClaims and MutationR89
wrote no report in this wave; their attack duty is covered by ReviewerC1, ReviewerC2, SentinelR89 and
ExecMutation, and the two empty seats are reported as dead in the round report.

