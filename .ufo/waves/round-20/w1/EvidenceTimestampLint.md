# Evidence Timestamp Linter — EvidenceTimestampLint-2

## Implementation
**Observation:** Added `.ufo/waves/round-20/tools/evidence-timestamps.py` in the isolated clone at baseline `14f0260ad319ecc26994381b2415d5a999003375`. It enumerates tracked blobs at the selected revision, skips NUL-containing or over-4-MiB blobs with reasons/sizes in JSON, parses the requested zoned formats, and compares each occurrence with the `committer-time` supplied by `git blame --porcelain REV -- path` for that specific line. Quoted timestamps are not filtered. Findings are retained in JSON when `--allow FILE:LINE` marks them exempt; the allow entries and whether applied are also recorded, and `--strict` exits 1 only for non-exempt findings. See tool lines 24–36, 88–121, 124–176, 201–278, and 422–451; contract D2 is `contract.md:41-45`.

## Red-before evidence
**Observation:** At revision `14f0260ad319ecc26994381b2415d5a999003375`:

- `.ufo/waves/round-19` — 751 scanned text blobs, 0 skipped. Finding: `future_dated claims.json:36`; line timestamp `2026-10-20T16:20:00-03:00`, introducing commit time `2026-10-20T19:09:17Z` (16:09:17 -03). This matches the requested red-before at `round-19/claims.json:36`.
- `.ufo/waves/round-18` — 767 scanned text blobs, 0 skipped. Finding: `future_dated claims.json:35`; line timestamp `2026-10-20T13:25:00-03:00`, introducing commit time `2026-10-20T16:23:55Z`.
- `.ufo/waves/round-17` — 580 scanned text blobs, 0 skipped. Findings: none.

The paths above are relative to each requested `--path`, as the JSON findings show.

## Selftest
Final run output (tool selftests at lines 336–419):

```text
PASS future_line_flagged
PASS past_line_clean
PASS zulu_and_offset_parsed
PASS later_commit_line_uses_own_time
SELFTEST: CLEAN cases=4
```

Exact last line: `SELFTEST: CLEAN cases=4`; exit 0. The first two runs also exited 0; the initial scans then exposed a blame-group parsing error, which was corrected before the final scan/selftest runs.

## Commands and exits
Commands ran from `/tmp/kr20-EvidenceTimestampLint-2` unless noted. Each command and its exit:

- `git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/kaidoku-shokunin /tmp/kr20-EvidenceTimestampLint-2 && git -C /tmp/kr20-EvidenceTimestampLint-2 checkout -q --detach 14f0260ad319ecc26994381b2415d5a999003375 && git -C /tmp/kr20-EvidenceTimestampLint-2 rev-parse HEAD` — exit 0; printed `14f0260ad319ecc26994381b2415d5a999003375`.
- `git -C /tmp/kr20-EvidenceTimestampLint-2 rev-parse --show-toplevel && git -C /tmp/kr20-EvidenceTimestampLint-2 rev-parse HEAD` — exit 0.
- `mkdir -p /tmp/kr20-EvidenceTimestampLint-2/.ufo/waves/round-20/tools` — exit 0.
- `python3 -I -B .ufo/waves/round-20/tools/evidence-timestamps.py --selftest` — exit 0 on each of three runs; the final exact output is above.
- `python3 -I -B .ufo/waves/round-20/tools/evidence-timestamps.py --root /tmp/kr20-EvidenceTimestampLint-2 --rev 14f0260ad319ecc26994381b2415d5a999003375 --path .ufo/waves/round-19` — exit 2 on the initial parser attempt; exit 0 after parser repair; exit 0 after JSON output compaction.
- `python3 -I -B .ufo/waves/round-20/tools/evidence-timestamps.py --root /tmp/kr20-EvidenceTimestampLint-2 --rev 14f0260ad319ecc26994381b2415d5a999003375 --path .ufo/waves/round-18` — exit 2 on the initial parser attempt; exit 0 after parser repair; exit 0 after JSON output compaction.
- `python3 -I -B .ufo/waves/round-20/tools/evidence-timestamps.py --root /tmp/kr20-EvidenceTimestampLint-2 --rev 14f0260ad319ecc26994381b2415d5a999003375 --path .ufo/waves/round-17` — exit 2 on the initial parser attempt; exit 0 after parser repair; exit 0 after JSON output compaction.
- `git --no-optional-locks -C /tmp/kr20-EvidenceTimestampLint-2 blame --porcelain 14f0260ad319ecc26994381b2415d5a999003375 -- .ufo/waves/round-19/claims.json` — exit 0; observed per-line headers despite the first header's group-size field, leading to the parser correction.
- `mkdir -p /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/w1/patches && git -C /tmp/kr20-EvidenceTimestampLint-2 add -A && git -C /tmp/kr20-EvidenceTimestampLint-2 diff --cached --binary 14f0260ad319ecc26994381b2415d5a999003375 > /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/w1/patches/EvidenceTimestampLint-2.patch && git -C /tmp/kr20-EvidenceTimestampLint-2 diff --cached --stat 14f0260ad319ecc26994381b2415d5a999003375` — exit 0; `1 file changed, 455 insertions(+)`.


## Risk / blockers
**Risk:** Binary detection uses the NUL-byte heuristic; an unusual binary blob without NUL may be treated as text. Oversize blobs are skipped before content inspection and reported as `over_4_mib`. No blocker. No tools were installed or updated.
