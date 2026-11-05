# Round 98 — lesson: a frontier class moves only through the packer's own gate, and an allow-list is checked against what its producer emits

Base `d0aebc288621b0072ac3eb2a79a62ad26bfa837a`. Freeze `69c581c7ca0c4ea2b58303669aab3700797277f9` (claims `plans/round-98-claims.md`, frozen counters `tools/round-98/pe-upx-tamper-battery.py` and `tools/round-98/allowlist-check.py`, do-nothing control `tools/round-98/controls/identity-copy.py`, control receipts `.ufo/waves/round-98/pre/`). Candidate landing `72346895a35a74af18151b125934fa0c09fe1e3c` (`tools/round-98/upx-pe-repair.py`, `tools/round-98/stop-boundary-repair-battery-v8.py`); both claims measured at `72346895`.

## Motive

Every owned axis sits at 10.0 and the stagnation nudge applies (AXES.md): the round takes a frontier → core move. The round-92 frontier note names "PE and Mach-O packed inputs" as still Frontier (`corpus/README.md`, round-92 note); every UPX class the lane holds is ELF. Separately, the round-97 non-author closure ruled calibration harmed: the landed v7 counter's nine-key allow-list refuses the verdict's fourteen-key counts on every honest public run (`corpus/lessons/round-97-verifier-spotcheck.md` §7 item 1). C1 takes the frontier; C2 repairs the harm.

## Verdict first

- **R98-C1 — verified on the frozen predicate, with a named discrimination limit.** At `72346895` the frozen battery prints `recovered 18 of 18; intact 6 of 6; refused 2 of 2; effective 18 of 18`, exit 0 (`.ufo/waves/round-98/l1/scores/c1-at-72346895a35a74af18151b125934fa0c09fe1e3c.json`); reproduced in a clone by ExecReproC1. Both do-nothing controls fail it (identity `recovered 0 of 18`, held ELF repair `recovered 0 of 18; intact 0 of 6`). Limit: the same battery admits three forgeries the critic seat built — a size-keyed cache that never reads its input, a lazy anchor without checksum/uniqueness, a validated fixed-offset patch (`w1/CriticC1.md` f2/f7/f1h) — because all six carriers share one layout (PackHeader at 992) and the battery has no held-out carrier. Substance outside the frozen predicate: 48 of 48 out-of-population tamper cells recovered on three unpinned win32/pe carriers under four pack modes (`w1/ExecHeldOut.md`), and the candidate refuses a checksum-valid decoy that the lazy-anchor forgery accepts (CriticC1 V2).
- **R98-C2 — verified on the frozen predicate, with a named discrimination limit.** At `72346895` `legs passed 4 of 4; public 1; real14 1; stub9 1; extra 1`, exit 0 (`.ufo/waves/round-98/l1/scores/c2-at-72346895a35a74af18151b125934fa0c09fe1e3c.json`, `counts_source` = the public receipt v8 wrote, not the fallback); reproduced by ExecReproC2; the v7 control scores `legs passed 1 of 4`. The v7→v8 diff is confined to the allow-list, `TOOL`, the selftest fixture/case and docstrings (ExecReproC2, ReviewerV8). Limit: the `public` leg trusts the candidate's printed `selfverify ok=True`, so a counter that lies on stdout (CriticC2 F2/F3) or a length-only `count_problems` (F5) is admitted, and an inverted `ok` survives because an in-place mutant's dirty tree always adds `byte-pin-not-bound:counter` (MutationC2 M6).

## Gate

Sources (CORPUS.md rule 1; access date 2026-11-05, opened in this round):

| row | source | URL | access date | located quote (≤25 words) | decision |
|---|---|---|---|---|---|
| S324 (new, admitted, tier A) | UPX 5.2.0 `src/pefile.cpp` (`PeFile::canUnpack0`) | https://raw.githubusercontent.com/upx/upx/v5.2.0/src/pefile.cpp (sha256 `6783a926f339b8fa5051c3c0c105c078655513d96ca4bb0f94c74315911379fa`; copy `.ufo/waves/round-98/pre/s324-pefile-v5.2.0.cpp`; ScoutSources' independent fetch has the same sha256) | 2026-11-05 | "if (memcmp(isection[0].name, "UPX", 3) == 0) { // current version fi->seek(isection[1].rawdataptr - 64, SEEK_SET); found_ph = readPackHeader(1024);" (lines 3167-3170) | **admit**: the packer's own PE unpack gate; grounds the name test and the PackHeader windows of R98-C1's repair rule |
| S325 (new, rejected, tier C) | "Unpacking Modified UPX", hardly programming | https://blog.hardlyprogramming.com/posts/Unpacking-Modified-UPX/ (sha256 `f1b7c347…1e402`; copy `.ufo/waves/round-98/pre/s325-hardlyprogramming-fetch.html`) | 2026-11-05 | "Breaking the ability to use the upx -d command is suprisingly easy. Simply changing 1 byte in the packed binary is enough." (22 words) | **reject**: names no tampered field and remedies by dynamic unpacking (x64dbg), not by a structure the packer checks; flip in the row |
| (not appended) | ScoutSources drafts S325–S328 | packhead.cpp and pefile.cpp again (same URLs as S308/S324 → within-scope duplicate URLs, E04), `p_w64pe_amd64.h`, JPCERT anti-UPX (ELF-scoped) | 2026-11-05 | in `w1/ScoutSources.md` | not appended: duplicates are cited through S308/S324; the header and JPCERT rows are cited by no admitted entry (CORPUS.md rule 4) |

Search log: question — which structure does UPX 5.2.0 test before it unpacks a PE, and where? Identified 6 (four UPX source files, two third-party write-ups), screened 6, included 1 new row, rejected 1, 4 not appended (reasons above). Stop rationale: the gate's own source states the test and the window.

Census before → after (`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku`): before exit 0, `kaidoku ok`, 228 registry rows (`.ufo/waves/round-98/pre/census-start.txt`); after exit 0, `kaidoku ok`, 230 rows (`.ufo/waves/round-98/l1/census-end.txt`).

## Mistakes

Each row: class · evidence pointer · captured-by · fix.

- **M98-a · false absence: an input probed at the wrong root (own, rounds 93–97).** `corpus/lessons/round-93.md:47`, `round-94.md:42`, `round-95.md:23`, `round-96.md:43`, `round-97.md:108` say `merge/kaidoku/` is absent; the package the prompt names, `/home/vgpnk/Projects/shokuknow/merge/kaidoku/`, exists (`MERGE-REPORT.md` mtime 2026-10-24 23:33, before all five rounds; `test -e /home/vgpnk/Projects/shokuknow/merge/kaidoku; echo $?` → `0`, run 2026-11-05). Captured-by: none (no criterion required the absolute path or the probe). Fix: QUALITY Row 198; shown able to fail — applied to the five lines it fails all five. The five lessons are not rewritten; this round states the package's presence and takes no assimilation (see `## Assimilation`).
- **M98-b · an allow-list derived from the label, not the producer (round 97, M97-j; closure routed defect 1).** v7 `COUNT_KEYS` nine keys vs `v3.score` fourteen (`tools/round-97/stop-boundary-repair-battery-v7.py:55-56`; `.ufo/waves/round-97/l1/public/v7.err`). Captured-by: none in round 97 (the frozen honest leg fed a stub). Fix: v8 allow-list equals the producer's fourteen keys, and QUALITY Row 199's two legs (`real14`, `stub9`) in the frozen counter; shown able to fail — the v7 control scores `legs passed 1 of 4; public 0; real14 0; stub9 0; extra 1` (`.ufo/waves/round-98/pre/c2-v7-control.json`).
- **M98-c · a preflight that read the tail of the output (own, this round, caught before data).** The first draft of `pe-upx-tamper-battery.py` reused `run()`, which keeps the last 400 bytes, for the `upx --version` check, so both controls exited 2 (`preflight: upx version 'A SDK version 4.43…'`). Captured-by: the controls' own exit 2 before any candidate existed. Fix: the version check reads the full stdout (frozen bytes at `69c581c7`).
- **M98-d · a seat's prose contradicts its own receipt (wave, ExecReproC1).** `w1/ExecReproC1.md` §4 says `upx -d` of the untampered pack "reproduced the original carrier byte-for-byte (`ref_equals_carrier: true`)"; its own `w1/ExecReproC1/hand-cells.json` records `"ref_equals_carrier": false` for every cell, and the lane's measurement agrees (t32 `6b4195e6…` vs unpack `2a300a74…`). Captured-by: the L1 reading the receipt, not the prose. Fix: the knowledge entry cites the receipt value; seat prose is never evidence without its receipt.
- **M98-e · both frozen counters were frozen with a do-nothing control but no forgery battery (own).** CriticC1 f2/f7/f1h and CriticC2 F2/F3/F5 (+ MutationC2 M6) meet the frozen labels. Captured-by: none before freeze (§9 asks for the cheapest do-nothing control; neither counter had a pre-freeze forgery arm). Fix: routed — round 99's successor counters carry the wave's forgeries as committed red fixtures scored before freeze; not yet shown able to fail, so not counted here.
- **M98-f · a reviewer seat ended without its report (wave, ReviewerRepair).** `r98-w1-results.json` holds its output, which stops mid-probe; no `w1/ReviewerRepair.md` exists. Captured-by: the L1's results read. Not replaced (a dead seat stays dead); its partial note (a short read can reach `decodePackHeaderFromBuf` with `blen < 20`, where UPX throws and the tool does not) is recorded, unverified.

## Measured

| claim | before (control, at base `d0aebc28`) | after (at `72346895`) | command |
|---|---|---|---|
| R98-C1 | identity: `recovered 0 of 18; intact 6 of 6; refused 0 of 2; effective 18 of 18` exit 1; held ELF repair: `recovered 0 of 18; intact 0 of 6; refused 2 of 2; effective 18 of 18` exit 1 | `recovered 18 of 18; intact 6 of 6; refused 2 of 2; effective 18 of 18` exit 0 | `python3 -I -B tools/round-98/pe-upx-tamper-battery.py --repair-cmd <cmd> --work <scratch> --json-out <receipt> --rev <rev>` |
| R98-C2 | v7: `legs passed 1 of 4; public 0; real14 0; stub9 0; extra 1` exit 1 | v8: `legs passed 4 of 4; public 1; real14 1; stub9 1; extra 1` exit 0 | `python3 -I -B tools/round-98/allowlist-check.py --counter <counter> --rev <rev> --work <scratch> --json-out <receipt>` |

Harm check: coverage proxy (`tools/round-66/coverage-selfcheck.py --selfcheck`, stem recipe) 175 of 181 at base → 176 of 182 at `9cb93001` (both 9.67; the new entry is mapped; `.ufo/waves/round-98/l1/scores/coverage-selfcheck-at-*.json`); depth rule blocks 36 resolved at both (same receipts, `recipe_a`). The base receipt shows a **pre-existing calibration mismatch**: the SCORECARD coverage head claims 10.0 and 168/168, observed 175/181 — the r93–r97 entries are indexed but unmapped. Not repaired here (not claimed); routed to round 99.

## Wave `r98-w1` — seat results

Dispatch `.ufo/waves/round-98/r98-w1-dispatch.json` (validated under `ufo-wave-policy.json`, `counts {spawn 13, total 13}`, band 8–16), ready `.ufo/waves/round-98/r98-w1.ready`, dispatched in tranches (`r98-w1.ready.dispatched`); results `.ufo/waves/round-98/r98-w1-results.json` (13 settled). Roles: executor 3, scout 1, scribe 1, connector 1, reviewer 2, critic 2, mutation-tester 2, sentinel 1; attack seats (reviewer, critic, mutation-tester) 6 of 13. Reports in `.ufo/waves/round-98/w1/`.

- **ExecReproC1** — frozen C1 label and both controls reproduced in a clone at L; three hand-built cells recovered (prose error M98-d).
- **ExecReproC2** — v8 selftest 24/0, v7 23/0; C2 label and v7 control reproduced; diff confined.
- **ExecHeldOut** — 48/48 out-of-population cells recovered on three unpinned win32/pe carriers × four modes; ARM64 PE unpackable by UPX 5.2.0; truncated packs ≥ `c_len` reported `ok intact` (routed).
- **ScoutSources** — S324 bytes independently equal; four further drafts (not appended, see Gate); S325 reject drafted.
- **ScribeEntry** — corrections integrated into the entry: the arch-split refusal message, the unexercised section-2 branch, the 992 monoculture, ARM64/.NET as pack-time refusals (S324 lines 141-142, 2207-2208, re-read by the L1).
- **ConnectorOverlap** — the round-98 note supersedes the PE half of the round-76/77/92 clauses; zero sibling lanes hold UPX-PE knowledge; v6 and v7 carry the nine-key list, v8 fourteen.
- **ReviewerV8** — v8 COUNT_KEYS equals `v3.score`'s emitted set (read and run); the fallback counts source can mask a stdout-lying candidate; routed defect 2 is open and was not named in the plan's not-claimed list (ReviewerV8 F2; acknowledged here).
- **CriticC1** — three admitted forgeries (M98-e); `effective` is real for the named reasons; the first `UPX!` is the PackHeader on every sample.
- **CriticC2** — three admitted forgeries (M98-e).
- **MutationC1** — 12 mutants, 7 killed, 5 survive (version range, window length, uniqueness, prefix, `.rsrc`/`UPX2` choice), all with byte-identical output on the frozen population: population blind spots.
- **MutationC2** — 14 mutants, 13 killed (8 only through the dirty-tree byte-pin confound), M6 survives.
- **SentinelInputs** — 756 malformed inputs exit only 0 or 2, no traceback, max 0.44 s; symlink victim survives; three CLI paths crash rc 1 (missing `--in`, missing `--out` dir, stale `<out>.tmp-<pid>`); a co-tamper of `dd[1].RVA` bytes 0–1 passes both the repair and `upx -t` and unpacks to a different program (the packer's own blind spot; the repair claims only the packer gate, routed as a limit).
- **ReviewerRepair** — settled without a report (M98-f).

## Assimilation

`Assimilation: none` — the package `/home/vgpnk/Projects/shokuknow/merge/kaidoku/` exists (`test -e` exit 0; 132 staged rows from 2026-10-24, `MERGE-REPORT.md`) but this round's claim cap is spent on the PE frontier and the routed calibration repair; no entry is adopted and no staged row appended. The lane has no `considerthese/` directory (`test -e /home/vgpnk/Projects/shokunin/kaidoku-shokunin/considerthese; echo $?` → `1`). No `corpus/lessons/operator-*.md` exists.

## Routed defects from the round-97 closure

1. Allow-list = verdict's key set with a red stub fixture — closed by R98-C2 (v8; `stub9` leg and selftest case `verify-catches-nine-key-stub`).
2. Honest leg runs the real public battery — the round-97 kill rule `kill-rule-v3.py` is not amended, so the defect is open; R98-C2's `public` leg runs the real public battery for v8 but trusts its printed verdict (CriticC2 F2/F3). The plan's not-claimed list omitted this item (ReviewerV8 F2).
3. `ownrec` measured slot — open (kill rule not amended).
4. Imported pins at the named revision; absent file a typed refusal — open (v8 inherits v7's binding unchanged).
5. K-ownrun recursion bound and a K-cwd leg that can fail — open.
6. Before-side receipts from a clean checkout of the base — partly answered: this round's before-side controls ran at base `d0aebc28` with only the uncommitted frozen counter and control present; the candidate did not exist.
7. Local-source gate FAIL on S082, S302, S321 — open (pre-existing debt).

## Corrections (append-only)

The round-92/76/77 frontier notes are not rewritten; the round-98 frontier note supersedes the "packed PE" half of their clause for the bounded class only.
