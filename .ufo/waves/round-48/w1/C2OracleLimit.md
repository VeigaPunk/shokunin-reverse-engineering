# C2OracleLimit — Round 48 C2 attack

## Verdict

The C2 design executes the round-47 `record.py` source from `--rev`, but its shared dependency `tools/round-46/gate.py` remains imported from the invoking worktree. This leaves a direct worktree-code path into C2 verdicts. It can flip exit 0. I did not complete an isolated positive/negative fixture measurement; do not treat this as an empirically measured successful exploit.

## Worktree-sourced paths

`record2.py` inserts the directory containing its executing script and `../round-46` on `sys.path` (lines 35–37), then imports `gate`. Thus the round-46 gate module used for all these operations is selected from the checkout/worktree, not loaded from `--rev`:

- `gate.freeze_state(root, freeze, rev, CLAIMS)`: frozen-state validation, freeze derivation, touched/restored calculations (evaluate lines 476–479).
- `gate.show(root, rev, path)`: all committed-byte reads for `SCORECARD.md`, `tools/round-47/record.py`, receipt files, and other oracle reads (lines 67, 480, 483; battery 444, 447).
- `gate.out_path(...)`, `gate.main_guard(...)`, and `gate.emit(...)`: output-path policy, exception-to-exit conversion, and receipt emission (CLI lines 513–520).
- `gate.scratch(...)` is used by the optional selftest (line 527).

The executed committed round-47 oracle itself also imports `gate` at its own source lines 28–30 (verified from frozen `tools/round-47/record.py`). In this invocation, Python's `sys.modules['gate']` is already populated by the worktree import, so its calls to gate helpers likewise resolve to that same worktree module. Its dispatch counting uses subprocess git calls; its `collect`, `derive`, and `corrects` logic is committed oracle code, but its data retrieval delegates to the worktree gate-backed `files` callback.

## Verdict-moving avenues

A modified worktree `gate.py` can alter freeze acceptance or bytes returned by `show`, changing the oracle input, facts about the committed card/receipts, or the resulting freeze verdict. More directly, it can return chosen content for selected paths (including the card or receipts), return `None` to influence absence/error branches, or change `freeze_state` to accept a failed freeze. It can also change `main_guard`/`out_path`/`emit` behavior, including error handling and reported output. Therefore at least the freeze and semantic score verdict are not fully pinned to frozen infrastructure. This is code-path analysis, not a claim that a particular attack fixture has been run.

## Attempted measurement / verification gap

I extracted the frozen `record2.py` to `/fast/scratch/hyaku/kaidoku-r48/C2OracleLimit/record2.py` and invoked it with `--root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --freeze dc73587a8b9c1a23ba5a91dc7707ac7381a8b873 --rev dc73587a8b9c1a23ba5a91dc7707ac7381a8b873 --no-battery`. It exited 1 with `ModuleNotFoundError: No module named 'gate'` because the extracted script lacks its expected sibling module. No verdict was obtained; battery was not run. No fixture repo or commit was created. Exact stdout/stderr receipt, stdout hash, and UTC timestamp were not captured, so this is not a citable command receipt.

Baseline repository HEAD observed: `ac02a79ff84133220d01ce3b59a4789b7004dbc5`, not the declared freeze; the lane had extensive pre-existing unrelated modifications. No files outside this seat report were changed by me. No tooling installed.

## Recommendation

Before landing, either pin and execute the round-46 gate from committed bytes (including the oracle's helper resolution), or explicitly narrow the claim so it does not assert that worktree replacement cannot affect C2. A useful falsification fixture should run the committed counter while replacing only worktree `tools/round-46/gate.py`, then compare both exit code and receipt with the unmodified helper. Do not claim that test passed until captured with the required command, exit, stdout SHA-256, and UTC time.