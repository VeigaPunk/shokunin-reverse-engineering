# ReviewerGates — round 74 freeze and wave evidence

Axes: freeze integrity; pin completeness; wave-contract consistency; honest observability.

## Findings (severity order)

- **Low — conflicting evidence-directory target.** `.ufo/waves/round-74/r74-w1-spec.json:10` and the corresponding ExecProbeCases dispatched task name `.the/ufo/waves/round-74/w1/ExecProbeCases/` as the target evidence directory; the actual required directory is `.ufo/waves/round-74/w1/ExecProbeCases/`. The receipt acceptance and final report trailer use the latter. Correct the target typo; the validated report trailer itself is correct.
- No freeze verdict or SHA-256 mismatch found. The gate checks only the two claim-named instruments, not all nine pinned files; the independent reader closes that coverage gap.

## Checks — commands and exact outputs

All subprocess commands ran with cwd `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, TMPDIR `/fast/scratch/hyaku/kaidoku-r74/ReviewerGates`; the sole scratch directory was removed in a finally block before this report. No installs, runtime invocation, git mutation, or production edits.

Executed wrapper: `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-74/w1/ReviewerGates/independent-reader.py all` (rc 0); its four independent checks ran concurrently. Full exact outputs, including the complete historical gate stdout, are preserved in `ReviewerGates/checks.json`. The retained reader imports no lane counter or freeze-pins implementation.

| Check | Exact command | Output |
|---|---|---|
| Freeze gate | `python3 -I -B tools/round-29/freeze-gate.py --root . --rev 021914c0e638454e507087accfe41af1ab69f185 --require-clean round-74` | rc 0; stderr empty; round-74 object below; full stdout: `checks.json#/gate/stdout` |
| Independent pins | `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-74/w1/ReviewerGates/independent-reader.py pins` (executed by `all`) | `pin_count: 9`, `mismatches: []`, `declaration_mismatches: []`; exact nine expected/actual pairs below |
| Wave evidence | `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-74/w1/ReviewerGates/independent-reader.py contract` (executed by `all`) | `counts: {resume: 0, spawn: 15, total: 15}`; all 15 names/roles match across spec/tasks/registry; `registry_matches_dispatch: true`; all 15 `trailer_matched`, `path_contained`, `prompt_prefix_matches` true; `resumeSends: []`; exact per-seat output: `checks.json#/contract` |
| Ledger | `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-74/w1/ReviewerGates/independent-reader.py ledger` (executed by `all`) | exact current/freeze row below; no round-74 row at observation; `r74_required_at_freeze: false`, `r74_required_at_record: true` |
| Outside-lane writes | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff --name-only 021914c0e638454e507087accfe41af1ab69f185` (executed by contract check) | Exact lane-relative changed paths in `checks.json#/contract/tracked_changes_since_freeze`; cannot enumerate or attribute outside-lane writes. **Not established**, not a pass. |
| Runtime identities | `read /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-74/r74-w1.ready.dispatched:1-30` | timestamp `2026-11-04T04:35:44`; 15 seat→runtime mappings, including `ReviewerGates: ReviewerGates-7`; registry agentId values remain null. This marker supplies mappings, not process execution/route continuity proof. |
| Semantic tooling | `read xd://lsp` | `No such tool: xd://lsp.` No server/status/references/definition/diagnostics available. Literal searches/source reads only; not represented as semantic proof. |

### Exact round-74 gate object

```json
{
  "claims_file": ".ufo/waves/round-74/claims.json",
  "findings": [],
  "freeze": "021914c0e638454e507087accfe41af1ab69f185",
  "instruments": [
    "tools/round-74/probe-mutation.py",
    "tools/round-74/record-audit.py"
  ],
  "verdict": "CLEAN"
}
```

Its exact instrument list is `["tools/round-74/probe-mutation.py", "tools/round-74/record-audit.py"]`: equals the two instruments named in claim objects, and is a subset of the five declared instruments. `reported_equals_claim_named: true`, `reported_subset_declared: true`.

### Every independent pin

Each row executes `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show 021914c0e638454e507087accfe41af1ab69f185:<path>` and hashes the raw stdout with `hashlib.sha256(data).hexdigest()`. Expected values come from that same commit's claims container, not the working tree.

| Path | Expected SHA-256 | Actual SHA-256 |
|---|---|---|
| `tools/round-74/seam-probe.py` | `81d6a43223c5504eb4ad7312563d7a9b1bd3f6288e39c196ee1d542a4c617039` | `81d6a43223c5504eb4ad7312563d7a9b1bd3f6288e39c196ee1d542a4c617039` |
| `tools/round-74/probe-mutation.py` | `156a92945f2acc257b025378e4de49064734a9652de19d6ed04b602161f0319b` | `156a92945f2acc257b025378e4de49064734a9652de19d6ed04b602161f0319b` |
| `tools/round-74/record-audit.py` | `5bcd1462ee25c3ab3ef92f5ff22eda43bfc15dbbca15750f4c678eb9b1a32c5c` | `5bcd1462ee25c3ab3ef92f5ff22eda43bfc15dbbca15750f4c678eb9b1a32c5c` |
| `tools/round-74/freeze-pins.py` | `29c75405ae7d853b0df7c2ead32b2d2b750be8e80777f6161ec738f8910f5e43` | `29c75405ae7d853b0df7c2ead32b2d2b750be8e80777f6161ec738f8910f5e43` |
| `tools/round-74/controls.py` | `851ec9edef3f681abc2c8469716a9613e37ac7884b79dfcf1f5dc70ebba3e86d` | `851ec9edef3f681abc2c8469716a9613e37ac7884b79dfcf1f5dc70ebba3e86d` |
| `tools/round-73/seam-probe.py` | `9c286fd7187e25a8c6de5d743e21d0402ec6c9862a14aecfaed75b2006710939` | `9c286fd7187e25a8c6de5d743e21d0402ec6c9862a14aecfaed75b2006710939` |
| `tools/round-73/packed-elf.py` | `ed3e26fab2ace12e94956704bab68940443fe093bd10aa2c70c75aa9c3284c1b` | `ed3e26fab2ace12e94956704bab68940443fe093bd10aa2c70c75aa9c3284c1b` |
| `tools/round-73/record-audit.py` | `3dc6fc9f2034e0e8cd6f4b136a4efafe929eb28642c6dc32fff861430520443f` | `3dc6fc9f2034e0e8cd6f4b136a4efafe929eb28642c6dc32fff861430520443f` |
| `tools/round-72/seam-probe.py` | `602b305d79222222c1f17c51cc10365246ecfc184cdd4afd8f773a0f5fd5f0e2` | `602b305d79222222c1f17c51cc10365246ecfc184cdd4afd8f773a0f5fd5f0e2` |

The five `instruments` rows also match the blobs at declaration `b3a7e28089582ce5fb002a1b88e5295caf696b9f` (each exact digest and command revision in reader and `checks.json#/pins/declaration_rows`).

### Ledger timing

```text
round-73	FLAGGED	INSTRUMENT_PIN_MISMATCH	round-73 freeze 8b928422 pins two round-72 producer digests that are not the blobs at the freeze; corrected by an appended erratum at the record revision (the gate reads pins from the freeze commit, so the finding is permanent for this freeze); the hardened instruments' later revisions are disclosed in instrument_supersessions
```

The round-73 row correctly remains FLAGGED / INSTRUMENT_PIN_MISMATCH. Round-74 CLEAN row is required **at record**, not at freeze; absence while this wave is still collecting work is not a freeze defect. Canonical logic: `tools/round-29/freeze-gate.py:177-188` derives expected disclosure rows from every audited freeze only when `--disclosures` is supplied and fails missing/mismatched/stray rows. `tools/round-74/record-audit.py:196-211` D3 independently requires the ledger to carry rounds 72–74 at the measured record.

## Residual risk and verification gaps

- No filesystem-wide audit stream or complete attributed command history is in the three wave contracts. Therefore this review cannot certify that no other seat wrote outside the lane. SentinelScope-11 explicitly reported its assigned static instrument audit also cannot certify fleet seat activity. No external-write incident is inferred from missing observability.
- The spec, dispatch and registry describe one 15-seat batched wave with 4/15 attack seats (26.67% rounded 27%). Policy ceiling 256 and globalRunnerCeiling 1056 are configuration, not measured saturation. No saturation achievement is claimed in these receipts.
- All fifteen report files were absent at the concurrent snapshot (including this report, not yet written); that is a live-wave snapshot, not a final missing-report defect. Completion needs the hub to collect each exact trailer destination.
- The dispatch has zero resume sends. No resume preflight or same-identity reroute was executed in this assignment; `resume_continuity_v1` zero-mutation behavior cannot be certified from a no-resume contract. No alternative runtime was invoked.
- These are review recommendations and evidence, not admission, judgment, integration, or shipping.

## Self-evaluation

Accuracy 4/5 (external writes not observable); completeness 4/5 (all requested checks attempted, external attribution remains unprovable); clarity 4/5 (full historical gate output is linked rather than duplicated); actionability 4/5 (fix one target typo and collect final reports); conciseness 4/5 (nine explicit digest pairs retained for audit). Overall 4.0/5. Main remaining improvement is attributed filesystem evidence, not another lane-only diff.
