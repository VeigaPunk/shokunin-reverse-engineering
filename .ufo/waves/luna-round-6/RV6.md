## CLAIM
Cannot verify whether the ten executors used the SC-seat’s selected carriers; no carrier substitutions can be confirmed or ruled out from the available evidence.

## METHOD
Checked the wave directory with `ls -la .ufo/waves` and attempted `ls -la .ufo/waves/luna-round-6 .ufo/waves/luna-round-6/receipts` from the repository root. The first listed only `luna-round-1` through `luna-round-5`; the second returned `No such file or directory` (exit 2). Thus neither the SC-seat scout report nor leg receipts were available for comparing carrier SHA-256 values against receipt commands.

## FINDINGS
No `luna-round-6` artifacts were present at audit time. Because the required scout hashes and executor receipt commands are absent, no per-leg continuity check is possible and no substitution finding is supported.

## THREATS
Concurrent wave artifacts may be created after this check. This report is a snapshot, not evidence that the eventual battery used the intended carriers.

## VERDICT
FINDING: Carrier continuity is unverifiable because the SC report and round-6 leg receipts were absent at audit time.
