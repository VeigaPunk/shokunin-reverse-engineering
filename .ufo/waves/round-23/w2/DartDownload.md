# DartDownload — source review (R23-C1, candidate 2838351450ff1ee4baa620c962a1153450d53311)

Scope: `legacy-saber-download.json` and the L1 Dart subject digest. Committed
bytes only via `git show 283835145…:<path>`; no producer replay, no fetch, no
execution. All file references are blobs at the candidate commit unless noted.

## Verdict

The four assigned properties hold. Two low-severity gaps: the HTTP-status and
"independently fetched" producer claims are self-asserted scalars with no
retained acquisition transcript, unlike R22's download record.

## Axis checks (observed)

- **Public URL — holds.** `legacy-saber-download.json` `url` =
  `https://f-droid.org/archive/com.adilhanney.saber_1330203.apk` (line 3).
  Same URL committed in `connect-dart-symbols/fetch.json` (`downloads[0].url`),
  `connect-dart-symbols/README.md` (Artifacts footer), and
  `corpus/knowledge/2026-10-21-r23-dart-legacy-layout-boundary.md` (source line
  and body). Retained in multiple committed locations.
- **Full digest — holds, independently bound twice.**
  `sha256` = `a7b1f5c8c077aafc8903eb8246d9b6f5fc8ebb4829dc5cb32bd2cdd8ba3ea618`.
  (a) Equals `inspect-dart-legacy-saber.envelope.json`
  `data.subject.digest.sha256`, the run.json stdout subject digest, and
  `normalized_result.target.sha256` — provider-computed over the file actually
  analyzed, not the producer's self-report. (b) Equals `fetch.json`
  `downloads[0].index_entry.hash` (sha256 declared by the F-Droid archive index
  entry) — a second, index-side binding for the same digest, plus
  `index_entry.size` 41263437 = record `size` = `normalized_result.target.bytes`.
  `tools/describe-dart.py` recomputes `subject_digest_matches_fetch:true`;
  `verify/initial/dart-record.json` confirms `passed:true` at rev 6615aeae.
- **No signing-chain claim — holds.** Record carries
  `signature_verification: "not performed; digest identity only"`. Knowledge
  file states "HTTPS plus digest identity is not a verified F-Droid signing
  chain; no archive-index/APK signature verification is asserted." LOG.md
  (~line 2607) says only "independently fetched … digest is a7b1f5c8…". No L1
  record asserts APK-signature, index-JAR, or signer-cert verification.
  (Connector-side `fetch.json` retains index `signer`/`sig` fields but with an
  explicit NOT-verified `signature_note`; consistent, not an L1 claim.)
- **Ignored APK not sole reproducer — holds.** `.ufo/waves/round-23/.gitignore:1`
  `/runtime/` ignores `runtime/saber-1330203.apk`; the blob is uncommitted by
  design. Reproduction is fully specified by committed URL + full sha256 +
  size; the knowledge `recheck:` line names re-fetch of "the exact
  digest-pinned public APK" and README repeats URL+digest. The record's `path`
  and the envelope's `subject.local_path` reference the ignored copy, but no
  claim treats it as the reproducer — disclosed, not hidden.

## Findings

1. **Low — acquisition transcript not retained; `status`/`captured_at` are
   self-asserted.** `legacy-saber-download.json` records `status:200`,
   `size`, `sha256`, `captured_at` but no fetch argv/stdout/stderr/exit or
   response headers. R22's `saber-download.json` (round-22/evidence/sources/)
   retained the full curl argv, exit, and `%{http_code}` stdout. Claimed fields
   `status` and `captured_at` are therefore asserted, not independently bound —
   only their digest/size *outcome* is bound by the envelope and index entry.
   (Timestamp ordering is at least internally consistent: download
   `captured_at` 14:47:18.289 precedes run `captured_at` 14:47:19.045.)
2. **Low — "independently fetched bytes" provenance is self-asserted.**
   `producer` claims an independent fetch after the connector's scope
   deviation; LOG.md repeats "independently fetched … Saber1330203". Retained
   bytes cannot distinguish an L1 re-download from a copy of the connector's
   `/tmp/kd23work/saber-1330203.apk` — the differing `local_path` is compatible
   with either, and the matching digest only binds byte identity, not the
   acquisition event. Given the disclosed ConnectDartSymbols deviation, the
   "independent" qualifier rests on self-report. Harmless to integrity (the
   digest pins the bytes regardless) but the independence claim exceeds what
   the records bind.
3. **Informational — `envelope.json` is byte-equal to run.json `stdout`.**
   Verified via `dart-record.json` `stdout_byte_equal:true` at source rev
   6615aeae and matching envelope sha256 `7768198e…`; the "untouched original
   envelope" wording in the knowledge file is accurate. No defect.

## Produced files

- `.ufo/waves/round-23/w2/DartDownload.md` (this report; new file, no prior
  DartDownload report overwritten).

## Installs

None. Read-only wave; git show + python3 json only.

## Open risks / verification gaps

- Whether the F-Droid URL still serves those exact bytes today is unverifiable
  under lane bounds (no remote access, no producer replay); the committed
  digest pin is the mitigation, and archive permanence is assumed not asserted.
- Residual: findings 1–2 mean the fetch event's provenance (who fetched, HTTP
  status, when) is weaker than the byte identity it produced. If outside
  admission ever requires distinguishing re-fetch from copy, the transcript
  gap is the blocker; for R23-C1 counting (original-envelope binding) the
  digest chain is already sufficient.
