# Round 21 snapshot inputs and expected digests — advisory findings

**Axes:** C1 calibration (tied-lowest) and C2 depth.  
**Scope:** Read-only review of the round-21 frozen contract, battery snapshot/digest code and the named round-20/QUALITY provenance rules. No tests, battery run, REA/provider execution, source-row edits, or production edits were performed. No external URLs were opened; no tools were installed.

## Observed source rules

- `corpus/QUALITY.md:18` (#18) requires execution evidence to retain the measured revision and immutable inputs, not only a boolean; recheck guidance must match the exercised flags/paths or name unexercised variants.
- `corpus/QUALITY.md:19` (#19) distinguishes point-in-time source-revision agreement from temporal stability. Exact located quote (8 words): **“map matches committed source-revision blobs; temporal stability not evidenced”**. It says a temporal-stability claim needs per-path SHA-256 and size pins, UTC timestamps, comparison verdicts at each named instant (including mid-run), and a retained red mutation run.
- `corpus/lessons/round-20-verifier-spotcheck.md:116-126` is a relevant precedent, not a new-round source of expected values: it reports prediction bytes identical to freeze `F`, per-run `map_path`/`map_sha256` checks, log-byte comparisons against retained bindings, and explicitly bounds its unchanged-input conclusion to named revisions/instants. It does not claim continuous custody or rerun mutable external dependencies.

## Round-21 input/digest mechanics observed in source

- `/.ufo/waves/round-21/fixture-contract.json:2-4` labels the contract frozen before measurements and explicitly limits its basis to a local application contract—not JSON-spec required fields or Evidence authentication. Its C1/C2 tables freeze the twelve and twenty cases and expected exits/rules (`:5-17`, `:19-40`); the separation/regression boundary is at `:41-44`.
- `/.ufo/waves/round-21/fixtures/expected.json:1-6` declares `kaidoku-r21-frozen-inputs-v1` and SHA-256 values for `fixture-contract.json` and `fixtures/battery.json`. It contains no digest for `fixtures/expected.json` itself or for `battery.py`.
- `/.ufo/waves/round-21/battery.py:51-58` reads `fixture-contract.json`/`fixtures/battery.json` from the local `HERE` directory, emits the battery-fixture digest as `fixtures_sha256`, then checks those local files against the locally read expected-digest manifest. That is an observed local manifest comparison; this source alone does not anchor the manifest to `--rev` or authenticate it.
- `battery.py:25-29,49-50,64-68,107` separately resolves `--rev`, reads validator/comparator source bytes using `git show <rev>:<path>`, computes their SHA-256, and reports the selected path/digest. `--rev` controls this Git-source selection; the fixture/manifest reads above are filesystem reads from `HERE`.
- `battery.py:108-125` (optional regression) selects R20 predictions, bindings, logs, comparator and extractor from the supplied revision, computes each materialized log digest and compares it with the retained binding's `log_sha256`. This is the battery's explicit expected-digest comparison for retained regression logs.

## Calibration/depth implication and limits

**Observed:** The R21 fixture manifest makes the frozen case bytes auditable by expected digest, while the optional historical regression uses the run receipt's expected log digest. The contract itself disclaims authentication. These are separate from the R20 rule that a digest map is only a snapshot identity unless timestamped observations and mutation controls substantiate temporal stability.

**Inference (high confidence from the inspected code):** Because the expected manifest is read locally and is not itself digest-pinned here, changing both that manifest and the fixture files can preserve a passing local comparison. Likewise, local fixture bytes are not selected from the `--rev` Git tree by the inspected code. Therefore do not describe these checks as authenticated inputs, tamper-proof fixtures, or proof that bytes stayed unchanged during execution. An expected digest recorded in the output should be described as the measured digest unless an independent frozen authority is checked.

## Parent checks after integration freeze

- Run the frozen C1 and C2 battery cases only after the integration revision is stable; preserve all twelve/twenty contract cases and their declared exits. For C2, include the optional R20 regression path if claiming its retained nineteen comparisons remain matches.
- Check that fixture/contract bytes used by the run equal the versions at the selected commit and that the expected-digest manifest itself is pinned to an independent frozen revision/record. Confirm the resulting report names the revision and inputs; do not convert a one-time digest check into a temporal-stability or authentication claim.
- This scout did not run any of those checks. Existing caller-specified commands are in `claims.json:8-11`; the regression option is implemented at `battery.py:108-125`.

**Remaining unknowns:** Whether the integration runner independently pins `expected.json` or binds local fixture bytes to the selected commit outside the inspected battery; whether actual current fixture bytes match the listed hashes; whether a later run will retain timestamped pin maps/red mutation evidence. No live hash verification was attempted.

Report: `.ufo/waves/round-21/w1/ScoutSnapshotScope.md`
