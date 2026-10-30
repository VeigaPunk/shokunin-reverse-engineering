# ExecCensusCheck findings

At round-52 base `ab0eafedc41402b43b41a4362084119578dfe7ce`, `census3.py --check` returned exit 0 with 56 registry paths, 56 census paths, and empty `census_outside`, `census_unregistered`, and `duplicates`. Historical mode returned exit 1 with 14 `census_outside` paths (not 13), no unregistered paths or duplicates, using frozen `tools/round-48/census2.json`. The exact stdout, command, exit, SHA-256 and UTC timestamps are retained in the seat directory receipts.

The v6 instrument's census clause must independently derive/compare census membership at both base and landing, requiring `census_outside == []` (count 0) at each endpoint; preserve the no-regression binding. The base observation is clean; landing was not available/run in this wave. Historical output has 14 outside entries, contrary to the assignment's expected 13; the raw receipt is authoritative.

`census3.py` functions relevant to porting the clause: `safe_path`, `read_at`, `exists_at`, `registry_paths`, `derive`, and `compare_paths`; `main` dispatches the check/historical modes and exit semantics. Full source inspection was not available beyond the displayed declaration excerpts.
