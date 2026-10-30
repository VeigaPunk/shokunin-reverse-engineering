# ExecFetchSelftest — round 51 wave 1

Verdict: partial draft; guard-present checks pass, but the required deleted-guard fixture proof is **not done**. Do not represent the guard deletion obligation as met.

Draft: `.ufo/waves/round-51/w1/ExecFetchSelftest/fetch-vendor.py` is copied from the round-50 fetcher (original and initial copy SHA-256 `c53221ea9e4ba586552a65cfa3be056a0ab8c792920a8361aca1e13addc3d8a8`) with added offline selftests for the initial non-HTTPS URL, initial wrong host and off-host redirect. Existing chain-pin/carve implementation and CLI are otherwise retained. Its three new checks are synthetic/offline; however, the redirect selftest directly instantiates `_AvmOnlyRedirect`, not the registered `_OPENER` wiring. The requested independent deleted-guard fixture copies (including registration deletion) were not run and are a material remaining gap.

Evidence (UTC 2026-10-30; exact commands, exit codes, stdout hashes):

- Base run: `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-50/fetch-vendor.py --selftest > "$S/base.out" 2>&1` (with `S=/fast/scratch/hyaku/kaidoku-r51/w1-ExecFetchSelftest`, `TMPDIR="$S"`); exit 0; stdout SHA-256 `828a9add44cff9e88dc7751bd290d981ba040eff20bb25a09666d9dad34804ec`; observed `SELFTEST cases=16 pass=16 fail=0`.
- Draft first attempt at its report location: exit 1 due to expected relative dependency `round-41/sqfs-list.py` not being adjacent to the draft path; stdout SHA-256 `b79ea9572ca4c435c17ad1f44f2dc630ada57259c2d9142110180f29129d5588`. Not an instrument defect at its intended `tools/round-51/` location.
- Draft matching-layout fixture: copied draft to `$S/fixture/tools/round-51/fetch-vendor.py` and dependency to `$S/fixture/tools/round-41/sqfs-list.py`; ran `python3 -I -B "$S/fixture/tools/round-51/fetch-vendor.py" --selftest > "$S/draft2.out" 2>&1`; exit 0; stdout SHA-256 `d0dd772d00d8608b855db9099987dd09988315b45436e5e8b97af0a3dcf54abe`; observed `SELFTEST cases=19 pass=19 fail=0`, including green checks for the three listed URL guards. The checked-in lane source/dependency was read-only; no REA run or downloads.

The invoked selftest commands ran at 2026-10-30T04:58Z (exact per-command timestamps were not captured). Deleted-guard fixture runs: **not run**. Therefore refusal-on-mutant and the requested proof of failure remain unverified. No tools installed.