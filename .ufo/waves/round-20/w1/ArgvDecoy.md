# ArgvDecoy-2 — D6d

Axes: calibration (refuse argv decoys), coverage (named refusal + positive selftest), depth (package/subcommand adjacency).

## Change

**Observation:** In `.ufo/waves/round-17/tools/receipt-validate.py:134-165`, list-step identity now requires `analyze` immediately after a `rea-agents@<numeric-version>` token; labels and decoy tokens only nominate candidates. `.ufo/waves/round-17/tools/receipt-validate.py:613-653` applies the same authentication to object- and list-shaped steps, emits `analyze_step_unauthenticated` for claimed but unauthenticated steps, and does not let their pin checks satisfy `--require-mid-maps`. The selftest asserts `argv_decoy_refused` and the positive `argv_analyze_after_package_accepted` (`:1141-1170`); fixture invocations were updated to the required package-token form.

Patch: `.ufo/waves/round-20/w1/patches/ArgvDecoy-2.patch`.
Base observed: `14f0260ad319ecc26994381b2415d5a999003375`.
`git diff --cached --stat 14f0260ad319ecc26994381b2415d5a999003375` (exit 0): `.ufo/waves/round-17/tools/receipt-validate.py | 152 ++++++++++++++++++--------`; `1 file changed, 105 insertions(+), 47 deletions(-)`.

## Verification and commands

Clone command (exit 0): `if test -e /tmp/kr20-ArgvDecoy-2; then printf 'BLOCKED: /tmp/kr20-ArgvDecoy-2 already exists\n'; exit 73; else git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/kaidoku-shokunin /tmp/kr20-ArgvDecoy-2 && git -C /tmp/kr20-ArgvDecoy-2 checkout -q --detach 14f0260ad319ecc26994381b2415d5a999003375 && git -C /tmp/kr20-ArgvDecoy-2 rev-parse HEAD; fi`; observed base was the stated hash.

Selftest command, run from `/tmp/kr20-ArgvDecoy-2`: `python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py --selftest; rc=$?; printf 'EXIT_CODE=%d\n' "$rc"; exit "$rc"`.
- First run exit 1: fixture construction raised `KeyError: 'analyze'`; corrected to build the list fixture from the available inspect step.
- Second run exit 1: existing object-shaped green fixture used `argv=["npx", "analyze"]`, which is unauthenticated under D6d; changed all such fixture invocations to include `rea-agents@6.5.0` before `analyze`.
- Final run's exact selftest last line: `SELFTEST: CLEAN cases=28`; exit 0. The only later edit was docstring wording in `verify_mid_maps` (`:493-512`); no runtime code changed afterward.

Receipt command template, each run from `/tmp/kr20-ArgvDecoy-2` (shell wrapper appended `; rc=$?; printf 'EXIT_CODE=%d\\n' "$rc"; exit "$rc"`): `python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps <receipt>`.

Round 18 exit codes:
- `runs/s1250-swiss-nomethods/receipt.json`: 1
- `runs/s1250-swiss-nethttp/receipt.json`: 1
- `runs/s1250-swiss-methods/receipt.json`: 1
- `runs/s1250-noswiss-nomethods/receipt.json`: 1
- `runs/s1250-noswiss-nethttp/receipt.json`: 1
- `runs/s1250-noswiss-methods/receipt.json`: 1
- `runs/s1246-swiss-nomethods/receipt.json`: 1
- `runs/s1246-swiss-nethttp/receipt.json`: 1
- `runs/s1246-swiss-methods/receipt.json`: 1
- `runs/s1246-noswiss-nomethods/receipt.json`: 1
- `runs/s1246-noswiss-nethttp/receipt.json`: 1
- `runs/s1246-noswiss-methods/receipt.json`: 1
- `runs/real-kimi-webbridge/receipt.json`: 1
- `runs/calib-notesmd-cli/receipt.json`: 1
- `runs/calib-aether/receipt.json`: 1

Round 19 pass2 exit codes:
- `runs/pass2/t1250-vet/receipt.json`: 0
- `runs/pass2/t1250-preprofile/receipt.json`: 0
- `runs/pass2/t1250-gofmt/receipt.json`: 0
- `runs/pass2/t1250-go/receipt.json`: 0
- `runs/pass2/t1250-cover/receipt.json`: 0
- `runs/pass2/t1250-compile/receipt.json`: 0
- `runs/pass2/t1250-cgo/receipt.json`: 0
- `runs/pass2/t1250-asm/receipt.json`: 0

**R18 blocker (observed):** All 15 R18 runs report `sha256_mismatch` and `size_mismatch` on the pinned live path `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/tools/receipt-validate.py`; no mid-map failure was reported. For example, the receipt records SHA-256 `70672eb3bd0c06e93ca439a31558f35ab7f76bd23aa74acd026290972553d145`, size 46047 at `.ufo/waves/round-18/runs/s1250-swiss-nomethods/receipt.json:1101-1104` (also `:1867-1870`). The measured live file is 52682 bytes, SHA-256 `6afb7ef6600cdc7907d5eb4af1ac97b9dae1a10c648c50474d249fca2ac2c762` (`wc -c` + `sha256sum`, exit 0). Inference: those R18 failures are existing live-file pin drift; I did not alter the lane source or receipt inputs.

Other commands: the initial patch packaging command (including `mkdir -p`, `git add -A`, and `git diff --cached --binary ... > ...`) exited 0; the final patch refresh (`git add -A && git diff --cached --binary 14f0260ad319ecc26994381b2415d5a999003375 > /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/w1/patches/ArgvDecoy-2.patch && git diff --cached --stat 14f0260ad319ecc26994381b2415d5a999003375`) exited 0. `wc -c ... && sha256sum ...` exited 0. No tools installed. LSP was unavailable in the supplied tool inventory; source discovery used `read`/`grep`.
