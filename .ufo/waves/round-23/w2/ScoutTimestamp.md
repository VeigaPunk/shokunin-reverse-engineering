# ScoutTimestamp — R23-C1

Snapshot inspected: candidate commit `2838351450ff1ee4baa620c962a1153450d53311` (baseline named by the round claims: `aa1450b82f9ede35aada63efe8a34e01c6e02f72`). Static inspection only; no checker invocation or selftest was run in this seat.

## Findings

- **Observed — final-pass command is wired to the shipping source revision.** In `.ufo/waves/round-20/verify.py` (pinned blob `60140699ebab8ec574cf8e9d289af2422a3818d8`), `build_plan` labels `evidence-timestamps-source` and passes `--root LANE --rev source --path .ufo/waves/round-20 --strict` (lines 299–303), with expected exit 0 (line 67). `source` is resolved as a commit (lines 311–322). The runner executes a source-path command only when the corresponding worktree file is present and SHA-256-identical to the blob at that revision; otherwise it records a skip with an unexpected exit (lines 404–436). This checks the scoped tracked tree at the named shipping revision, not the mutable working tree.

- **Observed — comparison authority is line-introducing committer time, not author time or report time.** The checker blob is `be0452eb44294d69d121d04ab571cf0252f2d8c2`. `_parse_blame` reads `committer-time` from porcelain blame headers (lines 129–163); `collect` invokes `git blame --porcelain` for each text blob and compares each explicit-zone parsed instant strictly against that line's committer epoch (lines 212–240). The timestamp grammar requires a timezone (`Z` or numeric offset; lines 25–30, 117–126). `--strict` exits 1 only when unexempted findings remain (lines 421–450); the final-pass argv supplies no `--allow` (verify.py:299–303). Tool/argument errors return 2 (checker lines 439–446).

- **Observed — binary skips are explicit but NUL-heuristic only.** The checker reads Git blob objects at the selected revision, skips a blob only when its bytes contain NUL, and records `{path, reason: "binary", size_bytes}` (checker lines 81–114, 201–215). The summary exposes the skip count and says every skip needs review; it explicitly states text blobs have no size-based skip (lines 251–263). The selftest source contains a >4 MiB text fixture asserting zero skipped files (lines 386–396); this is source evidence, not a test run by this seat. NUL-free binary data is not guaranteed to be recognized; the report's risk note agrees that this remains possible (`.ufo/waves/round-20/w1/EvidenceTimestampLint.md:42–43`).

- **Observed — one W1 implementation summary is stale against this pinned checker.** `EvidenceTimestampLint.md:4` says blobs over 4 MiB are skipped, and `:43` says oversize blobs are skipped as `over_4_mib`; neither behavior exists in the pinned checker, whose skip condition is NUL-only and whose summary says “no size skip” (`be0452…`, lines 207–210, 251–255). Treat the pinned source as authoritative for this candidate, not that older summary.

- **Observed — source quotations and capture timestamps are different facts, and the checker does not classify by provenance.** `EvidenceTimestampLint.md:9–10` quotes timestamps from the prior round-19/18 claims and their introducing commits; they are report-source quotations, not timestamps captured by the round-20 verification runner. Blame at the pinned candidate assigns both report lines to committer epoch `1792530874` (`2026-10-20T21:14:34Z`). The quoted values (latest `2026-10-20T16:20:00-03:00` = `19:20Z`, with the other quoted times earlier) precede that report-line committer time, so these examples are not future-dated relative to their report lines. The checker nevertheless scans timestamp-looking quotations like any other tracked text occurrence; it uses the quotation line's own blame committer time, not the original cited file's time. Separately, `verify.py` records actual command-capture fields `started_at_utc` and `ended_at_utc` (`:182–219`); those are runtime receipt timestamps, not source quotations.

- **Unknown — no final shipping run/result is evidenced in this candidate snapshot.** `VerifyR20.md:11` states that only a dry-run against `SOURCE=B` was done at that stage, with no full pass and no `verification.json`; `:15,40,52–53` mark the command table as planned and the dry-run as executed. In the pinned commit, `.ufo/waves/round-20/verification.json` and `verify/evidence-timestamps-source.stdout` are absent (`git show` for each returned exit 128). Thus the invocation is correctly wired in source, but this snapshot does not establish its final-run exit, findings, or actual binary skip list. Do not present the planned expected exit as observed success.

- **Observed — semantic LSP unavailable.** `xd://lsp` returned “No such tool” and the mounted device inventory contained no LSP device. Definition/caller tracing above is from pinned Git source only; no grep result is offered as semantic proof.

## Commands / exits

- Pinned `git show` reads of `verify.py`, `tools/evidence-timestamps.py`, `w1/VerifyR20.md`, and `w1/EvidenceTimestampLint.md`: exit 0.
- Pinned `git blame --line-porcelain -L 9,10` on `w1/EvidenceTimestampLint.md`: exit 0; both lines report `committer-time 1792530874`.
- Pinned `git show` for `.ufo/waves/round-20/verification.json` and `.ufo/waves/round-20/verify/evidence-timestamps-source.stdout`: exit 128 each (path absent at the candidate commit).
- No tests, builds, lint, formatters, or checker invocations run.

## Produced files and hashes

- `.ufo/waves/round-23/w2/ScoutTimestamp.md` — SHA-256 supplied in the final handoff (self-hash is not embedded in this file).

## Installs

- None.

## Open risks

- A NUL-free binary blob may not be skipped as binary.
- Final shipping output and the skip list are not retained in the inspected commit, so actual execution remains unverified.

Report: `.ufo/waves/round-23/w2/ScoutTimestamp.md`
