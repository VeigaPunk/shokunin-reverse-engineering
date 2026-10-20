# ReplicateAetherId — aether r18 Evidence ID vs r17 first/second pass

HOLDS

REV = `b2aad08ceeee8dd125ce0d316056d8bd766c7f94` (lane HEAD == REV verified: `git rev-parse HEAD` → `b2aad08…`, exit 0). All `path:line` anchors below are at REV unless the revision is named inline. No tool installs were needed.

## Claim (the "entry")

`corpus/knowledge/2026-10-20-r18-swiss-map-replay.md:87-88`: "The aether Evidence ID equals the round-17 second-pass ID (same carrier bytes and params)." The same entry's observations table lists `ev_247261e857d89e710977e8a40f118e797c6f4b70eed5ea4d617822910b5a4af4` for calib-aether (`:74`). [observation]

## 1. The two receipt IDs are equal

```
$ cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && python3 -I -B -c '<extract steps.analyze.evidence_id from both receipts via git show at REV>'
r18  calib-aether : ev_247261e857d89e710977e8a40f118e797c6f4b70eed5ea4d617822910b5a4af4
r17 pro-aether    : ev_247261e857d89e710977e8a40f118e797c6f4b70eed5ea4d617822910b5a4af4
equal: True
exit=0
```

[observation]

- REV:`.ufo/waves/round-18/runs/calib-aether/receipt.json:1930` — `"evidence_id": "ev_247261e857d89e710977e8a40f118e797c6f4b70eed5ea4d617822910b5a4af4"` (also in REA stdout, `analyze.json:1`).
- REV:`.ufo/waves/round-17/runs/pro-aether/receipt.json:1849` — same ID (also `analyze.json:1`).

## 2. The retained r17 receipt is the second-pass receipt

```
$ for r in b2aad08… d0ab2992149a38794e5ef2474ba5d4ef5ee1e905 da64646adcb19c1ede7537b799b8c7d283fe43da; do git rev-parse $r:.ufo/waves/round-17/runs/pro-aether/receipt.json; done
b2aad08… receipt.json blob: d552512e41492cff0f99bfbd85816d1b922fb9ad
d0ab299… receipt.json blob: d552512e41492cff0f99bfbd85816d1b922fb9ad
da64646… receipt.json blob: 413d2b975b44e42747ea8215daf7e77ed6aa0fef
exit=0
```

[observation] The receipt retained at REV is byte-identical to the one committed at `d0ab299` (the r17 verification revision that committed the second-pass receipts); the first-pass receipt at `da64646` is a different blob. So "r17 receipt ID" here is the **second-pass** ID, exactly what the entry claims. Attribution of passes (first pass produced by pre-hardening tooling at `da64646`, second pass produced by `95e34db` tooling and committed at `d0ab299`) is corroborated by the frozen manifest itself (`.ufo/waves/round-17/predictions/replicate-expectations.json:83-84`) [observation].

## 3. The r17 first/second-pass difference, per the replicate expectation file

`.ufo/waves/round-17/predictions/replicate-expectations.json`:

- `:4` (basis): "REA analyze evidence_id is a digest of the semantic Evidence record, not argv/time/session (w2 RevEvidenceIdRepeat; pilot and first pass already matched for calib-shfmt/calib-esbuild-0.25.12)". [observation of the frozen text; the content-keying mechanism itself is INFERENCE from REA, consistent with all replications below]
- `:27-28`: frozen pro-aether expectation `"analyze_evidence_id_equals_first_pass": "ev_ae9f7086540f70282970fd27d2ace6a20d50a080eaff143b256994e2f0909855"` — i.e. the **first-pass** ID.
- `:83-84`: `"first_pass_revision": "da64646adcb19c1ede7537b799b8c7d283fe43da"`; `"frozen_before": "second (replicate) measured pass with the w2-hardened carrier-run.py"`.

```
$ git show da64646adcb19c1ede7537b799b8c7d283fe43da:.ufo/waves/round-17/runs/pro-aether/receipt.json | grep -n '"evidence_id"'
1839:      "evidence_id": "ev_ae9f7086540f70282970fd27d2ace6a20d50a080eaff143b256994e2f0909855",
exit=0
```

[observation] The first pass produced `ev_ae9f7086…`; the second pass produced `ev_247261e8…`. The frozen expectation (second pass == first pass) was therefore falsified for aether, as the lane itself recorded: `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:116-122` ("aether id differed … because `string_count` went 29118 → 29117"), `corpus/lessons/round-17.md:42`, `corpus/lessons/round-17-verifier-spotcheck.md:67`. [observation of lane records]

Verified mechanism — the three runs' string counts:

```
$ python3 -I -B -c '<extract string_count from analyze.json at da64646 / REV r17 / REV r18>'
r17 first  da64646: [('string_count', 29118)]
r17 second REV    : [('string_count', 29117)]
r18        REV    : [('string_count', 29117)]
exit=0
```

[observation] The first/second-pass difference is exactly the one Ghidra string-count difference the lane recorded; the r18 run reproduces the second-pass state (29117), so its content-keyed ID equals the second-pass ID and cannot equal the first-pass ID.

## 4. Equality is content-forced, not coincidental

```
$ git rev-parse REV:.ufo/waves/round-17/runs/pro-aether/analyze.json REV:.ufo/waves/round-18/runs/calib-aether/analyze.json
REV r17 analyze.json blob: 9592bdddbd611b7f820fba220b9cfdb639f4a37c
REV r18 analyze.json blob: 9592bdddbd611b7f820fba220b9cfdb639f4a37c
exit=0
```

[observation] The REA `analyze` outputs of the r17 second pass and the r18 run are byte-identical, so identical Evidence IDs are the forced outcome of the content-keyed digest. Supporting sameness ("same carrier bytes and params", entry `:88`): identical carrier sha256 pre/post `06c91f55df4117e58b478242df366145148b956c41c11a46cd1800f76178006e` (REV:`.ufo/waves/round-18/runs/calib-aether/receipt.json:8-9`, REV:`.ufo/waves/round-17/runs/pro-aether/receipt.json:7-8`); identical REA argv `npx -y rea-agents@6.5.0 analyze /usr/bin/aether --format json` (r18 receipt `:1919-1926`, r17 receipt `:1838-1845`); identical recorded `stdout_sha256` `a3db9af2…` for analyze.json (r18 `:1985`, r17 `:1898`) and `12098863…` for inspect-go.json (r18 `:2004`, r17 `:1917`). [observation]

## 5. The r18 run also reproduced the deterministic failure the ID is keyed on

`.ufo/waves/round-18/runs/calib-aether/logs/rea-ghidra-HtDopV/ghidra.log:92` `WARN (GoApiSnapshot) Falling back from 1.25.14 to 1.25.0`; `:97` `ERROR … Go analysis failure`; `:177` `Caused by: java.io.EOFException: Unable to read past EOF: 17645861, 111938854`. This matches the frozen r17 expectation field `log_contains` (`replicate-expectations.json:32`) and the r18 entry's table row (`:74`). [observation]

## Residual risk / verification gaps

- The ID equality is established at recorded-value and byte-identity level (receipts + full REA stdout blobs). I did not recompute REA's internal digest over the Evidence record; that algorithm is upstream and outside this check's scope. Nothing observed contradicts it.
- The `string_count` drift between two identical-byte r17 passes (29118 → 29117) is lane-recorded and re-measured here, but its root cause (nondeterministic Ghidra string recovery) remains an upstream INFERENCE, correctly labelled INFERENCE by the r17 knowledge entry.
- First-pass anchors (`da64646` receipt `:1839`, first-pass `analyze.json`) live in r17 history, not in REV's tree; they are required by the ticket's explanation clause and cited at their own revision.
