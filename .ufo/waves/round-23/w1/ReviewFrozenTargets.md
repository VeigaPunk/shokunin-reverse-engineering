# Frozen T1 target review (R22 → R23)

Scope: inherited C1 target identity, denominator, and threshold only. This is an author-side review of the frozen declarations and retained baseline record, not independent admission of the claim.

## Findings

- **Medium — R23's declared counting command is absent, so denominator-shrink rejection is not demonstrated.** `.ufo/waves/round-23/claims.json:27` designates `.ufo/waves/round-23/tools/count-c1.py`; the inspected `round-23/tools/` inventory contains only `make-uart.py`, `setup-sigrok.py`, and `sigrok-cli.sh`. The retained `before-r22-c1.json:2-12` records a run of the R22 counter instead, not the designated R23 counter. Therefore the frozen declaration's six-item denominator is visible, but the current tree provides no R23 counter with which to check that a later count rejects a shortened denominator or reports `k/6`. This finding is about missing enforcement evidence; it is **not** an observed shrink in the declarations.

## Confirmed declaration boundary

- **Exact identity:** R22 C1 `.ufo/waves/round-22/claims.json:17` and R23 C1 `.ufo/waves/round-23/claims.json:16-23` declare the same six verbs in the same order: `identify-flutter-build`, `inspect-dart-aot`, `debug-with-gdb`, `debug-with-rizin`, `inspect-signal-decoders`, `decode-signal-recording`. No item was removed, substituted, or reordered in the R23 declaration.
- **No denominator shrink in the frozen values:** R23 explicitly declares `total: 6` and the list above has six entries (`claims.json:24-25`). R22's criterion also reports `k/6` (`round-22/claims.json:20`). The scoped diff from R23's declared baseline `aa1450b82f9ede35aada63efe8a34e01c6e02f72` adds the R23 claim and its baseline record; it does not modify the R22 claim file.
- **Threshold is `>=2/6`, not `6/6`:** R22's C1 target was `k/6` with `k>=1` (`round-22/claims.json:20`). R23 sets `before: 1`, `total: 6`, and a cumulative target of `>=2/6` with exact `k` reported; completeness remains incomplete unless `k=6` (`round-23/claims.json:24-26`). It expressly says `6/6 before observed` is not claimed (`claims.json:46-51`). This is a stricter minimum held-count threshold, not a claim of complete coverage.
- **Recorded inherited count:** `.ufo/waves/round-23/before-r22-c1.json:2-15` documents argv for the R22 counter at revision `aa1450b82f9ede35aada63efe8a34e01c6e02f72`, exit `1`, and empty stderr. Its retained stdout parses to `t1_total: 6`, `t1_exercised_count: 1`, and `t1_exercised: ["identify-flutter-build"]`. This is the recorded prior count, not a run of the absent R23 counter. R23's no-harm text also preserves `R22 C1=1/6` (`claims.json:55-61`).

## Residual risk and verification gaps

- The declaration currently preserves the exact six-verb T1 and a denominator of six, and its stated threshold does not overclaim 6/6. The missing R23 counter leaves the required operational guard against denominator shrink unverified; the declaration alone cannot establish counter behavior.
- No R23 final `k/6` result is reviewed here. Source relevance, ownership, and claim admission are outside this frozen-target boundary.
- No LSP or grep-based semantic claims were used; the reviewed files are frozen JSON declarations/records, and no LSP device was exposed in this seat's tool inventory. No tests or builds were run; none were assigned.

## Installs

None.
