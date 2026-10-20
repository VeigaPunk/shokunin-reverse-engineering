# CausesKeyCollision — D6e

## Result

**Observation:** At baseline `14f0260ad319ecc26994381b2415d5a999003375`, the writer clone was at that exact commit. Updated `.ufo/waves/round-19/tools/wave-outcomes.py:237-240` to identify a wrapped cause map only when `causes` is an object and the top-level `wave` key is present. A flat `{"causes": {"cause": ..., "source": ...}}` now resolves as a seat entry. The wrapped-map selftest now supplies `wave`; new case `seat_named_causes` checks object cause and source (`:703-729`). This implements the shared D6e interface (`.ufo/waves/round-20/contract.md:68-69`).

## Commands and evidence

- `git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/kaidoku-shokunin /tmp/kr20-CausesKeyCollision-2 && git -C /tmp/kr20-CausesKeyCollision-2 checkout -q --detach 14f0260ad319ecc26994381b2415d5a999003375 && git -C /tmp/kr20-CausesKeyCollision-2 rev-parse HEAD` → exit 0; observed base `14f0260ad319ecc26994381b2415d5a999003375`.
- `python3 -I -B .ufo/waves/round-19/tools/wave-outcomes.py --selftest` in the clone → exit 0; exact final line: `SELFTEST: CLEAN cases=34` (verify.py's required tool selftest loop: `.ufo/waves/round-19/verify.py:514-521`).
- Round-18 W2 red replay, using registration/report-dir from `.ufo/waves/round-19/w1/WaveOutcomesTool.md:80-89` and a `{}
` causes fixture under `tempfile.mkdtemp()`: command invoked twice with the same argv and output path; both tool exits 1, stdout-identical and JSON-identical; harness exit 0. Exact tool argv:
  `python3 -I -B /tmp/kr20-CausesKeyCollision-2/.ufo/waves/round-19/tools/wave-outcomes.py --registration .ufo/waves/round-18/wave2-registration.json --report-dir .ufo/waves/round-18/w2 --causes /tmp/kr20-causes-r18-v_pib8d0/empty-causes.json --out /tmp/kr20-causes-r18-v_pib8d0/r18-w2.json`
  ```text
  OUTCOMES seats=98 reports=94 missing=4 uncaused=4 (rule: report=report_present=<report-dir>/<name>.md exists as a regular file with size>0; cause=cause=causes[<name>| <agentId>], non-empty after strip)
  MISSING n=4 ["GatePRODUCERREV", "GateSUMSRUNLOG", "ShonenLines", "TruthREGISTRY"] (rule: seat has no report file)
  CAUSES recorded=0 unneeded=0 ignored_meta=0 (rule: one non-empty cause per seat, from causes[<name>|<agentId>])
  UNCAUSED n=4 ["GatePRODUCERREV", "GateSUMSRUNLOG", "ShonenLines", "TruthREGISTRY"] (rule: 1 iff any seat with report_present=false has cause null) -> exit 1
  OUT /tmp/kr20-causes-r18-v_pib8d0/r18-w2.json
  ```
- Round-18 W2 green replay with retained causes and same argv twice → tool exits 0/0, stdout and JSON identical, output JSON byte-identical to `.ufo/waves/round-19/evidence/wave-outcomes/r18-w2-outcomes.json:2-19`; harness exit 0. CWD: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-19`. Exact tool argv:
  `python3 -I -B /tmp/kr20-CausesKeyCollision-2/.ufo/waves/round-19/tools/wave-outcomes.py --registration ../round-18/wave2-registration.json --report-dir ../round-18/w2 --causes evidence/wave-outcomes/r18-w2-causes.json --out /tmp/kr20-causes-r18-green-02uanh4q/r18-w2-green.json`
  ```text
  OUTCOMES seats=98 reports=94 missing=4 uncaused=0 (rule: report=report_present=<report-dir>/<name>.md exists as a regular file with size>0; cause=cause=causes[<name>| <agentId>], non-empty after strip)
  MISSING n=4 ["GatePRODUCERREV", "GateSUMSRUNLOG", "ShonenLines", "TruthREGISTRY"] (rule: seat has no report file)
  CAUSES recorded=4 unneeded=0 ignored_meta=0 (rule: one non-empty cause per seat, from causes[<name>|<agentId>])
  OUT /tmp/kr20-causes-r18-green-02uanh4q/r18-w2-green.json
  ```
- Round-19 W2 replay using registration/report-dir/causes recorded at `.ufo/waves/round-19/wave2-outcomes.json:3-8`, same argv twice → tool exits 0/0, stdout and JSON identical; generated JSON byte-identical to retained `.ufo/waves/round-19/wave2-outcomes.json`; harness exit 0. Exact tool argv:
  `python3 -I -B /tmp/kr20-CausesKeyCollision-2/.ufo/waves/round-19/tools/wave-outcomes.py --registration /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-19/wave2-registration.json --report-dir /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-19/w2 --causes /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-19/evidence/wave-outcomes/w2-causes.json --out /tmp/kr20-causes-r19-99m4rk25/r19-w2.json`
  ```text
  OUTCOMES seats=72 reports=72 missing=0 uncaused=0 (rule: report=report_present=<report-dir>/<name>.md exists as a regular file with size>0; cause=cause=causes[<name>| <agentId>], non-empty after strip)
  MISSING n=0 [] (rule: seat has no report file)
  CAUSES recorded=0 unneeded=0 ignored_meta=0 (rule: one non-empty cause per seat, from causes[<name>|<agentId>])
  OUT /tmp/kr20-causes-r19-99m4rk25/r19-w2.json
  ```

## Command correction, patch, and limits

- One initial R18 replay wrapper wrote literal backslash-`n` in the temporary causes JSON; tool refused it as `causes_invalid` (tool exit 2; wrapper exit 1). Corrected fixture to a newline-terminated `{}`; successful red replay above. Temporary directories were removed.
- Patch command: `mkdir -p /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/w1/patches && git -C /tmp/kr20-CausesKeyCollision-2 add -A && git -C /tmp/kr20-CausesKeyCollision-2 diff --cached --binary 14f0260ad319ecc26994381b2415d5a999003375 > /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/w1/patches/CausesKeyCollision-2.patch && git -C /tmp/kr20-CausesKeyCollision-2 diff --cached --stat 14f0260ad319ecc26994381b2415d5a999003375` → exit 0. Cached stat: `.ufo/waves/round-19/tools/wave-outcomes.py | 25 +++++++++++++++++++++----`; `1 file changed, 21 insertions(+), 4 deletions(-)`.
- No tools installed or updated. No external state was changed. No LSP device was exposed in this seat's tool inventory; no LSP operation was available. No blocker to the scoped implementation.