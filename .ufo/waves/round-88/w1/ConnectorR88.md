# ConnectorR88 — cross-lane and cross-source pattern scan (round 88, kaidoku)

Seat: ConnectorR88 (connector, leaf — no dispatch). Read-only scan of
`/home/vgpnk/Projects/shokunin/*-shokunin` plus the lane's own packed-ELF corpus.
Scan window `2026-11-04T20:07–20:19-03:00`. Lane HEAD at scan start
`d190c5b57`; at scan close `01ffb9376ad7692141f641c5dc99bbcbb7788b21` (siblings were committing
during the scan). Base `0cf8e3243059e0bc510b90c880d13d191e78d732`.

No tool installed or upgraded. No git/jj mutation (read-only `log`/`status`/`ls-files`/`show`/
`cat-file`/`hash-object` only). No file written outside this seat dir and my scratch.

## 1. What I ran (exact commands)

```
grep -rlE '(\bUPX\b|\bupx\b|sz_cpr|\bb_info\b|NotPackedException|CantUnpackException|CantPackException)' \
  --include='*.md' --include='*.py' --include='*.sh' --include='*.json' --include='*.c' --include='*.txt' \
  /home/vgpnk/Projects/shokunin
grep -rlnE 'packed-ELF|packed ELF|packed-elf' --include='*.md' /home/vgpnk/Projects/shokunin
grep -ln 'packed-ELF\|UPX' /home/vgpnk/Projects/shokunin/*/PROVINCE.md
grep -n 'fields other than the magic\|Round-87 additions to Core\|Round-87 frontier note' PROVINCE.md
grep -c 'S309' corpus/SOURCES.md; grep -c 'S310' corpus/SOURCES.md
python3 -I -B tools/round-88/depth-blocks.py --root . --worktree
python3 -I -B tools/round-88/depth-blocks.py --root . --rev HEAD
python3 -c "json.load(.ufo/waves/round-88/claims.json)"          # instruments, pins, instrument_supersessions
python3 -c "json.load(.ufo/waves/round-88/l1/scores/c2-matrix-at-declaration.json)"   # per_class, cells_detail
diff -u tools/round-88/field-tamper-matrix.py tools/round-88/field-tamper-matrix-v2.py
```

Probe (one scratch `upx --best` pack of the pinned `jq`, then the repair on each tamper):

```
cp /usr/bin/jq work/orig && upx --best -q -o work/packed work/orig
python3 -I -B probe.py                    # r87 locators; zero 4 B at b0 and at b0+4
upx -t -q work/<f>-zeroed
python3 -I -B <LANE>/tools/round-88/upx-chain-repair.py --in work/<f>-zeroed --out work/<f>-fixed
```

## 2. Cross-lane: what exists

**No sibling lane holds an instrument, a Core row, or a claim on packed-ELF structure.** The token
sweep returns six non-kaidoku files with real content; `grep -ln 'packed-ELF\|UPX' */PROVINCE.md`
matches only `kaidoku-shokunin/PROVINCE.md`.

| path | what it is | verdict |
|---|---|---|
| `revenger-shokunin/reports/round-73/tool-probes.md:82-83` | `upx --version` → `upx 5.2.0`; `upx -t /usr/bin/true` → rc 2 `NotPackedException: not packed by UPX` | only sibling record of the refusal string; a tool-availability probe, not triage. **No duplication**; independently corroborates the `NotPackedException` label on plain input (round-68's negative arm) |
| `revenger-shokunin/reports/round-73/scout-packs/ReFrameworkTargets.md:13-14` | GoReSym README (commit `722897e0`, tier A): "malformed unpacked binaries, such as from UPX" | same law from the **consumer** angle; bounds *unpacked* output, not the *restored* bytes C1's identity arm measures. No contradiction |
| `game-dev-3d-shokunin/reports/round-102/adversary/F6.md:54` | `pacman -S … upx …` install line | not a link |
| `tameshi-shokunin/.ufo/waves/round-32/w1/CtlRegionDiff.md:276,744` | `UPX!` inside a base64 blob | false-positive class, not a link |
| `kumitate-shokunin/.ufo/waves/round-81/w1/K81ConnOverlap-captures/grep-05-admission.txt:123-131` | raw capture of `kaidoku-shokunin/tools/round-69|70|71/packed-elf.py` paths | a sibling *reading* kaidoku's instruments; no verdict, no claim |
| `mado-shokunin/.ufo/waves/round-81/w1/R81ConnSiblings/sweep-a-layer.txt:25` | broad sweep hit on a tsukuroi pacman log | unrelated |
| `tsukuroi-shokunin/.ufo/waves/round-19|50/…kaidoku*` | snapshots of this lane's PROVINCE | copies, not sources |

**Verdict: R88-C1 and R88-C2 duplicate no sibling instrument, entry or Core row, and no sibling
contradicts either claim.**

## 3. Cross-link into the lane's packed-ELF corpus

| entry | relation | verdict |
|---|---|---|
| `corpus/knowledge/2026-11-03-r68-packed-elf-route.md` | r68's detect step is `upx -l` rc 0; a zeroed `sz_cpr` makes `-l`/`-d` exit 2, so r68 reads the file as "not packed". C1 inserts a repair before `upx -d`; C2 replaces "rc 2 = not packed" with a taxonomy | extended, negative arm preserved as a distinct label |
| `corpus/knowledge/2026-11-03-r69-packed-route-contract.md` | r69's typed exit-2 classes are tool/REA-side; C1 adds packer-structure refusals; C2 is the packer-side complement | extends the same contract pattern on a different subject |
| `corpus/knowledge/2026-11-04-r70-provenance-bound-receipts.md` | C1 records repair sha256 **and** composed r87 module sha256 per record; carriers are r70's pinned table | extended (composition is a new producer-binding case) |
| `2026-11-04-r71-registry-grammar.md`, `…r72-checker-env-capsule.md`, `…r73-kernel-witness-record.md` | receipt grammar, child-env capsules, kernel witness | not extended; orthogonal |
| `corpus/knowledge/2026-11-04-r87-upx-magic-tamper-repair.md` | **primary extension**: `PROVINCE.md:686-695` leaves "tampering of PackHeader/l_info/p_info/b_info fields other than the magic" Frontier; C1 moves the `b_info.sz_cpr` slice. Entry `:123` (T2 + `p_filesize` zeroed → unrepaired) is the neighbouring cell still not repaired. Entry `:100` (chain-walk-free heuristic also 8/8, M87-3) is the overstatement risk C1 answers with four falsified cheaper rules (ReviewerC1 R1–R5: 3/4, 3/4, 3/4, 0/4, 0/4) | direct extension of a declared Frontier clause; r87 text unrewritten |
| `2026-11-04-r74…r86-*.md` | receipt/mutation/registry lineage | not extended |

**PROVINCE Core row touched:** `PROVINCE.md:666-695` — the *Round-87 additions to Core* bullet
(`:668`) and its frontier note (`:686`), specifically `:690-691` "Still Frontier: … tampering of
PackHeader/l_info/p_info/b_info fields other than the magic". Landed successor:
`PROVINCE.md:697-720` (*Round-88 additions to Core*), where the `b_info`/`sz_cpr` bullet moves that
slice to Core (`:699`) and the refusal matrix is filed **Held, not Core** (`:710`) — the right
disposition, since the matrix routes but does not repair. No sibling PROVINCE holds a competing row.

## 4. Contested scope and other angles

**Contested scope: none.** `revenger-shokunin` is the only RE lane with a UPX record and it owns a
tool-probe ledger (round 73), not packer structure; it neither blocks nor overlaps C1/C2.

Same law from a different angle:

1. **S307 `src/p_lx_elf.cpp:8065`** "if (sz_cpr != UPX_MAGIC_LE32) // sz_cpr must be h->magic" —
   the unpacker-check angle on the field C1 derives from layout; the sentinel test is what makes
   C1's candidate search terminate.
2. **S310 `src/packer.cpp:544-546`** — `c_len > u_len` raises "header corrupted" before any checksum
   is consulted: the packer-side reason C2's `header-corrupted` label exists (35 of 68 cells).
3. **GoReSym README** (revenger r73 row) — the consumer angle: unpacked output is not automatically
   well-formed.
4. **`revenger-shokunin/reports/round-73/tool-probes.md:83`** — the same refusal family observed from
   a CLI probe on a plain file, where C2 observes it from a tampered field.

## 5. Findings that contradict the claim or the plan

- **F1 (measured, unique).** `b_info corrupted` does not select the repair. Probe on one scratch
  `upx --best` pack of pinned `jq` (`b0` 576, `sz_unc` 904, `sz_cpr` 252, `u_len` 30800, sentinel
  13988): zeroing `b0-sz_unc` gives `upx -t` rc 1 `CantUnpackException: b_info corrupted` and the
  repair **refuses, rc 2, nothing written**; zeroing `b0-sz_cpr` gives the *same* `upx -t` message and
  the repair **rc 0, derived `sz_cpr 252`, accounted 30800/30800**, output passing `upx -t` and
  `upx -d` to sha256 `e8156675…` (the jq pin) and byte-identical to the clean pack. The matrix shows
  the same split across all four carriers (`b0-sz_unc` and `b0-sz_cpr` both `b-info-corrupted`,
  `identity false`, 4 of 4). Cause: `upx-chain-repair.py:109` `if sz_cpr0 != 0 or sz_unc0 == 0:
  continue`. **Bearing:** C2's block must not map the label `b_info corrupted` to one move; half its
  cells are refused by the repair it would name. Receipt:
  `.ufo/waves/round-88/w1/ConnectorR88/sz-unc-probe.json`.
- **F2 (credited: ReviewerC2 §Attack 3).** The signature is carrier-dependent: `l-checksum` →
  `tolerated` ×3, `bad-seek` on libz; `ph-filter` → `header-corrupted` ×3, `noop` on libz. A
  field→label table is wrong.
- **F3.** `plans/round-88-claims.md:60-61` says "68 cells, closed **7-label** vocabulary". The passing
  instrument is v2 with `VOCAB` of **10** (`field-tamper-matrix-v2.py:87-89`; selftest asserts
  `len(VOCAB) == 10`); the receipt reports 68 cells, **63 effective**, 5 `noop`, 0 unclassified, exit 0.
  The plan is frozen and unamended, and `claims.json.instrument_supersessions` states "labels …
  unchanged" while the label set changed 7→10. The block must state 10.
- **F4.** `claims.json.instruments` still sha256-pins only v1 (`0e055486…`); the supersession entry
  pins v2 by commit (`6d235a4cf`) and names v1's sha, not v2's (`9386711b…`, present only in the
  receipt `tool_sha256`). The plan says instruments are "pinned by sha256 in claims.json".
- **F5.** `corpus/knowledge/2026-11-04-r88-binfo-chain-geometry.md:3-4` cites S309 (`src/packhead.h`)
  and S310 (`src/packer.cpp`), and `PROVINCE.md:703` cites S309, but `corpus/SOURCES.md` max row is
  **S308** (`grep -c 'S309'` = 0, `'S310'` = 0). Dangling at scan time — the V87-2 class. A scribe
  seat may still land them; gate: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku`.
- **F6 (unique).** `upx-chain-repair.py:17` states a `p_filesize == u_file_size` **preference**; the
  ranking key is `(fits, total, -derived)` (`:136`) with no such term, and `l_info_candidates()`
  already *requires* that equality of every candidate. The implemented rule matches the plan exactly;
  only the prose overstates — the M87-3 failure mode, in miniature.
- **F7.** `depth-blocks.py:89` sets `met_target = not unresolved`, so at the base 27/27 it reports
  `met_target: true`, exit 0. Measured now: worktree `blocks 28, resolved 28, unresolved []`; at HEAD
  `01ffb937` `blocks 27, resolved 27`. The `28` is read from the `blocks` field by the reviewer, not
  enforced by the exit code. Not a defect of the claim (the kill rule names `resolved < 28`), but the
  counter cannot distinguish base from target on its own.

## 6. Measured numbers (this scan)

| quantity | value | source |
|---|---|---|
| matrix population / effective / noop / unclassified | 68 / 63 / 5 / 0, exit 0 | `l1/scores/c2-matrix-at-declaration.json` |
| matrix labels in the passing instrument | 10 (`header-corrupted` 35, `b-info-corrupted` 8, `b-info-corrupt-field` 4, `p-info-corrupted` 4, `compressed-data-violation` 4, `bad-method` 4, `bad-seek` 1, `tolerated` 3, `noop` 5) | same receipt `per_class` |
| v1 run on the same population | exit 1, `other-refusal` 5 (`b0-method` ×4, libz `l-checksum`) | `w1/ExecMatrix/matrix.json` |
| craft blocks, worktree / HEAD | 28 / 27, both `unresolved []` | `depth-blocks.py --worktree` / `--rev HEAD` |
| `b0-sz_cpr` cells | `b-info-corrupted`, `upx_t_rc 1`, `upx_d_rc 1`, `identity false`, 4 of 4 | declaration receipt `cells_detail` |
| `b0-sz_unc` cells | same class and rcs, 4 of 4 | same |
| probe: sz_unc zeroed | `upx -t` rc 1 `b_info corrupted`; repair rc 2 refused, no output | `ConnectorR88/sz-unc-probe.json` |
| probe: sz_cpr zeroed | `upx -t` rc 1 same text; repair rc 0, `sz_cpr 252`, 30800/30800; `upx -t` 0, `upx -d` 0, sha256 `e8156675…`, output = clean pack | same |
| SOURCES max row | S308; S309/S310 cited but absent | `grep -c` |

## 7. Files written

- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-88/w1/ConnectorR88/links.md`
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-88/w1/ConnectorR88/sz-unc-probe.json`
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-88/w1/ConnectorR88.md` (this file)

Scratch `/fast/scratch/hyaku/kaidoku-r88/ConnectorR88/` deleted after the receipts were written; no
cited value depends on it.

## 8. Limits

One scan at one worktree state; HEAD moved twice during it (`d190c5b57 → 6d235a4cf → 01ffb9376`) and
block 28 landed in the worktree at ~20:07, so every "landed/absent" statement above is timestamped,
not a verdict. The probe is one carrier (`jq`) and one pack mode (`--best`); the four-carrier claim
rests on the L1 receipt I read, not on my re-run. No sibling instrument was executed and no sibling
verdict is transferred. F3/F4/F5 are state-of-the-worktree observations that a scribe or L1 commit
may resolve; F1/F2/F6 are properties of the instruments and the sources themselves.
