# MutDocSection — source/document binding mutation probe

## Result

**KILLED:** one private-counter defect weakening exact heading uniqueness from `!= 1` to `< 1`. The same bounded detector returned **0 / 1 / 0**, with **6/6 / 5/6 / 6/6** expectations satisfied on pristine / mutated / restored bytes. Only the duplicate-heading attack became accepted under the mutant. All five assigned attacks were rejected on pristine and restored counter bytes.

This is an isolated text/JSON result, **not a production reader score, a twelve-carrier predicate result, or source-authority adjudication**.

## Axes and frozen context

Axes: unique exact section binding; complete affirmative document bytes; exact source identity/capture bytes; false-accept sensitivity; bounded reversible isolation.

- Sandbox: `/fast/scratch/hyaku/kaidoku-r34/w1/MutDocSection`.
- Measured sandbox HEAD and supplied freeze both resolved to `54a87a51a865ab931fd355e767303337b05cccf4`; exact Git argv/output retained in `MutDocSection-files/preparation.json`.
- Counter instrument revision recorded by the frozen contract: `8897a67f6074580d6eac1a3fc0e37fdcd7aa0df0`.
- Predicate, preserved verbatim:

> P34-version-needs: twelve public ELF carriers yield exactly their independently frozen GNU version-needs records on opaque paths, including randomized same-length string-table naming wherever requirements are present, and the pinned source-backed decision table is present.

The isolated comparator uses its existing fixture interface with one benign TEXT record, not a replacement target for that frozen predicate. No contract, production counter, production parser, or shared document was changed.

## Detector and interfaces actually exercised

1. Copied the reviewed counter into the sandbox's private evidence directory; its pristine digest matched the frozen instrument digest.
2. Imported only that counter. Extracted the **unchanged AST statements at `measure()` lines 185–211**, covering document digests, approved SKILL section equality, exact source registry rows, frozen source pins and measured source bytes. Wrapped these statements solely to return `docs`; supplied a file-backed `blob` shim selecting frozen or candidate TEXT fixtures. This does **not** claim the production `measure()` CLI or Git transport ran.
3. Used the real `section(text, title)` implementation from the private counter. Frozen document/source hashes and exact source rows came from the copied frozen `claims.json`; the baseline SKILL/registry fixture contained the exact approved section and exact rows, with minimal surrounding text.
4. Passed the resulting `all(d['ok'] for d in docs)` to the actual outer CLI, `--fixture-spec ... --fixture-reader ...`. This exercised `fixture_measure`, manifest validation, scoring, JSON comparison, document gating, exits/findings, and two schedules of a fake reader which checks its input is the exact benign TEXT fixture before returning an empty record.

Every case in every phase had `matched=1`, fixture `target=1`, and both TEXT schedules matched. Thus the red exits below were document failures, not reader failures.

**Not exercised:** production `measure --root/--rev/--freeze`, instrument/manifest pin gates inside that method, real Git blob retrieval as binding transport, production ELF reader/carriers, string-table renaming, source semantic authority review, or a production score. No ELF/binary fixture was authored or executed. Held items and the prior builder were not used.

## Exact red/green findings

Each cell is `documents_ok / CLI exit / finding`. `T`/`F` mean true/false.

| Fixture | Pristine | Mutated | Restored |
|---|---|---|---|
| Canonical approved documents, section and sources | T / 0 / `version_needs_match` | T / 0 / `version_needs_match` | T / 0 / `version_needs_match` |
| Duplicate complete approved SKILL heading/body | F / 1 / `document_mismatch` | **T / 0 / `version_needs_match`** | F / 1 / `document_mismatch` |
| Denial in pinned knowledge document | F / 1 / `document_mismatch` | F / 1 / `document_mismatch` | F / 1 / `document_mismatch` |
| Same approved body words, sorted into a word bag | F / 1 / `document_mismatch` | F / 1 / `document_mismatch` | F / 1 / `document_mismatch` |
| S103 row with wrong source URL | F / 1 / `document_mismatch` | F / 1 / `document_mismatch` | F / 1 / `document_mismatch` |
| Off-topic source capture carrying the identical quote | F / 1 / `document_mismatch` | F / 1 / `document_mismatch` | F / 1 / `document_mismatch` |

Perturbations, each isolated from the canonical fixture:

- **Duplicate heading:** append another exact approved section after a following unrelated section. Under the mutant, extraction accepts the first exact section despite two occurrences. This is the detector's decisive false-accept observation, not an original-counter bypass.
- **Denial:** change `` `vna_other` is the version identifier `` to `` `vna_other` is not the version identifier `` in the pinned knowledge document. Only that document check failed.
- **Word bag:** retain the exact heading and body words, but sort the body tokens instead of retaining the decision table. Only SKILL section equality failed.
- **Wrong source:** replace the LSB URL in the S103 registry row with `https://example.invalid/off-topic-source`, leaving other fields and pinned captures intact. Only the S103 row check failed; no network request was made.
- **Off-topic same quote:** replace the LSB capture with a 427-byte gardening HTML document containing the exact captured `vna_other` paragraph. Only that capture's source digest check failed. Quote preservation is evidenced by `source-quote.txt` and the full candidate HTML. This demonstrates exact source-byte binding, not semantic classification of gardening text.

All check-level arrays and the exact failed paths are retained in `receipts/<phase>/<case>/binding.json`.

## Mutant, expected detector, and restoration

Mutant at private `section()` line 159:

```diff
-    if lines.count(title) != 1:
+    if lines.count(title) < 1:
```

Expected detector: reject duplicate exact approved headings while accepting the canonical fixture; preserve rejection of denial, word-bag, wrong-source and off-topic-same-quote fixtures. The detector assertions and fixture bytes were unchanged across phases.

| Bytes | SHA-256 |
|---|---|
| Pristine private counter | `d7f0a8cf3ca08562437d40711d15e7ad4f6fa44edb4e8934c36f4673e4e7c45e` |
| Mutated private counter | `d742db3996ec518c902153382ad585e7b570f51a0ded8d27fe92004bb7d1d7ba` |
| Restored private counter | `d7f0a8cf3ca08562437d40711d15e7ad4f6fa44edb4e8934c36f4673e4e7c45e` |

Exact restored bytes equal the saved pristine bytes. The sandbox's original counter retained the pristine hash in every phase. The extracted document-binding block retained SHA-256 `57ab67ccf315e86e013b0ec07fb309ba4b395586e614ec0d3bfdafd518f309dc` in every phase; the mutation affected its called `section()` helper only. Detector SHA-256: `5af1be9a3ed67c35ee01d74192676f72924e2495ba9d1e7d6aad571e9d5fc06b`.

Full before/after hashes and sizes for every candidate fixture are in `mutation-summary.json`; full counter bytes for each phase are retained separately. Baseline and restoration succeeded, so this is a killed mutant, not an inconclusive baseline failure.

## Execution and retained evidence

Observed UTC:

- Preparation: `2026-10-23T10:55:38.316151+00:00`–`10:55:38.386775+00:00`, exit 0.
- Pristine: `2026-10-23T10:55:38.387029+00:00`–`10:55:38.965441+00:00`, exit 0.
- Mutated: `2026-10-23T10:56:10.915056+00:00`–`10:56:11.390505+00:00`, exit 1.
- Restored: `2026-10-23T10:56:17.362492+00:00`–`10:56:18.844994+00:00`, exit 0.

Each phase ran the same command shape, differing only in phase/output label:

```text
timeout --signal=TERM --kill-after=3s 180s python3 -I -B /fast/scratch/hyaku/kaidoku-r34/w1/MutDocSection/.ufo/waves/round-34/w1/MutDocSection-files/probe.py <pristine|mutated|restored>
```

Exact argv, cwd, UTC, unmodified stdout/stderr and exit are in `launch-*.json`; all phase stderr was empty. The eighteen outer fixture CLI invocations each have their own exact command/stdout/stderr/exit/UTC receipt at `receipts/<phase>/<case>/command.json`. Those outputs also retain both fake-reader attempt results. Python memory was capped at 512 MiB, CPU at 60 seconds, file output at 8 MiB, open files at 64, and NPROC at 8192. Execution was sequential, one child tree at a time; the fixed call chain permits at most four processes including `timeout`. All launched commands returned; none was backgrounded. Fixture writes were individually capped at 1 MiB and archival payload at 8 MiB.

Archive: **107 files**, including the inventory; payload before inventory was **571725 bytes**. `archive-manifest.json` lists exact retained artifact hashes/sizes; its own SHA-256 is `c34576ca65d6b6fb5a6db10b4b9d3c4041996d029161e25327b32a1f9abb1ff4`.

No tool installation/update, Git write, routing change, additional model invocation, safety refusal or fallback occurred. Visible session model: `openai-codex/gpt-6.1-sol`.

Scope boundary: these five original-counter fixture rejections and this killed uniqueness mutant support only the exercised source/document binding paths. They do not establish or falsify the complete twelve-carrier production predicate. No integration or production repair was performed.

Report: .ufo/waves/round-34/w1/MutDocSection.md
