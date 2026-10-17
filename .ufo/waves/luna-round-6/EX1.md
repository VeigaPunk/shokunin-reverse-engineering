## CLAIM
L1 matched the preregistered prediction: `rea-agents@6.5.0 --version` returned exact version `6.5.0` with exit code 0.

## METHOD
From `/tmp`, ran `timeout 240 npx -y rea-agents@6.5.0 --version`; captured stdout and stderr separately. Receipt: `.ufo/waves/luna-round-6/receipts/leg-1.md`.

## FINDINGS
stdout: `6.5.0`; stderr: empty; exit code: 0. stdout sha256: `3eb8e06ca1e02f0a30b0e3eebd289494b35d4fd1466ed907b9148e03b2459b00`.

## THREATS
This leg does not verify host mutation outside `/tmp`, operator-config drift, package inventory provenance, or the other battery legs. No broader host/config audit was performed.

## VERDICT
CLEAN
