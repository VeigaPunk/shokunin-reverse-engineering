# FinalC2FalseReplay — unchanged frozen C2v3 denial replay

Author-side advisory evidence only. Recorded 2026-10-23T07:16:36.936467Z. Assignment scope: reconstruct the already committed denial control at its frozen parent, commit once privately, run the unchanged C2v3 counter there and read-only at the landed product. No judgment, admission, integration, routing change, semantic repair, new calibration target, or capability acquisition is claimed.

## Axes and result

- **Calibration / discrimination:** the strongest assigned counterexample explicitly denies all four capabilities yet attains the frozen target. Affirmative repaired descriptions attain the same target. Target success is **not calibration improvement**.
- **Frozen-instrument identity / provenance:** identical C2v3 script and claims bytes; pinned manifest and base; one private commit directly on the freeze; denial fixture blob equals the already committed control blob.
- **Coverage and depth:** not measured or changed by this replay; no improvement or regression is inferred.

| Input | Immutable measured revision | UTC start → end | Observed result |
|---|---|---|---|
| Exact committed denial fixture, reconstructed at freeze | `49bc191c4d1dd4d4110966f598d4f13f80f92de2` | 2026-10-23T07:14:34.758386Z → 2026-10-23T07:14:34.834708Z | `statements=4 match=4 target=4 reverse_mismatch=0`, exit 0 |
| Landed product, read-only | `bb0af56c29e7b4c11d0583ed6697d0e17aba9d26` | 2026-10-23T07:13:28.386575Z → 2026-10-23T07:13:28.462475Z | `statements=4 match=4 target=4 reverse_mismatch=0`, exit 0 |

Observed shared-word counts (rounds 13 / 14 / 17 / 27): denial **8 / 12 / 12 / 11**; product **19 / 18 / 16 / 16**. Full outputs differ in row indices and counts, but their target lines and exits are identical. The old control receipt is not substituted for this new run.

## Counterexample bytes and truthful-repair comparison

The following is the complete decision-bearing denial section, extracted from the immutable committed fixture at `411f3a80a1efefabe2ba12f227147023cfbce4bd:.ufo/waves/round-32/controls/c2-negative/SCORECARD.md`. The entire 273,398-byte fixture remains committed there; its hash and replay blob identity are retained below. It is below the 1 MiB fixture cap.

```markdown
## Capabilities

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| curated source registry for existing REA frontier | This capability was never demonstrated and cannot capture anything. It cannot retain opened, scoped study sources, ordered paths, or recheck cadences. | `corpus/SOURCES.md`; `corpus/lessons/round-13.md` | arc3-loop1-round13 |
| local raw-quote/heading regression audit | This capability was never demonstrated and cannot capture anything. It cannot reject the retained splice or wrong section, accept corrected controls, refuse malformed/tampered inputs, or pin frozen manifest/source inputs. | `.ufo/waves/round-14/tools/quote-fidelity.py`; `.ufo/waves/round-14/fixtures/expected.json`; `.ufo/waves/round-14/verification.json` | round-14 |
| retained REA Ghidra-session log capture | This capability was never demonstrated and cannot capture anything. It does not run analyze on a pinned carrier in a private-TMPDIR session and never keeps ghidra.log or script.log; no receipt validates offline. | `.ufo/waves/round-17/run-carriers.sh` | round-17 |
| cross-pin evidence-ID attribution for saved REA envelopes | This capability was never demonstrated and cannot capture anything. It cannot attribute a saved envelope from its bytes using an installed package's canonical digest code, under either rule. | `tools/round-27/xpin-attribute.mjs` | round 27 |
```

The corresponding affirmative, bounded product rows below come from `bb0af56c29e7b4c11d0583ed6697d0e17aba9d26:SCORECARD.md`, not from a reconstructed paraphrase. “Truthful repaired descriptions” here refers to these already-recorded bounded summaries; this seat did not freshly re-demonstrate the four operations or reopen their underlying run receipts.

```markdown
| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| cross-pin evidence-ID attribution for saved REA envelopes | attributes a saved envelope to the `rea-agents` 6.5.0 id rule, the 6.7.0 rule, both or neither, from its bytes, using each installed package's own canonical digest code | `tools/round-27/xpin-attribute.mjs`; checker `tools/round-27/c2-xpin-check.py`; seat report `.ufo/waves/round-27/w1/BuildXpinTool.md`; receipts `corpus/evidence/round-27/c2/` | round 27 |
| curated source registry for existing REA frontier | Keeps opened, scoped study sources, ordered paths, recheck cadences, an auditable bounded search, and a source rejection with evidence and flip; source text is not held-capability evidence | `corpus/SOURCES.md`; `corpus/lessons/round-13.md` | arc3-loop1-round13 |
| local raw-quote/heading regression audit | Rejects the retained S017 splice and S018 wrong section, accepts corrected controls, and refuses malformed/tampered inputs; frozen runs pin every manifest/source input | `python3 -I .ufo/waves/round-14/tools/quote-fidelity.py --selftest`; `--frozen .ufo/waves/round-14/fixtures/expected.json`; `.ufo/waves/round-14/verification.json` | round-14 |
| retained REA Ghidra-session log capture | Runs REA analyze on a pinned carrier in a private-TMPDIR session and keeps ghidra.log/script.log before close; the receipt validates offline. Stored mid-run pin checks are verdicts, not full maps | `bash .ufo/waves/round-17/run-carriers.sh <LABEL>`; `.ufo/waves/round-17/verification.json`; `corpus/lessons/round-17-verifier-spotcheck.md` | round-17 |
```

The product preserves its four earlier luna/arc capability rows and the cross-pin row, and adds the three historical rows. The negative fixture instead replaces the original five-row summary with four denials; the single reconstruction commit reports four insertions and seven deletions. This is the assigned committed control, not a claimed minimal semantic mutation of the product.

The existing product paragraph expressly says: “C2v3's lexical counter is falsified by negative prose and word bags (`.ufo/waves/round-32/controls/c2-negative/receipt.json`); a passing numerical alignment is not calibration improvement.” This replay agrees with that limit and supplies no reason to reverse it.

Pinned outside-record items used by the unchanged instrument:

```json
[
  {
    "round": 13,
    "admitted": true,
    "capabilities_added": [
      "source-curation registry (22 opened rows, scoped tiers, ordered study paths, reasoned rejection; no domain-operation claim)"
    ]
  },
  {
    "round": 14,
    "admitted": true,
    "capabilities_added": [
      "local raw-quote/heading regression audit (bounded retained-defect controls; committed CLI and frozen evidence)"
    ]
  },
  {
    "round": 17,
    "admitted": true,
    "capabilities_added": [
      "retained REA Ghidra-session log capture"
    ]
  },
  {
    "round": 27,
    "admitted": false,
    "capabilities_added": [
      "cross-pin evidence-ID attribution for saved REA envelopes (tools/round-27/xpin-attribute.mjs, SCORECARD ## Capabilities, first-working round 27)"
    ]
  }
]
```

In particular, round 27 has `admitted: false` at the pin. These are four outside-recorded `capabilities_added` statements, **not four admitted rounds**. The counter includes such statements irrespective of the admitted boolean (`manifest_statements`, instrument lines 68–78); this report does not inflate their provenance.

## Why the counterexample works; smallest safe correction

**Observed implementation:** `words()` (lines 125–126 of the frozen instrument) forms lexical word sets. The decision at lines 167–171 accepts at least five shared words after the label, unique-round, and resolving-anchor checks. The fixture preserves those lexical/path/round conditions while negating capability possession and performance. No semantic polarity condition exists in that frozen calculation. All four denial rows exceed its unchanged threshold.

**Inference:** satisfying this target does not distinguish the affirmative bounded summaries from explicit denials, so it cannot establish calibration improvement. Larger shared-word counts in the product are not an authorized replacement measure. This is an instrument discrimination defect, not a calibration tradeoff that this author-side seat may waive. Any canonical closure decision remains outside this report.

**Smallest safe correction:** retain the already landed truthful summary maintenance and the already declared **C2 HONEST STOP**; retain both false-accept and product outputs; do not turn 4/4 into a calibration gain. Do not change/refreeze/relabel C2, repair its predicate, or invent another target. The product already carries this caveat, so no production edit is proposed. This replay does not independently establish whole-repertoire calibration, fresh operation of the historical capabilities, or any mastery/saturation conclusion.

## Immutable inputs and custody

| Input | Committed object locator | Bytes | SHA-256 |
|---|---|---:|---|
| Unchanged C2v3 instrument (also identical at product and replay) | `f382e3b7978e6091a19ca93277c15a75c0016b43:tools/round-32/c2-capability-calibration-v3.py` | 15665 | `5955e8ace76d93c7891a43ca282f129c8874cd1878a05c9f29e0b81d3cab2f9f` |
| Frozen C2v3 claim (also identical at product and replay) | `f382e3b7978e6091a19ca93277c15a75c0016b43:.ufo/waves/round-32/claims-v3.json` | 4870 | `a3be7e40df5a96cfa50df192adaef5b8f7b1c6e1470c560510f872185ec5171d` |
| Committed denial fixture, copied verbatim to replay SCORECARD.md | `411f3a80a1efefabe2ba12f227147023cfbce4bd:.ufo/waves/round-32/controls/c2-negative/SCORECARD.md` | 273398 | `201a320ee75c92fd85ac139943036fbc936b6878dbf0b071229e68db70421796` |
| Product SCORECARD.md | `bb0af56c29e7b4c11d0583ed6697d0e17aba9d26:SCORECARD.md` | 275937 | `147368d04410f2ced5725e24fba02a226bc7d89943fd8df85cb108f6f918f10c` |
| Frozen description/anchor base SCORECARD.md | `283aad7fe56d82f4ed4f8e43f099c2e1ceed5525:SCORECARD.md` | 274232 | `bba9f55de85001d6259ed728bdec82a20dd49830ccb9e01634909bb14c9c38e3` |
| Pinned outside capability record (input, not a generated fixture) | `cef00867ab3279ac2c2d10421e3e62c0e5d693f3:MANIFEST.json` | 1242275 | `2e089615936dae60d1b4ab3883dbbc8ed7608018b9c7f4694209207d84b3207f` |

- Replay parent: `f382e3b7978e6091a19ca93277c15a75c0016b43`; replay tree: `55b3dea2acf5ee1d7156c58cb73a6bd38a0523e3`.
- Replay `SCORECARD.md` blob: `5883c84c34799c17b4257eb25782ffab3eca9461`; committed control blob: `5883c84c34799c17b4257eb25782ffab3eca9461` — identical.
- Product tree: `b6372d2da1c4d26643c09563aa36529de3cf6c04`; product `SCORECARD.md` blob: `a41e6bca7a475bac1cae69648951dc8d33b1a218`.
- Instrument blob, replay and product: `d450cb9fa013625f1ce6597bdaf3012d344a2f6c`; claims blob, replay and product: `7d38b604313d7ff5a9f03bf446eb4eb1c5d9f0ad`.
- Reconstruction wrote exactly the committed fixture stdout to private `SCORECARD.md` through the write tool at 2026-10-23T07:14:09.751620Z; write tool reported 273,398 bytes. No counter or predicate file was edited.
- Private clone: `/fast/scratch/hyaku/kaidoku-r32/a2residual/FinalC2FalseReplay/clone`. All Git writes were confined there; all Git argv specify absolute `-C`. `GIT_DIR`, `GIT_WORK_TREE`, and `GIT_INDEX_FILE` were removed from every recorded subprocess environment. Commit identity overrides: {"GIT_AUTHOR_NAME": "Kaidoku residual C2 reviewer", "GIT_AUTHOR_EMAIL": "kaidoku-residual-c2@example.invalid", "GIT_COMMITTER_NAME": "Kaidoku residual C2 reviewer", "GIT_COMMITTER_EMAIL": "kaidoku-residual-c2@example.invalid"}.
- Source lane/fleet Git state, production files, routing, and MANIFEST were read-only. Only the assigned report was written in the lane. No held item was inspected or retried.
- Every recorded subprocess used a 900-second `communicate` timeout, a new session/process group, and group-kill cleanup. No timeouts occurred; remaining owned groups: `[]`. No REA/Ghidra invocation, carrier execution, other test/build/selftest, or model runtime was run.
- Tools observed: Python 3.14.8; Git 2.56.0. No package installed or updated. Host-wide pacman pause respected.

## Exact scoring receipts

Arrays below are the exact executed argv (no shell interpolation); `cwd`, UTC, exit, full stdout and stderr are included. The counter reads immutable Git objects at `--rev`; it does not score the moving worktree.

### Denial reconstruction

```json
{
  "label": "negative_counter",
  "utc_start": "2026-10-23T07:14:34.758386Z",
  "utc_end": "2026-10-23T07:14:34.834708Z",
  "cwd": "/fast/scratch/hyaku/kaidoku-r32/a2residual/FinalC2FalseReplay/clone",
  "argv": [
    "python3",
    "-I",
    "-B",
    "tools/round-32/c2-capability-calibration-v3.py",
    "--root",
    "/fast/scratch/hyaku/kaidoku-r32/a2residual/FinalC2FalseReplay/clone",
    "--rev",
    "49bc191c4d1dd4d4110966f598d4f13f80f92de2",
    "--fleet",
    "/home/vgpnk/Projects/shokunin"
  ],
  "exit": 0,
  "stdout": "round-13\tP2-match\trow 1 anchor evidence corpus/SOURCES.md, corpus/lessons/round-13.md; description words 8\nround-14\tP2-match\trow 2 anchor evidence .ufo/waves/round-14/fixtures/expected.json, .ufo/waves/round-14/tools/quote-fidelity.py, .ufo/waves/round-14/verification.json; description words 12\nround-17\tP2-match\trow 3 anchor evidence .ufo/waves/round-17/run-carriers.sh; description words 12\nround-27\tP2-match\trow 4 anchor evidence tools/round-27/xpin-attribute.mjs; description words 11\nstatements=4 match=4 target=4 reverse_mismatch=0\n",
  "stderr": "",
  "timeout": false
}
```

### Landed product

```json
{
  "label": "product_counter",
  "utc_start": "2026-10-23T07:13:28.386575Z",
  "utc_end": "2026-10-23T07:13:28.462475Z",
  "cwd": "/home/vgpnk/Projects/shokunin/kaidoku-shokunin",
  "argv": [
    "python3",
    "-I",
    "-B",
    "tools/round-32/c2-capability-calibration-v3.py",
    "--root",
    "/home/vgpnk/Projects/shokunin/kaidoku-shokunin",
    "--rev",
    "bb0af56c29e7b4c11d0583ed6697d0e17aba9d26",
    "--fleet",
    "/home/vgpnk/Projects/shokunin"
  ],
  "exit": 0,
  "stdout": "round-13\tP2-match\trow 6 anchor evidence corpus/SOURCES.md, corpus/lessons/round-13.md; description words 19\nround-14\tP2-match\trow 7 anchor evidence .ufo/waves/round-14/fixtures/expected.json, .ufo/waves/round-14/tools/quote-fidelity.py, .ufo/waves/round-14/verification.json; description words 18\nround-17\tP2-match\trow 8 anchor evidence .ufo/waves/round-17/run-carriers.sh; description words 16\nround-27\tP2-match\trow 5 anchor evidence tools/round-27/xpin-attribute.mjs; description words 16\nstatements=4 match=4 target=4 reverse_mismatch=0\n",
  "stderr": "",
  "timeout": false
}
```

## Construction, identity, and hash command receipts

```json
[
  {
    "label": "private_clone",
    "utc_start": "2026-10-23T07:13:28.383609Z",
    "utc_end": "2026-10-23T07:13:28.569670Z",
    "cwd": "/fast/scratch/hyaku/kaidoku-r32/a2residual/FinalC2FalseReplay",
    "argv": [
      "git",
      "-C",
      "/fast/scratch/hyaku/kaidoku-r32/a2residual/FinalC2FalseReplay",
      "clone",
      "--no-hardlinks",
      "--no-checkout",
      "/home/vgpnk/Projects/shokunin/kaidoku-shokunin",
      "/fast/scratch/hyaku/kaidoku-r32/a2residual/FinalC2FalseReplay/clone"
    ],
    "exit": 0,
    "stdout": "",
    "stderr": "Cloning into '/fast/scratch/hyaku/kaidoku-r32/a2residual/FinalC2FalseReplay/clone'...\ndone.\n",
    "timeout": false
  },
  {
    "label": "product_input_hashes",
    "utc_start": "2026-10-23T07:13:28.383856Z",
    "utc_end": "2026-10-23T07:13:28.386558Z",
    "cwd": "/home/vgpnk/Projects/shokunin/kaidoku-shokunin",
    "argv": [
      "sha256sum",
      "tools/round-32/c2-capability-calibration-v3.py",
      ".ufo/waves/round-32/claims-v3.json",
      "SCORECARD.md",
      ".ufo/waves/round-32/controls/c2-negative/SCORECARD.md"
    ],
    "exit": 0,
    "stdout": "5955e8ace76d93c7891a43ca282f129c8874cd1878a05c9f29e0b81d3cab2f9f  tools/round-32/c2-capability-calibration-v3.py\na3be7e40df5a96cfa50df192adaef5b8f7b1c6e1470c560510f872185ec5171d  .ufo/waves/round-32/claims-v3.json\n147368d04410f2ced5725e24fba02a226bc7d89943fd8df85cb108f6f918f10c  SCORECARD.md\n201a320ee75c92fd85ac139943036fbc936b6878dbf0b071229e68db70421796  .ufo/waves/round-32/controls/c2-negative/SCORECARD.md\n",
    "stderr": "",
    "timeout": false
  },
  {
    "label": "frozen_checkout",
    "utc_start": "2026-10-23T07:13:48.754227Z",
    "utc_end": "2026-10-23T07:13:49.443169Z",
    "cwd": "/fast/scratch/hyaku/kaidoku-r32/a2residual/FinalC2FalseReplay/clone",
    "argv": [
      "git",
      "-C",
      "/fast/scratch/hyaku/kaidoku-r32/a2residual/FinalC2FalseReplay/clone",
      "checkout",
      "--detach",
      "f382e3b7978e6091a19ca93277c15a75c0016b43"
    ],
    "exit": 0,
    "stdout": "",
    "stderr": "HEAD is now at f382e3b7 round-32: freeze R32-C2 v3 (supersedes v2 before any seat or data: an irrelevant-path control met v2) — anchored evidence and description, before receipts\n",
    "timeout": false
  },
  {
    "label": "stage_reconstructed_fixture",
    "utc_start": "2026-10-23T07:14:16.081186Z",
    "utc_end": "2026-10-23T07:14:17.385490Z",
    "cwd": "/fast/scratch/hyaku/kaidoku-r32/a2residual/FinalC2FalseReplay/clone",
    "argv": [
      "git",
      "-C",
      "/fast/scratch/hyaku/kaidoku-r32/a2residual/FinalC2FalseReplay/clone",
      "add",
      "--",
      "SCORECARD.md"
    ],
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "timeout": false
  },
  {
    "label": "single_control_commit",
    "utc_start": "2026-10-23T07:14:17.385555Z",
    "utc_end": "2026-10-23T07:14:17.412336Z",
    "cwd": "/fast/scratch/hyaku/kaidoku-r32/a2residual/FinalC2FalseReplay/clone",
    "argv": [
      "git",
      "-C",
      "/fast/scratch/hyaku/kaidoku-r32/a2residual/FinalC2FalseReplay/clone",
      "-c",
      "core.hooksPath=/dev/null",
      "-c",
      "commit.gpgsign=false",
      "commit",
      "-m",
      "round-32 residual: replay committed C2 negative scorecard"
    ],
    "exit": 0,
    "stdout": "[detached HEAD 49bc191] round-32 residual: replay committed C2 negative scorecard\n 1 file changed, 4 insertions(+), 7 deletions(-)\n",
    "stderr": "",
    "timeout": false
  },
  {
    "label": "sandbox_immutable_identity",
    "utc_start": "2026-10-23T07:14:34.754731Z",
    "utc_end": "2026-10-23T07:14:34.758141Z",
    "cwd": "/fast/scratch/hyaku/kaidoku-r32/a2residual/FinalC2FalseReplay/clone",
    "argv": [
      "git",
      "-C",
      "/fast/scratch/hyaku/kaidoku-r32/a2residual/FinalC2FalseReplay/clone",
      "rev-parse",
      "HEAD",
      "HEAD^",
      "HEAD^{tree}",
      "HEAD:SCORECARD.md",
      "411f3a80a1efefabe2ba12f227147023cfbce4bd:.ufo/waves/round-32/controls/c2-negative/SCORECARD.md",
      "HEAD:tools/round-32/c2-capability-calibration-v3.py",
      "HEAD:.ufo/waves/round-32/claims-v3.json"
    ],
    "exit": 0,
    "stdout": "49bc191c4d1dd4d4110966f598d4f13f80f92de2\nf382e3b7978e6091a19ca93277c15a75c0016b43\n55b3dea2acf5ee1d7156c58cb73a6bd38a0523e3\n5883c84c34799c17b4257eb25782ffab3eca9461\n5883c84c34799c17b4257eb25782ffab3eca9461\nd450cb9fa013625f1ce6597bdaf3012d344a2f6c\n7d38b604313d7ff5a9f03bf446eb4eb1c5d9f0ad\n",
    "stderr": "",
    "timeout": false
  },
  {
    "label": "sandbox_input_hashes",
    "utc_start": "2026-10-23T07:14:34.754987Z",
    "utc_end": "2026-10-23T07:14:34.758036Z",
    "cwd": "/fast/scratch/hyaku/kaidoku-r32/a2residual/FinalC2FalseReplay/clone",
    "argv": [
      "sha256sum",
      "tools/round-32/c2-capability-calibration-v3.py",
      ".ufo/waves/round-32/claims-v3.json",
      "SCORECARD.md"
    ],
    "exit": 0,
    "stdout": "5955e8ace76d93c7891a43ca282f129c8874cd1878a05c9f29e0b81d3cab2f9f  tools/round-32/c2-capability-calibration-v3.py\na3be7e40df5a96cfa50df192adaef5b8f7b1c6e1470c560510f872185ec5171d  .ufo/waves/round-32/claims-v3.json\n201a320ee75c92fd85ac139943036fbc936b6878dbf0b071229e68db70421796  SCORECARD.md\n",
    "stderr": "",
    "timeout": false
  },
  {
    "label": "product_immutable_identity",
    "utc_start": "2026-10-23T07:14:34.755254Z",
    "utc_end": "2026-10-23T07:14:34.756623Z",
    "cwd": "/home/vgpnk/Projects/shokunin/kaidoku-shokunin",
    "argv": [
      "git",
      "-C",
      "/home/vgpnk/Projects/shokunin/kaidoku-shokunin",
      "rev-parse",
      "bb0af56c29e7b4c11d0583ed6697d0e17aba9d26^{tree}",
      "bb0af56c29e7b4c11d0583ed6697d0e17aba9d26:SCORECARD.md",
      "bb0af56c29e7b4c11d0583ed6697d0e17aba9d26:tools/round-32/c2-capability-calibration-v3.py",
      "bb0af56c29e7b4c11d0583ed6697d0e17aba9d26:.ufo/waves/round-32/claims-v3.json"
    ],
    "exit": 0,
    "stdout": "b6372d2da1c4d26643c09563aa36529de3cf6c04\na41e6bca7a475bac1cae69648951dc8d33b1a218\nd450cb9fa013625f1ce6597bdaf3012d344a2f6c\n7d38b604313d7ff5a9f03bf446eb4eb1c5d9f0ad\n",
    "stderr": "",
    "timeout": false
  }
]
```

## Immutable acquisition receipts

Each stdout is the exact byte body of its named **already committed** blob. To avoid copying the full manifest and historical scorecards into this report, the immutable locator, complete byte length and SHA-256 identify that stdout; the decision-bearing fixture and product sections are reproduced above. These citations do not depend solely on scratch. Needed counter/input bytes are already in the named lane/fleet commits, and both new scoring outputs are embedded here.

```json
[
  {
    "label": "frozen_counter",
    "utc_start": "2026-10-23T07:13:48.754370Z",
    "utc_end": "2026-10-23T07:13:48.755779Z",
    "cwd": "/home/vgpnk/Projects/shokunin/kaidoku-shokunin",
    "argv": [
      "git",
      "-C",
      "/home/vgpnk/Projects/shokunin/kaidoku-shokunin",
      "show",
      "f382e3b7978e6091a19ca93277c15a75c0016b43:tools/round-32/c2-capability-calibration-v3.py"
    ],
    "exit": 0,
    "stderr": "",
    "timeout": false,
    "stdout_immutable_blob": "f382e3b7978e6091a19ca93277c15a75c0016b43:tools/round-32/c2-capability-calibration-v3.py",
    "stdout_bytes": 15665,
    "stdout_sha256": "5955e8ace76d93c7891a43ca282f129c8874cd1878a05c9f29e0b81d3cab2f9f"
  },
  {
    "label": "frozen_claim",
    "utc_start": "2026-10-23T07:13:48.754626Z",
    "utc_end": "2026-10-23T07:13:48.755908Z",
    "cwd": "/home/vgpnk/Projects/shokunin/kaidoku-shokunin",
    "argv": [
      "git",
      "-C",
      "/home/vgpnk/Projects/shokunin/kaidoku-shokunin",
      "show",
      "f382e3b7978e6091a19ca93277c15a75c0016b43:.ufo/waves/round-32/claims-v3.json"
    ],
    "exit": 0,
    "stderr": "",
    "timeout": false,
    "stdout_immutable_blob": "f382e3b7978e6091a19ca93277c15a75c0016b43:.ufo/waves/round-32/claims-v3.json",
    "stdout_bytes": 4870,
    "stdout_sha256": "a3be7e40df5a96cfa50df192adaef5b8f7b1c6e1470c560510f872185ec5171d"
  },
  {
    "label": "committed_negative_fixture",
    "utc_start": "2026-10-23T07:13:48.754787Z",
    "utc_end": "2026-10-23T07:13:48.756569Z",
    "cwd": "/home/vgpnk/Projects/shokunin/kaidoku-shokunin",
    "argv": [
      "git",
      "-C",
      "/home/vgpnk/Projects/shokunin/kaidoku-shokunin",
      "show",
      "411f3a80a1efefabe2ba12f227147023cfbce4bd:.ufo/waves/round-32/controls/c2-negative/SCORECARD.md"
    ],
    "exit": 0,
    "stderr": "",
    "timeout": false,
    "stdout_immutable_blob": "411f3a80a1efefabe2ba12f227147023cfbce4bd:.ufo/waves/round-32/controls/c2-negative/SCORECARD.md",
    "stdout_bytes": 273398,
    "stdout_sha256": "201a320ee75c92fd85ac139943036fbc936b6878dbf0b071229e68db70421796"
  },
  {
    "label": "product_scorecard",
    "utc_start": "2026-10-23T07:13:48.755061Z",
    "utc_end": "2026-10-23T07:13:48.756888Z",
    "cwd": "/home/vgpnk/Projects/shokunin/kaidoku-shokunin",
    "argv": [
      "git",
      "-C",
      "/home/vgpnk/Projects/shokunin/kaidoku-shokunin",
      "show",
      "bb0af56c29e7b4c11d0583ed6697d0e17aba9d26:SCORECARD.md"
    ],
    "exit": 0,
    "stderr": "",
    "timeout": false,
    "stdout_immutable_blob": "bb0af56c29e7b4c11d0583ed6697d0e17aba9d26:SCORECARD.md",
    "stdout_bytes": 275937,
    "stdout_sha256": "147368d04410f2ced5725e24fba02a226bc7d89943fd8df85cb108f6f918f10c"
  },
  {
    "label": "base_scorecard",
    "utc_start": "2026-10-23T07:13:48.755229Z",
    "utc_end": "2026-10-23T07:13:48.757572Z",
    "cwd": "/home/vgpnk/Projects/shokunin/kaidoku-shokunin",
    "argv": [
      "git",
      "-C",
      "/home/vgpnk/Projects/shokunin/kaidoku-shokunin",
      "show",
      "283aad7fe56d82f4ed4f8e43f099c2e1ceed5525:SCORECARD.md"
    ],
    "exit": 0,
    "stderr": "",
    "timeout": false,
    "stdout_immutable_blob": "283aad7fe56d82f4ed4f8e43f099c2e1ceed5525:SCORECARD.md",
    "stdout_bytes": 274232,
    "stdout_sha256": "bba9f55de85001d6259ed728bdec82a20dd49830ccb9e01634909bb14c9c38e3"
  },
  {
    "label": "pinned_manifest",
    "utc_start": "2026-10-23T07:13:48.755370Z",
    "utc_end": "2026-10-23T07:13:48.759638Z",
    "cwd": "/home/vgpnk/Projects/shokunin",
    "argv": [
      "git",
      "-C",
      "/home/vgpnk/Projects/shokunin",
      "show",
      "cef00867ab3279ac2c2d10421e3e62c0e5d693f3:MANIFEST.json"
    ],
    "exit": 0,
    "stderr": "",
    "timeout": false,
    "stdout_immutable_blob": "cef00867ab3279ac2c2d10421e3e62c0e5d693f3:MANIFEST.json",
    "stdout_bytes": 1242275,
    "stdout_sha256": "2e089615936dae60d1b4ab3883dbbc8ed7608018b9c7f4694209207d84b3207f"
  }
]
```

## Preserved preliminary tool failure

Before the timestamped scoring driver, the tool-version probe used the exact shell command below from `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` and returned exit **125**:

```text
python3 --version && git --version && timeout --version
```

Combined command output (the initial probe did not capture separate streams or UTC bounds):

```text
Python 3.14.8
git version 2.56.0
error: the following required arguments were not provided:
  <COMMAND>...

Usage: timeout <DURATION> <COMMAND>...
```

The `timeout --version` interface failure was not retried or treated as a scoring failure; the two authorized counters were run with Python-enforced subprocess deadlines instead. The initial read-only `df -h /fast` succeeded before cloning: `/dev/nvme1n1p2`, size 804G, used 582G, available 222G, use 73%. Scratch-directory creation (`mkdir -p /fast/scratch/hyaku/kaidoku-r32/a2residual/FinalC2FalseReplay`) exited 0 with no output. Their UTC bounds were not captured. No scoring failures were suppressed.

Report: .ufo/waves/round-32/a2residual/FinalC2FalseReplay.md
