# Receipt validator review

## Findings

### High — D6d has no end-to-end red case for object-shaped `steps`, and that branch currently bypasses argv authentication

**Observation:** List-shaped steps are checked by `_is_analyze_step` (`.ufo/waves/round-17/tools/receipt-validate.py:134-161`), but `--require-mid-maps` handles object-shaped steps separately: it accepts `steps["analyze"]` solely on the key and nonempty `pin_checks` (`:609-613`). The negative identity cases at `:1105-1112` call `_is_analyze_step` directly; they do not validate a receipt and cannot cover the object branch. D6d requires the `analyze` subcommand immediately after the package token and a rejection finding (`.ufo/waves/round-20/contract.md:65-67`).

**Inference:** A complete otherwise-valid carrier fixture with `steps.analyze.argv` set to `npx -y rea-agents@6.5.0 inspect-go-binary … analyze` and valid map checks satisfies the current object branch, despite `analyze` being a decoy argument. Add a `validate_paths` red case for this object-shaped attack and assert `analyze_step_unauthenticated`; retain a positive keyed-object receipt using the authentic argv shape. Hardening only `_is_analyze_step` leaves this bypass open.

### Medium — D6d invalidates existing green fixtures unless they are updated

**Observation:** Three currently green fixtures do not meet D6d’s package-token rule: the no-flag object fixture uses `argv=["npx", "analyze"]` (`:964-972`); the flagged object green fixture also uses that argv (`:989-1003`); and the list-shaped declared-name fixture uses `name="analyze", argv=["true"]` (`:1093-1103`). `_is_analyze_step` currently falls back to `bool(declared)` when it cannot derive a command (`:148-161`), which explains the latter green expectation.

**Inference:** If D6d authentication is enforced for analyze steps in all validation modes, these fixtures should become red and make the selftest fail. Replace their argv with the canonical package-token form; keep a separate invalid-argv fixture asserting the new finding. Whether the no-flag case is expected to authenticate is governed by the D6d contract, not the old verdict-only behavior.

### Medium — Several rejection paths have no finding-specific red selftest

**Observation:** The suite covers green retain/carrier receipts, tampered-file exit 1, one forged `pins_compare.changed`, binding-log mismatches, pin drift, selected mid-map failures, and an unreadable receipt (`:817-843`, `:845-901`, `:903-954`, `:956-1124`). It does not assert red findings for: unknown receipt shape and required/type errors (`:373-438`); `carrier_not_pinned` or absent/empty bound sessions (`:171-185`); `missing_file`/`unreadable_file` (`:249-269`); malformed pin entries (`:295-329`); `pins_compare_error` or mismatches in `equal`/`missing`/`errors` (`:442-482`); or mid-map write error, incomplete/missing-on-disk/unparseable map, timestamp/entry-count mismatch, absent pre-snapshot, and compare exception (`:526-605`). The tampered-file case checks only exit 1, not a `size_mismatch` finding (`:826-833`); the only unreadable case is a missing *receipt* path (`:1121-1124`). The list identity negatives test a helper return value rather than a validator finding (`:1105-1112`).

**Residual risk:** The archived selftest stdout says `SELFTEST: CLEAN cases=26` (`.ufo/waves/round-19/verify/selftest-w17-receipt-validate.stdout:1`), but that result does not demonstrate the above untested rejection properties.

## Retained-receipt compatibility

**Observation:** The 15 round-18 `runs/*/receipt.json` and 8 round-19 `runs/pass2/*/receipt.json` inspected all use object-keyed steps, with `analyze.argv` in the required `npx -y rea-agents@6.5.0 analyze ...` form. Representative records: round 18 `.ufo/waves/round-18/runs/real-kimi-webbridge/receipt.json:1922-1924`; round 19 `.ufo/waves/round-19/runs/pass2/t1250-vet/receipt.json:1924-1926`. Each also has an `inspect-go-binary` step, whose command must not be mistaken for the analyze step.

**Inference:** The strict D6d check should preserve these retained receipts if it authenticates the object key’s associated argv and accepts the observed npx form. A fix that only recognizes list-shaped entries, requires an explicit `step`/`name` field despite object keys, or applies analyze-command requirements to every step could break them. No inspected retained argv itself appears incompatible with the contract.

## Verification and gaps

- **LSP:** `xd://lsp` is not mounted (`No such tool`); no LSP status/references/definition/diagnostics were available. Findings use direct source and receipt reads; text search was used only for line anchors.
- **Command:** `cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && git --no-optional-locks rev-parse refs/heads/main; echo "rc=$?"; git --no-optional-locks diff --stat 14f0260ad319ecc26994381b2415d5a999003375 -- .ufo/waves/round-17/tools/receipt-validate.py; echo "diff_rc=$?"` — exit markers: `rc=0`, `diff_rc=0`; main was `d1d981d2cc041dda4656c5b01d2c8445d8d17124`, and the target had no diff from the stated baseline.
- No test/build command was run for this review; the selftest result above is read from the recorded stdout artifact (its exit code is not recorded there).