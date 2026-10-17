## CLAIM
Score legs 1–5 against the frozen round-8 predictions using available receipt evidence only.

## METHOD
Ran `ls -la .ufo/waves && ls -la .ufo/waves/luna-round-8`. Output listed `luna-round-1` through `luna-round-7`; the second lookup returned `ls: cannot access '.ufo/waves/luna-round-8': No such file or directory`. No leg receipts were available to inspect.

## FINDINGS
- L1 — predicted exact version `6.4.0`, exit 0; observed: no receipt; **UNSCORED**.
- L2 — predicted exactly 170 tools; observed: no receipt; **UNSCORED**.
- L3 — predicted `inspect_go_binary` → TYPED-REFUSAL; observed: no receipt; **UNSCORED**.
- L4 — predicted `inspect_rust_binary` → TYPED-REFUSAL; observed: no receipt; **UNSCORED**.
- L5 — predicted `inspect_electron_fuses` → TYPED-REFUSAL; observed: no receipt; **UNSCORED**.

Scoreable: 0/5; matches among scoreable legs: 0/0. No prediction can be marked matched or mismatched without receipts.

## THREATS
Missing receipts do not establish that probes were not run; their outcomes, exit codes, stdout hashes, and match status are unverifiable.

## VERDICT
FINDING: L1–L5 remain unscored because no round-8 receipts were available.
