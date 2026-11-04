# SentinelScope

Detailed findings and reproducible evidence: [SentinelScope/SentinelScope.md](SentinelScope/SentinelScope.md).

- **SS72-1 — advisory:** caller PATH controls A11 real git/readelf and shell cat; private shim parents prevent ordinary cross-user preplanting, not malicious tool provenance.
- **SS72-2 — blocking:** receipt-named absolute, traversal and symlink capsule paths read outside the lane. Harmless `/etc/hostname` probes all rejected after reading; direct audit exposed its matching SHA256.
- **SS72-3 — advisory:** capsule selftest ignores supplied --work; default tempfile honors TMPDIR, otherwise system temp fallback. No hardcoded /tmp write or world-writable mkdtemp found.
- **SS72-4 — advisory:** fixed canary values occur in frozen committed sources; they are nonsecret markers, not a confidentiality proof.
- **SS72-5 — blocking:** executed checker, controls and mutation failure cases leak allocated scratch. Additional seam/battery/route and child-timeout cleanup gaps are source-observed.
- **SS72-6 — fixed-in-round:** reviewed environ data and receipt argv do not grant write destinations; QUALITY 120 separation preserved in these paths.

Reviewed all six frozen instruments, without modifying them. Probe receipts copied under this seat's evidence directory before its single scratch directory was removed by finally. No installations, offensive executable probes, claim adjudication or integration.
