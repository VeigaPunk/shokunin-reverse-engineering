PARTIAL

## Findings (severity-ranked)

### Medium — S040 is the wrong source identity
**Observation:** At measured S, `corpus/SOURCES.md:46` assigns S040 to the `rea-agents@6.5.0` Harmony application projection (`artifactCommands.js`, `harmonyApplication.js`, `mobileApplicationGraphProjection.js`); it covers Stage/FA hints and Harmony inventory, not Rizin argv, digest gating, or limits. This contradicts the source label in the target note at `corpus/knowledge/2026-10-20-r20-rizin-command-observation.md:1`, repeated at `:41,43,49`. The actual retained Rizin source extracts are `.../evidence/c2/rizin-pe/rea-cli-source-notes.md:5-9`; the limits/schema observations are in `.ufo/waves/round-20/w1/ScoutRizinSchema.md:65-70,83-90`. **Inference:** This is a stale/misattributed source ID, not a contradiction of the observed run results; those separate retained files support the cited behavior.

### Low — Digest-error mapping is overgeneralized
**Observation:** Target note `:37` says “digest errors are converted to `AnalysisInputError`.” Its cited source notes at `.ufo/waves/round-20/evidence/c2/rizin-pe/rea-cli-source-notes.md:7` limit this to *non-access-denied, non-timeout* digest failures. The two tested inputs are missing-path and directory (receipts `03-missing-path/receipt.json:8-13`, `04-directory-path/receipt.json:8-13`); they do return exit 1 and the same generic error. The source supports the tested cases, but not the unqualified all-errors wording. Narrow the sentence to the stated exclusions; the output itself does not expose errno, as the note correctly says.

### Low — “Only input rule” omits schema constraints
**Observation:** Target note `:41` calls “no CR/LF/NUL” the “only input rule.” The retained schema description says path and command are required, both nonempty, and the object is strict; the command refinement rejects CR/LF/NUL (`rea-cli-source-notes.md:6`; `w1/ScoutRizinSchema.md:13-25,68-70`). The intended claim—that there is no command allow/deny list and no shell-command filter—is supported. As written, “only input rule” is broader than “only command-content rule.”

## Evidence and commands

All reads below were against Git object S=`5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9`; each completed with exit 0. No REA command was run by this reviewer.

- `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show 5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9:corpus/SOURCES.md` — exit 0; row S040 is the Harmony source above.
- `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show 5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9:.ufo/waves/round-20/evidence/c2/rizin-pe/rea-cli-source-notes.md` — exit 0; lines 6-8 contain the schema and error-class exclusions, line 9 the command/plugin warning.
- `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show 5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9:.ufo/waves/round-20/w1/ScoutRizinSchema.md` — exit 0; lines 68-70 describe the no-allow-list/one-line rule, lines 83-94 the 120000 ms / 16 MiB limits.
- `set -o pipefail; for p in 03-missing-path 04-directory-path 07-missing-json-full 08-directory-json-full; do git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show 5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9:.ufo/waves/round-20/evidence/c2/rizin-pe/$p/receipt.json | jq -c '{exit,input_artifact,evidence_ids,stdout}'; done; rc=$?; printf 'exit=%d\n' "$rc"` — exit 0. Outputs record exit 1, `nonexistent_path` / `directory`, null input digests, empty Evidence IDs, and identical stdout hashes within each pair.

**Retained run status cross-check:** the 13 ELF receipts/output envelopes report exit 0, `complete`, no truncation or artifact change, and post-run digest equal to the subject digest; jq `iI` repeat has the same stdout SHA-256 and Evidence ID. Its `iS` output and retained `readelf -W -S /usr/bin/jq` output contain the same 27 named sections. The PE table at target `:23-29` matches its receipts/output envelopes: `iI`, `iS`, unknown command, and `iI; iS` exit 0; invalid paths and JSON full-output retries exit 1; retained IDs and stdout hashes match. The outputs support the PE fields/sections and the Rizin command-level unknown-command error at `:31-35`. The note’s cap non-reach claim is consistent with retained output sizes/statuses and recorded durations.

## Residual risk / verification gaps

`!` was not invoked in the retained C2 runs; shell-capability remains documented by S044 and the source warning, while the earlier `!echo` capture is explicitly unretained. The note correctly discloses that the REA Evidence does not bind the exact Rizin executable (`provider.version: null`) and does not bind external plugin/file/network effects. No live reruns or tests were performed.