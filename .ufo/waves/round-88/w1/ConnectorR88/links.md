# ConnectorR88 — cross-lane and cross-source links (round 88, kaidoku)

Seat: ConnectorR88 (leaf, read-only scan). Scan at `2026-11-04T20:16-03:00`, lane HEAD
`01ffb9376ad7692141f641c5dc99bbcbb7788b21` (live worktree: siblings committing during the scan —
`d190c5b57 → 6d235a4cf → 01ffb9376`; `tools/round-88/field-tamper-matrix-v2.py` staged mid-scan).
Base `0cf8e3243059e0bc510b90c880d13d191e78d732`. No lane file outside this seat dir was written;
no git/jj mutation; nothing installed.

Scan commands (exact):

```
grep -rlE '(\bUPX\b|\bupx\b|sz_cpr|\bb_info\b|NotPackedException|CantUnpackException|CantPackException)' \
  --include='*.md' --include='*.py' --include='*.sh' --include='*.json' --include='*.c' --include='*.txt' \
  /home/vgpnk/Projects/shokunin            # every lane, kaidoku excluded by filter
grep -rlnE 'packed-ELF|packed ELF|packed-elf' --include='*.md' /home/vgpnk/Projects/shokunin
grep -ln 'packed-ELF\|UPX' /home/vgpnk/Projects/shokunin/*/PROVINCE.md
python3 -I -B tools/round-88/depth-blocks.py --root . --worktree
python3 -I -B tools/round-88/depth-blocks.py --root . --rev HEAD
```

---

## 1. Sibling lanes — what exists on packed-ELF / UPX / refusal triage

**No sibling lane holds an instrument, a Core row, or a claim on packed-ELF structure.** The
token sweep returns 6 non-kaidoku files with real content; none is a packed-ELF tool, none is a
knowledge entry on UPX structure, and `grep -ln 'packed-ELF\|UPX' */PROVINCE.md` matches only
`kaidoku-shokunin/PROVINCE.md`.

| path | what it is | verdict |
|---|---|---|
| `revenger-shokunin/reports/round-73/tool-probes.md:82-83` | `upx --version` → `upx 5.2.0`; `upx -t /usr/bin/true` → rc 2 `NotPackedException: not packed by UPX` | **Only sibling record of the refusal string.** A tool-availability probe, not triage. Does not duplicate C1/C2; corroborates C2's `NotPackedException` label on plain input (= round-68's negative arm) from an independent seat. |
| `revenger-shokunin/reports/round-73/scout-packs/ReFrameworkTargets.md:13-14` | GoReSym README (commit `722897e0`, tier A, status mined): "malformed unpacked binaries, such as from UPX" | **Same law, opposite angle** — a third-party tool warns that UPX-unpacked output can be malformed, where C1's identity arm proves the restored bytes are the pin. Not a contradiction; it bounds *unpacked* output, not *restored* output. |
| `game-dev-3d-shokunin/reports/round-102/adversary/F6.md:54` | a `pacman -S … upx …` install line | No knowledge. Not a link. |
| `tameshi-shokunin/.ufo/waves/round-32/w1/CtlRegionDiff.md:276,744` | a base64 blob whose text contains `UPX!` | False-positive class: the token is inside encoded bytes. Not a link. |
| `kumitate-shokunin/.ufo/waves/round-81/w1/K81ConnOverlap-captures/grep-05-admission.txt:123-131` | raw capture of `kaidoku-shokunin/tools/round-69|70|71/packed-elf.py` paths from a broad admission sweep | A sibling *reading* kaidoku's instruments; no verdict line, no claim. Confirms no sibling admission of the same ground. |
| `mado-shokunin/.ufo/waves/round-81/w1/R81ConnSiblings/sweep-a-layer.txt:25` | broad sweep hit on `tsukuroi/.ufo/waves/round-39/.../blocks.json` | Unrelated (pacman transaction log). |
| `tsukuroi-shokunin/.ufo/waves/round-19/l1-capture/siblings/kaidoku/*/PROVINCE.md`, `…/round-50/w1/R50*Siblings/*kaidoku*` | snapshots of *this* lane's PROVINCE | Copies, not independent sources. |

**Verdict on duplication: R88-C1 and R88-C2 duplicate no sibling instrument, entry or Core row.
No sibling contradicts either claim.** The nearest neighbour is revenger's round-73 RE-toolbench
ledger, which owns "installed tool + one probe per tool", not packer structure.

## 2. Cross-link into the lane's packed-ELF corpus (rounds 68–73, 87)

| entry | relation to the new class | verdict |
|---|---|---|
| `corpus/knowledge/2026-11-03-r68-packed-elf-route.md` | The route's first step is `upx -l` rc 0; a zeroed `sz_cpr` makes `upx -l`/`-d` exit 2, i.e. r68 reads the file as "not packed". C1 inserts a repair **before** `upx -d`; C2 replaces "rc 2 means not packed" with a 10-label taxonomy. | **Extended, not contradicted.** r68's negative arm (`NotPackedException` on plain input) is preserved as a distinct label. |
| `corpus/knowledge/2026-11-03-r69-packed-route-contract.md` | r69's typed exit-2 classes are REA/tool-side (`missing_tool`, `packer_mismatch`); C1 adds packer-structure refusals (`not a little-endian ELF`, `no validated PackHeader`, `no sentinel`); C2's vocabulary is the packer-side complement. | **Extends the same contract pattern on a different subject.** No conflict. |
| `corpus/knowledge/2026-11-04-r70-provenance-bound-receipts.md` | C1's counter records the repair sha256 **and** the composed r87 module sha256 per record; the four carriers are r70's pinned table. | **Extended** (composition is a new producer-binding case). |
| `2026-11-04-r71-registry-grammar.md`, `…-r72-checker-env-capsule.md`, `…-r73-kernel-witness-record.md` | receipt grammar, child-env capsules, kernel witness | **Not extended.** Orthogonal to packer structure; C1/C2 make no runtime-evidence claim. |
| `corpus/knowledge/2026-11-04-r87-upx-magic-tamper-repair.md` | **Primary extension.** `PROVINCE.md:686-695` leaves "tampering of PackHeader/l_info/p_info/b_info fields other than the magic" **Frontier**; C1 moves the `b_info.sz_cpr` slice of that clause to Core. Entry `:123` measured negative (T2 + `p_info.p_filesize` zeroed → unrepaired) is the neighbouring cell C1 still does **not** repair. Entry `:100` (a chain-walk-free heuristic also scores 8/8, M87-3) is the overstatement risk C1 answers with four falsified cheaper rules (ReviewerC1 R1–R5: 3/4, 3/4, 3/4, 0/4, 0/4). | **Direct extension of a declared Frontier clause**; no rewrite of the r87 text. |
| `corpus/knowledge/2026-11-04-r74…r86-*.md` | receipt/mutation/registry lineage | Not extended. |

**PROVINCE Core row touched.** `PROVINCE.md:666-695` — the *Round-87 additions to Core* bullet
(`:668`) and its frontier note (`:686`), specifically the sentence
"Still Frontier: … tampering of PackHeader/l_info/p_info/b_info fields other than the magic"
(`:690-691`). The landed successor is `PROVINCE.md:697-720` (*Round-88 additions to Core*): the
`b_info`/`sz_cpr` bullet moves that slice to Core (`:699`), and the refusal matrix is filed
**Held, not Core** (`:710`) — the correct disposition, since the matrix routes but does not repair.
No sibling PROVINCE holds a competing row.

## 3. Contested scope, and the same law from other angles

**Contested scope: none.** No sibling lane claims packed-ELF structure, UPX repair, or
refusal-signature triage. `revenger-shokunin` is the only RE lane with a UPX record and it is a
tool-probe ledger (round 73), not a capability claim; it neither blocks nor overlaps C1/C2.

Sources teaching the same law from a different angle:

1. **S307 `src/p_lx_elf.cpp:8065`** "if (sz_cpr != UPX_MAGIC_LE32) // sz_cpr must be h->magic" —
   the *unpacker check* angle on the same field C1 derives from *layout* (next block at `12 + sz_cpr`).
   One source, two laws: the sentinel test is what makes C1's candidate search terminate.
2. **S310 `src/packer.cpp:544-546`** — `c_len > u_len` raises "header corrupted" before any checksum
   is consulted: the packer-side reason C2's `header-corrupted` label exists (35 of 68 cells).
3. **GoReSym README** (`revenger-shokunin/reports/round-73/scout-packs/ReFrameworkTargets.md:13`) —
   "malformed unpacked binaries, such as from UPX": the *consumer* angle, warning that unpacked
   output is not automatically well-formed. C1's identity arm is the stronger guarantee on the four
   pinned carriers; it does not generalise to carriers outside the four.
4. **`revenger-shokunin/reports/round-73/tool-probes.md:83`** — the refusal string observed from a
   *CLI probe on a plain file*; C2 observes the same string family from a *tampered field*.

## 4. Findings that bear on the claims (all measured this scan)

- **F1 — the `b_info corrupted` label does not select the repair.** In
  `.ufo/waves/round-88/l1/scores/c2-matrix-at-declaration.json` the `b0-sz_cpr` cell is
  `b-info-corrupted`, `upx_t_rc 1`, `upx_d_rc 1`, `identity false` on **4 of 4** carriers — this
  independently corroborates C1's before-state. The `b0-sz_unc` cell carries the **same** label,
  same rcs, same `identity false` on 4 of 4. **Measured, not inferred** (probe receipt
  `.ufo/waves/round-88/w1/ConnectorR88/sz-unc-probe.json`, one scratch `upx --best` pack of the
  pinned `jq`, `b0` 576, `sz_unc` 904, `sz_cpr` 252, `u_len` 30800, sentinel 13988):

  | tamper | `upx -t` | exception | `upx-chain-repair.py` | restored |
  |---|---|---|---|---|
  | `b0-sz_unc` zeroed | rc 1 | `b_info corrupted` | **rc 2, refused**, nothing written | — |
  | `b0-sz_cpr` zeroed | rc 1 | `b_info corrupted` | rc 0, derived `sz_cpr 252`, accounted 30800/30800 | `upx -t` 0, `upx -d` 0, sha256 `e8156675…` = the jq pin |

  The repair refuses the `sz_unc` case because `geometry()` skips any candidate with
  `sz_unc0 == 0` (`if sz_cpr0 != 0 or sz_unc0 == 0: continue`, `upx-chain-repair.py:109`) and the
  composed round-87 anchor repair refuses first (`p_info is not followed by a plausible b_info`).
  **A block that maps `b_info corrupted` → chain-geometry repair mis-routes half the cells carrying
  that label.** The signature must be paired with the field (or with a repair that refuses cleanly),
  never with a single move. *Unique to this seat — ReviewerC2 keyed on carrier dependence, not on
  intra-label field ambiguity.*
- **F2 — the signature is carrier-dependent, not field-dependent.** `l-checksum` →
  `tolerated` on jq/xxd/dinit but `bad-seek` on libz; `ph-filter` → `header-corrupted` on 3 carriers
  but `noop` on libz (already `0x00`). Credited: ReviewerC2 §Attack 3. A field→label table is wrong.
- **F3 — "closed 7-label vocabulary" is falsified by the round's own passing evidence.**
  `plans/round-88-claims.md:60-61` says "68 cells, closed 7-label vocabulary". The passing
  instrument is v2 with `VOCAB` of **10** labels (`field-tamper-matrix-v2.py:87-89`, selftest
  `len(VOCAB) == 10`); the receipt shows 68 cells, **63 effective**, 5 `noop`, 0 unclassified,
  `per_class` over 10 classes, exit 0. The plan is frozen and unamended; `claims.json`
  `instrument_supersessions` says "labels … unchanged" while the label set changed 7→10.
  The block must state 10, not 7.
- **F4 — v2 is pinned by commit, not by sha256.** `claims.json.instruments` still sha256-pins only
  v1 (`0e055486…`); the supersession entry names v2's commit `6d235a4cf` and v1's sha, but not v2's
  own sha256 (`9386711b…`, present only in the receipt `tool_sha256`). The plan says instruments are
  "pinned by sha256 in claims.json".
- **F5 — S309/S310 are cited but not yet in the source table.** `corpus/knowledge/2026-11-04-r88-binfo-chain-geometry.md:3-4`
  cites S309 (`src/packhead.h`) and S310 (`src/packer.cpp`); `PROVINCE.md:703` cites S309.
  `corpus/SOURCES.md` max row is **S308** (`grep -c 'S309'` = 0, `S310` = 0). Dangling at scan time —
  the V87-2 class. A scribe seat may still land the rows; the census command is
  `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku`.
- **F6 — the repair docstring states a preference the code does not implement.**
  `tools/round-88/upx-chain-repair.py:17` says "Candidates whose `l_info` carries
  `p_filesize == PackHeader.u_file_size` are preferred". The ranking key is
  `(fits, total, -derived)` (`:136`) with no `p_filesize` term, and `l_info_candidates()` already
  *requires* `p_filesize == u_file_size` of every candidate (it searches for those exact four bytes),
  so the "preference" is vacuous. The implemented rule **matches the plan exactly**; only the prose
  overstates. Unique to this seat.
- **F7 — the depth counter cannot distinguish base from target.** `met_target = not unresolved`
  (`depth-blocks.py:89`); at the base 27/27 it reports `met_target: true`, exit 0. Measured now:
  worktree `blocks 28, resolved 28, unresolved []`; at HEAD `01ffb937` `blocks 27, resolved 27`.
  The `28` is read from the `blocks` field by the reviewer, not enforced by the exit code. Not a
  defect of the claim (the kill rule names `resolved < 28`), but a limit of the counter.

## 5. State at scan close

- Block 28 **has landed in the worktree** (`blocks 28, resolved 28, unresolved []`, measured
  `20:16:20-03:00`) but **not at HEAD** `01ffb937` (27/27). C2's measured revision must be the
  commit that carries it.
- `corpus/knowledge/2026-11-04-r88-binfo-chain-geometry.md` exists (6888 B, mtime 20:07) and is
  cited by `PROVINCE.md:709`.
- `tools/round-88/field-tamper-matrix-v2.py` is staged (index blob `c4e541a7…`, mode 100644 vs v1's
  100755) and is not at HEAD `01ffb937`; it is at `6d235a4cf` per the supersession entry — verify at
  the measured revision.
