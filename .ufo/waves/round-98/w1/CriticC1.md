# Round 98 · CriticC1 — falsify R98-C1 (packed PE UPX tamper repair)

Seat: CriticC1 (critic, leaf). Lane: kaidoku, L1 KaidokuR98. Clone of L = 72346895a35a74af18151b125934fa0c09fe1e3c
(`git -C $S/clone rev-parse HEAD` → `72346895a35a74af18151b125934fa0c09fe1e3c`; `--show-toplevel` = `$S/clone`).
Receipts: `.ufo/waves/round-98/w1/CriticC1/` (`out/` logs + JSON, `forgeries/` sources). Scratch removed on exit.

## Verdict
The real candidate reproduces the frozen label, but the frozen predicate **admits three forgeries** (f2, f7, f1h).
R98-C1 as frozen is met by the candidate; it is **not** a sufficient falsification-resistant coverage check.
Three defects are counter-side (no decoy arm, no input-derived check, no layout diversity). One coverage claim is over-reached.

## Reproduction (run, not inferred)
- `python3 -I -B clone/tools/round-98/pe-upx-tamper-battery.py --repair-cmd clone/tools/round-98/upx-pe-repair.py --work $S/w/base --json-out $S/out/base.json --rev 72346895…` → exit 0, `recovered 18 of 18; intact 6 of 6; refused 2 of 2; effective 18 of 18 met True`.
- Identity control (`controls/identity-copy.py`): exit 1, `recovered 0 of 18; intact 6 of 6; refused 0 of 2; effective 18 of 18` (matches frozen).
- `upx -t` on all 18 tampered cells: rc 1, reason `CantUnpackException: file is (possibly) modified/hacked/protected` (probe.log).
- Pack determinism: `upx --best` re-pack of each pinned carrier is byte-identical to the battery's pack (6/6 `repack_eq True`).
- UPX `pefile.cpp` v5.2.0 (fetched, 3341 lines) confirms the gate: `memcmp(isection[0].name,"UPX",3)`, PackHeader at `isection[1].rawdataptr-64` then `isection[2].rawdataptr`.
- Real repair output is byte-identical to the untampered pack for t32 and fastlist64 in magic/names/both, and the intact t32 is byte-identical (diag.log, cmp).

## Forgeries scored with the frozen battery (exit / label / predicate)
| id | repair | exit | label | admitted |
|---|---|---|---|---|
| identity | control | 1 | recovered 0 of 18; intact 6 of 6; refused 0 of 2 | no (control) |
| real | L candidate | 0 | recovered 18 of 18; intact 6 of 6; refused 2 of 2; effective 18 of 18 | **met** |
| f1 | fixed offset: `UPX!`@992, names UPX0/UPX1/UPX2, always exit 0 | 1 | recovered 18/18, intact 6/6, refused 0 of 2 | no (refuse arm only) |
| f2 | size-keyed cache of the six untampered packs; never reads input | 0 | 18/18; 6/6; 2/2 | **yes** |
| f3 | names-only (refuses unless a UPX-prefixed name exists) | 1 | recovered 0 of 18 | no |
| f4 | magic-only (structural anchor, names untouched) | 1 | recovered 6 of 18 | no |
| f5 | blanket refuser (exit 2) | 1 | recovered 0 of 18; intact 0 of 6 | no |
| f6 | `UPX!` over every zero dword, always exit 0 | 1 | recovered 0 of 18; intact 0 of 6; refused 0 of 2 | no |
| f7 | lazy anchor: first (format,version) match in window, no checksum/c_len, no uniqueness; exit 0 | 0 | 18/18; 6/6; 2/2 | **yes** |
| f1g | f1 + guard "section 0 starts with UPX" | 1 | recovered 6 of 18 (names cells refused by its own guard) | no |
| f1h | fixed offset 992 + full PackHeader validation (format, version, checksum, c_len), positional renames | 0 | 18/18; 6/6; 2/2 | **yes** |

Receipts: `out/{identity,real,f1_fixed_offset,f2_size_cache,f3_names_only,f4_magic_only,f5_refuser,f6_shotgun,f7_lazy_anchor,f1g_guarded_fixed_offset,f1h_fixed_offset_validated}.json`; log `out/forgeries.log`.

## Per-forgery classification
- **f2 size cache → counter defect.** Admitted because the oracle compares the repaired file's unpack to the reference pack of the same six pinned carriers. A repair that never reads its input passes. The battery has no held-out carrier and no "output derives from input" check. On a held-out set (setuptools cli-32/64, gui-32/64, cli.exe, fastlist-0.3.0-x86.exe; `out/heldout.log`) a size-keyed lookup has no entry, so a held-out carrier cannot be recovered by f2. Not a legitimate repair.
- **f7 lazy anchor → counter defect.** Admitted. It violates the candidate's own documented rule (checksum, c_len, unique candidate). Decoy test (V2, `out/variants.log`): battery t32 pack with real magic zeroed and a checksum-valid record placed at 960. Real candidate: `repair_rc=2 wrote=False` (refuses, correct). f7: `repair_rc=0`, `upx -t` rc 1, output corrupt, exit 0. The battery has no negative-with-candidates arm, so it cannot see this.
- **f1h fixed offset with validation → counter defect (coverage gap).** Admitted. It is a layout-specific repair, not the structural rule the candidate states. The frozen 12 carriers (6 pinned + 6 held-out) all have UPX1 `rawptr-64 = 960` (PackHeader at 992), so the battery cannot distinguish fixed-offset from structural anchoring. Stub-grown variants (`variants.log`): DOS stub +0x400 → UPX1 `rawptr-64 = 1984`; +0x800 → 3008. Real candidate: `upx -t` rc 0 and unpack-equivalent in both. f1h: refuses (rc 2). f1 (unguarded): `upx -t` rc 1, output corrupt, exit 0. f7: unpack-equivalent in both. (A stub growth of 0x1000 makes UPX refuse to pack; out of scope.)
- **f1 unguarded → rejected only by the refuse arm.** Its recovered and intact cells all pass (18/18, 6/6). Only the refuse arm (t64 and winhello, two cells) rejects it. A fixed-offset patcher that refuses on any other non-UPX shape would pass; the refuse arm is the sole defense and is two cells wide.
- f1g, f3–f6: rejected by recovered or intact arms, as expected; no finding.

## Attack on the tamper definitions
- **`effective 18 of 18` is real for the named reasons.** Attribution (`out/diag.log`): magic-only restoration (f4) makes `upx -t` pass for every magic cell (6/6), and leaves names cells failing. Names restoration with magic intact makes `upx -t` pass for every names cell (real candidate; magic intact in those files). Both reasons are independently necessary. However, the frozen predicate only checks `upx -t` rc != 0; it does not check the reason. That is a counter weakness, not a false cell today (finding 5).
- **"First `UPX!` is the PackHeader":** holds on every sample: one occurrence per untampered pack (6 pinned + 6 held-out + 2 stub variants, all at the header offset). The tamper uses `bytes.find` on the first occurrence; that is correct for these samples but not guaranteed in general (no counter check). Not a defect today.
- **Names tamper**: renames `UPX*` headers to `.text/.data/.rdata` by position. The real candidate restores `UPX0/UPX1` and `.rsrc` (the frozen carriers all end `.rsrc`, verified in `out/probe1.json` sections). Per the candidate docstring it picks `.rsrc` vs `UPX2` by RVA; I did not verify that branch. f3 wrote UPX2 and was not scored on names (its own guard rejected). Not a counter defect.

## Findings (count = 5)
1. Counter defect — f2 size-keyed cache admitted by the frozen predicate (no held-out carrier, no input-derived check).
2. Counter defect — f7 lazy anchor admitted; silent corrupt output with exit 0 on the decoy case (no negative-with-candidates arm).
3. Counter defect — f1h fixed-offset with validation admitted; carriers are layout monoculture (UPX1 rawptr 1024 on all 12), so the structural rule is untested (stub-grown variants fail f1/f1h).
4. Coverage over-claim — "packed PE inputs" is covered only for the 1024-byte-header layout; a stub-grown input is out of the frozen coverage.
5. Weak predicate — `effective` checks only `upx -t` rc != 0, not the reason; the refused arm is two cells and is the only rejector of unguarded f1.

## Recommendations (not applied — frozen; seats never re-freeze)
- Successor counter (new round, not this one): add (a) a stub-grown carrier (+0x400 stub, pinned by sha of the derived file) and (b) held-out carriers; (c) a negative arm with decoy PackHeader candidates expecting exit 2 and no output; (d) an input-derived check (repair output must differ from the tampered input only in the tampered bytes and must be byte-identical to the untampered pack); (e) check the `upx -t` failure reason string.
- Until then, C1's `met` must not be read as general PE UPX repair coverage; state it as coverage of the six pinned carriers at the 1024-byte-header layout.

## Tools
None installed. Used the pre-existing `/usr/bin/upx` 5.2.0 and `curl` (fetch of `pefile.cpp` from raw.githubusercontent.com v5.2.0). No pacman, no sysctl, no host changes.

## Commands (exit codes)
- `git clone --shared … $S/clone && git -C $S/clone checkout --detach 72346895…` (0)
- `python3 -I -B $S/clone/tools/round-98/pe-upx-tamper-battery.py --repair-cmd … --work $S/w/base --json-out … --rev 72346895…` (0)
- `bash $S/run_forgeries.sh` (0; logs `out/forgeries.log`)
- `python3 -I -B probe1.py` (0), `diag_names.py` (0), `heldout.py` (0), `variants.py` (0)
- f1g / f1h battery runs (1 / 0)
