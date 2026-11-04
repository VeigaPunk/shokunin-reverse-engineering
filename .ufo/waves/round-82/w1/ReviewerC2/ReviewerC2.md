# ReviewerC2 — frozen C2 review

## Scope and axes

Axes: execution-byte identity; exact sourced-row binding; work-root containment; runtime pin refusal. Reviewed the new `tools/round-82/printed-command.py` at freeze `2d63e1a7d04d4dcff45c3908bb51be787a2f22e1`, SHA-256 `d447f6b487f2f9b39e0585ddf48f41cf4068cb5da6f64a299cf7be3066aacd8c` (matches the container's instrument pin). Declaration-to-freeze diff for that file was empty; base-to-freeze adds its 614 lines. Findings are recommendations, not admission decisions.

All source paths/lines below refer to that frozen instrument unless stated otherwise. Retained executable demonstration: `probe.py`; observed receipts: `counterexamples.json`, both alongside this report. The demonstration invokes unchanged frozen functions, not a replacement instrument.

## Findings, by severity

### P1 — revision pin checks different bytes from those executed

`pin_matches` lines 140–143 hashes `git show REV:script`; `run_block` lines 177–188 then executes the relative script in `cwd=root`, reading current worktree bytes. There is no binding between those two byte streams. Every battery execution arm (lines 284–309) and CLI `--run` (587–591) takes this path. Thus a valid revision pin is insufficient to identify the executed instrument.

Observed `wrong_worktree_bytes`: private fixture committed a pinned script, then changed only its worktree copy. `run_block` returned `executed=true`, rc 0, integer counter 3, and no defects; its output identified `origin=uncommitted-worktree`. Pinned digest was `7a013df13b83ae48d0fdd79dc8d00282b53856ec79a4509296828ef6bd0c58b6`, executed-copy digest `949d92fc3993b5f0e76ead1965779d7a7ce9e9b0dbb7a54cd02d4fcfb9e8b03e`.

Minimal repair candidate: execute from a private revision-materialized tree whose script bytes have been checked against the pins, rather than executing an unrelated live worktree. At minimum reject execution-file digest mismatch immediately before launch; that narrower check still leaves a check/use race. Retain the worktree-mismatch case as a refusal regression. The separate R76 subprocess at lines 311–318 also executes a live relative path without calling `pin_matches`; use the same byte-identity rule there.

### P2 — `source: S2990` satisfies a requirement to cite S299

`entry_cites` lines 237–240 uses substring membership. `sourced_arm` directly trusts it at lines 251–267. Observed `source_S2990`: an entry containing only `source: S2990 — unrelated row` produced `entry_cites_row=true`, `met=true`, no defects. No S299 citation was present in the synthetic entry. The analogous plan check at line 249 also accepts a plan containing only `S2990`; observed `plan_S2990` was defect-free.

Minimal repair candidate: tokenize source identifiers and compare exact identifiers in both locations, e.g. membership in `re.findall(r'\bS[0-9]+\b', source_line)` rather than substring membership. Include S2990 and an unrelated exact row in refusal cases, retaining the existing genuine S299 acceptance case.

### P2 — a queued source is accepted as mined when another cell contains “mined”

`sourced_arm` line 246 tests `"mined" in row` and the date anywhere in the row, not the status/opened columns. `corpus/SOURCES.md:5` declares separate `teaches`, `status`, and `opened` columns. Observed `mined_arbitrary_cell`: a row with teaches=`mined discussion only`, status=`queued`, opened=`2026-11-04` produced `row_mined=true`, `met=true`, no defects.

Minimal repair candidate: parse the registry row according to its declared columns and compare status exactly to `mined` and opened exactly to `2026-11-04`. Reject wrong-column tokens and queued status even when prose discusses mining. No broad Markdown parser is needed for the fixed registry contract, but account for escaped delimiters if the existing format permits them.

### P2 — containment validates an API argument, not the actual printed output argument

`run_block` lines 177–181 validates its separate `out` parameter, but does not bind that parameter to the `--json-out` value in `argv`. Lines 187–203 execute the latter and read the former. Observed `literal_output_escape`: a pinned, unchanged fixture command with literal `--json-out <scratch>/outside-work.json`, alongside a contained API `out`, executed and created the outside-work file. It then accepted a stale, pre-existing contained receipt, returning no defects and integer counter 3. Both paths were inside this seat's authorized scratch; only the declared work-root boundary was crossed.

Minimal repair candidate: before execution parse/bind the actual output/work arguments used by the accepted command grammar, require their resolved values to equal the intended contained targets, and require a newly produced receipt (fresh per-invocation output directory or removal/refusal of an existing target). Preserve the printed argv or refuse it; do not silently rewrite it. This example changes a synthetic block, not the currently printed canonical C1 block: it establishes a helper-boundary defect, not an observed escape by the frozen canonical command.

## Controls and retained limits

- `revision_pin_mismatch`: wrong revision digest refused with `SCRIPT_PIN_MISMATCH`, `executed=false`.
- `unpinned_script`: non-member path refused with `SCRIPT_NOT_PINNED`, `executed=false`.
- Explicit outside `out` and a pre-existing output symlink escaping work were both refused without execution. These controls narrow the containment defect to argv/API identity, not a failure of `realpath/commonpath` itself.
- `different_source_control`: exact unrelated S260 citation correctly yielded `SOURCED_ENTRY_UNCITED`.
- Source predicate cases replace only `read_text` with synthetic text; execution cases use real private Git history and actual child execution. They do not establish a full six-arm false green for a forged production revision.
- LSP device unavailable: requesting `xd://lsp` returned `No such tool`. Definitions/callers were inspected textually; grep is not semantic references proof. No diagnostics or semantic completeness claim.
- No lane battery, selftest, repository build/lint/test sweeps, production edits, integration, promotion, alternative runtime, or admission performed. No resume/rerouting/saturation behavior exists in the assigned C2 slice; none is claimed.
- No repair candidate was applied or verified. L1 should retain the stated adversarial cases when evaluating a repair and rerun the canonical printed command itself.

## Execution hygiene

Read tooling authorization first. Used existing Python 3.14.8 and Git 2.56.0; no installations/updates, package transactions, PATH writes, or configuration inspection. Private fixture mutations used absolute `git -C`; fixture toplevel was asserted before staging and committing. `TMPDIR` was explicitly set to the single authorized scratch root. Scratch was removed in `finally`; observed `scratch_removed=True`. No scratch-tree inventory was performed. All retained files are in this seat directory.

## Self-evaluation

Accuracy 4/5: frozen functions and direct receipts, but not a full forged battery. Completeness 4/5: all assigned attack classes covered; no concurrent filesystem race demonstration. Clarity 4/5: exact cases and source lines, with four findings requiring some detail. Actionability 4/5: minimal repair directions and regression shapes, not applied patches. Conciseness 4/5: evidence and limitations retained rather than reduced to verdict labels. Overall 4.0/5. Highest-impact improvements are binding executed bytes and actual argv paths; no authority to implement them in this seat. The evidence/limits are intended to support the user's assessment rather than assert acceptance.
