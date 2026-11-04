# MutationR87 — R87-C1 mutation probe (round 87, kaidoku)

Artifacts: `.ufo/waves/round-87/w1/MutationR87/{mutation.json,mutation.md,notes.md,mutate.py,tabulate.py,raw-results.json,receipts/}`.
Repair under test: `tools/round-87/upx-magic-repair.py` at b5c7a49e, sha256 f4ebd152…c49723. Counter: `tools/round-87/upx-tamper-battery.py`, sha256 0f2d2bd8…5384b0. Production sha256 values match before and after the run. No production file was written.

## Verdict
- **Baselines held.** The committed repair passed the non-REA arms on 8/8 with N1, N2 and N3 all ok. identity scored 0/8 and met=false. naive-global passed the non-REA arms on 4/8. Both selftests passed.
- **Repair mutants: 22 total, 10 killed, 12 survived.** Survivors: R04, R06, R07, R08, R09, R14, R15, R17, R18, R19, R20, R22.
- **Counter mutants: 14 total, 8 killed, 6 survived.** Survivors: C02, C04, C05, C07, C09, C11.
- **Do-nothing control turned green by: none** of the 14 counter mutants. identity's red is over-determined: each case fails test_ok and identity, and N1 also fails. Turning it green takes at least three simultaneous defects, so identity is a weak detector for single counter defects.

## Findings
1. **The repair's selftest misses value defects that only the counter catches.** R01 (checksum `% 256`) and R05 (sentinel accepts a nonzero word3) both pass the selftest. The fixture computes its own PackHeader checksum with `ph_checksum`, so it never pins the 251 modulus. The fixture also contains no decoy b_info.
2. **The guards are not exercised by the population.** The repair walks a resume path on all 4 carriers (`walk.resume` jq 13228, xxd 18756, libz 62944, dinit 355828). Even so, removing each of these guards survives both the selftest and the counter: the l_info version/format cross-check (R04), the method checks (R07, R08), the plausibility bounds (R17, R18), the PackHeader version and length sanity checks (R14, R15), and front-first PackHeader selection (R09). Neither the carriers nor the fixture has a second checksum-valid window, a decoy p_filesize hit, or a mixed-method chain. The claim holds on this population, but these guards are untested.
3. **Some survivors are equivalent or near-equivalent.** R06 (resume at `stop`), R19 (`n1 == 0` refusal; N1 originals are refused earlier, at the PackHeader step) and R22 (`m >= 4`) leave the output unchanged on this population. R20 (selftest exit forced to 0) cannot be told apart while the pristine selftest has no failures.
4. **Calibration: T2 collides with T1 under a magic-including checksum.** The bytes of `KDK!` sum to 75+68+75+33 = 251 ≡ 0 (mod 251), the same as `00000000`. R02 (the checksum includes the magic) therefore still passes the non-REA arms on all 8 tampered cases. Only N3 (intact input) and the selftest kill it. The T2 class cannot detect this defect class. This is reported, not repaired; tamper values are frozen.
5. **N1 never reaches the ELF gate.** R12 (ELF/endianness gate dropped) is killed only by the selftest, because the plain originals are refused at the PackHeader step.
6. **Counter arms with no score-level coverage.** No reference repair (committed, identity, naive-global) exercises the failure path of the following:
   - C02: the N2 check is removed. N2 can only fire against a repack cheat, which is the counter's named limit.
   - C04: identity accepts any successful unpack.
   - C05: met ignores the controls.
   - C09: repair_rc0 ignores the exit code.
   - C11: N3 checks only the return code.
   - C07: the precondition is skipped. Every tamper is effective, so this is equivalent on this population.

   Two more mutants are killed only weakly. C01 (windows_only always True) is killed only by the counter selftest. C08 (test_ok always True) is killed only at reporting level: the false-arm list changes, but recovered, met and controls never do, because a test_ok failure always comes with an identity failure.
7. **The REA arm is the only thing keeping `--no-rea` runs unmet.** C12 ("recovered ignores rea_recover") makes the committed repair report met=true and exit 0 under `--no-rea`. It is caught here, but it shows that every non-REA pre-check depends on the integrated REA run to be meaningful.
8. **"Recovered" does not mean "restored to the packed bytes" on 2 carriers.** jq and xxd each carry a 4th `UPX!` word (jq offset 10971, xxd 16499). The repair leaves it tampered because it is not one of the three anchors. `upx -t` and `upx -d` pass, and the counter accepts the output, with `repaired_equals_packed` true on 4/8 cases (only libz and dinit). This matches the frozen arms, which require windows only, not byte identity to the packed file. Downstream claims should not read "recovered" as a byte-exact unpatch.

## Commands
`python3 -I -B .ufo/waves/round-87/w1/MutationR87/mutate.py --lane <lane> --scratch /fast/scratch/hyaku/kaidoku-r87/MutationR87 --out .ufo/waves/round-87/w1/MutationR87 --jobs 6`, then `tabulate.py`. The full 67-run matrix took about 26 s of wall time. Packed and tampered bytes were regenerated by the counter inside scratch and are not committed. Tools installed: none.

Checks for Main: confirm that the L1 integrated REA run scores 8/8 (this seat ran no REA scoring of the repair). Findings 4, 6 and 8 belong in the critic's weakness list, not in the frozen files.
