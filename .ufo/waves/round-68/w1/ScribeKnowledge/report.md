# ScribeKnowledge — round-68 w1 scoped findings

## Drafted

- `.ufo/waves/round-68/w1/ScribeKnowledge/entry.md` — 17,435 B, 105 lines, prose only, target repo path
  `corpus/knowledge/2026-11-03-r68-packed-elf-route.md`. It carries: a predicate-shaped `status:` line
  (Core iff the frozen counter at the measured revision reports `carriers_matched 2` of `target 2`,
  `control_ok true`, every arm true, both packed carriers at 3 procedures, originals neither listed nor
  decompressible); two `source:` lines citing **S269 first**; `verified-at:`; `recheck:`; the route arm
  table; the identity rule and the manual's `--exact` bound; the two carriers; the two do-nothing
  controls; the counter-boundary paragraph; `## Limits`; `## Unknowns`; `## Evidence`; and two separate
  fenced blocks — the `## Coverage map` row and the `## Round-68 additions to Core` row plus frontier note.
- `.ufo/waves/round-68/w1/ScribeKnowledge/upx-doc.txt` — the S269 object, 37,208 B, sha256
  `4dc547edc7201f205ce904f373518b6fcaef608d5aafd8a4a7564d42993b8c42`.
- `.ufo/waves/round-68/w1/ScribeKnowledge/upx-doc.pod` — the same manual's pod form at the same tag,
  35,451 B, sha256 `cc93ccea8e9e9f4721b1b1cd983d960deea432c7d4913f1efe35f33d2a1c31c2`.
- `.ufo/waves/round-68/w1/ScribeKnowledge/SHA256SUMS` — those two digests.
- This report. No tracked lane file was edited; nothing was committed, pushed, or run through `jj`.

## What this seat verified (observation)

1. **Frozen instrument.** `sha256sum tools/round-68/packed-elf.py` = `48ef4c68…` (matches the stated
   pin). `python3 -I -B tools/round-68/packed-elf.py --selftest` printed
   `{"selftest": "...", "cases": 13, "failed": [], "ok": true}` and exited 0.
2. **Base absence.** At `fcbe200f6739c38939e0dabf3f251de2cc6bd727`, `git cat-file -e
   fcbe200f:tools/round-68/packed-elf.py` exits 128 (`exists on disk, but not in …`); `git ls-tree -r
   --name-only fcbe200f -- tools | grep -i 'pack\|upx'` returns nothing; `git grep -n -i upx fcbe200f --
   PROVINCE.md SKILL.md tools` returns only `PROVINCE.md:62` (the host-fallback-readers row).
3. **Route receipt** (`.ufo/waves/round-68/l1/pre/c2-dryrun-at-base.json`, read, not re-run):
   `closure {carriers_matched 2, target 2, control_ok true, met_target true}`, `failing []`,
   `before_procedures [3, 3]`; `jq` original `167/30/190` vs packed `3/3/3`; `xxd` original `99/29/103` vs
   packed `3/3/6`; refusal `packed_rc 1`, `packed_error_code invalid_request`, `unpacked_rc 0`,
   `unpacked_code_bytes 4841`, `symbol_present true`; `control {list_rc 2, decompress_rc 2}` on both;
   packed sha `e8b6c9e7…` (jq) and `1727faf9…` (xxd).
4. **Controls receipt** (`.ufo/waves/round-68/l1/pre/controls-at-base.json`): six arms green;
   `c2-packed-only` and `c2-no-identity` both report `carriers_matched 0`, `met_target false`; `c2-real`
   reports 2 / true. **Skip-run** (`.ufo/waves/round-68/l1/pre/c2-skiprun.json`): `closure null`,
   `verdict_claimed false`, `met_target null`, instrument sha `ff11d8ec…`.
5. **Host spot checks, measured 2026-11-03.** `/usr/bin/xxd` is a symlink to `/usr/bin/tinyxxd`
   (sha256 `7b1e5d0c…`); `upx -l /usr/bin/xxd` exits 1 with `IOException: is a symlink -- skipped`, while a
   dereferenced copy of the same bytes gives `NotPackedException` rc 2 on `upx -l` and rc 2 on `upx -d`
   with nothing written. `upx -l /usr/bin/jq` and `upx -d /usr/bin/jq` both exit 2 with
   `NotPackedException` and write nothing. `readelf -SW` counts 28 section headers on `/usr/bin/jq` and 27
   on `/usr/bin/xxd`; both headers say `DYN (Position-Independent Executable file)`, `Advanced Micro
   Devices X86-64`. The packed copies' section count in the receipt is 0 for both. Ownership and sizes:
   `pacman -Qo` → `jq 1.8.2-1`, `tinyxxd 1.3.17-1`, `upx 5.2.0-1`; `stat -L` → 30,800 B and 38,928 B.
6. **Source locators and digests.** `upx-doc.txt` at tag `v5.2.0`: 37,208 B, `4dc547ed…`; ELF386 sentence
   "Packed programs will be byte-identical to the original after uncompression." (10 words) at fetched-bytes
   lines 441-442, byte offset 18,963; general passage at lines 383-384 (offset 16,437); `--exact` at lines
   101-106; `-d` at 73-75; `-l` at 84-88. `upx.pod` at the same tag: 35,451 B, `cc93ccea…`; general passage
   at lines 459-461 (offset 15,849), ELF386 at line 521 (offset 18,219). Installed man page (decompressed
   `upx.1`): 40,077 B, `09552b3c…`, the sentence at line 263.
7. **Current S269 row.** `corpus/SOURCES.md:186` (working tree) is the plain-text form at tag `v5.2.0`,
   37,208 B, sha256 `4dc547ed…`, quote at lines 441-442 — the same object my first `source:` line cites.

## Sibling state and conflicts (reported, not resolved here)

- **S-id changed under the seat.** When this seat first read the working tree, the added S269 row named
  `doc/upx.pod`; it was later re-anchored to `doc/upx-doc.txt` (same tag, `4dc547ed…`). The ScoutSource seat's
  `.ufo/waves/round-68/w1/ScoutSource/gate.md` registers a second row **S270** for the same txt file pinned at
  commit `034b6d0d81c53998c07ad6f34bfead6f5c5445ce` and states, verbatim: "If the L1 prefers one row per source
  family, fold the ELF386 line into S269's anchor cell and drop S270; nothing else changes." At this seat's last
  read, `grep -c '^| S270 ' corpus/SOURCES.md` = 0 — S270 is **not** in the registry. My draft therefore cites
  S269 only (txt form first, pod and man-page forms as further locators of the same manual). If the L1 lands
  S270, the second `source:` line can be re-pointed to it; no quote or number changes.
- **Landed coverage-map row is misfiled.** In the working tree `corpus/README.md:271` sits between the last
  Lessons row (`| round-51 | 51 | …`, line 269) and `## Frontier`; it has three cells and no `verified-at`,
  so it is not a `## Coverage map` row (three cells: topic | entry | verdict) and not a `## Knowledge` row
  (four cells: entry | topic | source | verified-at). The fenced row in my draft is the `## Coverage map`
  shape and does not move any existing line.
- **Landed entry vs this draft.** `corpus/knowledge/2026-11-03-r68-packed-elf-route.md` exists in the working
  tree (5,757 B, mtime 22:48) and is not this draft. My draft is the house-style superset: `status:` /
  `source:` / `verified-at:` / `recheck:` header lines, the S269 txt anchor with pod and man-page locators,
  the counter-boundary paragraph (the dryrun's `instrument.sha256 7ee286c0…` is not the frozen `48ef4c68…`;
  its `rev` is `main` and `instrument.rev` is null), the measured 28/27 section counts on the originals, the
  `/usr/bin/xxd` symlink nuance, the `Limits`/`Unknowns` split, and the two fenced row blocks.
- **ExecPacked's third-carrier probe** exists at `.ufo/waves/round-68/w1/ExecPacked/probe.json` (gzip:
  original `230/31/235`, packed `3/3/7`, all five arms true per its own JSON; an lzma-packed variant also
  recorded; `helper_sha256 48ef4c68…`). It is outside the frozen claim's two carriers and this seat did not
  re-run it; the entry does not use it.

## Not verified by this seat (unknown)

- **The scored after-arm.** At this seat's last read `.ufo/waves/round-68/l1/scores/` contains only
  `c1-at-landing.json`; no `c2-at-*.json` existed. The R68-C2 predicate reads that receipt, so this seat has
  not observed it. In particular it is unknown here whether the after-arm reproduces `before_procedures [3, 3]`
  and whether it records a commit in `rev` and a non-null `instrument.rev` (atom A9).
- **The route end-to-end.** This seat read the committed receipts and ran only the pure `--selftest`; it did
  not re-run `upx`/REA over the carriers.
- **Packed-byte reproducibility across runs** (UPX determinism) — not tested.
- **The C1 census and the four registry rows** (R68-C1) — outside this seat's reading.
- **Mutation bats and the control re-run** (MutPacked, MutRegistry, ExecControls) — not read.

## Out of scope / not done

- No tracked lane file was created or edited, no registry row, no commit, no push, no `jj` command, no
  subagent dispatch. The knowledge entry, the two rows, and the S269/S270 decision belong to the L1.

## Tools installed

None. No package manager transaction was run (pacman is paused host-wide); no tool was needed beyond the
pre-installed `python3`, `curl`, `/usr/bin/upx` 5.2.0, `readelf`, and `node`.

## Scratch

`/fast/scratch/hyaku/kaidoku-r68/ScribeKnowledge/` was created for the fetches and the two `upx` control
probes; its two source copies were copied into the wave dir first, and the scratch tree is removed before
this seat yields.
