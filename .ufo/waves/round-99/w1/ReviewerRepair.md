# ReviewerRepair — surgical review of `tools/round-99/upx-pe-repair.py` at L vs round-98 (R99-C2)

Lane: kaidoku round 99. Rev L = 01c4b79cc1cf8e6172b507edebb6a4d3125c5c6f; base tool `tools/round-98/upx-pe-repair.py` (same rev, unchanged there).
Method: read both sources in full; `git diff --no-index` (+54/−14, 1 file); then executed both tools side by side on the battery's ten sha256-pinned carriers (all 10 pins verified OK) across every battery cell class plus adversarial header attacks, with per-run directory snapshots to catch temp leftovers. Harness + raw receipts: `.ufo/waves/round-99/w1/ReviewerRepair/` (parity-receipt.json 135 cells; probe2/probe3-receipt.json; parity_harness.py).

## Claim-by-claim verification (all commands run; exit codes recorded in receipts)

1. **Parity: same decision, same bytes** — VERIFIED on the frozen-population shapes.
   - 72 cells where both tools wrote `--out`: sha256 identical in 72/72 (intact 10, tamper magic/names/both 30, decoy 9, overlay 20, nsec+1 2, t64+falign3 1). stdout identical (`ok magic@992,name0,name1` …); `--json` output identical byte-for-byte.
   - 40 truncated cells: r99 rc 2, no `--out`, `truncated: file N bytes < aligned end of last section M` in stderr (numbers match independent computation). r98 on `end-1` cuts repaired (rc 0) — the claimed carve-out; on `upx1-mid` cuts r98 also refused rc 2 (`packheader-candidates:0`, because `ph_ok`'s `c_len <= len(b)` fails) — same decision class, different reason string. Battery predicate (rc 2 + "truncated") unaffected.
   - REFUSE arm (t64, winhello originals): both tools rc 2 `packheader-candidates:0`, no output. Identical.
2. **Only new refusals are truncated / filealign-zero / CLI** — VERIFIED.
   - New refusal strings vs r98: `truncated: …`, `filealign-zero`, and the CLI envelope (`input-unreadable`, `output-is-directory`, `output-dir-missing`, `output-write-failed`). Nothing else added; shared refusals (`not-mz`, `not-pe`, `sections`, `packheader-candidates:N`) are code-identical.
   - filealign-zero matches the oracle: falign=0 pack → `upx -t` rc 1 (S324 `unpack0`: `throwCantUnpack("unexpected value in the PE header")`); r99 refuses rc 2; r98 wrongly "ok intact" rc 0.
   - CLI deltas: r98 exits 1 with Traceback on missing-in / missing-outdir / out-is-dir / readonly-outdir / in-is-dir; r99 exits 2 with typed refusals, no Traceback, nothing created (snapshot-checked). In-place `--in == --out`: both rc 0, identical bytes.
3. **Write path leaves no temporary on any error** — VERIFIED structurally and empirically.
   - Code (L174–189): `mkstemp` in the `--out` dir → write/flush/fsync → chmod 0644 → `os.replace`; `except OSError → refuse("output-write-failed")`; `finally: unlink tmp` unless replaced. Covers mkstemp failure, write/fsync failure, chmod failure, replace failure.
   - Empirics: 135 cell runs + 11 probes, directory snapshot before/after each run: zero `*.tmp-*` files anywhere, including readonly-outdir (mkstemp fails → rc 2 "output-write-failed: Permission denied", empty dir) and out-is-dir. No Traceback in any r99 run.

## Assigned axes

- **FileAlignment offset +36 (L83)** — CORRECT for PE32 and PE32+. `pe + 24 + 36` without Magic branch; SectionAlignment/FileAlignment sit at optional-header offsets 32/36 in both 0x10B and 0x20B (the diverging fields ImageBase/BaseOfData are below 32). Empirically honored on t32 (PE32) and t64 (PE32+): falign=0 refused on both; falign patches changed behavior on both.
- **ALIGN_UP arithmetic (L93)** — exact-division `(v + a − 1) // a * a` in Python big ints. Equals UPX 5.2.0's `((v)+(a)-1) & ~((a)-1)` iff falign is a power of two. See Finding L1.
- **Last section in table order vs highest raw end (L92)** — `secs[-1]`, exactly matching S324 `unpack0`: `overlay = file_size_u − ALIGN_UP(isection[iobjs−1].rawdataptr + isection[iobjs−1].size, ih.filealign)`; S326 `checkOverlay` throws iff `(int) overlay < 0 || overlay > file_size_u` ⇔ aligned end > file size. r99 refuses iff `len(b) < end` (L94–95) — the same predicate, boundary-inclusive (end == size accepted, like overlay 0). Using max-raw-end would have diverged from the packer; it does not.
- **Integer overflow on huge rawdataptr/size** — no crash possible (Python big ints). C-side 2^32 wrap never produced an oracle-accepted input in my probes: rptr=0xFFFFFE00, rptr=2^32−rsize (clean wrap to overlay=file_size), rsize=0xFFFFFF00 on t32/t64 → `upx -t` rc 1 on all (packer refuses the tampered last section for its own reasons), r99 refuses "truncated" — direction-consistent with the oracle; r98 accepted all four (rc 0, wrote bytes), so r99 is strictly closer to oracle behavior on these attacks.
- **n sections > what the file holds** — two sub-cases, both parity-clean. (a) NumberOfSections+1 where the table still fits in header padding (t32/t64): both rc 0 "ok intact", identical bytes (phantom header is zero padding → secs[-1] end 0); note `upx -t` refuses these (rc 2) — retained round-98 behavior, unchanged by r99, no parity impact (see L2). (b) true table-beyond-EOF (n+8, file cut inside the table, 919 bytes): both rc 2 `refused: sections`, no output (shared guard L80).

## Findings by severity

**L1 (low, fidelity/wording — no frozen-cell impact): non-power-of-2 FileAlignment makes the L93 ALIGN_UP diverge from the packer, in an input-dependent direction.**
UPX's formula is align-up only for pow2 `a`. With falign=3 on t32: `upx -t` rc 0 (accepts) but r99 refuses `truncated` (end 58881 > 58880) while r98 repaired — an over-refusal vs the oracle on a full-length file, outside the claim's literal carve-out. With falign=3 on t64 the aligned end lands exactly on 64512: both tools accept, byte-identical. falign=0xFFFFFFFF: oracle rc 0 on both packs, r99 refuses. None of the frozen cells tamper FileAlignment (all packs keep 512), so the R99-C2 predicate is untouched; but the claim sentence "for every input … whose length is not truncated" only holds under the reading "truncated = the tool's own aligned-end predicate" (circular for these 3 cells). Suggested (optional, non-frozen): scope the L90–95 check to pow2 falign — the only regime where it implements the cited rule — or add a qualifier to the claim wording.

**L2 (low, observation — retained round-98 coverage gap, unchanged in r99): phantom-section "ok intact".** A pack with NumberOfSections bumped into header padding is "ok intact" for BOTH tools while `upx -t` refuses (rc 2). Parity holds (identical bytes), so this is not an r99 defect; recorded as a candidate future coverage cell.

No medium/high findings. Static screen: zero FORBIDDEN tokens in the candidate (battery `static` cell reproduces locally: hits []).

## Residual risk / verification gaps

- `atk-swap-sec23` (out-of-raw-order sections) never ran: all 10 packs have exactly 3 sections, my n≥4 guard skipped it. Table-order fidelity is established by source identity (`secs[-1]` ↔ `isection[iobjs-1]`), not by an executed swap cell.
- I could not construct a 2^32-wrap cell the oracle accepts (3 shapes tried, all refused by upx) — absence of a counterexample is not proof; surface = header-tampered last section only, unexercised by frozen cells.
- Non-OSError exceptions during the write block (e.g., KeyboardInterrupt, MemoryError) hit `finally` (temp removed) but exit 1 with traceback — outside the "no other exit status is intended" docstring; same residual as r98, not exercised.
- r98-vs-r99 `--json` refusal envelope compared on one cell only; success-path JSON compared exactly (identical).

## Environment

Ran with python3 3.14.8 (`-I -B`), `/usr/bin/upx` 5.2.0. No tools installed or upgraded (none needed); pacman untouched. All work in clone `/fast/scratch/hyaku/kaidoku-r99/ReviewerRepair/clone` (toplevel verified) and my scratch; lane writes limited to `.ufo/waves/round-99/w1/ReviewerRepair/` and this report. Scratch deleted after receipt copy.

**Verdict:** r99 tool is a byte-faithful successor of r98 on the claimed surface — 72/72 identical outputs, new refusals exactly truncated/filealign-zero/CLI, zero temp leakage; one low finding (L1, non-pow2 falign ALIGN_UP divergence, unexercised by frozen cells) and one retained-behavior observation (L2).
