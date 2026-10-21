# R22-C1 unsupported-metadata review

## Finding

**P2 — C1 accepts a directory citation where its contract requires a full evidence-file path.** In `tools/count-c1.py:4-8`, the counter says each qualifying knowledge entry cites a retained evidence *file* by full lane path. But `count-c1.py:111-115` calls `r20.is_cited(path, cited)`, and the inherited helper at `.ufo/waves/round-20/tools/verb-coverage.py:127-133` treats any cited value ending in `/` as a directory prefix (`path.startswith(c)`). As a result, citing only `.ufo/waves/round-22/evidence/c1/` permits any candidate file below that directory to supply the matching ID and operation.

I reproduced this against the current target: starting with the positive six-verb fixture, I replaced only the `inspect-dart-aot` entry's exact file citation with the directory prefix. The counter still returned `finding: c1_complete`, `t1_exercised_count: 6`, and listed `.../evidence/c1/inspect-dart-aot.json` as bound evidence; exit was 0. The evidence JSON itself remained a matching, non-refused CLI envelope. This is a concrete path-specificity false positive, not a claim that the counter provides cryptographic authentication (its `limit` expressly disclaims that).

**Narrow fix:** for C1, require the candidate path to appear as an exact citation (`path in cited`) rather than calling the directory-aware `r20.is_cited`. Add a directory-only citation mutant to the C1 fixtures; it should produce five exercised verbs / exit 1. Keep the generic R20 helper unchanged if its directory-citation behavior is needed by other counters.

## Targeted metadata check (no finding)

The requested “matching ID and operation only under arbitrary metadata” case did **not** count. I placed both fields only under `data.metadata`, with no record at a supported evidence carrier. The target reported `c1_incomplete`, count 5, left `inspect-dart-aot` unexercised, and listed the candidate file under `unsupported_candidates`; exit was 1. This agrees with R21 `records()` walking only its named carriers (`evidence`, `evidences`, `records`, `result`) rather than arbitrary keys (`round-21/tools/verb-coverage.py:58-75`). No separate arbitrary-metadata false-positive finding was observed.

## Probe records and output

All probe repositories were private temporary Git fixtures. Dependencies were copied from the lane, and the fixture's retained CLI catalog was reduced to the six frozen T1 names so the counter's stdout stayed bounded; do not read these runs as a production-catalog measurement. Exact argv, exit, stderr, and losslessly retained stdout are in the same-name `C1Unsupported.json` attachment. Each stdout is zlib-compressed then base64-encoded there; decode with `base64 -d` followed by zlib decompression. `stdout_bytes` and SHA-256 are recorded for every observation.

| Case | Exact command args (after executable) | Exit | Observed stdout fields | stderr |
|---|---|---:|---|---|
| Positive six-verb control | `-I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-22/tools/count-c1.py --root /tmp/kaidoku-c1-capture-8tnd22yr --rev c65e93c72517dadf1673ae3df012fa73878e5e70` | 0 | `finding=c1_complete`, `t1_exercised_count=6`, all six T1 verbs exercised | empty |
| Directory-only citation adversary | `-I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-22/tools/count-c1.py --root /tmp/kaidoku-c1-capture-xvnw23s5 --rev f6106330d3377f1ff52e9e22eb5cacf78692c0f8` | 0 | **Same complete result**, including the unambiguously bound `inspect-dart-aot.json` file despite only its parent directory being cited | empty |
| Matching fields only under `data.metadata` | `-I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-22/tools/count-c1.py --root /tmp/kaidoku-c1-capture-vil1i6v4 --rev aa44e47a140ac676cbd06185d0d69c14691a142f` | 1 | `finding=c1_incomplete`, count 5; `inspect-dart-aot` unexercised and candidate reported unsupported | empty |
| In-tree fixture selftest | `-I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-22/tools/count-c1.py --selftest` | 0 | `finding=counter_controls_clean`; 18 listed cases all passed (including source, refusal, split-record, wrong-command, extraction-only, debug-operation, helper-drift, and invalid-revision controls) | empty |

The current selftest does not contain a directory-citation case, which is the regression gap behind the finding. Exact selftest stdout (100,470 bytes) is retained in the attachment as well.

## Scope and verification gaps

- The target was inspected after it changed during this review; an earlier probe against the pre-update CLI-envelope shape was discarded. All probe records above use the later current target.
- Diff against the frozen baseline shows `count-c1.py` as a new file. No lane source or production file was changed by this review; only the assigned report and attachment were written.
- No LSP device/namespace is exposed in this session, and `command -v lsp` returned no executable. I therefore make no semantic caller/reference/definition/diagnostics claim and used no grep as semantic proof.
- No tools were installed or updated. No build, formatter, or broad test suite was run; verification was limited to the requested bounded temporary-fixture probes and the counter's own fixture selftest.
- The target itself declares no cryptographic authentication and manual source relevance/scope admission as limits; those are not raised as additional defects here.
