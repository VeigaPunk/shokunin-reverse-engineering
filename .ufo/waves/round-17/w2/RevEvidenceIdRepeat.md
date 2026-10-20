# RevEvidenceIdRepeat — W2 falsification: what `analyze`'s `evidence_id` hashes, and whether pilot≡final ids are expected

- Seat: `KaidokuR17.RevEvidenceIdRepeat` (author-side advisory, leaf). Read-only attack.
- Lane revision `da64646adcb19c1ede7537b799b8c7d283fe43da`; predictions frozen at `271167473d87ef710f07ecdd98caf0ce12091686`.
- No REA `analyze`/`search`/`decompile`, no Ghidra, no carrier execution, no installs. Repro used only retained files.
- Axes: **calibration** (can this round distinguish a repeat from an independent run?) and **depth** (hash-input reconstruction + recomputation).

`DIST` below = `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist` (rea-agents 6.5.0).

## Verdict (both target questions answered)

1. **Inputs.** `evidence_id` is `ev_` + SHA-256 of the RFC-8785-canonical **semantic projection** of the whole Evidence record (`DIST/domain/evidence.js:156-182`, `DIST/domain/canonicalDigest.js:3-12,63`). For `analyze` (`operation: binary_overview`) it hashes: subject `{digest.sha256, format, architecture}`; provider; full `analysis_profile` (Ghidra 12.1.4, workflow_revision 3, both profile digests); `predicate_type`; `operation`; `parameters` (`{}`); `raw_result` (`null`); `normalized_result` (`document`, `image_base`, every segment, counts); `confidence`; `authority`; `environment`; `limitations`; `relationship_coverage` when non-null; `locations`; `evidence_links`. It **excludes** `subject.name`, `subject.local_path`, argv, cwd, timestamps, session dirs, retained-log bytes, and the rea-agents package version (`provider.version` is `"1"`, not `6.5.0`).
2. **Pilot vs final ids.** The identical `calib-shfmt` / `calib-esbuild` ids are **expected**, not a defect: the final `analyze.json` is **byte-identical** to the pilot's (equal sha256), the receipt records that stdout sha with fresh start/end times and exit 0, and the Ghidra sessions are distinct (different session roots and logs; normalized logs differ only in timings/one completion line). Equality is forced by identical semantic content. It is **not** evidence of an independent run; the freshness evidence is the receipt, and the id cannot supply it.

## R1 (depth, no-finding) — hash inputs, re-derived and recomputed

Sources, 6.5.0 dist:

- `DIST/domain/evidence.js:156-180` — `semanticProjection` (the complete hashed field set above).
- `DIST/domain/evidence.js:181-182` — `computeEvidenceId = ev_ + digestCanonicalValue(semanticProjection(evidence), "Evidence")`.
- `DIST/domain/evidence.js:133-140,184-190` — `parseEvidence` recomputes the id and rejects a mismatch (checksum, not a signature).
- `DIST/domain/canonicalDigest.js:8-14,63` — SHA-256 over compact JSON with keys sorted in RFC-8785 UTF-16 order.
- `DIST/domain/analysisProfile.js:29-48` — the nested profile digest is computed the same way over `{provider, parameters}`; it is itself hashed.
- `DIST/cli-runtime/DirectAnalysis-BgvAtpN3.js:39-47,419-430` — `analyze`'s record is built by `createWorkflowEvidence`; `:501` wraps the upstream profile via `workflowAnalysisProfile`.
- `DIST/cli-runtime/InvestigationProviders-DoQRIHii.js:14-17` — `workflow_revision: 3` for `binary_overview`.
- `DIST/cli-runtime/cli.js:10323-10347` — the `analyze` command calls `runDirectAnalysis(path, "binary_overview", {})`, so `parameters` is the empty object (the path is not in it).

Recomputation (Python mirror of the projection + canonical digest, `/tmp/evid_recompute.py`; cross-checked against the dist's own `digestCanonicalValue`):

```
$ python3 -B -c "…evid(e) vs e['evidence_id'] for all retained records…"
OK runs/calib-esbuild-0.25.12/analyze.json ev_391dbfe69769673c3af0bb7575e730e311f6f8bd273d848126d8f5addc22b03f
OK runs/calib-shfmt/analyze.json          ev_2b29a1ddfaead9d13a3d8923a2edc176dbe8ebda0ac776707625c6c1de3c5be3
OK runs/pro-aether/analyze.json           ev_ae9f7086540f70282970fd27d2ace6a20d50a080eaff143b256994e2f0909855
OK runs/pro-containerd-shim/analyze.json  ev_8a6f88c9927db2ec1b87526cdaf3baf2dd59b3cf574ab84026a7774e731dfe54
OK runs/pro-esbuild-0.21.5/analyze.json   ev_4ea99771648bcabf5645146cdb96d8c023967c9fbc8e9b21fd90975681d3b6be
OK runs/pro-esbuild-0.27.7/analyze.json   ev_987ae88921b7f72601c108d820028c0e8d8b8a8f1f76ba82657b9ebcd961e485
OK runs/pro-notesmd-cli/analyze.json      ev_4fd342dd05bcf5a5da4d3574c09501bff856245ccd336f1c6a337459c0b350d7
OK runs/pro-op/analyze.json               ev_3d7ba7eca7ad3fbc187431def31c5e32079f1689d1441752511afef8a3743f41
OK runs/calib-esbuild-0.25.12/inspect-go.json ev_0cabcc66620bf9f201e2b0aaba63d9bd1998b4e498ec823c01dc186a73041626
OK runs/calib-shfmt/inspect-go.json           ev_f8ef12a805b6b28bee4beed4cde7440efe567e22133db2a1fb1776d867f4a42a
OK runs/pro-aether/inspect-go.json            ev_01b04ce90eb6ea7e14da66e0c77458744f6c32912321ede98bed02ee65d56f22
OK runs/pro-containerd-shim/inspect-go.json   ev_a1b3433cd1ec10e34ecbf3a7e5e6fee7edc69efc3c20f697af87aac25b6d54ed
OK runs/pro-esbuild-0.21.5/inspect-go.json    ev_5c06eceff96ee9f44596daacb182839e8ab629d1b1b8926f187cfafaddae43f7
OK runs/pro-esbuild-0.27.7/inspect-go.json    ev_a1e7ac95032d7b36ea1c7c1429d7c6f8a8e252c153267bfa9f5e5228fe302ea1
OK runs/pro-notesmd-cli/inspect-go.json       ev_d5f4c18b84eb0bf09a5c8adbfc27d46bcbeb806ad98f0a69e676fd83363bbf6a
OK runs/pro-op/inspect-go.json                ev_4279a4264ab81b1511b5ce263eeed288474fddf180f019008ca1ece2a23f69f4
OK pilot/shfmt.json                            ev_2b29a1ddfaead9d13a3d8923a2edc176dbe8ebda0ac776707625c6c1de3c5be3
OK pilot/esb.json                              ev_391dbfe69769673c3af0bb7575e730e311f6f8bd273d848126d8f5addc22b03f
```

18/18 recompute exactly (16 run records + 2 pilot). Independent check with the dist's own digest function on `pilot/shfmt.json`:

```
$ node --input-type=module -e 'import {digestCanonicalValue} from "file:///…/dist/domain/canonicalDigest.js"; …'
node-digest ev_2b29a1ddfaead9d13a3d8923a2edc176dbe8ebda0ac776707625c6c1de3c5be3
recorded    ev_2b29a1ddfaead9d13a3d8923a2edc176dbe8ebda0ac776707625c6c1de3c5be3
```

Mutation matrix on `pilot/shfmt.json` (each mutation recomputed with the same script):

| mutation | id changes |
|---|---|
| `subject.name` + `subject.local_path` → `/MUTATED/PATH` | **no** |
| `subject.digest.sha256` → 64 zeros | yes |
| `subject.format` elf→pe; `subject.architecture` x86_64→aarch64 | yes |
| `parameters {}` → `{"x":1}` | yes |
| `normalized_result.procedure_count + 1`; `document` rename | yes |
| `confidence`; last `limitations` entry + `"."` | yes |
| Ghidra version 12.1.4→9.9.9; `workflow_revision` 3→2 | yes |
| `operation`; `environment` null→object; `locations []`→address | yes |

Value types in all four analyze JSONs are `null/bool/int/str/list/dict` only (no floats; no `undefined`), so the Python canonicalizer is not hiding a JS number-format divergence. The hashed analyze projection contains no `/usr/bin`, `/tmp`, `/home`, `rea-ghidra` or `2026-` string (grep of the dumped projection: no matches) — `normalized_result.document` is `target-<sha12>.bin`, derived from the carrier digest, not the path.

**Important boundary:** this path-independence is specific to `binary_overview`. `inspect_go_binary` in the same 6.5.0 dist hashes three path fields — `parameters.path`, `normalized_result.artifact.path`, `locations[0].path` (`DIST/application/go/GoBinaryService.js:55-71`). Walk of `runs/calib-shfmt/inspect-go.json` finds exactly those three carrying `/usr/bin/shfmt`; mutating `normalized_result.artifact.path` changes the id, mutating `subject.local_path` does not. This is already lane knowledge: `LOG.md:1697` and `corpus/knowledge/2026-10-19-arc3-r12-go-evidence-id-domain.md` (REA 6.7.0, same three fields, same-path repeat stable).

## R2 (calibration, no-finding) — why the equality is expected, and what it does not prove

```
$ sha256sum pilot/shfmt.json runs/calib-shfmt/analyze.json pilot/esb.json runs/calib-esbuild-0.25.12/analyze.json
271ced9024099abb010bba3b2128c74c7c7209107611e2b5cb43c46e65de62c1  pilot/shfmt.json
271ced9024099abb010bba3b2128c74c7c7209107611e2b5cb43c46e65de62c1  runs/calib-shfmt/analyze.json
1904619c2ee0d6c3d620eb9429ace8dc23f39fa1dd11740dbebc78fa3190f2c6  pilot/esb.json
1904619c2ee0d6c3d620eb9429ace8dc23f39fa1dd11740dbebc78fa3190f2c6  runs/calib-esbuild-0.25.12/analyze.json
$ cmp pilot/shfmt.json runs/calib-shfmt/analyze.json && echo shfmt-identical
shfmt-identical          # esbuild pair: cmp also identical
```

Every top-level field of pilot and final is equal (same dict comparison), so `semanticProjection` is identical and the digest *must* be identical.

The final receipt records that invocation producing those bytes:

- `runs/calib-shfmt/receipt.json:1839` `evidence_id ev_2b29…`; `:1861` `started_at_utc 2026-10-20T13:47:06.688621+00:00`; `:1865` `stdout_sha256 271ced90…` — equals the retained file's sha.
- `runs/calib-esbuild-0.25.12/receipt.json:1839` `ev_391d…`; `:1861` `started_at_utc 13:47:43.330377+00:00`; `:1865` `stdout_sha256 1904619c…`.
- Separate Ghidra sessions: pilot `/tmp/rea-ghidra-LuPZRm` (10:17:28) / `r9xmGu` (10:18:19) vs final `/tmp/kr17-rea-y138m4zi/rea-ghidra-j5AXOZ` (10:47:07) / `rea-ghidra-B5tAvn`. Log sha256 differ (`aaf677ed…`/`f6b61152…` pilot vs `13b8fbbe…`/`e2b678fe…` final).
- After normalizing timestamps and session roots, `diff` of pilot vs final logs shows only analyzer timing values, plus one trailing `ANALYZING changes made by post scripts` line present only in the final esbuild log (consistent with the documented polling gap, `contract.md:46`).
- The pilot ran with `cwd /tmp/kr17-pilot` (`pilot/README.txt:2`) while the final receipt records `cwd …/.ufo/waves/round-17` (`receipt.json:1837`); the ids are still equal because cwd/argv are not hashed.

So: equality is the *desired* outcome of a deterministic `binary_overview` rerun, not an anomaly. Conversely, a **different** id would have meant some semantic field changed (a finding). What equality cannot do is authenticate that a rerun happened — that claim rests on receipt timestamps/exit and the fresh session logs, not on the id. A reader who counts two "REA evidence ids" here is counting one distinct semantic record twice.

**Advisory for integration:** where the final knowledge/capability text cites the analyze id (slot at `w1/draft-knowledge-r17.md:105-111`), say it equals the pilot's (`ev_2b29…`/`ev_391d…`) because the semantic record is byte-identical; do not present it as a fresh distinct identity.

## F1 (medium, calibration) — `w1/CarrierCensusTool.md:66,72` misstates the id as per-call/per-invocation

Quotes:

- `w1/CarrierCensusTool.md:66`: "`evidence_id` is REA's per-call envelope id, not a digest of the binary — use `sha256` for pinning."
- `w1/CarrierCensusTool.md:71-72`: "Only the shfmt row's inspect call was duplicated (one pre-implementation shape probe) — both returned identical fields except evidence_id, confirming evidence ids are per-invocation."

Both clauses are wrong about the mechanism. The id is never assigned per call; it is the canonical SHA-256 of the semantic record (R1). That record includes the subject sha256 (so "not a digest of the binary" is only true in the narrow sense that it digests more than the binary). For `inspect_go_binary`, two calls **at different paths** with identical Go fields necessarily differ exactly at `parameters.path`, `normalized_result.artifact.path`, `locations[0].path` — which fully explains the census observation without any per-invocation randomness. The lane already recorded this: `LOG.md:131` ("content-deterministic evidence ids"), `LOG.md:227-229` ("content-addressed across lanes and rounds"), `LOG.md:1697`, and `corpus/knowledge/2026-10-19-arc3-r12-go-evidence-id-domain.md` (same-path repeat stable; path-sensitive via the three fields). Empirically, independent same-path runs reproduce exactly: final `inspect-go.json` ids `ev_f8ef…`/`ev_0cab…` equal the w1 census/scout ids, and the final inspect stdout sha `a5ddc648…`/`a20a65de…` (`receipt.json:1884`) equals the scout's recorded stdout sha (`w1/ScoutGoDataInventory.md:185-186`).

Smallest fix: rewrite `:66` as "`evidence_id` is the SHA-256 of the semantic Evidence record (it includes `subject.digest.sha256`, and excludes `subject.name`/`local_path`); use `sha256` for pinning" and `:71-72` as "the duplicate call differed at the three semantic path fields (`parameters.path`, `artifact.path`, `locations[0].path`), so the id differed while the Go fields matched — this verb is path-sensitive, not per-invocation."

## F2 (high, calibration) — `receipt-validate.py` rejects every carrier receipt and never checks `evidence_id`

`w1/ConnSiblingOverlap.md:130` flagged the risk that the validator's required-field logic might reject the new keys; the committed tool rejects the whole receipt, before any key check:

```
$ python3 -I .ufo/waves/round-17/tools/receipt-validate.py \
    .ufo/waves/round-17/runs/calib-shfmt/receipt.json \
    .ufo/waves/round-17/runs/calib-esbuild-0.25.12/receipt.json
{"counts":{"invalid":2,"receipts":2,"unreadable":0,"valid":0},"exit":1, …,   # abridged
 "findings":[{"code":"unrecognized_shape","detail":"receipt matches neither retain nor carrier shape","where":"$"}], …}
exit=1
```

Cause: `tools/receipt-validate.py:98` classifies a carrier receipt only when `steps` is a **list**; `tools/carrier-run.py:309` writes `steps` as a **dict**. Both tools' selftests pass because each tests its own shape: `carrier-run.py:555` asserts `receipt["steps"]["analyze"]["evidence_id"]`, while the validator fixture at `receipt-validate.py:470` builds `"steps": [{…}]` (list). `carrier-run.py --selftest` → `SELFTEST: CLEAN cases=2`; `receipt-validate.py --selftest` → `SELFTEST: CLEAN cases=5`. Even if classified, `CARRIER_STEP_REQUIRED` (`receipt-validate.py:62-65`) has no `evidence_id` key, so the id would never be checked.

This is not a final-run regression: both files are unchanged across `2711674..da64646` (`git diff` empty), and the frozen-rev copies have the same mismatch. But it invalidates the gates that were drafted on it: `w1/ConnCapabilityHistory.md:70,91` (capability row only if `receipt-validate.py` exit 0), `w1/draft-scorecard.md:46`, `w1/draft-log-entry.md:45`, `w1/ReviewCapabilityTable.md:37`. `run-carriers.sh` never invokes the validator, and `verify.py` contains no evidence/receipt check, so no second gate compensates.

Smallest fix: accept a mapping in `classify` and iterate `steps.values()` in the carrier step checks (keep the list path for compatibility), and add a dedicated check: for the `analyze` step, require a non-null `evidence_id`. Note the tool is also exercised by the run-calibration seats; this report is the evidence-id side of the same defect.

## F3 (low, calibration) — a missing analyze id is silently accepted

`tools/carrier-run.py:246-252` returns `None` on any parse failure; `:333-334` stores it; the exit logic (`:376-383`) checks only `pins_compare` and `analyze.exit`, never the id. `contract.md:45` says the id is recorded "if present", and `w1/ReviewContract.md:286-288` recommended making it required with exit 2, but neither the contract nor the tool adopted that. All 8 final receipts carry a non-null id (scan above), so there is no live failure — only a silent-failure path. Smallest fix: after `:333`, `if steps["analyze"]["evidence_id"] is None: receipt["error"]=…; return receipt, 2`, and add the same requirement to the validator.

## Bounded checks (no finding)

- All 8 run receipts: `steps.analyze.evidence_id` equals the recomputed id of its retained `analyze.json`, and `stdout_sha256` equals that file's sha256; `exit 0` for all; `pins_compare` not re-checked here (pins module out of this seat's scope).
- No id collision across the 18 recomputed records; each carrier/operation has a distinct digest.
- `analyze`'s hashed projection carries no absolute path, timestamp, session id or log bytes; `subject.name`/`local_path` are display-only.
- The id is a checksum, not a signature: `parseEvidence` (`DIST/domain/evidence.js:133-140`) rejects a stale id, but anyone can recompute it after mutating a record. Do not cite it as tamper-proof.
- `provider.version` is `"1"`, and the rea-agents package version is outside the projection, so the id is not a tool-build identity; the receipt argv/pins carry that.

Tool installs/updates: none.
