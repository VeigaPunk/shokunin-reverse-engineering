# R22-C1 counter review

**Axes:** coverage, calibration. **Scope:** the current working-copy `count-c1.py` diff, with dependencies read only where called. The requested baseline `7787fea4d6fd718726de92ed20759d11ce7b8b48` does not contain this tool (`git cat-file -e <baseline>:.ufo/waves/round-22/tools/count-c1.py` exited 128); the present tool is a modified working-copy file. Baseline/HEAD measurements below therefore use the current working-copy counter against those Git trees, not a counter at baseline.

## Findings

### High — measurement executes helper source from the revision being measured

`count-c1.py:38-52` obtains `.ufo/waves/round-20/tools/verb-coverage.py` and `.ufo/waves/round-21/tools/verb-coverage.py` from the selected `rev`; `count-c1.py:31-35` imports the retrieved R21 Python module with `spec.loader.exec_module`. Thus a selected revision is not data-only: its helper module top-level code executes before measurement. The existing `helper_drift` selftest mutates only an uncommitted helper after the fixture commit, so it does not cover a modified helper committed at the selected revision.

**Observed probe:** in a private temporary Git fixture, I appended `Path(<marker-in-fixture-root>).write_text("executed")` to the selected commit's R21 helper, then invoked:

```text
/usr/bin/python -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-22/tools/count-c1.py --root /tmp/c1-rev-helper-final-8095odjw --rev ab874df3d867d91490a9304d77af064d4a2048b3
```

Exit `0`; stderr empty; marker existed with content `executed`; stdout reported `c1_complete`, `t1_exercised_count: 6`, `t1_total: 6` (full exact stdout is below). This proves arbitrary selected-revision Python executes; **[INFERENCE]** a revision can also change the imported measurement/binding functions and thereby falsify its own count. The observed side effect was confined to the temporary fixture.

**Narrow fix:** use helper logic pinned independently of the measured revision (e.g. a reviewed immutable helper revision plus digest, or fixed in-counter code). Add a selftest that commits a helper with a harmless marker side effect and asserts the marker is not created.

### Medium — refusal records inside arrays are not traversed

`count-c1.py:67-79` pushes `raw_result` and `normalized_result` values onto `pending`, but skips every non-dict node (`continue`); it never descends into a list. The inherited `r21.refused` helper also returns false for non-dict values and does not recursively inspect lists (`.ufo/waves/round-21/tools/verb-coverage.py:39-55,77-98`). Consequently, a refusal object inside an array escapes both paths. This contradicts the frozen C1 falsifier that a typed refusal envelope must not count (`claims.json:21`).

**Observed probe:** a valid-looking envelope with matching command, operation and Evidence ID had `data.raw_result = [{"ok": false, "error": {"code": "capability_unavailable"}}]`. The counter nevertheless set `identify-flutter-build` exercised and reported `t1_exercised_count: 1`. Command exited `1` because the other five T1 verbs were absent; stderr was empty. Exact argv and stdout follow.

**Narrow fix:** recursively walk dicts and lists under `raw_result`/`normalized_result`, applying the refusal policy to every object; add the array-nested refusal case to `counter-fixtures.py` and expect zero.

### Medium — lossy UTF-8 replacement lets malformed evidence bind

`count-c1.py:93-96` obtains evidence through `r20.git_show`; `.ufo/waves/round-20/tools/verb-coverage.py:94-96` decodes every blob with `raw.decode("utf-8", "replace")`. The C1 JSON binder then parses this replacement text, so the original bytes are not validated as UTF-8.

**Observed probe:** in a private fixture, the cited evidence envelope contained raw byte `0xff` inside an otherwise ignored JSON string value. `raw_evidence_contains_invalid_utf8` was true, yet the counter set `identify-flutter-build` exercised and reported `t1_exercised_count: 1` (exit `1` for incomplete 6-verb coverage; stderr empty). It bound a repaired replacement-character string rather than a valid JSON byte stream.

**Narrow fix:** read evidence blobs as bytes and strict-decode UTF-8 before JSON parsing; retain lossy decoding only where needed for prose, not Evidence records. Add an invalid-UTF-8 evidence control that does not count.

## Exact positive/adversarial outputs

These controlled runs used private fixture repositories with the retained helper dependencies and synthetic CLI envelopes; they did not invoke REA or execute a target. Full output is included so counts and exit semantics are reproducible.

### Positive exact-file control — exit 0

```text
argv: /usr/bin/python -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-22/tools/count-c1.py --root /tmp/c1-dir-cite-final-mgd35e2d --rev 36bba2239f36a9552e99f74bda4d9edae2189460
exit: 0
stderr: ""
stdout: {"catalog_mentioned_count": 6, "catalog_total": 6, "catalog_zero": [], "catalog_zero_count": 0, "claim": "R22-C1", "finding": "c1_complete", "limit": "CLI envelope/entry/source linkage only; source relevance and scope admission remain manual; no cryptographic authentication", "rev": "36bba2239f36a9552e99f74bda4d9edae2189460", "t1": ["identify-flutter-build", "inspect-dart-aot", "debug-with-gdb", "debug-with-rizin", "inspect-signal-decoders", "decode-signal-recording"], "t1_exercised": ["identify-flutter-build", "inspect-dart-aot", "debug-with-gdb", "debug-with-rizin", "inspect-signal-decoders", "decode-signal-recording"], "t1_exercised_count": 6, "t1_total": 6, "targets": {"debug-with-gdb": {"bound_evidence": [["ev_0000000000000000000000000000000000000000000000000000000000000003", ".ufo/waves/round-22/evidence/c1/debug-with-gdb.json"]], "entries": 1, "exercised": true, "unsupported_candidates": []}, "debug-with-rizin": {"bound_evidence": [["ev_0000000000000000000000000000000000000000000000000000000000000004", ".ufo/waves/round-22/evidence/c1/debug-with-rizin.json"]], "entries": 1, "exercised": true, "unsupported_candidates": []}, "decode-signal-recording": {"bound_evidence": [["ev_0000000000000000000000000000000000000000000000000000000000000006", ".ufo/waves/round-22/evidence/c1/decode-signal-recording.json"]], "entries": 1, "exercised": true, "unsupported_candidates": []}, "identify-flutter-build": {"bound_evidence": [["ev_0000000000000000000000000000000000000000000000000000000000000001", ".ufo/waves/round-22/evidence/c1/identify-flutter-build.json"]], "entries": 1, "exercised": true, "unsupported_candidates": []}, "inspect-dart-aot": {"bound_evidence": [["ev_0000000000000000000000000000000000000000000000000000000000000002", ".ufo/waves/round-22/evidence/c1/inspect-dart-aot.json"]], "entries": 1, "exercised": true, "unsupported_candidates": []}, "inspect-signal-decoders": {"bound_evidence": [["ev_0000000000000000000000000000000000000000000000000000000000000005", ".ufo/waves/round-22/evidence/c1/inspect-signal-decoders.json"]], "entries": 1, "exercised": true, "unsupported_candidates": []}}}
```

### Adversarial array-nested refusal — incorrectly counts 1; exit 1

```text
argv: /usr/bin/python -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-22/tools/count-c1.py --root /tmp/c1-array-refusal-review-owxep7p4 --rev 9088684e395b2fd8982fb0cd7db9d9731fd96ef5
exit: 1
stderr: ""
stdout: {"catalog_mentioned_count": 1, "catalog_total": 1, "catalog_zero": [], "catalog_zero_count": 0, "claim": "R22-C1", "finding": "c1_incomplete", "limit": "CLI envelope/entry/source linkage only; source relevance and scope admission remain manual; no cryptographic authentication", "rev": "9088684e395b2fd8982fb0cd7db9d9731fd96ef5", "t1": ["identify-flutter-build", "inspect-dart-aot", "debug-with-gdb", "debug-with-rizin", "inspect-signal-decoders", "decode-signal-recording"], "t1_exercised": ["identify-flutter-build"], "t1_exercised_count": 1, "t1_total": 6, "targets": {"debug-with-gdb": {"bound_evidence": [], "entries": 0, "exercised": false, "unsupported_candidates": []}, "debug-with-rizin": {"bound_evidence": [], "entries": 0, "exercised": false, "unsupported_candidates": []}, "decode-signal-recording": {"bound_evidence": [], "entries": 0, "exercised": false, "unsupported_candidates": []}, "identify-flutter-build": {"bound_evidence": [["ev_0000000000000000000000000000000000000000000000000000000000000001", ".ufo/waves/round-22/evidence/c1/identify-flutter-build.json"]], "entries": 1, "exercised": true, "unsupported_candidates": []}, "inspect-dart-aot": {"bound_evidence": [], "entries": 0, "exercised": false, "unsupported_candidates": []}, "inspect-signal-decoders": {"bound_evidence": [], "entries": 0, "exercised": false, "unsupported_candidates": []}}}
```


### Adversarial committed-helper side effect — executes selected revision code; exit 0

```text
argv: /usr/bin/python -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-22/tools/count-c1.py --root /tmp/c1-rev-helper-final-8095odjw --rev ab874df3d867d91490a9304d77af064d4a2048b3
exit: 0
stderr: ""
stdout: {"catalog_mentioned_count": 6, "catalog_total": 6, "catalog_zero": [], "catalog_zero_count": 0, "claim": "R22-C1", "finding": "c1_complete", "limit": "CLI envelope/entry/source linkage only; source relevance and scope admission remain manual; no cryptographic authentication", "rev": "ab874df3d867d91490a9304d77af064d4a2048b3", "t1": ["identify-flutter-build", "inspect-dart-aot", "debug-with-gdb", "debug-with-rizin", "inspect-signal-decoders", "decode-signal-recording"], "t1_exercised": ["identify-flutter-build", "inspect-dart-aot", "debug-with-gdb", "debug-with-rizin", "inspect-signal-decoders", "decode-signal-recording"], "t1_exercised_count": 6, "t1_total": 6, "targets": {"debug-with-gdb": {"bound_evidence": [["ev_0000000000000000000000000000000000000000000000000000000000000003", ".ufo/waves/round-22/evidence/c1/debug-with-gdb.json"]], "entries": 1, "exercised": true, "unsupported_candidates": []}, "debug-with-rizin": {"bound_evidence": [["ev_0000000000000000000000000000000000000000000000000000000000000004", ".ufo/waves/round-22/evidence/c1/debug-with-rizin.json"]], "entries": 1, "exercised": true, "unsupported_candidates": []}, "decode-signal-recording": {"bound_evidence": [["ev_0000000000000000000000000000000000000000000000000000000000000006", ".ufo/waves/round-22/evidence/c1/decode-signal-recording.json"]], "entries": 1, "exercised": true, "unsupported_candidates": []}, "identify-flutter-build": {"bound_evidence": [["ev_0000000000000000000000000000000000000000000000000000000000000001", ".ufo/waves/round-22/evidence/c1/identify-flutter-build.json"]], "entries": 1, "exercised": true, "unsupported_candidates": []}, "inspect-dart-aot": {"bound_evidence": [["ev_0000000000000000000000000000000000000000000000000000000000000002", ".ufo/waves/round-22/evidence/c1/inspect-dart-aot.json"]], "entries": 1, "exercised": true, "unsupported_candidates": []}, "inspect-signal-decoders": {"bound_evidence": [["ev_0000000000000000000000000000000000000000000000000000000000000005", ".ufo/waves/round-22/evidence/c1/inspect-signal-decoders.json"]], "entries": 1, "exercised": true, "unsupported_candidates": []}}}
```

### Adversarial invalid-UTF-8 evidence — counts one target; exit 1

```text
argv: /usr/bin/python -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-22/tools/count-c1.py --root /tmp/c1-invalid-utf8-final-96a18xcc --rev 2e949793b8e3df450e6a78395639901aa737cc7c
exit: 1
stderr: ""
stdout: {"catalog_mentioned_count": 1, "catalog_total": 1, "catalog_zero": [], "catalog_zero_count": 0, "claim": "R22-C1", "finding": "c1_incomplete", "limit": "CLI envelope/entry/source linkage only; source relevance and scope admission remain manual; no cryptographic authentication", "rev": "2e949793b8e3df450e6a78395639901aa737cc7c", "t1": ["identify-flutter-build", "inspect-dart-aot", "debug-with-gdb", "debug-with-rizin", "inspect-signal-decoders", "decode-signal-recording"], "t1_exercised": ["identify-flutter-build"], "t1_exercised_count": 1, "t1_total": 6, "targets": {"debug-with-gdb": {"bound_evidence": [], "entries": 0, "exercised": false, "unsupported_candidates": []}, "debug-with-rizin": {"bound_evidence": [], "entries": 0, "exercised": false, "unsupported_candidates": []}, "decode-signal-recording": {"bound_evidence": [], "entries": 0, "exercised": false, "unsupported_candidates": []}, "identify-flutter-build": {"bound_evidence": [["ev_0000000000000000000000000000000000000000000000000000000000000001", ".ufo/waves/round-22/evidence/c1/identify-flutter-build.json"]], "entries": 1, "exercised": true, "unsupported_candidates": []}, "inspect-dart-aot": {"bound_evidence": [], "entries": 0, "exercised": false, "unsupported_candidates": []}, "inspect-signal-decoders": {"bound_evidence": [], "entries": 0, "exercised": false, "unsupported_candidates": []}}}
```

## Current directory-citation control — prior defect now closed

During this review an earlier working-copy snapshot accepted a directory citation. The current snapshot now requires `path in cited` (`count-c1.py:126-128`); rerunning the same synthetic controls gives exact file paths `6/6`, exit `0`, but directory-only citation `0/6`, exit `1`. The current 23-case selftest also includes `directory_citation` and passes. I do not report this as an open finding.

## Baseline, HEAD, and verification

- `python3 -I -B .ufo/waves/round-22/tools/count-c1.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev 7787fea4d6fd718726de92ed20759d11ce7b8b48`: exit `1`, `t1_exercised_count=0/6`, `catalog_zero_count=20`.
- `python3 -I -B .ufo/waves/round-22/tools/count-c1.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev HEAD`: exit `1`, `t1_exercised_count=1/6`, `catalog_zero_count=19`; bound ID `ev_3458b996b71e3dccde0177728ba60ef94800dd373db5a704048e18526d9d866b` resolves to the cited `.ufo/waves/round-22/evidence/c1/identify-godot.envelope.json` with matching `identify-flutter-build` command/operation. This is local record binding only, as the output limit says.
- Current `python3 -I -B .ufo/waves/round-22/tools/count-c1.py --selftest`: exit `0`, `counter_controls_clean`, 23 cases, no failed cases. It covers source eligibility, direct refusals, helper worktree drift, and exact-directory citation, but not the committed helper execution, array-nested refusal, or invalid UTF-8 cases above.
- The counter exit/`finding` means all-six T1 saturation; the frozen claim's `k>=1` criterion is separate. Do not treat exit `1` at `k=1` as proof that the claim acceptance predicate failed.

## Residual risk and verification gaps

No REA runtime, target execution, debugger, device, remote connection, or dynamic observation was invoked. This review therefore makes no runtime canonicalization or same-identity runtime-rerouting claim. The only measured identity relation was the synthetic/retained record ID plus command and operation; cryptographic authenticity remains explicitly unclaimed.

The LSP device is not mounted: `read xd://lsp` returned “No such tool”. No LSP status, references, definition, or diagnostics could be requested; source evidence came from direct file reads and bounded fixture executions, not grep presented as semantic proof. No packages or tools were installed. No production files were edited; only this report and its `.json` attachment were written.

Structured evidence and exact probe argv/exits are also summarized in `C1Revision.json`.