# CarrierGuardTool-2

## Axes
- **Calibration:** `arm` rejects non-regular carrier paths before changing any modes; `check` records distinct mode, ctime, and content findings.
- **Coverage:** implements `arm`, manifest-bound `check`/`disarm`, manual-record `adopt`, UTC JSON records, and isolated selftests.
- **Depth:** captures and rechecks SHA-256, size, mode, and ctime; adoption retains `mode_before` without accessing carrier paths.

## Observed implementation and evidence
- Added `.ufo/waves/round-20/tools/carrier-guard.py`. TSV parsing and regular-file preflight are at `.ufo/waves/round-20/tools/carrier-guard.py:9-13,119-143`; arm captures content/modes and clears exec bits at `.ufo/waves/round-20/tools/carrier-guard.py:300-360`; manifest-bound checks and mode restoration are at `.ufo/waves/round-20/tools/carrier-guard.py:363-475`; adoption copies the manual record without opening or statting carrier paths at `.ufo/waves/round-20/tools/carrier-guard.py:478-489`.
- The module documents the loader-mapped execution and root limits at `.ufo/waves/round-20/tools/carrier-guard.py:15-18`. The selftest uses temporary copies of `/usr/bin/true`, checks direct-exec refusal, mode/content tampering, non-regular refusal, and adoption at `.ufo/waves/round-20/tools/carrier-guard.py:499-625`.
- Baseline observed in the clone: `14f0260ad319ecc26994381b2415d5a999003375`.
- Selftest stdout last line (exact): `SELFTEST: CLEAN cases=4`; tool exit code: `0` (`SELFTEST_EXIT=0`). It ran once. No actual Go carrier was operated on.
- Staged patch stat: `.ufo/waves/round-20/tools/carrier-guard.py | 684 +++++++++++++++++++++++++++++` (`1 file changed, 684 insertions(+)`).

## Commands and exits
1. `git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/kaidoku-shokunin /tmp/kr20-CarrierGuardTool-2` — exit 0.
2. `git -C /tmp/kr20-CarrierGuardTool-2 checkout -q --detach 14f0260ad319ecc26994381b2415d5a999003375` — exit 0.
3. `git -C /tmp/kr20-CarrierGuardTool-2 rev-parse HEAD` — exit 0; output `14f0260ad319ecc26994381b2415d5a999003375`.
4. `python3 -I -B .ufo/waves/round-20/tools/carrier-guard.py --selftest; rc=$?; printf 'SELFTEST_EXIT=%s\n' "$rc"; exit "$rc"` — exit 0; last selftest line `SELFTEST: CLEAN cases=4`.
5. `git -C /tmp/kr20-CarrierGuardTool-2 add .ufo/waves/round-20/tools/carrier-guard.py` — exit 0.
6. `git -C /tmp/kr20-CarrierGuardTool-2 diff --cached --binary 14f0260ad319ecc26994381b2415d5a999003375 > /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/w1/patches/CarrierGuardTool-2.patch` — exit 0.
7. `git -C /tmp/kr20-CarrierGuardTool-2 diff --cached --stat 14f0260ad319ecc26994381b2415d5a999003375` — exit 0; output as above.

## Deliverable, risks, blockers
- Patch: `.ufo/waves/round-20/w1/patches/CarrierGuardTool-2.patch`.
- Risk/limit: mode bits do not prevent loader-mapped execution or privileged/root bypass, as documented in the module. `adopt` intentionally transforms record data only; later `check` is what revalidates live carrier state.
- Blockers: none. No tools were installed or updated.
