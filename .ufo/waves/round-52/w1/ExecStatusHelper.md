# ExecStatusHelper

Verdict: settled. Added `.ufo/waves/round-52/w1/ExecStatusHelper/wave-accounting.py`.

- Enumerates seat directories and reports valid settled/failed/blocked counts, role totals, and missing/malformed statuses as unknown without crashing.
- `--check` validates every expected name from a JSON array or newline-delimited file and exits 0 only for parseable, matching seat records with valid status; failures exit 1 (unreadable expected file exits 2).
- `--selftest --work PATH` uses that scratch path; absent `--work`, it honors `TMPDIR` (then platform temp directory).
- Selftest receipt: `ExecStatusHelper/selftest-receipt.json`; exact executed invocation, exit 0, UTC timestamp `2026-10-30T10:46:34Z`, stdout SHA-256 `8003bf6d38a5dcf1f5be30885ea10d8ffc408bba6bfb7e51de84d32831902ac9`. Fixture had one settled, one failed, one malformed and one missing seat; passed.
- No installation performed. Other checks not run.

Risk: role totals include only parseable records with a nonempty string role. `--check` checks the expected names, independent of unrelated extra seat directories.