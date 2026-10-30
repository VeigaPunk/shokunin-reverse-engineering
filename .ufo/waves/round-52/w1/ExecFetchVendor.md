# ExecFetchVendor

Verdict: blocked / partial draft only.

- `ExecFetchVendor/fetch-vendor.py` is based on the exact round-50 fetcher source, preserving the hash chain, SquashFS extraction/carving, and existing synthetic chain selftest. It changes the table default to `tools/round-52/carriers.json`, adds `--prior` for `tools/round-50/carriers.json`, adds `--carrier-table`, and implements offline `--plan` output for URL, image hash, member path and member hash.
- The source guard conditions are the original initial-fetch and redirect checks: each checks `u.scheme != 'https' or u.hostname != ALLOWED_HOST` against `ALLOWED_HOST = 'download.avm.de'`. This pins hostname and scheme, not port/proxy; same-host HTTPS redirects remain permitted.
- Required guard-deleted fixture copies and observations were NOT completed. Existing selftest does not prove those deletions go red; no fetcher selftest, plan, or mutation test was run. No claim of green or measured fail-closed mutation evidence.
- Review caught an intermediate reduced draft with broken chain semantics; it was replaced by the exact round-50 source before editing the extension. A subsequent locator error was corrected. Final source has not been runtime checked.

Artifacts: `.ufo/waves/round-52/w1/ExecFetchVendor/fetch-vendor.py`, `deltas.md`, `status.json`. No vendor URL accessed; no vendor bytes used. No tools installed. Scratch path `/fast/scratch/hyaku/kaidoku-r52/w1-ExecFetchVendor` remains and was not removed.
