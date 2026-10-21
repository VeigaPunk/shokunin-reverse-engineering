HOLDS

Scope: replay of the retained round-20 synthetic `compare-wasm-interfaces` observation (`scope=both`), evaluated from measured source S `5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9`.

**Observation — source at S.** Read the retained receipt, both inspect records, and comparison output with `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin --no-optional-locks show 5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9:<path>` (exit 0 for each). Receipt `.ufo/waves/round-20/evidence/c2/wasm-compare/compare-synth-both.receipt.json:2-8,10-20,28-31,40-44` records the argv, two synthetic carrier hashes, original input SHA-256 `42706f9a6a6554eac2f37c03e095e28370a9847196aa1e8e6110cefb8c553777` (13,717 bytes), and stdout SHA-256 `6859943b5f2b4377c77b9a1ed57ad1f88b53bbced56185c39ccc7beea1f92e67` (3,746 bytes). The retained complete inspect inputs are `.ufo/waves/round-20/evidence/c2/wasm-compare/inspect-synth-v1.stdout.txt:1` and `.ufo/waves/round-20/evidence/c2/wasm-compare/inspect-synth-v2.stdout.txt:1`; original comparison output is `.ufo/waves/round-20/evidence/c2/wasm-compare/compare-synth-both.stdout.txt:1`.

Rebuilt compact input JSON from those two source-at-S inspect Evidence records as `{left, right, scope: "both"}` plus one newline: 13,717 bytes; SHA-256 exactly matched the receipt. In `/tmp/kr20-wasm-compare-replay-3j3zuwp2` (created with `tempfile.mkdtemp`, removed after the run), ran:

```text
cwd=/tmp/kr20-wasm-compare-replay-3j3zuwp2
REA_WABT_BIN_DIRECTORY=/home/vgpnk/.local/opt/wabt-1.0.42/bin npx -y rea-agents@6.5.0 compare-wasm-interfaces /tmp/kr20-wasm-compare-replay-3j3zuwp2/synth-both.json --json
exit 0
```

Replay stdout was 3,746 bytes with the exact receipt SHA-256; stderr was empty; stdout matched the source-at-S retained output byte-for-byte. Observed evidence ID `ev_2529e50816c83bb2f37c596678299e223a27ccca696672596a847397ada43351` matched, and summary matched exactly: `{added:1, removed:1, changed:1, unchanged:1, unknown:0}`.

**Inference.** This falsification attempt did not disprove reproducibility of this retained synthetic comparison. It is bounded to the synthetic pair and `complete-within-inputs` comparison result; it does not establish runtime/ABI compatibility or, by itself, the broader C2 coverage claim. No install/update command was run; REA was invoked with the pinned `npx` package required by the contract.