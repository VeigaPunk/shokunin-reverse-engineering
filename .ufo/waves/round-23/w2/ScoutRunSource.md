# R23-C1 — `verify.py` original-run comparison

**Scope:** read-only review of candidate snapshot `2838351450ff1ee4baa620c962a1153450d53311` (`B=aa1450b82f9ede35aada63efe8a34e01c6e02f72`). No producer, verifier, test, or target was run.

Source SHA-256s of exact `git show <candidate>:<path>` bytes:

- `.ufo/waves/round-23/verify.py`: `59833006e860631b8d4d6f381056744595769308b377072ceacc116781a4a21a`
- `.ufo/waves/round-23/tools/describe-signals.py`: `a669607c12fd2be84dd28c80d4826b415c21bae06ec28aa78b22f6fc564078c3`
- `.ufo/waves/round-23/tools/describe-dart.py`: `145b09bb734692a371ee6b4971de8a2270547826be840f92d435b40f86a5234f`

## Findings

- **Signal REA-pair scope is five entries; the generator is excluded.** `describe-signals.py:14-15` fixes `NAMES` to `inventory`, `uart-help`, `decode-uart-hi`, `decode-official-uart`, and `decode-invalid-decoder`; `verify.py:71` requires five returned records. `generate-uart.run.json` is a separate Python `make-uart.py` run (recorded exit 0, empty stderr), has no listed envelope pair, and is not included in `NAMES`. The generated `uart-hi.bin` is nevertheless used as a decode input: the pinned decode envelope's subject digest and the pinned carrier bytes both hash to `4a2e729f514482287c17596cff3b29f07141fae9e86353680c99b1065e861727`. Thus generator execution/provenance is not compared as an REA pair; carrier-byte identity is a separate check.

- **Signal comparison currently gates only pair count and stdout/envelope equality.** `verify.py:71` predicate is `len(records)==5 and all(stdout_byte_equal)`. The helper at `describe-signals.py:57-64` emits target, command/meta, and carrier-digest comparison fields only under limited conditions; the top-level predicate does not require any of those fields. Specifically, the two `inspect-signal-decoders` records route the wrapper through `env_overrides`, but there is no check binding that override or the subject digest to the claimed subject. The failing decoder record has no `data.subject`, so its argv target is not compared. For the successful decode records, the helper hashes the committed carrier blob and computes argv-target/digest booleans; it does not hash the bytes at the original argv target, and `verify.py` ignores those booleans. A mismatch could coexist with five stdout matches and pass this check.

- **Dart comparison gates target-path and fetch-digest consistency, but not meta-command or original stderr.** `verify.py:72` requires the helper's stdout-byte, subject/fetch-digest, and argv-target booleans, plus selected normalized-result fields. `describe-dart.py:47-49` compares the argv target path string to the subject path and the envelope subject digest to `legacy-saber-download.json`; it does not hash the file at the original argv target. It also computes `command_matches`, but `verify.py:72` does not consume that field. The helper does not report the original run's stderr. `verify.py:38-48` records stderr from its child summarizer process; that is not the original REA run's stderr. Consequently neither signal nor Dart predicates assert consistency of original-run stderr, and the signal predicate also does not enforce its emitted argv/meta/digest comparisons.

- **Observed artifacts are consistent in this snapshot, without strengthening those predicates.** Read-only projections of all five signal run records and the Dart run show empty `stderr`; their run `argv[3]` values match the respective envelope `meta.command`. The signal decode argv paths match the successful decode subjects; the `uart-hi.bin` and official `.sr` carrier hashes match those subjects. The Dart run argv target matches the subject path and the envelope subject SHA-256 matches `legacy-saber-download.json` (`a7b1f5c8c077aafc8903eb8246d9b6f5fc8ebb4829dc5cb32bd2cdd8ba3ea618`). Read-only byte-hash comparisons also matched run stdout to each of the five signal envelopes and the Dart envelope. These are observations about committed bytes, not proof that the verifier enforces every relation or that the records are authentic/continuous.

**Confidence:** high for checker behavior and explicit list membership (pinned source lines); high for the stated committed-record byte/value observations. **Unresolved:** no `lsp` device/server was available in this session, so this was a pinned-source textual trace, not semantic LSP confirmation. No source-level mechanism here authenticates the historical REA producer runs.

## Produced files and hashes

- `.ufo/waves/round-23/w2/ScoutRunSource.md` — created; its final SHA-256 is given in the handoff (not embedded self-referentially).

## Installs

- None.

## Open risks

- Do not treat currently matching retained values as evidence that `verify.py` fails closed on argv/meta/digest/stderr mutations; the checks described above are omitted from the relevant predicates.
