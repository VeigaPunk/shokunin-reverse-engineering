# C1 R18-VALIDATOR-DIGEST — adversarial review

## Findings

### Medium — `s_validator_digest` can false-close if the guard is disconnected from the validator entrypoint

This is a gap in the C1 counter, not a defect in the observed main implementation. In `.ufo/waves/round-19/tools/routed-r18.py:128-143`, the check loads `_validator_pin` from the revision's `routed-defects.py` and calls that helper directly with synthetic good/wrong digests. It does not invoke `_d_validate16`/`evaluate` to prove that the real validator path uses the helper. At observed main, the wiring is present: `.ufo/waves/round-18/tools/routed-defects.py:497-499` calls `_validator_pin(root, doc)` and records its result.

**Mutation observation:** in an isolated clone detached at observed main `d0690fd44f46d8a7fe9da5f01c6be723d12abd41`, I changed only the call site back to the old format-only acceptance and changed the retained summary digest to 64 zeroes; committed test revision `a64de5ddf854e38a1d99c179b21369f044dcbade`. `routed-r18.py --strict` still reported `R18-VALIDATOR-DIGEST` named/substance true and `open_count: 0` (exit 0). Running that mutant's actual round-18 gate showed `validator-sha256-pinned: ok=true`, detail `validator_sha256='000…000' (format only)`; its overall strict exit was 1 only because the unrelated R17-REGISTRY check was open. This is a demonstrated false close of the validator-digest route under a plausible regression.

### Low — eight manifest rows need not represent eight distinct copies

`.ufo/waves/round-19/tools/routed-r18.py:153-163` requires `len(copies) == 8`, then hashes each row's label-resolved file and trusts that row's `validator_exit` is zero. It does not require eight unique labels. In a separate isolated clone at the same main tip, I changed the second manifest row to repeat the first label and digest; test revision `1eaa5d7cd3a375a100d835f0a5fb7f7a8f755bbd` still produced `R18-VALIDATOR-DIGEST` substance true, open count 0, exit 0. Thus the counter can claim “8/8 retained copies re-hash” when one copy is counted twice.

This is not a false closure on the observed main snapshot: its manifest has eight distinct labels (`digests.json:1-82`: calib-esbuild-0.25.12, calib-shfmt, pro-aether, pro-containerd-shim, pro-esbuild-0.21.5, pro-esbuild-0.27.7, pro-notesmd-cli, pro-op), and I independently re-hashed all eight immutable receipt blobs against the listed SHA-256 values.

## Immutable-blob re-derivation and actual counter results

**Observation:** `refs/heads/main` resolved to `d0690fd44f46d8a7fe9da5f01c6be723d12abd41`; B is `8a8da7e19375aadc66c6bcbff0bbcbb596048fb0`.

The routed correction is explicitly recorded at `corpus/lessons/round-19.md:57` and `SCORECARD.md:2484`. The fixed round-18 implementation pins `VALIDATOR_REV` to `9011581d84527ba34c675f9cf912e54d2e72d470` and, at `.ufo/waves/round-18/tools/routed-defects.py:402-428`, checks the revision identity and compares the summary's 64-hex digest with SHA-256 of the pinned `RECEIPT_VALIDATE` Git blob. The live call site at lines 497-499 is wired to that check. Re-hashing the immutable pinned blob yielded `618448829ba6c5d743ef10c5b686b9f4e09a3ae09f2da0aa5d0e50e3d239126f`, equal to `evidence/validate16-remap/digests.json:107-109`. The eight immutable copy hashes likewise matched the manifest, and all eight manifest rows state `validator_exit: 0`.

The correction's named claims therefore match the current source and evidence. The count runs also agree with the declared before/after on the observed commits: B reports `open_count=7`, `named_open=7`, `substance_open=7` (exit 1 under `--strict`); main reports all three counts 0 (exit 0). I found no false open or false close in those two actual revision results for this route. The baseline's open state is expected: the old round-18 gate is described as format-only at `SCORECARD.md:2451`; main contains the hash comparison.

Commands and observed exits:

```text
# Resolve the requested immutable revisions; exit 0
 git -C LANE rev-parse 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0 refs/heads/main
 # output: 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0; d0690fd44f46d8a7fe9da5f01c6be723d12abd41

# Both runs use the counter blob at observed main, piped to stdin; pipeline exit is the counter exit
 git --no-optional-locks -C LANE show d0690fd44f46d8a7fe9da5f01c6be723d12abd41:.ufo/waves/round-19/tools/routed-r18.py | python3 -I -B - --root LANE --rev 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0 --strict
 # exit 1; open/named/substance = 7/7/7
 git --no-optional-locks -C LANE show d0690fd44f46d8a7fe9da5f01c6be723d12abd41:.ufo/waves/round-19/tools/routed-r18.py | python3 -I -B - --root LANE --rev d0690fd44f46d8a7fe9da5f01c6be723d12abd41 --strict
 # exit 0; open/named/substance = 0/0/0

# Isolated duplicate-index mutation; exit 0 (false close; open_count 0)
 python3 -I -B /tmp/kr19-w2-SubstanceVALIDATORDIGEST.FuOVZb/clone/.ufo/waves/round-19/tools/routed-r18.py --root /tmp/kr19-w2-SubstanceVALIDATORDIGEST.FuOVZb/clone --rev 1eaa5d7cd3a375a100d835f0a5fb7f7a8f755bbd --strict

# Isolated disconnected-callsite / wrong-digest mutation; exit 0 (false close; open_count 0)
 python3 -I -B /tmp/kr19-w2-SubstanceVALIDATORDIGEST.FuOVZb/callsite-clone/.ufo/waves/round-19/tools/routed-r18.py --root /tmp/kr19-w2-SubstanceVALIDATORDIGEST.FuOVZb/callsite-clone --rev a64de5ddf854e38a1d99c179b21369f044dcbade --strict

# Same mutant through the round-18 gate; exit 1 overall, but validator-sha256-pinned is ok=true for the wrong digest
 python3 -I -B /tmp/kr19-w2-SubstanceVALIDATORDIGEST.FuOVZb/callsite-clone/.ufo/waves/round-18/tools/routed-defects.py --root /tmp/kr19-w2-SubstanceVALIDATORDIGEST.FuOVZb/callsite-clone --rev a64de5ddf854e38a1d99c179b21369f044dcbade --strict

# Re-hash pinned validator and eight immutable copy blobs from the clone's object database; command exit 0
set -o pipefail; repo=/tmp/kr19-w2-SubstanceVALIDATORDIGEST.FuOVZb/clone; git -C "$repo" show 9011581d84527ba34c675f9cf912e54d2e72d470:.ufo/waves/round-17/tools/receipt-validate.py | sha256sum; for f in .ufo/waves/round-19/evidence/validate16-remap/copies/*.receipt.json; do printf '%s ' "$f"; git -C "$repo" show d0690fd44f46d8a7fe9da5f01c6be723d12abd41:"$f" | sha256sum; done; exit ${PIPESTATUS[0]}
```

## Residual risk and verification gaps

- `digests.json` is an immutable Git artifact, but its `validator_exit` and replay fields are recorded claims; this review did not rerun the eight validators. The counter re-hashes the receipts and checks the manifest values, not execution provenance or authenticity against a coordinated rewrite.
- `SCORECARD.md:2493` still labels the 7→0 result a “target” and says “Final measured verdict appended after verification”; it contains no after-revision hash/exit, even though this review observed exit 0 at `d0690fd44f46d8a7fe9da5f01c6be723d12abd41`. This is a scorecard completion gap, not a miscount in the executed main result. The unchanged score 10.0→10.0 (delta 0) and saturation 10.0/window 10 are honest at lines 2493, 2497-2499.
- No `lsp` device was mounted (`read xd://lsp` returned “No such tool”); no LSP status/references/definition/diagnostics were available. Review was direct source and immutable-Git-object inspection, not grep-based semantic proof. No builds, broad suites, REA/Ghidra, carrier execution, installs, or production edits were performed.
