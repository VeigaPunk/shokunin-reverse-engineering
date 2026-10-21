FALSIFIED — R19-D6d does not reliably reject an argv decoy: an unrelated subcommand can pass `--require-mid-maps` when a later argument pair is `rea-agents@<version>`, `analyze`.

## Evidence at measured source S

**Observed source.** Extracted `.ufo/waves/round-17/tools/receipt-validate.py` from Git object `5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9` with `git show` (exit 0; blob `484dcf2b8d3296e768d09bf0ff4b2cc1a395e745`; SHA-256 `a31c7db8fbf2f67d34b3f0aad969847794efb8712b1c717b94960652becbe22c`, 55,518 bytes). S's contract says this must be the `npx` form and decoy `analyze` tokens elsewhere are rejected (`.ufo/waves/round-20/contract.md:65-67`). But `_is_analyze_step` scans every argv index for any numeric-version `rea-agents@...` token whose next token is `analyze`; it does not require the token to be npx's package operand or require an `npx` command (`.ufo/waves/round-17/tools/receipt-validate.py:134-154`). Both object- and list-shaped `steps` use this predicate to accept the analyze checks (`:613-645`; called by `validate_receipt` at `:664-667`, CLI at `:1218-1221`). The built-in decoy fixture only tests a later bare `analyze` after `inspect-go-binary`, without a second package token (`:1141-1166`); it misses the tested case below.

**Crafted object/list receipts.** Starting from the S Git-object receipt `.ufo/waves/round-20/runs/t1246-asm/receipt.json`, I copied the receipt into `/tmp/r20-d6d.bl8bV8/fixtures/` and changed only the analyze argv and whether `steps` was represented as its original object or as a list. These files were scratch-only, under a directory created by `mktemp -d`.

- Decoy-position argv, in both shapes: `["npx", "--yes", "rea-agents@6.5.0", "inspect-go-binary", "rea-agents@6.5.0", "analyze"]`. The first package invocation is `inspect-go-binary`; the second package-looking token is only a later argument. Both receipts were reported `valid` (exit 0) and their mid-map checks satisfied the flag.
- Non-npx argv, in both shapes: `["/usr/bin/true", "rea-agents@6.5.0", "analyze"]`. Both were also `valid` (exit 0), confirming the predicate does not establish the stated npx form.
- Positive `npx --yes` controls with `rea-agents@6.5.0 analyze` were valid in both shapes (exit 0).
- `npx --yes rea-agents@latest analyze` was invalid in both shapes, with `analyze_step_unauthenticated` and `mid_checks_absent` (per-receipt exit 1).

**Commands and exit codes.** Source extraction: `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show 5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9:.ufo/waves/round-17/tools/receipt-validate.py > /tmp/r20-d6d.bl8bV8/tools/receipt-validate.py` → 0. Extracted the sibling `pins.py` and every receipt input from the same S Git tree into that scratch directory; no working-tree receipt JSON was used.

`python3 -I -B /tmp/r20-d6d.bl8bV8/tools/receipt-validate.py --selftest` → 0; output `SELFTEST: CLEAN cases=28`.

`python3 -I -B /tmp/r20-d6d.bl8bV8/tools/receipt-validate.py --require-mid-maps /tmp/r20-d6d.bl8bV8/fixtures/yes-control-object.json /tmp/r20-d6d.bl8bV8/fixtures/yes-control-list.json /tmp/r20-d6d.bl8bV8/fixtures/decoy-position-object.json /tmp/r20-d6d.bl8bV8/fixtures/decoy-position-list.json /tmp/r20-d6d.bl8bV8/fixtures/latest-object.json /tmp/r20-d6d.bl8bV8/fixtures/latest-list.json /tmp/r20-d6d.bl8bV8/fixtures/non-npx-object.json /tmp/r20-d6d.bl8bV8/fixtures/non-npx-list.json` → 1 overall; counts: 8 receipts, 6 valid, 2 invalid, 0 unreadable. The only invalid pair was the expected `@latest` pair; both decoy-position shapes passed.

Revalidated all eight S round-19 pass2 receipts and all nineteen S round-20 run receipts together:

```sh
python3 -I -B /tmp/r20-d6d.bl8bV8/tools/receipt-validate.py --require-mid-maps \
  /tmp/r20-d6d.bl8bV8/source/.ufo/waves/round-19/runs/pass2/t1250-asm/receipt.json \
  /tmp/r20-d6d.bl8bV8/source/.ufo/waves/round-19/runs/pass2/t1250-cgo/receipt.json \
  /tmp/r20-d6d.bl8bV8/source/.ufo/waves/round-19/runs/pass2/t1250-compile/receipt.json \
  /tmp/r20-d6d.bl8bV8/source/.ufo/waves/round-19/runs/pass2/t1250-cover/receipt.json \
  /tmp/r20-d6d.bl8bV8/source/.ufo/waves/round-19/runs/pass2/t1250-go/receipt.json \
  /tmp/r20-d6d.bl8bV8/source/.ufo/waves/round-19/runs/pass2/t1250-gofmt/receipt.json \
  /tmp/r20-d6d.bl8bV8/source/.ufo/waves/round-19/runs/pass2/t1250-preprofile/receipt.json \
  /tmp/r20-d6d.bl8bV8/source/.ufo/waves/round-19/runs/pass2/t1250-vet/receipt.json \
  /tmp/r20-d6d.bl8bV8/source/.ufo/waves/round-20/runs/t1246-addr2line/receipt.json \
  /tmp/r20-d6d.bl8bV8/source/.ufo/waves/round-20/runs/t1246-asm/receipt.json \
  /tmp/r20-d6d.bl8bV8/source/.ufo/waves/round-20/runs/t1246-buildid/receipt.json \
  /tmp/r20-d6d.bl8bV8/source/.ufo/waves/round-20/runs/t1246-cgo/receipt.json \
  /tmp/r20-d6d.bl8bV8/source/.ufo/waves/round-20/runs/t1246-compile/receipt.json \
  /tmp/r20-d6d.bl8bV8/source/.ufo/waves/round-20/runs/t1246-covdata/receipt.json \
  /tmp/r20-d6d.bl8bV8/source/.ufo/waves/round-20/runs/t1246-cover/receipt.json \
  /tmp/r20-d6d.bl8bV8/source/.ufo/waves/round-20/runs/t1246-doc/receipt.json \
  /tmp/r20-d6d.bl8bV8/source/.ufo/waves/round-20/runs/t1246-fix/receipt.json \
  /tmp/r20-d6d.bl8bV8/source/.ufo/waves/round-20/runs/t1246-go/receipt.json \
  /tmp/r20-d6d.bl8bV8/source/.ufo/waves/round-20/runs/t1246-gofmt/receipt.json \
  /tmp/r20-d6d.bl8bV8/source/.ufo/waves/round-20/runs/t1246-nm/receipt.json \
  /tmp/r20-d6d.bl8bV8/source/.ufo/waves/round-20/runs/t1246-objdump/receipt.json \
  /tmp/r20-d6d.bl8bV8/source/.ufo/waves/round-20/runs/t1246-pack/receipt.json \
  /tmp/r20-d6d.bl8bV8/source/.ufo/waves/round-20/runs/t1246-pprof/receipt.json \
  /tmp/r20-d6d.bl8bV8/source/.ufo/waves/round-20/runs/t1246-preprofile/receipt.json \
  /tmp/r20-d6d.bl8bV8/source/.ufo/waves/round-20/runs/t1246-test2json/receipt.json \
  /tmp/r20-d6d.bl8bV8/source/.ufo/waves/round-20/runs/t1246-trace/receipt.json \
  /tmp/r20-d6d.bl8bV8/source/.ufo/waves/round-20/runs/t1246-vet/receipt.json
```
→ exit 1; counts: 27 receipts, 19 valid, 8 invalid, 0 unreadable. All nineteen round-20 run receipts were valid. All eight R19 pass2 receipts were invalid only for `sha256_mismatch` and `size_mismatch` on the pinned live path `.ufo/waves/round-17/tools/receipt-validate.py`: each recorded SHA-256 `6afb7ef6600cdc7907d5eb4af1ac97b9dae1a10c648c50474d249fca2ac2c762` / 52,682 bytes; live-at-validation S bytes were SHA-256 `a31c7db8fbf2f67d34b3f0aad969847794efb8712b1c717b94960652becbe22c` / 55,518 bytes. The validator documents that it compares committed digests with bytes present now, not historical run-window bytes (`W17/tools/receipt-validate.py:18-22,49-52`); these eight failures are validator-file pin drift, not a mid-map finding.

**Inference and limits.** The emitted valid results for both forged decoy shapes falsify the D6d contract (`W20/contract.md:65-67`) even though the selftest is green. `@latest` is refused as desired, but does not repair the decoy-position gap. The validator only inspects recorded argv and expressly executes no child process (`W17/tools/receipt-validate.py:45-52`); neither REA CLI nor a Go toolchain binary was launched. The supplied tool inventory has no LSP device, so I relied on Git-object source and direct validator execution, not grep as semantic proof. No tools were installed.