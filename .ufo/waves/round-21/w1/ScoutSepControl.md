# D6d control isolation — read-only findings

## Axes
- **Calibration:** demonstrate both an accepted, well-formed positive receipt and a rejected decoy without round-20 C3 evidence.
- **Depth:** exercise the validator’s full `--require-mid-maps` receipt path, not only its argv predicate.

## Observed source facts

- `.ufo/waves/round-20/tools/routed-r19.py:908-961` is `_s_d6d`. It makes an empty carrier/stdout/stderr and a sparse synthetic decoy receipt (`:910-940`), but sets `control` to the external-in-scope C3 artifact `.ufo/waves/round-20/runs/t1246-addr2line/receipt.json` (`:941-942`). It passes both to the revision-pinned `receipt-validate-v2.py --require-mid-maps` (`:943-944`), then requires an `analyze_step_unauthenticated` finding and a valid control entry (`:947-961`). Thus the *current harness’s positive* depends on that C3 receipt; removing it breaks the positive assertion. This is consistent with the round-20 lesson’s explicit R20-SEP note at `corpus/lessons/round-20-verifier-spotcheck.md:134`.
- A local synthetic full receipt pattern already exists in `.ufo/waves/round-17/tools/receipt-validate-v2.py:747-809` (`_carrier_receipt`): it supplies carrier bytes/digest, step fields, retained log/bound-session fields, and pre/post pin snapshots. The selftest’s good synthetic log and baseline full-receipt acceptance are at `:868-887`.
- Full positive behavior under the required mid-map option is independently fixture-tested at `receipt-validate-v2.py:1007-1028` (`carrier_flag_mid_map_green`): it creates a pin snapshot file, records its path and digest on the genuine `npx -y rea-agents@6.5.0 analyze` step, and expects exit 0. A list-shaped full positive is also at `:1107-1118`.
- Decoy behavior is fixture-tested at `receipt-validate-v2.py:1142-1167`; its post-package second `rea-agents@6.5.0 analyze` token yields `analyze_step_unauthenticated`. The adjacent `:1168-1179` positive/negative direct `_is_analyze_step` checks are predicate-level only, not a full-receipt positive.
- Validator documentation at `receipt-validate-v2.py:33-40` states the option’s relevant conditions: map fields for checks and a retained check on the unique step whose argv has `analyze` immediately after a versioned package token; declared names or a token elsewhere do not authenticate it.

## Advisory isolation design (inference from those fixtures)

Replace only the hard-coded `control` path with a second locally generated, complete carrier receipt. Reuse the selftest’s `_carrier_receipt` data shape and synthetic pin/log construction; give the control an actual analyze argv and a generated mid-map (`pins.snapshot`, serialized map path, matching SHA-256) attached to that analyze step, following `carrier_flag_mid_map_green`. Keep a separately generated decoy receipt with the existing decoy argv, or base it on the same complete carrier shape; preserve the assertion that the validator reports `analyze_step_unauthenticated`. Run both temporary receipts through the existing `--require-mid-maps` invocation and retain the current assertions: overall exit 1, decoy finding present, and control receipt `valid is True`.

This gives the harness a full-validator genuine positive and a decoy, with no C3 receipt or analyzed carrier execution. A raw `_is_analyze_step` positive alone is not an adequate replacement for the current `valid is True` assertion. When constructing the fixture, preserve all required carrier/log/pin fields and put a valid map on the genuine analyze step; otherwise unrelated receipt or mid-map findings would make the positive non-genuine.

## Limits and checks

- No code or source rows changed. Read/search only in the R20 routed counter, R17 successor validator, round-20 lesson, and frozen round-21 fixture contract. No tests, REA/provider tools, carrier execution, or external URLs were used; no tool was installed.
- Unresolved: this is source-only analysis; no new paired receipt was constructed or run, so acceptance of the proposed synthetic composite is not an observed result. The cited validator selftest establishes the constituent positive and decoy fixture patterns, not this proposed D6d harness change.
- Parent verification after any implementation: run the targeted routed D6d counter at the proposed revision, then the frozen C1 battery exactly as declared in `.ufo/waves/round-21/claims.json`: `python3 -I -B .ufo/waves/round-21/battery.py --root <LANE> --rev <REV> --claim C1`. Ensure all twelve frozen C1 cases remain in the denominator. Parent owns these checks.

Report: .ufo/waves/round-21/w1/ScoutSepControl.md
