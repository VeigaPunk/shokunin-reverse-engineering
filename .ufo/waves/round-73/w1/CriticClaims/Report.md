# CriticClaims receipt report

Canonical scoped findings: [../CriticClaims.md](../CriticClaims.md).

- C1: **falsified** for the original frozen base comparator (existing receipt 8/12, not 11/12). Identity-substitution attack additionally leaves the dirty worker unobserved; A12 fails closed, not falsely green.
- C2: **not falsified** numerically; D1 accepts a wrong-hash-only prose correction (false → true), demonstrating atom unsoundness.
- C3: **not falsified** for the enumerated frozen patch set; four additional wrong implementations retain all 38 green selftests.

Evidence: [attack-receipt.json](attack-receipt.json); reproduction: [attack.py](attack.py). Scratch removed by EXIT trap. No production changes or installations.
