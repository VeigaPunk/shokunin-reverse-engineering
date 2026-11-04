# MutationR87 - R87-C1 mutation table

Pristine baselines: repair selftest `SELFTEST cases=9 failures=0`, counter selftest `SELFTEST cases=8 failures=0`; committed repair --no-rea non-REA 8/8 controls {'N1-refuse-plain': True, 'N2-corrupt-payload': True, 'N3-intact-idempotent': True}; identity (REA on) `recovered 0 of 8` met=False; naive-global --no-rea non-REA 4/8.

## Repair mutants (frozen counter, `--no-rea`)

| mutant | anchor (old -> new) | selftest | counter non-REA / controls | verdict |
|---|---|---|---|---|
| R01 checksum mod 251 -> 256 | `% 251` -> `% 256` | rc 0 | 0/8, fail N3-intact-idempotent | **killed** counter |
| R02 checksum includes magic (buf[0:31]) | `sum(buf[4:PH_SIZE - 1])` -> `sum(buf[0:PH_SIZE - 1])` | rc 1 | 8/8, fail N3-intact-idempotent | **killed** selftest+counter |
| R03 p_filesize offset 12 -> 8 | `m = p - 12` -> `m = p - 8` | rc 1 | 0/8, fail N3-intact-idempotent | **killed** selftest+counter |
| R04 drop l_info version/format cross-check | `if d[m + 6] == ph["version"] and d[m + 7] == ph["format"]:` -> `if True:` | rc 0 | 8/8, controls ok | **survived**  |
| R05 sentinel accepts nonzero word3 (method/ftid/cto8/unused) | ` and d[s + 8:s + 12] == b"\0\0\0\0"` -> `(deleted)` | rc 0 | 2/8, fail N3-intact-idempotent | **killed** counter |
| R06 resume scan starts at stop instead of stop+1 | `range(stop + 1, ph_off - 12)` -> `range(stop, ph_off - 12)` | rc 0 | 8/8, controls ok | **survived**  |
| R07 walk_chain method-match check removed | `elif meth != method:` -> `elif False:` | rc 0 | 8/8, controls ok | **survived**  |
| R08 resume-candidate method check removed | ` or d[s + 8] != method or` -> ` or` | rc 0 | 8/8, controls ok | **survived**  |
| R09 PackHeader scan from the front (first, not last) | `range(n - PH_SIZE, lo - 1, -1)` -> `range(lo, n - PH_SIZE + 1)` | rc 0 | 8/8, controls ok | **survived**  |
| R10 write UPX! at sentinel instead of sentinel+4 | `"b_info_end": sentinel + 4` -> `"b_info_end": sentinel` | rc 1 | 0/8, fail N3-intact-idempotent | **killed** selftest+counter |
| R11 intact check inverted (rewrite only anchors already UPX!) | `if out[off:off + 4] != MAGIC:` -> `if out[off:off + 4] == MAGIC:` | rc 1 | 0/8, controls ok | **killed** selftest+counter |
| R12 drop the ELF/endianness gate | `if d[:4] != b"\x7fELF" or len(d) < 64 or d[5] != 1:` -> `if len(d) < 64:` | rc 1 | 8/8, controls ok | **killed** selftest |
| R13 drop the l_info anchor | `"l_info": l_magic, ` -> `(deleted)` | rc 1 | 0/8, controls ok | **killed** selftest+counter |
| R14 PackHeader version gate dropped | `if version < 10 or fmt >= 128` -> `if fmt >= 128` | rc 0 | 8/8, controls ok | **survived**  |
| R15 PackHeader length sanity dropped | `if not (0 < c_len <= n and 0 < u_len and 0 < u_file_size):` -> `if False:` | rc 0 | 8/8, controls ok | **survived**  |
| R16 TAIL_WINDOW 512 -> 32 | `TAIL_WINDOW = 512` -> `TAIL_WINDOW = 32` | rc 1 | 0/8, fail N3-intact-idempotent | **killed** selftest+counter |
| R17 resume candidate allows sz_cpr == sz_unc | `if not (0 < sz_cpr < sz_unc)` -> `if not (0 < sz_cpr <= sz_unc)` | rc 0 | 8/8, controls ok | **survived**  |
| R18 walk_chain drops sz_cpr > sz_unc bound | ` or sz_cpr > sz_unc or` -> ` or` | rc 0 | 8/8, controls ok | **survived**  |
| R19 refuse when first walk finds 0 blocks dropped | `if n1 == 0:` -> `if False:` | rc 0 | 8/8, controls ok | **survived**  |
| R20 selftest exit forced 0 | `return 0 if not fails else 1` -> `return 0` | rc 0 | 8/8, controls ok | **survived**  |
| R21 intact flag inverted | `"intact": not restored` -> `"intact": bool(restored)` | rc 1 | 8/8, controls ok | **killed** selftest |
| R22 l_info search from offset 0 and allows m<4 | `if m >= 4 and m + 20 <= ph_off:` -> `if m + 20 <= ph_off:` | rc 0 | 8/8, controls ok | **survived**  |

## Counter mutants (committed repair / identity / naive-global)

| mutant | anchor (old -> new) | selftest | repair | identity | naive-global | identity green? | verdict |
|---|---|---|---|---|---|---|---|
| C01 windows_only always True | `    """Every differing byte lies inside a 4-byte window that` -> `    """Every differing byte lies inside a 4-byte window that` | rc 1 | 8/8 nonREA, rec 0, met False, ctl-fail [] | 0/8 nonREA, rec 0, met False, ctl-fail ['N1-refuse-plain'] | 4/8 nonREA, rec 0, met False, ctl-fail ['N1-refuse-plain'] | False | **killed** selftest |
| C02 N2 control check removed | `"N2-corrupt-payload": not any(x["recovered"] for x in contro` -> `"N2-corrupt-payload": True,` | rc 0 | 8/8 nonREA, rec 0, met False, ctl-fail [] | 0/8 nonREA, rec 0, met False, ctl-fail ['N1-refuse-plain'] | 4/8 nonREA, rec 0, met False, ctl-fail ['N1-refuse-plain'] | False | **survived**  |
| C03 identity arm compares packed sha | `arms["identity"] = usha == c["sha256"]` -> `arms["identity"] = usha == sha256_bytes(pbytes)` | rc 0 | 0/8 nonREA, rec 0, met False, ctl-fail [] | 0/8 nonREA, rec 0, met False, ctl-fail ['N1-refuse-plain'] | 0/8 nonREA, rec 0, met False, ctl-fail ['N1-refuse-plain'] | False | **killed** ref-repair+ref-naive |
| C04 identity arm accepts any successful unpack | `arms["identity"] = usha == c["sha256"]` -> `arms["identity"] = usha is not None` | rc 0 | 8/8 nonREA, rec 0, met False, ctl-fail [] | 0/8 nonREA, rec 0, met False, ctl-fail ['N1-refuse-plain'] | 4/8 nonREA, rec 0, met False, ctl-fail ['N1-refuse-plain'] | False | **survived**  |
| C05 met ignores controls | `met = recovered == TARGET and all(ctl_ok.values())` -> `met = recovered == TARGET` | rc 0 | 8/8 nonREA, rec 0, met False, ctl-fail [] | 0/8 nonREA, rec 0, met False, ctl-fail ['N1-refuse-plain'] | 4/8 nonREA, rec 0, met False, ctl-fail ['N1-refuse-plain'] | False | **survived**  |
| C06 tamper leaves the last magic word | `return packed.replace(MAGIC, value)` -> `return packed.replace(MAGIC, value, max(packed.count(MAGIC) ` | rc 1 | 8/8 nonREA, rec 0, met False, ctl-fail [] | 0/8 nonREA, rec 0, met False, ctl-fail ['N1-refuse-plain'] | 0/8 nonREA, rec 0, met False, ctl-fail ['N1-refuse-plain'] | False | **killed** selftest+ref-naive |
| C07 precondition (upx -t fails on tampered) skipped | `if pre_t["rc"] == 0:` -> `if False:` | rc 0 | 8/8 nonREA, rec 0, met False, ctl-fail [] | 0/8 nonREA, rec 0, met False, ctl-fail ['N1-refuse-plain'] | 4/8 nonREA, rec 0, met False, ctl-fail ['N1-refuse-plain'] | False | **survived**  |
| C08 test_ok arm always True | `arms["test_ok"] = t["rc"] == 0` -> `arms["test_ok"] = True` | rc 0 | 8/8 nonREA, rec 0, met False, ctl-fail [] | 0/8 nonREA, rec 0, met False, ctl-fail ['N1-refuse-plain'] | 4/8 nonREA, rec 0, met False, ctl-fail ['N1-refuse-plain'] | False | **killed** ref-identity+ref-naive |
| C09 repair_rc0 ignores exit code | `arms["repair_rc0"] = rr["rc"] == 0 and os.path.isfile(outp)` -> `arms["repair_rc0"] = os.path.isfile(outp)` | rc 0 | 8/8 nonREA, rec 0, met False, ctl-fail [] | 0/8 nonREA, rec 0, met False, ctl-fail ['N1-refuse-plain'] | 4/8 nonREA, rec 0, met False, ctl-fail ['N1-refuse-plain'] | False | **survived**  |
| C10 N1 refuse always True | `"refused": n1["rc"] != 0` -> `"refused": True` | rc 0 | 8/8 nonREA, rec 0, met False, ctl-fail [] | 0/8 nonREA, rec 0, met False, ctl-fail [] | 4/8 nonREA, rec 0, met False, ctl-fail [] | False | **killed** ref-identity+ref-naive |
| C11 N3 ignores bytes (rc only) | `same = n3["rc"] == 0 and os.path.isfile(n3o) and sha256_file` -> `same = n3["rc"] == 0` | rc 0 | 8/8 nonREA, rec 0, met False, ctl-fail [] | 0/8 nonREA, rec 0, met False, ctl-fail ['N1-refuse-plain'] | 4/8 nonREA, rec 0, met False, ctl-fail ['N1-refuse-plain'] | False | **survived**  |
| C12 recovered ignores the rea arm | `case["recovered"] = all(arms.values())` -> `case["recovered"] = all(v for k, v in arms.items() if k != "` | rc 0 | 8/8 nonREA, rec 8, met True, ctl-fail [] | 0/8 nonREA, rec 0, met False, ctl-fail ['N1-refuse-plain'] | 4/8 nonREA, rec 4, met False, ctl-fail ['N1-refuse-plain'] | False | **killed** ref-repair+ref-naive |
| C13 N2 flips no byte | `tb[mid] ^= 0xFF` -> `tb[mid] ^= 0x00` | rc 0 | 8/8 nonREA, rec 0, met False, ctl-fail ['N2-corrupt-payload'] | 0/8 nonREA, rec 0, met False, ctl-fail ['N1-refuse-plain'] | 4/8 nonREA, rec 0, met False, ctl-fail ['N1-refuse-plain'] | False | **killed** ref-repair |
| C14 T2 tamper value equals T1 (zero) | `TAMPERS = {"T1-zero": b"\x00\x00\x00\x00", "T2-foreign": b"K` -> `TAMPERS = {"T1-zero": b"\x00\x00\x00\x00", "T2-foreign": b"\` | rc 0 | 8/8 nonREA, rec 0, met False, ctl-fail [] | 0/8 nonREA, rec 0, met False, ctl-fail ['N1-refuse-plain'] | 0/8 nonREA, rec 0, met False, ctl-fail ['N1-refuse-plain'] | False | **killed** ref-naive |

Survivors: C02, C04, C05, C07, C09, C11, R04, R06, R07, R08, R09, R14, R15, R17, R18, R19, R20, R22
Identity (do-nothing) turned green by: none
Counts: {'repair': {'killed': 10, 'survived': 12, 'inconclusive': 0}, 'counter': {'killed': 8, 'survived': 6, 'inconclusive': 0}}
Restoration: production sha256 before == after: True
